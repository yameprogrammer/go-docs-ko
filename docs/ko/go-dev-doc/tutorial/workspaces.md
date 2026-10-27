<!--{
  "Title": "튜토리얼: 멀티 모듈 워크스페이스 시작하기",
  "Breadcrumb": true
}-->

이 튜토리얼에서는 Go의 멀티 모듈 워크스페이스(multi-module workspaces) 기초에 대해 소개합니다.
멀티 모듈 워크스페이스를 사용하면 여러 모듈의 코드를 동시에 작성하고 있다는 것을 Go 명령어에 알릴 수 있으며, 해당 모듈들의 코드를 쉽게 빌드하고 실행할 수 있습니다.

이 튜토리얼에서는 공유 멀티 모듈 워크스페이스에 두 개의 모듈을 생성하고, 해당 모듈들에 걸쳐 변경 사항을 적용한 뒤, 빌드 결과에서 그 변경 사항들을 확인해 보겠습니다.

<!-- TODO TOC -->

**참고:** 다른 튜토리얼은 [Tutorials](/doc/tutorial/index.html)를 참조하세요.

## 사전 요구 사항

*   **Go.** 이 튜토리얼을 따라하기 위해 최신 버전의 Go를 사용하시는 것을 권장합니다.
    설치 방법은 [Installing Go](/doc/install)를 참조하세요.
*   **코드 편집 도구.** 사용 중인 어떤 텍스트 에디터라도 괜찮습니다.
*   **커맨드 터미널.** Go는 Linux 및 Mac의 모든 터미널, 그리고 Windows의 PowerShell 또는 cmd에서 원활하게 작동합니다.

## 코드 모듈 생성하기 {#create_folder}

시작하려면, 작성할 코드를 위한 모듈을 생성하세요.

1. 명령 프롬프트를 열고 홈 디렉터리로 이동하십시오.

Linux 또는 Mac에서:

```
    $ cd
    ```

Windows에서:

```
    C:\> cd %HOMEPATH%
    ```

이 튜토리얼의 나머지 부분에서는 프롬프트로 `$`가 표시됩니다. 사용하시는 명령어들은 Windows에서도 동일하게 작동합니다.

2. 명령 프롬프트에서 코드를 저장할 `workspace`라는 이름의 디렉토리를 생성합니다.

```
    $ mkdir workspace
    $ cd workspace
    ```

3. 모듈 초기화

우리의 예제에서는 `golang.org/x/example` 모듈에 의존하는 새로운 모듈 `hello`를 생성할 것입니다.

hello 모듈을 생성합니다:

```
   $ mkdir hello
   $ cd hello
   $ go mod init example.com/hello
   go: creating new go.mod: module example.com/hello
   ```

`go get`을 사용하여 `golang.org/x/example/hello/reverse` 패키지에 대한 의존성을 추가하세요.

```
   $ go get golang.org/x/example/hello/reverse
   ```

hello 디렉토리에 다음 내용으로 hello.go 파일을 생성하세요:

```
   package main
```

제공해주신 내용이 코드 조각의 일부(`import ("fmt"`)만 포함되어 있어, 전체 문맥이 없으나 요청하신 대로 기술 번역 원칙에 따라 번역해 드리겠습니다. (현재는 번역할 일반 텍스트가 없으므로 코드 형태를 그대로 유지합니다.)

```go
import (
       "fmt"
```

"golang.org/x/example/hello/reverse"
   )

```go
func main() {
       fmt.Println(reverse.String("Hello"))
   }
   ```

이제 hello 프로그램을 실행하세요:

```
   $ go run .
   olleH
   ```

## 워크스페이스 생성하기

이 단계에서는 모듈이 포함된 워크스페이스를 지정하기 위해 `go.work` 파일을 생성하겠습니다.

#### 워크스페이스 초기화

`workspace` 디렉토리에서 다음을 실행하세요:

```
   $ go work init ./hello
   ```

`go work init` 명령은 `go`에게 `./hello` 디렉토리에 있는 모듈들을 포함하는 워크스페이스를 위한 `go.work` 파일을 생성하도록 지시합니다.

`go` 명령어는 다음과 같은 형태의 `go.work` 파일을 생성합니다:

```
   go 1.18
```

`./hello`를 사용하세요.
   ```

`go.work` 파일은 `go.mod`와 유사한 구문을 가지고 있습니다.

`go` 지시문은 Go가 해당 파일을 어떤 버전의 Go로 해석해야 하는지를 알려줍니다. 이는 `go.mod` 파일에 있는 `go` 지시문과 유사합니다.

`use` 지시문은 빌드를 수행할 때 `hello` 디렉토리에 있는 모듈이 메인 모듈이 되어야 함을 Go에게 알려줍니다.

따라서 `workspace` 하위의 모든 디렉토리에서 모듈이 활성화됩니다.

#### 워크스페이스 디렉토리에서 프로그램 실행

`workspace` 디렉토리에서 다음을 실행하세요:

```
   $ go run ./hello
   olleH
   ```

`go` 명령은 워크스페이스의 모든 모듈을 메인 모듈로 포함합니다. 이를 통해 모듈 외부에서도 해당 모듈 내의 패키지를 참조할 수 있습니다. 모듈이나 워크스페이스 외부에서 `go run` 명령을 실행하면, `go` 명령이 어떤 모듈을 사용해야 할지 알 수 없으므로 에러가 발생합니다.

다음으로, `golang.org/x/example/hello` 모듈의 로컬 복사본을 워크스페이스에 추가하겠습니다.
해당 모듈은 `go.googlesource.com/example` Git 리포지토리의 하위 디렉토리에 저장되어 있습니다.
그 다음, `String` 대신 사용할 수 있는 새로운 함수를 `reverse` 패키지에 추가하겠습니다.

## `golang.org/x/example/hello` 모듈 다운로드 및 수정하기

이 단계에서는 `golang.org/x/example/hello` 모듈이 포함된 Git 저장소의 복사본을 다운로드하여 워크스페이스에 추가한 다음, hello 프로그램에서 사용할 새로운 함수를 추가해 보겠습니다.

1. 저장소 클론하기

워크스페이스 디렉토리에서 `git` 명령어를 실행하여 리포지토리를 클론하세요:

```
   $ git clone https://go.googlesource.com/example
   Cloning into 'example'...
   remote: Total 165 (delta 27), reused 165 (delta 27)
   Receiving objects: 100% (165/165), 434.18 KiB | 1022.00 KiB/s, done.
   Resolving deltas: 100% (27/27), done.
   ```

2. 모듈을 워크스페이스에 추가합니다.

Git 저장소가 방금 `./example`로 체크아웃되었습니다.
   `golang.org/x/example/hello` 모듈의 소스 코드는 `./example/hello`에 있습니다.
   이를 워크스페이스에 추가하세요:

```
   $ go work use ./example/hello
   ```

`go work use` 명령어는 `go.work` 파일에 새로운 모듈을 추가합니다. 이제 다음과 같이 표시됩니다:

```
   go 1.18
```

use (
       ./hello
       ./example/hello
   )
   ```

이제 워크스페이스에는 `example.com/hello` 모듈과 `golang.org/x/example/hello/reverse` 패키지를 제공하는 `golang.org/x/example/hello` 모듈이 모두 포함되어 있습니다.

이렇게 하면 `go get` 명령어로 다운로드한 모듈 캐시의 패키지 버전 대신, 우리가 직접 작성할 `reverse` 패키지 복사본의 새 코드를 사용할 수 있습니다.

3. 새 함수를 추가합니다.

`golang.org/x/example/hello/reverse` 패키지에 숫자를 뒤집는 새로운 함수를 추가하겠습니다.

`workspace/example/hello/reverse` 디렉토리에 다음 내용을 포함하는 `int.go`라는 이름의 새 파일을 생성하세요:

```go
   package reverse
```

`import "strconv"`

```go
   // Int는 정수 i의 십진수 역순 값을 반환합니다.
   func Int(i int) int {
       i, _ = strconv.Atoi(String(strconv.Itoa(i)))
       return i
   }
   ```

4. hello 프로그램을 함수를 사용하도록 수정하세요.

`workspace/hello/hello.go`의 내용을 다음과 같이 수정하십시오:

```
   package main
```

제시해주신 내용이 코드의 일부(`import` 문)만 포함되어 있어, 해당 부분의 번역이 필요 없으시거나 혹은 전체 문서의 일부를 누락하신 것으로 보입니다. 하지만 요청하신 지침에 따라 기술 번역가로서 해당 코드 스니펫을 그대로 유지하여 반환하겠습니다.

```go
import (
       "fmt"
```

"golang.org/x/example/hello/reverse"
   )

```go
func main() {
       fmt.Println(reverse.String("Hello"), reverse.Int(24601))
   }
   ```

#### 워크스페이스에서 코드 실행하기

워크스페이스 디렉토리에서 다음을 실행하세요.

```
   $ go run ./hello
   olleH 10642
   ```

Go 명령은 커맨드 라인에 지정된 `example.com/hello` 모듈을 `go.work` 파일에 지정된 `hello` 디렉토리에서 찾으며, 마찬가지로 `go.work` 파일을 사용하여 `golang.org/x/example/hello/reverse` 임포트를 해석합니다.

`go.work`는 여러 모듈에 걸쳐 작업하기 위해 [`replace`](/ref/mod#go-mod-file-replace) 지시문을 추가하는 대신 사용할 수 있습니다.

두 모듈이 동일한 워크스페이스에 있으므로, 한 모듈에서 변경 사항을 만들고 이를 다른 모듈에서 사용하는 것이 쉽습니다.

#### 향후 단계

이제 이러한 모듈들을 적절하게 릴리스하려면, 예를 들어 `v0.1.0` 버전으로 `golang.org/x/example/hello` 모듈을 릴리스해야 합니다. 이는 보통 모듈의 버전 관리 저장소에서 커밋에 태그를 지정함으로써 수행됩니다. 자세한 내용은 [모듈 릴리스 워크플로 문서](/doc/modules/release-workflow)를 참조하십시오. 릴리스가 완료되면, `hello/go.mod`에서 `golang.org/x/example/hello` 모듈의 요구 버전을 높일 수 있습니다.

```
   cd hello
   go get golang.org/x/example/hello@v0.1.0
   ```

그렇게 함으로써 `go` 명령어가 워크스페이스 외부의 모듈들을 적절하게 resolve할 수 있습니다.

## 워크스페이스에 대해 더 알아보기

`go` 명령어에는 앞서 튜토리얼에서 살펴본 `go work init` 외에도 워크스페이스 작업을 위한 몇 가지 서브커맨드가 더 있습니다:

- `go work use [-r] [dir]`는 `dir`이 존재하는 경우 `go.work` 파일에 `use` 지시어를 추가하고, 인자로 전달된 디렉터리가 존재하지 않으면 해당 `use` 디렉터리를 제거합니다. `-r` 플래그는 `dir`의 하위 디렉터리를 재귀적으로 조사합니다.
   - `go work edit`은 `go mod edit`과 유사하게 `go.work` 파일을 편집합니다.
   - `go work sync`는 워크스페이스의 빌드 리스트에 있는 의존성을 워크스페이스의 각 모듈로 동기화합니다.

워크스페이스와 `go.work` 파일에 대한 자세한 내용은 Go Modules Reference의 [Workspaces](/ref/mod#workspaces)를 참조하세요.
