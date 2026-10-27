```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.27 소개 {#introduction}

가장 최신 Go 릴리스, 버전 1.27은 [2026년 8월](/doc/devel/release#go1.27.0)에 출시되며, [Go 1.26](/doc/go1.26) 이후 6개월 후입니다.
대부분의 변경 사항은 툴체인, 런타임 및 라이브러리의 구현에 있습니다.
항상과 마찬가지로, 이 릴리스는 Go 1의 [호환성 약속](/doc/go1compat)을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일 및 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

<!-- go.dev/issue/77273 -->

Go 1.27 이제 [일반 메서드](/issue/77273)를 지원합니다:
[메서드 선언](/ref/spec#Method_declarations)은 자체의
[타입 매개변수](/ref/spec#Type_parameter_declarations)를 선언할 수 있습니다.
이것은 널리 기대되었던 변경 사항으로, 특정 데이터 타입의 네임스페이스 내에서 일반 함수를 추가할 수 있게 되었습니다. 이전에 이러한 함수는 전체 패키지의 범위를 가지고 선언해야 했습니다.
예를 들어, `math/rand/v2`는 이제 `(*Rand) N[Int intType](Int) Int`라는 일반 메서드를 선언하지만, 이전에 `N[Int intType](Int) Int`라는 일반 함수만 가지고 있었습니다 (자세한 내용은 [아래](#rand) 참조).
참고로, [인터페이스](/ref/spec#Interface_types)의 메서드는 타입 매개변수를 선언할 수 없으며, 인터페이스 메서드는 일반 메서드에 의해 구현될 수 없습니다.

<!-- go.dev/issue/9859 -->

`struct` 리터럴의 키는 이제 해당 `struct` 유형의 유효한 [필드 선택자](/issue/9859)가 될 수 있으며, (최상위) `struct` 필드의 이름뿐만 아니라 모든 필드를 선택할 수 있습니다.

<!-- go.dev/issue/77245 -->

함수 타입 추론이 일반화되어, (일반 함수가) 변수에 할당되거나 (일반 함수 타입과) 일치하는 함수 타입으로 변환될 때, 모든 컨텍스트에서 적용될 수 있습니다. [참조/spec#Assignability](https://github.com/golang/go/issues/77245)

## 도구 {#tools}

<!-- go.dev/issue/77177 -->

다음 도구(`compile`, `link`, `asm`, `cgo`, `cover`, `pack`)에서 응답 파일 (`@file`) 파싱이 이제 지원됩니다.
응답 파일에는 공백으로 구분된 인자와 단일 따옴표 및 이중 따옴표 문자열, 이스케이프 시퀀스, 백슬래시-새 줄 연속을 지원합니다.
이는 기존 빌드 시스템과의 호환성을 보장하기 위해 GCC의 응답 파일 구현과 호환되는 형식을 사용합니다.

### Go 명령어 {#go-command}

<!-- go.dev/issue/78090 -->

`go` 명령은 이제 `bzr` 버전 관리 시스템에 대한 지원을 더 이상 제공하지 않습니다.
더 이상 `bzr` 서버에 호스팅된 모듈을 직접 가져올 수 없습니다.

#### `GODEBUG`

<!-- go.dev/issue/79422 -->

Go 1.27부터 `go` 명령어는 `GODEBUG` 설정을 인식합니다. 이 설정을 지원 중단한 설정(예: `asynctimerchan`, 자세한 내용은 [아래](#runtime) 참조)이 `go.mod` 파일(`godebug` 항목)과 `.go` 소스 파일(`//go:debug` 주석)에 나타나는 경우에만 인식합니다.
이러한 설정은 제거되기 전에 확립된 최종 기본값으로 설정된 경우에만 유효합니다.
그렇지 않은 경우, `go` 명령어는 오류를 반환합니다.
이 변경은 [Go 1 호환성 보장](/doc/go1compat)의 정신에 부합하며, 기존 프로그램이 지원되는 `GODEBUG` 설정을 설정하고, 해당 설정을 지원 중단한 경우에도 변경 없이 빌드하고 실행할 수 있도록 합니다.

#### `go test`

`go test`는 이제 기본적으로 `stdversion` 검사를 실행합니다.
이는 현재 실행 중인 Go 버전에서 참조 파일에 사용된 표준 라이브러리 심볼이 너무 최신 버전이 아닌 경우를 보고합니다.
이는 `go.mod` 파일의 `go` 지시어 및 파일에 적용된 빌드 태그를 통해 확인됩니다.

<!-- go.dev/issue/62728 -->

`go test -json`는 이제 `"Action":"output"` 줄을 추가적인 필드 `"OutputType"`로 표시하며, 출력 유형을 지정합니다.
현재 가능한 값은 "error", "error-continue", 및 "frame"입니다.
자세한 내용은 [cmd/test2json 도움말](/cmd/test2json#hdr-Output_Format)을 참조하십시오.

#### `go doc`

`go doc` 명령어는 Go 패키지의 문서화 기능을 제공합니다.

<!-- go.dev/issue/63696 -->

`go doc` 명령은 이제 `package@version` 구문을 지원합니다. 예를 들어, `go doc example.com/pkg@v1.2.3`와 같이 사용할 수 있습니다.

<!-- go.dev/issue/26715 -->

`go doc` 명령어는 이제 주어진 패키지 또는 심볼의 실행 가능한 예제를 나열하기 위한 `-ex` 명령줄 옵션을 지원합니다.
명령줄에 예제 이름을 전달하면 (예: `go doc bytes.ExampleBuffer`), `go doc`는 주석과 함께 예제 소스 코드를 출력합니다.

#### `go fix`

`go fix` 명령어는 여러 새로운 현대화 도구(`atomictypes`, `embedlit`, `slicesbackward`, `unsafefuncs`)를 포함합니다.

<!-- go.dev/issue/77581 -->

기존의 `fmtappendf` 분석기는 스타일 관련 문제로 인해 제거되었습니다.

기존의 `waitgroup` 분석기는 명확성을 위해 `waitgroupgo`로 이름이 변경되었습니다.

#### `go mod tidy`

<!-- go.dev/issue/56471 -->

`go mod tidy` 명령은 `go.mod` 파일에 `go 1.27` 또는 그 이상의 버전을 지정하는 모듈의 경우, 이제 중복된 `require` 블록을 자동으로 병합합니다. 이를 통해 파일이 깨끗하고 표준적인 구조를 유지하며, 최대 두 개의 `require` 블록을 포함하도록 합니다:
- 직접 종속성을 위한 블록
- 간접 종속성을 위한 블록

기존에 종속성에 연결된 주석 블록은 이 과정에서 유지됩니다. 만약 주석 블록이 직접 및 간접 종속성을 모두 포함하는 여러 지시어와 연결되어 있다면, 해당 주석 블록은 병합되어 새 직접 종속성 블록에 연결됩니다.

이전에는 `go.mod` 파일에 여러 개의 분리된 `require` 블록이 쌓이면 (대부분 수동 편집, 해결되지 않은 Git 병합 충돌, 또는 이전 버전 업그레이드 때문)
`go mod tidy`는 추가 블록을 그대로 두거나, 의도치 않게 새로운 블록을 생성했습니다. 이제 이 도구는 엄격하게 두 블록 레이아웃을 적용하여, 서로 다른 요구 사항을 해당 블록으로 통합하고, 모듈 파일의 구조를 자동으로 정리합니다.

### Go 스타일 자동 포맷팅 도구 (Gofmt) {#gofmt}

<!-- go.dev/issue/77959, CL 752862 -->

이 릴리스에는 `gofmt` (및 [`go/format`](/pkg/go/format))에서 열 정렬을 결정하는 데 사용되는 논리의 수정 사항이 포함되어 있습니다.
이전 논리는 `gofmt`의 동작이 CPU 아키텍처에 따라 약간씩 다르게 만드는 원인이었습니다.
새로운 논리는 소수의 파일에 대해 정렬 결정을 변경하므로, Go 1.27 이상에서 이전에 포맷된 코드에 대해 `gofmt`를 실행하면 약간의 공백 변경이 발생할 수 있습니다.

### 수의사 {#vet}

<!-- go.dev/issue/61342, CL 761240 -->

`[printf](https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/printf)`
분석기는 다음과 같은 호출을 보고합니다. `fmt.Errorf("...: %w", p)` 여기서 `%w` 연산자 `p`는 `*E` 유형이고, `E` 유형 자체는 `error` 인터페이스를 구현합니다. 이 방식으로 포인터를 감싸는 것은 일반적으로 잠재적인 버그이며, 특정 오류 유형 (예: 유형 변환 또는 `errors.Is` 호출)을 테스트하는 작업에서 의도하지 않은 실패를 유발합니다.

### 추적

<!-- go.dev/issue/78921 -->

`go tool trace`의 `-http` 명령줄 옵션은 포트만 지정하는 경우 (예: `-http=:6060`)에만 청취 주소를 localhost로 제한합니다.
이 변경 사항은 `go tool trace`를 `go tool pprof`의 `-http` 플래그의 동작과 일치시킵니다.
모든 주소에서 청취하려면 지정된 주소를 명시적으로 포함해야 합니다 (예: `-http=0.0.0.0:6060`).

## 실행 시간 {#runtime}

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, world!")
}
```

<!-- CL 742580 -->

`go` 지시어를 사용하여 Go 1.27 이상을 구성하는 모듈의 트레이스백에는 이제 [`runtime/pprof`](https://pkg.go.dev/runtime/pprof)의 고루틴 레이블이 헤더 라인에 포함됩니다. 이 동작은 `tracebacklabels=0` `GODEBUG` 설정을 사용하여 비활성화할 수 있습니다 (Go 1.26에 추가됨 [Go 1.26](/doc/godebug#go-126)). 고루틴 레이블이 민감한 정보를 획득하여 트레이스백에 공개해서는 안 되는 경우, 이러한 동작은 영구적으로 유지됩니다.

<!-- CL 781580 -->

`asynctimerchan`의 `GODEBUG` 설정 (Go 1.23에 추가됨: [/doc/godebug#go-123])
는 영구적으로 제거되었습니다. [time](https://pkg.go.dev/time) 패키지로 생성된 채널은 이제 `GODEBUG` 설정과 관계없이 항상 버퍼되지 않습니다 (동기).

### 더 빠른 메모리 할당

<!-- go.dev/issue/79286 -->

컴파일러는 이제 크기별 메모 할당 루틴에 대한 호출을 생성하여, 일부 작은 (<80 바이트) 메모 할당 비용을 최대 30%까지 줄입니다.
개선 사항은 워크로드에 따라 다르지만, 전반적인 개선은 실제 할당이 많은 프로그램에서 약 1%로 예상됩니다.
이는 바이너리 크기를 약 60 KB 증가시킵니다 (워크로드에 관계없이).
어떤 문제가 발생하면 [이슈를 제출해주세요](/issue/new).
빌드 시 `GOEXPERIMENT=nosizespecializedmalloc`를 설정하여 비활성화할 수 있습니다.
이 옵트아웃 설정은 Go 1.28에서 제거될 것으로 예상됩니다.

### 고루틴 누수 프로파일 {#goroutineleak-profiles}

<!-- go.dev/issue/74609 -->

새로운 프로파일 유형으로, 이전에는 [Go 1.26](/doc/go1.26#goroutineleak-profiles)에서 실험적으로 제공되었던 누수된 고루틴을 보고하는 기능이 이제 일반적으로 사용 가능합니다.
새로운 프로파일 유형인 `goroutineleak`은 [`runtime/pprof`](/pkg/runtime/pprof) 패키지에서 지원됩니다.
또한, [`net/http/pprof`](/pkg/net/http/pprof) 엔드포인트 `/debug/pprof/goroutineleak`에서도 사용할 수 있습니다.

*누수된* goroutine은 특정 동시성 원리 (채널, [`sync.Mutex`](/pkg/sync#Mutex), [`sync.Cond`](/pkg/sync#Cond) 등)에서 차단된 goroutine입니다.
이 goroutine은 결코 차단되지 않습니다.
런타임은 가비지 컬렉터를 사용하여 누수된 goroutine을 감지합니다. 만약 goroutine G가 동시성 원리 P에서 차단되어 있고, P가 실행 가능한 다른 goroutine이나 *그것으로* 차단될 수 있는 다른 goroutine으로부터 도달 불가능하다면, P는 차단될 수 없으므로, goroutine G는 절대 깨어나지 않습니다.
모든 경우에 영구적으로 차단된 goroutine을 감지하는 것은 불가능하지만, 이 접근 방식은 이러한 누수의 큰 범위를 감지합니다.

이 기술은 접근성을 기반으로 하기 때문에, 런타임은 전역 변수 또는 실행 가능한 goroutine의 로컬 변수를 통해 접근 가능한 동시성 원자리에 차단으로 인해 발생하는 누출을 식별하지 못할 수 있습니다.

[Go 1.26 릴리스 노트](/doc/go1.26#goroutineleak-profiles)를 참조하세요.

특히 Uber의 Vlad Saioc 님께 감사의 말씀을 전합니다.

`goroutineleakprofile`의 `GOEXPERIMENT` 설정이 삭제되었습니다.

## 컴파일러 {#compiler}

컴파일러는 이제 `//line` 또는 `/*line*/` 지시문의 파일이 포함된 디렉터리에 상대 파일 이름을 해결합니다. 이는 [`go/scanner`](/pkg/go/scanner)의 동작과 동일합니다. 절대 파일 이름은 변경되지 않습니다.
자세한 내용은 [#70478](/issue/70478)를 참조하십시오.

<!-- go.dev/issue/60324, CL 770200 -->

컴파일러는 이제 함수 리터럴(클로저)에 더 간단한 이름을 생성합니다.
이전에는, 감싸는 함수가 인라인되면, 함수 리터럴의 이름이 상당히 길어질 수 있습니다.
이제 컴파일러는 인라인 여부에 관계없이 함수 리터럴에 동일한 이름을 선택합니다.
또한 감싸는 함수가 인라인될 때, 동일한 함수 리터럴의 여러 인스턴스를 결합하여 컴파일된 바이너리에서 동일한 코드를 공유할 수 있습니다.
이 변경은 Go 코드의 기능을 변경하지 않습니다.
심볼 이름 확인을 위한 테스트는 업데이트가 필요할 수 있지만, 함수 리터럴의 이름을 의존하지 않는 것이 좋습니다.
[잘못된 방법](/pkg/reflect#Value.Pointer)으로 함수 코드 포인터를 사용하여 동일성을 비교하는 프로그램의 경우, Go 1.27에서는 다양한 캡쳐된 클로저 데이터를 가진 함수 리터럴이 더 많은 경우에 동일한 코드 포인터를 가질 수 있으므로 문제가 더 두드러질 수 있습니다.

## 링크 편집기 {#linker}

<!-- CL 751260, go.dev/issue/58722 -->

macOS를 대상으로 할 때, 링크러는 이제 `-macos` 및 `-macsdk` 명령줄 옵션을 허용합니다. 이러한 옵션은 `LC_BUILD_VERSION` 로드 명령에 OS 및 SDK 버전을 지정합니다.

기본적으로, 최신 지원되는 macOS 버전 (현재 [13.0.0](#darwin)) 및 최신 SDK 버전 (현재 26.2.0)을 선택합니다.

## 표준 라이브러리 {#library}

### 새로운 encoding/json/v2 및 encoding/json/jsontext 패키지 {#jsonv2}

<!-- go.dev/issue/71497 -->

다음 두 개의 새 패키지가 이제 사용 가능합니다:

- 패키지 `encoding/json/v2`는 `encoding/json`의 주요 개선 버전입니다. `Marshal` ( `/pkg/encoding/json/v2#Marshal`), `MarshalWrite` ( `/pkg/encoding/json/v2#MarshalWrite`), `MarshalEncode` ( `/pkg/encoding/json/v2#MarshalEncode`), `Unmarshal` ( `/pkg/encoding/json/v2#Unmarshal`), `UnmarshalRead` ( `/pkg/encoding/json/v2#UnmarshalRead`), 그리고 `UnmarshalDecode` ( `/pkg/encoding/json/v2#UnmarshalDecode`)와 같은 함수를 제공하며, 이 함수들은 다양한 `Options` ( `/pkg/encoding/json/v2#Options`) 인수를 받아 매핑 및 역매핑 동작을 구성할 수 있습니다.

- `encoding/json/jsontext` 패키지
    는 JSON에 대한 저수준의 구문 처리를 제공합니다.
    `Encoder` 및 `Decoder` 타입은 JSON을
    `Token` 및 `Value`의
    시퀀스로 처리하며, 생성되거나 소비되는 시퀀스가 유효한 JSON 텍스트인지 확인하기 위해 상태 머신을 유지합니다.

v2 패키지는 v1보다 더 엄격하고 상호 운용성이 높은 기본 설정을 선택합니다:
`encoding/json` 패키지(`/pkg/encoding/json#hdr-Migrating_to_v2`)의
전체적인 동작 방식 차이와 이를 조정하는 데 사용할 수 있는 옵션에 대한
자세한 내용은 v1 패키지 설명서를 참조하십시오.
v2 패키지는 JSON 문자열에서 유효하지 않은 UTF-8을 거부하고,
JSON 객체 내에서 중복된 이름을 거부합니다.

[`encoding/json`](/pkg/encoding/json) 패키지는 이제 v2 구현을 사용합니다. 직렬화 및 역직렬화 동작은 유지되지만, 오류 메시지의 정확한 내용은 다를 수 있습니다. 패키지는 또한 v2를 v1 의미론과 함께 작동하도록 구성할 수 있는 수많은 새로운 [`Options`](/pkg/encoding/json#Options)를 얻습니다. 이를 통해 새로운 API로의 완전한 마이그레이션 없이 v2를 사용할 수 있습니다.
v1 API는 계속 지원되며, 사용자는 마이그레이션할 필요가 없습니다.

`Marshal` 성능은 이전 구현과 유사하며, `Unmarshal` 성능은 훨씬 빠릅니다.

사용자가 새로운 구현과 관련된 호환성 문제를 겪을 경우, 빌드 시 `GOEXPERIMENT=nojsonv2`를 설정하여 비활성화할 수 있으며, 이를 통해 원래의 v1 구현을 복원할 수 있습니다.
이 옵션 사용을 중단하는 기능은 향후 릴리스에서 제거될 예정입니다.

다음은 `encoding/json/v2`의 주요 변경 사항입니다. `GOEXPERIMENT` 과정에서 다음과 같은 기능이 제거되었습니다:
* `format` 태그 옵션 ([#79071](/issue/79071)),
* `unknown` 태그 옵션 ([#77271](/issue/77271)),
* `DiscardUnknownMembers` 매샬 옵션 ([#77271](/issue/77271)),
* `SkipFunc` 센트널 에러 ([#74324](/issue/74324)).

또한, `inline` 태그 옵션이 `embed`로 이름이 변경되었습니다 ([#79985](/issue/79985)),
그리고 [`string`](/pkg/encoding/json/v2#hdr-JSON_Representation_of_Go_structs)
태그 옵션에 대한 동작이 업데이트되었습니다 ([#79065](/issue/79065)),
그리고 [`MatchCaseInsensitiveNames`](/pkg/encoding/json/v2#MatchCaseInsensitiveNames)
옵션 ([CL 792780](/cl/792780))이 변경되었습니다.

`encoding/json/jsontext`에서는 숫자 `Token` 액세서가 에러를 반환하도록 변경되었습니다 ([#77666](/issue/77666)).

자세한 내용 및 추가 정보는 [제안 사항]( /issue/71497)을 참조하십시오.
새로운 구현을 비활성화해야 하는 경우, [새로운 이슈를 제출하십시오]( /issue/new).

### 새로운 crypto/mldsa 패키지 {#crypto_mldsa}

<!-- https://go.dev/issue/77626, https://go.dev/issue/78888 -->

새로운 [`crypto/mldsa`](/pkg/crypto/mldsa) 패키지는 FIPS 204에 명시된, 후-양자 머신 러닝-DSA 서명
스키마를 구현합니다.

[`crypto/x509`](/pkg/crypto/x509)는 이제 ML-DSA 개인 키, 공개 키 및 서명을 지원합니다.

[`crypto/tls`](/pkg/crypto/tls)는 이제 TLS 1.3에서 ML-DSA 서명을 지원하며, 새로운
[`MLDSA44`](/pkg/crypto/tls#MLDSA44), [`MLDSA65`](/pkg/crypto/tls#MLDSA65),
그리고 [`MLDSA87`](/pkg/crypto/tls#MLDSA87) [`SignatureScheme`](/pkg/crypto/tls#SignatureScheme) 값을 사용합니다.

### 새 uuid 패키지 {#uuid}

```go
package main

import (
	"fmt"
	"github.com/google/uuid"
)

func main() {
	id, err := uuid.New()
	if err != nil {
		fmt.Println("uuid.New() error:", err)
		return
	}
	fmt.Println("새로운 UUID:", id)

	uid, err := uuid.Parse("a1b2c3d4-e5f6-7890-1234-567890abcdef")
	if err != nil {
		fmt.Println("uuid.Parse() error:", err)
		return
	}
	fmt.Println("파싱된 UUID:", uid)
}
```

<!-- https://go.dev/issue/62026 -->

새로운 [`uuid`](/pkg/uuid) 패키지는 UUID를 생성하고 파싱합니다.

### 새로운 실험적 SIMD 패키지 {#simd}

Go 1.27은 새로운 실험적인 [`simd`](/pkg/simd) 패키지를 도입합니다. 이 패키지는 이식 가능하고 벡터 크기에 독립적인 SIMD 지원을 제공합니다.
사용 가능한 경우 하드웨어 명령어를 사용합니다.
이 패키지는 빌드 시 환경 변수 `GOEXPERIMENT=simd`를 설정하여 활성화할 수 있습니다.

`simd` 패키지는 모든 아키텍처에서 사용 가능하며, [`Int8s`](/pkg/simd#Int8s) 및 [`Float32s`](/pkg/simd#Float32s)와 같은 특정 크기의 벡터 유형을 제공합니다.
이 패키지는 [`simd/archsimd`](/pkg/simd/archsimd) 패키지에 존재하는 하드웨어에서 지원되거나, 다양한 아키텍처 및 벡터 너비에서 쉽게 에뮬레이션될 수 있는 "확장 가능한" 일부 연산을 지원합니다.

자세한 내용은 [제안 이슈](/issue/78902)를 참조하십시오.

### 실험적인 simd/archsimd 패키지 {#archsimd}

Go 1.27은 [`simd/archsimd`](/pkg/simd/archsimd/) 패키지에서 시작된 SIMD 연산에 대한 실험적인 지원을 계속합니다 (Go 1.26 참조: [Go 1.26](/doc/go1.26#simd)).
이번 릴리스는 amd64 API를 수정하고 arm64 "Neon" 128-bit SIMD 및 WebAssembly 128-bit SIMD에 대한 지원을 추가합니다.
`simd/archsimd` 패키지는 빌드 시간에 환경 변수 `GOEXPERIMENT=simd`를 설정하여 활성화합니다.

이 패키지는 아키텍처별 SIMD 연산에 대한 액세스를 제공합니다.
wasm, arm64, amd64에서 128비트 벡터 유형을 지원하며, 일부 amd64 프로세서에서는 256비트 및 512비트 벡터 유형을 지원합니다.
API는 아직 안정적인 것으로 간주되지 않습니다.

자세한 내용은 [패키지 문서](https://example.com/pkg/simd/archsimd) 및 [제안 이슈](https://example.com/issue/73787)를 참조하십시오.

향후 버전에서 추가 아키텍처를 지원할 계획이지만, API는 의도적으로 특정 아키텍처에 맞춰 설계되었으므로 이식성이 없습니다.

### 라이브러리의 미세 조정 {#minor_library_changes}

#### [`bytes`](/pkg/bytes/)

<!-- 6-stdlib/99-minor/bytes/71151.md -->

새로운 `[`CutLast`](/pkg/bytes#CutLast) 함수는 구분자를 기준으로 `[]byte`를 잘라냅니다.
이는 `LastIndex`](/pkg/bytes#LastIndex)의 일부 일반적인 사용 사례를 대체하고 단순화할 수 있습니다.

#### [`compress/flate`](/pkg/compress/flate/)

<!-- go.dev/issue/75532, CL 707355 -->

Go 1.27에서 압축 속도가 향상되었습니다.
[`Writer`](/pkg/compress/flate#Writer)에서 생성된 정확한 인코딩된 출력은 Go 1.26과 다를 수 있습니다.
이는 인코더 구현 변경으로 인해 발생합니다.
DEFLATE는 [`archive/zip`](/pkg/archive/zip), [`compress/gzip`](/pkg/compress/gzip), [`compress/zlib`](/pkg/compress/zlib), 및 [`image/png`](/pkg/image/png)에서 사용되는 기본 압축 알고리즘이므로, 이러한 패키지에서 생성된 출력도 변경되었을 수 있습니다.

```
#### [`crypto`](/pkg/crypto/)
```

<!-- 6-stdlib/99-minor/crypto/77626.md -->

새로운 [`MLDSAMu`](/pkg/crypto#MLDSAMu) [`Hash`](/pkg/crypto#Hash) 값은 외부 μ ML-DSA 서명에 대한 신호 메커니즘으로 사용하기 위해 추가되었습니다.

#### [`crypto/ecdsa`](/pkg/crypto/ecdsa/)

<!-- 6-stdlib/99-minor/crypto/ecdsa/hashlen.md -->

[`PrivateKey.Sign`](/pkg/crypto/ecdsa#PrivateKey.Sign)는 이제 해시의 길이가 올바른지 확인합니다.
만약 `nil`이 아닌 [`SignerOpts`](/pkg/crypto#SignerOpts)가 제공되면.

#### [`crypto/tls`](/pkg/crypto/tls/)

<!-- 6-stdlib/99-minor/crypto/tls/77363.md -->

새로운 [`QUICConfig.ClientHelloInfoConn`](/pkg/crypto/tls#QUICConfig.ClientHelloInfoConn) 필드는 [`net.Conn`](/pkg/net#Conn)를 사용하여 [`ClientHelloInfo.Conn`](/pkg/crypto/tls#ClientHelloInfo.Conn) 필드를 지정합니다. 이는 QUIC 서버 핸드셰이딩 중에 사용됩니다.

<!-- 6-stdlib/99-minor/crypto/tls/78543.md -->

[`MLKEM1024`](/pkg/crypto/tls#MLKEM1024) 키 교환이 이제 지원됩니다. `Config.CurvePreferences`에 추가하여 활성화할 수 있습니다.

<!-- 6-stdlib/99-minor/crypto/tls/78888.md -->
<!-- crypto/tls ML-DSA 지원에 대한 정보는 doc/next/6-stdlib/70-mldsa.md에 설명되어 있습니다. -->

<!-- 6-stdlib/99-minor/crypto/tls/79367.md -->

[`Config.Rand`](/pkg/crypto/tls#Config.Rand)는 더 이상 사용되지 않습니다.
확실한 테스트를 위해 [`testing/cryptotest.SetGlobalRandom`](/pkg/testing/cryptotest#SetGlobalRandom)을 사용하세요.

<!-- 6-stdlib/99-minor/crypto/tls/tlsmlkem.md -->

다음과 같은 `Post-quantum hybrid key exchanges`는 이제 [`Config.CurvePreferences`](/pkg/crypto/tls#Config.CurvePreferences)에서 명시적으로 활성화할 수 있습니다. `tlsmlkem=0` 또는 `tlssecpmlkem=0` `GODEBUG` 옵션이 사용되더라도 그렇습니다. 이러한 옵션은 항상 기본으로 사용되는 설정에만 적용되도록 설계되었습니다.

<!-- go.dev/issue/24673 -->

새로운 [`ConnectionState.LocalCertificate`](/pkg/crypto/tls#ConnectionState.LocalCertificate)
필드는 연결 상대방에게 핸드셰이크 중에 제시된 인증서 체인을 포함합니다.

<!-- go.dev/issue/75316 -->

`tlsunsafeekm` (Go 1.22에 추가됨, [Go 1.22](/doc/godebug#go-122)),
`tlsrsakex` (Go 1.22에 추가됨, [Go 1.22](/doc/godebug#go-122)),
`tls3des` (Go 1.23에 추가됨, [Go 1.23](/doc/godebug#go-123)),
`tls10server` (Go 1.22에 추가됨, [Go 1.22](/doc/godebug#go-122)),
그리고 `x509keypairleaf` (Go 1.23에 추가됨, [Go 1.23](/doc/godebug#go-123))
`GODEBUG` 설정이 영구적으로 제거되었습니다.

<!-- go.dev/issue/72111 -->

`tlskyber`의 `GODEBUG` 설정 (Go 1.23에 추가됨 [Go 1.23](/doc/godebug#go-123))
은 Go 1.24에서 제거되었지만, Go 1.24에 대한 [릴리스 노트](/doc/go1.24.md)에는 당시 제거에 대한 설명이 없었습니다.
이제 설명이 추가되었습니다.

#### [`crypto/x509`](/pkg/crypto/x509/)

<!-- 6-stdlib/99-minor/crypto/x509/75260.md -->

`pkix.Name` 필드로 파싱할 때,
더 다양한 `pkix.AttributeTypeAndValue.Value`
형식이 지원되며, 알 수 없는 유형은 `asn1.RawValue`로 파싱됩니다.

<!-- 6-stdlib/99-minor/crypto/x509/76133.md -->

새로운 [`Certificate.RawSignatureAlgorithm`](/pkg/crypto/x509#Certificate.RawSignatureAlgorithm), [`CertificateRequest.RawSignatureAlgorithm`](/pkg/crypto/x509#CertificateRequest.RawSignatureAlgorithm),
및 [`RevocationList.RawSignatureAlgorithm`](/pkg/crypto/x509#RevocationList.RawSignatureAlgorithm) 필드는 서명 알고리즘의 DER 인코딩된
AlgorithmIdentifier를 노출하며, 여기에는
`SignatureAlgorithm` 필드가 [`UnknownSignatureAlgorithm`](/pkg/crypto/x509#UnknownSignatureAlgorithm)일 때도 포함됩니다.

<!-- 6-stdlib/99-minor/crypto/x509/77865.md -->

## X509 인증서 구조

X509 인증서는 다음과 같은 구조를 가집니다.

*   **버전:** 인증서의 형식을 지정합니다. (예: 01, 02)
*   **제네릭 이름 (General Name):** 인증서가 적용되는 도메인 이름을 지정합니다.
*   **사용 목적 (Purpose):** 인증서의 사용 목적을 지정합니다 (예: 인증서, 코드 서명).
*   **시작 날짜 및 만료 날짜:** 인증서의 유효 기간을 지정합니다.
*   **인증서 서명:** 인증서의 무결성을 보장하기 위한 디지털 서명입니다.
*   **인증 기관 (Issuer):** 인증서를 발급한 기관의 정보입니다.
*   **주체 (Subject):** 인증서의 소유자 (예: 웹 서버, 사용자)의 정보입니다.
*   **인증서 공개 키:** 인증서의 공개 키입니다.

**예시:**

```
-----BEGIN CERTIFICATE-----
MIIDATCCAFODg4AMCPQpW441Y+N+28v/MA0KCRwEAq8+LwW/K85g9cQ3gJ9896
D5Qz+gR9XkAM5C2F2zD8/5e/Vp4f/8qK+kQ9qVl9fFjNq0pY56eE8W8Q8B5M
.... (생략) ....
zJ/dYV3oWj/19o68R0
-----END CERTIFICATE-----
```

이 예시에서:

*   `MIIDATCCAFODg4AMCPQpW441Y+N+28v/MA0KCRwEAq8+LwW/K85g9cQ3gJ9896D5Qz+gR9XkAM5C2F2zD8/5e/Vp4f/8qK+kQ9qVl9fFjNq0pY56eE8W8Q8B5M....zJ/dYV3oWj/19o68R0`는 인증서의 내용을 나타냅니다.
*   `-----BEGIN CERTIFICATE-----` 및 `-----END CERTIFICATE-----`는 인증서의 시작 및 종료를 나타냅니다.

## X509 인증서의 사용

X509 인증서는 다음과 같은 목적으로 사용됩니다.

*   **SSL/TLS:** 웹 브라우저와 웹 서버 간의 안전한 통신을 위한 암호화 프로토콜.
*   **코드 서명:** 소프트웨어의 무결성을 보장하기 위한 디지털 서명.
*   **전자 서명:** 전자 문서의 무결성을 보장하기 위한 디지털 서명.
*   **인증서 발급:** 사용자 또는 조직의 신원을 확인하기 위한 인증서.

[`SystemCertPool`](/pkg/crypto/x509#SystemCertPool)는 Windows 및 Darwin에서 `SSL_CERT_FILE` 및 `SSL_CERT_DIR` 환경 변수를 이제 인식합니다. 이러한 환경 변수가 설정되면, 루트 인증서는 디스크에서 로드되고, 플랫폼 인증서 검증 API 대신, 네이티브 Go 검증기가 사용됩니다. 이 동작은 `GODEBUG=x509sslcertoverrideplatform=0`로 비활성화할 수 있습니다.

<!-- 6-stdlib/99-minor/crypto/x509/78888.md -->
<!-- crypto/x509 ML-DSA 지원에 대한 자세한 내용은 doc/next/6-stdlib/70-mldsa.md에서 확인할 수 있습니다. -->

#### [`crypto/x509/pkix`](/pkg/crypto/x509/pkix/)

<!-- 6-stdlib/99-minor/crypto/x509/pkix/33093.md -->

[`RDNSequence.String`](/pkg/crypto/x509/pkix#RDNSequence.String) (그리고 따라서 [`Name.String`](/pkg/crypto/x509/pkix#Name.String))는 이제 속성의 OID가 인식되지 않아도 속성의 값을 문자열로 렌더링합니다.
이전에는 이러한 값은 항상 DER 형식에서 16진수로 인코딩되었습니다.
자세한 내용은 [#33093](/issue/33093)를 참조하세요.

#### [`database/sql`](/pkg/database/sql/)

<!-- 6-stdlib/99-minor/database/sql/67546.md -->

새로운 [`ConvertAssign`](/pkg/database/sql#ConvertAssign) 함수는 데이터베이스 드라이버에게 [`Rows.Scan`](/pkg/database/sql#Rows.Scan)에서 수행되는 타입 변환에 대한 액세스를 제공합니다.

#### [`database/sql/driver`](/pkg/database/sql/driver/)

<!-- 6-stdlib/99-minor/database/sql/driver/67546.md -->

운전자는 새 [`RowsColumnScanner`](/pkg/database/sql/driver#RowsColumnScanner) 인터페이스를 구현하여 사용자 지정 대상에 직접 스캔할 수 있습니다.

#### [`go/constant`](/pkg/go/constant/)

<!-- 6-stdlib/99-minor/go/constant/79042.md -->

## 상수 (Constants)

Go 언어에서 상수는 컴파일 시점에 결정되는 값입니다. 이 값은 프로그램의 실행 중에 변경될 수 없습니다.

### 상수를 선언하는 방법

상수를 선언하는 방법은 다음과 같습니다.

```go
const 상수이름 상수값
```

예:

```go
const PI float64 = 3.14159
const MAX_INT int = 2147483647
```

### 상수의 종류

Go 언어에서 상수는 다음과 같은 종류가 있습니다.

*   `iota`
*   `bool`
*   `int`
*   `uint`
*   `float64`
*   `string`

### 주의 사항

*   상수는 컴파일 시점에 결정되므로, 프로그램의 실행 중에 변경할 수 없습니다.
*   상수의 이름은 영문, 숫자, 밑줄(_)로 구성될 수 있습니다.
*   상수의 값은 특정 자료형으로 지정해야 합니다.

### 예제

```go
package main

import "fmt"

func main() {
    const message string = "Hello, World!"
    fmt.Println(message)
}
```

이 코드는 "Hello, World!" 문자열을 상수 `message`에 저장하고, `fmt.Println()` 함수를 사용하여 콘솔에 출력합니다.

새로운 [`StringLen`](/pkg/go/constant#StringLen) 함수는 `Value`를 완전히 구성하지 않고 문자열의 길이를 반환합니다.

#### [`go/scanner`](/pkg/go/scanner/)

<!-- 6-stdlib/99-minor/go/scanner/74958.md -->

스캐너는 이제 새로운 [`Scanner.End`](/pkg/go/scanner#Scanner.End) 메서드를 통해 토큰의 끝 위치를 가져올 수 있습니다.

#### [`go/token`](/pkg/go/token/)

<!-- 6-stdlib/99-minor/go/token/76285.md -->

[`File`](/pkg/go/token#File)에 이제 `String` 메서드가 추가되었습니다.

#### [`go/types`](/pkg/go/types/)

<!-- 6-stdlib/99-minor/go/types/69420.md -->

## 69420

이 문서는 Go의 정수 타입과 관련하여 설명합니다.

### 정수 타입

Go는 다음과 같은 정수 타입을 제공합니다.

* `int`: 64비트 정수
* `int8`: 8비트 정수 (-128 ~ 127)
* `int16`: 16비트 정수 (-32768 ~ 32767)
* `int32`: 32비트 정수 (-2147483648 ~ 2147483647)
* `int64`: 64비트 정수 (-9223372036854775808 ~ 9223372036854775807)
* `uint`: 64비트 부호 없는 정수 (0 ~ 18446744073709551615)
* `uint8`: 8비트 부호 없는 정수 (0 ~ 255)
* `uint16`: 16비트 부호 없는 정수 (0 ~ 65535)
* `uint32`: 32비트 부호 없는 정수 (0 ~ 4294967295)
* `uint64`: 64비트 부호 없는 정수 (0 ~ 18446744073709551615)

### const 키워드

`const` 키워드는 상수 값을 정의하는 데 사용됩니다. 상수 값은 컴파일 시간에 결정되므로 런타임에 변경할 수 없습니다.

```go
const PI float64 = 3.14159
```

### 타입 추론

Go는 컴파일 시간에 변수의 타입을 추론할 수 있습니다. 즉, 변수를 선언할 때 타입을 명시적으로 지정하지 않아도 Go가 자동으로 타입을 결정합니다.

```go
var x int = 10
```

이 경우, Go는 `x`의 타입을 `int`로 추론합니다.

### 타입 강제 변환

Go는 타입 강제 변환을 지원합니다. 즉, 한 타입의 값을 다른 타입으로 변환할 수 있습니다.

```go
var x int = 10
var y float64 = float64(x)
```

이 경우, `x`의 값을 `float64`로 변환합니다.

### 포인터

포인터는 메모리 주소를 가리키는 변수입니다. 포인터를 사용하여 다른 변수의 값을 수정하거나, 함수에 데이터를 전달할 수 있습니다.

```go
var x int = 10
var y *int = &x
*y = 20
```

이 경우, `y`는 `x`의 메모리 주소를 가리키고, `y`의 값을 20으로 변경합니다.

[`Hasher`](/pkg/go/types#Hasher) 유형은 [`maphash.Hasher`](/pkg/maphash#Hasher)의 구현으로, [`Type`](/pkg/go/types#Type)에 대해 [`Identical`](/pkg/go/types#Identical) 관계를 준수하며, 이를 통해 `Types`를 해시 테이블 및 유사한 데이터 구조에서 사용할 수 있습니다.
[`HasherIgnoreTags`](/pkg/go/types#HasherIgnoreTags)는 [`IdenticalIgnoreTags`](/pkg/go/types#IdenticalIgnoreTags)에 해당하는 해셔입니다.

<!-- 6-stdlib/99-minor/go/types/76472.md -->
<!-- CL 736441 -->

`gotypesalias`의 `GODEBUG` 설정 (Go 1.22에 추가됨: [https://go.dev/doc/godebug#go-122]) 은 영구적으로 제거되었으며, 패키지 [`go/types`](https://pkg.go.dev/go/types)는 이제 `GODEBUG` 설정과 관계없이 항상 [`Alias`](https://pkg.go.dev/go/types#Alias) 유형 노드를 생성합니다. `alias declarations`에 대한 설명: [https://go.dev/ref/spec#Alias_declarations]

<!-- 6-stdlib/99-minor/go/types/79287.md -->
<!-- 여기에 특별한 내용은 없지만, String 메서드만 있습니다 -->

#### [`hash/maphash`](/pkg/hash/maphash/)

<!-- 6-stdlib/99-minor/hash/maphash/70471.md -->

[`Hasher`](/pkg/hash/maphash#Hasher) 인터페이스 유형은 특정 유형의 값과, 해시 기반 데이터 구조 (예: 해시 테이블 및 블룸 필터) 간의 계약을 정의합니다; 자세한 내용은 [#70471](/issue/70471)를 참조하십시오.

[`ComparableHasher`](/pkg/hash/maphash#ComparableHasher) 타입은 `==` 연산자가 정의된 비교 가능한 타입에 대해 편리한 [`Hasher`](/pkg/hash/maphash#Hasher) 구현을 제공합니다.

#### [`math/big`](/pkg/math/big/)

<!-- 6-stdlib/99-minor/math/big/76821.md -->
<!-- go.dev/issue/76821 -->

[`Int`](/pkg/math/big#Int)에 이제 `Divide` 메서드가 추가되어 두 개의 `Int` 값의 몫과 나머지를 계산할 수 있습니다.
다음과 같은 반올림 모드를 지원합니다: `Trunc` (/pkg/math/big#Trunc), `Floor` (/pkg/math/big#Floor), `Round` (/pkg/math/big#Round), `Ceil` (/pkg/math/big#Ceil).

#### [`math/rand/v2`](/pkg/math/rand/v2/) {#rand}

<!-- 6-stdlib/99-minor/math/rand/v2/77853.md -->

[`Rand`](/pkg/math/rand/v2#Rand)는 이제 일반적인 방법을 지원합니다.
[`N`](/pkg/math/rand/v2#Rand.N),
이는 상위 레벨의 [`N`](/pkg/math/rand/v2#N) 함수와 동일한 동작을 합니다.

#### [`net`](/pkg/net/)

<!-- 6-stdlib/99-minor/net/78137.md -->

[`UnixConn`](/pkg/net#UnixConn)의 읽기 메서드는 이제 내부 읽기가 EOF를 반환할 때 `net.OpError`](/pkg/net#OpError)로 감싸지 않고 직접 [`io.EOF`](/pkg/io#EOF)를 반환합니다.

#### [`net/http`](/pkg/net/http/)

<!-- 6-stdlib/99-minor/net/http/21753.md -->

[`Transport`](/pkg/net/http#Transport) 및 [`Server`](/pkg/net/http#Server)는 사용자 제공 [`net.Conn`](/pkg/net#Conn) 연결에서 TLS ALPN 프로토콜 협상을 지원하며, 이 연결은 `ConnectionState() tls.ConnectionState` 메서드를 구현해야 합니다.

<!-- 6-stdlib/99-minor/net/http/75500.md -->

HTTP/2 서버는 이제 RFC 9218에 정의된 클라이언트 우선 순위 신호를 수락하며, 이를 통해 더 높은 우선 순위를 가진 HTTP/2 스트림을 우선적으로 제공할 수 있습니다. 만약 이전 동작 방식, 즉 우선 순위 무관으로 스트림을 순환 방식으로 제공하는 것을 선호한다면, [`Server.DisableClientPriority`](/pkg/net/http#Server.DisableClientPriority)를 `true`로 설정할 수 있습니다.

<!-- 6-stdlib/99-minor/net/http/77370.md -->

HTTP/1 [`Response.Body`](/pkg/net/http#Response.Body)가 닫힐 때, 연결 재사용을 위해 합리적인 제한 내에서 읽지 않은 모든 콘텐츠를 자동으로 비웁니다. 대부분의 프로그램에서는 이 변경 사항이 아무런 영향을 미치지 않거나 성능 향상을 가져올 것입니다.
드물게, 연결 재사용의 이점을 받지 못하는 프로그램은 과도한 수의 비활성 연결을 유지하도록 잘못 설정된 경우 성능 저하를 경험할 수 있습니다. 일반적으로 `Transport.MaxIdleConns`를 `0`으로 설정하거나, 각 요청에 대해 다른 [`Client`](/pkg/net/http#Client)를 사용하여 `Transport.MaxIdleConns` 제한을 우회하는 방식으로 작동합니다.
이러한 경우, `Transport.DisableKeepAlives`를 `true`로 설정하면 연결 재사용을 비활성화합니다.
그러나 이러한 성능 저하는 일반적으로 `Transport` 또는 `Client`의 잘못된 구성 또는 사용을 나타내며, 더 자세한 분석이 필요할 수 있습니다.

<!-- go.dev/issue/79936 -->

새로운 [`Server.MaxHeaderValueCount`](/pkg/net/http#Server.MaxHeaderValueCount)
필드는 HTTP 서버가 수락할 용의가 있는 헤더 값의 개수를 제어할 수 있도록 합니다. 설정되지 않은 경우,
[`DefaultMaxHeaderValueCount`](/pkg/net/http#DefaultMaxHeaderValueCount)가 사용됩니다.

#### [`net/http/httptest`](/pkg/net/http/httptest/)

<!-- 6-stdlib/99-minor/net/http/httptest/76608.md -->

새로운 `[`NewTestServer`](/pkg/net/http/httptest#NewTestServer) 함수는
[`Server`](/pkg/net/http/httptest#Server)를 생성하며, 이 서버는 [`testing/synctest`](/pkg/testing/synctest) 패키지와 함께 사용할 수 있는 메모리 기반의 가짜 네트워크를 사용하여 구성됩니다.

```go
#### [`net/url`](/pkg/net/url/)
```

<!-- 6-stdlib/99-minor/net/url/73450.md -->

새로운 [`URL.Clone`](/pkg/net/url#URL.Clone) 메서드는 URL의 깊은 복사본을 생성합니다.
새로운 [`Values.Clone`](/pkg/net/url#Values.Clone) 메서드는 Values의 깊은 복사본을 생성합니다.

#### [`runtime/secret`](/pkg/runtime/secret/)

Goroutine이 [비밀 모드](/pkg/runtime/secret#Do)에서 생성되면, 이제 해당 Goroutine도 비밀 모드로 실행됩니다.

#### [`strings`](/pkg/strings/)

<!-- 6-stdlib/99-minor/strings/71151.md -->

새로운 `CutLast` 함수는 문자열을 분리자를 마지막으로 나타내는 위치에서 자릅니다.
이는 `LastIndex` 함수의 일부 일반적인 사용 사례를 대체하고 단순화할 수 있습니다.

#### [`syscall`](/pkg/syscall/)

<!-- CL 750680 -->

On Plan 9, `[Errno](pkg/syscall#Errno)` 유형이 정의되었으며, 다른 플랫폼과 같이 `error` 인터페이스를 구현합니다. Plan 9 시스템 호출은 `ErrorString` 값을 반환하므로, 이 패키지는 Plan 9에서 `Errno`를 반환하지 않습니다. 이는 `syscall.Errno`를 참조하는 이식 가능한 코드가 Plan 9에서 빌드 제약 없이 작동하도록 정의되었습니다.

#### [`testing/synctest`](/pkg/testing/synctest/)

<!-- 6-stdlib/99-minor/testing/synctest/77169.md -->

새로운 [`Sleep`](/pkg/testing/synctest#Sleep) 헬퍼 함수는 [`time.Sleep`](/pkg/time#Sleep) 및 [`synctest.Wait`](/pkg/testing/synctest#Wait)를 결합합니다.

#### [`unicode`](/pkg/unicode/)

<!-- 6-stdlib/99-minor/unicode/77266.md -->

유니코드 패키지와 시스템 전체에 걸쳐 유니코드 15에서 유니코드 17으로 업그레이드되었습니다.
[Unicode 16.0.0](https://www.unicode.org/versions/Unicode16.0.0/) 및
[Unicode 17.0.0](https://www.unicode.org/versions/Unicode17.0.0/)
릴리스 노트에서 변경 사항에 대한 정보를 참조하십시오.

## 포트

### Darwin
```
# Darwin
```

<!-- go.dev/issue/75836 -->

正如 Go 1.26 릴리스 노트에 [공지](go1.26#darwin)된 바와 같이,
Go 1.27은 macOS 13 Ventura 또는 그 이후 버전을 요구합니다;
이전 버전 지원은 중단되었습니다.

### PowerPC {#ppc64}

<!-- go.dev/issue/76244 -->

리눅스 (`GOOS=linux` `GOARCH=ppc64`)의 64비트 Big-Endian PowerPC 포트에서,
Go 툴체인은 이제 ELFv2 시스템 ABI를 사용하는 바이너리를 생성합니다.
ELFv2 지원은 리눅스 커널 3.13 또는 그 이상을 필요로 합니다.
RHEL7은 이 기능을 3.10 커널로 백포트했습니다.

Cgo, 위치 독립 실행 파일 (PIE), 및 외부 링크가 이제 지원됩니다.
이 기능을 사용하려면 ELFv2와 호환되는 런타임 환경 (libc 및 모든 링크되고 로드된 라이브러리)이 필요합니다.

프로그램이 cgo를 사용하지 않는 경우, Go 도구 체인은 기본적으로 내부 링크를 사용하여 정적 실행 파일을 생성합니다.
cgo 옵션을 사용하는 프로그램의 경우, 정적, 순수 Go 실행 파일이 필요한 경우, `go build`를 실행할 때 환경 변수 `CGO_ENABLED=0`을 설정할 수 있습니다.
