<!--
참고: 이 문서 및 이 디렉터리의 다른 문서에서는
`hello` `world`와 같이 고정폭 구문을 비고정폭 공백으로 설정하는 것이 관례입니다.
이러한 구문에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

<style>
  main ul li { margin: 0.5em 0; }
</style>

## Go 1.8 소개 {#introduction}

최신 Go 릴리스인 버전 1.8가 [Go 1.7](go1.7) 출시 6개월 만에 공개되었습니다.
변경 사항의 대부분은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언어 사양에는 [두 가지의 사소한 변경 사항](#language)이 있습니다.
언제나 그렇듯, 이번 릴리스에서도 Go 1 [호환성 약속](/doc/go1compat.html)을 유지합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

이번 릴리스에서는 [32비트 MIPS 지원이 추가되었으며](#ports),
더 효율적인 코드를 생성하도록 [컴파일러 백엔드가 업데이트되었고](#compiler),
stop-the-world 스택 재스캔을 제거하여 [GC 일시 중단 시간이 단축되었으며](#gc),
[HTTP/2 Push 지원이 추가되었고](#h2push),
[HTTP graceful shutdown 기능이 추가되었으며](#http_shutdown),
[더 많은 context 지원이 추가되었고](#more_context),
[뮤텍스 프로파일링이 활성화되었으며](#mutex_prof),
[슬라이스 정렬 방식이 간소화되었습니다](#sort_slice).

## 언어 변경 사항 {#language}

하나의 구조체 타입을 다른 구조체 타입으로 명시적으로 변환할 때, Go 1.8부터는 태그가 무시됩니다. 따라서 태그만 서로 다른 두 구조체는 서로 간에 변환이 가능합니다:

```go
func example() {
		type T1 struct {
			X int `json:"foo"`
		}
		type T2 struct {
			X int `json:"bar"`
		}
		var v1 T1
		var v2 T2
		v1 = T1(v2) // 이제 유효함
	}
```

<!-- CL 17711 -->
이제 언어 명세에서는 구현체가 부동 소수점 상수의 지수를 최대 16비트까지 지원하도록만 요구합니다. 이는 “[`gc`](/cmd/compile/)” 및 `gccgo` 컴파일러 모두에 영향을 주지 않으며, 두 컴파일러 모두 여전히 32비트 지수를 지원합니다.

## 포트 {#ports}

Go는 이제 FPU 또는 커널 FPU 에뮬레이션을 구현하고 MIPS32r1 명령어 집합을 사용하는 빅 엔디안(`linux/mips`) 및 리틀 엔디안(`linux/mipsle`) 머신 모두에 대해 Linux 상의 32비트 MIPS를 지원합니다. 일반적인 많은 MIPS 기반 라우터에는 FPU가 없으며, 커널 FPU 에뮬레이션을 활성화하지 않은 펌웨어를 사용한다는 점에 유의하십시오. Go는 이러한 머신에서는 실행되지 않습니다.

DragonFly BSD에서 Go는 이제 DragonFly 4.4.4 또는 그 이후 버전이 필요합니다. <!-- CL 29491, CL 29971 -->

OpenBSD에서 Go는 이제 OpenBSD 5.9 이상 버전이 필요합니다. <!-- CL 34093 -->

Plan 9 포트의 네트워킹 지원이 이제 훨씬 더 완벽해졌으며, 데드라인(deadline) 및 취소(cancellation)와 관련하여 Unix 및 Windows의 동작과 일치합니다. Plan 9 커널 요구 사항은 [Plan 9 위키 페이지](/wiki/Plan9)를 참조하십시오.

Go 1.8는 이제 OS X 10.8 또는 그 이후 버전만 지원합니다. 이번 릴리스가 10.8을 지원하는 마지막 Go 릴리스가 될 가능성이 높습니다. 이전 OS X 버전에서 Go를 컴파일하거나 바이너리를 실행하는 것은 테스트되지 않았습니다.

Go 1.8는 ARMv5E 및 ARMv6 프로세서 기반의 Linux를 지원하는 마지막 릴리스가 됩니다.
Go 1.9는 (Raspberry Pi 1에서 볼 수 있는) ARMv6K 또는 그 이후 버전을 요구할 가능성이 높습니다.
Linux 시스템이 ARMv6K 이상인지 확인하려면 다음을 실행하십시오:
“`go` `tool` `dist` `-check-armv6k`”
(테스트를 용이하게 하기 위해, Go 1.8 전체를 설치하지 않고 `dist` 명령만 시스템으로 복사하는 것도 가능합니다)
프로그램이 "ARMv6K supported."라는 출력과 함께 종료되면 해당 시스템은 ARMv6K 또는 그 이후 버전을 구현한 것입니다.
non-Linux ARM 시스템의 Go는 이미 ARMv6K 또는 그 이후 버전을 요구하고 있습니다.

<!-- CL 31596, go.dev/issue/17528 -->
이제 `GOOS`의 인식 가능한 값으로 `zos`가 추가되었으며, 이는 z/OS 운영체제를 위해 예약되었습니다.

### 알려진 문제 {#known_issues}

FreeBSD 및 NetBSD에서 알려져 있지만 아직 원인이 파악되지 않은 일부 불안정성 문제가 있습니다.
이는 드문 경우지만 프로그램 충돌로 이어질 수 있습니다.
[issue 15658](/issue/15658) 및 [issue 16511](/issue/16511)을 참조하십시오.
이 문제들을 해결하는 데 도움을 주신다면 감사하겠습니다.

## 도구 {#tools}

### Assembler {#cmd_asm}

64비트 x86 시스템을 위해 다음 명령어들이 추가되었습니다:
`VBROADCASTSD`,
`BROADCASTSS`,
`MOVDDUP`,
`MOVSHDUP`,
`MOVSLDUP`,
`VMOVDDUP`,
`VMOVSHDUP`, 및
`VMOVSLDUP`.

64비트 PPC 시스템을 위해 다음과 같은 공통 벡터 스칼라(vector scalar) 명령어들이 추가되었습니다:
`LXS`,
`LXSDX`,
`LXSI`,
`LXSIWAX`,
`LXSIWZX`,
`LXV`,
`LXVD2X`,
`LXVDSX`,
`LXVW4X`,
`MFVSR`,
`MFVSRD`,
`MFVSRWZ`,
`MTVSR`,
`MTVSRD`,
`MTVSRWA`,
`MTVSRWZ`,
`STXS`,
`STXSDX`,
`STXSI`,
`STXSIWX`,
`STXV`,
`STXVD2X`,
`STXVW4X`,
`XSCV`,
`XSCVDPSP`,
`XSCVDPSPN`,
`XSCVDPSXDS`,
`XSCVDPSXWS`,
`XSCVDPUXDS`,
`XSCVDPUXWS`,
`XSCVSPDP`,
`XSCVSPDPN`,
`XSCVSXDDP`,
`XSCVSXDSP`,
`XSCVUXDDP`,
`XSCVUXDSP`,
`XSCVX`,
`XSCVXP`,
`XVCV`,
`XVCVDPSP`,
`XVCVDPSXDS`,
`XVCVDPSXWS`,
`XVCVDPUXDS`,
`XVCVDPUXWS`,
`XVCVSPDP`,
`XVCVSPSXDS`,
`XVCVSPSXWS`,
`XVCVSPUXDS`,
`XVCVSPUXWS`,
`XVCVSXDDP`,
`XVCVSXDSP`,
`XVCVSXWDP`,
`XVCVSXWSP`,
`XVCVUXDDP`,
`XVCVUXDSP`,
`XVCVUXWDP`,
`XVCVUXWSP`,
`XVCVX`,
`XVCVXP`,
`XXLAND`,
`XXLANDC`,
`XXLANDQ`,
`XXLEQV`,
`XXLNAND`,
`XXLNOR`,
`XXLOR`,
`XXLORC`,
`XXLORQ`,
`XXLXOR`,
`XXMRG`,
`XXMRGHW`,
`XXMRGLW`,
`XXPERM`,
`XXPERMDI`,
`XXSEL`,
`XXSI`,
`XXSLDWI`,
`XXSPLT`, 및
`XXSPLTW`.

### Yacc {#tool_yacc}

<!-- CL 27324, CL 27325 -->
`yacc` 도구(이전에는 “`go` `tool` `yacc`”를 실행하여 사용 가능)가 제거되었습니다.
Go 1.7부터 Go 컴파일러에서 더 이상 사용되지 않았습니다.
이 도구는 “tools” 저장소로 이동되었으며, 이제 [`golang.org/x/tools/cmd/goyacc`](https://godoc.org/golang.org/x/tools/cmd/goyacc)에서 사용할 수 있습니다.

### Fix {#tool_fix}

<!-- CL 28872 -->
`fix` 도구에 “`context`” 관련 새로운 수정 사항이 추가되었습니다.
이 수정 사항은 임포트를 “`golang.org/x/net/context`”에서
“[`context`](/pkg/context/)”로 변경합니다.

### Pprof {#tool_pprof}

<!-- CL 33157 -->
이제 `pprof` 도구는 “`https+insecure`” URL 스킴을 사용하여 TLS 서버를 프로파일링하고 인증서 검증을 건너뛸 수 있습니다.

<!-- CL 23781 -->
이제 callgrind 출력에 명령어 수준(instruction-level)의 세분성이 적용됩니다.

### Trace {#tool_trace}

<!-- CL 23324 -->
`trace` 도구에 실행 트레이스(execution trace)로부터 pprof 호환 블로킹(blocking) 및 레이턴시(latency) 프로파일을 생성하는 새로운 `-pprof` 플래그가 추가되었습니다.

<!-- CL 30017, CL 30702 -->
이제 실행 트레이스 뷰어(execution trace viewer)에서 가비지 컬렉션(garbage collection) 이벤트가 더 명확하게 표시됩니다. 가비지 컬렉션 활동은 별도의 행에 표시되며, GC 헬퍼 고루틴(helper goroutines)에는 각자의 역할이 주석으로 표시됩니다.

### Vet {#tool_vet}

Vet은 어떤 면에서는 더 엄격해졌고, 이전에 오탐(false positives)을 유발했던 부분에서는 더 완화되었습니다.

Vet는 이제 다음과 같은 사항들을 검사합니다:
* 락(lock) 배열의 복사
* 중복된 JSON 및 XML 구조체 필드 태그
* 공백으로 구분되지 않은 구조체 태그
* 에러 확인 전의 HTTP `Response.Body.Close` 지연 호출(deferred calls)
* `Printf` 내의 인덱싱된 인자(indexed arguments)

또한 기존 검사 기능들이 개선되었습니다.

### 컴파일러 툴체인 {#compiler}

Go 1.7에서는 64비트 x86 시스템을 위한 새로운 컴파일러 백엔드가 도입되었습니다.
Go 1.8에서는 해당 백엔드가 더욱 발전하여 이제 모든 아키텍처에서 사용됩니다.

[정적 단일 할당 형식](https://en.wikipedia.org/wiki/Static_single_assignment_form) (SSA)를 기반으로 하는 새로운 백엔드는 더 간결하고 효율적인 코드를 생성하며, 경계 검사 제거(bounds check elimination)와 같은 최적화를 위한 더 나은 플랫폼을 제공합니다.

새로운 백엔드는 32비트 ARM 시스템에서 벤치마크 프로그램에 필요한 CPU 시간을 20-30% 줄여줍니다. Go 1.7에서 이미 SSA 백엔드를 사용했던 64비트 x86 시스템의 경우, 성능 향상은 0-10%로 보다 완만합니다. 다른 아키텍처들은 32비트 ARM 수치에 가까운 개선 효과를 볼 가능성이 높습니다.

새로운 백엔드를 비활성화하기 위해 Go 1.7에서 도입되었던 임시 컴파일러 플래그 `-ssa=0`이 Go 1.8에서 제거되었습니다.

모든 시스템에 대해 새로운 컴파일러 백엔드를 활성화하는 것 외에도, Go 1.8은 새로운 컴파일러 프런트엔드를 도입합니다. 새로운 컴파일러 프런트엔드는 사용자가 체감하기 어렵겠지만, 향후 성능 개선 작업을 위한 기반이 됩니다.

컴파일러와 링커가 최적화되어 이번 릴리스에서는 Go 1.7보다 더 빠르게 실행됩니다. 비록 여전히 저희가 원하는 수준보다는 느리지만, 향후 릴리스에서 계속해서 최적화될 예정입니다.
이전 릴리스와 비교하여 Go 1.8은 [약 15% 더 빠릅니다](https://dave.cheney.net/2016/11/19/go-1-8-toolchain-improvements).

### Cgo {#cmd_cgo}

<!-- CL 31141 -->
이제 Go 도구는 `make.bash` 중에 설정된 `CGO_ENABLED` 환경 변수 값을 기억하며, 이슈 [#12808](/issue/12808)을 해결하기 위해 기본적으로 이후의 모든 컴파일에 이 값을 적용합니다.
네이티브 컴파일을 수행할 때, `make.bash`가 올바른 설정을 자동으로 감지하므로 `CGO_ENABLED` 환경 변수를 명시적으로 설정해야 하는 경우는 드뭅니다. `CGO_ENABLED` 환경 변수를 명시적으로 설정해야 하는 주된 이유는 환경이 cgo를 지원하지만 명시적으로 cgo 지원을 원하지 않는 경우이며, 이 경우 `make.bash` 또는 `all.bash` 중에 `CGO_ENABLED=0`으로 설정하십시오.

<!-- CL 29991 -->
이제 환경 변수 `PKG_CONFIG`를 사용하여 `#cgo` `pkg-config` 지시문을 처리하는 데 실행할 프로그램을 설정할 수 있습니다. 기본값은 이전 릴리스에서 항상 사용되었던 `pkg-config` 프로그램입니다. 이는 [cgo](/cmd/cgo/) 코드를 교차 컴파일(cross-compile)하는 것을 더 쉽게 만들기 위한 것입니다.

<!-- CL 32354 -->
이제 [cgo](/cmd/cgo/) 도구가 [go](/cmd/go/) 명령에서 사용하는 `-srcdir` 옵션을 지원합니다.

<!-- CL 31768, 31811 -->
[cgo](/cmd/cgo/) 코드가 `C.malloc`을 호출하고 `malloc`이 `NULL`을 반환하면, 이제 프로그램은 메모리 부족(out of memory) 오류와 함께 충돌합니다.
`C.malloc`은 절대 `nil`을 반환하지 않습니다.
대부분의 C 함수와 달리, `C.malloc`은 errno 값을 반환하는 두 개의 결과값 형태(two-result form)로 사용할 수 없습니다.

<!-- CL 33237 -->
[cgo](/cmd/cgo/)를 사용하여 C union에 대한 포인터를 전달하며 C 함수를 호출할 때, 해당 C union이 포인터 값을 포함할 수 있고 [cgo pointer checking](/cmd/cgo/#hdr-Passing_pointers)이 활성화되어 있다면(기본값), 이제 union 값에 대해 Go 포인터 검사가 수행됩니다.

### Gccgo {#gccgo}

Go의 반기별 릴리스 일정과 GCC의 연간 릴리스 일정의 정렬로 인해,
GCC 릴리스 6에는 gccgo의 Go 1.6.1 버전이 포함되어 있습니다.
다음 릴리스인 GCC 7에는 gccgo의 Go 1.8 버전이 포함될 것으로 예상합니다.

### 기본 GOPATH {#gopath}

[`GOPATH`
환경 변수](/cmd/go/#hdr-GOPATH_environment_variable)가 설정되지 않은 경우 이제 기본값이 적용됩니다. Unix에서는 `$HOME/go`, Windows에서는 `%USERPROFILE%/go`가 기본값으로 설정됩니다.

### Go get {#go_get}

<!-- CL 34818 -->
이제 “`go` `get`” 명령은 <code style="white-space:nowrap">-insecure</code> 플래그 사용 여부와 관계없이 항상 HTTP 프록시 환경 변수를 준수합니다. 이전 릴리스에서는 <code style="white-space:nowrap">-insecure</code> 플래그를 사용하면 프록시를 사용하지 않는 부수 효과가 있었습니다.

### Go 버그 {#go_bug}

새로운 “[`go` `bug`](/cmd/go/#hdr-Print_information_for_bug_reports)” 명령어는 현재 시스템에 대한 정보가 미리 채워진 상태로 GitHub에 버그 리포트를 시작합니다.

### Go doc {#cmd_doc}

<!-- CL 25419 -->
이제 “[`go` `doc`](/cmd/go/#hdr-Show_documentation_for_package_or_symbol)”
명령어가 [`godoc`](/cmd/godoc/)의 동작을 따라 상수와 변수를 해당 타입과 함께 그룹화하여 표시합니다.

<!-- CL 25420 -->
`doc` 출력의 가독성을 높이기 위해, 1레벨 항목의 각 요약(summary)은 반드시 한 줄을 차지하도록 보장됩니다.

<!-- CL 31852 -->
이제 “`go` `doc` `net.Conn.SetDeadline`”과 같이 인터페이스 정의 내의 특정 메서드에 대한 문서를 요청할 수 있습니다.

### 플러그인 {#plugin}

Go는 이제 Go로 작성된 플러그인을 생성하기 위한 “`plugin`” 빌드 모드와, 이러한 플러그인을 런타임에 로드하기 위한 새로운 [`plugin`](/pkg/plugin/) 패키지를 통해 플러그인에 대한 초기 지원을 제공합니다. 플러그인 지원은 현재 Linux에서만 가능합니다. 문제가 발생하면 보고해 주세요.

## Runtime {#runtime}

### 인자 활성 상태 (Argument Liveness) {#liveness}

<!-- Issue 15843 -->
가비지 컬렉터는 더 이상 함수 전체 범위에서 인수가 live 상태라고 간주하지 않습니다. 더 자세한 정보와 변수를 계속 live 상태로 유지하는 방법에 대해서는 Go 1.7에서 추가된 [`runtime.KeepAlive`](/pkg/runtime/#KeepAlive) 함수를 참조하십시오.

_업데이트:_
할당된 객체에 finalizer를 설정하는 코드는 해당 객체를 사용하는 함수나 메서드에 `runtime.KeepAlive` 호출을 추가해야 할 수도 있습니다.
자세한 내용은 [`KeepAlive` 문서](/pkg/runtime/#KeepAlive)와 해당 예제를 읽어보시기 바랍니다.

### Concurrent Map Misuse {#mapiter}

Go 1.6에서 런타임은 [맵의 동시성 오용에 대한 가벼운 베스트 에포트(best-effort) 감지 기능을 추가](/doc/go1.6#runtime)했습니다. 이번 릴리스에서는 맵에 동시에 쓰기와 반복문(iterate)을 수행하는 프로그램을 감지하는 기능을 지원하여 해당 감지기를 개선했습니다.

언제나 그렇듯이, 한 고루틴(goroutine)이 맵(map)에 데이터를 쓰고 있다면, 다른 어떤 고루틴도 동시에 해당 맵을 읽거나(반복문 포함) 써서는 안 됩니다.
런타임이 이러한 상황을 감지하면 진단 내용을 출력하고 프로그램을 충돌(crash)시킵니다.
이 문제에 대해 더 자세히 알아보는 가장 좋은 방법은 [race detector](/blog/race-detector)를 사용하여 프로그램을 실행하는 것이며, 이를 통해 레이스 컨디션(race)을 더 확실하게 식별하고 더 상세한 정보를 얻을 수 있습니다.

### MemStats 문서 {#memstats}

<!-- CL 28972 -->
[`runtime.MemStats`](/pkg/runtime/#MemStats)
타입에 대한 문서화가 더 상세하게 이루어졌습니다.

## 성능 {#performance}

언제나 그렇듯, 변경 사항이 매우 광범위하고 다양하여 성능에 대해 정확한 진술을 하기는 어렵습니다.
가비지 컬렉터의 속도 향상과 표준 라이브러리의 최적화 덕분에 대부분의 프로그램이 약간 더 빠르게 실행될 것입니다.

다음 패키지들의 구현에 최적화가 이루어졌습니다:
[`bytes`](/pkg/bytes/),
[`crypto/aes`](/pkg/crypto/aes/),
[`crypto/cipher`](/pkg/crypto/cipher/),
[`crypto/elliptic`](/pkg/crypto/elliptic/),
[`crypto/sha256`](/pkg/crypto/sha256/),
[`crypto/sha512`](/pkg/crypto/sha512/),
[`encoding/asn1`](/pkg/encoding/asn1/),
[`encoding/csv`](/pkg/encoding/csv/),
[`encoding/hex`](/pkg/encoding/hex/),
[`encoding/json`](/pkg/encoding/json/),
[`hash/crc32`](/pkg/hash/crc32/),
[`image/color`](/pkg/image/color/),
[`image/draw`](/pkg/image/draw/),
[`math`](/pkg/math/),
[`math/big`](/pkg/math/big/),
[`reflect`](/pkg/reflect/),
[`regexp`](/pkg/regexp/),
[`runtime`](/pkg/runtime/),
[`strconv`](/pkg/strconv/),
[`strings`](/pkg/strings/),
[`syscall`](/pkg/syscall/),
[`text/template`](/pkg/text/template/), 및
[`unicode/utf8`](/pkg/unicode/utf8/).

### 가비지 컬렉터 (Garbage Collector) {#gc}

가비지 컬렉션(Garbage collection) 일시 중지 시간은 Go 1.7보다 상당히 짧아져야 하며, 보통 100 마이크로초 미만, 때로는 10 마이크로초까지 낮아집니다.

자세한 내용은 [stop-the-world 스택 재스캔 제거에 관한 문서](https://github.com/golang/proposal/blob/master/design/17503-eliminate-rescan.md)를 참조하십시오. Go 1.9를 위한 추가 작업이 남아 있습니다.

### Defer {#defer}

<!-- CL 29656, CL 29656 -->

[지연 함수 호출](/ref/spec/#Defer_statements)의 오버헤드가 약 절반으로 줄어들었습니다.

### Cgo {#cgoperf}

Go에서 C로의 호출 오버헤드가 약 절반으로 줄어들었습니다.

## 표준 라이브러리 {#library}

### 예제 {#examples}

많은 패키지의 문서에 예제가 추가되었습니다.

### 정렬 {#sort_slice}

[sort](/pkg/sort/) 패키지에 _less_ 함수를 통해 슬라이스를 정렬할 수 있는 편리한 [`Slice`](/pkg/sort/#Slice) 함수가 추가되었습니다. 많은 경우, 이는 새로운 sorter 타입을 작성할 필요가 없음을 의미합니다.

또한 [`SliceStable`](/pkg/sort/#SliceStable)과 [`SliceIsSorted`](/pkg/sort/#SliceIsSorted)가 새로 추가되었습니다.

### HTTP/2 Push {#h2push}

[net/http](/pkg/net/http/) 패키지에 [`Handler`](/pkg/net/http/#Handler)에서 HTTP/2 서버 푸시를 보낼 수 있는 메커니즘이 추가되었습니다. 기존의 `Flusher` 및 `Hijacker` 인터페이스와 유사하게, 이제 HTTP/2 [`ResponseWriter`](/pkg/net/http/#ResponseWriter)는 새로운 [`Pusher`](/pkg/net/http/#Pusher) 인터페이스를 구현합니다.

### HTTP 서버의 Graceful Shutdown (우아한 종료) {#http_shutdown}

<!-- CL 32329 -->
이제 HTTP Server는 새로운 [`Server.Shutdown`](/pkg/net/http/#Server.Shutdown) 메서드를 사용한 우아한 종료(graceful shutdown)와 새로운 [`Server.Close`](/pkg/net/http/#Server.Close) 메서드를 사용한 즉각적인 종료(abrupt shutdown)를 지원합니다.

### 더 많은 컨텍스트 지원 {#more_context}

표준 라이브러리에 [`context.Context`](/pkg/context/#Context)를 도입한 [Go 1.7](/doc/go1.7#context)에 이어, Go 1.8은 기존 패키지들에 더 많은 컨텍스트 지원을 추가합니다:

- 새로운 [`Server.Shutdown`](/pkg/net/http/#Server.Shutdown)은 context 인자를 받습니다.
  - [database/sql](/pkg/database/sql/) 패키지에 context 지원을 포함한 [중요한 기능들이 추가되었습니다](#database_sql).
  - 새로운 [`net.Resolver`](/pkg/net/#Resolver)에 추가된 9가지 `Lookup` 메서드 모두 이제 context를 받습니다.

### Mutex 경합 프로파일링 (Mutex Contention Profiling) {#mutex_prof}

런타임과 도구들이 이제 경합이 발생하는 뮤텍스(contended mutexes)의 프로파일링을 지원합니다.

대부분의 사용자는 “[`go` `test`](/cmd/go/#hdr-Description_of_testing_flags)”와 함께 새로운 `-mutexprofile` 플래그를 사용하고, 생성된 파일에 [pprof](/cmd/pprof/)를 사용하기를 원할 것입니다.

새로운 [`MutexProfile`](/pkg/runtime/#MutexProfile) 및 [`SetMutexProfileFraction`](/pkg/runtime/#SetMutexProfileFraction)을 통해 더 낮은 수준(lower-level)의 지원도 가능합니다.

Go 1.8의 알려진 제한 사항은 프로파일이 [`sync.Mutex`](/pkg/sync/#Mutex)에 대한 경합만 보고하며, [`sync.RWMutex`](/pkg/sync/#RWMutex)에 대해서는 보고하지 않는다는 점입니다.

### 라이브러리의 소규모 변경 사항 {#minor_library_changes}

언제나 그렇듯, Go 1 [호환성 약속](/doc/go1compat)을 염두에 두고 라이브러리에 다양한 소규모 변경 및 업데이트가 이루어졌습니다. 다음 섹션에서는 사용자가 확인할 수 있는 변경 사항과 추가 사항을 나열합니다. 최적화 및 사소한 버그 수정 사항은 목록에 포함되지 않았습니다.

#### [archive/tar](/pkg/archive/tar/)

<!-- CL 28471, CL 31440, CL 31441, CL 31444, CL 28418, CL 31439 -->
tar 구현체에서 파일 형식의 엣지 케이스(corner cases)와 관련된 많은 버그가 수정되었습니다.
[`Reader`](/pkg/archive/tar/#Reader)
는 이제 8GB보다 큰 항목이 포함된 PAX 형식의 tar 파일을 처리할 수 있습니다.
[`Writer`](/pkg/archive/tar/#Writer)
는 긴 경로 이름이 포함된 일부 상황에서 더 이상 잘못된 tar 파일을 생성하지 않습니다.

#### [compress/flate](/pkg/compress/flate/)

<!-- CL 31640, CL 31174, CL 32149 -->
특정 상황에서 압축률을 향상시키기 위해 인코더에 몇 가지 사소한 수정 사항이 있었습니다. 그 결과, `DEFLATE`의 정확한 인코딩 출력값이 Go 1.7과 다를 수 있습니다. `DEFLATE`는 gzip, png, zlib, zip의 기본 압축 방식이므로, 해당 포맷들의 출력값 또한 변경되었을 수 있습니다.

<!-- CL 31174 -->
인코더가 [`NoCompression`](/pkg/compress/flate/#NoCompression) 모드로 동작할 때, 이제 [`Write`](/pkg/compress/flate/#Writer.Write) 메서드에 전달되는 슬라이스의 크기에 의존하지 않고 일관된 출력을 생성합니다.

<!-- CL 28216 -->
디코더는 이제 오류가 발생했을 때, 압축을 해제하여 버퍼에 보관하고 있던 데이터를 오류와 함께 반환합니다.

#### [compress/gzip](/pkg/compress/gzip/)

[`Writer`](/pkg/compress/gzip/#Writer)는 이제 [`Header.ModTime`](/pkg/compress/gzip/#Header) 필드가 제로 값(zero value)인 경우 `MTIME` 필드를 0으로 인코딩합니다. 이전 버전의 Go에서는 `Writer`가 의미 없는 값을 인코딩했습니다. 마찬가지로, [`Reader`](/pkg/compress/gzip/#Reader)는 이제 0으로 인코딩된 `MTIME` 필드를 제로 값의 `Header.ModTime`으로 보고합니다.

#### [context](/pkg/context/)

<!-- CL 30370 -->
[`DeadlineExceeded`](/pkg/context#DeadlineExceeded)
오류는 이제 [`net.Error`](/pkg/net/#Error)를
구현하며, `Timeout` 및 `Temporary` 메서드 모두에 대해 true를 보고합니다.

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 25159, CL 31318 -->
새로운 메서드
[`Conn.CloseWrite`](/pkg/crypto/tls/#Conn.CloseWrite)
를 통해 TLS 연결을 하프 클로즈(half closed) 상태로 만들 수 있습니다.

<!-- CL 28075 -->
새로운 메서드인 [`Config.Clone`](/pkg/crypto/tls/#Config.Clone)은 TLS 설정을 복제합니다.

<!-- CL 30790 -->
새로운 [`Config.GetConfigForClient`](/pkg/crypto/tls/#Config.GetConfigForClient)
콜백을 사용하면 클라이언트의
[`ClientHelloInfo`](/pkg/crypto/tls/#ClientHelloInfo)를 기반으로
클라이언트에 대한 설정을 동적으로 선택할 수 있습니다. <!-- CL 31391, CL 32119 -->
[`ClientHelloInfo`](/pkg/crypto/tls/#ClientHelloInfo)
구조체에 이제 `Conn`, `SignatureSchemes` (새로운
타입인 [`SignatureScheme`](/pkg/crypto/tls/#SignatureScheme) 사용),
`SupportedProtos` 및 `SupportedVersions` 필드가 새로 추가되었습니다.

<!-- CL 32115 -->
새로운 [`Config.GetClientCertificate`](/pkg/crypto/tls/#Config.GetClientCertificate)
콜백을 사용하면, 새로운 [`CertificateRequestInfo`](/pkg/crypto/tls/#CertificateRequestInfo)로 표현되는
서버의 TLS `CertificateRequest` 메시지에 따라 클라이언트 인증서를 선택할 수 있습니다.

<!-- CL 27434 -->
새로운 [`Config.KeyLogWriter`](/pkg/crypto/tls/#Config.KeyLogWriter)를 사용하면 [WireShark](https://www.wireshark.org/) 및 유사한 도구에서 TLS 연결을 디버깅할 수 있습니다.

<!-- CL 32115 -->
새로운
[`Config.VerifyPeerCertificate`](/pkg/crypto/tls/#Config.VerifyPeerCertificate)
콜백을 통해 피어(peer)가 제시한 인증서에 대한 추가 검증이 가능합니다.

<!-- CL 18130 -->
`crypto/tls` 패키지에 CBC 패딩 오라클(padding oracles)에 대한 기본적인 대응책이 구현되었습니다. 명시적인 비밀값 의존적 타이밍(secret-dependent timings)은 없어야 하지만, 캐시 타이밍 누수를 방지하기 위해 메모리 액세스를 정규화하는 시도는 하지 않았습니다.

`crypto/tls` 패키지가 이제
X25519 및 <!-- CL 30824, CL 30825 -->
ChaCha20-Poly1305를 지원합니다. <!-- CL 30957, CL 30958 -->
이제 AES-GCM에 대한 하드웨어 지원이 없는 한 <!-- CL 32871 -->
ChaCha20-Poly1305가 우선적으로 사용됩니다.

<!-- CL 27315, CL 35290 -->
SHA-256를 사용하는 AES-128-CBC 사이퍼 수트(cipher suites)도 이제 지원되지만, 기본적으로는 비활성화되어 있습니다.

#### [crypto/x509](/pkg/crypto/x509/)

<!-- CL 24743 -->
이제 PSS 서명을 지원합니다.

<!-- CL 32644 -->
[`UnknownAuthorityError`](/pkg/crypto/x509/#UnknownAuthorityError)에 신뢰할 수 없는 인증서를 보고하는 `Cert` 필드가 추가되었습니다.

인증서 검증은 몇몇 사례에서는 더 허용적이며, 다른 몇몇 사례에서는 더 엄격합니다. <!--
crypto/x509: 리프 인증서가 루트로 직접 지정되는 것을 허용 (CL 27393)
crypto/x509: 발급자 이름이 발급자의 주체 이름과 일치하는지 확인 (CL 23571)
crypto/x509: 체인에 이미 나타난 루트는 수락하지 않음 (CL 32121)
crypto/x509: 이름 제약 조건 처리 수정 (CL 30155)
crypto/x509: RDN의 모든 이름 파싱 (CL 30810)
crypto/x509: RSA+SHA1에 대한 ISO OID 인식 (CL 27394)
crypto/x509: RSA 공개 키에 대해 NULL 파라미터 요구 (CL 16166, CL 27312)
crypto/x509: SerialNumber 누락 시 에러 반환 (CL 27238)
-->

<!-- CL 30375 -->
이제 RHEL 및 CentOS를 지원하기 위해 Linux의 `/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem` 경로에서도 루트 인증서를 검색합니다.

#### [database/sql](/pkg/database/sql/)

이제 이 패키지는 `context.Context`를 지원합니다. [`DB.QueryContext`](/pkg/database/sql/#DB.QueryContext) 및 [`DB.PrepareContext`](/pkg/database/sql/#DB.PrepareContext)와 같이 `Context`로 끝나는 새로운 메서드들이 추가되었으며, 이들은 컨텍스트 인자를 받습니다. 새로운 `Context` 메서드들을 사용하면 요청이 완료되었을 때 연결이 닫히고 연결 풀(connection pool)로 반환되는 것을 보장하며, 드라이버가 지원하는 경우 진행 중인 쿼리를 취소할 수 있고, 데이터베이스 풀이 다음 사용 가능한 연결을 기다리는 상태를 취소할 수 있게 됩니다.

이제 [`TxOptions.Isolation`](/pkg/database/sql#TxOptions.Isolation)에 격리 수준을 설정하고 이를 [`DB.BeginTx`](/pkg/database/sql#DB.BeginTx)에 전달함으로써, 트랜잭션을 시작할 때 [`IsolationLevel`](/pkg/database/sql#IsolationLevel)을 설정할 수 있습니다. 드라이버가 지원하지 않는 격리 수준을 선택한 경우 에러가 반환됩니다. 또한 [`TxOptions.ReadOnly`](/pkg/database/sql/#TxOptions.ReadOnly)를 true로 설정하여 트랜잭션에 읽기 전용 속성을 설정할 수도 있습니다.

이제 이를 지원하는 드라이버의 경우 쿼리에서 SQL 컬럼 타입 정보를 제공합니다.
Rows는 SQL 타입 정보, 컬럼 타입 길이 및 Go 타입을 포함할 수 있는 [`ColumnTypes`](/pkg/database/sql#Rows.ColumnTypes)를 반환할 수 있습니다.

[`Rows`](/pkg/database/sql/#Rows)는 이제 여러 개의 결과 집합(result sets)을 나타낼 수 있습니다. [`Rows.Next`](/pkg/database/sql/#Rows.Next)가 false를 반환한 후, [`Rows.NextResultSet`](/pkg/database/sql/#Rows.NextResultSet)을 호출하여 다음 결과 집합으로 이동할 수 있습니다. 다음 결과 집합으로 이동한 후에도 기존의 `Rows`를 계속해서 사용해야 합니다.

[`NamedArg`](/pkg/database/sql/#NamedArg)를 쿼리 인자로 사용할 수 있습니다. 새로운 [`Named`](/pkg/database/sql/#Named) 함수를 사용하면 [`NamedArg`](/pkg/database/sql/#NamedArg)를 더 간결하게 생성할 수 있습니다.

드라이버가 새로운 [`Pinger`](/pkg/database/sql/driver/#Pinger) 인터페이스를 지원하는 경우, [`DB.Ping`](/pkg/database/sql/#DB.Ping) 및 [`DB.PingContext`](/pkg/database/sql/#DB.PingContext) 메서드는 해당 인터페이스를 사용하여 데이터베이스 연결이 여전히 유효한지 확인합니다.

새로운 `Context` 쿼리 메서드는 모든 드라이버에서 작동하지만, 드라이버가 해당 메서드를 사용하도록 업데이트되지 않았다면 `Context` 취소에 응답하지 않습니다. 그 외의 기능들은 [`database/sql/driver`](/pkg/database/sql/driver)의 드라이버 지원이 필요합니다.
드라이버 작성자는 새로운 인터페이스를 검토해야 합니다. 기존 드라이버 사용자는 드라이버 문서와 각 기능에 대한 시스템별 문서를 검토하여 지원 여부를 확인해야 합니다.

#### [debug/pe](/pkg/debug/pe/)

<!-- CL 22720, CL 27212, CL 22181, CL 22332, CL 22336, Issue 15345 -->
이 패키지는 기능이 확장되었으며, 이제 [Go 링커](/cmd/link/)에서 `gcc`가 생성한 오브젝트 파일을 읽는 데 사용됩니다.
새로 추가된
[`File.StringTable`](/pkg/debug/pe/#File.StringTable)
및
[`Section.Relocs`](/pkg/debug/pe/#Section.Relocs)
필드는 COFF 문자열 테이블(string table)과 COFF 재배치(relocations)에 대한 접근을 제공합니다.
새로 추가된
[`File.COFFSymbols`](/pkg/debug/pe/#File.COFFSymbols)
를 통해 COFF 심볼 테이블에 저수준으로 접근할 수 있습니다.

#### [encoding/base64](/pkg/encoding/base64/)

<!-- CL 24964 -->
새로운
[`Encoding.Strict`](/pkg/encoding/base64/#Encoding.Strict)
메서드는 trailing padding 비트가 0이 아닐 때 디코더가 에러를 반환하도록 하는 `Encoding`을 반환합니다.

#### [encoding/binary](/pkg/encoding/binary/)

<!-- CL 28514 -->
[`Read`](/pkg/encoding/binary/#Read)
및
[`Write`](/pkg/encoding/binary/#Write)
가 이제 불리언(boolean) 타입을 지원합니다.

#### [encoding/json](/pkg/encoding/json/)

<!-- CL 18692  -->
[`UnmarshalTypeError`](/pkg/encoding/json/#UnmarshalTypeError)
에 이제 구조체(struct)와 필드 이름이 포함됩니다.

<!-- CL 31932 -->
nil [`Marshaler`](/pkg/encoding/json/#Marshaler)가
이제 JSON `null` 값으로 마샬링됩니다.

<!-- CL 21811 -->
이제 [`RawMessage`](/pkg/encoding/json/#RawMessage) 값은 해당 포인터 타입과 동일하게 마샬링(marshal)됩니다.

<!-- CL 30371 -->
[`Marshal`](/pkg/encoding/json/#Marshal)은
ES6와 동일한 형식을 사용하여 부동 소수점 숫자를 인코딩하며,
더 넓은 범위의 값에 대해 10진수(지수 표기법이 아닌) 표기법을 우선적으로 사용합니다.
특히, 2<sup>64</sup>까지의 모든 부동 소수점 정수는
동일한 `int64` 표현과 동일하게 형식화됩니다.

<!-- CL 30944 -->
이전 버전의 Go에서는 JSON `null`을 [`Unmarshaler`](/pkg/encoding/json/#Unmarshaler)로 언마샬링(unmarshaling)하는 것이 아무런 작업도 수행하지 않는 no-op으로 간주되었습니다. 이제는 `Unmarshaler`의 `UnmarshalJSON` 메서드가 JSON 리터럴 `null`과 함께 호출되며, 해당 케이스의 시맨틱을 직접 정의할 수 있습니다.

#### [encoding/pem](/pkg/encoding/pem/)

<!-- CL 27391 -->
[`Decode`](/pkg/encoding/pem/#Decode)
가 이제 종료 행의 형식을 엄격하게 검사합니다.

#### [encoding/xml](/pkg/encoding/xml/)

<!-- CL 30946 -->
[`Unmarshal`](/pkg/encoding/xml/#Unmarshal)은
이제 새로운 `",any,attr"` 구조체 태그를 사용하여 모든 속성을 수집하는
와일드카드 지원 기능을 제공합니다.

#### [expvar](/pkg/expvar/)

<!-- CL 30917 -->
새로운 메서드인
[`Int.Value`](/pkg/expvar/#Int.Value),
[`String.Value`](/pkg/expvar/#String.Value),
[`Float.Value`](/pkg/expvar/#Float.Value), 그리고
[`Func.Value`](/pkg/expvar/#Func.Value)는
내보낸 변수의 현재 값을 보고합니다.

<!-- CL 24722 -->
새로운 [`Handler`](/pkg/expvar/#Handler) 함수는 패키지의 HTTP 핸들러를 반환하여, 표준이 아닌 위치에 설치할 수 있도록 지원합니다.

#### [fmt](/pkg/fmt/)

<!-- CL 30611 -->
[`Scanf`](/pkg/fmt/#Scanf),
[`Fscanf`](/pkg/fmt/#Fscanf), 및
[`Sscanf`](/pkg/fmt/#Sscanf)가 이제
이전 릴리스보다 공백을 다르게, 그리고 더 일관되게 처리합니다.
자세한 내용은 [스캐닝 문서](/pkg/fmt/#hdr-Scanning)를
참조하십시오.

#### [go/doc](/pkg/go/doc/)

<!-- CL 29870 -->
새로운 [`IsPredeclared`](/pkg/go/doc/#IsPredeclared) 함수는 문자열이 미리 선언된 식별자(predeclared identifier)인지 여부를 보고합니다.

#### [go/types](/pkg/go/types/)

<!-- CL 30715 -->
새로운 함수
[`Default`](/pkg/go/types/#Default)
는 "untyped" 타입에 대한 기본 "typed" 타입을 반환합니다.

<!-- CL 31939 -->
`complex64`의 정렬(alignment) 방식이 이제 [Go 컴파일러](/cmd/compile/)와 일치합니다.

#### [html/template](/pkg/html/template/)

<!-- CL 14336 -->
이제 패키지에서 `<script>` 태그의 `"type"` 속성을 검증합니다.

#### [image/png](/pkg/image/png/)

<!-- CL 32143, CL 32140 -->
[`Decode`](/pkg/image/png/#Decode)
(및 `DecodeConfig`)가
이제 트루 컬러(True Color) 및 그레이스케일 투명도를 지원합니다.

<!-- CL 29872 -->
[`Encoder`](/pkg/image/png/#Encoder)
가 이제 팔레트 이미지(paletted images)를 인코딩할 때 속도가 더 빨라지고 출력 파일 크기가 더 작게 생성됩니다.

#### [math/big](/pkg/math/big/)

<!-- CL 30706 -->
새로운 메서드
[`Int.Sqrt`](/pkg/math/big/#Int.Sqrt)
는 ⌊√x⌋를 계산합니다.

새로운 메서드 [`Float.Scan`](/pkg/math/big/#Float.Scan)은 [`fmt.Scanner`](/pkg/fmt/#Scanner)를 위한 지원 루틴입니다.

[`Int.ModInverse`](/pkg/math/big/#Int.ModInverse)가 이제 음수를 지원합니다.

#### [math/rand](/pkg/math/rand/)

<!-- CL 27253, CL 33456 -->
새로운 [`Rand.Uint64`](/pkg/math/rand/#Rand.Uint64)
메서드는 `uint64` 값을 반환합니다.
새로운 [`Source64`](/pkg/math/rand/#Source64)
인터페이스는 이러한 값을 직접 생성할 수 있는 소스를 정의합니다. 그렇지 않은 경우 `Rand.Uint64` 메서드는
[`Source`](/pkg/math/rand/#Source)의
`Int63` 메서드를 두 번 호출하여 `uint64`를 구성합니다.

#### [mime](/pkg/mime/)

<!-- CL 32175 -->
[`ParseMediaType`](/pkg/mime/#ParseMediaType)가
이제 MSIE를 지원하기 위해 불필요한 백슬래시 이스케이프를 리터럴로 유지합니다.
MSIE가 전체 파일 경로를 보낼 때(“인트라넷 모드”에서), 백슬래시를 이스케이프 처리하지 않습니다: “`C:\dev\go\foo.txt`”와 같이 보내며, “`C:\\dev\\go\\foo.txt`”로 보내지 않습니다.
이제 불필요한 백슬래시 이스케이프가 발견되면, 이를 MSIE에서 보낸 것이며 리터럴 백슬래시로 의도된 것으로 간주합니다.
숫자와 문자 같은 단순 토큰 문자에 대해 불필요한 백슬래시 이스케이프를 생성하는 알려진 MIME 생성기는 없습니다.

#### [mime/quotedprintable](/pkg/mime/quotedprintable/)

[`Reader`](/pkg/mime/quotedprintable/#Reader)의 파싱 방식이 실제 환경에서 발견되는 더 많은 입력을 허용하기 위해 두 가지 방향으로 완화되었습니다. <!-- CL 32174 -->
첫째, 두 자리 16진수가 뒤따르지 않는 등호(`=`)를 리터럴 등호로 허용합니다. <!-- CL 27530 -->
둘째, 인코딩된 입력 끝에 있는 trailing 등호를 조용히 무시합니다.

#### [net](/pkg/net/)

<!-- CL 30164, CL 33473 -->
[`Conn`](/pkg/net/#Conn) 문서가 인터페이스 구현에 대한 기대 사항을 명확히 하기 위해 업데이트되었습니다. `net/http` 패키지의 업데이트는 구현체가 해당 문서를 준수하는 것을 전제로 합니다.

_업데이트:_ `Conn` 인터페이스의 구현체는 문서화된 시맨틱을 준수하는지 확인해야 합니다. [golang.org/x/net/nettest](https://godoc.org/golang.org/x/net/nettest) 패키지를 사용하여 `Conn`을 테스트하고 적절하게 동작하는지 검증할 수 있습니다.

<!-- CL 32099 -->
새로운 메서드인 [`UnixListener.SetUnlinkOnClose`](/pkg/net/#UnixListener.SetUnlinkOnClose)는 리스너가 닫힐 때 기본 소켓 파일을 파일 시스템에서 제거할지 여부를 설정합니다.

<!-- CL 29951 -->
새로운 [`Buffers`](/pkg/net/#Buffers) 타입은 메모리 상의 여러 불연속적인 버퍼로부터 네트워크에 더 효율적으로 데이터를 쓰는 것을 가능하게 합니다. 특정 머신과 특정 연결 유형의 경우, 이는 OS 전용 일괄 쓰기 작업(예: `writev`)으로 최적화됩니다.

<!-- CL 29440 -->
새로운 [`Resolver`](/pkg/net/#Resolver)는 이름과 번호를 조회하며
[`context.Context`](/pkg/context/#Context)를 지원합니다.
[`Dialer`](/pkg/net/#Dialer)에는 이제 선택 사항인
[`Resolver` 필드](/pkg/net/#Dialer.Resolver)가 추가되었습니다.

<!-- CL 29892 -->
이제 Solaris에서 [`Interfaces`](/pkg/net/#Interfaces)가 지원됩니다.

<!-- CL 29233, CL 24901 -->
이제 Go DNS 리졸버가 `resolv.conf`의 “`rotate`” 및 “`option` `ndots:0`” 옵션을 지원합니다. “`ndots`” 옵션은 이제 `libresolve`와 동일한 방식으로 준수됩니다.

#### [net/http](/pkg/net/http/)

서버 변경 사항:

- 이제 서버에서 graceful shutdown을 지원합니다. [위에서 언급됨](#http_shutdown).
  - <!-- CL 32024 -->
    [`Server`](/pkg/net/http/#Server)에
    설정 옵션인 `ReadHeaderTimeout`과 `IdleTimeout`이 추가되었으며,
    `WriteTimeout`에 대한 문서가 추가되었습니다.
  - <!-- CL 32014 -->
    [`FileServer`](/pkg/net/http/#FileServer)와
    [`ServeContent`](/pkg/net/http/#ServeContent)가
    이제 HTTP `If-Match` 조건부 요청을 지원합니다.
    이는 RFC 7232, 섹션 2.3에 따라 적절하게 포맷된 ETag에 대해 기존에 제공하던 `If-None-Match` 지원에 추가된 기능입니다.

서버의 `Handler`가 수행할 수 있는 기능에 몇 가지 추가 사항이 있습니다:

- <!-- CL 31173 -->
    [`Request.Context`](/pkg/net/http/#Request.Context)에서 반환하는 [`Context`](/pkg/context/#Context)는 기저의 `net.Conn`이 닫히면 취소됩니다. 예를 들어, 사용자가 느린 요청 도중 브라우저를 닫으면 `Handler`는 이제 사용자가 떠났음을 감지할 수 있습니다. 이는 기존의 [`CloseNotifier`](/pkg/net/http/#CloseNotifier) 지원을 보완합니다. 이 기능이 작동하려면 기저의 [`net.Conn`](/pkg/net/#Conn)이 [최근에 명확해진 인터페이스 문서](#net)를 구현해야 합니다.
  - <!-- CL 32479 -->
    헤더가 이미 작성된 후 생성된 트레일러(trailers)를 제공하려면, 새로운 [`TrailerPrefix`](/pkg/net/http/#TrailerPrefix) 메커니즘을 참조하십시오.
  - <!-- CL 33099 -->
    이제 `Handler`는 [`ErrAbortHandler`](/pkg/net/http/#ErrAbortHandler) 에러와 함께 패닉(panic)을 일으켜 응답을 중단할 수 있습니다.
  - <!-- CL 30812 -->
    [`ResponseWriter`](/pkg/net/http/#ResponseWriter)에 0바이트를 `Write` 하는 것은 이제 `ResponseWriter`가 하이잭(hijack)되었는지 테스트하는 방법으로 정의됩니다. 하이잭된 경우, `Write`는 서버의 에러 로그에 에러를 출력하지 않고 [`ErrHijacked`](/pkg/net/http/#ErrHijacked)를 반환합니다.

Client 및 Transport 변경 사항:

- <!-- CL 28930, CL 31435 -->
    이제 [`Client`](/pkg/net/http/#Client)가 리다이렉트 시 대부분의 요청 헤더를 복사합니다. 자세한 내용은 `Client` 타입의 [문서](/pkg/net/http/#Client)를 참조하십시오.
  - <!-- CL 29072 -->
    이제 [`Transport`](/pkg/net/http/#Transport)가 국제화 도메인 이름(IDN)을 지원합니다. 이에 따라 [Get](/pkg/net/http/#Get) 및 기타 헬퍼 함수들도 이를 지원합니다.
  - <!-- CL 31733, CL 29852 -->
    이제 `Client`가 301, 307, 308 리다이렉트를 지원합니다.
    예를 들어, `Client.Post`는 이제 301 리다이렉트를 따라가며, 이전에 302 및 303 리다이렉트 응답에서 그랬던 것처럼 바디가 없는 `GET` 요청으로 변환합니다.
    또한 `Client`는 이제 307 및 308 리다이렉트를 따라가며, 원래의 요청 메서드와 바디(있는 경우)를 보존합니다. 리다이렉트로 인해 요청 바디를 다시 전송해야 하는 경우, 요청에 새로운 [`Request.GetBody`](/pkg/net/http/#Request) 필드가 정의되어 있어야 합니다.
    [`NewRequest`](/pkg/net/http/#NewRequest)는 일반적인 바디 타입에 대해 `Request.GetBody`를 자동으로 설정합니다.
  - <!-- CL 32482 -->
    이제 `Transport`는 포트에 숫자가 아닌 문자가 포함된 URL 요청을 거부합니다.
  - <!-- CL 27117 -->
    이제 `Transport`는 네트워크 실패 전까지 작성된 바이트가 없고 요청 바디가 없는 경우, 멱등성(non-idempotent)이 없는 요청에 대해서도 재시도합니다.
  - <!-- CL 32481 -->
    새로운 [`Transport.ProxyConnectHeader`](/pkg/net/http/#Transport)를 통해 `CONNECT` 요청 중에 프록시로 보낼 헤더 값을 설정할 수 있습니다.
  - <!-- CL 28077 -->
    이제 [`DefaultTransport.Dialer`](/pkg/net/http/#DefaultTransport)가 `DualStack` ("[Happy Eyeballs](https://tools.ietf.org/html/rfc6555)") 지원을 활성화하여, IPv6가 실패하는 것으로 보일 때 IPv4를 백업으로 사용할 수 있습니다.
  - <!-- CL 31726 -->
    이제 [`Transport`](/pkg/net/http/#Transport)는 [`Request.ContentLength`](/pkg/net/http/#Request.ContentLength)가 0일 때, `ContentLength`가 실제로 0인지 아니면 단순히 정의되지 않은 것인지 판단하기 위해 nil이 아닌 [`Request.Body`](/pkg/net/http/#Request.Body)의 1바이트를 읽지 않습니다.
    바디의 길이가 0임을 명시적으로 나타내려면, 이를 `nil`로 설정하거나 새로운 값인 [`NoBody`](/pkg/net/http/#NoBody)로 설정하십시오.
    새로운 `NoBody` 값은 `Request` 생성자 함수에서 사용하도록 설계되었으며, [`NewRequest`](/pkg/net/http/#NewRequest)에서 사용됩니다.

#### [net/http/httptrace](/pkg/net/http/httptrace/)

<!-- CL 30359 -->
이제 새로운
[`ClientTrace.TLSHandshakeStart`](/pkg/net/http/httptrace/#ClientTrace.TLSHandshakeStart) 및
[`ClientTrace.TLSHandshakeDone`](/pkg/net/http/httptrace/#ClientTrace.TLSHandshakeDone)을 통해
클라이언트 요청의 TLS 핸드셰이크를 추적하는 기능이 지원됩니다.

#### [net/http/httputil](/pkg/net/http/httputil/)

<!-- CL 32356 -->
[`ReverseProxy`](/pkg/net/http/httputil/#ReverseProxy)에 
백엔드로부터 받은 응답을 클라이언트로 프록시하기 전에 수정할 수 있는 
새로운 선택적 훅인 [`ModifyResponse`](/pkg/net/http/httputil/#ReverseProxy.ModifyResponse)가 추가되었습니다.

#### [net/mail](/pkg/net/mail/)

<!-- CL 32176 -->
주소의 이름 부분에서 빈 따옴표 문자열(`""`)이 다시 허용됩니다. 즉, Go 1.4 및 그 이전 버전에서는 `""` `<gopher@example.com>`을 허용했으나, Go 1.5에서 이를 거부하는 버그가 도입되었습니다. 이제 해당 주소를 다시 인식합니다.

<!-- CL 31581 -->
[`Header.Date`](/pkg/net/mail/#Header.Date) 메서드는 항상 `Date:` 헤더를 파싱하는 방법을 제공해 왔습니다.
새로운 함수인 [`ParseDate`](/pkg/net/mail/#ParseDate)를 통해 `Resent-Date:` 헤더와 같은 다른 헤더 라인에서 날짜를 파싱할 수 있습니다.

#### [net/smtp](/pkg/net/smtp/)

<!-- CL 33143 -->
[`Auth.Start`](/pkg/net/smtp/#Auth)
메서드의 구현체가 빈 `toServer` 값을 반환하는 경우,
패키지는 더 이상 SMTP `AUTH` 명령에서
일부 서버가 거부했던 후행 공백(trailing whitespace)을 전송하지 않습니다.

#### [net/url](/pkg/net/url/)

<!-- CL 31322 -->
새로운 함수인
[`PathEscape`](/pkg/net/url/#PathEscape)
와
[`PathUnescape`](/pkg/net/url/#PathUnescape)
는 쿼리 이스케이프 및 언이스케이프 함수와 유사하지만,
경로 요소(path elements)를 위한 함수입니다.

<!-- CL 28933 -->
새로운 메서드인
[`URL.Hostname`](/pkg/net/url/#URL.Hostname)
및
[`URL.Port`](/pkg/net/url/#URL.Port)
는 URL의 호스트 이름과 포트 필드를 반환하며, 포트가 없을 수 있는 경우를 올바르게 처리합니다.

<!-- CL 28343 -->
기존의 [`URL.ResolveReference`](/pkg/net/url/#URL.ResolveReference) 메서드가 이제 이스케이프된 바이트가 포함된 경로를 처리할 때 이스케이프 상태를 유지하며 적절하게 처리합니다.

<!-- CL 31467 -->
이제 `URL` 타입이 [`encoding.BinaryMarshaler`](/pkg/encoding/#BinaryMarshaler) 및 [`encoding.BinaryUnmarshaler`](/pkg/encoding/#BinaryUnmarshaler)를 구현하여, [gob 데이터](/pkg/encoding/gob/)에서 URL을 처리할 수 있게 되었습니다.

<!-- CL 29610, CL 31582 -->
RFC 3986에 따라,
[`Parse`](/pkg/net/url/#Parse)
는 이제 `this_that:other/thing`과 같은 URL을 상대 경로로 해석하는 대신 거부합니다 (`this_that`은 유효한 scheme이 아닙니다).
상대 경로로 해석되도록 강제하려면,
해당 URL 앞에 “`./`”를 접두사로 붙여야 합니다.
`URL.String` 메서드는 이제 필요에 따라 이 접두사를 삽입합니다.

#### [os](/pkg/os/)

<!-- CL 16551 -->
새로운 함수 [`Executable`](/pkg/os/#Executable)은 실행 중인 실행 파일의 경로 이름을 반환합니다.

<!-- CL 30614 -->
이미 닫힌 [`os.File`](/pkg/os/#File)의 메서드를 호출하려고 하면 이제 새로운 에러 값인 [`os.ErrClosed`](/pkg/os/#ErrClosed)를 반환합니다. 이전에는 `syscall.EBADF`와 같은 시스템별 에러를 반환했습니다.

<!-- CL 31358 -->
Unix 시스템에서 [`os.Rename`](/pkg/os/#Rename)은 이제 디렉터리를 기존의 빈 디렉터리로 이름을 변경하려 할 때 에러를 반환합니다.
이전에는 비어 있지 않은 디렉터리로 이름을 변경할 때는 실패했지만, 빈 디렉터리로 변경할 때는 성공했습니다.
이로써 Unix에서의 동작이 다른 시스템들의 동작과 일치하게 되었습니다.

<!-- CL 32451 -->
Windows에서 긴 절대 경로가 이제 확장 길이 경로(“`\\?\`”로 시작하는 경로)로 투명하게 변환됩니다. 이를 통해 패키지가 경로 이름이 260자를 초과하는 파일에서도 작동할 수 있습니다.

<!-- CL 29753 -->
Windows에서 [`os.IsExist`](/pkg/os/#IsExist)는 이제 시스템 에러 `ERROR_DIR_NOT_EMPTY`에 대해 `true`를 반환합니다. 이는 Unix 에러 `ENOTEMPTY`에 대한 기존 처리 방식과 대략적으로 일치합니다.

<!-- CL 32152 -->
Plan 9에서 `#M`에 의해 제공되지 않는 파일들은 이제 [`FileInfo.Mode`](/pkg/os/#FileInfo)가 반환하는 값에 [`ModeDevice`](/pkg/os/#ModeDevice)가 설정됩니다.

#### [path/filepath](/pkg/path/filepath/)

Windows에서 발생하던 여러 버그와 코너 케이스들이 수정되었습니다:
[`Abs`](/pkg/path/filepath/#Abs)가 이제 문서에 명시된 대로 `Clean`을 호출하며,
[`Glob`](/pkg/path/filepath/#Glob)가 이제 “`\\?\c:\*`”와 매칭되고,
[`EvalSymlinks`](/pkg/path/filepath/#EvalSymlinks)가 이제 “`C:.`”를 올바르게 처리하며,
[`Clean`](/pkg/path/filepath/#Clean)이 이제 경로 시작 부분의 “`..`”를 적절하게 처리합니다.

#### [reflect](/pkg/reflect/)

<!-- CL 30088 -->
[`sort.Slice`](#sortslice)를 지원하기 위해 새로운 함수 [`Swapper`](/pkg/reflect/#Swapper)가 추가되었습니다.

#### [strconv](/pkg/strconv/)

<!-- CL 31210 -->
[`Unquote`](/pkg/strconv/#Unquote) 함수가 이제 [Go 언어 시맨틱](/ref/spec#String_literals)에 따라 백틱으로 감싸진 raw string에서 캐리지 리턴(`\r`)을 제거합니다.

#### [syscall](/pkg/syscall/)

<!-- CL 25050, CL 25022 -->
[`Getpagesize`](/pkg/syscall/#Getpagesize) 함수가 이제 상수 값이 아닌 시스템의 실제 크기를 반환합니다.
이전에는 항상 4KB를 반환했습니다.

<!-- CL 31446 -->
Solaris에서 [`Utimes`](/pkg/syscall/#Utimes)의 시그니처가 다른 모든 Unix 시스템의 시그니처와 일치하도록 변경되었습니다. 이식 가능한 코드를 작성하려면 계속해서 [`os.Chtimes`](/pkg/os/#Chtimes)를 사용하십시오.

<!-- CL 32319 -->
[`Cmsghdr`](/pkg/syscall/#Cmsghdr)에서 `X__cmsg_data` 필드가 제거되었습니다.

#### [text/template](/pkg/text/template/)

<!-- CL 31462 -->
[`Template.Execute`](/pkg/text/template/#Template.Execute)
이제 데이터 인자로 [`reflect.Value`](/pkg/reflect/#Value)를 받을 수 있으며,
[`FuncMap`](/pkg/text/template/#FuncMap)
함수 또한 `reflect.Value`를 인자로 받거나 반환할 수 있습니다.

#### [time](/pkg/time/)

<!-- CL 20118 -->
새로운 [`Until`](/pkg/time/#Until) 함수는 이와 유사한 `Since` 함수를 보완합니다.

<!-- CL 29338 -->
[`ParseDuration`](/pkg/time/#ParseDuration)
이제 긴 소수점 부분을 허용합니다.

<!-- CL 33429 -->
[`Parse`](/pkg/time/#Parse)
이제 6월 0일과 같이 월 시작 이전의 날짜를 거부합니다.
이미 6월 31일이나 7월 32일과 같이 월 말 이후의 날짜는 거부하고 있었습니다.

<!-- CL 33029 -->
<!-- CL 34816 -->
로컬 시간대 데이터베이스가 없는 시스템을 위해 `tzdata` 데이터베이스가 2016j 버전으로 업데이트되었습니다.

#### [testing](/pkg/testing/)

<!-- CL 29970 -->
새로운 메서드인
[`T.Name`](/pkg/testing/#T.Name)
(그리고 `B.Name`)은 현재
테스트 또는 벤치마크의 이름을 반환합니다.

<!-- CL 32483 -->
새로운 함수
[`CoverMode`](/pkg/testing/#CoverMode)
는 테스트 커버리지 모드를 보고합니다.

<!-- CL 32615 -->
이제 race detector가 활성화된 상태에서 실행 중 데이터 레이스(data race)가 발생하면 테스트와 벤치마크가 실패로 표시됩니다. 이전에는 개별 테스트 케이스는 통과한 것으로 나타나고, 테스트 바이너리의 전체 실행 결과만 실패로 처리되었습니다.

<!-- CL 32455 -->
문서에서 허용된 대로 [`MainStart`](/pkg/testing/#MainStart) 함수의 시그니처가 변경되었습니다. 이는 내부 구현 상세이며 Go 1 호환성 약속의 일부가 아닙니다.
`MainStart`를 직접 호출하지 않는데도 오류가 발생하는 경우, 이는 일반적으로 비어 있어야 할 `GOROOT` 환경 변수를 설정했으며, 해당 변수가 `go` 명령 바이너리의 버전과 일치하지 않음을 의미할 가능성이 높습니다.

#### [unicode](/pkg/unicode/)

<!-- CL 30935 -->
[`SimpleFold`](/pkg/unicode/#SimpleFold)
함수는 이제 입력된 값이 유효하지 않은 rune인 경우 인자를 변경 없이 그대로 반환합니다.
이전 구현에서는 인덱스 범위 체크 패닉(index bounds check panic)이 발생하며 실패했습니다.
