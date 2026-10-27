## Go 1.2 소개 {#introduction}

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, World!")
}
```

## Go 언어의 특징

*   **경량화된 프로세스:** Go는 Go루틴이라는 경량화된 프로세스 모델을 사용하여 효율적인 동시성 프로그래밍을 지원합니다.
*   **강력한 표준 라이브러리:** Go는 다양한 기능을 제공하는 풍부한 표준 라이브러리를 제공합니다.
*   **컴파일 언어:** Go는 빠른 컴파일 속도를 제공하는 컴파일 언어입니다.
*   **가비지 컬렉션:** Go는 자동 가비지 컬렉션을 지원하여 메모리 관리를 단순화합니다.

## Go 언어의 장점

*   **경쟁력 있는 성능:** Go는 C, C++와 같은 저수준 언어에 준하는 뛰어난 성능을 제공합니다.
*   **쉬운 학습:** Go는 비교적 간단한 문법을 가지고 있어 배우기 쉽습니다.
*   **뛰어난 동시성 지원:** Go는 Go루틴을 통해 강력한 동시성 프로그래밍을 지원합니다.
*   **풍부한 생태계:** Go는 활발한 커뮤니티와 다양한 라이브러리를 보유하고 있습니다.

2013년 4월에 [Go 버전 1.1](/doc/go1.1.html)가 출시된 이후,
릴리스 주기를 단축하여 릴리스 프로세스를 더욱 효율적으로 만들었습니다.
이 릴리스, Go 버전 1.2 또는 Go 1.2라고 줄여 부르는 것은 1.1 이후 약 6개월 후에 출시되며,
1.1은 1.0 이후 약 1년이 걸렸습니다.
짧은 기간으로 인해 1.2는 1.0에서 1.1로의 변화보다 작은 변화이지만, 여전히 상당한 발전 사항이 포함되어 있습니다.
예를 들어, 개선된 스케줄러와 새로운 언어 기능이 있습니다.
물론, Go 1.2는 [호환성](/doc/go1compat.html)을 유지합니다.
Go 1.1(또는 1.0으로 구축된)로 작성된 대부분의 프로그램은 1.2로 이동해도 전혀 변경 없이 실행될 것입니다.
하지만 언어의 한 부분에 대한 한 가지 제한 사항이 도입되면 기존의 잘못된 코드가 드러날 수 있습니다 (자세한 내용은 [nil 사용](#use_of_nil) 참조).

## 언어 변경 사항 {#language}

명세를 더욱 명확하게 하기 위해, 하나의 예외적인 경우에 대한 설명이 추가되었으며, 이는 프로그램에 영향을 미칩니다.
또한, 새로운 언어 기능이 추가되었습니다.

### `nil` 사용법 {#use_of_nil}

```go
package main

func main() {
	var x *int
	fmt.Println(x) // 출력: nil

	var y *int
	y = nil
	fmt.Println(y) // 출력: nil
}
```

현재 언어는 안전상의 이유로,
특정 `nil` 포인터 사용은 실행 시 패닉을 발생시킬 것으로 보장합니다.
예를 들어, Go 1.0에서는 다음과 같은 코드를 사용하면

```markdown
```go
type T struct {
	X [1<<24]byte
	Field int32
}
```

```markdown
func main() {
    var x *T
    ...
}
```

`nil` 포인터 `x`는 잘못된 방식으로 메모리에 접근할 수 있습니다:
`x.Field`라는 표현은 주소 `1<<24`에 접근할 수 있습니다.
이러한 위험한 동작을 방지하기 위해, Go 1.2에서는 컴파일러가 `nil` 포인터를 통해 발생하는 모든 간접 참조(예: 여기에서 설명된 것뿐만 아니라 배열, 인터페이스 값, 슬라이스 등에 대한 `nil` 포인터)가 실패하거나 올바른, 안전한 비-`nil` 값을 반환하도록 보장합니다.
요약하면, 명시적이거나 암묵적으로 `nil` 주소의 평가를 필요로 하는 모든 표현은 오류입니다.
구현은 이 동작을 강제하기 위해 컴파일된 프로그램에 추가 테스트를 삽입할 수 있습니다.

자세한 내용은 다음 문서를 참조하십시오:
[설계 문서](/s/go12nil).

_업데이트_:
오래된 동작에 의존하는 대부분의 코드는 잘못되었으며 실행될 때 오류가 발생합니다.
이러한 프로그램은 수동으로 업데이트해야 합니다.

### 3개 인덱스 슬라이스 {#three_index}

Go 1.2에서는 기존의 배열 또는 슬라이스에 대한 슬라이싱 연산을 사용할 때, 길이를 지정하는 것뿐만 아니라 용량도 지정할 수 있는 기능을 추가했습니다.
슬라이싱 연산은 이미 생성된 배열 또는 슬라이스의 연속적인 부분을 설명하여 새로운 슬라이스를 생성합니다:

```markdown
var array [10]int
	slice := array[2:4]
```

슬라이스의 용량은 슬라이스가 재할당 후에도 담을 수 있는 최대 개수의 요소를 나타냅니다.
이는 기본 배열의 크기를 반영합니다.
이 예시에서 `slice` 변수의 용량은 8입니다.

Go 1.2는 슬라이싱 연산이 길이를 지정할 뿐만 아니라 용량도 지정할 수 있도록 새로운 구문을 추가합니다.
두 번째
콜론은 용량 값을 도입하며, 이는 소스 슬라이스 또는 배열의 용량보다 작거나 같아야 하며, 원본에 따라 조정됩니다. 예를 들어,

slice = array[2:4:7]

새 슬라이스는 이전 예제와 동일한 길이를 갖지만, 이제 용량은 5개의 요소(7-2)만 갖습니다.
이 새로운 슬라이스 값을 사용하여 원래 배열의 마지막 3개의 요소를 접근하는 것은 불가능합니다.

이 세 인덱스 표기법에서 첫 번째 인덱스가 누락된 경우 (`[:i:j]`) 기본값은 0이지만, 다른 두 인덱스는 항상 명시적으로 지정해야 합니다.
향후 Go의 버전에서 이러한 인덱스에 대한 기본값을 도입할 수도 있습니다.

자세한 내용은 다음에서 확인할 수 있습니다:
[설계 문서](/s/go12slice)

_업데이트_:
이것은 기존 프로그램에 영향을 미치지 않는 역호환성 변경 사항입니다.

## 구현 및 도구에 대한 변경 사항 {#impl}

### 스케줄러에서의 우선순위 설정 {#preemption}

이전 버전에서는 무한 루프를 실행하는 goroutine이 동일한 스레드 내의 다른 goroutine을 "굶게" 만들 수 있었고, 이는 `GOMAXPROCS`가 단일 사용자 스레드만 제공할 때 심각한 문제였습니다.
Go 1.2에서는 이 문제가 부분적으로 해결되었습니다: 스케줄러는 함수 진입 시 간헐적으로 호출됩니다.
따라서 (인라인되지 않은) 함수 호출을 포함하는 모든 루프는 중단될 수 있으며, 이를 통해 동일한 스레드 내에서 다른 goroutine을 실행할 수 있습니다.

### 스레드 수 제한 {#thread_limit}

Go 1.2 버전에서는 프로그램이 사용할 수 있는 주소 공간 내의 총 스레드 수를 구성 가능하게 설정 (기본값: 10,000) 합니다. 이는 일부 환경에서 자원 고갈 문제를 방지하기 위한 것입니다.
참고: goroutine은 스레드에 묶여 있으므로, 이 제한은 직접적으로 goroutine의 수를 제한하는 것이 아니라, 시스템 호출 시 동시에 차단될 수 있는 스레드 수를 제한합니다.
실제로 이 제한을 달성하는 것은 어렵습니다.

새로운 [`SetMaxThreads`](/pkg/runtime/debug/#SetMaxThreads) 함수는
[`runtime/debug`](/pkg/runtime/debug/) 패키지에 포함되어 있으며, 스레드 개수 제한을 제어합니다.

_업데이트_:
몇몇 함수만 제한에 영향을 받지만, 제한에 도달하여 프로그램이 종료되는 경우, `SetMaxThreads`를 호출하여 더 높은 값을 설정하도록 수정할 수 있습니다.
더 나은 방법은 프로그램 자체를 수정하여 더 적은 수의 스레드를 사용하도록 변경하고, 이를 통해 커널 자원 소비를 줄이는 것입니다.

### 스택 크기 {#stack_size}

Go 1.2에서 goroutine이 생성될 때 기본 스택 크기가 4KB에서 8KB로 변경되었습니다.
이전 크기는 많은 프로그램에서 성능 문제를 일으켰고, 특히 성능이 중요한 부분에서 비싼 스택 세그먼트 전환을 유발하는 경향이 있었습니다.
새로운 값은 실험적인 테스트를 통해 결정되었습니다.

반대쪽에서는 [`SetMaxStack`](/pkg/runtime/debug/#SetMaxStack) 함수가 [`runtime/debug`](/pkg/runtime/debug) 패키지에 존재하며,
단일 고루틴의 스택의 최대 크기를 제어합니다.
기본값은 64비트 시스템에서는 1GB, 32비트 시스템에서는 250MB입니다.
Go 1.2 이전에는, 무한 반복이 시스템의 메모리를 모두 소모하는 경우가 많았습니다.

_업데이트_:
최대 스택 크기 증가로 인해 많은 고루틴을 사용하는 프로그램이 더 많은 메모리를 사용할 수 있습니다. 이 문제를 해결할 수 있는 방법은 없지만, 향후 릴리스에는 더 나은 해결책을 제공할 새로운 스택 관리 기술이 포함될 예정입니다.

### Cgo와 C++ {#cgo_and_cpp}

명령 `cgo`는 이제 C++로 작성된 링크된 라이브러리의 일부를 빌드하기 위해 C++ 컴파일러를 호출합니다. 자세한 내용은 [문서](/cmd/cgo/)를 참조하십시오.

### Godoc 및 vet를 go.tools 서브리포지토리로 이동 (#go_tools_godoc)

`godoc` 및 `vet` 명령에 대한 소스 코드는 여전히 배포판에 포함되어 있지만, [go.tools](https://code.google.com/p/go.tools) 서브 저장소로 이동했습니다.

또한, godoc 프로그램의 핵심 기능이 [라이브러리](https://code.google.com/p/go/source/browse/?repo=tools#hg%2Fgodoc)로 분리되었으며, 자체 명령은 별도의 [디렉토리](https://code.google.com/p/go/source/browse/?repo=tools#hg%2Fcmd%2Fgodoc)에 있습니다. 이러한 변경을 통해 코드를 쉽게 업데이트할 수 있으며, 라이브러리와 명령으로의 분리는 로컬 사이트 및 다양한 배포 방법에 대한 사용자 정의 바이너리를 구축하는 데 용이합니다.

_업데이트_:
`godoc` 및 `vet`은 라이브러리의 일부가 아니므로,
클라이언트 Go 코드에서 이러한 소스에 의존하지 않으며, 업데이트가 필요하지 않습니다.

다음 바이너리 배포판은 [golang.org](/)에서 제공되므로, 이러한 배포판의 사용자는 영향을 받지 않습니다.

소스에서 빌드할 때, 사용자는 godoc 및 vet를 설치하기 위해 "go get"을 사용해야 합니다.
(실행 파일은 일반적인 위치에 계속 설치됩니다. `$GOPATH/bin`이 아닌.)

$ go get code.google.com/p/go.tools/cmd/godoc
	$ go get code.google.com/p/go.tools/cmd/vet

### gccgo의 상태 {#gccgo}

저희는 향후 GCC 4.9 릴리스에 gccgo가 Go 1.2에 대한 완전한 지원을 포함할 것으로 예상합니다.
현재 (4.8.2) 릴리스의 GCC에서 gccgo는 Go 1.1.2를 구현합니다.

### GC 컴파일러 및 링커 변경 사항 {#gc_changes}

Go 1.2에는 GC 컴파일러 스위트의 작동 방식에 여러 의미론적 변경 사항이 있습니다.
대부분의 사용자는 이 변경 사항으로 인해 영향을 받지 않습니다.

명령 `cgo`는 이제 C++이 링크되는 라이브러리에 포함될 때 작동합니다.
자세한 내용은 `cgo` 문서를 참조하십시오.

`gc` 컴파일러는 프로그램에 `package` 절이 없을 때, 컴파일러의 원래 형태를 반영하는 오류 메시지를 표시했습니다. 즉, 파일을 `main` 패키지에 있다고 가정했습니다.

과거는 사라졌고, `package` 절이 누락되면 이제는 오류가 발생합니다.

ARM 아키텍처에서는 "외부 링크" 기능을 지원하며, 이는 `gc` 툴체인을 사용하여 공유 라이브러리를 빌드하고, 필요한 환경에서 동적 링크를 지원하는 데 필요한 단계입니다.

ARM 아키텍처의 런타임 환경에서, `5a` 버전에서는 `R9`와 `R10`을 직접 사용하여 런타임 내부의 `m` (메시) 및 `g` (고루틴) 변수에 접근할 수 있었습니다.
이제는 해당 변수들을 적절한 이름으로 참조해야 합니다.

또한 ARM 아키텍처에서는 `5l` 링커가 `MOVBS` 및 `MOVHS` 명령어를 `MOVB` 및 `MOVH` 명령어와 동의어로 정의하여, 부호 있는(signed) 및 부호 없는(unsigned) 서브워드 이동 간의 구분을 명확하게 합니다. 이미 부호 없는 버전은 `U` 접미사를 사용하여 존재했습니다.

### 테스트 커버리지 {#cover}

`go test`의 주요 새로운 기능 중 하나는 이제 테스트 커버리지를 계산하고, 새로운 별도로 설치된 "go tool cover" 프로그램을 사용하여 테스트 커버리지를 표시할 수 있다는 것입니다.

`cover` 도구는 [`go.tools`](https://code.google.com/p/go/source/checkout?repo=tools)
서브리포지토리의 일부입니다.
다음 명령을 실행하여 설치할 수 있습니다:

$ go get code.google.com/p/go.tools/cmd/cover

이 도구는 두 가지 기능을 수행합니다.
첫째, "go test"에 "-cover" 플래그를 제공하면, 자동으로 패키지의 소스를 다시 작성하고 측정 문을 삽입하도록 실행됩니다.
그런 다음 테스트는 정상적으로 컴파일되고 실행되며, 기본적인 커버리지 통계가 보고됩니다:

```markdown
$ go test -cover fmt
	ok 	fmt	0.060s	테스트 결과: 91.4%의 코드 커버리지
	$
```

둘째, 더 자세한 보고서를 위해, `go test` 명령에 다양한 플래그를 사용하면 커버리지 프로필 파일을 생성할 수 있으며, `go tool cover` 명령으로 실행되는 `cover` 프로그램은 이를 분석할 수 있습니다.

다음 명령을 실행하여 생성 및 분석 방법에 대한 자세한 내용은 확인할 수 있습니다.

```
$ go help testflag
	$ go tool cover -help
```

### `go doc` 명령어는 삭제되었습니다 {#go_doc}

"go doc" 명령이 삭제되었습니다.
참고: [`godoc`](/cmd/godoc/) 도구 자체는 삭제되지 않았으며,
단 `go` 명령에서 제공하는 래퍼 기능만 삭제되었습니다.
이 도구는 단순히 패키지 경로별로 문서를 보여주는 기능만 제공했으며,
godoc 자체도 더 많은 유연성을 제공합니다.
따라서, 문서 생성 도구의 수를 줄이고, godoc의 재구성을 통해 향후 더 나은 옵션을 제공하기 위해 삭제되었습니다.

_업데이트_: 다음 기능을 정확하게 사용해야 하는 분들을 위해:

$ go doc

디렉토리 내에서, 동작은 다음과 같이 실행하는 것과 동일합니다.

`godoc .`

### `go` 명령어에 대한 변경 사항 {#gocmd}

[`go get`](/cmd/go/) 명령어는 이제 `-t` 플래그를 통해 패키지에 포함된 테스트를 실행하는 데 필요한 의존성을 다운로드할 수 있습니다. (패키지 자체의 의존성뿐만 아니라).
기본적으로, 이전과 마찬가지로, 테스트의 의존성은 다운로드되지 않습니다.

## 성능 {#performance}

표준 라이브러리에는 여러 가지 중요한 성능 개선 사항이 있습니다. 몇 가지 예시는 다음과 같습니다.

- [`compress/bzip2`](/pkg/compress/bzip2/)
    는 압축/해제 속도가 약 30% 더 빠릅니다.
  - [`crypto/des`](/pkg/crypto/des/) 패키지는 약 5배 더 빠릅니다.
  - [`encoding/json`](/pkg/encoding/json/) 패키지는 압축/해제 속도가 약 30% 더 빠릅니다.
  - Windows 및 BSD 시스템의 네트워크 성능은 통합 네트워크 폴러를 사용하여 약 30% 더 빠릅니다 (이는 Go 1.1에서 Linux 및 OS X에 적용된 방식과 유사합니다).

## 표준 라이브러리의 변경 사항 {#library}

이 섹션에서는 표준 라이브러리의 변경 사항에 대한 개요를 제공합니다.

### 아카이브/tar 및 아카이브/zip 패키지 {#archive_tar_zip}

[`archive/tar`](/pkg/archive/tar/)
과
[`archive/zip`](/pkg/archive/zip/)
패키지는 의미론적 측면에서 변경되었으며, 이는 기존 프로그램에 영향을 줄 수 있습니다.
문제는 이 두 패키지가 모두
[`os.FileInfo`](/pkg/os/#FileInfo)
인터페이스의 구현을 제공했지만, 이 인터페이스의 사양과 일치하지 않았다는 점입니다.
특히, `Name` 메서드는 엔트리의 전체
경로 이름을 반환했지만, 인터페이스 사양은 메서드가 최종 경로 요소(기본 이름)만 반환하도록 요구합니다.

_업데이트_: 이 동작이 최근에 구현되었고 다소 불명확하기 때문에, 이 오류 동작에 의존하는 코드가 없는 경우도 있을 수 있습니다. 만약 이 동작에 의존하는 프로그램이 있다면, 해당 프로그램을 식별하고 수동으로 수정해야 합니다.

### 새로운 인코딩 패키지 {#encoding}

새로운 패키지인 [`encoding`](/pkg/encoding/)는 표준 인코딩 인터페이스 집합을 정의하며, 이를 사용하여 `encoding/xml`](/pkg/encoding/xml/),
`encoding/json`](/pkg/encoding/json/),
그리고
`encoding/binary`](/pkg/encoding/binary/)와 같은 패키지를 위한 사용자 정의 마샬러 및 언마샬러를 구축하는 데 사용할 수 있습니다.

이 새로운 인터페이스는 표준 라이브러리의 일부 구현을 정리하는 데 사용되었습니다.

새로운 인터페이스는 다음과 같이 명명됩니다:
[`BinaryMarshaler`](/pkg/encoding/#BinaryMarshaler),
[`BinaryUnmarshaler`](/pkg/encoding/#BinaryUnmarshaler),
[`TextMarshaler`](/pkg/encoding/#TextMarshaler),
그리고
[`TextUnmarshaler`](/pkg/encoding/#TextUnmarshaler).
전체 내용은 패키지의 [문서](/pkg/encoding/)에 있으며, 별도의 [설계 문서](/s/go12encoding)도 있습니다.

### `fmt` 패키지 {#fmt_indexed_arguments}

[`fmt`](/pkg/fmt/) 패키지의 포맷된 출력
루틴, 예를 들어 [`Printf`](/pkg/fmt/#Printf),
이제 형식 사양 내의 인덱싱 연산을 사용하여 데이터를 임의의 순서로 출력할 수 있습니다.
형식에 사용할 인수를 가져올 위치, 즉 형식을 지정하거나 너비 또는 사양 정수로서,
새로운 선택적 인덱싱 표기법 `[_n_]`을 사용하여 _n_번째 인수를 가져옵니다.
_n_의 값은 1부터 시작합니다.
이러한 인덱싱 연산 후, 정상적인 처리가 다음 가져올 인수는 _n_+1이 됩니다.

예를 들어, 일반적인 `Printf` 호출
```go
fmt.Printf("Hello, world!\n")
```

`fmt.Sprintf("%c %c %c\n", 'a', 'b', 'c')`

다음과 같이 인덱싱 작업을 수행하면 `"a b c"`라는 문자열을 생성할 수 있습니다.

`fmt.Sprintf("%[3]c %[1]c %c\n", 'a', 'b', 'c')`

결과는 "`"c a b"`. 인덱스 `[3]`는 세 번째 포맷팅 인수를 참조하며, 이는 `'c'`입니다. 인덱스 `[1]`은 첫 번째 인수를 참조하며, 이는 `'a'`입니다. 그런 다음 다음 획득은 그 다음 인수를 참조하며, 이는 `'b'`입니다.

이 기능의 목적은 다양한 언어에 맞게 인수를 다른 순서로 접근하기 위한 프로그래밍 가능한 형식 문을 제공하는 것입니다. 하지만, 이 기능은 다음과 같은 다른 용도로도 사용될 수 있습니다:

log.Printf("trace: 값 %v 유형 %[1]T\n", expensiveFunction(a.b[c]))

_업데이트_: 형식 사양의 구문 변경은 엄격하게 역호환성을 유지하므로, 기존에 작동하는 프로그램에는 영향을 미치지 않습니다.

### `text/template` 및 `html/template` 패키지 {#text_template}

[`text/template`](/pkg/text/template/) 패키지는 Go 1.2에서 몇 가지 변경 사항이 있으며, 이 변경 사항은 `html/template`](/pkg/html/template/) 패키지도 반영하고 있습니다.

먼저, 기본 유형 비교를 위한 새로운 기본 함수가 추가되었습니다.
이 함수 목록은 테이블에 나와 있으며, 함수 이름과 관련된 일반적인 비교 연산자를 보여줍니다.

```markdown
<table cellpadding="0" summary="템플릿 비교 함수">
<tbody><tr>
<th width="50"></th><th width="100">이름</th> <th width="50">연산자</th>
</tr>
<tr>
<td></td><td><<code>eq</code></code></td> <td><<code>==</code></code></td>
</tr>
<tr>
<td></td><td><<code>ne</code></code></td> <td><<code>!=</code></code></td>
</tr>
<tr>
<td></td><td><<code>lt</code></code></td> <td><<code>&lt;</code></code></td>
</tr>
<tr>
<td></td><td><<code>le</code></code></td> <td><<code>&lt;=</code></code></td>
</tr>
<tr>
<td></td><td><<code>gt</code></code></td> <td><<code>&gt;</code></code></td>
</tr>
<tr>
<td></td><td><<code>ge</code></code></td> <td><<code>&gt;=</code></code></td>
</tr>
</tbody></table>
```

이 함수들은 해당 Go 연산자와 약간 다른 방식으로 작동합니다.
첫째, 이 함수들은 기본 타입(`bool`, `int`,
`float64`, `string` 등)에만 작동합니다.
(Go는 특정 조건 하에서 배열과 구조체도 비교할 수 있습니다.)
둘째, 동일한 유형의 값끼리 비교할 수 있습니다:
예를 들어, 어떤 부호 있는 정수 값도 다른 부호 있는 정수 값과 비교할 수 있습니다. (Go는 `int8`과 `int16`의 비교를 허용하지 않습니다.)
마지막으로, `eq` 함수(전용)는 첫 번째 인수를 하나 이상의 후속 인수로 비교할 수 있습니다. 이 예제에서 사용된 템플릿은

{{if eq .A 1 2 3}} 같음 {{else}} 다름 {{end}}

보고서는 `.A`가 1, 2, 또는 3 중 _어느 값과_ 같을 경우 "equal"이라고 보고합니다.

두 번째 변경 사항은 문법에 약간의 추가를 통해 "if else if" 형태의 조건문을 더 쉽게 작성할 수 있도록 하는 것입니다.
예를 들어, 다음과 같이 작성하는 대신,

{{if eq .A 1}} X {{else}} {{if eq .A 2}} Y {{end}} {{end}}

두 번째 "if" 문을 "else" 안에 통합하고, 단 하나의 "end"만 사용하는 방식으로 변경할 수 있습니다. 예를 들어:

{{if eq .A 1}} X {{else if eq .A 2}} Y {{end}}

두 형태는 효과가 동일합니다. 차이점은 문법만 다릅니다.

_업데이트_: "else if" 변경 사항이나 비교 함수는 기존 프로그램에 영향을 미치지 않습니다. 이미 `eq`와 같은 함수를 호출하는 함수를 정의한 프로그램은 영향을 받지 않습니다. 이는 연관된 함수 맵이 새로운 기본 함수 정의를 덮어쓸 것이기 때문입니다.

### 새로운 패키지 {#new_packages}

두 개의 새로운 패키지가 있습니다.

- [`encoding`](/pkg/encoding/) 패키지는
    [위에 설명](#encoding)되어 있습니다.
  - [`image/color/palette`](/pkg/image/color/palette/) 패키지는
    표준 색상 팔레트를 제공합니다.

### 라이브러리의 미미한 변경 사항 {#minor_library_changes}

다음 목록은 라이브러리의 여러 개의 소규모 변경 사항을 요약하고 있으며, 대부분은 추가 사항입니다.
각 변경 사항에 대한 자세한 내용은 관련 패키지 문서를 참조하십시오.

- [`archive/zip`](/pkg/archive/zip/) 패키지는
    [`DataOffset`](/pkg/archive/zip/#File.DataOffset) 접근자를 추가하여,
    파일의 (압축된) 데이터의 내 보관 파일 내 위치를 반환합니다.
  - [`bufio`](/pkg/bufio/) 패키지는
    [`Reset`](/pkg/bufio/#Reader.Reset)
    메서드를 [`Reader`](/pkg/bufio/#Reader) 및
    [`Writer`](/pkg/bufio/#Writer)에 추가합니다.
    이 메서드는 [`Readers`](/pkg/io/#Reader) 및
    [`Writers`](/pkg/io/#Writer)를 새로운 입력 및 출력 리더 및 라이터에서 재사용할 수 있도록 하며,
    할당 오버헤드를 절약합니다.
  - [`compress/bzip2`](/pkg/compress/bzip2/)는 이제 묶인 보관 파일을 압축 해제할 수 있습니다.
  - [`compress/flate`](/pkg/compress/flate/) 패키지는 [`Writer`](/pkg/compress/flate/#Writer)에
    [`Reset`](/pkg/compress/flate/#Writer.Reset)
    메서드를 추가하여, 예를 들어 여러 압축 파일을 포함하는 보관 파일을 구성할 때 할당을 줄일 수 있도록 합니다.
  - [`compress/gzip`](/pkg/compress/gzip/) 패키지의
    [`Writer`](/pkg/compress/gzip/#Writer) 유형에
    [`Reset`](/pkg/compress/gzip/#Writer.Reset)
    이 추가되어 재사용할 수 있습니다.
  - [`compress/zlib`](/pkg/compress/zlib/) 패키지의
    [`Writer`](/pkg/compress/zlib/#Writer) 유형에
    [`Reset`](/pkg/compress/zlib/#Writer.Reset)
    이 추가되어 재사용할 수 있습니다.
  - [`container/heap`](/pkg/container/heap/) 패키지는
    더 효율적인 방식으로 힙 내 항목의 위치를 업데이트하는 방법을 제공하기 위해
    [`Fix`](/pkg/container/heap/#Fix)
    메서드를 추가합니다.
  - [`container/list`](/pkg/container/list/) 패키지는
    [`MoveBefore`](/pkg/container/list/#List.MoveBefore) 및
    [`MoveAfter`](/pkg/container/list/#List.MoveAfter)
    메서드를 추가하여, 명확한 재정렬을 구현합니다.
  - [`crypto/cipher`](/pkg/crypto/cipher/) 패키지는
    거의 항상 AES 암호화와 함께 사용되는 새로운 GCM 모드 (Galois Counter Mode)를 추가합니다.
  - [`crypto/md5`](/pkg/crypto/md5/) 패키지는
    가성능을 저하시키지 않고 단순화하기 위해 새로운 [`Sum`](/pkg/crypto/md5/#Sum) 함수를 추가합니다.
  - 마찬가지로
    [`crypto/sha1`](/pkg/crypto/md5/) 패키지는 새로운 [`Sum`](/pkg/crypto/sha1/#Sum) 함수를 추가합니다.
  - 또한
    [`crypto/sha256`](/pkg/crypto/sha256/) 패키지는 [`Sum256`](/pkg/crypto/sha256/#Sum256) 및
    [`Sum224`](/pkg/crypto/sha256/#Sum224) 함수를 추가합니다.
  - 마지막으로, [`crypto/sha512`](/pkg/crypto/sha512/) 패키지는
    [`Sum512`](/pkg/crypto/sha512/#Sum512) 및
    [`Sum384`](/pkg/crypto/sha512/#Sum384) 함수를 추가합니다.
  - [`crypto/x509`](/pkg/crypto/x509/) 패키지는
    임의의 확장 파일을 읽고 쓰는 기능을 추가합니다.
  - [`crypto/tls`](/pkg/crypto/tls/) 패키지는
    TLS 1.1, 1.2 및 AES-GCM을 지원합니다.
  - [`database/sql`](/pkg/database/sql/) 패키지는
    [`DB`](/pkg/database/sql/#DB)에 [`SetMaxOpenConns`](/pkg/database/sql/#DB.SetMaxOpenConns)
    메서드를 추가하여, 데이터베이스에 열린 연결 수를 제한합니다.
  - [`encoding/csv`](/pkg/encoding/csv/) 패키지는
    이제 필드에 트레일링 쉼표를 항상 허용합니다.
  - [`encoding/gob`](/pkg/encoding/gob/) 패키지는
    구조체의 채널 및 함수 필드를 비개방으로 취급하며,
    이러한 필드가 비개방인 경우 오류를 발생시킵니다. 이전에는 이러한 필드가 오류를 발생시켜, 내장 구조가 이러한 필드를 추가하면 예상치 못한 호환성 문제가 발생할 수 있었습니다. 패키지는 또한
    `encoding` 패키지의 일반적인 `BinaryMarshaler` 및
    `BinaryUnmarshaler` 인터페이스를 지원합니다.
  - [`encoding/json`](/pkg/encoding/json/) 패키지는
    이제 문자열을 출력할 때 항상 "\u0026"로 "&"를 이스케이프합니다.
    이전에는 잘못된 UTF-8 인수가 거부되었습니다. 이제 잘못된 UTF-8를 허용하고 수정합니다. 마지막으로,
    `encoding` 패키지의 일반적인 인코딩 인터페이스를 지원합니다.
  - [`encoding/xml`](/pkg/encoding/xml/) 패키지는
    포인터에 저장된 속성을 매핑할 수 있습니다.
    또한 새로운
    [`Marshaler`](/pkg/encoding/xml/#Marshaler),
    [`Unmarshaler`](/pkg/encoding/xml/#Unmarshaler) 및 관련된
    [`MarshalerAttr`](/pkg/encoding/xml/#MarshalerAttr) 및
    [`UnmarshalerAttr`](/pkg/encoding/xml/#UnmarshalerAttr)
    인터페이스를 통해
    [`encoding`](/pkg/encoding/) 패키지의 일반적인 인코딩 인터페이스를 지원합니다.
    또한
    [`Encoder`](/pkg/encoding/xml/#Encoder) 유형에
    [`Flush`](/pkg/encoding/xml/#Encoder.Flush)
    메서드를 추가하여 사용자가 자체 인코더를 만들 수 있도록 합니다.
    [`EncodeToken`](/pkg/encoding/xml/#Encoder.EncodeToken)를 사용하여 사용하는 방법을 참조하십시오.
  - [`flag`](/pkg/flag/) 패키지는
    [`Getter`](/pkg/flag/#Getter) 인터페이스를 추가하여 플래그의 값을 가져올 수 있습니다.
    Go 1 호환성 지침으로 인해 이 메서드는 기존 [`Value`](/pkg/flag/#Value) 인터페이스에 추가할 수 없지만 모든 기존 표준 플래그 유형이 이를 구현합니다.
    패키지는 또한 명령줄에 있는 플래그를 포함하는 [`CommandLine`](/pkg/flag/#CommandLine) 플래그 세트를 내보냅니다.
  - [`go/ast`](/pkg/go/ast/) 패키지의
    [`SliceExpr`](/pkg/go/ast/#SliceExpr) 구조에 새로운 부울 필드, `Slice3`가 추가되어 세 개의 인덱스를 사용하는 슬라이스 표현을 나타냅니다. 기본값은 false이며, 이는 일반적인 두 개의 인덱스 형태를 나타냅니다.
  - [`go/build`](/pkg/go/build/) 패키지는
    [`Package`](/pkg/go/build/#Package) 유형에 `AllTags` 필드를 추가하여 빌드 태그를 처리하는 것을 더 쉽게 만듭니다.
  - [`image/draw`](/pkg/image/draw/) 패키지는
    새로운 인터페이스, [`Drawer`](/pkg/image/draw/#Drawer)를 내보냅니다.
    Porter-Duff 연산자는 이제 이 인터페이스를 구현하여, 연산을 draw operator에 묶어 연산을 직접 제공하지 않아도 됩니다.
    새로운 [`FloydSteinberg`](/pkg/image/draw/#FloydSteinberg) 구현은
    [`Drawer`](/pkg/image/draw/#Drawer) 인터페이스를 사용하여 팔레팅된 이미지를 그립니다.
    이러한 처리를 위한 적절한 팔레트를 만드는 새로운
    [`Quantizer`](/pkg/image/draw/#Quantizer) 인터페이스는 팔레트 선택 알고리즘을 구현합니다.
    이 인터페이스의 구현이 라이브러리에는 없습니다.
  - [`image/gif`](/pkg/image/gif/) 패키지는 이제 새로운
    [`Encode`](/pkg/image/gif/#Encode) 및
    [`EncodeAll`](/pkg/image/gif/#EncodeAll)
    함수를 사용하여 GIF 파일을 만들 수 있습니다.
    이 함수는 `nil`인 경우 (`nil`이면 기본인 `Plan9` 색상 맵(팔레트)을 사용합니다.
    또한 이 함수는 출력 이미지에 사용할 새
    [`Quantizer`](/pkg/image/draw/#Quantizer)를 지정할 수 있습니다.
    이 함수는 새
    [`Drawer`](/pkg/image/draw/#Drawer)를 지정할 수 있습니다. Floyd-Steinberg 오류 확산을 사용합니다.
  - [`Copy`](/pkg/io/#Copy) 메서드는 이제 우선순위를 다른 방식으로 지정합니다.
    `Copy`는 한쪽이 [`WriterTo`](/pkg/io/#WriterTo)를 구현하고 다른 쪽이 [`ReaderFrom`](/pkg/io/#ReaderFrom)를 구현하는 경우 이제
    `WriterTo`를 호출하여 작업을 수행하므로 일반적으로 중간 버퍼링이 덜 필요합니다.
  - [`net`](/pkg/net/) 패키지는 cgo를 기본으로 요구합니다.
    호스트 운영 체제가 네트워크 호출 설정을 일반적으로 중재해야 하기 때문입니다.
    그러나 시스템에서 cgo를 사용하지 않는 것이 가능하며, 이는 일반적으로 장점을 제공합니다.
    새로운 빌드 태그 `netgo`는 기본적으로 꺼져 있습니다.
  - [`net`](/pkg/net/) 패키지는 새로운 필드 `DualStack`을 [`Dialer`](/pkg/net/#Dialer) 구조에 추가하여 RFC 6555에 설명된 TCP 연결 설정을 중단합니다.
  - [`net/http`](/pkg/net/http/) 패키지는 이제 RFC 6265를 준수하지 않는 쿠키를 전송하지 않습니다.
    오류를 기록하고 전송하지 않습니다.
    또한 [`net/http`](/pkg/net/http/) 패키지의
    [`ReadResponse`](/pkg/net/http/#ReadResponse) 함수는 `*Request` 매개변수에 `nil`을 허용할 수 있으며, 이 경우 GET 요청으로 가정합니다.
    마지막으로, HTTP 서버는 이제 헤더를 처리하지 않고 HEAD 요청을 처리합니다.
    헤더를 처리할 때, [`Handler`](/pkg/net/http/#Handler)의
    [`ResponseWriter`](/pkg/net/http/#ResponseWriter)
    에 대한 쓰기는
    [`Server`](/pkg/net/http/#Server)에 의해 소비되며, 클라이언트는 HTTP 사양에 따라 빈 바디를 받습니다.
  - [`os/exec`](/pkg/os/exec/) 패키지의
    [`Cmd.StdinPipe`](/pkg/os/exec/#Cmd.StdinPipe) 메서드는 이제
    `io.WriteCloser`를 반환하지만, 더 이상 `*os.File`이 아닌 unexported 유형을 사용하여 반환합니다. 이전 Go 1.2 버전에서는 이로 인해 불필요한 경쟁이 발생했습니다. 이 문제를 해결하려면 인터페이스 유형 암시를 사용할 수 있습니다. 예를 들어, `wc.(interface{ Sync() error })`
  - [`runtime`](/pkg/runtime/) 패키지는
    [`SetFinalizer`](/pkg/runtime/#SetFinalizer) 메서드에서 finalizer 함수에 대한 제약을 완화합니다.
    이제 형식의 원래 유형에 매핑되는 모든 유형의 finalizer 인수를 허용합니다.
  - [`sort`](/pkg/sort/) 패키지는 이제 새로운
    [`Stable`](/pkg/sort/#Stable) 함수를 추가하여 안정적인 정렬을 구현합니다.
    이 함수는 표준 정렬 알고리즘보다 덜 효율적이지만.
  - [`strings`](/pkg/strings/) 패키지는
    [`IndexByte`](/pkg/strings/#IndexByte) 함수를 추가하여
    [`bytes`](/pkg/bytes/) 패키지의 해당 함수와 일관성을 유지합니다.
  - [`sync/atomic`](/pkg/sync/atomic/) 패키지는
    새로운 스왑 함수 세트를 추가합니다.
    이 함수는 지정된 포인터에 저장된 값을 원본 값으로 교환하고, 원래 값을 반환합니다.
    이러한 함수는
    [`SwapInt32`](/pkg/sync/atomic/#SwapInt32),
    [`SwapInt64`](/pkg/sync/atomic/#SwapInt64),
    [`SwapUint32`](/pkg/sync/atomic/#SwapUint32),
    [`SwapUint64`](/pkg/sync/atomic/#SwapUint64),
    [`SwapUintptr`](/pkg/sync/atomic/#SwapUintptr),
    [`SwapPointer`](/pkg/sync/atomic/#SwapPointer)입니다.
  - [`syscall`](/pkg/syscall/) 패키지는 이제
    [`Sendfile`](/pkg/syscall/#Sendfile)를 Darwin용으로 구현합니다.
  - [`testing`](/pkg/testing/) 패키지는 이제
    [`TB`](/pkg/testing/#TB) 인터페이스를 내보냅니다.
    이는 [`T`](/pkg/testing/#T) 및
    [`B`](/pkg/testing/#B) 유형에서 공통 메서드를 제공합니다.
  - [`text/template`](/pkg/text/template/) 패키지는 이제
    "escape" 함수에 대한 인수를 평가할 때 포인터 값의 무덤을 자동으로 처리합니다.
    `printf`와 같은 인쇄 함수에서 다른 함수와 일관성을 유지합니다.
  - [`time`](/pkg/time/) 패키지에서
    [`Parse`](/pkg/time/#Parse) 함수 및
    [`Format`](/pkg/time/#Time.Format) 메서드는
    예: "1871-01-01T05:33:02+00:34:08"와 같이 초 단위의 시간대를 처리합니다.
    또한 이러한 형식의 패턴 일치 규칙이 더 엄격합니다. 이제 "Jan" 및 "Mon"과 같이 표준 단어를 따릅니다.
  - [`unicode`](/pkg/unicode/) 패키지는
    새로운 [`In`](/pkg/unicode/#In) 함수를 추가합니다.
    이 함수는 원래의 [`IsOneOf`](/pkg/unicode/#IsOneOf)와 동일한 기능을 수행합니다.
