# 문체 규칙

`cubrid-doc` 4단계가 이 파일의 규칙을 적용한다.

**잠정 규칙이다. 사용자 결정으로 대체된다.** 사용자가 특정 표현을 지시하면 이 파일보다 그 지시가 우선한다.

출처: [Google developer documentation style guide](https://developers.google.com/style) 중 한국어 기술문서에 적용되는 항목만 추렸다. 원문은 Creative Commons Attribution 4.0 License 이고 코드 예제는 Apache 2.0 License 다.

## Google 스타일 가이드에서 채택한 것

| 규칙 | 원문 | 한국어 적용 |
|---|---|---|
| 능동태 | `Use active voice: make clear who's performing the action.` | 동작의 주체를 문장 앞에 둔다 |
| 예고 금지 | `Don't pre-announce anything in documentation.` | `이 절에서는 ~를 다룬다` 를 쓰지 않는다. 절의 내용이 그 일을 한다 |
| 순서 있는 목록 | `Use numbered lists for sequences.` | 절차와 순서에는 번호를 붙인다 |
| 순서 없는 목록 | `Use bulleted lists for most other lists.` | 나머지 나열은 불릿으로 |
| 짝을 이루는 자료 | `Use description lists for pairs of related pieces of data.` | 용어와 뜻, 파라미터와 설명은 두 열 표로 |
| 코드 서체 | `Put code-related text in code font.` | 함수명, 파라미터명, 상수, 경로, 파일명을 백틱으로 감싼다 |
| 링크 문구 | `Use descriptive link text.` | `여기` 를 쓰지 않고 가리키는 대상을 문구로 쓴다 |
| 전역 독자 | `Write for a global audience.` | 약어를 처음 나올 때 풀어 쓴다. 지역 관용구를 쓰지 않는다 |
| 접근성 | `Write accessibly.` | 그림에만 담긴 정보를 본문에도 적는다. ASCII 그림의 라벨은 영어로, 한글 설명은 그림 밖에 둔다 |
| UI 요소 | `Put UI elements in bold.` | 메뉴와 버튼 이름을 굵게 |
| 날짜 표기 | `Use unambiguous date formatting.` | `YYYY-MM-DD` 로 적는다 |

## 채택하지 않은 것

| 원문 규칙 | 왜 채택하지 않았나 |
|---|---|
| `Be conversational and friendly without being frivolous.` | 스펙 문서와 이슈 본문의 어조와 충돌한다 |
| `Use sentence case for document titles and section headings.` | 한국어에 대소문자가 없다 |
| `Use serial commas.` | 한국어 나열에 무의미하다 |
| 미국식 철자 (`color`, `canceled`) | 한국어에 무의미하다 |
| word list (`utilize` -> `use` 같은 낱말 목록) | 영어 낱말 목록이라 한국어에 무의미하다 |
| `Use second person: "you" rather than "we."` | 한국어 기술문서는 한다체 서술이 관례다. 절차만 독자를 향해 적는다 |

## 한국어 전용 규칙

Google 가이드에 없고 한국어에서 필요한 것들이다.

- **피동을 쓰지 않는다.** `잡히지 않았다` 대신 `찾지 못했다`. 주체를 찾아 앞에 둔다.
- **번역투를 쓰지 않는다.** `~에 대해`, `~을 통해`, `~되어진다`, `~에 있어`, `~로서` 를 쓰지 않는다.
- **가능형을 남발하지 않는다.** `~할 수 있다` 가 한 문단에 셋 이상이면 줄인다. 사실이면 `~한다` 로 단정한다.
- **한 문장에 한 주장.** 근거가 둘이면 문장도 둘이다.
- **영문 기술 용어를 번역하지 않는다.** `flush`, `bind`, `barrier`, `durability` 를 한글로 바꾸지 않는다. 표기는 `glossary.md` 가 정한다.
- **수치에는 단위와 기준을 함께 적는다.** `+3.4%` 만 적지 않고 무엇 대비인지, 몇 런인지, 변동 폭이 얼마인지 붙인다.
