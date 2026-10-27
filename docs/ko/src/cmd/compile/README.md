<!---
// Copyright 2018 The Go Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.
-->

## Go 컴파일러 소개

`cmd/compile`은 Go 컴파일러를 구성하는 주요 패키지들을 포함하고 있습니다. 컴파일러는 논리적으로 네 가지 단계로 나눌 수 있으며, 해당 코드가 포함된 패키지 목록과 함께 각 단계에 대해 간략히 설명하겠습니다.

컴파일러를 언급할 때 때때로 "프런트엔드(front-end)"와 "백엔드(back-end)"라는 용어를 듣게 될 것입니다. 대략적으로 말하자면, 이는 여기에 나열할 단계들 중 처음 두 단계와 마지막 두 단계에 해당합니다. 세 번째 용어인 "미들엔드(middle-end)"는 종종 두 번째 단계에서 일어나는 많은 작업들을 지칭합니다.

`go/parser` 및 `go/types`와 같은 `go/*` 패키지 제품군은 컴파일러에서 거의 사용되지 않는다는 점에 유의하십시오. 컴파일러가 처음에는 C로 작성되었기 때문에, `gofmt` 및 `vet`와 같이 Go 코드로 작동하는 도구들을 작성할 수 있도록 `go/*` 패키지들이 개발되었습니다. 하지만 시간이 흐르면서 컴파일러의 내부 API는 `go/*` 패키지 사용자들에게 더 친숙한 방향으로 서서히 발전해 왔습니다.

"gc"라는 이름은 "Go compiler"의 약자이며, 가비지 컬렉션을 의미하는 대문자 "GC"와는 거의 관련이 없다는 점을 분명히 해야 합니다.

### 1. 파싱(Parsing)

* `cmd/compile/internal/syntax` (렉서, 파서, 구문 트리)

컴파일의 첫 번째 단계에서는 소스 코드가 토큰화(어휘 분석)되고, 파싱(구문 분석)되며, 각 소스 파일에 대해 구문 트리(syntax tree)가 생성됩니다.

각 구문 트리(syntax tree)는 해당 소스 파일의 정확한 표현이며, 노드는 식(expressions), 선언(declarations), 문(statements)과 같이 소스의 다양한 요소에 대응합니다. 또한 구문 트리에는 오류 보고 및 디버깅 정보 생성에 사용되는 위치 정보가 포함됩니다.

### 2. 타입 체크 (Type checking)

* `cmd/compile/internal/types2` (타입 체킹)

types2 패키지는 `go/ast` 대신 syntax 패키지의 AST를 사용하도록 `go/types`를 포팅한 것입니다.

### 3. IR 생성 ("noding")

* `cmd/compile/internal/types` (컴파일러 타입)
* `cmd/compile/internal/ir` (컴파일러 AST)
* `cmd/compile/internal/noder` (컴파일러 AST 생성)

컴파일러 미들엔드는 C 언어로 작성되었을 당시부터 이어져 온 자체적인 AST 정의와 Go 타입 표현 방식을 사용합니다. 모든 코드가 이를 기반으로 작성되었으므로, 타입 체크 다음 단계는 syntax와 types 표현을 ir 및 types로 변환하는 것입니다. 이 과정을 "noding"이라고 합니다.

Noding은 Unified IR이라 불리는 프로세스를 사용하며, 이는 2단계의 타입 체크가 완료된 코드의 직렬화된 버전을 사용하여 노드 표현을 생성합니다.
Unified IR은 패키지의 임포트/익스포트(import/export) 및 인라이닝(inlining) 과정에도 관여합니다.

### 4. 미들엔드(Middle end)

* `cmd/compile/internal/inline` (함수 호출 인라이닝)
* `cmd/compile/internal/devirtualize` (알려진 인터페이스 메서드 호출의 역가상화)
* `cmd/compile/internal/escape` (탈출 분석)

IR 표현에 대해 다음과 같은 여러 최적화 패스가 수행됩니다:
데드 코드 제거(dead code elimination), (조기) 디버추얼라이제이션(devirtualization), 함수 호출 인라이닝(function call inlining), 그리고 이스케이프 분석(escape analysis).

초기 데드 코드 제거(dead code elimination) 패스는 통합 IR 라이터(unified IR writer) 단계에 통합되어 있습니다.

### 5. Walk

* `cmd/compile/internal/walk` (평가 순서, 디슈가링)

IR 표현에 대한 마지막 단계는 "walk"이며, 이는 두 가지 목적을 수행합니다:

1. 이는 복잡한 문장을 개별적인 더 단순한 문장으로 분해하며, 임시 변수를 도입하고 평가 순서를 준수합니다. 이 단계를 "order"라고도 합니다.

2. 고수준의 Go 구문을 더 원시적인(primitive) 구문으로 디슈거링(desugar)합니다. 예를 들어, `switch` 문은 이진 탐색이나 점프 테이블로 변환되며, 맵(map)과 채널(channel)에 대한 연산은 런타임 호출로 대체됩니다.

### 6. Generic SSA

* `cmd/compile/internal/ssa` (SSA 패스와 규칙)
* `cmd/compile/internal/ssagen` (IR을 SSA로 변환)

이 단계에서 IR은 Static Single Assignment (SSA) 형태로 변환됩니다. SSA는 최적화를 구현하고 최종적으로 머신 코드를 생성하는 것을 더 쉽게 만드는 특정 속성들을 가진 하위 수준의 중간 표현입니다.

이 변환 과정에서 함수 인트린직(function intrinsics)이 적용됩니다. 이는 컴파일러가 상황에 따라 고도로 최적화된 코드로 대체하도록 학습된 특수 함수들입니다.

AST에서 SSA로의 변환 과정에서 일부 노드들은 컴파일러의 나머지 부분이 처리할 수 있도록 더 단순한 구성 요소로 낮춰집니다(lowered). 예를 들어, `copy` 내장 함수는 메모리 이동(memory moves)으로 대체되며, `range` 루프는 `for` 루프로 다시 작성됩니다. 역사적인 이유로 인해 현재로서는 이러한 작업 중 일부가 SSA 변환 전에 발생하지만, 장기적인 계획은 이 모든 과정을 이곳으로 옮기는 것입니다.

그 다음으로, 일련의 머신 독립적인 패스(pass)와 규칙들이 적용됩니다. 이들은 특정 컴퓨터 아키텍처에 구애받지 않으므로 모든 `GOARCH` 변형에서 실행됩니다. 이러한 패스에는 데드 코드 제거(dead code elimination), 불필요한 nil 체크 제거, 그리고 사용되지 않는 분기 제거 등이 포함됩니다. 일반적인 리라이트 규칙(rewrite rules)은 주로 식(expression)과 관련이 있으며, 예를 들어 일부 식을 상수 값으로 대체하거나 곱셈 및 부동 소수점 연산을 최적화하는 작업 등이 있습니다.

### 7. 머신 코드 생성

* `cmd/compile/internal/ssa` (SSA lowering 및 아키텍처별 패스)
* `cmd/internal/obj` (머신 코드 생성)

컴파일러의 머신 의존적 단계는 일반적인 값들을 머신 특정 변형으로 다시 쓰는 "lower" 패스와 함께 시작됩니다. 예를 들어, amd64에서는 메모리 피연산자가 가능하므로 많은 load-store 연산을 결합할 수 있습니다.

하위 패스(lower pass)는 모든 머신 전용 rewrite 규칙을 실행하며, 따라서 현재 많은 최적화도 함께 적용한다는 점에 유의하십시오.

SSA가 "낮춰져(lowered)" 타겟 아키텍처에 더 구체화되면, 최종 코드 최적화 패스들이 실행됩니다. 여기에는 또 다른 데드 코드 제거(dead code elimination) 패스, 값들을 사용처에 더 가깝게 이동시키는 작업, 한 번도 읽히지 않는 지역 변수의 제거, 그리고 레지스터 할당(register allocation)이 포함됩니다.

이 단계의 일부로 수행되는 다른 중요한 작업에는 지역 변수에 스택 오프셋을 할당하는 스택 프레임 레이아웃(stack frame layout)과, 각 GC 세이프포인트(safe point)에서 스택상의 어떤 포인터가 살아있는지 계산하는 포인터 라이브니스 분석(pointer liveness analysis)이 포함됩니다.

SSA 생성 단계의 끝에서, Go 함수들은 일련의 `obj.Prog` 명령어로 변환됩니다. 이 명령어들은 어셈블러(`cmd/internal/obj`)로 전달되며, 어셈블러는 이를 머신 코드로 변환하여 최종 오브젝트 파일을 작성합니다. 오브젝트 파일에는 reflect 데이터, export 데이터 및 디버깅 정보도 포함됩니다.

### 7a. Export

컴파일러는 링커를 위한 오브젝트 코드 파일을 작성하는 것 외에도, 하위 컴파일 단위(downstream compilation units)를 위한 "export data" 파일을 작성합니다. export data 파일은 패키지 P를 직접 임포트하는 패키지 Q를 컴파일할 때 필요할 수 있는, 패키지 P의 컴파일 과정에서 계산된 모든 정보를 보유합니다. 여기에는 모든 export 된 선언에 대한 타입 정보, 인라이닝 대상이 되는 함수 본문의 IR, 다른 패키지에서 인스턴스화될 수 있는 제네릭 함수 본문의 IR, 그리고 함수 파라미터에 대한 탈출 분석(escape analysis) 결과 요약이 포함됩니다.

내보내기 데이터 파일의 형식은 여러 차례의 반복적인 개선 과정을 거쳤습니다. 현재의 형태는 "unified"라고 불리며, 이는 객체 그래프의 직렬화된 표현입니다. 또한 인덱스를 통해 전체 중 일부만 지연 디코딩(lazy decoding)할 수 있도록 하여, 대부분의 임포트가 소수의 심볼만 제공하는 데 사용된다는 점을 활용합니다. unified IR을 변경하는 방법에 대한 자세한 내용은 [여기](internal/noder/README.md)를 참조하십시오.

GOROOT 저장소에는 통합 포맷(unified format)을 위한 reader와 writer가 포함되어 있으며, 이는 컴파일러의 IR로 인코딩/디코딩합니다.
golang.org/x/tools 저장소 또한 export 데이터 reader(go/types 표현 사용)를 위한 공개 API를 제공하며, 이는 항상 컴파일러의 최신 파일 포맷과 소수의 과거 버전을 지원합니다.
(이는 타입 정보는 필요하지만 타입 주석이 달린 구문은 필요하지 않은 모드에서 x/tools/go/packages에 의해 사용됩니다.)

x/tools 저장소는 이전의 "indexed" 형식을 사용하여 내보낸(exported) 타입 정보(그 외의 내용은 없음)를 읽고 쓰기 위한 공개 API도 제공합니다. (예를 들어, gopls는 타입 정보를 포함하는 워크스페이스 정보 데이터베이스를 위해 이 버전을 사용합니다.)

내보내기 데이터(Export data)는 보통 "깊은(deep)" 요약을 제공합니다. 따라서 패키지 Q를 컴파일할 때 각 직접 임포트(direct import)에 대한 내보내기 데이터 파일만 읽어도, P의 퍼블릭 API에서 참조되는 타입의 메서드나 구조체 필드와 같이 간접 임포트(indirect import)에 있는 선언에 대한 모든 필요한 정보가 제공됨을 보장받을 수 있습니다. 깊은 내보내기 데이터는 직접 종속성당 하나의 파일만 필요하므로 빌드 시스템 입장에서 더 간단합니다. 하지만 대규모 리포지토리의 임포트 그래프 상단으로 갈수록 데이터가 커지는 경향이 있습니다. 예를 들어, API 규모가 큰 매우 흔히 사용되는 타입 세트가 있다면 거의 모든 패키지의 내보내기 데이터에 그 복사본이 포함될 것입니다. 이러한 문제가 필요에 따라 부분 로딩을 허용하는 "인덱싱된(indexed)" 설계의 동기가 되었습니다.

(gopls는 각 임포트에 대해 컴파일러보다 적은 작업을 수행하므로 내보내기 데이터 오버헤드에 더 민감합니다. 이러한 이유로 gopls는 간접 정보가 전혀 기록되지 않는 "얕은(shallow)" 내보내기 데이터를 사용합니다. 이는 모든 종속성의 내보내기 데이터 파일에 대한 무작위 액세스(random access)를 요구하므로, 분산 빌드 시스템에는 적합하지 않습니다.)

### 8. 팁

#### 시작하기

* 이전에 컴파일러에 기여한 적이 없다면, 조사 중인 내용에 대해 초기 통찰을 얻기 위해 로그 문을 추가하거나 `panic("here")`를 삽입하는 것이 시작하기 위한 간단한 방법이 될 수 있습니다.

* 컴파일러 자체적으로 다음과 같은 로깅, 디버깅 및 시각화 기능을 제공합니다:
   ```
   $ go build -gcflags=-m=2                   # 인라이닝, 이스케이프 분석을 포함한 최적화 정보 출력
   $ go build -gcflags=-d=ssa/check_bce/debug # 경계 검사(bounds check) 정보 출력
   $ go build -gcflags=-W                     # 타입 체크 후의 내부 파스 트리(parse tree) 출력
   $ GOSSAFUNC=Foo go build                   # func Foo에 대한 ssa.html 파일 생성
   $ go build -gcflags=-S                     # 어셈블리 출력
   $ go tool compile -bench=out.txt x.go      # 컴파일러 단계별 소요 시간 출력
   ```

다음과 같이 일부 플래그는 컴파일러의 동작을 변경합니다:
   ```
   $ go tool compile -h file.go               # 첫 번째 컴파일 오류 발생 시 패닉 발생
   $ go build -gcflags=-d=checkptr=2          # 추가적인 unsafe 포인터 검사 활성화
   ```

추가적인 플래그가 많이 있습니다. 일부 설명은 다음 명령어를 통해 확인할 수 있습니다:
   ```
   $ go tool compile -h              # 컴파일러 플래그, 예: go build -gcflags='-m=1 -l'
   $ go tool compile -d help         # 디버그 플래그, 예: go build -gcflags=-d=checkptr=2
   $ go tool compile -d ssa/help     # ssa 플래그, 예: go build -gcflags=-d=ssa/prove/debug=2
   ```

`-gcflags`에 대한 추가 세부 사항과 `go build`와 `go tool compile`의 차이점은 [아래 섹션](#-gcflags-and-go-build-vs-go-tool-compile)에 설명되어 있습니다.

* 일반적으로 컴파일러의 문제를 조사할 때는 가능한 한 가장 단순한 재현 사례부터 시작하여, 그 사례에서 정확히 어떤 일이 일어나고 있는지 이해하는 것이 좋습니다.

#### 변경 사항 테스트하기

* Go 기여 가이드의 [Quickly testing your changes](https://go.dev/doc/contribute#quick_test) 섹션을 반드시 읽어보시기 바랍니다.

* 일부 테스트는 `cmd/compile` 패키지 내에 있으며 `go test ./...` 또는 이와 유사한 명령어로 실행할 수 있지만, 많은 `cmd/compile` 테스트는 최상위 [test](https://github.com/golang/go/tree/master/test) 디렉토리에 있습니다:

```
  $ go test cmd/internal/testdir                           # 'test' 디렉토리의 모든 테스트 실행
  $ go test cmd/internal/testdir -run='Test/escape.*.go'   # 'test' 디렉토리 내 특정 파일 테스트 실행
  ```
  자세한 내용은 [testdir README](https://github.com/golang/go/tree/master/test#readme)를 참조하십시오.
  [testdir_test.go](https://github.com/golang/go/blob/master/src/cmd/internal/testdir/testdir_test.go)의 `errorCheck` 메서드는 해당 테스트들에서 많이 사용되는 `ERROR` 주석에 대한 설명을 확인하는 데 유용합니다.

또한, 표준 라이브러리의 `go/types` 패키지와 `cmd/compile/internal/types2`는 `src/internal/types/testdata`에 공유 테스트를 가지고 있으며, 해당 경로에서 변경 사항이 발생할 경우 두 타입 체커를 모두 확인해야 합니다.

* 새로운 [application-based coverage profiling](https://go.dev/testing/coverage/)은 다음과 같이 컴파일러와 함께 사용할 수 있습니다:

```
  $ go install -cover -coverpkg=cmd/compile/... cmd/compile  # 커버리지 계측을 포함하여 컴파일러 빌드
  $ mkdir /tmp/coverdir                                      # 커버리지 데이터 저장 위치 지정
  $ GOCOVERDIR=/tmp/coverdir go test [...]                   # 컴파일러를 사용하여 테스트하고 커버리지 데이터 저장
  $ go tool covdata textfmt -i=/tmp/coverdir -o coverage.out # 기존 커버리지 형식으로 변환
  $ go tool cover -html coverage.out                         # 기존 도구를 통해 커버리지 확인
  ```

#### 컴파일러 버전 관리하기

* 컴파일러 테스트의 상당수는 PATH에서 찾은 `go` 명령어 버전과 그에 해당하는 `compile` 바이너리를 사용합니다.

* 만약 특정 브랜치에 있고 PATH에 `<go-repo>/bin`이 포함되어 있다면, `go install cmd/compile`을 실행하여 해당 브랜치의 코드로 컴파일러를 빌드하고 적절한 위치에 설치할 수 있습니다. 이렇게 하면 `go build` 또는 `go test ./...`와 같은 이후의 `go` 명령들이 방금 빌드한 컴파일러를 사용하게 됩니다.

* [toolstash](https://pkg.go.dev/golang.org/x/tools/cmd/toolstash)는 Go 툴체인의 검증된 복사본을 저장, 실행 및 복구하는 방법을 제공합니다. 예를 들어, 처음에 브랜치를 빌드하고 해당 버전의 툴체인을 저장한 다음, 작업 중인 컴파일러 버전을 컴파일하기 위해 검증된 도구 버전을 복구하는 것이 좋은 관행이 될 수 있습니다.

설치 단계 예시:
  ```
  $ go install golang.org/x/tools/cmd/toolstash@latest
  $ git clone https://go.googlesource.com/go
  $ export PATH=$PWD/go/bin:$PATH
  $ cd go/src
  $ git checkout -b mybranch
  $ ./all.bash                      # 빌드 및 정상적인 시작점인지 확인
  $ toolstash save                  # 현재 도구 저장
  ```
  그 후, 수정/컴파일/테스트 사이클은 다음과 같이 진행할 수 있습니다:
  ```
  [... cmd/compile 소스 수정 ...]
  $ toolstash restore && go install cmd/compile   # 컴파일러 빌드를 위해 검증된 도구 복구
  [... 'go build', 'go test' 등 실행 ...]           # 새로 빌드된 컴파일러 사용
  ```

* toolstash를 사용하면 설치된 컴파일러와 저장된(stashed) 컴파일러 복사본을 비교할 수 있으며, 이는 리팩토링 후에도 동일한 동작을 기대하는 경우 등에 유용합니다. 예를 들어, 표준 라이브러리를 빌드하는 동안 변경된 컴파일러가 저장된 컴파일러와 동일한 오브젝트 파일을 생성하는지 확인하려면 다음과 같이 수행하십시오:
  ```
  $ toolstash restore && go install cmd/compile   # 최신 컴파일러 빌드
  $ go build -toolexec "toolstash -cmp" -a -v std # 최신 컴파일러와 저장된 컴파일러 비교
  ```

* 버전이 서로 일치하지 않는 것으로 보일 경우 (예: `devel go1.21-db3f952b1f`와 같은 버전 문자열과 함께 `linked object header mismatch` 같은 에러가 발생하는 경우), `toolstash restore && go install cmd/...`를 실행하여 `cmd` 하위의 모든 도구를 업데이트해야 할 수도 있습니다.

#### 추가로 유용한 도구들

* [compilebench](https://pkg.go.dev/golang.org/x/tools/cmd/compilebench)는 컴파일러의 속도를 벤치마크합니다.

* [benchstat](https://pkg.go.dev/golang.org/x/perf/cmd/benchstat)는 컴파일러 수정으로 인한 성능 변화를 보고하기 위한 표준 도구이며, 개선 사항이 통계적으로 유의미한지 여부를 포함하여 알려줍니다:
  ```
  $ go test -bench=SomeBenchmarks -count=20 > new.txt   # 새 컴파일러 사용
  $ toolstash restore                                   # 이전 컴파일러로 복구
  $ go test -bench=SomeBenchmarks -count=20 > old.txt   # 이전 컴파일러 사용
  $ benchstat old.txt new.txt                           # 이전 버전과 새 버전 비교
  ```

* [bent](https://pkg.go.dev/golang.org/x/benchmarks/cmd/bent)는 Docker 컨테이너 내부에서 다양한 커뮤니티 Go 프로젝트의 대규모 벤치마크 세트를 실행하는 것을 용이하게 합니다.

* [perflock](https://github.com/aclements/perflock)는 Linux에서 CPU 주파수 스케일링 설정을 조작하는 등의 방법을 통해 더 일관된 벤치마크 결과를 얻을 수 있도록 도와줍니다.

* [view-annotated-file](https://github.com/loov/view-annotated-file) (커뮤니티 제공)
   인라이닝(inlining), 경계 검사(bounds check) 및 이스케이프 정보(escape info)를 소스 코드 위에 오버레이로 표시합니다.

* [godbolt.org](https://go.godbolt.org)는 Go 컴파일터를 포함한 많은 컴파일러의 어셈블리 출력 결과를 확인하고 공유하는 데 널리 사용됩니다. 또한 함수의 서로 다른 버전이나 Go 컴파일터 버전 간의 어셈블리를 [비교](https://go.godbolt.org/z/5Gs1G4bKG)할 수 있어, 조사 및 버그 보고 시 유용하게 활용될 수 있습니다.

#### -gcflags와 'go build' vs. 'go tool compile'

* `-gcflags`는 go 커맨드의 [빌드 플래그](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies)입니다.
  `go build -gcflags=<args>`는 `go build` 커맨드가 정상적으로 수행하는 모든 작업(예: 빌드 캐시 처리, 모듈 관리 등)을 그대로 수행하면서, 제공된 `<args>`를 내부의 `compile` 호출로 전달합니다. 반면, `go tool compile <args>`는 표준 `go build` 메커니즘을 거치지 않고 `go` 커맨드가 `compile <args>`를 단 한 번만 호출하도록 요청합니다. `go build`의 도움 없이 컴파일할 수 있는 작은 독립 소스 파일이 있는 경우처럼, `go tool compile <args>`를 통해 동작 과정을 단순화하는 것이 도움이 될 때가 있습니다. 다른 경우에는 `go build`, `go test` 또는 `go install`과 같은 빌드 커맨드에 `-gcflags`를 전달하는 것이 더 편리합니다.

* `-gcflags`는 기본적으로 명령줄에 지정된 패키지에 적용되지만, `-gcflags='all=-m=1 -l'`와 같은 패키지 패턴이나 `-gcflags='all=-m=1' -gcflags='fmt=-m=2'`와 같이 여러 개의 패키지 패턴을 사용할 수 있습니다. 자세한 내용은 [cmd/go 문서](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies)를 참조하십시오.

### 더 읽어보기

pass와 rule을 포함하여 SSA 패키지가 어떻게 작동하는지 더 자세히 알아보려면 [cmd/compile/internal/ssa/README.md](internal/ssa/README.md)를 참조하십시오.

마지막으로, 이 README나 SSA README에서 불분명한 점이 있거나 개선 아이디어가 있다면, 언제든지 [issue 30074](https://go.dev/issue/30074)에 의견을 남겨 주세요.
