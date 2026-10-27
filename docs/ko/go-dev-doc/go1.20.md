<!--
참고: 이 문서와 이 디렉토리의 다른 문서들에서는 `hello` `world`와 같이 고정 폭 구절을 고정 폭이 아닌 공백으로 설정하는 관례를 따릅니다.
이러한 구절에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

<style>
  main ul li { margin: 0.5em 0; }
</style>

## Go 1.20 소개 {#introduction}

최신 Go 릴리스인 버전 1.20은 [Go 1.19](/doc/go1.19) 이후 6개월 만에 출시되었습니다.
변경 사항의 대부분은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언제나 그렇듯, 이번 릴리스는 Go 1의 [호환성 약속](/doc/go1compat)을 유지합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

Go 1.20에는 언어에 대한 네 가지 변경 사항이 포함되어 있습니다.

<!-- https://go.dev/issue/46505 -->
Go 1.17에서는 [슬라이스에서 배열 포인터로의 변환](/ref/spec#Conversions_from_slice_to_array_or_array_pointer)이 추가되었습니다.
Go 1.20에서는 이를 확장하여 슬라이스에서 배열로의 변환을 허용합니다:
슬라이스 `x`가 주어졌을 때, 이제 `*(*[4]byte)(x)` 대신 `[4]byte(x)`라고 작성할 수 있습니다.

<!-- https://go.dev/issue/53003 -->
[`unsafe` 패키지](/ref/spec/#Package_unsafe)에 `SliceData`, `String`, `StringData`라는 세 가지 새로운 함수가 정의되었습니다.
Go 1.17의 `Slice`와 더불어, 이제 이 함수들은 슬라이스와 문자열의 정확한 표현 방식에 의존하지 않고도 슬라이스 및 문자열 값을 생성하고 분해할 수 있는 완전한 기능을 제공합니다.

<!-- https://go.dev/issue/8606 -->
이제 명세서에서는 구조체(struct) 값의 비교가 구조체 타입 정의에 나타나는 순서대로 필드를 하나씩 비교하며, 첫 번째 불일치가 발생하는 지점에서 중단된다고 정의합니다.
이전 명세서에서는 첫 번째 불일치 이후에도 모든 필드를 비교해야 하는 것처럼 해석될 여지가 있었습니다.
마찬가지로, 배열(array) 값의 비교 또한 인덱스가 증가하는 순서대로 요소를 하나씩 비교한다고 정의합니다.
두 경우 모두, 이러한 차이는 특정 비교 상황에서 패닉(panic)이 발생해야 하는지 여부에 영향을 줍니다.
기존 프로그램에는 변동 사항이 없습니다. 새로운 명세서 문구는 구현체들이 항상 수행해 온 방식을 설명한 것입니다.

<!-- https://go.dev/issue/56548 -->
[비교 가능한 타입](/ref/spec#Comparison_operators) (일반 인터페이스 등)은 타입 인자가 엄격하게 비교 가능하지 않더라도 이제 `comparable` 제약 조건을 충족할 수 있습니다 (비교 시 런타임에 panic이 발생할 수 있습니다). 이를 통해 `comparable`로 제약된 타입 파라미터(예: 사용자 정의 제네릭 맵 키의 타입 파라미터)를 인터페이스 타입이나 인터페이스 타입을 포함하는 복합 타입과 같이 엄격하게 비교 가능하지 않은 타입 인자로 인스턴스화하는 것이 가능해집니다.

## 포트 {#ports}

### Windows {#windows}

<!-- https://go.dev/issue/57003, https://go.dev/issue/57004 -->
Go 1.20은 Windows 7, 8, Server 2008 및 Server 2012의 모든 릴리스에서 실행 가능한 마지막 릴리스입니다.
Go 1.21부터는 최소 Windows 10 또는 Server 2016이 필요합니다.

### Darwin 및 iOS {#darwin}

<!-- https://go.dev/issue/23011 -->
Go 1.20은 macOS 10.13 High Sierra 또는 10.14 Mojave에서 실행되는 마지막 릴리스입니다.
Go 1.21부터는 macOS 10.15 Catalina 이상 버전이 필요합니다.

### FreeBSD/RISC-V {#freebsd-riscv}

<!-- https://go.dev/issue/53466 -->
Go 1.20은 RISC-V 기반 FreeBSD(`GOOS=freebsd`, `GOARCH=riscv64`)에 대한 실험적 지원을 추가합니다.

## 도구 {#tools}

### Go 명령어 {#go-command}

<!-- CL 432535, https://go.dev/issue/47257 -->
`$GOROOT/pkg` 디렉토리는 더 이상 표준 라이브러리를 위한 사전 컴파일된 패키지 아카이브를 저장하지 않습니다:
`go` `install`은 더 이상 이를 작성하지 않으며,
`go` build는 더 이상 이를 확인하지 않고,
Go 배포판에도 더 이상 포함되지 않습니다.
대신, 표준 라이브러리의 패키지들은 `GOROOT` 외부의 패키지들과 마찬가지로 필요할 때 빌드되어 빌드 캐시에 저장됩니다.
이 변경 사항은 Go 배포판의 크기를 줄이며, cgo를 사용하는 패키지에서 발생할 수 있는 C 툴체인 불일치(skew) 문제를 방지합니다.

<!-- CL 448357: cmd/go: print test2json start events -->
`go` `test` `-json` 구현이 더욱 견고하게 개선되었습니다.
`go` `test` `-json`을 실행하는 프로그램은 업데이트가 필요하지 않습니다.
`go` `tool` `test2json`을 직접 호출하는 프로그램은 이제 일반 `-v` 대신 `-v=test2json`으로 테스트 바이너리를 실행해야 합니다.
(예: `go` `test` `-v=test2json` 또는 `./pkg.test` `-test.v=test2json`)

<!-- CL 448357: cmd/go: print test2json start events -->
`go` `test` `-json`와 관련된 변경 사항으로,
각 테스트 프로그램의 실행 시작 시점에 `Action`이 `start`로 설정된
이벤트가 추가되었습니다.
`go` 명령어를 사용하여 여러 테스트를 실행할 때,
이러한 시작 이벤트들은 명령줄에 지정된 패키지 순서와 동일한 순서로
출력됨이 보장됩니다.

<!-- https://go.dev/issue/45454, CL 421434 -->
이제 `go` 명령어는 `amd64.v2`와 같은 아키텍처 기능 빌드 태그를 정의하여, 특정 아키텍처 기능의 유무에 따라 패키지 구현 파일을 선택할 수 있도록 지원합니다. 자세한 내용은 [`go` `help` `buildconstraint`](/cmd/go#hdr-Build_constraints)를 참조하십시오.

<!-- https://go.dev/issue/50332 -->
이제 `go` 서브커맨드에서 `-C` `<dir>` 옵션을 사용하여 명령을 수행하기 전 디렉터리를 `<dir>`로 변경할 수 있습니다. 이는 여러 서로 다른 모듈에서 명령을 실행해야 하는 스크립트에서 유용하게 사용될 수 있습니다.

<!-- https://go.dev/issue/41696, CL 416094 -->
`go` `build` 및 `go` `test`
명령어에서 더 이상 `-i` 플래그를 지원하지 않습니다.
이 플래그는 [Go 1.16부터 deprecated 되었습니다](/issue/41696).

<!-- https://go.dev/issue/38687, CL 421440 -->
이제 `go` `generate` 명령에서 `<pattern>`과 일치하는 `//go:generate` 지시문을 건너뛰기 위한 `-skip` `<pattern>` 옵션을 사용할 수 있습니다.

<!-- https://go.dev/issue/41583 -->
이제 `go` `test` 명령에서 `-skip` `<pattern>`을 사용하여 `<pattern>`과 일치하는 테스트, 서브테스트 또는 예제(examples)를 건너뛸 수 있습니다.

<!-- https://go.dev/issue/37015 -->
메인 모듈이 `GOPATH/src` 내에 위치할 때, `go` `install`은 더 이상 `main`이 아닌 패키지의 라이브러리를 `GOPATH/pkg`에 설치하지 않으며, `go` `list`는 이러한 패키지에 대해 `Target` 필드를 더 이상 보고하지 않습니다. (모듈 모드에서 컴파일된 패키지는 [빌드 캐시](https://pkg.go.dev/cmd/go#hdr-Build_and_test_caching)에만 저장되지만, [버그](/issue/37015)로 인해 `GOPATH` 설치 타겟이 예상치 않게 계속 적용되는 문제가 있었습니다.)

<!-- https://go.dev/issue/55022 -->
`go` `build`, `go` `install` 및 기타 빌드 관련 명령어가 이제 프로필 기반 최적화(profile-guided optimization)를 활성화하는 `-pgo` 플래그를 지원합니다. 이에 대한 자세한 내용은 아래의 [Compiler](#compiler) 섹션에 설명되어 있습니다.
`-pgo` 플래그는 프로필의 파일 경로를 지정합니다.
`-pgo=auto`를 지정하면 `go` 명령어가 메인 패키지의 디렉토리에서 `default.pgo`라는 이름의 파일을 찾아 존재할 경우 이를 사용합니다.
현재 이 모드는 명령줄에 단일 메인 패키지가 지정되어야 하지만, 향후 릴리스에서 이 제한을 해제할 계획입니다.
`-pgo=off`를 지정하면 프로필 기반 최적화가 비활성화됩니다.

<!-- https://go.dev/issue/51430 -->
이제 `go` `build`, `go` `install` 및 기타 빌드 관련 명령에서 지정된 타겟을 코드 커버리지 계측(instrumentation)과 함께 빌드하는 `-cover` 플래그를 지원합니다.
자세한 내용은 아래의 [Cover](#cover) 섹션에 설명되어 있습니다.

#### `go` `version` {#go-version}

<!-- https://go.dev/issue/48187 -->
`go` `version` `-m` 명령어가 이제 더 많은 유형의 Go 바이너리 읽기를 지원합니다. 특히 `go` `build` `-buildmode=c-shared`로 빌드된 Windows DLL과 실행 권한이 없는 Linux 바이너리가 포함됩니다.

### Cgo {#cgo}

<!-- CL 450739 -->
이제 `go` 명령은 C 툴체인이 없는 시스템에서 기본적으로 `cgo`를 비활성화합니다.
더 구체적으로, `CGO_ENABLED` 환경 변수가 설정되지 않았고,
`CC` 환경 변수가 설정되지 않았으며,
기본 C 컴파일러(일반적으로 `clang` 또는 `gcc`)를
경로(path)에서 찾을 수 없는 경우,
`CGO_ENABLED`는 기본값으로 `0`이 됩니다.
언제나 그렇듯, `CGO_ENABLED`를 명시적으로 설정하여 기본값을 재정의할 수 있습니다.

기본값 변경의 가장 중요한 영향은 C 컴파일러가 없는 시스템에 Go를 설치했을 때, cgo를 사용하는 표준 라이브러리 패키지에 대해 이제 ( [위에서 언급한](#go-command) 대로 제거된 ) 사전 배포된 패키지 아카이브를 사용하거나 cgo 사용을 시도하다 실패하는 대신, 순수 Go 빌드(pure Go builds)를 사용한다는 점입니다.

이로 인해 일부 최소화된 컨테이너 환경뿐만 아니라, Go 1.16 이후로 cgo 기반 패키지에 대해 사전 배포된 패키지 아카이브를 사용하지 않은 macOS에서도 Go가 더 원활하게 작동하게 됩니다.

cgo를 사용하는 표준 라이브러리 패키지는 [`net`](/pkg/net/), [`os/user`](/pkg/os/user/), 그리고 [`plugin`](/pkg/plugin/)입니다.
macOS의 경우, `net` 및 `os/user` 패키지는 cgo를 사용하지 않도록 재작성되었습니다. 이제 cgo 및 non-cgo 빌드뿐만 아니라 교차 컴파일 빌드에서도 동일한 코드가 사용됩니다.
Windows의 경우, `net` 및 `os/user` 패키지는 cgo를 사용한 적이 없습니다.
그 외의 시스템에서는 cgo가 비활성화된 빌드 시 이러한 패키지들의 pure Go 버전이 사용됩니다.

그 결과, macOS에서 `net` 패키지를 사용하는 Go 코드를 `-buildmode=c-archive`로 빌드한 경우, 생성된 아카이브를 C 프로그램에 링크하려면 C 코드를 링크할 때 `-lresolv`를 전달해야 합니다.

macOS에서 레이스 디텍터(race detector)는 cgo를 사용하지 않도록 재작성되었습니다:
`race-detector-enabled` 프로그램은 Xcode 없이도 빌드하고 실행할 수 있습니다.
Linux 및 기타 Unix 시스템과 Windows에서는 레이스 디텍터를 사용하기 위해 호스트 C 툴체인이 필요합니다.

### 커버 {#cover}

<!-- CL 436236, CL 401236, CL 438503 -->
Go 1.20은 단순한 단위 테스트뿐만 아니라 프로그램(애플리케이션 및 통합 테스트)에 대한 코드 커버리지 프로파일 수집을 지원합니다.

프로그램의 커버리지 데이터를 수집하려면 `go build` 명령의 `-cover` 플래그를 사용하여 빌드한 다음, 커버리지 프로필이 저장될 출력 디렉토리를 환경 변수 `GOCOVERDIR`로 설정하여 결과 바이너리를 실행하십시오.

시작 방법에 대한 자세한 내용은 ['coverage for integration tests' 랜딩 페이지](/doc/build-cover)를 참조하십시오. 설계 및 구현에 관한 세부 사항은 [제안서](/issue/51430)를 참조하십시오.

### Vet {#vet}

#### 중첩 함수에 의한 루프 변수 캡처 탐지 개선 {#vet-loopclosure}

<!-- CL 447256, https://go.dev/issue/55972: extend the loopclosure analysis to parallel subtests -->
`vet` 도구가 이제 서브테스트 함수 본문 내에서 [`T.Parallel()`](/pkg/testing/#T.Parallel) 호출 이후의 루프 변수 참조를 보고합니다. 이러한 참조는 다른 반복문의 변수 값을 관찰하거나(일반적으로 테스트 케이스가 건너뛰어지는 원인이 됨), 동기화되지 않은 동시 액세스로 인해 잘못된 상태를 관찰할 수 있습니다.

<!-- CL 452615 -->
이 도구는 이제 더 많은 곳에서 참조 오류를 감지합니다. 이전에는 루프 본문의 마지막 문장만 고려했지만, 이제는 `if`, `switch`, `select` 문 내의 마지막 문장들을 재귀적으로 검사합니다.

#### 잘못된 시간 형식에 대한 새로운 진단 도구 {#vet-timeformat}

<!-- CL 354010, https://go.dev/issue/48801: check for time formats with 2006-02-01 -->
이제 vet 도구는 [`Time.Format`](/pkg/time/#Time.Format) 및 [`time.Parse`](/pkg/time/#Parse)에서 `2006-02-01` (yyyy-dd-mm) 시간 형식을 사용하는 경우를 보고합니다.
이 형식은 일반적인 날짜 표준에 나타나지 않지만, ISO 8601 날짜 형식 (yyyy-mm-dd)을 사용하려 할 때 실수로 자주 사용됩니다.

## 런타임 {#runtime}

<!-- CL 422634 -->
가비지 컬렉터의 일부 내부 데이터 구조가 공간 및 CPU 효율성을 모두 높이는 방향으로 재구성되었습니다.
이 변경 사항을 통해 메모리 오버헤드가 감소하며, 전체적인 CPU 성능이 최대 2% 향상됩니다.

<!-- CL 417558, https://go.dev/issue/53892 -->
일부 상황에서 가비지 컬렉터가 고루틴 어시스트(goroutine assists)와 관련하여 덜 변덕스럽게 동작합니다.

<!-- https://go.dev/issue/51430 -->
Go 1.20에서는 `os.Exit()`를 통해 종료되지 않는 장기 실행 프로그램 및 서버 프로그램에서 런타임 중에 커버리지 프로파일 데이터를 작성할 수 있는 API를 포함하는 새로운 `runtime/coverage` 패키지가 추가되었습니다.

## 컴파일러 {#compiler}

<!-- https://go.dev/issue/55022 -->
Go 1.20에서는 프로필 기반 최적화(PGO)에 대한 프리뷰 지원이 추가되었습니다.
PGO를 통해 툴체인은 런타임 프로필 정보를 기반으로 애플리케이션 및 워크로드 특화 최적화를 수행할 수 있습니다.
현재 컴파일러는 `runtime/pprof` 또는 `net/http/pprof` 패키지와 같은 일반적인 수단으로 수집할 수 있는 pprof CPU 프로필을 지원합니다.
PGO를 활성화하려면 [위](#go-command)에서 언급한 대로 `go` `build` 명령에 `-pgo` 플래그를 통해 pprof 프로필 파일의 경로를 전달하십시오.
Go 1.20은 PGO를 사용하여 핫 콜 사이트(hot call sites)에서 함수 인라이닝을 더 공격적으로 수행합니다.
대표적인 Go 프로그램 세트에 대한 벤치마크 결과, 프로필 기반 인라이닝 최적화를 활성화하면 성능이 약 3~4% 향상되는 것으로 나타났습니다.
자세한 문서는 [PGO 사용자 가이드](/doc/pgo)를 참조하십시오.
향후 릴리스에서 더 많은 프로필 기반 최적화를 추가할 계획입니다.
프로필 기반 최적화는 프리뷰 기능이므로 적절한 주의를 기울여 사용하시기 바랍니다.

Go 1.20 컴파일러는 컴파일러의 내부 데이터를 처리하는 새로운 방식을 사용하도록 프론트엔드를 업그레이드했습니다. 이를 통해 여러 제네릭 타입(generic-types) 문제가 해결되었으며, 제네릭 함수 및 메서드 내에서 타입 선언이 가능해졌습니다.

<!-- https://go.dev/issue/56103, CL 445598 -->
이제 컴파일러는 기본적으로 컴파일러 오류를 통해 [익명 인터페이스 순환 참조(anonymous interface cycles)](/issue/56103)를 거부합니다.
이러한 문제는 [임베디드 인터페이스](/ref/spec#Embedded_interfaces)의 까다로운 사용 방식에서 발생하며, 항상 미묘한 정확성 문제를 가지고 있었습니다. 하지만 실제로 실무에서 사용되고 있다는 증거는 찾지 못했습니다.
이 변경 사항으로 인해 부정적인 영향을 받은 사용자의 보고가 없다면, 도구 제작자들도 더 이상 이를 지원하지 않도록 Go 1.22 언어 명세에서 이를 공식적으로 금지할 계획입니다.

<!-- https://go.dev/issue/49569 -->
Go 1.18 및 1.19에서는 제네릭(generics) 지원 추가와 그에 따른 후속 작업으로 인해 빌드 속도가 저하되는 현상이 있었습니다. Go 1.20은 빌드 속도를 최대 10% 향상시켜 Go 1.17 수준으로 회복시켰습니다.
Go 1.19와 비교하여, 생성된 코드의 성능 또한 전반적으로 약간 향상되었습니다.

## Linker {#linker}

<!-- https://go.dev/issue/54197, CL 420774 -->
Linux에서 링커가 이제 링크 시점에 `glibc` 또는 `musl`을 위한 동적 인터프리터(dynamic interpreter)를 선택합니다.

<!-- https://go.dev/issue/35006 -->
이제 Windows에서 Go 링커가 최신 LLVM 기반 C 툴체인을 지원합니다.

<!-- https://go.dev/issue/37762, CL 317917 -->
Go 1.20은 컴파일러가 생성하는 심볼에 `go.` 및 `type.` 대신 `go:` 및 `type:` 접두사를 사용합니다.
이는 이름이 `go.`로 시작하는 사용자 패키지와의 혼동을 방지하기 위함입니다.
[`debug/gosym`](/pkg/debug/gosym) 패키지는 Go 1.20 및 그 이후 버전으로 빌드된 바이너리의 이러한 새로운 명명 규칙을 인식합니다.

## Bootstrap {#bootstrap}

<!-- https://go.dev/issue/44505 -->
소스에서 Go 릴리스를 빌드할 때 `GOROOT_BOOTSTRAP`이 설정되어 있지 않으면, 이전 버전의 Go는 `$HOME/go1.4`(`Windows의 경우 %HOMEDRIVE%%HOMEPATH%\go1.4`) 디렉토리에서 Go 1.4 이상의 부트스트랩 툴체인을 찾았습니다.

Go 1.18 및 Go 1.19는 Go 1.20 부트스트랩 시 Go 1.17이 필요할 것에 대비하여, `$HOME/go1.4`로 폴백(fallback)하기 전에 `$HOME/go1.17` 또는 `$HOME/sdk/go1.17`을 먼저 찾았습니다.

Go 1.20은 실제로 부트스트랩을 위해 Go 1.17 릴리스가 필요하지만, 부트스트랩 툴체인의 최신 포인트 릴리스를 채택해야 한다는 점을 깨달아 Go 1.17.13이 필요하게 되었습니다. Go 1.20은 `$HOME/go1.4`로 폴백하기 전에 `$HOME/go1.17.13` 또는 `$HOME/sdk/go1.17.13`을 찾습니다 (이는 `$HOME/go1.4` 경로를 하드코딩했지만 그곳에 더 최신 버전의 Go 툴체인을 설치한 시스템을 지원하기 위함입니다).

향후에는 부트스트랩 툴체인을 대략 1년에 한 번씩 업데이트할 계획이며, 특히 Go 1.22는 부트스트랩을 위해 Go 1.20의 최종 포인트 릴리스가 필요할 것으로 예상됩니다.

## 표준 라이브러리 {#library}

### 새로운 crypto/ecdh 패키지 {#crypto_ecdh}

<!-- https://go.dev/issue/52221, CL 398914, CL 450335, https://go.dev/issue/56052 -->
Go 1.20에서는 NIST 커브 및 Curve25519를 통한 Elliptic Curve Diffie-Hellman 키 교환을 명시적으로 지원하기 위해 새로운 [`crypto/ecdh`](/pkg/crypto/ecdh/) 패키지를 추가합니다.

프로그램은 ECDH를 위해 [`crypto/elliptic`](/pkg/crypto/elliptic/)의 하위 수준 기능 대신 `crypto/ecdh`를 사용해야 하며, 더 고급 사용 사례의 경우 서드파티 모듈을 사용해야 합니다.

### 여러 에러 래핑하기 {#errors}

<!-- CL 432898 -->
Go 1.20에서는 하나의 에러가 여러 개의 다른 에러를 래핑(wrap)할 수 있도록 에러 래핑 지원 범위를 확장했습니다.

에러 `e`는 `[]error`를 반환하는 `Unwrap` 메서드를 제공함으로써 하나 이상의 에러를 래핑(wrap)할 수 있습니다.

[`errors.Is`](/pkg/errors/#Is) 및 [`errors.As`](/pkg/errors/#As) 함수가 여러 번 래핑된(wrapped) 에러를 검사할 수 있도록 업데이트되었습니다.

[`fmt.Errorf`](/pkg/fmt/#Errorf) 함수는
이제 `%w` 포맷 동사의 중복 사용을 지원하며,
이를 통해 해당 모든 에러 피연산자를 래핑(wrap)하는 에러를 반환합니다.

새로운 함수 [`errors.Join`](/pkg/errors/#Join)은 에러 리스트를 래핑하는 에러를 반환합니다.

### HTTP ResponseController {#http_responsecontroller}

<!-- CL 436890, https://go.dev/issue/54136 -->
새로운 [`"net/http".ResponseController`](/pkg/net/http/#ResponseController) 타입은 [`"net/http".ResponseWriter`](/pkg/net/http/#ResponseWriter) 인터페이스에서 처리되지 않는 확장된 요청별 기능에 대한 액세스를 제공합니다.

이전에는 `ResponseWriter`가 구현할 수 있는 [`Flusher`](/pkg/net/http/#Flusher)와 같은 선택적 인터페이스를 정의함으로써 요청당 새로운 기능을 추가해 왔습니다. 이러한 인터페이스들은 발견 가능성이 낮으며 사용하기에 번거롭습니다.

`ResponseController` 타입은 핸들러별 제어 기능을 추가할 수 있는 더 명확하고 발견하기 쉬운 방법을 제공합니다. Go 1.20에서 함께 추가된 두 가지 제어 기능은 `SetReadDeadline`과 `SetWriteDeadline`으로, 요청별 읽기 및 쓰기 마감 시간을 설정할 수 있게 해줍니다. 예를 들어:

```go
func RequestHandler(w ResponseWriter, r *Request) {
	  rc := http.NewResponseController(w)
	  rc.SetWriteDeadline(time.Time{}) // 대용량 응답을 보낼 때 Server.WriteTimeout을 비활성화합니다.
	  io.Copy(w, bigData)
	}
```

### 새로운 ReverseProxy Rewrite 훅 {#reverseproxy_rewrite}

<!-- https://go.dev/issue/53002, CL 407214 -->
[`httputil.ReverseProxy`](/pkg/net/http/httputil/#ReverseProxy) 포워딩 프록시에 기존의 `Director` 훅을 대체하는 새로운 [`Rewrite`](/pkg/net/http/httputil/#ReverseProxy.Rewrite) 훅 함수가 추가되었습니다.

`Rewrite` 훅은 [`ProxyRequest`](/pkg/net/http/httputil/#ProxyRequest) 파라미터를 받으며, 여기에는 프록시가 수신한 인바운드 요청과 프록시가 전송할 아웃바운드 요청이 모두 포함됩니다.
아웃바운드 요청에만 작동하는 `Director` 훅과 달리, 이를 통해 `Rewrite` 훅은 악의적인 인바운드 요청으로 인해 훅에서 추가한 헤더가 전달되기 전에 제거될 수 있는 특정 시나리오를 방지할 수 있습니다.
[issue #50580](/issue/50580)을 참조하십시오.

[`ProxyRequest.SetURL`](/pkg/net/http/httputil/#ProxyRequest.SetURL) 메서드는 외부로 나가는 요청을 제공된 목적지로 라우팅하며, `NewSingleHostReverseProxy` 함수를 대체합니다. `NewSingleHostReverseProxy`와 달리, `SetURL`은 외부 요청의 `Host` 헤더도 함께 설정합니다.

<!-- https://go.dev/issue/50465, CL 407414 -->
[`ProxyRequest.SetXForwarded`](/pkg/net/http/httputil/#ProxyRequest.SetXForwarded)
메서드는 송신 요청의 `X-Forwarded-For`, `X-Forwarded-Host`,
및 `X-Forwarded-Proto` 헤더를 설정합니다.
`Rewrite`를 사용하는 경우, 이러한 헤더들은 기본적으로 추가되지 않습니다.

이러한 기능들을 사용하는 `Rewrite` 훅의 예시는 다음과 같습니다:

```go
proxyHandler := &httputil.ReverseProxy{
	  Rewrite: func(r *httputil.ProxyRequest) {
	    r.SetURL(outboundURL) // 요청을 outboundURL로 전달합니다.
	    r.SetXForwarded()     // X-Forwarded-* 헤더를 설정합니다.
	    r.Out.Header.Set("X-Additional-Header", "header set by the proxy")
	  },
	}
```

<!-- CL 407375 -->
[`ReverseProxy`](/pkg/net/http/httputil/#ReverseProxy)는 이제 수신된 요청에 `User-Agent` 헤더가 없는 경우, 전달되는 요청에 해당 헤더를 추가하지 않습니다.

### 라이브러리의 소규모 변경 사항 {#minor_library_changes}

언제나 그렇듯이, Go 1의 [호환성 약속](/doc/go1compat)을 염두에 두고 라이브러리에 다양한 소규모 변경 및 업데이트가 이루어졌습니다.
또한, 여기에는 나열되지 않은 다양한 성능 개선 사항들이 포함되어 있습니다.

#### [archive/tar](/pkg/archive/tar/)

<!-- https://go.dev/issue/55356, CL 449937 -->
`GODEBUG=tarinsecurepath=0` 환경 변수가 설정된 경우,
[`Reader.Next`](/pkg/archive/tar/#Reader.Next) 메서드는
파일 이름이 절대 경로이거나, 현재 디렉터리 외부의 위치를 참조하거나, 유효하지 않은
문자를 포함하거나, (Windows의 경우) `NUL`과 같은 예약된 이름인 엔트리에 대해
[`ErrInsecurePath`](/pkg/archive/tar/#ErrInsecurePath) 에러를 반환합니다.
향후 Go 버전에서는 기본적으로 보안상 안전하지 않은 경로(insecure paths)가 비활성화될 수 있습니다.

<!-- archive/tar -->

#### [archive/zip](/pkg/archive/zip/)

<!-- https://go.dev/issue/55356 -->
`GODEBUG=zipinsecurepath=0` 환경 변수가 설정된 경우,
[`NewReader`](/pkg/archive/zip/#NewReader)는 이제 절대 경로인 파일 이름, 현재 디렉토리 외부의 위치를 참조하는 파일 이름, 유효하지 않은 문자가 포함된 파일 이름, 또는 (Windows의 경우) `NUL`과 같은 예약된 이름을 포함하는 아카이브를 열 때 [`ErrInsecurePath`](/pkg/archive/zip/#ErrInsecurePath) 에러를 반환합니다.
향후 Go 버전에서는 기본적으로 안전하지 않은 경로(insecure paths)가 비활성화될 수 있습니다.

<!-- CL 449955 -->
파일 데이터를 포함하고 있는 디렉터리 파일로부터 읽기를 시도하면 이제 에러가 반환됩니다.
zip 명세에서는 디렉터리 파일이 파일 데이터를 포함하는 것을 허용하지 않으므로, 이 변경 사항은 유효하지 않은 아카이브를 읽을 때만 영향을 미칩니다.

<!-- archive/zip -->

#### [bytes](/pkg/bytes/)

<!-- CL 407176 -->
새로운 [`CutPrefix`](/pkg/bytes/#CutPrefix) 및 [`CutSuffix`](/pkg/bytes/#CutSuffix) 함수는 [`TrimPrefix`](/pkg/bytes/#TrimPrefix) 및 [`TrimSuffix`](/pkg/bytes/#TrimSuffix)와 유사하지만, 문자열이 트리밍되었는지 여부도 함께 보고합니다.

<!-- CL 359675, https://go.dev/issue/45038 -->
새로운 [`Clone`](/pkg/bytes/#Clone) 함수는
바이트 슬라이스의 복사본을 할당합니다.

<!-- bytes -->

#### [context](/pkg/context/)

<!-- https://go.dev/issue/51365, CL 375977 -->
새로운 [`WithCancelCause`](/pkg/context/#WithCancelCause) 함수는
특정 에러와 함께 컨텍스트를 취소할 수 있는 방법을 제공합니다.
해당 에러는 새로운 [`Cause`](/pkg/context/#Cause) 함수를 호출하여 가져올 수 있습니다.

제공해주신 원문 내용이 없습니다. 번역할 Markdown 콘텐츠를 제공해 주시면, 요청하신 지침에 따라 기술적으로 정확하게 한국어로 번역해 드리겠습니다.

#### [crypto/ecdsa](/pkg/crypto/ecdsa/)

<!-- CL 353849 -->
지원되는 곡선을 사용할 때, 이제 모든 작업이 상수 시간(constant time)으로 구현됩니다.
이로 인해 CPU 시간이 5%에서 30% 사이로 증가했으며, 주로 P-384 및 P-521에 영향을 미칩니다.

<!-- https://go.dev/issue/56088, CL 450816 -->
새로운 [`PrivateKey.ECDH`](/pkg/crypto/ecdsa/#PrivateKey.ECDH) 메서드는 `ecdsa.PrivateKey`를 `ecdh.PrivateKey`로 변환합니다.

<!-- crypto/ecdsa -->

#### [crypto/ed25519](/pkg/crypto/ed25519/)

<!-- CL 373076, CL 404274, https://go.dev/issue/31804 -->
[`PrivateKey.Sign`](/pkg/crypto/ed25519/#PrivateKey.Sign) 메서드와
[`VerifyWithOptions`](/pkg/crypto/ed25519/#VerifyWithOptions) 함수가
이제 [`crypto.SHA512`](/pkg/crypto/#SHA512)를 반환하는
[`Options.HashFunc`](/pkg/crypto/ed25519/#Options.HashFunc)를 통해
Ed25519ph를 사용하여 미리 해싱된 메시지에 서명하는 것을 지원합니다.
또한, 새로운 [`Options.Context`](/pkg/crypto/ed25519/#Options.Context) 필드를 설정함으로써
Ed25519ctx 및 컨텍스트가 포함된 Ed25519ph도 지원합니다.

<!-- crypto/ed25519 -->

#### [crypto/rsa](/pkg/crypto/rsa/)

<!-- CL 418874, https://go.dev/issue/19974 -->
새로운 필드 [`OAEPOptions.MGFHash`](/pkg/crypto/rsa/#OAEPOptions.MGFHash)를 통해 OAEP 복호화를 위한 MGF1 해시를 별도로 설정할 수 있습니다.

<!-- https://go.dev/issue/20654 -->
`crypto/rsa`가 이제 더 안전한 새로운 상수 시간(constant-time) 백엔드를 사용합니다. 이로 인해 복호화 작업의 CPU 런타임이 약 15%(amd64의 RSA-2048)에서 45%(arm64의 RSA-4096) 사이로 증가하며, 32비트 아키텍처에서는 더 많이 증가합니다. 암호화 작업은 이전보다 약 20배 느려졌습니다(하지만 여전히 복호화보다 5~10배 빠릅니다). 성능은 향후 릴리스에서 개선될 예정입니다.

프로그램은 [`PrecomputedValues`](/pkg/crypto/rsa/#PrecomputedValues)의 필드를 수정하거나 수동으로 생성해서는 안 됩니다.

<!-- crypto/rsa -->

#### [crypto/subtle](/pkg/crypto/subtle/)

<!-- https://go.dev/issue/53021, CL 421435 -->
새로운 함수 [`XORBytes`](/pkg/crypto/subtle/#XORBytes)는
두 개의 바이트 슬라이스를 XOR 연산합니다.

<!-- crypto/subtle -->

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 426455, CL 427155, CL 426454, https://go.dev/issue/46035 -->
이제 파싱된 인증서가 해당 인증서를 활발하게 사용하는 모든 클라이언트 간에 공유됩니다.
인증서 체인의 일부를 공유하는 서버 또는 서버 집합에 대해 많은 동시 연결을 생성하는 프로그램의 경우 메모리 절감 효과가 상당할 수 있습니다.

<!-- https://go.dev/issue/48152, CL 449336 -->
인증서 검증 실패로 인한 핸드셰이크 실패 시, 이제 TLS 클라이언트와 서버는 제시된 인증서가 포함된 새로운 타입의 오류인 [`CertificateVerificationError`](/pkg/crypto/tls/#CertificateVerificationError)를 반환합니다.

<!-- crypto/tls -->

#### [crypto/x509](/pkg/crypto/x509/)

<!-- CL 450816, CL 450815 -->
[`ParsePKCS8PrivateKey`](/pkg/crypto/x509/#ParsePKCS8PrivateKey)
및
[`MarshalPKCS8PrivateKey`](/pkg/crypto/x509/#MarshalPKCS8PrivateKey)
가 이제 [`*crypto/ecdh.PrivateKey`](/pkg/crypto/ecdh.PrivateKey) 타입의 키를 지원합니다.
[`ParsePKIXPublicKey`](/pkg/crypto/x509/#ParsePKIXPublicKey)
및
[`MarshalPKIXPublicKey`](/pkg/crypto/x509/#MarshalPKIXPublicKey)
가 이제 [`*crypto/ecdh.PublicKey`](/pkg/crypto/ecdh.PublicKey) 타입의 키를 지원합니다.
NIST 커브 키를 파싱하면 여전히 `*ecdsa.PublicKey` 및 `*ecdsa.PrivateKey` 타입의 값이 반환됩니다.
새로 추가된 `ECDH` 메서드를 사용하여 `crypto/ecdh` 타입으로 변환하십시오.

<!-- CL 449235 -->
새로운 [`SetFallbackRoots`](/pkg/crypto/x509/#SetFallbackRoots) 함수를 사용하면, 런타임에 운영 체제 검증기(verifier)나 표준 플랫폼 루트 번들을 사용할 수 없는 경우를 대비해 프로그램에서 폴백(fallback) 루트 인증서 세트를 정의할 수 있습니다. 이 함수는 최신 루트 번들을 제공하는 새로운 패키지인 [golang.org/x/crypto/x509roots/fallback](/pkg/golang.org/x/crypto/x509roots/fallback)와 함께 가장 흔하게 사용될 것입니다.

<!-- crypto/x509 -->

#### [debug/elf](/pkg/debug/elf/)

<!-- CL 429601 -->
[`Section.Data`](/pkg/debug/elf/#Section.Data) 또는 [`Section.Open`](/pkg/debug/elf/#Section.Open)에서 반환한 리더를 사용하여 `SHT_NOBITS` 섹션으로부터 읽으려는 시도는 이제 에러를 반환합니다.

<!-- CL 420982 -->
LoongArch 시스템에서 사용하기 위한 추가 [`R_LARCH_*`](/pkg/debug/elf/#R_LARCH) 상수가 정의되어 있습니다.

<!-- CL 420982, CL 435415, CL 425555 -->
PPC64 ELFv2 재배치(relocation)에 사용하기 위한 추가적인 [`R_PPC64_*`](/pkg/debug/elf/#R_PPC64) 상수들이 정의되어 있습니다.

<!-- CL 411915 -->
[`R_PPC64_SECTOFF_LO_DS`](/pkg/debug/elf/#R_PPC64_SECTOFF_LO_DS)의 상수 값이 61에서 62로 수정되었습니다.

<!-- debug/elf -->

#### [debug/gosym](/pkg/debug/gosym/)

<!-- https://go.dev/issue/37762, CL 317917 -->
[Go의 심볼 명명 규칙](#linker) 변경으로 인해, Go 바이너리를 처리하는 도구는 Go 1.20의 `debug/gosym` 패키지를 사용하여 이전 버전과 새 버전의 바이너리를 모두 투명하게 처리해야 합니다.

<!-- debug/gosym -->

#### [debug/pe](/pkg/debug/pe/)

<!-- CL 421357 -->
RISC-V 시스템에서 사용할 수 있도록 추가적인 [`IMAGE_FILE_MACHINE_RISCV*`](/pkg/debug/pe/#IMAGE_FILE_MACHINE_RISCV128) 상수가 정의되어 있습니다.

<!-- debug/pe -->

#### [encoding/binary](/pkg/encoding/binary/)

<!-- CL 420274 -->
이제 [`ReadVarint`](/pkg/encoding/binary/#ReadVarint) 및
[`ReadUvarint`](/pkg/encoding/binary/#ReadUvarint)
함수는 부분적인 값을 읽은 후 `io.EOF` 대신 `io.ErrUnexpectedEOF`를 반환합니다.

<!-- encoding/binary -->

#### [encoding/xml](/pkg/encoding/xml/)

<!-- https://go.dev/issue/53346, CL 424777 -->
새로운 [`Encoder.Close`](/pkg/encoding/xml/#Encoder.Close) 메서드를 사용하여 인코딩이 완료되었을 때 닫히지 않은 요소가 있는지 확인할 수 있습니다.

<!-- CL 103875, CL 105636 -->
이제 디코더는 `<a:b:c>`와 같이 콜론이 두 개 이상 포함된 요소 및 속성 이름과, `xmlns:a=""`와 같이 빈 문자열로 해석되는 네임스페이스를 거부합니다.

<!-- CL 107255 -->
이제 디코더는 시작 태그와 종료 태그에서 서로 다른 네임스페이스 접두사(namespace prefix)를 사용하는 요소를 거부합니다. 이는 해당 접두사들이 모두 동일한 네임스페이스를 나타내는 경우에도 마찬가지입니다.

<!-- encoding/xml -->

#### [errors](/pkg/errors/)

<!-- https://go.dev/issue/53435 -->
새로운 [`Join`](/pkg/errors/#Join) 함수는 여러 에러 목록을 래핑한 에러를 반환합니다.

<!-- errors -->

#### [fmt](/pkg/fmt/)

<!-- https://go.dev/issue/53435 -->
[`Errorf`](/pkg/fmt/#Errorf) 함수는 `%w` 포맷 동사(format verb)의 중복 사용을 지원하며, `%w`에 전달된 모든 인자 목록으로 언랩(unwrap)되는 에러를 반환합니다.

<!-- https://go.dev/issue/51668, CL 400875 -->
새로운 [`FormatString`](/pkg/fmt/#FormatString) 함수는 [`State`](/pkg/fmt/#State)에 해당하는 포맷팅 지시어(formatting directive)를 복구하며, 이는 [`Formatter`](/pkg/fmt/#Formatter) 구현 시 유용하게 사용될 수 있습니다.

<!-- fmt -->

#### [go/ast](/pkg/go/ast/)

<!-- CL 426091, https://go.dev/issue/50429 -->
새로운 [`RangeStmt.Range`](/pkg/go/ast/#RangeStmt.Range) 필드는
range 문에서 `range` 키워드의 위치를 기록합니다.

<!-- CL 427955, https://go.dev/issue/53202 -->
새로운 [`File.FileStart`](/pkg/go/ast/#File.FileStart)
및 [`File.FileEnd`](/pkg/go/ast/#File.FileEnd) 필드는
전체 소스 파일의 시작과 끝 위치를 기록합니다.

<!-- go/ast -->

#### [go/token](/pkg/go/token/)

<!-- CL 410114, https://go.dev/issue/53200 -->
새로운 [`FileSet.RemoveFile`](/pkg/go/token/#FileSet.RemoveFile) 메서드는
`FileSet`에서 파일을 제거합니다.
장시간 실행되는 프로그램은 이 메서드를 사용하여 더 이상 필요하지 않은
파일과 관련된 메모리를 해제할 수 있습니다.

<!-- go/token -->

#### [go/types](/pkg/go/types/)

<!-- CL 454575 -->
새로운 [`Satisfies`](/pkg/go/types/#Satisfies) 함수는 타입이 제약 조건(constraint)을 충족하는지 여부를 보고합니다.
이 변경 사항은 제약 조건을 충족하는 것과 인터페이스를 구현하는 것을 구분하는 [새로운 언어 세맨틱](#language)과 일치합니다.

<!-- go/types -->

#### [html/template](/pkg/html/template/)

<!-- https://go.dev/issue/59153 -->
<!-- CL 481993 -->
Go 1.20.3 및 이후 버전부터
[ECMAScript 6 템플릿 리터럴 내의 액션을 허용하지 않습니다.](/pkg/html/template#hdr-Security_Model)
이 동작은 `GODEBUG=jstmpllitinterp=1` 설정을 통해 이전 상태로 되돌릴 수 있습니다.

<!-- html/template -->

#### [io](/pkg/io/)

<!-- https://go.dev/issue/45899, CL 406776 -->
새로운 [`OffsetWriter`](/pkg/io/#OffsetWriter)는 하위 [`WriterAt`](/pkg/io/#WriterAt)을 래핑하며, 고정된 양만큼 유효 파일 오프셋 위치를 조정하는 `Seek`, `Write`, `WriteAt` 메서드를 제공합니다.

<!-- io -->

#### [io/fs](/pkg/io/fs/)

<!-- CL 363814, https://go.dev/issue/47209 -->
새로운 에러 [`SkipAll`](/pkg/io/fs/#SkipAll)은
[`WalkDir`](/pkg/io/fs/#WalkDir)를
즉시 종료하지만 성공적으로 처리합니다.

<!-- io -->

#### [math/big](/pkg/math/big/)

<!-- https://go.dev/issue/52182 -->
[math/big](/pkg/math/big/) 패키지는 범위가 넓고 입력값에 따라 실행 시간이 달라지므로 암호화 구현에 적합하지 않습니다. 표준 라이브러리의 암호화 패키지들은 더 이상 공격자가 제어하는 입력값에 대해 복잡한 [Int](/pkg/math/big#Int) 메서드를 호출하지 않습니다. 향후 math/big의 버그가 보안 취약점으로 간주될지 여부는 표준 라이브러리에 미치는 전반적인 영향에 따라 결정될 것입니다.

<!-- math/big -->

#### [math/rand](/pkg/math/rand/)

<!-- https://go.dev/issue/54880, CL 436955, https://go.dev/issue/56319 -->
[math/rand](/pkg/math/rand/) 패키지가 이제 `Float64` 및 `Int`와 같은 최상위 함수에서 사용하는 전역 난수 생성기를 랜덤 값으로 자동으로 시드(seed)하며, 최상위 [`Seed`](/pkg/math/rand/#Seed) 함수는 deprecated 되었습니다.
재현 가능한 난수 시퀀스가 필요한 프로그램은 `rand.New(rand.NewSource(seed))`를 사용하여 자체적인 랜덤 소스를 할당하는 것이 좋습니다.

이전의 일관된 글로벌 시딩(global seeding) 동작이 필요한 프로그램은 환경 변수에 `GODEBUG=randautoseed=0`을 설정할 수 있습니다.

<!-- https://go.dev/issue/20661 -->
최상위 [`Read`](/pkg/math/rand/#Read) 함수는 더 이상 사용되지 않습니다(deprecated).
거의 모든 경우에 [`crypto/rand.Read`](/pkg/crypto/rand/#Read)를 사용하는 것이 더 적절합니다.

<!-- math/rand -->

#### [mime](/pkg/mime/)

<!-- https://go.dev/issue/48866 -->
[`ParseMediaType`](/pkg/mime/#ParseMediaType) 함수는 이제 파라미터 이름이 중복되더라도 해당 이름의 값들이 동일하다면 이를 허용합니다.

제공해주신 내용이 없습니다. 번역할 Markdown 콘텐츠를 입력해 주세요.

#### [mime/multipart](/pkg/mime/multipart/)

<!-- CL 431675 -->
[`Reader`](/pkg/mime/multipart/#Reader) 타입의 메서드들이 이제 기본 `io.Reader`에서 반환된 에러를 래핑(wrap)합니다.

<!-- https://go.dev/issue/59153 -->
<!-- CL 481985 -->
Go 1.19.8 버전부터 이 패키지는 악의적인 입력으로부터 보호하기 위해 처리하는 MIME 데이터의 크기에 제한을 둡니다.
`Reader.NextPart` 및 `Reader.NextRawPart`는 하나의 파트 내 헤더 수를 10,000개로 제한하며, `Reader.ReadForm`은 모든 `FileHeaders`의 총 헤더 수를 10,000개로 제한합니다.
이 제한들은 `GODEBUG=multipartmaxheaders` 설정을 통해 조정할 수 있습니다.
`Reader.ReadForm`은 추가적으로 폼 내 파트 수를 1,000개로 제한합니다.
이 제한은 `GODEBUG=multipartmaxparts` 설정을 통해 조정할 수 있습니다.

Please provide the content you would like me to translate. You only provided the MIME type comment `<!-- mime/multipart -->` without any actual text. 

Once you provide the Markdown content, I will translate it into Korean while preserving all technical structures, code, and identifiers as requested.

#### [net](/pkg/net/)

<!-- https://go.dev/issue/50101, CL 446179 -->
[`LookupCNAME`](/pkg/net/#LookupCNAME) 함수가 이제 `CNAME` 레코드가 존재할 때 해당 내용을 일관되게 반환합니다. 이전에는 Unix 시스템에서 순수 Go resolver를 사용할 때, `CNAME` 레코드가 `A`, `AAAA` 또는 `CNAME` 레코드가 없는 이름을 참조하는 경우 `LookupCNAME`이 에러를 반환했습니다. 이번 변경을 통해 `LookupCNAME`이 Windows에서의 이전 동작과 일치하도록 수정되었으며, 이제 `CNAME`이 존재하기만 하면 `LookupCNAME`이 성공적으로 값을 반환합니다.

<!-- https://go.dev/issue/53482, CL 413454 -->
[`Interface.Flags`](/pkg/net/#Interface.Flags)에 운영상 활성화된 인터페이스를 나타내는 새로운 플래그인 `FlagRunning`이 추가되었습니다. 관리적으로 설정되었으나 활성화되지 않은 인터페이스(예: 네트워크 케이블이 연결되지 않은 경우)는 `FlagUp`은 설정되어 있지만 `FlagRunning`은 설정되지 않습니다.

<!-- https://go.dev/issue/55301, CL 444955 -->
새로운 [`Dialer.ControlContext`](/pkg/net/#Dialer.ControlContext) 필드는 기존의 [`Dialer.Control`](/pkg/net/#Dialer.Control) 훅과 유사하지만, 추가적으로 dial 컨텍스트를 파라미터로 받는 콜백 함수를 포함합니다.
`ControlContext`가 nil이 아닌 경우 `Control`은 무시됩니다.

<!-- CL 428955 -->
Go DNS 리졸버가 `trust-ad` 리졸버 옵션을 인식합니다.
`resolv.conf`에 `options trust-ad`가 설정되어 있으면,
Go 리졸버는 DNS 쿼리의 AD 비트를 설정합니다. 리졸버는
응답의 AD 비트를 사용하지 않습니다.

<!-- CL 448075 -->
DNS resolution은 `/etc/nsswitch.conf` 파일의 변경 사항을 감지하며, 파일이 변경되면 이를 다시 로드합니다. 확인 작업은 최대 5초마다 한 번씩 수행되며, 이는 `/etc/hosts` 및 `/etc/resolv.conf`의 이전 처리 방식과 일치합니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- https://go.dev/issue/51914 -->
이제 [`ResponseWriter.WriteHeader`](/pkg/net/http/#ResponseWriter.WriteHeader) 함수에서 `1xx` 상태 코드를 전송하는 것을 지원합니다.

<!-- https://go.dev/issue/41773, CL 356410 -->
새로운 [`Server.DisableGeneralOptionsHandler`](/pkg/net/http/#Server.DisableGeneralOptionsHandler) 설정 항목을 통해
기본 `OPTIONS *` 핸들러를 비활성화할 수 있습니다.

<!-- https://go.dev/issue/54299, CL 447216 -->
새로운 [`Transport.OnProxyConnectResponse`](/pkg/net/http/#Transport.OnProxyConnectResponse) 훅은 `Transport`가 `CONNECT` 요청에 대해 프록시로부터 HTTP 응답을 받았을 때 호출됩니다.

<!-- https://go.dev/issue/53960, CL 418614  -->
이제 HTTP 서버는 본문(body)이 포함된 HEAD 요청을 잘못된 요청으로 거부하는 대신 수락합니다.

<!-- https://go.dev/issue/53896 -->
`net/http` 함수에서 반환되는 HTTP/2 스트림 오류는 [`errors.As`](/pkg/errors/#As)를 사용하여 [`golang.org/x/net/http2.StreamError`](/pkg/golang.org/x/net/http2/#StreamError)로 변환될 수 있습니다.

<!-- https://go.dev/cl/397734 -->
쿠키 이름의 앞뒤 공백은 더 이상 유효하지 않은 것으로 거부되지 않고 제거(trim)됩니다.
예를 들어, "name =value"라는 쿠키 설정은 이제 쿠키 "name"을 설정하는 것으로 허용됩니다.

<!-- https://go.dev/issue/52989 -->
이제 Expires 필드가 비어 있는 [`Cookie`](/pkg/net/http#Cookie)는 유효한 것으로 간주됩니다.
[`Cookie.Valid`](/pkg/net/http#Cookie.Valid)는 Expires가 설정되어 있을 때만 이를 확인합니다.

<!-- net/http -->

#### [net/netip](/pkg/net/netip/)

<!-- https://go.dev/issue/51766, https://go.dev/issue/51777, CL 412475 -->
새로운 [`IPv6LinkLocalAllRouters`](/pkg/net/netip/#IPv6LinkLocalAllRouters)
및 [`IPv6Loopback`](/pkg/net/netip/#IPv6Loopback) 함수는
[`net.IPv6loopback`](/pkg/net/#IPv6loopback) 및
[`net.IPv6linklocalallrouters`](/pkg/net/#IPv6linklocalallrouters)에 대응하는
`net/netip` 패키지의 버전입니다.

<!-- net/netip -->

#### [os](/pkg/os/)

<!-- CL 448897 -->
Windows에서 `NUL`이라는 이름은 더 이상 [`Mkdir`](/pkg/os/#Mkdir) 및 [`Stat`](/pkg/os/#Stat)에서 특수한 경우로 처리되지 않습니다.

<!-- https://go.dev/issue/52747, CL 405275 -->
Windows에서 [`File.Stat`](/pkg/os/#File.Stat)이 이제 파일이 디렉터리인 경우 파일 핸들을 사용하여 속성을 가져옵니다.
이전에는 [`Open`](/pkg/os/#Open)에 전달된 경로를 사용했는데, 파일이 이동되었거나 교체된 경우 해당 경로가 더 이상 파일 핸들이 나타내는 파일이 아닐 수 있었습니다.
이 변경 사항은 `Open`이 일반 파일의 동작과 일치하도록 `FILE_SHARE_DELETE` 액세스 권한 없이 디렉터리를 열도록 수정합니다.

<!-- https://go.dev/issue/36019, CL 405275 -->
Windows에서 [`File.Seek`](/pkg/os/#File.Seek)가 이제 디렉터리의 시작 부분으로 이동(seek)하는 것을 지원합니다.

<!-- os -->

#### [os/exec](/pkg/os/exec/)

<!-- https://go.dev/issue/50436, CL 401835 -->
새로운 [`Cmd`](/pkg/os/exec/#Cmd) 필드인
[`Cancel`](/pkg/os/exec/#Cmd.Cancel)과
[`WaitDelay`](/pkg/os/exec/#Cmd.WaitDelay)는
연결된 `Context`가 취소되거나, 자식 프로세스가 I/O 파이프를 여전히 열어둔 상태에서 프로세스가 종료되었을 때의 `Cmd` 동작을 지정합니다.

<!-- os/exec -->

#### [path/filepath](/pkg/path/filepath/)

<!-- CL 363814, https://go.dev/issue/47209 -->
새로운 에러 [`SkipAll`](/pkg/path/filepath/#SkipAll)은
[`Walk`](/pkg/path/filepath/#Walk)를
즉시 종료하지만 성공적으로 처리합니다.

<!-- https://go.dev/issue/56219, CL 449239 -->
새로운 [`IsLocal`](/pkg/path/filepath/#IsLocal) 함수는 경로가 특정 디렉토리에 대해 어휘적으로(lexically) 로컬인지 여부를 보고합니다.
예를 들어, `IsLocal(p)`가 `true`라면, `Open(p)`는 현재 디렉토리를 루트로 하는 하위 트리 내에 어휘적으로 존재하는 파일을 참조하게 됩니다.

<!-- io -->

#### [reflect](/pkg/reflect/)

<!-- https://go.dev/issue/46746, CL 423794 -->
새로운 [`Value.Comparable`](/pkg/reflect/#Value.Comparable) 및
[`Value.Equal`](/pkg/reflect/#Value.Equal) 메서드를 사용하여 두 `Value`의 동등성을 비교할 수 있습니다.
`Comparable`은 주어진 `Value` 리시버에 대해 `Equal`이 유효한 작업인지 여부를 보고합니다.

<!-- https://go.dev/issue/48000, CL 389635 -->
새로운 [`Value.Grow`](/pkg/reflect/#Value.Grow) 메서드는
슬라이스를 확장하여 추가로 `n`개의 요소를 위한 공간을 보장합니다.

<!-- https://go.dev/issue/52376, CL 411476 -->
새로운 [`Value.SetZero`](/pkg/reflect/#Value.SetZero) 메서드는
값을 해당 타입의 제로 값(zero value)으로 설정합니다.

<!-- CL 425184 -->
Go 1.18에서 [`Value.SetIterKey`](/pkg/reflect/#Value.SetIterKey)와 [`Value.SetIterValue`](/pkg/reflect/#Value.SetIterValue) 메서드가 도입되었습니다.
이는 최적화를 위한 것이며, `v.SetIterKey(it)`는 `v.Set(it.Key())`와 동일하게 동작하도록 설계되었습니다.
기존 구현에서는 최적화되지 않은 형태에 포함되어 있던 비공개 필드(unexported fields) 사용 여부에 대한 확인 절차가 누락되어 있었습니다.
Go 1.20에서는 해당 메서드들이 비공개 필드 확인 절차를 포함하도록 수정되었습니다.

<!-- reflect -->

#### [regexp](/pkg/regexp/)

<!-- CL 444817 -->
Go 1.19.2 및 Go 1.18.7에는 정규 표현식 파서에 대한 보안 수정 사항이 포함되어, 너무 많은 메모리를 소비하는 매우 큰 표현식을 거부하도록 개선되었습니다.
Go 패치 릴리스는 새로운 API를 도입하지 않으므로, 이 경우 파서는 [`syntax.ErrInternalError`](/pkg/regexp/syntax/#ErrInternalError)를 반환했습니다.
Go 1.20에서는 더 구체적인 오류인 [`syntax.ErrLarge`](/pkg/regexp/syntax/#ErrLarge)가 추가되었으며, 이제 파서는 대신 이 오류를 반환합니다.

<!-- regexp -->

#### [runtime/cgo](/pkg/runtime/cgo/)

<!-- https://go.dev/issue/46731, CL 421879 -->
Go 1.20에 새로운 [`Incomplete`](/pkg/runtime/cgo/#Incomplete) 마커 타입이 추가되었습니다.
cgo에 의해 생성된 코드는 불완전한 C 타입을 표시하기 위해 `cgo.Incomplete`를 사용합니다.

<!-- runtime/cgo -->

#### [runtime/metrics](/pkg/runtime/metrics/)

<!-- https://go.dev/issue/47216, https://go.dev/issue/49881 -->
Go 1.20에서는 현재 `GOMAXPROCS` 설정(` /sched/gomaxprocs:threads`), 실행된 cgo 호출 횟수(`/cgo/go-to-c-calls:calls`), 총 뮤텍스 블록 시간(`/sync/mutex/wait/total:seconds`), 그리고 가비지 컬렉션에 소요된 시간의 다양한 측정 항목을 포함하여 새로운 [지원되는 메트릭](/pkg/runtime/metrics/#hdr-Supported_metrics)이 추가되었습니다.

<!-- CL 427615 -->
시간 기반 히스토그램 메트릭의 정밀도가 낮아졌지만, 메모리 사용량은 훨씬 줄어들었습니다.

<!-- runtime/metrics -->

#### [runtime/pprof](/pkg/runtime/pprof/)

<!-- CL 443056 -->
이제 Mutex 프로필 샘플이 미리 스케일링(pre-scaled)되어, 실행 중에 샘플링 속도가 변경될 경우 이전의 mutex 프로필 샘플이 잘못 스케일링되던 문제가 수정되었습니다.

<!-- CL 416975 -->
Windows에서 수집된 프로파일에 이제 메모리 매핑 정보가 포함되어, 위치 독립적(position-independent) 바이너리의 심볼화(symbolization) 문제를 해결합니다.

<!-- runtime/pprof -->

#### [runtime/trace](/pkg/runtime/trace/)

<!-- CL 447135, https://go.dev/issue/55022 -->
가비지 컬렉터의 백그라운드 스위퍼(background sweeper)가 이제 더 적게 양보(yield)하며, 그 결과 실행 트레이스(execution traces)에서 불필요한 이벤트가 훨씬 더 적게 발생합니다.

<!-- runtime/trace -->

#### [strings](/pkg/strings/)

<!-- CL 407176, https://go.dev/issue/42537 -->
새로운 [`CutPrefix`](/pkg/strings/#CutPrefix) 및 [`CutSuffix`](/pkg/strings/#CutSuffix) 함수는 [`TrimPrefix`](/pkg/strings/#TrimPrefix) 및 [`TrimSuffix`](/pkg/strings/#TrimSuffix)와 유사하지만, 문자열이 트리밍되었는지 여부도 함께 보고합니다.

<!-- strings -->

#### [sync](/pkg/sync/)

<!-- CL 399094, https://go.dev/issue/51972 -->
새로운 [`Map`](/pkg/sync/#Map) 메서드인 [`Swap`](/pkg/sync/#Map.Swap),
[`CompareAndSwap`](/pkg/sync/#Map.CompareAndSwap), 그리고
[`CompareAndDelete`](/pkg/sync/#Map.CompareAndDelete)를 통해
기존 맵 항목을 원자적으로(atomically) 업데이트할 수 있습니다.

<!-- sync -->

#### [syscall](/pkg/syscall/)

<!-- CL 411596 -->
FreeBSD에서 FreeBSD 11 및 그 이전 버전에 필요했던 호환성 심(compatibility shims)이 제거되었습니다.

<!-- CL 407574 -->
Linux에서는 [`SysProcAttr.Cloneflags`](/pkg/syscall/#SysProcAttr.Cloneflags) 필드와 함께 사용할 수 있도록 추가적인 [`CLONE_*`](/pkg/syscall/#CLONE_CLEAR_SIGHAND) 상수가 정의되어 있습니다.

<!-- CL 417695 -->
Linux에서 새로운 [`SysProcAttr.CgroupFD`](/pkg/syscall/#SysProcAttr.CgroupFD) 및 [`SysProcAttr.UseCgroupFD`](/pkg/syscall/#SysProcAttr.UseCgroupFD) 필드는 자식 프로세스를 특정 cgroup에 배치하는 방법을 제공합니다.

<!-- syscall -->

#### [testing](/pkg/testing/)

<!-- https://go.dev/issue/43620, CL 420254 -->
새로운 메서드 [`B.Elapsed`](/pkg/testing/#B.Elapsed)는 벤치마크의 현재 경과 시간을 보고하며, 이는 `ReportMetric`과 함께 보고할 비율을 계산할 때 유용할 수 있습니다.

<!-- https://go.dev/issue/48515, CL 352349 -->
[`T.Cleanup`](/pkg/testing/#T.Cleanup)에 전달된 함수에서
[`T.Run`](/pkg/testing/#T.Run)을 호출하는 것은
그동안 명확하게 정의되지 않았으며, 이제는 panic이 발생합니다.

<!-- testing -->

#### [time](/pkg/time/)

<!-- https://go.dev/issue/52746, CL 412495 -->
새로운 시간 레이아웃 상수인 [`DateTime`](/pkg/time/#DateTime),
[`DateOnly`](/pkg/time/#DateOnly), 그리고
[`TimeOnly`](/pkg/time/#TimeOnly)는
공개된 Go 소스 코드 조사에서 가장 흔히 사용되는 세 가지 레이아웃 문자열에 대한 이름을 제공합니다.

<!-- CL 382734, https://go.dev/issue/50770 -->
새로운 [`Time.Compare`](/pkg/time/#Time.Compare) 메서드는
두 시간을 비교합니다.

<!-- CL 425037 -->
[`Parse`](/pkg/time/#Parse)는 이제 입력값의 서브 나노초(sub-nanosecond) 정밀도를 오류로 보고하는 대신 무시합니다.

<!-- CL 444277 -->
[`Time.MarshalJSON`](/pkg/time/#Time.MarshalJSON) 메서드가
이제 RFC 3339 준수 여부를 더 엄격하게 검사합니다.

<!-- time -->

#### [unicode/utf16](/pkg/unicode/utf16/)

<!-- https://go.dev/issue/51896, CL 409054 -->
새로운 [`AppendRune`](/pkg/unicode/utf16/#AppendRune)
함수는 주어진 rune의 UTF-16 인코딩을 uint16 슬라이스에 추가하며,
이는 [`utf8.AppendRune`](/pkg/unicode/utf8/#AppendRune)과 유사합니다.

<!-- unicode/utf16 -->

<!-- Silence false positives from x/build/cmd/relnote: -->
<!-- https://go.dev/issue/45964 was documented in Go 1.18 release notes but closed recently -->
<!-- https://go.dev/issue/52114 is an accepted proposal to add golang.org/x/net/http2.Transport.DialTLSContext; it's not a part of the Go release -->
<!-- CL 431335: cmd/api: make check pickier about api/*.txt -->
<!-- CL 447896 api: add newline to 55301.txt; modified api/next/55301.txt -->
<!-- CL 449215 api/next/54299: add missing newline; modified api/next/54299.txt -->
<!-- CL 433057 cmd: update vendored golang.org/x/tools for multiple error wrapping -->
<!-- CL 423362 crypto/internal/boring: update to newer boringcrypto, add arm64 -->
<!-- https://go.dev/issue/53481 x/cryptobyte ReadUint64, AddUint64 -->
<!-- https://go.dev/issue/51994 x/crypto/ssh -->
<!-- https://go.dev/issue/55358 x/exp/slices -->
<!-- https://go.dev/issue/54714 x/sys/unix -->
<!-- https://go.dev/issue/50035 https://go.dev/issue/54237 x/time/rate -->
<!-- CL 345488 strconv optimization -->
<!-- CL 428757 reflect deprecation, rolled back -->
<!-- https://go.dev/issue/49390 compile -l -N is fully supported -->
<!-- https://go.dev/issue/54619 x/tools -->
<!-- CL 448898 reverted -->
<!-- https://go.dev/issue/54850 x/net/http2 Transport.MaxReadFrameSize -->
<!-- https://go.dev/issue/56054 x/net/http2 SETTINGS_HEADER_TABLE_SIZE -->
<!-- CL 450375 reverted -->
<!-- CL 453259 tracking deprecations in api -->
<!-- CL 453260 tracking darwin port in api -->
<!-- CL 453615 fix deprecation comment in archive/tar -->
<!-- CL 453616 fix deprecation comment in archive/zip -->
<!-- CL 453617 fix deprecation comment in encoding/csv -->
<!-- https://go.dev/issue/54661 x/tools/go/analysis -->
<!-- CL 423359, https://go.dev/issue/51317 arena -->
