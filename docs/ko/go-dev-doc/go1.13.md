<!--
참고: 이 문서 및 이 디렉토리에 있는 다른 문서에서, 고정 폭의 단어와 비고정 폭의 공백을 사용하는 규칙을 따릅니다. 예를 들어, `hello world`와 같이 사용합니다.
이러한 표현에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.13 소개 {#introduction}

가장 최신 Go 버전인 1.13은 [Go 1.12](go1.12) 이후 6개월 만에 출시되었습니다.
대부분의 변경 사항은 도구 체인, 런타임, 라이브러리의 구현에 있습니다.
물론, 이번 릴리스는 Go 1의 [호환성 보장](/doc/go1compat.html)을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일 및 실행될 것으로 예상됩니다.

Go 1.13부터, `go` 명령은 기본적으로 Google에서 운영하는 Go 모듈 미러 및 Go 체크섬 데이터베이스를 사용하여 모듈을 다운로드하고 인증합니다. 이러한 서비스 및 관련 정보에 대한 개인 정보 보호 정보는 <https://proxy.golang.org/privacy> 에서 확인할 수 있습니다. 또한 [go 명령 설명서](/cmd/go/#hdr-Module_downloading_and_verification)에서 구성 세부 정보, 특히 이러한 서버를 사용하지 않거나 다른 서버를 사용하는 방법에 대한 내용을 확인할 수 있습니다. 만약 비공개 모듈에 의존하는 경우, [환경을 구성하는 방법에 대한 설명서](/cmd/go/#hdr-Module_configuration_for_non_public_modules)를 참조하십시오.

## 언어 변경 사항 {#language}

```
// Example Go code
package main
```

| Feature | Description |
|---|---|
| `fmt.Println` | Prints to the console |
| `strconv.Atoi` | Converts a string to an integer |

*   This is a list
*   And this is another list item

[숫자 리터럴 제안](https://github.com/golang/proposal/blob/master/design/19308-number-literals.md)에 따라,
Go 1.13은 숫자 리터럴 프리픽스의 보다 일관성 있고 현대적인 세트를 지원합니다.

- [이진 정수 리터럴](/ref/spec#Integer_literals):
    `0b` 또는 `0B` 접두사는 이진 정수 리터럴을 나타냅니다 (예: `0b1011`).
  - [8진 정수 리터럴](/ref/spec#Integer_literals):
    `0o` 또는 `0O` 접두사는 8진 정수 리터럴을 나타냅니다 (예: `0o660`).
    기존 8진 표기법 (앞에 `0`이 오는 8진 숫자)은 유효합니다.
  - [16진 실수 리터럴](/ref/spec#Floating-point_literals):
    `0x` 또는 `0X` 접두사는 16진 형식으로 표현된 부동 소수점 숫자의 지수를 나타낼 수 있습니다 (예: `0x1.0p-1021`).
    16진 부동 소수점 숫자는 항상 지수를 가져야 하며, `p` 또는 `P` 문자와 함께 10진수로 표현됩니다. 지수는 지수의 2승으로 부동 소수점을 스케일링합니다.
  - [허수 리터럴](/ref/spec#Imaginary_literals):
    `i` 허수 접미사는 이제 모든 (이진, 10진, 16진) 정수 또는 실수 리터럴과 함께 사용될 수 있습니다.
  - 숫자 구분 기호:
    숫자 리터럴의 숫자는 밑줄을 사용하여 구분 (그룹화)할 수 있습니다 (예: `1_000_000`, `0b_1010_0110`, 또는 `3.1415_9265`).
    밑줄은 두 숫자 또는 리터럴 접두사와 첫 번째 숫자 사이에 나타날 수 있습니다.

이 [서명된 시프트 카운트 제안](https://github.com/golang/proposal/blob/master/design/19113-signed-shift-counts.md)에 따라
Go 1.13에서는 [시프트 카운트](/ref/spec#Operators)가 반드시 부호 없는 숫자여야 한다는 제약이 제거됩니다. 이 변경 사항은 `<<` 및 `>>` 연산자의 이 (이제 제거된) 제약을 만족시키기 위해 도입된 많은 인위적인 `uint` 변환이 필요하지 않게 만듭니다.

이 언어 변경 사항은 컴파일러의 변경 사항과 함께 구현되었으며, 이에 따라 [`go/scanner`](#go/scanner) 및 [`text/scanner`](#text/scanner) (정수 리터럴), 그리고 [`go/types`](#go/types) (부호 있는 시프트 개수) 라이브러리의 내부 변경 사항이 적용되었습니다.

만약 여러분의 코드가 모듈을 사용하고, `go.mod` 파일이 언어 버전을 지정한 경우,
최소 `1.13`으로 설정하여 이러한 언어 변경 사항에 액세스할 수 있도록 해야 합니다.
이를 `go.mod` 파일을 직접 편집하거나 `go mod edit -go=1.13` 명령을 실행하여 수행할 수 있습니다.

## 포트 {#ports}

Go 1.13은 Native Client (NaCl)에서 실행되는 마지막 릴리스입니다.

<!-- CL 170119, CL 168882 -->
`GOARCH=wasm`인 경우, 새로운 환경 변수 `GOWASM`은 바이너리가 컴파일될 때 포함될 실험적인 기능 목록을 쉼표로 구분하여 지정합니다.
유효한 값은 [여기](/cmd/go/#hdr-Environment_variables)에서 설명되어 있습니다.

### AIX

<!-- CL 164003, CL 169120 -->
AIX on PPC64 (`aix/ppc64`)에서 이제 cgo, 외부 링크, `c-archive` 및 `pie` 빌드 모드를 지원합니다.

### 안드로이드 {#android}

<!-- CL 170127 -->
Go 프로그램은 이제 Android 10과 호환됩니다.

### Darwin
```
{#darwin}
```

[공지](go1.12#darwin)된 바와 같이,
Go 1.13에서는 macOS 10.11 엘 캐피탄 또는 그 이후 버전을 요구합니다;
이전 버전 지원은 중단되었습니다.

### FreeBSD {#freebsd}

[공지](go1.12#freebsd)에 따르면,
Go 1.13에서는 FreeBSD 11.2 이상이 필요합니다;
이전 버전 지원은 중단되었습니다.
FreeBSD 12.0 이상에서는 `COMPAT_FREEBSD11` 옵션이 설정된 커널이 필요합니다 (이것이 기본 설정입니다).

### Illumos {#illumos}

<!-- CL 174457 -->
Go는 이제 `GOOS=illumos`를 통해 Illumos를 지원합니다.
`illumos` 빌드 태그는 `solaris` 빌드 태그를 의미합니다.

### Windows

<!-- CL 178977 -->
내부적으로 링크된 Windows 바이너리에 지정된 Windows 버전이 이제 Windows 7이 NT 4.0가 아닌 것입니다. 이는 Go에 대한 최소 요구 버전이었지만, 역호환성 모드를 사용하는 시스템 호출의 동작에 영향을 줄 수 있습니다. 이제 이러한 호출은 문서화된 대로 동작합니다. 외부적으로 링크된 바이너리(cgo를 사용하는 모든 프로그램)는 항상 더 최신 버전의 Windows를 지정했습니다.

## 도구 {#tools}

### 모듈 {#modules}

#### 환경 변수 {#proxy-vars}

<!-- CL 176580 -->
`[`GO111MODULE`](/cmd/go/#hdr-Module_support)
환경 변수는 계속해서 `auto`로 설정되지만, `auto` 설정은 현재 작업 디렉터리에 `go.mod` 파일이 있거나, `go.mod` 파일이 있는 디렉터리의 하위 디렉터리에 있는 경우, `go` 명령의 모듈 인식 모드를 활성화합니다 – 현재 디렉터리가 `GOPATH/src` 안에 있더라도 마찬가지입니다. 이 변경 사항은 `GOPATH/src` 안에 있는 기존 코드의 마이그레이션을 단순화하고, 모듈 인식 패키지와 함께 모듈 인식 패키지를 유지 관리하는 것을 용이하게 합니다.

<!-- CL 181719 -->
새로운
[`GOPRIVATE`](/cmd/go/#hdr-Module_configuration_for_non_public_modules)
환경 변수는 공개적으로 사용할 수 없는 모듈 경로를 나타냅니다.
이는 더 낮은 수준의 `GONOPROXY` 및 `GONOSUMDB` 변수의 기본값으로 사용되며, 이를 통해 어떤 모듈을 프록시를 통해 가져오고, 체크섬 데이터베이스를 사용하여 검증할지 세밀하게 제어할 수 있습니다.

<!-- CL 173441, CL 177958 -->
`[`GOPROXY`
환경 변수](/cmd/go/#hdr-Module_downloading_and_verification)는 이제 쉼표로 구분된 프록시 URL 목록 또는 특별 토큰 `direct`로 설정할 수 있으며,
기본값은 `https://proxy.golang.org,direct`입니다. 패키지 경로를 해당 모듈로 해결할 때, `go` 명령은 목록의 각 프록시를 순차적으로 사용하여 모든 후보 모듈 경로를 시도합니다. 연결되지 않은 프록시 또는 404 또는 410이 아닌 HTTP 상태 코드는 나머지 프록시를 확인하지 않고 검색을 중단합니다.

새로운
[`GOSUMDB`](/cmd/go/#hdr-Module_authentication_failures)
환경 변수는 checksum을 확인하는 데 사용할 데이터베이스의 이름, 그리고 선택적으로 공개 키 및 서버 URL을 식별합니다. 이는 아직 메인 모듈의 `go.sum` 파일에 없는 모듈의 checksum을 확인하는 데 사용됩니다.
`GOSUMDB`에 명시적인 URL이 포함되어 있지 않으면, URL은 checksum 데이터베이스를 지원하는 엔드포인트를 나타내는 `GOPROXY` URL을 검색하여 선택됩니다. 만약 프록이 이를 지원하지 않으면, 지정된 데이터베이스에 직접 연결됩니다.
`GOSUMDB`를 `off`로 설정하면, checksum 데이터베이스는 사용되지 않고, `go.sum` 파일에 있는 기존 checksum만 확인됩니다.

사용자가 기본 프록시 및 체크섬 데이터베이스(예: 방화벽 또는 격리된 구성으로 인해)에 액세스할 수 없는 경우, `GOPROXY`를 `direct`로, 그리고/또는 `GOSUMDB`를 `off`로 설정하여 사용을 비활성화할 수 있습니다.
[`go` `env` `-w`](#go-env-w)를 사용하면 플랫폼에 관계없이 이러한 변수의 기본값을 설정할 수 있습니다:

```
go env -w GOPROXY=direct
go env -w GOSUMDB=off
```

```go
get
```

<!-- CL 174099 -->
모듈 인식 모드에서,
[`go` `get`](/cmd/go/#hdr-Add_dependencies_to_current_module_and_install_them)
`-u` 플래그를 사용하면 업데이트되는 모듈의 수가 더 작아지고,
`go` `get` `-u` (GOPATH 모드에서)가 업데이트하는 패키지 세트와 더 일관성을 유지합니다.
`go` `get` `-u`는 명령줄에 지정된 모듈과 패키지를 계속 업데이트하지만, 추가적으로 지정된 패키지가 _가져온_ 패키지를 포함하는 모듈만 업데이트합니다.

특히, `go get -u` (추가 인자 없이)는 현재 디렉토리에 있는 패키지의 전이적 가져오기만 업데이트합니다. 대신, 메인 모듈에서 전이적으로 가져온 모든 패키지를 업데이트하려면 `go get -u all`을 사용하십시오.

<!-- CL 177879 -->
위 변경 사항의 결과,
`go get` `-u` 명령어는
`go get` 명령어가 더 이상
`-m` 플래그를 지원하지 않게 되었습니다. 이는 `go get`이 패키지를 로드하기 전에 중단되는 원인이 됩니다. `-d` 플래그는 여전히 지원되며, 지정된 패키지의 종속성을 빌드하는 데 필요한 소스 코드를 다운로드한 후 `go get`이 중단되는 것을 계속 유발합니다.

<!-- CL 177677 -->
기본적으로, 모듈 모드에서 `go get -u`는
테스트 의존성만 업그레이드합니다. 이는 GOPATH 모드와 동일합니다. 이제 `-t` 플래그도 지원하며, (GOPATH 모드와 마찬가지로)
`go get` 명령에 지정된 패키지의 _테스트_에서 가져온 패키지를 포함시킵니다.

<!-- CL 167747 -->
모듈 인식을 모드로 전환하면, `go get` 하위 명령이 이제
버전 접미사 `@patch`를 지원합니다. `@patch` 접미사는 지정된 모듈 또는 지정된 패키스가 포함된 모듈이, 빌드 목록에 있는 버전과 동일한 주요 및 부 버전의 최신 패치 릴리스로 업데이트되어야 함을 나타냅니다.

<!-- CL 184440 -->
만약 `go get` 명령에 전달된 모듈이 버전 접미사가 없는 경우, 이미 최신 릴리스된 버전보다 더 높은 버전에서 요구하는 모듈인 경우, 해당 모듈은 계속해서 더 높은 버전으로 유지됩니다. 이는 `-u` 플래그를 사용하여 모듈 의존성을 지정할 때와 일관성이 있습니다. 이를 통해 사전 릴리스 버전에서 예기치 않은 다운그레이드를 방지할 수 있습니다. 새로운 버전 접미사 `@upgrade`는 명시적으로 이러한 동작을 요청합니다. `@latest`는 현재 버전과 관계없이 항상 최신 버전을 명시적으로 요청합니다.

#### 버전 유효성 검사 {#version-validation}

<!-- CL 181881 -->

버전 관리 시스템에서 모듈을 추출할 때, `go` 명령은 이제 요청된 버전 문자열에 대한 추가적인 유효성 검사를 수행합니다.

`+incompatible` 버전 주석은 [의미론적
임포트 버전 관리](/cmd/go/#hdr-Module_compatibility_and_semantic_versioning) 요구 사항을 우회합니다. 이 주석은 모듈이 도입되기 전에 생성된 저장소에 적용됩니다. `go` 명령은 이러한 버전이 명시적인 `go.mod` 파일을 포함하지 않는지 확인합니다.

`go` 명령어는 이제 [가상 버전](/cmd/go/#hdr-Pseudo_versions)과 버전 관리 메타데이터 간의 매핑을 확인합니다. 구체적으로:

- 버전 접두사는 `vX.0.0` 형식이어야 하거나, 지정된 수정 사항의 조상에 있는 태그에서 파생되거나, 지정된 수정 사항 자체에 [빌드 메타데이터](https://semver.org/#spec-item-10)가 포함된 태그에서 파생되어야 합니다.
  - 날짜 문자열은 수정 사항의 UTC 타임스탬프와 일치해야 합니다.
  - 수정 사항의 짧은 이름은 `go` 명령어가 생성하는 것과 동일한 문자 수를 사용해야 합니다. (예: `git`에서 사용되는 SHA-1 해시의 경우, 12자리 접두사)

만약 [메인 모듈](/cmd/go/#hdr-The_main_module_and_the_build_list)에 있는 `require` 지시문이 유효하지 않은 가상 버전을 사용한다면, 일반적으로 버전을 커밋 해시만으로 변경하고 `go` 명령을 다시 실행하여 수정할 수 있습니다. 예를 들어, `go list -m all` 또는 `go mod tidy`와 같이.

require github.com/docker/docker v1.14.0-0.20190319215453-e7b5f7dbe98c

삭제될 수 있습니다

```go
require github.com/docker/docker e7b5f7dbe98c
```

현재는 다음과 같이 해결됩니다

require github.com/docker/docker v0.7.3-0.20190319215453-e7b5f7dbe98c

만약 메인 모듈의 트랜지티브 의존성이 유효하지 않은 버전 또는 "가상" 버전을 요구하는 경우, 유효한 버전으로 대체할 수 있습니다. 이를 `go.mod` 파일의 메인 모듈 내에서 `[`replace` 지시문](/cmd/go/#hdr-The_go_mod_file)을 사용하여 수행할 수 있습니다. 대체 항목이 커밋 해시인 경우, 위와 같이 적절한 "가상" 버전으로 해결됩니다. 예를 들어,

replace github.com/docker/docker v1.14.0-0.20190319215453-e7b5f7dbe98c => github.com/docker/docker e7b5f7dbe98c

현재 해결됨으로

replace github.com/docker/docker v1.14.0-0.20190319215453-e7b5f7dbe98c => github.com/docker/docker v0.7.3-0.20190319215453-e7b5f7dbe98c

### Go 명령어 {#go-command}

<!-- CL 171137 -->
`go` `env` (/cmd/go/#hdr-Environment_variables)
명령은 이제 `go` 명령에서 인식되는 환경 변수의 사용자별 기본값을 설정하기 위한 `-w` 플래그를 수락하고, 이에 해당하는 `-u` 플래그를 사용하여 이전에 설정된 기본값을 제거할 수 있습니다. `go` `env` `-w`를 통해 설정된 기본값은 `go/env` 파일 내에
[`os.UserConfigDir()`](/pkg/os/#UserConfigDir)에 저장됩니다.

<!-- CL 173343 -->
다음과 같은 [
`go` `버전`](/cmd/go/#hdr-Print_Go_version) 명령이 이제 실행 파일 및 디렉터리의 이름을 지정하는 인수를 허용합니다. 실행 파일에 호출될 때,
`go` `버전`은 실행 파일을 빌드하는 데 사용된 Go 버전 정보를 출력합니다. `-m` 플래그를 사용하면,
`go` `버전`은 사용할 수 있는 경우 실행 파일에 내장된 모듈 버전 정보를 출력합니다. 디렉터리에 호출될 때,
`go` `버전`은 디렉터리와 하위 디렉터리에 포함된 실행 파일에 대한 정보를 출력합니다.

<!-- CL 173345 -->
새로운 [`go`
`build` 플래그](/cmd/go/#hdr-Compile_packages_and_dependencies) `-trimpath`은 컴파일된 실행 파일에서 모든 파일 시스템 경로를 제거하여 빌드 재현성을 개선합니다.

<!-- CL 167679 -->
`-o` 플래그가 `go build`에 전달될 때,
`go` build가 기존 디렉토리를 가리키는 경우,
`go` build는 `main` 패키지의 패키지 인수에 해당하는
실행 파일들을 해당 디렉토리 내에 작성합니다.

<!-- CL 173438 -->
`go` 빌드 플래그 `-tags`가 이제 쉼표로 구분된 빌드 태그 목록을 받도록 변경되었습니다. 이를 통해 [`GOFLAGS`](/cmd/go/#hdr-Environment_variables)에서 여러 태그를 사용할 수 있습니다. 공백으로 구분된 형식은 더 이상 사용되지 않지만 여전히 인식되고 유지됩니다.

<!-- CL 175983 -->
[`go`
`generate`](/cmd/go/#hdr-Generate_Go_files_by_processing_source)가 이제 `generate` 빌드 태그를 설정하여
파일을 검색하기 위한 지시어를 설정하고, 빌드 과정에서는 무시하도록 합니다.

<!-- CL 165746 -->
Go 1.12 릴리스 노트에 발표된 대로, 바이너리 전용 패키지는 더 이상 지원되지 않습니다.
`//go:binary-only-package` 주석으로 표시된 바이너리 전용 패키지를 빌드하면 이제 오류가 발생합니다.

### 컴파일러 도구 체인 {#compiler}

```
# 컴파일러
```

<!-- CL 170448 -->
컴파일러는 더 정확한 방식으로의 새로운 이스케이프 분석 구현을 갖습니다. 대부분의 Go 코드에서는 개선이 있을 것입니다 (즉, 스택 대신 힙에 더 많은 Go 변수와 표현식이 할당됨). 그러나 이러한 정확도 증가는 이전에는 작동했던 잘못된 코드를 깨뜨릴 수도 있습니다 (예: `unsafe.Pointer` 안전 규칙을 위반하는 코드 [pkg/unsafe/#Pointer]). 관련 문제가 발생하는 경우, 이전 이스케이프 분석 단위를 `go build -gcflags=all=-newescape=false`를 사용하여 다시 활성화할 수 있습니다. 이전 이스케이프 분석 사용 옵션은 향후 릴리스에서 제거됩니다.

<!-- CL 161904 -->
컴파일러는 이제 부동 소수점 또는 복소수 상수를 `go_asm.h` 파일에 더 이상 생성하지 않습니다. 이러한 상수는 항상 어셈블리 코드에서 숫자 상수로 사용할 수 없는 형식으로 생성되었습니다.

### 어셈블러 {#assembler}

<!-- CL 157001 -->
어셈블러는 이제 ARM v8.1에 도입된 많은 원자 연산 명령어를 지원합니다.

### gofmt {#gofmt}

`gofmt` (그리고 `go fmt`)는 이제 숫자 리터럴의 접두사와 지수를 소문자로 통일하지만,
헥사데цима리 숫자는 그대로 둡니다. 이렇게 하면 새로운 8진수 접두사(`0O`가 `0o`로 변경됨)를 사용할 때 가독성이 향상됩니다. 그리고 변경 사항은 일관되게 적용됩니다.
`gofmt`는 이제 십진 정수 허상 리터럴에서 불필요한 앞의 0을 제거합니다. (역사적인 호환성을 위해, `0`으로 시작하는 정수 허상 리터럴은 십진수로 간주되며, 8진수로 간주되지 않습니다. 불필요한 앞의 0을 제거하면 잠재적인 혼란을 방지할 수 있습니다.)
예를 들어, `0B1010`, `0XabcDEF`, `0O660`,
`1.2E3` 및 `01i`는 `gofmt`를 적용한 후 `0b1010`, `0xabcDEF`,
`0o660`, `1.2e3` 및 `1i`가 됩니다.

### `godoc` 및 `go` 문서 생성 {#godoc}

<!-- CL 174322 -->
`godoc` 웹 서버는 이제 메인 바이너리 배포본에 포함되어 있지 않습니다.
로컬에서 `godoc` 웹 서버를 실행하려면 먼저 수동으로 설치해야 합니다:

```markdown
go get golang.org/x/tools/cmd/godoc
godoc
```

<!-- CL 177797 -->
`go` `doc` 명령어는 이제 항상 출력에 패키지 절을 포함합니다(예외는 있음). 이전에는 특정 조건에서 패키지 절이 생략되는 것을 막기 위해 휴리스틱이 사용되었습니다.

## 실행 시점 {#runtime}

<!-- CL 161477 -->
범위 초과 오류 메시지가 이제 범위를 벗어난 인덱스와 슬라이스의 길이 (또는 용량)를 포함합니다. 예를 들어, 길이가 1인 슬라이스에서 `s[3]`에 액세스하려고 하면 "실행 오류: 인덱스 [3] 범위 초과, 길이 1"과 같은 오류가 발생합니다.

<!-- CL 171758 -->
이번 릴리스는 `defer` 사용의 대부분의 경우의 성능을 30% 향상시킵니다.

<!-- CL 142960 -->
실행 시간은 이제 운영 체제에 메모리를 더 적극적으로 반환하여, 공동 사용자의 애플리케이션에 사용할 수 있도록 합니다.
이전에는 힙 크기가 증가했을 때 실행 시간이 5분 이상 동안 메모리를 유지했습니다. 이제 힙이 줄어들면 즉시 반환하기 시작합니다. 그러나 Linux를 포함한 많은 운영 체제에서는 운영 체제가 자체적으로 메모리를 느리게 회수하므로, 시스템이 메모리 압박 상태가 될 때까지 프로세스 RSS는 감소하지 않습니다.

## 표준 라이브러리 {#library}

### TLS 1.3 {#tls_1_3}

Go 1.12에서 발표된 바와 같이, Go 1.13은 `crypto/tls` 패키지에 대해 기본적으로 TLS 1.3 지원을 활성화합니다. `GODEBUG` 환경 변수에 `tls13=0` 값을 추가하여 비활성화할 수 있습니다. Go 1.14에서 이 옵트아웃 기능은 제거됩니다.

자세한 내용은 [Go 1.12 릴리스 노트](https://golang.org/doc/go1.12#tls_1_3)를 참조하십시오.

### [crypto/ed25519](/pkg/crypto/ed25519/) {#crypto_ed25519}

<!-- CL 174945, 182698 -->
새로운 [`crypto/ed25519`](/pkg/crypto/ed25519/)
패키지는 Ed25519 서명
스키마를 구현합니다. 이 기능은 이전에는
[`golang.org/x/crypto/ed25519`](https://godoc.org/golang.org/x/crypto/ed25519)
패키지에 의해 제공되었으며, Go 1.13 이상에서 사용될 때
`crypto/ed25519`의 래퍼 역할을 합니다.

### 오류 감싸기 {#error_wrapping}

<!-- CL 163558, 176998 -->
Go 1.13은 [
오류 값 제안](https://go.googlesource.com/proposal/+/master/design/29934-error-values.md)에서 처음 제안되었고, [
관련 이슈](/issue/29934)에서 논의된 오류 래핑 기능을 지원합니다.

오류 `e`는 또 다른 오류 `w`를 감싸서, `Unwrap` 메서드를 제공하여 `w`를 반환할 수 있습니다. `e`와 `w`는 모두 프로그램에서 사용 가능하며, `e`가 `w`에 추가적인 컨텍스트를 제공하거나, `w`를 재해석하는 동시에 프로그램이 `w`를 기반으로 결정을 내릴 수 있도록 합니다.

`fmt.Errorf`를 사용하여 오류를 감싸는 기능을 지원하기 위해, 이제 `%w`
동사를 사용하여 감싸인 오류를 생성할 수 있습니다. 또한 `errors` 패키지(
[`errors.Unwrap`](/pkg/errors/#Unwrap),
[`errors.Is`](/pkg/errors/#Is) 및
[`errors.As`](/pkg/errors/#As))에 세 가지 새로운 함수가 추가되어 감싸인 오류를 감싸고 검사하는 것을 단순화합니다.

자세한 내용은 [`errors` 패키지
문서](/pkg/errors/)를 참조하거나
[Error Value FAQ](/wiki/ErrorValueFAQ)를 참조하십시오.
곧 블로그 게시물도 게시될 예정입니다.

### 라이브러리의 미세 조정 {#minor_library_changes}

물론, 라이브러리에 다양한 미세한 변경 사항 및 업데이트가 있으며, 이는 Go 1의 [호환성 보장](/doc/go1compat)이라는 목표를 염두에 두고 이루어졌습니다.

#### [bytes](/pkg/bytes/)

새로운 [`ToValidUTF8`](/pkg/bytes/#ToValidUTF8) 함수는 주어진 바이트 슬라이스의 복사본을 반환하며, 유효하지 않은 UTF-8 바이트 시퀀스의 각 덩어리를 주어진 슬라이스로 대체합니다.

<!-- 바이트 -->

#### [context]( /pkg/context/)

<!-- CL 169080 -->
`WithValue` 함수에서 반환되는 컨텍스트의 형식이 `fmt`에 의존하지 않으며, 이전과 같이 문자열로 변환되지 않습니다. 정확한 이전 문자열 변환에 의존하는 코드가 영향을 받을 수 있습니다.

<!-- 컨텍스트 -->

#### [crypto/tls](pkg/crypto/tls/)

SSL 버전 3.0 (SSLv3)의 지원은
이제 더 이상 지원되지 않으며 Go 1.14에서 제거될 예정입니다.](/issue/32716)
참고: SSLv3는 TLS보다 이전의
[암호학적으로 취약한](https://tools.ietf.org/html/rfc7568)
프로토콜입니다.

SSLv3는 기본적으로 비활성화되어 있었으며, Go 1.12 이전에는 서버 측에서 실수로 기본 설정으로 활성화되어 있었습니다. 현재 다시 기본적으로 비활성화되었습니다. (SSLv3는 클라이언트 측에서 지원되지 않습니다.)

<!-- CL 177698 -->
Ed25519 인증서가 TLS 버전 1.2 및 1.3에서 지원됩니다.

<!-- crypto/tls -->

#### [crypto/x509](/pkg/crypto/x509/)

<!-- CL 175478 -->
Ed25519 키가 이제 인증서 및 인증서 요청에서 지원됩니다. 이는 [RFC 8410](https://www.rfc-editor.org/info/rfc8410)에 따라, 또한 `ParsePKCS8PrivateKey`, `MarshalPKCS8PrivateKey`, `ParsePKIXPublicKey` 함수를 통해 지원됩니다.

<!-- CL 169238 -->
검색되는 시스템 루트 경로가 이제 `/etc/ssl/cert.pem`를 포함합니다.
이는 Alpine Linux 3.7 이상에서 기본 위치를 지원하기 위함입니다.

<!-- crypto/x509 -->

#### [database/sql](/pkg/database/sql/)

<!-- CL 170699 -->
새로운 `NullTime` 유형은 `time.Time` 유형 중 null 값을 가질 수 있는 것을 나타냅니다.

<!-- CL 174178 -->
새로운 `NullInt32` 유형은 `int32` 유형이며, 값이 null일 수 있습니다.

```markdown
<!-- database/sql -->
```

#### [debug/dwarf](/pkg/debug/dwarf/)

<!-- CL 158797 -->
`Data.Type` ([/pkg/debug/dwarf/#Data.Type](/)
메서드는 타입 그래프 내에서 알려지지 않은 DWARF 태그를 만났을 때 더 이상 오류를 발생시키지 않습니다. 대신, 해당 타입을
`UnsupportedType` ([/pkg/debug/dwarf/#UnsupportedType](/)
객체로 표현합니다.

<!-- 디버깅/다프 -->

#### [errors](/pkg/errors/)

<!-- CL 163558 -->

새로운 함수 [`As`](/pkg/errors/#As)는 주어진 오류의 체인(감겨진 오류의 연속)에서, 주어진 대상의 유형과 일치하는 첫 번째 오류를 찾고, 일치하는 경우 대상 오류를 해당 오류 값으로 설정합니다.

새로운 함수 [`Is`](/pkg/errors/#Is)는 주어진 오류 값이 다른 오류 체인의 오류와 일치하는지 여부를 보고합니다.

새로운 함수 [`Unwrap`](/pkg/errors/#Unwrap)는 주어진 오류에 `Unwrap`을 호출한 결과를 반환합니다.

<!-- 오류 -->

#### [fmt](pkg/fmt/)

<!-- CL 160245 -->

인쇄 동사 `%x` 및 `%X`는 이제 부동 소수점 및 복소수를 각각 소문자와 대문자 형태의 16진수로 형식화합니다.

<!-- CL 160246 -->

새로운 출력 명령어 `%O`는 정수를 8진수로 포맷하고, `0o` 접두사를 사용하여 출력합니다.

<!-- CL 160247 -->

스캐너는 이제 16진수 부동 소수점 값, 숫자 분리용 밑줄, 그리고 선행 `0b` 및 `0o` 접두사를 허용합니다.
자세한 내용은 [언어 변경 사항](#language)를 참조하십시오.

<!-- CL 176998 -->

[`Errorf`](/pkg/fmt/#Errorf) 함수는 새로운 옵션 `%w`를 도입했으며, 이 옵션의 피연산자는 반드시 오류이어야 합니다.
`Errorf`에서 반환되는 오류에는 `Unwrap` 메서드가 포함되며, 이 메서드는 `%w`의 피연산자를 반환합니다.

<!-- fmt -->

#### [go/scanner](pkg/go/scanner/)

<!-- CL 175218 -->
스캐너가 새로운 Go 숫자 리터럴을 인식하도록 업데이트되었습니다. 구체적으로는 다음과 같은 리터럴을 인식합니다.
* 이진 리터럴: `0b`/`0B` 접두사
* 8진 리터럴: `0o`/`0O` 접두사
* 부동 소수점 숫자: 16진수 지수

`i` 접미사는 이제 모든 숫자 리터럴과 함께 사용할 수 있으며, 밑줄은 숫자 그룹을 구분하는 데 사용할 수 있습니다.
자세한 내용은 [언어 변경 사항](#language) 참조.

<!-- go/scanner -->

#### [go/types](/pkg/go/types/)

타입 검사기는 정수 시프트에 대한 새로운 규칙을 따르도록 업데이트되었습니다.
자세한 내용은 [언어 변경 사항](#language)를 참조하십시오.

<!-- go/types -->

#### [html/template](/pkg/html/template/)

<!-- CL 175218 -->
`<script>` 태그를 사용하여 "type" 속성을 "module"로 설정하면, 코드가 이제 [JavaScript 모듈 스크립트](https://html.spec.whatwg.org/multipage/scripting.html#the-script-element:module-script-2)로 해석됩니다.

```markdown
<!-- html/template -->
```

#### [log](/pkg/log/)

<!-- CL 168920 -->
새로운 `Writer` 함수는 표준 로거의 출력 대상을 반환합니다.

<!-- 로그 -->

#### [math/big](/pkg/math/big/)

<!-- CL 160682 -->
새로운 [`Rat.SetUint64`](/pkg/math/big/#Rat.SetUint64) 메서드는 `Rat`을 `uint64` 값으로 설정합니다.

<!-- CL 166157 -->
`Float.Parse`에 대해, `base`가 0인 경우, 숫자를 구분하기 위해 밑줄을 사용할 수 있습니다.
자세한 내용은 [언어 변경 사항](#language)를 참조하십시오.

<!-- CL 166157 -->
`[Int.SetString](pkg/math/big/#Int.SetString)`에서, `base`가 0인 경우, 숫자를 구분하기 위해 각 숫자 사이에 밑줄을 사용할 수 있습니다.
자세한 내용은 [언어 변경 사항](#language)를 참조하십시오.

<!-- CL 168237 -->
[`Rat.SetString`](/pkg/math/big/#Rat.SetString)가 이제 소수점 없는 부동 소수점 표현을 허용합니다.

<!-- 수학/큰 -->

#### [math/bits](/pkg/math/bits/)

<!-- CL 178177 -->
`Add` (‎`/pkg/math/bits/#Add`‎),
`Sub` (‎`/pkg/math/bits/#Sub`‎),
`Mul` (‎`/pkg/math/bits/#Mul`‎),
`RotateLeft` (‎`/pkg/math/bits/#RotateLeft`‎),
및
`ReverseBytes` (‎`/pkg/math/bits/#ReverseBytes`‎) 함수의 실행 시간은 이제 입력에 따라 달라지지 않도록 보장됩니다.

<!-- 수학/비트 -->

#### [net](pkg/net/)

<!-- CL 156366 -->
Unix 시스템에서 `use-vc`가 `resolv.conf`에 설정되어 있는 경우, TCP가 DNS 확인에 사용됩니다.

<!-- CL 170678 -->
새로운 필드 [`ListenConfig.KeepAlive`](/pkg/net/#ListenConfig.KeepAlive)는 리스너가 수신하는 네트워크 연결에 대한 keep-alive 기간을 지정합니다.
이 필드가 0 (기본값)인 경우 TCP keep-alive가 활성화됩니다.
이를 비활성화하려면 음수 값으로 설정합니다.

참고: 연결이 keep-alive 타임아웃으로 닫히면서 I/O에서 반환되는 오류는
`Timeout` 메서드를 가지며, 호출될 경우 `true`를 반환합니다.
이는 keep-alive 오류를 [`SetDeadline`](/pkg/net/#Conn) 및 유사한 메서드로 설정된 마감 시간 지남에 따른 오류와 구별하기 어렵게 만들 수 있습니다.
마감 시간을 사용하고 `Timeout` 메서드 또는 [`os.IsTimeout`](/pkg/os/#IsTimeout)를 사용하여 이를 확인하는 코드는 keep-alive를 비활성화하거나
`errors.Is(syscall.ETIMEDOUT)` (Unix 시스템의 경우)를 사용하여 keep-alive 타임아웃에 대해 `true`를 반환하고 마감 시간 타임아웃에 대해 `false`를 반환하도록 할 수 있습니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- CL 76410 -->
새로운 필드 [`Transport.WriteBufferSize`](/pkg/net/http/#Transport.WriteBufferSize)
과 [`Transport.ReadBufferSize`](/pkg/net/http/#Transport.ReadBufferSize)
을 통해 [`Transport`](/pkg/net/http/#Transport)에 대한 쓰기 및 읽기 버퍼의 크기를 지정할 수 있습니다.
만약 이 중 어느 필드가 0이면, 기본 크기인 4KB가 사용됩니다.

<!-- CL 130256 -->
새로운 필드 [`Transport.ForceAttemptHTTP2`](/pkg/net/http/#Transport.ForceAttemptHTTP2)는 `Dial`, `DialTLS`, 또는 `DialContext` 함수 또는 `TLSClientConfig`가 제공될 때 HTTP/2가 활성화되는지 여부를 제어합니다.

<!-- CL 140357 -->
[`Transport.MaxConnsPerHost`](/pkg/net/http/#Transport.MaxConnsPerHost) 가 이제 올바르게 HTTP/2와 작동합니다.

<!-- CL 154383 -->
[`TimeoutHandler`](/pkg/net/http/#TimeoutHandler)의
[`ResponseWriter`](/pkg/net/http/#ResponseWriter)가 이제
[`Pusher`](/pkg/net/http/#Pusher) 인터페이스를 구현합니다.

<!-- CL 157339 -->
`StatusCode` `103` `"Early Hints"`가 추가되었습니다.

<!-- CL 163599 -->
[`Transport`](/pkg/net/http/#Transport)는 이제 `Request.Body`의
[`io.ReaderFrom`](/pkg/io/#ReaderFrom) 구현을 사용할 수 있도록 하여, 요청 본문을 쓰는 것을 최적화합니다.

<!-- CL 167017 -->
지원되지 않는 전송 인코딩을 접촉하는 경우, [`http.Server`](/pkg/net/http/#Server)는 이제 HTTP 사양 [RFC 7230 섹션 3.3.1](https://tools.ietf.org/html/rfc7230#section-3.3.1)에 따라 "501 Unimplemented" 상태를 반환합니다.

<!-- CL 167681 -->
새로운 `Server` 필드인
`BaseContext` ([/pkg/net/http/#Server.BaseContext]) 및
`ConnContext` ([/pkg/net/http/#Server.ConnContext])
을 통해 요청 및 연결에 전달되는 `Context` 값에 대한 더 세밀한 제어가 가능합니다.

<!-- CL 167781 -->
[`http.DetectContentType`](/pkg/net/http/#DetectContentType)가 이제 RAR 서명을 올바르게 감지할 수 있으며, RAR v5 서명도 감지할 수 있습니다.

<!-- CL 173658 -->
새로운 [`Header`](/pkg/net/http/#Header) 메서드
[`Clone`](/pkg/net/http/#Header.Clone)는 수신 객체의 복사본을 반환합니다.

<!-- CL 174324 -->
새로운 함수 [`NewRequestWithContext`](/pkg/net/http/#NewRequestWithContext)가 추가되었으며, 이 함수는 생성된 모든 [`Request`](/pkg/net/http/#Request)의 전체 수명을 제어하는 [`Context`](/pkg/context/#Context)를 받습니다. 이는 [`Client.Do`](/pkg/net/http/#Client.Do) 및 [`Transport.RoundTrip`](/pkg/net/http/#Transport.RoundTrip)와 함께 사용하기에 적합합니다.

<!-- CL 179457 -->
`Transport`는 이제 서버가 비활성 연결을 "408 Request Timeout" 응답을 사용하여 정상적으로 닫을 때 오류를 기록하지 않습니다.

<!-- net/http -->

#### [os](/pkg/os/)

<!-- CL 160877 -->
새로운 `UserConfigDir` 함수는 사용자별 구성 데이터에 사용할 기본 디렉토리를 반환합니다.

<!-- CL 166578 -->
만약 `File` 객체가 `O_APPEND` 플래그를 사용하여 열리면,
`WriteAt` 메서드는 항상 오류를 반환합니다.

<!-- os -->

#### [os/exec](/pkg/os/exec/)

<!-- CL 174318 -->
Windows에서 `Cmd` 객체의 환경은 부모 프로세스의 `%SYSTEMROOT%` 값을 항상 상속합니다. 단, `Cmd.Env` 필드에 명시적으로 값을 지정하지 않는 한입니다.

<!-- os/exec -->

#### [reflect](/pkg/reflect/)

<!-- CL 171337 -->
새로운 `Value.IsZero` 메서드는 `Value`가 자신의 타입의 0 값인지 여부를 보고합니다.

<!-- CL 174531 -->
`[MakeFunc](https://pkg/reflect/#MakeFunc)` 함수가 반환 값에 대한 할당 변환을 허용하도록 변경되었습니다. 이전에는 정확한 타입 매칭이 필요했지만, 이제는 인터페이스 타입인 반환 값을 실제 구현하는 구체적인 값으로 할당할 수 있습니다.

<!-- 반영 -->

#### [runtime](/pkg/runtime/)

<!-- CL 167780 -->
오류 메시지, [`runtime.Caller`](/pkg/runtime/#Caller) 및 [`runtime.Callers`](/pkg/runtime/#Callers)가 이제 `PKG`의 전역 변수를 초기화하는 함수를
`PKG.init`으로 참조합니다. 이전에는 `PKG.init.ializers`로 참조되었습니다.

<!-- runtime -->

#### [strconv](/pkg/strconv/)

<!-- CL 160243 -->
`strconv.ParseFloat` (/[pkg/strconv/#ParseFloat]),
`strconv.ParseInt` (/[pkg/strconv/#ParseInt]),
그리고 `strconv.ParseUint` (/[pkg/strconv/#ParseUint]),
기본값이 0인 경우, 숫자를 구분하기 위해 괄호 안에 밑줄을 사용할 수 있습니다.
자세한 내용은 [언어 변경 사항](#language)를 참조하십시오.

<!-- strconv -->

#### [strings](pkg/strings/)

<!-- CL 142003 -->
새로운 [`ToValidUTF8`](/pkg/strings/#ToValidUTF8) 함수는 주어진 문자열의 각 유효하지 않은 UTF-8 바이트 시퀀스를 주어진 문자열로 대체하여 복사본을 반환합니다.

<!-- 문자열 -->

#### [sync](/pkg/sync/)

<!-- CL 148958, CL 148959, CL 152697, CL 152698 -->
`Mutex.Lock`의, `Mutex.Unlock`의,
`RWMutex.Lock`의, `RWMutex.Unlock`의,
`Once.Do`의 빠른 경로가 이제 호출자에서 내장되었습니다.
amd64에서 경쟁이 없는 경우에, 이러한 변경 사항은 `Once.Do`를 2배 더 빠르게 만들고,
`Mutex`와 `RWMutex` 메서드를 최대 10% 더 빠르게 만듭니다.

<!-- CL 166960 -->
큰 [`Pool`](/pkg/sync/#Pool)이 더 이상 "스톱 더 월드" 일시 중지 시간을 증가시키지 않습니다.

<!-- CL 166961 -->
`Pool`는 이제 GC 후 완전히 재구성할 필요가 없습니다. 대신, GC 사이에 일부 객체를 유지하며, 모든 객체를 해제하는 대신, `Pool`을 과도하게 사용하는 사용자에게 발생하는 부하 급증을 줄입니다.

<!-- 동기화 -->

#### [syscall](/pkg/syscall/)

<!-- CL 168479 -->
`_getdirentries64` 사용은 Darwin 빌드에서 제거되었으며, 이를 통해 Go 바이너리를 macOS App Store에 업로드할 수 있습니다.

<!-- CL 174197 -->
새로운 `ProcessAttributes` 및 `ThreadAttributes` 필드가 `SysProcAttr` (`/pkg/syscall/?GOOS=windows#SysProcAttr`)에 추가되었으며, Windows에서 새 프로세스를 생성할 때 보안 설정을 노출합니다.

<!-- CL 174320 -->
`EINVAL` 오류가 Windows에서 `Chmod` 모드(`Chmod`)가 0으로 설정되었을 때 더 이상 반환되지 않습니다.

<!-- CL 191337 -->
`Errno` 유형의 값은 `os` 패키지에 있는 오류 값과 비교하여
[`ErrExist`](/pkg/os/#ErrExist)와 같이 테스트할 수 있습니다.
이를 위해 [`errors.Is`](/pkg/errors/#Is)를 사용합니다.

<!-- syscall -->

```
#### [syscall/js](/pkg/syscall/js/)
```

```markdown
<!-- CL 177537 -->
`TypedArrayOf`가 `CopyBytesToGo`([/pkg/syscall/js/#CopyBytesToGo]) 및 `CopyBytesToJS`([/pkg/syscall/js/#CopyBytesToJS])로 대체되었습니다. 이는 바이트 슬라이스와 `Uint8Array` 간에 바이트를 복사하는 데 사용됩니다.
```

<!-- syscall/js -->

#### [테스팅](/pkg/testing/)

<!-- CL 112155 -->
성능 테스트를 실행할 때, [`B.N`](/pkg/testing/#B.N)는 더 이상 반올림되지 않습니다.

<!-- CL 166717 -->
새로운 방법 [`B.ReportMetric`](/pkg/testing/#B.ReportMetric)은 사용자가 사용자 정의 벤치마크 메트릭을 보고 기본 메트릭을 덮어쓸 수 있도록 합니다.

<!-- CL 173722 -->
테스트 플래그는 이제 새 [`Init`](/pkg/testing/#Init) 함수에서 등록됩니다.
이 함수는 생성된 `main` 함수에서 테스트를 실행할 때 호출됩니다.
따라서 테스트 플래그는 이제 테스트 실행 시에만 등록되며, 패키지 초기화 중에 `flag.Parse`를 호출하는 패키지는 테스트 실패를 유발할 수 있습니다.

<!-- 테스트 -->

#### [text/scanner](/pkg/text/scanner/)

<!-- CL 183077 -->
스캐너가 새로운 Go 숫자 리터럴을 인식하도록 업데이트되었습니다. 특히, `0b`/`0B` 접두사를 사용하는 이진 리터럴, `0o`/`0O` 접두사를 사용하는 8진 리터럴, 그리고 16진수 지수를 사용하는 부동 소수점 숫자를 인식합니다.
또한, 새로운 [`AllowDigitSeparators`](/pkg/text/scanner/#AllowDigitSeparators) 모드를 사용하면 숫자 리터럴에 밑줄을 숫자 구분자로 포함할 수 있습니다 (역호환성을 위해 기본적으로 비활성화).
자세한 내용은 [언어 변경 사항](#language)를 참조하십시오.

<!-- text/scanner -->

#### [text/template](https://example.com/pkg/text/template/)

<!-- CL 161762 -->
새로운 [슬라이스 함수](/pkg/text/template/#hdr-Functions)는 다음 인수를 사용하여 첫 번째 인수를 슬라이스합니다.

<!-- text/template -->

#### [time](/pkg/time/)

<!-- CL 122876 -->
연중 날짜가 이제 `[Format](pkg/time/#Time.Format)` 및 `[Parse](pkg/time/#Parse)`에서 지원됩니다.

<!-- CL 167387 -->
새로운 `Duration` 메서드인
[`Microseconds`](/pkg/time/#Duration.Microseconds) 및
[`Milliseconds`](/pkg/time/#Duration.Milliseconds)는 각각의 이름으로 지정된 단위의 정수 개수를 반환합니다.

<!-- 시간 -->

#### [유니코드](/pkg/unicode/)

[`unicode`](/pkg/unicode/) 패키지와 시스템 전반에 걸쳐 제공되는 관련 지원이 Unicode 10.0에서 [Unicode 11.0](https://www.unicode.org/versions/Unicode11.0.0/)로 업그레이드되었습니다.
이는 7개의 새로운 문자 체계 및 66개의 새로운 이모지를 포함하여 총 684개의 새로운 문자를 추가합니다.

<!-- unicode -->
