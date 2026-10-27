## Go 1.1 소개 {#introduction}

Go 버전 1 ([Go 버전 1](/doc/go1.html)) (Go 1 또는 Go 1.0)의 릴리스는 2012년 3월에 이루어졌으며, Go 언어 및 라이브러리에 새로운 안정성을 가져왔습니다.
이 안정성은 전 세계의 Go 사용자 및 시스템 커뮤니티의 성장에 기여했습니다.
그 이후로 1.0.1, 1.0.2, 1.0.3 등 여러 "버전" 릴리스가 발표되었습니다.
이 버전 릴리스는 알려진 버그를 수정했지만, 구현에 중요한 변경 사항은 포함하지 않았습니다.

이 새로운 버전, Go 1.1은 [호환성](/doc/go1compat.html)을 유지하면서, 몇 가지 중요한 (물론, 이전 버전과 호환되는) 언어 변경 사항, 그리고 (다시, 호환되는) 라이브러리 변경 사항을 추가하고, 컴파일러, 라이브러리 및 런타임 구현에 대한 주요 작업을 포함합니다.
주요 목표는 성능 향상입니다.
벤치마킹은 최적의 경우에도 정확한 과학이 아니지만, 저희의 테스트 프로그램에서 상당한, 때로는 극적인 속도 향상을 보았습니다.
저희는 많은 사용자의 프로그램이 Go 설치를 업데이트하고 다시 컴파일하는 것만으로도 개선을 보일 것이라고 믿습니다.

이 문서는 Go 1과 Go 1.1 간의 변경 사항을 요약합니다.
Go 1.1을 사용하려면 코드 수정이 거의 필요하지 않지만, 이 버전에서는 몇 가지 드문 오류가 발생할 수 있으며, 이러한 오류가 발생할 경우 해결해야 합니다.
자세한 내용은 아래에 설명되어 있습니다. 특히 [64비트 정수](#int) 및 [유니코드 리터럴](#unicode_literals)에 대한 설명 참조.

## 언어 변경 사항 {#language}

```
// Go package name
package mypackage

// Identifier
myVariable := "Hello, world!"

// URL
https://example.com
```

## Changes to the language {#language}

```
// Go package name
package mypackage

// Identifier
myVariable := "Hello, world!"

// URL
https://example.com
```

[Go 호환성 문서](/doc/go1compat.html)는
Go 1 언어 사양에 따라 작성된 프로그램이 계속 작동할 것이라고 약속하며,
이 약속은 유지됩니다.
사양을 더욱 명확하게 하기 위해, 일부 오류 사례에 대한 세부 사항이 명확하게 설명되었습니다.
또한 새로운 언어 기능이 추가되었습니다.

### 0으로의 정수 나눗셈 {#divzero}

Go 1에서 정수 나눗셈 연산이 상수 0으로 나누어질 때, 런타임 패닉이 발생했습니다:

```
func f(x int) int {
		return x/0
	}
```

Go 1.1 버전에서는 상수의 0으로의 정수 나눗셈은 유효한 프로그램이 아니므로, 컴파일 시간 오류가 발생합니다.

### 유니코드 리터럴 내의 대체 문자 {#unicode_literals}

문자열 및 래너 리터럴의 정의가 수정되어, 유효한 유니코드 코드 포인트 집합에서 서류 하프를 제외했습니다.
자세한 내용은 [유니코드](#unicode) 섹션을 참조하십시오.

### 메서드 값 {#method_values}

Go 1.1에서 다음과 같은 기능을 구현했습니다.
[메서드 값](/ref/spec#Method_values),
이는 특정 수신자 값에 바인딩된 함수입니다.
예를 들어, `Writer` 값 `w`가 주어졌을 때,
`w.Write`는 메서드 값으로, 항상 `w`에 쓰기를 수행하는 함수입니다. 이는 `w`를 래핑하는 함수 리터럴과 동일합니다:

```
func (p []byte) (n int, err error) {
		return w.Write(p)
	}
```

메서드 값은 메서드 표현식과 구별됩니다. 메서드 표현식은 주어진 유형의 메서드에서 함수를 생성합니다. 메서드 표현식 `(*bufio.Writer).Write`는 `(*bufio.Writer)` 유형의 수신자를 가진 추가적인 첫 번째 인수를 갖는 함수와 같습니다:

```markdown
```go
func (w *bufio.Writer, p []byte) (n int, err error) {
		return w.Write(p)
	}
```

_업데이트_: 기존 코드가 영향을 받지 않으며, 변경 사항은 엄격하게 이전 버전과 호환됩니다.

### 반환 요구사항 {#return}

```
// Go package name
```

Go 1.1 이전에는 값을 반환하는 함수는 함수 끝에서 명시적인 "return" 문을 사용하거나 `panic`을 호출해야 했습니다. 이는 프로그래머가 함수의 의미를 명확하게 나타내는 간단한 방법이었습니다. 그러나 최종 "return" 문이 명확히 불필요한 경우가 많습니다. 예를 들어 무한 "for" 루프만 있는 함수가 있습니다.

Go 1.1에서는 "return" 문에 대한 규칙이 더 관대합니다.
이는 "종결 문"([_terminating statement_](/ref/spec#Terminating_statements))이라는 개념을 도입하며, 이는 함수가 실행하는 마지막 문이라고 보장되는 문입니다.
예로는 조건이 없는 "for" 루프와 각 절이 "return"으로 끝나는 "if-else" 문이 있습니다.
함수의 마지막 문이 _구문적으로_ 종결 문이라고 증명될 수 있다면, 최종 "return" 문은 필요하지 않습니다.

참고: 이 규칙은 순전히 문법적인 규칙이며, 코드 내의 값에 대해서는 아무런 고려를 하지 않으므로 복잡한 분석이 필요하지 않습니다.

_업데이트_: 이 변경은 이전 버전과 호환되지만, 불필요한 "return" 문과 `panic` 호출이 포함된 기존 코드는 수동으로 단순화할 수 있습니다.
이러한 코드는 `go vet`를 사용하여 식별할 수 있습니다.

## 구현 및 도구에 대한 변경 사항 {#impl}

### gccgo의 상태 {#gccgo}

GCC의 릴리스 스케줄은 Go의 릴리스 스케줄과 일치하지 않으므로, `gccgo`의 릴리스에는 필연적으로 차이가 발생합니다.
GCC의 4.8.0 버전은 2013년 3월에 출시되었으며, 거의 Go 1.1 버전의 `gccgo`를 포함합니다.
라이브러리는 출시보다 약간 뒤쳐져 있지만, 가장 큰 차이점은 메서드 값 구현이 이루어지지 않았다는 것입니다.
2013년 7월쯤에, GCC의 4.8.2 버전이 완전한 Go 1.1 구현을 제공하는 `gccgo`를 포함하여 출시될 것으로 예상됩니다.

### 명령줄 플래그 파싱 {#gc_flag}

gc 도구 체인에서 컴파일러와 링커는 이제 Go 플래그 패키지의 동일한 명령줄 플래그 파싱 규칙을 사용하며, 이는 전통적인 유닉스 플래그 파싱 규칙에서 벗어난 것입니다. 이는 도구를 직접 호출하는 스크립트에 영향을 미칠 수 있습니다.
예를 들어,
`go tool 6c -Fw -Dfoo`는 이제 다음과 같이 작성해야 합니다.
`go tool 6c -F -w -D foo`.

### 64비트 플랫폼에서 `int`의 크기 {#int}

이 언어는 구현이 `int` 및 `uint` 유형이 32비트 또는 64비트인지 선택할 수 있도록 합니다. 이전 Go 구현에서는 모든 시스템에서 `int` 및 `uint`를 32비트로 설정했습니다. 현재 gc 및 gccgo 구현에서는 AMD64/x86-64와 같은 64비트 플랫폼에서 `int` 및 `uint`를 64비트로 설정합니다.
이것은 64비트 플랫폼에서 20억 개 이상의 요소로 구성된 슬라이스를 할당할 수 있도록 합니다.

_업데이트:_
대부분의 프로그램은 이 변경 사항에 영향을 받지 않습니다.
Go는 서로 다른 [숫자 유형](`/ref/spec#Numeric_types`) 간의 암시적 변환을 허용하지 않으므로, 이 변경 사항으로 인해 프로그램이 컴파일되지 않습니다.
그러나 `int`가 32비트만이라고 암시적으로 가정하는 프로그램의 동작이 변경될 수 있습니다.
예를 들어, 다음 코드는 64비트 시스템에서 양수를 출력하고 32비트 시스템에서 음수를 출력합니다:

```markdown
x := ^uint32(0)  // x는 0xffffffff
	i := int(x)     // i는 32비트 시스템에서는 -1, 64비트 시스템에서는 0xffffffff
	fmt.Println(i)
```

이동 가능한 코드는 32비트 부호 확장을 의도하지만, 결과는 모든 시스템에서 `-1`이 됩니다.

i := int(int32(x))

### 64비트 아키텍처에서의 힙 크기 {#heap}

64비트 아키텍처에서는 힙 크기가 크게 확장되었습니다.
수 GB에서 수십 GB로 증가했습니다.
(정확한 세부 사항은 시스템에 따라 다르며 변경될 수 있습니다.)

32비트 아키텍처에서는 힙 크기가 변경되지 않았습니다.

_업데이트_:
이 변경 사항은 기존 프로그램에 영향을 미치지 않아야 하며, 단순히 더 큰 힙 메모리 공간을 사용할 수 있도록 허용하는 것 외에는 아무런 영향도 미치지 않습니다.

### 유니코드 {#unicode}

다음과 같이, UTF-16에서 65535보다 큰 코드 포인트를 표현할 수 있도록,
유니코드는 _서로 다른 절반_을 정의합니다.
이것은 큰 값을 구성하는 데만 사용되는 코드 포인트의 범위이며, UTF-16에서만 사용됩니다.
이 서로 다른 절반 범위에 있는 코드 포인트는 다른 용도로는 유효하지 않습니다.
Go 1.1에서는 컴파일러, 라이브러리, 런타임이 이러한 제약을 준수합니다.
서로 다른 절반은 UTF-8로 인코딩하거나, 고립된 UTF-16으로 인코딩할 때, 또는
`rune` 값으로 사용할 수 없습니다.
예를 들어, `rune`에서 UTF-8로 변환할 때 발생하면,
이는 인코딩 오류로 처리되며, 대체 `rune`인 `utf8.RuneError` ([`utf8.RuneError`](/pkg/unicode/utf8/#RuneError))인 U+FFFD를 생성합니다.

이 프로그램,

```go
import "fmt"
```

```markdown
```go
package main

import "fmt"

func main() {
	fmt.Printf("%+q\n", string(0xD800))
}
```

출력 결과는 Go 1.0에서는 `"\ud800"`이지만, Go 1.1에서는 `"\ufffd"`입니다.

`Surrogate-half Unicode` 값은 이제 `rune` 및 `string` 상수에 불법입니다. 따라서 다음과 같은 상수는 컴파일러에서 거부됩니다.
`'\ud800'` 및 `"\ud800"`
명시적으로 UTF-8 인코딩된 바이트로 작성하면,
이러한 문자열은 여전히 생성할 수 있습니다 (예: `"\xed\xa0\x80"`).
그러나, 이러한 문자열을 런(rune)의 시퀀스로 디코딩하면, (예: 범위 루프에서) `utf8.RuneError`
값만 생성됩니다.

유니코드 바이트 순서 표시 U+FEFF는 UTF-8로 인코딩되었으며 이제 Go 소스 파일의 첫 번째 문자로 허용됩니다.
바이트 순서가 없는 UTF-8 인코딩에서 나타나는 것은 명백히 불필요하지만, 일부 편집기에서는 이 표시를 UTF-8로 인코딩된 파일의 "마법 숫자"로 사용하여 식별합니다.

_업데이트_:
대부분의 프로그램은 대체 문자 변경의 영향을 받지 않습니다.
기존 동작에 의존하는 프로그램은 이 문제를 해결하기 위해 수정해야 합니다.
바이트 순서 표시 변경은 엄격하게 이전 버전과 호환됩니다.

### 레이스 감지기 {#race}

이 도구에 추가된 주요 기능은 _레이스 검출기_입니다. 이는 동일한 변수에 대한 동시 액세스로 인해 발생하는 프로그램의 버그를 찾는 방법입니다. 여기서 적어도 하나의 액세스는 쓰기 작업입니다.
이 새로운 기능은 `go` 도구에 통합되어 있습니다.
현재는 64비트 x86 프로세서를 갖춘 Linux, Mac OS X, Windows 시스템에서만 사용할 수 있습니다.
이를 활성화하려면 프로그램을 빌드하거나 테스트할 때 `-race` 플래그를 설정하십시오 (예: `go test -race`).
레이스 검출기는 [별도의 문서](/doc/articles/race_detector.html)에서 설명되어 있습니다.

### GC 어셈블러 {#gc_asm}

`[int](`#int`)`이 64비트로 변경되고
새로운 내부 함수 표현 방식(`/s/go11func`)으로 인해, gc 툴체인에서 함수 인수의 스택 내 배열 방식이 변경되었습니다.
어셈블리로 작성된 함수는 최소한 프레임 포인터 오프셋을 조정하기 위해 수정해야 합니다.

_업데이트:_
`go vet` 명령이 이제 어셈블리에서 구현된 함수가 구현하는 Go 함수 프로토타입과 일치하는지 확인합니다.

### `go` 명령어의 변경 사항 {#gocmd}

[`go`](/cmd/go/) 명령어는 새로운 Go 사용자에게 더욱 편리한 경험을 제공하기 위해 여러 가지 변경 사항을 추가했습니다.

먼저, Go 코드를 컴파일, 테스트 또는 실행할 때, `go` 명령은 패키지를 찾을 수 없을 때, 검색된 경로 목록을 포함한 더 자세한 오류 메시지를 제공합니다.

$ go build foo/quxx
	패키지를 로드할 수 없습니다: 패키지 foo/quxx: 다음 위치 중 어느 곳에서도 "foo/quxx" 패키지를 찾을 수 없습니다:
	        /home/you/go/src/pkg/foo/quxx (GOROOT에서)
	        /home/you/src/foo/quxx (GOPATH에서)

둘째, `go get` 명령은 패키지 소스 다운로드 시 기본 대상으로 `$GOROOT`을 허용하지 않습니다.

`go get` 명령을 사용하려면 유효한 `$GOPATH`가 필요합니다. ([$GOPATH](https://golang.org/doc/code.html#GOPATH) 참조)

```markdown
$ GOPATH= go get code.google.com/p/foo/quxx
패키지 code.google.com/p/foo/quxx: 다운로드 불가, GOPATH 설정되지 않음. 자세한 내용은 다음을 참조하십시오: go help gopath
```

마지막으로, 이전 변경 사항의 결과로, `go get` 명령은 `$GOPATH` 및 `$GOROOT`이 동일한 값을 갖는 경우에도 실패합니다.

```markdown
```go
GOPATH=$GOROOT go get code.google.com/p/foo/quxx
	경고: GOPATH이 GOROOT (/home/you/go)으로 설정되어 효과가 없습니다.
	package code.google.com/p/foo/quxx: 다운로드할 수 없습니다. GOPATH는 GOROOT으로 설정되지 않아야 합니다. 자세한 내용은 다음을 참조하십시오: go help gopath
```

### `go test` 명령어의 변경 사항 {#gotest}

```go
package main

import (
	"fmt"
	"testing"
)

func main() {
	testing.Short() // 테스트를 빠르게 실행
	defer func() {
		fmt.Println("Goodbye, World!")
	}()

	fmt.Println("Hello, World!")
}
```

```go
func TestAdd(t *testing.T) {
	result := Add(2, 3)
	expected := 5
	if result != expected {
		t.Errorf("Add(2, 3) returned %d, expected %d", result, expected)
	}
}
```

```go
package main

import "testing"

func TestSomething(t *testing.T) {
    // 테스트 코드
}
```

명령 `go test`는 프로파일링이 활성화된 상태에서 실행될 때 더 이상 바이너리를 삭제하지 않습니다.
이렇게 함으로써 프로파일 분석을 더 쉽게 할 수 있습니다.
구현은 자동으로 `-c` 플래그를 설정하므로, 실행 후,

$ go test -cpuprofile cpuprof.out mypackage

파일 `mypackage.test`은 `go test` 명령이 실행된 디렉토리에 남겨질 것입니다.

명령 [`go test`](/cmd/go/#hdr-Test_packages)
이제 goroutine이 차단되는 위치에 대한 프로파일링 정보를 생성할 수 있습니다. 즉, 채널 통신과 같이 특정 이벤트에 대한 대기 중인 위치를 보고합니다.
이 정보는
_차단 프로파일_
로 표시되며, `go test` 명령의
`-blockprofile`
옵션을 통해 활성화됩니다. 자세한 내용은 `go help test`를 실행하십시오.

### `go fix` 명령어의 변경 사항 {#gofix}

명령 `fix` (`/cmd/fix/`)는 일반적으로 `go fix`로 실행되지만, Go 1 이전의 코드를 Go 1 API를 사용하는 코드로 업데이트하는 수정 사항을 더 이상 적용하지 않습니다.

Go 1 이전의 코드를 Go 1.1로 업데이트하려면, 먼저 Go 1.0 툴체인을 사용하여 코드를 Go 1.0으로 변환한 다음, Go 1.1로 업데이트해야 합니다.

### 빌드 제약 조건 {#tags}

"`go1.1`" 태그가 기본 설정 목록에 추가되었습니다.
[빌드 제약 조건](/pkg/go/build/#hdr-Build_Constraints).
이를 통해 패키지는 Go 1.1의 새로운 기능의 장점을 활용하면서 이전 버전의 Go와의 호환성을 유지할 수 있습니다.

1.1 이상 버전의 Go를 사용하여 파일만 빌드하려면, 다음 빌드 제약 조건을 추가하세요:

```
// +build go1.1
```

Go 1.0.x 버전만으로 파일을 빌드하려면, 다음과 같은 제약 조건을 사용합니다:

// +build !go1.1

### 추가 플랫폼 {#platforms}

Go 1.1 툴체인은 `freebsd/arm`, `netbsd/386`, `netbsd/amd64`, `netbsd/arm`, `openbsd/386` 및 `openbsd/amd64` 플랫폼에 대한 실험적인 지원을 추가합니다.

`freebsd/arm` 또는 `netbsd/arm`을 사용하려면 ARMv6 또는 그 이후의 프로세서가 필요합니다.

Go 1.1은 `linux/arm`에서 `cgo`에 대한 실험적인 지원을 추가합니다.

### 교차 컴파일 {#crosscompile}

크로스 컴파일 시, `go` 도구가 기본적으로 `cgo` 지원을 비활성화합니다.

`cgo`를 명시적으로 활성화하려면 `CGO_ENABLED=1`을 설정하십시오.

## 성능 {#performance}

Go 1.1 버전의 gc 도구 세트로 컴파일된 코드의 성능은 대부분의 Go 프로그램에서 뚜렷하게 개선될 것으로 예상됩니다.
Go 1.0에 비해 일반적인 개선 사항은 약 30%-40% 정도이며, 때로는 훨씬 더 높을 수 있지만, 때로는 그렇지 않거나 심지어 거의 없는 경우도 있습니다.
도구와 라이브러리를 통해 이루어진 수많은 작은 성능 관련 조정 사항들을 모두 나열하는 것은 불가능하지만, 다음 주요 변경 사항은 주목할 가치가 있습니다:

- GC 컴파일러는 많은 경우에 더 나은 코드를 생성하며, 특히 32비트 Intel 아키텍처에서 부동 소수점 연산에 효과적입니다.
  - GC 컴파일러는 [`append`](/pkg/builtin/#append) 및 일부 런타임 연산(인터페이스 변환 등)을 포함하여 더 많은 인라인 작업을 수행합니다.
  - Go 맵의 새로운 구현으로 메모리 사용량과 CPU 시간을 크게 줄일 수 있습니다.
  - 가비지 컬렉터가 병렬화되어 여러 CPU를 사용하는 프로그램의 지연 시간을 줄일 수 있습니다.
  - 가비지 컬렉터가 더욱 정밀해졌으며, 약간의 CPU 시간을 소비하지만 특히 32비트 아키텍처에서 힙 크기를 크게 줄일 수 있습니다.
  - 런타임 및 네트워크 라이브러리의 긴밀한 결합으로 네트워크 작업에서 컨텍스트 스위칭이 줄어듭니다.

## 표준 라이브러리의 변경 사항 {#library}

이 섹션에서는 표준 라이브러리의 변경 사항에 대한 정보를 제공합니다.

### bufio.Scanner {#bufio_scanner}

다양한 루틴인 [`bufio`](/pkg/bufio/) 패키지의
[`ReadBytes`](/pkg/bufio/#Reader.ReadBytes),
[`ReadString`](/pkg/bufio/#Reader.ReadString)
및 특히
[`ReadLine`](/pkg/bufio/#Reader.ReadLine)
는 단순한 목적으로 사용하기에 지나치게 복잡합니다.
Go 1.1에서는 새로운 타입인
[`Scanner`](/pkg/bufio/#Scanner)가 추가되어, 라인 단위 또는 공백으로 구분된 단어의 시퀀스로 입력을 읽는 등의 간단한 작업을 더 쉽게 수행할 수 있습니다.
이는 문제 해결을 위해, 비정상적으로 긴 라인과 같은 잘못된 입력을 처리하고, 기본적으로 라인 기반 입력을 제공하며, 각 라인에서 줄 바꿈 문자를 제거하는 방식으로 문제를 단순화합니다.
다음은 한 줄씩 입력을 재현하는 코드입니다:

```markdown
```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		fmt.Println(scanner.Text()) // Println은 최종 '\n'을 다시 추가
	}
	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "reading standard input:", err)
	}
}
```

입력 분할 동작은 함수를 통해 제어할 수 있습니다 (자세한 내용은 [`SplitFunc`](/pkg/bufio/#SplitFunc) 참조).
하지만 복잡한 문제나 오류 발생 시 계속 진행해야 하는 경우에는 이전 인터페이스가 여전히 필요할 수 있습니다.

### net

[`net`](/pkg/net/) 패키지에 있는 프로토콜별 리졸버는 이전에 전달된 네트워크 이름을 엄격하게 검사하지 않았습니다.
문서에는 명확하게 명시되어 있었지만,
`ResolveTCPAddr`](/pkg/net/#ResolveTCPAddr)에 유일하게 유효한 네트워크는 `"tcp"`, `"tcp4"`, 및 `"tcp6"` 뿐이라고,
Go 1.0 구현은 어떤 문자열이든 무심하게 허용했습니다.
Go 1.1 구현은 네트워크가 이 문자열 중 하나가 아닌 경우 오류를 반환합니다.
동일하게, 다른 프로토콜별 리졸버인 `ResolveIPAddr`](/pkg/net/#ResolveIPAddr), `ResolveUDPAddr`](/pkg/net/#ResolveUDPAddr), 및 `ResolveUnixAddr`](/pkg/net/#ResolveUnixAddr)도 동일합니다.

이전 구현인
[`ListenUnixgram`](/pkg/net/#ListenUnixgram)
은
[`UDPConn`](/pkg/net/#UDPConn)
을 연결 엔드포인트의 표현으로 반환했습니다.
Go 1.1 구현은 대신
[`UnixConn`](/pkg/net/#UnixConn)
을 반환하여
[`ReadFrom`](/pkg/net/#UnixConn.ReadFrom)
및
[`WriteTo`](/pkg/net/#UnixConn.WriteTo)
메서드를 사용하여 읽고 쓰는 기능을 제공합니다.

데이터 구조
[`IPAddr`](/pkg/net/#IPAddr),
[`TCPAddr`](/pkg/net/#TCPAddr), 및
[`UDPAddr`](/pkg/net/#UDPAddr)
에 새로운 문자열 필드인 `Zone`가 추가되었습니다.
태깅되지 않은 복합 리터럴(예: `net.TCPAddr{ip, port}`)을 사용하는 대신
태깅된 리터럴(`net.TCPAddr{IP: ip, Port: port}`)을 사용하는 코드가
새로운 필드 때문에 오류를 발생시킬 수 있습니다.
Go 1 호환성 규칙은 이러한 변경을 허용합니다. 클라이언트 코드는 이러한 오류를 방지하기 위해
태깅된 리터럴을 사용해야 합니다.

_업데이트_:
새로운 구조체 필드 때문에 발생하는 문제를 수정하려면,
`go fix`는 이러한 유형에 대한 태그를 추가하기 위해 코드를 다시 작성합니다.
더 일반적으로, `go vet`는 수정하여 필드 태그를 사용하는 것이 적절한 복합 리터럴을 식별합니다.

### reflect

[`reflect`](/pkg/reflect/) 패키지는 여러 중요한 기능을 추가했습니다.

이제 `reflect` 패키지를 사용하여 "select" 문을 실행할 수 있습니다. 자세한 내용은
[`Select`](/pkg/reflect/#Select)
및
[`SelectCase`](/pkg/reflect/#SelectCase)
를 참조하십시오.

새로운 방법
[`Value.Convert`](/pkg/reflect/#Value.Convert)
(또는
[`Type.ConvertibleTo`](/pkg/reflect/#Type))
은
[`Value`](/pkg/reflect/#Value)
(또는 해당 가능성을 테스트하는)에 Go 변환 또는 타입 어설션 작업을 수행하는 기능을 제공합니다.

새로운 함수
[`MakeFunc`](/pkg/reflect/#MakeFunc)
은 기존
[`Values`](/pkg/reflect/#Value)를 사용하여 함수를 호출하는 것을 더 쉽게 만드는 래퍼 함수를 생성합니다.
인수 간의 표준 Go 변환을 수행하여, 예를 들어 실제 `int`를 형식적인 `interface{}`에 전달하는 것을 가능하게 합니다.

마지막으로, 새로운 함수
[`ChanOf`](/pkg/reflect/#ChanOf),
[`MapOf`](/pkg/reflect/#MapOf)
및
[`SliceOf`](/pkg/reflect/#SliceOf)
은 기존의 타입으로부터 새로운
[`Types`](/pkg/reflect/#Type)를 생성합니다. 예를 들어, 단지 `T`만 주어졌을 때 `[]T`와 같은 타입을 생성할 수 있습니다.

### 시간 {#time}

FreeBSD, Linux, NetBSD, OS X 및 OpenBSD에서는 이전 버전의
[`time`](/pkg/time/) 패키지가 마이크로초 단위의 정밀도로 시간을 반환했습니다.
이 시스템에서 Go 1.1 구현은 나노초 단위의 정밀도로 시간을 반환합니다.
마이크로초 정밀도로 외부 형식으로 작성하고 다시 읽어 원본 값을 복구할 것으로 예상하는 프로그램은 정밀도 손실로 인해 영향을 받습니다.
[`Time`](/pkg/time/#Time),
[`Round`](/pkg/time/#Time.Round) 및
[`Truncate`](/pkg/time/#Time.Truncate)라는 두 가지 새로운 방법을 사용하여 외부 저장소로 전달하기 전에 시간의 정밀도를 제거할 수 있습니다.

새로운 방법
[`YearDay`](/pkg/time/#Time.YearDay)
은 주어진 시간 값에 의해 지정된 연의 일(1부터 시작하는 정수)을 반환합니다.

`[`Timer`](/pkg/time/#Timer)
형에는 새로운 메서드
[`Reset`](/pkg/time/#Timer.Reset)
이 있으며, 이 메서드는 지정된 기간 후에 타이머를 만료하도록 수정합니다.

마지막으로, 새로운 함수
[`ParseInLocation`](/pkg/time/#ParseInLocation)
은 기존의
[`Parse`](/pkg/time/#Parse)
과 유사하지만, 파싱된 문자열에 시간대 정보를 무시하고, 시간대를 고려하여 시간을 파싱합니다.
이 함수는 시간 API에서 흔하게 발생하는 혼란의 원인을 해결합니다.

_업데이트_:
외부 형식으로 시간을 읽고 쓰기 위해 더 낮은 정밀도를 사용하는 코드는 새 방법을 사용하여 수정해야 합니다.

### Exp 및 이전 서브트리 이동: go.exp 및 go.text 서브리포지토리로 이동 {#exp_old}

다음과 같이, 필요한 경우 이진 배포판에서 쉽게 접근할 수 있도록, `exp` 및 `old` 소스 서브트리(이진 배포판에 포함되지 않은)가 `code.google.com/p/go.exp`의 새 `go.exp` 서브리포지토리로 이동되었습니다. 예를 들어, `ssa` 패키지에 접근하려면 다음을 실행합니다.

$ go get code.google.com/p/go.exp/ssa

그리고 Go 소스에서,

```
import "code.google.com/p/go.exp/ssa"
```

오래된 패키지 `exp/norm`도 이동되었지만, 이제 `go.text`라는 새 저장소로 이동되었습니다. 여기서 유니코드 API 및 기타 텍스트 관련 패키지가 개발될 예정입니다.

### 새로운 패키지 {#new_packages}

새로운 패키지가 3개 있습니다.

- [`go/format`](/pkg/go/format/) 패키지는
    프로그램이 [`go fmt`](/cmd/go/#hdr-Run_gofmt_on_package_sources) 명령의 포맷팅 기능을 편리하게 사용할 수 있도록 합니다.
    두 가지 함수를 제공합니다.
    `Node` (패킷을 포맷하는 [`Node`](/pkg/go/format/#Node)) 및
    `Source` (어떤 Go 소스 코드를 [`go fmt`](/cmd/go/#hdr-Run_gofmt_on_package_sources) 명령에서 제공하는 표준 형식으로 재포맷하는 [`Source`](/pkg/go/format/#Source))
  - [`net/http/cookiejar`](/pkg/net/http/cookiejar/) 패키지는 HTTP 쿠키 관리를 위한 기본적인 기능을 제공합니다.
  - [`runtime/race`](/pkg/runtime/race/) 패키지는 데이터 레이스 감지를 위한 저수준 기능을 제공합니다.
    이는 레이스 감지기에 내부적으로 존재하며, 사용자가 직접 사용할 수 있는 기능을 제공하지 않습니다.

### 라이브러리의 미미한 변경 사항 {#minor_library_changes}

다음 목록은 라이브러리의 여러 개의 미미한 변경 사항을 요약합니다. 대부분이 추가 사항입니다.
각 변경 사항에 대한 자세한 내용은 관련 패키지 문서를 참조하십시오.

- `bytes` 패키지는 두 개의 새로운 함수,
    `TrimPrefix` 및
    `TrimSuffix`를 도입했습니다.
    또한 `Buffer` 타입은 `Grow`라는 새로운 메서드를 도입했으며, 이 메서드는 버퍼 내의 메모리 할당을 제어할 수 있도록 합니다.
    마지막으로 `Reader` 타입은 이제 `WriteTo` 메서드를 갖게 되었으며, 이를 통해 `io.WriterTo` 인터페이스를 구현합니다.
  - `compress/gzip` 패키지는 `Writer` 타입의 새로운 `Flush` 메서드를 도입했으며, 이를 통해 `flate.Writer`를 플러시합니다.
  - `crypto/hmac` 패키지는 두 개의 새로운 함수,
    `Equal`을 도입했습니다. 이 함수는 두 개의 MAC을 비교합니다.
  - `crypto/x509` 패키지는 PEM 블록을 지원하도록 업데이트되었으며, 새로운 함수 `ParseECPrivateKey`를 도입하여 타원 곡선 개인 키를 파싱합니다.
  - `database/sql` 패키지는 `DB` 타입의 새로운 `Ping` 메서드를 도입했으며, 이 메서드는 연결의 상태를 테스트합니다.
  - `database/sql/driver` 패키지는 `Conn` 타입에 구현할 수 있는 새로운 `Queryer` 인터페이스를 도입했으며, 이를 통해 성능을 향상시킬 수 있습니다.
  - `encoding/json` 패키스의 `Decoder`는 `Buffered`라는 새로운 메서드를 도입하여 버퍼에 남아 있는 데이터를 접근할 수 있게 되었으며, 또한 새로운 `UseNumber` 메서드를 도입하여 `Number` 타입으로 값을 언마샬링할 수 있게 되었고, `float64` 대신 문자열을 사용합니다.
  - `encoding/xml` 패키지는 새로운 함수 `EscapeText`를 도입했으며, 이 함수는 XML 출력을 이스케이프합니다. 또한 `Encoder` 타입에 `Indent`라는 메서드를 추가하여 들여쓰기된 출력을 지정할 수 있습니다.
  - `go/ast` 패키지에서는 새로운 타입 `CommentMap`과 관련된 메서드를 도입하여 Go 프로그램에서 주석을 추출하고 처리하는 것을 더 쉽게 만들었습니다.
  - `go/doc` 패키지에서는 새로운 코드 내의 스타일 지정된 주석, 예를 들어 `TODO(joe)`를 더 잘 추적하도록 파서가 업데이트되었습니다. 이 정보는 `godoc` 명령어가 `-notes` 플래그의 값을 기반으로 필터링하거나 표시할 수 있습니다.
  - `html/template` 패키지의 문서화되지 않은 "noescape" 기능이 제거되었습니다. 이 기능에 의존하는 프로그램이 중단될 수 있습니다.
  - `image/jpeg` 패키지는 이제 프로그레시브 JPEG 파일을 읽고 더 많은 서브샘플링 구성을 처리합니다.
  - `io` 패키지는 `io.ByteWriter` 인터페이스를 내보냅니다. 이를 통해 데이터를 바이트 단위로 쓰는 것이 일반적인 기능을 제공합니다. 또한 `Read` 구현이 데이터를 제공하지 않고 반복되는 경우에 사용되는 새로운 오류, `ErrNoProgress`를 도입했습니다.
  - `log/syslog` 패키지는 이제 OS별 로깅 기능을 더 잘 지원합니다.
  - `math/big` 패키지의 `Int` 타입은 이제 JSON 표현으로 변환하고 JSON 표현에서 변환할 수 있는 `MarshalJSON` 및 `UnmarshalJSON` 메서드를 도입했습니다. 또한 `Int` 타입은 `uint64` 및 `SetUint64`를 사용하여 `uint64`로 직접 변환할 수 있으며, `Rat` 타입은 `float64` 및 `SetFloat64`를 사용하여 `float64`로 변환할 수 있습니다.
  - `mime/multipart` 패키지는 `Writer` 타입에 새로운 메서드 `SetBoundary`를 도입했습니다. 이 메서드는 출력 패키징에 사용되는 구분 기호를 정의합니다. `Reader` 타입도 이제 `quoted-printable` 부분을 자동으로 디코딩하고, 이를 수행하는 경우 `Content-Transfer-Encoding` 헤더를 제거합니다.
  - `net` 패키지의 `ListenUnixgram` 함수는 이제 다른 유형의 반환 값을 갖습니다. 이제 `UnixConn`을 반환합니다. 이전에는 `UDPConn`을 반환했지만, 이는 Go 1.0의 실수였습니다. 따라서 이 API 변경은 Go 1과의 호환성을 유지하면서 버그를 수정하기 때문에 허용됩니다.
  - `net` 패키지는 `Dialer`라는 새로운 유형을 도입하여 `Dial` 함수의 옵션을 제공합니다.
  - `net` 패키지는 링크-로컬 IPv6 주소, 예를 들어 `fe80::1%lo0`을 지원합니다. 주소 구조체 `IPAddr`, `UDPAddr` 및 `TCPAddr`은 새로운 필드를 사용하여 영역을 기록하고, 문자열 형식으로 이러한 주소를 사용하는 함수, 예를 들어 `Dial`, `ResolveIPAddr`, `ResolveUDPAddr` 및 `ResolveTCPAddr`은 영역 형식을 받습니다.
  - `net` 패키지는 `LookupNS`라는 새로운 함수를 추가했습니다. `LookupNS`는 호스트 이름에 대한 [NS 레코드](/pkg/net/#NS)를 반환합니다.
  - `net` 패키지는 `IPConn` 및 `UDPConn`에 패킷 읽기 및 쓰기 메서드(`ReadMsgIP` 및 `WriteMsgIP`)를 추가했습니다. 이는 `PacketConn`의 `ReadFrom` 및 `WriteTo` 메서드의 특수 버전이며, 패킷과 관련된 오프보드 데이터를 액세스할 수 있습니다.
  - `net` 패키지는 `UnixConn`에 클라이언트 측 연결의 절반을 닫는 메서드(`CloseRead` 및 `CloseWrite`)를 추가했습니다. 이는 `TCPConn`에 있는 것과 동일합니다.
  - `net/http` 패키지는 여러 새로운 기능이 포함되어 있습니다. `ParseTime` 함수는 다양한 HTTP 시간 형식을 사용하여 시간 문자열을 파싱합니다. `Request` 타입의 `PostFormValue` 메서드는 `FormValue`와 유사하지만 URL 파라미터를 무시합니다. `ServeMux` 타입은 `Handler` 메서드를 도입하여 요청을 실행하지 않고도 경로의 `Handler`에 액세스할 수 있습니다. `Transport`는 이제 `Response.Body`가 완전히 소비되기 전에 TCP 연결을 취소할 수 있습니다. 마지막으로, `Transport`는 `Response.Body`가 소비되기 전에 TCP 연결을 더 적극적으로 닫아 `net/http` 패키지에서 사용되는 새 기능을 제공합니다.
  - `net/mail` 패키지에는 `ParseAddress` 및 `ParseAddressList`라는 두 개의 새로운 함수가 도입되었습니다. 이 함수는 RFC 5322 형식의 이메일 주소를 `Address` 구조체로 파싱합니다.
  - `net/smtp` 패키지의 `Client` 타입은 새로운 메서드 `Hello`를 도입했으며, 이를 통해 서버에 `HELO` 또는 `EHLO` 메시지를 전송합니다.
  - `net/textproto` 패키지는 `TrimBytes` 및 `TrimString`이라는 두 개의 새로운 함수를 도입했으며, 이 함수는 ASCII만으로 문자열의 앞과 뒤의 공백을 제거합니다.
  - `os` 패키지의 `FileMode.IsRegular` 메서드는 파일이 일반 파일인지 쉽게 확인할 수 있도록 도와줍니다.
  - `os/signal` 패키지는 새로운 함수 `Stop`을 도입했으며, 이를 통해 패키지가 채널로 신호를 더 이상 전달하지 않도록 할 수 있습니다.
  - `regexp` 패키지는 `Regexp.Longest`라는 새로운 메서드를 도입했으며, 이를 통해 Unix-original의 가장 긴 일치 항목을 찾을 수 있습니다. 또한 `Regexp.Split`은 정규 표현식에 정의된 구분자를 기준으로 문자열을 쪼갤 수 있습니다.
  - `runtime/debug` 패키지는 메모리 사용량에 대한 세 가지 새로운 함수를 도입했습니다. `FreeOSMemory` 함수는 래퍼 콜렉터를 실행하고, 사용하지 않은 메모리를 운영 체제로 반환합니다. `ReadGCStats` 함수는 래퍼 콜렉터에 대한 통계를 가져옵니다. `SetGCPercent` 함수는 콜렉터가 실행되는 빈도를 프로그래밍 방식으로 제어하고, 완전히 비활성화할 수도 있습니다.
  - `sort` 패키지는 `Reverse`라는 새로운 함수를 도입했습니다. 이 함수는 `sort.Sort` 호출에 제공된 인수를 반대로 정렬합니다.
  - `strings` 패키지는 `TrimPrefix` 및 `TrimSuffix`라는 두 개의 새로운 함수를 도입했으며, 이는 직관적인 속성을 갖습니다. 또한 `Reader` 타입은 이제 `io.WriterTo` 인터페이스를 구현하기 위해 `WriteTo` 메서드를 갖습니다.
  - `syscall` 패키지의 `Fchflags` 함수는 여러 BSD(예: Darwin)에서 서명 변경되었습니다. 이제 이 함수의 첫 번째 인수로 정수 값을 전달해야 합니다. 이 API 변경은 Go 1과의 호환성을 유지하면서 버그를 수정하기 때문에 허용됩니다.
  - `syscall` 패키지는 지원되는 각 운영 체제에 대한 새로운 상수와 시스템 호출을 포함하여 업데이트되었습니다.
  - `testing` 패키지는 테스트 및 벤치마크에서 할당 통계를 자동으로 생성하는 새로운 기능이 도입되었습니다. `AllocsPerRun` 함수는 래퍼 콜렉터를 실행하고, 사용하지 않은 메모리를 운영 체제로 반환합니다. `ReportAllocs` 메서드는 `testing.B`의 `ReportAllocs` 메서드를 통해 호출할 수 있으며, 실행되는 래퍼 콜렉터에 대한 메모리 할당 통계를 출력합니다. 또한 `AllocsPerOp` 메서드를 `BenchmarkResult` 타입에 도입하여 각 작업에 대한 할당 횟수를 측정할 수 있습니다. 또한 새로운 `Skip` 메서드를 도입하여 테스트를 쉽게 건너뛸 수 있습니다.
  - `text/template` 및 `html/template` 패키지에서는 파이프에 대한 그룹을 단순화하기 위해 파이프에 대한 괄호를 사용할 수 있습니다. 또한 새로운 메서드를 도입하여 더 나은 오류 보고를 제공합니다.
  - Go 1과의 호환성을 유지하면서 이 인터페이스가 `text/template` 및 `html/template` 패키지에만 명시적으로 사용된다는 점을 고려할 때, 이는 Go 1과의 호환성을 유지합니다.
  - `unicode` 패키지의 구현이 Unicode 버전 6.2.0으로 업데이트되었습니다.
  - `unicode/utf8` 패키지의 새로운 함수 `ValidRune`은 문자가 유효한 Unicode 코드 포인트인지 여부를 보고합니다. 유효한 문자는 범위 내에 있어야 하고, 서루에이트를 포함할 수 없습니다.
