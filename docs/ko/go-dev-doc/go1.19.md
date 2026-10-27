<!--
참고: 이 문서 및 이 디렉토리에 있는 다른 문서에서, 고정 폭의 구문과 고정 폭이 아닌 공백을 혼용하는 것을 사용합니다. 예를 들어, `hello` `world`와 같이 사용합니다.
이러한 구문에 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.19 소개 {#introduction}

```
## Introduction to Go 1.19 {#introduction}
```

가장 최신 Go 릴리스인 버전 1.19는 [Go 1.18](/doc/go1.18) 이후 5개월 만에 출시되었습니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
물론, 이 릴리스는 Go 1의 [호환성 약속](/doc/go1compat)을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

<!-- https://go.dev/issue/52038 -->
언어에 대한 변경 사항은 매우 적습니다.
방법 선언의 [타입 매개변수의 범위에 대한 매우 작은 수정 사항](/issue/52038)
기존 프로그램에는 영향을 미치지 않습니다.

## 메모리 모델 {#mem}

<!-- https://go.dev/issue/50859 -->
[Go 메모리 모델](https://go.dev/ref/mem)이 다음과 같이
[개정](https://research.swtch.com/gomm)되어 Go가 C, C++, Java, JavaScript, Rust, Swift에서 사용되는 메모리 모델과 일치하도록 했습니다.
Go는 다른 언어에서 찾을 수 있는 더 느슨한 형태가 아닌 순차적 일관성 있는 원자적 연산만 제공합니다.
메모리 모델 업데이트와 함께,
Go 1.19는 `sync/atomic` 패키지에 [새로운 유형](https://go.dev/ref/pkg/sync/atomic)을 도입하여 원자적 값을 더 쉽게 사용할 수 있도록 합니다.
예를 들어
[atomic.Int64](https://go.dev/pkg/sync/atomic/#Int64)와
[atomic.Pointer[T](https://go.dev/pkg/sync/atomic/#Pointer)가 있습니다.

## 포트

### LoongArch 64비트 {#loong64}

<!-- https://go.dev/issue/46229 -->
Go 1.19은 Loongson 64비트 아키텍처를 위한 지원을 추가합니다.
[LoongArch](https://loongson.github.io/LoongArch-Documentation)
를 Linux (`GOOS=linux`, `GOARCH=loong64`)에서 사용할 수 있습니다.
구현된 ABI는 LP64D입니다. 지원되는 최소 커널 버전은 5.19입니다.

참고: LoongArch용 대부분의 기존 상용 Linux 배포판에는 역사적으로 호환되지 않는 시스템 호출 ABI를 가진 오래된 커널이 포함되어 있습니다. 이러한 시스템에서는 정적 연결 여부와 관계없이 컴파일된 바이너리가 작동하지 않습니다. 이러한 지원되지 않는 시스템에서 사용자는 배포판에서 제공하는 Go 패키지에만 제한됩니다.

### RISC-V {#riscv64}

<!-- CL 402374 -->
`riscv64` 포트가 이제 함수 인자와 결과를 레지스터를 사용하여 전달하도록 지원합니다. 테스트 결과, `riscv64`에서 일반적인 성능 향상을 10% 이상 보입니다.

## 도구 {#tools}

### 문서 주석 {#go-doc}

<!-- https://go.dev/issue/51082 -->
<!-- CL 384265, CL 397276, CL 397278, CL 397279, CL 397281, CL 397284 -->
Go 1.19는 문서 주석에 대한 링크, 목록 및 더 명확한 제목 지원을 추가합니다.
이 변경의 일부로, [`gofmt`](/cmd/gofmt)
이제 렌더링된 의미를 더 명확하게 만들기 위해 문서 주석을 재포맷합니다.
“[Go Doc Comments](/doc/comment)”
에서 구문 세부 정보 및 `gofmt`가 강조 표시하는 일반적인 오류에 대한 설명을 참조하십시오.
이 변경의 또 다른 부분으로, 새로운 패키지 [go/doc/comment](/pkg/go/doc/comment/)
문서 주석의 파싱 및 재포맷뿐만 아니라 HTML, Markdown 및 텍스트로 렌더링하는 데 대한 지원을 제공합니다.

### 새로운 `unix` 빌드 제약 조건 {#go-unix}

<!-- CL 389934 -->
<!-- https://go.dev/issue/20322 -->
<!-- https://go.dev/issue/51572 -->
`unix` 빌드 제약 조건이 이제 `//go:build` 줄에서 인식됩니다. 제약 조건은 대상 운영 체제가 (또는 `GOOS`) Unix 또는 Unix와 유사한 시스템인 경우에 충족됩니다. 1.19 릴리스에서는 다음 운영 체제 중 하나인 경우에 충족됩니다.
`aix`, `android`, `darwin`,
`dragonfly`, `freebsd`, `hurd`,
`illumos`, `ios`, `linux`,
`netbsd`, `openbsd`, 또는 `solaris`.
향후 릴리스에서는 `unix` 제약 조건이 추가적으로 지원되는 운영 체제와 일치할 수 있습니다.

### Go 명령어 {#go-command}

<!-- https://go.dev/issue/51461 -->

`-trimpath` 플래그가 설정되면, `go build` 명령에 의해 생성된 Go 바이너리에 포함되는 빌드 설정에 추가됩니다. 이를 검사하려면 다음을 사용할 수 있습니다.
[`go version -m`](https://pkg.go.dev/cmd/go#hdr-Print_Go_version)
또는 [`debug.ReadBuildInfo`](https://pkg.go.dev/runtime/debug#ReadBuildInfo).

`go generate`는 이제 생성기의 환경 변수에 `GOROOT` 환경 변수를 명시적으로 설정합니다. 이를 통해 생성기는 `-trimpath`로 빌드되었더라도 올바른 `GOROOT`를 찾을 수 있습니다.

<!-- CL 404134 -->
`go` `test` 및 `go` `generate` 명령은 이제
`PATH` 환경 변수에 `GOROOT/bin`을 맨 앞에 위치시키므로,
`go` 명령을 실행하는 테스트 및 생성기는 동일한 `GOROOT`을 참조하게 됩니다.

<!-- CL 398058 -->
`go` `env`가 이제 `CGO_CFLAGS`, `CGO_CPPFLAGS`, `CGO_CXXFLAGS`, `CGO_FFLAGS`, `CGO_LDFLAGS`, 그리고 `GOGCCFLAGS` 변수에 공백이 포함된 항목을 따옴표로 묶어 보고합니다.

<!-- https://go.dev/issue/29666 -->
`go list` `-json`은 이제 쉼표로 구분된 JSON 필드의 목록을 받아들입니다. 목록이 지정되면, JSON 출력에는 해당 필드만 포함되고, `go list`는 포함되지 않은 필드를 계산하는 작업을 줄일 수 있습니다. 일부 경우에는, 이로 인해 원래 보고되던 오류가 억제될 수 있습니다.

<!-- CL 410821 -->
`go` 명령이 일부 모듈을 로드하는 데 필요한 정보를 캐싱하도록 변경되었습니다.
이는 일부 `go list` 호출의 속도를 향상시킬 것으로 예상됩니다.

### 수의사 {#vet}

<!-- https://go.dev/issue/47528 -->
`vet` 검사기가 이제 `[`errors.As`](/pkg/errors/#As)가
두 번째 인자로 `*error` 타입의 인자를 가지고 호출될 때
오류를 보고합니다. 이는 흔한 실수입니다.

## 실행 시간 {#runtime}

<!-- https://go.dev/issue/48409 -->
<!-- CL 397018 -->
실행 시간은 이제 소프트 메모리 제한을 지원합니다. 이 메모리 제한에는 Go 힙과 실행 시간에 의해 관리되는 모든 메모리가 포함되며, 자체 바이너리의 매핑, 다른 언어로 관리되는 메모리, 운영 체제가 Go 프로그램의 몫으로 사용하는 메모리는 제외됩니다. 이 제한은 `[`runtime/debug.SetMemoryLimit`](/pkg/runtime/debug/#SetMemoryLimit) 또는 해당 `[`GOMEMLIMIT`](/pkg/runtime/#hdr-Environment_Variables) 환경 변수를 통해 관리할 수 있습니다. 이 제한은 `[`runtime/debug.SetGCPercent`](/pkg/runtime/debug/#SetGCPercent) / `[`GOGC`](/pkg/runtime/#hdr-Environment_Variables)와 함께 작동하며, `GOGC=off`로 설정하더라도 Go 프로그램이 항상 메모리 제한을 최대한 활용할 수 있도록 합니다. 이로 인해 특정 경우에 리소스 효율성이 향상됩니다. 소프트 메모리 제한에 대한 자세한 설명, 다양한 일반적인 사용 사례 및 시나리오에 대한 자세한 가이드는 [GC 가이드](/doc/gc-guide)를 참조하십시오. 특히, 작은 메모리 제한(수십 메가바이트 미만)은 OS 스케줄링과 같은 외부 지연 요인으로 인해 덜 견고할 수 있습니다. 자세한 내용은 [issue 52433](/issue/52433)를 참조하십시오. 수백 메가바이트 이상의 큰 메모리 제한은 안정적이며 프로덕션 환경에서 사용 가능합니다.

<!-- CL 353989 -->
프로그램의 사용 가능한 힙 크기가 소프트 메모리 제한에 가까워질 때, 가비지 컬렉션(GC)의 과도한 활동을 줄이기 위해, Go 런타임은 총 GC CPU 사용량을 50%로 제한하려고 시도합니다. (대기 시간 제외), 애플리케이션의 진행을 방해하는 대신 더 많은 메모리를 사용하는 것을 선택합니다. 실제로는, 이 제한이 예외적인 경우에만 영향을 미칠 것으로 예상되며, 새로운
[런타임 메트릭](/pkg/runtime/metrics/#hdr-Supported_metrics)
`/gc/limiter/last-enabled:gc-cycle`에서 마지막으로 이 제한이 활성화되었음을 보고합니다.

<!-- https://go.dev/issue/44163 -->
실행 시간은 애플리케이션이 주기적인 GC 사이클을 강제할 정도로 충분히 비활성화된 경우, 운영 체제 스레드에서 훨씬 적은 수의 GC 워커 고루틴을 예약합니다.

<!-- https://go.dev/issue/18138 -->
<!-- CL 345889 -->
실행 시간은 이제 고루틴의 역사적 평균 스택 사용량에 따라 초기 고루틴 스택을 할당합니다. 이를 통해 평균적인 경우에 필요한 초기 스택 증가 및 복사를 줄여, 평균 이하의 고루틴에 대해 최대 2배의 불필요한 공간을 사용합니다.

<!-- https://go.dev/issue/46279 -->
<!-- CL 393354 -->
<!-- CL 392415 -->
Unix 운영 체제에서 Go 프로그램이 [os](/pkg/os/) 패키지를 가져올 때, 열린 파일 제한(`RLIMIT_NOFILE`)이 자동으로 최대 허용 값으로 증가합니다. 즉, 소프트 제한을 하드 제한과 일치하도록 변경합니다.
이는 매우 오래된 C 프로그램을 사용하여 _select_ 시스템 호출을 사용하는 일부 시스템에서 인위적으로 낮은 제한을 설정하는 문제를 해결합니다.
Go 프로그램은 이러한 제한으로 인해 영향을 받지 않으며, 대신 `gofmt`와 같은 간단한 프로그램이 여러 파일을 병렬로 처리할 때 이러한 시스템에서 파일 디스크립터를 부족하게 사용할 수 있습니다.
이 변경의 한 가지 영향은 Go 프로그램이 자식 프로세스에서 매우 오래된 C 프로그램을 실행하는 경우, 이러한 프로그램에 너무 높은 제한을 설정할 수 있다는 것입니다.
Go 프로그램을 실행하기 전에 하드 제한을 설정하여 이 문제를 해결할 수 있습니다.

<!-- https://go.dev/issue/51485 -->
<!-- CL 390421 -->
복구 불가능한 치명적인 오류(예: 동시 맵 쓰기, 또는 잠긴 뮤텍스 해제)는 이제 실행 시간 메타데이터를 제외한 더 간단한 추적을 출력합니다 (실제 패닉과 동일). `GOTRACEBACK=system` 또는 `crash`가 설정된 경우에만 작동합니다. 실행 내부의 치명적인 오류 추적은 `GOTRACEBACK` 값에 관계없이 항상 전체 메타데이터를 포함합니다.

<!-- https://go.dev/issue/50614 -->
<!-- CL 395754 -->
ARM64에서 디버거에 삽입된 함수 호출을 지원하도록 추가되었습니다. 이를 통해 디버거를 업데이트하여 사용하는 디버깅 세션에서 사용자는 자신의 바이너리에서 함수를 호출할 수 있습니다.

<!-- https://go.dev/issue/44853 -->
[`address sanitizer` 지원이 Go 1.18에 추가되어](/doc/go1.18#go-build-asan)
이제 함수 인자와 전역 변수를 더 정확하게 처리합니다.

## 컴파일러
```
# 컴파일러
```

<!-- https://go.dev/issue/5496 -->
<!-- CL 357330, 395714, 403979 -->
컴파일러는 이제 큰 정수 및 문자열 스위치 문을 구현하기 위해
[점프 테이블](https://en.wikipedia.org/wiki/Branch_table)을 사용합니다.
스위치 문에 대한 성능 개선은 다양하지만, 약 20% 더 빠를 수 있습니다.
(`GOARCH=amd64` 및 `GOARCH=arm64`에서만 적용)

<!-- CL 391014 -->
Go 컴파일러는 이제 링크 가능한 오브젝트 파일을 빌드하기 위해 `-p=importpath` 플래그를 필요로 합니다. 이 플래그는 이미 `go` 명령과 Bazel에서 제공됩니다. Go 컴파일러를 직접 호출하는 다른 빌드 시스템은 이 플래그를 전달하도록 해야 합니다.

<!-- CL 415235 -->
Go 컴파일러는 이제 `-importmap` 플래그를 더 이상 허용하지 않습니다.
Go 컴파일러를 직접 호출하는 빌드 시스템은 대신 `-importcfg` 플래그를 사용해야 합니다.

## 어셈블러 {#assembler}

<!-- CL 404298 -->
컴파일러와 마찬가지로, 어셈블러도 링크 가능한 오브젝트 파일을 빌드하려면
`-p=importpath` 플래그를 필요로 합니다.
이는 이미 `go` 명령어를 통해 제공됩니다. Go 어셈블러를 직접 호출하는 다른 빌드 시스템은 이 플래그도 전달해야 합니다.

## 링크 편집기 {#linker}

<!-- https://go.dev/issue/50796, CL 380755 -->
ELF 플랫폼에서 링크러는 표준 gABI 형식 (`SHF_COMPRESSED`)으로 압축된 DWARF 섹션을 생성하며, 이전의 `.zdebug` 형식 대신 사용합니다.

## 표준 라이브러리 {#library}

```go
package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Println("Hello, World!")

	// 파일 읽기
	file, err := os.Open("example.txt")
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	// 파일 내용을 읽기
	content, err := ioutil.ReadAll(file)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}

	fmt.Println("File content:", string(content))
}
```

## 주요 모듈

*   `fmt`: 포맷팅된 입출력
*   `os`: 운영 체제 기능
*   `io`: 입출력
*   `ioutil`: 입출력 (deprecated)

### 새로운 원자형 데이터 타입 {#atomic_types}

<!-- https://go.dev/issue/50860 -->
<!-- CL 381317 -->
`sync/atomic` 패키지는 다음과 같은 새로운 원자형 타입을 정의합니다:
[`Bool`](/pkg/sync/atomic/#Bool),
[`Int32`](/pkg/sync/atomic/#Int32),
[`Int64`](/pkg/sync/atomic/#Int64),
[`Uint32`](/pkg/sync/atomic/#Uint32),
[`Uint64`](/pkg/sync/atomic/#Uint64),
[`Uintptr`](/pkg/sync/atomic/#Uintptr),
그리고 [`Pointer`](/pkg/sync/atomic/#Pointer).
이 타입은 내부 값을 숨겨 모든 접근이 원자형 API를 사용하도록 강제합니다.
`Pointer` 또한 호출 위치에서 `unsafe.Pointer`로 변환할 필요를 방지합니다.
`Int64` 및 `Uint64`는 구조체 및 할당된 데이터에서 64비트 경계에 자동으로 맞춰져, 32비트 시스템에서도 작동합니다.

### PATH 검색 {#os-exec-path}

<!-- https://go.dev/issue/43724 -->
<!-- CL 381374 -->
<!-- CL 403274 -->
[`Command`](/pkg/os/exec/#Command) 및
[`LookPath`](/pkg/os/exec/#LookPath)는 이제 PATH 검색 결과를 현재 디렉토리에 상대적으로 찾을 수 없습니다.
이는 [흔한 보안 문제의 원인을 제거합니다](/blog/path-security)
하지만, 예를 들어 `exec.Command("prog")`를 사용하여 현재 디렉토리에 있는 `prog` (또는 Windows에서는 `prog.exe`)라는 바이너리를 실행하는 기존 프로그램을 중단시킬 수도 있습니다.
`os/exec` 패키지의 설명서를 참조하여
이러한 프로그램을 최신 버전으로 업데이트하는 방법에 대한 정보를 확인하십시오.

<!-- https://go.dev/issue/43947 -->
Windows에서 `Command` 및 `LookPath`는 이제 `NoDefaultCurrentDirectoryInExePath`
환경 변수를 인식하여, Windows 시스템에서 PATH 검색 시 기본적으로 "."을 찾는 것을 비활성화할 수 있게 됩니다.

### 라이브러리의 미세 조정 {#minor_library_changes}

물론, 라이브러리의 다양한 미세한 변경 사항과 업데이트가 있으며, 이는 Go 1의 [호환성](/doc/go1compat)을 염두에 두고 이루어졌습니다.
또한, 여기에는 나열되지 않은 다양한 성능 개선 사항도 있습니다.

#### [archive/zip](/pkg/archive/zip/)

<!-- CL 387976 -->
[`Reader`](/pkg/archive/zip/#Reader)
이제 ZIP 파일의 시작 부분에 있는 ZIP 데이터가 아닌 데이터를 무시하여, 대부분의 다른 구현과 일치합니다.
이는 Java JAR 파일 등을 읽는 데 필요합니다.

<!-- archive/zip -->

```
#### [crypto/elliptic](/pkg/crypto/elliptic/)

<!-- CL 382995 -->
유효하지 않은 곡선 점(즉, `IsOnCurve` 메서드가 `false`를 반환하는 점, 그리고 유효한 점에 대해 `Unmarshal` 메서드나 `Curve` 메서드에서 반환되지 않는 점)을 사용하는 것은 항상 정의되지 않은 동작을 일으키고, 키 복구 공격으로 이어질 수 있습니다. 만약 유효하지 않은 점을 `Marshal`([/pkg/crypto/elliptic/#Marshal]), `MarshalCompressed`([/pkg/crypto/elliptic/#MarshalCompressed]), `Add`([/pkg/crypto/elliptic/#Curve.Add]), `Double`([/pkg/crypto/elliptic/#Curve.Double]), 또는 `ScalarMult`([/pkg/crypto/elliptic/#Curve.ScalarMult]) 메서드에 제공하면, 이제 오류가 발생합니다.

<!-- golang.org/issue/52182 -->
`ScalarBaseMult` 연산은 `P224`, `P384`, 및 `P521` 커브에서 이제 3배 더 빠르며, 이는 일부 ECDSA 연산에서도 유사한 속도 향상을 가져옵니다. 일반적인 (플랫폼 최적화되지 않은) `P256` 구현이 공식적으로 검증된 모델에서 파생된 구현으로 대체되었습니다. 이로 인해 32비트 플랫폼에서는 상당한 성능 저하가 발생할 수 있습니다.

<!-- crypto/elliptic -->

#### [crypto/rand](/pkg/crypto/rand/)

<!-- CL 370894 -->
<!-- CL 390038 -->
[`Read`](/pkg/crypto/rand/#Read)는 이제 호출 간에 운영 체제로부터 얻은
임의의 데이터를 버퍼링하지 않습니다. 많은 작은 읽기를 고빈도로 수행하는 애플리케이션은 성능상의 이유로
[`Reader`](/pkg/crypto/rand/#Reader)를 `bufio.Reader`로 래핑하는 것을 고려할 수 있으며,
[`io.ReadFull`](/pkg/io/#ReadFull)를 사용하여 부분적인 읽기가 발생하지 않도록 주의해야 합니다.

<!-- CL 375215 -->
Plan 9에서 `Read` 함수가 재구현되었으며, ANSI X9.31 알고리즘을 대체하여 더 빠른 키 삭제 생성기를 사용합니다.

<!-- CL 391554 -->
<!-- CL 387554 -->
`[Prime](pkg/crypto/rand/#Prime)`
구현이 변경되어, 단독으로 재단 샘플링만 사용하도록 변경되었습니다.
이는 비암호화 컨텍스트에서 소형 난수를 생성할 때 발생하는 편향을 제거하고,
잠재적인 미미한 타이밍 누출을 제거하며,
BoringSSL과 동작 방식을 더 일치시키고,
구현을 단순화하는 효과를 가져옵니다.
이 변경으로 인해 동일한 난수 소스 스트림에 대해 이전 구현과 비교하여 다른 출력이 생성될 수 있으며,
이는 특정 결과(특정 결정론적 난수 소스에서)를 기대하는 테스트를 깨뜨릴 수 있습니다.
향후 이러한 문제 발생을 방지하기 위해,
구현은 이제 입력 스트림에 대해 의도적으로 비결정적이게 되었습니다.

<!-- crypto/rand -->

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 400974 -->
<!-- https://go.dev/issue/45428 -->
`GODEBUG` 옵션 `tls10default=1`이 제거되었습니다. `Config.MinVersion`을 설정하여 TLS 1.0 클라이언트 측에서 활성화하는 것은 여전히 가능합니다.

<!-- CL 384894 -->
TLS 서버와 클라이언트는 이제 TLS 핸드셰이프에서 중복된 확장 요청을 거부합니다. 이는 RFC 5246, 섹션 7.4.1.4 및 RFC 8446, 섹션 4.2에 따라 요구됩니다.

<!-- crypto/tls -->

#### [crypto/x509](/pkg/crypto/x509/)

<!-- CL 285872 -->
[`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate)
더 이상 `SignatureAlgorithm`을 `MD5WithRSA`로 설정하여 인증서를 생성하는 기능을 지원하지 않습니다.

<!-- CL 400494 -->
`CreateCertificate` 기능이 더 이상 음수 시리얼 번호를 허용하지 않습니다.

<!-- CL 399827 -->
`CreateCertificate`는 이제 생성된 인증서에 확장 기능이 없는 경우 더 이상 빈 SEQUENCE를 생성하지 않습니다.

<!-- CL 396774 -->
`GODEBUG` 옵션 `x509sha1=1`의 제거,
원래 Go 1.19에 계획되었던 것은, 향후 릴리스로 변경되었습니다.
이 옵션을 사용하는 애플리케이션은 마이그레이션하는 것을 고려해야 합니다.
SHA-1에 대한 실제 공격은 2017년부터 시연되었으며, 공신력 있는 인증 기관에서는 2015년부터 SHA-1 인증서를 발급하지 않고 있습니다.

<!-- CL 383215 -->
[`ParseCertificate`](/pkg/crypto/x509/#ParseCertificate)
과 [`ParseCertificateRequest`](/pkg/crypto/x509/#ParseCertificateRequest)
은 이제 중복된 확장 항목을 포함하는 인증서 및 CSR를 거부합니다.

<!-- https://go.dev/issue/46057 -->
<!-- https://go.dev/issue/35044 -->
<!-- CL 398237 -->
<!-- CL 400175 -->
<!-- CL 388915 -->
새로운 `CertPool.Clone` 및 `CertPool.Equal` 메서드는 `CertPool`을 복제하고 두 개의 `CertPool`의 동등성을 확인하는 기능을 제공합니다.

<!-- https://go.dev/issue/50674 -->
<!-- CL 390834 -->
새로운 함수 [`ParseRevocationList`](/pkg/crypto/x509/#ParseRevocationList)는
더 빠르고 안전하게 사용할 수 있는 CRL 파서를 제공하며,
[`RevocationList`](/pkg/crypto/x509/#RevocationList)를 반환합니다.
CRL 파싱은 또한 새로운 `RevocationList` 필드인
`RawIssuer`, `Signature`,
`AuthorityKeyId`, 및 `Extensions`을 채웁니다. 이 필드는
[`CreateRevocationList`](/pkg/crypto/x509/#CreateRevocationList)에서 무시됩니다.

새로운 방법 [`RevocationList.CheckSignatureFrom`](/pkg/crypto/x509/#RevocationList.CheckSignatureFrom)는 CRL에 있는 서명이 유효한 [`Certificate`](/pkg/crypto/x509/#Certificate)의 서명인지 확인합니다.

[`ParseCRL`](/pkg/crypto/x509/#ParseCRL) 및
[`ParseDERCRL`](/pkg/crypto/x509/#ParseDERCRL) 함수는 `ParseRevocationList` 함수로 대체되었습니다.
[`Certificate.CheckCRLSignature`](/pkg/crypto/x509/#Certificate.CheckCRLSignature) 메서드는 `RevocationList.CheckSignatureFrom`로 대체되었습니다.

<!-- CL 389555, CL 401115, CL 403554 -->
`Certificate.Verify` 패키지의 경로 빌더가 수정되었으며, 이제 더 나은 체인을 생성하거나 복잡한 시나리오에서 더 효율적으로 작동해야 합니다.
이제 비 잎 인증서에도 이름 제약 조건이 적용됩니다.

<!-- crypto/x509 -->

#### [crypto/x509/pkix]

<!-- CL 390834 -->
`CertificateList` 및 `TBSCertificateList` 유형이 더 이상 사용되지 않습니다. 대신 새로운 `crypto/x509` CRL 기능 (`#crypto/x509`)을 사용해야 합니다.

<!-- crypto/x509/pkix -->

#### [debug/elf](/pkg/debug/elf/)

<!-- CL 396735 -->
새로운 `EM_LOONGARCH` 및 `R_LARCH_*` 상수는 loong64 포트를 지원합니다.

<!-- 디버깅/ELF -->

#### [debug/pe](/pkg/debug/pe/)

<!-- https://go.dev/issue/51868 -->
<!-- CL 394534 -->
새로운 `File.COFFSymbolReadSectionDefAux` 방법([https://go.dev/pkg/debug/pe/#File.COFFSymbolReadSectionDefAux](https://go.dev/pkg/debug/pe/#File.COFFSymbolReadSectionDefAux)),
이 방법은 `COFFSymbolAuxFormat5`를 반환하며, PE 파일 섹션의 COMDAT 정보를 액세스할 수 있도록 해줍니다.
이것은 새로운 `IMAGE_COMDAT_*` 및 `IMAGE_SCN_*` 상수로 지원됩니다.

<!-- 디버깅/PE -->

#### [encoding/binary](/pkg/encoding/binary/)

<!-- https://go.dev/issue/50601 -->
<!-- CL 386017 -->
<!-- CL 389636 -->
새로운 인터페이스
[`AppendByteOrder`](/pkg/encoding/binary/#AppendByteOrder)
은 `uint16`, `uint32`, 또는 `uint64`를 바이트 슬라이스에 추가하기 위한 효율적인 방법을 제공합니다.
[`BigEndian`](/pkg/encoding/binary/#BigEndian) 및
[`LittleEndian`](/pkg/encoding/binary/#LittleEndian)이 이제 이 인터페이스를 구현합니다.

<!-- https://go.dev/issue/51644 -->
<!-- CL 400176 -->
마찬가지로, 새로운 함수
[`AppendUvarint`](/pkg/encoding/binary/#AppendUvarint) 및
[`AppendVarint`](/pkg/encoding/binary/#AppendVarint)는
[`PutUvarint`](/pkg/encoding/binary/#PutUvarint) 및
[`PutVarint`](/pkg/encoding/binary/#PutVarint)의 효율적인 추가 버전입니다.

<!-- encoding/binary -->

#### [encoding/csv](/pkg/encoding/csv/)

<!-- https://go.dev/issue/43401 -->
<!-- CL 405675 -->
새로운 메서드
[`Reader.InputOffset`](/pkg/encoding/csv/#Reader.InputOffset)
는 리더의 현재 입력 위치를 바이트 오프셋으로 보고하며,
`encoding/json`의
[`Decoder.InputOffset`](/pkg/encoding/json/#Decoder.InputOffset)와 유사합니다.

<!-- encoding/csv -->

#### [encoding/xml](/pkg/encoding/xml/)

<!-- https://go.dev/issue/45628 -->
<!-- CL 311270 -->
새로운 메서드
[`Decoder.InputPos`](/pkg/encoding/xml/#Decoder.InputPos)
는 리더의 현재 입력 위치를 줄과 열로 보고하며,
`encoding/csv`의
[`Decoder.FieldPos`](/pkg/encoding/csv/#Decoder.FieldPos)와 유사합니다.

<!-- encoding/xml -->

#### [flag](/pkg/flag/)

<!-- https://go.dev/issue/45754 -->
<!-- CL 313329 -->
새로운 함수
[`TextVar`](/pkg/flag/#TextVar)
은 `encoding.TextUnmarshaler` 인터페이스를 구현하는 값을 갖는 플래그를 정의하며, 이를 통해 명령줄 플래그 변수에 `big.Int`, `netip.Addr`, `time.Time`과 같은 타입을 사용할 수 있습니다.

<!-- 깃발 -->

#### [fmt](/pkg/fmt/)

<!-- https://go.dev/issue/47579 -->
<!-- CL 406177 -->
새로운 함수
[`Append`](/pkg/fmt/#Append),
[`Appendf`](/pkg/fmt/#Appendf), 및
[`Appendln`](/pkg/fmt/#Appendln)는 형식화된 데이터를 바이트 슬라이스에 추가합니다.

<!-- fmt -->

#### [go/parser](/pkg/go/parser/)

<!-- CL 403696 -->
파서가 이제 `~x`를 연산자 있는 단일 표현식으로 인식합니다.
[token.TILDE](/pkg/go/token/#TILDE),
이를 통해 `~int`와 같은 타입 제약 조건이 잘못된 컨텍스트에서 사용될 때 더 나은 오류 복구를 할 수 있습니다.

<!-- go/parser -->

#### [go/types](pkg/go/types/)

<!-- https://go.dev/issue/51682 -->
<!-- CL 395535 -->
새로운 메서드 `Func.Origin` 및 `Var.Origin`은
[`Object`](/pkg/go/types/#Object) 유형을 반환합니다.
이는 생성 중인 합성 `Func` 및 `Var` 객체에 대한
일반적인 유형에 해당합니다.

<!-- https://go.dev/issue/52728 -->
<!-- CL 404885 -->
이제 재귀 호출을 통해
[`Named`](/pkg/go/types/#Named) 타입의 인스턴스를 무한히 생성하는 것은 더 이상 불가능합니다.
`Named.Underlying` 또는 `Named.Method`에 대한 재귀 호출을 사용합니다.

<!-- go/types -->

#### [hash/maphash](/pkg/hash/maphash/)

<!-- https://go.dev/issue/42710 -->
<!-- CL 392494 -->
새로운 함수
[`Bytes`](/pkg/hash/maphash/#Bytes)
및
[`String`](/pkg/hash/maphash/#String)
은 단일 바이트 슬라이스 또는 문자열을 효율적으로 해싱하는 방법을 제공합니다.
이는 더 일반적인
[`Hash`](/pkg/hash/maphash/#Hash)
를 사용하는 것과 동일하지만, 작은 입력에 대한 설정 오버헤드를 피합니다.

<!-- 해시/맵 (hash/map) -->

#### [html/template](/pkg/html/template/)

<!-- https://go.dev/issue/46121 -->
<!-- CL 389156 -->
`FuncMap` 유형은 이제 `/pkg/html/template/#FuncMap` 대신
`text/template`의 `FuncMap`에 대한 별칭입니다.
이를 통해, `FuncMap`을 설정에서든 다른 설정에서든 사용할 수 있는 코드를 작성할 수 있습니다.

<!-- https://go.dev/issue/59153 -->
<!-- CL 481987 -->
Go 1.19.8 이상
[ECMAScript 6 템플릿 리터럴에서 동작 제한](/pkg/html/template#hdr-Security_Model)
이 동작은 `GODEBUG=jstmpllitinterp=1` 설정으로 되돌릴 수 있습니다.

<!-- html/템플릿 -->

#### [이미지/그리기](/pkg/image/draw/)

<!-- CL 396795 -->
[`Draw`](/pkg/image/draw/#Draw) 연산자를 사용하여
[`Src`](/pkg/image/draw/#Src) 를 사용하면, 대상 및 소스 이미지가 모두
[`image.NRGBA`](/pkg/image/#NRGBA) 또는 모두
[`image.NRGBA64`](/pkg/image/#NRGBA64) 인 경우,
비-곱셈된 알파 색상을 유지합니다.
이는 Go 1.18 라이브러리 최적화로 인해 실수로 도입된 동작 변경 사항을 되돌립니다. 현재 코드는 Go 1.17 및 이전 버전의 동작과 일치합니다.

<!-- 이미지/그리기 -->

#### [io](/pkg/io/)

<!-- https://go.dev/issue/51566 -->
<!-- CL 400236 -->
[`NopCloser`](/pkg/io/#NopCloser)의 결과가 이제
[`WriterTo`](/pkg/io/#WriterTo)를 구현합니다.

<!-- https://go.dev/issue/50842 -->
[`MultiReader`](/pkg/io/#MultiReader)의 결과는 이제 `WriterTo`](/pkg/io/#WriterTo)를 조건 없이 구현합니다.
만약 어떤 내부 리더가 `WriterTo`를 구현하지 않으면, 적절하게 시뮬레이션됩니다.

<!-- 입출력 -->

#### [mime](/pkg/mime/)

<!-- CL 406894 -->
Windows에서만, `mime` 패키지는 이제 레지스트리 항목을 무시하여 `.js` 확장자에 대해 `text/plain` MIME 유형을 지정하는 것을 방지합니다. 이는 Windows 시스템에서 흔한 의도치 않은 설정입니다. 결과적으로 `.js`는 기본 MIME 유형인 `text/javascript; charset=utf-8`을 갖게 됩니다.
Windows에서 `text/plain`을 예상하는 애플리케이션은 이제 명시적으로
[`AddExtensionType`](/pkg/mime/#AddExtensionType)를 호출해야 합니다.

<!-- mime -->

#### [mime/multipart](/pkg/mime/multipart)

<!-- https://go.dev/issue/59153 -->
<!-- CL 481985 -->
Go 1.19.8 이후 버전에서, 이 패키지는 악의적인 입력으로부터 보호하기 위해 처리하는 MIME 데이터의 크기를 제한합니다.
`Reader.NextPart` 및 `Reader.NextRawPart`는 한 파트의 헤더 수를 10000으로 제한하고, `Reader.ReadForm`은 모든 `FileHeaders`에 있는 헤더의 총 수를 10000으로 제한합니다.
이 제한은 `GODEBUG=multipartmaxheaders` 설정을 통해 조정할 수 있습니다.
`Reader.ReadForm`은 또한 폼에 있는 파트의 수를 1000으로 더욱 제한합니다.
이 제한은 `GODEBUG=multipartmaxparts` 설정을 통해 조정할 수 있습니다.

<!-- mime/multipart -->

#### [net](/pkg/net/)

<!-- CL 386016 -->
순수 Go 리졸버는 이제 EDNS(0)를 사용하여 예상 최대 응답 패킷 길이를 포함하게 됩니다. 이를 통해 응답 패킷은 최대 1232 바이트(이전 최대값은 512 바이트)를 포함할 수 있습니다.
만약 이로 인해 로컬 DNS 리졸버에 문제가 발생한다면, `GODEBUG=netdns=cgo` 환경 변수를 설정하여 cgo 기반 리졸버를 사용하는 것이 해결책이 될 수 있습니다.
이러한 문제를 [이슈 추적기](/issue/new)에 보고해 주십시오.

<!-- https://go.dev/issue/51428 -->
<!-- CL 396877 -->
`net` 패키지 함수 또는 메서드가 "I/O 타임아웃" 오류를 반환할 때, 오류가 이제 `errors.Is(err, context.DeadlineExceeded)`를 만족합니다. `net` 패키지 함수가 "운영이 취소됨" 오류를 반환할 때, 오류가 이제 `errors.Is(err, context.Canceled)`를 만족합니다.
이 변경 사항은 컨텍스트 취소 또는 타임아웃이 `net` 패키지 함수 또는 메서드가 오류를 반환하는 경우를 테스트하는 데 도움이 되도록 하는 것을 목표로 하며, 오류 메시지에 대한 이전 호환성을 유지합니다.

<!-- https://go.dev/issue/33097 -->
<!-- CL 400654 -->
[`Resolver.PreferGo`](/pkg/net/#Resolver.PreferGo)
이 기능은 Windows 및 Plan 9에서도 구현되었습니다. 이전에는 Unix 플랫폼에서만 작동했습니다. `Dialer.Resolver` 및 `Resolver.Dial`과 함께 사용하면, DNS 이름 확인을 제어하고 모든 DNS 확인을 처리하는 휴대성이 뛰어난 프로그램을 작성할 수 있습니다.

`net` 패키지는 이제 Windows에서 `netgo` 빌드 태그에 대한 초기 지원을 제공합니다. 사용될 때, 패키지는 Windows에 DNS 결과를 요청하는 대신 Go DNS 클라이언트(Resolver.PreferGo에서 사용되는 것과 동일)를 사용합니다. Windows에서 발견하는 업스트림 DNS 서버가 복잡한 시스템 네트워크 구성과 일치하지 않을 수 있습니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- CL 269997 -->
[`ResponseWriter.WriteHeader`](/pkg/net/http/#ResponseWriter)
이제 사용자 정의 1xx 정보 헤더를 전송할 수 있습니다.

<!-- CL 361397 -->
`io.ReadCloser` 타입으로 반환되는
[`MaxBytesReader`](/pkg/net/http/#MaxBytesReader)는
더 이상 읽기 제한이 초과될 때
[`MaxBytesError`](/pkg/net/http/#MaxBytesError) 타입을 반환합니다.

<!-- CL 375354 -->
HTTP 클라이언트는 `Location` 헤더가 없는 3xx 응답을 처리하여 호출자에게 반환합니다.
오류로 처리하는 대신입니다.

<!-- net/http -->

#### [net/url](/pkg/net/url/)

<!-- CL 374654 -->
새로운
[`JoinPath`](/pkg/net/url/#JoinPath)
함수와
[`URL.JoinPath`](/pkg/net/url/#URL.JoinPath)
메서드는 경로 요소의 목록을 결합하여 새로운 `URL`을 생성합니다.

<!-- https://go.dev/issue/46059 -->
`URL` 타입은 이제 권한이 없는 URL과 빈 권한이 있는 URL을 구별합니다. 예를 들어, `http:///path`는 빈 권한(호스트)을 가지고 있으며, `http:/path`는 권한이 없습니다.

새로운 [`URL`](/pkg/net/url/#URL) 필드
`OmitHost`는 `URL`이 비어 있는 호스트를 가질 때 `true`로 설정됩니다.

<!-- net/url -->

#### [os/exec](/pkg/os/exec/)

<!-- https://go.dev/issue/50599 -->
<!-- CL 401340 -->
`Cmd` 객체에 비어 있지 않은 `Dir` 필드와 `Env`가 `nil`인 경우, 이제 하위 프로세스의 `PWD` 환경 변수를 `Dir` 값과 일치하도록 자동으로 설정합니다.

새로운 방법 [`Cmd.Environ`](/pkg/os/exec/#Cmd.Environ)은 명령을 실행하는 데 사용될 환경을 보고하며, 명시적으로 설정된 `PWD` 변수도 포함합니다.

<!-- os/exec -->

#### [reflect](/pkg/reflect/)

<!-- https://go.dev/issue/47066 -->
<!-- CL 357331 -->
`Value.Bytes` 메서드는 슬라이스 외에도 주소 지정된 배열을 이제 지원합니다.

<!-- CL 400954 -->
`Value.Len` 및 `Value.Cap` 메서드는 이제 배열의 포인터에 성공적으로 작동하여 해당 배열의 길이를 반환하며, 이는 [내장
`len` 및 `cap` 함수](/ref/spec#Length_and_capacity)가 수행하는 것과 일치합니다.

<!-- 반영 -->

#### [regexp/구문](/pkg/regexp/syntax/)

<!-- https://go.dev/issue/51684 -->
<!-- CL 401076 -->
Go 1.18 릴리스 후보 1, Go 1.17.8, 및 Go 1.16.15은 정규 표현식 파서에 보안 패치를 포함하여, 매우 깊게 중첩된 표현식을 거부하도록 변경했습니다.
Go 패치 릴리스는 새로운 API를 도입하지 않으므로, 이 경우 파서는 [`syntax.ErrInternalError`](/pkg/regexp/syntax/#ErrInternalError)를 반환했습니다.
Go 1.19는 더 구체적인 오류인 [`syntax.ErrNestingDepth`](/pkg/regexp/syntax/#ErrNestingDepth)를 도입하여, 파서가 이제 이 오류를 반환합니다.

<!-- 정규 표현식 -->

#### [runtime](pkg/runtime/)

<!-- https://go.dev/issue/51461 -->
`[`GOROOT`](/pkg/runtime/#GOROOT) 함수는 이제 바이너리가 `-trimpath` 플래그로 빌드되었고, `GOROOT` 변수가 프로세스 환경 변수에 설정되지 않은 경우 빈 문자열을 반환합니다 (대신 `"go"`).

<!-- 실행 환경 -->

#### [runtime/metrics](/pkg/runtime/metrics/)

<!-- https://go.dev/issue/47216 -->
<!-- CL 404305 -->
새로운 `/sched/gomaxprocs:threads`
[메트릭](https://go.dev/pkg/runtime/metrics/#hdr-Supported_metrics)은
현재
[`runtime.GOMAXPROCS`](https://go.dev/pkg/runtime/#GOMAXPROCS)
값을 보고합니다.

<!-- https://go.dev/issue/47216 -->
<!-- CL 404306 -->
새로운 `/cgo/go-to-c-calls:calls`
[메트릭](/pkg/runtime/metrics/#hdr-Supported_metrics)
은 Go에서 C로 호출된 총 횟수를 보고합니다. 이 메트릭은
`runtime.NumCgoCall`
함수와 동일합니다.

<!-- https://go.dev/issue/48409 -->
<!-- CL 403614 -->
새로운 `/gc/limiter/last-enabled:gc-cycle`
[메트릭](pkg/runtime/metrics/#hdr-Supported_metrics)
는 GC CPU 제한기가 활성화되었을 때의 마지막 GC 사이클을 보고합니다. GC CPU 제한기에 대한 자세한 내용은 [실시간 노트](runtime)를 참조하십시오.

<!-- 성능/메트릭스 -->

#### [runtime/pprof](/pkg/runtime/pprof/)

<!-- https://go.dev/issue/33250 -->
<!-- CL 387415 -->
goroutine 프로필을 수집할 때, `Stop-the-world` 일시 중지 시간이 크게 줄어들어, 전체적인 애플리케이션의 지연 시간에 미치는 영향을 감소시킵니다.

<!-- CL 391434 -->
`MaxRSS`는 이제 모든 유닉스 운영 체제(이전에는 `GOOS=android`, `darwin`, `ios`, 및 `linux`에 대해서만 보고됨)의 힙 프로필에서 보고됩니다.

<!-- runtime/pprof -->

#### [runtime/race](/pkg/runtime/race/)

<!-- https://go.dev/issue/49761 -->
<!-- CL 333529 -->
레이스 감지기는 모든 지원 플랫폼에서 thread sanitizer 버전 v3을 사용하도록 업그레이드되었습니다.
`windows/amd64` 및 `openbsd/amd64`는 v2를 유지합니다.
v2에 비해 일반적으로 1.5배에서 2배 더 빠르고, 메모리 사용량이 절반으로 줄어들며, 무제한의 goroutine을 지원합니다.
Linux에서 레이스 감지기는 이제 glibc 버전 2.17 이상 및 GNU binutils 2.26 이상을 필요로 합니다.

<!-- CL 336549 -->
레이스 감지 기능이 `GOARCH=s390x`에서 지원됩니다.

<!-- https://go.dev/issue/52090 -->
`openbsd/amd64`에 대한 레이스 감지 기능은 스레드 산산파에 의해 제거되었으므로, v2에서 업데이트될 가능성은 낮습니다.

<!-- runtime/race -->

#### [runtime/trace](/pkg/runtime/trace/)

<!-- CL 400795 -->
트레이싱 및
[CPU 프로파일러](/pkg/runtime/pprof/#StartCPUProfile)를 동시에 활성화하면 실행 트레이스에는 CPU 프로파일 샘플이 즉각적인 이벤트로 포함됩니다.

<!-- runtime/trace -->

#### [sort](/pkg/sort/)

<!-- CL 371574 -->
정렬 알고리즘이 [패턴을 무력화하는 퀵소트](https://arxiv.org/pdf/2106.05123.pdf)를 사용하도록 재작성되었습니다.
이는 여러 일반적인 시나리오에서 더 빠른 성능을 제공합니다.

<!-- https://go.dev/issue/50340 -->
<!-- CL 396514 -->
새로운 함수
[`Find`](/pkg/sort/#Find)
은
[`Search`](/pkg/sort/#Search)
과 유사하지만, 일반적으로 사용하기 더 쉽습니다: 이 함수는 동일한 값이 발견되었는지 여부를 나타내는 추가적인 부울 값을 반환합니다.

<!-- 정렬 -->

#### [strconv](/pkg/strconv/)

<!-- CL 397255 -->
[`Quote`](/pkg/strconv/#Quote)
및 관련 함수가 이제 유니코드 문자 `U+007F`를 `\x7f`로 쿼트하며,
`\u007f`가 아닌,
다른 ASCII 값과의 일관성을 위해.

<!-- strconv -->

#### [syscall](/pkg/syscall/)

<!-- https://go.dev/issue/51192 -->
<!-- CL 385796 -->
PowerPC (`GOARCH=ppc64`, `ppc64le`)에서,
[`Syscall`](/pkg/syscall/#Syscall),
[`Syscall6`](/pkg/syscall/#Syscall6),
[`RawSyscall`](/pkg/syscall/#RawSyscall),
그리고
[`RawSyscall6`](/pkg/syscall/#RawSyscall6)
이제 반환 값 `r2`에 대해 항상 0을 반환하며, 더 이상 정의되지 않은 값을 반환하지 않습니다.

<!-- CL 391434 -->
AIX 및 Solaris에서, [`Getrusage`](/pkg/syscall/#Getrusage)가 정의되었습니다.

<!-- syscall -->

#### [time](/pkg/time/)

<!-- https://go.dev/issue/51414 -->
<!-- CL 393515 -->
새로운 메서드
[`Duration.Abs`](/pkg/time/#Duration.Abs)
은 시간의 절대값을 쉽게 안전하게 취하는 방법을 제공하며, −2⁶³을 2⁶³−1로 변환합니다.
(이 경계 사례는 최근 시간을 0부터 뺀 결과로 발생할 수 있습니다.)

<!-- https://go.dev/issue/50062 -->
<!-- CL 405374 -->
새로운 메서드
[`Time.ZoneBounds`](/pkg/time/#Time.ZoneBounds)
는 주어진 시간에 유효한 시간대의 시작 및 종료 시간을 반환합니다.
이를 사용하여 특정 위치에서 발생하는 모든 알려진 시간대 전환을 반복적으로 나열할 수 있습니다.

<!-- 시간 -->

<!-- 다음 빌드 관련 false positive를 무시: -->
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
