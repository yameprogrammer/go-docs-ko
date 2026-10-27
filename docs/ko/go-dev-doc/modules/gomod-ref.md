<!--{
  "제목": "go.mod 파일 참조"
}-->

각 Go 모듈은 `go.mod` 파일로 정의되며, 이 파일은 모듈의 속성을 설명하고, 여기에는 다른 모듈 및 Go 버전과의 의존성이 포함됩니다.

다음 속성들을 포함합니다:

* 현재 모듈의 **모듈 경로**. Go 도구(예: 모듈 코드의 저장소 위치)에서 모듈을 다운로드할 수 있는 위치여야 합니다. 이는 모듈의 버전 번호와 함께 사용되어 고유한 식별자로 사용됩니다. 또한 모듈 내 모든 패키지의 패키지 경로의 접두사입니다. Go가 모듈을 찾는 방법에 대한 자세한 내용은 <a href="/ref/mod#vcs-find">Go 모듈 참조</a>를 참조하십시오.
* 현재 모듈이 요구하는 **최소 Go 버전**.
* 현재 모듈이 요구하는 다른 **모듈의 최소 버전 목록**.
* 필요한 모듈을 다른 모듈 버전 또는 로컬 디렉토리로 대체하거나, 특정 버전의 필요한 모듈을 제외하거나, 패키지 패턴 일치 시 모듈 내 특정 디렉토리를 무시하는 등의 **지침** (선택 사항).

Go는 `go mod init` 명령을 실행할 때 `go.mod` 파일을 생성합니다. 다음 예제는 `go.mod` 파일을 생성하고, 모듈의 모듈 경로를 `example/mymodule`로 설정합니다:

```
$ go mod init example/mymodule
```

`go` 명령어를 사용하여 의존성을 관리합니다. 이러한 명령들은 `go.mod` 파일에 설명된 요구 사항이 일관성을 유지하고, `go.mod` 파일의 내용이 유효하도록 보장합니다. 이러한 명령어에는 `go get` (`/ref/mod#go-get`), `go mod tidy` (`/ref/mod#go-mod-tidy`), 그리고 `go mod edit` (`/ref/mod#go-mod-edit`) 명령어가 포함됩니다.

참조용으로 `go` 명령어에 대한 내용은 [Command go](/cmd/go/)를 참조하십시오. `go help` 명령어를 사용하여 명령줄에서 도움을 받을 수 있습니다. 예를 들어 `go help mod tidy`와 같이 사용할 수 있습니다.

**참고**

* Go 도구는 의존성을 관리하기 위해 사용될 때 go.mod 파일을 변경합니다. 자세한 내용은 [의존성 관리](/doc/modules/managing-dependencies)를 참조하십시오.
* go.mod 파일과 관련된 자세한 내용 및 제약 사항은 [Go 모듈 참조](/ref/mod#go-mod-file)를 참조하십시오.

## 예제 {#example}

`go.mod` 파일에는 다음과 같이 지시문이 포함될 수 있습니다. 이러한 지시문은 이 주제의 다른 부분에서 설명됩니다.

```
모듈 example.com/mymodule

go 1.14

요구 사항 (
    example.com/othermodule v1.2.3
    example.com/thismodule v1.2.3
    example.com/thatmodule v1.2.3
)

example.com/thatmodule 를 대체하여 ../thatmodule 사용
example.com/thismodule v1.3.0 제외
```

## 모듈 {#module}

정의하는 것은 모듈의 모듈 경로, 즉 모듈의 고유 식별자입니다. (모듈 버전 번호와 함께 사용될 때). 모듈 경로가 모듈에 포함된 모든 패키지에 대한 임포트 프리픽스로 사용됩니다.

자세한 내용은 [`module` 지시문](/ref/mod#go-mod-file-module)을 Go Modules Reference에서 참조하십시오.

### 문법 {#module-syntax}

```
모듈 <var>모듈-경로</var>
```

```
<dl>
    <dt>module-path</dt>
    <dd>모듈의 모듈 경로. 일반적으로 Go 도구가 모듈을 다운로드할 수 있는 저장소 위치입니다. 모듈 버전 v2 및 이후 버전의 경우, 이 값은 주요 버전 번호로 끝나야 합니다 (예: <code/>v2</code/>).</dd>
</dl>
```

### 예제 {#module-예제}

다음 예시에서는 `example.com`을 모듈을 다운로드할 수 있는 저장소 도메인으로 대체합니다.

* v0 또는 v1 모듈에 대한 모듈 선언:
  ```
  module example.com/mymodule
  ```
* v2 모듈에 대한 모듈 경로:
  ```
  module example.com/mymodule/v2
  ```

### 참고 사항 {#module-참고}

모듈 경로는 고유하게 여러분의 모듈을 식별해야 합니다. 대부분의 모듈의 경우 경로는 `go` 명령이 코드를 찾을 수 있는 URL입니다 (또는 코드에 대한 리디렉션).

직접 다운로드되지 않을 모듈의 경우, 모듈 경로는 여러분이 제어하는 이름일 수 있으며, 이를 통해 고유성을 보장할 수 있습니다. `example/` 접두사는 이러한 예제와 같이 사용하도록 예약되어 있습니다.

자세한 내용은 [의존성 관리](/doc/modules/managing-dependencies#naming_module)를 참조하십시오.

실제로, 모듈 경로는 일반적으로 모듈 소스의 저장소 도메인과 저장소 내의 모듈 코드 경로입니다. `go` 명령은 모듈 사용자의 대신 종속성을 해결하기 위해 이 형식을 사용합니다.

물론, 처음에는 다른 코드에서 사용하도록 모듈을 공개할 계획이 없더라도, 저장소 경로를 사용하는 것은 좋은 방법입니다. 이는 나중에 모듈을 공개할 때 이름을 변경해야 하는 번거로움을 피하는 데 도움이 됩니다.

만약 초기에는 모듈의 최종 저장소 위치를 알 수 없는 경우, 다음과 같은 안전한 대체 이름을 임시로 사용해 보세요. 예를 들어, 자신이 소유한 도메인 이름이나 자신이 관리하는 이름(예: 회사 이름)과 모듈 이름이나 소스 디렉토리를 따르는 경로를 함께 사용하는 것입니다. 자세한 내용은 다음을 참조하세요: [의존성 관리](/doc/modules/managing-dependencies#naming_module).

예를 들어, `stringtools` 디렉토리에서 개발하는 경우, 임시 모듈 경로는 다음과 같은 예시와 같이 `<company-name>/stringtools`가 될 수 있습니다. 여기서 `<company-name>`은 귀사의 회사 이름입니다:

```
go mod init <회사 이름>/stringtools
```

## go {#go}

이것은 모듈이 지정된 지침에서 정의된 Go 버전의 의미를 기준으로 작성되었음을 나타냅니다.

자세한 내용은 `go` 지시어에 대한 [`go` directive](/ref/mod#go-mod-file-go)를 참조하십시오.

### 문법 {#go-syntax}

```go
go <var>최소-go-버전</var>
```

```markdown
<dl>
    <dt>최소 Go 버전</dt>
    <dd>이 모듈에서 패키지를 컴파일하는 데 필요한 최소 Go 버전.</dd>
</dl>
```

### 예시 {#go-예시}

* 모듈은 Go 버전 1.14 이상에서 실행되어야 합니다:
  ```
  go 1.14
  ```

### 참고 사항 {#go-참고}

`go` 지시문은 이 모듈을 사용하기 위해 필요한 최소 Go 버전을 설정합니다.
Go 1.21 이전에는 이 지시문은 권고 사항이었지만, 이제는 필수 요구 사항입니다:
Go 툴체인은 더 높은 Go 버전을 선언하는 모듈을 사용하지 않습니다.

`go` 지시어는 어떤 Go 도구 체인을 실행할지 선택하는 데 사용됩니다. 자세한 내용은 “[Go 도구 체인](/doc/toolchain)”를 참조하십시오.

`go` 지시어는 새로운 언어 기능 사용에 영향을 미칩니다:

* 모듈 내의 패키지에서는, `go` 지시어에 명시된 버전을 기준으로 도입된 언어 기능을 사용하려고 할 때 컴파일러가 오류를 발생시킵니다. 예를 들어, 모듈에 `go 1.12` 지시어가 지정된 경우, 해당 모듈의 패키지는 Go 1.13에 도입된 숫자 리터럴(예: `1_000_000`)을 사용할 수 없습니다.
* 이전 버전의 Go로 모듈의 패키지를 빌드하고 컴파일 오류가 발생하면, 오류 메시지는 해당 모듈이 더 새로운 버전의 Go를 대상으로 작성되었다고 나타냅니다. 예를 들어, 모듈에 `go 1.13`이 지정되어 있고, 패키지가 숫자 리터럴 `1_000_000`을 사용하는 경우, 해당 패키지를 Go 1.12로 빌드하면 컴파일러는 해당 코드가 Go 1.13을 대상으로 작성되었음을 알립니다.

`go` 지시어는 `go` 명령의 동작에도 영향을 미칩니다:

* `go 1.14` 이상 버전에서는 자동 [벤더링](/ref/mod#vendoring)이 활성화될 수 있습니다. `vendor/modules.txt` 파일이 존재하고 `go.mod` 파일과 일치하는 경우 `-mod=vendor` 플래그를 명시적으로 사용할 필요가 없습니다.
* `go 1.16` 이상 버전에서는 `all` 패키지 패턴은 [메인 모듈](/ref/mod#glos-main-module)에 있는 패키지와 테스트에서 트랜지티브로 가져온 패키지만 일치합니다. 이것은 모듈이 도입된 이후 `go mod vendor`로 유지되는 동일한 패키트 집합입니다. 이전 버전에서는 `all`은 메인 모듈에 있는 패키지와 해당 패키지의 테스트, 그리고 그 외에도 포함했습니다.
* `go 1.17` 이상 버전:
   * `go.mod` 파일에는 메인 모듈에 있는 패키지 또는 테스트에서 트랜지티브로 가져온 패키지를 제공하는 각 모듈에 대한 명시적인 `require` 지시문이 포함됩니다. (`go 1.16` 및 이전 버전에서는 간접 의존성이 선택되더라도 다른 버전을 선택하는 경우에만 포함됩니다.) 이 추가 정보는 [모듈 그래프 가지치기](/ref/mod#graph-pruning) 및 [지연 모듈 로딩](/ref/mod#lazy-loading)을 가능하게 합니다.
   * 이전 `go` 버전보다 훨씬 더 많은 `// indirect` 의존성이 있을 수 있으므로, 간접 의존성은 `go.mod` 파일 내의 별도의 블록에 기록됩니다.
   * `go mod vendor`는 벤더링된 의존성에 대한 `go.mod` 및 `go.sum` 파일을 제외합니다. (이를 통해 `vendor` 디렉토리 내의 하위 디렉토리에서 `go` 명령을 호출할 때 올바른 메인 모듈을 식별할 수 있습니다.)
   * `go mod vendor`는 각 의존성의 `go.mod` 파일에서 `go` 버전을 `vendor/modules.txt`에 기록합니다.
* `go 1.21` 이상 버전:
   * `go` 라인은 이 모듈을 사용하는 데 필요한 최소 Go 버전을 선언합니다.
   * `go` 라인은 모든 종속성의 `go` 라드보다 크거나 같아야 합니다.
   * `go` 명령어는 이전의 오래된 Go 버전과의 호환성을 유지하려고 하지 않습니다.
   * `go` 명령어는 `go.sum` 파일에 있는 `go.mod` 파일의 체크섬을 유지하는 데 더 신중합니다.
<!-- 이 목록을 업데이트할 때 /ref/mod#go-mod-file-go도 업데이트하십시오. -->

`go.mod` 파일에는 최대 하나의 `go` 지시문을 포함할 수 있습니다. 대부분의 명령은 현재 Go 버전의 `go` 지시문을 추가합니다(존재하지 않는 경우).

## 도구 체인 {#toolchain}

이 모듈과 함께 사용하기에 권장되는 Go 툴체인을 선언합니다.
이 효과는 모듈이 메인 모듈일 때만 발생하며, 기본 툴체인이 선언된 툴체인보다 오래된 경우에만 발생합니다.

자세한 내용은 "[Go 툴체인](/doc/toolchain)" 및
`toolchain` 지시어에 대해 Go Modules Reference에서 참조하십시오.

### 문법 {#toolchain-syntax}

```
toolchain <var>toolchain-name</var>
```

```
<dl>
    <dt>toolchain-name</dt>
    <dd>제안되는 Go 도구 체인의 이름입니다. 표준 도구 체인의 이름은 <code>go<i>V</i></code> 형식으로, Go 버전 <i>V</i>에 해당하며, 예시로 <code>go1.21.0</code> 및 <code>go1.18rc1</code>가 있습니다. 특수한 값 <code>default</code>는 자동 도구 체인 전환을 비활성화합니다.</dd>
</dl>
```

### 예제 {#toolchain-examples}

* 다음 버전 또는 이후 버전을 사용하는 것을 권장합니다:
    ```
    toolchain go1.21.0
    ```

### 참고 사항 {#toolchain-참고}

자세한 내용은 “[Go 툴체인](/doc/toolchain)”을 참조하십시오. `toolchain` 줄이 Go 툴체인 선택에 미치는 영향에 대한 정보가 포함되어 있습니다.

## godebug {#godebug}

이 모듈의 주요 패키지에 적용될 기본 [GODEBUG](/doc/godebug) 설정을 나타냅니다.
이 설정은 도구 체인의 기본 설정을 덮어쓰고, 메인 패키지에 있는 명시적인 `//go:debug` 줄에 의해 덮어써질 수 있습니다.

### 문법 {#godebug-문법}

```go
godebug <var>debug-key</var>=<var>debug-value</var>
```

```markdown
<dl>
    <dt>debug-key</dt>
    <dd>적용할 설정의 이름입니다.
      설정과 해당 설정이 도입된 버전에 대한 목록은 다음에서 확인할 수 있습니다.
      <a href="/doc/godebug#history">GODEBUG History</a>.
    </dd>
    <dt>debug-value</dt>
    <dd>설정에 제공되는 값입니다.
      그렇지 않은 경우, <code>0</code>를 사용하여 기능을 비활성화하고, <code>1</code>을 사용하여 기능을 활성화합니다.</dd>
</dl>
```

### 예제 {#godebug-examples}

* 새로운 1.23 `asynctimerchan=0` 동작 방식을 사용하십시오:
  ```
  godebug asynctimerchan=0
  ```
* Go 1.21의 기본 `GODEBUG`를 사용하지만, 이전의 `panicnil=1` 동작 방식을 사용하십시오:
  ```
  godebug (
      default=go1.21
      panicnil=1
  )
  ```

### 참고 사항 {#godebug-참고}

`GODEBUG` 설정은 현재 모듈 내의 메인 패키지와 테스트 바이너리에 적용됩니다.
모듈이 의존성으로 사용될 때는 효과가 없습니다.

자세한 내용은 “[Go, 역호환성 및 GODEBUG](/doc/godebug)”를 참조하십시오.

## require {#require}

현재 모듈에 모듈을 종속성으로 선언하고, 필요한 모듈의 최소 버전을 지정합니다.

자세한 내용은 `require` 지시어에 대해 참조하십시오: [`require` 지시어](/ref/mod#go-mod-file-require) Go Modules Reference에서.

### 구문 {#require-syntax}

```
require <var>모듈 경로</var> <var>모듈 버전</var>
```

```markdown
<dl>
    <dt>module-path</dt>
    <dd>모듈의 모듈 경로. 일반적으로 모듈 소스 저장소 도메인과 모듈 이름을 연결한 값입니다. v2 이상의 모듈 버전의 경우, 이 값은 주요 버전 번호로 끝나야 합니다 (예: `<code/>v2</code>`).</dd>
    <dt>module-version</dt>
    <dd>모듈의 버전입니다. 이는 릴리스 버전 번호 (예: v1.2.3) 또는 Go에서 생성된 가상 버전 번호 (예: v0.0.0-20200921210052-fa0125251cc4)일 수 있습니다.</dd>
</dl>
```

### 예시 {#require-examples}

* v1.2.3 버전이 출시된 것을 요구:
    ```
    require example.com/othermodule v1.2.3
    ```
* 저장소에 태그되지 않은 버전을 Go 도구에서 생성된 가상 버전 번호를 사용하여 요구:
    ```
    require example.com/othermodule v0.0.0-20200921210052-fa0125251cc4
    ```

### 참고 사항 {#require-notes}

`go` 명령 (예: `go get`)을 실행하면, Go는 가져온 패키지가 포함된 각 모듈에 대해 `require` 지시문을 삽입합니다. 모듈이 아직 저장소에 태그되지 않은 경우, Go는 해당 명령을 실행할 때 생성하는 가상 버전 번호를 할당합니다.

다음 명령어를 사용하여 Go가 저장소 외부의 위치에서 모듈을 요구할 수 있습니다: [`replace` 지시어](#replace).

더 자세한 내용은 [모듈 버전 번호](/doc/modules/version-numbers)를 참조하세요.

자세한 내용은 다음을 참조하십시오:

* [의존성 추가](/doc/modules/managing-dependencies#adding_dependency)
* [특정 의존성 버전 얻기](/doc/modules/managing-dependencies#getting_version)
* [사용 가능한 업데이트 확인하기](/doc/modules/managing-dependencies#discovering_updates)
* [의존성 업그레이드 또는 다운그레이드 하기](/doc/modules/managing-dependencies#upgrading)
* [코드의 의존성 동기화하기](/doc/modules/managing-dependencies#synchronizing)

## 도구 {#tool}

현재 모듈의 종속성으로 패키지를 추가하고, 현재 작업 디렉터리가 이 모듈 내에 있을 때 `go tool`을 사용하여 실행할 수 있도록 합니다.

### 문법 {#tool-syntax}

`<pre>tool <var>패키지-경로</var></pre>`

```markdown
<dl>
    <dt>package-path</dt>
    <dd>도구의 패키지 경로입니다. 이는 도구를 포함하는 모듈과 해당 모듈 내에서 도구를 구현하는 패키지의 (필요한 경우 비어 있는) 경로를 연결한 것입니다.</dd>
</dl>
```

### 예제 {#tool-examples}

* 현재 모듈에 구현된 도구를 선언하는 방법:
    ```
    module example.com/mymodule
    ```

```
* 별도의 모듈에 구현된 도구를 선언하는 방법:
    ```
    module example.com/mymodule
    ```

예시: tool.example.com/atool/cmd/atool

```
require example.com/atool v1.2.3

### 참고 사항 {#tool-참고}

`go tool` 명령어를 사용하여 모듈에 정의된 도구를 실행할 수 있습니다. 이를 위해 완전한 패키지 경로 또는, 모호성이 없을 경우 마지막 경로 세그먼트를 사용합니다. 위의 첫 번째 예제에서 `go tool mytool` 또는 `go tool example.com/mymodule/cmd/mytool`을 실행할 수 있습니다.

워크스페이스 모드에서는 `go tool`을 사용하여 워크스페이스 모듈에 정의된 도구를 실행할 수 있습니다.

이 도구는 자체 모듈의 동일한 모듈 그래프를 사용하여 구축됩니다. 도구가 구현하는 모듈의 버전을 선택하려면 [`require` 지시문](#require)이 필요합니다. 또한 [`replace` 지시문](#replace) 또는 [`exclude` 지시문](#exclude)도 도구 및 해당 종속성에 적용됩니다.

자세한 내용은 [도구 종속성](/doc/modules/managing-dependencies#tools) 참조하십시오.

## 대체: {#replace}

특정 버전(또는 모든 버전)의 모듈의 내용을 다른 모듈 버전 또는 로컬 디렉토리로 대체합니다. Go 도구는 종속성을 해결할 때 대체 경로를 사용합니다.

자세한 내용은 [`replace` 지침](/ref/mod#go-mod-file-replace)을 Go Modules Reference에서 참조하십시오.

### 구문 {#replace-syntax}

```
<var>module-path</var> <var>[module-version]</var> 를 <var>replacement-path</var> <var>[replacement-version]</var> 로 대체
```

```markdown
<dl>
    <dt>module-path</dt>
    <dd>대체할 모듈의 모듈 경로.</dd>
    <dt>module-version</dt>
    <dd>선택 사항. 대체할 특정 버전. 이 버전 번호가 지정되지 않으면, 화살표의 오른쪽 내용으로 모듈의 모든 버전이 대체됩니다.</dd>
    <dt>replacement-path</dt>
    <dd>Go가 필요한 모듈을 찾을 경로. 이는 모듈 경로이거나, 대체 모듈의 로컬 파일 시스템에 있는 디렉터리 경로일 수 있습니다. 만약 이것이 모듈 경로라면, <em replacement-version</em> 값을 지정해야 합니다. 만약 이것이 로컬 경로라면, <em replacement-version</em> 값을 사용할 수 없습니다.</dd>
    <dt>replacement-version</dt>
    <dd>대체 모듈의 버전. <em replacement-path</em> 가 모듈 경로(로컬 디렉터리가 아닌 경우)인 경우에만 <em replacement-version</em>이 지정될 수 있습니다.</dd>
</dl>
```

### 예시 {#replace-examples}

* 모듈 저장소의 포크를 사용하여 대체

다음 예시에서, example.com/othermodule의 모든 버전은 지정된 코드의 포크로 대체됩니다.

```
  require example.com/othermodule v1.2.3
```

```
example.com/othermodule => example.com/myfork/othermodule v1.2.3-fixed
```

하나의 모듈 경로를 다른 경로로 대체할 때, 대체하는 모듈의 패키지에 대한 import 문을 변경하지 마세요.

자체 저장소의 포크된 모듈 코드 사용에 대한 자세한 내용은 [자체 저장소에서 외부 모듈 코드 요구](/doc/modules/managing-dependencies#external_fork)를 참조하세요.

* 다른 버전 번호로 대체

다음 예시는 모듈의 다른 버전 대신 버전 v1.2.3을 사용하도록 지정합니다.

```
  require example.com/othermodule v1.2.2
```

```
example.com/othermodule v1.2.3

다음 예시는 동일한 모듈의 버전 v1.2.5를 버전 v1.2.3으로 대체합니다.

```
  대체 example.com/othermodule v1.2.5 => example.com/othermodule v1.2.3
  ```

* 로컬 코드 대체

다음 예시는 특정 로컬 디렉토리를 모듈의 모든 버전 대신 사용하도록 지정합니다.

```
  require example.com/othermodule v1.2.3
```

```
예: example.com/othermodule => ../othermodule
```

다음 예제는 특정 버전(v1.2.5)에 대해서만 로컬 디렉토리를 대체하도록 지정합니다.

```
  require example.com/othermodule@v1.2.5
```

```
example.com/othermodule v1.2.5 => ../othermodule
```

자세한 내용은 로컬 모듈 코드 사용에 대한 [로컬 디렉토리에서 모듈 코드 요구](/doc/modules/managing-dependencies#local_directory)를 참조하십시오.

### 참고 사항 {#replace-notes}

`replace` 지시어를 사용하여, Go가 다른 경로를 사용하여 모듈의 소스를 찾도록 하려면 모듈 경로 값을 임시로 다른 값으로 대체합니다. 이렇게 하면 Go의 모듈 검색을 대체 위치로 리디렉션하는 효과가 있습니다. 대체 경로를 사용하려면 패키지 가져오기 경로를 변경할 필요가 없습니다.

`exclude` 및 `replace` 지시문을 사용하여 현재 모듈을 빌드할 때 빌드 시간에 의존성 해결을 제어합니다. 이러한 지시문은 현재 모듈에 의존하는 모듈에서는 무시됩니다.

`replace` 지시어는 다음과 같은 상황에서 유용하게 사용될 수 있습니다:

* 새로운 모듈을 개발 중이며, 해당 코드의 버전이 아직 저장소에 포함되어 있지 않습니다.
  고객에게 로컬 버전을 사용하여 테스트를 진행하고 싶습니다.
* 의존성 관련 문제를 식별했으며, 해당 의존성의 저장소를 복제하고, 로컬 저장소에서 수정 사항을 테스트하고 있습니다.

참고: `replace` 지시문만으로는 [모듈 그래프](/ref/mod#glos-module-graph)에 모듈을 추가하지 않습니다. 대체된 모듈 버전을 참조하는 [`require` 지시문](#require)도 필요합니다. 이는 메인 모듈의 `go.mod` 파일 또는 종속 모듈의 `go.mod` 파일에 있어야 합니다. 특정 버전을 대체할 필요가 없는 경우, 아래 예제와 같이 가짜 버전을 사용할 수 있습니다. 단, `replace` 지시문은 메인 모듈에서만 적용되므로, 이 경우에 의존하는 모듈이 손상될 수 있습니다.

```
require example.com/mod v0.0.0-replace

replace example.com/mod v0.0.0-replace => ./mod
```

필수 모듈을 대체하는 방법에 대한 자세한 내용은, 여기 참조:

* [자신의 저장소에서 외부 모듈 코드를 사용하기
Fork](/doc/modules/managing-dependencies#external_fork)
* [로컬 디렉토리에서 모듈 코드를 사용하기
디렉토리](/doc/modules/managing-dependencies#local_directory)

더 자세한 내용은 [모듈 버전 번호](/doc/modules/version-numbers)를 참조하십시오.

## 제외 {#exclude}

현재 모듈의 의존성 그래프에서 특정 모듈 또는 모듈 버전을 제외하도록 지정합니다.

자세한 내용은 [`exclude` 지시어](/ref/mod#go-mod-file-exclude)를 Go Modules Reference에서 참조하십시오.

### 구문 {#exclude-syntax}

```
제외 <var>모듈-경로</var> <var>모듈-버전</var>
```

```markdown
<dl>
    <dt>module-path</dt>
    <dd>제외할 모듈의 모듈 경로.</dd>
    <dt>module-version</dt>
    <dd>제외할 특정 버전.</dd>
</dl>
```

### 예시 {#exclude-example}

* `example.com/theirmodule` 버전 v1.3.0 제외

```
  제외 예시: example.com/theirmodule v1.3.0
```

### 참고 사항 {#exclude-notes}

`exclude` 지시어를 사용하여 특정 모듈의 특정 버전을 간접적으로 필요로 하지만, 어떤 이유로든 로드할 수 없는 경우에 해당 버전을 제외합니다. 예를 들어, 유효하지 않은 체크섬을 가진 모듈의 특정 버전을 제외하는 데 사용할 수 있습니다.

`exclude` 및 `replace` 지시문을 사용하여 현재 모듈(빌드 중인 메인 모듈)을 빌드할 때 빌드 타임 의존성 해결을 제어합니다.
이 지시문은 현재 모듈에 의존하는 모듈에서는 무시됩니다.

다음 예제와 같이 [`go mod edit`](/ref/mod#go-mod-edit) 명령을 사용하여 모듈을 제외할 수 있습니다.

```
go mod edit --exclude=example.com/theirmodule@v1.3.0
```

자세한 내용은 다음을 참조하세요.
[모듈 버전 번호](/doc/modules/version-numbers).

## 취소하기 {#retract}

지정된 `go.mod`에 정의된 모듈의 특정 버전 또는 버전 범위에 의존하지 않아야 함을 나타냅니다. `retract` 지시문은 버전이 미리 출시되었거나 버전이 출시된 후 심각한 문제가 발견되었을 때 유용합니다.

자세한 내용은 [`retract` 지침](/ref/mod#go-mod-file-retract)을 Go Modules Reference에서 참조하십시오.

### 구문 {#retract-구문}

```
취소 <var>버전</var> // <var>이유</var>
취소 [<var>버전-낮음</var>,<var>버전-높음</var>] // <var>이유</var>
```

```markdown
<dl>
  <dt>version</dt>
  <dd>철회할 단일 버전</dd>
  <dt>version-low</dt>
  <dd>철회할 버전 범위의 하한</dd>
  <dt>version-high</dt>
  <dd>
    철회할 버전 범위의 상한. <var>version-low</var>
    및 <var>version-high</var>은 범위에 모두 포함됩니다.
  </dd>
  <dt>rationale</dt>
  <dd>
    철회 이유에 대한 선택적 설명. 사용자와의 메시지에 표시될 수 있습니다.
  </dd>
</dl>
```

### 예시 {#retract-example}

* 단일 버전 되돌리기

```
  이전 버전으로 되돌림 v1.1.0 // 실수로 게시됨.
  ```

* 여러 버전 되돌리기

```
  retract [v1.0.0, v1.0.5] // 일부 플랫폼에서 빌드 오류 발생.
```

### 참고 사항 {#retract-notes}

`retract` 지시어를 사용하여 모듈의 이전 버전을 사용하지 않도록 지정합니다. `go get`, `go mod tidy` 또는 기타 명령을 사용하여 자동으로 이전 버전으로 업그레이드되지 않습니다. `go list -m -u` 명령을 사용하여 이전 버전이 사용 가능한 업데이트로 표시되지 않습니다.

이전 버전은 사용자가 이미 의존하는 경우에도 사용 가능하도록 유지해야 합니다. 이전 버전이 소스 저장소에서 삭제되더라도, [proxy.golang.org](https://proxy.golang.org)와 같은 미러에서 여전히 사용할 수 있습니다. 이전 버전에 의존하는 사용자는 관련 모듈에서 `go get` 또는 `go list -m -u`를 실행할 때 알림을 받을 수 있습니다.

명령 `go`는 모듈의 최신 버전에 있는 `go.mod` 파일의 `retract` 지시문을 읽어서, 제거된 버전을 찾습니다. 최신 버전은 다음 순서로 적용됩니다:

1. 최신 릴리스 버전 (있는 경우)
2. 최신 사전 릴리스 버전 (있는 경우)
3. 저장소의 기본 브랜치의 최신 버전의 가상 버전.

새로운, 더 높은 버전을 태그해야 하는 경우가 거의 항상 있습니다.
이렇게 하면 명령이 최신 버전의 모듈에서 이를 인식할 수 있습니다.

새로운 버전을 게시할 수 있으며, 이 버전의 유일한 목적은 회수를 알리는 것입니다.
이 경우, 새로운 버전은 자체적으로 회수될 수도 있습니다.

예를 들어, 실수로 `v1.0.0`을 태그한 경우, 다음 지침을 사용하여 `v1.0.1`을 태그할 수 있습니다:

```
취소 v1.0.0 // 실수로 게시.
취소 v1.0.1 // 취소만 포함.
```

불행히도, 버전이 게시되면 변경할 수 없습니다. 만약 나중에 `v1.0.0`을 다른 커밋에서 태그하면, `go` 명령어가 `go.sum` 또는 [체크섬
데이터베이스](/ref/mod#checksum-database)에서 일치하지 않는 합계를 감지할 수 있습니다.

`go list -m -versions`의 출력에는 일반적으로 복호화되지 않은 모듈 버전이 나타나지 않지만, `-retracted` 옵션을 사용하여 확인할 수 있습니다.
자세한 내용은 [`go list -m`](/ref/mod#go-list-m)에서 Go 모듈 참조를 참조하십시오.

## 무시 {#ignore}

`go` 명령어가 패키지 패턴과 일치할 때 무시해야 하는 모듈 내의 디렉토리 경로를 지정합니다.

자세한 내용은 [`ignore` 지시어](/ref/mod#go-mod-file-ignore)를 Go Modules Reference에서 참조하십시오.

### 구문 {#ignore-syntax}

```
무시 <var>경로</var>
```

```
<dl>
  <dt>path</dt>
  <dd>
    슬래시로 구분된 경로를 무시하도록 지정합니다. 만약 경로가 <code >./</code>로 시작하면, 해당 경로는 모듈의 루트 디렉토리에 상대적으로 해석됩니다. 그렇지 않으면, 모듈 내의 모든 깊이에서 해당 이름을 가진 디렉토리는 무시됩니다.
  </dd>
</dl>
```

### 예제 {#ignore-examples}

* 모듈 루트에 상대적인 로컬 디렉토리를 무시합니다

```
  무시 ./node_modules
  ```

* 모듈 내 어디에서든 `generated`라는 이름의 모든 디렉토리를 무시합니다.

```
 무시
```

* 여러 경로를 무시하기 위해 블록 사용

```
  무시 (
      정적
      content/html
      ./third_party/javascript
  )
  ```

### 참고 사항 {#ignore-notes}

`ignore` 지시어를 사용하여 `go` 명령이 생성된 또는 Go가 아닌 디렉토리의 패키지를 와일드카드 패턴(예: `./...`)을 사용할 때 일치하지 않도록 방지합니다. 무시되는 디렉토리와 해당 내용은 패키지 패턴에서 제외되지만, 여전히 모듈 파일 트리에 존재합니다.

`ignore` 지시사항은 단독 모듈의 `go.mod` 파일에서만 적용됩니다.
`go.mod` 파일에 있는 종속 모듈에서는 효과가 없습니다.
