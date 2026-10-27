<!--
참고: 이 문서 및 이 디렉터리의 다른 문서에서는
`hello` `world`와 같이 고정 폭 구문을 비고정 폭 공백으로 설정하는 것이 관례입니다.
이러한 구문에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

이 내용은 제공해주신 스타일 시트가 포함된 HTML/Markdown 조각이지만, 번역할 텍스트 본문이 포함되어 있지 않습니다. 번역이 필요한 내용을 제공해 주시면, 기술 번역 원칙에 따라 Markdown 구조와 코드를 보존하여 한국어로 번역해 드리겠습니다.

## Go 1.19 소개 {#introduction}

최신 Go 릴리스인 버전 1.19가 [Go 1.18](/doc/go1.18) 이후 5개월 만에 출시되었습니다.
대부분의 변경 사항은 툴체인, 런타임 및 라이브러리의 구현에 적용되었습니다.
언제나 그렇듯, 이번 릴리스에서도 Go 1 [호환성 약속](/doc/go1compat)을 유지합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 기대합니다.

## 언어 변경 사항 {#language}

<!-- https://go.dev/issue/52038 -->
언어 사양에는 단 한 가지의 작은 변경 사항이 있으며,
이는 [메서드 선언 내 타입 파라미터의 범위](/ref/spec#Declarations_and_scope)에 대한
[매우 작은 수정](/issue/52038)입니다.
기존 프로그램에는 영향을 주지 않습니다.

## 메모리 모델 {#mem}

<!-- https://go.dev/issue/50859 -->
[Go 메모리 모델](/ref/mem)이 C, C++, Java, JavaScript, Rust, Swift에서 사용하는 메모리 모델과 일치하도록 [수정되었습니다](https://research.swtch.com/gomm).
Go는 순차적 일관성(sequentially consistent)을 갖는 원자적 연산(atomics)만 제공하며, 다른 언어에서 볼 수 있는 더 완화된 형태의 모델은 제공하지 않습니다.
메모리 모델 업데이트와 함께, Go 1.19에서는 [atomic.Int64](/pkg/sync/atomic/#Int64) 및 [atomic.Pointer[T]](/pkg/sync/atomic/#Pointer)와 같이 원자적 값들을 더 쉽게 사용할 수 있게 해주는 [`sync/atomic` 패키지의 새로운 타입들](#atomic_types)을 도입했습니다.

## 포트 {#ports}

### LoongArch 64-bit {#loong64}

<!-- https://go.dev/issue/46229 -->
Go 1.19에서 Linux(`GOOS=linux`, `GOARCH=loong64`) 환경의 [LoongArch](https://loongson.github.io/LoongArch-Documentation) 64비트 아키텍처 지원이 추가되었습니다.
구현된 ABI는 LP64D입니다. 지원되는 최소 커널 버전은 5.19입니다.

대부분의 기존 LoongArch용 상용 Linux 배포판은 이전 버전의 커널을 사용하며, 역사적으로 호환되지 않는 시스템 콜 ABI를 가지고 있음에 유의하십시오. 정적으로 링크되었더라도, 컴파일된 바이너리는 이러한 시스템에서 작동하지 않습니다. 지원되지 않는 시스템의 사용자는 배포판에서 제공하는 Go 패키지로 사용이 제한됩니다.

### RISC-V {#riscv64}

<!-- CL 402374 -->
이제 `riscv64` 포트에서 레지스터를 사용하여 함수 인자와 결과값을 전달하는 것을 지원합니다. 벤치마크 결과 `riscv64`에서 일반적으로 10% 이상의 성능 향상이 나타났습니다.

## 도구 {#tools}

### Doc 코멘트 {#go-doc}

<!-- https://go.dev/issue/51082 -->
<!-- CL 384265, CL 397276, CL 397278, CL 397279, CL 397281, CL 397284 -->
Go 1.19에서는 문서 주석(doc comments) 내의 링크, 리스트 및 더 명확한 헤딩(headings)에 대한 지원이 추가되었습니다.
이 변경 사항의 일환으로, [`gofmt`](/cmd/gofmt)는 이제 렌더링된 의미를 더 명확하게 하기 위해 문서 주석의 형식을 다시 지정합니다.
구문 세부 사항과 이제 `gofmt`에서 강조 표시되는 일반적인 실수에 대한 설명은 “[Go Doc Comments](/doc/comment)”를 참조하십시오.
또한 이 변경 사항의 또 다른 부분으로, 새로운 패키지 [go/doc/comment](/pkg/go/doc/comment/)는 문서 주석의 파싱 및 리포맷팅뿐만 아니라 HTML, Markdown 및 텍스트로 렌더링하는 기능을 제공합니다.

### 새로운 `unix` 빌드 제약 조건 {#go-unix}

<!-- CL 389934 -->
<!-- https://go.dev/issue/20322 -->
<!-- https://go.dev/issue/51572 -->
이제 `//go:build` 라인에서 빌드 제약 조건인 `unix`가 인식됩니다. 타겟 운영체제(`GOOS`)가 Unix 또는 Unix 계열 시스템인 경우 이 제약 조건이 충족됩니다. 1.19 릴리스에서는 `GOOS`가 다음 중 하나일 때 충족됩니다:
`aix`, `android`, `darwin`,
`dragonfly`, `freebsd`, `hurd`,
`illumos`, `ios`, `linux`,
`netbsd`, `openbsd`, 또는 `solaris`.
향후 릴리스에서 `unix` 제약 조건은 새롭게 지원되는 추가 운영체제와 일치할 수 있습니다.

### Go 명령 {#go-command}

<!-- https://go.dev/issue/51461 -->

`-trimpath` 플래그가 설정된 경우, 이제 `go` `build`에 의해 Go 바이너리에 기록되는 빌드 설정에 포함되며, [`go` `version` `-m`](https://pkg.go.dev/cmd/go#hdr-Print_Go_version) 또는 [`debug.ReadBuildInfo`](https://pkg.go.dev/runtime/debug#ReadBuildInfo)를 사용하여 확인할 수 있습니다.

`go` `generate`는 이제 제너레이터의 환경에 `GOROOT` 환경 변수를 명시적으로 설정합니다. 이를 통해 제너레이터가 `-trimpath` 옵션으로 빌드되었더라도 올바른 `GOROOT`를 찾을 수 있습니다.

<!-- CL 404134 -->
이제 `go` `test`와 `go` `generate`는 서브프로세스에 사용되는 `PATH`의 시작 부분에 `GOROOT/bin`을 배치합니다. 따라서 `go` 명령어를 실행하는 테스트와 제너레이터가 동일한 `GOROOT`를 통해 해당 명령어를 찾게 됩니다.

<!-- CL 398058 -->
`go` `env`가 이제 `CGO_CFLAGS`, `CGO_CPPFLAGS`, `CGO_CXXFLAGS`, `CGO_FFLAGS`, `CGO_LDFLAGS` 및 `GOGCCFLAGS` 변수를 보고할 때, 공백이 포함된 항목에 따옴표를 붙입니다.

<!-- https://go.dev/issue/29666 -->
`go` `list` `-json`에서 이제 채울 JSON 필드의 쉼표 구분 목록을 허용합니다. 목록이 지정되면 JSON 출력에 해당 필드만 포함되며, `go` `list`는 포함되지 않은 필드를 계산하기 위한 작업을 생략할 수 있습니다. 일부 경우, 이로 인해 평소라면 보고되었을 오류가 억제될 수 있습니다.

<!-- CL 410821 -->
이제 `go` 명령어가 일부 모듈을 로드하는 데 필요한 정보를 캐싱하며, 이는 일부 `go` `list` 호출 속도의 향상으로 이어질 것입니다.

### Vet {#vet}

<!-- https://go.dev/issue/47528 -->
`vet` 검사기의 “errorsas”가 이제 흔한 실수인 `*error` 타입을 두 번째 인자로 하여 [`errors.As`](/pkg/errors/#As)를 호출하는 경우를 보고합니다.

## 런타임 {#runtime}

<!-- https://go.dev/issue/48409 -->
<!-- CL 397018 -->
이제 런타임에서 소프트 메모리 제한(soft memory limit)을 지원합니다. 이 메모리 제한에는 Go 힙과 런타임에서 관리하는 모든 기타 메모리가 포함되며, 바이너리 자체의 매핑, 다른 언어에서 관리하는 메모리, 운영 체제가 Go 프로그램을 대신하여 보유한 메모리와 같은 외부 메모리 소스는 제외됩니다. 이 제한은 [`runtime/debug.SetMemoryLimit`](/pkg/runtime/debug/#SetMemoryLimit) 또는 이와 동일한 [`GOMEMLIMIT`](/pkg/runtime/#hdr-Environment_Variables) 환경 변수를 통해 관리할 수 있습니다. 이 제한은 [`runtime/debug.SetGCPercent`](/pkg/runtime/debug/#SetGCPercent) / [`GOGC`](/pkg/runtime/#hdr-Environment_Variables)와 함께 작동하며, `GOGC=off`인 경우에도 준수됩니다. 이를 통해 Go 프로그램이 항상 메모리 제한을 최대한 활용할 수 있게 하여 일부 사례에서 리소스 효율성을 향상시킵니다. 소프트 메모리 제한에 대한 더 자세한 설명과 다양한 일반적인 사용 사례 및 시나리오는 [GC 가이드](/doc/gc-guide)를 참조하십시오. 수십 메가바이트 이하의 작은 메모리 제한은 OS 스케줄링과 같은 외부 지연 요인으로 인해 준수되지 않을 가능성이 높다는 점에 유의하십시오. 자세한 내용은 [issue 52433](/issue/52433)을 참조하십시오. 수백 메가바이트 이상의 더 큰 메모리 제한은 안정적이며 프로덕션 환경에서 사용할 준비가 되어 있습니다.

<!-- CL 353989 -->
프로그램의 live heap 크기가 soft memory limit에 도달할 때 발생하는 GC thrashing의 영향을 제한하기 위해, Go 런타임은 유휴 시간(idle time)을 제외한 전체 GC CPU 사용률을 50%로 제한하려고 시도합니다. 이는 애플리케이션의 진행을 막는 것보다 메모리를 더 사용하는 쪽을 선택하는 것입니다. 실제로 이 제한은 예외적인 경우에만 작용할 것으로 예상되며, 새로운 [runtime metric](/pkg/runtime/metrics/#hdr-Supported_metrics)인 `/gc/limiter/last-enabled:gc-cycle`을 통해 이 현상이 마지막으로 발생한 시점을 보고합니다.

<!-- https://go.dev/issue/44163 -->
이제 런타임은 애플리케이션이 주기적인 GC 사이클을 강제할 만큼 충분히 유휴 상태일 때, 유휴 운영 체제 스레드에 훨씬 더 적은 수의 GC 워커 고루틴(worker goroutines)을 스케줄링합니다.

<!-- https://go.dev/issue/18138 -->
<!-- CL 345889 -->
이제 런타임은 고루틴의 과거 평균 스택 사용량을 기반으로 초기 고루틴 스택을 할당합니다. 이를 통해 평균적인 경우에 필요한 초기 스택 성장 및 복사 작업을 일부 방지할 수 있으며, 그 대신 평균 미만의 고루틴에 대해 최대 2배의 공간 낭비가 발생할 수 있습니다.

<!-- https://go.dev/issue/46279 -->
<!-- CL 393354 -->
<!-- CL 392415 -->
Unix 운영 체제에서 [os](/pkg/os/) 패키지를 임포트하는 Go 프로그램은 이제 열린 파일 제한(`RLIMIT_NOFILE`)을 자동으로 허용된 최대값으로 증가시킵니다. 즉, 소프트 제한(soft limit)을 하드 제한(hard limit)과 일치하도록 변경합니다.

이는 [_select_](https://en.wikipedia.org/wiki/Select_(Unix)) 시스템 호출을 사용하는 매우 오래된 C 프로그램과의 호환성을 위해 일부 시스템에서 인위적으로 낮게 설정된 제한을 수정하기 위함입니다. Go 프로그램은 이러한 제한으로 인한 이점이 없으며, 오히려 `gofmt`와 같은 간단한 프로그램조차 많은 파일을 병렬로 처리할 때 해당 시스템에서 파일 서술자(file descriptor)가 부족해지는 경우가 빈번했습니다.

이 변경 사항으로 인해, 자식 프로세스로 매우 오래된 C 프로그램을 실행하는 Go 프로그램의 경우 해당 프로그램이 너무 높은 제한 값으로 실행될 수 있습니다. 이는 Go 프로그램을 실행하기 전에 하드 제한을 설정함으로써 수정할 수 있습니다.

<!-- https://go.dev/issue/51485 -->
<!-- CL 390421 -->
복구 불가능한 치명적 오류(concurrent map writes 또는 unlock 상태인 mutex의 unlock 등)는 이제 `GOTRACEBACK=system` 또는 `crash`가 아닌 한, 런타임 메타데이터를 제외한 더 단순한 traceback(fatal panic과 동일)을 출력합니다. 런타임 내부의 치명적 오류 traceback은 `GOTRACEBACK` 값에 관계없이 항상 전체 메타데이터를 포함합니다.

<!-- https://go.dev/issue/50614 -->
<!-- CL 395754 -->
ARM64에서 디버거 주입 함수 호출(debugger-injected function calls) 기능이 추가되었습니다. 이를 통해 사용자는 해당 기능을 사용하도록 업데이트된 디버거를 사용하여 대화형 디버깅 세션 중에 바이너리의 함수를 호출할 수 있습니다.

<!-- https://go.dev/issue/44853 -->
[Go 1.18에서 추가된 주소 sanitizer 지원](/doc/go1.18#go-build-asan)이
이제 함수 인자와 전역 변수를 더 정밀하게 처리합니다.

## 컴파일러 {#compiler}

<!-- https://go.dev/issue/5496 -->
<!-- CL 357330, 395714, 403979 -->
이제 컴파일러가 큰 정수 및 문자열 switch 문을 구현하기 위해 [jump table](https://en.wikipedia.org/wiki/Branch_table)을 사용합니다.
switch 문의 성능 향상 정도는 다양하지만, 약 20% 정도 빨라질 수 있습니다.
(`GOARCH=amd64` 및 `GOARCH=arm64`에서만 적용)

<!-- CL 391014 -->
이제 Go 컴파일러는 링크 가능한 오브젝트 파일을 빌드하기 위해 `-p=importpath` 플래그를 요구합니다. 이 플래그는 이미 `go` 명령어와 Bazel에 의해 제공되고 있습니다. Go 컴파일러를 직접 호출하는 다른 빌드 시스템이 있다면, 해당 플래그를 함께 전달하도록 수정해야 합니다.

<!-- CL 415235 -->
Go 컴파일러는 더 이상 `-importmap` 플래그를 허용하지 않습니다. Go 컴파일러를 직접 호출하는 빌드 시스템은 대신 `-importcfg` 플래그를 사용해야 합니다.

## Assembler {#assembler}

<!-- CL 404298 -->
컴파일러와 마찬가지로, 이제 어셈블러에서도 링크 가능한 오브젝트 파일을 빌드하려면 `-p=importpath` 플래그가 필요합니다.
이 플래그는 이미 `go` 명령어를 통해 제공됩니다. Go 어셈블러를 직접 호출하는 다른 빌드 시스템을 사용하는 경우, 해당 플래그를 반드시 전달하도록 설정해야 합니다.

## Linker {#linker}

<!-- https://go.dev/issue/50796, CL 380755 -->
ELF 플랫폼에서 링커가 이제 레거시 `.zdebug` 형식 대신 표준 gABI 형식(`SHF_COMPRESSED`)으로 압축된 DWARF 섹션을 생성합니다.

## 표준 라이브러리 {#library}

### 새로운 원자적 타입 (atomic types) {#atomic_types}

<!-- https://go.dev/issue/50860 -->
<!-- CL 381317 -->
[`sync/atomic`](/pkg/sync/atomic/) 패키지는 새로운 원자적 타입인
[`Bool`](/pkg/sync/atomic/#Bool),
[`Int32`](/pkg/sync/atomic/#Int32),
[`Int64`](/pkg/sync/atomic/#Int64),
[`Uint32`](/pkg/sync/atomic/#Uint32),
[`Uint64`](/pkg/sync/atomic/#Uint64),
[`Uintptr`](/pkg/sync/atomic/#Uintptr), 그리고
[`Pointer`](/pkg/sync/atomic/#Pointer)를 정의합니다.
이 타입들은 기저 값을 숨김으로써 모든 접근이 원자적 API를 사용하도록 강제합니다.
[`Pointer`](/pkg/sync/atomic/#Pointer)는 호출부에서
[`unsafe.Pointer`](/pkg/unsafe/#Pointer)로 변환해야 하는 필요성을 없애줍니다.
[`Int64`](/pkg/sync/atomic/#Int64)와
[`Uint64`](/pkg/sync/atomic/#Uint64)는 32비트 시스템에서도 구조체와 할당된 데이터 내에서
자동으로 64비트 경계에 맞춰 정렬됩니다.

### PATH 조회 {#os-exec-path}

<!-- https://go.dev/issue/43724 -->
<!-- CL 381374 -->
<!-- CL 403274 -->
[`Command`](/pkg/os/exec/#Command) 및
[`LookPath`](/pkg/os/exec/#LookPath)는 더 이상
PATH 검색 결과가 현재 디렉토리를 기준으로 발견되는 것을 허용하지 않습니다.
이는 [일반적인 보안 문제의 원인](/blog/path-security)을 제거하지만,
현재 디렉토리에 있는 `prog`라는 이름의 바이너리(Windows의 경우 `prog.exe`)를 실행하기 위해
`exec.Command("prog")`를 사용하는 등의 방식에 의존하는 기존 프로그램들은 작동하지 않을 수 있습니다.
이러한 프로그램들을 업데이트하는 가장 좋은 방법에 대한 정보는 [`os/exec`](/pkg/os/exec/) 패키지 문서를 참조하십시오.

<!-- https://go.dev/issue/43947 -->
Windows에서 `Command`와 `LookPath`가 이제 [`NoDefaultCurrentDirectoryInExePath`](https://docs.microsoft.com/en-us/windows/win32/api/processenv/nf-processenv-needcurrentdirectoryforexepatha) 환경 변수를 준수합니다. 이를 통해 Windows 시스템의 PATH 조회 시 기본적으로 수행되는 “`.`” (현재 디렉토리)에 대한 암시적 검색을 비활성화할 수 있습니다.

### 라이브러리의 소규모 변경 사항 {#minor_library_changes}

언제나 그렇듯이, Go 1의 [호환성 약속](/doc/go1compat)을 염두에 두고 라이브러리에 여러 가지 사소한 변경 사항과 업데이트가 적용되었습니다.
또한, 여기에는 모두 나열하지 않았으나 다양한 성능 개선이 이루어졌습니다.

#### [archive/zip](/pkg/archive/zip/)

<!-- CL 387976 -->
[`Reader`](/pkg/archive/zip/#Reader)는
이제 ZIP 파일 시작 부분의 non-ZIP 데이터를 무시하며, 이는 대부분의 다른 구현체와 일치하는 동작입니다.
이 변경 사항은 다른 용도 외에도 일부 Java JAR 파일을 읽기 위해 필요합니다.

<!-- archive/zip -->

#### [crypto/elliptic](/pkg/crypto/elliptic/)

<!-- CL 382995 -->
`IsOnCurve` 메서드가 false를 반환하고, `Unmarshal`이나 유효한 포인트에 작동하는 `Curve` 메서드에 의해 절대 반환되지 않는 유효하지 않은 커브 포인트(invalid curve points)를 사용하는 것은 항상 정의되지 않은 동작(undefined behavior)이었으며, 이는 키 복구 공격(key recovery attacks)으로 이어질 수 있습니다. 이제 [`Marshal`](/pkg/crypto/elliptic/#Marshal), [`MarshalCompressed`](/pkg/crypto/elliptic/#MarshalCompressed), [`Add`](/pkg/crypto/elliptic/#Curve.Add), [`Double`](/pkg/crypto/elliptic/#Curve.Double), 또는 [`ScalarMult`](/pkg/crypto/elliptic/#Curve.ScalarMult)에 유효하지 않은 포인트가 전달되면 패닉(panic)이 발생합니다.

<!-- golang.org/issue/52182 -->
`P224`, `P384`, `P521` 곡선에서의 `ScalarBaseMult` 연산 속도가 최대 3배까지 향상되었으며, 이에 따라 일부 ECDSA 연산에서도 유사한 속도 향상이 이루어졌습니다. 제네릭(플랫폼 최적화되지 않은) `P256` 구현이 정형 검증된(formally verified) 모델에서 파생된 구현으로 교체되었습니다. 이로 인해 32비트 플랫폼에서는 성능이 크게 저하될 수 있습니다.

<!-- crypto/elliptic -->

#### [crypto/rand](/pkg/crypto/rand/)

<!-- CL 370894 -->
<!-- CL 390038 -->
[`Read`](/pkg/crypto/rand/#Read)는 더 이상 호출 사이에 운영 체제로부터 얻은 랜덤 데이터를 버퍼링하지 않습니다. 높은 빈도로 많은 작은 읽기 작업을 수행하는 애플리케이션은 성능상의 이유로 [`Reader`](/pkg/crypto/rand/#Reader)를 [`bufio.Reader`](/pkg/bufio/#Reader)로 감싸서 사용할 수 있으며, 이때 부분 읽기가 발생하지 않도록 [`io.ReadFull`](/pkg/io/#ReadFull)을 사용해야 합니다.

<!-- CL 375215 -->
Plan 9에서 `Read`가 재구현되었으며, ANSI X9.31 알고리즘이 빠른 키 소거 생성기(fast key erasure generator)로 대체되었습니다.

<!-- CL 391554 -->
<!-- CL 387554 -->
[`Prime`](/pkg/crypto/rand/#Prime) 구현이 거절 샘플링(rejection sampling)만 사용하도록 변경되었습니다. 이를 통해 비암호학적 컨텍스트에서 작은 소수를 생성할 때의 편향(bias)을 제거하고, 발생 가능한 사소한 타이밍 누수(timing leak)를 제거하며, 구현을 단순화하는 동시에 BoringSSL과의 동작 일관성을 높였습니다.

이 변경으로 인해 동일한 랜덤 소스 스트림에 대해 이전 구현과 다른 결과값이 생성됩니다. 이로 인해 특정 결정론적 랜덤 소스로부터 특정 결과가 나올 것을 기대하고 작성된 테스트가 실패할 수 있습니다. 향후 이러한 문제를 방지하기 위해, 이제 구현 단계에서 입력 스트림에 대해 의도적으로 비결정론적(non-deterministic)으로 동작하도록 설정되었습니다.

<!-- crypto/rand -->

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 400974 -->
<!-- https://go.dev/issue/45428 -->
`GODEBUG` 옵션 `tls10default=1`이 제거되었습니다. [`Config.MinVersion`](/pkg/crypto/tls/#Config.MinVersion)을 설정하여 클라이언트 측에서 TLS 1.0을 여전히 활성화할 수 있습니다.

<!-- CL 384894 -->
이제 TLS 서버와 클라이언트는 RFC 5246, Section 7.4.1.4 및 RFC 8446, Section 4.2의 요구 사항에 따라 TLS 핸드셰이크에서 중복된 확장을 거부합니다.

<!-- crypto/tls -->

#### [crypto/x509](/pkg/crypto/x509/)

<!-- CL 285872 -->
[`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate)는
더 이상 `SignatureAlgorithm`이 `MD5WithRSA`로 설정된 인증서 생성을 지원하지 않습니다.

<!-- CL 400494 -->
`CreateCertificate`가 더 이상 음수 시리얼 번호를 허용하지 않습니다.

<!-- CL 399827 -->
생성된 인증서에 확장(extensions)이 없는 경우, `CreateCertificate`가 더 이상 빈 SEQUENCE를 출력하지 않습니다.

<!-- CL 396774 -->
원래 Go 1.19에서 계획되었던 `GODEBUG` 옵션 `x509sha1=1`의 제거가 향후 릴리스로 연기되었습니다.
해당 옵션을 사용하는 애플리케이션은 마이그레이션을 진행해야 합니다. SHA-1에 대한 실질적인 공격은 2017년부터 입증되었으며, 공개적으로 신뢰받는 인증 기관(Certificate Authorities)은 2015년부터 SHA-1 인증서를 발급하지 않았습니다.

<!-- CL 383215 -->
[`ParseCertificate`](/pkg/crypto/x509/#ParseCertificate)
및 [`ParseCertificateRequest`](/pkg/crypto/x509/#ParseCertificateRequest)
가 이제 중복된 확장(extensions)을 포함하는 인증서 및 CSR을 거부합니다.

새로운 [`CertPool.Clone`](/pkg/crypto/x509/#CertPool.Clone) 및 [`CertPool.Equal`](/pkg/crypto/x509/#CertPool.Equal) 메서드를 통해 각각 `CertPool`을 복제하고 두 `CertPool`의 동일 여부를 확인할 수 있습니다.

<!-- https://go.dev/issue/50674 -->
<!-- CL 390834 -->
새로운 [`ParseRevocationList`](/pkg/crypto/x509/#ParseRevocationList) 함수는 [`RevocationList`](/pkg/crypto/x509/#RevocationList)를 반환하며, 더 빠르고 안전하게 사용할 수 있는 CRL 파서를 제공합니다.
CRL을 파싱하면 `CreateRevocationList`에서는 무시되었던 `RevocationList`의 새로운 필드인 `RawIssuer`, `Signature`, `AuthorityKeyId`, 및 `Extensions` 값들도 함께 채워집니다.

새로운 메서드 [`RevocationList.CheckSignatureFrom`](/pkg/crypto/x509/#RevocationList.CheckSignatureFrom)은 CRL의 서명이 [`Certificate`](/pkg/crypto/x509/#Certificate)로부터 생성된 유효한 서명인지 확인합니다.

[`ParseCRL`](/pkg/crypto/x509/#ParseCRL) 및 [`ParseDERCRL`](/pkg/crypto/x509/#ParseDERCRL) 함수는 이제 `ParseRevocationList`로 대체되어 deprecated 되었습니다.
[`Certificate.CheckCRLSignature`](/pkg/crypto/x509/#Certificate.CheckCRLSignature) 메서드는 `RevocationList.CheckSignatureFrom`으로 대체되어 deprecated 되었습니다.

<!-- CL 389555, CL 401115, CL 403554 -->
[`Certificate.Verify`](/pkg/crypto/x509/#Certificate.Verify)의 경로 빌더(path builder)가 전면 개편되어, 이제 더 나은 체인을 생성하거나 복잡한 시나리오에서 더 효율적으로 동작합니다.
이름 제약 조건(Name constraints)이 이제 리프(leaf) 인증서가 아닌 인증서에도 적용됩니다.

<!-- crypto/x509 -->

#### [crypto/x509/pkix](/pkg/crypto/x509/pkix/)

<!-- CL 390834 -->
[`CertificateList`](/pkg/crypto/x509/pkix/#CertificateList) 및
[`TBSCertificateList`](/pkg/crypto/x509/pkix/#TBSCertificateList)
타입은 더 이상 사용되지 않습니다(deprecated). 대신 새로운 [`crypto/x509` CRL 기능](#crypto/x509)을 사용해야 합니다.

<!-- crypto/x509/pkix -->

#### [debug/elf](/pkg/debug/elf/)

<!-- CL 396735 -->
새로운 `EM_LOONGARCH` 및 `R_LARCH_*` 상수는 loong64 포트를 지원합니다.

<!-- debug/elf -->

#### [debug/pe](/pkg/debug/pe/)

<!-- https://go.dev/issue/51868 -->
<!-- CL 394534 -->
[`COFFSymbolAuxFormat5`](/pkg/debug/pe/#COFFSymbolAuxFormat5)를 반환하는 새로운 [`File.COFFSymbolReadSectionDefAux`](/pkg/debug/pe/#File.COFFSymbolReadSectionDefAux) 메서드는 PE 파일 섹션의 COMDAT 정보에 대한 접근을 제공합니다.
이는 새로운 `IMAGE_COMDAT_*` 및 `IMAGE_SCN_*` 상수에 의해 지원됩니다.

<!-- debug/pe -->

#### [encoding/binary](/pkg/encoding/binary/)

새로운 인터페이스인
[`AppendByteOrder`](/pkg/encoding/binary/#AppendByteOrder)는 `uint16`, `uint32` 또는 `uint64`를
바이트 슬라이스에 추가하기 위한 효율적인 메서드를 제공합니다.
이제 [`BigEndian`](/pkg/encoding/binary/#BigEndian)과
[`LittleEndian`](/pkg/encoding/binary/#LittleEndian)이 이 인터페이스를 구현합니다.

<!-- https://go.dev/issue/51644 -->
<!-- CL 400176 -->
마찬가지로, 새로운 함수인 [`AppendUvarint`](/pkg/encoding/binary/#AppendUvarint)와 [`AppendVarint`](/pkg/encoding/binary/#AppendVarint)는 [`PutUvarint`](/pkg/encoding/binary/#PutUvarint) 및 [`PutVarint`](/pkg/encoding/binary/#PutVarint)의 효율적인 추가(appending) 버전입니다.

<!-- encoding/binary -->

#### [encoding/csv](/pkg/encoding/csv/)

새로운 메서드 [`Reader.InputOffset`](/pkg/encoding/csv/#Reader.InputOffset)은 `encoding/json`의 [`Decoder.InputOffset`](/pkg/encoding/json/#Decoder.InputOffset)과 유사하게, 리더의 현재 입력 위치를 바이트 오프셋으로 보고합니다.

<!-- encoding/csv -->

#### [encoding/xml](/pkg/encoding/xml/)

새로운 메서드
[`Decoder.InputPos`](/pkg/encoding/xml/#Decoder.InputPos)는
`encoding/csv`의
[`Decoder.FieldPos`](/pkg/encoding/csv/#Decoder.FieldPos)와 유사하게
리더의 현재 입력 위치를 행과 열로 보고합니다.

<!-- encoding/xml -->

#### [flag](/pkg/flag/)

<!-- https://go.dev/issue/45754 -->
<!-- CL 313329 -->
새로운 함수 [`TextVar`](/pkg/flag/#TextVar)는 [`encoding.TextUnmarshaler`](/pkg/encoding/#TextUnmarshaler)를 구현하는 값을 가진 플래그를 정의하며, 이를 통해 커맨드라인 플래그 변수가 [`big.Int`](/pkg/math/big/#Int), [`netip.Addr`](/pkg/net/netip/#Addr), [`time.Time`](/pkg/time/#Time)과 같은 타입을 가질 수 있게 합니다.

제공해주신 콘텐츠가 없습니다. 번역할 Markdown 내용을 입력해 주세요.

#### [fmt](/pkg/fmt/)

<!-- https://go.dev/issue/47579 -->
<!-- CL 406177 -->
새로운 함수인
[`Append`](/pkg/fmt/#Append),
[`Appendf`](/pkg/fmt/#Appendf), 그리고
[`Appendln`](/pkg/fmt/#Appendln)은
포맷팅된 데이터를 바이트 슬라이스(byte slice)에 추가합니다.

<!-- fmt -->

#### [go/parser](/pkg/go/parser/)

<!-- CL 403696 -->
이제 파서가 `~x`를 [token.TILDE](/pkg/go/token/#TILDE) 연산자를 가진 단항 식(unary expression)으로 인식하여, `~int`와 같은 타입 제약(type constraint)이 잘못된 문맥에서 사용되었을 때 더 나은 오류 복구가 가능해졌습니다.

<!-- go/parser -->

#### [go/types](/pkg/go/types/)

<!-- https://go.dev/issue/51682 -->
<!-- CL 395535 -->
새로운 메서드 [`Func.Origin`](/pkg/go/types/#Func.Origin)
및 [`Var.Origin`](/pkg/go/types/#Var.Origin)은 타입 인스턴스화 중에 생성된
합성 [`Func`](/pkg/go/types/#Func) 및 [`Var`](/pkg/go/types/#Var) 객체에 대해
제네릭 타입의 해당 [`Object`](/pkg/go/types/#Object)를 반환합니다.

<!-- https://go.dev/issue/52728 -->
<!-- CL 404885 -->
이제 [`Named`](/pkg/go/types/#Named) 타입 인스턴스화에 대해 [`Named.Underlying`](/pkg/go/types/#Named.Underlying) 또는 [`Named.Method`](/pkg/go/types/#Named.Method)를 재귀적으로 호출하여 서로 다르지만 동일한 타입 인스턴스를 무한히 생성하는 것이 불가능합니다.

<!-- go/types -->

#### [hash/maphash](/pkg/hash/maphash/)

<!-- https://go.dev/issue/42710 -->
<!-- CL 392494 -->
새로운 함수인
[`Bytes`](/pkg/hash/maphash/#Bytes)
와
[`String`](/pkg/hash/maphash/#String)
은 단일 바이트 슬라이스나 문자열을 해싱하는 효율적인 방법을 제공합니다.
이 함수들은 단일 write를 사용하는 더 일반적인
[`Hash`](/pkg/hash/maphash/#Hash)
와 동일하지만, 입력값이 작은 경우의 설정 오버헤드를 피할 수 있습니다.

<!-- hash/maphash -->

#### [html/template](/pkg/html/template/)

<!-- https://go.dev/issue/46121 -->
<!-- CL 389156 -->
[`FuncMap`](/pkg/html/template/#FuncMap) 타입이 이제 자체 이름이 지정된 타입 대신 `text/template`의 [`FuncMap`](/pkg/text/template/#FuncMap)에 대한 별칭(alias)이 되었습니다.
이를 통해 두 설정 중 어느 쪽의 `FuncMap`에서도 동작하는 코드를 작성할 수 있습니다.

<!-- https://go.dev/issue/59153 -->
<!-- CL 481987 -->
Go 1.19.8 및 이후 버전
[ECMAScript 6 템플릿 리터럴 내의 액션을 허용하지 않습니다.](/pkg/html/template#hdr-Security_Model)
이 동작은 `GODEBUG=jstmpllitinterp=1` 설정을 통해 되돌릴 수 있습니다.

<!-- html/template -->

#### [image/draw](/pkg/image/draw/)

<!-- CL 396795 -->
대상 이미지와 소스 이미지가 모두 [`image.NRGBA`](/pkg/image/#NRGBA)이거나 모두 [`image.NRGBA64`](/pkg/image/#NRGBA64)일 때, [`Src`](/pkg/image/draw/#Src) 연산자를 사용한 [`Draw`](/pkg/image/draw/#Draw)는 비-프리멀티플라이드-알파(non-premultiplied-alpha) 색상을 보존합니다.
이는 Go 1.18 라이브러리 최적화 과정에서 실수로 도입된 동작 변경 사항을 되돌리는 것이며, 이제 코드는 Go 1.17 및 그 이전 버전의 동작과 일치합니다.

<!-- image/draw -->

#### [io](/pkg/io/)

<!-- https://go.dev/issue/51566 -->
<!-- CL 400236 -->
이제 [`NopCloser`](/pkg/io/#NopCloser)의 입력값이 [`WriterTo`](/pkg/io/#WriterTo)를 구현하는 경우, 그 결과값 또한 이를 구현합니다.

<!-- https://go.dev/issue/50842 -->
[`MultiReader`](/pkg/io/#MultiReader)의 결과가 이제 무조건 [`WriterTo`](/pkg/io/#WriterTo)를 구현합니다.
기저 리더 중 `WriterTo`를 구현하지 않는 것이 있다면, 적절하게 시뮬레이션됩니다.

<!-- io -->

#### [mime](/pkg/mime/)

<!-- CL 406894 -->
Windows에서만, `mime` 패키지가 확장자 `.js`가 MIME 타입 `text/plain`을 가져야 한다는 레지스트리 항목을 이제 무시합니다. 이는 Windows 시스템에서 흔히 발생하는 의도치 않은 잘못된 설정입니다. 이 변경으로 인해 `.js`는 기본 MIME 타입인 `text/javascript; charset=utf-8`을 갖게 됩니다. Windows에서 `text/plain`을 기대하는 애플리케이션은 이제 [`AddExtensionType`](/pkg/mime/#AddExtensionType)을 명시적으로 호출해야 합니다.

제공해주신 내용이 비어 있습니다. 번역할 Markdown 콘텐츠를 제공해 주시면, 요청하신 지침에 따라 기술적으로 정확하게 한국어로 번역해 드리겠습니다.

#### [mime/multipart](/pkg/mime/multipart)

<!-- https://go.dev/issue/59153 -->
<!-- CL 481985 -->
Go 1.19.8 이후 버전부터, 이 패키지는 악의적인 입력으로부터 보호하기 위해 처리하는 MIME 데이터의 크기에 제한을 둡니다.
`Reader.NextPart` 및 `Reader.NextRawPart`는 파트당 헤더 수를 10,000개로 제한하며, `Reader.ReadForm`은 모든 `FileHeaders`의 총 헤더 수를 10,000개로 제한합니다.
이 제한은 `GODEBUG=multipartmaxheaders` 설정을 통해 조정할 수 있습니다.
`Reader.ReadForm`은 추가적으로 폼 내의 파트 수를 1,000개로 제한합니다.
이 제한은 `GODEBUG=multipartmaxparts` 설정을 통해 조정할 수 있습니다.

제공해주신 입력 내용이 비어 있거나 주석(`<!-- mime/multipart -->`)만 포함되어 있습니다. 번역할 영문 Markdown 내용을 제공해 주시면, 요청하신 지침에 따라 정확하게 한국어로 번역해 드리겠습니다.

#### [net](/pkg/net/)

<!-- CL 386016 -->
이제 pure Go 리졸버는 EDNS(0)를 사용하여 권장 최대 응답 패킷 길이를 포함하며, 응답 패킷이 최대 1232바이트까지 포함될 수 있도록 허용합니다 (이전 최대값은 512였습니다).
그럴 가능성은 낮지만, 이로 인해 로컬 DNS 리졸버에 문제가 발생하는 경우, 환경 변수 `GODEBUG=netdns=cgo`를 설정하여 cgo 기반 리졸버를 사용하면 해결될 것입니다.
이러한 문제가 발생하면 [이슈 트래커](/issue/new)에 보고해 주세요.

<!-- https://go.dev/issue/51428 -->
<!-- CL 396877 -->
`net` 패키지의 함수나 메서드가 "I/O timeout" 에러를 반환할 때, 이제 해당 에러는 `errors.Is(err, context.DeadlineExceeded)`를 만족합니다. `net` 패키지의 함수가 "operation was canceled" 에러를 반환할 때, 이제 해당 에러는 `errors.Is(err, context.Canceled)`를 만족합니다.

이러한 변경 사항은 에러 메시지에 대한 하위 호환성을 유지하면서, 컨텍스트 취소(cancellation)나 타임아웃으로 인해 `net` 패키지의 함수나 메서드가 에러를 반환하는 경우를 코드로 더 쉽게 테스트할 수 있도록 하기 위함입니다.

<!-- https://go.dev/issue/33097 -->
<!-- CL 400654 -->
[`Resolver.PreferGo`](/pkg/net/#Resolver.PreferGo)가 이제 Windows와 Plan 9에서도 구현되었습니다. 이전에는 Unix 플랫폼에서만 작동했습니다. [`Dialer.Resolver`](/pkg/net/#Dialer.Resolver) 및 [`Resolver.Dial`](/pkg/net/#Resolver.Dial)과 결합하여, 이제 이식 가능한 프로그램을 작성하고 다이얼링 시 모든 DNS 이름 조회(lookup)를 제어할 수 있습니다.

`net` 패키지는 이제 Windows에서 `netgo` 빌드 태그에 대한 초기 지원을 제공합니다. 이 태그를 사용하면 패키지는 Windows에 DNS 결과를 요청하는 대신 Go DNS 클라이언트(`Resolver.PreferGo`에서 사용됨)를 사용합니다. 다만, 복잡한 시스템 네트워크 설정의 경우 Windows에서 검색한 업스트림 DNS 서버가 아직 정확하지 않을 수 있습니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- CL 269997 -->
[`ResponseWriter.WriteHeader`](/pkg/net/http/#ResponseWriter)가
이제 사용자 정의 1xx 정보(informational) 헤더 전송을 지원합니다.

<!-- CL 361397 -->
[`MaxBytesReader`](/pkg/net/http/#MaxBytesReader)가 반환하는 `io.ReadCloser`는 이제 읽기 제한을 초과했을 때 정의된 에러 타입인 [`MaxBytesError`](/pkg/net/http/#MaxBytesError)를 반환합니다.

<!-- CL 375354 -->
HTTP 클라이언트는 `Location` 헤더가 없는 3xx 응답을 에러로 처리하는 대신, 호출자에게 반환하여 처리하도록 합니다.

<!-- net/http -->

#### [net/url](/pkg/net/url/)

<!-- CL 374654 -->
새로운
[`JoinPath`](/pkg/net/url/#JoinPath)
함수와
[`URL.JoinPath`](/pkg/net/url/#URL.JoinPath)
메서드는 경로 요소 목록을 결합하여 새로운 `URL`을 생성합니다.

<!-- https://go.dev/issue/46059 -->
이제 `URL` 타입은 authority가 없는 URL과 authority가 비어 있는 URL을 구분합니다. 예를 들어, `http:///path`는 비어 있는 authority(호스트)를 가지며, `http:/path`는 authority가 없습니다.

새로운 [`URL`](/pkg/net/url/#URL) 필드
`OmitHost`는 `URL`의 authority가 비어 있을 때 `true`로 설정됩니다.

<!-- net/url -->

#### [os/exec](/pkg/os/exec/)

<!-- https://go.dev/issue/50599 -->
<!-- CL 401340 -->
`Dir` 필드가 비어 있지 않고 `Env`가 nil인 [`Cmd`](/pkg/os/exec/#Cmd)는 이제 하위 프로세스의 `PWD` 환경 변수를 `Dir`과 일치하도록 암시적으로 설정합니다.

새로운 메서드 [`Cmd.Environ`](/pkg/os/exec/#Cmd.Environ)은 암시적으로 설정된 `PWD` 변수를 포함하여, 명령어를 실행하는 데 사용될 환경 변수를 보고합니다.

<!-- os/exec -->

#### [reflect](/pkg/reflect/)

<!-- https://go.dev/issue/47066 -->
<!-- CL 357331 -->
[`Value.Bytes`](/pkg/reflect/#Value.Bytes) 메서드가 이제 슬라이스뿐만 아니라 주소 지정 가능한(addressable) 배열도 허용합니다.

<!-- CL 400954 -->
이제 [`Value.Len`](/pkg/reflect/#Value.Len) 및 [`Value.Cap`](/pkg/reflect/#Value.Cap) 메서드가 배열 포인터에 대해서도 성공적으로 동작하여 해당 배열의 길이를 반환합니다. 이는 [내장 `len` 및 `cap` 함수가 동작하는 방식](/ref/spec#Length_and_capacity)과 일치시키기 위함입니다.

<!-- reflect -->

#### [regexp/syntax](/pkg/regexp/syntax/)

<!-- https://go.dev/issue/51684 -->
<!-- CL 401076 -->
Go 1.18 release candidate 1, Go 1.17.8, 그리고 Go 1.16.15에는 매우 깊게 중첩된 표현식을 거부하도록 하는 정규 표현식 파서의 보안 수정 사항이 포함되었습니다.
Go의 패치 릴리스는 새로운 API를 도입하지 않기 때문에, 이 경우 파서는 [`syntax.ErrInternalError`](/pkg/regexp/syntax/#ErrInternalError)를 반환했습니다.
Go 1.19에서는 더 구체적인 오류인 [`syntax.ErrNestingDepth`](/pkg/regexp/syntax/#ErrNestingDepth)를 추가했으며, 이제 파서는 대신 이 오류를 반환합니다.

<!-- regexp -->

#### [runtime](/pkg/runtime/)

<!-- https://go.dev/issue/51461 -->
이제 [`GOROOT`](/pkg/runtime/#GOROOT) 함수는 `-trimpath` 플래그를 설정하여 바이너리를 빌드하고 프로세스 환경에 `GOROOT` 변수가 설정되지 않은 경우, (`"go"` 대신) 빈 문자열을 반환합니다.

<!-- 런타임 -->

#### [runtime/metrics](/pkg/runtime/metrics/)

<!-- https://go.dev/issue/47216 -->
<!-- CL 404305 -->
새로운 `/sched/gomaxprocs:threads` [metric](/pkg/runtime/metrics/#hdr-Supported_metrics)은 현재의 [`runtime.GOMAXPROCS`](/pkg/runtime/#GOMAXPROCS) 값을 보고합니다.

<!-- https://go.dev/issue/47216 -->
<!-- CL 404306 -->
새로운 `/cgo/go-to-c-calls:calls`
[메트릭](/pkg/runtime/metrics/#hdr-Supported_metrics)은 Go에서 C로 이루어진 총 호출 횟수를 보고합니다. 이 메트릭은
[`runtime.NumCgoCall`](/pkg/runtime/#NumCgoCall)
함수와 동일합니다.

<!-- https://go.dev/issue/48409 -->
<!-- CL 403614 -->
새로운 `/gc/limiter/last-enabled:gc-cycle`
[metric](/pkg/runtime/metrics/#hdr-Supported_metrics)은 GC CPU limiter가 활성화되었던 마지막 GC 사이클을 보고합니다. GC CPU limiter에 대한 자세한 내용은 [runtime notes](#runtime)를 참조하세요.

<!-- runtime/metrics -->

#### [runtime/pprof](/pkg/runtime/pprof/)

<!-- https://go.dev/issue/33250 -->
<!-- CL 387415 -->
goroutine 프로파일을 수집할 때 Stop-the-world 일시 중지 시간이 크게 단축되어, 애플리케이션에 미치는 전반적인 지연 시간 영향이 감소했습니다.

<!-- CL 391434 -->
이제 모든 Unix 운영체제의 힙 프로파일에서 `MaxRSS`가 보고됩니다 (이전에는 `GOOS=android`, `darwin`, `ios`, `linux`에서만 보고되었습니다).

<!-- runtime/pprof -->

#### [runtime/race](/pkg/runtime/race/)

<!-- https://go.dev/issue/49761 -->
<!-- CL 333529 -->
레이스 검출기(race detector)가 `windows/amd64`와 `openbsd/amd64`(v2 유지)를 제외한 모든 지원 플랫폼에서 thread sanitizer 버전 v3를 사용하도록 업그레이드되었습니다.
v2와 비교하여 일반적으로 1.5배에서 2배 더 빠르고, 메모리 사용량은 절반으로 줄었으며, 제한 없는 수의 goroutine을 지원합니다.
Linux의 경우, 레이스 검출기를 사용하려면 이제 최소 glibc 버전 2.17 및 GNU binutils 2.26이 필요합니다.

<!-- CL 336549 -->
이제 `GOARCH=s390x`에서 race detector가 지원됩니다.

<!-- https://go.dev/issue/52090 -->
thread sanitizer 업스트림에서 `openbsd/amd64`에 대한 Race detector 지원이 제거되었으므로, v2 버전 이후로 업데이트될 가능성이 낮습니다.

<!-- runtime/race -->

#### [runtime/trace](/pkg/runtime/trace/)

<!-- CL 400795 -->
트레이싱과 [CPU profiler](/pkg/runtime/pprof/#StartCPUProfile)가 동시에 활성화된 경우, 실행 트레이스(execution trace)에는 CPU 프로파일 샘플이 순간 이벤트(instantaneous events)로 포함됩니다.

<!-- runtime/trace -->

#### [sort](/pkg/sort/)

<!-- CL 371574 -->
정렬 알고리즘이 여러 일반적인 시나리오에서 더 빠른 [pattern-defeating quicksort](https://arxiv.org/pdf/2106.05123.pdf)를 사용하도록 재작성되었습니다.

<!-- https://go.dev/issue/50340 -->
<!-- CL 396514 -->
새로운 함수 [`Find`](/pkg/sort/#Find)는 [`Search`](/pkg/sort/#Search)와 비슷하지만 사용하기 더 편리한 경우가 많습니다. 이 함수는 동일한 값이 발견되었는지 여부를 보고하는 추가적인 boolean 값을 반환합니다.

<!-- sort -->

#### [strconv](/pkg/strconv/)

<!-- CL 397255 -->
[`Quote`](/pkg/strconv/#Quote)
및 관련 함수들이 이제 다른 ASCII 값들과의 일관성을 위해 룬(rune) U+007F를 `\u007f`가 아닌 `\x7f`로 쿼트(quote)합니다.

<!-- strconv -->

#### [syscall](/pkg/syscall/)

<!-- https://go.dev/issue/51192 -->
<!-- CL 385796 -->
PowerPC (`GOARCH=ppc64`, `ppc64le`)에서
[`Syscall`](/pkg/syscall/#Syscall),
[`Syscall6`](/pkg/syscall/#Syscall6),
[`RawSyscall`](/pkg/syscall/#RawSyscall), 및
[`RawSyscall6`](/pkg/syscall/#RawSyscall6)가
이제 정의되지 않은 값 대신 반환 값 `r2`에 대해 항상 0을 반환합니다.

<!-- CL 391434 -->
AIX 및 Solaris에서 [`Getrusage`](/pkg/syscall/#Getrusage)가 이제 정의되었습니다.

<!-- syscall -->

#### [time](/pkg/time/)

새로운 메서드 [`Duration.Abs`](/pkg/time/#Duration.Abs)는 duration의 절대값을 구하는 편리하고 안전한 방법을 제공하며, −2⁶³를 2⁶³−1로 변환합니다.
(이 경계 사례는 제로 시간(zero time)에서 최근 시간을 뺐을 때 결과로 발생할 수 있습니다.)

<!-- https://go.dev/issue/50062 -->
<!-- CL 405374 -->
새로운 메서드 [`Time.ZoneBounds`](/pkg/time/#Time.ZoneBounds)는 주어진 시간에 적용되는 시간대의 시작 시간과 종료 시간을 반환합니다.
이 메서드를 루프 내에서 사용하여 특정 위치의 모든 알려진 시간대 전환(transition)을 열거할 수 있습니다.

<!-- time -->

<!-- x/build/cmd/relnote의 다음과 같은 오탐(false positives)을 무시합니다: -->
<!-- CL 382460 -->
<!-- CL 384154 -->
<!-- CL 384554 -->
<!-- CL 392134 -->
<!-- CL 392414 -->
<!-- CL 396215 -->
<!-- CL 403058 -->
<!-- CL 410133 -->
<!-- https://go.dev/issue/27837 -->
<!-- https://go.dev/issue/38340 -->
<!-- https://go.dev/issue/42516 -->
<!-- https://go.dev/issue/45713 -->
<!-- https://go.dev/issue/46654 -->
<!-- https://go.dev/issue/48257 -->
<!-- https://go.dev/issue/50447 -->
<!-- https://go.dev/issue/50720 -->
<!-- https://go.dev/issue/50792 -->
<!-- https://go.dev/issue/51115 -->
<!-- https://go.dev/issue/51447 -->
