<!--
참고: 이 문서 및 이 디렉토리에 있는 다른 문서에서, 고정 폭 문자열과 고정 폭이 아닌 공백을 함께 사용하는 것이 관례입니다. 예를 들어, `hello` `world`와 같이 사용합니다.
이러한 문자열에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.17 소개 {#introduction}

Go 1.17 버전은 Go 언어의 새로운 기능과 개선 사항을 제공합니다. 이 문서는 Go 1.17의 주요 특징과 사용 방법을 소개합니다.

가장 최신 Go 버전인 1.17은 [Go 1.16](/doc/go1.16) 이후 6개월 만에 출시되었습니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
물론, 이번 릴리스는 Go 1의 [호환성 약속](/doc/go1compat)을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상됩니다.

## 언어 변경 사항 {#language}

Go 1.17 버전에는 언어에 대한 세 가지 작은 개선 사항이 포함되어 있습니다.

- <!-- CL 216424; issue 395 -->
    [슬라이스에서 배열 포인터로의 변환
    ](/ref/spec#Conversions_from_slice_to_array_pointer): `[]T` 타입의 표현식 `s`는 이제 `*[N]T` 타입의 배열 포인터로 변환될 수 있습니다. 만약 `a`가 이러한 변환의 결과라면, 해당 인덱스 중 범위 내에 있는 인덱스는 동일한 기본 요소를 참조합니다: `&a[i] == &s[i]`는 `0 <= i < N`일 때 유효합니다. `len(s)`가 `N`보다 작을 경우 변환은 오류를 발생시킵니다.
  - <!-- CL 312212; issue 40481 -->
    [`unsafe.Add`](/pkg/unsafe#Add):
    `unsafe.Add(ptr, len)`는 `ptr`에 `len`을 더하고 업데이트된 포인터 `unsafe.Pointer(uintptr(ptr) + uintptr(len))`를 반환합니다.
  - <!-- CL 312212; issue 19367 -->
    [`unsafe.Slice`](/pkg/unsafe#Slice):
    `*T` 타입의 표현식 `ptr`에 대해,
    `unsafe.Slice(ptr, len)`는 `[]T` 타입의 슬라이스를 반환합니다. 이 슬라이스의 기본 배열은 `ptr`에서 시작하고, 길이는 `len`입니다.

`unsafe.Pointer`의 안전 규칙을 준수하는 코드를 작성하기 쉽게 하기 위해 `unsafe` 패키지에 대한 개선 사항이 추가되었습니다 ([unsafe 패키지](https://pkg/unsafe/#Pointer)), 그러나 규칙은 변경되지 않았습니다. 특히, `unsafe.Pointer`를 올바르게 사용하는 기존 프로그램은 유효하게 유지되며, `unsafe.Add` 또는 `unsafe.Slice`를 사용할 때 새 프로그램도 여전히 규칙을 따라야 합니다.

참고: 슬라이스를 배열 포인터로 변환하는 새로운 변환은 실행 시간에 유형 변환이 발생할 수 있는 첫 번째 사례입니다.
유형 변환이 발생할 수 없다고 가정하는 분석 도구는 이 가능성을 고려하도록 업데이트해야 합니다.

## 포트

### Darwin
```
# Darwin
```

<!-- golang.org/issue/23011 -->
[공지](go1.16#darwin)된 바와 같이, Go 1.17은 macOS 10.13 High Sierra 또는 이후 버전을 필요로 합니다. 이전 버전 지원은 중단되었습니다.

### Windows

<!-- golang.org/issue/36439 -->
Go 1.17 버전에서 Windows ( `windows/arm64` 포트) 에서 64비트 ARM 아키텍처를 지원하는 기능이 추가되었습니다. 이 포트는 cgo를 지원합니다.

### OpenBSD {#openbsd}

<!-- golang.org/issue/43005 -->
64비트 MIPS 아키텍처 (OpenBSD의 `openbsd/mips64` 포트)에서 이제 cgo를 지원합니다.

<!-- golang.org/issue/36435 -->
Go 1.16 버전에서, OpenBSD (amd64 및 arm64 아키텍처의 `openbsd/amd64` 및 `openbsd/arm64` 포트)의 64비트 x86 및 64비트 ARM 아키텍처에서는 `libc`를 통해 시스템 호출이 수행됩니다. 대신, 직접적인 머신 명령어 사용은 하지 않습니다. Go 1.17 버전에서는 32비트 x86 및 32비트 ARM 아키텍처 (amd64 및 arm 포트의 `openbsd/386` 및 `openbsd/arm`)에서도 동일한 방식이 적용됩니다.
이는 OpenBSD 6.9 이상 버전과의 호환성을 보장하며, 이 버전들은 정적이지 않은 Go 바이너리에 대해 시스템 호출을 `libc`를 통해 수행하도록 요구합니다.

### ARM64 {#arm64}

<!-- CL 288814 -->
Go 프로그램은 64비트 ARM 아키텍처에서 모든 운영 체제에서 스택 프레임 포인터를 유지합니다. 이전에는 스택 프레임 포인터가 Linux, macOS 및 iOS에서만 활성화되었습니다.

### loong64 GOARCH 값 예약 {#loong64}

<!-- CL 333909 -->
메인 Go 컴파일러는 아직 LoongArch 아키텍처를 지원하지 않지만, `GOARCH` 값을 "`loong64`"으로 예약했습니다.
이것은 Go 파일 중 `*_loong64.go`라는 이름으로 작성된 파일이 Go 도구에 의해 [무시됩니다](/pkg/go/build/#hdr-Build_Constraints) (단, `GOARCH` 값이 사용되는 경우에만).

## 도구 {#tools}

### Go 명령어 {#go-명령어}

```md
<a id="lazy-loading"></a>
```

#### `go 1.17` 모듈에서 트리밍된 모듈 그래프 {#graph-pruning}

<!-- golang.org/issue/36460 -->
만약 모듈이 `go` `1.17` 또는 그 이상의 버전을 지정하면, 모듈
그래프에는 다른 `go` `1.17` 모듈의 _직접적인_ 종속성만 포함되며,
전체적인 추상 종속성은 포함되지 않습니다. (자세한 내용은 [모듈 그래프 절단](/ref/mod#graph-pruning) 참조.)

`go` 명령이 잘린 모듈 그래프를 사용하여 전이적 종속성을 올바르게 해결하려면, 각 모듈의 `go.mod` 파일에는 해당 모듈에 관련된 전이적 종속성에 대한 자세한 정보가 포함되어야 합니다.

만약 모듈이 `go.mod` 파일에 `go 1.17` 또는 그 이상의 버전을 지정하면, 해당 모듈의 `go.mod` 파일에는 전이적으로 가져온 패키지를 제공하는 모든 모듈에 대해 명시적인 `require` 지시문이 포함됩니다. (이전 버전에서는 `go.mod` 파일은 일반적으로 직접적으로 가져온 패키지에 대한 명시적인 요구 사항만 포함했습니다.)

이전 버전의 `go.mod` 파일이 모듈 그래프를 정리하는 데 필요한 모든 의존성을 포함하고 있기 때문에, 주요 모듈이 `go` 1.17 또는 그 이상의 버전을 지정하는 경우, `go` 도구가 필요한 의존성의 `go.mod` 파일을 읽거나 (또는 다운로드하지 않고) 요청된 명령을 완료하기 위해 필요하지 않은 경우에만 파일을 읽습니다. (참조: [지연 로딩](/ref/mod#lazy-loading).)

<!-- golang.org/issue/45965 -->
확장된 Go 1.17 `go.mod` 파일에는 명시적인 요구 사항 수가 훨씬 많을 수 있기 때문에, `go` 1.17 모듈에 추가된 간접 종속성의 요구 사항은 직접 종속성이 포함된 블록과 별도의 `require` 블록에 유지됩니다.

<!-- golang.org/issue/45094 -->
Go 1.17으로 업그레이드를 용이하게 하기 위해,
[`go` `mod` `tidy`](/ref/mod#go-mod-tidy)
명령이 이제 `-go` 플래그를 사용하여 `go.mod` 파일에 Go 버전을 설정하거나 변경할 수 있습니다. 기존 모듈의 `go.mod` 파일을 Go 1.17으로 변환하고, 선택한 의존성의 버전을 변경하지 않고 수행하려면 다음 명령을 실행하세요:

go mod tidy -go=1.17

<!-- golang.org/issue/46141 -->
기본적으로, `go` `mod` `tidy`는 메인 모듈에 관련된 의존성의 선택된 버전을 확인하여, 이전 Go 릴리스 (Go 1.16에 대한 모듈에서 `go` `1.17`을 지정한 경우)에서 사용될 버전과 동일한 버전을 사용하도록 합니다. 또한, 다른 명령에서 일반적으로 필요하지 않은 의존성에도 필요한 `go.sum` 항목을 유지합니다.

`-compat` 플래그를 사용하면 특정 버전을 재정의하여 이전 (또는 단지 최신) 버전을 지원할 수 있습니다. `go.mod` 파일의 `go` 지시어로 지정된 버전까지 지원합니다. Go 1.17만 사용하도록 Go 1.17 모듈을 정리하려면, Go 1.16에 대한 체크섬을 저장하거나 일관성을 확인하지 않도록 다음과 같이 설정할 수 있습니다:

go mod tidy -compat=1.17

참고: 메인 모듈이 `-compat=1.17`으로 정리되었더라도,
`require` 명령으로 모듈을 사용하는
`go` 1.16 또는 이전 버전의 모듈에서도,
패키지가 호환 가능한 언어 및 라이브러리 기능만 사용하면
이 모듈을 사용할 수 있습니다.

<!-- golang.org/issue/46366 -->
`go` `mod` `graph`
명령어도 `-go` 플래그를 지원하며, 이를 사용하면 지정된 Go 버전에서 그래프를 보고하여, 일반적으로 제거될 수 있는 종속성을 보여줍니다.

#### 모듈 사용 중단에 대한 설명 {#module-deprecation-comments}

<!-- golang.org/issue/40357 -->
모듈 작성자는 `go.mod` 파일에 `// Deprecated:`
주석을 추가하고 새로운 버전을 태그하여 모듈을 비활성화할 수 있습니다.
`go get` 명령에 지정된 패키지가 필요로 하는 모듈이 비활성화된 경우, `go`는 경고를 출력합니다. `go list -m -u`는 모든 종속성의 비활성화 정보를 출력합니다 (전체 메시지를 표시하려면 `-f` 또는 `-json`을 사용). `go` 명령은 서로 다른 주요 버전을 별도의 모듈로 간주하므로, 이 메커니즘을 사용하여 사용자가 새로운 주요 버전을 위한 마이그레이션 지침을 제공할 수 있습니다.

#### `go get` {#go-get}

<!-- golang.org/issue/37519 -->
`go`의 `get` 명령에 있는 `-insecure` 플래그는
더 이상 사용되지 않으며 제거되었습니다. 의사 모듈을 가져올 때 안전하지 않은 스킴을 사용하려면 `GOINSECURE`
환경 변수를 사용하십시오. `-insecure` 플래그는 또한 모듈의
합성 검사를 우회합니다. 필요한 경우 `GOPRIVATE` 또는 `GONOSUMDB`를 사용하십시오. 자세한 내용은 `go` `help`
`environment`를 참조하십시오.

<!-- golang.org/issue/43684 -->
`go get` 명령어를 메인 모듈 외부에서 설치할 때(`-d` 플래그 없이) 경고 메시지를 출력합니다.
특정 버전의 명령어를 설치하려면 `go install cmd@version`을 사용해야 합니다. 여기서 `version`은 `@latest` 또는 `@v1.2.3`과 같은 접미사를 포함합니다. Go 1.18에서는 `-d` 플래그가 항상 활성화되며, `go get`은 `go.mod` 파일의 종속성만 변경하는 데 사용됩니다.

#### `go.mod` 파일에 `go` 지시문 누락 {#missing-go-directive}

<!-- golang.org/issue/44976 -->
만약 메인 모듈의 `go.mod` 파일에 `go` 지시문이 없고, `go` 명령어가 `go.mod` 파일을 업데이트할 수 없는 경우,
`go` 명령은 현재 릴리스 대신 `go 1.11`을 사용합니다. (`go` `mod` `init`이 `go` 지시문을 자동으로 추가하기 시작했습니다 [Go 1.12 이후](/doc/go1.12#modules).)

<!-- golang.org/issue/44976 -->
만약 모듈 의존성이 명시적인 `go.mod` 파일을 가지고 있지 않거나,
또는 `go.mod` 파일에 `go` 지시문이 포함되어 있지 않다면,
`go` 명령어는 현재 버전 대신 해당 의존성에 대해 `go 1.16`을 사용합니다. (GOPATH 모드로 개발된 의존성은 `go.mod` 파일을 가지고 있지 않을 수 있으며,
`vendor/modules.txt`는 현재까지 의존성의 `go.mod` 파일에 지정된 `go` 버전을 기록하지 않았습니다.)

#### `vendor` 내용 {#vendor}

<!-- golang.org/issue/36876 -->
만약 메인 모듈이 `go` 1.17 또는 그 이상의 버전을 지정한다면,
[`go` `mod` `vendor`](/ref/mod#go-mod-vendor)는
각 벤더 모듈의 `go.mod` 파일에 지정된 `go` 버전을
`vendor/modules.txt`에 기록합니다. 이 버전은 벤더된 소스 코드에서 모듈의 패키지를 빌드할 때 사용됩니다.

<!-- golang.org/issue/42970 -->
만약 메인 모듈이 `go` `1.17` 또는 그 이상의 버전을 지정하면,
`go` `mod` `vendor`는 벤더된 종속성에 대한 `go.mod`
및 `go.sum` 파일을 더 이상 포함하지 않습니다. 이렇게 하면 `go` 명령어가 `vendor` 트리의 내부에서 호출될 때 올바른 모듈 루트를 식별하는 데 방해가 될 수 있습니다.

#### 비밀번호 요청 {#password-prompts}

<!-- golang.org/issue/44904 -->
`go` 명령은 기본적으로 SSH 비밀번호 프롬프트 및
Git Credential Manager 프롬프트를 비활성화하고, SSH를 사용하여 Git 저장소를 가져올 때 이전과 같이 다른 Git 비밀번호 프롬프트를 비활성화합니다. 사용자는 비밀번호 보호된 SSH를 사용하여 개인 Git 저장소에 인증할 때, `ssh-agent`를 구성하여 `go` 명령이 비밀번호 보호된 SSH 키를 사용할 수 있도록 할 수 있습니다.

#### `go` 모듈 다운로드 {#go-mod-download}

<!-- golang.org/issue/45332 -->
`go` `mod` `다운로드` 명령을 인수를 없이 호출하면, 다운로드한 모듈 콘텐츠의 합계를 더 이상 `go.sum`에 저장하지 않습니다. 하지만 빌드 목록을 로드하는 데 필요한 `go.mod` 및 `go.sum`에 대한 변경을 계속 수행할 수 있습니다. 이는 Go 1.15의 동작과 동일합니다. 모든 모듈에 대한 합계를 저장하려면 `go` `mod` `download all`을 사용하십시오.

#### `//go:build` 줄 {#build-줄}

`go` 명령은 이제 `//go:build` 줄을 이해하고, `// +build` 줄보다 선호합니다. 새로운 구문은 Go와 마찬가지로 부울 표현식을 사용하며, 오류 발생 가능성이 줄어듭니다. 이 릴리스부터, 새로운 구문은 완전히 지원되며, 모든 Go 파일은 동일한 의미로 두 가지 형식을 모두 갖도록 업데이트해야 합니다. 마이그레이션에 도움이 되도록, [`gofmt`](#gofmt)는 이제 자동으로 두 가지 형식을 동기화합니다. 구문 및 마이그레이션 계획에 대한 자세한 내용은 다음을 참조하십시오.
[https://golang.org/design/draft-gobuild](/design/draft-gobuild).

#### `go run` {#go_run}

<!-- golang.org/issue/42088 -->
`go run` 이제 버전 접미사와 함께 인수를 받습니다
(예: `go run example.com/cmd@v1.0.0`). 이를 통해 `go run`은 현재 디렉토리 또는 상위 디렉토리에 있는 `go.mod` 파일을 무시하고 모듈 인식 모드로 패키지를 빌드하고 실행합니다. 이를 통해 패키지를 설치하거나 현재 모듈의 종속성을 변경하지 않고 실행할 수 있습니다.

### Gofmt {#gofmt}

`gofmt` (및 `go` `fmt`) 이제 동기화됨
`//go:build` 라인을 `// +build` 라인과 함께 사용합니다. 만약 파일에
`// +build` 라인만 있다면, 해당 라인이 파일 내에 적절한 위치로 이동되고,
일치하는 `//go:build` 라인이 추가됩니다. 그렇지 않으면,
기존의 `//go:build` 라인을 기준으로 `// +build` 라인이 덮어쓰여집니다.
자세한 내용은 [https://golang.org/design/draft-gobuild](/design/draft-gobuild)를 참조하세요.

### 수의사 {#vet}

#### 일치하지 않는 `//go:build` 및 `// +build` 라인에 대한 새로운 경고 {#vet-buildtags}

<!-- CL 240609 -->
`vet` 도구가 이제 `//go:build` 및
`// +build` 라인이 올바른 파일 위치에 있고 서로
동기화되어 있는지 확인합니다. 그렇지 않은 경우,
[`gofmt`](#gofmt)를 사용하여 수정할 수 있습니다.
자세한 내용은 다음을 참조하십시오.
[https://golang.org/design/draft-gobuild](https://golang.org/design/draft-gobuild).

#### `signal.Notify`를 비버퍼링된 채널에서 호출하는 데 대한 새로운 경고 {#vet-sigchanyzer}

<!-- CL 299532 -->
이제 진료 도구가 `signal.Notify` 함수 호출에 대해 경고합니다.
이는 수신되는 신호가 버퍼되지 않은 채널로 전송되는 경우입니다. 버퍼되지 않은 채널을 사용하면 해당 채널을 통해 전송되는 신호를 놓칠 위험이 있습니다. `signal.Notify`는 채널로 전송할 때 차단되지 않기 때문입니다. 예를 들어:

```markdown
c := make(chan os.Signal)
    // 신호는 채널에서 읽기 전에 c에 전송됩니다.
    // 이 신호는 c가 버퍼링되지 않은 채널이기 때문에 손실될 수 있습니다.
    signal.Notify(c, os.Interrupt)
```

`signal.Notify`를 사용하는 사용자는 예상되는 신호 속도를 감당할 수 있도록 충분한 버퍼 공간을 가진 채널을 사용해야 합니다.

#### `Is`, `As` 및 `Unwrap` 메서드에 대한 새로운 경고 {#vet-error-stdmethods}

<!-- CL 321389 -->
이번에 제공되는 Veterinary Tool은 `error` 인터페이스를 구현하는 타입에서 `As`, `Is` 또는 `Unwrap`이라는 이름의 메서드에 대해 경고합니다. 특히, `errors.{As,Is,Unwrap}` 함수는 이러한 메서드가 다음과 같은 시그니처를 구현하도록 예상합니다.
* `Is(error)` `bool`
* `As(interface{})` `bool`
* `Unwrap()` `error`
하지만, 동일한 이름이지만 다른 시그니처를 가진 메서드는 무시합니다. 예를 들어:

```markdown
```go
type MyError struct {
	hint string
}

func (m MyError) Error() string {
	// ...
} // MyError는 error 인터페이스를 구현합니다.

func (MyError) Is(target interface{}) bool {
	// ... target은 interface{} 대신 error를 사용합니다.
}

func Foo() bool {
	x, y := MyError{"A"}, MyError{"B"}
	return errors.Is(x, y) // x != y 이므로 false를 반환하고, MyError에는 Is(error) bool 함수가 없습니다.
}
```

### 표지 {#cover}

<!-- CL 249759 -->
`cover` 도구가 이제 `golang.org/x/tools/cover`에서 최적화된 파서를 사용합니다. 이를 통해 대규모 커버리지 프로필을 파싱할 때 속도 향상을 확인할 수 있습니다.

## 컴파일러

<!-- golang.org/issue/40724 -->
Go 1.17은 스택 대신 레지스터를 사용하여 함수 인자와 결과를 전달하는 새로운 방법을 구현합니다.
대표적인 Go 패키지 및 프로그램에 대한 성능 테스트 결과, 약 5%의 성능 향상과 함께, 평균적으로 바이너리 크기가 약 2% 감소하는 것을 보여줍니다.
현재 이 기능은 64비트 x86 아키텍처 (linux/amd64, darwin/amd64, windows/amd64 포트)에서 Linux, macOS, Windows에서 활성화되어 있습니다.

이 변경 사항은 안전한 Go 코드의 기능을 변경하지 않으며, 대부분의 어셈블리 코드에 영향을 미치지 않도록 설계되었습니다.
`[`unsafe.Pointer`](/pkg/unsafe#Pointer) 규칙을 위반하는 코드, 특히 함수 인수를 사용할 때 또는 함수 코드 포인터를 비교하는 데 의존하는 코드에 영향을 미칠 수 있습니다.
기존 어셈블리 함수와의 호환성을 유지하기 위해, 컴파일러는 새로운 레지스터 기반 호출 규칙과 이전 스택 기반 호출 규칙 간에 변환하는 어댑터 함수를 생성합니다.
이 어댑터는 일반적으로 사용자에게는 보이지 않지만, 어셈블리 코드에서 Go 함수를 가져오거나 Go 코드에서 `reflect.ValueOf(fn).Pointer()` 또는 `unsafe.Pointer`를 사용하여 어셈블리 함수를 가져오는 경우, 어댑터의 주소를 반환합니다.
이 코드 포인터의 값을 의존하는 코드는 더 이상 예상대로 작동하지 않을 수 있습니다.
어댑터는 또한 다음과 같은 경우에 약간의 성능 오버헤드를 발생시킬 수 있습니다.
* `func` 값을 사용하여 어셈블리 함수를 간접적으로 Go에서 호출하는 경우
* 어셈블리에서 Go 함수를 호출하는 경우

<!-- CL 304470 -->
실행 시간에서 생성되는 스택 트레이스의 형식이 개선되었습니다 (예외가 발생하거나 `runtime.Stack`이 호출될 때 출력됨). 이전에는 함수 인수가 메모리 레이아웃을 기반으로 한 16진수 단어로 출력되었습니다. 이제 소스 코드의 각 인수는 쉼표로 구분하여 개별적으로 출력됩니다. 집합형(구조, 배열, 문자열, 슬라이스, 인터페이스, 복합형) 인수는 중괄호로 구분합니다. 주의할 점은, 메모리에 저장되지 않고 레지스터에만 존재하는 인수의 값은 부정확할 수 있다는 것입니다. 함수 반환 값(일반적으로 부정확했던)은 더 이상 출력되지 않습니다.

<!-- CL 283112, golang.org/issue/28727 -->
클로저를 포함하는 함수를 이제 인라인할 수 있습니다.
이 변경의 한 가지 효과는 클로저를 포함하는 함수가 함수가 인라인되는 각 위치에서
별도의 클로저 코드 포인터를 생성할 수 있다는 것입니다.
Go 함수 값은 직접 비교할 수 없지만, 이 언어 제약을 우회하여 `reflect` 또는 `unsafe.Pointer`를 사용하여 함수를 코드 포인터로 비교하는 코드가
있는 경우 이 변경으로 인해 버그가 드러날 수 있습니다.

### 링커 {#link}

<!-- CL 310349 -->
외부 링크 모드를 사용할 때, 링크어가 기본적으로 사용하는 방식이며, cgo를 사용하는 프로그램을 링크할 때 사용됩니다. 링크어를 `-I` 옵션으로 호출하면, 이 옵션이 이제 외부 링크어에 `-Wl,--dynamic-linker` 옵션으로 전달됩니다.

## 표준 라이브러리 {#library}

```go
package main

import (
	"fmt"
	"os"
)

func main() {
	// 표준 입력에서 읽기
	reader := os.Stdin
	input := reader.ReadString('\n')
	fmt.Println("입력:", input)

	// 표준 출력
	fmt.Println("Hello, world!")
}
```

### [Cgo](/pkg/runtime/cgo) {#runtime_cgo}

[runtime/cgo](/pkg/runtime/cgo) 패키지는 이제 새로운 기능을 제공하여, Go의 모든 값을 안전하게 표현하여 C와 Go 간에 안전하게 값을 전달할 수 있도록 합니다. 자세한 내용은 [runtime/cgo.Handle](/pkg/runtime/cgo#Handle)를 참조하십시오.

### URL 쿼리 파싱 {#semicolons}

<!-- CL 325697, CL 326309 -->

`net/url` 및 `net/http` 패키지는 URL 쿼리에 대해 `";"` (세미콜론) 뿐만 아니라 `&` (앰퍼샌드)를 설정 구분자로 사용했습니다. 이제, 퍼센트 인코딩되지 않은 세미콜론을 사용하는 설정은 거부되며, `net/http` 서버는 요청 URL에서 이를 발견할 때 `Server.ErrorLog`에 경고를 기록합니다.

예를 들어, Go 1.17 이전에는 `URL`의 `example?a=1;b=2&c=3`에 대한 [`Query`](/pkg/net/url#URL.Query) 메서드는 `map[a:[1] b:[2] c:[3]]`를 반환했지만, 현재는 `map[c:[3]]`를 반환합니다.

다음과 같은 쿼리 문자열을 처리할 때,
[`URL.Query`](/pkg/net/url#URL.Query)
과
[`Request.FormValue`](/pkg/net/http#Request.FormValue)
은 세미콜론을 포함하는 모든 설정을 무시하고,
[`ParseQuery`](/pkg/net/url#ParseQuery)
는 나머지 설정을 반환하고 오류를 반환하며,
[`Request.ParseForm`](/pkg/net/http#Request.ParseForm)
과
[`Request.ParseMultipartForm`](/pkg/net/http#Request.ParseMultipartForm)
는 오류를 반환하지만, 나머지 설정을 기반으로 `Request` 필드를 설정합니다.

`net/http` 사용자는 새
[`AllowQuerySemicolons`](/pkg/net/http#AllowQuerySemicolons)
핸들러 래퍼를 사용하여 원래 동작을 복원할 수 있습니다. 이는 `ErrorLog` 경고도 억제합니다.
주의: 쿼리 구분자로 세미콜론을 허용하면, 시스템마다 캐시 키를 다르게 해석하는 경우 보안 문제가 발생할 수 있습니다.
자세한 내용은 [issue 25192](/issue/25192)를 참조하십시오.

### 엄격한 TLS ALPN 설정 {#ALPN}

<!-- CL 289209, CL 325432 -->

`Config.NextProtos`가 설정되면, 서버는 클라이언트가 광고하는 ALPN 프로토콜 중, 구성된 프로토콜과 겹치는 프로토콜이 있는지 확인합니다. 만약 상호 지원되는 프로토콜이 없다면, `no_application_protocol` 알림을 사용하여 연결을 종료합니다 (RFC 7301 요구). 이는 [ALPACA 교차 프로토콜 공격](https://alpaca-attack.com/)을 완화하는 데 도움이 됩니다.

예외적으로, 서버의 `Config.NextProtos`에 `"h2"` 값이 포함된 경우, HTTP/1.1 클라이언트는 ALPN을 지원하지 않는 것처럼 연결할 수 있습니다.
자세한 내용은 [issue 46310](/issue/46310)를 참조하십시오.

### 라이브러리의 미세한 변경 사항 {#minor_library_changes}

물론, 라이브러리에는 다양한 미세한 변경 사항과 업데이트가 있으며, 이는 Go 1의 [호환성](https://doc/go1compat)을 염두에 두고 개발되었습니다.

#### [archive/zip](/pkg/archive/zip/)

<!-- CL 312310 -->
새로운 방법 [`File.OpenRaw`](/pkg/archive/zip#File.OpenRaw), [`Writer.CreateRaw`](/pkg/archive/zip#Writer.CreateRaw), [`Writer.Copy`](/pkg/archive/zip#Writer.Copy)는 성능이 주요 고려 사항인 경우를 지원합니다.

<!-- archive/zip -->

#### [bufio](/pkg/bufio/)

<!-- CL 280492 -->
`Writer.WriteRune` 메서드는 이제 음수 런 값에 대해 대체 문자를 U+FFFD로 쓰고
다른 유효하지 않은 런 값에 대해서도 동일하게 동작합니다.

<!-- bufio -->

#### [bytes](/pkg/bytes/)

<!-- CL 280492 -->
`Buffer.WriteRune` 메서드는 이제 음수 런에 대한 대체 문자를 U+FFFD로 쓰고,
다른 유효하지 않은 런의 경우에도 동일하게 동작합니다.

<!-- 바이트 -->

#### [compress/lzw](/pkg/compress/lzw/)

<!-- CL 273667 -->
`[NewReader](/pkg/compress/lzw/#NewReader)`
함수는 반드시 새로운
형식인 `[Reader](/pkg/compress/lzw/#Reader)`의 값을 반환하며,
마찬가지로 `[NewWriter](/pkg/compress/lzw/#NewWriter)`
함수는 반드시 새로운
형식인 `[Writer](/pkg/compress/lzw/#Writer)`의 값을 반환합니다.
이 새로운 형식 모두 `Reset` 메서드를 구현합니다 (`[Reader.Reset](/pkg/compress/lzw/#Reader.Reset)`,
`[Writer.Reset](/pkg/compress/lzw/#Writer.Reset)`).
이 메서드를 사용하여 `Reader` 또는 `Writer`를 재사용할 수 있습니다.

<!-- 압축/LZW -->

#### [crypto/ed25519](/pkg/crypto/ed25519/)

<!-- CL 276272 -->
`crypto/ed25519` 패키지가 다시 작성되었으며, amd64 및 arm64 아키텍처에서 모든 작업이 약 2배 더 빠릅니다.
관찰 가능한 동작은 다른 방식으로 변경되지 않았습니다.

<!-- crypto/ed25519 -->

```
#### [crypto/elliptic](/pkg/crypto/elliptic/)

<!-- CL 233939 -->
[`CurveParams`](/pkg/crypto/elliptic#CurveParams)
메서드가 이제 사용 가능한 알려진 곡선(P-224, P-256, P-521)에 대해 더 빠르고 안전한 전용 구현을 자동으로 호출합니다. 이 방법은 최선을 다하지만, 애플리케이션은 일반적인, 즉 항상 동일한 시간 복잡도를 가지는 `CurveParams` 메서드를 사용하지 않고, 대신 [`Curve`](/pkg/crypto/elliptic#Curve) 구현, 예를 들어 [`P256`](/pkg/crypto/elliptic#P256)와 같은 전용 구현을 사용해야 합니다.

<!-- CL 315271, CL 315274 -->
`P521` 곡선의
구현이 [fiat-crypto 프로젝트](https://github.com/mit-plv/fiat-crypto)에서 생성된 코드를 사용하여 다시 작성되었습니다. 이 코드는 산술 연산에 대한 공식적으로 검증된 모델을 기반으로 합니다. 이제 amd64 및 arm64에서 상수 시간 및 3배 더 빠릅니다. 관찰 가능한 동작은 변경되지 않았습니다.

```markdown
<!-- crypto/elliptic -->

```

#### [crypto/rand](/pkg/crypto/rand/)

<!-- CL 302489, CL 299134, CL 269999 -->
`crypto/rand` 패키지는 이제 macOS에서는 `getentropy` 시스템 호출, Solaris, Illumos, DragonFlyBSD에서는 `getrandom` 시스템 호출을 사용합니다.

```markdown
<!-- crypto/rand -->
```

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 295370 -->
새로운 `Conn.HandshakeContext` 방법은 사용자가 진행 중인 TLS 핸드셰이크를 취소할 수 있도록 합니다. 제공된 컨텍스트는 새로운 `ClientHelloInfo.Context` 및 `CertificateRequestInfo.Context` 메서드를 통해 다양한 콜백에서 액세스할 수 있습니다. 핸드셰이크가 완료된 후 컨텍스트를 취소하는 것은 아무런 효과가 없습니다.

<!-- CL 314609 -->
암호화 스위트의 순서는 이제 `crypto/tls` 패키지에 완전히 의해 관리됩니다. 현재, 암호화 스위트는 보안, 성능, 하드웨어 지원 측면에서 로컬 및 상대방의 하드웨어를 고려하여 정렬됩니다. 다음의
[`Config.CipherSuites`](/pkg/crypto/tls#Config.CipherSuites)
필드의 순서는 더 이상 무시되며,
[`Config.PreferServerCipherSuites`](/pkg/crypto/tls#Config.PreferServerCipherSuites)
필드도 무시됩니다. 참고로, `Config.CipherSuites`는 여전히 애플리케이션이 사용할 TLS 1.0–1.2 암호화 스위트를 선택할 수 있도록 합니다.

3DES 암호화 구성은 다음 위치로 이동되었습니다.
[`InsecureCipherSuites`](/pkg/crypto/tls#InsecureCipherSuites)
이는 [기본적인 블록 크기 관련 취약점](https://sweet32.info/) 때문입니다. 여전히 기본적으로 활성화되어 있지만, 위에서 언급한 암호화 구성 순서 변경 덕분에 최후의 수단으로만 사용됩니다.

<!-- golang.org/issue/45428 -->
다음 릴리스인 Go 1.18부터, `crypto/tls` 클라이언트에 대한 [`Config.MinVersion`](/pkg/crypto/tls/#Config.MinVersion)는 기본적으로 TLS 1.2로 설정되며, TLS 1.0 및 TLS 1.1을 기본적으로 비활성화합니다. 애플리케이션은 명시적으로 `Config.MinVersion`을 설정하여 이 변경 사항을 덮어쓸 수 있습니다.
이것은 `crypto/tls` 서버에 영향을 미치지 않습니다.

<!-- crypto/tls -->

#### [crypto/x509](/pkg/crypto/x509/)

<!-- CL 224157 -->
[`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate)
이제 제공된 개인 키가 부모의 공개 키와 일치하지 않는 경우 오류를 반환합니다. 결과로 생성된 인증서는 유효성 검사에 실패했을 것입니다.

<!-- CL 315209 -->
임시 `GODEBUG=x509ignoreCN=0` 플래그가 제거되었습니다.

<!-- CL 274234 -->
[`ParseCertificate`](/pkg/crypto/x509/#ParseCertificate)
이 부분이 재작성되었으며, 이제 ~70% 더 적은 리소스를 소비합니다. 웹PKI 인증서를 처리할 때 관찰 가능한 동작은 변경되지 않았습니다(오류 메시지만 제외).

<!-- CL 321190 -->
BSD 시스템에서는 `/etc/ssl/certs`에서 신뢰할 수 있는 루트 인증서를 찾습니다. 이는 FreeBSD 12.2 이상에서 새로운 시스템에서 신뢰하는 인증서 저장소를 지원합니다.

<!-- golang.org/issue/41682 -->
다음 릴리스인 Go 1.18부터, `crypto/x509`는 SHA-1 해시 함수로 서명된 인증서를 거부합니다. 이는 자체 서명된 루트 인증서에는 적용되지 않습니다. SHA-1에 대한 실질적인 공격은 2017년에 [시연되었습니다](https://shattered.io/)이며, 공신력 있는 인증 기관은 2015년 이후 SHA-1 인증서를 발급하지 않았습니다.

<!-- crypto/x509 -->

```
#### [database/sql](/pkg/database/sql/)
```

<!-- CL 258360 -->
`DB.Close` 메서드는 이제 `connector` 필드를 닫습니다. 이 필드의 유형이 `io.Closer` 인터페이스를 구현하는 경우.

<!-- CL 311572 -->
새로운
[`NullInt16`](/pkg/database/sql/#NullInt16)
및
[`NullByte`](/pkg/database/sql/#NullByte]
구조체는 null 값을 가질 수 있는 int16 및 바이트 값을 나타냅니다. 이러한 값은
`Scan` 메서드의
대상으로 사용될 수 있으며, 이는 NullString과 유사합니다.

<!-- 데이터베이스/SQL -->

#### [debug/elf](/pkg/debug/elf/)

<!-- CL 239217 -->
`[SHT_MIPS_ABIFLAGS]` 상수가 추가되었습니다.

<!-- 디버깅/ELF -->

#### [encoding/binary](/pkg/encoding/binary/)

<!-- CL 299531 -->
`binary.Uvarint`는 불필요한 계산을 피하기 위해 10 바이트를 읽은 후 더 이상 읽지 않습니다. 더 많은 바이트가 필요하면 반환되는 바이트 수는 -11입니다.
\
이전 Go 버전에서는 잘못 인코딩된 varint를 읽을 때 더 큰 음수 값을 반환할 수 있었습니다.

<!-- encoding/binary -->

#### [encoding/csv](/pkg/encoding/csv/)

<!-- CL 291290 -->
새로운
[`Reader.FieldPos`](/pkg/encoding/csv/#Reader.FieldPos)
메서드는 기록에서 가장 최근에 반환된 레코드 내의 특정 필드의 시작 위치에 해당하는 행과 열을 반환합니다.
[`Read`](/pkg/encoding/csv/#Reader.Read) 메서드가 반환한 레코드 내에서.

<!-- encoding/csv -->

#### [encoding/xml](/pkg/encoding/xml/)

<!-- CL 277893 -->
`<Directive>` 내에 나타나는 주석이 이제는 완전히 삭제되는 대신
단일 공백으로 대체됩니다.

다음과 같은 유효하지 않은 요소 또는 속성 이름 (앞, 뒤, 또는 여러 개의 콜론이 있는 경우)은 이제 `[Name.Local]`(`/pkg/encoding/xml/#Name`) 필드에 수정 없이 저장됩니다.

<!-- encoding/xml -->

#### [flag](/pkg/flag/)

<!-- CL 271788 -->
플래그 선언은 유효하지 않은 이름이 지정된 경우에 패닉을 발생시킵니다.

<!-- 깃발 -->

#### [go/build](/pkg/go/build/)

<!-- CL 310732 -->
새로운
[`Context.ToolTags`](/pkg/go/build/#Context.ToolTags)
필드는 현재 Go
툴체인 구성에 적합한 빌드 태그를 저장합니다.

<!-- go/build -->

#### [go/format](pkg/go/format/)

[`Source`](/pkg/go/format/#Source) 및
[`Node`](/pkg/go/format/#Node) 함수는 이제 `//go:build` 줄과 `// +build` 줄을 동기화합니다. 파일에 `// +build` 줄만 있는 경우, 해당 줄은 파일 내 적절한 위치로 이동되고, 일치하는 `//go:build` 줄이 추가됩니다. 그렇지 않으면, 기존 `//go:build` 줄에 따라 `// +build` 줄이 덮어쓰여집니다. 자세한 내용은 [https://golang.org/design/draft-gobuild](/design/draft-gobuild)를 참조하십시오.

<!-- go/format -->

#### [go/parser](pkg/go/parser/)

<!-- CL 306149 -->
새로운 `SkipObjectResolution` (`Mode` 값은 파서를 해당 식별자를 선언으로 해결하지 않도록 지시합니다. 이를 통해 파싱 속도를 향상시킬 수 있습니다. [pkg/go/parser/#SkipObjectResolution](https://example.com/pkg/go/parser/#SkipObjectResolution) 참조)

<!-- go/parser -->

#### [이미지](/pkg/image/)

<!-- CL 311129 -->
`RGBA`, `Gray16` 등과 같은 콘크리트 이미지 유형이
이제 새로운 [`RGBA64Image`](/pkg/image/#RGBA64Image) 인터페이스를 구현합니다.
이전에 `draw.Image`](/pkg/image/draw/#Image)를 구현하던 콘크리트 유형도
이제 `image/draw` 패키지의 새로운 인터페이스인
[`draw.RGBA64Image`](/pkg/image/draw/#RGBA64Image)를 구현합니다.

<!-- 이미지 -->

#### [io/fs](/pkg/io/fs/)

<!-- CL 293649 -->
새로운 [`FileInfoToDirEntry`](/pkg/io/fs/#FileInfoToDirEntry) 함수는 `FileInfo`를 `DirEntry`로 변환합니다.

<!-- io/fs -->

#### [math](pkg/math/)

<!-- CL 247058 -->
`math` 패키지는 이제 `MaxUint`, `MaxInt` 및 `MinInt`라는 세 가지 추가 상수를 정의합니다.
32비트 시스템의 경우, 각각의 값은 `2^32 - 1`, `2^31 - 1` 및 `-2^31`입니다.
64비트 시스템의 경우, 각각의 값은 `2^64 - 1`, `2^63 - 1` 및 `-2^63`입니다.

<!-- 수식 -->

#### [mime](/pkg/mime/)

<!-- CL 305230 -->
유닉스 시스템에서는 MIME 유형의 테이블이, 사용할 수 있는 경우 로컬 시스템의 [Shared MIME-info Database](https://specifications.freedesktop.org/shared-mime-info-spec/shared-mime-info-spec-0.21.html)에서 읽어옵니다.

<!-- mime -->

#### [mime/multipart](/pkg/mime/multipart/)

<!-- CL 313809 -->
[`Part.FileName`](/pkg/mime/multipart/#Part.FileName)
이제
[`filepath.Base`](/pkg/path/filepath/#Base)를 반환 값에 적용합니다. 이는 `net/http` 서버와 같이 멀티파트 메시지를 수신하는 애플리케이션에서 발생할 수 있는 잠재적인 경로 탐색 취약점을 완화합니다. 특히, `Request.FormFile`을 호출하는 서버에서 그렇습니다.

<!-- mime/multipart -->

#### [net](pkg/net/)

<!-- CL 272668 -->
새로운 방법 [`IP.IsPrivate`](/pkg/net/#IP.IsPrivate)는 주소가 [RFC 1918](https://datatracker.ietf.org/doc/rfc1918)에 따라 사설 IPv4 주소인지, 또는 [RFC 4193](https://datatracker.ietf.org/doc/rfc4193)에 따라 로컬 IPv6 주소인지 여부를 보고합니다.

<!-- CL 301709 -->
Go DNS 리졸버는 IPv4 또는 IPv6만 사용하는 네트워크의 주소를 해결할 때, IPv4 및 IPv6 두 가지 주소 유형에 대해 쿼리를 보내는 대신, 단 하나의 DNS 쿼리만 보냅니다.

<!-- CL 307030 -->
`[`ErrClosed`](/pkg/net/#ErrClosed) 및 `[`ParseError`](/pkg/net/#ParseError) 오류 유형이 이제 `net.Error`](/pkg/net/#Error) 인터페이스를 구현합니다.

<!-- CL 325829 -->
`[`ParseIP`](/pkg/net/#ParseIP) 및 `[`ParseCIDR`](/pkg/net/#ParseCIDR)
함수는 이제 0으로 시작하는 십진수 구성이 포함된 IPv4 주소를 거부합니다.
이 구성 요소는 항상 십진수로 해석되었지만, 일부 운영 체제에서는 이를 8진수로 처리합니다.
이 불일치는 Go 애플리케이션이 IP 주소를 유효성 검사하는 데 사용될 때 발생할 수 있으며, 이 주소가 원래 형식으로 다른 Go 애플리케이션(구성 요소를 8진수로 해석)에 사용될 경우 보안 문제가 발생할 수 있습니다. 일반적으로 유효성 검사 후 값을 다시 인코딩하는 것이 좋습니다. 이는 이러한 파서 호환성 문제를 방지합니다.

<!-- net -->

#### [net/http](pkg/net/http/)

<!-- CL 295370 -->
`net/http` 패키지는 이제 클라이언트 또는 서버에서 TLS 핸드셰이를 수행할 때,
`[*tls.Conn].HandshakeContext` 및 `Request` 컨텍스트를 사용합니다.

<!-- CL 235437 -->
[`Server`](/pkg/net/http/#Server)의 `ReadTimeout` 또는 `WriteTimeout` 필드를 음수 값으로 설정하면 더 이상 타임아웃이 발생하지 않음을 나타냅니다.

<!-- CL 308952 -->
`ReadRequest` 함수가 이제 요청에 여러 개의 `Host` 헤더가 있는 경우 오류를 반환합니다.

<!-- CL 313950 -->
URL의 정리된 버전으로 리디렉션을 생성할 때,
[`ServeMux`](/pkg/net/http/#ServeMux)는 이제 항상 `Location` 헤더에 상대 URL을 사용합니다. 이전에는 요청의 전체 URL을 반사했는데, 클라이언트가 절대 URL로 요청을 보내도록 유도될 수 있었고, 이는 의도하지 않은 리디렉션으로 이어질 수 있었습니다.

<!-- CL 308009, CL 313489 -->
`net/http`에서 처리하는 특정 HTTP 헤더를 해석할 때,
이제 비-ASCII 문자는 무시되거나 거부됩니다.

<!-- CL 325697 -->
만약
[`Request.ParseForm`](/pkg/net/http/#Request.ParseForm)
이
[`Request.ParseMultipartForm`](/pkg/net/http/#Request.ParseMultipartForm)
에 의해 호출될 때 오류를 반환하는 경우,
그 후에는
[`Request.MultipartForm`](/pkg/net/http/#Request.MultipartForm)
을 채우기 시작하고, 이를 반환하기 전에 계속 채웁니다.

<!-- net/http -->

#### [net/http/httptest](/pkg/net/http/httptest/)

<!-- CL 308950 -->
[`ResponseRecorder.WriteHeader`](/pkg/net/http/httptest/#ResponseRecorder.WriteHeader)
이제 제공된 코드가 유효한 세 자리 HTTP 상태 코드가 아니면 패닉(panic)을 발생시킵니다.
이는 [`ResponseWriter`](/pkg/net/http/#ResponseWriter) 구현체인 [`net/http`](/pkg/net/http/) 패키지 내에서 동작하는 방식과 일치합니다.

<!-- net/http/httptest -->

#### [net/url](pkg/net/url/)

<!-- CL 314850 -->
새로운 메서드 [`Values.Has`](/pkg/net/url/#Values.Has)는 쿼리 매개변수가 설정되었는지 여부를 보고합니다.

<!-- net/url -->

#### [os](/pkg/os/)

<!-- CL 268020 -->
`File.WriteString` 메서드가 최적화되어 입력 문자열을 복사하지 않습니다.

<!-- os -->

#### [reflect](/pkg/reflect/)

<!-- CL 334669 -->
새로운
[`Value.CanConvert`](/pkg/reflect/#Value.CanConvert)
메서드는 값이 특정 타입으로 변환될 수 있는지 여부를 보고합니다.
이는 슬라이스를 배열 포인터 타입으로 변환할 때, 슬라이스가 너무 짧은 경우에 패닉이 발생하는 것을 방지하는 데 사용될 수 있습니다.
이전에
[`Type.ConvertibleTo`](/pkg/reflect/#Type.ConvertibleTo)
를 사용하면 충분했지만, 슬라이스를 배열 포인터 타입으로 변환하는 새로운 허용된 변환은 타입이 변환 가능하다 하더라도 패닉을 발생시킬 수 있습니다.

<!-- CL 266197 -->
새로운
[`StructField.IsExported`](/pkg/reflect/#StructField.IsExported)
및
[`Method.IsExported`](/pkg/reflect/#Method.IsExported)
메서드는 구조 필드 또는 타입 메서드가 내보내지는지 여부를 보고합니다.
`PkgPath`가 비어 있는지 확인하는 것보다 더 읽기 쉬운 대안을 제공합니다.

<!-- CL 281233 -->
새로운 `VisibleFields` 함수는 (`/pkg/reflect/#VisibleFields`)
구조체 유형에 있는 모든 보이도록 설정된 필드를 반환하며, 여기에는 익명 구조체 멤버 내부의 필드도 포함됩니다.

<!-- CL 284136 -->
`[ArrayOf](/pkg/reflect/#ArrayOf)` 함수는 이제 음수 길이로 호출될 때 패닉을 발생시킵니다.

<!-- CL 301652 -->
`[Type.ConvertibleTo](pkg/reflect/#Type.ConvertibleTo)` 메서드를 확인하는 것만으로는 `[Value.Convert](pkg/reflect/#Value.Convert)` 호출이 예외를 발생시키지 않을 것이라고 보장할 수 없다는 것을 확인했습니다.
슬라이스의 길이가 N보다 작은 경우, `[]T`를 `\*[N]T`로 변환할 때 예외가 발생할 수 있습니다.
상단의 [언어 변경 사항](#language) 섹션을 참조하세요.

<!-- CL 309729 -->
`Value.Convert` 및
`Type.ConvertibleTo` 메서드가 수정되어, 동일한 이름을 가진 다른 패키지의 유형을 동일한 것으로 취급하지 않도록 하여, 언어가 허용하는 대로 작동합니다.

<!-- 반영 -->

#### [runtime/metrics](/pkg/runtime/metrics)

<!-- CL 308933, CL 312431, CL 312909 -->
전체 할당 및 해제된 바이트와 객체에 대한 추적을 위한 새로운 지표가 추가되었습니다.
또한, goroutine 스케줄링 지연의 분포를 추적하는 새로운 지표도 추가되었습니다.

<!-- runtime/metrics -->

#### [runtime/pprof](pkg/runtime/pprof)

<!-- CL 299991 -->
블록 프로파일이 더 이상 드문 장시간 이벤트보다 빈번한 짧은 이벤트를 선호하도록 편향되지 않습니다.

<!-- runtime/pprof -->

#### [strconv](/pkg/strconv/)

<!-- CL 170079, CL 170080 -->
`strconv` 패키지는 이제 Ulf Adams의 Ryū 알고리즘을 사용하여 부동 소수점 숫자를 형식화합니다.
이 알고리즘은 대부분의 입력에 대해 성능을 향상시키며, 최악의 경우 입력에 대해 99% 이상 빠릅니다.

<!-- CL 314775 -->
새로운 [`QuotedPrefix`](/pkg/strconv/#QuotedPrefix) 함수는
입력의 시작 부분에 있는 인용 문자열 ([`Unquote`](/pkg/strconv/#Unquote)에서 이해하는 대로)을 반환합니다.

```markdown
<!-- strconv -->
```

#### [strings](pkg/strings/)

<!-- CL 280492 -->
`Builder.WriteRune` 메서드는
이제 음수 런 값에 대해 U+FFFD 대체 문자를 쓰고,
다른 유효하지 않은 런 값에 대해서도 동일하게 동작합니다.

<!-- 문자열 -->

#### [sync/atomic](/pkg/sync/atomic/)

<!-- CL 241678 -->
`atomic.Value`는 이제 [`Swap`](/pkg/sync/atomic/#Value.Swap) 및
[`CompareAndSwap`](/pkg/sync/atomic/#Value.CompareAndSwap) 메서드를 제공하여
추가적인 원자적 연산을 제공합니다.

<!-- 동기화/원자성 -->

#### [syscall](/pkg/syscall/)

<!-- CL 295371 -->

[`GetQueuedCompletionStatus`](/pkg/syscall/#GetQueuedCompletionStatus) 및
[`PostQueuedCompletionStatus`](/pkg/syscall/#PostQueuedCompletionStatus)
함수는 이제 사용되지 않습니다. 이러한 함수는 잘못된 서명으로 되어 있으며,
[`golang.org/x/sys/windows`](https://godoc.org/golang.org/x/sys/windows) 패키지의
동등한 함수로 대체되었습니다.

<!-- CL 313653 -->
유닉스 계열 시스템에서는 자식 프로세스의 프로세스 그룹이 이제 신호를 차단하도록 설정됩니다.
이렇게 하면 부모 프로세스가 백그라운드 프로세스 그룹에 있을 때 자식 프로세스에 `SIGTTOU` 신호를 보내지 않도록 할 수 있습니다.

<!-- CL 288298, CL 288300 -->
Windows 버전의
[`SysProcAttr`](/pkg/syscall/#SysProcAttr)
에는 두 개의 새로운 필드가 추가되었습니다. `AdditionalInheritedHandles`는 새 자식 프로세스가 상속받을 추가 핸들의 목록입니다. `ParentProcess`는 새 프로세스의 부모 프로세스를 지정할 수 있도록 합니다.

<!-- CL 311570 -->
상수 `MSG_CMSG_CLOEXEC`가 이제 DragonFly 및 모든 OpenBSD 시스템에서 정의됩니다 (이미 일부 OpenBSD, FreeBSD, NetBSD 및 Linux 시스템에서 정의되어 있었습니다).

<!-- CL 315281 -->
상수 `SYS_WAIT6` 및 `WEXITED`는 이제 NetBSD 시스템에서 정의되었습니다 (`SYS_WAIT6`는 DragonFly 및 FreeBSD 시스템에서 이미 정의되었고, `WEXITED`는 Darwin, DragonFly, FreeBSD, Linux, Solaris 시스템에서 이미 정의되었습니다).

<!-- syscall -->

#### [테스팅](/pkg/testing/)

<!-- CL 310033 -->
`-shuffle`라는 새로운 테스트 플래그를 추가했습니다. 이 플래그는 테스트 및 벤치마크의 실행 순서를 제어합니다. (`/cmd/go/#hdr-Testing_flags` 참조)

<!-- CL 260577 -->
새로운
[`T.Setenv`](/pkg/testing/#T.Setenv)
및
[`B.Setenv`](/pkg/testing/#B.Setenv)
메서드는 테스트 또는 벤치마크의
전체 기간 동안 환경 변수를 설정하는 기능을 지원합니다.

<!-- 테스트 -->

#### [text/template/parse](/pkg/text/template/parse/)

<!-- CL 301493 -->
새로운 [`SkipFuncCheck`](/pkg/text/template/parse/#Mode) `Mode`
값은 템플릿 파서를 사용하여 함수가 정의되었는지 확인하지 않도록 변경합니다.

<!-- text/template/parse -->

#### [time](/pkg/time/)

<!-- CL 260858 -->
`Time` 타입에 이제 `GoString`
(`/pkg/time/#Time.GoString`) 메서드가 추가되어, `fmt` 패키지의 `%#v` 형식 지정자를 사용하여 출력할 때 더 유용한 값을 반환합니다.

<!-- CL 264077 -->
새로운 `Time.IsDST` 메서드는 구성된 위치에서 시간이 디저타임 (Daylight Savings Time)에 해당하는지 확인하는 데 사용할 수 있습니다.

<!-- CL 293349 -->
새로운 [`Time.UnixMilli`](/pkg/time/#Time.UnixMilli) 및
[`Time.UnixMicro`](/pkg/time/#Time.UnixMicro)
메서드는 각각 1월 1일 1970 UTC 이후 경과된 밀리초 및 마이크로초 수를 반환합니다.
\
새로운 [`UnixMilli`](/pkg/time/#UnixMilli) 및
[`UnixMicro`](/pkg/time/#UnixMicro) 함수는 주어진 유닉스 시간을 나타내는 로컬 `Time` 객체를 반환합니다.

<!-- CL 300996 -->
패키지는 시간 파싱 및 형식을 지정할 때 소수점 밀리초를 구분하는 데 쉼표 (",")를 허용합니다.
예를 들어, 다음 시간 형식은 이제 허용됩니다:

- 2006-01-02 15:04:05,999999999 -0700 MST
  - 월 1월 2일 15:04:05,000000 2006
  - 월요일, 1월 2일 15:04:05,000 2006

<!-- CL 320252 -->
새로운 상수 [`Layout`](/pkg/time/#Layout)
은 참조 시간을 정의합니다.

<!-- 시간 -->

#### [unicode](pkg/unicode/)

<!-- CL 280493 -->
`[`Is`](/pkg/unicode/#Is),
`[`IsGraphic`](/pkg/unicode/#IsGraphic),
`[`IsLetter`](/pkg/unicode/#IsLetter),
`[`IsLower`](/pkg/unicode/#IsLower),
`[`IsMark`](/pkg/unicode/#IsMark),
`[`IsNumber`](/pkg/unicode/#IsNumber),
`[`IsPrint`](/pkg/unicode/#IsPrint),
`[`IsPunct`](/pkg/unicode/#IsPunct),
`[`IsSpace`](/pkg/unicode/#IsSpace),
`[`IsSymbol`](/pkg/unicode/#IsSymbol), and
`[`IsUpper`](/pkg/unicode/#IsUpper) 함수는 이제 음수 런에 대한 값을 반환하며, 다른 유효하지 않은 런에 대해서도 동일하게 동작합니다.

<!-- 유니코드 -->
