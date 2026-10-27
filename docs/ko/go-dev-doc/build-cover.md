목차:

[개요](#overview)\
 [커버리지 프로파일링을 위한 바이너리 빌드](#building)\
 [커버리지 계측 바이너리 실행](#running)\
 [커버리지 데이터 파일 작업](#working)\
 [자주 묻는 질문](#FAQ)\
 [리소스](#resources)\
 [용어 사전](#glossary)

Go 1.20부터 Go는 애플리케이션과 통합 테스트(Go 프로그램에 대한 더 크고 복잡한 테스트)로부터 커버리지 프로필을 수집하는 기능을 지원합니다.

# 개요 {#overview}

Go는 "`go test -coverprofile=... <pkg_target>`" 명령어를 통해 패키지 단위 테스트 수준에서 커버리지 프로필을 수집할 수 있는 사용하기 쉬운 지원을 제공합니다.
Go 1.20부터 사용자는 더 큰 규모의 [통합 테스트](#glos-integration-test), 즉 주어진 애플리케이션 바이너리를 여러 번 실행하는 더 무겁고 복잡한 테스트에 대한 커버리지 프로필을 수집할 수 있습니다.

단위 테스트의 경우, 커버리지 프로필을 수집하고 보고서를 생성하려면 두 단계가 필요합니다. 먼저 `go test -coverprofile=...`를 실행한 다음, `go tool cover {-func,-html}`를 호출하여 보고서를 생성해야 합니다.

통합 테스트를 위해서는 다음과 같이 설명된 세 단계가 필요합니다: [빌드](#building) 단계, [실행](#running) 단계(빌드 단계에서 생성된 바이너리를 여러 번 호출하는 과정이 포함될 수 있음), 그리고 마지막으로 [보고](#reporting) 단계입니다.

# 커버리지 프로파일링을 위한 바이너리 빌드 {#building}

커버리지 프로필을 수집하는 애플리케이션을 빌드하려면, 애플리케이션 바이너리 타겟에 대해 `go build`를 호출할 때 `-cover` 플래그를 전달하십시오. `go build -cover` 호출 예제는 [아래](#packageselection) 섹션을 참조하십시오.

이렇게 생성된 바이너리는 환경 변수 설정을 통해 커버리지 프로필을 캡처하며 실행할 수 있습니다 ([실행](#running)에 관한 다음 섹션 참조).

## 인스트루멘테이션을 위한 패키지 선택 방법 {#packageselection}

특정 "`go build -cover`" 호출 중에, `go` 커맨드는 커버리지 프로파일링을 위해 메인 모듈 내의 패키지들을 선택합니다. 빌드에 포함되는 다른 패키지들(`go.mod`에 나열된 의존성 또는 Go 표준 라이브러리의 일부인 패키지들)은 기본적으로 포함되지 않습니다.

예를 들어, 여기 `main` 패키지와 로컬 main-module 패키지인 `greetings`, 그리고 `rsc.io/quote` 및 `fmt`를 포함하여 모듈 외부에서 가져온 패키지 세트를 포함하는 토이 프로그램이 있습니다 ([전체 프로그램 링크](/play/p/VSQJN8xkkf-?v=gotip)).

```
$ cat go.mod
module mydomain.com

go 1.20

require rsc.io/quote v1.5.2

require (
	golang.org/x/text v0.0.0-20170915032832-14c0d48ead0c // indirect
	rsc.io/sampler v1.3.0 // indirect
)

$ cat myprogram.go
package main

import (
	"fmt"
	"mydomain.com/greetings"
	"rsc.io/quote"
)

func main() {
	fmt.Printf("I say %q and %q\n", quote.Hello(), greetings.Goodbye())
}
$ cat greetings/greetings.go
package greetings

func Goodbye() string {
	return "see ya"
}
$ go build -cover -o myprogram.exe .
$
```

이 프로그램을 "`-cover`" 명령줄 플래그와 함께 빌드하고 실행하면, `main`과 `mydomain.com/greetings`라는 정확히 두 개의 패키지만 프로파일에 포함되며, 그 외의 의존 패키지들은 제외됩니다.

커버리지에 포함될 패키지를 더 세밀하게 제어하고 싶은 사용자는 `"-coverpkg"` 플래그를 사용하여 빌드할 수 있습니다. 예시:

```
$ go build -cover -o myprogramMorePkgs.exe -coverpkg=io,mydomain.com,rsc.io/quote .
$
```

위의 빌드에서 `mydomain.com`의 main 패키지와 `rsc.io/quote` 및 `io` 패키지가 프로파일링 대상으로 선택되었습니다. `mydomain.com/greetings`는 구체적으로 목록에 지정되지 않았으므로, 메인 모듈 내에 있더라도 프로파일에서 제외됩니다.

# 커버리지 계측 바이너리 실행하기 {#running}

"`-cover`"로 빌드된 바이너리는 실행이 종료될 때 환경 변수 `GOCOVERDIR`를 통해 지정된 디렉토리에 프로파일 데이터 파일을 기록합니다. 예시:

```
$ go build -cover -o myprogram.exe myprogram.go
$ mkdir somedata
$ GOCOVERDIR=somedata ./myprogram.exe
I say "Hello, world." and "see ya"
$ ls somedata
covcounters.c6de772f99010ef5925877a7b05db4cc.2424989.1670252383678349347
covmeta.c6de772f99010ef5925877a7b05db4cc
$
```

`somedata` 디렉토리에 작성된 두 개의 파일을 확인하십시오. 이 (바이너리) 파일들은 커버리지 결과를 포함하고 있습니다. 이 데이터 파일들로부터 사람이 읽을 수 있는 결과물을 생성하는 방법에 대한 자세한 내용은 [reporting](#reporting) 섹션을 참조하십시오.

`GOCOVERDIR` 환경 변수가 설정되어 있지 않으면, 커버리지 계측(instrumented)된 바이너리는 여전히 올바르게 실행되지만 경고를 발생시킵니다.
예시:

```
$ ./myprogram.exe
warning: GOCOVERDIR not set, no coverage data emitted
I say "Hello, world." and "see ya"
$
```

## 여러 번의 실행을 포함하는 테스트

통합 테스트의 경우 많은 상황에서 여러 번의 프로그램 실행이 포함될 수 있습니다. 프로그램이 "`-cover`" 옵션으로 빌드되면, 각 실행마다 새로운 데이터 파일이 생성됩니다. 예시:

```
$ mkdir somedata2
$ GOCOVERDIR=somedata2 ./myprogram.exe          // 첫 번째 실행
I say "Hello, world." and "see ya"
$ GOCOVERDIR=somedata2 ./myprogram.exe -flag    // 두 번째 실행
I say "Hello, world." and "see ya"
$ ls somedata2
covcounters.890814fca98ac3a4d41b9bd2a7ec9f7f.2456041.1670259309405583534
covcounters.890814fca98ac3a4d41b9bd2a7ec9f7f.2456047.1670259309410891043
covmeta.890814fca98ac3a4d41b9bd2a7ec9f7f
$
```

커버리지 데이터 출력 파일은 두 가지 유형으로 제공됩니다. 메타데이터 파일(소스 파일 이름 및 함수 이름과 같이 실행 시마다 변하지 않는 항목을 포함)과 카운터 데이터 파일(프로그램에서 실행된 부분을 기록)입니다.

위의 예시에서, 첫 번째 실행에서는 두 개의 파일(`counter`와 `meta`)이 생성되었지만, 두 번째 실행에서는 `counter` 데이터 파일만 생성되었습니다. 메타데이터는 실행 시마다 변경되지 않으므로 한 번만 기록하면 되기 때문입니다.

# 커버리지 데이터 파일 작업하기 {#working}

Go 1.20에서는 `GOCOVERDIR` 디렉토리의 커버리지 데이터 파일을 읽고 조작하는 데 사용할 수 있는 새로운 도구인 '`covdata`'가 도입되었습니다.

Go의 `covdata` 도구는 다양한 모드로 실행됩니다. `covdata` 도구 호출의 일반적인 형식은 다음과 같습니다.

```
$ go tool covdata <mode> -i=<dir1,dir2,...> ...flags...
```

여기서 "`-i`" 플래그는 읽어올 디렉터리 목록을 제공하며, 각 디렉터리는 ( `GOCOVERDIR`을 통해) 커버리지 계측(instrumentation)이 적용된 바이너리의 실행 결과로부터 생성됩니다.

## 커버리지 프로파일 보고서 생성하기 {#reporting}

이 섹션에서는 커버리지 데이터 파일로부터 사람이 읽을 수 있는 보고서를 생성하기 위해 "`go tool covdata`"를 사용하는 방법을 설명합니다.

### 커버된 퍼센트 문장 보고하기

각 계측된 패키지에 대해 "퍼센트 문장 커버리지(percent statements covered)" 메트릭을 보고하려면, "`go tool covdata percent -i=<directory>`" 명령어를 사용하십시오.
위의 [실행(running)](#running) 섹션에 있는 예시를 사용하면 다음과 같습니다.

```
$ ls somedata
covcounters.c6de772f99010ef5925877a7b05db4cc.2424989.1670252383678349347
covmeta.c6de772f99010ef5925877a7b05db4cc
$ go tool covdata percent -i=somedata
	main	coverage: 100.0% of statements
	mydomain.com/greetings	coverage: 100.0% of statements
$
```

여기에서 "statements covered" 백분율은 `go test -cover`에 의해 보고된 수치와 직접적으로 일치합니다.

## 레거시 텍스트 형식으로 변환하기

`covdata textfmt` 셀렉터를 사용하여 바이너리 커버리지 데이터 파일을 "`go test -coverprofile=<outfile>`"로 생성된 레거시 텍스트 형식으로 변환할 수 있습니다. 이렇게 생성된 텍스트 파일은 "`go tool cover -func`" 또는 "`go tool cover -html`"과 함께 사용하여 추가 보고서를 생성하는 데 사용할 수 있습니다. 예시:

```
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
$
```

## Merging

`go tool covdata`의 `merge` 서브커맨드는 여러 데이터 디렉토리의 프로필을 하나로 병합하는 데 사용할 수 있습니다.

예를 들어, macOS와 Windows 모두에서 실행되는 프로그램을 생각해 보겠습니다.
이 프로그램의 작성자는 각 운영 체제에서 별도로 실행한 커버리지 프로필을 하나의 프로필 코퍼스(corpus)로 결합하여, 크로스 플랫폼 커버리지 요약을 생성하고 싶을 수 있습니다.
예를 들면 다음과 같습니다:

```
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
```

위의 merge 작업은 지정된 입력 디렉터리의 데이터를 결합하여 "merged" 디렉터리에 병합된 새로운 데이터 파일 세트를 기록합니다.

## 패키지 선택

대부분의 "`go tool covdata`" 명령은 작업의 일부로 패키지 선택을 수행하는 "`-pkg`" 플래그를 지원합니다. "`-pkg`"에 전달되는 인수는 Go 명령의 "`-coverpkg`" 플래그에서 사용하는 것과 동일한 형식을 갖습니다.
예시:

```

$ ls somedata
covcounters.c6de772f99010ef5925877a7b05db4cc.2424989.1670252383678349347
covmeta.c6de772f99010ef5925877a7b05db4cc
$ go tool covdata percent -i=somedata -pkg=mydomain.com/greetings
	mydomain.com/greetings	coverage: 100.0% of statements
$ go tool covdata percent -i=somedata -pkg=nonexistentpackage
$
```

"`-pkg`" 플래그를 사용하여 특정 보고서에 대해 관심 있는 패키지의 특정 하위 집합을 선택할 수 있습니다.

번역할 원문 콘텐츠가 제공되지 않았습니다. 번역이 필요한 Markdown 내용을 입력해 주세요. 세심한 기술 번역을 통해 Markdown 구조, 표, 링크, 리스트, 인라인 코드 및 코드 펜스를 그대로 유지하며, Go 패키지 이름, 식별자, URL, 명령어 또는 코드 스니펫은 번역하지 않고 정확하게 전달해 드리겠습니다.

## 자주 묻는 질문 {#FAQ}

1. [`go.mod` 파일에 언급된 모든 가져온 패키지에 대해 커버리지 인스트루멘테이션(instrumentation)을 요청하려면 어떻게 해야 하나요?](#gomodselect)
2. [GOPATH/GO111MODULE=off 모드에서 `go build -cover`를 사용할 수 있나요?](#gopathmode)
3. [프로그램에 패닉(panic)이 발생하면 커버리지 데이터가 기록되나요?](#panicprof)
4. [`-coverpkg=main`을 사용하면 프로파일링을 위해 main 패키지가 선택되나요?](#mainpkg)

#### `go.mod` 파일에 언급된 모든 임포트된 패키지에 대해 커버리지 인스트루먼테이션(instrumentation)을 요청하려면 어떻게 해야 하나요? {#gomodselect}

기본적으로 `go build -cover`는 모든 메인 모듈 패키지에 대해 커버리지 계측(instrument)을 수행하지만, 메인 모듈 외부의 임포트(예: 표준 라이브러리 패키지 또는 `go.mod`에 나열된 임포트)는 계측하지 않습니다.
표준 라이브러리를 제외한 모든 의존성에 대해 계측을 요청하는 한 가지 방법은 `go list`의 출력을 `-coverpkg`에 전달하는 것입니다.
위에서 언급한 [예제 프로그램](/play/p/VSQJN8xkkf-?v=gotip)을 사용한 예시는 다음과 같습니다.

```
$ go list -f '{{"{{if not .Standard}}{{.ImportPath}}{{end}}"}}' -deps . | paste -sd "," > pkgs.txt
$ go build -o myprogram.exe -coverpkg=`cat pkgs.txt` .
$ mkdir somedata
$ GOCOVERDIR=somedata ./myprogram.exe
$ go tool covdata percent -i=somedata
	golang.org/x/text/internal/tag	coverage: 78.4% of statements
	golang.org/x/text/language	coverage: 35.5% of statements
	mydomain.com	coverage: 100.0% of statements
	mydomain.com/greetings	coverage: 100.0% of statements
	rsc.io/quote	coverage: 25.0% of statements
	rsc.io/sampler	coverage: 86.7% of statements
$
```

#### GO111MODULE=off 모드에서 `go build -cover`를 사용할 수 있나요? {#gopathmode}

네, `go build -cover`는 `GO111MODULE=off` 설정에서도 작동합니다.
`GO111MODULE=off` 모드로 프로그램을 빌드할 때, 커맨드 라인에서 타겟으로 명시된 패키지만 프로파일링을 위해 계측(instrumented)됩니다. 프로파일에 추가 패키지를 포함하려면 `-coverpkg` 플래그를 사용하십시오.

#### 프로그램이 패닉(panic)이 발생하면 커버리지 데이터가 기록되나요? {#panicprof}

`go build -cover`로 빌드된 프로그램은 프로그램이 `os.Exit()`를 호출하거나 `main.main`에서 정상적으로 반환되는 경우에만 실행 종료 시 완전한 프로파일 데이터를 기록합니다.

만약 프로그램이 복구되지 않은 panic으로 종료되거나, 치명적인 예외(세그멘테이션 위반, 0으로 나누기 등)가 발생하면 실행 중에 수행된 문장들의 프로파일 데이터가 손실됩니다.

#### `-coverpkg=main`을 사용하면 프로파일링을 위해 main 패키지가 선택되나요? {#mainpkg}

`-coverpkg` 플래그는 패키지 이름의 목록이 아니라 임포트 경로(import paths)의 목록을 받습니다. 커버리지 계측(instrumentation) 대상으로 `main` 패키지를 선택하려면, 이름이 아닌 임포트 경로로 지정하십시오. 예시 ([이 예제 프로그램](/play/p/VSQJN8xkkf-?v=gotip) 사용):

```
$ go list -m
mydomain.com
$ go build -coverpkg=main -o oops.exe .
warning: no packages being built depend on matches for pattern main
$ go build -coverpkg=mydomain.com -o myprogram.exe .
$ mkdir somedata
$ GOCOVERDIR=somedata ./myprogram.exe
I say "Hello, world." and "see ya"
$ go tool covdata percent -i=somedata
	mydomain.com	coverage: 100.0% of statements
$
```

## 리소스 {#resources}

- **Go 1.2의 유닛 테스트 커버리지를 소개하는 블로그 포스트**:
  - 유닛 테스트를 위한 커버리지 프로파일링이 Go 1.2 릴리스의 일부로 도입되었습니다. 자세한 내용은 [이 블로그 포스트](/blog/cover)를 참조하십시오.
- **문서**:
  - [`cmd/go`](https://pkg.go.dev/cmd/go) 패키지 문서는 커버리지와 관련된 빌드 및 테스트 플래그에 대해 설명합니다.
- **기술 세부 정보**:
  - [디자인 초안](/design/51430-revamp-code-coverage)
  - [제안서](/issue/51430)

## 용어집 {#glossary}

<a id="glos-unit-test"></a>
**unit test:** Go의 `testing` 패키지를 활용하여, 특정 Go 패키지와 연관된 `*_test.go` 파일 내에서 수행하는 테스트입니다.

<a id="glos-integration-test"></a>
**integration test (통합 테스트):** 특정 애플리케이션이나 바이너리에 대해 수행하는 더 포괄적이고 비중이 큰 테스트입니다. 통합 테스트는 일반적으로 프로그램 또는 프로그램 집합을 빌드한 다음, Go의 `testing` 패키지 기반 여부와 상관없이 테스트 하네스(test harness)의 제어 하에 다양한 입력값과 시나리오를 사용하여 해당 프로그램들을 여러 번 실행하는 과정을 포함합니다.
