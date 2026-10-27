<style>
  main ul li { margin: 0.5em 0; }
</style>

## Go 1.24 소개 {#introduction}

최신 Go 릴리스인 버전 1.24가 [Go 1.23](/doc/go1.23) 출시 6개월 후인 [2025년 2월](/doc/devel/release#go1.24.0)에 출시됩니다.
변경 사항의 대부분은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언제나 그렇듯, 이번 릴리스에서도 Go 1의 [호환성 약속](/doc/go1compat)을 유지합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

<!-- go.dev/issue/46477 -->
Go 1.24부터 [제네릭 타입 별칭(generic type aliases)](/issue/46477)을 완전히 지원합니다. 이제 타입 별칭을 정의된 타입(defined type)처럼 매개변수화할 수 있습니다.
자세한 내용은 [언어 명세](/ref/spec#Alias_declarations)를 참조하십시오.
현재로서는 `GOEXPERIMENT=noaliastypeparams`를 설정하여 이 기능을 비활성화할 수 있지만, `aliastypeparams` 설정은 Go 1.25에서 제거될 예정입니다.

## Tools {#tools}

### Go 명령어 {#go-command}

<!-- go.dev/issue/48429 -->

이제 Go 모듈은 `go.mod` 파일의 `tool` 지시어를 사용하여 실행 파일 의존성을 추적할 수 있습니다. 이를 통해 관습적으로 "tools.go"라고 이름 붙인 파일에 도구들을 빈 임포트(blank imports)로 추가하던 기존의 우회 방법이 더 이상 필요하지 않습니다. 이제 `go tool` 명령어를 사용하여 Go 배포판에 포함된 도구 외에도 이러한 도구들을 실행할 수 있습니다. 자세한 내용은 [문서](/doc/modules/managing-dependencies#tools)를 참조하십시오.

`go get`의 새로운 `-tool` 플래그는 지정된 패키지에 대해 `require` 지시문을 추가하는 것 외에도, 현재 모듈에 tool 지시문을 추가합니다.

새로운 [`tool` 메타 패턴](/cmd/go#hdr-Package_lists_and_patterns)은 현재 모듈의 모든 도구를 참조합니다. 이는 `go get tool`을 통해 모두 업그레이드하거나, `go install tool`을 통해 GOBIN 디렉토리에 설치하는 데 사용할 수 있습니다.

<!-- go.dev/issue/69290 -->

`go run`으로 생성된 실행 파일과 `go tool`의 새로운 동작 방식이 이제 Go 빌드 캐시에 저장됩니다. 이로 인해 캐시 크기는 커지지만, 반복 실행 속도는 더 빨라집니다. [#69290](/issue/69290)을 참조하십시오.

<!-- go.dev/issue/62067 -->

`go build` 및 `go install` 명령어가 이제 `-json` 플래그를 지원하며, 이를 통해 빌드 출력 및 실패 내용을 표준 출력(standard output)에 구조화된 JSON 형식으로 보고합니다.
보고 형식에 대한 자세한 내용은 `go help buildjson`을 참조하십시오.

또한, `go test -json`은 이제 빌드 출력과 실패 내용을 JSON으로 보고하며, 이는 테스트 결과 JSON과 서로 인터리브(interleaved)되어 나타납니다.
이들은 새로운 `Action` 타입으로 구분되지만, 만약 테스트 통합 시스템에서 문제가 발생할 경우 [GODEBUG 설정](/doc/godebug) `gotestjsonbuildtext=1`을 통해 텍스트 빌드 출력 방식으로 되돌릴 수 있습니다.

<!-- go.dev/issue/26232 -->

새로운 `GOAUTH` 환경 변수는 프라이빗 모듈 패치(fetch)를 인증하는 유연한 방법을 제공합니다. 자세한 내용은 `go help goauth`를 참조하세요.

<!-- go.dev/issue/50603 -->

`go build` 명령어는 이제 버전 관리 시스템의 태그 및/또는 커밋을 기반으로 컴파일된 바이너리에 [메인 모듈의 버전](/pkg/runtime/debug#BuildInfo.Main)을 설정합니다.
커밋되지 않은 변경 사항이 있는 경우 `+dirty` 접미사가 추가됩니다.
바이너리에서 버전 관리 정보를 제외하려면 `-buildvcs=false` 플래그를 사용하십시오.

<!-- go.dev/issue/63939 -->

새로운 [GODEBUG 설정](/doc/godebug) [`toolchaintrace=1`](/doc/toolchain#select)을 사용하여 `go` 명령의 툴체인 선택 과정을 추적할 수 있습니다.

### Cgo {#cgo}

<!-- go.dev/issue/56378, CL 579955 -->
Cgo는 런타임 성능을 향상시키기 위해 C 함수에 대한 새로운 어노테이션을 지원합니다.
`#cgo noescape cFunctionName`은 C 함수 `cFunctionname`으로 전달된 메모리가 escape(탈출)하지 않음을 컴파일러에 알립니다.
`#cgo nocallback cFunctionName`은 C 함수 `cFunctionName`이 Go 함수를 다시 호출(callback)하지 않음을 컴파일러에 알립니다.
자세한 내용은 [cgo 문서](/pkg/cmd/cgo#hdr-Optimizing_calls_of_C_code)를 참조하십시오.

<!-- go.dev/issue/67699 -->
Cgo는 현재 여러 개의 호환되지 않는 선언을 가진 C 함수에 대한 호출 컴파일을 거부합니다. 예를 들어, `f`가 `void f(int)`와 `void f(double)`로 모두 선언된 경우, cgo는 `f(0)`에 대해 잘못된 호출 시퀀스를 생성하는 대신 에러를 보고합니다. 이번 릴리스에서는 이러한 호환되지 않는 선언이 서로 다른 파일에 나타날 때 이 에러 조건을 더 잘 감지하는 기능이 추가되었습니다. [#67699](/issue/67699)를 참조하십시오.

### Objdump

`objdump`는 바이너리 파일의 내용을 조사하는 데 사용되는 강력한 명령줄 도구입니다. 주로 컴파일된 실행 파일, 오브젝트 파일 또는 라이브러리의 어셈블리 코드를 역어셈블(disassemble)하거나 섹션 정보를 확인하는 데 사용됩니다.

#### 일반적인 사용법

가장 일반적인 사용 사례는 바이너리를 어셈블리로 변환하여 제어 흐름을 분석하는 것입니다.

```bash
objdump -d <binary_file>
```

* `-d`: 실행 가능한 섹션의 내용을 역어셈블합니다.

#### 주요 옵션

| 옵션 | 설명 |
| :--- | :--- |
| `-d` | 실행 가능한 섹션을 역어셈블합니다. |
| `-D` | 모든 섹션을 역어셈블합니다. |
| `-s` | 모든 섹션의 전체 내용을 16진수(hex)와 ASCII로 덤프합니다. |
| `-h` | 섹션 헤더 정보를 표시합니다. |
| `-x` | 모든 헤더 정보를 표시합니다 (심볼 테이블 포함). |
| `-M <arch>` | 특정 아키텍처를 위해 역어셈블 형식을 지정합니다. |

#### 실전 예제

**1. 특정 함수만 찾아서 분석하기**

파일이 너무 클 경우 `grep`과 함께 사용하여 특정 함수 주변의 코드만 확인할 수 있습니다.

```bash
objdump -d <binary_file> | grep -A 20 "<function_name>:"
```

**2. 심볼 테이블 확인하기**

바이너리에 포함된 함수 및 변수 이름(심볼)을 확인하려면 다음 명령어를 사용합니다.

```bash
objdump -t <binary_file>
```

**3. 소스 코드와 함께 보기**

바이너리가 디버그 정보(`-g` 옵션으로 컴파일됨)를 포함하고 있다면, 소스 코드와 어셈블리를 나란히 표시할 수 있습니다.

```bash
objdump -S <binary_file>
```

#### 분석 팁

* **주소 확인**: `objdump` 출력의 왼쪽 열은 메모리 주소를 나타냅니다. 이는 디버거(GDB 등)에서 중단점(breakpoint)을 설정할 때 유용합니다.
* **오퍼랜드 분석**: 명령어 뒤에 오는 값들은 레지스터, 메모리 주소 또는 즉시값(immediate value)을 나타냅니다.
* **섹션 분석**: `.text` 섹션은 실행 코드를, `.data` 섹션은 초기화된 전역 변수를, `.bss` 섹션은 초기화되지 않은 전역 변수를 담고 있습니다.

<!-- go.dev/issue/15255, go.dev/issue/36738 -->
[objdump](/cmd/objdump) 도구가 이제 64비트 LoongArch (`GOARCH=loong64`), RISC-V (`GOARCH=riscv64`), S390X (`GOARCH=s390x`)의 역어셈블리를 지원합니다.

### Vet

<!-- go.dev/issue/44251 -->
새로운 `tests` 분석기는 테스트 패키지 내의 테스트, 퍼저(fuzzers), 벤치마크 및 예제 선언에서 발생하는 일반적인 실수들을 보고합니다. 예를 들어 잘못된 이름, 부정확한 시그니처, 또는 존재하지 않는 식별자를 문서화하는 예제 등이 이에 해당합니다. 이러한 실수 중 일부는 테스트가 실행되지 않는 원인이 될 수 있습니다.

이 분석기는 `go test`에 의해 실행되는 분석기 서브셋 중 하나입니다.

<!-- go.dev/issue/60529 -->
기존의 `printf` 분석기(analyzer)는 이제 다른 인자 없이 `fmt.Printf(s)` 형태로 호출되며, 여기서 `s`가 상수가 아닌 포맷 문자열인 경우 진단 보고서를 생성합니다. `s`의 값에 `%` 기호가 포함될 수 있으므로 이러한 호출은 거의 항상 실수이며, 대신 `fmt.Print`를 사용해야 합니다. [#60529](/issue/60529)를 참조하십시오. 이 체크는 기존 코드에서 탐지 결과가 많이 발생하는 경향이 있으므로, 1.24 Go 툴체인으로 업데이트할 때 지속적 통합(CI) 실패가 발생하는 것을 방지하기 위해 언어 버전(go.mod의 `go` 지시어 또는 `//go:build` 주석으로 지정됨)이 최소 Go 1.24인 경우에만 적용됩니다.

<!-- go.dev/issue/64127 -->
기존의 `buildtag` 분석기가 이제 `//go:build` 지시문 내에 유효하지 않은 Go [주 버전 빌드 제약 조건](/pkg/cmd/go#hdr-Build_constraints)이 있을 때 진단 보고서를 생성합니다. 예를 들어, `//go:build go1.23.1`은 포인트 릴리스를 참조하므로, 대신 `//go:build go1.23`을 사용하십시오.
[#64127](/issue/64127)을 참조하십시오.

<!-- go.dev/issue/66387 -->
기존의 `copylock` 분석기는 이제 `for i := iter(); done(i); i = next(i) { ... }`와 같은 3절 "for" 루프에서 선언된 변수가 `sync.Mutex`와 같은 `sync.Locker`를 포함하는 경우 진단 보고서를 생성합니다. [Go 1.22](/doc/go1.22#language)에서는 이러한 루프의 동작이 변경되어 각 반복마다 이전 반복의 값을 복사하여 새로운 변수를 생성하도록 되었으며, 이러한 복사 작업은 락(lock)에 대해 안전하지 않습니다. [#66387](/issue/66387)을 참조하십시오.

### GOCACHEPROG

`GOCACHEPROG` 환경 변수는 Go 빌드 캐시의 읽기 및 쓰기 작업을 처리하는 데 사용할 프로그램을 지정합니다.

기본적으로 Go는 표준 파일 시스템 라이브러리를 사용하여 캐시를 관리하지만, 이 변수를 통해 캐시 작업을 가로채는 외부 도구를 지정할 수 있습니다. 이는 네트워크 파일 시스템이나 압축 파일 시스템과 같이 특수한 저장소 계층을 사용하여 빌드 캐시를 관리하려는 경우에 유용합니다.

`GOCACHEPROG`로 지정된 프로그램은 다음과 같은 표준 인터페이스를 통해 Go 툴체인과 통신해야 합니다:

1.  **명령어**: Go는 특정 작업을 수행하기 위해 프로그램을 호출하며, 각 호출에는 작업 유형을 나타내는 인자가 포함됩니다.
2.  **동작**: 프로그램은 파일을 읽고, 쓰고, 삭제하며, 디렉토리를 생성하는 등의 파일 시스템 작업을 에뮬레이션해야 합니다.

이 기능은 주로 고급 사용자나 빌드 인프라 최적화를 수행하는 팀을 위한 것이며, 일반적인 개발 환경에서는 설정할 필요가 없습니다.

<!-- go.dev/issue/64876 -->
`cmd/go` 내부의 바이너리 및 테스트 캐싱 메커니즘은 이제 `cmd/go` 도구와 `GOCACHEPROG` 환경 변수로 지정된 자식 프로세스 간의 JSON 프로토콜을 구현하는 자식 프로세스에 의해 구현될 수 있습니다.
이 기능은 이전에 GOEXPERIMENT 뒤에 숨겨져 있었습니다.
프로토콜에 대한 자세한 내용은 [문서](/cmd/go/internal/cacheprog)를 참조하십시오.

## 런타임 {#runtime}

<!-- go.dev/issue/54766 -->
<!-- go.dev/cl/614795 -->
<!-- go.dev/issue/68578 -->

런타임의 여러 성능 개선을 통해 대표적인 벤치마크 세트 전반에서 CPU 오버헤드가 평균 2~3% 감소했습니다.
결과는 애플리케이션에 따라 다를 수 있습니다.
이러한 개선 사항에는 [Swiss Tables](https://abseil.io/about/design/swisstables) 기반의 새로운 내장 `map` 구현, 소형 객체의 더 효율적인 메모리 할당, 그리고 새로운 런타임 내부 mutex 구현이 포함됩니다.

새로운 내장 `map` 구현과 새로운 런타임 내부 뮤텍스는 빌드 시 각각 `GOEXPERIMENT=noswissmap` 및 `GOEXPERIMENT=nospinbitmutex`를 설정하여 비활성화할 수 있습니다.

## 컴파일러 {#compiler}

<!-- go.dev/issue/60725, go.dev/issue/57926 -->
컴파일러는 이미 cgo로 생성된 리시버 타입을 사용하여 새로운 메서드를 정의하는 것을 금지하고 있었으나, 별칭 타입(alias type)을 통해 해당 제한을 우회하는 것이 가능했습니다.
Go 1.24부터는 리시버가 직접적으로든 간접적으로든(별칭 타입을 통해) cgo로 생성된 타입을 나타내는 경우 항상 에러를 보고합니다.

## 링커 (Linker) {#linker}

<!-- go.dev/issue/68678, go.dev/issue/68652, CL 618598, CL 618601 -->
이제 링커는 기본적으로 ELF 플랫폼에서 GNU 빌드 ID(ELF `NT_GNU_BUILD_ID` 노트)를, macOS에서 UUID(Mach-O `LC_UUID` 로드 커맨드)를 생성합니다.
빌드 ID 또는 UUID는 Go 빌드 ID로부터 파생됩니다.
이는 `-B none` 링커 플래그로 비활성화하거나, 사용자가 지정한 16진수 값인 `-B 0xNNNN` 링커 플래그로 재정의할 수 있습니다.

## Bootstrap {#bootstrap}

<!-- go.dev/issue/64751 -->
[Go 1.22 릴리스 노트](/doc/go1.22#bootstrap)에서 언급했듯이, Go 1.24의 부트스트랩(bootstrap)에는 이제 Go 1.22.6 이상의 버전이 필요합니다.
Go 1.26의 부트스트랩에는 Go 1.24의 포인트 릴리스 또는 그 이후 버전이 필요할 것으로 예상됩니다.

## 표준 라이브러리 {#library}

### 디렉토리 제한 파일 시스템 액세스

<!-- go.dev/issue/67002 -->
새로운 [`os.Root`](/pkg/os#Root) 타입은 특정 디렉터리 내에서 파일 시스템 작업을 수행하는 기능을 제공합니다.

[`os.OpenRoot`](/pkg/os#OpenRoot) 함수는 디렉토리를 열고 [`os.Root`](/pkg/os#Root)를 반환합니다.
[`os.Root`](/pkg/os#Root)의 메서드들은 해당 디렉토리 내에서 작동하며, 디렉토리 외부의 위치를 참조하는 경로(디렉토리 외부로 나가는 심볼릭 링크를 따르는 경로 포함)를 허용하지 않습니다.
`os.Root`의 메서드들은 예를 들어 [`os.Root.Open`](/pkg/os#Root.Open),
[`os.Root.Create`](/pkg/os#Root.Create),
[`os.Root.Mkdir`](/pkg/os#Root.Mkdir),
그리고 [`os.Root.Stat`](/pkg/os#Root.Stat)와 같이 `os` 패키지에서 사용할 수 있는 대부분의 파일 시스템 작업을 반영합니다.

### 새로운 벤치마크 함수

이제 벤치마크에서 `for range b.N`과 같이 `b.N`을 사용하는 일반적인 루프 구조 대신, 더 빠르고 오류 발생 가능성이 적은 [`testing.B.Loop`](/pkg/testing#B.Loop) 메서드를 사용하여 `for b.Loop() { ... }` 형태로 벤치마크 반복을 수행할 수 있습니다. 이는 다음과 같은 두 가지 중요한 이점을 제공합니다:
 - 벤치마크 함수가 `-count`당 정확히 한 번만 실행되므로, 비용이 많이 드는 설정(setup) 및 정리(cleanup) 단계가 한 번만 수행됩니다.
 - 함수 호출 매개변수와 결과값이 유지되어, 컴파일러가 루프 본문을 완전히 최적화하여 제거하는 것을 방지합니다.

### 개선된 finalizer

<!-- go.dev/issue/67535 -->
새로운 [`runtime.AddCleanup`](/pkg/runtime#AddCleanup) 함수는 [`runtime.SetFinalizer`](/pkg/runtime#SetFinalizer)보다 더 유연하고 효율적이며 오류 발생 가능성이 적은 종료 처리(finalization) 메커니즘입니다.
`AddCleanup`은 객체에 정리(cleanup) 함수를 연결하며, 이 함수는 해당 객체에 더 이상 접근할 수 없게 되면 한 번 실행됩니다.
하지만 `SetFinalizer`와 달리,
단일 객체에 여러 개의 cleanup 함수를 연결할 수 있고,
내부 포인터(interior pointers)에 cleanup 함수를 연결할 수 있으며,
객체들이 순환 구조(cycle)를 형성하더라도 일반적으로 메모리 누수를 일으키지 않고,
객체나 해당 객체가 가리키는 객체들의 해제 시점을 지연시키지 않습니다.
새로운 코드를 작성할 때는 `SetFinalizer`보다 `AddCleanup`을 사용하는 것이 권장됩니다.

### 새로운 weak 패키지 {#weak}

새로운 [`weak`](/pkg/weak/) 패키지는 약한 포인터(weak pointers)를 제공합니다.

약한 포인터(Weak pointers)는 값 연결을 위한 약한 맵(weak maps), [`unique`](/pkg/unique/) 패키지에서 다루지 않는 모든 항목을 위한 정규화 맵(canonicalization maps), 그리고 다양한 종류의 캐시와 같이 메모리 효율적인 구조의 생성을 가능하게 하기 위해 제공되는 저수준 프리미티브입니다.

이러한 사용 사례를 지원하기 위해, 이번 릴리스에서는 [`runtime.AddCleanup`](/pkg/runtime/#AddCleanup)과 [`maphash.Comparable`](/pkg/maphash/#Comparable)도 함께 제공합니다.

### 새로운 crypto/mlkem 패키지 {#crypto-mlkem}

<!-- go.dev/issue/70122 -->

새로운 [`crypto/mlkem`](/pkg/crypto/mlkem/) 패키지는 ML-KEM-768 및 ML-KEM-1024를 구현합니다.

ML-KEM은 이전에 Kyber로 알려졌으며 [FIPS 203](https://doi.org/10.6028/NIST.FIPS.203)에 정의된 양자 내성 키 교환 메커니즘입니다.

### 새로운 crypto/hkdf, crypto/pbkdf2 및 crypto/sha3 패키지 {#crypto-packages}

<!-- go.dev/issue/61477, go.dev/issue/69488, go.dev/issue/69982, go.dev/issue/65269, CL 629176 -->

새로운 [`crypto/hkdf`](/pkg/crypto/hkdf/) 패키지는 [RFC 5869](https://www.rfc-editor.org/rfc/rfc5869.html)에 정의된 HMAC 기반의 Extract-and-Expand 키 유도 함수인 HKDF를 구현합니다.

새로운 [`crypto/pbkdf2`](/pkg/crypto/pbkdf2/) 패키지는 [RFC 8018](https://www.rfc-editor.org/rfc/rfc8018.html)에 정의된 비밀번호 기반 키 유도 함수인 PBKDF2를 구현합니다.

새로운 [`crypto/sha3`](/pkg/crypto/sha3/) 패키지는 [FIPS 202](http://doi.org/10.6028/NIST.FIPS.202)에 정의된 SHA-3 해시 함수와 SHAKE 및 cSHAKE 확장 출력 함수(extendable-output functions)를 구현합니다.

세 패키지 모두 기존의 `golang.org/x/crypto/...` 패키지를 기반으로 합니다.

### FIPS 140-3 준수 {#fips140}

이번 릴리스에는 [FIPS 140-3 준수를 용이하게 하기 위한 새로운 메커니즘 세트](/doc/security/fips140)가 포함되어 있습니다.

Go Cryptographic Module은 FIPS 140-3 승인 알고리즘을 구현하기 위해 투명하게 사용되는 내부 표준 라이브러리 패키지 세트입니다. 애플리케이션은 승인된 알고리즘을 위해 Go Cryptographic Module을 사용하는 데 별도의 변경 사항이 필요하지 않습니다.

새로운 `GOFIPS140` 환경 변수를 사용하여 빌드 시 사용할 Go Cryptographic Module 버전을 선택할 수 있습니다. 새로운 `fips140` [GODEBUG 설정](/doc/godebug)을 사용하여 런타임에 FIPS 140-3 모드를 활성화할 수 있습니다.

Go 1.24에는 현재 CMVP 공인 실험실에서 테스트 중인 Go Cryptographic Module 버전 v1.0.0이 포함되어 있습니다.

### 새로운 실험적 testing/synctest 패키지 {#testing-synctest}

새로운 실험적 [`testing/synctest`](/pkg/testing/synctest/) 패키지는 동시성 코드 테스트를 위한 지원을 제공합니다.
- [`synctest.Run`](/pkg/testing/synctest/#Run) 함수는 격리된 "버블(bubble)" 내에서 고루틴 그룹을 시작합니다.
  버블 내부에서 [`time`](/pkg/time) 패키지 함수들은 가상 시계(fake clock)를 기반으로 동작합니다.
- [`synctest.Wait`](/pkg/testing/synctest#Wait) 함수는 현재 버블 내의 모든 고루틴이 블록(block) 상태가 될 때까지 대기합니다.

자세한 내용은 패키지 문서를 참조하십시오.

`synctest` 패키지는 실험적이며, 빌드 시 `GOEXPERIMENT=synctest`를 설정하여 활성화해야 합니다.
패키지 API는 향후 릴리스에서 변경될 수 있습니다.
자세한 정보 확인 및 피드백 제공은 [issue #67434](/issue/67434)를 참조하십시오.

### 라이브러리의 마이너 변경 사항 {#minor_library_changes}

#### [`archive`](/pkg/archive/)

`archive/zip`와 `archive/tar` 모두에서 `(*Writer).AddFS` 구현체가 이제 빈 디렉토리에 대해 디렉토리 헤더를 작성합니다.

#### [`bytes`](/pkg/bytes/)

[`bytes`](/pkg/bytes) 패키지는 이터레이터(iterator)와 함께 작동하는 여러 함수를 추가합니다:
- [`Lines`](/pkg/bytes#Lines)는 바이트 슬라이스에서 개행 문자로 끝나는 라인들에 대한 이터레이터를 반환합니다.
- [`SplitSeq`](/pkg/bytes#SplitSeq)는 구분자를 기준으로 분할된 바이트 슬라이스의 모든 하위 슬라이스들에 대한 이터레이터를 반환합니다.
- [`SplitAfterSeq`](/pkg/bytes#SplitAfterSeq)는 구분자가 나타나는 지점 뒤에서 분할된 바이트 슬라이스의 하위 슬라이스들에 대한 이터레이터를 반환합니다.
- [`FieldsSeq`](/pkg/bytes#FieldsSeq)는 [`unicode.IsSpace`](/pkg/unicode#IsSpace)에 정의된 공백 문자열을 기준으로 분할된 바이트 슬라이스의 하위 슬라이스들에 대한 이터레이터를 반환합니다.
- [`FieldsFuncSeq`](/pkg/bytes#FieldsFuncSeq)는 서술자(predicate)를 만족하는 유니코드 코드 포인트 문자열을 기준으로 분할된 바이트 슬라이스의 하위 슬라이스들에 대한 이터레이터를 반환합니다.

#### [`crypto/aes`](/pkg/crypto/aes/)

[`NewCipher`](/pkg/crypto/aes#NewCipher)가 반환하는 값은 더 이상 `NewCTR`, `NewGCM`, `NewCBCEncrypter` 및 `NewCBCDecrypter` 메서드를 구현하지 않습니다. 이 메서드들은 문서화되지 않았으며 모든 아키텍처에서 사용할 수 있었던 것도 아니었습니다. 대신, [`Block`](/pkg/crypto/cipher#Block) 값을 관련 [`crypto/cipher`](/pkg/crypto/cipher/) 함수로 직접 전달해야 합니다. 현재로서는 `crypto/cipher`가 표준 라이브러리에서 더 이상 사용하지 않더라도 `Block` 값에서 해당 메서드들이 있는지 여전히 확인합니다.

#### [`crypto/cipher`](/pkg/crypto/cipher/)

새로운 [`NewGCMWithRandomNonce`](/pkg/crypto/cipher#NewGCMWithRandomNonce) 함수는 Seal 과정에서 무작위 nonce를 생성하여 암호문 앞에 추가함으로써 AES-GCM을 구현하는 [`AEAD`](/pkg/crypto/cipher#AEAD)를 반환합니다.

[`crypto/aes`](/pkg/crypto/aes/)와 함께 [`NewCTR`](/pkg/crypto/cipher#NewCTR)를 사용하여 반환된 [`Stream`](/pkg/crypto/cipher#Stream) 구현이 이제 amd64 및 arm64에서 수 배 더 빨라졌습니다.

[`NewOFB`](/pkg/crypto/cipher#NewOFB),
[`NewCFBEncrypter`](/pkg/crypto/cipher#NewCFBEncrypter), 및
[`NewCFBDecrypter`](/pkg/crypto/cipher#NewCFBDecrypter)는 이제 deprecated 되었습니다.
OFB 및 CFB 모드는 인증되지 않으므로, 일반적으로 활성 공격(active attacks)을 통해 평문을 조작하고 복구하는 것이 가능합니다. 애플리케이션에서는 대신 [`AEAD`](/pkg/crypto/cipher#AEAD) 모드를 사용할 것을 권장합니다. 인증되지 않은 [`Stream`](/pkg/crypto/cipher#Stream) 모드가 필요한 경우에는 대신 [`NewCTR`](/pkg/crypto/cipher#NewCTR)를 사용하십시오.

#### [`crypto/ecdsa`](/pkg/crypto/ecdsa/)

<!-- go.dev/issue/64802 -->
`PrivateKey.Sign`(`/pkg/crypto/ecdsa#PrivateKey.Sign`)은 이제 random source가 nil인 경우 [RFC 6979](https://www.rfc-editor.org/rfc/rfc6979.html)에 따라 결정론적(deterministic) 서명을 생성합니다.

#### [`crypto/md5`](/pkg/crypto/md5/)

[`md5.New`](/pkg/md5#New)에 의해 반환되는 값은 이제 [`encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 인터페이스도 구현합니다.

#### [`crypto/rand`](/pkg/crypto/rand/)

<!-- go.dev/issue/66821 -->
이제 [`Read`](/pkg/crypto/rand#Read) 함수는 실패하지 않음이 보장됩니다.
이 함수는 `error` 결과로 항상 `nil`을 반환합니다.
만약 `Read`가 [`Reader`](/pkg/crypto/rand#Reader)로부터 읽는 동안 오류가 발생하면, 프로그램은 복구 불가능하게 충돌(crash)합니다.
기본 `Reader`가 사용하는 플랫폼 API는 항상 성공하는 것으로 문서화되어 있으므로, 이 변경 사항은 `Reader` 변수를 오버라이드하는 프로그램에만 영향을 미칠 것입니다. 한 가지 예외는 리눅스 커널 3.17 이전 버전으로, 이 버전에서는 기본 `Reader`가 여전히 `/dev/urandom`을 열며 실패할 가능성이 있습니다.

<!-- go.dev/issue/69577 -->
Linux 6.11 및 이후 버전에서 `Reader`는 이제 vDSO를 통해 `getrandom` 시스템 호출을 사용합니다.
이는 특히 작은 크기의 읽기 작업에서 여러 배 더 빠릅니다.

<!-- CL 608395 -->
OpenBSD에서 `Reader`가 이제 `arc4random_buf(3)`를 사용합니다.

<!-- go.dev/issue/67057 -->
새로운 [`Text`](/pkg/crypto/rand#Text) 함수를 사용하여 암호학적으로 안전한 무작위 텍스트 문자열을 생성할 수 있습니다.

#### [`crypto/rsa`](/pkg/crypto/rsa/)

[`GenerateKey`](/pkg/crypto/rsa#GenerateKey)는 이제 1024비트 미만의 키를 요청할 경우 에러를 반환합니다.
모든 Sign, Verify, Encrypt, Decrypt 메서드는 이제 1024비트보다 작은 키와 함께 사용될 경우 에러를 반환합니다. 이러한 키들은 안전하지 않으며 사용해서는 안 됩니다.
[GODEBUG 설정](/doc/godebug) `rsa1024min=0`을 사용하면 이전 동작으로 복구되지만, 필요한 경우에만, 그리고 예를 들어 테스트 파일에 `//go:debug rsa1024min=0` 라인을 추가하는 식으로 테스트에서만 사용할 것을 권장합니다.
새로운 `GenerateKey` [예제](/pkg/crypto/rsa#example-GenerateKey-TestKey)에서 사용하기 쉬운 표준 2048비트 테스트 키를 제공합니다.

이제 [`PrivateKey.Validate`](/pkg/crypto/rsa#PrivateKey.Validate)를 호출하기 전에 [`PrivateKey.Precompute`](/pkg/crypto/rsa#PrivateKey.Precompute)를 호출하는 것이 안전하며 더 효율적입니다. `Precompute`는 JSON에서 키를 언마샬링(unmarshaling)할 때와 같이 [`PrecomputedValues`](/pkg/crypto/rsa#PrecomputedValues)가 일부만 채워져 있는 경우 더 빠르게 동작합니다.

이제 `Validate`가 호출되지 않더라도 더 많은 잘못된 키를 거부하며, [`GenerateKey`](/pkg/crypto/rsa#GenerateKey)는 손상된 난수 소스에 대해 새로운 에러를 반환할 수 있습니다.
[`PrivateKey`](/pkg/crypto/rsa#PrivateKey)의 [`Primes`](/pkg/crypto/rsa#PrivateKey.Primes) 및 [`Precomputed`](/pkg/crypto/rsa#PrivateKey.Precomputed) 필드는 이제 일부 값이 누락된 경우에도 사용되고 검증됩니다.
RSA 키의 파싱 및 마샬링에 관한 `crypto/x509` 변경 사항은 [아래 설명](#cryptox509pkgcryptox509)을 참조하십시오.

<!-- go.dev/issue/43923 -->
[`SignPKCS1v15`](/pkg/crypto/rsa#SignPKCS1v15) 및
[`VerifyPKCS1v15`](/pkg/crypto/rsa#VerifyPKCS1v15)가 이제
SHA-512/224, SHA-512/256 및 SHA-3를 지원합니다.

<!-- CL 639936 -->
[`GenerateKey`](/pkg/crypto/rsa#GenerateKey)가 이제 개인 지수(private exponent)를 생성하기 위해 약간 다른 방법(오일러 피 함수 대신 카마이클 함수 사용)을 사용합니다. 소수 인수(prime factors)만으로 외부에서 키를 재생성하는 일부 드문 애플리케이션의 경우, 결과가 달라질 수 있으나 서로 호환됩니다.

<!-- CL 626957 -->
이제 wasm에서 공개키 및 개인키 연산 속도가 최대 2배 더 빨라졌습니다.

#### [`crypto/sha1`](/pkg/crypto/sha1/)

[`sha1.New`](/pkg/sha1#New)가 반환하는 값은 이제 [`encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 인터페이스도 구현합니다.

#### [`crypto/sha256`](/pkg/crypto/sha256/)

[`sha256.New`](/pkg/sha256#New) 및 [`sha256.New224`](/pkg/sha256#New224)가 반환하는 값들이 이제 [`encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 인터페이스를 구현합니다.

#### [`crypto/sha512`](/pkg/crypto/sha512/)

[`sha512.New`](/pkg/sha512#New),
[`sha512.New384`](/pkg/sha512#New384),
[`sha512.New512_224`](/pkg/sha512#New512_224) 및
[`sha512.New512_256`](/pkg/sha512#New512_256)에 의해 반환되는 값들이 이제
[`encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 인터페이스도 구현합니다.

#### [`crypto/subtle`](/pkg/crypto/subtle/)

새로운 [`WithDataIndependentTiming`](/pkg/crypto/subtle#WithDataIndependentTiming) 함수를 사용하면 사용자는 특정 명령어가 데이터 값에 관계없이 일정한 실행 시간을 갖도록 보장하는 아키텍처별 기능을 활성화하여 함수를 실행할 수 있습니다. 이는 상수 시간(constant time)으로 실행되도록 설계된 코드가 CPU 수준의 기능에 의해 최적화되어 가변 시간(variable time)으로 동작하는 것을 방지하는 데 사용될 수 있습니다. 현재 `WithDataIndependentTiming`은 arm64의 PSTATE.DIT 비트를 사용하며, 그 외 모든 아키텍처에서는 아무런 동작을 하지 않습니다(no-op). [GODEBUG 설정](/doc/godebug) `dataindependenttiming=1`을 사용하면 Go 프로그램 전체에 대해 DIT 모드가 활성화됩니다.

<!-- CL 622276 -->
[`XORBytes`](/pkg/crypto/subtle#XORBytes)의 출력값은 입력값과 완전히 겹치거나 전혀 겹치지 않아야 합니다. 이전에는 그 외의 경우 동작이 정의되지 않았으나, 이제 `XORBytes`는 panic을 발생시킵니다.

#### [`crypto/tls`](/pkg/crypto/tls/)

이제 TLS 서버가 Encrypted Client Hello (ECH)를 지원합니다. 이 기능은 [`Config.EncryptedClientHelloKeys`](/pkg/crypto/tls#Config.EncryptedClientHelloKeys) 필드를 설정하여 활성화할 수 있습니다.

새로운 양자 내성 [`X25519MLKEM768`](/pkg/crypto/tls#X25519MLKEM768) 키 교환 메커니즘이 이제 지원되며, [`Config.CurvePreferences`](/pkg/crypto/tls#Config.CurvePreferences)가 nil인 경우 기본적으로 활성화됩니다.
[GODEBUG 설정](/doc/godebug) `tlsmlkem=0`을 통해 기본 설정을 되돌릴 수 있습니다.
이는 대형 레코드를 올바르게 처리하지 못해 핸드셰이크 중 타임아웃이 발생하는 버그가 있는 TLS 서버를 다룰 때 유용할 수 있습니다 ( [TLS post-quantum TL;DR fail](https://tldr.fail/) 참고).

실험적인 `X25519Kyber768Draft00` 키 교환에 대한 지원이 제거되었습니다.

<!-- go.dev/issue/69393, CL 630775 -->
이제 키 교환 순서는 `crypto/tls` 패키지에서 전적으로 처리됩니다. [`Config.CurvePreferences`](/pkg/crypto/tls#Config.CurvePreferences)의 순서는 이제 무시되며, 해당 필드가 채워져 있을 때 어떤 키 교환을 활성화할지 결정하는 용도로만 사용됩니다.

<!-- go.dev/issue/32936 -->
새로운 [`ClientHelloInfo.Extensions`](/pkg/crypto/tls#ClientHelloInfo.Extensions)
필드는 Client Hello 메시지에서 수신한 확장(extension)들의 ID 목록을 제공합니다.
이는 TLS 클라이언트의 핑거프린팅(fingerprinting)에 유용하게 사용될 수 있습니다.

<!-- go.dev/issue/72111, Go 1.27 릴리스 이후 소급하여 문서화됨 -->

`tlskyber` `GODEBUG` 설정([Go 1.23](/doc/godebug#go-123에서 추가됨)이 제거되었습니다.

#### [`crypto/x509`](/pkg/crypto/x509/)

<!-- go.dev/issue/41682 -->
`x509sha1` [GODEBUG 설정](/doc/godebug)이 제거되었습니다.
[`Certificate.Verify`](/pkg/crypto/x509#Certificate.Verify)는 더 이상 SHA-1 기반 서명을 지원하지 않습니다.

[`OID`](/pkg/crypto/x509#OID)가 이제 [`encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 및 [`encoding.TextAppender`](/pkg/encoding#TextAppender) 인터페이스를 구현합니다.

기본 인증서 정책 필드가 [`Certificate.PolicyIdentifiers`](/pkg/crypto/x509#Certificate.PolicyIdentifiers)에서 [`Certificate.Policies`](/pkg/crypto/x509#Certificate.Policies)로 변경되었습니다. 인증서를 파싱할 때는 두 필드가 모두 채워지지만, 인증서를 생성할 때는 이제 `Certificate.PolicyIdentifiers` 필드 대신 `Certificate.Policies` 필드에서 정책을 가져옵니다. 이 변경 사항은 [GODEBUG 설정](/doc/godebug) `x509usepolicies=0`을 통해 되돌릴 수 있습니다.

<!-- go.dev/issue/67675 -->
[`CreateCertificate`](/pkg/crypto/x509#CreateCertificate)에 [`Certificate.SerialNumber`](/pkg/crypto/x509#Certificate.SerialNumber) 필드가 nil인 템플릿이 전달될 때, 실패하는 대신 이제 RFC 5280을 준수하는 방식으로 일련번호(serial number)를 생성합니다.

[`Certificate.Verify`](/pkg/crypto/x509#Certificate.Verify)가 이제 RFC 5280 및 RFC 9618에 정의된 정책 검증(policy validation)을 지원합니다. 새로운 [`VerifyOptions.CertificatePolicies`](/pkg/crypto/x509#VerifyOptions.CertificatePolicies) 필드를 통해 허용 가능한 정책 [`OIDs`](/pkg/crypto/x509#OID) 집합을 설정할 수 있습니다. 유효한 정책 그래프를 가진 인증서 체인만이 [`Certificate.Verify`](/pkg/crypto/x509#Certificate.Verify)를 통해 반환됩니다.

[`MarshalPKCS8PrivateKey`](/pkg/crypto/x509#MarshalPKCS8PrivateKey)가 이제 유효하지 않은 RSA 키를 마샬링하는 대신 에러를 반환합니다.
([`MarshalPKCS1PrivateKey`](/pkg/crypto/x509#MarshalPKCS1PrivateKey)는 에러를 반환하지 않으며, 유효하지 않은 키가 제공되었을 때의 동작은 계속해서 정의되지 않은 상태로 유지됩니다.)

[`ParsePKCS1PrivateKey`](/pkg/crypto/x509#ParsePKCS1PrivateKey) 및
[`ParsePKCS8PrivateKey`](/pkg/crypto/x509#ParsePKCS8PrivateKey)가 이제 인코딩된 CRT 값을 사용하고
검증하므로, 이전에는 허용되었던 잘못된 RSA 키를 거부할 수 있습니다. CRT 값을 다시 계산하는 이전 방식으로 되돌리려면 [GODEBUG 설정](/doc/godebug) `x509rsacrt=0`을 사용하십시오.

#### [`debug/elf`](/pkg/debug/elf/)

<!-- go.dev/issue/63952 -->

[`debug/elf`](/pkg/debug/elf) 패키지는 동적 ELF(Executable and Linkable Format) 파일의 심볼 버전을 처리하는 기능을 추가합니다.
새로운 [`File.DynamicVersions`](/pkg/debug/elf#File.DynamicVersions) 메서드는 ELF 파일에 정의된 동적 버전 목록을 반환합니다.
새로운 [`File.DynamicVersionNeeds`](/pkg/debug/elf#File.DynamicVersionNeeds) 메서드는 이 ELF 파일에서 필요로 하며 다른 ELF 객체에 정의된 동적 버전 목록을 반환합니다.
마지막으로, 새로운 [`Symbol.HasVersion`](/pkg/debug/elf#Symbol) 및 [`Symbol.VersionIndex`](/pkg/debug/elf#Symbol) 필드는 심볼의 버전을 나타냅니다.

#### [`encoding`](/pkg/encoding/)

객체의 텍스트 또는 바이너리 표현을 바이트 슬라이스에 추가하기 위해 두 개의 새로운 인터페이스인 [`TextAppender`](/pkg/encoding#TextAppender)와 [`BinaryAppender`](/pkg/encoding#BinaryAppender)가 도입되었습니다. 이 인터페이스들은 [`TextMarshaler`](/pkg/encoding#TextMarshaler) 및 [`BinaryMarshaler`](/pkg/encoding#BinaryMarshaler)와 동일한 기능을 제공하지만, 매번 새로운 슬라이스를 할당하는 대신 기존 슬라이스에 데이터를 직접 추가합니다.
이제 `TextMarshaler` 및/또는 `BinaryMarshaler`를 이미 구현하고 있던 표준 라이브러리 타입들이 이 인터페이스들을 구현합니다.

#### [`encoding/json`](/pkg/encoding/json/)

<!-- go.dev/issue/45669 -->
마샬링 시, 구조체 필드 태그에 새로운 `omitzero` 옵션이 지정되어 있고 해당 필드의 값이 제로 값(zero value)인 경우, 그 필드는 생략됩니다. 필드 타입에 `IsZero() bool` 메서드가 있는 경우, 해당 메서드를 사용하여 값이 제로 값인지 판단합니다. 그렇지 않은 경우, 해당 값이 [타입에 따른 제로 값](/ref/spec#The_zero_value)이면 제로 값으로 간주합니다.

제로 값을 생략하려는 의도일 때, `omitzero` 필드 태그는 `omitempty`보다 더 명확하며 오류가 발생할 가능성이 적습니다.

특히 `omitempty`와 달리, `omitzero`는 제로 값인 [`time.Time`](/pkg/time#Time) 값도 생략하며, 이는 그동안 흔히 발생하던 불편함을 해결해 줍니다.

`omitempty`와 `omitzero`가 모두 지정된 경우, 값이 비어 있거나(empty) 제로 값(zero)인 경우(또는 둘 다인 경우) 해당 필드는 생략됩니다.

[`UnmarshalTypeError.Field`](/pkg/encoding/json#UnmarshalTypeError.Field)에 이제 임베디드 구조체(embedded structs)가 포함되어 더 상세한 에러 메시지를 제공합니다.

#### [`go/types`](/pkg/go/types/)

`Len() int` 및 `At(int) T`와 같은 메서드 쌍을 통해 시퀀스를 노출하는 모든 `go/types` 데이터 구조에 이제 이터레이터를 반환하는 메서드가 추가되었습니다. 이를 통해 다음과 같은 코드를 간소화할 수 있습니다:

```
params := fn.Type.(*types.Signature).Params()
for i := 0; i < params.Len(); i++ {
   use(params.At(i))
}
```

번역할 내용을 제공해 주세요. 영문 마크다운 내용을 입력해 주시면, 요청하신 대로 구조, 헤더, 표, 링크, 리스트, 인라인 코드 및 코드 펜스를 유지하면서 기술적으로 정확하게 한국어로 번역해 드리겠습니다. Go 패키지 이름, 식별자, URL, 명령어 및 코드 스니펫은 번역하지 않고 그대로 유지하겠습니다.

```
for param := range fn.Signature().Params().Variables() {
   use(param)
}
```

메서드들은 다음과 같습니다:
[`Interface.EmbeddedTypes`](/pkg/go/types#Interface.EmbeddedTypes),
[`Interface.ExplicitMethods`](/pkg/go/types#Interface.ExplicitMethods),
[`Interface.Methods`](/pkg/go/types#Interface.Methods),
[`MethodSet.Methods`](/pkg/go/types#MethodSet.Methods),
[`Named.Methods`](/pkg/go/types#Named.Methods),
[`Scope.Children`](/pkg/go/types#Scope.Children),
[`Struct.Fields`](/pkg/go/types#Struct.Fields),
[`Tuple.Variables`](/pkg/go/types#Tuple.Variables),
[`TypeList.Types`](/pkg/go/types#TypeList.Types),
[`TypeParamList.TypeParams`](/pkg/go/types#TypeParamList.TypeParams),
[`Union.Terms`](/pkg/go/types#Union.Terms).

#### [`hash/adler32`](/pkg/hash/adler32/)

[`New`](/pkg/hash/adler32#New)에서 반환되는 값은 이제 [`encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 인터페이스도 구현합니다.

#### [`hash/crc32`](/pkg/hash/crc32/)

[`New`](/pkg/hash/crc32#New) 및 [`NewIEEE`](/pkg/hash/crc32#NewIEEE)가 반환하는 값들이 이제 [`encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 인터페이스도 구현합니다.

#### [`hash/crc64`](/pkg/hash/crc64/)

[`New`](/pkg/hash/crc64#New)에 의해 반환되는 값은 이제 [`encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 인터페이스도 구현합니다.

#### [`hash/fnv`](/pkg/hash/fnv/)

[`New32`](/pkg/hash/fnv#New32), [`New32a`](/pkg/hash/fnv#New32a), [`New64`](/pkg/hash/fnv#New64), [`New64a`](/pkg/hash/fnv#New64a), [`New128`](/pkg/hash/fnv#New128) 및 [`New128a`](/pkg/hash/fnv#New128a)에서 반환하는 값들이 이제 [`encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 인터페이스도 구현합니다.

#### [`hash/maphash`](/pkg/hash/maphash/)

새로운 [`Comparable`](/pkg/hash/maphash#Comparable) 및
[`WriteComparable`](/pkg/hash/maphash#WriteComparable) 함수를 사용하여 모든 비교 가능한(comparable) 값의
해시를 계산할 수 있습니다.
이를 통해 Go 맵 키로 사용할 수 있는 모든 항목에 대해 해싱이 가능해졌습니다.

#### [`log/slog`](/pkg/log/slog/)

새로운 [`DiscardHandler`](/pkg/log/slog#DiscardHandler)는 절대 활성화되지 않으며 항상 출력을 폐기하는 핸들러입니다.

[`Level`](/pkg/log/slog#Level) 및 [`LevelVar`](/pkg/log/slog#LevelVar)가 이제 [`encoding.TextAppender`](/pkg/encoding#TextAppender) 인터페이스를 구현합니다.

#### [`math/big`](/pkg/math/big/)

[`Float`](/pkg/math/big#Float), [`Int`](/pkg/math/big#Int) 및 [`Rat`](/pkg/math/big#Rat)이 이제 [`encoding.TextAppender`](/pkg/encoding#TextAppender) 인터페이스를 구현합니다.

#### [`math/rand`](/pkg/math/rand/)

더 이상 사용되지 않는(deprecated) 최상위 [`Seed`](/pkg/math/rand#Seed) 함수 호출은 더 이상 아무런 영향을 주지 않습니다. 이전 동작으로 복구하려면 [GODEBUG 설정](/doc/godebug) `randseednop=0`을 사용하십시오. 자세한 배경 내용은 [제안서 #67273](/issue/67273)을 참조하십시오.

#### [`math/rand/v2`](/pkg/math/rand/v2/)

[`ChaCha8`](/pkg/math/rand/v2#ChaCha8)와 [`PCG`](/pkg/math/rand/v2#PCG)가 이제 [`encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 인터페이스를 구현합니다.

#### [`net`](/pkg/net/)

[`ListenConfig`](/pkg/net#ListenConfig)는 이제 이를 지원하는 시스템(현재 리눅스만 해당)에서 기본적으로 MPTCP를 사용합니다.

[`IP`](/pkg/net#IP)가 이제 [`encoding.TextAppender`](/pkg/encoding#TextAppender) 인터페이스를 구현합니다.

#### [`net/http`](/pkg/net/http/)

[`Transport`](/pkg/net/http#Transport)가 요청에 대해 수신하는 1xx 정보 응답(informational responses)에 대한 제한 사항이 변경되었습니다.
이전에는 5개 이상의 1xx 응답을 수신하면 요청을 중단하고 에러를 반환했습니다.
이제는 모든 1xx 응답의 총 크기가 [`Transport.MaxResponseHeaderBytes`](/pkg/net/http#Transport.MaxResponseHeaderBytes) 설정 값을 초과하는 경우 에러를 반환합니다.

또한, 요청에 [`net/http/httptrace.ClientTrace.Got1xxResponse`](/pkg/net/http/httptrace#ClientTrace.Got1xxResponse) 트레이스 훅이 있는 경우, 이제 1xx 응답의 총 횟수에 제한이 없습니다. `Got1xxResponse` 훅은 요청을 중단하기 위해 에러를 반환할 수 있습니다.

[`Transport`](/pkg/net/http#Transport)와 [`Server`](/pkg/net/http#Server)에 HTTP/2 프로토콜 설정을 구성할 수 있는 HTTP2 필드가 추가되었습니다.

새로운 [`Server.Protocols`](/pkg/net/http#Server.Protocols) 및 [`Transport.Protocols`](/pkg/net/http#Transport.Protocols) 필드는 서버나 클라이언트가 사용할 HTTP 프로토콜을 설정하는 간단한 방법을 제공합니다.

서버와 클라이언트는 암호화되지 않은 HTTP/2 연결을 지원하도록 설정될 수 있습니다.

[`Server.Protocols`](/pkg/net/http#Server.Protocols)에 UnencryptedHTTP2가 포함되어 있으면, 서버는 암호화되지 않은 포트에서 HTTP/2 연결을 허용합니다. 서버는 동일한 포트에서 HTTP/1과 암호화되지 않은 HTTP/2를 모두 허용할 수 있습니다.

[`Transport.Protocols`](/pkg/net/http#Transport.Protocols)에 UnencryptedHTTP2가 포함되어 있고 HTTP1이 포함되어 있지 않은 경우, transport는 http:// URL에 대해 암호화되지 않은 HTTP/2를 사용합니다.
transport가 HTTP/1과 암호화되지 않은 HTTP/2를 모두 사용하도록 설정된 경우, HTTP/1을 사용합니다.

암호화되지 않은 HTTP/2 지원은 "Prior Knowledge를 통한 HTTP/2"(RFC 9113, 섹션 3.3)를 사용합니다. 더 이상 사용되지 않는 "Upgrade: h2c" 헤더는 지원되지 않습니다.

#### [`net/netip`](/pkg/net/netip/)

[`Addr`](/pkg/net/netip#Addr), [`AddrPort`](/pkg/net/netip#AddrPort) 및 [`Prefix`](/pkg/net/netip#Prefix)가 이제 [`encoding.BinaryAppender`](/pkg/encoding#BinaryAppender)와 [`encoding.TextAppender`](/pkg/encoding#TextAppender) 인터페이스를 구현합니다.

#### [`net/url`](/pkg/net/url/)

[`URL`](/pkg/net/url#URL)이 이제 [`encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 인터페이스도 구현합니다.

#### [`os/user`](/pkg/os/user/)

Windows에서 [`Current`](/pkg/os/user#Current)를 이제 Windows Nano Server에서도 사용할 수 있습니다.
Nano Server에서 사용할 수 없는 `NetApi32` 라이브러리의 함수 사용을 피하도록 구현이 업데이트되었습니다.

Windows에서 [`Current`](/pkg/os/user#Current), [`Lookup`](/pkg/os/user#Lookup) 및 [`LookupId`](/pkg/os/user#LookupId)가 이제 다음의 빌트인 서비스 사용자 계정을 지원합니다:
- `NT AUTHORITY\SYSTEM`
- `NT AUTHORITY\LOCAL SERVICE`
- `NT AUTHORITY\NETWORK SERVICE`

Windows에서 현재 사용자가 느린 도메인에 가입되어 있는 경우(많은 기업 사용자의 일반적인 사례), [`Current`](/pkg/os/user#Current)의 속도가 상당히 빨라졌습니다. 새로운 구현의 성능은 밀리초 단위로 향상되었으며, 이는 완료까지 수 초 또는 심지어 수 분이 걸릴 수 있었던 이전 구현과 대조적입니다.

Windows에서, 현재 스레드가 다른 사용자를 impersonating(가장)하고 있을 때 [`Current`](/pkg/os/user#Current)가 이제 프로세스 소유자 사용자를 반환합니다. 이전에는 에러를 반환했습니다.

#### [`regexp`](/pkg/regexp/)

[`Regexp`](/pkg/regexp#Regexp)가 이제 [`encoding.TextAppender`](/pkg/encoding#TextAppender) 인터페이스를 구현합니다.

#### [`runtime`](/pkg/runtime/)

[`GOROOT`](/pkg/runtime#GOROOT) 함수는 이제 deprecated 되었습니다.
새로운 코드에서는 시스템 경로를 통해 “go” 바이너리를 찾는 방식을 권장하며,
`go env GOROOT`를 사용하여 GOROOT를 찾으십시오.

#### [`strings`](/pkg/strings/)

[`strings`](/pkg/strings) 패키지는 반복자(iterator)와 함께 작동하는 여러 함수를 추가합니다:
- [`Lines`](/pkg/strings#Lines)는 문자열에서 줄 바꿈으로 끝나는 각 줄에 대한 반복자를 반환합니다.
- [`SplitSeq`](/pkg/strings#SplitSeq)는 구분자를 기준으로 분할된 문자열의 모든 하위 문자열에 대한 반복자를 반환합니다.
- [`SplitAfterSeq`](/pkg/strings#SplitAfterSeq)는 구분자가 나타난 직후를 기준으로 분할된 문자열의 하위 문자열에 대한 반복자를 반환합니다.
- [`FieldsSeq`](/pkg/strings#FieldsSeq)는 [`unicode.IsSpace`](/pkg/unicode#IsSpace)에 정의된 공백 문자열을 기준으로 분할된 하위 문자열에 대한 반복자를 반환합니다.
- [`FieldsFuncSeq`](/pkg/strings#FieldsFuncSeq)는 서술자(predicate)를 만족하는 유니코드 코드 포인트 연속을 기준으로 분할된 하위 문자열에 대한 반복자를 반환합니다.

#### [`sync`](/pkg/sync/)

[`sync.Map`](/pkg/sync#Map)의 구현이 변경되어, 특히 맵 수정 시의 성능이 향상되었습니다.
예를 들어, 더 큰 맵에서 서로 겹치지 않는 키 집합을 수정할 때 경합(contention)이 발생할 가능성이 훨씬 낮아졌으며, 맵에서 낮은 경합 부하를 달성하기 위해 필요했던 준비 시간(ramp-up time)이 더 이상 필요하지 않습니다.

문제가 발생할 경우, 빌드 시 `GOEXPERIMENT=nosynchashtriemap`를 설정하여 이전 구현 방식으로 되돌리고 [이슈를 제출](/issue/new)해 주시기 바랍니다.

#### [`testing`](/pkg/testing/)

새로운 [`T.Context`](/pkg/testing#T.Context) 및 [`B.Context`](/pkg/testing#B.Context) 메서드는 테스트가 완료된 후 그리고 테스트 정리(cleanup) 함수들이 실행되기 전에 취소되는 context를 반환합니다.

<!-- 6-stdlib/6-testing-bloop.md에 언급된 testing.B.Loop입니다. -->

새로운 [`T.Chdir`](/pkg/testing#T.Chdir) 및 [`B.Chdir`](/pkg/testing#B.Chdir) 메서드를 사용하여 테스트 또는 벤치마크가 실행되는 동안 작업 디렉터리를 변경할 수 있습니다.

#### [`text/template`](/pkg/text/template/)

템플릿에서 이제 `range-over-func` 및 `range-over-int`를 지원합니다.

#### [`time`](/pkg/time/)

[`Time`](/pkg/time#Time)은 이제 [`encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 및 [`encoding.TextAppender`](/pkg/encoding#TextAppender) 인터페이스를 구현합니다.

## Ports {#ports}

### Linux {#linux}

<!-- go.dev/issue/67001 -->
Go 1.23 릴리스 노트에서 [공지](go1.23#linux)한 바와 같이, Go 1.24는 Linux 커널 버전 3.2 이상이 필요합니다.

### Darwin {#darwin}

<!-- go.dev/issue/69839 -->
Go 1.24은 macOS 11 Big Sur에서 실행되는 마지막 릴리스입니다.
Go 1.25부터는 macOS 12 Monterey 또는 그 이후 버전이 필요합니다.

### WebAssembly {#wasm}

<!-- go.dev/issue/65199, CL 603055 -->
Go 프로그램이 WebAssembly 호스트로 함수를 내보낼 수 있도록 `go:wasmexport` 컴파일러 지시어가 추가되었습니다.

WebAssembly System Interface Preview 1 (`GOOS=wasip1 GOARCH=wasm`)에서 Go 1.24는 `-buildmode=c-shared` 빌드 플래그를 지정하여 Go 프로그램을 [reactor/library](https://github.com/WebAssembly/WASI/blob/63a46f61052a21bfab75a76558485cf097c0dbba/legacy/application-abi.md#current-unstable-abi)로 빌드하는 것을 지원합니다.

<!-- go.dev/issue/66984, CL 626615 -->
이제 더 많은 타입이 `go:wasmimport` 함수의 인자 또는 결과 타입으로 허용됩니다.
구체적으로, 기존에 허용되었던 32비트 및 64비트 정수 및 부동 소수점 타입, `unsafe.Pointer`와 더불어 `bool`, `string`, `uintptr` 및 특정 타입에 대한 포인터가 허용됩니다 (자세한 내용은 [문서](/pkg/cmd/compile#hdr-WebAssembly_Directives) 참조).
이러한 타입들은 `go:wasmexport` 함수의 인자 또는 결과 타입으로도 허용됩니다.

<!-- go.dev/issue/68024 -->
WebAssembly 지원 파일이 `misc/wasm`에서 `lib/wasm`으로 이동되었습니다.

<!-- CL 621635, CL 621636 -->
초기 메모리 크기가 크게 감소했으며, 특히 소규모 WebAssembly 애플리케이션에서 더욱 두드러집니다.

### Windows {#windows}

<!-- go.dev/issue/70705 -->
32비트 windows/arm 포트(`GOOS=windows GOARCH=arm`)가 broken 상태로 표시되었습니다.
자세한 내용은 [issue #70705](/issue/70705)를 참조하십시오.

<!-- Go 1.24 릴리스 노트에 언급될 필요는 없으나 relnote todo에 의해 선택된 항목들입니다. -->

승인된 제안 https://go.dev/issue/25309 (https://go.dev/cl/594018, https://go.dev/cl/595120, https://go.dev/cl/595564, https://go.dev/cl/601778 기반) - 새로운 x/crypto 패키지; 언급할 필요가 없어 보임
승인된 제안 https://go.dev/issue/43744 (https://go.dev/cl/357530 기반) - 표준 라이브러리 변경 사항 없음
승인된 제안 https://go.dev/issue/60905 (https://go.dev/cl/610195 기반) - CL 610195 되돌림(reverted)
승인된 제안 https://go.dev/issue/61395 (https://go.dev/cl/594738, https://go.dev/cl/594976 기반) - CL 594738은 amd64에서 sync/atomic AND/OR 연산을 intrinsic으로 만들었으나, API는 이미 Go 1.23에 추가됨; CL 594976은 수정 사항임; 아마도 Go 1.24 릴리스 노트에 필요하지 않음 (성능 변경만 해당)
승인된 제안 https://go.dev/issue/51269 (https://go.dev/cl/627035 기반) - Go 1.24 릴리스 노트에 언급할 가치가 있거나, 제외해도 무방함; https://go.dev/issue/51269#issuecomment-2501802763 에서 논의됨; Ian이 제외해도 괜찮다고 확인함
승인된 제안 https://go.dev/issue/66540 (https://go.dev/cl/603958 기반) - Go 언어 사양(spec) 명확화; Go 1.24 릴리스 노트에 언급할 필요가 없을 수 있음; https://go.dev/issue/66540#issuecomment-2502051684 에 의견을 남김; Robert가 실제로 필요하지 않음을 확인함
승인된 제안 https://go.dev/issue/34208 (https://go.dev/cl/586241 기반) - CL 586241은 Go 1.23 기능에 대한 수정 사항을 구현함, Go 1.24 릴리스 노트에 필요한 내용은 없어 보임
승인된 제안 https://go.dev/issue/43993 (https://go.dev/cl/626116 기반) - CL 626116은 vet 변경을 위해 트리를 준비하지만 vet 변경 자체는 Go 1.24에 구현되지 않음, 따라서 Go 1.24 릴리스 노트에 기재할 내용 없음
승인된 제안 https://go.dev/issue/44505 (https://go.dev/cl/609955 기반) - CL 609955는 x/tools 내부 정리 작업임, Go 1.24 릴리스 노트 불필요
승인된 제안 https://go.dev/issue/61476 (https://go.dev/cl/608255 기반) - CL 608255는 Go 1.23에 추가된 GORISCV64를 기반으로 함; Go 1.24 릴리스 노트에 언급할 내용 없음
승인된 제안 https://go.dev/issue/66315 (https://go.dev/cl/577996 기반) - x/tools/go/analysis에 Pass.Module 필드를 추가하는 것은 Go 1.24 릴리스 노트에 언급할 사항이 아닌 것으로 보임
승인된 제안 https://go.dev/issue/57786 (https://go.dev/cl/472717 기반) - CL 472717은 x/net/http2에 있으며 Go 1.21 제안을 언급함; Go 1.24 릴리스 노트에 필요한 내용은 없어 보임
승인된 제안 https://go.dev/issue/54265 (https://go.dev/cl/609915, https://go.dev/cl/610675 기반) - Go 1.22 제안을 참조하는 CL들임, Go 1.24 릴리스 노트에 추가로 필요한 내용 없음
승인된 제안 https://go.dev/issue/53021 (https://go.dev/cl/622276 기반) - CL 622276은 문서를 개선함; 제안 53021은 Go 1.20 당시에 이루어졌으므로 Go 1.24 릴리스 노트에 추가로 필요한 내용 없음
승인된 제안 https://go.dev/issue/51430 (https://go.dev/cl/613375 기반) - CL 613375는 내부 문서 주석임; 제안 51430은 Go 1.20/1.21 당시에 이루어졌으므로 Go 1.24 릴리스 노트에 추가로 필요한 내용 없음
승인된 제안 https://go.dev/issue/38445 (https://go.dev/cl/626495 기반) - CL 626495는 x/tools/go/package에 관한 제안 38445에 대한 작업임, Go 1.24 릴리스 노트에 필요한 내용 없음
승인된 제안 https://go.dev/issue/56986 (https://go.dev/cl/618115 기반) - CL 618115는 문서를 추가함; Go 1.24 릴리스 노트에 언급될 필요 없음
승인된 제안 https://go.dev/issue/60061 (https://go.dev/cl/612038 기반) - CL 612038은 x/tools/go/ast의 일부 항목을 deprecated하고 Go 1.22 제안을 언급하는 CL임; Go 1.24 릴리스 노트에 필요한 내용 없음
승인된 제안 https://go.dev/issue/61324 (https://go.dev/cl/411907 기반) - CL 411907은 x/tools의 새로운 패키지에 대한 제안을 구현한 CL임; Go 1.24 릴리스 노트에 필요한 내용 없음
승인된 제안 https://go.dev/issue/61777 (https://go.dev/cl/601496 기반) - CL 601496은 x/net/http2.Server에 WriteByteTimeout 필드를 추가함; Go 1.24 릴리스 노트 불필요
승인된 제안 https://go.dev/issue/61940 (https://go.dev/cl/600997 기반) - CL 600997은 x/build의 오래된 코드를 삭제하고 승인된 제안을 언급함; Go 1.24 릴리스 노트 불필요
승인된 제안 https://go.dev/issue/62113 (https://go.dev/cl/594195 기반) - CL 594195는 x/net/html에 iterator 관련 내용을 추가함; Go 1.24 릴리스 노트 불필요
승인된 제안 https://go.dev/issue/62484 (https://go.dev/cl/600775 기반) - CL 600775는 CopyFS 심볼릭 링크 동작을 문서화하고 Go 1.23 제안을 언급함; Go 1.24 릴리스 노트 불필요
승인된 제안 https://go.dev/issue/64207 (https://go.dev/cl/605875 기반) - Go 1.23 제안의 후속 조치인 x/website CL임; Go 1.24 릴리스 노트 불필요
승인된 제안 https://go.dev/issue/65236 (https://go.dev/cl/596135 기반) - CL 596135는 Go 1.23 제안 65236에 대한 테스트를 추가함; Go 1.24 릴리스 노트 불필요
승인된 제안 https://go.dev/issue/67795 (https://go.dev/cl/616218 기반) - x/tools/go/ast/inspector의 iterator 지원; Go 1.24 릴리스 노트 불필요
승인된 제안 https://go.dev/issue/67812 (https://go.dev/cl/601497 기반) - x/net/http2.Server를 위한 설정 가능한 서버 핑(pings); Go 1.24 릴리스 노트 불필요
승인된 제안 https://go.dev/issue/68232 (https://go.dev/cl/595676 기반) - x/sys/unix 추가 사항; Go 1.24 릴리스 노트 불필요
승인된 제안 https://go.dev/issue/68898 (https://go.dev/cl/607495, https://go.dev/cl/620036, https://go.dev/cl/620135, https://go.dev/cl/623638 기반) - x/tools/go/gcexportdata가 2개 릴리스 + tip 지원 정책을 문서화하도록 하는 제안임; 변경 사항이 x/tools에 있으므로 Go 1.24 릴리스 노트 불필요
승인된 제안 https://go.dev/issue/69095 (https://go.dev/cl/593683, https://go.dev/cl/608955, https://go.dev/cl/610716 기반) - golang.org/x 저장소의 유지보수 및 지원에 영향을 주는 제안임; Go 1.24 릴리스 노트에 언급할 필요 없음
승인된 제안 https://go.dev/issue/68384 (https://go.dev/cl/611875 기반) - Go Telemetry의 범위를 Delve까지 확장하는 것은 Go 1.24와 직접적으로 연결되지 않으며 Go 1.24 릴리스 노트에 언급할 필요가 없어 보임
승인된 제안 https://go.dev/issue/69291 (https://go.dev/cl/610939 기반) - CL 610939는 x/tools의 코드를 리팩토링하며 x/tools/go/ssa/ssautil에 Reachable을 추가하려는 아직 열려 있는 제안 #69291을 언급함; Go 1.24 릴리스 노트 불필요
승인된 제안 https://go.dev/issue/69360 (https://go.dev/cl/614158, https://go.dev/cl/614159, https://go.dev/cl/614635, https://go.dev/cl/614675 기반) - 제안 69360은 x/tools에서 gorename을 태그 지정하고 삭제하는 것임; Go 1.24 릴리스 노트 불필요
승인된 제안 https://go.dev/issue/61417 (https://go.dev/cl/605955 기반) - x/oauth2의 새로운 필드; Go 1.24 릴리스 노트에 언급할 내용 없음
승인된 제안 https://go.dev/issue/29266 (https://go.dev/cl/632897 기반) - go.dev/doc/contribute를 위한 문서 전용 제안임; Go 1.24 릴리스 노트 불필요
-->
