## Go 1.4 소개 {#introduction}

최신 Go 릴리스인 버전 1.4가 1.3 출시 6개월 후 예정대로 공개되었습니다.

이 내용은 단 하나의 아주 작은 언어 변경 사항만을 포함하고 있습니다.
하나는 `for`-`range` 루프의 하위 호환 가능한 단순 변형 형태이며,
다른 하나는 포인터-투-포인터(pointers-to-pointers)의 메서드와 관련된 컴파일러의 잠재적인 파괴적 변경 사항(breaking change)입니다.

이번 릴리스는 주로 구현 작업에 집중하고 있으며, 가비지 컬렉터를 개선하고 향후 몇 번의 릴리스에 걸쳐 도입될 완전한 동시성(fully concurrent) 컬렉터를 위한 기반을 마련하는 데 중점을 두었습니다.

이제 스택은 연속적인 구조를 가지며, 새로운 "세그먼트"를 연결하는 대신 필요할 때 재할당됩니다. 따라서 이번 릴리스를 통해 악명 높았던 "hot stack split" 문제가 해결되었습니다.

빌드 시 소스 코드 생성을 위한 `go` 명령의 지원을 포함하여 몇 가지 새로운 도구들이 제공됩니다.

또한 이번 릴리스에서는 Android 및 Native Client(NaCl)의 ARM 프로세서와 Plan 9의 AMD64에 대한 지원이 추가되었습니다.

언제나 그렇듯이, Go 1.4는 [호환성 약속](/doc/go1compat.html)을 준수하며, 거의 모든 코드가 1.4로 옮겨졌을 때 변경 없이 계속해서 컴파일되고 실행될 것입니다.

## 언어 변경 사항 {#language}

### For-range 루프 {#forrange}

Go 1.3까지 `for`-`range` 루프에는 두 가지 형태가 있었습니다.

```go
for i, v := range x {
		...
	}
```

제공해주신 입력값이 "and"뿐이라 번역할 내용이 없습니다. 번역이 필요한 Markdown 콘텐츠를 입력해 주시면, 요청하신 지침에 따라 정중하고 정확하게 기술 번역을 진행하겠습니다.

```go
for i := range x {
		...
	}
```

루프 값에는 관심이 없고 반복 그 자체에만 관심이 있는 경우에도, 여전히 변수(아마도 `for` `_` `=` `range` `x`에서와 같이 [blank identifier](/ref/spec#Blank_identifier))를 언급해야 했습니다. 왜냐하면 다음과 같은 형태는

`for range x {
		...
	}`

구문적으로 허용되지 않았습니다.

이 상황은 어색해 보였으며, 이에 따라 Go 1.4부터는 변수가 없는 형태가 허용됩니다.
이러한 패턴은 드물게 나타나지만, 발생했을 때 코드를 더 깔끔하게 만들 수 있습니다.

_업데이트_: 이 변경 사항은 기존 Go 프로그램과 엄격하게 하위 호환되지만, Go 파스 트리를 분석하는 도구는 수정이 필요할 수 있습니다. [`RangeStmt`](/pkg/go/ast/#RangeStmt)의 `Key` 필드가 이제 `nil`일 수 있기 때문입니다.

### \*\*T에 대한 메서드 호출 {#methodonpointertopointer}

다음 선언들이 주어졌을 때,

```go
type T int
	func (T) M() {}
	var x **T
```

`gc`와 `gccgo` 모두 해당 메서드 호출을 허용했습니다.

Please provide the Markdown content you would like me to translate. You only provided `x.M()`, which appears to be a code snippet. I am ready to translate your technical documentation once you provide the text.

이는 포인터-투-포인터(pointer-to-pointer) `x`를 두 번 역참조(double dereference)하는 것입니다.
Go 명세에서는 단일 역참조의 자동 삽입은 허용하지만, 두 번의 역참조는 허용하지 않으므로 언어 정의에 따라 이 호출은 잘못된 것입니다.
따라서 Go 1.4에서는 이를 금지했으며, 이는 breaking change에 해당하지만 영향을 받는 프로그램은 매우 적을 것입니다.

_업데이트_: 이전의 잘못된 동작에 의존하던 코드는 더 이상 컴파일되지 않으나, 명시적 역참조(dereference)를 추가함으로써 쉽게 수정할 수 있습니다.

## 지원되는 운영 체제 및 아키텍처 변경 사항 {#os}

### Android {#android}

Go 1.4는 Android 운영 체제에서 실행되는 ARM 프로세서용 바이너리를 빌드할 수 있습니다.
또한 [mobile](https://golang.org/x/mobile) 서브리포지토리의 지원 패키지를 사용하여 Android 애플리케이션에서 로드할 수 있는 `.so` 라이브러리를 빌드할 수 있습니다.
이 실험적인 포팅 계획에 대한 간략한 설명은 [여기](/s/go14android)에서 확인할 수 있습니다.

### ARM에서의 NaCl {#naclarm}

이전 릴리스에서는 32비트 x86(`GOARCH=386`) 및 32비트 포인터를 사용하는 64비트 x86(`GOARCH=amd64p32`)에 대한 Native Client (NaCl) 지원이 도입되었습니다.
1.4 릴리스에서는 ARM(`GOARCH=arm`)에 대한 NaCl 지원이 추가되었습니다.

### AMD64 기반의 Plan9 {#plan9amd64}

이번 릴리스에서는 커널이 `nsec` 시스템 호출을 지원하고 4K 페이지를 사용하는 경우, AMD64 프로세서의 Plan 9 운영 체제에 대한 지원이 추가되었습니다.

## 호환성 가이드라인 변경 사항 {#compatibility}

[`unsafe`](/pkg/unsafe/) 패키지를 사용하면 구현의 내부 세부 사항이나 데이터의 머신 표현을 이용하여 Go의 타입 시스템을 무력화할 수 있습니다.

[Go 호환성 가이드라인](go1compat.html)에 명시된 호환성과 관련하여 `unsafe` 사용이 무엇을 의미하는지는 명시적으로 규정된 적이 없었습니다.

당연하게도, 그 답은 unsafe한 작업을 수행하는 코드에 대해서는 호환성을 보장할 수 없다는 것입니다.

릴리스에 포함된 문서에서 이 상황을 명확히 설명했습니다.
[Go 호환성 가이드라인](go1compat.html)과 [`unsafe`](/pkg/unsafe/) 패키지 문서는 이제 unsafe 코드가 호환성을 유지한다는 보장이 없음을 명시적으로 밝히고 있습니다.

_업데이트_: 기술적인 변경 사항은 없으며, 문서의 내용을 명확하게 하기 위한 수정입니다.

## 구현 및 도구의 변경 사항 {#impl}

### 런타임 변경 사항 {#runtime}

Go 1.4 이전에는 런타임(가비지 컬렉터, 동시성 지원, 인터페이스 관리, maps, slices, strings, ...)의 대부분이 C 언어로 작성되었으며, 일부 어셈블러 지원이 포함되어 있었습니다.
1.4 버전에서는 가비지 컬렉터가 런타임 내 프로그램의 스택을 스캔하여 어떤 변수가 활성 상태인지에 대한 정확한 정보를 얻을 수 있도록, 많은 코드가 Go로 변환되었습니다.
이 변경 사항은 규모가 컸지만, 프로그램의 시맨틱(semantic)에는 아무런 영향을 미치지 않아야 합니다.

이 리라이트는 1.4의 가비지 컬렉터가 완전 정밀(fully precise)하게 동작하도록 하며, 이는 프로그램 내의 모든 활성 포인터 위치를 인식함을 의미합니다. 이는 포인터가 아닌 데이터가 포인터로 오인되어 메모리에 유지되는 오탐(false positives)이 발생하지 않으므로, 힙 크기가 더 줄어든다는 것을 의미합니다. 기타 관련 변경 사항들 또한 힙 크기를 줄여, 이전 릴리스 대비 전체적으로 10%~30% 더 작아졌습니다.

그 결과 스택이 더 이상 세그먼트화되지 않으며, "hot split" 문제가 제거되었습니다.
스택 제한에 도달하면 더 큰 새로운 스택이 할당되고, 해당 goroutine의 모든 활성 프레임이 그곳으로 복사되며, 스택을 가리키는 모든 포인터가 업데이트됩니다.
일부 사례에서는 성능이 눈에 띄게 향상될 수 있으며, 항상 더 예측 가능해집니다.
자세한 내용은 [설계 문서](/s/contigstacks)에서 확인할 수 있습니다.

연속 스택(contiguous stacks)을 사용하면 성능 저하 없이 스택을 더 작게 시작할 수 있으며, 이에 따라 1.4 버전에서 고루틴 스택의 기본 시작 크기가 8192바이트에서 2048바이트로 줄어들었습니다.

1.5 릴리스에 예정된 동시성 가비지 컬렉터(concurrent garbage collector)를 준비하기 위해, 힙(heap)의 포인터 값에 대한 쓰기 작업은 이제 값을 업데이트하는 함수에서 직접 수행하는 대신 '쓰기 배리어(write barrier)'라고 불리는 함수 호출을 통해 수행됩니다.
다음 릴리스에서 이는 가비지 컬렉터가 실행되는 동안 힙에 대한 쓰기 작업을 중재할 수 있게 해줄 것입니다.
이 변경 사항은 1.4 버전의 프로그램에 세만틱(semantic)한 영향을 주지는 않지만, 컴파일러와 그로 인한 성능을 테스트하기 위해 이번 릴리스에 포함되었습니다.

인터페이스 값의 구현이 변경되었습니다.
이전 릴리스에서는 저장된 구체적인 객체의 유형에 따라 인터페이스가 포인터 또는 한 단어(one-word) 크기의 스칼라 값을 포함했습니다.
이러한 구현은 가비지 컬렉터(garbage collector)에 문제가 되었으며, 이에 따라 1.4 버전부터 인터페이스 값은 항상 포인터를 보유합니다.
실행 중인 프로그램에서 대부분의 인터페이스 값은 이미 포인터였으므로 영향은 미미하지만, 인터페이스에 정수(예시) 등을 저장하는 프로그램에서는 더 많은 할당(allocation)이 발생하게 됩니다.

Go 1.3부터 런타임은 유효한 포인터를 포함해야 할 메모리 워드에 명백히 유효하지 않은 포인터(예: 값 3)가 포함되어 있는 것을 발견하면 크래시가 발생합니다. 포인터 값에 정수를 저장하는 프로그램은 이 체크로 인해 문제가 발생하여 크래시가 날 수 있습니다.

Go 1.4에서는 [`GODEBUG`](/pkg/runtime/) 변수를 `invalidptr=0`으로 설정하여 임시 방편으로 크래시를 비활성화할 수 있지만, 향후 릴리스에서도 이 크래시를 피할 수 있다고 보장할 수 없습니다. 올바른 해결 방법은 정수와 포인터를 앨리어싱(alias)하지 않도록 코드를 다시 작성하는 것입니다.

### Assembly {#asm}

`cmd/5a`, `cmd/6a` 및 `cmd/8a` 어셈블러가 허용하는 언어에는 여러 변경 사항이 있었으며, 이는 주로 런타임에 타입 정보를 더 쉽게 전달하기 위함입니다.

먼저, `TEXT` 지시어에 대한 플래그를 정의하는 `textflag.h` 파일이 단순한 지시어로 포함될 수 있도록 링커 소스 디렉토리에서 표준 위치로 복사되었습니다.

#include "textflag.h"

더 중요한 변경 사항은 어셈블러 소스가 필요한 타입 정보를 정의하는 방식에 있습니다.
대부분의 프로그램의 경우, 데이터 정의(`DATA` 및 `GLOBL` 지시어)를 어셈블리에서 Go 파일로 옮기고, 각 어셈블리 함수에 대해 Go 선언을 작성하는 것으로 충분할 것입니다.
[어셈블리 문서](/doc/asm#runtime)에 처리 방법이 설명되어 있습니다.

_업데이트_:
이전 위치에서 `textflag.h`를 포함하는 어셈블리 파일들은 여전히 작동하지만, 업데이트하는 것이 권장됩니다.
타입 정보의 경우, 대부분의 어셈블리 루틴은 변경이 필요 없으나 모두 검토해야 합니다.
데이터를 정의하거나, 비어 있지 않은 스택 프레임을 가진 함수, 또는 포인터를 반환하는 함수를 정의하는 어셈블리 소스 파일은 특히 주의가 필요합니다.
필요한 (하지만 간단한) 변경 사항에 대한 설명은 [어셈블리 문서](/doc/asm#runtime)에 있습니다.

이러한 변경 사항에 대한 더 자세한 내용은 [assembly document](/doc/asm)에 나와 있습니다.

### gccgo 상태 {#gccgo}

GCC와 Go 프로젝트의 릴리스 일정은 서로 일치하지 않습니다.
GCC 릴리스 4.9에는 gccgo의 Go 1.2 버전이 포함되어 있습니다.
다음 릴리스인 GCC 5에는 gccgo의 Go 1.4 버전이 포함될 가능성이 높습니다.

### 내부 패키지 (Internal packages) {#internalpackages}

Go의 패키지 시스템은 프로그램을 명확한 경계를 가진 컴포넌트로 구조화하기 쉽게 만들어 주지만, 접근 권한은 로컬(unexported)과 글로벌(exported) 두 가지 형태만 존재합니다. 때로는 내보내기(export) 되지 않는 컴포넌트가 필요할 때가 있습니다. 예를 들어, 공용 저장소의 일부이지만 해당 프로그램 외부에서 사용할 의도가 없는 코드의 인터페이스에 대해 클라이언트가 생성되는 것을 방지하고 싶은 경우입니다.

Go 언어 자체는 이러한 구분을 강제할 능력이 없지만, Go 1.4부터 [`go`](/cmd/go/) 커맨드에 해당 패키지가 위치한 소스 서브트리 외부의 패키지에서 임포트할 수 없는 "internal" 패키지를 정의하는 메커니즘이 도입되었습니다.

그러한 패키지를 생성하려면, `internal`이라는 이름의 디렉토리나 `internal`이라는 이름의 디렉토리 하위 디렉토리에 배치하십시오.
`go` 명령어가 경로에 `internal`이 포함된 패키지의 임포트(import)를 발견하면, 임포트를 수행하는 패키지가 `internal` 디렉토리의 부모를 루트로 하는 트리 내에 있는지 확인합니다.
예를 들어, `.../a/b/c/internal/d/e/f` 패키지는 `.../a/b/c`를 루트로 하는 디렉토리 트리 내의 코드에서만 임포트할 수 있습니다.
`.../a/b/g`에 있는 코드나 다른 저장소에 있는 코드에서는 임포트할 수 없습니다.

Go 1.4의 경우, 내부 패키지(internal package) 메커니즘은 메인 Go 저장소에 대해서만 강제 적용됩니다. 1.5 버전부터는 모든 저장소에 대해 강제 적용됩니다.

메커니즘에 대한 자세한 내용은
[설계 문서](/s/go14internal)에 나와 있습니다.

### 정식 임포트 경로 (Canonical import paths) {#canonicalimports}

코드는 종종 `github.com`과 같은 공개 서비스에서 호스팅되는 저장소에 저장됩니다. 이는 패키지의 임포트 경로가 호스팅 서비스의 이름으로 시작함을 의미하며, 예를 들어 `github.com/rsc/pdf`와 같습니다.
[기존 메커니즘](/cmd/go/#hdr-Remote_import_paths)을 사용하여 `rsc.io/pdf`와 같은 "커스텀(custom)" 또는 "배니티(vanity)" 임포트 경로를 제공할 수 있지만, 이는 해당 패키지에 대해 두 개의 유효한 임포트 경로를 생성하게 됩니다.
이는 문제가 됩니다. 하나의 프로그램에서 실수로 두 개의 서로 다른 경로를 통해 패키지를 임포트하여 자원을 낭비할 수 있고, 사용 중인 경로가 오래된 것으로 인식되지 않아 패키지 업데이트를 놓칠 수 있으며, 패키지를 다른 호스팅 서비스로 이동함으로써 이전 경로를 사용하는 클라이언트를 중단시킬 수 있기 때문입니다.

Go 1.4는 Go 소스 코드의 패키지 절(package clause)에 해당 패키지의 정식(canonical) 임포트 경로를 식별하는 어노테이션을 도입합니다.
정식 경로가 아닌 경로를 사용하여 임포트를 시도하면, [`go`](/cmd/go/) 커맨드는 임포트하는 패키지의 컴파일을 거부합니다.

구문은 간단합니다. 패키지 라인에 식별용 주석을 추가하십시오.
우리의 예제에서 패키지 절은 다음과 같이 작성됩니다:

package pdf // import "rsc.io/pdf"

이렇게 설정하면, `go` 명령어는 `github.com/rsc/pdf`를 임포트하는 패키지의 컴파일을 거부하게 되며, 이를 통해 사용자에게 영향을 주지 않고 코드를 이동시킬 수 있습니다.

이 검사는 다운로드 시점이 아니라 빌드 시점에 수행됩니다. 따라서 이 검사로 인해 `go` `get`이 실패한다면, 잘못 임포트된 패키지가 이미 로컬 머신으로 복사된 상태이므로 수동으로 제거해야 합니다.

이 새로운 기능을 보완하기 위해, 로컬 패키지의 원격 저장소가 커스텀 임포트(custom import)의 저장소와 일치하는지 확인하는 체크 로직이 업데이트 시점에 추가되었습니다.
`go` `get` `-u` 명령은 패키지가 처음 다운로드된 이후 원격 저장소가 변경되었다면 업데이트에 실패하게 됩니다.
새로 추가된 `-f` 플래그는 이 체크 과정을 무시합니다.

더 자세한 정보는 [설계 문서](/s/go14customimport)에서 확인할 수 있습니다.

### 서브리포지토리의 임포트 경로 {#subrepo}

Go 프로젝트 서브 리포지토리(`code.google.com/p/go.tools` 등)를 이제 `code.google.com/p/go.`를 `golang.org/x/`로 대체한 커스텀 임포트 경로(예: `golang.org/x/tools`)를 통해 사용할 수 있습니다.

2015년 6월 1일경에 코드에 정규(canonical) 임포트 주석을 추가할 예정이며, 이 시점부터 Go 1.4 및 이후 버전에서는 이전의 `code.google.com` 경로를 더 이상 허용하지 않습니다.

_업데이트_: 서브리포지토리(subrepositories)에서 임포트하는 모든 코드는 새로운 `golang.org` 경로를 사용하도록 변경해야 합니다.
Go 1.0 및 이후 버전은 새로운 경로를 해석하고 임포트할 수 있으므로, 업데이트하더라도 이전 릴리스와의 호환성이 깨지지 않습니다.
업데이트하지 않은 코드는 2015년 6월 1일경부터 Go 1.4에서 컴파일되지 않게 됩니다.

### go generate 하위 명령어 {#gogenerate}

[`go`](/cmd/go/) 명령에 새로운 서브커맨드인
[`go generate`](/cmd/go/#hdr-Generate_Go_files_by_processing_source)가 추가되었습니다.
이는 컴파일 전에 소스 코드를 생성하는 도구들의 실행을 자동화하기 위한 것입니다.
예를 들어, `.y` 파일에 [`yacc`](/cmd/yacc) 컴파일러-컴파일러를 실행하여 문법을 구현하는 Go 소스 파일을 생성하거나, `golang.org/x/tools` 서브리포지토리의 새로운 [stringer](https://godoc.org/golang.org/x/tools/cmd/stringer) 도구를 사용하여 타입화된 상수(typed constants)를 위한 `String` 메서드 생성을 자동화하는 데 사용할 수 있습니다.

더 자세한 정보는 [설계 문서](/s/go1.4-generate)를 참조하십시오.

### 파일 이름 처리 변경 사항 {#filenames}

빌드 제약 조건(build constraints)은 빌드 태그(build tags)라고도 하며, 파일의 포함 또는 제외를 통해 컴파일을 제어합니다 ([`/go/build`](/pkg/go/build/) 문서 참조).
또한 파일 이름 자체에 언더스코어(`_`)와 아키텍처 또는 운영체제 이름을 접미사로 붙여( `.go` 또는 `.s` 확장자 앞) "태깅"함으로써 컴파일을 제어할 수 있습니다.
예를 들어, `gopher_arm.go` 파일은 대상 프로세서가 ARM인 경우에만 컴파일됩니다.

Go 1.4 이전에는 `arm.go`와 같은 파일이 유사하게 태그되었으나, 이러한 동작은 새로운 아키텍처가 추가될 때 파일이 갑자기 태그되어 소스 코드가 손상될 수 있습니다. 따라서 1.4 버전부터는 태그(아키텍처 또는 운영체제 이름) 앞에 언더스코어(`_`)가 붙어 있는 경우에만 파일이 이러한 방식으로 태그됩니다.

_업데이트_: 이전 동작에 의존하는 패키지는 더 이상 올바르게 컴파일되지 않습니다.
`windows.go` 또는 `amd64.go`와 같은 이름의 파일은 소스에 명시적인 빌드 태그(build tags)를 추가하거나, `os_windows.go` 또는 `support_amd64.go`와 같은 이름으로 변경해야 합니다.

### go 명령어의 기타 변경 사항 {#gocmd}

[`cmd/go`](/cmd/go/)
명령어에 주목할 만한 몇 가지 사소한 변경 사항이 있었습니다.

- [`cgo`](/cmd/cgo/)를 사용하여 패키지를 빌드하지 않는 한, 이제 `go` 커맨드는 C 소스 파일의 컴파일을 거부합니다. 이는 관련 C 컴파일러([`6c`](/cmd/6c/) 등)가 향후 릴리스에서 설치 항목에서 제거될 예정이기 때문입니다. (현재 이들은 런타임의 일부를 빌드하는 데만 사용됩니다.) 어떠한 경우에도 이들을 올바르게 사용하기 어렵기 때문에, 기존의 사용 사례들은 잘못되었을 가능성이 높으며, 이에 따라 해당 기능을 비활성화했습니다.
  - [`go` `test`](/cmd/go/#hdr-Test_packages) 하위 커맨드에 다른 하위 커맨드의 동일한 플래그와 대응하는, 결과 바이너리의 이름을 설정하는 새로운 플래그 `-o`가 추가되었습니다. 기능이 없던 `-file` 플래그는 제거되었습니다.
  - [`go` `test`](/cmd/go/#hdr-Test_packages) 하위 커맨드는 패키지 내의 모든 `*_test.go` 파일에 `Test` 함수가 없더라도 해당 파일들을 컴파일하고 링크합니다. 이전에는 이러한 파일들을 무시했습니다.
  - 개발용이 아닌 설치 환경에서 [`go` `build`](/cmd/go/#hdr-Test_packages) 하위 커맨드의 `-a` 플래그 동작이 변경되었습니다. 정식 릴리스 배포판을 실행하는 설치 환경의 경우, 설치된 파일이 덮어쓰여지는 것을 방지하기 위해 `-a` 플래그가 더 이상 표준 라이브러리와 커맨드들을 재빌드하지 않습니다.

### 패키지 소스 레이아웃 변경 사항 {#pkg}

메인 Go 소스 저장소에서 패키지의 소스 코드는 `src/pkg` 디렉토리에 보관되었습니다. 이는 타당한 구조였으나 Go 서브 저장소를 포함한 다른 저장소들과는 달랐습니다.
Go 1.4에서는 소스 트리의 `pkg` 레벨이 제거되었습니다. 따라서 예를 들어 이전에 `src/pkg/fmt` 디렉토리에 보관되었던 [`fmt`](/pkg/fmt/) 패키지의 소스는 이제 한 단계 위인 `src/fmt`에 위치합니다.

_업데이트_: 소스 코드를 검색하는 `godoc`와 같은 도구들은 새로운 위치를 알아야 합니다. Go 팀에서 유지 관리하는 모든 도구와 서비스는 업데이트되었습니다.

### SWIG {#swig}

이번 릴리스의 런타임 변경 사항으로 인해, Go 1.4는 SWIG 3.0.3이 필요합니다.

### 기타 {#misc}

표준 저장소의 최상위 `misc` 디렉터리에는 이전의 에디터 및 IDE를 위한 Go 지원 사항(플러그인, 초기화 스크립트 등)이 포함되어 있었습니다. 핵심 팀원들이 사용하는 에디터가 아닌 것들이 많이 포함되어 있었기에, 이를 유지 관리하는 작업은 점점 더 많은 시간을 소모하게 되었으며 외부의 도움이 필요했습니다. 또한, 우리가 사용하지 않는 에디터에 대해서조차 어떤 플러그인이 가장 적합한지에 대한 결정을 내려야 하는 상황이었습니다.

전반적인 Go 커뮤니티가 이러한 정보를 관리하기에 훨씬 더 적합합니다.
따라서 Go 1.4에서는 리포지토리에서 이 지원 기능이 제거되었습니다.
대신, 이용 가능한 항목들에 대해 엄선된 정보 목록이 [위키 페이지](/wiki/IDEsAndTextEditorPlugins)에 마련되어 있습니다.

## Performance {#performance}

대부분의 프로그램은 1.3에서보다 1.4에서 거의 비슷하거나 약간 더 빠르게 실행될 것이며, 일부는 약간 더 느려질 수 있습니다.
변경 사항이 많아 정확히 무엇을 기대할 수 있을지 단정하기 어렵습니다.

앞서 언급했듯이, 런타임의 상당 부분이 C에서 Go로 번역되었으며, 이로 인해 힙 크기가 일부 감소했습니다. 또한, 런타임을 빌드하는 데 사용된 C 컴파일러보다 Go 컴파일러가 인라이닝(inlining)과 같은 최적화에 더 능숙하기 때문에 성능이 약간 향상되었습니다.

가비지 컬렉터의 속도가 향상되어 가비지 발생량이 많은 프로그램에서 측정 가능한 수준의 개선이 이루어졌습니다.
반면, 새로운 write barrier로 인해 속도가 다시 느려졌으며, 일반적으로는 비슷한 정도의 차이를 보이지만, 동작 방식에 따라 일부 프로그램은 다소 더 느려지거나 빨라질 수 있습니다.

성능에 영향을 미치는 라이브러리 변경 사항은 아래에 문서화되어 있습니다.

## 표준 라이브러리 변경 사항 {#library}

### 새 패키지 {#new_packages}

이번 릴리스에는 새로운 패키지가 없습니다.

### 라이브러리의 주요 변경 사항 {#major_library_changes}

#### bufio.Scanner {#scanner}

[`bufio`](/pkg/bufio/) 패키지의 [`Scanner`](/pkg/bufio/#Scanner) 타입에서 커스텀 [`split functions`](/pkg/bufio/#SplitFunc)의 변경이 필요할 수 있는 버그가 수정되었습니다.

해당 버그로 인해 EOF(파일 끝)에서 빈 토큰을 생성하는 것이 불가능했습니다. 이번 수정으로 split 함수가 확인하는 종료 조건이 변경되었습니다. 이전에는 더 이상 데이터가 없으면 EOF에서 스캐닝이 중단되었습니다. 1.4 버전부터는 입력이 모두 소진된 후 EOF에서 split 함수가 한 번 더 호출되므로, 문서에 명시된 대로 split 함수가 최종 빈 토큰을 생성할 수 있게 되었습니다.

_업데이트_: EOF에서의 빈 토큰을 원하는 방식으로 처리하기 위해 사용자 정의 split 함수를 수정해야 할 수도 있습니다.

#### syscall {#syscall}

[`syscall`](/pkg/syscall/) 패키지는 이제 핵심 저장소(core repository) 유지를 위해 필요한 변경 사항을 제외하고 동결되었습니다.
특히, 핵심 저장소에서 사용되지 않는 새로운 또는 다른 시스템 호출을 지원하기 위해 더 이상 확장되지 않습니다.
이에 대한 자세한 이유는 [별도의 문서](/s/go1.4-syscall)에 설명되어 있습니다.

모든 커널의 시스템 콜 지원을 위한 새로운 개발 거점으로 활용될 새로운 서브 리포지토리인 [golang.org/x/sys](https://golang.org/x/sys)가 생성되었습니다.

이 리포지토리는 더 나은 구조를 가지고 있으며, 각각 [Unix](https://godoc.org/golang.org/x/sys/unix), [Windows](https://godoc.org/x/sys/windows), [Plan 9](https://godoc.org/golang.org/x/sys/plan9)의 시스템 콜 구현을 담고 있는 세 개의 패키지로 구성되어 있습니다.

이 패키지들은 해당 운영체제의 커널 인터페이스를 반영하는 모든 합리적인 변경 사항을 수용하며 더욱 관대하게 관리될 예정입니다.

더 자세한 정보는 문서와 위에 언급된 기사를 참조하시기 바랍니다.

_업데이트_: `syscall` 패키지가 1.3 릴리스와 거의 동일하므로 기존 프로그램은 영향을 받지 않습니다.
`syscall` 패키지에 없는 시스템 호출이 필요한 향후 개발은 대신 `golang.org/x/sys`를 기반으로 구축해야 합니다.

### 라이브러리의 사소한 변경 사항 {#minor_library_changes}

다음 목록은 라이브러리의 여러 소규모 변경 사항(주로 추가 사항)을 요약한 것입니다.
각 변경 사항에 대한 자세한 내용은 관련 패키지 문서를 참조하십시오.

- [`archive/zip`](/pkg/archive/zip/) 패키지의 [`Writer`](/pkg/archive/zip/#Writer)가 이제 [`Flush`](/pkg/archive/zip/#Writer.Flush) 메서드를 지원합니다.
  - [`compress/flate`](/pkg/compress/flate/), [`compress/gzip`](/pkg/compress/gzip/), [`compress/zlib`](/pkg/compress/zlib/) 패키지의 디컴프레서(decompressor)가 이제 `Reset` 메서드를 지원하여, 버퍼를 재사용하고 성능을 향상시킬 수 있습니다. [`compress/gzip`](/pkg/compress/gzip/) 패키지에는 멀티스트림 파일 지원을 제어하기 위한 [`Multistream`](/pkg/compress/gzip/#Reader.Multistream) 메서드도 추가되었습니다.
  - [`crypto`](/pkg/crypto/) 패키지에 [`Signer`](/pkg/crypto/#Signer) 인터페이스가 추가되었으며, 이는 [`crypto/ecdsa`](/pkg/crypto/ecdsa)와 [`crypto/rsa`](/pkg/crypto/rsa)의 `PrivateKey` 타입들에 의해 구현되었습니다.
  - [`crypto/tls`](/pkg/crypto/tls/) 패키지가 이제 [RFC 7301](https://tools.ietf.org/html/rfc7301)에 정의된 ALPN을 지원합니다.
  - [`crypto/tls`](/pkg/crypto/tls/) 패키지가 이제 [`Config`](/pkg/crypto/tls/#Config) 구조체의 새로운 [`CertificateForName`](/pkg/crypto/tls/#Config.CertificateForName) 함수를 통해 서버 인증서를 프로그래밍 방식으로 선택하는 기능을 지원합니다.
  - 또한 crypto/tls 패키지의 서버가 이제 [TLS\_FALLBACK\_SCSV](https://tools.ietf.org/html/draft-ietf-tls-downgrade-scsv-00)를 지원하여 클라이언트가 폴백 공격(fallback attacks)을 감지하는 것을 돕습니다. (Go 클라이언트는 폴백을 전혀 지원하지 않으므로 해당 공격에 취약하지 않습니다.)
  - [`database/sql`](/pkg/database/sql/) 패키지에서 이제 등록된 모든 [`Drivers`](/pkg/database/sql/#Drivers) 목록을 나열할 수 있습니다.
  - [`debug/dwarf`](/pkg/debug/dwarf/) 패키지가 이제 [`UnspecifiedType`](/pkg/debug/dwarf/#UnspecifiedType)을 지원합니다.
  - [`encoding/asn1`](/pkg/encoding/asn1/) 패키지에서 기본값이 있는 선택적 요소(optional elements)는 이제 해당 기본값을 가질 때만 생략됩니다.
  - [`encoding/csv`](/pkg/encoding/csv/) 패키지가 더 이상 빈 문자열에 따옴표를 붙이지 않지만, 데이터 종료 마커인 `\.` (백슬래시 점)에는 따옴표를 붙입니다. 이는 CSV 정의에서 허용되며 Postgres와 더 잘 작동하게 합니다.
  - [`encoding/gob`](/pkg/encoding/gob/) 패키지가 unsafe 연산 사용을 제거하도록 재작성되어, [`unsafe`](/pkg/unsafe/) 패키지 사용이 허용되지 않는 환경에서도 사용할 수 있게 되었습니다. 일반적인 사용 시 10-30% 더 느려지지만, 그 차이는 데이터 타입에 따라 다르며 특히 배열이 포함된 일부 경우에는 더 빠를 수 있습니다. 기능적인 변경 사항은 없습니다.
  - [`encoding/xml`](/pkg/encoding/xml/) 패키지의 [`Decoder`](/pkg/encoding/xml/#Decoder)가 이제 입력 오프셋(input offset)을 보고할 수 있습니다.
  - [`fmt`](/pkg/fmt/) 패키지에서 맵 포인터의 포맷팅 방식이 구조체, 배열 등의 포인터 방식과 일치하도록 변경되었습니다. 예를 들어, `&map[string]int{"one":` `1}`은 이제 기본적으로 16진수 포인터 값 대신 `&map[one:` `1]`로 출력됩니다.
  - [`image`](/pkg/image/) 패키지의 [`RGBA`](/pkg/image/#RGBA) 및 [`Gray`](/pkg/image/#Gray)와 같은 [`Image`](/pkg/image/#Image) 구현체들이 일반적인 [`At`](/pkg/image/#Image.At) 메서드와 더불어 특화된 [`RGBAAt`](/pkg/image/#RGBA.RGBAAt) 및 [`GrayAt`](/pkg/image/#Gray.GrayAt) 메서드를 갖게 되었습니다.
  - [`image/png`](/pkg/image/png/) 패키지에 인코딩에 사용되는 압축 레벨을 제어할 수 있는 [`Encoder`](/pkg/image/png/#Encoder) 타입이 추가되었습니다.
  - [`math`](/pkg/math/) 패키지에 [`Nextafter32`](/pkg/math/#Nextafter32) 함수가 추가되었습니다.
  - [`net/http`](/pkg/net/http/) 패키지의 [`Request`](/pkg/net/http/#Request) 타입에 HTTP Basic Authentication 스킴을 사용하는 인증된 요청에서 사용자 이름과 비밀번호를 반환하는 새로운 [`BasicAuth`](/pkg/net/http/#Request.BasicAuth) 메서드가 추가되었습니다.
  - [`net/http`](/pkg/net/http/) 패키지의 [`Transport`](/pkg/net/http/#Request) 타입에 외부 TLS 연결 동작을 커스텀할 수 있는 새로운 [`DialTLS`](/pkg/net/http/#Transport.DialTLS) 훅이 추가되었습니다.
  - [`net/http/httputil`](/pkg/net/http/httputil/) 패키지의 [`ReverseProxy`](/pkg/net/http/httputil/#ReverseProxy) 타입에 로깅 제어 기능을 제공하는 새로운 필드 [`ErrorLog`](/pkg/net/http/#ReverseProxy.ErrorLog)가 추가되었습니다.
  - [`os`](/pkg/os/) 패키지가 이제 Windows 운영 체제에서 [`Symlink`](/pkg/os/#Symlink) 함수를 통해 심볼릭 링크를 구현합니다. 다른 운영 체제는 이미 이 기능을 지원하고 있었습니다. 또한 새로운 [`Unsetenv`](/pkg/os/#Unsetenv) 함수가 추가되었습니다.
  - [`reflect`](/pkg/reflect/) 패키지의 [`Type`](/pkg/reflect/#Type) 인터페이스에 해당 타입이 일반 비교를 구현하는지 여부를 보고하는 새로운 메서드 [`Comparable`](/pkg/reflect/#type.Comparable)가 추가되었습니다.
  - 또한 [`reflect`](/pkg/reflect/) 패키지에서 런타임의 인터페이스 구현 변경으로 인해 [`Value`](/pkg/reflect/#Value) 인터페이스가 이제 4워드에서 3워드로 변경되었습니다. 이는 메모리를 절약하지만 의미론적인 영향은 없습니다.
  - [`runtime`](/pkg/runtime/) 패키지가 이제 다른 시스템과 마찬가지로 Windows에서도 모노토닉 클락(monotonic clocks)을 구현합니다.
  - [`runtime`](/pkg/runtime/) 패키지의 [`Mallocs`](/pkg/runtime/#MemStats.Mallocs) 카운터가 이제 Go 1.3에서 누락되었던 매우 작은 할당까지 카운트합니다. 이로 인해 더 정확한 결과가 나오게 되어, [`ReadMemStats`](/pkg/runtime/#ReadMemStats) 또는 [`AllocsPerRun`](/pkg/testing/#AllocsPerRun)을 사용하는 테스트가 실패할 수 있습니다.
  - [`runtime`](/pkg/runtime/) 패키지의 [`MemStats`](/pkg/runtime/#MemStats) 및 [`GCStats`](/pkg/runtime/#GCStats) 구조체에 [`PauseEnd`](/pkg/runtime/#MemStats.PauseEnd) 배열이 추가되었습니다. 이 배열은 가비지 컬렉션 일시 중단이 종료된 시간들의 순환 버퍼입니다. 해당 일시 중단 지속 시간은 이미 [`PauseNs`](/pkg/runtime/#MemStats.PauseNs)에 기록되고 있습니다.
  - [`runtime/race`](/pkg/runtime/race/) 패키지가 이제 FreeBSD를 지원하며, 이는 [`go`](/pkg/cmd/go/) 명령의 `-race` 플래그가 이제 FreeBSD에서 작동함을 의미합니다.
  - [`sync/atomic`](/pkg/sync/atomic/) 패키지에 새로운 타입 [`Value`](/pkg/sync/atomic/#Value)가 추가되었습니다. `Value`는 임의의 타입 값에 대해 원자적 로드(load) 및 저장(store)을 수행하는 효율적인 메커니즘을 제공합니다.
  - Linux의 [`syscall`](/pkg/syscall/) 패키지 구현에서 [`Setuid`](/pkg/syscall/#Setuid)와 [`Setgid`](/pkg/syscall/#Setgid) 기능이 비활성화되었습니다. 해당 시스템 콜은 전체 프로세스가 아닌 호출한 스레드에만 작용하며, 이는 다른 플랫폼과 다르고 예상되는 결과가 아니기 때문입니다.
  - [`testing`](/pkg/testing/) 패키지에 테스트 세트 실행을 더 세밀하게 제어할 수 있는 새로운 기능이 추가되었습니다. 테스트 코드에 다음과 같은 함수가 포함되어 있다면:
    <pre>
    func TestMain(m *<a href="/pkg/testing/#M"><code>testing.M</code></a>)
    </pre>
    테스트를 직접 실행하는 대신 이 함수가 호출됩니다. `M` 구조체는 테스트에 접근하고 실행하기 위한 메서드들을 포함하고 있습니다.
  - 또한 [`testing`](/pkg/testing/) 패키지에 현재 테스트 커버리지 비율을 보고하는 새로운 [`Coverage`](/pkg/testing/#Coverage) 함수가 추가되어, 개별 테스트가 전체 커버리지에 얼마나 기여하는지 보고할 수 있게 되었습니다.
  - [`text/scanner`](/pkg/text/scanner/) 패키지의 [`Scanner`](/pkg/text/scanner/#Scanner) 타입에 새로운 함수 [`IsIdentRune`](/pkg/text/scanner/#Scanner.IsIdentRune)가 추가되어, 스캔 시 식별자 정의를 제어할 수 있게 되었습니다.
  - [`text/template`](/pkg/text/template/) 패키지의 불리언 함수 `eq`, `lt` 등이 일반화되어 부호 있는 정수와 부호 없는 정수의 비교를 허용함으로써 실제 사용이 간편해졌습니다. (이전에는 동일한 부호 여부를 가진 값들만 비교할 수 있었습니다.) 모든 음수는 모든 부호 없는 값보다 작은 것으로 비교됩니다.
  - `time` 패키지가 이제 마이크로초 지속 시간을 출력할 때 마이크로 접두사의 표준 기호인 마이크로 기호(U+00B5 'µ')를 사용합니다. [`ParseDuration`](/pkg/time/#ParseDuration)은 여전히 `us`를 허용하지만, 패키지에서 마이크로초를 더 이상 `us`로 출력하지 않습니다.
    \
    _업데이트_: `ParseDuration`을 사용하지 않으면서 지속 시간의 출력 형식에 의존하는 코드는 업데이트가 필요합니다.
