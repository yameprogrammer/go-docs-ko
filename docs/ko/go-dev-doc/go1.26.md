Please provide the Markdown content you would like me to translate. I am ready to translate it from English to Korean while preserving all technical elements and structures.

## Go 1.26 소개 {#introduction}

최신 Go 릴리스인 버전 1.26는 [Go 1.25](/doc/go1.25) 이후 6개월 뒤인 [2026년 2월](/doc/devel/release#go1.26.0)에 출시됩니다.
변경 사항의 대부분은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언제나 그렇듯, 이번 릴리스에서도 Go 1의 호환성 약속을 유지합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

<!-- https://go.dev/issue/45624 --->

새 변수를 생성하는 내장 함수 `new`가 이제 피연산자로 표현식을 허용하여, 변수의 초기값을 지정할 수 있게 되었습니다.

이 기능은 `encoding/json`이나 프로토콜 버퍼(protocol buffers)와 같이 선택적 값(optional value)을 표현하기 위해 포인터를 사용하는 직렬화 패키지를 사용할 때 특히 유용합니다. 예를 들어, 다음과 같이 간단한 표현식으로 선택적 필드를 채울 수 있게 해줍니다.

```go
import "encoding/json"

type Person struct {
	Name string   `json:"name"`
	Age  *int     `json:"age"` // 나이를 알 경우 값 할당, 그렇지 않으면 nil
}

func personJSON(name string, born time.Time) ([]byte, error) {
	return json.Marshal(Person{
		Name: name,
		Age:  new(yearsSince(born)),
	})
}

func yearsSince(t time.Time) int {
	return int(time.Since(t).Hours() / (365.25 * 24)) // 근사치
}
```

<!-- https://go.dev/issue/75883 --->

제네릭 타입이 자신의 타입 파라미터 목록에서 자기 자신을 참조할 수 없었던 제한이 해제되었습니다.

이제 제약 대상이 되는 제네릭 타입을 참조하는 타입 제약(type constraints)을 지정하는 것이 가능해졌습니다.

예를 들어, 제네릭 타입 `Adder`는 자기 자신과 유사한 타입으로 인스턴스화될 것을 요구할 수 있습니다:

```go
type Adder[A Adder[A]] interface {
	Add(A) A
}

func algo[A Adder[A]](x, y A) A {
	return x.Add(y)
}
```

이전에는 첫 번째 줄의 `Adder`에 대한 자기 참조(self-reference)가 허용되지 않았습니다.
이번 변경 사항은 타입 제약(type constraints)을 더 강력하게 만들 뿐만 아니라, 타입 파라미터에 대한 사양 규칙을 아주 조금 더 단순화합니다.

## 도구 {#tools}

### Go 명령 {#go-command}

<!-- go.dev/issue/75432 -->
오랫동안 사용되어 온 `go fix` 명령어가 완전히 개편되어 이제 Go의 *modernizers*를 위한 공간이 되었습니다. 이 명령어는 Go 코드 베이스를 최신 관용구(idioms)와 핵심 라이브러리 API로 업데이트할 수 있는 신뢰할 수 있는 원클릭 방법을 제공합니다. 초기 modernizers 제품군에는 Go 언어와 라이브러리의 현대적인 기능들을 활용할 수 있게 해주는 수십 개의 fixers와, 사용자가 [`//go:fix inline` 지시어](https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/inline#hdr-Analyzer_inline)를 사용하여 자체적인 API 마이그레이션을 자동화할 수 있게 해주는 소스 레벨 인라이너(inliner)가 포함되어 있습니다. 이러한 fixers는 프로그램의 동작을 변경해서는 안 되므로, `go fix`에 의해 수행된 수정으로 인해 문제가 발생할 경우 [제보해 주세요](/issue/new).

새롭게 작성된 `go fix` 명령어는 `go vet`과 완전히 동일한 [Go analysis framework](https://pkg.go.dev/golang.org/x/tools/go/analysis)를 기반으로 구축되었습니다. 이는 `go vet`에서 진단 정보를 제공하는 동일한 분석기(analyzer)들을 `go fix`에서 수정 사항을 제안하고 적용하는 데 사용할 수 있음을 의미합니다. 이제 더 이상 사용되지 않는 `go fix` 명령어의 기존 픽서(fixer)들은 모두 제거되었습니다.

앞으로 게시될 두 건의 Go 블로그 포스트에서 modernizer, 인라이너(inliner), 그리고 `go fix`를 최대한 활용하는 방법에 대해 더 자세히 다룰 예정입니다.
<!-- TODO(adonovan): link to blog posts once live. -->

<!-- go.dev/issue/74748 -->
`go mod init`이 이제 새로운 `go.mod` 파일에서 더 낮은 `go` 버전을 기본값으로 설정합니다.
`1.N.X` 버전의 툴체인을 사용하여 `go mod init`을 실행하면
Go 버전 `go 1.(N-1).0`을 지정하는 `go.mod` 파일이 생성됩니다. `1.N`의 프리릴리즈(Pre-release) 버전은
`go 1.(N-2).0`을 지정하는 `go.mod` 파일을 생성합니다. 예를 들어, Go 1.26
릴리스 후보(release candidates)는 `go 1.24.0`이 포함된 `go.mod` 파일을 생성하며, Go 1.26
및 그 마이너 릴리스들은 `go 1.25.0`이 포함된 `go.mod` 파일을 생성합니다. 이는
현재 지원되는 Go 버전과 호환되는 모듈 생성을 권장하기 위함입니다. 새 모듈의 `go` 버전을
추가로 제어하려면, `go mod init` 이후에 `go get go@version`을 실행하면 됩니다.

<!-- go.dev/issue/74667 -->
`cmd/doc` 및 `go tool doc`이 삭제되었습니다. `go tool doc`의 대체제로 `go doc`을 사용할 수 있습니다. `go doc`은 동일한 플래그와 인자를 가지며 동일하게 동작합니다.

### Pprof {#pprof}

<!-- go.dev/issue/74774 -->
`-http` 플래그로 활성화되는 `pprof` 도구 웹 UI의 기본 뷰가 이제 플레임 그래프(flame graph) 뷰로 설정됩니다.
이전의 그래프 뷰는 "View -> Graph" 메뉴 또는 `/ui/graph`를 통해 이용할 수 있습니다.

## 런타임 {#runtime}

### 새로운 가비지 컬렉터

Go 1.25에서 실험적 기능으로 제공되었던 Green Tea 가비지 컬렉터가 피드백을 반영하여 이제 기본적으로 활성화되었습니다.

이 가비지 컬렉터의 설계는 더 나은 로컬리티(locality)와 CPU 확장성을 통해 작은 객체의 마킹 및 스캐닝 성능을 향상시킵니다.
벤치마크 결과는 다양하지만, 가비지 컬렉터를 많이 사용하는 실제 프로그램에서 가비지 컬렉션 오버헤드가 약 10–40% 감소할 것으로 기대합니다.
최신 amd64 기반 CPU 플랫폼(Intel Ice Lake 또는 AMD Zen 4 이상)에서 실행할 경우, 가비지 컬렉터가 가능할 때 벡터 명령어를 사용하여 작은 객체를 스캐닝하므로 가비지 컬렉션 오버헤드가 추가로 약 10% 더 개선될 것으로 예상됩니다.

새로운 가비지 컬렉터는 빌드 시 `GOEXPERIMENT=nogreenteagc`를 설정하여 비활성화할 수 있습니다.
이 옵트아웃 설정은 Go 1.27에서 제거될 예정입니다.
성능이나 동작과 관련된 어떤 이유로든 새로운 가비지 컬렉터를 비활성화하는 경우, [이슈를 제기해](/issue/new) 주시기 바랍니다.

### 더 빠른 cgo 호출

<!-- CL 646198 -->

cgo 호출의 기본 런타임 오버헤드가 약 30% 감소했습니다.

### 힙 기본 주소 무작위화 (Heap base address randomization)

<!-- CL 674835 -->

64비트 플랫폼에서 런타임이 이제 시작 시 힙 기본 주소(heap base address)를 무작위화합니다.

이는 공격자가 메모리 주소를 예측하고 cgo 사용 시 취약점을 악용하는 것을 더 어렵게 만드는 보안 강화 조치입니다.

이 기능은 빌드 시 `GOEXPERIMENT=norandomizedheapbase64`를 설정하여 비활성화할 수 있습니다.

이 제외 설정은 향후 Go 릴리스에서 제거될 예정입니다.

### 실험적인 goroutine 누수 프로파일 {#goroutineleak-profiles}

<!-- CL 688335 -->

누수된 goroutine을 보고하는 새로운 프로필 타입이 실험적 기능으로 제공됩니다.

[`runtime/pprof`](/pkg/runtime/pprof) 패키지의 `goroutineleak`라는 이름의 이 새로운 프로필 타입은 빌드 시 `GOEXPERIMENT=goroutineleakprofile`를 설정하여 활성화할 수 있습니다.

이 실험적 기능을 활성화하면 [`net/http/pprof`](/pkg/net/http/pprof) 엔드포인트인 `/debug/pprof/goroutineleak`를 통해서도 프로필을 사용할 수 있습니다.

*누수된(leaked)* 고루틴이란, 어떤 동시성 프리미티브(채널, [`sync.Mutex`](/pkg/sync#Mutex), [`sync.Cond`](/pkg/sync#Cond) 등)에서 블록되어 더 이상 해제될 가능성이 없는 고루틴을 말합니다.

런타임은 가비지 컬렉터를 사용하여 누수된 고루틴을 감지합니다. 만약 고루틴 G가 동시성 프리미티브 P에서 블록되어 있고, P가 실행 가능한 어떤 고루틴이나 그 고루틴들이 해제할 수 있는 다른 고루틴으로부터 도달 불가능한 상태라면, P는 해제될 수 없으며 따라서 고루틴 G는 결코 깨어날 수 없습니다.

모든 경우의 영구적으로 블록된 고루틴을 감지하는 것은 불가능하지만, 이 방식은 이러한 누수의 상당 부분을 감지해 냅니다.

다음 예제는 새로운 프로파일을 통해 발견할 수 있는 실제 사례의 goroutine 누수를 보여줍니다:

```go
type result struct {
	res workResult
	err error
}

func processWorkItems(ws []workItem) ([]workResult, error) {
	// 작업 항목들을 병렬로 처리하고, 결과를 ch에 집계합니다.
	ch := make(chan result)
	for _, w := range ws {
		go func() {
			res, err := processWorkItem(w)
			ch <- result{res, err}
		}()
	}

	// ch에서 결과를 수집하며, 에러가 발견되면 에러를 반환합니다.
	var results []workResult
	for range len(ws) {
		r := <-ch
		if r.err != nil {
			// 이 조기 반환(early return)은 고루틴 누수(goroutine leaks)를 유발할 수 있습니다.
			return nil, r.err
		}
		results = append(results, r.res)
	}
	return results, nil
}
```

`ch`가 버퍼링되지 않았기 때문에, 만약 `processWorkItems`가 오류로 인해 조기에 반환되면, 나머지 모든 `processWorkItem` 고루틴들은 누수(leak)됩니다. 이 일이 발생한 직후, 누수에 관여하지 않은 다른 모든 고루틴들은 `ch`에 접근할 수 없게 되며, 이에 따라 런타임이 누수된 고루틴들을 감지하고 보고할 수 있게 됩니다.

이 기법은 도달 가능성(reachability)을 기반으로 하므로, 전역 변수나 실행 가능한 고루틴(runnable goroutine)의 지역 변수를 통해 도달 가능한 동시성 프리미티브(concurrency primitives)에서 블로킹이 발생하여 생기는 누수는 런타임이 식별하지 못할 수 있습니다.

이 작업에 기여해 주신 Uber의 Vlad Saioc 님께 특별한 감사를 드립니다.
기저 이론은 [Saioc et al의 논문](https://dl.acm.org/doi/pdf/10.1145/3676641.3715990)에 자세히 설명되어 있습니다.

이 구현은 프로덕션 환경에서 사용할 준비가 되어 있으며, API에 대한 피드백(특히 새로운 프로필로 만드는 선택)을 수집하기 위한 목적으로만 실험적으로 간주됩니다. 또한, 이 기능은 실제로 사용되지 않는 한 추가적인 런타임 오버헤드가 발생하지 않도록 설계되었습니다.

사용자 여러분께서 [Go playground](/play/p/3C71z4Dpav-?v=gotip), 테스트, 지속적 통합(CI), 그리고 프로덕션 환경에서 새로운 기능을 사용해 보시기를 권장합니다. [제안 이슈](/issue/74609)를 통한 추가 피드백을 환영합니다.

Go 1.27에서 goroutine leak 프로파일을 기본적으로 활성화하는 것을 목표로 하고 있습니다.

## 컴파일러 {#compiler}

<!-- CLs 707755, 722440 -->

이제 컴파일러가 더 많은 상황에서 슬라이스의 backing store를 스택에 할당할 수 있게 되어 성능이 향상되었습니다. 만약 이 변경 사항으로 인해 문제가 발생한다면, [bisect tool](https://pkg.go.dev/golang.org/x/tools/cmd/bisect)과 `-compile=variablemake` 플래그를 사용하여 문제가 되는 할당 지점을 찾을 수 있습니다. 또한 `-gcflags=all=-d=variablemakehash=n`를 사용하여 이러한 새로운 스택 할당 기능을 모두 끌 수 있습니다.

이 최적화와 관련하여 문제를 발견하시면 [이슈를 제기](/issue/new)해 주세요.

## Linker {#linker}

64비트 ARM 기반 Windows(`windows/arm64` 포트)에서, 이제 링커가 cgo 프로그램의 내부 링킹 모드(internal linking mode)를 지원하며, 이는 `-ldflags=-linkmode=internal` 플래그로 요청할 수 있습니다.

실행 파일에 몇 가지 사소한 변경 사항이 있습니다. 이러한 변경 사항은 Go 프로그램의 실행에는 영향을 주지 않습니다. 다만, Go 실행 파일을 분석하는 프로그램에는 영향을 줄 수 있으며, 사용자 정의 링커 스크립트를 사용하여 외부 링킹 모드를 사용하는 사용자에게 영향을 줄 수 있습니다.

- `moduledata` 구조체가 이제 `.go.module`이라는 이름의 별도 섹션으로 분리되었습니다.
- 슬라이스인 `moduledata`의 `cutab` 필드가 이제 올바른 길이를 가집니다. 이전에는 길이가 4배 더 크게 설정되어 있었습니다.
- `.gopclntab` 섹션의 시작 부분에 있는 `pcHeader`가 더 이상 텍스트 섹션의 시작 지점을 기록하지 않습니다. 해당 필드는 이제 항상 0으로 설정됩니다.
- 이러한 `pcHeader` 변경은 `.gopclntab` 섹션에 더 이상 재배치(relocation) 정보가 포함되지 않도록 하기 위해 이루어졌습니다. relro를 지원하는 플랫폼에서 해당 섹션은 relro 세그먼트에서 rodata 세그먼트로 이동했습니다.
- funcdata 심볼과 findfunctab이 `.rodata` 섹션에서 `.gopclntab` 섹션으로 이동했습니다.
- `.gosymtab` 섹션이 제거되었습니다. 이 섹션은 이전까지 항상 존재했지만 비어 있었습니다.
- 내부 링크(internal linking)를 사용할 때, ELF 섹션들이 이제 주소순으로 정렬되어 섹션 헤더 목록에 나타납니다. 이전의 순서는 다소 예측 불가능했습니다.

여기서 섹션 이름에 대한 참조는 Linux 및 기타 시스템에서 볼 수 있는 ELF 이름을 사용합니다. Darwin에서 볼 수 있는 Mach-O 이름은 이중 언더스코어(`__`)로 시작하며 점(`.`)을 포함하지 않습니다.

## Bootstrap {#bootstrap}

<!-- go.dev/issue/69315 -->
[Go 1.24 릴리스 노트](/doc/go1.24#bootstrap)에 언급된 바와 같이, 이제 Go 1.26의 부트스트랩(bootstrap)을 위해 Go 1.24.6 이상의 버전이 필요합니다.
Go 1.28은 부트스트랩을 위해 Go 1.26의 마이너 릴리스 이상의 버전이 필요할 것으로 예상됩니다.

## 표준 라이브러리 {#library}

### 새로운 crypto/hpke 패키지

새로운 [`crypto/hpke`](/pkg/crypto/hpke) 패키지는 포스트 퀀텀(post-quantum) 하이브리드 KEM 지원을 포함하여 [RFC 9180](https://rfc-editor.org/rfc/rfc9180.html)에 정의된 하이브리드 공개 키 암호화(Hybrid Public Key Encryption, HPKE)를 구현합니다.

### 새로운 실험적 simd/archsimd 패키지 {#simd}

Go 1.26에서는 새로운 실험적 [`simd/archsimd`](/pkg/simd/archsimd/) 패키지가 도입되었으며, 빌드 시 환경 변수 `GOEXPERIMENT=simd`를 설정하여 활성화할 수 있습니다.
이 패키지는 아키텍처별 SIMD 연산에 대한 액세스를 제공합니다.
현재 amd64 아키텍처에서 사용할 수 있으며, [`Int8x16`](/pkg/simd/archsimd#Int8x16) 및 [`Float64x8`](/pkg/simd/archsimd#Float64x8)와 같은 128비트, 256비트, 512비트 벡터 타입과 [`Int8x16.Add`](/pkg/simd/archsimd#Int8x16.Add)와 같은 연산을 지원합니다.
해당 API는 아직 안정적이지 않은 것으로 간주됩니다.

향후 버전에서 다른 아키텍처에 대한 지원을 제공할 예정이지만, 본 API는 의도적으로 아키텍처 전용으로 설계되었으며 따라서 이식성이 없습니다.
또한, 향후에 수준 높은 이식성 있는 SIMD 패키지를 개발할 계획입니다.

더 자세한 내용은 [패키지 문서](/pkg/simd/archsimd)와 [제안 이슈](/issue/73787)를 참조하세요.

### 새로운 실험적 runtime/secret 패키지

<!-- https://go.dev/issue/21865 --->

새로운 [`runtime/secret`](/pkg/runtime/secret) 패키지를 실험적 기능으로 사용할 수 있으며, 빌드 시 환경 변수 `GOEXPERIMENT=runtimesecret`를 설정하여 활성화할 수 있습니다.
이 패키지는 일반적으로 암호화 성격의 비밀 정보를 다루는 코드에서 레지스터, 스택, 새로운 힙 할당과 같이 사용된 임시 데이터를 안전하게 삭제하는 기능을 제공합니다.
이 패키지는 [forward secrecy](https://en.wikipedia.org/wiki/Forward_secrecy)(전방향 안전성)를 더 쉽게 보장하기 위해 설계되었습니다.
현재 Linux의 amd64 및 arm64 아키텍처를 지원합니다.

### 라이브러리의 소소한 변경 사항 {#minor_library_changes}

#### [`bytes`](/pkg/bytes/)

새로운 [`Buffer.Peek`](/pkg/bytes#Buffer.Peek) 메서드는 버퍼의 포인터를 이동시키지 않고 다음 n바이트를 반환합니다.

#### [`crypto`](/pkg/crypto/)

새로운 [`Encapsulator`](/pkg/crypto#Encapsulator) 및 [`Decapsulator`](/pkg/crypto#Decapsulator) 인터페이스를 통해 추상화된 KEM 캡슐화(encapsulation) 또는 역캡슐화(decapsulation) 키를 수락할 수 있습니다.

#### [`crypto/dsa`](/pkg/crypto/dsa/)

[`GenerateKey`](/pkg/crypto/dsa#GenerateKey)의 random 파라미터가 이제 무시됩니다.
대신, 이제 항상 암호학적으로 안전한 무작위 바이트 소스를 사용합니다.
결정론적 테스트(deterministic testing)를 위해서는 새로운 [`testing/cryptotest.SetGlobalRandom`](/pkg/testing/cryptotest#SetGlobalRandom) 함수를 사용하십시오.
새로운 GODEBUG 설정인 `cryptocustomrand=1`을 통해 일시적으로 이전 동작을 복구할 수 있습니다.

#### [`crypto/ecdh`](/pkg/crypto/ecdh/)

[`Curve.GenerateKey`](/pkg/crypto/ecdh#Curve.GenerateKey)의 random 매개변수는 이제 무시됩니다.
대신, 이제 항상 암호학적으로 안전한 무작위 바이트 소스를 사용합니다.
결정론적 테스트를 위해서는 새로운 [`testing/cryptotest.SetGlobalRandom`](/pkg/testing/cryptotest#SetGlobalRandom) 함수를 사용하십시오.
새로운 GODEBUG 설정인 `cryptocustomrand=1`을 통해 일시적으로 이전 동작을 복원할 수 있습니다.

[`PrivateKey`](/pkg/crypto/ecdh#PrivateKey)에 의해 구현된 새로운 [`KeyExchanger`](/pkg/crypto/ecdh#KeyExchanger) 인터페이스를 통해, 하드웨어로 구현된 키와 같은 추상적인 ECDH 개인 키를 수락하는 것이 가능해졌습니다.

#### [`crypto/ecdsa`](/pkg/crypto/ecdsa/)

[`PublicKey`](/pkg/crypto/ecdsa#PublicKey) 및 [`PrivateKey`](/pkg/crypto/ecdsa#PrivateKey)의 `big.Int` 필드는 이제 deprecated 되었습니다.

[`GenerateKey`](/pkg/crypto/ecdsa#GenerateKey), [`SignASN1`](/pkg/crypto/ecdsa#SignASN1), [`Sign`](/pkg/crypto/ecdsa#Sign), 그리고 [`PrivateKey.Sign`](/pkg/crypto/ecdsa#PrivateKey.Sign)의 `random` 파라미터가 이제 무시됩니다.
대신, 이제 항상 암호학적으로 안전한 난수 바이트 소스를 사용합니다.
결정론적인 테스트를 위해서는 새로운 [`testing/cryptotest.SetGlobalRandom`](/pkg/testing/cryptotest#SetGlobalRandom) 함수를 사용하십시오.
새로운 GODEBUG 설정인 `cryptocustomrand=1`을 통해 일시적으로 이전 동작을 복구할 수 있습니다.

#### [`crypto/ed25519`](/pkg/crypto/ed25519/)

[`GenerateKey`](/pkg/crypto/ed25519#GenerateKey)에 전달되는 `random` 파라미터가 `nil`인 경우, 이제 `GenerateKey`는 (재정의되었을 가능성이 있는) [`crypto/rand.Reader`](/pkg/crypto/rand#Reader) 대신 항상 안전한 암호학적 난수 바이트 소스를 사용합니다. 새로운 `GODEBUG` 설정인 `cryptocustomrand=1`을 통해 일시적으로 이전 동작으로 복구할 수 있습니다.

#### [`crypto/fips140`](/pkg/crypto/fips140/)

[FIPS 140-3 Go Cryptographic Module](/doc/security/fips140) v1.26.0에는 이번 릴리스까지 `crypto/internal/fips140/...` 패키지에 적용된 변경 사항이 포함되어 있으며, 이제 GOFIPS140으로 선택할 수 있습니다.

새로운 [`WithoutEnforcement`](/pkg/crypto/fips140#WithoutEnforcement) 및 [`Enforced`](/pkg/crypto/fips140#Enforced) 함수를 통해 이제 `GODEBUG=fips140=only` 모드로 실행하면서 엄격한 FIPS 140-3 검사를 선택적으로 비활성화할 수 있습니다.

[`Version`](/pkg/crypto/fips140#Version)은 GOFIPS140과 함께 frozen module을 대상으로 빌드할 때, 확인된 FIPS 140-3 Go Cryptographic Module 버전을 반환합니다.

#### [`crypto/mlkem`](/pkg/crypto/mlkem/)

새로운 [`DecapsulationKey768.Encapsulator`](/pkg/crypto/mlkem#DecapsulationKey768.Encapsulator) 및
[`DecapsulationKey1024.Encapsulator`](/pkg/crypto/mlkem#DecapsulationKey1024.Encapsulator) 메서드는 새로운
[`crypto.Decapsulator`](/pkg/crypto#Decapsulator) 인터페이스를 구현합니다.

캡슐화(Encapsulation) 및 역캡슐화(decapsultion) 작업 속도가 약 18% 향상되었습니다.

#### [`crypto/mlkem/mlkemtest`](/pkg/crypto/mlkem/mlkemtest/)

새로운 [`crypto/mlkem/mlkemtest`](/pkg/crypto/mlkem/mlkemtest) 패키지는 알려진 정답 테스트(known-answer tests)에서 사용할 수 있도록, 결정론적(derandomized) ML-KEM 캡슐화를 구현한 [`Encapsulate768`](/pkg/crypto/mlkem/mlkemtest#Encapsulate768) 및 [`Encapsulate1024`](/pkg/crypto/mlkem/mlkemtest#Encapsulate1024) 함수를 제공합니다.

#### [`crypto/rand`](/pkg/crypto/rand/)

[`Prime`](/pkg/crypto/rand#Prime)의 random 파라미터가 이제 무시됩니다.
대신, 이제 항상 암호학적으로 안전한 난수 바이트 소스를 사용합니다.
결정론적인 테스트를 위해서는 새로운 [`testing/cryptotest.SetGlobalRandom`](/pkg/testing/cryptotest#SetGlobalRandom) 함수를 사용하세요.
새로운 GODEBUG 설정인 `cryptocustomrand=1`을 통해 일시적으로 이전 동작을 복구할 수 있습니다.

#### [`crypto/rsa`](/pkg/crypto/rsa/)

새로운 [`EncryptOAEPWithOptions`](/pkg/crypto/rsa#EncryptOAEPWithOptions) 함수를 통해 OAEP 패딩과 MGF1 마스크 생성에 서로 다른 해시 함수를 지정할 수 있습니다.

[`GenerateKey`](/pkg/crypto/rsa#GenerateKey), [`GenerateMultiPrimeKey`](/pkg/crypto/rsa#GenerateMultiPrimeKey), 그리고 [`EncryptPKCS1v15`](/pkg/crypto/rsa#EncryptPKCS1v15)의 `random` 파라미터가 이제 무시됩니다.
대신, 이제 항상 암호학적으로 안전한 난수 바이트 소스를 사용합니다.
결정론적 테스트(deterministic testing)를 위해서는 새로운 [`testing/cryptotest.SetGlobalRandom`](/pkg/testing/cryptotest#SetGlobalRandom) 함수를 사용하십시오.
새로운 GODEBUG 설정인 `cryptocustomrand=1`을 통해 일시적으로 이전 동작을 복구할 수 있습니다.

[`PrivateKey`](/pkg/crypto/rsa#PrivateKey) 필드가 [`PrivateKey.Precompute`](/pkg/crypto/rsa#PrivateKey.Precompute)를 호출한 후 수정되면, 이제 [`PrivateKey.Validate`](/pkg/crypto/rsa#PrivateKey.Validate)가 실패합니다.

[`PrivateKey.D`](/pkg/crypto/rsa#PrivateKey.D)가 사용되지 않더라도 이제 사전 계산된 값과의 일관성을 확인합니다.

안전하지 않은 PKCS #1 v1.5 암호화 패딩([`EncryptPKCS1v15`](/pkg/crypto/rsa#EncryptPKCS1v15), [`DecryptPKCS1v15`](/pkg/crypto/rsa#DecryptPKCS1v15), 및 [`DecryptPKCS1v15SessionKey`](/pkg/crypto/rsa#DecryptPKCS1v15SessionKey)에 의해 구현됨)는 이제 deprecated 되었습니다.

#### [`crypto/sha3`](/pkg/crypto/sha3/)

[`SHA3`](/pkg/crypto/sha3#SHA3)의 제로 값(zero value)은 이제 사용 가능한 SHA3-256 인스턴스이며, [`SHAKE`](/pkg/crypto/sha3#SHAKE)의 제로 값은 이제 사용 가능한 SHAKE256 인스턴스입니다.

#### [`crypto/subtle`](/pkg/crypto/subtle)

[`WithDataIndependentTiming`](/pkg/crypto/subtle#WithDataIndependentTiming) 함수는 더 이상 전달된 함수를 실행하는 동안 호출한 goroutine을 OS 스레드에 고정(lock)하지 않습니다. 또한, 전달된 함수가 실행되는 동안 생성된 모든 goroutine과 그 하위 goroutine들은 수명 주기 동안 `WithDataIndependentTiming`의 속성을 상속받습니다. 이 변경 사항은 cgo에도 다음과 같은 영향을 미칩니다:

- `WithDataIndependentTiming`에 전달된 함수 내부에서, 또는 해당 함수 및 그 하위 함수에서 생성된 goroutine 내에서 cgo를 통해 호출되는 모든 C 코드는 호출되는 동안 데이터 독립적 타이밍(data independent timing)이 활성화됩니다. 만약 C 코드에서 데이터 독립적 타이밍을 비활성화하더라도, Go로 돌아올 때 다시 활성화됩니다.
- `WithDataIndependentTiming`에 전달된 함수나 다른 곳에서 cgo를 통해 호출된 C 코드가 데이터 독립적 타이밍을 활성화하거나 비활성화한 경우, Go를 호출하면 해당 상태가 호출 기간 동안 유지됩니다.

#### [`crypto/tls`](/pkg/crypto/tls/)

하이브리드 [`SecP256r1MLKEM768`](/pkg/crypto/tls#SecP256r1MLKEM768) 및 [`SecP384r1MLKEM1024`](/pkg/crypto/tls#SecP384r1MLKEM1024) 양자 내성 키 교환이 이제 기본적으로 활성화됩니다. 이는 [`Config.CurvePreferences`](/pkg/crypto/tls#Config.CurvePreferences)를 설정하거나 `tlssecpmlkem=0` GODEBUG 설정을 통해 비활성화할 수 있습니다.

새로운 [`ClientHelloInfo.HelloRetryRequest`](/pkg/crypto/tls#ClientHelloInfo.HelloRetryRequest) 필드는 ClientHello가 HelloRetryRequest 메시지에 대한 응답으로 전송되었는지 여부를 나타냅니다. 새로운 [`ConnectionState.HelloRetryRequest`](/pkg/crypto/tls#ConnectionState.HelloRetryRequest) 필드는 연결 역할에 따라 서버가 HelloRetryRequest를 보냈는지, 또는 클라이언트가 HelloRetryRequest를 받았는지를 나타냅니다.

QUIC 구현에서 사용하는 [`QUICConn`](/pkg/crypto/tls#QUICConn) 타입에는 TLS 핸드셰이크 오류를 보고하기 위한 새로운 이벤트가 포함되어 있습니다.

[`Certificate.PrivateKey`](/pkg/crypto/tls#Certificate.PrivateKey)가 [`crypto.MessageSigner`](/pkg/crypto#MessageSigner)를 구현하는 경우, TLS 1.2 및 이후 버전에서는 Sign 대신 SignMessage 메서드가 사용됩니다.

[Go 1.22](/doc/godebug#go-122) 및 [Go 1.23](/doc/godebug#go-123)에서 도입된 다음 GODEBUG 설정들은 다음 Go 메이저 릴리스에서 제거될 예정입니다.
Go 1.27부터는 GODEBUG 설정이나 go.mod 언어 버전에 관계없이 새로운 동작이 적용됩니다.

- `tlsunsafeekm`: [`ConnectionState.ExportKeyingMaterial`](/pkg/crypto/tls#ConnectionState.ExportKeyingMaterial)은 TLS 1.3 또는 Extended Master Secret을 요구하게 됩니다.
- `tlsrsakex`: ECDH가 없는 레거시 RSA 전용 키 교환이 기본적으로 활성화되지 않습니다.
- `tls10server`: 클라이언트와 서버 모두의 기본 최소 TLS 버전이 TLS 1.2로 변경됩니다.
- `tls3des`: 기본 사이퍼 스위트(cipher suites)에 3DES가 포함되지 않습니다.
- `x509keypairleaf`: [`X509KeyPair`](/pkg/crypto/tls#X509KeyPair) 및 [`LoadX509KeyPair`](/pkg/crypto/tls#LoadX509KeyPair)가 항상 [`Certificate.Leaf`](/pkg/crypto/tls#Certificate.Leaf) 필드를 채우게 됩니다.

#### [`crypto/x509`](/pkg/crypto/x509/)

[`ExtKeyUsage`](/pkg/crypto/x509#ExtKeyUsage) 및 [`KeyUsage`](/pkg/crypto/x509#KeyUsage) 타입에 이제 RFC 5280 및 기타 레지스트리에 정의된 해당 OID 이름을 반환하는 `String` 메서드가 추가되었습니다.

[`ExtKeyUsage`](/pkg/crypto/x509#ExtKeyUsage) 타입에 EKU에 해당하는 OID를 반환하는 `OID` 메서드가 추가되었습니다.

새로운 [`OIDFromASN1OID`](/pkg/crypto/x509#OIDFromASN1OID) 함수를 통해 [`encoding/asn1.ObjectIdentifier`](/pkg/encoding/asn1#ObjectIdentifier)를 [`OID`](/pkg/crypto/x509#OID)로 변환할 수 있습니다.

#### [`debug/elf`](/pkg/debug/elf/)

LoongArch 시스템에서 사용할 수 있도록 [LoongArch ELF psABI v20250521](https://github.com/loongson/la-abi-specs/blob/v2.40/laelf.adoc) (글로벌 버전 v2.40)의 추가 `R_LARCH_*` 상수들이 정의되었습니다.

#### [`errors`](/pkg/errors/)

새로운 [`AsType`](/pkg/errors#AsType) 함수는 [`As`](/pkg/errors#As)의 제네릭 버전입니다. 이 함수는 타입 안전하며, 더 빠르고, 대부분의 경우 사용하기 더 쉽습니다.

#### [`fmt`](/pkg/fmt/)

<!-- go.dev/cl/708836 -->
포맷팅되지 않은 문자열의 경우, `fmt.Errorf("x")`는 이제 메모리 할당을 적게 하며 일반적으로 `errors.New("x")`의 할당량과 일치합니다.

#### [`go/ast`](/pkg/go/ast/)

새로운 [`ParseDirective`](/pkg/go/ast#ParseDirective) 함수는 `//go:generate`와 같은 [디렉티브 주석](/doc/comment#Syntax)을 파싱합니다. 소스 코드 도구들은 자체적인 디렉티브 주석을 지원할 수 있으며, 이 새로운 API는 도구들이 관례적인 구문을 구현하는 데 도움을 줄 것입니다.

<!-- go.dev/issue/76395 -->
새로운 [`BasicLit.ValueEnd`](/pkg/go/ast#BasicLit.ValueEnd) 필드는 리터럴의 정확한 종료 위치를 기록하여, 이제 [`BasicLit.End`](/pkg/go/ast#BasicLit.End) 메서드가 항상 정확한 값을 반환할 수 있게 합니다. (이전에는 캐리지 리턴 제거로 인해 Windows 소스 파일의 다중 행 raw string 리터럴에서 부정확한 휴리스틱을 사용하여 계산되었습니다.)

파서가 생성한 `BasicLit`의 `ValuePos` 필드를 업데이트하는 프로그램은, 포맷팅된 출력 결과의 미세한 차이를 방지하기 위해 `ValueEnd` 필드 또한 업데이트하거나 비워야 할 수도 있습니다.

#### [`go/token`](/pkg/go/token/)

새로운 [`File.End`](/pkg/go/token#File.End) 편의 메서드는 파일의 끝 위치를 반환합니다.

#### [`go/types`](/pkg/go/types/)

[Go 1.22](/doc/godebug#go-122)에서 도입된 `gotypesalias` GODEBUG 설정은 다음 Go 메이저 릴리스에서 제거될 예정입니다.
Go 1.27부터는 GODEBUG 설정이나 go.mod 언어 버전과 관계없이, [`go/types`](/pkg/go/types) 패키지가 [타입 별칭](/ref/spec#Type_declarations)의 표현으로 항상 [Alias 타입](/pkg/go/types#Alias)을 생성하게 됩니다.

#### [`image/jpeg`](/pkg/image/jpeg/)

JPEG 인코더와 디코더가 더 빠르고 정확한 새로운 구현체로 교체되었습니다.
인코더 또는 디코더로부터 비트 단위로 일치하는 특정 출력을 기대하는 코드는 업데이트가 필요할 수 있습니다.

#### [`io`](/pkg/io/)

<!-- go.dev/cl/722500 -->
[`ReadAll`](/pkg/io#ReadAll)이 이제 중간 메모리 할당량을 줄이고 최소 크기의 최종 슬라이스를 반환합니다. 일반적으로 총 메모리 할당량은 약 절반으로 줄어들며 속도는 약 두 배 정도 빨라졌으며, 입력값이 클수록 더 많은 이점이 있습니다.

#### [`log/slog`](/pkg/log/slog/)

[`NewMultiHandler`](/pkg/log/slog#NewMultiHandler) 함수는 제공된 모든 Handler를 호출하는 [`MultiHandler`](/pkg/log/slog#MultiHandler)를 생성합니다.
이 핸들러의 `Enabled` 메서드는 핸들러들 중 어느 하나의 `Enabled` 메서드라도 true를 반환하는지 여부를 보고합니다.
`Handle`, `WithAttrs` 및 `WithGroup` 메서드는 활성화된 각 핸들러의 해당 메서드를 호출합니다.

#### [`net`](/pkg/net/)

새로운 [`Dialer`](/pkg/net/#Dialer) 메서드인
[`DialIP`](/pkg/net/#Dialer.DialIP),
[`DialTCP`](/pkg/net/#Dialer.DialTCP),
[`DialUDP`](/pkg/net/#Dialer.DialUDP), 그리고
[`DialUnix`](/pkg/net/#Dialer.DialUnix)는
컨텍스트(context) 값과 함께 특정 네트워크 유형으로 다이얼링하는 것을 가능하게 합니다.

#### [`net/http`](/pkg/net/http/)

새로운 [`HTTP2Config.StrictMaxConcurrentRequests`](/pkg/net/http#HTTP2Config.StrictMaxConcurrentRequests) 필드는 기존 HTTP/2 연결이 스트림 제한을 초과했을 때 새로운 연결을 열어야 하는지 여부를 제어합니다.

새로운 [`Transport.NewClientConn`](/pkg/net/http#Transport.NewClientConn) 메서드는 HTTP 서버로의 클라이언트 연결을 반환합니다.
대부분의 사용자는 연결 풀을 관리하는 [`Transport.RoundTrip`](/pkg/net/http#Transport.RoundTrip)을 계속 사용하여 요청을 보내야 합니다.
`NewClientConn`은 자체적인 연결 관리를 구현해야 하는 사용자에게 유용합니다.

[`Client`](/pkg/net/http#Client)는 이제 가능할 경우 [`Request.Host`](/pkg/net/http#Request.Host)와 일치하는 호스트 부분을 가진 URL 범위의 쿠키를 사용하고 설정합니다.
이전에는 항상 연결 주소(connection address)의 호스트가 사용되었습니다.
[`ServeMux`](/pkg/net/http#ServeMux)의 트레일링 슬래시(trailing slash) 리다이렉트는 이제 301(Moved Permanently) 대신 HTTP 상태 코드 307(Temporary Redirect)을 사용합니다.

#### [`net/http/httptest`](/pkg/net/http/httptest/)

[`Server.Client`](/pkg/net/http/httptest#Server.Client)에 의해 반환된 HTTP 클라이언트는 이제 `example.com` 및 모든 서브도메인에 대한 요청을 테스트 중인 서버로 리다이렉트합니다.

#### [`net/http/httputil`](/pkg/net/http/httputil/)

[`ReverseProxy.Director`](/pkg/net/http/httputil#ReverseProxy.Director) 설정 필드는 [`ReverseProxy.Rewrite`](/pkg/net/http/httputil#ReverseProxy.Rewrite)로 대체되어 더 이상 권장되지 않습니다(deprecated).

악의적인 클라이언트는 `Director` 함수에 의해 추가된 헤더를 홉 바이 홉(hop-by-hop)으로 지정함으로써 해당 헤더를 제거할 수 있습니다. `Director` API의 범위 내에서는 이 문제를 해결할 방법이 없기 때문에, Go 1.20에서 새로운 `Rewrite` 훅을 추가했습니다. `Rewrite` 훅은 프록시가 수신한 수정되지 않은 인바운드 요청과 프록시가 전송할 아웃바운드 요청을 모두 제공합니다.

`Director` 훅은 근본적으로 안전하지 않기 때문에, 이제 이를 deprecated(사용 중단 예정) 처리합니다.

#### [`net/netip`](/pkg/net/netip/)

새로운 [`Prefix.Compare`](/pkg/net/netip#Prefix.Compare) 메서드는 두 개의 prefix를 비교합니다.

#### [`net/url`](/pkg/net/url/)

[`Parse`](/pkg/net/url#Parse)는 이제 `http://::1/` 또는 `http://localhost:80:80/`와 같이 호스트 하위 컴포넌트에 콜론이 포함된 잘못된 형식의 URL을 거부합니다.
`http://[::1]/`와 같이 대괄호로 묶인 IPv6 주소가 포함된 URL은 여전히 허용됩니다.
새로운 GODEBUG 설정인 `urlstrictcolons=0`을 통해 이전 동작으로 복구할 수 있습니다.

#### [`os`](/pkg/os/)

새로운 [`Process.WithHandle`](/pkg/os#Process.WithHandle) 메서드는 지원되는 플랫폼(Linux 5.4 이상에서의 pidfd, Windows에서의 Handle)에서 내부 프로세스 핸들에 대한 액세스를 제공합니다.

Windows에서 [`OpenFile`](/pkg/os#OpenFile)의 `flag` 매개변수는 이제 파일 또는 장치 캐싱 동작, 액세스 모드 및 기타 특수 목적 플래그를 제어하기 위해 `FILE_FLAG_OVERLAPPED` 및 `FILE_FLAG_SEQUENTIAL_SCAN`과 같은 Windows 전용 파일 플래그의 모든 조합을 포함할 수 있습니다.

#### [`os/signal`](/pkg/os/signal/)

[`NotifyContext`](/pkg/os/signal#NotifyContext)는 이제 [`context.CancelCauseFunc`](/pkg/context#CancelCauseFunc)와 어떤 시그널을 수신했는지 나타내는 에러를 사용하여 반환된 컨텍스트를 취소합니다.

#### [`reflect`](/pkg/reflect/)

새로운 메서드 [`Type.Fields`](/pkg/reflect#Type.Fields),
[`Type.Methods`](/pkg/reflect#Type.Methods),
[`Type.Ins`](/pkg/reflect#Type.Ins)
및 [`Type.Outs`](/pkg/reflect#Type.Outs)는
각각 타입의 필드(struct 타입의 경우), 메서드,
입력 및 출력 매개변수(함수 타입의 경우)에 대한 반복자(iterator)를 반환합니다.

마찬가지로, 새로운 메서드 [`Value.Fields`](/pkg/reflect#Value.Fields)와 [`Value.Methods`](/pkg/reflect#Value.Methods)는 각각 값의 필드 또는 메서드에 대한 반복자(iterator)를 반환합니다.
각 반복은 필드 또는 메서드의 타입 정보([`StructField`](/pkg/reflect#StructField) 또는 [`Method`](/pkg/reflect#Method))와 함께 해당 필드 또는 메서드의 [`Value`](/pkg/reflect#Value)를 제공합니다.

#### [`runtime/metrics`](/pkg/runtime/metrics/)

여러 새로운 스케줄러 메트릭이 추가되었습니다. 여기에는 `/sched/goroutines` 접두사 아래의 다양한 상태(waiting, runnable 등)에 있는 goroutine 수, `/sched/threads:threads`를 통한 런타임이 인지하는 OS 스레드 수, 그리고 `/sched/goroutines-created:goroutines`를 통한 프로그램에 의해 생성된 총 goroutine 수가 포함됩니다.

#### [`testing`](/pkg/testing/)

새로운 메서드 [`T.ArtifactDir`](/pkg/testing#T.ArtifactDir), [`B.ArtifactDir`](/pkg/testing#B.ArtifactDir), [`F.ArtifactDir`](/pkg/testing#F.ArtifactDir)는 테스트 출력 파일(아티팩트)을 작성할 디렉터리를 반환합니다.

`go test`에 `-artifacts` 플래그가 제공되면, 이 디렉토리는 출력 디렉토리(`-outputdir`로 지정하거나 기본적으로 현재 디렉토리) 아래에 위치하게 됩니다. 그렇지 않으면 아티팩트는 테스트 완료 후 삭제되는 임시 디렉토리에 저장됩니다.

`-artifacts`가 제공되었을 때 `ArtifactDir`에 대한 첫 번째 호출은 디렉터리 위치를 테스트 로그에 기록합니다.

예를 들어, `TestArtifacts`라는 이름의 테스트에서
`t.ArtifactDir()`은 다음과 같이 출력합니다:

```
=== ARTIFACTS TestArtifacts /path/to/artifact/dir
```

<!-- go.dev/issue/73137 -->

[`B.Loop`](/pkg/testing#B.Loop) 메서드가 더 이상 루프 본문 내의 인라이닝(inlining)을 방지하지 않으며, 이는 예상치 못한 할당과 벤치마크 속도 저하로 이어질 수 있었습니다. 이번 수정으로 모든 벤치마크를 기존의 [`B.N`](/pkg/testing#B) 스타일에서 새로운 `B.Loop` 스타일로 부작용 없이 전환할 수 있을 것으로 기대합니다. `for b.Loop() { ... }` 루프 본문 내에서 함수 호출 매개변수, 결과 및 할당된 변수들은 여전히 유지되어, 컴파일러가 벤치마크의 전체 부분을 최적화하여 제거하는 것을 방지합니다.

#### [`testing/cryptotest`](/pkg/testing/cryptotest/)

새로운 [`SetGlobalRandom`](/pkg/testing/cryptotest#SetGlobalRandom) 함수는 테스트가 진행되는 동안 전역적이고 결정론적인 암호화 난수 생성원을 설정합니다. 이는 `crypto/rand`와 `crypto/...` 패키지 내의 모든 암시적 암호화 난수 생성원에 영향을 줍니다.

#### [`time`](/pkg/time/)

[Go 1.23](/doc/godebug#go-123)에서 도입된 `asynctimerchan` GODEBUG 설정은 다음 주요 Go 릴리스에서 제거될 예정입니다.
Go 1.27부터 [`time`](/pkg/time) 패키지는 GODEBUG 설정이나 go.mod 언어 버전과 관계없이 타이머에 항상 버퍼가 없는(동기식) 채널을 사용합니다.

## 포트 {#ports}

### Darwin

<!-- go.dev/issue/75836 -->

Go 1.26은 macOS 12 Monterey에서 실행되는 마지막 릴리스입니다. Go 1.27부터는 macOS 13 Ventura 또는 그 이후 버전이 필요합니다.

### FreeBSD

<!-- go.dev/issue/76475 -->

freebsd/riscv64 포트(`GOOS=freebsd GOARCH=riscv64`)가 [broken](/wiki/PortingPolicy#broken-ports)으로 표시되었습니다.
자세한 내용은 [issue 76475](/issue/76475)를 참조하십시오.

### Windows

<!-- go.dev/issue/71671 -->

Go 1.25 릴리스 노트에서 [공지](/doc/go1.25#windows)한 바와 같이, [정상적으로 작동하지 않던](/doc/go1.24#windows) 32비트 windows/arm 포트(`GOOS=windows` `GOARCH=arm`)가 제거되었습니다.

### PowerPC

<!-- go.dev/issue/76244 -->

Go 1.26은 Linux의 big-endian 64비트 PowerPC 포트(`GOOS=linux` `GOARCH=ppc64`)에서 ELFv1 ABI를 지원하는 마지막 릴리스입니다.
Go 1.27부터는 ELFv2 ABI로 전환될 예정입니다.
해당 포트는 현재 다른 ELF 객체와의 링크를 지원하지 않으므로, 이 변경 사항이 사용자에게 영향을 주지 않고 투명하게 적용될 것으로 예상합니다.

### RISC-V

<!-- CL 690497 -->

`linux/riscv64` 포트가 이제 race detector를 지원합니다.

### S390X

<!-- CL 719482 -->

`s390x` 포트가 이제 레지스터를 사용하여 함수 인자와 결과값을 전달하는 기능을 지원합니다.

### WebAssembly {#wasm}

<!-- CL 707855 -->

이제 컴파일러는 부호 확장(sign extension) 및 트랩이 발생하지 않는 부동 소수점-정수 변환(non-trapping floating-point to integer conversion) 명령어를 무조건적으로 사용합니다.
이러한 기능들은 최소 Wasm 2.0부터 표준화되었습니다.
이에 따라 관련 `GOWASM` 설정인 `signext`와 `satconv`는 이제 무시됩니다.

<!-- CL 683296 -->

WebAssembly 애플리케이션의 경우, 이제 런타임이 힙 메모리 청크를 훨씬 더 작은 증분 단위로 관리합니다. 이로 인해 힙 크기가 약 16 MiB 미만인 애플리케이션의 메모리 사용량이 크게 감소했습니다.
