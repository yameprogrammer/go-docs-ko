<!--
참고: 이 문서와 이 디렉토리의 다른 문서들에서는
`hello` `world`와 같이 고정 폭 구절을 고정 폭이 아닌 공백으로 설정하는 것이 관례입니다.
이러한 구절에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

<style>
  main ul li { margin: 0.5em 0; }
</style>

## Go 1.18 소개 {#introduction}

최신 Go 릴리스인 버전 1.18은 언어, 툴체인 구현, 런타임 및 라이브러리의 변경 사항을 포함하는 중요한 릴리스입니다. Go 1.18은 [Go 1.17](/doc/go1.17) 이후 7개월 만에 출시되었습니다. 언제나 그렇듯이, 이번 릴리스에서도 Go 1 [호환성 약속](/doc/go1compat)을 유지합니다. 거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 기대합니다.

## 언어 변경 사항 {#language}

### 제네릭 (Generics) {#generics}

<!-- https://golang.org/issue/43651, https://golang.org/issue/45346 -->
Go 1.18에는 [Type Parameters Proposal](https://go.googlesource.com/proposal/+/refs/heads/master/design/43651-type-parameters.md)에서 설명한 제네릭 기능의 구현이 포함되어 있습니다. 여기에는 언어에 대한 중대한 변경 사항이 포함되어 있으나, 완전히 하위 호환됩니다.

이러한 새로운 언어 변경 사항으로는 실제 운영 환경에서 충분한 테스트를 거치지 않은 방대한 양의 새로운 코드가 필요했습니다. 이는 더 많은 사람들이 제네릭 코드를 작성하고 사용함에 따라 점차 이루어질 것입니다. 저희는 이 기능이 잘 구현되었으며 품질이 높다고 믿습니다. 하지만 Go의 대부분의 다른 측면들과 달리, 이 믿음을 실제 세계의 경험으로 뒷받침할 수는 없습니다. 따라서 제네릭이 적절한 곳에서의 사용은 권장하지만, 운영 환경에 제네릭 코드를 배포할 때는 적절한 주의를 기울여 주시기 바랍니다.

새로운 언어 기능들이 잘 설계되었고 명확하게 명시되었다고 믿지만, 저희가 실수를 했을 가능성도 있습니다.
저희는 [Go 1 호환성 보장](/doc/go1compat) 내용 중 "명세의 불일치나 불완전함을 해결해야 할 필요가 생길 경우, 해당 문제를 해결하는 과정에서 기존 프로그램의 의미나 적법성에 영향을 줄 수 있습니다. 저희는 구현 업데이트를 포함하여 이러한 문제를 해결할 권리를 보유합니다"라는 점을 강조하고 싶습니다. 또한 "컴파일러나 라이브러리에 명세를 위반하는 버그가 있는 경우, 해당 버그 동작에 의존하는 프로그램은 버그가 수정될 때 작동하지 않을 수 있습니다. 저희는 이러한 버그를 수정할 권리를 보유합니다"라고 명시되어 있습니다. 즉, 제네릭을 사용하는 코드 중 1.18 릴리스에서는 작동하지만 이후 릴리스에서는 작동하지 않는 코드가 발생할 가능성이 있습니다. 저희는 이러한 변경을 계획하거나 예상하고 있지 않습니다. 하지만 현재로서는 예측할 수 없는 이유로 인해 향후 릴리스에서 1.18 프로그램들이 작동하지 않게 되는 상황이 필요할 수도 있습니다. 저희는 이러한 파손(breakage)을 최대한 최소화하겠지만, 파손이 전혀 없을 것이라고 보장할 수는 없습니다.

다음은 가장 눈에 띄는 변경 사항 목록입니다. 더 포괄적인 개요는 [제안서](https://go.googlesource.com/proposal/+/refs/heads/master/design/43651-type-parameters.md)를 참조하십시오.
자세한 내용은 [언어 명세](/ref/spec)를 참조하십시오.

- [함수](/ref/spec#Function_declarations) 및 [타입 선언](/ref/spec#Type_declarations)의 구문이 이제 [타입 파라미터](/ref/spec#Type_parameter_declarations)를 허용합니다.
  - 파라미터화된 함수와 타입은 뒤에 대괄호`[]`로 타입 인자 목록을 지정하여 인스턴스화할 수 있습니다.
  - 새로운 토큰 `~`가 [연산자 및 구두점](/ref/spec#Operators_and_punctuation) 집합에 추가되었습니다.
  - [인터페이스 타입](/ref/spec#Interface_types) 구문이 이제 인터페이스의 타입 이름뿐만 아니라 임의의 타입 임베딩과 유니온 및 `~T` 타입 요소를 허용합니다. 이러한 인터페이스는 타입 제약(type constraints)으로만 사용할 수 있습니다.
    이제 인터페이스는 메서드 집합뿐만 아니라 타입 집합도 정의합니다.
  - 새로운 [사전 정의 식별자](/ref/spec#Predeclared_identifiers) `any`는 빈 인터페이스의 별칭입니다. `interface{}` 대신 사용할 수 있습니다.
  - 새로운 [사전 정의 식별자](/ref/spec#Predeclared_identifiers) `comparable`은 `==` 또는 `!=`를 사용하여 비교할 수 있는 모든 타입의 집합을 나타내는 인터페이스입니다. 이는 타입 제약으로만 사용(또는 임베딩)될 수 있습니다.

제네릭을 사용하는 유용한 세 가지 실험적 패키지가 있습니다.
이 패키지들은 `x/exp` 저장소에 있으며, 이들의 API는 Go 1 보장 범위에 포함되지 않으며 제네릭에 대한 경험이 쌓임에 따라 변경될 수 있습니다.

#### [`golang.org/x/exp/constraints`](https://pkg.go.dev/golang.org/x/exp/constraints)

제네릭 코드에 유용한 [`constraints.Ordered`](https://pkg.go.dev/golang.org/x/exp/constraints#Ordered)와 같은 제약 조건들입니다.

#### [`golang.org/x/exp/slices`](https://pkg.go.dev/golang.org/x/exp/slices)

모든 요소 타입의 슬라이스에서 동작하는 제네릭 함수 모음입니다.

#### [`golang.org/x/exp/maps`](https://pkg.go.dev/golang.org/x/exp/maps)

모든 키 또는 요소 타입의 맵(map)에서 작동하는 제네릭 함수 모음입니다.

현재 제네릭 구현에는 다음과 같은 알려진 제한 사항이 있습니다:

- <!-- https://golang.org/issue/47631 -->
    Go 컴파일러는 제네릭 함수나 메서드 내부의 타입 선언을 처리할 수 없습니다. 향후 릴리스에서 이 기능에 대한 지원을 제공할 예정입니다.
  - <!-- https://golang.org/issue/50937 -->
    Go 컴파일러는 미리 정의된 함수인 `real`, `imag`, `complex`에 타입 파라미터 타입의 인자를 전달하는 것을 허용하지 않습니다. 향후 릴리스에서 이 제한을 제거할 예정입니다.
  - <!-- https://golang.org/issue/51183 -->
    Go 컴파일러는 타입 파라미터 타입 `P`인 값 `x`에 대해 메서드 `m`을 호출하는 것을 `m`이 `P`의 제약 인터페이스(constraint interface)에 명시적으로 선언된 경우에만 지원합니다. 마찬가지로, `P`에 속한 모든 타입이 `m`을 구현하여 `m`이 `P`의 메서드 집합(method set)에 포함되어 있더라도, 메서드 값 `x.m` 및 메서드 표현식 `P.m` 또한 `m`이 `P`에 명시적으로 선언된 경우에만 지원됩니다. 향후 릴리스에서 이 제한을 제거할 예정입니다.
  - <!-- https://golang.org/issue/51576 -->
    Go 컴파일러는 타입 파라미터의 타입 집합에 있는 모든 타입이 필드 `f`를 가지고 있더라도, 타입 파라미터 타입인 `x`의 구조체 필드 `x.f`에 접근하는 것을 지원하지 않습니다. 향후 릴리스에서 이 제한을 제거할 수 있습니다.
  - <!-- https://golang.org/issue/49030 -->
    구조체 타입의 익명 필드로 타입 파라미터 또는 타입 파라미터를 가리키는 포인터를 임베딩(embedding)하는 것은 허용되지 않습니다. 마찬가지로, 인터페이스 타입에 타입 파라미터를 임베딩하는 것도 허용되지 않습니다. 이것들이 나중에 허용될지 여부는 현재로서는 불분명합니다.
  - 두 개 이상의 항을 가진 유니온(union) 요소는 비어 있지 않은 메서드 집합을 가진 인터페이스 타입을 포함할 수 없습니다. 이것이 나중에 허용될지 여부는 현재로서는 불분명합니다.

제네릭(Generics)은 Go 생태계에도 큰 변화를 의미합니다. 여러 핵심 도구에 제네릭 지원 기능을 업데이트했지만, 아직 해야 할 일이 많이 남아 있습니다. 나머지 도구와 문서, 라이브러리들이 이러한 언어적 변화를 따라잡는 데에는 시간이 걸릴 것입니다.

### 버그 수정 {#bug_fixes}

Go 1.18 컴파일러는 이제 함수 리터럴 내부에서 설정되었지만 한 번도 사용되지 않은 변수에 대해 `declared but not used` 에러를 정확하게 보고합니다. Go 1.18 이전에는 컴파일러가 이러한 경우에 에러를 보고하지 않았습니다. 이는 오랫동안 해결되지 않았던 컴파일러 이슈 [#8560](/issue/8560)을 수정하는 것입니다. 이 변경으로 인해 (잠재적으로 잘못된) 프로그램들이 더 이상 컴파일되지 않을 수 있습니다. 필요한 수정 방법은 간단합니다. 프로그램이 실제로 잘못되었다면 이를 수정하거나, 해당 변수를 블랭크 식별자 `_`에 할당하는 등의 방식으로 변수를 사용하십시오. `go vet`이 항상 이 에러를 지적해 왔기 때문에, 영향을 받는 프로그램의 수는 매우 적을 것으로 예상됩니다.

Go 1.18 컴파일러는 이제 `'1' << 32`와 같은 rune 상수 표현식을 미리 선언된 함수인 `print` 및 `println`의 인자로 전달할 때 오버플로우를 보고하며, 이는 사용자 정의 함수의 동작과 일치합니다. Go 1.18 이전에는 컴파일러가 이러한 경우에 오류를 보고하지 않았으며, 해당 상수 인자가 `int64`에 적합한 경우 이를 묵묵히 수용했습니다. 이 변경으로 인해 (잠재적으로 잘못된) 프로그램이 더 이상 컴파일되지 않을 수 있습니다. 필요한 해결 방법은 간단합니다. 프로그램이 실제로 잘못되었다면 수정하거나, 문제가 되는 인자를 올바른 타입으로 명시적으로 변환하십시오. `go vet`이 항상 이 오류를 지적해 왔으므로, 영향을 받는 프로그램의 수는 매우 적을 가능성이 높습니다.

## 포트 {#ports}

### AMD64 {#amd64}

<!-- CL 349595 -->
Go 1.18에서는 컴파일 시 AMD64 아키텍처의 최소 타겟 버전을 선택하는 새로운 `GOAMD64` 환경 변수가 도입되었습니다. 허용되는 값은 `v1`, `v2`, `v3` 또는 `v4`입니다. 레벨이 높아질수록 추가적인 프로세서 기능이 필요하며 이를 활용합니다. 자세한 설명은 [여기](/wiki/MinimumRequirements#amd64)에서 확인할 수 있습니다.

`GOAMD64` 환경 변수의 기본값은 `v1`입니다.

### RISC-V {#riscv}

<!-- golang.org/issue/47100, CL 334872 -->
Linux의 64비트 RISC-V 아키텍처(`linux/riscv64` 포트)에서 이제 `c-archive` 및 `c-shared` 빌드 모드를 지원합니다.

### Linux {#linux}

<!-- golang.org/issue/45964 -->
Go 1.18은 리눅스 커널 버전 2.6.32 이상을 요구합니다.

### Windows {#windows}

<!-- https://golang.org/issue/49759 -->
이제 `windows/arm` 및 `windows/arm64` 포트가 비협력적 선점(non-cooperative preemption)을 지원합니다. 이로써 4개의 모든 Windows 포트에서 해당 기능을 사용할 수 있게 되었으며, 이를 통해 장시간 블로킹되는 Win32 함수를 호출할 때 발생하는 미묘한 버그들이 해결될 것으로 기대됩니다.

### iOS {#ios}

<!-- golang.org/issue/48076, golang.org/issue/49616 -->
iOS(`ios/arm64` 포트) 및 AMD64 기반 macOS에서 실행되는 iOS 시뮬레이터(`ios/amd64` 포트)의 경우,
Go 1.18부터 iOS 12 이상 버전이 필요하며 이전 버전에 대한 지원은 중단되었습니다.

### FreeBSD {#freebsd}

Go 1.18은 이미 수명 주기(end-of-life)가 종료된 FreeBSD 11.x에서 지원되는 마지막 릴리스입니다. Go 1.19는 FreeBSD 12.2+ 또는 FreeBSD 13.0+가 필요합니다.
FreeBSD 13.0+는 `COMPAT_FREEBSD12` 옵션이 설정된 커널이 필요합니다(이는 기본값입니다).

## 도구 {#tools}

### 퍼징 (Fuzzing) {#fuzzing}

Go 1.18에는 [fuzzing 제안서](/issue/44551)에 설명된 fuzzing 구현이 포함되어 있습니다.

시작하시려면 [fuzzing landing page](/security/fuzz)를 참조하세요.

퍼징(fuzzing)은 많은 양의 메모리를 소비하며 실행 중 머신의 성능에 영향을 줄 수 있음을 유의하시기 바랍니다. 또한, 퍼징 엔진은 실행 중에 테스트 커버리지를 확장하는 값들을 `$GOCACHE/fuzz` 내의 퍼즈 캐시 디렉토리에 기록합니다. 현재 퍼즈 캐시에 기록될 수 있는 파일 수나 총 바이트 수에 제한이 없으므로, 많은 양의 저장 공간(수 GB에 달할 수 있음)을 차지할 수 있습니다.

### Go 명령 {#go-command}

#### `go` `get` {#go-get}

<!-- golang.org/issue/43684 -->
`go` `get`은 더 이상 모듈 인식 모드(module-aware mode)에서 패키지를 빌드하거나 설치하지 않습니다. 이제 `go` `get`은 `go.mod`의 의존성을 조정하는 전용 명령어로 사용됩니다. 사실상 `-d` 플래그가 항상 활성화된 상태와 같습니다. 현재 모듈 컨텍스트 외부에서 실행 파일의 최신 버전을 설치하려면 [`go` `install` `example.com/cmd@latest`](/ref/mod#go-install)를 사용하십시오. `latest` 대신 모든 [버전 쿼리](/ref/mod#version-queries)를 사용할 수 있습니다. 이러한 형태의 `go` `install`은 Go 1.16에서 추가되었으므로, 이전 버전을 지원하는 프로젝트에서는 `go` `install`과 `go` `get` 두 가지 모두에 대한 설치 지침을 제공해야 할 수도 있습니다. `go` `get`을 모듈 외부에서 사용하면 업데이트할 `go.mod` 파일이 없으므로 이제 에러를 보고합니다. GOPATH 모드(`GO111MODULE=off`)에서는 `go` `get`이 이전과 동일하게 패키지를 빌드하고 설치합니다.

#### 자동 `go.mod` 및 `go.sum` 업데이트 {#go-mod-updates}

<!-- https://go.dev/issue/45551 -->
`go` `mod` `graph`,
`go` `mod` `vendor`,
`go` `mod` `verify`, 그리고
`go` `mod` `why` 서브커맨드는
더 이상 `go.mod` 및
`go.sum` 파일을 자동으로 업데이트하지 않습니다.
(해당 파일들은 `go` `get`,
`go` `mod` `tidy`, 또는
`go` `mod` `download`를 사용하여 명시적으로 업데이트할 수 있습니다.)

#### `go` `version` {#go-version}

<!-- golang.org/issue/37475 -->
이제 `go` 명령어가 바이너리에 버전 관리 정보를 포함합니다. 여기에는 현재 체크아웃된 리비전, 커밋 시간, 그리고 수정되었거나 추적되지 않은 파일이 있는지 여부를 나타내는 플래그가 포함됩니다. `go` 명령어가 Git, Mercurial, Fossil 또는 Bazaar 저장소 내의 디렉토리에서 실행되고, `main` 패키지와 이를 포함하는 메인 모듈이 동일한 저장소에 있는 경우 버전 관리 정보가 포함됩니다. 이 정보는 `-buildvcs=false` 플래그를 사용하여 제외할 수 있습니다.

<!-- golang.org/issue/37475 -->
추가적으로, `go` 명령어는 빌드 태그 및 툴 태그(`-tags`로 설정), 컴파일러, 어셈블러, 링커 플래그(예: `-gcflags`), cgo 활성화 여부, 그리고 활성화된 경우 cgo 환경 변수 값(예: `CGO_CFLAGS`)을 포함한 빌드 정보를 내장합니다.
VCS 정보와 빌드 정보는 모두 모듈 정보와 함께 `go` `version` `-m` `file` 또는 `runtime/debug.ReadBuildInfo` (현재 실행 중인 바이너리의 경우), 또는 새로운 [`debug/buildinfo`](#debug/buildinfo) 패키지를 사용하여 읽을 수 있습니다.

<!-- CL 369977 -->
임베디드 빌드 정보의 기본 데이터 형식은 새로운 go 릴리스에 따라 변경될 수 있으므로, 오래된 버전의 `go`는 최신 버전의 `go`로 생성된 빌드 정보를 처리하지 못할 수 있습니다.
`go` 1.18 버전으로 빌드된 바이너리에서 버전 정보를 읽으려면, `go` 1.18 이상의 `go` `version` 명령어와 `debug/buildinfo` 패키지를 사용하십시오.

#### `go` `mod` `download` {#go-mod-download}

<!-- https://golang.org/issue/44435 -->
메인 모듈의 `go.mod` 파일에 [`go` `1.17`](/ref/mod#go-mod-file-go) 또는 그 이상의 버전이 지정된 경우, 인자 없이 `go` `mod` `download`를 실행하면 이제 메인 모듈의 `go.mod` 파일에 명시적으로 [required](/ref/mod#go-mod-file-require)로 지정된 모듈의 소스 코드만 다운로드합니다. (`go` `1.17` 이상의 모듈에서는 해당 세트에 메인 모듈의 패키지와 테스트를 빌드하는 데 필요한 모든 종속성이 이미 포함되어 있습니다.)
간접 종속성(transitive dependencies)의 소스 코드까지 함께 다운로드하려면 `go` `mod` `download` `all`을 사용하십시오.

#### `go` `mod` `vendor` {#go-mod-vendor}

<!-- https://golang.org/issue/47327 -->
이제 `go` `mod` `vendor` 하위 명령어가 출력 디렉터리를 설정하는 `-o` 플래그를 지원합니다.
(다른 `go` 명령어들은 `-mod=vendor`로 패키지를 로드할 때 여전히 모듈 루트에 있는 `vendor` 디렉터리에서 읽으므로, 이 플래그의 주요 용도는 패키지 소스 코드를 수집해야 하는 서드파티 도구를 위한 것입니다.)

#### `go` `mod` `tidy` {#go-mod-tidy}

<!-- https://golang.org/issue/47738, CL 344572 -->
이제 `go` `mod` `tidy` 명령은 [빌드 리스트](/ref/mod#glos-build-list)의 각 임포트된 패키지가 단 하나의 모듈에 의해 제공되는지 확인하는 데 소스 코드가 필요한 모듈에 대해 `go.sum` 파일에 추가 체크섬을 유지합니다. 이러한 상황은 드물며, 이를 적용하지 않을 경우 빌드 오류가 발생하므로, 이 변경 사항은 메인 모듈의 `go.mod` 파일에 명시된 `go` 버전에 따라 조건부로 적용되지 _않습니다_.

#### `go` `work` {#go-work}

<!-- https://golang.org/issue/45713 -->
이제 `go` 명령어가 "워크스페이스(Workspace)" 모드를 지원합니다. 작업 디렉토리나 상위 디렉토리에서 `go.work` 파일이 발견되거나, `GOWORK` 환경 변수를 통해 지정된 경우 `go` 명령어는 워크스페이스 모드로 동작합니다. 워크스페이스 모드에서는 일반적인 `go.mod` 파일을 통해 단일 메인 모듈을 지정하는 대신, `go.work` 파일을 사용하여 모듈 해결(module resolution)의 루트로 사용될 메인 모듈 집합을 결정합니다. 자세한 내용은 [`go work`](/pkg/cmd/go#hdr-Workspace_maintenance) 문서를 참조하십시오.

#### `go` `build` `-asan` {#go-build-asan}

<!-- CL 298612 -->
`go` `build` 명령 및 관련 명령들이 이제 `-asan` 플래그를 지원합니다. 이 플래그를 사용하면 주소 분석기(C 컴파일러 옵션 `-fsanitize=address`)로 컴파일된 C (또는 C++) 코드와의 상호 운용이 가능합니다.

#### `go` `test` {#go-test}

<!-- CL 251441 -->
`go` 명령어가 이제 [위에서 설명한 퍼징 지원](#fuzzing)을 위한 추가 명령줄 옵션을 지원합니다:

- `go test`는 `-fuzz`, `-fuzztime` 및 `-fuzzminimizetime` 옵션을 지원합니다.
    자세한 내용은 [`go help testflag`](/pkg/cmd/go#hdr-Testing_flags) 문서를 참조하십시오.
  - `go clean`은 `-fuzzcache` 옵션을 지원합니다.
    자세한 내용은 [`go help clean`](/pkg/cmd/go#hdr-Remove_object_files_and_cached_files) 문서를 참조하십시오.

#### `//go:build` 라인 {#go-build-lines}

<!-- CL 240611 -->
Go 1.17에서는 `//` `+build` 라인 대신 빌드 제약 조건을 작성하는 더 읽기 쉬운 방법으로 `//go:build` 라인을 도입했습니다.
Go 1.17부터 `gofmt`는 기존 `+build` 라인과 일치하도록 `//go:build` 라인을 추가하고 이를 동기화하며, `go` `vet`은 두 라인이 서로 일치하지 않을 때 이를 진단합니다.

Go 1.18의 출시로 Go 1.16에 대한 지원이 종료됨에 따라, 이제 모든 지원되는 Go 버전은 `//go:build` 라인을 인식합니다. Go 1.18에서 `go` `fix`는 `go.mod` 파일에 `go` `1.18` 이상을 선언한 모듈에서 이제는 더 이상 사용되지 않는 `//` `+build` 라인을 제거합니다.

더 자세한 정보는 [go.dev/design/draft-gobuild](/design/draft-gobuild)를 참조하세요.

### Gofmt {#gofmt}

<!-- https://golang.org/issue/43566 -->
`gofmt`가 이제 입력 파일을 동시에 읽고 포맷하며, 메모리 제한은 `GOMAXPROCS`에 비례합니다. 여러 개의 CPU가 있는 머신에서 `gofmt`의 속도가 상당히 빨라졌을 것입니다.

### Vet {#vet}

#### Generics 관련 업데이트 {#vet-generics}

<!-- https://golang.org/issue/48704 -->
`vet` 도구가 제네릭 코드를 지원하도록 업데이트되었습니다. 대부분의 경우, 타입 파라미터를 해당 [타입 세트](/ref/spec#Interface_types)의 타입으로 대체했을 때, 그와 동일한 비제네릭 코드에서 에러를 보고했을 상황이라면 제네릭 코드에서도 에러를 보고합니다.
예를 들어, `vet`은 다음과 같은 경우에 포맷 에러를 보고합니다.

```go
func Print[T ~int|~string](t T) {
		fmt.Printf("%d", t)
	}
```

`Print[string]`의 제네릭이 아닌 동등한 코드에서는 형식 오류(format error)를 보고할 것이기 때문입니다:

```go
func PrintString(x string) {
		fmt.Printf("%d", x)
	}
```

#### 기존 체커의 정밀도 개선 {#vet-precision}

<!-- CL 323589 356830 319689 355730 351553 338529 -->
`cmd/vet` 검사기인 `copylock`, `printf`,
`sortslice`, `testinggoroutine`, 그리고 `tests`에
추가적인 코드 패턴을 처리하기 위한 적절한 정밀도 개선이 이루어졌습니다.
이로 인해 기존 패키지에서 새로운 오류가 보고될 수 있습니다. 예를 들어,
`printf` 검사기는 이제 문자열 상수를 연결하여 생성된 포맷팅 문자열을 추적합니다. 따라서 `vet`은 다음과 같은 코드에서 오류를 보고합니다:

// fmt.Printf 포맷팅 지시어 %d가 Println에 전달되고 있습니다.
	  fmt.Println("%d"+` ≡ x (mod 2)`+"\n", x%2)

## 런타임 {#runtime}

<!-- https://golang.org/issue/44167 -->
가비지 컬렉터가 실행 빈도를 결정할 때, 이제 힙 이외의 가비지 컬렉션 작업 소스(예: 스택 스캔)를 포함합니다. 그 결과, 이러한 소스들의 비중이 클 때 가비지 컬렉터 오버헤드가 더 예측 가능해집니다. 대부분의 애플리케이션에서 이러한 변경 사항은 무시할 수 있는 수준이겠지만, 일부 Go 애플리케이션은 이전보다 메모리를 적게 사용하고 가비지 컬렉션에 더 많은 시간을 소비하거나, 혹은 그 반대의 경우가 발생할 수 있습니다. 권장되는 해결 방법은 필요한 경우 `GOGC` 값을 조정하는 것입니다.

<!-- CL 358675, CL 353975, CL 353974 -->
이제 런타임이 운영체제에 메모리를 더 효율적으로 반환하며, 그 결과로 더 공격적으로 작동하도록 튜닝되었습니다.

<!-- CL 352057, https://golang.org/issue/45728 -->
Go 1.17에서는 일반적으로 스택 트레이스의 인자 포맷팅이 개선되었으나, 레지스터를 통해 전달된 인자의 경우 부정확한 값이 출력될 수 있었습니다.
Go 1.18에서는 부정확할 가능성이 있는 각 값 뒤에 물음표(`?`)를 출력함으로써 이 점이 개선되었습니다.

<!-- CL 347917 -->
내장 함수 `append`가 새로운 기본 배열(underlying array)을 할당해야 할 때, 슬라이스를 얼마나 늘릴지 결정하는 공식이 약간 변경되었습니다.
새로운 공식은 할당 동작의 갑작스러운 변화가 발생할 가능성이 더 적습니다.

## 컴파일러 {#compiler}

<!-- https://golang.org/issue/40724 -->
Go 1.17은 선택된 운영체제의 64비트 x86 아키텍처에서 스택 대신 레지스터를 사용하여 함수 인자와 결과값을 전달하는 새로운 방식을 [구현했습니다](go1.17#compiler).
Go 1.18은 지원 플랫폼을 확장하여 64비트 ARM (`GOARCH=arm64`), 빅 엔디안 및 리틀 엔디안 64비트 PowerPC (`GOARCH=ppc64`, `ppc64le`), 그리고 모든 운영체제의 64비트 x86 아키텍처 (`GOARCH=amd64`)를 포함합니다.
64비트 ARM 및 64비트 PowerPC 시스템의 벤치마크 결과, 일반적으로 10% 이상의 성능 향상이 나타났습니다.

Go 1.17 릴리스 노트에서 [언급](go1.17#compiler)되었듯이,
이 변경 사항은 안전한(safe) Go 코드의 기능에 영향을 주지 않으며
대부분의 어셈블리 코드에도 영향을 주지 않도록 설계되었습니다. 자세한 내용은
[Go 1.17 릴리스 노트](go1.17#compiler)를 참조하십시오.

<!-- CL 355497, CL 356869 -->
이제 컴파일러가 range 루프나 레이블이 지정된 for 루프를 포함하는 함수를 인라이닝할 수 있습니다.

<!-- CL 298611 -->
새로운 `-asan` 컴파일러 옵션은 새로운 `go` 명령의 `-asan` 옵션을 지원합니다.

<!-- https://golang.org/issue/50954 -->
제네릭(generics)을 지원하기 위해 컴파일러의 타입 체커가 완전히 교체되었으며, 이로 인해 일부 에러 메시지의 문구가 이전과 달라졌을 수 있습니다. 어떤 경우에는 Go 1.18 이전의 에러 메시지가 더 상세하거나 더 도움이 되는 방식으로 표현되었습니다.
저희는 Go 1.19에서 이러한 사례들을 해결할 계획입니다.

<!-- /issue/49569 -->
제네릭 지원과 관련된 컴파일러의 변경 사항으로 인해, Go 1.18의 컴파일 속도가 Go 1.17보다 약 15% 더 느려질 수 있습니다. 컴파일된 코드의 실행 시간은 영향을 받지 않습니다. 향후 릴리스에서 컴파일러의 속도를 개선할 계획입니다.

## Linker {#linker}

링커가 [훨씬 더 적은 재배치(relocations)](https://tailscale.com/blog/go-linker/)를 생성합니다.
그 결과, 대부분의 코드베이스에서 링크 속도가 빨라지고, 링크에 필요한 메모리가 줄어들며, 더 작은 바이너리가 생성됩니다.
Go 바이너리를 처리하는 도구는 Go 1.18의 `debug/gosym` 패키지를 사용하여 이전 및 최신 바이너리를 모두 투명하게 처리해야 합니다.

<!-- CL 298610 -->
새로운 `-asan` 링커 옵션은 새로운 `go` 커맨드의 `-asan` 옵션을 지원합니다.

## Bootstrap {#bootstrap}

<!-- CL 369914, CL 370274 -->
소스에서 Go 릴리스를 빌드할 때 `GOROOT_BOOTSTRAP`이 설정되어 있지 않으면, 이전 버전의 Go는 `$HOME/go1.4`(`Windows의 경우 %HOMEDRIVE%%HOMEPATH%\go1.4`) 디렉토리에서 Go 1.4 이상의 부트스트랩 툴체인을 찾았습니다.
이제 Go는 `$HOME/go1.4`로 돌아가기 전에 먼저 `$HOME/go1.17` 또는 `$HOME/sdk/go1.17`을 찾습니다.
우리는 Go 1.19부터 부트스트랩을 위해 Go 1.17 이상이 필요하도록 할 계획이며, 이번 변경 사항은 그 전환을 더 원활하게 만들어 줄 것입니다.
자세한 내용은 [go.dev/issue/44505](/issue/44505)를 참조하십시오.

## 표준 라이브러리 {#library}

### 새로운 `debug/buildinfo` 패키지 {#debug_buildinfo}

<!-- golang.org/issue/39301 -->
새로운 [`debug/buildinfo`](/pkg/debug/buildinfo) 패키지는 `go` 명령어로 빌드된 실행 파일에 내장된 모듈 버전, 버전 관리 정보 및 빌드 플래그에 대한 액세스를 제공합니다.
동일한 정보는 현재 실행 중인 바이너리의 경우 [`runtime/debug.ReadBuildInfo`](/pkg/runtime/debug#ReadBuildInfo)를 통해, 커맨드 라인에서는 `go` `version` `-m`을 통해 확인할 수 있습니다.

### 새로운 `net/netip` 패키지 {#netip}

새로운 [`net/netip`](/pkg/net/netip/) 패키지는 새로운 IP 주소 타입인 [`Addr`](/pkg/net/netip/#Addr)를 정의합니다. 기존의 [`net.IP`](/pkg/net/#IP) 타입과 비교하여, `netip.Addr` 타입은 메모리를 더 적게 사용하고, 불변(immutable)이며, 비교 가능하므로 `==` 연산자를 지원하고 맵(map)의 키로 사용할 수 있습니다.

`Addr` 외에도, 이 패키지는 IP와 포트를 나타내는 [`AddrPort`](/pkg/net/netip/#AddrPort)와 네트워크 CIDR 프리픽스를 나타내는 [`Prefix`](/pkg/net/netip/#Prefix)를 정의합니다.

이 패키지는 또한 이러한 새로운 타입들을 생성하고 조사하기 위한 여러 함수를 정의합니다:
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

[`net`](/pkg/net/) 패키지에는 기존 메서드와 병렬로 작동하는 새로운 메서드들이 추가되었습니다. 이 메서드들은 상대적으로 무거운 [`net.IP`](/pkg/net/#IP)나 [`*net.UDPAddr`](/pkg/net/#UDPAddr) 타입 대신 `netip.AddrPort`를 반환합니다:
[`Resolver.LookupNetIP`](/pkg/net/#Resolver.LookupNetIP),
[`UDPConn.ReadFromUDPAddrPort`](/pkg/net/#UDPConn.ReadFromUDPAddrPort),
[`UDPConn.ReadMsgUDPAddrPort`](/pkg/net/#UDPConn.ReadMsgUDPAddrPort),
[`UDPConn.WriteToUDPAddrPort`](/pkg/net/#UDPConn.WriteToUDPAddrPort),
[`UDPConn.WriteMsgUDPAddrPort`](/pkg/net/#UDPConn.WriteMsgUDPAddrPort).
새로운 `UDPConn` 메서드들은 할당 없는(allocation-free) I/O를 지원합니다.

`net` 패키지에는 이제 기존의 [`TCPAddr`](/pkg/net/#TCPAddr)/[`UDPAddr`](/pkg/net/#UDPAddr) 타입과 `netip.AddrPort` 간의 변환을 위한 함수와 메서드들이 포함되었습니다: [`TCPAddrFromAddrPort`](/pkg/net/#TCPAddrFromAddrPort), [`UDPAddrFromAddrPort`](/pkg/net/#UDPAddrFromAddrPort), [`TCPAddr.AddrPort`](/pkg/net/#TCPAddr.AddrPort), [`UDPAddr.AddrPort`](/pkg/net/#UDPAddr.AddrPort).

### 클라이언트 측에서 기본적으로 TLS 1.0 및 1.1 비활성화 {#tls10}

<!-- CL 359779, golang.org/issue/45428 -->
[`Config.MinVersion`](/pkg/crypto/tls/#Config.MinVersion)이 설정되지 않은 경우, 이제 클라이언트 연결에 대해 TLS 1.2가 기본값으로 적용됩니다. 안전하게 최신 상태를 유지하는 서버라면 TLS 1.2를 지원할 것으로 예상되며, 브라우저들은 2020년부터 이를 필수로 요구해 왔습니다. `Config.MinVersion`을 `VersionTLS10`으로 설정하면 TLS 1.0 및 1.1을 여전히 지원합니다.
서버 측 기본값은 TLS 1.0으로 변경되지 않고 유지됩니다.

`GODEBUG=tls10default=1` 환경 변수를 설정하여 기본 설정을 일시적으로 TLS 1.0으로 되돌릴 수 있습니다.
이 옵션은 Go 1.19에서 제거될 예정입니다.

### SHA-1 인증서 거부 {#sha1}

<!-- CL 359777, golang.org/issue/41682 -->
`crypto/x509`는 이제 SHA-1 해시 함수로 서명된 인증서를 거부합니다. 이는 자체 서명된 루트 인증서에는 적용되지 않습니다. SHA-1에 대한 실제 공격은 [2017년부터 입증되었으며](https://shattered.io/), 공인 인증 기관(CA)들은 2015년부터 SHA-1 인증서를 발행하지 않았습니다.

이는 `GODEBUG=x509sha1=1` 환경 변수를 설정하여 일시적으로 되돌릴 수 있습니다.
이 옵션은 향후 릴리스에서 제거될 예정입니다.

### 라이브러리의 소소한 변경 사항 {#minor_library_changes}

언제나 그렇듯, Go 1의 [호환성 약속](/doc/go1compat)을 염두에 두고 라이브러리에 다양한 소규모 변경 및 업데이트가 이루어졌습니다.

#### [bufio](/pkg/bufio/)

<!-- CL 345569 -->
새로운 [`Writer.AvailableBuffer`](/pkg/bufio#Writer.AvailableBuffer) 메서드는 append 방식의 API에서 사용할 수 있도록, 비어 있지만 용량(capacity)은 0이 아닐 수 있는 버퍼를 반환합니다. 데이터를 append한 후, 해당 버퍼를 이어지는 `Write` 호출에 제공함으로써 복사 과정을 생략할 수 있습니다.

<!-- CL 345570 -->
[`Reader.Reset`](/pkg/bufio#Reader.Reset) 및
[`Writer.Reset`](/pkg/bufio#Writer.Reset) 메서드가
이제 버퍼가 `nil`인 객체에서 호출될 때 기본 버퍼 크기를 사용합니다.

<!-- bufio -->

#### [bytes](/pkg/bytes/)

<!-- CL 351710 -->
새로운 [`Cut`](/pkg/bytes/#Cut) 함수는 구분자를 기준으로 `[]byte`를 슬라이싱합니다. 이 함수는 [`Index`](/pkg/bytes/#Index), [`IndexByte`](/pkg/bytes/#IndexByte), [`IndexRune`](/pkg/bytes/#IndexRune), 그리고 [`SplitN`](/pkg/bytes/#SplitN)의 많은 일반적인 사용 사례를 대체하고 단순화할 수 있습니다.

<!-- CL 323318, CL 332771 -->
[`Trim`](/pkg/bytes/#Trim), [`TrimLeft`](/pkg/bytes/#TrimLeft),
및 [`TrimRight`](/pkg/bytes/#TrimRight)는 이제 할당(allocation)이 발생하지 않으며, 특히 작은 ASCII 컷셋(cutset)의 경우 최대 10배 더 빨라졌습니다.

<!-- CL 359485 -->
[`Title`](/pkg/bytes/#Title) 함수는 이제 사용되지 않습니다(deprecated). 이 함수는 유니코드 문장 부호와 언어별 대문자 변환 규칙을 처리하지 못하며, [golang.org/x/text/cases](https://golang.org/x/text/cases) 패키지로 대체되었습니다.

<!-- bytes -->

#### [crypto/elliptic](/pkg/crypto/elliptic/)

<!-- CL 320071, CL 320072, CL 320074, CL 361402, CL 360014 -->
[`P224`](/pkg/crypto/elliptic#P224),
[`P384`](/pkg/crypto/elliptic#P384), 및
[`P521`](/pkg/crypto/elliptic#P521) 곡선
구현은 이제 모두 [addchain](https://github.com/mmcloughlin/addchain) 및
[fiat-crypto](https://github.com/mit-plv/fiat-crypto)
프로젝트에서 생성된 코드를 기반으로 하며, 후자는 산술 연산의 형식 검증된 모델을 기반으로 합니다. 이제 더 안전한 완전 공식(complete formulas)과 내부 API를 사용합니다. P-224와 P-384는 이제 약 4배 더 빨라졌습니다. 모든 특정 곡선 구현은 이제 상수 시간(constant-time)으로 동작합니다.

유효하지 않은 곡선 점(`IsOnCurve` 메서드가 `false`를 반환하며, [`Unmarshal`](/pkg/crypto/elliptic#Unmarshal)이나 유효한 점을 대상으로 하는 `Curve` 메서드에 의해 절대 반환되지 않는 점)을 대상으로 하는 연산은 항상 정의되지 않은 동작(undefined behavior)이었으며, 키 복구 공격으로 이어질 수 있고, 이제 새로운 백엔드에서는 지원되지 않습니다. `P224`, `P384` 또는 `P521` 메서드에 유효하지 않은 점이 전달되면, 해당 메서드는 이제 무작위 점을 반환합니다. 이 동작은 향후 릴리스에서 명시적인 패닉(panic)으로 변경될 수 있습니다.

<!-- crypto/elliptic -->

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 325250 -->
새로운 [`Conn.NetConn`](/pkg/crypto/tls/#Conn.NetConn)
메서드를 통해 기본 [`net.Conn`](/pkg/net#Conn)에
접근할 수 있습니다.

<!-- crypto/tls -->

#### [crypto/x509](/pkg/crypto/x509)

<!-- CL 353132, CL 353403 -->
[`Certificate.Verify`](/pkg/crypto/x509/#Certificate.Verify)는 이제
[`VerifyOpts.Roots`](/pkg/crypto/x509/#VerifyOpts.Roots)가 nil로 전달되거나
[`SystemCertPool`](/pkg/crypto/x509/#SystemCertPool)에서 반환된 루트 풀을 사용할 때, macOS 및 iOS에서 인증서 유효성을 검증하기 위해 플랫폼 API를 사용합니다.

<!-- CL 353589 -->
[`SystemCertPool`](/pkg/crypto/x509/#SystemCertPool)을 이제 Windows에서 사용할 수 있습니다.

Windows, macOS 및 iOS에서 [`SystemCertPool`](/pkg/crypto/x509/#SystemCertPool)에 의해 반환된 [`CertPool`](/pkg/crypto/x509/#CertPool)에 추가 인증서가 추가된 경우, [`Certificate.Verify`](/pkg/crypto/x509/#Certificate.Verify)는 두 번의 검증을 수행합니다. 하나는 플랫폼 검증기 API와 시스템 루트를 사용하는 것이고, 다른 하나는 Go 검증기와 추가된 루트를 사용하는 것입니다. 플랫폼 검증기 API에 의해 반환된 체인이 우선권을 가집니다.

[`CertPool.Subjects`](/pkg/crypto/x509/#CertPool.Subjects)
는 더 이상 권장되지 않습니다(deprecated). Windows, macOS 및 iOS에서
[`SystemCertPool`](/pkg/crypto/x509/#SystemCertPool)
에 의해 반환되는 [`CertPool`](/pkg/crypto/x509/#CertPool)
은 `Subjects`가 반환하는 슬라이스에 시스템 루트를 포함하지 않는 풀을 반환합니다. 이는 정적 리스트가 플랫폼 정책을 적절하게 표현할 수 없으며, 플랫폼 API에서 아예 제공되지 않을 수도 있기 때문입니다.

MD5 해시(`MD5WithRSA`)에 의존하는 서명 알고리즘을 사용한 인증서 서명 지원이 Go 1.19에서 제거될 수 있습니다.

#### [debug/dwarf](/pkg/debug/dwarf/)

<!-- CL 380714 -->
[`StructField`](/pkg/debug/dwarf#StructField)
및 [`BasicType`](/pkg/debug/dwarf#BasicType)
구조체에 이제 모두 `DataBitOffset` 필드가 추가되었습니다. 이 필드는 `DW_AT_data_bit_offset`
속성이 존재하는 경우 해당 값을 보유합니다.

#### [debug/elf](/pkg/debug/elf/)

<!-- CL 352829 -->
[`R_PPC64_RELATIVE`](/pkg/debug/elf/#R_PPC64_RELATIVE)
상수가 추가되었습니다.

<!-- debug/elf -->

#### [debug/plan9obj](/pkg/debug/plan9obj/)

<!-- CL 350229 -->
이제 [File.Symbols](/pkg/debug/plan9obj#File.Symbols)
메서드는 파일에 심볼 섹션이 없는 경우 새롭게 내보내진(exported) 에러 값인 [ErrNoSymbols](/pkg/debug/plan9obj#ErrNoSymbols)를 반환합니다.

<!-- debug/plan9obj -->

#### [embed](/pkg/embed/)

<!-- CL 359413 -->
이제 [`go:embed`](/pkg/embed#hdr-Directives)
지시문이 `all:`로 시작하여 이름이 점(`.`)이나 언더스코어(`_`)로 시작하는 파일을 포함할 수 있습니다.

<!-- debug/plan9obj -->

#### [go/ast](/pkg/go/ast/)

<!-- https://golang.org/issue/47781, CL 325689, CL 327149, CL 348375, CL 348609 -->
다음 제안서에 따라
[
Additions to go/ast and go/token to support parameterized functions and types
](https://go.googlesource.com/proposal/+/master/design/47781-parameterized-go-ast.md)
[`go/ast`](/pkg/go/ast) 패키지에 다음과 같은 사항들이 추가되었습니다:

- [`FuncType`](/pkg/go/ast/#FuncType) 및 [`TypeSpec`](/pkg/go/ast/#TypeSpec) 노드에는 타입 파라미터가 있을 경우 이를 저장하기 위한 새로운 필드 `TypeParams`가 추가되었습니다.
  - 새로운 표현식 노드인 [`IndexListExpr`](/pkg/go/ast/#IndexListExpr)는 여러 개의 인덱스를 가진 인덱스 표현식을 나타내며, 두 개 이상의 명시적 타입 인자를 사용하는 함수 및 타입 인스턴스화에 사용됩니다.

#### [go/constant](/pkg/go/constant/)

<!-- https://golang.org/issue/46211, CL 320491 -->
새로운 [`Kind.String`](/pkg/go/constant/#Kind.String)
메서드는 리시버 kind에 대해 사람이 읽을 수 있는 이름을 반환합니다.

#### [go/token](/pkg/go/token/)

<!-- https://golang.org/issue/47781, CL 324992 -->
새로운 상수 [`TILDE`](/pkg/go/token/#TILDE)는 제안서 [Additions to go/ast and go/token to support parameterized functions and types](https://go.googlesource.com/proposal/+/master/design/47781-parameterized-go-ast.md)에 따라 `~` 토큰을 나타냅니다.

#### [go/types](/pkg/go/types/)

<!-- https://golang.org/issue/46648 -->
새로운 [`Config.GoVersion`](/pkg/go/types/#Config.GoVersion)
필드는 허용되는 Go 언어 버전을 설정합니다.

<!-- https://golang.org/issue/47916 -->
다음 제안서에 따라
[
Additions to go/types to support type parameters
](https://go.googlesource.com/proposal/+/master/design/47916-parameterized-go-types.md)
[`go/types`](/pkg/go/types) 패키지에 다음과 같은 사항들이 추가되었습니다:

- 타입 파라미터를 표현하기 위해 새로운 타입 [`TypeParam`](/pkg/go/types/#TypeParam), 팩토리 함수 [`NewTypeParam`](/pkg/go/types/#NewTypeParam) 및 관련 메서드들이 추가되었습니다.
  - 새로운 타입 [`TypeParamList`](/pkg/go/types/#TypeParamList)는 타입 파라미터 목록을 보유합니다.
  - 새로운 타입 [`TypeList`](/pkg/go/types/#TypeList)는 타입 목록을 보유합니다.
  - 새로운 팩토리 함수 [`NewSignatureType`](/pkg/go/types/#NewSignatureType)는 (리시버 또는 함수) 타입 파라미터를 가진 [`Signature`](/pkg/go/types/#Signature)를 할당합니다. 이러한 타입 파라미터에 접근하기 위해 `Signature` 타입에 [`Signature.RecvTypeParams`](/pkg/go/types/#Signature.RecvTypeParams)와 [`Signature.TypeParams`](/pkg/go/types/#Signature.TypeParams)라는 두 가지 새로운 메서드가 추가되었습니다.
  - [`Named`](/pkg/go/types/#Named) 타입에 네 가지 새로운 메서드가 추가되었습니다: 인스턴스화된 타입의 원본 파라미터화된 타입을 가져오는 [`Named.Origin`](/pkg/go/types/#Named.Origin), 인스턴스화되었거나 파라미터화된 타입의 타입 인자 또는 타입 파라미터를 가져오는 [`Named.TypeArgs`](/pkg/go/types/#Named.TypeArgs) 및 [`Named.TypeParams`](/pkg/go/types/#Named.TypeParams), 그리고 타입 파라미터를 설정하는 [`Named.SetTypeParams`](/pkg/go/types/#Named.TypeParams) (예: 명명된 타입을 임포트할 때, 가능한 순환 참조로 인해 명명된 타입의 할당과 타입 파라미터 설정이 동시에 이루어질 수 없는 경우)입니다.
  - [`Interface`](/pkg/go/types/#Interface) 타입에 네 가지 새로운 메서드가 추가되었습니다: 인터페이스에 의해 정의된 타입 세트의 속성을 쿼리하는 [`Interface.IsComparable`](/pkg/go/types/#Interface.IsComparable) 및 [`Interface.IsMethodSet`](/pkg/go/types/#Interface.IsMethodSet), 그리고 인터페이스가 타입 제약 리터럴 주변의 암시적 인터페이스인지 설정하고 테스트하는 [`Interface.MarkImplicit`](/pkg/go/types/#Interface.MarkImplicit) 및 [`Interface.IsImplicit`](/pkg/go/types/#Interface.IsImplicit)입니다.
  - 인터페이스 내의 타입 세트를 표현하기 위해 새로운 타입 [`Union`](/pkg/go/types/#Union) 및 [`Term`](/pkg/go/types/#Term), 팩토리 함수 [`NewUnion`](/pkg/go/types/#NewUnion) 및 [`NewTerm`](/pkg/go/types/#NewTerm), 그리고 관련 메서드들이 추가되었습니다.
  - 새로운 함수 [`Instantiate`](/pkg/go/types/#Instantiate)는 파라미터화된 타입을 인스턴스화합니다.
  - 새로운 [`Info.Instances`](/pkg/go/types/#Info.Instances) 맵은 새로운 [`Instance`](/pkg/go/types/#Instance) 타입을 통해 함수 및 타입 인스턴스화를 기록합니다.
  - <!-- CL 342671 -->
    타입 인자와 관련된 에러를 표현하기 위해 새로운 타입 [`ArgumentError`](/pkg/go/types/#ArgumentError) 및 관련 메서드들이 추가되었습니다.
  - <!-- CL 353089 -->
    새로운 [`Config.Context`](/pkg/go/types/#Config.Context) 필드를 통해 타입 체크된 패키지 간에 동일한 타입 인스턴스를 공유하기 쉽도록 새로운 타입 [`Context`](/pkg/go/types/#Context)와 팩토리 함수 [`NewContext`](/pkg/go/types/#NewContext)가 추가되었습니다.

[`AssignableTo`](/pkg/go/types/#AssignableTo),
[`ConvertibleTo`](/pkg/go/types/#ConvertibleTo),
[`Implements`](/pkg/go/types/#Implements),
[`Identical`](/pkg/go/types/#Identical),
[`IdenticalIgnoreTags`](/pkg/go/types/#IdenticalIgnoreTags), 그리고
[`AssertableTo`](/pkg/go/types/#AssertableTo)
술어들이 이제 일반화된 인터페이스(generalized interfaces), 즉 Go 코드에서 타입 제약(type constraints)으로만 사용될 수 있는 인터페이스이거나 이를 포함하는 인자들과도 함께 작동합니다.
`AssignableTo`,
`ConvertibleTo`, `Implements`, 그리고
`AssertableTo`의 동작은 인자가
인스턴스화되지 않은 제네릭 타입(uninstantiated generic types)일 때 정의되지 않으며, `AssertableTo`는
첫 번째 인자가 일반화된 인터페이스인 경우 정의되지 않음에 유의하십시오.

#### [html/template](/pkg/html/template/)

<!-- CL 321491 -->
`range` 파이프라인 내에서 새로운 `{{break}}` 명령은 루프를 조기에 종료하며, 새로운 `{{continue}}` 명령은 즉시 다음 루프 반복을 시작합니다.

<!-- CL 321490 -->
`and` 함수는 더 이상 항상 모든 인자를 평가하지 않습니다. 거짓(false)으로 평가되는 첫 번째 인자를 만난 후에는 인자 평가를 중단합니다. 마찬가지로, `or` 함수는 이제 참(true)으로 평가되는 첫 번째 인자를 만난 후에 인자 평가를 중단합니다. 이는 인자 중 함수 호출이 포함되어 있을 때 차이를 만듭니다.

<!-- html/template -->

#### [image/draw](/pkg/image/draw/)

<!-- CL 340049 -->
인수가 가장 일반적인 이미지 타입이 아닐 때 사용되는 `Draw` 및 `DrawMask` 폴백(fallback) 구현이, 해당 인수가 Go 1.17에서 추가된 선택적 [`draw.RGBA64Image`](/pkg/image/draw/#RGBA64Image) 및 [`image.RGBA64Image`](/pkg/image/#RGBA64Image) 인터페이스를 구현하는 경우 이제 더 빠르게 동작합니다.

<!-- image/draw -->

#### [net](/pkg/net/)

<!-- CL 340261 -->
[`net.Error.Temporary`](/pkg/net#Error)가 deprecated되었습니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- CL 330852 -->
WebAssembly 타겟에서, [`Transport`](/pkg/net/http/#Transport)의 `Dial`, `DialContext`,
`DialTLS` 및 `DialTLSContext` 메서드 필드가 지정된 경우, 이제 HTTP 요청을 만드는 데 올바르게 사용됩니다.

<!-- CL 338590 -->
새로운
[`Cookie.Valid`](/pkg/net/http#Cookie.Valid)
메서드는 쿠키가 유효한지 여부를 보고합니다.

<!-- CL 346569 -->
새로운
[`MaxBytesHandler`](/pkg/net/http#MaxBytesHandler)
함수는 `ResponseWriter`와 `Request.Body`를
[`MaxBytesReader`](/pkg/net/http#MaxBytesReader)로 래핑하는 `Handler`를 생성합니다.

<!-- CL 359634, CL 360381, CL 362735 -->
비 ASCII 문자가 포함된 도메인 이름을 조회할 때, Unicode-to-ASCII 변환이 이제 [Unicode IDNA Compatibility Processing](https://unicode.org/reports/tr46/) 표준(UTS #46)에 정의된 Nontransitional Processing에 따라 수행됩니다. ß, ς, 제로 폭 결합자(zero-width joiner) U+200D, 제로 폭 비결합자(zero-width non-joiner) U+200C 등 네 가지 서로 다른 룬(rune)의 해석이 변경되었습니다. Nontransitional Processing은 대부분의 애플리케이션 및 웹 브라우저와 일관되게 동작합니다.

<!-- net/http -->

#### [os/user](/pkg/os/user/)

<!-- CL 330753 -->
[`User.GroupIds`](/pkg/os/user#User.GroupIds)는 이제 cgo를 사용할 수 없는 경우 Go 네이티브 구현을 사용합니다.

<!-- os/user -->

#### [reflect](/pkg/reflect/)

<!-- CL 356049, CL 320929 -->
새로운
[`Value.SetIterKey`](/pkg/reflect/#Value.SetIterKey)
및 [`Value.SetIterValue`](/pkg/reflect/#Value.SetIterValue)
메서드는 맵 반복자(map iterator)를 소스로 사용하여 Value를 설정합니다. 이 메서드들은
`Value.Set(iter.Key())` 및 `Value.Set(iter.Value())`와 동일하게 동작하지만,
할당(allocation) 횟수가 더 적습니다.

<!-- CL 350691 -->
새로운 [`Value.UnsafePointer`](/pkg/reflect/#Value.UnsafePointer) 메서드는 Value의 값을 [`unsafe.Pointer`](/pkg/unsafe/#Pointer)로 반환합니다. 이를 통해 호출자는 [`Value.UnsafeAddr`](/pkg/reflect/#Value.UnsafeAddr) 및 [`Value.Pointer`](/pkg/reflect/#Value.Pointer)에서 마이그레이션하여, 호출 측에서 (unsafe.Pointer 규칙에 따라 필요한) uintptr에서 unsafe.Pointer로의 변환을 수행할 필요를 없앨 수 있습니다.

<!-- CL 321891 -->
새로운 [`MapIter.Reset`](/pkg/reflect/#MapIter.Reset) 메서드는 리시버를 변경하여 다른 맵을 반복하도록 합니다. [`MapIter.Reset`](/pkg/reflect/#MapIter.Reset)을 사용하면 여러 맵에 대해 할당 없이(allocation-free) 반복 작업을 수행할 수 있습니다.

<!-- CL 352131 -->
변환이 안전한지 테스트하기 위해 [`Value`](/pkg/reflect#Value)에 여러 메서드(
[`Value.CanInt`](/pkg/reflect#Value.CanInt),
[`Value.CanUint`](/pkg/reflect#Value.CanUint),
[`Value.CanFloat`](/pkg/reflect#Value.CanFloat),
[`Value.CanComplex`](/pkg/reflect#Value.CanComplex)
)가 추가되었습니다.

<!-- CL 357962 -->
[`Value.FieldByIndex`](/pkg/reflect#Value.FieldByIndex)에서 임베디드 구조체(embedded struct)의 nil 포인터를 거쳐 접근할 때 발생하는 패닉을 방지하기 위해 [`Value.FieldByIndexErr`](/pkg/reflect#Value.FieldByIndexErr)가 추가되었습니다.

<!-- CL 341333 -->
[`reflect.Ptr`](/pkg/reflect#Ptr) 및
[`reflect.PtrTo`](/pkg/reflect#PtrTo)가
`reflect` 패키지의 다른 부분과의 일관성을 위해
각각 [`reflect.Pointer`](/pkg/reflect#Pointer) 및
[`reflect.PointerTo`](/pkg/reflect#PointerTo)로 이름이 변경되었습니다.
기존 이름도 계속 작동하지만, 향후 Go 릴리스에서 deprecated 될 예정입니다.

<!-- reflect -->

#### [regexp](/pkg/regexp/)

<!-- CL 354569 -->
[`regexp`](/pkg/regexp/)
이제 UTF-8 문자열의 각 잘못된 바이트를 `U+FFFD`로 처리합니다.

<!-- regexp -->

#### [runtime/debug](/pkg/runtime/debug/)

<!-- CL 354569 -->
[`BuildInfo`](/pkg/runtime/debug#BuildInfo)
구조체에 바이너리가 어떻게 빌드되었는지에 대한 추가 정보를 포함하는 두 개의 새로운 필드가 추가되었습니다:

- [`GoVersion`](/pkg/runtime/debug#BuildInfo.GoVersion)
    바이너리를 빌드하는 데 사용된 Go 버전을 보유합니다.
  - [`Settings`](/pkg/runtime/debug#BuildInfo.Settings)
    빌드를 설명하는 키/값 쌍을 보유하는 [`BuildSettings`](/pkg/runtime/debug#BuildSettings) 구조체의 슬라이스입니다.

<!-- runtime/debug -->

#### [runtime/pprof](/pkg/runtime/pprof/)

<!-- CL 324129 -->
이제 CPU 프로파일러가 Linux에서 스레드별 타이머를 사용합니다. 이를 통해 프로파일이 관찰할 수 있는 최대 CPU 사용량이 증가하고, 일부 형태의 편향(bias)이 감소합니다.

<!-- runtime/pprof -->

#### [strconv](/pkg/strconv/)

<!-- CL 343877 -->
[`strconv.Unquote`](/pkg/strconv/#strconv.Unquote)가
이제 유니코드 서로게이트 하프(Unicode surrogate halves)를 거부합니다.

<!-- strconv -->

#### [strings](/pkg/strings/)

<!-- CL 351710 -->
새로운 [`Cut`](/pkg/strings/#Cut) 함수는
구분자를 기준으로 `string`을 슬라이싱합니다. 이 함수는
[`Index`](/pkg/strings/#Index),
[`IndexByte`](/pkg/strings/#IndexByte),
[`IndexRune`](/pkg/strings/#IndexRune),
그리고 [`SplitN`](/pkg/strings/#SplitN)의
많은 일반적인 사용 사례를 대체하고 단순화할 수 있습니다.

<!-- CL 345849 -->
새로운 [`Clone`](/pkg/strings/#Clone) 함수는 입력 `string`을 복사하며, 반환된 복제 `string`이 입력 문자열의 메모리를 참조하지 않도록 합니다.

<!-- CL 323318, CL 332771 -->
[`Trim`](/pkg/strings/#Trim), [`TrimLeft`](/pkg/strings/#TrimLeft),
및 [`TrimRight`](/pkg/strings/#TrimRight)가 이제 할당(allocation)이 발생하지 않으며, 특히 작은 ASCII cutset의 경우 최대 10배 더 빨라졌습니다.

<!-- CL 359485 -->
[`Title`](/pkg/strings/#Title) 함수는 이제 deprecated 되었습니다. 이 함수는 유니코드 문장 부호와 언어별 대문자 변환 규칙을 처리하지 못하며, [golang.org/x/text/cases](https://golang.org/x/text/cases) 패키지로 대체되었습니다.

<!-- strings -->

#### [sync](/pkg/sync/)

<!-- CL 319769 -->
새로운 메서드인
[`Mutex.TryLock`](/pkg/sync#Mutex.TryLock),
[`RWMutex.TryLock`](/pkg/sync#RWMutex.TryLock), 그리고
[`RWMutex.TryRLock`](/pkg/sync#RWMutex.TryRLock)은
현재 락이 잡혀 있지 않은 경우에만 락을 획득합니다.

<!-- sync -->

#### [syscall](/pkg/syscall/)

<!-- CL 336550 -->
임의의 개수만큼 인자를 전달하여 호출할 수 있는 새로운 함수 [`SyscallN`](/pkg/syscall/?GOOS=windows#SyscallN)이 Windows용으로 도입되었습니다. 이에 따라, [`Syscall`](/pkg/syscall/?GOOS=windows#Syscall), [`Syscall6`](/pkg/syscall/?GOOS=windows#Syscall6), [`Syscall9`](/pkg/syscall/?GOOS=windows#Syscall9), [`Syscall12`](/pkg/syscall/?GOOS=windows#Syscall12), [`Syscall15`](/pkg/syscall/?GOOS=windows#Syscall15), [`Syscall18`](/pkg/syscall/?GOOS=windows#Syscall18)은 [`SyscallN`](/pkg/syscall/?GOOS=windows#SyscallN)을 사용하는 방향으로 deprecated 되었습니다.

<!-- CL 355570 -->
이제 FreeBSD에서 [`SysProcAttr.Pdeathsig`](/pkg/syscall/?GOOS=freebsd#SysProcAttr.Pdeathsig)를 지원합니다.

<!-- syscall -->

#### [syscall/js](/pkg/syscall/js/)

<!-- CL 356430 -->
`Wrapper` 인터페이스가 삭제되었습니다.

<!-- syscall/js -->

#### [testing](/pkg/testing/)

<!-- CL 343883 -->
`-run` 및 `-bench` 인자에서 `/`의 우선순위가 높아졌습니다. 기존에는 `A/B|C/D`가 `A/(B|C)/D`로 처리되었으나, 이제는 `(A/B)|(C/D)`로 처리됩니다.

<!-- CL 356669 -->
`-run` 옵션이 어떤 테스트도 선택하지 않는 경우, `-count` 옵션은 무시됩니다. 테스트 함수 자체가 실행될 때마다 실행되는 하위 테스트(subtests) 집합이 변경되는 드문 경우, 이는 기존 테스트의 동작을 변경할 수 있습니다.

<!-- CL 251441 -->
새로운 [`testing.F`](/pkg/testing#F) 타입은 [위에서 설명한 새로운 퍼징 지원](#fuzzing)에 사용됩니다. 또한 이제 테스트에서 커맨드 라인 옵션 `-test.fuzz`, `-test.fuzztime`, `-test.fuzzminimizetime`을 지원합니다.

<!-- testing -->

#### [text/template](/pkg/text/template/)

<!-- CL 321491 -->
`range` 파이프라인 내에서 새로운 `{{break}}` 명령은 루프를 조기에 종료하며, 새로운 `{{continue}}` 명령은 즉시 다음 루프 반복을 시작합니다.

<!-- CL 321490 -->
`and` 함수가 더 이상 항상 모든 인자를 평가하지 않습니다. `false`로 평가되는 첫 번째 인자를 만난 후 평가를 중단합니다. 마찬가지로, `or` 함수는 이제 `true`로 평가되는 첫 번째 인자를 만난 후 평가를 중단합니다. 인자 중에 함수 호출이 포함되어 있는 경우 결과가 달라질 수 있습니다.

<!-- text/template -->

#### [text/template/parse](/pkg/text/template/parse/)

<!-- CL 321491 -->
이 패키지는 새로운 상수 [`NodeBreak`](/pkg/text/template/parse#NodeBreak)와 새로운 타입 [`BreakNode`](/pkg/text/template/parse#BreakNode)를 통해 [text/template](/pkg/text/template/) 및 [html/template](/pkg/html/template/)의 새로운 `{{break}}` 명령어를 지원하며, 마찬가지로 새로운 상수 [`NodeContinue`](/pkg/text/template/parse#NodeContinue)와 새로운 타입 [`ContinueNode`](/pkg/text/template/parse#ContinueNode)를 통해 새로운 `{{continue}}` 명령어를 지원합니다.

<!-- text/template -->

#### [unicode/utf8](/pkg/unicode/utf8/)

<!-- CL 345571 -->
새로운 [`AppendRune`](/pkg/unicode/utf8/#AppendRune) 함수는 `rune`의 UTF-8 인코딩을 `[]byte`에 추가합니다.

<!-- unicode/utf8 -->
