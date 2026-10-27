# Go SIMD 제너레이터를 `internal/spec`으로 전환하기

이 계획은 SIMD API의 수많은 제너레이터와 수동으로 작성된 소스들을, 개별적으로 수동으로 일관성을 유지하던 방식에서 모든 메서드 시그니처, 문서 및 검증 가능한 시맨틱을 제공하는 단일 기저 실행 가능 API 사양으로 전환하는 방법을 설명합니다.

SIMD 패키지에 대한 배경 지식, "하나의 이름, 하나의 의미(one name, one meaning)" 규칙, 제너레이터, simdgen의 작동 방식, spec 및 specgen이 무엇인지, 그리고 실행 방법은 [README.md](README.md)를 참조하십시오.

## 목차

- 파트 1: 결정 사항 및 근거
- 파트 2: 태스크 그래프
- 파트 3: 태스크 상세 내용
- 파트 4: 리스크 및 미지수
- 부록 A: 생성된 두 파일 재생성하기

## 계획 요약

`internal/spec` — 각 연산을 설명하는 제네릭 Go 함수들 — 이 SIMD API의 단일한 수동 작성 설명서가 됩니다. 현재는 동일한 연산이 여섯 군데에서 설명되고 있으며, 이들은 이미 서로 일치하지 않는 상태입니다 (§1.5).

세 가지 일이 일어나야 하며, 이들은 대체로 독립적입니다:

1. **`specfill` 체커를 구축합니다.** 생성된 소스 및 수동으로 작성된 소스에 spec의 문서를 주입하고, spec에 대해 시그니처를 검증하는 하나의 AST 패스입니다. 타입은 거의 즉시 강제될 수 있습니다 — SPEC-STATS.txt §2는 spec과 출시된 API 사이에 타입 수준의 불일치가 전혀 없음을 보여줍니다.
2. **spec 함수(`spec-common` 및 `spec-all`)를 작성합니다.** 커버리지는 SPEC-STATS.txt §1에 나와 있습니다. 이는 다른 트랙들이 의존하는 병목 지점입니다.
3. **기존 입력을 폐기합니다**: 다른 문서 소스들을 먼저 제거한 다음 `categories.yaml`을 제거합니다. 이 시점이 되면 unifier는 더 이상 API를 정의하지 않으며, 단지 하나의 arch 항목을 그에 맞는 머신 명령어로 확장하는 역할만 수행하게 됩니다.

`internal/simdref` (트랙 C)에 대한 동작 일치성(Behavioral conformance) 검사는 병렬로 실행됩니다.
자체 `ci-audit` 외에도, 이는 스펙 커버리지와 `width` 및 `impl-defined` 결정 사항에만 의존합니다.

## 플랜 진행 상황 모니터링

이 전환의 진행 상황은 두 가지 방식으로 추적됩니다:

**작업 완료** 여부는 각 작업 및 리스크에 있는 `[ ]` 체크박스를 통해 이 문서에서 직접 추적됩니다. 파트 2의 작업 테이블은 모든 작업 완료 상태를 한곳에 요약하여 보여줍니다.

[SPEC-TASKS.dot](SPEC-TASKS.dot)는 태스크 그래프와 완료된 태스크의 시각적 표현을 보여줍니다. 이는 `_gen`에서 `go run ./cmd/spectasks -w`를 실행하여 이 문서로부터 직접 생성됩니다. 이 생성기는 또한 이 문서의 일관성을 검사하며, `./cmd/spectasks`의 테스트가 CI에서 문서 일관성을 강제합니다. 태스크 메타데이터를 수정 후에는 생성기를 다시 실행하십시오.

**측정값**은 [SPEC-STATS.txt](SPEC-STATS.txt)에 기록되며, 여기에는 API의 스펙 커버리지, 시그니처 및 이름 일치 여부, 문서 소스, 그리고 이전 입력값의 폐기 상태가 추적됩니다. 이 파일은 `_gen` 디렉토리에서 `go run ./cmd/specstats -w`를 실행하여 생성됩니다. 해당 파일의 모든 수치는 100%를 향한 분수 형태의 헤더이거나 0을 향한 카운트 형태의 헤더이며, 이를 변화시키는 작업(task)이 태그로 지정되어 있습니다. 들여쓰기가 되어 있고 태그가 없는 숫자는 바로 위의 수치를 세분화하여 설명하는 컨텍스트입니다. 이 문서의 파트 1에서는 특정 결정의 근거가 된 측정값들을 인용하며, 측정이 수행된 시점의 CL이 함께 기록되어 있습니다. 이 값들은 고정된 것이므로 갱신할 필요가 없습니다.

## 태스크 구현 방법

파트 2에서는 어떤 작업을 선택해야 하는지 알려줍니다. 모든 선행 작업이 완료된 다음 작업을 선택하십시오. 그림이 도움이 된다면 [SPEC-TASKS.dot](SPEC-TASKS.dot)에서 동일한 내용을 확인할 수 있습니다. 파트 3의 커밋 시퀀스는 작업 시작 전의 예상치입니다. 코드를 통해 수정이 필요하다고 판단되면 변경하되, 해당 내용을 CL 설명에 명시하십시오.

작업(Tasks)과 리스크(risks)에는 `[ ]` 체크박스가 표시되어 있습니다. 항목을 해결하면 체크박스에 체크하고, 구현된 실제 상황을 반영하여 작업 텍스트를 업데이트하십시오. 이는 후속 작업을 수행할 때 참고 자료로서 유용하게 유지하기 위함입니다(정확한 커밋 시퀀스는 삭제하거나 요약해도 됩니다). 그 후 [SPEC-TASKS.dot](SPEC-TASKS.dot) 파일을 다시 생성하십시오.

이 변경 사항은 작업을 구현한 CL들의 상단에 별도의 CL로 커밋하고, 작업 텍스트를 변경한 경우 커밋 메시지에 그 정당성과 근거를 포함하십시오.

## 핵심 개념 및 용어

**`specfill`**은 이 계획에서 가장 먼저 구축하고 이후에 활용하는 도구입니다. 이는 Go 소스 코드에 대해 한 번의 AST 패스를 수행하여 스펙(spec)에서 파생된 문서 주석(doc comments)과 파라미터 및 결과 이름을 주입하고, 스펙에 따라 시그니처를 검증합니다. 이 도구는 제너레이터에 통합할 수 있는 패키지 형태와 독립 실행형 도구 형태로 모두 제공됩니다.

- **`specdoc.Fill`**은 라이브러리 진입점으로, Go 소스를 입력받아 Go 소스를 출력합니다:
  `func Fill(src []byte, idx *specgen.Index, opts Options) ([]byte, error)`.
  검증 체크에 실패하면 에러로 `*Report`를 반환합니다. Generator들은 쓰기 작업 전에 `gentools` 버퍼에 대해 이 함수를 호출합니다.
- **`cmd/specfill`**은 이를 래핑한 `gentools` 기반 명령어로, 수동으로 작성된 파일들에 대해 실행하는 용도입니다. 이 문서에서 `specfill -w`라고 적힌 것은 해당 명령어를 의미하며, `specfill`이라고 적힌 것은 라이브러리 함수를 의미합니다. CI 강제 적용은 이 패키지의 `go test`를 통해 이루어집니다.

이 패키지와 명령 이름들은 제안 사항이며, 라이브러리와 명령의 구분은 확정된 사항입니다.

**Target**은 amd64, arm64 (NEON), arm64 SVE 또는 wasm 중 하나를 의미합니다. README.md를 참조하십시오.

**Spec operation**이란 `spec` 패키지에 있는 하나의 함수를 의미합니다. 각 operation은 요소 타입(element types), 너비(widths), 템플릿 이름(templated names)에 따라 많은 API 이름과 많은 `(receiver, name)` 쌍으로 확장됩니다. 따라서 이는 spec이 *작성되는* 단위이며, "어디에도 구현되지 않음(implemented nowhere)"이라는 말이 의미를 갖는 유일한 단위입니다 (SPEC-STATS.txt §5).

**Operation** (한정되지 않은 상태)은 이름이 나타내는 API 수준의 작업을 의미하며, 이는 사양(spec), `categories.yaml` 또는 생성된 소스 중 어디에서 설명하든 상관없습니다. `categories.yaml` 항목은 *entry*라고 하며, 하나의 작업 이름은 여러 개의 entry를 가질 수 있습니다.

**세분성(Granularity).** 스펙 커버리지는 세 가지 세분성 수준에서 측정됩니다:
`(target, receiver, name)` — 모든 내보내기(exported) 선언으로, 빌드 구성당 한 번씩 계산됩니다; `(receiver, name)` — 타겟 간에 통합된 형태로, 스펙이 연산을 한 번만 설명하므로 기본 분모로 사용됩니다; 그리고 `name` — 리시버까지 통합된 형태로, 더 거칠며 스펙과 API의 서로 다른 리시버 세트에 동일한 이름이 존재할 때 오해의 소지가 있습니다 (SPEC-STATS.txt §5). SPEC-STATS.txt §1은 이 세 가지를 모두 보고합니다. `String`과 `Len`은 전반적으로 제외됩니다 (§1.7).

제공해주신 원문 내용이 없습니다. 번역할 Markdown 내용을 입력해 주시면, 요청하신 지침(Markdown 구조 유지, Go 패키지 및 식별자/코드 미번역 등)에 따라 정확하게 한국어로 번역해 드리겠습니다.

# 파트 1 — 결정 및 근거

이것들은 하중 지지 결정 사항들입니다. 각 사항은 설계 과정에서 논의가 있었습니다. 새로운 근거가 나타날 경우 결정을 다시 검토하기 쉽게 함과 동시에, 동일한 논쟁이 반복되지 않도록 그 근거를 기록해 두었습니다.

별도의 언급이 없는 한, 이 섹션의 측정값은 CL 831485에서 측정되었습니다.
결정을 재검토해야 하는 경우가 아니면 업데이트해서는 안 됩니다.

## 1.1 우리는 simdgen을 다시 작성하지 않습니다

유혹은 강렬합니다. `simdgen`에는 피연산자 개수, 피연산자 순열 및 즉시값(immediate) 배치를 *이름*으로 인코딩한 28개의 스텁 템플릿(`op3_231Type1`, `op4_31`, `op2Imm8_II`)이 있고, `RawOperation`(23개)과 `Operand`(19개)에 걸쳐 42개의 필드가 있으며, "simdgen only supports" 또는 "simdgen does not"로 시작하는 메시지를 가진 27개의 베일아웃(bail-out)이 존재합니다. 하지만 계층 분석 결과, 이 혼란은 규모가 작고 그 가치는 큽니다 (CL 831485 기준; Go 카운트에는 `_test.go`가 포함되며, "signature derivation + emission"은 `simdgen/gen_*.go`, `godefs.go`, `arch.go`, `types/operation.go`입니다):

| 레이어 | 라인 수 | "unification이 잘못되었는가?"의 영향을 받는가? |
|---|---|---|
| Platform loaders | 5,100 | 아니요 — 대체 불가능함 |
| Unifier engine | 3,169 | 부분적으로 |
| Signature derivation + emission | 4,715 | 가장 지저분한 약 500 라인은 그렇습니다 |
| `categories.yaml` | 1,284 | 어차피 이 계획에 의해 삭제됨 |
| `go_GOARCH.yaml` | 4,475 | 아니요 |

통합(unification)이 잘못된 결정이었을 경우 버려지게 될 부분은 시그니처 유도(signature derivation)와 관련된 가장 지저분한 약 500줄의 코드이며, 이는 그보다 몇 배는 더 크고 대체 불가능한 플랫폼 로더(platform loaders)들에 비하면 적은 수준입니다.

수천 줄의 수작업 YAML이 4개의 타겟에 걸쳐 수만 줄의 생성된 API 및 컴파일러 백엔드를 구동합니다. 이 비율은 훌륭합니다. 하지만 **API 정의자**로서의 unification의 역할, 즉 `categories.yaml` ↔ `go_GOARCH.yaml` 조인(join)은 그 가치를 다하지 못하고 있으며, 이번 전환은 구조적으로 해당 역할을 제거합니다. ISA 데이터베이스를 대상으로 하나의 아키텍처 항목을 일치하는 모든 구체적인 명령어 변형으로 확장하는 unifier의 남은 작업은 효율적으로 수행되고 있습니다.

## 1.2 Spec은 unifier 입력값이 아닙니다.

`DefBuilder`를 통해 unification으로 spec을 전달하는 것은 쉽지만 잘못된 방법입니다. spec의 구조는 경계를 넘는 순간 구조화되지 않은 value language로 평탄화(flattened)되어, 우리가 피하고자 하는 정확히 동일한 실패 모드를 재현하게 됩니다. 대신, simdgen은 `[]*specgen.Func`를 타입이 지정된 Go 테이블로 소비합니다.

또한, `spec`은 본질적으로 Go SIMD API의 구조만 알고 있지만, unifier로 들어오는 입력값들은 플랫폼 용어로 되어 있습니다. unifier 출력의 상당 부분은 플랫폼 구조를 Go SIMD API로 매핑하는 방법에 대한 정보이므로, 해당 매핑 처리가 완료된 *이후*에야 `spec`을 도입할 수 있습니다.

## 1.3 spec에 포함되어야 할 내용

테스트 항목은 다음과 같습니다: **이것이 명세(spec) 자체의 시맨틱(semantics)에 대해 검증 가능한 주장인가?**

- `commutative` — 예. `Add(x,y) == Add(y,x)`는 실행 가능한 본문(executable body)에 대해 테스트 가능하며, 스펙(spec)은 이를 확인할 수 있는 유일한 곳입니다.
- `noGenericOps`, `noTypes` — 아니요. 제너레이터 출력에 관한 주장입니다.
- `constImm` — 아니요. x86 인코딩에 관한 주장입니다.
- `regexpTag`, `signed` — 아니요. 유니파이어(unifier)에 관한 주장입니다.

이 테스트는 자체적으로 규제됩니다. 테스트를 통과하는 모든 항목은 어차피 우리가 원하는 적합성 테스트 범위에서 벗어나게 됩니다. 이 테스트가 *컴파일러*가 사용하는 사실들을 허용한다는 점에 유의하십시오. 잘못된 구분선은 "API 대 컴파일러"이며, 올바른 구분선은 "작업에 내재적인 것 대 메커니즘 또는 플랫폼에 부수적인 것"입니다.

`commutative`의 경우, 현재 `categories.yaml` 내의 어떤 이름도 플랫폼별 교환법칙을 필요로 하지 않으므로, 현재로서는 spec의 함수 수준 지시어(directive)만으로도 충분합니다. 하지만 우리가 아직 발견하지 못한 예외 사례가 있을 수 있습니다. 특히, float 타입의 `Min`/`Max`가 모든 플랫폼에서 교환법칙이 성립하지 않을 수 있다는 증거가 있습니다. 이러한 연산들을 단순히 교환 가능(commutative)으로 표시하지 않고, 놀라운 이유로 인해 연산의 교환법칙이 성립하지 않는 경우를 문서화하는 것만으로도 충분할 수 있습니다.

`categories.yaml`의 필드에 테스트를 적용한 결과 (CL 831485 기준; 217개 항목, 195개의 고유한 operation 이름, 163개 export됨):

| 필드 | 개수 | 전환 계획 |
|---|---|---|
| `go` | 217 | → spec 함수 이름 |
| `commutative` | 217 | → `//specgen:commutative` 지시어; `categories.yaml` 복사본은 `sig-from-spec`에 의해 제거됨 |
| `documentation` | 211 | → spec 문서 주석; `template-docs`에 의해 제거됨 |
| `regexpTag` | 25 | unification 조인 키; 역할 미확인 (`risk-cat-unknowns` 참조) |
| `constImm` | 22 | → `go_amd64.yaml`로 측면 이동 (x86 인코딩) |
| `out` | 14 | 문서 변체 선택에만 사용되는 조인 키; → 하나의 `//specgen:name`을 공유하는 여러 spec 함수 |
| `elemBits` | 14 | 동일 |
| `bits` | 4 | 동일 |
| `signed` | 12 | 동일 |
| `noGenericOps` 13 / `noTypes` 6 | 13개 항목 | **미결 질문** — 컴파일러 전용 연산 |

`cat-rehome` 태스크는 "transition plan" 컬럼의 대부분을 처리합니다.
`compiler-ops-impl`은 `noGenericOps` / `noTypes` 항목을 처리합니다.

## 1.4 `specfill`는 파싱을 수행하며, 타입 체크를 하지 않습니다.

`ops_amd64.go`와 `types_amd64.go`는 임포트가 최소한으로 구성되어 있으며, 두 패키지의 어떤 내보내기(exported) 시그니처도 한정 타입(qualified type)을 사용하지 않습니다. 따라서 `go/parser`만으로도 충분하며, `go/types`, `packages.Load`, GOEXPERIMENT 조정, 또는 GOROOT 표준 패키지의 교차 모듈 로딩이 필요하지 않습니다.

이는 임시방편보다 더 나은 방법입니다. 타입 체크(Type-checking)는 한 번에 하나의 빌드 구성만 확인하므로, 교차 아키텍처 비교를 더 *어렵게* 만들 것입니다. 빌드 태그와 관계없이 모든 파일을 파싱하면 단 한 번의 패스로 `ops_amd64.go`, `ops_arm64.go`, `ops_wasm.go`에서 `(Int32x4) Add`를 찾아낼 수 있으며, 이것이 바로 우리가 원하는 비교 방식입니다. `apisum`이 이미 이 방식을 사용하고 있으므로, 이 API에서 검증된 방법입니다.

`cmd/specstats` (부록 A)는 동일한 목적을 위해 다른 경로를 취합니다. 이는 타겟별 수치를 보고하기 때문에, 빌드 구성당 한 번씩 `go/packages`를 통해 구문을 로드합니다. 여전히 타입 체크는 수행하지 않으며, `specfill`은 구성별 로딩이 필요하지 않습니다.

## 1.5 2단계 문서 주입(Two-pass doc injection)과 "단점"이 핵심인 이유

동기는 문서의 불일치(doc divergence)입니다. CL 831485 시점에는 `categories.yaml`, wasmgen 인라인 문자열, tmplgen 인라인 문자열, `midway/comments.yaml`, 수작업으로 작성된 `simd_emulated.go`, 그리고 수작업으로 작성된 `archsimd` 파일까지 총 **6개의 독립적인 문서 소스**가 있었으며, 어느 하나도 서로 일치하지 않았습니다. `simd`와 `archsimd` 모두에 문서화된 90개의 `(receiver, name)` 쌍은 모두 문서 텍스트가 달랐고, portable 패키지 내에서는 `simd_stubs.go`(midway 생성)와 `simd_emulated.go`(수작업 작성)가 미러링된 336개 메서드 중 40개에서 서로 어긋나 있었습니다. `Add` 메서드의 경우 세 가지 서로 다른 문구로 제공되었습니다:

| Where | Text | Source |
|---|---|---|
| `ops_amd64.go`, `ops_sve.go` | *Add는 두 벡터의 해당 요소를 더합니다.* | `categories.yaml` |
| `ops_wasm.go` | *Add는 x와 y를 요소별로 더한 결과를 반환합니다.* | wasmgen, inline |
| `simd_stubs.go`, `simd_emulated.go` | *Add는 x와 y의 요소별 합계를 반환합니다.* | `midway/comments.yaml` |

124개의 메서드 이름이 둘 이상의 제너레이터에 의해 생성되었습니다. 이는 의견 불일치가 발생하기 가장 쉬운 지점입니다. 선언의 대부분은 `simdgen`이 차지하고 있지만, 나머지는 `tmplgen`, `wasmgen`, `midway` 및 직접 작성한(hand-written) 코드가 보유하고 있으며, 이 세트들은 서로 중첩됩니다. 따라서 `simdgen`만 확인하는 도구는 문제의 상당 부분을 놓치게 됩니다 (`SPEC-STATS.txt` §1에 제너레이터별 카운트가 기록되어 있습니다).

제너레이터는 생성된 코드를 `specfill`로 전달하며, `specfill`은 디스크에 쓰기 전에 시그니처를 확인하고 문서를 주입합니다. 최종 상태에서 제너레이터는 선언과 구현 노트(§1.6)를 출력하지만, 자체적인 API 설명 문구(prose)는 생성하지 않습니다. `refgen`이 하는 것처럼 `specgen`이 전체 선언을 출력하게 하는 대안은, 그렇게 하면 설계서(spec)와의 일치 여부가 구조적으로 당연해져서 검증할 내용이 남지 않게 되므로 거부되었습니다. API에 대한 내부 모델이 변경된 제너레이터가 있다면, 그 오류가 조용히 덮여버릴 것입니다. 템플릿이 여전히 시그니처를 생성하기 때문에, `specfill`은 동일한 선언에 대한 두 개의 독립적인 증거를 확인하고 이를 비교할 수 있습니다. 즉, 단 한 번의 AST 순회(walk)로 문서 주입, 시그니처 검증, 커버리지 보고를 모두 수행할 수 있습니다.

결과:

- **`specfill`은 대체가 아니라 오버라이드(override)입니다.** 생성기(Generator)들은 계속해서 현재의 문서를 생성하며, `specfill`은 명세(spec)가 해당 연산을 알고 있는 경우에만 명세 소유 단락을 교체합니다. 따라서 폴백(Fallback)은 자동으로 이루어지며, 일괄적인 변경일(flag day)은 필요하지 않습니다. 텍스트가 없는 생성(Prose-less emission)은 생성기의 문서 소스가 비워졌을 때 도달하는 *최종 상태*이지, 전제 조건이 아닙니다.
- **wasmgen과 tmplgen은 flush 전 호출 한 번만 필요하며**, 생성하는 노트가 §1.6의 접두사를 따르도록 하면 됩니다.
- **이 기능을 `gentools.Files.Flush()`에 연결하지 마십시오.** `gentools`는 일반 유틸리티입니다. 이를 specgen에 결합하면 모든 소비자가 `golang.org/x/tools/go/packages`와 로드 가능한 명세 트리(spec tree)에 의존하게 됩니다. gentools에 좁은 범위의 훅(hook) 메커니즘을 두고 생성기당 몇 줄의 코드를 추가하는 것이 경계를 유지하는 방법입니다.

## 1.6 문서 소유권 관례 (The doc-ownership convention)

`specfill`은 기존 문서 주석의 일부를 다시 작성하므로, 어느 부분을 수정할 수 있는지에 대한 규칙이 필요하며, 두 번 실행했을 때 결과가 동일한 멱등성(idempotent)을 유지해야 합니다. "첫 번째 단독 `//` 위의 모든 내용"이라는 명백한 규칙은 작동하지 않습니다. CL 831485에서는 문서화된 선언 3,920개 중 2,759개만이 해당 구분자를 가지고 있었습니다. 또한 spec 자체의 문서에는 빈 주석 줄이 포함되어 있습니다. 예를 들어 `Add`의 경우 요약, `//`, 그리고 `z[i] = x[i] + y[i]` 순으로 구성되어 있습니다. 따라서 단독 `//`를 사용하는 방식은 멱등성을 보장하지 않습니다.

**규칙.** 문서 주석(doc comment)은 명세 소유 단락(spec-owned paragraphs), 이어서 "구현 노트(implementation notes)", 그리고 지시어 주석(`//go:fix inline` 및 이와 유사한 형태) 순으로 구성됩니다. 명세 소유 단락은 연산의 동작을 설명합니다. 구현 노트는 특정 타겟이 연산을 어떻게 구현하는지에 대한 세부 사항입니다. 섹션은 반드시 이 순서대로 나타나야 하며, 도구가 이를 검증합니다.

*구현 노트(implementation note)*는 정해진 접두사 세트 중 하나로 시작하는 단락을 의미합니다: `Asm:`, `CPU Feature:`, `Emulated[,\n]`, `Deprecated:`, `Performance:`, 또는 `Note:`. 일치 여부는 정확히 일치해야 하며 대소문자를 구분합니다. 단락의 첫 번째 줄만 확인하므로, 노트는 접두사를 결합(`Asm: VPADDD, CPU Feature: AVX`)하거나 자유롭게 줄바꿈을 할 수 있습니다.

**검사.** 멱등성(idempotence)을 위해서는 엄격한 순서가 필요하며, 도구들은 이를 유지하기 위해 다음과 같은 검사를 수행합니다: (a) 기존 주석에서 명세 소유 단락(구현 노트 접두사가 없는 단락)은 반드시 구현 노트(구현 노트 접두사가 있는 단락)보다 앞에 나타나야 하며, 구현 노트는 반드시 지시어 주석(directive comments)보다 앞에 나타나야 합니다. (b) 명세의 문서는 노트 접두사로 시작하는 줄을 포함해서는 안 되며, 명세는 이를 표준 `go/doc/comment` 형태로 저장합니다.

**Rewrite.** `specfill`은 spec에 해당 선언에 대한 항목이 있고 체크 (a)를 통과했을 때만 주석을 다시 씁니다. 새로운 주석은 spec 문서, 구현 노트(implementation notes)가 있는 경우 빈 줄, 변경되지 않은 해당 노트, 그리고 변경되지 않은 지시어(directives) 순으로 구성됩니다. 그 외의 모든 경우에는 주석을 그대로 둡니다. 이는 멱등성(idempotent)을 가집니다. (b)에 의해 삽입된 spec 문서는 절대 노트처럼 보이지 않으므로, 다음 실행 시 주석을 동일한 위치에서 분할하여 동일한 바이트를 생성합니다. 다만, 멱등성으로 *첫 번째* 실행에서 손실된 텍스트를 잡아낼 수는 없으므로, spec으로 전환하는 과정에서 새로 적용된 작업에 대해 생성된 문서들을 주의 깊게 검토해야 합니다.

**마커가 아닌 접두사를 사용하는 이유.** 대안은 `specfill`의 영역을 지시어 주석(`//spec:doc` … `//spec:end`)으로 묶는 것이었습니다. 이러한 방식은 godoc에서 보이지 않으며 기본적으로 안전합니다(마커가 없으면 아무것도 건드리지 않음). 하지만 모든 선언에 줄을 추가하게 되며, 텍스트가 왜 spec 외부에 있는지에 대해서는 아무런 설명도 해주지 않습니다. 접두사는 이미 노트가 가지고 있는 형태를 재사용하며, 생성된 파일과 직접 작성한 파일에서 동일하게 작동하고, spec이 아닌 각 텍스트 조각이 어떤 종류의 노트인지 명시하도록 강제합니다. 그 대가로 마커가 없는 텍스트는 기본적으로 spec 소유로 간주되는데, 이것이 모든 재작성 사항을 diff로 검토하는 이유이자, 생성기가 자체적인 API 산문을 내보내지 않게 된 이후에는 spec 소유 텍스트를 전혀 내보내서는 안 되는 이유입니다(`specfill` 참조).

## 1.7 오류와 허용 오차(tolerated gaps)의 차이

CL 831485에서, 둘 이상의 타겟에 대해 선언된 782개의 `(receiver, name)` 쌍 중 파라미터 또는 결과 *타입*이 서로 다른 경우는 단 하나도 없었습니다. 하지만 파라미터 이름이 일치하지 않는 경우가 72건, 결과 이름이 일치하지 않는 경우가 16건 있었습니다. 따라서 이 사양은 *교정적(remedial)이라기보다 예방적(preventive)*입니다. 즉, 타입 수준에서 해결해야 할 밀린 작업(backlog)은 없으며, 점진적인 마이그레이션이 상태 악화와 경주(racing decay)하는 상황도 아닙니다.

- **서명 불일치(Signature mismatch)는 오류입니다.** 사양(spec)이 알고 있는 작업에 대해 불일치가 발생했다면, 이는 사양 또는 생성기(generator)의 버그입니다.
- **누락된 사양 함수는** 전환이 완료될 때까지 허용됩니다.
- **매개변수 및 결과 이름은** 선언부에서 이름이 지정된 경우 확인됩니다(이름이 없는 경우는 사양에서 채워집니다; §1.8). 여기에는 두 가지 이유가 있습니다. 첫째, 이 이름들이 문서에 나타나므로 문서의 소스와 일치해야 하며, 둘째, 과거에 인자 이름이 혼동되거나 바뀌어 발생한 버그가 여러 건 있었기 때문입니다.
- **`specfill`은 내보내기(exported)된 선언만 고려합니다.** 이 덕분에 허용된 누락 목록이 수렴하게 됩니다. 세 개의 `ops_internal_*.go` 파일(amd64, arm64, sve) 모두 내보내기된 선언이 전혀 없으므로, 모든 컴파일러 전용 작업은 별도의 카테고리 없이도 `specfill`의 시야 밖에 있게 됩니다. 영구적으로 남는 잔여물은 `String`, `Len`, `ToArch` 메서드와 `xFromArch` 함수들로, 그 수가 적고 열거 가능합니다.

## 1.8 Named results

Spec은 결과값에 이름을 지정하며, 문서에서도 해당 이름들을 참조합니다 (`z[i] = x[i] + y[i]`). 하지만 제공되는 API에서는 결과값에 이름을 지정하는 경우가 거의 없습니다 (SPEC-STATS.txt §2). Spec의 문서가 archsimd의 문서가 될 때, Spec의 결과값 이름들도 함께 가져오지 않는다면 문서 내의 `z`에 대한 참조는 의미가 없게 됩니다.

결정: **spec이 선언을 다루는 경우, 해당 매개변수와 결과 이름은 spec에서 가져옵니다**. 따라서 이는 동일하게 spec에서 가져오는 문서(doc)와 일치하게 됩니다. 모든 결과에 이름을 지정하는 것은 목표가 아닙니다. 문서나 본문에서 해당 이름을 사용하는 경우에만 이름이 가치가 있으며, 나머지를 맹목적으로 이름 짓는 것은 누구에게도 도움이 되지 않습니다. spec이 다루지 않는 선언은 `spec-all`이 이를 다룰 때까지 기존 이름을 그대로 유지합니다.

`specfill`은 본문(body)을 건드리지 않고 이를 강제합니다. API의 이름 없는 인자/결과(`_` 포함)를 명세와 일치하도록 다시 쓰고, 양측 모두 인자/결과에 이름을 지정했으나 그 이름이 서로 다를 경우 불일치 오류를 보고합니다. 본문이 없는 선언의 경우, 중요한 것은 이름이 문서와 일치하는지 여부뿐입니다. 본문은 이름이 지정된 인자는 참조할 수 있지만 이름 없는 인자는 참조할 수 없으므로, 이름 없는 인자를 채우는 것은 안전하며 이름이 지정된 인자는 반드시 확인해야 합니다. SPEC-STATS.txt §2에서도 이 두 케이스를 동일한 방식으로 나누어 집계합니다.

## 1.9 동작 적합성은 병렬 트랙입니다

동작 적합성(Behavioral conformance)은 정적 분석과는 다른 병렬 트랙입니다. 정적 분석은 코드를 실행하지 않고도 특정 규칙을 준수하는지 확인할 수 있지만, 동작 적합성은 프로그램이 실행될 때 예상대로 작동하는지를 확인하는 것입니다.

동작 적합성을 검증하는 일반적인 방법은 테스트 케이스를 작성하여 실행하는 것입니다. 테스트 케이스는 다음과 같은 요소를 포함해야 합니다:

* **입력**: 함수나 메서드에 전달할 인자.
* **기대 결과**: 함수나 메서드가 반환해야 할 값 또는 발생해야 할 부수 효과(side effect).
* **실제 결과**: 실제 실행 결과.

만약 기대 결과와 실제 결과가 일치하지 않는다면, 이는 동작 적합성 위반으로 간주됩니다.

동작 적합성을 보장하는 것은 매우 중요합니다. 정적 분석을 통과하더라도 실제 실행 시에 버그가 발생할 수 있기 때문입니다. 따라서 정적 분석과 동적 테스트를 병행하여 소프트웨어의 품질과 안정성을 높이는 것이 권장됩니다.

동작 일치성(Behavioral conformance)은 **API 문서화 트랙(API documentation track)에 대한 강한 의존성이 없습니다**. 두 프로세스는 동일한 입력인 스펙 커버리지(spec coverage)를 독립적으로 소비하며, 서로 겹치지 않는 버그 클래스를 찾아냅니다. 예를 들어, 새로운 아키텍처의 `Sub`에서 인자가 서로 바뀌었을 경우, 시그니처와 문서 내용은 동일하므로 오직 동작 일치성 검사에서만 이를 발견할 수 있습니다.

부트스트래핑 적합성(conformance) 확인 순서가 중요합니다. **먼저 amd64를 기준으로 spec을 검증하십시오.** amd64는 가장 성숙한 타겟이며, 다른 증거가 없는 한 모든 실패는 spec의 버그입니다. amd64 구현에 버그나 하드웨어 특유의 코너 케이스가 있을 수 있지만, spec의 버그일 가능성이 훨씬 더 높습니다. spec과 amd64가 일치하게 되면, **그때 전환하십시오.** 이제 spec이 오라클(기준)이 되어 arm64, wasm, SVE 및 나중에 추가될 모든 아키텍처의 게이트 역할을 합니다. 이 순서를 바꾸게 되면 올바른 구현임에도 적합성 실패가 발생하며, 결국 당연하게도 구현체를 "수정"하려는 잘못된 방향으로 가게 됩니다.

우리가 실제로 목격하는 버그 클래스들로부터 유추한 하네스(harness) 요구사항: 타입별 엣지 케이스 입력값(0, ±1, MinInt, MaxInt, ±0, ±Inf, NaN, 포화 경계값)과 랜덤 벡터의 조합 — 균등 랜덤(uniform random) 방식으로는 포화(saturation)나 NaN 코너 케이스를 안정적으로 찾아낼 수 없습니다. 또한, 마스크 반전 오류는 랜덤 테스트를 약 절반의 확률로 통과하므로 명시적인 마스크 패턴이 필요합니다.

**이는 우리가 이미 성공적으로 진행했던 경로입니다.**
`simd/internal/test_helpers`는 `float32s`부터 `uint8s`까지, 그리고 마스크를 위한 `bools`에 이르기까지 타입별 입력 벡터를 보유하고 있습니다. 이는 엄선된 코너 케이스 목록(±0, ±Inf, quiet 및 signalling NaN, `MaxFloat`, 8비트 및 16비트 포화 경계값)을 고정된 길이까지 순환시켜 구축한 것입니다. `archsimd/internal/simd_test/helpers_test.go`에서는 `forSlice`/`forSlicePair`/`forSliceTriple`/`forSlicePairMasked` 헬퍼가 교차 곱(cross-product)을 위해 이 벡터들을 윈도우 단위로 훑으며, `map1`/`map2`/`map3`/`mapCompare`는 사양서 본문(spec body)과 동일한 형태로 기대 결과값을 요소별로 구축합니다. 또한 `grouped2`는 `doc-explore`에서 문제가 되었던 128비트 그룹화를 이미 처리하고 있습니다. `checkSlicesLogInput`은 허용 오차(tolerance)까지 인자로 받는데, 이는 `impl-defined`가 해결해야 할 어휘에 대한 첫 번째 접근 시도입니다.

`conform-fixed`가 해당 코드를 그대로 재사용할 필요는 없지만, 그렇다고 처음부터 다시 시작해서도 안 됩니다. `conform-fixed`가 추가하는 점은 각 작업별로 케이스를 직접 작성하는 대신 spec으로부터 케이스를 생성하는 것입니다.

## 1.10 진척도는 정규화가 아니라 이름으로 측정됩니다.

`apisum`은 이름들이 하나의 의미를 갖는지 *테스트*하는 것이 목적이므로 정규화가 필요합니다. 일단 이름들이 하나의 의미를 갖도록 강제하면, **메서드 이름 자체가 정확하게 그리고 별도의 비용 없이 동치 클래스(equivalence class)**가 됩니다. 커버리지는 집합의 교집합이 되며, 이는 `cmd/specstats`에서 이미 계산하고 있습니다. 이름 정규화도 필요 없고, 유지하거나 폐기해야 할 복잡한 패턴 매칭 규칙도 필요 없습니다.

주의 사항(해결보다는 인지하고 있어야 할 점): `LoadInt8x16`, `LoadInt8x32` 등 하나의 spec 함수에서 파생된 템플릿 이름 패밀리들은 커버리지 메트릭의 분모를 증가시킵니다. 이는 API *표면(surface)*을 측정하는 관점에서는 논리적으로 맞을 수 있습니다. "spec에 N개의 함수가 있으며 M개의 이름을 커버함"과 같이 두 수치를 모두 보고하는 것이 어느 하나만 보고하는 것보다 더 유익합니다.

제공해주신 번역 대상 콘텐츠가 없습니다. 번역할 Markdown 내용을 입력해 주시면, 지침에 따라 기술적으로 정확하게 한국어로 번역해 드리겠습니다.

# Part 2 — Task graph

27개의 작업은 6개의 **트랙(tracks)**으로 나뉩니다. 트랙은 사람 간에 작업을 분담하고 파트 3를 쉽게 살펴볼 수 있도록 나누는 방법입니다. 트랙은 단계(phase)가 아니며, 작업의 순서를 암시하지 않습니다. 각 트랙의 작업들은 일반적으로 작업 의존성 그래프에서 군집을 이루지만, 트랙 간 의존성도 존재합니다.

| | 트랙 | 정의 | 작업 |
|---|---|---|---|
| **A** | 결정 사항 (Decisions) | 인간의 판단이 필요한 사항; 선행 조건 없음, 모든 다운스트림 작업의 블로커가 됨 | `width`, `compiler-ops`, `convert-lo`, `mask-bits`, `impl-defined` |
| **B** | 계측 및 강제 적용 (Instrumentation and enforcement) | `specfill`을 구축한 후, 이를 권위 있는 기준으로 설정 | `specfill`, `fill-gen`, `named-results`, `gen-docs`, `fill-enforce` |
| **C** | 적합성 (Conformance) | `simdref`를 대상으로 한 동작 테스트 | `ci-audit`, `conform-fixed`, `validate-amd64`, `conform-scalable`, `conform-flip` |
| **D** | 명세 내용 (Spec content) | 명세 함수, 문서 및 본문 작성 — 공통 병목 구간 | `doc-explore`, `spec-common`, `spec-all` |
| **E** | 기존 입력 제거 (Retiring the old inputs) | 5가지 비명세 문서 소스 제거 후, `categories.yaml` 처리 | `comments-yaml`, `doc-triage`, `handwritten-fill`, `template-docs`, `cat-rehome`, `compiler-ops-impl`, `cat-delete` |
| **F** | simdgen 내부 구조 (simdgen internals) | 시그니처 리팩토링 후, 명세로부터 시그니처 소싱 | `sig-refactor`, `sig-from-spec` |

## 의존성 (Dependencies)

모든 전제 조건이 체크되면 작업을 시작할 수 있습니다. 필수 의존성(Hard dependencies)은 `Needs`로 표시하며, 선택적 의존성(soft dependencies) — 해당 조건이 없어도 작업은 가능하지만 효율이 떨어지거나 가치가 낮아지는 경우 — 은 `Prefers`로 표시합니다.

태스크는 번호가 아닌 이름으로 명명됩니다. 이는 다른 태스크를 바로 옆에 삽입하더라도 태스크의 정체성이 유지되도록 하며, "`cat-rehome`을 구현함"이라고 적힌 CL이 1년 후에도 여전히 의미를 갖게 하기 위함입니다. 순서는 행 순서로 결정됩니다. 테이블은 위상 정렬(topologically sorted)되어 있으며(`Needs`와 `Prefers` 모두 엣지로 간주함), 순위가 같을 경우 트랙(track)에 따라 결정됩니다. 따라서 위에서 아래로 읽는 것이 작업을 수행하는 적법한 순서가 되며, 편집 과정에서 이 규칙이 깨지면 `cmd/spectasks`가 실패합니다. 전제 조건과 트랙이 허용하는 위치 어디든 행을 추가하여 태스크를 추가하십시오.

| ✓ | T | Task | 내용 | 필요 사항 | 선호 사항 |
|---|---|---|---|---|---|
| [x] | A | `width` | 가변 너비(scalable width) 해결 | — | — |
| [ ] | A | `compiler-ops` | 컴파일러 전용 연산(ops) 결정 | — | — |
| [ ] | A | `convert-lo` | `ExtendLo*`/`ConvertLo*` 형태 및 명명 규칙 | — | `width` |
| [ ] | A | `mask-bits` | 마스크 비트맵 로드/스토어 형태 및 명명 규칙 | — | `width` |
| [ ] | A | `impl-defined` | 구현 정의 동작(implementation-defined behavior) 정책 | — | — |
| [x] | B | `specfill` | API 워커 + 리포트 모드 | — | — |
| [x] | B | `fill-gen` | 생성기에 `specfill` 연결 | `specfill` | — |
| [x] | B | `named-results` | 매개변수 및 결과 이름을 명세와 일치시킴 | `fill-gen` | — |
| [x] | B | `gen-docs` | 생성된 출력물에 명세 문서 주입 | `fill-gen` | `named-results` |
| [x] | B | `fill-enforce` | 시그니처 + 이름 불일치를 에러로 처리 | `named-results` | — |
| [x] | C | `ci-audit` | CI/하드웨어 감사 | — | — |
| [ ] | C | `conform-fixed` | 적합성 하네스, 고정 너비 타입 | `ci-audit` | `specfill` |
| [ ] | C | `conform-scalable` | 적합성 하네스, 가변 너비 타입 | `width`, `conform-fixed` | — |
| [x] | D | `doc-explore` | 까다로운 패밀리에 대한 문서화 메커니즘 탐색 | — | — |
| [x] | D | `spec-common` | 공통 연산 명세화 | `width`, `doc-explore` | `specfill` |
| [ ] | C | `validate-amd64` | amd64를 대상으로 명세 본문 검증 | `conform-fixed`, `spec-common`, `impl-defined` | — |
| [ ] | C | `conform-flip` | 적합성 검사 방향 전환 | `validate-amd64`, `conform-scalable` | — |
| [ ] | D | `spec-all` | 대량 명세 마이그레이션 | `spec-common`, `convert-lo`, `mask-bits` | `specfill`, `fill-enforce` |
| [ ] | E | `doc-triage` | 수기 작성 문서 충돌 조정 | `specfill` | `spec-common` |
| [x] | E | `comments-yaml` | `midway/comments.yaml`에서 명세로 대체된 문서 제거 | `gen-docs`, `spec-common` | `fill-enforce` |
| [ ] | E | `handwritten-fill` | 수기 작성 파일에 `-w` 활성화 | `gen-docs`, `doc-triage` | — |
| [ ] | E | `template-docs` | 생성기 제공 API 문서 폐기 | `gen-docs`, `spec-all` | — |
| [ ] | E | `cat-rehome` | `categories.yaml`의 비문서 필드 이전 | `template-docs` | — |
| [ ] | E | `compiler-ops-impl` | 컴파일러 전용 연산 표현 구현 | `compiler-ops`, `cat-rehome` | — |
| [ ] | F | `sig-refactor` | simdgen 시그니처 리팩토링 | — | — |
| [ ] | F | `sig-from-spec` | simdgen이 명세로부터 시그니처를 가져옴 | `sig-refactor`, `cat-rehome`, `compiler-ops-impl` | — |
| [ ] | E | `cat-delete` | `categories.yaml` 삭제 | `sig-from-spec` | — |

**임계 경로(Critical path).** [SPEC-TASKS.dot](SPEC-TASKS.dot)에서 빨간색으로 표시됩니다. 이는 `Needs` 엣지로 연결된 가장 긴 체인 상의 모든 태스크를 의미합니다. 이 중 어느 하나라도 지연되면 프로젝트 전체가 지연됩니다. `cmd/spectasks`가 테이블로부터 이를 도출하므로, 여기에서 다시 기술하지는 않습니다.

트랙 B는 선수 조건이 없으므로 즉시 시작하여 자체적인 속도로 완료될 수 있습니다. 다만 `gen-docs`가 트랙 E 작업 중 세 가지의 게이트 역할을 합니다.
`sig-refactor`는 `sig-from-spec` 전까지는 다른 모든 요소로부터 독립적입니다.

## 마일스톤

마일스톤(Milestone)은 자체적인 작업을 가지지 않으며, 알릴 가치가 있는 지점들을 의미합니다. 마일스톤은 해당 작업들이 완료(ticked)되었을 때 달성되므로, 별도로 유지해야 할 상태가 없으며 여기서 동기화할 내용도 없습니다.

| 마일스톤 | 달성 시점 | 의미 |
|---|---|---|
| **M1 — Enforced** | `fill-enforce` | 명세(Spec)가 다루는 범위에 대해 권위적입니다. 이름이나 서명이 명세와 일치하지 않는 경우, 두 패키지 모두에서 4개 타겟 전체의 빌드가 실패합니다. |
| **M2 — Documented** | `comments-yaml`, `handwritten-fill`, `spec-all`, `template-docs` | 두 public 패키지의 모든 오퍼레이션 문서 주석이 명세로부터 유도됩니다. SPEC-STATS.txt의 "docs sourced from spec" 수치가 100%가 됩니다. |
| **M3 — Gated** | `conform-flip` | 적합성(Conformance) 검사가 명세 우선으로 실행됩니다. 따라서 나중에 추가되는 아키텍처는 반영되기 전에 반드시 명세와 일치해야 합니다. |
| **M4 — Complete** | `cat-delete` | `categories.yaml`이 삭제되며, 명세가 API에 대한 유일한 수동 작성 설명서가 됩니다. 아래 섹션을 참조하세요. |

## 그래프

[SPEC-TASKS.dot](SPEC-TASKS.dot)는 위의 두 테이블을 그립니다. 렌더링된 그래프는 자체적인 범례(key)를 가지고 있습니다. Track은 클러스터가 아닌 노드 색상으로 표시되는데, 이는 클러스터의 경우 연속적으로 배치되어야 하며, 이는 그래프가 보여주려는 왼쪽에서 오른쪽으로의 의존성 순서와 충돌하기 때문입니다.

`dot -Tsvg SPEC-TASKS.dot -o SPEC-TASKS.svg`

이 문서는 생성된 파일이며, 생성기(generator)가 동시에 검사기(checker) 역할도 수행합니다. 이 문서는 의존성을 세 군데에서 명시합니다: 파트 2의 테이블, 파트 3의 `Needs:`/`Prefers:` 라인, 그리고 파트 3의 `Blocks:` 라인(동일한 엣지를 역방향으로 표시)입니다. 따라서 이 내용들이 서로 일치하지 않거나, 그래프가 재생성되지 않은 경우 `go test ./cmd/spectasks`는 실패합니다. 또한, 임계 경로(critical path)를 도출합니다.

## 여기에서 시작하세요

시작 가능한 작업은 의존성 테이블에서 체크되지 않은 `Needs`가 없는 작업들입니다. 1~3명 규모의 팀에게는 `Needs`가 전혀 없는 모든 작업을 포함하는 다음과 같은 초기 할당 방식이 합리적입니다.

- **명세의 타입 모델에 가장 강력한 영향:** `width`, 그다음 `convert-lo` 및 `mask-bits`. 이들은 가장 긴 체인의 뿌리가 되며, 지연될 경우 비용이 가장 많이 듭니다.
- **API 시맨틱 소유:** `impl-defined` 및 `compiler-ops` — 순수한 결정 사항으로 코드가 없으며, 하위의 모든 작업이 이를 기다립니다.
- **툴링 선호:** `specfill`, 그다음 `fill-gen` 및 `named-results`.
- **규모가 큰 작업을 단독으로 수행:** `sig-refactor`. 선행 조건이 없으며, 모든 단계에서 바이트 단위로 검증 가능합니다.
- **비용이 저렴하며 관계없이 조기에 수행할 가치가 있음:** `doc-explore` 및 `ci-audit`.

## "완료(done)"의 정의

`cat-delete` 이후, `simd/internal/spec`이 API의 유일한 수동 작성 설명서가 됩니다. 모든 연산의 이름, 시그니처 및 문서는 공개 패키지와 4개의 모든 타겟에서 이 spec으로부터 파생되며, `specfill`은 이들 중 어느 하나라도 일치하지 않을 경우 빌드를 실패 처리합니다. `categories.yaml`은 삭제되었습니다. `midway/comments.yaml`은 벡터 타입, `VectorSize`, `String` 및 `Len`과 같이 spec에서 설명하지 않는 부분만 문서화합니다. wasmgen과 tmplgen은 더 이상 doc 문자열을 보유하지 않습니다. 수동으로 작성된 구현체는 그대로 유지되지만, 해당 연산의 doc 주석은 자동으로 생성됩니다.

simdgen은 여전히 존재하며 여전히 unification 기반입니다. 그 이유는 §1.1에서 설명합니다. 변경된 점은 그 역할입니다. 이제 unifier는 API를 정의하지 않고, 하나의 `go_GOARCH.yaml` 항목을 그와 일치하는 모든 구체적인 머신 명령어로 확장하는 역할만 수행합니다. 명령어의 불규칙성은 실제로 존재하며 어딘가에는 기록되어야 하므로, `go_GOARCH.yaml`과 그 quirk 필드들은 그대로 유지됩니다. 컴파일러 백엔드 생성 과정은 전 과정에 걸쳐 변경되지 않습니다.

제공해주신 원문 콘텐츠가 없습니다. 번역할 Markdown 내용을 입력해 주세요. 내용을 제공해 주시면 기술적인 맥락을 유지하며 정확하게 한국어로 번역해 드리겠습니다.

# 파트 3 — 작업 상세 내용

많은 완료 기준이 "생성된 출력이 바이트 단위로 동일함"이며, 이는 `_gen` 디렉토리에서 `go run . -diff`로 확인합니다. 이 명령은 3개 타겟 모두에 대한 simdgen을 포함하여 모든 생성기를 실행하므로, 먼저 XED 및 ARM ISA 데이터가 필요합니다 — `fetch-xed.sh` 및 `fetch-arm64.sh`를 참조하십시오. 드라이버에는 `-arch` 플래그가 없습니다. `-arch`는 `simdgen`을 직접 실행할 때 사용하는 플래그입니다.

## 트랙 A — 결정 (Decisions)

사람의 판단이 필요합니다. 전제 조건은 없지만, 각각이 후속 작업을 차단합니다. 이것이 바로 이 작업들이 우선순위를 갖는 이유입니다. 각 작업은 코드상으로는 작지만 그 결과는 매우 큽니다.

### `width` — 확장 가능한 너비 결정
**완료:** [x] · **필요:** — · **차단됨:** `spec-common`, `conform-scalable` · **리스크:** `risk-concrete-width`

`simd/internal/spec/types.go`는 `scalableWidth = 4096`을 하드코딩하고 있으며, `simdref`는 해당 너비로 빌드됩니다. 반면 `archsimd`의 SVE는 런타임 `vl()`을 사용합니다. 따라서 가변 길이(scalable) 타입의 적합성 테스트(conformance test)는 서로 다른 길이의 벡터를 비교하게 됩니다. Spec의 TODO 항목에서도 이 문제를 지적하고 있으나 아직 해결되지 않은 상태입니다.

특히 4096비트는 shuffle과 같이 벡터 내의 인덱스를 참조하는 연산에서 문제를 일으키며, 이것이 RISC-V RVV를 제외한 모든 플랫폼이 2048비트 이하인 이유입니다. 이 작업을 해결하려면 2048비트보다 넓은 벡터를 지원할 것인지 여부를 결정해야 할 수도 있습니다.

무엇이 잘못되지 *않았는지* 유의하십시오. spec의 타입 시스템은 확장 가능한 너비(scalable widths)를 위해 설계되었으며 이를 적절히 처리합니다. 간극은 spec이 구체적인 적합성 오라클(conformance oracle)로 사용될 때만 나타나며, 해결되지 않은 문제는 매우 좁은 범위에 한정되어 있습니다. 즉, spec이 일반적인 타입 메커니즘을 방해하지 않으면서 호출자가 선택한 너비로 실행될 수 있는지 여부입니다.

이것이 첫 번째 이유는 이번 수정이 spec의 타입 모델을 변경할 수 있기 때문입니다. 즉, width를 컴파일 타임 상수가 아닌 런타임 파라미터로 변경하게 되며, 이는 모든 spec 함수 본문에 영향을 미칩니다. 수백 개의 본문이 존재한 후에 이를 해결하는 것은 지금처럼 본문이 적을 때 해결하는 것보다 훨씬 더 어렵습니다 (SPEC-STATS.txt §1).

**커밋 사항.** (1) `Vec`, `makeVec`, `lanes`, `refgen` 및 conformance harness에 미치는 영향과 함께 옵션들을 작성하십시오. 지금까지 검토된 내용: spec 실행 시 width를 매개변수화하거나, `simdref` 생성 시 width를 설정 가능하게 만들거나, 초기에는 conformance 범위를 고정 width로 제한하고 나중에 처리하는 방식입니다. (2) 선택한 방식을 `internal/spec`에 구현하십시오. (3) `internal/simdref`를 다시 생성하고 `cmd/specls` 출력 결과가 변경되지 않았는지 확인하거나, 변경된 사항이 있다면 설명하십시오.

**완료 조건:** 확장 가능 타입(scalable-typed) 연산이 선택된 타겟과 일치하는 너비로 `simdref`를 통해 실행될 수 있고, 해당 선택 사항이 `internal/spec/doc.go`에 문서화되었을 때.

### `compiler-ops` — 컴파일러 전용 ops 결정
**완료:** [ ] · **필요 사항:** — · **차단 대상:** `compiler-ops-impl`

`categories.yaml`이 삭제된 후, 내보낸 선언(exported declaration)을 생성하지 않는 컴파일러 전용 항목(SPEC-STATS.txt §4)과 `noTypes` / `noGenericOps` 스위치를 어떻게 표현할지 결정하십시오. 이는 명확한 해답이 없는 유일한 핵심 블로커(hard blocker)이므로, 조기에 해결하시기 바랍니다.

참고 §1.7: `specfill`은 내보내기(exported) 선언으로 범위가 제한되므로, 이는 체커(checker)나 컨포먼스 트랙(conformance tracks)을 차단하지 *않습니다*.

디자인 노트에는 `categories.yaml`이 삭제된 후 다음 항목들이 어디로 이동해야 하는지도 명시해야 합니다: `archsimd/ops_internal_*.go` 내 비공개(unexported) 메서드의 문서 주석으로 제공되는 컴파일러 전용 항목들의 `documentation:`, 해당 항목들의 `commutative`, `signed` 및 `out` 필드, 그리고 `go_arm64.yaml`에서 사용하는 `noGenericOps`입니다. 이 문서는 엄격하게 내부용이므로, 사용자 대상 API 문서보다 낮은 기준이 적용됩니다. 즉, 사양(spec)에서 가져오거나 `specfill`을 거칠 필요가 없으며, M2를 충족하지 않아도 됩니다. 컴파일러 전용 연산(op)의 다른 설명 옆에 유지되기만 한다면 어디에 배치되어도 무방합니다.

**Commits.** 이 문서 또는 `internal/spec/doc.go`에 디자인 노트 하나를 추가하여, `_gen/simdgen`의 모든 컴파일러 전용 작업(`grep -h "go: [a-z]" ops/*/categories.yaml | sort -u` 및 대문자로 시작하는 `noTypes` 항목들)을 목록화하고, `categories.yaml`이 제거된 후 각 제품군(family)의 설명, 문서 및 나머지 필드가 어디에 위치하게 될지 명시합니다. 후보안: `//specgen:unexported` 지시어 사용, 컴파일러 전용 작업을 보유하는 네 번째 simdgen 입력 추가, 또는 이들이 API가 아닌 아키텍처별 로워링(lowering) 세부 사항이라는 근거로 `go_GOARCH.yaml`에 남겨두는 방법이 있습니다.

결정 사항이 문서화와 모든 남은 필드를 포함하여 서면으로 작성되었고, 추가적인 설계 작업 없이 `compiler-ops-impl`을 구현할 수 있는 상태가 되었을 때 **완료된 것으로 간주합니다.**

### `convert-lo` — `ExtendLo*` / `ConvertLo*` 형태 및 명명 규칙
**완료:** [ ] · **필요:** — · **선호:** `width` · **차단:** `spec-all` · **리스크:** `risk-spec-defects`

고정 너비(fixed-width)와 확장 가능 벡터(scalable vectors) 모두에서 저정밀도 요소 확장(low-elements widening) 제품군의 형태와 명명 방식을 결정합니다. 이는 기계적인 수정이 아닌 API 설계 결정입니다. 서로 얽혀 있는 세 가지 문제입니다:

1. **형태(Shape).** `ExtendLoLToZ`는 `x Vec[E,W]`와 `z Vec[zE,W]`를 선언하며, 이는 동일한 전체 너비를 가집니다. 하지만 실제 제공되는 API는 너비를 확장합니다. 예를 들어 `Int8x16.ExtendLo8ToInt64()`는 128비트를 입력받아 512비트를 반환합니다. 따라서 명세(Spec)에서 8개의 실제 선언이 누락되었으며, 어떤 플랫폼에도 존재하지 않는 너비 보존형 선언들이 임의로 만들어졌습니다.
2. **명명법(Naming).** `//specgen:name ExtendLo{zL}To{zE}`는 *결과 레인 수*를 포함하므로, 개념적으로 동일한 작업이라도 너비에 따라 서로 다른 이름을 갖게 됩니다. API는 128비트 리시버만 사용하도록 결정되어 이 점이 가려져 있습니다.
3. **확장성(Scalable).** `converts.go`의 TODO에 이미 리터럴 `zL`이 가변 길이(scalable) 벡터에서 작동할 수 없음을 명시하고 있으며, 리시버와 타겟 타입에 의해 이미 암시되므로 숫자를 완전히 제거할 것을 제안하고 있습니다. 예를 들어 `Uint8x16.ExtendLo2ToUint64`는 실제로는 하위 절반이 아니라 하위 *8번째*이므로, 작동하는 경우라도 숫자가 오해의 소지가 있다고 볼 수 있습니다.

여기서 이루어지는 모든 이름 변경은 API에 노출되며, `spec-all`이 Converts 제품군을 마이그레이션하기 전에 결정되어야 합니다. `categories.yaml`의 Converts 문서 대부분이 바로 그곳에 포함되어 있기 때문입니다.

**커밋 사항.** (1) 고정 너비(fixed-width) 및 가변 너비(scalable) 벡터에 대한 옵션과 그에 따른 영향을 정리하십시오. 여기에는 레인 수(lane count)를 이름에 유지할지 여부가 포함됩니다. (2) `ExtendLoLToZ`를 재설계하고, 현재 `zL<xL` 제약 조건으로 인해 하드웨어에서 제공하지 않는 변환을 허용하고 있는 `ConvertLoLToZ`를 다시 점검하십시오. (3) API 이름이 변경되는 경우, 스펙 변경과는 별개로 제너레이터(generators)를 통한 이름 변경을 별도의 CL로 반영하십시오.

`cmd/specls`가 API가 가진 `ExtendLo*` 선언과 의도된 최대주의적 추가 사항들을 정확하게 생성하고, 확장 가능한 네이밍 문제에 대한 답변이 `internal/spec/doc.go`에 작성되었을 때 **완료**된 것으로 간주합니다.

### `mask-bits` — 마스크 비트맵 로드/스토어 형상 및 명명 규칙
**완료:** [ ] · **필요:** — · **선호:** `width` · **차단:** `spec-all` · **리스크:** `risk-spec-defects`

고정 너비의 `ToBits` 및 `MaskNxMFromBits`(예: `Mask8x16FromBits`)에 대응하는 확장 가능한(scalable) 카운터파트—현재 `Mask*s.Store` 및 `LoadMask*s`로 구현된 기능—를 확정하십시오. 또한, 현재 중간 문서에서 엘리먼트 시맨틱(element semantics)으로 설명하고 있는 포터블 `simd.Mask*s`에서 `Store`와 `ToBits`가 의미하는 바를 확정하십시오.

API는 SVE의 가변 길이 마스크(`archsimd/types_sve.go`)에 대해서만 `Store(bits []uint16)`를 선언하며, 이는 `LoadMask8s(bits []uint16)` 등과 쌍을 이룹니다. 이는 SVE 프레디케이트 비트를 바이트 단위(byte granularity)로 저장합니다. 고정 길이 마스크에는 `Store`가 없으며, 대신 `ToBits() UintN`을 가집니다 (사양: `MaskToBits`, `internal/spec/masks.go`, `FixedWidth`로 제한됨). 따라서 `Mask*s.Store`는 다른 모든 `Store`와는 다른 의미를 가지며, 이는 "하나의 이름, 하나의 의미(one name, one meaning)" 규칙을 위반할 가능성이 있습니다. 또한 비트 레이아웃이 레인별(per-lane) 방식이 아닌 SVE 표현 방식을 따르는데, 이는 §1.3의 "작업 자체의 시맨틱에 대한 주장" 테스트를 통과하지 못한다고 볼 수 있습니다.

**커밋(Commits).** (1) 고정 너비(fixed-width) 및 가변 너비(scalable) 마스크, 그리고 portable 패키지에 대한 옵션과 그에 따른 결과를 작성하십시오. (2) 이에 맞게 사양(spec)을 변경하십시오. (3) API 이름이 변경되는 경우, 제너레이터(generators)를 통해 이름 변경 사항을 별도의 CL로 반영하십시오.

**완료 조건:** SPEC-STATS.txt §5에 `Store` 마스크 결함이 기재되지 않고, 해당 선택 사항이 `internal/spec/doc.go`에 기록되었을 때.

### `impl-defined` — 구현 정의 동작 정책(Implementation-defined behavior policy)
**완료:** [ ] · **필요 사항:** — · **차단 대상:** `validate-amd64` · **리스크:** `risk-impl-defined-behavior`

SIMD API에서 무엇을 구현 정의 동작(implementation-defined behavior)으로 간주할지, 그리고 적합성 테스트(conformance testing)가 의미 있게 유지될 수 있도록 사양(spec)에서 이를 어떻게 표현할지 결정하십시오. 아키텍처마다 세부적인 차이가 있을 수 있습니다. 예를 들어, 부동 소수점 결과의 마지막 비트, 범위를 벗어난 셔플 인덱스, 포화(saturation) 경계, NaN 전파 및 부호 있는 0 등이 이에 해당합니다. 사양의 `math.go`에는 이미 `DotProductPairs` 오버플로에 관한 TODO가 있으며, 여기서 문제점을 명시하고 그 해결책 중 하나로 "아키텍처 종속적(architecture dependent)"으로 지정된 패닉(panic)을 제시하고 있습니다.

번역할 내용을 제공해 주시기 바랍니다. 영문 Markdown 콘텐츠를 보내주시면 지침에 따라 기술적으로 정확하게 한국어로 번역해 드리겠습니다.

1. **구현 정의(implementation-defined)란 무엇인가?** 작업별 API 시맨틱에 대한 판단입니다.
   양방향 모두로 비용이 발생합니다. 너무 많이 선언하면 적합성 검사가 실제 버그를 잡아내지 못하게 되고, 너무 적게 선언하면 올바른 구현체가 명세에 대해 실패하게 됩니다.
2. **어떻게 기록하는가?** 구현 정의 동작에는 적어도 두 가지 주요 범주가 있습니다: 예외 값 사례(예: 오버플로 동작은 완전히 정의되지 않음)와 정밀도(모든 아키텍처가 대략적으로는 동의하지만, 마지막 자릿수까지는 아닐 수 있음)입니다. 현재 명세 바디(spec bodies)는 정확한 값을 반환하며, "여기에는 어떤 값이라도 가능", "N ulp 이내", 또는 "명시되지 않았으나 플랫폼별로 결정론적(deterministic)"임을 나타내는 어휘가 없습니다. 무엇을 선택하든 `refgen`과 적합성 테스트 하네스(conformance harness) 모두가 이해할 수 있어야 하며, 이는 명세 바디의 형태를 변화시킵니다. 이것이 대다수의 명세가 작성되기 전에 이 문제가 해결되어야 하는 이유입니다. 기존 스위트의 `checkSlicesLogInput`은 이미 호출별 허용 오차(tolerance, §1.9)를 사용하고 있으며, 이는 수치적인 부분에 대한 선례가 됩니다. 하지만 "명시되지 않았으나 플랫폼별로 결정론적"인 부분에 대해서는 아무런 언급이 없습니다.

**Commits.** (1) 알려진 사례들을 조사합니다 — `DotProductPairs` 오버플로, float 변환 반올림, shuffle 인덱스 범위 초과, saturation 엣지, NaN/±0 처리 — 각 사례를 명세서에 정의됨(specified), 구현 정의(implementation-defined), 또는 정의되지 않음(undefined)으로 분류합니다. (2) `internal/spec/doc.go`에 사용할 명세 용어(spec vocabulary)를 선택하고 문서화합니다. (3) 실제로 구현 정의된 코너 케이스가 있는 연산 하나가 `refgen` 및 하네스를 통해 왕복(round-trip) 테스트가 가능할 정도로 구현합니다.

**완료 조건:** 아키텍처 종속적인 코너 케이스가 있는 연산을 명세(spec)에 작성하고, `simdref`로 생성하며, 지원되는 모든 타겟에서 거짓 실패(false failure) 없이 적합성 테스트(conformance-tested)를 통과했을 때 완료된 것으로 간주합니다.

## 트랙 B — 계측 및 집행 (Instrumentation and enforcement)

`specfill`을 빌드한 다음, 이를 authoritative하게 만드십시오. 트랙 C, D, F와는 독립적이며; `gen-docs`는 트랙 E의 세 가지 항목을 게이트합니다.

### `specfill` — API walker + report mode
**완료:** [x] · **필요:** — · **차단:** `fill-gen`, `doc-triage`

나머지 계획이 읽어오는 도구입니다.

`specfill`은 `specdoc.Fill`과 `cmd/specfill` 전체를 빌드합니다 — 여기에는 walk, spec index, 비교, 그리고 doc 코멘트 및 파라미터/결과 이름의 rewrite 작업이 포함됩니다. `fill-gen`은 rewriting 기능을 끈 상태로 이를 generator에 연결합니다. 이후 `named-results`와 `gen-docs`가 해당 부분에서 이름 채우기(name filling)와 doc 주입(doc injection) 기능을 활성화하며, `handwritten-fill`는 직접 작성한 파일들에 대해 `-w` 옵션을 활성화합니다.

**인터페이스.** `specdoc.Fill`은 라이브러리의 진입점입니다 — Go 소스가 입력되면 Go 소스가 출력됩니다: `func Fill(src []byte, idx *specgen.Index, opts Options) ([]byte, error)`. 생성자들은 쓰기 작업을 수행하기 전 버퍼에 대해 이 함수를 호출합니다 (§1.5). 검증 확인이 실패하면, `Fill`은 아래에 나열된 결과들이 포함된 `*Report`를 에러로 반환합니다. 호출자는 파일 간의 결과들을 조사하거나 결합하려는 경우 `errors.As`를 통해 이 에러를 식별할 수 있습니다. 옵션 필드:

- **RejectUnknown**은 spec 항목이 없는 내보내기 선언(exported declaration)을 에러로 처리할지 여부(`Report.UnknownDecls`에 기록됨)를 제어합니다. 전환 기간 동안에는 꺼져 있으며, 제너레이터는 `spec-all` 이후에 이를 켭니다. 이는 spec 함수를 작성하지 않고 오퍼레이션을 추가했을 때, 커버리지에서 조용히 누락되는 대신 생성 시점에 실패하도록 하기 위함입니다.
- **AllowDocRewrite**는 선언 spec 커버(covers)가 이미 spec 소유의 단락(§1.6)을 포함하고 있을 수 있는지 여부를 제어합니다. false(기본값)일 때, 이를 포함하는 각 항목은 에러로 처리됩니다(`Report.UnexpectedDocs`에 기록됨). 단, 구현 노트(implementation notes)와 지시어(directives)는 항상 허용됩니다. 제너레이터가 자체적인 API 산문(prose)을 출력하지 않게 되면(`template-docs`), 이는 조용한 문서 손실(`risk-silent-doc-loss`)에 대한 방어책이 됩니다. 즉, 노트 접두사가 누락된 제너레이터 단락은 `Fill`이 조용히 대체하는 대신 에러로 처리됩니다. 그 전까지 제너레이터는 이를 true로 설정합니다. 수동으로 작성된 파일은 설계상 산문을 포함하므로, `cmd/specfill`은 항상 이를 true로 설정하며 대신 `-diff`와 `-w` 가드에 의존합니다.
- **AllowNameMismatches**는 이름 불일치(name mismatches)를 허용할지 여부를 제어합니다. false(기본값)일 때, 이는 에러로 처리됩니다. 제너레이터는 `named-results`를 통해 이를 조정하기 전까지 전환 기간 동안 true로 설정할 수 있습니다.

추가로 두 개의 필드는 `Fill`이 무엇을 재작성할지 선택하며, 일부분만 적용하려는 호출자를 위해 제공됩니다. **NoFillDoc**은 문서 주석(doc comments)을 그대로 두고, **NoFillNames**는 이름 없는 인자를 이름 없는 상태로 유지합니다(따라서 이를 이름 불일치로 보고합니다). 기본적으로 `Fill`은 두 작업을 모두 수행합니다. 마지막으로, **Filename** 필드는 결과(findings)에서 위치에 레이블을 지정합니다.

**이름.** `Fill`은 §1.8에서 설명하는 방식대로 이름을 채우고 검사합니다. 선언에서 이름을 지정하지 않았거나(또는 `_`로 지정한) 인수는 spec의 이름을 가져오며, 이름이 지정되었으나 spec의 이름과 다른 인수는 불일치(mismatch)로 간주됩니다. `Fill`은 해당 선언에 타입이나 이름의 불일치가 없을 때만 선언의 이름을 다시 씁니다. 따라서 나머지 선언 이름들이 채워지기 전에 불일치 사항이 먼저 수정되어야 합니다.

`cmd/specfill`은 `gentools` 기반의 명령어로, 직접 작성한 파일에 `specdoc`을 적용합니다. 이 명령어는 `simd` 및 `archsimd` 내의 테스트가 아닌 `.go` 파일들을 탐색하며, 생성된 파일(제너레이터가 자체적으로 `Fill`을 호출함)은 건너뜁니다. 각 파일에 대해 `AllowDocRewrite` 옵션과 함께 `Fill`을 호출하고, 결합된 리포트를 출력합니다. `-diff`는 재작성 시 변경될 내용을 보여줍니다. `-w`를 사용하면 제자리에서 재작성(rewrite in place)합니다. 리포트에 발견 사항이 있거나 커밋되지 않은 변경 사항이 있는 경우 `-w`는 재작성 없이 중단되므로, git diff를 통해 수행된 작업의 전체 내용을 확인할 수 있습니다. `-no-fill-doc` 및 `-no-fill-names` 플래그는 해당하는 옵션을 설정합니다. CI 강제 적용은 명령 호출 방식이 아니라, 이 패키지의 `go test`(`fill-enforce`가 이를 연결함)로 구현되어 있습니다.

**보고서(Report).** 보고서는 영구적인 강제 적용 레이어입니다. API가 계속 진화함에 따라 보고서의 모든 항목은 전환 후에도 유용하게 유지되며, `fill-enforce`가 CI에서 실행하는 대상이 됩니다. 커버리지와 이름 관계(name relations)는 목표치에 수렴하는 전환 메트릭입니다. 이들은 `cmd/specstats` / SPEC-STATS.txt에 유지되며, 이 보고서의 일부가 아닙니다.

이 보고서에는 오류만 포함되며, 리라이트(rewrite) 결과의 미리보기는 제공하지 않습니다. `cmd/specfill`을 포함하여 `specdoc`을 사용하는 모든 컨슈머는 `gentools` 프로그램이므로, `-diff` 플래그를 통해 텍스트 삭제 내용을 포함하여 리라이트로 인해 디스크 상의 파일이 어떻게 변경될지를 정확하게 확인할 수 있습니다. 이러한 diff가 리라이트를 검토하는 방식이며, 이를 다시 계산하여 보고서에 포함하는 것은 동기화 상태를 유지해야 할 두 번째 복사본을 만드는 것에 불과합니다.

발생 가능한 오류는 다음과 같습니다:

1. **타입 시그니처 불일치 (Type signature mismatches)** — 매개변수나 결과 타입, 또는 그 개수가 spec과 walker가 찾은 선언부 간에 서로 일치하지 않는 경우입니다.
2. **이름 시그니처 불일치 (Name signature mismatches)** — 이름이 지정된 매개변수나 결과의 이름이 spec과 다른 경우입니다. 이름이 없는 항목은 `NoFillNames`가 설정되지 않은 한, 보고되는 대신 채워집니다. `AllowNameMismatches`가 설정된 경우 이 항목은 생략됩니다.
3. **Check (a) 위반** — spec이 다루는 선언부 내의 §1.6 순서 위반 사항입니다. `Fill`은 이러한 주석을 그대로 둡니다. spec이 다루지 않는 선언부는 확인되지 않습니다. 순서 규칙은 rewrite 작업이 멱등성(idempotent)을 갖도록 하기 위해 존재하며, `Fill`은 이를 절대 다시 쓰지 않습니다. 특히 수작업으로 작성된 파일에는 spec이 절대 다루지 않을 선언부가 포함되어 있을 수 있습니다. 각 선언부는 spec이 이를 다루는 시점부터 확인됩니다.
4. **알 수 없는 선언부 (Unknown declarations)** — `RejectUnknown`이 설정되었을 때, spec 항목이 없는 내보내기(exported) 선언부입니다.
5. **예상치 못한 문서 주석 (Unexpected doc comments)** — `AllowDocRewrite`가 false일 때, spec이 소유한 단락을 포함하고 있는 spec 대상 선언부입니다.

**Commits.** (1) `specgen`: `Load()` 결과에 대해 `(recv, name)`을 키로 하는 인덱스를 추가합니다. §1.6에 따라 주석 단락을 명세서 소유(spec-owned) 또는 구현 노트(implementation note)로 분류하는 함수를 추가합니다. 체크 (b)를 위반하는 명세서 문서를 거부합니다. (2) 새 패키지 `_gen/specdoc` 및 새 명령 `_gen/cmd/specfill`: AST 선언 워커(walker), 시그니처 및 주석 순서 비교, `error` 인터페이스를 구현하는 결과 보고, 그리고 `AllowDocRewrite` / `AllowNameMismatches` 옵션을 추가합니다. 시그니처 비교는 파싱된 `*ast.FuncDecl`을 명세서 자체의 표현식으로 변환하며, 이때 타입들은 `specexpr` 타입으로 변환됩니다. 한정 타입(qualified types)이 존재하지 않으므로(§1.4) 이것으로 충분하며, 이를 `specgen.Func`와 구조적으로 비교합니다. (3) `specdoc.Fill`의 재작성 엔진(문서 주석 및 시그니처 이름 모두)과 `cmd/specfill`의 인플레이스(in-place) 재작성 옵션(`-w`, `-no-fill-doc`, `-no-fill-names`)을 추가합니다.

**완료 조건:** 현재 트리에서 `specfill`을 실행했을 때, ( `-w` 옵션 없이) 아무것도 쓰지 않고 모든 리포트 결과가 위치 순서대로 출력될 때.

`SPEC-STATS.txt`는 시그니처에 대한 새니티 체크(sanity check) 파일입니다. `cmd/specstats`는 `Fill`과 동일한 방식(§1.8)으로 이름들을 계산하여 동일한 타입 및 이름 불일치를 산출하므로, `specfill`의 리포트는 해당 항목들에 대해 줄 단위로 `specstats`와 일치해야 합니다. 일치하지 않는 부분이 있다면 배포 전에 반드시 원인을 설명해야 합니다. 커버리지와 이름 관계는 전환 메트릭(transition metrics)으로서 `specstats`에 유지되며, 목표치에 도달하면 `specstats`는 폐기될 수 있습니다.

### `fill-gen` — 생성기에 `specfill` 연결
**완료:** [x] · **필요 항목:** `specfill` · **차단 항목:** `named-results`, `gen-docs`

각 제너레이터는 쓰기 작업을 수행하기 전 `specfill`을 통해 버퍼를 전달하며, 현재는 모든 재작성(rewriting) 기능이 꺼져 있습니다: `NoFillNames` (`named-results`가 이름 채우기를 활성화함) 및 `NoFillDoc` (`gen-docs`가 문서 주입을 활성화함). 또한 제너레이터들은 `AllowNameMismatches`를 설정하는데, 이는 `named-results` 전까지는 이름이 여전히 spec과 일치하지 않기 때문이며, `AllowDocRewrite`를 설정하는 이유는 `template-docs` 전까지는 제너레이터들이 자체적인 API 산문을 생성하기 때문입니다.

따라서 이 작업은 제너레이터들을 연결만 하며, 생성된 출력물은 변경되지 않습니다. 변경되는 점은 `Fill`의 나머지 검사들이 이제 생성 시점에 실행된다는 것입니다. 즉, 생성된 출력물에서 타입 불일치나 (a) 검사 위반이 발생하면 생성이 실패합니다. 두 경우 모두 옵션으로 허용할 수 없으며, `specfill`이 완료된 시점 기준으로 생성된 출력물에는 이러한 문제가 없습니다.

**Commits.** (1) `gentools`가 `specgen`에 의존하지 않도록 하는 좁은 범위의 후처리 훅(post-processing hook)을 추가합니다(§1.5 참조). (2) `simdgen`을 연결합니다. (3) `tmplgen`, `wasmgen`, `midway`를 연결합니다.

**완료 조건:** 4개의 제너레이터가 모두 `specfill`을 통해 라우팅되고, 생성된 출력값이 이전 트리와 바이트 단위로 동일할 때.

### `named-results` — spec와 파라미터 및 결과 이름 일치시키기
**완료:** [x] · **필요 항목:** `fill-gen` · **차단 항목:** `fill-enforce`

모든 declaration spec은 해당 spec의 parameter 및 result 이름을 포함합니다. §1.8을 참조하십시오. Declaration spec에 포함되지 않은 항목은 범위(scope) 밖에 있으며, `spec-all`이 이를 포함할 때 이름을 얻게 됩니다.

SPEC-STATS.txt §2에 카운트가 있으며, 이는 `specfill`이 처리하는 방식과 동일하게 나누어져 있습니다:

- **명세(spec)와 이름이 일치하지 않는 명명된 인자(Named arguments)**: 생성된 코드 또는 직접 작성한 코드에서 발생합니다. 명세 또는 API 중 이름이 더 좋지 않은 쪽(명세, 생성기의 템플릿 또는 입력값, 혹은 직접 작성한 파일)을 수정하여 해결합니다. 어느 쪽이든 diff는 이름과 해당 이름을 언급하는 문서 텍스트만 수정합니다. 이 작업이 우선순위를 갖습니다: `Fill`은 불일치가 있는 선언의 이름은 채우지 않습니다.
- **이름 없는 인자(Unnamed arguments)**: `Fill`이 명세로부터 이름을 채웁니다. 생성된 코드의 경우, 생성기에서 이름 채우기(name filling) 기능을 활성화하는 것을 의미합니다. 직접 작성한 파일의 경우, `specfill -w -no-fill-doc`가 이를 채웁니다. `-w` 옵션은 리포트에 결과가 있는 동안은 거부하므로, 직접 작성한 파일 내의 모든 확인 사항 (a) 위반 사항이 먼저 해결되어야 합니다(이들은 `doc-triage` 대상이기도 합니다).

교차 대상 파라미터 이름 불일치(Cross-target parameter-name divergence, SPEC-STATS.txt §2 참조)는 여기서 spec이 다루는 쌍에 대해서만 수정되었습니다. 나머지는 `spec-all`이 이를 다루므로 0에 도달하며, 이때 각 새로운 spec 함수는 모든 대상과 동시에 일치해야 합니다.

**커밋.** (1) 제너레이터 또는 작업 제품군별로 그룹화하여 이름 불일치를 조정하고, 각 커밋에 재생성된 출력물을 포함합니다. (2) 제너레이터에서 `NoFillNames` 및 `AllowNameMismatches` 설정을 중단하고 재생성된 출력물을 반영합니다. 이제 이름 채우기(name filling)가 활성화되며, 생성된 출력물에서 이름이 불일치할 경우 생성에 실패합니다. (3) `specfill -w -no-fill-doc`을 사용하여 직접 작성한 파일의 이름 없는 인자들을 채웁니다.

**완료 조건:** SPEC-STATS.txt §2의 이름 불일치(name mismatches) 및 이름 없음(unnamed) 카운트가 0이며, `NoFillNames` 또는 `AllowNameMismatches` 옵션 없이 제너레이터가 실행될 때.

### `gen-docs` — 생성된 출력물에 스펙 문서 주입
**완료:** [x] · **필요 사항:** `fill-gen` · **선호 사항:** `named-results` · **차단 사항:** `comments-yaml`, `handwritten-fill`, `template-docs` · **리스크:** `risk-silent-doc-loss`

`NoFillDoc`을 제거하여 제너레이터의 문서 주입(doc injection) 기능을 활성화하십시오. `template-docs`가 제너레이터 자체의 산문을 제거할 때까지 제너레이터는 `AllowDocRewrite`를 계속 설정합니다.

`named-results` 이후에 이를 반영하는 것을 선호합니다. 명세(spec) 문서에서 인자 이름(§1.8)을 참조하고 있으므로, 제너레이터가 해당 이름들을 채우기 전에 이를 주입하면 시그니처에서 바인딩하지 않는 이름을 언급하는 문서가 남게 됩니다.

단순한 no-op이 아니라 실제 diff가 발생할 것으로 예상됩니다: spec은 이미 수백 개의 `(receiver, name)` 쌍과 겹치며(SPEC-STATS.txt §1), 기존 문서 텍스트 중 spec과 일치하는 것은 거의 없습니다(SPEC-STATS.txt §3). 따라서 이 작업은 그만큼 많은 문서 주석을 재작성합니다. `go run . -diff`를 먼저 실행하여 변경 규모를 정확히 확인하십시오.

제너레이터의 문서가 주입되기 전에, 해당 구현 노트(implementation notes)는 반드시 §1.6을 따라야 하며, 그렇지 않으면 첫 번째 rewrite 과정에서 해당 내용이 조용히 누락됩니다. 알려진 미비점: 일부 노트에는 `CPU Features:`라고 표기되어 있거나 콜론이 누락되어 있습니다. simdgen의 성능 주의 사항("A non-constant value of shift may result in significantly worse performance" 및 `SetElem` 점프 테이블 관련 라인)에는 접두사가 없으며, `SetElem` 관련 라인은 빈 줄 없이 `Asm:` 라인 바로 위에 위치해 있습니다. `specfill`의 체크 (a) 위반 사항과 주입 설정 시 출력물의 `-diff` 결과가 작업 대상 목록입니다.

**커밋.** (1) simdgen, tmplgen, wasmgen 및 midway 템플릿의 노트 접두사 수정 — 주의 사항(caveats)에는 `Performance:`, 모든 노트 앞에는 빈 줄 추가 — 재생성된 출력 결과 포함; diff는 노트 라인만 수정해야 함. (2) simdgen에서 doc injection 활성화. (3) tmplgen, wasmgen, midway에서 활성화. 커밋 (2)와 (3)에는 재생성된 출력 결과가 포함됨; 출력 변경 사항이 연산 스펙 커버(operations spec covers)에만 해당하는지 확인하고, 변경된 모든 doc comment를 검토하여 의도치 않게 누락된 내용이 없는지 확인할 것. (4) `fill-enforce`가 이미 완료되었다면, 생성된 파일들이 문서 일치 여부를 강제하기 시작하도록 `cmd/specfill.TestFill`에서 `NoFillDoc: true`를 제거.

**완료 조건:** 생성된 출력물에 check (a) 위반 사항이 없고, 4개의 제너레이터 모두 문서를 주입했으며, 검토 없이 누락된 내용이 없어야 하며, 이전 트리와의 유일한 차이점이 operation spec cover에 대한 문서 주석뿐일 때 완료된 것으로 간주합니다.

### `fill-enforce` — 시그니처와 이름 불일치 시 에러 발생
**완료:** [x] · **필요 사항:** `named-results`

연산 사양(operations spec)이 적용되는 경우, 불일치가 발생하면 실패합니다. 누락된 사양 함수는 계속 허용됩니다. 이는 `sig-refactor`에 의존하지 **않는다**는 점에 유의하십시오. `specfill`은 simdgen의 내부 모델이 아니라 출력된 소스를 비교합니다.

생성된 출력물은 생성되는 시점에 이미 확인됩니다: `fill-gen`이 켜져 있으면 타입 불일치가 실패하고, `named-results`가 켜져 있으면 이름 불일치가 실패합니다.
이는 직접 작성한 파일이나, 생성기를 다시 실행하지 않고 수동으로 편집한 생성된 파일들을 놓치게 됩니다. 이 작업은 `cmd/specfill` 내의 `go test`를 통해 두 경우를 모두 해결하며, 생성 여부와 관계없이 `simd` 및 `archsimd` 내의 모든 비-테스트 `.go` 파일에 대해 `Fill`을 실행하고 발견되는 모든 오류에 대해 실패 처리합니다. 해당 파일들은 설계상 주입되었든 직접 작성되었든 스펙 소유의 문서를 포함하고 있으므로 `AllowDocRewrite`를 설정합니다.

**커밋.** 테스트를 추가하는 커밋 하나.

**완료 조건:** 생성되었거나 직접 작성된 exported 선언에서 의도적으로 도입한 시그니처 또는 인자 이름(argument-name) 변경 시 빌드가 실패하면 완료됩니다.

## 트랙 C — 적합성 (Conformance)

`simdref`에 대한 동작 테스트(Behavioral testing). 다른 모든 작업과 병렬로 진행되며, 명세 커버리지(spec-coverage) 병목 지점만 공유합니다.

### `ci-audit` — CI/하드웨어 감사
**완료:** [x] · **필요:** — · **차단:** `conform-fixed` · **리스크:** `risk-conformance-env`

amd64, arm64, wasm 및 SVE에 대해 실제로 테스트를 실행할 수 있는 환경(네이티브 또는 에뮬레이션)을 결정하십시오. 다른 아키텍처에 대한 적합성 테스트 스위트의 가치는 이에 달려 있습니다.

"테스트 실행"의 의미는 다음과 같습니다. 타겟에 맞게 `simd` 및 `archsimd`를 빌드하고, 실제 하드웨어 또는 에뮬레이션된 하드웨어에서 `go test`를 실행합니다. 이때 실행 속도는 수천 개의 생성된 적합성 테스트 케이스를 감당할 수 있는 수준이어야 합니다. SVE는 SVE 지원 하드웨어 또는 QEMU가 필요하며, wasm은 런타임이 필요합니다.

**완료 조건:** 대상(target)별로 오늘 실행 가능한지, 무엇으로 실행하는지, 속도는 어느 정도인지, 실행 불가능하다면 무엇이 필요한지를 기록한 문서나 이슈가 하나라도 존재해야 합니다. 각 대상을 실행 가능(runnable), 작업 후 실행 가능(runnable-with-work, 작업 내용 명시), 또는 실행 불가능(not runnable)으로 표시하여 `conform-fixed`가 어떤 대상에 대해 테스트를 작성하고 있는지 알 수 있도록 합니다.

**결과**

| amd64            | gotip-linux-amd64 | gotip-linux-amd64_avx512 |
| ---------------- | ----------------- | ------------------------ |
| AVX              | ✔                 | ✔                        |
| AVX2             | ✔                 | ✔                        |
| AVX512           | ✘                 | ✔                        |
| AVX512BITALG     | ✘                 | ✔                        |
| AVX512GFNI       | ✘                 | ✔                        |
| AVX512VAES       | ✘                 | ✔                        |
| AVX512VBMI       | ✘                 | ✔                        |
| AVX512VBMI2      | ✘                 | ✔                        |
| AVX512VNNI       | ✘                 | ✔                        |
| AVX512VPCLMULQDQ | ✘                 | ✔                        |
| AVX512VPOPCNTDQ  | ✘                 | ✔                        |
| AVXAES           | ✔                 | ✔                        |
| AVXPCLMULQDQ     | ✔                 | ✔                        |
| AVXVNNI          | ✘                 | ✔                        |
| FMA              | ✔                 | ✔                        |
| SHA              | ✘                 | ✔                        |
| VAES             | ✘                 | ✔                        |
| VPCLMULQDQ       | ✘                 | ✔                        |

amd64의 경우, 테스트를 위해 `gotip-linux-amd64_avx512` gomote를 사용하십시오.

| arm64           | gotip-linux-arm64 | qemu-aarch64 -cpu neoverse-n2 | qemu-aarch64 -cpu neoverse-v1 |
| --------------- | ----------------- | ----------------------------- | ----------------------------- |
| PMULL           | ✔                 | ✔                             | ✔                             |
| SVE             | ✘                 | ✔                             | ✔                             |
| SVE2            | ✘                 | ✔                             | ✔                             |
| SVE 벡터 크기   | n/a               | 128                           | 256                           |

`qemu-aarch64 -cpu neoverse-n1` (gotip-linux-arm64의 기능과 일치함)은 `gotip-linux-arm64`보다 약 7배 느리며, 이는 실질적인 적합성 테스트(conformance testing)가 가능한 범위 내에 있습니다.

NEON의 경우, 테스트를 위해 `gotip-linux-arm64` gomote를 사용하십시오. SVE의 경우, `qemu-aarch64 -cpu neoverse-v1`을 사용하십시오.

| wasm    | js-node | wasip1-wazero |
| ------- | ------- | ------------- |
| SIMD128 | ✔       | ✔             |

`node`가 `wazero`보다 약 3배 더 빠릅니다.

wasm의 경우, 테스트를 위해 `node`를 사용하세요.

### `conform-fixed` — 적합성 테스트 하네스, 고정 너비 타입
**완료:** [ ] · **필요:** `ci-audit` · **차단:** `validate-amd64`, `conform-scalable` · **선호:** `specfill`

`archsimd`와 `internal/simdref`를 비교하는 테스트를 생성했습니다. 제너레이터의 입력은 spec(수기로 작성된 소스)이므로, 이는 다른 제너레이터의 출력을 읽는 제너레이터가 아닙니다.

**커밋.** (1) 입력 생성: 이미 타입별 엣지 케이스 벡터, 마스크 패턴 및 윈도우 워킹 헬퍼(§1.9)가 포함되어 있는 `archsimd/internal/simd_test/helpers_test.go`에서 시작합니다. 이를 생성된 테스트가 임포트할 수 있는 패키지로 올릴지 결정합니다. (2) `(recv, name)` 명세가 커버하는 항목당 하나의 테스트를 생성하는 테스트 제너레이터를 구현합니다. (3) 명세 본문에서 패닉이 발생하는 연산을 제외하고 SIMD 테스트 스위트에 연결합니다.

**완료 조건:** 실행 가능하다고 표시된 모든 타겟 `ci-audit`에서 모든 연산 사양이 포함되어 있으며, 엣지 케이스 및 랜덤 입력을 모두 사용하여 `simdref`에 대해 테스트되었고, 실패 시 해당 연산, 입력, 그리고 두 결과값이 모두 명시되어야 합니다.

### `conform-scalable` — 적합성 하네스, 확장 가능 유형
**완료:** [ ] · **필요 항목:** `width`, `conform-fixed` · **차단 항목:** `conform-flip`

SVE의 확장 가능 타입(`Int8s` … `Float64s`, `Mask8s` … `Mask64s`)으로 `conform-fixed`의 하네스를 확장하십시오. `width`가 구체적인 너비에서 사양(spec)이 어떻게 실행되는지를 결정하기 전까지는 작성될 수 없으므로 `conform-fixed`와 분리하십시오. 하네스는 사양의 고정된 `scalableWidth`가 아니라, 하드웨어가 `vl()`을 통해 보고하는 너비로 `simdref` 값을 생성해야 합니다.

**커밋 사항.** (1) 런타임 벡터 길이에 맞춰 벡터 크기를 조정하도록 입력 생성 기능을 수정합니다. (2) 테스트 생성기를 확장 가능한 리시버(scalable receivers)까지 확장합니다. (3) `ci-audit`에 따라 SVE 가용 여부에 따라 게이트가 설정되도록 스위트에 연결합니다.

**완료 조건:** 확장 가능한 작업(scalable operations) 사양이 하드웨어의 실제 벡터 길이(vector length)에서 SVE 적합성 테스트를 통과했을 때.

### `validate-amd64` — amd64에 대해 스펙 본문 검증
**완료:** [ ] · **필수 사항:** `conform-fixed`, `spec-common`, `impl-defined` · **차단 항목:** `conform-flip`

amd64를 오라클(oracle)로 하여 적합성(conformance) 테스트를 실행하십시오. 달리 증명되기 전까지 모든 실패는 명세(spec) 버그로 간주합니다. §1.9를 참조하십시오.

**커밋.** 스펙 수정 묶음당 하나씩 생성하십시오. 각 수정 이유를 명확히 알 수 있도록 스펙 변경 사항과 하네스(harness) 변경 사항을 분리하여 유지하십시오.

**완료 조건:** amd64에서 모든 operation spec이 다루는 항목에 대해 harness가 통과하고, 남아 있는 모든 차이점이 spec에서 수정되거나 `impl-defined` 정책에 따라 구현 정의(implementation-defined)로 기록되었을 때 완료된 것으로 간주합니다.

### `conform-flip` — 적합성(conformance) 방향 반전
**완료:** [ ] · **필요 사항:** `validate-amd64`, `conform-scalable`

Spec은 이제 amd64뿐만 아니라 모든 타겟에 대한 오라클(oracle)이 됩니다. 후반부는 기여자 대상 노트로, 아마도 `internal/spec/doc.go`와 SIMD README에 포함될 것이며, 다음과 같은 워크플로우를 설명합니다: 작업(operation)이 spec에 없다면 추가하고, 이를 구현한 뒤, 적합성 테스트(conformance)를 실행하십시오.

**완료 조건:** conformance가 실행되어 runnable로 표시된 모든 `ci-audit` 타겟에서 빌드가 실패하고, 아키텍처를 추가하는 사람이 찾을 수 있도록 워크플로우가 문서화되었을 때.

## 트랙 D — 스펙 내용

spec 함수, 문서 및 본문 작성. 다른 트랙들이 의존하는 공통의 병목 지점입니다.

### `doc-explore` — 하드 패밀리에 대한 문서 메커니즘 탐색
**완료:** [x] · **필요:** — · **차단 요소:** `spec-common` · **리스크:** `risk-doc-template-ceiling`

CL 831485 기준으로, `categories.yaml`의 문서 라인 8줄 중 대략 1줄이 모양(shape) 특정 리터럴(`[x0, x1, x2, x3, ...]`, `128-bit`, `0b_11_01_00_10`)을 포함하고 있으며, 이는 `AddSub`의 `Concat*Pairs`와 `Moves`의 `concatSelectedConstant*`에 집중되어 있습니다. 해당 문서들은 하나의 템플릿에 `{vL}`을 치환하는 방식으로는 생성할 수 없으며, 각 모양마다 고유한 텍스트가 필요합니다.

예상되는 메커니즘은 여러 spec 함수가 하나의 `//specgen:name`을 공유하는 것이며, `funcKey`가 `(recv, name)`이고 제약 조건 집합(constraint sets)이 서로 중복되지 않으므로 specgen은 이를 지원합니다. **대규모 마이그레이션을 진행하기 전에 이를 검증하십시오**. 사후에 검증하는 것이 아니라 미리 해야 합니다. 쉬운 문서 150개를 작성한 후에야 확장이 불가능하다는 것을 발견한다면, 그 모든 문서에 소급 적용해야 하기 때문입니다.

**Commits.** (1) `ConcatAddPairs` / `ConcatSubPairs`를 spec으로 마이그레이션하고 문서를 포함합니다. 해당 텍스트는 16/32비트 요소와 64비트 요소 간에 차이가 있습니다. `cmd/specls`를 통해 확인하십시오. (2) `Grouped` 변형들을 마이그레이션합니다. 이들의 문서는 요소 크기*와* 128비트 그룹화에 따라 달라집니다. 이는 두 가지 축을 가진 메커니즘의 진정한 테스트가 될 것입니다. (3) `ShiftSaturated`, `ShiftAllRight`, `ShiftRight`는 부호 있는(signed) 요소와 부호 없는(unsigned) 요소 간에 문서가 다릅니다. `categories.yaml`은 `signed:` 조인 키를 통해 변형을 선택했는데, 이번 작업으로 이를 폐지합니다. (4) 만약 이 메커니즘이 불충분하다고 판단되면, 이를 확장하고(조건부 문서 텍스트 형태가 될 가능성이 높음) `internal/spec/doc.go`에 해당 확장을 문서화하십시오.

`concatSelectedConstant*`는 훨씬 더 어렵습니다. 하나의 API 이름에 네 개의 spec 함수가 대응하기 때문입니다. 하지만 이는 *unexported* 상태이므로, §1.7에 따라 `specfill`의 범위 밖에 있으며 `compiler-ops` 전까지는 결정되지 않습니다. `compiler-ops`가 적용되었고 더 엄격한 테스트를 원하는 경우에만 이를 사용하십시오.

`cmd/specls`가 세 가지 제품군 모두에 대해 기존 문서 텍스트를 재현하거나, 그렇게 할 수 있도록 문서 메커니즘이 확장되었을 때 완료됩니다.

### `spec-common` — 공통 작업 명세화
**완료:** [x] · **필요 항목:** `width`, `doc-explore` · **차단 항목:** `validate-amd64`, `comments-yaml`, `spec-all` · **선호 항목:** `specfill` · **리스크:** `risk-ref-impl-effort`

`midway/comments.yaml`의 메서드 세트는 다음을 문서화합니다: `.common_methods` 블록에서 `String`과 `Len`을 제외한 `Add`, `Sub`, `Min`, `Max`, `And`, `Or`, `MulAdd`, 비교 연산자 및 나머지 portable core. `SPEC-STATS.txt`에서는 이를 "portable core"로 추적하며, 이것이 이번 작업의 완료 기준입니다. 계획에서 가장 효율이 높은 부분입니다. 이들은 올바르게 구현하기 가장 쉬운 레퍼런스 구현체들이며, (가장 광범위한 사용자가 사용하는 패키지임에도 문서 불일치가 가장 심한) `comments-yaml` 문제를 해결할 수 있게 해주며, 새로운 아키텍처가 가장 먼저 구현해야 할 정확한 대상입니다.

파일의 키가 모두 연산(operation)인 것은 아닙니다. 메서드 문서 외에도 벡터 *타입*(types), 함수 및 템플릿을 문서화하며, 공유 블록(shared block)에 키로 지정된 리시버 이름(receiver names)을 포함합니다. 여기서는 메서드/함수만 범위(scope)에 포함되며, 이는 non-spec 잔여물(`String` 등, §1.7)을 제외합니다.

**커밋.** 나머지 작업을 확정하기 전에 `risk-ref-impl-effort`를 조정하기 위해, 먼저 무작위로 약 10개의 연산을 샘플링하여 구현에 걸리는 시간을 측정하십시오. 그 다음, 각 제품군(arithmetic, bitwise, min/max, compares, multiply-accumulate)당 하나의 커밋을 생성하며, 각 커밋에는 문서와 본문이 포함된 spec 함수를 추가하고 `cmd/specls` 출력을 확인하십시오.

**완료 조건:** `midway/comments.yaml`의 non-spec residue를 제외한 모든 *method* 이름이 실제 본문이 있는 spec 함수로 연결되어 `comments-yaml`의 블로킹이 해제되었을 때.

### `spec-all` — 일괄 spec 마이그레이션
**완료:** [ ] · **필요 사항:** `spec-common`, `convert-lo`, `mask-bits` · **선호 사항:** `specfill`, `fill-enforce` · **차단 항목:** `template-docs` · **리스크:** `risk-ref-impl-effort`

나머지 내보낸(exported) 작업들은 둘 이상의 생성자에 의해 생성된 이름(SPEC-STATS.txt §1)을 기준으로 우선순위를 정합니다. 이는 드리프트(drift) 위험이 가장 높으며, 각 마이그레이션이 한 번에 여러 파일을 수정하기 때문입니다. 가능한 범위 내에서 구현된 본문(body)이면 충분합니다. 적합성 테스트(conformance)에서 이를 건너뛰므로 `panic("not implemented")`를 사용하는 것은 안전합니다. *잘못된* 본문은 본문이 없는 것보다 더 좋지 않습니다.

두 개의 분모가 있으며, 둘 다 유용합니다. API 기준으로는 `(receiver, name)` 쌍이며, SPEC-STATS.txt §1에 표시된 uncovered 항목이 스코어보드에서 추적하는 대상입니다. 처리(retired)되는 입력 기준으로는 `categories.yaml`의 exported operation name 중 `spec-common`에서 처리하는 항목을 제외한 것입니다. 이 둘은 서로 다른 대상에 대한 서로 다른 수치입니다. 즉, `categories.yaml`의 이름 하나가 여러 개의 API 이름으로 확장될 수 있습니다. 따라서 대상 청중이 필요로 하는 수치를 인용하고, 어떤 기준인지 명시하십시오.

**왜 `convert-lo`와 `mask-bits`가 이를 제어하는가.** 실제로 이들에 의존하는 것은 Converts 및 LoadStore 제품군뿐입니다. `convert-lo`는 `ExtendLo*` / `ConvertLo*`를 이름 변경할 수 있고, `mask-bits`는 확장 가능 마스크 비트맵 쌍(scalable mask bitmap pair)을 이름 변경할 수 있는데, 문서 마이그레이션 후에 이름 변경을 수행하면 작업을 두 번 해야 하기 때문입니다. 이 작업이 시작될 때 둘 중 하나라도 아직 열려 있다면, 다른 제품군들은 영향을 받지 않으므로 그 부분부터 시작하면 됩니다.

**커밋.** `ops/*/` 그룹화와 동일하게 연산 패밀리당 하나씩 생성합니다. 연산이 가환(commutative)인 경우 각 spec 함수에 `//specgen:commutative`를 추가합니다. 이 지시어는 이미 존재하며 `specgen`에 의해 파싱됩니다. spec에서 처리하게 된 `comments.yaml` 항목들은 삭제합니다. 각 커밋에 재생성된 모든 출력물을 포함하십시오. `gen-docs`가 반영되면, 각 패밀리의 재생성 과정에서 해당 패밀리의 문서가 다시 작성되므로, diff를 검토하여 모든 문서 주석 내용이 동일한지 확인하십시오. 삭제된 텍스트가 있다면, 그것이 spec에서 설명해야 할 내용이거나 접두사가 누락된 구현 참고 사항(implementation note)이어야 합니다.

`specfill`이 §1.7에서 명시한 영구적 잔여물(`String`, `Len`)을 제외하고, 스펙에 의해 커버되지 않은 남은 API 선언이 없다고 보고할 때 **완료**된 것으로 간주합니다.

## 트랙 E — 오래된 입력 방식의 폐지

다른 문서 소스들을 중단한 다음, `categories.yaml` 자체를 중단합니다.

### `doc-triage` — 수동 문서 충돌 분류(triage)
**완료:** [ ] · **필요:** `specfill` · **선호:** `spec-common` · **차단:** `handwritten-fill` · **리스크:** `risk-silent-doc-loss`

`handwritten-fill`이 충돌 세트(conflict set)를 먼저 비움으로써, 수기로 작성된 파일들을 안전하게 다시 작성할 수 있도록 수정합니다.

충돌(conflict)이란 명세(spec)에 문서가 존재*하고* 동시에 수기로 작성된 파일에 명세 소유 단락(spec-owned paragraphs, §1.6)이 서로 다르게 작성된 선언을 의미합니다. `-w` 옵션이 덮어쓰는 곳은 오직 이런 지점들뿐입니다. 명세에 항목이 없는 경우, 해당 선언은 그대로 유지됩니다. 따라서 모든 충돌은 다음 두 가지 방법 중 하나로 해결됩니다. 하나는 산문(prose) 내용이 명세에 포함되어야 할 내용인 경우(명세로 이동), 또는 특정 타겟이 해당 연산을 어떻게 구현하는지에 관한 내용인 경우(§1.6의 접두사 중 하나를 부여하여 구현 노트(implementation note)로 변환하며, 이 경우 `specfill`은 이를 절대 수정하지 않습니다). 두 결과 모두 텍스트를 손실시키지 않으며, 이것이 이후에 `-w`를 안전하게 사용할 수 있게 하는 이유입니다.

수기로 작성된 파일들에 대해 `specfill -diff`를 실행하십시오. 다시 작성될 모든 문서 주석은 충돌(conflict)이며, 각 충돌을 앞서 언급한 두 가지 범주 중 하나로 분류하십시오.

SPEC-STATS.txt §3에는 파일별 충돌 횟수가 세분화되어 있으며, `simd_emulated.go`가 대부분을 차지하고 `archsimd/slicepart_*.go`, `shuffles_amd64.go`, `extra_amd64.go` 등이 긴 꼬리(long tail) 형태로 이어집니다. 일부 구현 텍스트에는 현재 접두사가 없습니다. 예를 들어 `extra_amd64.go`의 "This method compiles to VPTEST x, x"는 `Performance:` 노트에 해당합니다. 동일한 패스를 통해 이 파일들의 check (a) 위반 사항과 노트의 오타를 수정합니다.

`slicepart_*.go` 파일들이 가장 중요합니다: 이 파일들은 `Load*Part` 제품군을 선언합니다. 이는 `LoadZPart`를 통해 *이미* 다루고 있으므로, 처음부터 설명 문구가 서로 충돌하며 — 그 중 하나는 `LoadUint32x4Part`를 "a Int32x4"를 로드하는 것으로 설명하고 있습니다.

`specfill -no-fill-names -diff` 결과가 비어 있고, `specfill`이 check (a) 위반 사항이 0건이라고 보고하면 **완료**됩니다.

### `comments-yaml` — `midway/comments.yaml`에서 spec으로 커버되는 문서 제거
**완료:** [x] · **필요 사항:** `gen-docs`, `spec-common` · **선호 사항:** `fill-enforce`

`comments.yaml`에서 각 메서드 또는 함수 템플릿 항목이 `spec`에 포함되면 삭제됩니다. 이 작업 시점(`spec-common` 이후)에는 이식 가능한 코어 외의 비-spec 잔여물(`String` 등, §1.7)과 Load/LoadPart/Broadcast 템플릿이 이에 해당합니다. 이후 `spec-all`에서 `spec`이 획득하게 되는 항목들은 `spec`에 반영되는 시점에 삭제됩니다.

**커밋.** (1) 명세(spec)가 portable core를 다루고 있는지 확인하고, 누락된 부분을 채웁니다. (2) `comments.yaml`에서 처리된 항목들을 삭제합니다. (3) `simd/simd_emulated.go`에 대해 `specfill -w`를 실행합니다. 이 작업은 `handwritten-fill`과 겹치므로, 먼저 완료되는 순서대로 진행하십시오.

**완료 조건:** `comments.yaml`에 operation spec이 다루는 항목에 대한 엔트리가 없고, 중간 소스들이 `specfill`을 통해 해당 문서들을 가져오며, `simd_stubs.go`와 `simd_emulated.go`가 이들에 대해 spec에서 유도된 동일한 문서 내용을 포함하고 있을 때.

### `handwritten-fill` — 수기 작성 파일에 `-w` 옵션 활성화
**완료:** [ ] · **필요 사항:** `gen-docs`, `doc-triage` · **리스크:** `risk-silent-doc-loss`

`doc-triage`가 충돌 세트(conflict set)를 모두 비운 후, 수기로 작성된 파일에 대해 문서 재작성(doc rewriting) 기능을 켜십시오. 이 시점에서 `-w`는 이미 재작성될 내용과 일치하는 문서만 다시 작성합니다.

두 개의 가드(guard)가 있으며, 둘 다 `cmd/specfill`에만 적용됩니다. 이는 모든 제너레이터가 사용하는 `gentools`의 공유 `-w` 플래그를 변경하지 **않습니다**:

- `specfill -w`는 리포트에 발견 사항(findings)이 있거나 커밋되지 않은 변경 사항이 있는 경우 실행을 거부하므로, 해당 diff가 수행한 작업의 전체 내용을 나타냅니다.
- `specfill -w`는 CI에서 실행되지 않습니다. CI에서는 리포트 모드(`fill-enforce`)가 실행됩니다.

**완료 조건:** 깨끗한 트리(clean tree) 상태에서 수동으로 작성한 파일들에 대해 `specfill -w`를 실행했을 때 아무런 변경 사항이 없어야 합니다(no-op).

### `template-docs` — 제너레이터 제공 API 문서 폐기
**완료:** [ ] · **필요 사항:** `gen-docs`, `spec-all` · **차단 항목:** `cat-rehome`

wasmgen 및 tmplgen 템플릿에 내장된 doc string과 내보낸 `categories.yaml` 항목의 `documentation:` 필드를 삭제하여, `specfill`이 이를 제공하도록 합니다. `spec-all`이 해당 제너레이터들이 생성하는 연산들을 모두 커버하면 기계적으로 수행할 수 있는 작업이지만, 템플릿의 산문(prose)이 제너레이터에 남아있어야 할 구현 노트(implementation notes)와 섞여 있기 때문에 자동화할 수는 없습니다 (§1.6).

**커밋.** 제너레이터당 하나씩, 산문(prose)은 제거하고 노트는 유지합니다. 내보낸 `categories.yaml` 항목의 `documentation:` 필드에 대해 하나를 생성합니다. 각 커밋에는 재생성된 출력물이 포함됩니다. 그 후 제너레이터에서 `AllowDocRewrite` 설정을 중단하여, API 산문을 출력하는 제너레이터가 다시 생성에 실패하도록 합니다.

**완료 조건:** 생성기의 소스에 API 설명문(prose)이 포함되어 있지 않고, export된 `categories.yaml` 항목에 `documentation:`이 없으며, 재생성 결과가 이전 트리와 바이트 단위로 동일하고, 생성기가 `AllowDocRewrite` 없이 실행될 때 완료된 것으로 간주합니다.

### `cat-rehome` — `categories.yaml` 비-문서(non-doc) 필드 재배치
**완료:** [ ] · **필요 사항:** `template-docs` · **차단 항목:** `compiler-ops-impl`, `sig-from-spec` · **리스크:** `risk-cat-unknowns`

`categories.yaml`의 내보낸 엔트리(exported entries)에서 `go:`와 `commutative:`를 제외한 모든 내용을 비우고, 나머지 각 필드를 §1.3의 인벤토리에 명시된 해당 위치로 전송하십시오. `template-docs`에서 이미 `documentation:`은 제거했으며, 이것이 나머지 작업입니다. `compiler-ops-impl`을 위한 컴파일러 전용 엔트리들은 수정하지 않고 그대로 둡니다.

예상치 못한 결과가 있을 수 있습니다. §1.3의 감사는 정적이었으며, 필드 조합에 대한 unifier의 동작이 철저하게 추적되지 않았습니다 — `regexpTag`의 역할은 여전히 검증되지 않은 상태입니다 (§1.3). 완화 요인: `go run . -diff`를 통해 모든 단계를 체크인된 생성 출력물과 바이트 단위로 대조하여 검증할 수 있습니다.

**커밋.** §1.3의 disposition 열을 따라 커밋당 하나의 필드를 처리하며, 각 단계에서 생성된 출력 결과가 변경되지 않았음을 확인하십시오: (1) `categories.yaml` 및 `go_*.yaml`에서 `regexpTag`와 `signed`를 삭제합니다. 대부분의 `go_*.yaml` 사용 사례는 이미 비활성 상태일 것으로 예상됩니다. (2) `constImm`을 `go_amd64.yaml`로 이동합니다. (3) `out`/`elemBits`/`bits` 항목을 spec 함수 분할로 변환합니다. 이는 `spec-all`에서 이미 처리되었어야 하므로 이를 확인하십시오.

`categories.yaml`의 모든 내보내기(exported) 항목이 `go:` 및 `commutative:` 키만 가지고 있고, `compiler-ops-impl`을 위한 컴파일러 전용 항목들은 변경되지 않았을 때 **완료**됩니다. 생성된 출력물은 전체적으로 바이트 단위까지 동일해야 합니다.

### `compiler-ops-impl` — 컴파일러 전용 op 표현 구현
**완료:** [ ] · **필요 사항:** `compiler-ops`, `cat-rehome` · **차단 항목:** `sig-from-spec`

내보내기 선언(exported declaration)을 생성하지 않는 컴파일러 전용 항목들과 `noTypes` / `noGenericOps` 스위치에 대해 `compiler-ops`가 결정한 사항을 구현하십시오. 이 시점에서는 남은 설계 작업이 없어야 합니다. 만약 남아 있다면, `compiler-ops` 작업이 완료되지 않은 것입니다.

이 작업들은 API 표면(surface)을 가지지 않습니다. 즉, SSA 연산 및 로워링(lowering) 규칙으로만 존재하므로, 여기서 `specfill`, spec 또는 공개 패키지를 건드리는 부분은 없습니다. 이는 전적으로 `simdgen`이 `categories.yaml` 외의 다른 곳에서 해당 내용을 읽어올 수 있도록 하기 위한 것입니다.

`categories.yaml`에 컴파일러 전용 항목이 더 이상 남아 있지 않고 (SPEC-STATS.txt §4), 생성된 출력 결과가 바이트 단위로 동일할 때 **완료**됩니다.

### `cat-delete` — `categories.yaml` 삭제
**완료:** [ ] · **필요 사항:** `sig-from-spec`

`ops/*/categories.yaml`, 이를 로드하는 `!import` 스텁, 그리고 `simdgen/main.go` 내의 관련 처리 로직을 삭제합니다. 이 시점에는 해당 파일이 가지고 있던 모든 필드가 재배치되었고(`cat-rehome`), 컴파일러 전용 항목들은 이동했으며(`compiler-ops-impl`), 시그니처는 스펙에서 가져오므로(`sig-from-spec`), 이는 순수하게 삭제 작업만 수행하면 됩니다.

`categories.yaml` 파일이 더 이상 존재하지 않고, 해당 파일 없이도 simdgen이 실행되며, 생성된 출력 결과가 바이트 단위로 동일할 때 완료됩니다.

## 트랙 F — simdgen 내부 구조

시그니처 리팩터링과, 궁극적으로 spec에서 시그니처를 소싱하는 작업.

### `sig-refactor` — simdgen signature refactor
**완료:** [ ] · **필요:** — · **차단:** `sig-from-spec` · **리스크:** `risk-sig-refactor-convergence`

`Operation`의 시그니처를 `shape()` → `classifyOp()` → 템플릿 이름으로 이어지는 파생 속성이 아니라, `Operation`의 일급 값(first-class value)으로 만드세요. 이상적으로는 `specgen.Func`의 `Recv`/`In`/`Out`과 직접 비교 가능한 형태로 구성해야 합니다.

이렇게 하면 스텁 템플릿(§1.1에서 이를 계산함)이 대략 3개로 축소됩니다. 그 이유는 피연산자 순열(operand permutation)과 매개변수 명명(parameter naming)이 템플릿의 정체성이 아닌 데이터가 되기 때문입니다. `_21`, `_231Type1`, `_31`과 같은 접미사는 명시적인 순열이 됩니다.

또한 이는 통합 접근 방식을 유지할 수 있는지에 대한 실증적인 테스트이기도 합니다.
이번 리팩터링은 서명(signature)이 새로운 특수 사례들을 무더기로 만들지 않고 데이터로 표현 가능하다고 가정합니다. §1.1에 기록된 쿼크(quirk) 필드들과 `simdgen only supports…` 패닉들은 대부분 서명의 *업스트림*(XED 불일치)이거나 *다운스트림*(레지스터 형상, 규칙)에 위치하므로, 접점(seam)이 얇아 보입니다. 하지만 이는 사전 가정일 뿐 측정 결과가 아닙니다. 만약 수렴하지 않는다면, 그것이 §1.1을 재검토해야 한다는 증거가 될 것이며, 이는 §1.1의 레이어 테이블이 격리하고 있는 수백 줄의 코드만으로 저렴하게 얻은 결론이 될 것입니다.

**커밋 사항.** (1) 가장 단순한 클래스들(`op1`, `op2`, `op3`)을 다루는 시그니처 타입과 `GoSignature()` 메서드를 도입합니다. (2) 처리가 까다로울 수 있는 즉시값 변형(`op*Imm*`)으로 확장합니다. (3) 순열 및 `VecAsScalar` 변형으로 확장합니다. (4) 시그니처 값을 사용하도록 스텁 템플릿을 다시 작성하고, 중복된 템플릿을 삭제합니다.

`go run . -diff` 실행 시 모든 커밋에서 바이트 단위로 동일한 출력이 나타나면 **완료**된 것으로 간주합니다.

### `sig-from-spec` — 명세(spec)로부터 simdgen 시그니처 생성
**완료:** [ ] · **필요 사항:** `sig-refactor`, `cat-rehome`, `compiler-ops-impl` · **차단 항목:** `cat-delete`

simdgen은 `(recv, name)`으로 spec 함수를 조회하고 시그니처(signature)의 일치 여부를 확인하며, 불일치 시 구조화된 diff를 보고합니다. **조회 키는 spec 자체의 고유 키인 `(recv, name)`으로만 설정**하고, 시그니처는 별도로 확인하십시오. 시그니처를 조회 키에 포함하면, 시그니처의 변경(divergence)을 "아직 마이그레이션되지 않음"과 구별할 수 없게 되며, 이는 이번 작업이 포착하고자 하는 바로 그 실패 사례입니다.

이 부분에서 `sig-refactor`의 효과가 나타납니다. 조회가 렌더링된 템플릿이 아니라, refactor가 도입한 시그니처 값과 비교되기 때문입니다.

**커밋 내역.** (1) spec 함수를 찾아 일치 여부를 확인하고, 불일치 시 제너레이터 실행을 실패 처리합니다. (2) `go_GOARCH.yaml`에서 더 이상 필요하지 않은 시그니처 정보를 삭제합니다. (3) simdgen이 spec의 `//specgen:commutative` 지시어에서 교환 법칙(commutativity) 정보를 읽도록 변경하고, 내보낸 `categories.yaml` 항목에서 `commutative:`를 삭제합니다.

**완료 조건:** `simdgen`이 출력하는 모든 내보내기(exported) 시그니처가 spec에서 유도되고, 교환 법칙(commutativity)이 spec에서 기인하며, 생성된 출력물이 바이트 단위로 동일할 때.

제공해주신 내용이 없습니다. 번역할 영어 마크다운 콘텐츠를 입력해 주세요. 그러면 요청하신 지침에 따라 정확하게 한국어로 번역해 드리겠습니다.

# 파트 4 — 리스크 및 불확실성 (Risks and unknowns)

모든 리스크는 태스크(task)가 소유하며, 그 구체적인 내용은 해당 태스크에 명시됩니다. 이것이 인덱스입니다. `risk-concrete-width`, `risk-impl-defined-behavior` 및 `risk-ref-impl-effort`는 비용이 많이 드는 항목들입니다. 각 항목이 모든 사양서 본문(spec body)에 영향을 미치므로, 본문을 작성한 후보다는 작성 전에 해결하는 것이 훨씬 더 경제적입니다.

| | 리스크 | 내용 | 담당자 |
|---|---|---|---|
| **[ ]** | `risk-spec-defects` | 알려진 스펙 결함 | `convert-lo`, `mask-bits` |
| **[x]** | `risk-concrete-width` | 구체적인 너비(concrete width)에서 스펙 실행 | `width` |
| **[ ]** | `risk-impl-defined-behavior` | 구현 정의 동작 (Implementation-defined behavior) | `impl-defined` |
| **[x]** | `risk-doc-template-ceiling` | 문서 템플릿 한계 — 폴백(fallback)은 지금까지 작성된 모든 문서에 영향을 주는 메커니즘 변경임 | `doc-explore` |
| **[ ]** | `risk-ref-impl-effort` | 참조 구현 노력 — 마이그레이션된 모든 연산은 정합성 테스트의 기준이 되므로 *정확한* 본문이 필요함; 난이도 분포는 미지수임 | `spec-common`, `spec-all` |
| **[x]** | `risk-conformance-env` | 정합성 실행 환경 — CI에서 arm64/SVE/wasm을 실행할 수 있는가, 그리고 비용은 얼마인가? | `ci-audit` |
| **[ ]** | `risk-sig-refactor-convergence` | `sig-refactor`가 수렴하지 않을 가능성 — 수렴하지 않을 경우 §1.1을 재검토해야 함 | `sig-refactor` |
| **[ ]** | `risk-silent-doc-loss` | 암묵적인 문서 손실 — §1.6에 따라 노트 접두사가 없는 텍스트는 스펙 소유이며, 접두사를 붙이지 않은 구현 텍스트는 첫 번째 재작성 시 삭제됨; 방지책은 모든 재작성본의 `-diff`를 검토하는 것이며, 제너레이터가 자체 산문(prose)을 생성하지 않게 되면 `AllowDocRewrite`를 사용함 | `gen-docs`, `doc-triage`, `handwritten-fill` |
| **[ ]** | `risk-cat-unknowns` | `categories.yaml` 내의 미지의 미지수(unknown unknowns) — 필드 감사는 정적으로 수행됨 | `cat-rehome` |

번역할 내용을 제공해 주세요. 제공해주시는 즉시 요청하신 지침에 따라 기술 번역을 시작하겠습니다.

# 부록 A — 생성된 두 파일 재생성하기

## `SPEC-STATS.txt`

`cmd/specstats`는 전이 스코어보드인 [SPEC-STATS.txt](SPEC-STATS.txt)를 생성합니다:

```sh
cd $GOROOT/src/simd/archsimd/_gen
go run . -w                   # (필요한 경우) 제너레이터 출력물이 최신 상태인지 확인합니다.
go run ./cmd/specstats        # 리포트를 출력합니다.
go run ./cmd/specstats -diff  # 변경 사항을 확인합니다.
go run ./cmd/specstats -w     # SPEC-STATS.txt 파일을 덮어씁니다.
```

각 빌드 구성에 대해 `go/packages`를 통해 `simd`와 `archsimd`를 로드하며, §1.4에 따라 타입 체크 없이 구문(syntax)만 가져오고 `specgen.Load`를 통해 `simd/internal/spec`을 읽습니다. 최신 Go 툴체인과 SIMD 제너레이터의 최신 출력물이 필요하지만, 자체적으로 ISA 데이터가 필요하지는 않습니다. 숫자가 변경된 수정 사항과 함께 재생성된 파일을 커밋하십시오. diff가 변경된 내역에 대한 기록이 됩니다.

이 보고서는 전환이 얼마나 진행되었는지를 측정하는 수치만을 기록합니다. 모든 수치는 100%를 향하는 분수이거나 0을 향하는 카운트이며, 이를 움직이는 작업들이 태그로 지정되어 있습니다. 들여쓰기가 되어 있고 태그가 없는 숫자는 바로 위의 수치를 세분화하는 컨텍스트입니다. 수치를 추가하시려면 분모와 방향을 지정하시거나, 그렇지 않으면 제외하시기 바랍니다.

의도적으로 수행하지 않는 한 가지가 있습니다. 바로 발산(divergence, §5)을 분류하지만, 아무것도 놓치지 않는다는 점입니다. 강제 집행(enforcement)은 `specfill`의 역할입니다. 두 개의 구현체가 서로 어긋나게 두기보다는 `specfill`이 이 프로그램의 비교 부분을 흡수해야 합니다.

보고서가 답변하지 못하는 일회성 질문의 경우, `cmd/specls`는 현재 확장되는 API 스펙을 출력합니다:

```sh
go run ./cmd/specls              # 전체 확장
go run ./cmd/specls -f Add       # 하나의 spec 함수
go run ./cmd/specls -f Add -trace  # 왜 그렇게 확장되는지에 대한 추적
```

## `SPEC-TASKS.dot`

태스크 그래프는 `cmd/spectasks`에 의해 파트 2의 두 테이블로부터 그려집니다:

```sh
go run ./cmd/spectasks        # 그래프 출력
go run ./cmd/spectasks -w     # SPEC-TASKS.dot 파일을 제자리에서 다시 작성
dot -Tsvg SPEC-TASKS.dot -o /tmp/tasks.svg  # SVG로 렌더링
go run ./cmd/spectasks | grep -v ^-- | xdot -  # 현재 그래프 보기
```

이 프로그램은 이 파일 외에는 아무것도 읽지 않습니다. 그리기 외에 수행하는 두 가지 작업은 다음과 같습니다.

이 과정은 `go test ./cmd/spectasks`를 통해 **검증**됩니다. 의존성은 여기서 세 번 명시됩니다. 파트 2의 표, 파트 3의 `Needs:`/`Prefers:` 라인, 그리고 파트 4의 `Blocks:` 라인(동일한 엣지를 역방향으로 표시)이 그것입니다. 만약 이 세 곳의 내용이 일치하지 않거나, 표가 위상 정렬(topologically sorted)되어 있지 않거나, 태스크가 어떤 트랙에도 속하지 않거나 혹은 두 개 이상의 트랙에 속해 있는 경우, 또는 엣지가 존재하지 않는 태스크를 가리키는 경우 테스트는 실패합니다. 두 번째 테스트는 SPEC-TASKS.dot 파일이 더 이상 문서와 일치하지 않을 때 실패하므로, 재생성 단계를 건너뛴 수정 사항 또한 감지됩니다. 명령어 자체는 일관되지 않은 문서로부터 그래프를 작성하는 것을 거부하지만, 문제는 테스트 단계에서 보고됩니다.

이것은 임의의 경로를 다시 진술하는 것이 아니라 **임계 경로(critical path)를 도출**합니다. 특정 태스크의 가장 긴 진입 체인(longest chain in)과 가장 긴 진출 체인(longest chain out)의 합이 전체 그래프의 길이에 도달할 때, 해당 태스크는 임계 경로 위에 있는 것으로 간주됩니다. 이를 통해 수동으로 선택한 경로 하나가 아니라 모든 가장 긴 체인을 유지하므로, 깊이가 동일한 병렬 루트들이 모두 표시됩니다.
