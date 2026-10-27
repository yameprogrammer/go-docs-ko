<!--
참고: 이 문서 및 이 디렉토리에 있는 다른 문서에서, 고정 폭 문자열과 고정 폭이 아닌 공백을 함께 사용하는 것이 관례입니다 (예: `hello world`).
이러한 문자열에서 내부 태그를 제거하는 CL을 보내지 마세요.
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.12 소개 {#introduction}

가장 최신 Go 버전인 1.12은 [Go 1.11](go1.11) 이후 6개월 만에 출시되었습니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
항상처럼, 이 릴리스는 Go 1의 [호환성 보장](/doc/go1compat)을 유지합니다.
대부분의 Go 프로그램이 기존과 동일하게 컴파일 및 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

```
// Go package name: "example"
// Identifier: "myVariable"
// URL: "https://example.com"
// Command: "go run main.go"
// Code snippet: "fmt.Println("Hello, world!")"
```

변경 사항은 없습니다.

## 포트 {#ports}

<!-- CL 138675 -->
레이스 감지 기능이 `linux/arm64`에서 지원됩니다.

Go 1.12은 이미 지원 종료된 FreeBSD 10.x에서만 지원되는 마지막 버전입니다. Go 1.13은 FreeBSD 11.2 이상 또는 FreeBSD 12.0 이상을 필요로 합니다.

FreeBSD 12.0 이상은 COMPAT\_FREEBSD11 옵션이 설정된 커널을 필요로 합니다 (이는 기본 설정입니다).

<!-- CL 146898 -->
`linux/ppc64`에서 cgo가 이제 지원됩니다.

<!-- CL 146023 -->
`hurd`는 이제 `GOOS`에 대해 인식되는 값으로, `gccgo`를 사용하여 GNU/Hurd 시스템에서 사용하도록 예약되어 있습니다.

### Windows

Go의 새로운 `windows/arm` 포트는 Windows 10에서 Go 실행을 지원합니다.
32비트 ARM 칩(예: Raspberry Pi 3)에서 IoT Core를 실행합니다.

### AIX

Go는 현재 POWER8 아키텍처(`aix/ppc64`)에서 AIX 7.2 및 이후 버전을 지원합니다. 외부 링크, cgo, pprof, 그리고 레이스 감지 기능은 아직 지원되지 않습니다.

### Darwin
```
# Darwin
```

Go 1.12은 macOS 10.10 Yosemite에서만 실행 가능한 마지막 버전입니다.
Go 1.13은 macOS 10.11 El Capitan 또는 이후 버전에서만 실행됩니다.

<!-- CL 141639 -->
`libSystem`은 이제 Darwin에서 시스템 호출을 수행할 때 사용되며, 향후 macOS 및 iOS의 버전과의 호환성을 보장합니다. <!-- CL 153338 -->
`libSystem`으로의 전환은 App Store에서 개인 API 사용에 대한 추가 검사를 유발했습니다. `syscall.Getdirentries`는 개인 API로 간주되므로, iOS에서는 항상 `ENOSYS` 오류를 반환합니다.
또한, [`syscall.Setrlimit`](/pkg/syscall/#Setrlimit)는 과거에 성공했던 위치에서 `invalid` `argument`를 보고합니다. 이러한 결과는 Go에만 국한되지 않으며, 사용자는 앞으로 `libSystem`의 구현과 동일한 동작을 예상해야 합니다.

## 도구 {#tools}

### `go tool vet` 기능 더 이상 지원되지 않음 {#vet}

명령 `go vet`가 다양한 소스 코드 분석 도구의 기반으로 재작성되었습니다. 자세한 내용은 [golang.org/x/tools/go/analysis](https://godoc.org/golang.org/x/tools/go/analysis) 패키지를 참조하십시오. 이로 인해 `go tool vet`는 더 이상 지원되지 않습니다. `go tool vet`를 사용하는 외부 도구는 `go vet`를 사용하도록 변경해야 합니다. `go vet`를 `go tool vet` 대신 사용하는 것은 지원되는 모든 Go 버전과 호환되어야 합니다.

이 변경의 일부로, 실험적인 `-shadow` 옵션은 `go vet`에서 더 이상 사용되지 않습니다. 변수 섀도잉 검사는 이제 다음을 사용하여 수행할 수 있습니다:

```markdown
go get -u golang.org/x/tools/go/analysis/passes/shadow/cmd/shadow
	go vet -vettool=$(which shadow)
```

### 투어 {#tour}

<!-- CL 152657 -->
Go 튜어는 이제 메인 바이너리 배포본에 포함되지 않습니다. 
로컬에서 튜어를 실행하려면, `go` `tool` `tour`를 실행하는 대신, 수동으로 설치하십시오:

go get -u golang.org/x/tour
	tour

### Go 캐시 요구 사항 {#gocache}

```
go get -u golang.org/x/tools/cache
```

[빌드 캐시](/cmd/go/#hdr-Build_and_test_caching)는 이제
`$GOPATH/pkg`를 제거하기 위한
필수 단계입니다. `GOCACHE=off` 환경 변수를 설정하면
캐시에 쓰기를 수행하는 `go` 명령이 실패합니다.

### 이진 파일만 설치 가능한 패키지 {#binary-only}

Go 1.12은 바이너리만 지원하는 패키지를 지원하는 마지막 릴리스입니다.

### Cgo {#cgo}

Go 1.12에서 C 타입 `EGLDisplay`를 Go 타입 `uintptr`로 변환합니다.
이 변경 사항은 Go 1.10 및 이후 버전에서 Darwin의 CoreFoundation 및 Java의 JNI 유형을 처리하는 방식과 유사합니다. 자세한 내용은 [cgo 설명서](/cmd/cgo/#hdr-Special_cases)를 참조하십시오.

<!-- CL 152657 -->
Cgo를 사용하는 패키지에서는 래핑된 C 이름이 더 이상 허용되지 않습니다. 대신 Cgo 이름을 사용하십시오. 예를 들어, cgo가 생성한 래핑된 이름인 `_Ctype_char` 대신 문서화된 `C.char` 이름을 사용하십시오.

### 모듈 {#modules}

<!-- CL 148517 -->
`GO111MODULE`가 `on`으로 설정된 경우, `go`
명령은 현재 모듈 디렉터리 외부에서도 모듈 인식 기능을 지원하며,
다음 조건이 충족되는 경우에만 작동합니다. 즉, 해당 작업이 현재 디렉터리 내의 임포트 경로를 참조하거나
`go.mod` 파일을 명시적으로 편집하지 않는 경우입니다.
`go get`,
`go list`, 및
`go mod download`와 같은 명령은 초기 상태가 비어 있는 모듈과 동일하게 작동합니다.
이 모드에서는 `go env GOMOD`가 시스템의 null 장치 (`/dev/null` 또는 `NUL`)를 보고합니다.

<!-- CL 146382 -->
`go` 명령어를 사용하여 모듈을 다운로드하고 추출하는 것은 이제 동시 실행이 안전합니다.
모듈 캐시 (`GOPATH/pkg/mod`)는 파일 잠금을 지원하는 파일 시스템에 있어야 합니다.

<!-- CL 147282, 147281 -->
`go.mod` 파일 내의 `go` 지시어는 해당 모듈 내의 파일에서 사용되는 언어의 버전을 나타냅니다.
기존 버전이 없는 경우, 기본적으로 현재 릴리스(`go` `1.12`)로 설정됩니다.
만약 모듈의 `go` 지시어가 사용 중인 도구 체인보다 _더 새로운_ 버전을 지정하는 경우, `go` 명령은 해당 패키지를 빌드하려고 시도하며, 빌드가 실패할 경우에만 불일치 사항을 기록합니다.

<!-- CL 147282, 147281 -->
이 변경된 `go` 지시어 사용 방식은 다음과 같은 결과를 초래합니다. 만약 Go 1.12로 모듈을 빌드하고, `go.mod` 파일에 `go 1.12`를 기록한다면, Go 1.11 (Go 1.11.3 버전 포함)을 사용하여 동일한 모듈을 빌드하려고 시도하면 오류가 발생합니다. Go 1.11.4 또는 그 이후 버전은 정상적으로 작동하며, Go 1.11 이전 버전도 작동합니다.

만약 Go 1.11부터 1.11.3 버전까지 사용해야 한다면, 다음과 같은 방법으로 문제를 해결할 수 있습니다:

*   언어 버전을 1.11로 설정하고, `go mod edit -go=1.11` 명령어를 사용하여 Go 1.12 go tool을 사용합니다.

<!-- CL 152739 -->
`go` 명령은 현재 모듈을 사용하여 가져오기를 해결할 수 없는 경우,
주 모듈의 `replace` 지시문에 언급된 모듈을 먼저 사용하려고 시도합니다.
그리고 모듈 캐시 및 일반 네트워크 소스를 참조합니다.
일치하는 대체 항목이 발견되었지만 `replace` 지시문이 버전 정보를 지정하지 않는 경우, `go` 명령은 `time.Time`의 0 값을 기반으로 하는 가상 버전을 사용합니다 (예: `v0.0.0-00010101000000-000000000000`).

### 컴파일러 도구 체인 {#compiler}

<!-- CL 134155, 134156 -->
컴파일러의 실시간 변수 분석이 개선되었습니다. 이는 이 릴리스에서 이전 릴리스보다 종료자가 더 빨리 실행될 수 있음을 의미합니다. 만약 그렇다면, [`runtime.KeepAlive`](/pkg/runtime/#KeepAlive) 호출을 적절하게 추가하는 것을 고려하십시오.

<!-- CL 147361 -->
더 많은 함수가 기본적으로 인라인될 수 있으며, 단순히 다른 함수를 호출하는 것 외의 함수도 포함됩니다.
이 추가적인 인라인 기능은 `runtime.CallersFrames` ( [pkg/runtime/#CallersFrames](/) ) 를 직접 사용하기보다는 `runtime.Callers` ( [pkg/runtime/#Callers](/) ) 의 결과를 반복하는 것보다 더 중요하게 만듭니다.

```
// 이전 코드이며 더 이상 올바르게 작동하지 않습니다 (내장 호출 프레임을 누락합니다).
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
// 새로운 코드이며 올바르게 작동합니다.
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
컴파일러가 생성한 메타 표현식을 구현하기 위한 래퍼는
더 이상 [`runtime.CallersFrames`](/pkg/runtime/#CallersFrames) 및 [`runtime.Stack`](/pkg/runtime/#Stack)에 의해
보고되지 않습니다. 또한, 이 래퍼는 패닉 스택 추적에도
출력되지 않습니다.
이 변경 사항은 `gc` 도구 체인을 `gccgo` 도구 체인과 일치하도록
합니다. `gccgo` 도구 체인은 이미 이러한 래퍼를 스택 추적에서 제거했습니다.
이러한 API의 클라이언트는 누락된 프레임을 고려해야 합니다. 1.11 및 1.12 릴리스 간에 상호 작용해야 하는 코드를 사용하는 경우, 메타 표현식 `x.M`을 함수 리터럴 ` func(...) { x.M(...) } `로 대체할 수 있습니다.

<!-- CL 144340 -->
컴파일러는 이제 `-lang` 플래그를 사용하여 사용할 Go 언어 버전을 지정할 수 있습니다. 예를 들어, `-lang=go1.8`는 프로그램이 타입 별칭을 사용하는 경우 컴파일러가 오류를 발생시키도록 합니다. (타입 별칭은 Go 1.9에 추가되었습니다.)

Go 1.12 이전의 언어 변경 사항은 일관되게 적용되지 않습니다.

<!-- CL 147160 -->
컴파일러 도구 체인은 이제 Go 함수와 어셈블리 함수를 호출하는 데 다른 규칙을 사용합니다. 이 변경 사항은 사용자에게는 보이지 않아야 하지만, 동시에 Go와 어셈블리로 전환하고 _그리고_ 패키지 경계를 넘어가는 호출의 경우에는 보일 수 있습니다. 링크 과정에서 "relocation target not defined for ABIInternal (but is defined for ABI0)"와 같은 오류가 발생하면, [호환성 섹션](https://github.com/golang/proposal/blob/master/design/27539-internal-abi.md#compatibility)의 ABI 설계 문서 참조하십시오.

<!-- CL 145179 -->
컴파일러가 생성하는 DWARF 디버깅 정보에 대한 여러 개선 사항이 있습니다. 여기에는 인자 출력 및 변수 위치 정보 개선이 포함됩니다.

<!-- CL 61511 -->
Go 프로그램은 이제 `linux/arm64`에서 `perf`와 같은 프로파일링 도구에 유용하도록 스택 프레임 포인터를 유지합니다. 프레임 포인터 유지에는 약간의 런타임 오버헤드가 있으며, 이는 약 3% 정도의 평균값을 가집니다. 프레임 포인터를 사용하지 않는 도구 체인을 빌드하려면 `make.bash`를 실행할 때 `GOEXPERIMENT=noframepointer`를 설정하십시오.

<!-- CL 142717 -->
오래된 "안전" 컴파일러 모드 (`-u` gcflag 옵션으로 활성화됨)가 제거되었습니다.

### `godoc` 및 `go` 문서 {#godoc}

Go 1.12에서 `godoc`는 더 이상 명령줄 인터페이스를 가지고 있지 않고, 웹 서버로만 작동합니다. 사용자는 명령줄 도움말 출력을 위해 `go` `doc`를 사용해야 합니다. Go 1.12는 `godoc` 웹 서버를 포함하는 마지막 릴리스이며, Go 1.13에서는 `go` `get`을 통해 사용할 수 있습니다.

<!-- CL 141977 -->
`go doc` 명령이 이제 `-all` 플래그를 지원하며,
이를 사용하면 모든 공개 API와 해당 문서를 출력합니다.
`godoc` 명령줄에서 사용하던 기능과 동일합니다.

<!-- CL 140959 -->
`go` `doc`에 이제 `-src` 플래그가 추가되어, 대상의 소스 코드를 보여줍니다.

### 추적 {#trace}

<!-- CL 60790 -->
트레이스 도구가 이제 뮤테이터 활용 곡선을 그리는 기능을 지원하며, 여기에는 실행 트레이스와의 교차 참조가 포함됩니다. 이는 애플리케이션의 가비지 컬렉터가 처리 속도 및 처리량에 미치는 영향을 분석하는 데 유용합니다.

### 어셈블러 {#assembler}

<!-- CL 147218 -->
`arm64` 아키텍처에서, `R18` 레지스터가 `R18_PLATFORM`으로 이름이 변경되었습니다. 이는 운영체제가 이 레지스터를 예약할 수 있으므로, 의도치 않은 사용을 방지하기 위한 조치입니다.

## 런타임 {#runtime}

<!-- CL 138959 -->
Go 1.12 버전에서 힙의 상당 부분이 살아있는 상태일 때, 스윕 작업의 성능이 크게 향상됩니다. 이는 가비지 컬렉션 후 즉시 발생하는 할당 지연 시간을 줄입니다.

<!-- CL 139719 -->
Go 런타임은 이제 운영 체제에 메모를 더 적극적으로 반환하며, 특히 기존 힙 공간을 재사용할 수 없는 큰 할당에 응답합니다.

<!-- CL 146342, CL 146340, CL 146345, CL 146339, CL 146343, CL 146337, CL 146341, CL 146338 -->
Go 런타임의 타이머 및 데드라인 코드는 더 많은 CPU 수와 함께 더 빠르고 효율적으로 작동합니다. 특히, 이는 네트워크 연결 데드라인을 조작하는 성능을 향상시킵니다.

<!-- CL 135395 -->
리눅스에서, 런타임은 이제 사용되지 않는 메모리를 해제하기 위해 `MADV_FREE`를 사용합니다. 이는 더 효율적이지만 보고되는 RSS가 더 높아질 수 있습니다. 커널은 필요한 경우 사용되지 않는 데이터를 회수합니다.
Go 1.11의 동작(`MADV_DONTNEED`)으로 되돌리려면, 환경 변수 `GODEBUG=madvdontneed=1`을 설정하십시오.

<!-- CL 149578 -->
`cpu._extension_=off`를 환경 변수에 추가하면
[GODEBUG](/doc/diagnostics.html#godebug)가
표준 라이브러리와 런타임에서 선택적인 CPU 명령어 세트 확장을 사용하지 못하게 됩니다.
현재 Windows에서는 아직 지원되지 않습니다.

<!-- CL 158337 -->
Go 1.12은 큰 힙 할로케이션의 과도한 횟수를 수정하여 메모리 프로파일의 정확도를 향상시킵니다.

<!-- CL 159717 -->
`runtime.Caller` 및 `runtime.Callers`에서 컴파일러가 생성한 초기화 함수가 더 이상 포함되지 않습니다. 전역 변수의 초기화 중에 트레이스를 수행하면 이제 `PKG.init.ializers`라는 이름의 함수가 표시됩니다.

## 표준 라이브러리 {#library}

### TLS 1.3 {#tls_1_3}

Go 1.12는 `crypto/tls` 패키지에 [RFC 8446](https://www.rfc-editor.org/info/rfc8446)에서 정의된 TLS 1.3의 선택적 지원을 추가합니다. 이를 활성화하려면 `GODEBUG` 환경 변수에 `tls13=1` 값을 추가할 수 있습니다. Go 1.13에서는 기본적으로 활성화됩니다.

TLS 1.3를 협상하려면 다음을 확인하십시오.
[`Config`](/pkg/crypto/tls/#Config)에서 명시적인 `MaxVersion`을 설정하지 않도록 하고, 환경 변수 `GODEBUG=tls13=1`을 설정하여 프로그램을 실행하십시오.

다음 기능(`TLSUnique`)을 제외한 모든 TLS 1.2 기능은
[`ConnectionState`](/pkg/crypto/tls/#ConnectionState)에서 TLS 1.3에서 사용 가능하며, 동등하거나 더 나은 보안 및 성능을 제공합니다. TLS 1.3은 이전 버전과 역호환되지만, 일부 구형 시스템에서 TLS 1.3을 시도할 때 제대로 작동하지 않을 수 있습니다. 안전하지 않은 RSA 인증서 키(512비트 키 포함)는 TLS 1.3과 작동하지 않습니다.

TLS 1.3 암호화 모드는 구성할 수 없습니다. 지원되는 모든 암호화 모드는 안전하며, `Config`에서 `PreferServerCipherSuites`가 설정된 경우 선호 순서는 사용 가능한 하드웨어에 따라 결정됩니다.

초기 데이터 (또는 "0-RTT 모드")는 현재 클라이언트 또는 서버에서 지원되지 않습니다. 또한, Go 1.12 서버는 클라이언트가 이를 전송할 경우 예상치 못한 초기 데이터를 건너뛰는 것을 지원하지 않습니다. TLS 1.3의 0-RTT 모드는 클라이언트가 어떤 서버가 0-RTT를 지원하는지 추적해야 하므로, Go 1.12 서버는 다른 서버가 0-RTT를 지원하는 로드 밸런싱 풀의 일부가 될 수 없습니다. 특정 도메인을 0-RTT를 지원하는 서버에서 Go 1.12 서버로 전환할 경우, 전환 전에 최소 발행된 세션 티켓의 수명 동안 0-RTT를 비활성화해야 원활한 작동을 보장할 수 있습니다.

TLS 1.3에서 클라이언트는 핸드셰이크 마지막 단계에서 메시지를 보내므로, 서버에서 오류가 발생하면 클라이언트는 `Read`(`Read`](/pkg/crypto/tls/#Conn.Read)를 통해 오류를 받게 되며, `Handshake`(`Handshake`](/pkg/crypto/tls/#Conn.Handshake)를 통해 오류를 받지는 않습니다. 예를 들어, 서버가 클라이언트 인증서를 거부하는 경우에 해당됩니다.

마찬가지로, 세션 티켓은 이제 핸드셰이크 이후 메시지이므로, 클라이언트는 처음 `Read`(`Read`](/pkg/crypto/tls/#Conn.Read)를 통해만 수신됩니다.

### 라이브러리의 미세 조정 {#minor_library_changes}

물론, 라이브러리에는 항상 다양한 미세한 변경 사항과 업데이트가 있으며, 이는 Go 1의 [호환성 보장](/doc/go1compat)을 염두에 두고 만들어졌습니다.

<!-- TODO: CL 115677: https://golang.org/cl/115677: cmd/vet: 내장 필드 태그도 확인 -->

```
#### [bufio](/pkg/bufio/)
```

<!-- CL 149297 -->
`Reader`의 [`UnreadRune`](/pkg/bufio/#Reader.UnreadRune) 및
[`UnreadByte`](/pkg/bufio/#Reader.UnreadByte) 메서드는 이제 `Peek`가 호출된 후 호출될 경우 오류를 반환합니다.

<!-- bufio -->

#### [bytes](/pkg/bytes/)

<!-- CL 137855 -->
새로운 함수 [`ReplaceAll`](/pkg/bytes/#ReplaceAll)는 특정 값을 다른 값으로 대체한 후, 비중복되는 모든 인스턴스를 포함하는 바이트 슬라이스의 복사본을 반환합니다.

<!-- CL 145098 -->
`Reader`의 0값에 대한 포인터는 이제 [`NewReader`](/pkg/bytes/#NewReader)`(nil)`와 기능적으로 동일합니다.
Go 1.12 이전에는 이전 포인터를 모든 경우에 후자의 대체로 사용할 수 없었습니다.

<!-- 바이트 -->

#### [crypto/rand](/pkg/crypto/rand/)

<!-- CL 139419 -->
이제 `Reader.Read`가 커널로부터 엔트로피를 읽는 데 60초 이상 대기하는 경우 표준 오류에 경고가 출력됩니다.

<!-- CL 120055 -->
FreeBSD에서, `Reader`는 `getrandom` 시스템 호출을 사용할 수 있는 경우에 사용하고, 그렇지 않은 경우에는 `/dev/urandom`을 사용합니다.

<!-- crypto/rand -->

#### [crypto/rc4](/pkg/crypto/rc4/)

<!-- CL 130397 -->
이 릴리스에서는 어셈블리 구현을 제거하고, 순 Go 버전만 남깁니다. Go 컴파일러는 CPU에 따라 약간 더 나거나 약간 덜 효율적인 코드를 생성합니다. RC4는 안전하지 않으므로, 기존 시스템과의 호환성을 위해만 사용해야 합니다.

<!-- crypto/rc4 -->

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 143177 -->
클라이언트가 TLS와 유사하지 않은 초기 메시지를 보내면, 서버는 더 이상 경고를 보내지 않고, `net.Conn`의 기본 연결을 새 필드 `Conn`의 `RecordHeaderError`에 노출합니다.

<!-- crypto/tls -->

#### [database/sql](/pkg/database/sql/)

<!-- CL 145738 -->
쿼리 커서를 이제 `*Rows` 값을 `Row.Scan` 메서드에 전달하여 얻을 수 있습니다.
[`*Rows`](/pkg/database/sql/#Rows)

<!-- database/sql -->

#### [expvar](/pkg/expvar/)

<!-- CL 139537 -->
새로운 `Delete` 메서드는 [`Map`](/pkg/expvar/#Map)에서 키/값 쌍을 삭제할 수 있도록 합니다.

<!-- expvar -->

#### [fmt](/pkg/fmt/)

<!-- CL 142737 -->
지도들이 키 순서대로 인쇄되도록 변경되어 테스트가 용이하도록 했습니다. 정렬 규칙은 다음과 같습니다:

- 해당되는 경우, nil은 가장 낮게 비교
  - 정수, 부동 소수점 수, 문자열은 `<`를 기준으로 비교
  - NaN은 non-NaN 부동 소수점 수보다 작게 비교
  - bool은 false를 true보다 먼저 비교
  - Complex는 먼저 실수, 그 다음 허수 순으로 비교
  - 포인터는 머신 주소로 비교
  - 채널 값은 머신 주소로 비교
  - 구조체는 각 필드를 순서대로 비교
  - 배열은 각 요소를 순서대로 비교
  - 인터페이스 값은 먼저 `reflect.Type`으로 설명된 구체적인 유형으로 비교하고, 그 다음 이전 규칙에 설명된 구체적인 값으로 비교

<!-- CL 129777 -->
지도 출력을 할 때, `NaN`과 같이 반사되지 않는 키 값을 이전에 `<nil>`로 표시했습니다. 이번 릴리스부터는 올바른 값이 표시됩니다.

<!-- fmt -->

#### [go/doc](pkg/go/doc/)

<!-- CL 140958 -->
`cmd/doc` 내의 일부 해결되지 않은 문제를 해결하기 위해,
이 패키지는 새로운 [`Mode`](/pkg/go/doc/#Mode) 비트, `PreserveAST`를 도입했습니다.
이 비트는 AST 데이터가 삭제되는지 여부를 제어합니다.

<!-- go/doc -->

#### [go/token](pkg/go/token/)

<!-- CL 134075 -->
`[`File`](/pkg/go/token#File) 타입에 새로운
`[LineStart]('/',pkg/go/token#File.LineStart)` 필드가 추가되었습니다.
이 필드는 주어진 라인의 시작 위치를 반환합니다. 이는 어셈블리와 같은 비-Go 파일도 처리하는 프로그램에서 특히 유용하며, 파일 위치를 식별하기 위해 `token.Pos` 메커니즘을 사용하고 싶을 때 활용할 수 있습니다.

<!-- go/token -->

#### [이미지](/pkg/image/)

<!-- CL 118755 -->
`RegisterFormat` 함수가 이제 동시 사용이 안전합니다.

<!-- 이미지 -->

#### [이미지/png](/pkg/image/png/)

<!-- CL 134235 -->
색상 팔레트가 있는 이미지를 16개 이하의 색상으로 사용하면, 출력 크기가 작게 됩니다.

<!-- 이미지/png -->

```
#### [io](/pkg/io/)
```

<!-- CL 139457 -->
새로운 [`StringWriter`](/pkg/io#StringWriter) 인터페이스는 [`WriteString`](/pkg/io/#WriteString) 함수를 감쌉니다.

<!-- io -->

#### [math](/pkg/math/)

<!-- CL 153059 -->
다음 함수:
[`Sin`](/pkg/math/#Sin),
[`Cos`](/pkg/math/#Cos),
[`Tan`](/pkg/math/#Tan),
그리고 [`Sincos`](/pkg/math/#Sincos)는 이제 매우 큰 인수에 대해 Payne-Hanek 범위 감소를 적용합니다.
이는 더 정확한 결과를 제공하지만 이전 버전의 결과와 정확히 일치하지는 않습니다.

<!-- 수식 -->

#### [math/bits](pkg/math/bits/)

<!-- CL 123157 -->
새로운 확장된 정밀도 연산 [`Add`](/pkg/math/bits/#Add), [`Sub`](/pkg/math/bits/#Sub), [`Mul`](/pkg/math/bits/#Mul), 및 [`Div`](/pkg/math/bits/#Div)가 `uint`, `uint32`, 및 `uint64` 버전에서 사용 가능합니다.

<!-- 수학/비트 -->

#### [net](pkg/net/)

<!-- CL 146659 -->
`Dialer.DualStack` 설정은 이제 무시되고 더 이상 사용되지 않습니다. RFC 6555의 "Fast Fallback" (Happy Eyeballs) 기능이 기본적으로 활성화되었습니다. 비활성화하려면 `Dialer.FallbackDelay`를 음수 값으로 설정하십시오.

<!-- CL 107196 -->
마찬가지로, `Dialer.KeepAlive`가 0이면 TCP keep-alive가 기본적으로 활성화됩니다.
활성화하려면 음수 값으로 설정합니다.

<!-- CL 113997 -->
Linux에서는 [`splice` 시스템 호출](https://man7.org/linux/man-pages/man2/splice.2.html)이 `UnixConn`에서 `TCPConn`으로 복사할 때 사용됩니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- CL 143177 -->
HTTP 서버는 이제 평문 "400 Bad Request" 응답으로 잘못된 HTTP 요청을 HTTPS 서버로 보내는 것을 거부합니다.

<!-- CL 130115 -->
새로운 `Client.CloseIdleConnections`
메서드는, 만약 `Client`의 기본 `Transport`에 해당 메서드가 있다면, `Transport`의 `CloseIdleConnections`
메서드를 호출합니다.

<!-- CL 145398 -->
`Transport`가 이제 HTTP 응답을 거부하지 않습니다. HTTP Trailers를 선언하지만 chunked encoding을 사용하지 않는 HTTP 응답도 처리합니다. 대신, 선언된 Trailers는 이제 무시됩니다.

<!-- CL 152080 -->
<!-- CL 151857 -->
`[Transport](pkg/net/http/#Transport)`는 이제 Go 1.10 및 Go 1.11에서와 같이 HTTP/2 서버에서 광고하는 `MAX_CONCURRENT_STREAMS` 값을 엄격하게 처리하지 않습니다. 기본 동작은 이제 Go 1.9와 동일하게 돌아갑니다. 즉, 각 서버 연결은 최대 `MAX_CONCURRENT_STREAMS`개의 요청을 가질 수 있으며, 필요한 경우 새 TCP 연결이 생성됩니다. Go 1.10 및 Go 1.11에서는 `http2` 패키지가 요청이 완료될 때까지 대기하고 새 연결을 생성하는 대신 차단되었습니다.
엄격한 동작을 다시 얻으려면 다음 패키지를 직접 가져오고
[`golang.org/x/net/http2](https://godoc.org/golang.org/x/net/http2)를 가져와
[`Transport.StrictMaxConcurrentStreams`](https://godoc.org/golang.org/x/net/http2#Transport.StrictMaxConcurrentStreams)를 `true`로 설정하십시오.

<!-- net/http -->

#### [net/url](/pkg/net/url/)

<!-- CL 159157, CL 160178 -->
[`Parse`](/pkg/net/url/#Parse),
[`ParseRequestURI`](/pkg/net/url/#ParseRequestURI),
그리고
[`URL.Parse`](/pkg/net/url/#URL.Parse)
은 이제 ASCII 제어 문자가 포함된 URL에 대해 오류를 반환합니다. 여기에는 NULL, 탭 및 줄바꿈이 포함됩니다.

<!-- net/url -->

#### [net/http/httputil](/pkg/net/http/httputil/)

<!-- CL 146437 -->
`ReverseProxy`는 이제 자동으로 WebSocket 요청을 프록시합니다.

<!-- net/http/httputil -->

```
#### [os](pkg/os/)
```

<!-- CL 125443 -->
새로운 `ProcessState.ExitCode` 메서드는 프로세스의 종료 코드를 반환합니다.

<!-- CL 135075 -->
`ModeCharDevice`가 `ModeType` 비트 마스크에 추가되어, `ModeDevice | ModeCharDevice`를 `ModeType`를 사용하여 마스킹할 때 `FileMode`를 처리할 수 있습니다.

<!-- CL 139418 -->
새로운 함수 [`UserHomeDir`](/pkg/os/#UserHomeDir)는 현재 사용자의 홈 디렉토리를 반환합니다.

<!-- CL 146020 -->
[`RemoveAll`](/pkg/os/#RemoveAll) 이제 대부분의 유닉스 시스템에서 4096자보다 긴 경로도 지원합니다.

<!-- CL 130676 -->
[`File.Sync`](/pkg/os/#File.Sync)는 이제 macOS에서 `F_FULLFSYNC`를 사용하여 파일 내용을 영구 저장소에 올바르게 플래시합니다.
이로 인해 메서드가 이전 버전보다 더 느리게 실행될 수 있습니다.

<!--CL 155517 -->
[`File`](/pkg/os/#File)가 이제
`SyscallConn`](/pkg/os/#File.SyscallConn) 메서드를 지원하며,
이는
`syscall.RawConn`](/pkg/syscall/#RawConn) 인터페이스 값을 반환합니다.
이를 통해 파일 디스크립터에 대한 시스템별 작업을 호출할 수 있습니다.

<!-- os -->

#### [path/filepath](/pkg/path/filepath/)

<!-- CL 145220 -->
`IsAbs` 함수가 이제 Windows에서 예약된 파일 이름(`NUL`과 같은)을 전달받을 때 `true`를 반환합니다.
[예약된 이름 목록.](https://docs.microsoft.com/en-us/windows/desktop/fileio/naming-a-file#naming-conventions)

<!-- path/경로 -->

#### [reflect](/pkg/reflect/)

<!-- CL 33572 -->
새로운 [`MapIter`](/pkg/reflect#MapIter) 타입은 맵을 순회하기 위한 반복자입니다. 이 타입은 `Value` 타입의 새로운 `MapRange` 메서드를 통해 노출됩니다.
이는 `range` 문과 동일한 반복 메커니즘을 사용하며, `Next`를 사용하여 반복자를 진행하고, `Key`/`Value`를 사용하여 각 항목에 접근합니다.

<!-- 반영 -->

#### [regexp](/pkg/regexp/)

<!-- CL 139784 -->
[`Copy`](/pkg/regexp/#Regexp.Copy)는 더 이상 필요하지 않으며,
잠금 경쟁을 피하기 위해 부분적으로 비활성화됩니다.
[`Copy`](/pkg/regexp/#Regexp.Copy)
두 개의 다른 [`Longest`](/pkg/regexp/#Regexp.Longest) 설정을 가진 복사본을 만드는 것이 그 이유라면 여전히 적절할 수 있습니다.

<!-- 정규 표현식 -->

#### [runtime/debug](/pkg/runtime/debug/)

<!-- CL 144220 -->
새로운 `BuildInfo` 타입이
실행 중인 바이너리에서 읽어온 빌드 정보를 노출합니다. 이 정보는 모듈 지원으로 빌드된 바이너리에만 사용할 수 있습니다. 여기에는 메인 패키지 경로, 메인 모듈 정보 및 모듈 종속성이 포함됩니다. 이 타입은 `ReadBuildInfo` 함수를 통해 `BuildInfo`에서 가져올 수 있습니다.

<!-- 실행/디버깅 -->

#### [strings](/pkg/strings/)

<!-- CL 137855 -->
새로운 함수 [`ReplaceAll`](/pkg/strings/#ReplaceAll)는 특정 값의 모든 비겹치는 인스턴스를 다른 값으로 대체한 문자열의 복사본을 반환합니다.

<!-- CL 145098 -->
`Reader`의 제로값에 대한 포인터는 이제 기능적으로 `NewReader`(/pkg/strings/#NewReader)(`nil`)와 동일합니다.
Go 1.12 이전에는 이전 포인터를 후자의 모든 경우에 대체로 사용할 수 없었습니다.

<!-- CL 122835 -->
새로운 `Builder.Cap` 메서드는 빌더의 내부 바이트 슬라이스의 용량을 반환합니다.

<!-- CL 131495 -->
`Map` ([]pkg/strings/#Map),
`Title` ([]pkg/strings/#Title),
`ToLower` ([]pkg/strings/#ToLower),
`ToLowerSpecial` ([]pkg/strings/#ToLowerSpecial),
`ToTitle` ([]pkg/strings/#ToTitle),
`ToTitleSpecial` ([]pkg/strings/#ToTitleSpecial),
`ToUpper` ([]pkg/strings/#ToUpper), 및
`ToUpperSpecial` ([]pkg/strings/#ToUpperSpecial)
기능은 이제 항상 유효한 UTF-8을 반환합니다. 이전 버전에서는 입력이 유효하지 않은 UTF-8이었지만, 문자를 대체할 필요가 없는 경우, 이러한 함수는 잘못된 UTF-8을 수정하지 않고 그대로 반환했습니다.

<!-- 문자열 -->

#### [syscall](/pkg/syscall/)

<!-- CL 138595 -->
64비트 inode가 FreeBSD 12에서 지원됩니다. 일부 유형은 이에 따라 조정되었습니다.

<!-- CL 125456 -->
유닉스 소켓
([`AF_UNIX`](https://blogs.msdn.microsoft.com/commandline/2017/12/19/af_unix-comes-to-windows/))
주소 패밀리가 호환되는 Windows 버전에서 지원됩니다.

<!-- CL 147117 -->
새로운 함수 [`Syscall18`](/pkg/syscall/?GOOS=windows&GOARCH=amd64#Syscall18)가 Windows용으로 도입되었으며, 최대 18개의 인자를 전달할 수 있도록 합니다.

<!-- syscall -->

```
#### [syscall/js](/pkg/syscall/js/)
```

<!-- CL 153559 -->

`Callback` 타입과 `NewCallback` 함수는 이름이 변경되었습니다.
이제 `Func` 및 `FuncOf`로 불립니다.
(`/pkg/syscall/js/?GOOS=js&GOARCH=wasm#Func`) 및
(`/pkg/syscall/js/?GOOS=js&GOARCH=wasm#FuncOf`) 각각.
이것은 호환성을 해치는 변경 사항이지만, WebAssembly 지원은 여전히 실험적이며
[Go 1 호환성 약속](/doc/go1compat)을 아직 준수하지 않습니다. 이전 이름으로 사용하는 코드는 업데이트해야 합니다.

<!-- CL 141644 -->
만약 타입이 새로운
[`Wrapper`](/pkg/syscall/js/?GOOS=js&GOARCH=wasm#Wrapper)
인터페이스를 구현하면,
[`ValueOf`](/pkg/syscall/js/?GOOS=js&GOARCH=wasm#ValueOf)
는 해당 타입에 대한 JavaScript 값을 반환하는 데 사용됩니다.

<!-- CL 143137 -->
"0"의 의미
[`Value`](/pkg/syscall/js/?GOOS=js&GOARCH=wasm#Value)
가 변경되었습니다. 이제는 숫자 0 대신 JavaScript의 `undefined` 값을 나타냅니다.
이것은 호환성 문제가 있는 변경 사항이지만, WebAssembly 지원은 여전히 실험적이며 [Go 1 호환성 약속](/doc/go1compat)에 아직 적용되지 않습니다. "0"을 숫자 0으로 해석하는 코드는 업데이트해야 합니다.

<!-- CL 144384 -->
새로운
[`Value.Truthy`](/pkg/syscall/js/?GOOS=js&GOARCH=wasm#Value.Truthy)
메서드는 주어진 값의
[JavaScript "truthiness"](https://developer.mozilla.org/en-US/docs/Glossary/Truthy)
을 보고합니다.

<!-- syscall/js -->

#### [테스팅](/pkg/testing/)

<!-- CL 139258 -->
`[-benchtime](cmd/go/#hdr-Testing_flags)` 플래그는 이제 값이 "`x`"로 끝날 때 시간 대신 명시적인 반복 횟수를 설정할 수 있습니다. 예를 들어, `-benchtime=100x`는 벤치마크를 100번 실행합니다.

<!-- 테스트 -->

#### [text/template](pkg/text/template/)

<!-- CL 142217 -->
템플릿을 실행할 때, 긴 컨텍스트 값은 더 이상 오류 메시지에 잘리거나 표시되지 않습니다.

`"tmpl" 실행 중 (<.very.deep.context.v...>: 맵에 "notpresent" 키가 없음`

현재

`"tmpl" 실행 중 <.very.deep.context.value.notpresent>에서: map에 "notpresent" 키가 없음`

<!-- CL 143097 -->
템플릿에서 호출되는 사용자 정의 함수가 패닉을 발생시키면,
패닉이 이제 `Execute` 또는 `ExecuteTemplate` 메서드에 의해 
포착되어 오류로 반환됩니다.

```markdown
<!-- 템플릿 -->

#### [time](/pkg/time/)

<!-- CL 151299 -->
`$GOROOT/lib/time/zoneinfo.zip`에 있는 시간대 데이터베이스가 2018i 버전으로 업데이트되었습니다. 이 ZIP 파일은 운영체제에서 시간대 데이터베이스를 제공하지 않을 경우에만 사용됩니다.

<!-- 시간 -->

#### [unsafe](/pkg/unsafe/)

<!-- CL 146058 -->
`unsafe.Pointer`가 nil인 경우, 이를 `uintptr`로 변환한 다음 산술 연산을 수행하고 다시 `uintptr`로 변환하는 것은 유효하지 않습니다.
(이것은 이미 유효하지 않았지만, 이제는 컴파일러가 잘못 동작하게 됩니다.)

<!-- unsafe -->
