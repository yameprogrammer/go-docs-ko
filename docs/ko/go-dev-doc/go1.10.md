<!--
참고: 이 문서 및 이 디렉토리의 다른 문서에서는 `hello` `world`와 같이 고정 폭 구절을 고정 폭이 아닌 공백으로 설정하는 것이 관례입니다.
이러한 구절에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

이 내용은 번역할 텍스트가 포함되어 있지 않은 스타일 시트(` <style> ` 태그)만 포함되어 있습니다. 번역할 기술 문서 내용을 제공해 주시면 정확하게 번역해 드리겠습니다.

## Go 1.10 소개 {#introduction}

최신 Go 릴리스인 버전 1.10이 [Go 1.9](go1.9) 출시 6개월 만에 공개되었습니다.
대부분의 변경 사항은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언제나 그렇듯, 이번 릴리스에서도 Go 1 [호환성 약속](/doc/go1compat.html)을 유지합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 기대합니다.

이번 릴리스에서는 [빌드된 패키지의 캐싱](#build) 기능이 개선되었고,
[성공한 테스트 결과의 캐싱](#test) 기능이 추가되었으며,
[테스트 중 vet이 자동으로 실행](#test-vet)되고,
[cgo를 사용하여 Go와 C 간에 문자열 값을 직접 전달](#cgo)하는 것이 허용됩니다.
새롭게 [하드코딩된 안전한 컴파일러 옵션 세트](#cgo)로 인해,
이전 릴리스에서 성공적으로 빌드되었던 코드에서 예상치 못한 [`invalid flag`](/s/invalidflag) 오류가 발생할 수 있습니다.

## 언어 변경 사항 {#language}

언어 사양에 중요한 변경 사항은 없습니다.

<!-- CL 60230 -->
타입이 지정되지 않은 상수(untyped constants)의 시프트 연산과 관련된 코너 케이스가 명확해졌으며, 그 결과 `s`가 부호 없는 정수(unsigned integer)인 경우 인덱스 표현식 `x[1.0`&nbsp;`<<`&nbsp;`s]`를 허용하도록 컴파일러가 업데이트되었습니다. [go/types](/pkg/go/types/) 패키지는 이미 이를 지원하고 있었습니다.

<!-- CL 73233 -->
메서드 표현식(method expressions)의 문법이 업데이트되어, 리시버(receiver)로 모든 타입 표현식을 사용할 수 있도록 구문이 완화되었습니다. 이는 컴파일러가 이미 구현하고 있던 방식과 일치합니다.
예를 들어, `struct{io.Reader}.Read`는 다소 특이하지만 유효한 메서드 표현식이며, 컴파일러는 이미 이를 허용하고 있었고 이제는 언어 문법에서도 허용됩니다.

## 포트 {#ports}

이번 릴리스에서 새롭게 지원되는 운영 체제나 프로세서 아키텍처는 없습니다.
대부분의 작업은 기존 포트에 대한 지원을 강화하는 데 집중되었으며, 특히 [어셈블러의 새로운 명령어](#asm)와 컴파일러가 생성하는 코드의 개선이 이루어졌습니다.

[Go 1.9 릴리스 노트에서 발표한 바와 같이](go1.9#freebsd),
Go 1.10부터는 FreeBSD 10.3 이상 버전이 필요하며,
FreeBSD 9.3에 대한 지원은 제거되었습니다.

Go가 다시 NetBSD에서 실행되지만, 아직 출시되지 않은 NetBSD 8 버전이 필요합니다.
`GOARCH` `amd64` 및 `386`만 수정되었습니다. `arm` 포트는 여전히 작동하지 않습니다.

32비트 MIPS 시스템에서, 새로운 환경 변수 설정인
`GOMIPS=hardfloat` (기본값)와
`GOMIPS=softfloat`는
부동 소수점 연산에 하드웨어 명령어를 사용할지 아니면 소프트웨어 에뮬레이션을 사용할지를 선택합니다.

Go 1.10은 OpenBSD 6.0에서 실행되는 마지막 릴리스입니다.
Go 1.11은 OpenBSD 6.2가 필요합니다.

Go 1.10은 OS X 10.8 Mountain Lion 또는 OS X 10.9 Mavericks에서 실행되는 마지막 릴리스입니다.
Go 1.11은 OS X 10.10 Yosemite 이상 버전이 필요합니다.

Go 1.10은 Windows XP 또는 Windows Vista에서 실행 가능한 마지막 릴리스입니다.
Go 1.11부터는 Windows 7 이상의 버전이 필요합니다.

## 도구 {#tools}

### 기본 GOROOT 및 GOTMPDIR {#goroot}

환경 변수 `$GOROOT`가 설정되지 않은 경우, 이전에 go 툴은 툴체인 컴파일 중에 설정된 기본 `GOROOT`를 사용했습니다.
이제 go 툴은 해당 기본값으로 되돌아가기 전에, 자체 실행 파일 경로로부터 `GOROOT`를 추론하려고 시도합니다.
이를 통해 바이너리 배포판을 파일 시스템 어디에나 압축 해제하여 `GOROOT`를 명시적으로 설정하지 않고도 사용할 수 있습니다.

기본적으로 `go` 툴은 시스템 임시 디렉토리(예: Unix의 `$TMPDIR`)에 임시 파일과 디렉토리를 생성합니다.
새로운 환경 변수인 `$GOTMPDIR`이 설정되어 있다면, `go` 툴은 대신 해당 디렉토리에 임시 파일과 디렉토리를 생성합니다.

### 빌드 및 설치 {#build}

`go` `build` 명령은 이제 소스 파일의 내용, 지정된 빌드 플래그, 그리고 컴파일된 패키지에 저장된 메타데이터만을 기반으로 최신 상태가 아닌 패키지를 감지합니다.
수정 시간(Modification times)은 더 이상 참조되지 않으며 중요하지 않습니다.
여러 가지 이유로(예: 빌드 플래그 변경) 수정 시간이 오해의 소지가 있는 경우, 강제로 다시 빌드하기 위해 `-a`를 추가하라는 기존의 권고는 더 이상 필요하지 않습니다.
이제 빌드 시 패키지를 다시 빌드해야 하는 시점을 항상 정확하게 감지합니다.
(만약 그렇지 않은 현상을 발견하신다면, 버그 리포트를 제출해 주세요.)

`go` `build`의 `-asmflags`, `-gcflags`, `-gccgoflags`, `-ldflags` 옵션은 이제 기본적으로 명령줄에 직접 나열된 패키지에만 적용됩니다. 예를 들어, `go` `build` `-gcflags=-m` `mypkg`는 `mypkg`를 빌드할 때 컴파일러에 `-m` 플래그를 전달하지만, 해당 패키지의 의존성 패키지에는 전달하지 않습니다.

새롭게 도입된 더 일반적인 형태인 `-asmflags=pattern=flags`(다른 옵션들도 동일)는 패턴과 일치하는 패키지에만 `flags`를 적용합니다. 예를 들어, `go` `install` `-ldflags=cmd/gofmt=-X=main.version=1.2.3` `cmd/...`는 `cmd/...`와 일치하는 모든 명령어를 설치하지만, `-X` 옵션은 `cmd/gofmt`의 링커 플래그에만 적용합니다.

자세한 내용은 [`go` `help` `build`](/cmd/go/#hdr-Compile_packages_and_dependencies)를 참조하십시오.

`go` `build` 명령어는 이제 `$GOROOT/pkg` 또는 `$GOPATH/pkg`에 설치된 패키지와는 별도로, 최근에 빌드된 패키지의 캐시를 유지합니다. 이 캐시의 목적은 패키지를 명시적으로 설치하지 않는 빌드나, 소스 코드의 서로 다른 복사본 사이를 전환할 때(예: 버전 관리 시스템에서 서로 다른 브랜치 간을 앞뒤로 전환할 때) 빌드 속도를 높이는 것입니다. `go` `build` `-i` 또는 `go` `test` `-i`와 같이 속도를 높이기 위해 `-i` 플래그를 추가하라는 이전의 권고는 더 이상 필요하지 않습니다. `-i` 없이도 빌드는 동일하게 빠르게 실행됩니다. 자세한 내용은 [`go` `help` `cache`](/cmd/go/#hdr-Build_and_test_caching)를 참조하십시오.

`go` `install` 명령은 이제 명령줄에 직접 나열된 패키지와 명령만 설치합니다.
예를 들어, `go` `install` `cmd/gofmt`는 gofmt 프로그램을 설치하지만, 해당 프로그램이 의존하는 패키지들은 설치하지 않습니다.
새로운 빌드 캐시 덕분에, 의존성 패키지들이 설치된 것처럼 이후의 명령들도 여전히 빠르게 실행됩니다.
의존성 패키지들의 설치를 강제하려면 새로운 `go` `install` `-i` 플래그를 사용하십시오.
일반적으로 의존성 패키지를 설치하는 것은 필요하지 않으며, '설치된 패키지'라는 개념 자체가 향후 릴리스에서 사라질 수 있습니다.

이러한 개선 사항을 지원하기 위해 `go` `build` 구현의 많은 세부 사항이 변경되었습니다.
이러한 변경으로 인해 발생하는 새로운 요구 사항 중 하나는, 바이너리 전용 패키지가 스텁(stub) 소스 코드에 정확한 import 블록을 선언해야 한다는 것입니다. 그래야만 바이너리 전용 패키지를 사용하여 프로그램을 링크할 때 해당 import들을 사용할 수 있습니다.
자세한 내용은 [`go` `help` `filetype`](/cmd/go/#hdr-File_types)를 참조하십시오.

### 테스트 {#test}

`go` `test` 명령어는 이제 테스트 결과를 캐시합니다:
테스트 실행 파일과 명령줄이 이전 실행과 일치하고,
해당 실행 시 참조된 파일과 환경 변수 또한
변경되지 않았다면, `go` `test`는
이전 테스트 출력을 출력하며 경과 시간을 “(cached)”라는 문자열로 대체합니다.
테스트 캐싱은 성공한 테스트 결과에만 적용되며,
패키지 목록이 명시적으로 지정된 `go` `test`
명령어에만 적용되고,
`-cpu`, `-list`, `-parallel`,
`-run`, `-short`, `-v` 테스트 플래그의
일부만 사용하는 명령줄에만 적용됩니다.
테스트 캐싱을 우회하는 관용적인 방법은 `-count=1`을 사용하는 것입니다.

`go` `test` 명령어는 이제 테스트 대상 패키지에 대해 `go` `vet`을 자동으로 실행하여, 테스트를 수행하기 전에 중대한 문제를 식별합니다.
이러한 문제는 빌드 오류와 동일하게 처리되며 테스트 실행을 중단시킵니다.
자동 검사에는 `go` `vet`에서 제공하는 검사 중 신뢰도가 높은 일부 하위 집합만 활성화됩니다.
`go` `vet` 실행을 비활성화하려면 `go` `test` `-vet=off`를 사용하십시오.

`go` `test` `-coverpkg` 플래그가 이제 인자를 각 테스트의 종속성과 일치시킬 쉼표로 구분된 패턴 목록으로 해석하며, 새로 로드할 패키지 목록으로 해석하지 않습니다. 예를 들어, `go` `test` `-coverpkg=all`은 이제 테스트 패키지와 모든 종속성에 대해 커버리지를 활성화하여 테스트를 실행하는 의미 있는 방법이 되었습니다.
또한, 이제 여러 테스트를 실행할 때 `go` `test` `-coverprofile` 옵션을 지원합니다.

타임아웃으로 인해 실패하는 경우, 이제 테스트가 종료되기 전에 프로파일을 작성할 가능성이 더 높아졌습니다.

`go` `test` 명령은 이제 항상 주어진 테스트 바이너리 실행의 표준 출력(standard output)과 표준 에러(standard error)를 병합하여 `go` `test`의 표준 출력으로 기록합니다. 이전 릴리스에서 `go` `test`는 대부분의 경우에만 이러한 병합을 적용했습니다.

`go`&nbsp;`test` `-v` 출력에 [병렬 테스트](/pkg/testing/#T.Parallel)가 일시 중지되고 다시 시작되는 시점을 표시하는 `PAUSE` 및 `CONT` 상태 업데이트 라인이 추가되었습니다.

새로운 `go` `test` `-failfast` 플래그는
어떤 테스트라도 실패하면 이후의 추가 테스트 실행을 중단합니다.
단, 실패한 테스트와 병렬로 실행 중인 테스트들은 완료될 때까지 허용됩니다.

마지막으로, 새로운 `go` `test` `-json` 플래그는 새로운 명령어인 `go` `tool` `test2json`을 통해 테스트 출력을 필터링하여, 테스트 실행에 대한 기계 판독 가능한 JSON 형식의 설명을 생성합니다. 이를 통해 IDE 및 기타 도구에서 테스트 실행에 대한 풍부한 프레젠테이션을 구현할 수 있습니다.

이 모든 변경 사항에 대한 자세한 내용은
[`go` `help` `test`](/cmd/go/#hdr-Test_packages)와
[test2json 문서](/cmd/test2json/)를 참조하십시오.

### Cgo {#cgo}

`#cgo CFLAGS` 등과 같이 cgo에서 지정한 옵션들이 이제 허용된 옵션 목록과 대조하여 확인됩니다.
이는 다운로드한 패키지가 <span style="white-space: nowrap">`-fplugin`</span>과 같은 컴파일러 옵션을 사용하여 빌드 중인 머신에서 임의의 코드를 실행할 수 있었던 보안 취약점을 해결합니다.
이로 인해 `invalid flag in #cgo CFLAGS`와 같은 빌드 에러가 발생할 수 있습니다.
자세한 배경 설명 및 이 에러를 처리하는 방법은 [https://golang.org/s/invalidflag](/s/invalidflag)를 참조하십시오.

Cgo는 이제 “`typedef` `X` `Y`”와 같은 C typedef를 Go 타입 별칭(type alias)을 사용하여 구현하므로, Go 코드에서 `C.X`와 `C.Y` 타입을 서로 교체하여 사용할 수 있습니다.
또한, 이제 인자가 없는 함수 형태의 매크로(niladic function-like macros) 사용을 지원합니다.
아울러, cgo로 내보낸(exported) 함수의 타입 시그니처에서는 Go 구조체(struct)와 Go 배열(array)이 지원되지 않는다는 점을 명확히 하기 위해 문서가 업데이트되었습니다.

이제 Cgo는 C에서 Go 문자열 값에 직접 접근하는 기능을 지원합니다.
C 프리앰블(preamble)의 함수는 `_GoString_` 타입을 사용하여 Go 문자열을 인자로 받을 수 있습니다.
C 코드는 `_GoStringLen` 및 `_GoStringPtr`을 호출하여 문자열 내용에 직접 접근할 수 있습니다.
`_GoString_` 타입의 값은 Go 타입 `string`을 인자로 받는 내보내기(exported)된 Go 함수 호출 시 전달될 수 있습니다.

툴체인 부트스트랩 중에 환경 변수 `CC`와 `CC_FOR_TARGET`은 결과 툴체인이 각각 호스트 및 타겟 빌드에 사용할 기본 C 컴파일러를 지정합니다.
하지만 툴체인을 여러 타겟과 함께 사용하는 경우, 각 타겟마다 다른 C 컴파일러를 지정해야 할 수도 있습니다(예를 들어, `darwin/arm64`와 `linux/ppc64le`에 대해 서로 다른 컴파일러 사용).
새로운 환경 변수 세트인 `CC_FOR__goos___goarch_`를 사용하면 각 타겟에 대해 다른 기본 C 컴파일러를 지정할 수 있습니다.
이 변수들은 결과 툴체인에서 사용할 기본값을 설정하기 위해 툴체인 부트스트랩 중에만 적용된다는 점에 유의하십시오.
이후의 `go` `build` 명령은 `CC` 환경 변수 또는 내장된 기본값을 사용합니다.

이제 Cgo는 일반적으로 Go의 포인터 타입으로 매핑되는 일부 C 타입을 대신 `uintptr`로 변환합니다. 이러한 타입에는 Darwin의 CoreFoundation 프레임워크에 있는 `CFTypeRef` 계층 구조와 Java의 JNI 인터페이스에 있는 `jobject` 계층 구조가 포함됩니다.

이 타입들은 Go 측에서 반드시 `uintptr`이어야 합니다. 그렇지 않으면 Go 가비지 컬렉터(garbage collector)가 혼동을 일으킬 수 있기 때문입니다. 이들은 때때로 실제 포인터가 아니라 포인터 크기의 정수로 인코딩된 데이터 구조일 수 있습니다. Go 메모리를 가리키는 포인터는 이러한 `uintptr` 값에 저장해서는 안 됩니다.

이 변경 사항으로 인해, 영향을 받는 타입의 값들은 상수 `nil` 대신 상수 `0`으로 제로 초기화되어야 합니다. Go 1.10은 이러한 재작성을 돕기 위해 `gofix` 모듈을 제공합니다:

go tool fix -r cftype <pkg>
	go tool fix -r jni <pkg>

더 자세한 내용은 [cgo 문서](/cmd/cgo/)를 참조하십시오.

### Doc {#doc}

`go` `doc` 도구는 이제 `T` 또는 `*T` 의 슬라이스를 반환하는 함수를 타입 `T` 의 표시 항목에 추가합니다. 이는 단일 `T` 또는 `*T` 결과를 반환하는 함수에 적용되던 기존 동작과 유사합니다.
예를 들어:

$ go doc mail.Address
	package mail // import "net/mail"

```go
type Address struct {
		Name    string
		Address string
	}
```
`Address`는 단일 메일 주소를 나타냅니다.

```go
func ParseAddress(address string) (*Address, error)
	func ParseAddressList(list string) ([]*Address, error)
	func (a *Address) String() string
```

이전에는 `ParseAddressList`가 패키지 개요(`go` `doc` `mail`)에만 표시되었습니다.

### Fix {#fix}

`go`&nbsp;`fix` 도구는 이제 `"golang.org/x/net/context"` 임포트를 `"context"`로 대체합니다.
(Go 1.9 이상 버전을 사용하는 경우, 전자의 포워딩 별칭 덕분에 후자와 완전히 동일하게 동작합니다.)

### Get {#get}

`go`&nbsp;`get` 명령어가 이제 Fossil 소스 코드 저장소를 지원합니다.

### Pprof {#pprof}

`runtime/pprof` 패키지에서 생성하는 blocking 및 mutex 프로파일에 이제 심볼 정보가 포함되어, 프로파일을 생성한 바이너리 없이도 `go` `tool` `pprof`에서 확인할 수 있습니다.
(다른 모든 프로파일 유형은 Go 1.9에서 심볼 정보를 포함하도록 변경되었습니다.)

[`go`&nbsp;`tool`&nbsp;`pprof`](/cmd/pprof/)
프로파일 시각화 도구가 [github.com/google/pprof](https://github.com/google/pprof)의 git 버전 9e20b5b (2017-11-08)로 업데이트되었으며, 여기에는 업데이트된 웹 인터페이스가 포함되어 있습니다.

### Vet {#vet}

[`go`&nbsp;`vet`](/cmd/vet/) 명령은 이제 cgo를 사용하거나 벤더링된(vendored) 임포트를 사용하는 패키지일지라도, 패키지를 검사할 때 항상 완전하고 최신 상태인 타입 정보에 접근할 수 있습니다. 그 결과 보고서가 더 정확해질 것입니다.

이 정보에 접근할 수 있는 것은 `go`&nbsp;`vet`뿐이며, 더 낮은 수준의 `go`&nbsp;`tool`&nbsp;`vet`은 접근할 수 없으므로 `vet` 자체를 작업하는 경우가 아니면 사용을 지양해야 합니다. (Go 1.9부터 `go`&nbsp;`vet`은 `go`&nbsp;`tool`&nbsp;`vet`과 동일한 모든 플래그에 대한 접근을 제공합니다.)

### Diagnostics {#diag}

이번 릴리스에는 사용 가능한 Go 프로그램 진단 도구에 대한 새로운 [개요](/doc/diagnostics.html)가 포함되어 있습니다.

### Gofmt {#gofmt}

Go 소스 코드의 기본 포맷팅에서 두 가지 세부 사항이 변경되었습니다.

첫째, 이전에는 `x[i+1`&nbsp;`:`&nbsp;`j:k]`와 같이 포맷팅되었던 일부 복잡한 3-인덱스 슬라이스 표현식이 이제는 더 일관된 간격인 `x[i+1`&nbsp;`:`&nbsp;`j`&nbsp;`:`&nbsp;`k]`로 포맷팅됩니다.

둘째, 타입 단언(type assertions)에서 간혹 사용되는 한 줄로 작성된 단일 메서드 인터페이스 리터럴이 더 이상 여러 줄로 분리되지 않습니다.

`gofmt`에 대한 이러한 종류의 사소한 업데이트는 때때로 발생할 수 있음을 유의하십시오.
일반적으로 소스 코드가 특정 버전의 `gofmt` 출력 결과와 일치하는지 확인하는 시스템을 구축하는 것은 권장하지 않습니다.
예를 들어, 저장소에 이미 체크인된 코드 중 "적절하게 포맷팅되지 않은" 코드가 있을 때 실패하는 지속적 통합(CI) 테스트는 본질적으로 취약하며 권장되지 않습니다.

여러 프로그램이 소스 파일 포맷팅에 사용할 `gofmt` 버전에 대해 합의해야 하는 경우, 동일한 `gofmt` 바이너리를 호출하도록 설정하는 것을 권장합니다.
예를 들어, Go 오픈 소스 저장소의 Git pre-commit 훅은 Go로 작성되어 `go/format`을 직접 임포트할 수 있지만, 대신 현재 경로에서 `gofmt` 바이너리를 호출합니다. 이렇게 함으로써 `gofmt`가 변경될 때마다 pre-commit 훅을 매번 다시 컴파일할 필요가 없게 됩니다.

### 컴파일러 툴체인 {#compiler}

컴파일러에는 생성된 코드의 성능을 향상시키는 많은 개선 사항이 포함되어 있으며, 이는 지원되는 아키텍처 전반에 걸쳐 상당히 균등하게 적용되었습니다.

바이너리에 기록되는 DWARF 디버그 정보가 다음과 같이 몇 가지 방식으로 개선되었습니다:
상수 값이 이제 기록됩니다.
라인 번호 정보가 더 정확해져서, 프로그램의 소스 레벨 스테핑(stepping) 기능이 더 원활하게 작동합니다.
이제 각 패키지가 개별적인 DWARF 컴파일 단위(compilation unit)로 제공됩니다.

다양한 [빌드 모드](https://docs.google.com/document/d/1nr-TQHw_er6GOQRsF6T43GGhFDelrAP0NqSS_00RgZQ/edit)가 더 많은 시스템으로 포팅되었습니다.
구체적으로, `c-shared`는 이제 `linux/ppc64le`, `windows/386`, `windows/amd64`에서 작동하며,
`pie`는 이제 `darwin/amd64`에서 작동하고 모든 시스템에서 외부 링킹(external linking) 사용을 강제합니다.
또한 `plugin`은 이제 `linux/ppc64le` 및 `darwin/amd64`에서 작동합니다.

`linux/ppc64le` 포트는 이제 cgo를 사용하는 모든 프로그램(표준 라이브러리에서 사용하는 경우 포함)에 대해 외부 링킹(external linking) 사용을 요구합니다.

### Assembler {#asm}

ARM 32비트 포트의 경우, 어셈블러가 이제 다음 명령어들을 지원합니다:
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

ARM 64비트 포트를 위해, 어셈블러가 이제 <code><small>VADD</small></code>,
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
명령어를 지원합니다.

PowerPC 64비트 포트의 경우, 어셈블러가 이제 다음과 같은 POWER9 명령어들을 지원합니다:
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

S390X 포트의 경우, 어셈블러가 이제 <code><small>TMHH</small></code>, <code><small>TMHL</small></code>, <code><small>TMLH</small></code> 및 <code><small>TMLL</small></code> 명령어를 지원합니다.

X86 64비트 포트의 경우, 어셈블러가 이제 AVX, AVX2, BMI, BMI2, F16C, FMA3, SSE2, SSE3, SSSE3, SSE4.1 및 SSE4.2 확장 세트 전체를 포함하여 359개의 새로운 명령어를 지원합니다.
또한 어셈블러는 조건 플래그가 예기치 않게 지워지는 것을 방지하기 위해, 더 이상 <code><small>MOVL</small></code>&nbsp;<code><small>$0,</small></code>&nbsp;<code><small>AX</small></code>를 <code><small>XORL</small></code> 명령어로 구현하지 않습니다.

### Gccgo {#gccgo}

Go의 반기 출시 일정과 GCC의 연간 출시 일정의 조율로 인해, GCC 릴리스 7에는 gccgo의 Go 1.8.3 버전이 포함되어 있습니다. 다음 릴리스인 GCC 8에는 gccgo의 Go 1.10 버전이 포함될 것으로 예상합니다.

## 런타임 {#runtime}

[`LockOSThread`](/pkg/runtime/#LockOSThread)와 [`UnlockOSThread`](/pkg/runtime/#UnlockOSThread)의 중첩 호출 동작이 변경되었습니다.
이 함수들은 고루틴이 특정 운영체제 스레드에 고정될지 여부를 제어하여, 해당 고루틴은 오직 그 스레드에서만 실행되고, 그 스레드는 오직 해당 고루틴만 실행하도록 합니다.
이전에는 `LockOSThread`를 연속으로 여러 번 호출하는 것이 한 번 호출하는 것과 동일했으며, 단 한 번의 `UnlockOSThread` 호출로 항상 스레드 잠금이 해제되었습니다.
이제는 호출이 중첩됩니다. 즉, `LockOSThread`가 여러 번 호출되었다면, 스레드 잠금을 해제하기 위해 `UnlockOSThread`를 동일한 횟수만큼 호출해야 합니다.
이러한 호출을 중첩하지 않도록 주의해서 작성된 기존 코드는 그대로 올바르게 작동합니다.
호출이 중첩된다고 잘못 가정했던 기존 코드는 이제 올바르게 작동하게 됩니다.
공개된 Go 소스 코드에서 이 함수들을 사용하는 대부분의 사례가 후자의 경우에 해당합니다.

`LockOSThread`와 `UnlockOSThread`의 일반적인 용도 중 하나가 Go 코드로 스레드 로컬 상태(예: Linux 또는 Plan 9 네임스페이스)를 안정적으로 수정하는 것이기 때문에, 이제 런타임은 잠긴(locked) 스레드를 재사용하거나 새로운 스레드를 생성하는 데 부적합한 것으로 처리합니다.

스택 트레이스에 더 이상 암시적 래퍼 함수(이전에 `<autogenerated>`로 표시됨)가 포함되지 않습니다. 단, 래퍼 함수 자체에서 결함(fault)이나 패닉(panic)이 발생하는 경우는 제외됩니다.
그 결과, [`Caller`](/pkg/runtime/#Caller)와 같은 함수에 전달되는 skip count는 이제 최적화 결정이나 구현 세부 사항에 의존하지 않고, 작성된 코드의 구조와 항상 일치해야 합니다.

가비지 컬렉터가 할당 지연 시간(allocation latency)에 미치는 영향을 줄이도록 수정되었습니다.
이제 실행 시 전체 CPU의 더 작은 비율을 사용하지만, 실행되는 시간은 더 늘어날 수 있습니다.
가비지 컬렉터가 소비하는 총 CPU 사용량은 크게 변하지 않았습니다.

[`GOROOT`](/pkg/runtime/#GOROOT) 함수는 이제 (`$GOROOT` 환경 변수가 설정되지 않았을 때) 호출 프로그램이 컴파일될 당시의 `GOROOT` 또는 `GOROOT_FINAL`을 기본값으로 사용합니다. 이전에는 호출 프로그램을 컴파일한 툴체인이 컴파일될 당시의 `GOROOT` 또는 `GOROOT_FINAL`을 사용했습니다.

이제 [`GOMAXPROCS`](/pkg/runtime/#GOMAXPROCS) 설정에 제한이 없습니다.
(Go 1.9에서의 제한은 1024였습니다.)

## 성능 {#performance}

언제나 그렇듯, 변경 사항이 매우 광범위하고 다양하여 성능에 대한 정확한 설명을 하기는 어렵습니다. 하지만 가비지 컬렉터의 속도 향상, 더 개선된 코드 생성, 그리고 코어 라이브러리의 최적화 덕분에 대부분의 프로그램이 조금 더 빠르게 실행될 것입니다.

## Garbage Collector {#gc}

가비지 컬렉터가 활성화되었을 때, 많은 애플리케이션에서 할당 지연 시간(allocation latency)과 전반적인 성능 오버헤드가 상당히 낮아지는 것을 경험할 것입니다.

## 표준 라이브러리 {#library}

표준 라이브러리의 모든 변경 사항은 미미합니다.
[bytes](#bytes) 및 [net/url](#net/url)의 변경 사항이 기존 프로그램의 업데이트를 필요로 할 가능성이 가장 높습니다.

### 라이브러리의 마이너 변경 사항 {#minor_library_changes}

언제나 그렇듯, Go 1의 [호환성 약속](/doc/go1compat)을 염두에 두고 라이브러리에 다양한 마이너 변경 사항과 업데이트가 적용되었습니다.

#### [archive/tar](/pkg/archive/tar/)

일반적으로, 특수 헤더 형식의 처리 방식이 대폭 개선되고 확장되었습니다.

[`FileInfoHeader`](/pkg/archive/tar/#FileInfoHeader)는 항상 [`os.FileInfo`](/pkg/os/#FileInfo) 인자(구체적으로 `FileInfo`의 `Sys` 메서드에 의해 반환되는 시스템 종속적 정보)로부터 Unix UID 및 GID 번호를 기록하여 [`Header`](/pkg/archive/tar/#Header)를 반환해 왔습니다.
이제는 해당 ID에 대응하는 사용자 및 그룹 이름과 더불어, 디바이스 파일의 경우 주(major) 및 부(minor) 디바이스 번호도 함께 기록합니다.

[`Format`](/pkg/archive/tar/#Format) 타입의 새로운 [`Header.Format`](/pkg/archive/tar/#Header) 필드는 [`Writer`](/pkg/archive/tar/#Writer)가 사용할 tar 헤더 형식을 제어합니다.
이전과 마찬가지로 기본값은 헤더에 필요한 필드들을 인코딩할 수 있는 가장 널리 지원되는 헤더 유형을 선택하는 것입니다(가능하면 USTAR, 아니면 PAX, 그 외에는 GNU).
[`Reader`](/pkg/archive/tar/#Reader)는 읽어들이는 각 헤더에 대해 `Header.Format`을 설정합니다.

`Reader`와 `Writer`는 이제 새로운 [`Header.PAXRecords`](/pkg/archive/tar/#Header) 필드를 사용하여 임의의 PAX 레코드를 지원합니다. 이 필드는 기존 `Xattrs` 필드를 일반화한 것입니다.

`Reader`는 더 이상 GNU 헤더의 파일 이름이나 링크 이름이 유효한 UTF-8이어야 한다고 강제하지 않습니다.

PAX 또는 GNU 형식의 헤더를 작성할 때, 이제 `Writer`는 `Header.AccessTime` 및 `Header.ChangeTime` 필드(설정된 경우)를 포함합니다.
PAX 형식의 헤더를 작성할 때, 시간은 초 미만 단위의 정밀도를 포함합니다.

#### [archive/zip](/pkg/archive/zip/)

Go 1.10에서는 ZIP 아카이브의 시간 및 문자 집합 인코딩에 대한 더 완전한 지원이 추가되었습니다.

원래의 ZIP 형식은 연, 월, 일, 시, 분, 초를 두 개의 16비트 값 필드로 인코딩하는 표준 MS-DOS 인코딩을 사용했습니다.
해당 인코딩으로는 시간대나 정밀한 초 단위를 표현할 수 없기 때문에, 더 풍부한 인코딩을 가능하게 하는 여러 확장 기능이 도입되었습니다.
Go 1.10에서는 [`Reader`](/pkg/archive/zip/#Reader)와 [`Writer`](/pkg/archive/zip/#Writer)가 32비트 Unix "epoch 이후 경과 초" 형식으로 시간을 별도로 인코딩하는, 널리 알려진 Info-Zip 확장을 이제 지원합니다.
[`FileHeader`](/pkg/archive/zip/#FileHeader)의 새로운 [`time.Time`](/pkg/time/#Time) 타입 필드인 `Modified`는 MS-DOS 인코딩을 계속 유지하고 있는 `ModifiedTime` 및 `ModifiedDate` 필드를 대체합니다.
이제 `Reader`와 `Writer`는 시간대와 무관한 Unix 시간을 저장하는 ZIP 아카이브가 MS-DOS 필드에도 로컬 시간을 함께 저장하여 시간대 오프셋을 추론할 수 있게 하는 일반적인 관례를 따릅니다.
호환성을 위해 [`ModTime`](/pkg/archive/zip/#FileHeader.ModTime) 및 [`SetModTime`](/pkg/archive/zip/#FileHeader.SetModTime) 메서드는 이전 릴리스와 동일하게 동작하며, 새로운 코드에서는 `Modified`를 직접 사용해야 합니다.

ZIP 아카이브의 각 파일 헤더에는 이름과 주석 필드가 시스템별 기본 인코딩이 아닌 UTF-8로 인코딩되었는지 나타내는 플래그 비트가 있습니다.
Go 1.8 및 그 이전 버전에서 `Writer`는 UTF-8 비트를 설정하지 않았습니다.
Go 1.9에서 `Writer`는 거의 항상 UTF-8 비트를 설정하도록 변경되었습니다.
이로 인해 Shift-JIS 파일 이름이 포함된 ZIP 아카이브 생성이 제대로 작동하지 않는 문제가 발생했습니다.
Go 1.10에서는 이름과 주석 필드가 모두 유효한 UTF-8이며 그 중 최소 하나가 non-ASCII인 경우에만 `Writer`가 UTF-8 비트를 설정합니다.
non-ASCII 인코딩이 유효한 UTF-8처럼 보일 가능성은 매우 드물기 때문에, 이 새로운 휴리스틱은 거의 항상 정확할 것입니다.
`FileHeader`의 새로운 `NonUTF8` 필드를 true로 설정하면 해당 파일에 대해 이 휴리스틱이 완전히 비활성화됩니다.

이제 `Writer`는 `Writer`의 새로운 [`SetComment`](/pkg/archive/zip/#Writer.SetComment) 메서드를 호출하여 central-directory 레코드의 comment 필드를 설정하는 기능도 지원합니다.

#### [bufio](/pkg/bufio/)

새로운 [`Reader.Size`](/pkg/bufio/#Reader.Size) 및 [`Writer.Size`](/pkg/bufio/#Writer.Size) 메서드는 `Reader` 또는 `Writer`의 기본 버퍼 크기를 보고합니다.

#### [bytes](/pkg/bytes/)

[`Fields`](/pkg/bytes/#Fields),
[`FieldsFunc`](/pkg/bytes/#FieldsFunc),
[`Split`](/pkg/bytes/#Split),
그리고
[`SplitAfter`](/pkg/bytes/#SplitAfter)
함수들은 항상 입력값의 서브슬라이스(subslices)를 반환해 왔습니다.
Go 1.10에서는 반환되는 각 서브슬라이스의 용량(capacity)이 길이(length)와 동일하게 변경되어, 특정 서브슬라이스에 값을 추가(append)하더라도 원래 입력값의 인접한 데이터를 덮어쓰지 않도록 했습니다.

#### [crypto/cipher](/pkg/crypto/cipher/)

[`NewOFB`](/pkg/crypto/cipher/#NewOFB)가 이제 잘못된 길이의 초기화 벡터(initialization vector)가 전달될 경우 패닉(panic)을 발생시킵니다. 이는 패키지 내 다른 생성자들과 동일한 동작입니다.
(이전에는 `nil` `Stream` 구현체를 반환했습니다.)

#### [crypto/tls](/pkg/crypto/tls/)

이제 TLS 서버는 TLS 1.2 사용 시 SHA-512 서명 지원을 알립니다(advertise).
서버는 이미 해당 서명을 지원하고 있었으나, 일부 클라이언트는 명시적으로 알리지 않으면 이를 선택하지 않는 경우가 있었습니다.

#### [crypto/x509](/pkg/crypto/x509/)

[`Certificate.Verify`](/pkg/crypto/x509/#Certificate.Verify)는 이제 클라이언트가 요청한 단일 이름뿐만 아니라, 인증서에 포함된 모든 이름에 대해 이름 제약 조건(name constraints)을 강제합니다. 확장 키 사용 용도(Extended key usage) 제한 또한 비슷하게 한 번에 모두 확인됩니다. 그 결과, 인증서 검증이 완료되면 이제 인증서 전체를 신뢰할 수 있습니다. 추가 이름이나 키 사용 용도에 대해 인증서를 매번 다시 검증할 필요가 더 이상 없습니다.

이제 파싱된 인증서는 새로운 [`Certificate`](/pkg/crypto/x509/#Certificate) 필드인 `URIs`, `PermittedIPRanges`, `ExcludedIPRanges`, `PermittedEmailAddresses`, `ExcludedEmailAddresses`, `PermittedURIDomains`, `ExcludedURIDomains`를 사용하여 URI 이름과 IP, 이메일, URI 제약 조건을 보고합니다. 해당 필드에 유효하지 않은 값이 포함된 인증서는 이제 거부됩니다.

새로운 [`MarshalPKCS1PublicKey`](/pkg/crypto/x509/#MarshalPKCS1PublicKey) 및 [`ParsePKCS1PublicKey`](/pkg/crypto/x509/#ParsePKCS1PublicKey) 함수는 RSA 공개키를 PKCS#1 인코딩 형식으로 변환하거나 그 반대로 변환합니다.

새로운 [`MarshalPKCS8PrivateKey`](/pkg/crypto/x509/#MarshalPKCS8PrivateKey)
함수는 개인 키를 PKCS#8 인코딩 형식으로 변환합니다.
([`ParsePKCS8PrivateKey`](/pkg/crypto/x509/#ParsePKCS8PrivateKey)는
Go 1부터 존재해 왔습니다.)

#### [crypto/x509/pkix](/pkg/crypto/x509/pkix/)

[`Name`](/pkg/crypto/x509/pkix/#Name)은 이제 X.509 식별 이름(distinguished name)을 표준 RFC 2253 형식으로 포맷팅하는 [`String`](/pkg/crypto/x509/pkix/#Name.String) 메서드를 구현합니다.

#### [database/sql/driver](/pkg/database/sql/driver/)

[`driver.Rows.Next`](/pkg/database/sql/driver/#Rows.Next)에 의해 제공된 목적지 버퍼를 현재 보유하고 있는 드라이버는 해당 호출 외부에서 목적지 배열에 할당된 버퍼에 더 이상 쓰지 않도록 보장해야 합니다. 드라이버는 [`driver.Rows`](/pkg/database/sql/driver/#Rows)를 닫을 때 기본 버퍼가 수정되지 않도록 주의해야 합니다.

클라이언트적으로 [`sql.DB`](/pkg/database/sql/#DB)를 구축하려는 드라이버는 이제 [`sql.Open`](/pkg/database/sql/#Open)에 전달되는 문자열에 모든 설정을 인코딩하는 대신, [`Connector`](/pkg/database/sql/driver/#Connector) 인터페이스를 구현하고 새로운 [`sql.OpenDB`](/pkg/database/sql/#OpenDB) 함수를 호출할 수 있습니다.

[`sql.Conn`](/pkg/database/sql/#Conn)마다 한 번씩이 아니라 `sql.DB`당 단 한 번만 설정 문자열을 파싱하길 원하거나, 각 `sql.Conn`의 기본 컨텍스트(underlying context)에 접근하길 원하는 드라이버는 [`Driver`](/pkg/database/sql/driver/#Driver) 구현체가 [`DriverContext`](/pkg/database/sql/driver/#DriverContext)의 새로운 `OpenConnector` 메서드 또한 구현하도록 만들 수 있습니다.

[`ExecerContext`](/pkg/database/sql/driver/#ExecerContext)를 구현하는 드라이버는 더 이상 [`Execer`](/pkg/database/sql/driver/#Execer)를 구현할 필요가 없습니다. 마찬가지로, [`QueryerContext`](/pkg/database/sql/driver/#QueryerContext)를 구현하는 드라이버는 더 이상 [`Queryer`](/pkg/database/sql/driver/#Queryer)를 구현할 필요가 없습니다. 이전에는 context 기반 인터페이스를 구현했더라도, non-context 기반 인터페이스를 함께 구현하지 않으면 무시되었습니다.

드라이버가 캐시된 드라이버 연결을 연속적으로 사용하여 서로 다른 클라이언트를 더 잘 격리할 수 있도록,
[`Conn`](/pkg/database/sql/driver/#Conn)이 새로운 [`SessionResetter`](/pkg/database/sql/driver/#SessionResetter) 인터페이스를 구현하는 경우,
`database/sql`은 이제 새로운 클라이언트를 위해 `Conn`을 재사용하기 전에 `ResetSession`을 호출합니다.

#### [debug/elf](/pkg/debug/elf/)

이번 릴리스에서는 [`R_386`](/pkg/debug/elf/#R_386), [`R_AARCH64`](/pkg/debug/elf/#R_AARCH64), [`R_ARM`](/pkg/debug/elf/#R_ARM), [`R_PPC64`](/pkg/debug/elf/#R_PPC64), 및 [`R_X86_64`](/pkg/debug/elf/#R_X86_64) 재배치 유형으로 나뉜 348개의 새로운 재배치 상수가 추가되었습니다.

#### [debug/macho](/pkg/debug/macho/)

Go 1.10에서는 [`Section`](/pkg/debug/macho#Section) 구조체의 새로운 `Relocs` 필드와 새로운 [`Reloc`](/pkg/debug/macho/#Reloc), [`RelocTypeARM`](/pkg/debug/macho/#RelocTypeARM), [`RelocTypeARM64`](/pkg/debug/macho/#RelocTypeARM64), [`RelocTypeGeneric`](/pkg/debug/macho/#RelocTypeGeneric), [`RelocTypeX86_64`](/pkg/debug/macho/#RelocTypeX86_64) 타입 및 관련 상수들을 사용하여 Mach-O 섹션에서 재배치(relocation) 정보를 읽는 기능을 지원합니다.

Go 1.10은 [`RpathCmd`](/pkg/debug/macho/#RpathCmd) 및 [`Rpath`](/pkg/debug/macho/#Rpath) 타입으로 표현되는 `LC_RPATH` 로드 명령에 대한 지원과, 헤더에서 발견되는 다양한 플래그 비트를 위한 새로운 [명명된 상수](/pkg/debug/macho/#pkg-constants)를 추가합니다.

#### [encoding/asn1](/pkg/encoding/asn1/)

[`Marshal`](/pkg/encoding/asn1/#Marshal)은 이제 별표(*)가 포함된 문자열을 `PrintableString` 대신 `UTF8String` 타입으로 올바르게 인코딩합니다. 단, 해당 문자열이 `PrintableString` 사용을 강제하는 태그가 지정된 구조체 필드에 있는 경우는 제외됩니다. 또한 `Marshal`은 이제 `application` 지시어가 포함된 구조체 태그를 준수합니다.

새로운 [`MarshalWithParams`](/pkg/encoding/asn1/#MarshalWithParams) 함수는 추가 파라미터가 해당 구조체 필드 태그인 것처럼 인자를 마샬링합니다.

[`Unmarshal`](/pkg/encoding/asn1/#Unmarshal) 이제 `explicit` 및 `tag` 지시어를 사용하는 구조체 필드 태그를 준수합니다.

`Marshal`과 `Unmarshal` 모두 이제 ASN.1 NumericString을 나타내는 새로운 구조체 필드 태그인 `numeric`을 지원합니다.

#### [encoding/csv](/pkg/encoding/csv/)

[`Reader`](/pkg/encoding/csv/#Reader)는 이제 NUL, 캐리지 리턴(carriage return), 줄바꿈(newline), 잘못된 룬(invalid runes), 유니코드 대체 문자(Unicode replacement character)와 같이 의미 없는 `Comma` 및 `Comment` 설정이나, `Comma`와 `Comment`를 동일하게 설정하는 것을 허용하지 않습니다.

여러 입력 줄에 걸쳐 있는 CSV 레코드에서 구문 오류(syntax error)가 발생한 경우, 이제 `Reader`는 [`ParseError`](/pkg/encoding/csv/#ParseError)의 새로운 `StartLine` 필드에 해당 레코드가 시작된 줄 번호를 보고합니다.

#### [encoding/hex](/pkg/encoding/hex/)

새로운 함수인
[`NewEncoder`](/pkg/encoding/hex/#NewEncoder)
와
[`NewDecoder`](/pkg/encoding/hex/#NewDecoder)
는 16진수(hexadecimal)로의 변환 및 16진수로부터의 변환에 대한 스트리밍 기능을 제공하며, 이는
[encoding/base32](/pkg/encoding/base32/)
및
[encoding/base64](/pkg/encoding/base64/)
에 이미 존재하는 동일한 함수들과 유사합니다.

[`Decode`](/pkg/encoding/hex/#Decode) 및 [`DecodeString`](/pkg/encoding/hex/#DecodeString) 함수가 잘못된 입력을 발견했을 때, 이제 오류와 함께 이미 변환된 바이트 수를 반환합니다. 이전에는 오류가 발생하면 항상 0을 반환했습니다.

#### [encoding/json](/pkg/encoding/json/)

[`Decoder`](/pkg/encoding/json/#Decoder)에
알 수 없는 JSON 필드가 포함된 입력에 대해 디코딩 에러를 보고하도록 하는
[`DisallowUnknownFields`](/pkg/encoding/json/#Decoder.DisallowUnknownFields)
새 메서드가 추가되었습니다.
(기존의 기본 동작은 항상 알 수 없는 필드를 무시하는 것이었습니다.)

[reflect 버그 수정](#reflect)의 결과로,
[`Unmarshal`](/pkg/encoding/json/#Unmarshal)은
더 이상 비공개(unexported) 구조체 타입의 내장 포인터(embedded pointers) 내에 있는 필드로 디코딩할 수 없습니다.
이는 비공개 내장 포인터를 새로운 저장 공간을 가리키도록 초기화할 수 없기 때문입니다.
이제 이러한 경우 `Unmarshal`은 에러를 반환합니다.

#### [encoding/pem](/pkg/encoding/pem/)

[`Encode`](/pkg/encoding/pem/#Encode)
및
[`EncodeToMemory`](/pkg/encoding/pem/#EncodeToMemory)
는 PEM 데이터로 인코딩할 수 없는 블록이 제공되었을 때 더 이상 부분적인 출력을 생성하지 않습니다.

#### [encoding/xml](/pkg/encoding/xml/)

새로운 함수 [`NewTokenDecoder`](/pkg/encoding/xml/#NewTokenDecoder)는 [`NewDecoder`](/pkg/encoding/xml/#NewDecoder)와 비슷하지만, XML 형식의 바이트 스트림 대신 [`TokenReader`](/pkg/encoding/xml/#TokenReader)로부터 읽어오는 디코더를 생성합니다. 이는 클라이언트 라이브러리에서 XML 스트림 트랜스포머(transformer)를 구축할 수 있도록 하기 위함입니다.

#### [flag](/pkg/flag/)

기본 [`Usage`](/pkg/flag/#Usage) 함수가 이제 첫 번째 출력 줄을 `os.Stderr`로 가정하는 대신 `CommandLine.Output()`에 출력합니다. 이를 통해 `CommandLine.SetOutput`을 사용하는 클라이언트가 사용법 메시지를 적절하게 리다이렉션할 수 있습니다.

[`PrintDefaults`](/pkg/flag/#PrintDefaults)가 이제 플래그 사용법(usage) 문자열의 줄바꿈 뒤에 적절한 들여쓰기를 추가하여, 여러 줄로 된 사용법 문자열이 깔끔하게 표시됩니다.

[`FlagSet`](/pkg/flag/#FlagSet)에 [`NewFlagSet`](/pkg/flag/#NewFlagSet) 및 [`FlagSet.SetOutput`](/pkg/flag/#FlagSet.SetOutput)으로 전달된 설정을 조회하기 위한 새로운 메서드 [`ErrorHandling`](/pkg/flag/#FlagSet.ErrorHandling), [`Name`](/pkg/flag/#FlagSet.Name), 그리고 [`Output`](/pkg/flag/#FlagSet.Output)이 추가되었습니다.

#### [go/doc](/pkg/go/doc/)

위에서 설명한 [문서 변경 사항](#doc)을 지원하기 위해,
`T`, `*T`, `**T` 등의 슬라이스를 반환하는 함수들이
이제 [`Package`](/pkg/go/doc/#Package)의 `Funcs` 목록 대신
`T`의 [`Type`](/pkg/go/doc/#Type)에 있는 `Funcs` 목록에 보고됩니다.

#### [go/importer](/pkg/go/importer/)

[`For`](/pkg/go/importer/#For) 함수가 이제 nil이 아닌 lookup 인자를 허용합니다.

#### [go/printer](/pkg/go/printer/)

위의 [gofmt 섹션](#gofmt)에서 논의된 Go 소스 코드의 기본 포맷팅 변경 사항은 [go/printer](/pkg/go/printer/) 패키지에 구현되었으며, 더 상위 수준인 [go/format](/pkg/go/format/) 패키지의 출력 결과에도 영향을 미칩니다.

#### [hash](/pkg/hash/)

이제 [`Hash`](/pkg/hash/#Hash) 인터페이스의 구현체들은 내부 상태를 저장하고 다시 생성할 수 있도록 [`encoding.BinaryMarshaler`](/pkg/encoding/#BinaryMarshaler) 및 [`encoding.BinaryUnmarshaler`](/pkg/encoding/#BinaryUnmarshaler)를 구현하는 것이 권장됩니다. 이에 따라 표준 라이브러리의 모든 구현체([hash/crc32](/pkg/hash/crc32/), [crypto/sha256](/pkg/crypto/sha256/) 등)가 해당 인터페이스들을 구현합니다.

#### [html/template](/pkg/html/template/)

새로운 [`Srcset`](/pkg/html/template#Srcset) 콘텐츠 타입은 `img` 태그의 [`srcset`](https://w3c.github.io/html/semantics-embedded-content.html#element-attrdef-img-srcset) 속성 내의 값들을 적절하게 처리할 수 있도록 해줍니다.

#### [math/big](/pkg/math/big/)

[`Int`](/pkg/math/big/#Int)의 [`SetString`](/pkg/math/big/#Int.SetString) 및 [`Text`](/pkg/math/big/#Text) 메서드에서 이제 2부터 62까지의 진법 변환을 지원합니다.
(이전에는 2부터 36까지의 진법만 허용되었습니다.)
상수 `MaxBase`의 값이 업데이트되었습니다.

[`Int`](/pkg/math/big/#Int)에 새로운 [`CmpAbs`](/pkg/math/big/#CmpAbs) 메서드가 추가되었습니다. 이 메서드는 [`Cmp`](/pkg/math/big/#Cmp)와 비슷하지만, 인자의 부호를 제외한 절대값만을 비교합니다.

[`Float`](/pkg/math/big/#Float)에 제곱근을 계산하기 위한 새로운 [`Sqrt`](/pkg/math/big/#Float.Sqrt) 메서드가 추가되었습니다.

#### [math/cmplx](/pkg/math/cmplx/)

[`Asin`](/pkg/math/cmplx/#Asin),
[`Asinh`](/pkg/math/cmplx/#Asinh),
[`Atan`](/pkg/math/cmplx/#Atan),
및
[`Sqrt`](/pkg/math/cmplx/#Sqrt)
의 분지 절단(Branch cuts) 및 기타 경계 사례들이 C99 표준에서 사용하는 정의와 일치하도록 수정되었습니다.

#### [math/rand](/pkg/math/rand/)

새로운 [`Shuffle`](/pkg/math/rand/#Shuffle) 함수와 그에 대응하는 [`Rand.Shuffle`](/pkg/math/rand/#Rand.Shuffle) 메서드는 입력 시퀀스를 셔플합니다.

#### [math](/pkg/math/)

새로운 함수인
[`Round`](/pkg/math/#Round)
와
[`RoundToEven`](/pkg/math/#RoundToEven)
은 인수를 가장 가까운 부동 소수점 정수로 반올림합니다.
`Round`는 반올림 기준점(half-integer)을 더 큰 정수(0에서 먼 쪽)로 반올림하는 반면, `RoundToEven`은 반올림 기준점을 짝수 정수로 반올림합니다.

새로운 함수인 [`Erfinv`](/pkg/math/#Erfinv)와 [`Erfcinv`](/pkg/math/#Erfcinv)는 역 오차 함수(inverse error function)와 역 상보 오차 함수(inverse complementary error function)를 계산합니다.

#### [mime/multipart](/pkg/mime/multipart/)

[`Reader`](/pkg/mime/multipart/#Reader)가 이제 파일 이름(filename) 속성이 비어 있는 파트(part)를 허용합니다.

#### [mime](/pkg/mime/)

[`ParseMediaType`](/pkg/mime/#ParseMediaType)가 이제 유효하지 않은 속성 값을 무시합니다. 이전에는 이러한 값들을 빈 문자열로 반환했습니다.

#### [net](/pkg/net/)

이 패키지의 [`Conn`](/pkg/net/#Conn) 및 [`Listener`](/pkg/net/#Conn) 구현은 이제 `Close`가 반환될 때 기본 파일 디스크립터(file descriptor)가 닫혔음을 보장합니다. (이전 릴리스에서는 `Close`가 다른 고루틴에서 보류 중인 I/O를 중단시킨 경우, `Close`가 반환된 직후 해당 고루틴 중 하나에서 파일 디스크립터가 닫힐 수 있었습니다.)

[`TCPListener`](/pkg/net/#TCPListener)와
[`UnixListener`](/pkg/net/#UnixListener)가
이제 [`syscall.Conn`](/pkg/syscall/#Conn)을 구현하여,
[`syscall.RawConn.Control`](/pkg/syscall/#RawConn)을 통해
기저의 파일 디스크립터(file descriptor)에 옵션을 설정할 수 있게 되었습니다.

[`Pipe`](/pkg/net/#Pipe)에 의해 반환되는 `Conn` 구현체들이 이제 읽기 및 쓰기 데드라인(deadline) 설정을 지원합니다.

[`IPConn.ReadMsgIP`](/pkg/net/#IPConn.ReadMsgIP),
[`IPConn.WriteMsgIP`](/pkg/net/#IPConn.WriteMsgIP),
[`UDPConn.ReadMsgUDP`](/pkg/net/#UDPConn.ReadMsgUDP),
및
[`UDPConn.WriteMsgUDP`](/pkg/net/#UDPConn.WriteMsgUDP)
메서드가 이제 Windows에서 구현되었습니다.

#### [net/http](/pkg/net/http/)

클라이언트 측에서 HTTP 프록시(가장 일반적으로 [`ProxyFromEnvironment`](/pkg/net/http/#ProxyFromEnvironment)로 설정됨)를 이제 `https://` URL로 지정할 수 있습니다. 이는 클라이언트가 표준 프록시 HTTP 요청을 보내기 전에 HTTPS를 통해 프록시에 연결됨을 의미합니다. (이전에는 HTTP 프록시 URL이 반드시 `http://` 또는 `socks5://`로 시작해야 했습니다.)

서버 측에서는, [`FileServer`](/pkg/net/http/#FileServer)와 단일 파일용 대응 함수인 [`ServeFile`](/pkg/net/http/#ServeFile)이 이제 `HEAD` 요청에 대해 `If-Range` 체크를 적용합니다.
`FileServer`는 또한 이제 디렉토리 읽기 실패 시 이를 [`Server`](/pkg/net/http/#Server)의 `ErrorLog`에 보고합니다.
콘텐츠 제공 핸들러들은 이제 길이가 0인 콘텐츠를 제공할 때 `Content-Type` 헤더를 생략합니다.

[`ResponseWriter`](/pkg/net/http/#ResponseWriter)의 `WriteHeader` 메서드는 이제 유효하지 않은(3자리가 아닌) 상태 코드가 전달되면 panic을 발생시킵니다.

<!-- CL 46631 -->
`Handler`가 아무런 출력물을 작성하지 않을 때, `Server`는 더 이상 암시적인 Content-Type을 추가하지 않습니다.

[`Redirect`](/pkg/net/http/#Redirect)가 이제 HTTP 응답을 작성하기 전에 `Content-Type` 헤더를 설정합니다.

#### [net/mail](/pkg/net/mail/)

[`ParseAddress`](/pkg/net/mail/#ParseAddress) 및
[`ParseAddressList`](/pkg/net/mail/#ParseAddressList)가
이제 다양한 구식(obsolete) 주소 형식을 지원합니다.

#### [net/smtp](/pkg/net/smtp/)

[`Client`](/pkg/net/smtp/#Client)에 서버가 여전히 응답하고 있는지 테스트하기 위한 새로운 [`Noop`](/pkg/net/smtp/#Client.Noop) 메서드가 추가되었습니다. 또한 이제 [`Hello`](/pkg/net/smtp/#Client.Hello) 및 [`Verify`](/pkg/net/smtp/#Client.Verify) 메서드의 입력값에서 발생할 수 있는 SMTP 인젝션을 방어합니다.

#### [net/textproto](/pkg/net/textproto/)

[`ReadMIMEHeader`](/pkg/net/textproto/#ReadMIMEHeader)는 이제 연속(들여쓰기 된) 헤더 라인으로 시작하는 모든 헤더를 거부합니다. 이전에는 첫 번째 라인이 들여쓰기 된 헤더의 경우, 첫 번째 라인이 들여쓰기 되지 않은 것처럼 처리되었습니다.

#### [net/url](/pkg/net/url/)

[`ResolveReference`](/pkg/net/url/#ResolveReference)가 이제 대상 URL의 앞부분에 있는 여러 개의 슬래시(//)를 유지합니다.
이전에는 앞부분의 여러 슬래시를 하나의 슬래시로 다시 썼으며, 이로 인해 [`http.Client`](/pkg/net/http/#Client)가 특정 리다이렉션을 잘못 처리하는 결과가 발생했습니다.

예를 들어, 이 코드의 출력 결과가 변경되었습니다:

```go
base, _ := url.Parse("http://host//path//to/page1")
	target, _ := url.Parse("page2")
	fmt.Println(base.ResolveReference(target))
```

`path` 주변의 이중 슬래시(//)에 주의하십시오.
Go 1.9 및 이전 버전에서 해석된 URL은 `http://host/path//to/page2`였습니다.
`path` 앞의 이중 슬래시는 잘못하여 단일 슬래시로 재작성되었으며, `path` 뒤의 이중 슬래시는 올바르게 유지되었습니다.
Go 1.10은 [RFC 3986](https://tools.ietf.org/html/rfc3986#section-5.2)의 요구 사항에 따라 두 이중 슬래시를 모두 유지하여 `http://host//path//to/page2`로 해석합니다.

이 변경 사항은 경로 시작 부분에 실수로 이중 슬래시(//)가 포함된 기본 URL을 생성하고, `ResolveReference`가 이를 수정해 줄 것에 의도치 않게 의존하고 있던 기존의 버그성 프로그램들을 작동 불능 상태로 만들 수 있습니다.

예를 들어, 코드에서 `/my/api`와 같은 경로에 `http://host/`와 같은 호스트 접두사를 추가하여 `http://host//my/api`와 같이 이중 슬래시가 포함된 URL이 생성되는 경우에 이러한 현상이 발생할 수 있습니다.

[`UserInfo`](/pkg/net/url/#UserInfo)의 메서드들이 이제 nil 수신자(receiver)를 zero `UserInfo`를 가리키는 포인터와 동일하게 처리합니다. 이전에는 패닉(panic)이 발생했습니다.

#### [os](/pkg/os/)

[`File`](/pkg/os/#File)에 새로운 메서드인
[`SetDeadline`](/pkg/os/#File.SetDeadline),
[`SetReadDeadline`](/pkg/os/#File.SetReadDeadline),
그리고
[`SetWriteDeadline`](/pkg/os/#File.SetWriteDeadline)가 추가되었습니다.
이 메서드들은 기본 파일 디스크립터가 논블로킹(non-blocking) I/O 작업을 지원하는 경우 I/O 데드라인을 설정할 수 있게 해줍니다.
이 메서드들의 정의는 [`net.Conn`](/pkg/net/#Conn)의 정의와 일치합니다.
I/O 메서드가 데드라인 초과로 인해 실패하면 타임아웃 에러를 반환하며,
새로 추가된 [`IsTimeout`](/pkg/os/#IsTimeout) 함수를 통해 에러가 타임아웃을 나타내는지 확인할 수 있습니다.

`net.Conn`과 마찬가지로, `File`의 [`Close`](/pkg/os/#File.Close) 메서드는 이제 `Close`가 반환될 때 기저의 파일 디스크립터(file descriptor)가 닫혔음을 보장합니다.
(이전 릴리스에서는 `Close`가 다른 goroutine에서 대기 중인 I/O를 중단시킨 경우, 파일 디스크립터의 닫힘 작업이 `Close`가 반환된 직후 해당 goroutine 중 하나에서 발생할 수 있었습니다.)

BSD, macOS 및 Solaris 시스템에서,
[`Chtimes`](/pkg/os/#Chtimes)
가 이제 나노초 정밀도로 파일 시간을 설정하는 것을 지원합니다
(기저 파일 시스템이 이를 표현할 수 있다는 가정 하에).

#### [reflect](/pkg/reflect/)

[`Copy`](/pkg/reflect/#Copy) 함수는 이제 [내장 copy 함수](/pkg/builtin/#copy)와 일치하도록 문자열(string)에서 바이트 배열(byte array) 또는 바이트 슬라이스(byte slice)로 복사하는 것을 허용합니다.

구조체(structs)에서 공개되지 않은(unexported) 구조체 타입에 대한 내장 포인터(embedded pointers)가 해당 [StructField](/pkg/reflect/#StructField)에서 `PkgPath`가 비어 있는 것으로 잘못 보고되었습니다. 그 결과, 해당 필드들에 대해 [`Value.CanSet`](/pkg/reflect/#Value.CanSet)이 잘못되게 true를 반환하고 [`Value.Set`](/pkg/reflect/#Value.Set)이 잘못되게 성공했습니다.

기저 메타데이터가 수정되었습니다. 이제 해당 필드들에 대해 `CanSet`은 올바르게 false를 반환하며, `Set`은 올바르게 패닉(panic)을 발생시킵니다. 이는 이전에는 이러한 필드들에 언마셜(unmarshal)할 수 있었으나 이제는 불가능해진 리플렉션 기반의 언마셜러에 영향을 줄 수 있습니다. 예를 들어, [`encoding/json` 참고 사항](#encoding/json)을 확인하십시오.

#### [runtime/pprof](/pkg/runtime/pprof/)

[위에서 언급했듯이](#pprof), blocking 및 mutex 프로파일에는 이제 심볼 정보가 포함되어 있어, 이를 생성한 바이너리 없이도 확인할 수 있습니다.

#### [strconv](/pkg/strconv/)

[`ParseUint`](/pkg/strconv/#ParseUint)는 이제 `ErrRange` 오류가 발생할 때 문서에 명시된 대로 해당 크기의 최대 크기 정수를 반환합니다. 이전에는 `ErrRange` 오류와 함께 0을 반환했습니다.

#### [strings](/pkg/strings/)

새로운 타입인 [`Builder`](/pkg/strings/#Builder)는 텍스트를 `string` 결과로 누적하는 유스케이스에서 [`bytes.Buffer`](/pkg/bytes/#Buffer)를 대체하는 수단입니다.
`Builder`의 API는 `bytes.Buffer` API의 제한된 서브셋으로, [`String`](/pkg/strings/#Builder.String) 메서드 호출 시 데이터의 중복 복사본을 생성하는 것을 안전하게 피할 수 있게 해줍니다.

#### [syscall](/pkg/syscall/)

Windows에서,
[`SysProcAttr`](/pkg/syscall/#SysProcAttr)의 새로운 `Token` 필드는
[`Token`](/pkg/syscall/#Token) 타입으로, [`StartProcess`](/pkg/syscall/#StartProcess) 동안
(따라서 [`os.StartProcess`](/pkg/os/#StartProcess) 및
[`exec.Cmd.Start`](/pkg/os/exec/#Cmd.Start) 동안에도) 다른 사용자로
실행되는 프로세스를 생성할 수 있게 해줍니다.
새로운 함수인 [`CreateProcessAsUser`](/pkg/syscall/#CreateProcessAsUser)를 통해
기저에 있는 시스템 콜에 접근할 수 있습니다.

BSD, macOS 및 Solaris 시스템에서 [`UtimesNano`](/pkg/syscall/#UtimesNano)가 이제 구현되었습니다.

#### [time](/pkg/time/)

[`LoadLocation`](/pkg/time/#LoadLocation)은 이제 기본 시스템별 설치 경로 목록이나 `$GOROOT/lib/time/zoneinfo.zip`을 확인하기 전에, `$ZONEINFO` 환경 변수에 지정된 디렉터리 또는 압축되지 않은 zip 파일을 먼저 사용합니다.

새로운 함수 [`LoadLocationFromTZData`](/pkg/time/#LoadLocationFromTZData)를 통해 IANA 시간대 파일 데이터를 [`Location`](/pkg/time/#Location)으로 변환할 수 있습니다.

#### [unicode](/pkg/unicode/)

[`unicode`](/pkg/unicode/) 패키지와 시스템 전반의 관련 지원 사항이 Unicode 9.0에서 [Unicode 10.0](https://www.unicode.org/versions/Unicode10.0.0/)으로 업그레이드되었습니다. 이번 업데이트를 통해 4개의 새로운 스크립트, 1개의 새로운 속성, 비트코인 통화 기호, 그리고 56개의 새로운 이모지를 포함하여 총 8,518개의 새로운 문자가 추가되었습니다.
