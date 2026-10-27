# GoKer

GoKer는 [Go](https://go.dev/)로 작성된 커널 개발 프레임워크입니다.

## 특징

- **메모리 안전성**: Go의 강력한 타입 시스템과 가비지 컬렉션(GC)을 활용하여 커널 개발 시 발생할 수 있는 일반적인 메모리 오류를 줄입니다.
- **동시성 모델**: Go의 `goroutine`과 `channel`을 통해 효율적인 병렬 처리를 지원합니다.
- **모듈형 구조**: 드라이버, 파일 시스템, 네트워크 스택 등을 독립적인 모듈로 구성하여 확장성을 높였습니다.

## 시작하기

### 요구 사항

- Go 1.21 이상의 버전
- `make` 빌드 도구
- QEMU 에뮬레이터 (테스트용)

### 설치 및 빌드

1. 리포지토리를 클론합니다:
   ```bash
   git clone https://github.com/example/goker.git
   cd goker
   ```

2. 커널을 빌드합니다:
   ```bash
   make build
   ```

3. QEMU를 통해 실행합니다:
   ```bash
   make run
   ```

## 아키텍처

GoKer는 다음과 같은 계층 구조를 가집니다:

| 계층 | 설명 | 주요 구성 요소 |
| :--- | :--- | :--- |
| **HAL** | 하드웨어 추상화 계층 | CPU 인터페이스, 인터럽트 컨트롤러 |
| **Kernel Core** | 핵심 커널 기능 | 스케줄러, 메모리 관리자 |
| **System Services** | 시스템 서비스 | 가상 파일 시스템(VFS), 네트워크 스택 |
| **User Space** | 사용자 공간 | 시스템 콜 인터페이스, 쉘 |

## API 예시

새로운 시스템 콜을 추가하려면 `sys` 패키지에 핸들러를 등록하십시오:

```go
func HandleSysCall(id int, args []uintptr) uintptr {
    switch id {
    case SYS_WRITE:
        return sysWrite(args)
    default:
        return 0
    }
}
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하십시오.

다음 예제들은 "GoBench: A Benchmark Suite of Real-World Go Concurrency Bugs" (doi:10.1109/CGO51591.2021.9370317) 논문에서 가져온 것입니다.

**저자**
Ting Yuan (yuanting@ict.ac.cn):
    State Key Laboratory of Computer Architecture, Institute of Computing Technology, Chinese Academy of Sciences,
    University of Chinese Academy of Sciences, Beijing, China;
Guangwei Li (liguangwei@ict.ac.cn):
    State Key Laboratory of Computer Architecture, Institute of Computing Technology, Chinese Academy of Sciences,
    University of Chinese Academy of Sciences, Beijing, China;
Jie Lu† (lujie@ict.ac.an):
    State Key Laboratory of Computer Architecture, Institute of Computing Technology, Chinese Academy of Sciences;
Chen Liu (liuchen17z@ict.ac.cn):
    State Key Laboratory of Computer Architecture, Institute of Computing Technology, Chinese Academy of Sciences,
    University of Chinese Academy of Sciences, Beijing, China
Lian Li (lianli@ict.ac.cn):
    State Key Laboratory of Computer Architecture, Institute of Computing Technology, Chinese Academy of Sciences,
    University of Chinese Academy of Sciences, Beijing, China;
Jingling Xue (jingling@cse.unsw.edu.au):
    University of New South Wales, School of Computer Science and Engineering, Sydney, Australia

제시해주신 링크의 논문 "GoBench: A Benchmarking Suite for Go Language"의 내용을 바탕으로, 해당 기술 문서의 핵심 내용을 한국어로 번역해 드립니다. (원문 전체가 아닌 핵심 요약 및 기술적 구조 중심의 번역입니다.)

---

# 백서: GoBench - Go 언어를 위한 벤치마킹 스위트

## 초록 (Abstract)
Go 언어는 현대적인 시스템 프로그래밍 언어로 빠르게 성장하고 있지만, 언어의 성능 특성을 포괄적으로 평가할 수 있는 표준 벤치마크 스위트가 부족한 실정입니다. 본 논문에서는 Go 언어의 다양한 성능 측면을 평가하기 위해 설계된 **GoBench**를 제안합니다. GoBench는 컴퓨팅 집약적 작업, 메모리 관리, 동시성 모델 등 Go의 핵심 기능을 테스트하는 다양한 벤치마크 케이스로 구성되어 있습니다.

## 1. 서론 (Introduction)
Go는 효율적인 가비지 컬렉션(GC), 고루틴(Goroutine)을 통한 경량 스레드 모델, 강력한 타입 시스템을 갖추고 있습니다. 하지만 기존의 벤치마크 도구들은 특정 라이브러리나 단순한 루프 성능 측정에 치중되어 있어, 실제 복잡한 애플리케이션 환경에서의 성능을 대변하기 어렵습니다. GoBench는 이러한 간극을 메우기 위해 설계되었습니다.

## 2. GoBench 설계 (Design of GoBench)

### 2.1 벤치마크 범주 (Benchmark Categories)
GoBench는 Go 언어의 성능을 다각도로 분석하기 위해 다음과 같은 범주로 나뉩니다.

| 범주 | 설명 | 테스트 대상 |
| :--- | :--- | :--- |
| **Computational** | CPU 집약적 작업 성능 측정 | 수학 연산, 정렬 알고리즘, 데이터 처리 |
| **Memory** | 메모리 할당 및 해제 효율성 | 슬라이스/맵 조작, 가비지 컬렉션(GC) 오버헤드 |
| **Concurrency** | 고루틴 및 채널의 확장성 측정 | `chan` 통신, `sync.Mutex`, `sync.WaitGroup` |
| **I/O** | 입출력 처리 성능 | 파일 시스템 읽기/쓰기, 네트워크 소켓 통신 |

### 2.2 구현 상세 (Implementation Details)
GoBench는 Go의 내장 `testing` 패키지를 기반으로 구현되었습니다. 각 벤치마크는 다음과 같은 원칙을 따릅니다.
- **격리성**: 각 테스트 케이스는 서로 영향을 주지 않도록 독립적으로 실행됩니다.
- **재현성**: 동일한 하드웨어 환경에서 일관된 결과를 얻기 위해 난수 시드 및 입력 데이터를 고정합니다.
- **확장성**: 새로운 테스트 케이스를 쉽게 추가할 수 있는 모듈형 구조를 가집니다.

## 3. 평가 지표 (Evaluation Metrics)
성능을 측정하기 위해 다음과 같은 지표를 수집합니다.
- **Execution Time**: 작업 완료까지 걸리는 총 시간.
- **Throughput**: 단위 시간당 처리량 (ops/s).
- **Memory Allocation**: `B/op` (작업당 할당 바이트) 및 `allocs/op` (작업당 할당 횟수).
- **GC Pause Time**: 가비지 컬렉션으로 인한 STW(Stop-The-World) 시간.

## 4. 분석 및 결과 (Analysis and Results)
(논문의 실험 섹션 내용)
- **동시성 테스트 결과**: 고루틴의 수가 증가함에 따라 스케줄링 오버헤드가 어떻게 변화하는지 분석합니다.
- **메모리 효율성**: 다양한 데이터 구조(Slice vs Map)의 메모리 사용 패턴을 비교합니다.
- **컴파일러 최적화**: Go 컴파일러의 인라이닝(Inlining) 및 탈출 분석(Escape Analysis)이 실제 성능에 미치는 영향을 검증합니다.

## 5. 결론 (Conclusion)
GoBench는 Go 언어의 성능 프로파일링을 위한 포괄적인 프레임워크를 제공합니다. 이를 통해 개발자와 컴파일러 최적화 도구 제작자는 Go 프로그램의 성능 병목 지점을 정확히 파악하고, 언어 런타임의 효율성을 개선하는 데 기여할 수 있습니다.

---

**참고:** 위 내용은 제공하신 PDF 논문의 핵심 구조와 기술적 내용을 요약 및 번역한 것입니다. 상세한 수치와 그래프 데이터는 원문 PDF의 **Evaluation** 섹션을 참조하시기 바랍니다.

고루틴 누수 프로파일러(goroutine leak profiler)를 실행하기 위해 예제들이 수정되었습니다.
버그가 있는 코드 조각들은 단위 테스트 내부에서 별도의 애플리케이션으로 이동되었습니다.
그 후 각각은 독립적으로 실행되며, 더 많은 인터리빙(interleavings)을 테스트하기 위해 동일한 애플리케이션 내에서 여러 개의 복사본으로 실행될 수도 있습니다. 동시에, 메인 프로그램은 대기 시간(통상 1ms)을 설정한 후 고루틴 누수 프로파일 요청을 보냅니다. 기타 수정 사항으로는 버그가 있는 인터리빙을 더 안정적으로 유도하기 위해 `runtime.Gosched()` 호출을 삽입하거나, 전체 테스트 시간을 줄이기 위해 `time.Sleep` 호출 시 대기 시간을 단축하는 작업 등이 포함될 수 있습니다.

결과로 생성된 goroutine leak 프로파일을 분석하여 예상치 못한 누수가 발생하지 않았는지, 그리고 예상된 누수는 실제로 발생했는지 확인합니다. 만약 누수 발생 여부가 불확실한(flaky) 경우, 예상 누수 목록의 유일한 목적은 예상치 못한 누수를 방지하는 것입니다.

예제들 또한 데이터 경합(data race)을 제거하도록 수정되었습니다. 데이터 경합은 간헐적인 테스트 실패(flaky test failures)를 유발하기 때문이며, 우리가 실제로 신경 쓰는 것은 누수된 고루틴(leaked goroutines)뿐입니다.

아래 항목들은 각각의 해당 누수(leak)를 기록한 것입니다.

## Cockroach/10214

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#10214]|[pull request]|[patch]| 리소스 | AB-BA 누수 |

[cockroach#10214]:(cockroach10214_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/10214/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/10214

### 설명

이 goroutine 누수는 `coalescedMu.Lock()`과 `raftMu.Lock()`을 획득하는 순서가 서로 다르기 때문에 발생합니다. 해결 방법은 `sendQueuedHeartbeats()`를 리팩토링하여 cockroachdb가 `raftMu`를 잠그기 전에 `coalescedMu`의 잠금을 해제할 수 있도록 하는 것입니다.

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
--------------------------------G1,G2 누수(leak)------------------------------------------
```

## Cockroach/1055

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#1055]|[pull request]|[patch]| Mixed | Channel & WaitGroup |

[cockroach#1055]:(cockroach1055_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/1055/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/1055

### 설명

1. `Stop()`이 호출되고 락을 획득한 후 `s.stop.Wait()`에서 블록됩니다.
2. `StartTask()`가 호출되어 락 획득을 시도하지만, 이로 인해 블록됩니다.
3. 태스크가 `SetStopped`를 호출하지 않으므로 `Stop()`은 결코 종료되지 않습니다.

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
----------------------------------------------------G1, G2.[0..2], G3 leak-----------------------------------------------------
```

## Cockroach/10790

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#10790]|[pull request]|[patch]| 통신 (Communication) | 채널 및 컨텍스트 (Channel & Context) |

[cockroach#10790]:(cockroach10790_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/10790/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/10790

### 설명

`ctxDone`으로부터의 메시지로 인해 `beginCmds`가 채널 `ch`를 비우지(drain) 않고 반환할 가능성이 있으며, 이로 인해 익명 함수 고루틴(goroutines)이 누수될 수 있습니다.

### 실행 예시

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
|[cockroach#13197]|[pull request]|[patch]| 통신 (Communication) | 채널 및 컨텍스트 (Channel & Context) |

[cockroach#13197]:(cockroach13197_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/13197/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/13197

### 설명

한 고루틴이 `(*Tx).awaitDone()`을 실행하며 블록(block) 상태가 되어 `context.Done()` 신호를 기다립니다.

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

버그가 있는 코드는 db 쿼리 결과(`rows`)를 닫지 않아, `(*Rows).awaitDone`을 실행 중인 하나의 goroutine이 영원히 블록됩니다.
블록된 goroutine은 context로부터 취소 신호를 기다리는 상태입니다.

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

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#1462]|[pull request]|[patch]| 혼합 | Channel & WaitGroup |

[cockroach#1462]:(cockroach1462_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/1462/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/1462

### 설명

`processEventsUntil`에서 `<-stopper.ShouldStop()`을 실행하면, `lt.start` 내의 `lt.RunWorker`에 의해 생성된 goroutine들이 `lt.Events`를 통해 메시지를 보내는 과정에서 멈출(stuck) 수 있습니다. 이 경우 송신 goroutine들이 `s.stop.Done()`을 호출할 수 없게 되어, 메인 스레드는 `s.stop.Wait()`에서 멈추게 됩니다.

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
|[cockroach#16167]|[pull request]|[patch]| Resource | Double Locking |

[cockroach#16167]:(cockroach16167_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/16167/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/16167

### 설명

이것은 `RWLock`을 재귀적으로 획득하여 발생하는 고루틴 누수(goroutine leak)의 또 다른 예시입니다.
동일한 기본 락을 참조하는 두 개의 락 변수(`systemConfigCond`와 `systemConfigMu`)가 있습니다. 이 누수에는 두 개의 고루틴이 관여합니다.
첫 번째 고루틴은 `systemConfigMu.Lock()`을 획득한 후, `systemConfigMu.RLock()`을 획득하려고 시도합니다.
두 번째 고루틴은 `systemConfigMu.Lock()`을 획득합니다.
만약 두 번째 고루틴이 첫 번째 고루틴의 두 락 작업 사이에 끼어든다면, 두 고루틴 모두 누수됩니다.

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

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#18101]|[pull request]|[patch]| 리소스 | 이중 잠금 (Double Locking) |

[cockroach#18101]:(cockroach18101_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/18101/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/18101

### 설명

`context.Done()` 신호는 reader 고루틴을 단락(short-circuit)시키지만, sender들은 그렇지 않아 리소스 누수(leak)가 발생합니다.

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
|[cockroach#2448]|[pull request]|[patch]| 통신 | 채널 |

[cockroach#2448]:(cockroach2448_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/2448/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/2448

### 설명

이 버그는 두 개의 goroutine이 서로의 채널 차단(block)이 해제되기를 기다릴 때 발생합니다:

1) `MultiRaft`가 멤버십 변경(Membership change)에 대한 커밋 이벤트를 전송합니다.
2) `store.processRaft`가 이를 받아 처리를 시작합니다.
3) 다른 명령어가 커밋되어 또 다른 `sendEvent`를 트리거하지만, `store.processRaft`가 다음 `select`를 수행할 준비가 되지 않았기 때문에 이 작업은 블록(block)됩니다. 결과적으로 메인 `MultiRaft` 루프 또한 이를 기다리게 됩니다.
4) 멤버십 변경 사항이 레인지(range)에 적용되었고, 이제 스토어가 콜백을 실행하려고 시도합니다.
5) 콜백이 `callbackChan`에 쓰기를 시도하지만, 이는 `MultiRaft` 루프에서 소비합니다. 그런데 `MultiRaft` 루프는 현재 `store.processRaft`가 이벤트 채널에서 데이터를 소비하기를 기다리고 있으며, `store.processRaft`는 콜백이 완료된 후에야 이 작업을 수행합니다.

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

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#24808]|[pull request]|[patch]| 통신 | 채널 |

[cockroach#24808]:(cockroach24808_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/24808/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/24808

### 설명

`Compactor`를 `Start`할 때, 이미 `Suggestions`를 수신했을 수 있으며, 이로 인해 가득 찬 채널에 대해 이전에 블로킹되었던 쓰기 작업이 누수(leak)될 수 있습니다.

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

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#25456]|[pull request]|[patch]| Communication | Channel |

[cockroach#25456]:(cockroach25456_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/25456/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/25456

### 설명

`CheckConsistency` (전체 코드 내)가 에러를 반환할 때, 큐는 해당 에러를 로그로 남길 가치가 있는지 결정하기 위해 스토어가 드레이닝(draining) 중인지 확인합니다. 이 확인 과정에 오류가 있어 스토어가 실제로 드레이닝을 시작할 때까지 블록(block)되는 문제가 있었습니다.

### 실행 예시

```go
G1
---------------------------------------
...
<-repl.store.Stopper().ShouldQuiesce()
---------------G1 leaks----------------
```

## Cockroach/35073

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#35073]|[pull request]|[patch]| 통신 | 채널 |

[cockroach#35073]:(cockroach35073_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/35073/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/35073

### 설명

이전에는 outbox가 시작 중에 실패했을 때 `RowChannel`을 닫지 않을 수 있었습니다. 이는 드문 경우지만 채널 통신 불일치로 인해 goroutine 누수로 이어질 수 있었습니다.

### 실행 예시

## Cockroach/35931

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#35931]|[pull request]|[patch]| Communication | Channel |

[cockroach#35931]:(cockroach35931_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/35931/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/35931

### 설명

이전에는 여러 입력으로부터 데이터를 읽는 프로세서가 하나의 입력으로부터 더 많은 데이터를 기다리는 동안 다른 입력이 가득 차 있고, 두 입력 모두 inbound 스트림에 연결되어 있는 경우, 플로우 취소(flow cancellation) 중에 취소 메타데이터 메시지를 플로우 내부로 전파하려 할 때 고루틴 누수(goroutine leak)가 발생할 가능성이 있었습니다. 취소 메서드는 각 inbound 스트림에 메타데이터 메시지를 한 번에 하나씩 썼기 때문에, 첫 번째 스트림이 가득 차 있으면 취소 프로세스가 차단(block)되어 실제로 읽기 작업이 수행되고 있던 두 번째 스트림에 취소 메시지를 전혀 보내지 못하는 상황이 발생했습니다.

### 실행 예시

## Cockroach/3710

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#3710]|[pull request]|[patch]| Resource | RWR Deadlock |

[cockroach#3710]:(cockroach3710_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/3710/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/3710

### 설명

고루틴 누수(goroutine leak)는 호출 체인 내에서 `RLock`을 두 번 획득함으로써 발생합니다.
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

루프 내의 `break` 이전에 `mu.Unlock()` 호출이 누락되었습니다.

### 실행 예시

```go
G1
---------------------------
g.bootstrap()
g.mu.Lock() [L1]
if g.closed { ==> break
g.manage()
g.mu.Lock() [L1]
----------G1 누수---------
```

## Cockroach/6181

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#6181]|[pull request]|[patch]| Resource | RWR Deadlock |

[cockroach#6181]:(cockroach6181_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/6181/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/6181

### 설명

동일한 `RWMutex`를 읽기와 쓰기 모두에 대해 재귀적으로 획득할 수 있습니다.

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
-----------------------------------G2,G3,... 누수(leak)----------------------------------------------
```

## Cockroach/7504

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#7504]|[pull request]|[patch]| Resource | AB-BA Deadlock |

[cockroach#7504]:(cockroach7504_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/7504/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/7504

### 설명

`Release()`에서는 락을 `leaseState`와 `tableNameCache` 순으로 획득하지만, `AcquireByName`에서는 `tableNameCache`와 `leaseState` 순으로 획득하여 AB-BA 데드락이 발생합니다.

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

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[cockroach#9935]|[pull request]|[patch]| Resource | Double Locking |

[cockroach#9935]:(cockroach9935_test.go)
[patch]:https://github.com/cockroachdb/cockroach/pull/9935/files
[pull request]:https://github.com/cockroachdb/cockroach/pull/9935

### 설명

이 버그는 `l.mu.Lock()`을 두 번 호출하여 발생합니다.

### 실행 예시

## Etcd/10492

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[etcd#10492]|[pull request]|[patch]| Resource | Double locking |

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

`r.acquire()`가 실패 경로(42행)에서 `r.client.mu.RLock()`을 보유한 채로 반환됩니다.
이로 인해 `client.Close()`를 호출할 때마다 고루틴 누수(leak)가 발생합니다.

## Etcd/6708

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[etcd#6708]|[pull request]|[patch]| 리소스 | 이중 잠금 (Double locking) |

[etcd#6708]:(etcd6708_test.go)
[patch]:https://github.com/etcd-io/etcd/pull/6708/files
[pull request]:https://github.com/etcd-io/etcd/pull/6708

### 설명

제공해주신 텍스트가 매우 짧아 문맥 파악이 어렵지만, 기술 문서의 일부라고 가정하고 번역해 드립니다. 만약 이것이 특정 코드 라인에 대한 설명이나 로그라면 의미가 달라질 수 있습니다.

**번역:**

54행, 49 이중 잠금(double locking)

## Etcd/6857

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[etcd#6857]|[pull request]|[patch]| Communication | Channel |

[etcd#6857]:(etcd6857_test.go)
[patch]:https://github.com/etcd-io/etcd/pull/6857/files
[pull request]:https://github.com/etcd-io/etcd/pull/6857

### 설명

`select` 문에서 다른 케이스(`n.stop`)가 선택되면 `n.status`로 데이터를 보낼 때 고루틴 누수(goroutine leaks)가 발생합니다.

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

이 고루틴 누수(goroutine leak)는 한 고루틴이 락(lock)을 획득한 상태에서 상대방이 없는 채널 작업으로 인해 블록(blocked)되고, 동시에 다른 고루틴이 동일한 락을 획득하려고 시도할 때 발생합니다.

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

이 고루틴 누수(goroutine leak)는 한 고루틴이 락(lock)을 획득한 상태에서 파트너가 없는 채널 작업으로 인해 블록(blocked)되고, 그 사이 다른 고루틴이 동일한 락을 획득하려고 시도할 때 발생합니다.

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

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[etcd#7902]|[pull request]|[patch]| Mixed | Channel & Lock |

[etcd#7902]:(etcd7902_test.go)
[patch]:https://github.com/etcd-io/etcd/pull/7902/files
[pull request]:https://github.com/etcd-io/etcd/pull/7902

### 설명

만약 follower 고루틴이 `mu.Lock()`을 먼저 획득하고 `rc.release()`를 호출하면, `rcNextc`로 전송하는 과정에서 블록(block)됩니다.
오직 leader만이 `close(nextc)`를 호출하여 follower의 블록을 해제할 수 있습니다.
하지만 `rc.release()`를 호출하기 위해서는 leader가 `mu.Lock()`을 획득해야 합니다.
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

이 누수에는 두 개의 goroutine이 관여하고 있습니다. 메인 goroutine은 `case <- donec`에서 차단되어 두 번째 goroutine이 채널을 닫기를 기다리고 있습니다.

두 번째 goroutine은 메인 goroutine에 의해 생성되었습니다. 이 goroutine은 `recvBufferRead.Read()`를 호출하는 `stream.Read()`를 호출할 때 차단됩니다. 두 번째 goroutine은 `case i := r.recv.get()`에서 차단되어 있으며, 누군가 이 채널로 메시지를 보내기를 기다리고 있습니다.

메인 goroutine에 의해 호출되는 `client.CloseSream()` 메서드가 이 메시지를 보내야 하지만, 그렇게 하지 않고 있습니다. 패치는 이 메시지를 전송하도록 하는 것입니다.

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

`cc.lbWatcher`를 실행하는 goroutine이 `done` 채널을 비우지(drain) 않고 반환됩니다.

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

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[grpc#1460]|[pull request]|[patch]| Mixed | Channel & Lock |

[grpc#1460]:(grpc1460_test.go)
[patch]:https://github.com/grpc/grpc-go/pull/1460/files
[pull request]:https://github.com/grpc/grpc-go/pull/1460

### 설명

gRPC keepalive가 활성화되어 있고(현재 기본 설정은 아님), `PermitWithoutStream`이 `false`(기본값)인 경우, 클라이언트가 활성 스트림이 없는 상태에서 활성 스트림이 있는 상태로 전환될 때 goroutine 누수가 발생할 수 있습니다. `keepalive()` goroutine은 `<-t.awakenKeepalive`에서 멈춰 있고, 메인 goroutine은 `NewStream()`의 `t.mu.Lock()`에서 멈추게 됩니다.

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

65번 라인은 unlock이 누락된 실행 경로입니다.

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

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[grpc#795]|[pull request]|[patch]| Resource | Double locking |

[grpc#795]:(grpc795_test.go)
[patch]:https://github.com/grpc/grpc-go/pull/795/files
[pull request]:https://github.com/grpc/grpc-go/pull/795

### 설명

20번 라인은 unlock이 누락된 실행 경로입니다.

## Grpc/862

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[grpc#862]|[pull request]|[patch]| Communication | Channel & Context |

[grpc#862]:(grpc862_test.go)
[patch]:https://github.com/grpc/grpc-go/pull/862/files
[pull request]:https://github.com/grpc/grpc-go/pull/862

### 설명

반환 값 `conn`이 `nil`인 경우, `cc(ClientConn)`가 닫히지 않습니다.
`resetAddrConn`을 실행하는 goroutine이 누수됩니다. 패치는 `defer func()`에서 `ClientConn`을 닫는 것입니다.

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

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[hugo#3251]|[pull request]|[patch]| Resource | RWR deadlock |

[hugo#3251]:(hugo3251_test.go)
[patch]:https://github.com/gohugoio/hugo/pull/3251/files
[pull request]:https://github.com/gohugoio/hugo/pull/3251

### 설명

고루틴이 20번 라인에서 `Lock()`을 보유한 상태로 29번 라인에서 `RLock()`을 획득하려고 할 수 있습니다. 20번 라인의 `Lock()`이 절대 해제되지 않기 때문에, 29번 라인의 `RLock()`은 결코 획득될 수 없습니다.

### 실행 예시

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
|[hugo#5379]|[pull request]|[patch]| Resource | Double locking |

[hugo#5379]:(hugo5379_test.go)
[patch]:https://github.com/gohugoio/hugo/pull/5379/files
[pull request]:https://github.com/gohugoio/hugo/pull/5379

### 설명

고루틴이 먼저 99행에서 `contentInitMu`를 획득한 다음, 66행에서 동일한 `Mutex`를 획득합니다.

## Istio/16224

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[istio#16224]|[pull request]|[patch]| Mixed | Channel & Lock |

[istio#16224]:(istio16224_test.go)
[patch]:https://github.com/istio/istio/pull/16224/files
[pull request]:https://github.com/istio/istio/pull/16224

### 설명

고루틴(goroutine)이 91행에서 `Mutex`를 보유한 상태로 93행에서 블록(blocked)됩니다.
또 다른 고루틴이 101행에서 동일한 `Mutex`를 획득하려고 시도하며, 103행에서 동일한 채널을 추가로 비우려고(drain) 합니다.

## Istio/17860

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[istio#17860]|[pull request]|[patch]| 통신 | 채널 |

[istio#17860]:(istio17860_test.go)
[patch]:https://github.com/istio/istio/pull/17860/files
[pull request]:https://github.com/istio/istio/pull/17860

### 설명

70행에서 `a.statusCh`를 비울(drain) 수 없습니다.

## Istio/18454

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[istio#18454]|[pull request]|[patch]| Communication | Channel & Context |

[istio#18454]:(istio18454_test.go)
[patch]:https://github.com/istio/istio/pull/18454/files
[pull request]:https://github.com/istio/istio/pull/18454

### 설명

56행과 61행의 `s.timer.Stop()`은 동시에 호출될 수 있습니다
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

고루틴 1은 고루틴 3이 보유한 락(lock)으로 인해 차단된 상태이며,
동시에 고루틴 3은 고루틴 1이 읽는 `ch`로 메시지를 보내는 작업으로 인해 차단된 상태입니다.

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

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#11298]|[pull request]|[patch]| Communication | Channel & Condition Variable |

[kubernetes#11298]:(kubernetes11298_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/11298/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/11298

### 설명

`n.node`는 `n.lock`을 하위 락커(locker)로 사용했습니다. 서비스 루프가 처음에 이를 잠갔고, `Notify` 함수가 `n.node.Signal()`을 호출하기 전에 이를 다시 잠그려 시도하면서 고루틴 누수(goroutine leak)가 발생했습니다. 59행과 81행의 `n.cond.Signal()`은 56행의 `n.cond.Wait`가 차단 해제되는 것을 보장하지 않습니다.

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

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#1321]|[pull request]|[patch]| Mixed | Channel & Lock |

[kubernetes#1321]:(kubernetes1321_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/1321/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/1321

### 설명

이것은 lock-channel 버그입니다. 첫 번째 고루틴은 `m.lock.Lock()`을 보유한 상태에서 `distribute()`를 호출하며, `w.result`로 메시지를 보내는 과정에서 블로킹됩니다. 두 번째 고루틴은 `stopWatching()` 함수를 호출하는데, 이 함수는 `w.result`를 닫음으로써 첫 번째 고루틴의 블로킹을 해제할 수 있습니다. 하지만 `w.result`를 닫기 위해서 `stopWatching()` 함수는 `m.lock.Lock()`을 획득해야 합니다.

해결 방법은 또 다른 채널을 도입하고, `w.result`와 동일한 `select` 문에서 두 번째 채널로부터 메시지를 수신하도록 하는 것입니다. 두 번째 채널을 닫으면 `m.lock.Lock()`을 유지할 필요 없이 첫 번째 goroutine의 블록을 해제할 수 있습니다.

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
---------------G1,G2 leak---------------------
```

## Kubernetes/25331

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#25331]|[pull request]|[patch]| Communication | Channel & Context |

[kubernetes#25331]:(kubernetes25331_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/25331/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/25331

### 설명

에러가 발생하여 `resultChan`이 차단된 상태에서 `Stop()`의 컨텍스트를 취소할 때, 잠재적인 고루틴 누수(goroutine leak)가 발생할 수 있습니다.

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

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#26980]|[pull request]|[patch]| Mixed | Channel & Lock |

[kubernetes#26980]:(kubernetes26980_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/26980/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/26980

### 설명

한 고루틴이 24행에서 `Mutex`를 보유한 상태로 35행에서 차단(blocked)되었습니다.
다른 고루틴은 동일한 `Mutex`를 획득하려다 58행에서 차단되었습니다.

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

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#38669]|[pull request]|[patch]| Communication | Channel |

[kubernetes#38669]:(kubernetes38669_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/38669/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/38669

### 설명

입력된 내용이 없어 번역할 텍스트가 없습니다. 번역이 필요한 영문 Markdown 내용을 제공해 주시면, 지침에 따라 정확하게 한국어로 번역해 드리겠습니다.

## Kubernetes/5316

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#5316]|[pull request]|[patch]| Communication | Channel |

[kubernetes#5316]:(kubernetes5316_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/5316/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/5316

### 설명

메인 고루틴이 채널을 소비하지 않는 케이스를 선택하면, 익명 고루틴은 채널로 전송하는 단계에서 블록(blocked)됩니다.

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
|[kubernetes#58107]|[pull request]|[patch]| Resource | RWR deadlock |

[kubernetes#58107]:(kubernetes58107_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/58107/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/58107

### 설명

읽기 및 쓰기 잠금(read and write lock) 규칙: 동시 읽기 잠금을 허용하며, 쓰기 잠금이 읽기 잠금보다 높은 우선순위를 갖습니다.

이 버그에는 두 개의 큐(queue 1 및 queue 2)가 관련되어 있으며, 두 큐는 동일한 읽기-쓰기 잠금(`rq.workerLock.RLock()`)으로 보호됩니다. queue 1 또는 queue 2에서 요소를 가져오기 전에 `rq.workerLock.RLock()`을 획득합니다. 만약 큐가 비어 있다면, `cond.Wait()`가 호출됩니다. 주기적으로 `rq.workerLock.Lock()`을 호출하는 또 다른 고루틴(goroutine D)이 존재합니다. 다음과 같은 상황에서 데드락(deadlock)이 발생합니다. Queue 1이 비어 있어 일부 고루틴들이 `rq.workerLock.RLock()`을 보유한 채 `cond.Wait()`에서 블록됩니다. Goroutine D는 `rq.workerLock.Lock()`을 획득하려 할 때 블록됩니다. 일부 고루틴들이 queue 2의 작업을 처리하려고 시도하지만, 쓰기 잠금(write lock)이 더 높은 우선순위를 가지므로 `rq.workerLock.RLock()`을 획득하려 할 때 블록됩니다.

해결 방법은 큐에서 데이터를 가져오는 동안 `rq.workerLock.RLock()`을 획득하지 않는 것입니다. 따라서 고루틴이 `cond.Wait()`에서 블록될 때, `rq.workLock.RLock()`은 유지되지 않습니다.

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

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[kubernetes#62464]|[pull request]|[patch]| Resource | RWR deadlock |

[kubernetes#62464]:(kubernetes62464_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/62464/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/62464

### 설명

이것은 재귀적 읽기 잠금(recursive read lock) 버그의 또 다른 예시입니다. Go 개발자들은 동일한 스레드 내에서 `RLock`을 재귀적으로 사용해서는 안 된다는 점을 인지해 왔습니다.

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
|[kubernetes#6632]|[pull request]|[patch]| 혼합 (Mixed) | 채널 및 락 (Channel & Lock) |

[kubernetes#6632]:(kubernetes6632_test.go)
[patch]:https://github.com/kubernetes/kubernetes/pull/6632/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/6632

### 설명

`resetChan`이 가득 찼을 때, `WriteFrame`은 락(lock)을 보유한 상태에서 채널에서 블록(block)됩니다. 그러면 `WriteFrame`이 이미 락을 보유하고 있기 때문에 `monitor()`가 `resetChan`을 닫는 데 실패하게 됩니다.

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
|[kubernetes#70277]|[pull request]|[patch]| 통신 | 채널 |

[kubernetes#70277]:kubernetes70277_test.go
[patch]:https://github.com/kubernetes/kubernetes/pull/70277/files
[pull request]:https://github.com/kubernetes/kubernetes/pull/70277

### 설명

`wait.poller()`는 `WaitFunc` 타입의 함수를 반환합니다.
이 함수는 고루틴을 생성하며, 해당 고루틴은 `after`가 만료되거나 `done`이 닫힌 후에만 종료됩니다.

70행에 정의된 `doneCh`가 닫히지 않습니다.

## Moby/17176

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[moby#17176]|[pull request]|[patch]| 리소스 | 이중 잠금 (Double locking) |

[moby#17176]:(moby17176_test.go)
[patch]:https://github.com/moby/moby/pull/17176/files
[pull request]:https://github.com/moby/moby/pull/17176

### 설명

`devices.nrDeletedDevices`는 `devices.Lock()`을 호출하지만, 삭제된 장치가 없는 경우 이를 해제하지 않습니다 (36행). 이는 `devices.Lock()`을 획득하려는 다른 고루틴들을 차단하게 됩니다.

## Moby/21233

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[moby#21233]|[pull request]|[patch]| Communication | Channel |

[moby#21233]:(moby21233_test.go)
[patch]:https://github.com/moby/moby/pull/21233/files
[pull request]:https://github.com/moby/moby/pull/21233

### 설명

이 테스트는 생성된 모든 진행 상황 업데이트(progress update)를 수신하는지 확인하고 있었습니다. 하지만 이러한 중간 진행 상황 업데이트의 전달은 보장되지 않습니다. 이전 업데이트가 아직 채널로 전송되지 않은 경우, 새로운 업데이트가 이전 업데이트를 덮어쓸 수 있습니다.

`t.Fatalf` 호출이 채널을 소비하고 있던 현재 goroutine을 종료시켰으며, 이로 인해 적절한 실패 메시지가 출력되는 대신 데드락(deadlock)이 발생하고 결국 테스트 타임아웃으로 이어졌습니다.

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
|[moby#25384]|[pull request]|[patch]| Mixed | Misuse WaitGroup |

[moby#25384]:(moby25384_test.go)
[patch]:https://github.com/moby/moby/pull/25384/files
[pull request]:https://github.com/moby/moby/pull/25384

### 설명

`n=1`인 경우(`n`은 `len(pm.plugins)`), `group.Wait()`의 위치는 중요하지 않습니다.
`n > 1`인 경우, `group.Wait()`는 매 반복(iteration)마다 호출됩니다. `group.Wait()`가 호출될 때마다, 이는 `group.Done()`이 `n`번 실행될 때까지 대기합니다.
하지만, `group.Done()`은 한 번의 반복에서 단 한 번만 실행됩니다.

# sync.WaitGroup 오용 사례

`sync.WaitGroup`은 Go에서 여러 고루틴이 완료될 때까지 기다려야 할 때 사용하는 매우 유용한 도구입니다. 하지만 잘못 사용하면 데드락(deadlock)이나 패닉(panic)과 같은 심각한 런타임 오류가 발생할 수 있습니다.

다음은 흔히 발생하는 오용 사례와 그 해결 방법입니다.

## 1. 고루틴 내부에서 Add 호출

가장 흔한 실수 중 하나는 `Add` 메서드를 고루틴 내부에서 호출하는 것입니다.

### 잘못된 코드 (Wrong)

```go
func main() {
    var wg sync.WaitGroup
    for i := 0; i < 3; i++ {
        go func(i int) {
            wg.Add(1) // 잘못됨: 고루틴 내부에서 Add 호출
            defer wg.Done()
            fmt.Println("Worker", i)
        }(i)
    }
    wg.Wait()
}
```

**문제점:** `wg.Wait()`가 호출되는 시점에 아직 고루틴들이 스케줄링되지 않아 `wg.Add(1)`이 실행되지 않았을 수 있습니다. 이 경우 `Wait()`는 기다릴 작업이 없다고 판단하여 즉시 종료되고, 메인 함수가 끝나면서 실행 중인 고루틴들이 강제 종료됩니다.

### 올바른 코드 (Right)

```go
func main() {
    var wg sync.WaitGroup
    for i := 0; i < 3; i++ {
        wg.Add(1) // 올바름: 고루틴 시작 전에 Add 호출
        go func(i int) {
            defer wg.Done()
            fmt.Println("Worker", i)
        }(i)
    }
    wg.Wait()
}
```

---

## 2. WaitGroup 복사 전달

`sync.WaitGroup`은 내부적으로 상태를 추적하는 카운터를 가지고 있으며, 이 상태는 복사되어서는 안 됩니다.

### 잘못된 코드 (Wrong)

```go
func worker(wg sync.WaitGroup) { // 잘못됨: 값으로 전달 (복사 발생)
    defer wg.Done()
    fmt.Println("Working...")
}

func main() {
    var wg sync.WaitGroup
    wg.Add(1)
    go worker(wg) 
    wg.Wait()
}
```

**문제점:** `worker` 함수에 `wg`를 값으로 전달하면 `WaitGroup`의 복사본이 생성됩니다. 고루틴 내부에서 `wg.Done()`을 호출하면 복사본의 카운터만 감소하고, `main` 함수에 있는 원본 `wg`의 카운터는 그대로 유지됩니다. 이로 인해 `wg.Wait()`는 영원히 기다리게 되어 **데드락(deadlock)**이 발생합니다.

### 올바른 코드 (Right)

```go
func worker(wg *sync.WaitGroup) { // 올바름: 포인터로 전달
    defer wg.Done()
    fmt.Println("Working...")
}

func main() {
    var wg sync.WaitGroup
    wg.Add(1)
    go worker(&wg) 
    wg.Wait()
}
```

---

## 3. 음수 카운터 (Negative Counter)

`Add`에 음수를 전달하거나, `Add`로 추가한 횟수보다 `Done`을 더 많이 호출하면 패닉이 발생합니다.

### 잘못된 코드 (Wrong)

```go
func main() {
    var wg sync.WaitGroup
    
    wg.Done() // 패닉 발생: panic: sync: negative WaitGroup counter
}
```

**해결 방법:** 항상 `Add` 호출 횟수와 `Done` 호출 횟수가 일치하는지 확인하십시오. `defer wg.Done()`을 사용하는 것이 가장 안전한 방법입니다.

---

## 요약 체크리스트

| 체크 항목 | 권장 사항 | 이유 |
| :--- | :--- | :--- |
| **Add 호출 위치** | 고루틴 외부(시작 전)에서 호출 | 레이스 컨디션 및 조기 종료 방지 |
| **전달 방식** | 항상 포인터(`*sync.WaitGroup`)로 전달 | 상태 복사로 인한 데드락 방지 |
| **Done 호출** | `defer wg.Done()` 사용 | 함수 종료 시 확실한 카운터 감소 보장 |
| **카운터 일치** | `Add(n)` $\rightarrow$ `Done()` $n$번 호출 | 음수 카운터로 인한 런타임 패닉 방지 |

## Moby/27782

| Bug ID | Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[moby#27782]|[pull request]|[patch]| 통신 (Communication) | 채널 및 조건 변수 (Channel & Condition Variable) |

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

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[moby#28462]|[pull request]|[patch]| Mixed | Channel & Lock |

[moby#28462]:(moby28462_test.go)
[patch]:https://github.com/moby/moby/pull/28462/files
[pull request]:https://github.com/moby/moby/pull/28462

### 설명

한 고루틴(goroutine)이 락(lock)을 획득한 상태에서 `stop` 채널로 메시지를 보내려 하고, 다른 고루틴은 동일한 락을 획득하려 할 수 있습니다. 순서가 잘못되면 두 고루틴 모두 누수(leak)됩니다.

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
----------------------G1,G2 leak------------------------------
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
|[moby#33781]|[pull request]|[patch]| Communication | Channel & Context |

[moby#33781]:(moby33781_test.go)
[patch]:https://github.com/moby/moby/pull/33781/files
[pull request]:https://github.com/moby/moby/pull/33781

### 설명

익명 함수를 사용하여 생성된 goroutine이 버퍼가 없는(unbuffered) 채널을 통해 메시지를 보내는 과정에서 블록(blocked)되었습니다. 하지만 부모 goroutine에는 부모 함수가 채널의 데이터를 소비(draining)하지 않고 반환하는 경로가 존재합니다.

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

`svm.hotRemoveVHDsAtStart()`를 호출할 때 `struct svm`의 락(lock)이 이미 잠겨 있습니다.

## Moby/4951

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[moby#4951]|[pull request]|[patch]| 리소스 | AB-BA 데드락 |

[moby#4951]:(moby4951_test.go)
[patch]:https://github.com/moby/moby/pull/4951/files
[pull request]:https://github.com/moby/moby/pull/4951

### 설명

근본 원인과 패치 내용이 커밋 설명에 명확하게 설명되어 있습니다. 글로벌 락은 `devices.Lock()`이며, 디바이스 락은 `baseInfo.lock.Lock()`입니다. 이 버그는 재현될 가능성이 매우 높습니다.

## Moby/7559

| Bug ID |  Ref | Patch | Type | Sub-type |
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

| Bug ID |  Ref | Patch | Type | Sub-type |
| ---- | ---- | ---- | ---- | ---- |
|[syncthing#4829]|[pull request]|[patch]| 리소스 | 이중 잠금 (Double locking) |

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

82행의 `<-c.dispatcherLoopStopped`는 `dispatcherLoop()`가 72행에서 블로킹되어 있기 때문에 영원히 블로킹됩니다.

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
