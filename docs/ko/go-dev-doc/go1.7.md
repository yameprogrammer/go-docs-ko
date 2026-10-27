<!--
acme에 대해:
편집 .,s;^PKG:([a-z][A-Za-z0-9_/]+);<a href="/pkg/\1/"><code>\1</code></a>;g
편집 .,s;^([a-z][A-Za-z0-9_/]+)\.([A-Z][A-Za-z0-9_]+\.)?([A-Z][A-Za-z0-9_]+)([ .',)]|$);<a href="/pkg/\1/#\2\3"><code>\3</code></a>\4;g
편집 .,s;^FULL:([a-z][A-Za-z0-9_/]+)\.([A-Z][A-Za-z0-9_]+\.)?([A-Z][A-Za-z0-9_]+)([ .',)]|$);<a href="/pkg/\1/#\2\3"><code>\1.\2\3</code></a>\4;g
편집 .,s;^DPKG:([a-z][A-Za-z0-9_/]+);<dl id="\1"><a href="/pkg/\1/">\1</a></dl>;g
rsc 마지막 업데이트는 6729576을 통해
-->

<!--
참고: 이 문서 및 이 디렉토리에 있는 다른 문서에서, 고정폭 문자열과 고정폭이 아닌 공백을 함께 사용하는 규칙을 따릅니다 (예: `hello world`).
이러한 문자열에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.7 소개 {#introduction}

가장 최신 Go 릴리스인 버전 1.7은 1.6 이후 6개월 후에 출시되었습니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
언어 사양에 대한 하나의 미미한 변경 사항이 있습니다.
항상처럼, 이 릴리스는 Go 1의 [호환성 약속](/doc/go1compat.html)을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일 및 실행될 것으로 예상합니다.

이 릴리스는 [포트를 IBM LinuxOne에 추가합니다](#ports);
[x86-64 컴파일러 백엔드를 업데이트하여 더 효율적인 코드를 생성하도록 합니다](#compiler);
[컨텍스트 패키지](#context)를 포함하고, 이 패키지는 [x/net 서브리포지토리](https://golang.org/x/net/context)에서 가져온 것으로,
이제 표준 라이브러리에 포함됩니다;
또한 [테스팅 패키지](#testing)에서 테스트 및 벤치마크의 계층 구조를 만드는 기능을 추가합니다.
이 릴리스는 또한 Go 1.5에서 시작된 [벤더링 지원을 완료하고](#cmd_go), 이를 표준 기능으로 만듭니다.

## 언어 변경 사항 {#language}

이번 릴리스에는 아주 작은 언어 변경 사항이 있습니다.
"[종료 문장](/ref/spec#Terminating_statements)" 섹션은
문장 목록이 종료 문장으로 끝나는지 여부를 결정하기 위해,
"최종 비어 있지 않은 문장"을 끝으로 간주하도록 명확히 합니다.
이는 기존의 gc 및 gccgo 컴파일러 도구 체인과 일치합니다.
이전 릴리스에서는 정의가 "최종 문장"만 언급하여,
꼬리 부분의 빈 문장의 효과를 가장 불분명하게 만들었습니다.
[`go/types`](/pkg/go/types/)
패키지는 이 점에 있어서 gc 및 gccgo 컴파일러 도구 체인과 일치하도록 업데이트되었습니다.
이 변경 사항은 기존 프로그램의 정확성에 영향을 미치지 않습니다.

## 포트 {#ports}

```
ports
```

Go 1.7은 macOS 10.12 Sierra에 대한 지원을 추가합니다.
1.7 이전 버전으로 빌드된 바이너리는 Sierra에서 제대로 작동하지 않습니다.

Go 1.7는 [Linux on z Systems](https://en.wikipedia.org/wiki/Linux_on_z_Systems) ( `linux/s390x` ) 에 대한 실험적인 포트를 추가하고, Plan 9 on ARM (`plan9/arm`) 에 대한 포트의 시작을 제공합니다.

실험적인 Linux용 64비트 MIPS 포트 (`linux/mips64` 및 `linux/mips64le`)
Go 1.6에 추가된 cgo 및 외부 링크에 대한 완전한 지원이 제공됩니다.

실험적인 리눅스 포트는 리틀엔디언 64비트 파워PC (`linux/ppc64le`)에서 실행되도록 설계되었으며, 이제 POWER8 아키텍처 또는 이후 버전이 필요합니다.
빅엔디언 64비트 파워PC (`linux/ppc64`)는 POWER5 아키텍처 이상을 요구합니다.

OpenBSD 포트는 이제 OpenBSD 5.6 또는 그 이상의 버전을 필요로 합니다. 이 버전에서는 `_getentropy_(2)` 시스템 호출에 액세스할 수 있습니다.

### 알려진 문제 {#known_issues}

FreeBSD에는 알려진 문제 중 일부가 있지만, 그 원인을 정확히 파악하지 못했습니다.
이러한 문제로 인해 프로그램이 드물게 오류를 발생시킬 수 있습니다.
자세한 내용은 다음 이슈를 참조하세요:
[이슈 16136](/issue/16136),
[이슈 15658](/issue/15658),
[이슈 16396](/issue/16396).
이 FreeBSD 특정 문제를 해결하는 데 도움이 필요합니다.

## 도구 {#tools}

### 어셈블러 {#cmd_asm}

```
asm(source, destination, flags)
```

64비트 ARM 시스템의 경우, 벡터 레지스터 이름이 `V0`부터 `V31`까지로 수정되었습니다.
이전 버전에서는 이들을 `V32`부터 `V63`까지로 잘못 지칭했습니다.

64비트 x86 시스템용으로 다음 명령어들이 추가되었습니다:
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

### 컴파일러 도구 체인 {#compiler}

이 릴리스에는 64비트 x86 시스템용 새로운 코드 생성 백엔드가 포함되어 있으며,
이는 2015년에 제안된 [제안](https://s/go17ssa)을 기반으로 개발되었습니다.
새로운 백엔드는
[SSA](https://en.wikipedia.org/wiki/Static_single_assignment_form)를 기반으로 하여,
더 작고 효율적인 코드를 생성하며,
경계 확인 제거와 같은 최적화에 대한 더 나은 플랫폼을 제공합니다.
새로운 백엔드는
우리 벤치마크 프로그램이 필요로 하는 CPU 시간을 5-35% 감소시킵니다.

이번 릴리스에서는 새로운 백엔드를 비활성화하려면 컴파일러에 `-ssa=0`을 전달하면 됩니다.
만약 프로그램이 새로운 백엔드가 비활성화된 상태에서만 성공적으로 컴파일되거나 실행된다면,
[버그 보고서 제출](/issue/new)해주세요.

컴파일러가 패키지 아카이브에 작성하는 내보낸 메타데이터의 형식이 변경되었습니다:
구형 텍스트 형식은 보다 간결한 이진 형식으로 대체되었습니다.
이는 약간 더 작은 패키지 아카이브를 생성하고 오래된 특정 상황 버그를 수정합니다.

이 릴리스에서는 새로운 내보내기 형식을 비활성화하려면 컴파일러에 `-newexport=0`을 전달할 수 있습니다.
프로그램이 새로운 내보내기 형식 없이 성공적으로 컴파일하거나 실행되는 경우, [버그 보고서 제출](/issue/new)하십시오.

링커의 `-X` 옵션은 더 이상 비정상적인 두 개의 인자 형태를 지원하지 않습니다.
`-X` `name` `value`,
Go 1.6 릴리스에서 [공지](https://golang.org/doc/go1.6#compiler)되었고, 링커에서 출력되는 경고 메시지에 포함되어 있습니다.
대신 `-X` `name=value`를 사용하십시오.

이 릴리스에서는 컴파일러와 링커가 Go 1.6보다 훨씬 빠르고 효율적으로 실행되지만, 여전히 원하는 만큼 빠르지는 않으며 향후 릴리스에서 계속 최적화될 예정입니다.

컴파일러 도구 체인 및 표준 라이브러리의 변경으로 인해,
이 릴리스로 빌드된 바이너리는 일반적으로 Go 1.6로 빌드된 바이너리보다 작아야 하며,
때로는 20-30% 정도 더 작을 수 있습니다.

x86-64 시스템에서는 Go 프로그램이 perf (Linux) 및 VTune (Intel)와 같은 프로파일링 도구가 기대하는 대로 스택 프레임 포인터를 유지합니다. 이를 통해 이러한 도구를 사용하여 Go 프로그램을 분석하고 최적화하기가 더 쉬워집니다.

프레임 포인터 유지에는 약간의 런타임 오버헤드가 발생하며, 이는 약 2% 정도의 평균값을 가집니다. 향후 릴리스에서 이러한 비용을 줄이는 것을 목표로 합니다. 프레임 포인터를 사용하지 않는 도구 체인을 구축하려면 다음 명령을 실행할 때 `GOEXPERIMENT=noframepointer`를 설정하십시오.
`make.bash`, `make.bat`, 또는 `make.rc`.

### Cgo {#cmd_cgo}

패키지가 [cgo](/cmd/cgo/)를 사용하는 경우 이제 Fortran 소스 파일을 포함할 수 있습니다 (C, C++, Objective C, SWIG 외에도).
그러나 Go 바인딩은 여전히 C 언어 API를 사용해야 합니다.

Go 바인딩은 이제 새로운 헬퍼 함수 `C.CBytes`를 사용할 수 있습니다.
`C.CString`와 달리, Go의 `string`을 받아 C의 `char*` (C의 `*C.byte`)를 반환하는 대신,
`C.CBytes`는 Go의 `[]byte`를 받아 `unsafe.Pointer` (C의 `void*`)를 반환합니다.

이전 버전에서 `cgo`를 사용하여 빌드된 패키지와 바이너리는 임시 디렉토리 이름을 포함하여 각 빌드마다 다른 출력을 생성했습니다.

이 릴리스를 GCC 또는 Clang의 충분히 최신 버전(`-fdebug-prefix-map` 옵션을 지원하는 버전)과 함께 사용하면, 최종적으로 빌드는 결정적(deterministic)이 될 것입니다.

### Gccgo {#gccgo}

Go의 반기별 릴리즈 일정과 GCC의 연간 릴리즈 일정이 일치하기 때문에,

GCC 6에는 Go 1.6.1 버전의 gccgo가 포함되어 있습니다.
다음 릴리즈인 GCC 7에는 Go 1.8 버전의 gccgo가 포함될 가능성이 높습니다.

### Go 명령어 {#cmd_go}

[`go`](/cmd/go/) 명령어의 기본 작동 방식은 동일하지만, 몇 가지 주목할 만한 변경 사항이 있습니다.

이 릴리스에서 `GO15VENDOREXPERIMENT` 환경 변수에 대한 지원이 제거되었습니다.
이는 Go 1.6 릴리스에 [공지된 내용](/doc/go1.6#go_command)입니다.
[Vendor 지원](/s/go15vendor)은 이제 `go` 명령 및 도구 체의 표준 기능입니다.

`Package` 데이터 구조가 "go list"에 제공되면서,
`StaleReason` 필드가 특정 패키지가 왜 "낡았다"고 간주되는지 (즉, 재구축이 필요한지) 설명합니다.
이 필드는 `-f` 또는 `-json` 옵션에서 사용할 수 있으며, 대상이 재구축되는 이유를 이해하는 데 유용합니다.

다음 명령 `"go get"`가 이제 `git.openstack.org`를 참조하는 임포트 경로를 지원합니다.

이 릴리스는 실험적인, 최소한의 기능을 제공하여 바이너리 형태로만 구성된 프로그램을 빌드할 수 있도록 지원합니다.
[`binary-only packages`](/pkg/go/build#hdr-Binary_Only_Packages)는 소스 코드가 없는 바이너리 형태로 배포된 패키지를 대상으로 합니다.
이 기능은 특정 상업 환경에서 필요하지만, 나머지 도구 체인과의 완전한 통합을 목표로 하지 않습니다.
예를 들어, 완전한 소스 코드에 접근을 가정하는 도구는 이러한 패키지와 작동하지 않으며, "`go get`" 명령에서 이러한 패키지를 지원할 계획은 없습니다.

### Go 문서 {#cmd_doc}

"`go` `doc`" 명령은
이제 생성자와 그 생성하는 유형을 함께 그룹화합니다.
이는 [`godoc`](/cmd/godoc/)의 기능을 따릅니다.

### Go vet {#cmd_vet}

"`go vet`" 명령은
`-copylock` 및 `-printf` 검사에 더 정확한 분석을 제공하며,
새로운 `-tests` 검사를 도입하여, 일반적으로 사용되는 테스트 함수의 이름과 서명을 확인합니다.
새로운 `-tests` 검사와 혼동을 피하기 위해, 이전, 광고되지 않은
`-test` 옵션이 제거되었습니다. 이 옵션은 `-all` `-shadow`와 동일한 기능을 수행했습니다.

`vet` 명령에도 새로운 검사가 추가되었습니다.
`-lostcancel`는 Go 1.7의 새로운 `context` 패키지에서 `WithCancel`, `WithTimeout`, `WithDeadline` 함수에서 반환되는 취소 함수를 호출하지 못한 경우를 감지합니다 (자세한 내용은 [아래](#context) 참조).
함수를 호출하지 않으면 새로운 `Context`는 부모 컨텍스트가 취소될 때까지 재사용되지 않습니다.
(백그라운드 컨텍스트는 절대로 취소되지 않습니다.)

### Go 도구: 배포 기능 {#cmd_dist}

새로운 서브명령 "`go` `tool` `dist` `list`"는 모든 지원되는 운영체제/아키텍처 조합을 출력합니다.

### Go 툴 트레이스 {#cmd_trace}

명령 "``go tool trace``",
[Go 1.5에 소개됨](https://go.dev/doc/go1.5#trace_command),
은 다양한 방식으로 개선되었습니다.

첫째, 추적을 수집하는 것이 이전 버전보다 훨씬 효율적입니다.
이 버전에서 추적을 수집하는 데 드는 일반적인 실행 시간 오버헤드는 약 25%;
이전 버전에서는 최소 400%였습니다.
둘째, 추적 파일에는 파일 및 줄 번호 정보가 포함되어 있어, 추적 도구를 실행할 때 원래 실행 파일을 선택적으로 사용할 수 있습니다.
셋째, 추적 도구는 브라우저 기반 뷰어의 제한을 피하기 위해 큰 추적을 분할합니다.

이 릴리스에서 트레이스 파일 형식은 변경되었지만, Go 1.7 도구는 이전 버전의 트레이스도 읽을 수 있습니다.

## 성능 {#performance}

```
perf
```

물론입니다. 변경 사항이 매우 일반적이고 다양하기 때문에 정확한 성능에 대한 진술을 내리는 것은 어렵습니다.
대부분의 프로그램은 더 빠르게 실행될 것으로 예상되며, 이는 가비지 컬렉터의 속도 향상과 핵심 라이브러리의 최적화 때문입니다.
x86-64 시스템에서는 새로운 컴파일러 백엔드에 의해 생성된 코드를 통해 많은 프로그램이 훨씬 빠르게 실행될 것으로 예상됩니다.
위에 언급했듯이, 당사 자체 벤치마크에서는 코드 생성 변경만으로도 프로그램의 CPU 시간을 일반적으로 5-35% 감소시킬 수 있습니다.

<!-- git log --grep '-[0-9][0-9]\.[0-9][0-9]%' go1.6.. -->
주요 최적화를 통해 `crypto/sha1`, `crypto/sha256`, `encoding/binary`, `fmt`, `hash/adler32`, `hash/crc32`, `hash/crc64`, `image/color`, `math/big`, `strconv`, `strings`, `unicode`, 그리고 `unicode/utf16` 패키지에 상당한 개선(10% 이상)을 가져왔습니다.

가비지 컬렉션 중단 시간은 Go 1.6에 비해, 특히 대량의 비활성 고루틴, 상당한 스택 크기 변동, 또는 대규모 패키지 수준 변수를 사용하는 프로그램에서는 훨씬 짧아야 합니다.

## 표준 라이브러리 {#library}

```go
package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Println("Hello, world!")

	// 예시: 파일 읽기
	file, err := os.Open("example.txt")
	if err != nil {
		fmt.Println("오류 발생:", err)
		return
	}
	defer file.Close()

	// 파일 내용을 읽기
	data := make([]byte, 100)
	count, err := file.Read(data)
	if err != nil {
		fmt.Println("오류 발생:", err)
		return
	}
	fmt.Printf("읽은 데이터: %s\n", string(data[:count]))
}
```

### 맥락 {#context}

Go 1.7에서 `golang.org/x/net/context` 패키지를 표준 라이브러리로 이동했습니다. 이제 [`context`](/pkg/context/)를 사용하여 취소, 타임아웃, 요청 범위의 데이터를 다른 표준 라이브러리 패키지에서 사용할 수 있습니다. 여기에는 다음이 포함됩니다.
[net](#net),
[net/http](#net_http),
그리고
[os/exec](#os_exec),
아래에 언급된 바와 같이.

자세한 내용은 다음을 참조하십시오:
[패키지 설명서](/pkg/context/)
및 Go 블로그 게시물
“[Go 동시성 패턴: 컨텍스트](/blog/context).”

### HTTP 추적 {#httptrace}

Go 1.7에서는 [`net/http/httptrace`](/pkg/net/http/httptrace/)라는 패키지를 도입했습니다. 이 패키지는 HTTP 요청 내에서 이벤트 추적을 위한 메커니즘을 제공합니다.

### 테스트 {#testing}

`testing` 패키지는 이제 하위 테스트와 하위 벤치마크를 정의하는 기능을 지원합니다.
이 기능은 테이블 기반 벤치마크를 쉽게 작성하고 계층적 테스트를 생성하는 데 도움이 됩니다.
또한, 공통 설정 및 정리 코드를 공유하는 방법도 제공합니다.
자세한 내용은 [패키지 문서](/pkg/testing/#hdr-Subtests_and_Sub_benchmarks)를 참조하십시오.

### 실행 시간 {#runtime}

이제 런타임에 의해 시작된 모든 패닉은
`builtin [`error`](/ref/spec#Errors)` 및
`[`runtime.Error`](/pkg/runtime/#Error)` 인터페이스를
구현하는 패닉 값을 사용합니다.
이는 언어 사양에 따라 [필수]( /ref/spec#Run_time_panics)입니다.

패닉 발생 시, 신호의 이름이 알려진 경우, 스택 트레이스에 표시됩니다.
그렇지 않은 경우, Go1.7 이전부터 사용되던 신호 번호가 사용됩니다.

새로운 함수
[`KeepAlive`](/pkg/runtime/#KeepAlive)
은 특정 프로그램 지점에서 할당된 객체가 접근 가능하다고 명시적으로 선언하는 메커니즘을 제공합니다.
이는 일반적으로 관련된 finalizer의 실행을 지연시키는 데 사용됩니다.

새로운 함수
[`CallersFrames`](/pkg/runtime/#CallersFrames)
은 `Callers`](/pkg/runtime/#Callers)에서 얻은 PC 슬라이스를 호출 스택에 해당하는 프레임 시퀀스로 변환합니다.
이 새로운 API는 직접 `FuncForPC`](/pkg/runtime/#FuncForPC)를 사용하는 것보다 선호되어야 합니다. 왜냐하면 프레임 시퀀스는 인라인된 함수 호출을 포함하는 호출 스택을 더 정확하게 설명할 수 있기 때문입니다.

새로운 함수
[`SetCgoTraceback`](/pkg/runtime/#SetCgoTraceback)
은 동일한 프로세스 내에서 cgo를 사용하여 실행되는 Go 및 C 코드 간의 더욱 긴밀한 통합을 용이하게 합니다.

32비트 시스템에서는 런타임이 이제 운영체제가 할당한 메모리를 주소 공간의 어느 곳에서나 사용할 수 있습니다.
이로 인해 "운영체제가 할당한 메모리가 사용 불가능한 범위에 속함"과 같은 문제가 일부 환경에서 발생하는 것을 방지할 수 있습니다.

실행 시간은 이제 모든 아키텍처에서 사용되지 않은 메모리를 운영 체제로 반환할 수 있습니다.
Go 1.6 이전 버전에서는 실행 시간이 ARM64, 64비트 PowerPC 또는 MIPS에서 메모리를 반환할 수 없었습니다.

Windows에서 Go 프로그램 (Go 1.5 및 이전 버전)은 `timeBeginPeriod(1)`를 호출하여
글로벌 Windows 타이머 해상도를 시작 시 1ms로 강제했습니다.
글로벌 타이머 해상도 변경은 일부 시스템에서 문제를 일으켰고,
테스트 결과 해당 호출이 좋은 스케줄러 성능을 위해 필요하지 않다는 것이 밝혀졌으므로,
Go 1.6에서는 해당 호출을 제거했습니다.
Go 1.7에서는 해당 호출을 다시 도입했습니다: 일부 워크로드에서는 여전히
좋은 스케줄러 성능을 위해 해당 호출이 필요합니다.

### 라이브러리의 미세 조정 {#미세_조정}

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, world!")
}
```

물론, 라이브러리에는 항상 다양한 소규모 변경 사항과 업데이트가 있으며, 이는 Go 1의 [호환성] 약속을 염두에 두고 이루어졌습니다. ([/doc/go1compat](/)

```
#### [bufio](/pkg/bufio/)
```

이전 Go 버전의 `Reader`의 `Peek` 메서드가, 내부 버퍼에 들어갈 수 있는 것보다 더 많은 바이트를 요청하면, 빈 슬라이스와 오류 `ErrBufferFull`을 반환했습니다.

이제는 전체 내부 버퍼를 반환하며, 여전히 `ErrBufferFull` 오류를 반환합니다.

#### [bytes](/pkg/bytes/)

새로운 함수
[`ContainsAny`](/pkg/bytes/#ContainsAny) 및
[`ContainsRune`](/pkg/bytes/#ContainsRune)
가 [`strings`](/pkg/strings/) 패키지와 일관성을 유지하기 위해 추가되었습니다.

이전 Go 릴리스에서는 `Reader`의 `Read` 메서드가 빈 데이터를 읽을 수 없는 경우, 0바이트를 반환하고 오류를 발생시키지 않았습니다.
이제는 0바이트를 반환하고 오류 `io.EOF`를 반환합니다.

[`Reader`](/pkg/bytes/#Reader) 타입에 새로운 메서드
[`Reset`](/pkg/bytes/#Reader.Reset)이 추가되어 `Reader`를 재사용할 수 있습니다.

#### [compress/flate](/pkg/compress/flate/)

패키지 전반에 걸쳐 다양한 성능 최적화가 적용되어 있습니다.
압축 속도는 약 10% 향상되었으며, `DefaultCompression`의 압축 속도는 2배로 빨라졌습니다.

이러한 일반적인 개선 사항 외에도,
`BestSpeed`
압축기가 완전히 대체되었으며, [Snappy](https://github.com/google/snappy)와 유사한 알고리즘을 사용하므로, 약 2.5X의 속도 향상을 얻을 수 있습니다.
그러나 이전 알고리즘에 비해 출력 크기가 5-10% 더 클 수 있습니다.

또한 새로운 압축 레벨이 있습니다.
`HuffmanOnly`
이 레벨은 허프만 압축만 적용하고, 램펠-지브 인코딩은 적용하지 않습니다.
`램펠-지브 인코딩을 포기하는 것`([https://blog.klauspost.com/constant-time-gzipzip-compression/](https://blog.klauspost.com/constant-time-gzipzip-compression/))은
`HuffmanOnly`가 새로운 `BestSpeed`보다 약 3배 빠르지만, `BestSpeed`가 생성하는 것보다 20-40% 더 큰 압축된 출력을 생성한다는 의미입니다.

다음 사항에 유의하십시오:

`BestSpeed` 및 `HuffmanOnly`는 모두 [RFC 1951](https://tools.ietf.org/html/rfc1951)을 준수하는 압축된 출력을 생성합니다.
즉, 모든 유효한 DEFLATE 디컴프레서는 이러한 출력을 계속 디컴프레할 수 있습니다.

마지막으로, 압축 해제기의 `io.Reader` 구현에 약간의 변경 사항이 있습니다. 이전 버전에서는 압축 해제기가 정확히 더 이상 읽을 수 없는 경우에만 `io.EOF`를 보고했습니다.
이제 마지막 블록의 바이트를 읽을 때 `io.EOF`를 더 빨리 보고합니다.

#### [crypto/tls](pkg/crypto/tls/)

TLS 구현은 각 연결에서 처음 몇 개의 데이터 패킷을 작은 레코드 크기로 전송하며, 점차 TLS 최대 레코드 크기로 증가시킵니다.
이 전략은 첫 번째 패킷을 해독하기 전에 수신해야 하는 데이터 양을 줄여, 낮은 대역폭 네트워크에서 통신 지연 시간을 개선합니다.
`Config`의 `DynamicRecordSizingDisabled` 필드를 `true`로 설정하면, Go 1.6 이전 버전과 동일한 동작이 적용됩니다. 이때 패킷은 연결 시작부터 가능한 한 최대한의 크기로 전송됩니다.

TLS 클라이언트는 이제 서버에서 시작하는 재협상을 위한 선택적, 제한적인 지원을 제공하며, 이를 활성화하려면 `Config`의 `Renegotiation` 필드를 설정합니다.
[`Config`](/pkg/crypto/tls/#Config)
이 기능은 많은 Microsoft Azure 서버에 연결하는 데 필요합니다.

현재 패키지가 반환하는 오류는 이제 일관되게 `tls:` 접두사로 시작합니다.
이전 버전에서는 일부 오류가 `crypto/tls:` 접두사를 사용하고, 일부는 `tls:` 접두사를 사용했으며, 일부는 접두사가 전혀 없었습니다.

자체 서명 인증서를 생성할 때, 패키지는 기본적으로 "Authority Key Identifier" 필드를 설정하지 않습니다.

#### [crypto/x509](/pkg/crypto/x509/)

새로운 함수
[`SystemCertPool`](/pkg/crypto/x509/#SystemCertPool)
은, 사용 가능한 경우 전체 시스템 인증서 풀에 액세스합니다.
또한 새로운 관련 오류 유형
[`SystemRootsError`](/pkg/crypto/x509/#SystemRootsError)가 있습니다.

#### [debug/dwarf](/pkg/debug/dwarf/)

`Reader` 유형의 새로운
[`SeekPC`](/pkg/debug/dwarf/#Reader.SeekPC) 메서드와
`Data` 유형의 새로운
[`Ranges`](/pkg/debug/dwarf/#Ranges) 메서드는
`LineReader`에 전달할 컴파일 유닛을 찾고, 주어진 프로그램 카운터에 해당하는 특정 함수를 식별하는 데 도움이 됩니다.

#### [debug/elf](/pkg/debug/elf/)

새로운
[`R_390`](/pkg/debug/elf/#R_390) 리로케이션 유형
및 그 다양한 미리 정의된 상수
는 S390 포트를 지원합니다.

#### [encoding/asn1](/pkg/encoding/asn1/)

ASN.1 디코더는 이제 최소 정수 인코딩을 거부합니다.
이는 패키지가 일부 유효하지 않지만 이전에는 허용되었던 ASN.1 데이터를 거부하는 원인이 될 수 있습니다.

#### [encoding/json](/pkg/encoding/json/)

[`Encoder`](/pkg/encoding/json/#Encoder)의 새로운
[`SetIndent`](/pkg/encoding/json/#Encoder.SetIndent) 메서드는 JSON 인코딩의 들여쓰기 매개변수를 설정하며,
`Indent` 함수와 유사합니다.

`[`Encoder`](pkg/encoding/json/#Encoder)'의 새로운
[`SetEscapeHTML`](pkg/encoding/json/#Encoder.SetEscapeHTML) 메서드는
인용된 문자열에 있는 `&`, `<`, `>`
문자를 각각 `\u0026`, `\u003c`, `\u003e`로 이스케이프할지 여부를 제어합니다.
이전 버전과 마찬가지로, 인코더는 기본적으로 이 이스케이핑을 적용하여 HTML에 JSON을 포함할 때 발생할 수 있는 특정 문제를 방지합니다.

이전 Go 버전에서는 이 패키지가 문자열 타입의 키를 사용하여 맵의 인코딩 및 디코딩만 지원했습니다.
Go 1.7 버전에서는 정수 타입의 키를 사용하여 맵을 지원합니다:
인코딩은 JSON 키로 따옴표로 묶인 십진수 표현을 사용합니다.
Go 1.7 버전에서는 `MarshalText`
(참조: [`encoding.TextMarshaler`](/pkg/encoding/#TextMarshaler))
메서드를 구현하는 비문자열 키를 사용하여 맵을 인코딩하는 기능과, `UnmarshalText`
(참조: [`encoding.TextUnmarshaler`](/pkg/encoding/#TextUnmarshaler))
메서드를 구현하는 비문자열 키를 사용하여 맵을 디코딩하는 기능을 추가했습니다.
이러한 메서드는 이전 Go 버전에서 사용된 인코딩 및 디코딩을 유지하기 위해 문자열 타입의 키에 대해 무시됩니다.

`Marshal` 함수를 사용하여 바이트 슬라이스를 인코딩할 때,
[`Marshal`](/pkg/encoding/json/#Marshal)
함수는 이제 해당 바이트 유형의
`MarshalJSON`
또는
`MarshalText`
메서드를 사용할 수 있으면 해당 바이트 유형을 사용하여 인코딩된 요소의 배열을 생성합니다.
어떤 메서드도 사용할 수 없는 경우에만 기본 base64 인코딩된 문자열 데이터로의 기본값으로 전환됩니다.

이전 버전의 Go는 원래 base64 인코딩된 문자열 인코딩과 함께 배열 인코딩을 모두 지원했습니다 (바이트 유형이 적절하게
`UnmarshalJSON`
또는
`UnmarshalText`
메서드를 구현한다고 가정).
따라서 이러한 변경 사항은 이전 버전의 Go와도 의미적으로 뒷받침되는 방식으로 호환되어야 합니다.
이러한 변경 사항은 인코딩 유형을 변경하지만.

#### [go/build](/pkg/go/build/)

다음 명령(`go`의 새로운 기능인 바이너리 전용 패키지와 cgo 기반 패키지에서의 Fortran 코드 지원을 구현하기 위해)을 사용합니다.
[`Package`](/pkg/go/build/#Package) 타입은 다음과 같은 새로운 필드를 추가합니다: `BinaryOnly`, `CgoFFLAGS`, 그리고 `FFiles`.

#### [go/doc](pkg/go/doc/)

다음에서 설명된 `go`의 `test`와 관련된 변경 사항을 지원하기 위해,
[`Example`](/pkg/go/doc/#Example) 구조체에 `Unordered` 필드를 추가하여, 예제가 출력 줄을 어떤 순서로 생성할 수 있는지 나타냅니다.

#### [io](/pkg/io/)

이 패키지는 `SeekStart`, `SeekCurrent`, 및 `SeekEnd`의 새로운 상수를 추가하여
[`Seeker`](/pkg/io/#Seeker) 구현과 함께 사용하기 위한 것입니다.
이 상수들은 `os.SEEK_SET`, `os.SEEK_CUR`, 및 `os.SEEK_END`보다 선호되지만, 후자는 호환성을 위해 유지됩니다.

#### [math/big](/pkg/math/big/)

`Float` 타입은
[`GobEncode`](/pkg/math/big/#Float.GobEncode) 및
[`GobDecode`](/pkg/math/big/#Float.GobDecode) 메서드를 추가하여, `Float` 타입의 값들을 이제
[`encoding/gob`](/pkg/encoding/gob/)
패키지를 사용하여 인코딩하고 디코딩할 수 있습니다.

#### [math/rand](pkg/math/rand/)

[`Read`](/pkg/math/rand/#Read) 함수와
[`Rand`](/pkg/math/rand/#Rand)의
[`Read`](/pkg/math/rand/#Rand.Read) 메서드는 이제 입력 버퍼의 크기에 의존하지 않고 일관성 있는, 가짜 난수 스트림의 바이트를 생성합니다.

문서는 다음을 명확히 하고 있습니다.
`Rand`의 [`Seed`](/pkg/math/rand/#Rand.Seed)
및 [`Read`](/pkg/math/rand/#Rand.Read) 메서드는 동시에 호출하는 것이 안전하지 않지만, 전역 함수인 [`Seed`](/pkg/math/rand/#Seed)
및 [`Read`](/pkg/math/rand/#Read)는 (그리고 항상 그랬습니다) 안전합니다.

#### [mime/multipart](/pkg/mime/multipart/)

[`Writer`](/pkg/mime/multipart/#Writer)
구현은 이제 각 멀티파트 섹션의 헤더를 키별로 정렬하여 출력합니다.
이전에는 맵을 순회하면 섹션 헤더가 비정형적인 순서로 사용되었습니다.

#### [net](/pkg/net/)

[컨텍스트](#context) 소개의 일부로,
[`Dialer`](/pkg/net/#Dialer) 유형에는 새로운 메서드인
[`DialContext`](/pkg/net/#Dialer.DialContext)가 있으며,
[`Dial`](/pkg/net/#Dialer.Dial)와 유사하지만
`context.Context`를 래핑하여 래핑된 컨텍스트를 사용하여
연결을 수행합니다.

이 컨텍스트는 `Dialer`의
`Cancel` 및 `Deadline` 필드를 대체하기 위한 것이지만,
역사적 호환성을 위해 구현은 여전히 이를 존중합니다.

[`IP`](/pkg/net/#IP) 유형의
[`String`](/pkg/net/#IP.String) 메서드가 유효하지 않은 `IP` 주소에 대한 결과를 변경했습니다.
이전 버전에서는 `IP` 바이트 슬라이스의 길이가 0, 4 또는 16이 아닌 경우 `String`은 `"?"`를 반환했습니다.
Go 1.7에서는 바이트의 16진수 인코딩을 추가했습니다 (예: `"?12ab"`).

순 Go [이름 해결](/pkg/net/#hdr-Name_Resolution)
구현은 이제 `nsswitch.conf`에 명시된 대로 DNS 조회의 우선순위를 로컬 파일 (즉, `/etc/hosts`) 조회보다 우선시합니다.

#### [net/http](/pkg/net/http/)

[`ResponseWriter`](/pkg/net/http/#ResponseWriter)의
문서에는 이제 응답을 쓰기 시작하면 요청 본문의 향후 읽기를 방지할 수 있다는 점이 명확하게 설명되어 있습니다.
최대 호환성을 위해, 구현체는 응답의 일부를 쓰기 전에 요청 본문을 완전히 읽도록 권장됩니다.

[컨텍스트](#context) 소개의 일부로,
[`Request`](/pkg/net/http/#Request)는 새로운 메서드
[`Context`](/pkg/net/http/#Request.Context)를 통해 연결된 컨텍스트를 가져오고,
[`WithContext`](/pkg/net/http/#Request.WithContext)를 사용하여 수정된 컨텍스트를 가진 `Request`의 복사본을 생성할 수 있습니다.

[`Server`](/pkg/net/http/#Server) 구현에서,
[`Serve`](/pkg/net/http/#Server.Serve)는 요청 컨텍스트에
`ServerContextKey` 키를 사용하여,
저수준의 `*Server`뿐만 아니라, 요청이 수신된 로컬 주소 (즉,
[`Addr`](/pkg/net/#Addr))를 `LocalAddrContextKey` 키를 사용하여 기록합니다.
예를 들어, 요청이 수신된 주소는
`req.Context().Value(http.LocalAddrContextKey).(net.Addr)`로 접근할 수 있습니다.

서버의 `Serve` 메서드는 이제 HTTP/2를 활성화하는 경우 `Server.TLSConfig` 필드가 `nil`이거나 `TLSConfig.NextProtos`에 `"h2"`가 포함되어 있을 때만 활성화됩니다.

서버 구현은 이제
100 미만의 응답 코드를 3자리 숫자로 채웁니다.
이는 프로토콜 요구 사항에 따라,
따라서 `w.WriteHeader(5)`는 HTTP 응답 상태 `005`를 사용하며, 단순히 `5`가 아닙니다.

서버 구현은 이제 "chunked"가 명시적으로 설정된 경우에만 정확하게 하나의 "Transfer-Encoding" 헤더만 전송합니다. 이는 [RFC 7230](https://tools.ietf.org/html/rfc7230#section-3.3.1)에 따라 구현되었습니다.

서버 구현은 이제 유효하지 않은 HTTP 버전을 사용하는 요청을 거부하는 것이 더 엄격해졌습니다.
HTTP/0.x로 주장하는 잘못된 요청은 이제 거부됩니다 (HTTP/0.9는 완전히 지원되지 않음),
"PRI \* HTTP/2.0" 업그레이드 요청 외의 일반 텍스트 HTTP/2 요청도 이제 거부됩니다.
서버는 암호화된 HTTP/2 요청을 계속 처리합니다.

서버에서, 빈 응답 본체가 있는 경우, 타임아웃 핸들러가 200 상태 코드를 반환합니다. 0을 상태 코드로 보내는 대신입니다.

클라이언트에서,
[`Transport`](/pkg/net/http/#Transport) 구현은 원격 서버에 연결되는 모든 `dial` 작업에 요청 컨텍스트를 전달합니다.
사용자 정의 디얼러가 필요한 경우, 새로운 `Transport` 필드인 `DialContext`를 기존의 `Dial` 필드보다 선호합니다. 이를 통해 트랜스포트가 컨텍스트를 제공할 수 있습니다.

[`Transport`](/pkg/net/http/#Transport) 또한 `IdleConnTimeout`, `MaxIdleConns`, 및 `MaxResponseHeaderBytes`와 같은 필드를 추가하여, 비활성 또는 과도하게 통신하는 서버가 소비하는 클라이언트 자원을 제어하는 데 도움을 줍니다.

A
[`Client`](/pkg/net/http/#Client)의 구성된 `CheckRedirect` 함수는 이제
`ErrUseLastResponse`를 반환하여,
가장 최근의 리디렉션 응답을
HTTP 요청의 결과로 반환해야 함을 나타낼 수 있습니다.
이 응답은 이제 `CheckRedirect` 함수에
`req.Response`로 사용 가능합니다.

Go 1부터 HTTP 클라이언트의 기본 동작은
`Accept-Encoding` 요청 헤더를 사용하여
서버 측 압축을 요청하고,
응답 본문을 투명하게 해제하는 것입니다.
이 동작은 `Transport`의 `DisableCompression` 필드를 사용하여
조절할 수 있습니다.
Go 1.7에서는 HTTP 프록시 구현을 돕기 위해,
`Response`의 새로운 `Uncompressed` 필드는
이 투명한 해제가 이루어졌는지
알립니다.

[`DetectContentType`](/pkg/net/http#DetectContentType)
몇 가지 새로운 오디오 및 비디오 콘텐츠 유형에 대한 지원을 추가합니다.

#### [net/http/cgi](/pkg/net/http/cgi/)

[`Handler`](/pkg/net/http/cgi/#Handler)
은 새로운 필드
`Stderr`
을 추가하여 자식 프로세스의
표준 오류를 호스트 프로세스의
표준 오류로부터 리디렉션할 수 있도록 합니다.

#### [net/http/httptest](/pkg/net/http/httptest/)

새로운 함수
[`NewRequest`](/pkg/net/http/httptest/#NewRequest)
은 테스트 중에
[`http.Request`](/pkg/net/http/#Request)
을
[`http.Handler`](/pkg/net/http/#Handler)
에 전달하기에 적합한 새로운
[`http.Request`](/pkg/net/http/#Request)
을 준비합니다.

[`ResponseRecorder`](/pkg/net/http/httptest/#ResponseRecorder)의 새로운
[`Result`](/pkg/net/http/httptest/#ResponseRecorder.Result) 메서드는 기록된
[`http.Response`](/pkg/net/http/#Response)를 반환합니다.
응답의 헤더 또는 트레일러를 확인해야 하는 테스트는
`Result`를 호출하고 응답 필드를 검사하는 대신
`ResponseRecorder`의 `HeaderMap`에 직접 접근하는 대신 호출해야 합니다.

#### [net/http/httputil](/pkg/net/http/httputil/)

[`ReverseProxy`](/pkg/net/http/httputil/#ReverseProxy) 구현은 백엔드에 연결할 수 없는 경우에 "502 Bad Gateway" 오류를 반환합니다. 이전 버전에서는 "500 Internal Server Error" 오류를 반환했습니다.

`[`ClientConn`](/pkg/net/http/httputil/#ClientConn)` 및 `[`ServerConn`](/pkg/net/http/httputil/#ServerConn)`는 모두 사용 중단됨으로 문서화되었습니다.
이들은 저수준의, 오래된, 그리고 현재 Go의 HTTP 스택에서 사용되지 않는 구성 요소입니다.
더 이상 업데이트되지 않습니다.
프로그램은 대신
`[http.Client](https://pkg.go.dev/net/http#Client)`,
`[http.Transport](https://pkg.go.dev/net/http#Transport)`,
및
`[http.Server](https://pkg.go.dev/net/http#Server)`를 사용해야 합니다.

#### [net/http/pprof](/pkg/net/http/pprof/)

런타임 트레이스 HTTP 핸들러, `/debug/pprof/trace` 경로를 처리하도록 설치된 이 핸들러는 이제 `seconds` 쿼리 매개변수에 소수를 허용하며, 이를 통해 1초보다 짧은 간격의 트레이스 수집이 가능합니다. 특히, 과도하게 사용되는 서버 환경에서 유용합니다.

#### [net/mail](/pkg/net/mail/)

주소 파서는 이제 [RFC 6532](https://tools.ietf.org/html/rfc6532)에 따라 이스케이프되지 않은 UTF-8 텍스트를 주소에 포함할 수 있습니다.
하지만 결과에 어떤 정규화도 적용하지 않습니다.
오래된 메일 파서와의 호환성을 위해,
주소 인코더, 즉
[`Address`](/pkg/net/mail/#Address)의
[`String`](/pkg/net/mail/#Address.String) 메서드는 [RFC 5322](https://tools.ietf.org/html/rfc5322)에 따라 모든 UTF-8 텍스트를 이스케이프합니다.

[`ParseAddress`](/pkg/net/mail/#ParseAddress)
함수와
`AddressParser.Parse`
메서드는 더 엄격합니다.
이전에는 이메일 주소 뒤에 오는 모든 문자를 무시했지만,
이제 공백이 아닌 모든 것을 처리할 때 오류를 반환합니다.

#### [net/url](pkg/net/url/)

[`URL`](/pkg/net/url/#URL)의
새로운 `ForceQuery` 필드는 URL이 쿼리 문자열을 필수로 포함해야 하는지 여부를 기록하며, 이를 통해 쿼리 문자열이 없는 URL (예: `/search`)을 쿼리 문자열이 비어 있는 URL (예: `/search?`)과 구별합니다.

```
#### [os](/pkg/os/)
```

[`IsExist`](/pkg/os#IsExist)는 이제 `syscall.ENOTEMPTY`에 대해 `true`를 반환합니다.
이 기능은 해당 오류가 존재하는 시스템에서 작동합니다.

On Windows,
[`Remove`](/pkg/os/#Remove) 이제 가능하면 읽기 전용 파일을 제거합니다.
이를 통해 구현이 비 Windows 시스템과 동일하게 작동합니다.

#### [os/exec](/pkg/os/exec/)

다음과 같이, [컨텍스트](#context) 소개의 일부로,
새로운 생성자
[`CommandContext`](/pkg/os/exec/#CommandContext)
는
[`Command`](/pkg/os/exec/#Command)와 유사하지만, 명령 실행을 취소하는 데 사용할 수 있는 컨텍스트를 포함합니다.

#### [os/user](/pkg/os/user/)

[`Current`](/pkg/os/user#/Current)
함수는 cgo가 사용되지 않는 경우에도 구현되었습니다.

새로운
[`Group`](/pkg/os/user/#Group) 타입,
함수 `LookupGroup` 및 `LookupGroupId`와
`User` 구조체의 새로운 필드 `GroupIds`를 통해
시스템별 사용자 그룹 정보를 접근할 수 있습니다.

#### [reflect](/pkg/reflect/)

비록
[`Value`](/pkg/reflect/#Value)의
[`Field`](/pkg/reflect/#Value.Field) 메서드는 항상 지정된 필드 번호 `i`가 범위를 벗어나는 경우에 패닉을 발생하도록 문서화되어 있었지만, 대신
무심하게 0을 반환했습니다.
Go 1.7 버전에서는 이 메서드를 문서화된 대로 동작하도록 변경했습니다.

새로운
[`StructOf`](/pkg/reflect/#StructOf)
함수는 런타임에 구조체를 생성합니다.
이는 다음 타입 생성자를 포함한 타입 생성자 집합을 완성합니다.
[`ArrayOf`](/pkg/reflect/#ArrayOf),
[`ChanOf`](/pkg/reflect/#ChanOf),
[`FuncOf`](/pkg/reflect/#FuncOf),
[`MapOf`](/pkg/reflect/#MapOf),
[`PtrTo`](/pkg/reflect/#PtrTo),
및
[`SliceOf`](/pkg/reflect/#SliceOf).

[`StructTag`](/pkg/reflect/#StructTag)의
`new` 메서드
[`Lookup`](/pkg/reflect/#StructTag.Lookup)는
[`Get`](/pkg/reflect/#StructTag.Get)와 유사하지만, 주어진 키를 포함하지 않는 태그와
주어진 키에 빈 문자열을 연결하는 태그를 구별합니다.

[`Method`](/pkg/reflect/#Type.Method) 및
[`NumMethod`](/pkg/reflect/#Type.NumMethod)
메서드는
[`Type`](/pkg/reflect/#Type) 및
[`Value`](/pkg/reflect/#Value)의 메서드에서
더 이상 내보내거나 개수를 세지 않습니다.

#### [strings](/pkg/strings/)

이전 Go 버전에서는,
[`Reader`](/pkg/strings/#Reader)의
[`Read`](/pkg/strings/#Reader.Read) 메서드가
더 이상 데이터를 읽을 수 없을 때,
0 바이트를 요청하면 0을 반환하고 오류를 발생시키지 않았습니다.
이제는 0을 반환하고 오류
[`io.EOF`](/pkg/io/#EOF)를 반환합니다.

```
[`Reader`](/pkg/strings/#Reader) 유형에는 `Reset`이라는 새로운 메서드가 추가되어 `Reader`를 재사용할 수 있습니다.
```

#### [time](/pkg/time/)

[`Duration`](/pkg/time/#Duration)의
`time.Duration.String` 메서드는 이제 0 지속 시간을 `"0s"`로 보고, `"0"`가 아닌 `"0s"`로 표시합니다.
`ParseDuration`](/pkg/time/#ParseDuration)는 여전히 두 가지 형식을 모두 허용합니다.

`time.Local.String()` 메서드 호출은 이제 모든 시스템에서 `"Local"`을 반환합니다;
이전 버전에서는 Windows에서 빈 문자열을 반환했습니다.

`$GOROOT/lib/time`에 있는 시간대 데이터베이스가
IANA 2016d 버전으로 업데이트되었습니다.
이 백업 데이터베이스는 시스템 시간대 데이터베이스를 찾을 수 없을 때만 사용됩니다. 예를 들어 Windows에서 그렇습니다.
Windows 시간대 약어 목록도 업데이트되었습니다.

#### [syscall](/pkg/syscall/)

리눅스에서,
[`SysProcAttr`](/pkg/syscall/#SysProcAttr) 구조체
([`os/exec.Cmd`](/pkg/os/exec/#Cmd)의 `SysProcAttr` 필드에서 사용되는)
에 새로운 `Unshareflags` 필드가 추가되었습니다.
필드가 0이 아닌 경우,
[`ForkExec`](/pkg/syscall/#ForkExec)
(또는 `exec.Cmd`의 `Run` 메서드에서 사용되는)
에 의해 생성된 자식 프로세스는
새로운 프로그램을 실행하기 전에
`_unshare_(2)`
시스템 콜을 호출합니다.

#### [unicode](pkg/unicode/)

[`unicode`](/pkg/unicode/) 패키지와 시스템 전반에 걸쳐 제공되는 관련 지원이 8.0 버전에서 [Unicode 9.0](https://www.unicode.org/versions/Unicode9.0.0/) 버전으로 업그레이드되었습니다.
