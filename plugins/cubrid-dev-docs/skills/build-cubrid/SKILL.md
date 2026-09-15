---
name: build-cubrid
description: CUBRID 소스 빌드 (현재 develop 은 cmake preset, 과거 버전은 build.sh) — 버전별 제약과 우회법 포함
argument-hint: "[debug|release] [source-dir]"
---

# CUBRID Source Build

빌드 방법은 대상 커밋의 시점에 따라 다르다. 현재 develop 은 cmake preset 으로 충분하지만,
과거 버전을 빌드할 때에는 아래 "과거 버전 빌드" 절의 제약을 먼저 확인한다.
**항상 전체(클린) 빌드한다 — 증분 빌드 금지.** 증분 빌드는 재컴파일 여부를 헷갈리게 하므로 쓰지 않는다.

## 현재 develop 빌드

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

빌드 후 로케일을 다시 만들어야 한다. 설치가 `conf/cubrid_locales.txt` 를 비우므로, 이 단계를 건너뛰면
콜레이션 개수가 맞지 않아 기존 데이터베이스가 뜨지 않는다.

```bash
cp $CUBRID/conf/cubrid_locales.all.txt $CUBRID/conf/cubrid_locales.txt
$CUBRID/bin/make_locale.sh -t64
```

## 과거 버전 빌드

특정 커밋에서 결함이 유입된 시점을 찾는 등, 과거 버전을 빌드해야 할 때가 있다.
시점마다 제약이 달라 아래 표를 먼저 확인한다. 기준 날짜는 2026-09-15 에 11.3 ~ 11.5 구간을 실제로
빌드하며 확인한 것이다.

| 시점 | 제약 | 대응 |
|---|---|---|
| 2024-07-10 이전 | `CMakePresets.json` 없음 (프리셋은 `cd8fdc0cf9` 에서 도입) | `./build.sh` 를 쓴다 |
| 2023 ~ 2024 상반기 | `CMakeLists.txt` 가 `.git` 을 디렉터리로 가정 (`configure_file(".git/HEAD" ...)`) | git worktree 에서는 `.git` 이 파일이라 설정이 실패한다. `git clone --shared` 로 복제본을 만들어 빌드 |
| 전 구간 | `cubridmanager` 가 jsoncpp 와 C++ ABI 불일치로 링크 실패 | `-DWITH_CMSERVER=OFF` |
| 전 구간 | 설치본의 `libcubridsa.so` / `libcubridcs.so` 가 C++ 표준 라이브러리 심볼을 못 찾음 | 아래 "RPATH 함정" 참고 |

### 권장 절차

```bash
# 1. 복제본을 만든다 (worktree 는 .git 이 파일이라 과거 버전 설정이 실패한다)
git clone --shared /path/to/cubrid /path/to/cubrid-build
cd /path/to/cubrid-build
git checkout <커밋 또는 태그>

# 2. 서브모듈을 완전히 새로 받는다
#    체크아웃을 옮기면 서브모듈 리비전이 따라 바뀌고, 이전 산출물이 남아 링크가 깨진다
git submodule deinit -f --all
rm -rf cubrid-cci cubrid-jdbc cubridmanager
git submodule update --init

# 3. build.sh 로 빌드한다 (기본 생성기는 make)
./build.sh -m debug -c "-DWITH_CMSERVER=OFF" build

# 4. 설치 경로를 지정해 설치한다
cd build_x86_64_debug
cmake -DCMAKE_INSTALL_PREFIX=/path/to/CUBRID_test .
make install
```

### RPATH 함정

가장 오래 헤맸던 지점이다. 빌드 디렉터리의 산출물은 멀쩡한데 설치본만 실행되지 않는다.

```
$ cubrid createdb ...
/path/to/CUBRID_test/lib/libcubridsa.so: undefined symbol: _ZNSaIcEC1Ev
```

`libcubridsa.so` 와 `libcubridcs.so` 는 `libstdc++` 를 동적 링크 목록에 두지 않고
`libcascci.so` 를 통해 간접적으로 C++ 표준 라이브러리 심볼을 얻는다. 빌드 디렉터리에서는
RPATH 가 `build_x86_64_debug/cubrid-cci/cci` 를 가리켜 문제가 없지만, 설치하면 RPATH 가
`<prefix>/lib` 으로 바뀌는 반면 `libcascci.so` 는 `<prefix>/cci/lib` 에 놓여 연결이 끊긴다.

실행 시 `LD_LIBRARY_PATH` 에 `cci/lib` 을 더하면 해결된다.

```bash
export CUBRID=/path/to/CUBRID_test
export CUBRID_DATABASES=$CUBRID/databases
export PATH=$CUBRID/bin:$PATH
export LD_LIBRARY_PATH=$CUBRID/lib:$CUBRID/cci/lib:$LD_LIBRARY_PATH
```

진단할 때에는 다음으로 확인한다. 빌드본이 0 이고 설치본이 20 여 개면 이 함정이다.

```bash
ldd -r $(readlink -f $CUBRID/lib/libcubridsa.so) | grep -c "undefined symbol"
readelf -d $(readlink -f $CUBRID/lib/libcubridsa.so) | grep -i rpath
```

### 그 밖에 겪은 것들

`libssl.a: No such file or directory` — CCI 서브모듈이 CMake 3.21 로 올라가면서 OpenSSL 이
`3rdparty/lib64` 에 설치되는데 CCI 는 `3rdparty/lib` 에서 찾는다. 두 파일을 링크로 잇는다.

```bash
cd <build>/3rdparty
ln -sf ../lib64/libssl.a lib/libssl.a
ln -sf ../lib64/libcrypto.a lib/libcrypto.a
```

`ninja: error: remove(...): Directory not empty` — `--target clean` 이 rapidjson 디렉터리에서 실패한다.
빌드 디렉터리를 통째로 지우고 다시 설정하는 편이 빠르다.

## 여러 버전을 동시에 다룰 때

설치 경로를 버전마다 나누고, 서버는 한 번에 하나만 띄운다. 같은 포트를 쓰므로 동시에 기동하면 충돌한다.

```bash
cubrid service stop      # 이전 버전 서버를 먼저 내린다
```

재귀 CTE 로 테스트 데이터를 만들 때 재귀 깊이 상한은 2000 이다. 그보다 큰 행 수가 필요하면
얕은 재귀를 곱해서 만든다.

```sql
INSERT INTO tb
WITH RECURSIVE cte (n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM cte WHERE n < 200)
SELECT (ROWNUM - 1) % 100 + 1, (ROWNUM - 1) / 100 + 1 FROM cte x, cte y WHERE x.n <= 100;
```
