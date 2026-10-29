# 트레이스 실험 (Trace experiments)

실행 트레이스(Execution traces)를 사용하면 트레이스 실험(trace experiments)을 통해 새로운 이벤트를 실험적으로 시도해 볼 수 있습니다.
이 문서는 사용자 정의 트레이스 실험을 정의하는 방법을 설명하는 가이드입니다.

단순히 디버깅을 하거나 가벼운 인스트루멘테이션(instrumentation)을 수행하려는 것이라면, 트레이스 실험(trace experiment)은 과한 설정일 수 있습니다.
대신 `runtime/trace.Log`를 사용하세요.
빈도가 낮은 이벤트에 대한 개념 증명(proof-of-concept)을 만들려는 경우라도, 적용만 가능하다면 `runtime/trace.Log`를 사용하는 것이 전반적으로 더 쉬울 것입니다.

다음과 같은 경우에 트레이스 실험(trace experiment)을 고려하십시오:
- 새로운 트레이스 이벤트의 양이 상대적으로 많아, 더 컴팩트한 표현 방식(데이터 중복 제거를 위한 새 테이블 생성, varint 표현 활용 등)을 통해 이득을 얻을 수 있는 경우.
- 이벤트를 생성하려는 컨텍스트(예: 타이머 관련 이벤트)에서 `runtime/trace.Log`(또는 그에 해당하는 런타임 함수)를 호출하는 것이 안전하지 않은 경우.

## 새로운 실험 정의하기

새로운 실험을 정의하려면, `internal/trace/tracev2`를 수정하여 새로운 `Experiment` enum 값을 정의하십시오.

실험은 두 가지 부분으로 구성됩니다: timed events와 experimental batches입니다.
Timed events는 다른 모든 이벤트와 동일하며 같은 형식을 따릅니다.
이들은 순서를 정하기 쉽고 활용하는 데 더 적은 작업이 필요합니다.
Experimental batches는 기본적으로 전체 trace 생성에 대응하는 바이트 뭉치(bags of bytes)입니다.
그 안에 무엇이 포함되고 어떻게 해석될지는 전적으로 사용자에게 달려 있지만, 주로 다른 이벤트들이 참조할 수 있는 테이블 용도로 유용하게 사용됩니다.
예를 들어, AllocFree 실험은 할당 이벤트(allocation events)가 참조할 수 있는 타입 정보를 저장하는 데 이를 사용합니다.

### 새로운 이벤트 정의하기

1. 새로운 실험적 이벤트 유형을 정의하십시오 (관례적으로 실험적 이벤트 유형은 ID 127부터 시작하므로, 해당 지점부터 이벤트를 정의하는 `const` 블록을 찾으십시오).
2. `specs`에 새로운 이벤트를 설명하십시오.
   `Spec` 문서를 참조하여 새로운 스펙을 작성하고, `internal/trace/tracev2` 패키지의 테스트를 실행하여 작업 내용을 확인하십시오.
   이벤트 인수가 특정 방식으로 해석되기를 원하는 경우, `src/internal/trace/tracev2/spec.go`의 명명 규칙을 따르십시오.
   예를 들어, 문자열 인수를 출력하려는 경우 인수 이름에 `string` 접미사가 붙어 있는지 확인하십시오.
3. `src/internal/trace/order.go`의 `orderingDispatch` 테이블에 해당 이벤트의 핸들러를 목록화하여, 새로운 이벤트에 대한 순서 지정 및 검증 로직을 추가하십시오.
   이벤트가 항상 일반 사용자 고루틴 컨텍스트에서 출력된다면, 핸들러는 단순하게 스케줄링 컨텍스트가 `userGoReqs`와 일치하는지만 검증하면 됩니다.
   더 복잡한 경우, 더 다양한 실행 환경의 이벤트를 처리하는 조금 더 복잡한 예제인 `(*ordering).advanceAllocFree`를 참조하십시오.
   부분 순서(partial ordering)를 인코딩해야 하는 경우, 스케줄러 이벤트(`Go`로 시작하는 이름)를 살펴보거나 도움을 요청하십시오.
4. `src/internal/trace/event.go`의 `tracev2Type2Kind` 테이블에 새로운 이벤트를 추가하십시오.

## 데이터 방출(Emitting data)

### 새로운 이벤트 발행하기

1. 이벤트를 출력하기 위해 `runtime.traceEventWriter`에 헬퍼 메서드를 정의하십시오.
2. 이러한 헬퍼 메서드 호출을 통해 런타임에 인스트루멘테이션(instrumentation)을 수행하십시오.
   이벤트가 나타내는 작업 전후로 `traceAcquire`와 `traceRelease`를 반드시 호출하십시오. 그렇지 않으면 해당 작업의 완료와 함께 이벤트가 원자적으로 출력되지 않아, 추적 결과가 오해의 소지가 있을 수 있습니다.

### 실험적 배치 방출 (Emitting experimental batches)

실험적 배치(experimental batches)를 출력하려면, `runtime.unsafeTraceExpWriter`를 사용하여 해당 실험과 관련된 실험적 배치를 기록하십시오.
주의 사항을 준수하고, 배치를 기록하는 동안 트레이스 생성(trace generation)이 진행되지 않도록 하십시오.
각 실험은 오직 하나의 구별 가능한 배치 세트만 가질 수 있다는 점에 유의하십시오.

## 실험 데이터 복구하기

### 트레이스에서 실험 이벤트 복구하기

실험적 이벤트(Experimental events)는 이벤트 스트림에 `EventExperimental` `Kind`를 가진 이벤트로 나타납니다.

트레이스에 삽입된 원시 데이터(raw data)를 수집하려면 `Experimental` 메서드를 사용하십시오.

이후 단계에서 이 이벤트를 어떻게 해석할지는 기본적으로 사용자에게 달려 있습니다.
원하신다면 더 깔끔한 인터페이스를 제공하기 위해 얇은 래퍼(thin wrapper) API를 작성하는 것을 권장합니다.

### 실험 배치 복구하기

`Sync` 이벤트가 발생할 때마다 모든 실험적 배치(experimental batches)를 파싱하십시오.
이러한 실험적 배치들은 다음 `Sync` 이벤트가 발생하기 전까지의 모든 실험적 이벤트들과 동일한 세대에 속합니다.
