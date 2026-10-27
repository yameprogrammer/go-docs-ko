<!--{
  "Title": "go.mod 파일 레퍼런스"
}-->

`go.mod` 파일은 Go 모듈의 메인 정의 파일입니다. 이 파일은 모듈의 경로, Go 버전 및 의존성 목록을 정의합니다.

## 문법

`go.mod` 파일의 구문은 다음과 같습니다.

### module

`module` 지시어는 모듈의 경로를 정의합니다. 모듈 경로는 다른 모듈이 이 모듈을 가져올(import) 때 사용하는 식별자입니다.

```go
module example.com/my-module
```

### go

`go` 지시어는 모듈에 필요한 최소 Go 버전을 지정합니다.

```go
go 1.21
```

### require

`require` 지시어는 모듈이 의존하는 다른 모듈과 그 버전을 나열합니다.

```go
require (
    example.com/other-module v1.2.3
    github.com/google/uuid v1.3.0
)
```

단일 의존성만 있을 경우 괄호 없이 한 줄로 작성할 수 있습니다.

```go
require example.com/other-module v1.2.3
```

### exclude

`exclude` 지시어는 특정 버전의 모듈을 사용하지 않도록 설정합니다. 이는 버그가 있는 특정 버전을 피해야 할 때 유용합니다.

```go
exclude example.com/bad-module v1.1.0
```

### replace

`replace` 지시어는 의존성 경로를 다른 경로(예: 로컬 디렉토리)나 다른 버전으로 교체합니다. 이는 주로 라이브러리를 수정하여 테스트할 때 사용됩니다.

```go
// 특정 버전을 다른 버전으로 교체
replace example.com/module v1.0.0 => example.com/module v1.0.1

// 원격 모듈을 로컬 경로로 교체
replace example.com/module => ../local-module
```

## 버전 선택 (Version Selection)

Go는 **최소 버전 선택(Minimal Version Selection, MVS)** 알고리즘을 사용하여 의존성 그래프에서 사용할 모듈 버전을 결정합니다.

- `go.mod` 파일에 명시된 버전 중 가장 높은 버전이 선택됩니다.
- 간접 의존성(indirect dependencies)의 경우, `// indirect` 주석이 붙어 표시됩니다.

## 주요 명령어

`go.mod` 파일을 관리하기 위해 다음 명령어를 사용합니다.

| 명령어 | 설명 |
| :--- | :--- |
| `go mod init <module-path>` | 새로운 `go.mod` 파일을 생성하고 모듈을 초기화합니다. |
| `go mod tidy` | 사용하지 않는 의존성을 제거하고 누락된 의존성을 추가하여 `go.mod`와 `go.sum`을 최신 상태로 유지합니다. |
| `go mod vendor` | 의존성 패키지들을 프로젝트 내의 `vendor` 디렉토리에 복사합니다. |
| `go mod download` | 의존성 모듈을 로컬 캐시에 다운로드합니다. |
| `go mod verify` | 다운로드된 의존성이 수정되지 않았는지 검증합니다. |

각 Go 모듈은 다른 모듈 및 Go 버전에 대한 의존성을 포함하여 모듈의 속성을 기술하는 `go.mod` 파일에 의해 정의됩니다.

이러한 속성에는 다음이 포함됩니다:

* 현재 모듈의 **module path**입니다. 이는 모듈 코드의 저장소 위치와 같이 Go 도구가 모듈을 다운로드할 수 있는 위치여야 합니다. 이는 모듈의 버전 번호와 결합되어 고유 식별자 역할을 합니다. 또한 모듈 내 모든 패키지 경로의 접두사가 됩니다. Go가 모듈을 찾는 방법에 대한 자세한 내용은 <a href="/ref/mod#vcs-find">Go Modules Reference</a>를 참조하십시오.
* 현재 모듈에 필요한 최소 **version of Go**입니다.
* 현재 모듈에서 **required**하는 다른 모듈들의 최소 버전 목록입니다.
* 선택적으로, 필요한 모듈을 다른 모듈 버전이나 로컬 디렉터리로 **replace**하거나, 필요한 모듈의 특정 버전을 **exclude**하거나, 패키지 패턴을 매칭할 때 모듈 내의 특정 디렉터리를 **ignore**하는 지침입니다.

[`go mod init` 명령](/ref/mod#go-mod-init)을 실행하면 Go가 go.mod 파일을 생성합니다. 다음 예제는 모듈 경로를 example/mymodule로 설정하여 go.mod 파일을 생성하는 방법입니다.

```
$ go mod init example/mymodule
```

`go` 명령어를 사용하여 종속성을 관리하세요. 이 명령어들은 `go.mod` 파일에 기술된 요구 사항이 일관되게 유지되고 `go.mod` 파일의 내용이 유효하도록 보장합니다. 이러한 명령어에는 [`go get`](/ref/mod#go-get), [`go mod tidy`](/ref/mod#go-mod-tidy) 및 [`go mod edit`](/ref/mod#go-mod-edit) 명령어가 포함됩니다.

`go` 명령어에 대한 참조는 [Command go](/cmd/go/)를 확인하세요.
`go help mod tidy`와 같이 커맨드 라인에서 `go help` _명령어-이름_을 입력하여 도움말을 얻을 수 있습니다.

**함께 보기**

* Go 도구는 의존성을 관리하는 동안 `go.mod` 파일을 자동으로 변경합니다. 자세한 내용은 [의존성 관리](/doc/modules/managing-dependencies)를 참조하세요.
* `go.mod` 파일과 관련된 더 자세한 내용 및 제약 사항은 [Go 모듈 참조](/ref/mod#go-mod-file)를 참조하세요.

## 예제 {#example}

`go.mod` 파일에는 다음 예제와 같이 지시문(directives)이 포함됩니다. 이에 대한 자세한 설명은 이 주제의 다른 섹션에서 다룹니다.

```
module example.com/mymodule

go 1.14

require (
    example.com/othermodule v1.2.3
    example.com/thismodule v1.2.3
    example.com/thatmodule v1.2.3
)

replace example.com/thatmodule => ../thatmodule
exclude example.com/thismodule v1.3.0
```

## module {#module}

모듈의 모듈 경로(module path)를 선언합니다. 모듈 경로는 (모듈 버전 번호와 결합되었을 때) 모듈의 고유 식별자가 됩니다. 모듈 경로는 해당 모듈에 포함된 모든 패키지의 import 접두사가 됩니다.

자세한 내용은 Go 모듈 참조의 [`module` 지시어](/ref/mod#go-mod-file-module)를 확인하세요.

### Syntax {#module-syntax}

<pre>module <var>module-path</var></pre>

<dl>
    <dt>module-path</dt>
    <dd>모듈의 모듈 경로로, 일반적으로 Go 도구를 통해 모듈을 다운로드할 수 있는 저장소 위치입니다. v2 이상의 모듈 버전의 경우, 이 값은 <code>/v2</code>와 같이 주 버전 번호로 끝나야 합니다.</dd>
</dl>

### 예제 {#module-examples}

다음 예제들은 모듈을 다운로드할 수 있는 리포지토리 도메인을 `example.com`으로 대체하여 표시합니다.

* v0 또는 v1 모듈의 모듈 선언:
  ```
  module example.com/mymodule
  ```
* v2 모듈의 모듈 경로:
  ```
  module example.com/mymodule/v2
  ```

### 참고 사항 {#module-notes}

모듈 경로는 모듈을 고유하게 식별해야 합니다. 대부분의 모듈의 경우, 경로는 `go` 명령어가 코드를 찾을 수 있는 URL(또는 코드로 연결되는 리다이렉트 주소)입니다. 직접 다운로드될 일이 없는 모듈의 경우, 모듈 경로는 고유성을 보장할 수 있는 사용자가 제어하는 임의의 이름일 수 있습니다. `example/` 접두사는 이와 같은 예제에서 사용하기 위해 예약되어 있습니다.

더 자세한 내용은 [의존성 관리](/doc/modules/managing-dependencies#naming_module)를 참조하십시오.

실제로 모듈 경로는 일반적으로 모듈 소스의 저장소 도메인과 저장소 내 모듈 코드까지의 경로로 구성됩니다. `go` 명령어는 모듈 사용자를 대신하여 의존성을 해결하기 위해 모듈 버전을 다운로드할 때 이 형식을 사용합니다.

처음에는 모듈을 다른 코드에서 사용할 수 있도록 제공할 의도가 없더라도, 저장소 경로(repository path)를 사용하는 것이 가장 좋습니다. 이렇게 하면 나중에 모듈을 게시하게 되었을 때 모듈 이름을 변경해야 하는 상황을 피할 수 있습니다.

모듈의 최종 저장소 위치를 처음부터 알지 못하는 경우, 본인 소유의 도메인 이름이나 제어 가능한 이름(예: 회사 이름)을 모듈 이름 또는 소스 디렉터리 뒤에 경로를 붙여 임시로 안전한 대체제로 사용하는 것을 고려하십시오. 자세한 내용은 [의존성 관리](/doc/modules/managing-dependencies#naming_module)를 참조하십시오.

예를 들어, `stringtools` 디렉토리에서 개발 중이라면, 다음 예시와 같이 임시 모듈 경로는 `<company-name>/stringtools`가 될 수 있습니다. 여기서 _company-name_은 귀사의 이름입니다.

```
go mod init <company-name>/stringtools
```

## go {#go}

해당 지시어(directive)에 의해 지정된 Go 버전의 시맨틱(semantics)을 가정하고 모듈이 작성되었음을 나타냅니다.

더 자세한 내용은 Go 모듈 참조(Go Modules Reference)의 [`go` 지시어](/ref/mod#go-mod-file-go)를 참조하십시오.

### 구문 {#go-syntax}

<pre>go <var>minimum-go-version</var></pre>

<dl>
    <dt>minimum-go-version</dt>
    <dd>이 모듈의 패키지를 컴파일하는 데 필요한 Go의 최소 버전입니다.</dd>
</dl>

### 예제 {#go-examples}

* 모듈은 Go 버전 1.14 이상에서 실행되어야 합니다:
  ```
  go 1.14
  ```

### 노트 {#go-notes}

`go` 지시문은 이 모듈을 사용하는 데 필요한 Go의 최소 버전을 설정합니다.
Go 1.21 이전에는 이 지시문이 권장 사항일 뿐이었으나, 이제는 필수 요구 사항입니다.
Go 툴체인은 더 최신 Go 버전을 선언한 모듈의 사용을 거부합니다.

`go` 지시문은 실행할 Go 툴체인을 선택하는 입력값으로 사용됩니다.
자세한 내용은 “[Go toolchains](/doc/toolchain)”를 참조하십시오.

`go` 지시문은 새로운 언어 기능의 사용에 영향을 줍니다:

* 모듈 내의 패키지에 대해, 컴파일러는 `go` 지시어에 의해 지정된 버전 이후에 도입된 언어 기능의 사용을 거부합니다. 예를 들어, 모듈에 `go 1.12` 지시어가 있다면, 해당 패키지들은 Go 1.13에서 도입된 `1_000_000`과 같은 숫자 리터럴을 사용할 수 없습니다.
* 이전 버전의 Go가 모듈의 패키지 중 하나를 빌드하다가 컴파일 에러가 발생하면, 해당 모듈이 더 최신 버전의 Go를 위해 작성되었다는 점을 에러 메시지에 명시합니다. 예를 들어, 모듈에 `go 1.13`이 지정되어 있고 패키지에서 숫자 리터럴 `1_000_000`을 사용하는 경우, 해당 패키지를 Go 1.12로 빌드하면 컴파일러는 이 코드가 Go 1.13을 위해 작성되었음을 알립니다.

`go` 지시문은 `go` 명령어의 동작에도 영향을 미칩니다:

* `go 1.14` 이상에서는 자동 [vendoring](/ref/mod#vendoring)이 활성화될 수 있습니다. `vendor/modules.txt` 파일이 존재하고 `go.mod`와 일치한다면, 명시적으로 `-mod=vendor` 플래그를 사용할 필요가 없습니다.
* `go 1.16` 이상에서 `all` 패키지 패턴은 [main module](/ref/mod#glos-main-module)의 패키지 및 테스트에서 전이적으로(transitively) 임포트된 패키지만과 일치합니다. 이는 모듈이 도입된 이후 [`go mod vendor`](/ref/mod#go-mod-vendor)에 의해 유지되는 패키지 집합과 동일합니다. 이전 버전에서 `all`은 메인 모듈의 패키지에 의해 임포트된 패키지의 테스트, 해당 패키지들의 테스트 등을 모두 포함했습니다.
* `go 1.17` 이상:
   * `go.mod` 파일은 메인 모듈의 패키지나 테스트에서 전이적으로 임포트된 패키지를 제공하는 각 모듈에 대해 명시적인 [`require` directive](/ref/mod#go-mod-file-require)를 포함합니다. (`go 1.16` 이하에서는 [minimal version selection](/ref/mod#minimal-version-selection)이 다른 버전을 선택하게 될 경우에만 간접 의존성이 포함되었습니다.) 이 추가 정보는 [module graph pruning](/ref/mod#graph-pruning) 및 [lazy module loading](/ref/mod#lazy-loading)을 가능하게 합니다.
   * 이전 `go` 버전보다 `// indirect` 의존성이 훨씬 더 많아질 수 있기 때문에, 간접 의존성은 `go.mod` 파일 내의 별도 블록에 기록됩니다.
   * `go mod vendor`는 벤더링된 의존성에 대한 `go.mod` 및 `go.sum` 파일을 생략합니다. (이를 통해 `vendor` 하위 디렉터리 내에서 `go` 명령어를 실행할 때 올바른 메인 모듈을 식별할 수 있습니다.)
   * `go mod vendor`는 각 의존성의 `go.mod` 파일에 명시된 `go` 버전을 `vendor/modules.txt`에 기록합니다.
* `go 1.21` 이상:
   * `go` 라인은 이 모듈과 함께 사용해야 하는 Go의 최소 요구 버전을 선언합니다.
   * `go` 라인은 모든 의존성의 `go` 라인보다 크거나 같아야 합니다.
   * `go` 명령어는 더 이상 이전의 오래된 Go 버전과의 호환성을 유지하려고 시도하지 않습니다.
   * `go` 명령어는 `go.sum` 파일 내의 `go.mod` 파일 체크섬을 유지하는 데 더 주의를 기울입니다.
<!-- If you update this list, also update /ref/mod#go-mod-file-go. -->

`go.mod` 파일에는 최대 하나의 `go` 지시문이 포함될 수 있습니다. 대부분의 명령어는 `go` 지시문이 없는 경우 현재 Go 버전으로 `go` 지시문을 추가합니다.

## toolchain {#toolchain}

이 모듈과 함께 사용할 권장 Go 툴체인을 선언합니다.
모듈이 메인 모듈이고 기본 툴체인이 권장 툴체인보다 오래된 경우에만 적용됩니다.

더 자세한 내용은 “[Go toolchains](/doc/toolchain)” 및 Go Modules Reference의 [`toolchain` directive](/ref/mod/#go-mod-file-toolchain)를 참조하십시오.

### 구문 {#toolchain-syntax}

<pre>toolchain <var>toolchain-name</var></pre>

<dl>
    <dt>toolchain-name</dt>
    <dd>제안된 Go 툴체인의 이름입니다. 표준 툴체인 이름은 Go 버전 <i>V</i>에 대해 <code>go<i>V</i></code> 형태를 가지며, 예시는 <code>go1.21.0</code> 및 <code>go1.18rc1</code>입니다.
      특수 값인 <code>default</code>는 자동 툴체인 전환을 비활성화합니다.</dd>
</dl>

### 예제 {#toolchain-examples}

* Go 1.21.0 또는 그 이상의 버전 사용을 권장합니다:
    ```
    toolchain go1.21.0
    ```

### 참고 사항 {#toolchain-notes}

`toolchain` 라인이 Go 툴체인 선택에 어떻게 영향을 미치는지에 대한 자세한 내용은 “[Go toolchains](/doc/toolchain)”를 참조하세요.

## godebug {#godebug}

이 모듈의 메인 패키지에 적용될 기본 [GODEBUG](/doc/godebug) 설정을 나타냅니다.
이 설정은 모든 툴체인 기본값을 덮어쓰며, 메인 패키지에 명시된 `//go:debug` 라인에 의해 다시 덮어쓰여집니다.

### 구문 {#godebug-syntax}

<pre>godebug <var>debug-key</var>=<var>debug-value</var></pre>

<dl>
    <dt>debug-key</dt>
    <dd>적용할 설정의 이름입니다.
      설정 목록과 해당 설정이 도입된 버전은
      <a href="/doc/godebug#history">GODEBUG History</a>에서 확인할 수 있습니다.
    </dd>
    <dt>debug-value</dt>
    <dd>설정에 제공되는 값입니다.
      별도로 지정되지 않은 경우, 해당 동작을 비활성화하려면 <code>0</code>을, 활성화하려면 <code>1</code>을 사용합니다.</dd>
</dl>

### 예제 {#godebug-examples}

* 새로운 1.23 `asynctimerchan=0` 동작을 사용하십시오:
  ```
  godebug asynctimerchan=0
  ```
* Go 1.21의 기본 GODEBUG 설정을 사용하되, 이전의 `panicnil=1` 동작을 사용하십시오:
  ```
  godebug (
      default=go1.21
      panicnil=1
  )
  ```

### 참고 사항 {#godebug-notes}

GODEBUG 설정은 현재 모듈의 main 패키지 빌드 및 테스트 바이너리에만 적용됩니다.
모듈이 의존성으로 사용될 때는 아무런 영향을 미치지 않습니다.

하위 호환성에 대한 자세한 내용은 “[Go, Backwards Compatibility, and GODEBUG](/doc/godebug)”를 참조하십시오.

## require {#require}

현재 모듈의 의존성으로 모듈을 선언하며, 필요한 모듈의 최소 버전을 지정합니다.

더 자세한 내용은 Go 모듈 참조의 [`require` 지시어](/ref/mod#go-mod-file-require)를 확인하세요.

### 구문 {#require-syntax}

<pre>require <var>module-path</var> <var>module-version</var></pre>

<dl>
    <dt>module-path</dt>
    <dd>모듈의 모듈 경로로, 일반적으로 모듈 소스의 저장소 도메인과 모듈 이름의 결합입니다. v2 이상의 모듈 버전의 경우, 이 값은 <code>/v2</code>와 같이 메이저 버전 번호로 끝나야 합니다.</dd>
    <dt>module-version</dt>
    <dd>모듈의 버전입니다. v1.2.3과 같은 릴리스 버전 번호이거나, v0.0.0-20200921210052-fa0125251cc4와 같이 Go에서 생성한 pseudo-version 번호일 수 있습니다.</dd>
</dl>

### 예제 {#require-examples}

* 출시된 버전 v1.2.3을 요구하는 경우:
    ```
    require example.com/othermodule v1.2.3
    ```
* Go 도구에 의해 생성된 의사 버전(pseudo-version) 번호를 사용하여 저장소에 아직 태그가 지정되지 않은 버전을 요구하는 경우:
    ```
    require example.com/othermodule v0.0.0-20200921210052-fa0125251cc4
    ```

### 참고 사항 {#require-notes}

`go get`와 같은 `go` 명령어를 실행하면, Go는 임포트된 패키지를 포함하는 각 모듈에 대해 `require` 지시문을 삽입합니다. 모듈이 아직 저장소에서 태그 지정되지 않은 경우, Go는 명령어를 실행할 때 생성한 의사 버전(pseudo-version) 번호를 할당합니다.

[`replace` 지시어](#replace)를 사용하면 Go가 저장소가 아닌 다른 위치에서 모듈을 가져오도록 설정할 수 있습니다.

버전 번호에 대한 자세한 내용은 [Module version numbering](/doc/modules/version-numbers)을 참조하십시오.

의존성 관리에 대한 자세한 내용은 다음을 참조하십시오.

* [의존성 추가하기](/doc/modules/managing-dependencies#adding_dependency)
* [특정 의존성 버전 가져오기](/doc/modules/managing-dependencies#getting_version)
* [사용 가능한 업데이트 확인하기](/doc/modules/managing-dependencies#discovering_updates)
* [의존성 업그레이드 또는 다운그레이드하기](/doc/modules/managing-dependencies#upgrading)
* [코드의 의존성 동기화하기](/doc/modules/managing-dependencies#synchronizing)

## tool {#tool}

현재 모듈의 종속성으로 패키지를 추가하며, 현재 작업 디렉토리가 이 모듈 내에 있을 때 `go tool`로 실행할 수 있도록 설정합니다.

### 구문 {#tool-syntax}

<pre>tool <var>package-path</var></pre>

<dl>
    <dt>package-path</dt>
    <dd>툴의 패키지 경로로, 툴을 포함하는 모듈과 모듈 내에서 툴을 구현하는 패키지로의 경로(비어 있을 수 있음)를 결합한 것입니다.</dd>
</dl>

### 예제 {#tool-examples}

* 현재 모듈에 구현된 도구를 선언하기:
    ```
    module example.com/mymodule
    ```

tool example.com/mymodule/cmd/mytool
    ```
* 별도의 모듈로 구현된 도구를 선언하는 방법:
    ```
    module example.com/mymodule

tool example.com/atool/cmd/atool

require example.com/atool v1.2.3
    ```

### 참고 사항 {#tool-notes}

`go tool`을 사용하여 전체 패키지 경로(fully qualified package path) 또는 모호함이 없는 경우 마지막 경로 세그먼트를 통해 모듈에 선언된 도구를 실행할 수 있습니다. 위의 첫 번째 예시에서 `go tool mytool` 또는 `go tool example.com/mymodule/cmd/mytool`을 실행할 수 있습니다.

워크스페이스 모드에서는 `go tool`을 사용하여 워크스페이스 내의 어떤 모듈에서든 선언된 도구를 실행할 수 있습니다.

도구는 모듈 자체와 동일한 모듈 그래프를 사용하여 빌드됩니다. 도구를 구현하는 모듈의 버전을 선택하려면 [`require` 지시문](#require)이 필요합니다. 모든 [`replace` 지시문](#replace) 또는 [`exclude` 지시문](#exclude) 또한 해당 도구와 그 의존성 항목들에 적용됩니다.

자세한 내용은 [Tool dependencies](/doc/modules/managing-dependencies#tools)를 참조하십시오.

## replace {#replace}

특정 버전(또는 모든 버전)의 모듈 콘텐츠를 다른 모듈 버전이나 로컬 디렉토리로 대체합니다. Go 도구는 의존성을 해결할 때 이 대체 경로를 사용합니다.

더 자세한 내용은 Go 모듈 레퍼런스의 [`replace` directive](/ref/mod#go-mod-file-replace)를 참조하십시오.

### 구문 {#replace-syntax}

<pre>replace <var>module-path</var> <var>[module-version]</var> => <var>replacement-path</var> <var>[replacement-version]</var></pre>

<dl>
    <dt>module-path</dt>
    <dd>교체할 모듈의 모듈 경로입니다.</dd>
    <dt>module-version</dt>
    <dd>선택 사항입니다. 교체할 특정 버전입니다. 이 버전 번호를 생략하면, 해당 모듈의 모든 버전이 화살표 오른쪽에 있는 내용으로 교체됩니다.</dd>
    <dt>replacement-path</dt>
    <dd>Go가 필요한 모듈을 찾을 경로입니다. 이는 모듈 경로이거나 교체 모듈이 있는 로컬 파일 시스템의 디렉토리 경로일 수 있습니다. 모듈 경로인 경우 <em>replacement-version</em> 값을 지정해야 합니다. 로컬 경로인 경우 <em>replacement-version</em> 값을 사용할 수 없습니다.</dd>
    <dt>replacement-version</dt>
    <dd>교체 모듈의 버전입니다. <em>replacement-path</em>가 모듈 경로(로컬 디렉토리가 아님)인 경우에만 교체 버전을 지정할 수 있습니다.</dd>
</dl>

### 예제 {#replace-examples}

* 모듈 저장소의 포크(fork)로 교체하기

다음 예제에서는 `example.com/othermodule`의 모든 버전이 지정된 코드 포크(fork)로 대체됩니다.

```
  require example.com/othermodule v1.2.3
```

replace example.com/othermodule => example.com/myfork/othermodule v1.2.3-fixed
  ```

한 모듈 경로를 다른 경로로 교체할 때, 교체 대상이 되는 모듈 내 패키지들의 import 문은 변경하지 마십시오.

모듈 코드의 포크(forked) 복사본 사용에 대한 자세한 내용은 [자신의 리포지토리 포크에서 외부 모듈 코드 요구하기](/doc/modules/managing-dependencies#external_fork)를 참조하세요.

* 다른 버전 번호로 교체하기

다음 예제는 모듈의 다른 버전 대신 v1.2.3 버전을 사용해야 함을 지정합니다.

```
  require example.com/othermodule v1.2.2
```

replace example.com/othermodule => example.com/othermodule v1.2.3
  ```

다음 예제는 모듈 버전 `v1.2.5`를 동일한 모듈의 버전 `v1.2.3`으로 교체합니다.

```
  replace example.com/othermodule v1.2.5 => example.com/othermodule v1.2.3
  ```

* 로컬 코드로 교체

다음 예제는 모든 버전의 모듈을 대체하여 로컬 디렉토리를 사용하도록 지정하는 방법을 보여줍니다.

```
  require example.com/othermodule v1.2.3
```

replace example.com/othermodule => ../othermodule
  ```

다음 예제는 v1.2.5에 대해서만 로컬 디렉토리를 대체제로 사용하도록 지정합니다.

```
  require example.com/othermodule v1.2.5
```

replace example.com/othermodule v1.2.5 => ../othermodule
  ```

모듈 코드의 로컬 복사본 사용에 대한 자세한 내용은 [로컬 디렉토리의 모듈 코드 요구하기](/doc/modules/managing-dependencies#local_directory)를 참조하십시오.

### 참고 사항 {#replace-notes}

`replace` 지시어를 사용하면 Go가 모듈 소스를 찾을 때 다른 경로를 사용하도록 모듈 경로 값을 일시적으로 다른 값으로 대체할 수 있습니다. 이는 Go의 모듈 검색 방향을 대체 경로의 위치로 리다이렉션하는 효과가 있습니다. 대체 경로를 사용하기 위해 패키지 import 경로를 변경할 필요는 없습니다.

현재 모듈을 빌드할 때 `exclude` 및 `replace` 지시문을 사용하여 빌드 타임의 의존성 해결을 제어하십시오. 이러한 지시문은 현재 모듈에 의존하는 다른 모듈에서는 무시됩니다.

`replace` 지시어는 다음과 같은 상황에서 유용하게 사용할 수 있습니다:

* 아직 저장소에 코드가 반영되지 않은 새로운 모듈을 개발 중이며, 로컬 버전을 사용하여 클라이언트와 함께 테스트하려는 경우.
* 의존성 라이브러리에서 문제를 발견하여 해당 저장소를 클론했고, 로컬 저장소에서 수정 사항을 테스트하려는 경우.

`replace` 지시문만으로는 [모듈 그래프](/ref/mod#glos-module-graph)에 모듈이 추가되지 않는다는 점에 유의하십시오. 메인 모듈의 `go.mod` 파일이나 종속성 모듈의 `go.mod` 파일에 대체된 모듈 버전을 참조하는 [`require` 지시문](#require)이 함께 필요합니다. 대체할 특정 버전이 없는 경우, 아래 예시와 같이 가짜 버전을 사용할 수 있습니다. `replace` 지시문은 메인 모듈에서만 적용되므로, 이 방식은 귀하의 모듈에 의존하는 다른 모듈들을 망가뜨릴 수 있다는 점에 유의하십시오.

```
require example.com/mod v0.0.0-replace

replace example.com/mod v0.0.0-replace => ./mod
```

필수 모듈을 교체하는 방법(Go 도구를 사용하여 변경하는 방법 포함)에 대한 자세한 내용은 다음을 참조하십시오:

* [본인의 저장소에서 포크(fork)한 외부 모듈 코드 가져오기](/doc/modules/managing-dependencies#external_fork)
* [로컬 디렉터리의 모듈 코드 가져오기](/doc/modules/managing-dependencies#local_directory)

버전 번호에 대한 자세한 내용은 [Module version numbering](/doc/modules/version-numbers)을 참조하세요.

## exclude {#exclude}

현재 모듈의 의존성 그래프에서 제외할 모듈 또는 모듈 버전을 지정합니다.

자세한 내용은 Go Modules Reference의 [`exclude` directive](/ref/mod#go-mod-file-exclude)를 참조하십시오.

### 구문 {#exclude-syntax}

<pre>exclude <var>module-path</var> <var>module-version</var></pre>

<dl>
    <dt>module-path</dt>
    <dd>제외할 모듈의 모듈 경로입니다.</dd>
    <dt>module-version</dt>
    <dd>제외할 특정 버전입니다.</dd>
</dl>

### 예제 {#exclude-example}

* example.com/theirmodule 버전 v1.3.0 제외

```
  exclude example.com/theirmodule v1.3.0
  ```

### Notes {#exclude-notes}

`exclude` 지시어를 사용하여 간접적으로 필요하지만 어떤 이유로든 로드할 수 없는 모듈의 특정 버전을 제외하십시오. 예를 들어, 체크섬(checksum)이 잘못된 모듈 버전을 제외하는 데 사용할 수 있습니다.

현재 모듈(빌드 중인 메인 모듈)을 빌드할 때, `exclude` 및 `replace` 지시어를 사용하여 빌드 시간의 의존성 해결(dependency resolution)을 제어하십시오. 이 지시어들은 현재 모듈에 의존하는 다른 모듈에서는 무시됩니다.

다음 예제와 같이 [`go mod edit`](/ref/mod#go-mod-edit) 명령어를 사용하여 모듈을 제외할 수 있습니다.

```
go mod edit -exclude=example.com/theirmodule@v1.3.0
```

버전 번호에 대한 자세한 내용은
[Module version numbering](/doc/modules/version-numbers)을(를) 참조하십시오.

## retract {#retract}

`go.mod`에 정의된 모듈의 특정 버전 또는 버전 범위에 대해 의존해서는 안 됨을 나타냅니다. `retract` 지시문은 버전이 너무 일찍 게시되었거나, 게시 후 심각한 문제가 발견되었을 때 유용합니다.

더 자세한 내용은 Go 모듈 참조의 [`retract` directive](/ref/mod#go-mod-file-retract)를 확인하세요.

### 구문 {#retract-syntax}

<pre>
retract <var>version</var> // <var>rationale</var>
retract [<var>version-low</var>,<var>version-high</var>] // <var>rationale</var>
</pre>

<dl>
  <dt>version</dt>
  <dd>철회할 단일 버전입니다.</dd>
  <dt>version-low</dt>
  <dd>철회할 버전 범위의 하한선입니다.</dd>
  <dt>version-high</dt>
  <dd>
    철회할 버전 범위의 상한선입니다. <var>version-low</var>와
    <var>version-high</var> 모두 범위에 포함됩니다.
  </dd>
  <dt>rationale</dt>
  <dd>
    철회 이유를 설명하는 선택적 코멘트입니다. 사용자에게 보내는 메시지에
    표시될 수 있습니다.
  </dd>
</dl>

### 예제 {#retract-example}

* 단일 버전 회수하기

```
  retract v1.1.0 // 실수로 게시됨.
  ```

* 버전 범위 회수(Retracting a range of versions)

```
  retract [v1.0.0,v1.0.5] // 일부 플랫폼에서 빌드 오류 발생.
  ```

### 참고 사항 {#retract-notes}

`retract` 지시어를 사용하여 모듈의 이전 버전을 사용하지 말아야 함을 나타내십시오. 사용자는 `go get`, `go mod tidy` 또는 다른 명령어를 통해 회수된(retracted) 버전으로 자동 업그레이드되지 않습니다. 또한 사용자는 `go list -m -u`를 실행했을 때 회수된 버전을 사용 가능한 업데이트로 보지 않게 됩니다.

철회된(Retracted) 버전은 이미 해당 버전에 의존하고 있는 사용자가 패키지를 빌드할 수 있도록 계속 제공되어야 합니다. 철회된 버전이 소스 저장소에서 삭제되더라도, [proxy.golang.org](https://proxy.golang.org)와 같은 미러 사이트에서는 계속 제공될 수 있습니다. 철회된 버전에 의존하는 사용자는 관련 모듈에 대해 `go get` 또는 `go list -m -u`를 실행할 때 알림을 받을 수 있습니다.

`go` 명령어는 모듈의 최신 버전 내 `go.mod` 파일에 있는 `retract` 지시문을 읽어 철회된(retracted) 버전을 찾아냅니다. 최신 버전은 다음 우선순위에 따라 결정됩니다:

1. 가장 높은 릴리스 버전(있는 경우)
2. 가장 높은 프리릴리스 버전(있는 경우)
3. 저장소의 기본 브랜치 최신 지점(tip)에 대한 의사 버전(pseudo-version).

retraction을 추가할 때는 거의 항상 더 높은 버전의 새 태그를 지정해야 합니다. 그래야 명령어가 모듈의 최신 버전에서 해당 내용을 확인할 수 있기 때문입니다.

철회(retraction)를 알리는 것만을 목적으로 하는 버전을 게시할 수 있습니다. 이 경우, 새 버전이 자기 자신을 철회할 수도 있습니다.

예를 들어, 실수로 `v1.0.0` 태그를 지정한 경우, 다음 지시어를 사용하여 `v1.0.1` 태그를 지정할 수 있습니다.

```
retract v1.0.0 // 실수로 게시되었습니다.
retract v1.0.1 // 철회 내용만 포함되어 있습니다.
```

안타깝게도 버전이 한 번 게시되면 변경할 수 없습니다. 나중에 다른 커밋에 `v1.0.0` 태그를 지정하면, `go` 명령어가 `go.sum` 또는 [체크섬 데이터베이스](/ref/mod#checksum-database)에서 일치하지 않는 합계(sum)를 감지할 수 있습니다.

모듈의 철회된(Retracted) 버전은 보통 `go list -m -versions` 출력에 나타나지 않지만, `-retracted` 플래그를 사용하여 이를 표시할 수 있습니다.
자세한 내용은 Go 모듈 참조의 [`go list -m`](/ref/mod#go-list-m)을 확인하세요.

## ignore {#ignore}

`go` 명령어가 패키지 패턴을 매칭할 때 무시해야 할 모듈 내의 디렉터리 경로를 지정합니다.

더 자세한 내용은 Go 모듈 레퍼런스의 [`ignore` 지시문](/ref/mod#go-mod-file-ignore)을 참조하십시오.

### 구문 {#ignore-syntax}

<pre>
ignore <var>path</var>
</pre>

<dl>
  <dt>path</dt>
  <dd>
    무시할 슬래시(/) 구분 경로입니다. 경로가 <code>./</code>로 시작하면
    모듈 루트 디렉토리를 기준으로 상대 경로로 해석됩니다. 그렇지 않으면,
    모듈 내 어느 깊이에서든 해당 이름을 가진 모든 디렉토리가 무시됩니다.
  </dd>
</dl>

### 예제 {#ignore-examples}

* 모듈 루트를 기준으로 로컬 디렉터리를 무시합니다.

```
  ignore ./node_modules
  ```

* 모듈 내 어디서든 `generated`라는 이름의 모든 디렉터리를 무시합니다.

```
  ignore generated
  ```

* 블록을 사용하여 여러 경로 무시하기

```
  ignore (
      static
      content/html
      ./third_party/javascript
  )
  ```

### 참고 사항 {#ignore-notes}

`./...`와 같은 와일드카드 패턴을 사용할 때, `go` 명령어가 생성된 디렉토리나 Go 관련이 없는 디렉토리의 패키지를 매칭하지 않도록 하려면 `ignore` 지시어를 사용하십시오. 무시된 디렉토리와 그 내용은 패키지 패턴에서 제외되지만, 모듈 파일 트리에는 여전히 존재합니다.

`ignore` 지시문은 메인 모듈의 `go.mod` 파일에만 적용됩니다.
의존성 모듈의 `go.mod` 파일에서는 아무런 효과가 없습니다.
