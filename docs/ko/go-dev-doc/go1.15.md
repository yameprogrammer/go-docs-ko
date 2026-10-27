<!--
참고: 이 문서 및 이 디렉토리에 있는 다른 문서에서, 고정 폭 문구를 비고정 폭 공백으로 표현하는 것이 관례입니다 (예: `hello world`).
이러한 문구에서 내부 태그를 제거하는 CL을 보내지 마세요.
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.15 소개 {#introduction}

가장 최신 Go 릴리스인 버전 1.15은 [Go 1.14](go1.14) 이후 6개월 만에 출시되었습니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
물론, 이 릴리스는 Go 1의 [호환성 보장](/doc/go1compat.html)을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

Go 1.15에는 [링크어에 대한 상당한 개선 사항](#linker),
[높은 코어 수에서 작은 객체에 대한 할당 개선](#runtime),
그리고 [X.509 CommonName]을 [deprecated] 합니다.
`GOPROXY`는 이제 오류를 반환하는 프록시를 건너뛰도록 지원하며,
새로운 [내장 tzdata 패키지](#time/tzdata)가 추가되었습니다.

## 언어 변경 사항 {#language}

```markdown
## 변경 사항 없음

현재 언어는 변경되지 않습니다.
```

## 포트

### 다윈

```
{#darwin}
```

كما [공지](go1.14#darwin)된 Go 1.14 릴리스 노트에 따르면, Go 1.15은 macOS 10.12 Sierra 또는 그 이상 버전을 필요로 합니다. 이전 버전 지원은 중단되었습니다.

<!-- golang.org/issue/37610, golang.org/issue/37611, CL 227582, 및 CL 227198 -->
Go 1.14 릴리스 노트에 발표된 대로, Go 1.15에서는 macOS, iOS, iPadOS, watchOS, tvOS에서 32비트 바이너리에 대한 지원이 중단됩니다 (`darwin/386` 및 `darwin/arm` 포트). Go는 여전히 64비트 `darwin/amd64` 및 `darwin/arm64` 포트를 지원합니다.

### Windows

<!-- CL 214397 및 CL 230217 -->
Go는 이제 `-buildmode=pie` 플래그가 제공될 때 Windows ASLR 실행 파일을 생성합니다. Go 명령어는 Windows에서 기본적으로 `-buildmode=pie`를 사용합니다.

<!-- CL 227003 -->
`-race` 및 `-msan` 플래그는 이제 항상 `-d=checkptr`를 활성화하여 `unsafe.Pointer`의 사용을 검사합니다. 이 기능은 이전에 Windows를 제외한 모든 운영 체제에서 사용되었습니다.

<!-- CL 211139 -->
Go로 빌드된 DLL이 시그널 (예: 터미널에서 Ctrl-C)을 받으면 더 이상 프로세스가 종료되지 않습니다.

### 안드로이드 {#android}

<!-- CL 235017, golang.org/issue/38838 -->
Android용 바이너리를 링크할 때, Go 1.15은 NDK의 최신 버전에서 사용 가능한 `lld` 링커를 명시적으로 선택합니다.
`lld` 링커는 일부 장치에서 충돌을 방지하며, 향후 NDK 버전에서 기본 NDK 링커로 사용될 예정입니다.

### OpenBSD {#openbsd}

<!-- CL 234381 -->
Go 1.15 버전에서 `GOARCH=arm` 및 `GOARCH=arm64`에서 OpenBSD 6.7를 지원합니다. 이전 Go 버전에서는 `GOARCH=386` 및 `GOARCH=amd64`에서 OpenBSD 6.7를 지원했습니다.

### RISC-V {#riscv}

<!-- CL 226400, CL 226206 등 -->
Linux에서 64비트 RISC-V 포트에 대한 안정성과 성능 개선이 이루어졌습니다 (`GOOS=linux`, `GOARCH=riscv64`). 또한 비동기적 전위도 지원합니다.

### 386 {#386}

<!-- golang.org/issue/40255 -->
Go 1.15은 x87-전용 부동 소수점 하드웨어(`GO386=387`)만을 지원하는 마지막 릴리스입니다. 향후 릴리스에서는 386에서 SSE2를 지원해야 합니다. 이를 통해 Go의 최소 `GOARCH=386` 요구 사항을 Intel Pentium 4 (2000년 출시) 또는 AMD Opteron/Athlon 64 (2003년 출시)로 변경합니다.

## 도구 {#tools}

### Go 명령어 {#go-명령어}

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, world!")
}
```

이 코드는 "Hello, world!"를 출력하는 간단한 Go 프로그램입니다.

**Go 명령어 사용법:**

1.  `go run main.go` 명령어를 사용하여 Go 프로그램을 실행합니다.
2.  `go build main.go` 명령어를 사용하여 실행 가능한 파일(main.exe)을 생성합니다.
3.  `go install` 명령어를 사용하여 Go 패키지를 설치합니다.

**예시:**

다음은 Go 명령어를 사용하는 예시입니다.

```bash
go version
```

이 명령어는 Go 버전 정보를 출력합니다.

```bash
go env
```

이 명령어는 Go 환경 변수 목록을 출력합니다.

<!-- golang.org/issue/37367 -->
`GOPROXY` 환경 변수는 이제 오류를 반환하는 프록시를 건너뛸 수 있습니다. 프록시 URL은 이제 쉼표(`,`) 또는 파이 문자(`|`)를 사용하여 구분할 수 있습니다. 만약 프록시 URL 뒤에 쉼표가 오면, `go` 명령은 404 또는 410 HTTP 응답 후 목록의 다음 프록시만 시도합니다. 만약 프록시 URL 뒤에 파이 문자가 오면, `go` 명령은 모든 오류 후 목록의 다음 프록시를 시도합니다. `GOPROXY`의 기본값은 `https://proxy.golang.org,direct`로 유지되므로, 오류 발생 시 `direct`로 전환되지 않습니다.

#### `go` 테스트 {#go-test}

<!-- https://golang.org/issue/36134 -->
`-timeout` 플래그를 변경하면 캐시된 테스트 결과가 무효화됩니다. 긴 타임아웃으로 실행된 테스트의 캐시된 결과는 `go test` 명령어를 짧은 타임아웃으로 다시 실행할 때 더 이상 성공으로 간주되지 않습니다.

#### 플래그 파싱 {#go-flag-parsing}

<!-- https://golang.org/cl/211358 -->
`go` `test` 및 `go` `vet`에서 발생하는 다양한 플래그 파싱 문제를 수정했습니다. 특히, `GOFLAGS`에 지정된 플래그가 보다 일관성 있게 처리되도록 수정되었으며, `-outputdir` 플래그는 이제 `go` 명령의 현재 작업 디렉토리(각 개별 테스트의 작업 디렉토리가 아닌)에 대한 상대 경로를 해석합니다.

#### 모듈 캐시 {#module-cache}

<!-- https://golang.org/cl/219538 -->
모듈 캐시의 위치는 이제 `GOMODCACHE` 환경 변수를 사용하여 설정할 수 있습니다. `GOMODCACHE`의 기본값은 이전 변경 전에 모듈 캐시의 위치인 `GOPATH[0]/pkg/mod`입니다.

<!-- https://golang.org/cl/221157 -->
Windows에서 "접근이 거부됨" 오류가 발생하는 경우, `go` 명령어가 모듈 캐시에 접근하는 데 문제가 발생할 때, 외부 프로그램이 동시에 파일 시스템을 스캔하는 경우에 대한 해결책이 마련되었습니다 (자세한 내용은 [문제 #36568](/issue/36568) 참조). 이 해결책은 기본적으로 활성화되어 있지 않습니다. 왜냐하면 Go 버전이 1.14.2 및 1.13.10보다 낮고, 동일한 모듈 캐시를 사용하는 경우 안전하지 않기 때문입니다. `GODEBUG=modcacheunzipinplace=1` 환경 변수를 명시적으로 설정하여 활성화할 수 있습니다.

### 수의사

#### 새로운 경고: string(x) {#vet-string-int}

<!-- CL 212919, 232660 -->
이제 제공되는 도구는 `string(x)` 형태의 변환에 대해 경고합니다. 여기서 `x`는 `rune` 또는 `byte`가 아닌 정수 유형입니다.
Go 언어를 사용한 경험을 통해, 많은 변환이 `string(x)`가 정수 `x`의 문자열 표현으로 평가된다고 잘못 가정하는 경우가 있다는 것을 알 수 있습니다.
실제로는 `x`의 값에 대한 UTF-8 인코딩을 포함하는 문자열로 평가됩니다.
예를 들어, `string(9786)`는 `"9786"` 문자열로 평가되지 않고, `"☺"` 또는 `"\xe2\x98\xba"` 문자열로 평가됩니다.

코드가 `string(x)`를 올바르게 사용하는 경우, 다음과 같이 `string(rune(x))`로 다시 작성할 수 있습니다.
또는, 특정 경우에는 적절한 바이트 슬라이스 `buf`를 사용하여 `utf8.EncodeRune(buf, x)`를 호출하는 것이 적절한 해결책일 수 있습니다.
다른 코드는 대부분 `strconv.Itoa` 또는 `fmt.Sprint`를 사용하는 것이 좋습니다.

이 새로운 수의사 검사는 기본적으로 `go` `test`를 사용할 때 활성화됩니다.

저희는 향후 Go의 릴리스에서 이 변환을 금지하는 것을 고려하고 있습니다.
즉, 언어는 `string(x)`를 정수 `x`에만 허용하도록 변경됩니다.
이 경우, `x`의 타입이 `rune` 또는 `byte`일 때만 가능합니다.
이러한 언어 변경은 이전 버전과의 호환성을 제공하지 않습니다.
저희는 이 래트 검사를 언어를 변경하기 위한 초기 단계로 사용하고 있습니다.

#### 불가능한 인터페이스 변환에 대한 새로운 경고 {#vet-impossible-interface}

<!-- CL 218779, 232660 -->
동물병원 도구가 이제 하나의 인터페이스 유형에서 다른 인터페이스 유형으로의 타입 추론에 대해 경고합니다.
특히, 타입 추론이 항상 실패할 경우에 발생합니다.
이것은 두 인터페이스 유형이 동일한 이름을 가진 메서드를 구현하지만 다른 타입 시그니처를 가지고 있을 때 발생합니다.

항상 실패하는 타입 어설션을 작성할 이유가 없으므로,
이 검사를 트리거하는 모든 코드는 다시 작성해야 합니다.

이 새로운 수의사 검사는 기본적으로 다음을 사용할 때 활성화됩니다.
`go` `test`.

우리는 Go의 향후 릴리스에서 불가능한 인터페이스 유형 주장을 금지하는 것을 고려하고 있습니다.
이러한 언어 변경은 이전 버전과의 호환성을 제공하지 않습니다.
우리는 이 검사를 언어 변경을 위한 초기 단계로 사용하고 있습니다.

## 런타임 {#runtime}

<!-- CL 221779 -->
`panic`이 다음 유형 중 하나로 전달된 값과 함께 호출될 때, 값 자체가 출력됩니다. (예: `bool`, `complex64`, `complex128`, `float32`, `float64`, `int`, `int8`, `int16`, `int32`, `int64`, `string`, `uint`, `uint8`, `uint16`, `uint32`, `uint64`, `uintptr`)
이전에는 정확히 이러한 유형의 값에만 적용되었습니다.

<!-- CL 228900 -->
유닉스 시스템에서 `kill` 명령 또는 `kill` 시스템 호출을 사용하여 Go 프로그램에 `SIGSEGV`, `SIGBUS`, 또는 `SIGFPE` 신호를 보내고, 신호가 `[os/signal.Notify](pkg/os/signal/#Notify)`를 통해 처리되지 않으면, Go 프로그램은 이제 신뢰성 있게 스택 트레이스와 함께 종료됩니다.
이전 버전에서는 동작이 예측 불가능했습니다.

<!-- CL 221182, CL 229998 -->
작은 객체의 할당이 고성능 코어 수에서 훨씬 더 효율적으로 작동하며, 최악의 경우 지연 시간이 낮아졌습니다.

<!-- CL 216401 -->
작은 정수 값을 인터페이스 값으로 변환하는 것이 더 이상 할당을 유발하지 않습니다.

<!-- CL 216818 -->
닫힌 채널에서 비동기적으로 수신하는 동작과 열린 채널에서 비동기적으로 수신하는 동작이 동일하게 수행됩니다.

## 컴파일러

<!-- CL 229578 -->
`unsafe` 패키지의 [안전 규칙](/pkg/unsafe/#Pointer)은 특정 함수를 호출할 때 `unsafe.Pointer`를 `uintptr`로 변환할 수 있도록 허용합니다. 이전에는 일부 경우에 컴파일러가 여러 개의 연쇄적인 변환(예: `syscall.Syscall(…, uintptr(uintptr(ptr)), …)`와 같이)을 허용했습니다. 이제 컴파일러는 정확히 하나의 변환만 허용합니다. 여러 변환을 사용하는 코드는 안전 규칙을 준수하도록 업데이트해야 합니다.

<!-- CL 230544, CL 231397 -->
Go 1.15는 Go
1.14에 비해 약 5% 정도의 일반적인 바이너리 크기를 줄입니다. 이는 특정 유형의 GC 메타데이터를 제거하고, 더 적극적으로 사용되지 않는 유형의 메타데이터를 제거함으로써 가능합니다.

<!-- CL 219357, CL 231600 -->
이 도구 체인은 `GOARCH=amd64`에서 `Intel
CPU 오류 SKX102`를 완화합니다. 함수를 32바이트 경계에 맞추고 점프 명령을 패딩하여 이를 수행합니다. 이러한 패딩으로 인해 바이너리 크기가 증가하지만, 위에서 언급한 바이너리 크기 개선으로 인해 충분히 상쇄됩니다.

<!-- CL 222661 -->
Go 1.15 버전에서 컴파일러와 어셈블러 모두에 `-spectre` 플래그를 추가하여 Spectre 완화 기능을 활성화할 수 있도록 했습니다.
이 기능은 거의 필요하지 않으며, 주로 "다중 방어" 메커니즘으로 제공됩니다.
자세한 내용은 [Spectre 위키 페이지](/wiki/Spectre)를 참조하십시오.

<!-- CL 228578 -->
컴파일러는 이제 "잘못된 컴파일러 지시문" 오류를 발생시켜, `//go:` 컴파일러 지시문을 더 이상 해석하지 않습니다. 이러한 잘못된 지시문은 이전 버전에서는 무시되었지만, 이제는 컴파일러에 의해 오류로 처리됩니다.

<!-- CL 206658, CL 205066 -->
컴파일러의 `-json` 최적화 로깅이 이제
큰 (>= 128 바이트) 복사본을 보고하고, 이스케이프 분석 결정에 대한 설명을 포함합니다.

## 링커 {#linker}

이 릴리스에는 Go 링커에 대한 상당한 개선 사항이 포함되어 있으며, 이는 링커의 리소스 사용량(시간 및 메모리 모두)을 줄이고 코드의 견고성/유지 관리성을 향상시킵니다.

다음은 대규모 Go 프로그램의 대표적인 집합에 대해 링크를 사용하는 것이 평균 20% 더 빠르고 30% 적은 메모리를 필요로 한다는 것을 보여줍니다. 이는 `ELF`-기반 OS(Linux, FreeBSD, NetBSD, OpenBSD, Dragonfly, 및 Solaris)에서 `amd64` 아키텍처에서 실행될 때 해당됩니다. 다른 아키텍처/OS 조합에 대해서는 더 미미한 개선이 있습니다.

더 나은 링커 성능에 기여하는 주요 요소는 새로운 설계된 오브젝트 파일 형식과 내부 단계의 재구성이 되어 동시성을 높이는 것입니다 (예: 심볼에 대한 위치 지정 작업을 병렬로 적용). Go 1.15의 오브젝트 파일은 1.14와 비교하여 약간 더 큽니다.

이 변경 사항은 여러 버전 프로젝트의 일부입니다.
[Go 링크러를 현대화하기 위한 작업](https://s/better-linker)을 수행하는 것이므로, 향후 출시 버전에서는 추가적인 링크러 개선이 예상됩니다.

<!-- CL 207877 -->
링커는 이제 `-buildmode=pie`에 대해 `linux/amd64` 및 `linux/arm64`에서 내부 링킹 모드로 기본값을 갖습니다. 따라서 이러한 구성은 더 이상 C 링커가 필요하지 않습니다. 외부 링킹 모드 (Go 1.14의 기본값인 `-buildmode=pie`에 대한)는 `-ldflags=-linkmode=external` 플래그를 사용하여 요청할 수 있습니다.

## Objdump
```
objdump
```

<!-- CL 225459 -->
`objdump` 도구가 이제 GNU 어셈블러 구문으로 디스어셈블하는 기능을 지원합니다.
`-gnu` 플래그를 사용합니다.

## 표준 라이브러리 {#library}

### 새로운 임베디드 tzdata 패키지 {#time_tzdata}

<!-- CL 224588 -->
Go 1.15에는 새로운 패키지인
[`time/tzdata`](/pkg/time/tzdata/)가 포함되어 있으며,
이를 통해 프로그램을 통해 시간대 데이터베이스를 포함할 수 있습니다.
이 패키지를 가져오기 (예: `import _ "time/tzdata"`)를 통해,
시간대 데이터베이스가 로컬 시스템에 없는 경우에도 프로그램이 시간대 정보를 찾을 수 있습니다.
또한, `-tags timetzdata`를 사용하여 시간대 데이터베이스를 포함할 수도 있습니다.
어떤 방법을 사용하든, 프로그램의 크기는 약 800 KB 증가합니다.

### Cgo {#cgo}

<!-- CL 235817 -->
Go 1.15에서 C 타입 `EGLConfig`을 Go 타입 `uintptr`으로 변환합니다. 이 변경 사항은 Go 1.12 및 이후 버전에서 `EGLDisplay`, Darwin의 CoreFoundation, Java의 JNI 타입들을 다루는 방식과 유사합니다. 자세한 내용은 [cgo
문서](/cmd/cgo/#hdr-Special_cases)를 참조하십시오.

<!-- CL 250940 -->
Go 1.15.3 이상 버전에서는 cgo가 Go 코드가 정의되지 않은 구조체 유형(예: `struct S;`와 같이 정의된 C 구조체)을 스택 또는 힙에 할당하는 것을 허용하지 않습니다.
Go 코드는 이러한 유형에 대한 포인터만 사용할 수 있습니다.
이러한 구조체의 인스턴스를 할당하고 포인터 또는 전체 구조체 값을 C 코드에 전달하는 것은 항상 위험하며 제대로 작동하지 않을 가능성이 높았으며, 이제는 금지됩니다.
해결책은 Go 코드를 포인터만 사용하는 방식으로 다시 작성하거나, Go 코드가 적절한 C 헤더 파일을 포함하여 구조체의 전체 정의를 참조하도록 하는 것입니다.

### X.509 CommonName 폐기 {#commonname}

<!-- CL 231379 -->
X.509 인증서의 `CommonName` 필드를 호스트 이름으로 처리하는 구형 동작은, 대체 이름이 없는 경우 기본적으로 비활성화됩니다. `GODEBUG` 환경 변수에 `x509ignoreCN=0` 값을 추가하여 일시적으로 다시 활성화할 수 있습니다.

참고: 만약 `CommonName`이 유효하지 않은 호스트 이름인 경우, `GODEBUG` 설정과 관계없이 항상 무시됩니다. 유효하지 않은 이름에는 다음과 같은 것들이 포함됩니다.
* 문자, 숫자, 하이픈, 밑줄 외의 모든 문자를 포함하는 이름
* 빈 레이블 또는 끝에 점이 있는 이름

### 라이브러리의 미세 조정 {#minor_library_changes}

항상 그렇듯이, 라이브러리에는 다양한 미미한 변경 사항과 업데이트가 있으며, 이는 Go 1의 [호환성 보장](/doc/go1compat)을 염두에 두고 구현되었습니다.

#### [bufio](/pkg/bufio/)

<!-- CL 225357, CL 225557 -->
`[`Scanner`](/pkg/bufio/#Scanner)을 유효하지 않은
`[`io.Reader`](/pkg/io/#Reader)과 함께 사용할 때,
`Read`에서 잘못된 음수 값을 반환하는 경우,
`Scanner`는 더 이상 오류를 발생시키지 않으며, 대신
새로운 오류 [`ErrBadReadCount`](/pkg/bufio/#ErrBadReadCount)를 반환합니다.

<!-- bufio -->

#### [context](pkg/context/)

<!-- CL 223777 -->
제로 값의 부모를 사용하여 파생 `Context`를 만드는 것은 이제 명시적으로 허용되지 않습니다. 다음 함수(`WithValue[/pkg/context/#WithValue], `WithDeadline[/pkg/context/#WithDeadline], 또는 `WithCancel[/pkg/context/#WithCancel]`)를 사용하여 시도할 경우, 예외가 발생합니다.

<!-- 컨텍스트 -->

#### [암호화](/pkg/crypto/)

<!-- CL 231417, CL 225460 -->
`PrivateKey` 및 `PublicKey` 타입은 다음 패키지에서 `Equal` 메서드를 제공하여 키의 동등성을 비교하거나 공용키에 대한 타입 안전 인터페이스를 제공합니다:
[`crypto/rsa`](/pkg/crypto/rsa/),
[`crypto/ecdsa`](/pkg/crypto/ecdsa/), 및
[`crypto/ed25519`](/pkg/crypto/ed25519/). 메서드 시그니처는
[`go-cmp`의 동등성 정의](https://pkg.go.dev/github.com/google/go-cmp/cmp#Equal)와 호환됩니다.

<!-- CL 224937 -->
[`Hash`](/pkg/crypto/#Hash)가 이제
[`fmt.Stringer`](/pkg/fmt/#Stringer)를 구현합니다.

<!-- 암호화폐 -->

#### [crypto/ecdsa](/pkg/crypto/ecdsa/)

<!-- CL 217940 -->
새로운 `[SignASN1](/pkg/crypto/ecdsa/#SignASN1)`
및 `[VerifyASN1](/pkg/crypto/ecdsa/#VerifyASN1)`
함수는 표준 ASN.1 DER 인코딩을 사용하여 ECDSA 서명을 생성하고 검증할 수 있게 합니다.

```markdown
<!-- crypto/ecdsa -->
```

```
#### [crypto/elliptic](/pkg/crypto/elliptic/)

<!-- CL 202819 -->
새로운 `MarshalCompressed` 및 `UnmarshalCompressed` 함수는 NIST  elliptice 곡선 점을 압축된 형식으로 인코딩하고 디코딩할 수 있게 합니다. ([NIST elliptice 곡선 점 압축 형식 인코딩 및 디코딩](pkg/crypto/elliptic/#MarshalCompressed) 및 [NIST elliptice 곡선 점 압축 형식 인코딩 및 디코딩](pkg/crypto/elliptic/#UnmarshalCompressed))

<!-- crypto/elliptic -->

#### [crypto/rsa](/pkg/crypto/rsa/)

<!-- CL 226203 -->
[`VerifyPKCS1v15`](/pkg/crypto/rsa/#VerifyPKCS1v15)
이제 RFC 8017에 따라, 선행 0이 누락된 유효하지 않은 짧은 서명을 거부합니다.

<!-- crypto/rsa -->

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 214977 -->
새로운
[`Dialer`](/pkg/crypto/tls/#Dialer)
형식과 그
[`DialContext`](/pkg/crypto/tls/#Dialer.DialContext)
메서드는 컨텍스트를 사용하여 TLS 서버에 연결하고 핸드셰이크를 수행하는 것을 허용합니다.

<!-- CL 229122 -->
새로운
[`VerifyConnection`](/pkg/crypto/tls/#Config.VerifyConnection)
콜백은
[`Config`](/pkg/crypto/tls/#Config)
형에 추가되었으며, 각 연결에 대해 사용자 정의 검증 로직을 사용하도록 합니다. 이 콜백은 다음 정보를 포함하는
[`ConnectionState`](/pkg/crypto/tls/#ConnectionState)
에 접근할 수 있습니다. 여기에는 상대방 인증서, SCT(인증서 상태 코드), 그리고 스태플드 OCSP(온라인 인증서 상태 프로토콜) 응답이 포함됩니다.

<!-- CL 230679 -->
자동으로 생성된 세션 티켓 키는 이제 24시간마다 자동으로 회전되며, 유효 기간은 7일로 설정되어, 프론트 시크릿에 미치는 영향을 최소화합니다.

<!-- CL 231317 -->
TLS 1.2 및 이전 버전에 사용되는 세션 티켓의 유효 기간이 7일로 제한됩니다. 이 기능은 재연결 시 재사용되는 세션 키의 영향을 줄이기 위해 도입되었습니다.

<!-- CL 231038 -->
RFC 8446에 명시된 클라이언트 측 다운그레이드 보호 확인이 이제 적용됩니다. 이는 중간 상자가 승인되지 않은 다운그레이드 공격과 유사하게 동작하는 경우 클라이언트에서 연결 오류가 발생할 수 있습니다.

<!-- CL 208226 -->
[`SignatureScheme`](/pkg/crypto/tls/#SignatureScheme),
[`CurveID`](/pkg/crypto/tls/#CurveID), 및
[`ClientAuthType`](/pkg/crypto/tls/#ClientAuthType)
이제 [`fmt.Stringer`](/pkg/fmt/#Stringer)를 구현합니다.

<!-- CL 236737 -->
`ConnectionState`(`/pkg/crypto/tls/#ConnectionState`)
필드 `OCSPResponse` 및 `SignedCertificateTimestamps`는 이제 클라이언트 측에서 재개된 연결에서 다시 채워집니다.

<!-- CL 227840 -->
[`tls.Conn`](/pkg/crypto/tls/#Conn)
이제 영구적으로 끊어진 연결의 경우 불투명한 오류를 반환하며,
일시적인
[`net.Error`](/pkg/net/http/#Error)를 감쌉니다. 원래 `net.Error`에 액세스하려면
`errors.As` (또는 `errors.Unwrap`)를 대신 사용하는 것이 좋습니다.

```markdown
<!-- crypto/tls -->
```

#### [crypto/x509](/pkg/crypto/x509/)

<!-- CL 231378, CL 231380, CL 231381 -->
만약 인증서에 있는 이름 또는 검증되는 이름 ( `VerifyOptions.DNSName` 또는 `VerifyHostname`을 사용하여)이 유효하지 않으면, 이제 추가적인 처리를 거치지 않고 대소문자를 구분하지 않고 비교합니다 (와일드카드를 존중하거나 끝에 있는 점을 제거하지 않습니다).
유효하지 않은 이름에는 알파벳, 숫자, 하이픈, 밑줄 외에 다른 모든 문자가 포함된 이름, 빈 레이블이 있는 이름, 인증서에 끝에 점이 있는 이름 등이 포함됩니다.

<!-- CL 217298 -->
새로운 [`CreateRevocationList`](/pkg/crypto/x509/#CreateRevocationList)
함수와 [`RevocationList`](/pkg/crypto/x509/#RevocationList) 타입은 RFC 5280을 준수하는 X.509 v2 인증서 취소 목록을 생성할 수 있도록 합니다.

<!-- CL 227098 -->
[`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate)
이제 템플릿이 CA이고 명시적으로 지정되지 않은 경우 자동으로 `SubjectKeyId`를 생성합니다.

<!-- CL 228777 -->
[`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate)
이제 템플릿에 `MaxPathLen`이 지정되어 있지만 CA가 아닌 경우 오류를 반환합니다.

<!-- CL 205237 -->
macOS를 제외한 유닉스 시스템에서는 `SSL_CERT_DIR` 환경 변수가 이제 콜론으로 구분된 목록일 수 있습니다.

<!-- CL 227037 -->
macOS에서는 바이너리가 이제 항상 `Security.framework`에 연결되어 시스템 신뢰 뿌리를 추출합니다. cgo가 사용 가능한지 여부에 관계없이 이 동작이 더 일관성 있게 OS verifier와 작동합니다.

<!-- crypto/x509 -->

#### [crypto/x509/pkix](/pkg/crypto/x509/pkix/)

<!-- CL 229864, CL 240543 -->
[`Name.String`](/pkg/crypto/x509/pkix/#Name.String)
이제 [`Names`](/pkg/crypto/x509/pkix/#Name.Names)에서
표준 외의 속성을 출력합니다.
[`ExtraNames`](/pkg/crypto/x509/pkix/#Name.ExtraNames)가 nil인 경우.

<!-- crypto/x509/pkix -->

#### [database/sql](/pkg/database/sql/)

<!-- CL 145758 -->
새로운 [`DB.SetConnMaxIdleTime`](/pkg/database/sql/#DB.SetConnMaxIdleTime)
메서드는 연결이 특정 시간 동안 비활성 상태인 경우, 연결 풀에서 연결을 제거할 수 있게 합니다. 이 기능은 연결의 총 수명과 관계없이 작동합니다. [`DBStats.MaxIdleTimeClosed`](/pkg/database/sql/#DBStats.MaxIdleTimeClosed)
필드는 `DB.SetConnMaxIdleTime`로 인해 닫힌 연결의 총 개수를 보여줍니다.

<!-- CL 214317 -->
새로운 `Row.Err` 접근자를 사용하면 `Row.Scan`을 호출하지 않고도 쿼리 오류를 확인할 수 있습니다.

<!-- database/sql -->

#### [database/sql/driver](/pkg/database/sql/driver/)

<!-- CL 174122 -->
새로운 [`Validator`](/pkg/database/sql/driver/#Validator)
인터페이스는 `Conn`에서 구현될 수 있으며, 이를 통해 드라이버가 연결이 유효한지 또는 폐기해야 하는지 신호를 보낼 수 있습니다.

<!-- 데이터베이스/SQL/드라이버 -->

#### [디버깅/PE 파일](/pkg/debug/pe/)

<!-- CL 222637 -->
이 패키지는 PE 파일 형식에서 사용되는
`IMAGE_FILE`, `IMAGE_SUBSYSTEM`,
그리고 `IMAGE_DLLCHARACTERISTICS` 상수를 정의합니다.

<!-- 디버깅/PE -->

#### [encoding/asn1](/pkg/encoding/asn1/)

<!-- CL 226984 -->
[`Marshal`](/pkg/encoding/asn1/#Marshal)가 이제 SET OF의 구성 요소를 X.690 DER 규격에 따라 정렬합니다.

<!-- CL 227320 -->
[`Unmarshal`](/pkg/encoding/asn1/#Unmarshal) 이제 X.690 DER에 따라 최소하게 인코딩되지 않은 태그 및
객체 식별자를 거부합니다.

<!-- encoding/asn1 -->

#### [encoding/json](/pkg/encoding/json/)

<!-- CL 199837 -->
이 패키지는 디코딩 시 최대 중첩 깊이에 대한 내부 제한을 갖습니다. 이를 통해 깊게 중첩된 입력이 큰 양의 스택 메모리를 사용하거나, 심지어 "goroutine 스택이 제한을 초과" 에러를 발생시키는 것을 방지할 수 있습니다.

<!-- encoding/json -->

#### [flag](/pkg/flag/)

<!-- CL 221427 -->
`flag` 패키지가 `-h` 또는 `-help` 플래그를 감지하고,
이 플래그가 정의되지 않았을 때, 이제 사용법 메시지를 출력합니다.
만약 `FlagSet`가 `ExitOnError`와 함께 생성되었다면,
`FlagSet.Parse`는 상태를 2로 종료합니다.
이 릴리스에서는 `-h` 또는 `-help`에 대한 종료 상태가 0으로 변경되었습니다.
특히, 이는 기본 명령줄 플래그 처리에 적용됩니다.

#### [fmt](pkg/fmt/)

<!-- CL 215001 -->
`%#g` 및 `%#G` 형식의 인쇄 함수는 부동 소수점 값에 대한
후행 0을 유지합니다.

<!-- fmt -->

#### [go/format](pkg/go/format/)

<!-- golang.org/issue/37476, CL 231461, CL 240683 -->
`[`Source`](/pkg/go/format/#Source) 및
`[`Node`](/pkg/go/format/#Node) 함수는 이제 Go 소스 코드 형식을 위해 숫자 리터럴 접두사 및 지수를 표준화합니다. 이는 `gofmt` (`/pkg/cmd/gofmt/`) 명령이 구현된 대로 동작합니다 (Go 1.13부터 [`/doc/go1.13#gofmt`]).

<!-- go/format -->

#### [html/template](/pkg/html/template/)

<!-- CL 226097 -->
패키지는 이제 모든 JavaScript 및 JSON 컨텍스트에서 유니코드 이스케이프(`\uNNNN`)를 사용합니다. 이를 통해 `application/ld+json` 및 `application/json` 컨텍스트에서 발생하는 이스케이프 오류를 수정합니다.

<!-- html/템플릿 -->

#### [io/ioutil](/pkg/io/ioutil/)

<!-- CL 212597 -->
[`TempDir`](/pkg/io/ioutil/#TempDir) 및
[`TempFile`](/pkg/io/ioutil/#TempFile)
은 이제 경로 구분자를 포함하는 패턴을 거부합니다.
즉, `ioutil.TempFile("/tmp",` `"../base*")`와 같은 호출은 더 이상 성공하지 않습니다.
이는 의도하지 않은 디렉토리 탐색을 방지합니다.

<!-- io/ioutil -->

#### [math/big](/pkg/math/big/)

<!-- CL 230397 -->
새로운 [`Int.FillBytes`](/pkg/math/big/#Int.FillBytes)
메서드는 고정 크기의 미리 할당된 바이트 슬라이스로 직렬화할 수 있게 합니다.

<!-- math/big -->

```
#### [math/cmplx](pkg/math/cmplx/)
```

<!-- CL 220689 -->
이 패키지의 함수는 C99 표준 (IEC 60559 호환 복소수 연산, 부록 G)에 따라 무한대, NaN (Not a Number), 부호 있는 0와 같은 특수 인수를 처리하도록 업데이트되었습니다.

```
<!-- math/cmplx-->
```

#### [net](/pkg/net/)

<!-- CL 228645 -->
I/O 작업이 `Conn.SetDeadline`(`/pkg/net/#Conn`),
`Conn.SetReadDeadline`,
또는 `Conn.SetWriteDeadline` 메서드가 설정한 데드라인을 초과하면, 이제
`os.ErrDeadlineExceeded`를 반환하거나 감싸는 오류를 반환합니다.
이를 사용하여 데드라인이 초과되었는지 신뢰성 있게 감지할 수 있습니다.
이전 버전에서는 `Timeout` 메서드를 오류에 호출하도록 권장되었지만, 데드라인이 초과되지 않았음에도 I/O 작업이 `Timeout`이 `true`를 반환하는 오류를 반환할 수 있습니다.

<!-- CL 228641 -->
새로운 `Resolver.LookupIP`
메서드는 네트워크별 IP 조회뿐만 아니라 컨텍스트를 지원합니다.

#### [net/http](/pkg/net/http/)

<!-- CL 231418, CL 231419 -->
파싱이 이제는 요청 스미싱 공격에 대한 보안 강화 조치로 더욱 엄격해졌습니다:
비-ASCII 공백이 SP 및 HTAB과 같이 잘리지 않게 되었으며, "`identity`" `Transfer-Encoding`에 대한 지원이 제거되었습니다.

<!-- net/http -->

#### [net/http/httputil](pkg/net/http/httputil/)

<!-- CL 230937 -->
[`ReverseProxy`](/pkg/net/http/httputil/#ReverseProxy)
이제 들어오는 `Request.Header` 맵의 해당 필드에 대한 항목이 `nil`일 때 `X-Forwarded-For` 헤더를 수정하지 않습니다.

<!-- CL 224897 -->
`ReverseProxy`에 의해 처리되는 스위칭 프로토콜(예: WebSocket) 요청이 취소될 때, 백엔드 연결이 이제 올바르게 닫힙니다.

#### [net/http/pprof](/pkg/net/http/pprof/)

<!-- CL 147598, CL 229537 -->
모든 프로필 엔드포인트가 이제 "`seconds`" 파라미터를 지원합니다. 이 파라미터가 존재할 경우, 지정된 시간 동안의 엔드포인트 프로필을 반환하고, 차이를 보고합니다.
`cpu` 프로필 및 추적 엔드포인트에서 "`seconds`" 파라미터의 의미는 변경되지 않습니다.

#### [net/url](pkg/net/url/)

<!-- CL 227645 -->
새로운 `URL` 필드인 `RawFragment` 및 메서드 `EscapedFragment`(`/pkg/net/url/#URL`)은 특정 프래그먼트의 정확한 인코딩에 대한 세부 정보와 제어를 제공합니다.
이는 `RawPath` 및 `EscapedPath`(`/pkg/net/url/#URL.EscapedPath`)와 유사합니다.

<!-- CL 207082 -->
새로운 [`URL`](/pkg/net/url/#URL)
메서드 [`Redacted`](/pkg/net/url/#URL.Redacted)는 URL을 문자열 형식으로 반환하며, 모든 비밀번호를 `xxxxx`로 대체합니다.

#### [os](/pkg/os/)

<!-- CL -->
만약 I/O 작업이 `File.SetDeadline` ([pkg/os/#File.SetDeadline]),
`File.SetReadDeadline` ([pkg/os/#File.SetReadDeadline]),
또는 `File.SetWriteDeadline` ([pkg/os/#File.SetWriteDeadline])
메서드가 설정한 데드라인을 초과하면, 이제는
`os.ErrDeadlineExceeded` ([pkg/os/#ErrDeadlineExceeded])를 반환하거나 감싸는 오류를 반환합니다.
이를 사용하여, 데드라인이 초과되었는지 여부를 신뢰성 있게 감지할 수 있습니다.
이전 버전에서는 `Timeout` 메서드를 오류에 호출하도록 권장되었지만, 데드라인이 초과되지 않았음에도 I/O 작업이 `Timeout`이 `true`를 반환하는 오류를 반환할 수 있습니다.

<!-- CL 232862 -->
`os` 및 `net` 패키지는 `EINTR` 오류로 실패하는 시스템 호출을 이제 자동으로 재시도합니다. 이전에는 이러한 오류로 인해 가짜 실패가 발생했으며, 이는 Go 1.14에서 비동기적인 사전 중단 기능이 추가되면서 더 흔하게 발생했습니다. 이제 이러한 동작은 투명하게 처리됩니다.

<!-- CL 229101 -->
`[`os.File`](/pkg/os/#File) 타입이 이제
`[ReadFrom](</pkg/os/#File.ReadFrom>`
메서드를 지원합니다. 이를 통해 `io.Copy`](/pkg/io/#Copy)를 사용하여
하나의 `os.File`에서 다른 `os.File`로 데이터를 복사할 때,
`copy_file_range` 시스템 호출을 사용할 수 있습니다. 결과적으로
`[io.CopyBuffer](</pkg/io/#CopyBuffer>`
메서드는 `os.File`로 복사할 때 항상 제공된 버퍼를 사용하지 않을 수 있습니다. 프로그램이 제공된 버퍼를 강제로 사용하려면,
`io.CopyBuffer(struct{ io.Writer }{dst}, src, buf)`를 사용하여 복사할 수 있습니다.

#### [플러그인](/pkg/plugin/)

<!-- CL 182959 -->
DWARF 생성 기능이 이제 macOS에서 `-buildmode=plugin`에 대해 지원됩니다 (기본적으로 활성화됨).

<!-- CL 191617 -->
`-buildmode=plugin` 모드로 빌드하는 기능이 `freebsd/amd64`에서 지원됩니다.

#### [reflect](/pkg/reflect/)

<!-- CL 228902 -->
패키지 `reflect`는 이제 모든 비공개 필드의 메서드에 접근하는 것을 허용하지 않으며, 이전에는 비공개, 중첩된 필드의 메서드에 접근하는 것을 허용했습니다. 이전 동작에 의존하는 코드는 대신 래핑 변수의 해당 프로모트된 메서드에 접근하도록 업데이트해야 합니다.

#### [regexp](/pkg/regexp/)

<!-- CL 187919 -->
새로운 [`Regexp.SubexpIndex`](/pkg/regexp/#Regexp.SubexpIndex)
메서드는 지정된 이름의 첫 번째 서브 표현식의 인덱스를 정규 표현식 내에서 반환합니다.

<!-- regexp -->

#### [runtime](/pkg/runtime/)

<!-- CL 216557 -->
다음 함수, 예를 들어
[`ReadMemStats`](/pkg/runtime/#ReadMemStats)
및
[`GoroutineProfile`](/pkg/runtime/#GoroutineProfile),
더 이상 가비지 수거가 진행 중일 때 블록되지 않습니다.

#### [runtime/pprof](pkg/runtime/pprof/)

<!-- CL 189318 -->
이제 goroutine 프로파일은 프로파일링 시 각 goroutine과 관련된 프로파일 라벨을 포함합니다. 이 기능은 `debug=2`로 보고된 프로파일에는 아직 구현되지 않았습니다.

#### [strconv](/pkg/strconv/)

<!-- CL 216617 -->
[`FormatComplex`](/pkg/strconv/#FormatComplex) 및 [`ParseComplex`](/pkg/strconv/#ParseComplex)는 복소수 처리를 위한 기능입니다.

[`FormatComplex`](/pkg/strconv/#FormatComplex)는 복소수를 (a+bi) 형태의 문자열로 변환합니다. 여기서 a와 b는 실수 및 허수 부분입니다.

[`ParseComplex`](/pkg/strconv/#ParseComplex)는 지정된 정밀도로 문자열을 복소수로 변환합니다. `ParseComplex`는 `N+Ni` 형식의 복소수를 받습니다.

<!-- strconv -->

#### [sync](/pkg/sync/)

<!-- CL 205899, golang.org/issue/33762 -->
새로운 메서드
[`Map.LoadAndDelete`](/pkg/sync/#Map.LoadAndDelete)
는 키를 원자적으로 삭제하고, 해당 키에 값이 존재할 경우 이전 값을 반환합니다.

<!-- CL 205899 -->
`Map.Delete` 방법이 더 효율적입니다.

<!-- 동기화 -->

#### [syscall](/pkg/syscall/)

<!-- CL 231638 -->
Unix 시스템에서 `SysProcAttr`를 사용하는 함수는 이제 `Setctty`와 `Foreground` 필드를 동시에 설정하는 시도를 거부합니다. 이는 두 필드 모두 `Ctty` 필드를 사용하지만, 호환되지 않는 방식으로 사용하기 때문입니다. 현재 대부분의 프로그램은 두 필드를 동시에 설정하지 않습니다.

`Setctty` 필드를 설정하려면 이제 `Ctty` 필드가 자식 프로세스에서 `ProcAttr.Files` 필드에 의해 결정된 파일 설명자 번호로 설정되어야 합니다.
자식 설명자를 사용하는 것은 항상 작동했지만, 특정 경우에는 부모 파일 설명자를 사용하는 것도 작동했습니다.
`Setctty`를 설정하는 일부 프로그램은 자식 설명자 번호를 사용하기 위해 `Ctty` 값을 변경해야 할 수 있습니다.

<!-- CL 220578 -->
이제 `windows/amd64`에서 부동 소수점 값을 반환하는 시스템 호출을 호출하는 것이 가능합니다.
[Proc.Call](https://pkg/syscall/#Proc.Call)

#### [테스팅](/pkg/testing/)

<!-- golang.org/issue/28135 -->
`testing.T` 타입에 이제 `Deadline`라는
[`메서드](pkg/testing/#T.Deadline)가 추가되어, 테스트 바이너리가 타임아웃을 초과하는 시간을 보고합니다.

<!-- golang.org/issue/34129 -->
`TestMain` 함수에서 `os.Exit`를 호출하는 것이 더 이상 필요하지 않습니다. 만약 `TestMain` 함수가 반환되면, 테스트 바이너리는 `m.Run`에서 반환된 값을 사용하여 `os.Exit`를 호출합니다.

<!-- CL 226877, golang.org/issue/35998 -->
새로운 메서드
[`T.TempDir`](/pkg/testing/#T.TempDir) 및
[`B.TempDir`](/pkg/testing/#B.TempDir)
은 테스트가 종료될 때 자동으로 삭제되는 임시 디렉토리를 반환합니다.

<!-- CL 229085 -->
`go test -v` 명령이 이제 출력을 테스트 이름별로 그룹화하여 출력합니다. 이전에는 각 줄마다 테스트 이름을 출력했습니다.

<!-- 테스트 -->

#### [text/template](pkg/text/template/)

<!-- CL 226097 -->
[`JSEscape`](/pkg/text/template/#JSEscape)가 이제
일관성 있게 유니코드 이스케이프(`\u00XX`)를 사용하며, 이는
JSON과 호환됩니다.

<!-- 텍스트/템플릿 -->

#### [time](pkg/time/)

<!-- CL 220424, CL 217362, golang.org/issue/33184 -->
새로운 방법
[`Ticker.Reset`](/pkg/time/#Ticker.Reset)
은 타이커의 지속 시간을 변경하는 기능을 지원합니다.

<!-- CL 227878 -->
오류를 반환할 때, [`ParseDuration`](/pkg/time/#ParseDuration)는 이제 원래 값을 따옴표로 묶습니다.

<!-- 시간 -->
