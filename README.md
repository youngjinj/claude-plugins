# claude-plugins

[Claude Code](https://claude.com/claude-code) 개인 플러그인 마켓플레이스.

## 설치

```bash
claude plugin marketplace add youngjinj/claude-plugins
```

```bash
claude plugin install korean-writing@youngjinj
```

## 플러그인

| 플러그인 | 스킬 | 설명 |
|---|---|---|
| `korean-writing` | `korean-analysis-doc` | 한글 데이터 분석 문서를 수치 정합성·논리 구조·용어 일관성·재현성 층위에서 검토 |

## 구조

```
.claude-plugin/marketplace.json          카탈로그
plugins/<plugin>/.claude-plugin/plugin.json   플러그인 매니페스트
plugins/<plugin>/skills/<skill>/SKILL.md      스킬 본문
```

플러그인은 *켜고 끄는 단위*로 나눈다. 항상 같이 쓰는 스킬은 한 플러그인에 묶고,
프로젝트마다 필요 여부가 갈리는 스킬은 따로 뺀다.

## 스킬 추가

1. `plugins/<plugin>/skills/<skill>/SKILL.md` 작성 (프론트매터에 `name`, `description` 필수)
2. 새 플러그인이면 `plugin.json`을 만들고 `marketplace.json`의 `plugins` 배열에 등록
3. 검증 후 커밋

```bash
claude plugin validate .
```

## 갱신

푸시한 뒤 사용하는 쪽에서:

```bash
claude plugin marketplace update youngjinj && claude plugin update korean-writing@youngjinj
```

## 라이선스

MIT
