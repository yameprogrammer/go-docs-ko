## Go 1.1 소개 {#introduction}

2012년 3월에 출시된 [Go 버전 1](/doc/go1.html) (줄여서 Go 1 또는 Go 1.0)은 Go 언어와 라이브러리에 새로운 안정기(stability)를 가져왔습니다. 이러한 안정성은 전 세계적으로 성장하는 Go 사용자 커뮤니티와 시스템을 육성하는 데 도움이 되었습니다. 그 이후로 1.0.1, 1.0.2, 1.0.3과 같은 여러 "포인트" 릴리스가 발행되었습니다. 이러한 포인트 릴리스들은 알려진 버그를 수정했으며, 구현상으로 비임계적인(non-critical) 변경 사항은 포함하지 않았습니다.

이번 새 릴리스인 Go 1.1은 [호환성 약속](/doc/go1compat.html)을 유지하면서도, 몇 가지 중요한(물론 하위 호환성이 유지되는) 언어 변경 사항을 추가했으며, 방대한 양의 (마찬가지로 호환되는) 라이브러리 변경 사항을 포함하고 있습니다. 또한 컴파일러, 라이브러리 및 런타임 구현에 대한 대대적인 작업이 이루어졌습니다.

중점 사항은 성능입니다. 벤치마킹은 기껏해야 부정확한 과학이라 할 수 있지만, 당사의 많은 테스트 프로그램에서 상당하며 때로는 극적인 속도 향상을 확인했습니다. 많은 사용자분들의 프로그램 또한 Go 설치 버전을 업데이트하고 다시 컴파일하는 것만으로도 성능 향상을 경험하실 수 있을 것이라 믿습니다.

이 문서는 Go 1과 Go 1.1 사이의 변경 사항을 요약합니다.
Go 1.1에서 실행하기 위해 수정해야 할 코드는 거의 없으나, 이번 릴리스에서 몇 가지 드문 오류 사례가 발견되었으며 문제가 발생할 경우 해결이 필요합니다.
자세한 내용은 아래를 참조하십시오. 특히 [64-bit ints](#int) 및 [Unicode literals](#unicode_literals)에 관한 논의를 확인하시기 바랍니다.

## 언어 변경 사항 {#language}

[Go 호환성 문서](/doc/go1compat.html)에서는 Go 1 언어 명세에 따라 작성된 프로그램이 계속해서 작동할 것임을 보장하며, 이러한 약속은 계속 유지되고 있습니다.
다만, 명세를 더욱 확고히 하기 위해 일부 에러 케이스에 대한 세부 사항이 명확해졌습니다.
또한 몇 가지 새로운 언어 기능이 추가되었습니다.

### 정수 0 나누기 {#divzero}

Go 1에서 상수로 0을 나누는 정수 나눗셈은 런타임 패닉을 발생시켰습니다:

```go
func f(x int) int {
		return x/0
	}
```

Go 1.1에서 상수로 0을 나누는 정수 나눗셈은 유효한 프로그램이 아니므로, 컴파일 타임 오류가 발생합니다.

### Unicode 리터럴의 서로게이트(Surrogates) {#unicode_literals}

문자열(string)과 룬(rune) 리터럴의 정의가 수정되어, 유효한 Unicode 코드 포인트 집합에서 서로게이트 절반(surrogate halves)이 제외되었습니다.
자세한 내용은 [Unicode](#unicode) 섹션을 참조하십시오.

### 메서드 값 (Method values) {#method_values}

Go 1.1부터 [method values](/ref/spec#Method_values)를 구현합니다. method value는 특정 리시버 값에 바인딩된 함수입니다. 예를 들어, [`Writer`](/pkg/bufio/#Writer) 값 `w`가 있을 때, method value인 식 `w.Write`는 항상 `w`에 쓰는 함수가 됩니다. 이는 `w`를 캡처하는 함수 리터럴과 동일합니다.

```go
func (p []byte) (n int, err error) {
		return w.Write(p)
	}
```

메서드 값(Method values)은 주어진 타입의 메서드로부터 함수를 생성하는 메서드 표현식(method expressions)과는 다릅니다. 메서드 표현식 `(*bufio.Writer).Write`는 첫 번째 인자로 `(*bufio.Writer)` 타입의 리시버가 추가된 함수와 동일합니다:

```go
func (w *bufio.Writer, p []byte) (n int, err error) {
		return w.Write(p)
	}
```

_업데이트_: 기존 코드에 영향을 주지 않으며, 이번 변경 사항은 엄격하게 하위 호환성을 유지합니다.

### 반환 요구 사항 {#return}

Go 1.1 이전에는 값을 반환하는 함수가 함수의 끝에서 명시적인 `return`이나 `panic` 호출을 필요로 했습니다. 이는 프로그래머가 함수의 의미를 명확하게 표현하도록 하기 위한 간단한 방법이었습니다. 하지만 무한 `for` 루프만 포함된 함수와 같이 마지막 `return`이 분명히 불필요한 경우가 많이 존재합니다.

Go 1.1에서는 최종 `return` 문에 대한 규칙이 더 완화되었습니다.
함수가 실행하는 마지막 문장이 될 것이 보장되는 문장인
[_terminating statement_](/ref/spec#Terminating_statements)(종료 문)의 개념이 도입되었습니다.
예로는 조건이 없는 `for` 루프와 각 분기가 `return`으로 끝나는 `if-else` 문 등이 있습니다.
함수의 마지막 문장이 _구문적으로(syntactically)_ 종료 문임이 입증되면, 최종 `return` 문이 필요하지 않습니다.

이 규칙은 순수하게 구문론적(syntactic)이라는 점에 유의하십시오. 코드 내의 값에는 주의를 기울이지 않으며, 따라서 복잡한 분석이 필요하지 않습니다.

_업데이트_: 변경 사항은 하위 호환성을 유지하지만, 불필요한 "return" 문이나 `panic` 호출이 포함된 기존 코드는 수동으로 단순화할 수 있습니다.
이러한 코드는 `go vet`을 통해 식별할 수 있습니다.

## 구현 및 도구의 변경 사항 {#impl}

### gccgo의 상태 {#gccgo}

GCC 릴리스 일정은 Go 릴리스 일정과 일치하지 않으므로, `gccgo` 릴리스에서 어느 정도의 차이가 발생하는 것은 불가피합니다.
2013년 3월에 출시된 GCC 4.8.0 버전에는 Go 1.1에 근접한 버전의 `gccgo`가 포함되어 있습니다.
해당 라이브러리는 릴리스보다 약간 뒤쳐져 있으며, 가장 큰 차이점은 메서드 값(method values)이 구현되지 않았다는 점입니다.
2013년 7월경에 Go 1.1 구현을 완전히 제공하는 `gccgo`가 포함된 GCC 4.8.2가 출시될 것으로 예상합니다.

### 커맨드라인 플래그 파싱 {#gc_flag}

gc 툴체인에서 컴파일러와 링커는 이제 전통적인 Unix 플래그 파싱 방식에서 벗어나 Go `flag` 패키지와 동일한 명령줄 플래그 파싱 규칙을 사용합니다. 이는 툴을 직접 호출하는 스크립트에 영향을 줄 수 있습니다.

예를 들어,
`go tool 6c -Fw -Dfoo`는 이제
`go tool 6c -F -w -D foo`로 작성해야 합니다.

### 64비트 플랫폼에서의 int 크기 {#int}

이 언어는 `int` 타입과 `uint` 타입이 32비트일지 64비트일지를 구현체에서 선택할 수 있도록 허용합니다. 이전의 Go 구현체들은 모든 시스템에서 `int`와 `uint`를 32비트로 처리했습니다. 이제 gc와 gccgo 구현체 모두 AMD64/x86-64와 같은 64비트 플랫폼에서 `int`와 `uint`를 64비트로 처리합니다. 이를 통해 다른 여러 이점과 더불어, 64비트 플랫폼에서 20억 개 이상의 요소를 가진 슬라이스를 할당할 수 있게 되었습니다.

_업데이트_:
대부분의 프로그램은 이 변경 사항으로 인해 영향을 받지 않을 것입니다.
Go는 서로 다른 [numeric types](/ref/spec#Numeric_types) 간의 암시적 변환을 허용하지 않으므로,
이 변경으로 인해 컴파일이 중단되는 프로그램은 없을 것입니다.
하지만 `int`가 32비트라고 암시적으로 가정하는 프로그램은 동작이 변경될 수 있습니다.
예를 들어, 다음 코드는 64비트 시스템에서는 양수를, 32비트 시스템에서는 음수를 출력합니다:

```go
x := ^uint32(0) // x는 0xffffffff입니다.
	i := int(x)     // i는 32비트 시스템에서 -1, 64비트 시스템에서 0xffffffff가 됩니다.
	fmt.Println(i)
```

32비트 부호 확장(모든 시스템에서 `-1`을 반환)을 의도하는 이식 가능한 코드는 대신 다음과 같이 작성해야 합니다:

`i := int(int32(x))`

### 64비트 아키텍처에서의 힙 크기 {#heap}

64비트 아키텍처에서 최대 힙 크기가 몇 기가바이트에서 수십 기가바이트로 상당히 확대되었습니다.
(정확한 세부 사항은 시스템에 따라 다르며 변경될 수 있습니다.)

32비트 아키텍처에서 힙 크기는 변경되지 않았습니다.

_업데이트_:
이 변경 사항은 기존 프로그램이 더 큰 힙(heap)을 사용할 수 있게 하는 것 외에는 기존 프로그램에 아무런 영향을 미치지 않아야 합니다.

### Unicode {#unicode}

UTF-16에서 65535보다 큰 코드 포인트를 표현할 수 있도록,
Unicode는 _surrogate halves_(대리 쌍)를 정의합니다.
이는 오직 큰 값을 구성하는 용도로만, 그리고 오직 UTF-16에서만 사용되는 코드 포인트 범위입니다.
해당 surrogate 범위의 코드 포인트는 다른 어떤 목적으로도 사용할 수 없습니다.
Go 1.1에서 이 제약 사항은 컴파일러, 라이브러리 및 런타임에 의해 준수됩니다.
즉, surrogate half는 rune 값으로 사용되거나, UTF-8로 인코딩되거나,
단독으로 UTF-16으로 인코딩될 때 허용되지 않습니다.
예를 들어 rune을 UTF-8로 변환하는 과정에서 surrogate half가 발견되면,
이는 인코딩 오류로 처리되며 대체 rune인
[`utf8.RuneError`](/pkg/unicode/utf8/#RuneError),
U+FFFD를 반환합니다.

제공해주신 텍스트가 "This program,"라는 문구뿐입니다. 번역할 전체 내용을 제공해 주시면, 요청하신 지침에 따라 정밀하게 기술 번역을 진행해 드리겠습니다.

```go
import "fmt"
```

```go
func main() {
	    fmt.Printf("%+q\n", string(0xD800))
	}
```

Go 1.0에서는 `"\ud800"`이 출력되었으나, Go 1.1에서는 `"\ufffd"`가 출력됩니다.

이제 `rune` 및 `string` 상수에서 서로게이트-하프(Surrogate-half) 유니코드 값은 허용되지 않으므로, `'\ud800'` 및 `"\ud800"`와 같은 상수는 컴파일러에 의해 거부됩니다.
UTF-8로 인코딩된 바이트로 명시적으로 작성된 경우, `"\xed\xa0\x80"`와 같이 이러한 문자열을 여전히 생성할 수 있습니다.
하지만 range 루프에서와 같이 이러한 문자열을 `rune` 시퀀스로 디코딩하면 `utf8.RuneError` 값만 반환됩니다.

UTF-8로 인코딩된 유니코드 바이트 순서 표식(byte order mark) U+FEFF가 이제 Go 소스 파일의 첫 번째 문자로 허용됩니다.
바이트 순서가 필요 없는 UTF-8 인코딩에서 이 표식의 등장은 분명 불필요하지만, 일부 에디터는 UTF-8로 인코딩된 파일을 식별하기 위한 일종의 "매직 넘버"로서 이 표식을 추가합니다.

_업데이트_:
대부분의 프로그램은 서로게이트(surrogate) 변경으로 인한 영향을 받지 않습니다.
이전 동작에 의존하는 프로그램은 해당 문제를 피하도록 수정해야 합니다.
BOM(byte-order-mark) 변경은 엄격하게 하위 호환성을 유지합니다.

### Race detector {#race}

도구의 주요 추가 사항은 _race detector_(경쟁 검출기)로, 동일한 변수에 대해 동시에 접근하며 그중 최소 하나가 쓰기 작업일 때 발생하는 프로그램 버그를 찾는 방법입니다.
이 새로운 기능은 `go` 도구에 내장되어 있습니다.
현재로서는 64비트 x86 프로세서가 탑재된 Linux, Mac OS X 및 Windows 시스템에서만 사용할 수 있습니다.
이 기능을 활성화하려면 프로그램을 빌드하거나 테스트할 때 `-race` 플래그를 설정하십시오 (예: `go test -race`).
race detector에 대한 자세한 내용은 [별도의 문서](/doc/articles/race_detector.html)에 설명되어 있습니다.

### gc 어셈블러 {#gc_asm}

[`int`](#int)가 64비트로 변경되고
함수의 새로운 내부 [표현 방식](/s/go11func)이 도입됨에 따라,
gc 툴체인에서 스택의 함수 인자 배치가 변경되었습니다.
어셈블리로 작성된 함수들은 최소한 프레임 포인터 오프셋을 조정하기 위해
수정 작업이 필요합니다.

_업데이트_:
`go vet` 명령어가 이제 어셈블리로 구현된 함수가 구현하려는 Go 함수 프로토타입과 일치하는지 확인합니다.

### go 명령어 변경 사항 {#gocmd}

[`go`](/cmd/go/) 명령에는 새로운 Go 사용자의 경험을 개선하기 위한 여러 변경 사항이 적용되었습니다.

먼저, Go 코드를 컴파일, 테스트 또는 실행할 때 패키지를 찾을 수 없는 경우, `go` 명령어가 검색된 경로 목록을 포함하여 더 자세한 에러 메시지를 제공합니다.

$ go build foo/quxx
	패키지를 로드할 수 없습니다: 패키지 foo/quxx: 다음 경로 어디에서도 패키지 "foo/quxx"를 찾을 수 없습니다:
	        /home/you/go/src/pkg/foo/quxx ($GOROOT 기준)
	        /home/you/src/foo/quxx ($GOPATH 기준)

둘째로, `go get` 명령어는 더 이상 패키지 소스를 다운로드할 때 `$GOROOT`를 기본 목적지로 사용하는 것을 허용하지 않습니다. `go get` 명령어를 사용하려면 이제 [유효한 `$GOPATH`](/doc/code.html#GOPATH)가 필요합니다.

$ GOPATH= go get code.google.com/p/foo/quxx
	package code.google.com/p/foo/quxx: cannot download, $GOPATH not set. For more details see: go help gopath

마지막으로, 이전 변경 사항의 결과로 `$GOPATH`와 `$GOROOT`가 동일한 값으로 설정된 경우 `go get` 명령 또한 실패하게 됩니다.

$ GOPATH=$GOROOT go get code.google.com/p/foo/quxx
	warning: GOPATH set to GOROOT (/home/you/go) has no effect
	package code.google.com/p/foo/quxx: cannot download, $GOPATH must not be set to $GOROOT. For more details see: go help gopath

### go test 명령어의 변경 사항 {#gotest}

[`go test`](/cmd/go/#hdr-Test_packages)
명령어는 프로파일링이 활성화된 상태로 실행될 때, 프로파일 분석을 더 쉽게 만들기 위해 더 이상 바이너리를 삭제하지 않습니다.
구현상 `-c` 플래그가 자동으로 설정되므로, 실행 후에는

$ go test -cpuprofile cpuprof.out mypackage

`mypackage.test` 파일은 `go test`가 실행된 디렉토리에 남게 됩니다.

[`go test`](/cmd/go/#hdr-Test_packages) 명령어가 이제 고루틴(goroutine)이 어디에서 블록(block)되는지, 즉 채널 통신과 같은 이벤트 대기로 인해 어디에서 멈추는 경향이 있는지를 보고하는 프로파일링 정보를 생성할 수 있습니다. 이 정보는 `go test`의 `-blockprofile` 옵션으로 활성화할 수 있는 _블록 프로파일(blocking profile)_ 형태로 제공됩니다. 자세한 내용은 `go help test`를 실행하여 확인하십시오.

### go fix 명령의 변경 사항 {#gofix}

보통 `go fix`로 실행되는 [`fix`](/cmd/fix/) 명령은 더 이상 Go 1 이전의 코드를 Go 1 API를 사용하도록 업데이트하는 수정 사항을 적용하지 않습니다.

Go 1 이전의 코드를 Go 1.1로 업데이트하려면, 먼저 Go 1.0 툴체인을 사용하여 코드를 Go 1.0으로 변환하십시오.

### 빌드 제약 조건 (Build constraints) {#tags}

"`go1.1`" 태그가 기본 [빌드 제약 조건](/pkg/go/build/#hdr-Build_Constraints) 목록에 추가되었습니다.
이를 통해 패키지는 이전 버전의 Go와 호환성을 유지하면서도 Go 1.1의 새로운 기능들을 활용할 수 있습니다.

Go 1.1 이상 버전에서만 파일을 빌드하려면 다음 빌드 제약 조건을 추가하십시오:

// +build go1.1

Go 1.0.x 버전으로만 파일을 빌드하려면, 다음과 같은 반대 제약 조건을 사용하세요:

// +build !go1.1

### 추가 플랫폼 {#platforms}

Go 1.1 툴체인은 `freebsd/arm`, `netbsd/386`, `netbsd/amd64`, `netbsd/arm`, `openbsd/386` 및 `openbsd/amd64` 플랫폼에 대한 실험적 지원을 추가합니다.

`freebsd/arm` 또는 `netbsd/arm`을 사용하려면 ARMv6 이상의 프로세서가 필요합니다.

Go 1.1은 `linux/arm`에서 `cgo`에 대한 실험적 지원을 추가합니다.

### 교차 컴파일 {#crosscompile}

교차 컴파일(cross-compiling) 시, `go` 도구는 기본적으로 `cgo` 지원을 비활성화합니다.

`cgo`를 명시적으로 활성화하려면 `CGO_ENABLED=1`로 설정하십시오.

## 성능 {#performance}

Go 1.1 gc 도구 모음으로 컴파일된 코드의 성능은 대부분의 Go 프로그램에서 눈에 띄게 향상될 것입니다.
Go 1.0 대비 일반적인 개선 사항은 약 30%~40% 정도이며, 때로는 훨씬 더 많을 수도 있고, 가끔은 더 적거나 거의 없을 수도 있습니다.
도구와 라이브러리를 통해 이루어진 성능 중심의 작은 수정 사항이 너무 많아 모두 나열할 수는 없지만, 다음과 같은 주요 변경 사항은 주목할 만합니다:

- gc 컴파일러는 많은 경우에 더 나은 코드를 생성하며, 특히 32비트 Intel 아키텍처의 부동 소수점 연산에서 가장 두드러집니다.
  - gc 컴파일러는 [`append`](/pkg/builtin/#append) 및 인터페이스 변환과 같은 런타임의 일부 작업을 포함하여 더 많은 인라이닝(in-lining)을 수행합니다.
  - 메모리 사용량과 CPU 시간을 상당히 줄인 Go 맵(map)의 새로운 구현이 도입되었습니다.
  - 가비지 컬렉터가 더 병렬적으로 개선되어, 여러 CPU에서 실행되는 프로그램의 지연 시간(latency)을 줄일 수 있습니다.
  - 가비지 컬렉터가 더 정밀해졌습니다. 이는 약간의 CPU 시간을 소모하지만, 특히 32비트 아키텍처에서 힙(heap)의 크기를 크게 줄일 수 있습니다.
  - 런타임과 네트워크 라이브러리의 결합도가 높아짐에 따라, 네트워크 작업 시 필요한 컨텍스트 스위칭(context switch) 횟수가 줄어들었습니다.

## 표준 라이브러리 변경 사항 {#library}

### bufio.Scanner {#bufio_scanner}

[`bufio`](/pkg/bufio/) 패키지에서 텍스트 입력을 스캔하기 위한 다양한 루틴들인 [`ReadBytes`](/pkg/bufio/#Reader.ReadBytes), [`ReadString`](/pkg/bufio/#Reader.ReadString), 그리고 특히 [`ReadLine`](/pkg/bufio/#Reader.ReadLine)은 단순한 용도로 사용하기에는 불필요하게 복잡합니다. Go 1.1에서는 입력을 한 줄씩 또는 공백으로 구분된 단어들의 시퀀스로 읽는 것과 같은 간단한 작업을 더 쉽게 수행할 수 있도록 새로운 타입인 [`Scanner`](/pkg/bufio/#Scanner)가 추가되었습니다. `Scanner`는 병적으로 긴 줄과 같은 문제가 있는 입력에서 스캔을 종료함으로써 문제를 단순화하며, 각 줄에서 종료 문자를 제거한 라인 기반 입력이라는 간단한 기본 설정을 제공합니다. 다음은 입력을 한 줄씩 출력하는 코드입니다:

```go
scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
	    fmt.Println(scanner.Text()) // Println이 마지막 '\n'을 다시 추가합니다.
	}
	if err := scanner.Err(); err != nil {
	    fmt.Fprintln(os.Stderr, "reading standard input:", err)
	}
```

스캐닝 동작은 입력의 분할 방식을 제어하는 함수를 통해 조정할 수 있으며 ( [`SplitFunc`](/pkg/bufio/#SplitFunc) 문서 참조), 까다로운 문제나 에러 발생 후에도 계속 진행해야 하는 경우에는 여전히 이전 인터페이스가 필요할 수 있습니다.

### net {#net}

[`net`](/pkg/net/) 패키지의 프로토콜 전용 리졸버(resolver)들은 이전에 전달되는 네트워크 이름에 대해 관대했습니다.
문서에는 [`ResolveTCPAddr`](/pkg/net/#ResolveTCPAddr)에 사용할 수 있는 유효한 네트워크가 `"tcp"`, `"tcp4"`, `"tcp6"`뿐이라고 명확히 기재되어 있었지만, Go 1.0 구현체에서는 어떤 문자열이든 묵시적으로 허용했습니다.
Go 1.1 구현체에서는 네트워크가 해당 문자열 중 하나가 아니면 에러를 반환합니다.
이는 다른 프로토콜 전용 리졸버인 [`ResolveIPAddr`](/pkg/net/#ResolveIPAddr), [`ResolveUDPAddr`](/pkg/net/#ResolveUDPAddr), 그리고 [`ResolveUnixAddr`](/pkg/net/#ResolveUnixAddr)에도 동일하게 적용됩니다.

이전의 [`ListenUnixgram`](/pkg/net/#ListenUnixgram) 구현은 연결 엔드포인트의 표현으로 [`UDPConn`](/pkg/net/#UDPConn)을 반환했습니다. Go 1.1 구현에서는 대신 [`UnixConn`](/pkg/net/#UnixConn)을 반환하여, 해당 타입의 [`ReadFrom`](/pkg/net/#UnixConn.ReadFrom) 및 [`WriteTo`](/pkg/net/#UnixConn.WriteTo) 메서드를 통해 읽고 쓰기가 가능하도록 했습니다.

[`IPAddr`](/pkg/net/#IPAddr),
[`TCPAddr`](/pkg/net/#TCPAddr), 및
[`UDPAddr`](/pkg/net/#UDPAddr)
데이터 구조에 `Zone`이라는 새로운 string 필드가 추가되었습니다.
태그가 지정된 리터럴(`net.TCPAddr{IP: ip, Port: port}`) 대신
태그가 지정되지 않은 복합 리터럴(예: `net.TCPAddr{ip, port}`)을 사용하는 코드는
새로운 필드로 인해 작동하지 않게 됩니다.
Go 1 호환성 규칙은 이러한 변경을 허용합니다. 클라이언트 코드는 이러한 중단을 방지하기 위해 태그가 지정된 리터럴을 사용해야 합니다.

_업데이트_:
새로운 구조체 필드로 인해 발생한 오류를 수정하기 위해,
`go fix`는 이러한 타입에 태그를 추가하도록 코드를 재작성합니다.
보다 일반적으로, `go vet`은 필드 태그를 사용하도록 수정해야 할 복합 리터럴을 식별합니다.

### reflect {#reflect}

[`reflect`](/pkg/reflect/) 패키지에 몇 가지 중요한 추가 사항이 있습니다.

이제 `reflect` 패키지를 사용하여 "select" 문을 실행할 수 있습니다. 자세한 내용은 [`Select`](/pkg/reflect/#Select) 및 [`SelectCase`](/pkg/reflect/#SelectCase) 설명을 참조하십시오.

새로운 메서드인 [`Value.Convert`](/pkg/reflect/#Value.Convert) (또는 [`Type.ConvertibleTo`](/pkg/reflect/#Type))는 [`Value`](/pkg/reflect/#Value)에 대해 Go 변환 또는 타입 단언(type assertion) 작업을 실행하거나, 해당 작업의 가능 여부를 테스트하는 기능을 제공합니다.

새로운 함수 [`MakeFunc`](/pkg/reflect/#MakeFunc)는 기존의 [`Values`](/pkg/reflect/#Value)를 사용하여 함수를 더 쉽게 호출할 수 있도록 래퍼 함수를 생성하며, 인자들 간의 표준 Go 변환을 수행합니다. 예를 들어, 실제 `int` 값을 형식상의 `interface{}`로 전달하는 것과 같은 작업이 가능합니다.

마지막으로, 새로운 함수인
[`ChanOf`](/pkg/reflect/#ChanOf),
[`MapOf`](/pkg/reflect/#MapOf)
그리고
[`SliceOf`](/pkg/reflect/#SliceOf)
는 기존 타입으로부터 새로운
[`Types`](/pkg/reflect/#Type)
를 생성합니다. 예를 들어, `T`만 주어진 상태에서 `[]T` 타입을 생성할 때 사용할 수 있습니다.

### time {#time}

FreeBSD, Linux, NetBSD, OS X 및 OpenBSD에서 이전 버전의 [`time`](/pkg/time/) 패키지는 마이크로초(microsecond) 정밀도로 시간을 반환했습니다.
이러한 시스템에서의 Go 1.1 구현은 이제 나노초(nanosecond) 정밀도로 시간을 반환합니다.
마이크로초 정밀도의 외부 형식으로 기록하고 이를 다시 읽어 원래 값을 복구하려는 프로그램은 정밀도 손실의 영향을 받게 됩니다.
[`Time`](/pkg/time/#Time)에는 외부 저장소로 전달하기 전에 시간의 정밀도를 제거하는 데 사용할 수 있는 [`Round`](/pkg/time/#Time.Round)와 [`Truncate`](/pkg/time/#Time.Truncate)라는 두 가지 새로운 메서드가 추가되었습니다.

새로운 메서드 [`YearDay`](/pkg/time/#Time.YearDay)는 시간 값으로 지정된 연도의 1부터 시작하는 정수 일 수를 반환합니다.

[`Timer`](/pkg/time/#Timer)
타입에 지정된 기간 후에 타이머가 만료되도록 수정하는 새로운 메서드인
[`Reset`](/pkg/time/#Timer.Reset)
이 추가되었습니다.

마지막으로, 새로운 함수인 [`ParseInLocation`](/pkg/time/#ParseInLocation)은 기존의 [`Parse`](/pkg/time/#Parse)와 유사하지만, 파싱된 문자열에 포함된 시간대 정보를 무시하고 특정 위치(시간대)의 문맥에서 시간을 파싱합니다. 이 함수는 time API에서 흔히 발생하는 혼란의 원인을 해결합니다.

_업데이트_:
낮은 정밀도의 외부 형식을 사용하여 시간을 읽고 써야 하는 코드는 새로운 메서드를 사용하도록 수정해야 합니다.

### Exp 및 이전 서브트리가 go.exp 및 go.text 하위 저장소로 이동됨 {#exp_old}

바이너리 배포판에서 원할 때 더 쉽게 접근할 수 있도록, 바이너리 배포판에 포함되지 않는 `exp` 및 `old` 소스 서브트리가 `code.google.com/p/go.exp`에 있는 새로운 `go.exp` 서브리포지토리로 이동되었습니다. 예를 들어, `ssa` 패키지에 접근하려면 다음과 같이 실행하십시오.

$ go get code.google.com/p/go.exp/ssa

그리고 Go 소스 코드에서는,

`import "code.google.com/p/go.exp/ssa"`

기존의 `exp/norm` 패키지 또한 이동되었으나, 이는 Unicode API 및 기타 텍스트 관련 패키지들이 개발될 새로운 저장소인 `go.text`로 이동되었습니다.

### 새 패키지 {#new_packages}

세 개의 새로운 패키지가 있습니다.

- [`go/format`](/pkg/go/format/) 패키지는 프로그램이 [`go fmt`](/cmd/go/#hdr-Run_gofmt_on_package_sources) 명령의 포맷팅 기능을 편리하게 사용할 수 있는 방법을 제공합니다. 이 패키지에는 Go 파서 [`Node`](/pkg/go/ast/#Node)를 포맷팅하는 [`Node`](/pkg/go/format/#Node) 함수와, 임의의 Go 소스 코드를 [`go fmt`](/cmd/go/#hdr-Run_gofmt_on_package_sources) 명령이 제공하는 표준 포맷으로 다시 포맷팅하는 [`Source`](/pkg/go/format/#Source) 함수, 이렇게 두 가지 함수가 있습니다.
  - [`net/http/cookiejar`](/pkg/net/http/cookiejar/) 패키지는 HTTP 쿠키 관리를 위한 기본 기능을 제공합니다.
  - [`runtime/race`](/pkg/runtime/race/) 패키지는 데이터 레이스(data race) 감지를 위한 로우 레벨 기능을 제공합니다. 이 패키지는 레이스 디텍터(race detector) 내부용이며, 그 외에 사용자에게 노출되는 기능은 내보내지(export) 않습니다.

### 라이브러리의 소규모 변경 사항 {#minor_library_changes}

다음 목록은 라이브러리의 몇 가지 사소한 변경 사항(주로 추가 사항)을 요약한 것입니다.
각 변경 사항에 대한 자세한 내용은 관련 패키지 문서를 참조하십시오.

- [`bytes`](/pkg/bytes/) 패키지에 이름 그대로의 기능을 가진 [`TrimPrefix`](/pkg/bytes/#TrimPrefix) 및 [`TrimSuffix`](/pkg/bytes/#TrimSuffix)라는 두 개의 새로운 함수가 추가되었습니다. 또한, [`Buffer`](/pkg/bytes/#Buffer) 타입에 버퍼 내부의 메모리 할당을 일부 제어할 수 있는 새로운 메서드 [`Grow`](/pkg/bytes/#Buffer.Grow)가 추가되었습니다. 마지막으로, [`Reader`](/pkg/bytes/#Reader) 타입에 [`WriteTo`](/pkg/strings/#Reader.WriteTo) 메서드가 추가되어 이제 [`io.WriterTo`](/pkg/io/#WriterTo) 인터페이스를 구현합니다.
  - [`compress/gzip`](/pkg/compress/gzip/) 패키지의 [`Writer`](/pkg/compress/gzip/#Writer) 타입에 기본 `flate.Writer`를 플러시(flush)하는 새로운 [`Flush`](/pkg/compress/gzip/#Writer.Flush) 메서드가 추가되었습니다.
  - [`crypto/hmac`](/pkg/crypto/hmac/) 패키지에 두 개의 MAC을 비교하기 위한 새로운 함수 [`Equal`](/pkg/crypto/hmac/#Equal)이 추가되었습니다.
  - [`crypto/x509`](/pkg/crypto/x509/) 패키지에서 이제 PEM 블록을 지원하며 (예: [`DecryptPEMBlock`](/pkg/crypto/x509/#DecryptPEMBlock) 참조), 타원 곡선 개인 키를 파싱하기 위한 새로운 함수 [`ParseECPrivateKey`](/pkg/crypto/x509/#ParseECPrivateKey)가 추가되었습니다.
  - [`database/sql`](/pkg/database/sql/) 패키지의 [`DB`](/pkg/database/sql/#DB) 타입에 연결 상태를 테스트하는 새로운 [`Ping`](/pkg/database/sql/#DB.Ping) 메서드가 추가되었습니다.
  - [`database/sql/driver`](/pkg/database/sql/driver/) 패키지에 [`Conn`](/pkg/database/sql/driver/#Conn)이 성능 향상을 위해 구현할 수 있는 새로운 [`Queryer`](/pkg/database/sql/driver/#Queryer) 인터페이스가 추가되었습니다.
  - [`encoding/json`](/pkg/encoding/json/) 패키지의 [`Decoder`](/pkg/encoding/json/#Decoder)에 버퍼에 남아 있는 데이터에 접근할 수 있는 새로운 메서드 [`Buffered`](/pkg/encoding/json/#Decoder.Buffered)와, 값을 `float64`가 아닌 문자열인 새로운 타입 [`Number`](/pkg/encoding/json/#Number)로 언마샬링(unmarshal)하기 위한 새로운 메서드 [`UseNumber`](/pkg/encoding/json/#Decoder.UseNumber)가 추가되었습니다.
  - [`encoding/xml`](/pkg/encoding/xml/) 패키지에 이스케이프 처리된 XML 출력을 작성하는 새로운 함수 [`EscapeText`](/pkg/encoding/xml/#EscapeText)와, 들여쓰기 된 출력을 지정하기 위한 [`Encoder`](/pkg/encoding/xml/#Encoder)의 메서드 [`Indent`](/pkg/encoding/xml/#Encoder.Indent)가 추가되었습니다.
  - [`go/ast`](/pkg/go/ast/) 패키지에 새로운 타입 [`CommentMap`](/pkg/go/ast/#CommentMap)과 관련 메서드들이 추가되어 Go 프로그램에서 주석을 추출하고 처리하기가 더 쉬워졌습니다.
  - [`go/doc`](/pkg/go/doc/) 패키지에서 이제 파서가 코드 전반에 걸쳐 `TODO(joe)`와 같은 스타일화된 주석을 더 잘 추적하며, 이 정보는 [`godoc`](/cmd/godoc/) 명령어가 `-notes` 플래그 값에 따라 필터링하거나 표시할 수 있습니다.
  - [`html/template`](/pkg/html/template/) 패키지의 문서화되지 않았고 부분적으로만 구현되었던 "noescape" 기능이 제거되었습니다. 이 기능에 의존하는 프로그램은 작동하지 않을 것입니다.
  - [`image/jpeg`](/pkg/image/jpeg/) 패키지에서 이제 프로그레시브(progressive) JPEG 파일을 읽으며, 몇 가지 더 많은 서브샘플링 설정을 처리합니다.
  - [`io`](/pkg/io/) 패키지에서 한 번에 한 바이트씩 쓰는 공통 기능을 캡처하기 위해 [`io.ByteWriter`](/pkg/io/#ByteWriter) 인터페이스를 내보냅니다. 또한, `Read` 구현이 데이터를 전달하지 않고 루프를 돌고 있음을 나타내는 새로운 에러 [`ErrNoProgress`](/pkg/io/#ErrNoProgress)를 내보냅니다.
  - [`log/syslog`](/pkg/log/syslog/) 패키지에서 이제 OS별 로깅 기능에 대해 더 나은 지원을 제공합니다.
  - [`math/big`](/pkg/math/big/) 패키지의 [`Int`](/pkg/math/big/#Int) 타입에 JSON 표현으로 변환하거나 그 반대로 변환하기 위한 [`MarshalJSON`](/pkg/math/big/#Int.MarshalJSON) 및 [`UnmarshalJSON`](/pkg/math/big/#Int.UnmarshalJSON) 메서드가 추가되었습니다. 또한, [`Int`](/pkg/math/big/#Int)는 이제 [`Uint64`](/pkg/math/big/#Int.Uint64) 및 [`SetUint64`](/pkg/math/big/#Int.SetUint64)를 사용하여 `uint64`로 직접 변환할 수 있으며, [`Rat`](/pkg/math/big/#Rat)은 [`Float64`](/pkg/math/big/#Rat.Float64) 및 [`SetFloat64`](/pkg/math/big/#Rat.SetFloat64)를 사용하여 `float64`와 동일하게 수행할 수 있습니다.
  - [`mime/multipart`](/pkg/mime/multipart/) 패키지의 [`Writer`](/pkg/mime/multipart/#Writer)에 출력물을 패키징하는 데 사용되는 경계 구분자(boundary separator)를 정의하는 새로운 메서드 [`SetBoundary`](/pkg/mime/multipart/#Writer.SetBoundary)가 추가되었습니다. 또한 [`Reader`](/pkg/mime/multipart/#Reader)가 이제 `quoted-printable` 부분을 투명하게 디코딩하며, 이 과정에서 `Content-Transfer-Encoding` 헤더를 제거합니다.
  - [`net`](/pkg/net/) 패키지의 [`ListenUnixgram`](/pkg/net/#ListenUnixgram) 함수의 반환 타입이 변경되었습니다. 이제 [`UDPConn`](/pkg/net/#UDPConn)이 아닌 [`UnixConn`](/pkg/net/#UnixConn)을 반환하며, 이는 Go 1.0의 명백한 실수였습니다. 이 API 변경은 버그를 수정하는 것이므로 Go 1 호환성 규칙에 의해 허용됩니다.
  - [`net`](/pkg/net/) 패키지에 [`Dial`](/pkg/net/#Dialer.Dial)에 옵션을 제공하기 위한 새로운 타입 [`Dialer`](/pkg/net/#Dialer)가 추가되었습니다.
  - [`net`](/pkg/net/) 패키지에서 `fe80::1%lo0`와 같이 존 한정자(zone qualifiers)가 있는 링크-로컬 IPv6 주소에 대한 지원이 추가되었습니다. 주소 구조체 [`IPAddr`](/pkg/net/#IPAddr), [`UDPAddr`](/pkg/net/#UDPAddr), [`TCPAddr`](/pkg/net/#TCPAddr)는 새로운 필드에 존을 기록하며, [`Dial`](/pkg/net/#Dial), [`ResolveIPAddr`](/pkg/net/#ResolveIPAddr), [`ResolveUDPAddr`](/pkg/net/#ResolveUDPAddr), [`ResolveTCPAddr`](/pkg/net/#ResolveTCPAddr)와 같이 이러한 주소의 문자열 형태를 기대하는 함수들이 이제 존 한정 형태를 허용합니다.
  - [`net`](/pkg/net/) 패키지의 해석 함수 모음에 [`LookupNS`](/pkg/net/#LookupNS)가 추가되었습니다. `LookupNS`는 호스트 이름에 대한 [NS 레코드](/pkg/net/#NS)를 반환합니다.
  - [`net`](/pkg/net/) 패키지가 [`IPConn`](/pkg/net/#IPConn) ([`ReadMsgIP`](/pkg/net/#IPConn.ReadMsgIP) 및 [`WriteMsgIP`](/pkg/net/#IPConn.WriteMsgIP)) 및 [`UDPConn`](/pkg/net/#UDPConn) ([`ReadMsgUDP`](/pkg/net/#UDPConn.ReadMsgUDP) 및 [`WriteMsgUDP`](/pkg/net/#UDPConn.WriteMsgUDP))에 프로토콜별 패킷 읽기 및 쓰기 메서드를 추가했습니다. 이는 패킷과 관련된 대역 외(out-of-band) 데이터에 대한 접근을 제공하는 [`PacketConn`](/pkg/net/#PacketConn)의 `ReadFrom` 및 `WriteTo` 메서드의 특수 버전입니다.
  - [`net`](/pkg/net/) 패키지가 [`UnixConn`](/pkg/net/#UnixConn)에 연결의 절반을 닫을 수 있는 메서드 ([`CloseRead`](/pkg/net/#UnixConn.CloseRead) 및 [`CloseWrite`](/pkg/net/#UnixConn.CloseWrite))를 추가하여, 기존 [`TCPConn`](/pkg/net/#TCPConn)의 메서드와 일치하도록 했습니다.
  - [`net/http`](/pkg/net/http/) 패키지에 여러 가지 새로운 기능이 추가되었습니다. [`ParseTime`](/pkg/net/http/#ParseTime)은 몇 가지 일반적인 HTTP 시간 형식을 시도하여 시간 문자열을 파싱합니다. [`Request`](/pkg/net/http/#Request)의 [`PostFormValue`](/pkg/net/http/#Request.PostFormValue) 메서드는 [`FormValue`](/pkg/net/http/#Request.FormValue)와 비슷하지만 URL 파라미터는 무시합니다. [`CloseNotifier`](/pkg/net/http/#CloseNotifier) 인터페이스는 서버 핸들러가 클라이언트의 연결 끊김을 감지할 수 있는 메커니즘을 제공합니다. `ServeMux` 타입에는 이제 실행하지 않고 경로의 `Handler`에 접근할 수 있는 [`Handler`](/pkg/net/http/#ServeMux.Handler) 메서드가 있습니다. `Transport`는 이제 [`CancelRequest`](/pkg/net/http/#Transport.CancelRequest)를 통해 진행 중인 요청을 취소할 수 있습니다. 마지막으로, [`Response.Body`](/pkg/net/http/#Response)가 완전히 소비되기 전에 닫힌 경우 Transport가 TCP 연결을 더 적극적으로 닫습니다.
  - [`net/mail`](/pkg/net/mail/) 패키지에 RFC 5322 형식의 메일 주소를 [`Address`](/pkg/net/mail/#Address) 구조체로 파싱하기 위한 두 개의 새로운 함수 [`ParseAddress`](/pkg/net/mail/#ParseAddress) 및 [`ParseAddressList`](/pkg/net/mail/#ParseAddressList)가 추가되었습니다.
  - [`net/smtp`](/pkg/net/smtp/) 패키지의 [`Client`](/pkg/net/smtp/#Client) 타입에 서버로 `HELO` 또는 `EHLO` 메시지를 전송하는 새로운 메서드 [`Hello`](/pkg/net/smtp/#Client.Hello)가 추가되었습니다.
  - [`net/textproto`](/pkg/net/textproto/) 패키지에 앞뒤 공백을 ASCII로만 트리밍하는 두 개의 새로운 함수 [`TrimBytes`](/pkg/net/textproto/#TrimBytes) 및 [`TrimString`](/pkg/net/textproto/#TrimString)이 추가되었습니다.
  - 새로운 메서드 [`os.FileMode.IsRegular`](/pkg/os/#FileMode.IsRegular)를 통해 파일이 일반 파일인지 쉽게 확인할 수 있습니다.
  - [`os/signal`](/pkg/os/signal/) 패키지에 패키지가 채널로 더 이상 신호를 전달하지 않도록 중단하는 새로운 함수 [`Stop`](/pkg/os/signal/#Stop)이 추가되었습니다.
  - [`regexp`](/pkg/regexp/) 패키지는 이제 [`Regexp.Longest`](/pkg/regexp/#Regexp.Longest) 메서드를 통해 Unix 원형의 leftmost-longest 매칭을 지원하며, [`Regexp.Split`](/pkg/regexp/#Regexp.Split)은 정규 표현식으로 정의된 구분자를 기반으로 문자열을 조각으로 나눕니다.
  - [`runtime/debug`](/pkg/runtime/debug/) 패키지에 메모리 사용과 관련된 세 가지 새로운 함수가 추가되었습니다. [`FreeOSMemory`](/pkg/runtime/debug/#FreeOSMemory) 함수는 가비지 컬렉터를 실행한 후 사용하지 않는 메모리를 운영 체제에 반환하려고 시도합니다. [`ReadGCStats`](/pkg/runtime/debug/#ReadGCStats) 함수는 컬렉터에 대한 통계를 가져옵니다. [`SetGCPercent`](/pkg/runtime/debug/#SetGCPercent)는 컬렉터가 실행되는 빈도를 제어하는 프로그래밍 방식의 방법을 제공하며, 완전히 비활성화하는 것도 포함됩니다.
  - [`sort`](/pkg/sort/) 패키지에 새로운 함수 [`Reverse`](/pkg/sort/#Reverse)가 추가되었습니다. [`sort.Sort`](/pkg/sort/#Sort) 호출의 인자를 `Reverse` 호출로 감싸면 정렬 순서가 반전됩니다.
  - [`strings`](/pkg/strings/) 패키지에 이름 그대로의 기능을 가진 두 개의 새로운 함수 [`TrimPrefix`](/pkg/strings/#TrimPrefix) 및 [`TrimSuffix`](/pkg/strings/#TrimSuffix)가 추가되었으며, 새로운 메서드 [`Reader.WriteTo`](/pkg/strings/#Reader.WriteTo)가 추가되어 이제 [`Reader`](/pkg/strings/#Reader) 타입이 [`io.WriterTo`](/pkg/io/#WriterTo) 인터페이스를 구현합니다.
  - 다양한 BSD(Darwin 포함)에서 [`syscall`](/pkg/syscall/) 패키지의 [`Fchflags`](/pkg/syscall/#Fchflags) 함수 시그니처가 변경되었습니다. 이제 첫 번째 파라미터로 문자열 대신 int를 받습니다. 이 API 변경은 버그를 수정하는 것이므로 Go 1 호환성 규칙에 의해 허용됩니다.
  - [`syscall`](/pkg/syscall/) 패키지는 또한 지원되는 각 운영 체제의 상수와 시스템 호출을 더 많이 포함하도록 많은 업데이트를 받았습니다.
  - [`testing`](/pkg/testing/) 패키지는 이제 새로운 [`AllocsPerRun`](/pkg/testing/#AllocsPerRun) 함수를 사용하여 테스트 및 벤치마크에서 할당 통계 생성을 자동화합니다. 또한 [`testing.B`](/pkg/testing/#B)의 [`ReportAllocs`](/pkg/testing/#B.ReportAllocs) 메서드를 사용하면 호출하는 벤치마크에 대한 메모리 할당 통계 출력을 활성화할 수 있습니다. 또한 [`BenchmarkResult`](/pkg/testing/#BenchmarkResult)의 [`AllocsPerOp`](/pkg/testing/#BenchmarkResult.AllocsPerOp) 메서드를 도입했습니다. 더불어 `-v` 명령줄 플래그의 상태를 테스트하기 위한 새로운 [`Verbose`](/pkg/testing/#Verbose) 함수와, 부적절한 테스트를 건너뛰는 것을 단순화하기 위한 [`testing.B`](/pkg/testing/#B) 및 [`testing.T`](/pkg/testing/#T)의 새로운 [`Skip`](/pkg/testing/#B.Skip) 메서드가 추가되었습니다.
  - [`text/template`](/pkg/text/template/) 및 [`html/template`](/pkg/html/template/) 패키지에서, 이제 템플릿이 괄호를 사용하여 파이프라인의 요소를 그룹화할 수 있어 복잡한 파이프라인 구성을 단순화할 수 있습니다. 또한, 새로운 파서의 일부로 [`Node`](/pkg/text/template/parse/#Node) 인터페이스에 더 나은 에러 보고를 제공하기 위한 두 개의 새로운 메서드가 추가되었습니다. 비록 이것이 Go 1 호환성 규칙을 위반하지만, 이 인터페이스는 명시적으로 [`text/template`](/pkg/text/template/) 및 [`html/template`](/pkg/html/template/) 패키지에서만 사용되도록 의도되었으며 이를 보장하는 안전 장치가 있으므로 기존 코드에는 영향을 미치지 않을 것입니다.
  - [`unicode`](/pkg/unicode/) 패키지의 구현이 유니코드 버전 6.2.0으로 업데이트되었습니다.
  - [`unicode/utf8`](/pkg/unicode/utf8/) 패키지에서, 새로운 함수 [`ValidRune`](/pkg/unicode/utf8/#ValidRune)은 룬(rune)이 유효한 유니코드 코드 포인트인지 여부를 보고합니다. 유효하려면 룬이 범위 내에 있어야 하며 서로게이트 절반(surrogate half)이 아니어야 합니다.
