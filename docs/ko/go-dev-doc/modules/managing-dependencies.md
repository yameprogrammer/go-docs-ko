<!--{
  "Title": "의존성 관리"
}-->

코드에서 외부 패키지를 사용할 때, 해당 패키지(모듈 형태로 배포됨)는 의존성(dependencies)이 됩니다. 시간이 지나면서 이러한 패키지들을 업그레이드하거나 교체해야 할 수도 있습니다. Go는 외부 의존성을 통합하는 동안 Go 애플리케이션의 보안을 유지할 수 있도록 돕는 의존성 관리 도구를 제공합니다.

이 주제에서는 코드에서 사용하는 의존성을 관리하기 위한 작업 수행 방법을 설명합니다. 이러한 작업의 대부분은 Go 도구를 사용하여 수행할 수 있습니다. 또한, 유용하게 사용할 수 있는 몇 가지 다른 의존성 관련 작업 수행 방법도 함께 설명합니다.

**참고 항목**

*   모듈로서의 의존성 작업이 처음이라면, [Getting started tutorial](/doc/tutorial/getting-started)에서 간략한 소개를 확인해 보세요.
*   의존성을 관리하기 위해 `go` 명령어를 사용하면 요구 사항을 일관되게 유지하고 go.mod 파일의 내용이 유효함을 보장하는 데 도움이 됩니다. 명령어에 대한 참조는 [Command go](/cmd/go/)를 확인하세요. 또한 `go help mod tidy`와 같이 커맨드 라인에서 `go help` _command-name_을 입력하여 도움말을 얻을 수 있습니다.
*   의존성 변경을 위해 사용하는 Go 명령어들은 go.mod 파일을 수정합니다. 파일 내용에 대한 자세한 내용은 [go.mod file reference](/doc/modules/gomod-ref)를 참조하세요.
*   에디터나 IDE가 Go 모듈을 인식하게 하면 모듈 관리 작업이 더 쉬워질 수 있습니다. Go를 지원하는 에디터에 대한 자세한 내용은 [Editor plugins and IDEs](/doc/editors.html)를 확인하세요.
*   이 주제에서는 다른 사람들이 사용할 수 있도록 모듈을 개발, 게시 및 버전 관리하는 방법은 다루지 않습니다. 이에 대한 자세한 내용은 [Developing and publishing modules](developing)를 참조하세요.

## 의존성 사용 및 관리 워크플로우 {#workflow}

Go 도구를 사용하여 유용한 패키지를 가져오고 사용할 수 있습니다. [pkg.go.dev](https://pkg.go.dev)에서 유용하다고 생각되는 패키지를 검색한 후, `go` 명령어를 사용하여 해당 패키지를 자신의 코드에 import하여 함수를 호출할 수 있습니다.

다음은 가장 일반적인 의존성 관리 단계들을 나열한 것입니다. 각 단계에 대한 자세한 내용은 본 주제의 해당 섹션을 참조하십시오.

1. [pkg.go.dev](https://pkg.go.dev)에서 [유용한 패키지를 찾으세요](#locating_packages).
1. 코드에 사용하려는 [패키지를 가져오세요(import)](#locating_packages).
1. 의존성 추적을 위해 코드를 모듈에 추가하세요 (이미 모듈에 포함되어 있지 않은 경우). [의존성 추적 활성화하기](#enable_tracking)를 참조하세요.
1. 외부 패키지를 [의존성으로 추가하여](#adding_dependency) 관리하세요.
2. 시간이 지남에 따라 필요에 따라 [의존성 버전을 업그레이드하거나 다운그레이드하세요](#upgrading).

## 모듈로 의존성 관리하기 {#modules}

Go에서는 임포트하는 패키지들을 포함하는 모듈 형태로 의존성을 관리합니다.
이 프로세스는 다음 요소들에 의해 지원됩니다:

*   모듈을 게시하고 코드를 검색하기 위한 **탈중앙화된 시스템**입니다.
    개발자는 자신의 저장소에서 다른 개발자가 사용할 수 있도록 모듈을 제공하고 버전 번호와 함께 게시합니다.
*   모듈을 찾을 수 있는 **패키지 검색 엔진** 및 문서 브라우저(pkg.go.dev)입니다. [유용한 패키지 찾기 및 가져오기](#locating_packages)를 참조하세요.
*   모듈의 안정성과 하위 호환성 보장 내용을 이해하는 데 도움이 되는 모듈 **버전 번호 지정 규칙**입니다. [모듈 버전 번호 지정](version-numbers)을 참조하세요.
*   모듈 소스 가져오기, 업그레이드 등 의존성 관리를 쉽게 해주는 **Go 도구**들입니다. 자세한 내용은 이 주제의 각 섹션을 참조하세요.

## 유용한 패키지 찾기 및 임포트하기 {#locating_packages}

[pkg.go.dev](https://pkg.go.dev)에서 유용한 함수가 포함된 패키지를 검색할 수 있습니다.

코드에서 사용하려는 패키지를 찾았다면, 페이지 상단에서 패키지 경로를 찾아 Copy path 버튼을 클릭하여 경로를 클립보드에 복사하세요. 작성 중인 코드의 import 문에 다음과 같이 경로를 붙여넣으세요.

```
import "rsc.io/quote"
```

코드에서 패키지를 임포트한 후, 의존성 추적을 활성화하고 컴파일에 필요한 패키지 코드를 가져오십시오. 자세한 내용은 [코드에서 의존성 추적 활성화하기](#enable_tracking) 및 [의존성 추가하기](#adding_dependency)를 참조하십시오.

## 코드에서 의존성 추적 활성화하기 {#enable_tracking}

추가하는 의존성을 추적하고 관리하려면, 먼저 코드를 별도의 모듈에 넣는 것부터 시작하십시오. 이렇게 하면 소스 트리의 루트에 `go.mod` 파일이 생성됩니다. 추가하는 의존성들은 해당 파일에 나열됩니다.

코드를 별도의 모듈에 추가하려면 [`go mod init` 명령어](/ref/mod#go-mod-init)를 사용하세요. 예를 들어, 커맨드 라인에서 코드의 루트 디렉터리로 이동한 다음, 아래 예시와 같이 명령어를 실행합니다.

```
$ go mod init example/mymodule
```

`go mod init` 명령어의 인자는 모듈의 모듈 경로(module path)입니다. 가능하다면, 모듈 경로는 소스 코드의 저장소 위치로 설정해야 합니다.

처음에 모듈의 최종 저장소 위치를 알 수 없는 경우, 안전한 대체 경로를 사용하십시오. 이는 소유하고 있는 도메인 이름이나 제어 가능한 다른 이름(예: 회사 이름)과 함께, 모듈 이름 또는 소스 디렉터리를 따르는 경로가 될 수 있습니다. 자세한 내용은 [Naming a module](#naming_module)를 참조하십시오.

Go 도구를 사용하여 종속성을 관리하면, 도구가 `go.mod` 파일을 업데이트하여 종속성 목록을 최신 상태로 유지합니다.

의존성을 추가하면 Go 도구는 당신이 의존하는 모듈의 체크섬(checksum)이 포함된 `go.sum` 파일도 함께 생성합니다. Go는 다운로드한 모듈 파일의 무결성을 검증하는 데 이 파일을 사용하며, 특히 프로젝트에서 함께 작업하는 다른 개발자들에게 유용합니다.

`go.mod` 및 `go.sum` 파일을 코드와 함께 저장소에 포함하세요.

더 자세한 내용은 [go.mod reference](/doc/modules/gomod-ref)를 참조하십시오.

## 모듈 이름 짓기 {#naming_module}

의존성 추적을 위한 모듈을 생성하기 위해 `go mod init`을 실행할 때, 모듈의 이름 역할을 하는 모듈 경로(module path)를 지정합니다. 이 모듈 경로는 모듈 내 패키지들의 임포트 경로 접두사(import path prefix)가 됩니다. 다른 모듈의 모듈 경로와 충돌하지 않는 모듈 경로를 지정해야 합니다.

최소한 모듈 경로는 회사, 작성자 또는 소유자 이름과 같이 그 기원에 대한 정보만 나타내면 됩니다. 하지만 경로는 모듈이 무엇인지 또는 어떤 기능을 하는지에 대해 더 상세하게 기술할 수도 있습니다.

모듈 경로는 일반적으로 다음과 같은 형태입니다:

```
<prefix>/<descriptive-text>
```

* _prefix_는 일반적으로 모듈을 부분적으로 설명하는 문자열이며, 예를 들어 모듈의 출처를 설명하는 문자열일 수 있습니다. 다음과 같은 형태가 될 수 있습니다:

*   Go 도구가 모듈의 소스 코드를 찾을 수 있는 리포지토리의 위치 (모듈을 게시하는 경우 필수).

예를 들어, `github.com/<project-name>/`와 같을 수 있습니다.

다른 사람들이 사용할 수 있도록 모듈을 게시할 계획이라면 이 권장 사항을 따르십시오. 게시에 대한 자세한 내용은 [Developing and publishing modules](/doc/modules/developing)를 참조하십시오.

*   사용자가 제어할 수 있는 이름.

리포지토리 이름을 사용하지 않는 경우, 다른 사람이 사용하지 않을 것이라고 확신할 수 있는 접두사를 선택하십시오. 회사 이름이 좋은 선택지가 될 수 있습니다. `widgets`, `utilities` 또는 `app`과 같은 일반적인 용어는 피하십시오.

* _설명 텍스트(descriptive text)_의 경우, 프로젝트 이름을 사용하는 것이 좋은 선택입니다. 패키지 이름이 기능 설명을 하는 데 있어 가장 큰 비중을 차지한다는 점을 기억하세요. 모듈 경로는 이러한 패키지 이름들을 위한 네임스페이스를 생성합니다.

**예약된 모듈 경로 접두사(Reserved module path prefixes)**

Go는 다음 문자열들이 패키지 이름에 사용되지 않음을 보장합니다.

- `test` -- 다른 모듈의 함수를 로컬에서 테스트하기 위해 설계된 모듈의 경우, 모듈 경로 접두사로 `test`를 사용할 수 있습니다.

테스트의 일부로 생성되는 모듈에는 `test` 경로 접두사를 사용하세요.
예를 들어, 테스트 자체가 `go mod init test`를 실행한 다음, Go 소스 코드 분석 도구로 테스트하기 위해 해당 모듈을 특정 방식으로 설정할 수 있습니다.

- `example` -- 일부 Go 문서에서 모듈 경로 접두사로 사용됩니다. 예를 들어, 단순히 종속성을 추적하기 위해 모듈을 생성하는 튜토리얼 등에서 사용됩니다.

Go 문서에서도 예제가 게시된 모듈일 수 있음을 설명하기 위해 `example.com`을 사용한다는 점에 유의하세요.

## 의존성 추가하기 {#adding_dependency}

게시된 모듈에서 패키지를 임포트하고 있다면, [`go get` 명령어](/cmd/go/#hdr-Add_dependencies_to_current_module_and_install_them)를 사용하여 해당 모듈을 관리 대상 의존성으로 추가할 수 있습니다.

해당 명령어는 다음과 같은 작업을 수행합니다:

*   필요한 경우, 명령줄에 지정된 패키지를 빌드하는 데 필요한 모듈에 대해 `go.mod` 파일에 `require` 지시어를 추가합니다. `require` 지시어는 모듈이 의존하는 모듈의 최소 버전을 추적합니다. 자세한 내용은 [go.mod reference](/doc/modules/gomod-ref)를 참조하세요.
*   필요한 경우, 해당 모듈에 의존하는 패키지를 컴파일할 수 있도록 모듈 소스 코드를 다운로드합니다. proxy.golang.org와 같은 모듈 프록시 또는 버전 관리 저장소에서 직접 모듈을 다운로드할 수 있습니다. 소스는 로컬에 캐시됩니다.

Go 도구가 모듈을 다운로드하는 위치를 설정할 수 있습니다. 자세한 내용은 [모듈 프록시 서버 지정](#proxy_server)을 참조하십시오.

다음은 몇 가지 예시에 대한 설명입니다.

*   모듈 내 패키지의 모든 의존성을 추가하려면 아래와 같은 명령어를 실행하세요 ("."은 현재 디렉터리의 패키지를 의미합니다):

```
    $ go get .
    ```

*   특정 의존성을 추가하려면, 명령어의 인자로 해당 모듈 경로를 지정하십시오.

```
    $ go get example.com/theirmodule
    ```

이 명령은 다운로드하는 각 모듈을 인증합니다. 이를 통해 모듈이 게시된 시점부터 변경되지 않았음을 보장합니다. 만약 게시 이후에 모듈이 변경되었다면(예: 개발자가 커밋 내용을 변경한 경우), Go 도구는 보안 오류를 표시합니다. 이러한 인증 확인은 변조되었을 가능성이 있는 모듈로부터 사용자를 보호합니다.

## 특정 종속성 버전 가져오기 {#getting_version}

`go get` 명령어에서 버전을 지정함으로써 의존성 모듈의 특정 버전을 가져올 수 있습니다. 이 명령어는 go.mod 파일의 `require` 지시문을 업데이트합니다 (수동으로 업데이트할 수도 있습니다).

다음과 같은 경우에 이 작업을 수행하는 것이 좋습니다:

*   테스트를 위해 모듈의 특정 프리릴리스(pre-release) 버전을 가져오고 싶을 때.
*   현재 요구(require)하고 있는 버전이 제대로 작동하지 않아, 신뢰할 수 있는 다른 버전을 가져오고 싶을 때.
*   이미 요구(require)하고 있는 모듈을 업그레이드하거나 다운그레이드하고 싶을 때.

[`go get` 명령어](/ref/mod#go-get) 사용 예시는 다음과 같습니다:

*   특정 버전 번호를 가져오려면, 모듈 경로 뒤에 @ 기호와 원하는 버전을 추가하세요:

```
    $ go get example.com/theirmodule@v1.3.4
    ```

*   최신 버전을 가져오려면 모듈 경로 뒤에 `@latest`를 추가하세요:

```
    $ go get example.com/theirmodule@latest
    ```

다음 `go.mod` 파일의 `require` 지시문 예시([go.mod 참조](/doc/modules/gomod-ref) 참조)는 특정 버전 번호를 요구하는 방법을 보여줍니다:

```
require example.com/theirmodule v1.3.4
```

## 사용 가능한 업데이트 찾기 {#discovering_updates}

현재 모듈에서 이미 사용 중인 의존성의 최신 버전이 있는지 확인할 수 있습니다. `go list` 명령어를 사용하면 모듈의 의존성 목록과 해당 모듈에서 사용 가능한 최신 버전을 함께 표시할 수 있습니다. 사용 가능한 업그레이드 버전을 발견하면, 코드에 적용해 보고 새 버전으로 업그레이드할지 여부를 결정할 수 있습니다.

`go list` 명령에 대한 자세한 내용은 [`go list -m`](/ref/mod#go-list-m)을 참조하십시오.

여기에 몇 가지 예시가 있습니다.

*   현재 모듈의 의존성인 모든 모듈의 목록과 각 모듈의 최신 사용 가능 버전을 표시합니다:

```
    $ go list -m -u all
    ```

*   특정 모듈에서 사용 가능한 최신 버전을 표시합니다:

```
    $ go list -m -u example.com/theirmodule
    ```

## 의존성 업그레이드 또는 다운그레이드 {#upgrading}

Go 도구를 사용하여 사용 가능한 버전을 확인한 후, 다른 버전을 의존성으로 추가하여 의존성 모듈을 업그레이드하거나 다운그레이드할 수 있습니다.

1. 새로운 버전을 찾으려면 [사용 가능한 업데이트 찾기](#discovering_updates)에 설명된 대로 `go list` 명령어를 사용하십시오.

1. 특정 버전을 종속성으로 추가하려면 [특정 종속성 버전 가져오기](#getting_version)에 설명된 대로 `go get` 명령어를 사용하세요.

## 코드 의존성 동기화하기 {#synchronizing}

코드에서 임포트한 모든 패키지의 의존성을 관리하는 동시에, 더 이상 임포트하지 않는 패키지의 의존성을 제거할 수 있습니다.

이는 코드와 종속성을 변경하는 과정에서, 코드에 임포트된 패키지들이 구체적으로 요구하는 컬렉션과 더 이상 일치하지 않는 관리형 종속성 및 다운로드된 모듈 컬렉션이 생성되었을 때 유용할 수 있습니다.

관리되는 종속성 세트를 깔끔하게 유지하려면 `go mod tidy` 명령어를 사용하세요. 이 명령어는 코드에서 임포트된 패키지 세트를 사용하여, 필요하지만 누락된 모듈을 추가하도록 go.mod 파일을 수정합니다. 또한 관련 패키지를 제공하지 않는 사용되지 않는 모듈을 제거합니다.

이 명령은 제거된 모듈에 대한 정보를 출력하는 `-v` 플래그 하나를 제외하고는 인수를 가지지 않습니다.

```
$ go mod tidy
```

## 게시되지 않은 모듈 코드를 대상으로 개발 및 테스트하기 {#unpublished}

게시되지 않은 의존성 모듈을 사용하도록 코드를 지정할 수 있습니다. 이러한 모듈의 코드는 각각의 저장소, 해당 저장소의 포크(fork), 또는 이를 사용하는 현재 모듈과 동일한 드라이브에 있을 수 있습니다.

다음과 같은 경우에 이 작업을 수행하면 좋습니다:

*   포크(fork) 및/또는 클론(clone) 후와 같이 외부 모듈의 코드에 직접 변경 사항을 적용하고 싶은 경우입니다. 예를 들어, 모듈의 수정 사항을 준비한 다음 이를 모듈 개발자에게 풀 리퀘스트(pull request)로 보내고 싶을 때 사용할 수 있습니다.
*   새로운 모듈을 빌드 중이며 아직 게시하지 않아, `go get` 명령어가 접근할 수 있는 저장소에서 사용할 수 없는 경우입니다.

### 로컬 디렉토리의 모듈 코드 require 하기 {#local_directory}

필수 모듈의 코드가 이를 필요로 하는 코드와 동일한 로컬 드라이브에 있음을 지정할 수 있습니다. 다음과 같은 상황에서 이 기능이 유용할 수 있습니다.

*   별도의 모듈을 개발 중이며, 현재 모듈에서 이를 테스트하고 싶은 경우.
*   외부 모듈의 문제를 수정하거나 기능을 추가하고 있으며, 현재 모듈에서 이를 테스트하고 싶은 경우. (외부 모듈을 직접 포크(fork)한 저장소에서 가져와 사용할 수도 있습니다. 자세한 내용은 [본인의 저장소 포크에서 외부 모듈 코드 가져오기](#external_fork)를 참조하세요.)

Go 명령어가 모듈 코드의 로컬 복사본을 사용하도록 하려면, `go.mod` 파일의 `replace` 지시어를 사용하여 `require` 지시어에 지정된 모듈 경로를 대체하십시오. 지시어에 대한 자세한 내용은 [go.mod reference](/doc/modules/gomod-ref)를 참조하십시오.

다음 `go.mod` 파일 예시에서, 현재 모듈은 외부 모듈인 `example.com/theirmodule`을 필요로 합니다. 이때 `replace` 지시문이 올바르게 작동하는지 확인하기 위해 존재하지 않는 버전 번호(`v0.0.0-unpublished`)가 사용되었습니다. 이후 `replace` 지시문은 원래의 모듈 경로를 현재 모듈의 디렉토리와 동일한 수준에 있는 디렉토리인 `../theirmodule`로 대체합니다.

```
module example.com/mymodule

go 1.23.0

require example.com/theirmodule v0.0.0-unpublished

replace example.com/theirmodule v0.0.0-unpublished => ../theirmodule
```

`require`/`replace` 쌍을 설정할 때는 [`go mod edit`](/ref/mod#go-mod-edit) 및 [`go get`](/ref/mod#go-get) 명령어를 사용하여 파일에 기술된 요구 사항이 일관되게 유지되도록 하십시오.

```
$ go mod edit -replace=example.com/theirmodule@v0.0.0-unpublished=../theirmodule
$ go get example.com/theirmodule@v0.0.0-unpublished
```

**참고:** `replace` 지시문을 사용하면, Go 도구는 [의존성 추가하기](#adding_dependency)에서 설명한 방식대로 외부 모듈을 인증하지 않습니다.

버전 번호에 대한 자세한 내용은 [Module version numbering](/doc/modules/version-numbers)을 참조하십시오.

Go 1.18에는 여러 모듈을 동시에 작업할 수 있게 해주는 [워크스페이스 모드](/blog/get-familiar-with-workspaces)가 추가되었습니다. [튜토리얼: 멀티 모듈 워크스페이스 시작하기](/doc/tutorial/workspaces)를 참고하세요.

### 자신의 리포지토리 포크에서 외부 모듈 코드 가져오기 {#external_fork}

외부 모듈의 저장소를 포크한 경우(예: 모듈 코드의 문제를 수정하거나 기능을 추가하기 위해), Go 도구가 해당 모듈의 소스로 사용자의 포크 버전을 사용하도록 설정할 수 있습니다. 이는 자신의 코드에서 변경 사항을 테스트할 때 유용합니다.
(참고로, 모듈을 요구하는 위치와 동일한 로컬 드라이브의 디렉토리에 있는 모듈 코드를 요구할 수도 있습니다. 자세한 내용은 [로컬 디렉토리의 모듈 코드 요구하기](#local_directory)를 참조하십시오.)

이는 `go.mod` 파일에서 `replace` 지시어를 사용하여 외부 모듈의 원래 모듈 경로를 사용자 저장소에 있는 포크(fork) 경로로 대체함으로써 수행할 수 있습니다. 이렇게 하면 컴파일 시 Go 도구가 대체 경로(포크된 위치)를 사용하게 되며, 예를 들어 `import` 문은 원래 모듈 경로 그대로 유지할 수 있습니다.

`replace` 지시문에 대한 자세한 내용은 [go.mod 파일 참조](gomod-ref)를 확인하세요.

다음 `go.mod` 파일 예시에서, 현재 모듈은 외부 모듈인 `example.com/theirmodule`을 필요로 합니다. 이때 `replace` 지시문은 원래의 모듈 경로를 해당 모듈 저장소의 포크 버전인 `example.com/myfork/theirmodule`로 대체합니다.

```
module example.com/mymodule

go 1.23.0

require example.com/theirmodule v1.2.3

replace example.com/theirmodule v1.2.3 => example.com/myfork/theirmodule v1.2.3-fixed
```

`require`/`replace` 쌍을 설정할 때는 파일에 기술된 요구 사항들이 일관되게 유지되도록 Go 툴 명령어를 사용하십시오. [`go list`](/ref/mod#go-list-m) 명령어를 사용하여 현재 모듈에서 사용 중인 버전을 확인하십시오. 그 다음 [`go mod edit`](/ref/mod#go-mod-edit) 명령어를 사용하여 요구되는 모듈을 포크(fork)된 버전으로 교체하십시오.

```
$ go list -m example.com/theirmodule
example.com/theirmodule v1.2.3
$ go mod edit -replace=example.com/theirmodule@v1.2.3=example.com/myfork/theirmodule@v1.2.3-fixed
```

**참고:** `replace` 지시문을 사용할 때, Go 도구는 [의존성 추가](#adding_dependency) 섹션에 설명된 대로 외부 모듈을 인증하지 않습니다.

버전 번호에 대한 자세한 내용은 [Module version numbering](/doc/modules/version-numbers)을 참조하십시오.

## 저장소 식별자를 사용하여 특정 커밋 가져오기 {#repo_identifier}

`go get` 명령어를 사용하여 리포지토리의 특정 커밋으로부터 모듈의 게시되지 않은 코드를 추가할 수 있습니다.

이를 위해 `go get` 명령어를 사용하며, `@` 기호를 통해 원하는 코드를 지정합니다. `go get`을 사용하면, 해당 명령어는 커밋 상세 정보를 기반으로 한 pseudo-version 번호를 사용하여 외부 모듈을 필요로 하는 `require` 지시문을 go.mod 파일에 추가합니다.

다음 예제들은 몇 가지 사례를 제공합니다. 이 예제들은 소스 코드가 git 저장소에 있는 모듈을 기반으로 합니다.

*   특정 커밋의 모듈을 가져오려면 `@<em>commithash</em>` 형식을 추가하십시오:

```
    $ go get example.com/theirmodule@4cf76c2
    ```

*   특정 브랜치의 모듈을 가져오려면 `@<em>branchname</em>` 형식을 추가하세요:

```
    $ go get example.com/theirmodule@bugfixes
    ```

## 의존성 제거하기 {#removing_dependency}

코드에서 모듈의 어떤 패키지도 더 이상 사용하지 않는 경우, 해당 모듈을 의존성으로 추적하는 것을 중단할 수 있습니다.

사용하지 않는 모든 모듈의 추적을 중단하려면 [`go mod tidy` 명령](/ref/mod#go-mod-tidy)을 실행하세요. 이 명령은 모듈의 패키지를 빌드하는 데 필요한 누락된 종속성을 추가할 수도 있습니다.

```
$ go mod tidy
```

특정 의존성을 제거하려면, 다음 예시와 같이 모듈의 모듈 경로를 지정하고 뒤에 `@none`을 추가하여 [`go get` 명령](/ref/mod#go-get)을 사용하십시오.

```
$ go get example.com/theirmodule@none
```

`go get` 명령어는 제거된 모듈에 의존하는 다른 의존성들을 함께 다운그레이드하거나 제거합니다.

## 도구 의존성 {#tools}

도구 의존성(Tool dependencies)을 사용하면 Go로 작성되었으며 모듈 작업 시 사용되는 개발 도구들을 관리할 수 있습니다. 예를 들어, [`go generate`](/blog/generate)와 함께 [`stringer`](https://pkg.go.dev/golang.org/x/tools/cmd/stringer)를 사용하거나, 변경 사항을 제출하기 위해 준비하는 과정의 일부로 특정 린터(linter)나 포매터(formatter)를 사용할 수 있습니다.

Go 1.24 이상부터는 다음과 같이 도구 의존성(tool dependency)을 추가할 수 있습니다:

```
$ go get -tool golang.org/x/tools/cmd/stringer
```

이 작업은 `go.mod` 파일에 [`tool` 지시어](/ref/mod/#go-mod-file-tool)를 추가하며, 필요한 `require` 지시어들이 포함되어 있는지 확인합니다. 이 지시어가 추가되면, 도구 임포트 경로의 마지막 [비주 버전(non-major-version)](/ref/mod#major-version-suffixes) 구성 요소를 `go tool`에 전달하여 도구를 실행할 수 있습니다.

```
$ go tool stringer
```

여러 도구가 마지막 경로 조각(path fragment)을 공유하거나, 경로 조각이 Go 배포판에 포함된 도구 중 하나와 일치하는 경우에는 전체 패키지 경로를 전달해야 합니다:

```
$ go tool golang.org/x/tools/cmd/stringer
```

현재 사용 가능한 모든 도구 목록을 확인하려면, 인자 없이 `go tool`을 실행하십시오:

```
$ go tool
```

`go.mod` 파일에 `tool` 지시문을 수동으로 추가할 수 있지만, 해당 도구를 정의하는 모듈에 대한 `require` 지시문이 반드시 있어야 합니다. 누락된 `require` 지시문을 추가하는 가장 쉬운 방법은 다음 명령어를 실행하는 것입니다:

```
$ go mod tidy
```

도구 의존성(tool dependencies)을 충족하기 위해 필요한 요구 사항은 [모듈 그래프](/ref/mod#glos-module-graph)의 다른 일반적인 요구 사항과 동일하게 동작합니다. 이들은 [최소 버전 선택](/ref/mod#minimal-version-selection) 과정에 참여하며 `require`, `replace`, `exclude` 지시문을 준수합니다. 모듈 가지치기(module pruning)로 인해, 도구 의존성을 가진 모듈에 의존하는 경우, 해당 도구 의존성을 충족하기 위해서만 존재하는 요구 사항은 일반적으로 사용자의 모듈 요구 사항이 되지 않습니다.

`tool` [메타 패턴](/cmd/go#hdr-Package_lists_and_patterns)은 모든 도구에 대해 동시에 작업을 수행하는 방법을 제공합니다. 예를 들어, `go get tool`을 사용하여 모든 도구를 업그레이드할 수 있으며, 이는 `go get tool@upgrade`와 동일합니다. 또는 `go install tool`을 사용하여 모든 도구를 $GOBIN에 설치할 수 있습니다.

Go 1.24 이전 버전에서는 [빌드 제약 조건](/pkg/go/build/#hdr-Build_Constraints)을 사용하여 빌드에서 제외된 모듈 내 go 파일에 빈 임포트(blank import)를 추가함으로써 `tool` 지시어와 유사한 기능을 구현할 수 있습니다. 이렇게 하면 전체 패키지 경로와 함께 `go run`을 사용하여 해당 도구를 실행할 수 있습니다.

## 모듈 프록시 서버 지정하기 {#proxy_server}

Go 도구를 사용하여 모듈로 작업할 때, 도구는 기본적으로 proxy.golang.org(Google에서 운영하는 공개 모듈 미러)에서 모듈을 다운로드하거나 모듈 저장소에서 직접 다운로드합니다. Go 도구가 모듈 다운로드 및 인증을 위해 대신 다른 프록시 서버를 사용하도록 지정할 수 있습니다.

본인(또는 팀)이 사용하려는 별도의 모듈 프록시 서버를 설정했거나 선택한 경우 이 작업을 수행하고 싶을 수 있습니다. 예를 들어, 일부 사용자는 종속성 사용 방식을 더 세밀하게 제어하기 위해 모듈 프록시 서버를 설정합니다.

Go 도구에서 사용할 다른 모듈 프록시 서버를 지정하려면, `GOPROXY` 환경 변수를 하나 이상의 서버 URL로 설정하십시오. Go 도구는 지정한 순서대로 각 URL을 시도합니다. 기본적으로 `GOPROXY`는 Google에서 운영하는 공용 모듈 프록시를 먼저 지정하고, 그다음 모듈 저장소(모듈 경로에 지정됨)에서 직접 다운로드하도록 설정되어 있습니다.

```
GOPROXY="https://proxy.golang.org,direct"
```

`GOPROXY` 환경 변수 및 다른 동작을 지원하는 값들에 대한 자세한 내용은 [`go` 커맨드
참조](/cmd/go/#hdr-Module_downloading_and_verification)를 확인하세요.

이 변수를 다른 모듈 프록시 서버의 URL로 설정할 수 있으며, URL은 쉼표(,) 또는 파이프(|) 기호로 구분합니다.

*   쉼표를 사용하는 경우, Go 도구는 현재 URL이 HTTP 404 또는 410을 반환할 때만 목록의 다음 URL을 시도합니다.

```
    GOPROXY="https://proxy.example.com,https://proxy2.example.com"
    ```

*   파이프(`|`)를 사용하면 Go 도구는 HTTP 오류 코드와 상관없이 목록의 다음 URL을 시도합니다.

```
    GOPROXY="https://proxy.example.com|https://proxy2.example.com"
    ```

Go 모듈은 퍼블릭 인터넷에서 사용할 수 없는 버전 관리 서버 및 모듈 프록시에서 빈번하게 개발되고 배포됩니다. `GOPRIVATE` 환경 변수를 설정하여 `go` 명령어가 프라이빗 소스에서 모듈을 다운로드하고 빌드하도록 구성할 수 있습니다.
그러면 go 명령어는 프라이빗 소스에서 모듈을 다운로드하고 빌드할 수 있게 됩니다.

`GOPRIVATE` 또는 `GONOPROXY` 환경 변수는 프라이빗하며 어떠한 프록시에서도 요청해서는 안 되는 모듈 접두사와 일치하는 글로브(glob) 패턴 목록으로 설정될 수 있습니다. 예를 들어:

```
GOPRIVATE=*.corp.example.com,*.research.example.com
```
