"""GitHub 이슈 상태를 Notion SYS-REQ DB 의 `구현 상태` 로 반영한다.

경계 규칙 (docs/notion-boundary.md):
    요구사항의 내용과 승인 여부  -> Notion 이 원본. **이 스크립트는 건드리지 않는다.**
    작업의 진행 상태             -> GitHub 이 원본. Notion 의 `구현 상태` 는 미러.

그래서 `승인 상태` 는 절대 쓰지 않는다. 하나의 select 에 승인과 진행을 섞어 담으면
자동화가 사람의 판단(승인 여부)을 덮어쓰게 된다.

여러 이슈가 하나의 REQ 에 걸릴 수 있으므로, 이슈 하나가 닫혔다고 바로 `완료` 로
만들지 않는다. 같은 REQ 를 참조하는 **열린 이슈가 남아 있으면 `구현 중`** 이다.

환경변수:
    NOTION_TOKEN, NOTION_DB_ID   Notion 연결 토큰과 대상 DB
    GITHUB_TOKEN, GITHUB_REPOSITORY   남은 열린 이슈를 세기 위해 필요
    ISSUE_TITLE, ISSUE_URL, ISSUE_STATE, ISSUE_STATE_REASON
"""

from __future__ import annotations

import os
import re
import sys

import requests

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
GITHUB_API = "https://api.github.com"
TIMEOUT = 30

REQ_PATTERN = re.compile(r"REQ-\d{3,}")

# Notion 속성 이름. DB 스키마와 어긋나면 여기만 고친다.
PROP_REQ_ID = "REQ ID"
PROP_IMPL_STATUS = "구현 상태"

STATUS_IN_PROGRESS = "구현 중"
STATUS_DONE = "완료"
STATUS_ON_HOLD = "보류"


class SyncError(RuntimeError):
    """동기화를 중단해야 하는 상황. 워크플로를 실패시킨다."""


def log(message: str) -> None:
    print(message, flush=True)


def notion_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def find_page(token: str, db_id: str, req_id: str) -> str | None:
    """`REQ ID` 가 req_id 인 페이지의 id. 없으면 None."""
    resp = requests.post(
        f"{NOTION_API}/databases/{db_id}/query",
        headers=notion_headers(token),
        json={
            "filter": {"property": PROP_REQ_ID, "title": {"equals": req_id}},
            "page_size": 2,
        },
        timeout=TIMEOUT,
    )

    if resp.status_code == 404:
        raise SyncError(
            "Notion DB 를 찾을 수 없습니다 (404).\n"
            "  토큰이 틀렸을 수도 있지만, 대개는 DB 에 연결이 추가되지 않은 경우입니다.\n"
            "  SYS-REQ DB -> ··· -> 연결 -> 통합 추가 를 확인하세요."
        )
    if resp.status_code == 401:
        raise SyncError("Notion 토큰이 거부되었습니다 (401). NOTION_TOKEN 시크릿을 확인하세요.")
    resp.raise_for_status()

    results = resp.json().get("results", [])
    if len(results) > 1:
        # 같은 REQ ID 가 둘 이상이면 어느 쪽을 갱신해도 틀린다. 사람이 고쳐야 한다.
        raise SyncError(f"{req_id} 페이지가 DB 에 2개 이상 있습니다. 중복을 먼저 정리하세요.")
    return results[0]["id"] if results else None


def count_open_issues(repo: str, req_id: str, token: str | None) -> int:
    """같은 REQ 를 제목에 달고 아직 열려 있는 이슈 수."""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    resp = requests.get(
        f"{GITHUB_API}/search/issues",
        headers=headers,
        params={"q": f"repo:{repo} {req_id} in:title is:issue is:open"},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return int(resp.json().get("total_count", 0))


def decide_status(state: str, state_reason: str, open_issues: int) -> str:
    """GitHub 쪽 사실로부터 Notion 에 쓸 `구현 상태` 를 결정한다.

    판단 근거는 **개별 이슈가 아니라 REQ 전체**다. 하나의 REQ 에 이슈가 여러 개
    걸릴 수 있으므로, 지금 이벤트가 난 이슈만 보고 결정하면 틀린다.
    """
    if open_issues > 0:
        # 아직 남은 일이 있다. 개별 이슈가 어떻게 닫혔든 REQ 는 진행 중이다.
        return STATUS_IN_PROGRESS
    if state == "open":
        # 방금 열린/다시 열린 이슈. 검색 인덱스 반영이 늦어 open_issues 가
        # 0 으로 나올 수 있으므로 여기서 한 번 더 막는다.
        return STATUS_IN_PROGRESS
    if state_reason == "not_planned":
        return STATUS_ON_HOLD
    return STATUS_DONE


def update_status(token: str, page_id: str, status: str) -> None:
    resp = requests.patch(
        f"{NOTION_API}/pages/{page_id}",
        headers=notion_headers(token),
        json={"properties": {PROP_IMPL_STATUS: {"select": {"name": status}}}},
        timeout=TIMEOUT,
    )
    if resp.status_code == 400:
        raise SyncError(
            f"Notion 이 값을 거부했습니다: {status}\n"
            f"  `{PROP_IMPL_STATUS}` select 에 그 옵션이 있는지 확인하세요.\n"
            f"  응답: {resp.text[:300]}"
        )
    resp.raise_for_status()


def main() -> int:
    notion_token = os.environ["NOTION_TOKEN"]
    db_id = os.environ["NOTION_DB_ID"]
    title = os.environ["ISSUE_TITLE"]
    issue_url = os.environ.get("ISSUE_URL", "")
    state = os.environ.get("ISSUE_STATE", "closed")
    state_reason = os.environ.get("ISSUE_STATE_REASON") or ""
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    gh_token = os.environ.get("GITHUB_TOKEN")

    match = REQ_PATTERN.search(title)
    if not match:
        # 모든 이슈가 요구사항에서 나오지는 않는다. 정상 종료.
        log(f"[skip] 제목에 REQ ID 가 없습니다: {title}")
        return 0

    req_id = match.group(0)

    try:
        page_id = find_page(notion_token, db_id, req_id)
        if page_id is None:
            # 오타난 REQ ID 를 조용히 넘기면 "동기화됐다고 믿었는데 아니었던"
            # 상태가 쌓인다. 여기서는 반드시 실패해야 한다.
            raise SyncError(
                f"Notion 에 {req_id} 페이지가 없습니다.\n"
                f"  이슈: {issue_url}\n"
                f"  제목의 REQ ID 오타이거나, DB 에 요구사항이 아직 없습니다."
            )

        open_issues = count_open_issues(repo, req_id, gh_token) if repo else 0
        status = decide_status(state, state_reason, open_issues)

        update_status(notion_token, page_id, status)
        log(f"[ok] {req_id} -> {status} (남은 열린 이슈 {open_issues}건)")
        return 0

    except SyncError as exc:
        log(f"::error::{exc}")
        return 1
    except requests.RequestException as exc:
        log(f"::error::API 호출 실패: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
