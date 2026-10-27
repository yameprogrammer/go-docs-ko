<!--
참고: 이 문서 및 이 디렉토리에 있는 다른 문서에서, 고정 폭 문자열을 사용하고, 고정 폭이 아닌 공백을 사용하는 규칙을 따릅니다. 예를 들어 `hello world`와 같이 사용합니다.
이러한 문자열에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.9 소개 {#introduction}

가장 최신 Go 릴리스인 버전 1.9는 [Go 1.8](go1.8) 이후 6개월 만에 출시되었으며, [Go 1.x
시리즈](/doc/devel/release.html)의 10번째 릴리스입니다.
언어에 대한 두 가지 [변경 사항](#language)이 있습니다:
타입 별칭을 지원하고, 구현이 부동 소수점 연산을 결합할 수 있는 시점을 정의하는 기능이 추가되었습니다.
대부분의 변경 사항은 도구 체, 런타임 및 라이브러리의 구현에 있습니다.
항상처럼, 이 릴리스는 Go 1의 [호환성 약속](/doc/go1compat.html)을 유지합니다.
대부분의 Go 프로그램이 기존과 동일하게 컴파일 및 실행될 것으로 예상됩니다.

릴리스
에는 [투명한 단일 시간 지원](#monotonic-time),
패키지 내에서 [함수 컴파일을 병렬화](#parallel-compile),
[테스트 헬퍼 함수] 지원을 개선,
새로운 [비트 조작 패키지](#math-bits)를 포함,
그리고 새로운 [동시 맵 타입](#sync-map)을 제공합니다.

## 언어 변경 사항 {#language}

다음은 두 가지 언어 변경 사항입니다.

Go는 이제 타입 별칭을 지원하여, 타입이 패키지를 이동하는 동안 점진적인 코드 복구를 지원합니다.
타입 별칭에 대한 [설계 문서](/design/18130-type-alias)와 [리팩토링에 대한
기사](/talks/2016/refactor.article)는 이 문제를 자세히 다룹니다.
요약하자면, 타입 별칭 선언은 다음과 같은 형태를 가집니다:

```
type T1 = T2
```

이 선언은 `T2`로 지정된 유형에 대한 대체 이름인 `T1`을 도입합니다. 즉, `T1`과 `T2`는 동일한 유형을 나타냅니다.

<!-- CL 40391 -->
언어 변경 사항 중 하나는 언어 사양이 이제 구현이 부동 소수점 연산을 함께 수행하도록 허용하는 경우를 명시하고 있다는 것입니다. 예를 들어, "Fused multiply and add" (FMA) 명령을 사용하여 중간 결과 `x*y`를 반올림하지 않고 `x*y` `+` `z`를 계산할 수 있습니다.
중간 결과의 반올림을 강제로 하려면 `float64(x*y)` `+` `z`를 사용하십시오.

## 포트

이 릴리스에는 새로운 지원되는 운영 체제 또는 프로세서 아키텍처가 없습니다.

### ppc64x는 POWER8을 필요로 합니다 {#power8}

<!-- CL 36725, CL 36832 -->
`GOARCH=ppc64` 및 `GOARCH=ppc64le` 모두 이제 최소 POWER8 지원이 필요합니다. 이전 버전에서는 `GOARCH=ppc64le`만 POWER8을 필요로 했으며, 큰 엔디안인 `ppc64` 아키텍처는 이전 하드웨어를 지원했습니다.

### FreeBSD {#freebsd}

Go 1.9은 FreeBSD 9.3에서만 실행되는 마지막 버전이며,
이미
[FreeBSD에서 지원되지 않음](https://www.freebsd.org/security/unsupported.html).
Go 1.10은 FreeBSD 10.3 이상을 필요로 합니다.

### OpenBSD 6.0 {#openbsd}

<!-- CL 40331 -->
Go 1.9에서 cgo 바이너리에 대한 PT\_TLS 생성 기능을 활성화했으며, 따라서 OpenBSD 6.0 또는 그 이상 버전을 필요로 합니다. Go 1.9에서는 OpenBSD 5.9를 더 이상 지원하지 않습니다.

### 알려진 문제 {#known_issues}

FreeBSD에는 알려진 특정 불안정성이 존재합니다.
이러한 불안정성은 드물게 프로그램 오류를 발생시킬 수 있습니다.
자세한 내용은 [issue 15658](/issue/15658)를 참조하십시오.
이 FreeBSD 특정 문제를 해결하는 데 도움이 필요합니다.

Go는 Go 1.9 개발 주기 동안 NetBSD 빌더를 중단했습니다. 이는 NetBSD 커널 충돌로 인해 NetBSD 7.1까지 영향을 미쳤습니다.
Go 1.9가 출시됨에 따라 NetBSD 7.1.1이 수정 사항과 함께 출시되었습니다.
그러나 현재 저희 테스트 스위트를 통과하는 NetBSD 빌더는 없습니다.
[다양한 NetBSD 문제](https://github.com/golang/go/labels/OS-NetBSD)에 대한 조사에 도움이 된다면 감사하겠습니다.

## 도구 {#tools}

### 병렬 컴파일 {#parallel-compile}

이제 Go 컴파일러는 여러 코어를 활용하여 패키지의 함수를 병렬로 컴파일할 수 있습니다. 이는 기존의 `go` 명령어가 별도의 패키지의 병렬 컴파일을 지원하는 것 외에 추가적인 기능입니다.

병렬 컴파일은 기본적으로 활성화되어 있지만, 환경 변수 `GO19CONCURRENTCOMPILATION`을 `0`으로 설정하여 비활성화할 수 있습니다.

### 공급업체 매칭 (./... 참조) {#vendor-dotdotdot}

<!-- CL 38745 -->
많은 요청에 따라, `./...`은 이제 `vendor` 디렉토리 내의 패키지를 더 이상 일치시키지 않습니다. 이는 `go test`와 같은 패키지 이름을 허용하는 도구에서 해당됩니다. `vendor` 디렉토리를 일치시키려면 `./vendor/...`을 사용하십시오.

### GOROOT 이동 {#goroot}

<!-- CL 42533 -->
[go 도구](/cmd/go/)는 이제 실행된 경로에서 Go 설치 트리의 루트를 찾기 위해 시도합니다.
즉, 전체 Go 설치를 새 위치로 이동하면 go 도구가 정상적으로 작동해야 합니다.
`GOROOT` 환경 변수를 설정하여 이를 덮어쓸 수 있습니다.
그러나 이는 특수한 경우에만 수행해야 합니다.
참고로, 이는 [runtime.GOROOT](/pkg/runtime/#GOROOT) 함수의 결과를 변경하지 않습니다.
이 함수는 원래 설치 위치를 계속 보고합니다.
이 기능은 향후 릴리스에서 수정될 수 있습니다.

### 컴파일러 도구 체인 {#compiler}

<!-- CL 37441 -->
복잡한 나눗셈이 이제 C99와 호환됩니다. 이는 항상 gccgo에서 작동했으며, 이제 gc 도구 체인에서 수정되었습니다.

<!-- CL 36983 -->
이제 링커는 Windows에서 cgo 실행 파일에 대한 DWARF 정보를 생성합니다.

<!-- CL 44210, CL 40095 -->
컴파일러가 `-N -l` 플래그가 제공되면 생성된 DWARF에 어휘적 스코프를 포함합니다. 이를 통해 디버거는 범위에 없는 변수를 숨길 수 있습니다. `.debug_info` 섹션은 이제 DWARF 버전 4를 사용합니다.

<!-- CL 43855 -->
`GOARM` 및 `GO386`의 값은 이제 컴파일된 패키지의 빌드 ID에 영향을 미치며, 이는 `go` 도구의 의존성 캐싱에 사용됩니다.

### 어셈블러 {#asm}

<!-- CL 42028 -->
ARM 명령어 `MULA` (4개의 연산자)가 이제 올바르게 어셈블되었으며,
덧셈 연산자 레지가 세 번째 인수로, 결과 레지가 네 번째 및 마지막 인수로 사용됩니다.
이전 릴리스에서는 두 가지 의미가 뒤바뀌었습니다.
네 번째 인수가 명시적으로 세 번째 인수인 세 개의 연산자 형태는 변경되지 않습니다.
네 개의 연산자 `MULA` 명령어를 사용하는 코드는 업데이트가 필요하지만, 이 형태는 매우 드물게 사용된다고 생각합니다.
`MULAWT` 및 `MULAWB`는 모든 형태에서 올바른 순서를 사용하고 있으며 변경되지 않았습니다.

<!-- CL 42990 -->
어셈블러는 이제 `ADDSUBPS/PD`를 지원하며, 누락되었던 두 가지 x86 SSE3 명령어를 완료합니다.

### 설명 {#go-doc}

<!-- CL 36031 -->
긴 인자 목록이 이제 잘리는 방식으로 처리됩니다. 이는 일부 생성된 `go` `doc`에 대한 가독성을 향상시킵니다.

<!-- CL 38438 -->
구조체 필드에 대한 설명서를 확인하는 기능이 지원되었습니다.
예를 들어, `go` `doc` `http.Client.Jar`를 참조하십시오.

### 환경 변수 {#go-env-json}

<!-- CL 38757 -->
새로운 `go` `env` `-json` 플래그는
JSON 출력을 활성화하여, 기본 OS별 출력이 아닌 형식을 사용합니다.

### 테스트 {#go-test-list}

<!-- CL 41195 -->
`go test` 명령은 새로운 `-list` 플래그를 허용하며, 이 플래그는 정규 표현식을 인수로 받아, 일치하는 모든 테스트, 벤치마크 또는 예제의 이름을 stdout에 출력합니다. 실행하지는 않습니다.

### Pprof {#go-tool-pprof}

<!-- CL 34192 -->
`runtime/pprof` 패키지로 생성된 프로파일에는 심볼 정보가 포함되므로, 프로파일을 생성한 바이너리 파일 없이 `go` `tool` `pprof`에서 확인할 수 있습니다.

<!-- CL 38343 -->
`go` 도구 `pprof` 명령이 이제
환경에 정의된 HTTP 프록시 정보를 사용합니다. `http.ProxyFromEnvironment` ([https://pkg.go.dev/net/http#ProxyFromEnvironment](https://pkg.go.dev/net/http#ProxyFromEnvironment))를 사용합니다.

### 수의사 {#vet}

<!-- CL 40112 -->

[`vet` 명령어](/cmd/vet/)
이 이제 `/cmd/go/` 도구에 더 잘 통합되어,
`go vet`는 이제 모든 표준 빌드 플래그를 지원하며,
`vet` 명령어 자체의 플래그는 이제 `go vet` 뿐만 아니라
`go tool vet`에서도 사용할 수 있습니다.

### Gccgo {#gccgo}

Go의 반기별 릴리즈 스케줄과 GCC의 연간 릴리즈 스케줄이 일치하기 때문에,
GCC 7에는 Go 1.8.3 버전의 gccgo가 포함되어 있습니다.
다음 릴리즈인 GCC 8에는 Go 1.10 버전의 gccgo가 포함될 것으로 예상합니다.

## 실행 시점 {#runtime}

### 호출 스택에 포함된 프레임 {#callersframes}

사용자는
[`runtime.Callers`](/pkg/runtime#Callers)
의 결과인 PC 슬라이스를 직접 검사하는 대신,
[`runtime.CallersFrames`](/pkg/runtime#CallersFrames)
를 사용하여 전체적인 호출 스택을 확인하거나,
[`runtime.Caller`](/pkg/runtime#Caller)
를 사용하여 단일 호출자 정보를 얻어야 합니다.

그 이유는, 개별 PC 슬라이스의 요소는 인라인된 프레임이나 호출 스택의 다른 뉘앙스를 설명할 수 없기 때문입니다.

특히, PC 슬라이스를 직접 반복적으로 순회하면서
`runtime.FuncForPC`와 같은 함수를 사용하여 각 PC를 개별적으로 해결하는 코드는 인라인된 프레임을 놓칠 수 있습니다.
전체적인 스택을 확인하려면, 대신 `CallersFrames`를 사용하는 것이 좋습니다.
또한, `Callers`가 반환하는 길이는 호출 깊이에 대한 어떤 지표도 아니라는 가정은 잘못된 것입니다.
대신, `CallersFrames`에서 반환된 프레임 수를 세어야 합니다.

코드가 특정 깊이에서 단일 호출자를 쿼리해야 하는 경우,
`Caller`를 사용하는 것이 `Callers`에 길이가 1인 슬라이스를 전달하는 것보다 좋습니다.

[`runtime.CallersFrames`](/pkg/runtime#CallersFrames)
은 Go 1.7부터 사용 가능하며, Go 1.9로 업그레이드하기 전에 코드를 업데이트할 수 있습니다.

## 성능 {#performance}

물론, 변경 사항이 너무 광범위하고 다양하여 정확한 성능에 대한 언급은 어렵습니다. 대부분의 프로그램은 가비지 컬렉터, 개선된 생성된 코드 및 핵심 라이브러리의 최적화로 인해 약간 더 빠르게 실행될 것으로 예상됩니다.

### 가비지 컬렉터 {#gc}

<!-- CL 37520 -->
이전에는 스톱 더 월드 가비지
수집을 트리거하는 라이브러리 함수는 이제 동시 가비지
수집을 트리거합니다.
특히, [`runtime.GC`](/pkg/runtime/#GC),
[`debug.SetGCPercent`](/pkg/runtime/debug/#SetGCPercent),
그리고
[`debug.FreeOSMemory`](/pkg/runtime/debug/#FreeOSMemory)는
이제 동시 가비지 수집을 트리거하며, 가비지 수집이 완료될 때까지 호출하는
goroutine만 차단합니다.

<!-- CL 34103, CL 39835 -->
`debug.SetGCPercent`
함수는 새로운 GOGC 값 때문에 즉시 가비지 컬렉션이 필요한 경우에만 가비지 컬렉션을 트리거합니다.
이를 통해 GOGC를 즉석에서 조정할 수 있습니다.

<!-- CL 38732 -->
대규모 힙 (50GB 이상)에 많은 대규모 객체가 포함된 애플리케이션에서 대규모 객체 할당 성능이 크게 향상됩니다.

<!-- CL 34937 -->
`runtime.ReadMemStats` 함수는 이제 매우 큰 힙도 100µs 미만으로 작동합니다.

## 표준 라이브러리 {#library}

### 투명한 단조 시간 지원 {#monotonic-time}

<!-- CL 36255 -->
`[time](pkg/time/)` 패키지는 이제 각 `[Time](pkg/time/#Time)` 값에 대해 일관된 시간을 투명하게 추적하며, 이를 통해 두 `Time` 값 사이의 기간을 계산하는 것이 벽시계 조정이 있는 경우에도 안전하게 수행됩니다.
자세한 내용은 [패키지 문서](/pkg/time/#hdr-Monotonic_Clocks) 및 [설계 문서](/design/12914-monotonic)를 참조하십시오.

### 새로운 비트 조작 패키지 {#math-bits}

<!-- CL 36315 -->
Go 1.9에는 최적화된 비트 조작 기능이 포함된 새로운 패키지,
[`math/bits`](/pkg/math/bits/)가 포함됩니다. 대부분의 아키텍처에서, 이 패키지의 함수는 컴파일러에 의해 추가로 인식되어 성능 향상을 위해 내부 함수로 처리됩니다.

### 테스트 헬퍼 함수 {#test-helper}

<!-- CL 38796 -->
새로운 [`(*T).Helper`](/pkg/testing/#T.Helper)
및 [`(*B).Helper`](/pkg/testing/#B.Helper)
메서드는 호출되는 함수를 테스트 헬퍼 함수로 표시합니다. 파일 및 라인 정보를 출력할 때, 해당 함수는 건너뜁니다. 이를 통해 유용한 라인 번호를 유지하면서 테스트 헬퍼 함수를 작성할 수 있습니다.

### 동시 맵 {#sync-map}

<!-- CL 36617 -->
`[`Map`](/pkg/sync/#Map) 유형
`[`sync`](/pkg/sync/) 패키지 내에 있는 새로운 유형은
평균적으로 상수 시간 내에 읽기, 쓰기 및 삭제 작업을 수행하는
동시 맵입니다. 여러 고루틴이 `Map`의 메서드를 동시에 호출하는 데 안전합니다.

### 프로파일러 레이블 {#pprof-레이블}

<!-- CL 34198 -->
`runtime/pprof` 패키지 ([/pkg/runtime/pprof])
이제 `pprof` 프로파일링 기록에 레이블을 추가할 수 있습니다.
레이블은 키-값 맵으로, `pprof` 명령 ([/cmd/pprof])으로 프로파일을 볼 때 동일한 함수 호출을 다른 컨텍스트에서 구별하는 데 사용됩니다.
`pprof` 패키지의
새로운 [`Do` 함수](/pkg/runtime/pprof/#Do)
제공된 레이블과 관련된 코드를 실행합니다. 패키지 내의 다른 새로운 함수들은 레이블과 함께 작업하는 데 도움을 줍니다.

<!-- runtime/pprof -->

### 라이브러리의 미세 조정 {#minor_library_changes}

물론, 라이브러리에는 항상 다양한 미세한 변경 사항 및 업데이트가 있으며, 이는 Go 1의 [호환성 보장](/doc/go1compat)을 염두에 두고 구현되었습니다.

#### [archive/zip](/pkg/archive/zip/)

<!-- CL 39570 -->
`ZIP Writer`
이제 적절한 경우
`FileHeader.Flags` 내에 UTF-8 비트를 설정합니다.

<!-- 압축/zip -->

#### [crypto/rand](/pkg/crypto/rand/)

<!-- CL 43852 -->
Linux에서 Go는 이제 `getrandom` 시스템 호출을 `GRND_NONBLOCK` 플래그 없이 호출합니다. 그러면 Go는 커널이 충분한 무작위 데이터를 생성할 때까지 대기합니다. `getrandom` 시스템 호출이 이전의 커널에서는 Go는 여전히 `/dev/urandom`에서 데이터를 읽습니다.

```markdown
<!-- crypto/rand -->
```

#### [crypto/x509](/pkg/crypto/x509/)

<!-- CL 36093 -->
유닉스 시스템에서는 `SSL_CERT_FILE` 및 `SSL_CERT_DIR` 환경 변수를 사용하여 SSL 인증서 파일 및 SSL 인증서 파일 디렉토리의 시스템 기본 위치를 재정의할 수 있습니다.

FreeBSD 파일 `/usr/local/etc/ssl/cert.pem`이 이제 인증서 검색 경로에 포함됩니다.

<!-- CL 36900 -->
이제 패키지는 이름 제약 조건에 제외된 도메인을 지원합니다.
이러한 제약 조건을 적용하는 것 외에도,
[`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate)
는 제공된 템플릿 인증서에 새로운
필드
[`ExcludedDNSDomains`](/pkg/crypto/x509/#Certificate.ExcludedDNSDomains)
가 채워져 있으면 제외된 이름 제약 조건을 가진 인증서를 생성합니다.

<!-- CL 36696 -->
만약 인증서에 DNS 이름이 없는 SAN 확장(들)이 포함되어 있는 경우,
`Subject`에서 가져온 일반 이름은 무시됩니다.
이전 버전에서는 코드가 인증서에 DNS 이름이 포함되어 있는지만 확인했습니다.

<!-- crypto/x509 -->

#### [database/sql](/pkg/database/sql/)

<!-- CL 35476 -->
이 패키지는 이제 `Stmt`를 캐시하여 사용하고, `Tx.Stmt`에 사용할 수 있는 경우 이를 사용합니다.
이를 통해 `Tx.Stmt`가 호출될 때마다 쿼리가 다시 준비되지 않도록 방지합니다.

<!-- CL 38533 -->
이제 패키지는 드라이버가 자체적인 인자 검사기를 구현할 수 있도록 [`driver.NamedValueChecker`](/pkg/database/sql/driver/#NamedValueChecker)를 구현할 수 있도록 합니다.
이 기능은 드라이버가 `OUTPUT` 및 `INOUT` 매개변수 유형을 지원할 수도 있도록 합니다.
드라이버에서 지원되는 경우 `Out`([/pkg/database/sql/#Out])를 사용하여 출력 매개변수를 반환해야 합니다.

<!-- CL 39031 -->
[`Rows.Scan`](/pkg/database/sql/#Rows.Scan) 이제 사용자 정의 문자열 유형을 스캔할 수 있습니다.
이전 버전에서는 `type` `Int` `int64`와 같은 숫자 유형으로 스캔하는 기능을 지원했습니다. 이제 `type` `String` `string`과 같은 문자열 유형으로 스캔하는 기능도 지원합니다.

<!-- CL 40694 -->
새로운 `DB.Conn` 메서드는 연결 풀에서 가져온 데이터베이스에 대한
독점적인 연결을 나타내는 새로운 `Conn` 유형을 반환합니다.
`Conn`을 사용하여 실행되는 모든 쿼리는 `Conn.Close`가 호출될 때까지
동일한 기본 연결을 사용합니다.

```
<!-- database/sql -->
```

#### [encoding/asn1](/pkg/encoding/asn1/)

<!-- CL 38660 -->
새로운
[`NullBytes`](/pkg/encoding/asn1/#NullBytes)
과
[`NullRawValue`](/pkg/encoding/asn1/#NullRawValue)
은 ASN.1 NULL 유형을 나타냅니다.

<!-- encoding/asn1 -->

#### [encoding/base32](/pkg/encoding/base32/)

<!-- CL 38634 -->
새로운 `Encoding.WithPadding`
메서드는 사용자 정의 패딩 문자를 사용하고 패딩을 비활성화하는 기능을 추가합니다.

<!-- encoding/base32 -->

#### [encoding/csv](/pkg/encoding/csv/)

<!-- CL 41730 -->
새로운 필드
[`Reader.ReuseRecord`](/pkg/encoding/csv/#Reader.ReuseRecord)
은 [`Read`](/pkg/encoding/csv/#Reader.Read) 함수가 이전 호출의 반환된 슬라이스의 백업 배열을 공유하는 슬라이스를 반환할 수 있는지 제어합니다. 이를 통해 성능을 향상시킬 수 있습니다.

<!-- encoding/csv -->

#### [fmt](/pkg/fmt/)

<!-- CL 37051 -->
날카로운 플래그 (`#`)가 부동 소수점 및 복소수를 출력할 때 이제 지원됩니다.
`%e`, `%E`, `%f`, `%F`, `%g` 및 `%G` 형식에서는 항상 소수점을 출력합니다.
`%g` 및 `%G` 형식에서는 꼬리 자릿수를 제거하지 않습니다.

<!-- fmt -->

#### [hash/fnv](/pkg/hash/fnv/)

<!-- CL 38356 -->
이 패키지는 이제 128비트 FNV-1 및 FNV-1a 해시를 지원하며,
[`New128`](/pkg/hash/fnv/#New128) 및
[`New128a`](/pkg/hash/fnv/#New128a)를 각각 사용합니다.

<!-- hash/fnv -->

#### [html/template](/pkg/html/template/)

<!-- CL 37880, CL 40936 -->
이제 패키지는 파이프라인에서 미리 정의된 이스케이퍼("html", "urlquery" 및 "js" 중 하나)가 발견되었지만, 자동 이스케이퍼가 스스로 결정했을 것과 일치하지 않는 경우 오류를 보고합니다.
이는 특정 보안 또는 정확성 문제를 방지합니다.
이제 이러한 이스케이퍼 중 하나를 사용하는 것은 항상 무효하거나 오류를 나타냅니다.
(무효인 경우 [text/template](/pkg/text/template/)에서 마이그레이션하는 것을 더 쉽게 만듭니다.)

<!-- html/템플릿 -->

#### [이미지](/pkg/image/)

<!-- CL 36734 -->
[`Rectangle.Intersect`](/pkg/image/#Rectangle.Intersect)
메서드가 인접하지만 겹치지 않는 사각형에 호출될 때 이제 0인 `Rectangle`을 반환합니다. 이는 문서화된 대로입니다. 이전 버전에서는 잘못된 방식으로 빈이지만 0이 아닌 `Rectangle`을 반환했습니다.

<!-- 이미지 -->

#### [이미지/색상](/pkg/image/color/)

<!-- CL 36732 -->
YCbCr에서 RGBA로 변환하는 공식이 수정되어,
반올림 조정이 [0, 0xffff] 범위의 전체 RGBA
범위를 커버하도록 했습니다.

<!-- 이미지/색상 -->

#### [이미지/png](/pkg/image/png/)

<!-- CL 34150 -->
새로운 `Encoder.BufferPool` 필드는 [`EncoderBufferPool`](/pkg/image/png/#Encoder.BufferPool)을 지정할 수 있도록 하며, 인코더는 PNG 이미지를 인코딩할 때 임시 `EncoderBuffer` 버퍼를 가져오는 데 사용할 것입니다.
`BufferPool`을 사용하면 여러 이미지를 인코딩하는 동안 수행되는 메모리 할당 횟수를 줄일 수 있습니다.

<!-- CL 38271 -->
이 패키지는 이제 투명한 8비트 그레이스케일("Gray8") 이미지의 디코딩을 지원합니다.

<!-- 이미지/png -->

#### [math/big](/pkg/math/big/)

<!-- CL 36487 -->
새로운
[`IsInt64`](/pkg/math/big/#Int.IsInt64)
및
[`IsUint64`](/pkg/math/big/#Int.IsUint64)
메서드는 `Int`
이 `int64` 또는 `uint64`
값으로 표현될 수 있는지 여부를 보고합니다.

<!-- 수식/big -->

#### [mime/multipart](/pkg/mime/multipart/)

<!-- CL 39223 -->
새로운
[`FileHeader.Size`](/pkg/mime/multipart/#FileHeader.Size)
필드는 multipart 메시지 내 파일의 크기를 설명합니다.

<!-- mime/multipart -->

#### [net](pkg/net/)

<!-- CL 32572 -->
새로운
[`Resolver.StrictErrors`](/pkg/net/#Resolver.StrictErrors)
은 Go의 내장 DNS 리졸버가 여러 하위 쿼리를 포함하는 쿼리 중 일시적인 오류를 처리하는 방식을 제어합니다. 예를 들어 A+AAAA 주소 조회와 같은 경우입니다.

<!-- CL 37260 -->
새로운
[`Resolver.Dial`](#Resolver.Dial)
기능을 통해 `Resolver`는 사용자 정의 래핑 함수를 사용할 수 있습니다.

<!-- CL 40510 -->
[`JoinHostPort`](/pkg/net/#JoinHostPort)는 이제 호스트에 콜론이 포함된 경우에만 주소를 대괄호로 묶습니다.
이전 버전에서는 퍼센트 문자(`%`)가 포함된 주소도 대괄호로 묶었습니다.

<!-- CL 37913 -->
새로운 메서드
[`TCPConn.SyscallConn`](/pkg/net/#TCPConn.SyscallConn),
[`IPConn.SyscallConn`](/pkg/net/#IPConn.SyscallConn),
[`UDPConn.SyscallConn`](/pkg/net/#UDPConn.SyscallConn),
및
[`UnixConn.SyscallConn`](/pkg/net/#UnixConn.SyscallConn)
은 연결의 내부 파일 디스크립터에 접근할 수 있도록 합니다.

<!-- 45088 -->
이제 `Listen` 함수를 사용하여 포트를 설정한 후, `(*TCPListener).String()`에서 얻은 주소로 `Dial` 함수를 호출하는 것이 안전합니다.
예: `<code>[Listen](/pkg/net/#Listen)("tcp", ":0")</code>`를 사용하여 리스너를 생성한 후입니다.
이전에는 부분적으로 설정된 IPv6 스택을 가진 일부 머신에서 오류가 발생했습니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- CL 37328 -->
`Cookie.String` 메서드 (`/pkg/net/http/#Cookie.String`), `Cookie` 및 `Set-Cookie` 헤더에 사용되는 메서드는 값이 공백 또는 쉼표를 포함하는 경우 값을 이중 따옴표로 묶습니다.

서버 변경 사항:

- <!-- CL 38194 -->
    [`ServeMux`](/pkg/net/http/#ServeMux)는 핸들 매칭 시 호스트 헤더에 있는 포트를 무시합니다. `CONNECT` 요청의 경우 호스트는 수정되지 않은 상태로 매칭됩니다.
  - <!-- CL 44074 -->
    새로운 [`Server.ServeTLS`](/pkg/net/http/#Server.ServeTLS) 메서드는 [`Server.Serve`](/pkg/net/http/#Server.Serve)를 TLS 지원을 추가하여 래핑합니다.
  - <!-- CL 34727 -->
    [`Server.WriteTimeout`](/pkg/net/http/#Server.WriteTimeout)는 이제 HTTP/2 연결에 적용되며 스트림별로 적용됩니다.
  - <!-- CL 43231 -->
    HTTP/2는 기본적으로 우선순위 쓰기 스케줄러를 사용합니다. 프레임은 [RFC 7540 섹션 5.3](https://tools.ietf.org/html/rfc7540#section-5.3)에 설명된 HTTP/2 우선 순위에 따라 스케줄링됩니다.
  - <!-- CL 36483 -->
    [`StripPrefix`](/pkg/net/http/#StripPrefix)에 의해 반환된 HTTP 핸들러는 이제 원래 `*http.Request`의 수정된 복사본을 사용하여 제공된 핸들러를 호출합니다. `*http.Request` 키로 된 매핑을 사용하여 요청별 상태를 저장하는 코드는 다음을 사용해야 합니다.
    [`Request.Context`](/pkg/net/http/#Request.Context),
    [`Request.WithContext`](/pkg/net/http/#Request.WithContext),
    및
    [`context.WithValue`](/pkg/context/#WithValue).
  - <!-- CL 35490 -->
    [`LocalAddrContextKey`](/pkg/net/http/#LocalAddrContextKey)는 이제 리스너에서 사용되는 인터페이스 주소가 아닌 연결의 실제 네트워크 주소를 포함합니다.

**클라이언트 및 트랜스포트 변경 사항:**

- <!-- CL 35488 -->
    [`Transport`](/pkg/net/http/#Transport)
    이제 `socks5` 스킴을 가진 [`Transport.Proxy`](/pkg/net/http/#Transport.Proxy)에서 반환된 URL을 통해 SOCKS5 프록시를 사용하여 요청을 만들 수 있습니다.

<!-- net/http -->

#### [net/http/fcgi](/pkg/net/http/fcgi/)

<!-- CL 40012 -->
새로운
[`ProcessEnv`](/pkg/net/http/fcgi/#ProcessEnv)
함수는 HTTP 요청에 대한 FastCGI 환경 변수를 반환합니다. 이 요청에는 적절한
[`http.Request`](/pkg/net/http/#Request)
필드가 없는 경우, 예를 들어 `REMOTE_USER`와 같은 변수가 포함될 수 있습니다.

<!-- net/http/fcgi -->

#### [net/http/httptest](/pkg/net/http/httptest/)

<!-- CL 34639 -->
새로운
[`Server.Client`](/pkg/net/http/httptest/#Server.Client)
메서드는 테스트 서버에 대한 요청을 만드는 데 구성된 HTTP 클라이언트를 반환합니다.

새로운
[`Server.Certificate`](/pkg/net/http/httptest/#Server.Certificate)
메서드는 테스트 서버의 TLS 인증서를 반환합니다 (있는 경우).

<!-- net/http/httptest -->

#### [net/http/httputil](/pkg/net/http/httputil/)

<!-- CL 43712 -->
`ReverseProxy` ([/pkg/net/http/httputil/#ReverseProxy](https://example.com/pkg/net/http/httputil/#ReverseProxy))
이제 초기 응답 헤더에 선언되지 않은 HTTP/2 응답 트레이럴도 모두 프록시합니다. 이러한 선언되지 않은 트레이럴은 gRPC 프로토콜에서 사용됩니다.

<!-- net/http/httputil -->

#### [os](pkg/os/)

<!-- CL 36800 -->
`os` 패키지는 이제 내부 런타임 폴러를 사용하여 파일 I/O를 처리합니다.
이는 파이프에 대한 읽기/쓰기 작업에 필요한 스레드 수를 줄이고, 한 고루틴이 파일을 닫는 동안 다른 고루틴이 파일을 I/O에 사용하는 경우 발생하는 경쟁 조건을 제거합니다.

<!-- CL 37915 -->
Windows에서,
[`Args`](/pkg/os/#Args)
이 이제 `shell32.dll` 없이 채워지므로, 프로세스 시작 시간을 1-7ms 개선했습니다.

<!-- os -->

#### [os/exec](/pkg/os/exec/)

<!-- CL 37586 -->
`os/exec` 패키지는 이제 자식 프로세스가 중복된 환경 변수를 사용하여 생성되는 것을 방지합니다.
`Cmd.Env`가 중복된 환경 변수 키를 포함하는 경우, 각 중복 키에 대한 슬라이스의 마지막 값만 사용됩니다.

<!-- os/exec -->

#### [os/user](/pkg/os/user/)

<!-- CL 37664 -->
[`Lookup`](/pkg/os/user/#Lookup) 및
[`LookupId`](/pkg/os/user/#LookupId) 함수는 `CGO_ENABLED=0`일 때 Unix 시스템에서 `/etc/passwd` 파일을 읽어 작동합니다.

<!-- CL 33713 -->
[`LookupGroup`](/pkg/os/user/#LookupGroup) 및
[`LookupGroupId`](/pkg/os/user/#LookupGroupId)는 `CGO_ENABLED=0`일 때 유닉스 시스템에서 `/etc/group` 파일을 읽어 작동합니다.

<!-- os/user -->

#### [reflect](/pkg/reflect/)

<!-- CL 38335 -->
새로운
[`MakeMapWithSize`](/pkg/reflect/#MakeMapWithSize)
함수는 용량 힌트가 있는 맵을 생성합니다.

<!-- 반사 -->

#### [runtime](/pkg/runtime/)

<!-- CL 37233, CL 37726 -->
실행 시간에 생성되고 프로필에 기록된 트레이스백은 이제 인라이닝의 영향을 받더라도 정확합니다.

프로그램적으로 트레이스백을 가져오려면 애플리케이션은 다음을 사용해야 합니다.
[`runtime.CallersFrames`](/pkg/runtime/#CallersFrames) 대신
[`runtime.Callers`](/pkg/runtime/#Callers)의 결과를 직접 반복하는 대신.

<!-- CL 38403 -->
Windows에서, Go는 프로그램이 비활성 상태일 때 시스템 타이머를 고해상도로 강제 실행하는 것을 더 이상 하지 않습니다.
이는 Go 프로그램이 배터리 수명에 미치는 영향을 줄이는 데 도움이 됩니다.

<!-- CL 29341 -->
FreeBSD에서, `GOMAXPROCS` 및 `runtime.NumCPU`는 이제 프로세스의 CPU 마스크를 기반으로 하며, 총 CPU 수가 아닌.

<!-- CL 43641 -->
런타임은 Android O에 대한 초기 지원을 제공합니다.

<!-- runtime -->

#### [runtime/debug](/pkg/runtime/debug/)

<!-- CL 34013 -->
`SetGCPercent` 함수를 호출
[`SetGCPercent`](/pkg/runtime/debug/#SetGCPercent)
에 음수 값을 전달하면 더 이상 즉시 가비지 컬렉션이 실행되지 않습니다.

<!-- 실행/디버깅 -->

#### [runtime/trace](/pkg/runtime/trace/)

<!-- CL 36015 -->
실행 추적에 이제 마크 어시스트 이벤트가 표시되며, 이는 애플리케이션 goroutine이 너무 빠르게 할당하여 가비지 컬렉션 지원을 강제로 받는 시점을 나타냅니다.

<!-- CL 40810 -->
"Sweep" 이벤트는 이제 할당에 필요한 빈 공간을 찾는 전체 프로세스를 포함하며, 개별적으로 청소되는 스팬을 기록하는 대신.
이는 할당이 많은 프로그램을 추적할 때 할당 지연 시간을 줄입니다.
Sweep 이벤트는 청소된 바이트 수와 회수된 바이트 수를 보여줍니다.

<!-- 실행/추적 -->

#### [sync](/pkg/sync/)

<!-- CL 34310 -->
[`Mutex`](/pkg/sync/#Mutex)가 이제 더 공정하게 동작합니다.

<!-- 동기화 -->

#### [syscall](/pkg/syscall/)

<!-- CL 36697 -->
새로운 필드
[`Credential.NoSetGroups`](/pkg/syscall/#Credential.NoSetGroups)
는 Unix 시스템이 새 프로세스를 시작할 때 보조 그룹을 설정하기 위해 `setgroups` 시스템 호출을 수행할지 여부를 제어합니다.

<!-- CL 43512 -->
새로운 필드
[`SysProcAttr.AmbientCaps`](/pkg/syscall/#SysProcAttr.AmbientCaps)
은 Linux 4.3 이상에서 새 프로세스를 생성할 때 환경 기반 기능을 설정할 수 있도록 합니다.

<!-- CL 37439 -->
64비트 x86 Linux에서 프로세스 생성 지연 시간을 최적화하기 위해 `CLONE_VFORK` 및 `CLONE_VM`을 사용했습니다.

<!-- CL 37913 -->
새로운
[`Conn`](/pkg/syscall/#Conn)
인터페이스는
[`net`](/pkg/net/)
패키지에 있는 일부 유형을 설명하며, 이 유형은 새로운
[`RawConn`](/pkg/syscall/#RawConn)
인터페이스를 사용하여 자체 내부 파일 설명자에 액세스할 수 있습니다.

<!-- syscall -->

#### [testing/quick](/pkg/testing/quick/)

<!-- CL 39152 -->
이 패키지는 `int64` 및 `uint64`의 무작위
숫자를 생성할 때 전체 범위를 선택합니다. 이전 버전에서는 항상
[-2<sup>62</sup>, 2<sup>62</sup>) 범위 내의 값만 생성되었습니다.

이전 버전에서는 `nil` [`Config.Rand`](/pkg/testing/quick/#Config.Rand) 값을 사용하면 고정된 결정론적 난수 생성기가 사용되었습니다.
이제 현재 시간을 기준으로 시드된 난수 생성기를 사용합니다.
이전 동작을 사용하려면 `Config.Rand`를 `rand.New(rand.NewSource(0))`로 설정하십시오.

<!-- 테스트/빠른 사용법 -->

#### [text/template](pkg/text/template/)

<!-- CL 38420 -->
빈 블록 처리 문제는 Go 1.8의 변경으로 인해 발생했으며, 이 변경 사항은 템플릿의 순서에 따라 결과가 달라지는 문제를 야기했습니다. 이 문제는 해결되어, Go 1.7의 이전 동작 방식이 복원되었습니다.

```markdown
<!-- 템플릿 -->

#### [time](/pkg/time/)

<!-- CL 36615 -->
새로운 메서드
[`Duration.Round`](/pkg/time/#Duration.Round)
과
[`Duration.Truncate`](/pkg/time/#Duration.Truncate)
는 주어진 기간의 배수로 시간을 반올림하고 잘라내는 기능을 처리합니다.

<!-- CL 35710 -->
Wine 환경에서 "시간 확인" 및 "잠자기" 기능이 정상적으로 작동합니다.

만약 `Time` 값에 단방향 시계 값이 있다면,
`String` 함수를 통해 반환되는 문자열 표현에는
최종 필드 `"m=±value"`가 포함됩니다. 여기서 `value`는
초 단위의 소수를 나타내는 단방향 시계 값입니다.

<!-- CL 44832 -->
포함된 `tzdata` 시간대 데이터베이스가 2017b 버전으로 업데이트되었습니다. 항상, 이 데이터베이스는 시스템에 이미 사용 가능한 경우에만 사용됩니다.

<!-- 시간 -->
