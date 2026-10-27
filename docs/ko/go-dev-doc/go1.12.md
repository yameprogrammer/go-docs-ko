<!--
참고: 이 문서 및 이 디렉토리의 다른 문서에서는
`hello` `world`와 같이 고정폭 구문을 비고정폭 공백으로 설정하는 관례를 따릅니다.
이러한 구문에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

<style>
  main ul li { margin: 0.5em 0; }
</style>

## Go 1.12 소개 {#introduction}

최신 Go 릴리스인 버전 1.12가 [Go 1.11](go1.11) 이후 6개월 만에 출시되었습니다.
변경 사항의 대부분은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언제나 그랬듯, 이번 릴리스는 Go 1의 [호환성 약속](/doc/go1compat)을 유지합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

언어 사양에는 변경 사항이 없습니다.

## 포트 {#ports}

<!-- CL 138675 -->
이제 `linux/arm64`에서 race detector가 지원됩니다.

Go 1.12는 이미 수명 종료(end-of-life)된 FreeBSD 10.x에서 지원되는 마지막 릴리스입니다. Go 1.13을 사용하려면 FreeBSD 11.2+ 또는 FreeBSD 12.0+가 필요합니다.
FreeBSD 12.0+는 `COMPAT_FREEBSD11` 옵션이 설정된 커널이 필요합니다(이는 기본 설정입니다).

<!-- CL 146898 -->
이제 `linux/ppc64`에서 cgo가 지원됩니다.

<!-- CL 146023 -->
이제 `GOOS`에 `hurd` 값이 추가되었으며, 이는 `gccgo`와 함께 사용되는 GNU/Hurd 시스템을 위해 예약되었습니다.

### Windows {#windows}

Go의 새로운 `windows/arm` 포트는 Raspberry Pi 3와 같은 32비트 ARM 칩 기반의 Windows 10 IoT Core에서 Go를 실행하는 것을 지원합니다.

### AIX {#aix}

Go는 이제 POWER8 아키텍처(`aix/ppc64`)의 AIX 7.2 및 이후 버전을 지원합니다. 외부 링킹(External linking), cgo, pprof 및 레이스 디텍터(race detector)는 아직 지원되지 않습니다.

### Darwin {#darwin}

Go 1.12는 macOS 10.10 Yosemite에서 실행 가능한 마지막 릴리스입니다.
Go 1.13부터는 macOS 10.11 El Capitan 또는 그 이후 버전이 필요합니다.

<!-- CL 141639 -->
이제 Darwin에서 syscall을 호출할 때 `libSystem`이 사용되며, 이를 통해 향후 macOS 및 iOS 버전과의 전방 호환성을 보장합니다. <!-- CL 153338 -->
`libSystem`으로의 전환으로 인해 프라이빗 API 사용에 대한 추가적인 App Store 검사가 발생했습니다. `syscall.Getdirentries`는 프라이빗으로 간주되므로, 이제 iOS에서 항상 `ENOSYS`와 함께 실패합니다.
또한, [`syscall.Setrlimit`](/pkg/syscall/#Setrlimit)은 과거에 성공했던 지점에서 `invalid` `argument`를 보고합니다. 이러한 결과는 Go에 국한된 것이 아니며, 사용자들은 앞으로 `libSystem` 구현과의 동작 일치(parity)를 예상해야 합니다.

## 도구 {#tools}

### `go tool vet` 더 이상 지원되지 않음 {#vet}

`go vet` 명령은 다양한 소스 코드 분석 도구의 기반으로 사용될 수 있도록 재작성되었습니다. 자세한 내용은 [golang.org/x/tools/go/analysis](https://godoc.org/golang.org/x/tools/go/analysis) 패키지를 참조하십시오. 이에 따른 부수적인 결과로 `go tool vet`은 더 이상 지원되지 않습니다. `go tool vet`을 사용하는 외부 도구는 `go vet`을 사용하도록 변경해야 합니다. `go tool vet` 대신 `go vet`을 사용하는 것은 지원되는 모든 Go 버전에서 작동할 것입니다.

이번 변경 사항의 일환으로, 실험적 옵션인 `-shadow`를 더 이상 `go vet`에서 사용할 수 없습니다. 변수 섀도잉(variable shadowing) 확인은 이제 다음을 사용하여 수행할 수 있습니다.

```bash
go get -u golang.org/x/tools/go/analysis/passes/shadow/cmd/shadow
	go vet -vettool=$(which shadow)
```

### Tour {#tour}

<!-- CL 152657 -->
Go tour는 더 이상 메인 바이너리 배포판에 포함되지 않습니다. 투어를 로컬에서 실행하려면 `go` `tool` `tour`를 실행하는 대신, 다음과 같이 수동으로 설치하십시오:

```bash
go get -u golang.org/x/tour
	tour
```

### 빌드 캐시 요구사항 {#gocache}

[빌드 캐시](/cmd/go/#hdr-Build_and_test_caching)는 이제 `$GOPATH/pkg`를 제거하기 위한 단계로 필수적으로 사용됩니다. 환경 변수 `GOCACHE=off`를 설정하면 캐시에 기록하는 `go` 명령어가 실패하게 됩니다.

### 바이너리 전용 패키지 {#binary-only}

Go 1.12은 바이너리 전용 패키지(binary-only packages)를 지원하는 마지막 릴리스입니다.

### Cgo {#cgo}

Go 1.12는 C 타입 `EGLDisplay`를 Go 타입 `uintptr`로 변환합니다.
이 변경 사항은 Go 1.10 및 최신 버전에서 Darwin의 CoreFoundation 및 Java의 JNI 타입을 처리하는 방식과 유사합니다. 자세한 내용은 [cgo 문서](/cmd/cgo/#hdr-Special_cases)를 참조하십시오.

<!-- CL 152657 -->
Cgo를 사용하는 패키지에서 더 이상 Mangled C 이름을 허용하지 않습니다. 대신 Cgo 이름을 사용하십시오. 예를 들어, cgo가 생성하는 mangled 이름인 `_Ctype_char` 대신 문서화된 cgo 이름인 `C.char`를 사용하십시오.

### 모듈 {#modules}

<!-- CL 148517 -->
`GO111MODULE`가 `on`으로 설정된 경우, 이제 `go` 명령어는 모듈 디렉토리 외부에서도 모듈 인식(module-aware) 작업을 지원합니다. 단, 해당 작업이 현재 디렉토리를 기준으로 임포트 경로(import paths)를 해석하거나 `go.mod` 파일을 명시적으로 수정할 필요가 없어야 합니다.
`go`&nbsp;`get`, `go`&nbsp;`list`, 그리고 `go`&nbsp;`mod`&nbsp;`download`와 같은 명령어들은 요구 사항(requirements)이 처음에 비어 있는 모듈 내에 있는 것처럼 동작합니다.
이 모드에서 `go`&nbsp;`env`&nbsp;`GOMOD`는 시스템의 null 디바이스 (`/dev/null` 또는 `NUL`)를 보고합니다.

<!-- CL 146382 -->
모듈을 다운로드하고 추출하는 `go` 명령어를 이제 동시에(concurrently) 안전하게 실행할 수 있습니다.
모듈 캐시(`GOPATH/pkg/mod`)는 파일 잠금(file locking)을 지원하는 파일 시스템에 위치해야 합니다.

<!-- CL 147282, 147281 -->
`go.mod` 파일의 `go` 지시어는 이제 해당 모듈 내의 파일에서 사용하는 언어 버전을 나타냅니다.
기존 버전이 지정되어 있지 않은 경우, 현재 릴리스(`go`&nbsp;`1.12`)로 설정됩니다.
모듈의 `go` 지시어가 사용 중인 툴체인보다 _최신_ 버전을 지정한 경우, `go` 명령은 관계없이 패키지 빌드를 시도하며, 빌드가 실패한 경우에만 버전 불일치를 알립니다.

<!-- CL 147282, 147281 -->
`go` 지시문의 사용 방식이 변경됨에 따라, Go 1.12를 사용하여 모듈을 빌드하고 `go.mod` 파일에 `go 1.12`를 기록한 경우, Go 1.11부터 Go 1.11.3 버전으로 동일한 모듈을 빌드하려고 하면 에러가 발생합니다.
Go 1.11.4 이상 버전이나 Go 1.11보다 오래된 릴리스 버전에서는 정상적으로 작동합니다.
반드시 Go 1.11에서 1.11.3 버전을 사용해야 하는 경우, Go 1.12 go 툴에서 `go mod edit -go=1.11` 명령어를 통해 언어 버전을 1.11로 설정함으로써 이 문제를 피할 수 있습니다.

<!-- CL 152739 -->
활성 모듈을 사용하여 임포트(import)를 해결할 수 없는 경우, `go` 명령은 이제 모듈 캐시와 일반적인 네트워크 소스를 참조하기 전에 메인 모듈의 `replace` 지시문에 언급된 모듈을 먼저 사용하려고 시도합니다.
일치하는 대체 항목이 발견되었으나 `replace` 지시문에 버전이 지정되지 않은 경우, `go` 명령은 제로 `time.Time`에서 파생된 유사 버전(pseudo-version)(예: `v0.0.0-00010101000000-000000000000`)을 사용합니다.

### 컴파일러 툴체인 {#compiler}

<!-- CL 134155, 134156 -->
컴파일러의 라이브 변수 분석(live variable analysis)이 개선되었습니다. 이로 인해 이번 릴리스에서는 이전 릴리스보다 파이널라이저(finalizer)가 더 빨리 실행될 수 있습니다. 만약 이것이 문제가 된다면, 적절한 위치에 [`runtime.KeepAlive`](/pkg/runtime/#KeepAlive) 호출을 추가하는 것을 고려하십시오.

<!-- CL 147361 -->
이제 다른 함수를 호출하는 것 외에는 아무것도 하지 않는 함수를 포함하여, 더 많은 함수가 기본적으로 인라이닝(inlining) 대상이 됩니다.
이러한 추가적인 인라이닝으로 인해, [`runtime.Callers`](/pkg/runtime/#Callers)의 결과를 직접 반복문으로 처리하는 대신 [`runtime.CallersFrames`](/pkg/runtime/#CallersFrames)를 사용하는 것이 더욱 중요해졌습니다.

```
// 더 이상 올바르게 작동하지 않는 이전 코드입니다 (인라인된 호출 프레임을 누락하게 됩니다).
var pcs [10]uintptr
n := runtime.Callers(1, pcs[:])
for _, pc := range pcs[:n] {
	f := runtime.FuncForPC(pc)
	if f != nil {
		fmt.Println(f.Name())
	}
}
```

```
// 올바르게 작동하는 새로운 코드입니다.
var pcs [10]uintptr
n := runtime.Callers(1, pcs[:])
frames := runtime.CallersFrames(pcs[:n])
for {
	frame, more := frames.Next()
	fmt.Println(frame.Function)
	if !more {
		break
	}
}
```

<!-- CL 153477 -->
메서드 표현식(method expressions)을 구현하기 위해 컴파일러가 생성하는 래퍼(wrapper)들이 더 이상 [`runtime.CallersFrames`](/pkg/runtime/#CallersFrames) 및 [`runtime.Stack`](/pkg/runtime/#Stack)에 의해 보고되지 않습니다. 또한 패닉 스택 트레이스(panic stack traces)에서도 출력되지 않습니다. 이 변경 사항은 이미 스택 트레이스에서 이러한 래퍼들을 생략하고 있던 `gccgo` 툴체인과 `gc` 툴체인의 동작을 일치시키기 위한 것입니다.

이 API들을 사용하는 클라이언트는 누락된 프레임에 맞게 조정이 필요할 수 있습니다. 1.11 버전과 1.12 버전 릴리스 간에 상호 운용되어야 하는 코드의 경우, 메서드 표현식 `x.M`을 함수 리터럴 ` func (...) { x.M(...) }  `로 대체하여 사용할 수 있습니다.

<!-- CL 144340 -->
이제 컴파일러에서 사용할 Go 언어 버전을 설정하기 위해 `-lang` 플래그를 사용할 수 있습니다. 예를 들어, `-lang=go1.8`을 설정하면 Go 1.9에서 추가된 타입 별칭(type aliases)을 프로그램에서 사용할 때 컴파일러가 에러를 발생시킵니다. Go 1.12 이전에 이루어진 언어 변경 사항들은 일관되게 적용되지 않습니다.

<!-- CL 147160 -->
이제 컴파일러 툴체인은 Go 함수와 어셈블리 함수를 호출할 때 서로 다른 컨벤션을 사용합니다. 이는 사용자에게 보이지 않아야 하지만, Go와 어셈블리 사이를 넘나드는 동시에 패키지 경계를 넘어서는 호출의 경우에는 예외가 있을 수 있습니다. 만약 링크 과정에서 "relocation target not defined for ABIInternal (but is defined for ABI0)"와 같은 오류가 발생한다면, ABI 설계 문서의 [compatibility section](https://github.com/golang/proposal/blob/master/design/27539-internal-abi.md#compatibility)을 참조하시기 바랍니다.

<!-- CL 145179 -->
인자 출력 및 변수 위치 정보 개선을 포함하여, 컴파일러가 생성하는 DWARF 디버그 정보에 많은 개선 사항이 있었습니다.

<!-- CL 61511 -->
이제 Go 프로그램은 `perf`와 같은 프로파일링 도구의 활용을 위해 `linux/arm64`에서 스택 프레임 포인터(stack frame pointers)를 유지합니다. 프레임 포인터 유지로 인해 실행 시간 오버헤드가 약간 발생하며, 이는 상황에 따라 다르지만 평균적으로 약 3% 정도입니다. 프레임 포인터를 사용하지 않는 툴체인을 빌드하려면 `make.bash`를 실행할 때 `GOEXPERIMENT=noframepointer`를 설정하십시오.

<!-- CL 142717 -->
더 이상 사용되지 않는 "safe" 컴파일러 모드 (`-u` gcflag로 활성화)가 제거되었습니다.

### `godoc` 및 `go` `doc` {#godoc}

Go 1.12부터 `godoc`은 더 이상 명령줄 인터페이스(CLI)를 제공하지 않으며 웹 서버로만 동작합니다. 명령줄에서 도움말 출력을 확인하려는 사용자는 대신 `go` `doc`을 사용해야 합니다. Go 1.12는 `godoc` 웹 서버가 기본으로 포함되는 마지막 릴리스이며, Go 1.13부터는 `go` `get`을 통해 설치하여 사용할 수 있습니다.

<!-- CL 141977 -->
`go` `doc`에서 이제 `-all` 플래그를 지원합니다.
이 플래그를 사용하면 이전의 `godoc` 커맨드 라인 도구와 마찬가지로, 모든 공개(exported) API와 해당 문서를 출력합니다.

<!-- CL 140959 -->
`go` `doc`에 이제 `-src` 플래그가 추가되었으며, 이를 통해 대상의 소스 코드를 확인할 수 있습니다.

### Trace {#trace}

<!-- CL 60790 -->
이제 trace 도구가 실행 트레이스에 대한 상호 참조를 포함하여 mutator 이용률 곡선을 그리는 기능을 지원합니다. 이는 가비지 컬렉터가 애플리케이션의 지연 시간(latency)과 처리량(throughput)에 미치는 영향을 분석하는 데 유용합니다.

### Assembler {#assembler}

<!-- CL 147218 -->
`arm64`에서 플랫폼 레지스터의 이름이 `R18`에서 `R18_PLATFORM`으로 변경되었습니다. 이는 OS가 해당 레지스터를 예약하여 사용할 수 있으므로, 실수로 사용하는 것을 방지하기 위함입니다.

## 런타임 {#runtime}

<!-- CL 138959 -->
Go 1.12는 힙의 상당 부분이 살아있는 상태(live)일 때의 sweeping 성능을 크게 개선했습니다. 이를 통해 가비지 컬렉션 직후의 할당 지연 시간(allocation latency)이 단축됩니다.

<!-- CL 139719 -->
이제 Go 런타임은 메모리를 운영 체제로 더 공격적으로 반환하며, 특히 기존 힙 공간을 재사용할 수 없는 대규모 할당이 발생했을 때 더욱 그러합니다.

<!-- CL 146342, CL 146340, CL 146345, CL 146339, CL 146343, CL 146337, CL 146341, CL 146338 -->
Go 런타임의 타이머 및 데드라인 코드가 더 빨라졌으며, CPU 수가 많아질수록 확장성이 향상되었습니다. 특히, 네트워크 연결 데드라인을 조작하는 성능이 개선되었습니다.

<!-- CL 135395 -->
Linux에서 런타임은 이제 사용하지 않는 메모리를 해제하기 위해 `MADV_FREE`를 사용합니다. 이는 더 효율적이지만, 보고되는 RSS(Resident Set Size)가 더 높게 나타날 수 있습니다. 커널은 메모리가 필요할 때 사용하지 않는 데이터를 회수합니다.
Go 1.11의 동작(`MADV_DONTNEED`)으로 되돌리려면 환경 변수 `GODEBUG=madvdontneed=1`을 설정하십시오.

<!-- CL 149578 -->
[GODEBUG](/doc/diagnostics.html#godebug) 환경 변수에 `cpu._extension_=off`를 추가하면 이제 표준 라이브러리와 런타임에서 선택적 CPU 명령어 세트 확장 기능의 사용이 비활성화됩니다. 이 기능은 아직 Windows에서 지원되지 않습니다.

<!-- CL 158337 -->
Go 1.12는 대규모 힙 할당의 과다 계상을 수정하여 메모리 프로파일의 정확도를 향상시켰습니다.

<!-- CL 159717 -->
Traceback, `runtime.Caller`, 그리고 `runtime.Callers`에서 더 이상 컴파일러가 생성한 초기화 함수를 포함하지 않습니다. 전역 변수 초기화 중에 traceback을 수행하면 이제 `PKG.init.ializers`라는 이름의 함수가 표시됩니다.

## 표준 라이브러리 {#library}

### TLS 1.3 {#tls_1_3}

Go 1.12에서는 [RFC 8446](https://www.rfc-editor.org/info/rfc8446)에 명시된 대로 `crypto/tls` 패키지에 TLS 1.3에 대한 선택적 지원(opt-in support)이 추가되었습니다. `GODEBUG` 환경 변수에 `tls13=1` 값을 추가하여 활성화할 수 있습니다. Go 1.13부터는 기본적으로 활성화될 예정입니다.

TLS 1.3를 협상하려면, [`Config`](/pkg/crypto/tls/#Config)에서 `MaxVersion`을 명시적으로 설정하지 않았는지 확인하고, 환경 변수 `GODEBUG=tls13=1`을 설정하여 프로그램을 실행하십시오.

[`ConnectionState`](/pkg/crypto/tls/#ConnectionState)의 `TLSUnique`와 재협상(renegotiation)을 제외한 모든 TLS 1.2 기능은 TLS 1.3에서 사용할 수 있으며, 동등하거나 더 나은 보안성과 성능을 제공합니다. TLS 1.3이 이전 버전과 하위 호환되더라도, 특정 레거시 시스템에서는 TLS 1.3 협상을 시도할 때 올바르게 작동하지 않을 수 있다는 점에 유의하십시오. 보안상 너무 짧은 RSA 인증서 키(512비트 키 포함)는 TLS 1.3에서 작동하지 않습니다.

TLS 1.3 사이퍼 수트(cipher suites)는 설정할 수 없습니다. 지원되는 모든 사이퍼 수트는 안전하며, [`Config`](/pkg/crypto/tls/#Config)에서 `PreferServerCipherSuites`가 설정된 경우 선호 순서는 사용 가능한 하드웨어를 기반으로 결정됩니다.

Early data(또는 "0-RTT 모드")는 현재 클라이언트나 서버로서 지원되지 않습니다. 또한, Go 1.12 서버는 클라이언트가 예상치 못한 early data를 보냈을 때 이를 건너뛰는 기능을 지원하지 않습니다. TLS 1.3 0-RTT 모드는 어떤 서버가 0-RTT를 지원하는지에 대한 상태를 클라이언트가 유지하는 방식이므로, Go 1.12 서버는 일부 다른 서버들이 0-RTT를 지원하는 로드 밸런싱 풀의 일부가 될 수 없습니다. 0-RTT를 지원하는 서버에서 Go 1.12 서버로 도메인을 전환하는 경우, 중단 없는 운영을 보장하려면 전환 전에 발행된 세션 티켓의 수명 기간 동안 최소한 0-RTT를 비활성화해야 합니다.

TLS 1.3에서는 클라이언트가 핸드셰이크에서 마지막으로 발언하는 주체입니다. 따라서 클라이언트가 서버에서 오류를 발생시킨 경우, 해당 오류는 [`Handshake`](/pkg/crypto/tls/#Conn.Handshake)가 아니라 첫 번째 [`Read`](/pkg/crypto/tls/#Conn.Read) 호출 시 클라이언트에 반환됩니다. 예를 들어, 서버가 클라이언트 인증서를 거부하는 경우가 이에 해당합니다. 마찬가지로, 세션 티켓은 이제 핸드셰이크 이후 메시지(post-handshake messages)이므로 클라이언트가 첫 [`Read`](/pkg/crypto/tls/#Conn.Read)를 수행할 때만 수신됩니다.

### 라이브러리의 소규모 변경 사항 {#minor_library_changes}

언제나 그렇듯, Go 1의 [호환성 약속](/doc/go1compat)을 염두에 두고 라이브러리에 다양한 소규모 변경 사항 및 업데이트가 적용되었습니다.

<!-- TODO: CL 115677: https://golang.org/cl/115677: cmd/vet: 임베디드 필드 태그도 확인 필요 -->

#### [bufio](/pkg/bufio/)

<!-- CL 149297 -->
`Reader`의 [`UnreadRune`](/pkg/bufio/#Reader.UnreadRune) 및
[`UnreadByte`](/pkg/bufio/#Reader.UnreadByte) 메서드는 이제 [`Peek`](/pkg/bufio/#Reader.Peek) 호출 후에
사용될 경우 에러를 반환합니다.

<!-- bufio -->

#### [bytes](/pkg/bytes/)

<!-- CL 137855 -->
새로운 함수 [`ReplaceAll`](/pkg/bytes/#ReplaceAll)은 값의 모든 겹치지 않는 인스턴스를 다른 값으로 대체한 바이트 슬라이스의 복사본을 반환합니다.

<!-- CL 145098 -->
이제 제로 값(zero-value)인 [`Reader`](/pkg/bytes/#Reader)에 대한 포인터는 [`NewReader`](/pkg/bytes/#NewReader)`(nil)`과 기능적으로 동일합니다.
Go 1.12 이전에는 전자를 후자의 대체제로 모든 경우에 사용할 수 없었습니다.

<!-- bytes -->

#### [crypto/rand](/pkg/crypto/rand/)

<!-- CL 139419 -->
이제 `Reader.Read`가 커널로부터 엔트로피를 읽기 위해 60초 이상 대기하며 블록(blocked)되는 첫 번째 상황에서 표준 에러(standard error)로 경고가 출력됩니다.

<!-- CL 120055 -->
FreeBSD에서 `Reader`는 이제 `getrandom` 시스템 호출을 사용할 수 있으면 이를 사용하고, 그렇지 않으면 `/dev/urandom`을 사용합니다.

<!-- crypto/rand -->

#### [crypto/rc4](/pkg/crypto/rc4/)

<!-- CL 130397 -->
이번 릴리스에서는 어셈블리 구현을 제거하고 순수 Go 버전만 남겼습니다. Go 컴파일러가 생성하는 코드는 정확한 CPU에 따라 약간 더 좋거나 나쁠 수 있습니다. RC4는 안전하지 않으며 레거시 시스템과의 호환성을 위해서만 사용해야 합니다.

<!-- crypto/rc4 -->

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 143177 -->
클라이언트가 TLS처럼 보이지 않는 초기 메시지를 보내는 경우, 서버는 더 이상 alert로 응답하지 않으며, [`RecordHeaderError`](/pkg/crypto/tls/#RecordHeaderError)의 새로운 필드인 `Conn`을 통해 하위의 `net.Conn`을 노출합니다.

<!-- crypto/tls -->

#### [database/sql](/pkg/database/sql/)

<!-- CL 145738 -->
이제 [`Row.Scan`](/pkg/database/sql/#Row.Scan) 메서드에 [`*Rows`](/pkg/database/sql/#Rows) 값을 전달하여 쿼리 커서를 얻을 수 있습니다.

<!-- database/sql -->

#### [expvar](/pkg/expvar/)

<!-- CL 139537 -->
새로운 [`Delete`](/pkg/expvar/#Map.Delete) 메서드를 통해 [`Map`](/pkg/expvar/#Map)에서 키/값 쌍을 삭제할 수 있습니다.

<!-- expvar -->

#### [fmt](/pkg/fmt/)

<!-- CL 142737 -->
테스트를 용이하게 하기 위해 이제 Map이 키 기준 정렬 순으로 출력됩니다. 정렬 규칙은 다음과 같습니다:

- 해당되는 경우, `nil`은 가장 낮은 값으로 비교됩니다.
  - `int`, `float`, `string`은 `<` 연산자로 정렬됩니다.
  - `NaN`은 `NaN`이 아닌 `float`보다 작은 값으로 비교됩니다.
  - `bool`은 `false`가 `true`보다 먼저 옵니다.
  - `Complex`는 실수부를 먼저 비교한 후, 허수부를 비교합니다.
  - 포인터는 머신 주소로 비교합니다.
  - 채널 값은 머신 주소로 비교합니다.
  - 구조체는 각 필드를 순서대로 비교합니다.
  - 배열은 각 요소를 순서대로 비교합니다.
  - 인터페이스 값은 먼저 구체적인 타입을 설명하는 `reflect.Type`으로 비교한 다음, 이전 규칙에 설명된 대로 구체적인 값으로 비교합니다.

<!-- CL 129777 -->
맵(map)을 출력할 때, `NaN`과 같이 반사적이지 않은(non-reflexive) 키 값이 이전에는 `<nil>`로 표시되었습니다. 이번 릴리스부터는 올바른 값이 출력됩니다.

<!-- fmt -->

#### [go/doc](/pkg/go/doc/)

<!-- CL 140958 -->
[`cmd/doc`](/cmd/doc/)의 몇 가지 미결 이슈를 해결하기 위해,
이 패키지에 AST 데이터 삭제 여부를 제어하는
새로운 [`Mode`](/pkg/go/doc/#Mode) 비트인 `PreserveAST`가 추가되었습니다.

<!-- go/doc -->

#### [go/token](/pkg/go/token/)

<!-- CL 134075 -->
[`File`](/pkg/go/token#File) 타입에 새로운 [`LineStart`](/pkg/go/token#File.LineStart) 필드가 추가되었으며, 이는 주어진 라인의 시작 위치를 반환합니다. 이 기능은 어셈블리와 같이 때때로 non-Go 파일을 처리해야 하지만, 파일 위치를 식별하기 위해 `token.Pos` 메커니즘을 사용하고자 하는 프로그램에서 특히 유용합니다.

<!-- go/token -->

#### [image](/pkg/image/)

<!-- CL 118755 -->
[`RegisterFormat`](/pkg/image/#RegisterFormat) 함수는 이제 동시 사용(concurrent use)이 안전합니다.

제공해주신 내용에 번역할 텍스트가 없습니다. 번역이 필요한 Markdown 콘텐츠를 제공해 주시면, 요청하신 지침에 따라 정확하게 한국어로 번역해 드리겠습니다.

#### [image/png](/pkg/image/png/)

<!-- CL 134235 -->
16가지 미만의 색상을 가진 팔레트 이미지가 이제 더 작은 출력으로 인코딩됩니다.

제공해주신 내용에 텍스트가 포함되어 있지 않습니다. 번역할 Markdown 콘텐츠를 제공해 주시면, 요청하신 지침에 따라 정성껏 기술 번역을 진행하겠습니다.

#### [io](/pkg/io/)

<!-- CL 139457 -->
새로운 [`StringWriter`](/pkg/io#StringWriter) 인터페이스는 [`WriteString`](/pkg/io/#WriteString) 함수를 래핑합니다.

<!-- io -->

#### [math](/pkg/math/)

<!-- CL 153059 -->
[`Sin`](/pkg/math/#Sin),
[`Cos`](/pkg/math/#Cos),
[`Tan`](/pkg/math/#Tan),
및 [`Sincos`](/pkg/math/#Sincos) 함수가 이제 매우 큰 인자에 대해 Payne-Hanek 범위 축소(range reduction)를 적용합니다. 이로 인해 더 정확한 결과가 생성되지만, 이전 릴리스의 결과와 비트 단위로 일치하지는 않을 수 있습니다.

<!-- math -->

#### [math/bits](/pkg/math/bits/)

<!-- CL 123157 -->
새로운 확장 정밀도 연산인 [`Add`](/pkg/math/bits/#Add), [`Sub`](/pkg/math/bits/#Sub), [`Mul`](/pkg/math/bits/#Mul), [`Div`](/pkg/math/bits/#Div)를 `uint`, `uint32`, `uint64` 버전으로 사용할 수 있습니다.

<!-- math/bits -->

#### [net](/pkg/net/)

<!-- CL 146659 -->
[`Dialer.DualStack`](/pkg/net/#Dialer.DualStack) 설정은 이제 무시되며 더 이상 사용되지 않습니다(deprecated). 이제 RFC 6555 Fast Fallback ("Happy Eyeballs")이 기본적으로 활성화됩니다. 이를 비활성화하려면 [`Dialer.FallbackDelay`](/pkg/net/#Dialer.FallbackDelay)를 음수 값으로 설정하십시오.

<!-- CL 107196 -->
마찬가지로, [`Dialer.KeepAlive`](/pkg/net/#Dialer.KeepAlive)가 0인 경우 이제 TCP keep-alives가 기본적으로 활성화됩니다.
비활성화하려면 음수 값으로 설정하십시오.

<!-- CL 113997 -->
Linux에서 [`UnixConn`](/pkg/net/#UnixConn)에서 [`TCPConn`](/pkg/net/#TCPConn)으로 데이터를 복사할 때 이제 [`splice` 시스템 콜](https://man7.org/linux/man-pages/man2/splice.2.html)이 사용됩니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- CL 143177 -->
이제 HTTP 서버는 HTTPS 서버로 잘못 전송된 HTTP 요청에 대해 평문 "400 Bad Request" 응답을 보내며 거부합니다.

<!-- CL 130115 -->
새로운 [`Client.CloseIdleConnections`](/pkg/net/http/#Client.CloseIdleConnections) 메서드는 `Client`가 사용하는 하위 `Transport`에 `CloseIdleConnections`가 있는 경우 이를 호출합니다.

<!-- CL 145398 -->
[`Transport`](/pkg/net/http/#Transport)는 더 이상 HTTP Trailers를 선언했지만 chunked encoding을 사용하지 않는 HTTP 응답을 거부하지 않습니다. 대신, 선언된 trailer는 이제 그냥 무시됩니다.

<!-- CL 152080 -->
<!-- CL 151857 -->
[`Transport`](/pkg/net/http/#Transport)는 더 이상 Go 1.10 및 Go 1.11 때만큼 HTTP/2 서버가 알리는 `MAX_CONCURRENT_STREAMS` 값을 엄격하게 처리하지 않습니다. 기본 동작은 이제 Go 1.9 때의 방식으로 돌아갔습니다. 즉, 서버에 대한 각 연결은 최대 `MAX_CONCURRENT_STREAMS`개의 요청을 활성화할 수 있으며, 필요한 경우 새로운 TCP 연결이 생성됩니다. Go 1.10 및 Go 1.11에서 `http2` 패키지는 새로운 연결을 생성하는 대신 요청이 완료될 때까지 블록(block)하고 대기했습니다.

이전의 더 엄격한 동작을 다시 사용하려면, [`golang.org/x/net/http2`](https://godoc.org/golang.org/x/net/http2) 패키지를 직접 임포트하고 [`Transport.StrictMaxConcurrentStreams`](https://godoc.org/golang.org/x/net/http2#Transport.StrictMaxConcurrentStreams)를 `true`로 설정하십시오.

<!-- net/http -->

#### [net/url](/pkg/net/url/)

<!-- CL 159157, CL 160178 -->
[`Parse`](/pkg/net/url/#Parse),
[`ParseRequestURI`](/pkg/net/url/#ParseRequestURI),
및
[`URL.Parse`](/pkg/net/url/#URL.Parse)는
이제 NULL, 탭, 줄바꿈을 포함하여 ASCII 제어 문자가 포함된 URL에 대해
에러를 반환합니다.

<!-- net/url -->

#### [net/http/httputil](/pkg/net/http/httputil/)

<!-- CL 146437 -->
이제 [`ReverseProxy`](/pkg/net/http/httputil/#ReverseProxy)가 WebSocket 요청을 자동으로 프록시합니다.

<!-- net/http/httputil -->

#### [os](/pkg/os/)

<!-- CL 125443 -->
새로운 [`ProcessState.ExitCode`](/pkg/os/#ProcessState.ExitCode) 메서드는
프로세스의 종료 코드(exit code)를 반환합니다.

<!-- CL 135075 -->
`ModeType` 비트마스크에 `ModeCharDevice`가 추가되었습니다. 이제 [`FileMode`](/pkg/os/#FileMode)를 `ModeType`으로 마스킹할 때 `ModeDevice | ModeCharDevice`를 복구할 수 있습니다.

<!-- CL 139418 -->
새로운 함수 [`UserHomeDir`](/pkg/os/#UserHomeDir)는 현재 사용자의 홈 디렉터리를 반환합니다.

<!-- CL 146020 -->
[`RemoveAll`](/pkg/os/#RemoveAll)이 이제 대부분의 Unix 시스템에서 4096자보다 긴 경로를 지원합니다.

<!-- CL 130676 -->
[`File.Sync`](/pkg/os/#File.Sync)가 이제 macOS에서 `F_FULLFSYNC`를 사용하여 파일 내용을 영구 저장소로 올바르게 플러시(flush)합니다.
이로 인해 이전 릴리스보다 메서드 실행 속도가 더 느려질 수 있습니다.

<!--CL 155517 -->
[`File`](/pkg/os/#File)는 이제 [`syscall.RawConn`](/pkg/syscall/#RawConn)
인터페이스 값을 반환하는 [`SyscallConn`](/pkg/os/#File.SyscallConn)
메서드를 지원합니다. 이를 사용하여 기본 파일 서술자(file descriptor)에 대해 시스템별 작업을 호출할 수 있습니다.

<!-- os -->

#### [path/filepath](/pkg/path/filepath/)

<!-- CL 145220 -->
[`IsAbs`](/pkg/path/filepath/#IsAbs) 함수는 이제 Windows에서 `NUL`과 같은 예약된 파일 이름이 전달되면 true를 반환합니다.
[예약된 이름 목록.](https://docs.microsoft.com/en-us/windows/desktop/fileio/naming-a-file#naming-conventions)

<!-- path/filepath -->

#### [reflect](/pkg/reflect/)

<!-- CL 33572 -->
새로운 [`MapIter`](/pkg/reflect#MapIter) 타입은 맵을 순회하기 위한 반복자(iterator)입니다. 이 타입은 [`Value`](/pkg/reflect#Value) 타입의 새로운 [`MapRange`](/pkg/reflect#Value.MapRange) 메서드를 통해 제공됩니다.
이는 range 문과 동일한 반복 세맨틱을 따르며, 반복자를 전진시키기 위한 `Next`와 각 엔트리에 접근하기 위한 `Key`/`Value` 메서드를 제공합니다.

<!-- reflect -->

#### [regexp](/pkg/regexp/)

<!-- CL 139784 -->
락 경합(lock contention)을 피하기 위해 [`Copy`](/pkg/regexp/#Regexp.Copy)를 사용할 필요가 더 이상 없으므로, 부분적인 deprecation 주석이 추가되었습니다.
서로 다른 [`Longest`](/pkg/regexp/#Regexp.Longest) 설정값을 가진 두 개의 복사본을 만들기 위한 목적이라면 [`Copy`](/pkg/regexp/#Regexp.Copy)를 사용하는 것이 여전히 적절할 수 있습니다.

<!-- regexp -->

#### [runtime/debug](/pkg/runtime/debug/)

<!-- CL 144220 -->
새로운 [`BuildInfo`](/pkg/runtime/debug/#BuildInfo) 타입은 실행 중인 바이너리에서 읽어온 빌드 정보를 제공하며, 이는 모듈 지원과 함께 빌드된 바이너리에서만 사용할 수 있습니다. 여기에는 메인 패키지 경로, 메인 모듈 정보 및 모듈 의존성이 포함됩니다. 이 타입은 [`BuildInfo`](/pkg/runtime/debug/#BuildInfo)의 [`ReadBuildInfo`](/pkg/runtime/debug/#ReadBuildInfo) 함수를 통해 제공됩니다.

<!-- runtime/debug -->

#### [strings](/pkg/strings/)

<!-- CL 137855 -->
새로운 함수 [`ReplaceAll`](/pkg/strings/#ReplaceAll)은 문자열 내에서 겹치지 않는 모든 값의 인스턴스를 다른 값으로 대체한 문자열의 복사본을 반환합니다.

<!-- CL 145098 -->
이제 zero-value인 [`Reader`](/pkg/strings/#Reader)에 대한 포인터는 [`NewReader`](/pkg/strings/#NewReader)`(nil)`과 기능적으로 동일합니다.
Go 1.12 이전에는 전자를 후자의 대체제로 모든 경우에 사용할 수 없었습니다.

<!-- CL 122835 -->
새로운 [`Builder.Cap`](/pkg/strings/#Builder.Cap) 메서드는 빌더의 내부 바이트 슬라이스(byte slice) 용량을 반환합니다.

<!-- CL 131495 -->
문자 매핑 함수인 [`Map`](/pkg/strings/#Map),
[`Title`](/pkg/strings/#Title),
[`ToLower`](/pkg/strings/#ToLower),
[`ToLowerSpecial`](/pkg/strings/#ToLowerSpecial),
[`ToTitle`](/pkg/strings/#ToTitle),
[`ToTitleSpecial`](/pkg/strings/#ToTitleSpecial),
[`ToUpper`](/pkg/strings/#ToUpper), 그리고
[`ToUpperSpecial`](/pkg/strings/#ToUpperSpecial)
이제 항상 유효한 UTF-8을 반환하도록 보장합니다. 이전 릴리스에서는 입력값이 유효하지 않은 UTF-8이더라도 문자 교체가 필요하지 않은 경우, 이러한 루틴들이 유효하지 않은 UTF-8을 수정하지 않고 그대로 잘못 반환했습니다.

<!-- strings -->

#### [syscall](/pkg/syscall/)

<!-- CL 138595 -->
이제 FreeBSD 12에서 64비트 inode가 지원됩니다. 이에 따라 일부 타입이 조정되었습니다.

<!-- CL 125456 -->
이제 호환되는 버전의 Windows에서 Unix 소켓 ([`AF_UNIX`](https://blogs.msdn.microsoft.com/commandline/2017/12/19/af_unix-comes-to-windows/)) 주소 제품군이 지원됩니다.

<!-- CL 147117 -->
Windows를 위해 최대 18개의 인자를 사용하는 호출이 가능한 새로운 함수 [`Syscall18`](/pkg/syscall/?GOOS=windows&GOARCH=amd64#Syscall18)이 도입되었습니다.

<!-- syscall -->

#### [syscall/js](/pkg/syscall/js/)

<!-- CL 153559 -->

`Callback` 타입과 `NewCallback` 함수가 이름이 변경되었습니다. 이제 각각 [`Func`](/pkg/syscall/js/?GOOS=js&GOARCH=wasm#Func)와 [`FuncOf`](/pkg/syscall/js/?GOOS=js&GOARCH=wasm#FuncOf)로 불립니다.
이는 breaking change이지만, WebAssembly 지원은 여전히 실험적이며 아직 [Go 1 호환성 약속](/doc/go1compat)의 대상이 아닙니다. 이전 이름을 사용하는 모든 코드는 업데이트가 필요합니다.

<!-- CL 141644 -->
타입이 새로운 [`Wrapper`](/pkg/syscall/js/?GOOS=js&GOARCH=wasm#Wrapper) 인터페이스를 구현하는 경우, [`ValueOf`](/pkg/syscall/js/?GOOS=js&GOARCH=wasm#ValueOf)는 이를 사용하여 해당 타입에 대한 JavaScript 값을 반환합니다.

<!-- CL 143137 -->
제로 `Value`([`/pkg/syscall/js/?GOOS=js&GOARCH=wasm#Value`](/pkg/syscall/js/?GOOS=js&GOARCH=wasm#Value))의 의미가 변경되었습니다. 이제 제로 `Value`는 숫자 0 대신 JavaScript의 `undefined` 값을 나타냅니다.

이는 파괴적 변경(breaking change)이지만, WebAssembly 지원은 여전히 실험적 단계이며 아직 [Go 1 호환성 약속](/doc/go1compat)의 대상이 아닙니다. 제로 [`Value`](/pkg/syscall/js/?GOOS=js&GOARCH=wasm#Value)가 숫자 0을 의미한다고 가정하고 작성된 모든 코드는 업데이트가 필요합니다.

<!-- CL 144384 -->
새로운
[`Value.Truthy`](/pkg/syscall/js/?GOOS=js&GOARCH=wasm#Value.Truthy)
메서드는 주어진 값의
[JavaScript "truthiness"](https://developer.mozilla.org/en-US/docs/Glossary/Truthy)
(참 같은 값 여부)를 보고합니다.

<!-- syscall/js -->

#### [testing](/pkg/testing/)

<!-- CL 139258 -->
이제 [`-benchtime`](/cmd/go/#hdr-Testing_flags) 플래그에서 값이 "`x`"로 끝나는 경우, 시간 대신 명시적인 반복 횟수를 설정할 수 있습니다. 예를 들어, `-benchtime=100x`는 벤치마크를 100번 실행합니다.

<!-- testing -->

#### [text/template](/pkg/text/template/)

<!-- CL 142217 -->
템플릿을 실행할 때, 에러 메시지에서 긴 컨텍스트 값이 더 이상 생략되지 않습니다.

`executing "tmpl" at <.very.deep.context.v...>: map has no entry for key "notpresent"`

Please provide the Markdown content you would like me to translate. You haven't included any text in your request yet. Once you provide the content, I will translate it from English to Korean while following all your technical constraints.

`executing "tmpl" at <.very.deep.context.value.notpresent>: map has no entry for key "notpresent"`

<!-- CL 143097 -->
템플릿에서 호출한 사용자 정의 함수에서 panic이 발생할 경우, 이제 해당 panic을 포착하여 `Execute` 또는 `ExecuteTemplate` 메서드를 통해 에러로 반환합니다.

<!-- text/template -->

#### [time](/pkg/time/)

<!-- CL 151299 -->
`$GOROOT/lib/time/zoneinfo.zip`에 있는 시간대 데이터베이스가 2018i 버전으로 업데이트되었습니다. 이 ZIP 파일은 운영 체제에서 시간대 데이터베이스가 제공되지 않는 경우에만 사용됩니다.

<!-- time -->

#### [unsafe](/pkg/unsafe/)

<!-- CL 146058 -->
nil `unsafe.Pointer`를 `uintptr`로 변환하고 산술 연산을 거쳐 다시 되돌리는 것은 유효하지 않습니다.
(이는 이전부터 유효하지 않았으나, 이제는 컴파일러의 오작동을 유발하게 됩니다.)

제공해주신 내용이 없습니다. 번역할 Markdown 콘텐츠를 입력해 주세요.
