<!--
참고: 이 문서와 이 디렉터리의 다른 문서에서는 `hello` `world`와 같이 고정폭 구문을 비고정폭 공백으로 설정하는 것이 관례입니다.
이러한 구문에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

<style>
  main ul li { margin: 0.5em 0; }
</style>

## Go 1.15 소개 {#introduction}

최신 Go 릴리스인 버전 1.15가 [Go 1.14](go1.14) 출시 6개월 만에 공개되었습니다.
변경 사항의 대부분은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언제나 그렇듯, 이번 릴리스에서도 Go 1 [호환성 약속](/doc/go1compat.html)을 준수합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

Go 1.15에는 [링커에 대한 상당한 개선 사항](#linker)이 포함되어 있으며,
높은 코어 수에서의 [작은 객체 할당 성능이 향상](#runtime)되었고,
[X.509 CommonName](#commonname)이 더 이상 권장되지 않습니다(deprecates).
`GOPROXY`는 이제 에러를 반환하는 프록시를 건너뛰는 기능을 지원하며,
새로운 [내장 tzdata 패키지](#time/tzdata)가 추가되었습니다.

## 언어 변경 사항 {#language}

언어에 변경 사항이 없습니다.

## 포트 {#ports}

### Darwin {#darwin}

Go 1.14 [릴리스 노트](go1.14#darwin)에서 발표한 바와 같이, Go 1.15는 macOS 10.12 Sierra 또는 그 이후 버전을 필요로 하며, 이전 버전에 대한 지원은 중단되었습니다.

<!-- golang.org/issue/37610, golang.org/issue/37611, CL 227582, and CL 227198  -->
Go 1.14 릴리스 노트에서 [공지](/doc/go1.14#darwin)한 바와 같이, Go 1.15부터는 macOS, iOS, iPadOS, watchOS 및 tvOS의 32비트 바이너리(`darwin/386` 및 `darwin/arm` 포트)에 대한 지원이 중단됩니다. Go는 계속해서 64비트 `darwin/amd64` 및 `darwin/arm64` 포트를 지원합니다.

### Windows {#windows}

<!-- CL 214397 및 CL 230217 -->
이제 `cmd/link` 플래그로 `-buildmode=pie`가 제공되면 Go가 Windows ASLR 실행 파일을 생성합니다. Go 커맨드는 Windows에서 기본적으로 `-buildmode=pie`를 사용합니다.

<!-- CL 227003 -->
이제 `-race` 및 `-msan` 플래그는 항상 `-d=checkptr`를 활성화하며, 이는 `unsafe.Pointer` 사용 여부를 확인합니다. 이전에는 Windows를 제외한 모든 OS에서 적용되었습니다.

<!-- CL 211139 -->
Go로 빌드된 DLL은 이제 시그널(터미널의 Ctrl-C 등)을 수신했을 때 프로세스가 종료되지 않습니다.

### Android {#android}

<!-- CL 235017, golang.org/issue/38838 -->
Android용 바이너리를 링크할 때, Go 1.15는 최신 버전의 NDK에서 제공되는 `lld` 링커를 명시적으로 선택합니다.
`lld` 링커는 일부 기기에서의 크래시를 방지하며, 향후 NDK 버전에서 기본 NDK 링커가 될 예정입니다.

### OpenBSD {#openbsd}

<!-- CL 234381 -->
Go 1.15은 `GOARCH=arm` 및 `GOARCH=arm64` 환경에서 OpenBSD 6.7 지원을 추가합니다. 이전 버전의 Go는 이미 `GOARCH=386` 및 `GOARCH=amd64` 환경에서 OpenBSD 6.7을 지원했습니다.

### RISC-V {#riscv}

<!-- CL 226400, CL 226206, and others -->
Linux의 64비트 RISC-V 포트(`GOOS=linux`, `GOARCH=riscv64`)의 안정성과 성능을 개선하는 진전이 있었습니다. 또한 이제 비동기식 선점(asynchronous preemption)을 지원합니다.

### 386 {#386}

<!-- golang.org/issue/40255 -->
Go 1.15은 x87 전용 부동 소수점 하드웨어(`GO386=387`)를 지원하는 마지막 릴리스입니다. 향후 릴리스에서는 386 아키텍처에 최소 SSE2 지원이 필요하며, 이에 따라 Go의 최소 `GOARCH=386` 요구 사항이 Intel Pentium 4(2000년 출시) 또는 AMD Opteron/Athlon 64(2003년 출시)로 상향됩니다.

## Tools {#tools}

### Go 명령어 {#go-command}

<!-- golang.org/issue/37367 -->
이제 `GOPROXY` 환경 변수에서 에러를 반환하는 프록시를 건너뛰는 기능을 지원합니다. 프록시 URL은 이제 쉼표(`,`) 또는 파이프 문자(`|`)로 구분할 수 있습니다. 프록시 URL 뒤에 쉼표가 오면, `go` 명령어는 404 또는 410 HTTP 응답을 받은 경우에만 목록의 다음 프록시를 시도합니다. 프록시 URL 뒤에 파이프 문자가 오면, `go` 명령어는 모든 에러 발생 시 목록의 다음 프록시를 시도합니다. `GOPROXY`의 기본값은 여전히 `https://proxy.golang.org,direct`이며, 이는 에러 발생 시 `direct`로 폴백(fall back)하지 않는다는 점에 유의하십시오.

#### `go` `test` {#go-test}

<!-- https://golang.org/issue/36134 -->
이제 `-timeout` 플래그를 변경하면 캐시된 테스트 결과가 무효화됩니다. 긴 타임아웃으로 테스트를 실행하여 캐시된 결과는 `go` `test`를 짧은 타임아웃으로 다시 호출했을 때 더 이상 성공으로 간주되지 않습니다.

#### 플래그 파싱 {#go-flag-parsing}

<!-- https://golang.org/cl/211358 -->
`go` `test` 및 `go` `vet`에서의 다양한 플래그 파싱 문제가 수정되었습니다. 특히, `GOFLAGS`에 지정된 플래그들이 더 일관되게 처리되며, `-outputdir` 플래그가 이제 (개별 테스트의 작업 디렉터리가 아닌) `go` 명령의 작업 디렉터리를 기준으로 상대 경로를 해석합니다.

#### 모듈 캐시 {#module-cache}

<!-- https://golang.org/cl/219538 -->
이제 `GOMODCACHE` 환경 변수를 통해 모듈 캐시의 위치를 설정할 수 있습니다. `GOMODCACHE`의 기본값은 `GOPATH[0]/pkg/mod`이며, 이는 이번 변경 전의 모듈 캐시 위치와 동일합니다.

<!-- https://golang.org/cl/221157 -->
외부 프로그램이 파일 시스템을 동시에 스캔하여 모듈 캐시에 액세스하는 `go` 명령에서 발생하는 Windows "Access is denied" 오류에 대한 해결 방법이 마련되었습니다([이슈 #36568](/issue/36568) 참조). 이 해결 방법은 Go 1.14.2 및 1.13.10보다 낮은 버전이 동일한 모듈 캐시를 사용하여 동시에 실행될 때 안전하지 않으므로 기본적으로 활성화되지 않습니다. 환경 변수 `GODEBUG=modcacheunzipinplace=1`을 명시적으로 설정하여 활성화할 수 있습니다.

### Vet {#vet}

#### string(x)에 대한 새로운 경고 {#vet-string-int}

<!-- CL 212919, 232660 -->
이제 vet 도구는 `x`가 `rune`이나 `byte` 이외의 정수 타입인 경우 `string(x)` 형태의 변환에 대해 경고를 표시합니다.
Go를 사용한 경험에 따르면, 이러한 형태의 많은 변환이 `string(x)`가 정수 `x`의 문자열 표현으로 평가될 것이라고 잘못 가정하는 경우가 많았습니다.
실제로 이는 `x` 값의 UTF-8 인코딩을 포함하는 문자열로 평가됩니다.
예를 들어, `string(9786)`은 문자열 `"9786"`으로 평가되지 않고, 문자열 `"\xe2\x98\xba"` 또는 `"☺"`로 평가됩니다.

`string(x)`를 올바르게 사용하고 있는 코드는 `string(rune(x))`로 다시 작성할 수 있습니다.
또는 경우에 따라 적절한 바이트 슬라이스 `buf`와 함께 `utf8.EncodeRune(buf, x)`를 호출하는 것이 올바른 해결책일 수 있습니다.
그 외의 코드는 `strconv.Itoa` 또는 `fmt.Sprint`를 사용해야 할 가능성이 높습니다.

이 새로운 vet 체크는 `go` `test`를 사용할 때 기본적으로 활성화됩니다.

우리는 Go의 향후 릴리스에서 해당 변환을 금지하는 것을 검토하고 있습니다.
즉, 언어 사양을 변경하여 `x`의 타입이 `rune` 또는 `byte`인 경우에만 정수 `x`에 대해 `string(x)`를 허용하도록 할 계획입니다.
이러한 언어 변경은 하위 호환성을 유지하지 않습니다.
우리는 언어를 변경하기 위한 첫 번째 시도 단계로 이 vet 체크를 사용하고 있습니다.

#### 불가능한 인터페이스 변환에 대한 새로운 경고 {#vet-impossible-interface}

<!-- CL 218779, 232660 -->
이제 `vet` 도구는 한 인터페이스 타입에서 다른 인터페이스 타입으로의 타입 단언(type assertion)이 항상 실패할 경우 경고를 표시합니다.
이는 두 인터페이스 타입이 동일한 이름의 메서드를 구현하지만, 타입 시그니처가 서로 다를 때 발생합니다.

항상 실패하는 타입 단언(type assertion)을 작성할 이유는 없으므로, 이 vet 체크를 트리거하는 모든 코드는 수정되어야 합니다.

이 새로운 vet 체크는 `go` `test`를 사용할 때 기본적으로 활성화됩니다.

우리는 향후 Go 릴리스에서 불가능한 인터페이스 타입 단언(interface type assertions)을 금지하는 것을 고려하고 있습니다.
이러한 언어 변경 사항은 하위 호환성을 유지하지 않습니다.
우리는 언어를 변경하기 위한 첫 번째 시험 단계로 이 vet 체크를 사용하고 있습니다.

## 런타임 {#runtime}

<!-- CL 221779 -->
`panic`이 다음 중 하나에서 파생된 타입의 값과 함께 호출되면: `bool`, `complex64`, `complex128`, `float32`, `float64`,
`int`, `int8`, `int16`, `int32`, `int64`, `string`,
`uint`, `uint8`, `uint16`, `uint32`, `uint64`, `uintptr`,
단순히 주소만 출력되는 대신 해당 값이 출력됩니다.
이전에는 정확히 이 타입들에 해당하는 값에 대해서만 이 동작이 적용되었습니다.

<!-- CL 228900 -->
Unix 시스템에서 `kill` 명령어나 `kill` 시스템 콜을 사용하여 Go 프로그램에 `SIGSEGV`, `SIGBUS` 또는 `SIGFPE` 시그널을 보냈을 때, 해당 시그널이 [`os/signal.Notify`](/pkg/os/signal/#Notify)를 통해 처리되지 않고 있다면 이제 Go 프로그램은 스택 트레이스와 함께 안정적으로 크래시(crash)됩니다. 이전 릴리스에서는 이 동작이 예측 불가능했습니다.

<!-- CL 221182, CL 229998 -->
작은 객체의 할당 성능이 높은 코어 수에서 훨씬 더 향상되었으며, 최악의 경우의 지연 시간(worst-case latency)이 감소했습니다.

<!-- CL 216401 -->
작은 정수 값을 인터페이스 값으로 변환할 때 더 이상 할당(allocation)이 발생하지 않습니다.

<!-- CL 216818 -->
이제 닫힌 채널에서의 non-blocking receive 성능이 열린 채널에서의 non-blocking receive 성능만큼 향상되었습니다.

## 컴파일러 {#compiler}

<!-- CL 229578 -->
`unsafe` 패키지의 [안전 규칙](/pkg/unsafe/#Pointer)에 따라 특정 함수를 호출할 때 `unsafe.Pointer`를 `uintptr`로 변환하는 것이 허용됩니다. 이전에는 일부 경우에 컴파일러가 여러 번의 연속된 변환(예: `syscall.Syscall(…,` `uintptr(uintptr(ptr)),` `…)` )을 허용했습니다. 이제 컴파일러는 정확히 한 번의 변환만을 요구합니다. 여러 번의 변환을 사용했던 코드는 안전 규칙을 충족하도록 업데이트해야 합니다.

<!-- CL 230544, CL 231397 -->
Go 1.15는 특정 유형의 GC 메타데이터를 제거하고 사용하지 않는 타입 메타데이터를 더 적극적으로 제거함으로써, Go 1.14 대비 일반적인 바이너리 크기를 약 5% 줄였습니다.

<!-- CL 219357, CL 231600 -->
이제 툴체인은 함수를 32바이트 경계로 정렬하고 점프 명령어를 패딩함으로써 `GOARCH=amd64`에서 [Intel CPU erratum SKX102](https://www.intel.com/content/www/us/en/support/articles/000055650/processors.html) 문제를 완화합니다. 이러한 패딩으로 인해 바이너리 크기가 증가하지만, 이는 위에서 언급한 바이너리 크기 개선 사항들로 충분히 상쇄됩니다.

<!-- CL 222661 -->
Go 1.15에서는 Spectre 완화 조치를 활성화할 수 있도록 컴파일러와 어셈블러 모두에 `-spectre` 플래그가 추가되었습니다.
이 플래그는 거의 필요하지 않으며, 주로 "심층 방어(defense in depth)" 메커니즘으로 제공됩니다.
자세한 내용은 [Spectre 위키 페이지](/wiki/Spectre)를 참조하세요.

<!-- CL 228578 -->
이제 컴파일러는 적용된 선언에 대해 아무런 의미가 없는 `//go:` 컴파일러 지시어(directives)가 사용될 경우 "misplaced compiler directive" 에러를 발생시키며 거부합니다. 이전에는 이렇게 잘못 적용된 지시어들이 제대로 작동하지 않았지만, 컴파일러가 이를 묵묵히 무시해 왔습니다.

<!-- CL 206658, CL 205066 -->
컴파일러의 `-json` 최적화 로깅이 이제 큰 크기(>= 128바이트)의 복사(copy)를 보고하며, 탈출 분석(escape analysis) 결정에 대한 설명을 포함합니다.

## 링커 (Linker) {#linker}

이번 릴리스에는 Go 링커에 대한 상당한 개선 사항이 포함되어 있으며, 이를 통해 링커 리소스 사용량(시간 및 메모리 모두)을 줄이고 코드의 견고성과 유지보수성을 향상시켰습니다.

대표적인 대규모 Go 프로그램 세트의 경우, `amd64` 아키텍처에서 실행되는 `ELF` 기반 OS(Linux, FreeBSD, NetBSD, OpenBSD, Dragonfly 및 Solaris)에서 링크 속도가 평균 20% 더 빠르고 메모리 사용량은 30% 더 적으며, 다른 아키텍처/OS 조합에서도 이에 못지않은 개선이 이루어졌습니다.

링커 성능 향상의 핵심 기여 요인은 새롭게 설계된 오브젝트 파일 포맷과, 동시성을 높이기 위해 내부 단계들을 개편한 것(예: 심볼에 대한 재배치(relocation)를 병렬로 적용)입니다. Go 1.15의 오브젝트 파일은 1.14 버전의 파일보다 크기가 약간 더 큽니다.

이 변경 사항들은 [Go 링커를 현대화](/s/better-linker)하기 위한 다중 릴리스 프로젝트의 일부이며, 이는 향후 릴리스에서 추가적인 링커 개선이 이루어질 예정임을 의미합니다.

<!-- CL 207877 -->
이제 `linux/amd64` 및 `linux/arm64`에서 `-buildmode=pie` 설정 시 링커가 기본적으로 내부 링킹 모드(internal linking mode)를 사용하므로, 해당 구성에서 더 이상 C 링커가 필요하지 않습니다. (Go 1.14에서 `-buildmode=pie` 시 기본값이었던) 외부 링킹 모드(external linking mode)는 여전히 `-ldflags=-linkmode=external` 플래그를 통해 요청할 수 있습니다.

## Objdump {#objdump}

<!-- CL 225459 -->
이제 [objdump](/cmd/objdump/) 도구에서 `-gnu` 플래그를 사용하여 GNU 어셈블러 구문으로 디스어셈블하는 기능을 지원합니다.

## 표준 라이브러리 {#library}

### 새로운 내장 tzdata 패키지 {#time_tzdata}

<!-- CL 224588 -->
Go 1.15에는 프로그램에 시간대(timezone) 데이터베이스를 내장할 수 있게 해주는 새로운 패키지인 [`time/tzdata`](/pkg/time/tzdata/)가 포함되었습니다.
이 패키지를 (`import _ "time/tzdata"`와 같이) 임포트하면 로컬 시스템에 시간대 데이터베이스가 없더라도 프로그램이 시간대 정보를 찾을 수 있습니다.
또한 `-tags timetzdata` 옵션을 사용하여 빌드함으로써 시간대 데이터베이스를 내장할 수도 있습니다.
두 방법 모두 프로그램의 크기를 약 800 KB 정도 증가시킵니다.

### Cgo {#cgo}

<!-- CL 235817 -->
Go 1.15는 C 타입인 `EGLConfig`를 Go 타입인 `uintptr`로 변환합니다. 이 변경 사항은 Go 1.12 및 그 이후 버전에서 `EGLDisplay`, Darwin의 CoreFoundation 및 Java의 JNI 타입을 처리하는 방식과 유사합니다. 자세한 내용은 [cgo 문서](/cmd/cgo/#hdr-Special_cases)를 참조하세요.

<!-- CL 250940 -->
Go 1.15.3 및 이후 버전부터 cgo는 Go 코드에서 정의되지 않은 구조체 타입(단순히 `struct S;` 등으로 정의된 C 구조체 등)을 스택이나 힙에 할당하는 것을 허용하지 않습니다.
Go 코드는 해당 타입에 대한 포인터만 사용할 수 있습니다.
이러한 구조체의 인스턴스를 할당하여 포인터나 전체 구조체 값을 C 코드로 전달하는 것은 항상 안전하지 않았으며 정상적으로 작동할 가능성이 낮았습니다. 이제 이는 금지됩니다.
해결 방법은 Go 코드를 포인터만 사용하도록 재작성하거나, 적절한 C 헤더 파일을 포함하여 Go 코드가 구조체의 전체 정의를 인식할 수 있도록 하는 것입니다.

### X.509 CommonName 지원 중단 {#commonname}

<!-- CL 231379 -->
Subject Alternative Names가 없을 때 X.509 인증서의 `CommonName` 필드를 호스트 이름으로 처리하던 지원 중단된 레거시 동작이 이제 기본적으로 비활성화되었습니다. `GODEBUG` 환경 변수에 `x509ignoreCN=0` 값을 추가하여 일시적으로 다시 활성화할 수 있습니다.

`CommonName`이 유효하지 않은 호스트 이름인 경우, `GODEBUG` 설정과 관계없이 항상 무시된다는 점에 유의하십시오. 유효하지 않은 이름에는 문자, 숫자, 하이픈, 언더스코어 이외의 문자가 포함된 이름, 빈 레이블이 있거나 끝에 점이 붙은 이름이 포함됩니다.

### 라이브러리의 소규모 변경 사항 {#minor_library_changes}

언제나 그렇듯, Go 1의 [호환성 약속](/doc/go1compat)을 염두에 둔 다양한 소규모 변경 사항과 업데이트가 라이브러리에 적용되었습니다.

#### [bufio](/pkg/bufio/)

<!-- CL 225357, CL 225557 -->
[`Scanner`](/pkg/bufio/#Scanner)를 사용할 때 `Read`에서 잘못된 음수를 반환하는 유효하지 않은 [`io.Reader`](/pkg/io/#Reader)와 함께 사용하면, `Scanner`는 더 이상 패닉(panic)을 발생시키지 않고 대신 새로운 에러인 [`ErrBadReadCount`](/pkg/bufio/#ErrBadReadCount)를 반환합니다.

<!-- bufio -->

#### [context](/pkg/context/)

<!-- CL 223777 -->
이제 nil 부모를 사용하여 파생된 `Context`를 생성하는 것이 명시적으로 금지됩니다. [`WithValue`](/pkg/context/#WithValue), [`WithDeadline`](/pkg/context/#WithDeadline), 또는 [`WithCancel`](/pkg/context/#WithCancel) 함수를 사용하여 그렇게 시도하면 패닉(panic)이 발생합니다.

제공해주신 컨텍스트가 없습니다. 번역할 영문 Markdown 내용을 입력해 주세요. 신속하고 정확하게 기술 번역을 진행해 드리겠습니다.

#### [crypto](/pkg/crypto/)

<!-- CL 231417, CL 225460 -->
[`crypto/rsa`](/pkg/crypto/rsa/),
[`crypto/ecdsa`](/pkg/crypto/ecdsa/), 및
[`crypto/ed25519`](/pkg/crypto/ed25519/) 패키지의
`PrivateKey`와 `PublicKey` 타입에 키의 동등성을 비교하거나 공개 키를 위한 타입 안전한 인터페이스를 만들기 위한 `Equal` 메서드가 추가되었습니다. 이 메서드의 시그니처는
[`go-cmp`의 equality 정의](https://pkg.go.dev/github.com/google/go-cmp/cmp#Equal)와 호환됩니다.

<!-- CL 224937 -->
이제 [`Hash`](/pkg/crypto/#Hash)가 [`fmt.Stringer`](/pkg/fmt/#Stringer)를 구현합니다.

<!-- crypto -->

#### [crypto/ecdsa](/pkg/crypto/ecdsa/)

<!-- CL 217940 -->
새로운 [`SignASN1`](/pkg/crypto/ecdsa/#SignASN1)
및 [`VerifyASN1`](/pkg/crypto/ecdsa/#VerifyASN1)
함수를 통해 표준 ASN.1 DER 인코딩으로 ECDSA 서명을 생성하고 검증할 수 있습니다.

<!-- crypto/ecdsa -->

#### [crypto/elliptic](/pkg/crypto/elliptic/)

<!-- CL 202819 -->
새로운 [`MarshalCompressed`](/pkg/crypto/elliptic/#MarshalCompressed) 및 [`UnmarshalCompressed`](/pkg/crypto/elliptic/#UnmarshalCompressed) 함수를 사용하여 NIST 타원 곡선 점을 압축 형식으로 인코딩하고 디코딩할 수 있습니다.

<!-- crypto/elliptic -->

#### [crypto/rsa](/pkg/crypto/rsa/)

<!-- CL 226203 -->
[`VerifyPKCS1v15`](/pkg/crypto/rsa/#VerifyPKCS1v15)은(는) 이제 RFC 8017에 따라 앞부분의 0이 누락된 잘못된 짧은 서명을 거부합니다.

<!-- crypto/rsa -->

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 214977 -->
새로운 [`Dialer`](/pkg/crypto/tls/#Dialer) 타입과 그 [`DialContext`](/pkg/crypto/tls/#Dialer.DialContext) 메서드를 사용하면, TLS 서버와의 연결 및 핸드셰이크 모두에 컨텍스트(context)를 사용할 수 있습니다.

<!-- CL 229122 -->
[`Config`](/pkg/crypto/tls/#Config) 타입의 새로운 [`VerifyConnection`](/pkg/crypto/tls/#Config.VerifyConnection) 콜백을 통해 모든 연결에 대해 사용자 정의 검증 로직을 사용할 수 있습니다. 이 콜백은 피어 인증서, SCT, 스테이플드(stapled) OCSP 응답이 포함된 [`ConnectionState`](/pkg/crypto/tls/#ConnectionState)에 접근할 수 있습니다.

<!-- CL 230679 -->
자동 생성된 세션 티켓 키가 이제 24시간마다 자동으로 교체되며, 유효 기간은 7일로 설정되어 순방향 비밀성(forward secrecy)에 미치는 영향을 제한합니다.

<!-- CL 231317 -->
세션 키가 재개된 연결(resumed connections)에 재사용되는 TLS 1.2 및 이전 버전의 세션 티켓 수명은 이제 7일로 제한됩니다. 이는 순방향 비밀성(forward secrecy)에 미치는 영향을 제한하기 위함입니다.

<!-- CL 231038 -->
RFC 8446에 명시된 클라이언트 측 다운그레이드 보호 확인(downgrade protection checks)이 이제 강제 적용됩니다. 이로 인해 권한 없는 다운그레이드 공격과 유사하게 동작하는 미들박스(middlebox)를 만나는 클라이언트의 경우 연결 오류가 발생할 가능성이 있습니다.

<!-- CL 208226 -->
[`SignatureScheme`](/pkg/crypto/tls/#SignatureScheme),
[`CurveID`](/pkg/crypto/tls/#CurveID), 및
[`ClientAuthType`](/pkg/crypto/tls/#ClientAuthType)가
이제 [`fmt.Stringer`](/pkg/fmt/#Stringer)를 구현합니다.

<!-- CL 236737 -->
[`ConnectionState`](/pkg/crypto/tls/#ConnectionState)의
`OCSPResponse` 및 `SignedCertificateTimestamps` 필드가
이제 클라이언트 측에서 재개된 연결(resumed connections)에서도 다시 채워집니다.

<!-- CL 227840 -->
[`tls.Conn`](/pkg/crypto/tls/#Conn)은
이제 영구적으로 단절된 연결에 대해 불투명한(opaque) 에러를 반환하며, 내부적으로 일시적인
[`net.Error`](/pkg/net/http/#Error)를 래핑합니다.
원본 `net.Error`에 접근하려면 타입 단언(type assertion) 대신
[`errors.As`](/pkg/errors/#As)(또는
[`errors.Unwrap`](/pkg/errors/#Unwrap))를 사용하십시오.

<!-- crypto/tls -->

#### [crypto/x509](/pkg/crypto/x509/)

<!-- CL 231378, CL 231380, CL 231381 -->
인증서의 이름이나 검증 대상 이름([`VerifyOptions.DNSName`](/pkg/crypto/x509/#VerifyOptions.DNSName) 또는 [`VerifyHostname`](/pkg/crypto/x509/#Certificate.VerifyHostname) 사용 시) 중 어느 하나라도 유효하지 않은 경우, 이제 추가 처리 없이(와일드카드 적용이나 trailing dot 제거 없이) 대소문자를 구분하지 않고 비교됩니다.
유효하지 않은 이름에는 문자, 숫자, 하이픈, 언더스코어 이외의 문자가 포함된 이름, 비어 있는 레이블이 포함된 이름, 그리고 trailing dot이 있는 인증서 이름이 포함됩니다.

<!-- CL 217298 -->
새로운 [`CreateRevocationList`](/pkg/crypto/x509/#CreateRevocationList) 함수와 [`RevocationList`](/pkg/crypto/x509/#RevocationList) 타입은 RFC 5280을 준수하는 X.509 v2 인증서 폐기 목록(Certificate Revocation Lists) 생성을 가능하게 합니다.

<!-- CL 227098 -->
[`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate)는 이제 템플릿이 CA이고 `SubjectKeyId`가 명시적으로 지정되지 않은 경우, 이를 자동으로 생성합니다.

<!-- CL 228777 -->
[`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate)
이제 템플릿에 `MaxPathLen`이 지정되어 있지만 CA가 아닌 경우 에러를 반환합니다.

<!-- CL 205237 -->
macOS 이외의 Unix 시스템에서, 이제 `SSL_CERT_DIR`
환경 변수에 콜론(`:`)으로 구분된 목록을 사용할 수 있습니다.

<!-- CL 227037 -->
macOS에서 바이너리는 이제 cgo 사용 가능 여부와 관계없이 시스템 신뢰 루트(trust roots)를 추출하기 위해 항상 `Security.framework`에 링크됩니다. 이를 통해 결과적인 동작이 OS 검증기(verifier)와 더 일관되게 유지될 것입니다.

<!-- crypto/x509 -->

#### [crypto/x509/pkix](/pkg/crypto/x509/pkix/)

<!-- CL 229864, CL 240543 -->
[`Name.String`](/pkg/crypto/x509/pkix/#Name.String)은 이제 [`ExtraNames`](/pkg/crypto/x509/pkix/#Name.ExtraNames)가 nil인 경우 [`Names`](/pkg/crypto/x509/pkix/#Name.Names)에서 비표준 속성을 출력합니다.

<!-- crypto/x509/pkix -->

#### [database/sql](/pkg/database/sql/)

<!-- CL 145758 -->
새로운 [`DB.SetConnMaxIdleTime`](/pkg/database/sql/#DB.SetConnMaxIdleTime)
메서드를 사용하면 연결의 전체 수명과 관계없이, 일정 시간 동안 유휴 상태(idle)였던 연결을 연결 풀에서 제거할 수 있습니다. [`DBStats.MaxIdleTimeClosed`](/pkg/database/sql/#DBStats.MaxIdleTimeClosed)
필드는 `DB.SetConnMaxIdleTime`으로 인해 닫힌 연결의 총 횟수를 보여줍니다.

<!-- CL 214317 -->
새로운 [`Row.Err`](/pkg/database/sql/#Row.Err) getter를 통해
`Row.Scan`을 호출하지 않고도 쿼리 오류를 확인할 수 있습니다.

<!-- database/sql -->

#### [database/sql/driver](/pkg/database/sql/driver/)

<!-- CL 174122 -->
새로운 [`Validator`](/pkg/database/sql/driver/#Validator) 인터페이스는 `Conn`에서 구현될 수 있으며, 이를 통해 드라이버는 연결이 유효한지 또는 폐기되어야 하는지를 알릴 수 있습니다.

<!-- database/sql/driver -->

#### [debug/pe](/pkg/debug/pe/)

<!-- CL 222637 -->
이제 이 패키지는 PE 파일 형식에서 사용되는 `IMAGE_FILE`, `IMAGE_SUBSYSTEM` 및 `IMAGE_DLLCHARACTERISTICS` 상수를 정의합니다.

<!-- debug/pe -->

#### [encoding/asn1](/pkg/encoding/asn1/)

<!-- CL 226984 -->
[`Marshal`](/pkg/encoding/asn1/#Marshal)이 이제 X.690 DER에 따라 SET OF의 구성 요소를 정렬합니다.

<!-- CL 227320 -->
[`Unmarshal`](/pkg/encoding/asn1/#Unmarshal)은 이제 X.690 DER에 따라 최소로 인코딩되지 않은 태그 및 객체 식별자(Object Identifiers)를 거부합니다.

<!-- encoding/asn1 -->

#### [encoding/json](/pkg/encoding/json/)

<!-- CL 199837 -->
이제 이 패키지는 디코딩 시 중첩 최대 깊이에 대한 내부 제한을 가집니다. 이를 통해 깊게 중첩된 입력값이 대량의 스택 메모리를 사용하거나, 심지어 "goroutine stack exceeds limit" 패닉을 발생시킬 가능성을 줄여줍니다.

<!-- encoding/json -->

#### [flag](/pkg/flag/)

<!-- CL 221427 -->
`flag` 패키지에서 `-h` 또는 `-help` 플래그를 감지했을 때 해당 플래그가 정의되어 있지 않다면, 이제 사용법(usage) 메시지를 출력합니다.
[`FlagSet`](/pkg/flag/#FlagSet)이 [`ExitOnError`](/pkg/flag/#ExitOnError)와 함께 생성된 경우, [`FlagSet.Parse`](/pkg/flag/#FlagSet.Parse)는 상태 코드 2로 종료되었습니다. 이번 릴리스에서는 `-h` 또는 `-help`에 대한 종료 상태 코드가 0으로 변경되었습니다. 특히, 이는 명령줄 플래그의 기본 처리 방식에 적용됩니다.

#### [fmt](/pkg/fmt/)

<!-- CL 215001 -->
이제 출력 동사 `%#g`와 `%#G`가 부동 소수점 값의 trailing zero(후행 제로)를 유지합니다.

<!-- fmt -->

#### [go/format](/pkg/go/format/)

<!-- golang.org/issue/37476, CL 231461, CL 240683 -->
이제 [`Source`](/pkg/go/format/#Source) 및 [`Node`](/pkg/go/format/#Node) 함수는 Go 소스 코드 포맷팅의 일부로 숫자 리터럴의 접두사와 지수를 정준화(canonicalize)합니다. 이는 [Go 1.13부터](/doc/go1.13#gofmt) 구현된 [`gofmt`](/pkg/cmd/gofmt/) 명령어의 동작과 일치합니다.

<!-- go/format -->

#### [html/template](/pkg/html/template/)

<!-- CL 226097 -->
이제 패키지의 모든 JavaScript 및 JSON 컨텍스트에서 유니코드 이스케이프(`\uNNNN`)를 사용합니다. 이를 통해 `application/ld+json` 및 `application/json` 컨텍스트에서의 이스케이프 오류를 수정했습니다.

<!-- html/template -->

#### [io/ioutil](/pkg/io/ioutil/)

<!-- CL 212597 -->
[`TempDir`](/pkg/io/ioutil/#TempDir) 및
[`TempFile`](/pkg/io/ioutil/#TempFile)
이제 경로 구분자(path separator)가 포함된 패턴을 거부합니다.
즉, `ioutil.TempFile("/tmp",` `"../base*")`와 같은 호출은 더 이상 성공하지 않습니다.
이를 통해 의도치 않은 디렉터리 탐색(directory traversal)을 방지합니다.

<!-- io/ioutil -->

#### [math/big](/pkg/math/big/)

<!-- CL 230397 -->
새로운 [`Int.FillBytes`](/pkg/math/big/#Int.FillBytes) 메서드를 통해 고정 크기로 미리 할당된 바이트 슬라이스로 직렬화할 수 있습니다.

<!-- math/big -->

#### [math/cmplx](/pkg/math/cmplx/)

<!-- CL 220689 -->
이 패키지의 함수들은 무한대, NaN, 부호 있는 0과 같은 특수 인자 처리와 관련하여 C99 표준(Annex G IEC 60559 호환 복소수 산술)을 준수하도록 업데이트되었습니다.

<!-- math/cmplx-->

#### [net](/pkg/net/)

<!-- CL 228645 -->
[`Conn.SetDeadline`](/pkg/net/#Conn),
`Conn.SetReadDeadline`,
또는 `Conn.SetWriteDeadline` 메서드에 의해 설정된 데드라인을 I/O 작업이 초과하는 경우, 이제 [`os.ErrDeadlineExceeded`](/pkg/os/#ErrDeadlineExceeded)이거나 이를 래핑한 에러를 반환합니다.
이를 통해 에러가 데드라인 초과로 인한 것인지 신뢰성 있게 감지할 수 있습니다.
이전 릴리스에서는 에러의 `Timeout` 메서드를 호출하는 것을 권장했으나, I/O 작업은 데드라인이 초과되지 않았음에도 `Timeout`이 `true`를 반환하는 에러를 반환할 수 있습니다.

<!-- CL 228641 -->
새로운 [`Resolver.LookupIP`](/pkg/net/#Resolver.LookupIP)
메서드는 네트워크 특정(network-specific) IP 조회와 컨텍스트(context) 수용을 모두 지원합니다.

#### [net/http](/pkg/net/http/)

<!-- CL 231418, CL 231419 -->
요청 스머글링(request smuggling) 공격에 대한 강화 조치로 파싱 규칙이 더 엄격해졌습니다.
이제 비-ASCII 공백 문자는 SP 및 HTAB처럼 더 이상 트리밍되지 않으며, `Transfer-Encoding`의 "`identity`" 지원이 중단되었습니다.

<!-- net/http -->

#### [net/http/httputil](/pkg/net/http/httputil/)

<!-- CL 230937 -->
[`ReverseProxy`](/pkg/net/http/httputil/#ReverseProxy)는 이제 들어오는 `Request.Header` 맵 엔트리의 해당 필드가 `nil`인 경우 `X-Forwarded-For` 헤더를 수정하지 않는 기능을 지원합니다.

<!-- CL 224897 -->
[`ReverseProxy`](/pkg/net/http/httputil/#ReverseProxy)에서 처리하는 Switching Protocol(WebSocket 등) 요청이 취소될 때, 이제 백엔드 연결이 올바르게 닫힙니다.

#### [net/http/pprof](/pkg/net/http/pprof/)

<!-- CL 147598, CL 229537 -->
이제 모든 프로파일 엔드포인트가 "`seconds`" 파라미터를 지원합니다. 이 파라미터가 지정되면, 엔드포인트는 지정된 초 동안 프로파일링을 수행하고 그 차이점을 보고합니다. `cpu` 프로파일 및 트레이스 엔드포인트에서 "`seconds`" 파라미터의 의미는 변경되지 않았습니다.

#### [net/url](/pkg/net/url/)

<!-- CL 227645 -->
새로운 [`URL`](/pkg/net/url/#URL) 필드인 `RawFragment`와 메서드 [`EscapedFragment`](/pkg/net/url/#URL.EscapedFragment)는 특정 프래그먼트(fragment)의 정확한 인코딩에 대한 세부 정보와 제어 기능을 제공합니다. 이는 `RawPath` 및 [`EscapedPath`](/pkg/net/url/#URL.EscapedPath)와 유사합니다.

<!-- CL 207082 -->
새로운 [`URL`](/pkg/net/url/#URL)
메서드인 [`Redacted`](/pkg/net/url/#URL.Redacted)는
비밀번호를 `xxxxx`로 대체한 문자열 형태의 URL을 반환합니다.

#### [os](/pkg/os/)

<!-- CL -->
I/O 작업이 [`File.SetDeadline`](/pkg/os/#File.SetDeadline), [`File.SetReadDeadline`](/pkg/os/#File.SetReadDeadline) 또는 [`File.SetWriteDeadline`](/pkg/os/#File.SetWriteDeadline) 메서드로 설정한 마감 시간을 초과하면, 이제 [`os.ErrDeadlineExceeded`](/pkg/os/#ErrDeadlineExceeded)이거나 이를 래핑하는 에러를 반환합니다. 이를 통해 에러가 마감 시간 초과로 인해 발생했는지 여부를 확실하게 감지할 수 있습니다.

이전 릴리스에서는 에러의 `Timeout` 메서드를 호출하는 것을 권장했으나, I/O 작업은 마감 시간이 초과되지 않았음에도 `Timeout`이 `true`를 반환하는 에러를 반환할 수 있습니다.

<!-- CL 232862 -->
이제 `os` 및 `net` 패키지는 `EINTR`로 실패하는 시스템 호출을 자동으로 재시도합니다. 이전에는 이로 인해 간헐적인 실패가 발생했으며, Go 1.14에서 비동기 선점(asynchronous preemption)이 추가되면서 이러한 현상이 더 빈번해졌습니다. 이제 이 과정은 투명하게 처리됩니다.

<!-- CL 229101 -->
이제 [`os.File`](/pkg/os/#File) 타입이 [`ReadFrom`](/pkg/os/#File.ReadFrom) 메서드를 지원합니다. 이를 통해 [`io.Copy`](/pkg/io/#Copy)를 사용하여 한 `os.File`에서 다른 `os.File`로 데이터를 복사할 때, 일부 시스템에서 `copy_file_range` 시스템 호출을 사용할 수 있게 됩니다. 이에 따라 [`io.CopyBuffer`](/pkg/io/#CopyBuffer)가 `os.File`로 복사할 때 제공된 버퍼를 항상 사용하지는 않게 됩니다. 프로그램에서 제공된 버퍼의 사용을 강제하려면 `io.CopyBuffer(struct{ io.Writer }{dst}, src, buf)`와 같이 작성하면 됩니다.

#### [plugin](/pkg/plugin/)

<!-- CL 182959 -->
이제 macOS의 `-buildmode=plugin`에 대해 DWARF 생성(기본적으로 활성화됨)이 지원됩니다.

<!-- CL 191617 -->
이제 `freebsd/amd64`에서 `-buildmode=plugin`을 사용한 빌드가 지원됩니다.

#### [reflect](/pkg/reflect/)

<!-- CL 228902 -->
이제 `reflect` 패키지는 모든 비공개(non-exported) 필드의 메서드 접근을 허용하지 않습니다. 이전에는 비공개 임베디드 필드의 메서드 접근이 허용되었습니다. 이전 동작에 의존하는 코드는 대신 이를 포함하는 변수의 승격된(promoted) 메서드에 접근하도록 업데이트해야 합니다.

#### [regexp](/pkg/regexp/)

<!-- CL 187919 -->
새로운 [`Regexp.SubexpIndex`](/pkg/regexp/#Regexp.SubexpIndex) 메서드는 정규 표현식 내에서 주어진 이름을 가진 첫 번째 하위 표현식(subexpression)의 인덱스를 반환합니다.

<!-- regexp -->

#### [runtime](/pkg/runtime/)

<!-- CL 216557 -->
[`ReadMemStats`](/pkg/runtime/#ReadMemStats) 및
[`GoroutineProfile`](/pkg/runtime/#GoroutineProfile)을 포함한 여러 함수가
더 이상 가비지 컬렉션이 진행 중일 때 블록(block)되지 않습니다.

#### [runtime/pprof](/pkg/runtime/pprof/)

<!-- CL 189318 -->
이제 goroutine 프로파일에 프로파일링 시점의 각 goroutine과 연결된 프로파일 레이블이 포함됩니다. 이 기능은 `debug=2`로 보고되는 프로파일에는 아직 구현되지 않았습니다.

#### [strconv](/pkg/strconv/)

<!-- CL 216617 -->
복소수 작업을 위해 [`FormatComplex`](/pkg/strconv/#FormatComplex)와 [`ParseComplex`](/pkg/strconv/#ParseComplex)가 추가되었습니다.

[`FormatComplex`](/pkg/strconv/#FormatComplex)는 복소수를 실수부 a와 허수부 b를 사용하여 (a+bi) 형태의 문자열로 변환합니다.

[`ParseComplex`](/pkg/strconv/#ParseComplex)는 문자열을 지정된 정밀도의 복소수로 변환합니다. `ParseComplex`는 `N+Ni` 형식의 복소수를 허용합니다.

<!-- strconv -->

#### [sync](/pkg/sync/)

<!-- CL 205899, golang.org/issue/33762 -->
새로운 메서드 [`Map.LoadAndDelete`](/pkg/sync/#Map.LoadAndDelete)는 키를 원자적으로 삭제하고, 값이 존재했다면 이전 값을 반환합니다.

<!-- CL 205899 -->
[`Map.Delete`](/pkg/sync/#Map.Delete)
메서드가 더 효율적입니다.

<!-- sync -->

#### [syscall](/pkg/syscall/)

<!-- CL 231638 -->
Unix 시스템에서 [`SysProcAttr`](/pkg/syscall/#SysProcAttr)를 사용하는 함수는 이제 `Setctty`와 `Foreground` 필드를 모두 설정하려는 시도를 거부합니다. 이는 두 필드가 모두 `Ctty` 필드를 사용하지만 서로 호환되지 않는 방식으로 사용하기 때문입니다. 기존 프로그램 중 두 필드를 모두 설정하는 경우는 거의 없을 것으로 예상됩니다.

이제 `Setctty` 필드를 설정하려면 `Ctty` 필드가 `ProcAttr.Files` 필드에 의해 결정된 자식 프로세스의 파일 디스크립터 번호로 설정되어야 합니다. 자식 디스크립터를 사용하는 방식은 항상 작동했지만, 부모 파일 디스크립터를 사용해도 우연히 작동하는 특정 사례들이 있었습니다. `Setctty`를 설정하는 일부 프로그램은 자식 디스크립터 번호를 사용하도록 `Ctty` 값을 변경해야 할 것입니다.

<!-- CL 220578 -->
이제 `windows/amd64`에서 부동 소수점 값을 반환하는 시스템 콜을 호출하는 것이 [가능합니다](/pkg/syscall/#Proc.Call).

#### [testing](/pkg/testing/)

<!-- golang.org/issue/28135 -->
`testing.T` 타입에 테스트 바이너리가 타임아웃을 초과하게 되는 시간을 보고하는 [`Deadline`](/pkg/testing/#T.Deadline) 메서드가 추가되었습니다.

<!-- golang.org/issue/34129 -->
이제 `TestMain` 함수에서 `os.Exit`를 반드시 호출할 필요가 없습니다. `TestMain` 함수가 반환되면, 테스트 바이너리가 `m.Run`에 의해 반환된 값으로 `os.Exit`를 호출합니다.

<!-- CL 226877, golang.org/issue/35998 -->
새로운 메서드 [`T.TempDir`](/pkg/testing/#T.TempDir)와 [`B.TempDir`](/pkg/testing/#B.TempDir)는 테스트가 끝날 때 자동으로 정리되는 임시 디렉터리를 반환합니다.

<!-- CL 229085 -->
`go` `test` `-v`는 이제 테스트 이름을 매 라인마다 출력하는 대신, 테스트 이름별로 출력을 그룹화합니다.

<!-- testing -->

#### [text/template](/pkg/text/template/)

<!-- CL 226097 -->
[`JSEscape`](/pkg/text/template/#JSEscape)가 이제 JSON과 호환되는 유니코드 이스케이프(`\u00XX`)를 일관되게 사용합니다.

<!-- text/template -->

#### [time](/pkg/time/)

<!-- CL 220424, CL 217362, golang.org/issue/33184 -->
새로운 메서드
[`Ticker.Reset`](/pkg/time/#Ticker.Reset)
은 티커(ticker)의 기간을 변경하는 기능을 지원합니다.

<!-- CL 227878 -->
에러를 반환할 때, 이제 [`ParseDuration`](/pkg/time/#ParseDuration)이 원래의 값을 따옴표로 감쌉니다.

<!-- time -->
