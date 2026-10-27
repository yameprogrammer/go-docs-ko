<!--
참고: 이 문서 및 이 디렉토리에 있는 다른 문서에서, 고정 폭 문구와 고정 폭이 아닌 공백을 함께 사용하는 규칙을 따릅니다. 예를 들어, `hello` `world`와 같이 사용합니다.
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.23 소개 {#introduction}

가장 최신 Go 버전인 1.23은 [Go 1.22](/doc/go1.22) 이후 6개월 만에 출시되었습니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
물론, 이 릴리스는 Go 1의 [호환성 약속](/doc/go1compat)을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일 및 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

```
go
package main

func main() {
	fmt.Println("Hello, world!")
}
```

<!-- go.dev/issue/61405, CL 557835, CL 584596 -->
"range" 절은 "for-range" 루프에서 이제 다음 유형의 반복자 함수를 허용합니다

```
func(func() bool)
    func(func(K) bool)
    func(func(K, V) bool)
```

**범위 표현식으로 사용.**
`iterator` 인수의 호출은 "for-range" 루프의 반복 값을 생성합니다.
자세한 내용은 [`iter`](/pkg/iter) 패키지 설명서, [언어 사양](/ref/spec#For_range), 및 [Range over Function Types 블로그 게시물](/blog/range-functions)를 참조하십시오.
동기화 이유는 2022년 ["range-over-func" 토론](/issue/56413)을 참조하십시오.

<!-- go.dev/issue/46477, CL 566856, CL 586955, CL 586956 -->
Go 1.23은 [일반적인 타입 별칭] 지원을 미리 제공합니다. ([/issue/46477])
`GOEXPERIMENT=aliastypeparams`를 사용하여 도구 체인을 빌드하면 패키지 내에서 이 기능을 활성화할 수 있습니다.
(패키지 경계를 넘어 일반적인 별칭 타입을 사용하는 것은 아직 지원되지 않습니다.)

## 도구 {#tools}

### Telemetry

<!-- go.dev/issue/58894, go.dev/issue/67111 -->
Go 1.23부터 Go 도구 체인은 사용 및 오류 통계를 수집할 수 있습니다. 이러한 통계는 Go 팀이 Go 도구 체인이 어떻게 사용되고, 얼마나 잘 작동하는지 이해하는 데 도움이 됩니다. 이러한 통계는 [Go 전력 측정](/doc/telemetry)이라고 합니다.

`Go` 텔레메트리는 _선택적 시스템_이며, `[`go` `telemetry` 명령]( /cmd/go/#hdr-Manage_telemetry_data_and_settings)을 통해 제어됩니다.
기본적으로, 도구 체 프로그램은 카운터 파일에 통계를 수집하며, 이 파일은 로컬에서 검사할 수 있지만, 그렇지 않은 경우 사용되지 않습니다 (`go` `telemetry` `local`).

Go가 잘 작동하고 Go 사용을 이해하는 데 도움이 되도록,
`go` `telemetry` `on` 명령을 실행하여 Go 추적 기능을 활성화하는 것을 고려해 주세요.
이 모드에서는,
익명 카운터 보고서가 매주
[telemetry.go.dev](https://telemetry.go.dev)로 업로드되며,
여기서 데이터를 그래프로 집계하고, 데이터를 분석하려는 모든 Go 기여자 또는 사용자에게 다운로드할 수 있습니다.
Go Telemetry 시스템에 대한 자세한 내용은 "[Go Telemetry](/doc/telemetry)"를 참조하세요.

### Go 명령어 {#go-command}

`GOROOT_FINAL` 환경 변수를 설정해도 더 이상 효과가 없습니다.
`go` 명령어를 `GOROOT/bin/go` 외의 위치에 설치하는 배포판은 `go` 바이너리를 이동하거나 복사하는 대신 심볼릭 링크를 설치해야 합니다.

<!-- go.dev/issue/34208, CL 563137, CL 586095 -->
새로운 `go env` `-changed` 플래그는 명령이 실제로 유효한 값이 기본값과 다릅니다. 즉, `-w` 플래그를 이전부터 사용하지 않은 빈 환경에서 얻을 수 있는 기본값과 다른 설정만 출력하도록 합니다.

<!-- go.dev/issue/27005, CL 585401 -->
새로운 `go` `mod` `tidy` `-diff` 플래그는 명령이 파일 내용을 수정하는 대신 필요한 변경 사항을 유니파이드 다프로 출력합니다. 업데이트가 필요한 경우 0이 아닌 코드로 종료됩니다.

<!-- go.dev/issue/52792, CL 562775 -->
`go list -m -json` 명령에 새로운 `Sum` 및 `GoModSum` 필드가 추가되었습니다.
이는 기존의 `go mod download -json` 명령의 동작과 유사합니다.

<!-- go.dev/issue/65573 ("cmd/go: separate default GODEBUGs from go language version") -->
`godebug` 지시어(go.mod 및 go.work에서 사용)는 사용 중인 워크 모듈 또는 워크스페이스에 적용할
[GODEBUG 설정]([/doc/godebug)을 선언합니다.

### 수의사 {#vet}

<!-- go.dev/issue/46136 -->
`go vet` 명령어에 이제 `stdversion` 분석기가 포함되어 있습니다.
[stdversion](https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/stdversion) 분석기는 현재 파일에서 참조되는 심볼 중, 해당 파일의 `go.mod` 파일에 있는 `go` 지시어 및 [`//go:build` 제약 조건](/cmd/go#hdr-Build_constraints)에 의해 결정되는 Go 버전보다 너무 새로운 심볼에 대한 참조를 감지합니다.

예를 들어, `reflect.TypeFor` 함수 (go1.22에서 도입)에 대한 참조가 있는 파일 (모듈의 `go.mod` 파일이 `go 1.21`을 지정)에 대한 진단 결과를 보고합니다.

### Cgo {#cgo}

<!-- go.dev/issue/66456 -->
[`cmd/cgo`](/pkg/cmd/cgo)는 C 링커에 플래그를 전달하기 위한 새로운 `-ldflags` 플래그를 지원합니다.
`go` 명령은 이를 자동으로 사용하며, 매우 큰 `CGO_LDFLAGS`로 인해 발생하는 "인수 목록이 너무 깁니다" 오류를 방지합니다.

### 추적 {#trace}

<!-- go.dev/issue/65316 -->
`trace` 도구가 부분적으로 손상된 트레이스를 더 잘 처리할 수 있도록 개선되었습니다. 도구는 가능한 한 트레이스 데이터를 복구하려고 시도합니다. 이 기능은 특히 프로그램 충돌 중에 수집된 트레이스를 볼 때 유용합니다. 왜냐하면 충돌 이전의 트레이스 데이터는 대부분의 경우에 [복구 가능]( /issue/65319)하기 때문입니다.

## 런타임 {#runtime}

실행 시간에 발생한 처리되지 않은 패닉 또는 기타 치명적인 오류 후 출력되는 추적은 이제 오류 메시지의 두 번째 줄부터 후속 줄을 단 탭으로 들여쓰기합니다(예: panic 함수에 전달되는 인자). 이를 통해 첫 번째 goroutine의 스택 추적과 명확하게 구별할 수 있습니다. 자세한 내용은 [#64590](/issue/64590)를 참조하십시오.

## 컴파일러

[프로파일 가이드 최적화](/doc/pgo)를 사용하여 빌드하는 데 필요한 시간 오버헤드가 크게 줄었습니다.
이전에는 큰 빌드에서 PGO를 활성화하면 빌드 시간이 100% 이상 증가하는 경우가 있었습니다.
Go 1.23에서는 오버헤드가 소수 퍼센트 수준으로 줄어듭니다.

<!-- https://go.dev/issue/62737 , https://golang.org/cl/576681,  https://golang.org/cl/577615 -->
Go 1.23의 컴파일러는 이제 함수 내의 서로 다른 영역에서 액세스되는 지역 변수의 스택 프레임 슬롯을 겹쳐 사용할 수 있습니다. 이를 통해 Go 애플리케이션의 스택 사용량을 줄일 수 있습니다.

<!-- https://go.dev/cl/577935 -->
386 및 amd64 아키텍처의 경우, 컴파일러는 PGO에서 얻은 정보를 사용하여 루프 내의 특정 핫 블록을 정렬합니다. 이를 통해 성능이 추가적으로 1~1.5% 향상되지만, 추가적인 0.1%의 텍스트 및 바이너리 크기가 발생합니다. 현재 이 기능은 386 및 amd64 아키텍처에서만 구현되었기 때문입니다. 다른 플랫폼에서는 개선 효과를 보이지 않았기 때문입니다.

핫 블록 정렬 기능을 비활성화하려면 `-gcflags=[<패키지>=]-d=alignhot=0` 명령을 사용합니다.

## 링커 {#linker}

<!-- go.dev/issue/67401, CL 585556, CL 587220, 그리고 더 많은 것 -->
링크어는 이제 표준 라이브러리(runtime 포함) 내의 내부 심볼을 참조하기 위해 `//go:linkname` 지시어를 사용하는 것을 허용하지 않습니다. 이러한 심볼이 정의에 `//go:linkname`으로 표시되지 않은 경우에도 마찬가지입니다.
또한, 링크어는 어셈블리 코드에서 이러한 심볼에 대한 참조를 허용하지 않습니다.
역사적 호환성을 위해, 대규모 오픈 소스 코드 코퍼스에 존재하는 기존의 `//go:linkname` 사용은 계속 지원됩니다.
표준 라이브러리의 내부 심볼에 대한 모든 새로운 참조는 허용되지 않습니다.

링크러 명령줄 플래그 `-checklinkname=0`를 사용하여 이 검사를 비활성화할 수 있습니다. 이는 디버깅 및 실험 목적으로 사용됩니다.

<!-- CL 473495 -->
동적으로 링크되는 ELF 바이너리를 빌드할 때 (PIE 바이너리를 포함),
새로운 `-bindnow` 플래그는 즉시 함수 바인딩을 활성화합니다.

## 표준 라이브러리 {#library}

### 타이머 변경 사항

Go 1.23에서는 [`time.Timer`](/pkg/time#Timer) 및 [`time.Ticker`](/pkg/time#Ticker)의 구현에 두 가지 주요 변경 사항을 도입합니다.

<!-- go.dev/issue/61542 -->
먼저, 더 이상 프로그램에서 참조되지 않는 `Timer` 및 `Ticker`는 `Stop` 메서드가 호출되지 않았더라도 즉시 가비지 컬렉션 대상이 됩니다.
이전 버전의 Go는 중단되지 않은 `Timer`를 실행한 후에만, 중단되지 않은 `Ticker`를 실행한 후에만 수집했습니다.

<!-- go.dev/issue/37196 -->
둘째, `Timer` 또는 `Ticker`와 관련된 타임어 채널은 이제 버퍼가 없으며, 용량은 0입니다.
이 변경의 주요 효과는 Go가 이제 `Reset` 또는 `Stop` 메서드 호출에 대해, 호출 전에 준비된 모든 값들이 호출 후에 전송되거나 수신되지 않음을 보장한다는 것입니다.
이전 버전의 Go는 1개의 요소 버퍼를 사용하는 채널을 사용했기 때문에 `Reset` 및 `Stop` 메서드를 올바르게 사용하는 것이 어려웠습니다.
이 변경의 눈에 띄는 효과는 타임어 채널의 `len` 및 `cap`이 이제 1 대신 0을 반환한다는 것입니다. 이는 타임어 채널에서 값을 수신할 시도가 성공할지 여부를 결정하기 위해 길이를 폴링하는 프로그램에 영향을 줄 수 있습니다.
이러한 코드는 비동기 수신을 사용해야 합니다.

이 새로운 동작은 메인 Go 프로그램이 `go.mod` 파일에 `go` 라인으로 Go 1.23.0 이상을 사용하는 모듈 내에 있을 때만 활성화됩니다.
Go 1.23이 이전 프로그램을 빌드할 때, 이전 동작이 계속 적용됩니다.
새로운 `GODEBUG` 설정 [`asynctimerchan=1`](/doc/godebug)는 Go 1.23.0 이상을 `go.mod` 파일에 명시한 프로그램이라도 비동기 채널 동작으로 되돌릴 수 있습니다.

### 새로운 고유 패키지

새로운 [`unique`](/pkg/unique) 패키지는 값들을 표준화하는 기능을 제공합니다 (예: "인터닝" 또는 "해시-컨싱").

새로운 `Make[T]` 함수를 사용하여 비교 가능한 유형의 모든 값은 표준화될 수 있습니다. 이 함수는 값의 표준 복사본에 대한 참조를 생성하며, 이 참조는 `Handle[T]` 형식입니다.
`Handle[T]` 두 개는 값에 사용된 값이 동일한 경우에만 동일합니다. 이를 통해 프로그램은 값 중복을 제거하고 메모리 사용량을 줄일 수 있습니다.
`Handle[T]` 값 두 개를 비교하는 것은 효율적이며, 간단한 포인터 비교로 줄어듭니다.

### 반복자

새로운 [`iter`](/pkg/iter) 패키지는 사용자 정의 반복자를 사용하기 위한 기본 정의를 제공합니다.

[`slices`](/pkg/slices) 패키지는 여러 함수를 추가하여 반복자와 함께 작동합니다:
- [All](/pkg/slices#All)는 슬라이스의 인덱스와 값에 대한 반복자를 반환합니다.
- [Values](/pkg/slices#Values)는 슬라이스의 요소에 대한 반복자를 반환합니다.
- [Backward](/pkg/slices#Backward)는 슬라이스를 역방향으로 반복하는 반복자를 반환합니다.
- [Collect](/pkg/slices#Collect)는 반복자에서 값을 새로운 슬라이스로 수집합니다.
- [AppendSeq](/pkg/slices#AppendSeq)는 기존 슬라이스에 반복자의 값을 추가합니다.
- [Sorted](/pkg/slices#Sorted)는 반복자에서 값을 새로운 슬라이스로 수집한 다음 슬라이스를 정렬합니다.
- [SortedFunc](/pkg/slices#SortedFunc)는 `Sorted`와 유사하지만 비교 함수를 사용합니다.
- [SortedStableFunc](/pkg/slices#SortedStableFunc)는 `SortFunc`와 유사하지만 안정적인 정렬 알고리즘을 사용합니다.
- [Chunk](/pkg/slices#Chunk)는 슬라이스의 최대 n개의 요소 크기의 연속적인 하위 슬라이스에 대한 반복자를 반환합니다.

[`maps`](/pkg/maps) 패키지는 반복자와 함께 작동하는 여러 함수를 추가합니다:
- [All](/pkg/maps#All)는 맵의 키-값 쌍에 대한 반복자를 반환합니다.
- [Keys](/pkg/maps#Keys)는 맵의 키에 대한 반복자를 반환합니다.
- [Values](/pkg/maps#Values)는 맵의 값에 대한 반복자를 반환합니다.
- [Insert](/pkg/maps#Insert)는 반복자의 키-값 쌍을 기존 맵에 추가합니다.
- [Collect](/pkg/maps#Collect)는 반복자의 키-값 쌍을 새로운 맵에 수집하고 이를 반환합니다.

### 새로운 구조체 패키지

새로운 [`structs`](/pkg/structs) 패키지는, 
컨테이너 구조의 유형과 같은 메모리 레이아웃과 같은 속성을 수정하는 구조 필드에 대한 유형을 제공합니다.

이 릴리스에서는 유일한 유형은
[`HostLayout`](/pkg/structs#HostLayout)
이며, 이는 해당 유형의 필드를 가진 구조체가 호스트 플랫폼의 기대에 부합하는 레이아웃을 가질 때 사용되어야 함을 나타냅니다. `HostLayout`은 호스트 API를 통해 전달되거나, 반환되거나, 액세스되는 유형에 사용해야 합니다.
이 마커가 없으면, 언어 사양에 의해 구조체의 레이아웃 순서가 보장되지 않지만, Go 1.23 버전부터 호스트와 언어 레이아웃이 일치합니다.

### 라이브러리의 미세 조정 {#미세_조정_사항}

#### [`archive/tar`](/pkg/archive/tar/)

만약 `FileInfoHeader`에 전달된 인수가 새로운 `FileInfoNames` 인터페이스를 구현한다면, 인터페이스 메서드를 사용하여 파일 헤더의 `Uname`/`Gname` 값을 설정합니다. 이를 통해 애플리케이션은 시스템에 종속적인 `Uname`/`Gname` 검색을 재정의할 수 있습니다.

#### [`crypto/tls`](/pkg/crypto/tls/)

TLS 클라이언트는 이제 암호화된 클라이언트 헬로 ([초안 사양](https://www.ietf.org/archive/id/draft-ietf-tls-esni-18.html))를 지원합니다.
이 기능을 활성화하려면, 연결하려는 호스트에 대해 `Config.EncryptedClientHelloConfigList` 필드를 인코딩된 ECHConfigList로 설정할 수 있습니다.

[`QUICConn`](/pkg/crypto/tls#QUICConn) 타입은 QUIC 구현에서 사용되며, 세션 재개 상태에 대한 새로운 이벤트를 포함하고, QUIC 레이어가 세션 티켓 및 세션 캐시 항목에 데이터를 추가하는 방법을 제공합니다.

`3DES` 암호화 세트는 `Config.CipherSuites`가 `nil`일 때 사용되는 기본 목록에서 제거되었습니다. 기본 설정을 복원하려면 `tls3des=1`을 `GODEBUG` 환경 변수에 추가할 수 있습니다.

실험적인 포스트-퀀텀 키 교환 메커니즘 X25519Kyber768Draft00은 [`Config.CurvePreferences`](/pkg/crypto/tls#Config.CurvePreferences)가 `nil`일 때 기본적으로 활성화됩니다.
기본 설정을 되돌리려면 `tlskyber=0`을 `GODEBUG` 환경 변수에 추가할 수 있습니다.
이는 잘못된 TLS 서버를 처리할 때 유용할 수 있으며, 이는 큰 레코드를 제대로 처리하지 못하여 핸드셰이크 중에 타임아웃이 발생하도록 합니다 (자세한 내용은 [TLS 포스트-퀀텀 TL;DR 실패](https://tldr.fail/) 참조).

Go 1.23은 [`X509KeyPair`](/pkg/crypto/tls#X509KeyPair) 및 [`LoadX509KeyPair`](/pkg/crypto/tls#LoadX509KeyPair)의 동작 방식을 변경하여 반환되는 [`Certificate`](/pkg/crypto/tls#Certificate)의 `Certificate.Leaf` 필드를 채우도록 했습니다.
이 새로운 동작에 대한 `x509keypairleaf` [GODEBUG 설정](/doc/godebug)이 추가되었습니다.

#### [`crypto/x509`](/pkg/crypto/x509/)

[`CreateCertificateRequest`](/pkg/crypto/x509#CreateCertificateRequest)가 이제 올바르게 RSA-PSS 서명 알고리즘을 지원합니다.

[`CreateCertificateRequest`](/pkg/crypto/x509#CreateCertificateRequest) 및 [`CreateRevocationList`](/pkg.crypto/x509#CreateRevocationList]는 생성된 서명을 서명자의 공개 키를 사용하여 검증합니다. 서명이 유효하지 않으면 오류가 반환됩니다. 이는 Go 1.16부터 [`CreateCertificate`](/pkg/crypto/x509#CreateCertificate]의 동작 방식과 동일합니다.

[`x509sha1` GODEBUG 설정](/pkg/crypto/x509#InsecureAlgorithmError)은 다음 Go 주요 릴리스 (Go 1.24)에서 제거됩니다. 이는 `crypto/x509`가 SHA-1 기반 서명 알고리즘을 사용하는 인증서에 대한 서명 검증을 더 이상 지원하지 않음을 의미합니다.

새로운 `ParseOID` 함수는 도트-인코딩된 ASN.1 객체 식별자 문자열을 파싱합니다.
`OID` 타입이 이제 `encoding.BinaryMarshaler` 인터페이스, `encoding.BinaryUnmarshaler` 인터페이스, `encoding.TextMarshaler` 인터페이스, `encoding.TextUnmarshaler` 인터페이스를 구현합니다.

```
#### [`database/sql`](/pkg/database/sql/)
```

`[driver.Valuer](pkg/driver#Valuer)` 구현에서 반환되는 오류가 이제 개선된 오류 처리를 위해 감싸여 있습니다. 이는 `DB.Query`, `DB.Exec`, 및 `DB.QueryRow`와 같은 작업 중에 사용됩니다.

#### [`debug/elf`](/pkg/debug/elf/)

`debug/elf` 패키지는 이제 `PT_OPENBSD_NOBTCFI`를 정의합니다. 이 `ProgType`은
OpenBSD 바이너리에서 Branch Tracking Control Flow Integrity (BTCFI) 적용을 비활성화하는 데 사용됩니다.

이제 `STT_RELC`, `STT_SRELC`, 그리고 `STT_GNU_IFUNC`의 심볼 유형 상수를 정의합니다.

#### [`encoding/binary`](/pkg/encoding/binary/)

새로운 `[`Encode`](/pkg/encoding/binary#Encode) 및 `[`Decode`](/pkg/encoding/binary#Decode) 함수는 `[`Read`](/pkg/encoding/binary#Read) 및 `[`Write`](/pkg/encoding/binary#Write)의 바이트 슬라이스에 해당하는 기능을 제공합니다.
`[`Append`](/pkg/encoding/binary#Append)는 여러 데이터를 동일한 바이트 슬라이스에 래핑(marshaling)할 수 있도록 합니다.

#### [`go/ast`](/pkg/go/ast/)

새로운 `[`Preorder`](/pkg/go/ast#Preorder) 함수는 구문 트리의 모든 노드를 쉽게 순회하는 이터레이터를 반환합니다.

#### [`go/types`](/pkg/go/types/)

<!-- 참조: ../../../../2-language.md -->

`[Func](pkg/go/types#Func)` 타입, 이는 함수 또는 메서드의 심볼을 나타내며, 이제
`Func.Signature` 메서드가 존재하여, 함수의 타입을 반환합니다. 이 타입은 항상 `Signature` 입니다.

[`Alias`](/pkg/go/types#Alias) 타입에 이제 `Rhs` 메서드가 추가되었으며, 이 메서드는 선언의 오른쪽 피드를 반환합니다: 예를 들어, `type A = B`인 경우, A의 `Rhs`는 B입니다. ([#66559](/issue/66559))

다음 메서드 [`Alias.Origin`](/pkg/go/types#Alias.Origin), [`Alias.SetTypeParams`](/pkg/go/types#Alias.SetTypeParams), [`Alias.TypeParams`](/pkg/go/types#Alias.TypeParams),
및 [`Alias.TypeArgs`](/pkg/go/types#Alias.TypeArgs)가 추가되었습니다. 이는 제네릭 alias 타입에 필요합니다.

<!-- CL 577715, CL 579076 -->
기본적으로 `go/types`는 이제 타입 별칭에 대해 [`Alias`](/pkg/go/types#Alias) 타입 노드를 생성합니다.
이 동작은 `GODEBUG`의 `gotypesalias` 플래그를 사용하여 제어할 수 있습니다.
기본값이 Go 1.22에서 0에서 Go 1.23에서 1로 변경되었습니다.

#### [`math/rand/v2`](/pkg/math/rand/v2/)

[`Uint`](/pkg/math/rand/v2#Uint) 함수 및 [`Rand.Uint`](/pkg/math/rand/v2#Rand.Uint) 메서드가 추가되었습니다.
이들은 Go 1.22 버전에서 의도치 않게 누락되었습니다.

새로운 [`ChaCha8.Read`](/pkg/math/rand/v2#ChaCha8.Read) 메서드는 [`io.Reader`](/pkg/io#Reader) 인터페이스를 구현합니다.

#### [`net`](/pkg/net/)

새로운 유형 [`KeepAliveConfig`](/pkg/net#KeepAliveConfig)는 TCP 연결의 keep-alive 옵션을 세밀하게 조정할 수 있도록, 새로운 [`TCPConn.SetKeepAliveConfig`](/pkg/net#TCPConn.SetKeepAliveConfig) 메서드와 [`Dialer`](/pkg/net#Dialer) 및 [`ListenConfig`](/pkg/net#ListenConfig)에 대한 새로운 KeepAliveConfig 필드를 제공합니다.

[`DNSError`](/pkg/net#DNSError) 유형은 이제 타임아웃 또는 취소로 인해 발생하는 오류를 감싸고 있습니다.
예를 들어, `errors.Is(someDNSErr, context.DeadlineExceedeed)`는 이제 DNS 오류가 타임아웃으로 인해 발생했는지 여부를 보고합니다.

새로운 `GODEBUG` 설정 `netedns0=0` 은 DNS 요청에 추가되는 EDNS0 헤더를 전송하지 않도록 합니다. 이는 일부 모뎀에서 DNS 서버를 손상시킨다고 보고됩니다.

```go
#### [`net/http`](/pkg/net/http/)
```

[`Cookie`](/pkg/net/http#Cookie)는 이제 쿠키 값 둘러싸는 따옴표를 유지합니다.
새로운 `Cookie.Quoted` 필드는 `Cookie.Value`가 원래 따옴표로 묶였는지 여부를 나타냅니다.

새로운 [`Request.CookiesNamed`](/pkg/net/http#Request.CookiesNamed) 메서드는 주어진 이름과 일치하는 모든 쿠키를 가져옵니다.

새로운 [`Cookie.Partitioned`](/pkg/net/http#Cookie.Partitioned) 필드는 "Partitioned" 속성을 가진 쿠키를 식별합니다.

`ServeMux`에서 사용되는 패턴은 이제 메서드 이름 다음에 하나 이상의 공백 또는 탭을 허용합니다.
이전에는 단일 공백만 허용되었습니다.

새로운 [`ParseCookie`](/pkg/net/http#ParseCookie) 함수는 쿠키 헤더 값을 파싱하고,
그 안에 설정된 모든 쿠키를 반환합니다. 동일한 쿠키 이름이 여러 번 나타날 수 있으므로, 반환되는 `Values`에는 동일한 키에 대해 여러 값이 포함될 수 있습니다.

새로운 [`ParseSetCookie`](/pkg/net/http#ParseSetCookie) 함수는 Set-Cookie 헤더 값을 파싱하고 쿠키를 반환합니다. 문법 오류가 발생하면 오류를 반환합니다.

[`ServeContent`](/pkg/net/http#ServeContent), [`ServeFile`](/pkg/net/http#ServeFile), 및 [`ServeFileFS`](/pkg/net/http#ServeFileFS)는 오류를 반환할 때 `Cache-Control`, `Content-Encoding`, `Etag`, 및 `Last-Modified` 헤더를 제거합니다. 이러한 헤더는 일반적으로 오류가 아닌 콘텐츠에 적용되지만, 오류 메시지에는 적용되지 않습니다.

미들웨어는 `ResponseWriter`를 감싸고, 런타임에 인코딩을 적용하는 기능을 제공합니다 (예: `Content-Encoding: gzip`). 이 변경 후에는 이러한 미들웨어는 더 이상 작동하지 않습니다. 이전의 `ServeContent`, `ServeFile`, `ServeFileFS` 함수의 동작은 `GODEBUG=httpservecontentkeepheaders=1` 설정을 통해 복원할 수 있습니다.

참고: 콘텐츠 크기를 변경하는 미들웨어 (예: 압축)는 [`ServeContent`](/pkg/net/http#ServeContent)가 Range 요청을 처리할 때 제대로 작동하지 않습니다. 실시간 압축은 `Transfer-Encoding` 헤더를 사용하는 것이 `Content-Encoding` 헤더를 사용하는 것보다 적합합니다.

수신 요청의 경우, 새 [`Request.Pattern`](/pkg/net/http#Request.Pattern) 필드는 요청과 일치하는 [`ServeMux`](/pkg/net/http#ServeMux) 패턴(있는 경우)을 포함합니다. 이 필드는 `GODEBUG=httpmuxgo121=1`이 설정된 경우 설정되지 않습니다.

#### [`net/http/httptest`](/pkg/net/http/httptest/)

새로운 [`NewRequestWithContext`](/pkg/net/http/httptest#NewRequestWithContext) 메서드는 `context.Context`와 함께 들어오는 요청을 생성합니다.

```go
#### [`net/netip`](패키지)

Go 1.22 및 이전 버전에서,
[`reflect.DeepEqual`](/pkg/reflect#DeepEqual)을 사용하여 IPv4 주소를 담고 있는 `Addr`를, 해당 주소의 IPv6 형식으로 매핑된 IPv4 형태의 `Addr`와 비교하는 것은 잘못된 결과를 반환했습니다. 즉, `==` 또는 [`Addr.Compare`](/pkg/net/netip#Addr.Compare)와 비교할 때 `Addr` 값이 다를 경우에도 `true`가 반환되었습니다.
이 문제는 현재 수정되었으며, 세 가지 접근 방식 모두 동일한 결과를 보고합니다.

#### [`os`](/pkg/os/)

[`Stat`](/pkg/os#Stat) 함수는 이제 Windows에서 Unix 소켓 파일에 대해 [`ModeSocket`](/pkg/os#ModeSocket) 비트를 설정합니다. 이러한 파일은 `IO_REPARSE_TAG_AF_UNIX`로 설정된 재파싱 태그를 사용하여 식별됩니다.

Windows에서 [`Lstat`](/pkg/os#Lstat) 및 [`Stat`](/pkg/os#Stat)이 보고하는 재파싱 포인트에 대한 모드 비트가 변경되었습니다. 마운트 포인트에 더 이상 [`ModeSymlink`](/pkg/os#ModeSymlink)가 설정되지 않으며, 심링크, Unix 소켓 또는 deduplication 파일이 아닌 재파싱 포인트는 항상 [`ModeIrregular`](/pkg/os#ModeIrregular)가 설정됩니다.
이 동작은 `winsymlink` 설정에 의해 제어됩니다.
Go 1.23의 경우 기본값은 `winsymlink=1`입니다.
이전 버전의 경우 기본값은 `winsymlink=0`입니다.

[`CopyFS`](/pkg/os#CopyFS) 함수는 `io/fs.FS`를 로컬 파일 시스템으로 복사합니다.

Windows에서 [`Readlink`](/pkg/os#Readlink)은 이제 볼륨을 드라이브 문자로 정규화하려고 시도하지 않습니다. 이는 항상 가능한 것은 아니었습니다.
이 동작은 `winreadlinkvolume` 설정에 의해 제어됩니다.
Go 1.23의 경우 기본값은 `winreadlinkvolume=1`입니다.
이전 버전의 기본값은 `winreadlinkvolume=0`입니다.

<!-- go.dev/issue/62654, CL 570036, CL 570681 -->
Linux에서 pidfd 지원 (일반적으로 Linux v5.4 이상)을 사용하는 경우,
[`Process`](/pkg/os#Process) 관련 함수 및 메서드는 내부적으로 pidfd (PID 대신)를 사용하며, OS가 PID를 재사용할 때 발생할 수 있는 오타를 방지합니다. Pidfd 지원은 사용자에게 완전히 투명하며, 프로세스가 가질 수 있는 추가적인 프로세스 파일 디스크립터를 제외하고는 영향을 미치지 않습니다.

#### [`path/filepath`](/pkg/path/filepath/)

새로운 [`Localize`](/pkg/path/filepath#Localize) 함수는 슬래시로 구분된 경로를 운영 체제 경로로 안전하게 변환합니다.

On Windows, [`EvalSymlinks`](/pkg/path/filepath#EvalSymlinks)는 이제 마운트 포인트를 평가하지 않습니다.
이는 많은 불일치와 버그의 원인이었습니다.
이 동작은 `winsymlink` 설정에 의해 제어됩니다.
Go 1.23의 경우, 기본값은 `winsymlink=1`입니다.
이전 버전의 기본값은 `winsymlink=0`입니다.

On Windows, [`EvalSymlinks`](/pkg/path/filepath#EvalSymlinks)는 더 이상 볼륨을 드라이브 문자로 정규화하려고 시도하지 않습니다. 이는 항상 가능했던 것은 아니었습니다.
이 동작은 `winreadlinkvolume` 설정에 의해 제어됩니다.
Go 1.23의 경우 기본값은 `winreadlinkvolume=1`입니다.
이전 버전의 경우 기본값은 `winreadlinkvolume=0`입니다.

#### [`reflect`](/pkg/reflect/)

새로운 메서드는 [`Value`](/pkg/reflect#Value)의 동일한 이름의 메서드와 동의어로 추가되었습니다:
1. [`Type.OverflowComplex`](/pkg/reflect#Type.OverflowComplex)
2. [`Type.OverflowFloat`](/pkg/reflect#Type.OverflowFloat)
3. [`Type.OverflowInt`](/pkg/reflect#Type.OverflowInt)
4. [`Type.OverflowUint`](/pkg/reflect#Type.OverflowUint)

새로운 [`SliceAt`](/pkg/reflect#SliceAt) 함수는 [`NewAt`](/pkg/reflect#NewAt)와 유사하지만, 슬라이스에 사용됩니다.

[`Value.Pointer`](/pkg/reflect#Value.Pointer) 및 [`Value.UnsafePointer`](/pkg/reflect#Value.UnsafePointer) 메서드가 이제 `String` 종류의 값도 지원합니다.

새로운 메서드 [`Value.Seq`](/pkg/reflect#Value.Seq) 및 [`Value.Seq2`](/pkg/reflect#Value.Seq2)는 값을 `for`/`range` 루프를 사용하는 것처럼 반복하는 시퀀스를 반환합니다.
새로운 메서드 [`Type.CanSeq`](/pkg/reflect#Type.CanSeq) 및 [`Type.CanSeq2`](/pkg/reflect#Type.CanSeq2)는 각각 [`Value.Seq`](/pkg/reflect#Value.Seq) 및 [`Value.Seq2`](/pkg/reflect#Value.Seq2)를 호출할 때 패닉이 발생하는지 여부를 보고합니다.

#### [`runtime/debug`](/pkg/runtime/debug/)

[`SetCrashOutput`](/pkg/runtime/debug#SetCrashOutput) 함수는 사용자가 런타임이 작성할 수 있는 대체 파일을 지정할 수 있도록 합니다.
이를 통해 `recover`를 명시적으로 사용하는 goroutine에서 발생하는 예기치 않은 모든 충돌에 대한 자동 보고 메커니즘을 구축할 수 있습니다.

<!-- pacify TestCheckAPIFragments -->

#### [`runtime/pprof`](/pkg/runtime/pprof/)

`alloc`, `mutex`, `block`, `threadcreate` 및 `goroutine` 프로파일의 최대 스택 깊이는 32에서 128 프레임으로 변경되었습니다.

#### [`runtime/trace`](/pkg/runtime/trace/)

<!-- go.dev/issue/65319 -->
실행 시간은 프로그램이 `panic` 오류로 인해 중단될 때 명시적으로 추적 데이터를 플러시합니다. 이는 프로그램이 추적 중인 동안 중단되면 추적에 더 완전한 추적 데이터가 사용 가능하다는 의미입니다.

#### [`slices`](/pkg/slices/)

<!-- 참조: ../../3-iter.md -->

<!-- 참조: ../../3-iter.md -->

[`Repeat`](/pkg/slices#Repeat) 함수는 주어진 슬라이스를 지정된 횟수만큼 반복하여 새로운 슬라이스를 반환합니다.

#### [`sync`](/pkg/sync/)

[`Map.Clear`](/pkg/sync#Map.Clear) 메서드는 모든 항목을 삭제하여 빈 [`Map`](/pkg/sync#Map)을 생성합니다. 이는 `clear`와 유사합니다.

#### [`sync/atomic`](/pkg/sync/atomic/)

<!-- 이슈 #61395 -->
새로운 [`And`](/pkg/sync/atomic#And) 및 [`Or`](/pkg/sync/atomic#Or) 연산자는 주어진 입력을 사용하여 비트별 `AND` 또는 `OR` 연산을 수행하고, 이전 값을 반환합니다.

#### [`syscall`](/pkg/syscall/)

`syscall` 패키지는 이제 Windows에서 `[WSAENOPROTOOPT](pkg/syscall#WSAENOPROTOOPT)`를 정의합니다.

[`GetsockoptInt`](/pkg/syscall#GetsockoptInt) 함수가 이제 Windows에서 지원됩니다.

#### [`testing/fstest`](/pkg/testing/fstest/)

[`TestFS`](/pkg/testing/fstest#TestFS)는 이제 구조화된 오류를 반환하며, 이를 `Unwrap()` 메서드를 통해 언래핑할 수 있습니다. 이를 통해 `errors.Is` 또는 `errors.As`를 사용하여 오류를 검사할 수 있습니다.

#### [`text/template`](/pkg/text/template/)

템플릿은 이제 "else with" 작업을 지원하므로, 특정 사용 사례에서 템플릿 복잡성을 줄일 수 있습니다.

#### [`time`](/pkg/time/)

[`Parse`](/pkg/time#Parse) 및 [`ParseInLocation`](/pkg/time#ParseInLocation) 함수는 이제 시간대 오프셋이 유효 범위를 벗어나는 경우 오류를 반환합니다.

Windows에서, [`Timer`](/pkg/time#Timer), [`Ticker`](/pkg/time#Ticker), 그리고 goroutine을 일시 중지하는 함수, 예를 들어 [`Sleep`](/pkg/time#Sleep)의 시간 분해능이 15.6ms 대신 0.5ms로 개선되었습니다.

#### [`unicode/utf16`](/pkg/unicode/utf16/)

[`RuneLen`](/pkg/unicode/utf16#RuneLen) 함수는 룬의 UTF-16 인코딩에서 16비트 단어의 수를 반환합니다. 룬이 유효한 UTF-16 인코딩 값으로 변환될 수 없는 경우 -1을 반환합니다.

## 포트

### Darwin

<!-- go.dev/issue/64207 -->
Go 1.23을 사용하려면 macOS 11 Big Sur 또는 그 이후 버전을 설치해야 합니다. 이전 버전 지원은 중단되었습니다. (Go 1.22 릴리스 노트에 발표됨)

### 리눅스 {#linux}

<!-- go.dev/issue/67001 -->
Go 1.23은 Linux 커널 버전 2.6.32 이상을 요구하는 마지막 릴리스입니다. Go 1.24는 Linux 커널 버전 3.2 이상을 요구합니다.

### OpenBSD {#openbsd}

<!-- go.dev/issue/55999, CL 518629, CL 518630 -->
Go 1.23 버전에서 64비트 RISC-V 아키텍처 ( `GOOS=openbsd`, `GOARCH=riscv64`) 에 대한 실험적인 OpenBSD 지원이 추가되었습니다.

### ARM64 {#arm64}

<!-- go.dev/issue/60905, CL 559555 -->
Go 1.23은 새로운 `GOARM64` 환경 변수를 도입하며, 이는 컴파일 시간에 ARM64 아키텍처의 최소 대상 버전을 지정합니다. 허용되는 값은 `v8.{0-9}` 및 `v9.{0-5}`입니다. 또한 대상 하드웨어가 구현한 확장을 지정하는 옵션이 뒤따를 수 있습니다. 유효한 옵션은 `,lse` 및 `,crypto`입니다.

`GOARM64` 환경 변수의 기본값은 `v8.0`입니다.

### RISC-V {#riscv}

<!-- go.dev/issue/61476, CL 541135 -->
Go 1.23은 새로운 `GORISCV64` 환경 변수를 도입합니다. 이 환경 변수는 컴파일할 [RISC-V 사용자 모드 애플리케이션 프로필](https://github.com/riscv/riscv-profiles/blob/main/src/profiles.adoc)을 선택합니다. 허용되는 값은 `rva20u64` 및 `rva22u64`입니다.

`GORISCV64` 환경 변수의 기본값은 `rva20u64`입니다.

### WebAssembly {#wasm}

<!-- go.dev/issue/63718 -->
`GOROOT/misc/wasm`에 있는 `go_wasip1_wasm_exec` 스크립트가 `wasmtime` 버전 14.0.0 미만을 지원 중단했습니다.

<!-- 다음 항목들을 완료하고 적절한 위치에 릴리스 노트에 이동해야 합니다. -->

<!-- 다음 항목들을 검토하고, Go 1.23 릴리스 노트에 적절히 언급해야 합니다.

현재 없습니다; 나중에 추가될 수 있습니다.

<!-- 아마도 설명이 필요할까요? 아니면 필요 없을까요? 이 변경 사항에 대해 잘 아는 사람이 결정해야 합니다.

CL 359594 ("x/website/_content/ref/mod: document dotless module paths") - 해결됨: go.dev/issue/32819 ("cmd/go: document that module names without dots are reserved") 및 또한 승인된 제안 go.dev/issue/37641을 언급
CL 555075 ("x/tools/go/ssa: support range-over-func") - x/tools CL은 승인된 제안 https://go.dev/issue/66601에 따라 x/tools/go/ssa에서 range-over-func 지원을 구현합니다. 이 특정 제안 및 변경 사항은 Go 1.23 릴리스 노트에 별도의 언급이 필요하지 않지만, 더 숙련된 사람이 다시 검토해야 합니다.

<!-- 1.23 릴리스 노트에 언급할 필요가 없는 항목이지만, relnote todo에서 감지되는 항목. -->

CL 458895 - x/playground 수정으로 언급된 수락된 cmd/go 제안 go.dev/issue/40728 (Go 1.16 마일스톤)
CL 582097 - x/build CL, 자체 릴리스 노트 작업 중. 릴리스 노트 불필요
CL 561935 - crypto CL, purego 태그 사용 및 수락된 구현되지 않은 제안 https://go.dev/issue/23172로 purego 태그 문서화. 릴리스 노트 불필요
CL 568340 - time.Ticker.Reset의 허위 경쟁 수정 (https://go.dev/issue/33184를 통해 수락된 제안). 릴리스 노트 불필요
CL 562619 - x/website CL, go.dev에서 최소 부트스트랩 버전 문서화, 수락된 제안 go.dev/issue/54265 및 go.dev/issue/44505 참조. 릴리스 노트 불필요
CL 557055 - x/tools CL, x/tools/go/ssa에 대한 수락된 제안 https://go.dev/issue/46941 구현
CL 564275 - x/tools CL, 수락된 제안 https://go.dev/issue/51473에 대한 테스트 데이터 업데이트. 제안은 Go 1.23에 구현되지 않았으므로 릴리스 노트 불필요
CL 572535 - "unix" 빌드 태그를 더 많은 곳에 사용, 수락된 제안 https://go.dev/issue/51572 참조. 릴리스 노트 불필요
CL 555255 - x/tools CL, x/tools/go/cfg에 대한 수락된 제안 https://go.dev/issue/53367 구현
CL 585216 - x/build CL, 새로운 Go 1.22 포트에 대한 다운로드 생성 중 오류를 수정하는 것을 언급, https://go.dev/issue/56001 (Go 1.22)에 대한 Go 1.23 릴리스 노트와 관련 없음
CL 481062 - 수락된 제안 https://go.dev/issue/56102에 대한 예제 추가. 릴리스 노트 불필요
CL 497195 - x/net CL, x/net/http2에서 수락된 제안 https://go.dev/issue/57893의 4개 필드 중 하나 추가. net/http와 관련이 없으므로 Go 1.23 릴리스 노트 불필요
CL 463097, CL 568198 - x/net CL, x/net/websocket에 대한 수락된 제안 https://go.dev/issue/57953 구현. rel note 불필요
많은 x/net CLs - x/net/quic에 QUIC 구현을 추가하기 위한 수락된 제안 https://go.dev/issue/58547 작업
CL 514775 - 수락된 제안 https://go.dev/issue/59488에 대한 성능 최적화 구현
CL 484995 - x/sys CL, x/sys/unix API 추가를 위한 수락된 제안 https://go.dev/issue/59537 구현
CL 555597 - 인터페이스 유형이 아닌 유형에 대해 TypeFor 최적화 (https://go.dev/issue/60088에 추가된 수락된 제안). 릴리스 노트 불필요
몇 개의 x/tools CLs, go.dev/x/tools/cmd/getgo 도구를 수락된 제안 https://go.dev/issue/60951에 따라 사용 중단 및 삭제. 릴리스 노트에 포함되지 않음
많은 x/vuln CLs, govulncheck에 수락된 제안 https://go.dev/issue/61347 ("x/vuln: govulncheck 출력을 SARIF 형식으로 변환") 구현
CL 516355 - x/crypto CL, x/crypto/ssh에 대한 수락된 제안 https://go.dev/issue/61447 구현. Go 1.23 릴리스 노트 불필요
CL 559799 - Go 1.22 릴리스 노트 수정, Go 1.22에 대한 수락된 제안 https://go.dev/issue/62039, Go 1.23 개발 시작 후 약간.
CL 581555 - x/tools CL, x/tools/go/aalysis에 대한 수락된 제안 https://go.dev/issue/62292 언급. Go 1.23 릴리스 노트 불필요
CL 578355 - GOARCH=wasm32 추가, https://go.dev/issue/63131에 대한 수락된 제안 언급, 그러나 해당 제안은 Go 1.23에 구현되지 않았으므로 릴리스 노트 불필요
CL 543335 - x/exp CL, 슬라이스 패키지에 변경 사항을 백포트 (https://go.dev/issue/63393에 수락된 제안)를 x/exp/slices에 추가. Go 1.23 릴리스 노트 불필요
CL 556820 - x/tools CL, x/tools/go/analysis에 대한 수락된 제안 https://go.dev/issue/64548 구현
CL 557056 - x/tools CL, x/tools/go/packages에 대한 수락된 제안 https://go.dev/issue/64608 구현
CL 558695 - x/crypto CL, x/crypto/ssh에 대한 수락된 제안 https://go.dev/issue/64962 작업
CL 572016 - x/tools CL, x/tools/go/cfg에 대한 수락된 제안 https://go.dev/issue/65754 구현
몇 개의 x/tools CLs, go.dev/x/tools/cmd/guru 명령을 수락된 제안 https://go.dev/issue/65880에 따라 태그하고 삭제. 릴리스 노트에 포함되지 않음
CL 580076 - x/go 내부 명령, 모듈 정보를 전파하기 위한 수락된 제안 https://go.dev/issue/66315. 릴리스 노트 불필요
CL 529816 - "tests" vet check를 "go test" 세트에 추가, 수락된 제안 https://go.dev/issue/44251, 변경 사항이 CL 571695에서 되돌렸고 2024-05-23 이후로 진행되지 않음. Go 1.23 릴리스 노트에 문서화할 내용 없음
CL 564035 - encoding/xml 변경, 변경이 너무 광범위하여 CL 570175에서 되돌렸고, 추적 이슈 go.dev/issue/65691 재개. Go 1.23 릴리스 노트에 문서화할 내용 없음
CL 587855 - 수락된 제안 https://go.dev/issue/60529의 이점을 보여줌. 실제 변경은 Go 1.23에 적용되지 않으므로 릴리스 노트 불필요
CL 526875 - x/crypto CL, x/crypto/ssh에 대한 수락된 제안 https://go.dev/issue/62518 구현
