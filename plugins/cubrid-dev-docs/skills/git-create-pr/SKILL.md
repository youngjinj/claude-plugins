---
name: git-create-pr
description: Draft a GitHub PR body paired with a CUBRID JIRA ticket. Use when the user asks for a PR body/description/draft, or to "create PR" text. Pairs with jira-create-imprv/jira-create-error — JIRA carries the full Description/Implementation/A/C; PR body carries only what a reviewer needs to open the diff.
argument-hint: <ticket-id or topic>
---

Draft a GitHub PR body for a CUBRID ticket. JIRA already holds the canonical Description, Implementation, A/C, and DoD — the PR body must NOT duplicate them.

If context is insufficient, ask for: ticket ID (CBRD-#####), branch, and a one-line topic. Otherwise infer from `git log`, `git diff`, open files, and recent conversation.

$ARGUMENTS

## Title

Unify the PR title with the JIRA issue title. Format:

```
[CBRD-#####] <Imperative short description>
```

Title must be the same string in both JIRA and GitHub. Prefer verbs that describe the net change (`Remove`, `Simplify`, `Add`, `Fix`), not the motivation.

## Output template (PR body, GitHub-flavored Markdown)

```markdown
http://jira.cubrid.org/browse/CBRD-#####

### Purpose

<!-- 왜 이 PR이 필요한가를 1~2문장으로.
     "무엇이 문제인지 + 어떻게 해결하는지" 의 핵심만.
     perf 수치·벤치 결과는 여기 넣지 않는다(테스트 근거가 필요한 내용). -->

### Implementation

<!-- 리뷰어가 diff 를 열기 전에 알아야 할 net change 를 bullet 으로 나열.
     develop 기준 순변화만 적고, 과정에서 넣었다 뺀 실험은 제외.
     JIRA 의 Implementation 을 그대로 복붙하지 말고, 리뷰 포커스용으로 3~5개로 압축.
     "세부 내용은 JIRA 참고" 같은 연결 문구는 넣지 않는다. -->

- <net change 1>
- <net change 2>
- <net change 3>

### Remarks

<!-- diff 상에서 바로 보이지 않지만 리뷰어가 알면 유용한 캐비앳만.
     예: 스타일 재포맷을 일부러 피한 파일, ABI 안전을 위해 의도적으로 남긴 API, 외부 서브모듈 영향 등.
     "lock_table 은 별도 patch 로 분리" 처럼 이 PR의 범위 외 항목이나, "revert 커밋 포함" 같은
     브랜치 정리 상태 메모는 넣지 않는다 — 순변화와 무관. -->

- <caveat 1>
```

## 공통 규칙

*문법*
* GitHub-flavored Markdown. 코드·식별자는 백틱으로 감싼다.
* 섹션 헤더는 `### Purpose` / `### Implementation` / `### Remarks` 로 고정. H1/H2 는 쓰지 않는다 (GitHub PR UI 가 title 을 이미 H1 으로 렌더).
* 본문 최상단에 JIRA 링크 한 줄. 괄호/bold 없이 raw URL.

*용어 — 비유 대신 기술 용어*
* 동작은 그 동작의 기술 용어로 쓴다. 비유어는 읽는 사람마다 다르게 해석되고, 검색으로 코드와 이어지지 않는다.
* 자주 새는 비유와 대체어: 굽다/구워진 -> 변환한다/변환된, 앉히다/앉은 -> 설정한다/저장된, 도장을 찍다 -> 값을 설정한다, 찍다(출력 문맥) -> 출력한다, 누르다(부하 문맥) -> 부하를 준다, 태우다(경로 문맥) -> 그 경로로 실행한다.
* 같은 낱말을 서로 다른 대상에 쓰지 않는다. 한 문서에서 두 대상이 같은 낱말로 불리면 수식어를 붙여 가른다.

*내용 분리*
* **Purpose**: 1~2문장. 문제 상황 + 해결 방향. 수치·벤치·Test plan 없음.
* **Implementation**: develop 기준 net change 만. 3~5개 bullet.
* **Remarks**: 리뷰 관점 캐비앳 전용. 순변화와 무관한 것(실험 revert, 분리된 패치, Related 링크)은 제외.

*하지 말 것*
* `## Summary` / `## Motivation` / `## Test plan` / `## Related` 섹션 추가 금지. JIRA 와 역할이 겹친다.
* baseline perf 수치 (before/after %) — 벤치 테스트 결과로 별도 제공.
* 체크박스 Test plan — QA 영역.
* `**Title**:` 같은 메타 라인을 PR body 안에 넣지 않는다. Title 은 GitHub UI 의 title 필드에만.
* TU (Translation Unit) 같은 용어 해설 — JIRA 본문에 이미 있음. 중복 금지.
* "자세한 건 JIRA 참고" 류의 연결 문구 — 독자가 이미 링크 위에서 알고 있다.

## 참고

* 같은 티켓의 JIRA 본문은 `jira-create-imprv` 또는 `jira-create-error` 스킬로 작성한다. JIRA 가 canonical source, PR body 는 리뷰 유도용 요약.
* 설계 노트·리뷰 가이드·PR/JIRA 초안은 같은 리포지터리의 `engineering/development/<topic>_<CBRD-#####>/` 에 분리 보관하고, PR body 안에는 그 경로를 노출하지 않는다(내부 노트 성격).
