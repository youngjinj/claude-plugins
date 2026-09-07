---
name: build-cubrid
description: CUBRID 소스 빌드 (cmake preset debug/release → $CUBRID 설치)
argument-hint: "[debug|release] [source-dir]"
---

# CUBRID Source Build

cmake preset으로 빌드하고 `$CUBRID`에 설치한다.
**항상 전체(클린) 빌드한다 — 증분 빌드 금지** (`--clean-first`). 증분 빌드는 재컴파일 여부를 헷갈리게 하므로 쓰지 않는다.

## Workflow

```bash
MODE="${1:-debug}"                     # debug or release
SRC_DIR="${2:-$(pwd)}"                 # source dir or cwd
source $HOME/cubrid.sh
[ -z "$CUBRID" ] && echo "ERROR: \$CUBRID not set" && exit 1
[ ! -f "$SRC_DIR/CMakeLists.txt" ] && echo "ERROR: Not a CUBRID source: $SRC_DIR" && exit 1
cd "$SRC_DIR"
cubrid service stop
cmake --preset "$MODE"
cmake --build --preset "$MODE" --target install --clean-first   # full rebuild, never incremental
```
