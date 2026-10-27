<!--{
  "Title": "튜토리얼: 제네릭 시작하기",
  "Breadcrumb": true
}-->

이 튜토리얼에서는 Go 제네릭의 기초를 소개합니다. 제네릭을 사용하면 호출하는 코드에서 제공하는 일련의 타입 중 어느 것과도 동작하도록 작성된 함수나 타입을 선언하고 사용할 수 있습니다.

이 튜토리얼에서는 두 개의 단순한 비제네릭(non-generic) 함수를 선언한 다음, 동일한 로직을 하나의 제네릭 함수로 캡처하는 방법을 배웁니다.

다음 섹션들을 통해 학습을 진행하시게 됩니다:

1. 코드를 위한 폴더를 생성합니다.
2. 제네릭이 아닌 함수를 추가합니다.
3. 여러 타입을 처리할 수 있는 제네릭 함수를 추가합니다.
4. 제네릭 함수를 호출할 때 타입 인자를 제거합니다.
5. 타입 제약(type constraint)을 선언합니다.

**참고:** 다른 튜토리얼은 [Tutorials](/doc/tutorial/index.html)를 참조하십시오.

## 사전 요구 사항

*   **Go.** 이 튜토리얼을 따라 하기 위해 최신 버전의 Go를 사용하는 것을 권장합니다.
    설치 방법은 [Installing Go](/doc/install)를 참조하세요.
*   **코드 편집 도구.** 사용 중인 어떤 텍스트 에디터든 상관없습니다.
*   **명령어 터미널.** Go는 Linux 및 Mac의 모든 터미널, 그리고 Windows의 PowerShell 또는 cmd에서 잘 작동합니다.

## 코드를 위한 폴더 생성 {#create_folder}

먼저, 작성할 코드를 저장할 폴더를 생성하세요.

1. 명령 프롬프트를 열고 홈 디렉터리로 이동하십시오.

Linux 또는 Mac에서:

```
    $ cd
    ```

Windows에서:

```
    C:\> cd %HOMEPATH%
    ```

이 튜토리얼의 나머지 부분에서는 프롬프트로 `$`가 표시됩니다. 사용하는 명령어들은 Windows에서도 동일하게 작동합니다.

2. 명령 프롬프트에서 코드를 위한 `generics`라는 이름의 디렉토리를 생성하세요.

```
    $ mkdir generics
    $ cd generics
    ```

3. 코드를 저장할 모듈을 생성합니다.

`go mod init` 명령어를 실행하고, 새로 작성한 코드의 모듈 경로를 지정하십시오.

```
    $ go mod init example/generics
    go: creating new go.mod: module example/generics
    ```

**참고:** 프로덕션 코드에서는 자신의 필요에 더 구체적인 모듈 경로를 지정해야 합니다. 자세한 내용은 [의존성 관리](/doc/modules/managing-dependencies)를 참조하세요.

다음으로, 맵(map)을 다루는 간단한 코드를 추가해 보겠습니다.

## non-generic 함수 추가 {#non_generic_functions}

이 단계에서는 맵의 값들을 각각 합산하여 총합을 반환하는 두 개의 함수를 추가하게 됩니다.

`int64` 값을 저장하는 맵과 `float64` 값을 저장하는 맵이라는 두 가지 서로 다른 타입의 맵을 다루고 있기 때문에, 하나의 함수 대신 두 개의 함수를 선언하고 있는 것입니다.

#### 코드 작성하기

1. 텍스트 편집기를 사용하여 `generics` 디렉토리에 `main.go`라는 파일을 생성하세요. 이 파일에 Go 코드를 작성하게 됩니다.
2. `main.go` 파일의 맨 위에 다음 패키지 선언을 붙여넣으세요.

```
    package main
    ```

독립 실행형 프로그램(라이브러리와 대조되는)은 항상 `main` 패키지에 속합니다.

3. 패키지 선언 아래에 다음 두 함수 선언을 붙여넣으세요.

```go
    // SumInts는 m의 값들을 모두 더합니다.
    func SumInts(m map[string]int64) int64 {
    	var s int64
    	for _, v := range m {
    		s += v
    	}
    	return s
    }
```

```go
    // SumFloats는 m의 값들을 모두 더합니다.
    func SumFloats(m map[string]float64) float64 {
    	var s float64
    	for _, v := range m {
    		s += v
    	}
    	return s
    }
    ```

이 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   맵의 값들을 모두 더해 그 합계를 반환하는 두 개의 함수를 선언하십시오.
    *   `SumFloats`는 `string`에서 `float64` 값으로 매핑되는 맵을 인자로 받습니다.
    *   `SumInts`는 `string`에서 `int64` 값으로 매핑되는 맵을 인자로 받습니다.

4. `main.go` 파일 상단의 package 선언 아래에 다음 `main` 함수를 붙여넣으세요. 이 함수는 두 개의 map을 초기화하고, 이전 단계에서 선언한 함수들을 호출할 때 이들을 인자로 사용합니다.

```go
    func main() {
    	// 정수 값을 위한 맵을 초기화합니다.
    	ints := map[string]int64{
    		"first":  34,
    		"second": 12,
    	}
```

// float 값들을 위한 map을 초기화합니다
    	floats := map[string]float64{
    		"first":  35.98,
    		"second": 26.99,
    	}

```go
    fmt.Printf("Non-Generic Sums: %v and %v\n",
    		SumInts(ints),
    		SumFloats(floats))
    }
    ```

이 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   `float64` 값들의 맵과 `int64` 값들의 맵을 각각 두 개의 항목으로 초기화하세요.
    *   앞서 선언한 두 함수를 호출하여 각 맵 값들의 합계를 구하세요.
    *   결과를 출력하세요.

5. `main.go` 파일의 상단, package 선언 바로 아래에서 방금 작성한 코드를 지원하는 데 필요한 패키지를 import 하세요.

코드의 첫 부분은 다음과 같아야 합니다:

```markdown
    package main
```

import "fmt"
    ```

6. `main.go`를 저장하세요.

#### 코드 실행하기

`main.go` 파일이 포함된 디렉토리의 명령줄에서 코드를 실행하세요.

```
$ go run .
Non-Generic Sums: 46 and 62.97
```

제네릭을 사용하면 여기서 두 개의 함수 대신 하나의 함수만 작성할 수 있습니다. 다음으로는 정수 또는 부동 소수점 값을 포함하는 맵을 위한 단일 제네릭 함수를 추가하게 됩니다.

## 여러 타입을 처리하기 위한 제네릭 함수 추가 {#add_generic_function}

이 섹션에서는 정수 또는 부동 소수점 값을 포함하는 맵을 받을 수 있는 단일 제네릭 함수를 추가하여, 방금 작성한 두 개의 함수를 하나의 함수로 효과적으로 대체하는 방법을 알아봅니다.

두 가지 타입의 값을 모두 지원하려면, 해당 단일 함수는 자신이 어떤 타입을 지원하는지 선언하는 방법이 필요합니다. 반면, 호출하는 코드에서는 정수 맵으로 호출하는지 아니면 부동 소수점 맵으로 호출하는지를 지정하는 방법이 필요할 것입니다.

이를 지원하기 위해, 일반 함수 매개변수 외에 _타입 매개변수(type parameters)_를 선언하는 함수를 작성하게 됩니다. 이러한 타입 매개변수는 함수를 제네릭(generic)하게 만들어, 서로 다른 타입의 인자와 함께 동작할 수 있게 합니다. 함수를 호출할 때는 _타입 인자(type arguments)_와 일반 함수 인자를 함께 전달하게 됩니다.

각 타입 파라미터는 해당 타입 파라미터의 일종의 메타 타입 역할을 하는 _타입 제약(type constraint)_을 가집니다. 각 타입 제약은 호출하는 코드에서 해당 타입 파라미터에 사용할 수 있는 허용 가능한 타입 인자(type arguments)를 지정합니다.

타입 파라미터의 제약 조건(constraint)은 일반적으로 타입들의 집합을 나타내지만, 컴파일 시점에 타입 파라미터는 단 하나의 타입, 즉 호출하는 코드에서 타입 인자(type argument)로 제공한 그 타입을 나타냅니다. 만약 타입 인자의 타입이 타입 파라미터의 제약 조건에 의해 허용되지 않는다면, 코드는 컴파일되지 않습니다.

타입 파라미터는 제네릭 코드가 해당 파라미터에 대해 수행하는 모든 연산을 지원해야 한다는 점을 유념하십시오. 예를 들어, 제약 조건에 숫자 타입이 포함된 타입 파라미터에 대해 (인덱싱과 같은) `string` 연산을 수행하려고 하면 코드가 컴파일되지 않습니다.

작성하게 될 코드에서는 정수형 또는 부동 소수점형 타입을 모두 허용하는 제약 조건(constraint)을 사용하게 됩니다.

#### 코드 작성하기

1. 이전에 추가한 두 함수 아래에 다음 제네릭(generic) 함수를 붙여넣으세요.

```
    // SumIntsOrFloats는 맵 m의 값들을 합산합니다. 맵 값의 타입으로 int64와 float64를 모두 지원합니다.
    func SumIntsOrFloats[K comparable, V int64 | float64](m map[K]V) V {
        var s V
        for _, v := range m {
            s += v
        }
        return s
    }
    ```

이 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   두 개의 타입 파라미터 `K`와 `V`(대괄호 안에 작성)와, 이 타입 파라미터들을 사용하는 하나의 인자 `map[K]V` 타입의 `m`을 가진 `SumIntsOrFloats` 함수를 선언하세요. 이 함수는 `V` 타입의 값을 반환합니다.
    *   `K` 타입 파라미터에 대해 `comparable` 타입 제약 조건을 지정하세요. 특별히 이러한 경우를 위해 설계된 `comparable` 제약 조건은 Go에 미리 선언되어 있습니다. 이는 비교 연산자 `==` 및 `!=`의 피연산자로 사용할 수 있는 모든 타입을 허용합니다. Go는 맵의 키가 반드시 비교 가능할 것을 요구합니다. 따라서 `K`를 `comparable`로 선언해야 `K`를 맵 변수의 키로 사용할 수 있습니다. 또한 이는 호출하는 코드에서 맵 키로 허용되는 타입을 사용하도록 보장합니다.
    *   `V` 타입 파라미터에 대해 두 타입 `int64`와 `float64`의 유니온(union) 제약 조건을 지정하세요. `|`를 사용하면 두 타입의 유니온을 지정하며, 이는 이 제약 조건이 두 타입 중 하나를 허용함을 의미합니다. 호출하는 코드에서 이 두 타입 중 어느 것을 인자로 사용하더라도 컴파일러가 허용합니다.
    *   `m` 인자가 `map[K]V` 타입임을 지정하세요. 여기서 `K`와 `V`는 앞서 타입 파라미터로 지정한 타입들입니다. `K`가 비교 가능한 타입이므로 `map[K]V`가 유효한 맵 타입이라는 점에 유의하세요. 만약 `K`를 `comparable`로 선언하지 않았다면, 컴파일러는 `map[K]V` 참조를 거부했을 것입니다.

2. `main.go` 파일의 기존 코드 아래에 다음 코드를 붙여넣으세요.

```
    fmt.Printf("Generic Sums: %v and %v\n",
    	SumIntsOrFloats[string, int64](ints),
    	SumIntsOrFloats[string, float64](floats))
    ```

이 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   방금 선언한 제네릭 함수를 호출하며, 생성한 각 맵을 전달하세요.
    *   호출하는 함수의 타입 파라미터를 대체할 타입을 명확히 하기 위해 대괄호 `[]` 안에 타입 인자를 지정하세요.

다음 섹션에서 보시겠지만, 함수 호출 시 타입 인자를 생략할 수 있는 경우가 많습니다. Go는 코드로부터 이를 추론할 수 있기 때문입니다.
    *   함수가 반환한 합계를 출력하세요.

#### 코드 실행하기

`main.go` 파일이 포함된 디렉토리의 명령줄에서 코드를 실행하세요.

```
$ go run .
Non-Generic Sums: 46 and 62.97
Generic Sums: 46 and 62.97
```

코드를 실행하기 위해, 컴파일러는 각 호출 시 타입 파라미터를 해당 호출에서 지정된 구체적인 타입으로 대체했습니다.

작성한 제네릭 함수를 호출할 때, 함수의 타입 파라미터 대신 사용할 타입을 컴파일러에게 알려주는 타입 인자(type arguments)를 지정했습니다. 다음 섹션에서 살펴보겠지만, 많은 경우 컴파일러가 이를 추론할 수 있으므로 이러한 타입 인자를 생략할 수 있습니다.

## 제네릭 함수 호출 시 타입 인자 제거 {#remove_type_arguments}

이 섹션에서는 제네릭 함수 호출의 수정된 버전을 추가하여, 호출 코드를 단순화하기 위한 작은 변경 사항을 적용하겠습니다. 이 경우에는 필요하지 않은 타입 인자(type arguments)를 제거할 것입니다.

Go 컴파일러가 사용하려는 타입을 추론할 수 있는 경우, 호출 코드에서 타입 인자를 생략할 수 있습니다. 컴파일러는 함수 인자의 타입을 통해 타입 인자를 추론합니다.

이것이 항상 가능한 것은 아니라는 점에 유의하십시오. 예를 들어, 인자가 없는 제네릭 함수를 호출해야 하는 경우, 함수 호출 시 타입 인자(type arguments)를 포함해야 합니다.

#### 코드 작성하기

*   `main.go` 파일에서 기존 코드 아래에 다음 코드를 붙여넣으세요.

```
    fmt.Printf("Generic Sums, type parameters inferred: %v and %v\n",
    	SumIntsOrFloats(ints),
    	SumIntsOrFloats(floats))
    ```

이 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   타입 인수를 생략하고 제네릭 함수를 호출합니다.

#### 코드 실행하기

`main.go` 파일이 포함된 디렉토리의 커맨드 라인에서 코드를 실행하세요.

```
$ go run .
Non-Generic Sums: 46 and 62.97
Generic Sums: 46 and 62.97
Generic Sums, type parameters inferred: 46 and 62.97
```

다음으로, 정수와 부동 소수점의 합집합을 재사용 가능한 타입 제약(type constraint)으로 캡처하여 함수를 더욱 단순화하겠습니다. 이렇게 하면 다른 코드에서도 해당 제약을 사용할 수 있습니다.

## 타입 제약 선언하기 {#declare_type_constraint}

이 마지막 섹션에서는 이전에 정의한 제약 조건(constraint)을 별도의 인터페이스로 이동하여 여러 곳에서 재사용할 수 있도록 하겠습니다. 이렇게 제약 조건을 선언하면, 특히 제약 조건이 복잡할 때 코드를 효율적으로 간소화하는 데 도움이 됩니다.

_타입 제약(type constraint)_은 인터페이스로 선언합니다. 이 제약은 해당 인터페이스를 구현하는 모든 타입을 허용합니다. 예를 들어, 세 개의 메서드를 가진 타입 제약 인터페이스를 선언하고 이를 제네릭 함수의 타입 파라미터와 함께 사용한다면, 해당 함수를 호출하는 데 사용되는 타입 인자들은 반드시 그 모든 메서드들을 가지고 있어야 합니다.

제약 인터페이스(Constraint interfaces)는 이 섹션에서 보시게 될 것처럼 특정 타입을 참조할 수도 있습니다.

#### 코드 작성하기

1. `main` 바로 위, import 문 직후에 다음 코드를 붙여넣어 타입 제약(type constraint)을 선언하십시오.

```
    type Number interface {
        int64 | float64
    }
    ```

이 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   타입 제약 조건(type constraint)으로 사용할 `Number` 인터페이스 타입을 선언합니다.
    *   인터페이스 내부에 `int64`와 `float64`의 유니온(union)을 선언합니다.

기본적으로, 유니온(union)을 함수 선언부에서 새로운 타입 제약(type constraint)으로 옮기는 것입니다. 그렇게 하면 타입 파라미터를 `int64` 또는 `float64`로 제한하고 싶을 때, `int64 | float64`라고 일일이 쓰는 대신 이 `Number` 타입 제약을 사용할 수 있습니다.

2. 기존에 작성한 함수들 아래에 다음의 제네릭 `SumNumbers` 함수를 붙여넣으세요.

```
    // SumNumbers는 맵 m의 값들의 합계를 구합니다. 맵 값으로 정수와 부동 소수점 숫자를 모두 지원합니다.
    func SumNumbers[K comparable, V Number](m map[K]V) V {
        var s V
        for _, v := range m {
            s += v
        }
        return s
    }
    ```

이 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   이전에 선언했던 제네릭 함수와 동일한 로직을 가진 제네릭 함수를 선언하되, 타입 제약 조건으로 union 대신 새로운 인터페이스 타입을 사용하세요. 이전과 마찬가지로 인수와 반환 타입에 타입 매개변수를 사용합니다.

3. `main.go` 파일에서 기존에 작성한 코드 아래에 다음 코드를 붙여넣으세요.

```
    fmt.Printf("Generic Sums with Constraint: %v and %v\n",
    	SumNumbers(ints),
    	SumNumbers(floats))
    ```

이 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   각 맵에 대해 `SumNumbers`를 호출하고, 각 맵의 값들의 합계를 출력합니다.

앞선 섹션에서와 마찬가지로, 제네릭 함수를 호출할 때 타입 인자(대괄호 안의 타입 이름)를 생략할 수 있습니다. Go 컴파일러는 다른 인자들을 통해 타입 인자를 추론할 수 있습니다.

#### 코드 실행하기

`main.go` 파일이 포함된 디렉토리의 커맨드 라인에서 코드를 실행하세요.

```
$ go run .
Non-Generic Sums: 46 and 62.97
Generic Sums: 46 and 62.97
Generic Sums, type parameters inferred: 46 and 62.97
Generic Sums with Constraint: 46 and 62.97
```

## 결론 {#conclusion}

잘 하셨습니다! 방금 Go의 제네릭(generics)에 대해 알아보았습니다.

추천 다음 주제:

*   [Go Tour](/tour/)는 Go의 기초를 단계별로 배울 수 있는 훌륭한 입문서입니다.
*   [Effective Go](/doc/effective_go)와 [How to write Go code](/doc/code)에서 유용한 Go 베스트 프랙티스를 확인하실 수 있습니다.

## 완성된 코드 {#completed_code}

이 프로그램은 [Go playground](/play/p/apNmfVwogK0)에서 실행할 수 있습니다. playground에서 **Run** 버튼을 클릭하기만 하면 됩니다.

```go
package main

import "fmt"

type Number interface {
	int64 | float64
}

func main() {
	// 정수 값을 위한 맵을 초기화합니다.
	ints := map[string]int64{
		"first": 34,
		"second": 12,
	}

	// 실수 값을 위한 맵을 초기화합니다.
	floats := map[string]float64{
		"first": 35.98,
		"second": 26.99,
	}

	fmt.Printf("Non-Generic Sums: %v and %v\n",
		SumInts(ints),
		SumFloats(floats))

	fmt.Printf("Generic Sums: %v and %v\n",
		SumIntsOrFloats[string, int64](ints),
		SumIntsOrFloats[string, float64](floats))

	fmt.Printf("Generic Sums, type parameters inferred: %v and %v\n",
		SumIntsOrFloats(ints),
		SumIntsOrFloats(floats))

	fmt.Printf("Generic Sums with Constraint: %v and %v\n",
		SumNumbers(ints),
		SumNumbers(floats))
}

// SumInts는 m의 값들을 모두 더합니다.
func SumInts(m map[string]int64) int64 {
	var s int64
	for _, v := range m {
		s += v
	}
	return s
}

// SumFloats는 m의 값들을 모두 더합니다.
func SumFloats(m map[string]float64) float64 {
	var s float64
	for _, v := range m {
		s += v
	}
	return s
}

// SumIntsOrFloats는 맵 m의 값들을 더합니다. 맵의 값으로 실수와 정수를 모두 지원합니다.
func SumIntsOrFloats[K comparable, V int64 | float64](m map[K]V) V {
	var s V
	for _, v := range m {
		s += v
	}
	return s
}

// SumNumbers는 맵 m의 값들을 더합니다. 맵의 값으로 정수와 실수를 모두 지원합니다.
func SumNumbers[K comparable, V Number](m map[K]V) V {
	var s V
	for _, v := range m {
		s += v
	}
	return s
}
```
