<!--
참고: 이 문서 및 이 디렉토리에 있는 다른 문서에서, 고정 폭의 구문과 그렇지 않은 공백을 사용하는 규칙을 따릅니다. 예를 들어, <code>hello</code> <code>world</code>와 같이 사용합니다.
이러한 구문에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.22 소개 {#introduction}

## Overview
This document provides an overview of Go 1.22, including its new features, improvements, and changes.

## New Features
*   **Go 1.22 Release Notes:** [https://go.dev/doc/go1.22](https://go.dev/doc/go1.22)
*   **Go 1.22 Changelog:** [https://github.com/golang/go/releases/tag/go1.22.0](https://github.com/golang/go/releases/tag/go1.22.0)

## Improvements
*   **Performance Improvements:** Go 1.22 includes several performance improvements, including:
    *   Faster compilation times
    *   Improved garbage collection
    *   Optimized code generation

## Changes
*   **Deprecations:** Go 1.22 introduces several new deprecations. Please review the release notes for a complete list.
*   **Breaking Changes:** Go 1.22 introduces some breaking changes. Please review the release notes for a complete list.

## Getting Started
To get started with Go 1.22, you can:

*   Install the Go toolchain
*   Update your Go environment variables
*   Try out the new features and improvements

가장 최신 Go 릴리스인 버전 1.22는 [Go 1.21](/doc/go1.21) 이후 6개월 만에 출시되었습니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
물론, 이 릴리스는 Go 1의 [호환성 약속](/doc/go1compat)을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일 및 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

```
// Go package name: example
package example

// Identifier: myFunc
func myFunc() {
  // Inline code: fmt.Println("Hello, world!")
  fmt.Println("Hello, world!")
}
```

```
// URL: https://example.com
// Command: git clone https://example.com/repo.git
// Code snippet:
//   package main
//   import "fmt"
//   func main() {
//       fmt.Println("Hello, world!")
//   }
```

<!-- 반복 변수 범위 -->
<!-- 정수 범위에 대해 반복 -->
Go 1.22은 "for" 루프에 대해 두 가지 변경 사항을 도입했습니다.

- 이전에는 "for" 루프에 선언된 변수는 한 번 생성되고 각 반복에서 업데이트되었습니다. Go 1.22에서는 루프의 각 반복이 새로운 변수를 생성하여 의도하지 않은 공유 오류를 방지합니다.
    제안된 [전이 지원 도구]( /wiki/LoopvarExperiment#my-test-fails-with-the-change-how-can-i-debug-it)는 Go 1.21과 동일한 방식으로 작동합니다.
  - "for" 루프는 이제 정수를 반복할 수 있습니다.
    예를 들어: [ /play/p/ky02zZxgk_r?v=gotip]

```go
패키지 main
```

```
import "fmt"
```

```markdown
```go
package main {
    func main() {
    	  for i := range 10 {
    	    fmt.Println(10 - i)
    	  }
    	  fmt.Println("go1.22 has lift-off!")
    	}
```
```

자세한 내용은 [스펙](https://example.com/ref/spec#For_range)을 참조하십시오.

<!-- GOEXPERIMENT 범위 내의 함수 GOEXPERIMENT에 대한 테스트: https://go.dev/issue/61405, https://go.dev/issue/61897, CL 510541, 539277, 540263, 543319 -->

Go 1.22에는 미래의 Go 버전에서 고려 중인 언어 변경 사항의 미리보기 기능이 포함되어 있습니다: [range-over-function iterators](https://wiki/RangefuncExperiment).
`GOEXPERIMENT=rangefunc`로 빌드하면 이 기능을 활성화할 수 있습니다.

## 도구 {#tools}

### Go 명령어 {#go-command}

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, World!")
}
```

| 명령어 | 설명 |
|---|---|
| `go run` | Go 프로그램을 컴파일하고 실행합니다. |
| `go build` | Go 프로그램을 컴파일하여 실행 가능한 파일을 생성합니다. |
| `go test` | Go 프로그램의 테스트를 실행합니다. |
| `go get` | Go 모듈을 다운로드하고 설치합니다. |
| `go fmt` | Go 코드 스타일을 자동으로 포맷합니다. |

<!-- https://go.dev/issue/60056 -->

명령어는 이제 [작업 공간](/ref/mod#workspaces) 내에 있는 종속성을 포함하는 `vendor` 디렉토리를 사용할 수 있습니다. 이 디렉토리는 `go` `work` `vendor` 명령어로 생성되며, 빌드 명령어에서 `-mod` 플래그가 `vendor`로 설정될 때 사용됩니다. 이는 작업 공간 내에 `vendor` 디렉토리가 존재할 때 기본 설정입니다.

참고: 워크스페이스의 `vendor` 디렉토리 내용과 단일 모듈의 내용은 다릅니다. 워크스페이스의 루트 디렉토리에 있는 디렉토리가 워크스페이스 내의 하나의 모듈을 포함하는 경우, 해당 디렉토리의 `vendor` 디렉토리는 워크스페이스 또는 모듈의 종속성을 포함할 수 있지만, 둘 다 포함할 수는 없습니다.

<!-- CL 518775, https://go.dev/issue/60915 -->

`go get`는 레거시 `GOPATH` 모드(즉, `GO111MODULE=off`인 경우)에서 모듈 외부에서는 더 이상 지원되지 않습니다.
`go build` 및 `go test`와 같은 다른 빌드 명령어는 레거시 `GOPATH` 프로그램에 대해서는 계속 작동합니다.

<!-- CL 518776 -->

`go` `mod` `init`는 이제 다른 벤더링 도구(예: `Gopkg.lock`)에서 구성 파일로부터 모듈 요구 사항을 가져오려고 시도하지 않습니다.

<!-- CL 495447 -->

`go test -cover` 이제 코버리지 요약을 출력합니다.
자체 테스트 파일이 없는 패키지에 대해. Go 1.22 이전에는
`go test -cover` 명령이 이러한 패키지에 대해
보고했습니다.

`?     mymod/mypack    [테스트 파일 없음]`

그리고 Go 1.22부터, 패키지 내의 함수는 노출된 것으로 취급됩니다:

`mymod/mypack    코드 커버리지: 0.0%`

참고: 만약 패키지에 실행 가능한 코드가 전혀 없다면, 우리는 의미 있는 커버리지 비율을 보고할 수 없습니다. 그러한 패키지의 경우, `go` 도구는 여전히 테스트 파일이 없다는 것을 계속 보고합니다.

<!-- CL 522239, https://go.dev/issue/46330 -->

`go` 빌드 명령어에서 링커를 호출할 때, 외부 (C) 링커를 사용할 경우에만 오류가 발생합니다. 하지만 cgo가 활성화되지 않은 경우에는 오류가 발생합니다. (Go 런타임은 C 링커가 추가로 설치한 라이브러리와 호환되도록 cgo 지원이 필요합니다.)

### 추적 {#trace}

<!-- https://go.dev/issue/63960 -->

`trace` 도구의 웹 UI는 새로운 트레이서를 지원하기 위한 작업의 일환으로 부드럽게 업데이트되었습니다. 이를 통해 여러 문제를 해결하고 다양한 하위 페이지의 가독성을 개선했습니다.
이제 웹 UI는 스레드 기반의 방식으로 트레이스를 탐색할 수 있습니다.
트레이스 뷰어는 또한 모든 시스템 호출의 전체 지속 시간을 표시합니다.
\
이러한 개선 사항은 Go 1.22 또는 그 이상 버전으로 빌드된 프로그램에 의해 생성된 트레이스를 보는 데만 적용됩니다.
향후 릴리스에서는 이전 버전의 Go로 생성된 트레이스에도 일부 개선 사항이 적용될 예정입니다.

### 수의사 {#vet}

#### 루프 변수에 대한 참조 {#vet-loopclosure}

<!-- CL 539016, https://go.dev/issue/63888: cmd/vet: 루프 변수에 대한 새로운 규칙에 따라 변수 캡처에 대한 보고를 중단 -->
`vet` 도구의 동작은 Go 1.22의 새로운 의미(위 참조)에 따라 변경되었습니다.
Go 1.22 또는 그 이상 버전이 필요한 파일을 분석할 때 (go.mod 파일 또는 파일별 빌드 제약 조건으로 인해),
`vet`은 이제 루프 변수에서 호출된 참조를 더 이상 보고하지 않습니다.
Go 1.22에서는 루프 변수가 각 반복마다 새롭게 생성되므로, 이러한 참조가 루프에 의해 업데이트된 후에 변수를 사용하는 위험이 더 이상 없습니다.

#### 추가 후 누락된 값에 대한 새로운 경고 {#vet-appends}

<!-- CL 498416, https://go.dev/issue/60448: 추가 작업 후 누락된 값 확인을 위한 새로운 분석기 추가 -->
`vet` 도구가 이제 `append` 함수 호출을 보고합니다.
[`append`](/pkg/builtin/#append) 함수를 호출하여 슬라이스에 추가할 값을 전달하지 않는 경우, 예를 들어 `slice = append(slice)`와 같은 경우입니다.
이러한 문은 아무런 효과가 없으며, 경험적으로 보면 거의 항상 오류인 것으로 나타났습니다.

#### `time.Since`을 지연 호출하는 데 대한 새로운 경고 {#vet-defers}

<!-- CL 527095, https://go.dev/issue/60048: time.Since는 defer 문에서 사용해서는 안 됨 -->
`vet` 도구가 이제 `defer` 문 내에서 `time.Since(t)`를 호출하는 것을 보고합니다.
이는 `defer` 문이 호출되기 전에 `time.Now().Sub(t)`를 호출하는 것과 같습니다.
대부분의 경우, 올바른 코드는 `time.Since` 호출을 `defer` 해야 합니다. 예를 들어:

```markdown
t := time.Now()
	defer log.Println(time.Since(t))  // 시간 지연 없이 time.Since 호출
	tmp := time.Since(t); defer log.Println(tmp) // 위와 동일한 시간 지연
```

```
defer func() {
	  log.Println(time.Since(t)) // 올바르게 셔터링된 time.Since 호출
	}()
```

#### `log/slog` 호출 시 키-값 쌍 불일치에 대한 새로운 경고 {#vet-slog}

<!-- CL 496156, https://go.dev/issue/59407: log/slog: 추가된 vet 검사: 가변적인 ...any 입력에 대한 검사 -->
`vet` 도구가 이제 `log/slog` ([`log/slog`](/pkg/log/slog)) 패키지에 있는 구조화된 로깅 기능을 사용하는 함수 및 메서드 호출에 유효하지 않은 인수를 보고합니다.
특히, 키/값 쌍을 교대로 받는 함수/메서드 호출에서, 키 위치에 있는 인수가 `string`이 아니거나 `slog.Attr`가 아닐 때, 그리고 마지막 키에 값이 없을 때에 대한 보고를 합니다.

## 실행 시간 {#runtime}

<!-- CL 543255 -->
실행 시간은 이제 타입 기반의 가비지 컬렉션 메타데이터를 각 힙 객체에 더 가깝게 유지하여 Go 프로그램의 CPU 성능(지연 시간 또는 처리량)을 1~3% 향상시킵니다.
또한, 이 변경 사항은 대부분의 Go 프로그램의 메모리 오버헤드를 약 1% 줄여 중복된 메타데이터를 제거합니다.
일부 프로그램은 이 변경 사항이 메모리 할당기의 크기 범위를 조정하기 때문에 약간의 개선을 보일 수 있으며, 일부 객체가 크기 범위를 하나 올릴 수 있습니다.

이 변경의 결과로, 이전에 항상 16 바이트 (또는 그 이상의) 경계에 맞춰 정렬되던 일부 객체의 주소는 이제 8 바이트 경계로만 정렬됩니다.
메모리 할당기의 이전 정렬 동작에 의존하고, 8 바이트 이상의 정렬을 요구하는 어셈블리 명령어를 사용하는 일부 프로그램이 중단될 수 있지만, 이러한 프로그램은 드물 것으로 예상됩니다.
이러한 프로그램은 `GOEXPERIMENT=noallocheaders`를 사용하여 이전의 메타데이터 레이아웃으로 되돌리고, 이전의 정렬 동작을 복원할 수 있지만, 패키지 소유자는 어셈블리 코드를 업데이트하여 정렬을 가정하지 않도록 해야 합니다. 왜냐하면 이러한 임시 해결책은 향후 릴리스에서 제거될 예정이기 때문입니다.

<!-- CL 525475 -->
`windows/amd64` 포트에서, `-buildmode=c-archive` 또는 `-buildmode=c-shared`으로 빌드된 Go 라이브러리를 링크하거나 로드하는 프로그램은 이제 `SetUnhandledExceptionFilter` Win32 함수를 사용하여 Go 런타임에 의해 처리되지 않는 예외를 잡을 수 있습니다. 참고로, 이는 이미 `windows/386` 포트에서 지원되었습니다.

## 컴파일러

<!-- https://go.dev/issue/61577 -->
[프로파일 가이드 최적화 (PGO)](/doc/pgo)를 통해
이제 이전보다 더 많은 호출을 비가환화할 수 있습니다.
대표적인 Go 프로그램 집합에서 대부분의 프로그램은 PGO를 활성화했을 때 실행 시간에서 2~14%의 성능 향상을 보입니다.

<!-- https://go.dev/cl/528321 -->
컴파일러는 이제 데비어츄얼라이제이션과 인라인을 번갈아 사용하므로 인터페이스 메서드 호출이 더 잘 최적화됩니다.

<!-- https://go.dev/issue/61502 -->
Go 1.22에는 컴파일러의 인라인 단계를 개선한 구현의 미리보기 기능이 포함되어 있습니다. 이 기능은 "중요한" 위치(예: 루프)에서 인라인 가능성을 높이기 위해 휴리스틱을 사용하고, "중요하지 않은" 위치(예: 패닉 경로)에서의 인라인을 억제합니다.

`GOEXPERIMENT=newinliner`로 빌드하면 새로운 호출 위치 휴리스틱을 사용할 수 있습니다. 자세한 내용과 피드백을 제공하려면 [issue #61502](/issue/61502)를 참조하십시오.

## 링커 {#linker}

<!-- CL 493136 -->
링커의 `-s` 및 `-w` 플래그가 이제 모든 플랫폼에서 더 일관된 방식으로 동작합니다.
`-w` 플래그는 DWARF 디버그 정보 생성을 억제합니다.
`-s` 플래그는 심볼 테이블 생성을 억제합니다.
`-s` 플래그는 `-w` 플래그를 암시하며, 이는 `-w=0`로 부정될 수 있습니다.
즉, `-s -w=0`는 DWARF 디버그 정보 생성과 심볼 테이블 생성을 모두 수행하지만, 심볼 테이블은 생성하지 않습니다.

<!-- CL 511475 -->
ELF 플랫폼에서 `-B` 링커 플래그는 이제 특별한 형식을 지원합니다:
`-B` `gobuildid`를 사용하면 링커는 Go 빌드 ID에서 파생된 GNU 빌드 ID (ELF `NT_GNU_BUILD_ID` 노트)를 생성합니다.

<!-- CL 534555 -->
Windows에서 `-linkmode=internal`로 빌드할 때, 링커는 이제 C 오브젝트 파일에서 SEH(Stack Exception Handling) 정보를 복사하여 최종 바이너리에 `.pdata` 및 `.xdata` 섹션을 유지합니다.
이를 통해 WinDbg와 같은 네이티브 도구를 사용하여 바이너리를 디버깅하고 프로파일링하는 데 도움이 됩니다.
참고로, 지금까지 C 함수의 SEH 예외 처리기가 적용되지 않았으므로, 이 변경 사항으로 인해 일부 프로그램의 동작이 달라질 수 있습니다.
`-linkmode=external`은 이 변경 사항에 영향을 받지 않으며, 외부 링커는 이미 SEH 정보를 유지합니다.

## 부트스트랩 {#bootstrap}

다음과 같이 언급된 [Go 1.20 릴리스 노트](/doc/go1.20#bootstrap)에 따르면, Go 1.22에서는 bootstrap를 위해 Go 1.20의 최종 릴리스 버전 또는 이후 버전을 필요로 합니다.
Go 1.24는 bootstrap를 위해 Go 1.22의 최종 릴리스 버전 또는 이후 버전을 필요로 할 것으로 예상됩니다.

## 표준 라이브러리 {#library}

### 새로운 math/rand/v2 패키지 {#math_rand_v2}

<!-- CL 502495 -->
<!-- CL 502497 -->
<!-- CL 502498 -->
<!-- CL 502499 -->
<!-- CL 502500 -->
<!-- CL 502505 -->
<!-- CL 502506 -->
<!-- CL 516857 -->
<!-- CL 516859 -->

Go 1.22에는 표준 라이브러리에 처음 "v2" 패키지인 [`math/rand/v2`](/pkg/math/rand/v2/)가 포함됩니다.
[`math/rand`](/pkg/math/rand/)과의 변경 사항은 [제안 #61716](/issue/61716)에 자세히 설명되어 있습니다. 가장 중요한 변경 사항은 다음과 같습니다:

- `Read` 메서드, `math/rand`에서 더 이상 사용되지 않는,
    `math/rand/v2`에는 적용되지 않았습니다.
    (여전히 `math/rand`에서 사용 가능합니다.)
    대부분의 `Read` 호출은 `crypto/rand`의 `Read`를 사용해야 합니다.
    그렇지 않으면 `Uint64` 메서드를 사용하여 사용자 정의 `Read`를 구성할 수 있습니다.
  - 최상위 함수에서 액세스하는 전역 생성기는 무조건적으로 무작위로 시드됩니다.
    API가 고정된 결과 시퀀스를 보장하기 때문에,
    스레드별 무작위 생성기 상태와 같은 최적화가 가능합니다.
  - [`Source`](/pkg/math/rand/v2/#Source) 인터페이스는 이제 단일 `Uint64` 메서드만 가집니다.
    `Source64` 인터페이스는 없습니다.
  - 많은 메서드가 이제 더 빠르고 효율적인 알고리즘을 사용하는데, 이는 `math/rand`에서는 적용할 수 없었습니다.
    왜냐하면 이 알고리즘들이 출력 스트림을 변경했기 때문입니다.
  -
    `Intn`,
    `Int31`,
    `Int31n`,
    `Int63`,
    그리고
    `Int64n`
    `math/rand`의 최상위 함수 및 메서드는 `math/rand/v2`에서 더 자연스러운 방식으로 표현됩니다.
    `IntN`,
    `Int32`,
    `Int32N`,
    `Int64`,
    그리고
    `Int64N`.
    또한 새로운 최상위 함수 및 메서드인
    `Uint32`,
    `Uint32N`,
    `Uint64`,
    `Uint64N`,
    그리고
    `UintN`이 있습니다.
  -
    새로운 일반 함수 [`N`](/pkg/math/rand/v2/#N)은
    [`Int64N`](/pkg/math/rand/v2/#Int64N) 또는
    [`Uint64N`](/pkg/math/rand/v2/#Uint64N)과 유사하지만
    어떤 정수 유형에도 작동합니다.
    예를 들어 0부터 5분까지의 임의의 지속 시간을 얻는 것은
    `rand.N(5*time.Minute)`입니다.
  - `math/rand`의 `Source`에서 제공하는 Mitchell & Reeds LFSR 생성기는 다음과 같은 두 가지 더 현대적인 가짜 무작위 생성기 소스로 대체되었습니다.
    [`ChaCha8`](/pkg/math/rand/v2/#ChaCha8) 및
    [`PCG`](/pkg/math/rand/v2/#PCG).
    ChaCha8는 PCG와 유사하게 효율적인 새로운, 암호학적으로 강력한 무작위 숫자 생성기입니다.
    ChaCha8는 `math/rand/v2`의 최상위 함수에서 사용되는 알고리즘입니다.
    Go 1.22부터, `math/rand`의 최상위 함수 (명시적으로 시드되지 않은 경우)와 Go 런타임도 ChaCha8를 사용하여 무작위성을 제공합니다.

저희는 향후 릴리즈, 아마도 Go 1.23에서 API 마이그레이션 도구를 포함할 계획입니다.

### 새로운 go/version 패키지 {#go-version}

<!-- https://go.dev/issue/62039, https://go.dev/cl/538895 -->
새로운 `go/version` 패키지는 Go 버전 문자열의 유효성 검사와 비교를 위한 함수를 구현합니다.

### 향상된 라우팅 패턴 {#향상된_라우팅_패턴}

<!-- https://go.dev/issue/61410 -->
표준 라이브러리에서 HTTP 라우팅이 더욱 강력해졌습니다.
`net/http.ServeMux`에서 사용되는 패턴이 메서드 및 와일드카드를 허용하도록 개선되었습니다.

메서드와 함께 핸들러를 등록하는 경우, 예를 들어 `"POST /items/create"`와 같이, 해당 메서드에 대한 핸들러 호출만 허용됩니다. 메서드를 포함하는 패턴은 메서드가 없는 패턴보다 우선합니다.
특수한 경우로, `"GET"`과 함께 핸들러를 등록하면, `"HEAD"`와 함께 등록됩니다.

패턴 내의 와일드카드, 예: `/items/{id}`, 는 URL 경로의 세그먼트를 일치시킵니다.
실제 세그먼트 값을 액세스하려면 [`Request.PathValue`](/pkg/net/http#Request.PathValue) 메서드를 호출해야 합니다.
"..."로 끝나는 와일드카드, 예: `/files/{path...}`, 는 패턴의 끝에 있어야 하며 모든 나머지 세그먼트를 일치시킵니다.

`/`로 끝나는 패턴은 항상 해당 패턴을 접두어로 갖는 모든 경로와 일치합니다.
정확한 패턴(마지막 슬래시 포함)과 일치시키려면 `{$}`로 끝내십시오. 예: `/exact/match/{$}`

두 패턴이 요청에 일치하는 부분이 겹치는 경우, 더 구체적인 패턴이 우선 적용됩니다.
만약 두 패턴 모두 구체성이 없다면, 패턴 간에 충돌이 발생합니다.
이 규칙은 원래 우선순위 규칙을 일반화하고, 패턴이 등록되는 순서는 중요하지 않다는 속성을 유지합니다.

이 변경 사항은 작은 방식으로 이전 호환성을 깨뜨립니다. 예를 들어 "{" 및 "}"을 사용하는 패턴이 다르게 동작합니다.
또한, 이스케이프된 경로 처리가 개선되었습니다.
이 변경 사항은 `httpmuxgo121`이라는 이름의 [`GODEBUG`](/doc/godebug) 필드를 사용하여 제어됩니다.
이전 동작을 복원하려면 `httpmuxgo121=1`로 설정하십시오.

### 라이브러리의 소규모 변경 사항 {#minor_library_changes}

물론, 라이브러리에 대한 다양한 미세한 변경 사항 및 업데이트가 있으며, 이는 Go 1의 [호환성] 약속 [doc/go1compat]을 염두에 두고 이루어졌습니다.
또한, 여기에는 나열되지 않은 다양한 성능 개선 사항도 있습니다.

[archive/tar](/pkg/archive/tar/)

:   <!-- https://go.dev/issue/58000, CL 513316 -->
    새로운 방법 [`Writer.AddFS`](/pkg/archive/tar#Writer.AddFS)는 [`fs.FS`](/pkg/io/fs#FS)의 모든 파일을 아카이브에 추가합니다.

<!-- archive/tar -->

[archive/zip](/pkg/archive/zip/)

:   <!-- https://go.dev/issue/54898, CL 513438 -->
    새로운 메서드 [`Writer.AddFS`](/pkg/archive/zip#Writer.AddFS)는 [`fs.FS`](/pkg/io/fs#FS)의 모든 파일을 아카이브에 추가합니다.

<!-- archive/zip -->

[bufio](/pkg/bufio/)

:   <!-- https://go.dev/issue/56381, CL 498117 -->
    `SplitFunc`에서 `nil` 토큰과 함께 `ErrFinalToken`을 반환하는 경우, `Scanner`는 이제 즉시 중지됩니다.
    이전에는 중지하기 전에 최종 빈 토큰을 보고했지만, 이는 일반적으로 바람직하지 않았습니다.
    최종 빈 토큰을 보고하고 싶은 경우, `nil` 대신 `[]byte{}`를 반환하여 이를 수행할 수 있습니다.

<!-- bufio -->

[cmp](/pkg/cmp/)

:   <!-- https://go.dev/issue/60204 -->
    <!-- CL 504883 -->
    새로운 함수 `Or`는 값의 시퀀스 중 첫 번째 값이 0이 아닌 값을 반환합니다.

<!-- cmp -->

[crypto/tls](/pkg/crypto/tls/)

:   <!-- https://go.dev/issue/43922, CL 544155 -->
    [`ConnectionState.ExportKeyingMaterial`](/pkg/crypto/tls#ConnectionState.ExportKeyingMaterial)는 이제 TLS 1.3을 사용하거나, 서버와 클라이언트 모두 `extended_master_secret` 확장 기능을 지원하지 않는 경우에만
    성공합니다. `crypto/tls`는 Go 1.20부터 이 확장을 지원합니다. `tlsunsafeekm=1` GODEBUG 설정을 사용하여 이 기능을 비활성화할 수 있습니다.

<!-- https://go.dev/issue/62459, CL 541516 -->
    기본적으로 `crypto/tls` 서버에서 제공하는 최소 버전은 `config.MinimumVersion`으로 지정되지 않은 경우 TLS 1.2로 설정됩니다. 이는 `crypto/tls` 클라이언트의 동작과 일치합니다. 이 변경 사항은 `tls10server=1` GODEBUG 설정을 사용하여 되돌릴 수 있습니다.

<!-- https://go.dev/issue/63413, CL 541517 -->
    기본적으로, ECDHE를 지원하지 않는 암호 스위트는 TLS 1.3 이전의
    프리-TLS 핸드셰이크 단계에서 클라이언트 또는 서버에 의해 더 이상 제공되지 않습니다.
    이 변경 사항은 `tlsrsakex=1` GODEBUG 설정을 사용하여 되돌릴 수 있습니다.

<!-- crypto/tls -->

[crypto/x509](/pkg/crypto/x509/)

:   <!-- https://go.dev/issue/57178 -->
    새로운 [`CertPool.AddCertWithConstraint`](/pkg/crypto/x509#CertPool.AddCertWithConstraint)
    메서드를 사용하여, 체인 구축 중에 적용할 루트 인증서를 사용자 지정 제약 조건과 함께 추가할 수 있습니다.

<!-- https://go.dev/issue/58922, CL 519315-->
    안드로이드에서는 루트 인증서가 `/data/misc/keychain/certs-added` 뿐만 아니라 `/system/etc/security/cacerts`에서도 로드됩니다.

<!-- https://go.dev/issue/60665, CL 520535 -->
    새로운 타입인 [`OID`](/pkg/crypto/x509#OID)는 31비트보다 큰 개별 구성 요소가 있는 ASN.1 오브젝트 식별자를 지원합니다. 이 새로운 타입을 사용하는 새로운 필드인 [`Policies`](/pkg/crypto/x509#Certificate.Policies)가 `Certificate` 구조체에 추가되었으며, 이제 파싱 중에 채워집니다. [`asn1.ObjectIdentifier`](/pkg/encoding/asn1#ObjectIdentifier)를 사용하여 표현할 수 없는 모든 오브젝트 식별자는 `Policies` 필드에 나타나지만, 이전의 `PolicyIdentifiers` 필드에는 나타나지 않습니다.
    `CreateCertificate` 함수를 호출할 때, `Policies` 필드는 무시되며, 정책은 `PolicyIdentifiers` 필드에서 가져옵니다. `x509usepolicies=1` GODEBUG 설정을 사용하면, 이 동작이 반전되어, `Policies` 필드에서 인증서 정책을 가져오고 `PolicyIdentifiers` 필드를 무시합니다. Go 1.23에서 `x509usepolicies`의 기본값을 변경하여, `Policies` 필드를 기본 필드로 설정할 수 있습니다.

```markdown
<!-- crypto/x509 -->
```

[database/sql](/pkg/database/sql/)

:   <!-- https://go.dev/issue/60370, CL 501700 -->
    새로운 `Null[T]` 유형
    (`pkg/database/sql/#Null`)는 NULL 가능한 열을 스캔하여 모든 열 유형을 확인하는 방법을 제공합니다.

```markdown
<!-- database/sql -->
```

[디버깅/ELF](/pkg/debug/elf/)

:   <!-- https://go.dev/issue/61974, CL 469395 -->
    상수 `R_MIPS_PC32`는 MIPS64 시스템에서 사용하기 위해 정의되었습니다.

<!-- https://go.dev/issue/63725, CL 537615 -->
    LoongArch 시스템에서 사용하기 위한 추가적인 `R_LARCH_*` 상수가 정의되었습니다.

<!-- 디버깅/ELF -->

[인코딩](/pkg/encoding/)

:   <!-- https://go.dev/issue/53693, https://go.dev/cl/504884 -->
    `AppendEncode` 및 `AppendDecode` 메서드가 `encoding/base32` ([/pkg/encoding/base32]), `encoding/base64` ([/pkg/encoding/base64]), 및 `encoding/hex` ([/pkg/encoding/hex]) 패키지의 각 `Encoding` 유형에 추가되었습니다.
    이 메서드는 바이트 슬라이스 버퍼 관리를 처리하여 바이트 슬라이스로부터 인코딩 및 디코딩을 간소화합니다.

<!-- https://go.dev/cl/505236 -->
    메서드
    [`base32.Encoding.WithPadding`](/pkg/encoding/base32#Encoding.WithPadding) 및
    [`base64.Encoding.WithPadding`](/pkg/encoding/base64#Encoding.WithPadding)
    가 `padding` 인수가 음수 값인 경우 (단, `NoPadding`이 아닌 경우)에 패닉을 발생시킵니다.

<!-- 인코딩 -->

[encoding/json](/pkg/encoding/json/)

:   <!-- https://go.dev/cl/521675 -->
    마샬링 및 인코딩 기능이 이제
    `'\b'` 및 `'\f'` 문자를
    `\b` 및 `\f`로,
    `\u0008` 및 `\u000c`가 아닌
    으로 이스케이프합니다.

<!-- encoding/json -->

[go/ast](pkg/go/ast/)

:   <!-- https://go.dev/issue/52463, https://go/dev/cl/504915 -->
    다음은
    [구문 식별자 해결](https://pkg.go.dev/go/ast#Object)
    관련 선언이며 이제 [사용 중단]( /issue/52463)되었습니다.
    `Ident.Obj`,
    `Object`,
    `Scope`,
    `File.Scope`,
    `File.Unresolved`,
    `Importer`,
    `Package`,
    `NewPackage`.
    일반적으로 유형 정보를 가지고 있지 않으면 식별자를 정확하게 해결할 수 없습니다.
    예를 들어,
    `T{K: ""}`
    에서 식별자 `K`는 다음과 같습니다.
    만약 `T`가 맵 유형이면, 이는 지역 변수의 이름일 수 있고, 만약 `T`가 구조 유형이면, 이는 필드의 이름일 수 있습니다.
    새로운 프로그램은 식별자를 해결하기 위해 [go/types](/pkg/go/types) 패키지를 사용해야 합니다. 자세한 내용은 다음을 참조하세요.
    [`Object`](https://pkg.go.dev/go/types#Object),
    [`Info.Uses`](https://pkg.go.dev/go/types#Info.Uses),
    [`Info.Defs`](https://pkg.go.dev/go/types#Info.Defs)

<!-- https://go.dev/issue/60061 -->
    새로운 [`ast.Unparen`](https://pkg.go.dev/go/ast#Unparen)
    함수는 모든 래핑
    [괄호](https://pkg.go.dev/go/ast#ParenExpr)를
    [표현식](https://pkg.go.dev/go/ast#Expr)에서 제거합니다.

<!-- go/ast -->

[go/types](/pkg/go/types/)

:   <!-- https://go.dev/issue/63223, CL 521956, CL 541737 -->
    새로운 `Alias` 유형은 타입 별칭을 나타냅니다.
    이전에는 타입 별칭이 명시적으로 표현되지 않았기 때문에, 타입 별칭에 대한 참조는 별칭된 타입을 명시적으로 작성하는 것과 동일했으며, 별칭의 이름이 손실되었습니다.
    새로운 표현은 중간 `Alias`를 유지합니다.
    이를 통해 개선된 오류 보고가 가능합니다 (타입 별칭의 이름을 보고할 수 있음) 및 타입 별칭이 포함된 순환 타입 선언을 더 잘 처리할 수 있습니다.
    향후 릴리스에서는 `Alias` 유형도 [타입 매개변수 정보](/issue/46477)를 포함합니다.
    새로운 함수 `Unalias`는 `Alias` 유형으로 지정된 실제 타입을 반환합니다 (또는 어떤 `Type`이든).

이유는 `Alias` 타입이 기존의 타입 스위치를 파괴할 수 있으며, 이러한 스위치는 해당 타입을 확인하도록 설정되어 있지 않기 때문입니다.
    따라서, 이 기능은 `gotypesalias`라는 이름의 `GODEBUG` 필드를 사용하여 제어됩니다.
    `gotypesalias=0`인 경우, 모든 것이 이전과 동일하게 동작하며 `Alias` 타입은 생성되지 않습니다.
    `gotypesalias=1`인 경우, `Alias` 타입이 생성되며, 클라이언트는 이를 예상해야 합니다.
    기본값은 `gotypesalias=0`입니다.
    향후 릴리스에서는 기본값이 `gotypesalias=1`로 변경됩니다.
    _`go/types`의 클라이언트는 가능한 한 빨리 코드를 조정하여 `gotypesalias=1`과 함께 작동하도록 하는 것이 좋습니다. 이를 통해 문제를 조기에 해결할 수 있습니다._

<!-- https://go.dev/issue/62605, CL 540056 -->
    `Info` 구조체가 이제 `FileVersions` 맵을 내보냅니다.
    `FileVersions` 맵은 파일별 Go 버전 정보를 제공합니다.

<!-- https://go.dev/issue/62037, CL 541575 -->
    새로운 헬퍼 메서드 [`PkgNameOf`](/pkg/go/types#Info.PkgNameOf)는 주어진 가져오기 선언에 대한 로컬 패키지 이름을 반환합니다.

<!-- https://go.dev/issue/61035, 여러 CL, 자세한 내용은 이슈 참조 -->
    `SizesFor` 구현이 조정되어, 컴파일러 인수가 `"gc"`일 때 컴파일러와 동일한 타입 크기를 계산하도록 변경되었습니다.
    타입 검사기에서 사용되는 기본 `Sizes` 구현은 이제 `types.SizesFor("gc", "amd64")`입니다.

<!-- https://go.dev/issue/64295, CL 544035 -->
    어휘 환경 블록(`Scope`)의 시작 위치 ([`Pos`](/pkg/go/types#Scope.Pos))
    (함수 본체를 나타내는 것)은 변경되었습니다.
    이전에는 함수 본체의 중괄호에서 시작했지만, 이제는 함수의 `func` 토큰에서 시작합니다.

[html/템플릿](/pkg/html/template/)

:   <!-- https://go.dev/issue/61619, CL 507995 -->
    JavaScript 템플릿 리터럴은 이제 Go 템플릿 액션을 포함할 수 있으며, 이를 포함하는 템플릿을 파싱하면 더 이상 `ErrJSTemplate`가 반환되지 않습니다. 마찬가지로 `jstmpllitinterp` 설정인 GODEBUG는 더 이상 효과가 없습니다.

<!-- html/템플릿 -->

[io](/pkg/io/)

:   <!-- https://go.dev/issue/61870, CL 526855 -->
    새로운 `SectionReader.Outer` 메서드는 `NewSectionReader`에 전달된 `ReaderAt`, 오프셋, 크기를 반환합니다.

<!-- 입출력 -->

[log/slog](/pkg/log/slog/)

:   <!-- https://go.dev/issue/62418 -->
    새로운 `SetLogLoggerLevel` 함수는 `slog` 및 `log` 패키지 간의 브릿지에서 레벨을 제어합니다. 이 함수는 상위 레벨 `slog` 로깅 함수 호출에 대한 최소 레벨을 설정하고, `slog`를 통해 `log.Logger`에 호출되는 레벨을 설정합니다.

[math/big](/pkg/math/big/)

:   <!-- https://go.dev/issue/50489, CL 539299 -->
    새로운 메서드 [`Rat.FloatPrec`](/pkg/math/big#Rat.FloatPrec)는 주어진 유한비율(rational number)을 정확하게 부동 소수점 숫자로 표현하는 데 필요한 소수 자릿수를 계산하고, 정확한 소수 표현이 가능한지 여부를 판단합니다.

<!-- 수학/빅 -->

[net](/pkg/net/)

:   <!-- https://go.dev/issue/58808 -->
    `io.Copy`가 `TCPConn`에서 `UnixConn`으로 복사할 때,
    가능한 경우 Linux의 `splice(2)` 시스템 호출을 사용하며,
    새로운 방법인 `TCPConn.WriteTo`를 사용합니다.

<!-- CL 467335 -->
    -tags=netgo"으로 빌드할 때 사용되는 Go DNS 리졸버가,
    DNS 쿼리를 실행하기 전에,
    Windows 호스트 파일인 `%SystemRoot%\System32\drivers\etc\hosts`에서
    일치하는 이름을 검색합니다.

<!-- net -->

[net/http](/pkg/net/http/)

:   <!-- https://go.dev/issue/51971 -->
    새로운 함수
    [`ServeFileFS`](/pkg/net/http#ServeFileFS),
    [`FileServerFS`](/pkg/net/http#FileServerFS),
    [`NewFileTransportFS`](/pkg/net/http#NewFileTransportFS)
    는 기존의
    `ServeFile`, `FileServer`, `NewFileTransport` 함수의 새로운 버전으로, `fs.FS`를 사용합니다.

<!-- https://go.dev/issue/61679 -->
    HTTP 서버와 클라이언트는 이제 유효하지 않은 빈 `Content-Length` 헤더를 포함하는 요청 및 응답을 거부합니다.
    이전 동작은 `GODEBUG` 필드의 `httplaxcontentlength=1`을 설정하여 복원할 수 있습니다.

<!-- https://go.dev/issue/61410, CL 528355 -->
    새로운 메서드
    [`Request.PathValue`](/pkg/net/http#Request.PathValue)
    는 요청에서 경로 와일드카드 값을 반환합니다.
    그리고 새로운 메서드
    [`Request.SetPathValue`](/pkg/net/http#Request.SetPathValue)
    는 요청에 경로 와일드카드 값을 설정합니다.

<!-- net/http -->

[net/http/cgi](/pkg/net/http/cgi/)

:   <!-- CL 539615 -->
    CGI 프로세스를 실행할 때, `PATH_INFO` 변수는 이제 항상 빈 문자열 또는 `/` 문자로 시작하는 값으로 설정됩니다. 이는 RFC 3875 요구 사항을 충족합니다. 이전에는 `[Handler.Root](/pkg/net/http/cgi#Handler.Root)` 및 요청 URL의 특정 조합으로 인해 이 요구 사항이 위반될 수 있었습니다.

<!-- net/http/cgi -->

[net/netip](/pkg/net/netip/)

:   <!-- https://go.dev/issue/61642 -->
    새로운 [`AddrPort.Compare`](/pkg/net/netip#AddrPort.Compare)
    메서드는 두 개의 `AddrPort`를 비교합니다.

<!-- net/netip -->

[os](/pkg/os/)

:   <!-- CL 516555 -->
    Windows에서, [`Stat`](/pkg/os#Stat) 함수는 이제 시스템 내의 다른 이름이 지정된 엔티티에 연결된 모든 재파싱 지점을 따릅니다.
    이전에는 `IO_REPARSE_TAG_SYMLINK` 및 `IO_REPARSE_TAG_MOUNT_POINT` 재파싱 지점을만 따랐습니다.

<!-- CL 541015 -->
    Windows에서 [`O_SYNC`](/pkg/os#O_SYNC)를 [`OpenFile`](/pkg/os#OpenFile)에 전달하면, 쓰기 작업이 이제 직접 디스크로 전송되어, Unix 플랫폼에서 `O_SYNC`와 동일한 동작을 수행합니다.

<!-- CL 452995 -->
    Windows에서, [`ReadDir`](/pkg/os#ReadDir),
    [`File.ReadDir`](/pkg/os#File.ReadDir),
    [`File.Readdir`](/pkg/os#File.Readdir),
    그리고 [`File.Readdirnames`](/pkg/os#File.Readdirnames) 함수는 이제 디렉토리 항목을 일괄적으로 읽어 시스템 호출 횟수를 줄여 성능을 최대 30% 향상시킵니다.

<!-- https://go.dev/issue/58808 -->
    `[`io.Copy`](/pkg/io#Copy)가 `File`에서 `net.UnixConn`으로 복사할 때,
    가능한 경우 Linux의 `sendfile(2)` 시스템 호출을 사용하게 됩니다.
    새로운 메서드 `[`File.WriteTo`](/pkg/os#File.WriteTo)를 사용합니다.

<!-- os -->

[os/exec](/pkg/os/exec/)

:   <!-- CL 528037 -->
    Windows에서, [`LookPath`](/pkg/os/exec#LookPath)는 `%PATH%`에 있는 빈 항목을 이제 무시하고,
    명확하게 해석 가능한 이름이지만 실행 파일 확장자를 찾을 수 없는 경우
    `ErrNotFound` (예전의 `ErrNotExist` 대신)를 반환합니다.

<!-- CL 528038, CL 527820 -->
    Windows에서, `Command` 및 `Cmd.Start`는 실행 파일의 경로가 이미 절대 경로이고 실행 파일 확장자를 가지고 있는 경우에 `LookPath`를 더 이상 호출하지 않습니다. 또한, `Cmd.Start`는 해결된 확장자를 `Path` 필드로 다시 쓰지 않으므로, `Start` 호출과 함께 `String` 메서드를 동시에 호출하는 것이 안전합니다.

<!-- os/exec -->

[reflect](/pkg/reflect/)

:   <!-- https://go.dev/issue/61827, CL 517777 -->
    `Value.IsZero` ([/pkg/reflect/#Value.IsZero])
    메서드는 이제 부동 소수점 또는 복소수 형태의 음의 0에 대해 true를 반환하고, 또한 블랭크 필드 (이름이 `_`인 필드)가 비어 있지 않은 경우에 대해 구조체 값에 대해 true를 반환합니다.
    이러한 변경 사항은 `IsZero`를 언어 `==` 연산자를 사용하여 값을 0과 비교하는 것과 일관되게 만듭니다.

<!-- https://go.dev/issue/59599, CL 511035 -->
    `PtrTo` 함수는 더 이상 사용되지 않으며, 대신 `PointerTo` 함수를 사용해야 합니다.

<!-- https://go.dev/issue/60088, CL 513478 -->
    새로운 함수 [`TypeFor`](/pkg/reflect/#TypeFor)는
    `Type` (/[pkg/reflect/#Type])을 반환합니다.
    이 `Type`은 인자 T를 나타냅니다.
    이전에는 특정 유형의 `reflect.Type` 값을 얻으려면
    `reflect.TypeOf((*T)(nil)).Elem()`을 사용해야 했습니다.
    이제 이것은 `reflect.TypeFor[T]()`로 작성할 수 있습니다.

<!-- 반영 -->

[runtime/metrics](/pkg/runtime/metrics/)

:   <!-- https://go.dev/issue/63340 -->
    새로운 히스토그램 메트릭 4개
    `/sched/pauses/stopping/gc:seconds`,
    `/sched/pauses/stopping/other:seconds`,
    `/sched/pauses/total/gc:seconds`, 및
    `/sched/pauses/total/other:seconds`는 "스톱 더 월드" 멈춤에 대한 추가적인 정보를 제공합니다.
    "stopping" 메트릭은 세계를 멈추기로 결정한 시점부터 모든 고루틴이 멈출 때까지 걸리는 시간을 보고합니다.
    "total" 메트릭은 세계를 다시 시작할 때까지 멈추기로 결정한 시점부터 걸리는 시간을 보고합니다.

<!-- https://go.dev/issue/63340 -->
    `/gc/pauses:seconds` 메트릭은 더 이상 사용되지 않으며, 이는
    새로운 `/sched/pauses/total/gc:seconds` 메트릭과 동일합니다.

<!-- https://go.dev/issue/57071 -->
    `/sync/mutex/wait/total:seconds`는 이제 `sync.Mutex` 및 `sync.RWMutex` 외에도
    런타임 내부 잠금에 대한 경쟁도 포함합니다.

<!-- runtime/metrics -->

[runtime/pprof](/pkg/runtime/pprof/)

:   <!-- https://go.dev/issue/61015 -->
    뮤텍스 프로파일은 뮤텍스에서 차단된 고루틴의 수를 기준으로 경쟁을 스케일링합니다.
    이를 통해 뮤텍스가 Go 프로그램에서 얼마나 병목 현상을 일으키는지 보다 정확하게 나타낼 수 있습니다.
    예를 들어, 100개의 고루틴이 10밀리초 동안 뮤텍스에서 차단되면 뮤텍스 프로파일은 10밀리초의 지연 대신 1초의 지연을 기록합니다.

<!-- https://go.dev/issue/57071 -->
    Mutex 프로필은 `sync.Mutex` 및
    [`sync.RWMutex`](/pkg/sync#RWMutex) 외에도 런타임 내부 잠금에 대한 경쟁 상황을 포함합니다.
    런타임 내부 잠금에 대한 경쟁 상황은 항상 `runtime._LostContendedRuntimeLock`에서 보고됩니다.
    향후 릴리스에서는 이러한 경우에 완전한 스택 트레이스를 추가할 예정입니다.

<!-- https://go.dev/issue/50891 -->
    Darwin 플랫폼에서 생성되는 CPU 프로파일에는 프로세스의 메모리 맵 정보가 포함되어 있어, pprof 도구에서 디스어셈블 뷰를 사용할 수 있습니다.

<!-- runtime/pprof -->

[runtime/trace](/pkg/runtime/trace/)

:   <!-- https://go.dev/issue/60773 -->
    이번 릴리스에서는 실행 추적기가 완전히 재구축되었으며, 여러 오래된 문제를 해결하고 실행 추적에 대한 새로운 사용 사례를 열었습니다.

실행 추적은 대부분의 플랫폼(Windows 제외)에서 운영 체제의 클록을 사용하므로
    이를 하위 레벨 구성 요소에서 생성된 추적과 연결할 수 있습니다.
    실행 추적은 이제 플랫폼의 클록의 신뢰성에 의존하지 않습니다.
    실행 추적은 이제 정기적으로 생성되며, 결과적으로 스트리밍 방식으로 처리할 수 있습니다.
    실행 추적은 이제 모든 시스템 호출의 전체 지속 시간을 포함합니다.
    실행 추적은 이제 goroutine이 실행된 운영 체제 스레드에 대한 정보를 포함합니다.
    실행 추적을 시작하고 중지하는 데 따른 지연 영향이 크게 줄었습니다.
    실행 추적은 이제 가비지 컬렉션 마크 단계 중에 시작하거나 종료될 수 있습니다.

Go 개발자가 이러한 개선 사항을 활용할 수 있도록, 실험적인 추적 읽기 패키지가 [golang.org/x/exp/trace](https://golang.org/x/exp/trace)에 있습니다.
참고: 이 패키지는 현재 Go 1.22로 빌드된 프로그램에서 생성된 추적만 작동합니다.
패키지를 사용해 보고 [관련 제안 이슈](/issue/62627)에 피드백을 제공해 주시기 바랍니다.

만약 새로운 실행 추적 구현에 문제가 발생하면, `GOEXPERIMENT=noexectracer2`를 사용하여 Go 프로그램을 빌드함으로써 이전 구현으로 되돌릴 수 있습니다.
    이 경우, 문제점을 보고해 주십시오. 그렇지 않으면, 향후 릴리스에서 이 옵션이 제거됩니다.

<!-- runtime/trace -->

[슬라이스](/pkg/slices/)

:   <!-- https://go.dev/issue/56353 -->
    <!-- CL 504882 -->
    새로운 함수 `Concat`은 여러 슬라이스를 연결합니다.

<!-- https://go.dev/issue/63393 -->
    <!-- CL 543335 -->
    `Delete`, `DeleteFunc`, `Compact`, `CompactFunc`, 및 `Replace` 함수는 이제 새 길이와 이전 길이 사이의 요소를 0으로 설정합니다.

```
<!-- https://go.dev/issue/63913 -->
<!-- CL 540155 -->
`Insert` 함수는 이제 `i` 인자가 범위를 벗어나는 경우 항상 패닉(panic)을 발생시킵니다. 이전에는 요소가 삽입될 필요가 없는 경우에 패닉을 발생시키지 않았습니다.
```

<!-- 슬라이스 -->

[syscall](/pkg/syscall/)

:   <!-- https://go.dev/issue/60797 -->
    `syscall` 패키지는 Go 1.4부터 [동결](https://go.dev/issue/60797)되었으며, Go 1.11에서 사용 중단됨으로, 많은 에디터에서 해당 패키지의 사용에 대해 경고를 표시했습니다.
    그러나 일부 사용 중단되지 않은 기능은 `syscall` 패키지를 사용해야 합니다. 예를 들어, `os/exec.Cmd.SysProcAttr` 필드입니다.
    이러한 코드에 대한 불필요한 경고를 피하기 위해, `syscall` 패키지는 더 이상 사용 중단됨으로 표시되지 않습니다.
    패키지는 대부분의 새로운 기능에 대해 동결 상태를 유지하며, 새로운 코드는 가능한 경우 `golang.org/x/sys/unix` 또는 `golang.org/x/sys/windows`를 사용하는 것이 좋습니다.

<!-- https://go.dev/issue/51246, CL 520266 -->
    리눅스에서, 새로운 `SysProcAttr.PidFD` 필드는 `StartProcess` 또는 `os/exec`을 통해 자식 프로세스를 시작할 때, 프로세스 ID (PID) FD를 얻을 수 있도록 합니다.

<!-- CL 541015 -->
    Windows에서 [`O_SYNC`](/pkg/syscall#O_SYNC)를 [`Open`](/pkg/syscall#Open)에 전달하면, 쓰기 작업이 직접 디스크로 전송되어, Unix 플랫폼에서 `O_SYNC`와 동일한 동작을 수행합니다.

<!-- syscall -->

[testing/slogtest](/pkg/testing/slogtest/)

:   <!-- https://go.dev/issue/61758 -->
    새로운 `Run` 함수는 하위 테스트를 사용하여 테스트 케이스를 실행하며, 더 세분화된 제어를 제공합니다.

<!-- testing/slogtest -->

## 포트

### Darwin

<!-- CL 461697 -->
macOS에서 64비트 x86 아키텍처 (darwin/amd64 포트)에서,
Go 툴체인은 기본적으로 위치 독립 실행 파일 (PIE)을 생성합니다.
PIE가 아닌 바이너리는 `-buildmode=exe` 빌드 플래그를 지정하여 생성할 수 있습니다.
64비트 ARM 기반 macOS (darwin/arm64 포트)에서는,
Go 툴체인은 기본적으로 PIE를 생성합니다.

<!-- go.dev/issue/64207 -->
Go 1.22은 macOS 10.15 Catalina에서 실행되는 마지막 버전입니다. Go 1.23은 macOS 11 Big Sur 또는 이후 버전이 필요합니다.

### ARM {#arm}

<!-- CL 514907 -->
`GOARM` 환경 변수는 이제 소프트웨어 또는 하드웨어 플로팅 포인트를 선택할 수 있도록 합니다.
이전에는 유효한 `GOARM` 값은 `5`, `6` 또는 `7`이었습니다. 이제 이러한 값 뒤에 선택적으로 `,softfloat` 또는 `,hardfloat`을 추가하여 플로팅 포인트 구현을 선택할 수 있습니다.

이 새로운 옵션은 버전 `5`에는 기본적으로 `softfloat`을, 버전 `6` 및 `7`에는 `hardfloat`을 사용하도록 설정합니다.

### Loong64 {#loong64}

<!-- CL 481315 -->
`loong64` 포트가 이제 함수 인자와 결과를 레지스터를 사용하여 전달할 수 있도록 지원합니다.

<!-- CL 481315,537615,480878 -->
`linux/loong64` 포트는 이제 주소 분석기, 메모리 분석기, 새로운 스타일의 링커 위치 지정, 그리고 `plugin` 빌드 모드를 지원합니다.

### OpenBSD {#openbsd}

<!-- CL 517935 -->
Go 1.22 버전에서 OpenBSD에서 big-endian 64비트 PowerPC (`openbsd/ppc64`) 플랫폼용 실험적인 포트가 추가되었습니다.
