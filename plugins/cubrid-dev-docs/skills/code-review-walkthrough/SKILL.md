---
name: code-review-walkthrough
description: CUBRID PR 변경사항을 오프라인 리뷰용 워크스루 markdown 으로 정리. 시나리오가 있으면 그것을 running example 로 잡고, 없으면 코드 실행 흐름 분석으로 구성.
argument-hint: "<PR# 또는 branch>"
---

이 스킬은 **워크스루 문서 하나**를 만든다. 확인사항은 `review-notes.md` 로 분리한다.
디렉터리 규칙, TC 저장소 확인, 선행 이슈 계보, 교차 반증은
`/home/cubrid/github/notes/engineering/review/README.md` 에 있다. 시작 전에 읽는다.

서술이 어긋날 때 신뢰 순서

```
  코드      가장 최신. 이것을 사실로 본다
  JIRA      합의된 명세. 코드가 벗어나면 문서 오류가 아니라 명세 미준수다
  PR 본문   후반 리뷰 커밋을 반영하지 못한다. 갱신 요청 대상
```

## Workflow

1. **PR 메타** — `gh pr view` 로 title·본문을 받고 JIRA 번호(`CBRD-NNNNN`)를 잡는다.
   못 찾으면 사용자에게 확인 요청.

2. **JIRA 명세** — `cubrid-jira search CBRD-NNNNN`.
   `Specification Changes` / `Acceptance Criteria` 에서 파라미터 기본값과 기능 on/off 조건을 뽑아
   5단계에서 코드와 대조한다. 어긋나면 최상위 findings 다.
   `Definition of Done` 미체크 항목과 `Related Issues` 의 선행 PR 머지 여부도 본다.

3. **Base commit** — fetch 를 먼저 한다. stale ref 면 변경 규모부터 틀린다.

   ```bash
   git remote -v                        # 원격 이름이 저장소마다 다르다 (origin / upstream)
   git fetch <remote> develop
   B=$(git merge-base HEAD <remote>/develop)
   ```

   develop 이 더 최신이어도 무시한다. 현재 PR 에 머지된 마지막 develop 커밋이 기준이다.

4. **시나리오** — TC 저장소의 신규 케이스 / PR 본문 / repo 안 scenarios / `jira` / 합성 순.
   TC 신규 케이스가 가장 좋다 — 기대 출력이 답지로 확정되어 있다.
   못 잡으면 §0 을 생략하고 코드 실행 흐름 분석으로 대체한다.

5. **함수 단위 감사** — hunk 를 함수 단위로 훑어 변경 형태를 표기한다
   (신규 / 제거 / 시그니처 변경 / 본문 변경 / rename / 이동).
   파일이 20개를 넘으면 파일 순서 대신 독립 축으로 쪼개고, 축과 읽기 순서를 §1 에 적는다.

6. **문서 작성** — 아래 골격대로.

## 문서 골격

- 제목: `# <JIRA-ID> / PR #<NN> — <한 줄 요약>`
- §0 리뷰 시나리오 (있을 때만) — 출처 + 사전 조건 + 시나리오 본문 + 기대 출력
- §1 진입점 — 외부에서 이 함수까지 도달하는 경로. 축이 여럿이면 축별 진입점과 읽기 순서
- §2~ 변경 파일별 섹션
  - 변경 요약 표 — 호출 흐름이 명확하면 entry → leaves → cleanup, 아니면 의미 그룹 또는 소스 순
  - 함수 단위 sub-section: AS-IS / TO-BE 슈도코드 + 파생 흐름
- 핵심 불변식 (의미 있는 invariant 가 있을 때만)
- 시나리오 ↔ 코드 매핑 표 (시나리오가 있을 때만)
- 부록: 변경 파일 한눈에 — 파일 / ± / 축 / 본 문서 섹션

## 작성 규칙

- **변수명/타입명은 실제 코드 그대로** — 단축 금지. base 본문을 확인 후 작성.
- **`★ 추가` 마커는 진짜 신규 라인에만.** 표 + AS-IS/TO-BE 로 충분하면 쓰지 않아도 된다.
- **시나리오 출처는 §0 도입부에 한 줄로** 표기.
- **findings 를 워크스루에 섞지 않는다.** 섞으면 둘 다 읽히지 않는다.
- 문장은 `tight-comments` 규칙을 따른다.

## 검증 표기

```
  [확인]   코드 읽기로 확정 — 기본값, 시그니처, 분기 조건
  [예측]   코드 읽기 기반 추정 — 동작 결과, 에러 발생 여부
  [재현]   실행으로 확인함
```

"이 조건에서 실패한다" 류는 실행 전까지 전부 `[예측]` 이다.
실행하면 `[재현]` 으로 올리거나 사유를 적고 철회한다.
빌드는 `build-cubrid` 로 걸어두고 그동안 문서를 쓴다.

## 함정

- **grep 은 `-i` 기본** — SQL 케이스와 힌트는 대소문자가 섞인다.
- **stale ref** — 3단계 fetch 를 건너뛰면 변경 규모부터 틀린다.
- **테스트 러너의 암묵 설정** — CTP 는 `<case>.queryPlan` 형제 마커로 플랜 덤프를 켠다.
  케이스 안의 힌트·지시자만 보고 판단하지 않는다.
- **PR 본문의 케이스 목록** — 브랜치와 어긋난다. diff 로 대조한다.

## Example

```
/code-review-walkthrough 7068
```

출력 경로는 지정이 없으면 review/README.md 의 이름 규칙을 따라 만든다.
