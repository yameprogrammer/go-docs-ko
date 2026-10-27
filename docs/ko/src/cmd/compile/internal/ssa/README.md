<!---
// Copyright 2018 The Go Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.
-->

## Go 컴파일러의 SSA 백엔드 소개

이 패키지는 컴파일러의 정적 단일 할당(Static Single Assignment) 폼 컴포넌트를 포함하고 있습니다. SSA에 익숙하지 않으시다면, [Wikipedia 문서](https://en.wikipedia.org/wiki/Static_single_assignment_form)가 좋은 시작점이 될 것입니다.

Go 컴파일러에 익숙하지 않다면 먼저 [cmd/compile/README.md](../../README.md)를 읽어보시는 것을 권장합니다. 해당 문서에서는 컴파일러의 전반적인 개요를 제공하며, 그 안에서 SSA의 역할과 목적이 무엇인지 설명합니다.

### 핵심 개념

아래에 설명된 이름들은 대응하는 Go 개념들과 느슨하게 연관되어 있을 수 있지만, 서로 동일하지 않다는 점에 유의하십시오. 예를 들어, Go의 블록 문(block statement)은 변수 범위(variable scope)를 가지지만, SSA에는 변수나 변수 범위라는 개념이 없습니다.

값(values)과 블록(blocks)이 고유한 순차적 ID로 명명되었다는 점 또한 놀라울 수 있습니다. 이러한 ID는 변수나 함수 매개변수와 같이 원래 코드의 명명된 엔티티와 일치하는 경우가 드뭅니다. 또한 순차적 ID를 사용함으로써 컴파일러는 맵(maps) 사용을 피할 수 있으며, 디버그 및 위치 정보를 통해 항상 값을 Go 코드로 역추적하는 것이 가능합니다.

#### 값 (Values)

값(Value)은 SSA의 가장 기본적인 구성 요소입니다. SSA의 정의에 따라, 값은 정확히 한 번만 정의되지만, 여러 번 사용될 수 있습니다. 값은 주로 고유 식별자, 연산자, 타입 및 일부 인자로 구성됩니다.

연산자 또는 `Op`는 값을 계산하는 연산을 설명합니다. 각 연산자의 세맨틱은 `_gen/*Ops.go`에서 확인할 수 있습니다. 예를 들어, `OpAdd8`은 8비트 정수를 가진 두 개의 값 인수를 받아 그 합계를 결과로 냅니다. 다음은 두 `uint8` 값의 덧셈에 대한 가능한 SSA 표현입니다:

// var c uint8 = a + b
	v4 = Add8 <uint8> v2 v3

값의 타입은 보통 Go 타입입니다. 예를 들어, 위 예제에 있는 값은 `uint8` 타입이며, 상수 불리언 값은 `bool` 타입을 갖습니다. 하지만 일부 타입은 Go에서 오지 않는 특수한 타입입니다. 아래에서 그 중 가장 일반적인 `memory` 타입에 대해 다루겠습니다.

일부 연산자(operator)는 보조 필드(auxiliary field)를 포함합니다. 보조 필드는 보통 `[]` 또는 `{}`로 둘러싸여 출력되며, 상수 연산자 인자(constant op argument), 인자 타입(argument type) 등이 될 수 있습니다. 예를 들어:

v13 (?) = Const64 <int> [1]

여기서 `aux` 필드는 상수 연산 인자이며, 해당 연산은 1이라는 `Const64` 값을 생성하고 있습니다. 또 다른 예시입니다:

v17 (361) = Store <mem> {int} v16 v14 v8

여기서 `aux` 필드는 `Store`되는 값의 타입이며, 여기서는 `int`입니다.

더 자세한 내용은 [value.go](value.go)와 `_gen/*Ops.go`를 참조하세요.

#### 메모리 유형

`memory`는 전역 메모리 상태를 나타냅니다. 메모리 인자를 받는 `Op`는 해당 메모리 상태에 의존하며, 메모리 타입을 가진 `Op`는 메모리의 상태에 영향을 줍니다. 이를 통해 메모리 작업들이 올바른 순서로 유지되도록 보장합니다. 예를 들어:

// *a = 3
	// *b = *a
	v10 = Store <mem> {int} v6 v8 v1
	v14 = Store <mem> {int} v7 v8 v10

여기서 `Store`는 두 번째 인자(`int` 타입)를 첫 번째 인자(`*int` 타입)에 저장합니다. 마지막 인자는 메모리 상태입니다. 두 번째 store가 첫 번째 store에 의해 정의된 메모리 값에 의존하므로, 두 store의 순서를 바꿀 수 없습니다.

더 자세한 정보는 [cmd/compile/internal/types/type.go](../types/type.go)를 참조하십시오.

#### 블록 (Blocks)

블록(block)은 함수의 제어 흐름 그래프(control flow graph)에서 기본 블록(basic block)을 나타냅니다. 이는 본질적으로 해당 블록의 연산을 정의하는 값들의 리스트입니다. 값들의 리스트 외에도, 블록은 주로 고유 식별자(unique identifier), 종류(kind), 그리고 후속 블록(successor blocks)의 리스트로 구성됩니다.

가장 단순한 형태는 `plain` 블록입니다. 이는 단순히 제어 흐름을 다른 블록으로 전달하며, 따라서 후속(successors) 리스트에 하나의 블록만 포함합니다.

또 다른 일반적인 블록 종류는 `exit` 블록입니다. 이러한 블록은 제어 값(control value)이라고 불리는 최종 값을 가지며, 이는 반드시 메모리 상태(memory state)를 반환해야 합니다. 이는 함수가 일부 값을 반환하기 위해 필요한데, 예를 들어 호출자는 반환 값을 올바르게 수신하는 것을 보장하기 위해 의존할 수 있는 메모리 상태가 필요하기 때문입니다.

마지막으로 언급할 중요한 블록 종류는 `if` 블록입니다. 이 블록은 반드시 불리언(boolean) 값이어야 하는 단일 제어 값을 가지며, 정확히 두 개의 후속 블록을 가집니다. 불리언 값이 true이면 첫 번째 후속 블록으로 제어 흐름이 전달되고, 그렇지 않으면 두 번째 후속 블록으로 전달됩니다.

다음은 기본 블록(basic blocks)으로 표현된 if-else 제어 흐름의 예시입니다:

// func(b bool) int {
	// 	if b {
	// 		return 2
	// 	}
	// 	return 3
	// }
	b1:
	  v1 = InitMem <mem>
	  v2 = SP <uintptr>
	  v5 = Addr <*int> {~r1} v2
	  v6 = Arg <bool> {b}
	  v8 = Const64 <int> [2]
	  v12 = Const64 <int> [3]
	  If v6 -> b2 b3
	b2: <- b1
	  v10 = VarDef <mem> {~r1} v1
	  v11 = Store <mem> {int} v5 v8 v10
	  Ret v11
	b3: <- b1
	  v14 = VarDef <mem> {~r1} v1
	  v15 = Store <mem> {int} v5 v12 v14
	  Ret v15

<!---
TODO: 제어 흐름을 여전히 보여주면서도 더 짧은 예제를 만들 수 있을까요?
-->

더 자세한 정보는 [block.go](block.go)를 참조하십시오.

#### Functions

함수는 함수 선언과 그 본문(body)을 나타냅니다. 주로 이름, 타입(시그니처), 본문을 구성하는 블록 리스트, 그리고 해당 리스트 내의 진입 블록(entry block)으로 구성됩니다.

함수가 호출되면, 제어 흐름은 해당 함수의 진입 블록(entry block)으로 전달됩니다. 함수가 종료되면, 제어 흐름은 결과적으로 종료 블록(exit block)에 도달하여 함수 호출을 끝내게 됩니다.

함수는 Go 함수가 여러 개의 반환 지점을 가질 수 있는 것과 마찬가지로, 종료 블록(exit block)이 없을 수도 있고 여러 개일 수도 있지만, 진입 지점 블록(entry point block)은 반드시 정확히 하나만 있어야 한다는 점에 유의하십시오.

또한, 맵 키로 사용되는 각 타입에 대한 해시 함수와 같이 일부 SSA 함수는 자동으로 생성된다는 점에 유의하십시오.

예를 들어, 이는 SSA에서 빈 함수가 가질 수 있는 모습으로, 흥미롭지 않은 메모리 상태를 반환하는 단일 exit 블록을 포함하고 있습니다:

foo func()
	  b1:
	    v1 = InitMem <mem>
	    Ret v1

더 자세한 내용은 [func.go](func.go)를 참조하세요.

### 컴파일러 패스 (Compiler passes)

SSA 형태의 프로그램을 갖는 것 자체만으로는 그리 유용하지 않습니다. SSA의 장점은 프로그램을 더 효율적으로 개선하는 최적화 기법들을 작성하기가 매우 쉽다는 점에 있습니다. Go 컴파일러는 일련의 패스(pass) 목록을 통해 이를 수행합니다.

각 패스는 SSA 함수를 어떤 방식으로든 변환합니다. 예를 들어, 데드 코드 제거(dead code elimination) 패스는 절대 실행되지 않는다고 증명된 블록과 값을 제거하며, nil 체크 제거(nil check elimination) 패스는 중복된다고 증명된 nil 체크를 제거합니다.

컴파일러 패스(Compiler passes)는 한 번에 하나의 함수에 대해 작동하며, 기본적으로 순차적으로 정확히 한 번 실행됩니다.

`lower` 패스는 특별합니다. 이는 SSA 표현식을 머신 독립적(machine-independent)인 상태에서 머신 종속적(machine-dependent)인 상태로 변환합니다. 즉, 일부 추상 연산자들이 범용적이지 않은 대응 연산자로 대체되며, 이 과정에서 최종 값의 개수가 줄어들거나 늘어날 수 있습니다.

<!---
TODO: 패스(pass)의 순서가 왜 중요한지, 그리고 deadstore와 같은 일부 패스가 왜 서로 다른 단계에서 여러 변형(variant)으로 존재하는지 여기서 설명해야 할 것 같습니다.
-->

자세한 내용은 [compile.go](compile.go)에 정의된 `passes` 리스트를 참조하십시오.

### SSA 활용해 보기

컴파일러의 SSA가 실제로 어떻게 작동하는지 확인하고 익히는 좋은 방법은 `GOSSAFUNC`를 사용하는 것입니다. 예를 들어, `Foo` 함수의 초기 SSA 형태와 최종 생성된 어셈블리를 확인하려면 다음과 같이 실행하면 됩니다.

`GOSSAFUNC=Foo go build`

생성된 `ssa.html` 파일에는 각 컴파일 패스(compile pass)에서의 SSA 함수가 포함되어 있어, 각 패스가 특정 프로그램에 어떤 작업을 수행하는지 쉽게 확인할 수 있습니다. 또한 값(value)과 블록(block)을 클릭하여 강조 표시함으로써 제어 흐름과 값의 변화를 더 쉽게 추적할 수 있습니다.

`GOSSAFUNC`에 지정된 값은 패키지 경로가 포함된 함수 이름일 수도 있습니다. 예를 들어:

`GOSSAFUNC=blah.Foo go build`

이는 최종 접미사가 "blah"인 패키지 내의 "Foo"라는 이름을 가진 모든 함수와 일치합니다 (예: something/blah.Foo, anotherthing/extra/blah.Foo).

사용자는 다음과 같은 형식으로 `GOSSAFUNC` 값에 지정하여 제어 흐름 그래프(Control Flow Graph, CFG)를 출력할 수도 있습니다:

GOSSAFUNC="$FunctionName:$PassName1,$PassName2,..." go build

예를 들어, 다음 명령어는 `sccp` 및 `generic deadcode` 패스 열에 CFG가 첨부된 SSA를 출력합니다:

`GOSSAFUNC="blah.Foo:sccp,generic deadcode" go build`

non-HTML 덤프가 필요한 경우, `GOSSAFUNC` 값에 "+"를 추가하면 덤프가 stdout으로 출력됩니다:

`GOSSAFUNC=Bar+ go build`

<!---
TODO: 이 섹션에 더 많은 아이디어가 필요함
-->

### SSA 해킹하기

대부분의 컴파일러 패스는 Go 코드로 직접 구현되지만, 일부는 코드로 생성됩니다. 이는 현재 rewrite rule을 통해 수행되며, rewrite rule은 자체적인 구문을 가지며 `_gen/*.rules`에 유지 관리됩니다. 단순한 최적화는 이 방식으로 쉽고 빠르게 작성할 수 있지만, rewrite rule은 더 복잡한 최적화에는 적합하지 않습니다.

리라이트 규칙(rewrite rules)에 대해 더 자세히 알아보려면 [_gen/generic.rules](_gen/generic.rules) 및 [_gen/rulegen.go](_gen/rulegen.go) 파일 상단의 주석을 확인하십시오.

마찬가지로, 연산자를 관리하는 코드 또한 `_gen/*Ops.go`에서 생성된 코드입니다. 이는 방대한 양의 코드보다 몇 개의 테이블을 유지 관리하는 것이 더 쉽기 때문입니다. 규칙이나 연산자를 변경한 후에는 `go generate cmd/compile/internal/ssa`를 실행하여 Go 코드를 다시 생성하십시오.

<!---
TODO: 더 많은 팁과 정보가 여기에 추가될 수 있을 것 같습니다.
-->
