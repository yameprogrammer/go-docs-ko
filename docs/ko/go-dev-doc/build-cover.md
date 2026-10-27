목차:

[개요](#overview)
[커버리지 프로파일링을 위한 바이너리 빌드](#building)
[커버리지로 장착된 바이너리 실행](#running)
[커버리지 데이터 파일 작업](#working)
[자주 묻는 질문](#FAQ)
[자원](#resources)
[용어 설명](#glossary)

Go 1.20부터, Go는 애플리케이션과 통합 테스트에서 수집된 커버리지 프로파일을 지원하며, Go 프로그램에 대한 더 크고 복잡한 테스트를 가능하게 합니다.

## 개요 {#overview}

Go는 "`go test -coverprofile=... <pkg_target>`" 명령어를 통해 패키지 단위 테스트 수준에서 커버리지 프로필을 수집하는 데 사용하기 쉬운 기능을 제공합니다.

Go 1.20부터 사용자는 더 큰 [통합 테스트](#glos-integration-test)를 위한 커버리지 프로필을 수집할 수 있습니다: 특정 애플리케이션 바이너리를 여러 번 실행하는 더 무겁고 복잡한 테스트입니다.

단위 테스트를 위한 커버리지 프로파일을 수집하고 보고서를 생성하려면 두 단계가 필요합니다: `go test -coverprofile=...` 실행 후, `go tool cover {-func, -html}`을 호출하여 보고서를 생성합니다.

통합 테스트를 수행하려면 다음 세 단계가 필요합니다: [빌드](#building) 단계, [실행](#running) 단계 (이는 빌드 단계에서 여러 번 실행되는 바이너리의 호출을 포함할 수 있음), 그리고 마지막으로 [보고](#reporting) 단계, 아래에 설명된 대로.

# 커버리지 프로파일링을 위한 바이너리 빌드 {#building}

## Prerequisites
*   A working Go development environment.
*   The `go` toolchain installed.
*   The `go test` command available in your PATH.

## Building the Binary

The process of building a binary for coverage profiling depends on your specific needs and the toolchain you are using. However, the general steps are as follows:

1.  **Ensure your project is correctly configured.** This includes having a `go.mod` file and a `go.sum` file, and that your project is properly initialized with `go mod init`.

2.  **Build the project.** Use the `go build` command to build the executable. For example:

    ```bash
    go build -o my_app ./
    ```

    This command will create an executable named `my_app`. Replace `my_app` with the desired name for your binary.

3.  **(Optional) Install any necessary dependencies.** If your project has external dependencies, make sure they are installed before building. You can use `go get` or your project's package manager.

4.  **Run the binary.** Once the binary is built, you can run it and observe its behavior.

## Example: Building with `go test`

If you are using `go test` for building, you can use the `-build` flag to create an executable. For example:

```bash
go test -build ./ ...
```

This will create a binary named `my_app` (or whatever name you specify).

## Important Considerations

*   **Operating System:** The build process may vary depending on your operating system (Windows, macOS, Linux).
*   **Compiler:** Ensure you have a compatible Go compiler installed and configured.
*   **Dependencies:** Carefully manage your project's dependencies to avoid build errors.

## Troubleshooting

If you encounter any issues during the build process, here are some common troubleshooting steps:

*   **Check your error messages:** Carefully read the error messages to understand the cause of the problem.
*   **Verify your Go environment:** Make sure your Go environment is correctly configured.
*   **Search for solutions online:** Use search engines to find solutions to common build problems.

## Further Resources

*   [Go Documentation](https://go.dev/doc)
*   [Go Blog](https://go.dev/blog)

애플리케이션을 실행할 때, `go build` 명령을 실행할 때 `-cover` 플래그를 전달하여 커버리지 프로파일을 수집하는 애플리케이션의 대상 바이너리에 전달합니다. 샘플 `go build -cover` 실행 예시는 [아래](#packageselection) 섹션을 참조하십시오.

결과 바이너리는 다음 섹션 ([실행](#running))에서 환경 변수를 설정하여 커버리지 프로파일을 캡처하는 데 사용할 수 있습니다.

## 패키지 선택 기준 {#패키지선택}

이 섹션에서는 어떤 패키지가 프로파일링 및 분석에 사용될지 결정하는 방법에 대해 설명합니다.

"`go build -cover`" 명령을 실행하는 동안, Go 명령은 메인 모듈의 패키지를 커버리지 프로파일링에 선택합니다. 기본적으로 build에 기여하는 다른 패키지 (go.mod 파일에 나열된 의존성 또는 Go 표준 라이브러리의 일부인 패키지)는 포함되지 않습니다.

예를 들어, 여기는 main 패키지, 로컬 main-모듈 패키지 `greetings` 및 외부 모듈에서 가져온 패키지들의 집합을 포함하는 간단한 프로그램입니다. 여기에는 (예시로) `rsc.io/quote` 및 `fmt` 등이 포함됩니다 ([전체 프로그램 링크](/play/p/VSQJN8xkkf-?v=gotip)).

```
$ cat go.mod
모듈 mydomain.com

go 1.20

require rsc.io/quote v1.5.2

require (
	golang.org/x/text v0.0.0-20170915032832-14c0d48ead0c // 간접 의존
	rsc.io/sampler v1.3.0 // 간접 의존
)

$ cat myprogram.go
패키지 main

import (
	"fmt"
	"mydomain.com/greetings"
	"rsc.io/quote"
)

func main() {
	fmt.Printf("저는 %q 와 %q 라고 말합니다\n", quote.Hello(), greetings.Goodbye())
}
$ cat greetings/greetings.go
패키지 greetings

func Goodbye() string {
	return "see ya"
}
$ go build -cover -o myprogram.exe .
$
```

만약 이 프로그램을 "-cover" 명령줄 플래그와 함께 빌드하고 실행하면, 프로필에 포함될 패키지는 정확히 두 개입니다: `main`과 `mydomain.com/greetings`입니다. 다른 의존 패키지는 제외됩니다.

사용자가 포함할 패키지를 더 세밀하게 제어하고 싶다면, "`-coverpkg`" 플래그를 사용하여 빌드할 수 있습니다. 예시:

$ go build -cover -o myprogramMorePkgs.exe -coverpkg=io,mydomain.com,rsc.io/quote .
$

위 빌드에서, `mydomain.com`의 메인 패키지와 `rsc.io/quote` 및 `io` 패키지가 프로파일링에 선택되었습니다. `mydomain.com/greetings`가 명시적으로 나열되지 않았기 때문에, 메인 모듈에 위치하고 있음에도 불구하고 프로파일에서 제외됩니다.

# 커버처 삽입된 바이너리 실행 방법 {#running}

## 실행 방법

1.  커버처 삽입된 바이너리를 실행합니다.
2.  커버처가 올바르게 작동하는지 확인하기 위해 테스트를 실행합니다.
3.  커버처 보고서를 분석하여 코드 커버리지를 확인합니다.

`"-cover"`로 빌드된 바이너리는 실행 후 지정된 디렉터리 (환경 변수 `GOCOVERDIR`을 통해 지정)에 프로파일링 데이터 파일을 작성합니다. 예:

$ go build -cover -o myprogram.exe myprogram.go
$ mkdir somedata
$ GOCOVERDIR=somedata ./myprogram.exe
저는 "Hello, world."과 "see ya"라고 말합니다.
$ ls somedata
covcounters.c6de772f99010ef5925877a7b05db4cc.2424989.1670252383678349347
covmeta.c6de772f99010ef5925877a7b05db4cc
$

참고: `somedata` 디렉토리에 작성된 두 파일입니다. 이 (이진) 파일에는 커버리지 결과가 포함되어 있습니다. 이 데이터 파일에서 사람이 읽을 수 있는 결과를 생성하는 방법에 대한 자세한 내용은 다음 섹션인 [보고](#보고)를 참조하십시오.

만약 `GOCOVERDIR` 환경 변수가 설정되지 않은 경우, 커버리지에 장착된 바이너리가 여전히 올바르게 실행되지만 경고를 표시합니다.
예시:

```
$ ./myprogram.exe
경고: GOCOVERDIR이 설정되지 않았으므로, 커버리지 데이터가 생성되지 않습니다.
저는 "Hello, world." 및 "see ya"라고 말합니다.
$
```

## 여러 번 실행을 포함하는 테스트

통합 테스트는 종종 여러 프로그램 실행을 포함합니다. 프로그램이 "-cover" 옵션으로 빌드되면, 각 실행은 새로운 데이터 파일을 생성합니다. 예시:

$ mkdir somedata2
$ GOCOVERDIR=somedata2 ./myprogram.exe          // 첫 번째 실행
저는 "Hello, world." 및 "see ya" 라고 말합니다.
$ GOCOVERDIR=somedata2 ./myprogram.exe -flag    // 두 번째 실행
저는 "Hello, world." 및 "see ya" 라고 말합니다.
$ ls somedata2
covcounters.890814fca98ac3a4d41b9bd2a7ec9f7f.2456041.1670259309405583534
covcounters.890814fca98ac3a4d41b9bd2a7ec9f7f.2456047.1670259309410891043
covmeta.890814fca98ac3a4d41b9bd2a7ec9f7f

커버리지 데이터 출력 파일은 두 가지 형태로 제공됩니다: 메타데이터 파일 (실행 간 일관성을 유지하는 항목을 포함, 예를 들어 소스 파일 이름 및 함수 이름) 및 카운터 데이터 파일 (프로그램에서 실행된 부분을 기록).

위의 예시에서 첫 번째 실행은 `counter` 및 `meta` 두 개의 파일을 생성했지만, 두 번째 실행에서는 `counter` 데이터 파일만 생성되었습니다. 이는 `meta` 데이터가 실행마다 변경되지 않기 때문에, 한 번만 기록하면 되기 때문입니다.

# 커버리지 데이터 파일 사용 방법 {#working}

## 1. 파일 구조 이해
커버리지 데이터 파일은 일반적으로 다음과 같은 구조를 가집니다.

Go 1.20에서 새 도구인 "`covdata`"를 소개합니다. 이 도구를 사용하면 `GOCOVERDIR` 디렉터리에서 커버리지 데이터 파일을 읽고 조작할 수 있습니다.

Go의 `covdata` 도구는 다양한 모드로 실행됩니다. `covdata` 도구 호출의 일반적인 형태는 다음과 같습니다.

```
$ go tool covdata <모드> -i=<dir1,dir2,...> ...플래그...
```

여기에서 "-i" 플래그는 읽을 디렉토리 목록을 제공하며, 각 디렉토리는 `GOCOVERDIR`을 통해 실행된 커버리지 측정된 바이너리(coverage-instrumented binary)에서 파생됩니다.

## 커버리지 프로파일 보고서 생성 {#reporting}

## Creating coverage profile reports {#reporting}

이 섹션에서는 "`go tool covdata`"를 사용하여 커버리지 데이터 파일에서 사람이 읽을 수 있는 보고서를 생성하는 방법을 설명합니다.

### 보고서의 비율 명세 항목 확인

각 "측정된 패키지별 비율" 메트릭을 보고하려면 다음 명령을 사용합니다: ``go tool covdata percent -i=<디렉토리>``.

위의 [실행](#running) 섹션의 예제를 참조하십시오:

$ ls somedata
covcounters.c6de772f99010ef5925877a7b05db4cc.2424989.1670252383678349347
covmeta.c6de772f99010ef5925877a7b05db4cc
$ go tool covdata percent -i=somedata
	main	코드 커버리지: 100.0%
	mydomain.com/greetings	코드 커버리지: 100.0%

"처리된 문장의 비율"은 여기 표시된 비율은 `go test -cover`에서 보고된 것과 직접적으로 일치합니다.

## 레거시 텍스트 형식으로 변환하기

이 섹션에서는 다양한 형식의 데이터를 레거시 텍스트 형식으로 변환하는 방법을 설명합니다.

`covdata`의 `textfmt` 선택기를 사용하여 이진 커버리지 데이터 파일을 "`go test -coverprofile=<outfile>`"에서 생성된 기존 텍스트 형식으로 변환할 수 있습니다. 생성된 텍스트 파일을 "`go tool cover -func`" 또는 "`go tool cover -html`"과 함께 사용하여 추가 보고서를 생성할 수 있습니다. 예시:

$ ls somedata
covcounters.c6de772f99010ef5925877a7b05db4cc.2424989.1670252383678349347
covmeta.c6de772f99010ef5925877a7b05db4cc
$ go tool covdata textfmt -i=somedata -o profile.txt
$ cat profile.txt
mode: set
mydomain.com/myprogram.go:10.13,12.2 1 1
mydomain.com/greetings/greetings.go:3.23,5.2 1 1
$ go tool cover -func=profile.txt
mydomain.com/greetings/greetings.go:3:	Goodbye		100.0%
mydomain.com/myprogram.go:10:		main		100.0%
total:					(statements)	100.0%

## 병합

`merge` 하위 명령어는 "`go tool covdata`"의 기능을 사용하여 여러 데이터 디렉토리에서 생성된 프로파일을 합치는 데 사용할 수 있습니다.

예를 들어, macOS와 Windows에서 모두 실행되는 프로그램을 고려해 보세요.
이 프로그램의 작성자는 각 운영 체제에서 별도로 실행된 커버리지 프로필을 하나의 프로필 코퍼스로 결합하여,
교차 플랫폼 커버리지 요약을 생성하고 싶을 수 있습니다.
예를 들어:

$ ls windows_datadir
covcounters.f3833f80c91d8229544b25a855285890.1025623.1667481441036838252
covcounters.f3833f80c91d8229544b25a855285890.1025628.1667481441042785007
covmeta.f3833f80c91d8229544b25a855285890
$ ls macos_datadir
covcounters.b245ad845b5068d116a4e25033b429fb.1025358.1667481440551734165
covcounters.b245ad845b5068d116a4e25033b429fb.1025364.1667481440557770197
covmeta.b245ad845b5068d116a4e25033b429fb
$ ls macos_datadir
$ mkdir merged
$ go tool covdata merge -i=windows_datadir,macos_datadir -o merged
$

위의 병합 작업은 지정된 입력 디렉토리의 데이터를 결합하고, "merged" 디렉토리에 새로운 병합된 데이터 파일 세트를 작성합니다.

## 패키지 선택

대부분의 "`go tool covdata`" 명령어는 운영의 일부로 패키지를 선택하는 데 "-pkg" 플래그를 지원합니다. "-pkg"에 전달되는 인수는 Go 명령어의 "-coverpkg" 플래그에서 사용되는 동일한 형식을 갖습니다.
예시:

```
$ ls somedata
covcounters.c6de772f99010ef5925877a7b05db4cc.2424989.1670252383678349347
covmeta.c6de772f99010ef5925877a7b05db4cc
$ go tool covdata percent -i=somedata -pkg=mydomain.com/greetings
	mydomain.com/greetings	커버리지: 100.0%
$ go tool covdata percent -i=somedata -pkg=nonexistentpackage
$
```

"-pkg" 플래그를 사용하면 특정 보고서에 필요한 특정 패키지 집합을 선택할 수 있습니다.

#

## 자주 묻는 질문 {#FAQ}

1. [내 `go.mod` 파일에 언급된 모든 가져온 패키지에 대한 커버리지 측정 도구를 요청하는 방법은 무엇입니까?](#gomodselect)
2. `go build -cover`를 GOPATH/GO111MODULE=off 모드에서 사용할 수 있습니까?](#gopathmode)
3. 프로그램이 패닉(panic)을 발생시키면, 커버리지 데이터가 기록됩니까?](#panicprof)
4. `-coverpkg=main`이 내 메인 패키지를 프로파일링에 선택합니까?](#mainpkg)

#### `go.mod` 파일에 언급된 모든 가져온 패키지에 대한 커버리지 측정값을 요청하는 방법 {#gomodselect}

`go build -cover`는 기본적으로 모든 메인 모듈 패키지에 대해 커버리지를 측정합니다. 그러나 메인 모듈 외부의 패키지(예: 표준 라이브러리 패키지 또는 `go.mod` 파일에 나열된 임포트)에 대해서는 측정하지 않습니다.
표준 라이브러리 외의 모든 종속성에 대해 커버리지를 요청하는 한 가지 방법은 `go list`의 출력을 `-coverpkg`에 제공하는 것입니다.
다음은 위에서 언급된 [예제 프로그램](/play/p/VSQJN8xkkf-?v=gotip)을 사용하는 예입니다:

```
$ go list -f '{{if not .Standard}}{{.ImportPath}}{{end}}' -deps . | paste -sd "," > pkgs.txt
$ go build -o myprogram.exe -coverpkg=`cat pkgs.txt` .
$ mkdir somedata
$ GOCOVERDIR=somedata ./myprogram.exe
$ go tool covdata percent -i=somedata
	golang.org/x/text/internal/tag	커버리지: 78.4%의 스테이트먼트
	golang.org/x/text/language	커버리지: 35.5%의 스테이트먼트
	mydomain.com	커버리지: 100.0%의 스테이트먼트
	mydomain.com/greetings	커버리지: 100.0%의 스테이트먼트
	rsc.io/quote	커버리지: 25.0%의 스테이트먼트
	rsc.io/sampler	커버리지: 86.7%의 스테이트먼트
$
```

#### `go build -cover`를 GO111MODULE=off 모드에서 사용할 수 있나요? {#gopathmode}

네, `go build -cover`는 `GO111MODULE=off`와 함께 작동합니다.

`GO111MODULE=off` 모드로 프로그램을 빌드할 때, 명령줄에 명시적으로 지정된 대상 패키지만 프로파일링을 위해 측정됩니다. `-coverpkg` 플래그를 사용하여 프로파일에 추가 패키지를 포함할 수 있습니다.

#### 프로그램이 충돌하면 커버리지 데이터가 기록될까요? {#panicprof}

`go build -cover`로 빌드된 프로그램은 프로그램이 `os.Exit()`를 호출하거나 `main.main`에서 정상적으로 반환하는 경우에만 실행 후 전체 프로파일 데이터를 기록합니다.

만약 프로그램이 복구 불가능한 패닉으로 종료되거나, 프로그램이 심각한 예외(예: 메모리 접근 오류, 0으로 나누기 등)를 발생시키는 경우, 실행 중에 실행된 문에 대한 프로파일 데이터는 손실됩니다.

#### `-coverpkg=main` 옵션이 메인 패키지를 프로파일링 대상으로 선택합니까? {#mainpkg}

`-coverpkg` 플래그는 임포트 경로 목록을 받아들입니다. 패키지 이름 목록이 아닌, 패키지 경로 목록을 사용해야 합니다. `main` 패키지를 커버리지 측정에 선택하려면, 이름을 아닌 패키지 경로로 식별하십시오. 예시 (다음 예제 프로그램을 사용: [이 예제 프로그램](/play/p/VSQJN8xkkf-?v=gotip)):

```
$ go list -m
mydomain.com
$ go build -coverpkg=main -o oops.exe .
경고: 빌드되는 패키지 중 main 패턴과 일치하는 패키지가 없음
$ go build -coverpkg=mydomain.com -o myprogram.exe .
$ mkdir somedata
$ GOCOVERDIR=somedata ./myprogram.exe
저는 "Hello, world."와 "see ya"라고 말합니다.
$ go tool covdata percent -i=somedata
	mydomain.com	커버리지: 100.0%의 스테이트
$
```

## 리소스 {#resources}

- **1.2 버전의 Go에서 유닛 테스트 커버리지를 소개하는 블로그 게시물**:
  - 유닛 테스트를 위한 커버리지 프로파일링은 Go 1.2 릴리스의 일부로 도입되었습니다. 자세한 내용은 [이 블로그 게시물](/blog/cover)를 참조하세요.
- **문서**:
  - [`cmd/go`](https://pkg.go.dev/cmd/go) 패키지의 문서에는 커버리지와 관련된 빌드 및 테스트 플래그에 대한 설명이 포함되어 있습니다.
- **기술적 세부 사항**:
  - [설계 초안](/design/51430-revamp-code-coverage)
  - [제안](/issue/51430)

## 용어 설명 {#glossary}

<a id="glos-unit-test"></a>
**단위 테스트:** 특정 Go 패키지에 연결된 `*_test.go` 파일 내에서 수행되는 테스트로, Go의 `testing` 패키지를 사용합니다.

**통합 테스트:** 특정 애플리케이션 또는 바이너리에 대한 보다 포괄적이고, 더 많은 리소스를 사용하는 테스트입니다. 통합 테스트는 일반적으로 프로그램을 또는 프로그램 집합을 빌드하고, 여러 입력 및 시나리오를 사용하여 프로그램을 여러 번 실행하는 것을 포함하며, 이는 Go의 `testing` 패키지에 기반한 테스트 래프를 사용하여 제어될 수 있습니다.
