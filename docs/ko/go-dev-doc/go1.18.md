<!--
참고: 이 문서 및 이 디렉토리에 있는 다른 문서에서, 고정 폭의 표현과 고정 폭이 아닌 공백을 혼용하는 규칙을 사용합니다. 예를 들어 `hello` `world`와 같습니다.
이러한 표현에서 내부 태그를 제거하는 CL을 보내지 마세요.
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.18 소개 {#introduction}

가장 최신 Go 버전인 1.18은 언어,
툴 체인, 런타임 및 라이브러리에 대한 변경 사항을 포함하는
중요한 릴리스입니다.
Go 1.18은 Go 1.17 ([/doc/go1.17](https://example.com/doc/go1.17)) 이후 7개월 후에 출시됩니다.
항상처럼, 이 릴리스는 Go 1의 [호환성 약속](/doc/go1compat)을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상됩니다.

## 언어 변경 사항 {#language}

```
// Go code example
package main
```

### 제네릭스

<!-- https://golang.org/issue/43651, https://golang.org/issue/45346 -->
Go 1.18은 [Type
Parameters Proposal](https://go.googlesource.com/proposal/+/refs/heads/master/design/43651-type-parameters.md)에 설명된 제네릭 기능을 구현합니다.
이는 주요 - 하지만 완전히 이전 버전과 호환되는 - 언어 변경 사항을 포함합니다.

이 새로운 언어 변경 사항은 상당량의 새로운 코드를 필요로 했으며, 이러한 코드는 실제 환경에서 상당한 테스트를 거치지 않았습니다. 이는 더 많은 사람들이 일반적인 코드를 작성하고 사용할 때 발생할 것입니다. 저희는 이 기능이 잘 구현되었고 고품질이라고 믿습니다. 그러나, Go의 대부분의 측면과는 달리, 실제 경험을 통해 이를 뒷받침할 수 없습니다. 따라서, 일반적인 코드를 사용하는 것이 합리적이라고 생각될 때 사용을 권장하지만, 실제 환경에 일반적인 코드를 배포할 때는 적절한 주의를 기울여야 합니다.

물론, 저희는 새로운 언어 기능이 잘 설계되었고 명확하게 정의되어 있다고 믿지만, 실수를 했을 가능성도 있습니다.
다음 사항을 강조하고자 합니다. "[Go 1 호환성 보장](/doc/go1compat)"에는 "제공 사양에 존재하는 불일치 또는 불완전성을 해결해야 하는 경우, 해당 문제를 해결하면 기존 프로그램의 의미 또는 법적 효력을 변경할 수 있습니다. 저희는 이러한 문제에 대한 해결책을 포함하여 구현을 업데이트할 권한을 보유합니다."라고 명시되어 있습니다. 또한 "컴파일러 또는 라이브러리에 사양을 위반하는 버그가 있는 경우, 해당 버그를 수정하면 의존하는 프로그램이 오류로 인해 중단될 수 있습니다. 저희는 이러한 버그를 수정할 권한을 보유합니다."라고 명시되어 있습니다. 즉, 1.18 릴리스와 호환되도록 작동하는 제네릭을 사용하는 코드가 있지만, 이후 릴리스에서는 작동하지 않을 가능성이 있습니다. 저희는 그러한 변경을 계획하거나 예상하지 않습니다. 그러나, 저희가 오늘날 예측할 수 없는 이유로 인해, 1.18 프로그램을 이후 릴리스에서 중단해야 할 수 있습니다. 저희는 가능한 한 이러한 중단을 최소화할 것입니다. 그러나, 중단이 없을 것이라는 보장은 할 수 없습니다.

다음은 가장 눈에 띄는 변경 사항 목록입니다. 보다 포괄적인 개요는 [제안](https://go.googlesource.com/proposal/+/refs/heads/master/design/43651-type-parameters.md)을 참조하십시오. 자세한 내용은 [언어 사양](/ref/spec)을 참조하십시오.

- `[함수](/ref/spec#Function_declarations)` 및
    `[타입 선언](/ref/spec#Type_declarations)`의 구문은 이제
    `[타입 매개변수](/ref/spec#Type_parameter_declarations)`를 허용합니다.
  - 매개변수를 갖는 함수 및 타입은 괄호 안에 타입 인수를 나열하여 생성할 수 있습니다.
  - 새로운 토큰 `~`이 `[운영자와 구두점](/ref/spec#Operators_and_punctuation)` 집합에 추가되었습니다.
  - `[인터페이스 타입](/ref/spec#Interface_types)`의 구문은 이제 인터페이스의 이름뿐만 아니라 임의의 타입 및 유니언, `~T` 타입 요소를 포함하도록 허용합니다. 이러한 인터페이스는 타입 제약 조건으로만 사용될 수 있습니다.
    인터페이스는 이제 타입 집합뿐만 아니라 메서드 집합도 정의합니다.
  - 새로운
    `[사전 정의된 식별자](/ref/spec#Predeclared_identifiers)`
    `any`는 빈 인터페이스의 별칭입니다. `interface{}` 대신 사용할 수 있습니다.
  - 새로운
    `[사전 정의된 식별자](/ref/spec#Predeclared_identifiers)`
    `comparable`은 `==` 또는 `!=`를 사용하여 비교할 수 있는 모든 타입의 집합을 나타내는 인터페이스입니다. 이 인터페이스는 (또는 포함) 타입 제약 조건으로만 사용될 수 있습니다.

다음 세 가지 실험적인 패키지는 제네릭을 사용하는 것이 유용할 수 있습니다.
이 패키지는 x/exp 저장소에 있습니다. 이들의 API는 Go 1의 보증 대상이 아니며, 제네릭에 대한 경험이 쌓이면서 변경될 수 있습니다.

#### [`golang.org/x/exp/constraints`](https://pkg.go.dev/golang.org/x/exp/constraints)

유용한 일반 코드에 사용되는 제약 조건, 예를 들어
[`constraints.Ordered`](https://pkg.go.dev/golang.org/x/exp/constraints#Ordered).

#### [`golang.org/x/exp/slices`](https://pkg.go.dev/golang.org/x/exp/slices)

원하는 요소 유형의 슬라이스에 작동하는 일반적인 함수들의 모음.

#### [`golang.org/x/exp/maps`](https://pkg.go.dev/golang.org/x/exp/maps)

모든 키 또는 요소 유형의 맵에 작동하는 일반적인 함수들의 모음.

현재 제네릭 구현에는 다음과 같은 알려진 제한 사항이 있습니다:

- <!-- https://golang.org/issue/47631 -->
    Go 컴파일러는 제네릭 함수 또는 메서드 내에서 타입 선언을 처리할 수 없습니다.
    향후 릴리스에서 이 기능을 지원할 계획입니다.
  - <!-- https://golang.org/issue/50937 -->
    Go 컴파일러는 미리 선언된 함수 `real`, `imag`, `complex`에 대해 타입 매개변수 유형의 인수를 허용하지 않습니다.
    향후 릴리스에서 이 제한을 제거할 계획입니다.
  - <!-- https://golang.org/issue/51183 -->
    Go 컴파일러는 제네릭 타입 `P`의 제약 인터페이스에 명시적으로 선언된 경우에만 타입 매개변수 타입 `P`의 값 `x`에 메서드 `m`을 호출할 수 있습니다.
    동일하게, 메서드 값 `x.m` 및 메서드 표현식 `P.m`도 `m`이 `P`에 의해 명시적으로 선언된 경우에만 지원됩니다. `m`이 `P`의 메서드 세트에 속하는 이유와 관계없이, `m`이 `P`의 모든 타입에 의해 구현되더라도 그렇습니다. 향후 릴리스에서 이 제한을 제거할 계획입니다.
  - <!-- https://golang.org/issue/51576 -->
    Go 컴파일러는 제네릭 타입의 타입 세트에 필드 `f`가 있는 경우에도 구조체 필드 `x.f`에 액세스하는 것을 지원하지 않습니다.
    향후 릴리스에서 이 제한을 제거할 수 있습니다.
  - <!-- https://golang.org/issue/49030 -->
    구조체 타입 내에 이름 없는 필드로 제네릭 타입 또는 제네릭 타입의 포인터를 포함하는 것은 허용되지 않습니다. 마찬가지로, 인터페이스 타입 내에 제네릭 타입을 포함하는 것은 허용되지 않습니다.
    이러한 기능이 향후에 허용될지는 현재 불분명합니다.
  - 단, 여러 항을 가진 유니언 요소는 비어 있지 않은 메서드 세트가 있는 인터페이스 타입을 포함할 수 없습니다.
    이러한 기능이 향후에 허용될지는 현재 불분명합니다.

제네릭 또한 Go 생태계에 큰 변화를 가져옵니다. 당사에서 핵심 도구에 제네릭 지원을 추가했지만, 아직 더 많은 작업이 필요합니다. 나머지 도구, 문서, 라이브러리가 이러한 언어 변경 사항을 따라잡는 데는 시간이 걸릴 것입니다.

### 버그 수정 {#bug_fixes}

Go 1.18 컴파일러는 이제 함수 리터럴 내에서 설정되지만 사용되지 않는 변수에 대해 "선언되었지만 사용되지 않음" 오류를 올바르게 보고합니다. Go 1.18 이전에는 컴파일러가 이러한 경우 오류를 보고하지 않았습니다. 이는 오랫동안 해결되지 않았던 컴파일러 문제를 해결합니다 [#8560](/issue/8560). 이 변경으로 인해 (아마도 잘못된) 프로그램이 더 이상 컴파일되지 않을 수 있습니다. 필요한 해결 방법은 간단합니다: 프로그램이 실제로 잘못된 경우 수정하거나, 문제를 일으키는 변수를 사용합니다. 예를 들어, 빈 식별자 `_`에 할당합니다. `go vet`이 항상 이 오류를 지적했기 때문에 영향을 받는 프로그램의 수는 매우 적을 것으로 예상됩니다.

Go 1.18 컴파일러는 이제 `print` 및 `println`과 같은 선언된 함수에 `rune` 상수 표현식 (예: `'1' << 32`)을 인수로 전달할 때 오버플로우를 보고합니다. 이는 사용자 정의 함수와 일치하는 동작입니다. Go 1.18 이전에는 컴파일러가 이러한 경우에 오류를 보고하지 않고, 해당 상수 인수가 `int64`에 맞으면 자동으로 허용했습니다. 이 변경으로 인해 (잠재적으로 잘못된) 프로그램이 더 이상 컴파일되지 않을 수 있습니다. 필요한 수정은 간단합니다: 실제로 잘못된 경우 프로그램을 수정하거나, 문제의 인수를 올바른 유형으로 명시적으로 변환합니다. `go vet`이 항상 이 오류를 지적했기 때문에, 영향을 받는 프로그램 수는 매우 적을 것으로 예상됩니다.

## 포트

### AMD64 {#amd64}

<!-- CL 349595 -->
Go 1.18에서 새로운 환경 변수 `GOAMD64`를 도입했습니다. 이 변수는 컴파일 시간에 AMD64 아키텍처의 최소 타겟 버전을 선택합니다. 허용되는 값은 `v1`, `v2`, `v3` 또는 `v4`입니다. 각 더 높은 레벨은 추가적인 프로세서 기능을 필요로 하며, 이를 활용합니다. 자세한 설명은
[여기](/wiki/MinimumRequirements#amd64)에서 확인할 수 있습니다.

`GOAMD64` 환경 변수는 기본적으로 `v1`로 설정됩니다.

### RISC-V {#riscv}

<!-- golang.org/issue/47100, CL 334872 -->
리눅스에서 64비트 RISC-V 아키텍처 (`linux/riscv64` 포트)는 이제 `c-archive` 및 `c-shared` 빌드 모드를 지원합니다.

### 리눅스 {#linux}

<!-- golang.org/issue/45964 -->
Go 1.18은 Linux 커널 버전 2.6.32 이상을 요구합니다.

### Windows
```
{#windows}
```

<!-- https://golang.org/issue/49759 -->
`windows/arm` 및 `windows/arm64` 포트가 이제 비협조적인 우선순위 처리를 지원하며, 이를 모든 Windows 포트에 적용합니다. 이를 통해 Win32 함수를 호출할 때 발생하는, 특히 널리 대기하는 경우에 발생하는 미묘한 버그를 해결할 수 있을 것으로 예상됩니다.

### iOS {#ios}

<!-- golang.org/issue/48076, golang.org/issue/49616 -->
iOS (`ios/arm64` 포트)
및 AMD64 기반 macOS ( `ios/amd64` 포트)에서 실행되는 iOS 시뮬레이터에서,
Go 1.18은 이제 iOS 12 또는 그 이상 버전을 필요로 합니다; 이전 버전 지원은 중단되었습니다.

### FreeBSD {#freebsd}

Go 1.18은 FreeBSD 11.x에서 지원되는 마지막 버전이며, 이미 지원이 종료되었습니다. Go 1.19는 FreeBSD 12.2+ 또는 FreeBSD 13.0+를 필요로 합니다.

FreeBSD 13.0+는 COMPAT\_FREEBSD12 옵션이 설정된 커널을 필요로 합니다 (이는 기본 설정입니다).

## 도구 {#tools}

### 퍼징 {#fuzzing}

Go 1.18은 [퍼징 제안](/issue/44551)에 설명된 대로 퍼징 구현을 포함합니다.

자세한 내용은 [퍼징 시작 페이지](/security/fuzz)를 참조하세요.

다음 사항을 유의하십시오: 퍼징은 많은 메모리를 소비하고 실행 중에 시스템 성능에 영향을 미칠 수 있습니다. 또한 퍼징 엔진은 `$GOCACHE/fuzz` 내의 퍼징 캐시 디렉터리에 테스트 커버리지를 확장하는 값을 기록합니다. 현재 퍼징 캐시에 작성할 수 있는 파일 수 또는 총 바이트 수에 제한이 없으므로, 이는 상당한 양의 저장 공간(예: 수 GB)을 차지할 수 있습니다.

### Go 명령어 {#go-command}

```go
get
```
#### `go` `get` {#go-get}

<!-- golang.org/issue/43684 -->
`go get`는 더 이상 모듈에 대한 방식으로 패키지를 빌드하거나 설치하지 않습니다. `go get`는 이제 `go.mod`에서 종속성을 조정하는 데 전념합니다. 실질적으로 `-d` 플래그는 항상 활성화됩니다. 현재 모듈의 컨텍스트 외부에서 최신 버전을 설치하려면 다음을 사용합니다:
[`go install example.com/cmd@latest`](/ref/mod#go-install). 버전 쿼리[version queries](/ref/mod#version-queries)를 `latest` 대신 사용할 수 있습니다. `go install`의 이러한 형태는 Go 1.16에 추가되었으므로, 이전 버전을 지원하는 프로젝트는 `go install` 및 `go get` 모두에 설치 지침을 제공해야 할 수 있습니다. `go get`는 이제 모듈 외부에서 사용될 때 오류를 보고합니다. 왜냐하면 업데이트할 `go.mod` 파일이 없기 때문입니다. GOPATH 모드( `GO111MODULE=off` 와 함께)에서는 `go get`는 여전히 패키지를 빌드하고 설치합니다.

#### 자동 `go.mod` 및 `go.sum` 업데이트 {#go-mod-업데이트}

<!-- https://go.dev/issue/45551 -->
`go` `mod` 그래프,
`go` `mod` 벤더,
`go` `mod` 검증 및
`go` `mod` 왜
명령어는 더 이상 `go.mod` 및
`go.sum` 파일을 자동으로 업데이트하지 않습니다.
(이 파일은 `go get`,
`go mod tidy` 또는
`go mod download`를 사용하여 명시적으로 업데이트할 수 있습니다.)

#### `go` 버전 {#go-version}

<!-- golang.org/issue/37475 -->
`go` 명령은 이제 실행 파일에 버전 관리 정보를 포함합니다. 현재 체크아웃된 버전, 커밋 시간, 그리고 편집되거나 추적되지 않는 파일이 존재하는지 여부를 나타내는 플래그를 포함합니다. 버전 관리 정보는 `go` 명령이 Git, Mercurial, Fossil 또는 Bazaar 저장소 내의 디렉토리에서 실행될 때, 그리고 `main` 패키지와 해당 메인 모듈이 동일한 저장소에 있는 경우에 포함됩니다. 이 정보는 `-buildvcs=false` 플래그를 사용하여 생략할 수 있습니다.

<!-- golang.org/issue/37475 -->
또한, `go` 명령어는 빌드에 대한 정보를 포함합니다. 여기에는 빌드 및 도구 태그(`-tags`로 설정), 컴파일러, 어셈블러 및 링커 플래그(예: `-gcflags`), CGO가 활성화되었는지 여부, 그리고 활성화된 경우 CGO 환경 변수 값(예: `CGO_CFLAGS`) 등이 포함됩니다.

VCS 및 빌드 정보는 `go` `version` `-m` `file` 또는
`runtime/debug.ReadBuildInfo`(현재 실행 중인 바이너리에 대해) 또는 새로운 [`debug/buildinfo`](#debug/buildinfo) 패키지를 사용하여 모듈 정보와 함께 읽을 수 있습니다.

<!-- CL 369977 -->
내장된 빌드 정보의 기본 데이터 형식이 새로운 Go 릴리스와 함께 변경될 수 있으므로, 이전 버전의 `go`는 더 새로운 버전의 `go`로 생성된 빌드 정보를 처리하지 못할 수 있습니다.

`go` 1.18로 빌드된 바이너리에서 버전 정보를 읽으려면 `go` 명령의 `version`과 `go` 1.18+의 `debug/buildinfo` 패키지를 사용하십시오.

#### `go` 모듈 다운로드 {#go-mod-download}

<!-- https://golang.org/issue/44435 -->
만약 메인 모듈의 `go.mod` 파일이 [`go` `1.17`](/ref/mod#go-mod-file-go)
또는 그 이상의 버전을 지정하는 경우, `go` `mod` `download` 명령은
인수가 없는 경우, 메인 모듈의 `go.mod` 파일에 명시적으로 [필요한](/ref/mod#go-mod-file-require) 모듈의
소스 코드를만 다운로드합니다. ( `go` `1.17` 또는 그 이상의 버전을 사용하는 모듈에서는, 이미 메인 모듈의 패키지와 테스트를 빌드하는 데 필요한 모든 종속성이 포함되어 있습니다.)
전이적인 종속성의 소스 코드를 포함하여 다운로드하려면 `go` `mod` `download` `all` 명령을 사용하십시오.

#### `go` 모듈 및 벤더 {#go-mod-vendor}

<!-- https://golang.org/issue/47327 -->
`go mod vendor` 서브명령은 이제 `-o` 플래그를 지원하여 출력 디렉토리를 설정할 수 있습니다.
(다른 `go` 명령어는 `-mod=vendor`를 사용하여 패키지를 로드할 때 여전히 모듈의 루트 디렉터리에 있는 `vendor` 디렉터리를 읽습니다. 따라서 이 플래그의 주요 사용 사례는 패키지 소스 코드를 수집해야 하는 타사 도구에 해당합니다.)

#### `go` 모듈 정리 (`go mod tidy`) {#go-mod-tidy}

<!-- https://golang.org/issue/47738, CL 344572 -->
`go mod tidy` 명령이 이제 모듈의 소스 코드가 필요하여 각 가져온 패키지가 단 하나의 모듈에서 제공되는지 확인하는 데 사용되는 추가 체크섬을 `go.sum` 파일에 유지합니다. [빌드 목록](/ref/mod#glos-build-list)에 정의된 모듈에 따라 각 가져온 패키지가 단 하나의 모듈에서 제공되는지 확인하는 것은 드문 경우이며, 이 조건이 적용되지 않으면 빌드 오류가 발생합니다. 따라서 이 변경 사항은 주요 모듈의 `go.mod` 파일에 있는 `go` 버전과 관련이 없습니다.

#### `go` 작업 {#go-work}

<!-- https://golang.org/issue/45713 -->
`go` 명령은 이제 "Workspace" 모드를 지원합니다. 만약 `go.work` 파일이 현재 작업 디렉토리 또는 상위 디렉토리에 존재하거나, `GOWORK` 환경 변수를 사용하여 지정된 경우, `go` 명령은 Workspace 모드로 실행됩니다.
Workspace 모드에서는 `go.work` 파일을 사용하여 모듈 해소에 사용되는 루트 모듈 세트를 결정합니다. 일반적으로 사용되는 `go.mod` 파일을 사용하여 단일 루트 모듈을 지정하는 대신입니다. 자세한 내용은 [`go work`](/pkg/cmd/go#hdr-Workspace_maintenance) 문서를 참조하십시오.

#### `go build` `-asan`

<!-- CL 298612 -->
`go` `build` 명령어 및 관련 명령어에 이제 `-asan` 플래그가 추가되어 C (또는 C++) 코드를 어드레스 산타이저(C 컴파일러 옵션 `-fsanitize=address`)로 컴파일한 코드와 상호 작용할 수 있습니다.

#### `go test` {#go-test}

<!-- CL 251441 -->
`go` 명령은 위에서 설명한 [퍼징 지원](#fuzzing)에 대한 추가적인 명령줄 옵션을 지원합니다:

- `go test`는 다음 옵션을 지원합니다.
    `-fuzz`, `-fuzztime`, 및
    `-fuzzminimizetime` 옵션.
    이 옵션에 대한 설명은 다음에서 확인하십시오.
    [`go help testflag`](/pkg/cmd/go#hdr-Testing_flags).
  - `go clean`은 `-fuzzcache` 옵션을 지원합니다.
    설명은 다음에서 확인하십시오.
    [`go help clean`](/pkg/cmd/go#hdr-Remove_object_files_and_cached_files).

#### `//go:build` 라인 {#go-build-라인}

<!-- CL 240611 -->
Go 1.17에서는 더 읽기 쉬운 방식으로 빌드 제약 조건을 작성하기 위해 `//go:build` 줄을 도입했습니다.
`//` `+build` 줄 대신에 사용됩니다.
Go 1.17부터, `gofmt`는 기존 `+build` 줄과 일치하도록 `//go:build` 줄을 추가하고, 이들을 동기화합니다.
또한, `go vet`은 이들이 동기화되지 않았을 때 경고를 표시합니다.

Go 1.18의 출시로 인해 Go 1.16에 대한 지원이 종료되었으므로,
지원되는 모든 Go 버전에서 `//go:build` 줄을 이해합니다.
Go 1.18에서는 `go` `fix`가 이제는 더 이상 사용되지 않는
`//` `+build` 줄을 `go.mod` 파일에 Go 1.18 이상을 선언하는 모듈에서 제거합니다.

자세한 내용은 [go.dev/design/draft-gobuild](/design/draft-gobuild)를 참조하십시오.

### Gofmt {#gofmt}

<!-- https://golang.org/issue/43566 -->
`gofmt`은 이제 입력을 동시에 읽고 포맷하며, `GOMAXPROCS`에 비례하는 메모리 제한을 갖습니다. 여러 CPU를 가진 머신에서는 `gofmt`가 훨씬 빠르게 실행될 것입니다.

### 수의사 {#vet}

#### 제네릭 관련 업데이트 {#vet-generics}

<!-- https://golang.org/issue/48704 -->
`vet` 도구가 제네릭 코드를 지원하도록 업데이트되었습니다. 대부분의 경우,
제네릭 코드에서 비제네릭 코드에 타입 매개변수를 해당 타입으로 대체한 후,
[타입 세트](/ref/spec#Interface_types)에 정의된 타입을 사용하여 오류를 보고했을 때와 동일한 오류를 제네릭 코드에서 보고합니다.
예를 들어, `vet`은 다음과 같은 형식 오류를 보고합니다:

```markdown
```go
func Print[T ~int|~string](t T) {
		fmt.Printf("%d", t)
	}
```

이는 `Print[string]`의 비 일반화된 동등물에서 형식 오류를 보고하는 데 사용되기 때문입니다:

```markdown
```go
func PrintString(x string) {
		fmt.Printf("%d", x)
	}
```

#### 기존 검사기의 정밀도 개선 {#vet-precision}

<!-- CL 323589 356830 319689 355730 351553 338529 -->
`cmd/vet`의 `copylock`, `printf`,
`sortslice`, `testinggoroutine`, 및 `tests` 검사기는 추가적인 코드 패턴을 처리하기 위해 상당한 정밀도 개선이 이루어졌습니다.
이는 기존 패키지에 새롭게 보고되는 오류를 유발할 수 있습니다. 예를 들어,
`printf` 검사기는 문자 상수를 연결하여 생성된 포맷팅 문자열을 추적합니다. 따라서 `vet`은 다음과 같은 오류를 보고합니다:

// fmt.Printf 서식 지정자 %d이 Println에 전달됨.
	  fmt.Println("%d" + ` ≡ x (mod 2)` + "\n", x%2)

## 실행 시간 {#runtime}

<!-- https://golang.org/issue/44167 -->
가비지 컬렉터는 이제 실행 빈도를 결정할 때, 스택 스캔과 같은 힙 이외의 가비지 컬렉터 작업 소스를 포함합니다. 결과적으로, 이러한 소스가 중요한 경우 가비지 컬렉터 오버헤드가 더 예측 가능해집니다. 대부분의 애플리케이션에서는 이러한 변경 사항이 미미할 것입니다. 그러나 일부 Go 애플리케이션은 이전보다 덜 메모리를 사용하고 가비지 컬렉션에 더 많은 시간을 소비하거나, 그 반대로 이전보다 더 많은 메모리를 사용하고 가비지 컬렉션에 더 적은 시간을 소비할 수 있습니다. 의도된 해결책은 필요한 경우 `GOGC`를 조정하는 것입니다.

<!-- CL 358675, CL 353975, CL 353974 -->
실행 시간은 이제 운영 체제에 메모리를 더 효율적으로 반환하도록 최적화되었으며, 그 결과 더 적극적으로 작동하도록 조정되었습니다.

<!-- CL 352057, https://golang.org/issue/45728 -->
Go 1.17은 일반적으로 스택 트레이스에서 인수의 형식을 개선했지만, 레지스터에 전달된 인수의 부정확한 값을 출력할 수 있었습니다.
이 문제는 Go 1.18에서 각 부정확할 수 있는 값 뒤에 물음표 (`?`)를 출력하여 개선되었습니다.

<!-- CL 347917 -->
내장 함수 `append`가 새로운 배열을 할당해야 할 때, 슬라이스를 얼마나 확장할지 결정하는 데 약간 다른 공식을 사용합니다.
새로운 공식은 할당 동작에서 갑작스러운 변화를 덜 받습니다.

## 컴파일러

<!-- https://golang.org/issue/40724 -->
Go 1.17은 선택된 운영 체제에서 64비트 x86 아키텍처에서 함수 인자와 결과를 스택 대신 레지스터를 사용하여 전달하는 새로운 방법을 구현했습니다.
Go 1.18은 64비트 ARM (`GOARCH=arm64`), 큰 엔디안 및 작은 엔디안 64비트 파워PC (`GOARCH=ppc64`, `ppc64le`), 그리고 모든 운영 체제에서 64비트 x86 아키텍처 (`GOARCH=amd64`)를 지원하는 플랫폼을 확장합니다.
64비트 ARM 및 64비트 파워PC 시스템에서, 성능 테스트 결과 평균 10% 이상의 성능 향상을 보입니다.

正如 [Go 1.17 릴리스 노트](go1.17#compiler)에서 언급된 것처럼,
이 변경 사항은 안전한 Go 코드의 기능을 변경하지 않으며,
대부분의 어셈블리 코드에 영향을 미치지 않도록 설계되었습니다. 자세한 내용은 [Go 1.17 릴리스 노트](go1.17#compiler)를 참조하십시오.

<!-- CL 355497, CL 356869 -->
컴파일러는 이제 범위 루프 또는 레이블이 지정된 `for` 루프를 포함하는 함수를 인라인할 수 있습니다.

<!-- CL 298611 -->
새로운 `-asan` 컴파일러 옵션은
새로운 `go` 명령 `-asan` 옵션을 지원합니다.

<!-- https://golang.org/issue/50954 -->
컴파일러의 타입 검사기가 완전히 대체되어 제네릭을 지원하게 되면서, 일부 오류 메시지는 이전과 다른 표현을 사용할 수 있습니다. 일부 경우에는 Go 1.18 이전의 오류 메시지가 더 자세하거나 더 유용한 방식으로 작성되었습니다.
우리는 Go 1.19에서 이러한 경우를 해결할 계획입니다.

<!-- /issue/49569 -->
컴파일러의 제네릭 지원 관련 변경 사항으로 인해, Go 1.18의 컴파일 속도는 Go 1.17보다 대략 15% 느릴 수 있습니다.
컴파일된 코드의 실행 시간은 영향을 받지 않습니다. 향후 릴리스에서 컴파일러의 속도를 개선할 계획입니다.

## 링커 {#linker}

링크러는 [훨씬 적은 위치 지정(relocation)을 생성](https://tailscale.com/blog/go-linker/).
그 결과, 대부분의 코드베이스는 더 빠르게 링크되고, 링크에 필요한 메모리가 줄어들며, 더 작은 바이너리를 생성합니다.
Go 바이너리를 처리하는 도구는 Go 1.18의 `debug/gosym` 패키지를 사용하여 기존 및 새로운 바이너리를 모두 원활하게 처리해야 합니다.

<!-- CL 298610 -->
새로운 `-asan` 링커 옵션은
새로운 `go` 명령의 `-asan` 옵션을 지원합니다.

## 부트스트랩 {#bootstrap}

<!-- CL 369914, CL 370274 -->
소스에서 Go 배포를 빌드할 때 `GOROOT_BOOTSTRAP`이 설정되지 않은 경우, 이전 버전의 Go는 `$HOME/go1.4` 디렉터리 (`%HOMEDRIVE%%HOMEPATH%\go1.4` on Windows)에서 Go 1.4 또는 그 이후의 런타임 도구 체인을 찾았습니다.
현재 Go는 `$HOME/go1.17` 또는 `$HOME/sdk/go1.17`을 먼저 찾은 후 `$HOME/go1.4`로 되돌아갑니다.
Go 1.19는 런타임 도구를 위해 Go 1.17 또는 그 이후 버전을 필요로 하며, 이 변경 사항으로 인해 전환이 더 원활해질 것으로 예상됩니다.
자세한 내용은 [go.dev/issue/44505](/issue/44505)를 참조하십시오.

## 표준 라이브러리 {#library}

### 새로운 `debug/buildinfo` 패키지 {#debug_buildinfo}

<!-- golang.org/issue/39301 -->
새로운 [`debug/buildinfo`](/pkg/debug/buildinfo) 패키지는 `go` 명령어로 빌드된 실행 파일에 내장된 모듈 버전, 버전 관리 정보 및 빌드 플래그에 액세스할 수 있도록 합니다.
동일한 정보는 현재 실행 중인 바이너리에 대해 `runtime/debug.ReadBuildInfo`](/pkg/runtime/debug#ReadBuildInfo)를 통해, 그리고 명령줄에서 `go version -m` 명령어를 통해 사용할 수도 있습니다.

### 새로운 `net/netip` 패키지 {#netip}

```go
package net

// NetIP는 IPv4 및 IPv6 주소를 나타내는 데 사용되는 인터페이스입니다.
type NetIP struct {
	// ...
}

// NewNetIP는 새로운 NetIP 인스턴스를 만듭니다.
func NewNetIP(ip string) (*NetIP, error)
```

```go
package net

// NetIP는 IPv4 및 IPv6 주소를 나타내는 데 사용되는 인터페이스입니다.
type NetIP struct {
	// ...
}

// NewNetIP는 새로운 NetIP 인스턴스를 만듭니다.
func NewNetIP(ip string) (*NetIP, error)
```

새로운 [`net/netip`](/pkg/net/netip/)
패키지는 새로운 IP 주소 유형인 [`Addr`](/pkg/net/netip/#Addr)을 정의합니다.
기존의
[`net.IP`](/pkg/net/#IP) 유형과 비교하여, `netip.Addr` 유형은 더 적은 메모리를 사용하며, 변경 불가능하고 비교 가능하므로 `==` 연산자를 사용할 수 있으며, 맵 키로도 사용할 수 있습니다.

`Addr` 외에도, 패키지는
[`AddrPort`](/pkg/net/netip/#AddrPort)를 정의합니다. 이 구조체는 IP 주소와 포트를 나타내며,
[`Prefix`](/pkg/net/netip/#Prefix)를 정의하여 네트워크 CIDR 프리픽스를 나타냅니다.

이 패키지는 또한 이러한 새 유형을 생성하고 검사하는 데 사용되는 여러 함수를 정의합니다:
[`AddrFrom4`](/pkg/net/netip#AddrFrom4),
[`AddrFrom16`](/pkg/net/netip#AddrFrom16),
[`AddrFromSlice`](/pkg/net/netip#AddrFromSlice),
[`AddrPortFrom`](/pkg/net/netip#AddrPortFrom),
[`IPv4Unspecified`](/pkg/net/netip#IPv4Unspecified),
[`IPv6LinkLocalAllNodes`](/pkg/net/netip#IPv6LinkLocalAllNodes),
[`IPv6Unspecified`](/pkg/net/netip#IPv6Unspecified),
[`MustParseAddr`](/pkg/net/netip#MustParseAddr),
[`MustParseAddrPort`](/pkg/net/netip#MustParseAddrPort),
[`MustParsePrefix`](/pkg/net/netip#MustParsePrefix),
[`ParseAddr`](/pkg/net/netip#ParseAddr),
[`ParseAddrPort`](/pkg/net/netip#ParseAddrPort),
[`ParsePrefix`](/pkg/net/netip#ParsePrefix),
[`PrefixFrom`](/pkg/net/netip#PrefixFrom).

[`net`](/pkg/net/) 패키지는 기존 메서드와 병렬로 작동하는 새로운 메서드를 포함하지만, `netip.AddrPort` 유형을 반환하며, 이는 더 무거운 [`net.IP`](/pkg/net/#IP) 또는 `*net.UDPAddr`](/pkg/net/#UDPAddr) 유형 대신 사용됩니다:
[`Resolver.LookupNetIP`](/pkg/net/#Resolver.LookupNetIP),
[`UDPConn.ReadFromUDPAddrPort`](/pkg/net/#UDPConn.ReadFromUDPAddrPort),
[`UDPConn.ReadMsgUDPAddrPort`](/pkg/net/#UDPConn.ReadMsgUDPAddrPort),
[`UDPConn.WriteToUDPAddrPort`](/pkg/net/#UDPConn.WriteToUDPAddrPort),
[`UDPConn.WriteMsgUDPAddrPort`](/pkg/net/#UDPConn.WriteMsgUDPAddrPort).
새로운 `UDPConn` 메서드는 할당이 없는 I/O를 지원합니다.

`net` 패키지는 기존의
[`TCPAddr`](/pkg/net/#TCPAddr) 및 [`UDPAddr`](/pkg/net/#UDPAddr) 유형과 `netip.AddrPort` 유형 간에 변환하는 데 사용할 수 있는 함수 및 메서드를 포함합니다.
다음 함수를 제공합니다.
[`TCPAddrFromAddrPort`](/pkg/net/#TCPAddrFromAddrPort),
[`UDPAddrFromAddrPort`](/pkg/net/#UDPAddrFromAddrPort),
[`TCPAddr.AddrPort`](/pkg/net/#TCPAddr.AddrPort),
[`UDPAddr.AddrPort`](/pkg/net/#UDPAddr.AddrPort).

### TLS 1.0 및 1.1 기본적으로 비활성화 (클라이언트 측) {#tls10}

<!-- CL 359779, golang.org/issue/45428 -->
만약 [`Config.MinVersion`](/pkg/crypto/tls/#Config.MinVersion)이 설정되지 않은 경우, 클라이언트 연결에 대해 기본적으로 TLS 1.2를 사용합니다. 안전하고 최신 버전의 서버는 TLS 1.2를 지원해야 하며, 브라우저는 2020년부터 이를 요구하고 있습니다. `Config.MinVersion`을 `VersionTLS10`으로 설정하면 TLS 1.0 및 1.1도 지원됩니다.
서버 측의 기본값은 변경되지 않고 TLS 1.0을 유지합니다.

기본 설정을 일시적으로 TLS 1.0으로 되돌리려면 다음 환경 변수를 설정합니다.
`GODEBUG=tls10default=1`
이 옵션은 Go 1.19에서 제거됩니다.

### SHA-1 인증서 거부 {#sha1}

```
openssl s_client -connect example.com:443 -CAfile root.pem
```

<!-- CL 359777, golang.org/issue/41682 -->
`crypto/x509`는 이제
SHA-1 해시 함수로 서명된 인증서를 거부합니다. 이는 자체 서명된 루트 인증서에는 적용되지 않습니다. SHA-1에 대한 실질적인 공격은 2017년부터 [증명되었으며](https://shattered.io/), 공신력 있는 인증 기관은 2015년 이후 SHA-1 인증서를 발급하지 않습니다.

이를 일시적으로 재설정하려면 다음 환경 변수를 설정합니다.
`GODEBUG=x509sha1=1`

이 옵션은 향후 버전에서 제거됩니다.

### 라이브러리의 미미한 변경 사항 {#minor_library_changes}

물론, 라이브러리에는 항상 다양한 작은 변경 사항과 업데이트가 있으며, 이는 Go 1의 [호환성]( /doc/go1compat)이라는 약속에 따라 이루어졌습니다.

#### [bufio](/pkg/bufio/)

<!-- CL 345569 -->
새로운 `Writer.AvailableBuffer` 메서드는 `append`와 유사한 API를 사용하기 위해, 용량은 비어있을 수도 있지만, 비어있는 버퍼를 반환합니다. 버퍼에 데이터를 추가한 후, 이 버퍼를 이후의 `Write` 호출에 제공하여 복사를 방지할 수 있습니다.

<!-- CL 345570 -->
`Reader.Reset` 및
`Writer.Reset` 메서드는 `nil` 버퍼를 가진 객체에서 호출될 때 기본 버퍼 크기를 사용합니다.

<!-- bufio -->

#### [bytes](/pkg/bytes/)

<!-- CL 351710 -->
새로운 `Cut` 함수는
`[]byte`를 구분자를 기준으로 잘라냅니다. 이는
`Index` (/pkg/bytes/#Index),
`IndexByte` (/pkg/bytes/#IndexByte),
`IndexRune` (/pkg/bytes/#IndexRune),
그리고 `SplitN` (/pkg/bytes/#SplitN)의
많은 일반적인 사용 사례를 대체하고 단순화할 수 있습니다.

<!-- CL 323318, CL 332771 -->
[`Trim`](/pkg/bytes/#Trim), [`TrimLeft`](/pkg/bytes/#TrimLeft),
그리고 [`TrimRight`](/pkg/bytes/#TrimRight)는 이제 할당 없이 작동하며, 특히 작은 ASCII 문자열을 자르는 경우 최대 10배 더 빠릅니다.

<!-- CL 359485 -->
`Title` 함수는 이제 사용되지 않습니다. 이 함수는 유니코드 구두점과 언어별 대소문자 규칙을 처리하지 않으며, `golang.org/x/text/cases` 패키지로 대체됩니다.

<!-- 바이트 -->

#### [crypto/elliptic](/pkg/crypto/elliptic/)

<!-- CL 320071, CL 320072, CL 320074, CL 361402, CL 360014 -->
`[P224]`,
`[P384]` 및
`[P521]` 커브
구현은 이제 `addchain` 및
`fiat-crypto` 프로젝트에서 생성된 코드로 모두 지원됩니다. `fiat-crypto`는 수치 연산에 대한 형식적으로 검증된 모델을 기반으로 합니다. 이제 더 안전하고 완전한 수식을 사용하며 내부 API를 사용합니다. P-224 및 P-384는 이제 약 4배 더 빠릅니다. 모든 특정 커브 구현은 이제 일정한 시간 내에 실행됩니다.

유효하지 않은 곡선 점을 사용하는 경우 (즉, `IsOnCurve` 메서드가 `false`를 반환하는 점, 그리고 `Unmarshal` ([pkg/crypto/elliptic#Unmarshal](https://pkg/crypto/elliptic#Unmarshal)) 또는 유효한 점을 사용하는 `Curve` 메서드에 의해 반환되지 않는 점)는 항상 정의되지 않은 동작을 일으킵니다. 이는 키 복구 공격으로 이어질 수 있으며, 현재 새로운 백엔드에서는 지원되지 않습니다. 만약 유효하지 않은 점을 `P224`, `P384`, 또는 `P521` 메서드에 제공하면, 해당 메서드는 이제 임의의 점을 반환합니다. 이러한 동작은 향후 릴리스에서 명시적인 패닉으로 변경될 수 있습니다.

<!-- crypto/elliptic -->

#### [crypto/tls](pkg/crypto/tls/)

<!-- CL 325250 -->
새로운 [`Conn.NetConn`](/pkg/crypto/tls/#Conn.NetConn)
메서드는 내부 [`net.Conn`](/pkg/net#Conn)에 접근을 허용합니다.

<!-- crypto/tls -->

#### [crypto/x509](/pkg/crypto/x509)

<!-- CL 353132, CL 353403 -->
[`Certificate.Verify`](/pkg/crypto/x509/#Certificate.Verify)
이제 macOS 및 iOS에서 인증서 유효성을 확인하기 위해 플랫폼 API를 사용합니다.
`VerifyOpts.Roots`가 `nil`로 전달되거나 `SystemCertPool`에서 반환된 루트 풀을 사용할 때 호출될 때.

<!-- CL 353589 -->
[`SystemCertPool`](/pkg/crypto/x509/#SystemCertPool)
이 이제 Windows에서 사용할 수 있습니다.

Windows, macOS, 및 iOS에서, `SystemCertPool`에 의해 반환된
[`CertPool`](/pkg/crypto/x509/#CertPool)에 추가 인증서가 추가된 경우,
`Certificate.Verify`는 다음 두 가지 검증을 수행합니다: 플랫폼 검증 API 및 시스템 루트를 사용한 검증, 그리고 Go 검증 및 추가 루트를 사용한 검증입니다.
플랫폼 검증 API에서 반환된 체인은 우선적으로 사용됩니다.

[`CertPool.Subjects`](/pkg/crypto/x509/#CertPool.Subjects)
은 더 이상 사용되지 않습니다. Windows, macOS 및 iOS에서
[`CertPool`](/pkg/crypto/x509/#CertPool)는
[`SystemCertPool`](/pkg/crypto/x509/#SystemCertPool)에서 반환되는 풀에는 플랫폼 루트가 포함되지 않습니다. `Subjects` 슬라이스에 반환되는 목록은 정적 목록이 플랫폼 정책을 적절하게 표현할 수 없으며, 플랫폼 API에서 사용할 수 없을 수도 있습니다.

MD5 해시(`MD5WithRSA`)에 의존하는 서명 알고리즘을 사용하여 인증서를 서명하는 기능은 Go 1.19에서 제거될 수 있습니다.

#### [debug/dwarf](/pkg/debug/dwarf/)

<!-- CL 380714 -->
`StructField` 및 `BasicType` 구조체 모두 이제 `DataBitOffset` 필드를 가지고 있으며, 이 필드는 `DW_AT_data_bit_offset` 속성이 존재하는 경우 해당 값을 저장합니다.

#### [debug/elf](/pkg/debug/elf/)

<!-- CL 352829 -->
`[`R_PPC64_RELATIVE`](/pkg/debug/elf/#R_PPC64_RELATIVE)
상수가 추가되었습니다.

<!-- 디버깅/ELF -->

#### [debug/plan9obj](/pkg/debug/plan9obj/)

<!-- CL 350229 -->
`File.Symbols` ([File.Symbols](/pkg/debug/plan9obj#File.Symbols))
메서드가 이제 파일에 심볼 섹션이 없는 경우, 새로운 내보낸 오류 값인 `ErrNoSymbols` ([ErrNoSymbols](/pkg/debug/plan9obj#ErrNoSymbols))을 반환합니다.

<!-- debug/plan9obj -->

#### [embed](/pkg/embed/)

<!-- CL 359413 -->
`go:embed`
지시어는 이제 `all:`으로 시작하여 이름이 점(.) 또는 밑줄(_)로 시작하는 파일도 포함할 수 있습니다.

<!-- debug/plan9obj -->

#### [go/ast](pkg/go/ast/)

<!-- https://golang.org/issue/47781, CL 325689, CL 327149, CL 348375, CL 348609 -->
제안된 대로,
[
`go/ast` 및 `go/token` 패키지에 대한 기능 추가 (매개변수화된 함수 및 유형 지원)
](https://go.googlesource.com/proposal/+/master/design/47781-parameterized-go-ast.md)
다음 기능이 `go/ast` 패키지에 추가되었습니다:

- [`FuncType`](/pkg/go/ast/#FuncType)
  및 [`TypeSpec`](/pkg/go/ast/#TypeSpec)
  노드는 타입 매개변수가 있는 경우, 새로운 필드 `TypeParams`를 추가합니다.
  - 새로운 표현식 노드 [`IndexListExpr`](/pkg/go/ast/#IndexListExpr)는 여러 인덱스를 갖는 인덱스 표현식을 나타내며, 이는 함수 및 타입 인스턴스화에 사용됩니다.
    특히, 명시적인 타입 인수가 여러 개인 경우에 사용됩니다.

#### [go/constant](/pkg/go/constant/)

<!-- https://golang.org/issue/46211, CL 320491 -->
새로운 `[`Kind.String`](/pkg/go/constant/#Kind.String)`
메서드는 수신 객체의 종류에 대한 사람이 읽을 수 있는 이름을 반환합니다.

#### [go/token](pkg/go/token/)

<!-- https://golang.org/issue/47781, CL 324992 -->
새로운 상수 [`TILDE`](/pkg/go/token/#TILDE)는 제안된 대로 `~` 토큰을 나타냅니다.
[
go/ast 및 go/token에 대한 추가 기능으로, 매개변수화된 함수 및 타입을 지원
](https://go.googlesource.com/proposal/+/master/design/47781-parameterized-go-ast.md).

#### [go/types](pkg/go/types/)

<!-- https://golang.org/issue/46648 -->
새로운 `Config.GoVersion` 필드는 허용되는 Go 언어 버전을 설정합니다.

<!-- https://golang.org/issue/47916 -->
제안된 내용에 따라,
[
`go/types` 패키지에 타입 매개변수를 지원하기 위한 추가 기능
](https://go.googlesource.com/proposal/+/master/design/47916-parameterized-go-types.md)
이 패키지에 다음과 같은 추가 기능이 포함됩니다:

- 새로운 타입
    [`TypeParam`](/pkg/go/types/#TypeParam), 팩토리 함수
    [`NewTypeParam`](/pkg/go/types/#NewTypeParam),
    그리고 관련 메서드를 추가하여 타입 매개변수를 나타냅니다.
  - 새로운 타입
    [`TypeParamList`](/pkg/go/types/#TypeParamList)은 타입 매개변수의 목록을 포함합니다.
  - 새로운 타입
    [`TypeList`](/pkg/go/types/#TypeList)은 타입의 목록을 포함합니다.
  - 새로운 팩토리 함수
    [`NewSignatureType`](/pkg/go/types/#NewSignatureType)는
    [`Signature`](/pkg/go/types/#Signature)를 할당하고 (수신자 또는 함수) 타입 매개변수를 포함합니다.
    이러한 타입 매개변수에 액세스하려면 `Signature` 타입에 두 개의 새로운 메서드,
    [`Signature.RecvTypeParams`](/pkg/go/types/#Signature.RecvTypeParams) 및
    [`Signature.TypeParams`](/pkg/go/types/#Signature.TypeParams)가 있습니다.
  - [`Named`](/pkg/go/types/#Named) 타입에는 다음과 같은 네 개의 새로운 메서드가 있습니다.
    [`Named.Origin`](/pkg/go/types/#Named.Origin)는 인스턴스화된 타입의 원래 매개변수화된 타입을 가져오고,
    [`Named.TypeArgs`](/pkg/go/types/#Named.TypeArgs) 및
    [`Named.TypeParams`](/pkg/go/types/#Named.TypeParams)는 인스턴스화되거나 매개변수화된 타입의 타입 인자 또는 타입 매개변수를 가져오고,
    [`Named.SetTypeParams`](/pkg/go/types/#Named.TypeParams)는 타입 매개변수를 설정합니다 (예: 이름이 지정된 타입을 가져올 때, 이름이 지정된 타입과 타입 매개변수를 동시에 할당할 수 없는 경우).
  - [`Interface`](/pkg/go/types/#Interface) 타입에는 다음과 같은 네 개의 새로운 메서드가 있습니다.
    [`Interface.IsComparable`](/pkg/go/types/#Interface.IsComparable) 및
    [`Interface.IsMethodSet`](/pkg/go/types/#Interface.IsMethodSet)는 인터페이스로 정의된 타입 세트의 속성을 쿼리하고,
    [`Interface.MarkImplicit`](/pkg/go/types/#Interface.MarkImplicit) 및
    [`Interface.IsImplicit`](/pkg/go/types/#Interface.IsImplicit)는 타입 제약 조건 리터럴 주변의 암시적 인터페이스를 설정하고 테스트하는 데 사용됩니다.
  - 새로운 타입
    [`Union`](/pkg/go/types/#Union) 및
    [`Term`](/pkg/go/types/#Term), 팩토리 함수
    [`NewUnion`](/pkg/go/types/#NewUnion) 및
    [`NewTerm`](/pkg/go/types/#NewTerm), 그리고 관련
    메서드를 추가하여 인터페이스에서 타입 세트를 나타냅니다.
  - 새로운 함수
    [`Instantiate`](/pkg/go/types/#Instantiate)는 매개변수화된 타입을 인스턴스화합니다.
  - 새로운 [`Info.Instances`](/pkg/go/types/#Info.Instances)
    맵은 새로운
    [`Instance`](/pkg/go/types/#Instance) 타입을 통해 함수 및 타입 인스턴스화를 기록합니다.
  - <!-- CL 342671 -->
    새로운 타입 [`ArgumentError`](/pkg/go/types/#ArgumentError) 및 관련 메서드는 타입 인자에 대한 오류를 나타내는 데 사용됩니다.
  - <!-- CL 353089 -->
    새로운 타입 [`Context`](/pkg/go/types/#Context) 및 팩토리 함수
    [`NewContext`](/pkg/go/types/#NewContext)는 타입 확인된 패키지 간에 동일한 타입 인스턴스를 공유하는 데 사용되며, 새로운
    [`Config.Context`](/pkg/go/types/#Config.Context) 필드를 통해 구현됩니다.

다음 프레디케이트:
[`AssignableTo`](/pkg/go/types/#AssignableTo),
[`ConvertibleTo`](/pkg/go/types/#ConvertibleTo),
[`Implements`](/pkg/go/types/#Implements),
[`Identical`](/pkg/go/types/#Identical),
[`IdenticalIgnoreTags`](/pkg/go/types/#IdenticalIgnoreTags), 및
[`AssertableTo`](/pkg/go/types/#AssertableTo)
이제 일반화된 인터페이스, 즉 Go 코드에서 유형 제약 조건으로만 사용될 수 있는 인터페이스를 인수로 사용합니다.
참고: `AssignableTo`, `ConvertibleTo`, `Implements`, 및 `AssertableTo`의 동작은 인스턴스화되지 않은 제네릭 유형에 대해 정의되지 않으며, `AssertableTo`는 첫 번째 인수가 일반화된 인터페이스인 경우에 대해 정의되지 않습니다.

#### [html/template](/pkg/html/template/)

<!-- CL 321491 -->
`range` 파이프라인 내에서 새로운
`{{break}}` 명령은 루프를 조기에 종료하고,
새로운 `{{continue}}` 명령은 즉시 다음 루프 반복을 시작합니다.

<!-- CL 321490 -->
`and` 함수는 이제 항상 모든 인수를 평가하지 않습니다. 대신, 첫 번째 인수가 `false`로 평가되는 시점에 평가를 중단합니다. 마찬가지로, `or` 함수는 첫 번째 인수가 `true`로 평가되는 시점에 평가를 중단합니다. 이는 인수가 함수 호출인 경우에 차이를 발생시킵니다.

<!-- html/템플릿 -->

#### [이미지/그리기](/pkg/image/draw/)

<!-- CL 340049 -->
`Draw` 및 `DrawMask`의 기본 구현 (가장 일반적인 이미지 유형이 아닌 경우에 사용)이 이제 더 빠릅니다.
이 구현은 `draw.RGBA64Image` 및 `image.RGBA64Image` 인터페이스를 구현하는 경우에 특히 그렇습니다.
이러한 인터페이스는 Go 1.17에서 추가되었습니다.

<!-- 이미지/그리기 -->

#### [net](/pkg/net/)

<!-- CL 340261 -->
[`net.Error.Temporary`](/pkg/net#Error)이 더 이상 사용되지 않습니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- CL 330852 -->
WebAssembly 타겟에서, `Dial`, `DialContext`,
`DialTLS` 및 `DialTLSContext` 메서드 필드가
[`Transport`](/pkg/net/http/#Transport)에 정의되어 있고, 지정된 경우 HTTP 요청을 올바르게 사용됩니다.

<!-- CL 338590 -->
새로운
[`Cookie.Valid`](/pkg/net/http#Cookie.Valid)
메서드는 쿠키가 유효한지 여부를 보고합니다.

<!-- CL 346569 -->
새로운
[`MaxBytesHandler`](/pkg/net/http#MaxBytesHandler)
함수는 `Handler`를 생성하며, 이는 `ResponseWriter`와 `Request.Body`를
[`MaxBytesReader`](/pkg/net/http#MaxBytesReader)로 감쌉니다.

<!-- CL 359634, CL 360381, CL 362735 -->
ASCII 문자가 아닌 문자를 포함하는 도메인 이름을 검색할 때,
이제 유니코드-ASCII 변환은 [Unicode IDNA
호환 처리](https://unicode.org/reports/tr46/) 표준(UTS #46)에 정의된
Nontransitional Processing에 따라 수행됩니다. 다음과 같은 네 개의 고유한 문자의 해석이 변경됩니다: ß, ς,
공간 대체 문자 U+200D, 그리고 공간 대체 문자 아닌 문자
U+200C. Nontransitional Processing는 대부분의 애플리케이션 및 웹 브라우저와 호환됩니다.

<!-- net/http -->

#### [os/user](/pkg/os/user/)

<!-- CL 330753 -->
[`User.GroupIds`](/pkg/os/user#User.GroupIds)
이제 cgo가 사용 불가능한 경우, Go 네이티브 구현을 사용합니다.

<!-- os/user -->

#### [reflect](/pkg/reflect/)

<!-- CL 356049, CL 320929 -->
새로운
[`Value.SetIterKey`](/pkg/reflect/#Value.SetIterKey)
및
[`Value.SetIterValue`](/pkg/reflect/#Value.SetIterValue)
메서드는 맵 반복자를 소스로 사용하여 Value를 설정합니다. 이 메서드는
`Value.Set(iter.Key())` 및 `Value.Set(iter.Value())`와 동일하지만, 덜한 할당을 수행합니다.

<!-- CL 350691 -->
새로운
[`Value.UnsafePointer`](/pkg/reflect/#Value.UnsafePointer)
메서드는 Value의 값을 `unsafe.Pointer`로 반환합니다.
이를 통해 호출자는 `Value.UnsafeAddr` 및 `Value.Pointer`에서 `unsafe.Pointer`로의 변환을 수행할 필요 없이 이전 방식으로 전환할 수 있습니다 (unsafe.Pointer 규칙에 따라).

<!-- CL 321891 -->
새로운
[`MapIter.Reset`](/pkg/reflect/#MapIter.Reset)
메서드는 수신자를 다른 맵을 순회하도록 변경합니다.
[`MapIter.Reset`](/pkg/reflect/#MapIter.Reset)
의 사용은 할당 없이 여러 맵을 순회할 수 있게 합니다.

<!-- CL 352131 -->
다음 메서드 (
[`Value.CanInt`](/pkg/reflect#Value.CanInt),
[`Value.CanUint`](/pkg/reflect#Value.CanUint),
[`Value.CanFloat`](/pkg/reflect#Value.CanFloat),
[`Value.CanComplex`](/pkg/reflect#Value.CanComplex)
)
가 `Value` ([/pkg/reflect#Value])에 추가되어, 변환이 안전한지 테스트합니다.

<!-- CL 357962 -->
[`Value.FieldByIndexErr`](/pkg/reflect#Value.FieldByIndexErr)
이 기능을 추가하여, 임베디드 구조체로의 `nil` 포인터를 거치면서 발생하는 오류를 방지합니다. 이 오류는 [`Value.FieldByIndex`](/pkg/reflect#Value.FieldByIndex)에서 발생합니다.

<!-- CL 341333 -->
[`reflect.Ptr`](/pkg/reflect#Ptr) 및
[`reflect.PtrTo`](/pkg/reflect#PtrTo)
이 `reflect.Pointer` 및
`reflect.PointerTo`로 각각 이름이 변경되었습니다. 이는 `reflect` 패키지의 나머지 부분과의 일관성을 유지하기 위함입니다.
기존 이름은 계속 작동하지만, 향후 Go 릴리스에서는 사용이 중단될 예정입니다.

<!-- 반영 -->

#### [regexp](/pkg/regexp/)

<!-- CL 354569 -->
[`regexp`](/pkg/regexp/)
이제 UTF-8 문자열의 각 유효하지 않은 바이트를 `U+FFFD`로 처리합니다.

<!-- regexp -->

#### [runtime/debug](/pkg/runtime/debug/)

<!-- CL 354569 -->
`BuildInfo` 구조체는 두 개의 새로운 필드를 가지고 있으며, 이 필드에는 바이너리가 어떻게 빌드되었는지에 대한 추가 정보가 포함되어 있습니다:

- [`GoVersion`](/pkg/runtime/debug#BuildInfo.GoVersion)
    은 바이너리를 빌드하는 데 사용된 Go 버전 정보를 담고 있습니다.
  - [`Settings`](/pkg/runtime/debug#BuildInfo.Settings)
    는 다음 구조체의 슬라이스로, 빌드에 대한 키/값 쌍을 담고 있습니다.
    [`BuildSettings`](/pkg/runtime/debug#BuildSettings)

<!-- 실행/디버깅 -->

#### [runtime/pprof](/pkg/runtime/pprof/)

<!-- CL 324129 -->
CPU 프로파일러는 이제 Linux에서 각 스레드별 타이머를 사용합니다. 이를 통해 프로파일러가 감지할 수 있는 최대 CPU 사용량을 늘리고, 일부 형태의 편향을 줄입니다.

<!-- runtime/pprof -->

#### [strconv](/pkg/strconv/)

<!-- CL 343877 -->
[`strconv.Unquote`](/pkg/strconv/#strconv.Unquote)
이제 유니코드 서류를 거부합니다.

<!-- strconv -->

#### [strings](/pkg/strings/)

<!-- CL 351710 -->
새로운 `Cut` 함수는
`string`을 구분자를 기준으로 자릅니다. 이는 `Index`, `IndexByte`, `IndexRune` 및 `SplitN`의
많은 일반적인 사용 사례를 대체하고 단순화할 수 있습니다.

<!-- CL 345849 -->
새로운 `Clone` 함수는 입력 `string`을 복사하지만, 반환된 복제된 `string`이 입력 `string`의 메모리를 참조하지 않습니다.

<!-- CL 323318, CL 332771 -->
[`Trim`](/pkg/strings/#Trim), [`TrimLeft`](/pkg/strings/#TrimLeft),
및 [`TrimRight`](/pkg/strings/#TrimRight)는 이제 할당 없이 작동하며, 특히 작은 ASCII 문자열에 대해서는 최대 10배 더 빠릅니다.

<!-- CL 359485 -->
`[Title](pkg/strings/#Title)` 함수가 이제 사용되지 않습니다. 이 함수는 유니코드 기호 및 언어별 대소문자 규칙을 처리하지 않으며, `golang.org/x/text/cases` 패키지로 대체됩니다.

<!-- 문자열 -->

#### [sync](/pkg/sync/)

<!-- CL 319769 -->
새로운 메서드
[`Mutex.TryLock`](/pkg/sync#Mutex.TryLock),
[`RWMutex.TryLock`](/pkg/sync#RWMutex.TryLock), 및
[`RWMutex.TryRLock`](/pkg/sync#RWMutex.TryRLock),
현재 잠금이 획득되지 않은 경우 잠금을 획득합니다.

<!-- 동기화 -->

#### [syscall](/pkg/syscall/)

<!-- CL 336550 -->
새로운 함수 [`SyscallN`](/pkg/syscall/?GOOS=windows#SyscallN)가 Windows용으로 도입되었으며, 임의의 개수의 인자를 사용하여 호출할 수 있습니다. 결과적으로,
[`Syscall`](/pkg/syscall/?GOOS=windows#Syscall),
[`Syscall6`](/pkg/syscall/?GOOS=windows#Syscall6),
[`Syscall9`](/pkg/syscall/?GOOS=windows#Syscall9),
[`Syscall12`](/pkg/syscall/?GOOS=windows#Syscall12),
[`Syscall15`](/pkg/syscall/?GOOS=windows#Syscall15), 및
[`Syscall18`](/pkg/syscall/?GOOS=windows#Syscall18)는 [`SyscallN`](/pkg/syscall/?GOOS=windows#SyscallN)를 대체하도록 폐기되었습니다.

<!-- CL 355570 -->
[`SysProcAttr.Pdeathsig`](/pkg/syscall/?GOOS=freebsd#SysProcAttr.Pdeathsig)
이 기능이 FreeBSD에서 지원됩니다.

<!-- syscall -->

```
#### [syscall/js](/pkg/syscall/js/)
```

<!-- CL 356430 -->
`Wrapper` 인터페이스가 제거되었습니다.

<!-- syscall/js -->

#### [테스팅](/pkg/testing/)

<!-- CL 343883 -->
`-run` 및 `-bench`의 인수에 `/` 연산자의 우선 순위를 높였습니다.
`A/B|C/D`는 이전에는 `A/(B|C)/D`로 처리되었지만, 이제는 `(A/B)|(C/D)`로 처리됩니다.

<!-- CL 356669 -->
`-run` 옵션이 특정 테스트를 선택하지 않으면,
`-count` 옵션은 무시됩니다. 이로 인해, 테스트 함수 자체가 실행될 때마다 서브 테스트의 집합이 변경되는 경우, 기존 테스트의 동작이 변경될 수 있습니다.

<!-- CL 251441 -->
새로운 `testing.F` 타입은
위에서 설명된 [퍼징 지원](#fuzzing)에서 사용됩니다. 테스트는 이제 `-test.fuzz`, `-test.fuzztime`,
그리고 `-test.fuzzminimizetime` 명령줄 옵션을 지원합니다.

<!-- 테스트 -->

#### [text/template](pkg/text/template/)

<!-- CL 321491 -->
`range` 파이프라인 내에서 새로운
`{{break}}` 명령어는 루프를 조기에 종료하고,
새로운 `{{continue}}` 명령어는 즉시 다음 루프 반복을 시작합니다.

<!-- CL 321490 -->
`and` 함수는 이제 항상 모든 인수를 평가하지 않습니다. 첫 번째 인수가 `false`로 평가되면 평가를 중단합니다. `or` 함수도 마찬가지로 첫 번째 인수가 `true`로 평가되면 평가를 중단합니다. 따라서 인수가 함수 호출인 경우에 차이가 발생합니다.

<!-- 텍스트/템플릿 -->

#### [text/template/parse](/pkg/text/template/parse/)

<!-- CL 321491 -->
이 패키지는 새로운
[text/template](/pkg/text/template/) 및
[html/template](/pkg/html/template/)
`{{break}}` 명령을 새로운 상수
[`NodeBreak`](/pkg/text/template/parse#NodeBreak] 및 새로운 유형
[`BreakNode`](/pkg/text/template/parse#BreakNode]를 통해 지원하며,
마찬가지로 새로운 `{{continue}}` 명령을 새로운 상수
[`NodeContinue`](/pkg/text/template/parse#NodeContinue] 및 새로운 유형
[`ContinueNode`](/pkg/text/template/parse#ContinueNode]를 통해 지원합니다.

<!-- 텍스트/템플릿 -->

#### [unicode/utf8](/pkg/unicode/utf8/)

<!-- CL 345571 -->
새로운 `AppendRune` 함수는 `rune`의 UTF-8 인코딩을 `[]byte`에 추가합니다. ([`/pkg/unicode/utf8/#AppendRune`](#AppendRune))

<!-- unicode/utf8 -->
