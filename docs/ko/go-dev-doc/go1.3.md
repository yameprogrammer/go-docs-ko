## Go 1.3 소개 {#introduction}

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, World!")
}
```

이 코드는 Go 1.3의 기본적인 구조를 보여줍니다. `package main`은 Go 프로그램의 진입점을 정의합니다. `import "fmt"`은 `fmt` 패키지를 가져옵니다. 이 패키지는 문자열을 출력하는 기능을 제공합니다. `func main()`은 프로그램의 시작점을 정의하며, `fmt.Println("Hello, World!")`는 "Hello, World!"라는 메시지를 콘솔에 출력합니다.

가장 최신 Go 릴리스인 버전 1.3은 1.2 이후 6개월 만에 출시되었으며, 언어 변경 사항은 없습니다.
주요 초점은 구현 작업에 있으며, 정확한 가비지 컬렉션을 제공하고, 컴파일러 도구 체인을 크게 재구성하여 다음과 같은 이점을 제공합니다.
* 특히 대규모 프로젝트의 경우 빌드 속도 향상
* 전반적인 성능 향상
* DragonFly BSD, Solaris, Plan 9 및 Google의 Native Client 아키텍처 (NaCl) 지원
또한, 메모리 모델에 대한 중요한 개선 사항이 포함되어 있으며, 특히 동기화와 관련하여 그렇습니다.
물론, Go 1.3은 [호환성
약속](/doc/go1compat.html)을 유지하며, 1.3으로 이동하면 거의 모든 것이 변경 없이 컴파일 및 실행됩니다.

## 지원되는 운영체제 및 아키텍처 변경 {#os}

### Windows 2000 지원 중단 {#win2000}

마이크로소프트는 2010년에 Windows 2000의 지원을 중단했습니다.
이는 예외 처리(Unix 용어로 신호)와 관련된 [구현상의 어려움](https://codereview.appspot.com/74790043) 때문에, Go 1.3 버전에서는 Go에서도 지원되지 않습니다.

### DragonFly BSD 지원 {#dragonfly}

```
# 지원 대상
* DragonFly BSD
```

Go 1.3은 이제 `amd64` (64비트 x86) 및 `386` (32비트 x86) 아키텍처에서 DragonFly BSD에 대한 실험적인 지원을 포함합니다.
DragonFly BSD 3.6 이상을 사용합니다.

### FreeBSD 지원 {#freebsd}

이것은 당시 발표되지 않았지만, Go 1.2 이후부터 FreeBSD에서 Go를 사용하려면 FreeBSD 8 또는 그 이상이 필요합니다.

Go 1.3 버전부터, FreeBSD에서 Go를 사용하려면 커널이 `COMPAT_FREEBSD32` 플래그로 구성되어 있어야 합니다.

EABI 시스템 호출을 ARM 플랫폼에 사용하는 것과 함께, Go 1.3은 FreeBSD 10에서만 실행됩니다.
x86 플랫폼(386 및 amd64)은 영향을 받지 않습니다.

### 네이티브 클라이언트 지원 {#nacl}

1.3 릴리스부터 Native Client 가상 머신 아키텍처에 대한 지원이 Go로 돌아왔습니다.
32비트 Intel 아키텍처(`GOARCH=386`)와 64비트 Intel 아키텍처에서도 실행됩니다.
그러나 32비트 포인터를 사용합니다(`GOARCH=amd64p32`).
현재 ARM 아키텍처에 대한 Native Client 지원은 없습니다.
참고: 이것은 Native Client (NaCl)입니다, Portable Native Client (PNaCl)가 아닙니다.
Native Client에 대한 자세한 내용은 [여기](https://developers.google.com/native-client/dev/)를 참조하세요.
Go 버전을 설정하는 방법은 [여기](/wiki/NativeClient)에서 설명합니다.

### NetBSD 지원 {#netbsd}

Go 1.3 버전부터 NetBSD에서 Go를 사용하려면 NetBSD 6.0 이상 버전이 필요합니다.

### OpenBSD 지원 {#openbsd}

Go 1.3 버전부터 OpenBSD 지원을 위해서는 OpenBSD 5.5 버전 이상이 필요합니다.

### Plan 9 지원 {#plan9}

```
# Plan 9 지원

Go 1.3는 `386` (32비트 x86) 아키텍처에서 Plan 9에 대한 실험적인 지원을 포함합니다.
이는 `Tsemacquire` 시스템 호출을 필요로 하며, 이는 Plan 9에서 2012년 6월부터 사용 가능했습니다.

### Solaris 지원 {#solaris}

Go 1.3 버전에서는 `amd64` (64비트 x86) 아키텍처에서 Solaris에 대한 실험적인 지원이 포함됩니다.
illumos, Solaris 11 이상이 필요합니다.

## 메모리 모델 변경 사항 {#memory}

```
// Example Go code
package main

import "fmt"

func main() {
    fmt.Println("Hello, world!")
}
```

## 테이블 예시

| 헤더 1 | 헤더 2 | 헤더 3 |
|---|---|---|
| 데이터 1 | 데이터 2 | 데이터 3 |
| 데이터 4 | 데이터 5 | 데이터 6 |

## 목록 예시

- 항목 1
- 항목 2
- 항목 3

Go 1.3 메모리 모델 [새 규칙](https://codereview.appspot.com/75130045)을 추가하여, 버퍼된 채널을 통한 송수신에 대한 내용을 명확히 합니다.
이를 통해 버퍼된 채널을 간단한 세마포로 사용할 수 있음을 명시하며, 채널로 전송하여 획득하고, 채널에서 수신하여 해제하는 방식으로 작동합니다.
이는 언어 변경이 아니며, 통신에 대한 예상되는 속성에 대한 설명입니다.

## 구현 및 도구에 대한 변경 사항 {#impl}

이 섹션에서는 구현 및 관련 도구의 변경 사항에 대한 정보를 제공합니다.

### 스택 {#stacks}

Go 1.3은 기존의 "분할" 모델에서 연속적인 모델로 goroutine 스택의 구현을 변경했습니다.
goroutine이 사용할 수 있는 스택보다 더 많은 스택 공간이 필요할 때, 해당 스택은 더 큰 단일 메모리 블록으로 이동됩니다.
이 이동 작업의 오버헤드는 잘 분산되어 있으며, 계산이 반복적으로 섹먼트 경계를 건너뛸 때 발생하는 이전의 "핫 스팟" 문제를 제거합니다.
성능 수치와 같은 자세한 내용은 다음 [설계 문서]( /s/contigstacks)에서 확인할 수 있습니다.

### 가비지 컬렉터 변경 사항 {#garbage_collector}

오랫동안, 가비지 컬렉터는 힙 내의 값들을 정확하게 검사해 왔습니다. Go 1.3 버전은 스택 내의 값에도 동일한 정확도를 추가합니다.
이는 포인터가 아닌 Go 값, 예를 들어 정수가 포인터로 오인되지 않도록 하고, 사용되지 않는 메모리가 회수되는 것을 방지합니다.

Go 1.3부터 런타임은 포인터 유형의 값에는 포인터가 포함되어 있고, 다른 값에는 포함되어 있지 않다고 가정합니다.
이 가정은 스택 확장 및 가비지 컬렉션의 정확한 동작에 필수적입니다.
[package unsafe](/pkg/unsafe/)를 사용하여 정수를 포인터 유형의 값에 저장하는 프로그램은 불법이며, 런타임이 이러한 동작을 감지하면 충돌합니다.
[package unsafe](/pkg/unsafe/)를 사용하여 정수를 정수 유형의 값에 저장하는 프로그램도 불법이지만, 실행 중에 진단하기가 더 어렵습니다.
포인터가 런타임에서 숨겨져 있기 때문에, 스택 확장 또는 가비지 컬렉션이 해당 포인터를 가리키는 메모리를 회수하여
[dangling pointers](https://en.wikipedia.org/wiki/Dangling_pointer)를 생성할 수 있습니다.

_업데이트_: `unsafe.Pointer`를 사용하여 메모리에 있는 정수형 값을 포인터로 변환하는 코드는 불법이며 수정해야 합니다.
이러한 코드는 `go vet`를 사용하여 식별할 수 있습니다.

### 맵 순회 {#map}

작은 맵에 대한 반복이 더 이상 일관된 순서로 이루어지지 않습니다.
Go 1은 "[맵 반복 순서는 지정되지 않으며, 한 반복에서 다음 반복으로 변경될 때 동일하지 않을 수 있습니다.](/ref/spec#For_statements)"를 정의합니다.
맵 반복 순서에 의존하는 코드를 방지하기 위해,
Go 1.0은 맵 내의 임의의 인덱스에서 맵 반복을 시작했습니다.
Go 1.1에서 도입된 새로운 맵 구현은 8개 이하의 항목을 가진 맵에 대한 반복 순서를 무작위화하지 않았습니다. 그러나 맵 반복 순서는 여전히 시스템마다 다를 수 있습니다.
이는 사람들이 Go 1.1 및 Go 1.2 프로그램을 작성하여 작은 맵 반복 순서에 의존하게 되었으며, 따라서 특정 시스템에서만 안정적으로 작동할 수 있도록 했습니다.
Go 1.3은 이러한 버그를 해결하기 위해 작은 맵에 대한 무작위 반복을 다시 도입했습니다.

_업데이트_: 만약 코드가 작은 맵에 대해 고정된 반복 순서를 가정한다면,
이는 오류를 발생시키므로 코드를 수정하여 해당 가정을 제거해야 합니다.
왜냐하면, 이 문제는 주로 작은 맵에만 발생하기 때문입니다.

### 링크 편집기 {#liblink}

일반적인 [개편](/s/go13linker)의 일부로, Go 링커와 컴파일러가 재구조화되었습니다.
링커는 여전히 C 프로그램이지만, 이제 링커의 일부였던 인스트럭션 선택 단계가 `liblink`라는 새로운 라이브러리를 통해 컴파일러로 이동되었습니다.
이렇게 하면 패키지를 처음 컴파일할 때 인스트럭션 선택을 한 번만 수행함으로써, 대규모 프로젝트의 컴파일 속도를 크게 향상시킬 수 있습니다.

_업데이트_: 이 변경은 내부적으로 중요한 변경이지만, 프로그램에는 영향을 미치지 않아야 합니다.

### gccgo의 상태 {#gccgo}

GCC 4.9 버전에는 Go 1.2 (1.3이 아닌) 버전의 gccgo가 포함됩니다.
GCC 및 Go 프로젝트의 릴리스 일정은 일치하지 않으므로,
1.3 버전은 개발 브랜치에서 사용할 수 있지만,
다음 GCC 릴리스인 4.10 버전에는 Go 1.4 버전의 gccgo가 포함될 가능성이 높습니다.

### `go` 명령어의 변경 사항 {#gocmd}

[`cmd/go`](/cmd/go/) 명령어는 여러 가지 새로운 기능을 제공합니다.
`go run` 및 `go test` 하위 명령어는 결과 바이너리를 실행하는 대체 방법을 지정하는 새로운 `-exec` 옵션을 지원합니다.
이 옵션의 즉각적인 목적은 NaCl을 지원하는 것입니다.

`go test` 명령어의 테스트 커버리지 지원 기능은 이제 레이스 감지기가 활성화될 때 자동으로 커버리지 모드를 `-atomic`으로 설정합니다. 이를 통해, 커버리지 카운터에 대한 안전하지 않은 접근에 대한 오탐을 방지합니다.

[`go test`](/cmd/go/) 서브명령어
이제 항상 패키지를 빌드합니다. 테스트 파일이 없더라도 그렇습니다.
이전에는 테스트 파일이 없으면 아무 작업도 수행하지 않았습니다.

[`go build`](/cmd/go/) 명령어는 지정된 대상에 대한 종속성을 설치할 수 있는 새로운 `-i` 옵션을 지원합니다. 하지만 대상 자체는 설치할 수 없습니다.

`[cgo](https://cmd/cgo/)`을 사용하여 크로스 컴파일이 이제 지원됩니다.
`all.bash`를 실행할 때 `CC_FOR_TARGET` 및 `CXX_FOR_TARGET` 환경 변수를 사용하여 C 및 C++ 코드에 대한 크로스 컴파일러를 지정합니다.

마지막으로, `go` 명령은 이제 `cgo`를 통해 Objective-C 파일을 가져오는 패키지를 지원합니다 (확장자 `.m`).

### cgo 변경 사항 {#cgo}

명령 [`cmd/cgo`](/cmd/cgo/),
이 명령어는 Go 패키지에서 `import "C"` 선언을 처리하며,
심각한 버그를 수정하여 일부 패키지가 더 이상 컴파일되지 않는 문제를 해결했습니다.
이전 버전에서는 모든 불완전한 구조 유형에 대한 포인터가 Go 유형 `*[0]byte`로 변환되었으며,
이를 통해 Go 컴파일러는 한 유형의 구조 포인터를 다른 유형의 함수에 전달하는 것을 감지할 수 없었습니다.
Go 1.3은 이 오류를 수정하여 각 다른 불완전한 구조 유형을 서로 다른 이름이 지정된 유형으로 변환합니다.

주어진 C 선언 `typedef struct S T`는 불완전한 `struct S`에 대한 것이며,
일부 Go 코드는 이 버그를 이용하여 `C.struct_S`와 `C.T`를 상호 교환적으로 참조했습니다.
Cgo는 이제 이 사용을 명시적으로 허용하며, 완료된 struct 타입에 대해서도 그렇습니다.
그러나 일부 Go 코드는 또한 이 버그를 사용하여 (예를 들어) `*C.FILE`을 한 패키지에서 다른 패키지로 전달했습니다.
이는 불법적이며 더 이상 작동하지 않습니다: 일반적으로 Go 패키지는 API에서 C 타입과 이름을 노출하는 것을 피해야 합니다.

_업데이트_: 코드가 불완전한 타입으로의 혼동적인 포인터 사용 또는
패키지 경계를 넘어 전달하는 경우 더 이상 컴파일되지 않으며
새로 작성해야 합니다.
변환이 정확하고 유지해야 하는 경우, `[unsafe.Pointer](pkg/unsafe/#Pointer)`를 사용하여
명시적인 변환을 사용하십시오.

### SWIG 3.0이 필요합니다 (SWIG 관련) {#swig}

Go 프로그램에서 SWIG를 사용하는 경우, SWIG 버전 3.0이 이제 필요합니다.
`cmd/go` 명령은 이제 SWIG가 생성한 오브젝트 파일을 직접 바이너리에 링크합니다. 공유 라이브러리를 빌드하고 링크하는 대신.

### 명령줄 플래그 파싱 {#gc_flag}

```go
package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	// 플래그 정의
	var (
		name    string
		age     int
		verbose bool
	)

	// 플래그 파싱
	flag.StringVar(&name, "name", "default_name", "사용자 이름")
	flag.IntVar(&age, "age", 0, "사용자 나이")
	flag.BoolVar(&verbose, "verbose", false, "상세 정보 표시 여부")

	// 파싱된 플래그 출력
	fmt.Printf("Name: %s\n", name)
	fmt.Printf("Age: %d\n", age)
	fmt.Printf("Verbose: %t\n", verbose)

	// 셸에서 실행했을 때
	if len(os.Args) > 1 {
		// 첫 번째 인수를 플래그로 사용
		flag.Set("name", os.Args[1])
		flag.Set("age", os.Args[2]) // 2번째 인수를 age 플래그로 사용
		flag.Set("verbose", true) // 3번째 인수를 verbose 플래그로 사용, 또는 false로 설정
		fmt.Printf("Name: %s\n", name)
		fmt.Printf("Age: %d\n", age)
		fmt.Printf("Verbose: %t\n", verbose)
	}
}
```

gc 툴 체인에서, 어셈블러는 이제 Go 플래그 패키지와 동일한 명령줄 플래그 파싱 규칙을 사용합니다. 이는 전통적인 유닉스 플래그 파싱 방식과 다릅니다.
이는 도구를 직접 호출하는 스크립트에 영향을 줄 수 있습니다.
예를 들어,
`go tool 6a -SDfoo`는 이제 `go tool 6a -S -D foo`로 작성해야 합니다.
(동일한 변경 사항은 [Go 1.1](/doc/go1.1#gc_flag)의 컴파일러 및 링커에도 적용되었습니다.)

### godoc 변경 사항 {#godoc}

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, world!")
}
```

`-analysis` 플래그로 호출될 때,
[godoc](https://godoc.org/golang.org/x/tools/cmd/godoc)
이제 인덱싱된 코드에 대한 정교한 정적 분석을 수행합니다.
분석 결과는 소스 뷰와 패키지 문서 뷰 모두에서 표시되며, 각 패키지의 호출 그래프 및 정의와 참조, 유형과 해당 메서드, 인터페이스와 구현, 채널에 대한 송수신 작업, 함수와 호출자, 호출 위치와 호출 대상 간의 관계를 포함합니다.

### 기타 내용 {#misc}

프로그램 `misc/benchcmp`는 성능을 비교하는 기능을 제공하며, 이를 다시 작성했습니다.
이전에는 셸과 awk 스크립트로 구성되어 있었지만, 이제 `go.tools` 저장소에 있는 Go 프로그램으로 변경되었습니다.
문서는 [여기](https://godoc.org/golang.org/x/tools/cmd/benchcmp)에 있습니다.

몇몇 Go 배포판 개발자분들께, 도구 `misc/dist`는 이동 및 이름이 변경되었습니다. 이제 `misc/makerelease`에 위치하며, 여전히 메인 저장소에 있습니다.

## 성능 {#performance}

이 릴리스에서 Go 바이너의 성능이 여러 경우에 개선되었는데, 이는 런타임 및 가비지 컬렉션의 변경, 그리고 일부 라이브러리의 변경 때문입니다. 주요 개선 사항은 다음과 같습니다:

- 런타임은 `defer`를 더 효율적으로 처리하여, 각 `defer`를 호출하는 고루틴마다 약 2킬로바이트의 메모리 사용량을 줄입니다.
  - 가비지 컬렉터가 개선되어, 동시 sweep 알고리즘, 더 나은 병렬화 및 더 큰 페이지 크기를 사용합니다.
    이러한 효과로 인해 컬렉터 일시 중지 시간을 50-70% 줄일 수 있습니다.
  - Race detector ([이 가이드](/doc/articles/race_detector.html))가 약 40% 더 빠릅니다.
  - 정규 표현식 패키지 [`regexp`](/pkg/regexp/)가, 두 번째, 단일 패스 실행 엔진의 구현으로 인해 특정 간단한 표현식에 대해 훨씬 더 빠릅니다.
    어떤 엔진을 사용할지는 자동으로 선택됩니다.
    자세한 내용은 사용자에게 숨겨집니다.

또한, 런타임은 스택 덤프에 고루틴이 얼마나 블로킹되었는지 포함하여, 이를 통해 데드락 또는 성능 문제 해결에 유용한 정보를 얻을 수 있습니다.

## 표준 라이브러리의 변경 사항 {#library}

```
# Changelog
```

| 변경 사항 | 설명 |
|---|---|
| 새로운 기능 추가 | 새로운 기능을 라이브러리에 추가했습니다. |
| 버그 수정 | 버그를 수정했습니다. |
| 성능 개선 | 성능을 개선했습니다. |

```
## Contributing {#contributing}
```

```
# Contributing Guidelines
```

```
## Getting Started {#getting-started}
```

### 새로운 패키지 {#new_packages}

새로운 패키지 [`debug/plan9obj`](/pkg/debug/plan9obj/)가 표준 라이브러리에 추가되었습니다.
이는 Plan 9 [a.out](https://9p.io/magic/man2html/6/a.out) 객체 파일에 대한 접근을 구현합니다.

### 주요 라이브러리 변경 사항 {#major_library_changes}

*   이전 버전과의 호환성 문제가 해결되었습니다.
*   성능이 향상되었습니다.
*   새로운 기능이 추가되었습니다.

| 기능 | 설명 |
|---|---|
| 새로운 기능 | 설명 |
| 성능 향상 | 설명 |
| 호환성 문제 해결 | 설명 |

이전 [`crypto/tls`](/pkg/crypto/tls/) 버그로 인해 TLS에서 인증을 우회하는 것이 불의도적으로 가능했습니다.
Go 1.3에서는 이 버그가 수정되었습니다: 사용자는 ServerName 또는 InsecureSkipVerify 중 하나를 지정해야 하며, ServerName을 지정하면 이를 적용합니다.
이는 잘못된 방식으로 불확실한 동작에 의존하는 기존 코드를 손상시킬 수 있습니다.

표준 라이브러리에 중요한 새로운 유형이 추가되었습니다: [`sync.Pool`](/pkg/sync/#Pool).
이는 시스템이 자동으로 메모리를 회수할 수 있는 특정 유형의 캐시를 구현하는 효율적인 메커니즘을 제공합니다.

[`testing`](/pkg/testing/) 패키지의 벤치마킹 헬퍼,
[`B`](/pkg/testing/#B), 이제 `RunParallel` 메서드를 제공하여 여러 CPU를 활용하는 벤치마크를 더 쉽게 실행할 수 있습니다.

_업데이트_: crypto/tls 수정은 기존 코드를 손상시킬 수 있지만, 이러한 코드는 잘못되었으며 업데이트되어야 합니다.

### 라이브러리의 미세 조정 {#minor_library_changes}

다음 목록은 라이브러리의 여러 가지 작은 변경 사항을 요약합니다. 대부분이 추가 사항입니다.
각 변경 사항에 대한 자세한 내용은 관련 패키지 문서를 참조하십시오.

- 在 [`crypto/tls`](/pkg/crypto/tls/) 包中，
    一个新的 [`DialWithDialer`](/pkg/crypto/tls/#DialWithDialer)
    函数允许使用现有的拨号器建立 TLS 连接，这使得更容易
    控制拨号选项，如超时时间。
    该包现在还报告连接使用的 TLS 版本，
    在 [`ConnectionState`](/pkg/crypto/tls/#ConnectionState)
    结构中。
  - [`crypto/tls`](/pkg/crypto/tls/) 包中的 [`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate)
    函数现在支持解析 (以及其他地方的序列化) 的 PKCS #10 证书
    签名请求。
  - `fmt` 包中的格式化打印函数现在将 `%F` 定义为浮点值打印时等同于 `%f`。
  - [`math/big`](/pkg/math/big/) 包的
    [`Int`](/pkg/math/big/#Int) 和
    [`Rat`](/pkg/math/big/#Rat) 类型
    现在实现了
    [`encoding.TextMarshaler`](/pkg/encoding/#TextMarshaler) 和
    [`encoding.TextUnmarshaler`](/pkg/encoding/#TextUnmarshaler)。
  - 复杂求幂函数 [`Pow`](/pkg/math/cmplx/#Pow)，
    现在指定了第一个参数为零时的行为。
    此前未定义。
    详细信息请参见该函数的 [文档](/pkg/math/cmplx/#Pow)。
  - [`net/http`](/pkg/net/http/) 包现在在新的
    [`Response.TLS`](/pkg/net/http/#Response) 字段中
    暴露了用于进行客户端请求的 TLS 连接的属性。
  - [`net/http`](/pkg/net/http/) 包现在
    允许使用 [`Server.ErrorLog`](/pkg/net/http/#Server)
    设置可选的服务器错误日志记录器。
    默认情况下，所有错误仍然发送到 stderr。
  - [`net/http`](/pkg/net/http/) 包现在
    支持在服务器端禁用 HTTP 保持连接，
    使用 [`Server.SetKeepAlivesEnabled`](/pkg/net/http/#Server.SetKeepAlivesEnabled)。
    默认情况下，服务器仍然保持连接（为多个请求重用连接）。
    只有资源受限的服务器或正在优雅地关闭的服务器才会禁用它们。
  - [`net/http`](/pkg/net/http/) 包添加了一个可选
    [`Transport.TLSHandshakeTimeout`](/pkg/net/http/#Transport)
    设置，用于限制 HTTP 客户端请求等待 TLS 握手完成的时间。
    它现在默认设置为 [`DefaultTransport`](/pkg/net/http#DefaultTransport)。
  - [`net/http`](/pkg/net/http/) 包的
    [`DefaultTransport`](/pkg/net/http/#DefaultTransport)，
    用于 HTTP 客户端代码，现在默认启用 TCP
    保持连接([https://en.wikipedia.org/wiki/Keepalive#TCP_keepalive](https://en.wikipedia.org/wiki/Keepalive#TCP_keepalive))。
    其他具有 `Dial` 字段为 `nil` 的 [`Transport`](/pkg/net/http/#Transport) 值继续按以前的方式工作：不使用 TCP 保持连接。
  - [`net/http`](/pkg/net/http/) 包现在
    在使用 [`ListenAndServe`](/pkg/net/http/#ListenAndServe)
    或
    [`ListenAndServeTLS`](/pkg/net/http/#ListenAndServeTLS)
    时，启用 TCP
    保持连接([https://en.wikipedia.org/wiki/Keepalive#TCP_keepalive](https://en.wikipedia.org/wiki/Keepalive#TCP_keepalive))。
    当以其他方式启动服务器时，不启用 TCP 保持连接。
  - [`net/http`](/pkg/net/http/) 包现在
    提供了一个可选的 [`Server.ConnState`](/pkg/net/http/#Server)
    回调，用于连接生命周期的各种阶段。
    这可用于实现速率限制或优雅关闭。
  - [`net/http`](/pkg/net/http/) 包的 HTTP
    客户端现在具有一个可选的 [`Client.Timeout`](/pkg/net/http/#Client)
    字段，用于指定使用客户端的请求的终到超时。
  - [`net/http`](/pkg/net/http/) 包的
    [`Request.ParseMultipartForm`](/pkg/net/http/#Request.ParseMultipartForm)
    方法现在如果 `Content-Type`
    是 `multipart/form-data` 时将返回错误。
    在 Go 1.3 之前，它会默默地失败并返回 `nil`。
    依赖先前行为的代码应进行更新。
  - 在 [`net`](/pkg/net/) 包中，
    `Dialer` 结构现在具有一个 `KeepAlive` 选项，用于指定连接的保持时间。
  - [`net/http`](/pkg/net/http/) 包的
    `Transport`
    现在一致地关闭 [`Request.Body`](/pkg/net/http/#Request)，
    即使出错。
  - [`os/exec`](/pkg/os/exec/) 包现在实现了文档中关于二进制文件相对路径的说明。
    特别是，只有当二进制文件名不包含路径分隔符时，才会调用 [`LookPath`](/pkg/os/exec/#LookPath)。
  - [`reflect`](/pkg/reflect/) 包中的 [`SetMapIndex`](/pkg/reflect/#Value.SetMapIndex)
    函数现在不再在删除 `nil` 映射时引发错误。
  - 如果主 goroutine 调用
    [`runtime.Goexit`](/pkg/runtime/#Goexit)
    并且所有其他 goroutine 完成执行，则该程序现在始终崩溃，并报告检测到的死锁。
    较早版本的 Go 以不一致的方式处理这种情况：大多数实例报告为死锁，但一些简单的用例会干净地退出。
  - `runtime/debug` 包现在具有一个新的函数
    [`debug.WriteHeapDump`](/pkg/runtime/debug/#WriteHeapDump)
    ，该函数将写入堆描述。
  - [`strconv`](/pkg/strconv/) 包中的 [`CanBackquote`](/pkg/strconv/#CanBackquote)
    函数现在将 `DEL` 字符 (U+007F) 视为非打印字符。
  - [`syscall`](/pkg/syscall/) 包现在提供了 [`SendmsgN`](/pkg/syscall/#SendmsgN)
    作为 [`Sendmsg`](/pkg/syscall/#Sendmsg)
    的替代版本，该版本返回写入的字节数。
  - 在 Windows 上，[`syscall`](/pkg/syscall/) 包现在支持通过添加一个新的函数
    [`NewCallbackCDecl`](/pkg/syscall/#NewCallbackCDecl)
    以及现有的函数
    [`NewCallback`](/pkg/syscall/#NewCallback)。
  - [`testing`](/pkg/testing/) 包现在诊断调用 `panic(nil)` 的测试，这些测试几乎总是错误的。
    此外，测试即使在失败的情况下也会写入配置文件。
  - [`unicode`](/pkg/unicode/) 包和相关支持在整个系统中的升级为 Unicode 6.3.0。
