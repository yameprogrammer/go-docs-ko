## Go 1.2 소개 {#introduction}

2013년 4월 [Go version 1.1](/doc/go1.1.html)이 출시된 이후, 릴리스 프로세스를 더욱 효율적으로 만들기 위해 릴리스 일정이 단축되었습니다. 이번 릴리스인 Go version 1.2(약칭 Go 1.2)는 1.1 출시 후 약 6개월 만에 나왔으며, 이는 1.0 이후 1.1이 나오기까지 1년 넘게 걸렸던 것과 대조적입니다.

시간적 간격이 짧아진 만큼 1.2는 1.0에서 1.1로 넘어갈 때보다 변경 사항이 적지만, 더 나은 스케줄러와 하나의 새로운 언어 기능을 포함하여 여전히 몇 가지 중요한 발전이 있었습니다. 물론 Go 1.2는 [호환성 약속](/doc/go1compat.html)을 그대로 유지합니다. Go 1.1(또는 1.0)로 빌드된 대다수의 프로그램은 1.2로 옮겨도 아무런 수정 없이 실행될 것입니다. 다만, 언어의 일부 구석진 부분에 도입된 하나의 제한 사항으로 인해 이미 잘못 작성되었던 코드가 드러날 수 있습니다([nil 사용](#use_of_nil)에 관한 논의를 참조하십시오).

## 언어 변경 사항 {#language}

사양을 확정 짓기 위해 한 가지 코너 케이스가 명확해졌으며, 이에 따라 프로그램에 영향을 주는 변경 사항이 있습니다.
또한 새로운 언어 기능이 하나 추가되었습니다.

### nil의 사용 {#use_of_nil}

이제 언어 명세에서는 안전상의 이유로, `nil` 포인터의 특정 사용이 런타임 패닉(run-time panic)을 트리거하도록 보장합니다.
예를 들어, Go 1.0에서 다음과 같은 코드가 주어졌을 때

```go
type T struct {
	    X [1<<24]byte
	    Field int32
	}
```

```go
func main() {
	    var x *T
	    ...
	}
```

`nil` 포인터 `x`가 메모리에 잘못 접근하는 데 사용될 수 있습니다:
표현식 `x.Field`가 주소 `1<<24`의 메모리에 접근할 수 있습니다.
이러한 안전하지 않은 동작을 방지하기 위해, Go 1.2의 컴파일러는 여기에 예시된 경우뿐만 아니라 배열에 대한 `nil` 포인터, `nil` 인터페이스 값, `nil` 슬라이스 등 `nil` 포인터를 통한 모든 간접 참조가 패닉(panic)을 발생시키거나 올바르고 안전한 non-nil 값을 반환하도록 보장합니다.
요약하자면, 명시적으로든 암시적으로든 `nil` 주소의 평가를 요구하는 모든 표현식은 오류입니다.
구현체는 이 동작을 강제하기 위해 컴파일된 프로그램에 추가 테스트를 삽입할 수 있습니다.

더 자세한 내용은 [설계 문서](/s/go12nil)에서 확인하실 수 있습니다.

_업데이트_:
이전 동작에 의존했던 대부분의 코드는 잘못된 것이며 실행 시 실패하게 됩니다.
이러한 프로그램들은 수동으로 업데이트해야 합니다.

### 세 개의 인덱스를 사용하는 슬라이스 {#three_index}

Go 1.2부터는 기존의 배열이나 슬라이스에 슬라이싱 연산을 사용할 때, 길이(length)뿐만 아니라 용량(capacity)도 지정할 수 있는 기능이 추가되었습니다.
슬라이싱 연산은 이미 생성된 배열이나 슬라이스의 연속된 섹션을 기술함으로써 새로운 슬라이스를 생성합니다.

```go
var array [10]int
	slice := array[2:4]
```

슬라이스의 용량(capacity)은 재슬라이싱(reslicing) 후에도 슬라이스가 보유할 수 있는 요소의 최대 개수이며, 이는 기본 배열(underlying array)의 크기를 반영합니다.
이 예제에서 `slice` 변수의 용량은 8입니다.

Go 1.2에서는 슬라이싱 연산에서 길이뿐만 아니라 용량(capacity)도 지정할 수 있도록 새로운 구문을 추가했습니다.
두 번째
콜론은 용량 값을 도입하며, 이 값은 원본 슬라이스나 배열의 용량(시작 지점에 따라 조정됨)보다 작거나 같아야 합니다. 예를 들어,

`slice = array[2:4:7]`

슬라이스의 길이는 이전 예제와 동일하게 설정하지만, 용량(capacity)은 이제 5개의 요소(7-2)만 갖게 됩니다.
이 새로운 슬라이스 값으로는 원본 배열의 마지막 세 요소에 접근하는 것이 불가능합니다.

이 세 개의 인덱스 표기법에서, 첫 번째 인덱스가 누락된 경우(`[:i:j]`) 기본값은 0이 되지만 나머지 두 인덱스는 항상 명시적으로 지정해야 합니다.
향후 Go 릴리스에서 이러한 인덱스들에 대한 기본값이 도입될 가능성이 있습니다.

더 자세한 내용은 [설계 문서](/s/go12slice)에 나와 있습니다.

_업데이트_:
이 변경 사항은 하위 호환성을 유지하며 기존 프로그램에 영향을 주지 않습니다.

## 구현 및 도구의 변경 사항 {#impl}

### 스케줄러의 선점 (Pre-emption) {#preemption}

이전 릴리스에서는 무한 루프를 도는 goroutine이 동일한 스레드 상의 다른 goroutine들을 기아 상태(starve)로 만들 수 있었으며, 이는 `GOMAXPROCS`가 단 하나의 사용자 스레드만 제공할 때 심각한 문제가 되었습니다.

Go 1.2에서는 이 문제가 부분적으로 해결되었습니다. 이제 함수에 진입할 때 가끔씩 스케줄러가 호출됩니다.

이는 (인라이닝되지 않은) 함수 호출을 포함하는 모든 루프가 선점(pre-empted)될 수 있음을 의미하며, 이를 통해 동일한 스레드에서 다른 goroutine들이 실행될 수 있게 합니다.

### 스레드 수 제한 {#thread_limit}

Go 1.2에서는 일부 환경에서의 리소스 고갈 문제를 방지하기 위해, 단일 프로그램이 주소 공간 내에 가질 수 있는 총 스레드 수에 설정 가능한 제한(기본값 10,000개)을 도입했습니다.

고루틴(goroutine)은 스레드 위에 멀티플렉싱되므로, 이 제한이 고루틴의 수를 직접적으로 제한하는 것이 아니라 시스템 콜(system call)에서 동시에 블록(blocked)될 수 있는 스레드의 수만을 제한한다는 점에 유의하십시오.

실무적으로 이 제한치에 도달하는 일은 드뭅니다.

[`runtime/debug`](/pkg/runtime/debug/) 패키지에 새로 추가된 [`SetMaxThreads`](/pkg/runtime/debug/#SetMaxThreads) 함수는 스레드 수 제한을 제어합니다.

_업데이트_:
제한으로 인해 영향을 받는 함수는 거의 없겠지만, 프로그램이 제한에 도달하여 종료되는 경우 `SetMaxThreads`를 호출하여 더 높은 수치를 설정하도록 수정할 수 있습니다.
더 좋은 방법은 프로그램의 구조를 개선하여 필요한 스레드 수를 줄임으로써 커널 리소스 소비를 낮추는 것입니다.

### 스택 크기 {#stack_size}

Go 1.2에서는 고루틴(goroutine) 생성 시 스택의 최소 크기가 4KB에서 8KB로 상향 조정되었습니다.
많은 프로그램이 이전 크기로 인해 성능 문제를 겪었으며, 특히 성능이 중요한 구간에서 비용이 많이 드는 스택 세그먼트 스위칭(stack-segment switching)이 발생하는 경향이 있었습니다.
새로운 크기는 경험적 테스트를 통해 결정되었습니다.

반대편에서는, [`runtime/debug`](/pkg/runtime/debug) 패키지의 새로운 함수인 [`SetMaxStack`](/pkg/runtime/debug/#SetMaxStack)이 단일 고루틴 스택의 _최대_ 크기를 제어합니다.
기본값은 64비트 시스템에서 1GB, 32비트 시스템에서 250MB입니다.
Go 1.2 이전에는 제어되지 않는 재귀 호출로 인해 머신의 모든 메모리를 소모하기가 너무 쉬웠습니다.

_업데이트_:
최소 스택 크기가 증가함에 따라 고루틴(goroutine)이 많은 프로그램의 메모리 사용량이 늘어날 수 있습니다. 현재로서는 해결 방법이 없으나, 향후 릴리스 계획에 이 문제를 더 효과적으로 해결할 수 있는 새로운 스택 관리 기술이 포함되어 있습니다.

### Cgo와 C++ {#cgo_and_cpp}

[`cgo`](/cmd/cgo/) 명령은 이제 링크된 라이브러리 중 C++로 작성된 부분을 빌드하기 위해 C++ 컴파일러를 호출합니다. 자세한 내용은 [문서](/cmd/cgo/)를 참조하십시오.

### Godoc 및 vet이 go.tools 하위 저장소로 이동되었습니다 {#go_tools_godoc}

두 바이너리 모두 여전히 배포판에 포함되어 있지만, `godoc` 및 `vet` 명령어의 소스 코드는 [go.tools](https://code.google.com/p/go.tools) 서브리포지토리로 이동되었습니다.

또한, godoc 프로그램의 핵심 부분은 [library](https://code.google.com/p/go/source/browse/?repo=tools#hg%2Fgodoc)로 분리되었으며, 명령어 자체는 별도의 [directory](https://code.google.com/p/go/source/browse/?repo=tools#hg%2Fcmd%2Fgodoc)에 위치합니다. 이러한 변경을 통해 코드를 쉽게 업데이트할 수 있으며, 라이브러리와 명령어로 분리함으로써 로컬 사이트 및 다양한 배포 방식에 맞는 커스텀 바이너리를 더 쉽게 구축할 수 있게 되었습니다.

_업데이트_:
godoc과 vet은 라이브러리의 일부가 아니므로,
클라이언트 Go 코드는 이들의 소스에 의존하지 않으며 업데이트가 필요하지 않습니다.

[golang.org](/)에서 제공하는 바이너리 배포판에는 해당 바이너리들이 포함되어 있으므로, 이 배포판을 사용하는 사용자들은 영향을 받지 않습니다.

소스에서 빌드할 때, 사용자는 `go get`을 사용하여 godoc과 vet을 설치해야 합니다.
(바이너리는 `$GOPATH/bin`이 아니라 평소 설치되던 위치에 계속 설치됩니다.)

$ go get code.google.com/p/go.tools/cmd/godoc
	$ go get code.google.com/p/go.tools/cmd/vet

### gccgo의 상태 {#gccgo}

향후 GCC 4.9 릴리스에는 Go 1.2를 완전히 지원하는 gccgo가 포함될 것으로 예상됩니다.
현재(4.8.2) GCC 릴리스에서 gccgo는 Go 1.1.2를 구현합니다.

### gc 컴파일러 및 링커 변경 사항 {#gc_changes}

Go 1.2에는 gc 컴파일러 스위트의 작동 방식에 몇 가지 의미론적(semantic) 변경 사항이 있습니다.
대부분의 사용자는 이에 영향을 받지 않을 것입니다.

이제 링크하려는 라이브러리에 C++이 포함되어 있어도 [`cgo`](/cmd/cgo/) 명령이 작동합니다. 자세한 내용은 [`cgo`](/cmd/cgo/) 문서를 참조하십시오.

gc 컴파일러는 프로그램에 `package` 절이 없을 때 해당 파일이 `main` 패키지에 속해 있다고 가정함으로써 그 기원의 흔적을 보여주었습니다.
이제 과거의 흔적은 지워졌으며, `package` 절이 누락된 경우 에러로 처리됩니다.

ARM의 경우, 툴체인은 "외부 링킹(external linking)"을 지원합니다. 이는 gc 툴체인으로 공유 라이브러리를 빌드하고, 이것이 필요한 환경에 동적 링킹 지원을 제공하기 위한 단계입니다.

ARM 런타임의 `5a` 버전까지는 `R9` 및 `R10`을 사용하여 런타임 내부의 `m` (machine) 및 `g` (goroutine) 변수를 직접 참조할 수 있었습니다. 이제는 적절한 이름을 통해 이 변수들을 참조해야 합니다.

또한 ARM의 경우, `5l` 링커(sic)가 이제 `MOVBS` 및 `MOVHS` 명령어를 `MOVB` 및 `MOVH`의 동의어로 정의합니다. 이는 부호 있는(signed) 서브 워드 이동과 부호 없는(unsigned) 서브 워드 이동 간의 구분을 더 명확하게 하기 위함이며, 부호 없는 버전은 이미 `U` 접미사와 함께 존재했습니다.

### 테스트 커버리지 {#cover}

[`go test`](/pkg/go/)의 주요 새로운 기능 중 하나는 이제 테스트 커버리지 결과를 계산할 수 있으며, 별도로 설치되는 새로운 "go tool cover" 프로그램의 도움을 받아 이를 표시할 수 있다는 점입니다.

`cover` 도구는 [`go.tools`](https://code.google.com/p/go/source/checkout?repo=tools) 서브리포지토리의 일부입니다.
다음 명령어를 실행하여 설치할 수 있습니다.

$ go get code.google.com/p/go.tools/cmd/cover

`cover` 도구는 두 가지 기능을 수행합니다.
첫째, `go test`에 `-cover` 플래그가 지정되면, 패키지의 소스 코드를 재작성하고 인스트루멘테이션(instrumentation) 문을 삽입하기 위해 자동으로 실행됩니다.
그 후 테스트는 평소와 같이 컴파일 및 실행되며, 기본적인 커버리지 통계가 보고됩니다.

$ go test -cover fmt
	ok  	fmt	0.060s	coverage: 91.4% of statements
	$

둘째로, 더 상세한 보고서를 위해 `go test`에 다양한 플래그를 사용하면 커버리지 프로파일 파일을 생성할 수 있으며, 이후 `go tool cover`로 호출되는 `cover` 프로그램이 이 파일을 분석할 수 있습니다.

커버리지 통계를 생성하고 분석하는 방법에 대한 자세한 내용은 다음 명령어를 실행하여 확인할 수 있습니다.

$ go help testflag
	$ go tool cover -help

### go doc 명령어가 삭제되었습니다 {#go_doc}

`go doc` 명령어가 삭제되었습니다.
[`godoc`](/cmd/godoc/) 도구 자체가 삭제된 것이 아니라,
[`go`](/cmd/go/) 명령어에서 이를 래핑(wrapping)하던 기능만 삭제된 것임에 유의하십시오.
해당 기능은 단순히 패키지 경로를 통해 패키지 문서를 보여주는 역할만 했으며, 이는 godoc 자체가 이미 더 유연하게 제공하고 있는 기능입니다.
따라서 문서화 도구의 수를 줄이고, godoc의 구조 재편의 일환으로 향후 더 나은 옵션들을 권장하기 위해 삭제되었습니다.

_업데이트_: 여전히 실행의 정확한 기능이 필요하신 분들을 위해

`go doc` 명령은 Go 패키지와 그 구성 요소에 대한 문서를 출력하는 도구입니다.

### 기본 사용법

`go doc`을 인자 없이 실행하면 사용법이 출력됩니다.

```bash
$ go doc
```

특정 패키지의 문서를 보려면 패키지 이름을 인자로 전달하십시오.

```bash
$ go doc fmt
```

### 특정 심볼(Symbol) 조회

패키지 내의 특정 함수, 타입, 변수 또는 상수의 문서를 보려면 패키지 이름 뒤에 해당 심볼을 지정하십시오.

```bash
$ go doc fmt.Printf
```

### 현재 패키지 조회

인자를 생략하고 실행하면 현재 디렉토리의 패키지 문서를 출력합니다.

```bash
$ go doc
```

### 주요 옵션

*   `-all`: 패키지의 모든 문서를 출력합니다.
*   `-all`과 함께 심볼 지정: 해당 심볼과 관련된 모든 내용을 출력합니다.

### 예시

**`fmt` 패키지의 `Printf` 함수 문서 조회:**

```bash
$ go doc fmt.Printf
```

**현재 패키지의 모든 문서 조회:**

```bash
$ go doc -all
```

### 참고 사항

`go doc`은 소스 코드 내의 주석을 기반으로 문서를 생성합니다. 더 상세한 HTML 형태의 문서를 확인하고 싶다면 [pkg.go.dev](https://pkg.go.dev)를 방문하거나 `pkgsite`를 로컬에 설치하여 사용할 수 있습니다.

디렉토리 내에서, 이 동작은 다음을 실행하는 것과 동일합니다.

`$ godoc .`

### go 명령어의 변경 사항 {#gocmd}

[`go get`](/cmd/go/) 명령에 이제 `-t` 플래그가 추가되어, 패키지 자체의 의존성뿐만 아니라 해당 패키지에서 실행되는 테스트의 의존성까지 다운로드하도록 합니다. 기본적으로는 이전과 마찬가지로 테스트의 의존성은 다운로드되지 않습니다.

## 성능 {#performance}

표준 라이브러리에 다수의 중요한 성능 개선 사항이 포함되었습니다. 그 중 몇 가지를 소개합니다.

- [`compress/bzip2`](/pkg/compress/bzip2/)의
    압축 해제 속도가 약 30% 향상되었습니다.
  - [`crypto/des`](/pkg/crypto/des/) 패키지의
    속도가 약 5배 향상되었습니다.
  - [`encoding/json`](/pkg/encoding/json/) 패키지의
    인코딩 속도가 약 30% 향상되었습니다.
  - Windows 및 BSD 시스템의 네트워킹 성능이 약 30% 향상되었습니다. 이는 Go 1.1에서 Linux 및 OS X에 적용되었던 것과 유사하게, 런타임에 통합 네트워크 폴러(network poller)를 사용함으로써 가능해졌습니다.

## 표준 라이브러리 변경 사항 {#library}

### archive/tar 및 archive/zip 패키지 {#archive_tar_zip}

[`archive/tar`](/pkg/archive/tar/) 및 [`archive/zip`](/pkg/archive/zip/) 패키지의 시맨틱(semantics)에 기존 프로그램에서 오류를 일으킬 수 있는 변경 사항이 있었습니다. 문제는 두 패키지 모두 [`os.FileInfo`](/pkg/os/#FileInfo) 인터페이스의 구현체를 제공했는데, 이것이 해당 인터페이스의 사양을 준수하지 않았다는 점입니다. 특히, 이들의 `Name` 메서드는 항목의 전체 경로 이름을 반환했지만, 인터페이스 사양에서는 해당 메서드가 기본 이름(최종 경로 요소)만 반환하도록 요구하고 있습니다.

_업데이트_: 이 동작은 새로 구현되었으며 다소 모호했기 때문에, 기존의 잘못된 동작에 의존하는 코드가 없을 가능성이 있습니다. 만약 이에 의존하는 프로그램이 있다면, 이를 식별하여 수동으로 수정해야 합니다.

### 새로운 encoding 패키지 {#encoding}

[`encoding`](/pkg/encoding/)이라는 새로운 패키지가 추가되었습니다. 이 패키지는 [`encoding/xml`](/pkg/encoding/xml/), [`encoding/json`](/pkg/encoding/json/), [`encoding/binary`](/pkg/encoding/binary/)와 같은 패키지를 위한 커스텀 marshaler 및 unmarshaler를 구축하는 데 사용할 수 있는 표준 인코딩 인터페이스 집합을 정의합니다. 이러한 새로운 인터페이스들은 표준 라이브러리의 일부 구현 사항들을 정리하는 데 사용되었습니다.

새로운 인터페이스의 이름은
[`BinaryMarshaler`](/pkg/encoding/#BinaryMarshaler),
[`BinaryUnmarshaler`](/pkg/encoding/#BinaryUnmarshaler),
[`TextMarshaler`](/pkg/encoding/#TextMarshaler),
그리고
[`TextUnmarshaler`](/pkg/encoding/#TextUnmarshaler)입니다.
자세한 내용은 패키지 [문서](/pkg/encoding/)와 별도의 [설계 문서](/s/go12encoding)에서 확인하실 수 있습니다.

### fmt 패키지 {#fmt_indexed_arguments}

[`fmt`](/pkg/fmt/) 패키지의 [`Printf`](/pkg/fmt/#Printf)와 같은 형식화된 출력 루틴은 이제 형식 지정자 내에서 인덱싱 연산을 사용하여 출력할 데이터 항목에 임의의 순서로 접근할 수 있습니다.
형식화를 위해 인자 목록에서 인자를 가져와야 하는 모든 곳(형식화할 값으로 사용하거나 너비 또는 지정 정수로 사용되는 경우 모두 포함)에서, 새로운 선택적 인덱싱 표기법 `[`_n_`]`을 사용하면 대신 _n_번째 인자를 가져옵니다.
_n_의 값은 1부터 시작하는 인덱스(1-indexed)입니다.
이러한 인덱싱 연산 이후, 일반적인 처리 과정에서 다음에 가져올 인자는 _n_+1이 됩니다.

예를 들어, 일반적인 `Printf` 호출입니다.

`fmt.Sprintf("%c %c %c\n", 'a', 'b', 'c')`

`"a b c"` 문자열을 생성하겠지만, 다음과 같은 인덱싱 작업을 사용하면,

`fmt.Sprintf("%[3]c %[1]c %c\n", 'a', 'b', 'c')`는 인덱스 기반의 인자 참조를 사용하여 출력 순서를 지정하는 예제입니다.

### 동작 방식

`fmt` 패키지의 서식 지정자에서 `[n]` 구문을 사용하면, 전달된 인자 목록에서 `n`번째 인자를 명시적으로 선택할 수 있습니다. (인덱스는 1부터 시작합니다.)

주어진 코드 `fmt.Sprintf("%[3]c %[1]c %c\n", 'a', 'b', 'c')`를 분석하면 다음과 같습니다:

1.  **`%[3]c`**: 3번째 인자인 `'c'`를 문자로 출력합니다.
2.  **`%[1]c`**: 1번째 인자인 `'a'`를 문자로 출력합니다.
3.  **`%c`**: 인덱스가 명시되지 않았으므로, 이전 인자들의 순서에 따라 다음 인자인 2번째 인자 `'b'`를 문자로 출력합니다.

### 결과

이 코드가 실행되면 다음과 같은 문자열이 반환됩니다:
`"c a b\n"`

결과는 "`"c a b"`"입니다. `[3]` 인덱스는 세 번째 포맷팅 인자인 `'c'`에 접근하고, `[1]`은 첫 번째 인자인 `'a'`에 접근하며, 그다음 페치(fetch)는 그 뒤를 잇는 인자인 `'b'`에 접근합니다.

이 기능의 동기는 현지화를 위해 인자에 다른 순서로 접근할 수 있는 프로그래밍 가능한 포맷 구문을 제공하는 것이지만, 다음과 같은 다른 용도로도 사용됩니다:

`log.Printf("trace: value %v of type %[1]T\n", expensiveFunction(a.b[c]))`

_업데이트_: 형식 지정자(format specifications) 구문의 변경 사항은 엄격하게 하위 호환성을 유지하므로, 기존에 작동하는 프로그램에는 아무런 영향을 미치지 않습니다.

### text/template 및 html/template 패키지 {#text_template}

[`text/template`](/pkg/text/template/) 패키지는 Go 1.2에서 몇 가지 변경 사항이 있으며, 이 변경 사항들은 [`html/template`](/pkg/html/template/) 패키지에도 동일하게 반영되었습니다.

먼저, 기본 타입을 비교하기 위한 새로운 기본 함수들이 추가되었습니다.
함수 목록은 다음 표에 정리되어 있으며, 각 함수의 이름과 그에 대응하는 익숙한 비교 연산자를 보여줍니다.

<table cellpadding="0" summary="템플릿 비교 함수">
<tbody><tr>
<th width="50"></th><th width="100">이름</th> <th width="50">연산자</th>
</tr>
<tr>
<td></td><td><code>eq</code></td> <td><code>==</code></td>
</tr>
<tr>
<td></td><td><code>ne</code></td> <td><code>!=</code></td>
</tr>
<tr>
<td></td><td><code>lt</code></td> <td><code>&lt;</code></td>
</tr>
<tr>
<td></td><td><code>le</code></td> <td><code>&lt;=</code></td>
</tr>
<tr>
<td></td><td><code>gt</code></td> <td><code>&gt;</code></td>
</tr>
<tr>
<td></td><td><code>ge</code></td> <td><code>&gt;=</code></td>
</tr>
</tbody></table>

이 함수들은 대응하는 Go 연산자와 약간 다르게 동작합니다.
첫째, 이 함수들은 기본 타입(`bool`, `int`, `float64`, `string` 등)에 대해서만 동작합니다.
(Go에서는 일부 상황에서 배열과 구조체의 비교도 허용합니다.)
둘째, 값들이 동일한 종류의 값이기만 하면 비교할 수 있습니다. 예를 들어, 모든 부호 있는 정수 값은 다른 모든 부호 있는 정수 값과 비교할 수 있습니다. (Go는 `int8`과 `int16`의 비교를 허용하지 않습니다.)
마지막으로, `eq` 함수(만) 첫 번째 인자를 하나 이상의 후속 인자들과 비교하는 것을 허용합니다. 이 예제의 템플릿에서,

{{if eq .A 1 2 3}} equal {{else}} not equal {{end}}

`.A`가 1, 2 또는 3 중 *어느 하나라도* 해당하면 "equal"을 보고합니다.

두 번째 변경 사항은 문법에 작은 추가 사항이 생겨 "if else if" 체인을 더 쉽게 작성할 수 있게 되었다는 점입니다.
다음과 같이 작성하는 대신,

{{if eq .A 1}} X {{else}} {{if eq .A 2}} Y {{end}} {{end}}

두 번째 "if"를 "else" 안으로 접어 넣어 다음과 같이 "end"를 하나만 사용할 수 있습니다:

{{if eq .A 1}} X {{else if eq .A 2}} Y {{end}}

두 형태는 효과 면에서 동일하며, 차이점은 단지 구문에 있습니다.

_업데이트_: "else if" 변경 사항과 비교 함수 모두 기존 프로그램에 영향을 주지 않습니다. 함수 맵(function map)을 통해 `eq` 등의 함수를 이미 정의하여 사용 중인 프로그램은, 연결된 함수 맵이 새로운 기본 함수 정의보다 우선순위를 가지므로 영향을 받지 않습니다.

### 새로운 패키지 {#new_packages}

두 개의 새로운 패키지가 있습니다.

- [`encoding`](/pkg/encoding/) 패키지는 [위에서 설명되었습니다](#encoding).
  - [`image/color/palette`](/pkg/image/color/palette/) 패키지는 표준 색상 팔레트를 제공합니다.

### 라이브러리의 사소한 변경 사항 {#minor_library_changes}

다음 목록은 라이브러리의 여러 소규모 변경 사항(대부분 추가 사항)을 요약한 것입니다.
각 변경 사항에 대한 자세한 내용은 관련 패키지 문서를 참조하십시오.

- [`archive/zip`](/pkg/archive/zip/) 패키지에 아카이브 내 파일 데이터(압축되었을 수 있음)의 오프셋을 반환하는 [`DataOffset`](/pkg/archive/zip/#File.DataOffset) 접근자가 추가되었습니다.
  - [`bufio`](/pkg/bufio/) 패키지의 [`Reader`](/pkg/bufio/#Reader) 및 [`Writer`](/pkg/bufio/#Writer)에 [`Reset`](/pkg/bufio/#Reader.Reset) 메서드가 추가되었습니다. 이 메서드들을 사용하면 [`Readers`](/pkg/io/#Reader)와 [`Writers`](/pkg/io/#Writer)를 새로운 입력 및 출력 리더/라이터에서 재사용할 수 있어, 할당 오버헤드를 줄일 수 있습니다.
  - [`compress/bzip2`](/pkg/compress/bzip2/)에서 이제 연결된(concatenated) 아카이브를 압축 해제할 수 있습니다.
  - [`compress/flate`](/pkg/compress/flate/) 패키지의 [`Writer`](/pkg/compress/flate/#Writer)에 [`Reset`](/pkg/compress/flate/#Writer.Reset) 메서드가 추가되었습니다. 이를 통해 예를 들어 여러 압축 파일을 포함하는 아카이브를 생성할 때 할당을 줄일 수 있습니다.
  - [`compress/gzip`](/pkg/compress/gzip/) 패키지의 [`Writer`](/pkg/compress/gzip/#Writer) 타입에 재사용이 가능하도록 [`Reset`](/pkg/compress/gzip/#Writer.Reset)이 추가되었습니다.
  - [`compress/zlib`](/pkg/compress/zlib/) 패키지의 [`Writer`](/pkg/compress/zlib/#Writer) 타입에 재사용이 가능하도록 [`Reset`](/pkg/compress/zlib/#Writer.Reset)이 추가되었습니다.
  - [`container/heap`](/pkg/container/heap/) 패키지에 힙 내 항목의 위치를 더 효율적으로 업데이트할 수 있는 [`Fix`](/pkg/container/heap/#Fix) 메서드가 추가되었습니다.
  - [`container/list`](/pkg/container/list/) 패키지에 요소의 순서를 재배치하는 [`MoveBefore`](/pkg/container/list/#List.MoveBefore) 및 [`MoveAfter`](/pkg/container/list/#List.MoveAfter) 메서드가 추가되었습니다.
  - [`crypto/cipher`](/pkg/crypto/cipher/) 패키지에 AES 암호화와 거의 항상 함께 사용되는 새로운 GCM 모드(Galois Counter Mode)가 추가되었습니다.
  - [`crypto/md5`](/pkg/crypto/md5/) 패키지에 성능 저하 없이 해싱을 단순화하는 새로운 [`Sum`](/pkg/crypto/md5/#Sum) 함수가 추가되었습니다.
  - 마찬가지로, [`crypto/sha1`](/pkg/crypto/md5/) 패키지에도 새로운 [`Sum`](/pkg/crypto/sha1/#Sum) 함수가 추가되었습니다.
  - 또한, [`crypto/sha256`](/pkg/crypto/sha256/) 패키지에 [`Sum256`](/pkg/crypto/sha256/#Sum256) 및 [`Sum224`](/pkg/crypto/sha256/#Sum224) 함수가 추가되었습니다.
  - 마지막으로, [`crypto/sha512`](/pkg/crypto/sha512/) 패키지에 [`Sum512`](/pkg/crypto/sha512/#Sum512) 및 [`Sum384`](/pkg/crypto/sha512/#Sum384) 함수가 추가되었습니다.
  - [`crypto/x509`](/pkg/crypto/x509/) 패키지에 임의의 확장(extension)을 읽고 쓰는 기능이 추가되었습니다.
  - [`crypto/tls`](/pkg/crypto/tls/) 패키지에 TLS 1.1, 1.2 및 AES-GCM 지원이 추가되었습니다.
  - [`database/sql`](/pkg/database/sql/) 패키지의 [`DB`](/pkg/database/sql/#DB)에 데이터베이스에 대한 오픈 연결 수를 제한하는 [`SetMaxOpenConns`](/pkg/database/sql/#DB.SetMaxOpenConns) 메서드가 추가되었습니다.
  - [`encoding/csv`](/pkg/encoding/csv/) 패키지에서 이제 필드의 후행 쉼표(trailing commas)를 항상 허용합니다.
  - [`encoding/gob`](/pkg/encoding/gob/) 패키지는 이제 구조체의 채널 및 함수 필드가 내보내기 되지 않은(unexported) 필드처럼 처리됩니다(실제로 내보내기 된 필드라 하더라도 마찬가지입니다). 즉, 이를 완전히 무시합니다. 이전에는 이러한 필드가 있을 때 오류가 발생했으며, 이는 임베디드 구조체에 해당 필드가 추가될 경우 예상치 못한 호환성 문제를 일으킬 수 있었습니다. 또한 이 패키지는 이제 위에서 설명한 [`encoding`](/pkg/encoding/) 패키지의 제네릭 `BinaryMarshaler` 및 `BinaryUnmarshaler` 인터페이스를 지원합니다.
  - [`encoding/json`](/pkg/encoding/json/) 패키지는 이제 문자열을 출력할 때 앰퍼샌드(&)를 항상 "\u0026"으로 이스케이프 합니다. 또한 [`Marshal`](/pkg/encoding/json/#Marshal)에서 유효하지 않은 UTF-8을 허용하되 이를 수정합니다(이전에는 이러한 입력을 거부했습니다). 마지막으로, 위에서 설명한 [`encoding`](/pkg/encoding/) 패키지의 제네릭 인코딩 인터페이스를 지원합니다.
  - [`encoding/xml`](/pkg/encoding/xml/) 패키지는 이제 포인터에 저장된 속성(attribute)의 마샬링을 허용합니다. 또한 새로운 [`Marshaler`](/pkg/encoding/xml/#Marshaler), [`Unmarshaler`](/pkg/encoding/xml/#Unmarshaler), 그리고 관련 [`MarshalerAttr`](/pkg/encoding/xml/#MarshalerAttr) 및 [`UnmarshalerAttr`](/pkg/encoding/xml/#UnmarshalerAttr) 인터페이스를 통해 위에서 설명한 [`encoding`](/pkg/encoding/) 패키지의 제네릭 인코딩 인터페이스를 지원합니다. 또한 커스텀 인코더에서 사용할 수 있도록 [`Encoder`](/pkg/encoding/xml/#Encoder) 타입에 [`Flush`](/pkg/encoding/xml/#Encoder.Flush) 메서드를 추가했습니다. 사용 방법은 [`EncodeToken`](/pkg/encoding/xml/#Encoder.EncodeToken) 문서를 참조하십시오.
  - [`flag`](/pkg/flag/) 패키지에 플래그 값을 가져올 수 있도록 하는 [`Getter`](/pkg/flag/#Getter) 인터페이스가 추가되었습니다. Go 1 호환성 가이드라인으로 인해 이 메서드를 기존의 [`Value`](/pkg/flag/#Value) 인터페이스에 추가할 수 없었으나, 기존의 모든 표준 플래그 타입은 이를 구현하고 있습니다. 또한 커맨드라인 플래그를 보유하는 [`CommandLine`](/pkg/flag/#CommandLine) 플래그 세트를 이제 내보냅니다.
  - [`go/ast`](/pkg/go/ast/) 패키지의 [`SliceExpr`](/pkg/go/ast/#SliceExpr) 구조체에 새로운 불리언 필드 `Slice3`가 추가되었습니다. 이 필드는 세 개의 인덱스(두 개의 콜론)를 가진 슬라이스 표현식을 나타낼 때 true로 설정됩니다. 기본값은 false이며, 일반적인 두 개의 인덱스 형태를 나타냅니다.
  - [`go/build`](/pkg/go/build/) 패키지의 [`Package`](/pkg/go/build/#Package) 타입에 빌드 태그를 더 쉽게 처리할 수 있도록 `AllTags` 필드가 추가되었습니다.
  - [`image/draw`](/pkg/image/draw/) 패키지는 이제 표준 [`Draw`](/pkg/image/draw/#Draw) 메서드를 래핑하는 [`Drawer`](/pkg/image/draw/#Drawer) 인터페이스를 내보냅니다. Porter-Duff 연산자들은 이제 이 인터페이스를 구현하며, 결과적으로 연산을 명시적으로 제공하는 대신 그리기 연산자(draw operator)에 연산을 바인딩하게 됩니다. 목적지가 팔레트 이미지인 경우, [`Drawer`](/pkg/image/draw/#Drawer) 인터페이스의 새로운 [`FloydSteinberg`](/pkg/image/draw/#FloydSteinberg) 구현체는 Floyd-Steinberg 오차 확산 알고리즘을 사용하여 이미지를 그립니다. 이러한 처리에 적합한 팔레트를 생성하기 위해, 새로운 [`Quantizer`](/pkg/image/draw/#Quantizer) 인터페이스는 풀 컬러 이미지에서 팔레트를 선택하는 양자화 알고리즘의 구현을 나타냅니다. 라이브러리 내에 이 인터페이스의 구현체는 없습니다.
  - [`image/gif`](/pkg/image/gif/) 패키지에서 이제 새로운 [`Encode`](/pkg/image/gif/#Encode) 및 [`EncodeAll`](/pkg/image/gif/#EncodeAll) 함수를 사용하여 GIF 파일을 생성할 수 있습니다. 옵션 인수를 통해 사용할 이미지 [`Quantizer`](/pkg/image/draw/#Quantizer)를 지정할 수 있으며, `nil`인 경우 생성된 GIF는 새로운 [`image/color/palette`](/pkg/image/color/palette/) 패키지에 정의된 [`Plan9`](/pkg/image/color/palette/#Plan9) 컬러 맵(팔레트)을 사용합니다. 옵션에는 출력 이미지를 생성하는 데 사용할 [`Drawer`](/pkg/image/draw/#Drawer)도 지정할 수 있으며, `nil`인 경우 Floyd-Steinberg 오차 확산이 사용됩니다.
  - [`io`](/pkg/io/) 패키지의 [`Copy`](/pkg/io/#Copy) 메서드가 이제 인수의 우선순위를 다르게 처리합니다. 한 인수가 [`WriterTo`](/pkg/io/#WriterTo)를 구현하고 다른 인수가 [`ReaderFrom`](/pkg/io/#ReaderFrom)을 구현한 경우, [`Copy`](/pkg/io/#Copy)는 이제 [`WriterTo`](/pkg/io/#WriterTo)를 호출하여 작업을 수행함으로써 일반적으로 중간 버퍼링을 줄입니다.
  - [`net`](/pkg/net/) 패키지는 기본적으로 cgo를 필요로 합니다. 왜냐하면 호스트 운영체제가 일반적으로 네트워크 호출 설정을 중재해야 하기 때문입니다. 하지만 일부 시스템에서는 cgo 없이 네트워크를 사용할 수 있으며, 동적 링크를 피하기 위해 그렇게 하는 것이 유용할 수 있습니다. 새로운 빌드 태그 `netgo`(기본값은 off)를 사용하면 가능한 시스템에서 순수 Go로 `net` 패키지를 빌드할 수 있습니다.
  - [`net`](/pkg/net/) 패키지의 [`Dialer`](/pkg/net/#Dialer) 구조체에 [RFC 6555](https://tools.ietf.org/html/rfc6555)에 설명된 듀얼 IP 스택을 사용하는 TCP 연결 설정을 위한 새로운 `DualStack` 필드가 추가되었습니다.
  - [`net/http`](/pkg/net/http/) 패키지는 더 이상 [RFC 6265](https://tools.ietf.org/html/rfc6265)에 따라 올바르지 않은 쿠키를 전송하지 않습니다. 대신 오류를 로그에 기록하고 아무것도 보내지 않습니다. 또한, [`net/http`](/pkg/net/http/) 패키지의 [`ReadResponse`](/pkg/net/http/#ReadResponse) 함수는 이제 `*Request` 파라미터가 `nil`인 것을 허용하며, 이 경우 GET 요청으로 간주합니다. 마지막으로, 이제 HTTP 서버는 핸들러 코드에서 특별한 처리를 할 필요 없이 HEAD 요청을 투명하게 처리합니다. HEAD 요청을 처리하는 동안 [`Handler`](/pkg/net/http/#Handler)의 [`ResponseWriter`](/pkg/net/http/#ResponseWriter)에 대한 쓰기 작업은 [`Server`](/pkg/net/http/#Server)에 의해 흡수되며, 클라이언트는 HTTP 명세에 따라 빈 본문(body)을 받게 됩니다.
  - [`os/exec`](/pkg/os/exec/) 패키지의 [`Cmd.StdinPipe`](/pkg/os/exec/#Cmd.StdinPipe) 메서드는 `io.WriteCloser`를 반환하지만, 구체적인 구현이 `*os.File`에서 `*os.File`을 임베드하는 비내보내기 타입으로 변경되었습니다. 이제 반환된 값을 닫는(close) 것이 안전합니다. Go 1.2 이전에는 이 변경으로 해결된 불가피한 레이스 조건(race)이 있었습니다. `*os.File`의 메서드에 접근해야 하는 코드는 `wc.(interface{ Sync() error })`와 같은 인터페이스 타입 단언(type assertion)을 사용할 수 있습니다.
  - [`runtime`](/pkg/runtime/) 패키지는 [`SetFinalizer`](/pkg/runtime/#SetFinalizer)의 파이널라이저 함수 제약을 완화했습니다. 이제 실제 인수는 Go의 일반적인 함수 호출과 마찬가지로 함수의 형식 타입(formal type)에 할당 가능한 모든 타입이 될 수 있습니다.
  - [`sort`](/pkg/sort/) 패키지에 안정 정렬(stable sorting)을 구현하는 새로운 [`Stable`](/pkg/sort/#Stable) 함수가 추가되었습니다. 다만, 일반 정렬 알고리즘보다는 효율성이 떨어집니다.
  - [`strings`](/pkg/strings/) 패키지에 [`bytes`](/pkg/bytes/) 패키지와의 일관성을 위해 [`IndexByte`](/pkg/strings/#IndexByte) 함수가 추가되었습니다.
  - [`sync/atomic`](/pkg/sync/atomic/) 패키지에 인수를 포인터에 저장된 값과 원자적으로 교환하고 이전 값을 반환하는 새로운 스왑(swap) 함수 세트가 추가되었습니다. 해당 함수들은 [`SwapInt32`](/pkg/sync/atomic/#SwapInt32), [`SwapInt64`](/pkg/sync/atomic/#SwapInt64), [`SwapUint32`](/pkg/sync/atomic/#SwapUint32), [`SwapUint64`](/pkg/sync/atomic/#SwapUint64), [`SwapUintptr`](/pkg/sync/atomic/#SwapUintptr), 그리고 `unsafe.Pointer`를 교환하는 [`SwapPointer`](/pkg/sync/atomic/#SwapPointer)입니다.
  - [`syscall`](/pkg/syscall/) 패키지가 이제 Darwin(macOS)에 대해 [`Sendfile`](/pkg/syscall/#Sendfile)을 구현합니다.
  - [`testing`](/pkg/testing/) 패키지가 이제 [`TB`](/pkg/testing/#TB) 인터페이스를 내보냅니다. 이는 테스트와 벤치마크 간에 코드를 더 쉽게 공유할 수 있도록 [`T`](/pkg/testing/#T) 및 [`B`](/pkg/testing/#B) 타입의 공통 메서드들을 기록합니다. 또한, [`AllocsPerRun`](/pkg/testing/#AllocsPerRun) 함수는 이제 초기화로 인한 오차를 반올림하여 결과를 더 재현 가능하게 만들기 위해 반환 값을 정수로 양자화합니다(타입은 여전히 `float64`입니다).
  - [`text/template`](/pkg/text/template/) 패키지는 이제 "html"과 같은 "escape" 함수의 인수를 평가할 때 포인터 값을 자동으로 역참조(dereference)하여, 이러한 함수의 동작을 "printf"와 같은 다른 출력 함수와 일치시킵니다.
  - [`time`](/pkg/time/) 패키지의 [`Parse`](/pkg/time/#Parse) 함수와 [`Format`](/pkg/time/#Time.Format) 메서드는 이제 "1871-01-01T05:33:02+00:34:08"과 같은 역사적 날짜의 초 단위 시간대 오프셋을 처리합니다. 또한, 해당 루틴들의 형식 패턴 매칭이 더 엄격해졌습니다. "Jan" 및 "Mon"과 같은 표준 단어 뒤에는 이제 반드시 소문자가 아닌 문자가 와야 합니다.
  - [`unicode`](/pkg/unicode/) 패키지에 문자가 유니코드 카테고리의 멤버인지 확인하는 [`IsOneOf`](/pkg/unicode/#IsOneOf)의 더 사용하기 쉬운 버전인 [`In`](/pkg/unicode/#In)이 추가되었습니다.
