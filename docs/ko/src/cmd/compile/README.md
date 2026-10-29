<!---
// Copyright 2018 The Go Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.
-->

## Go 컴파일러 소개

`cmd/compile`에는 Go 컴파일러를 구성하는 주요 패키지들이 포함되어 있습니다. 컴파일러는 논리적으로 네 단계로 나눌 수 있으며, 해당 코드가 포함된 패키지 목록과 함께 각 단계를 간략하게 설명하겠습니다.

컴파일러를 언급할 때 때때로 "프런트엔드(front-end)"와 "백엔드(back-end)"라는 용어를 듣게 될 것입니다. 대략적으로 말하자면, 이는 여기서 나열할 단계들 중 처음 두 단계와 마지막 두 단계를 의미합니다. 세 번째 용어인 "미들엔드(middle-end)"는 주로 두 번째 단계에서 일어나는 많은 작업들을 지칭합니다.

`go/parser` 및 `go/types`와 같은 `go/*` 패키지 제품군은 컴파일러에서 거의 사용되지 않는다는 점에 유의하십시오. 컴파일러가 처음에는 C로 작성되었기 때문에, `go/*` 패키지들은 `gofmt` 및 `vet`과 같이 Go 코드를 다루는 도구들을 작성할 수 있도록 개발되었습니다. 하지만 시간이 흐르면서 컴파일러의 내부 API는 `go/*` 패키지 사용자들에게 더 익숙한 형태로 서서히 진화해 왔습니다.

"gc"라는 이름은 "Go compiler"의 약자이며, 가비지 컬렉션을 의미하는 대문자 "GC"와는 거의 관련이 없음을 분명히 해야 합니다.

### 1. 파싱(Parsing)

* `cmd/compile/internal/syntax` (렉서, 파서, 구문 트리)

컴파일의 첫 번째 단계에서 소스 코드는 토큰화(어휘 분석)되고, 파싱(구문 분석)되며, 각 소스 파일에 대한 구문 트리(syntax tree)가 생성됩니다.

각 구문 트리(syntax tree)는 해당 소스 파일의 정확한 표현이며, 노드는 식(expression), 선언(declaration), 문(statement)과 같은 소스의 다양한 요소에 대응합니다. 구문 트리에는 오류 보고 및 디버깅 정보 생성을 위해 사용되는 위치 정보도 포함됩니다.

### 2. 타입 체크 (Type checking)

* `cmd/compile/internal/types2` (타입 체크)

types2 패키지는 `go/ast` 대신 syntax 패키지의 AST를 사용하도록 `go/types`를 포팅한 것입니다.

### 3. IR 구성 ("noding")

* `cmd/compile/internal/types` (컴파일러 타입)
* `cmd/compile/internal/ir` (컴파일러 AST)
* `cmd/compile/internal/noder` (컴파일러 AST 생성)

컴파일러 미들엔드는 C 언어로 작성되었을 당시부터 이어져 온 자체적인 AST 정의와 Go 타입 표현 방식을 사용합니다. 모든 코드가 이를 기반으로 작성되어 있으므로, 타입 체크 이후의 다음 단계는 syntax 및 types 표현을 ir 및 types로 변환하는 것입니다. 이 과정을 "noding"이라고 합니다.

Noding은 Unified IR이라는 프로세스를 사용하며, 이는 2단계에서 타입 체크가 완료된 코드의 직렬화된 버전을 사용하여 노드 표현(node representation)을 구축합니다.
Unified IR은 패키지의 import/export 및 인라이닝(inlining) 작업에도 관여합니다.

### 4. 미들 엔드 (Middle end)

* `cmd/compile/internal/inline` (함수 호출 인라이닝)
* `cmd/compile/internal/devirtualize` (알려진 인터페이스 메서드 호출의 역가상화)
* `cmd/compile/internal/escape` (탈출 분석)

IR 표현 방식에 대해 다음과 같은 여러 최적화 패스가 수행됩니다:
dead code elimination, (early) devirtualization, function call
inlining, 그리고 escape analysis.

초기 데드 코드 제거(dead code elimination) 패스는 통합 IR 작성 단계(unified IR writer phase)에 통합되어 있습니다.

### 5. Walk

* `cmd/compile/internal/walk` (평가 순서, 디슈가링)

IR 표현에 대한 최종 패스는 "walk"이며, 이는 다음 두 가지 목적을 수행합니다:

1. 복잡한 문장을 개별적인 더 단순한 문장으로 분해하며, 임시 변수를 도입하고 평가 순서를 준수합니다. 이 단계는 "order"라고도 불립니다.

2. 고수준의 Go 구문을 더 원시적인 구문으로 디슈거링(desugars)합니다. 예를 들어,
   `switch` 문은 이진 탐색이나 점프 테이블로 변환되며,
   맵(map)과 채널(channel)에 대한 연산은 런타임 호출로 대체됩니다.

### 6. Generic SSA

* `cmd/compile/internal/ssa` (SSA 패스와 규칙)
* `cmd/compile/internal/ssagen` (IR을 SSA로 변환)

이 단계에서 IR은 정적 단일 할당(Static Single Assignment, SSA) 형태로 변환됩니다. SSA는 최적화를 구현하고 최종적으로 머신 코드를 생성하는 것을 더 쉽게 만드는 특정 속성들을 가진 더 낮은 수준의 중간 표현입니다.

이 변환 과정에서 함수 인트린직(function intrinsics)이 적용됩니다. 이는 컴파일러가 사례별로 고도로 최적화된 코드로 대체하도록 학습된 특수 함수입니다.

AST에서 SSA로 변환하는 동안 특정 노드들은 컴파일러의 나머지 부분이 처리할 수 있도록 더 단순한 컴포넌트로 로워링(lowered)됩니다. 예를 들어, `copy` 빌트인은 메모리 이동(memory moves)으로 대체되며, `range` 루프는 `for` 루프로 다시 작성됩니다. 역사적인 이유로 인해 이러한 작업 중 일부는 현재 SSA 변환 전에 발생하지만, 장기적인 계획은 이 모든 과정을 이곳으로 옮기는 것입니다.

그 다음으로, 일련의 머신 독립적(machine-independent) 패스와 규칙들이 적용됩니다. 이들은 특정 컴퓨터 아키텍처에 구애받지 않으므로 모든 `GOARCH` 변체에서 실행됩니다. 이러한 패스에는 데드 코드 제거(dead code elimination), 불필요한 nil 체크 제거, 사용되지 않는 분기 제거 등이 포함됩니다. 일반적인 재작성(rewrite) 규칙은 주로 식(expression)과 관련이 있으며, 일부 식을 상수 값으로 대체하거나 곱셈 및 부동 소수점 연산을 최적화하는 작업 등이 이에 해당합니다.

### 7. 머신 코드 생성

* `cmd/compile/internal/ssa` (SSA lowering 및 아키텍처별 패스)
* `cmd/internal/obj` (머신 코드 생성)

컴파일러의 머신 종속적(machine-dependent) 단계는 일반적인 값들을 머신별 변체로 다시 쓰는 "lower" 패스로 시작됩니다. 예를 들어, amd64에서는 메모리 피연산자(memory operands)가 가능하므로 많은 load-store 작업이 결합될 수 있습니다.

lower pass는 모든 머신별 rewrite rules를 실행하며, 이에 따라 현재 많은 최적화 작업도 함께 적용된다는 점에 유의하십시오.

SSA가 "낮춰져(lowered)" 타겟 아키텍처에 더 구체적으로 맞춰지면, 최종 코드 최적화 패스가 실행됩니다. 여기에는 또 다른 데드 코드 제거(dead code elimination) 패스, 값들을 사용처(use)에 더 가깝게 이동시키는 작업, 한 번도 읽히지 않는 지역 변수의 제거, 그리고 레지스터 할당(register allocation)이 포함됩니다.

이 단계의 일환으로 수행되는 다른 중요한 작업으로는 지역 변수에 스택 오프셋을 할당하는 스택 프레임 레이아웃(stack frame layout)과, 각 GC 세이프 포인트(safe point)에서 어떤 스택 내 포인터가 살아있는지 계산하는 포인터 라이브니스 분석(pointer liveness analysis)이 포함됩니다.

SSA 생성 단계의 끝에서, Go 함수들은 일련의 `obj.Prog` 명령어들로 변환됩니다. 이 명령어들은 어셈블러(`cmd/internal/obj`)로 전달되어 머신 코드로 변환되고, 최종 오브젝트 파일로 기록됩니다. 오브젝트 파일에는 reflect 데이터, export 데이터 및 디버깅 정보도 함께 포함됩니다.

### 7a. Export

링커를 위한 오브젝트 코드 파일을 작성하는 것 외에도, 컴파일러는 하위 컴파일 단위(downstream compilation units)를 위한 "내보내기 데이터(export data)" 파일을 작성합니다. 내보내기 데이터 파일은 패키지 P를 직접 임포트하는 패키지 Q를 컴파일할 때 필요할 수 있는, 패키지 P의 컴파일 과정에서 계산된 모든 정보를 보유합니다. 여기에는 모든 내보낸(exported) 선언에 대한 타입 정보, 인라이닝 대상이 되는 함수 본문의 IR, 다른 패키지에서 인스턴스화될 수 있는 제네릭 함수 본문의 IR, 그리고 함수 파라미터에 대한 탈출 분석(escape analysis) 결과의 요약본이 포함됩니다.

내보내기 데이터 파일의 형식은 여러 차례의 반복적인 변경 과정을 거쳤습니다. 현재의 형식은 "unified"라고 불리며, 이는 객체 그래프를 직렬화하여 표현한 것입니다. 또한 인덱스를 통해 전체 중 일부만 지연 디코딩(lazy decoding)할 수 있도록 하여, 대부분의 임포트가 소수의 심볼만을 제공하는 데 사용된다는 점을 고려했습니다. unified IR을 변경하는 방법에 대한 자세한 내용은 [여기](internal/noder/README.md)를 참조하십시오.

GOROOT 저장소에는 통합 포맷을 위한 reader와 writer가 포함되어 있으며, 이는 컴파일러의 IR로 인코딩/디코딩합니다.
golang.org/x/tools 저장소 또한 export 데이터 reader(go/types 표현 사용)를 위한 공개 API를 제공하며, 이는 항상 컴파일러의 최신 파일 포맷과 소수의 과거 버전을 지원합니다.
(이는 타입 정보는 필요하지만 타입이 주석 처리된 구문은 필요하지 않은 모드에서 x/tools/go/packages에 의해 사용됩니다.)

x/tools 저장소는 이전의 "indexed" 형식을 사용하여 내보낸(exported) 타입 정보(그 외의 정보는 제외)를 읽고 쓰기 위한 공개 API도 제공합니다. (예를 들어, gopls는 타입 정보를 포함한 워크스페이스 정보 데이터베이스를 위해 이 버전을 사용합니다.)

Export data는 보통 "깊은(deep)" 요약을 제공합니다. 따라서 패키지 Q를 컴파일할 때 각 직접 임포트(direct import)에 대한 export data 파일만 읽어도, P의 public API에서 참조되는 타입의 메서드나 struct 필드와 같이 간접 임포트(indirect imports) 내 선언에 관한 모든 필요한 정보가 제공됨을 보장받을 수 있습니다. 깊은 export data는 직접 의존성당 하나의 파일만 필요하므로 빌드 시스템 입장에서 더 단순합니다. 하지만 거대 저장소의 임포트 그래프 상단으로 올라갈수록 데이터가 커지는 경향이 있습니다. 예를 들어, API 규모가 큰 매우 공통적인 타입 세트가 있다면, 거의 모든 패키지의 export data에 해당 복사본이 포함될 것입니다. 이러한 문제가 필요에 따라 부분 로딩이 가능한 "인덱싱된(indexed)" 설계의 동기가 되었습니다.

(gopls는 각 임포트에 대해 컴파일러보다 적은 작업을 수행하므로 export data 오버헤드에 더 민감합니다. 이러한 이유로 gopls는 간접 정보가 전혀 기록되지 않는 "얕은(shallow)" export data를 사용합니다. 이는 모든 의존성의 export data 파일에 대한 랜덤 액세스를 요구하므로, 분산 빌드 시스템에는 적합하지 않습니다.)

### 8. 팁

#### 시작하기

* 컴파일러에 기여한 경험이 없다면, 조사 중인 내용에 대해 초기 통찰을 얻기 위해 로그 문을 추가하거나 `panic("here")`를 삽입하는 것이 시작하는 간단한 방법이 될 수 있습니다.

* 컴파일러 자체에서 다음과 같은 로깅, 디버깅 및 시각화 기능을 제공합니다:
   ```
   $ go build -gcflags=-m=2                   # 인라이닝, 탈출 분석을 포함한 최적화 정보 출력
   $ go build -gcflags=-d=ssa/check_bce/debug # 경계 검사(bounds check) 정보 출력
   $ go build -gcflags=-W                     # 타입 체크 후의 내부 파스 트리 출력
   $ GOSSAFUNC=Foo go build                   # func Foo에 대한 ssa.html 파일 생성
   $ go build -gcflags=-S                     # 어셈블리 출력
   $ go tool compile -bench=out.txt x.go      # 컴파일러 단계별 소요 시간 출력
   ```

일부 플래그는 다음과 같이 컴파일러 동작을 변경합니다:
   ```
   $ go tool compile -h file.go               # 첫 번째 컴파일 오류 발생 시 panic 발생
   $ go build -gcflags=-d=checkptr=2          # 추가적인 unsafe 포인터 검사 활성화
   ```

많은 추가 플래그가 있습니다. 일부 설명은 다음을 통해 확인할 수 있습니다:
   ```
   $ go tool compile -h              # 컴파일러 플래그, 예: go build -gcflags='-m=1 -l'
   $ go tool compile -d help         # 디버그 플래그, 예: go build -gcflags=-d=checkptr=2
   $ go tool compile -d ssa/help     # ssa 플래그, 예: go build -gcflags=-d=ssa/prove/debug=2
   ```

`-gcflags`에 대한 추가 세부 정보와 `go build` 및 `go tool compile`의 차이점은 [아래 섹션](#-gcflags-and-go-build-vs-go-tool-compile)에서 확인하실 수 있습니다.

* 일반적으로 컴파일러의 문제를 조사할 때는 가능한 한 가장 단순한 재현 사례부터 시작하여, 해당 사례에서 정확히 어떤 일이 일어나고 있는지 이해하는 것이 좋습니다.

#### 변경 사항 테스트하기

* Go 기여 가이드의 [Quickly testing your changes](https://go.dev/doc/contribute#quick_test) 섹션을 반드시 읽어보시기 바랍니다.

* 일부 테스트는 `cmd/compile` 패키지 내에 존재하며 `go test ./...` 또는 이와 유사한 명령어로 실행할 수 있지만, 많은 `cmd/compile` 테스트는 최상위 [test](https://github.com/golang/go/tree/master/test) 디렉토리에 있습니다:

```
  $ go test cmd/internal/testdir                           # 'test' 디렉토리의 모든 테스트 실행
  $ go test cmd/internal/testdir -run='Test/escape.*.go'   # 'test' 디렉토리의 특정 파일 테스트 실행
  ```
  자세한 내용은 [testdir README](https://github.com/golang/go/tree/master/test#readme)를 참조하세요.
  [testdir_test.go](https://github.com/golang/go/blob/master/src/cmd/internal/testdir/testdir_test.go)의 `errorCheck` 메서드를 통해 해당 테스트들에서 사용되는 `ERROR` 주석에 대한 설명을 확인할 수 있습니다.

또한, 표준 라이브러리의 `go/types` 패키지와 `cmd/compile/internal/types2`는 `src/internal/types/testdata`에서 테스트를 공유하며, 해당 경로에 변경 사항이 있을 경우 두 타입 체커 모두 확인해야 합니다.

* 새로운 [애플리케이션 기반 커버리지 프로파일링](https://go.dev/testing/coverage/)은 다음과 같이 컴파일러와 함께 사용할 수 있습니다:

```
  $ go install -cover -coverpkg=cmd/compile/... cmd/compile  # 커버리지 계측을 포함하여 컴파일러 빌드
  $ mkdir /tmp/coverdir                                      # 커버리지 데이터 저장 경로 생성
  $ GOCOVERDIR=/tmp/coverdir go test [...]                   # 컴파일러를 사용하고 커버리지 데이터 저장
  $ go tool covdata textfmt -i=/tmp/coverdir -o coverage.out # 전통적인 커버리지 형식으로 변환
  $ go tool cover -html coverage.out                         # 기존 도구를 통해 커버리지 확인
  ```

#### 컴파일러 버전 관리하기

* 많은 컴파일러 테스트는 PATH에서 찾은 `go` 명령어 버전과 그에 해당하는 `compile` 바이너리를 사용합니다.

* 브랜치 내에 있고 PATH에 `<go-repo>/bin`이 포함되어 있다면, `go install cmd/compile`을 실행하여 현재 브랜치의 코드로 컴파일러를 빌드하고 적절한 위치에 설치할 수 있습니다. 이렇게 하면 이후에 실행하는 `go build` 또는 `go test ./...`와 같은 `go` 명령어가 방금 빌드한 컴파일러를 사용하게 됩니다.

* [toolstash](https://pkg.go.dev/golang.org/x/tools/cmd/toolstash)는 Go 툴체인의 검증된 복사본을 저장, 실행 및 복원하는 방법을 제공합니다. 예를 들어, 처음에 브랜치를 빌드하고 해당 툴체인 버전을 저장한 다음, 작업 중인 컴파일러 버전을 컴파일하기 위해 검증된 툴 버전으로 복원하는 것이 좋은 관행이 될 수 있습니다.

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
  [... 'go build', 'go test' 등 수행 ...]           # 새로 빌드된 컴파일러 사용
  ```

* toolstash를 사용하면 설치된 컴파일러와 저장된(stashed) 컴파일러 복사본을 비교할 수 있으며, 이는 리팩토링 후 동작이 동일한지 확인해야 할 때 유용합니다. 예를 들어, 표준 라이브러리를 빌드하는 동안 변경된 컴파일러가 저장된 컴파일러와 동일한 오브젝트 파일을 생성하는지 확인하려면 다음과 같이 실행합니다:
  ```
  $ toolstash restore && go install cmd/compile   # 최신 컴파일러 빌드
  $ go build -toolexec "toolstash -cmp" -a -v std # 최신 컴파일러와 저장된 컴파일러 비교
  ```

* 버전이 서로 일치하지 않는 것으로 보인다면 (예를 들어, `devel go1.21-db3f952b1f`와 같은 버전 문자열과 함께 `linked object header mismatch`와 같은 오류가 발생하는 경우), `toolstash restore && go install cmd/...`를 실행하여 `cmd` 아래의 모든 도구를 업데이트해야 할 수도 있습니다.

#### 추가 유용한 도구들

* [compilebench](https://pkg.go.dev/golang.org/x/tools/cmd/compilebench)는 컴파일러의 속도를 벤치마킹합니다.

* [benchstat](https://pkg.go.dev/golang.org/x/perf/cmd/benchstat)는 컴파일러 수정으로 인한 성능 변화를 보고하기 위한 표준 도구이며, 여기에는 개선 사항이 통계적으로 유의미한지 여부가 포함됩니다:
  ```
  $ go test -bench=SomeBenchmarks -count=20 > new.txt   # 새 컴파일러 사용
  $ toolstash restore                                   # 이전 컴파일러로 복구
  $ go test -bench=SomeBenchmarks -count=20 > old.txt   # 이전 컴파일러 사용
  $ benchstat old.txt new.txt                           # 이전 버전과 새 버전 비교
  ```

* [bent](https://pkg.go.dev/golang.org/x/benchmarks/cmd/bent)는 다양한 커뮤니티 Go 프로젝트의 대규모 벤치마크 세트를 Docker 컨테이너 내부에서 실행하는 것을 용이하게 합니다.

* [perflock](https://github.com/aclements/perflock)는 Linux의 CPU 주파수 스케일링 설정을 조작하는 등의 방법을 통해 더 일관된 벤치마크 결과를 얻을 수 있도록 도와줍니다.

* [view-annotated-file](https://github.com/loov/view-annotated-file) (커뮤니티 제공)
   인라이닝, 경계 검사(bounds check) 및 이스케이프 정보(escape info)를 소스 코드 위에 오버레이로 표시합니다.

* [godbolt.org](https://go.godbolt.org)는 Go 컴파일터를 포함한 많은 컴파일터의 어셈블리 출력을 조사하고 공유하는 데 널리 사용됩니다. 또한 함수 버전 간 또는 Go 컴파일터 버전 간의 어셈블리를 [비교](https://go.godbolt.org/z/5Gs1G4bKG)할 수 있어, 조사 및 버그 보고 시 유용하게 활용될 수 있습니다.

#### -gcflags와 'go build' 및 'go tool compile'의 차이점

* `-gcflags`는 `go` 명령의 [빌드 플래그](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies)입니다.
  `go build -gcflags=<args>`는 `go build` 명령이 평소에 수행하는 모든 작업(예: 빌드 캐시 처리, 모듈 관리 등)을 그대로 수행하면서, 제공된 `<args>`를 내부의 `compile` 호출로 전달합니다. 이와 대조적으로, `go tool compile <args>`는 표준 `go build` 메커니즘을 거치지 않고 `go` 명령이 `compile <args>`를 단 한 번만 호출하도록 요청합니다. 어떤 경우에는 `go build`의 도움 없이도 컴파일할 수 있는 작은 독립 소스 파일이 있는 것처럼, `go tool compile <args>`를 사용하여 작동 단계를 줄이는 것이 도움이 될 수 있습니다. 다른 경우에는 `go build`, `go test` 또는 `go install`과 같은 빌드 명령에 `-gcflags`를 전달하는 것이 더 편리합니다.

* `-gcflags`는 기본적으로 명령줄에 지정된 패키지에 적용되지만, `-gcflags='all=-m=1 -l'`와 같은 패키지 패턴이나 `-gcflags='all=-m=1' -gcflags='fmt=-m=2'`와 같은 여러 개의 패키지 패턴을 사용할 수 있습니다. 자세한 내용은 [cmd/go 문서](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies)를 참조하십시오.

### 추가 읽을거리

SSA 패키지의 패스(pass)와 규칙(rule)을 포함하여 작동 방식에 대해 더 자세히 알아보려면 [cmd/compile/internal/ssa/README.md](internal/ssa/README.md)를 참조하세요.

마지막으로, 이 README나 SSA README에서 불명확한 부분이 있거나 개선 아이디어가 있다면, [issue 30074](https://go.dev/issue/30074)에 자유롭게 의견을 남겨 주세요.
