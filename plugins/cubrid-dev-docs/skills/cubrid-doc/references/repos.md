# CUBRID 저장소

`cubrid-doc` 0단계가 참조한다.

## 기본 소스

`~/github/develop` 을 쓴다. 연결 계층은 `src/connection/`, 서버 지원 코드는 `src/connection/server_support.c` 에 있다.

## 리비전을 가진 워크트리

리비전을 체크아웃하지 않고 그 커밋의 트리에서 센다.

```bash
cd ~/github/develop
git grep -n '<패턴>' <리비전> -- src
git show <리비전>:src/connection/<파일> | sed -n '<줄>p'
```

`f30f1c2`(11.5.0.2374)를 가진 워크트리는 이렇다. 다른 리비전은 `git cat-file -t <리비전>` 으로 확인한다.

| 워크트리 | `f30f1c2` |
|---|---|
| `~/github/develop` | 있음 |
| `~/github/cubrid` | 있음 |
| `~/github/perf-2374` | 있음 |
| `~/github/perf-bisect` | 있음 |
| `~/github/cubrid-multirow` | 있음 |
| `~/github/cubrid-develop` | 없음 |
