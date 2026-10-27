<!--
참고: 이 문서 및 이 디렉토리의 다른 문서에서, 고정 폭 문구를 사용합니다. 예를 들어 `hello` `world` 와 같이.
이러한 문구에서 내부 태그를 제거하는 CL을 보내지 마세요.
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.21 소개 {#introduction}

이 문서는 Go 1.21 버전의 주요 변경 사항 및 새로운 기능에 대한 소개를 제공합니다.

가장 최신 Go 릴리스인 버전 1.21은 [Go 1.20](/doc/go1.20) 이후 6개월 만에 출시되었습니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
물론, 이 릴리스는 Go 1의 [호환성 약속](/doc/go1compat)을 유지합니다;
실제로, Go 1.21은 이 약속을 [개선합니다](#tools).
대부분의 Go 프로그램이 이전과 같이 컴파일 및 실행될 것으로 예상합니다.

<!-- https://go.dev/issue/57631 -->
Go 1.21은 릴리스 번호에 대한 작은 변경 사항을 도입합니다.
과거에는 Go 1._N_를 사용하여 전체 Go 언어 버전, 릴리스 패밀리 및 해당 패밀리의 첫 번째 릴리스를 모두 참조했습니다.
Go 1.21부터 첫 번째 릴리스는 이제 Go 1._N_.0으로 지정됩니다.
오늘 저희는 Go 1.21 언어와 초기 구현인 Go 1.21.0 릴리스를 모두 출시합니다.
이 문서는 "Go 1.21"을 참조합니다. `go version`과 같은 도구는 (Go 1.21.1로 업그레이드할 때까지) "`go1.21.0`"을 보고합니다.
새로운 버전 번호에 대한 자세한 내용은 "Go Toolchains" 설명서의 "[Go versions](/doc/toolchain#version)"를 참조하십시오.

## 언어 변경 사항 {#language}

```
// Example Go code
package main
```

Go 1.21 버전에서는 새로운 세 가지 기본 함수가 언어에 추가되었습니다.

- <!-- https://go.dev/issue/59488 -->
    새로운 함수 `min` 및 `max`은 고정된 수의 주어진 인수의
    가장 작은 (또는 `max`의 경우 가장 큰) 값을 계산합니다.
    자세한 내용은 언어 사양을 참조하십시오.
    [https://go.dev/ref/spec#Min_and_max](https://go.dev/ref/spec#Min_and_max)
  - <!-- https://go.dev/issue/56351 -->
    새로운 함수 `clear`은 맵의 모든 요소를 삭제하거나 슬라이스의 모든 요소를 0으로 설정합니다.
    자세한 내용은 언어 사양을 참조하십시오.
    [https://go.dev/ref/spec#Clear](https://go.dev/ref/spec#Clear)

<!-- https://go.dev/issue/57411 -->
패키지 초기화 순서가 이제 더 정확하게 지정됩니다.
새로운 알고리즘은 다음과 같습니다:

- 모든 패키지를 임포트 경로별로 정렬합니다.
- 패키지 목록이 비어 있을 때까지 반복합니다:
  - 목록에서 모든 임포트가 이미 초기화된 첫 번째 패키지를 찾습니다.
  - 해당 패키지를 초기화하고 목록에서 제거합니다.

이로 인해 특정 초기화 순서를 의존하는 일부 프로그램의 동작이 변경될 수 있습니다. 이러한 순서를 명시적으로 import하지 않은 경우, 과거 버전의 사양에서는 이러한 프로그램의 동작이 명확하게 정의되지 않았습니다. 새로운 규칙은 명확한 정의를 제공합니다.

여러 가지 개선 사항이 추가되어 타입 추론의 성능과 정확성이 향상되었습니다.

- <!-- https://go.dev/issue/59338 -->
    (부분적으로 인스턴스화된) 일반 함수는 이제 자체적으로 (부분적으로 인스턴스화된) 일반 함수를 인수로 호출할 수 있습니다.
    컴파일러는 호출된 함수의 누락된 타입 인수를 (이전과 마찬가지로) 추론하고,
    완전히 인스턴스화되지 않은 일반 함수 인수인 각 인수의 경우,
    누락된 타입 인수를 (새로운) 추론합니다.
    일반적인 사용 사례는 컨테이너 (예: [slices.IndexFunc](/pkg/slices#IndexFunc))에서 작동하는 일반 함수를 호출하는 경우이며, 여기서 함수 인수도 일반 함수일 수 있고, 호출된 함수의 타입 인자와 해당 인수의 타입 인수는 컨테이너 타입에서 추론됩니다.
    일반적으로, 인수가 할당되거나 결과 값으로 반환될 때, 타입 인수가 할당에서 추론될 수 있는 경우, 일반 함수는 명시적인 인스턴스화 없이 사용할 수 있습니다.
  - <!-- https://go.dev/issue/60353, https://go.dev/issue/57192, https://go.dev/issue/52397, https://go.dev/issue/41176 -->
    타입 추론은 이제 인터페이스에 값을 할당할 때 메서드를 고려합니다.
    메서드 시그니처에 사용된 타입 매개변수의 타입 인수는 해당 메서드의 대응되는 매개변수 타입에서 추론될 수 있습니다.
  - <!-- https://go.dev/issue/51593 https://go.dev/issue/39661 -->
    마찬가지로, 타입 인수가 해당 제약 조건의 모든 메서드를 구현해야 하므로, 타입 인수와 제약 조건의 메서드가 일치합니다. 그러면 추가적인 타입 인수가 추론될 수 있습니다.
  - <!-- https://go.dev/issue/58671 -->
    여러 가지 유형 (예: 유형 지정되지 않은 정수와 유형 지정되지 않은 부동 소수점 상수)의 유형 지정되지 않은 상수 인수가 동일한 (다른 방식으로 지정되지 않은) 타입 매개변수 유형의 매개변수에 전달될 때, 오류 대신 타입 추론은 유형을 운영자에서 유형 지정되지 않은 상수 연산자와 동일한 방식으로 결정합니다.
    이 변경 사항은 유형 지정되지 않은 상수 인수로 추론된 유형을 상수 표현식의 유형과 일치시킵니다.
  - <!-- https://go.dev/issue/59750 -->
    타입 추론은 이제 할당에서 대응되는 유형을 일치시킬 때 정확합니다.
    (예: 슬라이스의 요소 또는 함수 시그니처의 매개변수 유형)와 같이 구성 요소 유형은 일치하기 위해 동일해야 (적절한 타입 인수를 사용하여) 합니다. 그렇지 않으면 추론에 실패합니다.
    이 변경 사항은 보다 정확한 오류 메시지를 생성합니다.
    과거에는 타입 추론이 잘못 성공하고 유효하지 않은 할당으로 이어질 수 있었지만, 이제 두 유형이 일치할 수 없는 경우 컴파일러는 추론 오류를 보고합니다.

<!-- https://go.dev/issue/58650 -->
일반적으로,
[타입 추론](/ref/spec#Type_inference)에 대한 언어 사양의 설명이 명확하게 변경되었습니다.
이러한 변경 사항들이 모두 결합되어, 타입 추론이 더욱 강력해지고, 추론 실패가 덜 발생하게 됩니다.

<!-- https://go.dev/issue/57969 -->

Go 1.21에는 미래 버전의 Go에서 고려 중인 언어 변경 사항의 미리보기 기능이 포함되어 있습니다:
루프 변수를 루프 전체가 아닌 루프의 각 반복마다 생성하도록 하는 것입니다. 이를 통해 의도치 않은 공유 오류를 방지할 수 있습니다.

이 언어 변경 사항을 사용하는 방법에 대한 자세한 내용은 [LoopvarExperiment 위키 페이지](/wiki/LoopvarExperiment)를 참조하십시오.

<!-- https://go.dev/issue/25448 -->

Go 1.21에서 goroutine이 panicking 되고, recover가 직접으로 deferred 함수에서 호출되면, recover의 반환 값이 반드시 nil이 아님을 정의합니다. 이를 보장하기 위해, nil 인터페이스 값(또는 유형이 지정되지 않은 nil)으로 panic을 호출하면 런타임에 `*runtime.PanicNilError` 유형의 panicking이 발생합니다.

오래된 버전의 Go로 작성된 프로그램의 경우, `GODEBUG=panicnil=1`을 설정하여 nil 패닉을 다시 활성화할 수 있습니다.
이 설정은 메인 패키지가 `go` `1.20` 또는 이전 버전을 선언하는 모듈에 있는 프로그램을 컴파일할 때 자동으로 활성화됩니다.

## 도구 {#tools}

Go 1.21은 Go 도구 체인에서 향상된 역방향 호환성 및 전방향 호환성을 추가합니다.

<!-- https://go.dev/issue/56986 -->
역호환성을 개선하기 위해, Go 1.21은 Go가 [호환성 정책](/doc/go1compat)에 따라 변경 사항을 제어하기 위해 `GODEBUG` 환경 변수를 사용하는 것을 공식화합니다.
이 변경 사항은 기존 프로그램을 중단시킬 수 있지만, 일반적으로 중단하는 변경 사항으로 간주되지 않습니다.
(예를 들어, 버그에 의존하는 프로그램은 버그가 수정될 때 중단될 수 있지만, 버그 수정은 중단하는 변경 사항으로 간주되지 않습니다.)
Go가 이러한 종류의 동작 변경을 해야 할 때,
이제 `go` 라인이 워크스페이스의 `go.work` 파일 또는 메인 모듈의 `go.mod` 파일에 설정된 버전에 따라 이전 동작과 새 동작 중 하나를 선택합니다.
새 Go 툴체인으로 업그레이드하되 `go` 라인이 원래 (더 이전) Go 버전으로 유지하면, 이전 툴체인의 동작을 유지할 수 있습니다.
이 호환성 지원을 통해 최신 Go 툴체인은 항상 이전 버전의 Go의 가장 최신, 가장 안전한 구현이어야 합니다.
자세한 내용은 “[Go, 역호환성, 및 GODEBUG](/doc/godebug)”를 참조하십시오.

<!-- https://go.dev/issue/57001 -->
Go 1.21에서 전방 호환성을 개선하기 위해, `go` 라인은 `go.work` 또는 `go.mod` 파일에서 엄격한 최소 요구 사항으로 읽습니다.
`go` `1.21.0`은 워크스페이스 또는 모듈이 Go 1.20 또는 Go 1.21rc1과 함께 사용할 수 없음을 의미합니다.
이를 통해 Go의 후속 버전에서 구현된 수정 사항에 의존하는 프로젝트는, 이전 버전에서는 사용되지 않도록 보장할 수 있습니다.
또한, 새로운 Go 기능을 사용하는 프로젝트에 대한 더 나은 오류 보고를 제공합니다.
문제는 최신 Go 버전이 필요할 때, 코드 빌드를 시도하고 해결되지 않은 import 또는 구문 오류에 대한 오류를 출력하는 대신, 명확하게 보고됩니다.

이를 통해 새로운 엄격한 버전 요구 사항을 더 쉽게 관리할 수 있습니다.
`go` 명령은 이제 자체 배포에 포함된 도구 체뿐만 아니라 PATH에 있는 다른 Go 도구 체 버전이나 필요에 따라 다운로드한 다른 Go 도구 체 버전을 호출할 수 있습니다.
`go.mod` 또는 `go.work` 파일에서 Go의 최신 버전의 최소 요구 사항을 선언하는 경우, `go` 명령은 해당 버전을 자동으로 찾아서 실행합니다.
새로운 `toolchain` 지침은 사용할 권장 최소 도구 체를 설정하며, 이는 엄격한 `go`의 최소 버전보다 최신 버전일 수 있습니다.
자세한 내용은 “[Go 도구 체](/doc/toolchain)”를 참조하십시오.

### Go 명령어 {#go-명령어}

<!-- https://go.dev/issue/58099, CL 474236 -->
`-pgo` 빌드 플래그는 기본적으로 `-pgo=auto`로 설정되었으며, 명령줄에서 단일 메인 패키지를 지정하는 제한이 제거되었습니다. 메인 패키지 디렉토리에 `default.pgo`라는 이름의 파일이 존재하면, `go` 명령은 해당 프로그램을 빌드할 때 프로파일 가이드 최적화를 활성화하기 위해 이를 사용합니다.

`-C` `dir` 플래그는 이제 명령줄에서 사용될 때 항상 첫 번째 플래그여야 합니다.

<!-- https://go.dev/issue/37708, CL 463837 -->
새로운 `go test` 옵션
`-fullpath`는 테스트 로그 메시지에 기본 이름 대신 전체 경로 이름을 출력합니다.

<!-- https://go.dev/issue/15513, CL 466397 -->
`go test` 명령의 `-c` 플래그는 이제 여러 패키지에 대한 테스트 바이너리를 생성할 수 있으며, 각 바이너리는 `pkg.test`에 저장됩니다. 여기서 `pkg`는 패키지 이름입니다. 컴파일 중인 테스트 패키지 중 동일한 패키지 이름을 가진 패키지가 하나 이상이면 오류가 발생합니다.

<!-- https://go.dev/issue/15513, CL 466397 -->
`go` `test` 명령어의 `-o` 플래그는 이제 디렉터리 인수를 받습니다. 이 경우, 테스트 실행 파일은 현재 디렉터리 대신 지정된 디렉터리에 작성됩니다.

<!-- https://go.dev/issue/31544, CL 477839 -->
외부 (C) 링커를 사용하고 cgo가 활성화된 경우, `runtime/cgo` 패키지는 Go 링커에 추가 의존성으로 제공되어 Go 런타임이 C 링커에 의해 추가된 모든 라이브러리와 호환되도록 보장합니다.

### Cgo {#cgo}

<!-- CL 490819 -->
`import "C"`를 사용하는 파일에서, Go 도구는 이제 C 유형에 Go 메서드를 선언하려는 시도에 대해 올바르게 오류를 보고합니다.

## 실행 시 변경 {#runtime-changes}

<!-- https://go.dev/issue/7181 -->
매우 깊은 스택을 출력할 때, 런타임은 이제 처음 50개 (가장 안쪽) 프레임과 그 아래 50개 (가장 바깥쪽) 프레임을 출력합니다.
단지 처음 100개 프레임을 출력하는 대신 말입니다. 이렇게 하면 재귀적으로 깊은 스택이 어떻게 시작되었는지 더 쉽게 알 수 있으며, 특히 스택 오버플로우 디버깅에 유용합니다.

<!-- https://go.dev/issue/59960 -->
Linux 플랫폼에서 투명한 큰 페이지를 지원하는 경우, Go 런타임은 이제 힙의 어떤 부분이 큰 페이지를 사용할 수 있는지 보다 명시적으로 관리합니다. 이는 메모리 사용량 개선으로 이어집니다. 작은 힙은 메모리 사용량이 줄어들어야 합니다 (이상적인 경우 최대 50% 감소). 반면, 큰 힙은 힙의 밀집된 부분에 대한 깨진 큰 페이지 수를 줄여 CPU 사용량과 지연 시간을 최대 1%까지 향상시킬 수 있습니다. 이러한 변경의 결과로, 런타임은 특정 문제 있는 Linux 구성 설정을 더 이상 사용하지 않습니다. 이는 메모리 오버헤드가 증가할 수 있습니다. 권장되는 해결책은 OS의 큰 페이지 설정을 [GC 가이드](/doc/gc-guide#Linux_transparent_huge_pages)에 따라 조정하는 것입니다. 그러나 다른 해결 방법도 있습니다. `max_ptes_none` 섹션을 참조하십시오. (/doc/gc-guide#Linux_THP_max_ptes_none_workaround)

<!-- https://go.dev/issue/57069, https://go.dev/issue/56966 -->
실시간 내부 가비지 컬렉션 튜닝 결과,
애플리케이션은 애플리케이션의 마지막 작업 지연 시간을 최대 40% 감소시키고, 메모리 사용량은 약간 감소할 수 있습니다. 일부 애플리케이션은 처리량 측면에서 약간의 손실을 경험할 수도 있습니다.
메모리 사용량 감소는 처리량 손실과 비례하여야 하며, 이전 릴리스의 처리량/메모리 효율성을 회복할 수 있습니다 (지연 시간에 큰 변화 없이). 이를 위해 `GOGC` 및/또는 `GOMEMLIMIT` 값을 약간 증가시킬 수 있습니다.

<!-- https://go.dev/issue/51676 -->
C에서 생성된 스레드에서 Go로 호출하는 경우, Go 실행을 위해 몇 가지 설정이 필요합니다. Unix 플랫폼에서는 동일한 스레드에서 여러 번 호출하는 경우에도 이러한 설정이 유지됩니다. 이는 이후 C에서 Go로의 호출에 필요한 오버헤드를 대략 1-3 마이크로초에서 100-200 나노초로 줄입니다.

## 컴파일러

프로파일 기반 최적화 (PGO), Go 1.20에서 미리보기로 추가된 기능이며, 이제 일반적인 사용을 위해 준비되었습니다. PGO는 프로덕션 워크로드의 프로파일을 통해 식별된 "핫" 코드에 대한 추가 최적화를 가능하게 합니다. [Go 명령어 섹션](#go-command)에서 언급했듯이, `default.pgo` 프로파일이 메인 패키지 디렉토리에 있는 바이너리에 PGO는 기본적으로 활성화됩니다. 성능 개선은 애플리케이션 동작에 따라 다르며, 대표적인 Go 프로그램 세트에서 2%에서 7% 정도의 성능 향상을 볼 수 있습니다. 자세한 내용은 [PGO 사용자 가이드](/doc/pgo)를 참조하십시오.

<!-- https://go.dev/issue/59959 -->

PGO 빌드는 이제 일부 인터페이스 메서드 호출을 데비추얼화할 수 있으며, 가장 일반적인 호출 대상에 구체적인 호출을 추가합니다. 이를 통해 추가적인 최적화가 가능해집니다. 예를 들어, 호출 대상 함수를 인라인할 수 있습니다.

<!-- CL 497455 -->

Go 1.21은 빌드 속도를 최대 6%까지 향상시켜, 주로 컴파일러 자체를 PGO (프로파일 기반 컴파일)로 빌드함으로써 달성했습니다.

## 어셈블러 {#assembler}

<!-- https://go.dev/issue/58378 -->

amd64 아키텍처에서, frameless nosplit 어셈블리 함수는 자동으로 `NOFRAME`로 표시되지 않습니다.
대신, 원하는 경우 `NOFRAME` 속성을 명시적으로 지정해야 합니다.
이는 이미 다른 아키텍처(프레임 포인터를 지원하는 경우)에서 사용되는 동작과 동일합니다.
이로 인해 런타임은 스택 전환을 위한 프레임 포인터를 유지합니다.

<!-- CL 476295 -->

`R15`의 잘못된 사용을 검사하는 검증기가 amd64에서 동적 링크 시에 개선되었습니다.

## 링커 {#linker}

<!-- https://go.dev/issue/57302, CL 461749, CL 457455 -->
Windows/amd64에서 링커 (컴파일러의 도움을 받아)는 기본적으로 SEH 언윈딩 데이터를 생성합니다. 이를 통해 Go 애플리케이션이 Windows 디버거 및 기타 도구와 더 잘 통합됩니다.

<!-- CL 463395, CL 461315 -->

Go 1.21에서 링커 (컴파일러의 도움을 받아)는 충분히 큰 개수만큼의 항목이 변수 초기화에 존재하고, 초기화 표현식이 부작용이 없는 경우, 사용되지 않는 (참조되지 않는) 전역 맵 변수를 삭제할 수 있습니다.

## 표준 라이브러리 {#library}

### 새로운 log/slog 패키지 {#slog}

```go
package slog

// Logger는 로깅 메시지를 기록하는 인터페이스입니다.
type Logger interface {
    // Info는 정보를 기록하는 메서드입니다.
    Info(string)
    // Warn은 경고를 기록하는 메서드입니다.
    Warn(string)
    // Error는 오류를 기록하는 메서드입니다.
    Error(string)
    // Info는 정보를 기록하는 메서드입니다.
    Info(string, string)
    // Warn은 경고를 기록하는 메서드입니다.
    Warn(string, string)
    // Error는 오류를 기록하는 메서드입니다.
    Error(string, string)
}
```

<!--
 https://go.dev/issue/59060, https://go.dev/issue/59141, https://go.dev/issue/59204, https://go.dev/issue/59280,
        https://go.dev/issue/59282, https://go.dev/issue/59339, https://go.dev/issue/59345, https://go.dev/issue/61200,
        CL 477295, CL 484096, CL 486376, CL 486415, CL 487855, CL 508195
 -->
새로운 [log/slog](/pkg/log/slog) 패키지는 레벨과 함께 구조화된 로깅을 제공합니다.
구조화된 로깅은 키-값 쌍을 통해 대량의 로그 데이터를 빠르게, 정확하게 처리할 수 있도록 합니다.
이 패키지는 인기 있는 로깅 분석 도구 및 서비스와의 통합을 지원합니다.

### 새로운 testing/slogtest 패키지 {#slogtest}

<!-- CL 487895 -->
새로운 [testing/slogtest](/pkg/testing/slogtest) 패키지는 [slog.Handler](/pkg/log/slog#Handler) 구현을 검증하는 데 도움이 될 수 있습니다.

### 새로운 슬라이스 패키지 {#slices}

<!-- https://go.dev/issue/45955, https://go.dev/issue/54768 -->
<!-- https://go.dev/issue/57348, https://go.dev/issue/57433 -->
<!-- https://go.dev/issue/58565, https://go.dev/issue/60091 -->
<!-- https://go.dev/issue/60546 -->
<!-- CL 467417, CL 468855, CL 483175, CL 496078, CL 498175, CL 502955 -->
새로운 [slices](/pkg/slices) 패키지는 다양한 슬라이스 관련 작업을 제공하며, 모든 요소 유형의 슬라이스와 함께 작동하는 일반 함수를 사용합니다.

### 새로운 맵스 패키지 {#maps}

<!-- https://go.dev/issue/57436, CL 464343 -->
새로운 [maps](/pkg/maps/) 패키지는 다양한 맵 관련 작업을 제공하며, 맵의 키 또는 요소 유형에 관계없이 작동하는 제네릭 함수를 사용합니다.

### 새로운 cmp 패키지 {#cmp}

<!-- https://go.dev/issue/59488, CL 496356 -->
새로운 [cmp](/pkg/cmp/) 패키지는 타입 제약 [`Ordered`](/pkg/cmp/#Ordered)을 정의하고,
두 개의 새로운 제네릭 함수인
[`Less`](/pkg/cmp/#Less)
와 [`Compare`](/pkg/cmp/#Compare)를 제공하며,
이는 [정렬된
타입](/ref/spec/#Comparison_operators)과 함께 사용하기에 유용합니다.

### 라이브러리의 미미한 변경 사항 {#minor_library_changes}

물론, 라이브러리에 다양한 미세한 변경 사항과 업데이트가 있으며, 이는 Go 1의 [호환성](https://docs.example.com/go1compat)을 염두에 두고 만들어졌습니다.
또한, 여기에는 나열되지 않은 다양한 성능 개선 사항이 있습니다.

#### [archive/tar](/pkg/archive/tar/)

<!-- https://go.dev/issue/54451, CL 491175 -->
`io/fs.FileInfo` 인터페이스를 반환하는
[`Header.FileInfo`](/pkg/archive/tar/#Header.FileInfo)
의 구현이 이제
[`io/fs.FormatFileInfo`](/pkg/io/fs/#FormatFileInfo)를 호출하는
`String` 메서드를 구현합니다.

<!-- archive/tar -->

#### [archive/zip](/pkg/archive/zip/)

<!-- https://go.dev/issue/54451, CL 491175 -->
`io/fs.FileInfo` 인터페이스를 반환하는
[`FileHeader.FileInfo`](/pkg/archive/zip/#FileHeader.FileInfo)
의 구현이 이제 `String` 메서드를 구현하여
[`io/fs.FormatFileInfo`](/pkg/io/fs/#FormatFileInfo)를 호출합니다.

<!-- https://go.dev/issue/54451, CL 491175 -->
`io/fs.DirEntry` 인터페이스의 구현,
`/pkg/io/fs/#DirEntry`
은 `io/fs.ReadDirFile.ReadDir`
메서드의 반환값인
`/pkg/io/fs/#File`
인
`Reader.Open`
의 결과에서 반환되는
[`io/fs.File`](/pkg/io/fs/#File)
이제
`String`
메서드를 구현하고,
`io/fs.FormatDirEntry`
를 호출합니다.

<!-- archive/zip -->

#### [bytes](/pkg/bytes/)

<!-- https://go.dev/issue/53685, CL 474635 -->
`Buffer` 타입
에는 두 가지 새로운 메서드가 추가되었습니다:
`Available`
(`pkg/bytes/#Buffer.Available`)
및
`AvailableBuffer`
(`pkg/bytes/#Buffer.AvailableBuffer`).
이 메서드는 `Write`
메서드와 함께 사용하여 `Buffer`에 직접 추가할 수 있습니다.

<!-- 바이트 -->

#### [context](/pkg/context/)

<!-- https://go.dev/issue/40221, CL 479918 -->
새로운 `WithoutCancel` 함수는 원본 컨텍스트가 취소될 때, 해당 컨텍스트를 취소하지 않고 복사본을 반환합니다.

<!-- https://go.dev/issue/56661, CL 449318 -->
새로운 `WithDeadlineCause` 및 `WithTimeoutCause` 함수는 데드라인 또는 타임아웃이 만료될 때 컨텍스트 취소 이유를 설정하는 방법을 제공합니다. 이 이유를 `Cause` 함수를 사용하여 가져올 수 있습니다.

<!-- https://go.dev/issue/57928, CL 482695 -->
새로운 `AfterFunc` 함수는 컨텍스트가 취소된 후 실행될 함수를 등록합니다.

<!-- CL 455455 -->
최적화란 `Background` 및 `TODO`를 호출하고, 이를 공유 유형으로 변환한 결과가 동일하게 취급될 수 있다는 의미입니다. 이전 버전에서는 항상 다르게 취급되었습니다. `Context` 값을 비교하여 동등성을 확인하는 것은 명확하게 정의되지 않았으므로, 이는 호환되지 않는 변경 사항으로 간주되지 않습니다.

```
#### [crypto/ecdsa](/pkg/crypto/ecdsa/)
```

<!-- CL 492955 -->
[`PublicKey.Equal`](/pkg/crypto/ecdsa/#PublicKey.Equal) 및
[`PrivateKey.Equal`](/pkg/crypto/ecdsa/#PrivateKey.Equal)
이제 상수 시간으로 실행됩니다.

```markdown
<!-- crypto/ecdsa -->
```

```
#### [crypto/elliptic](/pkg/crypto/elliptic/)
```

<!-- CL 459977 -->
`Curve` 패키지의 모든 메서드(`Curve`)가 함께 폐기되었으며, `GenerateKey`, `Marshal`, `Unmarshal`도 폐기되었습니다. ECDH 작업의 경우, 새로운 `crypto/ecdh` 패키지를 사용해야 합니다. 더 낮은 수준의 작업의 경우, `filippo.io/nistec`와 같은 타사 모듈을 사용하십시오.

<!-- crypto/elliptic -->

#### [crypto/rand](/pkg/crypto/rand/)

<!-- CL 463123 -->
`crypto/rand` 패키지는 NetBSD 10.0 이상에서 `getrandom` 시스템 호출을 사용합니다.

<!-- crypto/rand -->

#### [crypto/rsa](/pkg/crypto/rsa/)

<!-- CL 471259, CL 492935 -->
`GOARCH=amd64` 및 `GOARCH=arm64`에서 프라이빗 RSA 연산(복호화 및 서명)의 성능이 Go 1.19보다 향상되었습니다. Go 1.20에서는 성능이 저하되었습니다.

[`PrecomputedValues`](/pkg/crypto/rsa/#PrecomputedValues)에 프라이빗 필드를 추가했기 때문에, 이전에 미리 계산된 프라이빗 키를 JSON과 같은 형식으로 디시리즈(예: JSON에서)할 때도 최적의 성능을 위해 `PrivateKey.Precompute`](/pkg/crypto/rsa/#PrivateKey.Precompute)를 호출해야 합니다.

<!-- CL 492955 -->
[`PublicKey.Equal`](/pkg/crypto/rsa/#PublicKey.Equal) 및
[`PrivateKey.Equal`](/pkg/crypto/rsa/#PrivateKey.Equal)
이제 상수 시간으로 실행됩니다.

<!-- https://go.dev/issue/56921, CL 459976 -->
`GenerateMultiPrimeKey` 함수와 `PrecomputedValues.CRTValues` 필드는 더 이상 사용되지 않습니다. `PrecomputedValues.CRTValues`는 `PrivateKey.Precompute`가 호출될 때 여전히 채워지지만, 이 값은 복호화 작업 중에 사용되지 않습니다.

<!-- crypto/rsa -->

<!-- CL 483815 취소됨 -->

#### [crypto/sha256](/pkg/crypto/sha256/)

<!-- https://go.dev/issue/50543, CL 408795 -->
SHA-224 및 SHA-256 연산이 `GOARCH=amd64`인 경우, 사용할 수 있는 경우 기본 명령어 사용하도록 변경되어 성능이 3-4배 향상되었습니다.

```markdown
<!-- crypto/sha256 -->
```

<!-- CL 481478이 되돌림 -->
<!-- CL 483816이 되돌림 -->

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 497895 -->
서버는 클라이언트 인증서(특히 [`Config.VerifyPeerCertificate`](/pkg/crypto/tls/#Config.VerifyPeerCertificate)가 실행되지 않는 경우)를 재연결 시 검증하지 않습니다. 또한 유효 기간만 확인합니다. 이렇게 하면 클라이언트 인증서가 사용될 때 세션 티켓의 크기가 커집니다. 클라이언트는 이미 재연결 시 검증을 건너뛰었지만, 이제 [`Config.InsecureSkipVerify`](/pkg/crypto/tls/#Config.InsecureSkipVerify)가 설정되어 있더라도 유효 기간을 확인합니다.

<!-- https://go.dev/issue/60105, CL 496818, CL 496820, CL 496822, CL 496821, CL 501675 -->
애플리케이션은 이제 세션 티켓의 내용을 제어할 수 있습니다.

- 새로운 [`SessionState`](/pkg/crypto/tls/#SessionState) 타입은
    재개 가능한 세션을 설명합니다.
  - [`SessionState.Bytes`](/pkg/crypto/tls/#SessionState.Bytes) 메서드와 [`ParseSessionState`](/pkg/crypto/tls/#ParseSessionState) 함수는 `SessionState`를 직렬화하고 역직렬화합니다.
  - [`Config.WrapSession`](/pkg/crypto/tls/#Config.WrapSession) 및 [`Config.UnwrapSession`](/pkg/crypto/tls/#Config.UnwrapSession) 훅은 서버 측에서 `SessionState`를 티켓으로 변환하고 역으로 변환합니다.
  - [`Config.EncryptTicket`](/pkg/crypto/tls/#Config.EncryptTicket) 및 [`Config.DecryptTicket`](/pkg/crypto/tls/#Config.DecryptTicket) 메서드는 `WrapSession` 및 `UnwrapSession`의 기본 구현을 제공합니다.
  - [`ClientSessionState.ResumptionState`](/pkg/crypto/tls/#ClientSessionState.ResumptionState) 메서드 및 [`NewResumptionState`](/pkg/crypto/tls/#NewResumptionState) 함수는 `ClientSessionCache` 구현에서 클라이언트 측에서 세션을 저장하고 재개하는 데 사용될 수 있습니다.

<!-- CL 496817 -->
세션 티켓이 연결 간 추적 메커니즘으로 사용될 가능성을 줄이기 위해, 서버는 이제 연결 재개 시 (지원되고 비활성화되지 않은 경우) 새로운 티켓을 발급하고, 티켓에는 더 이상 암호화된 데 대한 키 식별자가 포함되지 않습니다. `Conn.SetSessionTicketKeys`에 많은 수의 키를 전달하는 경우, 이는 눈에 띄는 성능 비용으로 이어질 수 있습니다.

<!-- CL 497376 -->
클라이언트와 서버 모두 확장된 마스터 시크릿 확장(RFC 7627)을 구현합니다.
`ConnectionState.TLSUnique`의 폐기가 되돌아갔으며, 이제 확장된 마스터 시크릿을 지원하는 재개된 연결에 대해 설정됩니다.

<!-- https://go.dev/issue/44886, https://go.dev/issue/60107, CL 493655, CL 496995, CL 514997 -->
새로운 [`QUICConn`](/pkg/crypto/tls/#QUICConn) 유형은 QUIC 구현을 지원하며, 0-RTT 지원도 포함합니다.
참고: 이것은 자체적인 QUIC 구현이 아니며, 0-RTT는 여전히 TLS에서 지원되지 않습니다.

<!-- https://go.dev/issue/46308, CL 497377 -->
새로운 `VersionName` 함수는
TLS 버전 번호에 대한 이름을 반환합니다.

<!-- https://go.dev/issue/52113, CL 410496 -->
서버에서 클라이언트 인증 실패에 대해 전송되는 TLS 경고 코드가 개선되었습니다. 이전에는 이러한 실패가 항상 "잘못된 인증서" 경고를 발생시켰습니다.
이제 특정 실패는 RFC 5246 및 RFC 8446에 정의된 더 적절한 경고 코드를 발생시킵니다:

- TLS 1.3 연결의 경우, 서버가 클라이언트 인증을 요구하도록 구성된 경우 (예:
    [RequireAnyClientCert](/pkg/crypto/tls/#RequireAnyClientCert) 또는
    [RequireAndVerifyClientCert](/pkg/crypto/tls/#RequireAndVerifyClientCert)),
    그리고 클라이언트가 인증서를 제공하지 않으면, 서버는 이제 "인증서 필요" 알림을 반환합니다.
  - 클라이언트가 서버에서 구성된 신뢰된 인증서 당국의 서명이 없는 인증서를 제공하는 경우, 서버는 "알 수 없는 인증서 당국" 알림을 반환합니다.
  - 클라이언트가 만료되었거나 아직 유효하지 않은 인증서를 제공하는 경우, 서버는 "만료된 인증서" 알림을 반환합니다.
  - 클라이언트 인증 실패와 관련된 모든 다른 시나리오에서, 서버는 여전히 "잘못된 인증서" 알림을 반환합니다.

<!-- crypto/tls -->

#### [crypto/x509](pkg/crypto/x509/)

<!-- https://go.dev/issue/53573, CL 468875 -->
[`RevocationList.RevokedCertificates`](/pkg/crypto/x509/#RevocationList.RevokedCertificates)가 더 이상 사용되지 않고 새로운 [`RevokedCertificateEntries`](/pkg/crypto/x509/#RevocationList.RevokedCertificateEntries) 필드로 대체되었습니다. 이 필드는 [`RevocationListEntry`](/pkg/crypto/x509/#RevocationListEntry) 슬라이스의 컬렉션입니다. [`RevocationListEntry`](/pkg/crypto/x509/#RevocationListEntry)는 [`pkix.RevokedCertificate`](/pkg/crypto/x509/pkix#RevokedCertificate)의 모든 필드와 함께, 또한 해지를 위한 이유 코드를 포함합니다.

<!-- CL 478216 -->
이름 제약이 이제 비-리프 인증서에 올바르게 적용되며,
적용된 인증서에는 적용되지 않습니다.

<!-- crypto/x509 -->

#### [debug/elf](/pkg/debug/elf/)

<!-- https://go.dev/issue/56892, CL 452617 -->
새로운
[`File.DynValue`](/pkg/debug/elf/#File.DynValue)
메서드는 주어진 동적 태그와 함께 나열된 숫자 값을 가져오는 데 사용될 수 있습니다.

<!-- https://go.dev/issue/56887, CL 452496 -->
`DT_FLAGS_1` 동적 태그에 허용되는 상수는 이제 `DynFlag1` 유형으로 정의됩니다.
이 태그는 `DF_1`으로 시작하는 이름을 가집니다.

<!-- CL 473256 -->
패키지는 이제 상수를 정의합니다.
[`COMPRESS_ZSTD`](/pkg/debug/elf/#COMPRESS_ZSTD).

<!-- https://go.dev/issue/60348, CL 496918 -->
이 패키지는 이제 상수를 정의합니다.
[`R_PPC64_REL24_P9NOTOC`](/pkg/debug/elf/#R_PPC64_REL24_P9NOTOC)

<!-- 디버깅/ELF -->

#### [debug/pe](/pkg/debug/pe/)

<!-- CL 488475 -->
초기화되지 않은 데이터가 포함된 섹션에서 읽으려고 시도할 때
`[Section.Data](/pkg/debug/pe/#Section.Data)`
또는 `[Section.Open](/pkg/debug/pe/#Section.Open)`에서 반환된 리더를 사용
하면 이제 오류가 반환됩니다.

<!-- 디버깅/PE -->

#### [embed](/pkg/embed/)

<!-- https://go.dev/issue/57803, CL 483235 -->
`io/fs.File`
객체,
`FS.Open`에서 반환되는
이제 `ReadAt` 메서드를
구현하여 `io.ReaderAt`를
사용할 수 있습니다.

<!-- https://go.dev/issue/54451, CL 491175 -->
`<code [FS.Open](/pkg/embed/FS.Open).[Stat](/pkg/io/fs/#File.Stat)</code>`를 호출하면 이제 `String`
메서드를 구현하는 유형이 반환됩니다. 이 메서드는
`[`io/fs.FormatFileInfo](/pkg/io/fs/#FormatFileInfo)`를 호출합니다.

<!-- 삽입 -->

#### [encoding/binary](/pkg/encoding/binary/)

<!-- https://go.dev/issue/57237, CL 463218, CL 463985 -->
새로운
[`NativeEndian`](/pkg/encoding/binary/#NativeEndian)
변수를 사용하면 현재 머신의 기본 바이트 순서에 따라 바이트 슬라이스와 정수 간의 변환을 수행할 수 있습니다.

<!-- encoding/binary -->

#### [errors](/pkg/errors/)

<!-- https://go.dev/issue/41198, CL 473935 -->
새로운
[`ErrUnsupported`](/pkg/errors/#ErrUnsupported)
오류는 요청된
작업이 수행되지 않을 수 있음을 나타내는 표준화된 방법을 제공합니다.
예를 들어, 하드 링크를 지원하지 않는 파일 시스템을 사용할 때
`os.Link`에 대한 호출입니다.

<!-- 오류 -->

#### [flag](/pkg/flag/)

<!-- https://go.dev/issue/53747, CL 476015 -->
새로운 [`BoolFunc`](/pkg/flag/#BoolFunc)
함수와
[`FlagSet.BoolFunc`](/pkg/flag/#FlagSet.BoolFunc)
메서드는 인수를 필요로 하지 않는 플래그를 정의하고, 플래그가 사용될 때 함수를 호출합니다. 이는 [`Func`](/pkg/flag/#Func)와 유사하지만, 부울 플래그에 사용됩니다.

<!-- CL 480215 -->
플래그 정의
(예: [`Bool`](/pkg/flag/#Bool),
[`BoolVar`](/pkg/flag/#BoolVar),
[`Int`](/pkg/flag/#Int),
[`IntVar`](/pkg/flag/#IntVar) 등)
`Set` 함수가 동일한 이름을 가진 플래그에 이미 호출된 경우에 멈추게 됩니다. 이 변경은 [초기화 순서의 변경](#language)로 인해 플래그 작업이 예상과 다른 순서로 발생할 수 있는 경우를 감지하기 위한 것입니다. 이 문제를 해결하는 방법은 대부분 플래그 정의를 올바르게 정렬하기 위해 명시적인 패키지 의존성을 추가하는 것입니다.

<!-- 깃발 -->

```
#### [go/ast](pkg/go/ast/)
```

<!-- https://go.dev/issue/28089, CL 487935 -->
새로운 `IsGenerated` 프레디케이트
(`/pkg/go/ast/#IsGenerated`)는 파일의 구문 트리가
[특별한 주석](/s/generatedcode)을 포함하는지
보고합니다. 이 주석은 일반적으로 파일이 도구에 의해 생성되었음을 나타냅니다.

<!-- https://go.dev/issue/59033, CL 476276 -->
새로운
[`File.GoVersion`](/pkg/go/ast/#File.GoVersion)
필드는 `//go:build` 또는 `// +build`
지시문에 의해 요구되는 최소 Go 버전을 기록합니다.

<!-- go/ast -->

#### [go/build](/pkg/go/build/)

<!-- https://go.dev/issue/56986, CL 453603 -->
이 패키지는 이제 파일 헤더 (패키지 선언 *앞*)에 있는 빌드 지시어 ( `//go:`로 시작하는 주석)를 파싱합니다. 이러한 지시어는 새
[`Package`](/pkg/go/build#Package) 필드인
[`Directives`](/pkg/go/build#Package.Directives),
[`TestDirectives`](/pkg/go/build#Package.TestDirectives),
그리고
[`XTestDirectives`](/pkg/go/build#Package.XTestDirectives)에서 사용할 수 있습니다.

<!-- go/build -->

#### [go/build/constraint](pkg/go/build/constraint/)

<!-- https://go.dev/issue/59033, CL 476275 -->
새로운
[`GoVersion`](/pkg/go/build/constraint/#GoVersion)
함수는 빌드 표현식에서 암시하는 최소 Go 버전을 반환합니다.

<!-- go/build/constraint -->

#### [go/token](pkg/go/token/)

<!-- https://go.dev/issue/57708, CL 464515 -->
새로운 `File.Lines` 메서드는
`File.SetLines`이 허용하는 동일한 형식으로 파일의 라인 번호 테이블을 반환합니다.

<!-- go/token -->

#### [go/types](/pkg/go/types/)

<!-- https://go.dev/issue/61175, CL 507975 -->
새로운 [`Package.GoVersion`](/pkg/go/types/#Package.GoVersion)
메서드는 패키지를 검사하는 데 사용된 Go 언어 버전을 반환합니다.

<!-- go/types -->

```
#### [hash/maphash](/pkg/hash/maphash/)
```

<!-- https://go.dev/issue/47342, CL 468795 -->
`hash/maphash` 패키지는 이제 순수 Go 구현을 제공하며, `purego` 빌드 태그를 사용하여 선택할 수 있습니다.

<!-- 해시/맵 해시 -->

#### [html/template](/pkg/html/template/)

<!-- https://go.dev/issue/59584, CL 496395 -->
새로운 오류
[`ErrJSTemplate`](/pkg/html/template/#ErrJSTemplate)
는 JavaScript 템플릿 내에서 액션이 나타날 때 반환됩니다. 이전에는 비공개 오류가 반환되었습니다.

<!-- html/템플릿 -->

#### [io/fs](/pkg/io/fs/)

<!-- https://go.dev/issue/54451, CL 489555 -->
새로운
[`FormatFileInfo`](/pkg/io/fs/#FormatFileInfo)
함수는
[`FileInfo`](/pkg/io/fs/#FileInfo)의 형식화된 버전을 반환합니다.
새로운
[`FormatDirEntry`](/pkg/io/fs/#FormatDirEntry)
함수는
[`DirEntry`](/pkg/io/fs/#FileInfo)의 형식화된 버전을 반환합니다.
`ReadDir`에 의해 반환되는
[`DirEntry`](/pkg/io/fs/#DirEntry)의 구현은
`String` 메서드를 구현하며, 이는
`FormatDirEntry`를 호출합니다.
이것은
`WalkDirFunc`에 전달되는
[`DirEntry`](/pkg/io/fs/#DirEntry) 값에도 적용됩니다.

<!-- io/fs -->

<!-- https://go.dev/issue/56491이 https://go.dev/issue/60519에 의해 되돌림됨 -->
<!-- CL 459435이 CL 467255에 의해 되돌림됨 -->
<!-- CL 467515이 CL 499416에 의해 되돌림됨 -->

#### [math/big](/pkg/math/big/)

<!-- https://go.dev/issue/56984, CL 453115, CL 500116 -->
새로운 `Int.Float64`
메서드는 멀티-정밀 정수에 가장 가까운 부동 소수점 값을 반환하며, 발생한 반올림에 대한 정보를 함께 제공합니다.

<!-- 수학/큰 -->

#### [net](/pkg/net/)

<!-- https://go.dev/issue/59166, https://go.dev/issue/56539 -->
<!-- CL 471136, CL 471137, CL 471140 -->
Linux에서 `net` 패키지는 커널이 지원하는 경우 Multipath TCP를 사용할 수 있습니다. 기본적으로 사용되지 않습니다. 클라이언트에서 Multipath TCP를 사용하려면, `Dialer.SetMultipathTCP` 메서드를 호출하기 전에 `Dialer.Dial` 또는 `Dialer.DialContext` 메서드를 호출합니다. 서버에서 Multipath TCP를 사용하려면, `ListenConfig.SetMultipathTCP` 메서드를 호출하기 전에 `ListenConfig.Listen` 메서드를 호출합니다. 네트워크를 `"tcp"`, `"tcp4"` 또는 `"tcp6"`로 지정합니다. Multipath TCP가 커널 또는 원격 호스트에서 지원되지 않으면, 연결은 자동으로 TCP로 전환됩니다. 특정 연결이 Multipath TCP를 사용하는지 테스트하려면 `TCPConn.MultipathTCP` 메서드를 사용합니다.

향후 Go 릴리스에서, 지원되는 시스템에서는 Multipath TCP를 기본적으로 활성화할 수 있습니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- CL 472636 -->
새로운 `ResponseController.EnableFullDuplex`
메서드는 서버 핸들러가 HTTP/1 요청 바디에서 동시에 읽고 응답을 쓰는 것을 허용합니다. 일반적으로 HTTP/1 서버는 응답을 쓰기 전에 요청 바디의 나머지 부분을 자동으로 소비하여, 응답을 읽기 전에 완전한 요청을 쓰려고 시도하는 클라이언트의 블로킹을 방지합니다. `EnableFullDuplex` 메서드는 이러한 동작을 비활성화합니다.

<!-- https://go.dev/issue/44855, CL 382117 -->
새로운 `ErrSchemeMismatch` 오류는 `Client` 및 `Transport`에서 HTTPS 요청에 대해 서버가 HTTP 응답을 반환할 때 반환됩니다.

<!-- CL 494122 -->
`net/http` 패키지가 이제 [`errors.ErrUnsupported`](/pkg/errors/#ErrUnsupported)를 지원합니다.
구체적으로,
`errors.Is(http.ErrNotSupported, errors.ErrUnsupported)`
라는 표현은 `true`를 반환합니다.

<!-- net/http -->

```
#### [os](/pkg/os/)
```

<!-- https://go.dev/issue/32558, CL 219638 -->
프로그램은 이제 빈 `time.Time` 값을 `Chtimes` 함수에 전달하여 액세스 시간 또는 수정 시간을 변경하지 않도록 할 수 있습니다.

<!-- CL 480135 -->
Windows에서
[`File.Chdir`](/pkg/os#File.Chdir) 메서드는
현재 디렉토리를 파일로 변경하고,
항상 오류를 반환하는 대신 동작합니다.

<!-- CL 495079 -->
유닉스 시스템에서, 비동기 디스크립터가 [`NewFile`](/pkg/os/#NewFile)에 전달될 경우,
`File.Fd` 메서드를 호출하면 이제 비동기 디스크립터가 반환됩니다. 이전에는 디스크립터가 블로킹 모드로 변환되었습니다.

<!-- CL 477215 -->
Windows에서 호출 시
[`Truncate`](/pkg/os/#Truncate)를 사용하여
존재하지 않는 파일에 호출하면, 빈 파일을 생성합니다. 이제 파일이 존재하지 않는다는
오류를 반환합니다.

<!-- https://go.dev/issue/56899, CL 463219 -->
Windows에서 `TempDir`을 호출할 때, `GetTempPath2W`를 사용할 수 있는 경우 `GetTempPathW` 대신 사용합니다.
이 새로운 동작은 SYSTEM으로 실행되는 프로세스가 생성한 임시 파일을 다른 프로세스가 접근하는 것을 방지하는 보안 강화 조치입니다.

<!-- CL 493036 -->
Windows에서 os 패키지는 이제 이름이 UTF-16로 저장되어 UTF-8로 유효하게 표현되지 않는 파일과 함께 작업할 수 있습니다.

<!-- CL 463177 -->
Windows에서 [`Lstat`](/pkg/os/#Lstat)이 이제 경로가 경로 구분자로 끝나는 심볼릭 링크를 해결하여, POSIX 플랫폼에서와 동일한 방식으로 동작합니다.

<!-- https://go.dev/issue/54451, CL 491175 -->
`io/fs.DirEntry` 인터페이스를 반환하는
[`ReadDir`](/pkg/os/#ReadDir) 함수와
`File.ReadDir` 메서드의 구현이 이제
`String` 메서드를 구현하여
[`io/fs.FormatDirEntry`](/pkg/io/fs/#FormatDirEntry)를 호출합니다.

<!-- https://go.dev/issue/53761, CL 416775, CL 498015-->
`io/fs.FS` 인터페이스를 반환하는
`DirFS` 함수의 구현이 이제
`io/fs.ReadFileFS` 및
`io/fs.ReadDirFS` 인터페이스를 구현합니다.

<!-- os -->

#### [경로/파일 경로](/pkg/path/filepath/)

다음과 같이 구현된
[`io/fs.DirEntry`](/pkg/io/fs/#DirEntry)
인터페이스가
[`WalkDir`](/pkg/path/filepath/#WalkDir)
함수의 인수로 전달되면,
[`io/fs.FormatDirEntry`](/pkg/io/fs/#FormatDirEntry)
를 호출하는
`String`
메서드를 구현합니다.

<!-- path/경로 -->

<!-- CL 459455 취소됨 -->

```
#### [reflect](/pkg/reflect/)
```

<!-- CL 408826, CL 413474 -->
Go 1.21에서, [`ValueOf`](/pkg/reflect/#ValueOf) 함수는 더 이상 인수를 힙에 할당하도록 강제하지 않으므로, `Value`의 내용을 스택에 할당할 수 있습니다. 대부분의 `Value`에 대한 작업도, 기본 값을 스택에 할당하도록 허용합니다.

<!-- https://go.dev/issue/55002 -->
새로운 `Value` [`Value.Clear`](/pkg/reflect/#Value.Clear)
메서드는 맵의 내용을 지우거나 슬라이스의 내용을 0으로 초기화합니다.
이는 언어에 추가된 새로운 `clear` 내장 기능과 일치합니다. [언어](#language)

<!-- https://go.dev/issue/56906, CL 452762 -->
`SliceHeader`
(`pkg/reflect/#SliceHeader`)
와 `StringHeader`
(`pkg/reflect/#StringHeader`)
타입은 이제 사용되지 않습니다. 새 코드에서는
`unsafe.Slice`
(`pkg/unsafe/#Slice`),
`unsafe.SliceData`
(`pkg/unsafe/#SliceData`),
`unsafe.String`
(`pkg/unsafe/#String`),
또는 `unsafe.StringData`
(`pkg/unsafe/#StringData`)를 사용하는 것을 권장합니다.

<!-- 반영 -->

#### [regexp](/pkg/regexp/)

<!-- https://go.dev/issue/46159, CL 479401 -->
`Regexp`는 이제
[`MarshalText`](/pkg/regexp#Regexp.MarshalText)
및
[`UnmarshalText`](/pkg/regexp#Regexp.UnmarshalText)
메서드를 정의합니다. 이러한 메서드는
[`encoding.TextMarshaler`](/pkg/encoding#TextMarshaler)
및
[`encoding.TextUnmarshaler`](/pkg/encoding#TextUnmarshaler)
을 구현하며, `encoding/json`과 같은 패키지에서 사용됩니다.

<!-- 정규 표현식 -->

#### [runtime](pkg/runtime/)

<!-- https://go.dev/issue/38651, CL 435337 -->
Go 프로그램에서 생성되는 텍스트 기반의 스택 트레이스, 예를 들어 충돌 발생 시, `runtime.Stack`을 호출하거나 `debug=2`를 사용하여 고루틴 프로파일을 수집할 때 생성되는 스택 트레이스에는 이제 각 스택 트레이스에 생성된 고루틴의 ID가 포함됩니다.

<!-- https://go.dev/issue/57441, CL 474915 -->
Go 애플리케이션이 충돌하는 경우, Windows Error Reporting (WER)를 활성화하기 위해 환경 변수 `GOTRACEBACK=wer`를 설정하거나, 충돌 발생 전에 [`debug.SetTraceback("wer")`](/pkg/runtime/debug/#SetTraceback)를 호출할 수 있습니다. WER를 활성화하는 것 외에도, `GOTRACEBACK=crash`와 동일하게 동작합니다.
Windows 시스템이 아닌 경우, `GOTRACEBACK=wer`는 무시됩니다.

<!-- CL 447778 -->
`GODEBUG=cgocheck=2`, cgo 포인터 전달 규칙을 철저하게 검사하는 기능은 더 이상 [디버깅 옵션](/pkg/runtime#hdr-Environment_Variables)으로 사용되지 않습니다.
대신 `GOEXPERIMENT=cgocheck2`를 사용하여 실험 기능을 사용할 수 있습니다.
특히, 이 모드는 시작 시가 아닌 빌드 시간에 선택해야 합니다.

`GODEBUG=cgocheck=1`은 여전히 사용 가능하며 (그리고 기본값으로 유지됩니다).

<!-- https://go.dev/issue/46787, CL 367296 -->
런타임 패키지에 새로운 유형 `Pinner`가 추가되었습니다. `Pinner`는 Go 메모리를 "잠금"하여, 다른 Go 코드가 더 자유롭게 사용할 수 있도록 하는 데 사용될 수 있습니다. 예를 들어, 잠긴 Go 메모리를 참조하는 Go 값을 C 코드에 전달하는 것이 이제 허용됩니다. 이전에는 이러한 중첩된 참조를 전달하는 것은 [cgo 포인터 전달 규칙](https://pkg.go.dev/cmd/cgo#hdr-Passing_pointers)에 의해 금지되었습니다. 자세한 내용은 [문서](/pkg/runtime#Pinner)를 참조하십시오.

<!-- CL 472195, 릴리스 노트 필요 없음 -->

<!-- runtime -->

#### [runtime/metrics](/pkg/runtime/metrics/)

<!-- https://go.dev/issue/56857, CL 497315 -->
이전에는 내부적으로만 사용되던 GC 메트릭 중 일부, 예를 들어 "라이브 힙 크기"가 이제 사용 가능합니다.
`GOGC` 및 `GOMEMLIMIT` 또한 메트릭으로 사용 가능합니다.

<!-- 성능 지표 -->

#### [runtime/trace](/pkg/runtime/trace/)

<!-- https://go.dev/issue/16638 -->
amd64 및 arm64에서 추적을 수집하는 데 필요한 CPU 비용이 크게 줄었습니다: 이전 버전보다 최대 10배 개선되었습니다.

<!-- CL 494495 -->
이제 추적 정보에는 Go 런타임이 중단할 수 있는 모든 이유에 대한 명시적인 "스톱 더 월드" 이벤트가 포함됩니다. 이는 단순히 가비지 컬렉션뿐만 아니라 모든 경우에 적용됩니다.

<!-- runtime/trace -->

#### [sync](/pkg/sync/)

<!-- https://go.dev/issue/56102, CL 451356 -->
새로운 `OnceFunc` (/[pkg/sync/#OnceFunc]),
`OnceValue` (/[pkg/sync/#OnceValue]),
및 `OnceValues` (/[pkg/sync/#OnceValues])
함수는 [Once](/pkg/sync/#Once)의 일반적인 사용 사례인, 첫 번째 사용 시에 값을 비동기적으로 초기화하는 것을 캡처합니다.

#### [syscall](/pkg/syscall/)

<!-- CL 480135 -->
Windows에서
[`Fchdir`](/pkg/syscall#Fchdir) 함수는 이제 인자를 기준으로 현재 디렉토리를 변경하며, 더 이상 항상 오류를 반환하지 않습니다.

<!-- https://go.dev/issue/46259, CL 458335 -->
FreeBSD에서
[`SysProcAttr`](/pkg/syscall#SysProcAttr)
에는 새로운 필드 `Jail`이 추가되었으며, 이를 사용하여 새로 생성된 프로세스를 격리된 환경으로 설정할 수 있습니다.

<!-- CL 493036 -->
Windows에서 `syscall` 패키지는 이제 UTF-16로 저장된 파일 이름을 유효한 UTF-8로 표현할 수 없는 파일과 함께 작동할 수 있습니다.
`UTF16ToString` ([/pkg/syscall#UTF16ToString](https://simonsapin.github.io/wtf-8/)) 및 `UTF16FromString` ([/pkg/syscall#UTF16FromString](https://simonsapin.github.io/wtf-8/)) 함수는 이제 UTF-16 데이터를 WTF-8 문자열과 변환합니다.
이는 WTF-8가 이전 버전에서 사용된 UTF-8 형식의 상위 집합이기 때문에 이전 버전과의 호환성을 유지합니다.

<!-- CL 476578, CL 476875, CL 476916 -->
여러 오류 값들이 새로운
[`errors.ErrUnsupported`](/pkg/errors/#ErrUnsupported)와 일치합니다.
따라서 `errors.Is(err, errors.ErrUnsupported)`는 `true`를 반환합니다.

- `ENOSYS`
  - `ENOTSUP`
  - `EOPNOTSUPP`
  - `EPLAN9` (Plan 9 전용)
  - `ERROR_CALL_NOT_IMPLEMENTED` (Windows 전용)
  - `ERROR_NOT_SUPPORTED` (Windows 전용)
  - `EWINDOWS` (Windows 전용)

<!-- syscall -->

#### [테스팅](/pkg/testing/)

<!-- https://go.dev/issue/37708, CL 463837 -->
새로운 `-test.fullpath` 옵션은 테스트 로그 메시지에 기본 이름뿐만 아니라 전체 경로 이름을 출력합니다.

<!-- https://go.dev/issue/52600, CL 475496 -->
새로운 `Testing` 함수는 프로그램이 `go test`로 생성된 테스트인지 여부를 보고합니다.

<!-- 테스트 -->

```
#### [testing/fstest](/pkg/testing/fstest/)
```

<!-- https://go.dev/issue/54451, CL 491175 -->
`<code [Open](/pkg/testing/fstest/MapFS.Open).[Stat](/pkg/io/fs/#File.Stat)</code>`를 호출하면 이제 `String`
메서드를 구현하는 타입이 반환됩니다. 이 메서드는
`[`io/fs.FormatFileInfo`](/pkg/io/fs/#FormatFileInfo)를 호출합니다.

<!-- 테스트/fstest -->

#### [unicode](/pkg/unicode/)

<!-- CL 456837 -->
`[unicode`](/pkg/unicode/) 패키지와
전체 시스템 내의 관련 지원이
[Unicode 15.0.0](https://www.unicode.org/versions/Unicode15.0.0/)로 업그레이드되었습니다.

<!-- unicode -->

## 포트

### 다윈

```
# 다윈
```

<!-- https://go.dev/issue/57125 -->
[공지](go1.20#darwin)된 바와 같이,
Go 1.21은 macOS 10.15 카탈리나 또는 이후 버전을 필요로 합니다;
이전 버전 지원은 중단되었습니다.

### Windows
```
{#windows}
```

<!-- https://go.dev/issue/57003, https://go.dev/issue/57004 -->
Go 1.20의 릴리스 노트에 발표된 바와 같이,
Go 1.21은 최소 Windows 10 또는 Windows Server 2016을 필요로 하며, 이전 버전 지원은 중단되었습니다.

### ARM

<!-- CL 470695 -->

`GOARCH=arm`로 Go 배포본을 빌드할 때, ARM 시스템이 아닌 환경에서 빌드하는 경우 (즉, ARM용 크로스 컴파일러를 빌드하는 경우), `GOARM` 환경 변수의 기본값은 이제 항상 `7`로 설정됩니다.
이전에는 기본값이 빌드 시스템의 특성에 따라 결정되었습니다.

크로스 컴파일러를 빌드하지 않을 때, 기본값은 빌드 시스템을 검사하여 결정됩니다.
이는 이전 버전과 Go 1.21에서도 동일하게 적용됩니다.
변경된 부분은 크로스 컴파일러를 빌드할 때의 동작입니다.

### WebAssembly {#wasm}

WebAssembly (Wasm)는 웹 브라우저에서 실행되는 중간 표현 형식입니다. C, C++, Rust 등 다양한 언어로 작성된 코드를 컴파일하여 Wasm으로 변환한 후, 웹 브라우저에서 실행할 수 있습니다.

```
// Example Wasm code (simplified)
(module
  (func $my_func (param i32) (returns i32)
    (result i32)
    i32.add i32.const 1 i32.const 2
  )
)
```

**장점:**

*   **성능:** 네이티브 코드에 가까운 성능을 제공합니다.
*   **보안:** 웹 브라우저 내에서 격리된 환경에서 실행되므로 보안에 유리합니다.
*   **다양한 언어 지원:** C, C++, Rust 등 다양한 언어로 작성된 코드를 지원합니다.
*   **크로스 플랫폼:** 다양한 운영체제 및 브라우저에서 실행 가능합니다.

**활용 분야:**

*   고성능 게임
*   3D 그래픽
*   실시간 데이터 처리
*   웹 애플리케이션 성능 향상

**참고 자료:**

*   [WebAssembly 공식 웹사이트](https://webassembly.org/)
*   [WebAssembly Tutorial](https://developer.mozilla.org/ko/docs/Web/Web_Assembly)

<!-- https://go.dev/issue/38248, https://go.dev/issue/59149, CL 489255 -->
새로운 `go:wasmimport` 지시어를 사용하여 Go 프로그램에서 WebAssembly 호스트의 함수를 가져올 수 있습니다.

<!-- https://go.dev/issue/56100 -->

이제 Go 스케줄러는 JavaScript 이벤트 루프와 훨씬 효율적으로 상호 작용합니다. 특히 비동기 이벤트에서 자주 차단되는 애플리케이션에서 그렇습니다.

### WebAssembly 시스템 인터페이스 {#wasip1}

<!-- https://go.dev/issue/58141 -->
Go 1.21은 [
WebAssembly System Interface (WASI)](https://wasi.dev/)에 대한 실험적인 포트를 추가합니다 (Preview 1: `GOOS=wasip1`, `GOARCH=wasm`).

결과적으로 새로운 `GOOS` 값 "`wasip1`"이 추가됨에 따라, `*_wasip1.go`라는 이름의 Go 파일은 이제 Go 도구에서 [무시]됩니다](/pkg/go/build/#hdr-Build_Constraints), 단, 해당 `GOOS` 값이 사용되는 경우에는 예외입니다.

기존에 해당 패턴과 일치하는 파일 이름을 가지고 있다면, 해당 이름을 변경해야 합니다.

### ppc64/ppc64le {#PPC64}

<!-- go.dev/issue/44549 -->
Linux에서 `GOPPC64=power10`는 이제 PC 상대적 명령어, 접두사 명령, 그리고 기타 새로운 파워10 명령어를 생성합니다. AIX에서 `GOPPC64=power10`는 파워10 명령어를 생성하지만, PC 상대적 명령어를 생성하지 않습니다.

`GOPPC64=power10` 및 `GOOS=linux` `GOARCH=ppc64le`를 사용하여 위치 독립적인 바이너리를 빌드할 때, 사용자는 대부분의 경우 바이너리 크기가 줄어들 것으로 예상할 수 있으며, 특정 경우에는 3.5%까지 감소할 수 있습니다. 위치 독립적인 바이너리는 다음 `-buildmode` 값을 사용하여 ppc64le용으로 빌드됩니다.
`c-archive`, `c-shared`, `shared`, `pie`, `plugin`.

### loong64 {#loong64}

<!-- go.dev/issue/53301, CL 455075, CL 425474, CL 425476, CL 425478, CL 489576 -->
`linux/loong64` 포트는 이제 `-buildmode=c-archive`,
`-buildmode=c-shared` 및 `-buildmode=pie`를 지원합니다.

<!--
 x 저장소에 대한 제안 사항으로, 여기서 언급할 필요는 없지만
     relnote 도구에 의해 캡처됩니다.
 -->
<!-- https://go.dev/issue/54232 -->
<!-- https://go.dev/issue/57051 -->
<!-- https://go.dev/issue/57792 -->
<!-- https://go.dev/issue/57906 -->
<!-- https://go.dev/issue/58668 -->
<!-- https://go.dev/issue/59016 -->
<!-- https://go.dev/issue/59676 -->
<!-- https://go.dev/issue/60409 -->
<!-- https://go.dev/issue/61176 -->
<!-- api/cmd에 대한 변경 사항으로, 릴리스 노트가 필요하지 않습니다. -->
<!-- CL 469115, CL 469135, CL 499981 -->
<!-- 릴리스 노트가 필요하지 않은 제안 사항. -->
<!-- https://go.dev/issue/10275 -->
<!-- https://go.dev/issue/59719 -->
