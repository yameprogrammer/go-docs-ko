<!--
참고: 이 문서 및 이 디렉토리에 있는 다른 문서에서 일관된 규칙은 고정 폭 문자열을 사용하여 공백을 지정하는 것입니다. 예를 들어, `hello` `world`와 같이 사용합니다.
이러한 문자열에서 내부 태그를 제거하는 CL을 보내지 마세요.
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.10 소개 {#introduction}

가장 최신 Go 버전인 1.10은 [Go 1.9](go1.9) 이후 6개월 만에 출시되었습니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
항상과 마찬가지로, 이 릴리스는 Go 1의 [호환성 보장](/doc/go1compat.html)을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

이 릴리스는 [빌드된 패키지의 캐싱](#build)을 개선하고,
[성공적인 테스트 결과의 캐싱](#test)을 추가하며,
[테스트 중 자동으로 심층 검사를 실행](#test-vet)하고,
그리고
[Go와 C 간에 직접 문자열 값을 전달하도록 허용](#cgo).
새로운 [고정된 안전 컴파일러 옵션](#cgo)은 이전 릴리스로 성공적으로 빌드된 코드에서
예상치 못한 [`invalid
flag`](/s/invalidflag) 오류를 발생시킬 수 있습니다.

## 언어 변경 사항 {#language}

```
// Go code example
package main

import "fmt"

func main() {
	fmt.Println("Hello, world!")
}
```

언어 사양에 대한 주요 변경 사항은 없습니다.

<!-- CL 60230 -->
형 변환되지 않은 상수의 이동과 관련된 예외적인 경우에 대한 설명이 명확해졌으며, 그 결과 컴파일러는 인덱스 표현식 `x[1.0 << s]`를 허용하도록 업데이트되었습니다. 여기서 `s`는 부호 없는 정수입니다. 이는 이미 [go/types](/pkg/go/types/) 패키지에 포함되어 있었습니다.

<!-- CL 73233 -->
메서드 표현식의 문법이 업데이트되어, 수신자로 모든 타입 표현식을 허용하도록 구문을 완화했습니다.
이는 컴파일러가 이미 구현하던 방식과 일치합니다.
예를 들어, `struct{io.Reader}.Read`는 컴파일러가 이미 허용했던 유효하지만 특이한 메서드 표현식이며, 이제 언어 문법에 의해 허용됩니다.

## 포트

이 릴리스에는 새로운 지원되는 운영 체제 또는 프로세서 아키텍처가 없습니다.
대부분의 작업은 기존 포트에 대한 지원을 강화하는 데 집중되었습니다.
특히 [어셈블러의 새로운 명령어](#asm) 및 컴파일러에서 생성된 코드에 대한 개선 사항이 주요 내용입니다.

[공개된 Go 1.9 릴리스 노트](go1.9#freebsd)에 따르면,
Go 1.10에서는 FreeBSD 10.3 이상이 필요합니다;
FreeBSD 9.3에 대한 지원이 제거되었습니다.

Go는 이제 다시 NetBSD에서 실행되지만, 아직 출시되지 않은 NetBSD 8이 필요합니다.
`GOARCH`는 `amd64`와 `386`만 수정되었습니다. `arm` 포트는 아직 작동하지 않습니다.

32비트 MIPS 시스템에서 새로운 환경 변수 설정:
`GOMIPS=hardfloat` (기본값) 및
`GOMIPS=softfloat`은 하드웨어 명령 또는 소프트웨어 에뮬레이션을 사용하여 부동 소수점 계산을 수행할지 선택합니다.

Go 1.10은 OpenBSD 6.0에서만 실행 가능한 마지막 버전입니다.
Go 1.11은 OpenBSD 6.2를 필요로 합니다.

Go 1.10은 OS X 10.8 마운틴 라이온 또는 OS X 10.9 매버릭스에서 실행되는 마지막 버전입니다.
Go 1.11은 OS X 10.10 요세미트 또는 이후 버전이 필요합니다.

Go 1.10은 Windows XP 또는 Windows Vista에서 실행되는 마지막 버전입니다.
Go 1.11은 Windows 7 또는 그 이상 버전을 요구합니다.

## 도구 {#tools}

### 기본 GOROOT 및 GOTMPDIR {#goroot}

만약 환경 변수 `$GOROOT`가 설정되지 않은 경우,
`go` 도구는 이전에는 툴체인 컴파일 시 설정된 기본 `GOROOT`를 사용했습니다.
이제 기본값을 사용하기 전에, `go` 도구는 자체 실행 파일 경로에서 `GOROOT`를 추론하려고 시도합니다.
이를 통해 바이너리 배포본을 파일 시스템의 어느 곳에서나 추출하여 `GOROOT`를 명시적으로 설정하지 않고도 사용할 수 있습니다.

기본적으로, `go` 도구는 임시 파일과 디렉토리를 시스템의 임시 디렉토리에 생성합니다 (예: Unix 시스템의 `$TMPDIR`).
새로운 환경 변수 `$GOTMPDIR`이 설정되면, `go` 도구는 해당 디렉토리에 임시 파일과 디렉토리를 생성합니다.

### 빌드 및 설치 {#build}

`go build` 명령은 이제 컴파일된 패키지에 저장된 소스 파일의 내용, 지정된 빌드 플래그 및 메타데이터를 기반으로 최신 상태의 패키지를 감지합니다.
수정 시간은 더 이상 참조되지 않거나 관련이 없습니다.
수정 시간이 오해를 불러일으키는 경우 (예: 빌드 플래그의 변경) 재빌드를 강제로 수행하기 위해 `-a` 플래그를 추가하는 이전 방식은 더 이상 필요하지 않습니다.
이제 빌드는 항상 패키지가 재빌드되어야 하는지 감지합니다.
(그렇지 않은 경우, 버그를 신고해 주시기 바랍니다.)

`go` `build` 옵션 `-asmflags`, `-gcflags`, `-gccgoflags`, 및 `-ldflags`
이제 기본적으로 명령줄에 직접 나열된 패키지에만 적용됩니다.
예를 들어, `go` `build` `-gcflags=-m` `mypkg`
`mypkg`를 빌드할 때 컴파일러에 `-m` 플래그를 전달하지만, 해당 종속 패키지에는 전달하지 않습니다.
새로운, 보다 일반적인 형태인 `-asmflags=패턴=플래그` (그리고 다른 플래그에 대해서도 마찬가지)
`플래그`를 지정된 패턴과 일치하는 패키지에만 적용합니다.
예를 들어: `go` `install` `-ldflags=cmd/gofmt=-X=main.version=1.2.3` `cmd/...`
`cmd/...`와 일치하는 모든 명령을 설치하지만, `cmd/gofmt`에 대한 `-X` 옵션만 적용합니다.
자세한 내용은 [`go` `help` `build`](/cmd/go/#hdr-Compile_packages_and_dependencies)를 참조하십시오.

명령 `go build`는 `$GOROOT/pkg` 또는 `$GOPATH/pkg`에 설치된 패키지와 별도로, 최근 빌드된 패키지의 캐시를 유지합니다.
캐시의 효과는 명시적으로 패키지를 설치하지 않거나, 서로 다른 소스 코드의 복사본(예: 버전 관리 시스템에서 여러 브랜치를 번갈아 사용하는 경우) 간에 전환할 때 빌드 속도를 향상시키는 데 있습니다.

속도를 위해 `-i` 플래그를 추가하는 이전 권고(예: `go build -i` 또는 `go test -i`)는 더 이상 필요하지 않습니다. `-i` 플래그 없이도 빌드는 동일한 속도로 실행됩니다.

자세한 내용은 [`go` `help` `cache`](/cmd/go/#hdr-Build_and_test_caching)를 참조하십시오.

명령줄에 직접 나열된 패키지와 명령만 설치합니다.
예를 들어, `go install cmd/gofmt`는 `gofmt` 프로그램을 설치하지만, 의존하는 패키지는 설치하지 않습니다.
새로운 빌드 캐시는 향후 명령이 의존성이 설치된 것처럼 빠르게 실행되도록 합니다.
의존성을 강제로 설치하려면 새로운 `go install -i` 플래그를 사용하십시오.
일반적으로 의존성 패키지를 설치하는 것은 필요하지 않으며, 설치된 패키지의 개념은 향후 릴리스에서 사라질 수 있습니다.

많은 `go` 빌드 구현 세부 사항이 이러한 개선 사항을 지원하기 위해 변경되었습니다.
이러한 변경 사항에서 파생된 새로운 요구 사항은 다음과 같습니다.
바이너리 전용 패키지는 이제 링킹을 사용하여 프로그램을 링크할 때 해당 가져오기를 사용할 수 있도록, 스텁 소스 코드에 정확한 가져오기 블록을 선언해야 합니다.
자세한 내용은 [`go` `help` `filetype`](/cmd/go/#hdr-File_types)를 참조하십시오.

### 테스트 {#test}

`go test` 명령은 이제 테스트 결과를 캐싱합니다:
만약 테스트 실행 파일 및 명령줄이 이전 실행과 일치하고
그리고 그 실행에서 참조된 파일 및 환경 변수가 변경되지 않았다면, `go test`는
이전 테스트 출력을 출력하고, 실행 시간을 "(cached)"로 대체합니다.
테스트 캐싱은 성공적인 테스트 결과에만 적용됩니다;
`go test` 명령에만 적용되며,
명시적인 패키지 목록을 사용하는 명령에만 적용됩니다.
그리고 다음 테스트 플래그 중 일부를 사용하는 명령줄에만 적용됩니다:
`-cpu`, `-list`, `-parallel`,
`-run`, `-short`, `-v`
테스트 캐싱을 우회하는 일반적인 방법은 `-count=1`을 사용하는 것입니다.

명령 `go test`는 이제 테스트 중인 패키지에 대해 자동으로 `go vet`를 실행하여, 테스트를 실행하기 전에 중요한 문제를 식별합니다.
이러한 문제들은 빌드 오류처럼 처리되며, 테스트 실행을 방지합니다.
이 자동 검사는 사용 가능한 `go vet` 검사 중 신뢰도가 높은 부분만 활성화됩니다.
`go vet` 실행을 비활성화하려면 `go test -vet=off`를 사용하십시오.

`go test` 명령의 `-coverpkg` 플래그는 이제
각 테스트의 의존성에 대한 패턴 목록을 쉼표로 구분하여 해석합니다. 즉, 새로 로드할 패키스 목록이 아닌 것입니다.
예를 들어, `go test -coverpkg=all`은
테스트 패키지와 모든 의존성에 대한 커버된 테스트를 실행하는 데 유용한 방법입니다.
또한, `go test -coverprofile` 옵션은
여러 테스트를 실행할 때 지원됩니다.

실행 시간 초과로 인한 오류 발생 시, 테스트는 종료되기 전에 프로파일을 작성할 가능성이 더 높아졌습니다.

명령 `go test`는 이제 주어진 테스트 바이너리의 표준 출력 및 표준 오류를 항상 병합하고, 병합된 내용을 `go test`의 표준 출력으로 씁니다.
이전 버전에서는 `go test`가 이러한 병합을 주로 적용했습니다.

`go` 테스트 `-v` 출력
이제 `PAUSE` 및 `CONT` 상태 업데이트 라인을 포함하여, 병렬 테스트가 일시 중지되고 계속되는 시점을 표시합니다. ([병렬 테스트](/pkg/testing/#T.Parallel))

새로운 `go` `test` `-failfast` 플래그는, 어떤 테스트가 실패했을 때, 추가적인 테스트 실행을 중지합니다.
참고: 실패한 테스트와 병렬로 실행되는 테스트는 완료될 수 있습니다.

마지막으로, 새로운 `go` `test` `-json` 플래그는
새로운 명령 `go` `tool` `test2json`을 사용하여
테스트 결과 출력을 처리하여
테스트 실행의 기계 판독 가능한 JSON 형식의 설명을 생성합니다.
이를 통해 IDE 및 기타 도구에서
테스트 실행에 대한 풍부한 표현을 만들 수 있습니다.

자세한 내용은 다음을 참조하십시오.
[`go` `help` `test`](/cmd/go/#hdr-Test_packages)
및 [test2json 설명서](/cmd/test2json/).

### Cgo

`#cgo`를 사용하여 지정된 옵션 (예: `CFLAGS`)은 이제 허용된 옵션 목록에 대해 검사됩니다.
이를 통해 다운로드된 패키지가 컴파일러 옵션 (예:
`<span style="white-space: nowrap">`-fplugin`</span>)을 사용하여 빌드되는 머신에서 임의의 코드를 실행하는 보안 취약점을 해결합니다.
이로 인해 "유효하지 않은 플래그"와 같은 빌드 오류가 발생할 수 있습니다 (예: `#cgo CFLAGS`에서 유효하지 않은 플래그).
자세한 내용 및 이 오류를 처리하는 방법에 대한 정보는 다음 링크를 참조하십시오:
[https://golang.org/s/invalidflag](/s/invalidflag).

Cgo는 이제 Go 타입 별칭을 사용하여 C typedef와 유사한 것을 구현합니다 (예: `"typedef` `X` `Y"`).
따라서 Go 코드는 `C.X` 및 `C.Y` 유형을 상호 교환하여 사용할 수 있습니다.
또한, niladic 함수와 유사한 매크로 사용도 지원합니다.
또한, 문서가 업데이트되어 cgo로 내보낸 함수의 타입 서명에는 Go 구조체 및 Go 배열이 지원되지 않는다는 점이 명확하게 설명되었습니다.

Cgo는 이제 C에서 직접 Go 문자열 값에 액세스할 수 있습니다.
C 프레임워크 내의 함수는 `_GoString_` 유형을 사용하여 Go 문자열을 인수로 받을 수 있습니다.
C 코드는 문자열의 내용을 직접 액세스하기 위해 `_GoStringLen` 및 `_GoStringPtr`를 호출할 수 있습니다.
`_GoString_` 유형의 값은 Go 유형 `string` 인수를 취하는 내보낸 Go 함수 호출에 전달될 수 있습니다.

툴체인 초기화 과정에서, 환경 변수 `CC` 및 `CC_FOR_TARGET`는 결과적으로 생성될 툴체인이 호스트 및 타겟 빌드에 각각 사용할 기본 C 컴파일러를 지정합니다.
그러나 툴체인이 여러 타겟과 함께 사용되는 경우, 각 타겟에 대해 다른 C 컴파일러를 지정해야 할 수 있습니다 (예: `darwin/arm64`와 `linux/ppc64le`에 대해 다른 컴파일러).
새로운 환경 변수 세트 `<code>CC_FOR_<goos>_<goarch>_</code>`는 각 타겟에 대해 다른 기본 C 컴파일러를 지정할 수 있도록 합니다.
참고: 이러한 변수는 툴체인 초기화 단계에서만 적용되며, 결과적으로 생성된 툴체인이 사용할 기본값을 설정합니다.
나중에 사용되는 `go build` 명령어는 `CC` 환경 변수를 사용하거나, 기본값을 사용합니다.

Cgo는 이제 일반적으로 Go의 `pointer` 타입에 매핑되는 일부 C 타입을 `uintptr` 타입으로 변환합니다. 이러한 타입에는 다음이 포함됩니다.
* Darwin의 CoreFoundation 프레임워크의 `CFTypeRef` 계층 구조
* Java의 JNI 인터페이스의 `jobject` 계층 구조

이 유형은 Go 측에서 `uintptr`이어야 합니다. 그렇지 않으면 Go 가비지 컬렉터를 혼란스럽게 만들 수 있습니다. 때로는 실제로 포인터가 아니라, 포인터 크기의 정수로 인코딩된 데이터 구조일 수 있습니다. Go 메모리에 대한 포인터는 이러한 `uintptr` 값에 저장해서는 안 됩니다.

이 변경 사항 때문에, 영향을 받는 유형의 값은 상수가 아닌 `0`으로 초기화해야 합니다. `nil` 대신. Go 1.10은 이러한 변경 사항을 지원하기 위한 `gofix` 모듈을 제공합니다:

```
go tool fix -r cftype <pkg>
	go tool fix -r jni <pkg>
```

자세한 내용은 [cgo 문서]( /cmd/cgo/)를 참조하십시오.

### 문서 {#doc}

`go` `doc` 도구가 이제 `T` 또는 `*T` 슬라이스를 반환하는 함수를 `T` 유형의 표시 결과에 추가합니다. 이는 기존에 `T` 또는 `*T` 단일 결과만 반환하는 함수에 대해 동작하는 방식과 동일합니다.
예를 들어:

```markdown
$ go doc mail.Address
	패키지 mail // import "net/mail"
```

```markdown
```go
type Address struct {
	Name    string
	Address string
}

Address represents a single mail address.
```

```markdown
```
```go
func ParseAddress(address string) (*Address, error)
	func ParseAddressList(list string) ([]*Address, error)
	func (a *Address) String() string
```

이전에는 `ParseAddressList`가 패키지 개요(`go` `doc` `mail`)에서만 표시되었습니다.

### 해결 {#fix}

`go fix` 도구는 `"golang.org/x/net/context"`의 가져오기를 `"context"`로 대체합니다.
(이전의 포워딩 별칭은 Go 1.9 이상 버전에서 사용될 때 완전히 동일하게 만듭니다.)

### 가져오기 {#get}

`go` `get` 명령어는 이제 Fossil 소스 코드 저장소를 지원합니다.

### Pprof {#pprof}

`runtime/pprof` 패키지가 생성하는 블로킹 및 뮤텍스 프로파일은 이제 심볼 정보를 포함하므로, 프로파일을 생성한 바이너리 파일 없이 `go` 도구의 `pprof`를 사용하여 확인할 수 있습니다.
(다른 모든 프로파일 유형은 Go 1.9에서 심볼 정보를 포함하도록 변경되었습니다.)

[`go` 도구 `pprof`](/cmd/pprof/)
프로파일 시각화 도구가 git 버전 9e20b5b (2017-11-08)로 업데이트되었습니다.
[github.com/google/pprof](https://github.com/google/pprof)에서 제공되며, 업데이트된 웹 인터페이스를 포함합니다.

### 수의사 {#vet}

명령 [`go`&nbsp;`vet`](/cmd/vet/)는 패키지를 확인하는 동안, cgo 또는 벤더된 가져오기를 사용하는 패키지라도 완전하고 최신 정보를 항상 사용할 수 있습니다.
이로 인해 보고서는 더욱 정확해집니다.
참고: `go`&nbsp;`vet`만 이 정보를 사용할 수 있습니다.
더 낮은 수준의 `go`&nbsp;`tool`&nbsp;`vet`은 사용할 필요가 없으며, `vet` 자체를 개발할 때만 사용해야 합니다.
(Go 1.9부터, `go`&nbsp;`vet`은 `go`&nbsp;`tool`&nbsp;`vet`과 동일한 모든 플래그에 액세스할 수 있습니다.)

### 진단 {#diag}

이 릴리스에는 사용 가능한 Go 프로그램 진단 도구에 대한 새로운 개요가 포함되어 있습니다. ([개요](/doc/diagnostics.html))

### Gofmt {#gofmt}

다음은 Go 소스 코드의 기본 형식에 대한 두 가지 작은 변경 사항입니다.

첫째, 복잡한 세 개의 인덱스 슬라이스 표현식 (`x[i+1`&nbsp;`:`&nbsp;`j:k]`)이 이전에는 다음과 같이 형식화되었지만 이제는 다음과 같이 더욱 일관성 있는 공백을 사용합니다: `x[i+1`&nbsp;`:`&nbsp;`j`&nbsp;`:`&nbsp;`k]`.

둘째, 단일 줄에 작성된 단일 메서드 인터페이스 리터럴(특히 타입 추론에 사용되는 경우)이 더 이상 여러 줄로 분리되지 않습니다.

이러한 gofmt의 미세 업데이트는 때때로 발생할 수 있습니다.
일반적으로, 특정 버전의 gofmt 출력과 일치하는지 확인하는 시스템을 구축하는 것을 권장하지 않습니다.
예를 들어, 저장소에 이미 체크인된 코드 중 "적절하게 포맷되지 않은" 코드가 발견될 경우 실패하는 지속적 통합 테스트는 본질적으로 불안정하며 권장되지 않습니다.

만약 여러 프로그램이 소스 파일의 형식을 지정하는 데 사용될 gofmt 버전에 대해 합의해야 하는 경우,
다음과 같이 동일한 gofmt 실행 파일을 호출하도록 구성하는 것이 좋습니다.
예를 들어, Go 오픈 소스 저장소에서, 우리의 Git 사전 커밋 훅은 Go로 작성되었으며 `go/format`을 직접 가져올 수 있지만, 대신 현재 경로에 있는 `gofmt` 실행 파일을 호출합니다.
따라서 사전 커밋 훅을 매번 `gofmt`가 변경될 때마다 다시 컴파일할 필요가 없습니다.

### 컴파일러 도구 체인 {#compiler}

컴파일러는 지원되는 아키텍처에 걸쳐 성능이 향상된 생성 코드에 대한 많은 개선 사항을 포함합니다.

디버깅 정보(DWARF)가 바이너리에 기록되는 방식이 다음과 같이 개선되었습니다:
* 상수 값들이 이제 기록됩니다.
* 라인 번호 정보가 더 정확해져 프로그램의 소스 레벨에서 디버깅이 더 잘 작동합니다.
* 각 패키지는 이제 자체 DWARF 컴파일 단위로 표시됩니다.

다양한 [빌드 모드](https://docs.google.com/document/d/1nr-TQHw_er6GOQRsF6T43GGhFDelrAP0NqSS_00RgZQ/edit)가 더 많은 시스템으로 포트되었습니다.
특히, `c-shared`은 이제 `linux/ppc64le`, `windows/386`, 및 `windows/amd64`에서 작동합니다.
`pie`는 이제 `darwin/amd64`에서 작동하며, 모든 시스템에서 외부 링크 사용을 강제합니다.
그리고 `plugin`은 이제 `linux/ppc64le` 및 `darwin/amd64`에서 작동합니다.

`linux/ppc64le` 포트에 대한 호환성은 이제 cgo를 사용하는 모든 프로그램에서 외부 링크를 사용해야 합니다. 여기에는 표준 라이브러리에서 사용되는 프로그램도 포함됩니다.

### 어셈블러 {#asm}

ARM 32비트 포트의 어셈블러는 이제 다음 명령어들을 지원합니다:
<code><small>BFC</small></code>,
<code><small>BFI</small></code>,
<code><small>BFX</small></code>,
<code><small>BFXU</small></code>,
<code><small>FMULAD</small></code>,
<code><small>FMULAF</small></code>,
<code><small>FMULSD</small></code>,
<code><small>FMULSF</small></code>,
<code><small>FNMULAD</small></code>,
<code><small>FNMULAF</small></code>,
<code><small>FNMULSD</small></code>,
<code><small>FNMULSF</small></code>,
<code><small>MULAD</small></code>,
<code><small>MULAF</small></code>,
<code><small>MULSD</small></code>,
<code><small>MULSF</small></code>,
<code><small>NMULAD</small></code>,
<code><small>NMULAF</small></code>,
<code><small>NMULD</small></code>,
<code><small>NMULF</small></code>,
<code><small>NMULSD</small></code>,
<code><small>NMULSF</small></code>,
<code><small>XTAB</small></code>,
<code><small>XTABU</small></code>,
<code><small>XTAH</small></code>,
그리고
<code><small>XTAHU</small></code>.

ARM 64비트 포트용 어셈블러는 이제 다음 명령어를 지원합니다.
<code><small>VADD</small></code>,
<code><small>VADDP</small></code>,
<code><small>VADDV</small></code>,
<code><small>VAND</small></code>,
<code><small>VCMEQ</small></code>,
<code><small>VDUP</small></code>,
<code><small>VEOR</small></code>,
<code><small>VLD1</small></code>,
<code><small>VMOV</small></code>,
<code><small>VMOVI</small></code>,
<code><small>VMOVS</small></code>,
<code><small>VORR</small></code>,
<code><small>VREV32</small></code>,
및
<code><small>VST1</small></code>
명령어.

PowerPC 64비트 포트의 경우, 어셈블러는 이제 다음 POWER9 명령어를 지원합니다:
<code><small>ADDEX</small></code>,
<code><small>CMPEQB</small></code>,
<code><small>COPY</small></code>,
<code><small>DARN</small></code>,
<code><small>LDMX</small></code>,
<code><small>MADDHD</small></code>,
<code><small>MADDHDU</small></code>,
<code><small>MADDLD</small></code>,
<code><small>MFVSRLD</small></code>,
<code><small>MTVSRDD</small></code>,
<code><small>MTVSRWS</small></code>,
<code><small>PASTECC</small></code>,
<code><small>VCMPNEZB</small></code>,
<code><small>VCMPNEZBCC</small></code>,
및
<code><small>VMSUMUDM</small></code>.

S390X 포트용 어셈블러는 이제 다음 명령어를 지원합니다:
<code><small>TMHH</small></code>,
<code><small>TMHL</small></code>,
<code><small>TMLH</small></code>,
그리고
<code><small>TMLL</small></code>
명령어.

X86 64비트 포트용 어셈블러는 이제 AVX, AVX2, BMI, BMI2, F16C, FMA3, SSE2, SSE3, SSSE3, SSE4.1, SSE4.2 확장 세트 포함하여 359개의 새로운 명령어를 지원합니다.
또한, 어셈블러는 `<code><small>MOVL</small></code>&nbsp;<code><small>$0,</small></code>&nbsp;<code><small>AX</small></code>`를 `<code><small>XORL</small></code>` 명령어로 구현하지 않도록 변경하여, 조건 플래그를 예상치 않게 지우는 것을 방지합니다.

### Gccgo {#gccgo}

Go의 반기별 릴리즈 일정과 GCC의 연간 릴리즈 일정이 일치하기 때문에,
GCC 7에는 Go 1.8.3 버전의 gccgo가 포함되어 있습니다.
다음 릴리즈인 GCC 8에는 Go 1.10 버전의 gccgo가 포함될 것으로 예상합니다.

## 실행 시점 {#runtime}

`LockOSThread` 및 `UnlockOSThread` 함수의 중첩 호출 동작이 변경되었습니다.
이 함수들은 goroutine이 특정 운영체제 스레드에 묶여 있는지 제어하여, goroutine은 해당 스레드에서만 실행되고, 스레드는 해당 goroutine만 실행되도록 합니다.
이전에는 `LockOSThread`를 연속적으로 여러 번 호출하는 것은 한 번 호출하는 것과 동일했고, 단일 `UnlockOSThread` 호출은 항상 스레드를 해제했습니다.
이제 호출이 중첩됩니다. 즉, `LockOSThread`가 여러 번 호출되면, 스레드를 해제하기 위해 `UnlockOSThread`도 동일한 횟수만큼 호출해야 합니다.
이러한 호출을 중첩하지 않도록 주의하여 작성된 기존 코드는 그대로 유효하게 유지됩니다.
잘못 `LockOSThread` 및 `UnlockOSThread`가 중첩된다고 가정하여 작성된 기존 코드는 올바르게 동작하게 됩니다.
대부분의 공개 Go 소스 코드에서 이러한 함수를 사용하는 경우, 이 두 번째 범주에 속합니다.

`LockOSThread` 및 `UnlockOSThread`의 일반적인 사용법 중 하나는 Go 코드가 특정 스레드(예: Linux 또는 Plan 9 네임스페이스)의 스레드 로컬 상태를 안정적으로 수정할 수 있도록 하는 것입니다.
따라서 런타임은 잠긴 스레드를 재사용하거나 새 스레드를 만드는 데 사용하기에 적합하지 않다고 처리합니다.

스택 추적에는 더 이상 암시적인 래퍼 함수(이전에는 `<autogenerated>`으로 표시됨)가 포함되지 않습니다.
단, 래퍼 자체에서 오류 또는 패닉이 발생하는 경우에만 그렇습니다.
따라서 `Caller`와 같은 함수에 전달되는 건너뛰기 개수는 이제 작성된 코드의 구조와 일치해야 합니다.
최적화 결정 및 구현 세부 사항에 의존하는 대신.

쓰레기 수거기는 할당 지연에 미치는 영향을 줄이기 위해 수정되었습니다.
이제 전체 CPU 사용량이 줄었지만, 더 자주 실행될 수 있습니다.
쓰레기 수거기가 사용하는 총 CPU 사용량은 크게 변하지 않았습니다.

[`GOROOT`](/pkg/runtime/#GOROOT) 함수
이제 `$GOROOT` 환경 변수가 설정되지 않은 경우
(호출 프로그램이 컴파일될 때의) `GOROOT` 또는 `GOROOT_FINAL` 값으로 기본 설정됩니다.
이전에는 호출 프로그램이 컴파일된 도구 체인의 `GOROOT` 또는 `GOROOT_FINAL` 값을 사용했습니다.

[`GOMAXPROCS`](/pkg/runtime/#GOMAXPROCS) 설정에 더 이상 제한이 없습니다.
(Go 1.9에서는 제한이 1024였습니다.)

## 성능 {#performance}

물론, 변경 사항이 너무 광범위하고 다양하여 정확한 성능에 대한 진술을 내리는 것은 어렵습니다. 대부분의 프로그램은 가비지 컬렉터의 속도 향상, 더 나은 생성된 코드 및 핵심 라이브러리의 최적화를 통해 약간 더 빠르게 실행될 것으로 예상됩니다.

## 가비지 컬렉터 {#gc}

이 문서는 Go 언어의 가비지 컬렉터에 대한 정보를 제공합니다.

많은 애플리케이션은 가비지 컬렉터가 활성화될 때 상당한 낮은 할당 지연 시간과 전반적인 성능 오버헤드를 경험할 것입니다.

## 표준 라이브러리 {#library}

표준 라이브러리에 대한 모든 변경 사항은 미미합니다.
[bytes](#bytes) 및 [net/url](#net/url)에 대한 변경 사항은 기존 프로그램의 업데이트가 가장 가능성이 높습니다.

### 라이브러리의 미세 조정 {#minor_library_changes}

항상, 라이브러리에는 다양한 작은 변경 사항 및 업데이트가 있으며, 이는 Go 1의 [호환성](/doc/go1compat)을 염두에 두고 이루어졌습니다.

#### [archive/tar](/pkg/archive/tar/)

일반적으로, 특수 헤더 형식의 처리가 크게 개선되고 확장되었습니다.

[`FileInfoHeader`](/pkg/archive/tar/#FileInfoHeader)는 항상
`os.FileInfo`](/pkg/os/#FileInfo) 인수로 전달된 Unix UID 및 GID 번호를
(`FileInfo`의 `Sys` 메서드가 반환하는 시스템에 따라 다른 정보를 기반으로)
반환되는 [`Header`](/pkg/archive/tar/#Header)에 기록합니다.
이제 해당 ID에 해당하는 사용자 및 그룹 이름을, 그리고 장치 파일의 주요 및 부 장치 번호를
또한 기록합니다.

새로운 `[`Header.Format`](/pkg/archive/tar/#Header) 필드
의 유형은 `Format`](/pkg/archive/tar/#Format) 입니다.
`Writer`](/pkg/archive/tar/#Writer) 가 사용하는 tar 헤더 형식을 제어합니다.
기본값은 이전과 같이, 헤더에 필요한 필드를 인코딩할 수 있는 가장 널리 지원되는 헤더 형식을 선택하는 것입니다 (가능하면 USTAR, 그렇지 않으면 PAX, 그렇지 않으면 GNU).
`Reader`](/pkg/archive/tar/#Reader) 는 읽은 각 헤더에 대해 `Header.Format`을 설정합니다.

`Reader` 및 `Writer`는 이제 임의의 PAX 레코드를 지원하며,
새로운 [`Header.PAXRecords`](/pkg/archive/tar/#Header) 필드를 사용하여,
기존의 `Xattrs` 필드의 일반화된 기능을 제공합니다.

`Reader`는 이제 GNU 헤더 파일 이름 또는 링크 이름을 유효한 UTF-8로 유지해야 한다는 규칙을 더 이상 적용하지 않습니다.

PAX- 또는 GNU 형식의 헤더를 작성할 때, `Writer`는 이제 `Header.AccessTime` 및 `Header.ChangeTime` 필드를 포함합니다 (설정된 경우).
PAX 형식의 헤더를 작성할 때, 시간 값에는 소수점 이하의 정밀도가 포함됩니다.

#### [archive/zip](/pkg/archive/zip/)

Go 1.10은 ZIP 아카이브에서 시간 및 문자 집합 인코딩에 대한 보다 완전한 지원을 추가합니다.

원래 ZIP 형식은 년, 월, 일, 시간, 분, 초를 두 개의 16비트 값에 있는 필드에 MS-DOS 표준 인코딩 방식으로 표현했습니다.
이 인코딩 방식으로는 시간대나 홀수 초를 표현할 수 없으므로, 더 풍부한 인코딩을 허용하기 위해 여러 확장 기능이 도입되었습니다.
Go 1.10에서는 [`Reader`](/pkg/archive/zip/#Reader) 및 [`Writer`](/pkg/archive/zip/#Writer)가 널리 사용되는 Info-Zip 확장 기능을 지원하여 시간을 별도로 32비트 Unix "epoch 이후의 초" 형식으로 인코딩합니다.
[`FileHeader`](/pkg/archive/zip/#FileHeader)의 새로운 `Modified` 필드 (형식: [`time.Time`](/pkg/time/#Time))는 `ModifiedTime` 및 `ModifiedDate` 필드를 대체하며, 이 필드들은 여전히 MS-DOS 인코딩을 유지합니다.
`Reader` 및 `Writer`는 이제 ZIP 아카이브가 시간대 독립적인 Unix 시간을 저장하는 경우, 해당 로컬 시간을 MS-DOS 필드에 저장하여 시간대 오프셋을 유추할 수 있도록 하는 일반적인 관례를 따릅니다.
호환성을 위해 [`ModTime`](/pkg/archive/zip/#FileHeader.ModTime) 및 [`SetModTime`](/pkg/archive/zip/#FileHeader.SetModTime) 메서드는 이전 버전과 동일하게 작동합니다. 새로운 코드는 `Modified` 필드를 직접 사용해야 합니다.

각 ZIP 파일의 헤더에는 파일 이름 및 주석 필드가 UTF-8로 인코딩되었는지 여부를 나타내는 플래그 비트가 있습니다. 이는 시스템별 기본 인코딩 대신 UTF-8로 인코딩되었음을 나타냅니다.

Go 1.8 및 이전 버전에서는 `Writer`가 UTF-8 비트를 설정하지 않았습니다.
Go 1.9에서는 `Writer`가 UTF-8 비트를 거의 항상 설정하도록 변경되었습니다.
이는 Shift-JIS 파일 이름을 포함하는 ZIP 아카이브 생성을 중단시켰습니다.
Go 1.10에서는 `Writer`가 이제 이름과 주석 필드 모두가 유효한 UTF-8이고 적어도 하나가 비 ASCII인 경우에만 UTF-8 비트를 설정합니다.
비 ASCII 인코딩은 매우 드물게 유효한 UTF-8과 유사하게 나타나므로, 새로운 휴리스틱은 거의 항상 정확해야 합니다.
`FileHeader`의 새로운 `NonUTF8` 필드를 true로 설정하면 해당 파일에 대한 휴리스틱을 완전히 비활성화합니다.

`Writer`는 이제 중앙 디렉토리의 기록의 주석 필드를 설정할 수 있도록, `Writer`의 새로운 [`SetComment`](/pkg/archive/zip/#Writer.SetComment) 메서드를 호출하여 이를 수행할 수 있습니다.

#### [bufio](/pkg/bufio/)

새로운 [`Reader.Size`](/pkg/bufio/#Reader.Size)
및 [`Writer.Size`](/pkg/bufio/#Writer.Size)
메서드는 `Reader` 또는 `Writer`의 내부 버퍼 크기를 보고합니다.

#### [bytes](/pkg/bytes/)

[`Fields`](/pkg/bytes/#Fields),
[`FieldsFunc`](/pkg/bytes/#FieldsFunc),
[`Split`](/pkg/bytes/#Split),
및
[`SplitAfter`](/pkg/bytes/#SplitAfter)
함수는 항상 입력의 부분 슬라이스를 반환합니다.
Go 1.10에서는 반환되는 각 부분 슬라이스의 용량을 해당 길이와 동일하게 변경하여, 원래 입력의 인접한 데이터를 덮어쓰지 않도록 합니다.

#### [crypto/cipher](/pkg/crypto/cipher/)

[`NewOFB`](/pkg/crypto/cipher/#NewOFB)는 이제 잘못된 길이의 초기화 벡터를 제공받을 경우 패닉을 발생시킵니다. 이는 패키지 내의 다른 생성자와 마찬가지로 항상 발생합니다.
(이전에는 nil `Stream` 구현을 반환했습니다.)

#### [crypto/tls](/pkg/crypto/tls/)

TLS 서버는 이제 TLS 1.2를 사용할 때 SHA-512 서명을 지원한다고 광고합니다.
서버는 이미 서명을 지원했지만, 일부 클라이언트는 이를 명시적으로 광고하지 않는 경우 선택하지 않았습니다.

#### [crypto/x509](/pkg/crypto/x509/)

[`Certificate.Verify`](/pkg/crypto/x509/#Certificate.Verify)
이제 인증서에 포함된 모든 이름에 대한 이름 제약 조건을 적용하며, 클라이언트가 요청한 이름 하나뿐만 아니라 모든 이름을 검사합니다.
확장된 키 사용 제한도 동일하게 한 번에 확인합니다.
따라서 인증서가 유효성 검사된 후에는 이제 전체적으로 신뢰할 수 있습니다.
추가 이름이나 키 사용에 대해 인증서를 재검사할 필요가 없습니다.

다음(`Certificate[/pkg/crypto/x509/#Certificate]`) 필드인 `URIs`, `PermittedIPRanges`, `ExcludedIPRanges`, `PermittedEmailAddresses`, `ExcludedEmailAddresses`, `PermittedURIDomains`, 및 `ExcludedURIDomains`을 사용하여, 파싱된 인증서도 이제 URI 이름과 IP, 이메일, URI 제약 조건을 보고합니다.
유효하지 않은 값을 가진 인증서는 이제 거부됩니다.

새로운 `MarshalPKCS1PublicKey` 및 `ParsePKCS1PublicKey` 함수는 RSA 공개 키를 PKCS#1 형식으로 변환합니다.

새로운 [`MarshalPKCS8PrivateKey`](/pkg/crypto/x509/#MarshalPKCS8PrivateKey)
함수는 개인 키를 PKCS#8 형식으로 변환합니다.
([`ParsePKCS8PrivateKey`](/pkg/crypto/x509/#ParsePKCS8PrivateKey)
는 Go 1부터 존재했습니다.)

#### [crypto/x509/pkix](/pkg/crypto/x509/pkix/)

[`Name`](/pkg/crypto/x509/pkix/#Name)가 이제
[`String`](/pkg/crypto/x509/pkix/#Name.String) 메서드를 구현하여
X.509 구별 이름을 표준 RFC 2253 형식으로 포맷합니다.

#### [database/sql/driver](/pkg/database/sql/driver/)

현재 `[`driver.Rows.Next`](/pkg/database/sql/driver/#Rows.Next)에서 제공하는 대상 버퍼를 사용하는 드라이버는 해당 호출 이후 대상 배열에 할당된 버퍼에 더 이상 쓰지 않도록 해야 합니다.
드라이버는 `[`driver.Rows`](/pkg/database/sql/driver/#Rows)를 닫을 때, 내부 버퍼가 수정되지 않도록 주의해야 합니다.

드라이버가 자신의 클라이언트를 위해 [`sql.DB`](/pkg/database/sql/#DB)를 생성하고 싶다면,
[`Connector`](/pkg/database/sql/driver/#Connector) 인터페이스를 구현하고
새로운 [`sql.OpenDB`](/pkg/database/sql/#OpenDB) 함수를 호출할 수 있습니다.
이를 통해, 모든 구성을 문자열로 인코딩하여 [`sql.Open`](/pkg/database/sql/#Open)에 전달하는 대신,
직접 설정할 수 있습니다.

드라이버가 `sql.DB`에 대한 구성 문자열을 한 번만 파싱하도록 하고 싶을 때,
`sql.Conn`에 대한 파싱 대신,
또는 각 `sql.Conn`의 기본 컨텍스트에 접근하고 싶을 때,
들은 자신들의 [`Driver`](/pkg/database/sql/driver/#Driver)
구현이 [`DriverContext`](/pkg/database/sql/driver/#DriverContext)의 새로운 `OpenConnector` 메서드를 구현하도록 할 수 있습니다.

드라이버가 [`ExecerContext`](/pkg/database/sql/driver/#ExecerContext)을 구현하는 경우,
더 이상 [`Execer`](/pkg/database/sql/driver/#Execer)을 구현할 필요가 없습니다.
마찬가지로, [`QueryerContext`](/pkg/database/sql/driver/#QueryerContext)를 구현하는 드라이버는
더 이상 [`Queryer`](/pkg/database/sql/driver/#Queryer)를 구현할 필요가 없습니다.
이전에는 컨텍스트 기반 인터페이스가 구현되어 있어도,
컨텍스트 기반 인터페이스가 구현되지 않은 경우 무시되었습니다.

운전자가 캐시된 드라이버 연결을 순차적으로 사용하여 다른 클라이언트를 더 잘 분리할 수 있도록 하기 위해,
만약 [`Conn`](/pkg/database/sql/driver/#Conn)이 새로운
[`SessionResetter`](/pkg/database/sql/driver/#SessionResetter] 인터페이스를 구현하면,
`database/sql`은 `Conn`을 새로운 클라이언트에 재사용하기 전에 `ResetSession`을 호출합니다.

#### [debug/elf](/pkg/debug/elf/)

이 릴리스는 다음 유형의 리로케이션 상수를 348개 추가합니다.
[`R_386`](/pkg/debug/elf/#R_386),
[`R_AARCH64`](/pkg/debug/elf/#R_AARCH64),
[`R_ARM`](/pkg/debug/elf/#R_ARM),
[`R_PPC64`](/pkg/debug/elf/#R_PPC64),
그리고
[`R_X86_64`](/pkg/debug/elf/#R_X86_64).

#### [debug/macho](/pkg/debug/macho/)

Go 1.10 버전에서 Mach-O 섹션에서 위치 정보를 읽는 기능이 추가되었습니다.
`[`Section`](/pkg/debug/macho#Section) 구조체의 새로운 `Relocs` 필드와 새로운 `[`Reloc`](/pkg/debug/macho/#Reloc),
`[`RelocTypeARM`](/pkg/debug/macho/#RelocTypeARM),
`[`RelocTypeARM64`](/pkg/debug/macho/#RelocTypeARM64),
`[`RelocTypeGeneric`](/pkg/debug/macho/#RelocTypeGeneric),
그리고
`[`RelocTypeX86_64`](/pkg/debug/macho/#RelocTypeX86_64)
형식과 관련된 상수를 사용합니다.

Go 1.10 또한 `LC_RPATH` 로드 명령에 대한 지원을 추가합니다.
이는 다음 유형으로 표현됩니다.
[`RpathCmd`](/pkg/debug/macho/#RpathCmd) 및
[`Rpath`](/pkg/debug/macho/#Rpath),
그리고 헤더에 있는 다양한 플래그 비트에 대한 새로운 [명명된 상수](/pkg/debug/macho/#pkg-constants)가 추가되었습니다.

#### [encoding/asn1](/pkg/encoding/asn1/)

[`Marshal`](/pkg/encoding/asn1/#Marshal)가 이제 별표가 포함된 문자열을 `UTF8String` 유형으로 올바르게 인코딩합니다. 대신, 문자열이 `PrintableString` 유형을 강제하는 구조체 필드 내에 있는 경우에만 `PrintableString` 유형으로 인코딩됩니다.
`Marshal`는 `application` 지침이 포함된 구조체 태그도 이제 준수합니다.

새로운 [`MarshalWithParams`](/pkg/encoding/asn1/#MarshalWithParams)
함수는 추가 파라미터를 해당 구조체 필드 태그와 연관된 것처럼 처리합니다.

[`Unmarshal`](/pkg/encoding/asn1/#Unmarshal)는 이제 `explicit` 및 `tag` 지시어를 사용하여
구조 필드 태그를 준수합니다.

`Marshal` 및 `Unmarshal` 메서드는 이제 새로운 구조체 필드 태그를 지원합니다.
`numeric`, 이 태그는 ASN.1 NumericString을 나타냅니다.

#### [encoding/csv](/pkg/encoding/csv/)

[`Reader`](/pkg/encoding/csv/#Reader)는 이제 다음과 같은 의미 없는 `Comma` 및 `Comment` 설정의 사용을 금지합니다.
* NUL, 캐리지 리턴, 줄 바꿈, 유효하지 않은 라인, 유니코드 대체 문자
* `Comma` 및 `Comment`를 서로 동일하게 설정

만약 여러 입력 줄에 걸쳐 CSV 레코드로 발생하는 구문 오류가 발생하면, `Reader`는 이제 [`ParseError`](/pkg/encoding/csv/#ParseError)의 새로운 `StartLine` 필드에 레코드가 시작된 줄을 보고합니다.

#### [encoding/hex](/pkg/encoding/hex/)

새로운 함수
[`NewEncoder`](/pkg/encoding/hex/#NewEncoder)
및
[`NewDecoder`](/pkg/encoding/hex/#NewDecoder)
은 16진수 형식으로의 스트리밍 변환을 제공하며, 이는 이미
[encoding/base32](/pkg/encoding/base32/)
및
[encoding/base64](/pkg/encoding/base64/)
에 존재하는 해당 함수와 유사합니다.

`Decode` 및 `DecodeString` 함수가 잘못된 입력을 만나면,
이제 오류와 함께 이미 변환된 바이트 수를 반환합니다.
이전에는 어떤 오류가 발생하더라도 항상 0이라는 값을 반환했습니다.

#### [encoding/json](/pkg/encoding/json/)

[`Decoder`](/pkg/encoding/json/#Decoder)
새로운 메서드
[`DisallowUnknownFields`](/pkg/encoding/json/#Decoder.DisallowUnknownFields)
을 추가하여, 알 수 없는 JSON 필드가 있는 입력을 디코딩 오류로 보고합니다.
(기본 동작은 항상 알 수 없는 필드를 버리는 것이었습니다.)

결과적으로 [반사 기능 버그를 수정했으므로](#reflect),
[`Unmarshal`](/pkg/encoding/json/#Unmarshal)
더 이상 내장된 포인터 내의, 비공개 구조 유형의 필드에 디코딩할 수 없습니다.
이는 `Unmarshal`이 비공개 내장 포인터를 새로운 저장 위치를 가리키도록 초기화할 수 없기 때문입니다.
`Unmarshal`은 이제 이 경우 오류를 반환합니다.

#### [encoding/pem](/pkg/encoding/pem/)

[`Encode`](/pkg/encoding/pem/#Encode)
과
[`EncodeToMemory`](/pkg/encoding/pem/#EncodeToMemory)
는 더 이상, PEM 데이터로 인코딩할 수 없는 블록을 제시받을 때 불완전한 출력을 생성하지 않습니다.

```
#### [encoding/xml](/pkg/encoding/xml/)
```

새로운 함수
[`NewTokenDecoder`](/pkg/encoding/xml/#NewTokenDecoder)
은
[`NewDecoder`](/pkg/encoding/xml/#NewDecoder)
과 유사하지만, XML 형식의 바이트 스트림 대신
[`TokenReader`](/pkg/encoding/xml/#TokenReader)
에서 읽는 디코더를 생성합니다.
이는 클라이언트 라이브러리에서 XML 스트림 변환기를 구성하는 데 사용하도록 설계되었습니다.

#### [flag](/pkg/flag/)

기본
[`Usage`](/pkg/flag/#Usage) 함수는 이제
`CommandLine.Output()`로
첫 번째 줄의 출력을 출력하도록 변경되었으며,
`os.Stderr`를 가정하는 대신,
`CommandLine.SetOutput`을 사용하는 클라이언트에게
사용법 메시지를 올바르게 리디렉션합니다.

[`PrintDefaults`](/pkg/flag/#PrintDefaults)는 이제
플래그 사용 문자열의 새 줄 다음에 적절한 들여쓰기를 추가하여,
여러 줄로 구성된 사용 문자열이 보기 좋게 표시되도록 합니다.

[`FlagSet`](/pkg/flag/#FlagSet)는 새 메서드를 추가합니다.
[`ErrorHandling`](/pkg/flag/#FlagSet.ErrorHandling),
[`Name`](/pkg/flag/#FlagSet.Name),
및
[`Output`](/pkg/flag/#FlagSet.Output)를 사용하여
[`NewFlagSet`](/pkg/flag/#NewFlagSet)에 전달된 설정을 가져옵니다.
그리고
[`FlagSet.SetOutput`](/pkg/flag/#FlagSet.SetOutput).

#### [go/doc](/pkg/go/doc/)

다음과 같이 설명된 [문서 변경 사항](#doc)을 지원하기 위해,
`T`, `*T`, `**T` 등 슬라이스를 반환하는 함수는
이제 `T`의 [`Type`](/pkg/go/doc/#Type)의 `Funcs` 목록에 보고되지만,
`Package`의 `Funcs` 목록에는 보고되지 않습니다.

#### [go/importer](/pkg/go/importer/)

[`For`](/pkg/go/importer/#For) 함수는 이제 비-null lookup 인수를 받습니다.

#### [go/printer](pkg/go/printer/)

위의 [gofmt](#gofmt) 섹션에서 논의된 Go 소스 코드의 기본 서식 변경 사항은
[go/printer](/pkg/go/printer/) 패키지에서 구현되며,
또한 더 높은 수준의 [go/format](/pkg/go/format/) 패키지의 출력에도 영향을 미칩니다.

#### [해시](/pkg/hash/)

`Hash` 인터페이스의 구현은 이제 [`encoding.BinaryMarshaler`](/pkg/encoding/#BinaryMarshaler) 및 [`encoding.BinaryUnmarshaler`](/pkg/encoding/#BinaryUnmarshaler) 인터페이스를 구현하도록 권장됩니다. 이를 통해 내부 상태를 저장하고 복원할 수 있습니다.
또한, 표준 라이브러리의 모든 구현 (`hash/crc32`, `crypto/sha256` 등)도 이러한 인터페이스를 구현합니다.

#### [html/template](/pkg/html/template/)

새로운 [`Srcset`](/pkg/html/template#Srcset) 콘텐츠
형은 `img` 태그의 `srcset` 속성에 대한 값의 적절한 처리를 가능하게 합니다.

#### [math/big](/pkg/math/big/)

[`Int`](/pkg/math/big/#Int)는 이제 `SetString` 및 `Text` 메서드를 통해 2부터 62까지의 기반으로 변환을 지원합니다.
(이전에는 2부터 36까지의 기반만 지원했습니다.)
상수 `MaxBase`의 값이 업데이트되었습니다.

[`Int`](/pkg/math/big/#Int)는 새로운
[`CmpAbs`](/pkg/math/big/#CmpAbs) 메서드를 추가하여, [`Cmp`](/pkg/math/big/#Cmp)와 유사하지만, 인자의 절대값(부호는 고려하지 않고)만 비교합니다.

[`Float`](/pkg/math/big/#Float)은 제곱근을 계산하는 새로운
[`Sqrt`](/pkg/math/big/#Float.Sqrt) 메서드를 추가합니다.

#### [math/cmplx](/pkg/math/cmplx/)

`Asin`, `Asinh`, `Atan`, 및 `Sqrt` 함수의 분기 처리 및 기타 경계 사례가 C99 표준에서 사용되는 정의와 일치하도록 수정되었습니다.

#### [math/rand](/pkg/math/rand/)

새로운 [`Shuffle`](/pkg/math/rand/#Shuffle) 함수와 해당 [`Rand.Shuffle`](/pkg/math/rand/#Rand.Shuffle) 메서드는 입력 시퀀스를 섞습니다.

#### [math](/pkg/math/)

새로운 함수
[`Round`](/pkg/math/#Round)
과
[`RoundToEven`](/pkg/math/#RoundToEven)
은 주어진 인수를 가장 가까운 부동 소수점 정수로 반올림합니다.
`Round`은 반정수를 더 큰 정수 쪽으로 반올림(0에서 멀어지는 방향)합니다.
`RoundToEven`은 반정수를 가장 가까운 짝수 정수로 반올림합니다.

새로운 함수
[`Erfinv`](/pkg/math/#Erfinv)
과
[`Erfcinv`](/pkg/math/#Erfcinv)
은 역 오차 함수와 역 보완 오차 함수를 계산합니다.

#### [mime/multipart](/pkg/mime/multipart/)

[`Reader`](/pkg/mime/multipart/#Reader)
이제 빈 파일 이름 속성을 가진 파트를 허용합니다.

#### [mime](/pkg/mime/)

[`ParseMediaType`](/pkg/mime/#ParseMediaType)는 이제
유효하지 않은 속성 값을 버립니다; 이전에는 해당 값을 빈 문자열로 반환했습니다.

#### [net](/pkg/net/)

[`Conn`](/pkg/net/#Conn) 및
[`Listener`](/pkg/net/#Conn) 구현은 이 패키지에서 `Close`가 반환될 때,
기본 파일 디스크립터가 닫혔음을 보장합니다.
(이전 버전에서는 `Close`가 다른 고루틴에서 대기 중인 I/O를 중단하는 경우, `Close`가 반환된 후 해당 고루틴에서 파일 디스크립터가 곧바로 닫힐 수 있었습니다.)

[`TCPListener`](/pkg/net/#TCPListener) 및
[`UnixListener`](/pkg/net/#UnixListener)는 이제
[`syscall.Conn`](/pkg/syscall/#Conn)를 구현하여,
[`syscall.RawConn.Control`](/pkg/syscall/#RawConn)를 사용하여
기본 파일 디스크립터에 옵션을 설정할 수 있도록 합니다.

`Pipe`에서 반환되는 `Conn` 구현체는 이제 읽기 및 쓰기 시간 초를 설정할 수 있습니다.

다음 메서드들은 이제 Windows에서 구현되었습니다.

[`IPConn.ReadMsgIP`](/pkg/net/#IPConn.ReadMsgIP),
[`IPConn.WriteMsgIP`](/pkg/net/#IPConn.WriteMsgIP),
[`UDPConn.ReadMsgUDP`](/pkg/net/#UDPConn.ReadMsgUDP),
그리고
[`UDPConn.WriteMsgUDP`](/pkg/net/#UDPConn.WriteMsgUDP).

#### [net/http](/pkg/net/http/)

클라이언트 측에서, 일반적으로 [`ProxyFromEnvironment`](/pkg/net/http/#ProxyFromEnvironment)를 통해 구성되는 HTTP 프록시는 이제 `https://` URL로 지정할 수 있으며, 이는 클라이언트가 먼저 HTTPS를 통해 프록시에 연결한 후 표준, 프록시된 HTTP 요청을 발행한다는 의미입니다. (이전에는 HTTP 프록시 URL이 `http://` 또는 `socks5://`로 시작해야 했습니다.)

서버 측에서는 [`FileServer`](/pkg/net/http/#FileServer) 및 단일 파일에 해당 [`ServeFile`](/pkg/net/http/#ServeFile)가 이제 `HEAD` 요청에 대해 `If-Range` 확인을 적용합니다.
`FileServer`는 또한 디렉토리 읽기 실패를 [`Server`](/pkg/net/http/#Server)의 `ErrorLog`에 보고합니다.
콘텐츠 제공 핸들러는 이제 0 길이의 콘텐츠를 제공할 때 `Content-Type` 헤더를 제거합니다.

[`ResponseWriter`](/pkg/net/http/#ResponseWriter)의 `WriteHeader` 메서드가 유효하지 않은 (3자리 숫자가 아닌) 상태 코드를 전달하면 패닉(panic) 발생.

<!-- CL 46631 -->
`Server`에서 `Handler`가 아무 출력도 작성하지 않을 때 명시적인 `Content-Type`을 더 이상 추가하지 않습니다.

[`Redirect`](/pkg/net/http/#Redirect)는 이제 HTTP 응답을 쓰기 전에 `Content-Type` 헤더를 설정합니다.

#### [net/mail](pkg/net/mail/)

[`ParseAddress`](/pkg/net/mail/#ParseAddress) 및
[`ParseAddressList`](/pkg/net/mail/#ParseAddressList)
이제 다양한 구식 주소 형식도 지원합니다.

```
#### [net/smtp](pkg/net/smtp/)
```

[`Client`](/pkg/net/smtp/#Client)은 새로운
[`Noop`](/pkg/net/smtp/#Client.Noop) 메서드를 추가하여, 서버가 여전히 응답하는지 테스트합니다.
또한, [`Hello`](/pkg/net/smtp/#Client.Hello) 및 [`Verify`](/pkg/net/smtp/#Client.Verify) 메서드의 입력에 대한 잠재적인 SMTP 주입 공격을 방어합니다.

```
#### [net/textproto](pkg/net/textproto/)
```

[`ReadMIMEHeader`](/pkg/net/textproto/#ReadMIMEHeader)
이제 중첩된 (들여쓰기된) 헤더 라인이 시작되는 헤더를 모두 거부합니다.
이전에는 들여쓰기가 된 첫 번째 줄이 있는 헤더는 들여쓰기가 된 줄이 없다고 취급되었습니다.

#### [net/url](/pkg/net/url/)

[`ResolveReference`](/pkg/net/url/#ResolveReference)
이제 대상 URL의 여러 개의 선행 슬래시를 유지합니다.
이전에는 여러 개의 선행 슬래시를 단 하나의 슬래시로 변경하여, [`http.Client`](/pkg/net/http/#Client)가 특정 리디렉션을 잘못 처리하는 결과를 초래했습니다.

다음 코드의 출력 결과가 변경되었습니다:

base, _ := url.Parse("http://host//path//to/page1")
target, _ := url.Parse("page2")
fmt.Println(base.ResolveReference(target))

참고: `path` 주변의 이중 슬래시를 주목하세요.
Go 1.9 이전 버전에서 해결된 URL은 `http://host/path//to/page2`였습니다.
`path` 앞에 있는 이중 슬래시는 잘못되어 단일 슬래시로 대체되었지만, `path` 뒤에 있는 이중 슬래시는 올바르게 유지되었습니다.
Go 1.10은 두 개의 이중 슬래시 모두 유지하여, [RFC 3986](https://tools.ietf.org/html/rfc3986#section-5.2)에 따라 `http://host//path//to/page2`로 해결합니다.

이 변경 사항으로 기존의 결함 있는 프로그램이 의도치 않게 경로에 선행되는 이중 슬래시를 가진 기본 URL을 구성하고, 이 오류를 수정하기 위해 `ResolveReference`에 의존하게 될 수 있습니다.

예를 들어, 코드가 `/my/api`와 같은 경로에 `http://host/`와 같은 호스트 접두사를 추가하여 `http://host//my/api`와 같이 이중 슬래시를 포함하는 URL을 생성하는 경우에 발생할 수 있습니다.

[`UserInfo`](/pkg/net/url/#UserInfo)의 메서드
이제 `nil` 수신자를 0 값의 `UserInfo`에 대한 포인터와 동일하게 취급합니다.
이전에는 예외가 발생했습니다.

```
#### [os](pkg/os/)
```

[`File`](/pkg/os/#File)는 새로운 메서드를 추가합니다.
[`SetDeadline`](/pkg/os/#File.SetDeadline),
[`SetReadDeadline`](/pkg/os/#File.SetReadDeadline),
그리고
[`SetWriteDeadline`](/pkg/os/#File.SetWriteDeadline)
는 기본 파일 디스크립터가 비동기 I/O 작업을 지원할 때 I/O 시간 제한을 설정할 수 있도록 합니다.
이러한 메서드의 정의는 [`net.Conn`](/pkg/net/#Conn)에 있는 것과 동일합니다.
I/O 메서드가 시간 제한을 놓아 실패하면,
새로운 [`IsTimeout`](/pkg/os/#IsTimeout) 함수는 오류가 시간 초과를 나타내는지 여부를 보고합니다.

또한,
`net.Conn` 및
`File`의
[`Close`](/pkg/os/#File.Close) 메서드는 이제 `Close`가 반환될 때,
기본 파일 디스크립터가 닫히도록 보장합니다.
(이전 버전에서는,
`Close`가 다른 goroutine에서 대기 중인 I/O를 중단하는 경우, `Close`가 반환된 후 짧은 시간 안에 그 goroutine에서 파일 디스크립터가 닫힐 수 있었습니다.)

온 BSD, macOS, 및 Solaris 시스템에서,
[`Chtimes`](/pkg/os/#Chtimes)
이제 파일 타임을 나노초 단위로 설정할 수 있습니다 (하위 파일 시스템이 이를 표현할 수 있는 경우).

#### [reflect](/pkg/reflect/)

[`Copy`](/pkg/reflect/#Copy) 함수는 이제 문자열에서 바이트 배열 또는 바이트 슬라이스로 복사하는 기능을 제공하며, 이는 [내장된 copy 함수](/pkg/builtin/#copy)와 일치합니다.

구조체에서, 비공개 구조 유형에 대한 내장 포인터가
이전에는 해당 `StructField` ([StructField](/pkg/reflect/#StructField)) 내에 빈 `PkgPath`로
잘못 보고되었습니다. 그 결과,
그리고 `Value.CanSet` (/pkg/reflect/#Value.CanSet)
잘못하게 `true`를 반환하고
`Value.Set` (/pkg/reflect/#Value.Set)
잘못하게 성공했습니다.
기본 메타데이터가 수정되었습니다.
이제 이러한 필드에 대해,
`CanSet`은 올바르게 `false`를 반환하고
`Set`은 올바르게 `panic`합니다.
이는 이전에는 이러한 필드에 대한 unmarshal을 수행할 수 있었던
반사 기반 unmarshaler에 영향을 줄 수 있습니다.
예를 들어, `encoding/json` 섹션을 참조하십시오.

#### [runtime/pprof](pkg/runtime/pprof/)

正如 [위에 언급된](#pprof) 것처럼, 차단 및 뮤텍스 프로필에는 이제 심볼 정보가 포함되어 있어, 해당 프로필을 생성한 바이너리 없이도 확인할 수 있습니다.

#### [strconv](/pkg/strconv/)

[`ParseUint`](/pkg/strconv/#ParseUint)는 이제 적절한 크기의 최대 크기의 정수를 반환하며, `ErrRange` 오류가 발생할 때도 그렇습니다. 이는 이미 문서화된 대로 작동합니다.
이전에는 `ErrRange` 오류가 발생할 때 0을 반환했습니다.

#### [strings](pkg/strings/)

새로운 유형
[`Builder`](/pkg/strings/#Builder)는 `bytes.Buffer`를 대체하여 텍스트를 `string` 결과로 모으는 경우에 사용됩니다.
`Builder`의 API는 `bytes.Buffer`의 제한된 부분으로, `String` 메서드에서 데이터를 복사하는 중에도 안전하게 중복 복사를 피할 수 있도록 합니다.

#### [syscall](/pkg/syscall/)

On Windows,
새로운 `SysProcAttr` 필드 `Token`,
`Token` 유형(`/pkg/syscall/#SysProcAttr`, `/pkg/syscall/#Token`)은 `StartProcess`
(그리고 따라서 `os.StartProcess` 및 `exec.Cmd.Start`) 중에
다른 사용자로 실행되는 프로세스를 생성할 수 있도록 합니다.
새로운 함수 `CreateProcessAsUser`는 기본 시스템 호출에 액세스합니다.

다음 BSD, macOS 및 Solaris 시스템에서 [`UtimesNano`](/pkg/syscall/#UtimesNano) 기능이 구현되었습니다.

#### [time](/pkg/time/)

[`LoadLocation`](/pkg/time/#LoadLocation)는 이제 `$ZONEINFO` 환경 변수로 지정된 디렉토리 또는 압축되지 않은 ZIP 파일을 사용하기 전에, 기본 시스템별로 알려진 설치 위치 목록 또는 `$GOROOT/lib/time/zoneinfo.zip`을 확인합니다.

새로운 함수 [`LoadLocationFromTZData`](/pkg/time/#LoadLocationFromTZData)는 IANA 시간대 파일 데이터를 `Location` 객체로 변환할 수 있도록 합니다.

#### [유니코드](/pkg/unicode/)

[`unicode`](/pkg/unicode/) 패키지와 시스템 전체에 걸쳐 제공되는 관련 지원이 Unicode 9.0에서 [Unicode 10.0](https://www.unicode.org/versions/Unicode10.0.0/)로 업그레이드되었습니다. 이를 통해 8,518개의 새로운 문자, 4개의 새로운 스크립트, 1개의 새로운 속성, 비트코인 통화 기호 및 56개의 새로운 이모지가 추가되었습니다.
