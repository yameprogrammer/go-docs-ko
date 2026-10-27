```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.26 소개 {#introduction}

## Getting Started {#getting-started}

가장 최신 Go 릴리스인 버전 1.26은 [2026년 2월](/doc/devel/release#go1.26.0)에 출시되며, Go 1.25 이후 6개월 후입니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
항상처럼, 이 릴리스는 Go 1의 호환성 약속을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일 및 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

<!-- https://go.dev/issue/45624 -->

내장된 `new` 함수는 이제 새 변수를 생성할 때, 피연산자로 표현식을 사용할 수 있게 합니다. 이를 통해 변수의 초기값을 지정할 수 있습니다.

이 기능은 특히 `encoding/json` 또는 포털 버퍼와 같이 포인터를 사용하여 선택적 값을 나타내는 패키지를 사용할 때 유용합니다. 예를 들어, 선택적 필드를 간단한 표현식으로 채울 수 있도록 합니다.

```markdown
```go
import "encoding/json"

type Person struct {
	Name string   `json:"name"`
	Age  *int     `json:"age"` // age가 알려진 경우; 그렇지 않으면 nil
}

func personJSON(name string, born time.Time) ([]byte, error) {
	return json.Marshal(Person{
		Name: name,
		Age:  new(yearsSince(born)),
	})
}

func yearsSince(t time.Time) int {
	return int(time.Since(t).Hours() / (365.25 * 24)) // 대략적인 값
}
```

<!-- https://go.dev/issue/75883 -->

일반적인 타입이 타입 매개변수 목록에서 자기 자신을 참조하는 것을 제한하는 규칙이 완화되었습니다.
이제 제약 조건이 지정될 수 있으며, 이러한 제약 조건은 제약되는 일반적인 타입에 참조할 수 있습니다.
예를 들어, `Adder`라는 일반적인 타입은 다음과 같은 타입으로 인스턴스화되어야 합니다:

```markdown
```go
type Adder[A Adder[A]] 인터페이스 {
	Add(A) A
}

func algo[A Adder[A]](x, y A) A {
	return x.Add(y)
}
```

이전에는 `Adder`에 대한 자기 참조가 첫 번째 줄에서 허용되지 않았습니다.
이 변경은 단순히 타입 제약 조건을 더욱 강력하게 만드는 것 외에도, 타입 매개변수에 대한 사양 규칙을 약간 단순화합니다.

## 도구 {#tools}

### Go 명령어 {#go-명령어}

<!-- go.dev/issue/75432 -->
오래된 `go fix` 명령어가 완전히 재구축되었으며, 이제 Go의 *현대화 도구*가 되었습니다. 이 도구는 Go 코드 기반을 최신 스타일과 핵심 라이브러리 API로 업데이트하는 안정적이고 간단한 방법을 제공합니다. 초기 현대화 도구에는 Go 언어 및 라이브러리의 최신 기능을 활용하기 위한 수십 개의 패치가 포함되어 있으며, 사용자들은 [`//go:fix inline` 지시문을](https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/inline#hdr-Analyzer_inline) 사용하여 자체 API 마이그레이션을 자동화할 수 있는 소스 레벨 인라이너도 제공됩니다. 이러한 패치는 프로그램의 동작을 변경하지 않아야 합니다. 따라서 `go fix`를 사용하여 패치를 적용할 때 문제가 발생하면 [보고해주세요](/issue/new).

`go fix` 명령은 `go vet`와 정확히 동일한 [Go 분석
프레임워크](https://pkg.go.dev/golang.org/x/tools/go/analysis)를 기반으로 구축됩니다.
이는 `go vet`에서 제공하는 진단 기능을 제공하는 동일한 분석기가 `go fix`에서 제안하고 적용하는 데 사용될 수 있음을 의미합니다.
역사적인 `go fix`의 모든 고전적인 고정기(모두는 더 이상 사용되지 않음)가 제거되었습니다.

두 개의 다가오는 Go 블로그 게시물에서는 최신 버전의 도구, inliner, 그리고 `go fix`를 최대한 활용하는 방법에 대해 자세히 설명합니다.
<!-- TODO(adonovan): 게시물이 게시되면 링크를 추가. -->

<!-- go.dev/issue/74748 -->
`go mod init`은 새로운 `go.mod` 파일에서 더 낮은 `go` 버전을 기본값으로 사용합니다.
`go mod init`을 실행하는 경우
버전 `1.N.X`의 툴체인을 사용하는 경우, `go.mod` 파일이 생성되어 Go 버전 `go 1.(N-1).0`을 지정합니다. `1.N`의 프리릴리즈 버전은
`go.mod` 파일을 생성하여 Go 버전 `go 1.(N-2).0`을 지정합니다. 예를 들어, Go 1.26 릴리스 후보는 `go 1.24.0`을 포함하는 `go.mod` 파일을 생성하고, Go 1.26 및 그 마이너 릴리스는 `go 1.25.0`을 포함하는 `go.mod` 파일을 생성합니다. 이는 현재 지원되는 Go 버전과 호환되는 모듈을 만드는 것을 장려하기 위한 것입니다. 새로운 모듈에서 `go` 버전을 제어하기 위해 `go mod init` 다음에 `go get go@version`을 실행할 수 있습니다.

<!-- go.dev/issue/74667 -->
`cmd/doc` 및 `go tool doc`가 삭제되었습니다. `go doc`를 사용하여 대체할 수 있습니다: 동일한 플래그와 인수를 사용하며 동일한 동작을 합니다.

### Pprof {#pprof}

<!-- go.dev/issue/74774 -->
`-http` 플래그를 사용하여 활성화된 `pprof` 도구의 웹 UI는 기본적으로 플레임 그래프 뷰를 표시합니다.
이전의 그래프 뷰는 "보기 -> 그래프" 메뉴를 통해 또는 `/ui/graph` 경로를 통해 사용할 수 있습니다.

## 실행 시점 {#runtime}

### 새로운 가비지 컬렉터

"그린 티" 가비지 컬렉터는 이전에는 Go 1.25에서 실험 버전으로 제공되었으나, 피드백을 반영하여 이제 기본적으로 활성화됩니다.

이 가비지 컬렉터의 설계는 더 나은 지역성 및 CPU 확장성을 통해 작은 객체의 마킹 및 스캔 성능을 향상시킵니다.
벤치마크 결과는 다양하지만, 실제 프로그램에서 가비지 컬렉터를 과도하게 사용하는 경우, 가비지 컬렉션 오버헤드에서 10–40% 감소를 기대합니다.
새로운 amd64 기반 CPU 플랫폼(Intel Ice Lake 또는 AMD Zen 4 및 그 이후)에서 실행할 때, 가비지 컬렉터가 가능한 경우 벡터 명령어를 사용하여 작은 객체를 스캔함으로써, 가비지 컬렉션 오버헤드에서 10% 정도의 추가 개선이 예상됩니다.

새로운 가비지 컬렉터는 빌드 시간에 다음을 설정하여 비활성화할 수 있습니다.
`GOEXPERIMENT=nogreenteagc`
이 비활성화 설정은 Go 1.27에서 제거될 것으로 예상됩니다.
성능 또는 동작과 관련된 어떤 이유로든 새 가비지 컬렉터를 비활성화하는 경우, [문제 보고](/issue/new)해 주십시오.

### cgo 호출 성능 향상

<!-- CL 646198 -->

cgo 호출의 기본 실행 오버헤드가 약 30% 감소했습니다.

### 힙 베이스 주소 무작위화

<!-- CL 674835 -->

64비트 플랫폼에서는 런타임이 시작 시 힙 베이스 주소를 무작위로 설정합니다.
이는 cgo를 사용할 때 공격자가 메모리 주소를 예측하고 취약점을 악용하는 것을 어렵게 만드는 보안 강화 기능입니다.
이 기능을 비활성화하려면 빌드 시 `GOEXPERIMENT=norandomizedheapbase64`를 설정할 수 있습니다.
이 옵트아웃 설정은 향후 Go 릴리스에서 제거될 것으로 예상됩니다.

### 실험적인 고루틴 누출 프로필 {#goroutineleak-profiles}

<!-- CL 688335 -->

새로운 프로파일 유형으로, 누수된 고루틴을 보고하는 기능이 실험 버전으로 제공됩니다.
새로운 프로파일 유형인 `goroutineleak`은 `[`runtime/pprof`](/pkg/runtime/pprof) 패키지에 있으며, 빌드 시간에 `GOEXPERIMENT=goroutineleakprofile`로 설정하여 활성화할 수 있습니다.
실험을 활성화하면 프로파일도 `[`net/http/pprof`](/pkg/net/http/pprof) 엔드포인트인 `/debug/pprof/goroutineleak`로 사용할 수 있습니다.

*누수된* goroutine은 특정 동시성 원자 (채널, [`sync.Mutex`](/pkg/sync#Mutex), [`sync.Cond`](/pkg/sync#Cond) 등)에서 차단된 goroutine을 의미하며, 이 goroutine이 다시 실행 불가능합니다.
런타임은 가비지 컬렉터를 사용하여 누수된 goroutine을 감지합니다. 만약 goroutine G가 특정 동시성 원자 P에서 차단되어 있고, P가 실행 가능한 다른 어떤 goroutine 또는 *그것들*이 다시 실행할 수 없는 원자에서 접근할 수 없다면, P는 다시 실행될 수 없으므로, goroutine G는 절대 깨어나지 않습니다.
모든 경우에 영구적으로 차단된 goroutine을 감지하는 것은 불가능하지만, 이 접근 방식은 이러한 누수의 많은 종류를 감지합니다.

다음 예제는 실제 세계에서 발생할 수 있는 고루틴 누출을 보여줍니다. 이 누출은 새로운 프로파일을 사용하여 감지할 수 있습니다:

```markdown
```go
type result struct {
	res workResult
	err error
}

func processWorkItems(ws []workItem) ([]workResult, error) {
	// 작업 항목을 병렬로 처리하고, 결과를 ch 채널에 집계합니다.
	ch := make(chan result)
	for _, w := range ws {
		go func() {
			res, err := processWorkItem(w)
			ch <- result{res, err}
		}()
	}

	// ch 채널에서 결과를 수집하거나, 오류가 발견되면 오류를 반환합니다.
	var results []workResult
	for range len(ws) {
		r := <-ch
		if r.err != nil {
			// 이 조기 반환은 goroutine 누수를 발생시킬 수 있습니다.
			return nil, r.err
		}
		results = append(results, r.res)
	}
	return results, nil
}
```

`ch`가 버퍼링되지 않았기 때문에, `processWorkItems`가 오류로 인해 조기에 종료되면, 남아 있는 모든 `processWorkItem` 고루틴이 누출됩니다.
이 상황이 발생하면, `ch`는 누출에 관련된 고루틴 외의 다른 고루틴에게 더 이상 접근할 수 없게 되어 런타임이 누출된 고루틴을 감지하고 보고할 수 있습니다.

이 기술은 "닿음성"을 기반으로 하므로, 런타임은 전역 변수를 통해 또는 실행 가능한 goroutine의 로컬 변수를 통해 도달 가능한 동시성 프라임티브에서 발생하는 누출을 식별하지 못할 수 있습니다.

특히 Uber의 Vlad Saioc 님에게 이 작업을 기여해주신 것에 감사드립니다.

기본 이론은 [Saioc et al의 논문](https://dl.acm.org/doi/pdf/10.1145/3676641.3715990)에서 자세히 설명되어 있습니다.

이 구현은 실제 사용 가능하며, API에 대한 피드백을 수집하기 위한 실험으로만 간주됩니다. 특히, 이를 새로운 프로파일로 만드는 선택에 초점을 맞추고 있습니다.
또한, 이 기능은 실제로 사용될 때만 추가적인 실행 시간 오버헤드가 발생하도록 설계되었습니다.

저희는 사용자들이 새로운 기능을 [Go
플레이그라운드](https://play.golang.org/p/3C71z4Dpav-?v=gotip)에서, 테스트, 지속적 통합, 그리고 프로덕션 환경에서 사용해 보기를 권장합니다.
[제안
이슈](https://go.dev/issue/74609)에 대한 추가적인 피드백을 환영합니다.

우리는 Go 1.27에서 기본적으로 고루틴 누출 프로파일을 활성화하는 것을 목표로 합니다.

## 컴파일러

<!-- CL 707755, 722440 -->

컴파일러는 이제 스택에 슬라이스용 백잉 백을 더 많은 상황에서 할당할 수 있으며, 이는 성능을 향상시킵니다. 이 변경으로 인해 문제가 발생하면 [bisect 도구](https://pkg.go.dev/golang.org/x/tools/cmd/bisect)를 사용하여 `-compile=variablemake` 플래그를 사용하여 문제를 일으키는 할당을 찾을 수 있습니다. 이러한 모든 새로운 스택 할당을 `-gcflags=all=-d=variablemakehash=n`을 사용하여 비활성화할 수도 있습니다.
이 최적화와 관련된 문제가 발생하면 [문제 보고](/issue/new)하십시오.

## 링커 {#linker}

64비트 ARM 기반의 Windows ( `windows/arm64` 포트)에서는 링커가 이제 cgo 프로그램의 내부 링킹 모드를 지원합니다. 이를 `-ldflags=-linkmode=internal` 플래그를 사용하여 요청할 수 있습니다.

실행 파일에 대한 몇 가지 작은 변경 사항이 있습니다. 이러한 변경 사항은 Go 프로그램을 실행하는 데 영향을 미치지 않습니다. 그러나 Go 실행 파일을 분석하는 프로그램에 영향을 미칠 수 있으며, 사용자 정의 링커 스크립트를 사용하는 외부 링킹 모드를 사용하는 사람에게 영향을 미칠 수도 있습니다.

- `moduledata` 구조가 이제 자체 섹션, 이름 `.go.module`으로 분리되었습니다.
- `moduledata`의 `cutab` 필드 (슬라이스)의 길이가 이제 정확합니다. 이전에는 길이가 4배 더 컸습니다.
- `.gopclntab` 섹션의 시작 부분에 있던 `pcHeader`가 이제 텍스트 섹션의 시작을 기록하지 않습니다. 이 필드는 이제 항상 0입니다.
- 이 `pcHeader` 변경은 `.gopclntab` 섹션에 더 이상 위치 정보가 없도록 하기 위해 이루어졌습니다. relro를 지원하는 플랫폼에서는 이 섹션이 relro 세그먼트에서 rodata 세그먼트로 이동했습니다.
- funcdata 심볼과 findfunctab이 `.rodata` 섹션에서 `.gopclntab` 섹션으로 이동했습니다.
- `.gosymtab` 섹션이 제거되었습니다. 이전에는 항상 존재했지만 비어 있었습니다.
- 내부 링크를 사용할 때, ELF 섹션은 이제 주소별로 섹션 헤더 목록에 나타납니다. 이전에는 순서가 다소 예측 불가능했습니다.

여기 섹션 이름에 사용된 명칭은 Linux 및 기타 시스템에서 볼 수 있는 ELF 명칭을 사용합니다. Darwin에서 볼 수 있는 Mach-O 명칭은 두 개의 밑줄로 시작하며 점(.)을 포함하지 않습니다.

## 부트스트랩 {#bootstrap}

<!-- go.dev/issue/69315 -->
[Go 1.24 릴리스 노트](https://go.dev/doc/go1.24#bootstrap)에 언급된 대로, Go 1.26에서는 런타임을 설치하기 위해 Go 1.24.6 또는 그 이후 버전이 필요합니다.
Go 1.28 역시 런타임을 설치하기 위해 Go 1.26의 미니 릴리스 또는 그 이후 버전이 필요할 것으로 예상됩니다.

## 표준 라이브러리 {#library}

### 새로운 암호/HPKE 패키지

새로운 [`crypto/hpke`](/pkg/crypto/hpke) 패키지는 [RFC 9180](https://rfc-editor.org/rfc/rfc9180.html)에 명시된 하이브리드 공개 키 암호화 (HPKE)를 구현하며, 포스트-퀀텀 하이브리드 KEM에 대한 지원도 포함합니다.

### 새로운 실험적인 simd/archsimd 패키지 {#simd}

Go 1.26 버전에서는 새로운 실험적인 [`simd/archsimd`](/pkg/simd/archsimd/) 패키지를 도입했습니다. 이 패키지는 빌드 시간에 환경 변수 `GOEXPERIMENT=simd`를 설정하여 활성화할 수 있습니다.
이 패키지는 아키텍처별 SIMD 연산에 대한 액세스를 제공합니다.
현재는 amd64 아키텍처에서 사용할 수 있으며, 128비트, 256비트, 512비트 벡터 유형을 지원합니다 (예: [`Int8x16`](/pkg/simd/archsimd#Int8x16) 및 [`Float64x8`](/pkg/simd/archsimd#Float64x8)와 함께 [`Int8x16.Add`](/pkg/simd/archsimd#Int8x16.Add)와 같은 연산).
API는 아직 안정적으로 고려되지 않습니다.

향후 버전에서 다른 아키텍처를 지원할 계획이지만,
API는 의도적으로 아키텍처 특정이며, 따라서 이식성이 없습니다.
또한, 향후 고수준의 이식 가능한 SIMD 패키지를 개발할 계획입니다.

자세한 내용은 [패키지 설명서](/pkg/simd/archsimd) 및 [제안 이슈](/issue/73787)를 참조하십시오.

### 새로운 실험적인 런타임/비밀 패키지

<!-- https://go.dev/issue/21865 -->

새로운 [`runtime/secret`](/pkg/runtime/secret) 패키지는 실험 단계로 제공되며, 빌드 시간에 환경 변수 `GOEXPERIMENT=runtimesecret`를 설정하여 활성화할 수 있습니다.
이는 비밀 정보를 다루는 코드에서 사용되는 임시 파일을 안전하게 삭제하는 기능을 제공합니다. 일반적으로 암호화와 관련된 방식으로, 레지스터, 스택, 새로운 힙 할당 등을 관리하는 데 사용됩니다.
이 패키지는 [전방 보안](https://en.wikipedia.org/wiki/Forward_secrecy)을 더 쉽게 보장하는 데 도움이 되도록 설계되었습니다.
현재 Linux에서 amd64 및 arm64 아키텍처를 지원합니다.

### 라이브러리의 세부 변경 사항 {#minor_library_changes}

#### [`bytes`](/pkg/bytes/)

새로운 `Buffer.Peek` 메서드는 버퍼에서 다음 n 바이트를 반환하지만, 버퍼의 위치를 변경하지 않습니다.

```
#### [`crypto`](/pkg/crypto/)
```

새로운 [`Encapsulator`](/pkg/crypto#Encapsulator) 및 [`Decapsulator`](/pkg/crypto#Decapsulator) 인터페이스는 추상적인
KEM 암호화 또는 해제 키를 허용합니다.

#### [`crypto/dsa`](/pkg/crypto/dsa/)

`[GenerateKey](pkg/crypto/dsa#GenerateKey)`의 `random` 매개변수는 이제 무시됩니다.
대신, 이제는 항상 안전한 방식으로 암호학적으로 무작위 바이트를 사용합니다.
결정론적 테스트를 위해, 새로운 `[testing/cryptotest.SetGlobalRandom](pkg/testing/cryptotest#SetGlobalRandom)` 함수를 사용하십시오.
새로운 GODEBUG 설정 `cryptocustomrand=1`은 임시적으로 이전 동작을 복원합니다.

#### [`crypto/ecdh`](/pkg/crypto/ecdh/)

`Curve.GenerateKey` 함수의 `random` 매개변수는 이제 무시됩니다.
대신, 항상 안전한 암호학적으로 무작위 바이트 소스를 사용합니다.
판별 가능한 테스트를 위해, 새로운 `testing/cryptotest.SetGlobalRandom` 함수를 사용하십시오.
새로운 GODEBUG 설정 `cryptocustomrand=1`은 기존 동작을 일시적으로 복원합니다.

새로운 [`KeyExchanger`](/pkg/crypto/ecdh#KeyExchanger) 인터페이스, [`PrivateKey`](/pkg/crypto/ecdh#PrivateKey)에 의해 구현되어, 추상 ECDH 개인 키를 받아들일 수 있도록 합니다. 예를 들어, 하드웨어에서 구현된 키를 받을 수 있습니다.

#### [`crypto/ecdsa`](/pkg/crypto/ecdsa/)

`big.Int` 필드인 `PublicKey` 및 `PrivateKey`의 필드는 이제 사용되지 않습니다.

다음 함수에서 사용되는 `random` 파라미터는 이제 무시됩니다: [`GenerateKey`](/pkg/crypto/ecdsa#GenerateKey), [`SignASN1`](/pkg/crypto/ecdsa#SignASN1), [`Sign`](/pkg/crypto/ecdsa#Sign), [`PrivateKey.Sign`](/pkg/crypto/ecdsa#PrivateKey.Sign).
대신, 이 함수들은 항상 안전한 방식으로 생성된 암호학적으로 무작위 바이트를 사용합니다.
판별 가능한 테스트를 위해서는 새로운 [`testing/cryptotest.SetGlobalRandom`](/pkg/testing/cryptotest#SetGlobalRandom) 함수를 사용하십시오.
새로운 GODEBUG 설정 `cryptocustomrand=1`은 이전 동작을 일시적으로 복원합니다.

#### [`crypto/ed25519`](/pkg/crypto/ed25519/)

만약 `[`GenerateKey`](/pkg/crypto/ed25519#GenerateKey)에 전달되는 임의의 파라미터가 `nil`이면, `GenerateKey`는 이제 `crypto/rand.Reader`](/pkg/crypto/rand#Reader) 대신, 안전한 암호학적으로 무작위 바이트 소스를 항상 사용합니다 (이 소스는 덮어쓸 수 있었습니다). 새로운 GODEBUG 설정 `cryptocustomrand=1`은 기존 동작을 일시적으로 복원합니다.

#### [`crypto/fips140`](/pkg/crypto/fips140/)

[FIPS 140-3 Go 암호화 모듈](/doc/security/fips140) v1.26.0는 `crypto/internal/fips140/...` 패키지에 이 버전까지 적용된 변경 사항을 포함하며, 이제 GOFIPS140을 사용하여 선택할 수 있습니다.

새로운 [`WithoutEnforcement`](/pkg/crypto/fips140#WithoutEnforcement) 및 [`Enforced`](/pkg/crypto/fips140#Enforced) 함수를 사용하면 선택적으로 엄격한 FIPS 140-3 검사를 비활성화하면서 `GODEBUG=fips140=only` 모드로 실행할 수 있습니다.

[`Version`](/pkg/crypto/fips140#Version)는 `GOFIPS140`로 빌드될 때 해결된 FIPS 140-3 Go 암호화 모듈 버전을 반환합니다.

```
#### [`crypto/mlkem`](/pkg/crypto/mlkem/)
```

새로운 [`DecapsulationKey768.Encapsulator`](/pkg/crypto/mlkem#DecapsulationKey768.Encapsulator) 및
[`DecapsulationKey1024.Encapsulator`](/pkg/crypto/mlkem#DecapsulationKey1024.Encapsulator) 메서드는 새로운
[`crypto.Decapsulator`](/pkg/crypto#Decapsulator) 인터페이스를 구현합니다.

캡슐화 및 디캡슐화 작업이 이제 약 18% 더 빠릅니다.

#### [`crypto/mlkem/mlkemtest`](/pkg/crypto/mlkem/mlkemtest/)

새로운 [`crypto/mlkem/mlkemtest`](/pkg/crypto/mlkem/mlkemtest) 패키지는 알려진 답을 사용하는 테스트에 사용되는 `Encapsulate768`](/pkg/crypto/mlkem/mlkemtest#Encapsulate768) 및
`Encapsulate1024`](/pkg/crypto/mlkem/mlkemtest#Encapsulate1024) 함수를 노출합니다. 이 함수들은 난독화된 ML-KEM 인캡슐레이션을 구현합니다.

```
#### [`crypto/rand`](/pkg/crypto/rand/)

`[`Prime`](/pkg/crypto/rand#Prime) 함수의 `random` 매개변수는 이제 무시됩니다.
대신, 항상 암호학적으로 무작위 바이트의 안전한 소스를 사용합니다.
결정적인 테스트를 위해, 새로운 `[testing/cryptotest.SetGlobalRandom](https://example.com/pkg/testing/cryptotest#SetGlobalRandom)` 함수를 사용하십시오 (실제 URL로 대체).
새로운 GODEBUG 설정 `cryptocustomrand=1`은 이전 동작을 일시적으로 복원합니다.

```
#### [`crypto/rsa`](/pkg/crypto/rsa/)
```

새로운 [`EncryptOAEPWithOptions`](/pkg/crypto/rsa#EncryptOAEPWithOptions) 함수는 OAEP 패딩 및 MGF1 마스크 생성에 사용되는 다른 해시 함수를 지정할 수 있도록 합니다.

`[`GenerateKey`](/pkg/crypto/rsa#GenerateKey), `[`GenerateMultiPrimeKey`](/pkg/crypto/rsa#GenerateMultiPrimeKey), 및 `EncryptPKCS1v15`](/pkg/crypto/rsa#EncryptPKCS1v15) 함수의 `random` 매개변수는 더 이상 무시되지 않습니다.
대신, 이 함수들은 항상 안전한 암호학적으로 무작위 바이트 소스를 사용합니다.
결정론적인 테스트를 위해서는 새로운 `[`testing/cryptotest.SetGlobalRandom`](/pkg/testing/cryptotest#SetGlobalRandom) 함수를 사용하십시오.
새로운 GODEBUG 설정 `cryptocustomrand=1`은 이전 동작을 일시적으로 복원합니다.

만약 [`PrivateKey`](/pkg/crypto/rsa#PrivateKey) 필드가 `PrivateKey.Precompute()`를 호출한 후 수정되면,
[`PrivateKey.Validate`](/pkg/crypto/rsa#PrivateKey.Validate)가 이제 실패합니다.

[`PrivateKey.D`](/pkg/crypto/rsa#PrivateKey.D)는 이제 미리 계산된 값과 일치하는지 확인되지만, 실제로 사용되지 않더라도 그렇습니다.

`Unsafe PKCS #1 v1.5 암호화 패딩 ([`EncryptPKCS1v15`](/pkg/crypto/rsa#EncryptPKCS1v15),
[`DecryptPKCS1v15`](/pkg/crypto/rsa#DecryptPKCS1v15), 및 [`DecryptPKCS1v15SessionKey`](/pkg/crypto/rsa#DecryptPKCS1v15SessionKey)에 의해 구현됨)은 더 이상 사용되지 않습니다.

#### [`crypto/sha3`](/pkg/crypto/sha3/)

`[SHA3](pkg/crypto/sha3#SHA3)`의 0 값은 이제 사용 가능한 SHA3-256 인스턴스이고, `[SHAKE](pkg/crypto/sha3#SHAKE)`의 0 값은 이제 사용 가능한 SHAKE256 인스턴스입니다.

#### [`crypto/subtle`](/pkg/crypto/subtle)

[`WithDataIndependentTiming`](/pkg/crypto/subtle#WithDataIndependentTiming)
함수가 전달된 함수를 실행하는 동안 호출되는 goroutine을 OS 스레드에 묶지 않습니다. 또한, 전달된 함수 실행 중에 생성된 goroutine 및 그 후손은 이제 해당 수명 동안 `WithDataIndependentTiming`의 속성을 상속합니다. 이 변경 사항은 다음 방식으로 cgo에도 영향을 미칩니다:

- `WithDataIndependentTiming`에 전달된 함수 내에서 또는 이 함수에서 생성된 goroutine 및 그 후손에서 호출되는 모든 C 코드는 호출 기간 동안 데이터 독립적 타이밍이 활성화됩니다. C 코드가 데이터 독립적 타이밍을 비활성화하는 경우, Go로 반환될 때 다시 활성화됩니다.
- `WithDataIndependentTiming`에 전달된 함수 또는 다른 곳에서 호출되는 C 코드가 cgo를 통해 데이터 독립적 타이밍을 활성화하거나 비활성화하는 경우, Go로 호출될 때 해당 상태가 호출 기간 동안 유지됩니다.

#### [`crypto/tls`](/pkg/crypto/tls/)

하이브리드 [`SecP256r1MLKEM768`](/pkg/crypto/tls#SecP256r1MLKEM768) 및 [`SecP384r1MLKEM1024`](/pkg/crypto/tls#SecP384r1MLKEM1024) 포스트-양자 키 교환 기능은 기본적으로 활성화됩니다. 이 기능을 비활성화하려면 `Config.CurvePreferences` 설정을 변경하거나 `tlssecpmlkem=0` GODEBUG 설정을 사용하십시오.

새로운 `ClientHelloInfo.HelloRetryRequest` 필드는 클라이언트가 `HelloRetryRequest` 메시지에 응답으로 `ClientHello`를 보냈는지 여부를 나타냅니다. 새로운 `ConnectionState.HelloRetryRequest` 필드는 서버가 `HelloRetryRequest`를 보냈는지, 또는 클라이언트가 `HelloRetryRequest`를 수신했는지, 연결 역할에 따라 구분합니다.

[`QUICConn`](/pkg/crypto/tls#QUICConn) 유형은 QUIC 구현에서 사용되며, TLS 핸드셰이크 오류를 보고하기 위한 새로운 이벤트를 포함합니다.

만약 [`Certificate.PrivateKey`](/pkg/crypto/tls#Certificate.PrivateKey)가 [`crypto.MessageSigner`](/pkg/crypto#MessageSigner)를 구현한다면, TLS 1.2 이후 버전에서는 SignMessage
메서드가 Sign 대신 사용됩니다.

다음 GODEBUG 설정은 [Go 1.22](/doc/godebug#go-122) 및 [Go 1.23](/doc/godebug#go-123)에 도입되었으며, 다음 주요 Go 릴리스에서 제거됩니다.
Go 1.27부터, 새로운 동작은 GODEBUG 설정 또는 go.mod 언어 버전에 관계없이 적용됩니다.

- `tlsunsafeekm`: [`ConnectionState.ExportKeyingMaterial`](/pkg/crypto/tls#ConnectionState.ExportKeyingMaterial)는 TLS 1.3 또는 확장된 마스터 시크릿을 필요로 합니다.
- `tlsrsakex`: ECDH가 없는 기존 RSA만 사용하는 키 교환은 기본적으로 활성화되지 않습니다.
- `tls10server`: 클라이언트와 서버 모두의 기본 최소 TLS 버전은 TLS 1.2입니다.
- `tls3des`: 기본 암호화 모음에는 3DES가 포함되지 않습니다.
- `x509keypairleaf`: [`X509KeyPair`](/pkg/crypto/tls#X509KeyPair) 및 [`LoadX509KeyPair`](/pkg/crypto/tls#LoadX509KeyPair)는 항상 [`Certificate.Leaf`](/pkg/crypto/tls#Certificate.Leaf) 필드를 채웁니다.

#### [`crypto/x509`](/pkg/crypto/x509/)

[`ExtKeyUsage`](/pkg/crypto/x509#ExtKeyUsage) 및 [`KeyUsage`](/pkg/crypto/x509#KeyUsage) 유형에는 이제 `String` 메서드가 있으며, 이 메서드는 RFC 5280 및 기타 레지스트리에 정의된 해당 OID 이름을 반환합니다.

[`ExtKeyUsage`](/pkg/crypto/x509#ExtKeyUsage) 타입에 이제 `OID` 메서드가 추가되어, 해당 EKU에 대한 OID를 반환합니다.

새로운 [`OIDFromASN1OID`](/pkg/crypto/x509#OIDFromASN1OID) 함수는 [`encoding/asn1.ObjectIdentifier`](/pkg/encoding/asn1#ObjectIdentifier)를
[`OID`](/pkg/crypto/x509#OID)로 변환하는 기능을 제공합니다.

#### [`debug/elf`](/pkg/debug/elf/)

추가 `R_LARCH_*` 상수는 [LoongArch ELF psABI v20250521](https://github.com/loongson/la-abi-specs/blob/v2.40/laelf.adoc)에서 정의되어 LoongArch 시스템에서 사용됩니다.
(전역 버전 v2.40)

#### [`errors`](/pkg/errors/)

새로운 [`AsType`](/pkg/errors#AsType) 함수는 [`As`](/pkg/errors#As) 함수의 일반적인 버전입니다. 이 함수는 타입 안전하고 빠르며, 대부분의 경우 사용하기 더 쉽습니다.

#### [`fmt`](/pkg/fmt/)

<!-- go.dev/cl/708836 -->
비 형식화된 문자열의 경우, `fmt.Errorf("x")`는 이제 더 적은 메모리를 할당하고, 일반적으로 `errors.New("x")`에 해당하는 메모리 할당을 제공합니다.

#### [`go/ast`](/pkg/go/ast/)

새로운 [`ParseDirective`](/pkg/go/ast#ParseDirective) 함수는 [지시문
주석](/doc/comment#Syntax)을 파싱합니다. 이는 `//go:generate`와 같은 주석입니다.
소스 코드 도구는 자체 지시문 주석을 지원할 수 있으며, 이 새로운 API는 이를 사용하여 일반적인 구문을 구현하는 데 도움이 됩니다.

<!-- go.dev/issue/76395 -->
새로운 `BasicLit.ValueEnd` 필드는 리터럴의 정확한 끝 위치를 기록하여, `BasicLit.End` 메서드가 항상 올바른 값을 반환할 수 있도록 합니다. (이전에는 윈도우 소스 파일의 다중 줄 Raw 문자열 리터럴에 대해, 캐리지 리턴 제거로 인해, 오버랩된 방식으로 계산되었는데, 이 방식이 정확하지 않았습니다.)

프로그래밍이 `BasicLit` 유형의 파서에서 생성된 `ValuePos` 필드를 업데이트하는 경우, 출력 형식의 미세한 차이를 방지하기 위해 `ValueEnd` 필드를 업데이트하거나 지워야 할 수도 있습니다.

#### [`go/token`](/pkg/go/token/)

새로운 `[`File.End`](/pkg/go/token#File.End) 편의 메서드는 파일의 끝 위치를 반환합니다.

#### [`go/types`](/pkg/go/types/)

`gotypesalias` GODEBUG 설정은 [Go 1.22](/doc/godebug#go-122)에 도입되었지만, 다음 주요 Go 릴리스에서 제거됩니다.
Go 1.27부터, `go/types` ([/pkg/go/types](https://golang.org/ref/pkg/go/types)) 패키지는 GODEBUG 설정이나 go.mod 언어 버전에 관계없이 항상 [Alias 타입](/pkg/go/types#Alias)을 [타입 별칭](/ref/spec#Type_declarations)의 표현에 생성합니다.

#### [`image/jpeg`](/pkg/image/jpeg/)

JPEG 인코더 및 디코더는 새로운, 더 빠르고 정확한 구현으로 대체되었습니다.
인코더 또는 디코더에서 특정 비트 단위의 출력을 예상하는 코드는 업데이트가 필요할 수 있습니다.

#### [`io`](/pkg/io/)

<!-- go.dev/cl/722500 -->
[`ReadAll`](/pkg/io#ReadAll)가 이제 덜한 중간 메모리를 할당하고, 최소 크기의 최종 슬라이스를 반환합니다. 일반적으로 약 두 배 더 빠르며, 전체 메모리 할당량은 대략 절반 정도로 줄어듭니다. 특히 큰 입력의 경우 효과가 더 큽니다.

#### [`log/slog`](/pkg/log/slog/)

[`NewMultiHandler`](/pkg/log/slog#NewMultiHandler) 함수는 모든 주어진 핸들러를 호출하는
[`MultiHandler`](/pkg/log/slog#MultiHandler)를 생성합니다.
`Enabled` 메서드는 핸들러의 `Enabled` 메서드 중 하나라도 `true`를 반환하는지 여부를 보고합니다.
`Handle`, `WithAttrs` 및 `WithGroup` 메서드는 활성화된 각 핸들러의 해당 메서드를 호출합니다.

#### [`net`](/pkg/net/)

새로운 [`Dialer`](/pkg/net/#Dialer) 메서드
[`DialIP`](/pkg/net/#Dialer.DialIP),
[`DialTCP`](/pkg/net/#Dialer.DialTCP),
[`DialUDP`](/pkg/net/#Dialer.DialUDP), 및
[`DialUnix`](/pkg/net/#Dialer.DialUnix)
은 특정 네트워크 유형을 지정하고 컨텍스트 값을 함께 사용하여 연결을 설정할 수 있습니다.

#### [`net/http`](/pkg/net/http/)

새로운
[`HTTP2Config.StrictMaxConcurrentRequests`](/pkg/net/http#HTTP2Config.StrictMaxConcurrentRequests)
필드는 기존 HTTP/2 연결이 스트림 제한을 초과했을 때 새로운 연결을 여야 하는지 제어합니다.

새로운 `Transport.NewClientConn` 메서드는 HTTP 서버에 대한 클라이언트 연결을 반환합니다.
대부분의 사용자는 [`Transport.RoundTrip`](/pkg/net/http#Transport.RoundTrip) 메서드를 사용하여 요청을 보내는 것을 계속 사용하는 것이 좋습니다. 이 메서드는 연결 풀을 관리합니다.
`NewClientConn`은 자체 연결 관리 기능을 구현해야 하는 사용자에게 유용합니다.

[`Client`](/pkg/net/http#Client)는 이제 `Request.Host`가 사용 가능한 경우 호스트 부분과 일치하는 URL 범위에 대한 쿠키를 사용하고 설정합니다.
이전에는 항상 연결 주소의 호스트가 사용되었습니다.
[`ServeMux`](/pkg/net/http#ServeMux)의 trailing slash 리디렉션은 이제 307 (Temporary Redirect) HTTP 상태 코드를 사용합니다. (이전에는 301 (Moved Permanently)을 사용했습니다.)

#### [`net/http/httptest`](/pkg/net/http/httptest/)

`Server.Client`에서 반환된 HTTP 클라이언트는 이제 `example.com` 및 모든 하위 도메인에 대한 요청을 테스트 중인 서버로 리디렉션합니다.

#### [`net/http/httputil`](/pkg/net/http/httputil/)

[`ReverseProxy.Director`](/pkg/net/http/httputil#ReverseProxy.Director) 구성 필드는
[`ReverseProxy.Rewrite`](/pkg/net/http/httputil#ReverseProxy.Rewrite)로 대체됩니다.

악의적인 클라이언트는 `Director` 함수에 의해 추가된 헤더를 제거할 수 있으며, 이를 "호프별"로 지정하여 수행합니다. `Director` API의 범위를 벗어나 이 문제를 해결하는 방법이 없기 때문에, Go 1.20에서 새로운 `Rewrite` 훅을 추가했습니다. `Rewrite` 훅은 프록시가 수신하는 원래 요청과 프록시가 전송할 예정인 출력 요청 모두에 제공됩니다.

`Director` 훅은 기본적으로 안전하지 않으므로, 이제 이를 폐기하고 있습니다.

```go
#### [`net/netip`](패키지)
```

새로운 `Prefix.Compare` 메서드는 두 개의 접두사를 비교합니다.

#### [`net/url`](/pkg/net/url/)

[`Parse`](/pkg/net/url#Parse)는 이제 호스트 서브컴포넌트에 콜론이 포함된 잘못된 URL을 거부합니다. 예를 들어 `http://::1/` 또는 `http://localhost:80:80/`입니다.
대괄호로 묶인 IPv6 주소를 포함하는 URL은 여전히 허용됩니다. 예를 들어 `http://[::1]/`입니다.
새로운 GODEBUG 설정 `urlstrictcolons=0`은 이전 동작을 복원합니다.

#### [`os`](/pkg/os/)

새로운 [`Process.WithHandle`](/pkg/os#Process.WithHandle) 메서드는 지원되는 플랫폼(Linux 5.4 이상에서 pidfd, Windows에서 Handle)에서 내부 프로세스 핸들에 대한 액세스를 제공합니다.

Windows에서, [`OpenFile`](/pkg/os#OpenFile)의 `flag` 매개변수는 이제 Windows에 특정한 파일 플래그의 모든 조합을 포함할 수 있습니다. 예를 들어 `FILE_FLAG_OVERLAPPED` 및 `FILE_FLAG_SEQUENTIAL_SCAN`과 같이, 파일 또는 장치 캐싱 동작, 접근 모드 및 기타 특수 목적 플래그를 제어하기 위해 사용할 수 있습니다.

#### [`os/signal`](/pkg/os/signal/)

[`NotifyContext`](/pkg/os/signal#NotifyContext)는 이제 반환된 컨텍스트를 [`context.CancelCauseFunc`](/pkg/context#CancelCauseFunc) 및 수신된 신호를 나타내는 오류를 사용하여 취소합니다.

#### [`reflect`](/pkg/reflect/)

새로운 메서드 [`Type.Fields`](/pkg/reflect#Type.Fields),
[`Type.Methods`](/pkg/reflect#Type.Methods),
[`Type.Ins`](/pkg/reflect#Type.Ins)
그리고 [`Type.Outs`](/pkg/reflect#Type.Outs)는 각각 구조체 타입의 필드, 함수 타입의 메서드, 입력 및 출력 매개변수를 반환하는 반복자를 반환합니다.

마찬가지로, 새로운 메서드 [`Value.Fields`](/pkg/reflect#Value.Fields) 및 [`Value.Methods`](/pkg/reflect#Value.Methods)는 각각 값의 필드 또는 메서드를 순회하는 반복자를 반환합니다.
각 반복은 필드 또는 메서드의 유형 정보(`StructField` 또는 [`Method`](/pkg/reflect#Method))와 함께 필드 또는 메서드 자체의 [`Value`](/pkg/reflect#Value)를 제공합니다.

#### [`runtime/metrics`](/pkg/runtime/metrics/)

여러 새로운 스케줄러 메트릭이 추가되었습니다. 여기에는 다음이 포함됩니다.
`/sched/goroutines` 접두사를 사용하여 다양한 상태(대기, 실행 가능 등)의 고루틴 수, 런타임이 인지하는 OS 스레드 수(`/sched/threads:threads`), 그리고 프로그램이 생성한 고루틴의 총 개수(`/sched/goroutines-created:goroutines`).

#### [`testing`](/pkg/testing/)

새로운 메서드 [`T.ArtifactDir`](/pkg/testing#T.ArtifactDir), [`B.ArtifactDir`](/pkg/testing#B.ArtifactDir), 및 [`F.ArtifactDir`](/pkg/testing#F.ArtifactDir)는 테스트 출력 파일(아티팩트)을 쓸 디렉토리를 반환합니다.

`-artifacts` 플래그를 `go test`에 제공하면,
이 디렉토리는 출력 디렉토리 ( `-outputdir`으로 지정되거나, 기본적으로 현재 디렉토리) 아래에 위치합니다.
그렇지 않으면, 아티팩트는 테스트가 완료된 후 삭제되는 임시 디렉토리에 저장됩니다.

첫 번째 `ArtifactDir` 호출 시 `-artifacts` 옵션이 제공되면, 디렉토리의 위치를 테스트 로그에 기록합니다.

예를 들어, `TestArtifacts`라는 이름의 테스트에서,
`t.ArtifactDir()`은 다음과 같이 출력합니다:

=== ARTIFACTS TestArtifacts /path/to/artifact/dir
```

<!-- go.dev/issue/73137 -->

[`B.Loop`](/pkg/testing#B.Loop) 메서드는 이제 루프 본체에서 인라인을 방지하지 않으므로, 예상치 못한 할당과 느린 벤치마크가 발생할 수 있습니다.
이 수정 사항을 통해, 모든 벤치마크가 기존의 `B.N`](/pkg/testing#B) 스타일에서 새로운 `B.Loop` 스타일로 변환될 수 있다고 예상합니다.
`for b.Loop() { ... }` 루프의 본체 내에서, 함수 호출 파라미터, 결과 및 할당된 변수는 여전히 유지되므로 컴파일러가 전체 벤치마크의 일부를 최적화하는 것을 방지합니다.

#### [`testing/cryptotest`](/pkg/testing/cryptotest/)

새로운 [`SetGlobalRandom`](/pkg/testing/cryptotest#SetGlobalRandom) 함수는 테스트 기간 동안 전역적으로 일관된 암호화 난수 소스를 설정합니다. 이는 `crypto/rand` 및 `crypto/...` 패키지에 존재하는 모든 암호화 난수 소스에 영향을 미칩니다.

#### [`time`](/pkg/time/)

`asynctimerchan` GODEBUG 설정은 [Go 1.23](/doc/godebug#go-123)에서 도입되었으며,
다음 주요 Go 릴리스에서 제거됩니다.
Go 1.27부터, `time` 패키지는 GODEBUG 설정이나 go.mod 언어 버전에 관계없이 항상 버퍼되지 않은 (동기) 채널을 사용하여 타이머를 사용합니다.

## 포트

### 다윈

<!-- go.dev/issue/75836 -->

Go 1.26는 macOS 12 Monterey에서만 실행되는 마지막 릴리스입니다. Go 1.27은 macOS 13 Ventura 또는 그 이후 버전을 요구합니다.

### FreeBSD

<!-- go.dev/issue/76475 -->

`GOOS=freebsd GOARCH=riscv64` 포트는 [비활성화됨](/wiki/PortingPolicy#broken-ports)으로 표시되었습니다. 자세한 내용은 [issue 76475](/issue/76475)를 참조하십시오.

### Windows

<!-- go.dev/issue/71671 -->

[공지](https://go.dev/doc/go1.25#windows)에 따르면, Go 1.25 릴리스 노트에 발표된 바와 같이,
[오류가 있는](https://go.dev/doc/go1.24#windows) 32비트 Windows/ARM 포트(`GOOS=windows` `GOARCH=arm`)가 제거되었습니다.

### PowerPC

<!-- go.dev/issue/76244 -->

Go 1.26은 big-endian 64비트 PowerPC 포트에서 ELFv1 ABI를 지원하는 마지막 릴리스입니다 (Linux에서: `GOOS=linux` `GOARCH=ppc64`).
Go 1.27에서는 ELFv2 ABI로 전환됩니다.
포트가 현재 다른 ELF 객체와의 링크를 지원하지 않으므로, 이 변경 사항은 사용자에게 투명하게 적용될 것으로 예상됩니다.

### RISC-V

<!-- CL 690497 -->

`linux/riscv64` 포트는 이제 레이스 감지 기능을 지원합니다.

### S390X

<!-- CL 719482 -->

`s390x` 포트는 이제 함수 인자와 결과를 레지스터를 사용하여 전달할 수 있도록 지원합니다.

### WebAssembly {#wasm}

웹 어셈블리 (WebAssembly)는 웹 브라우저에서 실행할 수 있는 바이너리 명령어 형식입니다. JavaScript보다 빠른 실행 속도를 제공하며, C, C++, Rust 등 다양한 언어로 작성된 코드를 웹에서 실행할 수 있게 해줍니다.

<!-- CL 707855 -->

컴파일러는 이제 부호 확장 및 비-트랩핑 플로팅 포인트에서 정수 변환 명령어를 조건 없이 사용합니다.
이 기능은 최소 Wasm 2.0부터 표준화되었습니다.
해당하는 `GOWASM` 설정인 `signext` 및 `satconv`는 이제 무시됩니다.

<!-- CL 683296 -->

웹 어셈블리 애플리케이션의 경우, 런타임은 이제 힙 메모리를 훨씬 작은 단위로 관리합니다. 따라서 16 MiB 미만의 크기를 가진 애플리케이션의 경우 메모리 사용량이 크게 감소합니다.
