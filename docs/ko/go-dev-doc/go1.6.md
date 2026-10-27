제공해주신 내용에는 번역할 텍스트가 포함되어 있지 않으며, HTML 주석 내의 정규식 치환 패턴(sed 스타일)만 포함되어 있습니다.

해당 부분은 코드/스크립트의 일부이므로 기술적 무결성을 위해 번역하지 않고 그대로 유지합니다. 번역할 본문 내용을 제공해 주시면 정성껏 번역해 드리겠습니다.

<!--
Edit .,s;^PKG:([a-z][A-Za-z0-9_/]+);<a href="/pkg/\1/"><code>\1</code></a>;g
Edit .,s;^([a-z][A-Za-z0-9_/]+)\.([A-Z][A-Za-z0-9_]+\.)?([A-Z][A-Za-z0-9_]+)([ .',]|$);<a href="/pkg/\1/#\2\3"><code>\3</code></a>\4;g
-->

<style>
  main ul li { margin: 0.5em 0; }
</style>

## Go 1.6 소개 {#introduction}

최신 Go 릴리스인 버전 1.6가 1.5 출시 6개월 만에 공개되었습니다.
대부분의 변경 사항은 언어, 런타임 및 라이브러리의 구현 부분에 집중되어 있습니다.
언어 명세(language specification)에는 변경 사항이 없습니다.
언제나 그랬듯, 이번 릴리스에서도 Go 1의 [호환성 약속](/doc/go1compat.html)을 유지합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

이번 릴리스에서는 [64비트 MIPS 기반 Linux 및 32비트 x86 기반 Android](#ports)에 대한 새로운 포트가 추가되었으며,
[C와 Go 포인터를 공유하기 위한](#cgo) 정의 및 강제 규칙이 도입되었습니다.
또한 [HTTP/2](#http2)에 대한 투명하고 자동화된 지원과
[템플릿 재사용](#template)을 위한 새로운 메커니즘이 추가되었습니다.

## 언어 변경 사항 {#language}

이번 릴리스에서는 언어 변경 사항이 없습니다.

## 포트 {#ports}

Go 1.6에서는 64비트 MIPS Linux(`linux/mips64` 및 `linux/mips64le`)에 대한 실험적 포트가 추가되었습니다.
이 포트들은 `cgo`를 지원하지만, 내부 링킹(internal linking)을 통해서만 가능합니다.

Go 1.6는 32비트 x86(`android/386`) 기반의 Android 실험적 포트를 추가했습니다.

FreeBSD에서 Go 1.6은 외부 C 컴파일러로 `gcc`가 아닌 `clang`을 사용하는 것이 기본 설정입니다.

리틀 엔디안 64비트 PowerPC(`linux/ppc64le`) 기반의 Linux에서,
Go 1.6은 이제 외부 링킹을 통한 `cgo`를 지원하며
대략적으로 기능 구현이 완료되었습니다.

NaCl에서 Go 1.5는 SDK 버전 pepper-41이 필요했습니다.
Go 1.6에서는 더 최신 SDK 버전에 대한 지원이 추가되었습니다.

`-dynlink` 또는 `-shared` 컴파일 모드를 사용하는 32비트 x86 시스템에서, 이제 CX 레지스터는 특정 메모리 참조에 의해 덮어씌워지므로 수동으로 작성한 어셈블리에서는 사용을 피해야 합니다.
자세한 내용은 [어셈블리 문서](/doc/asm#x86)를 참조하십시오.

## 도구 {#tools}

### Cgo {#cgo}

[`cgo`](/cmd/cgo/)에 한 가지 주요 변경 사항과 한 가지 부수적인 변경 사항이 있습니다.

가장 주요한 변경 사항은 Go 포인터를 C 코드와 공유하기 위한 규칙의 정의이며, 이는 해당 C 코드가 Go의 가비지 컬렉터와 공존할 수 있도록 하기 위함입니다. 간단히 말해, Go와 C는 `cgo` 호출의 일부로 해당 메모리에 대한 포인터가 C로 전달될 때 Go가 할당한 메모리를 공유할 수 있습니다. 단, 해당 메모리 자체가 Go가 할당한 메모리에 대한 포인터를 포함하고 있지 않아야 하며, C가 호출 종료 후에도 해당 포인터를 유지하지 않아야 한다는 조건이 있습니다. 이러한 규칙은 프로그램 실행 중에 런타임에 의해 확인됩니다. 런타임이 위반 사항을 감지하면 진단 내용을 출력하고 프로그램을 종료(crash)시킵니다. 환경 변수 `GODEBUG=cgocheck=0`을 설정하여 이 확인 과정을 비활성화할 수 있지만, 이 확인 과정에서 식별된 코드의绝대다수는 어떤 방식으로든 가비지 컬렉션과 미묘하게 호환되지 않는다는 점에 유의하십시오. 확인 과정을 비활성화하면 일반적으로 더 미스터리한 실패 모드로 이어질 뿐입니다. 확인 과정을 끄는 것보다 문제가 되는 코드를 수정하는 것이 강력히 권장됩니다. 자세한 내용은 [`cgo` 문서](/cmd/cgo/#hdr-Passing_pointers)를 참조하십시오.

소소한 변경 사항은 Go의 `complex64` 및 `complex128`과 별개로, 명시적인 `C.complexfloat` 및 `C.complexdouble` 타입이 추가되었다는 점입니다. 다른 숫자 타입들과 마찬가지로, C의 복소수 타입과 Go의 복소수 타입은 더 이상 상호 교환 가능하지 않습니다.

### 컴파일러 툴체인 {#compiler}

컴파일러 툴체인은 대부분 변경되지 않았습니다.
내부적으로 가장 중요한 변경 사항은 파서(parser)가 더 이상 [yacc](/cmd/yacc/)로 생성되지 않고 이제 직접 작성(hand-written)되었다는 점입니다.

컴파일러, 링커, 그리고 `go` 명령에 `-race`와 유사한 새로운 플래그인 `-msan`이 추가되었습니다. 이 플래그는 linux/amd64에서만 사용할 수 있으며, [Clang MemorySanitizer](https://clang.llvm.org/docs/MemorySanitizer.html)와의 상호 운용을 활성화합니다. 이러한 상호 운용은 주로 의심스러운 C 또는 C++ 코드가 포함된 프로그램을 테스트할 때 유용합니다.

링커에 [`cgo`](/cmd/cgo/) 코드를 링크할 때 C 컴파일러 지원 라이브러리의 예상 위치를 설정하는 새로운 옵션 `-libgcc`가 추가되었습니다. 이 옵션은 `-linkmode=internal`을 사용할 때만 참조되며, `none`으로 설정하여 지원 라이브러리 사용을 비활성화할 수 있습니다.

[Go 1.5에서 시작된 빌드 모드 구현](/doc/go1.5#link)이 더 많은 시스템으로 확장되었습니다.
이번 릴리스에서는 `android/386`, `android/amd64`, `android/arm64`, `linux/386`, `linux/arm64` 시스템의 `c-shared` 모드 지원이 추가되었습니다.
또한 `linux/386`, `linux/arm`, `linux/amd64`, `linux/ppc64le` 시스템의 `shared` 모드 지원과,
`android/386`, `android/amd64`, `android/arm`, `android/arm64`, `linux/386`, `linux/amd64`, `linux/arm`, `linux/arm64`, `linux/ppc64le` 시스템의 새로운 `pie` 모드(위치 독립 실행 파일 생성) 지원이 추가되었습니다.
자세한 내용은 [설계 문서](/s/execmodes)를 참조하십시오.

참고로, Go 1.5에서 링커의 `-X` 플래그가 변경되었습니다.
Go 1.4 및 그 이전 버전에서는 다음과 같이 두 개의 인자를 받았습니다.

-X importpath.name value

Go 1.5에서는 단일 인수를 사용하는 대체 구문이 추가되었으며, 이 인수는 그 자체로 `name=value` 쌍입니다:

-X importpath.name=value

Go 1.5에서는 새로운 구문 사용을 권장하는 경고 메시지를 출력하며 기존 구문을 여전히 허용했습니다.
Go 1.6에서도 기존 구문을 계속 허용하며 경고 메시지를 출력합니다.
Go 1.7에서는 기존 구문에 대한 지원이 제거될 예정입니다.

### Gccgo {#gccgo}

GCC와 Go 프로젝트의 릴리스 일정은 서로 일치하지 않습니다.
GCC 릴리스 5에는 gccgo의 Go 1.4 버전이 포함되어 있습니다.
다음 릴리스인 GCC 6에는 gccgo의 Go 1.6.1 버전이 포함될 예정입니다.

### Go command {#go_command}

[`go`](/cmd/go) 명령의 기본 동작은 변경되지 않았지만, 주목할 만한 몇 가지 변경 사항이 있습니다.

Go 1.5에서는 `GO15VENDOREXPERIMENT` 환경 변수를 `1`로 설정하여 활성화할 수 있는 vendoring에 대한 실험적 지원이 도입되었습니다.
Go 1.6에서도 vendoring 지원이 유지되며, 더 이상 실험적인 기능으로 간주되지 않고 기본적으로 활성화됩니다.
`GO15VENDOREXPERIMENT` 환경 변수를 `0`으로 설정하여 명시적으로 비활성화할 수 있습니다.
Go 1.7에서는 해당 환경 변수에 대한 지원이 제거될 예정입니다.

기본적으로 벤더링(vendoring)을 활성화했을 때 발생할 가능성이 가장 높은 문제는, 새로운 벤더링 시맨틱에 따라 해석되는 것을 의도하지 않은 `vendor`라는 이름의 기존 디렉토리가 소스 트리 내에 포함되어 있는 경우에 발생합니다. 이 경우, 가장 간단한 해결 방법은 해당 디렉토리의 이름을 `vendor`가 아닌 다른 이름으로 변경하고, 영향을 받는 모든 임포트 경로(import paths)를 업데이트하는 것입니다.

벤더링(vendoring)에 대한 자세한 내용은
[`go` 명령어](/cmd/go/#hdr-Vendor_Directories) 문서와
[설계 문서](/s/go15vendor)를 참조하십시오.

새로운 빌드 플래그인 `-msan`이 추가되었습니다.
이 플래그는 LLVM memory sanitizer 지원과 함께 Go를 컴파일합니다.
이는 주로 memory sanitizer로 검사 중인 C 또는 C++ 코드와 링크할 때 사용하도록 설계되었습니다.

### Go doc 명령어 {#doc_command}

Go 1.5에서는 [`go doc`](/cmd/go/#hdr-Show_documentation_for_package_or_symbol) 명령어가 도입되어, `go` `doc` `http`와 같이 패키지 이름만으로 패키지를 참조할 수 있게 되었습니다.
모호함이 발생하는 경우, Go 1.5의 동작 방식은 사전순으로 가장 빠른 임포트 경로(import path)를 가진 패키지를 사용하는 것이었습니다.
Go 1.6에서는 요소 수가 더 적은 임포트 경로를 우선시하며, 동일한 경우 사전순 비교를 통해 모호함을 해결합니다.
이 변경 사항의 중요한 영향은 이제 벤더링된(vendored) 복사본보다 패키지의 원본 복사본이 우선시된다는 점입니다.
또한 성공적인 검색 속도가 빨라지는 경향이 있습니다.

### Go vet 명령 {#vet_command}

[`go vet`](/cmd/vet) 명령어가 이제 `Printf`에 함수나 메서드 값을 인자로 전달하는 경우를 진단합니다. 예를 들어, `f()`를 의도했으나 `f`를 전달하는 경우 등이 이에 해당합니다.

## 성능 {#performance}

언제나 그렇듯, 변경 사항이 매우 일반적이고 다양하여 성능에 대해 정확하게 진술하기는 어렵습니다.
어떤 프로그램은 더 빠르게 실행될 수도 있고, 어떤 프로그램은 더 느려질 수도 있습니다.
평균적으로 Go 1 벤치마크 슈트의 프로그램들은 Go 1.5에서보다 Go 1.6에서 몇 퍼센트 더 빠르게 실행됩니다.
가비지 컬렉터(garbage collector)의 일시 중단(pause) 시간은 Go 1.5보다 더 짧아졌으며, 특히 많은 양의 메모리를 사용하는 프로그램에서 더욱 그러합니다.

[`compress/bzip2`](/pkg/compress/bzip2/),
[`compress/gzip`](/pkg/compress/gzip/),
[`crypto/aes`](/pkg/crypto/aes/),
[`crypto/elliptic`](/pkg/crypto/elliptic/),
[`crypto/ecdsa`](/pkg/crypto/ecdsa/), 그리고
[`sort`](/pkg/sort/) 패키지의 구현체에 10% 이상의 성능 향상을 가져오는 상당한 최적화가 이루어졌습니다.

## 표준 라이브러리 {#library}

### HTTP/2 {#http2}

Go 1.6에서는 [`net/http`](/pkg/net/http/) 패키지에 새로운 [HTTP/2 프로토콜](https://http2.github.io/)에 대한 투명한 지원이 추가되었습니다.
Go 클라이언트와 서버는 HTTPS를 사용할 때 상황에 맞춰 자동으로 HTTP/2를 사용합니다.
HTTP/1.1과 마찬가지로, HTTP/2 프로토콜 처리의 세부 사항에 특화된 공개(exported) API는 제공되지 않습니다.

HTTP/2를 비활성화해야 하는 프로그램은
(클라이언트의 경우) [`Transport.TLSNextProto`](/pkg/net/http/#Transport) 또는
(서버의 경우) [`Server.TLSNextProto`](/pkg/net/http/#Server)를
nil이 아닌 빈 맵으로 설정하여 비활성화할 수 있습니다.

HTTP/2 프로토콜의 세부 사항을 조정해야 하는 프로그램은 [`golang.org/x/net/http2`](https://golang.org/x/net/http2)를 임포트하여 사용할 수 있으며, 특히 [ConfigureServer](https://godoc.org/golang.org/x/net/http2/#ConfigureServer) 및 [ConfigureTransport](https://godoc.org/golang.org/x/net/http2/#ConfigureTransport) 함수를 활용할 수 있습니다.

### 런타임 {#runtime}

런타임에 맵(map)의 동시성 오용을 감지하는 경량의 최선 노력(best-effort) 감지 기능이 추가되었습니다.
언제나 그렇듯이, 한 고루틴이 맵에 쓰고 있다면 다른 어떤 고루틴도 동시에 해당 맵을 읽거나 써서는 안 됩니다.
런타임이 이러한 상태를 감지하면 진단 내용을 출력하고 프로그램을 충돌(crash)시킵니다.
이 문제에 대해 더 자세히 알아보는 가장 좋은 방법은 [race detector](/blog/race-detector)를 사용하여 프로그램을 실행하는 것이며, 이를 통해 데이터 경합(race)을 더 확실하게 식별하고 더 상세한 정보를 얻을 수 있습니다.

프로그램을 종료시키는 패닉(panic)이 발생했을 때, 이제 런타임은 기본적으로 모든 고루틴이 아닌 현재 실행 중인 고루틴의 스택만 출력합니다.
보통 패닉과 관련이 있는 것은 현재 고루틴뿐이므로, 다른 고루틴들을 생략하면 크래시 메시지에서 불필요한 출력을 크게 줄일 수 있습니다.
크래시 메시지에서 모든 고루틴의 스택을 확인하려면, 환경 변수 `GOTRACEBACK`을 `all`로 설정하거나 크래시 발생 전에 [`debug.SetTraceback`](/pkg/runtime/debug/#SetTraceback)을 호출한 후 프로그램을 다시 실행하십시오.
자세한 내용은 [런타임 문서](/pkg/runtime/#hdr-Environment_Variables)를 참조하십시오.

_업데이트_:
타임아웃이 감지되었을 때나 수신된 시그널을 명시적으로 처리할 때와 같이, 전체 프로그램의 상태를 덤프하려는 의도로 발생하는 Uncaught panic은 이제 패닉이 발생하기 전에 `debug.SetTraceback("all")`을 호출해야 합니다.
[`signal.Notify`](/pkg/os/signal/#Notify) 사용 사례를 검색하면 이러한 코드를 식별하는 데 도움이 될 수 있습니다.

Windows에서 Go 1.5 및 그 이전 버전의 Go 프로그램은 시작 시 `timeBeginPeriod(1)`을 호출하여 전역 Windows 타이머 해상도를 1ms로 강제 설정했습니다.
이제 Go는 우수한 스케줄러 성능을 위해 더 이상 이 작업이 필요하지 않으며, 전역 타이머 해상도를 변경하는 것이 일부 시스템에서 문제를 일으켰기 때문에 해당 호출이 제거되었습니다.

`-buildmode=c-archive` 또는 `-buildmode=c-shared`를 사용하여 아카이브나 공유 라이브러리를 빌드할 때, 시그널 처리 방식이 변경되었습니다.

Go 1.5에서는 아카이브나 공유 라이브러리가 대부분의 시그널에 대해 시그널 핸들러를 설치했습니다.

Go 1.6에서는 Go 코드의 런타임 패닉을 처리하는 데 필요한 동기식 시그널인 `SIGBUS`, `SIGFPE`, `SIGSEGV`에 대해서만 시그널 핸들러를 설치합니다.

자세한 내용은 [os/signal](/pkg/os/signal) 패키지를 참조하십시오.

### Reflect {#reflect}

[`reflect`](/pkg/reflect/) 패키지에서 내보내지 않은(unexported) 구조체 타입이 내보낸(exported) 필드를 포함하고 있을 때, gc와 gccgo 툴체인 사이에 오랫동안 존재했던 [호환성 문제](/issue/12367)가 해결되었습니다.

리플렉션을 사용하여 데이터 구조를 탐색하는 코드, 특히 [`encoding/json`](/pkg/encoding/json/) 및 [`encoding/xml`](/pkg/encoding/xml/) 패키지의 방식대로 직렬화를 구현하는 코드는 업데이트가 필요할 수 있습니다.

이 문제는 리플렉션을 사용하여 내장된(embedded) 비공개(unexported) 구조체 타입 필드를 거쳐 해당 구조체의 공개(exported) 필드에 접근하려 할 때 발생합니다.
이전에는 `reflect`가 빈 `Field.PkgPath`를 반환함으로써 내장된 필드를 공개된 것으로 잘못 보고했습니다.
이제는 해당 필드를 비공개로 정확하게 보고하지만, 구조체 내부에 포함된 공개 필드에 대한 접근 권한을 평가할 때는 이 사실을 무시합니다.

_업데이트_:
일반적으로, 이전에는 구조체를 순회하며 사용했던 코드가

`f.PkgPath != ""`

접근 불가능한 필드를 제외하려면
이제 다음을 사용해야 합니다

`f.PkgPath != "" && !f.Anonymous`

예를 들어, [`encoding/json`](https://go-review.googlesource.com/#/c/14011/2/src/encoding/json/encode.go) 및 [`encoding/xml`](https://go-review.googlesource.com/#/c/14012/2/src/encoding/xml/typeinfo.go)의 구현 변경 사항을 확인하십시오.

### 정렬 {#sort}

[`sort`](/pkg/sort/) 패키지에서, [`Sort`](/pkg/sort/#Sort)의 구현이 다시 작성되었습니다. 이를 통해 [`Interface`](/pkg/sort/#Interface)의 `Less` 및 `Swap` 메서드 호출 횟수를 약 10% 줄였으며, 이에 따라 전체적인 실행 시간이 단축되었습니다. 새로운 알고리즘은 값이 동일하다고 비교되는 경우(`Less(i,` `j)`와 `Less(j,` `i)`가 모두 false인 쌍들) 이전과는 다른 순서를 선택합니다.

_업데이트_:
`Sort`의 정의는 동일한 값들의 최종 순서에 대해 아무런 보장을 하지 않지만, 새로운 동작 방식은 여전히 특정 순서를 기대하는 프로그램들을 중단시킬 수 있습니다.
이러한 프로그램들은 원하는 순서를 보고하도록 `Less` 구현을 개선하거나,
동일한 값들의 원래 입력 순서를 유지하는
[`Stable`](/pkg/sort/#Stable)로 전환해야 합니다.

### 템플릿 {#template}

[text/template](/pkg/text/template/) 패키지에는 템플릿 작성을 더 쉽게 만들기 위한 두 가지 중요한 새로운 기능이 추가되었습니다.

우선, 이제 [템플릿 액션 주변의 공백을 제거](/pkg/text/template/#hdr-Text_and_spaces)할 수 있게 되었으며, 이를 통해 템플릿 정의의 가독성을 높일 수 있습니다.
액션 시작 부분의 마이너스(`-`) 기호는 액션 이전의 공백을 제거하라는 의미이며, 액션 끝 부분의 마이너스(`-`) 기호는 액션 이후의 공백을 제거하라는 의미입니다.
예를 들어, 다음과 같은 템플릿은

{{23 -}}
	   <
	{{- 45}}

`23<45`와 같은 형식입니다.

둘째로, 새로운 [`{{block}}` 액션](/pkg/text/template/#hdr-Actions)은 이름이 지정된 템플릿의 재정의를 허용함으로써, 서로 다른 인스턴스화 과정에서 교체될 수 있는 템플릿 조각들을 정의하는 간단한 방법을 제공합니다. `text/template` 패키지에 이 새로운 기능을 보여주는 [예제](/pkg/text/template/#example_Template_block)가 있습니다.

### 라이브러리의 소규모 변경 사항 {#minor_library_changes}

- [`archive/tar`](/pkg/archive/tar/) 패키지의 구현체에서 파일 형식의 드문 코너 케이스에 발생하던 많은 버그가 수정되었습니다. 눈에 띄는 변경 사항 중 하나는 [`Reader`](/pkg/archive/tar/#Reader) 타입의 [`Read`](/pkg/archive/tar/#Reader.Read) 메서드가 이제 특수 파일 타입의 내용을 빈 상태로 표시하며 즉시 `io.EOF`를 반환한다는 점입니다.
  - [`archive/zip`](/pkg/archive/zip/) 패키지에서 [`Reader`](/pkg/archive/zip/#Reader) 타입에 [`RegisterDecompressor`](/pkg/archive/zip/#Reader.RegisterDecompressor) 메서드가 추가되었고, [`Writer`](/pkg/archive/zip/#Writer) 타입에 [`RegisterCompressor`](/pkg/archive/zip/#Writer.RegisterCompressor) 메서드가 추가되어 개별 zip 파일에 대한 압축 옵션을 제어할 수 있게 되었습니다. 이들은 기존의 전역 [`RegisterDecompressor`](/pkg/archive/zip/#RegisterDecompressor) 및 [`RegisterCompressor`](/pkg/archive/zip/#RegisterCompressor) 함수보다 우선순위가 높습니다.
  - [`bufio`](/pkg/bufio/) 패키지의 [`Scanner`](/pkg/bufio/#Scanner) 타입에 스캐닝 중에 사용할 초기 버퍼와 최대 버퍼 크기를 지정할 수 있는 [`Buffer`](/pkg/bufio/#Scanner.Buffer) 메서드가 추가되었습니다. 이를 통해 필요한 경우 `MaxScanTokenSize`보다 큰 토큰을 스캔할 수 있습니다. 또한 `Scanner`를 위해 [분할 함수](/pkg/bufio/#SplitFunc)가 처리를 중단하거나 최종 빈 토큰을 반환하는 데 사용할 수 있는 [`ErrFinalToken`](/pkg/bufio/#ErrFinalToken) 에러 값이 정의되었습니다.
  - [`compress/flate`](/pkg/compress/flate/) 패키지에서 [`ReadError`](/pkg/compress/flate/#ReadError) 및 [`WriteError`](/pkg/compress/flate/#WriteError) 에러 구현이 deprecated 되었습니다. Go 1.5에서는 에러 발생 시 매우 드물게 반환되었으나, 이제는 반환되지 않습니다. 다만 호환성을 위해 정의는 유지됩니다.
  - [`compress/flate`](/pkg/compress/flate/), [`compress/gzip`](/pkg/compress/gzip/), [`compress/zlib`](/pkg/compress/zlib/) 패키지가 이제 잘린 입력 스트림에 대해 [`io.EOF`](/pkg/io/#EOF) 대신 [`io.ErrUnexpectedEOF`](/pkg/io/#ErrUnexpectedEOF)를 보고합니다.
  - [`crypto/cipher`](/pkg/crypto/cipher/) 패키지는 이제 GCM 복호화 실패 시 대상 버퍼를 덮어씁니다. 이는 AESNI 코드가 임시 버퍼를 사용하지 않도록 하기 위함입니다.
  - [`crypto/tls`](/pkg/crypto/tls/) 패키지에 다양한 소규모 변경 사항이 있습니다. 이제 [`Config`](/pkg/crypto/tls/#Config)의 `Certificates`가 nil이더라도 `GetCertificate` 콜백이 설정되어 있다면 [`Listen`](/pkg/crypto/tls/#Listen)이 성공합니다. 또한 AES-GCM 사이퍼 스위트를 사용하는 RSA 지원이 추가되었으며, 클라이언트(특히 [`net/http`](/pkg/net/http/) 패키지)가 non-TLS 서버에 TLS 연결을 시도할 때 더 정확한 에러를 보고할 수 있도록 [`RecordHeaderError`](/pkg/crypto/tls/#RecordHeaderError)가 추가되었습니다.
  - [`crypto/x509`](/pkg/crypto/x509/) 패키지는 이제 인증서에 음수 일련번호가 포함되는 것을 허용하며(기술적으로는 에러지만 실제로는 흔한 경우임), MD5와 같은 안전하지 않은 알고리즘으로 서명된 인증서를 거부할 때 더 나은 에러 메시지를 제공하기 위해 새로운 [`InsecureAlgorithmError`](/pkg/crypto/x509/#InsecureAlgorithmError)를 정의합니다.
  - [`debug/dwarf`](/pkg/debug/dwarf) 및 [`debug/elf`](/pkg/debug/elf/) 패키지가 함께 압축된 DWARF 섹션 지원을 추가했습니다. 사용자 코드를 업데이트할 필요는 없으며, 섹션을 읽을 때 자동으로 압축이 해제됩니다.
  - [`debug/elf`](/pkg/debug/elf/) 패키지가 일반적인 압축 ELF 섹션 지원을 추가했습니다. 사용자 코드를 업데이트할 필요는 없으며, 섹션을 읽을 때 자동으로 압축이 해제됩니다. 다만, 압축된 [`Sections`](/pkg/debug/elf/#Section)는 임의 접근(random access)을 지원하지 않으며, `ReaderAt` 필드가 nil입니다.
  - [`encoding/asn1`](/pkg/encoding/asn1/) 패키지가 이제 ASN.1 구조의 고급 파싱에 유용한 [태그 및 클래스 상수](/pkg/encoding/asn1/#pkg-constants)를 export 합니다.
  - 또한 [`encoding/asn1`](/pkg/encoding/asn1/) 패키지에서 [`Unmarshal`](/pkg/encoding/asn1/#Unmarshal)이 이제 다양한 비표준 정수 및 길이 인코딩을 거부합니다.
  - [`encoding/base64`](/pkg/encoding/base64) 패키지의 [`Decoder`](/pkg/encoding/base64/#Decoder)가 입력의 마지막 바이트들을 처리하도록 수정되었습니다. 이전에는 가능한 한 많은 4바이트 토큰을 처리하고 최대 3바이트의 나머지는 무시했습니다. 따라서 `Decoder`는 이제 패딩이 없는 인코딩(예: [RawURLEncoding](/pkg/encoding/base64/#RawURLEncoding))의 입력을 올바르게 처리하지만, 패딩이 있는 인코딩에서 잘렸거나 후행 공백과 같은 잘못된 바이트로 끝나는 입력은 거부합니다.
  - [`encoding/json`](/pkg/encoding/json/) 패키지는 이제 [`Number`](/pkg/encoding/json/#Number)를 마샬링하기 전에 구문을 확인하여 숫자 값에 대한 JSON 사양을 준수하는지 요구합니다. 이전 릴리스와 마찬가지로, zero `Number`(빈 문자열)는 리터럴 0(zero)으로 마샬링됩니다.
  - [`encoding/xml`](/pkg/encoding/xml/) 패키지의 [`Marshal`](/pkg/encoding/xml/#Marshal) 함수가 이제 `chardata`와 유사하게 인수를 하나 이상의 `<![CDATA[ ... ]]>` 태그로 인코딩하는 `cdata` 속성을 지원합니다.
  - 또한 [`encoding/xml`](/pkg/encoding/xml/) 패키지에서 [`Decoder`](/pkg/encoding/xml/#Decoder)의 [`Token`](/pkg/encoding/xml/#Decoder.Token) 메서드가 이제 모든 열린 태그가 닫히기 전에 EOF를 만나면 에러를 보고합니다. 이는 입력의 태그가 적절히 매칭되어야 한다는 일반적인 요구 사항과 일치합니다. 이 요구 사항을 피하려면 [`RawToken`](/pkg/encoding/xml/#Decoder.RawToken)을 사용하십시오.
  - [`fmt`](/pkg/fmt/) 패키지는 이제 [`Printf`](/pkg/fmt/#Printf)의 `*` 너비 및 정밀도 지정 인수로 모든 정수 타입을 허용합니다. 이전 릴리스에서는 `*`에 대한 인수가 반드시 `int` 타입이어야 했습니다.
  - 또한 [`fmt`](/pkg/fmt/) 패키지에서 [`Scanf`](/pkg/fmt/#Scanf)가 이제 %x의 별칭으로 %X를 사용하여 16진수 문자열을 스캔할 수 있습니다. 두 형식 모두 대소문자가 섞인 16진수를 허용합니다.
  - [`image`](/pkg/image/) 및 [`image/color`](/pkg/image/color/) 패키지에 프리멀티플라이되지 않은 알파(non-premultiplied alpha)를 가진 Y'CbCr 이미지를 지원하기 위해 [`NYCbCrA`](/pkg/image/#NYCbCrA) 및 [`NYCbCrA`](/pkg/image/color/#NYCbCrA) 타입이 추가되었습니다.
  - [`io`](/pkg/io/) 패키지의 [`MultiWriter`](/pkg/io/#MultiWriter) 구현체에 [`WriteString`](/pkg/io/#WriteString)에서 사용할 수 있는 `WriteString` 메서드가 구현되었습니다.
  - [`math/big`](/pkg/math/big/) 패키지에서 [`Int`](/pkg/math/big/#Int)에 출력 제어력을 높이기 위한 [`Append`](/pkg/math/big/#Int.Append) 및 [`Text`](/pkg/math/big/#Int.Text) 메서드가 추가되었습니다.
  - 또한 [`math/big`](/pkg/math/big/) 패키지에서 [`Float`](/pkg/math/big/#Float)가 이제 [`encoding.TextMarshaler`](/pkg/encoding/#TextMarshaler) 및 [`encoding.TextUnmarshaler`](/pkg/encoding/#TextUnmarshaler)를 구현하여 [`encoding/json`](/pkg/encoding/json/) 및 [`encoding/xml`](/pkg/encoding/xml/) 패키지에 의해 자연스러운 형태로 직렬화될 수 있습니다.
  - 또한 [`math/big`](/pkg/math/big/) 패키지에서 [`Float`](/pkg/math/big/#Float)의 [`Append`](/pkg/math/big/#Float.Append) 메서드가 이제 특별한 정밀도 인수 -1을 지원합니다. [`strconv.ParseFloat`](/pkg/strconv/#ParseFloat)와 마찬가지로, 정밀도 -1은 결과를 동일한 정밀도의 `Float`로 [`Parse`](/pkg/math/big/#Float.Parse) 하여 읽었을 때 원래 값과 동일하게 되기 위해 필요한 최소한의 자릿수를 사용함을 의미합니다.
  - [`math/rand`](/pkg/math/rand/) 패키지에 [`Read`](/pkg/math/rand/#Read) 함수가 추가되었고, 마찬가지로 [`Rand`](/pkg/math/rand/#Rand)에 [`Read`](/pkg/math/rand/#Rand.Read) 메서드가 추가되었습니다. 이를 통해 의사 난수 테스트 데이터를 더 쉽게 생성할 수 있습니다. 패키지의 다른 부분과 마찬가지로, 이는 암호화 설정에서 사용해서는 안 되며, 그러한 용도로는 대신 [`crypto/rand`](/pkg/crypto/rand/) 패키지를 사용하십시오.
  - [`net`](/pkg/net/) 패키지의 [`ParseMAC`](/pkg/net/#ParseMAC) 함수가 이제 20바이트 IP-over-InfiniBand (IPoIB) 링크 계층 주소를 허용합니다.
  - 또한 [`net`](/pkg/net/) 패키지에서 DNS 조회에 몇 가지 변경 사항이 있었습니다. 첫째, [`DNSError`](/pkg/net/#DNSError) 에러 구현체가 이제 [`Error`](/pkg/net/#Error)를 구현하며, 특히 새로운 [`IsTemporary`](/pkg/net/#DNSError.IsTemporary) 메서드는 DNS 서버 에러에 대해 true를 반환합니다. 둘째, [`LookupAddr`](/pkg/net/#LookupAddr)와 같은 DNS 조회 함수가 이제 Plan 9 및 Windows에서도 Unix 시스템의 Go 동작과 일치하도록 루트 도메인 이름(끝에 점이 붙은 형태)을 반환합니다.
  - [`net/http`](/pkg/net/http/) 패키지에는 이미 논의된 HTTP/2 지원 외에 여러 소규모 추가 사항이 있습니다. 첫째, [`FileServer`](/pkg/net/http/#FileServer)가 이제 생성된 디렉토리 목록을 파일 이름순으로 정렬합니다. 둘째, [`ServeFile`](/pkg/net/http/#ServeFile) 함수는 이제 요청의 URL 경로에 경로 요소로 ".." (dot-dot)이 포함되어 있으면 결과를 제공하지 않습니다. 프로그램은 일반적으로 `ServeFile`을 직접 호출하는 대신 `FileServer`와 [`Dir`](/pkg/net/http/#Dir)를 사용해야 합니다. dot-dot이 포함된 URL 요청에 대해 파일 콘텐츠를 제공해야 하는 프로그램은 여전히 [`ServeContent`](/pkg/net/http/#ServeContent)를 호출할 수 있습니다. 셋째, [`Client`](/pkg/net/http/#Client)는 이제 사용자 코드가 `Expect:` `100-continue` 헤더를 설정할 수 있도록 허용합니다 ([`Transport.ExpectContinueTimeout`](/pkg/net/http/#Transport) 참조). 넷째, [다섯 가지 새로운 에러 코드](/pkg/net/http/#pkg-constants)가 추가되었습니다: RFC 6585의 `StatusPreconditionRequired` (428), `StatusTooManyRequests` (429), `StatusRequestHeaderFieldsTooLarge` (431), `StatusNetworkAuthenticationRequired` (511)와 최근 승인된 `StatusUnavailableForLegalReasons` (451)입니다. 다섯째, [`CloseNotifier`](/pkg/net/http/#CloseNotifier)의 구현과 문서가 상당히 변경되었습니다. [`Hijacker`](/pkg/net/http/#Hijacker) 인터페이스는 이제 이전에 `CloseNotifier`와 함께 사용된 연결에서도 올바르게 작동합니다. 문서에는 이제 `CloseNotifier`가 언제 작동할 것으로 기대되는지 설명되어 있습니다.
  - 또한 [`net/http`](/pkg/net/http/) 패키지에서 `Method` 필드가 빈 문자열로 설정된 [`Request`](/pkg/net/http/#Request) 데이터 구조 처리와 관련된 몇 가지 변경 사항이 있습니다. 빈 `Method` 필드는 항상 `"GET"`의 별칭으로 문서화되어 왔으며 앞으로도 그렇습니다. 하지만 Go 1.6은 빈 `Method`를 명시적인 `"GET"`과 동일하게 처리하지 않았던 몇 가지 루틴을 수정했습니다. 특히, 이전 릴리스에서 [`Client`](/pkg/net/http/#Client)는 `Method`가 명시적으로 `"GET"`으로 설정된 경우에만 리다이렉트를 따랐으나, Go 1.6의 `Client`는 빈 `Method`에 대해서도 리다이렉트를 따릅니다. 마지막으로, [`NewRequest`](/pkg/net/http/#NewRequest)는 빈 값으로 허용된다고 문서화되지 않은 `method` 인수를 받습니다. 이전 릴리스에서는 빈 `method` 인수를 전달하면 `Method` 필드가 빈 `Request`가 생성되었습니다. Go 1.6에서 결과 `Request`는 항상 초기화된 `Method` 필드를 갖습니다. 인수가 빈 문자열인 경우, `NewRequest`는 반환된 `Request`의 `Method` 필드를 `"GET"`으로 설정합니다.
  - [`net/http/httptest`](/pkg/net/http/httptest/) 패키지의 [`ResponseRecorder`](/pkg/net/http/httptest/#ResponseRecorder)는 이제 [`http.Server`](/pkg/net/http/#Server)와 동일한 콘텐츠 스니핑 알고리즘을 사용하여 기본 Content-Type 헤더를 초기화합니다.
  - [`net/url`](/pkg/net/url/) 패키지의 [`Parse`](/pkg/net/url/#Parse)는 이제 호스트 이름 파싱에 대해 더 엄격하고 사양을 더 잘 준수합니다. 예를 들어, 호스트 이름에 공백이 포함되는 것은 더 이상 허용되지 않습니다.
  - 또한 [`net/url`](/pkg/net/url/) 패키지에서 [`Error`](/pkg/net/url/#Error) 타입이 이제 [`net.Error`](/pkg/net/#Error)를 구현합니다.
  - [`os`](/pkg/os/) 패키지의 [`IsExist`](/pkg/os/#IsExist), [`IsNotExist`](/pkg/os/#IsNotExist), [`IsPermission`](/pkg/os/#IsPermission)은 이제 [`SyscallError`](/pkg/os/#SyscallError)에 대해 문의할 때 올바른 결과를 반환합니다.
  - Unix-like 시스템에서 [`os.Stdout` 또는 `os.Stderr`](/pkg/os/#pkg-variables) (더 정확하게는 파일 디스크립터 1 또는 2로 열린 `os.File`)에 쓰기가 broken pipe 에러로 인해 실패하면, 프로그램은 `SIGPIPE` 시그널을 발생시킵니다. 기본적으로 이는 프로그램의 종료를 유발하며, 이는 `syscall.SIGPIPE`에 대해 [`os/signal`](/pkg/os/signal) [`Notify`](/pkg/os/signal/#Notify) 함수를 호출하여 변경할 수 있습니다. 1 또는 2 이외의 파일 디스크립터에서 broken pipe에 쓰는 것은 단순히 호출자에게 `syscall.EPIPE` (아마도 [`os.PathError`](/pkg/os#PathError) 및/또는 [`os.SyscallError`](/pkg/os#SyscallError)로 래핑됨)를 반환합니다. broken pipe에 10번 연속으로 쓴 후 잡을 수 없는 `SIGPIPE` 시그널을 발생시키던 이전 동작은 더 이상 발생하지 않습니다.
  - [`os/exec`](/pkg/os/exec/) 패키지에서 [`Cmd`](/pkg/os/exec/#Cmd)의 [`Output`](/pkg/os/exec/#Cmd.Output) 메서드는 명령어가 성공하지 못한 상태로 종료될 때 계속해서 [`ExitError`](/pkg/os/exec/#ExitError)를 반환합니다. 표준 에러가 버려졌을 경우, 반환된 `ExitError`는 이제 디버깅이나 에러 메시지 포함을 위해 실패한 명령어의 표준 에러 출력의 접두사와 접미사(현재 32kB)를 보유합니다. `ExitError`의 [`String`](/pkg/os/exec/#ExitError.String) 메서드는 캡처된 표준 에러를 표시하지 않으며, 프로그램은 데이터 구조에서 별도로 이를 가져와야 합니다.
  - Windows에서 [`path/filepath`](/pkg/path/filepath/) 패키지의 [`Join`](/pkg/path/filepath/#Join) 함수는 이제 베이스가 상대 드라이브 경로인 경우를 올바르게 처리합니다. 예를 들어, ``Join(`c:`,`` `` `a`) ``는 이제 이전 릴리스의 `` `c:\a` `` 대신 `` `c:a` ``를 반환합니다. 이는 잘못된 결과를 예상하던 코드에 영향을 줄 수 있습니다.
  - [`regexp`](/pkg/regexp/) 패키지에서 [`Regexp`](/pkg/regexp/#Regexp) 타입은 항상 동시성 goroutine에서 사용하기에 안전했습니다. 이는 정규 표현식 검색 중에 사용되는 스크래치 공간 캐시를 보호하기 위해 [`sync.Mutex`](/pkg/sync/#Mutex)를 사용합니다. 많은 goroutine에서 동일한 `Regexp`를 사용하는 일부 고동시성 서버에서는 해당 뮤텍스의 경합으로 인해 성능 저하가 발생했습니다. 이러한 서버를 돕기 위해 `Regexp`에 [`Copy`](/pkg/regexp/#Regexp.Copy) 메서드가 추가되었습니다. 이 메서드는 원본의 대부분의 구조를 공유하지만 자체적인 스크래치 공간 캐시를 갖는 `Regexp` 복사본을 만듭니다. 두 goroutine은 뮤텍스 경합 없이 `Regexp`의 서로 다른 복사본을 사용할 수 있습니다. 복사본은 추가적인 공간 오버헤드가 있으므로, `Copy`는 경합이 관찰되었을 때만 사용해야 합니다.
  - [`strconv`](/pkg/strconv/) 패키지에 [`IsPrint`](/pkg/strconv/#IsPrint)와 유사한 [`IsGraphic`](/pkg/strconv/#IsGraphic)이 추가되었습니다. 또한 [`QuoteToASCII`](/pkg/strconv/#QuoteToASCII), [`QuoteRuneToASCII`](/pkg/strconv/#QuoteRuneToASCII) 등과 유사한 [`QuoteToGraphic`](/pkg/strconv/#QuoteToGraphic), [`QuoteRuneToGraphic`](/pkg/strconv/#QuoteRuneToGraphic), [`AppendQuoteToGraphic`](/pkg/strconv/#AppendQuoteToGraphic), [`AppendQuoteRuneToGraphic`](/pkg/strconv/#AppendQuoteRuneToGraphic)가 추가되었습니다. `ASCII` 제품군은 ASCII 공백(U+0020)을 제외한 모든 공백 문자를 이스케이프합니다. 반면 `Graphic` 제품군은 유니코드 공백 문자(카테고리 Zs)를 이스케이프하지 않습니다.
  - [`testing`](/pkg/testing/) 패키지에서 테스트가 [t.Parallel](/pkg/testing/#T.Parallel)을 호출하면, 해당 테스트는 모든 비병렬 테스트가 완료될 때까지 일시 중지되었다가 다른 모든 병렬 테스트와 함께 실행을 계속합니다. Go 1.6은 이러한 테스트에 대해 보고되는 시간을 변경합니다. 이전에는 병렬 실행 시간만 계산했지만, 이제는 테스트 시작부터 `t.Parallel` 호출까지의 시간도 함께 계산합니다.
  - [`text/template`](/pkg/text/template/) 패키지에는 위에서 설명한 [주요 변경 사항](#template) 외에 두 가지 소규모 변경 사항이 있습니다. 첫째, 기반 라이터(underlying writer)에 대한 `Write`에서 기인하지 않은 [`Execute`](/pkg/text/template/#Template.Execute) 중의 모든 에러에 대해 반환되는 새로운 [`ExecError`](/pkg/text/template/#ExecError) 타입을 추가했습니다. 호출자는 `ExecError`를 확인하여 템플릿 사용 에러와 I/O 에러를 구분할 수 있습니다. 둘째, [`Funcs`](/pkg/text/template/#Template.Funcs) 메서드가 이제 [`FuncMap`](/pkg/text/template/#FuncMap)의 키로 사용된 이름이 템플릿 함수 호출에 나타날 수 있는 식별자인지 확인합니다. 그렇지 않은 경우 `Funcs`는 패닉을 발생시킵니다.
  - [`time`](/pkg/time/) 패키지의 [`Parse`](/pkg/time/#Parse) 함수는 항상 1월 32일과 같이 31보다 큰 월의 날짜를 거부해 왔습니다. Go 1.6에서 `Parse`는 이제 평년의 2월 29일, 2월 30일, 2월 31일, 4월 31일, 6월 31일, 9월 31일, 11월 31일도 거부합니다.
