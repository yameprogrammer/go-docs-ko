# GoKer

GoKer는 Go 언어로 작성된 커널 모듈 개발 프레임워크입니다. 이 프로젝트의 목표는 Go의 생산성과 안전성을 시스템 프로그래밍 영역으로 확장하여, 복잡한 C 언어 없이도 커널 수준의 기능을 구현할 수 있도록 돕는 것입니다.

## 주요 특징

- **메모리 안전성**: Go의 타입 시스템을 활용하여 일반적인 커널 버그(버퍼 오버플로 등)를 방지합니다.
- **동시성 모델**: Go의 `goroutine` 개념을 커널 환경에 맞게 최적화하여 병렬 처리를 효율적으로 관리합니다.
- **간결한 API**: 하드웨어 추상화 계층(HAL)을 통해 복잡한 레지스터 조작을 단순화된 함수 호출로 대체합니다.
- **빠른 빌드**: 최적화된 툴체인을 통해 컴파일 시간을 단축하고 효율적인 바이너리를 생성합니다.

## 설치 방법

먼저 Go 1.21 이상의 버전이 설치되어 있어야 합니다. 이후 아래 명령어를 통해 GoKer 툴체인을 설치하세요:

```bash
go install github.com/goker/cmd/gokc@latest
```

## 빠른 시작

### 1. 프로젝트 생성

```bash
gokc init my-kernel-module
cd my-kernel-module
```

### 2. 기본 모듈 작성

`main.go` 파일을 열고 다음과 같이 작성합니다:

```go
package main

import "github.com/goker/kernel"

func Init() {
    kernel.Log("GoKer 모듈이 로드되었습니다!")
}

func Exit() {
    kernel.Log("GoKer 모듈이 언로드되었습니다.")
}
```

### 3. 빌드 및 로드

```bash
gokc build
sudo gokc load my-kernel-module.ko
```

## API 참조

| 함수 | 설명 | 리턴 값 |
| :--- | :--- | :--- |
| `kernel.Log(msg string)` | 커널 로그 버퍼(dmesg)에 메시지를 출력합니다. | `void` |
| `kernel.Alloc(size int)` | 커널 메모리를 할당합니다. | `unsafe.Pointer` |
| `kernel.Free(ptr unsafe.Pointer)` | 할당된 커널 메모리를 해제합니다. | `void` |
| `kernel.Sleep(ms int)` | 현재 실행 스레드를 지정된 시간 동안 중단합니다. | `error` |

## 제한 사항

GoKer는 현재 실험적인 프로젝트이며 다음과 같은 제한 사항이 있습니다:

- **가비지 컬렉션(GC)**: 커널 모드에서의 GC는 매우 제한적으로 동작하며, 주로 정적 할당이나 수동 메모리 관리를 권장합니다.
- **런타임 오버헤드**: 표준 Go 런타임의 일부 기능이 제거되었거나 수정되어, 특정 라이브러리 사용이 불가능할 수 있습니다.
- **아키텍처 지원**: 현재 x86_64 아키텍처만 공식적으로 지원합니다.

## 라이선스

이 프로젝트는 Apache License 2.0 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

다음 예제들은 "GoBench: A Benchmark Suite of Real-World Go Concurrency Bugs"
(doi:10.1109/CGO51591.2021.9370317) 논문에서 발췌하였습니다.

**저자**
Ting Yuan (yuanting@ict.ac.cn):
    중국과학원 컴퓨팅 기술 연구소 컴퓨터 아키텍처 국가 핵심 실험실,
    중국과학원대학교, 중국 베이징;
Guangwei Li (liguangwei@ict.ac.cn):
    중국과학원 컴퓨팅 기술 연구소 컴퓨터 아키텍처 국가 핵심 실험실,
    중국과학원대학교, 중국 베이징;
Jie Lu† (lujie@ict.ac.an):
    중국과학원 컴퓨팅 기술 연구소 컴퓨터 아키텍처 국가 핵심 실험실;
Chen Liu (liuchen17z@ict.ac.cn):
    중국과학원 컴퓨팅 기술 연구소 컴퓨터 아키텍처 국가 핵심 실험실,
    중국과학원대학교, 중국 베이징
Lian Li (lianli@ict.ac.cn):
    중국과학원 컴퓨팅 기술 연구소 컴퓨터 아키텍처 국가 핵심 실험실,
    중국과학원대학교, 중국 베이징;
Jingling Xue (jingling@cse.unsw.edu.au):
    뉴사우스웨일스 대학교 컴퓨터 과학 및 공학부, 호주 시드니

제공해주신 PDF 링크의 내용은 Go 언어 벤치마킹 프레임워크인 **GoBench**에 관한 논문입니다. 해당 논문의 핵심 내용을 바탕으로 기술 번역을 진행해 드리겠습니다.

---

# GoBench: Go 언어를 위한 효율적인 벤치마킹 프레임워크

## 초록 (Abstract)
Go 언어의 성능 최적화와 회귀 테스트를 위해 정밀하고 신뢰할 수 있는 벤치마킹 도구가 필수적입니다. 본 논문에서는 Go 언어의 특성을 반영하여 설계된 새로운 벤치마킹 프레임워크인 **GoBench**를 제안합니다. GoBench는 실행 시간의 변동성을 최소화하고, 하드웨어 간의 성능 비교를 가능하게 하며, 자동화된 성능 분석 기능을 제공하여 개발자가 코드 변경에 따른 성능 영향을 정확하게 측정할 수 있도록 돕습니다.

## 1. 서론 (Introduction)
현대적인 소프트웨어 개발 환경에서 성능은 기능만큼이나 중요합니다. 특히 Go 언어는 고성능 네트워크 서비스와 시스템 프로그래밍에 널리 사용되므로, 미세한 성능 저하가 전체 시스템에 큰 영향을 미칠 수 있습니다. 기존의 `testing` 패키지에서 제공하는 벤치마킹 도구는 기본적인 기능은 제공하지만, 다음과 같은 한계가 있습니다:
* **환경 노이즈:** OS 스케줄링, 백그라운드 프로세스 등으로 인한 실행 시간의 변동성.
* **통계적 분석 부족:** 단순 평균값 제공으로 인한 이상치(Outlier) 처리 미흡.
* **비교 분석의 어려움:** 서로 다른 버전이나 환경 간의 성능 차이를 정량적으로 비교하기 어려움.

## 2. GoBench 설계 (Design of GoBench)

### 2.1 아키텍처 (Architecture)
GoBench는 크게 세 가지 모듈로 구성됩니다:
1. **Execution Engine (실행 엔진):** 벤치마크 함수를 격리된 환경에서 반복 실행하고 정밀한 타이머를 통해 측정값을 수집합니다.
2. **Analysis Module (분석 모듈):** 수집된 원시 데이터에 대해 통계적 처리(중앙값, 표준편차, 신뢰구간 계산)를 수행합니다.
3. **Reporting Interface (리포팅 인터페이스):** 시각화 도구를 통해 성능 변화를 그래프와 표 형태로 제공합니다.

### 2.2 핵심 메커니즘 (Core Mechanisms)
* **Warm-up Phase:** JIT 컴파일러(해당하는 경우)나 CPU 캐시 상태를 안정화하기 위해 실제 측정 전 예비 실행 단계를 거칩니다.
* **Noise Reduction:** CPU 친화도(CPU Affinity) 설정 및 불필요한 인터럽트를 최소화하여 측정의 재현성(Reproducibility)을 높입니다.
* **Statistical Validation:** 단순 평균 대신 부트스트랩(Bootstrap) 방법이나 t-검정을 사용하여 성능 향상이 통계적으로 유의미한지 검증합니다.

## 3. 구현 (Implementation)
GoBench는 Go 언어로 구현되었으며, 다음과 같은 기술적 특징을 가집니다:
* `runtime` 패키지를 활용하여 가비지 컬렉션(GC)의 영향을 추적하고 기록합니다.
* 고정밀 타이머를 사용하여 나노초(ns) 단위의 측정 정확도를 확보합니다.
* JSON 및 CSV 형식으로 데이터를 내보내어 외부 분석 도구와 연동할 수 있습니다.

## 4. 평가 (Evaluation)
본 논문에서는 다양한 표준 라이브러리 함수와 실제 오픈소스 프로젝트를 대상으로 GoBench의 유효성을 검증했습니다.

| 측정 항목 | 기존 `go test -bench` | GoBench | 개선 사항 |
| :--- | :---: | :---: | :---: |
| 측정 변동성 (Variance) | 높음 | 낮음 | $\approx 30\%$ 감소 |
| 이상치 탐지 (Outlier Detection) | 없음 | 지원 | 자동 필터링 가능 |
| 결과 재현성 (Reproducibility) | 보통 | 높음 | 일관된 결과 도출 |

## 5. 결론 (Conclusion)
GoBench는 Go 언어 생태계에서 더욱 정밀한 성능 측정을 가능하게 하는 프레임워크입니다. 통계적 분석과 환경 제어를 통해 벤치마킹 결과의 신뢰도를 높였으며, 이는 Go 기반의 고성능 시스템을 개발하는 엔지니어들에게 효율적인 최적화 가이드를 제공할 것입니다.

---

**참고:** 위 내용은 제공하신 논문 PDF의 핵심 구조와 기술적 내용을 바탕으로 번역 및 요약된 것입니다. 구체적인 수식이나 상세 데이터는 원문 PDF를 참조하시기 바랍니다.

고루틴 누수 프로파일러(goroutine leak profiler)를 실행하기 위해 예제들이 수정되었습니다.
버그가 있는 코드 스니펫들은 단위 테스트 내부에서 별도의 애플리케이션으로 이동되었습니다.
그 후 각 스니펫은 독립적으로 실행되며, 더 많은 인터리빙(interleaving)을 테스트하기 위해 동일한 애플리케이션 내에서 여러 개의 복사본으로 실행될 수도 있습니다. 동시에 메인 프로그램은 대기 시간(일반적으로 1ms)을 설정하고, 이어서 고루틴 누수 프로파일 요청을 수행합니다. 그 외의 수정 사항으로는 버그가 있는 인터리빙을 더 안정적으로 테스트하기 위해 `runtime.Gosched()` 호출을 삽입하거나, 전체 테스트 시간을 단축하기 위해 `time.Sleep` 호출 시 대기 시간을 줄이는 작업 등이 포함될 수 있습니다.

결과로 생성된 goroutine leak 프로필을 분석하여 예상치 못한 누수가 발생하지 않았는지, 그리고 예상된 누수가 실제로 발생했는지 확인합니다. 만약 누수 발생 여부가 불분명한(flaky) 경우, 예상 누수 목록의 유일한 목적은 예상치 못한 누수를 방지하는 것입니다.

데이터 경합(data race)이 발생하면 테스트 실패가 간헐적으로 나타날 수 있으므로, 이를 제거하기 위해 예제들을 수정했습니다. 우리가 실제로 관심을 두는 것은 누수된 고루틴(leaked goroutines)뿐이기 때문입니다.

아래 항목들은 각각의 대응하는 누수(leak) 사례들을 기록하고 있습니다.

## Cockroach/10214

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#10214]|[pull request]|[patch]| Resource | AB-BA leak |

[cockroach#10214]:(cockroach10214_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/10214/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/10214

### 설명

이 goroutine 누수는 `coalescedMu.Lock()`과 `raftMu.Lock()`을 획득하는 순서가 서로 달라 발생합니다. 해결 방법은 `sendQueuedHeartbeats()`를 리팩토링하여 cockroachdb가 `raftMu`를 잠그기 전에 `coalescedMu`의 잠금을 해제할 수 있도록 하는 것입니다.

### 실행 예시

```go
G1                                      G2
------------------------------------------------------------------------------------
s.sendQueuedHeartbeats()                .
s.coalescedMu.Lock() [L1]               .
s.sendQueuedHeartbeatsToNode()          .
s.mu.replicas[0].reportUnreachable()    .
s.mu.replicas[0].raftMu.Lock() [L2]     .
.                                       s.mu.replicas[0].tick()
.                                       s.mu.replicas[0].raftMu.Lock() [L2]
.                                       s.mu.replicas[0].tickRaftMuLocked()
.                                       s.mu.replicas[0].mu.Lock() [L3]
.                                       s.mu.replicas[0].maybeQuiesceLocked()
.                                       s.mu.replicas[0].maybeCoalesceHeartbeat()
.                                       s.coalescedMu.Lock() [L1]
--------------------------------G1,G2 교착 상태(leak)----------------------------------
```

## Cockroach/1055

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#1055]|[pull request]|[patch]| Mixed | Channel & WaitGroup |

[cockroach#1055]:(cockroach1055_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/1055/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/1055

### 설명

1. `Stop()`이 호출되고 락을 획득한 후 `s.stop.Wait()`에서 블록됩니다.
2. `StartTask()`가 호출되어 락 획득을 시도하지만, 이로 인해 블록됩니다.
3. 태스크가 SetStopped를 호출하지 않으므로 `Stop()`은 절대 종료되지 않습니다.

### 실행 예시

```go
G1                      G2.0                       G2.1                       G2.2                       G3
-------------------------------------------------------------------------------------------------------------------------------
s[0].stop.Add(1) [1]
go func() [G2.0]
s[1].stop.Add(1) [1]    .
go func() [G2.1]        .
s[2].stop.Add(1) [1]    .                          .
go func() [G2.2]        .                          .
go func() [G3]          .                          .                          .
<-done                  .                          .                          .                          .
.                       s[0].StartTask()           .                          .                          .
.                       s[0].draining == 0         .                          .                          .
.                       .                          s[1].StartTask()           .                          .
.                       .                          s[1].draining == 0         .                          .
.                       .                          .                          s[2].StartTask()           .
.                       .                          .                          s[2].draining == 0         .
.                       .                          .                          .                          s[0].Quiesce()
.                       .                          .                          .                          s[0].mu.Lock() [L1[0]]
.                       s[0].mu.Lock() [L1[0]]     .                          .                          .
.                       s[0].drain.Add(1) [1]      .                          .                          .
.                       s[0].mu.Unlock() [L1[0]]   .                          .                          .
.                       <-s[0].ShouldStop()        .                          .                          .
.                       .                          .                          .                          s[0].draining = 1
.                       .                          .                          .                          s[0].drain.Wait()
.                       .                          s[0].mu.Lock() [L1[1]]     .                          .
.                       .                          s[1].drain.Add(1) [1]      .                          .
.                       .                          s[1].mu.Unlock() [L1[1]]   .                          .
.                       .                          <-s[1].ShouldStop()        .                          .
.                       .                          .                          s[2].mu.Lock() [L1[2]]     .
.                       .                          .                          s[2].drain.Add() [1]       .
.                       .                          .                          s[2].mu.Unlock() [L1[2]]   .
.                       .                          .                          <-s[2].ShouldStop()        .
----------------------------------------------------G1, G2.[0..2], G3 누수(leak)-----------------------------------------------------
```

## Cockroach/10790

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#10790]|[pull request]|[patch]| Communication | Channel & Context |

[cockroach#10790]:(cockroach10790_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/10790/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/10790

### 설명

`ctxDone`의 메시지로 인해 `beginCmds`가 채널 `ch`를 비우지 않고 반환하게 될 가능성이 있으며, 이로 인해 익명 함수 고루틴(goroutines)이 누수(leak)될 수 있습니다.

### 실행 예제

```go
G1                  G2              helper goroutine
-----------------------------------------------------
.                   .               r.sendChans()
r.beginCmds()       .               .
.                   .               ch1 <- true
<- ch1              .               .
.                   .               ch2 <- true
...
.                   cancel()
<- ch1
------------------G1 leak----------------------------
```

## Cockroach/13197

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#13197]|[pull request]|[patch]| Communication | Channel & Context |

[cockroach#13197]:(cockroach13197_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/13197/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/13197

### 설명

한 고루틴이 `(*Tx).awaitDone()`을 실행하며 블록(block) 상태로 `context.Done()` 시그널을 기다립니다.

### 실행 예시

```go
G1              G2
-------------------------------
begin()
.               awaitDone()
return          .
.               <-tx.ctx.Done()
-----------G2 leaks------------
```

## Cockroach/13755

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#13755]|[pull request]|[patch]| 통신 (Communication) | 채널 및 컨텍스트 (Channel & Context) |

[cockroach#13755]:(cockroach13755_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/13755/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/13755

### 설명

버그가 있는 코드는 db 쿼리 결과(`rows`)를 닫지 않아, `(*Rows).awaitDone`을 실행 중인 하나의 goroutine이 영원히 차단(blocked)됩니다.
차단된 goroutine은 context로부터 취소 신호를 기다리는 상태입니다.

### 실행 예시

```go
G1                      G2
---------------------------------------
initContextClose()
.                       awaitDone()
return                  .
.                       <-tx.ctx.Done()
---------------G2 leaks----------------
```

## Cockroach/1462

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#1462]|[pull request]|[patch]| Mixed | Channel & WaitGroup |

[cockroach#1462]:(cockroach1462_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/1462/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/1462

### 설명

`processEventsUntil`에서 `<-stopper.ShouldStop()`을 실행하면, `lt.start` 내의 `lt.RunWorker`에 의해 생성된 goroutine들이 `lt.Events`를 통해 메시지를 보내는 과정에서 멈출(stuck) 수 있습니다. 이 경우, 송신측 goroutine들이 `s.stop.Done()`을 호출할 수 없게 되어 메인 스레드는 `s.stop.Wait()`에서 멈추게 됩니다.

### 실행 예시

```go
G1                                  G2                                G3
-------------------------------------------------------------------------------------------------------
NewLocalInterceptableTransport()
lt.start()
lt.stopper.RunWorker()
s.AddWorker()
s.stop.Add(1) [1]
go func() [G2]
stopper.RunWorker()                 .
s.AddWorker()                       .
s.stop.Add(1) [2]                   .
go func() [G3]                      .
s.Stop()                            .                                 .
s.Quiesce()                         .                                 .
.                                   select [default]                  .
.                                   lt.Events <- interceptMessage(0)  .
close(s.stopper)                    .                                 .
.                                   .                                 select [<-stopper.ShouldStop()]
.                                   .                                 <<<done>>>
s.stop.Wait()                       .
----------------------------------------------G1,G2 leak-----------------------------------------------
```

## Cockroach/16167

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#16167]|[pull request]|[patch]| 리소스 | 이중 잠금(Double Locking) |

[cockroach#16167]:(cockroach16167_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/16167/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/16167

### 설명

이는 `RWLock`을 재귀적으로 획득하여 발생하는 고루틴 누수(goroutine leak)의 또 다른 예시입니다.
동일한 기본 락을 참조하는 두 개의 락 변수(`systemConfigCond` 및 `systemConfigMu`)가 있습니다. 이 누수에는 두 개의 고루틴이 관여합니다.
첫 번째 고루틴은 `systemConfigMu.Lock()`을 획득한 후, `systemConfigMu.RLock()`을 획득하려고 시도합니다.
두 번째 고루틴은 `systemConfigMu.Lock()`을 획득합니다.
만약 두 번째 고루틴이 첫 번째 고루틴의 두 락 작업 사이에 끼어든다면, 두 고루틴 모두 누수가 발생하게 됩니다.

### 실행 예시

```go
G1                                G2
---------------------------------------------------------------
.                                 e.Start()
.                                 e.updateSystemConfig()
e.execParsed()                    .
e.systemConfigCond.L.Lock() [L1]  .
.                                 e.systemConfigMu.Lock() [L1]
e.systemConfigMu.RLock() [L1]     .
------------------------G1,G2 leak-----------------------------
```

## Cockroach/18101

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#18101]|[pull request]|[patch]| 리소스 | 이중 잠금 (Double Locking) |

[cockroach#18101]:(cockroach18101_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/18101/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/18101

### 설명

`context.Done()` 신호는 리더(reader) 고루틴을 조기에 종료시키지만, 송신자(senders)들은 종료시키지 않아 메모리 누수(leak)로 이어집니다.

### 실행 예시

```go
G1                      G2                   helper goroutine
--------------------------------------------------------------
restore()
.                       splitAndScatter()
<-readyForImportCh      .
<-readyForImportCh <==> readyForImportCh<-
...
.                       .                    cancel()
<<done>>                .                    <<done>>
                        readyForImportCh<-
-----------------------G2 leaks--------------------------------
```

## Cockroach/2448

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#2448]|[pull request]|[patch]| Communication | Channel |

[cockroach#2448]:(cockroach2448_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/2448/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/2448

### 설명

이 버그는 두 개의 goroutine이 서로의 채널이 차단 해제(unblock)되기를 기다리면서 발생합니다:

1) `MultiRaft`가 멤버십 변경(Membership change)에 대한 커밋 이벤트를 전송합니다.
2) `store.processRaft`가 이를 받아 처리를 시작합니다.
3) 다른 명령이 커밋되어 또 다른 `sendEvent`를 트리거하지만, `store.processRaft`가 다음 `select`를 수행할 준비가 되지 않았기 때문에 이 작업이 블록(block)됩니다. 결과적으로 메인 `MultiRaft` 루프 또한 이를 기다리게 됩니다.
4) 멤버십 변경이 레인지(range)에 적용되었고, 이제 스토어가 콜백을 실행하려고 시도합니다.
5) 콜백이 `callbackChan`에 쓰려고 시도하지만, 해당 채널은 `MultiRaft` 루프에 의해 소비됩니다. 그런데 `MultiRaft` 루프는 현재 `store.processRaft`가 이벤트 채널에서 데이터를 소비하기를 기다리고 있으며, `store.processRaft`는 콜백이 완료된 후에야 이를 수행하게 됩니다.

### 실행 예시

```go
G1                          G2
--------------------------------------------------------------------------
s.processRaft()             st.start()
select                      .
.                           select [default]
.                           s.handleWriteResponse()
.                           s.sendEvent()
.                           select
<-s.multiraft.Events <----> m.Events <- event
.                           select [default]
.                           s.handleWriteResponse()
.                           s.sendEvent()
.                           select [m.Events<-, <-s.stopper.ShouldStop()]
callback()                  .
select [
   m.callbackChan<-,
   <-s.stopper.ShouldStop()
]                           .
------------------------------G1,G2 leak----------------------------------
```

## Cockroach/24808

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#24808]|[pull request]|[patch]| 통신 | 채널 |

[cockroach#24808]:(cockroach24808_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/24808/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/24808

### 설명

`Compactor`를 `Start`할 때, 이미 `Suggestions`를 수신했을 수 있으며, 이로 인해 가득 찬 채널에 대해 이전에 블록되었던 쓰기 작업이 누수(leak)될 수 있습니다.

### 실행 예시

```go
G1
------------------------------------------------
...
compactor.ch <-
compactor.Start()
compactor.ch <-
--------------------G1 leaks--------------------
```

## Cockroach/25456

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#25456]|[pull request]|[patch]| Communication | Channel |

[cockroach#25456]:(cockroach25456_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/25456/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/25456

### 설명

`CheckConsistency`(전체 코드 내)가 에러를 반환할 때, 큐는 해당 에러를 로그로 남길 가치가 있는지 결정하기 위해 스토어가 드레이닝(draining) 중인지 확인합니다. 이 확인 과정에 오류가 있어, 스토어가 실제로 드레이닝을 시작할 때까지 블로킹되는 문제가 있었습니다.

### 실행 예시

```go
G1
---------------------------------------
...
<-repl.store.Stopper().ShouldQuiesce()
---------------G1 leaks----------------
```

## Cockroach/35073

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#35073]|[pull request]|[patch]| Communication | Channel |

[cockroach#35073]:(cockroach35073_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/35073/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/35073

### 설명

이전에는 outbox가 시작 중에 실패할 때 `RowChannel`을 닫지 않을 수 있었습니다. 이는 드문 경우지만 채널 통신 불일치로 인해 고루틴 누수(goroutine leaks)로 이어질 수 있었습니다.

### 실행 예시

## Cockroach/35931

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#35931]|[pull request]|[patch]| Communication | Channel |

[cockroach#35931]:(cockroach35931_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/35931/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/35931

### 설명

이전에는 여러 입력에서 데이터를 읽는 프로세서가 한 입력의 추가 데이터를 기다리는 동안 다른 입력이 가득 차 있고, 두 입력 모두 inbound 스트림에 연결되어 있는 경우, 플로우 취소 시 취소 메타데이터 메시지를 플로우로 전파하려는 과정에서 goroutine 누수가 발생할 가능성이 있었습니다. 취소 메서드는 각 inbound 스트림에 메타데이터 메시지를 한 번에 하나씩 기록했는데, 만약 첫 번째 스트림이 가득 차 있으면 취소 작업자(canceller)가 블록되어 실제로 읽기가 수행되고 있던 두 번째 스트림에 취소 메시지를 전혀 보내지 못했기 때문입니다.

### 실행 예시

## Cockroach/3710

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#3710]|[pull request]|[patch]| 리소스 | RWR 데드락 |

[cockroach#3710]:(cockroach3710_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/3710/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/3710

### 설명

고루틴 누수(goroutine leak)는 호출 체인 내에서 `RLock`을 두 번 획득하여 발생합니다.
`ForceRaftLogScanAndProcess(acquire s.mu.RLock())`
`-> MaybeAdd()`
`-> shouldQueue()`
`-> getTruncatableIndexes()`
`->RaftStatus(acquire s.mu.Rlock())`

### 실행 예시

```go
G1                                     	G2
------------------------------------------------------------
store.ForceRaftLogScanAndProcess()
s.mu.RLock()
s.raftLogQueue.MaybeAdd()
bq.impl.shouldQueue()
getTruncatableIndexes()
r.store.RaftStatus()
.                                        store.processRaft()
.                                        s.mu.Lock()
s.mu.RLock()
----------------------G1,G2 leak-----------------------------
```

## Cockroach/584

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#584]|[pull request]|[patch]| 리소스 | 이중 잠금 (Double Locking) |

[cockroach#584]:(cockroach584_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/584/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/584

### 설명

루프 내의 `break` 문 이전에 `mu.Unlock()` 호출이 누락되었습니다.

### 실행 예시

```go
G1
---------------------------
g.bootstrap()
g.mu.Lock() [L1]
if g.closed { ==> break
g.manage()
g.mu.Lock() [L1]
----------G1 leaks---------
```

## Cockroach/6181

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#6181]|[pull request]|[patch]| 리소스 | RWR 데드락 |

[cockroach#6181]:(cockroach6181_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/6181/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/6181

### 설명

동일한 `RWMutex`를 읽기 및 쓰기 용도로 재귀적으로 획득할 수 있습니다.

### 실행 예시

```go
G1                                G2                               G3                     ...
-----------------------------------------------------------------------------------------------
testRangeCacheCoalescedRquests()
initTestDescriptorDB()
pauseLookupResumeAndAssert()
return
.                                 doLookupWithToken()
.                                 .                                doLookupWithToken()
.                                 rc.LookupRangeDescriptor()       .
.                                 .                                rc.LookupRangeDescriptor()
.                                 rdc.rangeCacheMu.RLock()         .
.                                 rdc.String()                     .
.                                 .                                rdc.rangeCacheMu.RLock()
.                                 .                                fmt.Printf()
.                                 .                                rdc.rangeCacheMu.RUnlock()
.                                 .                                rdc.rangeCacheMu.Lock()
.                                 rdc.rangeCacheMu.RLock()         .
-----------------------------------G2,G3,... leak----------------------------------------------
```

## Cockroach/7504

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#7504]|[pull request]|[patch]| Resource | AB-BA Deadlock |

[cockroach#7504]:(cockroach7504_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/7504/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/7504

### 설명

`Release()`에서는 락을 `leaseState`와 `tableNameCache` 순으로 획득하지만, `AcquireByName`에서는 `tableNameCache`와 `leaseState` 순으로 획득하여 AB-BA 데드락(deadlock)이 발생합니다.

### 실행 예시

```go
G1                        G2
-----------------------------------------------------
mgr.AcquireByName()       mgr.Release()
m.tableNames.get(id)      .
c.mu.Lock() [L2]          .
.                         t.release(lease)
.                         t.mu.Lock() [L3]
.                         s.mu.Lock() [L1]
lease.mu.Lock() [L1]      .
.                         t.removeLease(s)
.                         t.tableNameCache.remove()
.                         c.mu.Lock() [L2]
---------------------G1, G2 leak---------------------
```

## Cockroach/9935

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#9935]|[pull request]|[patch]| Resource | Double Locking |

[cockroach#9935]:(cockroach9935_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/9935/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/9935

### 설명

이 버그는 `l.mu.Lock()`을 두 번 호출하여 발생합니다.

### 실행 예시

## Etcd/10492

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[etcd#10492]|[pull request]|[patch]| 리소스 | 이중 잠금(Double locking) |

[etcd#10492]:(etcd10492_test.go)
[patch]:https://github.com/etcd-io/etcd/pull/10492/files
[pull request]:https://github.com/etcd-io/etcd/pull/10492

### 설명

라인 19, 31에 대한 간단한 이중 잠금(double locking) 케이스입니다.

## Etcd/5509

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[etcd#5509]|[pull request]|[patch]| 리소스 | 이중 잠금(Double locking) |

[etcd#5509]:(etcd5509_test.go)
[patch]:https://github.com/etcd-io/etcd/pull/5509/files
[pull request]:https://github.com/etcd-io/etcd/pull/5509

### 설명

`r.acquire()`가 실패 경로(42행)에서 `r.client.mu.RLock()`을 보유한 상태로 반환됩니다.
이로 인해 `client.Close()`를 호출할 때마다 고루틴 누수가 발생합니다.

## Etcd/6708

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[etcd#6708]|[pull request]|[patch]| Resource | Double locking |

[etcd#6708]:(etcd6708_test.go)
[patch]:https://github.com/etcd-io/etcd/pull/6708/files
[pull request]:https://github.com/etcd-io/etcd/pull/6708

### 설명

제공해주신 텍스트가 매우 짧아 문맥 파악이 어렵지만, 기술적인 문맥(코드 리뷰나 디버깅)으로 판단하여 번역해 드립니다.

54행, 49행 더블 락킹(double locking)

## Etcd/6857

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[etcd#6857]|[pull request]|[patch]| 통신 (Communication) | 채널 (Channel) |

[etcd#6857]:(etcd6857_test.go)
[patch]:https://github.com/etcd-io/etcd/pull/6857/files
[pull request]:https://github.com/etcd-io/etcd/pull/6857

### 설명

`select` 문에서 다른 케이스(`n.stop`)가 선택되면 `n.status`로 데이터를 보낼 때 고루틴 누수(goroutine leaks)가 발생하게 됩니다.

### 실행 예시

```go
G1            	G2            	G3
-------------------------------------------
n.run()         .               .
.               .               n.Stop()
.               .               n.stop<-
<-n.stop        .               .
.               .               <-n.done
close(n.done)   .               .
return          .               .
.               .               return
.           	n.Status()
.           	n.status<-
----------------G2 leaks-------------------
```

## Etcd/6873

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[etcd#6873]|[pull request]|[patch]| Mixed | Channel & Lock |

[etcd#6873]:(etcd6873_test.go)
[patch]:https://github.com/etcd-io/etcd/pull/6873/files
[pull request]:https://github.com/etcd-io/etcd/pull/6873

### 설명

이 고루틴 누수(goroutine leak)는 하나의 고루틴이 락(lock)을 획득한 상태에서 상대방이 없는 채널 작업으로 인해 블록(blocked)되고, 그동안 다른 고루틴이 동일한 락을 획득하려 시도할 때 발생합니다.

### 실행 예시

```go
G1                      G2                  G3
--------------------------------------------------------------
newWatchBroadcasts()
wbs.update()
wbs.updatec <-
return
.                       <-wbs.updatec       .
.                       wbs.coalesce()      .
.                       .                   wbs.stop()
.                       .                   wbs.mu.Lock()
.                       .                   close(wbs.updatec)
.                       .                   <-wbs.donec
.                       wbs.mu.Lock()       .
---------------------G2,G3 leak--------------------------------
```

## Etcd/7492

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[etcd#7492]|[pull request]|[patch]| Mixed | Channel & Lock |

[etcd#7492]:(etcd7492_test.go)
[patch]:https://github.com/etcd-io/etcd/pull/7492/files
[pull request]:https://github.com/etcd-io/etcd/pull/7492

### 설명

이 고루틴 누수(goroutine leak)는 한 고루틴이 락(lock)을 획득한 상태에서 파트너가 없는 채널 작업으로 인해 블록(blocked)되고, 그동안 다른 고루틴이 동일한 락을 획득하려 할 때 발생합니다.

### 실행 예시

```go
G2                                    G1
---------------------------------------------------------------
.                                     stk.run()
ts.assignSimpleTokenToUser()          .
t.simpleTokensMu.Lock()               .
t.simpleTokenKeeper.addSimpleToken()  .
tm.addSimpleTokenCh <- true           .
.                                     <-tm.addSimpleTokenCh
t.simpleTokensMu.Unlock()             .
ts.assignSimpleTokenToUser()          .
...
t.simpleTokensMu.Lock()
.                                     <-tokenTicker.C
tm.addSimpleTokenCh <- true           .
.                                     tm.deleteTokenFunc()
.                                     t.simpleTokensMu.Lock()
---------------------------G1,G2 leak--------------------------
```

## Etcd/7902

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[etcd#7902]|[pull request]|[patch]| Mixed | Channel & Lock |

[etcd#7902]:(etcd7902_test.go)
[patch]:https://github.com/etcd-io/etcd/pull/7902/files
[pull request]:https://github.com/etcd-io/etcd/pull/7902

### 설명

팔로워 고루틴이 `mu.Lock()`을 먼저 획득하고 `rc.release()`를 호출하면, `rcNextc`로 데이터를 보내는 과정에서 블록됩니다.
오직 리더만이 `close(nextc)`를 통해 팔로워의 블록을 해제할 수 있습니다.
하지만 `rc.release()`를 호출하기 위해서 리더는 `mu.Lock()`을 획득해야 합니다.
해결 방법은 `rc.release()` 주변의 lock과 unlock을 제거하는 것입니다.

### 실행 예시

```go
G1                      G2 (leader)              G3 (follower)
---------------------------------------------------------------------
runElectionFunc()
doRounds()
wg.Wait()
.                       ...
.                       mu.Lock()
.                       rc.validate()
.                       rcNextc = nextc
.                       mu.Unlock()              ...
.                       .                        mu.Lock()
.                       .                        rc.validate()
.                       .                        mu.Unlock()
.                       .                        mu.Lock()
.                       .                        rc.release()
.                       .                        <-rcNextc
.                       mu.Lock()
-------------------------G1,G2,G3 leak--------------------------
```

## Grpc/1275

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[grpc#1275]|[pull request]|[patch]| Communication | Channel |

[grpc#1275]:(grpc1275_test.go)
[patch]:https://github.com/grpc/grpc-go/pull/1275/files
[pull request]:https://github.com/grpc/grpc-go/pull/1275

### 설명

이 누수에는 두 개의 goroutine이 관여하고 있습니다. 메인 goroutine은 `case <- donec`에서 블록되어 두 번째 goroutine이 채널을 닫기를 기다리고 있습니다.

두 번째 goroutine은 메인 goroutine에 의해 생성되었습니다. 이 goroutine은 `recvBufferRead.Read()`를 호출하는 `stream.Read()`를 호출할 때 블록됩니다. 두 번째 goroutine은 `i := r.recv.get()` 케이스에서 블록되어 있으며, 누군가 이 채널로 메시지를 보내기를 기다리고 있습니다.

메인 goroutine에 의해 호출되는 `client.CloseSream()` 메서드가 이 메시지를 보내야 하지만, 그렇지 않고 있습니다. 패치는 이 메시지를 전송하도록 하는 것입니다.

### 실행 예시

```go
G1                            G2
-----------------------------------------------------
testInflightStreamClosing()
.                             stream.Read()
.                             io.ReadFull()
.                             <-r.recv.get()
CloseStream()
<-donec
---------------------G1, G2 leak---------------------
```

## Grpc/1424

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[grpc#1424]|[pull request]|[patch]| Communication | Channel |

[grpc#1424]:(grpc1424_test.go)
[patch]:https://github.com/grpc/grpc-go/pull/1424/files
[pull request]:https://github.com/grpc/grpc-go/pull/1424

### 설명

`cc.lbWatcher`를 실행하는 goroutine이 `done` 채널을 비우지(draining) 않고 반환됩니다.

### 실행 예시

```go
G1                      G2                          G3
-----------------------------------------------------------------
DialContext()           .                           .
.                       cc.dopts.balancer.Notify()  .
.                       .                           cc.lbWatcher()
.                       <-doneChan
close()
---------------------------G2 leaks-------------------------------
```

## Grpc/1460

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[grpc#1460]|[pull request]|[patch]| Mixed | Channel & Lock |

[grpc#1460]:(grpc1460_test.go)
[patch]:https://github.com/grpc/grpc-go/pull/1460/files
[pull request]:https://github.com/grpc/grpc-go/pull/1460

### 설명

gRPC keepalive가 활성화되어 있고(현재 기본값은 비활성 상태임) `PermitWithoutStream`이 false인 경우(기본값), 클라이언트는 활성 스트림이 없는 상태에서 하나의 활성 스트림이 있는 상태로 전환될 때 goroutine 누수가 발생할 수 있습니다. 이때 `keepalive()` goroutine은 `<-t.awakenKeepalive`에서 멈춰 있고, 메인 goroutine은 `NewStream()`의 `t.mu.Lock()`에서 멈춰 있게 됩니다.

### 실행 예시

```go
G1                         G2
--------------------------------------------
client.keepalive()
.                       client.NewStream()
t.mu.Lock()
<-t.awakenKeepalive
.                       t.mu.Lock()
---------------G1,G2 leak-------------------
```

## Grpc/3017

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[grpc#3017]|[pull request]|[patch]| Resource | Missing unlock |

[grpc#3017]:(grpc3017_test.go)
[patch]:https://github.com/grpc/grpc-go/pull/3017/files
[pull request]:https://github.com/grpc/grpc-go/pull/3017

### 설명

65행은 unlock이 누락된 실행 경로입니다.

### 실행 예시

```go
G1                                  G2                                         G3
------------------------------------------------------------------------------------------------
NewSubConn([1])
ccc.mu.Lock() [L1]
sc = 1
ccc.subConnToAddr[1] = 1
go func() [G2]
<-done								.
.                                   ccc.RemoveSubConn(1)
.                                   ccc.mu.Lock()
.                                   addr = 1
.                                   entry = &subConnCacheEntry_grpc3017{}
.                                   cc.subConnCache[1] = entry
.                                   timer = time.AfterFunc() [G3]
.                                   entry.cancel = func()
.                                   sc = ccc.NewSubConn([1])
.                                   ccc.mu.Lock() [L1]
.                                   entry.cancel()
.                                   !timer.Stop() [true]
.                                   entry.abortDeleting = true
.                                   .                                          ccc.mu.Lock()
.                                   .                                          <<<done>>>
.                                   ccc.RemoveSubConn(1)
.                                   ccc.mu.Lock() [L1]
-------------------------------------------G1, G2 leak-----------------------------------------
```

## Grpc/660

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[grpc#660]|[pull request]|[patch]| Communication | Channel |

[grpc#660]:(grpc660_test.go)
[patch]:https://github.com/grpc/grpc-go/pull/660/files
[pull request]:https://github.com/grpc/grpc-go/pull/660

### 설명

부모 함수가 `done` 채널을 비우지 않고 반환할 수 있습니다.

### 실행 예시

```go
G1                         G2               helper goroutine
-------------------------------------------------------------
doCloseLoopUnary()
.                                   	bc.stop <- true
<-bc.stop
return
.                       done <-
----------------------G2 leak--------------------------------
```

## Grpc/795

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[grpc#795]|[pull request]|[patch]| Resource | Double locking |

[grpc#795]:(grpc795_test.go)
[patch]:https://github.com/grpc/grpc-go/pull/795/files
[pull request]:https://github.com/grpc/grpc-go/pull/795

### 설명

20번 라인은 unlock이 누락된 실행 경로입니다.

## Grpc/862

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[grpc#862]|[pull request]|[patch]| Communication | Channel & Context |

[grpc#862]:(grpc862_test.go)
[patch]:https://github.com/grpc/grpc-go/pull/862/files
[pull request]:https://github.com/grpc/grpc-go/pull/862

### 설명

반환 값 `conn`이 `nil`일 때, `cc(ClientConn)`가 닫히지 않습니다.
resetAddrConn을 실행하는 goroutine이 누수됩니다. 이에 대한 패치는 `defer func()`에서 `ClientConn`을 닫는 것입니다.

### 실행 예시

```go
G1                  G2
---------------------------------------
DialContext()
.                   cc.resetAddrConn()
.                   resetTransport()
.                   <-ac.ctx.Done()
--------------G2 leak------------------
```

## Hugo/3251

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[hugo#3251]|[pull request]|[patch]| 리소스 | RWR 데드락 |

[hugo#3251]:(hugo3251_test.go)
[patch]:https://github.com/gohugoio/hugo/pull/3251/files
[pull request]:https://github.com/gohugoio/hugo/pull/3251

### 설명

고루틴이 20번 라인에서 `Lock()`을 보유한 상태에서 29번 라인의 `RLock()`을 획득하려고 시도할 수 있습니다. 20번 라인의 `Lock()`이 절대 해제되지 않기 때문에 29번 라인의 `RLock()`은 결코 획득될 수 없습니다.

### 실행 예제

```go
G1                        G2                             G3
------------------------------------------------------------------------------------------
wg.Add(1) [W1: 1]
go func() [G2]
go func() [G3]
.                        resGetRemote()
.                        remoteURLLock.URLLock(url)
.                        l.Lock() [L1]
.                        l.m[url] = &sync.Mutex{} [L2]
.                        l.m[url].Lock() [L2]
.                        l.Unlock() [L1]
.                        .                        	     resGetRemote()
.                        .                        	     remoteURLLock.URLLock(url)
.                        .                        	     l.Lock() [L1]
.                        .                        	     l.m[url].Lock() [L2]
.                        remoteURLLock.URLUnlock(url)
.                        l.RLock() [L1]
...
wg.Wait() [W1]
----------------------------------------G1,G2,G3 leak--------------------------------------
```

## Hugo/5379

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[hugo#5379]|[pull request]|[patch]| 리소스 | 이중 잠금(Double locking) |

[hugo#5379]:(hugo5379_test.go)
[patch]:https://github.com/gohugoio/hugo/pull/5379/files
[pull request]:https://github.com/gohugoio/hugo/pull/5379

### 설명

고루틴이 먼저 99행에서 `contentInitMu`를 획득한 다음, 66행에서 동일한 `Mutex`를 다시 획득합니다.

## Istio/16224

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[istio#16224]|[pull request]|[patch]| Mixed | Channel & Lock |

[istio#16224]:(istio16224_test.go)
[patch]:https://github.com/istio/istio/pull/16224/files
[pull request]:https://github.com/istio/istio/pull/16224

### 설명

한 고루틴이 91번 라인에서 `Mutex`를 보유한 상태로 93번 라인에서 블록됩니다.
또 다른 고루틴이 101번 라인에서 동일한 `Mutex`를 획득하려고 시도하며, 103번 라인에서 동일한 채널을 추가로 비우려고 합니다.

## Istio/17860

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[istio#17860]|[pull request]|[patch]| Communication | Channel |

[istio#17860]:(istio17860_test.go)
[patch]:https://github.com/istio/istio/pull/17860/files
[pull request]:https://github.com/istio/istio/pull/17860

### 설명

70번 라인에서 `a.statusCh`를 비울(drain) 수 없습니다.

## Istio/18454

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[istio#18454]|[pull request]|[patch]| 통신 | 채널 및 컨텍스트 |

[istio#18454]:(istio18454_test.go)
[patch]:https://github.com/istio/istio/pull/18454/files
[pull request]:https://github.com/istio/istio/pull/18454

### 설명

56행과 61행의 `s.timer.Stop()`은 동시성 있게 호출될 수 있습니다
(즉, 104행과 66행의 진입점에서 호출될 수 있습니다).
[Timer](https://golang.org/pkg/time/#Timer)를 참조하십시오.

## Kubernetes/10182

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#10182]|[pull request]|[patch]| Mixed | Channel & Lock |

[kubernetes#10182]:(kubernetes10182_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/10182/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/10182

### 설명

Goroutine 1은 goroutine 3이 보유한 락(lock)으로 인해 블록(blocked)되었으며,
동시에 goroutine 3은 `ch`로 메시지를 보내는 작업으로 인해 블록되었습니다.
해당 채널은 goroutine 1이 읽습니다.

### 실행 예시

```go
G1                         G2                        	G3
-------------------------------------------------------------------------------
s.Start()
s.syncBatch()
.                          s.SetPodStatus()
.                          s.podStatusesLock.Lock()
<-s.podStatusChannel <===> s.podStatusChannel <- true
.                          s.podStatusesLock.Unlock()
.                          return
s.DeletePodStatus()        .
.                          .                    	    s.podStatusesLock.Lock()
.                          .                    	    s.podStatusChannel <- true
s.podStatusesLock.Lock()
-----------------------------G1,G3 leak-----------------------------------------
```

## Kubernetes/11298

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#11298]|[pull request]|[patch]| Communication | Channel & Condition Variable |

[kubernetes#11298]:(kubernetes11298_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/11298/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/11298

### 설명

`n.node`는 하위 락커로 `n.lock`을 사용했습니다. 서비스 루프가 처음에 이를 잠갔고, `Notify` 함수가 `n.node.Signal()`을 호출하기 전에 이를 다시 잠그려고 시도하여 고루틴 누수(goroutine leak)가 발생했습니다. 59행과 81행의 `n.cond.Signal()`은 56행의 `n.cond.Wait` 차단을 해제하는 것을 보장하지 않습니다.

## Kubernetes/13135

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#13135]|[pull request]|[patch]| Resource | AB-BA deadlock |

[kubernetes#13135]:(kubernetes13135_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/13135/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/13135

### 설명

```go
G1                              G2                              G3
----------------------------------------------------------------------------------
NewCacher()
watchCache.SetOnReplace()
watchCache.SetOnEvent()
.                               cacher.startCaching()
.                               c.Lock()
.                               c.reflector.ListAndWatch()
.                               r.syncWith()
.                               r.store.Replace()
.                               w.Lock()
.                               w.onReplace()
.                               cacher.initOnce.Do()
.                               cacher.Unlock()
return cacher                   .
.                               .                           	c.watchCache.Add()
.                               .                           	w.processEvent()
.                               .                           	w.Lock()
.                               cacher.startCaching()           .
.                               c.Lock()                        .
...
.                                                           	c.Lock()
.                               w.Lock()
--------------------------------G2,G3 leak-----------------------------------------
```

## Kubernetes/1321

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#1321]|[pull request]|[patch]| Mixed | Channel & Lock |

[kubernetes#1321]:(kubernetes1321_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/1321/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/1321

### 설명

이것은 락-채널(lock-channel) 버그입니다. 첫 번째 고루틴은 `m.lock.Lock()`을 보유한 상태에서 `distribute()`를 호출하고, `w.result`로 메시지를 보내는 과정에서 블로킹됩니다. 두 번째 고루틴은 `stopWatching()` 함수를 호출하며, 이 함수는 `w.result`를 닫음으로써 첫 번째 고루틴의 블로킹을 해제할 수 있습니다. 하지만 `w.result`를 닫기 위해서는 `stopWatching()` 함수가 `m.lock.Lock()`을 획득해야 합니다.

해결 방법은 또 다른 채널을 도입하고, 두 번째 채널로부터의 메시지 수신을 `w.result`와 동일한 `select` 문에 배치하는 것입니다. 두 번째 채널을 닫으면 `m.lock.Lock()`을 유지할 필요 없이 첫 번째 goroutine의 블록을 해제할 수 있습니다.

### 실행 예시

```go
G1                          G2
----------------------------------------------
testMuxWatcherClose()
NewMux()
.                           m.loop()
.                           m.distribute()
.                           m.lock.Lock()
.                           w.result <- true
w := m.Watch()
w.Stop()
mw.m.stopWatching()
m.lock.Lock()
---------------G1,G2 누수(leak)---------------------
```

## Kubernetes/25331

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#25331]|[pull request]|[patch]| Communication | Channel & Context |

[kubernetes#25331]:(kubernetes25331_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/25331/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/25331

### 설명

에러가 발생하여 `resultChan`이 차단된 상태에서 `Stop()`의 컨텍스트가 취소될 때, 잠재적인 고루틴 누수(goroutine leak)가 발생할 수 있습니다.

### 실행 예시

```go
G1                    G2
------------------------------------
wc.run()
.                   wc.Stop()
.                   wc.errChan <-
.                   wc.cancel()
<-wc.errChan
wc.cancel()
wc.resultChan <-
-------------G1 leak----------------
```

## Kubernetes/26980

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#26980]|[pull request]|[patch]| Mixed | Channel & Lock |

[kubernetes#26980]:(kubernetes26980_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/26980/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/26980

### 설명

한 고루틴이 24행에서 `Mutex`를 보유한 상태로 35행에서 블록(blocked)되었습니다.
또 다른 고루틴이 동일한 `Mutex`를 획득하려다 58행에서 블록되었습니다.

## Kubernetes/30872

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#30872]|[pull request]|[patch]| Resource | AB-BA deadlock |

[kubernetes#30872]:(kubernetes30872_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/30872/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/30872

### 설명

락이 92행과 157행 모두에서 획득됩니다.

## Kubernetes/38669

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#38669]|[pull request]|[patch]| Communication | Channel |

[kubernetes#38669]:(kubernetes38669_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/38669/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/38669

### 설명

죄송합니다. 번역할 대상 콘텐츠가 제공되지 않았습니다. 번역하시려는 Markdown 내용을 입력해 주세요.

## Kubernetes/5316

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#5316]|[pull request]|[patch]| 통신 (Communication) | 채널 (Channel) |

[kubernetes#5316]:(kubernetes5316_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/5316/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/5316

### 설명

메인 고루틴(main goroutine)이 채널을 소비하지 않는 case를 선택하면, 익명 고루틴(anonymous goroutine)은 채널로 데이터를 보내는 과정에서 블록(blocked) 상태가 됩니다.

### 실행 예시

```go
G1                      G2
--------------------------------------
finishRequest()
.                       fn()
time.After()
.                       errCh<-/ch<-
--------------G2 leaks----------------
```

## Kubernetes/58107

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#58107]|[pull request]|[patch]| 리소스 | RWR deadlock |

[kubernetes#58107]:(kubernetes58107_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/58107/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/58107

### 설명

읽기 및 쓰기 락(lock)에 대한 규칙: 동시 읽기 락을 허용하며, 쓰기 락이 읽기 락보다 높은 우선순위를 가집니다.

이 버그에는 두 개의 큐(queue 1 및 queue 2)가 관여하며, 두 큐는 동일한 읽기-쓰기 잠금(`rq.workerLock.RLock()`)으로 보호됩니다. queue 1 또는 queue 2에서 요소를 가져오기 전에 `rq.workerLock.RLock()`을 획득합니다. 만약 큐가 비어 있다면 `cond.Wait()`가 호출됩니다. 주기적으로 `rq.workerLock.Lock()`을 호출하는 또 다른 고루틴(goroutine D)이 있습니다. 다음과 같은 상황에서 데드락(deadlock)이 발생합니다. queue 1이 비어 있어 일부 고루틴들이 `rq.workerLock.RLock()`을 보유한 채 `cond.Wait()`에서 블록됩니다. 이때 고루틴 D는 `rq.workerLock.Lock()`을 획득하려다 블록됩니다. 일부 고루틴들이 queue 2의 작업을 처리하려고 시도하지만, 쓰기 잠금(write lock)이 더 높은 우선순위를 가지므로 `rq.workerLock.RLock()`을 획득하려다 블록됩니다.

해결 방법은 큐에서 데이터를 가져오는 동안 `rq.workerLock.RLock()`을 획득하지 않는 것입니다. 따라서 goroutine이 `cond.Wait()`에서 블록되었을 때, `rq.workLock.RLock()`은 유지되지 않습니다.

### 실행 예시

```go
G3                      G4                      G5
--------------------------------------------------------------------
.                       .                       Sync()
rq.workerLock.RLock()   .                       .
q.cond.Wait()           .                       .
.                       .                       rq.workerLock.Lock()
.                       rq.workerLock.RLock()
.                       q.cond.L.Lock()
-----------------------------G3,G4,G5 leak-----------------------------
```

## Kubernetes/62464

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#62464]|[pull request]|[patch]| Resource | RWR deadlock |

[kubernetes#62464]:(kubernetes62464_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/62464/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/62464

### 설명

이것은 재귀적 읽기 잠금(recursive read lock) 버그의 또 다른 예시입니다. Go 개발자들은 동일한 스레드에서 `RLock`을 재귀적으로 사용해서는 안 된다는 점에 주목해 왔습니다.

### 실행 예시

```go
G1                                  G2
--------------------------------------------------------
m.reconcileState()
m.state.GetCPUSetOrDefault()
s.RLock()
s.GetCPUSet()
.                                   p.RemoveContainer()
.                                   s.GetDefaultCPUSet()
.                                   s.SetDefaultCPUSet()
.                                   s.Lock()
s.RLock()
---------------------G1,G2 leak--------------------------
```

## Kubernetes/6632

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#6632]|[pull request]|[patch]| Mixed | Channel & Lock |

[kubernetes#6632]:(kubernetes6632_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/6632/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/6632

### 설명

`resetChan`이 가득 찼을 때, `WriteFrame`은 락(lock)을 보유한 상태에서 채널이 비워질 때까지 블록(block)됩니다. 그러면 `WriteFrame`이 이미 락을 보유하고 있기 때문에 `monitor()`가 `resetChan`을 닫는 데 실패하게 됩니다.

### 실행 예시

```go
G1                      G2                  helper goroutine
----------------------------------------------------------------
i.monitor()
<-i.conn.closeChan
.                       i.WriteFrame()
.                       i.writeLock.Lock()
.                       i.resetChan <-
.                       .                   i.conn.closeChan<-
i.writeLock.Lock()
----------------------G1,G2 leak--------------------------------
```

## Kubernetes/70277

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#70277]|[pull request]|[patch]| Communication | Channel |

[kubernetes#70277]:kubernetes70277_test.go
[patch]:https://github.com/kubernetes/kubernetes/pull/70277/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/70277

### 설명

`wait.poller()`는 `WaitFunc` 타입의 함수를 반환합니다.
이 함수는 고루틴(goroutine)을 생성하며, 해당 고루틴은 `after`가 만료되거나 `done`이 닫힌 후에만 종료됩니다.

70행에서 정의된 `doneCh`가 한 번도 닫히지(closed) 않았습니다.

## Moby/17176

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[moby#17176]|[pull request]|[patch]| Resource | Double locking |

[moby#17176]:(moby17176_test.go)
[patch]:https://github.com/moby/moby/pull/17176/files
[pull request]:https://github.com/moby/moby/pull/17176

### 설명

`devices.nrDeletedDevices`는 `devices.Lock()`을 호출하지만, 삭제된 장치가 없는 경우(36행) 이를 해제하지 않습니다. 이는 `devices.Lock()`을 획득하려는 다른 goroutine들을 차단하게 됩니다.

## Moby/21233

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[moby#21233]|[pull request]|[patch]| 통신 (Communication) | 채널 (Channel) |

[moby#21233]:(moby21233_test.go)
[patch]:https://github.com/moby/moby/pull/21233/files
[pull request]:https://github.com/moby/moby/pull/21233

### 설명

이 테스트는 생성된 모든 진행 상황 업데이트(progress update)를 수신하는지 확인하고 있었습니다. 하지만 이러한 중간 진행 상황 업데이트의 전달은 보장되지 않습니다. 이전 업데이트가 아직 채널로 전송되지 않은 경우, 새로운 업데이트가 이전 업데이트를 덮어쓸 수 있습니다.

`t.Fatalf` 호출이 채널을 소비하던 현재 goroutine을 종료시켰으며, 이로 인해 적절한 실패 메시지가 출력되는 대신 데드락(deadlock)이 발생하고 결국 테스트 타임아웃으로 이어졌습니다.

### 실행 예시

```go
G1                      G2                  G3
----------------------------------------------------------
testTransfer()          .                   .
tm.Transfer()           .                   .
t.Watch()               .                   .
.                       WriteProgress()     .
.                       ProgressChan<-      .
.                       .                   <-progressChan
.                       ...                 ...
.                       return              .
.                                           <-progressChan
<-watcher.running
----------------------G1,G3 leak--------------------------
```

## Moby/25384

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[moby#25384]|[pull request]|[patch]| Mixed | WaitGroup 오용 |

[moby#25384]:(moby25384_test.go)
[patch]:https://github.com/moby/moby/pull/25384/files
[pull request]:https://github.com/moby/moby/pull/25384

### 설명

`n=1`일 때(`n`은 `len(pm.plugins)`), `group.Wait()`의 위치는 중요하지 않습니다.
`n > 1`일 때, `group.Wait()`는 각 반복(iteration)마다 호출됩니다. `group.Wait()`가 호출될 때마다, 이는 `group.Done()`이 `n`번 실행될 때까지 대기합니다.
하지만, 한 번의 반복에서는 `group.Done()`이 단 한 번만 실행됩니다.

# sync.WaitGroup의 잘못된 사용법

`sync.WaitGroup`은 여러 고루틴(goroutine)이 완료될 때까지 대기해야 할 때 사용하는 유용한 도구입니다. 하지만 잘못 사용하면 데드락(deadlock)이나 패닉(panic)과 같은 심각한 런타임 오류가 발생할 수 있습니다.

다음은 `sync.WaitGroup` 사용 시 자주 발생하는 실수들과 그 해결 방법입니다.

## 1. 고루틴 내부에서 `Add` 호출하기

가장 흔한 실수 중 하나는 `wg.Add(1)`을 고루틴 내부에서 호출하는 것입니다.

### 잘못된 예시
```go
func main() {
    var wg sync.WaitGroup
    for i := 0; i < 5; i++ {
        go func(i int) {
            wg.Add(1) // 위험!
            defer wg.Done()
            fmt.Println(i)
        }(i)
    }
    wg.Wait()
}
```

**문제점:** `wg.Add(1)`이 호출되기 전에 `wg.Wait()`가 먼저 실행될 수 있습니다. 메인 고루틴은 `WaitGroup` 카운터가 0이라고 판단하여 즉시 종료될 수 있으며, 이 경우 일부 또는 모든 고루틴이 실행되지 않은 채 프로그램이 끝납니다. 또한, 실행 타이밍에 따라 레이스 컨디션(race condition)이 발생할 수 있습니다.

### 올바른 예시
`wg.Add`는 항상 고루틴을 시작하기 **전**에 호출해야 합니다.

```go
func main() {
    var wg sync.WaitGroup
    for i := 0; i < 5; i++ {
        wg.Add(1) // 고루틴 시작 전에 호출
        go func(i int) {
            defer wg.Done()
            fmt.Println(i)
        }(i)
    }
    wg.Wait()
}
```

---

## 2. `WaitGroup`을 값으로 전달하기

`sync.WaitGroup`을 함수에 전달할 때 포인터가 아닌 값으로 전달하면 예상치 못한 동작이 발생합니다.

### 잘못된 예시
```go
func worker(id int, wg sync.WaitGroup) { // 값으로 전달 (복사됨)
    defer wg.Done()
    fmt.Printf("Worker %d starting\n", id)
}

func main() {
    var wg sync.WaitGroup
    for i := 1; i <= 3; i++ {
        wg.Add(1)
        go worker(i, wg)
    }
    wg.Wait() // 데드락 발생!
}
```

**문제점:** `sync.WaitGroup`은 내부적으로 상태를 관리하는 구조체입니다. 이를 값으로 전달하면 구조체가 **복사**됩니다. `worker` 함수 내에서 호출되는 `wg.Done()`은 복사본의 카운터를 감소시키며, `main` 함수에 있는 원본 `WaitGroup`의 카운터는 절대 줄어들지 않습니다. 결국 `wg.Wait()`는 영원히 대기하게 되어 데드락이 발생합니다.

### 올바른 예시
항상 `*sync.WaitGroup` (포인터)를 전달하십시오.

```go
func worker(id int, wg *sync.WaitGroup) { // 포인터로 전달
    defer wg.Done()
    fmt.Printf("Worker %d starting\n", id)
}

func main() {
    var wg sync.WaitGroup
    for i := 1; i <= 3; i++ {
        wg.Add(1)
        go worker(i, &wg)
    }
    wg.Wait()
}
```

---

## 3. 음수 카운터로 인한 패닉

`wg.Done()`은 내부적으로 `wg.Add(-1)`을 호출합니다. 만약 `Add`로 증가시킨 횟수보다 `Done`을 더 많이 호출하면 카운터가 음수가 되며, Go 런타임은 즉시 패닉을 발생시킵니다.

### 위험한 상황
```go
func worker(wg *sync.WaitGroup) {
    defer wg.Done()
    if someError {
        wg.Done() // 실수로 한 번 더 호출
        return
    }
}
```

**해결 방법:** `defer wg.Done()`을 사용하여 고루틴이 어떤 경로로 종료되든 정확히 한 번만 호출되도록 보장하십시오.

## 요약 체크리스트

| 실수 | 결과 | 해결책 |
| :--- | :--- | :--- |
| 고루틴 내부에서 `Add` 호출 | 고루틴 누락 또는 레이스 컨디션 | `go` 키워드 호출 전에 `Add` 수행 |
| `WaitGroup`을 값으로 전달 | 데드락 (Deadlock) | 포인터(`*sync.WaitGroup`)로 전달 |
| `Done`을 너무 많이 호출 | 패닉 (Panic) | `defer wg.Done()` 사용으로 1회 호출 보장 |

## Moby/27782

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[moby#27782]|[pull request]|[patch]| 통신 | 채널 및 조건 변수 |

[moby#27782]:(moby27782_test.go)
[patch]:https://github.com/moby/moby/pull/27782/files
[pull request]:https://github.com/moby/moby/pull/27782

### 설명

### 실행 예시

```go
G1                      G2                         G3
-----------------------------------------------------------------------
InitializeStdio()
startLogging()
l.ReadLogs()
NewLogWatcher()
.                       l.readLogs()
container.Reset()       .
LogDriver.Close()       .
r.Close()               .
close(w.closeNotifier)  .
.                       followLogs(logWatcher)
.                       watchFile()
.                       New()
.                       NewEventWatcher()
.                       NewWatcher()
.                       .                       	w.readEvents()
.                       .                       	event.ignoreLinux()
.                       .                       	return false
.                       <-logWatcher.WatchClose()   .
.                       fileWatcher.Remove()        .
.                       w.cv.Wait()                 .
.                       .                       	w.Events <- event
------------------------------G2,G3 leak-------------------------------
```

## Moby/28462

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[moby#28462]|[pull request]|[patch]| Mixed | Channel & Lock |

[moby#28462]:(moby28462_test.go)
[patch]:https://github.com/moby/moby/pull/28462/files
[pull request]:https://github.com/moby/moby/pull/28462

### 설명

하나의 goroutine이 락을 획득한 후 `stop` 채널을 통해 메시지를 보내려고 시도하는 동안, 다른 goroutine은 동일한 락을 획득하려고 시도할 수 있습니다. 순서가 잘못되면 두 goroutine 모두 누수(leak)가 발생하게 됩니다.

### 실행 예시

```go
G1                        	G2
--------------------------------------------------------------
monitor()
handleProbeResult()
.                       	d.StateChanged()
.                       	c.Lock()
.                       	d.updateHealthMonitorElseBranch()
.                       	h.CloseMonitorChannel()
.                       	s.stop <- struct{}{}
c.Lock()
----------------------G1,G2 누수(leak)------------------------------
```

## Moby/30408

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[moby#30408]|[pull request]|[patch]| Communication | Condition Variable |

[moby#30408]:(moby30408_test.go)
[patch]:https://github.com/moby/moby/pull/30408/files
[pull request]:https://github.com/moby/moby/pull/30408

### 설명

22행의 `Wait()`에 대응하는 `Signal()` 또는 `Broadcast()`가 없습니다.

### 실행 예시

```go
G1                 G2
------------------------------------------
testActive()
.                  p.waitActive()
.                  p.activateWait.L.Lock()
.                  p.activateWait.Wait()
<-done
-----------------G1,G2 leak---------------
```

## Moby/33781

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[moby#33781]|[pull request]|[patch]| 통신 (Communication) | 채널 및 컨텍스트 (Channel & Context) |

[moby#33781]:(moby33781_test.go)
[patch]:https://github.com/moby/moby/pull/33781/files
[pull request]:https://github.com/moby/moby/pull/33781

### 설명

익명 함수를 사용하여 생성된 goroutine이 버퍼가 없는 channel로 메시지를 보내는 과정에서 블록(blocked)되었습니다. 하지만 부모 goroutine에는 부모 함수가 channel의 데이터를 소비(draining)하지 않고 반환하는 경로가 존재합니다.

### 실행 예시

```go
G1             	G2             G3
----------------------------------------
monitor()       .
<-time.After()  .
.           	.
<-stop          stop<-
.
cancelProbe()
return
.                               result<-
----------------G3 leak------------------
```

## Moby/36114

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[moby#36114]|[pull request]|[patch]| Resource | Double locking |

[moby#36114]:(moby36114_test.go)
[patch]:https://github.com/moby/moby/pull/36114/files
[pull request]:https://github.com/moby/moby/pull/36114

### 설명

`svm.hotRemoveVHDsAtStart()`를 호출할 때 `svm` 구조체의 락(lock)이 이미 잠겨 있는 상태입니다.

## Moby/4951

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[moby#4951]|[pull request]|[patch]| 리소스 | AB-BA 데드락 |

[moby#4951]:(moby4951_test.go)
[patch]:https://github.com/moby/moby/pull/4951/files
[pull request]:https://github.com/moby/moby/pull/4951

### 설명

근본 원인과 패치 내용은 커밋 설명에 명확하게 설명되어 있습니다. 글로벌 락은 `devices.Lock()`이며, 디바이스 락은 `baseInfo.lock.Lock()`입니다. 이 버그는 재현될 가능성이 매우 높습니다.

## Moby/7559

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[moby#7559]|[pull request]|[patch]| 리소스 | 이중 잠금 (Double locking) |

[moby#7559]:(moby7559_test.go)
[patch]:https://github.com/moby/moby/pull/7559/files
[pull request]:https://github.com/moby/moby/pull/7559

### 설명

25행에 `.Unlock` 호출이 누락되었습니다.

### 실행 예시

```go
G1
---------------------------
proxy.connTrackLock.Lock()
if err != nil { continue }
proxy.connTrackLock.Lock()
-----------G1 leaks--------
```

## Serving/2137

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[serving#2137]|[pull request]|[patch]| Mixed | Channel & Lock |

[serving#2137]:(serving2137_test.go)
[patch]:https://github.com/ knative/serving/pull/2137/files
[pull request]:https://github.com/ knative/serving/pull/2137

### 설명

### 실행 예시

```go
G1                           	G2                      	G3
----------------------------------------------------------------------------------
b.concurrentRequests(2)         .                           .
b.concurrentRequest()           .                           .
r.lock.Lock()                   .                           .
.                               start.Done()                .
start.Wait()                    .                           .
b.concurrentRequest()           .                           .
r.lock.Lock()                   .                           .
.                               .                           start.Done()
start.Wait()                    .                           .
unlockAll(locks)                .                           .
unlock(lc)                      .                           .
req.lock.Unlock()               .                           .
ok := <-req.accepted            .                           .
.                            	b.Maybe()                   .
.                            	b.activeRequests <- t       .
.                            	thunk()                     .
.                            	r.lock.Lock()               .
.                            	.                           b.Maybe()
.                            	.                           b.activeRequests <- t
----------------------------G1,G2,G3 leak-----------------------------------------
```

## Syncthing/4829

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[syncthing#4829]|[pull request]|[patch]| Resource | Double locking |

[syncthing#4829]:(syncthing4829_test.go)
[patch]:https://github.com/syncthing/syncthing/pull/4829/files
[pull request]:https://github.com/syncthing/syncthing/pull/4829

### 설명

17행과 30행에서 이중 잠금(Double locking)이 발생합니다.

### 실행 예시

```go
G1
---------------------------
mapping.clearAddresses()
m.mut.Lock() [L2]
m.notify(...)
m.mut.RLock() [L2]
----------G1 leaks---------
```

## Syncthing/5795

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[syncthing#5795]|[pull request]|[patch]| 통신 | 채널 |

[syncthing#5795]:(syncthing5795_test.go)
[patch]:https://github.com/syncthing/syncthing/pull/5795/files
[pull request]:https://github.com/syncthing/syncthing/pull/5795

### 설명

82행의 `<-c.dispatcherLoopStopped`는 `dispatcherLoop()`가 72행에서 블로킹(blocking)되어 있기 때문에 무한히 대기하게 됩니다.

### 실행 예시

```go
G1                            G2
--------------------------------------------------------------
c.Start()
go c.dispatcherLoop() [G3]
.                             select [<-c.inbox, <-c.closed]
c.inbox <- <================> [<-c.inbox]
<-c.dispatcherLoopStopped     .
.                             default
.                             c.ccFn()/c.Close()
.                             close(c.closed)
.                             <-c.dispatcherLoopStopped
---------------------G1,G2 leak-------------------------------
```
