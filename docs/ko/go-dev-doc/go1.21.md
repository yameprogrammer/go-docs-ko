<!--
참고: 이 문서 및 이 디렉토리의 다른 문서들에서는
`hello` `world`와 같이 고정폭 구문을 비고정폭 공백으로 설정하는 것이 관례입니다.
이러한 구문에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

Please provide the Markdown content you would like me to translate. I am ready to translate your technical text from English to Korean while preserving all formatting, code, and identifiers.

## Go 1.21 소개 {#introduction}

최신 Go 릴리스인 버전 1.21은 [Go 1.20](/doc/go1.20) 이후 6개월 만에 출시되었습니다.
변경 사항의 대부분은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언제나 그랬듯, 이번 릴리스는 Go 1 [호환성 약속](/doc/go1compat)을 유지하며,
실제로 Go 1.21은 [해당 약속을 더욱 개선하였습니다](#tools).
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

<!-- https://go.dev/issue/57631 -->
Go 1.21에서는 릴리스 번호 매기기 방식에 약간의 변경 사항이 도입되었습니다.
이전에는 Go 언어의 전체 버전 및 릴리스 제품군과 해당 제품군의 첫 번째 릴리스를 모두 Go 1._N_으로 지칭했습니다.
Go 1.21부터는 첫 번째 릴리스가 Go 1._N_.0으로 표기됩니다.
오늘 저희는 Go 1.21 언어와 그 초기 구현체인 Go 1.21.0 릴리스를 모두 출시합니다.
본 노트에서는 이를 "Go 1.21"로 지칭하지만, `go` `version`과 같은 도구는 (Go 1.21.1로 업그레이드하기 전까지) "`go1.21.0`"으로 표시합니다.
새로운 버전 번호 매기기에 대한 자세한 내용은 "Go Toolchains" 문서의 “[Go versions](/doc/toolchain#version)”를 참조하십시오.

## 언어 변경 사항 {#language}

Go 1.21에서는 언어에 세 가지 새로운 내장 함수(built-ins)가 추가되었습니다.

- <!-- https://go.dev/issue/59488 -->
    새로운 함수 `min`과 `max`는 주어진 고정된 수의 인자 중 가장 작은 값(`max`는 가장 큰 값)을 계산합니다.
    자세한 내용은 언어 명세의 [상세 설명](/ref/spec#Min_and_max)을 참조하세요.
  - <!-- https://go.dev/issue/56351 -->
    새로운 함수 `clear`는 맵의 모든 요소를 삭제하거나 슬라이스의 모든 요소를 제로 값으로 초기화합니다.
    자세한 내용은 언어 명세의 [상세 설명](/ref/spec#Clear)을 참조하세요.

<!-- https://go.dev/issue/57411 -->
패키지 초기화 순서가 이제 더 정밀하게 지정됩니다. 새로운 알고리즘은 다음과 같습니다:

- 모든 패키지를 import 경로 순으로 정렬합니다.
- 패키지 목록이 비어 있을 때까지 다음 과정을 반복합니다:
  - 모든 import가 이미 초기화된 목록 내의 첫 번째 패키지를 찾습니다.
  - 해당 패키지를 초기화하고 목록에서 제거합니다.

이는 명시적인 import로 표현되지 않은 특정 초기화 순서에 의존하는 일부 프로그램의 동작을 변경할 수 있습니다. 이러한 프로그램의 동작은 이전 릴리스의 사양(spec)에서 명확하게 정의되지 않았습니다. 새로운 규칙은 모호함 없는 정의를 제공합니다.

타입 추론의 성능과 정밀도를 향상시키는 여러 개선 사항이 적용되었습니다.

- <!-- https://go.dev/issue/59338 -->
    이제 (부분적으로 인스턴스화된 제네릭일 수 있는) 함수를 호출할 때, 인자로 (부분적으로 인스턴스화된) 제네릭 함수 자체를 전달할 수 있습니다.
    컴파일러는 이전과 동일하게 피호출 함수의 누락된 타입 인자를 추론하려고 시도하며, 완전히 인스턴스화되지 않은 제네릭 함수 인자가 있는 경우 해당 인자의 누락된 타입 인자도 추론합니다(새로운 기능).
    대표적인 사용 사례는 함수 인자가 제네릭일 수 있고, 호출된 함수와 그 인자들의 타입 인자가 컨테이너 타입으로부터 추론되는 경우로, 컨테이너를 다루는 제네릭 함수([slices.IndexFunc](/pkg/slices#IndexFunc) 등)를 호출할 때 해당됩니다.
    더 일반적으로, 제네릭 함수를 변수에 할당하거나 결과 값으로 반환할 때 타입 인자를 할당문으로부터 추론할 수 있다면 명시적인 인스턴스화 없이 사용할 수 있습니다.
  - <!-- https://go.dev/issue/60353, https://go.dev/issue/57192, https://go.dev/issue/52397, https://go.dev/issue/41176 -->
    이제 값을 인터페이스에 할당할 때 타입 추론 과정에서 메서드도 고려합니다.
    메서드 시그니처에 사용된 타입 파라미터의 타입 인자는 일치하는 메서드의 해당 파라미터 타입으로부터 추론될 수 있습니다.
  - <!-- https://go.dev/issue/51593 https://go.dev/issue/39661 -->
    마찬가지로, 타입 인자는 해당 제약 조건(constraint)의 모든 메서드를 구현해야 하므로, 타입 인자와 제약 조건의 메서드들이 매칭되며 이를 통해 추가적인 타입 인자가 추론될 수 있습니다.
  - <!-- https://go.dev/issue/58671 -->
    서로 다른 종류의 타입되지 않은 상수 인자들(예: 타입되지 않은 int와 타입되지 않은 부동 소수점 상수)이 (별도로 지정되지 않은) 동일한 타입 파라미터 타입을 가진 파라미터로 전달될 때, 이제 에러 대신 타입되지 않은 상수 피연산자를 가진 연산자와 동일한 방식으로 타입을 결정합니다.
    이 변경 사항을 통해 타입되지 않은 상수 인자로부터 추론된 타입이 상수 표현식의 타입과 일치하게 됩니다.
  - <!-- https://go.dev/issue/59750 -->
    이제 할당문에서 대응하는 타입을 매칭할 때 타입 추론이 더 정밀해졌습니다.
    구성 요소 타입(슬라이스의 요소 또는 함수 시그니처의 파라미터 타입 등)은 (적절한 타입 인자가 주어진 상태에서) 동일해야 매칭되며, 그렇지 않으면 추론에 실패합니다.
    이 변경 사항은 더 정확한 에러 메시지를 생성합니다.
    과거에는 타입 추론이 잘못 성공하여 유효하지 않은 할당으로 이어졌을 수 있는 경우에도, 이제 두 타입이 절대 일치할 수 없다면 컴파일러가 추론 에러를 보고합니다.

<!-- https://go.dev/issue/58650 -->
더 일반적으로, 언어 명세의 [type inference](/ref/spec#Type_inference)에 대한 설명이 명확해졌습니다.
이 모든 변경 사항이 결합되어 타입 추론이 더 강력해졌으며, 추론 실패로 인한 당혹스러움이 줄어들었습니다.

<!-- https://go.dev/issue/57969 -->

Go 1.21에는 향후 Go 버전에서 고려 중인 언어 변경 사항의 프리뷰가 포함되어 있습니다.
그 내용은 실수로 변수를 공유하여 발생하는 버그를 방지하기 위해, `for` 루프 변수를 루프당 하나가 아닌 반복(iteration)당 하나로 만드는 것입니다.
이 언어 변경 사항을 시도하는 방법에 대한 자세한 내용은 [LoopvarExperiment 위키 페이지](/wiki/LoopvarExperiment)를 참조하십시오.

<!-- https://go.dev/issue/25448 -->

Go 1.21부터는 고루틴이 패닉(panicking) 상태이고 `recover`가 지연 함수(deferred function)에 의해 직접 호출된 경우, `recover`의 반환 값이 `nil`이 아님이 보장됩니다. 이를 보장하기 위해, `nil` 인터페이스 값(또는 타입이 지정되지 않은 `nil`)으로 `panic`을 호출하면 [`*runtime.PanicNilError`](/pkg/runtime/#PanicNilError) 타입의 런타임 패닉이 발생합니다.

이전 버전의 Go로 작성된 프로그램을 지원하기 위해, `GODEBUG=panicnil=1`을 설정하여 nil 패닉을 다시 활성화할 수 있습니다.
이 설정은 메인 패키지가 `go` `1.20` 또는 그 이전 버전을 선언한 모듈에 포함된 프로그램을 컴파일할 때 자동으로 활성화됩니다.

## 도구 {#tools}

Go 1.21은 Go 툴체인에서 하위 호환성(backwards compatibility) 및 상위 호환성(forwards compatibility)에 대한 개선된 지원을 추가합니다.

<!-- https://go.dev/issue/56986 -->
하위 호환성을 개선하기 위해, Go 1.21은 [호환성 정책](/doc/go1compat)에 따라 파괴적이지는 않으나 기존 프로그램의 동작에 영향을 줄 수 있는 변경 사항의 기본 동작을 제어하기 위한 `GODEBUG` 환경 변수 사용 방식을 공식화합니다.
(예를 들어, 버그가 있는 동작에 의존하는 프로그램은 버그가 수정될 때 문제가 발생할 수 있지만, 버그 수정은 파괴적 변경으로 간주되지 않습니다.)
Go가 이러한 종류의 동작 변경을 수행해야 할 때, 이제 워크스페이스의 `go.work` 파일이나 메인 모듈의 `go.mod` 파일에 명시된 `go` 라인을 기반으로 이전 동작과 새 동작 중 하나를 선택합니다.
새로운 Go 툴체인으로 업그레이드하더라도 `go` 라인을 원래의 (이전) Go 버전으로 유지하면 이전 툴체인의 동작이 유지됩니다.
이러한 호환성 지원을 통해, 최신 Go 툴체인은 항상 이전 버전 Go의 가장 최적화되고 보안이 강화된 구현체가 될 것입니다.
자세한 내용은 “[Go, Backwards Compatibility, and GODEBUG](/doc/godebug)”를 참조하십시오.

<!-- https://go.dev/issue/57001 -->
전방 호환성(forwards compatibility)을 개선하기 위해, Go 1.21은 이제 `go.work` 또는 `go.mod` 파일의 `go` 라인을 엄격한 최소 요구 사항으로 읽습니다. 예를 들어 `go` `1.21.0`은 해당 워크스페이스나 모듈을 Go 1.20 또는 Go 1.21rc1과 함께 사용할 수 없음을 의미합니다. 이를 통해 최신 버전의 Go에서 수정된 사항에 의존하는 프로젝트들이 이전 버전에서 사용되지 않도록 보장할 수 있습니다.

또한, 새로운 Go 기능을 사용하는 프로젝트에 대해 더 나은 오류 보고를 제공합니다. 최신 Go 버전이 필요한 상황일 때, 코드를 빌드하여 해결되지 않은 임포트(unresolved imports)나 구문 오류(syntax errors)를 출력하는 대신, 더 최신 버전의 Go가 필요하다는 문제가 명확하게 보고됩니다.

이러한 더 엄격해진 버전 요구 사항을 더 쉽게 관리하기 위해, 이제 `go` 명령어는 자체 릴리스에 포함된 툴체인뿐만 아니라 PATH에서 찾았거나 필요에 따라 다운로드한 다른 Go 툴체인 버전도 호출할 수 있습니다.

`go.mod` 또는 `go.work` 파일의 `go` 라인에 더 최신 버전의 Go에 대한 최소 요구 사항이 선언되어 있다면, `go` 명령어는 자동으로 해당 버전을 찾아 실행합니다.

새로운 `toolchain` 지시어는 사용할 권장 최소 툴체인을 설정하며, 이는 엄격한 `go` 최소 버전보다 더 최신 버전일 수 있습니다.

자세한 내용은 “[Go Toolchains](/doc/toolchain)”를 참조하십시오.

### Go 명령 {#go-command}

<!-- https://go.dev/issue/58099, CL 474236 -->
이제 `-pgo` 빌드 플래그의 기본값이 `-pgo=auto`로 설정되며, 커맨드 라인에서 단일 메인 패키지만 지정해야 했던 제한이 제거되었습니다. 메인 패키지 디렉토리에 `default.pgo`라는 이름의 파일이 존재하는 경우, `go` 커맨드는 해당 파일을 사용하여 해당 프로그램 빌드 시 프로파일 기반 최적화(profile-guided optimization)를 활성화합니다.

`-C` `dir` 플래그를 사용할 때는 이제 명령줄의 첫 번째 플래그로 지정해야 합니다.

<!-- https://go.dev/issue/37708, CL 463837 -->
새로운 `go` `test` 옵션인
`-fullpath`는 테스트 로그 메시지에 파일의 기본 이름(base name) 대신 전체 경로 이름을 출력합니다.

<!-- https://go.dev/issue/15513, CL 466397 -->
`go` `test` `-c` 플래그가 이제 여러 패키지에 대해 테스트 바이너리를 작성하는 기능을 지원하며, 각 바이너리는 `pkg`가 패키지 이름인 `pkg.test` 파일로 저장됩니다.
컴파일되는 테스트 패키지 중 동일한 패키지 이름을 가진 패키지가 둘 이상인 경우 에러가 발생합니다.

<!-- https://go.dev/issue/15513, CL 466397 -->
이제 `go` `test` `-o` 플래그에서 디렉토리 인수를 사용할 수 있으며, 이 경우 테스트 바이너리가 현재 디렉토리가 아닌 해당 디렉토리에 기록됩니다.

<!-- https://go.dev/issue/31544, CL 477839 -->
cgo가 활성화된 상태에서 외부(C) 링커를 사용할 때, C 링커에 의해 추가된 모든 추가 라이브러리와 Go 런타임의 호환성을 보장하기 위해 이제 `runtime/cgo` 패키지가 Go 링커에 추가 종속성으로 제공됩니다.

### Cgo {#cgo}

<!-- CL 490819 -->
`import "C"`를 사용하는 파일에서, Go 툴체인은 이제 C 타입에 Go 메서드를 선언하려는 시도에 대해 오류를 정확하게 보고합니다.

## 런타임 {#runtime-changes}

<!-- https://go.dev/issue/7181 -->
매우 깊은 스택을 출력할 때, 런타임은 이제 단순히 처음 100개의 프레임을 출력하는 대신, 처음 50개(가장 안쪽) 프레임을 출력한 뒤 마지막 50개(가장 바깥쪽) 프레임을 이어서 출력합니다. 이를 통해 재귀 스택이 얼마나 깊게 시작되었는지 더 쉽게 확인할 수 있으며, 특히 스택 오버플로(stack overflow)를 디버깅할 때 유용합니다.

<!-- https://go.dev/issue/59960 -->
투명한 거대 페이지(transparent huge pages)를 지원하는 Linux 플랫폼에서, Go 런타임은 이제 힙의 어느 부분이 거대 페이지로 뒷받침될 수 있는지를 더 명시적으로 관리합니다. 이는 더 나은 메모리 활용으로 이어집니다. 작은 힙의 경우 메모리 사용량이 감소하며(심한 경우 최대 50%까지), 큰 힙의 경우 힙의 밀집된 부분에서 거대 페이지의 단편화(broken huge pages)가 줄어들어 CPU 사용량과 지연 시간이 최대 1%까지 개선됩니다. 이 변경의 결과로, 런타임은 더 이상 특정 문제가 되는 Linux 설정값을 우회하려고 시도하지 않으며, 이로 인해 메모리 오버헤드가 높아질 수 있습니다. 권장되는 해결 방법은 [GC 가이드](/doc/gc-guide#Linux_transparent_huge_pages)에 따라 OS의 거대 페이지 설정을 조정하는 것입니다. 하지만 다른 우회 방법들도 존재합니다. [`max_ptes_none`에 관한 섹션](/doc/gc-guide#Linux_THP_max_ptes_none_workaround)을 참조하십시오.

<!-- https://go.dev/issue/57069, https://go.dev/issue/56966 -->
런타임 내부의 가비지 컬렉션 튜닝 결과로 인해, 애플리케이션의 꼬리 지연 시간(tail latency)이 최대 40%까지 감소하고 메모리 사용량이 소폭 줄어들 수 있습니다. 일부 애플리케이션에서는 처리량(throughput)이 약간 감소하는 현상이 나타날 수 있습니다.

메모리 사용량의 감소는 처리량의 손실과 비례하므로, `GOGC` 및/또는 `GOMEMLIMIT`을 약간 높임으로써 (지연 시간의 큰 변화 없이) 이전 릴리스의 처리량/메모리 트레이드오프 수준을 회복할 수 있습니다.

<!-- https://go.dev/issue/51676 -->
C에서 생성된 스레드에서 Go로 호출을 수행할 때는 Go 실행을 준비하기 위한 일부 설정이 필요합니다. 이제 Unix 플랫폼에서는 동일한 스레드에서 발생하는 여러 번의 호출 간에 이 설정이 유지됩니다. 이를 통해 이후의 C에서 Go로의 호출 오버헤드가 호출당 약 1-3마이크로초에서 약 100-200나노초로 크게 감소했습니다.

## 컴파일러 {#compiler}

Go 1.20에서 프리뷰로 추가되었던 프로파일 가이드 최적화(Profile-guide optimization, PGO)를 이제 일반 용도로 사용할 수 있습니다. PGO는 운영 워크로드의 프로파일을 통해 '핫(hot)'하다고 식별된 코드에 대해 추가적인 최적화를 가능하게 합니다. [Go command 섹션](#go-command)에서 언급했듯이, 메인 패키지 디렉토리에 `default.pgo` 프로파일이 포함된 바이너리의 경우 PGO가 기본적으로 활성화됩니다. 성능 향상 정도는 애플리케이션의 동작에 따라 다르며, 대표적인 Go 프로그램 세트로 테스트한 결과 대부분의 프로그램에서 PGO 활성화 시 2%에서 7% 사이의 성능 향상을 보였습니다. 자세한 내용은 [PGO 사용자 가이드](/doc/pgo)를 참조하십시오.

<!-- https://go.dev/issue/59959 -->

PGO 빌드는 이제 일부 인터페이스 메서드 호출을 역가상화(devirtualize)하여, 가장 빈번하게 호출되는 대상에 대한 구체적인 호출(concrete call)을 추가할 수 있습니다. 이를 통해 호출 대상의 인라이닝(inlining)과 같은 추가적인 최적화가 가능해집니다.

<!-- CL 497455 -->

Go 1.21은 주로 컴파일러 자체를 PGO로 빌드함으로써 빌드 속도를 최대 6%까지 향상시켰습니다.

## Assembler {#assembler}

<!-- https://go.dev/issue/58378 -->

amd64에서 프레임이 없는(frameless) nosplit 어셈블리 함수는 더 이상 자동으로 `NOFRAME`으로 표시되지 않습니다.
대신, 원하는 경우 `NOFRAME` 속성을 명시적으로 지정해야 하며, 이는 프레임 포인터를 지원하는 다른 아키텍처에서도 이미 적용되고 있는 동작입니다.
이를 통해 런타임은 이제 스택 전환(stack transitions)을 위한 프레임 포인터를 유지합니다.

<!-- CL 476295 -->

amd64에서 동적 링크 시 `R15` 레지스터의 잘못된 사용을 확인하는 검증기(verifier)가 개선되었습니다.

## 링커 (Linker) {#linker}

<!-- https://go.dev/issue/57302, CL 461749, CL 457455 -->
windows/amd64에서 링커는 (컴파일러의 도움을 받아) 이제 기본적으로 SEH unwinding 데이터를 생성하며, 이를 통해 Go 애플리케이션과 Windows 디버거 및 기타 도구 간의 통합이 개선됩니다.

<!-- CL 463395, CL 461315 -->

Go 1.21에서 링커는 (컴파일러의 도움을 받아) 글로벌 map 변수의 초기화 식에 포함된 항목 수가 충분히 많고, 초기화 식이 side-effect가 없는 경우, 사용되지 않는(참조되지 않는) 해당 글로벌 map 변수를 삭제할 수 있게 되었습니다.

## 표준 라이브러리 {#library}

### 새로운 log/slog 패키지 {#slog}

<!--
 https://go.dev/issue/59060, https://go.dev/issue/59141, https://go.dev/issue/59204, https://go.dev/issue/59280,
        https://go.dev/issue/59282, https://go.dev/issue/59339, https://go.dev/issue/59345, https://go.dev/issue/61200,
        CL 477295, CL 484096, CL 486376, CL 486415, CL 487855, CL 508195
 -->
새로운 [log/slog](/pkg/log/slog) 패키지는 레벨이 지정된 구조화된 로깅(structured logging)을 제공합니다.
구조화된 로깅은 대량의 로그 데이터를 빠르고 정확하게 처리할 수 있도록 키-값 쌍(key-value pairs)을 출력합니다.
이 패키지는 널리 쓰이는 로그 분석 도구 및 서비스와의 통합을 지원합니다.

### 새로운 testing/slogtest 패키지 {#slogtest}

<!-- CL 487895 -->
새로운 [testing/slogtest](/pkg/testing/slogtest) 패키지는 [slog.Handler](/pkg/log/slog#Handler) 구현을 검증하는 데 도움이 됩니다.

### 새로운 slices 패키지 {#slices}

<!-- https://go.dev/issue/45955, https://go.dev/issue/54768 -->
<!-- https://go.dev/issue/57348, https://go.dev/issue/57433 -->
<!-- https://go.dev/issue/58565, https://go.dev/issue/60091 -->
<!-- https://go.dev/issue/60546 -->
<!-- CL 467417, CL 468855, CL 483175, CL 496078, CL 498175, CL 502955 -->
새로운 [slices](/pkg/slices) 패키지는 모든 요소 타입의 슬라이스에서 작동하는 제네릭 함수를 사용하여, 슬라이스에 대한 많은 공통 작업을 제공합니다.

### 새로운 maps 패키지 {#maps}

<!-- https://go.dev/issue/57436, CL 464343 -->
새로운 [maps](/pkg/maps/) 패키지는 모든 키 또는 요소 타입의 맵에서 작동하는 제네릭 함수를 사용하여, 맵에 대한 몇 가지 공통 작업을 제공합니다.

### 새로운 cmp 패키지 {#cmp}

<!-- https://go.dev/issue/59488, CL 496356 -->
새로운 [cmp](/pkg/cmp/) 패키지는 타입 제약인 [`Ordered`](/pkg/cmp/#Ordered)와 [정렬 가능한 타입](/ref/spec/#Comparison_operators)에 유용한 두 가지 새로운 제네릭 함수인 [`Less`](/pkg/cmp/#Less) 및 [`Compare`](/pkg/cmp/#Compare)를 정의합니다.

### 라이브러리의 소규모 변경 사항 {#minor_library_changes}

언제나 그렇듯, Go 1 [호환성 약속](/doc/go1compat)을 염두에 두고 라이브러리에 다양한 소규모 변경 사항 및 업데이트가 이루어졌습니다.
또한, 여기에는 나열되지 않은 다양한 성능 개선 사항들이 포함되어 있습니다.

#### [archive/tar](/pkg/archive/tar/)

<!-- https://go.dev/issue/54451, CL 491175 -->
[`Header.FileInfo`](/pkg/archive/tar/#Header.FileInfo)가 반환하는
[`io/fs.FileInfo`](/pkg/io/fs/#FileInfo)
인터페이스의 구현체가 이제 [`io/fs.FormatFileInfo`](/pkg/io/fs/#FormatFileInfo)를 호출하는 `String` 메서드를 구현합니다.

<!-- archive/tar -->

#### [archive/zip](/pkg/archive/zip/)

<!-- https://go.dev/issue/54451, CL 491175 -->
[`FileHeader.FileInfo`](/pkg/archive/zip/#FileHeader.FileInfo)가 반환하는
[`io/fs.FileInfo`](/pkg/io/fs/#FileInfo)
인터페이스의 구현체가 이제 [`io/fs.FormatFileInfo`](/pkg/io/fs/#FormatFileInfo)를 호출하는 `String` 메서드를 구현합니다.

<!-- https://go.dev/issue/54451, CL 491175 -->
[`Reader.Open`](/pkg/archive/zip/#Reader.Open)에 의해 반환되는 [`io/fs.File`](/pkg/io/fs/#File)의 [`io/fs.ReadDirFile.ReadDir`](/pkg/io/fs/#ReadDirFile.ReadDir) 메서드가 반환하는 [`io/fs.DirEntry`](/pkg/io/fs/#DirEntry) 인터페이스의 구현체가 이제 [`io/fs.FormatDirEntry`](/pkg/io/fs/#FormatDirEntry)를 호출하는 `String` 메서드를 구현합니다.

<!-- archive/zip -->

#### [bytes](/pkg/bytes/)

<!-- https://go.dev/issue/53685, CL 474635 -->
[`Buffer`](/pkg/bytes/#Buffer) 타입에
[`Available`](/pkg/bytes/#Buffer.Available)
및 [`AvailableBuffer`](/pkg/bytes/#Buffer.AvailableBuffer)라는
두 가지 새로운 메서드가 추가되었습니다.
이 메서드들은 [`Write`](/pkg/bytes/#Buffer.Write)
메서드와 함께 사용하여 `Buffer`에 직접 데이터를 추가하는 데 사용할 수 있습니다.

<!-- bytes -->

#### [context](/pkg/context/)

<!-- https://go.dev/issue/40221, CL 479918 -->
새로운 [`WithoutCancel`](/pkg/context/#WithoutCancel)
함수는 원본 컨텍스트가 취소되어도 취소되지 않는 컨텍스트의 복사본을 반환합니다.

<!-- https://go.dev/issue/56661, CL 449318 -->
새로운 [`WithDeadlineCause`](/pkg/context/#WithDeadlineCause)
및 [`WithTimeoutCause`](/pkg/context/#WithTimeoutCause)
함수는 마감 시간(deadline)이나 타이머가 만료되었을 때 컨텍스트 취소 원인(cause)을 설정하는 방법을 제공합니다. 이 원인은
[`Cause`](/pkg/context/#Cause) 함수를 통해 조회할 수 있습니다.

<!-- https://go.dev/issue/57928, CL 482695 -->
새로운 [`AfterFunc`](/pkg/context/#AfterFunc) 함수는 컨텍스트(context)가 취소된 후 실행될 함수를 등록합니다.

<!-- CL 455455 -->
최적화를 통해 [`Background`](/pkg/context/#Background)와 [`TODO`](/pkg/context/#TODO)를 호출한 결과물을 공통 타입으로 변환했을 때, 이를 동일한 것으로 간주할 수 있게 되었습니다. 이전 릴리스에서는 이들이 항상 서로 달랐습니다. [`Context`](/pkg/context/#Context) 값의 동일성 비교는 한 번도 명확하게 정의된 적이 없으므로, 이는 호환되지 않는 변경 사항으로 간주되지 않습니다.

#### [crypto/ecdsa](/pkg/crypto/ecdsa/)

<!-- CL 492955 -->
[`PublicKey.Equal`](/pkg/crypto/ecdsa/#PublicKey.Equal) 및
[`PrivateKey.Equal`](/pkg/crypto/ecdsa/#PrivateKey.Equal)이
이제 상수 시간(constant time)으로 실행됩니다.

<!-- crypto/ecdsa -->

#### [crypto/elliptic](/pkg/crypto/elliptic/)

<!-- CL 459977 -->
[`Curve`](/pkg/crypto/elliptic/#Curve)의 모든 메서드는 [`GenerateKey`](/pkg/crypto/elliptic/#GenerateKey), [`Marshal`](/pkg/crypto/elliptic/#Marshal), [`Unmarshal`](/pkg/crypto/elliptic/#Unmarshal)과 함께 더 이상 사용되지 않습니다(deprecated). ECDH 작업의 경우, 대신 새로운 [`crypto/ecdh`](/pkg/crypto/ecdh/) 패키지를 사용해야 합니다. 더 낮은 수준의 작업이 필요한 경우에는 [filippo.io/nistec](https://pkg.go.dev/filippo.io/nistec)와 같은 서드파티 모듈을 사용하세요.

<!-- crypto/elliptic -->

#### [crypto/rand](/pkg/crypto/rand/)

<!-- CL 463123 -->
[`crypto/rand`](/pkg/crypto/rand/) 패키지는 이제 NetBSD 10.0 및 이후 버전에서 `getrandom` 시스템 호출을 사용합니다.

<!-- crypto/rand -->

#### [crypto/rsa](/pkg/crypto/rsa/)

<!-- CL 471259, CL 492935 -->
`GOARCH=amd64` 및 `GOARCH=arm64`에 대해 프라이빗 RSA 작업(복호화 및 서명)의 성능이 이제 Go 1.19보다 향상되었습니다. 해당 성능은 Go 1.20에서 저하되었었습니다.

[`PrecomputedValues`](/pkg/crypto/rsa/#PrecomputedValues)에 프라이빗 필드가 추가됨에 따라, 이전에 미리 계산된 프라이빗 키를 역직렬화(예: JSON에서)하는 경우에도 최적의 성능을 위해 [`PrivateKey.Precompute`](/pkg/crypto/rsa/#PrivateKey.Precompute)를 호출해야 합니다.

<!-- CL 492955 -->
[`PublicKey.Equal`](/pkg/crypto/rsa/#PublicKey.Equal) 및
[`PrivateKey.Equal`](/pkg/crypto/rsa/#PrivateKey.Equal)이
이제 상수 시간(constant time)에 실행됩니다.

<!-- https://go.dev/issue/56921, CL 459976 -->
[`GenerateMultiPrimeKey`](/pkg/crypto/rsa/#GenerateMultiPrimeKey) 함수와 [`PrecomputedValues.CRTValues`](/pkg/crypto/rsa/#PrecomputedValues.CRTValues) 필드가 deprecated 되었습니다. [`PrivateKey.Precompute`](/pkg/crypto/rsa/#PrivateKey.Precompute)를 호출할 때 [`PrecomputedValues.CRTValues`](/pkg/crypto/rsa/#PrecomputedValues.CRTValues) 값이 여전히 채워지기는 하지만, 복호화 작업 중에는 해당 값들이 사용되지 않습니다.

<!-- crypto/rsa -->

<!-- CL 483815 reverted -->

#### [crypto/sha256](/pkg/crypto/sha256/)

<!-- https://go.dev/issue/50543, CL 408795 -->
`GOARCH=amd64`일 때 SHA-224 및 SHA-256 연산이 사용 가능한 경우 네이티브 명령어를 사용하여, 약 3-4배의 성능 향상을 제공합니다.

<!-- crypto/sha256 -->

<!-- CL 481478 reverted -->
<!-- CL 483816 reverted -->

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 497895 -->
이제 서버는 재개된 연결(resumed connections)에 대해 만료 시간을 확인하는 것 외에는 클라이언트 인증서 검증( [`Config.VerifyPeerCertificate`](/pkg/crypto/tls/#Config.VerifyPeerCertificate) 실행 안 함 포함)을 건너뜁니다. 이로 인해 클라이언트 인증서를 사용하는 경우 세션 티켓의 크기가 더 커집니다. 클라이언트는 이미 재개 시 검증을 건너뛰고 있었으나, 이제는 [`Config.InsecureSkipVerify`](/pkg/crypto/tls/#Config.InsecureSkipVerify)가 설정되어 있더라도 만료 시간을 확인합니다.

<!-- https://go.dev/issue/60105, CL 496818, CL 496820, CL 496822, CL 496821, CL 501675 -->
이제 애플리케이션에서 세션 티켓(session tickets)의 내용을 제어할 수 있습니다.

- 새로운 [`SessionState`](/pkg/crypto/tls/#SessionState) 타입은 재개 가능한 세션을 설명합니다.
  - [`SessionState.Bytes`](/pkg/crypto/tls/#SessionState.Bytes) 메서드와 [`ParseSessionState`](/pkg/crypto/tls/#ParseSessionState) 함수는 `SessionState`를 직렬화 및 역직렬화합니다.
  - [`Config.WrapSession`](/pkg/crypto/tls/#Config.WrapSession) 및 [`Config.UnwrapSession`](/pkg/crypto/tls/#Config.UnwrapSession) 훅은 서버 측에서 `SessionState`를 티켓으로 변환하거나 그 반대로 변환합니다.
  - [`Config.EncryptTicket`](/pkg/crypto/tls/#Config.EncryptTicket) 및 [`Config.DecryptTicket`](/pkg/crypto/tls/#Config.DecryptTicket) 메서드는 `WrapSession` 및 `UnwrapSession`의 기본 구현을 제공합니다.
  - [`ClientSessionState.ResumptionState`](/pkg/crypto/tls/#ClientSessionState.ResumptionState) 메서드와 [`NewResumptionState`](/pkg/crypto/tls/#NewResumptionState) 함수는 `ClientSessionCache` 구현체에서 클라이언트 측 세션을 저장하고 재개하는 데 사용될 수 있습니다.

<!-- CL 496817 -->
세션 티켓이 연결 간의 추적 메커니즘으로 사용될 가능성을 줄이기 위해, 이제 서버는 매 재개(resumption) 시마다 새로운 티켓을 발행하며(지원되고 비활성화되지 않은 경우), 티켓에는 더 이상 이를 암호화한 키의 식별자가 포함되지 않습니다. [`Conn.SetSessionTicketKeys`](/pkg/crypto/tls/#Conn.SetSessionTicketKeys)에 많은 수의 키를 전달하는 경우, 이는 눈에 띄는 성능 비용으로 이어질 수 있습니다.

<!-- CL 497376 -->
이제 클라이언트와 서버 모두 Extended Master Secret 확장(RFC 7627)을 구현합니다.
[`ConnectionState.TLSUnique`](/pkg/crypto/tls/#ConnectionState.TLSUnique)의 사용 중단(deprecation) 결정이 철회되었으며, 이제 Extended Master Secret을 지원하는 재개된 연결(resumed connections)에 대해 설정됩니다.

<!-- https://go.dev/issue/44886, https://go.dev/issue/60107, CL 493655, CL 496995, CL 514997 -->
새로운 [`QUICConn`](/pkg/crypto/tls/#QUICConn) 타입은 0-RTT 지원을 포함하여 QUIC 구현을 위한 지원을 제공합니다. 이것 자체가 QUIC 구현은 아니며, 0-RTT는 여전히 TLS에서 지원되지 않는다는 점에 유의하십시오.

<!-- https://go.dev/issue/46308, CL 497377 -->
새로운 [`VersionName`](/pkg/crypto/tls/#VersionName) 함수는 TLS 버전 번호에 해당하는 이름을 반환합니다.

<!-- https://go.dev/issue/52113, CL 410496 -->
클라이언트 인증 실패 시 서버에서 전송하는 TLS alert 코드가 개선되었습니다. 이전에는 이러한 실패가 항상 "bad certificate" alert로 이어졌습니다. 이제 RFC 5246 및 RFC 8446에 정의된 대로, 특정 실패 상황에 대해 더 적절한 alert 코드가 전송됩니다.

- TLS 1.3 연결의 경우, 서버가 [RequireAnyClientCert](/pkg/crypto/tls/#RequireAnyClientCert) 또는 [RequireAndVerifyClientCert](/pkg/crypto/tls/#RequireAndVerifyClientCert)를 사용하여 클라이언트 인증을 요구하도록 설정되어 있고 클라이언트가 인증서를 제공하지 않으면, 이제 서버는 "certificate required" 경고를 반환합니다.
  - 클라이언트가 서버에 설정된 신뢰할 수 있는 인증 기관(CA) 집합에 의해 서명되지 않은 인증서를 제공하는 경우, 서버는 "unknown certificate authority" 경고를 반환합니다.
  - 클라이언트가 만료되었거나 아직 유효하지 않은 인증서를 제공하는 경우, 서버는 "expired certificate" 경고를 반환합니다.
  - 클라이언트 인증 실패와 관련된 그 외 모든 시나리오에서 서버는 여전히 "bad certificate"를 반환합니다.

<!-- crypto/tls -->

#### [crypto/x509](/pkg/crypto/x509/)

<!-- https://go.dev/issue/53573, CL 468875 -->
[`RevocationList.RevokedCertificates`](/pkg/crypto/x509/#RevocationList.RevokedCertificates)는 더 이상 사용되지 않으며(deprecated), [`RevocationListEntry`](/pkg/crypto/x509/#RevocationListEntry)의 슬라이스인 새로운 [`RevokedCertificateEntries`](/pkg/crypto/x509/#RevocationList.RevokedCertificateEntries) 필드로 대체되었습니다. [`RevocationListEntry`](/pkg/crypto/x509/#RevocationListEntry)는 [`pkix.RevokedCertificate`](/pkg/crypto/x509/pkix#RevokedCertificate)의 모든 필드와 폐기 사유 코드(revocation reason code)를 포함합니다.

<!-- CL 478216 -->
이름 제약 조건(Name constraints)이 이제 리프(leaf) 인증서가 아닌 인증서에 대해 올바르게 적용되며, 제약 조건이 명시된 인증서 자체에는 적용되지 않습니다.

<!-- crypto/x509 -->

#### [debug/elf](/pkg/debug/elf/)

<!-- https://go.dev/issue/56892, CL 452617 -->
새로운 [`File.DynValue`](/pkg/debug/elf/#File.DynValue) 메서드를 사용하여 특정 동적 태그(dynamic tag)와 함께 나열된 숫자 값들을 가져올 수 있습니다.

<!-- https://go.dev/issue/56887, CL 452496 -->
`DT_FLAGS_1` 동적 태그에서 허용되는 상수 플래그들이 이제 [`DynFlag1`](/pkg/debug/elf/#DynFlag1) 타입으로 정의됩니다. 이 태그들의 이름은 `DF_1`로 시작합니다.

<!-- CL 473256 -->
이제 패키지에 [`COMPRESS_ZSTD`](/pkg/debug/elf/#COMPRESS_ZSTD) 상수가 정의되었습니다.

<!-- https://go.dev/issue/60348, CL 496918 -->
이제 이 패키지는 [`R_PPC64_REL24_P9NOTOC`](/pkg/debug/elf/#R_PPC64_REL24_P9NOTOC) 상수를 정의합니다.

<!-- debug/elf -->

#### [debug/pe](/pkg/debug/pe/)

<!-- CL 488475 -->
[`Section.Data`](/pkg/debug/pe/#Section.Data) 또는 [`Section.Open`](/pkg/debug/pe/#Section.Open)에서 반환된 리더를 사용하여 초기화되지 않은 데이터가 포함된 섹션으로부터 읽기를 시도하면 이제 에러를 반환합니다.

<!-- debug/pe -->

#### [embed](/pkg/embed/)

<!-- https://go.dev/issue/57803, CL 483235 -->
[`FS.Open`](/pkg/embed/#FS.Open)에 의해 반환되는 [`io/fs.File`](/pkg/io/fs/#File)에 [`io.ReaderAt`](/pkg/io/#ReaderAt)을 구현하는 `ReadAt` 메서드가 추가되었습니다.

<!-- https://go.dev/issue/54451, CL 491175 -->
`<code>[FS.Open](/pkg/embed/FS.Open).[Stat](/pkg/io/fs/#File.Stat)</code>`를 호출하면, 이제 [`io/fs.FormatFileInfo`](/pkg/io/fs/#FormatFileInfo)를 호출하는 `String` 메서드를 구현하는 타입을 반환합니다.

<!-- embed -->

#### [encoding/binary](/pkg/encoding/binary/)

<!-- https://go.dev/issue/57237, CL 463218, CL 463985 -->
새로운 [`NativeEndian`](/pkg/encoding/binary/#NativeEndian) 변수를 사용하여 현재 머신의 네이티브 엔디언(native endianness)을 기반으로 바이트 슬라이스와 정수 간의 변환을 수행할 수 있습니다.

<!-- encoding/binary -->

#### [errors](/pkg/errors/)

<!-- https://go.dev/issue/41198, CL 473935 -->
새로운 [`ErrUnsupported`](/pkg/errors/#ErrUnsupported) 에러는 요청된 작업이 지원되지 않아 수행될 수 없음을 나타내는 표준화된 방법을 제공합니다. 예를 들어, 하드 링크를 지원하지 않는 파일 시스템을 사용할 때 [`os.Link`](/pkg/os/#Link)를 호출하는 경우가 이에 해당합니다.

<!-- errors -->

#### [flag](/pkg/flag/)

<!-- https://go.dev/issue/53747, CL 476015 -->
새로운 [`BoolFunc`](/pkg/flag/#BoolFunc) 함수와 [`FlagSet.BoolFunc`](/pkg/flag/#FlagSet.BoolFunc) 메서드는 인수가 필요하지 않으며, 플래그가 사용될 때 함수를 호출하는 플래그를 정의합니다. 이는 [`Func`](/pkg/flag/#Func)와 유사하지만 불리언(boolean) 플래그를 위한 것입니다.

<!-- CL 480215 -->
동일한 이름의 플래그에 대해 [`Set`](/pkg/flag/#Set)이 이미 호출된 경우,
플래그 정의([`Bool`](/pkg/flag/#Bool),
[`BoolVar`](/pkg/flag/#BoolVar),
[`Int`](/pkg/flag/#Int),
[`IntVar`](/pkg/flag/#IntVar) 등을 통한 정의)는
패닉(panic)을 발생시킵니다. 이 변경 사항은 [초기화 순서의 변경](#language)으로 인해
플래그 작업이 예상과 다른 순서로 발생하는 경우를 감지하기 위한 것입니다.
많은 경우 이 문제의 해결 방법은 명시적인 패키지 의존성을 도입하여
[`Set`](/pkg/flag/#Set) 작업이 수행되기 전에 정의가 올바른 순서로 이루어지도록 하는 것입니다.

<!-- flag -->

#### [go/ast](/pkg/go/ast/)

<!-- https://go.dev/issue/28089, CL 487935 -->
새로운 [`IsGenerated`](/pkg/go/ast/#IsGenerated) 서술어(predicate)는 파일 구문 트리(syntax tree)에 해당 파일이 도구에 의해 생성되었음을 관례적으로 나타내는 [특수 주석](/s/generatedcode)이 포함되어 있는지 여부를 보고합니다.

<!-- https://go.dev/issue/59033, CL 476276 -->
새로운 [`File.GoVersion`](/pkg/go/ast/#File.GoVersion) 필드는 모든 `//go:build` 또는 `// +build` 지시문에서 요구하는 최소 Go 버전을 기록합니다.

<!-- go/ast -->

#### [go/build](/pkg/go/build/)

<!-- https://go.dev/issue/56986, CL 453603 -->
이제 이 패키지는 파일 헤더(`package` 선언 이전)에 있는 빌드 지시어(`//go:`로 시작하는 주석)를 파싱합니다. 이러한 지시어들은 새로운 [`Package`](/pkg/go/build#Package) 필드인 [`Directives`](/pkg/go/build#Package.Directives), [`TestDirectives`](/pkg/go/build#Package.TestDirectives), 그리고 [`XTestDirectives`](/pkg/go/build#Package.XTestDirectives)에서 사용할 수 있습니다.

<!-- go/build -->

#### [go/build/constraint](/pkg/go/build/constraint/)

<!-- https://go.dev/issue/59033, CL 476275 -->
새로운 [`GoVersion`](/pkg/go/build/constraint/#GoVersion) 함수는 빌드 표현식(build expression)에 의해 암시되는 최소 Go 버전을 반환합니다.

<!-- go/build/constraint -->

#### [go/token](/pkg/go/token/)

<!-- https://go.dev/issue/57708, CL 464515 -->
새로운 [`File.Lines`](/pkg/go/token/#File.Lines) 메서드는
`File.SetLines`에서 허용되는 것과 동일한 형식으로 파일의 행 번호 테이블을
반환합니다.

<!-- go/token -->

#### [go/types](/pkg/go/types/)

<!-- https://go.dev/issue/61175, CL 507975 -->
새로운 [`Package.GoVersion`](/pkg/go/types/#Package.GoVersion)
메서드는 패키지를 검사하는 데 사용된 Go 언어 버전을 반환합니다.

<!-- go/types -->

#### [hash/maphash](/pkg/hash/maphash/)

<!-- https://go.dev/issue/47342, CL 468795 -->
`hash/maphash` 패키지에 `purego` 빌드 태그로 선택 가능한 순수 Go 구현체가 추가되었습니다.

<!-- hash/maphash -->

#### [html/template](/pkg/html/template/)

<!-- https://go.dev/issue/59584, CL 496395 -->
JavaScript 템플릿 리터럴 내에 액션(action)이 나타날 때 새로운 에러인 [`ErrJSTemplate`](/pkg/html/template/#ErrJSTemplate)가 반환됩니다. 이전에는 export 되지 않은(unexported) 에러가 반환되었습니다.

<!-- html/template -->

#### [io/fs](/pkg/io/fs/)

<!-- https://go.dev/issue/54451, CL 489555 -->
새로운 [`FormatFileInfo`](/pkg/io/fs/#FormatFileInfo) 함수는 [`FileInfo`](/pkg/io/fs/#FileInfo)의 포맷팅된 버전을 반환합니다.
새로운 [`FormatDirEntry`](/pkg/io/fs/#FormatDirEntry) 함수는 [`DirEntry`](/pkg/io/fs/#FileInfo)의 포맷팅된 버전을 반환합니다.
[`ReadDir`](/pkg/io/fs/#ReadDir)에 의해 반환되는 [`DirEntry`](/pkg/io/fs/#DirEntry)의 구현체는 이제 [`FormatDirEntry`](/pkg/io/fs/#FormatDirEntry)를 호출하는 `String` 메서드를 구현하며, 이는 [`WalkDirFunc`](/pkg/io/fs/#WalkDirFunc)에 전달되는 [`DirEntry`](/pkg/io/fs/#DirEntry) 값에 대해서도 마찬가지입니다.

<!-- io/fs -->

<!-- https://go.dev/issue/56491 rolled back by https://go.dev/issue/60519 -->
<!-- CL 459435 reverted by CL 467255 -->
<!-- CL 467515 reverted by CL 499416 -->

#### [math/big](/pkg/math/big/)

<!-- https://go.dev/issue/56984, CL 453115, CL 500116 -->
새로운 [`Int.Float64`](/pkg/math/big/#Int.Float64) 메서드는 다정밀도 정수(multi-precision integer)에 가장 가까운 부동 소수점 값과 함께, 반올림 발생 여부를 나타내는 지표를 반환합니다.

<!-- math/big -->

#### [net](/pkg/net/)

<!-- https://go.dev/issue/59166, https://go.dev/issue/56539 -->
<!-- CL 471136, CL 471137, CL 471140 -->
Linux에서 [net](/pkg/net/) 패키지는 이제 커널이 지원하는 경우 Multipath TCP를 사용할 수 있습니다. 기본적으로는 사용되지 않습니다. 클라이언트에서 Multipath TCP를 사용하려면, [`Dialer.Dial`](/pkg/net/#Dialer.Dial) 또는 [`Dialer.DialContext`](/pkg/net/#Dialer.DialContext) 메서드를 호출하기 전에 [`Dialer.SetMultipathTCP`](/pkg/net/#Dialer.SetMultipathTCP) 메서드를 호출하십시오. 서버에서 Multipath TCP를 사용하려면, [`ListenConfig.Listen`](/pkg/net/#ListenConfig.Listen) 메서드를 호출하기 전에 [`ListenConfig.SetMultipathTCP`](/pkg/net/#ListenConfig.SetMultipathTCP) 메서드를 호출하십시오. 네트워크는 평소와 같이 `"tcp"`, `"tcp4"` 또는 `"tcp6"`로 지정하십시오. 커널이나 원격 호스트에서 Multipath TCP를 지원하지 않는 경우, 연결은 자동으로 TCP로 폴백(fall back)됩니다. 특정 연결이 Multipath TCP를 사용하고 있는지 테스트하려면 [`TCPConn.MultipathTCP`](/pkg/net/#TCPConn.MultipathTCP) 메서드를 사용하십시오.

향후 Go 릴리스에서는 이를 지원하는 시스템에서 Multipath TCP를 기본적으로 활성화할 수 있습니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- CL 472636 -->
새로운 [`ResponseController.EnableFullDuplex`](/pkg/net/http#ResponseController.EnableFullDuplex)
메서드를 사용하면 서버 핸들러가 응답을 작성하는 동안 HTTP/1
요청 본문을 동시에 읽을 수 있습니다. 일반적으로 HTTP/1 서버는
응답을 읽기 전에 전체 요청을 작성하려는 클라이언트의 데드락을
방지하기 위해, 응답 작성을 시작하기 전 남은 요청 본문을 자동으로
소비합니다. `EnableFullDuplex` 메서드는 이러한 동작을 비활성화합니다.

<!-- https://go.dev/issue/44855, CL 382117 -->
새로운 [`ErrSchemeMismatch`](/pkg/net/http/#ErrSchemeMismatch) 에러는 서버가 HTTPS 요청에 대해 HTTP 응답으로 응답할 때 [`Client`](/pkg/net/http/#Client) 및 [`Transport`](/pkg/net/http/#Transport)에 의해 반환됩니다.

<!-- CL 494122 -->
이제 [net/http](/pkg/net/http/) 패키지가
[`errors.ErrUnsupported`](/pkg/errors/#ErrUnsupported)를 지원합니다.
이에 따라
`errors.Is(http.ErrNotSupported, errors.ErrUnsupported)`
식은 true를 반환합니다.

<!-- net/http -->

#### [os](/pkg/os/)

<!-- https://go.dev/issue/32558, CL 219638 -->
이제 프로그램은 [`Chtimes`](/pkg/os/#Chtimes) 함수에 빈 `time.Time` 값을 전달하여 액세스 시간 또는 수정 시간을 변경하지 않고 그대로 유지할 수 있습니다.

<!-- CL 480135 -->
Windows에서 [`File.Chdir`](/pkg/os#File.Chdir) 메서드가 항상 에러를 반환하는 대신, 이제 현재 디렉터리를 해당 파일로 변경합니다.

<!-- CL 495079 -->
Unix 시스템에서 비차단(non-blocking) 디스크립터가 [`NewFile`](/pkg/os/#NewFile)에 전달된 경우, [`File.Fd`](/pkg/os/#File.Fd) 메서드를 호출하면 이제 비차단 디스크립터가 반환됩니다. 이전에는 디스크립터가 차단(blocking) 모드로 변환되었습니다.

<!-- CL 477215 -->
Windows에서 존재하지 않는 파일에 [`Truncate`](/pkg/os/#Truncate)를 호출하면 이전에는 빈 파일을 생성했습니다. 이제는 파일이 존재하지 않는다는 에러를 반환합니다.

<!-- https://go.dev/issue/56899, CL 463219 -->
Windows에서 [`TempDir`](/pkg/os/#TempDir)을 호출할 때, 이제 GetTempPathW 대신 사용 가능한 경우 GetTempPath2W를 사용합니다. 이 새로운 동작은 SYSTEM 권한으로 실행되는 프로세스가 생성한 임시 파일에 비-SYSTEM 프로세스가 접근하는 것을 방지하기 위한 보안 강화 조치입니다.

<!-- CL 493036 -->
이제 Windows에서 `os` 패키지는 UTF-16으로 저장되어 유효한 UTF-8로 표현할 수 없는 파일 이름을 가진 파일에 대한 작업을 지원합니다.

<!-- CL 463177 -->
Windows에서 [`Lstat`](/pkg/os/#Lstat)이 이제 경로 구분자로 끝나는 경로에 대해 심볼릭 링크를 해석하며, 이는 POSIX 플랫폼에서의 동작과 일치합니다.

<!-- https://go.dev/issue/54451, CL 491175 -->
[`ReadDir`](/pkg/os/#ReadDir) 함수와 [`File.ReadDir`](/pkg/os/#File.ReadDir) 메서드에 의해 반환되는 [`io/fs.DirEntry`](/pkg/io/fs/#DirEntry) 인터페이스의 구현체가 이제 [`io/fs.FormatDirEntry`](/pkg/io/fs/#FormatDirEntry)를 호출하는 `String` 메서드를 구현합니다.

<!-- https://go.dev/issue/53761, CL 416775, CL 498015-->
[`DirFS`](/pkg/os/#DirFS) 함수가 반환하는 [`io/fs.FS`](/pkg/io/fs/#FS) 인터페이스의 구현체가 이제 [`io/fs.ReadFileFS`](/pkg/io/fs/#ReadFileFS) 및 [`io/fs.ReadDirFS`](/pkg/io/fs/#ReadDirFS) 인터페이스를 구현합니다.

<!-- os -->

#### [path/filepath](/pkg/path/filepath/)

[`WalkDir`](/pkg/path/filepath/#WalkDir)
의 함수 인자로 전달되는
[`io/fs.DirEntry`](/pkg/io/fs/#DirEntry)
인터페이스의 구현체가 이제 [`io/fs.FormatDirEntry`](/pkg/io/fs/#FormatDirEntry)를 호출하는 `String` 메서드를 구현합니다.

<!-- path/filepath -->

<!-- CL 459455 reverted -->

#### [reflect](/pkg/reflect/)

<!-- CL 408826, CL 413474 -->
Go 1.21에서 [`ValueOf`](/pkg/reflect/#ValueOf)는 더 이상 인수를 힙(heap)에 강제로 할당하지 않으며, `Value`의 내용이 스택(stack)에 할당될 수 있도록 합니다. `Value`에 대한 대부분의 작업 또한 기반 값이 스택에 할당되는 것을 허용합니다.

<!-- https://go.dev/issue/55002 -->
새로운 [`Value`](/pkg/reflect/#Value)
메서드인 [`Value.Clear`](/pkg/reflect/#Value.Clear)는
맵의 내용을 지우거나 슬라이스의 내용을 제로 값으로 초기화합니다.
이는 언어에 [추가된](#language) 새로운 `clear` 내장 함수와 대응됩니다.

<!-- https://go.dev/issue/56906, CL 452762 -->
[`SliceHeader`](/pkg/reflect/#SliceHeader)와 [`StringHeader`](/pkg/reflect/#StringHeader) 타입은 이제 deprecated 되었습니다. 새로운 코드에서는 [`unsafe.Slice`](/pkg/unsafe/#Slice), [`unsafe.SliceData`](/pkg/unsafe/#SliceData), [`unsafe.String`](/pkg/unsafe/#String), 또는 [`unsafe.StringData`](/pkg/unsafe/#StringData)를 사용하는 것을 권장합니다.

<!-- reflect -->

#### [regexp](/pkg/regexp/)

<!-- https://go.dev/issue/46159, CL 479401 -->
[`Regexp`](/pkg/regexp#Regexp)에 [`MarshalText`](/pkg/regexp#Regexp.MarshalText)와 [`UnmarshalText`](/pkg/regexp#Regexp.UnmarshalText) 메서드가 정의되었습니다. 이 메서드들은 [`encoding.TextMarshaler`](/pkg/encoding#TextMarshaler) 및 [`encoding.TextUnmarshaler`](/pkg/encoding#TextUnmarshaler)를 구현하며, [encoding/json](/pkg/encoding/json)과 같은 패키지에서 사용됩니다.

<!-- regexp -->

#### [runtime](/pkg/runtime/)

<!-- https://go.dev/issue/38651, CL 435337 -->
프로그램 충돌 시, `runtime.Stack` 호출 시, 또는 `debug=2`로 고루틴 프로파일을 수집할 때와 같이 Go 프로그램에서 생성되는 텍스트 기반 스택 트레이스에, 이제 스택 트레이스 내의 각 고루틴을 생성한 고루틴의 ID가 포함됩니다.

<!-- https://go.dev/issue/57441, CL 474915 -->
이제 크래시가 발생하는 Go 애플리케이션은 환경 변수 `GOTRACEBACK=wer`를 설정하거나 크래시 발생 전 [`debug.SetTraceback("wer")`](/pkg/runtime/debug/#SetTraceback)를 호출하여 Windows 오류 보고(WER)를 선택적으로 사용할 수 있습니다. WER 활성화를 제외하고, 런타임은 `GOTRACEBACK=crash`와 동일하게 동작합니다.
Windows가 아닌 시스템에서 `GOTRACEBACK=wer`는 무시됩니다.

<!-- CL 447778 -->
cgo 포인터 전달 규칙을 철저하게 검사하는 `GODEBUG=cgocheck=2`를 더 이상 [디버그 옵션](/pkg/runtime#hdr-Environment_Variables)으로 사용할 수 없습니다.
대신, `GOEXPERIMENT=cgocheck2`를 사용하는 실험적 기능으로 제공됩니다.
특히 이는 해당 모드를 실행 시점이 아닌 빌드 시점에 선택해야 함을 의미합니다.

`GODEBUG=cgocheck=1`은 여전히 사용할 수 있으며 (여전히 기본값입니다).

<!-- https://go.dev/issue/46787, CL 367296 -->
`runtime` 패키지에 새로운 타입인 `Pinner`가 추가되었습니다. `Pinner`는 Go 메모리를 "고정(pin)"하여 non-Go 코드에서 더 자유롭게 사용할 수 있도록 하는 데 사용될 수 있습니다. 예를 들어, 고정된 Go 메모리를 참조하는 Go 값을 C 코드로 전달하는 것이 이제 허용됩니다. 이전에는 [cgo 포인터 전달 규칙(cgo pointer passing rules)](https://pkg.go.dev/cmd/cgo#hdr-Passing_pointers)에 의해 이러한 중첩된 참조를 전달하는 것이 금지되었습니다. 자세한 내용은 [문서](/pkg/runtime#Pinner)를 참조하십시오.

<!-- CL 472195 릴리스 노트 필요 없음 -->

<!-- runtime -->

#### [runtime/metrics](/pkg/runtime/metrics/)

<!-- https://go.dev/issue/56857, CL 497315 -->
live heap size와 같은 몇 가지 기존 내부 GC 메트릭을 이제 사용할 수 있습니다.
`GOGC` 및 `GOMEMLIMIT` 또한 이제 메트릭으로 사용할 수 있습니다.

<!-- runtime/metrics -->

#### [runtime/trace](/pkg/runtime/trace/)

<!-- https://go.dev/issue/16638 -->
이제 amd64 및 arm64에서 트레이스(trace)를 수집할 때 발생하는 CPU 비용이 상당히 줄어들었습니다. 이전 릴리스 대비 최대 10배의 성능 향상이 이루어졌습니다.

<!-- CL 494495 -->
이제 트레이스(Trace)에 가비지 컬렉션뿐만 아니라 Go 런타임이 stop-the-world를 발생시킬 수 있는 모든 이유에 대한 명시적인 stop-the-world 이벤트가 포함됩니다.

<!-- runtime/trace -->

#### [sync](/pkg/sync/)

<!-- https://go.dev/issue/56102, CL 451356 -->
새로운 [`OnceFunc`](/pkg/sync/#OnceFunc),
[`OnceValue`](/pkg/sync/#OnceValue), 그리고
[`OnceValues`](/pkg/sync/#OnceValues)
함수들은 첫 사용 시 값을 지연 초기화(lazily initialize)하기 위해 [Once](/pkg/sync/#Once)를 사용하는 일반적인 패턴을 캡슐화합니다.

#### [syscall](/pkg/syscall/)

<!-- CL 480135 -->
Windows에서 [`Fchdir`](/pkg/syscall#Fchdir) 함수가 항상 에러를 반환하는 대신, 이제 현재 디렉터리를 인자로 전달된 디렉터리로 변경합니다.

<!-- https://go.dev/issue/46259, CL 458335 -->
FreeBSD에서
[`SysProcAttr`](/pkg/syscall#SysProcAttr)
에 새로 생성된 프로세스를 jail 환경에 배치하는 데 사용할 수 있는 새로운 필드 `Jail`이 추가되었습니다.

<!-- CL 493036 -->
Windows에서 `syscall` 패키지는 이제 UTF-16으로 저장되어 유효한 UTF-8로 표현할 수 없는 이름을 가진 파일 작업 기능을 지원합니다.
[`UTF16ToString`](/pkg/syscall#UTF16ToString) 및 [`UTF16FromString`](/pkg/syscall#UTF16FromString) 함수는 이제 UTF-16 데이터와 [WTF-8](https://simonsapin.github.io/wtf-8/) 문자열 간의 변환을 수행합니다.
WTF-8은 이전 릴리스에서 사용된 UTF-8 형식의 슈퍼셋이므로 하위 호환성이 유지됩니다.

<!-- CL 476578, CL 476875, CL 476916 -->
여러 오류 값이 새로운 [`errors.ErrUnsupported`](/pkg/errors/#ErrUnsupported)와 일치하므로, `errors.Is(err, errors.ErrUnsupported)`가 true를 반환합니다.

- `ENOSYS`
  - `ENOTSUP`
  - `EOPNOTSUPP`
  - `EPLAN9` (Plan 9 전용)
  - `ERROR_CALL_NOT_IMPLEMENTED` (Windows 전용)
  - `ERROR_NOT_SUPPORTED` (Windows 전용)
  - `EWINDOWS` (Windows 전용)

<!-- syscall -->

#### [testing](/pkg/testing/)

<!-- https://go.dev/issue/37708, CL 463837 -->
새로운 `-test.fullpath` 옵션은 테스트 로그 메시지에서 기본 이름(base name) 대신 전체 경로 이름을 출력합니다.

<!-- https://go.dev/issue/52600, CL 475496 -->
새로운 [`Testing`](/pkg/testing/#Testing) 함수는 프로그램이 `go` `test`에 의해 생성된 테스트인지 여부를 보고합니다.

<!-- testing -->

#### [testing/fstest](/pkg/testing/fstest/)

<!-- https://go.dev/issue/54451, CL 491175 -->
`<code>[Open](/pkg/testing/fstest/MapFS.Open).[Stat](/pkg/io/fs/#File.Stat)</code>`를 호출하면 이제 [`io/fs.FormatFileInfo`](/pkg/io/fs/#FormatFileInfo)를 호출하는 `String` 메서드를 구현하는 타입이 반환됩니다.

<!-- testing/fstest -->

#### [unicode](/pkg/unicode/)

<!-- CL 456837 -->
[`unicode`](/pkg/unicode/) 패키지와 시스템 전반의 관련 지원 기능이 [Unicode 15.0.0](https://www.unicode.org/versions/Unicode15.0.0/)으로 업그레이드되었습니다.

<!-- unicode -->

## 포트 (Ports) {#ports}

### Darwin {#darwin}

<!-- https://go.dev/issue/57125 -->
Go 1.20 릴리스 노트에서 [공지](go1.20#darwin)한 바와 같이,
Go 1.21은 macOS 10.15 Catalina 또는 그 이후 버전을 필요로 합니다.
이전 버전에 대한 지원은 중단되었습니다.

### Windows {#windows}

<!-- https://go.dev/issue/57003, https://go.dev/issue/57004 -->
Go 1.20 릴리스 노트에서 [공지](go1.20#windows)한 바와 같이,
Go 1.21은 최소 Windows 10 또는 Windows Server 2016 이상이 필요하며,
이전 버전에 대한 지원은 중단되었습니다.

### ARM

<!-- CL 470695 -->

ARM 시스템에서 실행 중이지 않을 때(즉, ARM용 교차 컴파일러를 빌드할 때) `GOARCH=arm`으로 Go 배포판을 빌드하는 경우, `GOARM` 환경 변수의 기본값이 이제 항상 `7`로 설정됩니다.

이전에는 기본값이 빌드 시스템의 특성에 따라 결정되었습니다.

크로스 컴파일러를 빌드하지 않는 경우, 기본값은 빌드 시스템을 조사하여 결정됩니다.
이는 이전에도 그랬으며 Go 1.21에서도 마찬가지입니다.
변경된 점은 크로스 컴파일러를 빌드할 때의 동작입니다.

### WebAssembly {#wasm}

<!-- https://go.dev/issue/38248, https://go.dev/issue/59149, CL 489255 -->
이제 Go 프로그램에서 WebAssembly 호스트의 함수를 임포트하기 위해 새로운 `go:wasmimport` 지시어를 사용할 수 있습니다.

<!-- https://go.dev/issue/56100 -->

Go 스케줄러가 이제 JavaScript 이벤트 루프와 훨씬 더 효율적으로 상호 작용하며, 특히 비동기 이벤트로 인해 빈번하게 블록(block)되는 애플리케이션에서 그 효과가 두드러집니다.

### WebAssembly 시스템 인터페이스 (WebAssembly System Interface) {#wasip1}

<!-- https://go.dev/issue/58141 -->
Go 1.21은 [WebAssembly System Interface (WASI)](https://wasi.dev/) Preview 1(`GOOS=wasip1`, `GOARCH=wasm`)에 대한 실험적인 포트를 추가합니다.

새로운 `GOOS` 값인 "`wasip1`"이 추가됨에 따라, 이제 `*_wasip1.go`라는 이름의 Go 파일은 해당 `GOOS` 값이 사용되는 경우를 제외하고는 [Go 도구에 의해 무시됩니다](/pkg/go/build/#hdr-Build_Constraints).
해당 패턴과 일치하는 기존 파일 이름이 있는 경우, 이름을 변경해야 합니다.

### ppc64/ppc64le {#PPC64}

<!-- go.dev/issue/44549 -->
Linux에서 `GOPPC64=power10`은 이제 PC-상대(PC-relative) 명령어, 접두사(prefixed) 명령어 및 기타 새로운 Power10 명령어를 생성합니다. AIX에서 `GOPPC64=power10`은 Power10 명령어를 생성하지만, PC-상대 명령어는 생성하지 않습니다.

`GOPPC64=power10`, `GOOS=linux`, `GOARCH=ppc64le` 설정으로 위치 독립적(position-independent) 바이너리를 빌드할 때, 대부분의 경우 바이너리 크기가 감소하며 일부 경우에는 최대 3.5%까지 감소할 수 있습니다. ppc64le에서 다음과 같은 `-buildmode` 값으로 위치 독립적 바이너리가 빌드됩니다:
`c-archive`, `c-shared`, `shared`, `pie`, `plugin`.

### loong64 {#loong64}

<!-- go.dev/issue/53301, CL 455075, CL 425474, CL 425476, CL 425478, CL 489576 -->
이제 `linux/loong64` 포트에서 `-buildmode=c-archive`,
`-buildmode=c-shared` 및 `-buildmode=pie`를 지원합니다.

<!--
 여기서 언급할 필요는 없지만 relnote 도구에 의해 수집되는 x 레포지토리들에 대한 제안들입니다.
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
<!-- 릴리스 노트가 필요 없는 cmd/api 변경 사항들입니다. -->
<!-- CL 469115, CL 469135, CL 499981 -->
<!-- 릴리스 노트가 필요 없는 제안들입니다. -->
<!-- https://go.dev/issue/10275 -->
<!-- https://go.dev/issue/59719 -->
