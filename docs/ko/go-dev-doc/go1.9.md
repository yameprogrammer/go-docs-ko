<!--
참고: 이 문서 및 이 디렉토리의 다른 문서에서는 `hello` `world`와 같이 고정폭 문구를 비고정폭 공백으로 구분하여 설정하는 관례를 따릅니다.
이러한 문구에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

<style>
  main ul li { margin: 0.5em 0; }
</style>

## Go 1.9 소개 {#introduction}

최신 Go 릴리스인 버전 1.9는 [Go 1.8](go1.8) 이후 6개월 만에 출시되었으며, [Go 1.x 시리즈](/doc/devel/release.html)의 열 번째 릴리스입니다.
언어에는 두 가지 [변경 사항](#language)이 있습니다: 타입 별칭(type aliases)에 대한 지원 추가와 부동 소수점 연산의 결합(fuse) 가능 시점 정의입니다.
대부분의 변경 사항은 툴체인, 런타임 및 라이브러리의 구현에 포함되어 있습니다.
언제나 그렇듯, 이번 릴리스는 Go 1의 [호환성 약속](/doc/go1compat.html)을 유지합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

이번 릴리스에서는
[투명한 단조 시간(monotonic time) 지원](#monotonic-time)이 추가되었고,
패키지 내 [함수의 병렬 컴파일](#parallel-compile)이 가능해졌으며,
[테스트 헬퍼 함수](#test-helper)에 대한 지원이 개선되었고,
새로운 [비트 조작 패키지](#math-bits)가 포함되었으며,
새로운 [동시성 맵 타입](#sync-map)이 추가되었습니다.

## 언어 변경 사항 {#language}

언어에 두 가지 변경 사항이 있습니다.

Go는 이제 타입을 패키지 간에 이동할 때 점진적인 코드 수정을 지원하기 위해 타입 별칭(type aliases)을 지원합니다.
[타입 별칭 설계 문서](/design/18130-type-alias)와 [리팩토링에 관한 문서](/talks/2016/refactor.article)에서 이 문제에 대해 자세히 다루고 있습니다.
요약하자면, 타입 별칭 선언은 다음과 같은 형태를 갖습니다:

`type T1 = T2`

이 선언은 `T2`로 표시된 타입에 대해 `T1`이라는 별칭(alias)—즉, 대체 표기법—을 도입합니다. 다시 말해, `T1`과 `T2`는 모두 동일한 타입을 나타냅니다.

<!-- CL 40391 -->
작은 언어 변경 사항으로, [언어 명세서](/ref/spec#Floating_point_operators)에 구현체가 부동 소수점 연산을 서로 결합할 수 있는 경우가 명시되었습니다. 예를 들어, 아키텍처의 "fused multiply and add"(FMA) 명령어를 사용하여 중간 결과인 `x*y`를 반올림하지 않고 `x*y` `+` `z`를 계산하는 경우가 이에 해당합니다.
중간 반올림을 강제하려면 `float64(x*y)` `+` `z`와 같이 작성하십시오.

## 포트 {#ports}

이번 릴리스에서 새롭게 지원되는 운영 체제나 프로세서 아키텍처는 없습니다.

### ppc64x는 POWER8이 필요합니다 {#power8}

<!-- CL 36725, CL 36832 -->
이제 `GOARCH=ppc64`와 `GOARCH=ppc64le` 모두 최소 POWER8 지원이 필요합니다. 이전 릴리스에서는 `GOARCH=ppc64le`만 POWER8을 필요로 했으며, 빅 엔디안(big endian) `ppc64` 아키텍처는 더 오래된 하드웨어를 지원했습니다.

### FreeBSD {#freebsd}

Go 1.9는 FreeBSD 9.3에서 실행되는 마지막 릴리스이며, 해당 버전은 이미 [FreeBSD에서 지원되지 않습니다](https://www.freebsd.org/security/unsupported.html). Go 1.10부터는 FreeBSD 10.3 이상 버전이 필요합니다.

### OpenBSD 6.0 {#openbsd}

<!-- CL 40331 -->
Go 1.9부터 cgo 바이너리에 대한 PT\_TLS 생성이 활성화되었으며, 이에 따라 OpenBSD 6.0 이상 버전이 필요합니다. Go 1.9는 더 이상 OpenBSD 5.9를 지원하지 않습니다.

### 알려진 문제 {#known_issues}

FreeBSD에서 알려져 있으나 원인이 파악되지 않은 일부 불안정성 문제가 있습니다.
이로 인해 드문 경우로 프로그램 충돌이 발생할 수 있습니다.
[issue 15658](/issue/15658)을 참조하십시오.
이 FreeBSD 전용 문제를 해결하는 데 도움을 주신다면 감사하겠습니다.

Go 1.9 개발 주기 동안 NetBSD 7.1을 포함한 이전 버전에서 NetBSD 커널 충돌이 발생하여 Go는 NetBSD 빌더 실행을 중단했습니다. Go 1.9가 출시됨에 따라, 수정 사항이 포함된 NetBSD 7.1.1이 출시되고 있습니다. 하지만 현재로서는 테스트 스위트를 통과하는 NetBSD 빌더가 없는 상태입니다. [다양한 NetBSD 이슈](https://github.com/golang/go/labels/OS-NetBSD)를 조사하는 데 도움을 주시면 감사하겠습니다.

## 도구 {#tools}

### 병렬 컴파일 {#parallel-compile}

이제 Go 컴파일러는 멀티코어를 활용하여 패키지 내의 함수들을 병렬로 컴파일하는 기능을 지원합니다. 이는 개별 패키지들을 병렬로 컴파일하는 `go` 명령어의 기존 지원 기능에 더해진 것입니다.
병렬 컴파일은 기본적으로 활성화되어 있으며, 환경 변수 `GO19CONCURRENTCOMPILATION`을 `0`으로 설정하여 비활성화할 수 있습니다.

### `./...`를 이용한 벤더 매칭 {#vendor-dotdotdot}

<!-- CL 38745 -->
많은 요청에 따라, `go` `test`와 같이 패키지 이름을 입력받는 도구에서 `./...`가 더 이상 `vendor` 디렉토리 내의 패키지를 일치시키지 않습니다. vendor 디렉토리를 일치시키려면 `./vendor/...`라고 작성하십시오.

### GOROOT 이동 {#goroot}

<!-- CL 42533 -->
이제 [go tool](/cmd/go/)은 Go 설치 트리의 루트를 찾기 위해 해당 도구가 호출된 경로를 사용합니다.
이는 Go 설치 전체가 새로운 위치로 이동하더라도 go tool이 평소처럼 계속 작동해야 함을 의미합니다.
환경 변수에서 `GOROOT`를 설정하여 이를 무시할 수 있으며, 이는 특수한 상황에서만 수행해야 합니다.
이 변경 사항은 [runtime.GOROOT](/pkg/runtime/#GOROOT) 함수의 결과에는 영향을 미치지 않으며, 해당 함수는 계속해서 원래의 설치 위치를 보고합니다. 이 문제는 이후 릴리스에서 수정될 수 있습니다.

### 컴파일러 툴체인 {#compiler}

<!-- CL 37441 -->
이제 복소수 나눗셈이 C99와 호환됩니다. 이는 gccgo에서는 항상 지원되던 사항이며, 이제 gc 툴체인에서도 수정되었습니다.

<!-- CL 36983 -->
이제 링커가 Windows의 cgo 실행 파일에 대해 DWARF 정보를 생성합니다.

<!-- CL 44210, CL 40095 -->
이제 `-N -l` 플래그가 제공되면 컴파일러가 생성된 DWARF에 어휘적 범위(lexical scopes)를 포함하여, 디버거가 범위 밖에 있는 변수를 숨길 수 있게 합니다. `.debug_info` 섹션은 이제 DWARF 버전 4를 사용합니다.

<!-- CL 43855 -->
이제 `GOARM` 및 `GO386` 값은 `go` 도구의 의존성 캐싱에 사용되는 컴파일된 패키지의 build ID에 영향을 줍니다.

### Assembler {#asm}

<!-- CL 42028 -->
이제 4-피연산자 ARM `MULA` 명령어가 올바르게 어셈블됩니다. 덧셈 피연산자(addend) 레지스터가 세 번째 인자로, 결과 레지스터가 네 번째이자 마지막 인자로 지정됩니다.
이전 릴리스에서는 이 두 가지 의미가 서로 바뀌어 있었습니다.
네 번째 인자가 암시적으로 세 번째 인자와 동일한 3-피연산자 형태는 영향을 받지 않습니다.
4-피연산자 `MULA` 명령어를 사용하는 코드는 업데이트가 필요하지만, 이 형태는 매우 드물게 사용되는 것으로 판단됩니다.
`MULAWT` 및 `MULAWB`는 이미 모든 형태에서 올바른 순서를 사용하고 있었으므로 변경 사항이 없습니다.

<!-- CL 42990 -->
어셈블러가 이제 `ADDSUBPS/PD`를 지원하며, 누락되었던 두 가지 x86 SSE3 명령어가 모두 구현되었습니다.

### Doc {#go-doc}

<!-- CL 36031 -->
이제 긴 인자 목록이 생략됩니다. 이를 통해 일부 생성된 코드에 대한 `go` `doc`의 가독성이 향상됩니다.

<!-- CL 38438 -->
이제 구조체 필드의 문서 확인이 지원됩니다.
예를 들어, `go` `doc` `http.Client.Jar`와 같이 사용할 수 있습니다.

### Env {#go-env-json}

<!-- CL 38757 -->
새로운 `go` `env` `-json` 플래그는
기본 OS별 출력 형식 대신 JSON 출력을 활성화합니다.

### 테스트 {#go-test-list}

<!-- CL 41195 -->
[`go` `test`](/cmd/go/#hdr-Description_of_testing_flags)
명령어는 새로운 `-list` 플래그를 지원합니다. 이 플래그는 정규 표현식을 인자로 받으며, 일치하는 테스트, 벤치마크 또는 예제의 이름을 실행하지 않고 stdout에 출력합니다.

### Pprof {#go-tool-pprof}

<!-- CL 34192 -->
`runtime/pprof` 패키지에서 생성된 프로파일에 이제 심볼 정보가 포함되므로, 프로파일을 생성한 바이너리 없이도 `go` `tool` `pprof`에서 확인할 수 있습니다.

<!-- CL 38343 -->
이제 `go` `tool` `pprof` 명령은 [`http.ProxyFromEnvironment`](/pkg/net/http/#ProxyFromEnvironment)를 사용하여 환경에 정의된 HTTP 프록시 정보를 사용합니다.

### Vet {#vet}

<!-- CL 40112 -->

[`vet` 명령어](/cmd/vet/)가
[`go` 도구](/cmd/go/)에 더 잘 통합되었습니다.
따라서 이제 `go` `vet`은 모든 표준 빌드 플래그를 지원하며, `vet` 자체의 플래그 역시 `go` `vet`뿐만 아니라
`go` `tool` `vet`에서도 사용할 수 있습니다.

### Gccgo {#gccgo}

Go의 반기별 릴리스 일정과 GCC의 연간 릴리스 일정이 맞물림에 따라,
GCC 릴리스 7에는 gccgo의 Go 1.8.3 버전이 포함되어 있습니다.
다음 릴리스인 GCC 8에는 gccgo의 Go 1.10 버전이 포함될 것으로 예상합니다.

## 런타임 {#runtime}

### 인라인 프레임이 포함된 콜 스택 {#callersframes}

[`runtime.Callers`](/pkg/runtime#Callers)
사용자는 결과로 반환된 PC 슬라이스를 직접 검사하는 것을 피해야 하며, 대신
[`runtime.CallersFrames`](/pkg/runtime#CallersFrames)
를 사용하여 호출 스택의 전체 뷰를 얻거나,
[`runtime.Caller`](/pkg/runtime#Caller)
를 사용하여 단일 호출자에 대한 정보를 얻어야 합니다.
이는 PC 슬라이스의 개별 요소가 인라인된 프레임이나 호출 스택의 다른 세부 사항들을 모두 반영할 수 없기 때문입니다.

구체적으로, PC 슬라이스를 직접 반복(iterate)하며 [`runtime.FuncForPC`](/pkg/runtime#FuncForPC)와 같은 함수를 사용하여 각 PC를 개별적으로 분석하는 코드는 인라인된 프레임(inlined frames)을 놓치게 됩니다.
스택의 전체 뷰를 얻으려면, 이러한 코드는 대신 `CallersFrames`를 사용해야 합니다.
마찬가지로, 코드는 `Callers`가 반환하는 길이가 호출 깊이(call depth)를 나타낸다고 가정해서는 안 됩니다.
대신 `CallersFrames`가 반환하는 프레임의 수를 세어야 합니다.

특정 깊이의 단일 호출자를 쿼리하는 코드는 `Callers`에 길이가 1인 슬라이스를 전달하는 대신 `Caller`를 사용해야 합니다.

[`runtime.CallersFrames`](/pkg/runtime#CallersFrames)는 Go 1.7부터 사용할 수 있었으므로, Go 1.9로 업그레이드하기 전에 코드를 업데이트할 수 있습니다.

## 성능 {#performance}

언제나 그렇듯, 변경 사항이 매우 일반적이고 다양하여 성능에 대한 정확한 진술을 하기는 어렵습니다. 하지만 가비지 컬렉터의 속도 향상, 더 개선된 코드 생성, 그리고 코어 라이브러리의 최적화 덕분에 대부분의 프로그램이 조금 더 빠르게 실행될 것입니다.

### Garbage Collector {#gc}

<!-- CL 37520 -->
이전에 stop-the-world 가비지 컬렉션을 트리거하던 라이브러리 함수들이 이제는 동시성(concurrent) 가비지 컬렉션을 트리거합니다.
구체적으로, [`runtime.GC`](/pkg/runtime/#GC),
[`debug.SetGCPercent`](/pkg/runtime/debug/#SetGCPercent),
그리고
[`debug.FreeOSMemory`](/pkg/runtime/debug/#FreeOSMemory)가
이제 동시성 가비지 컬렉션을 트리거하며, 가비지 컬렉션이 완료될 때까지 호출한 goroutine만 차단합니다.

<!-- CL 34103, CL 39835 -->
[`debug.SetGCPercent`](/pkg/runtime/debug/#SetGCPercent)
함수는 새로운 GOGC 값으로 인해 가비지 컬렉션이 즉시 필요한 경우에만 가비지 컬렉션을 트리거합니다.
이를 통해 GOGC 값을 실시간으로 조정할 수 있습니다.

<!-- CL 38732 -->
많은 수의 대형 객체를 포함하는 대규모(>50GB) 힙을 사용하는 애플리케이션에서 대형 객체 할당 성능이 크게 향상되었습니다.

<!-- CL 34937 -->
[`runtime.ReadMemStats`](/pkg/runtime/#ReadMemStats)
함수는 이제 매우 큰 힙(heap)에 대해서도 100µs 미만이 소요됩니다.

## 표준 라이브러리 {#library}

### 투명한 단조 시간(Monotonic Time) 지원 {#monotonic-time}

<!-- CL 36255 -->
이제 [`time`](/pkg/time/) 패키지는 각 [`Time`](/pkg/time/#Time) 값에서 단조 시간(monotonic time)을 투명하게 추적합니다. 이를 통해 월 클락(wall clock) 조정이 발생하는 상황에서도 두 `Time` 값 사이의 지속 시간(duration)을 계산하는 작업이 안전하게 수행됩니다. 자세한 내용은 [패키지 문서](/pkg/time/#hdr-Monotonic_Clocks)와 [설계 문서](/design/12914-monotonic)를 참조하십시오.

### 새로운 비트 조작 패키지 {#math-bits}

<!-- CL 36315 -->
Go 1.9에는 비트 조작을 위한 최적화된 구현을 제공하는 새로운 패키지 [`math/bits`](/pkg/math/bits/)가 포함되었습니다. 대부분의 아키텍처에서 이 패키지의 함수들은 컴파일러에 의해 추가로 인식되어, 성능 향상을 위해 인트린직(intrinsics)으로 처리됩니다.

### 테스트 헬퍼 함수 {#test-helper}

<!-- CL 38796 -->
새로운 [`(*T).Helper`](/pkg/testing/#T.Helper) 및 [`(*B).Helper`](/pkg/testing/#B.Helper) 메서드는 호출한 함수를 테스트 헬퍼 함수로 표시합니다. 파일 및 줄 정보(line information)를 출력할 때 해당 함수는 건너뛰게 됩니다. 이를 통해 사용자에게 여전히 유용한 줄 번호를 제공하면서 테스트 헬퍼 함수를 작성할 수 있습니다.

### Concurrent Map {#sync-map}

<!-- CL 36617 -->
[`sync`](/pkg/sync/) 패키지의 새로운 [`Map`](/pkg/sync/#Map) 타입은 분할 상환 상수 시간(amortized-constant-time)의 로드(load), 저장(store) 및 삭제(delete)를 지원하는 동시성 맵입니다. 여러 고루틴(goroutine)이 `Map`의 메서드를 동시에 호출해도 안전합니다.

### 프로파일러 레이블 (Profiler Labels) {#pprof-labels}

<!-- CL 34198 -->
[`runtime/pprof` 패키지](/pkg/runtime/pprof)가 이제 `pprof` 프로파일러 레코드에 레이블을 추가하는 기능을 지원합니다.
레이블은 키-값 맵 형태로 구성되며, [`pprof` 명령어](/cmd/pprof/)로 프로파일을 분석할 때 서로 다른 컨텍스트에서 호출된 동일한 함수의 호출들을 구분하는 데 사용됩니다.
`pprof` 패키지의 새로운 [`Do` 함수](/pkg/runtime/pprof/#Do)는 제공된 레이블과 연결된 코드를 실행합니다. 패키지에 추가된 다른 새로운 함수들은 레이블 작업을 돕습니다.

<!-- runtime/pprof -->

### 라이브러리의 사소한 변경 사항 {#minor_library_changes}

언제나 그렇듯, Go 1의 [호환성 약속](/doc/go1compat)을 염두에 두고 라이브러리에 다양한 소규모 변경 사항 및 업데이트가 이루어졌습니다.

#### [archive/zip](/pkg/archive/zip/)

<!-- CL 39570 -->
이제 ZIP [`Writer`](/pkg/archive/zip/#Writer)는 적절한 경우 [`FileHeader.Flags`](/pkg/archive/zip/#FileHeader.Flags)의 UTF-8 비트를 설정합니다.

<!-- archive/zip -->

#### [crypto/rand](/pkg/crypto/rand/)

<!-- CL 43852 -->
Linux에서 Go는 이제 `GRND_NONBLOCK` 플래그 없이 `getrandom` 시스템 콜을 호출합니다. 이제 커널에 충분한 무작위성이 확보될 때까지 블록(block)됩니다. `getrandom` 시스템 콜이 도입되기 이전의 커널에서는 계속해서 `/dev/urandom`에서 읽어옵니다.

<!-- crypto/rand -->

#### [crypto/x509](/pkg/crypto/x509/)

<!-- CL 36093 -->
Unix 시스템에서 환경 변수 `SSL_CERT_FILE` 및 `SSL_CERT_DIR`을 사용하여 각각 SSL 인증서 파일과 SSL 인증서 파일 디렉터리의 시스템 기본 위치를 재정의할 수 있습니다.

FreeBSD 파일 `/usr/local/etc/ssl/cert.pem`이 이제 인증서 검색 경로에 포함됩니다.

<!-- CL 36900 -->
이제 패키지에서 이름 제약 조건(name constraints)의 제외 도메인(excluded domains)을 지원합니다.
이러한 제약 조건을 강제하는 것 외에도,
제공된 템플릿 인증서에 새로운 필드인
[`ExcludedDNSDomains`](/pkg/crypto/x509/#Certificate.ExcludedDNSDomains)
가 채워져 있다면,
[`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate)
는 제외된 이름 제약 조건이 포함된 인증서를 생성합니다.

<!-- CL 36696 -->
DNS 이름이 없는 경우를 포함하여 인증서에 SAN 확장(extension)이 하나라도 존재하는 경우, [`Subject`](/pkg/crypto/x509/#Certificate.Subject)의 Common Name은 무시됩니다.
이전 릴리스에서는 코드에서 인증서에 DNS-name SAN이 존재하는지만 확인했습니다.

<!-- crypto/x509 -->

#### [database/sql](/pkg/database/sql/)

<!-- CL 35476 -->
이제 [`Tx.Stmt`](/pkg/database/sql/#Tx.Stmt)에서 사용 가능한 [`Stmt`](/pkg/database/sql/#Stmt)가 있다면 캐시된 항목을 사용합니다.
이를 통해 [`Tx.Stmt`](/pkg/database/sql/#Tx.Stmt)가 호출될 때마다 문(statement)을 매번 다시 준비(re-prepare)하는 것을 방지합니다.

<!-- CL 38533 -->
이제 드라이버가 [`driver.NamedValueChecker`](/pkg/database/sql/driver/#NamedValueChecker)를 구현하여 자체적인 인자 검사기(argument checker)를 구현할 수 있습니다.
이를 통해 드라이버에서 `OUTPUT` 및 `INOUT` 매개변수 타입을 지원할 수 있습니다.
드라이버가 이를 지원하는 경우, 출력 매개변수를 반환하기 위해 [`Out`](/pkg/database/sql/#Out)을 사용해야 합니다.

<!-- CL 39031 -->
[`Rows.Scan`](/pkg/database/sql/#Rows.Scan)이 이제 사용자 정의 문자열 타입을 스캔할 수 있습니다.
이전에는 `type` `Int` `int64`와 같은 숫자 타입으로의 스캔만 지원했지만, 이제는 `type` `String` `string`과 같은 문자열 타입으로의 스캔도 지원합니다.

<!-- CL 40694 -->
새로운 [`DB.Conn`](/pkg/database/sql/#DB.Conn) 메서드는 커넥션 풀에서 데이터베이스로의 독점적인 연결을 나타내는 새로운 [`Conn`](/pkg/database/sql/#Conn) 타입을 반환합니다. [`Conn`](/pkg/database/sql/#Conn)에서 실행되는 모든 쿼리는 [`Conn.Close`](/pkg/database/sql/#Conn.Close)가 호출되어 커넥션 풀로 연결을 반환할 때까지 동일한 기본 연결을 사용합니다.

<!-- database/sql -->

#### [encoding/asn1](/pkg/encoding/asn1/)

<!-- CL 38660 -->
새로운
[`NullBytes`](/pkg/encoding/asn1/#NullBytes)
및
[`NullRawValue`](/pkg/encoding/asn1/#NullRawValue)
는 ASN.1 NULL 타입을 나타냅니다.

<!-- encoding/asn1 -->

#### [encoding/base32](/pkg/encoding/base32/)

<!-- CL 38634 -->
새로운 [Encoding.WithPadding](/pkg/encoding/base32/#Encoding.WithPadding)
메서드는 사용자 정의 패딩 문자 지원 및 패딩 비활성화 기능을 추가합니다.

<!-- encoding/base32 -->

# encoding/base32

`base32` 패키지는 Base32 인코딩 및 디코딩을 지원합니다.

## 인덱스

- [함수](#함수)
- [변수](#변수)

## 함수

### func Encode(src []byte, dst []byte) int
`Encode`는 `src`를 Base32로 인코딩하여 `dst`에 씁니다. 작성된 바이트 수를 반환합니다.

### func Decode(dst, src []byte) (n int, err error)
`Decode`는 `src`를 Base32로 디코딩하여 `dst`에 씁니다. 작성된 바이트 수 `n`과 혹시 발생한 에러 `err`를 반환합니다.

## 변수

### var StdEncoding
`StdEncoding`은 RFC 4648에서 정의한 표준 Base32 알파벳을 사용하는 인코딩입니다.

#### [encoding/csv](/pkg/encoding/csv/)

<!-- CL 41730 -->
새로운 필드인
[`Reader.ReuseRecord`](/pkg/encoding/csv/#Reader.ReuseRecord)는
[`Read`](/pkg/encoding/csv/#Reader.Read)
호출 시 성능 향상을 위해 이전 호출에서 반환된 슬라이스의 backing array를 공유하는 슬라이스를 반환할 수 있는지 여부를 제어합니다.

<!-- encoding/csv -->

#### [fmt](/pkg/fmt/)

<!-- CL 37051 -->
부동 소수점 및 복소수 출력 시 샵 플래그('`#`')가 이제 지원됩니다. `%e`, `%E`, `%f`, `%F`, `%g` 및 `%G`에 대해 항상 소수점을 출력하며, `%g` 및 `%G`의 경우 후행 제로(trailing zeros)를 제거하지 않습니다.

<!-- fmt -->

#### [hash/fnv](/pkg/hash/fnv/)

<!-- CL 38356 -->
이제 이 패키지는 각각 [`New128`](/pkg/hash/fnv/#New128) 및 [`New128a`](/pkg/hash/fnv/#New128a)를 통해 128비트 FNV-1 및 FNV-1a 해시 지원을 포함합니다.

<!-- hash/fnv -->

#### [html/template](/pkg/html/template/)

<!-- CL 37880, CL 40936 -->
이제 파이프라인에서 사전 정의된 escaper("html", "urlquery", "js" 중 하나)가 발견되었으나, auto-escaper가 스스로 결정했을 결과와 일치하지 않는 경우 패키지가 에러를 보고합니다.
이는 특정 보안 또는 정확성 문제를 방지하기 위함입니다.
이제 이러한 escaper 중 하나를 사용하는 것은 항상 아무 작업도 수행하지 않거나(no-op) 에러가 발생합니다.
(no-op 케이스는 [text/template](/pkg/text/template/)로부터의 마이그레이션을 용이하게 합니다.)

<!-- html/template -->

#### [image](/pkg/image/)

<!-- CL 36734 -->
[`Rectangle.Intersect`](/pkg/image/#Rectangle.Intersect) 메서드는 이제 문서에 기재된 대로, 인접해 있지만 겹치지 않는 사각형들에 대해 호출되었을 때 zero `Rectangle`을 반환합니다. 이전 릴리스에서는 비어 있지만 zero가 아닌 `Rectangle`을 잘못 반환했습니다.

<!-- 이미지 -->

#### [image/color](/pkg/image/color/)

<!-- CL 36732 -->
반올림 조정 값이 [0, 0xffff] RGBA 전체 범위에 걸쳐 적용되도록 YCbCr에서 RGBA로의 변환 공식이 수정되었습니다.

<!-- image/color -->

#### [image/png](/pkg/image/png/)

<!-- CL 34150 -->
새로운 [`Encoder.BufferPool`](/pkg/image/png/#Encoder.BufferPool)
필드를 통해 [`EncoderBufferPool`](/pkg/image/png/#EncoderBufferPool)을 지정할 수 있으며,
인코더는 PNG 이미지를 인코딩할 때 임시 `EncoderBuffer`
버퍼를 가져오기 위해 이를 사용합니다.
`BufferPool`을 사용하면 여러 이미지를 인코딩하는 동안 발생하는
메모리 할당 횟수를 줄일 수 있습니다.

<!-- CL 38271 -->
이제 이 패키지는 투명 8비트 그레이스케일("Gray8") 이미지의 디코딩을 지원합니다.

제공해주신 내용에 텍스트가 포함되어 있지 않습니다. 번역할 내용을 입력해 주세요.

#### [math/big](/pkg/math/big/)

<!-- CL 36487 -->
새로운
[`IsInt64`](/pkg/math/big/#Int.IsInt64)
및
[`IsUint64`](/pkg/math/big/#Int.IsUint64)
메서드는 `Int`가
`int64` 또는 `uint64`
값으로 표현될 수 있는지 여부를 보고합니다.

<!-- math/big -->

#### [mime/multipart](/pkg/mime/multipart/)

<!-- CL 39223 -->
새로운 [`FileHeader.Size`](/pkg/mime/multipart/#FileHeader.Size) 필드는 멀티파트 메시지 내 파일의 크기를 나타냅니다.

제공해주신 내용이 비어 있거나 유효한 텍스트가 포함되어 있지 않습니다. 번역할 Markdown 내용을 입력해 주세요.

#### [net](/pkg/net/)

<!-- CL 32572 -->
새로운 [`Resolver.StrictErrors`](/pkg/net/#Resolver.StrictErrors)는 A+AAAA 주소 조회와 같이 여러 개의 하위 쿼리로 구성된 쿼리 도중 발생하는 일시적인 오류를 Go의 내장 DNS 리졸버가 처리하는 방식에 대한 제어 기능을 제공합니다.

<!-- CL 37260 -->
새로운 [`Resolver.Dial`](/pkg/net/#Resolver.Dial)을 통해 `Resolver`에서 커스텀 dial 함수를 사용할 수 있습니다.

<!-- CL 40510 -->
[`JoinHostPort`](/pkg/net/#JoinHostPort)는 이제 호스트에 콜론(`:`)이 포함된 경우에만 주소를 대괄호로 묶습니다.
이전 릴리스에서는 주소에 퍼센트('`%`') 기호가 포함된 경우에도 대괄호로 묶었습니다.

<!-- CL 37913 -->
새로운 메서드인
[`TCPConn.SyscallConn`](/pkg/net/#TCPConn.SyscallConn),
[`IPConn.SyscallConn`](/pkg/net/#IPConn.SyscallConn),
[`UDPConn.SyscallConn`](/pkg/net/#UDPConn.SyscallConn),
및
[`UnixConn.SyscallConn`](/pkg/net/#UnixConn.SyscallConn)은(는)
연결의 기본 파일 디스크립터(file descriptor)에 대한 접근을 제공합니다.

<!-- 45088 -->
이제 `<code>[Listen](/pkg/net/#Listen)("tcp", ":0")</code>`으로 리스너를 생성한 후 `(*TCPListener).String()`에서 얻은 주소를 사용하여 [`Dial`](/pkg/net/#Dial)을 호출해도 안전합니다.
이전에는 IPv6 스택이 불완전하게 설정된 일부 머신에서 실패하는 문제가 있었습니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- CL 37328 -->
`Cookie` 및 `Set-Cookie` 헤더에 사용되는 [`Cookie.String`](/pkg/net/http/#Cookie.String) 메서드는 이제 값에 공백이나 쉼표가 포함되어 있는 경우 해당 값을 큰따옴표로 감쌉니다.

서버 변경 사항:

- <!-- CL 38194 -->
    [`ServeMux`](/pkg/net/http/#ServeMux)가 핸들러를 매칭할 때 이제 host 헤더의 포트 번호를 무시합니다. `CONNECT` 요청의 경우 host는 수정 없이 매칭됩니다.
  - <!-- CL 44074 -->
    새로운 [`Server.ServeTLS`](/pkg/net/http/#Server.ServeTLS) 메서드는 TLS 지원이 추가된 [`Server.Serve`](/pkg/net/http/#Server.Serve)를 래핑합니다.
  - <!-- CL 34727 -->
    [`Server.WriteTimeout`](/pkg/net/http/#Server.WriteTimeout)이 이제 HTTP/2 연결에도 적용되며, 스트림별로 강제됩니다.
  - <!-- CL 43231 -->
    HTTP/2가 이제 기본적으로 우선순위 쓰기 스케줄러(priority write scheduler)를 사용합니다. 프레임은 [RFC 7540 Section 5.3](https://tools.ietf.org/html/rfc7540#section-5.3)에 기술된 HTTP/2 우선순위에 따라 스케줄링됩니다.
  - <!-- CL 36483 -->
    [`StripPrefix`](/pkg/net/http/#StripPrefix)가 반환하는 HTTP 핸들러가 이제 원본 `*http.Request`를 수정하여 복제한 후 제공된 핸들러를 호출합니다. `*http.Request`를 키로 사용하는 맵에 요청별 상태를 저장하는 코드는 대신 [`Request.Context`](/pkg/net/http/#Request.Context), [`Request.WithContext`](/pkg/net/http/#Request.WithContext), 그리고 [`context.WithValue`](/pkg/context/#WithValue)를 사용해야 합니다.
  - <!-- CL 35490 -->
    [`LocalAddrContextKey`](/pkg/net/http/#LocalAddrContextKey)가 이제 리스너가 사용하는 인터페이스 주소 대신 연결의 실제 네트워크 주소를 포함합니다.

클라이언트 및 전송(Transport) 변경 사항:

- <!-- CL 35488 -->
    이제 [`Transport`](/pkg/net/http/#Transport)는 [`Transport.Proxy`](/pkg/net/http/#Transport.Proxy)가 반환한 URL의 스킴(scheme)이 `socks5`인 경우, SOCKS5 프록시를 통해 요청을 보내는 기능을 지원합니다.

<!-- net/http -->

#### [net/http/fcgi](/pkg/net/http/fcgi/)

<!-- CL 40012 -->
새로운 [`ProcessEnv`](/pkg/net/http/fcgi/#ProcessEnv) 함수는 `REMOTE_USER`와 같이 [`http.Request`](/pkg/net/http/#Request) 필드에 적절한 항목이 없는 HTTP 요청과 관련된 FastCGI 환경 변수를 반환합니다.

<!-- net/http/fcgi -->

#### [net/http/httptest](/pkg/net/http/httptest/)

<!-- CL 34639 -->
새로운 [`Server.Client`](/pkg/net/http/httptest/#Server.Client) 메서드는 테스트 서버로 요청을 보내도록 설정된 HTTP 클라이언트를 반환합니다.

새로운 [`Server.Certificate`](/pkg/net/http/httptest/#Server.Certificate) 메서드는 테스트 서버의 TLS 인증서가 있는 경우 이를 반환합니다.

<!-- net/http/httptest -->

#### [net/http/httputil](/pkg/net/http/httputil/)

<!-- CL 43712 -->
[`ReverseProxy`](/pkg/net/http/httputil/#ReverseProxy)는 이제 초기 응답 헤더에 선언되지 않은 트레일러를 포함하여 모든 HTTP/2 응답 트레일러를 프록시합니다. 이러한 미선언 트레일러는 gRPC 프로토콜에서 사용됩니다.

<!-- net/http/httputil -->

#### [os](/pkg/os/)

<!-- CL 36800 -->
`os` 패키지가 이제 파일 I/O에 내부 런타임 폴러(runtime poller)를 사용합니다.
이를 통해 파이프의 읽기/쓰기 작업에 필요한 스레드 수가 줄어들며, 한 고루틴이 파일을 닫는 동안 다른 고루틴이 해당 파일을 I/O에 사용할 때 발생하는 레이스 컨디션(race)이 제거됩니다.

<!-- CL 37915 -->
Windows에서,
[`Args`](/pkg/os/#Args)
가 이제 `shell32.dll` 없이 채워지며, 이를 통해 프로세스 시작 시간이 1-7ms 개선되었습니다.

<!-- os -->

#### [os/exec](/pkg/os/exec/)

<!-- CL 37586 -->
이제 `os/exec` 패키지는 자식 프로세스가 중복된 환경 변수를 가지고 생성되는 것을 방지합니다.
[`Cmd.Env`](/pkg/os/exec/#Cmd.Env)에 중복된 환경 변수 키가 포함되어 있는 경우, 각 중복 키에 대해 슬라이스의 마지막 값만 사용됩니다.

<!-- os/exec -->

#### [os/user](/pkg/os/user/)

<!-- CL 37664 -->
이제 [`Lookup`](/pkg/os/user/#Lookup) 및 [`LookupId`](/pkg/os/user/#LookupId)는 `CGO_ENABLED=0`인 Unix 시스템에서 `/etc/passwd` 파일을 읽어 동작합니다.

<!-- CL 33713 -->
[`LookupGroup`](/pkg/os/user/#LookupGroup) 및
[`LookupGroupId`](/pkg/os/user/#LookupGroupId)가 이제
`CGO_ENABLED=0`인 Unix 시스템에서 `/etc/group` 파일을 읽어
작동합니다.

<!-- os/user -->

#### [reflect](/pkg/reflect/)

<!-- CL 38335 -->
새로운 [`MakeMapWithSize`](/pkg/reflect/#MakeMapWithSize) 함수는 용량 힌트(capacity hint)가 지정된 맵을 생성합니다.

<!-- reflect -->

#### [runtime](/pkg/runtime/)

<!-- CL 37233, CL 37726 -->
런타임에서 생성되어 프로파일에 기록되는 Traceback이 이제 인라이닝(inlining)이 발생한 상황에서도 정확하게 나타납니다.
프로그래밍 방식으로 Traceback을 가져오려면, 애플리케이션은 [`runtime.Callers`](/pkg/runtime/#Callers)의 결과를 직접 반복 처리하는 대신 [`runtime.CallersFrames`](/pkg/runtime/#CallersFrames)를 사용해야 합니다.

<!-- CL 38403 -->
Windows에서 Go는 더 이상 프로그램이 유휴 상태일 때 시스템 타이머가 고해상도로 작동하도록 강제하지 않습니다.
이를 통해 Go 프로그램이 배터리 수명에 미치는 영향이 줄어들 것입니다.

<!-- CL 29341 -->
FreeBSD에서 `GOMAXPROCS`와
[`runtime.NumCPU`](/pkg/runtime/#NumCPU)
는 이제 전체 CPU 수가 아닌 프로세스의 CPU 마스크를 기준으로 합니다.

<!-- CL 43641 -->
런타임은 Android O에 대한 예비 지원을 제공합니다.

<!-- runtime -->

#### [runtime/debug](/pkg/runtime/debug/)

<!-- CL 34013 -->
[`SetGCPercent`](/pkg/runtime/debug/#SetGCPercent)를 음수 값으로 호출해도 더 이상 즉시 가비지 컬렉션(garbage collection)이 실행되지 않습니다.

<!-- runtime/debug -->

#### [runtime/trace](/pkg/runtime/trace/)

<!-- CL 36015 -->
이제 실행 트레이스(execution trace)에 mark assist 이벤트가 표시됩니다. 이 이벤트는 애플리케이션 고루틴이 너무 빠르게 메모리를 할당하여 가비지 컬렉션을 돕도록 강제되는 시점을 나타냅니다.

<!-- CL 40810 -->
이제 "Sweep" 이벤트는 스윕(sweep)된 각 개별 span을 기록하는 대신, 할당을 위한 빈 공간을 찾는 전체 프로세스를 포괄합니다.
이를 통해 할당 작업이 많은 프로그램의 트레이싱 시 할당 지연 시간(allocation latency)이 감소합니다.
sweep 이벤트는 몇 바이트가 스윕되었고 몇 바이트가 회수되었는지를 보여줍니다.

<!-- runtime/trace -->

#### [sync](/pkg/sync/)

<!-- CL 34310 -->
[`Mutex`](/pkg/sync/#Mutex)가 이제 더 공정(fair)하게 동작합니다.

<!-- sync -->

#### [syscall](/pkg/syscall/)

<!-- CL 36697 -->
새로운 필드인
[`Credential.NoSetGroups`](/pkg/syscall/#Credential.NoSetGroups)는
Unix 시스템이 새로운 프로세스를 시작할 때 보조 그룹(supplementary groups)을 설정하기 위해
`setgroups` 시스템 호출을 수행할지 여부를 제어합니다.

<!-- CL 43512 -->
새로운 필드
[`SysProcAttr.AmbientCaps`](/pkg/syscall/#SysProcAttr.AmbientCaps)
를 사용하면 새 프로세스를 생성할 때 Linux 4.3 이상 버전에서 ambient capabilities를 설정할 수 있습니다.

<!-- CL 37439 -->
64비트 x86 Linux에서 `CLONE_VFORK` 및 `CLONE_VM`을 사용하여 프로세스 생성 지연 시간이 최적화되었습니다.

<!-- CL 37913 -->
새로운
[`Conn`](/pkg/syscall/#Conn)
인터페이스는 새로운
[`RawConn`](/pkg/syscall/#RawConn)
인터페이스를 사용하여 기본 파일 디스크립터(file descriptor)에 대한 액세스를 제공할 수 있는
[`net`](/pkg/net/)
패키지의 일부 타입들을 설명합니다.

<!-- syscall -->

#### [testing/quick](/pkg/testing/quick/)

<!-- CL 39152 -->
이제 이 패키지는 `int64` 및 `uint64` 난수를 생성할 때 전체 범위 내에서 값을 선택합니다. 이전 릴리스에서는 생성된 값이 항상 [-2<sup>62</sup>, 2<sup>62</sup>) 범위로 제한되었습니다.

이전 릴리스에서는 [`Config.Rand`](/pkg/testing/quick/#Config.Rand) 값으로 `nil`을 사용하면 고정된 결정론적 난수 생성기가 사용되었습니다. 이제는 현재 시간으로 시드(seed)가 설정된 난수 생성기를 사용합니다. 이전의 동작이 필요한 경우, `Config.Rand`를 `rand.New(rand.NewSource(0))`로 설정하십시오.

<!-- testing/quick -->

#### [text/template](/pkg/text/template/)

<!-- CL 38420 -->
템플릿의 순서에 따라 결과가 달라지게 만든 Go 1.8의 변경 사항으로 인해 발생했던 빈 블록(empty blocks) 처리 문제가 수정되어, 이전의 Go 1.7 동작 방식으로 복구되었습니다.

<!-- text/template -->

#### [time](/pkg/time/)

<!-- CL 36615 -->
새로운 메서드인
[`Duration.Round`](/pkg/time/#Duration.Round)
와
[`Duration.Truncate`](/pkg/time/#Duration.Truncate)
는 기간(duration)을 주어진 기간의 배수로 반올림하거나 절삭하는 기능을 처리합니다.

<!-- CL 35710 -->
이제 Wine 환경에서 시간 조회 및 슬립(sleeping) 기능이 정상적으로 작동합니다.

`Time` 값에 단조 시계(monotonic clock) 판독값이 있는 경우, `String` 메서드에 의해 반환되는 문자열 표현에 이제 마지막 필드로 `"m=±value"`가 포함됩니다. 여기서 `value`는 초 단위의 십진수로 포맷된 단조 시계 판독값입니다.

<!-- CL 44832 -->
포함된 `tzdata` 시간대 데이터베이스가 2017b 버전으로 업데이트되었습니다. 언제나 그렇듯이, 이 데이터베이스는 시스템에 이미 사용 가능한 데이터베이스가 없는 경우에만 사용됩니다.

<!-- time -->
