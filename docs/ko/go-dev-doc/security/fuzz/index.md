Go는 Go 1.18부터 표준 툴체인에서 퍼징(fuzzing)을 지원합니다. 네이티브 Go 퍼즈 테스트는 [OSS-Fuzz에서 지원됩니다](https://google.github.io/oss-fuzz/getting-started/new-project-guide/go-lang/#native-go-fuzzing-support).

**[Go를 이용한 퍼징 튜토리얼](/doc/tutorial/fuzz)을 시도해 보세요.**

## 개요

퍼징(Fuzzing)은 버그를 찾기 위해 프로그램의 입력을 지속적으로 조작하는 자동화된 테스트의 한 종류입니다. Go 퍼징은 커버리지 가이던스(coverage guidance)를 사용하여 퍼징 대상 코드를 지능적으로 탐색하며, 실패 사례를 찾아 사용자에게 보고합니다. 사람이 흔히 놓치는 엣지 케이스(edge cases)에 도달할 수 있기 때문에, 퍼즈 테스트는 특히 보안 익스플로잇과 취약점을 찾는 데 매우 가치 있을 수 있습니다.

다음은 [fuzz test](#glos-fuzz-test)의 예시이며, 주요 구성 요소들을 강조하여 보여줍니다.

<img class="DarkMode-img" alt="전체 퍼즈 테스트와 그 내부의 퍼즈 타겟을 보여주는 예제 코드입니다. 퍼즈 타겟 앞에는 f.Add를 통한 코퍼스 추가가 있으며, 퍼즈 타겟의 매개변수는 퍼징 인자로 강조 표시되어 있습니다."
src="/security/fuzz/example-dark.png" style="width: 600px; height:
auto;"/>
<img alt="전체 퍼즈 테스트와 그 내부의 퍼즈 타겟을 보여주는 예제 코드입니다. 퍼즈 타겟 앞에는 f.Add를 통한 코퍼스 추가가 있으며, 퍼즈 타겟의 매개변수는 퍼징 인자로 강조 표시되어 있습니다."
src="/security/fuzz/example.png" style="width: 600px; height:
auto;" class="LightMode-img"/>

## 퍼즈 테스트 작성하기

### 요구사항

다음은 퍼즈 테스트(fuzz tests)가 준수해야 하는 규칙입니다.

- 퍼즈 테스트(fuzz test)는 `FuzzXxx`와 같은 이름의 함수여야 하며, `*testing.F`만을 인자로 받고 반환 값은 없어야 합니다.
- 퍼즈 테스트가 실행되려면 `*_test.go` 파일에 있어야 합니다.
- [퍼즈 타겟(fuzz target)](#glos-fuzz-target)은 <code>[(\*testing.F).Fuzz](https://pkg.go.dev/testing#F.Fuzz)</code>에 대한 메서드 호출이어야 하며, 첫 번째 파라미터로 `*testing.T`를 받고 그 뒤에 퍼징 인자(fuzzing arguments)들이 와야 합니다. 반환 값은 없습니다.
- 퍼즈 테스트당 정확히 하나의 퍼즈 타겟이 있어야 합니다.
- 모든 [시드 코퍼스(seed corpus)](#glos-seed-corpus) 항목은 [퍼징 인자](#glos-fuzzing-arguments)와 동일한 순서 및 동일한 타입을 가져야 합니다. 이는 <code>[(\*testing.F).Add](https://pkg.go.dev/testing#F.Add)</code> 호출 및 퍼즈 테스트의 `testdata/fuzz` 디렉토리에 있는 모든 코퍼스 파일에 적용됩니다.
- 퍼징 인자는 다음 타입들만 가능합니다:
  - `string`, `[]byte`
  - `int`, `int8`, `int16`, `int32`/`rune`, `int64`
  - `uint`, `uint8`/`byte`, `uint16`, `uint32`, `uint64`
  - `float32`, `float64`
  - `bool`

### 제안 사항 {#suggestions}

다음은 퍼징(fuzzing)을 최대한 활용하는 데 도움이 되는 제안 사항들입니다.

- 퍼즈 타겟(Fuzz targets)은 퍼징 엔진이 효율적으로 작동하고, 새로운 실패 사례와 코드 커버리지를 쉽게 재현할 수 있도록 빠르고 결정적(deterministic)이어야 합니다.
- 퍼즈 타겟은 여러 워커(worker)에서 병렬로, 그리고 비결정적인 순서로 호출되므로, 퍼즈 타겟의 상태는 각 호출이 끝난 후에도 유지되어서는 안 되며, 퍼즈 타겟의 동작이 전역 상태(global state)에 의존해서는 안 됩니다.

## 퍼즈 테스트 실행하기

퍼즈 테스트를 실행하는 방법에는 두 가지 모드가 있습니다: 유닛 테스트로 실행(기본값 `go test`), 또는 퍼징으로 실행(`go test -fuzz=FuzzTestName`).

퍼즈 테스트는 기본적으로 단위 테스트와 매우 유사하게 실행됩니다. 각 [시드 코퍼스 항목](#glos-seed-corpus)은 퍼즈 타겟을 대상으로 테스트되며, 종료 전 모든 실패 사례를 보고합니다.

퍼징(fuzzing)을 활성화하려면 단일 퍼즈 테스트와 일치하는 정규 표현식을 제공하여 `-fuzz` 플래그와 함께 `go test`를 실행하십시오. 기본적으로 해당 패키지의 다른 모든 테스트가 퍼징 시작 전에 실행됩니다. 이는 기존 테스트에서 이미 발견되었을 문제를 퍼징이 보고하지 않도록 하기 위함입니다.

퍼징(fuzzing)을 얼마나 오래 실행할지는 사용자가 결정해야 한다는 점에 유의하십시오. 오류를 찾지 못할 경우 퍼징 실행이 무기한으로 계속될 가능성이 매우 높습니다. 향후 OSS-Fuzz와 같은 도구를 사용하여 이러한 퍼즈 테스트를 지속적으로 실행할 수 있는 지원이 제공될 예정입니다. [Issue #50192](/issue/50192)를 참조하십시오.

**참고:** 퍼징(Fuzzing)은 커버리지 도구화(coverage instrumentation)를 지원하는 플랫폼(현재 AMD64 및 ARM64)에서 실행해야 합니다. 그래야 실행 중에 코퍼스(corpus)가 의미 있게 성장하고, 퍼징 과정에서 더 많은 코드를 커버할 수 있습니다.

### 커맨드 라인 출력

퍼징이 진행되는 동안, [fuzzing engine](#glos-fuzzing-engine)은 새로운 입력을 생성하고 이를 제공된 fuzz target에 대해 실행합니다. 기본적으로, [failing input](#glos-failing-input)이 발견되거나 사용자가 프로세스를 취소(예: Ctrl^C)할 때까지 계속 실행됩니다.

출력 결과는 다음과 같은 형태가 됩니다:

```
~ go test -fuzz FuzzFoo
fuzz: elapsed: 0s, gathering baseline coverage: 0/192 completed
fuzz: elapsed: 0s, gathering baseline coverage: 192/192 completed, now fuzzing with 8 workers
fuzz: elapsed: 3s, execs: 325017 (108336/sec), new interesting: 11 (total: 202)
fuzz: elapsed: 6s, execs: 680218 (118402/sec), new interesting: 12 (total: 203)
fuzz: elapsed: 9s, execs: 1039901 (119895/sec), new interesting: 19 (total: 210)
fuzz: elapsed: 12s, execs: 1386684 (115594/sec), new interesting: 21 (total: 212)
PASS
ok      foo 12.692s
```

첫 몇 줄은 퍼징이 시작되기 전에 "기준 커버리지(baseline coverage)"가 수집됨을 나타냅니다.

베이스라인 커버리지를 수집하기 위해, 퍼징 엔진은 [seed corpus](#glos-seed-corpus)와 [generated corpus](#glos-generated-corpus)를 모두 실행하여 오류가 발생하지 않았는지 확인하고, 기존 코퍼스가 이미 제공하는 코드 커버리지를 파악합니다.

다음 라인들은 활성 퍼징 실행에 대한 통찰을 제공합니다:

- elapsed: 프로세스가 시작된 이후 경과된 시간
  - execs: 퍼즈 타겟(fuzz target)에 대해 실행된 총 입력 횟수
    (마지막 로그 라인 이후의 초당 평균 실행 횟수 포함)
  - new interesting: 이번 퍼징 실행 동안 생성된 코퍼스(corpus)에 추가된 "흥미로운" 입력의 총 횟수 (전체 코퍼스의 총 크기 포함)

입력이 "흥미롭기(interesting)" 위해서는, 기존에 생성된 코퍼스가 도달할 수 있는 범위를 넘어 코드 커버리지를 확장해야 합니다. 일반적으로 새로운 흥미로운 입력의 수는 초기에 빠르게 증가하다가 점차 둔화되며, 새로운 분기(branch)가 발견될 때마다 간헐적으로 급증하는 경향을 보입니다.

코퍼스의 입력값이 코드의 더 많은 라인을 커버하기 시작함에 따라 "new interesting" 수치는 시간이 지남에 따라 점차 감소할 것으로 예상되나, 퍼징 엔진이 새로운 코드 경로를 찾을 경우 간헐적으로 급증할 수 있습니다.

### 실패하는 입력

퍼징(fuzzing) 중에 다음과 같은 여러 가지 이유로 실패가 발생할 수 있습니다:

- 코드 또는 테스트에서 패닉(panic)이 발생했습니다.
  - 퍼즈 타겟(fuzz target)이 `t.Fail`을 직접 호출했거나, `t.Error` 또는 `t.Fatal`과 같은 메서드를 통해 호출했습니다.
  - `os.Exit` 또는 스택 오버플로(stack overflow)와 같이 복구 불가능한 오류가 발생했습니다.
  - 퍼즈 타겟의 완료 시간이 너무 오래 걸렸습니다. 현재 퍼즈 타겟의 실행 제한 시간은 1초입니다. 이는 데드락(deadlock)이나 무한 루프로 인해 발생할 수 있으며, 코드의 의도된 동작으로 인해 발생할 수도 있습니다. 이것이 [퍼즈 타겟을 빠르게 작성하도록 권장하는](#suggestions) 이유 중 하나입니다.

에러가 발생하면, 퍼징 엔진은 여전히 에러를 발생시키면서도 가능한 가장 작고 사람이 읽기 쉬운 값으로 입력을 최소화하려고 시도합니다. 이를 설정하려면 [custom settings](#custom-settings) 섹션을 참조하십시오.

최소화 작업이 완료되면 에러 메시지가 기록되며, 출력 결과는 다음과 같이 끝납니다:

```
    실패한 입력값이 testdata/fuzz/FuzzFoo/a878c3134fe0404d44eb1e662e5d8d4a24beb05c3d68354903670ff65513ff49 에 기록되었습니다.
    재실행 방법:
    go test -run=FuzzFoo/a878c3134fe0404d44eb1e662e5d8d4a24beb05c3d68354903670ff65513ff49
FAIL
exit status 1
FAIL    foo 0.839s
```

퍼징 엔진이 해당 퍼즈 테스트의 시드 코퍼스(seed corpus)에 이 [실패 입력](#glos-failing-input)을 기록했으며, 이제 `go test` 실행 시 기본적으로 실행되어 버그가 수정된 후 회귀 테스트(regression test) 역할을 하게 됩니다.

다음 단계는 문제를 진단하고, 버그를 수정하며, `go test`를 다시 실행하여 수정 사항을 검증한 뒤, 새로운 testdata 파일을 회귀 테스트(regression test)로 사용하여 패치를 제출하는 것입니다.

### 사용자 정의 설정 {#custom-settings}

기본 `go` 명령 설정은 대부분의 퍼징(fuzzing) 유스케이스에서 문제없이 작동합니다. 따라서 일반적으로 커맨드 라인에서의 퍼징 실행은 다음과 같은 형태가 됩니다:

```
$ go test -fuzz={FuzzTestName}
```

하지만 `go` 명령어는 퍼징(fuzzing)을 실행할 때 몇 가지 설정을 제공합니다.
이에 대한 내용은 [`cmd/go` 패키지 문서](https://pkg.go.dev/cmd/go)에 설명되어 있습니다.

몇 가지 주요 사항을 강조하자면 다음과 같습니다:

- `-fuzztime`: 퍼즈 타겟이 종료되기 전까지 실행될 총 시간 또는 반복 횟수이며, 기본값은 무제한입니다.
- `-fuzzminimizetime`: 각 최소화(minimization) 시도 중에 퍼즈 타겟이 실행될 시간 또는 반복 횟수이며, 기본값은 60초입니다. 퍼징 시 `-fuzzminimizetime 0`으로 설정하여 최소화 기능을 완전히 비활성화할 수 있습니다.
- `-parallel`: 동시에 실행될 퍼징 프로세스의 수이며, 기본값은 `$GOMAXPROCS`입니다. 현재 퍼징 중에 `-cpu`를 설정하는 것은 아무런 영향을 주지 않습니다.

## 코퍼스 파일 형식

코퍼스 파일은 특수한 형식으로 인코딩되어 있습니다. 이 형식은 [시드 코퍼스](#glos-seed-corpus)와 [생성된 코퍼스](#glos-generated-corpus) 모두에 동일하게 적용됩니다.

다음은 코퍼스(corpus) 파일의 예시입니다:

```
go test fuzz v1
[]byte("hello\\xbd\\xb2=\\xbc ⌘")
int64(572293)
```

첫 번째 줄은 퍼징 엔진에 파일의 인코딩 버전을 알리는 데 사용됩니다. 현재로서는 인코딩 형식의 향후 버전 계획이 없지만, 설계상 이러한 가능성을 지원해야 합니다.

다음의 각 줄은 코퍼스(corpus) 항목을 구성하는 값들이며, 필요한 경우 Go 코드에 직접 복사하여 사용할 수 있습니다.

위의 예시에서, 우리는 `[]byte` 뒤에 `int64`가 오는 구조를 가지고 있습니다. 이러한 타입들은 퍼징(fuzzing) 인자와 정확히 일치해야 하며, 순서 또한 동일해야 합니다. 이러한 타입들을 위한 퍼지 타겟(fuzz target)은 다음과 같습니다.

```
f.Fuzz(func(*testing.T, []byte, int64) {})
```

자체 시드 코퍼스(seed corpus) 값을 지정하는 가장 쉬운 방법은 `(*testing.F).Add` 메서드를 사용하는 것입니다. 위의 예제에서 적용하면 다음과 같습니다.

```
f.Add([]byte("hello\\xbd\\xb2=\\xbc ⌘"), int64(572293))
```

하지만 테스트 코드 내에 직접 복사하고 싶지 않은 커다란 바이너리 파일이 있을 수 있으며, 이 경우에는 대신 `testdata/fuzz/{FuzzTestName}` 디렉토리에 개별 시드 코퍼스(seed corpus) 항목으로 유지하는 것이 좋습니다. golang.org/x/tools/cmd/file2fuzz에 있는 [`file2fuzz`](https://pkg.go.dev/golang.org/x/tools/cmd/file2fuzz) 도구를 사용하여 이러한 바이너리 파일을 `[]byte`로 인코딩된 코퍼스 파일로 변환할 수 있습니다.

이 도구를 사용하려면:

```
$ go install golang.org/x/tools/cmd/file2fuzz@latest
$ file2fuzz -h
```

## 리소스

- **튜토리얼**:
  - 새로운 개념들을 깊이 있게 살펴보려면 [Go를 이용한 퍼징 튜토리얼](/doc/tutorial/fuzz)을 시도해 보세요.
  - Go 퍼징에 대한 짧은 입문용 튜토리얼은 [블로그 포스트](/blog/fuzz-beta)를 참조하시기 바랍니다.
- **문서**:
  - [`testing`](https://pkg.go.dev//testing#hdr-Fuzzing) 패키지 문서는 퍼즈 테스트를 작성할 때 사용되는 `testing.F` 타입에 대해 설명합니다.
  - [`cmd/go`](https://pkg.go.dev/cmd/go) 패키지 문서는 퍼징과 관련된 플래그들에 대해 설명합니다.
- **기술 세부 사항**:
  - [설계 초안](/s/draft-fuzzing-design)
  - [제안서](/issue/44551)

## 용어 사전 {#glossary}

<a id="glos-corpus-entry"></a>
**corpus entry (코퍼스 엔트리):** 퍼징(fuzzing) 중에 사용할 수 있는 코퍼스의 입력값입니다. 이는 특별한 형식의 파일이거나 <code>[(\*testing.F).Add](https://pkg.go.dev/testing#F.Add)</code> 호출일 수 있습니다.

<a id="glos-coverage-guidance"></a>
**coverage guidance:** 코드 커버리지의 확장을 사용하여 향후 사용을 위해 어떤 코퍼스 항목을 유지할 가치가 있는지 결정하는 퍼징 방법.

<a id="glos-failing-input"></a>
**failing input:** failing input이란 [fuzz target](#glos-fuzz-target)에 대해 실행했을 때 에러 또는 패닉(panic)을 유발하는 코퍼스(corpus) 항목을 의미합니다.

<a id="glos-fuzz-target"></a>
**fuzz target:** 퍼징 중에 코퍼스(corpus) 항목 및 생성된 값들에 대해 실행되는 퍼즈 테스트의 함수입니다. 이 함수는 <code>[(\*testing.F).Fuzz](https://pkg.go.dev/testing#F.Fuzz)</code>에 함수를 전달함으로써 퍼즈 테스트에 제공됩니다.

<a id="glos-fuzz-test"></a>
**fuzz test:** 퍼징(fuzzing)에 사용할 수 있는 `func FuzzXxx(*testing.F)` 형태의 테스트 파일 내 함수입니다.

<a id="glos-fuzzing"></a>
**fuzzing:** 프로그램의 입력값을 지속적으로 조작하여 버그나 코드가 취약할 수 있는 [vulnerabilities](#glos-vulnerability)와 같은 문제를 찾아내는 자동화된 테스트의 한 유형입니다.

<a id="glos-fuzzing-arguments"></a>
**fuzzing arguments:** 퍼즈 타겟(fuzz target)에 전달되며, [mutator](#glos-mutator)에 의해 변이(mutate)되는 타입들입니다.

<a id="glos-fuzzing-engine"></a>
**fuzzing engine:** 코퍼스(corpus) 유지, 뮤테이터(mutator) 호출, 새로운 커버리지 식별 및 실패 보고를 포함하여 퍼징을 관리하는 도구입니다.

<a id="glos-generated-corpus"></a>
**generated corpus (생성된 코퍼스):** 퍼징 엔진이 퍼징을 진행하는 동안 진행 상황을 추적하기 위해 지속적으로 유지 관리하는 코퍼스입니다. 이는 `$GOCACHE`/fuzz에 저장됩니다. 이 항목들은 퍼징 중에만 사용됩니다.

<a id="glos-mutator"></a>
**mutator:** 퍼징 중에 사용되는 도구로, 코퍼스 항목을 퍼즈 타겟(fuzz target)에 전달하기 전에 무작위로 조작합니다.

<a id="glos-package"></a>
**package:** 동일한 디렉터리에 있으며 함께 컴파일되는 소스 파일들의 집합입니다. Go 언어 사양의 [Packages 섹션](/ref/spec#Packages)을 참조하십시오.

<a id="glos-seed-corpus"></a>
**seed corpus (시드 코퍼스):** 퍼즈 엔진을 안내하는 데 사용할 수 있도록 사용자가 제공한 퍼즈 테스트용 코퍼스입니다. 이는 퍼즈 테스트 내의 `f.Add` 호출을 통해 제공된 코퍼스 항목과 패키지 내 `testdata/fuzz/{FuzzTestName}` 디렉토리에 있는 파일들로 구성됩니다. 퍼징 여부와 관계없이, 이러한 항목들은 `go test` 실행 시 기본적으로 실행됩니다.

<a id="glos-test-file"></a>
**test file:** 테스트, 벤치마크, 예제 및 퍼즈 테스트(fuzz tests)가 포함될 수 있는 `xxx_test.go` 형식의 파일입니다.

<a id="glos-vulnerability"></a>
**vulnerability (취약점):** 공격자에 의해 악용될 수 있는 코드 내의 보안 민감한 약점.

## 피드백

문제가 발생하거나 기능 제안 아이디어가 있다면, [이슈를 등록해](/issue/new?&labels=fuzz) 주세요.

이 기능에 대한 논의 및 일반적인 피드백은 Gophers Slack의 [#fuzzing 채널](https://gophers.slack.com/archives/CH5KV1AKE)에서도 참여하실 수 있습니다.
