<!--{
  "제목": "Go 모듈 구성하기"
}-->

Go를 처음 접하는 개발자들이 흔히 묻는 질문은 "Go 프로젝트를 어떻게 구성해야 할까요?", 특히 파일 및 폴더 구조 측면에서입니다. 이 문서의 목표는 이러한 질문에 답하는 데 도움이 될 수 있는 몇 가지 지침을 제공하는 것입니다. 이 문서를 최대한 활용하려면, 먼저 Go 모듈의 기본 사항을 [튜토리얼](/doc/tutorial/create-module)과 [모듈 소스 관리](/doc/modules/managing-source)를 통해 숙지하십시오.

Go 프로젝트는 패키지, 명령줄 프로그램을 또는 두 가지를 조합할 수 있습니다. 이 가이드는 프로젝트 유형별로 구성되어 있습니다.

### 기본 패키지

기본 Go 패키지는 프로젝트의 루트 디렉터리에 모든 코드를 포함합니다. 프로젝트는 단일 모듈로 구성되며, 이는 단일 패키지로 구성됩니다. 패키지 이름은 모듈 이름의 마지막 경로 구성 요소와 일치합니다. 단일 Go 파일을 필요로 하는 매우 간단한 패키지의 경우, 프로젝트 구조는 다음과 같습니다:

```
프로젝트 루트 디렉토리/
  go.mod
  modname.go
  modname_test.go
```

_[본 문서 전체에서 파일/패키지 이름은 완전히 임의로 지정됨]_

이 디렉토리가 `github.com/someuser/modname`에 GitHub 저장소로 업로드된 경우, `go.mod` 파일의 `module` 라인은 다음과 같아야 합니다.
`module github.com/someuser/modname`.

`modname.go` 파일에 있는 코드는 다음과 같이 패키지를 선언합니다:

```
패키지명

// ... 패키지 코드
```

사용자는 다음과 같이 Go 코드에서 `import`하여 이 패키지를 사용할 수 있습니다:

```
import "github.com/someuser/modname"
```

Go 패키지는 여러 파일로 분할할 수 있으며, 모든 파일은 동일한 디렉토리에 위치합니다. 예를 들어:

```
프로젝트 루트 디렉토리/
  go.mod
  modname.go
  modname_test.go
  auth.go
  auth_test.go
  hash.go
  hash_test.go
```

디렉토리에 있는 모든 파일은 `package modname`을 선언합니다.

### 기본 명령어

기본 실행 가능한 프로그램(또는 명령줄 도구)는 복잡성과 코드 크기에 따라 구조화됩니다. 가장 간단한 프로그램은 단일 Go 파일로 구성될 수 있으며, 여기서 `func main`이 정의됩니다. 더 큰 프로그램은 여러 파일에 코드를 분할할 수 있으며, 모든 파일은 `package main`을 선언합니다:

```
프로젝트 루트 디렉토리/
  go.mod
  auth.go
  auth_test.go
  client.go
  main.go
```

`main.go` 파일에는 `func main`이 포함되어 있지만, 이는 단순히 관례입니다.
"main" 파일은 "modname"에 적절한 값을 넣어 `modname.go`로도 호출할 수 있으며, 다른 이름으로도 호출할 수 있습니다.

만약 이 디렉토리가 `github.com/someuser/modname`라는 GitHub 저장소에 업로드된다면, `go.mod` 파일의 `module` 라인은 다음과 같아야 합니다:

```
모듈 github.com/someuser/modname
```

그리고 사용자는 다음과 같이 자신의 머신에서 설치할 수 있어야 합니다:

```
$ go install github.com/someuser/modname@최신 버전
```

### 지원 패키지와 함께 사용되는 패키지 또는 명령어

더 큰 패키지나 명령어는 일부 기능을 지원 패키지로 분리하는 데 도움이 될 수 있습니다. 처음에는 이러한 패키지를 `internal`이라는 이름의 디렉토리에 배치하는 것이 좋습니다.
[이렇게 하면](https://pkg.go.dev/cmd/go#hdr-Internal_Directories) 다른 모듈이 우리가 반드시 노출하고 지원하고 싶지 않은 패키기에 의존하는 것을 방지할 수 있습니다. 다른 프로젝트가 우리의 `internal` 디렉토리에서 코드를 가져올 수 없으므로, 외부 사용자를 손상시키지 않고 API를 재구성하고 일반적으로 패키지를 이동하는 것이 가능합니다. 패키지의 프로젝트 구조는 다음과 같습니다:

```
프로젝트-루트-디렉토리/
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

`modname.go` 파일은 `package modname`을 선언하고, `auth.go` 파일은 `package auth`를 선언합니다. `modname.go`는 다음과 같이 `auth` 패키지를 가져올 수 있습니다:

```
import "github.com/someuser/modname/내부/auth"
```

명령과 지원 패키지가 있는 `internal` 디렉토리의 레이아웃은 매우 유사하지만, 루트 디렉토리의 파일(들)은 `package
main`을 선언합니다.

### 여러 패키지

모듈은 여러 개의 가져올 수 있는 패키지로 구성될 수 있으며, 각 패키지는 자체 디렉토리를 가지고 있으며 계층적으로 구성될 수 있습니다. 다음은 샘플 프로젝트 구조입니다:

```
프로젝트_루트_디렉토리/
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

다음과 같이 `go.mod` 파일의 `module` 줄이 있다고 가정합니다:

```
모듈 github.com/someuser/modname
```

`modname` 패키지는 루트 디렉토리에 위치하며, `package modname`를 선언하고, 사용자는 다음과 같이 가져올 수 있습니다:

```
import "github.com/someuser/modname"
```

사용자는 다음과 같이 하위 패키지를 가져올 수 있습니다:

```
import "github.com/someuser/modname/auth"
import "github.com/someuser/modname/auth/token"
import "github.com/someuser/modname/hash"
```

패키지 `trace`가 `internal/trace`에 위치하고 있으므로, 이 모듈 외부에서는 가져올 수 없습니다. 가능한 한 패키지를 `internal`에 유지하는 것이 좋습니다.

### 여러 명령

동일한 저장소 내 여러 프로그램은 일반적으로 별도의 디렉토리를 가집니다:

```
프로젝트 루트 디렉토리/
  go.mod
  internal/
    ... 공유 내부 패키지
  prog1/
    main.go
  prog2/
    main.go
```

각 디렉토리에서 프로그램의 Go 파일은 `package main`을 선언합니다. 상위 레벨의 `internal` 디렉토리는 저장소의 모든 명령에서 사용되는 공유 패키지를 포함할 수 있습니다.

사용자는 다음 방법을 사용하여 이러한 프로그램을 설치할 수 있습니다:

```
$ go install github.com/someuser/modname/prog1@latest
$ go install github.com/someuser/modname/prog2@latest
```

일반적인 관례는 저장소의 모든 명령을 `cmd` 디렉토리에 배치하는 것입니다. 물론, 명령만으로 구성된 저장소에서는 엄격하게 필요하지는 않지만, 명령과 가져올 수 있는 패키지가 모두 포함된 혼합된 저장소에서는 매우 유용합니다. 다음에서 자세히 설명하겠습니다.

### 동일 저장소 내의 패키지 및 명령어

때로는 저장소가 가져올 수 있는 패키지와 함께, 관련된 기능을 제공하는 설치 가능한 명령어를 모두 제공할 수 있습니다. 예를 들어 다음과 같은 저장소 구조가 있을 수 있습니다:

`project-root-directory/`
  `go.mod`
  `modname.go`
  `modname_test.go`
  `auth/`
    `auth.go`
    `auth_test.go`
  `internal/`
    ... 내부 패키지
  `cmd/`
    `prog1/`
      `main.go`
    `prog2/`
      `main.go`

가정컨대 이 모듈은 `github.com/someuser/modname`로 호출됩니다. 사용자는 이제 다음과 같이 이 모듈에서 패키지를 가져올 수 있습니다:

```
import "github.com/someuser/modname"
import "github.com/someuser/modname/auth"
```

그리고 다음과 같은 프로그램들을 설치하십시오:

```
$ go install github.com/someuser/modname/cmd/prog1@latest
$ go install github.com/someuser/modname/cmd/prog2@latest
```

### 서버 프로젝트

Go는 *서버*를 구현하는 데 사용되는 일반적인 언어 선택입니다. 서버 개발의 다양한 측면으로 인해 이러한 프로젝트의 구조는 매우 다양합니다: 프로토콜 (REST? gRPC?), 배포, 프론트엔드 파일, 컨테이너화, 스크립트 등이 있습니다. 여기에서는 Go로 작성된 프로젝트의 특정 부분에 초점을 맞추어 안내하겠습니다.

서버 프로젝트는 일반적으로 내보낼 패키지를 갖지 않는데, 왜냐하면 서버는
일반적으로 자체 포함된 바이너리(또는 바이너리의 집합)이기 때문입니다. 따라서 서버의 로직을 구현하는 Go 패키지를 `internal` 디렉토리에 유지하는 것이 좋습니다. 또한 프로젝트에 다른 많은 디렉토리가 있고, 이 디렉토리는 Go 파일이 아닌 파일들을 포함하는 경우, 모든 Go 명령을 `cmd` 디렉토리에 함께 유지하는 것이 좋은 방법입니다:

```
프로젝트 루트 디렉토리/
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
  ... 프로젝트의 다른 디렉토리 (Go 코드가 아닌)
```

만약 서버 저장소가 다른 프로젝트와 공유할 수 있는 유용한 패키지를 포함하게 되면, 이러한 패키지를 별도의 모듈로 분리하는 것이 좋습니다.
