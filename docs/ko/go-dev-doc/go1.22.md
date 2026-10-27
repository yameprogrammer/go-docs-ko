<!--
참고: 이 문서 및 이 디렉토리의 다른 문서에서는
<code>hello</code> <code>world</code>와 같이 고정폭 문구 사이에
고정폭이 아닌 공백을 두는 관례를 따릅니다.
그러한 문구에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

제공해주신 내용이 스타일 시트(`<style>`)뿐이므로, 해당 부분은 기술적인 코드에 해당하여 번역하지 않고 그대로 유지합니다.

<style>
  main ul li { margin: 0.5em 0; }
</style>

## Go 1.22 소개 {#introduction}

최신 Go 릴리스인 버전 1.22가 [Go 1.21](/doc/go1.21) 이후 6개월 만에 출시되었습니다.
변경 사항의 대부분은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언제나 그렇듯, 이번 릴리스에서도 Go 1의 [호환성 약속](/doc/go1compat)을 유지합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

<!-- loop variable scope -->
<!-- range over int -->
Go 1.22에서는 "for" 루프에 두 가지 변경 사항이 도입되었습니다.

- 이전에는 "for" 루프에 의해 선언된 변수들이 한 번 생성되어 각 반복마다 업데이트되었습니다. Go 1.22에서는 의도치 않은 공유 버그를 방지하기 위해 루프의 각 반복마다 새로운 변수가 생성됩니다.
    제안서에 설명된 [전환 지원 도구](/wiki/LoopvarExperiment#my-test-fails-with-the-change-how-can-i-debug-it)는 Go 1.21에서와 동일한 방식으로 계속 작동합니다.
  - 이제 "for" 루프에서 정수(integers)에 대해 range를 사용할 수 있습니다.
    [예시](/play/p/ky02zZxgk_r?v=gotip)는 다음과 같습니다:

`package main`

```go
import "fmt"
```

```go
func main() {
    	  for i := range 10 {
    	    fmt.Println(10 - i)
    	  }
    	  fmt.Println("go1.22 has lift-off!")
    	}
```

[상세 내용](/ref/spec#For_range)은 명세서를 참조하십시오.

<!-- range over func GOEXPERIMENT; https://go.dev/issue/61405, https://go.dev/issue/61897, CLs 510541,539277,540263,543319 -->

Go 1.22에는 향후 Go 버전에서 고려 중인 언어 변경 사항의 프리뷰가 포함되어 있습니다: [range-over-function iterators](/wiki/RangefuncExperiment). `GOEXPERIMENT=rangefunc`와 함께 빌드하면 이 기능을 활성화할 수 있습니다.

## Tools {#tools}

### Go command {#go-command}

<!-- https://go.dev/issue/60056 -->

[workspaces](/ref/mod#workspaces)의 명령어들은 이제 워크스페이스의 의존성들이 포함된 `vendor` 디렉토리를 사용할 수 있습니다. 이 디렉토리는 [`go` `work` `vendor`](/pkg/cmd/go#hdr-Make_vendored_copy_of_dependencies) 명령어로 생성되며, `-mod` 플래그가 `vendor`로 설정되었을 때 빌드 명령어에 의해 사용됩니다. 워크스페이스 `vendor` 디렉토리가 존재할 경우 `vendor`가 기본값으로 설정됩니다.

워크스페이스의 `vendor` 디렉터리 내용은 단일 모듈의 경우와 다르다는 점에 유의하십시오. 워크스페이스 루트에 있는 디렉터리가 워크스페이스 내의 모듈 중 하나를 포함하고 있는 경우, 해당 `vendor` 디렉터리는 워크스페이스의 의존성 또는 모듈의 의존성 중 하나만 포함할 수 있으며, 둘 다 포함할 수는 없습니다.

<!-- CL 518775, https://go.dev/issue/60915 -->

레거시 `GOPATH` 모드(즉, `GO111MODULE=off`인 상태)에서 모듈 외부의 `go` `get`은 더 이상 지원되지 않습니다.
`go` `build` 및 `go` `test`와 같은 다른 빌드 명령은 레거시 `GOPATH` 프로그램에 대해 계속해서 무기한으로 작동합니다.

<!-- CL 518776 -->

`go` `mod` `init`은 더 이상 다른 벤더링 도구의 설정 파일(예: `Gopkg.lock`)로부터 모듈 요구 사항을 가져오지 않습니다.

<!-- CL 495447 -->

`go` `test` `-cover` 명령어가 이제 자체 테스트 파일이 없는 커버리지 대상 패키지에 대해서도 커버리지 요약을 출력합니다. Go 1.22 이전에는 이러한 패키지에 대해 `go` `test` `-cover`를 실행하면 다음과 같이 보고되었습니다.

`?     mymod/mypack    [no test files]`

그리고 이제 Go 1.22부터는, 패키지 내의 함수들이 uncovered(테스트되지 않음)로 처리됩니다:

`mymod/mypack    coverage: 0.0% of statements`

패키지에 실행 가능한 코드가 전혀 포함되어 있지 않은 경우, 의미 있는 커버리지 백분율을 보고할 수 없다는 점에 유의하십시오. 이러한 패키지에 대해 `go` 도구는 테스트 파일이 없다고 계속 보고합니다.

<!-- CL 522239, https://go.dev/issue/46330 -->

외부(C) 링커가 사용되지만 cgo가 활성화되지 않은 경우, 이제 링커를 호출하는 `go` build 명령에서 에러가 발생합니다. (Go 런타임은 C 링커에 의해 추가된 모든 라이브러리와의 호환성을 보장하기 위해 cgo 지원을 필요로 합니다.)

### Trace {#trace}

<!-- https://go.dev/issue/63960 -->

`trace` 도구의 웹 UI가 새로운 tracer를 지원하기 위한 작업의 일환으로 가볍게 업데이트되었으며, 이를 통해 여러 이슈가 해결되고 다양한 하위 페이지의 가독성이 향상되었습니다.
이제 웹 UI에서 스레드 중심 뷰(thread-oriented view)로 트레이스를 탐색할 수 있습니다.
또한 트레이스 뷰어에서 모든 시스템 콜의 전체 지속 시간이 표시됩니다.
\
이러한 개선 사항은 Go 1.22 또는 그 이후 버전으로 빌드된 프로그램이 생성한 트레이스를 볼 때만 적용됩니다.
향후 릴리스에서는 이전 버전의 Go가 생성한 트레이스에도 이러한 개선 사항 일부가 적용될 예정입니다.

### Vet {#vet}

#### 루프 변수에 대한 참조 {#vet-loopclosure}

<!-- CL 539016, https://go.dev/issue/63888: cmd/vet: do not report variable capture for loop variables with the new lifetime rules -->
`vet` 도구의 동작이 Go 1.22의 루프 변수에 대한 새로운 시맨틱(위 내용 참조)에 맞게 변경되었습니다.
`go.mod` 파일이나 파일별 빌드 제약 조건으로 인해 Go 1.22 이상 버전이 필요한 파일을 분석할 때, `vet`은 루프 반복보다 더 오래 유지될 수 있는 함수 리터럴 내에서 루프 변수를 참조하는 경우를 더 이상 보고하지 않습니다.
Go 1.22에서는 루프 변수가 매 반복마다 새로 생성되므로, 이러한 참조는 루프에 의해 변수가 업데이트된 후 해당 변수를 사용하게 될 위험이 더 이상 없습니다.

#### append 후 누락된 값에 대한 새로운 경고 {#vet-appends}

<!-- CL 498416, https://go.dev/issue/60448: add a new analyzer for check missing values after append -->
이제 `vet` 도구는 `slice = append(slice)`와 같이 슬라이스에 추가할 값을 전달하지 않는 [`append`](/pkg/builtin/#append) 호출을 보고합니다.
이러한 문장은 아무런 효과가 없으며, 경험상 이는 거의 항상 실수인 것으로 나타났습니다.

#### `time.Since` 지연 호출(defer)에 대한 새로운 경고 {#vet-defers}

<!-- CL 527095, https://go.dev/issue/60048: time.Since should not be used in defer statement -->
이제 vet 도구는 `defer` 문 내에서 지연되지 않은 [`time.Since(t)`](/pkg/time/#Since) 호출을 보고합니다.
이는 `defer` 문이 실행될 때가 아니라, `defer` 문 이전에 `time.Now().Sub(t)`를 호출하는 것과 동일합니다. 거의 모든 경우에 올바른 코드는 `time.Since` 호출 자체를 지연시키는 것입니다. 예를 들어:

```go
t := time.Now()
	defer log.Println(time.Since(t)) // time.Since에 대한 비지연(non-deferred) 호출
	tmp := time.Since(t); defer log.Println(tmp) // 이전 defer와 동일한 동작
```

```go
defer func() {
	  log.Println(time.Since(t)) // time.Since에 대한 올바른 지연 호출(deferred call)
	}()
```

#### `log/slog` 호출 시 일치하지 않는 키-값 쌍에 대한 새로운 경고 {#vet-slog}

<!-- CL 496156, https://go.dev/issue/59407: log/slog: add vet checks for variadic ...any inputs -->
이제 vet 도구는 키/값 쌍을 교대로 받는 구조화된 로깅 패키지 [`log/slog`](/pkg/log/slog)의 함수 및 메서드 호출에서 잘못된 인수를 보고합니다.
키 위치의 인수가 `string`이나 `slog.Attr`이 아니거나, 마지막 키에 해당하는 값이 누락된 호출을 보고합니다.

## 런타임 {#runtime}

<!-- CL 543255 -->
런타임이 이제 타입 기반 가비지 컬렉션 메타데이터를 각 힙 객체에 더 가깝게 유지하여, Go 프로그램의 CPU 성능(지연 시간 또는 처리량)을 1~3% 향상시킵니다.
또한, 이 변경 사항은 중복된 메타데이터를 제거함으로써 대부분의 Go 프로그램에서 메모리 오버헤드를 약 1% 줄여줍니다.
일부 프로그램에서는 개선 폭이 더 작을 수 있는데, 이는 이 변경 사항이 메모리 할당자의 크기 클래스(size class) 경계를 조정하므로 일부 객체가 더 높은 크기 클래스로 이동할 수 있기 때문입니다.

이 변경 사항의 결과로, 이전에는 항상 16바이트(또는 그 이상) 경계로 정렬되었던 일부 객체의 주소가 이제는 8바이트 경계로만 정렬됩니다.

메모리 주소가 8바이트보다 더 큰 단위로 정렬되어야 하는 어셈블리 명령어를 사용하며 메모리 할당자의 이전 정렬 동작에 의존하는 일부 프로그램은 작동하지 않을 수 있으나, 이러한 프로그램은 드물 것으로 예상됩니다.

이러한 프로그램은 `GOEXPERIMENT=noallocheaders`와 함께 빌드하여 이전의 메타데이터 레이아웃으로 되돌리고 이전의 정렬 동작을 복구할 수 있습니다. 하지만 이 임시 방편은 향후 릴리스에서 제거될 예정이므로, 패키지 소유자는 정렬 가정을 피하도록 어셈블리 코드를 업데이트해야 합니다.

<!-- CL 525475 -->
`windows/amd64 port`에서 `-buildmode=c-archive` 또는 `-buildmode=c-shared`로 빌드된 Go 라이브러리를 링크하거나 로드하는 프로그램은 이제 `SetUnhandledExceptionFilter` Win32 함수를 사용하여 Go 런타임에서 처리되지 않은 예외를 포착할 수 있습니다. 이는 `windows/386` port에서 이미 지원되고 있었음을 참고하십시오.

## 컴파일러 {#compiler}

<!-- https://go.dev/issue/61577 -->
[Profile-guided Optimization (PGO)](/doc/pgo) 빌드에서 이제 이전보다 더 높은 비율의 호출을 devirtualize할 수 있습니다.
대표적인 Go 프로그램 세트로 테스트한 결과, 대부분의 프로그램에서 PGO를 활성화했을 때 런타임 성능이 2%에서 14% 사이로 향상되었습니다.

<!-- https://go.dev/cl/528321 -->
이제 컴파일러가 devirtualization과 inlining을 교차로 수행하여, 인터페이스 메서드 호출이 더 효율적으로 최적화됩니다.

<!-- https://go.dev/issue/61502 -->
Go 1.22에는 컴파일러 인라이닝 단계의 개선된 구현에 대한 프리뷰가 포함되어 있습니다. 이 구현은 휴리스틱을 사용하여 "중요한" 호출 지점(예: 루프 내부)의 인라이닝 가능성을 높이고, "중요하지 않은" 호출 지점(예: panic 경로)의 인라이닝은 억제합니다.
`GOEXPERIMENT=newinliner`를 설정하여 빌드하면 새로운 호출 지점 휴리스틱이 활성화됩니다. 자세한 정보 확인 및 피드백 제공은 [issue #61502](/issue/61502)를 참조하십시오.

## Linker {#linker}

<!-- CL 493136 -->
이제 링커의 `-s` 및 `-w` 플래그가 모든 플랫폼에서 더 일관되게 동작합니다.
`-w` 플래그는 DWARF 디버그 정보 생성을 억제합니다.
`-s` 플래그는 심볼 테이블 생성을 억제합니다.
또한 `-s` 플래그는 `-w` 플래그를 포함하며, 이는 `-w=0`으로 부정할 수 있습니다.
즉, `-s` `-w=0`은 심볼 테이블은 없지만 DWARF 디버그 정보 생성은 포함된 바이너리를 생성합니다.

<!-- CL 511475 -->
ELF 플랫폼에서 `-B` 링커 플래그가 이제 특수한 형태를 지원합니다:
`-B` `gobuildid`를 사용하면, 링커는 Go 빌드 ID(Go build ID)에서 파생된 GNU 빌드 ID(ELF `NT_GNU_BUILD_ID` 노트)를 생성합니다.

<!-- CL 534555 -->
Windows에서 `-linkmode=internal`로 빌드할 때, 이제 링커가 `.pdata` 및 `.xdata` 섹션을 최종 바이너리로 복사함으로써 C 객체 파일의 SEH 정보를 보존합니다.
이는 WinDbg와 같은 네이티브 도구를 사용하여 바이너리를 디버깅하고 프로파일링하는 데 도움이 됩니다.
지금까지는 C 함수의 SEH 예외 핸들러가 준수되지 않았으므로, 이 변경으로 인해 일부 프로그램의 동작이 달라질 수 있음에 유의하십시오.
외부 링커는 이미 SEH 정보를 보존하고 있으므로, `-linkmode=external`은 이 변경 사항의 영향을 받지 않습니다.

## Bootstrap {#bootstrap}

[Go 1.20 릴리스 노트](/doc/go1.20#bootstrap)에 언급된 바와 같이, Go 1.22는 이제 부트스트랩을 위해 Go 1.20의 최종 포인트 릴리스 또는 그 이후 버전이 필요합니다.
Go 1.24는 부트스트랩을 위해 Go 1.22의 최종 포인트 릴리스 또는 그 이후 버전이 필요할 것으로 예상됩니다.

## 표준 라이브러리 {#library}

### 새로운 math/rand/v2 패키지 {#math_rand_v2}

Please provide the Markdown content you would like me to translate. You have only provided HTML comments (CL numbers), but no text to translate. Once you provide the content, I will translate it into Korean while preserving all technical structures and identifiers.

Go 1.22에는 표준 라이브러리 최초의 "v2" 패키지인 [`math/rand/v2`](/pkg/math/rand/v2/)가 포함되었습니다.
[`math/rand`](/pkg/math/rand/)와 비교하여 변경된 사항은 [proposal #61716](/issue/61716)에 자세히 설명되어 있습니다. 가장 중요한 변경 사항은 다음과 같습니다.

- `math/rand`에서 deprecated 되었던 `Read` 메서드는 `math/rand/v2`로 이관되지 않았습니다. (`math/rand`에서는 계속 사용할 수 있습니다.) 대부분의 `Read` 호출은 대신 [`crypto/rand`의 `Read`](/pkg/crypto/rand/#Read)를 사용해야 합니다. 그 외의 경우 `Uint64` 메서드를 사용하여 사용자 정의 `Read`를 구현할 수 있습니다.
- 최상위 함수로 액세스하는 전역 제너레이터는 조건 없이 무작위로 시드(seed)가 설정됩니다. API가 결과의 고정된 시퀀스를 보장하지 않으므로, 이제 스레드별 랜덤 제너레이터 상태와 같은 최적화가 가능합니다.
- [`Source`](/pkg/math/rand/v2/#Source) 인터페이스는 이제 단일 `Uint64` 메서드만 가지며, `Source64` 인터페이스는 더 이상 존재하지 않습니다.
- 많은 메서드가 더 빠른 알고리즘을 사용합니다. 이러한 알고리즘은 출력 스트림을 변경하기 때문에 `math/rand`에서는 채택할 수 없었습니다.
- `math/rand`의 `Intn`, `Int31`, `Int31n`, `Int63`, `Int64n` 최상위 함수 및 메서드들이 `math/rand/v2`에서는 더 관용적인 명칭인 `IntN`, `Int32`, `Int32N`, `Int64`, `Int64N`으로 변경되었습니다. 또한 `Uint32`, `Uint32N`, `Uint64`, `Uint64N`, `UintN`이라는 새로운 최상위 함수 및 메서드들이 추가되었습니다.
- 새로운 제네릭 함수인 [`N`](/pkg/math/rand/v2/#N)은 [`Int64N`](/pkg/math/rand/v2/#Int64N) 또는 [`Uint64N`](/pkg/math/rand/v2/#Uint64N)과 비슷하지만, 모든 정수 타입에 대해 작동합니다. 예를 들어, 0부터 5분 사이의 무작위 duration은 `rand.N(5*time.Minute)`로 생성할 수 있습니다.
- [`math/rand`의 `Source`](/pkg/math/rand/#Source)에서 제공하던 Mitchell & Reeds LFSR 제너레이터는 더 현대적인 두 가지 의사 난수 제너레이터 소스인 [`ChaCha8`](/pkg/math/rand/v2/#ChaCha8)과 [`PCG`](/pkg/math/rand/v2/#PCG)로 대체되었습니다. ChaCha8은 암호학적으로 강력한 새로운 난수 제너레이터이며 효율성 면에서 PCG와 비슷합니다. ChaCha8은 `math/rand/v2`의 최상위 함수에 사용되는 알고리즘입니다. Go 1.22부터 `math/rand`의 최상위 함수(명시적으로 시드 설정하지 않은 경우)와 Go 런타임에서도 난수 생성에 ChaCha8을 사용합니다.

우리는 향후 릴리스(아마도 Go 1.23)에 API 마이그레이션 도구를 포함할 계획입니다.

### 새로운 go/version 패키지 {#go-version}

<!-- https://go.dev/issue/62039, https://go.dev/cl/538895 -->
새로운 [`go/version`](/pkg/go/version/) 패키지는 Go 버전 문자열을 검증하고 비교하기 위한 함수들을 구현합니다.

### 향상된 라우팅 패턴 {#enhanced_routing_patterns}

<!-- https://go.dev/issue/61410 -->
표준 라이브러리의 HTTP 라우팅이 이제 더 표현력이 풍부해졌습니다.
[`net/http.ServeMux`](/pkg/net/http#ServeMux)에서 사용하는 패턴이 메서드와 와일드카드를 허용하도록 개선되었습니다.

`"POST /items/create"`와 같이 메서드와 함께 핸들러를 등록하면, 해당 핸들러의 호출이 지정된 메서드를 가진 요청으로 제한됩니다. 메서드가 포함된 패턴은 메서드가 없는 일치하는 패턴보다 우선순위를 갖습니다.
특수한 경우로, 핸들러를 `"GET"`으로 등록하면 `"HEAD"` 메서드에도 함께 등록됩니다.

`/items/{id}`와 같은 패턴의 와일드카드는 URL 경로의 세그먼트와 일치합니다.
실제 세그먼트 값은 [`Request.PathValue`](/pkg/net/http#Request.PathValue) 메서드를 호출하여 접근할 수 있습니다.
`/files/{path...}`와 같이 "..."로 끝나는 와일드카드는 반드시 패턴의 끝에 위치해야 하며, 나머지 모든 세그먼트와 일치합니다.

"/"로 끝나는 패턴은 언제나 그렇듯, 해당 패턴을 접두사(prefix)로 갖는 모든 경로와 일치합니다.
마지막 슬래시를 포함하여 정확히 일치하는 패턴을 찾으려면, `/exact/match/{$}`와 같이 `{$}`로 끝내십시오.

두 패턴이 일치하는 요청에서 서로 겹치는 경우, 더 구체적인(more specific) 패턴이 우선순위를 갖습니다.
어느 쪽도 더 구체적이지 않다면, 해당 패턴들은 충돌(conflict)하는 것으로 간주합니다.
이 규칙은 기존의 우선순위 규칙을 일반화한 것이며, 패턴이 등록되는 순서가 중요하지 않다는 속성을 유지합니다.

이 변경 사항은 사소한 방식으로 하위 호환성을 깨뜨립니다. 일부는 명백하며(예: "{" 및 "}"가 포함된 패턴의 동작 방식 변경), 일부는 덜 명백합니다(예: 이스케이프된 경로의 처리 방식 개선).

이 변경 사항은 `httpmuxgo121`이라는 이름의 [`GODEBUG`](/doc/godebug) 필드로 제어됩니다.
이전 동작으로 복구하려면 `httpmuxgo121=1`로 설정하십시오.

### 라이브러리의 사소한 변경 사항 {#minor_library_changes}

언제나 그렇듯, Go 1의 [호환성 약속](/doc/go1compat)을 염두에 두고 라이브러리에 다양한 소규모 변경 및 업데이트가 이루어졌습니다.
또한 여기에는 나열되지 않은 다양한 성능 개선 사항들이 포함되어 있습니다.

[archive/tar](/pkg/archive/tar/)

<!-- https://go.dev/issue/58000, CL 513316 -->
새로운 메서드 [`Writer.AddFS`](/pkg/archive/tar#Writer.AddFS)는 [`fs.FS`](/pkg/io/fs#FS)의 모든 파일을 아카이브에 추가합니다.

<!-- archive/tar -->

[archive/zip](/pkg/archive/zip/)

<!-- https://go.dev/issue/54898, CL 513438 -->
새로운 메서드 [`Writer.AddFS`](/pkg/archive/zip#Writer.AddFS)는 [`fs.FS`](/pkg/io/fs#FS)의 모든 파일을 아카이브에 추가합니다.

<!-- archive/zip -->

[bufio](/pkg/bufio/)

<!-- https://go.dev/issue/56381, CL 498117 -->
[`SplitFunc`](/pkg/bufio#SplitFunc)가 `nil` 토큰과 함께 [`ErrFinalToken`](/pkg/bufio#ErrFinalToken)을 반환하면, 이제 [`Scanner`](/pkg/bufio#Scanner)가 즉시 중단됩니다.
이전에는 중단되기 전에 마지막 빈 토큰을 보고했으며, 이는 일반적으로 의도되지 않은 동작이었습니다.
마지막 빈 토큰을 보고하고자 하는 호출자는 `nil` 대신 `[]byte{}`를 반환하면 됩니다.

<!-- bufio -->

[cmp](/pkg/cmp/)

<!-- https://go.dev/issue/60204 -->
    <!-- CL 504883 -->
    새로운 함수 `Or`는 값의 시퀀스 중 제로 값(zero value)이 아닌 첫 번째 값을 반환합니다.

제공해주신 텍스트가 비어 있거나 주석(`<!-- cmp -->`)만 포함되어 있습니다. 번역할 내용을 입력해 주시면, 요청하신 대로 Markdown 구조와 기술적 세부 사항을 유지하여 정확하게 한국어로 번역해 드리겠습니다.

[crypto/tls](/pkg/crypto/tls/)

<!-- https://go.dev/issue/43922, CL 544155 -->
    [`ConnectionState.ExportKeyingMaterial`](/pkg/crypto/tls#ConnectionState.ExportKeyingMaterial)은 이제 TLS 1.3을 사용 중이거나, 서버와 클라이언트 모두 `extended_master_secret` 확장 기능을 지원하지 않는 한 에러를 반환합니다. `crypto/tls`는 Go 1.20부터 이 확장 기능을 지원해 왔습니다. 이 동작은 `tlsunsafeekm=1` GODEBUG 설정으로 비활성화할 수 있습니다.

<!-- https://go.dev/issue/62459, CL 541516 -->
    이제 `crypto/tls` 서버가 제공하는 최소 버전은 [`config.MinimumVersion`](/pkg/crypto/tls#Config.MinimumVersion)으로 지정하지 않은 경우 기본적으로 TLS 1.2이며, 이는 `crypto/tls` 클라이언트의 동작과 일치합니다. 이 변경 사항은 `tls10server=1` GODEBUG 설정을 통해 되돌릴 수 있습니다.

<!-- https://go.dev/issue/63413, CL 541517 -->
    기본적으로, TLS 1.3 이전 버전의 핸드셰이크 동안 클라이언트와 서버 모두 ECDHE를 지원하지 않는 사이퍼 스위트(cipher suites)를 더 이상 제공하지 않습니다. 이 변경 사항은 `tlsrsakex=1` GODEBUG 설정을 통해 되돌릴 수 있습니다.

<!-- crypto/tls -->

[crypto/x509](/pkg/crypto/x509/)

<!-- https://go.dev/issue/57178 -->
새로운 [`CertPool.AddCertWithConstraint`](/pkg/crypto/x509#CertPool.AddCertWithConstraint)
메서드를 사용하여 체인 구축 중에 적용될 루트 인증서에 사용자 정의 제약 조건을 추가할 수 있습니다.

<!-- https://go.dev/issue/58922, CL 519315-->
    Android에서 이제 루트 인증서가 `/system/etc/security/cacerts`뿐만 아니라 `/data/misc/keychain/certs-added`에서도 로드됩니다.

<!-- https://go.dev/issue/60665, CL 520535 -->
    새로운 타입인 [`OID`](/pkg/crypto/x509#OID)는 개별 컴포넌트가 31비트보다 큰 ASN.1 객체 식별자(Object Identifiers)를 지원합니다. 이 타입을 사용하는 새로운 필드인 [`Policies`](/pkg/crypto/x509#Certificate.Policies)가 `Certificate` 구조체에 추가되었으며, 이제 파싱 중에 값이 채워집니다. [`asn1.ObjectIdentifier`](/pkg/encoding/asn1#ObjectIdentifier)를 사용하여 표현할 수 없는 모든 OID는 `Policies`에 나타나지만, 기존의 `PolicyIdentifiers` 필드에는 나타나지 않습니다.
    [`CreateCertificate`](/pkg/crypto/x509#CreateCertificate)를 호출할 때 `Policies` 필드는 무시되며, 정책은 `PolicyIdentifiers` 필드에서 가져옵니다. `x509usepolicies=1` GODEBUG 설정을 사용하면 이 동작이 반전되어, 인증서 정책을 `Policies` 필드에서 채우고 `PolicyIdentifiers` 필드는 무시합니다. Go 1.23에서 `x509usepolicies`의 기본값을 변경하여 `Policies`를 마샬링(marshaling)의 기본 필드로 만들 수 있습니다.

<!-- crypto/x509 -->

[database/sql](/pkg/database/sql/)

<!-- https://go.dev/issue/60370, CL 501700 -->
    새로운 [`Null[T]`](/pkg/database/sql/#Null) 타입은
    모든 컬럼 타입에 대해 null 허용(nullable) 컬럼을 스캔하는 방법을 제공합니다.

<!-- database/sql -->

[debug/elf](/pkg/debug/elf/)

<!-- https://go.dev/issue/61974, CL 469395 -->
    상수 `R_MIPS_PC32`는 MIPS64 시스템에서 사용하기 위해 정의되었습니다.

<!-- https://go.dev/issue/63725, CL 537615 -->
    LoongArch 시스템에서 사용할 수 있도록 추가적인 `R_LARCH_*` 상수가 정의되었습니다.

<!-- debug/elf -->

[encoding](/pkg/encoding/)

<!-- https://go.dev/issue/53693, https://go.dev/cl/504884 -->
    [`encoding/base32`](/pkg/encoding/base32),
    [`encoding/base64`](/pkg/encoding/base64), 및
    [`encoding/hex`](/pkg/encoding/hex) 패키지의 각 `Encoding` 타입에 추가된 새로운 메서드 `AppendEncode`와 `AppendDecode`는 바이트 슬라이스 버퍼 관리를 처리함으로써 바이트 슬라이스로부터의 인코딩 및 디코딩을 간소화합니다.

<!-- https://go.dev/cl/505236 -->
    [`base32.Encoding.WithPadding`](/pkg/encoding/base32#Encoding.WithPadding) 및
    [`base64.Encoding.WithPadding`](/pkg/encoding/base64#Encoding.WithPadding) 메서드는
    이제 `padding` 인자가 `NoPadding`이 아닌 음수 값일 경우 패닉(panic)이 발생합니다.

Please provide the English Markdown content you would like me to translate. I am ready to translate it into Korean while preserving all technical structures, code, and identifiers.

[encoding/json](/pkg/encoding/json/)

<!-- https://go.dev/cl/521675 -->
이제 마샬링(Marshaling) 및 인코딩 기능에서 `'\b'`와 `'\f'` 문자를 `\u0008` 및 `\u000c` 대신 `\b` 및 `\f`로 이스케이프합니다.

<!-- encoding/json -->

[go/ast](/pkg/go/ast/)

<!-- https://go.dev/issue/52463, https://go/dev/cl/504915 -->
    [구문 식별자 해석(syntactic identifier resolution)](https://pkg.go.dev/go/ast#Object)과 관련된 다음 선언들이 이제 [deprecated](/issue/52463) 되었습니다:
    `Ident.Obj`,
    `Object`,
    `Scope`,
    `File.Scope`,
    `File.Unresolved`,
    `Importer`,
    `Package`,
    `NewPackage`.
    일반적으로, 타입 정보 없이는 식별자를 정확하게 해석할 수 없습니다.
    예를 들어, `T{K: ""}`에서 식별자 `K`를 생각해보십시오. T가 맵(map) 타입이라면 이는 지역 변수의 이름일 수 있고, T가 구조체(struct) 타입이라면 필드의 이름일 수 있습니다.
    새로운 프로그램은 식별자를 해석하기 위해 [go/types](/pkg/go/types)
    패키지를 사용해야 합니다. 자세한 내용은
    [`Object`](https://pkg.go.dev/go/types#Object),
    [`Info.Uses`](https://pkg.go.dev/go/types#Info.Uses), 그리고
    [`Info.Defs`](https://pkg.go.dev/go/types#Info.Defs)를 참조하십시오.

<!-- https://go.dev/issue/60061 -->
    새로운 [`ast.Unparen`](https://pkg.go.dev/go/ast#Unparen)
    함수는 [expression](https://pkg.go.dev/go/ast#Expr)을
    둘러싸고 있는 모든 [parentheses](https://pkg.go.dev/go/ast#ParenExpr)를 제거합니다.

<!-- go/ast -->

[go/types](/pkg/go/types/)

<!-- https://go.dev/issue/63223, CL 521956, CL 541737 -->
    새로운 [`Alias`](/pkg/go/types#Alias) 타입은 타입 별칭(type aliases)을 나타냅니다.
    이전에는 타입 별칭이 명시적으로 표현되지 않았기 때문에, 타입 별칭에 대한 참조는 별칭이 지정된 타입을 그대로 적은 것과 동일했으며, 별칭의 이름은 소실되었습니다.
    새로운 표현 방식은 중간 단계인 `Alias`를 유지합니다.
    이를 통해 개선된 에러 보고(타입 별칭의 이름을 보고할 수 있음)가 가능해지며, 타입 별칭이 포함된 순환 타입 선언을 더 효율적으로 처리할 수 있습니다.
    향후 릴리스에서 `Alias` 타입은 [타입 파라미터 정보](/issue/46477)도 함께 포함하게 됩니다.
    새로운 함수 [`Unalias`](/pkg/go/types#Unalias)는 `Alias` 타입(또는 다른 모든 [`Type`](/pkg/go/types#Type))이 실제로 나타내는 타입을 반환합니다.

`Alias` 타입은 이를 확인하도록 설계되지 않은 기존의 타입 스위치(type switch)를 깨뜨릴 수 있기 때문에, 이 기능은 `gotypesalias`라는 이름의 [`GODEBUG`](/doc/godebug) 필드로 제어됩니다.
`gotypesalias=0`인 경우 모든 것이 이전과 동일하게 동작하며, `Alias` 타입은 절대 생성되지 않습니다.
`gotypesalias=1`인 경우 `Alias` 타입이 생성되며, 클라이언트는 이를 고려하여 처리해야 합니다.
기본값은 `gotypesalias=0`입니다.
향후 릴리스에서는 기본값이 `gotypesalias=1`로 변경될 예정입니다.
_[`go/types`](/pkg/go/types) 클라이언트는 문제를 조기에 해결하기 위해 가능한 한 빨리 `gotypesalias=1`에서 동작하도록 코드를 수정하시기를 권장합니다._

<!-- https://go.dev/issue/62605, CL 540056 -->
    [`Info`](/pkg/go/types#Info) 구조체에 파일별 Go 버전 정보를 제공하는 [`FileVersions`](/pkg/go/types#Info.FileVersions) 맵이 추가되어 이제 외부에서 접근 가능합니다.

<!-- https://go.dev/issue/62037, CL 541575 -->
    새로운 헬퍼 메서드 [`PkgNameOf`](/pkg/go/types#Info.PkgNameOf)는 주어진 import 선언에 대한 로컬 패키지 이름을 반환합니다.

<!-- https://go.dev/issue/61035, multiple CLs, see issue for details -->
    [`SizesFor`](/pkg/go/types#SizesFor)의 구현이 수정되어, `SizesFor`의 컴파일러 인자가 `"gc"`인 경우 컴파일러와 동일한 타입 크기를 계산합니다.
    타입 체커에서 사용하는 기본 [`Sizes`](/pkg/go/types#Sizes) 구현은 이제 `types.SizesFor("gc", "amd64")`입니다.

<!-- https://go.dev/issue/64295, CL 544035 -->
    함수 본문을 나타내는 어휘 환경 블록([`Scope`](/pkg/go/types#Scope))의
    시작 위치([`Pos`](/pkg/go/types#Scope.Pos))가 변경되었습니다.
    이전에는 함수 본문의 여는 중괄호(`{`)에서 시작했으나,
    이제는 함수의 `func` 토큰에서 시작합니다.

[html/template](/pkg/html/template/)

<!-- https://go.dev/issue/61619, CL 507995 -->
    이제 JavaScript 템플릿 리터럴 내에 Go 템플릿 액션을 포함할 수 있으며, 이를 포함하는 템플릿을 파싱하더라도 더 이상 `ErrJSTemplate`를 반환하지 않습니다. 마찬가지로 GODEBUG 설정인 `jstmpllitinterp`는 더 이상 아무런 영향을 주지 않습니다.

<!-- html/template -->

[io](/pkg/io/)

<!-- https://go.dev/issue/61870, CL 526855 -->
    새로운 [`SectionReader.Outer`](/pkg/io#SectionReader.Outer) 메서드는 [`NewSectionReader`](/pkg/io#NewSectionReader)에 전달된 [`ReaderAt`](/pkg/io#ReaderAt), 오프셋(offset) 및 크기(size)를 반환합니다.

<!-- io -->

[log/slog](/pkg/log/slog/)

<!-- https://go.dev/issue/62418 -->
새로운 [`SetLogLoggerLevel`](/pkg/log/slog#SetLogLoggerLevel) 함수는 `slog`와 `log` 패키지 간의 브리지 레벨을 제어합니다. 이 함수는 최상위 `slog` 로깅 함수 호출에 대한 최소 레벨을 설정하며, `slog`를 통해 전달되는 `log.Logger` 호출에 대한 레벨을 설정합니다.

[math/big](/pkg/math/big/)

<!-- https://go.dev/issue/50489, CL 539299 -->
    새로운 메서드 [`Rat.FloatPrec`](/pkg/math/big#Rat.FloatPrec)는 유리수를 부동 소수점으로 정확하게 표현하는 데 필요한 소수점 이하 자릿수와, 애초에 정확한 십진수 표현이 가능한지 여부를 계산합니다.

<!-- math/big -->

[net](/pkg/net/)

<!-- https://go.dev/issue/58808 -->
    [`io.Copy`](/pkg/io#Copy)가 `TCPConn`에서 `UnixConn`으로 데이터를 복사할 때,
    가능한 경우 새로운 메서드인 [`TCPConn.WriteTo`](/pkg/net#TCPConn.WriteTo)를 사용하여
    Linux의 `splice(2)` 시스템 콜을 사용합니다.

<!-- CL 467335 -->
    `-tags=netgo`를 사용하여 빌드할 때 사용되는 Go DNS Resolver가
    이제 DNS 쿼리를 수행하기 전에
    `%SystemRoot%\System32\drivers\etc\hosts`에 위치한
    Windows hosts 파일에서 일치하는 이름을 검색합니다.

<!-- net -->

[net/http](/pkg/net/http/)

<!-- https://go.dev/issue/51971 -->
    새로운 함수인
    [`ServeFileFS`](/pkg/net/http#ServeFileFS),
    [`FileServerFS`](/pkg/net/http#FileServerFS), 및
    [`NewFileTransportFS`](/pkg/net/http#NewFileTransportFS)는
    기존의 `ServeFile`, `FileServer`, `NewFileTransport`의 버전으로,
    `fs.FS` 상에서 동작합니다.

<!-- https://go.dev/issue/61679 -->
    이제 HTTP 서버와 클라이언트가 유효하지 않은 빈 `Content-Length` 헤더가 포함된 요청과 응답을 거부합니다.
    [`GODEBUG`](/doc/godebug) 필드를 `httplaxcontentlength=1`로 설정하여 이전 동작을 복구할 수 있습니다.

<!-- https://go.dev/issue/61410, CL 528355 -->
    새로운 메서드인
    [`Request.PathValue`](/pkg/net/http#Request.PathValue)는
    요청에서 경로 와일드카드 값을 반환하며,
    새로운 메서드인
    [`Request.SetPathValue`](/pkg/net/http#Request.SetPathValue)는
    요청에 경로 와일드카드 값을 설정합니다.

<!-- net/http -->

[net/http/cgi](/pkg/net/http/cgi/)

<!-- CL 539615 -->
    CGI 프로세스를 실행할 때, `PATH_INFO` 변수는 이제 RFC 3875의 요구 사항에 따라 항상 빈 문자열 또는 `/` 문자로 시작하는 값으로 설정됩니다. 이전에는 [`Handler.Root`](/pkg/net/http/cgi#Handler.Root)와 요청 URL의 일부 조합에 따라 이 요구 사항을 위반하는 경우가 있었습니다.

<!-- net/http/cgi -->

[net/netip](/pkg/net/netip/)

<!-- https://go.dev/issue/61642 -->
새로운 [`AddrPort.Compare`](/pkg/net/netip#AddrPort.Compare)
메서드는 두 개의 `AddrPort`를 비교합니다.

<!-- net/netip -->

[os](/pkg/os/)

<!-- CL 516555 -->
    Windows에서 [`Stat`](/pkg/os#Stat) 함수가 이제 시스템의 다른 명명된 엔티티(named entity)로 연결되는 모든 재분석 지점(reparse points)을 따릅니다.
    이전에는 `IO_REPARSE_TAG_SYMLINK` 및 `IO_REPARSE_TAG_MOUNT_POINT` 재분석 지점만 따랐습니다.

<!-- CL 541015 -->
    Windows에서 [`OpenFile`](/pkg/os#OpenFile)에 [`O_SYNC`](/pkg/os#O_SYNC)를 전달하면, 이제 Unix 플랫폼의 `O_SYNC`와 동일하게 쓰기 작업이 디스크로 직접 전달됩니다.

<!-- CL 452995 -->
    Windows에서 [`ReadDir`](/pkg/os#ReadDir),
    [`File.ReadDir`](/pkg/os#File.ReadDir),
    [`File.Readdir`](/pkg/os#File.Readdir),
    및 [`File.Readdirnames`](/pkg/os#File.Readdirnames) 함수가
    이제 시스템 호출 횟수를 줄이기 위해 디렉터리 항목을 일괄(batch) 읽기 방식으로 처리하며,
    이를 통해 성능이 최대 30% 향상되었습니다.

<!-- https://go.dev/issue/58808 -->
    [`io.Copy`](/pkg/io#Copy)가 `File`에서 `net.UnixConn`으로 데이터를 복사할 때,
    이제 새로운 메서드인 [`File.WriteTo`](/pkg/os#File.WriteTo)를 사용하여 가능한 경우 Linux의 `sendfile(2)` 시스템 호출을 사용합니다.

<!-- os -->

[os/exec](/pkg/os/exec/)

<!-- CL 528037 -->
    Windows에서 [`LookPath`](/pkg/os/exec#LookPath)가 이제 `%PATH%` 내의 빈 항목을 무시하며, 모호하지 않은 이름에 대해 해석할 수 있는 실행 파일 확장자를 찾지 못한 경우 `ErrNotExist` 대신 `ErrNotFound`를 반환합니다.

<!-- CL 528038, CL 527820 -->
    Windows에서 실행 파일로의 경로가 이미 절대 경로이며 실행 가능한 파일 확장자를 가지고 있는 경우, [`Command`](/pkg/os/exec#Command)와 [`Cmd.Start`](/pkg/os/exec#Cmd.Start)는 더 이상 `LookPath`를 호출하지 않습니다. 또한, `Cmd.Start`는 분석된 확장자를 [`Path`](/pkg/os/exec#Cmd.Path) 필드에 다시 기록하지 않으므로, 이제 `Start` 호출과 동시에 `String` 메서드를 안전하게 호출할 수 있습니다.

<!-- os/exec -->

[reflect](/pkg/reflect/)

<!-- https://go.dev/issue/61827, CL 517777 -->
    [`Value.IsZero`](/pkg/reflect/#Value.IsZero)
    메서드가 이제 부동 소수점 또는 복소수의 음수 제로(negative zero)에 대해 true를 반환하며, 빈 필드(이름이 `_`인 필드)가 어떤 이유로든 0이 아닌 값을 가진 구조체 값에 대해서도 true를 반환합니다.
    이러한 변경 사항을 통해 `IsZero`는 언어의 `==` 연산자를 사용하여 값을 0과 비교하는 것과 일관성을 갖게 됩니다.

<!-- https://go.dev/issue/59599, CL 511035 -->
    [`PtrTo`](/pkg/reflect/#PtrTo) 함수는 더 이상 사용되지 않으며(deprecated),
    대신 [`PointerTo`](/pkg/reflect/#PointerTo)를 사용하십시오.

<!-- https://go.dev/issue/60088, CL 513478 -->
    새로운 함수 [`TypeFor`](/pkg/reflect/#TypeFor)는
    타입 인자 T를 나타내는 [`Type`](/pkg/reflect/#Type)을
    반환합니다.
    이전에는 타입에 대한 `reflect.Type` 값을 얻으려면
    `reflect.TypeOf((*T)(nil)).Elem()`을 사용해야 했습니다.
    이제는 `reflect.TypeFor[T]()`로 작성할 수 있습니다.

<!-- reflect -->

[runtime/metrics](/pkg/runtime/metrics/)

<!-- https://go.dev/issue/63340 -->
네 가지의 새로운 히스토그램 메트릭인
`/sched/pauses/stopping/gc:seconds`,
`/sched/pauses/stopping/other:seconds`,
`/sched/pauses/total/gc:seconds`, 및
`/sched/pauses/total/other:seconds`가 stop-the-world 일시 중지에 대한 추가 세부 정보를 제공합니다.
"stopping" 메트릭은 world를 중지하기로 결정한 시점부터 모든 goroutine이 중지될 때까지 걸린 시간을 보고합니다.
"total" 메트릭은 world를 중지하기로 결정한 시점부터 다시 시작될 때까지 걸린 시간을 보고합니다.

<!-- https://go.dev/issue/63340 -->
    `/gc/pauses:seconds` 메트릭은 새로운 `/sched/pauses/total/gc:seconds` 메트릭과 동일하므로 더 이상 사용되지 않습니다(deprecated).

<!-- https://go.dev/issue/57071 -->
    `/sync/mutex/wait/total:seconds` 지표에 이제 [`sync.Mutex`](/pkg/sync#Mutex) 및 [`sync.RWMutex`](/pkg/sync#RWMutex) 외에도 런타임 내부 락(runtime-internal locks)의 경합(contention)이 포함됩니다.

<!-- runtime/metrics -->

[runtime/pprof](/pkg/runtime/pprof/)

<!-- https://go.dev/issue/61015 -->
Mutex 프로필이 이제 뮤텍스(mutex)에서 차단된 고루틴(goroutine)의 수에 따라 경합(contention) 규모를 조정합니다.
이를 통해 Go 프로그램에서 뮤텍스가 병목 지점이 되는 정도를 더 정확하게 나타낼 수 있습니다.
예를 들어, 100개의 고루틴이 10밀리초 동안 뮤텍스에서 차단된 경우, 뮤텍스 프로필은 이제 10밀리초가 아닌 1초의 지연 시간으로 기록합니다.

<!-- https://go.dev/issue/57071 -->
    이제 Mutex 프로파일에는 [`sync.Mutex`](/pkg/sync#Mutex) 및
    [`sync.RWMutex`](/pkg/sync#RWMutex) 외에도 런타임 내부 잠금(runtime-internal locks)에 대한 경합(contention) 정보가 포함됩니다.
    런타임 내부 잠금의 경합은 항상 `runtime._LostContendedRuntimeLock`으로 보고됩니다.
    향후 릴리스에서 이러한 경우에 대한 전체 스택 트레이스(stack traces)가 추가될 예정입니다.

<!-- https://go.dev/issue/50891 -->
    Darwin 플랫폼의 CPU 프로파일에 이제 프로세스의 메모리 맵이 포함되어, pprof 도구에서 디스어셈블리(disassembly) 뷰를 사용할 수 있습니다.

<!-- runtime/pprof -->

[runtime/trace](/pkg/runtime/trace/)

<!-- https://go.dev/issue/60773 -->
    이번 릴리스에서는 실행 트레이서(execution tracer)가 완전히 개편되어, 오랫동안 해결되지 않았던 여러 문제들이 해결되었으며 실행 트레이스의 새로운 활용 사례를 위한 기반이 마련되었습니다.

이제 대부분의 플랫폼(Windows 제외)에서 실행 트레이스(Execution traces)가 운영체제 클럭을 사용하므로, 하위 수준 구성 요소에서 생성된 트레이스와 상관 관계를 분석할 수 있습니다.
실행 트레이스는 더 이상 올바른 트레이스를 생성하기 위해 플랫폼 클럭의 신뢰성에 의존하지 않습니다.
실행 트레이스는 이제 실시간으로 정기적으로 분할되며, 결과적으로 스트리밍 방식으로 처리될 수 있습니다.
실행 트레이스에 이제 모든 시스템 호출의 전체 소요 시간이 포함됩니다.
실행 트레이스에 이제 goroutine이 실행된 운영체제 스레드에 대한 정보가 포함됩니다.
실행 트레이스를 시작하고 중지할 때 발생하는 지연 시간이 획기적으로 감소했습니다.
이제 가비지 컬렉션(garbage collection) 마크 단계 중에 실행 트레이스가 시작되거나 종료될 수 있습니다.

Go 개발자가 이러한 개선 사항을 활용할 수 있도록, 실험적인 트레이스 읽기 패키지를 [golang.org/x/exp/trace](/pkg/golang.org/x/exp/trace)에서 제공합니다.
이 패키지는 현재 Go 1.22로 빌드된 프로그램이 생성한 트레이스에서만 작동한다는 점에 유의하십시오.
패키지를 사용해 보시고 [해당 제안 이슈](/issue/62627)를 통해 피드백을 제공해 주시기 바랍니다.

새로운 실행 추적기(execution tracer) 구현으로 인해 문제가 발생할 경우, Go 프로그램을 빌드할 때 `GOEXPERIMENT=noexectracer2`를 사용하여 이전 구현으로 되돌릴 수 있습니다.
이 옵션을 사용하는 경우 이슈를 제보해 주시기 바랍니다. 그렇지 않으면 이 옵션은 향후 릴리스에서 제거될 예정입니다.

<!-- runtime/trace -->

[slices](/pkg/slices/)

<!-- https://go.dev/issue/56353 -->
    <!-- CL 504882 -->
    새로운 함수 `Concat`은 여러 슬라이스를 연결합니다.

<!-- https://go.dev/issue/63393 -->
    <!-- CL 543335 -->
    슬라이스의 크기를 줄이는 함수(`Delete`, `DeleteFunc`, `Compact`, `CompactFunc`, `Replace`)가 이제 새로운 길이와 기존 길이 사이의 요소들을 0으로 초기화합니다.

<!-- https://go.dev/issue/63913 -->
    <!-- CL 540155 -->
    이제 인자 `i`가 범위를 벗어날 경우 `Insert`는 항상 panic을 발생시킵니다. 이전에는 삽입할 요소가 없는 경우 이 상황에서 panic을 발생시키지 않았습니다.

<!-- slices -->

[syscall](/pkg/syscall/)

<!-- https://go.dev/issue/60797 -->
`syscall` 패키지는 Go 1.4 이후로 [동결(frozen)](/s/go1.4-syscall)되었으며 Go 1.11에서 deprecated로 표시되어, 많은 에디터가 해당 패키지 사용 시 경고를 표시해 왔습니다.
하지만 [`os/exec.Cmd.SysProcAttr`](/pkg/os/exec#Cmd) 필드와 같이, deprecated 되지 않은 일부 기능들은 여전히 `syscall` 패키지의 사용을 필요로 합니다.
이러한 코드에서 불필요한 경고가 발생하는 것을 방지하기 위해, `syscall` 패키지는 더 이상 deprecated로 표시되지 않습니다.
해당 패키지는 대부분의 새로운 기능에 대해 여전히 동결된 상태이며, 새로운 코드에서는 가능한 한 [`golang.org/x/sys/unix`](/pkg/golang.org/x/sys/unix) 또는 [`golang.org/x/sys/windows`](/pkg/golang.org/x/sys/windows)를 사용하는 것이 권장됩니다.

<!-- https://go.dev/issue/51246, CL 520266 -->
    Linux에서 새로운 [`SysProcAttr.PidFD`](/pkg/syscall#SysProcAttr) 필드를 통해 [`StartProcess`](/pkg/syscall#StartProcess) 또는 [`os/exec`](/pkg/os/exec)로 자식 프로세스를 시작할 때 PID FD를 얻을 수 있습니다.

<!-- CL 541015 -->
    Windows에서 [`Open`](/pkg/syscall#Open)에 [`O_SYNC`](/pkg/syscall#O_SYNC)를 전달하면 이제 쓰기 작업이 디스크로 직접 전달되며, 이는 Unix 플랫폼의 `O_SYNC`와 동일하게 동작합니다.

<!-- syscall -->

[testing/slogtest](/pkg/testing/slogtest/)

<!-- https://go.dev/issue/61758 -->
새로운 [`Run`](/pkg/testing/slogtest#Run) 함수는 테스트 케이스를 실행하기 위해 서브 테스트(sub-tests)를 사용하며, 이를 통해 더 세밀한 제어가 가능합니다.

<!-- testing/slogtest -->

## 포트 {#ports}

### Darwin {#darwin}

<!-- CL 461697 -->
64비트 x86 아키텍처의 macOS(`darwin/amd64` 포트)에서 Go 툴체인은 이제 기본적으로 위치 독립 실행 파일(PIE, position-independent executables)을 생성합니다.
Non-PIE 바이너리는 `-buildmode=exe` 빌드 플래그를 지정하여 생성할 수 있습니다.
64비트 ARM 기반 macOS(`darwin/arm64` 포트)에서는 Go 툴체인이 이미 기본적으로 PIE를 생성하고 있습니다.

<!-- go.dev/issue/64207 -->
Go 1.22는 macOS 10.15 Catalina에서 실행되는 마지막 릴리스입니다. Go 1.23부터는 macOS 11 Big Sur 또는 그 이후 버전이 필요합니다.

### ARM {#arm}

<!-- CL 514907 -->
이제 `GOARM` 환경 변수를 통해 소프트웨어 부동 소수점 또는 하드웨어 부동 소수점 사용 여부를 선택할 수 있습니다.
이전에는 `GOARM`의 유효한 값이 `5`, `6`, 또는 `7`이었습니다. 이제 이 값들 뒤에 선택적으로 `,softfloat` 또는 `,hardfloat`를 추가하여 부동 소수점 구현 방식을 선택할 수 있습니다.

이 새로운 옵션은 버전 `5`에서는 `softfloat`가, 버전 `6` 및 `7`에서는 `hardfloat`가 기본값으로 설정됩니다.

### Loong64 {#loong64}

<!-- CL 481315 -->
이제 `loong64` 포트에서 레지스터를 사용하여 함수 인자와 결과값을 전달하는 것을 지원합니다.

<!-- CL 481315,537615,480878 -->
`linux/loong64` 포트가 이제 address sanitizer, memory sanitizer, 새로운 스타일의 linker relocations 및 `plugin` 빌드 모드를 지원합니다.

### OpenBSD {#openbsd}

<!-- CL 517935 -->
Go 1.22에서는 빅 엔디안 64비트 PowerPC(`openbsd/ppc64`) 기반의 OpenBSD에 대한 실험적 포트가 추가되었습니다.
