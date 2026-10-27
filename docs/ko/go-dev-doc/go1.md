## Go 1 소개 {#introduction}

이 문서는 Go 1 버전의 소개를 제공합니다.

Go 버전 1, Go 1로 약칭되는 이 버전은 안정적인 제품, 프로젝트 및 출판물을 만들기 위한 견고한 기반을 제공하는 언어와 핵심 라이브러리 세트를 정의합니다.

Go 1의 주요 목표는 사용자를 위한 안정성을 확보하는 것입니다. 사용자는 Go 프로그램을 작성하고, 그 프로그램이 수년 동안 변경 없이 컴파일 및 실행될 것이라고 예상해야 합니다. 여기에는 Google App Engine과 같은 프로덕션 환경도 포함됩니다. 마찬가지로, 사용자는 Go에 대한 책을 작성하고, 해당 책이 어떤 Go 버전을 설명하는지 명확하게 밝히고, 해당 버전 번호가 훨씬 더 나중에 여전히 유효함을 보장해야 합니다.

코드가 Go 1에서 컴파일되면, 몇 가지 예외 외에는 해당 버전을 통해 계속 컴파일되고 실행될 것입니다. Go 버전 1.1, 1.2 등과 같이 업데이트 및 버그 수정 사항을 적용하더라도 마찬가지입니다.
[Go 1 호환성 문서](go1compat.html)는 호환성 지침에 대해 더 자세히 설명합니다.

Go 1은 현재 Go 언어의 모습을 반영한 것이며, 언어 자체의 근본적인 재설계는 아닙니다. 새로운 기능 설계를 피하고, 대신 문제와 불일치를 정리하고, 이식성을 개선하는 데 중점을 두었습니다. Go 언어와 패키지에 대해 오랫동안 고려하고 프로토타입을 만들었지만 아직 출시하지 않은 변경 사항이 몇 가지 있습니다. 이는 상당한 변경 사항이며, 이전 버전과의 호환성이 떨어지기 때문입니다. Go 1은 이러한 변경 사항을 적용할 수 있는 기회를 제공하며, 이는 장기적으로 유용하지만, Go 1은 이전 프로그램과의 호환성을 깨뜨립니다. 다행히 `go` `fix` 도구를 사용하면 프로그램을 Go 1 표준에 맞게 업데이트하는 데 필요한 작업을 자동화할 수 있습니다.

이 문서는 Go 1의 주요 변경 사항을 설명하고, 기존 코드를 업데이트하는 프로그래머에게 영향을 미칩니다. 주요 참조점은 이전 버전인 r60 (r60.3으로 태그됨)입니다. 또한, r60에서 Go 1로 코드를 업데이트하는 방법을 설명합니다.

## 언어 변경 사항 {#language}

### 추가 {#append}

`append`는 미리 정의된 변형 함수로서, 슬라이스에 요소를 추가하여 쉽게 확장할 수 있도록 합니다.
일반적인 사용 사례는 출력 생성을 할 때, 바이트 슬라이스의 끝에 바이트를 추가하는 것입니다.
그러나 `append`는 `[]byte`에 문자열을 추가하는 방법을 제공하지 않았기 때문에, 이것 또한 흔한 경우입니다.

```markdown
{{code "/doc/progs/go1.go" `/greeting := ..byte/` `/append.*hello/`}}
```

비슷한 속성을 가진 `copy`와 마찬가지로, Go 1에서는 문자열을 바이트 슬라이스에 직접 추가(바이트 단위)하도록 허용하여, 문자열과 바이트 슬라이스 간의 격차를 줄입니다.
이제 변환이 더 이상 필요하지 않습니다:

```markdown
{{code "/doc/progs/go1.go" `/append.*world/`}}
```

_업데이트_:
이것은 새로운 기능이므로 기존 코드는 수정할 필요가 없습니다.

### 닫기 {#close}

`close` 선언된 함수는 송자가 더 이상 값을 보내지 않음을 알리는 메커니즘을 제공합니다.
이는 채널을 통한 `for` `range` 루프의 구현에 중요하며, 다른 상황에서도 유용합니다.
일부는 설계에 의해, 그리고 다른 경우에는 발생할 수 있는 경쟁 조건 때문에,
이는 채널을 통해 송하는 goroutine에만 사용하도록 의도되었으며, 데이터를 수신하는 goroutine에는 사용하지 않아야 합니다.
그러나 Go 1 이전에는 `close`가 올바르게 사용되고 있는지 컴파일 시간에 검사하는 기능이 없었습니다.

이를 해결하기 위해, Go 1은 수신 전용 채널에서 `close`를 사용하는 것을 금지합니다.
이러한 채널을 닫으려고 시도하면, 컴파일 시간 오류가 발생합니다.

```markdown
{{code "/doc/progs/go1.go" `/STARTCLOSE/` `/ENDCLOSE/`}}
```

_업데이트_:
기존 코드가 수신 전용 채널을 닫으려고 시도하는 경우, Go 1 이전부터도 잘못되었으며 수정이 필요합니다. 컴파일러는 이제 이러한 코드를 거부합니다.

### 복합 리터럴 {#literals}

Go 1에서 배열, 슬라이스, 또는 맵 유형의 복합 리터럴은 요소의 초기화가 포인터 유형인 경우, 요소의 유형 지정 사항을 생략할 수 있습니다. 이 예제의 네 가지 초기화 모두 유효합니다. 마지막 초기화는 Go 1 이전에는 유효하지 않았습니다.

{{code "/doc/progs/go1.go" `/type Date struct/` `/STOP/`}}

_업데이트_:
이 변경은 기존 코드에 영향을 미치지 않지만, 기존 소스에 적용되는 `gofmt -s` 명령은 (그리고 다른 것들 역시) 허용되는 경우에 따라 명시적인 요소 유형을 제거합니다.

### 초기화 시 goroutine 사용 {#init}

구 버전의 언어는 초기화 중에 실행되는 `go` 문이 고루틴을 생성하지만, 이러한 고루틴이 실행되기 시작하는 것은 전체 프로그램의 초기화가 완료될 때까지 지연된다고 정의했습니다.
이것은 많은 곳에서 비효율성을 야기했으며, 실질적으로 `init` 구문의 유용성을 제한했습니다.
만약 다른 패키지가 초기화 중에 라이브러리를 사용할 수 있다면, 라이브러리는 고루틴을 사용하지 않도록 강제되었습니다.
이 설계는 단순성과 안전을 위해 이루어졌지만,
언어에 대한 우리의 확신이 커짐에 따라, 이것은 불필요하게 느껴졌습니다.
초기화 중에 고루틴을 실행하는 것은, 정상적인 실행 중에 고루틴을 실행하는 것만큼 복잡하거나 위험하지 않습니다.

Go 1에서, goroutine을 사용하는 코드는 `init` 루틴과 전역 초기화 표현식에서 호출할 수 있으며, 이를 통해 데드락이 발생하지 않습니다.

```markdown
{{code "/doc/progs/go1.go" `/PackageGlobal/` `/^}/`}}
```

_업데이트:_
이것은 새로운 기능이므로 기존 코드는 수정할 필요가 없습니다.
그러나 `main` 함수가 실행되기 전에 goroutine이 시작되지 않는 코드는 문제가 발생할 수 있습니다.
표준 저장소에는 그러한 코드가 없었습니다.

### `rune` 타입 {#rune}

언어 사양은 `int` 형이 32비트 또는 64비트 폭으로 지정할 수 있도록 허용하지만, 현재 구현에서는 64비트 플랫폼에서도 `int`를 32비트로 설정합니다.
64비트 플랫폼에서는 `int`를 64비트로 사용하는 것이 더 바람직합니다.
(대규모 슬라이스를 인덱싱하는 데 중요한 결과가 있습니다.)
그러나 이 변경은 이전 언어로 유니코드 문자를 처리할 때 공간 낭비를 초래합니다. 왜냐하면 `int` 형은 유니코드 코드 포인트를 저장하는 데에도 사용되었기 때문입니다. `int`가 32비트에서 64비트로 변경되면, 각 코드 포인트는 추가 32비트의 저장 공간을 낭비하게 됩니다.

64비트 `int`로 변경하는 것을 가능하게 하기 위해,
Go 1은 개별 유니코드 코드 포인트를 나타내는 새로운 기본 유형인 `rune`을 도입합니다.
`byte`가 `uint8`의 별칭인 것과 유사하게,
이는 `int32`의 별칭입니다.

문자 리터럴, 예: `'a'`, `'語'`, 및 `'\u0345'`는 이제 기본 유형이 `rune`이며, 이는 `1.0`의 기본 유형이 `float64`와 유사합니다.
문자 상수에 초기화된 변수는 따라서 `rune` 유형을 가지게 되지만, 그렇지 않은 경우에만 다른 유형이 지정될 수 있습니다.

라이브러리는 적절한 경우 `rune`를 사용하여 `int` 대신 사용하도록 업데이트되었습니다. 예를 들어, `unicode.ToLower` 및 관련 함수는 이제 `rune`를 입력으로 받고 반환합니다.

```
{{code "/doc/progs/go1.go" `/STARTRUNE/` `/ENDRUNE/`}}
```

_업데이트:_
대부분의 소스 코드는 영향을 받지 않습니다. 왜냐하면 `:=` 초기화에서 발생하는 타입 추론이 새로운 타입을 은밀하게 도입하고, 그 이후에 해당 타입이 적용되기 때문입니다.
일부 코드에서는 간단한 변환으로 해결할 수 있는 타입 오류가 발생할 수 있습니다.

### 오류 타입 {#error}

Go 1에서는 새로운 내장 타입인 `error`를 도입했으며, 다음과 같이 정의됩니다:

```
type 오류 인터페이스 {
    Error(): string
}
```

이 유형의 결과는 모두 패키지 라이브러리에 포함되어 있으므로,
이는 아래에 설명되어 있습니다 [오류](#errors).

### 지도에서 삭제하기 {#delete}

```
delete("key", "value")
```

| 메서드 | 설명 |
|---|---|
| `delete(key, value)` | 지정된 키와 값을 지도에서 제거합니다. |

옛 언어에서는 맵 `m`에서 키 `k`에 해당하는 항목을 삭제하려면 다음과 같은 문을 작성했습니다.

m[k] = value, false

이 구문은 특이한 특별한 경우였으며, 유일한 두-에서-하나 할당 방식이었습니다.
이는 일반적으로 무시되는 값을 전달해야 했으며, 이 값은 평가되지만 버려졌습니다.
또한 거의 항상 `false` 상수인 부울 값을 전달해야 했습니다.
이것은 작동했지만, 어색하고 논쟁의 대상이 되었습니다.

Go 1에서는 해당 구문이 사라졌습니다. 대신 새로운 내장 함수인 `delete`가 있습니다.

```markdown
## 삭제 (m, k)
```

이 표현식 `m[k]`에 의해 반환된 맵 항목을 삭제합니다.
반환 값이 없습니다. 존재하지 않는 항목을 삭제하는 것은 아무런 영향이 없습니다.

_업데이트_:
`go` `fix` 명령어를 실행하면 `m[k] = value, false`와 같은 표현을 `delete(m, k)`로 변환합니다. 이는 `false`가 미리 정의된 부울 상수를 참조하고, 프로그램에서 무시해도 안전하게 버릴 수 있는 값임을 명확히 할 때 작동합니다.
이 수정 도구는 프로그래머가 검토할 수 있도록 다른 문법 사용을 강조 표시합니다.

### 맵을 통한 반복 {#iteration}

```go
package main

import "fmt"

func main() {
	myMap := map[string]int{
		"apple":  1,
		"banana": 2,
		"orange": 3,
	}

	for key, value := range myMap {
		fmt.Printf("Key: %s, Value: %d\n", key, value)
	}
}
```

구 버전의 언어 사양은 맵에 대한 반복 순서를 정의하지 않았으며, 실제로 하드웨어 플랫폼마다 달랐습니다.
이는 맵을 반복하는 테스트를 불안정하고 이식성이 없게 만들었으며,
결과적으로 테스트는 한 기계에서는 항상 통과할 수 있지만 다른 기계에서는 실패할 수 있는 불쾌한 특성을 가졌습니다.

Go 1에서 `for` `range` 문을 사용하여 맵을 반복할 때, 요소가 방문되는 순서는 예측할 수 없습니다. 즉, 동일한 맵을 여러 번 반복해도 동일한 순서로 요소가 방문되지 않을 수 있습니다.

따라서, 코드는 요소가 특정 순서로 방문된다고 가정하지 않아야 합니다.

이 변경 사항은 반복 순서를 의존하는 코드가 쉽게 깨고, 문제가 발생하기 전에 수정될 가능성이 매우 높다는 것을 의미합니다.

더욱 중요한 점은, 이 변경 사항이 `map` 구현이 프로그램이 `range` 루프를 사용하여 `map`에서 요소를 선택하는 경우에도 더욱 효과적으로 `map`을 균형 있게 유지할 수 있도록 합니다.

```
{{code "/doc/progs/go1.go" `/일요일/` `/^	}/`}}
```

_업데이트_:
이것은 도구가 도움을 줄 수 없는 변경 사항입니다. 대부분의 기존 코드는 영향을 받지 않지만, 일부 프로그램이 중단되거나 예상치 못한 동작을 할 수 있습니다. 따라서 맵에 대한 모든 범위 문을 수동으로 확인하여 반복 순서에 의존하지 않는지 확인하는 것이 좋습니다. 표준 저장소에는 몇 가지 예시가 있었으며, 이들은 수정되었습니다.

참고로, 반복 순서에 의존하는 것은 이미 잘못된 것이었고, 이는 명시되지 않았습니다. 이 변경 사항은 이러한 예측 불가능성을 공식화합니다.

### 여러 변수 할당 {#multiple_assignment}

언어 사양은 오랫동안 보장해 왔습니다. 즉, 할당 연산에서
오른쪽 피연산은 항상 먼저 평가되고, 그 다음에 왼쪽 피연산이 할당됩니다.
예측 가능한 동작을 보장하기 위해,
Go 1은 사양을 더욱 명확하게 정의합니다.

만약 할당 문장의 왼쪽에는 함수 호출이나 배열 인덱싱과 같이 평가가 필요한 표현식이 포함되어 있는 경우, 이러한 표현식들은 변수에 값을 할당하기 전에 일반적인 왼쪽에서 오른쪽 규칙에 따라 먼저 평가됩니다. 모든 것이 평가되면, 실제 할당은 왼쪽에서 오른쪽 순서대로 진행됩니다.

이 예제들은 동작 방식을 보여줍니다.

```markdown
{{code "/doc/progs/go1.go" `sa := 2`}}
```

_업데이트_:
이 변경 사항은 도구를 사용하여 수정할 수 없지만, 오류 발생 가능성은 낮습니다.
표준 저장소의 코드는 이 변경 사항으로 인해 손상되지 않았으며, 이전의 명확하지 않은 동작에 의존하는 코드는 이미 잘못되었습니다.

### 반환 값 및 섀도 변수 {#shadowing}

흔한 실수는 동일한 이름을 가진 변수에 할당한 후 `return` (인자를 없이) 사용하는 것입니다. 이때, 할당된 변수와 결과 변수의 이름이 같지만, 실제로는 다른 변수일 수 있습니다.

이러한 상황을 _섀도잉_이라고 합니다. 즉, 동일한 이름으로 내부 범위에서 선언된 다른 변수에 의해 결과 변수가 가려집니다.

함수에서 명명된 반환 값을 사용하는 경우,
Go 1 컴파일러는 반환 문이 명명된 반환 값을 가리키는 경우에 인수가 없는 반환 문을 금지합니다.
(이는 여전히 탐구 중인 영역이므로 사양의 일부가 아닙니다.
상황은 컴파일러가 명시적인 반환 문으로 끝나는 함수를 거부하는 것과 유사합니다.)

이 함수는 암시적으로 반환 값을 반환하며, 컴파일러에 의해 거부됩니다:

```markdown
```go
package main

import "fmt"

func Bug() {
	fmt.Println("This is a bug")
}
```

_업데이트_:
이러한 방식으로 반환 값을 가리는 코드는 컴파일러에 의해 거부될 것이며, 수동으로 수정해야 합니다.
표준 저장소에서 발생한 몇 가지 사례는 대부분 버그였습니다.

### 비공개 필드를 가진 구조체 복사 {#비공개}

오래된 언어는 다른 패키지에 속한, 비공개 필드를 포함하는 구조체의 값을 복사하는 패키지가 허용하지 않았습니다.

그러나, 메서드 리시버에 대해서는 예외가 있었습니다.
또한, `copy` 및 `append` 함수의 구현은 이러한 제약을 준수하지 않았습니다.

Go 1은 다른 패키지에서 가져온 구조체의 값을 복사할 수 있도록 허용합니다. 이 기능은 불투명 필드를 포함하는 구조체의 값을 복사할 수 있습니다.
이 변경 사항은 새로운 유형의 API를 도입합니다: 패키지는 포인터 또는 인터페이스를 사용하지 않고도 불투명한 값을 반환할 수 있습니다.
`time.Time` 및 `reflect.Value`의 새로운 구현은 이러한 새로운 속성을 활용하는 유형의 예입니다.

예를 들어, 패키지 `p`가 다음과 같은 정의를 포함하고 있다고 가정합니다.

```markdown
```type Struct struct {
        Public int
        secret int
    }
    func NewStruct(a int) Struct {  // Note: not a pointer.
        return Struct{a, f(a)}
    }
    func (s Struct) String() string {
        return fmt.Sprintf("{%d (secret %d)}", s.Public, s.secret)
    }
```

이 패키지는 `p`를 가져올 때, `p.Struct`의 값을 자유롭게 할당하고 복사할 수 있습니다.

실제로는 내보내지지 않은 필드가 가져와서 할당되고 복사되지만, 클라이언트 코드는 이러한 필드를 인지하지 못합니다.

```
import "p"
```

```markdown
myStruct := p.NewStruct(23)
    copyOfMyStruct := myStruct
    fmt.Println(myStruct, copyOfMyStruct)
```

이것은 구조체의 비밀 필드가 새로운 값에 복사되었음을 보여줍니다.

_업데이트_:
이것은 새로운 기능이므로 기존 코드는 변경할 필요가 없습니다.

### 동등성 {#equality}

Go 1 이전에는 언어가 구조체 및 배열 값에 대한 동일성을 정의하지 않았습니다.
이는 다음과 같은 의미를 가집니다.
구조체 및 배열은 맵 키로 사용할 수 없었습니다.
반면에 Go는 함수 및 맵 값에 대한 동일성을 정의했습니다.
함수 동일성은 캡처와 함께 문제가 있었습니다.
(두 캡처는 언제 동일한가?)
반면 맵 동일성은 맵의 내용을 비교하는 대신 포인터를 비교했으며, 이는 일반적으로 사용자가 원하는 것이 아니었습니다.

Go 1은 이러한 문제들을 해결했습니다.

첫째, 구조체와 배열은 동등성과 불등성을 비교할 수 있습니다 (`==` 및 `!=`),
따라서 요소별 비교를 사용하여 정의된 요소로 구성된 경우, 맵 키로 사용할 수 있습니다.

```
{{code "/doc/progs/go1.go" `/type Day struct/` `/Printf/`}}
```

둘째, Go 1에서 함수 값에 대한 동등성 정의가 제거되었습니다.
`nil`과 비교할 때만 적용됩니다.
마지막으로, 맵의 동등성도 제거되었습니다.
`nil`과 비교할 때만 적용됩니다.

참고: 슬라이스에 대한 등호는 여전히 정의되지 않았으며, 이 경우 계산은 일반적으로 불가능합니다. 또한, 구조체 및 배열에 대한 정렬된 비교 연산자(`< <= > >=`)는 여전히 정의되지 않았습니다.

_업데이트_:
구조체 및 배열의 동일성 비교는 새로운 기능이므로 기존 코드는 수정할 필요가 없습니다.
함수 또는 맵의 동일성을 기반으로 하는 기존 코드는 컴파일러에서 거부되며, 수동으로 수정해야 합니다.
몇몇 프로그램에만 영향을 미치지만, 수정에는 일부 재설계가 필요할 수 있습니다.

## 패키지 계층 구조 {#packages}

```go
package mypackage

import "fmt"

func MyFunction() {
	fmt.Println("Hello from mypackage!")
}
```

## Subpackages

```go
package subpackage

import "fmt"

func SubFunction() {
	fmt.Println("Hello from subpackage!")
}
```

## Example usage

```go
package main

import (
	"fmt"
	"mypackage"
)

func main() {
	fmt.Println(mypackage.MyFunction())
}
```

Go 1은 이전 표준 라이브러리의 많은 결점을 해결하고, 여러 패키지를 정리하여 내부적으로 일관성을 높이고, 이식성을 향상시킵니다.

이 섹션에서는 Go 1에서 패키지가 어떻게 재구성되었는지 설명합니다.
일부는 이동되었습니다, 일부는 이름이 변경되었습니다, 일부는 삭제되었습니다.
새로운 패키지는 후속 섹션에서 설명합니다.

### 패키지 계층 구조 {#hierarchy}

Go 1은 관련된 항목을 하위 디렉토리에 그룹화하여 패키지 계층 구조를 재구성했습니다. 예를 들어, `utf8` 및 `utf16`은 이제 `unicode`의 하위 디렉토리에 위치합니다.
또한, [일부 패키지](#subrepo)는 `code.google.com/p/go`의 하위 저장소로 이동했으며, [다른 패키지](#deleted)는 완전히 삭제되었습니다.

```
<table class="codetable" frame="border" summary="이동된 패키지">
<colgroup align="left" width="60%"></colgroup>
<colgroup align="left" width="40%"></colgroup>
<tbody>
<tr align="left">
<th>이전 경로</th>
<th>새로운 경로</th>
</tr>
<tr align="left">
<td colspan="2"><hr></hr></td>
</tr>
<tr align="left">
<td>asn1</td>
<td>encoding/asn1</td>
</tr>
<tr align="left">
<td>csv</td>
<td>encoding/csv</td>
</tr>
<tr align="left">
<td>gob</td>
<td>encoding/gob</td>
</tr>
<tr align="left">
<td>json</td>
<td>encoding/json</td>
</tr>
<tr align="left">
<td>xml</td>
<td>encoding/xml</td>
</tr>
<tr align="left">
<td colspan="2"><hr></hr></td>
</tr>
<tr align="left">
<td>exp/template/html</td>
<td>html/template</td>
</tr>
<tr align="left">
<td colspan="2"><hr></hr></td>
</tr>
<tr align="left">
<td>big</td>
<td>math/big</td>
</tr>
<tr align="left">
<td>cmath</td>
<td>math/cmplx</td>
</tr>
<tr align="left">
<td>rand</td>
<td>math/rand</td>
</tr>
<tr align="left">
<td colspan="2"><hr></hr></td>
</tr>
<tr align="left">
<td>http</td>
<td>net/http</td>
</tr>
<tr align="left">
<td>http/cgi</td>
<td>net/http/cgi</td>
</tr>
<tr align="left">
<td>http/fcgi</td>
<td>net/http/fcgi</td>
</tr>
<tr align="left">
<td>http/httptest</td>
<td>net/http/httptest</td>
</tr>
<tr align="left">
<td>http/pprof</td>
<td>net/http/pprof</td>
</tr>
<tr align="left">
<td>mail</td>
<td>net/mail</td>
</tr>
<tr align="left">
<td>rpc</td>
<td>net/rpc</td>
</tr>
<tr align="left">
<td>rpc/jsonrpc</td>
<td>net/rpc/jsonrpc</td>
</tr>
<tr align="left">
<td>smtp</td>
<td>net/smtp</td>
</tr>
<tr align="left">
<td>url</td>
<td>net/url</td>
</tr>
<tr align="left">
<td colspan="2"><hr></hr></td>
</tr>
<tr align="left">
<td>exec</td>
<td>os/exec</td>
</tr>
<tr align="left">
<td colspan="2"><hr></hr></td>
</tr>
<tr align="left">
<td>scanner</td>
<td>text/scanner</td>
</tr>
<tr align="left">
<td>tabwriter</td>
<td>text/tabwriter</td>
</tr>
<tr align="left">
<td>template</td>
<td>text/template</td>
</tr>
<tr align="left">
<td>template/parse</td>
<td>text/template/parse</td>
</tr>
<tr align="left">
<td colspan="2"><hr></hr></td>
</tr>
<tr align="left">
<td>utf8</td>
<td>unicode/utf8</td>
</tr>
<tr align="left">
<td>utf16</td>
<td>unicode/utf16</td>
</tr>
</tbody>
</table>
```

참고: 이전 `cmath` 및 `exp/template/html` 패키지의 패키지 이름이 `cmplx` 및 `template`로 변경되었습니다.

_업데이트_:
`go fix` 명령어를 실행하면, 표준 저장소 내에 남아있는 패키지의 모든 임포트 및 패키지 이름을 업데이트합니다. 더 이상 표준 저장소에 없는 패키지를 임포트하는 프로그램은 수동으로 수정해야 합니다.

### 패키지 트리 탐색 {#exp}

이러한 패키지는 표준화되지 않았기 때문에, `exp` 디렉터리에 있는 패키지는 표준 Go 1 릴리스 배포판에는 포함되지 않지만, [저장소](https://code.google.com/p/go/)에는 소스 코드 형태로 제공됩니다. 이를 사용하고자 하는 개발자는 이 저장소를 활용할 수 있습니다.

Go 1 출시 시, 여러 패키지가 `exp` 아래로 이동했습니다:

- `ebnf`
  - `html`
  - `go/types`

(<sup>†</sup>`EscapeString` 및 `UnescapeString` 유형은 `html` 패키지에 남아 있습니다.)

모든 패키지는 동일한 이름으로 제공되며, 접두사로 `exp/`가 붙어 있습니다: `exp/ebnf` 등.

```markdown
# 변경 사항

*   `utf8.String` 타입이 `exp/utf8string` 패키지로 이동되었습니다.

## 테이블 예시

| 열 1 | 열 2 | 열 3 |
|---|---|---|
| 데이터 1 | 데이터 2 | 데이터 3 |
| 데이터 4 | 데이터 5 | 데이터 6 |

## 목록 예시

*   항목 1
*   항목 2
*   항목 3

## 코드 예시

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, world!")
}
```

## 링크 예시

[Google](https://www.google.com)

## 코드 펜스 예시

```python
def hello_world():
    print("Hello, world!")
```
```

마지막으로, `gotype` 명령은 이제 `exp/gotype`에 위치하고,
`ebnflint`은 이제 `exp/ebnflint`에 위치합니다.
만약 설치되어 있다면, 이제 `$GOROOT/bin/tool`에 위치합니다.

_업데이트_:
`exp` 패키지를 사용하는 코드는 수동으로 업데이트해야 하거나, `exp`가 설치된 환경에서 컴파일해야 합니다.
`go`의 `fix` 도구나 컴파일러는 이러한 사용에 대해 오류를 표시합니다.

### 패키지 트리: 이전 버전 {#old}

이러한 패키지는 더 이상 사용되지 않으므로, `old` 디렉터리에 있는 패키지는 표준 Go 1 릴리스 배포판에는 포함되지 않지만, 이를 사용하려는 개발자는 소스 코드 형태로 사용할 수 있습니다.

새로운 위치에 있는 패키지들은 다음과 같습니다:

- `old/netchan`

_업데이트_:
현재 `old` 패키지를 사용하는 코드는 수동으로 업데이트해야 하거나, `old`가 있는 설치에서 컴파일해야 합니다.
`go`의 `fix` 도구가 이러한 사용에 대해 경고합니다.

### 삭제된 패키지 {#deleted}

Go 1에서 여러 패키지를 완전히 제거합니다:

- `container/vector`
  - `exp/datafmt`
  - `go/typechecker`
  - `old/regexp`
  - `old/template`
  - `try`

```markdown
# 제목

## 서브 제목

**표:**

| 열 1 | 열 2 |
|---|---|
| 데이터 1 | 데이터 2 |
| 데이터 3 | 데이터 4 |

* 항목 1
* 항목 2

```

## 코드 예제

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, world!")
}
```

## 링크

[링크 텍스트](https://example.com)

## 목록

* 항목 1
* 항목 2

## 코드 블록

```
print("Hello")
```

## 외부 명령어

`gotry`

_업데이트_:
`container/vector`을 사용하는 코드는 직접적인 슬라이스를 사용하는 것으로 업데이트해야 합니다. 다음의 Go
언어 커뮤니티 위키([https://code.google.com/p/go-wiki/wiki/SliceTricks](https://code.google.com/p/go-wiki/wiki/SliceTricks))에서 몇 가지 제안을 참고하십시오.
다른 패키지를 사용하는 코드는 거의 없을 것입니다.

### 서브 리포지토리로의 패키지 이동 {#subrepo}

Go 1에서 여러 패키지를 다른 저장소로 이동했습니다. 일반적으로 [Go의 메인 저장소](https://code.google.com/p/go/)의 하위 저장소입니다.
다음 표는 이전 및 새로운 import 경로를 나열합니다:

``` Markdown
<table class="codetable" frame="border" summary="Sub-repositories">
<colgroup align="left" width="40%"></colgroup>
<colgroup align="left" width="60%"></colgroup>
<tbody><tr>
<th align="left">Old</th>
<th align="left">New</th>
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
```

_업데이트_:
`go fix` 명령어를 실행하면 이러한 패키지의 import을 새로운 import 경로를 사용하도록 업데이트합니다.
이 패키기에 의존하는 설치는 `go get` 명령어를 사용하여 설치해야 합니다.

## 라이브러리의 주요 변경 사항 {#major}

이 섹션에서는 핵심 라이브러리에 대한 주요 변경 사항을 설명합니다. 이러한 변경 사항은 가장 많은 프로그램에 영향을 미칩니다.

### 오류 유형 및 errors 패키지 {#errors}

```go
package main

import (
	"fmt"
	"log"
)

func main() {
	// 오류 발생 예시
	_, err := fmt.Errorf("failed to open file: %s", "myfile.txt")
	if err != nil {
		log.Println(err)
	}

	// 여러 오류 결합
	multiErr := fmt.Errorf("first error: %w\nsecond error: %w", err, err)
	log.Println(multiErr)

	// 사용자 정의 오류
	type MyError struct {
		Message string
		Code    int
	}

	func (e *MyError) Error() string {
		return fmt.Sprintf("MyError: %s (Code: %d)", e.Message, e.Code)
	}

	myErr := MyError{Message: "Something went wrong", Code: 500}
	err = myErr
	if err != nil {
		log.Println(err)
	}
}
```

`os.Error`의 위치는 주로 역사적인 이유입니다: 오류는 원래 `os` 패키지를 구현할 때 발생했고, 당시에는 운영체제와 관련된 것으로 보였습니다.
그 이후로 오류가 운영 체제보다 더 기본적인 개념임을 명확히 했습니다. 예를 들어, `os`에 의존하는 패키지(예: `syscall`)에서도 `Errors`를 사용하는 것이 좋겠습니다.
또한, `os`에 `Error`를 포함하면 원래는 존재하지 않아야 할 `os`에 대한 많은 의존성이 발생합니다.

Go 1은 내장된 `error` 인터페이스 타입과 별도의 `errors` 패키지(예: `bytes` 및 `strings`와 유사)를 도입하여 이러한 문제를 해결합니다. 이 패키지에는 유틸리티 함수가 포함되어 있습니다.
이는 `os.NewError`를 `[errors.New](pkg/errors/#New)`로 대체하여, 오류를 환경에서 더욱 중심적인 위치로 만듭니다.

따라서 널리 사용되는 `String` 메서드는 의도치 않게 `error` 인터페이스를 만족시키지 않습니다. `error` 인터페이스 대신 해당 메서드에 `Error`라는 이름을 사용합니다:

```
type 오류 인터페이스 {
    Error() string
}
```

`fmt` 라이브러리는 자동으로 `Error` 함수를 호출하여, `String` 함수도 이미 호출하는 것처럼, 오류 값을 쉽게 출력할 수 있도록 합니다.

```markdown
{{code "/doc/progs/go1.go" `/START ERROR EXAMPLE/` `/END ERROR EXAMPLE/`}}
```

모든 표준 패키지가 새로운 인터페이스를 사용하도록 업데이트되었습니다. 이전의 `os.Error`는 더 이상 사용되지 않습니다.

새로운 패키지, [`errors`](/pkg/errors/),에는 다음과 같은 함수가 포함되어 있습니다.

```
func New(text string) error
```

문자열을 오류로 변환하는 방법입니다. 이 기능은 이전의 `os.NewError` 기능을 대체합니다.

```markdown
{{code "/doc/progs/go1.go" `/ErrSyntax/`}}
```

_업데이트_:
`go` `fix`를 실행하면 변경 사항에 영향을 받는 대부분의 코드가 업데이트됩니다.
`String` 메서드를 사용하여 오류 유형을 정의하는 코드는 메서드 이름을 `Error`로 변경하여 수동으로 업데이트해야 합니다.

### 시스템 호출 오류 {#errno}

```c
#include <errno.h>
```

시스템 호출이 실패하면 `errno` 변수가 오류 코드와 함께 설정됩니다. 이 변수는 시스템 호출을 수행하는 운영 체제의 오류 코드에 대한 정보를 제공합니다. 예를 들어, 파일이 존재하지 않으면 `errno`가 `ENOENT`로 설정됩니다.

```c
#include <unistd.h>

int fd = open("myfile.txt", O_RDONLY);
if (fd == -1) {
  perror("open"); // 오류 메시지 출력
  exit(1);
}
```

`perror()` 함수는 `errno`의 값을 사용하여 오류 메시지를 표준 오류 스트림(stderr)에 출력합니다. 이 메시지는 오류의 원인에 대한 정보를 제공합니다.

## 오류 코드의 예

| 오류 코드 | 의미                                                                                                                                                                                                                              |
|---|---|
| `ENOENT` | 지정된 파일이나 디렉토리가 존재하지 않습니다.                                                                                                                                                                                              |
| `EACCES` | 접근 권한이 없습니다.                                                                                                                                                                                                                |
| `EPERM` | 권한이 없습니다.                                                                                                                                                                                                                      |
| `ENOMEM` | 메모리가 부족합니다.                                                                                                                                                                                                                  |

구형 `syscall` 패키지는 `os.Error` (그리고 거의 모든 것)가 등장하기 이전부터 존재했습니다.
이 패키지는 오류를 `int` 값으로 반환했습니다.
이에 따라 `os` 패키지는 이러한 오류 중 일부 (예: `EINVAL`)를 전달했지만, 각 플랫폼마다 다른 오류 집합을 사용했습니다.
이 동작은 불편하고 호환성이 떨어졌습니다.

Go 1에서는
[`syscall`](/pkg/syscall/)
패키지가 대신 시스템 호출 오류에 대해 `error`를 반환합니다.
Unix에서는 구현이 `syscall.Errno`
형식으로 이루어지며, 이 형식은 `error` 인터페이스를 만족하고 이전의 `os.Errno`를 대체합니다.

`os.EINVAL` 및 관련 기능에 영향을 미치는 변경 사항은
[다른 곳에서](#os) 설명되어 있습니다.

_업데이트_:
`go fix` 명령어를 실행하면 변경 사항에 영향을 받는 대부분의 코드가 업데이트됩니다.
어떤 경우든, 대부분의 코드는 `os` 패키지를 사용하는 것이 좋습니다.
따라서 `syscall` 대신 사용하면 영향을 받지 않습니다.

### 시간 {#time}

시간을 잘 다루는 것은 프로그래밍 언어에서 항상 어려운 과제입니다.
구 버전의 Go `time` 패키지는 `int64` 단위만 사용했으며,
실제 타입 안전성도 부족하고,
절대 시간과 기간을 구분하지 않았습니다.

따라서 Go 1 라이브러리의 가장 광범위한 변경 중 하나는 `time` 패키지의 완전한 재설계입니다.
`int64`로 표현되는 나노초 단위의 정수와, 시간을 나타내는 별도의 `*time.Time` 타입 대신, 다음과 같은 두 가지 기본 타입이 있습니다.
[`time.Time`](/pkg/time/#Time) (값이므로 `*`가 사라짐), 이는 특정 시점을 나타내며;
그리고 [`time.Duration`](/pkg/time/#Duration), 이는 간격을 나타냅니다.
두 타입 모두 나노초 해상도를 가집니다.
`Time`은 고대 과거와 먼 미래의 모든 시점을 나타낼 수 있으며, `Duration`은 플러스 또는 마이너스 약 290년 범위 내의 간격을 나타낼 수 있습니다.
이러한 타입에는 다양한 메서드와 함께 `time.Second`와 같은 유용한 미리 정의된 상수 간격도 있습니다.

다음과 같은 방법들이 있습니다:
[`Time.Add`](/pkg/time/#Time.Add),
이는 `Duration`을 `Time`에 더하는 기능이며,
[`Time.Sub`](/pkg/time/#Time.Sub),
이는 두 개의 `Time`을 빼서 `Duration`을 반환하는 기능입니다.

가장 중요한 의미적 변화는 유닉스 시점(1970년 1월 1일)이 이제는
유닉스를 언급하는 함수 및 메서드에만 관련이 있다는 것입니다:
[`time.Unix`](/pkg/time/#Unix)
과 [`Unix`](/pkg/time/#Time.Unix)
및 `Time` 유형의 [`UnixNano`](/pkg/time/#Time.UnixNano) 메서드.
특히,
[`time.Now`](/pkg/time/#Now)
는 유닉스 시점 이후의 나노초 수를 반환하는 대신,
구 버전의 API에서는 유닉스 시점 이후의 정수 나노초 수를 반환했습니다.

```markdown
```

새로운 타입, 메서드 및 상수는 `os`를 포함하여 `time`을 사용하는 모든 표준 패키지에 적용되었습니다. 여기에는 파일 타임스탬프를 나타내는 방식이 포함됩니다.

_업데이트_:
`go` `fix` 도구는 오래된 `time` 패키지의 많은 사용 사례를 새로운 유형과 메서드를 사용하여 업데이트합니다. 하지만 `1e9`와 같은 값을 나타내는 나노초/초와 같은 값은 대체하지 않습니다.
또한, 일부 값의 유형 변경으로 인해 `fix` 도구가 다시 작성한 일부 표현식은 추가적인 수동 편집이 필요할 수 있습니다. 이러한 경우, 재작성은 오래된 기능에 대한 올바른 함수 또는 메서드를 포함하지만, 잘못된 유형을 가질 수 있거나 추가 분석이 필요할 수 있습니다.

## 라이브러리의 미세 조정 {#minor}

*   변경 사항 요약
    *   [변경 사항 상세 내용](link_to_changes)
*   영향 받는 기능
    *   기능 A
    *   기능 B
*   사용 방법
    *   `library.update()`
    *   `library.configure()`
*   참고 자료
    *   [문서](link_to_documentation)
    *   [예제 코드](link_to_example)

이 섹션에서는 덜 자주 사용되는 패키지 또는 `go` `fix`를 실행해야 하는 것 외에 몇 가지 프로그램에만 영향을 미치는 변경 사항을 설명합니다. 여기에는 Go 1에 새로 추가된 패키지가 포함됩니다.
이러한 변경 사항은 포터블성을 개선하고, 동작을 표준화하고, 인터페이스를 더욱 현대적이고 Go와 유사하게 만듭니다.

### `archive/zip` 패키지 {#archive_zip}

Go 1에서 `[*zip.Writer`](/pkg/archive/zip/#Writer)에 더 이상 `Write` 메서드가 없습니다. 이는 실수였습니다.

_업데이트_:
작게 영향을 받는 코드는 컴파일러에 의해 감지되며, 수동으로 수정해야 합니다.

### `bufio` 패키지 {#bufio}

Go 1에서 [`bufio.NewReaderSize`](/pkg/bufio/#NewReaderSize)
과
[`bufio.NewWriterSize`](/pkg/bufio/#NewWriterSize)
함수는 더 이상 유효하지 않은 크기에 대해 오류를 반환하지 않습니다.
인수 크기가 너무 작거나 유효하지 않으면 조정됩니다.

_업데이트_:
`go fix` 명령을 실행하면 `_`에 오류를 할당하는 호출이 업데이트됩니다.
업데이트되지 않은 호출은 컴파일러에 의해 감지되며, 수동으로 업데이트해야 합니다.

### `compress/flate`, `compress/gzip` 및 `compress/zlib` 패키지 {#compress}

Go 1에서, `compress/flate`의 `NewWriterXxx` 함수, `compress/gzip`의 `NewWriterXxx` 함수, 그리고 `compress/zlib`의 `NewWriterXxx` 함수는 모두 압축 레벨을 인자로 받으면 `(*Writer, error)`를 반환하고, 그렇지 않으면 `*Writer`를 반환합니다. `gzip` 패키지의 `Compressor` 및 `Decompressor` 타입이 `Writer` 및 `Reader`로 이름이 변경되었습니다. `flate` 패키지의 `WrongValueError` 타입이 제거되었습니다.

_업데이트_
`go fix`를 실행하면 오래된 이름과 호출을 업데이트하고, 오류를 `_`에 할당하는 것을 수정합니다.
수정되지 않은 호출은 컴파일러에 의해 감지되며, 수동으로 업데이트해야 합니다.

### crypto/aes 및 crypto/des 패키지 {#crypto_aes_des}

Go 1에서 `Reset` 메서드는 제거되었습니다. Go는 메모리가 복사되지 않는 것을 보장하지 않으므로, 이 메서드는 오해를 불러일으킬 수 있었습니다.

`*aes.Cipher`, `*des.Cipher`,
및 `*des.TripleDESCipher`와 같은 암호별 유형은 `cipher.Block`으로 대체되었습니다.

_업데이트_:
Reset 호출을 제거합니다. 특정 암호화 유형의 사용을 `cipher.Block`으로 대체합니다.

### crypto/elliptic 패키지 {#crypto_elliptic}

Go 1에서 [`elliptic.Curve`](/pkg/crypto/elliptic/#Curve)는 대안적인 구현을 허용하기 위해 인터페이스로 변경되었습니다. 커브 매개변수는 `elliptic.CurveParams` 구조체로 이동되었습니다.

_업데이트:_
`*elliptic.Curve`를 사용하는 기존 사용자는 이제 `elliptic.Curve`로 변경해야 합니다. `Marshal`, `Unmarshal` 및 `GenerateKey`에 대한 호출은 이제 `crypto/elliptic`에서 `elliptic.Curve`를 첫 번째 인수로 사용하는 함수입니다.

### crypto/hmac 패키지 {#crypto_hmac}

Go 1에서, `hmac.NewMD5`와 같은 해시 특정 함수는 `crypto/hmac`에서 제거되었습니다. 대신, `hmac.New`는 `md5.New`와 같이 `hash.Hash`를 반환하는 함수를 받아 사용합니다.

_업데이트_:
`go` `fix` 명령어를 실행하면 필요한 변경 사항이 적용됩니다.

### crypto/x509 패키지 {#crypto_x509}

Go 1에서 `crypto/x509`의
[`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate)
함수와
[`CreateCRL`](/pkg/crypto/x509/#Certificate.CreateCRL)
메서드는 이전에는 `*rsa.PublicKey` 또는 `*rsa.PrivateKey`를 받는 대신
`interface{}`를 받도록 변경되었습니다. 이를 통해 향후 다른 공개 키 알고리즘을 구현할 수 있습니다.

_업데이트:_
변경 사항이 필요하지 않습니다.

### `encoding/binary` 패키지 {#encoding_binary}

Go 1에서는 `binary.TotalSize` 함수가 `Size`로 대체되었습니다.
[`Size`](/pkg/encoding/binary/#Size)는 `reflect.Value` 대신 `interface{}` 인수를 사용합니다.

_업데이트_:
작은 양의 코드가 영향을 받는 경우, 컴파일러가 이를 감지하고 수동으로 업데이트해야 합니다.

### `encoding/xml` 패키지 {#encoding_xml}

Go 1에서 [`xml`](/pkg/encoding/xml/) 패키지는 `encoding/gob`과 같은 다른 마샬링 패키지와 유사한 디자인으로 발전했습니다.

구형 `Parser` 타입이 이름이 변경되었습니다.
[`Decoder`](/pkg/encoding/xml/#Decoder) 및 새로운
[`Decode`](/pkg/encoding/xml/#Decoder.Decode) 메서드가 추가되었습니다. 또한
[`Encoder`](/pkg/encoding/xml/#Encoder) 타입도 도입되었습니다.

다음 함수 [`Marshal`](/pkg/encoding/xml/#Marshal)
과 [`Unmarshal`](/pkg/encoding/xml/#Unmarshal)
는 이제 `[]byte` 값을 사용합니다. 스트림을 처리하려면
새로운 [`Encoder`](/pkg/encoding/xml/#Encoder)
과 [`Decoder`](/pkg/encoding/xml/#Decoder) 유형을 사용하십시오.

값을 매핑하거나 역 매핑할 때, 필드 태그에 사용 가능한 플래그의 형식이 [`json`](/pkg/encoding/json) 패키지와 더 일치하도록 변경되었습니다 (`` `xml:"name,flag"` ``). 필드 태그, 필드 이름, 그리고 XML 속성 및 요소 이름 간의 일치 여부는 이제 대소문자를 구분합니다. `XMLName` 필드 태그가 존재하는 경우, 매핑되는 XML 요소의 이름과 일치해야 합니다.

_업데이트_:
`go fix` 명령을 실행하면 대부분의 패키지 사용이 업데이트되지만, `Unmarshal`에 대한 일부 호출은 업데이트되지 않습니다. 특히 필드 태그에 주의해야 합니다. 왜냐하면 이 도구는 태그를 업데이트하지 않기 때문이며, 수동으로 수정하지 않으면 일부 경우에는 예상치 못한 동작이 발생할 수 있습니다. 예를 들어, 이전의 `"attr"`은 이제 `"attr"`으로 변경되었으며, `"attr"`는 여전히 유효하지만 다른 의미를 가집니다.

### expvar 패키지 {#expvar}

```go
package expvar
```

Go 1에서는 `RemoveAll` 함수가 제거되었습니다.
`Iter` 함수와 `*Map`에 있는 `Iter` 메서드는
`[`Do`](/pkg/expvar/#Do)
와
`[*Map].Do`](/pkg/expvar/#Map.Do)
로 대체되었습니다.

_업데이트_:
대부분의 `expvar`을 사용하는 코드는 변경할 필요가 없습니다. `Iter`를 사용하는 드물게 사용되는 코드는 `Do`에 래퍼 함수를 전달하여 동일한 효과를 얻을 수 있습니다.

### `flag` 패키지 {#flag}

Go 1에서 인터페이스 [`flag.Value`](/pkg/flag/#Value)가 약간 변경되었습니다.
`Set` 메서드는 이제 성공 또는 실패를 나타내는 `bool` 대신 `error`를 반환합니다.

또한, `Duration`이라는 새로운 유형의 플래그가 도입되어, 시간 간격을 지정하는 인자 값을 지원합니다.
이러한 플래그의 값은 `time.Duration` 형식과 같이 유닛을 함께 지정해야 합니다: `10s`, `1h30m` 등.

```markdown
{{code "/doc/progs/go1.go" `/timeout/`}}
```

_업데이트_:
자체 플래그를 구현하는 프로그램은 `Set` 메서드를 업데이트하기 위해 약간의 수동 수정이 필요합니다.
`Duration` 플래그는 새 것이며 기존 코드에는 영향을 미치지 않습니다.

### `go/\*` 패키지 {#go}

`go` 하위에 있는 여러 패키지의 API가 약간 수정되었습니다.

구조체 `Mode` 유형이 구성 모드 플래그용으로 도입되었습니다.
이것은 다음 패키지에서 사용됩니다:
[`go/scanner`](/pkg/go/scanner/),
[`go/parser`](/pkg/go/parser/),
[`go/printer`](/pkg/go/printer/),
[`go/doc`](/pkg/go/doc/).

`AllowIllegalChars` 및 `InsertSemis` 모드는 [`go/scanner`](/pkg/go/scanner/) 패키지에서 제거되었습니다. 이 모드는 주로 Go 소스 파일이 아닌 텍스트를 스캔하는 데 유용했습니다. 대신, `text/scanner`](/pkg/text/scanner/) 패키지를 해당 목적으로 사용해야 합니다.

제공된 [`ErrorHandler`](/pkg/go/scanner/#ErrorHandler)는 스캐너의 [`Init`](/pkg/go/scanner/#Scanner.Init) 메서드에 전달되는 것이 이제 단순히 함수가 아닌 인터페이스가 되었습니다. `ErrorVector` 타입은 기존의 [`ErrorList`](/pkg/go/scanner/#ErrorList) 타입으로 대체되었으며, `ErrorVector` 메서드는 이동되었습니다. 스캐너의 클라이언트에 `ErrorVector`를 포함하는 대신, 클라이언트는 이제 `ErrorList`를 유지해야 합니다.

[`go/parser`](/pkg/go/parser/) 패키지에 제공되는 파싱 함수들의 집합은 주요 파싱 함수인
[`ParseFile`](/pkg/go/parser/#ParseFile)와 몇 가지 편의 함수인
[`ParseDir`](/pkg/go/parser/#ParseDir) 및
[`ParseExpr`](/pkg/go/parser/#ParseExpr)로 줄었습니다.

[`go/printer`](/pkg/go/printer/) 패키지는 추가적인 구성 모드인 [`SourcePos`](/pkg/go/printer/#Mode)를 지원합니다;
이 모드를 설정하면, 프린터는 생성된
출력에 원래 소스 코드 위치 정보가 포함되도록 `//line` 주석을 생성합니다.
새로운 타입인 [`CommentedNode`](/pkg/go/printer/#CommentedNode)를 사용하여
임의의 [`ast.Node`](/pkg/go/ast/#Node)와 관련된 주석을 제공할 수 있습니다 (지금까지는
[`ast.File`](/pkg/go/ast/#File)만 주석 정보를 담고 있었습니다).

[`go/doc`](/pkg/go/doc/) 패키지의 타입 이름이 다음과 같이 간소화되었습니다: `PackageDoc`는 이제 `Package`, `ValueDoc`는 `Value` 등으로 변경되었습니다.
또한, 모든 타입에는 이제 일관되게 `Name` 필드 (또는 `Value` 타입의 경우 `Names`)와 `Type.Factories`는 `Type.Funcs`로 변경되었습니다.
`doc.NewPackageDoc(pkg, importpath)`를 호출하는 대신, 패키지의 문서는 다음과 같이 생성됩니다:

doc.New(pkg, importpath, mode)

새로운 `mode` 매개변수는 작업을 수행하는 방식을 지정합니다:
`[AllDecls](pkg/go/doc/#AllDecls)`로 설정하면, 모든 선언(내보낸 선언뿐만 아니라)이 고려됩니다.
`NewFileDoc` 함수가 제거되었고, `CommentText` 함수가 `[Text](pkg/go/ast/#CommentGroup.Text)` 메서드가 되어 `[ast.CommentGroup](pkg/go/ast/#CommentGroup)`의 일부가 되었습니다.

패키지 [`go/token`](/pkg/go/token/), `Files` (원래는 `*token.File`의 채널을 반환) 메서드가 [`token.FileSet`](/pkg/go/token/#FileSet) 내에 있는 `Iterate` (이 메서드는 함수 인수를 받음) 이터레이터로 대체되었습니다.

패키지 [`go/build`](/pkg/go/build/)의 API는 거의 완전히 대체되었습니다.
이 패키지는 여전히 Go 패키지 정보를 계산하지만, 빌드를 실행하지는 않습니다. `Cmd` 및 `Script` 유형은 더 이상 사용되지 않습니다.
(코드를 빌드하려면 새 [`go`](/cmd/go/) 명령을 사용하십시오.)
`DirInfo` 유형은 이제 `[`Package`](/pkg/go/build/#Package)로 이름이 변경되었습니다.
`FindTree` 및 `ScanDir`은 `[`Import`](/pkg/go/build/#Import) 및 `[`ImportDir`](/pkg/go/build/#ImportDir)로 대체되었습니다.

_업데이트_:
`go` 패키지를 사용하는 코드는 수동으로 업데이트해야 하며,
컴파일러는 잘못된 사용을 거부합니다. `go/doc` 유형과 함께 사용되는 템플릿은 수동으로 수정해야 할 수 있으며, 이름이 변경된 필드는 런타임 오류를 발생시킬 수 있습니다.

### 해시 패키지 {#hash}

이 패키지는 다양한 해시 알고리즘을 제공합니다.

#### 해시 함수

| 함수 이름 | 설명 |
|---|---|
| `md5(string) string` | MD5 해시 함수를 사용하여 문자열의 해시 값을 계산합니다. |
| `sha1(string) string` | SHA-1 해시 함수를 사용하여 문자열의 해시 값을 계산합니다. |
| `sha256(string) string` | SHA-256 해시 함수를 사용하여 문자열의 해시 값을 계산합니다. |
| `sha512(string) string` | SHA-512 해시 함수를 사용하여 문자열의 해시 값을 계산합니다. |

#### 예제

```go
package main

import (
	"fmt"
	"hash/crc32"
)

func main() {
	message := "hello, world!"

	// MD5 해시 계산
	md5Hash := crc32.ChecksumIEEE([]byte(message))
	fmt.Printf("MD5 Hash: %x\n", md5Hash)

	// SHA-1 해시 계산
	// SHA-1은 Go의 `hash/sha1` 패키지에 포함되어 있습니다.
	// (예제에서는 crc32를 사용하여 SHA-1을 대체합니다)
	fmt.Println("SHA-1 Hash (예시): 계산 불가 (Go에서 sha1 패키지 필요)")

    // SHA-256 해시 계산 (예시)
    // sha256 패키지를 import해야 사용 가능
    // import "crypto/sha256"
    // hasher := sha256.New()
    // messageBytes := []byte(message)
    // hash := hasher.Sum(messageBytes)
    // fmt.Printf("SHA-256 Hash: %x\n", hash)

	// CRC32 해시 계산 (예시)
	crc32Hash := crc32.ChecksumIEEE([]byte(message))
	fmt.Printf("CRC32 Hash: %x\n", crc32Hash)
}
```

이 예제는 `hash/crc32` 패키지를 사용하여 CRC32 해시를 계산하는 방법을 보여줍니다.  다른 해시 알고리즘을 사용하려면 해당 패키지를 import 해야 합니다.  SHA-1 및 SHA-256 해시 계산은 예시로 주석 처리되어 있습니다.

Go 1에서 [`hash.Hash`](/pkg/hash/#Hash)의 정의에는
새로운 메서드, `BlockSize`가 포함되어 있습니다. 이 새로운 메서드는 주로 암호화 라이브러리에서 사용됩니다.

`Sum` 메서드는 이제 `[]byte` 인수를 받습니다. 이 인수에 해시 값이 추가됩니다.
이전 동작은 호출에 `nil` 인수를 추가하여 재현할 수 있습니다.

_업데이트_:
기존의 `hash.Hash` 구현은 `BlockSize` 메서드를 추가해야 합니다. 각 바이트 단위로 입력을 처리하는 해시 구현은 `BlockSize`를 구현하여 1을 반환할 수 있습니다. `go fix` 명령을 실행하면, 다양한 `hash.Hash` 구현의 `Sum` 메서드 호출이 업데이트됩니다.

_업데이트_:
이 패키지의 기능이 새로운 것이므로, 업데이트는 필요하지 않습니다.

### `http` 패키지 {#http}

Go 1에서 [`http`](/pkg/net/http/) 패키지가 재구성되어, 일부 유틸리티가 [`httputil`](/pkg/net/http/httputil/) 서브디렉토리에 이동되었습니다.
이 기능들은 HTTP 클라이언트에서 매우 드물게 사용됩니다.
영향을 받는 항목은 다음과 같습니다:

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

`Handle` 및 `HandleFunc` 함수, 그리고 유사하게 이름이 지정된 `ServeMux`의 메서드는 동일한 패턴을 두 번 등록하려고 시도할 경우 panic을 발생시킵니다.

_업데이트_:
`go fix` 명령어를 실행하면, 영향을 받는 일부 프로그램이 업데이트되지만, `RawURL` 사용 부분은 수동으로 수정해야 합니다.

### 이미지 패키지 {#image}

[`image`](/pkg/image/) 패키지는 다음과 같은 여러 가지 미세한 변경, 재구성 및 이름 변경을 포함하고 있습니다.

대부분의 색상 처리 코드가 자체 패키지로 이동되었습니다.
[`image/color`](/pkg/image/color/).
이동된 요소에 대해서는 대칭이 발생합니다. 예를 들어,
각
[`image.RGBA`](/pkg/image/#RGBA)
픽셀은
[`color.RGBA`](/pkg/image/color/#RGBA)
입니다.

기존의 `image/ycbcr` 패키지는 일부 이름 변경과 함께
`image` 및 `image/color` 패키지로 통합되었습니다.

구형 `image.ColorImage` 타입은 여전히 `image`
패키지에 있지만 이름이 변경되었습니다.
[`image.Uniform`](/pkg/image/#Uniform),
그리고 `image.Tiled`은 제거되었습니다.

이 표는 이름 변경 목록을 보여줍니다.

```
<table class="codetable" frame="border" summary="이미지 이름 변경">
<colgroup align="left" width="50%"></colgroup>
<colgroup align="left" width="50%"></colgroup>
<tbody>
<tr style="text-align: left;">
<th>원래</th>
<th>새로운</th>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>image.Color</td>
<td>color.Color</td>
</tr>
<tr>
<td>image.ColorModel</td>
<td>color.Model</td>
</tr>
<tr>
<td>image.ColorModelFunc</td>
<td>color.ModelFunc</td>
</tr>
<tr>
<td>image.PalettedColorModel</td>
<td>color.Palette</td>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>image.RGBAColor</td>
<td>color.RGBA</td>
</tr>
<tr>
<td>image.RGBA64Color</td>
<td>color.RGBA64</td>
</tr>
<tr>
<td>image.NRGBAColor</td>
<td>color.NRGBA</td>
</tr>
<tr>
<td>image.NRGBA64Color</td>
<td>color.NRGBA64</td>
</tr>
<tr>
<td>image.AlphaColor</td>
<td>color.Alpha</td>
</tr>
<tr>
<td>image.Alpha16Color</td>
<td>color.Alpha16</td>
</tr>
<tr>
<td>image.GrayColor</td>
<td>color.Gray</td>
</tr>
<tr>
<td>image.Gray16Color</td>
<td>color.Gray16</td>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>image.RGBAColorModel</td>
<td>color.RGBAModel</td>
</tr>
<tr>
<td>image.RGBA64ColorModel</td>
<td>color.RGBA64Model</td>
</tr>
<tr>
<td>image.NRGBAColorModel</td>
<td>color.NRGBAModel</td>
</tr>
<tr>
<td>image.NRGBA64ColorModel</td>
<td>color.NRGBA64Model</td>
</tr>
<tr>
<td>image.AlphaColorModel</td>
<td>color.AlphaModel</td>
</tr>
<tr>
<td>image.Alpha16ColorModel</td>
<td>color.Alpha16Model</td>
</tr>
<tr>
<td>image.GrayColorModel</td>
<td>color.GrayModel</td>
</tr>
<tr>
<td>image.Gray16ColorModel</td>
<td>color.Gray16Model</td>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>ycbcr.RGBToYCbCr</td>
<td>color.RGBToYCbCr</td>
</tr>
<tr>
<td>ycbcr.YCbCrToRGB</td>
<td>color.YCbCrToRGB</td>
</tr>
<tr>
<td>ycbcr.YCbCrColorModel</td>
<td>color.YCbCrModel</td>
</tr>
<tr>
<td>ycbcr.YCbCrColor</td>
<td>color.YCbCr</td>
</tr>
<tr>
<td>ycbcr.YCbCr</td>
<td>image.YCbCr</td>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>ycbcr.SubsampleRatio444</td>
<td>image.YCbCrSubsampleRatio444</td>
</tr>
<tr>
<td>ycbcr.SubsampleRatio422</td>
<td>image.YCbCrSubsampleRatio422</td>
</tr>
<tr>
<td>ycbcr.SubsampleRatio420</td>
<td>image.YCbCrSubsampleRatio420</td>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>image.ColorImage</td>
<td>image.Uniform</td>
</tr>
</tbody>
</table>
```

이미지 패키지의 `New` 함수
([`NewRGBA`](/pkg/image/#NewRGBA),
[`NewRGBA64`](/pkg/image/#NewRGBA64), 등)는
네 개의 정수 대신 [`image.Rectangle`](/pkg/image/#Rectangle)를 인자로 사용합니다.

마지막으로, 새롭게 정의된 `color.Color` 변수가 있습니다.
[`color.Black`](/pkg/image/color/#Black),
[`color.White`](/pkg/image/color/#White),
[`color.Opaque`](/pkg/image/color/#Opaque)
그리고
[`color.Transparent`](/pkg/image/color/#Transparent).

_업데이트_:
`go` `fix` 명령어를 실행하면 변경 사항에 영향을 받는 거의 모든 코드가 업데이트됩니다.

### `log/syslog` 패키지 {#log_syslog}

Go 1에서 `syslog.NewLogger` 함수는 `log.Logger` 뿐만 아니라 오류도 반환합니다.

_업데이트_:
영향을 받는 소스 코드는 컴파일러에 의해 감지되며, 수동으로 업데이트해야 합니다.

### `mime` 패키지 {#mime}

Go 1에서 `mime` 패키지의 `FormatMediaType` 함수가 `ParseMediaType`와 일관성을 유지하기 위해 단순화되었습니다.
이제 `"text/html"`를 사용하며 더 이상 `"text"`와 `"html"`를 사용하지 않습니다.

_업데이트_:
영향을 받는 코드는 컴파일러에서 감지되며, 수동으로 업데이트해야 합니다.

### net 패키지 {#net}

```go
package net
```

Go 1에서 다양한 `SetTimeout`, `SetReadTimeout`, 및 `SetWriteTimeout` 메서드는 다음과 같이 대체되었습니다.
[`SetDeadline`](/pkg/net/#IPConn.SetDeadline),
[`SetReadDeadline`](/pkg/net/#IPConn.SetReadDeadline), 및
[`SetWriteDeadline`](/pkg/net/#IPConn.SetWriteDeadline)

이 새로운 메서드는 연결의 모든 활동에 적용되는 나노초 단위의 타임아웃 값을 사용하지 않고, 절대적인 마감 시간을 (time.Time 값으로) 설정합니다. 이 마감 시간 이후에는 읽기 및 쓰기가 타임아웃되고 더 이상 블로킹되지 않습니다.

다음은 새로운 함수도 있습니다.
[`net.DialTimeout`](/pkg/net/#DialTimeout)
는 네트워크 주소에 대한 연결 시간을 지정하는 것을 단순화합니다.
그리고
[`net.ListenMulticastUDP`](/pkg/net/#ListenMulticastUDP)
는 여러 리스너에서 동시 멀티캐스트 UDP를 수신할 수 있도록 합니다.
`net.ListenMulticastUDP` 함수는 이전의
`JoinGroup` 및 `LeaveGroup` 메서드를 대체합니다.

_업데이트_:
기존 메서드를 사용하는 코드는 컴파일에 실패하고, 수동으로 업데이트해야 합니다.
의미론적 변경으로 인해, 자동 업데이트 도구가 쉽게 업데이트할 수 없습니다.

### `os` 패키지 {#os}

```python
import os
```

이 패키지는 운영체제와 상호 작용하기 위한 다양한 함수를 제공합니다.

**예시:**

```python
# 파일 시스템 작업
print(os.getcwd())  # 현재 작업 디렉토리 가져오기
os.chdir('/tmp')
print(os.listdir('/tmp'))

# 환경 변수
print(os.environ.get('PATH'))

# 프로세스 생성
import subprocess
process = subprocess.Popen(['ls', '-l'])
```

함수 `Time`이 제거되었습니다. 호출자는 `time` 패키지의 [`Time`](/pkg/time/#Time) 유형을 사용해야 합니다.

`Exec` 함수가 제거되었습니다. 사용자는 `syscall` 패키지에서 `Exec` 함수를 사용해야 합니다 (사용 가능한 경우).

`ShellExpand` 함수는 `[ExpandEnv](pkg/os/#ExpandEnv)`로 이름이 변경되었습니다.

[`NewFile`](/pkg/os/#NewFile) 함수
이제 `uintptr`인 `fd`를 받습니다. 이전에는 `int`를 받았습니다.

파일에 있는 [`Fd`](/pkg/os/#File.Fd) 메서드는
이제 `uintptr`도 반환합니다.

`os` 패키지에 `EINVAL`과 같은 오류 상수가 더 이상 존재하지 않습니다. 이는 기본 운영 체제에 따라 값이 달라졌기 때문입니다. 이제 `IsPermission`와 같은 새로운 포괄적인 함수를 사용하여 일반적인 오류 속성을 테스트할 수 있습니다. 또한 `ErrPermission` 및 `ErrNotExist`과 같이 Go와 유사한 이름의 몇 가지 새로운 오류 값도 추가되었습니다.

`Getenverror` 함수가 제거되었습니다. "존재하지 않는 환경 변수"와 "빈 문자열"을 구별하려면 `os.Environ` ([https://pkg/os/#Environ](https://pkg/os/#Environ)) 또는 `syscall.Getenv` ([https://pkg/syscall/#Getenv](https://pkg/syscall/#Getenv))을 사용하십시오.

[`Process.Wait`](/pkg/os/#Process.Wait) 메서드는
옵션 인수를 제거했으며, 해당 상기도 패키지에서 제거되었습니다.
또한, `Wait` 함수는 더 이상 존재하지 않으며, `Process` 타입의 메서드만 남아 있습니다.

`Waitmsg` 타입, `[`Process.Wait`](/pkg/os/#Process.Wait)에서 반환되는 타입이
더욱 호환 가능한 `[`ProcessState`](/pkg/os/#ProcessState) 타입으로 대체되었습니다.
이 타입은 프로세트에 대한 정보를 복구하기 위한 접근자 메서드를 제공합니다.

`Wait`의 변경으로 인해 `ProcessState` 값은 항상 종료된 프로세스를 나타냅니다.

호환성 관련 문제로 인해 인터페이스가 다른 방식으로 단순화되었지만,
`[`ProcessState.Sys`](/pkg/os/#ProcessState.Sys) 및
`[`ProcessState.SysUsage`](/pkg/os/#ProcessState.SysUsage) 메서드에서 반환되는 값은 Unix에서
`[`syscall.WaitStatus`](/pkg/syscall/#WaitStatus) 및
`[`syscall.Rusage`](/pkg/syscall/#Rusage)와 같은 기본 시스템별 데이터 구조로 타입 변환할 수 있습니다.

_업데이트_:
`go` `fix`를 실행하면 `Process.Wait`에 인수를 제거합니다.
다른 모든 변경 사항은 컴파일러가 감지하고 수동으로 업데이트해야 합니다.

#### `os.FileInfo` 타입 {#os_fileinfo}

Go 1에서 [`os.FileInfo`](/pkg/os/#FileInfo) 타입이 재정의됩니다.
구조체에서 인터페이스로 변경됩니다:

```go
type FileInfo 인터페이스 {
	        Name() string       // 파일의 기본 이름
	        Size() int64        // 바이트 단위의 길이
	        Mode() FileMode     // 파일 모드 비트
	        ModTime() time.Time // 수정 시간
	        IsDir() bool        // Mode().IsDir()의 약어
	        Sys() interface{}   // 기본 데이터 소스 (nil 반환 가능)
	    }
```

파일 모드 정보는 `os.FileMode`라는 하위 유형으로 이동되었습니다.
이는 `IsDir`, `Perm`, `String` 메서드를 가진 간단한 정수 유형입니다.

파일 모드 및 속성(예: Unix 시스템의)과 관련된 시스템별 세부 정보는 `FileInfo`에서 완전히 제거되었습니다.
대신, 각 운영 체제의 `os` 패키지는 `FileInfo` 인터페이스의 구현을 제공하며,
이 인터페이스에는 `Sys` 메서드가 포함되어 있으며, 이 메서드는 파일 메타데이터의 시스템별 표현을 반환합니다.
예를 들어, Unix 시스템에서 파일의 i-번호를 찾으려면 `FileInfo`를 다음과 같이 언패킹합니다:

```markdown
fi, err := os.Stat("hello.go")
    if err != nil {
        log.Fatal(err)
    }
    # 확인하기 위해 파일이 Unix 파일인지 확인합니다.
    unixStat, ok := fi.Sys().(*syscall.Stat_t)
    if !ok {
        log.Fatal("hello.go: Unix 파일이 아닙니다")
    }
    fmt.Printf("파일 i-number: %d\n", unixStat.Ino)
```

가정 (하지만 비현실적) 하건데, `"hello.go"`가 Unix 파일이라고 가정하면,
`i-number` 표현은 다음과 같이 축약될 수 있습니다:

fi.Sys().(*syscall.Stat_t).Ino

대부분의 `FileInfo` 사용은 표준 인터페이스의 메서드만 필요합니다.

`os` 패키지는 이제 `ENOENT`와 같은 POSIX 오류에 대한 래퍼를 더 이상 포함하지 않습니다.

특정 오류 조건을 확인해야 하는 몇몇 프로그램의 경우, 이제 다음과 같은 부울 함수가 있습니다.
[`IsExist`](/pkg/os/#IsExist),
[`IsNotExist`](/pkg/os/#IsNotExist)
및
[`IsPermission`](/pkg/os/#IsPermission).

```markdown
{{code "/doc/progs/go1.go" `/os\.Open/` `/}/`}}
```

_업데이트_:
`go fix` 명령어를 실행하면 현재 `os.FileInfo` 및 `os.FileMode` API의 이전 버전과 호환되는 코드를 업데이트합니다.
시스템별 파일 정보를 사용하는 코드는 수동으로 업데이트해야 합니다.
`os` 패키지에서 이전 POSIX 오류 값을 사용하는 코드는 컴파일에 실패하고, 이 또한 수동으로 업데이트해야 합니다.

### `os/signal` 패키지 {#os_signal}

```go
package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	// 시그널 수신 채널 생성
	sigs := make(chan os.Signal, 1)

	// 시그널 수신 등록
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)

	// 시그널 수신 대기
	fmt.Print("프로그램 실행 중... 종료하려면 Ctrl+C 누르세요.\n")
	for {
		select {
		case sig := <-sigs:
			fmt.Println()
			fmt.Println("시그널 획득:", sig)
			fmt.Println("프로그램 종료.")
			os.Exit(0)
		}
	}
}
```

### 설명:

이 예제는 `os/signal` 패키지를 사용하여 운영 체제에서 전송되는 시그널(예: `SIGINT`, `SIGTERM`)을 수신하고 처리하는 방법을 보여줍니다.

*   **`sigs := make(chan os.Signal, 1)`**:  `os.Signal` 타입의 채널을 생성합니다.  이 채널은 시그널을 수신하는 데 사용됩니다.  `1`은 채널에 저장할 수 있는 메시지의 최대 수를 나타냅니다.
*   **`signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)`**:  `SIGINT` (Ctrl+C) 및 `SIGTERM` 시그널을 `sigs` 채널에 수신하도록 등록합니다.
*   **`select { ... }`**:  `sigs` 채널에서 시그널을 수신하는 것을 기다리는 `select` 문을 사용합니다.  채널에서 메시지가 수신되면 해당 메시지가 `sig` 변수에 할당되고, 프로그램은 종료됩니다.
*   **`os.Exit(0)`**: 프로그램이 정상적으로 종료됩니다.

이 코드는 Ctrl+C를 누르면 프로그램이 종료됩니다.

`os/signal` 패키지(Go 1)에서 `Incoming` 함수를 대체하는 것이 `Notify` 함수입니다. 이 함수는 기존 채널을 통해 특정 신호만 받도록 요청합니다. 이 함수는 모든 들어오는 신호를 수신하는 채널을 반환하는 `Incoming` 함수를 대체합니다.

_업데이트_:
코드는 수동으로 업데이트해야 합니다.
다음과 같은 문자열을 그대로 사용해야 합니다.

c := signal.Incoming()

이

```
c := make(chan os.Signal, 1)
signal.Notify(c) // 모든 신호를 요청
```

하지만 대부분의 코드는 처리하려는 특정 신호를 명시적으로 나열해야 합니다:

```markdown
```go
c := make(chan os.Signal, 1)
	signal.Notify(c, syscall.SIGHUP, syscall.SIGQUIT)
```

### `/path` 및 `filepath` 패키지 {#path_filepath}

Go 1에서 `path/filepath` 패키지의 `Walk` 함수는
[`WalkFunc`](/pkg/path/filepath/#WalkFunc) 유형의 함수 값을
`Visitor` 인터페이스 값 대신 사용하도록 변경되었습니다.
`WalkFunc`는 파일과 디렉토리를 모두 처리하는 방식을 통합합니다.

```markdown
```go
type WalkFunc func(path string, info os.FileInfo, err error) error
```

`WalkFunc` 함수는 열 수 없는 파일이나 디렉토리에도 호출됩니다.
이 경우, 오류 인수는 실패를 설명합니다.
디렉토리의 내용을 건너뛰려면,
함수는 [`filepath.SkipDir`](/pkg/path/filepath/#pkg-variables) 값을 반환해야 합니다.

{{code "/doc/progs/go1.go" `/STARTWALK/` `/ENDWALK/`}}

_업데이트_:
이 변경 사항은 대부분의 코드를 단순화하지만, 미묘한 결과를 초래하므로 영향을 받는 프로그램은 수동으로 업데이트해야 합니다.
컴파일러는 이전 인터페이스를 사용하는 코드를 감지합니다.

### `regexp` 패키지 {#regexp}

```go
package main

import (
	"fmt"
	"regexp"
)

func main() {
	// 정규 표현식 컴파일
	pattern := "hello"
	re, err := regexp.Compile(pattern)
	if err != nil {
		fmt.Println("정규 표현식 컴파일 오류:", err)
		return
	}

	// 문자열 매칭
	text := "hello world"
	match := re.FindString(text)
	fmt.Println("매치 결과:", match)

	// 정규 표현식 생성
	re2, err := regexp.Compile("a(b*)c?")
	if err != nil {
		fmt.Println("정규 표현식 생성 오류:", err)
		return
	}

	// 그룹 추출
	text2 := "abcabc"
	matches := re2.FindAllStringSubmatch(text2, -1)
	fmt.Println("그룹 추출 결과:", matches)
}
```

| 기능 | 설명 |
|---|---|
| `Compile()` | 정규 표현식을 컴파일하여 `Regexp` 객체를 반환합니다. |
| `FindString()` | 주어진 텍스트에서 정규 표현식과 일치하는 첫 번째 문자열을 반환합니다. |
| `FindAllString()` | 주어진 텍스트에서 정규 표현식과 일치하는 모든 문자열을 찾고, 각 매치에 대한 정보를 포함하는 슬라이스를 반환합니다. `-1`은 모든 매치를 반환하도록 지정합니다. |

[`regexp`](/pkg/regexp/) 패키지가 재작성되었습니다.
인터페이스는 동일하지만, 지원하는 정규 표현식의 사양이 이전의 "egrep" 형식에서 [RE2](https://code.google.com/p/re2/) 형식으로 변경되었습니다.

_업데이트_:
패키지를 사용하는 코드는 정규 표현식을 수동으로 검토해야 합니다.

### 런타임 패키지 {#runtime}

Go 1에서는 `runtime` 패키지에 의해 내보낸 대부분의 API가 다른 패키지에 제공되는 기능으로 대체되었습니다.
`runtime.Type` 인터페이스 또는 그 구체적인 타입 구현을 사용하는 코드는 이제 `[`reflect`](/pkg/reflect/) 패키지를 사용해야 합니다.
`runtime.Semacquire` 및 `runtime.Semrelease`를 사용하는 코드는 채널 또는 `[`sync`](/pkg/sync/) 패키지에 있는 추상화를 사용해야 합니다.
`runtime.Alloc`, `runtime.Free`, 및 `runtime.Lookup` 함수는 메모리 할당자를 디버깅하기 위해 만들어진 안전하지 않은 API이며, 대체 기능이 없습니다.

이전에는 `runtime.MemStats`는 메모 할당에 대한 통계를 담고 있는 전역 변수였으며, `runtime.UpdateMemStats` 호출을 통해 최신 상태를 유지했습니다.

Go 1에서 `runtime.MemStats`는 구조체 유형이며, 코드는 `[`runtime.ReadMemStats](pkg/runtime/#ReadMemStats)`를 사용하여 현재 통계를 가져야 합니다.

이 패키지는 운영 체제 커널에서 보고하는 사용 가능한 CPU 수를 반환하는 새로운 함수, [`runtime.NumCPU`](/pkg/runtime/#NumCPU)를 추가합니다.
이 값은 `GOMAXPROCS` 설정을 안내하는 데 사용할 수 있습니다.
`runtime.Cgocalls` 및 `runtime.Goroutines` 함수는 `runtime.NumCgoCall` 및 `runtime.NumGoroutine`으로 이름이 변경되었습니다.

_업데이트_:
`go fix` 명령어를 실행하면 함수 이름 변경에 대한 코드가 업데이트됩니다.
다른 코드는 수동으로 업데이트해야 합니다.

### `strconv` 패키지 {#strconv}

Go 1에서
[`strconv`](/pkg/strconv/)
패키지는 더 Go와 유사하고 C와 덜 유사하도록 크게 수정되었습니다.
`Atoi`는 여전히 존재합니다 (예: `int(ParseInt(x, 10, 0))`과 유사),
그리고 `Itoa(x)`도 존재합니다 (`FormatInt(int64(x), 10)`).
또한 일부 함수는 문자열 대신 바이트 슬라이스에 추가하도록 변경되어, 할당을 제어할 수 있습니다.

이 표는 이름 변경 사항을 요약합니다. 자세한 내용은 [패키지 문서](/pkg/strconv/)를 참조하십시오.

```
<table>
<colgroup align="left" width="50%"></colgroup>
<colgroup align="left" width="50%"></colgroup>
<tbody>
<tr>
<th>Old call</th>
<th>New call</th>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>Atob(x)</td>
<td>ParseBool(x)</td>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>Atof32(x)</td>
<td>ParseFloat(x, 32)</td>
</tr>
<tr>
<td>Atof64(x)</td>
<td>ParseFloat(x, 64)</td>
</tr>
<tr>
<td>AtofN(x, n)</td>
<td>ParseFloat(x, n)</td>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>Atoi(x)</td>
<td>Atoi(x)</td>
</tr>
<tr>
<td>Atoi(x)</td>
<td>ParseInt(x, 10, 0)</td>
</tr>
<tr>
<td>Atoi64(x)</td>
<td>ParseInt(x, 10, 64)</td>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>Atoui(x)</td>
<td>ParseUint(x, 10, 0)</td>
</tr>
<tr>
<td>Atoui64(x)</td>
<td>ParseUint(x, 10, 64)</td>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>Btoi64(x, b)</td>
<td>ParseInt(x, b, 64)</td>
</tr>
<tr>
<td>Btoui64(x, b)</td>
<td>ParseUint(x, b, 64)</td>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>Btoa(x)</td>
<td>FormatBool(x)</td>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>Ftoa32(x, f, p)</td>
<td>FormatFloat(float64(x), f, p, 32)</td>
</tr>
<tr>
<td>Ftoa64(x, f, p)</td>
<td>FormatFloat(x, f, p, 64)</td>
</tr>
<tr>
<td>FtoaN(x, f, p, n)</td>
<td>FormatFloat(x, f, p, n)</td>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>Itoa(x)</td>
<td>Itoa(x)</td>
</tr>
<tr>
<td>Itoa(x)</td>
<td>FormatInt(int64(x), 10)</td>
</tr>
<tr>
<td>Itoa64(x)</td>
<td>FormatInt(x, 10)</td>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>Itob(x, b)</td>
<td>FormatInt(int64(x), b)</td>
</tr>
<tr>
<td>Itob64(x, b)</td>
<td>FormatInt(x, b)</td>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>Uitoa(x)</td>
<td>FormatUint(uint64(x), 10)</td>
</tr>
<tr>
<td>Uitoa64(x)</td>
<td>FormatUint(x, 10)</td>
</tr>
<tr>
<td colspan="2"><hr></hr></td>
</tr>
<tr>
<td>Uitob(x, b)</td>
<td>FormatUint(uint64(x), b)</td>
</tr>
<tr>
<td>Uitob64(x, b)</td>
<td>FormatUint(x, b)</td>
</tr>
</tbody>
</table>

_업데이트_:
`go fix` 명령어를 실행하면 변경 사항에 영향을 받는 거의 모든 코드가 업데이트됩니다.

§ `Atoi`는 유지되지만 `Atoui`와 `Atof32`는 유지되지 않으므로,
이를 위해서는 수동으로 변환이 필요할 수 있으며, `go fix` 도구가 이를 경고합니다.

### 템플릿 패키지 {#templates}

`template` 및 `exp/template/html` 패키지는
[`text/template`](/pkg/text/template/) 및
[`html/template`](/pkg/html/template/)로 이동했습니다.
더 중요한 것은, 이러한 패키지에 대한 인터페이스가 단순화되었습니다.
템플릿 언어는 동일하지만, "템플릿 세트"라는 개념은 사라졌고, 패키지의 함수 및 메서드도 이에 따라 변경되었으며, 종종 제거되었습니다.

대신 세트를 사용하는 대신, `Template` 객체는
여러 개의 이름이 지정된 템플릿 정의를 포함할 수 있으며,
실제로 템플릿 호출을 위한 이름 공간을 생성합니다.
템플릿은 다른 템플릿을 호출할 수 있지만,
해당 템플릿과 연결된 템플릿만 호출할 수 있습니다.
템플릿을 연결하는 가장 간단한 방법은 함께 파싱하는 것이며,
새로운 패키지의 구조 덕분에 이를 더 쉽게 수행할 수 있습니다.

_업데이트_:
`fix` 도구를 사용하여 가져오기를 업데이트합니다.
단일 템플릿 사용은 대부분 영향을 받지 않습니다.
여러 템플릿을 함께 사용하는 코드는 수동으로 업데이트해야 합니다.
`text/template`에 대한 설명서의 [예시](/pkg/text/template/#pkg-examples)에서 안내를 받을 수 있습니다.

### 테스트 패키지 {#testing}

테스팅 패키지는 `B`라는 타입을, 벤치마크 함수에 인수로 전달합니다.
Go 1에서는 `B` 타입에 `T` 타입과 유사한 새로운 메서드가 추가되어,
로깅 및 실패 보고 기능을 제공합니다.

```
{{code "/doc/progs/go1.go" `/func.*Benchmark/` `/^}/`}}
```

_업데이트_:
기존 코드는 영향을 받지 않지만, `println` 또는 `panic`을 사용하는 벤치마크는 새로운 메서드를 사용하는 방식으로 업데이트해야 합니다.

### testing/script 패키지 {#testing_script}

`testing/script` 패키지는 삭제되었습니다. 이는 더 이상 사용되지 않는 패키지였습니다.

_업데이트_:
코드가 영향을 받을 가능성은 낮습니다.

### `unsafe` 패키지 {#unsafe}

Go 1에서 다음 함수들이 제거되었습니다:
`unsafe.Typeof`, `unsafe.Reflect`,
`unsafe.Unreflect`, `unsafe.New`,
`unsafe.NewArray`
이 함수들은 `reflect` 패키지에 제공되는 더 안전한 기능을 중복했습니다.

_업데이트_:
이 함수를 사용하는 코드는 다음 패키지를 사용하여 다시 작성해야 합니다: [`reflect`](/pkg/reflect/).
[encoding/gob](/change/2646dc956207) 및 [protocol buffer 라이브러리](https://code.google.com/p/goprotobuf/source/detail?r=5340ad310031)에 대한 변경 사항이 도움이 될 수 있습니다.

### `url` 패키지 {#url}

Go 1에서 [`url.URL`](/pkg/net/url/#URL) 타입의 여러 필드가 제거되거나 대체되었습니다.

[`String`](/pkg/net/url/#URL.String) 메서드는 이제 `URL`의 모든 필드를 사용하여 인코딩된 URL 문자열을 예측 가능하게 재구성합니다. 결과 문자열에는 더 이상 비밀번호가 포함되지 않습니다.

`Raw` 필드가 제거되었습니다. 대부분의 경우 `String` 메서드를 대신 사용할 수 있습니다.

기존의 `RawUserinfo` 필드는 `User` 필드로 대체되며, 이 필드의 타입은 `*net.Userinfo`입니다.
이 타입의 값은 새로운 `net.User` 및 `net.UserPassword` 함수를 사용하여 생성할 수 있습니다. `EscapeUserinfo` 및 `UnescapeUserinfo` 함수는 더 이상 사용되지 않습니다.

`RawAuthority` 필드가 제거되었습니다. 동일한 정보는 `Host` 및 `User` 필드에서 사용할 수 있습니다.

`RawPath` 필드와 `EncodedPath` 메서드는 제거되었습니다. 루트 URL (스킴 뒤에 슬래시가 있는)에 있는 경로 정보는 이제 `Path` 필드에 디코딩된 형태로만 제공됩니다.
때로는 디코딩 과정에서 손실된 정보를 얻기 위해 인코딩된 데이터를 사용해야 할 수 있습니다. 이러한 경우에는 URL이 생성된 원래 데이터를 참조해야 합니다.

다음과 같은 루트가 없는 URL(예: `"mailto:dev@golang.org?subject=Hi"`)도 다르게 처리됩니다. `OpaquePath` 불리언 필드가 제거되었고, 이와 같은 URL에 인코딩된 경로를 저장하기 위한 새로운 `Opaque` 문자열 필드가 도입되었습니다. Go 1에서 위 URL은 다음과 같이 파싱됩니다:

```json
{
	        Scheme: "mailto",
	        Opaque: "dev@golang.org",
	        RawQuery: "subject=Hi",
	    }
```

새로운 `RequestURI` 메서드가 `URL`에 추가되었습니다.

`ParseWithReference` 함수가 `ParseWithFragment`로 이름이 변경되었습니다.

_업데이트_:
기존 필드를 사용하는 코드는 컴파일에 실패하고, 수동으로 업데이트해야 합니다.
의미론적 변경 사항으로 인해, 자동 업데이트 도구가 쉽게 수정할 수 없습니다.

## `go` 명령어 {#cmd_go}

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, World!")
}
```

| 기능 | 설명 |
|---|---|
| `go build` | Go 패키지를 실행 가능한 바이너리로 컴파일합니다. |
| `go run` | Go 패키지를 컴파일하고 실행합니다. |
| `go get` | Go 모듈을 다운로드하고 설치합니다. |
| `go install` | Go 패키지를 설치합니다. |
| `go test` | Go 패키지를 테스트합니다. |

Go 1은 `/cmd/go/`에서 사용되는 `go` 명령어를 소개합니다. 이는 Go 패키지와 명령어를 가져오고, 빌드하고, 설치하는 도구입니다. `go` 명령은 `make` 파일을 사용하지 않고, Go 소스 코드를 사용하여 의존성을 찾고 빌드 조건을 결정합니다. 대부분의 기존 Go 프로그램은 `make` 파일을 사용하여 빌드할 필요가 없어졌습니다.

자세한 내용은 [go 명령 사용 방법](/doc/code.html) 및 [go 명령 설명서](/cmd/go/)를 참조하세요.

_업데이트_:
Go 프로젝트의 기존 makefile 기반 빌드 인프라(`Make.pkg`, `Make.cmd` 등)에 의존하는 프로젝트는 Go 코드를 빌드하기 위해 `go` 명령어를 사용하도록 변경해야 합니다. 또한 필요한 경우, 빌드 작업을 수행하기 위해 makefile을 다시 작성해야 합니다.

## `cgo` 명령어 {#cmd_cgo}

이 명령어는 C 코드를 Go 프로그램에서 사용하는 방법을 정의합니다.

### 사용법

```
cgo [옵션] [C 코드 파일 또는 명령어]
```

### 옵션

*   `-pkgdir <경로>`: Go 패키지를 설치할 디렉토리를 지정합니다.
*   `-I <경로>`: C 헤더 파일 검색 경로를 추가합니다.
*   `-L <경로>`: C 라이브러리 검색 경로를 추가합니다.
*   `-buildmode <모드>`: 빌드 모드를 지정합니다 (예: `exe`, `cgo`, `panic`). 기본값은 `cgo`입니다.
*   `-race`: Go 런타임 레이스를 활성화합니다.
*   `-X C`: C 코드 실행 전후에 코드를 실행할 수 있도록 합니다.
*   `-X o`: C 코드 실행 후에 코드를 실행할 수 있도록 합니다.

### 예제

```go
package main

import "C"

func main() {
    // C 코드 실행
    C.printf("Hello from C!\n")
}
```

위 코드는 "Hello from C!"를 출력합니다.

### 주의사항

*   C 코드에서 Go 함수를 호출할 때는 Go 함수 이름과 유형을 정확하게 지정해야 합니다.
*   C 코드에서 메모리를 할당하고 해제할 때는 주의해야 합니다.
*   C 코드에서 Go 함수를 호출하기 전에 `package C`를 선언해야 합니다.

Go 1의 `[cgo 명령](cmd/cgo)`는 다른 `_cgo_export.h` 파일을 사용합니다.
이 파일은 `//export` 줄이 포함된 패키지에 대해 생성됩니다.
`_cgo_export.h` 파일은 이제 C 프리앰블 주석으로 시작합니다.
이를 통해 내보낸 함수 정의가 해당 정의에 정의된 유형을 사용할 수 있습니다.
이는 프리앰블을 여러 번 컴파일하는 효과를 발생시키므로, `//export`를 사용하는 패키지는 함수 정의 또는 변수 초기화를 C 프리앰블에 넣지 않아야 합니다.

## 패키지 배포 {#releases}

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, world!")
}
```

## 패키지 배포에 대한 정보

Go 1과 관련된 가장 중요한 변화 중 하나는 사전 패키징된, 다운로드 가능한 배포판의 가용성입니다.
이들은 다양한 아키텍처 및 운영 체제 조합(Windows 포함)에 대해 제공되며, 목록은 계속 확장될 예정입니다.
설치 방법에 대한 자세한 내용은 [시작하기](/doc/install) 페이지에 설명되어 있으며, 배포판 자체는 [다운로드 페이지](/dl/)에 나열되어 있습니다.
