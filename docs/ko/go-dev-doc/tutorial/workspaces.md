<!--{
  "제목": "멀티 모듈 워크스페이스 시작하기 튜토리얼",
  "브레드크럼": true
}-->

이 튜토리얼은 Go의 다중 모듈 워크스페이스의 기본 사항을 소개합니다.

다중 모듈 워크스페이스를 사용하면 Go 명령에 여러 모듈에서 동시에 코드를 작성하고 있음을 알릴 수 있으며, 해당 모듈의 코드를 쉽게 빌드하고 실행할 수 있습니다.

이 튜토리얼에서는 공유 멀티 모듈 워크스페이스 내에 두 개의 모듈을 만들고, 해당 모듈에서 변경 사항을 적용한 다음, 빌드에서 변경 사항의 결과를 확인하는 방법을 안내합니다.

<!-- TODO 목차 -->

**참고:** 다른 튜토리얼은 [Tutorial](/doc/tutorial/index.html) 에서 확인하십시오.

## 필수 조건

*   **Go.** 이 튜토리얼을 따라하기 위해 최신 버전의 Go를 사용하는 것을 권장합니다.
    설치 지침은 [Go 설치](/doc/install)를 참조하세요.
*   **코드 편집 도구.** 사용 중인 모든 텍스트 편집기가 잘 작동합니다.
*   **명령 터미널.** Go는 Linux 및 Mac의 모든 터미널, PowerShell 또는 cmd (Windows)에서 잘 작동합니다.

## 코드를 위한 모듈 생성 {#create_folder}

```
mkdir my_module
cd my_module
go mod init my_module
```

시작하려면, 작성할 코드를 위한 모듈을 만드세요.

1. 명령 프롬프트를 열고 홈 디렉토리로 이동합니다.

리눅스 또는 맥에서:

```
    $ cd
```

**Windows에서:**

```
    C:\> cd %HOMEPATH%
```

이 튜토리얼의 나머지 부분에서는 `$`를 프롬프트로 표시합니다. 사용하려는 명령어는 Windows에서도 작동합니다.

2. 명령 프롬프트에서 코드를 위한 디렉토리를 만들고 이름을 `workspace`로 지정합니다.

```
    $ mkdir workspace
    $ cd workspace
```

3. 모듈 초기화

다음 예에서는 `hello`라는 새로운 모듈을 만들고, 이 모듈이 `golang.org/x/example` 모듈에 의존하도록 구성합니다.

`hello` 모듈 생성:

```
   $ mkdir hello
   $ cd hello
   $ go mod init example.com/hello
   go: 생성 중: 새 go.mod 파일: 모듈 example.com/hello
   ```

`go get golang.org/x/example/hello/reverse` 명령어를 사용하여 `golang.org/x/example/hello/reverse` 패키지에 대한 의존성을 추가합니다.

```
   $ go get golang.org/x/example/hello/reverse
```

```markdown
# hello.go 파일 생성

`hello` 디렉토리에 다음 내용을 포함하는 `hello.go` 파일을 생성합니다.

```
   패키지 main
```

```
import (
    fmt
)
```

```
golang.org/x/example/hello/reverse
)
```

```
func main() {
       fmt.Println(reverse.String("Hello"))
   }
```

이제 `hello` 프로그램을 실행합니다:

```
   $ go run .
   olleH
   ```

## 워크스페이스 생성하기

이 단계에서는 모듈을 정의하는 워크스페이스를 지정하기 위해 `go.work` 파일을 생성합니다.

#### 워크스페이스 초기화

`workspace` 디렉터리에서 다음 명령을 실행하세요:

```
   go work init ./hello
```

명령 `go work init`는 `go`에게 `./hello` 디렉터리에 있는 모듈을 포함하는 워크스페이스에 대해 `go.work` 파일을 생성하도록 지시합니다.

명령 `go`는 다음과 같은 `go.work` 파일을 생성합니다:

```
   go 1.18
```

use ./hello
   ```

`go.work` 파일은 `go.mod` 파일과 유사한 구문을 가지고 있습니다.

`go` 지시어는 Go 컴파일러가 파일을 해석할 때 사용할 Go 버전이 무엇인지 알려줍니다. 이는 `go.mod` 파일의 `go` 지시어와 유사합니다.

`use` 지시어는 Go에게 `hello`
디렉토리에 있는 모듈이 빌드 시 메인 모듈로 사용되도록 지시합니다.

따라서 `workspace`의 모든 하위 디렉터리에서 모듈이 활성화됩니다.

#### 워크스페이스 디렉토리에서 프로그램을 실행합니다.

`workspace` 디렉토리에서 다음 명령을 실행하세요:

```
   $ go run ./hello
   olleH
   ```

`go` 명령어는 워크스페이스의 모든 모듈을 기본 모듈로 포함합니다. 이를 통해 모듈 외부에서도 모듈 내의 패키지를 참조할 수 있습니다. `go run` 명령을 모듈 또는 워크스페이스 외부에서 실행하면 오류가 발생합니다. 왜냐하면 `go` 명령은 어떤 모듈을 사용해야 할지 알 수 없기 때문입니다.

다음으로, `golang.org/x/example/hello` 모듈의 로컬 복사본을 워크스페이스에 추가하겠습니다.
이 모듈은 `go.googlesource.com/example` Git 저장소의 하위 디렉토리에 저장되어 있습니다.
그런 다음 `reverse` 패키지에 새로운 함수를 추가하여 `String` 대신 사용할 수 있도록 하겠습니다.

## `golang.org/x/example/hello` 모듈 다운로드 및 수정하기

1.  **모듈 다운로드:**
    ```bash
    go get golang.org/x/example/hello
    ```

2.  **소스 코드 확인:**
    다운로드된 모듈의 소스 코드는 다음과 같습니다.
    ```go
    package hello

    import "fmt"

    func Hello(name string) {
    	fmt.Printf("Hello, %s!\n", name)
    }
    ```

3.  **수정 (예시):**
    `Hello` 함수를 수정하여 다른 메시지를 출력하도록 할 수 있습니다.
    ```go
    package hello

    import "fmt"

    func Hello(name string) {
    	fmt.Printf("안녕하세요, %s!  이것은 수정된 메시지입니다!\n", name)
    }
    ```

4.  **프로그램에서 사용:**
    수정된 모듈을 사용하기 위한 간단한 Go 프로그램 예시:
    ```go
    package main

    import (
    	"fmt"
    	"golang.org/x/example/hello"
    )

    func main() {
    	hello.Hello("World")
    }
    ```

이 단계에서는 `golang.org/x/example/hello` 모듈을 포함하는 Git 저장소의 복사본을 다운로드하고, 워크스페이스에 추가한 다음, hello 프로그램에서 사용할 새로운 함수를 추가합니다.

1. 저장소를 복제하세요

워크스페이스 디렉토리에서 `git` 명령을 사용하여 저장소를 복제합니다:

```
   $ git clone https://go.googlesource.com/example
   'example'으로 복제 중...
   remote: 총 165개 (델타 27개), 165개 재사용 (델타 27개)
   객체 수신: 100% (165/165), 434.18 KiB | 1022.00 KiB/s, 완료.
   델타 해결: 100% (27/27), 완료.
   ```

2. 워크스페이스에 모듈 추가

이 Git 저장소는 `./example`에 체크아웃되었습니다.
   `golang.org/x/example/hello` 모듈의 소스 코드는 `./example/hello`에 있습니다.
   워크스페이스에 추가하십시오:

```
   $ go work use ./example/hello
   ```

명령 `go work use`는 `go.work` 파일에 새 모듈을 추가합니다. 그러면 파일은 다음과 같이 됩니다:

```
   go 1.18
```

```
(
       ./hello
       ./example/hello
   )
```

현재 워크스페이스에는 `example.com/hello` 모듈과 `golang.org/x/example/hello` 모듈이 모두 포함되어 있으며, 이 모듈은 `golang.org/x/example/hello/reverse` 패키지를 제공합니다.

이렇게 하면, `reverse` 패키지의 새 코드를 작성하고 사용할 수 있게 됩니다.
`go get` 명령으로 다운로드한 모듈 캐시에 있는 패키지의 버전을 사용하는 대신.

3. 새로운 함수를 추가합니다.

저희는 `golang.org/x/example/hello/reverse` 패키지에 숫자를 뒤집는 새로운 함수를 추가할 것입니다.

`workspace/example/hello/reverse` 디렉토리 내에 `int.go`라는 새 파일을 만들고 다음과 같은 내용을 포함합니다:

```
   package reverse
```

```
import "strconv"
```

```
// Int은 정수 i의 십진수를 거꾸로 변환합니다.
   func Int(i int) int {
       i, _ = strconv.Atoi(String(strconv.Itoa(i)))
       return i
   }
```

4. `hello` 프로그램을 수정하여 함수를 사용합니다.

```markdown
```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, world!")
}
```

```
   패키지 main
```

```
import (
        "fmt"
)
```

"golang.org/x/example/hello/reverse"
   )

```
func main() {
    fmt.Println(reverse.String("Hello"), reverse.Int(24601))
}
```

#### 워크스페이스에서 코드를 실행합니다

작업 디렉토리에서 다음 명령을 실행하세요:

```
   $ go run ./hello
   olleH 10642
   ```

`go` 명령은 명령줄에서 지정된 `example.com/hello` 모듈을 `go.work` 파일에 지정된 `hello` 디렉토리에서 찾고, `go.work` 파일을 사용하여 `golang.org/x/example/hello/reverse` import를 유사하게 해결합니다.

`go.work`를 사용하면 여러 모듈 간의 협업을 위해 `replace` 지시문을 추가할 필요가 없습니다.

두 모듈이 동일한 워크스페이스에 있기 때문에 한 모듈에서 변경을 하고 다른 모듈에서 사용하는 것이 간단합니다.

#### 다음 단계

이제 이러한 모듈을 제대로 배포하려면 `golang.org/x/example/hello` 모듈의 배포를 수행해야 합니다. 예를 들어 `v0.1.0` 버전으로 배포할 수 있습니다. 이는 일반적으로 모듈의 버전 제어 저장소에서 커밋을 태깅하여 수행됩니다. 자세한 내용은 다음 문서를 참조하십시오.
   [모듈 배포 워크플로우 설명서](/doc/modules/release-workflow)
   배포가 완료되면 `hello/go.mod` 파일에서 `golang.org/x/example/hello` 모듈의 요구 사항을 변경할 수 있습니다:

```
cd hello
go get golang.org/x/example/hello@v0.1.0
```

그렇게 하면, `go` 명령은 워크스페이스 외부의 모듈을 올바르게 해결할 수 있습니다.

## 워크스페이스에 대해 자세히 알아보세요

명령 `go`는 `go work init` 외에도 워크스페이스를 관리하기 위한 몇 가지 하위 명령어를 가지고 있으며, 이는 이전에 튜토리얼에서 본 내용입니다:

- `go work use [-r] [dir]`은 `go.work` 파일에 `dir`에 대한 `use` 지시문을 추가하고,
   지정된 디렉토리가 존재할 경우, 해당 디렉토리를 제거합니다. `-r` 플래그는 `dir`의 하위 디렉토리를 재귀적으로 검사합니다.
   - `go work edit`는 `go.work` 파일을 `go mod edit`와 유사하게 편집합니다.
   - `go work sync`는 작업 공간의 빌드 목록에서 종속성을 각 작업 공간 모듈로 동기화합니다.

자세한 내용은 Go Modules Reference의 [Workspaces](/ref/mod#workspaces)를 참조하십시오.
