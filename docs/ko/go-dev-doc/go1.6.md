<!--
수정: .,s;^PKG:([a-z][A-Za-z0-9_/]+);<a href="/pkg/\1/"><code>\1</code></a>;g
수정: .,s;^([a-z][A-Za-z0-9_/]+)\.([A-Z][A-Za-z0-9_]+\.)?([A-Z][A-Za-z0-9_]+)([ .',]|$);<a href="/pkg/\1/#\2\3"><code>\3</code></a>\4;g
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.6 소개 {#introduction}

### 개요

이 문서는 Go 1.6 버전의 주요 기능과 변경 사항을 소개합니다.

가장 최신 Go 릴리스인 버전 1.6은 1.5 이후 6개월 만에 출시되었습니다.
대부분의 변경 사항은 언어, 런타임 및 라이브러리의 구현에 있습니다.
언어 사양에는 변경 사항이 없습니다.
항상처럼, 이번 릴리스는 Go 1의 [호환성 약속](/doc/go1compat.html)을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

이 릴리스는 다음을 추가합니다:
* [Linux on 64-bit MIPS 및 Android on 32-bit x86](#ports)에 대한 새로운 포트
* C와 Go 포인터를 공유하기 위한 [규칙 정의 및 적용](#cgo)
* 투명하고 자동화된 [HTTP/2 지원](#http2)
* 새로운 템플릿 재사용 메커니즘 [템플릿](#template)

## 언어 변경 사항 {#language}

이 릴리스에는 언어 변경 사항이 없습니다.

## 포트

Go 1.6는 실험적인 MIPS 아키텍처 (64비트: `linux/mips64` 및 `linux/mips64le`)를 위한 포트를 추가합니다.
이 포트는 `cgo`를 지원하지만, 내부 링크만 지원합니다.

Go 1.6는 또한 32비트 x86 아키텍처 (`android/386`)에서 Android용의 실험적인 포트를 추가합니다.

프리BSD에서 Go 1.6는 기본적으로 `clang`을 외부 C 컴파일러로 사용합니다. `gcc`가 아닌.

리눅스, 리틀 엔디안 64비트 파워PC (`linux/ppc64le`)에서,
Go 1.6는 이제 `cgo`를 외부 링크와 함께 지원하며, 기능적으로 거의 완성되었습니다.

NaCl에서 Go 1.5는 SDK 버전 41을 필요로 했습니다.
Go 1.6는 더 높은 SDK 버전에 대한 지원을 추가합니다.

32비트 x86 시스템에서 `-dynlink` 또는 `-shared` 컴파일 모드를 사용하는 경우,
`CX` 레지는 특정 메모리 참조에 의해 덮어쓰이게 되므로,
수동으로 작성된 어셈블리 코드에서는 사용하지 않아야 합니다.
자세한 내용은 [어셈블리 문서](/doc/asm#x86)를 참조하십시오.

## 도구 {#tools}

### Cgo {#cgo}

다음 중 주요 변경 사항이 하나 있으며, 미미한 변경 사항도 하나 있습니다. [`cgo`](/cmd/cgo/)

주요 변경 사항은 Go 포인터를 C 코드와 공유하는 규칙을 정의하는 것입니다.
이를 통해 C 코드가 Go의 가비지 컬렉터와 함께 동작할 수 있도록 합니다.
간단히 말해서, Go가 가비지 컬렉션으로 할당된 메모리를 사용하고,
C 코드로 전달할 때, Go 포인터로 가비지 컬렉션으로 할당된 메모리에 대한 포인터가 포함되지 않아야 하고,
C 코드가 호출이 완료된 후 포인터를 유지하지 않아야 합니다.
이러한 규칙은 프로그램 실행 중에 런타임에 의해 검사됩니다.
런타임이 위반 사항을 감지하면, 오류 메시지를 출력하고 프로그램을 종료합니다.
이러한 검사를 비활성화하려면 환경 변수 `GODEBUG=cgocheck=0`을 설정할 수 있지만,
대부분의 검출된 코드가 가비지 컬렉션과 어느 정도 호환되지 않는다는 점에 유의해야 합니다.
검사를 비활성화하면 일반적으로 더 많은 의심스러운 오류가 발생합니다.
문제의 코드를 수정하는 것이 검사를 비활성화하는 것보다 훨씬 권장됩니다.
자세한 내용은 [`cgo` 문서를 참조하십시오](/cmd/cgo/#hdr-Passing_pointers).

작은 변경은 다음과 같습니다.
명시적인 `C.complexfloat` 및 `C.complexdouble` 유형의 추가,
이는 Go의 `complex64` 및 `complex128` 유형과 분리됩니다.
다른 숫자 유형과 마찬가지로, C의 복소수 유형과 Go의 복소수 유형은
더 이상 상호 교환될 수 없습니다.

### 컴파일러 도구 체인 {#compiler}

컴파일러 도구 체인은 대부분 변경되지 않았습니다.
내부적으로 가장 중요한 변경 사항은 파서가 이제 [yacc](/cmd/yacc/)에서 생성되는 대신 수동으로 작성되었다는 것입니다.

컴파일러, 링커, 그리고 `go` 명령어에는 새로운 플래그 `-msan`이 있으며, 이는 `-race`와 유사하며 Linux/amd64에서만 사용 가능합니다.
이 플래그는 [Clang MemorySanitizer](https://clang.llvm.org/docs/MemorySanitizer.html)과의 상호 작용을 활성화합니다.
이러한 상호 작용은 특히 의심스러운 C 또는 C++ 코드를 포함하는 프로그램을 테스트하는 데 유용합니다.

링커에는 이제 `-libgcc` 옵션이 추가되어, `cgo` 코드를 링크할 때 C 컴파일러 지원 라이브러리의 예상 위치를 지정할 수 있습니다.
이 옵션은 `-linkmode=internal`을 사용할 때만 참조되며, 지원 라이브러리의 사용을 비활성화하려면 `none`으로 설정할 수 있습니다.

[빌드 모드의 구현은 Go 1.5부터](/doc/go1.5#link) 더 많은 시스템으로 확장되었습니다.
이번 릴리스는 다음 모드에 대한 지원을 추가합니다:
- `c-shared` 모드: `android/386`, `android/amd64`, `android/arm64`, `linux/386`, `linux/arm64`
- `shared` 모드: `linux/386`, `linux/arm`, `linux/amd64`, `linux/ppc64le`
- 새로운 `pie` 모드 (상대적 위치 독립 실행 파일을 생성): `android/386`, `android/amd64`, `android/arm`, `android/arm64`, `linux/386`, `linux/amd64`, `linux/arm`, `linux/arm64`, `linux/ppc64le`
자세한 내용은 [설계 문서](/s/execmodes)를 참조하십시오.

리링크의 `-X` 플래그는 Go 1.5에서 변경되었습니다.
Go 1.4 및 이전 버전에서는 두 개의 인수를 사용했습니다.

-X importpath.name 값

Go 1.5에서 단일 인수를 사용하여 대체 구문을 추가했습니다.
이 인수는 `name=value` 쌍 자체입니다:

-X importpath.name=value

Go 1.5에서는 이전 구문이 여전히 허용되었지만, 새 구문을 사용하는 것을 제안하는 경고 메시지가 표시되었습니다.
Go 1.6은 이전 구문을 계속 허용하고 경고 메시지를 표시합니다.
Go 1.7에서는 이전 구문에 대한 지원이 제거됩니다.

### Gccgo {#gccgo}

GCC 및 Go 프로젝트의 릴리즈 일정은 일치하지 않습니다.
GCC 5 릴리즈에는 Go 1.4 버전의 `gccgo`가 포함되어 있습니다.
다음 릴리즈인 GCC 6에는 Go 1.6.1 버전의 `gccgo`가 포함됩니다.

### Go 명령어 {#go_command}

`[go](cmd/go)` 명령어의 기본 작동 방식은 동일하지만, 몇 가지 주목할 만한 변경 사항이 있습니다.

Go 1.5에서 벤더링에 대한 실험적인 지원이 도입되었으며, `GO15VENDOREXPERIMENT` 환경 변수를 `1`로 설정하여 활성화할 수 있습니다.
Go 1.6은 벤더링 지원을 유지하며, 더 이상 실험적인 기능으로 간주되지 않으며, 기본적으로 활성화됩니다.
필요에 따라 `GO15VENDOREXPERIMENT` 환경 변수를 `0`로 설정하여 명시적으로 비활성화할 수 있습니다.
Go 1.7에서는 환경 변수 지원이 제거됩니다.

가장 흔하게 발생하는 문제는, 기본적으로 벤더링을 활성화했을 때, 기존의 `vendor`라는 이름의 디렉터리가 포함된 소스 트리에 발생합니다. 이 디렉터리는 새로운 벤더링 규칙에 따라 해석되지 않도록 설계되었습니다.
이 경우 가장 간단한 해결책은 디렉터리의 이름을 `vendor`가 아닌 다른 이름으로 바꾸고, 영향을 받는 모든 임포트 경로를 업데이트하는 것입니다.

자세한 내용은 다음 문서를 참조하십시오.
[`go` 명령의 문서](/cmd/go/#hdr-Vendor_Directories)
및 [설계 문서](/s/go15vendor).

다음과 같은 새로운 빌드 플래그 `-msan`이 있습니다.
이 플래그는 Go 컴파일을 LLVM 메모리 산산화 기능을 지원하도록 합니다.
이는 주로 C 또는 C++ 코드를 메모리 산산화 기능으로 검사할 때 링크할 때 사용하는 데 목적이 있습니다.

### Go 문서 생성 명령어 {#doc_command}

Go 1.5에서 `go doc` 명령이 도입되었으며, 이를 통해 패키지 이름을만 사용하여 패키지를 참조할 수 있습니다 (예: `go doc http`).
모호한 경우, Go 1.5의 동작 방식은 가장 먼저 임포트된 패키지를 사용했습니다.
Go 1.6에서는, 임포트 경로의 요소 수가 적은 것을 선호하여 모호성을 해결합니다. 이때, 어휘적 비교를 통해 동일한 경우를 결정합니다.
이 변경의 중요한 결과는 원본 패키지의 복사본이 이제 임포트된 복사본보다 선호된다는 것입니다.
성공적인 검색 또한 더 빠르게 실행되는 경향이 있습니다.

### Go vet 명령어 {#vet_command}

```shell
go vet
```

[`go vet`](/cmd/vet) 명령은 이제 `Printf` 함수에 함수 또는 메서드 값을 인수로 전달하는 것을 진단합니다. 예를 들어 `f`를 전달하는 경우, 여기서 `f()`가 호출되도록 의도되었을 때입니다.

## 성능 {#performance}

물론, 변경 사항이 너무 광범위하고 다양하기 때문에 정확한 성능에 대한 언급을 하는 것은 어렵습니다.
일부 프로그램은 더 빠르게 실행될 수 있고, 일부는 더 느리게 실행될 수 있습니다.
평균적으로 Go 1 벤치마크 스위트에 있는 프로그램은 Go 1.6에서 Go 1.5보다 몇 퍼센트 더 빠르게 실행됩니다.
특히, 많은 양의 메모리를 사용하는 프로그램의 경우, 가비지 컬렉터의 중단 시간은 Go 1.5보다 훨씬 짧습니다.

다음 패키지의 구현에 상당한 최적화가 이루어져 10% 이상의 성능 향상을 가져왔습니다.
* `compress/bzip2` ([/pkg/compress/bzip2/](pkg/compress/bzip2/))
* `compress/gzip` ([/pkg/compress/gzip/](pkg/compress/gzip/))
* `crypto/aes` ([/pkg/crypto/aes/](pkg/crypto/aes/))
* `crypto/elliptic` ([/pkg/crypto/elliptic/](pkg/crypto/elliptic/))
* `crypto/ecdsa` ([/pkg/crypto/ecdsa/](pkg/crypto/ecdsa/))
* `sort` ([/pkg/sort/](pkg/sort/))

## 표준 라이브러리 {#library}

### HTTP/2 {#http2}

Go 1.6는 [`net/http`](/pkg/net/http/) 패키지에 HTTP/2 프로토콜에 대한 투명한 지원을 추가합니다.
[HTTP/2 프로토콜](https://http2.github.io/).
Go 클라이언트와 서버는 HTTPS를 사용할 때 적절하게 HTTP/2를 자동으로 사용합니다.
HTTP/2 프로토콜 처리의 세부 사항에 대한 특정 내보낸 API가 없으며, HTTP/1.1에 대한 특정 내보낸 API가 없는 것과 동일합니다.

프로그램이 HTTP/2를 비활성화해야 하는 경우, 다음을 설정하여 수행할 수 있습니다.
[`Transport.TLSNextProto`](/pkg/net/http/#Transport) (클라이언트용)
또는
[`Server.TLSNextProto`](/pkg/net/http/#Server) (서버용)
을 비어 있지 않은 맵으로 설정합니다.

프로그램은 HTTP/2 프로토콜에 특정한 세부 사항을 조정해야 하는 경우,
[`golang.org/x/net/http2`](https://golang.org/x/net/http2)를 가져와 사용할 수 있습니다.
특히,
[ConfigureServer](https://godoc.org/golang.org/x/net/http2/#ConfigureServer)
및
[ConfigureTransport](https://godoc.org/golang.org/x/net/http2/#ConfigureTransport)
함수를 사용합니다.

### 런타임 {#runtime}

런타임은 가벼운 방식으로, 맵의 동시 오용을 감지하는 기능을 추가했습니다.
항상 그렇듯이, 만약 하나의 goroutine이 맵에 쓰기 작업을 수행하는 경우, 다른 goroutine은 맵을 동시에 읽거나 쓰지 않아야 합니다.
런타임이 이러한 조건을 감지하면, 진단 메시지를 출력하고 프로그램을 종료합니다.
이 문제를 더 자세히 파악하는 가장 좋은 방법은 [레이스 디텍터](/blog/race-detector)를 사용하여 프로그램을 실행하는 것입니다. 이는 레이스를 더 신뢰성 있게 식별하고 더 자세한 정보를 제공합니다.

프로그램 종료 시 패닉 발생 시, 런타임은 기본적으로
현재 실행 중인 고루틴의 스택만 출력하며,
다른 모든 고루틴은 출력하지 않습니다.
일반적으로 패닉은 현재 고루틴에만 관련이 있으므로,
다른 고루틴을 제외하면, 충돌 메시지에 불필요한 출력을 크게 줄일 수 있습니다.
충돌 메시지에 모든 고루틴의 스택을 보려면, 환경 변수 `GOTRACEBACK`을 `all`로 설정하거나,
충돌 발생 전에 [`debug.SetTraceback`](/pkg/runtime/debug/#SetTraceback) 함수를 호출하고 프로그램을 다시 실행합니다.
자세한 내용은 [런타임 문서](/pkg/runtime/#hdr-Environment_Variables)를 참조하십시오.

_업데이트_:
예상치 못한 오류(panic)가 프로그램 전체의 상태를 dump하는 것을 의도하며,
예를 들어 타임아웃이 감지되거나 수신된 신호를 명시적으로 처리할 때,
panic 발생 전에 `debug.SetTraceback("all")`를 호출해야 합니다.
`signal.Notify` 사용을 검색하면 이러한 코드를 식별하는 데 도움이 될 수 있습니다.

Windows에서, Go 1.5 이전 버전에 작성된 Go 프로그램은 `timeBeginPeriod(1)`를 호출하여 전역 Windows 타이머 해상도를 시작 시 1ms로 강제했습니다.
Go는 더 이상 이를 필요로 하지 않으며, 전역 타이머 해상도를 변경하면 일부 시스템에서 문제가 발생했기 때문에 해당 호출은 제거되었습니다.

`-buildmode=c-archive` 또는
`-buildmode=c-shared`을 사용하여 아카이브 또는 공유 라이브러리를 빌드할 때, 신호 처리 방식이 변경되었습니다.
Go 1.5에서는 아카이브 또는 공유 라이브러리가 대부분의 신호에 대해 신호 처리기를 설치했습니다.
Go 1.6에서는 Go 코드 내에서 발생하는 런타임 패닉을 처리하는 데 필요한 동기 신호에 대해서만 신호 처리기를 설치합니다:
SIGBUS, SIGFPE, SIGSEGV.
자세한 내용은 [os/signal](/pkg/os/signal) 패키지를 참조하십시오.

### 반사 {#reflect}

[`reflect`](/pkg/reflect/) 패키지는
[해결된 오래된 호환성 문제](https://github.com/golang/go/issues/12367)를
gc 및 gccgo 도구 체인 간에
내부적으로 정의된 내보내기 필드가 있는 구조체 유형에 대한
관련하여 해결했습니다.
반사(reflection)를 사용하여 데이터 구조를 탐색하는 코드는, 특히
`encoding/json` 및 `encoding/xml` 패키지의
예시를 따르는 직렬화 구현에 사용될 때 업데이트가 필요할 수 있습니다.

문제는 `reflect`를 사용하여 내장된 비공개 구조체 유형의 필드를 해당 구조체의 공개 필드로 탐색할 때 발생합니다.
이 경우, `reflect`는 잘못하여 내장된 필드를 공개된 것으로 보고했으며, `Field.PkgPath`를 비어 있는 값으로 반환했습니다.
이제 필드를 올바르게 비공개로 보고하지만, 구조체 내부에 있는 공개 필드에 액세스할 때 이를 무시합니다.

_업데이트_:
일반적으로, 이전에 구조체에 접근하고 사용하던 코드를 업데이트해야 합니다.

f.PkgPath != ""

접근 불가능한 필드를 제외하려면
이제 다음을 사용해야 합니다

f.PkgPath != "" && !f.Anonymous

예를 들어, 다음 구현의 변경 사항을 참조하십시오.
[`encoding/json`](https://go-review.googlesource.com/#/c/14011/2/src/encoding/json/encode.go) 및
[`encoding/xml`](https://go-review.googlesource.com/#/c/14012/2/src/encoding/xml/typeinfo.go).

### 정렬 {#sort}

`sort` 패키지에서,
[`Sort`](/pkg/sort/#Sort)
구현이 재작성되어,
`Interface`의
`Less` 및 `Swap`
메서드 호출 횟수를 약 10% 줄였으며, 이에 따라 전반적인 시간 절약 효과가 있습니다.
새로운 알고리즘은 동일한 값을 비교하는 값에 대해 이전과 다른 순서를 선택합니다 (즉, `Less(i, j)` 및 `Less(j, i)`가 false인 경우).

_업데이트_:
`Sort` 함수의 정의는 동일한 값의 최종 순서에 대해 어떤 보장도 하지 않습니다.
그러나 새로운 동작이 특정 순서를 예상하는 프로그램에 영향을 줄 수 있습니다.
이러한 프로그램은 `Less` 구현을 수정하여 원하는 순서를 보고하거나,
[`Stable`](/pkg/sort/#Stable)로 변경하여
동일한 값의 원래 입력 순서를 유지할 수 있습니다.

### 템플릿 {#template}

`text/template` 패키지에는 템플릿 작성 작업을 더 쉽게 만들어주는 두 가지 주요 새로운 기능이 있습니다.

먼저, 이제 템플릿 액션 주위의 공백을 제거할 수 있습니다. (`/pkg/text/template/#hdr-Text_and_spaces`)
이를 통해 템플릿 정의를 더 읽기 쉽게 만들 수 있습니다.
액션의 시작 부분에 있는 마이너스 기호는 액션 앞에 있는 공백을 제거하도록 지시하고, 액션의 끝 부분에 있는 마이너스 기호는 액션 뒤에 있는 공백을 제거하도록 지시합니다.
예를 들어, 템플릿은

{{23 -}}
	   <
	{{- 45}}

형식은 `23<45`입니다.

둘째, 새로운 [`{{block}}` 액션](/pkg/text/template/#hdr-Actions)과 함께, 이름이 지정된 템플릿의 재정의를 허용함으로써, 템플릿의 여러 인스턴스에서 대체될 수 있는 템플릿의 부분을 간단하게 정의할 수 있습니다.
`text/template` 패키지에 [예제](/pkg/text/template/#example_Template_block)가 있으며, 이 새로운 기능을 보여줍니다.

### 라이브러리의 세부 변경 사항 {#minor_library_changes}

- [`archive/tar`](/pkg/archive/tar/) 패키지의
    구현은 파일 형식의 드문 경우에 많은 버그를 수정합니다.
    가장 눈에 띄는 변경 사항은
    [`Reader`](/pkg/archive/tar/#Reader) 유형의
    [`Read`](/pkg/archive/tar/#Reader.Read) 메서드가
    특수 파일 유형의 내용을 빈 것으로 보고, 즉시 `io.EOF`를 반환한다는 것입니다.
  - [`archive/zip`](/pkg/archive/zip/) 패키지에서,
    [`Reader`](/pkg/archive/zip/#Reader) 유형은 이제
    [`RegisterDecompressor`](/pkg/archive/zip/#Reader.RegisterDecompressor) 메서드를 가지고 있으며,
    [`Writer`](/pkg/archive/zip/#Writer) 유형은 이제
    [`RegisterCompressor`](/pkg/archive/zip/#Writer.RegisterCompressor) 메서드를 가지고 있습니다.
    이 기능을 통해 개별 zip 파일의 압축 옵션을 제어할 수 있습니다.
    이 기능은 기존의 전역 [`RegisterDecompressor`](/pkg/archive/zip/#RegisterDecompressor) 및
    [`RegisterCompressor`](/pkg/archive/zip/#RegisterCompressor) 함수보다 우선합니다.
  - [`bufio`](/pkg/bufio/) 패키지의
    [`Scanner`](/pkg/bufio/#Scanner) 유형은 이제
    [`Buffer`](/pkg/bufio/#Scanner.Buffer) 메서드를 가지고 있습니다.
    이 메서드를 사용하여 스캔 중에 사용할 초기 버퍼 및 최대 버퍼 크기를 지정할 수 있습니다.
    필요한 경우 `MaxScanTokenSize`보다 큰 토큰을 스캔할 수 있습니다.
    또한 `Scanner`에 대해서, 패키지는 이제
    [`ErrFinalToken`](/pkg/bufio/#ErrFinalToken) 오류 값을 정의하여
    [split 함수](/pkg/bufio/#SplitFunc)가 처리 중지하거나 최종 빈 토큰을 반환하는 데 사용할 수 있습니다.
  - [`compress/flate`](/pkg/compress/flate/) 패키지는
    [`ReadError`](/pkg/compress/flate/#ReadError) 및
    [`WriteError`](/pkg/compress/flate/#WriteError) 오류 구현을 중단했습니다.
    Go 1.5에서는 오류가 발생할 때 매우 드물게 반환되었습니다.
    이제 더 이상 반환되지 않지만, 호환성을 위해 정의해 둡니다.
  - [`compress/flate`](/pkg/compress/flate/),
    [`compress/gzip`](/pkg/compress/gzip/), 및
    [`compress/zlib`](/pkg/compress/zlib/) 패키지는 이제
    [`io.ErrUnexpectedEOF`](/pkg/io/#ErrUnexpectedEOF)를 사용하여
    잘린 입력 스트림을 보고, `/pkg/io/#EOF` 대신.
  - [`crypto/cipher`](/pkg/crypto/cipher/) 패키지는 GCM 디코딩 실패 시 대상 버퍼를 덮어씁니다.
    이렇게 하면 AESNI 코드가 임시 버퍼를 사용하지 않도록 할 수 있습니다.
  - [`crypto/tls`](/pkg/crypto/tls/) 패키지에는
    다양한 미세한 변경 사항이 있습니다.
    이제 `Listen`가
    [`Config`](/pkg/crypto/tls/#Config)
    의 `Certificates`가 `nil`일 때 성공할 수 있습니다.
    또한 RSA와 AES-GCM 암호화 방법을 지원하며,
    `RecordHeaderError`](/pkg/crypto/tls/#RecordHeaderError)를 추가하여
    네트워크 연결을 시도할 때 클라이언트 (특히 `net/http` 패키지)가 TLS 서버에 대한 더 나은 오류를 보고할 수 있습니다.
  - [`crypto/x509`](/pkg/crypto/x509/) 패키지는
    자격 증명이 음수 시리얼 번호를 포함할 수 있도록 허용합니다 (사실상 오류이지만 실제로 일반적임).
    또한 `InsecureAlgorithmError`](/pkg/crypto/x509/#InsecureAlgorithmError)를 정의하여 MD5와 같은 안전하지 않은 알고리즘으로 서명된 자격 증명을 거부할 때 더 나은 오류 메시지를 제공합니다.
  - [`debug/dwarf`](/pkg/debug/dwarf) 및
    [`debug/elf`](/pkg/debug/elf/) 패키지는
    함께 압축된 DWARF 섹션에 대한 지원을 추가합니다.
    사용자 코드는 업데이트할 필요가 없습니다. 섹션은 읽을 때 자동으로 해제됩니다.
  - [`debug/elf`](/pkg/debug/elf/) 패키지는
    일반적으로 압축된 ELF 섹션에 대한 지원을 추가합니다.
    사용자 코드는 업데이트할 필요가 없습니다. 섹션은 읽을 때 자동으로 해제됩니다.
    그러나 압축된
    [`Sections`](/pkg/debug/elf/#Section)는 무작위 액세스를 지원하지 않습니다.
    그들은 `ReaderAt` 필드가 `nil`입니다.
  - [`encoding/asn1`](/pkg/encoding/asn1/) 패키지는 이제
    [`tag and class constants](/pkg/encoding/asn1/#pkg-constants)를 내보내어
    ASN.1 구조의 고급 파싱에 유용합니다.
  - 또한 [`encoding/asn1`](/pkg/encoding/asn1/) 패키지에서,
    [`Unmarshal`](/pkg/encoding/asn1/#Unmarshal)는 이제
    일반적으로 허용되지 않는 다양한 정수 및 길이 인코딩을 거부합니다.
  - [`encoding/base64`](/pkg/encoding/base64) 패키지의
    [`Decoder`](/pkg/encoding/base64/#Decoder)는 이제
    입력의 마지막 바이트를 처리하도록 수정되었습니다. 이전에 4바이트 토큰을 최대한 처리했지만 나머지를 무시했습니다.
    따라서 `Decoder`는 패딩되지 않은 인코딩 (예:
    [RawURLEncoding](/pkg/encoding/base64/#RawURLEncoding))을 올바르게 처리하지만, 마지막에 공백이 있는 패딩된 인코딩 또는 유효하지 않은 바이트로 끝나는 패딩된 인코딩도 거부합니다.
  - [`encoding/json`](/pkg/encoding/json/) 패키지는
    [`Number`](/pkg/encoding/json/#Number)
    의 구문을 JSON 사양에 따라 준수하는지 확인하기 전에 마셜링하기 전에 확인합니다.
    이전 버전과 마찬가지로, 빈 `Number` (빈 문자열)는 0 (영)으로 마셜링됩니다.
  - [`encoding/xml`](/pkg/encoding/xml/) 패키지의
    [`Marshal`](/pkg/encoding/xml/#Marshal) 함수는 이제
    `chardata` 속성을 지원합니다. 즉,
    `<![CDATA[ ... ]]>` 태그 내에 인코딩합니다.
  - 또한 [`encoding/xml`](/pkg/encoding/xml/) 패키지에서,
    [`Decoder`](/pkg/encoding/xml/#Decoder)'s
    [`Token`](/pkg/encoding/xml/#Decoder.Token) 메서드는 이제
    입력에 열린 태그가 모두 보이지 않은 상태에서 EOF에 도달할 때 오류를 보고합니다.
    이 요구 사항을 피하려면 `RawToken`을 사용하십시오.
  - [`fmt`](/pkg/fmt/) 패키지는 이제
    어떤 정수 유형도
    [`Printf`](/pkg/fmt/#Printf)의 `*` 폭 및 정밀도 사양으로 전달할 수 있습니다.
    이전 버전에서는 `*` 인수의 유형이 `int`여야 했습니다.
  - 또한 [`fmt`](/pkg/fmt/) 패키지에서,
    [`Scanf`](/pkg/fmt/#Scanf)는 이제 %X를 사용하여
    16진수 문자열을 스캔할 수 있습니다.
    두 형식 모두 대- 및 소문자 16진수 조합을 허용합니다.
  - [`image`](/pkg/image/) 및
    [`image/color`](/pkg/image/color/) 패키지는
    [`NYCbCrA`](/pkg/image/#NYCbCrA) 및
    [`NYCbCrA`](/pkg/image/color/#NYCbCrA) 유형을 추가하여
    비-전단계 알파를 갖는 Y'CbCr 이미지를 지원합니다.
  - [`io`](/pkg/io/) 패키지의
    [`MultiWriter`](/pkg/io/#MultiWriter) 구현은 이제
    [`WriteString`](/pkg/io/#WriteString)를 사용하여
    [`WriteString`](/pkg/io/#WriteString)에 사용됩니다.
  - [`math/big`](/pkg/math/big/) 패키지는
    [`Int`](/pkg/math/big/#Int)에
    [`Append`](/pkg/math/big/#Int.Append) 및
    [`Text`](/pkg/math/big/#Int.Text) 메서드를 추가하여
    더 많은 제어를 제공합니다.
  - 또한 [`math/big`](/pkg/math/big/) 패키지에서,
    [`Float`](/pkg/math/big/#Float)는 이제
    [`encoding.TextMarshaler`](/pkg/encoding/#TextMarshaler) 및
    [`encoding.TextUnmarshaler`](/pkg/encoding/#TextUnmarshaler)를 구현하여
    [`encoding/json`](/pkg/encoding/json/) 및
    [`encoding/xml`](/pkg/encoding/xml/) 패키지가 자연스러운 형식으로 시리얼화할 수 있습니다.
  - 또한 [`math/big`](/pkg/math/big/) 패키지에서,
    [`Float`](/pkg/math/big/#Float)'s
    [`Append`](/pkg/math/big/#Float.Append) 메서드는 이제 -1 정밀도 인수를 지원합니다.
    [`strconv.ParseFloat`](/pkg/strconv/#ParseFloat)와 마찬가지로,
    정밀도 -1은 최소한의 숫자를 사용하여,
    [`Parse`](/pkg/math/big/#Float.Parse)
    결과를 `Float` 유형으로 읽을 때 원래 값을 생성하는 정밀도로
    [`Parse`](/pkg/math/big/#Float.Parse)
    함수에 전달합니다.
  - [`math/rand`](/pkg/math/rand/) 패키지는
    [`Read`](/pkg/math/rand/#Read) 함수를 추가하고,
    [`Rand`](/pkg/math/rand/#Rand)는
    [`Read`](/pkg/math/rand/#Rand.Read) 메서드를 추가합니다.
    이러한 기능은 테스트 데이터를 생성하는 데 도움이 됩니다.
    하지만 주의하십시오.
    이러한 기능은 암호화 목적으로 사용해서는 안 됩니다.
    이러한 목적으로는 [`crypto/rand`](/pkg/crypto/rand/) 패키지를 사용하십시오.
  - [`net`](/pkg/net/) 패키지의
    [`ParseMAC`](/pkg/net/#ParseMAC) 함수는 이제
    20바이트 IP-over-InfiniBand (IPoIB) 링크-레이어 주소를 받습니다.
  - 또한 [`net`](/pkg/net/) 패키지에서,
    DNS 쿼리에 대한 몇 가지 변경 사항이 있습니다.
    첫째, 오류 유형인
    [`DNSError`](/pkg/net/#DNSError) 오류 구현이
    이제 `Error`를 구현합니다 (특히, `IsTemporary` 메서드는
    `IsTemporary`](/pkg/net/#DNSError.IsTemporary)
    함수가 DNS 서버 오류를 반환합니다.
    둘째, DNS 쿼리 함수인
    [`LookupAddr`](/pkg/net/#LookupAddr)
    이제 계획 9 및 Windows에서 루트 도메인 이름을 반환합니다 (결국 점이 포함됨).
    이 동작은 Unix 시스템에서 Go가 따르는 동작과 일치합니다.
  - [`net/http`](/pkg/net/http/) 패키지는 HTTP/2 지원에 더해 추가된 몇 가지 미세한 기능이 있습니다.
    첫째, `FileServer`가 생성된 디렉토리 목록을 파일 이름별로 정렬합니다.
    둘째, `ServeFile` 함수는 요청의 URL 경로에 “..” (점-점)를 포함하는 결과를 제공하지 않습니다.
    이러한 경우 사용자는
    [`FileServer`](/pkg/net/http/#FileServer) 및
    [`Dir`](/pkg/net/http/#Dir)
    를 호출해야 합니다.
    점-점 경로가 필요한 경우
    [`ServeContent`](/pkg/net/http/#ServeContent)를 호출할 수도 있습니다.
    셋째, `Client`는
    [`Transport.ExpectContinueTimeout`](/pkg/net/http/#Transport)를 설정할 수 있도록 합니다.
    넷째, RFC 6585에 정의된 다섯 가지 새로운 오류 코드가 추가되었습니다.
    `StatusPreconditionRequired` (428),
    `StatusTooManyRequests` (429),
    `StatusRequestHeaderFieldsTooLarge` (431), 및
    `StatusNetworkAuthenticationRequired` (511).
    마지막으로, `CloseNotifier`
    의 구현 및 설명이 크게 변경되었습니다.
    `Hijacker`
    인터페이스는 이전에 `CloseNotifier`를 사용하여 사용된 연결에서도 제대로 작동합니다.
    `CloseNotifier`를 사용하는 경우에 작동하는 방식에 대한 설명이 제공됩니다.
  - [`net/http/httptest`](/pkg/net/http/httptest/) 패키지의
    [`ResponseRecorder`](/pkg/net/http/httptest/#ResponseRecorder)는 이제
    [`http.Server`](/pkg/net/http/#Server)의
    [`Content-Type` 헤더를 동일한 알고리즘으로 초기화합니다.
  - [`net/url`](/pkg/net/url/) 패키지의
    [`Parse`](/pkg/net/url/#Parse) 함수는 이제
    호스트 이름의 파싱에 대해 더 엄격하고, 더 엄격하게 사양 준수를 합니다.
    예를 들어 호스트 이름에 공백이 포함되지 않습니다.
  - 또한 [`net/url`](/pkg/net/url/) 패키지에서,
    [`Error`](/pkg/net/url/#Error) 유형이
    이제 `net.Error`를 구현합니다.
  - [`os`](/pkg/os/) 패키지의
    [`IsExist`](/pkg/os/#IsExist),
    [`IsNotExist`](/pkg/os/#IsNotExist), 및
    [`IsPermission`](/pkg/os/#IsPermission) 함수는 이제
    `SyscallError`를 쿼리할 때 올바른 결과를 반환합니다.
  - Unix 시스템에서는,
    `os.Stdout` 또는 `os.Stderr` (더 정확하게는 파일 설명자 1 또는 2에 쓰기하는 `os.File`)에 대한 쓰기가 실패하면,
    브이커 오류가 발생하면 프로그램이 `SIGPIPE` 신호를 발생시킵니다.
    이 신호는 기본적으로 프로그램을 종료합니다. 하지만
    [`os/signal`](/pkg/os/signal)
    의 `Notify` 함수를 호출하여 이 신호를 catch할 수 있습니다.
    파일 설명자 1 또는 2가 아닌 다른 파일에 대한 쓰기는 단순히
    `syscall.EPIPE` (이것이 `os.PathError` 및/또는 `os.SyscallError`에 래핑될 수 있음)을 반환합니다.
    이전 버전에서는 10번의 연속 쓰기를 통해, 닫힌 파이프에 쓰기를 시도했을 때, catch할 수 없는 `SIGPIPE` 신호가 발생했습니다.
  - [`os/exec`](/pkg/os/exec/) 패키지에서,
    `Cmd`의 `Output` 메서드는 여전히 명령이 실패할 때 `ExitError`를 반환합니다.
    이 오류에는 이제 기본 및 추가 (현재 32KB) 크기의 실패한 표준 오류의 일부가 포함되어 있습니다.
    이러한 `ExitError`의 `String` 메서드는 캡처된 표준 오류를 표시하지 않습니다.
    이러한 데이터를 가져오려면 별도로 가져와야 합니다.
  - Windows에서는,
    [`path/filepath`](/pkg/path/filepath/) 패키지의
    [`Join`](/pkg/path/filepath/#Join) 함수가 이제 올바르게 작동합니다.
    예를 들어 `` `Join(`c:`,`` `a`) ``는 이제
    `` `c:a` ``를 반환합니다 (이전 버전에서는 `` `c:\a` ``).
    이 동작은 점-점 경로를 사용하여 코드를 예상하는 기존 코드에 영향을 줄 수 있습니다.
  - [`regexp`](/pkg/regexp/) 패키지는
    [`Regexp`](/pkg/regexp/#Regexp) 유형이
    동시에 실행되는 goroutine에서 안전하게 사용할 수 있도록 합니다.
    이 유형은 정규식 검색 중에 사용되는 스크래치 공간을 보호하는
    [`sync.Mutex`](/pkg/sync/#Mutex)를 사용합니다.
    동일한 `Regexp`를 동시에 사용하는 여러 goroutine은
    이 뮤텍스에 대한 경쟁으로 인해 성능이 저하됩니다.
    이러한 상황에서, `Regexp`는
    [`Copy`](/pkg/regexp/#Regexp) 메서드를 제공합니다.
    이 메서드를 사용하면 원래와 유사한 구조를 가진 다른 `Regexp` 인스턴스를 만들 수 있습니다.
    이러한 두 개의 goroutine은 경쟁 없이 다른 `Regexp` 인스턴스를 사용할 수 있습니다.
    하지만 `Copy`는 추가된 공간 오버헤드를 가지므로, 문제가 발생했음을 관찰한 경우에만 사용해야 합니다.
  - [`encoding`](/pkg/encoding/) 패키지의
    [`strconv`](/pkg/strconv/) 패키지는 이제
    [`tag and class constants](/pkg/encoding/strconv/#pkg-constants)를 내보냅니다.
    이러한 상수는 ASN.1 구조의 고급 파싱에 유용합니다.
  - 또한 [`encoding`](/pkg/encoding/) 패키지,
    [`Unmarshal`](/pkg/encoding/strconv/#Unmarshal)는 이제
    일반적으로 허용되지 않는 다양한 정수 및 길이 인코딩을 거부합니다.
  - [`encoding/base64`](/pkg/encoding/base64) 패키지의
    [`Decoder`](/pkg/encoding/base64/#Decoder)는 이제
    입력의 마지막 바이트를 처리하도록 수정되었습니다. 이전에 4바이트 토큰을 최대한 처리했지만 나머지를 무시했습니다.
    따라서 `Decoder`는 패딩되지 않은 인코딩 (예:
    [RawURLEncoding](/pkg/encoding/base64/#RawURLEncoding))을 올바르게 처리하지만, 마지막에 공백이 있는 패딩된 인코딩 또는 유효하지 않은 바이트로 끝나는 패딩된 인코딩도 거부합니다.
  - [`encoding/json`](/pkg/encoding/json/) 패키지는
    [`Number`](/pkg/encoding/json/#Number)
    의 구문을 JSON 사양에 따라 준수하는지 확인하기 전에 마셜링하기 전에 확인합니다.
    이전 버전과 마찬가지로, 빈 `Number` (빈 문자열)는 0 (영)으로 마셜링됩니다.
  - [`encoding/xml`](/pkg/encoding/xml/) 패키지의
    [`Marshal`](/pkg/encoding/xml/#Marshal) 함수는 이제
    `cdata` 속성을 지원합니다. 즉,
    `<![CDATA[ ... ]]>` 태그 내에 인코딩합니다.
  - 또한 [`encoding/xml`](/pkg/encoding/xml/) 패키지에서,
    [`Decoder`](/pkg/encoding/xml/#Decoder)'s
    [`Token`](/pkg/encoding/xml/#Decoder.Token) 메서드는 이제
    입력에 열린 태그가 모두 보이지 않은 상태에서 EOF에 도달할 때 오류를 보고합니다.
    이 요구 사항을 피하려면 `RawToken`을 사용하십시오.
  - [`fmt`](/pkg/fmt/) 패키지는 이제
    어떤 정수 유형도
    [`Printf`](/pkg/fmt/#Printf)'s `*` 폭 및 정밀도 사양으로 전달할 수 있습니다.
    이전 버전에서는 `*` 인수의 유형이 `int`여야 했습니다.
  - 또한 [`fmt`](/pkg/fmt/) 패키지에서,
    [`Scanf`](/pkg/fmt/#Scanf)는 이제 %X를 사용하여
    16진수 문자열을 스캔할 수 있습니다.
    두 형식 모두 대- 및 소문자 16진수 조합을 허용합니다.
  - [`image`](/pkg/image/)
    및
    [`image/color`](/pkg/image/color/) 패키지는
    [`NYCbCrA`](/pkg/image/#NYCbCrA) 및
    [`NYCbCrA`](/pkg/image/color/#NYCbCrA) 유형을 추가하여
    비-전단계 알파를 갖는 Y'CbCr 이미지를 지원합니다.
  - [`io`](/pkg/io/) 패키지의
    [`MultiWriter`](/pkg/io/#MultiWriter) 구현은 이제
    [`WriteString`](/pkg/io/#WriteString)를 사용하여
    [`WriteString`](/pkg/io/#WriteString)에 사용됩니다.
  - [`math/big`](/pkg/math/big/) 패키지는
    [`Int`](/pkg/math/big/#Int)에
    [`Append`](/pkg/math/big/#Int.Append) 및
    [`Text`](/pkg/math/big/#Int.Text) 메서드를 추가하여 더 많은 제어를 제공합니다.
  - 또한 [`math/big`](/pkg/math/big/) 패키지에서,
    [`Float`](/pkg/math/big/#Float)는 이제
    [`encoding.TextMarshaler`](/pkg/encoding/#TextMarshaler) 및
    [`encoding.TextUnmarshaler`](/pkg/encoding/#TextUnmarshaler)를 구현하여
    [`encoding/json`](/pkg/encoding/json/) 및
    [`encoding/xml`](/pkg/encoding/xml/) 패키지가 자연스러운 형식으로 시리얼화할 수 있습니다.
  - 또한 [`math/big`](/pkg/math/big/) 패키지에서,
    [`Float`](/pkg/math/big/#Float)'s
    [`Append`](/pkg/math/big/#Float.Append) 메서드는 이제 -1 정밀도 인수를 지원합니다.
    [`strconv.ParseFloat`](/pkg/strconv/#ParseFloat)와 마찬가지로,
    정밀도 -1은 최소한의 숫자를 사용하여,
    [`Parse`](/pkg/math/big/#Float.Parse)
    함수에 전달할 때 원래 값을 생성하는 정밀도로
    [`Parse`](/pkg/math/big/#Float.Parse)
    함수에 전달합니다.
  - [`math/rand`](/pkg/math/rand/) 패키지는
    [`Read`](/pkg/math/rand/#Read) 함수와 함께
    [`Rand`](/pkg/math/rand/#Rand)에
    [`Read`](/pkg/math/rand/#Rand.Read) 메서드를 추가합니다.
    이러한 기능은 테스트 데이터를 생성하는 데 도움이 됩니다.
    하지만 주의하십시오.
    이러한 기능은 암호화 목적으로 사용해서는 안 됩니다.
    이러한 목적으로는 [`crypto/rand`](/pkg/crypto/rand/) 패키지를 사용하십시오.
  - [`net`](/pkg/net/) 패키지의
    [`ParseMAC`](/pkg/net/#ParseMAC) 함수는 이제
    20바이트 IP-over-InfiniBand (IPoIB) 링크-레이어 주소를 받습니다.
  - 또한 [`net`](/pkg/net/) 패키지에서,
    DNS 쿼리에 대한 몇 가지 변경 사항이 있습니다.
    첫째, 오류 유형인
    [`DNSError`](/pkg/net/#DNSError) 오류 구현이
    이제 `Error`를 구현합니다 (특히, `IsTemporary` 메서드는
    `IsTemporary`](/pkg/net/#DNSError.IsTemporary)
    함수가 DNS 서버 오류를 반환합니다.
    둘째, DNS 쿼리 함수인
    [`LookupAddr`](/pkg/net/#LookupAddr)
    이제 계획 9 및 Windows에서 루트 도메인 이름을 반환합니다 (결국 점이 포함됨).
    이 동작은 Unix 시스템에서 Go가 따르는 동작과 일치합니다.
  - [`net/http`](/pkg/net/http/) 패키지는 HTTP/2 지원에 더해 추가된 몇 가지 미세한 기능이 있습니다.
    첫째, `FileServer`가 생성된 디렉토리 목록을 파일 이름별로 정렬합니다.
    둘째, `ServeFile` 함수는 요청의 URL 경로에 “..” (점-점)를 포함하는 결과를 제공하지 않습니다.
    이러한 경우 사용자는
    [`FileServer`](/pkg/net/http/#FileServer) 및
    [`Dir`](/pkg/net/http/#Dir)
    를 호출해야 합니다.
    점-점 경로가 필요한 경우
    [`ServeContent`](/pkg/net/http/#ServeContent)를 호출할 수도 있습니다.
    셋째, `Client`는
    [`Transport.ExpectContinueTimeout`](/pkg/net/http/#Transport)를 설정할 수 있도록 합니다.
    넷째, RFC 6585에 정의된 다섯 가지 새로운 오류 코드가 추가되었습니다.
    `StatusPreconditionRequired` (428),
    `StatusTooManyRequests` (429),
    `StatusRequestHeaderFieldsTooLarge` (431), 및
    `StatusNetworkAuthenticationRequired` (511).
    마지막으로, `CloseNotifier`
    의 구현 및 설명이 크게 변경되었습니다.
    `Hijacker`
    인터페이스는 이전에 `CloseNotifier`를 사용하여 사용된 연결에서도 제대로 작동합니다.
    `CloseNotifier`를 사용하는 경우에 작동하는 방식에 대한 설명이 제공됩니다.
  - [`net/http/httptest`](/pkg/net/http/httptest/) 패키지의
    [`ResponseRecorder`](/pkg/net/http/httptest/#ResponseRecorder)는 이제
    [`http.Server`](/pkg/net/http/#Server)의
    [`Content-Type` 헤더를 동일한 알고리즘으로 초기화합니다.
  - [`net/url`](/pkg/net/url/) 패키지의
    [`Parse`](/pkg/net/url/#Parse) 함수는 이제
    호스트 이름의 파싱에 대해 더 엄격하고, 더 엄격하게 사양 준수를 합니다.
  - 또한 [`net/url`](/pkg/net/url/) 패키지에서,
    [`Error`](/pkg/net/url/#Error) 유형이
    이제 `net.Error`를 구현합니다.
  - [`os`](/pkg/os/) 패키지의
    [`IsExist`](/pkg/os/#IsExist),
    [`IsNotExist`](/pkg/os/#IsNotExist), 및
    [`IsPermission`](/pkg/os/#IsPermission) 함수는 이제
    `SyscallError`를 쿼리할 때 올바른 결과를 반환합니다.
  - Unix 시스템에서는,
    `os.Stdout` 또는 `os.Stderr` (더 정확하게는 파일 설명자 1 또는 2에 쓰기하는 `os.File`)에 대한 쓰기가 실패하면,
    브이커 오류가 발생하면 프로그램이 `SIGPIPE` 신호를 발생시킵니다.
    이 신호는 기본적으로 프로그램을 종료합니다. 하지만
    [`os/signal`](/pkg/os/signal)
    의 `Notify` 함수를 호출하여 이 신호를 catch할 수 있습니다.
