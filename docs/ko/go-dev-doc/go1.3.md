## Go 1.3 소개 {#introduction}

최신 Go 릴리스인 버전 1.3은 1.2 출시 6개월 후에 나왔으며, 언어 자체의 변경 사항은 없습니다.
이번 버전은 주로 구현 작업에 집중하여 다음과 같은 내용을 제공합니다:
정밀한 가비지 컬렉션(precise garbage collection),
특히 대규모 프로젝트에서 빌드 속도를 높여주는 컴파일러 툴체인의 대대적인 리팩토링,
전반적인 성능의 유의미한 향상,
그리고 DragonFly BSD, Solaris, Plan 9 및 Google의 Native Client 아키텍처(NaCl) 지원입니다.
또한 동기화와 관련된 메모리 모델의 중요한 개선 사항이 포함되었습니다.
언제나 그렇듯, Go 1.3은 [호환성 약속](/doc/go1compat.html)을 준수하며,
거의 모든 코드가 1.3으로 이동 시 변경 없이 그대로 컴파일되고 실행될 것입니다.

## 지원되는 운영 체제 및 아키텍처 변경 사항 {#os}

### Windows 2000 지원 중단 {#win2000}

Microsoft는 2010년에 Windows 2000에 대한 지원을 중단했습니다.
예외 처리(Unix 용어로 시그널)와 관련된 [구현상의 어려움](https://codereview.appspot.com/74790043)이 있기 때문에,
Go 1.3부터는 Go에서도 지원되지 않습니다.

### DragonFly BSD 지원 {#dragonfly}

Go 1.3는 이제 `amd64` (64-bit x86) 및 `386` (32-bit x86) 아키텍처에서 DragonFly BSD에 대한 실험적 지원을 포함합니다.
이 기능은 DragonFly BSD 3.6 이상 버전을 사용합니다.

### FreeBSD 지원 {#freebsd}

당시에는 발표되지 않았으나, Go 1.2 릴리스 이후로 FreeBSD에서의 Go 지원은 FreeBSD 8 버전 이상을 요구합니다.

Go 1.3부터 FreeBSD에서 Go를 지원하려면 커널이 `COMPAT_FREEBSD32` 플래그가 설정된 상태로 컴파일되어야 합니다.

ARM 플랫폼의 EABI syscall 전환에 맞춰, Go 1.3은 FreeBSD 10에서만 실행됩니다.
x86 플랫폼인 386 및 amd64는 영향을 받지 않습니다.

### Native Client 지원 {#nacl}

Native Client 가상 머신 아키텍처에 대한 지원이 Go 1.3 릴리스와 함께 다시 추가되었습니다.
이 기능은 32비트 Intel 아키텍처(`GOARCH=386`) 및 64비트 Intel에서 32비트 포인터를 사용하는 경우(`GOARCH=amd64p32`)에 실행됩니다.
ARM에서의 Native Client 지원은 아직 제공되지 않습니다.
이는 Portable Native Client (PNaCl)가 아니라 Native Client (NaCl)임에 유의하십시오.
Native Client에 대한 자세한 내용은 [여기](https://developers.google.com/native-client/dev/)에서, Go 버전 설정 방법은 [여기](/wiki/NativeClient)에서 확인할 수 있습니다.

### NetBSD 지원 {#netbsd}

Go 1.3부터 NetBSD의 Go 지원은 NetBSD 6.0 이상 버전을 필요로 합니다.

### OpenBSD 지원 {#openbsd}

Go 1.3부터 OpenBSD에서 Go를 지원하려면 OpenBSD 5.5 이상 버전이 필요합니다.

### Plan 9 지원 {#plan9}

Go 1.3는 이제 `386` (32비트 x86) 아키텍처의 Plan 9에 대한 실험적 지원을 포함합니다.
이를 위해서는 2012년 6월부터 Plan 9에 도입된 `Tsemacquire` syscall이 필요합니다.

### Solaris 지원 {#solaris}

Go 1.3에는 이제 `amd64` (64비트 x86) 아키텍처의 Solaris에 대한 실험적 지원이 포함됩니다.
illumos, Solaris 11 또는 그 이상의 버전이 필요합니다.

## 메모리 모델의 변경 사항 {#memory}

Go 1.3 메모리 모델은 [새로운 규칙을 추가하여](https://codereview.appspot.com/75130045)
버퍼드 채널(buffered channels)의 송신과 수신에 관한 내용을 다룹니다.
이는 버퍼드 채널을 단순한 세마포어(semaphore)로 사용할 수 있음을 명시적으로 하기 위함이며,
채널로의 송신을 통해 획득(acquire)하고, 채널로부터의 수신을 통해 해제(release)하는 방식입니다.
이것은 언어적 변경 사항이 아니며, 통신의 예상되는 속성에 대한 명확한 설명일 뿐입니다.

## 구현 및 도구의 변경 사항 {#impl}

### Stack {#stacks}

Go 1.3에서는 goroutine 스택의 구현 방식이 기존의 "segmented" 모델에서 연속적인(contiguous) 모델로 변경되었습니다. goroutine에 가용 가능한 것보다 더 많은 스택이 필요할 때, 해당 스택은 더 큰 단일 메모리 블록으로 이동됩니다. 이러한 전송 작업의 오버헤드는 충분히 분산되며, 계산이 세그먼트 경계를 반복적으로 넘나들 때 발생하던 기존의 "hot spot" 문제를 해결합니다. 성능 수치를 포함한 자세한 내용은 이 [설계 문서](/s/contigstacks)에서 확인할 수 있습니다.

### 가비지 컬렉터 변경 사항 {#garbage_collector}

한동안 가비지 컬렉터는 힙의 값을 검사할 때 _정밀(precise)_하게 동작해 왔으며, Go 1.3 릴리스에서는 스택의 값에 대해서도 동일한 정밀도가 추가되었습니다. 이는 정수와 같은 포인터가 아닌 Go 값이 포인터로 오인되어 사용되지 않는 메모리가 회수되는 것을 방해하는 일이 더 이상 발생하지 않음을 의미합니다.

Go 1.3부터 런타임은 포인터 타입의 값은 포인터를 포함하고, 그 외의 값은 포함하지 않는다고 가정합니다.
이 가정은 스택 확장(stack expansion)과 가비지 컬렉션(garbage collection) 모두의 정확한 동작에 있어 매우 근본적인 요소입니다.
[package unsafe](/pkg/unsafe/)를 사용하여 포인터 타입의 값에 정수를 저장하는 프로그램은 허용되지 않으며, 런타임이 이러한 동작을 감지하면 크래시가 발생합니다.
[package unsafe](/pkg/unsafe/)를 사용하여 정수 타입의 값에 포인터를 저장하는 프로그램 또한 허용되지 않지만, 실행 중에 진단하기는 더 어렵습니다.
포인터가 런타임에 숨겨져 있기 때문에, 스택 확장이나 가비지 컬렉션 과정에서 해당 포인터가 가리키는 메모리를 회수할 수 있으며, 이로 인해 [dangling pointers](https://en.wikipedia.org/wiki/Dangling_pointer)가 생성될 수 있습니다.

_업데이트_: 메모리에 저장된 정수 타입 값을 포인터로 변환하기 위해 `unsafe.Pointer`를 사용하는 코드는 허용되지 않으며 반드시 수정되어야 합니다. 이러한 코드는 `go vet`을 통해 식별할 수 있습니다.

### 맵 반복문 {#map}

작은 크기의 맵(map)에 대한 반복(iteration)이 더 이상 일관된 순서로 발생하지 않습니다.

Go 1에서는 “[맵에 대한 반복 순서는 지정되지 않았으며, 한 번의 반복에서 다음 반복으로 동일함이 보장되지 않습니다.](/ref/spec#For_statements)”라고 정의합니다.

코드 내부에서 맵 반복 순서에 의존하는 것을 방지하기 위해, Go 1.0은 각 맵 반복을 맵의 무작위 인덱스에서 시작하도록 했습니다.

Go 1.1에서 도입된 새로운 맵 구현에서는 항목이 8개 이하인 맵에 대해 반복 무작위화를 누락했습니다. 비록 반복 순서가 시스템마다 다를 수는 있지만 말입니다.

이로 인해 일부 사용자들이 작은 맵의 반복 순서에 의존하는 Go 1.1 및 Go 1.2 프로그램을 작성하게 되었고, 결과적으로 특정 시스템에서만 안정적으로 작동하는 코드가 만들어졌습니다.

Go 1.3에서는 이러한 버그들을 찾아내어 해결하기 위해 작은 맵에 대해서도 무작위 반복을 다시 도입합니다.

_업데이트_: 코드에서 작은 맵(map)의 반복 순서가 고정되어 있다고 가정하는 경우, 해당 코드는 작동하지 않게 되며 그러한 가정을 하지 않도록 다시 작성해야 합니다. 작은 맵만 영향을 받기 때문에, 이 문제는 테스트에서 가장 자주 발생합니다.

### 링커 (The linker) {#liblink}

Go 링커의 전반적인 [개편](/s/go13linker)의 일환으로, 컴파일러와 링커가 리팩토링되었습니다. 링커는 여전히 C 프로그램이지만, 기존에 링커의 일부였던 명령어 선택(instruction selection) 단계가 `liblink`라는 새로운 라이브러리의 생성을 통해 컴파일러로 이동되었습니다. 패키지가 처음 컴파일될 때 명령어 선택을 한 번만 수행함으로써, 대규모 프로젝트의 컴파일 속도를 상당히 높일 수 있습니다.

_업데이트_: 이는 내부적인 큰 변경 사항이지만, 프로그램에는 아무런 영향을 미치지 않아야 합니다.

### gccgo의 상태 {#gccgo}

GCC 릴리스 4.9에는 gccgo의 Go 1.2(1.3 아님) 버전이 포함될 예정입니다.
GCC와 Go 프로젝트의 릴리스 일정은 서로 일치하지 않으며,
이는 1.3 버전이 개발 브랜치(development branch)에서는 제공되지만,
다음 GCC 릴리스인 4.10에는 gccgo의 Go 1.4 버전이 포함될 가능성이 높다는 것을 의미합니다.

### go 명령어의 변경 사항 {#gocmd}

[`cmd/go`](/cmd/go/) 명령에 여러 새로운 기능이 추가되었습니다.
[`go run`](/cmd/go/) 및 [`go test`](/cmd/go/) 하위 명령은 결과 바이너리를 실행하는 대체 방법을 지정할 수 있는 새로운 `-exec` 옵션을 지원합니다.
이 옵션의 즉각적인 목적은 NaCl을 지원하는 것입니다.

[`go test`](/cmd/go/) 하위 명령의 테스트 커버리지 지원 기능은 이제 레이스 검출기(race detector)가 활성화되었을 때 커버리지 모드를 자동으로 `-atomic`으로 설정하여, 커버리지 카운터에 대한 안전하지 않은 접근과 관련된 잘못된 보고를 제거합니다.

[`go test`](/cmd/go/) 하위 명령어가 이제 테스트 파일이 없더라도 항상 패키지를 빌드합니다.
이전에는 테스트 파일이 없으면 아무 작업도 수행하지 않았습니다.

[`go build`](/cmd/go/) 하위 명령어는
지정된 타겟 자체가 아닌, 해당 타겟의 종속성을
설치하기 위한 새로운 `-i` 옵션을 지원합니다.

[`cgo`](/cmd/cgo/)가 활성화된 상태에서의 교차 컴파일(Cross compiling)이 이제 지원됩니다.
`all.bash`를 실행할 때 C 및 C++ 코드에 대한 교차 컴파일러를 각각 지정하려면 `CC_FOR_TARGET` 및 `CXX_FOR_TARGET` 환경 변수를 사용합니다.

마지막으로, 이제 `go` 명령어가 cgo를 통해 Objective-C 파일(`.m` 확장자)을 임포트하는 패키지를 지원합니다.

### cgo 변경 사항 {#cgo}

Go 패키지에서 `import "C"` 선언을 처리하는 [`cmd/cgo`](/cmd/cgo/) 명령에서
일부 패키지의 컴파일이 중단될 수 있는 심각한 버그가 수정되었습니다.
이전에는 불완전한 구조체 타입(incomplete struct types)에 대한 모든 포인터가 Go 타입 `*[0]byte`로 변환되어,
Go 컴파일러가 다른 구조체 포인터를 기대하는 함수에 엉뚱한 종류의 구조체 포인터를 전달하는 것을 진단할 수 없는 문제가 있었습니다.
Go 1.3에서는 각 서로 다른 불완전한 구조체를 서로 다른 이름이 지정된 타입으로 변환함으로써 이 오류를 수정했습니다.

불완전한 `struct S`에 대해 `typedef struct S T`라는 C 선언이 있을 때, 일부 Go 코드는 이 버그를 이용해 `C.struct_S`와 `C.T` 타입을 서로 혼용하여 참조했습니다.
이제 Cgo는 완료된 구조체 타입에 대해서도 이러한 사용을 명시적으로 허용합니다.
하지만 일부 Go 코드는 이 버그를 이용해 (예를 들어) `*C.FILE`을 한 패키지에서 다른 패키지로 전달하기도 했습니다.
이는 적법하지 않으며 더 이상 작동하지 않습니다. 일반적으로 Go 패키지는 API에서 C 타입과 이름을 노출하는 것을 피해야 합니다.

_업데이트_: 불완전한 타입(incomplete types)을 가리키는 포인터를 사용하거나 이를 패키지 경계를 넘어 전달하는 혼동스러운 코드는 더 이상 컴파일되지 않으며, 반드시 다시 작성해야 합니다.
만약 변환이 정확하며 이를 유지해야 하는 경우에는 [`unsafe.Pointer`](/pkg/unsafe/#Pointer)를 통한 명시적 변환을 사용하십시오.

### SWIG를 사용하는 프로그램에는 SWIG 3.0이 필요합니다 {#swig}

SWIG를 사용하는 Go 프로그램의 경우, 이제 SWIG 버전 3.0이 필요합니다.
[`cmd/go`](/cmd/go) 명령은 이제 공유 라이브러리로 빌드하고 링크하는 대신, SWIG가 생성한 오브젝트 파일들을 바이너리에 직접 링크합니다.

### 커맨드라인 플래그 파싱 {#gc_flag}

gc 툴체인에서 어셈블러는 이제 전통적인 Unix 플래그 파싱 방식에서 벗어나 Go `flag` 패키지와 동일한 커맨드라인 플래그 파싱 규칙을 사용합니다.

이 변경 사항은 툴을 직접 호출하는 스크립트에 영향을 줄 수 있습니다.
예를 들어,
`go tool 6a -SDfoo`는 이제
`go tool 6a -S -D foo`로 작성해야 합니다.
(동일한 변경 사항이 [Go 1.1](/doc/go1.1#gc_flag)의 컴파일러와 링커에도 적용되었습니다.)

### godoc 변경 사항 {#godoc}

`-analysis` 플래그와 함께 호출하면,
[godoc](https://godoc.org/golang.org/x/tools/cmd/godoc)
은 이제 인덱싱하는 코드에 대해 정교한 정적 분석을 수행합니다.
분석 결과는 소스 뷰와 패키지 문서 뷰 모두에 표시되며, 다음 내용을 포함합니다:
각 패키지의 호출 그래프(call graph)와
정의(definition)와 참조(reference) 사이의 관계,
타입(type)과 해당 메서드(method) 사이의 관계,
인터페이스(interface)와 그 구현체(implementation) 사이의 관계,
채널의 송신(send) 및 수신(receive) 작업,
함수와 해당 함수를 호출하는 호출자(caller), 그리고
호출 지점(call site)과 호출 대상(callee) 사이의 관계.

### 기타 {#misc}

벤치마킹 실행 간의 성능을 비교하는 `misc/benchcmp` 프로그램이 다시 작성되었습니다.
기존에는 메인 리포지토리의 셸 및 awk 스크립트였으나, 이제 `go.tools` 리포지토리의 Go 프로그램으로 변경되었습니다.
문서 내용은 [여기](https://godoc.org/golang.org/x/tools/cmd/benchcmp)에서 확인하실 수 있습니다.

Go 배포판을 빌드하시는 소수의 사용자분들께 알립니다. `misc/dist` 도구가 이동 및 이름 변경되었습니다. 이제 메인 저장소 내의 `misc/makerelease`에서 확인하실 수 있습니다.

## 성능 {#performance}

이번 릴리스의 Go 바이너리 성능은 런타임과 가비지 컬렉션의 변경 사항 및 일부 라이브러리 수정으로 인해 많은 경우에서 향상되었습니다.
주요 사례는 다음과 같습니다:

- 런타임이 `defer`를 더 효율적으로 처리하여, `defer`를 호출하는 고루틴당 메모리 사용량이 약 2킬로바이트 감소했습니다.
  - 가비지 컬렉터가 동시 스윕(concurrent sweep) 알고리즘, 향상된 병렬 처리, 더 큰 페이지를 사용하여 속도가 빨라졌습니다.
    그 결과 컬렉터 일시 정지 시간이 50-70% 감소할 수 있습니다.
  - 레이스 디텍터([이 가이드](/doc/articles/race_detector.html) 참조)의 속도가 약 40% 향상되었습니다.
  - 정규 표현식 패키지 [`regexp`](/pkg/regexp/)에 두 번째 원패스(one-pass) 실행 엔진이 구현되어, 특정 단순 표현식에 대한 처리 속도가 상당히 빨라졌습니다.
    어떤 엔진을 사용할지는 자동으로 결정되며, 세부 사항은 사용자에게 숨겨져 있습니다.

또한, 이제 런타임의 스택 덤프에 고루틴이 얼마나 오랫동안 차단(blocked)되었는지가 포함되며, 이는 데드락이나 성능 문제를 디버깅할 때 유용한 정보가 될 수 있습니다.

## 표준 라이브러리 변경 사항 {#library}

### 새 패키지 {#new_packages}

표준 라이브러리에 새로운 패키지 [`debug/plan9obj`](/pkg/debug/plan9obj/)가 추가되었습니다.
이 패키지는 Plan 9 [a.out](https://9p.io/magic/man2html/6/a.out) 오브젝트 파일에 대한 액세스를 구현합니다.

### 라이브러리의 주요 변경 사항 {#major_library_changes}

[`crypto/tls`](/pkg/crypto/tls/)의 이전 버그로 인해 TLS 검증을 의도치 않게 건너뛰는 것이 가능했습니다.
Go 1.3에서 이 버그가 수정되었습니다. 이제 `ServerName` 또는 `InsecureSkipVerify` 중 하나를 반드시 지정해야 하며, `ServerName`이 지정된 경우 검증이 강제됩니다.
이로 인해 보안되지 않은 동작에 잘못 의존하고 있던 기존 코드가 작동하지 않을 수 있습니다.

표준 라이브러리에 중요한 새로운 타입인 [`sync.Pool`](/pkg/sync/#Pool)이 추가되었습니다.
이는 메모리를 시스템이 자동으로 회수할 수 있는 특정 유형의 캐시를 구현하기 위한 효율적인 메커니즘을 제공합니다.

[`testing`](/pkg/testing/) 패키지의 벤치마킹 헬퍼인
[`B`](/pkg/testing/#B)에 이제
[`RunParallel`](/pkg/testing/#B.RunParallel) 메서드가 추가되어,
여러 CPU를 사용하는 벤치마크를 더 쉽게 실행할 수 있습니다.

_업데이트_: `crypto/tls` 수정으로 인해 기존 코드가 작동하지 않을 수 있으나, 해당 코드는 잘못 작성된 것이므로 업데이트해야 합니다.

### 라이브러리의 소규모 변경 사항 {#minor_library_changes}

다음 목록은 라이브러리의 몇 가지 사소한 변경 사항(대부분 추가 사항)을 요약한 것입니다.
각 변경 사항에 대한 자세한 내용은 관련 패키지 문서를 참조하십시오.

- [`crypto/tls`](/pkg/crypto/tls/) 패키지에 새로운 [`DialWithDialer`](/pkg/crypto/tls/#DialWithDialer) 함수가 추가되어, 기존 다이얼러를 사용하여 TLS 연결을 설정할 수 있게 되었습니다. 이를 통해 타임아웃과 같은 다이얼 옵션을 더 쉽게 제어할 수 있습니다. 또한 이제 [`ConnectionState`](/pkg/crypto/tls/#ConnectionState) 구조체에서 연결에 사용된 TLS 버전을 보고합니다.
- [`crypto/tls`](/pkg/crypto/tls/) 패키지의 [`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate) 함수가 이제 PKCS #10 인증서 서명 요청의 파싱(및 다른 곳에서의 직렬화)을 지원합니다.
- `fmt` 패키지의 포맷팅 출력 함수에서 부동 소수점 값을 출력할 때 `%F`를 `%f`의 동의어로 정의합니다.
- [`math/big`](/pkg/math/big/) 패키지의 [`Int`](/pkg/math/big/#Int) 및 [`Rat`](/pkg/math/big/#Rat) 타입이 이제 [`encoding.TextMarshaler`](/pkg/encoding/#TextMarshaler) 및 [`encoding.TextUnmarshaler`](/pkg/encoding/#TextUnmarshaler)를 구현합니다.
- 복소수 거듭제곱 함수인 [`Pow`](/pkg/math/cmplx/#Pow)가 이제 첫 번째 인자가 0일 때의 동작을 명시합니다. 이전에는 정의되지 않았었습니다. 자세한 내용은 [함수 문서](/pkg/math/cmplx/#Pow)를 참조하십시오.
- [`net/http`](/pkg/net/http/) 패키지가 이제 클라이언트 요청을 만드는 데 사용된 TLS 연결의 속성을 새로운 [`Response.TLS`](/pkg/net/http/#Response) 필드에서 노출합니다.
- [`net/http`](/pkg/net/http/) 패키지에서 이제 [`Server.ErrorLog`](/pkg/net/http/#Server)를 통해 선택적으로 서버 오류 로거를 설정할 수 있습니다. 기본값은 여전히 모든 오류가 stderr로 전송되는 것입니다.
- [`net/http`](/pkg/net/http/) 패키지에서 이제 [`Server.SetKeepAlivesEnabled`](/pkg/net/http/#Server.SetKeepAlivesEnabled)를 사용하여 서버의 HTTP keep-alive 연결을 비활성화할 수 있습니다. 기본값은 여전히 서버가 keep-alive를 수행(여러 요청에 대해 연결을 재사용)하는 것입니다. 리소스가 제한적인 서버나 점진적 종료(graceful shutdown) 과정에 있는 서버만 이를 비활성화하고 싶을 것입니다.
- [`net/http`](/pkg/net/http/) 패키지에 선택적인 [`Transport.TLSHandshakeTimeout`](/pkg/net/http/#Transport) 설정이 추가되어, HTTP 클라이언트 요청이 TLS 핸드셰이크 완료까지 대기하는 최대 시간을 제한할 수 있습니다. 이제 [`DefaultTransport`](/pkg/net/http#DefaultTransport)에도 기본값으로 설정됩니다.
- HTTP 클라이언트 코드에서 사용하는 [`net/http`](/pkg/net/http/) 패키지의 [`DefaultTransport`](/pkg/net/http/#DefaultTransport)가 이제 기본적으로 [TCP keep-alives](https://en.wikipedia.org/wiki/Keepalive#TCP_keepalive)를 활성화합니다. `Dial` 필드가 nil인 다른 [`Transport`](/pkg/net/http/#Transport) 값들은 이전과 동일하게 작동하며, TCP keep-alives를 사용하지 않습니다.
- [`net/http`](/pkg/net/http/) 패키지에서 [`ListenAndServe`](/pkg/net/http/#ListenAndServe) 또는 [`ListenAndServeTLS`](/pkg/net/http/#ListenAndServeTLS)를 사용할 때 들어오는 서버 요청에 대해 [TCP keep-alives](https://en.wikipedia.org/wiki/Keepalive#TCP_keepalive)를 활성화합니다. 그 외의 방식으로 서버를 시작할 때는 TCP keep-alives가 활성화되지 않습니다.
- [`net/http`](/pkg/net/http/) 패키지에서 이제 서버 연결 수명 주기의 다양한 단계에 훅을 걸 수 있는 선택적인 [`Server.ConnState`](/pkg/net/http/#Server) 콜백을 제공합니다([`ConnState`](/pkg/net/http/#ConnState) 참조). 이는 속도 제한(rate limiting)이나 점진적 종료를 구현하는 데 사용될 수 있습니다.
- [`net/http`](/pkg/net/http/) 패키지의 HTTP 클라이언트에 이제 클라이언트를 사용하여 수행된 요청에 대해 엔드-투-엔드 타임아웃을 지정하는 선택적인 [`Client.Timeout`](/pkg/net/http/#Client) 필드가 추가되었습니다.
- [`net/http`](/pkg/net/http/) 패키지의 [`Request.ParseMultipartForm`](/pkg/net/http/#Request.ParseMultipartForm) 메서드는 이제 바디의 `Content-Type`이 `multipart/form-data`가 아니면 에러를 반환합니다. Go 1.3 이전에는 조용히 실패하고 `nil`을 반환했습니다. 이전 동작에 의존하는 코드는 업데이트해야 합니다.
- [`net`](/pkg/net/) 패키지에서 [`Dialer`](/pkg/net/#Dialer) 구조체에 연결의 keep-alive 기간을 지정하는 `KeepAlive` 옵션이 추가되었습니다.
- [`net/http`](/pkg/net/http/) 패키지의 [`Transport`](/pkg/net/http/#Transport)가 이제 에러 발생 시에도 일관되게 [`Request.Body`](/pkg/net/http/#Request)를 닫습니다.
- [`os/exec`](/pkg/os/exec/) 패키지가 이제 바이너리의 상대 경로와 관련하여 문서에 명시되어 있던 내용을 구현합니다. 특히, 바이너리의 파일 이름에 경로 구분자가 없을 때만 [`LookPath`](/pkg/os/exec/#LookPath)를 호출합니다.
- [`reflect`](/pkg/reflect/) 패키지의 [`SetMapIndex`](/pkg/reflect/#Value.SetMapIndex) 함수가 이제 `nil` 맵에서 요소를 삭제할 때 패닉을 일으키지 않습니다.
- 메인 고루틴이 [`runtime.Goexit`](/pkg/runtime/#Goexit)를 호출하고 다른 모든 고루틴이 실행을 마친 경우, 이제 프로그램은 항상 데드락이 감지되었음을 보고하며 충돌합니다. 이전 버전의 Go에서는 이 상황을 일관성 없게 처리했습니다. 대부분 데드락으로 보고되었으나, 일부 단순한 경우에는 깨끗하게 종료되었습니다.
- `runtime/debug` 패키지에 힙의 설명을 출력하는 새로운 함수 [`debug.WriteHeapDump`](/pkg/runtime/debug/#WriteHeapDump)가 추가되었습니다.
- [`strconv`](/pkg/strconv/) 패키지의 [`CanBackquote`](/pkg/strconv/#CanBackquote) 함수가 이제 `DEL` 문자(`U+007F`)를 출력 불가능한 문자로 간주합니다.
- [`syscall`](/pkg/syscall/) 패키지가 이제 작성된 바이트 수를 반환하는 [`Sendmsg`](/pkg/syscall/#Sendmsg)의 대체 버전인 [`SendmsgN`](/pkg/syscall/#SendmsgN)을 제공합니다.
- Windows에서 [`syscall`](/pkg/syscall/) 패키지가 기존의 [`NewCallback`](/pkg/syscall/#NewCallback) 함수와 더불어 새로운 [`NewCallbackCDecl`](/pkg/syscall/#NewCallbackCDecl) 함수를 추가하여 cdecl 호출 규약을 지원합니다.
- [`testing`](/pkg/testing/) 패키지가 이제 거의 항상 오류인 `panic(nil)`을 호출하는 테스트를 진단합니다. 또한, 이제 테스트 실패 시에도 (프로파일링 플래그로 호출된 경우) 프로파일을 작성합니다.
- [`unicode`](/pkg/unicode/) 패키지 및 시스템 전체의 관련 지원 사항이 Unicode 6.2.0에서 [Unicode 6.3.0](https://www.unicode.org/versions/Unicode6.3.0/)으로 업그레이드되었습니다.
