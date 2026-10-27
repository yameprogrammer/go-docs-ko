<!--
참고: 이 문서 및 이 디렉토리의 다른 문서에서는 `hello` `world`와 같이 가변 폭 공백이 포함된 고정 폭 구문을 설정하는 관습을 따릅니다.
이러한 구문에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

<style>
  main ul li { margin: 0.5em 0; }
</style>

## Go 1.13 소개 {#introduction}

최신 Go 릴리스인 버전 1.13이 [Go 1.12](go1.12) 이후 6개월 만에 출시되었습니다.
변경 사항의 대부분은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언제나 그렇듯, 이번 릴리스는 Go 1의 [호환성 약속](/doc/go1compat.html)을 유지합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 기대합니다.

Go 1.13부터 `go` 명령어는 기본적으로 Google에서 운영하는 Go 모듈 미러와 Go 체크섬 데이터베이스를 사용하여 모듈을 다운로드하고 인증합니다. 이러한 서비스에 대한 개인정보 보호 정보는 <https://proxy.golang.org/privacy>를 참조하시고, 서버 사용 중지 방법이나 다른 서버 사용 방법을 포함한 설정 세부 사항은 [go 명령어 문서](/cmd/go/#hdr-Module_downloading_and_verification)를 참조하십시오. 비공개 모듈을 사용하는 경우, [환경 설정 문서](/cmd/go/#hdr-Module_configuration_for_non_public_modules)를 참조하십시오.

## 언어 변경 사항 {#language}

[number literal proposal](https://github.com/golang/proposal/blob/master/design/19308-number-literals.md)에 따라, Go 1.13은 더 균일하고 현대화된 숫자 리터럴 접두사 세트를 지원합니다.

- [이진 정수 리터럴](/ref/spec#Integer_literals):
    `0b` 또는 `0B` 접두사는 `0b1011`과 같은 이진 정수 리터럴을 나타냅니다.
  - [8진 정수 리터럴](/ref/spec#Integer_literals):
    `0o` 또는 `0O` 접두사는 `0o660`과 같은 8진 정수 리터럴을 나타냅니다.
    앞에 `0`이 오고 그 뒤에 8진수 숫자가 이어지는 기존의 8진수 표기법도 여전히 유효합니다.
  - [16진수 부동 소수점 리터럴](/ref/spec#Floating-point_literals):
    이제 `0x` 또는 `0X` 접두사를 사용하여 `0x1.0p-1021`과 같이 부동 소수점 수의 가수(mantissa)를 16진수 형식으로 표현할 수 있습니다.
    16진수 부동 소수점 수는 반드시 지수가 있어야 하며, 이는 문자 `p` 또는 `P` 뒤에 10진수 지수를 작성하여 표현합니다. 지수는 가수에 2의 지수 제곱을 곱하여 크기를 조절합니다.
  - [허수 리터럴](/ref/spec#Imaginary_literals):
    이제 허수 접미사 `i`를 모든 (2진수, 10진수, 16진수) 정수 또는 부동 소수점 리터럴과 함께 사용할 수 있습니다.
  - 숫자 구분자:
    이제 모든 숫자 리터럴의 자릿수를 `1_000_000`, `0b_1010_0110` 또는 `3.1415_9265`와 같이 언더스코어(`_`)를 사용하여 구분(그룹화)할 수 있습니다.
    언더스코어는 임의의 두 숫자 사이 또는 리터럴 접두사와 첫 번째 숫자 사이에 올 수 있습니다.

[signed shift counts 제안](https://github.com/golang/proposal/blob/master/design/19113-signed-shift-counts.md)에 따라,
Go 1.13에서는 [shift count](/ref/spec#Operators)가
반드시 unsigned여야 한다는 제한을 제거합니다. 이 변경으로 인해 `<<` 및 `>>` 연산자의
(이제는 제거된) 이 제한을 충족시키기 위해 오직 그 목적으로만 도입되었던
많은 인위적인 `uint` 변환의 필요성이 사라집니다.

이러한 언어 변경 사항은 컴파일러의 변경과 그에 따른 라이브러리 패키지 [`go/scanner`](#go/scanner) 및 [`text/scanner`](#text/scanner) (숫자 리터럴), 그리고 [`go/types`](#go/types) (부호 있는 시프트 횟수)의 내부 변경을 통해 구현되었습니다.

코드가 모듈을 사용하고 `go.mod` 파일에 언어 버전이 지정되어 있다면, 이러한 언어 변경 사항을 적용하기 위해 버전이 최소 `1.13`으로 설정되어 있는지 확인하십시오.
`go.mod` 파일을 직접 편집하거나, `go mod edit -go=1.13` 명령어를 실행하여 설정할 수 있습니다.

## 포트 {#ports}

Go 1.13은 Native Client (NaCl)에서 실행되는 마지막 릴리스입니다.

<!-- CL 170119, CL 168882 -->
`GOARCH=wasm`의 경우, 새로운 환경 변수 `GOWASM`에 바이너리 컴파일 시 적용할 실험적 기능들의 목록을 쉼표로 구분하여 지정할 수 있습니다.
유효한 값들에 대한 설명은 [여기](/cmd/go/#hdr-Environment_variables)에서 확인하십시오.

### AIX {#aix}

<!-- CL 164003, CL 169120 -->
PPC64(`aix/ppc64`) 기반 AIX에서 이제 cgo, external linking, 그리고 `c-archive` 및 `pie` 빌드 모드를 지원합니다.

### Android {#android}

<!-- CL 170127 -->
이제 Go 프로그램이 Android 10과 호환됩니다.

### Darwin {#darwin}

Go 1.12 릴리스 노트에서 [안내](go1.12#darwin)드린 바와 같이,
Go 1.13부터는 macOS 10.11 El Capitan 또는 그 이후 버전이 필요합니다.
이전 버전에 대한 지원은 중단되었습니다.

### FreeBSD {#freebsd}

Go 1.12 릴리스 노트에서 [공지](go1.12#freebsd)한 바와 같이,
이제 Go 1.13은 FreeBSD 11.2 이상 버전을 요구하며,
이전 버전에 대한 지원은 중단되었습니다.
FreeBSD 12.0 이상 버전은 `COMPAT_FREEBSD11` 옵션이 설정된 커널이 필요합니다 (이것이 기본값입니다).

### Illumos {#illumos}

<!-- CL 174457 -->
이제 Go는 `GOOS=illumos`를 통해 Illumos를 지원합니다.
`illumos` 빌드 태그는 `solaris` 빌드 태그를 포함합니다.

### Windows {#windows}

<!-- CL 178977 -->
내부적으로 링크된(internally-linked) Windows 바이너리에서 지정하는 Windows 버전이 이제 NT 4.0이 아닌 Windows 7로 변경되었습니다. 이는 이미 Go의 최소 요구 버전이었으나, 하위 호환 모드를 가진 시스템 콜의 동작에 영향을 줄 수 있습니다. 이제 이러한 시스템 콜들은 문서에 명시된 대로 동작하게 됩니다. 외부적으로 링크된(externally-linked) 바이너리(cgo를 사용하는 모든 프로그램)는 항상 더 최신 버전의 Windows 버전을 지정해 왔습니다.

## 도구 {#tools}

### 모듈 {#modules}

#### 환경 변수 {#proxy-vars}

<!-- CL 176580 -->
[`GO111MODULE`](/cmd/go/#hdr-Module_support) 환경 변수의 기본값은 계속해서 `auto`로 유지되지만, 이제 `auto` 설정은 현재 작업 디렉토리에 `go.mod` 파일이 포함되어 있거나 `go.mod` 파일이 포함된 디렉토리 하위에 있을 때, 현재 디렉토리가 `GOPATH/src` 내에 있더라도 `go` 명령의 모듈 인식(module-aware) 모드를 활성화합니다. 이 변경 사항은 `GOPATH/src` 내의 기존 코드 마이그레이션과, 모듈 인식 패키지를 모듈 인식 기능이 없는 임포터(importer)와 함께 유지 관리하는 작업을 간소화합니다.

<!-- CL 181719 -->
새로운 [`GOPRIVATE`](/cmd/go/#hdr-Module_configuration_for_non_public_modules) 환경 변수는 공개적으로 사용할 수 없는 모듈 경로를 지정합니다. 이 변수는 더 세밀한 제어를 제공하는 하위 수준의 `GONOPROXY` 및 `GONOSUMDB` 변수의 기본값으로 사용되며, 이를 통해 어떤 모듈을 프록시를 통해 가져오고 체크섬 데이터베이스를 사용하여 검증할지 결정할 수 있습니다.

<!-- CL 173441, CL 177958 -->
이제 [`GOPROXY`
환경 변수](/cmd/go/#hdr-Module_downloading_and_verification)를 쉼표로 구분된 프록시 URL 목록이나 특별 토큰인 `direct`로 설정할 수 있으며,
[기본값](#introduction)은 `https://proxy.golang.org,direct`로 변경되었습니다. 패키지 경로를 해당 패키지가 포함된 모듈로 해석할 때, `go` 커맨드는 목록에 있는 각 프록시의 모든 후보 모듈 경로를 순차적으로 시도합니다. 프록시에 접속할 수 없거나 404 또는 410 이외의 HTTP 상태 코드가 반환되면, 나머지 프록시를 확인하지 않고 검색을 종료합니다.

새로운 [`GOSUMDB`](/cmd/go/#hdr-Module_authentication_failures) 환경 변수는 메인 모듈의 `go.sum` 파일에 아직 나열되지 않은 모듈의 체크섬을 확인하기 위해 참조할 데이터베이스의 이름과, 선택적으로 공개 키 및 서버 URL을 식별합니다.

`GOSUMDB`에 명시적인 URL이 포함되어 있지 않은 경우, `GOPROXY` URL들을 조사하여 체크섬 데이터베이스 지원을 나타내는 엔드포인트를 찾아 URL을 선택하며, 어떤 프록시에서도 지원하지 않을 경우 지정된 데이터베이스로 직접 연결하는 방식으로 대체합니다. `GOSUMDB`가 `off`로 설정되면 체크섬 데이터베이스를 참조하지 않고 `go.sum` 파일에 존재하는 기존 체크섬만 검증합니다.

기본 프록시 및 체크섬 데이터베이스에 접속할 수 없는 사용자(예: 방화벽 또는 샌드박스 설정으로 인해)는 `GOPROXY`를 `direct`로, 그리고/또는 `GOSUMDB`를 `off`로 설정하여 사용을 중단할 수 있습니다.
[`go` `env` `-w`](#go-env-w)
를 사용하여 플랫폼에 관계없이 이러한 변수들의 기본값을 설정할 수 있습니다:

```bash
go env -w GOPROXY=direct
go env -w GOSUMDB=off
```

#### `go` `get` {#go-get}

<!-- CL 174099 -->
모듈 인식 모드(module-aware mode)에서,
[`go` `get`](/cmd/go/#hdr-Add_dependencies_to_current_module_and_install_them)
에 `-u` 플래그를 사용하면 이제 GOPATH 모드에서 `go` `get` `-u`가 업데이트하는 패키지 집합과 더 일관성 있는, 더 작은 범위의 모듈 집합을 업데이트합니다.
`go` `get` `-u`는 여전히 명령줄에 지정된 모듈과 패키지를 업데이트하지만, 추가적으로 지정된 패키지가 *임포트하는(imported by)* 패키지를 포함하는 모듈만 업데이트하며, 지정된 패키지를 포함하는 모듈의 전이적 모듈 요구사항(transitive module requirements)까지 모두 업데이트하지는 않습니다.

특히 `go` `get` `-u`를 (추가 인자 없이) 사용하면 이제 현재 디렉토리에 있는 패키지의 전이적 임포트(transitive imports)만 업데이트한다는 점에 유의하십시오. 대신 메인 모듈에서 전이적으로 임포트된 모든 패키지(테스트 의존성 포함)를 업데이트하려면 `go` `get` `-u` `all`을 사용하십시오.

<!-- CL 177879 -->
`go` `get` `-u`에 대한 위 변경 사항의 결과로, `go` `get` 하위 명령어는 더 이상 `-m` 플래그를 지원하지 않습니다. 이 플래그는 `go` `get`이 패키지를 로드하기 전에 중단되도록 하는 역할을 했습니다. `-d` 플래그는 계속 지원되며, 지정된 패키지의 의존성을 빌드하는 데 필요한 소스 코드를 다운로드한 후 `go` `get`이 중단되도록 합니다.

<!-- CL 177677 -->
기본적으로 모듈 모드에서의 `go` `get` `-u`는 GOPATH 모드와 마찬가지로 테스트용이 아닌 의존성만 업그레이드합니다. 이제는 `-t` 플래그도 사용할 수 있으며, 이 플래그를 사용하면 (GOPATH 모드와 마찬가지로) `go` `get`이 명령줄에 지정된 패키지의 _테스트에서_ 임포트한 패키지들을 포함하게 됩니다.

<!-- CL 167747 -->
모듈 인식(module-aware) 모드에서, `go` `get` 하위 명령어가 이제 버전 접미사 `@patch`를 지원합니다. `@patch` 접미사는 지정된 모듈 또는 지정된 패키지를 포함하는 모듈을 빌드 리스트에서 발견된 버전과 동일한 메이저 및 마이너 버전을 가진 가장 최신 패치 릴리스로 업데이트해야 함을 나타냅니다.

<!-- CL 184440 -->
버전 접미사 없이 `go` `get`의 인자로 전달된 모듈이 이미 최신 릴리스 버전보다 더 높은 버전으로 요구되고 있다면, 해당 모듈은 더 높은 버전으로 유지됩니다. 이는 모듈 의존성에 대한 `-u` 플래그의 동작 방식과 일치합니다. 이를 통해 프리릴리스 버전에서 예기치 않게 다운그레이드되는 것을 방지합니다.
새로운 버전 접미사인 `@upgrade`는 이러한 동작을 명시적으로 요청합니다. `@latest`는 현재 버전과 관계없이 최신 버전을 명시적으로 요청합니다.

#### 버전 검증 {#version-validation}

<!-- CL 181881 -->

버전 관리 시스템에서 모듈을 추출할 때, `go` 명령어가 요청된 버전 문자열에 대해 추가적인 검증을 수행합니다.

`+incompatible` 버전 주석은 모듈 도입 이전에 생성된 저장소에 대해 [시맨틱 임포트 버전 관리](/cmd/go/#hdr-Module_compatibility_and_semantic_versioning) 요구 사항을 우회합니다. 이제 `go` 커맨드는 해당 버전에 명시적인 `go.mod` 파일이 포함되어 있지 않은지 확인합니다.

`go` 명령어가 이제 [pseudo-versions](/cmd/go/#hdr-Pseudo_versions)와 버전 관리 메타데이터 간의 매핑을 검증합니다. 구체적으로는 다음과 같습니다:

- 버전 접두사는 `vX.0.0` 형태여야 하거나, 지정된 리비전의 조상(ancestor)에 있는 태그로부터 유도되어야 하며, 또는 지정된 리비전 자체에 [빌드 메타데이터](https://semver.org/#spec-item-10)가 포함된 태그로부터 유도되어야 합니다.
  - 날짜 문자열은 리비전의 UTC 타임스탬프와 일치해야 합니다.
  - 리비전의 짧은 이름(short name)은 `go` 명령어가 생성하는 것과 동일한 수의 문자를 사용해야 합니다. (`git`에서 사용하는 SHA-1 해시의 경우, 12자리 접두사.)

[메인 모듈](/cmd/go/#hdr-The_main_module_and_the_build_list)의 `require` 지시문에서 유효하지 않은 의사 버전(pseudo-version)을 사용하는 경우, 일반적으로 버전을 커밋 해시만 남기고 수정(redacting)한 뒤 `go` `list` `-m` `all` 또는 `go` `mod` `tidy`와 같은 `go` 명령어를 다시 실행하여 수정할 수 있습니다. 예를 들어,

require github.com/docker/docker v1.14.0-0.20190319215453-e7b5f7dbe98c

제공해주신 텍스트가 "can be redacted to"라는 짧은 구절뿐이라, 문맥에 따라 적절한 번역이 달라질 수 있습니다. 기술 문서의 문맥에서 가장 가능성 높은 번역들을 제안해 드립니다.

**1. 일반적인 기술 문서/가이드라인인 경우:**
> "~로 편집(또는 마스킹)될 수 있습니다"

**2. 데이터 보안이나 개인정보 보호 관련 설정인 경우:**
> "~로 익명화 처리될 수 있습니다"

**3. 특정 텍스트를 다른 텍스트로 대체한다는 의미인 경우:**
> "~로 수정될 수 있습니다"

**정확한 번역을 위해 전체 문장을 제공해주시면, 마크다운 구조를 유지하여 더 정확하게 번역해 드리겠습니다.**

`require github.com/docker/docker e7b5f7dbe98c`

현재 다음과 같이 해석되는 (또는 resolve되는)

require github.com/docker/docker v0.7.3-0.20190319215453-e7b5f7dbe98c

메인 모듈의 전이적 의존성(transitive dependencies) 중 하나가 유효하지 않은 버전이나 의사 버전(pseudo-version)을 요구하는 경우, 메인 모듈의 `go.mod` 파일에서 [`replace` 지시어](/cmd/go/#hdr-The_go_mod_file)를 사용하여 유효하지 않은 버전을 유효한 버전으로 대체할 수 있습니다. 만약 대체 대상이 커밋 해시라면, 위와 같이 적절한 의사 버전으로 해석됩니다. 예를 들어,

replace github.com/docker/docker v1.14.0-0.20190319215453-e7b5f7dbe98c => github.com/docker/docker e7b5f7dbe98c

현재 다음으로 해석됩니다.

replace github.com/docker/docker v1.14.0-0.20190319215453-e7b5f7dbe98c => github.com/docker/docker v0.7.3-0.20190319215453-e7b5f7dbe98c

### Go command {#go-command}

<!-- CL 171137 -->
[`go` `env`](/cmd/go/#hdr-Environment_variables)
명령어는 이제 `go` 명령어가 인식하는 환경 변수의 사용자별 기본값을 설정하는 `-w` 플래그와, 이전에 설정된 기본값을 해제하는 `-u` 플래그를 지원합니다. `go` `env` `-w`를 통해 설정된 기본값은 [`os.UserConfigDir()`](/pkg/os/#UserConfigDir) 내의 `go/env` 파일에 저장됩니다.

<!-- CL 173343 -->
[`go` `version`](/cmd/go/#hdr-Print_Go_version) 명령어가 이제 실행 파일 및 디렉터리 이름을 인자로 받습니다. 실행 파일을 대상으로 호출하면, `go` `version`은 해당 실행 파일을 빌드하는 데 사용된 Go 버전을 출력합니다. `-m` 플래그를 사용하면, `go` `version`은 사용 가능한 경우 해당 실행 파일에 내장된 모듈 버전 정보를 출력합니다. 디렉터리를 대상으로 호출하면, `go` `version`은 해당 디렉터리와 하위 디렉터리에 포함된 실행 파일들에 대한 정보를 출력합니다.

<!-- CL 173345 -->
새로운 [`go` `build` 플래그](/cmd/go/#hdr-Compile_packages_and_dependencies) `-trimpath`는 빌드 재현성(reproducibility)을 높이기 위해 컴파일된 실행 파일에서 모든 파일 시스템 경로를 제거합니다.

<!-- CL 167679 -->
`go` `build`에 전달된 `-o` 플래그가 기존 디렉터리를 가리키는 경우, 이제 `go` `build`는 패키지 인자와 일치하는 `main` 패키지에 대해 해당 디렉터리 내에 실행 파일을 작성합니다.

<!-- CL 173438 -->
`go` `build` 플래그 `-tags`는 이제 쉼표로 구분된 빌드 태그 목록을 받으며, 이를 통해 [`GOFLAGS`](/cmd/go/#hdr-Environment_variables)에서 여러 태그를 사용할 수 있습니다. 공백으로 구분하는 형식은 더 이상 권장되지 않지만(deprecated), 여전히 인식되며 계속 유지될 예정입니다.

<!-- CL 175983 -->
[`go`
`generate`](/cmd/go/#hdr-Generate_Go_files_by_processing_source)가 이제 `generate` 빌드 태그를 설정하여, 파일에서 지시문(directive)을 검색할 수는 있지만 빌드 과정에서는 무시되도록 합니다.

<!-- CL 165746 -->
Go 1.12 릴리스 노트에서 [공지](/doc/go1.12#binary-only)한 바와 같이, 바이너리 전용(binary-only) 패키지는 더 이상 지원되지 않습니다. 바이너리 전용 패키지(`//go:binary-only-package` 주석으로 표시됨)를 빌드하면 이제 에러가 발생합니다.

### 컴파일러 툴체인 {#compiler}

<!-- CL 170448 -->
컴파일러에 더 정밀한 탈출 분석(escape analysis)의 새로운 구현이 도입되었습니다. 대부분의 Go 코드에서 성능 향상이 있을 것입니다 (다시 말해, 더 많은 Go 변수와 표현식이 힙 대신 스택에 할당됩니다). 하지만 이러한 정밀도 향상으로 인해 이전에는 우연히 작동했던 잘못된 코드(예를 들어, [`unsafe.Pointer` 안전 규칙](/pkg/unsafe/#Pointer)을 위반하는 코드)가 작동하지 않을 수 있습니다. 이와 관련하여 회귀(regression) 현상이 발견되면, `go` `build` `-gcflags=all=-newescape=false`를 통해 이전의 탈출 분석 패스를 다시 활성화할 수 있습니다.
이전 탈출 분석을 사용하는 옵션은 향후 릴리스에서 제거될 예정입니다.

<!-- CL 161904 -->
컴파일러가 더 이상 부동 소수점 또는 복소수 상수를 `go_asm.h` 파일로 출력하지 않습니다. 이러한 값들은 항상 어셈블리 코드에서 숫자 상수로 사용할 수 없는 형태로 출력되어 왔습니다.

### Assembler {#assembler}

<!-- CL 157001 -->
어셈블러가 이제 ARM v8.1에서 도입된 많은 원자적(atomic) 명령어를 지원합니다.

### gofmt {#gofmt}

`gofmt`(그리고 이를 포함한 `go fmt`)는 이제 숫자 리터럴의 접두사와 지수를 소문자로 정규화하지만, 16진수 숫자는 그대로 유지합니다. 이는 새로운 8진수 접두사를 사용할 때 가독성을 향상시키며(`0O`가 `0o`가 됨), 이 재작성 규칙은 일관되게 적용됩니다.

또한 `gofmt`는 이제 10진수 정수 허수 리터럴에서 불필요한 앞자리 0을 제거합니다. (하위 호환성을 위해 `0`으로 시작하는 정수 허수 리터럴은 8진수가 아닌 10진수로 간주됩니다. 불필요한 앞자리 0을 제거함으로써 잠재적인 혼동을 방지합니다.)

예를 들어, `gofmt`를 적용하면 `0B1010`, `0XabcDEF`, `0O660`, `1.2E3`, 그리고 `01i`는 각각 `0b1010`, `0xabcDEF`, `0o660`, `1.2e3`, `1i`가 됩니다.

### `godoc` 및 `go` `doc` {#godoc}

<!-- CL 174322 -->
`godoc` 웹 서버는 더 이상 메인 바이너리 배포판에 포함되지 않습니다.
`godoc` 웹 서버를 로컬에서 실행하려면, 먼저 수동으로 설치하십시오:

```bash
go get golang.org/x/tools/cmd/godoc
	godoc
```

<!-- CL 177797 -->
이제 [`go` `doc`](/cmd/go/#hdr-Show_documentation_for_package_or_symbol)
명령어는 명령어를 제외하고 출력 결과에 항상 패키지 절(package clause)을 포함합니다. 이는 특정 조건에서 패키지 절이 생략되었던 기존의 휴리스틱 방식의 동작을 대체합니다.

## 런타임 {#runtime}

<!-- CL 161477 -->
범위 초과(Out of range) 패닉 메시지에 이제 범위를 벗어난 인덱스와 슬라이스의 길이(또는 용량)가 포함됩니다. 예를 들어, 길이가 1인 슬라이스에서 `s[3]`을 호출하면 "runtime error: index out of range [3] with length 1"이라는 패닉이 발생합니다.

<!-- CL 171758 -->
이번 릴리스에서는 대부분의 `defer` 사용 사례에 대한 성능이 30% 향상되었습니다.

<!-- CL 142960 -->
런타임이 이제 운영 체제에 메모리를 더 적극적으로 반환하여 공동 테넌트(co-tenant) 애플리케이션이 사용할 수 있도록 합니다. 이전에는 힙 크기가 급증한 후 런타임이 메모리를 5분 이상 보유할 수 있었습니다. 이제는 힙이 줄어든 후 즉시 반환을 시작합니다. 하지만 Linux를 포함한 많은 OS에서는 OS 자체가 메모리를 지연하여 회수하므로, 시스템에 메모리 압박이 발생하기 전까지는 프로세스의 RSS가 감소하지 않을 것입니다.

## 표준 라이브러리 {#library}

### TLS 1.3 {#tls_1_3}

Go 1.12에서 발표된 바와 같이, Go 1.13은 `crypto/tls` 패키지에서 기본적으로 TLS 1.3 지원을 활성화합니다. `GODEBUG` 환경 변수에 `tls13=0` 값을 추가하여 이 기능을 비활성화할 수 있습니다. 이 선택적 제외(opt-out) 옵션은 Go 1.14에서 제거될 예정입니다.

중요한 호환성 정보는 [Go 1.12 릴리스 노트](/doc/go1.12#tls_1_3)를 참조하십시오.

### [crypto/ed25519](/pkg/crypto/ed25519/) {#crypto_ed25519}

<!-- CL 174945, 182698 -->
새로운 [`crypto/ed25519`](/pkg/crypto/ed25519/)
패키지는 Ed25519 서명 체계를 구현합니다. 이 기능은 이전에
[`golang.org/x/crypto/ed25519`](https://godoc.org/golang.org/x/crypto/ed25519)
패키지에서 제공되었으며, Go 1.13 이상 버전에서 사용할 경우
`crypto/ed25519`를 위한 래퍼(wrapper)가 됩니다.

### 에러 래핑 (Error wrapping) {#error_wrapping}

<!-- CL 163558, 176998 -->
Go 1.13에는 [Error Values 제안](https://go.googlesource.com/proposal/+/master/design/29934-error-values.md)에서 처음 제안되고 [관련 이슈](/issue/29934)에서 논의된 에러 래핑(error wrapping) 지원 기능이 포함되어 있습니다.

에러 `e`는 `w`를 반환하는 `Unwrap` 메서드를 제공함으로써 다른 에러 `w`를 *wrap*(감싸기) 할 수 있습니다. 프로그램에서는 `e`와 `w`를 모두 사용할 수 있으므로, `e`가 `w`에 추가적인 컨텍스트를 제공하거나 이를 재해석하는 동시에, 프로그램이 여전히 `w`를 기반으로 의사결정을 내릴 수 있도록 합니다.

래핑(wrapping)을 지원하기 위해, 이제 [`fmt.Errorf`](#fmt)는 래핑된 에러를 생성하기 위한 `%w` 동사를 제공하며, [`errors`](#errors) 패키지의 세 가지 새로운 함수([`errors.Unwrap`](/pkg/errors/#Unwrap), [`errors.Is`](/pkg/errors/#Is), [`errors.As`](/pkg/errors/#As))를 통해 래핑된 에러의 언래핑(unwrapping)과 조사가 간소화되었습니다.

더 자세한 정보는 [`errors` 패키지 문서](/pkg/errors/)를 읽거나, [Error Value FAQ](/wiki/ErrorValueFAQ)를 참조하세요.
곧 관련 블로그 포스트도 게시될 예정입니다.

### 라이브러리의 마이너 변경 사항 {#minor_library_changes}

언제나 그렇듯, Go 1 [호환성 약속](/doc/go1compat)을 염두에 둔 라이브러리의 다양한 소규모 변경 및 업데이트가 있었습니다.

#### [bytes](/pkg/bytes/)

새로운 [`ToValidUTF8`](/pkg/bytes/#ToValidUTF8) 함수는 주어진 바이트 슬라이스의 복사본을 반환하며, 이때 유효하지 않은 UTF-8 바이트 시퀀스의 각 연속된 구간은 지정된 슬라이스로 대체됩니다.

<!-- bytes -->

#### [context](/pkg/context/)

<!-- CL 169080 -->
[`WithValue`](/pkg/context/#WithValue)에 의해 반환되는 컨텍스트의 포맷팅이 더 이상 `fmt`에 의존하지 않으며, 이전과 동일한 방식으로 문자열화(stringify)되지 않습니다. 이전의 정확한 문자열화 결과에 의존하는 코드는 영향을 받을 수 있습니다.

제공해주신 내용이 없습니다. 번역할 Markdown 콘텐츠를 입력해 주시면, 요청하신 지침에 따라 정확하게 한국어로 번역해 드리겠습니다.

#### [crypto/tls](/pkg/crypto/tls/)

SSL 버전 3.0 (SSLv3)에 대한 지원이 [이제 deprecated 되었으며 Go 1.14에서 제거될 예정입니다](/issue/32716). SSLv3는 TLS 이전에 사용되었으며 [암호학적으로 결함이 있는](https://tools.ietf.org/html/rfc7568) 프로토콜임에 유의하십시오.

SSLv3는 Go 1.12에서 서버 측의 기본 설정으로 실수로 활성화되었던 시기를 제외하고는 항상 기본적으로 비활성화되어 있었습니다. 현재는 다시 기본적으로 비활성화된 상태입니다. (SSLv3는 클라이언트 측에서 지원된 적이 없습니다.)

<!-- CL 177698 -->
이제 TLS 버전 1.2 및 1.3에서 Ed25519 인증서가 지원됩니다.

<!-- crypto/tls -->

#### [crypto/x509](/pkg/crypto/x509/)

<!-- CL 175478 -->
이제 [RFC 8410](https://www.rfc-editor.org/info/rfc8410)에 따라 인증서 및 인증서 요청에서 Ed25519 키가 지원되며, [`ParsePKCS8PrivateKey`](/pkg/crypto/x509/#ParsePKCS8PrivateKey), [`MarshalPKCS8PrivateKey`](/pkg/crypto/x509/#MarshalPKCS8PrivateKey), [`ParsePKIXPublicKey`](/pkg/crypto/x509/#ParsePKIXPublicKey) 함수에서도 지원됩니다.

<!-- CL 169238 -->
시스템 루트(system roots)를 검색하는 경로에 Alpine Linux 3.7+의 기본 위치를 지원하기 위해 `/etc/ssl/cert.pem`이 추가되었습니다.

<!-- crypto/x509 -->

#### [database/sql](/pkg/database/sql/)

<!-- CL 170699 -->
새로운 [`NullTime`](/pkg/database/sql/#NullTime) 타입은 null일 수 있는 `time.Time`을 나타냅니다.

<!-- CL 174178 -->
새로운 [`NullInt32`](/pkg/database/sql/#NullInt32) 타입은 null일 수 있는 `int32`를 나타냅니다.

<!-- database/sql -->

#### [debug/dwarf](/pkg/debug/dwarf/)

<!-- CL 158797 -->
[`Data.Type`](/pkg/debug/dwarf/#Data.Type)
메서드는 타입 그래프에서 알 수 없는 DWARF 태그를 발견해도 더 이상 패닉(panic)을 발생시키지 않습니다. 대신, 해당 타입 구성 요소를 [`UnsupportedType`](/pkg/debug/dwarf/#UnsupportedType)
객체로 표현합니다.

<!-- debug/dwarf -->

#### [errors](/pkg/errors/)

<!-- CL 163558 -->

새로운 함수 [`As`](/pkg/errors/#As)는 주어진 에러 체인(래핑된 에러들의 시퀀스)에서 지정된 타겟의 타입과 일치하는 첫 번째 에러를 찾아, 일치하는 경우 타겟을 해당 에러 값으로 설정합니다.

새로운 함수 [`Is`](/pkg/errors/#Is)는 주어진 에러 값이 다른 에러 체인 내의 에러와 일치하는지 여부를 보고합니다.

새로운 함수 [`Unwrap`](/pkg/errors/#Unwrap)은 주어진 에러에 대해 `Unwrap`을 호출한 결과가 존재하는 경우 이를 반환합니다.

<!-- errors -->

#### [fmt](/pkg/fmt/)

<!-- CL 160245 -->

출력 동사 `%x`와 `%X`는 이제 부동 소수점 및 복소수를 각각 소문자와 대문자의 16진수 표기법으로 형식화합니다.

<!-- CL 160246 -->

새로운 출력 동사 `%O`는 정수를 8진수로 포맷하며, `0o` 접두사를 출력합니다.

<!-- CL 160247 -->

이제 스캐너가 16진수 부동 소수점 값, 자릿수 구분 언더바(`_`), 그리고 `0b` 및 `0o` 접두사를 지원합니다.
자세한 내용은 [언어 변경 사항](#language)을 참조하십시오.

<!-- CL 176998 -->

[`Errorf`](/pkg/fmt/#Errorf) 함수에
새로운 동사 `%w`가 추가되었으며, 이의 피연산자는 반드시 error여야 합니다.
`Errorf`에서 반환된 error는 `%w`의 피연산자를 반환하는
`Unwrap` 메서드를 갖게 됩니다.

<!-- fmt -->

#### [go/scanner](/pkg/go/scanner/)

<!-- CL 175218 -->
스캐너가 새로운 Go 숫자 리터럴을 인식하도록 업데이트되었습니다. 구체적으로 `0b`/`0B` 접두사가 붙은 이진 리터럴, `0o`/`0O` 접두사가 붙은 8진 리터럴, 그리고 16진 가수(mantissa)를 가진 부동 소수점 수가 추가되었습니다. 이제 모든 숫자 리터럴에 허수 접미사 `i`를 사용할 수 있으며, 자릿수 구분자로 언더스코어(`_`)를 사용할 수 있습니다.
자세한 내용은 [언어 변경 사항](#language)을 참조하십시오.

<!-- go/scanner -->

#### [go/types](/pkg/go/types/)

타입 체커가 정수 시프트(integer shifts)에 대한 새로운 규칙을 따르도록 업데이트되었습니다.
자세한 내용은 [언어 변경 사항](#language)을 참조하세요.

<!-- go/types -->

#### [html/template](/pkg/html/template/)

<!-- CL 175218 -->
`<script>` 태그의 `type` 속성을 "module"로 설정하여 사용할 때, 이제 코드가 [JavaScript module script](https://html.spec.whatwg.org/multipage/scripting.html#the-script-element:module-script-2)로 해석됩니다.

<!-- html/template -->

#### [log](/pkg/log/)

<!-- CL 168920 -->
새로운 [`Writer`](/pkg/log/#Writer) 함수는 표준 로거의 출력 대상(output destination)을 반환합니다.

<!-- log -->

#### [math/big](/pkg/math/big/)

<!-- CL 160682 -->
새로운 [`Rat.SetUint64`](/pkg/math/big/#Rat.SetUint64) 메서드는 `Rat`을 `uint64` 값으로 설정합니다.

<!-- CL 166157 -->
[`Float.Parse`](/pkg/math/big/#Float.Parse)의 경우, base가 0이면 가독성을 위해 숫자 사이에 언더스코어(`_`)를 사용할 수 있습니다.
자세한 내용은 [언어 변경 사항](#language)을 참조하십시오.

<!-- CL 166157 -->
[`Int.SetString`](/pkg/math/big/#Int.SetString)의 경우, base가 0이면 가독성을 위해 숫자 사이에 언더스코어(`_`)를 사용할 수 있습니다.
자세한 내용은 [언어 변경 사항](#language)을 참조하십시오.

<!-- CL 168237 -->
[`Rat.SetString`](/pkg/math/big/#Rat.SetString)이 이제 10진수가 아닌 부동 소수점 표현을 허용합니다.

<!-- math/big -->

#### [math/bits](/pkg/math/bits/)

<!-- CL 178177 -->
[`Add`](/pkg/math/bits/#Add),
[`Sub`](/pkg/math/bits/#Sub),
[`Mul`](/pkg/math/bits/#Mul),
[`RotateLeft`](/pkg/math/bits/#RotateLeft), 그리고
[`ReverseBytes`](/pkg/math/bits/#ReverseBytes)의 실행 시간이 이제
입력값과 관계없이 일정함이 보장됩니다.

<!-- math/bits -->

#### [net](/pkg/net/)

<!-- CL 156366 -->
`resolv.conf`에 `use-vc`가 설정된 Unix 시스템에서는 DNS resolution을 위해 TCP가 사용됩니다.

<!-- CL 170678 -->
새로운 필드 [`ListenConfig.KeepAlive`](/pkg/net/#ListenConfig.KeepAlive)는
리스너가 수락한 네트워크 연결의 keep-alive 기간을 지정합니다.
이 필드가 0(기본값)이면 TCP keep-alive가 활성화됩니다.
이를 비활성화하려면 음수 값으로 설정하십시오.

keep-alive 타임아웃으로 인해 종료된 연결의 I/O에서 반환된 에러는 호출 시 `true`를 반환하는 `Timeout` 메서드를 갖게 된다는 점에 유의하십시오. 이로 인해 keep-alive 에러를 [`SetDeadline`](/pkg/net/#Conn) 메서드 및 유사한 메서드로 설정한 데드라인(deadline) 초과로 인해 반환된 에러와 구분하기 어려울 수 있습니다.

데드라인을 사용하고 `Timeout` 메서드나 [`os.IsTimeout`](/pkg/os/#IsTimeout)으로 이를 확인하는 코드는 keep-alive를 비활성화하거나, (Unix 시스템에서) `errors.Is(syscall.ETIMEDOUT)`를 사용하는 것이 좋습니다. 후자의 경우 keep-alive 타임아웃에는 `true`를 반환하고 데드라인 타임아웃에는 `false`를 반환합니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- CL 76410 -->
새로운 필드인 [`Transport.WriteBufferSize`](/pkg/net/http/#Transport.WriteBufferSize)와
[`Transport.ReadBufferSize`](/pkg/net/http/#Transport.ReadBufferSize)를 통해
[`Transport`](/pkg/net/http/#Transport)의 쓰기 및 읽기 버퍼 크기를 지정할 수 있습니다.
두 필드 중 어느 하나라도 0이면 기본 크기인 4KB가 사용됩니다.

<!-- CL 130256 -->
새로운 필드 [`Transport.ForceAttemptHTTP2`](/pkg/net/http/#Transport.ForceAttemptHTTP2)는 0이 아닌 `Dial`, `DialTLS`, `DialContext` 함수 또는 `TLSClientConfig`가 제공될 때 HTTP/2 활성화 여부를 제어합니다.

<!-- CL 140357 -->
[`Transport.MaxConnsPerHost`](/pkg/net/http/#Transport.MaxConnsPerHost)가 이제 HTTP/2와 함께 정상적으로 작동합니다.

<!-- CL 154383 -->
[`TimeoutHandler`](/pkg/net/http/#TimeoutHandler)의
[`ResponseWriter`](/pkg/net/http/#ResponseWriter)가 이제
[`Pusher`](/pkg/net/http/#Pusher) 인터페이스를 구현합니다.

<!-- CL 157339 -->
`StatusCode` `103` `"Early Hints"`가 추가되었습니다.

<!-- CL 163599 -->
[`Transport`](/pkg/net/http/#Transport)는 이제 바디 쓰기 작업을 최적화하기 위해, [`Request.Body`](/pkg/net/http/#Request.Body)의 [`io.ReaderFrom`](/pkg/io/#ReaderFrom) 구현이 가능한 경우 이를 사용합니다.

<!-- CL 167017 -->
지원되지 않는 transfer-encoding을 만났을 때, 이제 [`http.Server`](/pkg/net/http/#Server)는 HTTP 명세 [RFC 7230 Section 3.3.1](https://tools.ietf.org/html/rfc7230#section-3.3.1)에 따라 "501 Unimplemented" 상태를 반환합니다.

<!-- CL 167681 -->
새로운 [`Server`](/pkg/net/http/#Server) 필드인
[`BaseContext`](/pkg/net/http/#Server.BaseContext)와
[`ConnContext`](/pkg/net/http/#Server.ConnContext)를 통해
요청 및 연결에 제공되는 [`Context`](/pkg/context/#Context) 값을 더 세밀하게 제어할 수 있습니다.

<!-- CL 167781 -->
[`http.DetectContentType`](/pkg/net/http/#DetectContentType)가 이제 RAR 시그니처를 정확하게 감지하며, RAR v5 시그니처도 감지할 수 있습니다.

<!-- CL 173658 -->
새로운 [`Header`](/pkg/net/http/#Header) 메서드인 [`Clone`](/pkg/net/http/#Header.Clone)는 수신자의 복사본을 반환합니다.

<!-- CL 174324 -->
새로운 함수 [`NewRequestWithContext`](/pkg/net/http/#NewRequestWithContext)가 추가되었습니다. 이 함수는 생성된 외부 [`Request`](/pkg/net/http/#Request)의 전체 수명을 제어하는 [`Context`](/pkg/context/#Context)를 인자로 받으며, [`Client.Do`](/pkg/net/http/#Client.Do) 및 [`Transport.RoundTrip`](/pkg/net/http/#Transport.RoundTrip)과 함께 사용하기에 적합합니다.

<!-- CL 179457 -->
서버가 `"408 Request Timeout"` 응답을 사용하여 유휴 연결을 정상적으로 종료(gracefully shut down)할 때, [`Transport`](/pkg/net/http/#Transport)가 더 이상 오류를 기록하지 않습니다.

<!-- net/http -->

#### [os](/pkg/os/)

<!-- CL 160877 -->
새로운 [`UserConfigDir`](/pkg/os/#UserConfigDir) 함수는
사용자별 설정 데이터에 사용할 기본 디렉터리를 반환합니다.

<!-- CL 166578 -->
[`File`](/pkg/os/#File)을 `O_APPEND` 플래그를 사용하여 열었을 경우, 해당 파일의 [`WriteAt`](/pkg/os/#File.WriteAt) 메서드는 항상 에러를 반환합니다.

<!-- os -->

#### [os/exec](/pkg/os/exec/)

<!-- CL 174318 -->
Windows에서 [`Cmd`](/pkg/os/exec/#Cmd)의 환경은 [`Cmd.Env`](/pkg/os/exec/#Cmd.Env) 필드에 명시적인 값이 포함되어 있지 않은 한, 항상 부모 프로세스의 `%SYSTEMROOT%` 값을 상속받습니다.

<!-- os/exec -->

#### [reflect](/pkg/reflect/)

<!-- CL 171337 -->
새로운 [`Value.IsZero`](/pkg/reflect/#Value.IsZero) 메서드는 `Value`가 해당 타입의 제로 값(zero value)인지 여부를 보고합니다.

<!-- CL 174531 -->
이제 [`MakeFunc`](/pkg/reflect/#MakeFunc) 함수는 정확한 타입 일치를 요구하는 대신, 반환 값에 대한 할당 변환(assignment conversions)을 허용합니다. 이는 반환되는 타입은 인터페이스 타입이지만, 실제로 반환되는 값은 해당 타입을 구현하는 구체적인 값(concrete value)일 때 특히 유용합니다.

<!-- reflect -->

#### [runtime](/pkg/runtime/)

<!-- CL 167780 -->
이제 Traceback, [`runtime.Caller`](/pkg/runtime/#Caller),
그리고 [`runtime.Callers`](/pkg/runtime/#Callers)는 `PKG`의 전역 변수를
초기화하는 함수를 `PKG.init.ializers` 대신 `PKG.init`으로 참조합니다.

<!-- 런타임 -->

#### [strconv](/pkg/strconv/)

<!-- CL 160243 -->
[`strconv.ParseFloat`](/pkg/strconv/#ParseFloat),
[`strconv.ParseInt`](/pkg/strconv/#ParseInt)
및 [`strconv.ParseUint`](/pkg/strconv/#ParseUint)의 경우,
base가 0이면 가독성을 위해 숫자 사이에 언더스코어(`_`)를 사용할 수 있습니다.
자세한 내용은 [언어 변경 사항](#language)을 참조하십시오.

<!-- strconv -->

#### [strings](/pkg/strings/)

<!-- CL 142003 -->
새로운 [`ToValidUTF8`](/pkg/strings/#ToValidUTF8) 함수는 유효하지 않은 UTF-8 바이트 시퀀스의 각 연속된 구간을 지정된 문자열로 대체한 Given string의 복사본을 반환합니다.

<!-- strings -->

#### [sync](/pkg/sync/)

<!-- CL 148958, CL 148959, CL 152697, CL 152698 -->
[`Mutex.Lock`](/pkg/sync/#Mutex.Lock), [`Mutex.Unlock`](/pkg/sync/#Mutex.Unlock),
[`RWMutex.Lock`](/pkg/sync/#RWMutex.Lock), [`RWMutex.RUnlock`](/pkg/sync/#Mutex.RUnlock), 그리고
[`Once.Do`](/pkg/sync/#Once.Do)의 fast path가 이제 호출하는 쪽에서 인라인화(inline)됩니다.
amd64의 경합이 없는(uncontended) 경우, 이러한 변경을 통해 [`Once.Do`](/pkg/sync/#Once.Do)는 두 배 더 빨라졌으며,
[`Mutex`](/pkg/sync/#Mutex)/[`RWMutex`](/pkg/sync/#RWMutex) 메서드는 최대 10% 더 빨라졌습니다.

<!-- CL 166960 -->
대규모 [`Pool`](/pkg/sync/#Pool)이 더 이상 stop-the-world 일시 중지 시간을 증가시키지 않습니다.

<!-- CL 166961 -->
`Pool`은 더 이상 매 GC 이후에 완전히 다시 채워질 필요가 없습니다. 이제 모든 객체를 해제하는 대신 일부 객체를 GC 이후에도 유지하므로, `Pool`을 많이 사용하는 사용자의 부하 스파이크(load spikes)를 줄여줍니다.

<!-- sync -->

#### [syscall](/pkg/syscall/)

<!-- CL 168479 -->
Go 바이너리를 macOS App Store에 업로드할 수 있도록, Darwin 빌드에서 `_getdirentries64` 사용을 제거했습니다.

<!-- CL 174197 -->
[`SysProcAttr`](/pkg/syscall/?GOOS=windows#SysProcAttr)에 새롭게 추가된 `ProcessAttributes` 및 `ThreadAttributes` 필드는 Windows용으로 도입되었으며, 새로운 프로세스를 생성할 때 보안 설정을 지정할 수 있게 합니다.

<!-- CL 174320 -->
Windows에서 zero [`Chmod`](/pkg/syscall/?GOOS=windows#Chmod) 모드일 때 더 이상 `EINVAL`을 반환하지 않습니다.

<!-- CL 191337 -->
`Errno` 타입의 값은 [`errors.Is`](/pkg/errors/#Is)를 사용하여 [`ErrExist`](/pkg/os/#ErrExist)와 같이 `os` 패키지의 에러 값들과 비교하여 테스트할 수 있습니다.

<!-- syscall -->

#### [syscall/js](/pkg/syscall/js/)

<!-- CL 177537 -->
바이트 슬라이스와 `Uint8Array` 사이에서 바이트를 복사하기 위해 `TypedArrayOf`가
[`CopyBytesToGo`](/pkg/syscall/js/#CopyBytesToGo) 및
[`CopyBytesToJS`](/pkg/syscall/js/#CopyBytesToJS)로 대체되었습니다.

<!-- syscall/js -->

#### [testing](/pkg/testing/)

<!-- CL 112155 -->
벤치마크를 실행할 때, [`B.N`](/pkg/testing/#B.N)이 더 이상 반올림되지 않습니다.

<!-- CL 166717 -->
새로운 메서드 [`B.ReportMetric`](/pkg/testing/#B.ReportMetric)을 통해 사용자는 사용자 정의 벤치마크 메트릭을 보고하고 기본 제공 메트릭을 재정의할 수 있습니다.

<!-- CL 173722 -->
테스트 플래그는 이제 테스트를 위해 생성된 `main` 함수에 의해 호출되는 새로운 [`Init`](/pkg/testing/#Init) 함수에서 등록됩니다.
그 결과, 테스트 플래그는 이제 테스트 바이너리를 실행할 때만 등록되며, 패키지 초기화 중에 `flag.Parse`를 호출하는 패키지는 테스트 실패를 유발할 수 있습니다.

<!-- testing -->

#### [text/scanner](/pkg/text/scanner/)

<!-- CL 183077 -->
스캐너가 새로운 Go 숫자 리터럴을 인식하도록 업데이트되었습니다. 구체적으로 `0b`/`0B` 접두사가 붙은 2진수 리터럴, `0o`/`0O` 접두사가 붙은 8진수 리터럴, 그리고 16진수 가수를 가진 부동 소수점 숫자를 인식합니다.
또한, 새로운 [`AllowDigitSeparators`](/pkg/text/scanner/#AllowDigitSeparators) 모드를 통해 숫자 리터럴에 숫자 구분자로 언더스코어(`_`)를 포함할 수 있습니다 (하위 호환성을 위해 기본값은 off입니다).
자세한 내용은 [언어 변경 사항](#language)을 참조하십시오.

<!-- text/scanner -->

#### [text/template](/pkg/text/template/)

<!-- CL 161762 -->
새로운 [slice 함수](/pkg/text/template/#hdr-Functions)는
첫 번째 인자를 이후의 인자들로 슬라이싱한 결과를 반환합니다.

<!-- text/template -->

#### [time](/pkg/time/)

<!-- CL 122876 -->
이제 [`Format`](/pkg/time/#Time.Format) 및 [`Parse`](/pkg/time/#Parse)에서 연중 일수(Day-of-year)를 지원합니다.

<!-- CL 167387 -->
새로운 [`Duration`](/pkg/time/#Duration) 메서드인
[`Microseconds`](/pkg/time/#Duration.Microseconds)와
[`Milliseconds`](/pkg/time/#Duration.Milliseconds)는
해당 이름의 단위로 계산된 정수 값의 기간(duration)을 반환합니다.

<!-- time -->

#### [unicode](/pkg/unicode/)

[`unicode`](/pkg/unicode/) 패키지와 시스템 전반의 관련 지원 사항이 Unicode 10.0에서 [Unicode 11.0](https://www.unicode.org/versions/Unicode11.0.0/)으로 업그레이드되었습니다. 이번 업데이트를 통해 7개의 새로운 스크립트를 포함한 684개의 새 문자와 66개의 새 이모지가 추가되었습니다.

제공해주신 내용에 번역할 텍스트가 포함되어 있지 않습니다. 번역이 필요한 Markdown 내용을 입력해 주시면, 요청하신 지침에 따라 정확하게 한국어로 번역해 드리겠습니다.
