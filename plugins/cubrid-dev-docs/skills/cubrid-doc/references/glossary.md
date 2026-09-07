# CUBRID 문서 용어집

`cubrid-doc` 4단계가 이 파일과 대조한다. 왼쪽이 대상, 가운데가 쓸 표기, 오른쪽이 그 표기를 정한 근거다.

## 근거 우선순위

아래 순서로 찾고, 먼저 확정되는 것을 쓴다.

| 순위 | 근거 | 무엇을 정하나 | 어디서 확인하나 |
|---|---|---|---|
| 1 | 기존 CUBRID 한국어 표기 | 표기 전체 | `~/github/develop/msg/ko_KR.utf8/*.msg` 4,048줄. 벤더가 쓴 한국어다. 출현 횟수와 파일을 함께 적고, 표기가 갈리면 다수 표기와 비율을 적는다. 한국어 매뉴얼 저장소는 로컬에 없다 |
| 2 | 국립국어원 외래어 표기법 | **한글 철자만** | https://kornorms.korean.go.kr |
| 3 | TTA 정보통신용어사전 | 정보통신 표준 용어 | https://terms.tta.or.kr -- 검색이 POST/JavaScript 다. **GET 조회로 확인할 수 없으므로 스킬은 자동 조회하지 않는다.** 시도해서 실패를 반복하지 않는다. 대상은 `references/tta-pending.md` 에 모은다 |
| 4 | 팀 결정 | 위 셋으로 갈리지 않을 때 | 날짜를 함께 적는다 |

`영문 유지` 인지 `한글 표기` 인지는 **팀 결정**이다. 한글로 쓸 경우의 철자는 **국립국어원 외래어 표기법**이 정한다.

## 확정

| 용어 | 표기 | 근거 |
|---|---|---|
| broker | 브로커 | 기존 CUBRID 한국어 표기 -- `브로커` 7회 (`utils.msg`, `cubrid.msg`) |
| CAS | CAS | 팀 결정 2026-09-01. 풀어쓰지 않는다 |
| flush | flush | 팀 결정 2026-09-01. 영문 유지 |
| durability | durability | 팀 결정 2026-09-01. 영문 유지 |
| barrier | barrier | 팀 결정 2026-09-01. 영문 유지 |
| bind 값 | bind 값 | 팀 결정 2026-09-01. `바인드` 를 쓰지 않는다 |
| timestamp | timestamp | 팀 결정 2026-09-01. 영문 유지 |
| hot path | 핫패스 | 팀 결정 2026-09-01. 메시지 카탈로그 0회 -- `tta-pending.md` |
| socket | 소켓 | 기존 CUBRID 한국어 표기 -- `소켓` 1회 (`cubrid.msg`) |
| buffer | 버퍼 | 기존 CUBRID 한국어 표기 -- `버퍼` 37회 (`csql.msg`, `cubrid.msg`) |
| timer | 타이머 | 팀 결정 2026-09-01. 메시지 카탈로그 0회 -- `tta-pending.md` |
| epoll, eventfd, sendmsg | 원문 그대로 | 팀 결정 2026-09-01. 시스템 호출과 인터페이스 이름 |
| EPOLLIN, EPOLLOUT, EPOLLET | 원문 그대로 | 팀 결정 2026-09-01. 상수 |
| connection worker | 연결 워커 | `연결` 은 기존 CUBRID 한국어 표기 15회 (`csql.msg`, `utils.msg`, `cubrid.msg`). `워커` 는 카탈로그 0회로 팀 결정 2026-09-01 -- `tta-pending.md` |
| task thread | 태스크 스레드 | `스레드` 는 기존 CUBRID 한국어 표기 11회 (`utils.msg`, `cubrid.msg`). `태스크` 는 국립국어원 외래어 표기법(`태스크포스` 용례) |
| message queue | 메시지 큐 | `메시지` 는 기존 CUBRID 한국어 표기 34회 (`csql.msg`, `utils.msg`, `cubrid.msg`). `큐` 는 카탈로그 0회로 팀 결정 2026-09-01 -- `tta-pending.md` |
| descriptor | 디스크립터 | 기존 CUBRID 한국어 표기 1회 (`cubrid.msg`). 백틱 안 식별자(`add_descriptor`)는 원문 유지 |
| context | 컨텍스트 | 팀 결정 2026-09-01. 메시지 카탈로그 0회 -- `tta-pending.md`. 백틱 안 식별자(`ctx`)는 원문 유지 |

## 문서 안에서 정의해 쓰는 용어

아래는 이 용어집이 표기를 정하되, 뜻은 각 문서의 용어 표가 정한다.

| 용어 | 표기 | 근거 | 뜻을 정하는 자리 |
|---|---|---|---|
| 요청 | 요청 | 기존 CUBRID 한국어 표기 10회 (`utils.msg`, `cubrid.msg`) | 클라이언트가 보내는 질의나 명령. 큐에 담기는 내부 요청은 `메시지` 라 적어 가른다 |
| 메시지 | 메시지 | 기존 CUBRID 한국어 표기 34회 (`csql.msg`, `utils.msg`, `cubrid.msg`) | 워커 큐에 담기는 내부 요청. 코드 타입 이름이 `message` 다 |

## 미확정

없다.
