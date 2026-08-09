"""동기화 스크립트의 판단 로직 테스트.

네트워크를 타는 부분(Notion/GitHub API)은 테스트하지 않는다. 대신 **무엇을 쓸지
결정하는 규칙**만 고정한다. 여기가 틀리면 Notion 이 조용히 거짓말을 하게 된다.
"""

import pytest
from tools.sync_notion import (
    STATUS_DONE,
    STATUS_IN_PROGRESS,
    STATUS_ON_HOLD,
    decide_status,
)


def test_closed_with_no_remaining_issues_is_done():
    assert decide_status("closed", "completed", open_issues=0) == STATUS_DONE


def test_not_planned_becomes_on_hold():
    """not_planned 로 닫은 것은 '했다'가 아니라 '안 하기로 했다'이다."""
    assert decide_status("closed", "not_planned", open_issues=0) == STATUS_ON_HOLD


def test_reopened_is_in_progress():
    assert decide_status("open", "reopened", open_issues=0) == STATUS_IN_PROGRESS


@pytest.mark.parametrize("state_reason", ["completed", "not_planned", ""])
def test_remaining_open_issues_win(state_reason):
    """하나의 REQ 에 이슈가 여러 개일 때, 하나 닫혔다고 완료가 아니다.

    이 규칙이 없으면 REQ-003 의 이슈 3건 중 1건만 닫혀도 Notion 이 '완료'가 된다.
    """
    assert decide_status("closed", state_reason, open_issues=2) == STATUS_IN_PROGRESS


def test_state_reason_missing_defaults_to_done():
    """오래된 이슈는 state_reason 이 비어 있을 수 있다. 닫혔으면 완료로 본다."""
    assert decide_status("closed", "", open_issues=0) == STATUS_DONE
