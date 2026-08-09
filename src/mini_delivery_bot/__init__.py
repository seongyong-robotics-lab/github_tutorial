"""mini-delivery-bot — GitHub 실습용 가상 프로젝트.

공개 API는 아래 두 모듈로 나뉜다.

- :mod:`mini_delivery_bot.battery` — 전압/전류로부터 충전 상태와 잔여 시간을 계산하고
  텔레메트리 페이로드를 만든다.
- :mod:`mini_delivery_bot.safety` — 라이다 최근접 거리와 속도로 정지 여부를 판단한다.

두 모듈 모두 **ROS 비의존 순수 로직**이다. ROS 노드 래퍼는 별도 파일로 분리해
이 계층을 ROS 없이 단위 테스트할 수 있게 유지한다.
"""

from mini_delivery_bot.battery import (
    battery_level,
    battery_telemetry,
    remaining_minutes,
    state_of_charge,
)
from mini_delivery_bot.safety import should_stop, stopping_distance

__version__ = "0.1.0"

# 토픽 발행 주기(Hz). /battery_state 는 상태 표시용이라 낮게 잡는다.
BATTERY_STATE_PUBLISH_HZ = 1.0

__all__ = [
    "BATTERY_STATE_PUBLISH_HZ",
    "__version__",
    "battery_level",
    "battery_telemetry",
    "remaining_minutes",
    "should_stop",
    "state_of_charge",
    "stopping_distance",
]
