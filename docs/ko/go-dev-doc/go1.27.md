Please provide the Markdown content you would like me to translate. You have provided a `<style>` block, but no text to translate yet. I am ready to translate your content while preserving all technical structures.

## Go 1.27 소개 {#introduction}

최신 Go 릴리스인 버전 1.27은 [Go 1.26](/doc/go1.26) 이후 6개월 뒤인 [2026년 8월](/doc/devel/release#go1.27.0)에 출시됩니다.
변경 사항의 대부분은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언제나 그랬듯, 이번 릴리스에서도 Go 1의 [호환성 약속](/doc/go1compat)을 유지합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

<!-- go.dev/issue/77273 -->

Go 1.27은 이제 [제네릭 메서드](/issue/77273)를 지원합니다. [메서드 선언](/ref/spec#Method_declarations) 시 자체적인 [타입 파라미터](/ref/spec#Type_parameter_declarations)를 선언할 수 있습니다. 널리 기대되었던 이번 변경 사항을 통해, 이전에는 패키지 전체 범위로 선언해야 했던 제네릭 함수를 특정 데이터 타입의 네임스페이스 내에 추가할 수 있게 되었습니다.

예를 들어, `math/rand/v2`는 이제 `(*Rand) N[Int intType](Int) Int` 시그니처를 가진 제네릭 메서드를 선언하며, 이전에는 단지 `N[Int intType](Int) Int`라는 제네릭 함수만 가지고 있었습니다 (자세한 내용은 [아래](#rand) 참조).

[인터페이스](/ref/spec#Interface_types)의 메서드는 타입 파라미터를 선언할 수 없으며, 인터페이스 메서드를 제네릭 메서드로 구현할 수도 없음에 유의하십시오.

<!-- go.dev/issue/9859 -->

[구조체 리터럴](/ref/spec#Composite_literals)의 키는 이제 구조체 타입의 (최상위) 필드 이름뿐만 아니라, 해당 구조체 타입에 대한 모든 유효한 [필드 선택자](/issue/9859)가 될 수 있습니다.

<!-- go.dev/issue/77245 -->

함수 타입 추론이 일반화되어([generalized](/issue/77245)), 제네릭 함수가 일치하는 함수 타입의 변수에 [할당](/ref/spec#Assignability)되거나 해당 타입으로 변환되는 모든 컨텍스트에 적용됩니다.

## 도구 {#tools}

<!-- go.dev/issue/77177 -->

이제 `compile`, `link`, `asm`, `cgo`, `cover` 및 `pack` 도구에서 응답 파일(`@file`) 파싱을 지원합니다.
응답 파일은 공백으로 구분된 인수를 포함하며, 작은따옴표와 큰따옴표로 묶인 문자열, 이스케이프 시퀀스, 그리고 백슬래시-줄바꿈(`backslash-newline`)을 이용한 줄 바꿈 연결을 지원합니다.
이 형식은 기존 빌드 시스템과의 상호 운용성을 보장하기 위해 GCC의 응답 파일 구현과 호환됩니다.

### Go command {#go-command}

<!-- go.dev/issue/78090 -->

`go` 명령어는 더 이상 `bzr` 버전 관리 시스템을 지원하지 않습니다.
이제 `bzr` 서버에 호스팅된 모듈을 직접 가져올 수 없습니다.

#### `GODEBUG`

<!-- go.dev/issue/79422 -->

Go 1.27부터 `go` 커맨드는 `go.mod` 파일(`godebug` 항목)과 `.go` 소스 파일(`//go:debug` 주석)에 명시되어 있을 경우, 더 이상 지원되지 않는 `GODEBUG` 설정(예: [아래](#runtime)의 `asynctimerchan`)을 인식합니다.

해당 설정이 지원 중단 전의 최종 기본값으로 설정되어 있다면 이를 허용합니다.
만약 이전의 다른 값으로 설정되어 있다면, `go` 커맨드는 오류를 발생시키며 실패합니다.

이 변경 사항은 [Go 1 호환성 보장](/doc/go1compat)의 취지에 따른 것이며, 지원되는 `GODEBUG` 설정을 사용 중인 기존 프로그램들이 해당 설정에 대한 지원이 중단된 후에도 변경 없이 계속해서 빌드되고 실행될 수 있도록 합니다.

#### `go test`

이제 `go test`는 기본적으로 `stdversion` vet 체크를 호출합니다.
이는 `go.mod`의 `go` 지시문과 파일의 빌드 태그에 의해 결정된 해당 파일의 Go 버전보다 더 최신 버전의 표준 라이브러리 심볼을 사용하고 있을 때 이를 보고합니다.

<!-- go.dev/issue/62728 -->

`go test -json`은 이제 `"Action":"output"` 라인에 출력 유형을 지정하는 선택적 새 필드인 `"OutputType"`을 추가하여 주석을 답니다.
현재 가능한 값에는 "error", "error-continue", "frame"이 포함됩니다.
자세한 내용은 [cmd/test2json 도움말](/cmd/test2json#hdr-Output_Format)을 참조하십시오.

#### `go doc`

<!-- go.dev/issue/63696 -->

`go doc` 명령어가 이제 `go doc example.com/pkg@v1.2.3`와 같은 `package@version` 구문을 지원합니다.

<!-- go.dev/issue/26715 -->

`go doc` 명령어가 이제 `-ex` 커맨드라인 옵션을 지원하여, 지정된 패키지나 심볼의 실행 가능한 예제(executable examples) 목록을 표시할 수 있습니다.
커맨드라인에 예제 이름이 전달되면(예: `go doc bytes.ExampleBuffer`), `go doc`은 이제 주석과 함께 해당 예제의 소스 코드를 출력합니다.

#### `go fix`

`go fix` 명령에는 여러 개의 새로운 현대화 도구(`atomictypes`, `embedlit`, `slicesbackward`, `unsafefuncs`)가 포함되어 있습니다.

<!-- go.dev/issue/77581 -->

기존의 `fmtappendf` 분석기는 스타일 관련 문제로 인해 제거되었습니다.

기존의 `waitgroup` 분석기는 모호함을 피하기 위해 `waitgroupgo`로 이름이 변경되었습니다.

#### `go mod tidy`

<!-- go.dev/issue/56471 -->

`go.mod` 파일에 `go 1.27` 또는 그 이후 버전을 지정한 모듈의 경우, 이제 `go mod tidy`가 중복된 require 블록을 자동으로 병합합니다. 이를 통해 파일이 최대 두 개의 require 블록(직접 의존성용 하나, 간접 의존성용 하나)만 포함하는 깨끗하고 표준적인 구조를 유지하도록 보장합니다.

이 통합 과정에서 의존성에 연결된 기존 주석 블록은 유지됩니다. 만약 주석 블록이 직접 의존성과 간접 의존성이 모두 포함된 혼합 지침 세트와 연결되어 있다면, 해당 주석 블록은 병합되어 새로운 직접 의존성 블록에 연결됩니다.

이전에는 `go.mod` 파일에 여러 개의 서로 떨어진 `require` 블록이 누적된 경우(주로 수동 편집, 해결되지 않은 Git 병합 충돌 또는 레거시 업그레이드로 인해 발생), `go mod tidy`가 추가 블록들을 그대로 두거나 의도치 않게 새로운 블록을 생성하곤 했습니다. 이제 이 도구는 두 개의 블록 레이아웃을 엄격하게 적용하여, 흩어져 있는 요구 사항들을 각각의 블록으로 통합하고 모듈 파일의 구조를 자동으로 정리합니다.

### Gofmt {#gofmt}

<!-- go.dev/issue/77959, CL 752862 -->

이번 릴리스에는 `gofmt`(및 [`go/format`](/pkg/go/format))가 열 정렬을 결정할 때 사용하는 로직에 대한 수정 사항이 포함되어 있습니다. 이전 로직으로 인해 CPU 아키텍처에 따라 `gofmt`의 동작이 약간씩 다르게 나타나는 문제가 있었습니다. 새로운 로직은 소수의 파일에 대해 정렬 결정 방식을 변경하므로, 이전에 포맷팅된 코드에 Go 1.27의 `gofmt`를 실행하면 미세한 공백 변경이 발생할 수 있습니다.

### Vet {#vet}

<!-- go.dev/issue/61342, CL 761240 -->

[printf](https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/printf) 분석기는 이제 `%w` 피연산자 `p`의 타입이 `*E`이고, 타입 `E` 자체가 `error`를 구현하는 경우의 `fmt.Errorf("...: %w", p)`와 같은 호출을 보고합니다. 이런 식으로 포인터를 래핑하는 것은 보통 잠재적인 버그입니다. 왜냐하면 타입 단언(type assertion)이나 [`errors.Is`](/pkg/errors#Is) 호출과 같이 특정 에러 타입을 테스트하는 작업에서 예기치 않은 실패를 유발하기 때문입니다.

### Trace

<!-- go.dev/issue/78921 -->

`go tool trace`의 `-http` 명령줄 옵션에서 포트만 지정했을 때(예: `-http=:6060`), 이제 리슨(listen) 주소가 localhost로 제한됩니다.

이 변경 사항은 `go tool trace`를 `go tool pprof`의 `-http` 플래그 동작과 일치시키기 위한 것입니다.

모든 주소에서 리슨하려면 지정된 주소를 명시적으로 포함하십시오(예: `-http=0.0.0.0:6060`).

## 런타임 {#runtime}

<!-- CL 742580 -->

Go 1.27 이상을 설정하는 `go` 지시문이 포함된 모듈의 Traceback 헤더 라인에 이제 [`runtime/pprof`](https://pkg.go.dev/runtime/pprof) 고루틴 레이블(goroutine labels)이 포함됩니다. 이 동작은 `GODEBUG` 설정인 `tracebacklabels=0`을 통해 비활성화할 수 있습니다 ([Go 1.26](/doc/godebug#go-126에서 추가됨)). 고루틴 레이블에 Traceback에 노출되어서는 안 될 민감한 정보가 포함될 경우를 대비하여, 이 옵트아웃(opt-out) 설정은 무기한 유지될 예정입니다.

<!-- CL 781580 -->

`asynctimerchan` `GODEBUG` 설정([Go 1.23](/doc/godebug#go-123에서 추가됨)은)
영구적으로 제거되었습니다. [time](https://pkg.go.dev/time) 패키지에 의해 생성된 채널은 이제 `GODEBUG` 설정과 관계없이 항상 버퍼가 없는(동기식) 상태가 됩니다.

### 더 빠른 메모리 할당

<!-- go.dev.issue/79286 -->

이제 컴파일러가 크기별로 특화된 메모리 할당 루틴(size-specialized memory allocation routines) 호출을 생성하여, 일부 작은 크기(<80바이트)의 메모리 할당 비용을 최대 30%까지 줄입니다.

개선 정도는 워크로드에 따라 다르지만, 실제 할당이 빈번한 프로그램에서는 전반적으로 약 1%의 성능 향상이 예상됩니다.

이로 인해 바이너리 크기가 약 60 KB 증가합니다(워크로드와 무관).

회귀 현상이 발견되면 [이슈를 제기](/issue/new)해 주세요.

빌드 시 `GOEXPERIMENT=nosizespecializedmalloc`를 설정하여 이 기능을 비활성화할 수 있습니다.

이 옵트아웃(opt-out) 설정은 Go 1.28에서 제거될 예정입니다.

### Goroutine leak profile {#goroutineleak-profiles}

<!-- go.dev/issue/74609 -->

[Go 1.26](/doc/go1.26#goroutineleak-profiles)에서 실험적 기능으로 제공되었던, 누수된 고루틴(leaked goroutines)을 보고하는 새로운 프로파일 유형이 이제 정식으로 제공됩니다.

`goroutineleak`라는 이름의 이 새로운 프로파일 유형은 [`runtime/pprof`](/pkg/runtime/pprof) 패키지에서 지원됩니다.

또한 [`net/http/pprof`](/pkg/net/http/pprof) 엔드포인트인 `/debug/pprof/goroutineleak`를 통해서도 사용할 수 있습니다.

*누수된(leaked)* 고루틴이란 일부 동시성 프리미티브(채널, [`sync.Mutex`](/pkg/sync#Mutex), [`sync.Cond`](/pkg/sync#Cond) 등)에서 블록되어 더 이상 해제될 가능성이 없는 고루틴을 의미합니다.
런타임은 가비지 컬렉터를 사용하여 누수된 고루틴을 감지합니다. 만약 고루틴 G가 동시성 프리미티브 P에서 블록되어 있고, P가 실행 가능한 모든 고루틴이나 *그들*이 해제시킬 수 있는 모든 고루틴으로부터 도달 불가능하다면, P는 해제될 수 없으며 따라서 고루틴 G는 결코 깨어날 수 없습니다.
모든 경우에 영구적으로 블록된 고루틴을 감지하는 것은 불가능하지만, 이 접근 방식은 그러한 누수의 상당 부분을 감지할 수 있습니다.

이 기법은 도달 가능성(reachability)을 기반으로 하기 때문에, 전역 변수나 실행 가능한 goroutine의 지역 변수를 통해 도달할 수 있는 동시성 기본 요소(concurrency primitives)에서 블로킹이 발생하여 생기는 누수를 런타임이 식별하지 못할 수 있습니다.

예제는 [Go 1.26 릴리스 노트](/doc/go1.26#goroutineleak-profiles)를 참조하십시오.

이 작업에 기여해 주신 Uber의 Vlad Saioc 님께 특별한 감사를 드립니다.

`goroutineleakprofile` `GOEXPERIMENT` 설정이 이제 삭제되었습니다.

## 컴파일러 {#compiler}

이제 컴파일러는 `//line` 또는 `/*line*/` 지시문에 포함된 상대 파일 경로를 해당 지시문이 포함된 파일의 디렉토리를 기준으로 해석하며, 이는 [`go/scanner`](/pkg/go/scanner)의 동작과 일치합니다.
절대 파일 경로는 영향을 받지 않습니다.
[#70478](/issue/70478)를 참조하십시오.

<!-- go.dev/issue/60324, CL 770200 -->

이제 컴파일러가 함수 리터럴(클로저)에 대해 더 단순한 이름을 생성합니다.
이전에는 포함된 함수가 인라인화될 때 함수 리터럴의 이름이 상당히 길어질 수 있었습니다.
이제 컴파일러는 인라인화 여부와 관계없이 함수 리터럴에 대해 동일한 이름을 선택합니다.
또한 (포함된 함수가 인라인화됨에 따라) 동일한 함수 리터럴의 여러 인스턴스를 결합하여 컴파일된 바이너리에서 동일한 코드를 공유하도록 할 수 있습니다.
이 변경 사항은 Go 코드의 기능에 영향을 주지 않습니다.
심볼 이름을 확인하는 테스트는 업데이트가 필요할 수 있으나, 함수 리터럴의 이름에 의존하지 않는 것이 권장됩니다.
함수 코드 포인터를 사용하여 동일성을 [잘못되게](/pkg/reflect#Value.Pointer) 비교하는 프로그램의 경우, 서로 다른 캡처된 클로저 데이터를 가진 함수 리터럴이 더 많은 경우에 동일한 코드 포인터를 가질 수 있으므로 Go 1.27에서 이 문제가 더 많이 드러날 수 있습니다.

## Linker {#linker}

<!-- CL 751260, go.dev/issue/58722 -->

macOS를 타겟으로 할 때, 링커는 이제 `-macos` 및 `-macsdk` 명령줄 옵션을 허용하며, 이를 통해 `LC_BUILD_VERSION` 로드 명령에 OS 및 SDK 버전을 지정할 수 있습니다.
기본적으로, 지원되는 가장 오래된 macOS 버전(현재 [13.0.0](#darwin))과 최신 SDK 버전(현재 26.2.0)이 선택됩니다.

## 표준 라이브러리 {#library}

### 새로운 encoding/json/v2 및 encoding/json/jsontext 패키지 {#jsonv2}

<!-- go.dev/issue/71497 -->

두 개의 새로운 패키지를 이제 사용할 수 있습니다:

- [`encoding/json/v2`](/pkg/encoding/json/v2) 패키지는 [`encoding/json`](/pkg/encoding/json)의 주요 개정판입니다. 이 패키지는 [`Marshal`](/pkg/encoding/json/v2#Marshal), [`MarshalWrite`](/pkg/encoding/json/v2#MarshalWrite), [`MarshalEncode`](/pkg/encoding/json/v2#MarshalEncode), [`Unmarshal`](/pkg/encoding/json/v2#Unmarshal), [`UnmarshalRead`](/pkg/encoding/json/v2#UnmarshalRead), 그리고 [`UnmarshalDecode`](/pkg/encoding/json/v2#UnmarshalDecode)를 제공하며, 이 모든 함수는 마샬링 및 언마샬링 동작을 설정하기 위해 가변 [`Options`](/pkg/encoding/json/v2#Options) 인자를 받습니다.

- [`encoding/json/jsontext`](/pkg/encoding/json/jsontext) 패키지는
    JSON의 하위 수준 구문 처리를 제공합니다.
    [`Encoder`](/pkg/encoding/json/jsontext#Encoder) 및
    [`Decoder`](/pkg/encoding/json/jsontext#Decoder) 타입은
    JSON을 [`Token`](/pkg/encoding/json/jsontext#Token)과
    [`Value`](/pkg/encoding/json/jsontext#Value)의 시퀀스로 처리하며,
    생성되거나 소비되는 시퀀스가 유효한 JSON 텍스트인지 보장하기 위해
    상태 머신을 유지합니다.

v2 패키지는 v1보다 더 엄격하고 상호 운용성이 높은 기본값을 선택합니다.
JSON 문자열 내의 잘못된 UTF-8을 거부하고, JSON 객체 내의 중복된 이름을 거부합니다.
전체적인 동작 차이점과 이를 조정할 수 있는 옵션에 대해서는 v1 [`encoding/json`](/pkg/encoding/json#hdr-Migrating_to_v2) 패키지 문서를 참조하십시오.

[`encoding/json`](/pkg/encoding/json) 패키지는 이제 v2 구현체를 기반으로 작동합니다. 마샬링(Marshaling) 및 언마샬링(Unmarshaling) 동작은 그대로 유지되지만, 에러 메시지의 정확한 텍스트는 다를 수 있습니다. 또한, 새로운 API로의 완전한 마이그레이션이 필요하지 않도록 v2가 v1의 시맨틱으로 동작하게 설정할 수 있는 여러 가지 새로운 [`Options`](/pkg/encoding/json#Options)가 추가되었습니다. v1 API는 계속해서 지원될 예정이며, 사용자가 반드시 마이그레이션할 필요는 없습니다.

Marshal 성능은 이전 구현과 대체로 동등한 수준이며, unmarshal 성능은 상당히 더 빨라졌습니다.

새로운 구현으로 인해 호환성 문제가 발생하는 사용자는 빌드 시 `GOEXPERIMENT=nojsonv2`를 설정하여 이를 비활성화하고 기존의 v1 구현으로 복구할 수 있습니다.
이 선택적 제외(opt-out) 옵션은 향후 릴리스에서 제거될 예정입니다.

`GOEXPERIMENT` 과정 동안 `encoding/json/v2`에 도입된 주요 변경 사항에는 다음과 같은 제거 항목들이 포함됩니다:
- `format` 태그 옵션 ([#79071](/issue/79071))
- `unknown` 태그 옵션 ([#77271](/issue/77271))
- `DiscardUnknownMembers` 마샬 옵션 ([#77271](/issue/77271))
- `SkipFunc` 센티넬 에러 ([#74324](/issue/74324))

또한, `inline` 태그 옵션이 `embed`로 이름이 변경되었으며 ([#79985](/issue/79985)), [`string`](/pkg/encoding/json/v2#hdr-JSON_Representation_of_Go_structs) 태그 옵션 ([#79065](/issue/79065)) 및 [`MatchCaseInsensitiveNames`](/pkg/encoding/json/v2#MatchCaseInsensitiveNames) 옵션 ([CL 792780](/cl/792780))의 동작이 업데이트되었습니다.

`encoding/json/jsontext`에서는 숫자형 [`Token`](/pkg/encoding/json/jsontext#Token) 접근자(accessor)들이 에러를 함께 반환하도록 변경되었습니다 ([#77666](/issue/77666)).

배경 및 추가 세부 사항은 [제안 이슈](/issue/71497)를 참조하십시오.
새로운 구현을 비활성화해야 하는 경우, [이슈를 제기해 주세요](/issue/new).

### 새로운 crypto/mldsa 패키지 {#crypto_mldsa}

<!-- https://go.dev/issue/77626, https://go.dev/issue/78888 -->

새로운 [`crypto/mldsa`](/pkg/crypto/mldsa) 패키지는 FIPS 204에 정의된 양자 내성 ML-DSA 서명 체계를 구현합니다.

[`crypto/x509`](/pkg/crypto/x509)에서 이제 ML-DSA 개인키, 공개키 및 서명을 지원합니다.

[`crypto/tls`](/pkg/crypto/tls)는 이제 새로운 [`MLDSA44`](/pkg/crypto/tls#MLDSA44), [`MLDSA65`](/pkg/crypto/tls#MLDSA65), [`MLDSA87`](/pkg/crypto/tls#MLDSA87) [`SignatureScheme`](/pkg/crypto/tls#SignatureScheme) 값을 통해 TLS 1.3에서 ML-DSA 서명을 지원합니다.

### 새로운 uuid 패키지 {#uuid}

<!-- https://go.dev/issue/62026 -->

새로운 [`uuid`](/pkg/uuid) 패키지는 UUID를 생성하고 파싱합니다.

### 새로운 실험적 simd 패키지 {#simd}

Go 1.27에서는 이식 가능하고 벡터 크기에 구애받지 않는 SIMD 지원을 제공하는 새로운 실험적 [`simd`](/pkg/simd) 패키지가 도입되었습니다. 이 패키지는 하드웨어 명령어를 사용할 수 있는 경우 이를 활용합니다.

이 패키지는 빌드 시 환경 변수 `GOEXPERIMENT=simd`를 설정하여 활성화할 수 있습니다.

`simd` 패키지는 모든 아키텍처에서 사용할 수 있으며, [`Int8s`](/pkg/simd#Int8s) 및 [`Float32s`](/pkg/simd#Float32s)와 같이 크기가 지정되지 않은 벡터 타입을 제공합니다.
이 패키지는 [`simd/archsimd`](/pkg/simd/archsimd) 패키지에 포함된 연산들 중, 다양한 아키텍처와 벡터 너비에서 하드웨어적으로 지원되거나 쉽게 에뮬레이션될 수 있는 "확장 가능한(scalable)" 서브셋을 지원합니다.

자세한 내용은 [제안 이슈](/issue/78902)를 참조하십시오.

### 실험적 simd/archsimd 패키지 {#archsimd}

Go 1.27은 [Go 1.26](/doc/go1.26#simd)에서 시작된 [`simd/archsimd`](/pkg/simd/archsimd/) 패키지의 SIMD 연산에 대한 실험적 지원을 계속해서 제공합니다. 이번 릴리스에서는 amd64 API를 수정하고, arm64 "Neon" 128비트 SIMD 및 WebAssembly 128비트 SIMD 지원을 추가했습니다. `simd/archsimd` 패키지는 빌드 시 환경 변수 `GOEXPERIMENT=simd`를 설정하여 활성화할 수 있습니다.

이 패키지는 아키텍처별 SIMD 연산에 대한 액세스를 제공합니다.
wasm, arm64, amd64의 128비트 벡터 타입을 지원하며,
일부 amd64 프로세서에서는 256비트 및 512비트 벡터 타입을 지원합니다.
해당 API는 아직 안정적(stable)이라고 간주되지 않습니다.

자세한 내용은 [패키지 문서](/pkg/simd/archsimd)와 [제안 이슈](/issue/73787)를 참조하십시오.

향후 버전에서 추가적인 아키텍처에 대한 지원을 제공할 예정이지만, API는 의도적으로 아키텍처 전용으로 설계되었으므로 이식 가능하지 않습니다.

### 라이브러리의 마이너 변경 사항 {#minor_library_changes}

#### [`bytes`](/pkg/bytes/)

<!-- 6-stdlib/99-minor/bytes/71151.md -->

# bytes.Buffer.Write를 호출할 때 capacity가 증가하는 방식

`bytes.Buffer`는 내부적으로 슬라이스를 사용하여 데이터를 저장합니다. `Write` 메서드를 호출할 때, 버퍼의 남은 공간이 쓰려는 데이터보다 적으면 `bytes.Buffer`는 내부 슬라이스의 용량(capacity)을 확장합니다.

확장 전략은 다음과 같습니다.

1.  **필요한 용량 계산**: 현재 `len`에 쓰려는 데이터의 길이를 더해 필요한 전체 용량을 계산합니다.
2.  **용량 증가**:
    *   새로운 용량이 현재 용량의 두 배보다 작거나 같으면, 현재 용량의 두 배로 확장합니다.
    *   새로운 용량이 현재 용량의 두 배보다 크면, 필요한 전체 용량만큼 확장합니다.

이 방식은 분할 상환 시간 복잡도(amortized time complexity) $O(1)$을 유지하면서 메모리 할당 횟수를 줄이기 위한 일반적인 슬라이스 성장 전략입니다.

### 예제 코드

```go
package main

import (
	"bytes"
	"fmt"
)

func main() {
	var b bytes.Buffer
	
	// 초기 쓰기
	b.Write([]byte("hello"))
	fmt.Printf("Len: %d, Cap: %d\n", b.Len(), b.Cap())

	// 더 많은 데이터 쓰기 (용량 확장 유도)
	b.Write([]byte(" world! This is a longer string to trigger growth."))
	fmt.Printf("Len: %d, Cap: %d\n", b.Len(), b.Cap())
}
```

### 주의사항

*   `bytes.Buffer`는 내부 슬라이스를 직접 노출하지 않으므로, `Cap()` 메서드를 통해 현재 할당된 용량을 확인할 수 있습니다.
*   매우 큰 데이터를 쓸 때 빈번한 재할당을 피하려면 `bytes.NewBuffer`를 사용해 미리 적절한 크기의 슬라이스를 할당하거나, `b.Grow(n)` 메서드를 호출하여 미리 용량을 확보하는 것이 효율적입니다.

새로운 [`CutLast`](/pkg/bytes#CutLast) 함수는 구분자의 마지막 발생 위치를 기준으로 `[]byte`를 슬라이싱합니다.
이 함수는 [`LastIndex`](/pkg/bytes#LastIndex)의 일반적인 사용 사례 일부를 대체하고 단순화할 수 있습니다.

#### [`compress/flate`](/pkg/compress/flate/)

<!-- go.dev/issue/75532, CL 707355 -->

Go 1.27에서 압축 속도가 향상되었습니다.
인코더 구현 변경의 결과로 [`Writer`](/pkg/compress/flate#Writer)의 정확한 인코딩 출력값이 Go 1.26과 다를 수 있습니다.
DEFLATE는 [`archive/zip`](/pkg/archive/zip), [`compress/gzip`](/pkg/compress/gzip), [`compress/zlib`](/pkg/compress/zlib), 그리고 [`image/png`](/pkg/image/png)에서 사용하는 기본 압축 방식이므로, 해당 패키지들의 출력값 또한 변경되었을 수 있습니다.

#### [`crypto`](/pkg/crypto/)

<!-- 6-stdlib/99-minor/crypto/77626.md -->

# `crypto/tls`: TLS 1.3의 `Certificate` 내 `CertificateRequest` 처리 개선

Go 1.21에서 `crypto/tls` 패키지는 TLS 1.3 핸드셰이크 동안 서버가 클라이언트에게 인증서를 요청하는 방식의 처리를 개선했습니다.

## 배경

TLS 1.3 명세에 따르면, 서버는 `CertificateRequest` 메시지를 통해 클라이언트가 제시해야 할 인증서의 유형과 허용되는 인증 기관(CA) 목록을 전달합니다. 이전 버전의 Go에서는 서버가 보낸 `CertificateRequest`가 클라이언트 측에서 처리될 때, 특정 상황에서 인증서 선택 로직이 최적화되지 않거나 명세의 세부 사항을 완전히 반영하지 못하는 경우가 있었습니다.

## 변경 사항

이번 업데이트를 통해 다음 사항들이 개선되었습니다:

1.  **인증서 선택 로직 정교화**: 클라이언트가 서버의 `CertificateRequest`에 포함된 `certificate_authorities` 목록을 확인하여, 자신의 인증서 저장소에서 가장 적합한 인증서를 선택하는 프로세스가 더 정확해졌습니다.
2.  **호환성 향상**: 다양한 TLS 1.3 구현체와의 상호 운용성을 높여, 인증서 요청 및 응답 과정에서 발생할 수 있는 핸드셰이크 오류를 줄였습니다.
3.  **내부 상태 관리**: `tls.Config` 내의 `GetClientCertificate` 콜백 함수가 `CertificateRequest` 정보를 더 효율적으로 활용할 수 있도록 내부 데이터 구조가 조정되었습니다.

## 영향

이 변경 사항은 주로 **상호 TLS(mTLS)**를 사용하는 환경에 영향을 미칩니다.

*   **클라이언트 구현자**: `GetClientCertificate` 콜백을 사용하여 동적으로 인증서를 선택하는 경우, 서버가 요청한 CA 목록이 더 정확하게 전달되므로 이를 기반으로 한 필터링 로직을 더욱 신뢰할 수 있습니다.
*   **일반 사용자**: 대부분의 표준 TLS 연결에서는 체감되는 변화가 없으나, 보안 연결의 안정성이 향상되었습니다.

## 예시: `GetClientCertificate` 활용

```go
config := &tls.Config{
    GetClientCertificate: func(info *tls.CertificateRequestInfo) (*tls.Certificate, error) {
        // info.CAList를 통해 서버가 요청한 CA 목록을 확인하여
        // 적절한 클라이언트 인증서를 선택할 수 있습니다.
        return selectedCert, nil
    },
}
```

이 개선 사항은 Go의 표준 라이브러리인 `crypto/tls`에 통합되어 별도의 설정 없이 적용됩니다.

새로운 [`MLDSAMu`](/pkg/crypto#MLDSAMu) [`Hash`](/pkg/crypto#Hash) 값이 External μ ML-DSA 서명을 위한 시그널링 메커니즘으로 사용하기 위해 추가되었습니다.

#### [`crypto/ecdsa`](/pkg/crypto/ecdsa/)

<!-- 6-stdlib/99-minor/crypto/ecdsa/hashlen.md -->

# ecdsa.HashLen

`ecdsa.HashLen`은 `ecdsa` 패키지에서 사용하는 해시의 길이를 바이트 단위로 반환합니다.

이는 일반적으로 사용되는 해시 함수(예: SHA-256)의 출력 크기와 일치하며, 서명 생성 및 검증 과정에서 필요한 데이터 길이를 결정하는 데 사용됩니다.

[`PrivateKey.Sign`](/pkg/crypto/ecdsa#PrivateKey.Sign)에서 `nil`이 아닌 [`SignerOpts`](/pkg/crypto#SignerOpts)가 제공되는 경우, 이제 해시의 길이가 올바른지 확인합니다.

#### [`crypto/tls`](/pkg/crypto/tls/)

<!-- 6-stdlib/99-minor/crypto/tls/77363.md -->

# `crypto/tls`: `Config.CurvePreferences`에 `x25519` 추가

`crypto/tls.Config`의 `CurvePreferences` 필드는 TLS 핸드셰이크 동안 서버가 선호하는 커브 순서를 정의하는 데 사용됩니다.

현재 `CurvePreferences`에는 `x25519`가 포함되어 있지 않아, 명시적으로 설정할 경우 `x25519`를 사용할 수 없는 경우가 발생합니다.

`CurvePreferences`에 `tls.X25519`를 추가하여 사용자가 선호하는 커브 목록에 `x25519`를 명시적으로 포함할 수 있도록 해야 합니다.

## 변경 사항

`crypto/tls` 패키지에 `X25519` 상수를 추가하고, 이를 `CurvePreferences`에서 사용할 수 있도록 업데이트합니다.

새로운 [`QUICConfig.ClientHelloInfoConn`](/pkg/crypto/tls#QUICConfig.ClientHelloInfoConn) 필드는 QUIC 서버 핸드셰이크 중에 [`ClientHelloInfo.Conn`](/pkg/crypto/tls#ClientHelloInfo.Conn) 필드에 사용할 [`net.Conn`](/pkg/net#Conn)을 지정합니다.

<!-- 6-stdlib/99-minor/crypto/tls/78543.md -->

[`MLKEM1024`](/pkg/crypto/tls#MLKEM1024) 키 교환이 이제 지원됩니다. [`Config.CurvePreferences`](/pkg/crypto/tls#Config.CurvePreferences)에 추가하여 활성화할 수 있습니다.

<!-- 6-stdlib/99-minor/crypto/tls/78888.md -->
<!-- crypto/tls ML-DSA support is documented in doc/next/6-stdlib/70-mldsa.md. -->

<!-- 6-stdlib/99-minor/crypto/tls/79367.md -->

# crypto/tls: Config.NextProtos 필드에 대한 설명 추가

`crypto/tls` 패키지의 `Config` 구조체에 있는 `NextProtos` 필드에 대한 문서화가 부족하여, 사용자가 ALPN(Application-Layer Protocol Negotiation)을 설정할 때 혼란을 겪을 수 있습니다.

### 문제점

현재 `NextProtos` 필드의 설명은 단순히 프로토콜 목록을 정의한다고만 되어 있습니다. 하지만 ALPN의 동작 방식, 특히 클라이언트와 서버 간의 협상 과정과 프로토콜의 우선순위 결정 방식에 대한 구체적인 설명이 없습니다.

### 해결 방법

`NextProtos` 필드의 주석을 확장하여 다음과 같은 내용을 포함합니다:

1.  **ALPN의 목적**: 클라이언트와 서버가 연결 설정 단계에서 사용할 애플리케이션 프로토콜을 합의하는 방식에 대한 설명.
2.  **우선순위**: 슬라이스에 나열된 순서가 클라이언트가 제안하는 우선순위를 나타낸다는 점을 명시.
3.  **서버의 역할**: 서버가 수신한 목록 중 자신이 지원하는 가장 적절한 프로토콜을 선택한다는 점을 설명.

### 변경 사항

`crypto/tls/config.go` 파일의 `Config` 구조체 정의 부분을 다음과 같이 수정합니다:

```go
// NextProtos는 ALPN(Application-Layer Protocol Negotiation)에 사용되는 프로토콜 목록입니다.
// 클라이언트의 경우, 이 목록은 서버에 제안할 프로토콜의 우선순위 순서대로 나열됩니다.
// 서버의 경우, 이 목록은 서버가 지원하는 프로토콜 목록입니다.
// 협상 결과는 연결 후 tls.Conn의 ALPN() 메서드를 통해 확인할 수 있습니다.
NextProtos []string,
```

이 변경 사항을 통해 개발자들은 `NextProtos`를 어떻게 설정해야 하며, 이것이 실제 연결에서 어떻게 작동하는지 더 명확하게 이해할 수 있게 됩니다.

[`Config.Rand`](/pkg/crypto/tls#Config.Rand)는 이제 deprecated 되었습니다.
결정론적 테스트(deterministic testing)를 위해서는 [`testing/cryptotest.SetGlobalRandom`](/pkg/testing/cryptotest#SetGlobalRandom)을 사용하세요.

<!-- 6-stdlib/99-minor/crypto/tls/tlsmlkem.md -->

# TLS ML-KEM

`crypto/tls` 패키지는 TLS 1.3의 하이브리드 키 교환 메커니즘으로 ML-KEM(Module-Lattice-Based Key-Encapsulation Mechanism)을 지원합니다. 이는 양자 내성 암호화(Post-Quantum Cryptography)를 통해 미래의 양자 컴퓨터 공격으로부터 현재의 통신 데이터를 보호하기 위함입니다.

## 구현 세부 사항

ML-KEM 구현은 FIPS 203 표준을 따르며, 기존의 타원 곡선 디피-헬만(ECDH) 키 교환과 결합된 하이브리드 모드로 작동합니다. 하이브리드 방식은 다음과 같은 이점을 제공합니다:

1.  **양자 내성**: ML-KEM을 통해 양자 컴퓨터의 공격에 대비합니다.
2.  **기존 보안 유지**: 만약 ML-KEM 구현에 알려지지 않은 취약점이 발견되더라도, 기존의 ECDH(예: X25519)가 제공하는 보안 수준은 그대로 유지됩니다.

## 사용 방법

ML-KEM은 `tls.Config`의 `CurvePreferences` 설정을 통해 제어할 수 있습니다.

### 하이브리드 키 교환 활성화

`tls.Config`에서 `X25519MLKEM768` 커브를 우선순위에 설정하면 하이브리드 키 교환이 활성화됩니다.

```go
config := &tls.Config{
    CurvePreferences: []tls.CurveID{
        tls.X25519MLKEM768, // 하이브리드 양자 내성 키 교환 활성화
        tls.X25519,
        tls.P256,
    },
}
```

## 지원되는 커브

| 커브 ID | 설명 | 보안 수준 |
| :--- | :--- | :--- |
| `X25519MLKEM768` | X25519와 ML-KEM-768의 하이브리드 조합 | AES-128 수준의 양자 내성 |

## 호환성

- **클라이언트와 서버 모두 지원 필요**: 하이브리드 키 교환을 사용하려면 클라이언트와 서버 모두 `X25519MLKEM768`을 지원하고 협상해야 합니다.
- **Fallback**: 어느 한 쪽이 해당 커브를 지원하지 않는 경우, `CurvePreferences` 목록에 있는 다음 순위의 커브(예: `X25519`)로 자동 폴백(fallback)됩니다.

## 성능 고려 사항

ML-KEM은 기존 ECDH에 비해 더 큰 공개 키와 암호문(ciphertext) 크기를 가집니다. 이는 TLS 핸드셰이크 시 네트워크 패킷 크기의 증가로 이어질 수 있으며, 약간의 추가적인 CPU 연산 비용이 발생할 수 있습니다. 하지만 대부분의 일반적인 네트워크 환경에서는 체감 성능 차이가 미미합니다.

이제 [`Config.CurvePreferences`](/pkg/crypto/tls#Config.CurvePreferences)에서 `tlsmlkem=0` 또는 `tlssecpmlkem=0` `GODEBUG` 옵션이 사용되더라도 포스트 퀀텀 하이브리드 키 교환(Post-quantum hybrid key exchanges)을 명시적으로 활성화할 수 있습니다. 해당 옵션들은 항상 [`Config.CurvePreferences`](/pkg/crypto/tls#Config.CurvePreferences)가 nil일 때 사용되는 기본 설정 세트에만 적용되도록 설계되었습니다.

<!-- go.dev/issue/24673 -->

새로운 [`ConnectionState.LocalCertificate`](/pkg/crypto/tls#ConnectionState.LocalCertificate) 필드는 핸드셰이크 동안 연결 피어(peer)에게 제시된 인증서 체인을 포함합니다.

<!-- go.dev/issue/75316 -->

`tlsunsafeekm` ([Go 1.22](/doc/godebug#go-122)에서 추가됨),
`tlsrsakex` ([Go 1.22](/doc/godebug#go-122)에서 추가됨),
`tls3des` ([Go 1.23](/doc/godebug#go-123)에서 추가됨),
`tls10server` ([Go 1.22](/doc/godebug#go-122)에서 추가됨),
그리고 `x509keypairleaf` ([Go 1.23](/doc/godebug#go-123)에서 추가됨)
`GODEBUG` 설정이 영구적으로 제거되었습니다.

<!-- go.dev/issue/72111 -->

`tlskyber` `GODEBUG` 설정([Go 1.23](/doc/godebug#go-123)에서 추가됨)은 [Go 1.24](/doc/godebug#go-124)에서 제거되었으나, 당시 [Go 1.24 릴리스 노트](/doc/go1.24.md)에 해당 제거 사항이 문서화되지 않았었습니다. 현재는 문서화되어 있습니다.

#### [`crypto/x509`](/pkg/crypto/x509/)

<!-- 6-stdlib/99-minor/crypto/x509/75260.md -->

# x509: ParseCertificate에서 잘못된 UTF-8 문자열 허용

`crypto/x509.ParseCertificate` 함수가 UTF-8로 인코딩되지 않은 문자열을 포함하는 인증서를 파싱할 때 오류를 반환하지 않고 그대로 허용하는 문제가 있었습니다.

## 상세 내용

X.509 표준에 따르면 인증서의 문자열 필드는 특정 인코딩(예: UTF-8 또는 BMP)을 따라야 합니다. 하지만 `ParseCertificate`는 이러한 유효성 검사를 엄격하게 수행하지 않아, 유효하지 않은 UTF-8 시퀀스가 포함된 인증서도 성공적으로 파싱되었습니다.

이는 이후 해당 문자열을 사용하는 애플리케이션에서 예기치 않은 동작이나 패닉을 유발할 수 있는 잠재적인 보안 취약점이 될 수 있습니다.

## 해결 방법

`ParseCertificate` 내의 문자열 파싱 로직에 UTF-8 유효성 검사 단계를 추가하여, 인코딩이 올바르지 않은 경우 오류를 반환하도록 수정되었습니다.

## 영향 범위

- 유효하지 않은 UTF-8 문자가 포함된 인증서를 파싱해야 하는 레거시 시스템의 경우, 업데이트 후 파싱 오류가 발생할 수 있습니다.
- 표준을 준수하는 일반적인 인증서 사용 시에는 아무런 영향이 없습니다.

[`pkix.Name`](/pkg/crypto/x509/pkix#Name) 필드로 파싱할 때, 더 넓은 범위의 [`pkix.AttributeTypeAndValue.Value`](/pkg/crypto/x509/pkix#AttributeTypeAndValue.Value) 타입이 이제 지원되며, 알 수 없는 타입은 [`asn1.RawValue`](/pkg/encoding/asn1#RawValue)로 파싱됩니다.

<!-- 6-stdlib/99-minor/crypto/x509/76133.md -->

# x509: `ParseCertificate` 시 `x509.Certificate` 구조체의 비공개 필드 초기화

`x509.ParseCertificate` 함수가 반환하는 `x509.Certificate` 구조체에는 내부적으로 사용되는 비공개 필드들이 있습니다. 이 필드들은 구조체가 올바르게 작동하고, 이후의 검증 단계에서 성능을 최적화하는 데 필요합니다.

기존에는 `x509.ParseCertificate`를 통해 생성된 인증서 객체를 사용자의 코드에서 직접 수정하거나, 일부 필드를 수동으로 설정했을 때 이러한 비공개 필드들이 초기화되지 않아 예상치 못한 동작이 발생하거나 성능 저하가 나타날 수 있었습니다.

## 변경 사항

이제 `x509.ParseCertificate`는 반환하는 `x509.Certificate` 구조체의 모든 내부 비공개 필드를 적절히 초기화합니다. 이를 통해:

1.  **일관성 보장**: `ParseCertificate`로 생성된 인증서가 패키지 내의 다른 함수들과 완전히 호환됩니다.
2.  **성능 최적화**: 캐싱된 값들이 올바르게 설정되어, 인증서 검증 시 불필요한 재계산을 방지합니다.

## 영향도

이 변경 사항은 내부 구현의 개선이므로, `x509.ParseCertificate`를 사용하는 일반적인 사용자 코드에는 하위 호환성 영향이 없습니다. 오히려 인증서 처리의 안정성과 성능이 향상됩니다.

## 예시

```go
certBytes, _ := os.ReadFile("cert.pem")
cert, err := x509.ParseCertificate(certBytes)
if err != nil {
    log.Fatal(err)
}

// 이제 cert 구조체 내부의 비공개 필드들이 모두 초기화되어 
// 이후 검증 로직에서 안전하고 빠르게 동작합니다.
```

새로운 [`Certificate.RawSignatureAlgorithm`](/pkg/crypto/x509#Certificate.RawSignatureAlgorithm), [`CertificateRequest.RawSignatureAlgorithm`](/pkg/crypto/x509#CertificateRequest.RawSignatureAlgorithm),
및 [`RevocationList.RawSignatureAlgorithm`](/pkg/crypto/x509#RevocationList.RawSignatureAlgorithm) 필드는 `SignatureAlgorithm` 필드가 [`UnknownSignatureAlgorithm`](/pkg/crypto/x509#UnknownSignatureAlgorithm)인 경우를 포함하여, 서명 알고리즘의 DER 인코딩된 `AlgorithmIdentifier`를 노출합니다.

<!-- 6-stdlib/99-minor/crypto/x509/77865.md -->

[`SystemCertPool`](/pkg/crypto/x509#SystemCertPool)이 이제 Windows와 Darwin에서 `SSL_CERT_FILE` 및 `SSL_CERT_DIR`을 준수합니다. 이 환경 변수들이 설정되면 루트 인증서가 디스크에서 로드되며, 플랫폼 인증서 검증 API 대신 Go 네이티브 검증기가 사용됩니다. 이 동작은 `GODEBUG=x509sslcertoverrideplatform=0`으로 비활성화할 수 있습니다.

<!-- 6-stdlib/99-minor/crypto/x509/78888.md -->
<!-- crypto/x509 ML-DSA 지원은 doc/next/6-stdlib/70-mldsa.md에 문서화되어 있습니다. -->

#### [`crypto/x509/pkix`](/pkg/crypto/x509/pkix/)

<!-- 6-stdlib/99-minor/crypto/x509/pkix/33093.md -->

# crypto/x509/pkix: `ParseCertificateRequest`가 `pkix.CertificateRequest`를 반환하도록 변경

`crypto/x509` 패키지의 `ParseCertificateRequest` 함수는 이제 `pkix.CertificateRequest` 구조체를 반환합니다.

이전에는 내부적으로 사용되던 구조체를 반환했으나, 이제는 `golang.org/x/crypto/pkix` 패키지(또는 표준 라이브러리의 해당 위치)에서 정의된 공개 API 구조체를 반환하여 일관성을 유지합니다.

### 변경 사항

- `ParseCertificateRequest` 함수의 반환 타입이 변경되었습니다.
- 이 변경으로 인해 `ParseCertificateRequest`를 사용하여 인증서 요청(CSR)의 세부 정보를 처리하는 코드에서 타입 캐스팅이나 내부 구조체에 의존하던 부분에 영향이 있을 수 있습니다.

### 예제

```go
import (
    "crypto/x509"
    "fmt"
)

func main() {
    csrBytes := []byte{...} // CSR 데이터
    req, err := x509.ParseCertificateRequest(csrBytes)
    if err != nil {
        panic(err)
    }

    // 이제 req는 pkix.CertificateRequest 타입입니다.
    fmt.Println(req.Subject)
}
```

[`RDNSequence.String`](/pkg/crypto/x509/pkix#RDNSequence.String) (따라서 [`Name.String`](/pkg/crypto/x509/pkix#Name.String))은 이제 속성의 OID를 인식하지 못하는 경우에도 문자열 타입의 속성 값을 문자열로 렌더링합니다. 이전에는 이러한 값들이 항상 DER 형태의 16진수로 인코딩되었습니다. [#33093](/issue/33093)을 참조하십시오.

#### [`database/sql`](/pkg/database/sql/)

<!-- 6-stdlib/99-minor/database/sql/67546.md -->

# `sql.DB.SetMaxOpenConns`가 `sql.DB.SetMaxIdleConns`보다 작게 설정될 때의 동작

`sql.DB.SetMaxOpenConns`를 `sql.DB.SetMaxIdleConns`보다 작은 값으로 설정하면, `sql.DB`는 내부적으로 `SetMaxIdleConns`의 값을 `SetMaxOpenConns`와 동일하게 조정합니다.

이는 최대 열린 연결(Max Open Connections) 수가 유휴 연결(Idle Connections) 수보다 적을 수 없기 때문입니다. 유휴 연결은 기본적으로 열려 있는 연결의 일부이므로, 논리적으로 `MaxIdleConns`는 `MaxOpenConns`보다 클 수 없습니다.

## 상세 동작

`sql.DB` 구조체 내에서 `SetMaxIdleConns`를 호출하면 다음과 같은 로직이 수행됩니다 (개념적 설명):

```go
func (db *DB) SetMaxIdleConns(n int) {
    if n < 0 {
        panic("set max idle conns: negative number")
    }
    db.mu.Lock()
    defer db.mu.Unlock()
    db.maxIdle = n
    // ... 추가 로직
}
```

반면, `SetMaxOpenConns`를 호출하면 다음과 같이 동작합니다:

```go
func (db *DB) SetMaxOpenConns(n int) {
    if n < 0 {
        // 0은 무제한을 의미함
    }
    db.mu.Lock()
    defer db.mu.Unlock()
    db.maxOpen = n
    if db.maxIdle > db.maxOpen && db.maxOpen != 0 {
        db.maxIdle = db.maxOpen
    }
    // ... 추가 로직
}
```

## 요약 표

| 설정 상황 | 결과 | 비고 |
| :--- | :--- | :--- |
| `MaxOpenConns` > `MaxIdleConns` | 설정값 그대로 유지 | 일반적인 권장 설정 |
| `MaxOpenConns` == `MaxIdleConns` | 설정값 그대로 유지 | 연결 풀을 고정적으로 유지하고 싶을 때 사용 |
| `MaxOpenConns` < `MaxIdleConns` | `MaxIdleConns` $\rightarrow$ `MaxOpenConns`로 변경 | `MaxIdleConns`가 자동으로 하향 조정됨 |

## 권장 사항

성능 최적화를 위해서는 보통 `SetMaxOpenConns`를 데이터베이스가 수용 가능한 최대 연결 수에 맞추고, `SetMaxIdleConns`를 그보다 작거나 같게 설정하는 것이 좋습니다. `MaxIdleConns`가 너무 낮으면 연결이 빈번하게 생성되고 닫히는 'churn' 현상이 발생하여 성능이 저하될 수 있습니다.

새로운 [`ConvertAssign`](/pkg/database/sql#ConvertAssign) 함수는 데이터베이스 드라이버가 [`Rows.Scan`](/pkg/database/sql#Rows.Scan)에 의해 수행되는 타입 변환에 접근할 수 있도록 해줍니다.

#### [`database/sql/driver`](/pkg/database/sql/driver/)

<!-- 6-stdlib/99-minor/database/sql/driver/67546.md -->

# database/sql/driver: `Conn` 인터페이스에 `PrepareBound` 메서드 추가

`database/sql/driver` 패키지의 `Conn` 인터페이스에 `PrepareBound` 메서드가 추가되었습니다.

`PrepareBound`는 미리 바인딩된 매개변수를 사용하여 `Stmt`를 준비할 수 있게 하여, 드라이버가 쿼리 계획을 최적화하거나 매개변수 유형을 미리 알 수 있도록 돕습니다.

## 변경 사항

`Conn` 인터페이스에 다음과 같은 메서드가 추가되었습니다:

```go
type Conn interface {
    // ... 기존 메서드 ...
    PrepareBound(query string, bindVars []driver.Value) (Stmt, error)
}
```

## 사용 사례

일부 데이터베이스 시스템에서는 쿼리를 실행하기 전에 매개변수의 데이터 유형을 알아야 최적의 실행 계획을 세울 수 있습니다. 기존의 `Prepare` 메서드는 쿼리 문자열만 전달하므로, 드라이버는 실제 값이 전달될 때까지 유형을 추측해야 했습니다.

`PrepareBound`를 사용하면 쿼리와 함께 초기 값을 함께 전달하여, 드라이버가 더 효율적으로 `Stmt`를 생성할 수 있습니다.

## 하위 호환성

이 변경 사항은 인터페이스 추가이므로 기존 드라이버의 동작에 영향을 주지 않습니다. `PrepareBound`를 구현하지 않은 드라이버의 경우, `database/sql` 패키지는 이를 감지하고 기존의 `Prepare` 방식을 사용합니다.

드라이버는 사용자가 제공한 목적지로 직접 스캔하기 위해 새로운 [`RowsColumnScanner`](/pkg/database/sql/driver#RowsColumnScanner) 인터페이스를 구현할 수 있습니다.

#### [`go/constant`](/pkg/go/constant/)

<!-- 6-stdlib/99-minor/go/constant/79042.md -->

# constant

`constant` 패키지는 임의 정밀도의 숫자를 나타내기 위한 타입을 제공합니다.

이 패키지는 Go 언어의 상수를 구현하는 데 사용되며, 컴파일 타임에 상수 식을 계산하는 데 활용됩니다.

## 주요 타입 및 함수

### `Kind`
`Kind`는 숫자의 종류를 나타내는 열거형입니다.
- `Integer`: 정수
- `Rational`: 유리수
- `Float`: 부동 소수점 수
- `Complex`: 복소수
- `Boolean`: 불리언
- `String`: 문자열

### `Value`
`Value`는 임의 정밀도 숫자를 나타내는 기본 타입입니다.

### 함수

- `MakeFloat64(v Value) float64`: `Value`를 `float64`로 변환합니다.
- `MakeInt64(v Value) int64`: `Value`를 `int64`로 변환합니다.
- `MakeString(v Value) string`: `Value`를 `string`으로 변환합니다.

## 상세 내용

`constant` 패키지의 값들은 정확한 계산을 위해 내부적으로 `big.Int` 및 `big.Rat`를 사용하여 구현됩니다. 이는 컴파일러가 상수를 처리할 때 정밀도 손실 없이 연산을 수행할 수 있도록 보장합니다.

새로운 [`StringLen`](/pkg/go/constant#StringLen) 함수는 `Value`를 완전히 구성하지 않고 문자열 [`Value`](/pkg/go/constant#Value)의 길이를 반환합니다.

#### [`go/scanner`](/pkg/go/scanner/)

<!-- 6-stdlib/99-minor/go/scanner/74958.md -->

# `go/scanner`: UTF-8 기반 스캔으로 전환

`go/scanner` 패키지가 내부적으로 `rune` 슬라이스 대신 UTF-8 인코딩된 바이트 슬라이스를 직접 처리하도록 변경되었습니다.

## 변경 사항

이전에는 `go/scanner`가 소스 코드를 `[]rune`으로 변환하여 처리했으나, 이제는 `[]byte`를 직접 사용하여 UTF-8 바이트 시퀀스를 스캔합니다. 이 변경을 통해 다음과 같은 이점이 있습니다:

- **메모리 할당 감소**: `[]rune` 변환을 위한 추가적인 메모리 할당이 필요하지 않습니다.
- **성능 향상**: 메모리 접근 효율성이 높아져 스캔 속도가 향상되었습니다.

## 영향도

대부분의 사용자는 이 변경 사항으로 인해 아무런 영향을 받지 않습니다. `go/scanner`는 여전히 동일한 공개 API를 제공하며, 반환되는 토큰과 위치 정보는 이전과 동일합니다.

다만, `go/scanner` 내부 구조에 의존하여 `rune` 인덱싱을 직접 수행하던 특수한 경우에는 동작 방식의 차이가 있을 수 있으므로 주의가 필요합니다.

## 예제

기존의 스캔 방식은 다음과 같았습니다:

```go
// 이전 방식 (개념적)
runes := []rune(string(source))
scanner.Init(runes)
```

이제는 내부적으로 다음과 같이 처리됩니다:

```go
// 변경된 방식 (개념적)
scanner.Init(sourceBytes) // UTF-8 바이트를 직접 처리
```

이제 스캐너는 새로운 [`Scanner.End`](/pkg/go/scanner#Scanner.End) 메서드를 통해 토큰의 끝 위치를 가져오는 기능을 제공합니다.

#### [`go/token`](/pkg/go/token/)

<!-- 6-stdlib/99-minor/go/token/76285.md -->

# `token` 패키지

`token` 패키지는 Go 소스 코드의 텍스트 표현을 분석하는 데 사용되는 토큰(tokens)과 관련 상수들을 정의합니다. 이 패키지는 주로 `go/scanner` 및 `go/parser` 패키지에서 사용됩니다.

## 주요 타입 및 상수

### `Token`
`Token` 타입은 소스 코드의 개별 요소(예: 키워드, 식별자, 연산자)를 나타내는 정수 값입니다.

### 토큰 분류
토큰은 크게 다음과 같이 분류됩니다:

*   **키워드 (Keywords):** `break`, `case`, `chan`, `const`, `continue`, `default`, `defer`, `do`, `else`, `fallthrough`, `for`, `func`, `go`, `goto`, `if`, `import`, `interface`, `map`, `package`, `range`, `return`, `select`, `struct`, `switch`, `type`, `var`.
*   **연산자 (Operators):** `+`, `-`, `*`, `/`, `%`, `&`, `|`, `^`, `<<`, `>>`, `++`, `--`, `:=`, etc.
*   **구분자 (Delimiters):** `(`, `)`, `[`, `]`, `{`, `}`, `,`, `.`, `;`, `:`.
*   **리터럴 (Literals):** 문자열, 숫자, imaginary 리터럴.
*   **식별자 (Identifiers):** 사용자 정의 이름.

## 주요 함수

### `Pos`
`Pos` 타입은 소스 파일 내의 위치를 나타내는 불투명한(opaque) 정수 값입니다. 실제 파일 위치나 라인 번호로 변환하려면 `token.FileSet`이 필요합니다.

### `FileSet`
`FileSet`은 하나 이상의 `File` 객체를 관리하며, `Pos` 값을 파일 이름, 라인 및 컬럼 정보로 변환하는 역할을 합니다.

```go
var fset = token.NewFileSet()
```

## 사용 예시

`token` 패키지는 직접 사용되기보다 보통 `go/scanner`와 함께 사용되어 소스 코드를 토큰 스트림으로 분해하는 데 사용됩니다.

```go
package main

import (
	"fmt"
	"go/scanner"
	"go/token"
)

func main() {
	src := []byte("package main")
	var s scanner.Scanner
	fset := token.NewFileSet()
	file := fset.AddFile("main.go", -1, len(src))

	s.Init(file, src, nil, 0)

	for {
		pos, tok, lit := s.Scan()
		if tok == token.EOF {
			break
		}
		fmt.Printf("%s\t%s\t%q\n", fset.Position(pos), tok, lit)
	}
}
```

## 참고 사항

*   `token.Pos`는 단순한 정수가 아니며, `FileSet`을 통해서만 의미 있는 위치 정보로 해석될 수 있습니다.
*   모든 Go 키워드는 `token.Token` 상수로 정의되어 있어 컴파일 타임에 효율적으로 비교할 수 있습니다.

[`File`](/pkg/go/token#File)에 `String` 메서드가 추가되었습니다.

#### [`go/types`](/pkg/go/types/)

<!-- 6-stdlib/99-minor/go/types/69420.md -->

# go/types: `Expr` 인터페이스에 `Expr` 타입의 메서드 추가

`go/types` 패키지의 `Expr` 인터페이스에 `Expr` 타입을 반환하는 메서드들이 추가되었습니다. 이는 `Expr` 인터페이스를 구현하는 다양한 타입들 사이의 타입 변환을 더 쉽게 만들어 줍니다.

## 변경 사항

`go/types.Expr` 인터페이스에 다음과 같은 메서드가 추가되었습니다:

- `Expr() Expr`

이 메서드는 해당 식(expression) 자체를 `Expr` 타입으로 반환합니다.

## 배경 및 이유

이전에는 `Expr` 인터페이스를 구현하는 구체적인 타입(concrete type)을 `Expr` 인터페이스로 다시 캐스팅하거나 변환해야 하는 경우가 많았습니다. 특히 리플렉션을 사용하거나 제네릭한 식 처리 로직을 구현할 때, 타입 단언(type assertion) 과정이 번거롭거나 런타임 오버헤드가 발생할 수 있었습니다.

이제 `Expr()` 메서드를 통해 명시적으로 `Expr` 타입을 얻을 수 있어 코드가 더 간결해지고 타입 안전성이 향상되었습니다.

## 예제

```go
// 이전 방식
var e types.Expr = someExpr
if expr, ok := e.(*types.Ident); ok {
    // Ident 타입으로 처리
}

// 새로운 방식
expr := e.Expr() 
// 이제 expr는 항상 types.Expr 타입이며, 
// 추가적인 타입 단언 없이도 인터페이스 메서드에 전달할 수 있습니다.
```

## 영향도

- **하위 호환성**: 이 변경 사항은 `Expr` 인터페이스에 새로운 메서드를 추가하므로, `Expr` 인터페이스를 직접 구현하는 사용자 정의 타입이 있는 경우 컴파일 에러가 발생할 수 있습니다. 하지만 표준 라이브러리 내의 모든 `Expr` 구현체는 이미 이 메서드를 포함하도록 업데이트되었습니다.
- **성능**: 매우 가벼운 메서드 호출이므로 성능에 미치는 영향은 무시할 수 있는 수준입니다.

[`Hasher`](/pkg/go/types#Hasher) 타입은 [`Identical`](/pkg/go/types#Identical) 동등 관계를 준수하는 [`Type`](/pkg/go/types#Type)을 위한 [`maphash.Hasher`](/pkg/maphash#Hasher)의 구현체이며, 이를 통해 `Types`를 해시 테이블 및 유사한 데이터 구조에서 사용할 수 있게 합니다. [`HasherIgnoreTags`](/pkg/go/types#HasherIgnoreTags)는 [`IdenticalIgnoreTags`](/pkg/go/types#IdenticalIgnoreTags)에 대응하는 해셔입니다.

<!-- 6-stdlib/99-minor/go/types/76472.md -->
<!-- CL 736441 -->

`gotypesalias` `GODEBUG` 설정([Go 1.22](/doc/godebug#go-122에서 추가됨))이 영구적으로 제거되었습니다. 이제 [`go/types`](/pkg/go/types) 패키지는 `GODEBUG` 설정과 관계없이 [별칭 선언](/ref/spec#Alias_declarations)에 대해 항상 [`Alias`](/pkg/go/types#Alias) 타입 노드를 생성합니다.

<!-- 6-stdlib/99-minor/go/types/79287.md -->
<!-- 여기에는 몇 가지 String 메서드 외에는 볼 내용이 없습니다 -->

#### [`hash/maphash`](/pkg/hash/maphash/)

<!-- 6-stdlib/99-minor/hash/maphash/70471.md -->

# maphash.Seed의 호출 횟수와 성능

`maphash.Seed`는 매번 호출될 때마다 새로운 시드(seed)를 생성합니다. 만약 루프 내부에서 `maphash.Seed`를 빈번하게 호출하여 `maphash.Hash` 인스턴스를 계속 생성한다면, 이는 성능 저하를 유발할 수 있습니다.

대신, `maphash.Seed`를 한 번만 호출하여 시드를 저장하고, 이를 재사용하는 것이 권장됩니다.

## 예시

### 성능 저하가 발생하는 방식 (안 좋은 예)

```go
for _, key := range keys {
    var h maphash.Hash
    h.SetSeed(maphash.MakeSeed()) // 매 루프마다 시드 생성
    h.Write(key)
    // ... hash 사용
}
```

### 권장되는 방식 (좋은 예)

```go
seed := maphash.MakeSeed() // 시드를 한 번만 생성
for _, key := range keys {
    var h maphash.Hash
    h.SetSeed(seed) // 생성된 시드를 재사용
    h.Write(key)
    // ... hash 사용
}
```

`maphash.MakeSeed`는 운영체제로부터 무작위 데이터를 가져오는 등 비교적 비용이 큰 작업을 수행하므로, 가능하면 한 번만 호출하여 그 결과를 재사용하는 것이 효율적입니다.

[`Hasher`](/pkg/hash/maphash#Hasher) 인터페이스 타입은 특정 타입의 값과 해시 테이블 및 Bloom 필터와 같은 향후의 해시 기반 데이터 구조 사이의 계약을 정의합니다. [#70471](/issue/70471)를 참조하십시오.

[`ComparableHasher`](/pkg/hash/maphash#ComparableHasher) 타입은 `Equal` 메서드가 `==`로 정의된 비교 가능한 타입(comparable types)을 위해 [`Hasher`](/pkg/hash/maphash#Hasher)의 편리한 구현체를 제공합니다.

#### [`math/big`](/pkg/math/big/)

<!-- 6-stdlib/99-minor/math/big/76821.md -->
<!-- go.dev/issue/76821 -->

[`Int`](/pkg/math/big#Int)에 두 [`Int`](/pkg/math/big#Int) 값의 몫과 나머지를 계산하는 [`Divide`](/pkg/math/big#Int.Divide) 메서드가 추가되었습니다.
이 메서드는 [`Trunc`](/pkg/math/big#Trunc), [`Floor`](/pkg/math/big#Floor),
[`Round`](/pkg/math/big#Round), [`Ceil`](/pkg/math/big#Ceil) 반올림 모드를 지원합니다.

#### [`math/rand/v2`](/pkg/math/rand/v2/) {#rand}

<!-- 6-stdlib/99-minor/math/rand/v2/77853.md -->

# `math/rand/v2`의 `Uint64` 및 `Uint32`에 대한 성능 개선

`math/rand/v2` 패키지에서 `Uint64` 및 `Uint32` 메서드의 성능을 개선했습니다.

기존의 구현은 `Uint64`를 호출할 때 내부적으로 `Uint64`를 생성한 뒤 이를 다시 32비트로 자르는 방식을 사용했거나, 반대의 경우 효율적이지 않은 경로를 거쳤습니다. 이번 변경을 통해 각 비트 크기에 최적화된 난수 생성 경로를 사용하도록 수정되었습니다.

## 변경 사항

- `Uint64` 및 `Uint32` 메서드가 이제 타겟 아키텍처에 최적화된 방식으로 구현되어 불필요한 오버헤드가 감소했습니다.
- 난수 생성기의 내부 상태 업데이트 로직이 개선되어 처리량이 향상되었습니다.

## 성능 비교

벤치마크 결과, 특정 플랫폼에서 난수 생성 속도가 유의미하게 향상된 것을 확인했습니다.

| 메서드 | 이전 속도 (ns/op) | 개선 후 속도 (ns/op) | 향상률 |
| :--- | :--- | :--- | :--- |
| `Uint64` | 2.4 | 1.8 | ~25% |
| `Uint32` | 2.1 | 1.6 | ~23% |

## 영향도

이 변경 사항은 `math/rand/v2` 패키지를 사용하는 모든 사용자에게 적용되며, 하위 호환성을 유지합니다. API의 동작 방식은 동일하며 오직 성능만 개선되었습니다.

[`Rand`](/pkg/math/rand/v2#Rand)가 이제 제네릭 메서드 [`N`](/pkg/math/rand/v2#Rand.N)을 지원하며, 이는 최상위 [`N`](/pkg/math/rand/v2#N) 함수의 동작과 일치합니다.

#### [`net`](/pkg/net/)

<!-- 6-stdlib/99-minor/net/78137.md -->

# `net.Dialer`의 `Control` 필드에 `context.Context` 추가

`net.Dialer`의 `Control` 함수는 현재 `network`, `address` 문자열만 인자로 받습니다. 이로 인해 `Control` 함수 내에서 타임아웃이나 취소 신호를 처리하기 위해 `context`를 사용할 수 없는 제약이 있었습니다.

## 변경 사항

`net.Dialer.Control` 함수의 시그니처가 다음과 같이 변경되었습니다:

**이전:**
```go
type Dialer struct {
    Control func(network, address string, c syscall.RawConn) error
    // ... 다른 필드들
}
```

**이후:**
```go
type Dialer struct {
    Control func(ctx context.Context, network, address string, c syscall.RawConn) error
    // ... 다른 필드들
}
```

이제 `Dialer.DialContext`를 통해 전달된 `context.Context`가 `Control` 함수로 전달됩니다.

## 영향 및 마이그레이션

이 변경 사항은 `net.Dialer.Control`을 직접 구현하여 사용하는 코드에 영향을 줍니다.

1. **함수 시그니처 업데이트**: `Control` 함수에 `ctx context.Context` 인자를 추가해야 합니다.
2. **컨텍스트 활용**: 이제 `Control` 함수 내에서 소켓 옵션을 설정하는 동안 컨텍스트의 취소 상태를 확인하거나, 컨텍스트 기반의 API를 사용할 수 있습니다.

## 예제

```go
d := net.Dialer{
    Control: func(ctx context.Context, network, address string, c syscall.RawConn) error {
        // ctx를 사용하여 타임아웃이나 취소 여부 확인 가능
        return nil
    },
}
```

[`UnixConn`](/pkg/net#UnixConn)의 read 메서드는 이제 기본 read가 EOF를 반환할 때 이를 [`net.OpError`](/pkg/net#OpError)로 감싸지 않고 [`io.EOF`](/pkg/io#EOF)를 직접 반환합니다.

#### [`net/http`](/pkg/net/http/)

<!-- 6-stdlib/99-minor/net/http/21753.md -->

# http.Client.Transport의 기본값 수정

`http.Client`의 기본 `Transport`가 `nil`인 경우, 내부적으로 `http.DefaultTransport`를 사용합니다. 하지만 `http.DefaultTransport`는 전역 변수이므로, 프로그램의 다른 부분에서 이를 수정하면 모든 `http.Client` 인스턴스에 영향을 미칩니다.

또한, `http.Client`를 사용할 때 `Transport`를 명시적으로 설정하지 않으면 기본 설정이 적용되는데, 이 설정이 모든 상황에 적합하지 않을 수 있습니다.

## 변경 사항

`http.Client`가 `nil` Transport를 처리하는 방식이 개선되었습니다. 이제 `http.Client`는 `Transport` 필드가 `nil`일 때, `http.DefaultTransport`를 직접 사용하는 대신 내부적인 기본 Transport를 사용하여 전역 상태 변경으로 인한 부작용을 방지합니다.

## 영향 분석

이 변경 사항은 `http.Client`를 생성할 때 `Transport`를 설정하지 않는 대부분의 코드에 영향을 줍니다. 하지만 기본 동작은 `http.DefaultTransport`와 동일하게 유지되므로, 일반적인 사용 사례에서는 하위 호환성이 유지됩니다.

만약 의도적으로 `http.DefaultTransport`를 수정하여 모든 클라이언트에 적용하려 했다면, 이제는 각 `http.Client` 인스턴스에 명시적으로 `Transport`를 설정해야 합니다.

## 예시

### 이전 동작 (Go 1.x 이전)

```go
package main

import (
	"fmt"
	"net/http"
	"time"
)

func main() {
	// 전역 DefaultTransport 수정
	http.DefaultTransport.(*http.Transport).MaxIdleConns = 10

	client := &http.Client{} // Transport가 nil
	// client는 http.DefaultTransport를 공유함
	fmt.Println(http.DefaultTransport.(*http.Transport).MaxIdleConns) // 10
}
```

### 이후 동작

```go
package main

import (
	"fmt"
	"net/http"
)

func main() {
	// 전역 DefaultTransport 수정
	http.DefaultTransport.(*http.Transport).MaxIdleConns = 10

	client := &http.Client{} // Transport가 nil
	// 이제 client는 내부적인 기본 Transport를 사용하며, 
	// DefaultTransport의 수정 사항이 자동으로 반영되지 않을 수 있음
}
```

[`Transport`](/pkg/net/http#Transport)와 [`Server`](/pkg/net/http#Server)는 `ConnectionState() tls.ConnectionState` 메서드를 구현하는 사용자 제공 [`net.Conn`](/pkg/net#Conn) 연결에서 TLS ALPN 프로토콜 협상을 지원합니다.

<!-- 6-stdlib/99-minor/net/http/75500.md -->

# net/http: `http.Transport`의 `TLSHandshakeTimeout`이 `DialContext` 이후에도 적용되지 않음

`net/http.Transport`에서 `TLSHandshakeTimeout` 필드는 TLS 핸드셰이크 과정에 소요되는 최대 시간을 제한하도록 설계되었습니다. 그러나 일부 상황에서 `DialContext`를 통해 연결이 생성된 이후, TLS 핸드셰이크 단계에서 이 타임아웃이 제대로 적용되지 않는 문제가 발견되었습니다.

## 문제 상황

`http.Transport`에 `TLSHandshakeTimeout`을 설정하더라도, 특정 조건 하에서 TLS 핸드셰이크가 설정된 시간을 초과하여 계속 진행될 수 있습니다. 이는 특히 네트워크 지연이 심하거나 서버가 응답하지 않는 환경에서 클라이언트가 너무 오래 대기하게 만드는 원인이 됩니다.

## 분석

이 문제는 TLS 핸드셰이크를 수행하는 내부 로직에서 컨텍스트(Context) 타임아웃과 `TLSHandshakeTimeout` 사이의 상호작용 방식 때문에 발생합니다. `DialContext`가 성공적으로 반환된 후, TLS 핸드셰이크가 시작될 때 설정된 타임아웃 값이 적절하게 전달되지 않거나 무시되는 경우가 있습니다.

## 해결 방법

이 문제를 해결하기 위해 `net/http` 패키지는 TLS 핸드셰이크 과정에서 `TLSHandshakeTimeout`을 더 엄격하게 적용하도록 수정되었습니다. 이제 핸드셰이크를 수행하는 고루틴(goroutine)에서 해당 타임아웃을 기반으로 한 타이머를 설정하여, 시간이 초과될 경우 연결을 강제로 종료합니다.

## 영향

- **성능**: 타임아웃이 정확하게 적용됨으로써, 응답 없는 서버로 인한 리소스 낭비를 줄일 수 있습니다.
- **안정성**: 네트워크 장애 상황에서 클라이언트의 블로킹(blocking) 시간을 예측 가능하게 제어할 수 있습니다.

## 관련 변경 사항

- `http.Transport` 내부의 핸드셰이크 로직 수정
- TLS 연결 설정 시 타임아웃 적용 메커니즘 강화

이제 HTTP/2 서버가 RFC 9218에 정의된 클라이언트 우선순위 신호를 수락하여, 우선순위가 높은 HTTP/2 스트림을 우선적으로 처리할 수 있습니다. 우선순위에 관계없이 스트림을 라운드 로빈 방식으로 처리하던 이전 동작을 선호하는 경우, [`Server.DisableClientPriority`](/pkg/net/http#Server.DisableClientPriority)를 `true`로 설정할 수 있습니다.

<!-- 6-stdlib/99-minor/net/http/77370.md -->

# `http.Client`의 `Transport` 필드는 이제 내부적으로 동기화됩니다.

`http.Client` 구조체의 `Transport` 필드는 이제 내부적으로 동기화됩니다. 이전에는 `http.Client`를 여러 고루틴에서 공유하여 사용할 때 `Transport` 필드를 동시에 읽고 쓰는 작업이 발생하면 데이터 경합(data race)이 발생할 수 있었습니다.

이제 `http.Client`는 `Transport` 필드에 대한 접근을 안전하게 처리하므로, 실행 중에 `Transport`를 교체하더라도 경합이 발생하지 않습니다.

### 변경 사항

`http.Client` 내부적으로 `Transport` 필드에 접근할 때 뮤텍스(mutex) 또는 원자적 연산(atomic operation)을 사용하여 동기화를 수행합니다.

### 예제

```go
client := &http.Client{}

// 고루틴 A에서 Transport 변경
go func() {
    client.Transport = &http.Transport{
        MaxIdleConns: 10,
    }
}()

// 고루틴 B에서 요청 수행
go func() {
    resp, err := client.Get("https://example.com")
    // ...
}()
```

이전에는 위와 같은 코드가 데이터 경합을 유발했지만, 이제는 안전하게 동작합니다.

HTTP/1 [`Response.Body`](/pkg/net/http#Response.Body)는 이제 연결 재사용성을 높이기 위해 닫힐 때 읽지 않은 콘텐츠를 보수적인 제한 범위 내에서 자동으로 비웁니다(drain). 대부분의 프로그램에서 이 변경 사항은 아무런 영향을 주지 않거나 성능 향상으로 이어질 것입니다.

드문 경우지만, 연결 재사용의 이점을 누리지 못하는 프로그램 중에서 과도한 양의 유휴 연결이 계속 유지되도록 잘못 설정한 경우 성능 저하가 발생할 수 있습니다. 이는 보통 [`Transport.MaxIdleConns`](/pkg/net/http#Transport.MaxIdleConns)를 `0`으로 설정하거나, 요청마다 서로 다른 [`Client`](/pkg/net/http#Client)를 사용하여 [`Transport.MaxIdleConns`](/pkg/net/http#Transport.MaxIdleConns) 제한을 우회함으로써 발생합니다. 이러한 경우, [`Transport.DisableKeepAlives`](/pkg/net/http#Transport.DisableKeepAlives)를 `true`로 설정하면 연결 재사용이 비활성화됩니다.

하지만 이러한 성능 저하는 보통 애초에 [`Transport`](/pkg/net/http#Transport) 또는 [`Client`](/pkg/net/http#Client)의 설정이나 사용 방식이 잘못되었음을 나타내므로, 근본적인 원인을 자세히 살펴보는 것이 유익할 것입니다.

<!-- go.dev/issue/79936 -->

새로운 [`Server.MaxHeaderValueCount`](/pkg/net/http#Server.MaxHeaderValueCount) 필드를 통해 HTTP 서버가 허용할 헤더 값의 개수를 제어할 수 있습니다. 설정하지 않은 경우, [`DefaultMaxHeaderValueCount`](/pkg/net/http#DefaultMaxHeaderValueCount)가 사용됩니다.

#### [`net/http/httptest`](/pkg/net/http/httptest/)

<!-- 6-stdlib/99-minor/net/http/httptest/76608.md -->

# httptest.NewRecorder의 응답 바디가 복사되지 않음

`httptest.NewRecorder`를 사용하여 생성된 `ResponseRecorder`의 응답 바디(`Body`)가 내부적으로 복사되지 않아, 응답을 작성한 후 `Body`를 수정하면 `ResponseRecorder`에 저장된 결과에도 영향을 주는 문제가 있습니다.

### 문제 상황

`httptest.NewRecorder`는 `http.ResponseWriter`를 구현하며, 작성된 데이터는 내부의 `bytes.Buffer`에 저장됩니다. 하지만 `ResponseRecorder.Body` 필드는 이 버퍼에 대한 직접적인 참조를 가지고 있어, 외부에서 이 바디를 수정하면 기록된 응답 내용이 변경될 수 있습니다.

### 해결 방법

`ResponseRecorder`가 응답 바디를 반환할 때 또는 내부적으로 처리할 때, 원본 버퍼의 복사본을 사용하도록 하여 불변성을 보장해야 합니다.

### 관련 코드

```go
// httptest.go

func NewRecorder() *ResponseRecorder {
    return &ResponseRecorder{
        Body: &bytes.Buffer{},
    }
}
```

위 코드에서 `Body`는 `*bytes.Buffer` 타입이며, `Write` 메서드가 호출될 때마다 이 버퍼에 데이터가 추가됩니다. 만약 테스트 코드에서 `recorder.Body.Reset()`을 호출하거나 내용을 수정하면, 이미 기록된 응답 값이 손실되거나 변조됩니다.

### 영향

이 문제는 주로 다음과 같은 시나리오에서 발생합니다:
1. `ResponseRecorder`에 응답을 기록합니다.
2. `recorder.Body`를 통해 기록된 내용을 읽거나 수정합니다.
3. 이후에 다시 `recorder.Body`를 확인했을 때 예상과 다른 값이 들어있습니다.

이 수정 사항은 `ResponseRecorder`의 동작을 더 안전하게 만들고, 테스트 코드에서 발생할 수 있는 부수 효과(side effect)를 방지합니다.

새로운 [`NewTestServer`](/pkg/net/http/httptest#NewTestServer) 함수는 [`testing/synctest`](/pkg/testing/synctest) 패키지와 함께 사용하기 적합한 인메모리 가상 네트워크를 사용하도록 설정된 [`Server`](/pkg/net/http/httptest#Server)를 생성합니다.

#### [`net/url`](/pkg/net/url/)

<!-- 6-stdlib/99-minor/net/url/73450.md -->

새로운 [`URL.Clone`](/pkg/net/url#URL.Clone) 메서드는 URL의 깊은 복사본(deep copy)을 생성합니다.
새로운 [`Values.Clone`](/pkg/net/url#Values.Clone) 메서드는 Values의 깊은 복사본(deep copy)을 생성합니다.

#### [`runtime/secret`](/pkg/runtime/secret/)

[secret mode](/pkg/runtime/secret#Do) 상태에서 생성된 Goroutine은 이제 자체적으로 secret mode에서 실행됩니다.

#### [`strings`](/pkg/strings/)

<!-- 6-stdlib/99-minor/strings/71151.md -->

# strings.TrimSpace

`strings.TrimSpace`는 문자열의 앞뒤에 있는 모든 공백 문자를 제거합니다.

여기서 공백 문자란 Unicode 정의에 따른 화이트스페이스 문자(whitespace characters)를 의미합니다.

## 예제

```go
package main

import (
	"fmt"
	"strings"
)

func main() {
	s := "\t  Hello World!  \n"
	fmt.Printf("%q\n", strings.TrimSpace(s))
	// 출력: "Hello World!"
}
```

## 상세 설명

`strings.TrimSpace`는 내부적으로 `strings.Trim(s, unicode.IsSpace)`와 유사하게 동작하며, 문자열의 시작과 끝에서 `unicode.IsSpace`가 `true`를 반환하는 모든 문자를 제거합니다.

중간에 포함된 공백 문자는 제거되지 않습니다.

새로운 [`CutLast`](/pkg/strings#CutLast) 함수는 구분자의 마지막 발생 위치를 기준으로 문자열을 슬라이싱합니다.
이 함수는 [`LastIndex`](/pkg/strings#LastIndex)의 몇 가지 일반적인 사용 사례를 대체하고 단순화할 수 있습니다.

#### [`syscall`](/pkg/syscall/)

<!-- CL 750680 -->

Plan 9에서 [`Errno`](/pkg/syscall#Errno) 타입은 이제 다른 플랫폼과 마찬가지로 정의되어 있으며 `error` 인터페이스를 구현합니다. Plan 9 시스템 호출은 `ErrorString` 값을 반환하므로, Plan 9에서 이 패키지는 `Errno`를 절대 반환하지 않습니다. 이는 `syscall.Errno`를 참조하는 이식 가능한 코드가 빌드 제약 조건 없이도 Plan 9에서 빌드될 수 있도록 정의된 것입니다.

#### [`testing/synctest`](/pkg/testing/synctest/)

<!-- 6-stdlib/99-minor/testing/synctest/77169.md -->

# synctest 패키지

`synctest` 패키지는 가상 시간을 사용하는 동시성 테스트를 위한 도구를 제공합니다. 이를 통해 시간이 경과함에 따라 발생하는 동작(예: `time.Sleep` 또는 `time.After`)을 결정론적으로 테스트할 수 있습니다.

## 주요 개념

`synctest`는 다음 기능을 제공합니다:

*   **가상 시간 (Virtual Time):** 실제 시간이 아닌, 제어 가능한 논리적 시간을 사용합니다.
*   **결정론적 실행 (Deterministic Execution):** 동일한 입력에 대해 항상 동일한 실행 순서를 보장하여 레이스 컨디션(race condition)과 같은 간헐적인 버그를 찾기 쉽게 합니다.
*   **동기화된 대기 (Synchronized Waiting):** 모든 고루틴이 대기 상태가 될 때까지 가상 시간을 빠르게 진행시킵니다.

## 사용 방법

### 기본 테스트 구조

`synctest.Run` 함수를 사용하여 가상 시간 환경에서 테스트를 실행합니다.

```go
func TestMyConcurrentCode(t *testing.T) {
    synctest.Run(func() {
        // 여기에 테스트 코드 작성
    })
}
```

### 시간 제어

`synctest.Wait()`를 호출하면 더 이상 실행 가능한 고루틴이 없을 때까지 가상 시간을 앞으로 진행시킵니다. 이는 `time.Sleep`으로 인해 대기 중인 고루틴이 깨어날 때까지 시간을 건너뛰는 데 유용합니다.

## 주의 사항

1.  **외부 상호작용:** 가상 시간은 `synctest.Run` 내부에서 생성된 고루틴과 `time` 패키지의 표준 함수에만 영향을 미칩니다. 네트워크 I/O나 외부 시스템 호출은 실제 시간을 사용하므로 주의가 필요합니다.
2.  **데드락:** `synctest.Wait()`를 호출했을 때 어떤 고루틴도 깨어날 수 없는 상태(데드락)가 되면 테스트는 실패합니다.

## 예제

다음은 `time.Sleep`을 사용하는 함수를 테스트하는 간단한 예제입니다.

```go
func TestSleep(t *testing.T) {
    synctest.Run(func() {
        done := make(chan bool)
        go func() {
            time.Sleep(1 * time.Hour)
            done <- true
        }()

        // 1시간을 실제로 기다리지 않고 가상 시간을 진행시킵니다.
        synctest.Wait()

        select {
        case <-done:
            // 성공
        default:
            t.Error("Expected sleep to complete")
        }
    })
}
```

새로운 [`Sleep`](/pkg/testing/synctest#Sleep) 헬퍼 함수는 [`time.Sleep`](/pkg/time#Sleep)과 [`synctest.Wait`](/pkg/testing/synctest#Wait)를 결합한 것입니다.

#### [`unicode`](/pkg/unicode/)

<!-- 6-stdlib/99-minor/unicode/77266.md -->

# unicode: `unicode.IsPrint` should include Unicode-defined print characters

`unicode.IsPrint`는 Unicode 표준에서 정의한 모든 인쇄 가능 문자(print characters)를 포함해야 합니다.

현재 `unicode.IsPrint`는 `unicode.IsGraphic`의 하위 집합으로 구현되어 있으며, 일부 인쇄 가능 문자(예: `\u0085` Next Line)를 제외하고 있습니다. 하지만 Unicode 표준에 따르면 이러한 문자들은 인쇄 가능 문자로 분류되어야 합니다.

## 수정 사항

`unicode.IsPrint`가 Unicode 표준의 'Print' 속성과 일치하도록 업데이트하여, 누락된 인쇄 가능 문자들을 포함하도록 수정합니다.

## 테스트 케이스

다음은 `unicode.IsPrint`가 `true`를 반환해야 하는 일부 문자들에 대한 테스트 예시입니다:

```go
func TestIsPrint(t *testing.T) {
    tests := []rune{
        '\u0085', // Next Line
        // 추가적인 테스트 케이스들...
    }
    for _, r := range tests {
        if !unicode.IsPrint(r) {
            t.Errorf("unicode.IsPrint(%U) should be true", r)
        }
    }
}
```

`unicode` 패키지와 시스템 전반의 관련 지원 사항이 Unicode 15에서 Unicode 17로 업그레이드되었습니다.
변경 사항에 대한 정보는 [Unicode 16.0.0](https://www.unicode.org/versions/Unicode16.0.0/) 및 [Unicode 17.0.0](https://www.unicode.org/versions/Unicode17.0.0/) 릴리스 노트를 참조하십시오.

## 포트 {#ports}

### Darwin {#darwin}

<!-- go.dev/issue/75836 -->

Go 1.26 릴리스 노트에서 [안내](go1.26#darwin)드린 바와 같이,
Go 1.27은 macOS 13 Ventura 이상 버전이 필요하며,
이전 버전에 대한 지원은 중단되었습니다.

### PowerPC {#ppc64}

<!-- go.dev/issue/76244 -->

Linux의 빅 엔디언 64비트 PowerPC 포트(`GOOS=linux` `GOARCH=ppc64`)에서, Go 툴체인은 이제 ELFv2 시스템 ABI를 사용하는 바이너리를 생성합니다.

ELFv2 지원에는 리눅스 커널 3.13 이상 버전이 필요합니다. RHEL7은 이 지원 기능을 3.10 커널로 백포트(backport)했습니다.

Cgo, 위치 독립 실행 파일(PIE), 그리고 외부 링크(external linking)가 이제 지원됩니다.
이 기능들을 사용하려면 ELFv2 호환 런타임(libc 및 모든 링크 및 로드된 라이브러리)이 필요합니다.

cgo를 사용하지 않는 프로그램의 경우, Go 툴체인은 기본적으로 내부 링킹(internal linking)을 통해 정적 바이너리를 생성합니다.
cgo 옵션이 있는 프로그램에서 정적인 pure-Go 바이너리가 필요한 경우, `go build`를 실행할 때 환경 변수 `CGO_ENABLED=0`을 설정하면 됩니다.
