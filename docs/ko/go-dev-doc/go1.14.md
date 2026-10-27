<!--
참고: 이 문서 및 이 디렉토리의 다른 문서들에서는 `hello` `world`와 같이 고정 폭 구문을 비고정 폭 공백으로 설정하는 관례를 따릅니다.
이러한 구문에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

<style>
  main ul li { margin: 0.5em 0; }
</style>

## Go 1.14 소개 {#introduction}

최신 Go 릴리스인 버전 1.14가 [Go 1.13](go1.13) 이후 6개월 만에 출시되었습니다.
변경 사항의 대부분은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언제나 그랬듯이, 이번 릴리스에서도 Go 1 [호환성 약속](/doc/go1compat.html)이 유지됩니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

`go` 명령어의 모듈 지원이 이제 프로덕션 환경에서 사용할 준비가 되었으며, 모든 사용자가 [의존성 관리를 위해 Go 모듈로 마이그레이션](/blog/migrating-to-go-modules)하는 것을 권장합니다. Go 툴체인의 문제로 인해 마이그레이션이 불가능한 경우, 해당 문제에 대해 [오픈 이슈](/issue?q=is%3Aissue+is%3Aopen+label%3Amodules)가 등록되어 있는지 확인해 주십시오. (해당 이슈가 `Go1.15` 마일스톤에 포함되어 있지 않다면, 마이그레이션을 방해하는 이유를 알려주시기 바랍니다. 이를 통해 적절한 우선순위를 지정하도록 하겠습니다.)

## 언어 변경 사항 {#language}

[overlapping interfaces 제안](https://github.com/golang/proposal/blob/master/design/6977-overlapping-interfaces.md)에 따라,
Go 1.14부터는 메서드 집합이 겹치는 인터페이스의 임베딩을 허용합니다.
임베딩된 인터페이스의 메서드는 (임베딩하는) 인터페이스에 이미 존재하는 메서드와 이름이 같고 시그니처가 동일할 수 있습니다. 이는 일반적으로 (단독으로만 발생하는 것은 아니지만) 다이아몬드 형태의 임베딩 그래프에서 발생하는 문제들을 해결합니다.
인터페이스 내에 명시적으로 선언된 메서드들은 이전과 마찬가지로 [고유](https://tip.golang.org/ref/spec#Uniqueness_of_identifiers)해야 합니다.

## 포트 {#ports}

### Darwin {#darwin}

Go 1.14은 macOS 10.11 El Capitan에서 실행되는 마지막 릴리스입니다.
Go 1.15부터는 macOS 10.12 Sierra 또는 그 이후 버전이 필요합니다.

<!-- golang.org/issue/34749 -->
Go 1.14은 macOS에서 32비트 바이너리(`darwin/386` 포트)를 지원하는 마지막 Go 릴리스입니다. macOS 10.15(Catalina)부터는 더 이상 지원되지 않습니다.
Go는 64비트 `darwin/amd64` 포트를 계속해서 지원합니다.

<!-- golang.org/issue/34751 -->
Go 1.14은 iOS, iPadOS, watchOS 및 tvOS에서 32비트 바이너리를 지원하는 마지막 Go 릴리스가 될 가능성이 높습니다
(`darwin/arm` 포트). Go는 64비트 `darwin/arm64` 포트를 계속해서 지원합니다.

### Windows {#windows}

<!-- CL 203601 -->
이제 Windows의 Go 바이너리에는 [DEP
(데이터 실행 방지)](https://docs.microsoft.com/en-us/windows/win32/memory/data-execution-prevention)가 활성화됩니다.

<!-- CL 202439 -->
Windows에서 [`os.O_CREATE`](/pkg/os/#O_CREATE) 플래그와 함께 [`os.OpenFile`](/pkg/os#CreateFile)을 사용하거나, [`syscall.O_CREAT`](/pkg/syscall#O_CREAT) 플래그와 함께 [`syscall.Open`](/pkg/syscall#Open)을 통해 파일을 생성할 때, 권한 인자에 `0o200` 비트(소유자 쓰기 권한)가 설정되어 있지 않으면 이제 파일을 읽기 전용으로 생성합니다. 이를 통해 Windows에서의 동작이 Unix 시스템의 동작과 더 유사해졌습니다.

### WebAssembly {#wasm}

<!-- CL 203600 -->
`js.Value` 객체를 통해 Go에서 참조되는 JavaScript 값들을 이제 가비지 컬렉션(garbage collect)할 수 있습니다.

<!-- CL 203600 -->
`js.Value` 값은 더 이상 `==` 연산자를 사용하여 비교할 수 없으며, 대신 `Equal` 메서드를 사용하여 비교해야 합니다.

<!-- CL 203600 -->
`js.Value`에 이제 `IsUndefined`, `IsNull`,
그리고 `IsNaN` 메서드가 추가되었습니다.

### RISC-V {#riscv}

<!-- Issue 27532 -->
Go 1.14은 Linux(`GOOS=linux`, `GOARCH=riscv64`) 환경의 64비트 RISC-V에 대한 실험적 지원을 포함합니다. 성능, 어셈블리 구문 안정성, 그리고 잠재적인 정확성 부분은 현재 개선 작업 중임을 유의하시기 바랍니다.

### FreeBSD {#freebsd}

<!-- CL 199919 -->
이제 Go는 FreeBSD 12.0 이상 버전의 64비트 ARM 아키텍처(`freebsd/arm64` 포트)를 지원합니다.

### Native Client (NaCl) {#nacl}

<!-- golang.org/issue/30439 -->
Go 1.13 릴리스 노트에서 [공지](go1.13#ports)한 바와 같이,
Go 1.14부터는 Native Client 플랫폼(`GOOS=nacl`)에 대한 지원이 중단됩니다.

### Illumos {#illumos}

<!-- CL 203758 -->
이제 런타임이 `runtime.NumCPU` 및 `GOMAXPROCS`의 기본값에 대해 zone CPU 캡(`zone.cpu-cap` 리소스 제어)을 준수합니다.

## Tools {#tools}

### Go 명령어 {#go-command}

#### 벤더링 (Vendoring) {#vendor}

<!-- golang.org/issue/33848 -->

메인 모듈에 최상위 `vendor` 디렉터리가 포함되어 있고 `go.mod` 파일에 `go` `1.14` 이상의 버전이 지정된 경우, 이제 `go` 명령어는 해당 플래그를 허용하는 작업에 대해 기본적으로 `-mod=vendor`를 사용합니다. 이 플래그의 새로운 값인 `-mod=mod`를 사용하면, `go` 명령어는 (`vendor` 디렉터리가 없을 때와 마찬가지로) 모듈 캐시에서 모듈을 로드합니다.

`-mod=vendor`가 설정된 경우(명시적으로 또는 기본값으로), 이제 `go` 명령은 메인 모듈의 `vendor/modules.txt` 파일이 `go.mod` 파일과 일치하는지 확인합니다.

`go` `list` `-m` 명령어가 `vendor` 디렉터리에 패키지를 제공하지 않는 간접 의존성(transitive dependencies)을 더 이상 조용히 생략하지 않습니다. 이제 `-mod=vendor`가 설정되어 있고 `vendor/modules.txt`에 언급되지 않은 모듈에 대한 정보를 요청하는 경우, 명시적으로 실패합니다.

#### 플래그 {#go-flags}

<!-- golang.org/issue/32502, golang.org/issue/30345 -->
`go` `get` 명령어는 더 이상 `-mod` 플래그를 허용하지 않습니다. 이전에는 이 플래그 설정이 [무시되었거나](/issue/30345) [빌드 실패를 유발했습니다](/issue/32502).

<!-- golang.org/issue/33326 -->
`go.mod` 파일이 읽기 전용이고 최상위 `vendor` 디렉터리가 없는 경우, 이제 `-mod=readonly`가 기본값으로 설정됩니다.

<!-- golang.org/issue/31481 -->
`-modcacherw`는 `go` 명령어가 모듈 캐시에 새로 생성된 디렉토리를 읽기 전용으로 만드는 대신 기본 권한으로 남겨두도록 지시하는 새로운 플래그입니다.
이 플래그를 사용하면 테스트나 다른 도구가 모듈의 검증된 체크섬에 포함되지 않은 파일을 실수로 추가할 가능성이 높아집니다.
하지만, 모듈 캐시를 삭제할 때 (`go` `clean` `-modcache` 대신) `rm` `-rf`를 사용할 수 있게 해줍니다.

<!-- golang.org/issue/34506 -->
`-modfile=file`는 `go` 커맨드가 모듈 루트 디렉토리에 있는 `go.mod` 파일 대신 대체 `go.mod` 파일을 읽고(그리고 가능하면 쓰도록) 지시하는 새로운 플래그입니다. 모듈 루트 디렉토리를 결정하기 위해 `go.mod`라는 이름의 파일이 여전히 존재해야 하지만, 해당 파일에 접근하지는 않습니다. `-modfile`이 지정되면 대체 `go.sum` 파일도 함께 사용됩니다. 이 파일의 경로는 `-modfile` 플래그에서 `.mod` 확장자를 제거하고 `.sum`을 추가하여 유도됩니다.

#### 환경 변수 {#go-env-vars}

<!-- golang.org/issue/32966 -->
`GOINSECURE`는 특정 모듈을 원본에서 직접 가져올 때 `go` 명령어가 HTTPS 연결을 요구하지 않고 인증서 검증을 건너뛰도록 지시하는 새로운 환경 변수입니다. 기존의 `GOPRIVATE` 변수와 마찬가지로, `GOINSECURE`의 값은 쉼표로 구분된 글로브 패턴(glob patterns) 목록입니다.

#### 모듈 외부의 명령어 {#commands-outside-modules}

<!-- golang.org/issue/32027 -->
모듈 인식 모드가 명시적으로 활성화된 경우(`GO111MODULE=on` 설정 시), `go.mod` 파일이 없으면 대부분의 모듈 명령의 기능이 제한됩니다. 예를 들어, `go` `build`, `go` `run` 및 기타 빌드 명령은 표준 라이브러리의 패키지와 명령줄에 `.go` 파일로 지정된 패키지만 빌드할 수 있습니다.

이전에는 `go` 명령어가 각 패키지 경로를 모듈의 최신 버전으로 해석했지만, 모듈 경로와 버전을 기록하지는 않았습니다. 이로 인해 [느리고 재현 불가능한 빌드](/issue/32027)가 발생했습니다.

`go` `get`는 이전과 동일하게 작동하며, `go` `mod` `download`와 명시적 버전을 사용하는 `go` `list` `-m` 역시 마찬가지입니다.

#### `+incompatible` 버전 {#incompatible-versions}

<!-- golang.org/issue/34165 -->

모듈의 최신 버전에 `go.mod` 파일이 포함되어 있는 경우, `go` `get`은 해당 버전을 명시적으로 요청하거나 이미 필요한 경우가 아니라면 해당 모듈의 [호환되지 않는](/cmd/go/#hdr-Module_compatibility_and_semantic_versioning) 메이저 버전으로 더 이상 업그레이드하지 않습니다.
`go` `list` 또한 버전 관리 시스템에서 직접 가져올 때 해당 모듈의 호환되지 않는 메이저 버전을 생략하지만, 프록시에 의해 보고된 경우에는 포함될 수 있습니다.

#### `go.mod` 파일 유지 관리 {#go.mod}

<!-- golang.org/issue/34822 -->

`go mod tidy` 이외의 `go` 명령어는 메인 모듈의 다른 (전이적) 의존성에 의해 이미 암시된 간접 의존성 버전이 지정된 `require` 지시문을 더 이상 제거하지 않습니다.

`go mod tidy` 외의 `go` 명령어들은 변경 사항이 단순한 서식 수정(cosmetic)일 경우 더 이상 `go.mod` 파일을 수정하지 않습니다.

`-mod=readonly`가 설정되면, `go` 명령은 더 이상 누락된 `go` 지시문이나 잘못된 `// indirect` 주석으로 인해 실패하지 않습니다.

#### 모듈 다운로드 {#module-downloading}

<!-- golang.org/issue/26092 -->
이제 `go` 명령어가 모듈 모드에서 Subversion 리포지토리를 지원합니다.

<!-- golang.org/issue/30748 -->
이제 `go` 명령어는 모듈 프록시 및 기타 HTTP 서버로부터 받은 일반 텍스트 에러 메시지 스니펫을 포함합니다.
에러 메시지는 유효한 UTF-8이며 그래픽 문자(graphic characters)와 공백으로만 구성된 경우에만 표시됩니다.

#### 테스트 {#go-test}

<!-- golang.org/issue/24929 -->
`go test -v`는 이제 모든 테스트가 끝난 후가 아니라, `t.Log` 출력이 발생하는 즉시 스트리밍하여 표시합니다.

## 런타임 {#runtime}

<!-- CL 190098 -->
이번 릴리스에서는 대부분의 `defer` 사용 사례에 대한 성능을 개선하여, 지연 함수를 직접 호출하는 것과 비교했을 때 오버헤드가 거의 발생하지 않도록 했습니다.
그 결과, 이제 성능이 중요한 코드에서도 오버헤드 걱정 없이 `defer`를 사용할 수 있습니다.

<!-- CL 201760, CL 201762 and many others -->
이제 Goroutine은 비동기적으로 선점(preemptible) 가능합니다.
그 결과, 함수 호출이 없는 루프가 스케줄러를 데드락 상태로 만들거나 가비지 컬렉션을 크게 지연시킬 가능성이 사라졌습니다.
이 기능은 `windows/arm`, `darwin/arm`, `js/wasm`, `plan9/*`를 제외한 모든 플랫폼에서 지원됩니다.

선점(preemption) 구현의 결과로, Linux 및 macOS 시스템을 포함한 Unix 시스템에서 Go 1.14로 빌드된 프로그램은 이전 릴리스로 빌드된 프로그램보다 더 많은 시그널을 받게 됩니다.

이는 [`syscall`](/pkg/syscall/) 또는 [`golang.org/x/sys/unix`](https://godoc.org/golang.org/x/sys/unix)와 같은 패키지를 사용하는 프로그램에서 느린 시스템 콜이 `EINTR` 오류로 인해 실패하는 경우가 더 많아짐을 의미합니다. 이러한 프로그램들은 루프를 통해 시스템 콜을 다시 시도하는 등의 방식으로 해당 오류를 처리해야 합니다. 이에 대한 자세한 내용은 Linux 시스템의 경우 [`man 7 signal`](https://man7.org/linux/man-pages/man7/signal.7.html) 또는 다른 시스템의 유사한 문서를 참조하십시오.

<!-- CL 201765, CL 195701 and many others -->
페이지 할당자(page allocator)가 더 효율적으로 개선되었으며, `GOMAXPROCS` 값이 높을 때 락 경합(lock contention)이 현저히 줄어들었습니다.
이는 대규모 할당이 높은 빈도로 병렬 수행될 때, 지연 시간이 낮아지고 처리량이 증가하는 형태로 가장 두드러지게 나타납니다.

<!-- CL 171844 및 기타 다수 -->
[`time.After`](/pkg/time/#After),
[`time.Tick`](/pkg/time/#Tick),
[`net.Conn.SetDeadline`](/pkg/net/#Conn)
및 관련 기능에서 사용하는 내부 타이머가 개선되어, 락 경합(lock contention)과 컨텍스트 스위칭(context switches)이 줄어들어 더 효율적으로 동작합니다.
이는 성능 향상을 위한 변경 사항이며, 사용자에게 보이는 가시적인 변경 사항은 발생하지 않습니다.

## 컴파일러 {#compiler}

<!-- CL 162237 -->
이번 릴리스에서는 Go 코드가 `unsafe.Pointer` 안전 규칙을 동적으로 준수하는지 확인하기 위한 인스트루멘테이션(instrumentation)을 추가하는 컴파일 타임 옵션인 `-d=checkptr`가 추가되었습니다.
이 옵션은 `-race` 또는 `-msan` 플래그와 함께 사용할 때 기본적으로 활성화되며(Windows 제외), `-gcflags=all=-d=checkptr=0`를 통해 비활성화할 수 있습니다.
구체적으로, `-d=checkptr`는 다음 사항들을 확인합니다:

1. `unsafe.Pointer`를 `*T`로 변환할 때, 결과 포인터는 `T`에 맞게 적절히 정렬(aligned)되어 있어야 합니다.
2. 포인터 연산의 결과가 Go 힙 객체를 가리키는 경우, `unsafe.Pointer` 타입의 피연산자 중 하나는 반드시 동일한 객체를 가리키고 있어야 합니다.

Windows에서는 `-d=checkptr` 사용 시 표준 라이브러리에서 잘못된 경고(false alerts)가 발생하므로 현재 권장되지 않습니다.

<!-- CL 204338 -->
이제 컴파일러에서 `-json` 플래그를 사용하여 인라이닝(inlining), 탈출 분석(escape analysis), 경계 검사 제거(bounds-check elimination), nil 검사 제거(nil-check elimination)를 포함한 주요 최적화의 머신 판독 가능 로그를 생성할 수 있습니다.

<!-- CL 196959 -->
상세 탈출 분석 진단(`-m=2`)이 다시 작동합니다.
이 기능은 이전 릴리스의 새로운 탈출 분석 구현에서 누락되었었습니다.

<!-- CL 196217 -->
이제 macOS 바이너리의 모든 Go 심볼은 플랫폼 컨벤션에 따라 언더스코어(`_`)로 시작합니다.

<!-- CL 202117 -->
이번 릴리스에는 퍼징(fuzzing)을 위해 컴파일러가 삽입하는 커버리지 인스트루멘테이션(coverage instrumentation)에 대한 실험적 지원이 포함되었습니다.
자세한 내용은 [issue 14565](/issue/14565)를 참조하세요.
이 API는 향후 릴리스에서 변경될 수 있습니다.

<!-- CL 174704 -->
<!-- CL 196784 -->
경계 검사 제거(Bounds check elimination)가 이제 슬라이스 생성 정보를 사용하여 `int`보다 작은 타입의 인덱스에 대한 검사를 제거할 수 있습니다.

## 표준 라이브러리 {#library}

### 새로운 바이트 시퀀스 해싱 패키지 {#hash_maphash}

<!-- golang.org/issue/28322, CL 186877 -->
Go 1.14에는 바이트 시퀀스에 대한 해시 함수를 제공하는 새로운 패키지인 [`hash/maphash`](/pkg/hash/maphash/)가 포함되어 있습니다.
이 해시 함수들은 해시 테이블이나 임의의 문자열 또는 바이트 시퀀스를 부호 없는 64비트 정수의 균등 분포로 매핑해야 하는 기타 데이터 구조를 구현하는 데 사용하도록 설계되었습니다.

해시 함수는 충돌 저항성(collision-resistant)을 갖지만, 암호학적으로 안전(cryptographically secure)하지는 않습니다.

주어진 바이트 시퀀스의 해시 값은 단일 프로세스 내에서는 일관되게 유지되지만, 서로 다른 프로세스에서는 서로 다르게 나타납니다.

### 라이브러리의 소규모 변경 사항 {#minor_library_changes}

언제나 그렇듯, Go 1의 [호환성 약속](/doc/go1compat)을 염두에 두고 라이브러리에 다양한 소규모 변경 및 업데이트가 이루어졌습니다.

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 191976 -->
SSL 버전 3.0 (SSLv3)에 대한 지원이 제거되었습니다. SSLv3는 TLS 이전의 [암호학적으로 취약한](https://tools.ietf.org/html/rfc7568) 프로토콜임에 유의하십시오.

<!-- CL 191999 -->
더 이상 `GODEBUG` 환경 변수를 통해 TLS 1.3을 비활성화할 수 없습니다. TLS 버전을 설정하려면 [`Config.MaxVersion`](/pkg/crypto/tls/#Config.MaxVersion) 필드를 사용하십시오.

<!-- CL 205059 -->
[`Config.Certificates`](/pkg/crypto/tls/#Config.Certificates) 필드를 통해 여러 인증서 체인이 제공될 때, 이제 피어(peer)와 호환되는 첫 번째 체인이 자동으로 선택됩니다. 이를 통해 예를 들어 ECDSA 인증서와 RSA 인증서를 모두 제공하고, 패키지가 자동으로 최적의 인증서를 선택하게 할 수 있습니다.
[`Certificate.Leaf`](/pkg/crypto/tls/#Certificate.Leaf) 필드가 설정되어 있지 않으면 이 선택 과정의 성능이 저하될 수 있음에 유의하십시오.
특정 이름에 단일 인증서만 연결할 수 있도록 지원하는 [`Config.NameToCertificate`](/pkg/crypto/tls/#Config.NameToCertificate) 필드는 이제 deprecated 되었으며 `nil`로 두어야 합니다.
마찬가지로, 리프(leaf) 인증서로부터 `NameToCertificate` 필드를 구축하는 [`Config.BuildNameToCertificate`](/pkg/crypto/tls/#Config.BuildNameToCertificate) 메서드 또한 이제 deprecated 되었으며 호출해서는 안 됩니다.

<!-- CL 175517 -->
새로운 [`CipherSuites`](/pkg/crypto/tls/#CipherSuites) 및 [`InsecureCipherSuites`](/pkg/crypto/tls/#InsecureCipherSuites) 함수는 현재 구현된 사이퍼 스위트(cipher suites) 목록을 반환합니다.
새로운 [`CipherSuiteName`](/pkg/crypto/tls/#CipherSuiteName) 함수는 사이퍼 스위트 ID에 해당하는 이름을 반환합니다.

<!-- CL 205058, 205057 -->
새로운 [
`(*ClientHelloInfo).SupportsCertificate`](/pkg/crypto/tls/#ClientHelloInfo.SupportsCertificate) 및
[
`(*CertificateRequestInfo).SupportsCertificate`](/pkg/crypto/tls/#CertificateRequestInfo.SupportsCertificate)
메서드는 피어(peer)가 특정 인증서를 지원하는지 여부를 노출합니다.

<!-- CL 174329 -->
`tls` 패키지는 더 이상 레거시 Next Protocol Negotiation (NPN) 확장을 지원하지 않으며, 이제 ALPN만 지원합니다. 이전 릴리스에서는 두 가지 모두를 지원했습니다. API 변경 사항은 없으며 애플리케이션은 이전과 동일하게 작동해야 합니다. 대부분의 다른 클라이언트와 서버는 이미 표준화된 ALPN을 위해 NPN 지원을 제거했습니다.

<!-- CL 205063, 205062 -->
이제 TLS 1.2 핸드셰이크에서 지원되는 경우 RSA-PSS 서명이 사용됩니다. 이는 대부분의 애플리케이션에 영향을 주지 않지만, RSA-PSS 서명을 지원하지 않는 커스텀 [`Certificate.PrivateKey`](/pkg/crypto/tls/#Certificate.PrivateKey) 구현체는 새로운 [`Certificate.SupportedSignatureAlgorithms`](/pkg/crypto/tls/#Certificate.SupportedSignatureAlgorithms) 필드를 사용하여 이를 비활성화해야 합니다.

<!-- CL 205059, 205059 -->
[`Config.GetConfigForClient`](/pkg/crypto/tls/#Config.GetConfigForClient)가 설정된 경우, 이제 [`Config.Certificates`](/pkg/crypto/tls/#Config.Certificates)와 [`Config.GetCertificate`](/pkg/crypto/tls/#Config.GetCertificate) 모두 nil일 수 있습니다. 콜백에서 인증서와 에러를 모두 반환하지 않으면, 이제 `unrecognized_name`이 전송됩니다.

<!-- CL 205058 -->
새로운 [`CertificateRequestInfo.Version`](/pkg/crypto/tls/#CertificateRequestInfo.Version)
필드는 클라이언트 인증서 콜백에 TLS 버전을 제공합니다.

<!-- CL 205068 -->
새로운 `TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256` 및
`TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256` 상수는 이전에
`TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305` 및
`TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305`로 지칭되었던 사이퍼 스위트(cipher suites)의 최종 이름을 사용합니다.

<!-- crypto/tls -->

#### [crypto/x509](/pkg/crypto/x509/)

<!-- CL 204046 -->
[`Certificate.CreateCRL`](/pkg/crypto/x509/#Certificate.CreateCRL)
이제 Ed25519 발행자를 지원합니다.

#### [debug/dwarf](/pkg/debug/dwarf/)

<!-- CL 175138 -->
`debug/dwarf` 패키지가 이제 DWARF 버전 5 읽기를 지원합니다.

새로운 메서드 [`(*Data).AddSection`](/pkg/debug/dwarf/#Data.AddSection)은 입력 파일로부터 임의의 새로운 DWARF 섹션을 DWARF `Data`에 추가하는 기능을 지원합니다.

<!-- CL 192698 -->
새로운 메서드 [`(*Reader).ByteOrder`](/pkg/debug/dwarf/#Reader.ByteOrder)는 현재 컴파일 단위의 바이트 순서(byte order)를 반환합니다.
이는 위치 설명(location descriptions)과 같이 네이티브 순서로 인코딩된 속성들을 해석하는 데 사용될 수 있습니다.

<!-- CL 192699 -->
새로운 [`(*LineReader).Files`](/pkg/debug/dwarf/#LineReader.Files) 메서드는 라인 리더(line reader)로부터 파일 이름 테이블을 반환합니다.
이는 `AttrDeclFile`과 같은 DWARF 속성 값을 해석하는 데 사용될 수 있습니다.

<!-- debug/dwarf -->

#### [encoding/asn1](/pkg/encoding/asn1/)

<!-- CL 126624 -->
[`Unmarshal`](/pkg/encoding/asn1/#Unmarshal)
함수가 이제 새로운 [`TagBMPString`](/pkg/encoding/asn1/#TagBMPString) 상수로 표현되는 ASN.1 문자열 타입 BMPString을 지원합니다.

<!-- encoding/asn1 -->

#### [encoding/json](/pkg/encoding/json/)

<!-- CL 200677 -->
[`Decoder`](/pkg/encoding/json/#Decoder) 타입은 현재 디코더 위치의 입력 스트림 바이트 오프셋을 반환하는 새로운 메서드 [`InputOffset`](/pkg/encoding/json/#Decoder.InputOffset)을 지원합니다.

<!-- CL 200217 -->
[`Compact`](/pkg/encoding/json/#Compact)는 더 이상 `U+2028` 및 `U+2029` 문자를 이스케이프하지 않습니다. 이는 문서화된 적이 없는 기능이었습니다. 적절한 이스케이프 처리를 위해서는 [`HTMLEscape`](/pkg/encoding/json/#HTMLEscape)를 참조하십시오.

<!-- CL 195045 -->
문서화된 동작을 더 밀접하게 따르기 위해, [`Number`](/pkg/encoding/json/#Number)가 더 이상 유효하지 않은 숫자를 허용하지 않습니다.
빈 문자열과 같이 유효하지 않은 숫자를 허용해야 하는 프로그램의 경우, 해당 타입을 [`Unmarshaler`](/pkg/encoding/json/#Unmarshaler)로 래핑하는 것을 고려하십시오.

<!-- CL 200237 -->
[`Unmarshal`](/pkg/encoding/json/#Unmarshal)은 이제 [`encoding.TextUnmarshaler`](/pkg/encoding/#TextUnmarshaler)를 구현하고 기본 타입이 string인 맵 키를 지원합니다.

<!-- encoding/json -->

#### [go/build](/pkg/go/build/)

<!-- CL 203820, 211657 -->
[`Context`](/pkg/go/build/#Context) 타입에 빌드를 위한 작업 디렉터리를 설정하는 데 사용할 수 있는 새로운 필드 `Dir`이 추가되었습니다.
기본값은 실행 중인 프로세스의 현재 디렉터리입니다.
모듈 모드에서 이 필드는 메인 모듈의 위치를 찾는 데 사용됩니다.

<!-- go/build -->

#### [go/doc](/pkg/go/doc/)

<!-- CL 204830 -->
새로운 [`NewFromFiles`](/pkg/go/doc/#NewFromFiles) 함수는 `*ast.File` 목록으로부터 패키지 문서를 계산하고, 예제들을 적절한 패키지 요소들과 연결합니다.
새로운 정보는 [`Package`](/pkg/go/doc/#Package), [`Type`](/pkg/go/doc/#Type), [`Func`](/pkg/go/doc/#Func) 타입의 새로운 `Examples` 필드와, [`Example`](/pkg/go/doc/#Example) 타입의 새로운 [`Suffix`](/pkg/go/doc/#Example.Suffix) 필드에서 확인할 수 있습니다.

<!-- go/doc -->

#### [io/ioutil](/pkg/io/ioutil/)

<!-- CL 198488 -->
[`TempDir`](/pkg/io/ioutil/#TempDir)는 이제 이름에 예측 가능한 접두사와 접미사가 포함된 디렉터리를 생성할 수 있습니다.
[`TempFile`](/pkg/io/ioutil/#TempFile)와 마찬가지로, 패턴에 '\*'가 포함되어 있으면 랜덤 문자열이 마지막 '\*'를 대체합니다.

#### [log](/pkg/log/)

<!-- CL 186182 -->
새로운 [`Lmsgprefix`](https://tip.golang.org/pkg/log/#pkg-constants)
플래그를 사용하여 로깅 함수가 선택적 출력 접두사(prefix)를 줄 시작 부분이 아니라 로그 메시지 바로 앞에 출력하도록 설정할 수 있습니다.

<!-- log -->

#### [math](/pkg/math/)

<!-- CL 127458 -->
새로운 [`FMA`](/pkg/math/#FMA) 함수는
`x*y` 계산의 중간 반올림 없이 부동 소수점으로 `x*y+z`를
계산합니다. 여러 아키텍처는 성능 향상을 위해 전용 하드웨어 명령어를 사용하여 이 계산을 구현합니다.

<!-- math -->

#### [math/big](/pkg/math/big/)

<!-- CL 164972 -->
이제 [`GCD`](/pkg/math/big/#Int.GCD) 메서드에서 입력값 `a`와 `b`가 0이거나 음수일 수 있습니다.

<!-- math/big -->

#### [math/bits](/pkg/math/bits/)

<!-- CL 197838 -->
새로운 함수인 [`Rem`](/pkg/math/bits/#Rem), [`Rem32`](/pkg/math/bits/#Rem32), 및 [`Rem64`](/pkg/math/bits/#Rem64)는 몫이 오버플로우되는 경우에도 나머지를 계산하는 기능을 지원합니다.

<!-- math/bits -->

#### [mime](/pkg/mime/)

<!-- CL 186927 -->
`.js` 및 `.mjs` 파일의 기본 타입이
`application/javascript`에서 `text/javascript`로
변경되었습니다.
이는 `application/javascript`를 더 이상 사용하지 않는 것으로 간주하는 [IETF 드래프트](https://datatracker.ietf.org/doc/draft-ietf-dispatch-javascript-mjs/)를 따른 것입니다.

제공해주신 내용이 없거나 비어 있습니다. 번역할 Markdown 콘텐츠를 입력해 주세요. 정성껏 기술 번역을 도와드리겠습니다.

#### [mime/multipart](/pkg/mime/multipart/)

새로운 [`Reader`](/pkg/mime/multipart/#Reader)
메서드 [`NextRawPart`](/pkg/mime/multipart/#Reader.NextRawPart)는 `quoted-printable` 데이터를 투명하게 디코딩하지 않고 다음 MIME 파트를 가져오는 기능을 지원합니다.

제공해주신 내용이 비어 있거나 MIME 타입 표시(`<!-- mime/multipart -->`)만 포함되어 있습니다. 번역할 구체적인 기술 문서 내용을 제공해 주시면, 요청하신 지침에 따라 정밀하게 한국어로 번역해 드리겠습니다.

#### [net/http](/pkg/net/http/)

<!-- CL 200760 -->
새로운 [`Header`](/pkg/net/http/#Header)
메서드인 [`Values`](/pkg/net/http/#Header.Values)는
정규화된 키(canonicalized key)와 연결된 모든 값을 가져오는 데 사용될 수 있습니다.

<!-- CL 61291 -->
새로운 [`Transport`](/pkg/net/http/#Transport) 필드인 [`DialTLSContext`](/pkg/net/http/#Transport.DialTLSContext)는 프록시를 거치지 않는 HTTPS 요청에 대해 TLS 연결을 생성하는 선택적 dial 함수를 지정하는 데 사용될 수 있습니다. 이 새로운 필드는 이제 deprecated로 간주되는 [`DialTLS`](/pkg/net/http/#Transport.DialTLS) 대신 사용할 수 있습니다. `DialTLS`는 계속 작동하겠지만, 새로운 코드에서는 `DialTLSContext`를 사용해야 합니다. `DialTLSContext`를 사용하면 transport가 더 이상 필요하지 않은 즉시 dial을 취소할 수 있습니다.

<!-- CL 192518, CL 194218 -->
Windows에서 [`ServeFile`](/pkg/net/http/#ServeFile)이 이제 2GB보다 큰 파일을 올바르게 제공합니다.

<!-- net/http -->

#### [net/http/httptest](/pkg/net/http/httptest/)

<!-- CL 201557 -->
새로운 [`Server`](/pkg/net/http/httptest/#Server)
필드 [`EnableHTTP2`](/pkg/net/http/httptest/#Server.EnableHTTP2)는
테스트 서버에서 HTTP/2를 활성화하는 기능을 지원합니다.

<!-- net/http/httptest -->

#### [net/textproto](/pkg/net/textproto/)

<!-- CL 200760 -->
새로운 [`MIMEHeader`](/pkg/net/textproto/#MIMEHeader) 메서드인 [`Values`](/pkg/net/textproto/#MIMEHeader.Values)를 사용하여 정규화된 키와 관련된 모든 값을 가져올 수 있습니다.

<!-- net/textproto -->

#### [net/url](/pkg/net/url/)

<!-- CL 185117 -->
URL 파싱에 실패한 경우
(예를 들어 [`Parse`](/pkg/net/url/#Parse) 또는 [`ParseRequestURI`](/pkg/net/url/#ParseRequestURI) 사용 시),
결과로 반환되는 [`Error`](/pkg/net/url/#Error.Error) 메시지가
이제 파싱할 수 없는 URL을 따옴표로 감싸서 표시합니다.
이를 통해 더 명확한 구조를 제공하며 다른 파싱 오류와의 일관성을 유지합니다.

<!-- net/url -->

#### [os/signal](/pkg/os/signal/)

<!-- CL 187739 -->
Windows에서,
`CTRL_CLOSE_EVENT`, `CTRL_LOGOFF_EVENT`,
및 `CTRL_SHUTDOWN_EVENT` 이벤트가 이제
`syscall.SIGTERM` 신호를 생성합니다. 이는 Control-C와
Control-Break가 `syscall.SIGINT` 신호를 생성하는 방식과 유사합니다.

<!-- os/signal -->

#### [plugin](/pkg/plugin/)

<!-- CL 191617 -->
`plugin` 패키지가 이제 `freebsd/amd64`를 지원합니다.

<!-- 플러그인 -->

#### [reflect](/pkg/reflect/)

<!-- CL 85661 -->
이제 [`StructOf`](/pkg/reflect#StructOf)에서 `StructField` 요소의 `PkgPath` 필드를 설정하여, 비공개(unexported) 필드를 가진 구조체 타입을 생성하는 것을 지원합니다.

<!-- reflect -->

#### [runtime](/pkg/runtime/)

<!-- CL 200081 -->
`runtime.Goexit`를 재귀적인 `panic`/`recover`를 통해 중단시키는 것이 더 이상 불가능합니다.

<!-- CL 188297, CL 191785 -->
macOS에서 `SIGPIPE`는 더 이상 Go 런타임이 초기화되기 전에 설치된 시그널 핸들러로 전달되지 않습니다.
이는 macOS가 `SIGPIPE`를 닫힌 파이프에 쓰고 있는 스레드가 아니라 [메인 스레드로](/issue/33384) 전달하기 때문에 필요한 조치입니다.

<!-- runtime -->

#### [runtime/pprof](/pkg/runtime/pprof/)

<!-- CL 204636, 205097 -->
생성된 프로파일에 인라인 마크(inline marks)를 위해 사용되던 pseudo-PC가 더 이상 포함되지 않습니다. 인라인된 함수의 심볼 정보는 pprof 도구가 기대하는 [형식](https://github.com/google/pprof/blob/5e96527/proto/profile.proto#L177-L184)으로 인코딩됩니다. 이는 최근 릴리스 중에 발생한 회귀(regression) 문제를 해결하기 위한 수정 사항입니다.

<!-- runtime/pprof -->

#### [strconv](/pkg/strconv/)

[`NumError`](/pkg/strconv/#NumError) 타입에 이제 변환 실패 원인을 검색하는 데 사용할 수 있는 [`Unwrap`](/pkg/strconv/#NumError.Unwrap) 메서드가 추가되었습니다.
이를 통해 `NumError` 값을 [`errors.Is`](/pkg/errors/#Is)와 함께 사용하여 기본 오류가 [`strconv.ErrRange`](/pkg/strconv/#pkg-variables)인지 또는 [`strconv.ErrSyntax`](/pkg/strconv/#pkg-variables)인지 확인할 수 있습니다.

<!-- strconv -->

#### [sync](/pkg/sync/)

<!-- CL 200577 -->
경합이 심한 `Mutex`의 잠금을 해제하면 이제 해당 `Mutex`를 기다리는 다음 goroutine에 CPU 제어권을 직접 양도합니다. 이는 CPU 코어 수가 많은 머신에서 경합이 심한 mutex의 성능을 크게 향상시킵니다.

<!-- sync -->

#### [testing](/pkg/testing/)

<!-- CL 201359 -->
이제 `testing` 패키지는 테스트 또는 벤치마크가 종료된 후 호출되는 정리(cleanup) 함수를 지원합니다. 각각 [`T.Cleanup`](/pkg/testing#T.Cleanup) 또는 [`B.Cleanup`](/pkg/testing#B.Cleanup)을 호출하여 사용할 수 있습니다.

<!-- testing -->

#### [text/template](/pkg/text/template/)

<!-- CL 206124 -->
이제 `text/template` 패키지는 괄호로 묶인 인수가 함수로 사용될 때 오류를 정확하게 보고합니다.
이 현상은 `{{if (eq .F "a") or (eq .F "b")}}`와 같은 잘못된 사례에서 가장 흔히 발생합니다.
이 코드는 `{{if or (eq .F "a") (eq .F "b")}}`와 같이 작성해야 합니다.
잘못 작성된 사례는 기대한 대로 작동한 적이 없으며, 이제 `can't give argument to non-function` 오류와 함께 보고됩니다.

<!-- CL 207637 -->
[`JSEscape`](/pkg/text/template/#JSEscape)가 이제 `&` 및 `=` 문자를 이스케이프 처리하여, 출력값이 HTML 컨텍스트에서 잘못 사용되었을 때의 영향을 완화합니다.

<!-- text/template -->

#### [unicode](/pkg/unicode/)

[`unicode`](/pkg/unicode/) 패키지와 시스템 전반의 관련 지원 사항이 Unicode 11.0에서 [Unicode 12.0](https://www.unicode.org/versions/Unicode12.0.0/)으로 업그레이드되었습니다. 이번 업데이트를 통해 4개의 새로운 스크립트를 포함한 554개의 새로운 문자와 61개의 새로운 이모지가 추가되었습니다.

<!-- unicode -->
