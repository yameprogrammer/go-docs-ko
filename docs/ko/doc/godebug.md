---
title: "Go, 하위 호환성, 그리고 GODEBUG"
layout: article
---

<!--
이 문서는 x/website가 아닌 Go 저장소에 보관됩니다.
특정 릴리스와 연결된 알려진 GODEBUG 설정의 전체 목록을 문서화하기 때문입니다.
-->

## 소개 {#intro}

하위 호환성에 대한 Go의 강조는 Go의 핵심 강점 중 하나입니다.
하지만 완전한 호환성을 유지할 수 없는 때가 있습니다.
만약 코드가 버그가 있는(보안 취약점이 포함된 경우 포함) 동작에 의존하고 있다면,
그 버그를 수정하는 것이 해당 코드를 망가뜨리게 됩니다.
새로운 기능 또한 유사한 영향을 미칠 수 있습니다.
HTTP 클라이언트에서 HTTP/2 사용을 활성화했을 때, 버그가 있는 HTTP/2 구현체를 사용하는 서버에 연결하는 프로그램들이 작동하지 않게 된 사례가 있습니다.
이러한 종류의 변경은 불가피하며,
[Go 1 호환성 규칙](/doc/go1compat)에 의해 허용됩니다.
그럼에도 불구하고, Go는 최신 툴체인을 사용하여 이전 코드를 컴파일하는 Go 개발자들이 이러한 변경으로 인해 받는 영향을 줄이기 위해 `GODEBUG`라는 메커니즘을 제공합니다.

GODEBUG 설정은 Go 프로그램의 특정 부분의 실행을 제어하는 `key=value` 쌍입니다.
환경 변수 `GODEBUG`에는 이러한 설정들의 쉼표로 구분된 목록을 담을 수 있습니다.
예를 들어, Go 프로그램이 다음과 같은 환경에서 실행 중인 경우:

`GODEBUG=http2client=0,http2server=0`

그러면 해당 Go 프로그램은 HTTP 클라이언트와 HTTP 서버 모두에서 기본적으로 HTTP/2 사용을 비활성화합니다.
`GODEBUG` 환경 변수에서 인식되지 않는 설정은 무시됩니다.
특정 프로그램에 대해 기본 `GODEBUG` 설정을 지정하는 것도 가능합니다(아래에서 설명).

Go 1 호환성에 의해 허용되지만 그럼에도 불구하고 일부 기존 프로그램을 중단시킬 수 있는 변경 사항을 준비할 때, 우리는 먼저 가능한 한 많은 기존 프로그램이 계속 작동하도록 변경 사항을 설계합니다.
나머지 프로그램들을 위해, 개별 프로그램이 이전 동작을 다시 선택할 수 있도록 하는 새로운 `GODEBUG` 설정을 정의합니다.
`GODEBUG` 설정을 추가하는 것이 불가능한 경우에는 추가하지 않을 수 있으나, 이는 매우 드문 경우여야 합니다.

호환성을 위해 추가된 `GODEBUG` 설정은 최소 2년(Go 릴리스 4회분) 동안 유지됩니다.
`http2client` 및 `http2server`와 같은 일부 설정은 훨씬 더 오래, 혹은 무기한으로 유지됩니다.

가능한 경우, 각 GODEBUG 설정에는 `/godebug/non-default-behavior/<name>:events`라는 이름의 [runtime/metrics](/pkg/runtime/metrics/) 카운터가 연결되어 있으며, 이는 해당 설정의 비기본값(non-default value)에 따라 특정 프로그램의 동작이 변경된 횟수를 기록합니다.

예를 들어, `GODEBUG=http2client=0`이 설정된 경우, `/godebug/non-default-behavior/http2client:events`는 프로그램이 HTTP/2 지원 없이 구성한 HTTP 트랜스포트의 수를 기록합니다.

## 기본 GODEBUG 값 {#default}

GODEBUG 설정이 환경 변수에 나열되어 있지 않은 경우, 그 값은 다음 세 가지 소스에서 도출됩니다:
프로그램을 빌드하는 데 사용된 Go 툴체인의 기본값,
`go.mod`에 기재된 Go 버전에 맞게 수정된 값,
그리고 프로그램 내의 명시적인 `//go:debug` 라인에 의해 재정의된 값입니다.

[GODEBUG History](#history)에서 각 Go 툴체인 버전의 정확한 기본값을 확인할 수 있습니다.
예를 들어, Go 1.21에서는 `panic(nil)` 허용 여부를 제어하는 `panicnil` 설정이 도입되었습니다.
기본값은 `panicnil=0`이며, 이 경우 `panic(nil)`은 런타임 에러가 됩니다.
`panicnil=1`을 사용하면 Go 1.20 및 이전 버전의 동작로 복원됩니다.

이전 버전의 Go 버전을 선언한 워크 모듈(work module)이나 워크스페이스(workspace)를 컴파일할 때, Go 툴체인은 해당 이전 Go 버전과 최대한 일치하도록 기본 설정을 수정합니다. 예를 들어, Go 1.21 툴체인이 프로그램을 컴파일할 때 워크 모듈의 `go.mod` 또는 워크스페이스의 `go.work`에 `go` `1.20`이라고 명시되어 있다면, 프로그램은 Go 1.21 대신 Go 1.20에 맞춰 `panicnil=1`을 기본값으로 사용합니다.

예외적으로, 보안 릴리스를 위해 도입된 GODEBUG는 모든 버전에 새로운 동작이 적용됩니다.

GODEBUG 기본값을 설정하는 이 방법은 Go 1.21에서 처음 도입되었기 때문에, Go 1.20보다 이전 버전의 Go를 명시한 프로그램들은 해당 이전 버전이 아닌 Go 1.20에 맞춰 구성됩니다.

이러한 기본 설정을 재정의하기 위해, Go 1.23부터 작업 모듈의 `go.mod` 또는 워크스페이스의 `go.work` 파일에 하나 이상의 `godebug` 라인을 나열할 수 있습니다.

godebug (
		default=go1.21
		panicnil=1
		asynctimerchan=0
	)

특수 키 `default`는 지정되지 않은 설정을 가져올 Go 버전을 나타냅니다. 이를 통해 모듈의 Go 언어 버전과는 별도로 GODEBUG 기본값을 설정할 수 있습니다.

이 예시에서 프로그램은 Go 1.21 시맨틱을 요청하고, 이어서 Go 1.21 이전의 이전 `panic(nil)` 동작과 Go 1.23의 새로운 `asynctimerchan=0` 동작을 요청하고 있습니다.

`godebug` 지시어는 워크 모듈의 `go.mod` 파일만 참조합니다.
필수 종속성 모듈에 포함된 모든 지시어는 무시됩니다.
인식되지 않는 설정을 가진 `godebug`를 나열하는 것은 오류입니다.
(Go 1.23보다 오래된 툴체인은 `godebug`를 전혀 이해하지 못하므로 모든 `godebug` 라인을 거부합니다.) 워크스페이스를 사용하는 경우, `go.mod` 파일의 `godebug` 지시어는 무시되며 대신 `go.work`에서 `godebug` 지시어를 참조합니다.

`go` 및 `godebug` 라인의 기본값은 빌드되는 모든 메인 패키지에 적용됩니다. 더 세밀한 제어를 위해, Go 1.21부터는 메인 패키지의 소스 파일 상단(`package` 문 이전)에 하나 이상의 `//go:debug` 지시문을 포함할 수 있습니다.
이전 예제의 `godebug` 라인은 다음과 같이 작성될 수 있습니다:

//go:debug default=go1.21
	//go:debug panicnil=1
	//go:debug asynctimerchan=0

Go 1.21부터 Go 툴체인은 인식되지 않는 GODEBUG 설정이 포함된 `//go:debug` 지시문을 잘못된 프로그램으로 처리합니다.
특정 설정에 대해 `//go:debug` 라인이 두 개 이상인 프로그램 또한 잘못된 것으로 처리됩니다.
(이전 버전의 툴체인은 `//go:debug` 지시문을 완전히 무시합니다.)

main 패키지로 컴파일될 기본값들은 다음 명령어로 확인할 수 있습니다:

`go list -f '{{.DefaultGODEBUG}}' my/main/package`

기본 Go 툴체인 기본값과 다른 차이점만 보고됩니다.

패키지를 테스트할 때, `*_test.go` 파일에 있는 `//go:debug` 라인은 테스트의 메인 패키지를 위한 지시어로 처리됩니다. 그 외의 다른 문맥에서 `//go:debug` 라인은 툴체인에 의해 무시되며, `go` `vet`은 이러한 라인을 잘못 배치된 것으로 보고합니다.

## GODEBUG 이력 {#history}

이 섹션에서는 호환성 이유로 각 Go 주요 릴리스에서 도입되거나 제거된 GODEBUG 설정을 문서화합니다.
패키지나 프로그램은 내부 디버깅 목적으로 추가 설정을 정의할 수 있습니다.
예를 들어, [runtime 문서](/pkg/runtime#hdr-Environment_Variables)와 [go command 문서](/cmd/go#hdr-Build_and_test_caching)를 참조하십시오.

### Go 1.28

Go 1.28에서는 Range 헤더의 최대 범위(range) 수를 제한하기 위해 [`net/http.FileServer`](/pkg/net/http#FileServer), [`net/http.FileServerFS`](/pkg/net/http#FileServerFS), [`net/http.ServeContent`](/pkg/net/http#ServeContent), [`net/http.ServeFile`](/pkg/net/http#ServeFile), 및 [`net/http.ServeFileFS`](/pkg/net/http#ServeFileFS)가 변경되었습니다. 헤더의 범위 수가 새로운 `httpservecontentmaxranges` 설정값을 초과하면 해당 헤더는 무시됩니다. 기본값은 `httpservecontentmaxranges=200`입니다. `httpservecontentmaxranges=0`으로 설정하면 제한이 비활성화됩니다. 서비스 거부(DoS) 공격을 방지하기 위해, 이 설정과 기본값은 Go 1.27.2 및 Go 1.26.9 버전으로 백포트되었습니다.

Go 1.28에서는 `net.IPMask`, `net.IPNet`, `net.HardwareAddr` 타입의 텍스트 마샬링(marshaling) 가독성 여부를 제어하는 새로운 `netmarshal` 설정이 추가되었습니다. `netmarshal=0` 값은 이러한 타입들을 읽기 어려운 base64 인코딩으로 JSON 인코딩합니다. `netmarshal=1` 값은 IP 주소와 같이 읽기 쉬운 버전을 사용합니다.

Go 1.28 및 1.29 버전에서 기본값은 `netmarshal=0`으로 유지됩니다. 이는 해당 버전에서 생성된 JSON 또는 기타 마샬링된 데이터를 이전 버전의 Go에서도 읽을 수 있도록 하기 위함입니다.

Go 1.30에서는 기본값이 `netmarshal=1`로 변경될 예정입니다. Go 1.28 및 모든 향후 릴리스는 데이터를 읽을 때 기존 인코딩과 새로운 인코딩을 모두 지원합니다. 이 설정은 향후 Go 릴리스(가장 빠른 경우 Go 1.34)에서 제거될 수 있습니다.

### Go 1.27

Go 1.27에서는 [Go 1.22](#go-122) 섹션에 언급된 바와 같이 `gotypesalias` 설정이 제거되었습니다.

Go 1.27에서는 [Go 1.22](#go-122) 섹션에 언급된 대로 `tlsunsafeekm` 설정이 제거되었습니다.

[Go 1.22](#go-122) 섹션에 언급된 바와 같이, Go 1.27에서 `tlsrsakex` 설정이 제거되었습니다.

Go 1.27에서는 [Go 1.23](#go-123) 섹션에 언급된 바와 같이 `tls3des` 설정이 제거되었습니다.

Go 1.27에서는 [Go 1.22](#go-122) 섹션에 언급된 대로 `tls10server` 설정이 제거되었습니다.

[Go 1.23](#go-123) 섹션에 언급된 바와 같이, Go 1.27에서 `x509keypairleaf` 설정이 제거되었습니다.

[Go 1.23](#go-123) 섹션에 언급된 바와 같이, Go 1.27에서는 `asynctimerchan` 설정이 제거되었습니다.

Go 1.27에서는 `html/template`이 HTML meta 태그의 content 속성 중 `url=` 부분에 있는 URL을 이스케이프할지 여부를 제어하는 새로운 `htmlmetacontenturlescape` 설정이 추가되었습니다. 기본값인 `htmlmetacontentescape=1`은 URL이 이스케이프되도록 합니다. `htmlmetacontentescape=0`으로 설정하면 이 동작이 비활성화됩니다. 콘텐츠 주입 공격(content injection attacks)을 방지하기 위해, 이 설정과 기본값은 Go 1.25.8 및 Go 1.26.1 버전으로 백포트되었습니다.

Go 1.27에서는 `tracebacklabels`([Go 1.26](#go-126)에서 추가됨)의 기본값이 `1`로 변경됩니다. 고루틴 레이블에 트레이스백(traceback)에서 제공되어서는 안 되는 민감한 정보가 포함될 경우를 대비하여, 이 옵트아웃(opt-out) 설정은 무기한 유지될 예정입니다.

Go 1.27에서는 `SSL_CERT_FILE` 또는 `SSL_CERT_DIR`이 설정되었을 때, Windows 및 Darwin에서 `crypto/x509`가 디스크에서 루트 인증서를 로드할지 여부를 제어하는 새로운 `x509sslcertoverrideplatform` 설정이 추가되었습니다. 기본값인 `x509sslcertoverrideplatform=1`은 이러한 환경 변수가 설정되었을 때 루트 인증서를 디스크에서 로드하게 합니다. `x509sslcertoverrideplatform=0`으로 설정하면 이 동작이 비활성화되며, 환경 변수를 따르는 대신 플랫폼 인증서 저장소(platform certificate store)를 사용하게 됩니다. 이 설정은 Go 1.31에서 제거될 예정입니다.

Go 1.27에 `fips140ems` 설정이 추가되었으며, 이 값을 `0`으로 설정하면 FIPS 140-3 모드에서 Extended Master Secret 강제 적용이 비활성화됩니다. 기본 동작에는 변경 사항이 없습니다. 이 설정은 Go 1.26.6 및 Go 1.25.13으로 백포트되었습니다. 저희는 Go 1.31에서 이 설정을 제거할 계획입니다.

### Go 1.26

Go 1.26에서는 `net/http`가 HTTP 헤더를 파싱할 때 허용하는 쿠키의 최대 개수를 제어하는 새로운 `httpcookiemaxnum` 설정이 추가되었습니다. 헤더에 포함된 쿠키의 수가 `httpcookiemaxnum`에 설정된 수를 초과하면 쿠키 파싱이 조기에 실패합니다. 기본값은 `httpcookiemaxnum=3000`입니다. `httpcookiemaxnum=0`으로 설정하면 쿠키 파싱 시 무제한의 쿠키를 허용하게 됩니다. 서비스 거부(DoS) 공격을 방지하기 위해, 이 설정과 기본값은 Go 1.25.2 및 Go 1.24.8 버전으로 백포트되었습니다.

Go 1.26에는 `net/url`이 URL 인코딩된 쿼리 문자열을 파싱할 때 허용하는 쿼리 매개변수의 최대 수를 제어하는 새로운 `urlmaxqueryparams` 설정이 추가되었습니다. 매개변수의 수가 `urlmaxqueryparams`에 설정된 수를 초과하면 파싱이 조기에 실패합니다. 기본값은 `urlmaxqueryparams=10000`입니다. `urlmaxqueryparams=0`으로 설정하면 제한이 비활성화됩니다. 서비스 거부(DoS) 공격을 방지하기 위해, 이 설정과 기본값은 Go 1.25.6 및 Go 1.24.12 버전으로 백포트되었습니다.

Go 1.26에서는 `net/url.Parse`가 대괄호로 둘러싸인 IPv6 주소 이외의 위치에 콜론이 포함된 잘못된 호스트 이름을 허용할지 여부를 제어하는 새로운 `urlstrictcolons` 설정이 추가되었습니다. 기본값인 `urlstrictcolons=1`은 `http://localhost:1:2` 또는 `http://::1/`와 같은 URL을 거부합니다. 콜론은 `http://[::1]/`와 같이 대괄호로 둘러싸인 IPv6 주소의 일부로는 허용됩니다. Go 1.27에서는 이 검증 범위를 `http` 및 `https` URL로 제한하여, 다른 스킴(scheme)을 가진 URL에는 이 설정이 영향을 미치지 않습니다.

Go 1.26에서는 두 가지의 추가적인 양자 내성 키 교환 메커니즘인 SecP256r1MLKEM768 및 SecP384r1MLKEM1024가 활성화되었습니다. 기본 설정은 [`tlssecpmlkem` 설정](/pkg/crypto/tls/#Config.CurvePreferences)을 사용하여 되돌릴 수 있습니다.

Go 1.26에서는 `runtime/pprof` 패키지를 통해 설정된 고루틴 레이블(goroutine labels)의 포함 여부를 제어하는 새로운 `tracebacklabels` 설정이 추가되었습니다. `tracebacklabels=1`로 설정하면 런타임 트레이스백(runtime tracebacks)의 고루틴 상태 헤더와 `debug=2` runtime/pprof 스택 덤프에 이러한 키/값 쌍이 포함됩니다. 이 형식은 향후 변경될 수 있습니다. (go.dev/issue/76349 참조)

Go 1.26에는 대부분의 `crypto/...` API가 랜덤 `io.Reader` 파라미터를 무시할지 여부를 제어하는 새로운 `cryptocustomrand` 설정이 추가되었습니다. Go 1.26에서 이 설정의 기본값은 `cryptocustomrand=0`이며, 이 경우 랜덤 파라미터가 무시됩니다. `cryptocustomrand=1`을 사용하면 Go 1.26 이전의 동작으로 되돌아갑니다.

### Go 1.25

Go 1.25에서는 Go 런타임이 OS 익명 메모리 매핑(anonymous memory mappings)에 그 용도에 관한 컨텍스트를 주석으로 달지 여부를 제어하는 새로운 `decoratemappings` 설정이 추가되었습니다. 이러한 주석은 `/proc/self/maps` 및 `/proc/self/smaps`에 "[anon: Go: ...]" 형태로 나타납니다. 이 설정은 Linux에서만 사용됩니다. Go 1.25의 기본값은 `decoratemappings=1`이며, 이를 통해 주석 기능이 활성화됩니다. `decoratemappings=0`을 사용하면 Go 1.25 이전의 동작으로 되돌아갑니다. 이 설정은 프로그램 시작 시점에 고정되며, 프로그램이 시작된 후 `GODEBUG` 환경 변수를 변경하여 수정할 수 없습니다.

Go 1.25에는 Go 명령어가 파일을 임베딩할 때 일반 파일로 연결되는 심볼릭 링크를 따라갈지 여부를 제어하는 새로운 `embedfollowsymlinks` 설정이 추가되었습니다.
기본값인 `embedfollowsymlinks=0`은 심볼릭 링크를 따라가는 것을 허용하지 않습니다. `embedfollowsymlinks=1`은 심볼릭 링크를 따라가는 것을 허용합니다.

Go 1.25에는 Go 런타임이 기본 `GOMAXPROCS`를 설정할 때 cgroup CPU 제한을 고려할지 여부를 제어하는 새로운 `containermaxprocs` 설정이 추가되었습니다. 기본값인 `containermaxprocs=1`은 총 논리 CPU 수 및 CPU affinity와 더불어 cgroup 제한을 사용합니다. `containermaxprocs=0`은 cgroup 제한 고려를 비활성화합니다. 이 설정은 Linux에만 영향을 미칩니다.

Go 1.25에는 Go 런타임이 새로운 CPU affinity 또는 cgroup 제한에 따라 `GOMAXPROCS`를 주기적으로 업데이트할지 여부를 제어하는 새로운 `updatemaxprocs` 설정이 추가되었습니다. 기본값인 `updatemaxprocs=1`은 주기적 업데이트를 활성화하며, `updatemaxprocs=0`은 주기적 업데이트를 비활성화합니다.

Go 1.25은 RFC 9155에 따라 TLS 1.2에서 SHA-1 서명 알고리즘을 비활성화했습니다.
`tlssha1=1` 설정을 사용하여 기본값을 되돌릴 수 있습니다.

Go 1.25에서는 `crypto/x509.CreateCertificate`에서 누락된 `SubjectKeyId`를 채우기 위해 SHA-256을 사용하도록 변경되었습니다. `x509sha256skid=0` 설정을 통해 SHA-1로 되돌릴 수 있습니다.

Go 1.25에서 런타임 내부 락(lock)에 대한 경합 보고(contention reports)의 시맨틱이 수정되었으며, 이에 따라 [`runtimecontentionstacks` 설정](/pkg/runtime#hdr-Environment_Variables)이 제거되었습니다.

Go 1.25(Go 1.25 RC 2부터 시작)에서는 VCS 인젝션 공격에 대한 우려로 인해 여러 개의 VCS가 감지될 때 빌드 정보 스탬핑(build information stamping) 기능이 비활성화되었습니다. 이 동작과 설정은 Go 1.24.5 및 Go 1.23.11에도 백포트되었습니다. 이 동작은 `allowmultiplevcs=1` 설정을 통해 다시 활성화할 수 있습니다.

### Go 1.24

Go 1.24에는 Go Cryptographic Module이 FIPS 140-3 모드로 작동할지 여부를 제어하는 새로운 `fips140` 설정이 추가되었습니다.
가능한 값은 다음과 같습니다:
- "off": FIPS 140-3 모드에 대한 특별한 지원을 하지 않습니다. 이것이 기본값입니다.
- "on": Go Cryptographic Module이 FIPS 140-3 모드로 작동합니다.
- "only": "on"과 유사하지만, FIPS 140-3에서 승인되지 않은 암호화 알고리즘은 에러를 반환하거나 패닉(panic)을 발생시킵니다.
더 자세한 정보는 [FIPS 140-3 Compliance](/doc/security/fips140)를 참조하십시오.
이 설정은 프로그램 시작 시점에 고정되며, 프로그램이 시작된 후에는 `GODEBUG` 환경 변수를 변경하여 수정할 수 없습니다.

Go 1.24에서는 전역 [`math/rand.Seed`](/pkg/math/rand/#Seed)가 아무 작업도 수행하지 않는 no-op으로 변경되었습니다. 이 동작은 `randseednop` 설정으로 제어됩니다.
Go 1.24에서는 기본값이 `randseednop=1`입니다.
`randseednop=0`을 사용하면 Go 1.24 이전의 동작으로 되돌아갑니다.

Go 1.24에서 `multipathtcp` 설정에 새로운 값들이 추가되었습니다.
`multipathtcp`에 사용할 수 있는 값은 다음과 같습니다:
- "0": 기본적으로 dialer 및 listener에서 MPTCP 비활성화
- "1": 기본적으로 dialer 및 listener에서 MPTCP 활성화
- "2": 기본적으로 listener에서만 MPTCP 활성화
- "3": 기본적으로 dialer에서만 MPTCP 활성화

Go 1.24부터는 `multipathtcp="2"`가 기본값이 되며, 이에 따라 리스너(listeners)에서 기본적으로 활성화됩니다. `multipathtcp="0"`을 사용하면 Go 1.24 이전의 동작 방식으로 되돌아갑니다.

Go 1.24에서는 `go test -json`의 동작이 변경되어 빌드 오류를 텍스트 대신 JSON으로 출력합니다.
이 새로운 JSON 이벤트들은 새로운 `Action` 값으로 구분되지만, 이러한 이벤트에 유연하게 대응하지 못하는 CI 시스템에서는 여전히 문제가 발생할 수 있습니다.
이 동작은 `gotestjsonbuildtext` 설정으로 제어할 수 있습니다.
`gotestjsonbuildtext=1`을 사용하면 1.23 버전의 동작으로 복원됩니다.
이 설정은 향후 릴리스(빠르면 Go 1.28)에서 제거될 예정입니다.

Go 1.24에서는 [`crypto/rsa`](/pkg/crypto/rsa)가 RSA 키의 최소 길이를 1024비트로 요구하도록 변경되었습니다. 이 동작은 `rsa1024min` 설정으로 제어할 수 있습니다. `rsa1024min=0`을 사용하면 Go 1.23의 동작으로 복구됩니다.

Go 1.24에서는 [`crypto/subtle`](/pkg/crypto/subtle) 패키지에서 플랫폼별 데이터 독립적 타이밍(Data Independent Timing, DIT) 모드를 활성화하는 메커니즘이 도입되었습니다. 이 모드는 `dataindependenttiming` 설정을 통해 프로그램 전체에 대해 활성화할 수 있습니다. Go 1.24에서 기본값은 `dataindependenttiming=0`입니다. `dataindependenttiming`이 설정되지 않은 경우 Go 1.23과 비교하여 기본 동작에 변경 사항은 없습니다.

`dataindependenttiming=1`을 사용하면 전체 Go 프로그램에 대해 DIT 모드가 활성화됩니다. 활성화된 상태에서 Go에서 C를 호출하면 DIT가 활성화됩니다. 또한 활성화된 상태에서 C에서 Go 코드를 호출하면 DIT가 활성화되며, Go 코드 진입 시 DIT가 활성화되어 있지 않았다면 C로 돌아가기 전에 DIT를 비활성화합니다.

이 기능은 현재 arm64 프로그램에만 영향을 미칩니다. 다른 모든 플랫폼에서는 아무런 동작을 수행하지 않습니다(no-op).

Go 1.24에서 `x509sha1` 설정이 제거되었습니다. `crypto/x509`는 더 이상 SHA-1 기반 서명 알고리즘을 사용하는 인증서의 서명 검증을 지원하지 않습니다.

Go 1.24에서는 [`x509usepolicies` 설정](/pkg/crypto/x509/#CreateCertificate)의 기본값이 `0`에서 `1`로 변경됩니다. 이제 인증서를 마샬링할 때, 기본적으로 [`Certificate.PolicyIdentifiers`](/pkg/crypto/x509/#Certificate.PolicyIdentifiers) 필드 대신 [`Certificate.Policies`](/pkg/crypto/x509/#Certificate.Policies) 필드에서 정책을 가져옵니다.

Go 1.24에서는 양자 내성 키 교환 메커니즘인 `X25519MLKEM768`이 기본적으로 활성화되었습니다. 이 기본 설정은 [`tlsmlkem` 설정](/pkg/crypto/tls/#Config.CurvePreferences)을 통해 되돌릴 수 있습니다. 이는 대형 레코드를 올바르게 처리하지 못해 핸드셰이크 도중 타임아웃이 발생하는 버그가 있는 TLS 서버를 다룰 때 유용할 수 있습니다 (참조: [TLS post-quantum TL;DR fail](https://tldr.fail/)).

또한 Go 1.24에서는 `X25519Kyber768Draft00` 및 Go 1.23의 `tlskyber` 설정이 제거되었습니다.

Go 1.24부터 [`ParsePKCS1PrivateKey`](/pkg/crypto/x509/#ParsePKCS1PrivateKey)가 인코딩된 개인 키 내의 CRT 매개변수를 사용하고 검증하도록 변경되었습니다. 이 동작은 `x509rsacrt` 설정을 통해 제어할 수 있습니다. `x509rsacrt=0`을 사용하면 Go 1.23의 동작으로 복구됩니다.

### Go 1.23

Go 1.23에서는 `time` 패키지에서 생성하는 채널이 버퍼가 없는(동기식) 채널로 변경되었습니다. 이로 인해 [`Timer.Stop`](/pkg/time/#Timer.Stop) 및 [`Timer.Reset`](/pkg/time/#Timer.Reset) 메서드의 결과를 올바르게 사용하는 것이 훨씬 쉬워졌습니다.
[`asynctimerchan` 설정](/pkg/time/#NewTimer)을 통해 이 변경 사항을 비활성화할 수 있습니다.
이 변경 사항에 대한 런타임 메트릭은 제공되지 않습니다.
이 설정은 Go 1.27에서 제거될 예정입니다.

Go 1.23에서는 `winsymlink` 설정으로 제어할 수 있는 재분석 지점(reparse points)에 대해 [`os.Lstat`](/pkg/os#Lstat) 및 [`os.Stat`](/pkg/os#Stat)이 보고하는 모드 비트가 변경되었습니다.
Go 1.23(`winsymlink=1`)부터는 마운트 지점에 더 이상 [`os.ModeSymlink`](/pkg/os#ModeSymlink)가 설정되지 않으며, 심볼릭 링크, Unix 소켓 또는 중복 제거 파일(dedup files)이 아닌 재분석 지점에는 이제 항상 [`os.ModeIrregular`](/pkg/os#ModeIrregular)가 설정됩니다. 이러한 변경의 결과로, [`filepath.EvalSymlinks`](/pkg/path/filepath#EvalSymlinks)는 더 이상 마운트 지점을 평가하지 않으며, 이는 많은 불일치와 버그의 원인이었습니다.
이전 버전(`winsymlink=0`)에서는 마운트 지점이 심볼릭 링크로 처리되었으며, 기본값이 아닌 [`os.ModeType`](/pkg/os#ModeType) 비트(예: [`os.ModeDir`](/pkg/os#ModeDir))를 가진 다른 재분석 지점에는 `ModeIrregular` 비트가 설정되지 않았습니다.

Go 1.23에서는 [`os.Readlink`](/pkg/os#Readlink) 및 [`filepath.EvalSymlinks`](/pkg/path/filepath#EvalSymlinks)가 항상 가능하지는 않았던 볼륨의 드라이브 문자 정규화 시도를 피하도록 변경되었습니다.
이 동작은 `winreadlinkvolume` 설정으로 제어됩니다.
Go 1.23의 경우, 기본값은 `winreadlinkvolume=1`입니다.
이전 버전의 기본값은 `winreadlinkvolume=0`입니다.

Go 1.23에서는 실험적인 양자 내성 키 교환 메커니즘인 `X25519Kyber768Draft00`이 기본적으로 활성화되었습니다. 이 기본 설정은 [`tlskyber` 설정](/pkg/crypto/tls/#Config.CurvePreferences)을 통해 되돌릴 수 있습니다. 이는 큰 레코드를 올바르게 처리하지 못해 핸드셰이크 중 타임아웃이 발생하는 결함이 있는 TLS 서버를 다룰 때 유용할 수 있습니다 (참조: [TLS post-quantum TL;DR fail](https://tldr.fail/)).

Go 1.23에서는 [crypto/x509.ParseCertificate](/pkg/crypto/x509/#ParseCertificate)의 동작이 변경되어 음수 시리얼 번호를 거부합니다. 이 변경 사항은 [`x509negativeserial` 설정](/pkg/crypto/x509/#ParseCertificate)을 통해 되돌릴 수 있습니다.

Go 1.23부터 `html/template`에서 ECMAScript 6 템플릿 리터럴(template literals)에 대한 지원이 기본적으로 다시 활성화되었습니다.
[`jstmpllitinterp` 설정](/pkg/html/template#hdr-Security_Model)은 더 이상 아무런 영향을 주지 않습니다.

Go 1.23에서는 명시적으로 설정되지 않았을 때 클라이언트와 서버에서 사용하는 기본 TLS cipher suites가 변경되었으며, 3DES cipher suites가 제거되었습니다. 기본 설정은 [`tls3des` 설정](/pkg/crypto/tls/#Config.CipherSuites)을 통해 되돌릴 수 있습니다.
이 설정은 Go 1.27에서 제거될 예정입니다.

Go 1.23에서는 [`tls.X509KeyPair`](/pkg/crypto/tls#X509KeyPair) 및 [`tls.LoadX509KeyPair`](/pkg/crypto/tls#LoadX509KeyPair)의 동작이 변경되어, 반환되는 [`tls.Certificate`](/pkg/crypto/tls#Certificate)의 `Leaf` 필드를 채우도록 설정되었습니다.

이 동작은 `x509keypairleaf` 설정으로 제어됩니다. Go 1.23의 기본값은 `x509keypairleaf=1`이며, 이전 버전의 기본값은 `x509keypairleaf=0`입니다.

이 설정은 Go 1.27에서 제거될 예정입니다.

Go 1.23에서는 에러를 반환할 때 Cache-Control, Content-Encoding, Etag, Last-Modified 헤더를 제거하도록 [`net/http.ServeContent`](/pkg/net/http#ServeContent), [`net/http.ServeFile`](/pkg/net/http#ServeFile), [`net/http.ServeFS`](/pkg/net/http#ServeFS)가 변경되었습니다. 이 동작은 [`httpservecontentkeepheaders` 설정](/pkg/net/http#ServeContent)으로 제어됩니다. `httpservecontentkeepheaders=1`을 사용하면 Go 1.23 이전의 동작으로 복원됩니다.

### Go 1.22

Go 1.22에서는 TLS 핸드셰이크에 사용할 수 있는 최대 허용 RSA 키 크기를 제어하기 위해 [`tlsmaxrsasize` 설정](/pkg/crypto/tls#Conn.Handshake)으로 조절 가능한 제한 사항이 추가되었습니다. 기본값은 `tlsmaxrsasize=8192`이며, RSA 키를 8192비트로 제한합니다. 서비스 거부(DoS) 공격을 방지하기 위해, 이 설정과 기본값은 Go 1.19.13, Go 1.20.8 및 Go 1.21.1로 백포트되었습니다.

Go 1.22부터는 `net/http` 클라이언트 또는 서버가 읽는 요청이나 응답의 `Content-Length` 헤더가 비어 있을 경우 이를 오류로 처리합니다.
이 동작은 `httplaxcontentlength` 설정으로 제어됩니다.

Go 1.22에서는 `ServeMux`가 확장 패턴을 수용하고, 패턴과 요청 경로 모두를 세그먼트별로 언이스케이프(unescape)하도록 동작이 변경되었습니다. 이 동작은 [`httpmuxgo121` 설정](/pkg/net/http/#ServeMux)을 통해 제어할 수 있습니다.

Go 1.22에서는 [타입 별칭](/ref/spec#Type_declarations)(type aliases)을 명시적으로 표현하기 위해 [go/types](/pkg/go/types)에 [Alias type](/pkg/go/types#Alias)이 추가되었습니다.
타입 체커가 `Alias` 타입을 생성할지 여부는 [`gotypesalias` 설정](/pkg/go/types#Alias)으로 제어됩니다.
Go 1.22의 기본값은 `gotypesalias=0`입니다.
Go 1.23부터는 `gotypesalias=1`이 기본값이 됩니다.
이 설정은 Go 1.27에서 제거될 예정입니다.

Go 1.22에서 서버와 클라이언트 모두에서 지원하는 기본 최소 TLS 버전이 TLS 1.2로 변경되었습니다. [`tls10server` 설정](/pkg/crypto/tls/#Config)을 사용하여 기본값을 TLS 1.0으로 되돌릴 수 있습니다.
이 설정은 Go 1.27에서 제거될 예정입니다.

Go 1.22에서는 클라이언트와 서버에서 명시적으로 설정하지 않았을 때 사용하는 기본 TLS 사이퍼 스위트(cipher suites)가 변경되었으며, RSA 기반 키 교환을 사용하는 사이퍼 스위트들이 제거되었습니다. 기본 설정은 [`tlsrsakex` 설정](/pkg/crypto/tls/#Config)을 사용하여 되돌릴 수 있습니다. 이 설정은 Go 1.27에서 제거될 예정입니다.

Go 1.22에서는 연결이 TLS 1.3과 Extended Master Secret(Go 1.21에서 구현됨)을 모두 지원하지 않는 경우 [`ConnectionState.ExportKeyingMaterial`](/pkg/crypto/tls/#ConnectionState.ExportKeyingMaterial) 기능이 비활성화되었습니다. 이 기능은 [`tlsunsafeekm` 설정](/pkg/crypto/tls/#ConnectionState.ExportKeyingMaterial)을 통해 다시 활성화할 수 있습니다. 이 설정은 Go 1.27에서 제거될 예정입니다.

Go 1.22에서는 런타임이 Linux의 투명한 거대 페이지(transparent huge pages)와 상호 작용하는 방식이 변경되었습니다.
특히, 일반적인 기본 Linux 커널 설정으로 인해 상당한 메모리 오버헤드가 발생할 수 있으며, Go 1.22는 더 이상 이 기본 설정에 대한 우회 처리를 수행하지 않습니다.
커널 설정을 조정하지 않고 이 문제를 해결하려면, [`disablethp` 설정](/pkg/runtime#hdr-Environment_Variables)을 통해 Go 메모리에 대한 투명한 거대 페이지 기능을 비활성화할 수 있습니다.
이 동작은 Go 1.21.1로 백포트되었으나, 해당 설정은 Go 1.21.6부터 사용할 수 있습니다.
이 설정은 향후 릴리스에서 제거될 수 있으며, 이 문제의 영향을 받는 사용자는 [GC 가이드](/doc/gc-guide#Linux_transparent_huge_pages)의 권장 사항에 따라 Linux 설정을 조정하거나, 투명한 거대 페이지 기능을 완전히 비활성화하는 Linux 배포판으로 전환해야 합니다.

Go 1.22에서는 런타임 내부 락(runtime-internal locks)에 대한 경합(contention) 정보가 [`mutex` profile](/pkg/runtime/pprof#Profile)에 추가되었습니다. 이러한 락에 대한 경합은 항상 `runtime._LostContendedRuntimeLock`으로 보고됩니다. 런타임 락의 전체 스택 트레이스는 [`runtimecontentionstacks` 설정](/pkg/runtime#hdr-Environment_Variables)을 통해 활성화할 수 있습니다. 이러한 스택 트레이스는 표준과 다른 시맨틱을 가지므로, 자세한 내용은 설정 문서를 참조하십시오.

Go 1.22에서는 31비트보다 큰 구성 요소를 가진 인증서 정책 OID를 지원하는 새로운 [`crypto/x509.Certificate`](/pkg/crypto/x509/#Certificate) 필드인 [`Policies`](/pkg/crypto/x509/#Certificate.Policies)가 추가되었습니다. 기본적으로 이 필드는 파싱 중에 정책 OID가 채워질 때만 사용되며, 마샬링(marshaling) 중에는 사용되지 않습니다. [`x509usepolicies` 설정](/pkg/crypto/x509/#CreateCertificate)을 사용하면 기존의 `PolicyIdentifiers` 필드 대신 이 필드를 사용하여 더 큰 OID를 마샬링할 수 있습니다.

### Go 1.21

Go 1.21부터는 [`panicnil` 설정](/pkg/builtin/#panic)에 의해 제어되며, nil 인터페이스 값으로 `panic`을 호출하는 것이 런타임 에러가 되었습니다.

Go 1.21부터는 [`jstmpllitinterp` 설정](/pkg/html/template#hdr-Security_Model)에 의해 제어되며, ECMAScript 6 템플릿 리터럴 내부에 `html/template` 액션이 나타나는 것이 오류로 처리됩니다. 이 동작은 Go 1.19.8+ 및 Go 1.20.3+ 버전으로 백포트되었습니다.

Go 1.21에서는 MIME 헤더와 multipart 폼의 최대 개수에 대한 제한이 도입되었으며, 이는 각각 [`multipartmaxheaders` 및 `multipartmaxparts` 설정](/pkg/mime/multipart#hdr-Limits)으로 제어됩니다.
이 동작은 Go 1.19.8+ 및 Go 1.20.3+ 버전으로 백포트되었습니다.

Go 1.21에서는 Multipath TCP 지원이 추가되었으나, 애플리케이션에서 명시적으로 요청한 경우에만 사용됩니다. 이 동작은 [`multipathtcp` 설정](/pkg/net#Dialer.SetMultipathTCP)을 통해 제어할 수 있습니다.

이 설정들을 제거할 계획은 없습니다.

### Go 1.20

Go 1.20에서는 [`tarinsecurepath` 설정](/pkg/archive/tar/#Reader.Next)과 [`zipinsecurepath` 설정](/pkg/archive/zip/#NewReader)을 통해 tar 및 zip 아카이브의 안전하지 않은 경로를 거부하는 기능을 도입했습니다.
이 설정들의 기본값은 `tarinsecurepath=1` 및 `zipinsecurepath=1`이며, 이는 이전 버전의 Go 동작을 유지하기 위함입니다.
향후 Go 버전에서는 기본값이 `tarinsecurepath=0` 및 `zipinsecurepath=0`으로 변경될 수 있습니다.

Go 1.20에서는 [`randautoseed` 설정](/pkg/math/rand/#Seed)으로 제어되는 [`math/rand`](/pkg/math/rand) 글로벌 난수 생성기의 자동 시딩(automatic seeding) 기능이 도입되었습니다.

Go 1.20에서는 인증서 검증 중에 사용할 수 있는 폴백 루트(fallback roots) 개념이 도입되었으며, 이는 [`x509usefallbackroots` 설정](/pkg/crypto/x509/#SetFallbackRoots)으로 제어됩니다.

Go 1.20부터 Go 배포판에서 표준 라이브러리를 위해 미리 설치되었던 `.a` 파일들이 제거되었습니다.
이제 설치 프로세스는 다른 모듈의 패키지들과 마찬가지로 표준 라이브러리를 빌드하고 캐시합니다.
[`installgoroot` 설정](/cmd/go#hdr-Compile_and_install_packages_and_dependencies)을 사용하면 미리 설치된 `.a` 파일의 설치 및 사용 상태를 복구할 수 있습니다.

이 설정들 중 어느 것도 제거할 계획은 없습니다.

### Go 1.19

Go 1.19부터는 [`execerrdot` 설정](/pkg/os/exec#hdr-Executables_in_the_current_directory)에 의해 제어되며, 경로 조회(path lookups)가 현재 디렉터리의 바이너리로 해석되는 경우 에러가 발생하도록 변경되었습니다. 이 설정을 제거할 계획은 없습니다.

Go 1.19부터 DNS 요청 시 EDNS0 추가 헤더를 전송하기 시작했습니다.
이로 인해 CenturyLink Zyxel C3000Z와 같은 일부 라우터에서 제공하는 DNS 서버가 제대로 작동하지 않을 수 있다는 보고가 있습니다.
이는 [`netedns0` 설정](/pkg/net#hdr-Name_Resolution)을 통해 변경할 수 있습니다.
이 설정은 Go 1.21.12, Go 1.22.5, Go 1.23 및 이후 버전에서 사용할 수 있습니다.
이 설정을 제거할 계획은 없습니다.

### Go 1.18

Go 1.18에서는 [`x509sha1` 설정](/pkg/crypto/x509#InsecureAlgorithmError)으로 제어되는 대부분의 X.509 인증서에 대한 SHA1 지원이 제거되었습니다.
이 설정은 Go 1.24에서 제거되었습니다.

### Go 1.10

Go 1.10에서는 빌드 캐싱 작동 방식이 변경되었으며, [`gocacheverify`, `gocachehash`, `gocachetest` 설정](/cmd/go/#hdr-Build_and_test_caching)과 함께 테스트 캐싱이 추가되었습니다. 이러한 설정들을 제거할 계획은 없습니다.

### Go 1.6

Go 1.6에서는 [`http2client`, `http2server`, `http2debug` 설정](/pkg/net/http/#hdr-HTTP_2)으로 제어되는 HTTP/2의 투명한 지원(transparent support)이 도입되었습니다.
이 설정들을 제거할 계획은 없습니다.

### Go 1.5

Go 1.5에서는 [`netdns` 설정](/pkg/net/#hdr-Name_Resolution)으로 제어되는 순수 Go DNS 리졸버가 도입되었습니다.
이 설정을 제거할 계획은 없습니다.
