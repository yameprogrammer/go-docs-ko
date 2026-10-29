이 파일은 typechecker의 내부 구조와 컨벤션 중 일부를 설명합니다.
이 문서의 목적은 완전성을 기하는 것이 아니라, 필요에 따라 업데이트되는 살아있는 문서(living document)가 되는 것입니다.

코드에 변경 사항을 적용하기 전에 먼저 이 파일을 읽어주세요.

#
### 전체 구성

거의 동일한 두 개의 타입체커(typechecker)가 있습니다:

- `cmd/compile/internal/types2` (또는 짧게 `types2`)
- `go/types`

`types2`는 내부용이며 컴파일러에서 사용됩니다.
`go/types`는 표준 라이브러리 타입 체커이며, 그 API는 반드시 엄격하게 하위 호환성을 유지해야 합니다.
`types2` API는 `go/types` API와 매우 유사하지만, (`go/types`에서 유지해야 하는) 일부 더 이상 사용되지 않는(deprecated) 함수들은 포함하지 않을 수 있습니다.

이들은 주로 어떤 구문 트리(syntax tree)에서 작동하느냐에 따라 달라집니다.

- types2는 `cmd/compile/internal/syntax`에서 정의한 구문 트리를 사용합니다.
- go/types는 `go/ast`에서 정의한 구문 트리를 사용합니다.

우리는 각각의 소스를 매우 긴밀하게 동기화 상태로 유지하는 것을 목표로 합니다.
**모든 변경 사항은 두 typechecker 소스 베이스 모두에 적용되어야 합니다**.

많은 `go/types` 파일들은 그에 대응하는 `types2` 소스에서 자동으로 생성될 수 있습니다.
이는 `go/types` 디렉토리에서 `go generate`를 통해 호출할 수 있는 생성기(`go/types/generate_test.go`)를 통해 수행됩니다.
생성된 파일들은 상단의 주석으로 명확하게 표시되어 있으며, 수동으로 수정해서는 안 됩니다.
이러한 이유로, 보통 `types2` 소스를 먼저 수정하는 것이 가장 좋습니다.
아직 생성할 수 없는 `go/types` 파일들에 대해서만 변경 사항을 수동으로 반영하면 됩니다.

`generate_test.go`의 테이블에 해당 항목을 추가함으로써(그리고 필요한 경우 소스 변환 내용을 기술함으로써) 생성 파일 목록에 새 파일을 추가할 수 있습니다.

다음의 예제와 명령어들은 `types2`를 기준으로 하지만, 일반적으로 `go/types`에도 직접 적용됩니다.

#
### 테스트

주석이 달린 소스 파일 형태로 된 포괄적인 테스트 제품군이 제공됩니다.
테스트 파일은 다음 경로에 있습니다:

- src/internal/types/testdata/ (go/types와 types2 간에 공유됨)
- ./testdata/local (typechecker 로컬 테스트, 드문 상황에서만 사용)

테스트는 `/* ERROR "msg" */` 또는 `/* ERRORx "msg" */` 주석(또는 각각의 한 줄 주석 형태)이 작성된 .go 파일들입니다.
이러한 각 에러 주석에 대해, 해당 파일을 타입 체크(typechecking)했을 때 주석 _바로 앞에_ 위치한 구문 토큰(syntactic token)의 위치에서 에러가 보고되어야 합니다.
`ERROR`의 경우, `"msg"` 문자열은 타입 체커가 보고한 에러 메시지의 부분 문자열(substring)이어야 합니다.
`ERRORx`의 경우, `"msg"` 문자열은 보고된 에러와 일치하는 정규 표현식(regular expression)이어야 합니다.

typecheckers에서 수정된 각 이슈 #NNNN에 대해, `src/internal/types/testdata/fixedbugs/issueNNNN.go` 경로에 테스트를 추가해야 합니다.

#
### 디버깅

기존의 `./testdata/manual.go` 템플릿은 일시적인 디버깅 상황에서 편리하게 사용할 수 있습니다. 관심 있는 코드를 해당 파일에 작성한 후 `go test -run Manual`을 실행하면 해당 파일의 타입 체크(typecheck)를 수행합니다.

유용한 디버깅 플래그 (`go test -run Manual`과 함께 사용):

- -halt (패닉을 발생시키고 첫 번째 오류가 보고된 지점에서 스택 트레이스를 생성합니다)
- -v    (타입 체크 트레이스를 생성합니다)
- -verify       (manual.go의 `ERROR` 주석을 검증합니다)

#
### 자주 사용되는 타입 및 변수

#### Checker

파일: check.go

`Checker`는 패키지 타입 체크에 필요한 모든 타입 체크 상태를 유지합니다.
일반적으로 타입 체크 메서드들의 리시버 타입으로 사용됩니다.

#### 피연산자 (operand)

파일: operand.go

`operand`는 표현식의 타입과 값(있는 경우)을 설명합니다.
`operandMode`는 표현식의 종류(상수, 변수 등)를 설명합니다.
피연산자(Operand)는 표현식을 타입 체크(typechecking)한 주요 결과물입니다.
표현식의 타입 체크에 실패하면, 결과 피연산자의 모드는 `invalid`가 됩니다.

#### Typ

파일: universe.go

`Typ` 배열은 모든 사전 정의된 기본 타입에 대한 액세스를 제공합니다.
`Typ[Invalid]`는 유효하지 않은 타입을 나타내는 데 사용됩니다.

#
### 내부 코딩 컨벤션

#### Predicates

파일: predicates.go (자주 사용되는 predicate만 포함)

술어(Predicates)는 일반적으로 `isInteger`와 같이 `isX` 형태로 명명됩니다.

#### 표현식 타입 체크 (Type-checking expressions)

일반적으로 특정 표현식의 타입 체크를 위한 Checker 메서드가 존재합니다.
예를 들어, 단항 표현식을 타입 체크하는 `Checker.unary` 메서드가 있습니다.
이러한 함수 `f`의 기본 형태는 다음과 같습니다:
```
func (check *Checker) f(x *operand, e syntax.Expr, /* 추가 인자가 있는 경우 */)
```
표현식 `e`를 타입 체크한 결과는 operand `x`를 통해 반환됩니다
(이 `x`는 때때로 입력 인자로도 사용됩니다).
오류가 발생하면 함수 `f`는 오류를 보고하고 가능한 한 계속 진행하려고 시도하지만, 유효하지 않은 operand(`x.mode == invalid`)를 반환할 수 있습니다.
호출자는 유효하지 않은 operand인지 명시적으로 확인해야 할 수도 있습니다.

#
### TODO

제공해주신 원문 내용이 없습니다. 번역할 영문 마크다운 콘텐츠를 입력해 주시면, 요청하신 지침(구조 유지, 코드/식별자 보존 등)에 따라 정확하게 한국어로 번역해 드리겠습니다.
