<!--
참고: 이 문서 및 이 디렉토리의 다른 문서에서, 고정 폭 문자열과 고정 폭이 아닌 공백을 함께 사용하는 규칙을 따릅니다. 예를 들어, `hello world`와 같이 사용합니다.
이러한 문자열에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.20 소개 {#introduction}

이 문서는 Go 1.20 버전의 주요 기능과 변경 사항을 소개합니다.

가장 최신 Go 버전인 1.20은 [Go 1.19](/doc/go1.19) 이후 6개월 만에 출시되었습니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
항상 그렇듯이, 이번 버전은 Go 1의 [호환성 보장](/doc/go1compat)을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일 및 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

Go 1.20 버전에는 4가지 언어 변경 사항이 포함되어 있습니다.

<!-- https://go.dev/issue/46505 -->
Go 1.17에서 `[conversions from slice to an array pointer](/ref/spec#Conversions_from_slice_to_array_or_array_pointer)` 기능이 추가되었습니다.
Go 1.20에서는 이를 확장하여 슬라이스에서 배열로의 변환을 허용합니다:
슬라이스 `x`가 주어졌을 때, `[4]byte(x)`를 이제 사용할 수 있으며,
`*(*[4]byte)(x)` 대신 사용할 수 있습니다.

<!-- https://go.dev/issue/53003 -->
`unsafe` 패키지 (`/ref/spec/#Package_unsafe`)는
새로운 함수 `SliceData`, `String`, `StringData`를 정의합니다.
Go 1.17의 `Slice`와 함께, 이러한 함수는 슬라이스와 문자열 값을 생성하고 파괴하는 완전한 기능을 제공하며, 정확한 표현에 의존하지 않습니다.

<!-- https://go.dev/issue/8606 -->
이제 사양은 구조체 값을 개별 필드를 기준으로 비교하도록 정의하고 있습니다.
필드를 구조체 타입 정의에 나타나는 순서대로 고려하며, 첫 번째 불일치 시 중지합니다.
이전 사양은 다음과 같이 해석될 수 있었습니다:
모든 필드를 첫 번째 불일치 이후에도 비교해야 합니다.
마찬가지로, 사양은 이제 배열 값을 개별 요소 기준으로, 증가하는 인덱스 순서대로 비교하도록 정의합니다.
두 경우 모두, 이러한 차이는 특정 비교가 패닉을 발생시켜야 하는지 여부에 영향을 미칩니다.
기존 프로그램은 변경되지 않았습니다: 새로운 사양의 문구는 구현이 항상 수행해 온 내용을 설명합니다.

<!-- https://go.dev/issue/56548 -->
[비교 가능한 타입](/ref/spec#Comparison_operators) (예: 일반 인터페이스)
이제 `comparable` 제약 조건을 만족할 수 있으며, 타입 인수가 엄격하게 비교되지 않아도 됩니다 (비교는 런타임에 패닉을 발생시킬 수 있습니다).
이렇게 하면 `comparable` 제약 조건으로 제한된 타입 파라미터를 인스턴스화할 수 있습니다 (예: 사용자 정의 일반 맵 키의 타입 파라미터).
인터페이스 타입 또는 인터페이스 타입을 포함하는 복합 타입과 같이 엄격하게 비교되지 않는 타입 인수를 사용할 수 있습니다.

## 포트

### Windows
```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, Windows!")
}
```

<!-- https://go.dev/issue/57003, https://go.dev/issue/57004 -->
Go 1.20은 Windows 7, 8, Server 2008 및 Server 2012의 모든 버전에 실행할 수 있는 마지막 릴리스입니다.
Go 1.21은 최소 Windows 10 또는 Server 2016을 필요로 합니다.

### 다윈 및 iOS {#darwin}

<!-- https://go.dev/issue/23011 -->
Go 1.20은 macOS 10.13 High Sierra 또는 10.14 Mojave에서 실행되는 마지막 버전입니다.
Go 1.21은 macOS 10.15 Catalina 또는 이후 버전이 필요합니다.

### FreeBSD/RISC-V {#freebsd-riscv}

<!-- https://go.dev/issue/53466 -->
Go 1.20은 RISC-V에서 FreeBSD를 위한 실험적인 지원을 추가합니다 (`GOOS=freebsd`, `GOARCH=riscv64`).

## 도구 {#tools}

### Go 명령어 {#go-command}

<!-- CL 432535, https://go.dev/issue/47257 -->
`$GOROOT/pkg` 디렉터리에는 더 이상 표준 라이브러리의 사전 컴파일된 패키지 아카이브가 저장되지 않습니다.
`go install` 명령어가 더 이상 이를 작성하지 않고,
`go build` 명령어가 더 이상 이를 확인하지 않으며,
Go 배포판에서 더 이상 이를 포함하지 않습니다.
대신, 표준 라이브러리의 패키지는 필요할 때 빌드되고, 빌드 캐시에 캐시됩니다. 이는 `GOROOT` 외부의 패키지와 동일한 방식으로 작동합니다.
이 변경 사항은 Go 배포판의 크기를 줄이고, `cgo`를 사용하는 패키지에 대한 C 툴체인 불일치를 방지합니다.

<!-- CL 448357: cmd/go: print test2json 시작 이벤트 -->
`go` `test` `-json` 기능의 구현이 개선되어 더욱 강력하게 작동하도록 했습니다.
`go` `test` `-json`을 실행하는 프로그램은 별도의 업데이트가 필요 없습니다.
직접 `go` `tool` `test2json`을 호출하는 프로그램은 이제 `-v=test2json` 옵션으로 테스트 바이너리를 실행해야 합니다.
(예: `go` `test` `-v=test2json`
또는 `./pkg.test` `-test.v=test2json`)
일반적인 `-v` 옵션을 사용하는 대신.

<!-- CL 448357: cmd/go: test2json 실행 이벤트 출력 -->
`go` `test` `-json`과 관련된 변경 사항은 각 테스트 프로그램 실행의 시작 시 `Action`을 `start`로 설정하는 이벤트 추가입니다.
`go` 명령어를 사용하여 여러 테스트를 실행할 때, 이러한 시작 이벤트는 명령줄에 지정된 패키지 순서대로 발생하는 것을 보장합니다.

<!-- https://go.dev/issue/45454, CL 421434 -->
`go` 명령은 이제 `amd64.v2`와 같은 아키텍처 기능 빌드 태그를 정의하여 특정 아키텍처 기능의 존재 여부에 따라 패키지 구현 파일 선택을 가능하게 합니다.
자세한 내용은 [`go` `help` `buildconstraint`](/cmd/go#hdr-Build_constraints)를 참조하십시오.

<!-- https://go.dev/issue/50332 -->
`go` 서브 명령은 이제
`-C` `<dir>` 옵션을 사용하여 `<dir>` 디렉토리를 변경할 수 있습니다.
이 옵션을 사용하면 명령을 실행하기 전에 디렉토리를 변경할 수 있으며, 이는 여러 모듈에서 명령을 실행해야 하는 스크립트에 유용할 수 있습니다.

<!-- https://go.dev/issue/41696, CL 416094 -->
`go build` 및 `go test` 명령어는 이제 `-i` 플래그를 더 이상 허용하지 않습니다. 이 플래그는 Go 1.16부터 [폐지되었습니다](/issue/41696).

<!-- https://go.dev/issue/38687, CL 421440 -->
`go` `generate` 명령은 이제
`-skip` `<패턴>` 옵션을 사용하여, `<패턴>`과 일치하는 `//go:generate` 지시문을 건너뛸 수 있습니다.

<!-- https://go.dev/issue/41583 -->
`go test` 명령은 이제
`-skip <패턴>` 옵션을 사용하여 `<패턴>`과 일치하는 테스트, 서브테스트 또는 예제를 건너뛸 수 있습니다.

<!-- https://go.dev/issue/37015 -->
`GOPATH/src` 내에 있는 메인 모듈의 경우,
`go install` 명령은 `GOPATH/pkg`로
메인 모듈이 아닌 패키지의 라이브러리를 설치하지
않고, `go list` 명령은 이러한 패키지에 대한
`Target` 필드를 더 이상 보고하지 않습니다. (모듈 모드에서는 컴파일된 패키지가
[빌드 캐시](https://pkg.go.dev/cmd/go#hdr-Build_and_test_caching)에만
저장되지만, [버그](/issue/37015)로 인해
`GOPATH` 설치 대상이 예상치 않게 유지되었습니다.)

<!-- https://go.dev/issue/55022 -->
`go build`, `go install` 및 기타 빌드 관련 명령은 이제 `-pgo` 플래그를 지원하여 프로파일 가이던 최적화를 활성화합니다. 자세한 내용은 아래 "[컴파일러](#compiler)" 섹션에서 설명합니다.
`-pgo` 플래그는 프로파일 파일의 경로를 지정합니다.
`-pgo=auto`를 지정하면 `go` 명령이 메인 패키지의 디렉터리에서 `default.pgo`라는 이름의 파일을 검색하고, 존재하면 이를 사용합니다.
현재 이 모드는 명령 줄에서 단일 메인 패키지를 지정해야 하지만, 향후 릴리스에서 이 제한을 해제할 계획입니다.
`-pgo=off`를 지정하면 프로파일 가이던 최적화를 비활성화합니다.

<!-- https://go.dev/issue/51430 -->
`go build`, `go install` 및 기타 빌드 관련 명령은 이제 `-cover` 플래그를 지원하여 지정된 타겟을 코드 커버리지 측정 장비와 함께 빌드합니다.
자세한 내용은 아래 [Cover](#cover) 섹션에서 확인하십시오.

#### `go` 버전 {#go-version}

<!-- https://go.dev/issue/48187 -->
`go` `version` `-m` 명령어는 이제 더 많은 종류의 Go 바이너리를 읽을 수 있으며, 특히 `go` `build` `-buildmode=c-shared`로 빌드된 Windows DLL과 실행 권한이 없는 Linux 바이너리를 지원합니다.

### Cgo {#cgo}

<!-- CL 450739 -->
`go` 명령은 C 도구 체인이 없는 시스템에서는 기본적으로 `cgo`를 비활성화합니다.
더 구체적으로, `CGO_ENABLED` 환경 변수가 설정되지 않았을 때,
`CC` 환경 변수가 설정되지 않았을 때,
그리고 기본 C 컴파일러(일반적으로 `clang` 또는 `gcc`)가 경로에 없는 경우,
`CGO_ENABLED`는 기본적으로 `0`으로 설정됩니다.
항상처럼, `CGO_ENABLED`를 명시적으로 설정하여 기본 설정을 덮어쓸 수 있습니다.

가장 중요한 효과는 Go가 C 컴파일러가 없는 시스템에 설치될 때, 표준 라이브러리의 cgo를 사용하는 패키지에 대해, 미리 배포된 패키지 아카이브를 사용하는 대신 순수 Go 빌드를 사용한다는 것입니다. (이것은 [위에 언급된](#go-command) 내용과 동일).
이렇게 하면 Go가 최소 컨테이너 환경 및 macOS와 같은 환경에서 더 잘 작동합니다. Go 1.16 이후에는 cgo 기반 패키지에 대해 미리 배포된 패키지 아카이브를 사용하지 않았습니다.

표준 라이브러리에 포함된 `cgo`를 사용하는 패키지는 [`net`](/pkg/net/),
[`os/user`](/pkg/os/user/), 그리고
[`plugin`](/pkg/plugin/)입니다.

macOS에서는 `net` 및 `os/user` 패키지는 `cgo` 사용을 중단하고 재작성되었습니다.
`cgo` 및 비-`cgo` 빌드, 그리고 교차 컴파일 빌드 모두에 동일한 코드가 사용됩니다.

Windows에서는 `net` 및 `os/user` 패키지는 `cgo`를 사용하지 않았습니다.

다른 시스템에서는 `cgo`를 비활성화한 빌드에서 이러한 패키지의 순수 Go 버전이 사용됩니다.

따라서, macOS에서 `net` 패키지를 사용하는 Go 코드가 `-buildmode=c-archive`로 빌드되면, 생성된 아카이브를 C 프로그램에 링크하려면 C 코드를 링크할 때 `-lresolv`를 지정해야 합니다.

macOS에서는 race detector가 cgo를 사용하지 않도록 다시 작성되었습니다:
`race-detector-enabled` 프로그램은 Xcode 없이 빌드 및 실행할 수 있습니다.
Linux 및 기타 Unix 시스템, 그리고 Windows에서는 race detector를 사용하려면 호스트 C 툴체인이 필요합니다.

### 표지 {#cover}

<!-- CL 436236, CL 401236, CL 438503 -->
Go 1.20 버전은 애플리케이션 및 통합 테스트를 포함하여 프로그램의 코드 커버리지 프로필을 수집할 수 있도록 지원합니다 (단, 유닛 테스트만 지원하지 않습니다).

프로그램에 대한 커버리지 데이터를 수집하려면, `go`로 빌드합니다.
`build` 명령의 `-cover` 플래그를 사용하고, 그 결과로 생성된
실행 파일을 `GOCOVERDIR` 환경 변수를 설정하여 커버리지 프로필을 저장하는
출력 디렉토리로 실행합니다.
자세한 내용은 ['통합 테스트용 커버리지' 랜딩 페이지](/doc/build-cover)를 참조하세요.
설계 및 구현에 대한 자세한 내용은 [제안](/issue/51430)을 참조하세요.

### 수의사 {#vet}

#### 중첩 함수에 의한 루프 변수 캡처 감지 개선 {#vet-loopclosure}

<!-- CL 447256, https://go.dev/issue/55972: 병렬 서브테스트에 대한 루프 닫기 분석 확장 -->
`vet` 도구가 이제 `[T.Parallel()`](/pkg/testing/#T.Parallel) 호출 후 서브테스트 함수 본체 내에서 루프 변수에 대한 참조를 보고합니다. 이러한 참조는 변수의 값을 다른 반복에서 관찰할 수 있으며(일반적으로 테스트 케이스가 건너뛰게 됨) 또는 비동기 액세스 불일치로 인해 잘못된 상태를 초래할 수 있습니다.

<!-- CL 452615 -->
또한, 이 도구는 더 많은 곳에서 참조 오류를 감지합니다. 이전에는 이 도구는 루프 본문의 마지막 문만 고려했지만, 이제는 `if`, `switch`, `select` 문 내의 마지막 문을 재귀적으로 검사합니다.

#### 잘못된 시간 형식에 대한 새로운 진단 {#vet-timeformat}

<!-- CL 354010, https://go.dev/issue/48801: 2006-02-01 형식의 시간 구성을 확인 -->
동물 건강 관리 도구가 이제 2006-02-01 (yyyy-dd-mm) 형식의 시간 구성을 보고합니다.
`Time.Format` 및 `time.Parse`를 사용하여.
이 형식은 일반적인 날짜 표준에는 나타나지 않지만, ISO 8601 날짜 형식 (yyyy-mm-dd)을 사용하려고 할 때 자주 실수로 사용됩니다.

## 런타임 {#runtime}

<!-- CL 422634 -->
가비지 컬렉터의 일부 내부 데이터 구조가 재구성되어 공간 및 CPU 효율성을 향상시켰습니다.
이 변경은 메모리 오버헤드를 줄이고 전반적인 CPU 성능을 최대 2% 향상시킵니다.

<!-- CL 417558, https://go.dev/issue/53892 -->
가비지 컬렉터는 특정 상황에서 고루틴에 대한 지원에 대해 덜 불안정하게 동작합니다.

<!-- https://go.dev/issue/51430 -->
Go 1.20에서 `runtime/coverage` 패키지가 추가되었으며, 이는 실행 시간에 장시간 실행되거나 서버 프로그램에서 커버리지 프로파일 데이터를 기록하기 위한 API를 제공합니다. 이러한 프로그램은 `os.Exit()`를 통해 종료되지 않습니다.

## 컴파일러

<!-- https://go.dev/issue/55022 -->
Go 1.20은 프로파일 기반 최적화 (PGO)에 대한 미리보기 지원을 추가합니다.
PGO는 런타임 프로파일 정보를 기반으로 애플리케이션 및 워크로드별 최적화를 수행할 수 있도록 도구 체인에 기능을 제공합니다.
현재 컴파일러는 `runtime/pprof` 또는 `net/http/pprof` 패키지와 같은 일반적인 방법을 사용하여 수집할 수 있는 pprof CPU 프로필을 지원합니다.
PGO를 활성화하려면 `go build` 명령어에 `-pgo` 플래그를 사용하여 pprof 프로필 파일의 경로를 지정하십시오. (위의 [참조](#go-command) 참조).
Go 1.20은 핫 콜 사이트에 대해 더 적극적으로 함수를 인라인하는 데 PGO를 사용합니다.
대표적인 Go 프로그램 집합에 대한 벤치마크 테스트 결과, 프로파일 기반 인라인 최적화를 활성화하면 성능이 약 3–4% 향상됩니다.
자세한 내용은 [PGO 사용자 가이드](/doc/pgo)를 참조하십시오.
향후 릴리스에서 더 많은 프로파일 기반 최적화를 추가할 계획입니다.
참고: 프로파일 기반 최적화는 미리보기 기능이므로, 적절한 주의를 기울여 사용하십시오.

Go 1.20 컴파일러는 내부 데이터 처리에 대한 새로운 방법을 사용하여 컴파일러의 프론트를 업그레이드했습니다. 이를 통해 여러 제네릭 유형 관련 문제를 해결하고, 제네릭 함수 및 메서드 내에서 타입 선언을 가능하게 합니다.

<!-- https://go.dev/issue/56103, CL 445598 -->
컴파일러는 이제 익명 인터페이스 사이클을 기본적으로 컴파일 오류로 [거부합니다](/issue/56103).
이는 복잡한 [내장 인터페이스](/ref/spec#Embedded_interfaces) 사용에서 비롯되며, 항상 미묘한 정확성 문제를 가지고 있었지만, 실제 사용 사례에 대한 증거는 없습니다.
사용자가 이 변경으로 인해 부정적인 영향을 받지 않았다는 가정하에,
Go 1.22의 언어 사양을 공식적으로 금지하도록 업데이트할 계획입니다.
이를 통해 도구 작성자들이 이 기능을 지원을 중단하도록 할 수 있습니다.

<!-- https://go.dev/issue/49569 -->
Go 1.18 및 1.19 버전에서 빌드 속도에 문제가 발생했습니다. 이는 주로 제네릭 지원 및 관련 작업 추가로 인해 발생했습니다. Go 1.20은 빌드 속도를 최대 10% 향상시켜 Go 1.17과 비슷한 수준으로 되돌렸습니다.
Go 1.19에 비해 생성된 코드의 성능도 전반적으로 약간 향상되었습니다.

## 링커 {#linker}

<!-- https://go.dev/issue/54197, CL 420774 -->
Linux에서, 링커는 이제 `glibc` 또는 `musl`의 동적 인터프리터를 링크 시간에 선택합니다.

<!-- https://go.dev/issue/35006 -->
Windows에서 Go 링커는 이제 최신 LLVM 기반의 C 툴체인을 지원합니다.

<!-- https://go.dev/issue/37762, CL 317917 -->
Go 1.20은 컴파일러에서 생성된
기호를 `go:` 및 `type:` 접두사로 사용하지만, `go.` 및 `type.`을 사용하지 않습니다.
이는 `go.`로 시작하는 사용자 패키지에 혼동을 방지합니다.
`debug/gosym` 패키지는 Go 1.20 및 이후 버전으로 빌드된 바이너리에 대한 이 새로운 명명 규칙을 이해합니다.

## 부트스트랩 {#bootstrap}

<!-- https://go.dev/issue/44505 -->
소스에서 Go 배포본을 빌드할 때 `GOROOT_BOOTSTRAP`이 설정되지 않은 경우,
이전 버전의 Go는 `$HOME/go1.4` 디렉터리에 Go 1.4 또는 이후 버전의 부팅 도구 체인을 찾았습니다 (`%HOMEDRIVE%%HOMEPATH%\go1.4` on Windows).
Go 1.18 및 Go 1.19는 Go 1.20을 부팅할 때 Go 1.17이 필요하다는 것을 예상하여, 먼저 `$HOME/go1.17` 또는 `$HOME/sdk/go1.17`를 찾은 후 `$HOME/go1.4`를 찾았습니다.
Go 1.20은 부팅에 Go 1.17 배포본이 필요하지만, 부팅 도구 체인의 최신 점 배포본을 사용하도록 변경했습니다. 따라서 Go 1.17.13이 필요합니다.
Go 1.20은 `$HOME/go1.17.13` 또는 `$HOME/sdk/go1.17.13`을 찾은 후 `$HOME/go1.4`를 찾습니다.
(특정 시스템이 `$HOME/go1.4` 경로를 하드 코딩했지만, 해당 위치에 더 새로운 Go 도구 체인을 설치한 경우를 지원하기 위함).
향후, 우리는 부팅 도구 체인을 약 1년에 한 번씩 업데이트할 계획이며, 특히 Go 1.22는 Go 1.20의 최종 점 배포본을 필요로 할 것으로 예상합니다.

## 표준 라이브러리 {#library}

```python
import os
import sys
```

| 기능 | 설명 | 예시 |
|---|---|---|
| 파일 시스템 접근 | 파일 및 디렉토리 조작 | `os.listdir('.')` |
| 프로세스 관리 | 프로세스 시작 및 종료 | `subprocess.run(['ls', '-l'])` |
| 네트워크 통신 | 소켓 기반 통신 | `socket.socket(socket.AF_INET, socket.SOCK_STREAM)` |
| 문자열 처리 | 문자열 조작 및 분석 | `re.search(r'pattern', string)` |

*   `os.environ`
*   `sys.path`
*   `json.loads()`
*   `datetime.datetime.now()`

### 새로운 암호/ECDH 패키지 {#crypto_ecdh}

<!-- https://go.dev/issue/52221, CL 398914, CL 450335, https://go.dev/issue/56052 -->
Go 1.20은 [`crypto/ecdh`](/pkg/crypto/ecdh/) 패키지를 추가하여 NIST 곡선 및 Curve25519를 사용하여 명시적인 Elliptic Curve Diffie-Hellman 키 교환을 지원합니다.

프로그램은 ECDH를 위해 `crypto/ecdh`를 사용하고, [`crypto/elliptic`](/pkg/crypto/elliptic/)의 낮은 수준의 기능을 대신 사용해야 합니다. 또한, 보다 고급 사용 사례의 경우, 타사 모듈을 사용해야 합니다.

### 여러 오류를 묶기 {#errors}

<!-- CL 432898 -->
Go 1.20에서 오류 감싸기 기능을 확장하여, 하나의 오류가 여러 개의 다른 오류를 감싸도록 허용합니다.

오류 `e`는 여러 오류를 감싸는 기능을 제공할 수 있습니다. 이를 위해 `Unwrap` 메서드를 구현하여 `[]error`를 반환하도록 합니다.

[`errors.Is`](/pkg/errors/#Is) 및
[`errors.As`](/pkg/errors/#As) 함수는
여러 겹쳐진 오류를 검사하도록 업데이트되었습니다.

[`fmt.Errorf`](/pkg/fmt/#Errorf) 함수는 이제 `%w` 형식 지정자를 여러 번 사용할 수 있으며, 이를 통해 모든 오류 인수를 래핑한 오류를 반환합니다.

새로운 함수 [`errors.Join`](/pkg/errors/#Join)는 오류 목록을 감싸는 오류를 반환합니다.

### HTTP 응답 컨트롤러 {#http_responsecontroller}

<!-- CL 436890, https://go.dev/issue/54136 -->
새로운
[`"net/http".ResponseController`](/pkg/net/http/#ResponseController)
형은 `"net/http".ResponseWriter" 인터페이스에서 처리되지 않는 확장된 요청별 기능을 제공합니다.

이전에, `ResponseWriter`가 구현할 수 있는 선택적 인터페이스를 정의하여, 요청별 기능을 추가했습니다. 예를 들어, [`Flusher`](/pkg/net/http/#Flusher)와 같은 인터페이스를 사용할 수 있습니다. 하지만 이러한 인터페이스는 찾기 어렵고 사용하기 불편합니다.

`ResponseController` 타입은 각 핸들러에 대한 컨트롤을 더 명확하고 쉽게 추가할 수 있는 방법을 제공합니다. Go 1.20에서 추가된 `SetReadDeadline` 및 `SetWriteDeadline`와 같은 두 가지 컨트롤도 있습니다. 이 컨트롤을 사용하면 각 요청에 대한 읽기 및 쓰기 시간 초를 설정할 수 있습니다. 예를 들어:

```markdown
```go
func RequestHandler(w ResponseWriter, r *Request) {
	  rc := http.NewResponseController(w)
	  rc.SetWriteDeadline(time.Time{}) // 서버 WriteTimeout을 무시하여 대용량 응답 전송
	  io.Copy(w, bigData)
	}
```
```

### 새로운 리버스 프록시 리라이트 훅 {#reverseproxy_rewrite}

<!-- https://go.dev/issue/53002, CL 407214 -->
`httputil.ReverseProxy`
(https://go.dev/pkg/net/http/httputil/#ReverseProxy)
은 새로운
`Rewrite`
(https://go.dev/pkg/net/http/httputil/#ReverseProxy.Rewrite)
훅 함수를 포함하며, 이전의 `Director` 훅을 대체합니다.

`Rewrite` 훅은 `ProxyRequest` 파라미터를 받습니다.
[`ProxyRequest`](/pkg/net/http/httputil/#ProxyRequest)에는 프록시가 수신한 입구 요청과, 프록시가 전송할 출구 요청이 모두 포함되어 있습니다.
`Director` 훅과 달리, 이 훅은 출구 요청에만 작동하며,
악성 입구 요청으로 인해 훅에 의해 추가된 헤더가 전송되기 전에 제거되는 상황을 피할 수 있도록 합니다.
자세한 내용은 [issue #50580](/issue/50580)를 참조하십시오.

[`ProxyRequest.SetURL`](/pkg/net/http/httputil/#ProxyRequest.SetURL)
메서드는 외부 요청을 지정된 대상지로 라우팅하며, `NewSingleHostReverseProxy` 함수를 대체합니다.
`NewSingleHostReverseProxy`와 달리, `SetURL`는 외부 요청의 `Host` 헤더도 설정합니다.

<!-- https://go.dev/issue/50465, CL 407414 -->
`ProxyRequest.SetXForwarded`
[`https://go.dev/pkg/net/http/httputil/#ProxyRequest.SetXForwarded`](#)
메서드는 아웃바운드 요청의 `X-Forwarded-For`, `X-Forwarded-Host`,
그리고 `X-Forwarded-Proto` 헤더를 설정합니다.
`Rewrite`를 사용할 때, 이러한 헤더는 기본적으로 추가되지 않습니다.

`Rewrite` 훅을 사용하는 예시가 다음과 같습니다.

```markdown
proxyHandler := &httputil.ReverseProxy{
  	Rewrite: func(r *httputil.ProxyRequest) {
  	  r.SetURL(outboundURL) // 요청을 outboundURL로 전달.
  	  r.SetXForwarded()     // X-Forwarded-* 헤더를 설정.
  	  r.Out.Header.Set("X-Additional-Header", "프록시에서 설정한 헤더")
  	},
}
```

<!-- CL 407375 -->
[`ReverseProxy`](/pkg/net/http/httputil/#ReverseProxy)가 들어오는 요청에 `User-Agent` 헤더가 없는 경우, 전달되는 요청에 `User-Agent` 헤더를 더 이상 추가하지 않습니다.

### 라이브러리의 미미한 변경 사항 {#minor_library_changes}

물론, 라이브러리의 다양한 미세한 변경 사항 및 업데이트가 있으며, 이는 Go 1의 [호환성](https://example.com/doc/go1compat)을 염두에 두고 개발되었습니다.
또한, 여기에는 나열되지 않은 다양한 성능 개선 사항이 있습니다.

#### [archive/tar](/pkg/archive/tar/)

<!-- https://go.dev/issue/55356, CL 449937 -->
`GODEBUG=tarinsecurepath=0` 환경 변수가 설정되면,
[`Reader.Next`](/pkg/archive/tar/#Reader.Next) 메서드는
다음 조건 중 하나에 해당하는 항목에 대해 이제 오류 [`ErrInsecurePath`](/pkg/archive/tar/#ErrInsecurePath)를 반환합니다.
* 파일 이름이 절대 경로이고, 현재 디렉터리 외부의 위치를 참조하거나
* 유효하지 않은 문자를 포함하거나
* (Windows의 경우) `NUL`과 같은 예약된 이름을 포함합니다.
향후 버전의 Go는 기본적으로 안전하지 않은 경로를 비활성화할 수 있습니다.

<!-- archive/tar -->

#### [archive/zip](/pkg/archive/zip/)

<!-- https://go.dev/issue/55356 -->
`GODEBUG=zipinsecurepath=0` 환경 변수가 설정되면,
[`NewReader`](/pkg/archive/zip/#NewReader)는 이제 ZIP 아카이브를 열 때,
파일 이름이 절대 경로이고, 현재 디렉터리 외부의 위치를 참조하거나,
유효하지 않은 문자를 포함하거나 (Windows의 경우) `NUL`과 같은 예약된 이름을 포함하는 경우
[`ErrInsecurePath`](/pkg/archive/zip/#ErrInsecurePath) 오류를 반환합니다.
향후 Go 버전에서는 기본적으로 안전하지 않은 경로를 비활성화할 수 있습니다.

<!-- CL 449955 -->
디렉토리 파일에서 파일 데이터를 읽는 경우 이제 오류가 반환됩니다.
zip 사양은 디렉토리 파일에 파일 데이터를 포함하는 것을 허용하지 않으므로, 이 변경 사항은 유효하지 않은 아카이브에서 읽는 경우에만 영향을 미칩니다.

<!-- archive/zip -->

#### [bytes](/pkg/bytes/)

<!-- CL 407176 -->
새로운
[`CutPrefix`](/pkg/bytes/#CutPrefix) 및
[`CutSuffix`](/pkg/bytes/#CutSuffix) 함수는
[`TrimPrefix`](/pkg/bytes/#TrimPrefix) 및
[`TrimSuffix`](/pkg/bytes/#TrimSuffix)와 유사하지만, 문자열이 잘린 여부도 함께 보고합니다.

<!-- CL 359675, https://go.dev/issue/45038 -->
새로운 `Clone` 함수는 바이트 슬라이스의 복사본을 할당합니다.

<!-- 바이트 -->

#### [context]( /pkg/context/)

<!-- https://go.dev/issue/51365, CL 375977 -->
새로운 [`WithCancelCause`](/pkg/context/#WithCancelCause) 함수는 주어진 오류를 사용하여 컨텍스트를 취소하는 방법을 제공합니다.
이 오류는 새로운 [`Cause`](/pkg/context/#Cause) 함수를 호출하여 가져올 수 있습니다.

<!-- 컨텍스트 -->

#### [crypto/ecdsa](/pkg/crypto/ecdsa/)

<!-- CL 353849 -->
지원되는 곡선을 사용할 때, 모든 연산이 이제 상수 시간으로 구현되었습니다.
이는 주로 P-384 및 P-521에 영향을 주어 CPU 시간을 5%에서 30%까지 증가시켰습니다.

<!-- https://go.dev/issue/56088, CL 450816 -->
새로운 `PrivateKey.ECDH` 메서드
(`ecdsa.PrivateKey`를 `ecdh.PrivateKey`로 변환)

```markdown
<!-- crypto/ecdsa -->
```

#### [crypto/ed25519](/pkg/crypto/ed25519/)

<!-- CL 373076, CL 404274, https://go.dev/issue/31804 -->
`PrivateKey.Sign` 메서드와
`VerifyWithOptions` 함수는 이제 Ed25519ph를 사용하여 사전 해시된 메시지를 서명할 수 있도록 지원하며,
`Options.HashFunc` 필드가
`crypto.SHA512`를 반환하도록 지정됩니다.
또한, Ed25519ctx 및 컨텍스트를 사용하는 Ed25519ph를 지원하며,
새로운 `Options.Context` 필드를 설정하여 지정됩니다.

<!-- crypto/ed25519 -->

#### [crypto/rsa](/pkg/crypto/rsa/)

<!-- CL 418874, https://go.dev/issue/19974 -->
새로운 필드 [`OAEPOptions.MGFHash`](/pkg/crypto/rsa/#OAEPOptions.MGFHash)
은 OAEP 디코딩에 대해 MGF1 해시를 개별적으로 구성할 수 있도록 합니다.

<!-- https://go.dev/issue/20654 -->
`crypto/rsa`는 이제 새로운, 더 안전하고 일정한 시간 복잡도를 갖는 백엔드를 사용합니다. 이는 디코딩 작업에 대해 약 15% (amd64에서 RSA-2048)에서 45% (arm64에서 RSA-4096)까지 CPU 실행 시간을 증가시키고, 32비트 아키텍처에서는 더 높은 증가를 가져옵니다.
암호화 작업은 이전보다 약 20배 느리지만 (여전히 디코딩보다 5-10배 빠름) 여전히 5-10배 빠릅니다.
향후 릴리스에서 성능이 향상될 것으로 예상됩니다.
`[PrecomputedValues](pkg/crypto/rsa/#PrecomputedValues)`의 필드를 수정하거나 수동으로 생성해서는 안 됩니다.

<!-- crypto/rsa -->

#### [crypto/subtle](/pkg/crypto/subtle/)

<!-- https://go.dev/issue/53021, CL 421435 -->
새로운 함수 [`XORBytes`](/pkg/crypto/subtle/#XORBytes)
두 바이트 슬라이스를 XOR 연산합니다.

<!-- crypto/subtle -->

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 426455, CL 427155, CL 426454, https://go.dev/issue/46035 -->
파싱된 인증서는 현재 해당 인증서를 활발하게 사용하는 모든 클라이언트 간에 공유됩니다.
많은 동시 연결을 통해 서버 또는 서버 그룹에 연결하는 프로그램의 경우 메모리 절약 효과가 큽니다.

<!-- https://go.dev/issue/48152, CL 449336 -->
인증서 검증 실패로 인한 핸드셰이크 실패의 경우,
TLS 클라이언트와 서버는 이제 새로운 유형의 오류인 `CertificateVerificationError`를 반환합니다.
이 오류는 제시된 인증서를 포함합니다.

<!-- crypto/tls -->

#### [crypto/x509](/pkg/crypto/x509/)

<!-- CL 450816, CL 450815 -->
[`ParsePKCS8PrivateKey`](/pkg/crypto/x509/#ParsePKCS8PrivateKey)
및
[`MarshalPKCS8PrivateKey`](/pkg/crypto/x509/#MarshalPKCS8PrivateKey)
이제 `*crypto/ecdh.PrivateKey` 유형의 키를 지원합니다.
[`ParsePKIXPublicKey`](/pkg/crypto/x509/#ParsePKIXPublicKey)
및
[`MarshalPKIXPublicKey`](/pkg/crypto/x509/#MarshalPKIXPublicKey)
이제 `*crypto/ecdh.PublicKey` 유형의 키를 지원합니다.
NIST 곡선 키 파싱은 여전히 다음과 같은 유형의 값을 반환합니다.
`*ecdsa.PublicKey` 및 `*ecdsa.PrivateKey`.
새로운 `ECDH` 메서드를 사용하여 `crypto/ecdh` 유형으로 변환합니다.

<!-- CL 449235 -->
새로운 [`SetFallbackRoots`](/pkg/crypto/x509/#SetFallbackRoots)
함수는 프로그램이 운영 체제 검증기 또는 표준 플랫폼 루트 번들이 실행 시간에 사용할 수 없는 경우, 대체 루트 인증서를 정의할 수 있도록 합니다.
이 함수는 일반적으로 새로운 패키지인 [golang.org/x/crypto/x509roots/fallback](/pkg/golang.org/x/crypto/x509roots/fallback)와 함께 사용됩니다. 이 패키지는 최신 루트 번들을 제공합니다.

```
<!-- crypto/x509 -->
```

#### [debug/elf](/pkg/debug/elf/)

<!-- CL 429601 -->
`SHT_NOBITS` 섹션에서 데이터를 읽으려고 시도하는 경우,
[`Section.Data`](/pkg/debug/elf/#Section.Data)
또는 [`Section.Open`](/pkg/debug/elf/#Section.Open)에서 반환된 리더를 사용하더라도
이제 오류가 반환됩니다.

<!-- CL 420982 -->
LoongArch 시스템에서 사용하기 위한 추가적인 `R_LARCH_*` 상수가 정의되었습니다.

<!-- CL 420982, CL 435415, CL 425555 -->
`[R_PPC64_*`](/pkg/debug/elf/#R_PPC64) 유형의 추가 상수들이 PPC64 ELFv2 위치 지정에 사용하기 위해 정의되었습니다.

<!-- CL 411915 -->
`[R_PPC64_SECTOFF_LO_DS](pkg/debug/elf/#R_PPC64_SECTOFF_LO_DS)`의 상수 값은 61에서 62로 수정되었습니다.

<!-- 디버깅/ELF -->

#### [debug/gosym](/pkg/debug/gosym/)

<!-- https://go.dev/issue/37762, CL 317917 -->
[Go의 심볼 명명 규칙](#linker)의 변경으로 인해, Go 바이너리를 처리하는 도구는 Go 1.20의 `debug/gosym` 패키지를 사용하여 기존 및 새로운 바이너리를 모두 투명하게 처리해야 합니다.

<!-- debug/gosym -->

#### [debug/pe](/pkg/debug/pe/)

<!-- CL 421357 -->
`IMAGE_FILE_MACHINE_RISCV*` 상수를 추가로 정의하여 RISC-V 시스템에서 사용하도록 합니다. (자세한 내용은 `/pkg/debug/pe/#IMAGE_FILE_MACHINE_RISCV128` 참조)

<!-- 디버깅/PE -->

#### [encoding/binary](/pkg/encoding/binary/)

<!-- CL 420274 -->
`ReadVarint` 및 `ReadUvarint` 함수는 부분적인 값을 읽은 후 `io.ErrUnexpectedEOF`를 반환하게 되며, 이전에는 `io.EOF`를 반환했습니다.

<!-- encoding/binary -->

#### [encoding/xml](/pkg/encoding/xml/)

<!-- https://go.dev/issue/53346, CL 424777 -->
새로운 `Encoder.Close` 메서드
(`/pkg/encoding/xml/#Encoder.Close`)는 인코딩이 완료된 후 닫히지 않은 요소를 확인하는 데 사용할 수 있습니다.

<!-- CL 103875, CL 105636 -->
이제 디코더는 콜론이 두 개 이상 있는 요소 및 속성 이름을, 예를 들어 `<a:b:c>`와 같이, 그리고 빈 문자열로 해결되는 네임스페이스를, 예를 들어 `xmlns:a=""`와 같이 거부합니다.

<!-- CL 107255 -->
이제 디코더는 열림 태그와 닫힘 태그에서 서로 다른 네임스페이스 접미사를 사용하는 요소를 거부합니다.
두 접미사 모두 동일한 네임스페이스를 나타치더라도 마찬가지입니다.

<!-- encoding/xml -->

#### [errors](/pkg/errors/)

<!-- https://go.dev/issue/53435 -->
새로운 `Join` 함수는 오류 목록을 감싸는 오류를 반환합니다.

<!-- 오류 -->

#### [fmt](/pkg/fmt/)

<!-- https://go.dev/issue/53435 -->
`Errorf` 함수는 `%w` 형식 지정자를 여러 번 사용할 수 있으며, `%w`에 전달된 모든 인수를 포함하는 오류 목록으로 래핑된 오류를 반환합니다.

<!-- https://go.dev/issue/51668, CL 400875 -->
새로운 `FormatString` 함수는 [`State`](/pkg/fmt/#State)에 해당하는 포맷팅 지시문을 복구합니다.
이는 `Formatter` 구현에서 유용할 수 있습니다. (`/pkg/fmt/#Formatter`)

<!-- fmt -->

#### [go/ast](pkg/go/ast/)

<!-- CL 426091, https://go.dev/issue/50429 -->
새로운 `RangeStmt.Range` 필드(`/pkg/go/ast/#RangeStmt.Range`)는 `range` 키워드의 위치를 범위 문장에서 기록합니다.

<!-- CL 427955, https://go.dev/issue/53202 -->
새로운 `File.FileStart` 및 `File.FileEnd` 필드는 전체 소스 파일의 시작 및 끝 위치를 기록합니다.

<!-- go/ast -->

#### [go/token](pkg/go/token/)

<!-- CL 410114, https://go.dev/issue/53200 -->
새로운 `FileSet.RemoveFile` 메서드는 `FileSet`에서 파일을 제거합니다.
장시간 실행되는 프로그램은 더 이상 필요하지 않은 파일과 관련된 메모리를 해제하는 데 이 메서드를 사용할 수 있습니다.

<!-- go/token -->

#### [go/types](pkg/go/types/)

<!-- CL 454575 -->
새로운 `Satisfies` 함수는
어떤 타입이 제약 조건을 만족하는지 보고합니다.
이 변경 사항은 [새로운 언어 의미론](#language)과 일치하며, 제약 조건을 만족하는 것과 인터페이스를 구현하는 것을 구별합니다.

<!-- go/types -->

#### [html/template](pkg/html/template/)

<!-- https://go.dev/issue/59153 -->
<!-- CL 481993 -->
Go 1.20.3 이상
[ECMAScript 6 템플릿 리터럴에서 동작을 금지합니다.](/pkg/html/template#hdr-Security_Model)
이 동작은 `GODEBUG=jstmpllitinterp=1` 설정을 통해 되돌릴 수 있습니다.

<!-- html/템플릿 -->

#### [io](/pkg/io/)

<!-- https://go.dev/issue/45899, CL 406776 -->
새로운 `OffsetWriter`([https://go.dev/pkg/io#OffsetWriter])는
숨겨진 `WriterAt`([https://go.dev/pkg/io#WriterAt])를 감싸고
`Seek`, `Write`, `WriteAt` 메서드를 제공하여
효과적인 파일 오프셋 위치를 고정된 양만큼 조정합니다.

<!-- io -->

#### [io/fs](pkg/io/fs/)

<!-- CL 363814, https://go.dev/issue/47209 -->
새로운 오류 [`SkipAll`](/pkg/io/fs/#SkipAll)
은 [`WalkDir`](/pkg/io/fs/#WalkDir)를
즉시 종료하지만 성공적으로.

<!-- io -->

#### [math/big](/pkg/math/big/)

<!-- https://go.dev/issue/52182 -->
`math/big` 패키지의 넓은 범위와
입력에 따라 달라지는 동작 시간 때문에, 이를 사용하여 암호화를 구현하는 것은 적합하지 않습니다.
표준 라이브러리의 암호화 패키지는 이제 공격자가 제어하는 입력에 대해 복잡한
`Int` 메서드를 호출하지 않습니다.
미래에는 `math/big`에 존재하는 버그가 보안 취약점으로 간주될지는 표준 라이브러리에 미치는 더 광범위한 영향에 따라 결정됩니다.

<!-- 수학/큰 -->

#### [math/rand](pkg/math/rand/)

<!-- https://go.dev/issue/54880, CL 436955, https://go.dev/issue/56319 -->
`math/rand` 패키지는 이제 전역 난수 생성기를 자동으로 시드합니다
(예: `Float64` 및 `Int`와 같은 상위 레벨 함수에서 사용되는) 무작위 값으로,
그리고 상위 레벨의 `Seed` 함수는 더 이상 사용되지 않습니다.
재현 가능한 난수 시퀀스가 필요한 프로그램은 `rand.New(rand.NewSource(seed))`를 사용하여 자체 난수 소스를 할당하는 것을 선호해야 합니다.

프로그램이 일관된 전역 시드 동작을 필요로 하는 경우, 다음과 같이 환경 변수를 설정할 수 있습니다.
`GODEBUG=randautoseed=0`

<!-- https://go.dev/issue/20661 -->
최상위 `Read` 함수가 사용 중단됨.
대부분의 경우, `crypto/rand.Read`가 더 적절합니다.

<!-- math/rand -->

#### [mime](/pkg/mime/)

<!-- https://go.dev/issue/48866 -->
`ParseMediaType` 함수가 이제 중복된 매개변수 이름을 허용하며, 이름의 값이 동일한 경우에만 작동합니다.

<!-- mime -->

#### [mime/multipart](/pkg/mime/multipart/)

<!-- CL 431675 -->
`Reader` 타입의 메서드가 이제 `io.Reader`에서 반환되는 오류를 감싸고 있습니다.

<!-- https://go.dev/issue/59153 -->
<!-- CL 481985 -->
Go 1.19.8 이상 버전에서는 이 패키지가 처리하는 MIME 데이터의 크기를 제한하여 악성 입력을 방지합니다.
`Reader.NextPart` 및 `Reader.NextRawPart`는 한 파트의 헤더 수를 10000으로 제한하고, `Reader.ReadForm`은 모든 `FileHeaders`에 있는 헤더의 총 개수를 10000으로 제한합니다.
이 제한은 `GODEBUG=multipartmaxheaders` 설정을 통해 조정할 수 있습니다.
`Reader.ReadForm`은 또한 폼 내의 파트 수를 1000으로 더욱 제한합니다.
이 제한은 `GODEBUG=multipartmaxparts` 설정을 통해 조정할 수 있습니다.

<!-- mime/multipart -->

#### [net](pkg/net/)

<!-- https://go.dev/issue/50101, CL 446179 -->
`LookupCNAME` 함수는 이제 `CNAME` 레코드가 존재하는 경우, 해당 레코드의 내용을 일관되게 반환합니다. 이전에는 Unix 시스템 및 순수 Go 리소러를 사용할 때, `LookupCNAME`은 `A`, `AAAA` 또는 `CNAME` 레코드가 없는 이름을 참조하는 `CNAME` 레코드에 대해 오류를 반환했습니다. 이 변경 사항은 `LookupCNAME`을 Windows의 이전 동작과 일치하도록 수정하여, `CNAME`이 존재하는 경우 `LookupCNAME`이 성공하도록 합니다.

<!-- https://go.dev/issue/53482, CL 413454 -->
[`Interface.Flags`](/pkg/net/#Interface.Flags)에 새로운 플래그 `FlagRunning`이 추가되었습니다.
이는 인터페이스가 운영적으로 활성 상태임을 나타냅니다.
관리적으로 구성되었지만 활성화되지 않은 인터페이스(예: 네트워크 케이블이 연결되지 않은 경우)는
`FlagUp`이 설정되지만 `FlagRunning`은 설정되지 않습니다.

<!-- https://go.dev/issue/55301, CL 444955 -->
새로운 `Dialer.ControlContext` 필드는 기존의 `Dialer.Control` 훅과 유사한 콜백 함수를 포함하며, 또한 다이얼 컨텍스트를 매개변수로 받습니다.
`Control`는 `ControlContext`가 `nil`이 아닐 때 무시됩니다.

<!-- CL 428955 -->
Go DNS 리졸버는 `trust-ad` 리졸버 옵션을 인식합니다.
`resolv.conf` 파일에 `options trust-ad`를 설정하면,
Go 리졸버는 DNS 쿼리에서 AD 비트를 설정합니다. 그러나 리졸버는 응답에서 AD 비트를 사용하지 않습니다.

<!-- CL 448075 -->
DNS 확인은 `/etc/nsswitch.conf` 파일의 변경 사항을 감지하고, 변경될 때 파일을 다시 로드합니다. 확인은 최대 5초마다 수행되며, 이는 이전 `/etc/hosts` 및 `/etc/resolv.conf` 파일의 처리에 부합합니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- https://go.dev/issue/51914 -->
`ResponseWriter.WriteHeader` 함수가 이제 `1xx` 상태 코드를 전송하도록 지원합니다.

<!-- https://go.dev/issue/41773, CL 356410 -->
새로운 [`Server.DisableGeneralOptionsHandler`](/pkg/net/http/#Server.DisableGeneralOptionsHandler) 구성 설정은 기본 `OPTIONS *` 핸들러를 비활성화할 수 있도록 합니다.

<!-- https://go.dev/issue/54299, CL 447216 -->
새로운 `Transport.OnProxyConnectResponse` 훅은 `Transport`가 `CONNECT` 요청에 대한 프록시로부터 HTTP 응답을 받을 때 호출됩니다.

<!-- https://go.dev/issue/53960, CL 418614 -->
HTTP 서버는 이제 요청 본문이 포함된 HEAD 요청을 허용합니다.
이전에는 이러한 요청을 유효하지 않은 것으로 거부했습니다.

<!-- https://go.dev/issue/53896 -->
`net/http` 함수에서 반환되는 HTTP/2 스트림 오류는 [`errors.As`](/pkg/errors/#As)를 사용하여
[`golang.org/x/net/http2.StreamError`](/pkg/golang.org/x/net/http2/#StreamError)로 변환할 수 있습니다.

<!-- https://go.dev/cl/397734 -->
쿠키 이름에서 선행 및 후행 공백이 제거되므로, 유효하지 않은 것으로 거부되지 않습니다.
예를 들어, "name =value"로 설정된 쿠키는 "name"으로 쿠키를 설정하는 것으로 간주됩니다.

<!-- https://go.dev/issue/52989 -->
`Cookie` 객체에 `Expires` 필드가 비어 있는 경우, 이제 유효한 것으로 간주됩니다.
`Cookie.Valid` 메서드는 `Expires` 필드가 설정된 경우에만 확인합니다.

<!-- net/http -->

#### [net/netip](/pkg/net/netip/)

<!-- https://go.dev/issue/51766, https://go.dev/issue/51777, CL 412475 -->
새로운 `IPv6LinkLocalAllRouters`
및 `IPv6Loopback` 함수는
`net/netip` 패키지의
`net.IPv6loopback` 및
`net.IPv6linklocalallrouters`에 상응합니다.

<!-- net/netip -->

#### [os](/pkg/os/)

<!-- CL 448897 -->
Windows에서, `NUL`이라는 이름은 더 이상 `Mkdir`([https://pkg/os/#Mkdir](https://pkg/os/#Mkdir)) 및 `Stat`([https://pkg/os/#Stat](https://pkg/os/#Stat))에서 특별한 경우로 취급되지 않습니다.

<!-- https://go.dev/issue/52747, CL 405275 -->
Windows에서, [`File.Stat`](/pkg/os/#File.Stat)은 파일이 디렉터리일 때 파일 핸들을 사용하여 속성을 가져옵니다.
이전에는 `Open`](/pkg/os/#Open)에 전달된 경로를 사용했지만, 파일이 이동되거나 대체된 경우 이 경로가 파일 핸들이 나타내는 파일을 더 이상 나타내지 않을 수 있습니다.
이 변경 사항은 디렉터리를 `FILE_SHARE_DELETE` 접근 없이 열도록 `Open`을 수정하여, 일반 파일과 동일한 동작을 구현합니다.

<!-- https://go.dev/issue/36019, CL 405275 -->
Windows에서, [`File.Seek`](/pkg/os/#File.Seek)가 이제 디렉토리의 시작 부분으로 이동하는 것을 지원합니다.

<!-- os -->

#### [os/exec](/pkg/os/exec/)

<!-- https://go.dev/issue/50436, CL 401835 -->
새로운 [`Cmd`](/pkg/os/exec/#Cmd) 필드
[`Cancel`](/pkg/os/exec/#Cmd.Cancel) 및
[`WaitDelay`](/pkg/os/exec/#Cmd.WaitDelay)
는 `Cmd`가 연결된
`Context`가 취소되거나, 자식 프로세스가 I/O 파이프를 여전히 열어 놓은 상태에서 프로세스가 종료될 때, `Cmd`의 동작을 지정합니다.

<!-- os/exec -->

#### [경로/파일 경로](/pkg/path/filepath/)

<!-- CL 363814, https://go.dev/issue/47209 -->
새로운 오류 [`SkipAll`](/pkg/path/filepath/#SkipAll)
은 [`Walk`](/pkg/path/filepath/#Walk)를
즉시 종료하지만 성공적으로 완료합니다.

<!-- https://go.dev/issue/56219, CL 449239 -->
새로운 `IsLocal` 함수(`IsLocal` (/pkg/path/filepath/#IsLocal))는 경로가 특정 디렉토리에 대해 문자열 기반으로 로컬인지 여부를 보고합니다.
예를 들어, `IsLocal(p)`가 `true`이면, `Open(p)`는 현재 디렉토리에 속한 하위 트리의 문자열 내에 있는 파일을 참조합니다.

<!-- io -->

#### [reflect](/pkg/reflect/)

<!-- https://go.dev/issue/46746, CL 423794 -->
새로운 `Value.Comparable` 및
`Value.Equal` 메서드는 두 개의 `Value`를 비교하는 데 사용할 수 있습니다.
`Comparable`은 특정 `Value` 수신자에 대해 `Equal`이 유효한 작업인지 보고합니다.

<!-- https://go.dev/issue/48000, CL 389635 -->
새로운 `Value.Grow` 메서드
(`Value.Grow`)는 슬라이스를 확장하여, 추가 `n` 개의 요소에 대한 공간을 확보합니다.

<!-- https://go.dev/issue/52376, CL 411476 -->
새로운 [`Value.SetZero`](/pkg/reflect/#Value.SetZero) 메서드는
값이 해당 유형의 0 값으로 설정합니다.

<!-- CL 425184 -->
Go 1.18에서 [`Value.SetIterKey`](/pkg/reflect/#Value.SetIterKey)
과 [`Value.SetIterValue`](/pkg/reflect/#Value.SetIterValue) 메서드가 도입되었습니다.
이것은 최적화입니다: `v.SetIterKey(it)`는 `v.Set(it.Key())`와 동일하게 작동하도록 설계되었습니다.
구현은 최적화되지 않은 형태에 존재하는, 사용되지 않은 필드에 대한 검사를 누락했습니다.
Go 1.20은 이러한 메서드를 수정하여, 사용되지 않은 필드 검사를 포함합니다.

<!-- 반영 -->

```
#### [regexp](/pkg/regexp/)
```

<!-- CL 444817 -->
Go 1.19.2 및 Go 1.18.7은 정규 표현식 파서를 위한 보안 패치를 포함하여, 지나치게 큰 표현식을 거부하고 메모리 사용량을 제한하도록 수정했습니다.
Go 패치 릴리스는 새로운 API를 도입하지 않으므로, 이 경우 파서는 [`syntax.ErrInternalError`](/pkg/regexp/syntax/#ErrInternalError)를 반환했습니다.
Go 1.20에서는 더 구체적인 오류인 [`syntax.ErrLarge`](/pkg/regexp/syntax/#ErrLarge)를 도입했으며, 파서는 이제 이 오류를 반환합니다.

<!-- regexp -->

#### [runtime/cgo](/pkg/runtime/cgo/)

<!-- https://go.dev/issue/46731, CL 421879 -->
Go 1.20에서 새로운 [`Incomplete`](/pkg/runtime/cgo/#Incomplete) 마커 유형이 추가되었습니다.
cgo로 생성된 코드는 `cgo.Incomplete`를 사용하여 불완전한 C 유형을 표시합니다.

<!-- runtime/cgo -->

#### [runtime/metrics](/pkg/runtime/metrics/)

<!-- https://go.dev/issue/47216, https://go.dev/issue/49881 -->
Go 1.20에서 새롭게 지원되는 [메트릭](pkg/runtime/metrics/#hdr-Supported_metrics)이 추가되었습니다.
여기에는 현재 `GOMAXPROCS` 설정(`/sched/gomaxprocs:threads`),
실행된 cgo 호출 수(`/cgo/go-to-c-calls:calls`),
전체 뮤텍스 블록 시간(`/sync/mutex/wait/total:seconds`),
그리고 가비지 컬렉션에 소요된 시간과 관련된 다양한 측정값이 포함됩니다.

<!-- CL 427615 -->
시간 기반 히스토그램 지표는 이제 정확도가 떨어졌지만, 메모리 사용량이 훨씬 적습니다.

<!-- 성능/지표 -->

#### [runtime/pprof](/pkg/runtime/pprof/)

<!-- CL 443056 -->
뮤텍스 프로필 샘플이 이제 미리 스케일링되어 있으며, 실행 중에 샘플링 속도가 변경될 경우 이전 뮤텍스 프로필 샘플이 잘못 스케일링되는 문제를 해결합니다.

<!-- CL 416975 -->
Windows에서 수집된 프로파일에는 메모 매핑 정보가 포함되어 있어, 위치 독립적인 바이너리에 대한 심볼화 문제를 해결합니다.

<!-- runtime/pprof -->

#### [runtime/trace](/pkg/runtime/trace/)

<!-- CL 447135, https://go.dev/issue/55022 -->
가비지 컬렉터의 백그라운드 스위퍼가 덜 자주 실행되면서, 실행 추적에 발생하는 불필요한 이벤트가 현저히 줄어들었습니다.

<!-- runtime/trace -->

#### [strings](pkg/strings/)

<!-- CL 407176, https://go.dev/issue/42537 -->
새로운
[`CutPrefix`](/pkg/strings/#CutPrefix) 및
[`CutSuffix`](/pkg/strings/#CutSuffix) 함수는
[`TrimPrefix`](/pkg/strings/#TrimPrefix) 및
[`TrimSuffix`](/pkg/strings/#TrimSuffix)와 유사하지만, 문자열이 잘린 여부도 보고합니다.

<!-- 문자열 -->

#### [sync](/pkg/sync/)

<!-- CL 399094, https://go.dev/issue/51972 -->
새로운 [`Map`](/pkg/sync/#Map) 메서드인 [`Swap`](/pkg/sync/#Map.Swap),
[`CompareAndSwap`](/pkg/sync/#Map.CompareAndSwap), 및
[`CompareAndDelete`](/pkg/sync/#Map.CompareAndDelete)
을 사용하면 기존 맵 항목을 원자적으로 업데이트할 수 있습니다.

<!-- 동기화 -->

#### [syscall](/pkg/syscall/)

<!-- CL 411596 -->
FreeBSD 11 및 이전 버전을 위한 FreeBSD 호환 섀도 코드가 FreeBSD에서 제거되었습니다.

<!-- CL 407574 -->
리눅스에서는 [`CLONE_*`](/pkg/syscall/#CLONE_CLEAR_SIGHAND) 상수를 추가로 정의하여 `SysProcAttr.Cloneflags` 필드와 함께 사용할 수 있습니다.

<!-- CL 417695 -->
Linux에서 새로운 `SysProcAttr.CgroupFD` 및 `SysProcAttr.UseCgroupFD` 필드는 자식 프로세스를 특정 cgroup으로 배치하는 방법을 제공합니다.

<!-- syscall -->

#### [테스팅](/pkg/testing/)

<!-- https://go.dev/issue/43620, CL 420254 -->
새로운 메서드 [`B.Elapsed`](/pkg/testing/#B.Elapsed)는
벤치마크의 현재 경과 시간을 보고하며, 이는 `ReportMetric`를 사용하여 보고할 때 사용할 수 있는 속도를 계산하는 데 유용할 수 있습니다.

<!-- https://go.dev/issue/48515, CL 352349 -->
`T.Run` 함수에서
`T.Cleanup`에 전달된
함수에서 호출하는 것은
잘 정의되지 않았으며, 이제 panic이 발생합니다.

<!-- 테스트 -->

#### [time](pkg/time/)

<!-- https://go.dev/issue/52746, CL 412495 -->
새로운 타임 레이아웃 상수 [`DateTime`](/pkg/time/#DateTime),
[`DateOnly`](/pkg/time/#DateOnly), 및
[`TimeOnly`](/pkg/time/#TimeOnly)는 공개 Go 소스 코드 설문조사에서 가장 일반적으로 사용되는 세 가지 레이아웃 문자열에 대한 이름입니다.

<!-- CL 382734, https://go.dev/issue/50770 -->
새로운 `Time.Compare` 메서드는 두 개의 시간을 비교합니다.

<!-- CL 425037 -->
[`Parse`](/pkg/time/#Parse)
이제 입력에서 서브-나노초 정밀도를 무시하고, 대신 해당 자릿수를 오류로 보고하는 대신, 이를 무시합니다.

<!-- CL 444277 -->
`Time.MarshalJSON` 메서드는 이제 RFC 3339에 대한 준수를 더욱 엄격하게 적용합니다.

<!-- 시간 -->

#### [unicode/utf16](pkg/unicode/utf16/)

<!-- https://go.dev/issue/51896, CL 409054 -->
새로운 `AppendRune`
함수는 주어진 `rune`의 UTF-16 인코딩을 uint16 슬라이스에 추가합니다.
이는 `utf8.AppendRune`와 유사합니다.

<!-- unicode/utf16 -->

<!-- x/build/cmd/relnote에서 발생하는 오탐을 방지합니다: -->
<!-- https://go.dev/issue/45964는 Go 1.18 릴리스 노트에 문서화되었지만 최근에 닫혔습니다 -->
<!-- https://go.dev/issue/52114는 golang.org/x/net/http2.Transport.DialTLSContext를 추가하기 위한 승인된 제안입니다; 이는 Go 릴리스의 일부가 아닙니다 -->
<!-- CL 431335: cmd/api: api/*.txt에 대한 검사를 더 엄격하게 수행 -->
<!-- CL 447896 api: 55301.txt에 개행 문자 추가; api/next/55301.txt 수정 -->
<!-- CL 449215 api/next/54299: 누락된 개행 문자 추가; api/next/54299.txt 수정 -->
<!-- CL 433057 cmd: vendored golang.org/x/tools를 여러 오류 감싸기 위해 업데이트 -->
<!-- CL 423362 crypto/internal/boring: 더 최신 boringcrypto로 업데이트, arm64 지원 추가 -->
<!-- https://go.dev/issue/53481 x/cryptobyte ReadUint64, AddUint64 -->
<!-- https://go.dev/issue/51994 x/crypto/ssh -->
<!-- https://go.dev/issue/55358 x/exp/slices -->
<!-- https://go.dev/issue/54714 x/sys/unix -->
<!-- https://go.dev/issue/50035 https://go.dev/issue/54237 x/time/rate -->
<!-- CL 345488 strconv 최적화 -->
<!-- CL 428757 reflect 은퇴, 되돌림 -->
<!-- https://go.dev/issue/49390 compile -l -N은 완전히 지원됩니다 -->
<!-- https://go.dev/issue/54619 x/tools -->
<!-- CL 448898 되돌림 -->
<!-- https://go.dev/issue/54850 x/net/http2 Transport.MaxReadFrameSize -->
<!-- https://go.dev/issue/56054 x/net/http2 SETTINGS_HEADER_TABLE_SIZE -->
<!-- CL 450375 되돌림 -->
<!-- CL 453259 api에서 은퇴 추적 -->
<!-- CL 453260 api에서 darwin 포트 추적 -->
<!-- CL 453615 archive/tar에서 은퇴 주석 수정 -->
<!-- CL 453616 archive/zip에서 은퇴 주석 수정 -->
<!-- CL 453617 encoding/csv에서 은퇴 주석 수정 -->
<!-- https://go.dev/issue/54661 x/tools/go/analysis -->
<!-- CL 423359, https://go.dev/issue/51317 arena -->
