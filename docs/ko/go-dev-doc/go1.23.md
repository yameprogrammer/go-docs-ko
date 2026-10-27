<!--
참고: 이 문서 및 이 디렉토리의 다른 문서에서는 `hello` `world`와 같이 고정폭 구문을 비고정폭 공백으로 설정하는 것이 관례입니다.
-->

<style>
  main ul li { margin: 0.5em 0; }
</style>

## Go 1.23 소개 {#introduction}

최신 Go 릴리스인 버전 1.23이 [Go 1.22](/doc/go1.22) 출시 6개월 만에 공개되었습니다.
변경 사항의 대부분은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언제나 그렇듯, 이번 릴리스에서도 Go 1 [호환성 약속](/doc/go1compat)을 유지합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

<!-- go.dev/issue/61405, CL 557835, CL 584596 -->
"for-range" 루프의 "range" 절은 이제 다음과 같은 타입의 반복자(iterator) 함수를 허용합니다.

func(func() bool)
    func(func(K) bool)
    func(func(K, V) bool)

range 표현식으로 사용됩니다.
반복자(iterator) 인자 함수를 호출하면 "for-range" 루프에 필요한 반복 값이 생성됩니다.
자세한 내용은 [`iter`](/pkg/iter) 패키지 문서, [언어 사양](/ref/spec#For_range), 그리고 [Range over Function Types 블로그 포스트](/blog/range-functions)를 참조하십시오.
도입 배경은 2022년 ["range-over-func" 토론](/issue/56413)을 참조하십시오.

<!-- go.dev/issue/46477, CL 566856, CL 586955, CL 586956 -->
Go 1.23에는 [제네릭 타입 별칭(generic type aliases)](/issue/46477)에 대한 프리뷰 지원이 포함되었습니다.
`GOEXPERIMENT=aliastypeparams`를 사용하여 툴체인을 빌드하면 패키지 내에서 이 기능을 활성화할 수 있습니다.
(패키지 경계를 넘나드는 제네릭 별칭 타입 사용은 아직 지원되지 않습니다.)

## Tools {#tools}

### Telemetry

<!-- go.dev/issue/58894, go.dev/issue/67111 -->
Go 1.23부터 Go 툴체인은 Go 팀이 Go 툴체인이 어떻게 사용되고 얼마나 잘 작동하는지 이해하는 데 도움이 되는 사용량 및 오류 통계를 수집할 수 있습니다. 우리는 이러한 통계를 [Go telemetry](/doc/telemetry)라고 부릅니다.

Go telemetry는 [`go` `telemetry` 명령](/cmd/go/#hdr-Manage_telemetry_data_and_settings)으로 제어되는 _선택 참여 시스템(opt-in system)_입니다. 기본적으로 툴체인 프로그램은 로컬에서 확인할 수 있지만 그 외에는 사용되지 않는 카운터 파일에 통계를 수집합니다 (`go` `telemetry` `local`).

Go가 원활하게 작동하도록 유지하고 Go 사용 현황을 파악하는 데 도움을 주기 위해,
`go` `telemetry` `on` 명령어를 실행하여 Go 텔레메트리(telemetry) 참여를 고려해 주세요.
이 모드에서는
익명의 카운터 보고서가 매주 [telemetry.go.dev](https://telemetry.go.dev)로 업로드되며,
이 데이터는 그래프로 집계될 뿐만 아니라
데이터 분석을 원하는 모든 Go 기여자나 사용자가 다운로드할 수 있도록 제공됩니다.
Go 텔레메트리 시스템에 대한 자세한 내용은 “[Go Telemetry](/doc/telemetry)”를 참조하세요.

### Go command {#go-command}

`GOROOT_FINAL` 환경 변수를 설정하는 것은 더 이상 효과가 없습니다 ([#62047](/issue/62047)).
`go` 명령어를 `$GOROOT/bin/go` 이외의 위치에 설치하는 배포판은 `go` 바이너리를 이동하거나 복사하는 대신 심볼릭 링크(symlink)를 설치해야 합니다.

<!-- go.dev/issue/34208, CL 563137, CL 586095 -->
새로운 `go` `env` `-changed` 플래그를 사용하면, `-w` 플래그를 이전에 사용하지 않은 빈 환경에서 얻을 수 있는 기본값과 실제 유효 값이 다른 설정들만 출력합니다.

<!-- go.dev/issue/27005, CL 585401 -->
새로운 `go` `mod` `tidy` `-diff` 플래그를 사용하면 명령어가 파일을 수정하는 대신 필요한 변경 사항을 unified diff 형식으로 출력합니다. 업데이트가 필요한 경우 0이 아닌 종료 코드로 종료됩니다.

<!-- go.dev/issue/52792, CL 562775 -->
`go` `list` `-m` `-json` 명령에 새로운 `Sum` 및 `GoModSum` 필드가 추가되었습니다.
이는 `go` `mod` `download` `-json` 명령의 기존 동작과 유사합니다.

<!-- go.dev/issue/65573 ("cmd/go: separate default GODEBUGs from go language version") -->
`go.mod` 및 `go.work`에 추가된 새로운 `godebug` 지시문은 사용 중인 작업 모듈 또는 워크스페이스에 적용할 [GODEBUG 설정](/doc/godebug)을 선언합니다.

### Vet {#vet}

<!-- go.dev/issue/46136 -->
`go vet` 서브커맨드에 이제 [stdversion](https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/stdversion) 분석기가 포함되었습니다. 이 분석기는 참조하는 파일에 적용되는 Go 버전보다 너무 최신인 심볼을 참조하는 경우 플래그를 표시합니다. (적용 버전은 해당 파일이 포함된 `go.mod` 파일의 `go` 지시문과 파일 내의 [`//go:build` 제약 조건](/cmd/go#hdr-Build_constraints)에 의해 결정됩니다.)

예를 들어, `go.mod` 파일에 `go 1.21`이 지정된 모듈의 파일에서 (go1.22에서 도입된) `reflect.TypeFor` 함수를 참조하는 경우 진단 보고서(diagnostic)를 생성합니다.

### Cgo {#cgo}

<!-- go.dev/issue/66456 -->
[`cmd/cgo`](/pkg/cmd/cgo)가 C 링커에 플래그를 전달하기 위한 새로운 `-ldflags` 플래그를 지원합니다.
`go` 명령어가 이를 자동으로 사용하므로, `CGO_LDFLAGS`가 매우 클 때 발생하는 "argument list too long" 오류를 방지할 수 있습니다.

### Trace {#trace}

<!-- go.dev/issue/65316 -->
`trace` 도구가 이제 가능한 한 많은 트레이스 데이터를 복구하려고 시도함으로써, 부분적으로 손상된 트레이스에 대해 더 나은 내성을 갖게 되었습니다. 이 기능은 프로그램 충돌 중에 수집된 트레이스를 확인할 때 특히 유용한데, 대부분의 상황에서 충돌 직전까지의 트레이스 데이터를 [복구할 수 있기](/issue/65319) 때문입니다.

## 런타임 {#runtime}

처리되지 않은 panic이나 기타 치명적인 오류가 발생한 후 런타임이 출력하는 traceback에서, 이제 오류 메시지(예: panic으로 전달된 인자)의 두 번째 줄부터는 탭 하나만큼 들여쓰기가 적용됩니다. 이를 통해 첫 번째 goroutine의 스택 트레이스와 명확하게 구분할 수 있습니다. 관련 논의는 [#64590](/issue/64590)을 참조하십시오.

## 컴파일러 {#compiler}

[Profile Guided Optimization](/doc/pgo)을 사용하여 빌드할 때 발생하는 빌드 시간 오버헤드가 크게 감소했습니다.
이전에는 대규모 빌드 시 PGO를 활성화하면 빌드 시간이 100% 이상 증가하는 경우가 있었습니다.
Go 1.23에서는 오버헤드가 한 자릿수 퍼센트 내외가 될 것입니다.

<!-- https://go.dev/issue/62737 , https://golang.org/cl/576681,  https://golang.org/cl/577615 -->
Go 1.23의 컴파일러는 이제 함수의 서로 다른 영역에서 액세스되는 지역 변수의 스택 프레임 슬롯을 중첩(overlap)시킬 수 있으며, 이를 통해 Go 애플리케이션의 스택 사용량을 줄입니다.

<!-- https://go.dev/cl/577935 -->
386 및 amd64의 경우, 컴파일러는 PGO의 정보를 사용하여 루프 내의 특정 핫 블록(hot blocks)을 정렬합니다. 이는 텍스트 및 바이너리 크기가 약 0.1% 증가하는 대신 성능을 1-1.5% 추가로 향상시킵니다. 현재 이 기능은 다른 플랫폼에서는 개선 효과가 나타나지 않았기 때문에 386 및 amd64에서만 구현되었습니다.
핫 블록 정렬은 `-gcflags=[<packages>=]-d=alignhot=0`으로 비활성화할 수 있습니다.

## Linker {#linker}

<!-- go.dev/issue/67401, CL 585556, CL 587220, and many more -->
이제 링커는 정의 부분에 `//go:linkname`이 표시되지 않은 표준 라이브러리(런타임 포함)의 내부 심볼을 참조하기 위해 `//go:linkname` 지시어를 사용하는 것을 허용하지 않습니다.
마찬가지로, 링커는 어셈블리 코드에서 이러한 심볼을 참조하는 것을 허용하지 않습니다.
하위 호환성을 위해, 대규모 오픈 소스 코드 코퍼스에서 발견된 기존의 `//go:linkname` 사용 사례는 계속 지원됩니다.
표준 라이브러리 내부 심볼에 대한 새로운 참조는 허용되지 않습니다.

디버깅 및 실험 목적으로 이 검사를 비활성화하려면 링커 커맨드 라인 플래그 `-checklinkname=0`을 사용할 수 있습니다.

<!-- CL 473495 -->
동적으로 링크된 ELF 바이너리(PIE 바이너리 포함)를 빌드할 때, 새로운 `-bindnow` 플래그를 사용하면 즉시 함수 바인딩(immediate function binding)이 활성화됩니다.

## 표준 라이브러리 {#library}

### 타이머 변경 사항

Go 1.23에서는 [`time.Timer`](/pkg/time#Timer) 및 [`time.Ticker`](/pkg/time#Ticker)의 구현에 두 가지 중요한 변경 사항이 도입되었습니다.

<!-- go.dev/issue/61542 -->
먼저, 프로그램에서 더 이상 참조되지 않는 `Timer`와 `Ticker`는 `Stop` 메서드가 호출되지 않았더라도 즉시 가비지 컬렉션(garbage collection) 대상이 됩니다.
이전 버전의 Go에서는 정지되지 않은 `Timer`가 만료될 때까지 수집하지 않았으며, 정지되지 않은 `Ticker`는 절대 수집하지 않았습니다.

<!-- go.dev/issue/37196 -->
둘째로, `Timer` 또는 `Ticker`와 연결된 타이머 채널이 이제 용량 0의 언버퍼드(unbuffered) 채널이 되었습니다.
이 변경 사항의 주요 효과는 `Reset` 또는 `Stop` 메서드를 호출할 때, 해당 호출 이전에 준비된 오래된 값(stale values)이 호출 이후에 전송되거나 수신되지 않음을 Go가 이제 보장한다는 점입니다.
이전 버전의 Go에서는 요소 하나 크기의 버퍼를 가진 채널을 사용하여 `Reset` 및 `Stop`을 올바르게 사용하는 것이 어려웠습니다.
이 변경으로 인해 눈에 띄는 효과는 타이머 채널의 `len`과 `cap`이 이제 1 대신 0을 반환한다는 것이며, 이는 채널의 길이를 확인하여 타이머 채널의 수신 성공 여부를 결정하는 프로그램에 영향을 줄 수 있습니다.
이러한 코드는 대신 논블로킹 수신(non-blocking receive)을 사용해야 합니다.

이러한 새로운 동작들은 메인 Go 프로그램이 Go 1.23.0 또는 그 이후 버전을 사용하는 `go.mod` 파일의 `go` 라인이 포함된 모듈에 있을 때만 활성화됩니다. Go 1.23이 이전 프로그램들을 빌드할 때는 기존 동작이 그대로 유지됩니다. 새로운 [GODEBUG 설정](/doc/godebug) [`asynctimerchan=1`](/pkg/time/#NewTimer)을 사용하면, 프로그램의 `go.mod` 파일에 Go 1.23.0 또는 그 이후 버전이 명시되어 있더라도 비동기 채널 동작으로 되돌릴 수 있습니다.

### 새로운 고유 패키지

새로운 [`unique`](/pkg/unique) 패키지는 값의 정규화(canonicalizing)를 위한 기능(예: "interning" 또는 "hash-consing")을 제공합니다.

comparable 타입의 모든 값은 새로운 `Make[T]` 함수를 통해 정준화(canonicalized)될 수 있으며, 이 함수는 해당 값의 정준 복사본에 대한 참조를 `Handle[T]` 형태로 생성합니다.
두 `Handle[T]`는 핸들을 생성하는 데 사용된 값들이 서로 같을 때에만 서로 같습니다. 이를 통해 프로그램은 값의 중복을 제거하고 메모리 사용량을 줄일 수 있습니다.
두 `Handle[T]` 값을 비교하는 것은 효율적이며, 단순한 포인터 비교로 환원됩니다.

### 이터레이터 (Iterators)

새로운 [`iter`](/pkg/iter) 패키지는 사용자 정의 반복자(iterator)를 다루기 위한 기본 정의를 제공합니다.

[`slices`](/pkg/slices) 패키지는 반복자(iterator)와 함께 작동하는 여러 함수를 제공합니다:
- [All](/pkg/slices#All)은 슬라이스의 인덱스와 값에 대한 반복자를 반환합니다.
- [Values](/pkg/slices#Values)는 슬라이스 요소에 대한 반복자를 반환합니다.
- [Backward](/pkg/slices#Backward)는 슬라이스를 역순으로 순회하는 반복자를 반환합니다.
- [Collect](/pkg/slices#Collect)는 반복자의 값들을 모아 새로운 슬라이스로 만듭니다.
- [AppendSeq](/pkg/slices#AppendSeq)는 반복자의 값들을 기존 슬라이스에 추가합니다.
- [Sorted](/pkg/slices#Sorted)는 반복자의 값들을 모아 새로운 슬라이스로 만든 후, 해당 슬라이스를 정렬합니다.
- [SortedFunc](/pkg/slices#SortedFunc)는 `Sorted`와 유사하지만 비교 함수를 사용합니다.
- [SortedStableFunc](/pkg/slices#SortedStableFunc)는 `SortFunc`와 유사하지만 안정 정렬(stable sort) 알고리즘을 사용합니다.
- [Chunk](/pkg/slices#Chunk)는 슬라이스를 최대 n개의 요소로 구성된 연속적인 하위 슬라이스들에 대한 반복자로 반환합니다.

[`maps`](/pkg/maps) 패키지는 이터레이터(iterator)와 함께 작동하는 여러 함수를 제공합니다:
- [All](/pkg/maps#All)은 맵의 키-값 쌍에 대한 이터레이터를 반환합니다.
- [Keys](/pkg/maps#Keys)는 맵의 키에 대한 이터레이터를 반환합니다.
- [Values](/pkg/maps#Values)는 맵의 값에 대한 이터레이터를 반환합니다.
- [Insert](/pkg/maps#Insert)는 이터레이터의 키-값 쌍을 기존 맵에 추가합니다.
- [Collect](/pkg/maps#Collect)는 이터레이터의 키-값 쌍을 모아 새로운 맵을 생성하여 반환합니다.

### 새로운 structs 패키지

새로운 [`structs`](/pkg/structs) 패키지는 메모리 레이아웃과 같이 포함된 struct 타입의 속성을 수정하는 struct 필드용 타입들을 제공합니다.

이번 릴리스에서 유일한 이러한 타입은 [`HostLayout`](/pkg/structs#HostLayout)이며, 이는 해당 타입의 필드를 가진 구조체가 호스트 플랫폼의 기대치에 부합하는 레이아웃을 가지고 있음을 나타냅니다. `HostLayout`은 호스트 API로 전달되거나, 호스트 API로부터 반환되거나, 또는 호스트 API로 전달/수신되는 포인터를 통해 액세스되는 타입에 사용해야 합니다. 이 마커가 없으면 언어 명세상 구조체 레이아웃 순서가 보장되지 않지만, Go 1.23 기준으로 호스트 레이아웃과 언어 레이아웃이 우연히 일치합니다.

### 라이브러리의 마이너 변경 사항 {#minor_library_changes}

#### [`archive/tar`](/pkg/archive/tar/)

[`FileInfoHeader`](/pkg/archive/tar#FileInfoHeader)에 전달되는 인자가 새로운 [`FileInfoNames`](/pkg/archive/tar#FileInfoNames) 인터페이스를 구현하는 경우, 해당 인터페이스 메서드들이 파일 헤더의 Uname/Gname을 설정하는 데 사용됩니다. 이를 통해 애플리케이션은 시스템 종속적인 Uname/Gname 조회를 오버라이드할 수 있습니다.

#### [`crypto/tls`](/pkg/crypto/tls/)

이제 TLS 클라이언트는 암호화된 클라이언트 헬로(Encrypted Client Hello) [초안 사양](https://www.ietf.org/archive/id/draft-ietf-tls-esni-18.html)을 지원합니다.
이 기능은 [`Config.EncryptedClientHelloConfigList`](/pkg/crypto/tls#Config.EncryptedClientHelloConfigList) 필드를 연결하려는 호스트에 대한 인코딩된 ECHConfigList로 설정하여 활성화할 수 있습니다.

QUIC 구현에서 사용하는 [`QUICConn`](/pkg/crypto/tls#QUICConn) 타입에는 세션 재개(session resumption) 상태를 보고하는 새로운 이벤트가 포함되어 있으며, QUIC 계층에서 세션 티켓 및 세션 캐시 엔트리에 데이터를 추가할 수 있는 방법을 제공합니다.

[`Config.CipherSuites`](/pkg/crypto/tls#Config.CipherSuites)가 nil일 때 사용되는 기본 목록에서 3DES 사이퍼 스위트(cipher suites)가 제거되었습니다. GODEBUG 환경 변수에 `tls3des=1`을 추가하여 기본 설정으로 되돌릴 수 있습니다.

실험적인 양자 내성 키 교환 메커니즘인 `X25519Kyber768Draft00`이 이제 [`Config.CurvePreferences`](/pkg/crypto/tls#Config.CurvePreferences)가 `nil`일 때 기본적으로 활성화됩니다.
`GODEBUG` 환경 변수에 `tlskyber=0`을 추가하여 기본 설정을 되돌릴 수 있습니다.
이는 큰 레코드를 올바르게 처리하지 못해 핸드쉐이크 중 타임아웃이 발생하는 결함이 있는 TLS 서버를 다룰 때 유용할 수 있습니다 ( [TLS post-quantum TL;DR fail](https://tldr.fail/) 참조).

Go 1.23에서는 [`X509KeyPair`](/pkg/crypto/tls#X509KeyPair) 및 [`LoadX509KeyPair`](/pkg/crypto/tls#LoadX509KeyPair)의 동작이 변경되어, 반환되는 [`Certificate`](/pkg/crypto/tls#Certificate)의 [`Certificate.Leaf`](/pkg/crypto/tls#Certificate.Leaf) 필드를 채우도록 수정되었습니다.
이 동작을 제어하기 위해 새로운 `x509keypairleaf` [GODEBUG 설정](/doc/godebug)이 추가되었습니다.

#### [`crypto/x509`](/pkg/crypto/x509/)

[`CreateCertificateRequest`](/pkg/crypto/x509#CreateCertificateRequest)가 이제 RSA-PSS 서명 알고리즘을 올바르게 지원합니다.

[`CreateCertificateRequest`](/pkg/crypto/x509#CreateCertificateRequest) 및 [`CreateRevocationList`](/pkg/crypto/x509#CreateRevocationList)가 이제 서명자의 공개 키를 사용하여 생성된 서명을 검증합니다. 서명이 유효하지 않은 경우 에러가 반환됩니다. 이는 Go 1.16부터 [`CreateCertificate`](/pkg/crypto/x509#CreateCertificate)에 적용되어 온 동작입니다.

[`x509sha1` GODEBUG 설정](/pkg/crypto/x509#InsecureAlgorithmError)은 다음 Go 메이저 릴리스(Go 1.24)에서 제거될 예정입니다. 이는 `crypto/x509`가 SHA-1 기반 서명 알고리즘을 사용하는 인증서의 서명 검증을 더 이상 지원하지 않음을 의미합니다.

새로운 [`ParseOID`](/pkg/crypto/x509#ParseOID) 함수는 점으로 구분된(dot-encoded) ASN.1 객체 식별자(Object Identifier) 문자열을 파싱합니다.
[`OID`](/pkg/crypto/x509#OID) 타입은 이제 [`encoding.BinaryMarshaler`](/pkg/encoding#BinaryMarshaler),
[`encoding.BinaryUnmarshaler`](/pkg/encoding#BinaryUnmarshaler), [`encoding.TextMarshaler`](/pkg/encoding#TextMarshaler), [`encoding.TextUnmarshaler`](/pkg/encoding#TextUnmarshaler) 인터페이스를 구현합니다.

#### [`database/sql`](/pkg/database/sql/)

[`driver.Valuer`](/pkg/driver#Valuer) 구현체에서 반환하는 에러가 이제 래핑되어, [`DB.Query`](/pkg/database/sql#DB.Query), [`DB.Exec`](/pkg/database/sql#DB.Exec), [`DB.QueryRow`](/pkg/database/sql#DB.QueryRow)와 같은 작업 중에 더 향상된 에러 처리가 가능해졌습니다.

#### [`debug/elf`](/pkg/debug/elf/)

`debug/elf` 패키지에 이제 [`PT_OPENBSD_NOBTCFI`](/pkg/debug/elf#PT_OPENBSD_NOBTCFI)가 정의되었습니다. 이 [`ProgType`](/pkg/debug/elf#ProgType)은 OpenBSD 바이너리에서 Branch Tracking Control Flow Integrity (BTCFI) 적용을 비활성화하는 데 사용됩니다.

이제 심볼 타입 상수 [`STT_RELC`](/pkg/debug/elf#STT_RELC), [`STT_SRELC`](/pkg/debug/elf#STT_SRELC), 그리고 [`STT_GNU_IFUNC`](/pkg/debug/elf#STT_GNU_IFUNC)를 정의합니다.

#### [`encoding/binary`](/pkg/encoding/binary/)

새로운 [`Encode`](/pkg/encoding/binary#Encode) 및 [`Decode`](/pkg/encoding/binary#Decode) 함수는 [`Read`](/pkg/encoding/binary#Read) 및 [`Write`](/pkg/encoding/binary#Write)의 바이트 슬라이스 버전입니다.
[`Append`](/pkg/encoding/binary#Append)를 사용하면 여러 데이터를 동일한 바이트 슬라이스로 마샬링(marshaling)할 수 있습니다.

#### [`go/ast`](/pkg/go/ast/)

새로운 [`Preorder`](/pkg/go/ast#Preorder) 함수는 구문 트리(syntax tree)의 모든 노드에 대해 편리한 이터레이터(iterator)를 반환합니다.

#### [`go/types`](/pkg/go/types/)

<!-- see ../../../../2-language.md -->

함수 또는 메서드 심볼을 나타내는 [`Func`](/pkg/go/types#Func) 타입에 함수의 타입을 반환하는 [`Func.Signature`](/pkg/go/types#Func.Signature) 메서드가 추가되었습니다. 이 메서드가 반환하는 타입은 항상 `Signature`입니다.

[`Alias`](/pkg/go/types#Alias) 타입에 이제 선언문의 우변에 있는 타입을 반환하는 [`Rhs`](/pkg/go/types#Rhs) 메서드가 추가되었습니다. 예를 들어 `type A = B`가 주어진 경우, A의 `Rhs`는 B가 됩니다. ([#66559](/issue/66559))

[`Alias.Origin`](/pkg/go/types#Alias.Origin), [`Alias.SetTypeParams`](/pkg/go/types#Alias.SetTypeParams), [`Alias.TypeParams`](/pkg/go/types#Alias.TypeParams),
그리고 [`Alias.TypeArgs`](/pkg/go/types#Alias.TypeArgs) 메서드가 추가되었습니다. 이들은 제네릭 별칭 타입(generic alias types)을 위해 필요합니다.

<!-- CL 577715, CL 579076 -->
기본적으로 이제 go/types는 타입 별칭(type alias)에 대해 [`Alias`](/pkg/go/types#Alias) 타입 노드를 생성합니다.
이 동작은 `GODEBUG` `gotypesalias` 플래그로 제어할 수 있습니다.
기본값이 Go 1.22의 0에서 Go 1.23의 1로 변경되었습니다.

#### [`math/rand/v2`](/pkg/math/rand/v2/)

[`Uint`](/pkg/math/rand/v2#Uint) 함수와 [`Rand.Uint`](/pkg/math/rand/v2#Rand.Uint) 메서드가 추가되었습니다.
이들은 실수로 Go 1.22에서 누락되었습니다.

새로운 [`ChaCha8.Read`](/pkg/math/rand/v2#ChaCha8.Read) 메서드는 [`io.Reader`](/pkg/io#Reader) 인터페이스를 구현합니다.

#### [`net`](/pkg/net/)

새로운 타입 [`KeepAliveConfig`](/pkg/net#KeepAliveConfig)는 새로운 [`TCPConn.SetKeepAliveConfig`](/pkg/net#TCPConn.SetKeepAliveConfig) 메서드와 [`Dialer`](/pkg/net#Dialer) 및 [`ListenConfig`](/pkg/net#ListenConfig)에 추가된 새로운 KeepAliveConfig 필드를 통해 TCP 연결의 keep-alive 옵션을 세밀하게 조정할 수 있게 해줍니다.

[`DNSError`](/pkg/net#DNSError) 타입이 이제 타임아웃이나 취소로 인해 발생한 에러를 래핑(wrap)합니다.
예를 들어, `errors.Is(someDNSErr, context.DeadlineExceedeed)`를 통해 DNS 에러가 타임아웃으로 인해 발생했는지 여부를 확인할 수 있습니다.

새로운 `GODEBUG` 설정인 `netedns0=0`은 DNS 요청 시 EDNS0 추가 헤더 전송을 비활성화합니다. 이는 일부 모뎀의 DNS 서버에서 해당 헤더로 인해 문제가 발생한다는 보고가 있었기 때문입니다.

#### [`net/http`](/pkg/net/http/)

[`Cookie`](/pkg/net/http#Cookie)가 이제 쿠키 값을 둘러싼 큰따옴표를 보존합니다.
새로운 [`Cookie.Quoted`](/pkg/net/http#Cookie.Quoted) 필드는 [`Cookie.Value`](/pkg/net/http#Cookie.Value)가 원래 따옴표로 둘러싸여 있었는지를 나타냅니다.

새로운 [`Request.CookiesNamed`](/pkg/net/http#Request.CookiesNamed) 메서드는 주어진 이름과 일치하는 모든 쿠키를 가져옵니다.

새로운 [`Cookie.Partitioned`](/pkg/net/http#Cookie.Partitioned) 필드는 Partitioned 속성이 지정된 쿠키를 식별합니다.

[`ServeMux`](/pkg/net/http#ServeMux)에서 사용하는 패턴은 이제 메서드 이름 뒤에 하나 이상의 공백이나 탭을 허용합니다.
이전에는 단일 공백만 허용되었습니다.

새로운 [`ParseCookie`](/pkg/net/http#ParseCookie) 함수는 Cookie 헤더 값을 파싱하여 설정된 모든 쿠키를 반환합니다. 동일한 쿠키 이름이 여러 번 나타날 수 있으므로, 반환된 Values는 특정 키에 대해 하나 이상의 값을 포함할 수 있습니다.

새로운 [`ParseSetCookie`](/pkg/net/http#ParseSetCookie) 함수는 Set-Cookie 헤더 값을 파싱하여 쿠키를 반환합니다. 구문 오류가 발생하면 에러를 반환합니다.

[`ServeContent`](/pkg/net/http#ServeContent), [`ServeFile`](/pkg/net/http#ServeFile), 및 [`ServeFileFS`](/pkg/net/http#ServeFileFS)가 이제 에러를 응답할 때 `Cache-Control`, `Content-Encoding`, `Etag`, 및 `Last-Modified` 헤더를 제거합니다. 이러한 헤더들은 보통 에러가 아닌 콘텐츠에 적용되며, 에러 텍스트에는 적용되지 않습니다.

[`ResponseWriter`](/pkg/net/http#ResponseWriter)를 래핑하여 `Content-Encoding: gzip`과 같은 실시간 인코딩을 적용하는 미들웨어는 이번 변경 이후로 작동하지 않습니다. [`ServeContent`](/pkg/net/http#ServeContent), [`ServeFile`](/pkg/net/http#ServeFile), 그리고 [`ServeFileFS`](/pkg/net/http#ServeFileFS)의 이전 동작은 `GODEBUG=httpservecontentkeepheaders=1`를 설정하여 복원할 수 있습니다.

콘텐츠의 크기를 변경하는 미들웨어(예: 압축)는 [`ServeContent`](/pkg/net/http#ServeContent)가 Range 요청을 처리할 때 이미 제대로 작동하지 않는다는 점에 유의하십시오. 즉석 압축(On-the-fly compression)은 `Content-Encoding` 대신 `Transfer-Encoding` 헤더를 사용해야 합니다.

인바운드 요청의 경우, 새로운 [`Request.Pattern`](/pkg/net/http#Request.Pattern) 필드에는 요청과 일치하는 [`ServeMux`](/pkg/net/http#ServeMux) 패턴(있는 경우)이 포함됩니다. `GODEBUG=httpmuxgo121=1`이 설정된 경우에는 이 필드가 설정되지 않습니다.

#### [`net/http/httptest`](/pkg/net/http/httptest/)

새로운 [`NewRequestWithContext`](/pkg/net/http/httptest#NewRequestWithContext) 메서드는 [`context.Context`](/pkg/context#Context)를 포함하는 수신 요청(incoming request)을 생성합니다.

#### [`net/netip`](/pkg/net/netip/)

Go 1.22 및 그 이전 버전에서는 IPv4 주소를 보유한 [`Addr`](/pkg/net/netip#Addr)와 해당 주소의 IPv4 매핑 IPv6 형태를 보유한 `Addr`를 비교하기 위해 [`reflect.DeepEqual`](/pkg/reflect#DeepEqual)을 사용할 때, `==` 또는 [`Addr.Compare`](/pkg/net/netip#Addr.Compare)로 비교했을 때 `Addr` 값이 다름에도 불구하고 잘못되게 true를 반환했습니다.
이 버그는 이제 수정되었으며, 세 가지 접근 방식 모두 이제 동일한 결과를 보고합니다.

#### [`os`](/pkg/os/)

[`Stat`](/pkg/os#Stat) 함수는 이제 Windows에서 Unix 소켓인 파일에 대해 [`ModeSocket`](/pkg/os#ModeSocket) 비트를 설정합니다. 이러한 파일은 리파스 태그(reparse tag)가 `IO_REPARSE_TAG_AF_UNIX`로 설정되어 있는 것으로 식별됩니다.

Windows에서 [`Lstat`](/pkg/os#Lstat) 및 [`Stat`](/pkg/os#Stat)이 재파싱 지점(reparse points)에 대해 보고하는 모드 비트(mode bits)가 변경되었습니다. 마운트 지점에는 더 이상 [`ModeSymlink`](/pkg/os#ModeSymlink)가 설정되지 않으며, 심볼릭 링크, Unix 소켓 또는 중복 제거 파일(dedup files)이 아닌 재파싱 지점에는 이제 항상 [`ModeIrregular`](/pkg/os#ModeIrregular)가 설정됩니다.
이 동작은 `winsymlink` 설정에 의해 제어됩니다.
Go 1.23의 경우, 기본값은 `winsymlink=1`입니다.
이전 버전의 기본값은 `winsymlink=0`입니다.

[`CopyFS`](/pkg/os#CopyFS) 함수는 [`io/fs.FS`](/pkg/io/fs#FS)를 로컬 파일 시스템으로 복사합니다.

Windows에서 [`Readlink`](/pkg/os#Readlink)는 더 이상 볼륨을 드라이브 문자로 정규화하려고 시도하지 않습니다. 이는 항상 가능했던 작업이 아니었습니다.
이 동작은 `winreadlinkvolume` 설정으로 제어됩니다.
Go 1.23의 경우, 기본값은 `winreadlinkvolume=1`입니다.
이전 버전의 기본값은 `winreadlinkvolume=0`입니다.

<!-- go.dev/issue/62654, CL 570036, CL 570681 -->
pidfd를 지원하는 Linux(일반적으로 Linux v5.4 이상)에서, [`Process`](/pkg/os#Process) 관련 함수와 메서드는 내부적으로 PID 대신 pidfd를 사용합니다. 이를 통해 OS에 의해 PID가 재사용될 때 발생할 수 있는 오타겟팅(mistargeting) 문제를 제거합니다. pidfd 지원은 프로세스가 가질 수 있는 추가적인 프로세스 파일 디스크립터를 제외하고는 사용자에게 완전히 투명하게 작동합니다.

#### [`path/filepath`](/pkg/path/filepath/)

새로운 [`Localize`](/pkg/path/filepath#Localize) 함수는 슬래시(`/`)로 구분된 경로를 운영 체제 경로로 안전하게 변환합니다.

Windows에서 [`EvalSymlinks`](/pkg/path/filepath#EvalSymlinks)는 더 이상 마운트 포인트(mount points)를 평가하지 않으며, 이는 많은 불일치와 버그의 원인이었습니다.
이 동작은 `winsymlink` 설정으로 제어됩니다.
Go 1.23의 경우, 기본값은 `winsymlink=1`입니다.
이전 버전의 기본값은 `winsymlink=0`입니다.

Windows에서 [`EvalSymlinks`](/pkg/path/filepath#EvalSymlinks)는 더 이상 볼륨을 드라이브 문자로 정규화하려고 시도하지 않으며, 이는 항상 가능했던 작업도 아니었습니다.
이 동작은 `winreadlinkvolume` 설정에 의해 제어됩니다.
Go 1.23의 경우, 기본값은 `winreadlinkvolume=1`입니다.
이전 버전의 기본값은 `winreadlinkvolume=0`입니다.

#### [`reflect`](/pkg/reflect/)

[`Value`](/pkg/reflect#Value)의 동일한 이름의 메서드와 의미가 같은 새로운 메서드들이 [`Type`](/pkg/reflect#Type)에 추가되었습니다:
1. [`Type.OverflowComplex`](/pkg/reflect#Type.OverflowComplex)
2. [`Type.OverflowFloat`](/pkg/reflect#Type.OverflowFloat)
3. [`Type.OverflowInt`](/pkg/reflect#Type.OverflowInt)
4. [`Type.OverflowUint`](/pkg/reflect#Type.OverflowUint)

새로운 [`SliceAt`](/pkg/reflect#SliceAt) 함수는 [`NewAt`](/pkg/reflect#NewAt)와 유사하지만, 슬라이스(slice)를 위한 함수입니다.

[`Value.Pointer`](/pkg/reflect#Value.Pointer) 및 [`Value.UnsafePointer`](/pkg/reflect#Value.UnsafePointer) 메서드가 이제 [`String`](/pkg/reflect#String) 종류의 값을 지원합니다.

새로운 메서드 [`Value.Seq`](/pkg/reflect#Value.Seq)와 [`Value.Seq2`](/pkg/reflect#Value.Seq2)는 해당 값이 for/range 루프에서 사용되는 것처럼 값을 반복하는 시퀀스를 반환합니다.
새로운 메서드 [`Type.CanSeq`](/pkg/reflect#Type.CanSeq)와 [`Type.CanSeq2`](/pkg/reflect#Type.CanSeq2)는 각각 [`Value.Seq`](/pkg/reflect#Value.Seq)와 [`Value.Seq2`](/pkg/reflect#Value.Seq2)를 호출했을 때 패닉 없이 성공할지 여부를 보고합니다.

#### [`runtime/debug`](/pkg/runtime/debug/)

[`SetCrashOutput`](/pkg/runtime/debug#SetCrashOutput) 함수를 사용하면 런타임이 치명적인 크래시 보고서를 작성할 대체 파일을 사용자가 지정할 수 있습니다.
이 함수는 `recover`를 명시적으로 사용하는 고루틴뿐만 아니라, 모든 예기치 않은 크래시에 대한 자동 보고 메커니즘을 구축하는 데 사용할 수 있습니다.

<!-- pacify TestCheckAPIFragments -->

#### [`runtime/pprof`](/pkg/runtime/pprof/)

`alloc`, `mutex`, `block`, `threadcreate` 및 `goroutine` 프로파일의 최대 스택 깊이가 32프레임에서 128프레임으로 상향되었습니다.

#### [`runtime/trace`](/pkg/runtime/trace/)

<!-- go.dev/issue/65319 -->
이제 런타임은 처리되지 않은 패닉(uncaught panic)으로 인해 프로그램이 충돌할 때 트레이스 데이터를 명시적으로 플러시(flush)합니다. 이는 트레이싱이 활성화된 상태에서 프로그램이 충돌하더라도 더 완전한 트레이스 데이터를 사용할 수 있음을 의미합니다.

#### [`slices`](/pkg/slices/)

<!-- see ../../3-iter.md -->

<!-- see ../../3-iter.md -->

[`Repeat`](/pkg/slices#Repeat) 함수는 제공된 슬라이스를 지정된 횟수만큼 반복하는 새 슬라이스를 반환합니다.

#### [`sync`](/pkg/sync/)

[`Map.Clear`](/pkg/sync#Map.Clear) 메서드는 모든 항목을 삭제하여 [`Map`](/pkg/sync#Map)을 비웁니다. 이는 `clear`와 유사하게 동작합니다.

#### [`sync/atomic`](/pkg/sync/atomic/)

<!-- Issue #61395 -->
새로운 [`And`](/pkg/sync/atomic#And) 및 [`Or`](/pkg/sync/atomic#Or) 연산자는 주어진 입력에 비트 단위 `AND` 또는 `OR`를 적용하며, 이전 값을 반환합니다.

#### [`syscall`](/pkg/syscall/)

이제 `syscall` 패키지에서 Windows의 [`WSAENOPROTOOPT`](/pkg/syscall#WSAENOPROTOOPT)를 정의합니다.

이제 Windows에서 [`GetsockoptInt`](/pkg/syscall#GetsockoptInt) 함수가 지원됩니다.

#### [`testing/fstest`](/pkg/testing/fstest/)

[`TestFS`](/pkg/testing/fstest#TestFS)는 이제 언랩(unwrap)이 가능한(메서드 `Unwrap() []error`를 통해) 구조화된 에러를 반환합니다. 이를 통해 [`errors.Is`](/pkg/errors#Is) 또는 [`errors.As`](/pkg/errors#As)를 사용하여 에러를 검사할 수 있습니다.

#### [`text/template`](/pkg/text/template/)

이제 템플릿에서 새로운 "else with" 액션을 지원하며, 이를 통해 일부 사용 사례에서 템플릿의 복잡성을 줄일 수 있습니다.

#### [`time`](/pkg/time/)

[`Parse`](/pkg/time#Parse) 및 [`ParseInLocation`](/pkg/time#ParseInLocation)은 이제 시간대 오프셋이 범위를 벗어난 경우 에러를 반환합니다.

Windows에서 [`Timer`](/pkg/time#Timer), [`Ticker`](/pkg/time#Ticker), 그리고 [`Sleep`](/pkg/time#Sleep)과 같이 고루틴을 휴면 상태로 만드는 함수들의 시간 해상도가 15.6ms에서 0.5ms로 개선되었습니다.

#### [`unicode/utf16`](/pkg/unicode/utf16/)

[`RuneLen`](/pkg/unicode/utf16#RuneLen) 함수는 rune의 UTF-16 인코딩에서 16비트 단어(word)의 수를 반환합니다. rune이 UTF-16으로 인코딩하기에 유효한 값이 아니면 -1을 반환합니다.

## 포트 (Ports) {#ports}

### Darwin {#darwin}

<!-- go.dev/issue/64207 -->
Go 1.22 릴리스 노트에서 [공지](go1.22#darwin)한 바와 같이,
Go 1.23은 macOS 11 Big Sur 이상 버전이 필요하며,
이전 버전에 대한 지원은 중단되었습니다.

### Linux {#linux}

<!-- go.dev/issue/67001 -->
Go 1.23은 Linux 커널 버전 2.6.32 이상을 요구하는 마지막 릴리스입니다. Go 1.24부터는 Linux 커널 버전 3.2 이상이 필요합니다.

### OpenBSD {#openbsd}

<!-- go.dev/issue/55999, CL 518629, CL 518630 -->
Go 1.23은 64비트 RISC-V(`GOOS=openbsd`, `GOARCH=riscv64`) 환경의 OpenBSD에 대한 실험적 지원을 추가합니다.

### ARM64 {#arm64}

<!-- go.dev/issue/60905, CL 559555 -->
Go 1.23에서는 컴파일 시 ARM64 아키텍처의 최소 대상 버전을 지정하는 새로운 `GOARM64` 환경 변수가 도입되었습니다. 허용되는 값은 `v8.{0-9}` 및 `v9.{0-5}`입니다. 이 값 뒤에는 대상 하드웨어에서 구현된 확장을 지정하는 옵션이 올 수 있습니다. 유효한 옵션은 `,lse`와 `,crypto`입니다.

`GOARM64` 환경 변수는 기본값이 `v8.0`입니다.

### RISC-V {#riscv}

<!-- go.dev/issue/61476, CL 541135 -->
Go 1.23에서는 컴파일 대상이 될 [RISC-V 사용자 모드 애플리케이션 프로필](https://github.com/riscv/riscv-profiles/blob/main/src/profiles.adoc)을 선택하는 새로운 `GORISCV64` 환경 변수가 도입되었습니다. 허용되는 값은 `rva20u64`와 `rva22u64`입니다.

`GORISCV64` 환경 변수의 기본값은 `rva20u64`입니다.

### Wasm {#wasm}

<!-- go.dev/issue/63718 -->
`GOROOT/misc/wasm`에 있는 `go_wasip1_wasm_exec` 스크립트에서 `wasmtime` 14.0.0 미만 버전에 대한 지원이 중단되었습니다.

<!-- 이 항목들은 완료되어 릴리스 노트의 적절한 위치로 이동되어야 합니다. -->

<!-- 다음 항목들은 검토가 필요하며, 해당하는 경우 Go 1.23 릴리스 노트에 언급되어야 합니다.

현재는 없습니다. 나중에 더 생길 수 있습니다.

<!-- 문서화해야 할까요? 아니면 하지 말아야 할까요? 변경 사항을 잘 아는 사람이 결정해야 합니다.

CL 359594 ("x/website/_content/ref/mod: document dotless module paths") - go.dev/issue/32819 ("cmd/go: document that module names without dots are reserved") 문제를 해결했으며, 수락된 제안인 go.dev/issue/37641 또한 언급했습니다.
CL 555075 ("x/tools/go/ssa: support range-over-func") - x/tools CL은 수락된 제안 https://go.dev/issue/66601 에 따라 x/tools/go/ssa 에 range-over-func 지원을 구현합니다. 이 특정 제안과 변경 사항은 Go 1.23 릴리스 노트에 별도로 언급할 필요는 없어 보이지만, 더 잘 아는 사람이 다시 한 번 검토해야 합니다.

<!-- Go 1.23 릴리스 노트에 언급될 필요는 없으나 relnote todo에 의해 선택된 항목들입니다. -->

CL 458895 - Go 1.16 마일스톤에서 승인된 cmd/go 제안 go.dev/issue/40728을 언급한 x/playground 수정 사항...
CL 582097 - 릴리스 노트 자체를 작업하는 x/build CL; 릴리스 노트가 필요하지 않음
CL 561935 - purego 태그를 사용하고, purego 태그를 문서화하기 위해 승인되었으나 구현되지 않은 제안 https://go.dev/issue/23172를 언급한 crypto CL; 릴리스 노트가 필요하지 않음
CL 568340 - time.Ticker.Reset의 일시적인 race 수정 (승인된 제안 https://go.dev/issue/33184를 통해 추가됨), 릴리스 노트가 필요하지 않은 것으로 보임
CL 562619 - go.dev에 최소 부트스트랩 버전을 문서화한 x/website CL이며, 승인된 제안 go.dev/issue/54265 및 go.dev/issue/44505를 언급함; 릴리스 노트가 필요하지 않음
CL 557055 - x/tools/go/ssa를 위해 승인된 제안 https://go.dev/issue/46941을 구현한 x/tools CL
CL 564275 - 승인된 제안 https://go.dev/issue/51473을 준비하며 테스트 데이터를 업데이트하는 x/tools CL; 해당 제안은 Go 1.23에서 구현되지 않았으므로 릴리스 노트가 필요하지 않음
CL 572535 - 더 많은 곳에서 "unix" 빌드 태그를 사용했으며, 승인된 제안 https://go.dev/issue/51572를 언급함; 릴리스 노트가 필요하지 않음
CL 555255 - x/tools/go/cfg를 위해 승인된 제안 https://go.dev/issue/53367을 구현하는 x/tools CL
CL 585216 - Go 1.22에서 새로 추가된 포트에 대해 다운로드가 생성되지 않는 버그를 수정했기 때문에 승인된 제안 https://go.dev/issue/56001을 언급하는 x/build CL; 이는 Go 1.23 릴리스 노트와 관련이 없음
CL 481062 - 승인된 제안 https://go.dev/issue/56102를 위한 예제를 추가함; 릴리스 노트가 필요하지 않음
CL 497195 - x/net/http2에서 승인된 제안 https://go.dev/issue/57893을 위한 4개 필드 중 하나를 추가하는 x/net CL; net/http와 관련이 없는 것으로 보이며 따라서 Go 1.23 릴리스 노트가 필요하지 않음
CL 463097, CL 568198 - x/net/websocket을 위해 승인된 제안 https://go.dev/issue/57953을 구현한 x/net CL들; 릴리스 노트 불필요
많은 x/net CL들 - x/net/quic에 QUIC 구현을 추가하기 위한 승인된 제안 https://go.dev/issue/58547 작업
CL 514775 - 승인된 제안 https://go.dev/issue/59488을 위한 성능 최적화를 구현함
CL 484995 - x/sys/unix API를 추가하기 위해 승인된 제안 https://go.dev/issue/59537을 구현하는 x/sys CL
CL 555597 - non-interface 타입에 대해 TypeFor(승인된 제안 https://go.dev/issue/60088에서 추가됨)를 최적화함; 릴리스 노트가 필요하지 않은 것으로 보임
몇몇 x/tools CL들 - 승인된 제안 https://go.dev/issue/60951에 따라 실험적인 golang.org/x/tools/cmd/getgo 도구를 deprecated 처리하고 삭제함; 릴리스되지 않은 변경 사항이며 Go 1.23 릴리스 노트의 범위에 해당하지 않음
많은 x/vuln CL들 - govulncheck에서 승인된 제안 https://go.dev/issue/61347 ("x/vuln: convert govulncheck output to sarif format")을 구현함
CL 516355 - x/crypto/ssh를 위해 승인된 제안 https://go.dev/issue/61447을 구현한 x/crypto CL; Go 1.23 릴리스 노트가 필요하지 않음
CL 559799 - Go 1.23 개발이 시작된 직후, Go 1.22 승인 제안 https://go.dev/issue/62039를 언급한 Go 1.22 릴리스 노트 수정 CL
CL 581555 - x/tools/go/aalysis를 위해 승인된 제안 https://go.dev/issue/62292를 언급한 x/tools CL; Go 1.23 릴리스 노트가 필요하지 않음
CL 578355 - GOARCH=wasm32를 추가하기 위한 승인된 제안 https://go.dev/issue/63131을 언급했으나, 해당 제안은 Go 1.23에서 구현되지 않았으므로 릴리스 노트가 필요하지 않음
CL 543335 - slices 패키지의 동작 변경 사항(승인된 제안 https://go.dev/issue/63393)을 x/exp/slices로 백포팅한 x/exp CL; Go 1.23 릴리스 노트가 필요하지 않음
CL 556820 - x/tools/go/analysis를 위해 승인된 제안 https://go.dev/issue/64548을 구현한 x/tools CL
CL 557056 - x/tools/go/packages를 위해 승인된 제안 https://go.dev/issue/64608을 구현한 x/tools CL
CL 558695 - x/crypto/ssh를 위해 승인된 제안 https://go.dev/issue/64962를 작업한 x/crypto CL
CL 572016 - x/tools/go/cfg를 위해 승인된 제안 https://go.dev/issue/65754를 구현한 x/tools CL
몇몇 x/tools CL들 - 승인된 제안 https://go.dev/issue/65880에 따라 golang.org/x/tools/cmd/guru 명령어를 태그 지정하고 삭제함; 릴리스되지 않은 변경 사항이며 Go 1.23 릴리스 노트의 범위에 해당하지 않음
CL 580076 - 승인된 제안 https://go.dev/issue/66315를 위해 모듈 정보를 전파하는 내부 cmd/go 변경 사항으로 보임; 릴리스 노트가 필요하지 않은 것으로 보임
CL 529816 - 승인된 제안 https://go.dev/issue/44251에 따라 'tests' vet 체크가 처음에 'go test' 스위트에 추가되었으나, CL 571695에서 롤백되었으며 2024-05-23 현재까지 다시 적용되지 않음; 현재 Go 1.23 릴리스 노트에 기록할 내용이 없음
CL 564035 - encoding/xml을 변경했으나, 변경 사항이 너무 파괴적이라 CL 570175에서 롤백되었으며 추적 이슈 go.dev/issue/65691이 다시 열림; Go 1.23 릴리스 노트에 기록할 내용이 없음
CL 587855 - 승인된 제안 https://go.dev/issue/60529의 이점을 시연함; 실제 변경 사항은 Go 1.23에서 발생하지 않으므로 릴리스 노트가 필요하지 않음
CL 526875 - x/crypto/ssh를 위해 승인된 제안 https://go.dev/issue/62518을 구현한 x/crypto CL
-->
