<!--
참고: 이 문서와 이 디렉토리에 있는 다른 문서에서, 고정 폭 문구를 비고정 폭 공백으로 표현하는 것이 관례입니다. 예를 들어, `hello` `world`와 같습니다.
이러한 문구에서 내부 태그를 제거하는 CL을 보내지 마세요.
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.8 소개 {#introduction}

이 문서는 Go 1.8 버전의 주요 기능과 변경 사항을 소개합니다.

가장 최신 Go 릴리스인 버전 1.8은 [Go 1.7](go1.7) 이후 6개월 후에 출시되었습니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
언어 사양에 [두 가지 주요 변경 사항](#language)이 있습니다.
항상처럼, 이 릴리스는 Go 1의 [호환성 보장](/doc/go1compat.html)을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일 및 실행될 것으로 예상합니다.

이 릴리스는 [32비트 MIPS 지원 추가](#ports),
[컴파일러 백엔드를 업데이트하여 더욱 효율적인 코드를 생성](#compiler),
[GC 일시 중단 시 스택 재검색을 제거하여 GC 일시 중단을 줄임](#gc),
[HTTP/2 푸시 지원 추가](#h2push),
[HTTP 미세 종료 지원 추가](#http_shutdown),
[더 많은 컨텍스트 지원 추가](#more_context),
[뮤텍스 프로파일링 활성화](#mutex_prof),
그리고 [슬라이스 정렬 단순화](#sort_slice)를 제공합니다.

## 언어 변경 사항 {#language}

명시적으로 값을 한 구조체 유형에서 다른 구조체 유형으로 변환할 때,
Go 1.8부터는 태그가 무시됩니다. 따라서 태그만 다른 두 구조체는 서로 변환될 수 있습니다:

```markdown
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
	v1 = T1(v2) // 이제 유효
}
```

<!-- CL 17711 -->
언어 사양은 이제 구현이 부동 소수점 상수에 대해 최대 16비트 지수를 지원하도록 요구합니다. 이는 `[`gc`](/cmd/compile/)` 또는 `gccgo` 컴파일러에 영향을 미치지 않으며, 이 두 컴파일러는 여전히 32비트 지수를 지원합니다.

## 포트

Go는 Linux에서 32비트 MIPS를 지원하며, big-endian (`linux/mips`) 및 little-endian (`linux/mipsle`) 시스템 모두에 적용 가능합니다. 이러한 시스템은 MIPS32r1 명령어 세트와 함께 FPU 또는 커널 FPU 에뮬레이션을 구현해야 합니다. 참고: 많은 일반적인 MIPS 기반 라우터에는 FPU가 없으며, 펌웨어가 커널 FPU 에뮬레이션을 활성화하지 않습니다. 이러한 시스템에서는 Go가 실행되지 않습니다.

DragonFly BSD에서는 Go는 이제 DragonFly 4.4.4 또는 그 이후 버전을 필요로 합니다. <!-- CL 29491, CL 29971 -->

OpenBSD에서 Go는 이제 OpenBSD 5.9 이상이 필요합니다. <!-- CL 34093 -->

현재 Plan 9 포트의 네트워킹 지원이 훨씬 더 완전해졌으며, Unix 및 Windows와 동일하게 데드라인 및 취소에 대한 동작을 따릅니다. Plan 9 커널 요구 사항에 대한 내용은 [Plan 9 위키 페이지](/wiki/Plan9)를 참조하십시오.

Go 1.8는 이제 OS X 10.8 또는 이후 버전을만 지원합니다. 이는 10.8를 지원하는 마지막 Go 릴리스일 가능성이 높습니다. 이전 버전의 OS X에서 Go를 컴파일하거나 실행 파일을 실행하는 것은 아직 테스트되지 않았습니다.

Go 1.8은 Linux를 ARMv5E 및 ARMv6 프로세서에서 지원하는 마지막 버전입니다:
Go 1.9는 아마도 ARMv6K (Raspberry Pi 1에 사용되는 것과 동일) 또는 이후 버전을 요구할 것입니다.
Linux 시스템이 ARMv6K 또는 이후인지 확인하려면 다음 명령을 실행하십시오:
`go tool dist -check-armv6k`
(테스트를 용이하게 하기 위해 Go 1.8의 전체 복사본을 설치하지 않고도 시스템에 `dist` 명령을 복사할 수도 있습니다)
그리고 프로그램이 "ARMv6K supported."라는 출력으로 종료되면, 해당 시스템은 ARMv6K 또는 이후를 구현합니다.
Linux가 아닌 ARM 시스템에서는 이미 ARMv6K 또는 이후가 필요합니다.

<!-- CL 31596, go.dev/issue/17528 -->
`zos`는 이제 `GOOS`에 대해 인식되는 값으로, z/OS 운영 체제에 예약되어 있습니다.

### 알려진 문제 {#known_issues}

FreeBSD와 NetBSD에서 알려진 있지만 이해되지 않는 불안정성이 있습니다.
이로 인해 드물게 프로그램이 충돌할 수 있습니다.
자세한 내용은 다음 링크를 참조하세요.
[문제 15658](/issue/15658) 및
[문제 16511](/issue/16511).
이러한 문제 해결에 도움이 필요합니다.

## 도구 {#tools}

### 어셈블러 {#cmd_asm}

64비트 x86 시스템용으로 다음과 같은 명령어들이 추가되었습니다:
`VBROADCASTSD`,
`BROADCASTSS`,
`MOVDDUP`,
`MOVSHDUP`,
`MOVSLDUP`,
`VMOVDDUP`,
`VMOVSHDUP`, 및
`VMOVSLDUP`.

64비트 PPC 시스템의 경우, 다음과 같은 일반적인 벡터 스칼라 명령어가 추가되었습니다:
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
`yacc` 도구 (이전에는 "`go` `tool` `yacc`"를 실행하여 사용 가능)가 제거되었습니다.
Go 1.7부터는 Go 컴파일러에서 더 이상 사용되지 않습니다.
이제 "tools" 저장소로 이동했으며 다음 위치에서 사용할 수 있습니다:
[`golang.org/x/tools/cmd/goyacc`](https://godoc.org/golang.org/x/tools/cmd/goyacc).

### 해결 {#tool_fix}

<!-- CL 28872 -->
`fix` 도구가 새로운 기능인 "`context`"을 도입하여
import을 "golang.org/x/net/context"에서 "[`context`](/pkg/context/)"으로 변경합니다.

### Pprof {#tool_pprof}

<!-- CL 33157 -->
`pprof` 도구를 사용하여 TLS 서버를 프로파일링하고, "`https+insecure`" URL 스킴을 사용하여 인증서 검증을 건너뛸 수 있습니다.

<!-- CL 23781 -->
`callgrind`의 출력 결과는 이제 명령어 수준의 세분성을 갖게 되었습니다.

### 추적 {#tool_trace}

<!-- CL 23324 -->
`trace` 도구는 실행 기록에서 pprof 호환되는 블로킹 및 지연도 프로필을 생성하기 위한 새로운 `-pprof` 플래그를 제공합니다.

<!-- CL 30017, CL 30702 -->
가비지 컬렉션 이벤트가 실행 추적 뷰어에서 더 명확하게 표시됩니다. 가비지 컬렉션 활동은 별도의 행에 표시되며, GC 헬퍼 고루틴은 역할에 따라 표시됩니다.

### Vet {#tool_vet}

동물병원 검사는 일부 측면에서 더 엄격하고, 이전에는 오탐을 유발했던 부분에서는 더 유연합니다.

Vet now는 다음과 같은 사항을 확인합니다.
* 배열의 잠금 복사
* 중복된 JSON 및 XML 구조체 필드 태그
* 공백으로 구분되지 않은 구조체 태그
* HTTP `Response.Body.Close` 호출의 지연 (오류 확인 전)
* `Printf`에서 인덱싱된 인자

또한 기존 검사를 개선합니다.

### 컴파일러 도구 체인 {#compiler}

Go 1.7에서는 64비트 x86 시스템용 새로운 컴파일러 백엔드가 도입되었습니다.
Go 1.8에서는 해당 백엔드가 더욱 발전되었으며 현재 모든 아키텍처에서 사용됩니다.

새로운 백엔드, [정적 단일 할당 형태](https://en.wikipedia.org/wiki/Static_single_assignment_form) (SSA)를 기반으로 하여,
더욱 간결하고 효율적인 코드를 생성하며,
경계 검사 제거와 같은 최적화에 대한 더 나은 플랫폼을 제공합니다.
새로운 백엔드는 32비트 ARM 시스템에서
저희의 벤치마크 프로그램에 필요한 CPU 시간을 20-30% 감소시킵니다.
이미 Go 1.7에서 SSA 백엔드를 사용하던 64비트 x86 시스템의 경우, 그 효과는 더욱 미미한 0-10%입니다. 다른 아키텍처는 32비트 ARM 수치와 유사한 수준의 개선을 보일 가능성이 큽니다.

Go 1.7에 도입된 임시 `-ssa=0` 컴파일러 플래그, 새로운 백엔드를 비활성화하는 기능은 Go 1.8에서 제거되었습니다.

뿐만 아니라 모든 시스템에서 새로운 컴파일러 백엔드를 활성화하는 것 외에도,
Go 1.8은 새로운 컴파일러 프론트엔드를 도입합니다. 새로운 컴파일러
프론트엔드는 사용자가 인지하지 못하도록 설계되었지만, 향후 성능 개선을 위한 기반이 됩니다.

컴파일러와 링커는 이번 릴리스에서 Go 1.7보다 최적화되어 더 빠르게 실행되지만, 여전히 원하는 만큼 빠르지는 않으며, 향후 릴리스에서 계속 최적화될 예정입니다.
이전 릴리스에 비해 Go 1.8은 [약 15% 더 빠름](https://dave.cheney.net/2016/11/19/go-1-8-toolchain-improvements)

### Cgo {#cmd_cgo}

<!-- CL 31141 -->
Go 도구가 `make.bash`에서 설정된 `CGO_ENABLED` 환경 변수의 값을 기억하고, 이를 기본적으로 모든 후속 컴파일에 적용하여 문제 [#12808](/issue/12808)을 해결합니다.
네이티브 컴파일을 수행할 때, `make.bash`가 올바른 설정을 자동으로 감지하므로 `CGO_ENABLED` 환경 변수를 명시적으로 설정하는 것은 일반적으로 필요하지 않습니다. `CGO_ENABLED` 환경 변수를 명시적으로 설정하는 주요 이유는 다음과 같습니다.
* 환경이 CGO를 지원하지만, 명시적으로 CGO 지원을 원하지 않는 경우입니다. 이 경우, `make.bash` 또는 `all.bash`에서 `CGO_ENABLED=0`을 설정합니다.

<!-- CL 29991 -->
환경 변수 `PKG_CONFIG`를 사용하여 프로그램을 실행하도록 설정할 수 있습니다. 이 설정은 `#cgo` `pkg-config` 지시문을 처리하도록 지정합니다. 기본값은 `pkg-config`이며, 이전 버전에서 항상 사용되었습니다. 이는 특히 크로스 컴파일을 더 쉽게 만들어줍니다.
[cgo](/cmd/cgo/)

<!-- CL 32354 -->
[cgo](/cmd/cgo/) 도구가 이제 `-srcdir` 옵션을 지원하며, 이는 [go](/cmd/go/) 명령에서 사용됩니다.

<!-- CL 31768, 31811 -->
`[cgo](/cmd/cgo/)` 코드에서 `C.malloc`를 호출하고,
`malloc`가 `NULL`을 반환하면, 프로그램은 이제
메모리 부족 오류로 인해 충돌합니다.
`C.malloc`는 절대 `nil`을 반환하지 않습니다.
대부분의 C 함수와 달리, `C.malloc`는 `errno` 값을 반환하는 두 개의 결과 형태로는 사용할 수 없습니다.

<!-- CL 33237 -->
`[cgo](/cmd/cgo/)`을 사용하여 C 함수를 호출하고, C 유니온에 포인터 값을 전달하는 경우, 만약 C 유니온이 어떤 포인터 값도 포함할 수 있고, `[cgo pointer checking](/cmd/cgo/#hdr-Passing_pointers)`이 활성화되어 있는 경우 (기본적으로 활성화되어 있음), 유니온 값은 Go 포인터로 검사됩니다.

### Gccgo {#gccgo}

Go의 반기별 릴리즈 일정이 GCC의 연간 릴리즈 일정과 겹쳐서,
GCC 6에는 Go 1.6.1 버전의 gccgo가 포함됩니다.
다음 릴리즈인 GCC 7에는 Go 1.8 버전의 gccgo가 포함될 것으로 예상합니다.

### 기본 GOPATH {#gopath}

[`GOPATH`
환경 변수는 설정되지 않은 경우 기본값을 갖습니다. Unix에서는 `$HOME/go`로, Windows에서는 `%USERPROFILE%/go`로 기본값이 설정됩니다.

### Go get {#go_get}

<!-- CL 34818 -->
`go get` 명령은 이제 `<code style="white-space:nowrap">-insecure</code>` 플래그가 사용되었는지 여부에 관계없이 항상 HTTP 프록시 환경 변수를 존중합니다. 이전 버전에서는 `<code style="white-space:nowrap">-insecure</code>` 플래그가 프록시 사용을 방지하는 부작용이 있었습니다.

### Go 버그 {#go_bug}

새로운
“[`go`](/cmd/go/#hdr-Print_information_for_bug_reports)”
명령은 GitHub에서 버그 보고서를 시작하고, 현재 시스템에 대한 정보를 미리 채워 넣습니다.

### Go 문서 {#cmd_doc}

<!-- CL 25419 -->
"[`go` `doc`](/cmd/go/#hdr-Show_documentation_for_package_or_symbol)"
명령이 이제 상수와 변수를 해당 유형과 함께 그룹화하여,
[`godoc`](/cmd/godoc/)의 동작을 따릅니다.

<!-- CL 25420 -->
`doc`의 출력을 더 읽기 쉽게 만들기 위해, 첫 번째 레벨 항목의 각 요약은 단일 줄을 차지하도록 보장됩니다.

<!-- CL 31852 -->
인터페이스 정의 내의 특정 메서드에 대한 설명서를 이제 요청할 수 있습니다. 예를 들어 "`go` `doc` `net.Conn.SetDeadline`"와 같습니다.

### 플러그인 {#plugin}

Go는 이제 "plugin" 빌드 모드를 통해 Go로 작성된 플러그인을 생성하고, 실행 시간에 이러한 플러그인을 로드하기 위한 새로운 [`plugin`](/pkg/plugin/) 패키지를 제공합니다. 플러그인 지원은 현재 Linux에서만 사용 가능합니다. 문제가 발생하면 알려주세요.

## 런타임 {#runtime}

### 논산성 {#liveness}

<!-- Issue 15843 -->
가비지 컬렉터는 이제 함수 전체에서 변수를 유효하다고 간주하지 않습니다. 자세한 내용 및 변수를 계속 유효하게 유지하는 방법에 대한 내용은 Go 1.7에 추가된 [`runtime.KeepAlive`](/pkg/runtime/#KeepAlive) 함수를 참조하십시오.

_업데이트:_
할당된 객체에 최종 처리자를 설정하는 코드는 해당 객체를 사용하는 함수나 메서드에서 `runtime.KeepAlive` 호출을 추가해야 할 수 있습니다.
자세한 내용은 [`KeepAlive`
문서](/pkg/runtime/#KeepAlive) 및 예제를 참조하십시오.

### 동시 맵의 오용 {#mapiter}

```go
// ConcurrentMap은 여러 고루틴에서 동시에 접근할 수 있는 맵입니다.
// 그러나 잘못 사용하면 데이터 경쟁 및 기타 문제가 발생할 수 있습니다.
// 예를 들어, 여러 고루틴이 동시에 맵에 쓰려고 하면 데이터가 손상될 수 있습니다.

// 다음은 ConcurrentMap을 오용하는 예입니다.
//
// ```go
// import "sync"
//
// var mu sync.Mutex
//
// func main() {
//   myMap := make(map[string]int)
//
//   var wg sync.WaitGroup
//   for i := 0; i < 10; i++ {
//     wg.Add(1)
//     go func(i int) {
//       defer wg.Done()
//
//       mu.Lock()
//       myMap[fmt.Sprintf("key%d", i)] = i
//       mu.Unlock()
//     }(i)
//   }
//
//   wg.Wait()
//
//   // myMap의 내용 확인
//   // ...
// }
// ```
//
// 위 코드는 여러 고루틴이 동시에 `myMap`에 데이터를 쓰려고 시도합니다.
// 각 고루틴은 `mu.Lock()`을 사용하여 맵에 접근하고, `mu.Unlock()`을 사용하여 맵에 접근을 해제합니다.
// 그러나 여러 고루틴이 동시에 `mu.Lock()`을 얻으면 데이터 경쟁이 발생할 수 있습니다.
//
// 데이터 경쟁을 방지하기 위해 `mu`를 여러 번 사용해야 합니다.
// 예를 들어, 각 고루틴이 맵에 쓰기 전에 `mu.Lock()`을 한 번 호출하고, 쓰기를 완료한 후에는 `mu.Unlock()`을 한 번 호출해야 합니다.
//
// 또한 고루틴이 맵에 쓰기 전에 잠금을 획득하는 순서를 제어하는 데 도움이 되는 `sync.RWMutex`를 사용할 수도 있습니다.
//
// ```go
// import "sync"
//
// var mu sync.RWMutex
//
// func main() {
//   myMap := make(map[string]int)
//
//   var wg sync.WaitGroup
//   for i := 0; i < 10; i++ {
//     wg.Add(1)
//     go func(i int) {
//       defer wg.Done()
//
//       mu.Lock()
//       myMap[fmt.Sprintf("key%d", i)] = i
//       mu.Unlock()
//     }(i)
//   }
//
//   wg.Wait()
//
//   // myMap의 내용 확인
//   // ...
// }
// ```
//
// `sync.RWMutex`는 읽기 작업을 여러 고루틴이 동시에 수행할 수 있게 하지만, 쓰기 작업은 한 번에 한 고루틴만 수행할 수 있도록 합니다.
// 이것은 데이터 경쟁을 방지하는 데 도움이 됩니다.
//
// 맵을 동시 사용하기 전에 `sync.Mutex` 또는 `sync.RWMutex`를 사용하여 동시성을 제어하는 것이 중요합니다.
//

Go 1.6에서 런타임은
[가벼운, 최선을 다한 방식의 동시 맵 오용 감지 기능이 추가되었습니다](/doc/go1.6#runtime). 이 릴리스는 프로그램을 동시 맵에 쓰거나 동시에 반복하는 경우를 감지하는 기능을 개선합니다.

항상, 만약 하나의 goroutine이 맵에 쓰고 있다면, 다른 goroutine은 맵을 읽거나 (반복 포함) 동시적으로 쓰지 않아야 합니다.
런타임이 이러한 조건을 감지하면, 진단 메시지를 출력하고 프로그램을 종료합니다.
문제에 대해 더 자세히 알아보기 위한 가장 좋은 방법은 다음을 실행하는 것입니다.
[레이스 검출기](/blog/race-detector),
이 도구는 레이스를 더 신뢰성 있게 감지하고 더 자세한 정보를 제공합니다.

### MemStats 문서 {#memstats}

<!-- CL 28972 -->
`runtime.MemStats` 타입에 대한 설명이 더욱 상세하게 제공되었습니다.

## 성능 {#performance}

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, world!")
}
```

항상처럼, 변경 사항이 너무 일반적이고 다양하여 정확한 성능에 대한 진술을 내리는 것은 어렵습니다.
대부분의 프로그램은 
가비지 컬렉터의 개선 및
표준 라이브러리의 최적화를 통해 약간 더 빠르게 실행될 것입니다.

다음 패키지에서 최적화가 이루어졌습니다:
[`bytes`](/,
[`crypto/aes`](/,
[`crypto/cipher`](/,
[`crypto/elliptic`](/,
[`crypto/sha256`](/,
[`crypto/sha512`](/,
[`encoding/asn1`](/,
[`encoding/csv`](/,
[`encoding/hex`](/,
[`encoding/json`](/,
[`hash/crc32`](/,
[`image/color`](/,
[`image/draw`](/,
[`math`](/,
[`math/big`](/,
[`reflect`](/,
[`regexp`](/,
[`runtime`](/,
[`strconv`](/,
[`strings`](/,
[`syscall`](/,
[`text/template`](/,
[`unicode/utf8`](/).

### 가비지 컬렉터 {#gc}

수집 중 일시 중지는 Go 1.7보다 훨씬 짧아야 하며, 일반적으로 100 마이크로초 미만이고 종종 10 마이크로초 수준이어야 합니다.
[글로벌 스택 재검사를 제거하는 방법에 대한 문서](https://github.com/golang/proposal/blob/master/design/17503-eliminate-rescan.md)를 참조하십시오. Go 1.9에 대해서는 더 많은 작업이 남아 있습니다.

### 지연 실행 {#defer}

<!-- CL 29656, CL 29656 -->

[지연된
함수 호출]의 오버헤드는 약 절반으로 줄었습니다.

### Cgo {#cgoperf}

Go에서 C로의 호출 오버헤드는 약 절반으로 줄었습니다.

## 표준 라이브러리 {#library}

### 예제 {#examples}

다양한 패키지에 대한 설명서에 예제가 추가되었습니다.

### 슬라이스 정렬 {#sort_slice}

[sort](/pkg/sort/) 패키지는
이제 _less_ 함수를 사용하여 슬라이스를 정렬하는 데 유용한
[`Slice`](/pkg/sort/#Slice) 함수를 포함합니다.
많은 경우에 이로 인해 새로운 정렬 유형을 작성할 필요가 없습니다.

다음은 새 기능입니다.
[`SliceStable`](/pkg/sort/#SliceStable) 및
[`SliceIsSorted`](/pkg/sort/#SliceIsSorted).

### HTTP/2 푸시 {#h2push}

`[net/http](/pkg/net/http/)` 패키지는 이제 `[`Handler`](/pkg/net/http/#Handler)에서 HTTP/2 서버 푸시를 보내는
기전을 제공합니다.
기존의 `Flusher` 및 `Hijacker` 인터페이스와 유사하게, HTTP/2 `[`ResponseWriter`](/pkg/net/http/#ResponseWriter)는 이제 새로운 `[`Pusher`](/pkg/net/http/#Pusher) 인터페이스를 구현합니다.

### HTTP 서버의 부드러운 종료 {#http_shutdown}

<!-- CL 32329 -->
HTTP 서버는 이제 새로운
[`Server.Shutdown`](/pkg/net/http/#Server.Shutdown)
메서드를 사용하여 부드러운 종료를 지원하고, 새로운
[`Server.Close`](/pkg/net/http/#Server.Close)
메서드를 사용하여 갑작스러운 종료를 지원합니다.

### 더 많은 컨텍스트 지원 {#more_context}

계속 [Go 1.7의 `context.Context`](/pkg/context/#Context)
채택을 표준 라이브러리로 확장하는 것은 Go 1.8에서 기존 패키지에 더 많은 컨텍스트 지원을 추가합니다:

- 새로운 `Server.Shutdown` 기능은 컨텍스트 인수를 받습니다.
  - `database/sql` 패키지에 컨텍스트 지원과 관련된 상당한 기능이 추가되었습니다. ([/pkg/database/sql/](https://pkg.go.dev/database/sql))
  - 새로운 `net.Resolver`의 모든 9개의 `Lookup` 메서드는 이제 컨텍스트를 받습니다.

### 뮤텍스 경쟁 프로파일링 {#mutex_prof}

현재 런타임 및 도구는 경쟁적인 뮤텍스 프로파일링을 지원합니다.

대부분의 사용자는 새로운 `-mutexprofile` 플래그와 “[`go` `test`](/cmd/go/#hdr-Description_of_testing_flags)”를 사용하고, 그 결과 파일에서 [pprof](/cmd/pprof/)을 사용하는 것을 선호할 것입니다.

다음과 같은 저수준 지원도 새 기능인
[`MutexProfile`](/pkg/runtime/#MutexProfile) 및
[`SetMutexProfileFraction`](/pkg/runtime/#SetMutexProfileFraction)를 통해 제공됩니다.

Go 1.8에서 알려진 제한 사항은 프로파일이
[`sync.Mutex`](/pkg/sync/#Mutex)에 대한 경쟁만 보고한다는 것입니다.
[`sync.RWMutex`](/pkg/sync/#RWMutex)는 보고하지 않습니다.

### 라이브러리의 미세 조정 {#minor_library_changes}

물론, 라이브러리에는 항상 다양한 미세한 변경 사항 및 업데이트가 있으며, 이는 Go 1의 [호환성]( /doc/go1compat)을 염두에 두고 개발되었습니다. 다음 섹션에서는 사용자에게 보이는 변경 사항 및 추가 사항을 나열합니다.
최적화 및 미세한 버그 수정 사항은 나열되지 않습니다.

#### [archive/tar](/pkg/archive/tar/)

<!-- CL 28471, CL 31440, CL 31441, CL 31444, CL 28418, CL 31439 -->
tar 구현은 파일 형식의 다양한 예외 상황에서 많은 버그를 수정합니다.
[`Reader`](/pkg/archive/tar/#Reader)
은 이제 8GB 이상의 크기를 가진 PAX 형식의 tar 파일을 처리할 수 있습니다.
[`Writer`](/pkg/archive/tar/#Writer)
은 더 이상 긴 경로 이름이 포함된 특정 상황에서 유효하지 않은 tar 파일을 생성하지 않습니다.

#### [compress/flate](/pkg/compress/flate/)

<!-- CL 31640, CL 31174, CL 32149 -->
인코더에 대한 몇 가지 작은 수정 사항이 추가되어 특정 상황에서 압축 비율을 개선했습니다. 그 결과, `DEFLATE`의 정확한 인코딩된 출력은 Go 1.7과 다를 수 있습니다. 왜냐하면 `DEFLATE`는 gzip, png, zlib, zip 등의 압축 방식이기 때문이며, 이러한 형식의 출력도 변경되었을 수 있습니다.

<!-- CL 31174 -->
인코더가 `NoCompression`
[`NoCompression`](/pkg/compress/flate/#NoCompression)
모드로 작동할 때, 이제 전달된 슬라이스의 크기에 의존하지 않고 일관된 출력을 생성합니다.
`Write`
[`Write`](/pkg/compress/flate/#Writer.Write)
메서드에 전달된 슬라이스의 크기에 관계없이.

<!-- CL 28216 -->
디코더는 오류가 발생했을 때, 저장된 데이터를 압축 해제하지 않고 함께 오류를 반환합니다.

#### [compress/gzip](/pkg/compress/gzip/)

[`Writer`](/pkg/compress/gzip/#Writer)
이제 `MTIME` 필드를 0으로 인코딩할 때,
[`Header.ModTime`](/pkg/compress/gzip/#Header)
필드가 0 값일 때 동작합니다.
이전 Go 버전에서는 `Writer`가
무의미한 값을 인코딩했습니다.
마찬가지로,
[`Reader`](/pkg/compress/gzip/#Reader)
이제 0으로 인코딩된 `MTIME` 필드를
`Header.ModTime`이 0인 것으로 보고합니다.

#### [컨텍스트](/pkg/context/)

<!-- CL 30370 -->
`DeadlineExceeded` (`/pkg/context#DeadlineExceeded`)
오류가 이제
`net.Error` (`/pkg/net/#Error`)
을 구현하고 `Timeout` 및 `Temporary` 메서드 모두에 대해 `true`를 보고합니다.

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 25159, CL 31318 -->
새로운 방법
[`Conn.CloseWrite`](/pkg/crypto/tls/#Conn.CloseWrite)
을 사용하여 TLS 연결을 부분적으로 닫을 수 있습니다.

<!-- CL 28075 -->
새로운 방법
[`Config.Clone`](/pkg/crypto/tls/#Config.Clone)
은 TLS 구성 설정을 복제합니다.

<!-- CL 30790 -->
새로운 [`Config.GetConfigForClient`](/pkg/crypto/tls/#Config.GetConfigForClient)
콜백을 사용하면, 클라이언트의
[`ClientHelloInfo`](/pkg/crypto/tls/#ClientHelloInfo)를 기반으로 동적으로 클라이언트용 설정을 선택할 수 있습니다. <!-- CL 31391, CL 32119 -->
[`ClientHelloInfo`](/pkg/crypto/tls/#ClientHelloInfo)
구조는 이제 `Conn`, `SignatureSchemes` (새로운
형식 [`SignatureScheme`](/pkg/crypto/tls/#SignatureScheme)를 사용), `SupportedProtos`, 및 `SupportedVersions`와 같은 새로운 필드를 가집니다.

<!-- CL 32115 -->
새로운 `Config.GetClientCertificate` 콜백을 통해 서버의
TLS `CertificateRequest` 메시지에 기반하여 클라이언트 인증서를 선택할 수 있습니다. 이를 위해 새로운
`CertificateRequestInfo`가 사용됩니다.

<!-- CL 27434 -->
새로운
[`Config.KeyLogWriter`](/pkg/crypto/tls/#Config.KeyLogWriter)
은 TLS 연결 디버깅을
[WireShark](https://www.wireshark.org/) 및
유사한 도구에서 가능하게 합니다.

<!-- CL 32115 -->
새로운
[`Config.VerifyPeerCertificate`](/pkg/crypto/tls/#Config.VerifyPeerCertificate)
콜백은 동료가 제시한 인증서에 대한 추가적인 검증을 허용합니다.

<!-- CL 18130 -->
`crypto/tls` 패키지는 이제 CBC 패딩 오라클에 대한 기본적인 방어 메커니즘을 구현합니다. 명시적인 비밀번호에 의존하는 시간 차이를 방지하지만, 캐시 타이밍 누출을 방지하기 위해 메모리 액세스를 정상화하려고 시도하지 않습니다.

`crypto/tls` 패키지는 이제
X25519 및 <!-- CL 30824, CL 30825 -->
ChaCha20-Poly1305를 지원합니다. <!-- CL 30957, CL 30958 -->
ChaCha20-Poly1305는 <!-- CL 32871 -->
AES-GCM에 대한 하드웨어 지원이 있는 경우에만 우선적으로 사용됩니다.

<!-- CL 27315, CL 35290 -->
AES-128-CBC 암호화 세트와 SHA-256도 이제 지원되지만, 기본적으로 비활성화되어 있습니다.

#### [crypto/x509](/pkg/crypto/x509/)

<!-- CL 24743 -->
PSS 서명 지원이 이제 가능합니다.

<!-- CL 32644 -->
[`UnknownAuthorityError`](/pkg/crypto/x509/#UnknownAuthorityError)
이제 `Cert` 필드를 추가하여, 신뢰할 수 없는 인증서를 보고합니다.

인증 유효성 검사는 몇 가지 경우에는 더 관대하고, 다른 몇 가지 경우에는 더 엄격합니다.
<!--
crypto/x509: 리프 인증서를 직접 루트로 지정할 수 있도록 허용 (CL 27393)
crypto/x509: 발급자 이름이 발급자의 서브젝트 이름과 일치하는지 확인 (CL 23571)
crypto/x509: 이미 체인에 존재하는 루트는 허용하지 않음 (CL 32121)
crypto/x509: 이름 제약 조건 처리 수정 (CL 30155)
crypto/x509: RDN 내의 모든 이름을 파싱 (CL 30810)
crypto/x509: RSA+SHA1에 대한 ISO OID 인식 (CL 27394)
crypto/x509: RSA 공개 키에 NULL 파라미터 필요 (CL 16166, CL 27312)
crypto/x509: SerialNumber 누락 시 오류 반환 (CL 27238)
-->

<!-- CL 30375 -->
이제 루트 인증서도 `/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem`에서 검색됩니다. 이는 RHEL 및 CentOS를 지원하기 위한 것입니다.

```
#### [database/sql](/pkg/database/sql/)
```

이 패키지는 이제 `context.Context`를 지원합니다. `Context`로 끝나는 새로운 메서드가 추가되었으며, 예를 들어
[`DB.QueryContext`](/pkg/database/sql/#DB.QueryContext) 및
[`DB.PrepareContext`](/pkg/database/sql/#DB.PrepareContext)가 컨텍스트 인수를 사용합니다. 새로운 `Context` 메서드를 사용하면,
요청이 완료될 때 연결이 닫히고 연결 풀로 반환되도록 합니다.
또한, 드라이버가 지원하는 경우 중단 기능을 활성화하고, 데이터베이스 풀이 다음 사용 가능한 연결을 기다리는 것을 취소할 수 있도록 합니다.

[`IsolationLevel`](/pkg/database/sql#IsolationLevel)는 이제 트랜잭션을 시작할 때, `TxOptions.Isolation`에 격리 수준을 설정하고 `DB.BeginTx`에 전달하여 설정할 수 있습니다.
드라이버가 지원하지 않는 격리 수준이 선택되면 오류가 반환됩니다. 트랜잭션에 읽기 전용 속성을 설정하려면 `TxOptions.ReadOnly`를 `true`로 설정할 수 있습니다.

쿼리 이제는 지원하는 드라이버에 대해 SQL 컬럼 유형 정보를 노출합니다.
행은 [`ColumnTypes`](/pkg/database/sql#Rows.ColumnTypes)를 반환할 수 있으며, 이에는 SQL 유형 정보, 컬럼 유형 길이, Go 유형 등이 포함될 수 있습니다.

[`Rows`](/pkg/database/sql/#Rows)
이제 여러 결과 집합을 나타낼 수 있습니다. `Rows.Next`가 `false`를 반환한 후,
`Rows.NextResultSet`를 호출하여 다음 결과 집합으로 이동할 수 있습니다. 기존 `Rows`는 다음 결과 집합으로 이동한 후에도 계속 사용해야 합니다.

[`NamedArg`](/pkg/database/sql/#NamedArg)는 쿼리 인수로 사용될 수 있습니다. 새로운 함수 [`Named`](/pkg/database/sql/#Named)는 [`NamedArg`](/pkg/database/sql/#NamedArg)를 더 간결하게 생성하는 데 도움이 됩니다.

만약 드라이버가 새로운
[`Pinger`](/pkg/database/sql/driver/#Pinger)
인터페이스를 지원한다면,
[`DB.Ping`](/pkg/database/sql/#DB.Ping)
과
[`DB.PingContext`](/pkg/database/sql/#DB.PingContext)
메서드는 해당 인터페이스를 사용하여 데이터베이스 연결이 유효한지 확인합니다.

새로운 `Context` 쿼리 메서드는 모든 드라이버에서 작동하지만,
`Context`의 취소 기능은 드라이버가 이를 사용하도록 업데이트될 때만 작동합니다. 다른 기능은 [`database/sql/driver`](/pkg/database/sql/driver)에서 드라이버 지원을 필요로 합니다.
드라이버 작성자는 새로운 인터페이스를 검토해야 합니다. 기존 드라이버 사용자는 해당 드라이버가 지원하는 내용을 확인하고, 각 기능에 대한 시스템별 문서를 참조하여 확인해야 합니다.

#### [debug/pe](/pkg/debug/pe/)

<!-- CL 22720, CL 27212, CL 22181, CL 22332, CL 22336, Issue 15345 -->
패키지가 확장되었으며, 이제 [Go 링커](/cmd/link/)에서 `gcc`-로 생성된 오브젝트 파일을 읽는 데 사용됩니다.
새로운
[`File.StringTable`](/pkg/debug/pe/#File.StringTable)
과
[`Section.Relocs`](/pkg/debug/pe/#Section.Relocs)
필드는 COFF 문자열 테이블과 COFF 이동 정보를 액세스할 수 있도록 합니다.
새로운
[`File.COFFSymbols`](/pkg/debug/pe/#File.COFFSymbols)
는 COFF 심볼 테이블에 대한 저수준 액세스를 제공합니다.

```
#### [encoding/base64](pkg/encoding/base64/)
```

<!-- CL 24964 -->
새로운
[`Encoding.Strict`](/pkg/encoding/base64/#Encoding.Strict)
메서드는 디코더가 후행 패딩 비트가 0이 아닐 때 오류를 반환하도록 하는 `Encoding` 객체를 반환합니다.

#### [encoding/binary](/pkg/encoding/binary/)

<!-- CL 28514 -->
[`Read`](/pkg/encoding/binary/#Read)
및
[`Write`](/pkg/encoding/binary/#Write)
기능이 이제 부울 값을 지원합니다.

#### [encoding/json](/pkg/encoding/json/)

<!-- CL 18692  -->
[`UnmarshalTypeError`](/pkg/encoding/json/#UnmarshalTypeError)
이제 구조체 및 필드 이름을 포함합니다.

<!-- CL 31932 -->
비어 있는 [`Marshaler`](/pkg/encoding/json/#Marshaler)
이제 JSON `null` 값으로 마샬링됩니다.

<!-- CL 21811 -->
`RawMessage` 값은 이제 포인터 유형과 동일하게 직렬화됩니다.

<!-- CL 30371 -->
[`Marshal`](/pkg/encoding/json#Marshal)
ES6에서 사용되는 동일한 형식으로 부동 소수점 숫자를 인코딩하며, 더 넓은 범위의 값에 대해 소수 (지수 표기법이 아닌) 표기법을 선호합니다.
특히, 2<sup>64</sup> 형식의 모든 부동 소수점 정수는 해당 `int64` 표현과 동일한 형식으로 변환됩니다.

<!-- CL 30944 -->
이전 Go 버전에서는 JSON의 `null`을 `Unmarshaler`로 파싱하는 것은 무효 연산으로 간주되었습니다; 이제 `Unmarshaler`의 `UnmarshalJSON` 메서드는 JSON 리터럴 `null`과 함께 호출될 수 있으며, 이 경우의 의미를 정의할 수 있습니다.

#### [encoding/pem](/pkg/encoding/pem/)

<!-- CL 27391 -->
[`Decode`](/pkg/encoding/pem/#Decode)
이제 종료 라인의 형식을 엄격하게 검사합니다.

#### [encoding/xml](/pkg/encoding/xml/)

<!-- CL 30946 -->
[`Unmarshal`](/pkg/encoding/xml/#Unmarshal)
이제 새로운 `",any,attr"` 구조체 태그를 사용하여 모든 속성을 수집하기 위한 와일드카드 지원을 제공합니다.

#### [expvar](/pkg/expvar/)

<!-- CL 30917 -->
새로운 메서드
[`Int.Value`](/pkg/expvar/#Int.Value),
[`String.Value`](/pkg/expvar/#String.Value),
[`Float.Value`](/pkg/expvar/#Float.Value), 및
[`Func.Value`](/pkg/expvar/#Func.Value)
은 내보낸 변수의 현재 값을 보고합니다.

<!-- CL 24722 -->
새로운
함수 [`Handler`](/pkg/expvar/#Handler)는 패키지의 HTTP 핸들러를 반환하여, 이를 표준 위치가 아닌 곳에 설치할 수 있도록 합니다.

#### [fmt](pkg/fmt/)

```
[`Scanf`](/pkg/fmt/#Scanf),
[`Fscanf`](/pkg/fmt/#Fscanf), 및
[`Sscanf`](/pkg/fmt/#Sscanf)는
이전 버전보다 공간을 처리하는 방식이 더 일관성 있게 변경되었습니다.
자세한 내용은 [스캔 관련 문서](/pkg/fmt/#hdr-Scanning)를 참조하십시오.
```

#### [go/doc](pkg/go/doc/)

<!-- CL 29870 -->
새로운 [`IsPredeclared`](/pkg/go/doc/#IsPredeclared)
함수는 문자열이 선언된 식별자인지 여부를 보고합니다.

```
#### [go/types](/pkg/go/types/)
```

<!-- CL 30715 -->
새로운 함수
[`Default`](/pkg/go/types/#Default)
는 "비정형" 유형에 대해 기본 "정형" 유형을 반환합니다.

<!-- CL 31939 -->
`complex64` 형식의 정렬이 이제
[Go 컴파일러](/cmd/compile/)와 일치합니다.

#### [html/template](/pkg/html/template/)

<!-- CL 14336 -->
이 패키지는 이제 `<script>` 태그의 `"type"` 속성을 검증합니다.

#### [이미지/png](/pkg/image/png/)

<!-- CL 32143, CL 32140 -->
[`Decode`](/pkg/image/png/#Decode)
(및 `DecodeConfig`)
이제 True Color 및 그레이스케일 투명도를 지원합니다.

<!-- CL 29872 -->
[`Encoder`](/pkg/image/png/#Encoder)
이제 팔렛화된 이미지를 인코딩할 때 더 빠르고, 더 작은 출력을 생성합니다.

#### [math/big](/pkg/math/big/)

<!-- CL 30706 -->
새로운 방법인
[`Int.Sqrt`](/pkg/math/big/#Int.Sqrt)
은 ⌊√x⌋를 계산합니다.

새로운 방법
[`Float.Scan`](/pkg/math/big/#Float.Scan)
은
[`fmt.Scanner`](/pkg/fmt/#Scanner)
용 지원 루틴입니다.

[`Int.ModInverse`](/pkg/math/big/#Int.ModInverse)
이제 음수도 지원합니다.

#### [math/rand](pkg/math/rand/)

<!-- CL 27253, CL 33456 -->
새로운 `[Rand.Uint64](pkg/math/rand/#Rand.Uint64)`
메서드는 `uint64` 값을 반환합니다.
새로운 `[Source64](pkg/math/rand/#Source64)`
인터페이스는 이러한 값을 직접 생성할 수 있는 소스를 설명합니다. 그렇지 않은 경우 `Rand.Uint64` 메서드는 `[Source](pkg/math/rand/#Source)`의
`Int63` 메서드에 두 번 호출하여 `uint64`를 생성합니다.

#### [mime](/pkg/mime/)

<!-- CL 32175 -->
[`ParseMediaType`](/pkg/mime/#ParseMediaType)
이제 불필요한 백슬래시 이스케이프를 리터럴로 유지하여, MSIE를 지원합니다.
MSIE가 전체 파일 경로("인트라넷 모드"에서)를 보낼 때, 백슬래시를 이스케이프하지 않습니다: "`C:\dev\go\foo.txt`", 아닌
"`C:\\dev\\go\\foo.txt`".
불필요한 백슬래시 이스케이프가 보이면, 이제 이를 MSIE에서 온 것으로 보고 리터럴 백슬래시로 취급합니다.
알려진 MIME 생성기는 숫자나 문자와 같은 간단한 토큰 문자에서 불필요한 백슬래시 이스케이프를 생성하지 않습니다.

#### [mime/quotedprintable](/pkg/mime/quotedprintable/)

`Reader`의 파싱이 다음과 같은 두 가지 방법으로 완화되어 더 많은 입력을 허용합니다. (<!-- CL 32174 -->
첫째, 두 개의 16진수가 아닌 `=` 기호가 아닌 `=` 기호를 리터럴로 처리합니다. (<!-- CL 27530 -->
둘째, 인코딩된 입력의 끝에 있는 `=` 기호를 무시합니다.

#### [net](/pkg/net/)

<!-- CL 30164, CL 33473 -->
[`Conn`](/pkg/net/#Conn)에 대한 설명서가 업데이트되어 인터페이스 구현에 대한 기대 사항을 명확히 했습니다. `net/http` 패키지의 업데이트는 설명서를 따르는 구현에 의존합니다.

_업데이트:_ `Conn` 인터페이스의 구현은 문서화된 의미를 검증해야 합니다.
[golang.org/x/net/nettest](https://godoc.org/golang.org/x/net/nettest)
패키지는 `Conn` 객체를 사용하여 테스트하고, 제대로 작동하는지 검증합니다.

<!-- CL 32099 -->
새로운 방법인
[`UnixListener.SetUnlinkOnClose`](/pkg/net/#UnixListener.SetUnlinkOnClose)
은 리스너가 닫힐 때, 해당 소켓 파일이 파일 시스템에서 제거되는지 여부를 설정합니다.

<!-- CL 29951 -->
새로운 [`Buffers`](/pkg/net/#Buffers) 유형은 메모리의 여러 비연속 버퍼에서 네트워크에 더 효율적으로 쓰는 것을 허용합니다. 특정 머신 및 특정 유형의 연결에서, 이는 OS별 배치 쓰기 작업(예: `writev`)으로 최적화됩니다.

<!-- CL 29440 -->
새로운 [`Resolver`](/pkg/net/#Resolver)는 이름과 번호를 찾고, [`context.Context`](/pkg/context/#Context)를 지원합니다.
[`Dialer`](/pkg/net/#Dialer)는 이제 선택적인
[`Resolver` 필드](/pkg/net/#Dialer.Resolver)를 갖습니다.

<!-- CL 29892 -->
[`Interfaces`](/pkg/net/#Interfaces)가 Solaris에서 이제 지원됩니다.

<!-- CL 29233, CL 24901 -->
Go DNS 해결자는 이제 `resolv.conf`의 "`rotate`" 및 "`option ndots:0`" 옵션을 지원합니다. "`ndots`" 옵션은 이제 `libresolve`와 동일한 방식으로 적용됩니다.

#### [net/http](pkg/net/http/)

서버 변경 사항:

- 서버는 이제 점진적 종료를 지원하며, [위에 언급된](#http_shutdown) 내용에 따라 동작합니다.
  - <!-- CL 32024 -->
    `Server` ( /pkg/net/http/#Server)
    는 `ReadHeaderTimeout` 및 `IdleTimeout`과 같은 구성 옵션을 추가하고 `WriteTimeout`에 대한 문서를 제공합니다.
  - <!-- CL 32014 -->
    `FileServer` ( /pkg/net/http/#FileServer) 및
    `ServeContent` ( /pkg/net/http/#ServeContent)는 이전의 `If-None-Match` 지원 외에도, RFC 7232, 2.3절에 따라 적절하게 형식화된 ETags를 사용하는 HTTP `If-Match` 조건부 요청을 지원합니다.

서버의 `Handler`가 할 수 있는 기능에 몇 가지 추가 사항이 있습니다:

- <!-- CL 31173 -->
    [`Context`](/pkg/context/#Context)
    가 [`Request.Context`](/pkg/net/http/#Request.Context)
    에 의해 반환되며,
    그 `net.Conn`가 닫히면 취소됩니다. 예를 들어, 사용자가 느린 요청 중에 브라우저를 닫으면, `Handler`는 이제 사용자가 떠났음을 감지할 수 있습니다. 이는 기존의 [`CloseNotifier`](/pkg/net/http/#CloseNotifier) 지원을 보완합니다. 이 기능은 기본 `net.Conn`](/pkg/net/#Conn)가 [최근에 명확화된 인터페이스 설명서](#net)를 구현해야 합니다.
  - <!-- CL 32479 -->
    헤더가 이미 작성된 후 생성된 트레일을 제공하려면,
    새로운
    [`TrailerPrefix`](/pkg/net/http/#TrailerPrefix)
    메시언을 참조하십시오.
  - <!-- CL 33099 -->
    `Handler`는 이제 `ErrAbortHandler`](/pkg/net/http/#ErrAbortHandler) 오류를 사용하여 응답을 중단할 수 있습니다.
  - <!-- CL 30812 -->
    `ResponseWriter`](/pkg/net/http/#ResponseWriter)에 0바이트의 `Write` 작업은 이제 `ResponseWriter`가 가로채졌는지 테스트하는 방법으로 정의됩니다:
    그렇다면, `Write`는 오류를 서버의 오류 로그에 출력하지 않고 `ErrHijacked`](/pkg/net/http/#ErrHijacked)를 반환합니다.

**클라이언트 및 전송 변경 사항:**

- <!-- CL 28930, CL 31435 -->
    `[Client](/pkg/net/http/#Client)`
    이제 리디렉션 시 대부분의 요청 헤더를 복사합니다. 자세한 내용은
    [문서](/pkg/net/http/#Client)에서 `Client` 유형에 대해 참조하십시오.
  - <!-- CL 29072 -->
    `[Transport](/pkg/net/http/#Transport)`
    이제 국제 도메인 이름을 지원합니다. 따라서 `Get` 및 기타 헬퍼도 지원합니다.
  - <!-- CL 31733, CL 29852 -->
    `Client`은 이제 301, 307, 308 리디렉션을 지원합니다. 예를 들어, `Client.Post`는 이제 301 리디렉션을 따르며, 302 및 303 리디렉션 응답에서 했던 것처럼, 본체 없이 `GET` 요청으로 변환합니다.
    `Client`은 이제 307 및 308 리디렉션을 따르며, 원본 요청 메서드와 본체를 유지합니다(존재하는 경우). 리디렉션이 요청 본체를 다시 전송해야 하는 경우, 요청에 새 `[Request.GetBody](/pkg/net/http/#Request)` 필드를 정의해야 합니다.
    `NewRequest`는 일반적인 본체 유형에 대해 `Request.GetBody`를 자동으로 설정합니다.
  - <!-- CL 32482 -->
    `Transport`는 포트에 비숫자 문자가 포함된 URL에 대한 요청을 이제 거부합니다.
  - <!-- CL 27117 -->
    `Transport`는 네트워크 오류가 발생한 후 바이트가 쓰여지지 않았고 요청에 본체가 없는 경우, 비멱등 요청을 재시도합니다.
  - <!-- CL 32481 -->
    새로운 `[Transport.ProxyConnectHeader](/pkg/net/http/#Transport)`는 `CONNECT` 요청 중에 프록시에 전송할 헤더 값을 구성할 수 있습니다.
  - <!-- CL 28077 -->
    `DefaultTransport.Dialer`가 이제 `DualStack` ("[Happy Eyeballs](https://tools.ietf.org/html/rfc6555)") 지원을 활성화하여, IPv6이 실패할 가능성이 있는 경우 IPv4를 백업으로 사용할 수 있도록 합니다.
  - <!-- CL 31726 -->
    `Transport`는 이제 `Request.Body`가 비어 있지 않은 경우 `Request.ContentLength`가 0인지 확인하기 위해 `Request.Body`의 첫 번째 바이트를 더 이상 읽지 않습니다. `ContentLength`가 실제로 0인지 아니면 정의되지 않은지 확인하기 위해 사용됩니다.
    본체의 길이가 0임을 명시적으로 나타내려면, `nil`로 설정하거나 새로운 값인 `NoBody`로 설정합니다. `NoBody` 값은 `Request` 생성 함수에서 사용하도록 설계되었으며, `NewRequest`에서 사용됩니다.

#### [net/http/httptrace](/pkg/net/http/httptrace/)

<!-- CL 30359 -->
이제 클라이언트 요청의 TLS 핸드셰이프를 추적하는 기능이 추가되었습니다.
새로운
[`ClientTrace.TLSHandshakeStart`](/pkg/net/http/httptrace/#ClientTrace.TLSHandshakeStart)
및
[`ClientTrace.TLSHandshakeDone`](/pkg/net/http/httptrace/#ClientTrace.TLSHandshakeDone)
기능을 사용합니다.

#### [net/http/httputil](/pkg/net/http/httputil/)

<!-- CL 32356 -->
[`ReverseProxy`](/pkg/net/http/httputil/#ReverseProxy)
에는 새로운 선택적 훅,
[`ModifyResponse`](/pkg/net/http/httputil/#ReverseProxy.ModifyResponse),
가 추가되어, 클라이언트로 프록시하기 전에 백엔드에서 응답을 수정할 수 있습니다.

#### [net/mail] (/pkg/net/mail/)

<!-- CL 32176 -->
빈 괄호로 묶인 문자열이 주소의 이름 부분에 다시 허용됩니다. 즉, Go 1.4 및 이전 버전에서는
`"" <gopher@example.com>`을 허용했지만, Go 1.5에서는 이 주소를 거부하는 버그가 발생했습니다.
이제 이 주소가 다시 인식됩니다.

<!-- CL 31581 -->
`[Header.Date](pkg/net/mail/#Header.Date)`
메서드는 항상 `Date:` 헤더를 파싱하는 방법을 제공했습니다.
새로운 함수
`[ParseDate](pkg/net/mail/#ParseDate)`
는 `Resent-Date:`와 같은 다른 헤더 라인에 있는 날짜를 파싱할 수 있도록 합니다.

```
#### [net/smtp](pkg/net/smtp/)
```

<!-- CL 33143 -->
`Auth.Start`
메서드의 구현이 빈 `toServer` 값을 반환하는 경우,
패키지는 더 이상 SMTP `AUTH` 명령의 후행 공백을 보내지 않으므로,
일부 서버가 이를 거부합니다.

#### [net/url](pkg/net/url/)

<!-- CL 31322 -->
새로운 함수
[`PathEscape`](/pkg/net/url/#PathEscape)
및
[`PathUnescape`](/pkg/net/url/#PathUnescape)
은 쿼리 인코딩 및 디코딩 함수와 유사하지만, 경로 요소에 사용됩니다.

<!-- CL 28933 -->
새로운 메서드
[`URL.Hostname`](/pkg/net/url/#URL.Hostname)
과
[`URL.Port`](/pkg/net/url/#URL.Port)
은 URL의 호스트 이름과 포트 필드를 반환하며, 포트가 존재하지 않을 경우를 올바르게 처리합니다.

<!-- CL 28343 -->
기존의 방법인
[`URL.ResolveReference`](/pkg/net/url/#URL.ResolveReference)
이제 이스케이프된 바이트를 포함하는 경로를 제대로 처리하고, 이스케이프 정보를 잃어버리지 않습니다.

<!-- CL 31467 -->
`URL` 타입이 이제 `encoding.BinaryMarshaler` 및 `encoding.BinaryUnmarshaler` 인터페이스를 구현하며, 이를 통해 [gob 데이터](/pkg/encoding/gob/)를 사용하여 URL을 처리할 수 있습니다.

<!-- CL 29610, CL 31582 -->
RFC 3986에 따라,
[`Parse`](/pkg/net/url/#Parse)
이제 `this_that:other/thing`과 같은 URL을 거부하고,
`this_that`이 유효한 스킴이 아니므로,
상대 경로로 해석하는 대신 거부합니다.
상대 경로로 해석하도록 강제하려면,
이러한 URL은 "`./`"으로 시작해야 합니다.
`URL.String` 메서드는 필요한 경우 이 접두사를 삽입합니다.

#### [os](/pkg/os/)

<!-- CL 16551 -->
새로운 함수
[`Executable`](/pkg/os/#Executable)는
실행 중인 실행 파일의 경로 이름을 반환합니다.

<!-- CL 30614 -->
`os.File` 객체에 메서드를 호출하려는 시도가 이제 `os.ErrClosed` 새 오류 값을 반환합니다.
이전에는 `syscall.EBADF`와 같은 시스템별 오류를 반환했습니다.

<!-- CL 31358 -->
유닉스 시스템에서, [`os.Rename`](/pkg/os/#Rename)
함수는 이제 기존 빈 디렉토리를 다른 디렉토리로 이름을 변경하려고 사용할 때 오류를 반환합니다.
이전에 비어 있지 않은 디렉토리로 이름을 변경할 때는 실패했지만, 빈 디렉토리로 이름을 변경할 때는 성공했습니다.
이로써 유닉스 시스템의 동작이 다른 시스템의 동작과 일치하게 됩니다.

<!-- CL 32451 -->
Windows에서, 긴 절대 경로는 이제 자동으로 확장된 길이의 경로(예: "`\\?\`"으로 시작하는 경로)로 변환됩니다.
이를 통해 패키지가 260자보다 긴 파일 경로를 사용하는 파일과 함께 작동할 수 있습니다.

<!-- CL 29753 -->
Windows에서, [`os.IsExist`](/pkg/os/#IsExist)는 이제 시스템 오류 `ERROR_DIR_NOT_EMPTY`에 대해 `true`를 반환합니다.
이는 기존의 Unix 오류 `ENOTEMPTY` 처리에 해당합니다.

<!-- CL 32152 -->
Plan 9에서 `#M`에 의해 제공되지 않는 파일은 이제
`FileInfo.Mode`의 값을 반환하는
`ModeDevice`가 설정됩니다.

#### [path/filepath](/pkg/path/filepath/)

Windows에서 발견된 여러 버그와 예외 상황이 수정되었습니다:
[`Abs`](/pkg/path/filepath/#Abs)가 이제 문서화된 대로 `Clean`을 호출합니다.
[`Glob`](/pkg/path/filepath/#Glob)가 이제
“`\\?\c:\*`”와 일치합니다.
[`EvalSymlinks`](/pkg/path/filepath/#EvalSymlinks)가 이제
“`C:.`”를 올바르게 처리하며,
[`Clean`](/pkg/path/filepath/#Clean)가 이제 경로의
시작 부분에 있는 “`..`”를 올바르게 처리합니다.

#### [reflect](/pkg/reflect/)

<!-- CL 30088 -->
새로운 함수
[`Swapper`](/pkg/reflect/#Swapper)가
`sort.Slice`를 지원하기 위해 추가되었습니다.

```
#### [strconv](/pkg/strconv/)
```

<!-- CL 31210 -->
[`Unquote`](/pkg/strconv/#Unquote)
함수는 이제 백쿼트된 원시 문자열에서 캐리지 리턴(`\r`)을 제거합니다. 이는 [Go 언어의 의미론](/ref/spec#String_literals)을 따릅니다.

#### [syscall](/pkg/syscall/)

<!-- CL 25050, CL 25022 -->
[`Getpagesize`](/pkg/syscall/#Getpagesize)
이제 시스템의 크기를 반환하며, 더 이상 상수 값을 반환하지 않습니다.
이전에는 항상 4KB를 반환했습니다.

<!-- CL 31446 -->
`[Utimes`](/pkg/syscall/#Utimes)의 시그니처가 Solaris에서 다른 Unix 시스템의 시그니처와 일치하도록 변경되었습니다. 이식 가능한 코드는 계속해서 `[os.Chtimes]( /pkg/os/#Chtimes)`를 사용해야 합니다.

<!-- CL 32319 -->
`X__cmsg_data` 필드가 `Cmsghdr`에서 제거되었습니다.
[Cmsghdr](pkg/syscall/#Cmsghdr)

#### [text/template](pkg/text/template/)

<!-- CL 31462 -->
[`Template.Execute`](/pkg/text/template/#Template.Execute)
이제 `reflect.Value`를 데이터
인수로 받아들일 수 있으며,
[`FuncMap`](/pkg/text/template/#FuncMap) 함수도 `reflect.Value`를 받아들이고 반환할 수 있습니다.

#### [time](/pkg/time/)

<!-- CL 20118 -->
새로운 함수
[`Until`](/pkg/time/#Until)은
동일한 기능을 수행하는 `Since` 함수를 보완합니다.

<!-- CL 29338 -->
[`ParseDuration`](/pkg/time/#ParseDuration)
이제 긴 소수 부분을 허용합니다.

<!-- CL 33429 -->
[`Parse`](/pkg/time/#Parse)
이제 월의 시작 이전 날짜, 예를 들어 6월 0일을 거부합니다;
또한 월의 끝 이후 날짜, 예를 들어 6월 31일 및 7월 32일을 이미 거부합니다.

<!-- CL 33029 -->
<!-- CL 34816 -->
`tzdata` 데이터베이스가 현재 로컬 시간대 데이터베이스가 없는 시스템용 버전 2016j으로 업데이트되었습니다.

#### [테스팅](/pkg/testing/)

<!-- CL 29970 -->
새로운 메서드
[`T.Name`](/pkg/testing/#T.Name)
(그리고 `B.Name`)는 현재 테스트 또는 벤치마크의 이름을 반환합니다.

<!-- CL 32483 -->
새로운 함수
[`CoverMode`](/pkg/testing/#CoverMode)
은 테스트 커버리지 모드를 보고합니다.

<!-- CL 32615 -->
테스트 및 성능 측정 결과가 이제 race 감지기가 활성화되어 실행 중에 데이터 경쟁이 발생하면 실패로 표시됩니다.
이전에는 개별 테스트 케이스가 통과하는 것처럼 보였고, 테스트 실행 파일 전체가 실패하는 것으로 표시되었습니다.

<!-- CL 32455 -->
`MainStart` 함수의 서명은 문서에 따라 변경되었습니다. 이는 내부적인 세부 사항이며, Go 1과의 호환성을 보장하는 내용은 아닙니다.
`MainStart` 함수를 직접 호출하지 않고 오류가 발생한다면, 일반적으로 비어 있어야 하는 `GOROOT` 환경 변수가 설정되었고, `go` 명령의 실행 파일 버전과 일치하지 않을 가능성이 있습니다.

#### [unicode](pkg/unicode/)

<!-- CL 30935 -->
[`SimpleFold`](/pkg/unicode/#SimpleFold)
이제 제공된 입력이 유효하지 않은 문인 경우, 원래 인수를 변경하지 않고 반환합니다.
이전 구현에서는 인덱스 범위 검사 중 예외가 발생했습니다.
