# 멀티 repo 구조 (Stage 7)

## 지금 조직에 있는 repo

| repo | 담는 것 | 분리 이유 (Part 3 축) |
|---|---|---|
| `github_tutorial` | 이 연습장 자체 | — |
| `robot-stack` | ROS 2 코어 스택 (interfaces / drivers / control / bringup) | — (기준점) |
| `firmware-motor` | 구동 모터 MCU 펌웨어 | **2 툴체인, 3 릴리스 주기, 7 인증** |
| `robot-config-model-a` | 기종별 파라미터·캘리브레이션 | **3 릴리스 주기** |
| `releases` | 버전 조합 매니페스트 | **7 추적성** |
| `.github` | 조직 공통 워크플로·템플릿 | 재사용 워크플로의 단일 소스 |

핵심 원칙은 하나다.

> **"같은 rosbag 을 재생했을 때 결과가 바뀌는 코드"는 한 repo 에 둔다.**
> 그 바깥(펌웨어, 클라우드, UI, 학습)은 분리한다.

## 왜 firmware-motor 만 따로인가

팀 규모가 아니라 아키텍처 때문이다.

```
robot-stack     colcon + Python        주 단위 릴리스     인증 대상 아님
firmware-motor  arm-none-eabi + Make   분기 단위 릴리스   기능안전 대상
```

**하나의 CI 로 묶을 수 없다.** 빌드 명령도, 러너도, 테스트 방식(HIL)도 다르다.

반대로 `robot-stack` 안의 `interfaces` / `control` 은 **메시지 하나 바꾸면 같이 바뀐다.**
Part 3 의 축 4(변경 결합도)가 "합쳐라"라고 말하는 경우다.
이걸 쪼개면 메시지 하나 바꿀 때 PR 을 여러 개 열어야 한다 — Part 4-10 의 첫 번째 안티패턴이다.

## 두 가지 "함께"를 구분한다

| 질문 | 답하는 파일 |
|---|---|
| 무엇이 **함께 빌드**되는가 | `robot.repos` / `dev.repos` |
| 무엇이 **함께 릴리스**되는가 | `releases/model-a/<version>.yaml` |

`firmware-motor` 는 `.repos` 에 없지만 릴리스 매니페스트에는 있다. 같은 로봇에 올라가지만
같은 워크스페이스에서 빌드되지는 않기 때문이다. **둘은 다른 질문이다.**

## 워크스페이스 조립

```bash
pip install vcstool

mkdir -p ws/src && cd ws
vcs import src < ../robot.repos      # 릴리스 조합 (태그 고정)
vcs import src < ../dev.repos        # 개발 조합 (main)
```

확인:

```bash
vcs custom src --git --args describe --tags
```

### ⚠️ `.repos` 는 ASCII 로만 쓴다

vcstool 은 이 파일을 **플랫폼 기본 인코딩**으로 연다. 한국어 Windows(cp949)에서
한글 주석이 들어 있으면 이렇게 죽는다.

```
UnicodeDecodeError: 'cp949' codec can't decode byte 0xed
```

`PYTHONUTF8=1` 로 우회는 되지만, **환경변수에 의존하면 팀원 PC 마다 다르게 동작한다.**
매니페스트는 기계가 읽는 파일이므로 ASCII 로 유지하고, 설명은 이 문서에 둔다.

> 규칙을 사람이 지키게 하지 말고 파일이 지키게 한다 — Stage 2~3 에서 배운 것과 같다.

## 기종이 여러 개가 되면

**절대 stack 을 fork 하지 않는다.**

```
robot-stack                     공통 코드. 기종 무관. 100% 공유
   ├── robot-config-model-a     params / calibration
   ├── robot-config-model-b
   └── robot-config-dev-rig     개발 지그
```

코드에 `if (model == "A")` 가 들어가기 시작하면 이미 설계가 틀린 것이다.
정말 동작이 달라야 하면 플러그인 인터페이스로 교체한다.

기종을 추가한다는 것은 **repo 하나와 `.repos` 한 줄이 늘어나는 일**이어야 한다.

## 언제 코어 스택을 더 쪼개나

**40명 넘기 전까지 참는다.** 로봇 조직에서 가장 흔한 실패는 너무 일찍 쪼개서
인터페이스 변경 한 번에 5개 repo 의 PR 을 동시에 열어야 하는 상태가 되는 것이다.

판단 기준은 인원수가 아니라 **"PR 하나에 두 repo 를 동시에 고쳐야 하는 일이 잦은가"** 이다.
잦다면 잘못 쪼갠 것이고, 6개월 동안 따로만 바뀌었다면 합쳐 둘 이유가 없다.

git log 를 분석해 "함께 변경되는 디렉터리"를 뽑아보면 실제 경계가 보인다.
