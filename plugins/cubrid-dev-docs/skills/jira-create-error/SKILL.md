---
name: jira-create-error
description: Draft a JIRA description for a bug/error-resolution ticket in CUBRID JIRA wiki format. Use when the user asks for a JIRA body, description, or ticket draft for a bug report, defect, crash, wrong result, or regression. Do NOT use this for enhancement/feature tickets — use jira-create-imprv instead.
argument-hint: <ticket-id or topic>
---

Draft a JIRA ticket description for a *bug-fix / error-resolution* ticket in the format used by CUBRID JIRA.

If the user hasn't given enough context, ask for: the ticket ID (CBRD-#####), build information, reproduction steps, observed vs expected behavior, and any logs/stack traces. Otherwise infer from the current working context (git log, error messages, open files).

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
# <영문 한 줄 제목 — 증상을 서술>

> JIRA [CBRD-#####](http://jira.cubrid.org/browse/CBRD-#####) -- <상위 이슈나 관계>.
> 내부용 -- 이 파일은 저장소 안에서 리뷰하는 문서다. 실제 JIRA 붙여넣기는 ISSUE.jira 를 쓴다.
> (재현 조건이나 조사 범위에 대한 주의가 있으면 한 줄 더)

## Test Build
...
## Repro
...
## Expected Result
...
## Actual Result
...
## Additional Information
...
```

`ISSUE.jira` 는 파일 전체가 JIRA wiki 블록이다. 코드 펜스로 감싸지 않는다 —
파일 자체가 그 내용이므로 감쌀 이유가 없다. 내용은 아래 `Output template` 절이 정한다.

*문법 대응표*

| 요소 | `ISSUE.md` | `ISSUE.jira` |
|---|---|---|
| 섹션 제목 | `## Repro` | `h2. *Repro*` |
| 하위 제목 | `#### 1. 제목` | `h4. 1. 제목` |
| 강조 | `**text**` | `*text*` |
| 코드·로그 블록 | ` ```sql ` / ` ``` ` | `{code:sql}` / `{code}` … `{code}` |
| 표 헤더 | `\| a \| b \|` + 구분선 | `\|\|a\|\|b\|\|` |
| 표 본문 | `\| 1 \| 2 \|` | `\|1\|2\|` |
| 불릿 | `- item` | `* item` |
| 번호 목록 | `1. item` | `# item` |
| 중첩 번호 | 들여쓴 `- item` | `#*`, `#**` |

*주의*
* 스택 트레이스·assert 메시지·결과셋은 **두 파일 모두 원문 그대로** 둔다.
  줄바꿈이나 공백을 정리하지 않는다 — 재현 판정의 근거가 훼손된다.
* `ISSUE.md` 에서는 백틱 인라인 코드를 써도 되지만, `ISSUE.jira` 에서는 `*볼드*` 로 바꾼다.
* 재현 단계는 표로 정리하면 시점별 상태(트랜잭션별 동작, 관찰값)를 보이기 좋다.
* 두 파일은 같은 디렉터리에 함께 둔다 —
  `engineering/development/<topic>_<CBRD-#####>/ISSUE.md` 와 `ISSUE.jira`.
  티켓 번호가 아직 없으면 `<topic>` 만으로 시작해도 된다.

## Output template (JIRA wiki markup)

아래는 `ISSUE.jira` 파일 전체의 내용이다.

```
h2. *Test Build*

<!-- 재현된 빌드를 버전별로 나열. "CBRD-##### 머지 이후 버전만 테스트" 처럼
     범위를 먼저 밝히고, 빌드 식별자(version-gitsha)마다 재현 여부를 표기한다.
     서버 설정·환경(OS, 메모리, 파라미터 등) 이 재현에 영향을 준다면 이 섹션에 같이 적는다. -->

* CBRD-##### 머지 이후 버전만 테스트
* 11.2.9.0866-ef544a1: 재현됨
* 11.3.4.1245-bdc3a53: 재현됨
* 11.4.4.1832-7f8f019: 재현됨
* 11.5.0.2169-34fc777 (develop): 재현됨

<!-- 필요한 경우 영향 설정/환경 블록 추가 예시:
* OS: CentOS 7.9 / Ubuntu 22.04
* max_clients = 200
* isolation_level = TRAN_REP_CLASS_COMMIT_INSTANCE
* 데이터 크기: sbtest 5M rows -->

h2. *Repro*

<!-- 재현 단계. 번호 목록으로 순서 명확히. 가능하면 SQL 스크립트나 명령을 그대로 포함.
     최소 재현 케이스(MRC) 가 있으면 제일 앞에 둔다.
     환경/설정/파라미터가 필요하면 Test Build 와 중복되지 않게 여기에 작업 수준으로 기재. -->

# <단계 1>
# <단계 2>
# <단계 3>

{code:sql}
-- 재현 SQL 예시
{code}

h2. *Expected Result*

<!-- 기대 동작. SQL 이라면 반환되어야 할 결과셋, 내부 경로라면 정상 상태에서의 동작.
     표/결과값을 있는 그대로 붙여 넣는다. -->

<기대 결과>

h2. *Actual Result*

<!-- 실제 관찰된 동작. 오류 메시지, 스택 트레이스, 잘못된 결과값 등을 가감 없이.
     크래시면 assert 메시지/시그널/코어 위치. -->

<실제 결과>

{code}
<에러 로그 / 스택 트레이스>
{code}

h2. *Additional Information*

<!-- 근본 원인 가설, 관련 커밋, 연관 티켓, 재현 빈도, 워크로드, 임시 우회법 등.
     모르면 빼도 된다 (섹션 자체 생략 가능). -->

* Root cause (가설):
* Related tickets:
* Frequency / impact:
* Workaround:
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

## 버그 티켓 특화 규칙

*스타일*
* Test Build 는 재현된 각 버전별 식별자(version-gitsha)를 한 줄씩 나열하고, 테스트 범위(예: "CBRD-##### 머지 이후 버전만 테스트") 를 첫 줄에 명시한다.
* 재현 여부는 "재현됨 / 재현 안 됨 / 미확인" 으로 일관되게 표기한다.
* 서버 설정·환경 요인이 재현 여부를 바꾼다면 Test Build 섹션 안에 같이 적어 재현 조건을 한 눈에 보이게 한다.
* 현재 최신 develop 에서 결함이 남아 있는지 확인한다 -- 코드 읽기(패치 미반영 확인)로 충분하고, 최신 커밋에서 다시 빌드·재현할 필요는 없다.
* Repro 는 **재현 가능성** 이 최우선. "가끔 된다" 가 아니라 "이 순서로 하면 재현됨" 이어야 한다. 재현 빈도/타이밍 이슈는 Additional Information 에 별도 기재.
* Expected / Actual 는 관찰 가능한 사실만. 원인 해석은 Additional Information 으로 분리.

*하지 말 것*
* `{{monospace}}` 사용 — 많은 환경에서 렌더링되지 않음.
* "고쳐야 함" 같은 결론만 있는 description 은 피한다 — 항상 Repro + 관찰값이 있어야 한다.
* 여러 버그를 한 티켓에 합쳐 쓰지 않는다. 증상이 다르면 티켓을 나눈다.

## 참고

재현이 어려운 경우에도 *현재까지 확보된 정보* 를 모두 담아 두는 편이 낫다. Repro 섹션에는 "간헐적 재현, 현재까지 확인된 조건" 을 그대로 적고, Additional Information 에 "재현 데이터/덤프 위치" 를 가리킨다.
