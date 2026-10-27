<!--
for acme:
Edit .,s;^PKG:([a-z][A-Za-z0-9_/]+);<a href="/pkg/\1/"><code>\1</code></a>;g
Edit .,s;^([a-z][A-Za-z0-9_/]+)\.([A-Z][A-Za-z0-9_]+\.)?([A-Z][A-Za-z0-9_]+)([ .',)]|$);<a href="/pkg/\1/#\2\3"><code>\3</code></a>\4;g
Edit .,s;^FULL:([a-z][A-Za-z0-9_/]+)\.([A-Z][A-Za-z0-9_]+\.)?([A-Z][A-Za-z0-9_]+)([ .',)]|$);<a href="/pkg/\1/#\2\3"><code>\1.\2\3</code></a>\4;g
Edit .,s;^DPKG:([a-z][A-Za-z0-9_/]+);<dl id="\1"><a href="/pkg/\1/">\1</a></dl>;g
rsc last updated through 6729576
-->

<!--
참고: 이 문서와 이 디렉토리의 다른 문서들에서는 `hello` `world`와 같이 고정폭 구문을 비고정폭 공백으로 설정하는 관습을 따릅니다.
이러한 구문에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

Please provide the Markdown content you would like me to translate. You have provided a `<style>` block, but no text to translate yet. Once you provide the content, I will translate it carefully into Korean while preserving all technical elements.

## Go 1.7 소개 {#introduction}

최신 Go 릴리스인 버전 1.7이 1.6 출시 6개월 만에 공개되었습니다.
변경 사항의 대부분은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언어 명세에는 한 가지 사소한 변경 사항이 있습니다.
언제나 그랬듯이, 이번 릴리스에서도 Go 1의 [호환성 약속](/doc/go1compat.html)을 유지합니다.
우리는 거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 기대합니다.

이번 릴리스에서는 [IBM LinuxOne 포트가 추가되었으며](#ports),
더 효율적인 코드를 생성하도록 [x86-64 컴파일러 백엔드가 업데이트되었고](#compiler),
[x/net 서브리포지토리](https://golang.org/x/net/context)에서 승격되어 이제 표준 라이브러리에서 사용되는 [context 패키지가](#context) 포함되었습니다.
또한 [testing 패키지](#testing)에 테스트 및 벤치마크의 계층 구조를 생성하는 기능이 추가되었습니다.
아울러 이번 릴리스에서는 Go 1.5에서 시작된 [vendoring 지원을 완료하여](#cmd_go) 표준 기능으로 만들었습니다.

## 언어 변경 사항 {#language}

이번 릴리스에서는 아주 작은 언어 사양 변경이 하나 있습니다.
[종료 문(terminating statements)](/ref/spec#Terminating_statements) 섹션에서
문장 목록이 종료 문으로 끝나는지 여부를 판단할 때,
"마지막으로 비어 있지 않은 문장(final non-empty statement)"을 끝으로 간주함을 명확히 하였으며,
이는 gc 및 gccgo 컴파일러 툴체인의 기존 동작과 일치합니다.
이전 릴리스에서는 정의가 "마지막 문장(final statement)"만을 언급하여,
뒤따르는 빈 문장들의 효과가 최소한 불분명한 상태였습니다.
[`go/types`](/pkg/go/types/)
패키지도 이 점에 있어 gc 및 gccgo 컴파일러 툴체인과 일치하도록 업데이트되었습니다.
이 변경 사항은 기존 프로그램의 정확성에는 영향을 미치지 않습니다.

## 포트 {#ports}

Go 1.7 버전부터 macOS 10.12 Sierra를 지원합니다.
1.7 이전 버전의 Go로 빌드된 바이너리는 Sierra에서 정상적으로 작동하지 않습니다.

Go 1.7에서는 [Linux on z Systems](https://en.wikipedia.org/wiki/Linux_on_z_Systems) (`linux/s390x`)에 대한 실험적인 포트와 ARM 기반 Plan 9 (`plan9/arm`)로의 포트 시작 단계가 추가되었습니다.

Go 1.6에서 추가된 64비트 MIPS(`linux/mips64` 및 `linux/mips64le`)용 실험적 Linux 포트가 이제 cgo 및 외부 링크(external linking)를 완전히 지원합니다.

리틀 엔디안 64비트 PowerPC(`linux/ppc64le`)로의 실험적 Linux 포트는 이제 POWER8 아키텍처 이상을 요구합니다.
빅 엔디안 64비트 PowerPC(`linux/ppc64`)는 POWER5 아키텍처만 요구합니다.

OpenBSD 포트는 이제 [_getentropy_(2)](https://man.openbsd.org/getentropy.2) 시스템 콜을 사용하기 위해 OpenBSD 5.6 이상 버전을 요구합니다.

### 알려진 문제 {#known_issues}

FreeBSD에서 알려져 있지만 원인이 파악되지 않은 일부 불안정성 문제가 있습니다.
이로 인해 드문 경우로 프로그램 충돌이 발생할 수 있습니다.
[issue 16136](/issue/16136),
[issue 15658](/issue/15658),
그리고 [issue 16396](/issue/16396)을 참조하십시오.
이러한 FreeBSD 전용 문제를 해결하는 데 도움을 주신다면 감사하겠습니다.

## 도구 {#tools}

### Assembler {#cmd_asm}

64비트 ARM 시스템의 경우, 벡터 레지스터 이름이 `V0`에서 `V31`로 수정되었습니다. 이전 릴리스에서는 이를 `V32`에서 `V63`으로 잘못 표기하였습니다.

64비트 x86 시스템을 위해 다음 명령어들이 추가되었습니다:
`PCMPESTRI`,
`RORXL`,
`RORXQ`,
`VINSERTI128`,
`VPADDD`,
`VPADDQ`,
`VPALIGNR`,
`VPBLENDD`,
`VPERM2F128`,
`VPERM2I128`,
`VPOR`,
`VPSHUFB`,
`VPSHUFD`,
`VPSLLD`,
`VPSLLDQ`,
`VPSLLQ`,
`VPSRLD`,
`VPSRLDQ`,
그리고
`VPSRLQ`.

### 컴파일러 툴체인 {#compiler}

이번 릴리스에는 64비트 x86 시스템을 위한 새로운 코드 생성 백엔드가 포함되었으며, 이는 [2015년의 제안](/s/go17ssa) 이후 지속적으로 개발되어 온 결과입니다.
[SSA](https://en.wikipedia.org/wiki/Static_single_assignment_form)를 기반으로 하는 새로운 백엔드는 더 간결하고 효율적인 코드를 생성하며, bounds check elimination과 같은 최적화를 위한 더 나은 플랫폼을 제공합니다.
새로운 백엔드는 벤치마크 프로그램에 필요한 CPU 시간을 5-35% 감소시킵니다.

이번 릴리스에서는 컴파일러에 `-ssa=0`을 전달하여 새로운 백엔드를 비활성화할 수 있습니다.
만약 새로운 백엔드를 비활성화해야만 프로그램이 성공적으로 컴파일되거나 실행되는 것을 발견하신다면, [버그 리포트를 제출](/issue/new)해 주세요.

패키지 아카이브에 컴파일러가 기록하는 내보내기된 메타데이터(exported metadata)의 형식이 변경되었습니다. 기존의 텍스트 형식이 더 압축된 바이너리 형식으로 대체되었습니다. 이로 인해 패키지 아카이브의 크기가 다소 줄어들었으며, 오랫동안 지속되었던 몇 가지 예외적인 케이스의 버그들이 수정되었습니다.

이번 릴리스에서는 컴파일러에 `-newexport=0`를 전달하여 새로운 export 포맷을 비활성화할 수 있습니다.
만약 새로운 export 포맷을 비활성화했을 때만 프로그램이 성공적으로 컴파일되거나 실행되는 것을 발견하신다면, [버그 리포트를 제출](/issue/new)해 주세요.

링커의 `-X` 옵션은 더 이상 특이한 두 개의 인자 형태인
`-X` `name` `value`를
지원하지 않습니다. 이는 Go 1.6 릴리스의 [공지](/doc/go1.6#compiler) 및 링커가 출력하는 경고 문구에서 안내된 바와 같습니다.
대신 `-X` `name=value` 형식을 사용하십시오.

컴파일러와 링커가 최적화되어 이번 릴리스에서는 Go 1.6보다 훨씬 빠르게 실행됩니다. 비록 여전히 우리가 원하는 수준보다는 느리지만, 향후 릴리스에서 계속해서 최적화될 예정입니다.

컴파일러 툴체인과 표준 라이브러리의 변경 사항으로 인해, 이 릴리스로 빌드한 바이너리는 일반적으로 Go 1.6으로 빌드한 바이너리보다 크기가 작으며, 때로는 20-30%까지 더 작을 수 있습니다.

x86-64 시스템에서 Go 프로그램은 이제 Linux의 perf 및 Intel의 VTune과 같은 프로파일링 도구가 기대하는 대로 스택 프레임 포인터를 유지합니다. 이를 통해 이러한 도구들을 사용하여 Go 프로그램을 분석하고 최적화하는 것이 더 쉬워졌습니다. 프레임 포인터 유지 관리로 인해 변동성이 있으나 평균 약 2% 정도의 작은 런타임 오버헤드가 발생합니다. 향후 릴리스에서 이 비용을 줄일 수 있기를 기대하고 있습니다.
프레임 포인터를 사용하지 않는 툴체인을 빌드하려면 `make.bash`, `make.bat` 또는 `make.rc`를 실행할 때 `GOEXPERIMENT=noframepointer`를 설정하십시오.

### Cgo {#cmd_cgo}

[cgo](/cmd/cgo/)를 사용하는 패키지는 이제 (C, C++, Objective C, SWIG와 더불어) Fortran 소스 파일을 포함할 수 있습니다. 다만, Go 바인딩은 여전히 C 언어 API를 사용해야 합니다.

Go 바인딩에서 이제 새로운 헬퍼 함수인 `C.CBytes`를 사용할 수 있습니다.
Go `string`을 받아 `*C.byte`(C의 `char*`)를 반환하는 `C.CString`과 달리,
`C.CBytes`는 Go `[]byte`를 받아 `unsafe.Pointer`(C의 `void*`)를 반환합니다.

`cgo`를 사용하여 빌드된 패키지와 바이너리는 임시 디렉터리 이름이 포함되는 특성 때문에, 과거 릴리스에서 빌드할 때마다 서로 다른 결과물을 생성했습니다.
충분히 최신 버전의 GCC 또는 Clang(`-fdebug-prefix-map` 옵션을 지원하는 버전)과 함께 이번 릴리스를 사용하면, 해당 빌드들이 마침내 결정론적(deterministic)으로 수행될 것입니다.

### Gccgo {#gccgo}

Go의 반기별 릴리스 일정과 GCC의 연간 릴리스 일정의 정렬로 인해,
GCC 릴리스 6에는 gccgo의 Go 1.6.1 버전이 포함되어 있습니다.
다음 릴리스인 GCC 7에는 gccgo의 Go 1.8 버전이 포함될 가능성이 높습니다.

### Go 커맨드 {#cmd_go}

[`go`](/cmd/go/) 명령어의 기본 동작은 변경되지 않았으나, 주목할 만한 몇 가지 변경 사항이 있습니다.

이번 릴리스에서는 Go 1.6 릴리스에서 [공지한](/doc/go1.6#go_command) 바와 같이 `GO15VENDOREXPERIMENT` 환경 변수에 대한 지원이 제거되었습니다.
[Vendoring 지원](/s/go15vendor)은 이제 `go` 명령어 및 툴체인의 표준 기능입니다.

`go list`에서 제공하는 `Package` 데이터 구조에 특정 패키지가 왜 stale 상태(재빌드 필요)이거나 그렇지 않은지를 설명하는 `StaleReason` 필드가 추가되었습니다. 이 필드는 `-f` 또는 `-json` 옵션을 통해 확인할 수 있으며, 타겟이 왜 재빌드되는지 이해하는 데 유용합니다.

“`go` `get`” 명령어가 이제 `git.openstack.org`를 참조하는 가져오기 경로(import paths)를 지원합니다.

이번 릴리스에서는 소스 코드 없이 바이너리 형태로 배포되는 [binary-only packages](/pkg/go/build#hdr-Binary_Only_Packages)를 사용하여 프로그램을 빌드할 수 있도록 실험적인 최소 지원 기능을 추가합니다. 이 기능은 일부 상용 환경에서 필요하지만, 툴체인의 나머지 부분에 완전히 통합되도록 설계되지는 않았습니다. 예를 들어, 전체 소스 코드에 접근할 수 있다고 가정하는 도구들은 이러한 패키지에서 작동하지 않으며, “`go` `get`” 명령에서 이러한 패키지를 지원할 계획은 없습니다.

### Go doc {#cmd_doc}

“`go` `doc`” 명령어가 이제 [`godoc`](/cmd/godoc/)을 따라 생성자(constructors)를 해당 생성자가 생성하는 타입과 함께 그룹화하여 표시합니다.

### Go vet {#cmd_vet}

“`go` `vet`” 명령은
`-copylock` 및 `-printf` 검사에서 더 정확한 분석을 제공하며,
테스트 함수일 가능성이 높은 함수의 이름과 시그니처를 검사하는 새로운 `-tests` 검사가 추가되었습니다.
새로운 `-tests` 검사와의 혼동을 피하기 위해, 기존의 공개되지 않았던
`-test` 옵션이 제거되었습니다. 해당 옵션은 `-all` `-shadow`와 동일하게 동작했습니다.

`vet` 명령에는 새로운 검사 옵션인 `-lostcancel`이 추가되었습니다. 이 옵션은 Go 1.7의 새로운 `context` 패키지( [아래](#context) 참조)에서 `WithCancel`, `WithTimeout`, `WithDeadline` 함수가 반환하는 취소 함수(cancellation function)를 호출하지 않은 경우를 감지합니다. 이 함수를 호출하지 않으면, 부모 컨텍스트가 취소될 때까지 새로운 `Context`가 회수되지 않습니다. (백그라운드 컨텍스트는 절대 취소되지 않습니다.)

### Go tool dist {#cmd_dist}

새로운 서브커맨드 “`go` `tool` `dist` `list`”는 지원되는 모든 운영체제/아키텍처 쌍을 출력합니다.

### Go tool trace {#cmd_trace}

Go 1.5에서 [도입된](/doc/go1.5#trace_command) “`go` `tool` `trace`” 명령은 여러 방면으로 개선되었습니다.

첫째, 트레이스(trace) 수집 효율이 이전 릴리스보다 훨씬 향상되었습니다.
이번 릴리스에서 트레이스 수집으로 인한 일반적인 실행 시간 오버헤드는 약 25%인 반면,
이전 릴리스에서는 최소 400%였습니다.
둘째, 이제 트레이스 파일에 파일 및 라인 번호 정보가 포함되어
파일 자체의 독립성이 높아졌으며, 트레이스 도구를 실행할 때
원본 실행 파일이 필수가 아니게 되었습니다.
셋째, 이제 트레이스 도구가 브라우저 기반 뷰어의 제한을 피하기 위해
대규모 트레이스를 분할하여 저장합니다.

이번 릴리스에서 트레이스 파일 형식이 변경되었지만, Go 1.7 도구들은 여전히 이전 릴리스의 트레이스를 읽을 수 있습니다.

## 성능 {#performance}

언제나 그렇듯, 변경 사항이 매우 일반적이고 다양하기 때문에 성능에 대해 정확하게 진술하기는 어렵습니다.
가비지 컬렉터의 속도 향상과 코어 라이브러리의 최적화 덕분에 대부분의 프로그램이 조금 더 빠르게 실행될 것입니다.
x86-64 시스템의 경우, 새로운 컴파일러 백엔드가 제공하는 생성 코드 개선 덕분에 많은 프로그램이 훨씬 더 빠르게 실행될 것입니다.
위에서 언급했듯이, 자체 벤치마크 결과 코드 생성 변경만으로도 일반적으로 프로그램의 CPU 시간이 5-35% 감소했습니다.

<!-- git log -''-grep '-[0-9][0-9]\.[0-9][0-9]%' go1.6.. -->
다음 패키지들의 구현체에서 10% 이상의 성능 향상을 가져오는 상당한 최적화가 이루어졌습니다:
[`crypto/sha1`](/pkg/crypto/sha1/),
[`crypto/sha256`](/pkg/crypto/sha256/),
[`encoding/binary`](/pkg/encoding/binary/),
[`fmt`](/pkg/fmt/),
[`hash/adler32`](/pkg/hash/adler32/),
[`hash/crc32`](/pkg/hash/crc32/),
[`hash/crc64`](/pkg/hash/crc64/),
[`image/color`](/pkg/image/color/),
[`math/big`](/pkg/math/big/),
[`strconv`](/pkg/strconv/),
[`strings`](/pkg/strings/),
[`unicode`](/pkg/unicode/),
그리고
[`unicode/utf16`](/pkg/unicode/utf16/).

유휴 상태의 goroutine 수가 많거나, 스택 크기의 변동이 심하거나, 패키지 수준 변수가 많은 프로그램의 경우, 가비지 컬렉션(Garbage collection) 일시 중단 시간이 Go 1.6 때보다 상당히 짧아질 것입니다.

## 표준 라이브러리 {#library}

### 컨텍스트 {#context}

Go 1.7에서는 `golang.org/x/net/context` 패키지가 표준 라이브러리의 [`context`](/pkg/context/)로 이동되었습니다.
이를 통해 아래에 언급된 [net](#net), [net/http](#net_http), [os/exec](#os_exec)를 포함한 다른 표준 라이브러리 패키지에서 취소, 타임아웃 및 요청 범위 데이터(request-scoped data) 전달을 위해 컨텍스트(context)를 사용할 수 있게 되었습니다.

context에 대한 자세한 내용은 [패키지 문서](/pkg/context/)와 Go 블로그 포스트 “[Go Concurrent Patterns: Context](/blog/context)”를 참조하세요.

### HTTP 트레이싱 {#httptrace}

Go 1.7에서는 HTTP 요청 내의 이벤트를 추적하기 위한 메커니즘을 제공하는 패키지인 [`net/http/httptrace`](/pkg/net/http/httptrace/)가 도입되었습니다.

### 테스트 {#testing}

`testing` 패키지가 이제 서브테스트(subtests)를 포함한 테스트 정의와 서브벤치마크(sub-benchmarks)를 포함한 벤치마크 정의를 지원합니다.
이 지원을 통해 테이블 기반 벤치마크(table-driven benchmarks)를 작성하고 계층적 테스트를 생성하는 것이 쉬워졌습니다.
또한 공통 설정(setup) 및 정리(tear-down) 코드를 공유하는 방법도 제공합니다.
자세한 내용은 [패키지 문서](/pkg/testing/#hdr-Subtests_and_Sub_benchmarks)를 참조하십시오.

### 런타임 {#runtime}

이제 런타임에서 시작되는 모든 패닉은 [언어 명세](/ref/spec#Run_time_panics)에서 [요구하는 바와 같이]( /ref/spec#Run_time_panics), 내장 [`error`](/ref/spec#Errors)와 [`runtime.Error`](/pkg/runtime/#Error)를 모두 구현하는 패닉 값을 사용합니다.

패닉(panic) 발생 시, 시그널의 이름을 알 수 있다면 스택 트레이스에 해당 이름이 출력됩니다.
그렇지 않은 경우에는 Go1.7 이전과 마찬가지로 시그널 번호가 사용됩니다.

새로운 함수 [`KeepAlive`](/pkg/runtime/#KeepAlive)는 할당된 객체가 프로그램의 특정 시점에서 도달 가능(reachable)한 것으로 간주되어야 함을 선언하는 명시적인 메커니즘을 제공하며, 이는 일반적으로 연결된 파이널라이저(finalizer)의 실행을 지연시키기 위해 사용됩니다.

새로운 함수인 [`CallersFrames`](/pkg/runtime/#CallersFrames)는 [`Callers`](/pkg/runtime/#Callers)에서 얻은 PC 슬라이스를 호출 스택에 해당하는 프레임 시퀀스로 변환합니다. 프레임 시퀀스는 인라인 함수 호출이 포함된 호출 스택을 더 정확하게 설명할 수 있으므로, [`FuncForPC`](/pkg/runtime/#FuncForPC)를 직접 사용하는 대신 이 새로운 API를 사용하는 것이 권장됩니다.

새로운 함수 [`SetCgoTraceback`](/pkg/runtime/#SetCgoTraceback)은 cgo를 통해 호출되어 동일한 프로세스 내에서 실행되는 Go 코드와 C 코드 간의 더 긴밀한 통합을 지원합니다.

32비트 시스템에서 런타임은 이제 주소 공간 어디에서나 운영 체제에 의해 할당된 메모리를 사용할 수 있으며, 이를 통해 일부 환경에서 흔히 발생하던 “memory allocated by OS not in usable range” 오류가 제거되었습니다.

이제 모든 아키텍처에서 런타임이 사용하지 않는 메모리를 운영 체제로 반환할 수 있습니다.
Go 1.6 및 이전 버전에서는 ARM64, 64비트 PowerPC 또는 MIPS에서 메모리를 해제할 수 없었습니다.

Windows에서 Go 1.5 및 그 이전 버전의 Go 프로그램은 시작 시 `timeBeginPeriod(1)`을 호출하여 전역 Windows 타이머 해상도를 1ms로 강제 설정했습니다.
전역 타이머 해상도를 변경하는 것은 일부 시스템에서 문제를 일으켰으며, 테스트 결과 스케줄러의 우수한 성능을 위해 해당 호출이 필요하지 않은 것으로 나타나 Go 1.6에서 이 호출이 제거되었습니다.
Go 1.7에서는 이 호출이 다시 도입되었습니다. 일부 워크로드에서는 스케줄러의 우수한 성능을 위해 여전히 이 호출이 필요하기 때문입니다.

### 라이브러리의 마이너 변경 사항 {#minor_library_changes}

언제나 그렇듯, Go 1의 [호환성 약속](/doc/go1compat)을 염두에 둔 라이브러리의 다양한 소규모 변경 및 업데이트가 이루어졌습니다.

#### [bufio](/pkg/bufio/)

이전 버전의 Go에서는 [`Reader`](/pkg/bufio/#Reader)의 [`Peek`](/pkg/bufio/#Reader.Peek) 메서드에 기본 버퍼의 크기보다 더 많은 바이트를 요청하면, 빈 슬라이스와 `ErrBufferFull` 에러를 반환했습니다. 이제는 `ErrBufferFull` 에러와 함께 기본 버퍼 전체를 반환합니다.

#### [bytes](/pkg/bytes/)

[`strings`](/pkg/strings/) 패키지와의 대칭성을 위해 새로운 함수인 [`ContainsAny`](/pkg/bytes/#ContainsAny)와 [`ContainsRune`](/pkg/bytes/#ContainsRune)이 추가되었습니다.

이전 버전의 Go에서는 [`Reader`](/pkg/bytes/#Reader)의 [`Read`](/pkg/bytes/#Reader.Read) 메서드에 남은 데이터가 없는 상태에서 0바이트를 요청하면, 0의 카운트와 에러 없음(no error)을 반환했습니다. 이제는 0의 카운트와 [`io.EOF`](/pkg/io/#EOF) 에러를 반환합니다.

[`Reader`](/pkg/bytes/#Reader) 타입에 `Reader`를 재사용할 수 있도록 하는 새로운 메서드 [`Reset`](/pkg/bytes/#Reader.Reset)이 추가되었습니다.

#### [compress/flate](/pkg/compress/flate/)

패키지 전반에 걸쳐 많은 성능 최적화가 이루어졌습니다.
압축 해제 속도는 약 10% 향상되었으며,
`DefaultCompression`의 압축 속도는 두 배 더 빨라졌습니다.

이러한 일반적인 개선 사항 외에도, `BestSpeed` 압축기가 완전히 교체되어 [Snappy](https://github.com/google/snappy)와 유사한 알고리즘을 사용하게 되었습니다. 이로 인해 속도가 약 2.5배 향상되었으나, 출력물 크기는 이전 알고리즘보다 5-10% 더 커질 수 있습니다.

또한 Lempel-Ziv 인코딩은 적용하지 않고 Huffman 인코딩만 적용하는 새로운 압축 레벨인 `HuffmanOnly`가 추가되었습니다. [Lempel-Ziv 인코딩을 생략하면](https://blog.klauspost.com/constant-time-gzipzip-compression/) `HuffmanOnly`는 새로운 `BestSpeed`보다 약 3배 빠르게 동작하지만, 압축 결과물의 크기가 `BestSpeed`로 생성한 것보다 20-40% 더 커진다는 단점이 있습니다.

`BestSpeed`와 `HuffmanOnly` 모두 [RFC 1951](https://tools.ietf.org/html/rfc1951)을 준수하는 압축 출력물을 생성한다는 점에 유의하십시오.
다시 말해, 모든 유효한 DEFLATE 압축 해제 도구는 이러한 출력물들을 계속해서 압축 해제할 수 있습니다.

마지막으로, [`io.Reader`](/pkg/io/#Reader)를 구현하는 압축 해제기(decompressor)에 소소한 변경 사항이 있습니다. 이전 버전에서는 더 이상 읽을 수 있는 바이트가 전혀 없을 때까지 [`io.EOF`](/pkg/io/#EOF) 보고를 지연했습니다. 이제는 마지막 바이트 집합을 읽을 때 [`io.EOF`](/pkg/io/#EOF)를 더 빠르게 보고합니다.

#### [crypto/tls](/pkg/crypto/tls/)

TLS 구현은 각 연결의 처음 몇 개의 데이터 패킷을 작은 레코드 크기로 전송하며, 점진적으로 TLS 최대 레코드 크기까지 늘립니다. 이러한 휴리스틱은 첫 번째 패킷을 복호화하기 전까지 수신해야 하는 데이터 양을 줄여, 저대역폭 네트워크에서의 통신 지연 시간을 개선합니다.

[`Config`](/pkg/crypto/tls/#Config)의 `DynamicRecordSizingDisabled` 필드를 true로 설정하면, 연결 시작부터 패킷을 가능한 한 크게 전송하던 Go 1.6 및 그 이전 버전의 동작 방식으로 강제됩니다.

이제 TLS 클라이언트는 [`Config`](/pkg/crypto/tls/#Config)의 `Renegotiation` 필드를 설정하여 활성화할 수 있는, 서버 시작 재협상(server-initiated renegotiation)에 대한 선택적이고 제한적인 지원을 제공합니다. 이는 많은 Microsoft Azure 서버에 연결하는 데 필요합니다.

이제 이 패키지에서 반환하는 오류는 일관되게 `tls:` 접두사로 시작합니다.
이전 릴리스에서는 일부 오류에 `crypto/tls:` 접두사가 사용되었고, 일부는 `tls:` 접두사를 사용했으며, 일부는 접두사가 전혀 없었습니다.

셀프 사인 인증서를 생성할 때, 이제 이 패키지는 기본적으로 “Authority Key Identifier” 필드를 설정하지 않습니다.

#### [crypto/x509](/pkg/crypto/x509/)

새로운 함수 [`SystemCertPool`](/pkg/crypto/x509/#SystemCertPool)은 사용 가능한 경우 시스템 인증서 풀 전체에 대한 접근을 제공합니다.
또한 이와 관련된 새로운 에러 타입인 [`SystemRootsError`](/pkg/crypto/x509/#SystemRootsError)가 추가되었습니다.

#### [debug/dwarf](/pkg/debug/dwarf/)

[`Reader`](/pkg/debug/dwarf/#Reader) 타입의 새로운 [`SeekPC`](/pkg/debug/dwarf/#Reader.SeekPC) 메서드와 [`Data`](/pkg/debug/dwarf/#Data) 타입의 새로운 [`Ranges`](/pkg/debug/dwarf/#Ranges) 메서드는 [`LineReader`](/pkg/debug/dwarf/#LineReader)에 전달할 컴파일 단위(compilation unit)를 찾고, 주어진 프로그램 카운터(program counter)에 해당하는 특정 함수를 식별하는 데 도움을 줍니다.

#### [debug/elf](/pkg/debug/elf/)

새로운 [`R_390`](/pkg/debug/elf/#R_390) 재배치(relocation) 타입과 다수의 사전 정의된 상수는 S390 포트를 지원합니다.

#### [encoding/asn1](/pkg/encoding/asn1/)

ASN.1 디코더가 이제 최소값이 아닌 정수 인코딩(non-minimal integer encodings)을 거부합니다.
이로 인해 이전에는 허용되었으나 유효하지 않은 일부 ASN.1 데이터가 거부될 수 있습니다.

#### [encoding/json](/pkg/encoding/json/)

[`Encoder`](/pkg/encoding/json/#Encoder)의 새로운 [`SetIndent`](/pkg/encoding/json/#Encoder.SetIndent) 메서드는 최상위 [`Indent`](/pkg/encoding/json/#Indent) 함수와 마찬가지로 JSON 인코딩을 위한 들여쓰기 매개변수를 설정합니다.

[`Encoder`](/pkg/encoding/json/#Encoder)의 새로운 [`SetEscapeHTML`](/pkg/encoding/json/#Encoder.SetEscapeHTML) 메서드는 따옴표로 둘러싸인 문자열 내의 `&`, `<`, `>` 문자를 각각 `\u0026`, `\u003c`, `\u003e`로 이스케이프 처리할지 여부를 제어합니다. 이전 릴리스와 마찬가지로, 인코더는 JSON을 HTML에 임베딩할 때 발생할 수 있는 특정 문제들을 방지하기 위해 기본적으로 이 이스케이프 처리를 적용합니다.

이전 버전의 Go에서 이 패키지는 문자열 타입의 키를 사용하는 맵의 인코딩 및 디코딩만 지원했습니다.

Go 1.7부터는 정수 타입의 키를 사용하는 맵에 대한 지원이 추가되었습니다. 인코딩 시 JSON 키로 따옴표로 둘러싸인 10진수 표현을 사용합니다.

또한 Go 1.7에서는 `MarshalText` ([`encoding.TextMarshaler`](/pkg/encoding/#TextMarshaler) 참조) 메서드를 구현하는 비문자열 키를 사용하는 맵의 인코딩 지원과, `UnmarshalText` ([`encoding.TextUnmarshaler`](/pkg/encoding/#TextUnmarshaler) 참조) 메서드를 구현하는 비문자열 키를 사용하는 맵의 디코딩 지원이 추가되었습니다.

이전 버전의 Go에서 사용된 인코딩 및 디코딩 방식을 유지하기 위해, 문자열 타입의 키에 대해서는 이러한 메서드들이 무시됩니다.

타입이 지정된 바이트 슬라이스를 인코딩할 때, [`Marshal`](/pkg/encoding/json/#Marshal)은 이제 해당 바이트 타입에 `MarshalJSON` 또는 `MarshalText` 메서드가 있는 경우 이를 사용하여 인코딩된 요소들의 배열을 생성하며, 두 메서드 모두 없는 경우에만 기본값인 base64 인코딩 문자열 데이터로 대체합니다.

이전 버전의 Go는 기존의 base64 인코딩 문자열 인코딩과 배열 인코딩(바이트 타입이 적절하게 `UnmarshalJSON` 또는 `UnmarshalText`를 구현하고 있다고 가정할 때)을 모두 허용하므로, 선택된 인코딩 방식은 변경되었더라도 이 변경 사항은 이전 버전의 Go와 의미론적으로 하위 호환됩니다.

#### [go/build](/pkg/go/build/)

`go` 커맨드의 바이너리 전용(binary-only) 패키지에 대한 새로운 지원과 cgo 기반 패키지의 Fortran 코드 지원을 구현하기 위해, [`Package`](/pkg/go/build/#Package) 타입에 `BinaryOnly`, `CgoFFLAGS`, 및 `FFiles` 필드가 새롭게 추가되었습니다.

#### [go/doc](/pkg/go/doc/)

위에서 설명한 `go` `test` 의 해당 변경 사항을 지원하기 위해, [`Example`](/pkg/go/doc/#Example) 구조체에 예제 출력 라인이 어떤 순서로든 생성될 수 있는지를 나타내는 `Unordered` 필드가 추가되었습니다.

#### [io](/pkg/io/)

이 패키지는 [`Seeker`](/pkg/io/#Seeker) 구현체와 함께 사용할 수 있는 새로운 상수 `SeekStart`, `SeekCurrent`, `SeekEnd`를 추가합니다.
이 상수들은 `os.SEEK_SET`, `os.SEEK_CUR`, `os.SEEK_END`보다 권장되지만, 후자들은 호환성을 위해 유지됩니다.

#### [math/big](/pkg/math/big/)

[`Float`](/pkg/math/big/#Float) 타입은 [`GobEncode`](/pkg/math/big/#Float.GobEncode) 및 [`GobDecode`](/pkg/math/big/#Float.GobDecode) 메서드를 추가하여, 이제 `Float` 타입의 값을 [`encoding/gob`](/pkg/encoding/gob/) 패키지를 사용하여 인코딩하고 디코딩할 수 있습니다.

#### [math/rand](/pkg/math/rand/)

[`Read`](/pkg/math/rand/#Read) 함수와 [`Rand`](/pkg/math/rand/#Rand)의 [`Read`](/pkg/math/rand/#Rand.Read) 메서드는 이제 입력 버퍼의 크기에 의존하지 않고 일관된 의사 난수 바이트 스트림을 생성합니다.

문서에 따르면 `Rand`의 [`Seed`](/pkg/math/rand/#Rand.Seed) 및 [`Read`](/pkg/math/rand/#Rand.Read) 메서드는 동시에 호출하는 것이 안전하지 않지만, 전역 함수인 [`Seed`](/pkg/math/rand/#Seed)와 [`Read`](/pkg/math/rand/#Read)는 안전하며(항상 그래왔습니다) 동시에 호출할 수 있습니다.

#### [mime/multipart](/pkg/mime/multipart/)

[`Writer`](/pkg/mime/multipart/#Writer) 구현이 이제 각 멀티파트 섹션의 헤더를 키 기준으로 정렬하여 출력합니다. 이전에는 맵(map)을 통한 반복 작업으로 인해 섹션 헤더가 비결정적인 순서로 사용되었습니다.

#### [net](/pkg/net/)

[context](#context) 도입의 일환으로, [`Dialer`](/pkg/net/#Dialer) 타입에 [`Dial`](/pkg/net/#Dialer.Dial)과 유사하지만 다이얼 작업(dial operation)을 위한 [`context.Context`](/pkg/context/#Context)가 추가된 새로운 메서드 [`DialContext`](/pkg/net/#Dialer.DialContext)가 추가되었습니다.
이 컨텍스트는 `Dialer`의 `Cancel` 및 `Deadline` 필드를 대체하기 위해 도입되었으나, 하위 호환성을 위해 구현상으로는 계속해서 해당 필드들을 존중합니다.

[`IP`](/pkg/net/#IP) 타입의 [`String`](/pkg/net/#IP.String) 메서드가 유효하지 않은 `IP` 주소에 대한 결과 값을 변경했습니다.
이전 릴리스에서는 `IP` 바이트 슬라이스의 길이가 0, 4, 16이 아닌 경우 `String`이 `"?"`를 반환했습니다.
Go 1.7에서는 `"?12ab"`와 같이 바이트의 16진수 인코딩을 추가합니다.

순수 Go [이름 분석](/pkg/net/#hdr-Name_Resolution) 구현이 이제 로컬 파일(즉, `/etc/hosts`) 조회와 비교하여 DNS 조회의 우선순위에 대해 `nsswitch.conf`에 명시된 기본 설정을 준수합니다.

#### [net/http](/pkg/net/http/)

[`ResponseWriter`](/pkg/net/http/#ResponseWriter)의 문서에는 이제 응답 작성을 시작하면 이후에 요청 본문(request body)을 읽는 것이 제한될 수 있음이 명시되어 있습니다.
최대한의 호환성을 위해, 응답의 어느 부분이라도 작성하기 전에 요청 본문을 완전히 읽는 구현 방식을 권장합니다.

[context](#context) 도입의 일환으로, [`Request`](/pkg/net/http/#Request)에 연관된 컨텍스트를 가져오는 [`Context`](/pkg/net/http/#Request.Context) 메서드와, 수정된 컨텍스트를 가진 `Request` 복사본을 생성하는 [`WithContext`](/pkg/net/http/#Request.WithContext) 메서드가 새롭게 추가되었습니다.

[`Server`](/pkg/net/http/#Server) 구현에서, [`Serve`](/pkg/net/http/#Server.Serve)는 요청 컨텍스트(request context)에 `ServerContextKey` 키를 사용하여 기반이 되는 `*Server`와, `LocalAddrContextKey` 키를 사용하여 요청을 수신한 로컬 주소([`Addr`](/pkg/net/#Addr))를 모두 기록합니다. 예를 들어, 요청을 수신한 주소는 `req.Context().Value(http.LocalAddrContextKey).(net.Addr)`입니다.

서버의 [`Serve`](/pkg/net/http/#Server.Serve) 메서드는 이제 `Server.TLSConfig` 필드가 `nil`이거나 `TLSConfig.NextProtos`에 `"h2"`가 포함되어 있는 경우에만 HTTP/2 지원을 활성화합니다.

이제 서버 구현에서 프로토콜 요구 사항에 따라 100보다 작은 응답 코드를 세 자리로 패딩합니다. 이에 따라 `w.WriteHeader(5)`는 HTTP 응답 상태로 `5`가 아닌 `005`를 사용합니다.

이제 서버 구현에서 `chunked`가 명시적으로 설정되었을 때 [RFC 7230](https://tools.ietf.org/html/rfc7230#section-3.3.1)에 따라 "Transfer-Encoding" 헤더를 단 하나만 올바르게 전송합니다.

이제 서버 구현에서 유효하지 않은 HTTP 버전의 요청을 거부하는 기준이 더 엄격해졌습니다.
HTTP/0.x라고 주장하는 유효하지 않은 요청은 이제 거부되며(HTTP/0.9는 완전히 지원된 적이 없습니다),
"PRI \* HTTP/2.0" 업그레이드 요청을 제외한 평문 HTTP/2 요청 또한 이제 거부됩니다.
서버는 암호화된 HTTP/2 요청을 계속해서 처리합니다.

서버에서 타임아웃 핸들러가 상태 코드로 0을 반환하는 대신, 빈 응답 본문과 함께 200 상태 코드를 반환합니다.

클라이언트에서 [`Transport`](/pkg/net/http/#Transport) 구현은 요청 컨텍스트를 원격 서버에 연결하는 모든 dial 작업으로 전달합니다.
커스텀 dialer가 필요한 경우, 전송 계층(transport)이 컨텍스트를 제공할 수 있도록 기존의 `Dial` 필드보다 새로운 `Transport` 필드인 `DialContext`를 사용하는 것이 권장됩니다.

[`Transport`](/pkg/net/http/#Transport)는 유휴 상태이거나 잦은 통신을 주고받는 서버로 인해 소비되는 클라이언트 리소스를 제어하는 데 도움이 되는 `IdleConnTimeout`, `MaxIdleConns`, `MaxResponseHeaderBytes` 필드를 추가로 제공합니다.

[`Client`](/pkg/net/http/#Client)의 설정된 `CheckRedirect` 함수가 이제 `ErrUseLastResponse`를 반환하여, 가장 최근의 리다이렉트 응답을 HTTP 요청의 결과로 반환해야 함을 나타낼 수 있습니다.
해당 응답은 이제 `CheckRedirect` 함수에서 `req.Response`로 사용할 수 있습니다.

Go 1부터 HTTP 클라이언트의 기본 동작은 `Accept-Encoding` 요청 헤더를 사용하여 서버 측 압축을 요청한 다음, 응답 본문을 투명하게(transparently) 압축 해제하는 것입니다. 이 동작은 [`Transport`](/pkg/net/http/#Transport)의 `DisableCompression` 필드를 사용하여 조정할 수 있습니다. Go 1.7에서는 HTTP 프록시 구현을 돕기 위해, [`Response`](/pkg/net/http/#Response)에 추가된 `Uncompressed` 필드를 통해 이러한 투명한 압축 해제가 수행되었는지 여부를 보고합니다.

[`DetectContentType`](/pkg/net/http/#DetectContentType)는 몇 가지 새로운 오디오 및 비디오 콘텐츠 유형에 대한 지원을 추가합니다.

#### [net/http/cgi](/pkg/net/http/cgi/)

[`Handler`](/pkg/net/http/cgi/#Handler)에는 자식 프로세스의 표준 에러(standard error)를 호스트 프로세스의 표준 에러와 다른 곳으로 리다이렉션할 수 있도록 하는 새로운 필드 `Stderr`가 추가되었습니다.

#### [net/http/httptest](/pkg/net/http/httptest/)

새로운 함수 [`NewRequest`](/pkg/net/http/httptest/#NewRequest)는 테스트 중에 [`http.Handler`](/pkg/net/http/#Handler)로 전달하기에 적합한 새로운 [`http.Request`](/pkg/net/http/#Request)를 준비합니다.

[`ResponseRecorder`](/pkg/net/http/httptest/#ResponseRecorder)의 새로운 [`Result`](/pkg/net/http/httptest/#ResponseRecorder.Result) 메서드는 기록된 [`http.Response`](/pkg/net/http/#Response)를 반환합니다. 응답의 헤더(headers)나 트레일러(trailers)를 확인해야 하는 테스트는 `ResponseRecorder`의 `HeaderMap`에 직접 접근하는 대신 `Result`를 호출하여 응답 필드를 검사해야 합니다.

#### [net/http/httputil](/pkg/net/http/httputil/)

[`ReverseProxy`](/pkg/net/http/httputil/#ReverseProxy) 구현이 이제 백엔드에 연결할 수 없을 때 “502 Bad Gateway”로 응답합니다. 이전 릴리스에서는 “500 Internal Server Error”로 응답했습니다.

[`ClientConn`](/pkg/net/http/httputil/#ClientConn)와
[`ServerConn`](/pkg/net/http/httputil/#ServerConn) 모두 deprecated로 문서화되었습니다.
이들은 저수준(low-level)의 오래된 기능이며, Go의 현재 HTTP 스택에서 사용되지 않으므로
더 이상 업데이트되지 않습니다.
대신
[`http.Client`](/pkg/net/http/#Client),
[`http.Transport`](/pkg/net/http/#Transport),
및
[`http.Server`](/pkg/net/http/#Server)를
사용해야 합니다.

#### [net/http/pprof](/pkg/net/http/pprof/)

`/debug/pprof/trace` 경로를 처리하도록 설치된 런타임 트레이스 HTTP 핸들러가 이제 `seconds` 쿼리 파라미터에서 소수점 숫자를 허용하여, 1초 미만의 간격으로 트레이스를 수집할 수 있게 되었습니다. 이는 특히 부하가 많은 서버에서 유용합니다.

#### [net/mail](/pkg/net/mail/)

이제 주소 파서는 [RFC 6532](https://tools.ietf.org/html/rfc6532)에 따라 주소 내의 이스케이프 되지 않은 UTF-8 텍스트를 허용하지만, 결과에 어떠한 정규화(normalization)도 적용하지 않습니다. 이전 버전의 메일 파서와의 호환성을 위해, 주소 인코더(즉, [`Address`](/pkg/net/mail/#Address)의 [`String`](/pkg/net/mail/#Address.String) 메서드)는 계속해서 [RFC 5322](https://tools.ietf.org/html/rfc5322)에 따라 모든 UTF-8 텍스트를 이스케이프 처리합니다.

[`ParseAddress`](/pkg/net/mail/#ParseAddress) 함수와 [`AddressParser.Parse`](/pkg/net/mail/#AddressParser.Parse) 메서드는 더 엄격해졌습니다. 이전에는 이메일 주소 뒤에 오는 모든 문자를 무시했지만, 이제는 공백 이외의 문자가 있을 경우 에러를 반환합니다.

#### [net/url](/pkg/net/url/)

[`URL`](/pkg/net/url/#URL)의 새로운 `ForceQuery` 필드는 URL에 쿼리 문자열이 반드시 포함되어야 하는지 여부를 기록합니다. 이는 쿼리 문자열이 없는 URL(예: `/search`)과 빈 쿼리 문자열이 있는 URL(예: `/search?`)을 구분하기 위함입니다.

#### [os](/pkg/os/)

[`IsExist`](/pkg/os/#IsExist)는 이제 해당 오류가 존재하는 시스템에서 `syscall.ENOTEMPTY`에 대해 true를 반환합니다.

Windows에서,
[`Remove`](/pkg/os/#Remove)가 이제 가능한 경우 읽기 전용 파일까지 삭제하여,
구현 방식이 non-Windows 시스템과 동일하게 동작합니다.

#### [os/exec](/pkg/os/exec/)

[context](#context) 도입의 일환으로,
새로운 생성자인
[`CommandContext`](/pkg/os/exec/#CommandContext)는
[`Command`](/pkg/os/exec/#Command)와 비슷하지만, 명령 실행을 취소하는 데 사용할 수 있는 context를 포함합니다.

#### [os/user](/pkg/os/user/)

[`Current`](/pkg/os/user/#Current) 함수가 이제 cgo를 사용할 수 없는 환경에서도 구현되었습니다.

새로운 [`Group`](/pkg/os/user/#Group) 타입과
[`LookupGroup`](/pkg/os/user/#LookupGroup) 및
[`LookupGroupId`](/pkg/os/user/#LookupGroupId) 조회 함수,
그리고 `User` 구조체의 새로운 필드인 `GroupIds`는
시스템별 사용자 그룹 정보에 대한 액세스를 제공합니다.

#### [reflect](/pkg/reflect/)

[`Value`](/pkg/reflect/#Value)의 [`Field`](/pkg/reflect/#Value.Field) 메서드는 지정된 필드 번호 `i`가 범위를 벗어날 경우 패닉(panic)이 발생한다고 항상 문서화되어 있었으나, 실제로는 조용히 zero [`Value`](/pkg/reflect/#Value)를 반환해 왔습니다.
Go 1.7에서는 이 메서드가 문서에 기술된 대로 동작하도록 변경되었습니다.

새로운 [`StructOf`](/pkg/reflect/#StructOf) 함수는 런타임에 구조체 타입을 생성합니다.
이 함수는 [`ArrayOf`](/pkg/reflect/#ArrayOf), [`ChanOf`](/pkg/reflect/#ChanOf), [`FuncOf`](/pkg/reflect/#FuncOf), [`MapOf`](/pkg/reflect/#MapOf), [`PtrTo`](/pkg/reflect/#PtrTo), [`SliceOf`](/pkg/reflect/#SliceOf)와 함께 타입 생성자 세트를 완성합니다.

[`StructTag`](/pkg/reflect/#StructTag)의 새로운 메서드인 [`Lookup`](/pkg/reflect/#StructTag.Lookup)은 [`Get`](/pkg/reflect/#StructTag.Get)과 유사하지만, 태그에 주어진 키가 포함되어 있지 않은 경우와 주어진 키에 빈 문자열이 연결되어 있는 경우를 구분합니다.

[`Type`](/pkg/reflect/#Type) 및 [`Value`](/pkg/reflect/#Value)의 [`Method`](/pkg/reflect/#Type.Method)와 [`NumMethod`](/pkg/reflect/#Type.NumMethod) 메서드는 더 이상 공개되지 않은(unexported) 메서드를 반환하거나 계산하지 않습니다.

#### [strings](/pkg/strings/)

이전 Go 릴리스에서는 [`Reader`](/pkg/strings/#Reader)의 [`Read`](/pkg/strings/#Reader.Read) 메서드가 남은 데이터가 없는 상태에서 0바이트를 요청받으면, 0의 카운트와 에러 없음(no error)을 반환했습니다. 이제는 0의 카운트와 [`io.EOF`](/pkg/io/#EOF) 에러를 반환합니다.

[`Reader`](/pkg/strings/#Reader) 타입에 `Reader`를 재사용할 수 있도록 하는 새로운 메서드 [`Reset`](/pkg/strings/#Reader.Reset)이 추가되었습니다.

#### [time](/pkg/time/)

[`Duration`](/pkg/time/#Duration)의 `time.Duration.String` 메서드가 이제 제로 duration을 `"0"`이 아닌 `"0s"`로 보고합니다.
[`ParseDuration`](/pkg/time/#ParseDuration)은 계속해서 두 가지 형태를 모두 허용합니다.

`time.Local.String()` 메서드 호출이 이제 모든 시스템에서 `"Local"`을 반환합니다. 이전 릴리스에서는 Windows에서 빈 문자열을 반환했습니다.

`$GOROOT/lib/time`에 있는 시간대 데이터베이스가 IANA 릴리스 2016d로 업데이트되었습니다.
이 폴백(fallback) 데이터베이스는 Windows와 같이 시스템 시간대 데이터베이스를 찾을 수 없는 경우에만 사용됩니다.
Windows 시간대 약어 목록 또한 업데이트되었습니다.

#### [syscall](/pkg/syscall/)

Linux에서
[`SysProcAttr`](/pkg/syscall/#SysProcAttr) 구조체
([`os/exec.Cmd`](/pkg/os/exec/#Cmd)의 `SysProcAttr` 필드에서 사용됨)
에 새로운 `Unshareflags` 필드가 추가되었습니다.
이 필드가 0이 아니면,
[`ForkExec`](/pkg/syscall/#ForkExec)
(`exec.Cmd`의 `Run` 메서드에서 사용됨)
에 의해 생성된 자식 프로세스는 새로운 프로그램을 실행하기 전에
[_unshare_(2)](https://man7.org/linux/man-pages/man2/unshare.2.html)
시스템 콜을 호출합니다.

#### [unicode](/pkg/unicode/)

[`unicode`](/pkg/unicode/) 패키지와 시스템 전반의 관련 지원 사항이 버전 8.0에서 [Unicode 9.0](https://www.unicode.org/versions/Unicode9.0.0/)으로 업그레이드되었습니다.
