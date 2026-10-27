## Go 1.5 소개 {#introduction}

최신 Go 릴리스인 버전 1.5는
구현상의 주요 아키텍처 변경 사항을 포함하는 중요한 릴리스입니다.
그럼에도 불구하고, 이번 릴리스가 여전히 Go 1의 [호환성 약속](/doc/go1compat.html)을 유지하고 있기 때문에, 거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

구현상의 가장 큰 발전 사항은 다음과 같습니다:

- 컴파일러와 런타임이 이제 전적으로 Go로 작성되었습니다 (약간의 어셈블러 포함).
    구현에 더 이상 C가 관여하지 않으며, 따라서 배포판 빌드에 필요했던 C 컴파일러가 더 이상 필요하지 않습니다.
  - 가비지 컬렉터가 이제 [동시성(/s/go14gc)](/s/go14gc)을 지원하며, 가능한 경우 다른 goroutine과 병렬로 실행되어 일시 중지 시간을 획기적으로 줄여줍니다.
  - 기본적으로 Go 프로그램은 사용 가능한 코어 수로 `GOMAXPROCS`가 설정된 상태로 실행됩니다. 이전 릴리스에서는 기본값이 1이었습니다.
  - Go 코어뿐만 아니라 모든 저장소에 대해 [내부 패키지(/s/go14internal)](/s/go14internal) 지원이 제공됩니다.
  - `go` 명령어가 이제 외부 종속성을 위한 "vendoring"에 대해 [실험적 지원(/s/go15vendor)](/s/go15vendor)을 제공합니다.
  - 새로운 `go tool trace` 명령어가 프로그램 실행의 세밀한 추적(tracing)을 지원합니다.
  - (`godoc`와는 별개인) 새로운 `go doc` 명령어가 명령줄 사용에 맞게 최적화되어 제공됩니다.

이러한 변경 사항과 구현 및 도구에 대한 여러 다른 변경 사항들은 아래에서 논의됩니다.

이번 릴리스에는 맵 리터럴(map literals)과 관련된 작은 언어 변경 사항이 하나 포함되어 있습니다.

마지막으로, 이번 [릴리스](/s/releasesched) 타이밍은 평소의 6개월 간격에서 벗어났습니다. 이는 이번 주요 릴리스를 준비하는 시간을 더 확보하고, 이후의 일정을 조정하여 릴리스 날짜를 보다 편리하게 맞추기 위함입니다.

## 언어 변경 사항 {#language}

### Map 리터럴 {#map_literals}

실수로 인해 슬라이스 리터럴에서 요소 타입을 생략할 수 있게 한 규칙이 맵 키에는 적용되지 않았습니다.
이 점은 Go 1.5에서 [수정되었습니다](/cl/2591).
예시를 통해 이를 명확히 설명하겠습니다.
Go 1.5부터 다음 맵 리터럴은,

```go
m := map[Point]string{
	    Point{29.935523, 52.891566}:   "Persepolis",
	    Point{-25.352594, 131.034361}: "Uluru",
	    Point{37.422455, -122.084306}: "Googleplex",
	}
```

다음과 같이 `Point` 타입을 명시적으로 나열하지 않고 작성할 수 있습니다:

```go
m := map[Point]string{
	    {29.935523, 52.891566}:   "Persepolis",
	    {-25.352594, 131.034361}: "Uluru",
	    {37.422455, -122.084306}: "Googleplex",
	}
```

## 구현 {#implementation}

### 더 이상의 C는 없다 {#c}

컴파일러와 런타임은 이제 C 없이 Go와 어셈블리어로 구현되었습니다.
트리에 남아 있는 유일한 C 소스는 테스트 또는 `cgo`와 관련된 것입니다.
1.4 및 그 이전 버전의 트리에는 C 컴파일러가 포함되어 있었습니다.
이는 런타임을 빌드하는 데 사용되었으며, 부분적으로 C 코드가 고루틴의 스택 관리와 함께 작동하도록 보장하기 위해 커스텀 컴파일러가 필요했습니다.
이제 런타임이 Go로 구현되었으므로, 이 C 컴파일러는 더 이상 필요하지 않으며 삭제되었습니다.
C를 제거하는 과정에 대한 자세한 내용은 [다른 곳](/s/go13compiler)에서 논의됩니다.

C에서의 변환은 이 작업을 위해 제작된 커스텀 도구들의 도움으로 이루어졌습니다.
가장 중요한 점은, 컴파일러가 C 코드를 Go로 자동 변환함으로써 실제로 옮겨졌다는 것입니다.
이는 사실상 다른 언어로 작성된 동일한 프로그램입니다.
컴파일러를 새로 구현한 것이 아니므로, 이 과정에서 새로운 컴파일러 버그가 유입되지 않았을 것으로 기대합니다.
이 프로세스에 대한 개요는 [이 발표](/talks/2015/gogo.slide) 슬라이드에서 확인할 수 있습니다.

### 컴파일러 및 도구 {#compiler_and_tools}

Go로의 전환과는 별개로, 하지만 그 영향으로 도구들의 이름이 변경되었습니다.
`6g`, `8g`와 같은 이전 이름들은 사라졌으며, 대신 `$GOARCH` 및 `$GOOS`에 의해 지정된 아키텍처와 운영체제에 적합한 바이너리로 Go 소스를 컴파일하는 `go` `tool` `compile`이라는 단일 바이너리가 제공됩니다.
마찬가지로, 이제는 하나의 링커(`go` `tool` `link`)와 하나의 어셈블러(`go` `tool` `asm`)가 존재합니다.
링커는 기존 C 구현체에서 자동으로 변환되었지만, 어셈블러는 아래에서 더 자세히 다룰 새로운 네이티브 Go 구현체입니다.

`6g`, `8g` 등의 이름이 삭제된 것과 마찬가지로, 컴파일러와 어셈블러의 출력 파일 확장자가 이제 `.8`, `.6` 등이 아닌 일반 `.o` 접미사로 제공됩니다.

### 가비지 컬렉터 (Garbage collector) {#gc}

가비지 컬렉터는 [설계 문서](/s/go14gc)에 설명된 개발 과정의 일환으로 1.5 버전에서 재설계되었습니다.
고급 알고리즘, 개선된 컬렉터 [스케줄링](/s/go15gcpacing), 그리고 사용자 프로그램과 더 많은 컬렉션 작업을 병렬로 실행하는 방식의 결합을 통해, 이전 릴리스의 컬렉터보다 예상 지연 시간이 훨씬 낮아졌습니다.
컬렉터의 "stop the world" 단계는 거의 항상 10밀리초 미만이며, 보통 그보다 훨씬 짧을 것입니다.

사용자 응답형 웹사이트와 같이 낮은 지연 시간이 중요한 시스템의 경우, 새로운 collector를 통해 예상 지연 시간이 감소하는 것이 중요할 수 있습니다.

새로운 컬렉터의 상세 내용은 GopherCon 2015의 [강연](/talks/2015/go-gc.pdf)에서 발표되었습니다.

### 런타임 {#runtime}

Go 1.5에서 고루틴(goroutine)이 스케줄링되는 순서가 변경되었습니다.
스케줄러의 속성은 언어 차원에서 정의된 적이 없으나,
스케줄링 순서에 의존하는 프로그램은 이번 변경으로 인해
문제가 발생할 수 있습니다.
이 변경으로 인해 영향을 받는 몇 가지 (오류가 있는) 프로그램들이 확인되었습니다.
만약 스케줄링 순서에 암시적으로 의존하는 프로그램이 있다면,
해당 프로그램을 업데이트해야 합니다.

또 다른 잠재적인 파괴적 변경 사항은 이제 런타임이 동시에 실행할 기본 스레드 수(`GOMAXPROCS`로 정의됨)를 CPU에서 사용 가능한 코어 수로 설정한다는 점입니다.
이전 릴리스에서는 기본값이 1이었습니다.
멀티 코어에서 실행되는 것을 예상하지 않은 프로그램은 의도치 않게 작동하지 않을 수 있습니다.
이러한 프로그램은 제한 사항을 제거하거나 `GOMAXPROCS`를 명시적으로 설정하여 업데이트할 수 있습니다.
이 변경 사항에 대한 더 자세한 논의는 [설계 문서](/s/go15gomaxprocs)를 참조하십시오.

### 빌드 {#build}

Go 컴파일러와 런타임이 Go로 구현되었으므로, 소스에서 배포판을 컴파일하려면 Go 컴파일러가 반드시 준비되어 있어야 합니다.
따라서 Go 코어를 빌드하려면, 이미 작동하는 Go 배포판이 설치되어 있어야 합니다.
(코어 작업을 하지 않는 Go 프로그래머는 이 변경 사항의 영향을 받지 않습니다.)
`gccgo`를 포함하여 Go 1.4 이후의 모든 배포판을 사용할 수 있습니다.
자세한 내용은 [설계 문서](/s/go15bootstrap)를 참조하십시오.

## Ports {#ports}

주로 업계가 32비트 x86 아키텍처에서 벗어남에 따라, 1.5 버전에서 제공되는 바이너리 다운로드 세트가 축소되었습니다.
OS X 운영 체제용 배포판은 `amd64` 아키텍처에 대해서만 제공되며, `386`은 제공되지 않습니다.
마찬가지로 Snow Leopard (Apple OS X 10.6)용 포트는 여전히 작동하지만, Apple에서 더 이상 해당 운영 체제 버전을 유지 관리하지 않으므로 더 이상 다운로드로 출시되거나 유지 관리되지 않습니다.
또한, DragonflyBSD 자체가 더 이상 32비트 386 아키텍처를 지원하지 않기 때문에 `dragonfly/386` 포트는 더 이상 전혀 지원되지 않습니다.

하지만 소스에서 빌드할 수 있는 몇 가지 새로운 포트들이 제공됩니다.
여기에는 `darwin/arm` 및 `darwin/arm64`가 포함됩니다.
새로운 포트인 `linux/arm64`는 대부분 준비되었으나, `cgo`는 외부 링킹(external linking)을 사용할 때만 지원됩니다.

`ppc64` 및 `ppc64le`(64비트 PowerPC, 빅 엔디안 및 리틀 엔디안) 또한 실험적 기능으로 제공됩니다.
이 두 포트 모두 `cgo`를 지원하지만, 내부 링크(internal linking)를 통해서만 가능합니다.

FreeBSD에서 Go 1.5는 새로운 `SYSCALL` 명령어를 사용하기 때문에 FreeBSD 8-STABLE 이상의 버전이 필요합니다.

NaCl에서 Go 1.5는 SDK 버전 pepper-41이 필요합니다. 이후의 pepper 버전들은 NaCl 런타임에서 sRPC 서브시스템이 제거되었기 때문에 호환되지 않습니다.

Darwin에서 `ios` 빌드 태그를 사용하여 시스템 X.509 인증서 인터페이스 사용을 비활성화할 수 있습니다.

이제 Solaris 포트에서 cgo와 [`net`](/pkg/net/), [`crypto/x509`](/pkg/crypto/x509/) 패키지를 완전히 지원하며, 그 외 다수의 수정 및 개선 사항이 적용되었습니다.

## Tools {#tools}

### 번역하기 {#translate}

트리에서 C를 제거하는 프로세스의 일환으로, 컴파일러와 링커가 C에서 Go로 번역되었습니다.
이는 진정한 (기계 보조) 번역이었으므로, 새 프로그램들은 새로운 버그가 포함된 새로운 프로그램이라기보다 기본적으로 기존 프로그램들을 번역한 것입니다.
우리는 번역 프로세스로 인해 새로운 버그가 거의 또는 전혀 도입되지 않았다고 확신하며, 실제로 이전에는 알려지지 않았던 다수의 버그를 발견하여 현재는 수정된 상태입니다.

어셈블러는 새로운 프로그램입니다. 이에 대한 설명은 아래와 같습니다.

### 이름 변경 {#rename}

컴파일러(`6g`, `8g` 등),
어셈블러(`6a`, `8a` 등),
그리고 링커(`6l`, `8l` 등)의 프로그램 세트들은
각각 `GOOS`와 `GOARCH` 환경 변수에 의해 설정되는
단일 도구로 통합되었습니다.
이전의 이름들은 사라졌으며, 새로운 도구들은 `go` `tool`
메커니즘을 통해 `go tool compile`,
`go tool asm`,
`go tool link`로 사용할 수 있습니다.
또한, 중간 오브젝트 파일에 사용되던 `.6`, `.8` 등의
파일 접미사도 사라졌으며, 이제는 단순한 `.o` 파일입니다.

예를 들어, `go build`를 통하지 않고 도구를 직접 사용하여 Darwin용 amd64 프로그램의 빌드 및 링크를 수행하려면 다음과 같이 실행합니다.

$ export GOOS=darwin GOARCH=amd64
	$ go tool compile program.go
	$ go tool link program.o

### 이동하기 {#moving}

[`go/types`](/pkg/go/types/) 패키지가 이제 메인 저장소로 이동함에 따라(아래 참조), [`vet`](/cmd/vet) 및 [`cover`](/cmd/cover) 도구 또한 이동되었습니다. 이 도구들은 더 이상 외부 `golang.org/x/tools` 저장소에서 유지 관리되지 않으며, 다만 이전 릴리스와의 호환성을 위해 (더 이상 사용되지 않는) 소스 코드가 그곳에 여전히 남아 있습니다.

### 컴파일러 {#compiler}

위에서 설명한 바와 같이, Go 1.5의 컴파일러는 기존 C 소스에서 변환된 단일 Go 프로그램으로, `6g`, `8g` 등을 대체합니다.
타겟 설정은 환경 변수 `GOOS`와 `GOARCH`에 의해 구성됩니다.

1.5 컴파일러는 대부분 이전 버전과 동일하지만, 일부 내부 세부 사항이 변경되었습니다.
한 가지 중요한 변경 사항은 상수 평가에 사용자 정의(및 테스트가 덜 된) 고정밀 산술 구현 대신 [`math/big`](/pkg/math/big/) 패키지를 사용한다는 점입니다.
이로 인해 결과에 영향이 있을 것으로 예상하지는 않습니다.

amd64 아키텍처에 한해, 컴파일러에 외부 공유 라이브러리에 정의된 Go 심볼에 대한 참조를 지원하여 동적 링크를 돕는 새로운 옵션인 `-dynlink`가 추가되었습니다.

### Assembler {#assembler}

컴파일러 및 링커와 마찬가지로, Go 1.5의 어셈블러는 기존의 어셈블러 제품군(`6a`, `8a` 등)을 대체하는 단일 프로그램이며, `GOARCH` 및 `GOOS` 환경 변수를 통해 아키텍처와 운영 체제를 설정합니다. 다른 프로그램들과 달리, 어셈블러는 Go로 작성된 완전히 새로운 프로그램입니다.

새로운 어셈블러는 이전 버전과 거의 호환되지만, 일부 어셈블러 소스 파일에 영향을 줄 수 있는 몇 가지 변경 사항이 있습니다.

이러한 변경 사항에 대한 더 자세한 정보는 업데이트된 [어셈블러 가이드](/doc/asm)를 참조하십시오. 요약은 다음과 같습니다.

우선, 상수에 사용되는 표현식 평가 방식이 약간 변경되었습니다.

이제 부호 없는 64비트 산술(unsigned 64-bit arithmetic)을 사용하며, 연산자(`+`, `-`, `<<` 등)의 우선순위는 C가 아닌 Go의 방식을 따릅니다.

이러한 변경 사항이 영향을 미치는 프로그램은 매우 적을 것으로 예상되나, 수동 검증이 필요할 수 있습니다.

아마 더 중요한 점은, ARM의 스택 포인터인 `R13`이나 하드웨어 프로그램 카운터인 `R15`와 같이 `SP` 또는 `PC`가 단순히 번호가 매겨진 레지스터의 별칭(alias)인 머신에서는, 심볼을 포함하지 않는 해당 레지스터에 대한 참조가 이제 허용되지 않는다는 것입니다.

예를 들어, `SP`와 `4(SP)`는 불법(illegal)이지만 `sym+4(SP)`는 괜찮습니다. 이러한 머신에서 하드웨어 레지스터를 참조하려면 실제 `R` 이름을 사용하십시오.

한 가지 작은 변경 사항은 일부 오래된 어셈블러들이 다음과 같은 표기법을 허용했다는 점입니다.

constant=value

이름이 지정된 상수를 정의하기 위한 것입니다.
전통적인 C 스타일의 `#define` 표기법으로 항상 가능하며, 이 표기법은 여전히 지원되기 때문에(어셈블러에 단순화된 C 전처리기 구현이 포함되어 있음), 해당 기능은 제거되었습니다.

### 링커 (Linker) {#link}

Go 1.5의 링커는 이제 `6l`, `8l` 등을 대체하는 하나의 Go 프로그램입니다.
운영 체제와 명령어 집합은 환경 변수 `GOOS` 및 `GOARCH`로 지정됩니다.

몇 가지 다른 변경 사항이 있습니다.
가장 중요한 것은 `-buildmode` 옵션의 추가로, 이를 통해 링크 스타일이 확장되었습니다. 이제 공유 라이브러리를 빌드하거나 다른 언어에서 Go 라이브러리를 호출할 수 있는 상황 등을 지원합니다.
이 중 일부는 [설계 문서](/s/execmodes)에 설명되어 있습니다.
사용 가능한 빌드 모드 목록과 그 용도를 확인하려면 다음을 실행하세요.

$ go help buildmode

또 다른 사소한 변경 사항은 링커가 더 이상 Windows 실행 파일의 헤더에 빌드 타임스탬프를 기록하지 않는다는 점입니다.
또한, 이 문제는 해결될 수 있겠으나, Windows cgo 실행 파일에서 일부 DWARF 정보가 누락되어 있습니다.

마지막으로, 다음과 같이 두 개의 인자를 받는 `-X` 플래그가 있습니다.

-X importpath.name value

이제 단일 인자로 `name=value` 쌍을 사용하는, 더 일반적인 Go 플래그 스타일도 지원합니다:

-X importpath.name=value

기존 구문이 여전히 작동하지만, 스크립트 등에서 이 플래그를 사용하는 경우 새로운 형식으로 업데이트하는 것이 권장됩니다.

### Go 명령 {#go_command}

[`go`](/cmd/go) 명령의 기본적인 동작은 변경되지 않았으나, 주목할 만한 몇 가지 변경 사항이 있습니다.

이전 릴리스에서는 패키지 내부의 특정 디렉토리를 `go` 명령어를 통해 임포트할 수 없게 만드는 개념이 도입되었습니다.
1.4 버전에서는 코어 저장소(core repository)에 몇 가지 내부 요소들을 도입하여 이를 테스트했습니다.
[설계 문서](/s/go14internal)에서 제안된 바와 같이, 이제 이 변경 사항이 모든 저장소에 적용됩니다.
상세 규칙은 설계 문서에 설명되어 있으나, 요약하자면 `internal`이라는 이름의 디렉토리 내 또는 그 하위에 있는 모든 패키지는 동일한 서브트리에 루트를 둔 패키지에서만 임포트할 수 있습니다.
`internal`이라는 이름의 디렉토리 요소를 가진 기존 패키지들은 이 변경 사항으로 인해 의도치 않게 깨질 수 있으며, 이것이 지난 릴리스에서 미리 공지된 이유입니다.

패키지를 처리하는 방식의 또 다른 변경 사항은 "vendoring" 지원의 실험적 추가입니다.
자세한 내용은 [`go` 커맨드](/cmd/go/#hdr-Vendor_Directories) 문서와 [설계 문서](/s/go15vendor)를 참조하십시오.

몇 가지 사소한 변경 사항도 있었습니다.
자세한 내용은 [문서](/cmd/go)를 읽어보시기 바랍니다.

- SWIG 지원이 업데이트되어 `.swig` 및 `.swigcxx` 파일에 SWIG 3.0.6 이상 버전이 필요합니다.
  - `install` 하위 명령어가 이제 소스 디렉토리에 `build` 하위 명령어에 의해 생성된 바이너리가 있을 경우 이를 삭제하여, 트리 내에 두 개의 바이너리가 존재하여 발생하는 문제를 방지합니다.
  - `std` (표준 라이브러리) 와일드카드 패키지 이름에서 이제 명령어(commands)가 제외됩니다. 새로운 `cmd` 와일드카드가 명령어를 포함합니다.
  - 새로운 `-asmflags` 빌드 옵션이 어셈블러에 전달할 플래그를 설정합니다. 하지만 `-ccflags` 빌드 옵션은 제거되었습니다. 이 옵션은 이제 삭제된 이전 C 컴파일러 전용이었습니다.
  - 새로운 `-buildmode` 빌드 옵션이 위에서 설명한 빌드 모드를 설정합니다.
  - 새로운 `-pkgdir` 빌드 옵션이 설치된 패키지 아카이브의 위치를 설정하여, 커스텀 빌드를 격리하는 데 도움을 줍니다.
  - 새로운 `-toolexec` 빌드 옵션을 통해 컴파일러 등을 호출하는 명령어를 다른 명령어로 대체할 수 있습니다. 이는 `go tool`에 대한 커스텀 대체제 역할을 합니다.
  - `test` 하위 명령어에 이제 각 테스트와 벤치마크를 몇 번 실행할지 지정하는 `-count` 플래그가 추가되었습니다. 이 작업은 [`testing`](/pkg/testing/) 패키지가 `-test.count` 플래그를 통해 수행합니다.
  - `generate` 하위 명령어에 몇 가지 새로운 기능이 추가되었습니다. `-run` 옵션은 실행할 지시문을 선택하기 위한 정규 표현식을 지정합니다. 이는 1.4 버전에서 제안되었으나 구현되지 않았던 기능입니다. 이제 실행 패턴은 두 개의 새로운 환경 변수에 접근할 수 있습니다: `$GOLINE`은 지시문의 소스 라인 번호를 반환하며, `$DOLLAR`는 달러 기호($)로 확장됩니다.
  - `get` 하위 명령어에 이제 `-insecure` 플래그가 추가되었습니다. 연결을 암호화하지 않는 보안되지 않은 리포지토리에서 가져오는 경우 이 플래그를 활성화해야 합니다.

### Go vet 명령 {#vet_command}

[`go tool vet`](/cmd/vet) 명령어가 이제 구조체 태그(struct tags)에 대해 더 철저한 검증을 수행합니다.

### Trace 명령 {#trace_command}

Go 프로그램의 동적 실행 트레이싱(dynamic execution tracing)을 위한 새로운 도구를 사용할 수 있습니다.
사용법은 테스트 커버리지(test coverage) 도구의 작동 방식과 유사합니다.
트레이스 생성은 `go test`에 통합되어 있으며, 이후 트레이싱 도구를 별도로 실행하여 결과를 분석합니다.

```bash
$ go test -trace=trace.out path/to/package
	$ go tool trace [flags] pkg.test trace.out
```

플래그를 사용하면 출력을 브라우저 창에 표시할 수 있습니다.
자세한 내용은 `go tool trace -help`를 실행하여 확인하십시오.
또한 GopherCon 2015의 이 [발표](/talks/2015/dynamic-tools.slide)에서 트레이싱 기능에 대한 설명을 확인하실 수 있습니다.

### Go doc 명령어 {#doc_command}

몇 번의 릴리스 전, `go doc` 명령은 불필요하다는 이유로 삭제되었습니다. 대신 언제나 "`godoc .`"을 실행하면 되었습니다.

1.5 릴리스에서는 `godoc`보다 더 편리한 커맨드라인 인터페이스를 갖춘 새로운 [`go doc`](/cmd/doc) 명령이 도입되었습니다. 이 명령은 특별히 커맨드라인 사용을 위해 설계되었으며, 호출 방식에 따라 패키지 또는 해당 요소에 대한 문서 내용을 더 간결하고 집중도 있게 제공합니다. 또한 대소문자를 구분하지 않는 매칭과 비공개(unexported) 심볼에 대한 문서 표시 기능을 지원합니다.

자세한 내용은 "`go help doc`"을 실행하여 확인하십시오.

### Cgo {#cgo}

`#cgo` 라인을 파싱할 때, `${SRCDIR}` 호출이 이제 소스 디렉토리 경로로 확장됩니다. 이를 통해 소스 코드 디렉토리를 기준으로 한 상대 파일 경로를 포함하는 옵션을 컴파일러와 링커에 전달할 수 있습니다. 이 확장 기능이 없다면, 현재 작업 디렉토리(current working directory)가 변경될 때 해당 경로들이 유효하지 않게 됩니다.

Solaris가 이제 완전한 cgo 지원을 제공합니다.

Windows에서 cgo는 이제 기본적으로 외부 링크(external linking)를 사용합니다.

C 구조체가 제로 크기 필드(zero-sized field)로 끝나지만 구조체 자체는 제로 크기가 아닌 경우, Go 코드는 더 이상 해당 제로 크기 필드를 참조할 수 없습니다. 이러한 모든 참조는 다시 작성되어야 합니다.

## 성능 {#performance}

언제나 그렇듯, 변경 사항이 매우 광범위하고 다양하여 성능에 대한 정확한 진술을 하기는 어렵습니다.
이번 릴리스에서는 새로운 가비지 컬렉터 도입과 런타임의 Go 변환이 포함되어 있어, 변경 범위가 평소보다 훨씬 더 넓습니다.
어떤 프로그램은 더 빠르게 실행될 수도 있고, 어떤 프로그램은 더 느려질 수도 있습니다.
평균적으로 Go 1 벤치마크 스위트의 프로그램들은 Go 1.4보다 Go 1.5에서 몇 퍼센트 더 빠르게 실행됩니다.
동시에 앞서 언급했듯이, 가비지 컬렉터의 일시 중단(pause) 시간은 획기적으로 단축되었으며 거의 항상 10밀리초 미만입니다.

Go 1.5의 빌드 속도는 약 2배 정도 느려질 것입니다.
컴파일러와 링커를 C에서 Go로 자동 변환하는 과정에서, 잘 작성된 Go 코드에 비해 성능이 떨어지는 비관용적인(unidiomatic) Go 코드가 생성되었습니다.
분석 도구와 리팩토링을 통해 코드를 개선했지만, 여전히 해야 할 작업이 많이 남아 있습니다.
추가적인 프로파일링과 최적화는 Go 1.6 및 향후 릴리스에서 계속해서 진행될 예정입니다.
더 자세한 내용은 이 [슬라이드](/talks/2015/gogo.slide)와 관련 [동영상](https://www.youtube.com/watch?v=cF1zJYkBW4A)을 참조하십시오.

## 표준 라이브러리 {#library}

### Flag {#flag}

`flag` 패키지의 [`PrintDefaults`](/pkg/flag/#PrintDefaults) 함수와 [`FlagSet`](/pkg/flag/#FlagSet) 메서드가 더 보기 좋은 사용법(usage) 메시지를 생성하도록 수정되었습니다. 포맷이 더 인간 친화적으로 변경되었으며, 사용법 메시지에서 \`백틱\`으로 감싸진 단어는 사용법 메시지에 표시될 플래그 피연산자의 이름으로 간주됩니다. 예를 들어, 다음과 같은 호출로 생성된 플래그의 경우,

`cpuFlag = flag.Int("cpu", 1, "run `N` processes in parallel")`

도움말 메시지를 표시합니다.

-cpu N
	    	N개의 프로세스를 병렬로 실행합니다 (기본값 1)

또한, 이제 기본값은 해당 타입의 제로 값(zero value)이 아닐 때만 표시됩니다.

### math/big의 Floats {#math_big}

[`math/big`](/pkg/math/big/) 패키지에는 임의 정밀도 부동 소수점 숫자를 구현하는 새로운 기본 데이터 타입인 [`Float`](/pkg/math/big/#Float)가 추가되었습니다. `Float` 값은 불리언 부호, 가변 길이 가수(mantissa), 그리고 32비트 고정 크기 유부호 지수로 표현됩니다. `Float`의 정밀도(비트 단위의 가수 크기)는 명시적으로 지정하거나, 값을 생성하는 첫 번째 연산에 의해 결정됩니다. 한 번 생성된 `Float`의 가수 크기는 [`SetPrec`](/pkg/math/big/#Float.SetPrec) 메서드를 통해 수정할 수 있습니다. `Float`는 오버플로 등으로 인해 발생하는 무한대(infinities) 개념을 지원하지만, IEEE 754의 NaN과 동일한 결과가 발생하는 값은 패닉(panic)을 발생시킵니다. `Float` 연산은 모든 IEEE-754 반올림 모드를 지원합니다. 정밀도가 24(53)비트로 설정되었을 때, 정규화된 `float32`(`float64`) 값의 범위 내에서 수행되는 연산은 해당 값들에 대한 IEEE-754 산술 연산과 동일한 결과를 생성합니다.

### Go 타입 {#go_types}

[`go/types`](/pkg/go/types/) 패키지는
지금까지 `golang.org/x` 저장소에서 유지 관리되어 왔으나, Go 1.5부터 메인 저장소로 이전되었습니다.
이전 위치의 코드는 이제 더 이상 사용되지 않습니다(deprecated).
또한 패키지에 약간의 API 변경 사항이 있으며, 이에 대한 내용은 아래에서 설명합니다.

이 이동과 함께, [`go/constant`](/pkg/go/constant/) 패키지도 메인 저장소로 이동되었습니다. 이전에는 `golang.org/x/tools/exact`였습니다. [`go/importer`](/pkg/go/importer/) 패키리와 위에서 설명한 일부 도구들 또한 메인 저장소로 이동되었습니다.

### Net {#net}

`net` 패키지의 DNS 리졸버는 시스템 인터페이스에 액세스하기 위해 거의 항상 `cgo`를 사용해 왔습니다.

Go 1.5에서의 변경 사항으로 인해 대부분의 Unix 시스템에서 DNS 리졸루션에 더 이상 `cgo`가 필요하지 않게 되었으며, 이는 해당 플랫폼에서의 실행을 단순화합니다.

이제 시스템의 네트워킹 설정이 허용한다면, 네이티브 Go 리졸버만으로 충분합니다.

이 변경 사항의 중요한 효과는 각 DNS 리졸루션이 스레드가 아닌 고루틴(goroutine)을 점유한다는 점이며, 따라서 여러 개의 DNS 요청이 대기 중인 프로그램이 더 적은 운영체제 리소스를 소비하게 됩니다.

리졸버(resolver)를 어떻게 실행할지에 대한 결정은 빌드 시간이 아닌 런타임에 적용됩니다.
Go 리졸버의 사용을 강제하기 위해 사용되었던 `netgo` 빌드 태그는 여전히 작동하지만 더 이상 필요하지 않습니다.
새로운 `netcgo` 빌드 태그는 빌드 시점에 `cgo` 리졸버의 사용을 강제합니다.
런타임에 `cgo` 리졸루션을 강제하려면 환경 변수에 `GODEBUG=netdns=cgo`를 설정하십시오.
더 많은 디버그 옵션은 [여기](/cl/11584)에 문서화되어 있습니다.

이 변경 사항은 Unix 시스템에만 적용됩니다.
Windows, Mac OS X 및 Plan 9 시스템은 이전과 동일하게 동작합니다.

### Reflect {#reflect}

[`reflect`](/pkg/reflect/) 패키지에 [`ArrayOf`](/pkg/reflect/#ArrayOf)와 [`FuncOf`](/pkg/reflect/#FuncOf)라는 두 개의 새로운 함수가 추가되었습니다. 기존의 [`SliceOf`](/pkg/reflect/#SliceOf) 함수와 유사하게, 이 함수들은 런타임에 배열과 함수를 설명하는 새로운 타입을 생성합니다.

### 하드닝 (Hardening) {#hardening}

[`go-fuzz`](https://github.com/dvyukov/go-fuzz) 도구를 이용한 무작위 테스트를 통해 표준 라이브러리에서 수십 개의 버그가 발견되었습니다.
다음 패키지들에서 버그가 수정되었습니다:
[`archive/tar`](/pkg/archive/tar/),
[`archive/zip`](/pkg/archive/zip/),
[`compress/flate`](/pkg/compress/flate/),
[`encoding/gob`](/pkg/encoding/gob/),
[`fmt`](/pkg/fmt/),
[`html/template`](/pkg/html/template/),
[`image/gif`](/pkg/image/gif/),
[`image/jpeg`](/pkg/image/jpeg/),
[`image/png`](/pkg/image/png/), 및
[`text/template`](/pkg/text/template/).
이러한 수정 사항들은 잘못되었거나 악의적인 입력에 대해 구현의 안정성을 강화합니다.

### 라이브러리의 사소한 변경 사항 {#minor_library_changes}

- [`archive/zip`](/pkg/archive/zip/) 패키지의 [`Writer`](/pkg/archive/zip/#Writer) 타입에 아카이브를 기록할 출력 스트림 내의 위치를 지정하는 [`SetOffset`](/pkg/archive/zip/#Writer.SetOffset) 메서드가 추가되었습니다.
  - [`bufio`](/pkg/bufio/) 패키지의 [`Reader`](/pkg/bufio/#Reader)에 입력 데이터를 버리는 [`Discard`](/pkg/bufio/#Reader.Discard) 메서드가 추가되었습니다.
  - [`bytes`](/pkg/bytes/) 패키지에서 [`Buffer`](/pkg/bytes/#Buffer) 타입에 버퍼 내에 할당된 바이트 수를 보고하는 [`Cap`](/pkg/bytes/#Buffer.Cap) 메서드가 추가되었습니다. 마찬가지로, [`bytes`](/pkg/bytes/) 및 [`strings`](/pkg/strings/) 패키지 모두에서 [`Reader`](/pkg/bytes/#Reader) 타입에 기반이 되는 슬라이스나 문자열의 원래 길이를 보고하는 [`Size`](/pkg/bytes/#Reader.Size) 메서드가 추가되었습니다.
  - [`bytes`](/pkg/bytes/) 및 [`strings`](/pkg/strings/) 패키지 모두에 인자로 전달된 값과 일치하는 가장 오른쪽 바이트의 위치를 찾는 [`LastIndexByte`](/pkg/bytes/#LastIndexByte) 함수가 추가되었습니다.
  - [`crypto`](/pkg/crypto/) 패키지에 비대칭 복호화에 사용되는 개인 키의 동작을 추상화하는 새로운 인터페이스인 [`Decrypter`](/pkg/crypto/#Decrypter)가 추가되었습니다.
  - [`crypto/cipher`](/pkg/crypto/cipher/) 패키지에서 소스와 대상의 길이가 다를 때의 동작에 관해 [`Stream`](/pkg/crypto/cipher/#Stream) 인터페이스의 문서가 명확해졌습니다. 대상이 소스보다 짧으면 메서드는 panic을 발생시킵니다. 이는 구현의 변경이 아니라 문서의 수정입니다.
  - 또한 [`crypto/cipher`](/pkg/crypto/cipher/) 패키지에서 일부 프로토콜에서 요구하는 AES의 Galois/Counter 모드(GCM)의 96바이트 이외의 nonce 길이에 대한 지원이 추가되었습니다.
  - [`crypto/elliptic`](/pkg/crypto/elliptic/) 패키지의 [`CurveParams`](/pkg/crypto/elliptic/#CurveParams) 구조체에 `Name` 필드가 추가되었으며, 패키지에 구현된 곡선들에 이름이 부여되었습니다. 이러한 이름은 곡선 의존적인 암호 시스템에서 비트 크기를 선택하는 대신 곡선을 선택하는 더 안전한 방법을 제공합니다.
  - 또한 [`crypto/elliptic`](/pkg/crypto/elliptic/) 패키지의 [`Unmarshal`](/pkg/crypto/elliptic/#Unmarshal) 함수가 이제 포인트가 실제로 곡선 위에 있는지 검증합니다. (그렇지 않은 경우 함수는 nil을 반환합니다). 이 변경 사항은 특정 공격을 방지합니다.
  - [`crypto/sha512`](/pkg/crypto/sha512/) 패키지가 이제 SHA-512 해시 알고리즘의 두 가지 절단 버전인 SHA-512/224 및 SHA-512/256을 지원합니다.
  - [`crypto/tls`](/pkg/crypto/tls/) 패키지의 최소 프로토콜 버전 기본값이 TLS 1.0으로 변경되었습니다. 필요한 경우 이전 기본값인 SSLv3는 여전히 [`Config`](/pkg/crypto/tls/#Config)를 통해 사용할 수 있습니다.
  - [`crypto/tls`](/pkg/crypto/tls/) 패키지가 이제 RFC 6962에 명시된 Signed Certificate Timestamps(SCTs)를 지원합니다. 서버는 SCT가 [`Certificate`](/pkg/crypto/tls/#Certificate) 구조체에 나열되어 있으면 이를 제공하며, 클라이언트는 이를 요청하고 존재할 경우 [`ConnectionState`](/pkg/crypto/tls/#ConnectionState) 구조체에서 이를 노출합니다.
  - 이전에 [`OCSPResponse`](/pkg/crypto/tls/#Conn.OCSPResponse) 메서드를 통해서만 사용할 수 있었던 [`crypto/tls`](/pkg/crypto/tls/) 클라이언트 연결의 stapled OCSP 응답이 이제 [`ConnectionState`](/pkg/crypto/tls/#ConnectionState) 구조체에서 노출됩니다.
  - [`crypto/tls`](/pkg/crypto/tls/) 서버 구현은 이제 인증서가 제공되지 않았을 때 연결을 위한 인증서를 선택하기 위해 [`Config`](/pkg/crypto/tls/#Config) 구조체의 `GetCertificate` 함수를 항상 호출합니다.
  - 마지막으로, [`crypto/tls`](/pkg/crypto/tls/) 패키지의 세션 티켓 키를 서버가 실행 중인 동안 변경할 수 있게 되었습니다. 이는 [`Config`](/pkg/crypto/tls/#Config) 타입의 새로운 [`SetSessionTicketKeys`](/pkg/crypto/tls/#Config.SetSessionTicketKeys) 메서드를 통해 수행됩니다.
  - [`crypto/x509`](/pkg/crypto/x509/) 패키지에서 와일드카드는 이제 [명세](https://tools.ietf.org/html/rfc6125#section-6.4.3)에 정의된 대로 가장 왼쪽 레이블에서만 허용됩니다.
  - 또한 [`crypto/x509`](/pkg/crypto/x509/) 패키지에서 알려지지 않은 중요 확장(critical extensions)의 처리 방식이 변경되었습니다. 이전에는 파싱 오류를 일으켰으나, 이제는 파싱은 되되 [`Verify`](/pkg/crypto/x509/#Certificate.Verify)에서만 오류를 발생시킵니다. [`Certificate`](/pkg/crypto/x509/#Certificate)의 새로운 필드 `UnhandledCriticalExtensions`에 이러한 확장들이 기록됩니다.
  - [`database/sql`](/pkg/database/sql/) 패키지의 [`DB`](/pkg/database/sql/#DB) 타입에 데이터베이스 통계를 가져오는 [`Stats`](/pkg/database/sql/#DB.Stats) 메서드가 추가되었습니다.
  - [`debug/dwarf`](/pkg/debug/dwarf/) 패키지는 DWARF 버전 4를 더 잘 지원하기 위해 광범위한 추가 사항이 반영되었습니다. 예를 들어 새로운 타입인 [`Class`](/pkg/debug/dwarf/#Class)의 정의를 확인하십시오.
  - [`debug/dwarf`](/pkg/debug/dwarf/) 패키지는 이제 DWARF 라인 테이블의 디코딩도 지원합니다.
  - [`debug/elf`](/pkg/debug/elf/) 패키지가 이제 64비트 PowerPC 아키텍처를 지원합니다.
  - [`encoding/base64`](/pkg/encoding/base64/) 패키지가 이제 두 개의 새로운 인코딩 변수인 [`RawStdEncoding`](/pkg/encoding/base64/#RawStdEncoding) 및 [`RawURLEncoding`](/pkg/encoding/base64/#RawURLEncoding)을 통해 패딩이 없는 인코딩을 지원합니다.
  - [`encoding/json`](/pkg/encoding/json/) 패키지는 이제 JSON 값이 언마샬링하려는 대상 변수나 컴포넌트에 적절하지 않은 경우 [`UnmarshalTypeError`](/pkg/encoding/json/#UnmarshalTypeError)를 반환합니다.
  - `encoding/json`의 [`Decoder`](/pkg/encoding/json/#Decoder) 타입에 JSON 문서를 디코딩하기 위한 스트리밍 인터페이스를 제공하는 새로운 메서드 [`Token`](/pkg/encoding/json/#Decoder.Token)이 추가되었습니다. 또한 이는 `Decode`의 기존 기능과 상호 운용되며, `Decoder.Token`으로 이미 시작된 디코딩 작업을 이어서 수행할 수 있습니다.
  - [`flag`](/pkg/flag/) 패키지에 위에서 설명한 새로운 관례를 사용하여 사용법 메시지를 작성하는 것을 돕는 [`UnquoteUsage`](/pkg/flag/#UnquoteUsage) 함수가 추가되었습니다.
  - [`fmt`](/pkg/fmt/) 패키지에서 [`Value`](/pkg/reflect/#Value) 타입의 값은 이제 `<int Value>`와 같은 결과를 내는 `reflect.Value`의 `Stringer` 메서드를 사용하는 대신, 해당 값이 보유한 내용을 출력합니다.
  - [`go/ast`](/pkg/go/ast/) 패키지의 [`EmptyStmt`](/pkg/ast/#EmptyStmt) 타입에 세미콜론이 암시적으로 추가되었는지 또는 소스에 존재했는지를 기록하는 불리언 `Implicit` 필드가 추가되었습니다.
  - 하위 호환성을 위해 [`go/build`](/pkg/go/build/) 패키지는 Go가 언젠가 지원할 수 있는 여러 아키텍처를 위해 `GOARCH` 값을 예약해 둡니다. 이것이 반드시 지원하겠다는 약속은 아닙니다. 또한, [`Package`](/pkg/go/build/#Package) 구조체에 설치할 아키텍처 종속적인 루트 디렉토리를 저장하는 `PkgTargetRoot` 필드가 추가되었습니다.
  - (새롭게 마이그레이션된) [`go/types`](/pkg/go/types/) 패키지에서는 여러 함수의 인자로 새로운 [`Qualifier`](/pkg/go/types/#Qualifier) 함수 타입을 사용하여 패키지 수준 이름에 붙는 접두사를 제어할 수 있습니다. 이는 패키지의 API 변경 사항이지만, 코어에 새로 추가된 것이므로 패키지를 사용하는 코드가 새 위치에서 명시적으로 요청해야 하기 때문에 Go 1 호환성 규칙을 깨뜨리지 않습니다. 업데이트하려면 패키지에서 [`go fix`](/cmd/go/#hdr-Run_go_tool_fix_on_packages)를 실행하십시오.
  - [`image`](/pkg/image/) 패키지에서 [`Rectangle`](/pkg/image/#Rectangle) 타입이 이제 [`Image`](/pkg/image/#Image) 인터페이스를 구현하므로, `Rectangle`을 그릴 때 마스크로 사용할 수 있습니다.
  - 또한 [`image`](/pkg/image/) 패키지에서 일부 JPEG 이미지 처리를 돕기 위해 4:1:1 및 4:1:0 YCbCr 서브샘플링과 기본 CMYK 지원(새로운 `image.CMYK` 구조체로 표현)이 추가되었습니다.
  - [`image/color`](/pkg/image/color/) 패키지는 일부 JPEG 이미지에 필요한 새로운 [`CMYK`](/pkg/image/color/#CMYK) 구조체, [`CMYKModel`](/pkg/image/color/#CMYKModel) 컬러 모델 및 [`CMYKToRGB`](/pkg/image/color/#CMYKToRGB) 함수를 통해 기본 CMYK 지원을 추가했습니다.
  - 또한 [`image/color`](/pkg/image/color/) 패키지에서 [`YCbCr`](/pkg/image/color/#YCbCr) 값을 `RGBA`로 변환하는 과정이 더 정밀해졌습니다. 이전에는 하위 8비트가 상위 8비트의 단순 반복이었으나, 이제는 더 정확한 정보를 포함합니다. 이전 코드의 반복 특성 때문에 8비트 빨간색 값을 추출하기 위한 `uint8(r)` 연산이 작동했으나 이는 부정확합니다. Go 1.5에서는 해당 연산이 다른 값을 반환할 수 있습니다. 올바른 코드는 항상 상위 8비트를 선택하는 `uint8(r>>8)`입니다. 참고로 `image/draw` 패키지는 이러한 변환에 대해 더 나은 지원을 제공합니다. 자세한 내용은 [이 블로그 포스트](/blog/go-imagedraw-package)를 참조하십시오.
  - 마지막으로, Go 1.5부터 [`Index`](/pkg/image/color/#Palette.Index)의 가장 가까운 일치 항목 확인 시 알파 채널을 고려합니다.
  - [`image/gif`](/pkg/image/gif/) 패키지에 몇 가지 일반화가 포함되었습니다. 이제 멀티 프레임 GIF 파일의 전체 경계(bounds)가 포함된 개별 프레임들의 경계와 다를 수 있습니다. 또한, [`GIF`](/pkg/image/gif/#GIF) 구조체에 각 프레임의 폐기 방법(disposal method)을 지정하는 `Disposal` 필드가 추가되었습니다.
  - [`io`](/pkg/io/) 패키지에 [`Copy`](/pkg/io/#Copy)와 유사하지만 호출자가 제공한 버퍼를 사용하여 할당 및 버퍼 크기를 제어할 수 있게 하는 [`CopyBuffer`](/pkg/io/#CopyBuffer) 함수가 추가되었습니다.
  - [`log`](/pkg/log/) 패키지에 타임스탬프를 UTC 시간대로 출력하게 하는 새로운 [`LUTC`](/pkg/log/#LUTC) 플래그가 추가되었습니다. 또한 사용자 정의 로거를 위한 [`SetOutput`](/pkg/log/#Logger.SetOutput) 메서드가 추가되었습니다.
  - Go 1.4에서 [`Max`](/pkg/math/#Max)는 가능한 모든 NaN 비트 패턴을 감지하지 못했습니다. 이는 Go 1.5에서 수정되었으므로, NaN이 포함된 데이터에 `math.Max`를 사용하는 프로그램은 다르게 동작할 수 있으나, 이제 NaN의 IEEE754 정의에 따라 올바르게 동작합니다.
  - [`math/big`](/pkg/math/big/) 패키지에 정수를 위한 새로운 [`Jacobi`](/pkg/math/big/#Jacobi) 함수와 [`Int`](/pkg/math/big/#Int) 타입을 위한 새로운 [`ModSqrt`](/pkg/math/big/#Int.ModSqrt) 메서드가 추가되었습니다.
  - mime 패키지에 RFC 204-인코딩된 단어가 포함된 MIME 헤더를 디코딩하기 위한 새로운 [`WordDecoder`](/pkg/mime/#WordDecoder) 타입이 추가되었습니다. 또한 RFC 2045 및 RFC 2047의 인코딩 scheme 구현체인 [`BEncoding`](/pkg/mime/#BEncoding) 및 [`QEncoding`](/pkg/mime/#QEncoding)을 제공합니다.
  - [`mime`](/pkg/mime/) 패키지에 특정 MIME 타입과 연관된 것으로 알려진 MIME 확장자들을 반환하는 [`ExtensionsByType`](/pkg/mime/#ExtensionsByType) 함수가 추가되었습니다.
  - RFC 2045에서 정의한 quoted-printable 인코딩을 구현하는 새로운 [`mime/quotedprintable`](/pkg/mime/quotedprintable/) 패키지가 추가되었습니다.
  - [`net`](/pkg/net/) 패키지의 [`Dial`](/pkg/net/#Dial)은 이제 성공할 때까지 각 IP 주소를 순서대로 시도하여 호스트 이름을 다이얼합니다. <code>[Dialer](/pkg/net/#Dialer).DualStack</code> 모드는 이제 첫 번째 주소 가족에 300ms의 우선권을 줌으로써 Happy Eyeballs ([RFC 6555](https://tools.ietf.org/html/rfc6555))를 구현합니다. 이 값은 새로운 `Dialer.FallbackDelay`로 재정의할 수 있습니다.
  - [`net`](/pkg/net/) 패키지의 에러가 반환하는 타입들의 여러 불일치 사항들이 정리되었습니다. 대부분 이제 이전보다 더 많은 정보를 담은 [`OpError`](/pkg/net/#OpError) 값을 반환합니다. 또한, [`OpError`](/pkg/net/#OpError) 타입에 로컬 네트워크 주소를 보유하는 `Source` 필드가 추가되었습니다.
  - [`net/http`](/pkg/net/http/) 패키지가 이제 서버 [`Handler`](/pkg/net/http/#Handler)로부터 트레일러(trailers)를 설정하는 기능을 지원합니다. 자세한 내용은 [`ResponseWriter`](/pkg/net/http/#ResponseWriter) 문서를 참조하십시오.
  - 새로운 [`Request.Cancel`](/pkg/net/http/#Request) 필드를 설정하여 [`net/http`](/pkg/net/http/) `Request`를 취소할 수 있는 새로운 방법이 추가되었습니다. 이는 `http.Transport`에 의해 지원됩니다. `Cancel` 필드의 타입은 [`context.Context.Done`](https://godoc.org/golang.org/x/net/context) 반환 값과 호환됩니다.
  - 또한 [`net/http`](/pkg/net/http/) 패키지의 [`ServeContent`](/pkg/net/#ServeContent) 함수에서 제로 [`Time`](/pkg/time/#Time) 값을 무시하는 코드가 추가되었습니다. Go 1.5부터는 Unix epoch와 동일한 시간 값도 무시합니다.
  - [`net/http/fcgi`](/pkg/net/http/fcgi/) 패키지가 해당 에러 상태를 보고하기 위해 [`ErrConnClosed`](/pkg/net/http/fcgi/#ErrConnClosed) 및 [`ErrRequestAborted`](/pkg/net/http/fcgi/#ErrRequestAborted)라는 두 개의 새로운 에러를 내보냅니다.
  - [`net/http/cgi`](/pkg/net/http/cgi/) 패키지에 환경 변수 `REMOTE_ADDR` 및 `REMOTE_HOST`의 값을 잘못 처리하던 버그가 있었으며, 이것이 수정되었습니다. 또한 Go 1.5부터 이 패키지는 `REMOTE_PORT` 변수를 설정합니다.
  - [`net/mail`](/pkg/net/mail/) 패키지에 메일 주소를 파싱할 수 있는 [`AddressParser`](/pkg/net/mail/#AddressParser) 타입이 추가되었습니다.
  - [`net/smtp`](/pkg/net/smtp/) 패키지의 [`Client`](/pkg/net/smtp/#Client) 타입에 클라이언트의 TLS 상태를 반환하는 [`TLSConnectionState`](/pkg/net/smtp/#Client.TLSConnectionState) 액세서가 추가되었습니다.
  - [`os`](/pkg/os/) 패키지에 [`Getenv`](/pkg/os/#Getenv)와 유사하지만 빈 환경 변수와 없는 환경 변수를 구분할 수 있는 새로운 [`LookupEnv`](/pkg/os/#LookupEnv) 함수가 추가되었습니다.
  - [`os/signal`](/pkg/os/signal/) 패키지에 새로운 [`Ignore`](/pkg/os/signal/#Ignore) 및 [`Reset`](/pkg/os/signal/#Reset) 함수가 추가되었습니다.
  - [`runtime`](/pkg/runtime/), [`runtime/trace`](/pkg/runtime/trace/), [`net/http/pprof`](/pkg/net/http/pprof/) 패키지 각각에 위에서 설명한 트레이싱 기능을 지원하는 새로운 함수들이 추가되었습니다: [`ReadTrace`](/pkg/runtime/#ReadTrace), [`StartTrace`](/pkg/runtime/#StartTrace), [`StopTrace`](/pkg/runtime/#StopTrace), [`Start`](/pkg/runtime/trace/#Start), [`Stop`](/pkg/runtime/trace/#Stop), [`Trace`](/pkg/net/http/pprof/#Trace). 자세한 내용은 각각의 문서를 참조하십시오.
  - [`runtime/pprof`](/pkg/runtime/pprof/) 패키지는 이제 기본적으로 모든 메모리 프로파일에 전반적인 메모리 통계를 포함합니다.
  - [`strings`](/pkg/strings/) 패키지에 새로운 [`Compare`](/pkg/strings/#Compare) 함수가 추가되었습니다. 이는 [`bytes`](/pkg/bytes/) 패키지와의 대칭성을 제공하기 위해 추가되었으며, 문자열은 기본적으로 비교를 지원하므로 그 외에는 불필요합니다.
  - [`sync`](/pkg/sync/) 패키지의 [`WaitGroup`](/pkg/sync/#WaitGroup) 구현은 이제 [`Add`](/pkg/sync/#WaitGroup.Add) 호출과 [`Wait`](/pkg/sync/#WaitGroup.Wait) 반환 사이에서 발생하는 레이스(race) 코드를 진단합니다. 이러한 조건이 감지되면 구현체는 panic을 발생시킵니다.
  - [`syscall`](/pkg/syscall/) 패키지에서 Linux `SysProcAttr` 구조체에 Linux 3.19의 보안 변경 사항으로 인해 필요해진 `GidMappingsEnableSetgroups` 필드가 추가되었습니다. 모든 Unix 시스템에서 해당 구조체에는 exec 시 더 많은 제어를 제공하기 위한 새로운 `Foreground` 및 `Pgid` 필드가 추가되었습니다. Darwin에서는 인수가 너무 많은 호출을 지원하기 위해 `Syscall9` 함수가 추가되었습니다.
  - [`testing/quick`](/pkg/testing/quick/)은 이제 포인터 타입에 대해 `nil` 값을 생성하여 재귀적 데이터 구조에서도 사용할 수 있게 되었습니다. 또한 이제 배열 타입의 생성도 지원합니다.
  - [`text/template`](/pkg/text/template/) 및 [`html/template`](/pkg/html/template/) 패키지에서 Go 정수로 표현하기에 너무 큰 정수 상수는 이제 파싱 에러를 트리거합니다. 이전에는 정밀도를 잃으며 묵시적으로 부동 소수점으로 변환되었습니다.
  - 또한 [`text/template`](/pkg/text/template/) 및 [`html/template`](/pkg/html/template/) 패키지에서 새로운 [`Option`](/pkg/text/template/#Template.Option) 메서드를 통해 실행 중 템플릿의 동작을 커스터마이징할 수 있습니다. 구현된 유일한 옵션은 맵을 인덱싱할 때 누락된 키를 처리하는 방법을 제어하는 것입니다. 이제 재정의 가능한 기본값은 이전과 동일하게 잘못된 값(invalid value)으로 계속 진행하는 것입니다.
  - [`time`](/pkg/time/) 패키지의 `Time` 타입에 시간 값을 출력할 때 할당을 피하는 데 사용할 수 있는 새로운 메서드 [`AppendFormat`](/pkg/time/#Time.AppendFormat)이 추가되었습니다.
  - [`unicode`](/pkg/unicode/) 패키지와 시스템 전반의 관련 지원 사항이 버전 7.0에서 [Unicode 8.0](https://www.unicode.org/versions/Unicode8.0.0/)으로 업그레이드되었습니다.
