<!--{
  "Title": "Go 모듈 구성하기"
}-->

Go를 처음 접하는 개발자들이 공통적으로 갖는 질문 중 하나는 파일과 폴더 구성 측면에서 "Go 프로젝트를 어떻게 조직해야 하는가?"입니다. 이 문서의 목표는 이 질문에 답하는 데 도움이 될 몇 가지 가이드라인을 제공하는 것입니다. 이 문서를 최대한 활용하시려면 [튜토리얼](/doc/tutorial/create-module)과 [모듈 소스 관리](/doc/modules/managing-source)를 읽고 Go 모듈의 기본 개념에 익숙해지시기 바랍니다.

Go 프로젝트는 패키지, 커맨드라인 프로그램 또는 이 둘의 조합을 포함할 수 있습니다. 이 가이드는 프로젝트 유형별로 구성되어 있습니다.

### 기본 패키지

기본적인 Go 패키지는 모든 코드가 프로젝트의 루트 디렉토리에 위치합니다. 프로젝트는 단일 모듈로 구성되며, 이 모듈은 다시 단일 패키지로 구성됩니다. 패키지 이름은 모듈 이름의 마지막 경로 구성 요소와 일치합니다. 단일 Go 파일만 필요한 매우 간단한 패키지의 경우, 프로젝트 구조는 다음과 같습니다:

```
project-root-directory/
  go.mod
  modname.go
  modname_test.go
```

_[이 문서 전반에 걸쳐 파일/패키지 이름은 완전히 임의로 지정되었습니다]_

이 디렉토리가 `github.com/someuser/modname`에 있는 GitHub 저장소에 업로드되었다고 가정하면, `go.mod` 파일의 `module` 라인은 `module github.com/someuser/modname`이라고 작성해야 합니다.

`modname.go` 파일의 코드는 다음과 같이 패키지를 선언합니다:

```
package modname

// ... 패키지 코드가 여기에 위치합니다
```

사용자는 이제 Go 코드에서 다음과 같이 해당 패키지를 `import` 하여 사용할 수 있습니다:

```
import "github.com/someuser/modname"
```

Go 패키지는 모두 동일한 디렉토리에 위치하는 여러 개의 파일로 나눌 수 있습니다. 예시는 다음과 같습니다.

```
project-root-directory/
  go.mod
  modname.go
  modname_test.go
  auth.go
  auth_test.go
  hash.go
  hash_test.go
```

디렉토리의 모든 파일이 `package modname`을 선언하고 있습니다.

### 기본 명령어

기본적인 실행 프로그램(또는 명령줄 도구)은 복잡성과 코드 크기에 따라 구조화됩니다. 가장 단순한 프로그램은 `func main`이 정의된 단일 Go 파일로 구성될 수 있습니다. 더 큰 프로그램은 모든 파일이 `package main`을 선언하면서 코드를 여러 파일로 나눌 수 있습니다.

```
project-root-directory/
  go.mod
  auth.go
  auth_test.go
  client.go
  main.go
```

여기 `main.go` 파일에 `func main`이 포함되어 있지만, 이는 단지 관례일 뿐입니다. "main" 파일은 `modname.go`(`modname`에 적절한 값을 사용) 또는 다른 이름으로 부를 수도 있습니다.

이 디렉토리가 `github.com/someuser/modname`에 있는 GitHub 저장소에 업로드된다고 가정하면, `go.mod` 파일의 `module` 라인은 다음과 같아야 합니다:

```
module github.com/someuser/modname
```

사용자는 다음 명령어로 자신의 머신에 설치할 수 있습니다:

```
$ go install github.com/someuser/modname@latest
```

### 패키지 또는 지원 패키지가 포함된 명령어

규모가 큰 패키지나 명령어는 일부 기능을 지원 패키지로 분리하는 것이 유리할 수 있습니다. 처음에는 이러한 패키지들을 `internal`이라는 이름의 디렉토리에 배치하는 것을 권장합니다. [이렇게 하면](https://pkg.go.dev/cmd/go#hdr-Internal_Directories) 외부 사용을 위해 반드시 노출하고 지원할 필요가 없는 패키지에 다른 모듈이 의존하는 것을 방지할 수 있습니다. 다른 프로젝트에서 우리의 `internal` 디렉토리에 있는 코드를 임포트할 수 없으므로, 외부 사용자에게 영향을 주지 않고 자유롭게 API를 리팩토링하거나 전반적인 구조를 변경할 수 있습니다. 따라서 패키지의 프로젝트 구조는 다음과 같습니다.

```
project-root-directory/
  internal/
    auth/
      auth.go
      auth_test.go
    hash/
      hash.go
      hash_test.go
  go.mod
  modname.go
  modname_test.go
```

`modname.go` 파일은 `package modname`을 선언하고, `auth.go` 파일은 `package auth` 등을 선언합니다. `modname.go`는 다음과 같이 `auth` 패키지를 import 할 수 있습니다:

```
import "github.com/someuser/modname/internal/auth"
```

`internal` 디렉터리에 지원 패키지가 포함된 커맨드의 레이아웃은 매우 유사하지만, 루트 디렉터리의 파일(들)이 `package main`을 선언한다는 점이 다릅니다.

### 여러 패키지

모듈은 여러 개의 임포트 가능한 패키지로 구성될 수 있습니다. 각 패키지는 자체 디렉토리를 가지며, 계층적으로 구조화될 수 있습니다. 다음은 샘플 프로젝트 구조입니다:

```
project-root-directory/
  go.mod
  modname.go
  modname_test.go
  auth/
    auth.go
    auth_test.go
    token/
      token.go
      token_test.go
  hash/
    hash.go
  internal/
    trace/
      trace.go
```

참고로, `go.mod` 파일의 `module` 라인이 다음과 같다고 가정합니다.

```
module github.com/someuser/modname
```

`modname` 패키지는 루트 디렉토리에 위치하며, `package modname`을 선언합니다. 사용자는 다음과 같이 임포트하여 사용할 수 있습니다:

```
import "github.com/someuser/modname"
```

사용자는 다음과 같이 서브 패키지를 임포트할 수 있습니다:

```
import "github.com/someuser/modname/auth"
import "github.com/someuser/modname/auth/token"
import "github.com/someuser/modname/hash"
```

`internal/trace`에 위치한 `trace` 패키지는 이 모듈 외부에서 임포트할 수 없습니다. 패키지는 가능한 한 `internal` 내에 유지하는 것이 권장됩니다.

### 여러 명령어

동일한 리포지토리에 있는 여러 프로그램은 일반적으로 별도의 디렉토리를 갖습니다:

```
project-root-directory/
  go.mod
  internal/
    ... 공유 내부 패키지(shared internal packages)
  prog1/
    main.go
  prog2/
    main.go
```

각 디렉토리에서 프로그램의 Go 파일들은 `package main`을 선언합니다. 최상위 `internal` 디렉토리는 저장소의 모든 커맨드에서 사용하는 공유 패키지들을 포함할 수 있습니다.

사용자는 다음과 같이 이 프로그램들을 설치할 수 있습니다:

```
$ go install github.com/someuser/modname/prog1@latest
$ go install github.com/someuser/modname/prog2@latest
```

일반적인 관례는 리포지토리의 모든 명령어를 `cmd` 디렉토리에 배치하는 것입니다. 명령어만으로 구성된 리포지토리에서는 이것이 엄격하게 필수적인 것은 아니지만, 다음에 논의할 내용처럼 명령어와 임포트 가능한 패키지가 모두 포함된 혼합 리포지토리에서는 매우 유용합니다.

### 동일한 리포지토리 내의 패키지와 커맨드

때로는 저장소가 가져와 사용할 수 있는 패키지(importable packages)와 관련 기능을 가진 설치 가능한 명령어(installable commands)를 모두 제공하는 경우가 있습니다. 이러한 저장소의 샘플 프로젝트 구조는 다음과 같습니다.

```
project-root-directory/
  go.mod
  modname.go
  modname_test.go
  auth/
    auth.go
    auth_test.go
  internal/
    ... internal packages
  cmd/
    prog1/
      main.go
    prog2/
      main.go
```

이 모듈의 이름이 `github.com/someuser/modname`이라고 가정하면, 이제 사용자는 다음과 같이 모듈 내의 패키지를 임포트할 수 있습니다.

```
import "github.com/someuser/modname"
import "github.com/someuser/modname/auth"
```

그리고 이를 통해 프로그램을 설치하세요:

```
$ go install github.com/someuser/modname/cmd/prog1@latest
$ go install github.com/someuser/modname/cmd/prog2@latest
```

### 서버 프로젝트

Go는 *서버*를 구현할 때 흔히 선택되는 언어입니다. 프로토콜(REST? gRPC?), 배포, 프론트엔드 파일, 컨테이너화, 스크립트 등 서버 개발의 다양한 측면으로 인해 이러한 프로젝트의 구조는 매우 다양합니다. 여기서는 프로젝트에서 Go로 작성된 부분에 집중하여 안내하겠습니다.

서버 프로젝트는 일반적으로 서버가 단일 바이너리(또는 바이너리 그룹)로 구성된 독립적인 형태이므로, 외부로 내보낼 패키지가 없는 경우가 많습니다. 따라서 서버 로직을 구현하는 Go 패키지들은 `internal` 디렉토리에 유지하는 것이 권장됩니다. 또한, 프로젝트에 Go 파일이 아닌 다른 파일들이 포함된 디렉토리가 많을 가능성이 높으므로, 모든 Go 명령어를 `cmd` 디렉토리에 모아두는 것이 좋습니다.

```
project-root-directory/
  go.mod
  internal/
    auth/
      ...
    metrics/
      ...
    model/
      ...
  cmd/
    api-server/
      main.go
    metrics-analyzer/
      main.go
    ...
  ... Go 코드가 아닌 프로젝트의 다른 디렉토리들
```

서버 저장소의 패키지가 성장하여 다른 프로젝트와 공유하기에 유용해지는 경우, 이를 별도의 모듈로 분리하는 것이 가장 좋습니다.
