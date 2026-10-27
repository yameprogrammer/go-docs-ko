## Go 1 소개 {#introduction}

Go 버전 1(줄여서 Go 1)은 신뢰할 수 있는 제품, 프로젝트 및 출판물을 만들기 위한 안정적인 기반을 제공하는 언어와 핵심 라이브러리 집합을 정의합니다.

Go 1의 핵심 동기는 사용자들을 위한 안정성입니다. 사용자들은 Go 프로그램을 작성했을 때, Google App Engine과 같은 프로덕션 환경을 포함하여 수년의 시간 규모 내에서도 변경 없이 계속해서 컴파일되고 실행될 것이라고 기대할 수 있어야 합니다. 마찬가지로, 사람들은 Go에 관한 책을 쓰고, 그 책이 어떤 버전의 Go를 설명하고 있는지 명시할 수 있어야 하며, 그 버전 번호가 훨씬 나중에도 여전히 의미가 있어야 합니다.

Go 1에서 컴파일되는 코드는 몇 가지 예외를 제외하고, Go 버전 1.1, 1.2와 같은 업데이트 및 버그 수정 버전이 출시되더라도 해당 버전의 수명 주기 동안 계속해서 컴파일되고 실행되어야 합니다. 치명적인 수정 사항을 제외하고, Go 1의 후속 릴리스를 위해 언어 및 라이브러리에 적용된 변경 사항은 기능을 추가할 수는 있지만 기존 Go 1 프로그램의 동작을 깨뜨리지 않습니다.
[Go 1 호환성 문서](go1compat.html)에서 호환성 가이드라인에 대해 더 자세히 설명합니다.

Go 1은 언어를 완전히 재설계한 것이 아니라, 오늘날 사용되는 방식 그대로의 Go를 표현한 것입니다. 새로운 기능을 설계하는 대신 문제점과 불일치 사항을 해결하고 이식성을 개선하는 데 집중했습니다. Go 언어와 패키지에는 오랫동안 고려하고 프로토타입을 만들었지만, 변경 사항이 크고 하위 호환성이 깨진다는 이유로 출시하지 않았던 내용들이 다수 있습니다. Go 1은 이러한 변경 사항들을 반영할 기회였으며, 이는 장기적으로 도움이 되지만 동시에 오래된 프로그램들과의 호환성 문제를 야기합니다. 다행히 `go` `fix` 도구를 사용하면 프로그램을 Go 1 표준으로 업데이트하는 데 필요한 작업의 상당 부분을 자동화할 수 있습니다.

이 문서는 기존 코드를 업데이트하는 프로그래머에게 영향을 미칠 Go 1의 주요 변경 사항을 설명합니다. 기준점은 이전 릴리스인 r60(r60.3으로 태그됨)입니다. 또한 r60 코드를 Go 1에서 실행할 수 있도록 업데이트하는 방법도 설명합니다.

## 언어 변경 사항 {#language}

### Append {#append}

`append` 미리 선언된 가변 인자 함수를 사용하면 슬라이스 끝에 요소를 추가하여 크기를 쉽게 늘릴 수 있습니다.
일반적인 사용 사례는 출력을 생성할 때 바이트 슬라이스의 끝에 바이트를 추가하는 것입니다.
하지만 `append`는 또 다른 흔한 사례인 `[]byte`에 문자열을 추가하는 방법을 제공하지 않았습니다.

{{code "/doc/progs/go1.go" `/greeting := ..byte/` `/append.*hello/`}}

`copy`의 유사한 속성과 마찬가지로, Go 1에서는 문자열을 바이트 슬라이스에 직접 (바이트 단위로) 추가하는 것을 허용하여 문자열과 바이트 슬라이스 사이의 마찰을 줄였습니다. 이제 변환이 더 이상 필요하지 않습니다:

{{code "/doc/progs/go1.go" `/append.*world/`}}

_업데이트_:
이것은 새로운 기능이므로, 기존 코드에 변경 사항이 필요하지 않습니다.

### Close {#close}

`close` 사전 정의 함수는 송신자가 더 이상 값을 보내지 않을 것임을 알리는 메커니즘을 제공합니다.
이는 채널에 대한 `for` `range` 루프 구현에 중요하며, 다른 상황에서도 유용하게 사용됩니다.
부분적으로는 설계 의도이며, 부분적으로는 그렇지 않을 때 발생할 수 있는 레이스 컨디션(race conditions) 때문인데, 이 함수는 데이터를 받는 고루틴이 아니라 채널에 데이터를 보내는 고루틴에서만 사용하도록 의도되었습니다.
하지만 Go 1 이전에는 `close`가 올바르게 사용되고 있는지 확인하는 컴파일 타임 체크 기능이 없었습니다.

이러한 격차를 최소한 부분적으로라도 메우기 위해, Go 1에서는 수신 전용(receive-only) 채널에 대한 `close`를 허용하지 않습니다.
그러한 채널을 닫으려고 시도하면 컴파일 타임 에러가 발생합니다.

{{code "/doc/progs/go1.go" `/STARTCLOSE/` `/ENDCLOSE/`}}

_업데이트_:
수신 전용(receive-only) 채널을 닫으려고 시도하는 기존 코드는 Go 1 이전에도 잘못된 것이었으며 수정되어야 합니다. 이제 컴파일러가 이러한 코드를 거부합니다.

### 복합 리터럴 (Composite literals) {#literals}

Go 1에서는 배열, 슬라이스 또는 맵 타입의 복합 리터럴(composite literal)에서 요소 초기화 식의 타입이 포인터 타입인 경우, 해당 타입 명시를 생략할 수 있습니다.
다음 예제의 네 가지 초기화는 모두 유효합니다. 마지막의 경우 Go 1 이전에는 유효하지 않았습니다.

{{code "/doc/progs/go1.go" `/type Date struct/` `/STOP/`}}

_업데이트_:
이 변경 사항은 기존 코드에 아무런 영향을 주지 않지만, 기존 소스에 `gofmt` `-s` 명령을 적용하면 다른 변경 사항과 더불어 허용되는 모든 곳에서 명시적인 요소 타입(element types)이 생략됩니다.

### init 중의 Goroutines {#init}

이전 언어 정의에서는 초기화 중에 실행되는 `go` 문이 고루틴을 생성하지만, 전체 프로그램의 초기화가 완료될 때까지 실행을 시작하지 않는 것으로 규정했습니다.
이는 여러 곳에서 불편함을 초래했으며, 결과적으로 `init` 구조의 유용성을 제한했습니다.
만약 다른 패키지가 초기화 중에 해당 라이브러리를 사용할 가능성이 있다면, 그 라이브러리는 고루틴 사용을 피해야만 했습니다.
이러한 설계는 단순성과 안전성을 위해 이루어졌으나, 언어에 대한 확신이 커지면서 더 이상 불필요해 보였습니다.
초기화 중에 고루틴을 실행하는 것은 일반적인 실행 중에 실행하는 것보다 더 복잡하거나 안전하지 않은 것이 아닙니다.

Go 1에서는 고루틴(goroutine)을 사용하는 코드를 데드락(deadlock) 없이 `init` 루틴 및 전역 초기화 식에서 호출할 수 있습니다.

{{code "/doc/progs/go1.go" `/PackageGlobal/` `/^}/`}}

_업데이트_:
이것은 새로운 기능이므로 기존 코드에는 변경 사항이 필요하지 않습니다.
다만, `main` 이전에 goroutine이 시작되지 않는 점에 의존하는 코드가 있다면 문제가 발생할 가능성이 있습니다.
표준 리포지토리에는 그러한 코드가 없었습니다.

### rune 타입 {#rune}

언어 사양에서는 `int` 타입이 32비트 또는 64비트 너비를 가질 수 있도록 허용하지만, 현재 구현에서는 64비트 플랫폼에서도 `int`를 32비트로 설정하고 있습니다.
64비트 플랫폼에서 `int`가 64비트가 되는 것이 바람직할 것입니다.
(이는 큰 슬라이스를 인덱싱할 때 중요한 영향을 미칩니다.)
하지만 이러한 변경은 이전 언어로 유니코드 문자를 처리할 때 공간을 낭비하게 되는데, 그 이유는 `int` 타입이 유니코드 코드 포인트(Unicode code points)를 저장하는 데에도 사용되었기 때문입니다. `int`가 32비트에서 64비트로 커지면 각 코드 포인트마다 32비트의 저장 공간이 추가로 낭비됩니다.

64비트 `int`로의 변경을 가능하게 하기 위해,
Go 1은 개별 유니코드 코드 포인트(Unicode code points)를 표현하는
새로운 기본 타입인 `rune`을 도입했습니다.
이는 `uint8`의 별칭인 `byte`와 마찬가지로,
`int32`의 별칭입니다.

`'a'`, `'語'`, `'\u0345'`와 같은 문자 리터럴의 기본 타입이 이제 `rune`이 되었습니다. 이는 `1.0`의 기본 타입이 `float64`인 것과 유사합니다. 따라서 별도로 지정하지 않는 한, 문자 상수로 초기화된 변수의 타입은 `rune`이 됩니다.

적절한 경우 `int` 대신 `rune`을 사용하도록 라이브러리가 업데이트되었습니다. 예를 들어, `unicode.ToLower` 및 관련 함수들은 이제 `rune`을 받고 반환합니다.

{{code "/doc/progs/go1.go" `/STARTRUNE/` `/ENDRUNE/`}}

_업데이트_:
대부분의 소스 코드는 `:=` 초기화자의 타입 추론이 새로운 타입을 조용히 도입하고 그 시점부터 전파되기 때문에 영향을 받지 않을 것입니다.
일부 코드에서는 타입 에러가 발생할 수 있으며, 이는 단순한 변환(conversion)으로 해결될 것입니다.

### 에러 타입 {#error}

Go 1에서는 다음과 같이 정의된 새로운 내장 타입인 `error`를 도입합니다:

```go
type error interface {
	        Error() string
	    }
```

이러한 유형의 결과는 모두 패키지 라이브러리에 포함되어 있으므로, [아래](#errors)에서 다룹니다.

### 맵에서 삭제하기 {#delete}

이전 언어에서는 맵 `m`에서 키 `k`를 가진 엔트리를 삭제하기 위해 다음과 같은 문장을 작성했습니다.

m[k] = value, false

이 구문은 특이한 특수 사례였으며, 유일한 2:1 할당 방식이었습니다.
평가되지만 버려지는 값(보통 무시됨)과, 거의 항상 상수 `false`인 불리언 값을 전달해야 했습니다.
제 기능은 수행했으나 이상한 방식이었으며 논쟁의 대상이 되었습니다.

Go 1에서는 해당 문법이 사라졌으며, 대신 `delete`라는 새로운 내장 함수가 추가되었습니다. 호출 방식은 다음과 같습니다.

{{code "/doc/progs/go1.go" `/delete\(m, k\)/`}}

표현식 `m[k]`로 검색된 맵 항목을 삭제합니다.
반환 값은 없습니다. 존재하지 않는 항목을 삭제하는 것은 아무런 동작도 수행하지 않습니다(no-op).

_업데이트_:
`go` `fix`를 실행하면 `m[k] = value, false` 형태의 표현식이 `delete(m, k)`로 변환됩니다. 이는 무시된 값을 프로그램에서 안전하게 폐기할 수 있고, `false`가 미리 정의된 불리언 상수를 참조한다는 것이 명확할 때 적용됩니다. `fix` 도구는 그 외의 구문 사용 사례에 대해서는 프로그래머가 검토할 수 있도록 표시(flag)합니다.

### 맵 반복문 {#iteration}

이전의 언어 사양에서는 map의 반복 순서를 정의하지 않았으며, 실제로 하드웨어 플랫폼마다 달랐습니다. 이로 인해 map을 반복 처리하는 테스트들이 취약하고 이식성이 떨어졌으며, 한 머신에서는 항상 통과하지만 다른 머신에서는 실패하는 불쾌한 특성이 나타났습니다.

Go 1에서 `for` `range` 문을 사용하여 맵을 반복할 때 요소가 방문되는 순서는 예측 불가능한 것으로 정의되어 있으며, 이는 동일한 맵으로 동일한 루프를 여러 번 실행하더라도 마찬가지입니다.

코드는 요소가 특정한 순서로 방문된다고 가정해서는 안 됩니다.

이 변경 사항은 반복 순서(iteration order)에 의존하는 코드가 초기에 빠르게 중단되어, 문제가 되기 훨씬 전에 수정될 가능성이 매우 높다는 것을 의미합니다.

마찬가지로 중요한 점은, 프로그램이 맵에서 요소를 선택하기 위해 `range` 루프를 사용하는 경우에도 맵 구현체가 더 나은 맵 밸런싱(map balancing)을 보장할 수 있게 한다는 것입니다.

{{code "/doc/progs/go1.go" `/Sunday/` `/^	}/`}}

_업데이트_:
이 부분은 도구의 도움을 받을 수 없는 변경 사항입니다. 대부분의 기존 코드는 영향을 받지 않겠지만, 일부 프로그램은 중단되거나 오작동할 수 있습니다. 맵(map)에 대한 모든 `range` 문이 반복 순서에 의존하지 않는지 수동으로 확인하는 것을 권장합니다. 표준 리포지토리에 몇 가지 이러한 사례가 있었으며, 현재는 모두 수정되었습니다.
반복 순서에 의존하는 것은 이전에도 이미 잘못된 방식이었으며, 해당 순서는 지정되지 않은 상태였습니다. 이번 변경 사항은 이러한 예측 불가능성을 명문화한 것입니다.

### 다중 할당 {#multiple_assignment}

언어 명세는 할당문에서 우측 식들이 모두 평가된 후에 좌측 식들에 할당이 이루어짐을 오랫동안 보장해 왔습니다.
예측 가능한 동작을 보장하기 위해, Go 1은 이 명세를 더욱 세분화합니다.

할당문의 왼쪽 항에 함수 호출이나 배열 인덱싱 작업과 같이 평가가 필요한 표현식이 포함되어 있는 경우, 변수에 값이 할당되기 전에 일반적인 왼쪽에서 오른쪽으로의 규칙(left-to-right rule)에 따라 모든 평가가 먼저 수행됩니다. 모든 평가가 완료되면, 실제 할당이 왼쪽에서 오른쪽 순서로 진행됩니다.

다음 예제들은 해당 동작을 설명합니다.

{{code "/doc/progs/go1.go" `/sa :=/` `/then sc.0. = 2/`}}

_업데이트_:
이 변경 사항은 도구가 도움을 줄 수 없는 부분이지만, 파손(breakage) 가능성은 낮습니다.
표준 저장소의 어떤 코드도 이 변경으로 인해 파손되지 않았으며, 이전의 지정되지 않은 동작에 의존했던 코드는 이미 잘못된 것이었습니다.

### 반환값과 섀도잉 변수(shadowed variables) {#shadowing}

흔히 하는 실수 중 하나는 결과 변수와 이름은 같지만 실제로는 다른 변수에 값을 할당한 후 (인자 없이) `return`을 사용하는 것입니다.
이러한 상황을 _섀도잉(shadowing)_이라고 합니다. 즉, 내부 스코프에서 선언된 동일한 이름의 다른 변수에 의해 결과 변수가 가려진 상태입니다.

이름이 지정된 반환 값(named return values)을 가진 함수에서,
Go 1 컴파일러는 반환 문(return statement) 시점에 이름이 지정된 반환 값 중 어느 하나라도 섀도잉(shadowed)된 경우, 인자가 없는 return 문을 허용하지 않습니다.
(이는 우리가 여전히 탐색 중인 영역이기에 명세(specification)의 일부는 아닙니다.
이 상황은 명시적인 return 문으로 끝나지 않는 함수를 컴파일러가 거부하는 상황과 유사합니다.)

이 함수는 암시적으로 섀도잉된(shadowed) 반환 값을 반환하며, 컴파일러에 의해 거부됩니다:

{{code "/doc/progs/go1.go" `/^func Bug/` `/^}$/`}}

_업데이트_:
이런 방식으로 반환 값을 섀도잉(shadowing)하는 코드는 컴파일러에 의해 거부되며, 수동으로 수정해야 합니다.
표준 저장소에서 발생한 몇 가지 사례들은 대부분 버그였습니다.

### 미공개 필드가 포함된 구조체 복사하기 {#unexported}

이전 언어 버전에서는 패키지가 다른 패키지에 속한 미공개(unexported) 필드를 포함하는 구조체 값의 복사본을 만드는 것을 허용하지 않았습니다.
하지만 메서드 리시버(method receiver)의 경우에는 필수적인 예외가 있었으며, `copy`와 `append`의 구현체 또한 이 제한 사항을 적용한 적이 없었습니다.

Go 1에서는 패키지가 다른 패키지에서 정의된, 공개되지 않은(unexported) 필드를 포함하는 struct 값을 복사하는 것을 허용합니다.
이 변경 사항은 불일치 문제를 해결할 뿐만 아니라,
포인터나 인터페이스에 의존하지 않고도 불투명한(opaque) 값을 반환할 수 있는 새로운 종류의 API를 가능하게 합니다.
`time.Time` 및 `reflect.Value`의 새로운 구현이 이러한 새로운 속성을 활용하는 타입의 예시입니다.

예를 들어, 패키지 `p`에 다음과 같은 정의가 포함되어 있다면,

```go
type Struct struct {
	        Public int
	        secret int
	    }
	    func NewStruct(a int) Struct {  // Note: 포인터가 아닙니다.
	        return Struct{a, f(a)}
	    }
	    func (s Struct) String() string {
	        return fmt.Sprintf("{%d (secret %d)}", s.Public, s.secret)
	    }
```

`p`를 임포트하는 패키지는 `p.Struct` 타입의 값을 자유롭게 할당하고 복사할 수 있습니다.
내부적으로는 export 되지 않은(unexported) 필드들도 마치 export 된 필드인 것처럼 할당되고 복사되지만, 클라이언트 코드는 이를 전혀 알 수 없습니다. 해당 코드는

제공해주신 내용이 `import "p"`라는 코드 한 줄뿐이라, 이를 기술적으로 번역하면 다음과 같습니다.

```go
import "p"
```

```go
myStruct := p.NewStruct(23)
	    copyOfMyStruct := myStruct
	    fmt.Println(myStruct, copyOfMyStruct)
```

struct의 secret 필드가 새로운 값으로 복사되었음을 보여줄 것입니다.

_업데이트_:
이것은 새로운 기능이므로, 기존 코드에 변경 사항이 필요하지 않습니다.

### 동등성 {#equality}

Go 1 이전에는 언어 수준에서 struct와 array 값에 대한 동등성(equality)을 정의하지 않았습니다.
이는 다른 여러 제약 사항과 더불어, struct와 array를 map의 키로 사용할 수 없음을 의미했습니다.
반면, Go는 function과 map 값에 대한 동등성을 정의하고 있었습니다.
함수의 동등성은 클로저(closure)가 있을 때 문제가 되었고(두 클로저가 언제 같다고 볼 수 있는가?),
map의 동등성은 map의 내용이 아니라 포인터를 비교했기 때문에 대개 사용자가 원하는 결과가 아니었습니다.

Go 1에서 이러한 문제들이 해결되었습니다.
먼저, 구조체(structs)와 배열(arrays)은 요소별 비교(element-wise comparison)를 통해 동일성 및 비동일성(`==` 및 `!=`)을 비교할 수 있으며, 따라서 동일성이 정의된 요소들로 구성된 경우 map의 키로 사용할 수 있습니다.

{{code "/doc/progs/go1.go" `/type Day struct/` `/Printf/`}}

둘째로, Go 1에서는 `nil`과의 비교를 제외하고 함수 값에 대한 동등성(equality) 정의를 제거했습니다.
마지막으로, 맵(map)의 동등성 또한 `nil`과의 비교를 제외하고 제거되었습니다.

슬라이스의 경우 등가성(equality)은 여전히 정의되지 않았으며, 일반적으로 계산이 불가능합니다. 또한, 구조체와 배열에 대해서는 순서 비교 연산자(`<` `<=` `>` `>=`)가 여전히 정의되지 않았음에 유의하십시오.

_업데이트_:
구조체(Struct) 및 배열(array)의 동등성 비교는 새로운 기능이므로, 기존 코드에는 변경 사항이 필요 없습니다.
함수(function) 또는 맵(map)의 동등성 비교에 의존하는 기존 코드는 컴파일러에 의해 거부되며, 수동으로 수정해야 합니다.
영향을 받는 프로그램은 거의 없겠지만, 수정 과정에서 일부 재설계가 필요할 수 있습니다.

## 패키지 계층 구조 {#packages}

Go 1은 이전 표준 라이브러리의 많은 결함들을 해결하고 다수의 패키지를 정리하여, 내부 일관성과 이식성을 높였습니다.

이 섹션에서는 Go 1에서 패키지들이 어떻게 재배치되었는지 설명합니다.
일부 패키지는 이동되었고, 일부는 이름이 변경되었으며, 일부는 삭제되었습니다.
새로운 패키지들은 이후 섹션에서 설명합니다.

### 패키지 계층 구조 {#hierarchy}

Go 1은 관련 항목들을 하위 디렉토리로 그룹화하여 패키지 계층 구조를 재배치했습니다. 예를 들어, `utf8`과 `utf16`은 이제 `unicode`의 하위 디렉토리에 위치합니다. 또한, [일부 패키지](#subrepo)는 [`code.google.com/p/go`](https://code.google.com/p/go)의 하위 리포지토리로 이동했으며, [다른 패키지들](#deleted)은 완전히 삭제되었습니다.

<table class="codetable" frame="border" summary="Moved packages">
<colgroup align="left" width="60%"></colgroup>
<colgroup align="left" width="40%"></colgroup>
<tbody><tr>
<th align="left">이전 경로</th>
<th align="left">새 경로</th>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>asn1</td> <td>encoding/asn1</td></tr>
<tr><td>csv</td> <td>encoding/csv</td></tr>
<tr><td>gob</td> <td>encoding/gob</td></tr>
<tr><td>json</td> <td>encoding/json</td></tr>
<tr><td>xml</td> <td>encoding/xml</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>exp/template/html</td> <td>html/template</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>big</td> <td>math/big</td></tr>
<tr><td>cmath</td> <td>math/cmplx</td></tr>
<tr><td>rand</td> <td>math/rand</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>http</td> <td>net/http</td></tr>
<tr><td>http/cgi</td> <td>net/http/cgi</td></tr>
<tr><td>http/fcgi</td> <td>net/http/fcgi</td></tr>
<tr><td>http/httptest</td> <td>net/http/httptest</td></tr>
<tr><td>http/pprof</td> <td>net/http/pprof</td></tr>
<tr><td>mail</td> <td>net/mail</td></tr>
<tr><td>rpc</td> <td>net/rpc</td></tr>
<tr><td>rpc/jsonrpc</td> <td>net/rpc/jsonrpc</td></tr>
<tr><td>smtp</td> <td>net/smtp</td></tr>
<tr><td>url</td> <td>net/url</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>exec</td> <td>os/exec</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>scanner</td> <td>text/scanner</td></tr>
<tr><td>tabwriter</td> <td>text/tabwriter</td></tr>
<tr><td>template</td> <td>text/template</td></tr>
<tr><td>template/parse</td> <td>text/template/parse</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>utf8</td> <td>unicode/utf8</td></tr>
<tr><td>utf16</td> <td>unicode/utf16</td></tr>
</tbody></table>

이전의 `cmath` 및 `exp/template/html` 패키지 이름이 `cmplx` 및 `template`으로 변경되었음에 유의하십시오.

_업데이트_:
`go` `fix`를 실행하면 표준 저장소 내에 남아 있는 패키지에 대한 모든 import와 패키지 이름 변경 사항이 업데이트됩니다. 더 이상 표준 저장소에 존재하지 않는 패키지를 import하는 프로그램은 수동으로 수정해야 합니다.

### 패키지 트리 exp {#exp}

`exp` 디렉터리 아래의 패키지들은 표준화되지 않았기 때문에 표준 Go 1 릴리스 배포판에서는 제공되지 않습니다. 다만, 이를 사용하고자 하는 개발자들을 위해 [저장소](https://code.google.com/p/go/)에 소스 코드 형태로 제공됩니다.

Go 1 릴리스 시점에 여러 패키지가 `exp` 아래로 이동되었습니다:

- `ebnf`
  - `html`<sup>†</sup>
  - `go/types`

(<sup>†</sup>`EscapeString` 및 `UnescapeString` 타입은 `html` 패키지에 그대로 유지됩니다.)

이 모든 패키지들은 `exp/` 접두사가 붙은 동일한 이름으로 제공됩니다: `exp/ebnf` 등.

또한, `utf8.String` 타입이 별도의 패키지인 `exp/utf8string`으로 이동되었습니다.

마지막으로, `gotype` 명령어는 이제 `exp/gotype`에 위치하며, `ebnflint`는 이제 `exp/ebnflint`에 위치합니다.
만약 설치되었다면, 이제 `$GOROOT/bin/tool`에 위치하게 됩니다.

_업데이트_:
`exp` 패키지를 사용하는 코드는 수동으로 업데이트하거나, `exp`를 사용할 수 있는 설치 환경에서 컴파일해야 합니다.
`go` `fix` 도구 또는 컴파일러가 이러한 사용에 대해 경고를 표시할 것입니다.

### 이전 패키지 트리 {#old}

`old` 디렉토리 하위의 패키지들은 더 이상 사용되지 않으므로(deprecated), 표준 Go 1 릴리스 배포판에서는 제공되지 않습니다. 다만, 사용를 원하는 개발자들을 위해 소스 코드 형태로 제공됩니다.

새로운 위치의 패키지들은 다음과 같습니다:

- `old/netchan`

_업데이트_:
현재 `old`에 포함된 패키지를 사용하는 코드는 수동으로 업데이트해야 하며, 그렇지 않으면 `old`를 사용할 수 있는 설치 환경에서 컴파일해야 합니다.
`go` `fix` 도구가 이러한 사용 사례에 대해 경고를 표시합니다.

### 삭제된 패키지 {#deleted}

Go 1에서는 여러 패키지가 완전히 삭제되었습니다:

- `container/vector`
  - `exp/datafmt`
  - `go/typechecker`
  - `old/regexp`
  - `old/template`
  - `try`

그리고 `gotry` 명령어도 있습니다.

_업데이트_:
`container/vector`를 사용하는 코드는 슬라이스(slice)를 직접 사용하도록 업데이트해야 합니다. 몇 가지 제안 사항은 [Go Language Community Wiki](https://code.google.com/p/go-wiki/wiki/SliceTricks)를 참조하십시오.
다른 패키지를 사용하는 코드(거의 없을 것입니다)는 설계를 다시 고민해야 할 것입니다.

### 서브레포지토리로 이동하는 패키지 {#subrepo}

Go 1에서는 다수의 패키지를 다른 저장소, 주로 [메인 Go 저장소](https://code.google.com/p/go/)의 하위 저장소로 이동시켰습니다.
이 표는 이전 및 새로운 import 경로를 나열합니다:

<table class="codetable" frame="border" summary="Sub-repositories">
<colgroup align="left" width="40%"></colgroup>
<colgroup align="left" width="60%"></colgroup>
<tbody><tr>
<th align="left">이전</th>
<th align="left">신규</th>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>crypto/bcrypt</td> <td>code.google.com/p/go.crypto/bcrypt</td></tr>
<tr><td>crypto/blowfish</td> <td>code.google.com/p/go.crypto/blowfish</td></tr>
<tr><td>crypto/cast5</td> <td>code.google.com/p/go.crypto/cast5</td></tr>
<tr><td>crypto/md4</td> <td>code.google.com/p/go.crypto/md4</td></tr>
<tr><td>crypto/ocsp</td> <td>code.google.com/p/go.crypto/ocsp</td></tr>
<tr><td>crypto/openpgp</td> <td>code.google.com/p/go.crypto/openpgp</td></tr>
<tr><td>crypto/openpgp/armor</td> <td>code.google.com/p/go.crypto/openpgp/armor</td></tr>
<tr><td>crypto/openpgp/elgamal</td> <td>code.google.com/p/go.crypto/openpgp/elgamal</td></tr>
<tr><td>crypto/openpgp/errors</td> <td>code.google.com/p/go.crypto/openpgp/errors</td></tr>
<tr><td>crypto/openpgp/packet</td> <td>code.google.com/p/go.crypto/openpgp/packet</td></tr>
<tr><td>crypto/openpgp/s2k</td> <td>code.google.com/p/go.crypto/openpgp/s2k</td></tr>
<tr><td>crypto/ripemd160</td> <td>code.google.com/p/go.crypto/ripemd160</td></tr>
<tr><td>crypto/twofish</td> <td>code.google.com/p/go.crypto/twofish</td></tr>
<tr><td>crypto/xtea</td> <td>code.google.com/p/go.crypto/xtea</td></tr>
<tr><td>exp/ssh</td> <td>code.google.com/p/go.crypto/ssh</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>image/bmp</td> <td>code.google.com/p/go.image/bmp</td></tr>
<tr><td>image/tiff</td> <td>code.google.com/p/go.image/tiff</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>net/dict</td> <td>code.google.com/p/go.net/dict</td></tr>
<tr><td>net/websocket</td> <td>code.google.com/p/go.net/websocket</td></tr>
<tr><td>exp/spdy</td> <td>code.google.com/p/go.net/spdy</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>encoding/git85</td> <td>code.google.com/p/go.codereview/git85</td></tr>
<tr><td>patch</td> <td>code.google.com/p/go.codereview/patch</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>exp/wingui</td> <td>code.google.com/p/gowingui</td></tr>
</tbody></table>

_업데이트_:
`go` `fix`를 실행하면 이 패키지들의 임포트 경로가 새로운 경로를 사용하도록 업데이트됩니다.
이 패키지들에 의존하는 설치 항목들은 `go get` 명령어를 사용하여 다시 설치해야 합니다.

## 라이브러리의 주요 변경 사항 {#major}

이 섹션에서는 가장 많은 프로그램에 영향을 미치는 핵심 라이브러리의 중요한 변경 사항에 대해 설명합니다.

### error 타입과 errors 패키지 {#errors}

`os` 패키지에 `os.Error`가 배치된 것은 대부분 역사적인 이유 때문입니다. 에러는 처음 `os` 패키지를 구현할 때 나타났으며, 당시에는 시스템 관련 사항으로 보였습니다.

그 이후로 에러는 운영체제보다 더 근본적인 개념이라는 점이 분명해졌습니다. 예를 들어, `os`가 의존하는 `syscall`과 같은 패키지에서 `Errors`를 사용할 수 있다면 좋을 것입니다.

또한, `os` 패키지에 `Error`가 있음으로 인해, 그렇지 않았다면 존재하지 않았을 수많은 `os` 패키지 의존성이 발생하게 됩니다.

Go 1은 내장 `error` 인터페이스 타입과 유틸리티 함수들을 포함하는 별도의 `errors` 패키지(`bytes` 및 `strings`와 유사함)를 도입하여 이러한 문제들을 해결합니다.
이는 `os.NewError`를 [`errors.New`](/pkg/errors/#New)로 대체하여, 환경 내에서 에러가 더 중심적인 위치를 갖게 합니다.

널리 사용되는 `String` 메서드가 실수로 `error` 인터페이스를 충족시키는 일을 방지하기 위해, `error` 인터페이스는 해당 메서드의 이름으로 대신 `Error`를 사용합니다:

```go
type error interface {
	        Error() string
	    }
```

`fmt` 라이브러리는 에러 값의 출력을 쉽게 하기 위해, `String`에서와 마찬가지로 `Error`를 자동으로 호출합니다.

{{code "/doc/progs/go1.go" `/START ERROR EXAMPLE/` `/END ERROR EXAMPLE/`}}

모든 표준 패키지가 새로운 인터페이스를 사용하도록 업데이트되었으며, 기존의 `os.Error`는 삭제되었습니다.

새로운 패키지인 [`errors`](/pkg/errors/)에 다음 함수가 포함되어 있습니다.

`func New(text string) error`

문자열을 에러로 변환하는 데 사용됩니다. 기존의 `os.NewError`를 대체합니다.

{{code "/doc/progs/go1.go" `/ErrSyntax/`}}

_업데이트_:
`go` `fix`를 실행하면 변경 사항의 영향을 받는 거의 모든 코드가 업데이트됩니다.
`String` 메서드로 에러 타입을 정의한 코드는 메서드 이름을 `Error`로 변경하도록 수동으로 업데이트해야 합니다.

### 시스템 콜 에러 {#errno}

`os.Error`(와 거의 모든 다른 기능들)보다 앞서 만들어진 오래된 `syscall` 패키지는 에러를 `int` 값으로 반환했습니다. 결과적으로 `os` 패키지는 `EINVAL`과 같은 많은 에러를 전달했지만, 플랫폼마다 서로 다른 에러 세트를 사용했습니다. 이러한 동작은 불편했으며 이식성이 떨어졌습니다.

Go 1에서는 [`syscall`](/pkg/syscall/) 패키지가 시스템 콜 오류에 대해 `error`를 반환합니다. Unix의 경우, 이 구현은 `error`를 충족하며 기존의 `os.Errno`를 대체하는 [`syscall.Errno`](/pkg/syscall/#Errno) 타입에 의해 이루어집니다.

`os.EINVAL` 및 관련 항목에 영향을 주는 변경 사항은 [다른 곳](#os)에 설명되어 있습니다.

_업데이트_:
`go` `fix`를 실행하면 변경 사항의 영향을 받는 거의 모든 코드가 업데이트됩니다.
그럼에도 불구하고, 대부분의 코드는 `syscall` 대신 `os` 패키지를 사용해야 하므로 영향을 받지 않을 것입니다.

### 시간 {#time}

시간은 프로그래밍 언어에서 제대로 지원하기 항상 까다로운 요소입니다.
기존의 Go `time` 패키지는 `int64` 단위를 사용했고, 실질적인 타입 안정성이 없었으며, 절대 시간(absolute times)과 기간(durations)의 구분이 없었습니다.

따라서 Go 1 라이브러리에서 가장 광범위한 변경 사항 중 하나는 [`time`](/pkg/time/) 패키지의 완전한 재설계입니다.
`int64` 형태의 나노초 정수 값과 시간, 년과 같은 인간 중심의 단위를 처리하기 위한 별도의 `*time.Time` 타입을 사용하는 대신, 이제 두 가지 기본 타입이 도입되었습니다.
시점(a moment in time)을 나타내는 [`time.Time`](/pkg/time/#Time)(값 타입이므로 `*`가 제거되었습니다)과, 시간 간격(an interval)을 나타내는 [`time.Duration`](/pkg/time/#Duration)입니다.
두 타입 모두 나노초 해상도를 가집니다.
`Time`은 아주 먼 과거부터 먼 미래까지의 모든 시간을 표현할 수 있는 반면, `Duration`은 약 ±290년까지만 표현할 수 있습니다.
이러한 타입들에는 여러 메서드가 제공되며, `time.Second`와 같이 유용하게 정의된 상수 duration들도 포함되어 있습니다.

새로운 메서드 중에는 `Time`에 `Duration`을 더하는 [`Time.Add`](/pkg/time/#Time.Add)와, 두 `Time`을 빼서 `Duration`을 산출하는 [`Time.Sub`](/pkg/time/#Time.Sub) 등이 있습니다.

가장 중요한 의미론적 변화는 Unix epoch(1970년 1월 1일)가 이제 Unix를 언급하는 함수와 메서드에만 관련된다는 점입니다:
[`time.Unix`](/pkg/time/#Unix)
그리고 `Time` 타입의 [`Unix`](/pkg/time/#Time.Unix)
및 [`UnixNano`](/pkg/time/#Time.UnixNano) 메서드가 이에 해당합니다.
특히,
[`time.Now`](/pkg/time/#Now)
는 이전 API와 달리 Unix epoch 이후의 정수 나노초 수가 아닌 `time.Time` 값을 반환합니다.

{{code "/doc/progs/go1.go" `/sleepUntil/` `/^}/`}}

새로운 타입, 메서드, 상수는 `os` 패키지와 그 안의 파일 타임스탬프 표현 등 `time`을 사용하는 모든 표준 패키지에 반영되었습니다.

_업데이트_:
`go` `fix` 도구는 오래된 `time` 패키지의 많은 사용 사례를 새로운 타입과 메서드를 사용하도록 업데이트하지만, 초당 나노초를 나타내는 `1e9`와 같은 값은 대체하지 않습니다.
또한, 일부 값의 타입 변경으로 인해 `fix` 도구에 의해 다시 작성된 일부 표현식은 추가적인 수동 편집이 필요할 수 있습니다. 이러한 경우, 다시 작성된 코드에는 이전 기능에 해당하는 올바른 함수나 메서드가 포함되어 있겠지만, 타입이 잘못되었거나 추가적인 분석이 필요할 수 있습니다.

## 라이브러리의 사소한 변경 사항 {#minor}

이 섹션에서는 덜 흔하게 사용되는 패키지에 대한 변경 사항이나, `go` `fix`를 실행해야 하는 필요성 외에는 소수의 프로그램에만 영향을 주는 작은 변경 사항들을 설명합니다.
이 범주에는 Go 1에서 새로 도입된 패키지들이 포함됩니다.
이러한 변경 사항들은 종합적으로 이식성을 향상시키고, 동작을 정형화하며, 인터페이스를 더욱 현대적이고 Go다운 방식으로 만들어 줍니다.

### archive/zip 패키지 {#archive_zip}

Go 1에서는 [`*zip.Writer`](/pkg/archive/zip/#Writer)에 더 이상 `Write` 메서드가 존재하지 않습니다. 해당 메서드의 존재는 실수였습니다.

_업데이트_:
영향을 받는 소수의 코드는 컴파일러가 감지하며, 수동으로 업데이트해야 합니다.

### bufio 패키지 {#bufio}

Go 1에서 [`bufio.NewReaderSize`](/pkg/bufio/#NewReaderSize) 및 [`bufio.NewWriterSize`](/pkg/bufio/#NewWriterSize) 함수는 더 이상 잘못된 크기에 대해 에러를 반환하지 않습니다. 인자로 전달된 크기가 너무 작거나 유효하지 않은 경우, 해당 값은 조정됩니다.

_업데이트_:
`go` `fix`를 실행하면 에러를 `_`에 할당하는 호출들이 업데이트됩니다.
수정되지 않은 호출들은 컴파일러에 의해 감지되며, 수동으로 업데이트해야 합니다.

### compress/flate, compress/gzip 및 compress/zlib 패키지 {#compress}

Go 1에서 [`compress/flate`](/pkg/compress/flate), [`compress/gzip`](/pkg/compress/gzip) 및 [`compress/zlib`](/pkg/compress/zlib) 패키지의 `NewWriterXxx` 함수들은 압축 레벨(compression level)을 인자로 받는 경우 `(*Writer, error)`를 반환하며, 그렇지 않은 경우에는 `*Writer`를 반환합니다. `gzip` 패키지의 `Compressor`와 `Decompressor` 타입은 각각 `Writer`와 `Reader`로 이름이 변경되었습니다. `flate` 패키지의 `WrongValueError` 타입은 삭제되었습니다.

_업데이트하기_
`go` `fix`를 실행하면 에러를 \_에 할당하는 오래된 이름과 호출들이 업데이트됩니다.
수정되지 않은 호출들은 컴파일러에 의해 감지되며, 수동으로 업데이트해야 합니다.

### crypto/aes 및 crypto/des 패키지 {#crypto_aes_des}

Go 1에서 `Reset` 메서드가 제거되었습니다. Go는 메모리가 복사되지 않음을 보장하지 않으며, 따라서 이 메서드는 오해의 소지가 있었습니다.

`*aes.Cipher`, `*des.Cipher` 및 `*des.TripleDESCipher`와 같은 암호 알고리즘별 타입들이 `cipher.Block`으로 대체되어 제거되었습니다.

_업데이트_:
Reset 호출을 제거하십시오. 특정 cipher 타입의 사용을 `cipher.Block`으로 대체하십시오.

### crypto/elliptic 패키지 {#crypto_elliptic}

Go 1에서 [`elliptic.Curve`](/pkg/crypto/elliptic/#Curve)는 대안적인 구현을 허용하기 위해 인터페이스로 변경되었습니다. 곡선 매개변수(curve parameters)는 [`elliptic.CurveParams`](/pkg/crypto/elliptic/#CurveParams) 구조체로 이동되었습니다.

_업데이트_:
`*elliptic.Curve`를 사용하던 기존 사용자는 단순히 `elliptic.Curve`로 변경해야 합니다. `Marshal`, `Unmarshal` 및 `GenerateKey` 호출은 이제 `crypto/elliptic` 내의 함수로 변경되었으며, 첫 번째 인자로 `elliptic.Curve`를 받습니다.

### crypto/hmac 패키지 {#crypto_hmac}

Go 1에서는 `hmac.NewMD5`와 같은 해시 전용 함수들이 `crypto/hmac`에서 제거되었습니다. 대신, `hmac.New`는 `md5.New`와 같이 `hash.Hash`를 반환하는 함수를 인자로 받습니다.

_업데이트_:
`go` `fix`를 실행하면 필요한 변경 사항이 적용됩니다.

### crypto/x509 패키지 {#crypto_x509}

Go 1에서는 `crypto/x509` 패키지의 [`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate) 함수와 [`CreateCRL`](/pkg/crypto/x509/#Certificate.CreateCRL) 메서드가 기존의 `*rsa.PublicKey` 또는 `*rsa.PrivateKey` 대신 `interface{}`를 받도록 변경되었습니다. 이를 통해 향후 다른 공개 키 알고리즘들이 구현될 수 있게 됩니다.

_업데이트_:
변경 사항이 필요하지 않습니다.

### encoding/binary 패키지 {#encoding_binary}

Go 1에서는 `binary.TotalSize` 함수가 [`Size`](/pkg/encoding/binary/#Size)로 대체되었으며, 이 함수는 `reflect.Value` 대신 `interface{}` 인자를 받습니다.

_업데이트_:
영향을 받는 소량의 코드는 컴파일러에 의해 감지되며, 수동으로 업데이트해야 합니다.

### encoding/xml 패키지 {#encoding_xml}

Go 1에서 [`xml`](/pkg/encoding/xml/) 패키지는 [`encoding/gob`](/pkg/encoding/gob/)와 같은 다른 마샬링 패키지들의 설계 방식과 더 유사하게 변경되었습니다.

기존의 `Parser` 타입은 [`Decoder`](/pkg/encoding/xml/#Decoder)로 이름이 변경되었으며, 새로운 [`Decode`](/pkg/encoding/xml/#Decoder.Decode) 메서드가 추가되었습니다. 또한 [`Encoder`](/pkg/encoding/xml/#Encoder) 타입가 도입되었습니다.

[`Marshal`](/pkg/encoding/xml/#Marshal) 및 [`Unmarshal`](/pkg/encoding/xml/#Unmarshal) 함수은 이제 `[]byte` 값으로 작동합니다. 스트림으로 작업하려면 새로운 [`Encoder`](/pkg/encoding/xml/#Encoder) 및 [`Decoder`](/pkg/encoding/xml/#Decoder) 타입을 사용하십시오.

값을 마샬링(marshaling)하거나 언마샬링(unmarshaling)할 때, 필드 태그에서 지원되는 플래그 형식이 [`json`](/pkg/encoding/json) 패키지와 더 유사하게 변경되었습니다(`` `xml:"name,flag"` ``). 이제 필드 태그, 필드 이름, 그리고 XML 속성 및 요소 이름 간의 매칭은 대소문자를 구분합니다. `XMLName` 필드 태그가 있는 경우, 해당 태그는 마샬링되는 XML 요소의 이름과 일치해야 합니다.

_업데이트_:
`go` `fix`를 실행하면 `Unmarshal`에 대한 일부 호출을 제외한 대부분의 패키지 사용처가 업데이트됩니다. 필드 태그의 경우 `fix` 도구가 이를 업데이트하지 않으므로 특별한 주의가 필요하며, 수동으로 수정하지 않으면 일부 경우에 소리 없이 잘못 작동할 수 있습니다. 예를 들어, 이전의 `"attr"`은 이제 `",attr"`로 작성하며, 일반 `"attr"`은 여전히 유효하지만 의미가 달라졌습니다.

### expvar 패키지 {#expvar}

Go 1에서 `RemoveAll` 함수가 제거되었습니다.
`*Map`의 `Iter` 함수와 `Iter` 메서드는
[`Do`](/pkg/expvar/#Do) 및
[`(*Map).Do`](/pkg/expvar/#Map.Do)로 대체되었습니다.

_업데이트_:
`expvar`를 사용하는 대부분의 코드는 변경할 필요가 없습니다. `Iter`를 사용했던 드문 경우에는 `Do`에 클로저를 전달하도록 업데이트하여 동일한 효과를 얻을 수 있습니다.

### flag 패키지 {#flag}

Go 1에서 [`flag.Value`](/pkg/flag/#Value) 인터페이스가 약간 변경되었습니다.
이제 `Set` 메서드는 성공 또는 실패를 나타내기 위해 `bool` 대신 `error`를 반환합니다.

시간 간격을 지정하는 인자 값을 지원하기 위해 `Duration`이라는 새로운 종류의 플래그가 추가되었습니다.
이러한 플래그의 값에는 `time.Duration` 형식과 동일하게 `10s`, `1h30m` 등과 같이 단위를 지정해야 합니다.

{{code "/doc/progs/go1.go" `/timeout/`}}

_업데이트_:
자체 플래그를 구현하는 프로그램은 `Set` 메서드를 업데이트하기 위해 약간의 수동 수정이 필요합니다.
`Duration` 플래그는 새로 추가되었으며 기존 코드에는 영향을 주지 않습니다.

### go/\* 패키지 {#go}

`go` 하위의 여러 패키지들의 API가 약간 수정되었습니다.

다음 패키지들의 설정 모드 플래그를 위해 구체적인 `Mode` 타입이 도입되었습니다:
[`go/scanner`](/pkg/go/scanner/),
[`go/parser`](/pkg/go/parser/),
[`go/printer`](/pkg/go/printer/), 그리고
[`go/doc`](/pkg/go/doc/).

[`go/scanner`](/pkg/go/scanner/) 패키지에서 `AllowIllegalChars` 및 `InsertSemis` 모드가 제거되었습니다. 이 모드들은 주로 Go 소스 파일이 아닌 텍스트를 스캔할 때 유용했습니다. 해당 목적을 위해서는 대신 [`text/scanner`](/pkg/text/scanner/) 패키지를 사용해야 합니다.

scanner의 [`Init`](/pkg/go/scanner/#Scanner.Init) 메서드에 제공되는 [`ErrorHandler`](/pkg/go/scanner/#ErrorHandler)가 이제 인터페이스가 아닌 단순한 함수로 변경되었습니다. `ErrorVector` 타입은 기존의 [`ErrorList`](/pkg/go/scanner/#ErrorList) 타입을 사용하는 방향으로 제거되었으며, `ErrorVector` 메서드들은 이전되었습니다. 이제 scanner 클라이언트는 `ErrorVector`를 임베딩하는 대신 `ErrorList`를 유지해야 합니다.

[`go/parser`](/pkg/go/parser/) 패키지에서 제공하는 파싱 함수 세트는 주요 파싱 함수인 [`ParseFile`](/pkg/go/parser/#ParseFile)과 몇 가지 편의 함수인 [`ParseDir`](/pkg/go/parser/#ParseDir) 및 [`ParseExpr`](/pkg/go/parser/#ParseExpr)로 축소되었습니다.

[`go/printer`](/pkg/go/printer/) 패키지는 추가 설정 모드인 [`SourcePos`](/pkg/go/printer/#Mode)를 지원합니다. 이 모드가 설정되면, printer는 생성된 출력물에 원본 소스 코드의 위치 정보가 포함되도록 `//line` 주석을 출력합니다. 새로운 타입인 [`CommentedNode`](/pkg/go/printer/#CommentedNode)를 사용하면 임의의 [`ast.Node`](/pkg/go/ast/#Node)와 연결된 주석을 제공할 수 있습니다 (기존에는 [`ast.File`](/pkg/go/ast/#File)만 주석 정보를 가지고 있었습니다).

[`go/doc`](/pkg/go/doc/) 패키지의 타입 이름들이 `Doc` 접미사를 제거하여 간소화되었습니다: `PackageDoc`은 이제 `Package`가 되었고, `ValueDoc`은 `Value`가 되는 방식입니다.
또한, 이제 모든 타입이 일관되게 `Name` 필드(`Value` 타입의 경우 `Names`)를 가지며, `Type.Factories`는 `Type.Funcs`로 변경되었습니다.
`doc.NewPackageDoc(pkg, importpath)`를 호출하는 대신, 패키지에 대한 문서는 다음과 같이 생성합니다:

`doc.New(pkg, importpath, mode)`

여기서 새로운 `mode` 매개변수는 동작 모드를 지정합니다:
[`AllDecls`](/pkg/go/doc/#AllDecls)로 설정하면, (내보내기 된 것뿐만 아니라) 모든 선언이 고려됩니다.
`NewFileDoc` 함수는 제거되었으며, `CommentText` 함수는 [`ast.CommentGroup`](/pkg/go/ast/#CommentGroup)의 [`Text`](/pkg/go/ast/#CommentGroup.Text) 메서드로 변경되었습니다.

[`go/token`](/pkg/go/token/) 패키지에서, 기존에 `*token.File` 채널을 반환하던 [`token.FileSet`](/pkg/go/token/#FileSet)의 `Files` 메서드가 함수 인자를 받는 이터레이터인 [`Iterate`](/pkg/go/token/#FileSet.Iterate)로 대체되었습니다.

[`go/build`](/pkg/go/build/) 패키지에서 API가 거의 완전히 교체되었습니다.
이 패키지는 여전히 Go 패키지 정보를 계산하지만, 빌드를 실행하지는 않습니다. 즉, `Cmd` 및 `Script` 타입이 삭제되었습니다.
(코드를 빌드하려면 대신 새로운 [`go`](/cmd/go/) 명령어를 사용하십시오.)
`DirInfo` 타입의 이름이 이제 [`Package`](/pkg/go/build/#Package)로 변경되었습니다.
`FindTree` 및 `ScanDir`은 [`Import`](/pkg/go/build/#Import) 및 [`ImportDir`](/pkg/go/build/#ImportDir)로 대체되었습니다.

_업데이트_:
`go` 패키지를 사용하는 코드는 수동으로 업데이트해야 합니다. 컴파일러가 잘못된 사용법을 거부할 것입니다. `go/doc` 타입과 함께 사용되는 템플릿은 수동 수정이 필요할 수 있습니다. 이름이 변경된 필드는 런타임 오류를 유발할 수 있습니다.

### hash 패키지 {#hash}

Go 1에서 [`hash.Hash`](/pkg/hash/#Hash)의 정의에는 새로운 메서드인 `BlockSize`가 포함되었습니다. 이 새로운 메서드는 주로 암호화 라이브러리에서 사용됩니다.

[`hash.Hash`](/pkg/hash/#Hash) 인터페이스의 `Sum` 메서드는 이제 해시 값이 추가될 `[]byte` 인자를 받습니다. 이전의 동작은 호출 시 `nil` 인자를 추가함으로써 재현할 수 있습니다.

_업데이트_:
`hash.Hash`의 기존 구현체들은 `BlockSize` 메서드를 추가해야 합니다. 입력을 한 번에 1바이트씩 처리하는 해시의 경우, `BlockSize`가 1을 반환하도록 구현할 수 있습니다.
`go` `fix`를 실행하면 `hash.Hash`의 다양한 구현체들에 있는 `Sum` 메서드 호출 부분이 업데이트됩니다.

_업데이트_:
패키지의 기능이 신규이므로, 업데이트가 필요하지 않습니다.

### http 패키지 {#http}

Go 1에서는 [`http`](/pkg/net/http/) 패키지가 리팩토링되어, 일부 유틸리티들이 [`httputil`](/pkg/net/http/httputil/) 하위 디렉토리로 이동되었습니다.
이 기능들은 HTTP 클라이언트에서 거의 드물게 사용됩니다.
영향을 받는 항목들은 다음과 같습니다:

- ClientConn
  - DumpRequest
  - DumpRequestOut
  - DumpResponse
  - NewChunkedReader
  - NewChunkedWriter
  - NewClientConn
  - NewProxyClientConn
  - NewServerConn
  - NewSingleHostReverseProxy
  - ReverseProxy
  - ServerConn

`Request.RawURL` 필드가 제거되었습니다. 이는 과거의 유산이었습니다.

`Handle` 및 `HandleFunc` 함수와 `ServeMux`의 유사한 이름의 메서드들은 이제 동일한 패턴을 두 번 등록하려고 시도하면 패닉(panic)이 발생합니다.

_업데이트_:
`go` `fix`를 실행하면 `RawURL` 사용 사례를 제외하고 영향을 받는 소수의 프로그램들이 업데이트됩니다. `RawURL` 사용 사례는 수동으로 수정해야 합니다.

### image 패키지 {#image}

[`image`](/pkg/image/) 패키지에 몇 가지 사소한 변경, 재배치 및 이름 변경이 있었습니다.

대부분의 색상 처리 코드가 별도의 패키지인 [`image/color`](/pkg/image/color/)로 이동되었습니다.
이동된 요소들 사이에는 대칭성이 발생합니다. 예를 들어,
[`image.RGBA`](/pkg/image/#RGBA)
의 각 픽셀은
[`color.RGBA`](/pkg/image/color/#RGBA)
입니다.

기존의 `image/ycbcr` 패키지는 일부 이름 변경과 함께 [`image`](/pkg/image/) 및 [`image/color`](/pkg/image/color/) 패키지로 통합되었습니다.

이전의 `image.ColorImage` 타입은 여전히 `image` 패키지에 존재하지만 [`image.Uniform`](/pkg/image/#Uniform)으로 이름이 변경되었으며, `image.Tiled`는 삭제되었습니다.

이 테이블은 이름 변경 사항을 나열합니다.

<table class="codetable" frame="border" summary="image renames">
<colgroup align="left" width="50%"></colgroup>
<colgroup align="left" width="50%"></colgroup>
<tbody><tr>
<th align="left">이전</th>
<th align="left">변경 후</th>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>image.Color</td> <td>color.Color</td></tr>
<tr><td>image.ColorModel</td> <td>color.Model</td></tr>
<tr><td>image.ColorModelFunc</td> <td>color.ModelFunc</td></tr>
<tr><td>image.PalettedColorModel</td> <td>color.Palette</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>image.RGBAColor</td> <td>color.RGBA</td></tr>
<tr><td>image.RGBA64Color</td> <td>color.RGBA64</td></tr>
<tr><td>image.NRGBAColor</td> <td>color.NRGBA</td></tr>
<tr><td>image.NRGBA64Color</td> <td>color.NRGBA64</td></tr>
<tr><td>image.AlphaColor</td> <td>color.Alpha</td></tr>
<tr><td>image.Alpha16Color</td> <td>color.Alpha16</td></tr>
<tr><td>image.GrayColor</td> <td>color.Gray</td></tr>
<tr><td>image.Gray16Color</td> <td>color.Gray16</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>image.RGBAColorModel</td> <td>color.RGBAModel</td></tr>
<tr><td>image.RGBA64ColorModel</td> <td>color.RGBA64Model</td></tr>
<tr><td>image.NRGBAColorModel</td> <td>color.NRGBAModel</td></tr>
<tr><td>image.NRGBA64ColorModel</td> <td>color.NRGBA64Model</td></tr>
<tr><td>image.AlphaColorModel</td> <td>color.AlphaModel</td></tr>
<tr><td>image.Alpha16ColorModel</td> <td>color.Alpha16Model</td></tr>
<tr><td>image.GrayColorModel</td> <td>color.GrayModel</td></tr>
<tr><td>image.Gray16ColorModel</td> <td>color.Gray16Model</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>ycbcr.RGBToYCbCr</td> <td>color.RGBToYCbCr</td></tr>
<tr><td>ycbcr.YCbCrToRGB</td> <td>color.YCbCrToRGB</td></tr>
<tr><td>ycbcr.YCbCrColorModel</td> <td>color.YCbCrModel</td></tr>
<tr><td>ycbcr.YCbCrColor</td> <td>color.YCbCr</td></tr>
<tr><td>ycbcr.YCbCr</td> <td>image.YCbCr</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>ycbcr.SubsampleRatio444</td> <td>image.YCbCrSubsampleRatio444</td></tr>
<tr><td>ycbcr.SubsampleRatio422</td> <td>image.YCbCrSubsampleRatio422</td></tr>
<tr><td>ycbcr.SubsampleRatio420</td> <td>image.YCbCrSubsampleRatio420</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>image.ColorImage</td> <td>image.Uniform</td></tr>
</tbody></table>

`image` 패키지의 `New` 함수들
([`NewRGBA`](/pkg/image/#NewRGBA),
[`NewRGBA64`](/pkg/image/#NewRGBA64) 등)은
4개의 정수 대신 [`image.Rectangle`](/pkg/image/#Rectangle)을 인자로 받습니다.

마지막으로, 새로운 사전 정의된 `color.Color` 변수인
[`color.Black`](/pkg/image/color/#Black),
[`color.White`](/pkg/image/color/#White),
[`color.Opaque`](/pkg/image/color/#Opaque)
및
[`color.Transparent`](/pkg/image/color/#Transparent)가 추가되었습니다.

_업데이트_:
`go` `fix`를 실행하면 변경 사항의 영향을 받는 거의 모든 코드가 업데이트됩니다.

### log/syslog 패키지 {#log_syslog}

Go 1에서 [`syslog.NewLogger`](/pkg/log/syslog/#NewLogger) 함수는 `log.Logger`와 함께 에러(error)를 반환합니다.

_업데이트_:
영향을 받는 소량의 코드는 컴파일러에 의해 감지되며, 수동으로 업데이트해야 합니다.

### mime 패키지 {#mime}

Go 1에서 `mime` 패키지의 [`FormatMediaType`](/pkg/mime/#FormatMediaType) 함수가 [`ParseMediaType`](/pkg/mime/#ParseMediaType)와 일관성을 유지하도록 간소화되었습니다. 이제 `"text"`와 `"html"` 대신 `"text/html"`을 인자로 받습니다.

_업데이트_:
영향을 받는 소수의 코드는 컴파일러가 감지하며, 수동으로 업데이트해야 합니다.

### net 패키지 {#net}

Go 1에서는 기존의 다양한 `SetTimeout`, `SetReadTimeout` 및 `SetWriteTimeout` 메서드가 각각 [`SetDeadline`](/pkg/net/#IPConn.SetDeadline), [`SetReadDeadline`](/pkg/net/#IPConn.SetReadDeadline) 및 [`SetWriteDeadline`](/pkg/net/#IPConn.SetWriteDeadline)으로 대체되었습니다. 연결의 모든 활동에 적용되는 나노초 단위의 타임아웃 값을 받는 대신, 새로운 메서드들은 절대적인 마감 기한(`time.Time` 값으로)을 설정하며, 이 시간이 지나면 읽기 및 쓰기 작업이 타임아웃되어 더 이상 블록(block)되지 않습니다.

또한 네트워크 주소 다이얼링의 타임아웃 처리를 단순화하는 [`net.DialTimeout`](/pkg/net/#DialTimeout)과, 여러 리스너에서 동시에 멀티캐스트 UDP를 수신할 수 있도록 하는 [`net.ListenMulticastUDP`](/pkg/net/#ListenMulticastUDP)라는 새로운 함수들이 추가되었습니다. `net.ListenMulticastUDP` 함수는 기존의 `JoinGroup` 및 `LeaveGroup` 메서드를 대체합니다.

_업데이트_:
이전 메서드를 사용하는 코드는 컴파일에 실패하며 수동으로 업데이트해야 합니다.
의미론적 변경으로 인해 수정 도구가 자동으로 업데이트하기 어렵습니다.

### os 패키지 {#os}

`Time` 함수가 삭제되었습니다. 호출자는 `time` 패키지의 [`Time`](/pkg/time/#Time) 타입을 사용해야 합니다.

`Exec` 함수가 제거되었습니다. 호출자는 사용 가능한 경우 `syscall` 패키지의 `Exec`를 사용해야 합니다.

`ShellExpand` 함수가 [`ExpandEnv`](/pkg/os/#ExpandEnv)로 이름이 변경되었습니다.

[`NewFile`](/pkg/os/#NewFile) 함수가 이제 `int` 대신 `uintptr` fd를 받습니다.
파일의 [`Fd`](/pkg/os/#File.Fd) 메서드 또한 이제 `uintptr`을 반환합니다.

`os` 패키지에서 `EINVAL`과 같은 에러 상수들이 더 이상 제공되지 않습니다. 이는 값의 집합이 기본 운영 체제에 따라 달랐기 때문입니다. 공통적인 에러 속성을 테스트하기 위해 [`IsPermission`](/pkg/os/#IsPermission)과 같은 새로운 이식성 있는 함수들이 추가되었으며, [`ErrPermission`](/pkg/os/#ErrPermission) 및 [`ErrNotExist`](/pkg/os/#ErrNotExist)와 같이 Go 스타일의 이름을 가진 몇 가지 새로운 에러 값들이 추가되었습니다.

`Getenverror` 함수가 삭제되었습니다. 존재하지 않는 환경 변수와 빈 문자열을 구분하려면 [`os.Environ`](/pkg/os/#Environ) 또는 [`syscall.Getenv`](/pkg/syscall/#Getenv)를 사용하세요.

[`Process.Wait`](/pkg/os/#Process.Wait) 메서드에서 옵션 인자가 제거되었으며, 관련 상수들도 패키지에서 삭제되었습니다.
또한, `Wait` 함수가 삭제되었으며, `Process` 타입의 메서드만 유지됩니다.

[`Process.Wait`](/pkg/os/#Process.Wait)에서 반환하던 `Waitmsg` 타입은 프로세스 정보를 복구하기 위한 접근자 메서드(accessor methods)를 가진, 보다 이식성 높은 [`ProcessState`](/pkg/os/#ProcessState) 타입으로 대체되었습니다.

`Wait` 함수의 변경 사항으로 인해, `ProcessState` 값은 항상 종료된 프로세스를 설명합니다.

이식성 문제로 인해 다른 방식의 인터페이스 단순화가 이루어졌으나, [`ProcessState.Sys`](/pkg/os/#ProcessState.Sys) 및 [`ProcessState.SysUsage`](/pkg/os/#ProcessState.SysUsage) 메서드가 반환하는 값은 Unix의 [`syscall.WaitStatus`](/pkg/syscall/#WaitStatus) 및 [`syscall.Rusage`](/pkg/syscall/#Rusage)와 같은 시스템별 기본 데이터 구조로 타입 단언(type-asserted)될 수 있습니다.

_업데이트_:
`go` `fix`를 실행하면 `Process.Wait`에 전달되는 제로 인자(zero argument)가 제거됩니다.
그 외의 모든 변경 사항은 컴파일러에 의해 감지되며, 수동으로 업데이트해야 합니다.

#### os.FileInfo 타입 {#os_fileinfo}

Go 1에서는 [`os.FileInfo`](/pkg/os/#FileInfo) 타입을 구조체(struct)에서 인터페이스(interface)로 변경하여 재정의합니다.

```go
type FileInfo interface {
	        Name() string       // 파일의 기본 이름
	        Size() int64        // 바이트 단위의 길이
	        Mode() FileMode     // 파일 모드 비트
	        ModTime() time.Time // 수정 시간
	        IsDir() bool        // Mode().IsDir()의 축약형
	        Sys() interface{}   // 기본 데이터 소스 (nil을 반환할 수 있음)
	    }
```

파일 모드 정보는 [`os.FileMode`](/pkg/os/#FileMode)라는 서브타입으로 이동되었습니다. 이는 `IsDir`, `Perm`, `String` 메서드를 가진 단순한 정수 타입입니다.

(Unix의) i-number와 같은 파일 모드 및 속성에 대한 시스템별 세부 사항이 `FileInfo`에서 완전히 제거되었습니다.
대신, 각 운영체제의 `os` 패키지는 파일 메타데이터의 시스템별 표현을 반환하는 `Sys` 메서드가 포함된 `FileInfo` 인터페이스의 구현체를 제공합니다.
예를 들어, Unix 시스템에서 파일의 i-number를 확인하려면 다음과 같이 `FileInfo`의 래퍼를 해제하십시오.

```go
fi, err := os.Stat("hello.go")
	    if err != nil {
	        log.Fatal(err)
	    }
	    // Unix 파일인지 확인합니다.
	    unixStat, ok := fi.Sys().(*syscall.Stat_t)
	    if !ok {
	        log.Fatal("hello.go: not a Unix file")
	    }
	    fmt.Printf("file i-number: %d\n", unixStat.Ino)
```

`"hello.go"`가 Unix 파일이라고 가정한다면(현명하지 못한 가정입니다), i-number 표현식은 다음과 같이 축약될 수 있습니다.

`fi.Sys().(*syscall.Stat_t).Ino`

`FileInfo` 사용 사례의 대부분은 표준 인터페이스의 메서드만 필요로 합니다.

`os` 패키지는 더 이상 `ENOENT`와 같은 POSIX 에러에 대한 래퍼(wrapper)를 포함하지 않습니다.
특정 에러 조건을 확인해야 하는 소수의 프로그램을 위해, 이제는 다음과 같은 불리언(boolean) 함수들이 제공됩니다:
[`IsExist`](/pkg/os/#IsExist),
[`IsNotExist`](/pkg/os/#IsNotExist),
그리고
[`IsPermission`](/pkg/os/#IsPermission).

{{code "/doc/progs/go1.go" `/os\.Open/` `/}/`}}

_업데이트_:
`go` `fix`를 실행하면 현재의 `os.FileInfo` 및 `os.FileMode` API의 이전 동등 기능을 사용하는 코드가 업데이트됩니다.
시스템별 파일 세부 정보가 필요한 코드는 수동으로 업데이트해야 합니다.
`os` 패키지의 이전 POSIX 에러 값을 사용하는 코드는 컴파일에 실패하며, 이 또한 수동으로 업데이트해야 합니다.

### os/signal 패키지 {#os_signal}

Go 1의 `os/signal` 패키지에서는 모든 수신 신호를 받는 채널을 반환했던 `Incoming` 함수가, 기존 채널로 특정 신호만 전달받도록 요청하는 선택적 `Notify` 함수로 대체되었습니다.

_업데이트_:
코드는 수동으로 업데이트해야 합니다.
~의 직역

`c := signal.Incoming()`

번역할 내용을 제공해 주세요. 영문 Markdown 콘텐츠를 입력하시면 요청하신 지침에 따라 정밀하게 한국어로 번역해 드리겠습니다.

```go
c := make(chan os.Signal, 1)
	signal.Notify(c) // 모든 시그널을 요청합니다.
```

하지만 대부분의 코드는 대신 처리하고자 하는 특정 시그널을 다음과 같이 나열해야 합니다:

```go
c := make(chan os.Signal, 1)
	signal.Notify(c, syscall.SIGHUP, syscall.SIGQUIT)
```

### path/filepath 패키지 {#path_filepath}

Go 1에서 `path/filepath` 패키지의 [`Walk`](/pkg/path/filepath/#Walk) 함수가 `Visitor` 인터페이스 값 대신 [`WalkFunc`](/pkg/path/filepath/#WalkFunc) 타입의 함수 값을 받도록 변경되었습니다. `WalkFunc`는 파일과 디렉토리 모두에 대한 처리를 통합합니다.

`type WalkFunc func(path string, info os.FileInfo, err error) error`

`WalkFunc` 함수는 열 수 없는 파일이나 디렉터리의 경우에도 호출됩니다.
이러한 경우 error 인자가 실패 원인을 설명합니다.
디렉터리의 내용을 건너뛰려면,
함수는 [`filepath.SkipDir`](/pkg/path/filepath/#pkg-variables) 값을 반환해야 합니다.

{{code "/doc/progs/go1.go" `/STARTWALK/` `/ENDWALK/`}}

_업데이트_:
이 변경 사항은 대부분의 코드를 단순화하지만 미묘한 영향을 미치므로, 영향을 받는 프로그램은 수동으로 업데이트해야 합니다.
컴파일러가 이전 인터페이스를 사용하는 코드를 감지하여 알려줄 것입니다.

### regexp 패키지 {#regexp}

[`regexp`](/pkg/regexp/) 패키지가 새롭게 작성되었습니다.
인터페이스는 동일하지만, 지원하는 정규 표현식 사양이 기존의 "egrep" 형식에서 [RE2](https://code.google.com/p/re2/) 형식으로 변경되었습니다.

_업데이트_:
패키지를 사용하는 코드는 정규 표현식을 수동으로 확인해야 합니다.

### runtime 패키지 {#runtime}

Go 1에서는 다른 패키지에서 제공하는 기능들을 대신 사용하도록 `runtime` 패키지에서 내보내는 API의 상당 부분이 제거되었습니다.
`runtime.Type` 인터페이스 또는 그 구체적인 타입 구현을 사용하는 코드는 이제 [`reflect`](/pkg/reflect/) 패키지를 사용해야 합니다.
`runtime.Semacquire` 또는 `runtime.Semrelease`를 사용하는 코드는 채널이나 [`sync`](/pkg/sync/) 패키지의 추상화 기능을 사용해야 합니다.
메모리 할당자 디버깅을 위해 만들어진 안전하지 않은(unsafe) API인 `runtime.Alloc`, `runtime.Free`, `runtime.Lookup` 함수는 대체 수단이 없습니다.

이전에는 `runtime.MemStats`가 메모리 할당에 관한 통계 정보를 보유하는 전역 변수였으며, `runtime.UpdateMemStats` 호출을 통해 최신 상태로 유지되었습니다.
Go 1에서 `runtime.MemStats`는 구조체 타입이며, 코드는 [`runtime.ReadMemStats`](/pkg/runtime/#ReadMemStats)를 사용하여 현재 통계 정보를 가져와야 합니다.

이 패키지는 운영 체제 커널이 보고하는 병렬 실행 가능 CPU 수를 반환하는 새로운 함수인 [`runtime.NumCPU`](/pkg/runtime/#NumCPU)를 추가합니다. 이 값은 `GOMAXPROCS` 설정을 결정하는 데 참고할 수 있습니다. `runtime.Cgocalls` 및 `runtime.Goroutines` 함수는 `runtime.NumCgoCall` 및 `runtime.NumGoroutine`으로 이름이 변경되었습니다.

_업데이트_:
`go` `fix`를 실행하면 함수 이름 변경에 따라 코드가 업데이트됩니다.
그 외의 코드는 수동으로 업데이트해야 합니다.

### strconv 패키지 {#strconv}

Go 1에서 [`strconv`](/pkg/strconv/) 패키지는 더 C-like가 아닌 Go-like하게 만들기 위해 상당 부분 재작업되었습니다. 비록 `Atoi`는 계속 유지되었지만(이는 `int(ParseInt(x, 10, 0))`와 유사하며, `Itoa(x)` 역시 `FormatInt(int64(x), 10)`와 유사합니다), 할당(allocation)을 제어할 수 있도록 문자열을 반환하는 대신 바이트 슬라이스에 추가하는 새로운 함수 변형들이 추가되었습니다.

이 표는 이름 변경 사항을 요약한 것입니다. 자세한 내용은 [패키지 문서](/pkg/strconv/)를 참조하십시오.

<table class="codetable" frame="border" summary="strconv renames">
<colgroup align="left" width="50%"></colgroup>
<colgroup align="left" width="50%"></colgroup>
<tbody><tr>
<th align="left">이전 호출</th>
<th align="left">새 호출</th>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>Atob(x)</td> <td>ParseBool(x)</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>Atof32(x)</td> <td>ParseFloat(x, 32)§</td></tr>
<tr><td>Atof64(x)</td> <td>ParseFloat(x, 64)</td></tr>
<tr><td>AtofN(x, n)</td> <td>ParseFloat(x, n)</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>Atoi(x)</td> <td>Atoi(x)</td></tr>
<tr><td>Atoi(x)</td> <td>ParseInt(x, 10, 0)§</td></tr>
<tr><td>Atoi64(x)</td> <td>ParseInt(x, 10, 64)</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>Atoui(x)</td> <td>ParseUint(x, 10, 0)§</td></tr>
<tr><td>Atoui64(x)</td> <td>ParseUint(x, 10, 64)</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>Btoi64(x, b)</td> <td>ParseInt(x, b, 64)</td></tr>
<tr><td>Btoui64(x, b)</td> <td>ParseUint(x, b, 64)</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>Btoa(x)</td> <td>FormatBool(x)</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>Ftoa32(x, f, p)</td> <td>FormatFloat(float64(x), f, p, 32)</td></tr>
<tr><td>Ftoa64(x, f, p)</td> <td>FormatFloat(x, f, p, 64)</td></tr>
<tr><td>FtoaN(x, f, p, n)</td> <td>FormatFloat(x, f, p, n)</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>Itoa(x)</td> <td>Itoa(x)</td></tr>
<tr><td>Itoa(x)</td> <td>FormatInt(int64(x), 10)</td></tr>
<tr><td>Itoa64(x)</td> <td>FormatInt(x, 10)</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>Itob(x, b)</td> <td>FormatInt(int64(x), b)</td></tr>
<tr><td>Itob64(x, b)</td> <td>FormatInt(x, b)</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>Uitoa(x)</td> <td>FormatUint(uint64(x), 10)</td></tr>
<tr><td>Uitoa64(x)</td> <td>FormatUint(x, 10)</td></tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr><td>Uitob(x, b)</td> <td>FormatUint(uint64(x), b)</td></tr>
<tr><td>Uitob64(x, b)</td> <td>FormatUint(x, b)</td></tr>
</tbody></table>

_업데이트_:
`go` `fix`를 실행하면 변경 사항의 영향을 받는 거의 모든 코드가 업데이트됩니다.
\
§ `Atoi`는 유지되지만 `Atoui`와 `Atof32`는 유지되지 않으므로,
수동으로 추가해야 하는 형변환(cast)이 필요할 수 있습니다. `go` `fix` 도구가 이에 대해 경고를 표시합니다.

### 템플릿 패키지 {#templates}

`template` 및 `exp/template/html` 패키지가 [`text/template`](/pkg/text/template/)와 [`html/template`](/pkg/html/template/)로 이동되었습니다.
더욱 중요한 점은, 이 패키지들의 인터페이스가 단순화되었다는 것입니다.
템플릿 언어는 동일하지만 "템플릿 세트(template set)"라는 개념이 사라졌으며, 이에 따라 패키지의 함수와 메서드들이 변경되었으며 많은 부분이 삭제되었습니다.

`set` 대신 `Template` 객체는 여러 개의 이름 지정된 템플릿 정의를 포함할 수 있으며, 결과적으로 템플릿 호출을 위한 네임스페이스를 구축하게 됩니다. 템플릿은 자신과 연관된 다른 모든 템플릿을 호출할 수 있지만, 오직 연관된 템플릿들만 호출할 수 있습니다. 템플릿을 연관시키는 가장 간단한 방법은 함께 파싱하는 것이며, 이는 새로운 패키지 구조 덕분에 더욱 쉬워졌습니다.

_업데이트_:
임포트(imports)는 fix 도구에 의해 업데이트됩니다.
단일 템플릿 사용의 경우 대체로 영향을 받지 않습니다.
여러 템플릿을 함께 사용하는 코드는 수동으로 업데이트해야 합니다.
`text/template` 문서의 [예제](/pkg/text/template/#pkg-examples)가 가이드가 될 수 있습니다.

### testing 패키지 {#testing}

`testing` 패키지에는 벤치마크 함수에 인자로 전달되는 `B` 타입이 있습니다.
Go 1에서 `B`에는 `T`와 유사한 새로운 메서드들이 추가되어, 로그 기록 및 실패 보고가 가능해졌습니다.

{{code "/doc/progs/go1.go" `/func.*Benchmark/` `/^}/`}}

_업데이트_:
기존 코드는 영향을 받지 않지만, `println` 또는 `panic`을 사용하는 벤치마크는 새로운 메서드를 사용하도록 업데이트해야 합니다.

### testing/script 패키지 {#testing_script}

`testing/script` 패키지가 삭제되었습니다. 이는 불필요한 잔재였습니다.

_업데이트_:
영향을 받는 코드는 없을 것으로 보입니다.

### unsafe 패키지 {#unsafe}

Go 1에서는 `unsafe.Typeof`, `unsafe.Reflect`, `unsafe.Unreflect`, `unsafe.New`, 그리고 `unsafe.NewArray` 함수가 제거되었습니다. 이 함수들은 [`reflect`](/pkg/reflect/) 패키지에서 제공하는 더 안전한 기능들과 중복되었습니다.

_업데이트_:
이 함수들을 사용하는 코드는 [`reflect`](/pkg/reflect/) 패키지를 사용하도록 다시 작성해야 합니다.
[encoding/gob](/change/2646dc956207) 및 [protocol buffer library](https://code.google.com/p/goprotobuf/source/detail?r=5340ad310031)의 변경 사항이 예시로서 도움이 될 수 있습니다.

### url 패키지 {#url}

Go 1에서 [`url.URL`](/pkg/net/url/#URL) 타입의 여러 필드가 제거되거나 변경되었습니다.

[`String`](/pkg/net/url/#URL.String) 메서드는 이제 `URL`의 모든 필드를 필요에 따라 사용하여 인코딩된 URL 문자열을 예측 가능한 방식으로 다시 생성합니다. 또한 결과 문자열에서 비밀번호는 더 이상 이스케이프 처리되지 않습니다.

`Raw` 필드가 제거되었습니다. 대부분의 경우 `String` 메서드를 대신 사용할 수 있습니다.

기존의 `RawUserinfo` 필드는 [`*net.Userinfo`](/pkg/net/url/#Userinfo) 타입인 `User` 필드로 대체되었습니다. 이 타입의 값은 새로운 [`net.User`](/pkg/net/url/#User) 및 [`net.UserPassword`](/pkg/net/url/#UserPassword) 함수를 사용하여 생성할 수 있습니다. `EscapeUserinfo` 및 `UnescapeUserinfo` 함수 또한 삭제되었습니다.

`RawAuthority` 필드가 삭제되었습니다. 동일한 정보를 `Host` 및 `User` 필드에서 확인할 수 있습니다.

`RawPath` 필드와 `EncodedPath` 메서드가 제거되었습니다. 루트가 지정된 URL(스키마 뒤에 슬래시가 오는 경우)의 경로 정보는 이제 `Path` 필드에서 디코딩된 형태로만 사용할 수 있습니다.
간혹 디코딩 과정에서 손실된 정보를 얻기 위해 인코딩된 데이터가 필요할 수 있습니다. 이러한 경우에는 URL을 생성하는 데 사용된 원본 데이터에 접근하여 처리해야 합니다.

`"mailto:dev@golang.org?subject=Hi"`와 같이 루트가 없는 경로를 가진 URL 또한 다르게 처리됩니다. `OpaquePath` 불리언 필드가 삭제되었으며, 이러한 URL의 인코딩된 경로를 저장하기 위해 새로운 `Opaque` 문자열 필드가 도입되었습니다. Go 1에서, 언급된 URL은 다음과 같이 파싱됩니다:

```go
URL{
	        Scheme: "mailto",
	        Opaque: "dev@golang.org",
	        RawQuery: "subject=Hi",
	    }
```

`URL`에 새로운 [`RequestURI`](/pkg/net/url/#URL.RequestURI) 메서드가 추가되었습니다.

`ParseWithReference` 함수가 `ParseWithFragment`로 이름이 변경되었습니다.

_업데이트_:
이전 필드를 사용하는 코드는 컴파일에 실패하며, 수동으로 업데이트해야 합니다.
시맨틱 변경 사항으로 인해 수정 도구(fix tool)를 통한 자동 업데이트가 어렵습니다.

## go 명령어 {#cmd_go}

Go 1은 Go 패키지와 명령어를 가져오고, 빌드하고, 설치하기 위한 도구인 [go 명령어](/cmd/go/)를 도입합니다. `go` 명령어는 makefile을 사용하는 대신 Go 소스 코드를 사용하여 의존성을 찾고 빌드 조건을 결정합니다. 대부분의 기존 Go 프로그램은 더 이상 빌드를 위해 makefile을 필요로 하지 않습니다.

`go` 명령어에 대한 기초 내용은 [How to Write Go Code](/doc/code.html)를, 상세 내용은 [go command documentation](/cmd/go/)을 참조하십시오.

_업데이트_:
Go 프로젝트의 기존 makefile 기반 빌드 인프라(`Make.pkg`, `Make.cmd` 등)에 의존하는 프로젝트는 Go 코드를 빌드하기 위해 `go` 명령어를 사용하는 방식으로 전환해야 하며, 필요한 경우 보조 빌드 작업을 수행하도록 makefile을 다시 작성해야 합니다.

## cgo 명령 {#cmd_cgo}

Go 1에서 [cgo 명령어](/cmd/cgo)는 `//export` 라인이 포함된 패키지를 위해 생성되는 별도의 `_cgo_export.h` 파일을 사용합니다. 이제 `_cgo_export.h` 파일은 C 프리앰블(preamble) 주석으로 시작하므로, 내보내기(exported)된 함수 정의에서 그곳에 정의된 타입을 사용할 수 있습니다. 이는 프리앰블이 여러 번 컴파일되는 결과를 초래하므로, `//export`를 사용하는 패키지는 C 프리앰블에 함수 정의나 변수 초기화를 넣어서는 안 됩니다.

## 패키지 릴리스 {#releases}

Go 1과 관련된 가장 중요한 변화 중 하나는 미리 패키징되어 다운로드 가능한 배포판을 제공한다는 점입니다.
이 배포판들은 다양한 아키텍처와 운영 체제(Windows 포함) 조합으로 제공되며, 지원 목록은 계속해서 늘어날 예정입니다.
설치에 관한 자세한 내용은 [시작하기](/doc/install) 페이지에 설명되어 있으며, 배포판 목록은 [다운로드 페이지](/dl/)에서 확인할 수 있습니다.
