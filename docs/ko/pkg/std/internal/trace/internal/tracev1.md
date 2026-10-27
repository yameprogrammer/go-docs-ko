# package internal/trace/internal/tracev1

- 원문: <https://pkg.go.dev/internal/trace/internal/tracev1>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `tracev1`는 1.11–1.21 버전의 Go 실행 추적을 위한 파서를 구현합니다.

## 원문 요약

Package tracev1 implements a parser for Go execution traces from versions 1.11–1.21.

## API 상세 (go doc -all)

~~~text
package tracev1 // import "internal/trace/internal/tracev1"

Package tracev1 implements a parser for Go execution traces from versions
1.11–1.21.

The package started as a copy of Go 1.19's internal/trace, but has been
optimized to be faster while using less memory and fewer allocations. It has
been further modified for the specific purpose of converting traces to the new
1.22+ format.

CONSTANTS

const (
	// Special P identifiers:
	FakeP    = 1000000 + iota
	TimerP   // contains timer unblocks
	NetpollP // contains network unblocks
	SyscallP // contains returns from syscalls
	GCP      // contains GC state
	ProfileP // contains recording of CPU profile samples
)

VARIABLES

var ErrTimeOrder = errors.New("time stamps out of order")
    ErrTimeOrder is returned by Parse when the trace contains time stamps that
    do not respect actual event ordering.

var EventDescriptions = [256]struct {
	Name       string
	minVersion version.Version
	Stack      bool
	Args       []string
	SArgs      []string // string arguments
}{
	EvNone:              {"None", 5, false, []string{}, nil},
	EvBatch:             {"Batch", 5, false, []string{"p", "ticks"}, nil},
	EvFrequency:         {"Frequency", 5, false, []string{"freq"}, nil},
	EvStack:             {"Stack", 5, false, []string{"id", "siz"}, nil},
	EvGomaxprocs:        {"Gomaxprocs", 5, true, []string{"procs"}, nil},
	EvProcStart:         {"ProcStart", 5, false, []string{"thread"}, nil},
	EvProcStop:          {"ProcStop", 5, false, []string{}, nil},
	EvGCStart:           {"GCStart", 5, true, []string{"seq"}, nil},
	EvGCDone:            {"GCDone", 5, false, []string{}, nil},
	EvSTWStart:          {"GCSTWStart", 5, false, []string{"kindid"}, []string{"kind"}},
	EvSTWDone:           {"GCSTWDone", 5, false, []string{}, nil},
	EvGCSweepStart:      {"GCSweepStart", 5, true, []string{}, nil},
	EvGCSweepDone:       {"GCSweepDone", 5, false, []string{"swept", "reclaimed"}, nil},
	EvGoCreate:          {"GoCreate", 5, true, []string{"g", "stack"}, nil},
	EvGoStart:           {"GoStart", 5, false, []string{"g", "seq"}, nil},
	EvGoEnd:             {"GoEnd", 5, false, []string{}, nil},
	EvGoStop:            {"GoStop", 5, true, []string{}, nil},
	EvGoSched:           {"GoSched", 5, true, []string{}, nil},
	EvGoPreempt:         {"GoPreempt", 5, true, []string{}, nil},
	EvGoSleep:           {"GoSleep", 5, true, []string{}, nil},
	EvGoBlock:           {"GoBlock", 5, true, []string{}, nil},
	EvGoUnblock:         {"GoUnblock", 5, true, []string{"g", "seq"}, nil},
	EvGoBlockSend:       {"GoBlockSend", 5, true, []string{}, nil},
	EvGoBlockRecv:       {"GoBlockRecv", 5, true, []string{}, nil},
	EvGoBlockSelect:     {"GoBlockSelect", 5, true, []string{}, nil},
	EvGoBlockSync:       {"GoBlockSync", 5, true, []string{}, nil},
	EvGoBlockCond:       {"GoBlockCond", 5, true, []string{}, nil},
	EvGoBlockNet:        {"GoBlockNet", 5, true, []string{}, nil},
	EvGoSysCall:         {"GoSysCall", 5, true, []string{}, nil},
	EvGoSysExit:         {"GoSysExit", 5, false, []string{"g", "seq", "ts"}, nil},
	EvGoSysBlock:        {"GoSysBlock", 5, false, []string{}, nil},
	EvGoWaiting:         {"GoWaiting", 5, false, []string{"g"}, nil},
	EvGoInSyscall:       {"GoInSyscall", 5, false, []string{"g"}, nil},
	EvHeapAlloc:         {"HeapAlloc", 5, false, []string{"mem"}, nil},
	EvHeapGoal:          {"HeapGoal", 5, false, []string{"mem"}, nil},
	EvTimerGoroutine:    {"TimerGoroutine", 5, false, []string{"g"}, nil},
	EvFutileWakeup:      {"FutileWakeup", 5, false, []string{}, nil},
	EvString:            {"String", 7, false, []string{}, nil},
	EvGoStartLocal:      {"GoStartLocal", 7, false, []string{"g"}, nil},
	EvGoUnblockLocal:    {"GoUnblockLocal", 7, true, []string{"g"}, nil},
	EvGoSysExitLocal:    {"GoSysExitLocal", 7, false, []string{"g", "ts"}, nil},
	EvGoStartLabel:      {"GoStartLabel", 8, false, []string{"g", "seq", "labelid"}, []string{"label"}},
	EvGoBlockGC:         {"GoBlockGC", 8, true, []string{}, nil},
	EvGCMarkAssistStart: {"GCMarkAssistStart", 9, true, []string{}, nil},
	EvGCMarkAssistDone:  {"GCMarkAssistDone", 9, false, []string{}, nil},
	EvUserTaskCreate:    {"UserTaskCreate", 11, true, []string{"taskid", "pid", "typeid"}, []string{"name"}},
	EvUserTaskEnd:       {"UserTaskEnd", 11, true, []string{"taskid"}, nil},
	EvUserRegion:        {"UserRegion", 11, true, []string{"taskid", "mode", "typeid"}, []string{"name"}},
	EvUserLog:           {"UserLog", 11, true, []string{"id", "keyid"}, []string{"category", "message"}},
	EvCPUSample:         {"CPUSample", 19, true, []string{"ts", "p", "g"}, nil},
}

TYPES

type Event struct {
	Ts    Timestamp // timestamp in nanoseconds
	G     uint64    // G on which the event happened
	Args  [4]uint64 // event-type-specific arguments
	StkID uint32    // unique stack ID
	P     int32     // P on which the event happened (can be a real P or one of TimerP, NetpollP, SyscallP)
	Type  EventType // one of Ev*
}
    Event describes one event in the trace.

func (ev *Event) String() string

type EventType uint8

const (
	EvNone              EventType = 0  // unused
	EvBatch             EventType = 1  // start of per-P batch of events [pid, timestamp]
	EvFrequency         EventType = 2  // contains tracer timer frequency [frequency (ticks per second)]
	EvStack             EventType = 3  // stack [stack id, number of PCs, array of {PC, func string ID, file string ID, line}]
	EvGomaxprocs        EventType = 4  // current value of GOMAXPROCS [timestamp, GOMAXPROCS, stack id]
	EvProcStart         EventType = 5  // start of P [timestamp, thread id]
	EvProcStop          EventType = 6  // stop of P [timestamp]
	EvGCStart           EventType = 7  // GC start [timestamp, seq, stack id]
	EvGCDone            EventType = 8  // GC done [timestamp]
	EvSTWStart          EventType = 9  // GC mark termination start [timestamp, kind]
	EvSTWDone           EventType = 10 // GC mark termination done [timestamp]
	EvGCSweepStart      EventType = 11 // GC sweep start [timestamp, stack id]
	EvGCSweepDone       EventType = 12 // GC sweep done [timestamp, swept, reclaimed]
	EvGoCreate          EventType = 13 // goroutine creation [timestamp, new goroutine id, new stack id, stack id]
	EvGoStart           EventType = 14 // goroutine starts running [timestamp, goroutine id, seq]
	EvGoEnd             EventType = 15 // goroutine ends [timestamp]
	EvGoStop            EventType = 16 // goroutine stops (like in select{}) [timestamp, stack]
	EvGoSched           EventType = 17 // goroutine calls Gosched [timestamp, stack]
	EvGoPreempt         EventType = 18 // goroutine is preempted [timestamp, stack]
	EvGoSleep           EventType = 19 // goroutine calls Sleep [timestamp, stack]
	EvGoBlock           EventType = 20 // goroutine blocks [timestamp, stack]
	EvGoUnblock         EventType = 21 // goroutine is unblocked [timestamp, goroutine id, seq, stack]
	EvGoBlockSend       EventType = 22 // goroutine blocks on chan send [timestamp, stack]
	EvGoBlockRecv       EventType = 23 // goroutine blocks on chan recv [timestamp, stack]
	EvGoBlockSelect     EventType = 24 // goroutine blocks on select [timestamp, stack]
	EvGoBlockSync       EventType = 25 // goroutine blocks on Mutex/RWMutex [timestamp, stack]
	EvGoBlockCond       EventType = 26 // goroutine blocks on Cond [timestamp, stack]
	EvGoBlockNet        EventType = 27 // goroutine blocks on network [timestamp, stack]
	EvGoSysCall         EventType = 28 // syscall enter [timestamp, stack]
	EvGoSysExit         EventType = 29 // syscall exit [timestamp, goroutine id, seq, real timestamp]
	EvGoSysBlock        EventType = 30 // syscall blocks [timestamp]
	EvGoWaiting         EventType = 31 // denotes that goroutine is blocked when tracing starts [timestamp, goroutine id]
	EvGoInSyscall       EventType = 32 // denotes that goroutine is in syscall when tracing starts [timestamp, goroutine id]
	EvHeapAlloc         EventType = 33 // gcController.heapLive change [timestamp, heap live bytes]
	EvHeapGoal          EventType = 34 // gcController.heapGoal change [timestamp, heap goal bytes]
	EvTimerGoroutine    EventType = 35 // denotes timer goroutine [timer goroutine id]
	EvFutileWakeup      EventType = 36 // denotes that the previous wakeup of this goroutine was futile [timestamp]
	EvString            EventType = 37 // string dictionary entry [ID, length, string]
	EvGoStartLocal      EventType = 38 // goroutine starts running on the same P as the last event [timestamp, goroutine id]
	EvGoUnblockLocal    EventType = 39 // goroutine is unblocked on the same P as the last event [timestamp, goroutine id, stack]
	EvGoSysExitLocal    EventType = 40 // syscall exit on the same P as the last event [timestamp, goroutine id, real timestamp]
	EvGoStartLabel      EventType = 41 // goroutine starts running with label [timestamp, goroutine id, seq, label string id]
	EvGoBlockGC         EventType = 42 // goroutine blocks on GC assist [timestamp, stack]
	EvGCMarkAssistStart EventType = 43 // GC mark assist start [timestamp, stack]
	EvGCMarkAssistDone  EventType = 44 // GC mark assist done [timestamp]
	EvUserTaskCreate    EventType = 45 // trace.NewTask [timestamp, internal task id, internal parent id, stack, name string]
	EvUserTaskEnd       EventType = 46 // end of task [timestamp, internal task id, stack]
	EvUserRegion        EventType = 47 // trace.WithRegion [timestamp, internal task id, mode(0:start, 1:end), name string]
	EvUserLog           EventType = 48 // trace.Log [timestamp, internal id, key string id, stack, value string]
	EvCPUSample         EventType = 49 // CPU profiling sample [timestamp, stack, real timestamp, real P id (-1 when absent), goroutine id]
	EvCount             EventType = 50
)
    Event types in the trace. Verbatim copy from src/runtime/trace.go with the
    "trace" prefix removed.

type Events struct {
	// Has unexported fields.
}

func (l *Events) All() func(yield func(ev *Event) bool)

func (l *Events) Len() int

func (l *Events) Less(i, j int) bool

func (l *Events) Peek() (*Event, bool)

func (l *Events) Pop() (*Event, bool)

func (l *Events) Ptr(i int) *Event

func (l *Events) Swap(i, j int)

type Frame struct {
	PC uint64
	// string ID of the function name
	Fn uint64
	// string ID of the file name
	File uint64
	Line int
}
    Frame is a frame in stack traces.

type STWReason int

const (
	STWUnknown                 STWReason = 0
	STWGCMarkTermination       STWReason = 1
	STWGCSweepTermination      STWReason = 2
	STWWriteHeapDump           STWReason = 3
	STWGoroutineProfile        STWReason = 4
	STWGoroutineProfileCleanup STWReason = 5
	STWAllGoroutinesStackTrace STWReason = 6
	STWReadMemStats            STWReason = 7
	STWAllThreadsSyscall       STWReason = 8
	STWGOMAXPROCS              STWReason = 9
	STWStartTrace              STWReason = 10
	STWStopTrace               STWReason = 11
	STWCountPagesInUse         STWReason = 12
	STWReadMetricsSlow         STWReason = 13
	STWReadMemStatsSlow        STWReason = 14
	STWPageCachePagesLeaked    STWReason = 15
	STWResetDebugLog           STWReason = 16

	NumSTWReasons = 17
)
type Timestamp int64
    Timestamp represents a count of nanoseconds since the beginning of the
    trace. They can only be meaningfully compared with other timestamps from the
    same trace.

type Trace struct {
	Version version.Version

	// Events is the sorted list of Events in the trace.
	Events Events
	// Stacks is the stack traces (stored as slices of PCs), keyed by stack IDs
	// from the trace.
	Stacks        map[uint32][]uint64
	PCs           map[uint64]Frame
	Strings       map[uint64]string
	InlineStrings []string
}
    Trace is the result of Parse.

func Parse(r io.Reader, vers version.Version) (Trace, error)
    Parse parses Go execution traces from versions 1.11–1.21. The provided
    reader will be read to completion and the entire trace will be materialized
    in memory. That is, this function does not allow incremental parsing.

    The reader has to be positioned just after the trace header and vers
    needs to be the version of the trace. This can be achieved by using
    version.ReadHeader.

func (tr *Trace) STWReason(kindID uint64) STWReason
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
