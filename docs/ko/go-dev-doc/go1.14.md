<!--
참고: 이 문서 및 이 디렉토리에 있는 다른 문서에서, 고정 폭 문자열을 비고정 폭 공백으로 설정하는 것이 관례입니다 (예: `hello world`).
이러한 문자열에서 내부 태그를 제거하는 CL을 보내지 마세요.
-->

```
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.14 소개 {#introduction}

가장 최신 Go 버전인 1.14은 [Go 1.13](go1.13) 이후 6개월 후에 출시되었습니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
항상 그렇듯이, 이 릴리스는 Go 1의 [호환성 보장](/doc/go1compat.html)을 유지합니다.
대부분의 Go 프로그램이 기존과 동일하게 컴파일 및 실행될 것으로 예상합니다.

`go` 명령의 모듈 지원은 이제 프로덕션 환경에서 사용이 가능하며, 모든 사용자가 의존성 관리를 위해 Go 모듈로 마이그레이션하도록 권장합니다. [Go 모듈로 마이그레이션하기](/blog/migrating-to-go-modules)를 참조하십시오. Go 툴체인에 문제가 있어 마이그레이션이 불가능한 경우, 해당 문제를 [열린 이슈](/issue?q=is%3Aissue+is%3Aopen+label%3Amodules)로 등록하십시오. (만약 이슈가 `Go1.15` 마일스톤에 포함되어 있지 않다면, 왜 마이그레이션이 불가능한지 알려주시면 우선순위를 적절하게 조정할 수 있습니다.)

## 언어 변경 사항 {#language}

[겹치는 인터페이스 제안](https://github.com/golang/proposal/blob/master/design/6977-overlapping-interfaces.md)에 따라,
Go 1.14는 겹치는 메서드 세트를 가진 인터페이스의 포함을 허용합니다:
포함된 인터페이스에서 가져온 메서드는 기존 인터페이스에 존재하는 메서드와 동일한 이름과 서명을 가질 수 있습니다. 이는 일반적으로 (그러나 반드시 그렇지 않은) 다이아몬드 형태의 포함 그래프에서 발생하는 문제를 해결합니다.
인터페이스에 명시적으로 선언된 메서드는 [고유](https://tip.golang.org/ref/spec#Uniqueness_of_identifiers)해야 합니다.

## 포트

### 다윈

```
# 다윈
```

Go 1.14은 macOS 10.11 El Capitan에서만 실행 가능한 마지막 버전입니다.
Go 1.15은 macOS 10.12 Sierra 또는 이후 버전에서 필요합니다.

<!-- golang.org/issue/34749 -->
Go 1.14은 macOS (darwin/386 포트)에서 32비트 바이너리를 지원하는 마지막 Go 릴리스입니다. macOS 10.15 (Catalina)부터 더 이상 지원되지 않습니다.
Go는 64비트 darwin/amd64 포트를 계속 지원합니다.

<!-- golang.org/issue/34751 -->
Go 1.14은 iOS, iPadOS, watchOS, tvOS ( `darwin/arm` 포트)에서 32비트 바이너리를 지원하는 마지막 Go 릴리스일 가능성이 높습니다. Go는 64비트 `darwin/arm64` 포트를 계속 지원합니다.

### Windows

<!-- CL 203601 -->
Windows에서 실행되는 Go 바이너리에 대해 [DEP
(데이터 실행 방지)](https://docs.microsoft.com/en-us/windows/win32/memory/data-execution-prevention)가 활성화되었습니다.

<!-- CL 202439 -->
Windows에서 `[`os.OpenFile`](/pkg/os#CreateFile)를 사용하여 파일
을 생성하거나, `[`os.O_CREATE`](/pkg/os/#O_CREATE) 플래그와
`[`syscall.Open`](/pkg/syscall#Open)를 사용하여
`[`syscall.O_CREAT`](/pkg/syscall#O_CREAT) 플래그와 함께
파일을 생성하면, 파일 권한에 `0o200` (소유자 쓰기 권한) 비트가 설정되지 않은
경우 파일이 기본적으로 읽기 전용으로 생성됩니다. 이로 인해 Windows에서의 동작 방식이 Unix 시스템과 유사해집니다.

### WebAssembly {#wasm}

웹 어셈블리 (WebAssembly)는 웹 브라우저에서 실행할 수 있는 바이너리 명령어 형식입니다. JavaScript보다 더 빠르고 효율적으로 코드를 실행할 수 있도록 설계되었습니다.

**특징:**

*   **성능:** JavaScript보다 훨씬 빠릅니다.
*   **이식성:** 다양한 플랫폼에서 실행 가능합니다.
*   **보안:** 웹 브라우저 환경에서 안전하게 실행됩니다.
*   **타입스크립트 지원:** 타입스크립트 코드를 WebAssembly로 컴파일할 수 있습니다.

**장점:**

*   고성능 애플리케이션 개발에 적합합니다.
*   복잡한 계산 및 그래픽 작업에 유용합니다.
*   기존 JavaScript 코드를 WebAssembly로 포팅하기 용이합니다.

**단점:**

*   아직 초기 단계의 기술입니다.
*   JavaScript 생태계와의 통합이 완벽하지 않습니다.

**예시 (JavaScript):**

```javascript
function add(a, b) {
  return a + b;
}
```

**예시 (WebAssembly):**

```
// (WebAssembly code - no translation needed)
```

<!-- CL 203600 -->
`js.Value`를 통해 Go에서 참조되는 JavaScript 값은 이제 가비지 컬렉션될 수 있습니다.

<!-- CL 203600 -->
`js.Value` 값은 이제 `==` 연산자를 사용하여 비교할 수 없으며, 대신 `Equal` 메서드를 사용하여 비교해야 합니다.

<!-- CL 203600 -->
`js.Value`에 이제
`IsUndefined`, `IsNull`,
그리고 `IsNaN` 메서드가 추가되었습니다.

### RISC-V {#riscv}

<!-- Issue 27532 -->
Go 1.14은 Linux에서 64비트 RISC-V에 대한 실험적인 지원을 포함합니다. (`GOOS=linux`, `GOARCH=riscv64`) 성능, 어셈블리 구문 안정성, 그리고 잠재적으로 정확성은 여전히 개발 중입니다.

### FreeBSD {#freebsd}

<!-- CL 199919 -->
Go는 이제 FreeBSD 12.0 이상 (또는 `freebsd/arm64` 포트)에서 64비트 ARM 아키텍처를 지원합니다.

### 네이티브 클라이언트 (NaCl) {#nacl}

<!-- golang.org/issue/30439 -->
[공지](go1.13#ports)된 바와 같이, Go 1.14에서는 Native Client 플랫폼(`GOOS=nacl`) 지원이 중단됩니다.

### Illumos {#illumos}

<!-- CL 203758 -->
실행 시간은 이제 `zone.cpu-cap` 리소스 제어를 사용하여 `runtime.NumCPU` 및 기본값인 `GOMAXPROCS`에 대한 CPU 제한을 준수합니다.

## 도구 {#tools}

### Go 명령어 {#go-command}

#### 의존성 파일 관리 {#vendor}

이 섹션에서는 프로젝트의 의존성을 관리하는 방법에 대해 설명합니다.

<!-- golang.org/issue/33848 -->

`main` 모듈에 상위 레벨의 `vendor` 디렉터리가 포함되어 있고
`go.mod` 파일이 `go` `1.14` 또는
더 높은 버전을 지정하는 경우, `go` 명령어는 해당 플래그를 허용하는 작업에 대해
기본적으로 `-mod=vendor`를 사용합니다.
하지만 해당 플래그에 새로운 값을 `-mod=mod`로 설정하면, `go` 명령어는 모듈 캐시에서 모듈을 로드합니다 (즉, `vendor` 디렉터리가
존재하지 않는 경우와 동일).

`-mod=vendor`이 설정(명시적으로 또는 기본 설정)되면,
`go` 명령은 메인 모듈의
`vendor/modules.txt` 파일이
`go.mod` 파일과 일치하는지 확인합니다.

`go list -m`는 더 이상 `vendor` 디렉터리에 패키지를 제공하지 않는 트랜지티브 의존성을 무시하지 않습니다. 대신, `-mod=vendor`가 설정되었을 때와 `vendor/modules.txt`에 언급되지 않은 모듈에 대한 정보가 요청되었을 때 명시적으로 오류를 발생시킵니다.

#### 플래그 {#go-flags}

<!-- golang.org/issue/32502, golang.org/issue/30345 -->
`go get` 명령은 이제 `-mod` 플래그를 더 이상 지원하지 않습니다. 이전에는 플래그를 설정하면
[무시되거나](/issue/30345)
[빌드 실패를 일으켰습니다](/issue/32502).

<!-- golang.org/issue/33326 -->
`-mod=readonly` 설정이 기본적으로 적용됩니다. `go.mod` 파일이 읽기 전용으로 설정되었고, 상위 레벨의 `vendor` 디렉터리가 존재하지 않을 때.

<!-- golang.org/issue/31481 -->
`-modcacherw`는 `go` 명령에 새로운 디렉토리를 모듈 캐시에 기본 권한으로 유지하도록 지시하는 새로운 플래그입니다.
이 플래그를 사용하면 테스트 또는 기타 도구가 모듈의 검증된 체크섬에 포함되지 않은 파일을 실수로 추가할 가능성이 높아집니다.
그러나 `rm -rf` (go clean -modcache 대신)를 사용하여 모듈 캐시를 삭제할 수 있습니다.

<!-- golang.org/issue/34506 -->
`-modfile=file`는 `go` 명령에 모듈의 대신의 `go.mod` 파일을 읽고 (그리고 잠재적으로 쓰도록) 지시하는 새로운 플래그입니다. 모듈의 루트 디렉토리를 결정하려면 `go.mod`라는 이름의 파일이 여전히 존재해야 하지만, 이 파일은 액세스되지 않습니다. `-modfile`이 지정되면, 대신의 `go.sum` 파일도 사용됩니다. 이 파일의 경로는 `-modfile` 플래그에서 `.mod` 확장자를 제거하고 `.sum`을 추가하여 파생됩니다.

#### 환경 변수 {#go-env-vars}

<!-- golang.org/issue/32966 -->
`GOINSECURE`는 `go` 명령이 특정 모듈을 직접 원본에서 가져올 때 HTTPS 연결을 필수로 요구하거나, 인증서 검증을 건너뛰도록 지시하는 새로운 환경 변수입니다. 기존의 `GOPRIVATE` 변수와 마찬가지로, `GOINSECURE`의 값은 쉼표로 구분된 패턴 목록입니다.

#### 모듈 외부 명령어 {#commands-outside-modules}

<!-- golang.org/issue/32027 -->
모듈 인식 모드가 명시적으로 활성화되면 (`GO111MODULE=on`로 설정), `go.mod` 파일이 없는 경우 대부분의 모듈 명령은 제한된 기능을 갖습니다. 예를 들어, `go build`, `go run` 및 기타 빌드 명령은 표준 라이브러리 및 명령줄에서 `.go` 파일로 지정된 패키지만 빌드할 수 있습니다.

이전에는 `go` 명령어가 각 패키지 경로를 최신 모듈 버전으로 해결했지만, 모듈 경로 또는 버전을 기록하지 않았습니다. 이로 인해 [느리고 재현 불가능한 빌드](/issue/32027)가 발생했습니다.

`go get`는 이전과 동일하게 작동하며,
`go mod download` 및
`go list -m` (명시적 버전과 함께)도 동일하게 작동합니다.

#### `+호환되지 않는` 버전 {#호환되지-않는-버전}

<!-- golang.org/issue/34165 -->

만약 모듈의 최신 버전이 `go.mod` 파일을 포함하고 있다면,
`go get`는 해당 모듈의
[호환되지 않는](/cmd/go/#hdr-Module_compatibility_and_semantic_versioning)
메이저 버전을 더 이상 업그레이드하지 않으며, 그러한 버전이 명시적으로 요청되거나 이미 필요로 하는 경우에만 업그레이드합니다.
`go list`는 직접 버전 제어에서 가져올 때, 호환되지 않는 메이저 버전을 해당 모듈에 대해 제외하지만, 프록시에서 보고되는 경우 포함할 수 있습니다.

#### `go.mod` 파일 유지 관리 {#go.mod}

<!-- golang.org/issue/34822 -->

`go` 명령어 (모든 명령어, `go mod tidy` 제외)는 더 이상
`require` 지시어를 사용하여 간접 의존성의 버전을 명시적으로 제거하지 않습니다.
이는 이미 메인 모듈의 다른 (전이적) 의존성에 의해 암시되는 버전입니다.

`go` 명령어 (단, `go mod tidy`는 제외)
만약 변경 사항이 단순 미적인 경우에만
`go.mod` 파일을 편집하세요.

`-mod=readonly`이 설정되면, `go` 명령어가 누락된 `go` 지시문이나 잘못된 `// indirect` 주석 때문에 실패하는 것을 더 이상 경험하지 않아도 됩니다.

#### 모듈 다운로드 {#module-downloading}

<!-- golang.org/issue/26092 -->
`go` 명령은 이제 모듈 모드에서 Subversion 저장소를 지원합니다.

<!-- golang.org/issue/30748 -->
`go` 명령은 이제 모듈 프록시 및 기타 HTTP 서버에서 제공하는 일반 텍스트 형식의 오류 메시지 스니펫을 포함합니다.
오류 메시지는 유효한 UTF-8 형식이며, 그래픽 문자 및 공백만으로 구성되어야 표시됩니다.

#### 테스트 {#go-test}

<!-- golang.org/issue/24929 -->
`go test -v`는 이제 테스트가 모두 완료된 후가 아니라, 테스트가 진행되는 동안 `t.Log`의 출력을 스트리밍합니다.

## 실행 시간 {#runtime}

<!-- CL 190098 -->
이 릴리스는 `defer`의 대부분의 사용 사례의 성능을 개선하여, 직접 호출하는 것과 거의 동일한 오버헤드를 발생시킵니다.
그 결과, `defer`는 이제 오버헤드에 대한 우려 없이 성능에 민감한 코드에서 사용할 수 있습니다.

<!-- CL 201760, CL 201762 및 기타 -->
goroutine은 이제 비동기적으로 중단 가능합니다.
따라서 함수 호출이 없는 루프는 더 이상 스케줄러를 차단하거나 가비지 컬렉션을 크게 지연시키지 않습니다.
이는 `windows/arm`, `darwin/arm`, `js/wasm` 및 `plan9/*`를 제외한 모든 플랫폼에서 지원됩니다.

프리엠션을 구현하는 결과는 다음과 같습니다. Unix 시스템, 특히 Linux 및 macOS 시스템에서 Go 1.14로 구축된 프로그램은 이전 버전의 프로그램보다 더 많은 신호를 받게 됩니다.
이는 `[`syscall`](/pkg/syscall/) 또는 `[golang.org/x/sys/unix](https://godoc.org/golang.org/x/sys/unix)`와 같은 패키지를 사용하는 프로그램이 `EINTR` 오류로 인해 더 많은 느린 시스템 호출이 실패하는 것을 의미합니다.
이러한 프로그램은 이러한 오류를 처리해야 하며, 가장 가능성이 높은 방법은 시스템 호출을 다시 시도하는 루프를 사용하는 것입니다. 이 주제에 대한 자세한 내용은 Linux 시스템의 경우 [`man 7 signal](https://man7.org/linux/man-pages/man7/signal.7.html) 또는 다른 시스템의 유사한 문서를 참조하십시오.

<!-- CL 201765, CL 195701 및 기타 -->
페이지 할당기는 `GOMAXPROCS` 값이 높을 때 더 효율적이며 잠금 경쟁이 훨씬 적습니다.
이는 특히 대규모 할당이 병렬로, 그리고 높은 속도로 이루어질 때 낮은 지연 시간과 높은 처리량을 의미합니다.

<!-- CL 171844 및 기타 -->
`time.After`, `time.Tick`, `net.Conn.SetDeadline` 및 기타 관련 내부 타이머는 효율성이 향상되었으며, 잠금 경쟁 및 컨텍스트 전환 수가 줄었습니다.
이는 사용자에게 눈에 띄는 변경을 일으키지 않는 성능 개선입니다.

## 컴파일러

<!-- CL 162237 -->
이 릴리스는 컴파일 시에 `checkptr` 옵션을 추가하여 Go 코드에서 `unsafe.Pointer` 안전 규칙을 동적으로 검사하는 데 사용될 수 있도록 합니다.
이 옵션은 기본적으로 활성화됩니다 (Windows를 제외하고). `-race` 또는 `-msan` 플래그를 사용하여 활성화할 수 있으며, 다음과 같이 비활성화할 수도 있습니다: `-gcflags=all=-d=checkptr=0`.
특히, `-d=checkptr`는 다음 사항을 확인합니다:

1. `unsafe.Pointer`를 `*T`로 변환할 때,
    결과 포인터는 `T`에 적절하게 정렬되어야 합니다.
 2. 포인터 연산의 결과가 Go 힙 객체를 가리키는 경우,
    하나의 `unsafe.Pointer` 유형의 피연산자는 동일한 객체를 가리켜야 합니다.

`-d=checkptr` 옵션을 Windows에서 사용하는 것은 현재 권장되지 않습니다. 이는 표준 라이브러리에 잘못된 경고를 발생시킵니다.

<!-- CL 204338 -->
컴파일러는 이제 `-json` 플래그를 사용하여 핵심 최적화에 대한 기계 판독 가능한 로그를 생성할 수 있습니다. 여기에는 인라이닝, 에스케이프 분석, 경계 검사 제거, nil 검사 제거 등이 포함됩니다.

<!-- CL 196959 -->
자세한 탈출 분석 진단 (`-m=2`)이 다시 작동합니다.
이 기능은 이전 릴리스의 새로운 탈출 분석 구현에서 제거되었습니다.

<!-- CL 196217 -->
macOS 바이너리에 있는 모든 Go 심볼은 이제 밑줄로 시작하며, 이는 플랫폼 규약을 따릅니다.

<!-- CL 202117 -->
이 릴리스에는 퍼징을 위한 컴파일러 삽입 커버리지 측정 지원이 포함되어 있습니다 (실험적).
자세한 내용은 [이슈 14565](/issue/14565)를 참조하세요.
이 API는 향후 릴리스에서 변경될 수 있습니다.

<!-- CL 174704 -->
<!-- CL 196784 -->
경계 검사 제거 기능은 슬라이스 생성 시 정보를 활용하여
`int`보다 작은 타입의 인덱스에 대한 검사를 제거할 수 있습니다.

## 표준 라이브러리 {#library}

### 새로운 바이트 시퀀스 해싱 패키지 {#hash_maphash}

<!-- golang.org/issue/28322, CL 186877 -->
Go 1.14에는 `hash/maphash` 패키지가 포함되어 있으며,
이는 바이트 시퀀스에 대한 해시 함수를 제공합니다.
이러한 해시 함수는 해시 테이블 또는
임의의 문자열 또는 바이트 시퀀스를 64비트 부호 없는 정수에서 균일한 분포로 매핑해야 하는
다른 데이터 구조를 구현하는 데 사용하도록 설계되었습니다.

해시 함수는 충돌에 강하지만, 암호학적으로 안전하지 않습니다.

주어진 바이트 시퀀스의 해시 값은 단일 프로세스 내에서는 일관되지만, 다른 프로세스에서는 다릅니다.

### 라이브러리의 미세 조정 {#미세_조정}

항상 그렇듯이, 라이브러리에 다양한 작은 변경 사항 및 업데이트가 있으며, 이는 Go 1의 [호환성](https://doc/go1compat)을 염두에 두고 개발되었습니다.

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 191976 -->
SSL 버전 3.0 (SSLv3) 지원이 제거되었습니다. SSLv3는 TLS보다 이전의
[암호학적으로 취약한](https://tools.ietf.org/html/rfc7568)
프로토콜임을 참고하십시오.

<!-- CL 191999 -->
TLS 1.3는 이제 `GODEBUG` 환경 변수를 통해 비활성화할 수 없습니다.
`Config.MaxVersion` 필드를 사용하여 TLS 버전을 구성하십시오.

<!-- CL 205059 -->
여러 인증서 체인이 `Config.Certificates` 필드를 통해 제공될 때, 이제 호스트와 호환되는 첫 번째 체인이 자동으로 선택됩니다. 예를 들어 ECDSA 및 RSA 인증서를 제공하고, 패키지가 자동으로 가장 적합한 체인을 선택하도록 할 수 있습니다.
하지만 이 선택의 성능은 `Certificate.Leaf` 필드가 설정되지 않으면 좋지 않습니다.
`Config.NameToCertificate` 필드는 단일 인증서를 특정 이름과 연결하는 데만 사용되므로 이제 사용되지 않아야 하며 `nil`로 설정해야 합니다.
마찬가지로 `Config.BuildNameToCertificate` 메서드는 `NameToCertificate` 필드를 잎 인증서에서 빌드하는 데 사용되므로 이제 사용되지 않아야 하며 호출해서는 안 됩니다.

<!-- CL 175517 -->
새로운 `CipherSuites`[/pkg/crypto/tls/#CipherSuites]
및 `InsecureCipherSuites`[/pkg/crypto/tls/#InsecureCipherSuites]
함수는 현재 구현된 암호화 모드 목록을 반환합니다.
새로운 `CipherSuiteName`[/pkg/crypto/tls/#CipherSuiteName]
함수는 암호화 모드 ID에 대한 이름을 반환합니다.

<!-- CL 205058, 205057 -->
새로운 [
`(*ClientHelloInfo).SupportsCertificate`](/pkg/crypto/tls/#ClientHelloInfo.SupportsCertificate) 및
[
`(*CertificateRequestInfo).SupportsCertificate`](/pkg/crypto/tls/#CertificateRequestInfo.SupportsCertificate)
메서드는 특정 인증서를 지원하는지 여부를 나타냅니다.

<!-- CL 174329 -->
`tls` 패키지는 더 이상 Legacy Next Protocol
네고시에이션 (NPN) 확장을 지원하지 않으며, 이제 ALPN만 지원합니다. 이전 버전에서는 둘 다 지원했습니다. API 변경 사항은 없으므로 애플리케이션은 이전과 동일하게 작동해야 합니다. 대부분의 다른 클라이언트와 서버는 표준화된 ALPN을 위해 NPN 지원을 제거했습니다.

<!-- CL 205063, 205062 -->
RSA-PSS 서명은 TLS 1.2 핸드셰이크에서 지원되는 경우 사용됩니다.
이것은 대부분의 애플리케이션에 영향을 미치지 않지만,
[`Certificate.PrivateKey`](/pkg/crypto/tls/#Certificate.PrivateKey)
구현이 RSA-PSS 서명을 지원하지 않는 경우,
[
`Certificate.SupportedSignatureAlgorithms`](/pkg/crypto/tls/#Certificate.SupportedSignatureAlgorithms)
필드를 사용하여 비활성화해야 합니다.

<!-- CL 205059, 205059 -->
[`Config.Certificates`](/pkg/crypto/tls/#Config.Certificates) 및
[`Config.GetCertificate`](/pkg/crypto/tls/#Config.GetCertificate)는 이제
[`Config.GetConfigForClient`](/pkg/crypto/tls/#Config.GetConfigForClient)가 설정된 경우 모두 `nil`일 수 있습니다. 콜백 함수가 인증서 또는 오류를 반환하지 않으면
`unrecognized_name`이 전송됩니다.

<!-- CL 205058 -->
새로운 `CertificateRequestInfo.Version` 필드는 클라이언트 인증서 콜백에 사용되는 TLS 버전을 지정합니다. ([https://pkg/crypto/tls/#CertificateRequestInfo.Version](https://pkg/crypto/tls/#CertificateRequestInfo.Version))

<!-- CL 205068 -->
새로운 `TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256` 및
`TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256` 상수는
이전의 `TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305` 및
`TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305`라는 이름으로 참조되었던 암호화 알고리즘의 최종 이름을 사용합니다.

<!-- crypto/tls -->

#### [crypto/x509](/pkg/crypto/x509/)

<!-- CL 204046 -->
[`Certificate.CreateCRL`](/pkg/crypto/x509/#Certificate.CreateCRL)
이제 Ed25519 발급자를 지원합니다.

#### [debug/dwarf](/pkg/debug/dwarf/)

<!-- CL 175138 -->
`debug/dwarf` 패키지는 이제 DWARF 버전 5를 읽도록 지원합니다.

새로운
방법 [`(*Data).AddSection`](/pkg/debug/dwarf/#Data.AddSection)는
입력 파일에서 임의의 새로운 DWARF 섹션을
DWARF `Data`에 추가하는 것을 지원합니다.

<!-- CL 192698 -->
새로운
메서드 [`(*Reader).ByteOrder`](/pkg/debug/dwarf/#Reader.ByteOrder)는 현재 컴파일 유닛의 바이트 오더를 반환합니다.
이를 통해, 원시 순서로 인코딩된 속성을 해석하는 데 사용할 수 있습니다. 예를 들어, 위치 설명과 같은 속성입니다.

<!-- CL 192699 -->
새로운
메서드 [`(*LineReader).Files`](/pkg/debug/dwarf/#LineReader.Files]
은 라인 리더로부터 파일 이름 테이블을 반환합니다.
이를 통해 `AttrDeclFile`과 같은 DWARF 속성의 값을 해석하는 데 사용할 수 있습니다.

<!-- 디버깅/다프 -->

#### [encoding/asn1](/pkg/encoding/asn1/)

<!-- CL 126624 -->
[`Unmarshal`](/pkg/encoding/asn1/#Unmarshal)
이제 ASN.1 문자열 유형인 BMPString을 지원하며, 이는 새로운
[`TagBMPString`](/pkg/encoding/asn1/#TagBMPString)
상수로 표현됩니다.

<!-- encoding/asn1 -->

#### [encoding/json](/pkg/encoding/json/)

<!-- CL 200677 -->
`Decoder` 유형이 새로운
메서드 [`InputOffset`](/pkg/encoding/json/#Decoder.InputOffset)를 지원하며, 이 메서드는 현재 디코더의 위치에 해당하는 입력 스트림 바이트 오프셋을 반환합니다.

<!-- CL 200217 -->
[`Compact`](/pkg/encoding/json/#Compact)는 더 이상
`U+2028` 및 `U+2029` 문자를 이스케이프하지 않습니다.
이는 문서화되지 않은 기능이었습니다. 적절한 이스케이핑을 위해서는 [`HTMLEscape`](/pkg/encoding/json/#HTMLEscape)를 참조하십시오.

<!-- CL 195045 -->
[`Number`](/pkg/encoding/json/#Number)는 이제
유효하지 않은 숫자를 더 이상
허용하지 않으며, 문서화된 동작을 더 잘 따릅니다.
프로그램이 빈 문자열과 같은 유효하지 않은 숫자를
받아야 하는 경우, `Unmarshaler`를 사용하여
이 유형을 래핑하는 것을 고려하십시오.

<!-- CL 200237 -->
[`Unmarshal`](/pkg/encoding/json/#Unmarshal)
이제 `encoding.TextUnmarshaler` 인터페이스를 구현하는 문자열 기반의 map 키도 지원할 수 있습니다.

<!-- encoding/json -->

#### [go/build](/pkg/go/build/)

<!-- CL 203820, 211657 -->
`[`Context`](/pkg/go/build/#Context)
형에 새로운 필드 `Dir`이 추가되었으며, 이를 사용하여 빌드 작업 디렉토리를 설정할 수 있습니다.
기본값은 현재 실행 중인 프로세스의 현재 디렉토리입니다.
모듈 모드에서는 이를 사용하여 메인 모듈을 찾습니다.

<!-- go/build -->

#### [go/doc](pkg/go/doc/)

<!-- CL 204830 -->
새로운
함수 [`NewFromFiles`](/pkg/go/doc/#NewFromFiles)는
`*ast.File` 목록에서 패키지 문서를 생성하고,
적절한 패키지 요소와 예제를 연결합니다.
새로운 정보는 다음 유형에 새 `Examples`
필드로 제공됩니다: [`Package`](/pkg/go/doc/#Package),
[`Type`](/pkg/go/doc/#Type),
[`Func`](/pkg/go/doc/#Func) 및
[`Example`](/pkg/go/doc/#Example) 유형에 새
[`Suffix`](/pkg/go/doc/#Example.Suffix)
필드.

```markdown
<!-- go/doc -->
```

#### [io/ioutil](/pkg/io/ioutil/)

<!-- CL 198488 -->
[`TempDir`](/pkg/io/ioutil/#TempDir) 이제 예측 가능한 접두사와 접미사를 가진 디렉토리를 생성할 수 있습니다.
`[TempFile`](/pkg/io/ioutil/#TempFile)와 마찬가지로, 패턴에 '\*'가 포함된 경우, 무작위 문자열이 마지막 '\*'를 대체합니다.

#### [log](/pkg/log/)

<!-- CL 186182 -->
새로운 [`Lmsgprefix`](https://tip.golang.org/pkg/log/#pkg-constants)
플래그를 사용하여 로깅 함수가 로그 메시지 앞에 선택적인 출력 프리픽스를 즉시 출력하도록 지시할 수 있습니다.

<!-- 로그 -->

#### [math](/pkg/math/)

<!-- CL 127458 -->
새로운 [`FMA`](/pkg/math/#FMA) 함수는
`x*y+z`를 부동 소수점 연산으로 계산하며, 중간에 `x*y`의
결과를 반올림하지 않습니다. 여러 아키텍처는 추가적인 성능을 위해
이 연산을 위한 전용 하드웨어 명령어를 사용합니다.

<!-- 수학 -->

#### [math/big](/pkg/math/big/)

<!-- CL 164972 -->
`[`GCD`](/pkg/math/big/#Int.GCD) 방법이
이제 입력 `a`와 `b`가 0이거나 음수 값을 가질 수 있습니다.

<!-- 수학/큰 -->

#### [math/bits](pkg/math/bits/)

<!-- CL 197838 -->
새로운 함수
[`Rem`](/pkg/math/bits/#Rem),
[`Rem32`](/pkg/math/bits/#Rem32), 및
[`Rem64`](/pkg/math/bits/#Rem64)는 몫이 오버플로우되더라도 나머지를 계산할 수 있도록 지원합니다.

<!-- 수학/비트 -->

#### [mime](/pkg/mime/)

<!-- CL 186927 -->
`.js` 및 `.mjs` 파일의 기본 MIME 타입이
`text/javascript`로 변경되었습니다.
이는 [IETF 초안](https://datatracker.ietf.org/doc/draft-ietf-dispatch-javascript-mjs/)에 따른 것으로, `application/javascript`를 더 이상 사용하지 않도록 합니다.

<!-- mime -->

#### [mime/multipart](/pkg/mime/multipart/)

새로운 [`Reader`](/pkg/mime/multipart/#Reader)
메서드 [`NextRawPart`](/pkg/mime/multipart/#Reader.NextRawPart)는
`quoted-printable` 데이터를 투명하게 디코딩하지 않고
다음 MIME 파트를 가져오는 기능을 지원합니다.

<!-- mime/multipart -->

#### [net/http](/pkg/net/http/)

<!-- CL 200760 -->
새로운 [`Header`](/pkg/net/http/#Header)
메서드 [`Values`](/pkg/net/http/#Header.Values)를 사용하여
표준화된 키와 관련된 모든 값을 가져올 수 있습니다.

<!-- CL 61291 -->
새로운 [`Transport`](/pkg/net/http/#Transport)
필드인 [`DialTLSContext`](/pkg/net/http/#Transport.DialTLSContext)를 사용하면, 프록시가 사용되지 않는 HTTPS 요청에 대한 TLS 연결을 생성하기 위한 선택적 래퍼 함수를 지정할 수 있습니다.
이 새로운 필드는 이제 устаревшим 것으로 간주되는 [`DialTLS`](/pkg/net/http/#Transport.DialTLS) 대신 사용될 수 있습니다. `DialTLS`는 계속 작동하지만, 새로운 코드는 `DialTLSContext`를 사용해야 하며, 이를 통해 트랜스포트는 더 이상 필요하지 않을 때 연결을 취소할 수 있습니다.

<!-- CL 192518, CL 194218 -->
Windows에서, [`ServeFile`](/pkg/net/http/#ServeFile)가 이제 2GB를 초과하는 파일도 정확하게
서버합니다.

<!-- net/http -->

#### [net/http/httptest](/pkg/net/http/httptest/)

<!-- CL 201557 -->
새로운 [`Server`](/pkg/net/http/httptest/#Server)
필드 [`EnableHTTP2`](/pkg/net/http/httptest/#Server.EnableHTTP2)
은 테스트 서버에서 HTTP/2를 활성화하는 기능을 지원합니다.

<!-- net/http/httptest -->

```
#### [net/textproto](pkg/net/textproto/)
```

<!-- CL 200760 -->
새로운 [`MIMEHeader`](/pkg/net/textproto/#MIMEHeader)
메서드 [`Values`](/pkg/net/textproto/#MIMEHeader.Values)를 사용하면, 표준화된 키와 관련된 모든 값을 가져올 수 있습니다.

<!-- net/textproto -->

#### [net/url](/pkg/net/url/)

<!-- CL 185117 -->
URL 파싱에 실패할 경우
(예를 들어 [`Parse`](/pkg/net/url/#Parse)
또는 [`ParseRequestURI`](/pkg/net/url/#ParseRequestURI)를 사용하여)
결과적으로 반환되는 [`Error`](/pkg/net/url/#Error.Error) 메시지는 파싱되지 못한 URL을 인용합니다.
이것은 더 명확한 구조와 다른 파싱 오류와의 일관성을 제공합니다.

<!-- net/url -->

#### [os/signal](/pkg/os/signal/)

<!-- CL 187739 -->
Windows에서,
`CTRL_CLOSE_EVENT`, `CTRL_LOGOFF_EVENT`,
그리고 `CTRL_SHUTDOWN_EVENT` 이벤트가 이제 `syscall.SIGTERM` 신호를 생성하며, 이는 Control-C 및 Control-Break가 `syscall.SIGINT` 신호를 생성하는 것과 유사합니다.

<!-- os/신호 -->

#### [플러그인](/pkg/plugin/)

<!-- CL 191617 -->
`plugin` 패키지가 이제 `freebsd/amd64`를 지원합니다.

<!-- 플러그인 -->

#### [reflect](/pkg/reflect/)

<!-- CL 85661 -->
[`StructOf`](/pkg/reflect#StructOf)가 이제
`StructField` 요소의 `PkgPath` 필드를 설정하여
내부 필드를 가진 구조 유형을 만드는 것을 지원합니다.

<!-- 반영 -->

```
#### [runtime](pkg/runtime/)
```

<!-- CL 200081 -->
`runtime.Goexit`는 이제 재귀적인 `panic`/`recover`에 의해 중단될 수 없습니다.

<!-- CL 188297, CL 191785 -->
macOS에서는 `SIGPIPE` 신호가 Go 런타임이 초기화되기 전에 설치된 신호 처리기에 더 이상 전달되지 않습니다.
이는 macOS가 `SIGPIPE` 신호를
[메인 스레드](/issue/33384)에 전달하기 때문입니다.
(즉, 파이프에 쓰기를 시도하는 스레드에 전달하는 대신).

<!-- 실행 환경 -->

#### [runtime/pprof](/pkg/runtime/pprof/)

<!-- CL 204636, 205097 -->
생성된 프로파일에는 더 이상 인라인 마크에 사용되는 가상 PC 정보가 포함되지 않습니다. 인라인된 함수의 심볼 정보는 [이 형식](https://github.com/google/pprof/blob/5e96527/proto/profile.proto#L177-L184)에 따라 `pprof` 도구에서 요구하는 방식으로 인코딩됩니다. 이는 최근 릴리스 중에 발생한 오류를 수정하는 것입니다.

<!-- runtime/pprof -->

#### [strconv](pkg/strconv/)

[`NumError`](/pkg/strconv/#NumError)
형에는
`Unwrap` 메서드가 있으며, 이를 사용하여 변환이 실패한 이유를 가져올 수 있습니다.
이를 통해 `NumError` 값을 `errors.Is` (/pkg/errors/#Is)와 함께 사용하여
기본 오류가 `strconv.ErrRange` (/pkg/strconv/#pkg-variables) 또는 `strconv.ErrSyntax` (/pkg/strconv/#pkg-variables)인지 확인할 수 있습니다.

<!-- strconv -->

#### [sync](/pkg/sync/)

<!-- CL 200577 -->
`Mutex`에 대한 높은 경쟁이 발생할 때, 이제 `Mutex`를 해제하면 CPU가 해당 `Mutex`를 기다리는 다음 goroutine에 직접 전달됩니다. 이는 특히 고성능 CPU를 사용하는 환경에서 높은 경쟁 상황에서 `Mutex`의 성능을 크게 향상시킵니다.

<!-- 동기화 -->

#### [테스팅](/pkg/testing/)

<!-- CL 201359 -->
테스팅 패키지는 이제 테스트 또는 벤치가 완료된 후 호출되는 정리 함수를 지원합니다. 이를 위해 `[T.Cleanup](pkg/testing#T.Cleanup)` 또는 `[B.Cleanup](pkg/testing#B.Cleanup)`를 각각 호출합니다.

<!-- 테스트 -->

#### [text/template](/pkg/text/template/)

<!-- CL 206124 -->
`text/template` 패키지는 이제 괄호로 묶인 인수를 함수로 사용하는 경우에 올바르게 오류를 보고합니다.
이것은 주로 다음과 같은 잘못된 경우에 나타납니다.
`{{if (eq .F "a") or (eq .F "b")}}`
이것은 `{{if or (eq .F "a") (eq .F "b")}}`로 작성해야 합니다.
이러한 잘못된 경우는 예상대로 작동하지 않았으며, 이제 "함수에 인수를 전달할 수 없습니다"라는 오류로 보고됩니다.

<!-- CL 207637 -->
`JSEscape` 기능이 이제
`&` 및 `=` 문자를 이스케이프하여, HTML 환경에서 잘못 사용될 경우의 영향을 완화합니다.

<!-- 텍스트/템플릿 -->

#### [유니코드](/pkg/unicode/)

[`unicode`](/pkg/unicode/) 패키지와 시스템 전반에 걸쳐 제공되는 지원이 Unicode 11.0에서 [Unicode 12.0](https://www.unicode.org/versions/Unicode12.0.0/)으로 업그레이드되었습니다. 이는 4개의 새로운 스크립트와 61개의 새로운 이모지를 포함하여 554개의 새로운 문자를 추가합니다.

<!-- unicode -->
