---
name: jira-create-imprv
description: Draft a JIRA description for an improvement/enhancement ticket in CUBRID JIRA wiki format. Use when the user asks for a JIRA body, description, or ticket draft for a feature/enhancement/refactor/performance/API-cleanup change. Do NOT use this for bug-fix tickets — use jira-create-error instead.
argument-hint: <ticket-id or topic>
---

Draft a JIRA ticket description for an *improvement* (enhancement, feature, refactor, performance, API cleanup, …) in the format used by CUBRID JIRA.

If the user hasn't given enough context, ask for: the ticket ID (CBRD-#####), the branch/commits, and any design notes. Otherwise infer from the current working context (git log, open files, recent conversation).

$ARGUMENTS

## 파일로 남길 때 — MD 파일과 JIRA 파일을 따로 만든다

JIRA 본문을 파일로 관리할 때는 리뷰용 Markdown 과 붙여넣기용 JIRA wiki 를
**서로 다른 파일**로 만든다. 한 파일에 이중으로 넣지 않는다.

| 파일 | 문법 | 용도 |
|---|---|---|
| `ISSUE.md` | Markdown | GitHub 에서 렌더링해 리뷰한다 |
| `ISSUE.jira` | JIRA wiki markup | 파일 전체를 그대로 JIRA 에 붙여넣는다 |

두 파일의 **내용은 같아야 한다.** 하나를 고치면 다른 것도 반영한다.

`ISSUE.md` 머리는 이렇게 시작한다.

```
# <영문 한 줄 제목 — 문제/개선을 서술>

> JIRA [CBRD-#####](http://jira.cubrid.org/browse/CBRD-#####) -- <상위 이슈나 관계>.
> 내부용 -- 이 파일은 저장소 안에서 리뷰하는 문서다. 실제 JIRA 붙여넣기는 ISSUE.jira 를 쓴다.
> (문서 성격에 대한 주의가 있으면 한 줄 더)

## Description
...
## Specification Changes
...
## Implementation
...
## Acceptance Criteria (A/C)
...
## Definition of done (DoD)
...
```

`ISSUE.jira` 는 파일 전체가 JIRA wiki 블록이다. 코드 펜스로 감싸지 않는다 —
파일 자체가 그 내용이므로 감쌀 이유가 없다. 내용은 아래 `Output template` 절이 정한다.

*문법 대응표*

| 요소 | `ISSUE.md` | `ISSUE.jira` |
|---|---|---|
| 섹션 제목 | `## Description` | `h2. *Description*` |
| 하위 제목 | `#### 1. 제목` | `h4. 1. 제목` |
| 강조 | `**text**` | `*text*` |
| 코드 블록 | ` ```sql ` | `{code:sql}` … `{code}` |
| 표 헤더 | `\| a \| b \|` + 구분선 | `\|\|a\|\|b\|\|` |
| 표 본문 | `\| 1 \| 2 \|` | `\|1\|2\|` |
| 불릿 | `- item` | `* item` |
| 번호 목록 | `1. item` | `# item` |
| 중첩 번호 | 들여쓴 `- item` | `#*`, `#**` |

*주의*
* `ISSUE.md` 에서는 백틱 인라인 코드를 써도 되지만, `ISSUE.jira` 에서는 `*볼드*` 로 바꾼다
  (`{{monospace}}` 는 렌더링되지 않는 환경이 많다).
* 두 파일은 같은 디렉터리에 함께 둔다 —
  `engineering/development/<topic>_<CBRD-#####>/ISSUE.md` 와 `ISSUE.jira`.
  티켓 번호가 아직 없으면 `<topic>` 만으로 시작해도 된다.

## Output template (JIRA wiki markup)

아래는 `ISSUE.jira` 파일 전체의 내용이다.

첫 절의 `h2. *Description*` 은 **생략해도 된다.** JIRA 의 Description 필드 자체가 그 제목이라 한 번 더 쓰면 겹친다. 나머지 절 제목은 그대로 둔다.

```
h2. *Description*

<!-- 문제가 무엇이고 왜 고치는지, 고친 뒤 어떻게 동작하는지를 추상적으로 기술.
     외부에서 관찰되는 동작·저장 포맷이 변하는지 여기서 명확히 밝힌다.
     구체 함수명/수치/파일이 필요하면 적어도 무방. -->

h2. *Specification Changes*

<!-- 이 섹션은 "버전 업그레이드 시 볼륨 호환이 되지 않는 경우 그 변경 사항" 전용.
     호환성 이슈가 없으면 한 줄로 "없음" 이라고만 적는다.
     행동 변화가 있어도 호환성 이슈가 아니면 Description 에 녹인다. -->

없음

h2. *Implementation*

<!-- 변경 내용을 소수의 상위 그룹(보통 3~5개)으로 묶어 JIRA 번호 목록으로 정리.
     각 그룹 안에는 하위 불릿으로 구체 항목을 나열한다.
     레벨: #  →  #*  →  #** (필요할 때만).
     용어 약어가 나오면 해당 위치 아래 한 단계 더 들여써서 뜻풀이를 덧붙이는 것을 권장. -->

# <그룹 1 제목>
#* <세부 항목>
#* <세부 항목>
#** <약어 해설이나 참고가 필요하면 여기>
# <그룹 2 제목>
#* ...
# <그룹 3 제목>
#* ...
# <그룹 4 제목 — 예: Defensive asserts>
#* ...

h2. *Acceptance Criteria (A/C)*

<!-- 코드 변경 범위를 근거로 "테스트가 필요한 시나리오" 와 "해당 시나리오에서 정상이라고 판정되는 동작"
     을 짝지어 기술한다. 구체 쿼리/라인/수치가 아니라 시나리오의 차원(입력 카테고리, 경계 조건,
     실행 경로 등) 과 그 시나리오에서의 정상 동작 정의를 서술한다.

     좋은 A/C 는 테스터가 읽고 "이런 테스트 케이스를 짜야겠구나" 라는 판단으로 이어진다.
     개수는 2~4개가 적당. -->

* <시나리오 차원 1> 에서 <정상 동작 정의>
* <시나리오 차원 2> 에서 <정상 동작 정의>
* <시나리오 차원 3> 에서 <정상 동작 정의>

h2. *Definition of done (DoD)*

<!-- Acceptance Criteria 달성 외에 완료 판정을 위해 요구되는 추상적 조건.
     예: 기존 QA 테스트 통과, 코드 리뷰 승인, 관련 릴리스 노트 갱신 등.
     티켓 성격에 맞게 자유롭게 확장한다. -->

* Acceptance Criteria를 모두 만족한다.
* 기존 QA 테스트를 통과한다.
```

## 공통 규칙 (개선·버그 스킬 공통)

*문법*
* JIRA wiki markup을 사용. 마크다운(`**bold**`, 백틱)과 혼용하지 않는다.
* 굵은 글씨는 `*text*` 한 쌍. 중첩된 별표 기호(포인터 타입 `*value`)는 `\*` 로 이스케이프.
* 식별자·함수명은 `*함수명()*` 형태로 볼드 처리. `{{…}}` 문법은 비활성 환경이 많으므로 사용하지 않는다.
* 최상위 섹션 헤더는 `h2. *Section Name*` 형식으로 통일.
* 서브 헤더가 필요하면 `h3.` 은 건너뛰고 `h4.` 부터 시작한다. 더 깊은 단계가 필요하면 `h5.`, `h6.` 순.
* 번호 목록은 `#`, `#*`, `#**`. 불릿 목록은 `*`, `**`, `***`.

*용어 — 비유 대신 기술 용어*
* 동작은 그 동작의 기술 용어로 쓴다. 비유어는 읽는 사람마다 다르게 해석되고, 검색으로 코드와 이어지지 않는다.
* 자주 새는 비유와 대체어: 굽다/구워진 -> 변환한다/변환된, 앉히다/앉은 -> 설정한다/저장된, 도장을 찍다 -> 값을 설정한다, 찍다(출력 문맥) -> 출력한다, 누르다(부하 문맥) -> 부하를 준다, 태우다(경로 문맥) -> 그 경로로 실행한다.
* 같은 낱말을 서로 다른 대상에 쓰지 않는다. 한 문서에서 두 대상이 같은 낱말로 불리면 수식어를 붙여 가른다.
* 로그·코드·SQL 은 `{code}` / `{code:sql}` 블록으로 감싼다.

## 개선 티켓 특화 규칙

*스타일*
* Description 은 "왜 바꾸는지 / 바꾸고 나면 어떻게 되는지" 를 말한다. 길이 제약 없음.
* Implementation 의 그룹 순서는 이해 순서로 정렬 (가장 핵심 API 변경 → 성능 최적화 → 부수 정리 → 방어 코드 순이 자주 맞는다).
* 같은 티켓 안에서 서로 성격이 다른 부수 정리는 하나의 "정리" 그룹으로 묶지 말고, 관련된 메인 그룹 하위에 흡수시킨다.
* A/C 는 승인 기준이자 *테스트 설계자의 시작점* 이다. 코드 변경을 근거로 어떤 시나리오(입력 카테고리, 경계 조건, 분기 경로)가 커버돼야 하는지 + 그 시나리오에서 무엇이 "정상" 인지를 정의한다. 구체 SQL 이나 숫자는 테스트 플랜 문서 몫.
* "빌드 성공" 같이 당연한 항목은 A/C 에 넣지 않는다.

*하지 말 것*
* `{{monospace}}` 사용 — 많은 환경에서 렌더링되지 않음.
* 마크다운 `**bold**` 사용 — JIRA 에서는 기울임이 아니라 그대로 출력됨.
* Implementation 에는 develop 기준 순변화 항목만 적는다.
* 성격이 다른 개선을 한 티켓에 합쳐 쓰지 않는다. 근거가 다르면 티켓을 나눈다.

## 참고

필요하면 별도 문서(디자인 배경, 리뷰 가이드, PR body)를 같은 리포지터리의 `engineering/development/<topic>_<CBRD-#####>/` 형식으로 분리해 관리하고, JIRA 본문은 요약에 집중한다.
