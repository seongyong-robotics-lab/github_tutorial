# 학습 로그

매 세션 끝에 3줄만. 이게 나중에 팀 온보딩 문서의 초안이 됩니다.

---

```
[YYYY-MM-DD] Stage N
오늘 한 것 :
막힌 것    :
다음 할 것 :
```

---

[2026-08-06] Stage 0
오늘 한 것 : gh CLI 설치 + auth, git init/identity 분리, venv(3.10) pytest 9 passed, 경계 규칙 3줄, private repo 생성·푸시 완료
막힌 것    : (1) 사내 pip 인덱스 DNS 실패 → `--index-url https://pypi.org/simple` 우회. (2) winget 설치 후 PATH가 VS Code 프로세스에 반영 안 됨 → 터미널이 아니라 에디터를 재시작해야 함. (3) 커밋 author에 사번이 박혀서 push 전에 filter-branch로 재작성
다음 할 것 : 2FA 활성화(웹) → Stage 1: 라벨 5개 정리, 이슈 10개 등록, Board 뷰, `Fixes #n`으로 이슈 자동 종료 확인

[2026-08-06] Stage 1 + Stage 2
오늘 한 것 : 라벨 5개·이슈 10개·Board 구성, `Fixes #3` 자동 종료 확인. public 전환 후 Ruleset 적용, NaN 버그 수정 PR(#12), 브랜치 3개 충돌 해결(#13~#15). 머지된 PR 5개 전부 squash
막힌 것    : (1) Free 플랜 private 에서는 Ruleset 이 강제되지 않음 — UI 로는 알 수 없고 실제로 push 해봐야 드러남. (2) repo 재생성 후 머지 설정(squash-only, head 자동 삭제)이 초기화되는 걸 놓쳐서 브랜치가 하나 남음. **repo 설정은 코드가 아니라서 히스토리에 안 남는다**
다음 할 것 : Stage 3 — CI 작성 후 Ruleset 에 status check 연결. 그 전에 Projects 의 `Auto-add to project` 워크플로를 꺼야 add-to-project 액션의 동작을 검증할 수 있음

[2026-08-07] Stage 3
오늘 한 것 : CI(ruff+pytest) 작성 → Ruleset 에 `lint-and-test` 필수 체크 등록 → 일부러 깨뜨린 PR(#18)이 BLOCKED 되는 것 확인 → 수정 push 로 CLEAN 전환. 이슈 폼 2종, add-to-project 액션(PAT 시크릿) 까지 완료
막힌 것    : PR #19 본문에 "워크플로는 base 기준으로 로드되니 이번엔 실행 안 된다"고 썼는데 **틀렸다.** `pull_request` 는 머지 커밋 기준이라 PR 이 추가한 워크플로도 실행된다. base 기준인 것은 `pull_request_target` 이고, 그건 fork PR 에 시크릿을 주기 때문에 그렇게 설계된 것. 파일 출처와 시크릿 정책이 한 쌍
다음 할 것 : Stage 4 — sub-issue 계층, Milestone, Project 필드(Priority/Estimate/Sprint), 뷰 3종, Insights. 이슈 #20(JSON Infinity)을 첫 sub-issue 실습 소재로 쓸 수 있음

[2026-08-07] Stage 4
오늘 한 것 : Epic #22 + sub-issue 5건(기존 이슈 연결), Milestone v0.1, 필드 3종, 뷰 3종, Insights 차트. 압축 스프린트 1회 — 계획 13점 중 3점 완료, 10점 이월, velocity 반영해 Sprint 2 를 5점으로 축소. #20 은 시뮬레이션이 아니라 실제로 고침(PR #23)
막힌 것    : (1) iteration 필드는 GraphQL 로 **생성만** 되고 주기 설정 뮤테이션이 없어 UI 필수. (2) `gh project field-create` 는 ITERATION 을 아예 거부. (3) sub-issue API 는 이슈 번호가 아니라 **내부 id** 를 요구 — repo 를 넘나드는 관계라 전역 id 여야 함. (4) PowerShell 에서 GraphQL 을 인자로 넘기면 따옴표가 깨짐 → `-F query=@파일` + 변수로 해결. `Set-Content -Encoding UTF8` 은 BOM 을 붙여서 파서가 거부함
다음 할 것 : Burn up 차트 Aug 13 확인. Stage 5 — Organization 생성, repo transfer, Team 2개, CODEOWNERS, Issue Types, 조직 Project(Roadmap)

[2026-08-09] Stage 5
오늘 한 것 : Org `seongyong-robotics-lab` 생성 → repo transfer(무손실) → Team 2개 + repo push 권한 → CODEOWNERS(PR #26 에서 팀 자동 지정 확인) → Issue Type 4종 부여 → 조직 Project `2026 Roadmap` 에 Epic #22 배치. bug/feature 라벨 삭제하고 Type 으로 일원화
막힌 것    : (1) **Project 는 조직으로 이전이 불가능하다.** repo 만 transfer 된다. 팀 보드가 개인 소유로 남았고, 템플릿 기능도 조직 Project 전용이라 쓸 수 없었다. 처음부터 조직 소유로 만들었어야 했다. (2) 조직 로드맵에 Epic 하나만 넣었는데 `Auto-add sub-issues to project` 기본 워크플로가 하위 5건을 따라 넣어 로드맵이 오염됐다. (3) PR 은 Issue Type 을 가질 수 없어서 릴리스 노트 라벨 분류는 별도 대책이 필요하다
다음 할 것 : Stage 6 — Notion SYS-REQ DB, REQ ID 규약(수동 2주), 반자동, 그리고 Actions + Notion API 자동 동기화. 커리큘럼이 "핵심"이라 부르는 단계

[2026-08-10] Stage 6
오늘 한 것 : SYS-REQ DB(REQ-001~008) → 제목 규약 백필 → REQ ID 자동 삽입 워크플로 → 검색 링크 → sync_notion.py + 워크플로. 💥 REQ-999 실패 재현, 💥 양쪽 동시 변경 실험까지 완료
막힌 것    : (1) 정답지대로 만들면 **경계 규칙을 자동화가 어긴다.** `상태` 한 칸에 승인 여부(Notion 원본)와 진행 상태(GitHub 원본)가 섞여 있어서, 초안 요구사항이 완료로 덮어써진다 → `승인 상태`/`구현 상태` 분리. **경계는 문서가 아니라 스키마에 있어야 한다.** (2) Notion 의 `ID` 는 예약어라 API 로 값을 못 넣음 → `REQ ID` 로 개명. (3) `ALTER COLUMN SET` 이 기존 속성을 바꾸지 않고 `승인 상태 1` 을 새로 만듦. DROP+RENAME 을 같은 배치에 넣으면 `승인 상태 2` 가 됨 → 두 번 나눠 실행. (4) 트리거에 `opened` 를 빠뜨려 완료된 REQ 에 새 이슈가 열려도 Notion 이 완료로 남았다
다음 할 것 : Stage 7 — robot-stack / firmware-motor / robot-config-model-a repo, `.repos` + vcs import, v0.1.0 태그, 릴리스 매니페스트, 크로스 repo 이슈 참조, `.github` 재사용 워크플로

[2026-08-10] Stage 7
오늘 한 것 : repo 5개 추가(robot-stack / firmware-motor / robot-config-model-a / releases / .github), 전부 v0.1.0 태그. `.repos` 2벌(release/dev)로 워크스페이스 조립 확인, 릴리스 매니페스트 + GitHub Release, 크로스 repo 이슈 참조, CI 를 조직 공통 재사용 워크플로 호출로 전환
막힌 것    : (1) **재사용 워크플로로 바꾸니 status check 이름이 `lint-and-test` → `call-shared-ci / lint-and-test` 로 바뀌었다.** Ruleset 은 옛 이름을 기다려서 체크가 통과했는데도 머지가 막혔다. 조직 전체를 재사용 워크플로로 옮길 때 모든 repo 의 Ruleset 을 같이 고쳐야 한다. (2) vcstool 이 `.repos` 를 cp949 로 열어서 한글 주석에 죽는다 → 매니페스트는 ASCII 로. (3) 존재하지 않는 태그로 import 하면 exit 1 이지만 디렉터리는 남고 main 이 체크아웃된다. 종료 코드를 안 보면 조립 성공으로 착각한다
다음 할 것 : Stage 8 — CONTRIBUTING.md, 온보딩 체크리스트, Before/After 설득 자료, 파일럿 범위 확정. **팀원 1명과 스프린트 1회**가 완료 조건이라 혼자서는 못 끝낸다
