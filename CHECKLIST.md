# 진행 체크리스트

매 세션 여기서 시작합니다. 시간이 아니라 **완료 조건**으로 진행하세요.

- 한 Stage의 체크박스가 다 채워지면 다음으로
- 막혔다고 건너뛰지 말 것. 단, **한 Stage에 3주 이상 머물지도 말 것**
- 세션 끝에 `docs/learning-log.md`에 3줄

---

## Stage 0 — 준비운동

- [ ] GitHub 계정에 2FA 활성화 ← **웹 UI, 직접 (유일한 미완료 항목)**
- [x] `gh` CLI 설치 (v2.97.0, winget) + `gh auth login` (Seong-Yong-Park, HTTPS)
- [x] `gh auth status` 정상 — 스코프 `gist, read:org, repo, workflow`
- [x] 이 repo를 `git init` → commit → `gh repo create --private --push`
      → https://github.com/Seong-Yong-Park/github_tutorial
- [x] `pip install -e ".[dev]"` 후 `pytest -q` 통과 확인 (9 passed, ruff clean)
- [x] `docs/notion-boundary.md`의 "직접 채우기" 3줄 작성

**✅ 완료 조건** — `gh auth status` 성공 + 경계 규칙이 적혀 있음

---

## Stage 1 — 혼자 굴리기

- [x] 기본 라벨 8개 삭제하고 5개만 새로 생성 (`bug` `feature` `chore` `idea` `blocked`)
- [x] `docs/stage1-issues.md`의 이슈 10개 생성 (#1~#10, 웹 UI 대신 `gh api --input`)
- [x] Project `mini-delivery-bot` 생성 → Board 뷰 → 이슈 10개 (import 옵션으로 일괄)
- [x] Built-in workflow 켜기 (*Item closed → Done*, *Auto-archive*) — 총 8개 활성
- [x] 이슈 #3(README)을 `main`에 직접 커밋해서 처리, 메시지에 `Fixes #3` → bd68518
- [x] 이슈가 자동으로 닫히고 보드에서 Done으로 이동하는 것 **눈으로 확인** (Todo 9 / Done 1)
- [~] 💥 `status: in-progress` 라벨 실습 — **의도적으로 건너뜀.** 결론은 아래에 기록
- [x] `_answers/stage1/seed_issues.sh` 대신 `gh api --input` 방식으로 진행 (한글 인코딩 이슈 회피)

**✅ 완료 조건** — 커밋 메시지만으로 이슈가 닫히고 보드가 움직이는 것을 확인함 → **달성**

> **건너뛴 실습의 결론 (자가 점검 질문 1번의 답)**
> 라벨은 배타성을 강제하지 못하고 변경 이력이 없다. `status: in-progress`와 `status: done`이
> 동시에 붙어도 GitHub은 막지 않고, 언제 붙었는지도 남지 않아 번다운·사이클타임 계산이 불가능하다.
> 상태는 Project의 Status 필드(single-select + 이력 보존)로 관리한다.
>
> **동작 확인된 연쇄**: `push(Fixes #3)` → GitHub이 커밋 메시지 파싱 → 이슈 종료
> → Projects `Item closed` 워크플로 → `Status = Done` → Board 뷰 재배치.
> 셋 다 별개 장치라 하나만 꺼져도 거기서 멈춘다. ①은 **default branch에 들어올 때만** 동작.

---

## Stage 2 — PR 워크플로

- [x] `git switch -c fix/imu-nan` → `safety.py`의 NaN 버그 수정 → PR #12 (CLI로)
- [x] `tests/test_safety.py` 주석 테스트 해제 + 속도 NaN·inf 회귀 테스트 추가 (12 passed)
- [x] 자기 PR에 **라인 코멘트** 달아보기 (`safety.py:34`)
- [x] Draft PR 만들어보고 Ready for review로 전환
- [x] `.github/pull_request_template.md` 작성 → `_answers/stage2/`와 비교 완료
- [x] Repo Settings에서 **Squash merge만 허용**하도록 변경 (+ head 브랜치 자동 삭제)
- [x] Ruleset `main-protection` 생성 — `pull_request` / `deletion` / `non_fast_forward`

> **⚠️ 요금제 제약 — 이 단계에서 실제로 막힌 것**
> GitHub Free 플랜에서 Ruleset(브랜치 보호)은 **public repo에서만** 동작한다.
> private 상태에서는 규칙을 만들어도 강제되지 않고 `main` 직접 push가 그대로 통과한다
> (`GET /rules/branches/main` → 403 *Upgrade to GitHub Pro or make this repository public*).
> 그래서 이 repo를 **public으로 전환**했다.
>
> 전환 전에 사내 식별 정보(제품 코드명, 내부 호스트명)를 문서에서 일반화하고
> `git filter-branch`로 **커밋 히스토리까지 재작성**했다. 그런데 그것만으로는 부족했다 —
> 이슈 타임라인의 *"closed this in \<sha\>"* 링크가 재작성 전 커밋을 영구 참조하고,
> GitHub은 force push 후에도 그 객체를 SHA로 계속 서빙한다.
> 결국 **repo를 삭제하고 재생성**해야 원격에서 완전히 사라졌다.
>
> → 교훈: repo의 **공개 범위(Part 3의 경계 축 5번)를 첫 커밋 전에** 정할 것.
> 나중에 바꾸면 히스토리·이슈·PR이 전부 정리 대상이 된다.
- [x] 💥 `main`에 직접 `git push` 시도 → `GH013: Repository rule violations found` 거부 확인
- [x] 💥 브랜치 3개에서 같은 줄 수정 후 순서대로 머지 → 충돌 2회 해결 (PR #13/#14/#15)

**✅ 완료 조건** — main 직접 push 불가 / 머지된 PR **5개** / 전부 squash (히스토리 선형) → **달성**

> **충돌 실습에서 실제로 배운 것**
> 세 브랜치가 `SAFETY_MARGIN_M` 을 각각 0.30 / 0.22 / 0.18 로 고쳤다.
> 셋 다 분기 시점에는 `MERGEABLE / CLEAN` 이었고, **첫 PR이 머지된 직후** 나머지 둘이
> `CONFLICTING / DIRTY` 로 바뀌었다. 충돌은 브랜치를 만들 때가 아니라 **머지 순서에 의해**
> 사후적으로 생긴다.
>
> 해결하면서 값 하나를 고르는 대신 **상·하한의 근거를 주석 블록으로 승격**시켰더니,
> 세 번째 충돌에서 그 블록이 곧바로 판단 기준이 됐다 — 0.18 이 명시된 하한 0.20 을
> 위반한다는 게 코드만 보고 드러나서, 0.20 으로 수렴시켰다.
>
> → 충돌 해결은 "어느 쪽을 고를까"가 아니라 **"왜 갈렸는지를 코드에 남길 기회"**다.
> 짧게 살고 빨리 머지하는 브랜치(GitHub Flow)를 권하는 이유이기도 하다.
> 세 브랜치가 2주씩 살아 있었다면 이 충돌은 훨씬 크고 근거는 이미 잊혔을 것이다.

---

## Stage 3 — 자동화와 게이트

- [x] `.github/workflows/ci.yml` 작성 (ruff + pytest, job name `lint-and-test`)
- [x] Ruleset에 **Require status checks to pass** 추가하고 `lint-and-test` 지정
- [x] `.github/ISSUE_TEMPLATE/bug_report.yml` 작성 (재현/현상/기대 필수)
- [x] `.github/ISSUE_TEMPLATE/feature_request.yml` 작성 (**REQ ID 필수 입력**)
- [x] `.github/workflows/add-to-project.yml` 추가 → 이슈 #20 이 자동으로 보드에 오름
- [x] 💥 lint 에러가 있는 PR(#18) → `mergeStateStatus=BLOCKED`, CLI 머지도 거부
- [x] 💥 Actions 로그에서 실패 스텝(`Lint (ruff)`)과 원인 줄(`battery.py:9:8`) 확인
- [x] `_answers/stage3/`와 비교 — `cache: pip`, 심각도 드롭다운을 정답지에서 가져옴

**✅ 완료 조건** — 깨진 코드가 물리적으로 머지 불가 / 이슈 폼에 REQ ID 칸이 있음 → **달성**

> **① `mergeable` 과 `mergeStateStatus` 는 다른 축이다**
> | 상황 | `mergeable` | `mergeStateStatus` |
> |---|---|---|
> | Stage 2 충돌 (#14, #15) | `CONFLICTING` | `DIRTY` |
> | Stage 3 lint 실패 (#18) | `MERGEABLE` | `BLOCKED` |
>
> 전자는 **git 이 합칠 수 있는가**, 후자는 **정책이 허락하는가**. #18 은 충돌이 전혀 없는데도 막혔다.
>
> **② status check 이름 = job 의 `name`**
> 워크플로 이름(`CI`)도 step 이름(`Lint (ruff)`)도 아니다. Ruleset 에 지정할 context 는
> job 의 `name` 값(`lint-and-test`)이다. 여기서 한 번은 반드시 헷갈린다.
>
> **③ 워크플로 파일을 어디서 읽는가 — 시크릿 정책과 한 쌍**
> | 이벤트 | 파일 출처 | fork PR 에 시크릿 |
> |---|---|---|
> | `pull_request` | 머지 커밋 (PR 이 추가한 워크플로도 실행됨) | 주지 않음 |
> | `pull_request_target` | base 브랜치 (PR 이 고쳐도 무시) | 줌 |
>
> `pull_request_target` 이 base 에 고정되는 이유가 보안이다. 시크릿을 주면서 워크플로 수정까지
> 허용하면 토큰을 훔쳐가는 PR 이 가능해진다. (PR #19 에서 실제로 확인)
>
> **④ 기본 `GITHUB_TOKEN` 의 사정거리는 repo 안까지**
> Projects 는 repo 가 아니라 사용자/조직에 속한 리소스라 범위 밖이다.
> 그래서 `project` 스코프 PAT 을 별도 시크릿(`ADD_TO_PROJECT_PAT`)으로 주입해야 한다.

---

## Stage 4 — 계층과 계획

- [x] 큰 이슈 생성 — **#22 자율 주행 스택 1차 통합**
- [x] **sub-issue 5개** 붙이기 (#1 #4 #5 #7 #9) — 새로 만들지 않고 기존 이슈를 연결
- [x] 진행률 바 확인 → `0/5(0%)` → `1/5(20%)` → `2/5(40%)` 자동 갱신
- [x] Milestone `v0.1 - 실내 주행 데모` (마감 2026-09-04) + 이슈 5건 배정
- [x] 필드 추가 — `Priority`(P0/P1/P2), `Estimate`(number), `Sprint`(iteration, **1주**)
- [x] 뷰 3개 — `Board` / `My Items`(`assignee:@me`) / `Backlog`(Table + Priority 정렬)
- [x] Table 뷰 **Show hierarchy** — Epic 아래 sub-issue 접힘/펼침 확인
- [x] Insights 차트 1개 (Status × Priority)

### 스프린트 — 압축 진행

- [x] 스프린트 1 — 이슈 5건 배정 (#4 #5 #7 #9 #20), **계획 13점**
- [~] 매일 카드 이동 — **압축 진행이라 생략.** 대신 상태 전이를 한 세션에 시연
- [x] 스프린트 1 종료 — 미완료 3건을 Sprint 2로 이월 (`In Progress` 상태 보존)
- [~] 번다운 차트 — Insights 기본 `Burn up` 차트가 이번 주(~Aug 13) 자동 축적됨
- [x] 스프린트 2 — 1차 결과 반영해 **양을 줄임** (10점 → 5점)

**✅ 완료 조건** — 스프린트 2회 완주 + 이월 처리 경험 + 번다운 확인 → **압축 달성**

> **압축 스프린트가 실제로 보여준 것**
>
> | | 점수 | 비율 |
> |---|---|---|
> | 계획 (Sprint 1) | 13점 / 5건 | 100% |
> | 완료 | **3점 / 2건** | **23%** |
> | 이월 (Sprint 2) | 10점 / 3건 | 77% |
>
> 관측 velocity 가 3점인데 이월만 10점이었다. 그대로 두면 Sprint 2 도 확정적으로 이월된다.
> 그래서 조정은 **더하는 것이 아니라 빼는 것**이었다 — `#9`(5점)를 백로그로 되돌려
> Sprint 2 를 5점으로 낮췄다. 계획이란 담을 양을 정하는 게 아니라 **못 담을 것을 골라내는 일**이다.
>
> **추정의 두 방향 오차가 동시에 나타났다**
> - 과대 추정: 13점을 계획했으나 3점 완료 (약 4배)
> - 과소 추정: Epic `#22` 를 13점으로 봤으나 sub-issue 합계는 15점.
>   **쪼개면 항상 커진다** — 뭉뚱그려 볼 때 안 보이던 일이 드러나기 때문
>
> **단, 이 숫자를 본인의 실제 추정 배율로 읽으면 안 된다.** `#4` 는 실제 구현 없이
> 완료 처리한 시뮬레이션이고, 압축이라 하루에 끝냈다. 진짜 측정치는 `Burn up` 차트가
> 이번 주 동안 쌓아줄 곡선이다.
>
> **iteration 필드는 API 로 주기 설정이 불가능하다.** GraphQL 로 필드 생성까지는 되지만
> (`createProjectV2Field(dataType: ITERATION)`) duration 과 iteration 목록을 넣는 뮤테이션이
> 없어 UI 에서만 가능하다. "Projects v2 는 GraphQL API 만 지원한다"는 말이
> "API 가 전부를 덮는다"는 뜻은 아니다.

---

## Stage 5 — Organization 전환

- [x] 무료 Organization 생성 — `seongyong-robotics-lab`
- [x] `github_tutorial` repo를 Org로 **transfer** — 부속물 전부 보존
- [x] Team 2개 — `autonomy`, `firmware`. 본인 maintainer + repo push 권한
- [x] `.github/CODEOWNERS` 작성 → PR #26 에서 `requested_teams: autonomy` 확인
- [x] **Issue Types** — 기본 `Task`/`Bug`/`Feature` + `Epic` 추가 (API 로 생성 가능)
- [x] 기존 이슈 12건에 Issue Type 부여, `#22` 는 `Epic`
- [x] **조직 Project** `2026 Roadmap` (orgs/1) + `Start date`/`Target date` 필드
- [x] 같은 Epic `#22` 가 조직 로드맵 + 팀 보드에 동시 존재 (복사 아님)
- [x] Project 템플릿 `Team Sprint Board Standard` (orgs/2) → 그 템플릿으로 `#4` 생성.
      뷰 2개(Backlog/Board) + 필드 4개가 그대로 복제되고 **항목은 0개** — 구조만 복제됨
- [x] Roadmap 뷰 레이아웃 + Date fields 지정
- [x] 조직 Project 의 `Auto-add sub-issues to project` 끄기 (팀 보드에서는 켜둠)

**✅ 완료 조건** — 한 이슈가 두 보드에 동시 존재 / 경로별 리뷰어 자동 지정 → **달성**

> **① transfer 는 무손실, 재생성은 손실**
> 같은 repo 를 옮기는 것과 지우고 다시 만드는 것은 결과가 완전히 다르다.
>
> | | repo 삭제 후 재생성 (Stage 2) | Org 로 transfer (Stage 5) |
> |---|---|---|
> | 이슈 / PR | 전부 소실 | 유지 (번호까지) |
> | 머지 설정 | **초기화됨** | 유지 |
> | Ruleset / Secret / 라벨 / 마일스톤 | 소실 | 유지 |
>
> **② Issue Type — "정의는 위, 값은 아래"**
> ```
> [정의] GET /orgs/{org}/issue-types  →  id=35899875 name=Bug   ← 조직에 한 벌
> [값]   GET /repos/.../issues/8      →  type:{id:35899875}     ← 이슈는 포인터만
> ```
> 이 구조가 GitHub 전반에 반복된다. 달라지는 건 정의가 얼마나 높이 있느냐뿐이다.
>
> | | 정의가 사는 곳 | 값이 사는 곳 |
> |---|---|---|
> | Label | repo | 이슈 |
> | Issue Type | **조직** | 이슈 |
> | Project 필드 | Project | project item |
>
> 정의를 위로 올리면 "어긋나지 않게 조심하자"가 "어긋날 수가 없다"로 바뀐다.
> repo 가 10개여도 `Bug` 는 물리적으로 하나다.
>
> **③ 라벨 5개 → 3개**
> `bug`/`feature` 는 Issue Type 과 정면으로 겹쳐 삭제했다. 남은 `chore`/`idea`/`blocked` 는
> Type 에 대응하는 개념이 없는 **성질**이다. 판단 기준: *"A이면서 동시에 B일 수 있는가?"*
> — 없으면 Type(배타적), 있으면 Label.
>
> **④ PR 은 Issue Type 을 가질 수 없다**
> `type` 필드 자체가 없다. 릴리스 노트를 PR 라벨로 분류하려면 PR 전용 라벨이 따로 필요하다.
> Stage 7 에서 릴리스를 만들 때 다시 판단한다.
>
> **⑤ Project 는 조직으로 이전할 수 없다**
> repo 는 transfer 가 되지만 Project 는 안 된다. 팀 보드(`users/.../projects/8`)가 개인
> 소유로 남은 이유다. 실무라면 **처음부터 조직 소유로 만들어야 한다** — 개인 계정에 두면
> 그 사람이 떠날 때 보드가 함께 사라진다. 템플릿 기능도 조직 Project 전용이다.
>
> **⑦ 템플릿은 "구조"만 복제한다**
> `Team Sprint Board Standard` → `#4` 복제 결과: 뷰·필드·워크플로 설정은 따라오고
> **항목(이슈)과 Insights 차트는 따라오지 않는다.** 일이 담긴 보드를 복사하는 게 아니라
> 새 팀이 같은 규격으로 시작하게 만드는 장치다.
> 필드 이름이 `Estimate`/`Points`/`Size` 로 갈라지는 것을 막는 가장 효과적인 방법.
>
> **⑥ 기본 워크플로가 로드맵을 오염시켰다**
> Epic `#22` 하나만 넣었는데 항목이 6개가 됐다. `Auto-add sub-issues to project` 가
> 켜져 있어 sub-issue 5건을 따라 넣었기 때문. **로드맵은 Epic 만** 있어야 2계층이 성립한다.
> 두 프로젝트의 워크플로 설정은 서로 달라야 한다 — 로드맵은 Epic 만, 팀 보드는 Task 까지.

---

## Stage 6 — Notion ↔ GitHub 연결

### 6-1. 수동 규약 (최소 2주는 손으로)

- [ ] Notion에 `SYS-REQ` DB 생성 — 속성: `ID`, `요구사항`, `상태`, `GitHub Issue`
- [ ] 요구사항 8개를 `REQ-001` ~ `REQ-008`로 작성
- [ ] 각 REQ에 대응하는 GitHub 이슈를 손으로 생성, 제목은 `[REQ-003] ...` 형식
- [ ] Notion REQ 페이지에 이슈 URL 붙여넣기
- [ ] 이슈를 닫을 때 Notion 상태도 손으로 변경
- [ ] **2주 뒤 자문: 어디가 제일 귀찮았나?** → 그 지점이 자동화할 곳

### 6-2. 반자동

- [ ] 이슈 템플릿의 REQ ID 칸을 실제로 채워서 사용
- [ ] PR 템플릿에도 REQ ID 줄 추가
- [ ] Notion REQ 페이지에 GitHub 검색 링크 저장
- [ ] 주 1회 "동기화 점검" 루틴 만들기

### 6-3. 자동화

- [ ] `_answers/stage6/notion-setup.md` 따라 Integration 생성 + DB Connections 연결
- [ ] repo Secrets에 `NOTION_TOKEN`, `NOTION_DB_ID` 등록
- [ ] `tools/sync_notion.py` 직접 작성 → 로컬에서 먼저 테스트
- [ ] `.github/workflows/sync-notion.yml` 추가
- [ ] 실제 이슈를 닫아서 Notion 상태가 바뀌는지 확인
- [ ] 💥 존재하지 않는 REQ ID로 테스트 → 실패 로그 확인 → 에러 처리 보완
- [ ] 💥 양쪽에서 동시에 상태를 다르게 바꿔보고 **어느 쪽이 이기는지** 확인
- [ ] 그 결과로 `docs/notion-boundary.md` 다시 다듬기

**✅ 완료 조건** — 이슈를 닫으면 Notion이 자동으로 바뀜 + 원본 규칙이 문서화됨

---

## Stage 7 — 로봇 SW 멀티 repo 구조

- [ ] Org에 repo 3개 생성 — `robot-stack`, `firmware-motor`, `robot-config-model-a`
- [ ] `robot-stack`에 골격 디렉터리만 — `src/interfaces`, `src/drivers`, `src/control`, `src/bringup`
- [ ] `robot.repos` 작성 후 `vcs import`로 조립해보기
- [ ] 각 repo에 `v0.1.0` 태그
- [ ] `releases` repo 생성 + 매니페스트 YAML 작성
- [ ] GitHub Release 생성하고 매니페스트 첨부
- [ ] 크로스 repo 이슈 참조 — `firmware-motor` 이슈에서 `ORG/robot-stack#1` 언급
- [ ] `.github` repo에 재사용 워크플로 작성 → 다른 repo에서 `uses:`로 호출
- [ ] 💥 `.repos`의 태그를 `v9.9.9`로 바꿔 import → 에러 메시지 읽기

**✅ 완료 조건** — `.repos` 하나로 워크스페이스 조립 / 매니페스트로 "뭐가 올라갔나" 즉답

---

## Stage 8 — 팀 도입

- [ ] `CONTRIBUTING.md` 작성 — 브랜치·커밋·PR·이슈 규칙을 **1페이지로**
- [ ] 온보딩 체크리스트 작성 — "신규 팀원이 첫 PR을 올리기까지"
- [ ] Before/After 설득 자료 작성 (Notion)
- [ ] **파일럿 범위 확정** — repo 1개, 스프린트 1회, 기능 3개만
- [ ] 팀원 1명에게 제안하고 함께 한 스프린트 돌리기
- [ ] 회고 → 안 쓰이는 기능 **최소 1개 끄기**

**✅ 완료 조건** — 다른 사람이 CONTRIBUTING만 읽고 PR 가능 / 팀원 1명과 스프린트 1회 완주

---

## 마무리

- [ ] `docs/self-check.md`의 8개 질문에 문서 없이 답해보고 답을 적기
- [ ] 답이 막히는 Stage로 돌아가서 그 부분만 다시
