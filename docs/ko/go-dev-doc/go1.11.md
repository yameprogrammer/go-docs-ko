<!--
참고: 이 문서 및 이 디렉토리에 있는 다른 문서에서 일관된 규칙은 고정 폭 문자열을 사용하여, 예를 들어 `hello` `world`와 같이 비고정 폭 공백을 사용하는 것입니다.
이러한 문자열에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.11 소개 {#introduction}

## Getting Started {#getting-started}

This guide will walk you through the basics of Go.

### Installation

To get started, you'll need to install Go. You can download the latest version from the official website: [https://golang.org/dl/](https://golang.org/dl/)

### Hello World

Here's a simple "Hello, World!" program:

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

To run this program, save it as `hello.go` and then run the following command:

```bash
go run hello.go
```

This will print "Hello, World!" to the console.

## Basic Concepts {#basic-concepts}

Go has several basic concepts that you should understand:

### Packages

Packages are collections of Go code that can be reused in multiple projects.

### Functions

Functions are blocks of code that perform a specific task.

### Variables

Variables are used to store data.

### Data Types

Go has several built-in data types, including:

*   `int`: Integer
*   `float64`: Floating-point number
*   `string`: Text
*   `bool`: Boolean

## Control Flow {#control-flow}

Go provides several ways to control the flow of execution:

### `if` Statements

```go
if x > 0 {
    fmt.Println("x is positive")
} else {
    fmt.Println("x is not positive")
}
```

### `for` Loops

```go
for i := 0; i < 10; i++ {
    fmt.Println(i)
}
```

### `switch` Statements

```go
switch day := "Monday"; day {
case "Monday":
    fmt.Println("It's Monday")
case "Tuesday":
    fmt.Println("It's Tuesday")
default:
    fmt.Println("It's another day")
}
```

## Conclusion {#conclusion}

This guide has provided a brief introduction to Go. There is much more to learn, but this should give you a good starting point.

가장 최신 Go 릴리스, 버전 1.11은 [Go 1.10](go1.10) 이후 6개월 만에 출시됩니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
물론, 이번 릴리스는 Go 1의 [호환성 보장](/doc/go1compat.html)을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일 및 실행될 것으로 예상됩니다.

## 언어 변경 사항 {#language}

변경 사항이 없습니다.

## 포트

<!-- CL 94255, CL 115038 등 -->
[Go 1.10 릴리스 노트](go1.10#ports)에 발표된 대로, Go 1.11에서는 다음 운영 체제 중 하나 이상이 필요합니다:
OpenBSD 6.2 이상, macOS 10.10 Yosemite 이상, 또는 Windows 7 이상;
이러한 운영 체제의 이전 버전에 대한 지원은 제거되었습니다.

<!-- CL 121657 -->
Go 1.11은 다가오는 OpenBSD 6.4 릴리스를 지원합니다. OpenBSD 커널의 변경으로 인해 이전 버전의 Go는 OpenBSD 6.4에서 작동하지 않습니다.

NetBSD에서 i386 하드웨어에서 [알려진 문제]( /issue/25206)가 있습니다.

<!-- CL 107935 -->
레이스 감지 기능이 `linux/ppc64le` 및 `netbsd/amd64` (제한적으로)에서 지원됩니다. NetBSD 레이스 감지 기능 지원은 [알려진 문제](/issue/26403)가 있습니다.

<!-- CL 109255 -->
메모리 검사기 (`-msan`)가 `linux/arm64`에서 지원됩니다.

<!-- CL 93875 -->
`c-shared` 및 `c-archive` 빌드 모드가 `freebsd/amd64`에서 지원됩니다.

<!-- CL 108475 -->
64비트 MIPS 시스템에서, 새로운 환경 변수 설정 `GOMIPS64=hardfloat` (기본값) 및
`GOMIPS64=softfloat`은 하드웨어 명령 또는 소프트웨어 에뮬레이션을 사용하여 부동 소수점 연산을 수행할지 선택합니다.
32비트 시스템의 경우, 환경 변수는 여전히 `GOMIPS`이며, [Go 1.10](go1.10#mips)에 추가되었습니다.

<!-- CL 107475 -->
소프트 플로팅 포인트 ARM 시스템 (`GOARM=5`)에서는 Go가 이제 보다 효율적인 소프트 플로팅 포인트 인터페이스를 사용합니다. 이는 Go 코드에 영향을 주지 않지만, `GOARM`에서 보호되지 않은 플로팅 포인트 명령을 사용하는 ARM 어셈블리는 중단될 수 있으며, [새 인터페이스](/cl/107475)로 포팅해야 합니다.

<!-- CL 94076 -->
Go 1.11에서 ARMv7에서는 Linux 커널이 `KUSER_HELPERS`로 구성되어 있지 않아도 됩니다. 이 설정은 기본 커널 구성에서 활성화되어 있지만, 최소화된 구성에서는 때때로 비활성화됩니다.

### WebAssembly {#wasm}

WebAssembly (Wasm)는 웹 브라우저에서 실행될 수 있는 낮은 수준의 바이너리 명령어 형식입니다.

Go 1.11은 [WebAssembly](https://webassembly.org) 에 대한 실험적인 포트를 추가합니다 (`js/wasm`).

현재 Go 프로그램은 goroutine 스케줄링, 가비지 컬렉션, 맵 등을 위한 Go 런타임을 포함하는 단일 WebAssembly 모듈로 컴파일됩니다.
따라서 결과 크기는 최소 2MB 또는 압축 시 500KB입니다. Go 프로그램은 새로운 실험적인 [`syscall/js`](/pkg/syscall/js/) 패키지를 사용하여 JavaScript를 호출할 수 있습니다.
바이너리 크기와 다른 언어와의 상호 운용성은 아직 우선순위가 아니지만, 향후 릴리스에서 고려될 수 있습니다.

결과적으로 `GOOS` 값으로 "`js`"와 `GOARCH` 값으로 "`wasm`"이 추가됨에 따라,
`*_js.go` 또는 `*_wasm.go`라는 이름의 Go 파일은
Go 툴에 의해 [무시됩니다](/pkg/go/build/#hdr-Build_Constraints) 단, 해당 `GOOS`/`GOARCH` 값이 사용될 때만 그렇습니다.
이미 해당 패턴과 일치하는 파일이 있는 경우, 이름을 변경해야 합니다.

더 자세한 내용은 다음 웹페이지에서 확인할 수 있습니다:
[WebAssembly 위키 페이지](/wiki/WebAssembly).

### RISC-V GOARCH 값 예약 {#riscv}

<!-- CL 106256 -->
주요 Go 컴파일러는 아직 RISC-V 아키텍처를 지원하지 않지만,
`GOARCH` 값인 "`riscv`" 및 "`riscv64`"를 예약했습니다. 이는 Gccgo와 같이 RISC-V를 지원하는 컴파일러가 사용하는 값과 동일합니다. 따라서, `*_riscv.go`라는 이름의 Go 파일은 Go 도구([`/pkg/go/build/#hdr-Build_Constraints`](/pkg/go/build/#hdr-Build_Constraints))에 의해 무시되지만, 해당 GOOS/GOARCH 값이 사용될 때만 그렇습니다.

## 도구 {#tools}

### 모듈, 패키지 버전 관리, 의존성 관리 {#modules}

Go 1.11은 "모듈"이라는 새로운 개념에 대한 초기 지원을 추가합니다 ([새로운 개념인 "모듈"에 대한 자세한 내용은](/cmd/go/#hdr-Modules__module_versions__and_more)).
이는 GOPATH를 대체하며, 버전 관리 및 패키지 배포에 대한 통합 지원을 제공합니다.
모듈을 사용하면 개발자는 GOPATH 내에서만 작업하는 데 제약 없이, 버전 의존성 정보가 명확하면서도 가볍게 관리할 수 있으며, 빌드 프로세스가 더 안정적이고 재현 가능합니다.

모듈 지원은 실험적인 기능으로 간주됩니다.
Go 1.11 사용자의 피드백에 따라 세부 사항이 변경될 가능성이 있으며, 추가 도구를 계획 중입니다.
모듈 지원에 대한 세부 사항이 변경되더라도, Go 1.11을 사용하여 모듈로 변환된 프로젝트는 Go 1.12 이상 버전과 함께 계속 작동합니다.
모듈을 사용할 때 문제가 발생하면,
[문제 제출](/issue/new)하여 수정할 수 있도록 도와주세요. 자세한 내용은 다음 문서를 참조하십시오.
[`go` 명령 문서](/cmd/go#hdr-Modules__module_versions__and_more).

### 가져오기 경로 제한 {#importpath}

Go 모듈 지원은 명령줄 작업에서 `@` 기호에 특별한 의미를 부여하기 때문에,
`go` 명령은 이제 `@` 기호가 포함된 임포트 경로를 사용하는 것을 허용하지 않습니다.
이러한 임포트 경로는 `go get`에서 허용되지 않았으므로,
이 제한은 다른 방법으로 사용자 정의 GOPATH 트리를 빌드하는 사용자에게만 영향을 미칩니다.

### 패키지 로딩 {#gopackages}

새로운 패키지
[`golang.org/x/tools/go/packages`](https://godoc.org/golang.org/x/tools/go/packages)
는 Go 소스 코드 패키지를 찾고 로드하기 위한 간단한 API를 제공합니다.
표준 라이브러리의 일부가 아니지만, 많은 작업에서
효과적으로 [`go/build`](/pkg/go/build) 패키지를 대체합니다.
이 패키지의 API는 모듈을 완전히 지원하지 못합니다.
외부 쿼리 명령인
[`go list`](/cmd/go/#hdr-List_packages)
을 사용하여 Go 패키지에 대한 정보를 얻기 때문에,
대안적인 빌드 시스템인 [Bazel](https://bazel.build)
및 [Buck](https://buckbuild.com)과 함께 작동하는
분석 도구를 구축할 수 있습니다.

### Go 캐시 요구 사항 {#gocache}

Go 1.11은 `GOCACHE=off` 환경 변수를 설정하여 빌드 캐시를 비활성화하는 기능을 지원하는 마지막 버전입니다.
이 기능은 Go 1.10에 도입되었습니다.
Go 1.12부터 빌드 캐시는 필수적으로 사용해야 하며, 이는 `$GOPATH/pkg`를 제거하기 위한 단계입니다.
위에 설명된 모듈 및 패키지 로딩 지원은 이미 빌드 캐시를 활성화하도록 요구합니다.
만약 문제가 발생하여 빌드 캐시를 비활성화한 경우, [이슈를 제출](https://example.com/issue/new)하여 알려주시기 바랍니다.

### 컴파일러 도구 체인 {#compiler}

<!-- CL 109918 -->
이제 기본적으로 더 많은 함수가 인라인될 수 있습니다. 여기에는 `panic`를 호출하는 함수도 포함됩니다.

<!-- CL 97375 -->
컴파일러 도구 체인이 이제 열 정보 지원을 제공합니다.
자세한 내용은 [line
지시문](/cmd/compile/#hdr-Compiler_Directives)를 참조하십시오.

<!-- CL 106797 -->
새로운 패키지 내보내기 데이터 형식이 도입되었습니다.
이는 최종 사용자에게는 투명하게 작동하지만, 대규모 Go 프로젝트의 빌드 시간을 단축하는 데 도움이 됩니다.
문제가 발생하면, 바이너리를 빌드할 때 `go` 도구에 `-gcflags=all=-iexport=false`를 전달하여 다시 비활성화할 수 있습니다.

<!-- CL 100459 -->
컴파일러는 이제 type switch의 guard 내에서 선언된 사용되지 않는 변수를 거부합니다. 예를 들어, 다음 예제에서 `x`와 같은 변수:

```markdown
```go
func f(v interface{}) {
	switch x := v.(type) {
	}
}
```

이것은 이미 `gccgo`와 [go/types](/pkg/go/types/) 모두에서 거부되었습니다.

### 어셈블러 {#assembler}

<!-- CL 113315 -->
`amd64`용 어셈블러가 이제 AVX512 명령어를 지원합니다.

### 디버깅 {#debugging}

<!-- CL 100738, CL 93664 -->
컴파일러는 최적화된 바이너리에 대해 훨씬 더 정확한 디버깅 정보를 생성합니다. 여기에는 변수 위치 정보, 라인 번호 및 중단점 위치가 포함됩니다.
이를 통해 `-N` 및 `-l` 옵션 없이 컴파일된 바이너리를 디버깅할 수 있습니다.
디버깅 정보의 품질에는 여전히 제한 사항이 있으며, 이러한 제한 사항 중 일부는 근본적인 것이고, 일부는 향후 릴리스에서 계속 개선될 것입니다.

<!-- CL 118276 -->
DWARF 섹션은 이제 컴파일러가 생성한 확장되고 더 정확한 디버깅 정보를 활용하여 기본적으로 압축됩니다.
이것은 대부분의 ELF 도구(예: Linux 및 \*BSD의 디버거)에 투명하며, Delve 디버거는 모든 플랫폼에서 지원되지만, macOS 및 Windows의 네이티브 도구에서는 제한적인 지원만 제공합니다.
DWARF 압축을 비활성화하려면, 바이너리를 빌드할 때 `go` 도구에 `-ldflags=-compressdwarf=false`를 전달하십시오.

<!-- CL 109699 -->
Go 1.11은 디버거 내에서 Go 함수를 호출하는 실험적인 기능을 추가합니다.
예를 들어, 중단점에서 일시 정지했을 때 `String` 메서드를 호출하는 데 유용합니다.
현재 이 기능은 Delve (버전 1.1.0 이상)에서만 지원됩니다.

### 테스트 {#test}

Go 1.10부터, `go` `test` 명령어는 테스트되는 패키지에 대해 `go` `vet` 명령을 실행하여, 테스트 실행 전에 문제를 식별합니다. `vet` 명령은 테스트 실행 전에 [go/types](/pkg/go/types/)를 사용하여 코드를 검사하므로, 타입 검사를 통과하지 못하는 테스트는 이제 실패합니다.
특히, Go 1.10으로 컴파일된 캡슐 안에 사용되지 않는 변수가 포함된 테스트는, Go 컴파일러가 잘못하여 허용했기 때문이었지만 ([Issue #3059](/issues/3059)), 이제 `go/types`가 올바르게 "사용되지 않는 변수" 오류를 보고하므로 실패합니다.

<!-- CL 102696 -->
`-memprofile` 플래그가 `go test` 명령에 적용될 때 기본적으로 "allocs" 프로파일로 설정되었습니다. 이 프로파일은 테스트가 시작된 이후부터 할당된 총 바이트 수를 기록합니다 (여기에는 가비지 컬렉션된 바이트도 포함됩니다).

### 수의사 {#vet}

<!-- CL 108555 -->
`go` &nbsp;`vet` (/cmd/vet/)
명령은 분석 대상 패키지가 타입 검사를 통과하지 못할 때 치명적인 오류를 보고합니다. 이전에는 타입 검사 오류가 단순히 경고를 출력하고 `vet`이 1의 상태로 종료되도록 했습니다.

<!-- CL 108559 -->
또한, [`go` `vet`](/cmd/vet)는 포맷 검사에서 `printf` 래퍼를 검사하는 데 더 강력해졌습니다.
다음 예제에서 오류를 이제 감지합니다:

```markdown
```go
func wrapper(s string, args ...interface{}) {
  fmt.Printf(s, args...)
}
```

```markdown
```go
package main

import "fmt"

func main() {
	wrapper("%d", 42)
}
```

### 추적 {#trace}

<!-- CL 63274 -->
새로운 `runtime/trace` 패키지의 [사용자
애노테이션 API](/pkg/runtime/trace/#hdr-User_annotation)를 통해 사용자는 실행 추적에 애플리케이션 레벨의 정보를 기록하고, 관련된 고루틴 그룹을 만들 수 있습니다.
`go` `tool` `trace` 명령은 이 정보를 추적 뷰와 새로운 사용자 작업/지역 분석 페이지에서 시각화합니다.

### Cgo {#cgo}

Go 1.10 이후, cgo는 일부 C 포인터 유형을 Go의 `uintptr` 유형으로 변환했습니다. 이러한 유형에는 Darwin의 CoreFoundation 프레임워크에 있는 `CFTypeRef` 계층 구조와 Java의 JNI 인터페이스에 있는 `jobject` 계층 구조가 포함됩니다. Go 1.11에서는 이러한 유형을 감지하는 코드를 개선했습니다. 이러한 유형을 사용하는 코드는 업데이트가 필요할 수 있습니다. 자세한 내용은 [Go 1.10 릴리스 노트](go1.10.html#cgo)를 참조하십시오. <!-- CL 126275, CL 127156, CL 122217, CL 122575, CL 123177 -->

### Go 명령어 {#go_command}

```
go version
```

<!-- CL 126656 -->
환경 변수 `GOFLAGS`를 사용하여 `go` 명령의 기본 플래그를 설정할 수 있습니다.
이는 특정 상황에서 유용합니다.
DWARF로 인해 저사양 시스템에서는 링크 속도가 현저히 느려질 수 있으며, 사용자는 기본적으로 `-ldflags=-w`를 설정할 수 있습니다.
모듈의 경우, 일부 사용자 및 CI 시스템에서는 항상 벤더링을 원하므로, 기본적으로 `-mod=vendor`를 설정해야 합니다.
자세한 내용은 [`go`
명령의 설명서](/cmd/go/#hdr-Environment_variables)를 참조하십시오.

### Godoc {#godoc}

Go 1.11은 `godoc`의 명령줄 인터페이스를 지원하는 마지막 버전입니다.

향후 버전에서는 `godoc`는 웹 서버로만 사용됩니다. 사용자는 명령줄 도움말 출력을 위해 `go` `doc`를 사용해야 합니다.

<!-- CL 85396, CL 124495 -->
`godoc` 웹 서버는 이제 어떤 버전의 Go가 새로운 API 기능을 도입했는지 표시합니다. 유형, 함수, 메서드의 초기 Go 버전은 오른쪽에 정렬되어 표시됩니다. 예를 들어, [`UserCacheDir`](/pkg/os/#UserCacheDir)를 참조하여, "1.11"이 오른쪽에 표시됩니다. 구조체의 필드에 대해서는, 구조체의 필드가 다른 Go 버전에서 도입되었을 때, 해당 필드에 대한 설명이 추가됩니다.
구조체의 필드 예시는 [`ClientTrace.Got1xxResponse`](/pkg/net/http/httptrace/#ClientTrace.Got1xxResponse)를 참조하십시오.

### Go 포맷 {#gofmt}

Go 소스 코드의 기본 서식 지정에 대한 하나의 작은 세부 사항이 변경되었습니다.
인라인 주석과 함께 표현식 목록을 서식 지정할 때, 주석은 휴리스틱에 따라 정렬되었습니다.
그러나, 일부 경우에는 정렬이 너무 쉽게 분리되거나, 과도한 공백을 추가하는 문제가 발생했습니다.
휴리스틱은 사람이 작성한 코드에 더 잘 작동하도록 변경되었습니다.

참고: 이러한 `gofmt`의 소규모 업데이트는 시간이 지남에 따라 예상되는 것입니다.
일반적으로 Go 소스 코드의 일관된 형식이 필요한 시스템은 특정 버전의 `gofmt` 바이너리를 사용해야 합니다.
자세한 내용은 [go/format](/pkg/go/format/) 패키지 문서를 참조하십시오.

### 실행 {#run}

<!-- CL 109341 -->
`go run` 명령은 이제 단일 가져오기 경로, 디렉토리 이름 또는 단일 패키지에 일치하는 패턴을 허용합니다.
이를 통해 `go run pkg` 또는 `go run dir`이 가능하며, 특히 `go run .`이 가능합니다.

## 런타임 {#runtime}

<!-- CL 85887 -->
런타임이 이제 스파스 힙 레이아웃을 사용하므로 Go 힙의 크기에 대한 제한이 더 이상 없습니다 (이전에는 제한이 512GiB였습니다).
또한, Go/C 바이너리 또는 `-race`로 컴파일된 바이너리에서 발생하는 드문 "주소 공간 충돌" 오류가 수정되었습니다.

<!-- CL 108679, CL 106156 -->
macOS 및 iOS에서 런타임이 이제 커널을 직접 호출하는 대신 `libSystem.dylib`을 사용합니다. 이를 통해 Go 바이너리가 향후 macOS 및 iOS 버전에 더 호환되도록 할 수 있습니다.
`syscall` ([/pkg/syscall]) 패키지는 여전히 직접 시스템 호출을 수행합니다. 이는 향후 릴리스에서 수정될 예정입니다.

## 성능 {#performance}

항상 마찬가지로, 변경 사항이 너무 광범위하고 다양하기 때문에 정확한 성능에 대한 진술을 내리는 것은 어렵습니다. 대부분의 프로그램은 더 나은 생성된 코드와 핵심 라이브러리의 최적화로 인해 약간 더 빠르게 실행될 것입니다.

<!-- CL 74851 -->
`math/big` 패키지에 여러 성능 변경 사항이 포함되었으며, 또한 `GOARCH=arm64`에 특정한 트리 전체에 걸쳐 많은 변경 사항이 있었습니다.

### 컴파일러 도구 체인 {#성능-컴파일러}

<!-- CL 110055 -->
컴파일러는 이제 다음과 같은 형태의 맵 정리 작업을 최적화합니다:

```
for k in m:
    delete(m, k)
```

<!-- CL 109517 -->
컴파일러는 이제 다음과 같은 슬라이스 확장 형태를 최적화합니다:
`append(s, make([]T, n)...)`

<!-- CL 100277, CL 105635, CL 109776 -->
컴파일러는 이제 훨씬 더 공격적인 경계 검사와 분기 제거를 수행합니다. 특히, 이제 전이 관계를 인식하므로, `i < j` 및 `j < len(s)`인 경우, 이러한 사실을 사용하여 `s[i]`에 대한 경계 검사를 제거할 수 있습니다. 또한, `s[i-10]`과 같은 간단한 산술 연산을 이해하고 루프 내에서 더 많은 추론 사례를 인식할 수 있습니다. 게다가, 컴파일러는 이제 경계 정보를 사용하여 shift 연산을 더욱 공격적으로 최적화합니다.

## 표준 라이브러리 {#library}

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, world!")
}
```

표준 라이브러리에 대한 모든 변경 사항은 미미합니다.

### 라이브러리의 미세 조정 {#minor_library_changes}

물론, 라이브러리에는 다양한 소규모 변경 사항 및 업데이트가 있으며, 이는 Go 1의 [호환성](https://doc/go1compat)을 염두에 두고 개발되었습니다.

<!-- CL 115095: https://golang.org/cl/115095: 예 (`go test pkg`는 이제 테스트 파일이 없더라도 항상 `pkg`를 빌드합니다): cmd/go: 테스트 파일이 없더라도 커버리지 보고서를 출력 -->
<!-- CL 110395: https://golang.org/cl/110395: cmd/go, cmd/compile: Windows 응답 파일을 사용하여 인자 길이 제한을 피합니다 -->
<!-- CL 112436: https://golang.org/cl/112436: cmd/pprof: 업스트림과 유사한 readline 지원을 추가 -->

#### [암호화](/pkg/crypto/)

<!-- CL 64451 -->
특정 암호화 연산, 예를 들어
[`ecdsa.Sign`](/pkg/crypto/ecdsa/#Sign),
[`rsa.EncryptPKCS1v15`](/pkg/crypto/rsa/#EncryptPKCS1v15) 및
[`rsa.GenerateKey`](/pkg/crypto/rsa/#GenerateKey)는
이제 추가적인 난수를 무작위로 읽어 테스트가 내부 동작에 의존하지 않도록 합니다.

<!-- 암호화폐 -->

#### [crypto/cipher](/pkg/crypto/cipher/)

<!-- CL 48510, CL 116435 -->
새로운 함수 [`NewGCMWithTagSize`](/pkg/crypto/cipher/#NewGCMWithTagSize)는 기존 암호화 시스템과의 호환성을 위해 표준과 다른 태그 길이를 사용하는 Galois Counter Mode를 구현합니다.

```markdown
<!-- crypto/cipher -->
```

#### [crypto/rsa](/pkg/crypto/rsa/)

<!-- CL 103876 -->
[`PublicKey`](/pkg/crypto/rsa/#PublicKey)가 이제
[`Size`](/pkg/crypto/rsa/#PublicKey.Size) 메서드를 구현하여
모듈의 크기를 바이트 단위로 반환합니다.

```markdown
<!-- crypto/rsa -->

```

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 85115 -->
`ConnectionState`의 새로운
`ExportKeyingMaterial`
메서드를 통해, RFC 5705에 따라 연결에 연결된 키잉 매터리얼을 내보낼 수 있습니다.

```markdown
<!-- crypto/tls -->
```

#### [crypto/x509](pkg/crypto/x509/)

<!-- CL 123355, CL 123695 -->
`CommonName` 필드를 호스트 이름으로 처리하는 구형, 더 이상 사용되지 않는 동작이 `CN`이 유효한 호스트 이름이 아닌 경우 비활성화되었습니다.
`CommonName`을 완전히 무시하려면 `GODEBUG` 환경 변수에 실험적인 값을 `x509ignoreCN=1`로 추가할 수 있습니다.
`CN`이 무시되면, SAN이 없는 인증서를 이름 제약 조건을 가진 체인에서 유효성 검사합니다.

<!-- CL 113475 -->
확장된 키 사용 제한 사항은 이제 `KeyUsages` 필드에만 존재할 경우에만 확인되므로, 항상 확인하는 대신.
이는 Go 1.9 이전 버전과 동일한 동작을 따릅니다.

<!-- CL 102699 -->
`SystemCertPool`에서 반환되는 값은 이제 캐싱되어 있으며, 호출 간에 시스템 변경 사항을 반영하지 않을 수 있습니다.

<!-- crypto/x509 -->

#### [debug/elf](/pkg/debug/elf/)

<!-- CL 112115 -->
`[`ELFOSABI`](/pkg/debug/elf/#ELFOSABI_NONE) 및 [`EM`](/pkg/debug/elf/#EM_NONE)
상수가 추가되었습니다.

<!-- 디버깅/ELF -->

#### [encoding/asn1](/pkg/encoding/asn1/)

<!-- CL 110561 -->
`Marshal` 및 [`Unmarshal`](/pkg/encoding/asn1/#Unmarshal)
이제 필드에 대한 "private" 클래스 어노테이션을 지원합니다.

<!-- encoding/asn1 -->

#### [encoding/base32](/pkg/encoding/base32/)

<!-- CL 112516 -->
디코더는 이제 불완전한 청크에 대해
일관되게 `io.ErrUnexpectedEOF`를 반환합니다.
이전에는 일부 경우에는 `io.EOF`를 반환했습니다.

<!-- encoding/base32 -->

#### [encoding/csv](/pkg/encoding/csv/)

<!-- CL 99696 -->
`Reader`는 이제 `Comma` 필드를 따옴표 문자로 설정하는 시도를 거부합니다. (참조: `/pkg/encoding/csv/#Reader.Comma`)
CSV에서는 이미 따옴표 문자가 특별한 의미를 가지고 있습니다.

<!-- encoding/csv -->

<!-- CL 100235이 되돌림됨 -->

#### [html/template](/pkg/html/template/)

<!-- CL 121815 -->
패키지가 타입화된 인터페이스 값을 명시적인 변환 함수에 전달할 때 동작을 변경했습니다. 이전에는 이러한 값은 `<nil>`의 (변환된 형태)로 작성되었습니다. 이제 이러한 값은 무시되며, 즉, 변환되지 않은 `nil` 값과 마찬가지로 무시됩니다.

<!-- html/템플릿 -->

#### [이미지/GIF](/pkg/image/gif/)

<!-- CL 93076 -->
루프가 없는 애니메이션 GIF를 지원합니다. 이를 나타내는 것은 `LoopCount`가 -1인 경우입니다.
[LoopCount](https://pkg/image/gif/#GIF.LoopCount)

<!-- 이미지/GIF -->

#### [io/ioutil](/pkg/io/ioutil/)

<!-- CL 105675 -->
`TempFile` ((`/pkg/io/ioutil/#TempFile`)
함수는 이제 임의의 문자열이 파일 이름에 위치하는 위치를 지정할 수 있습니다. `prefix` 인수에 "`*`"가 포함된 경우, 임의의 문자열이 "`*`"를 대체합니다. 예를 들어, `prefix` 인수가 "`myname.*.bat`"인 경우, 임의의 파일 이름, 예를 들어 "`myname.123456.bat`"이 생성됩니다. 만약 "`*`"가 포함되지 않은 경우, 이전 동작이 유지되고 임의의 숫자가 끝에 추가됩니다.

<!-- io/ioutil -->

#### [math/big](/pkg/math/big/)

<!-- CL 108996 -->
[`ModInverse`](/pkg/math/big/#Int.ModInverse)는 이제 g와 n이 서로 소가 아닌 경우 nil을 반환합니다. 이전에는 결과가 정의되지 않았습니다.

<!-- math/big -->

#### [mime/multipart](/pkg/mime/multipart/)

<!-- CL 121055 -->
파일 이름이 없는/비어 있는 form-data를 처리하는 방식이 Go 1.9의 동작으로 복원되었습니다:
[`Form`](/pkg/mime/multipart/#Form)의 form-data 부분에서 값은 `Value` 필드에 저장되며, `File` 필드가 아닌 `Value` 필드에 저장됩니다. Go 1.10부터 1.10.3 버전까지, 파일 이름이 없는/비어 있는 form-data 부분과 비어 있지 않은 "Content-Type" 필드를 가진 데이터는 `File` 필드에 저장되었습니다. 1.10 버전에서 이 변경은 오류였으며, 1.9 버전의 동작으로 되돌렸습니다.

<!-- mime/multipart -->

#### [mime/quotedprintable](/pkg/mime/quotedprintable/)

<!-- CL 121095 -->
자연에서 발견되는 유효하지 않은 입력을 지원하기 위해, 패키지는 이제 비-ASCII 바이트를 허용하지만, 해당 인코딩을 검증하지 않습니다.

<!-- mime/quotedprintable -->

#### [net](/pkg/net/)

<!-- CL 72810 -->
새로운 `ListenConfig` 타입과 새로운 `Dialer.Control` 필드는 각각 연결을 수락하고 생성하기 전에 소켓 옵션을 설정할 수 있도록 합니다.

<!-- CL 76391 -->
`[`syscall.RawConn`](/pkg/syscall/#RawConn)의 `Read`
및 `Write` 메서드가 이제 Windows에서 올바르게 작동합니다.

<!-- CL 107715 -->
`net` 패키지는 이제 Linux에서 TCP 연결 간에 데이터를 복사할 때
[`splice` 시스템 호출](https://man7.org/linux/man-pages/man2/splice.2.html)을 자동으로 사용합니다.
`TCPConn.ReadFrom` ([`TCPConn.ReadFrom`](/pkg/net/#TCPConn.ReadFrom)에서 호출됨) 및 `io.Copy`에 의해 호출되는 경우, 이 기능은 TCP 프록싱을 더 빠르고 효율적으로 만듭니다.

<!-- CL 108297 -->
`TCPConn.File`,
`UDPConn.File`,
`UnixConn.File`,
및 `IPConn.File`
메서드는 반환된 `*os.File`를
블로킹 모드로 설정하지 않습니다.

<!-- 네트워크 -->

#### [net/http](/pkg/net/http/)

<!-- CL 71272 -->
`Transport` 유형에는
새로운 `MaxConnsPerHost` 옵션이 있으며, 이는 각 호스트당 최대 연결 수를 제한할 수 있습니다.

<!-- CL 79919 -->
`[Cookie](pkg/net/http/#Cookie)` 유형에는 새로운
`[SameSite](pkg/net/http/#Cookie.SameSite)` 필드가 추가되었습니다 (새로운 유형이며 이름도 `[SameSite](pkg/net/http/#SameSite)`입니다). 이 필드는 최근 대부분의 브라우저에서 지원하는 새로운 쿠키 속성을 나타냅니다.
`net/http`의 `Transport`는 자체적으로 `SameSite` 속성을 사용하지 않지만, 패키지는 브라우저에서 사용할 수 있도록 속성의 파싱 및 직렬화를 지원합니다.

<!-- CL 81778 -->
[`Server`](/pkg/net/http/#Server)를 `Shutdown` 또는 `Close` 호출 후 재사용하는 것이 더 이상 허용되지 않습니다. 과거에는 공식적으로 지원되지 않았으며, 예측 불가능한 동작을 보였습니다. 이제, `Shutdown` 또는 `Close` 후 모든 향후 서버의 `Serve` 메서드 호출은 오류를 반환합니다.

<!-- CL 89275는 Go 1.11 이전 버전에서 되돌림됨 -->

<!-- CL 93296 -->
상수 `StatusMisdirectedRequest`가 이제 HTTP 상태 코드 421에 대해 정의되었습니다.

<!-- CL 123875 -->
HTTP 서버는 더 이상 파이프라인 HTTP/1.1 요청을 수신했을 때 컨텍스트를 취소하거나 [`CloseNotifier`](/pkg/net/http/#CloseNotifier) 채널을 통해 종료 신호를 보내지 않습니다. 브라우저는 HTTP 파이프라인을 사용하지 않지만, 일부 클라이언트 (예: Debian의 `apt`)는 이를 구성하여 사용할 수 있습니다.

<!-- CL 115255 -->
[`ProxyFromEnvironment`](/pkg/net/http/#ProxyFromEnvironment), 이 함수는
[`DefaultTransport`](/pkg/net/http/#DefaultTransport)에서 사용되며, 이제 `NO_PROXY` 환경 변수에서 CIDR 표기법과 포트를 지원합니다.

<!-- net/http -->

#### [net/http/httputil](/pkg/net/http/httputil/)

<!-- CL 77410 -->
`ReverseProxy`는
[`ErrorHandler`](/pkg/net/http/httputil/#ReverseProxy.ErrorHandler)
새로운 옵션을 제공하여 오류 처리를 변경하는 방법을 허용합니다.

<!-- CL 115135 -->
`ReverseProxy`는 이제 gRPC 프로토콜에 따라
"`TE:`&nbsp;`trailers`" 요청 헤더를 백엔드로 전달합니다.

<!-- net/http/httputil -->

#### [os](pkg/os/)

<!-- CL 78835 -->
새로운 `UserCacheDir` 함수는 사용자별 캐시 데이터를 사용하기 위한 기본 루트 디렉토리를 반환합니다.

<!-- CL 94856 -->
새로운 [`ModeIrregular`](/pkg/os/#ModeIrregular)
은 [`FileMode`](/pkg/os/#FileMode) 비트이며, 파일이 일반 파일이 아닌 것을 나타냅니다.
그러나 이 파일에 대해 다른 정보는 알 수 없거나, Go에서 정의된 모드 비트가 있는 소켓, 장치, 이름 지정 파이프, 심볼릭 링크 또는 다른 파일 유형이 아닌 경우에 사용됩니다.

<!-- CL 99337 -->
[`Symlink`](/pkg/os/#Symlink)가 이제
Windows 10에서 개발자 모드가 활성화된 기기에서
권한이 없는 사용자에게도 작동합니다.

<!-- CL 100077 -->
`NewFile`에 비동기 디스크립터를 전달하면,
결과적으로 생성되는 `*File`는 비동기 모드로 유지됩니다.
이는 해당 `*File`의 I/O가 별도의 스레드를 사용하지 않고,
runtime 폴러를 사용한다는 의미이며,
`SetDeadline` 메서드가 작동합니다.

<!-- os -->

#### [os/signal](/pkg/os/signal/)

<!-- CL 108376 -->
새로운 `Ignored` 함수는 신호가 현재 무시되고 있는지 여부를 보고합니다.

<!-- os/신호 -->

#### [os/user](/pkg/os/user/)

<!-- CL 92456 -->
`os/user` 패키지는 이제 "`osusergo`" 빌드 태그를 사용하여 순수한 Go 모드로 빌드할 수 있습니다. 이는 `CGO_ENABLED=0` 환경 변수를 사용하는 것과 관계없이 독립적으로 작동합니다. 이전에는 이 패키지의 순수한 Go 구현을 사용하려면 전체 프로그램에서 `cgo` 지원을 비활성화해야 했습니다.

<!-- os/사용자 -->

<!-- CL 101715이 되돌림됨 -->

#### [runtime](pkg/runtime/)

<!-- CL 70993 -->
`<code>GODEBUG=tracebackancestors=_N_</code>
환경 변수를 설정하면, goroutine이 생성된 스택 정보까지 트레이스백에 포함됩니다. 여기서 _N_은 보고할 부모 goroutine의 수를 제한합니다.

<!-- runtime -->

#### [runtime/pprof](/pkg/runtime/pprof/)

<!-- CL 102696 -->
이 릴리스는 프로그램이 시작된 이후에 할당된 총 바이트 수를 프로파일링하는 새로운 "allocs" 프로파일 유형을 추가합니다 (여기에는 가비지 컬렉션된 바이트도 포함). 이는 기존의 "-alloc_space" 모드에서 확인되는 "heap" 프로파일과 동일합니다.
이제 `go test -memprofile=...`는 "heap" 프로파일 대신 "allocs" 프로파일을 보고합니다.

<!-- runtime/pprof -->

#### [sync](/pkg/sync/)

<!-- CL 87095 -->
`RWMutex`에 대한 독자/쓰기 경쟁이 이제 뮤텍스 프로필에 포함됩니다.
쓰기/쓰기 경쟁은 이미 뮤텍스 프로필에 포함되어 있었습니다.

<!-- 동기화 -->

#### [syscall](/pkg/syscall/)

<!-- CL 106275 -->
Windows에서, 여러 필드가 `uintptr`에서 새 `[Pointer](pkg/syscall/?GOOS=windows&GOARCH=amd64#Pointer)`
타입으로 변경되었습니다. 이는 Go의 가비지 컬렉터와 관련된 문제를 피하기 위한 것입니다. 동일한 변경 사항은 `golang.org/x/sys/windows`
패키지도 변경되었습니다. 영향을 받는 모든 코드의 경우, 사용자는 먼저 `syscall`
패키지에서 `golang.org/x/sys/windows`
패키지로 이동하고, 그런 다음 `Pointer`를 사용하도록 변경해야 하며, `unsafe.Pointer`
변환 규칙을 준수해야 합니다.

<!-- CL 118658 -->
Linux에서 `flags` 매개변수를 `Faccessat` ([Faccessat](pkg/syscall/?GOOS=linux&GOARCH=amd64#Faccessat))에 전달하는 방식이 glibc와 동일하게 구현되었습니다. 이전 Go 버전에서는 `flags` 매개변수가 무시되었습니다.

<!-- CL 118658 -->
Linux에서 `flags` 매개변수를
[`Fchmodat`](/pkg/syscall/?GOOS=linux&GOARCH=amd64#Fchmodat)에 전달하는 경우, 이제 유효성 검사가 수행됩니다. Linux의 `fchmodat`은 `flags` 매개변수를 지원하지 않으므로, glibc의 동작을 모방하여, 값이 0이 아닌 경우 오류를 반환합니다.

<!-- syscall -->

#### [text/scanner](/pkg/text/scanner/)

<!-- CL 112037 -->
`Scanner.Scan` 메서드는 이제
`RawString` 토큰을 반환합니다.
(`/pkg/text/scanner/#RawString`)
대신 `String` 토큰을 반환하지 않습니다.
(`/pkg/text/scanner/#String`)
이는 원시 문자열 리터럴에 대한 것입니다.

<!-- text/scanner -->

#### [text/template](pkg/text/template/)

<!-- CL 84480 -->
할당을 통해 템플릿 변수를 수정하는 것이 이제 `=` 토큰을 사용하여 허용됩니다:

```
{{ $v := "init" }}
	  {{ if true }}
	    {{ $v = "changed" }}
	  {{ end }}
	  v: {{ $v }} {{/* "changed" */}}
```

<!-- CL 95215 -->
이전 버전에서는 유형이 지정되지 않은 `nil` 값이 템플릿 함수에 전달될 때 무시되었습니다. 이제 이들은 정상적인 인수로 전달됩니다.

```markdown
<!-- 템플릿 -->

#### [time](/pkg/time/)

<!-- CL 98157 -->
사인과 오프셋으로 지정된 타임존의 파싱이 이제 지원됩니다. 이전 버전에서는 숫자 타임존 이름(예: `+03`)이 유효한 것으로 간주되지 않았으며, 타임존 이름을 예상할 때 세 글자 약어(예: `MST`)만 허용되었습니다.

<!-- 시간 -->
