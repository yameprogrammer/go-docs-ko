# package internal/trace/tracev2

- 원문: <https://pkg.go.dev/internal/trace/tracev2>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package tracev2 contains definitions for the v2 execution trace wire format.

## 원문 요약

Package tracev2 contains definitions for the v2 execution trace wire format.

## API 상세 (go doc -all)

~~~text
package tracev2 // import "internal/trace/tracev2"

Package tracev2 contains definitions for the v2 execution trace wire format.

These definitions are shared between the trace parser and the runtime, so it
must not depend on any package that depends on the runtime (most packages).

CONSTANTS

const (
	// MaxBatchSize sets the maximum size that a batch can be.
	//
	// Directly controls the trace batch size in the runtime.
	//
	// NOTE: If this number decreases, the trace format version must change.
	MaxBatchSize = 64 << 10

	// Maximum number of PCs in a single stack trace.
	//
	// Since events contain only stack ID rather than whole stack trace,
	// we can allow quite large values here.
	//
	// Directly controls the maximum number of frames per stack
	// in the runtime.
	//
	// NOTE: If this number decreases, the trace format version must change.
	MaxFramesPerStack = 128

	// MaxEventTrailerDataSize controls the amount of trailer data that
	// an event can have in bytes. Must be smaller than MaxBatchSize.
	// Controls the maximum string size in the trace.
	//
	// Directly controls the maximum such value in the runtime.
	//
	// NOTE: If this number decreases, the trace format version must change.
	MaxEventTrailerDataSize = 1 << 10
)
const MaxTimedEventArgs = 5
    MaxTimedEventArgs is the maximum number of arguments for timed events.

const NumExperimentalEvents = MaxExperimentalEvent - MaxEvent

VARIABLES

var EventArgTypes = [...]string{
	"seq",
	"pstatus",
	"gstatus",
	"g",
	"m",
	"p",
	"string",
	"stack",
	"value",
	"task",
}
    EventArgTypes is a list of valid argument types for use in Args.

    See the documentation of Args for more details.


FUNCTIONS

func EventNames(specs []EventSpec) map[string]EventType
    EventNames is a helper that produces a mapping of event names to event
    types.

func Experiments() []string

TYPES

type EventSpec struct {
	// Name is the human-readable name of the trace event.
	Name string

	// Args contains the names of each trace event's argument.
	// Its length determines the number of arguments an event has.
	//
	// Argument names follow a certain structure and this structure
	// is relied on by the testing framework to type-check arguments
	// and to produce Values for experimental events.
	//
	// The structure is:
	//
	//     (?P<name>[A-Za-z]+)(_(?P<type>[A-Za-z]+))?
	//
	// In sum, it's a name followed by an optional type.
	// If the type is present, it is preceded with an underscore.
	// Arguments without types will be interpreted as just raw uint64s.
	// The valid argument types and the Go types they map to are listed
	// in the ArgTypes variable.
	Args []string

	// StringIDs indicates which of the arguments are string IDs.
	StringIDs []int

	// StackIDs indicates which of the arguments are stack IDs.
	//
	// The list is not sorted. The first index always refers to
	// the main stack for the current execution context of the event.
	StackIDs []int

	// StartEv indicates the event type of the corresponding "start"
	// event, if this event is an "end," for a pair of events that
	// represent a time range.
	StartEv EventType

	// IsTimedEvent indicates whether this is an event that both
	// appears in the main event stream and is surfaced to the
	// trace reader.
	//
	// Events that are not "timed" are considered "structural"
	// since they either need significant reinterpretation or
	// otherwise aren't actually surfaced by the trace reader.
	IsTimedEvent bool

	// HasData is true if the event has trailer consisting of a
	// varint length followed by unencoded bytes of some data.
	//
	// An event may not be both a timed event and have data.
	HasData bool

	// IsStack indicates that the event represents a complete
	// stack trace. Specifically, it means that after the arguments
	// there's a varint length, followed by 4*length varints. Each
	// group of 4 represents the PC, file ID, func ID, and line number
	// in that order.
	IsStack bool

	// Experiment indicates the ID of an experiment this event is associated
	// with. If Experiment is not NoExperiment, then the event is experimental
	// and will be exposed as an EventExperiment.
	Experiment Experiment
}
    EventSpec is a specification for a trace event. It contains sufficient
    information to perform basic parsing of any trace event for any version of
    Go.

func Specs() []EventSpec

type EventType uint8
    EventType indicates an event's type from which its arguments and semantics
    can be derived. Its representation matches the wire format's representation
    of the event types that precede all event data.

const (
	EvNone EventType = iota // unused

	// Structural events.
	EvEventBatch // start of per-M batch of events [generation, M ID, timestamp, batch length]
	EvStacks     // start of a section of the stack table [...EvStack]
	EvStack      // stack table entry [ID, ...{PC, func string ID, file string ID, line #}]
	EvStrings    // start of a section of the string dictionary [...EvString]
	EvString     // string dictionary entry [ID, length, string]
	EvCPUSamples // start of a section of CPU samples [...EvCPUSample]
	EvCPUSample  // CPU profiling sample [timestamp, M ID, P ID, goroutine ID, stack ID]
	EvFrequency  // timestamp units per sec [freq]

	// Procs.
	EvProcsChange // current value of GOMAXPROCS [timestamp, GOMAXPROCS, stack ID]
	EvProcStart   // start of P [timestamp, P ID, P seq]
	EvProcStop    // stop of P [timestamp]
	EvProcSteal   // P was stolen [timestamp, P ID, P seq, M ID]
	EvProcStatus  // P status at the start of a generation [timestamp, P ID, status]

	// Goroutines.
	EvGoCreate            // goroutine creation [timestamp, new goroutine ID, new stack ID, stack ID]
	EvGoCreateSyscall     // goroutine appears in syscall (cgo callback) [timestamp, new goroutine ID]
	EvGoStart             // goroutine starts running [timestamp, goroutine ID, goroutine seq]
	EvGoDestroy           // goroutine ends [timestamp]
	EvGoDestroySyscall    // goroutine ends in syscall (cgo callback) [timestamp]
	EvGoStop              // goroutine yields its time, but is runnable [timestamp, reason, stack ID]
	EvGoBlock             // goroutine blocks [timestamp, reason, stack ID]
	EvGoUnblock           // goroutine is unblocked [timestamp, goroutine ID, goroutine seq, stack ID]
	EvGoSyscallBegin      // syscall enter [timestamp, P seq, stack ID]
	EvGoSyscallEnd        // syscall exit [timestamp]
	EvGoSyscallEndBlocked // syscall exit and it blocked at some point [timestamp]
	EvGoStatus            // goroutine status at the start of a generation [timestamp, goroutine ID, M ID, status]

	// STW.
	EvSTWBegin // STW start [timestamp, kind, stack ID]
	EvSTWEnd   // STW done [timestamp]

	// GC events.
	EvGCActive           // GC active [timestamp, seq]
	EvGCBegin            // GC start [timestamp, seq, stack ID]
	EvGCEnd              // GC done [timestamp, seq]
	EvGCSweepActive      // GC sweep active [timestamp, P ID]
	EvGCSweepBegin       // GC sweep start [timestamp, stack ID]
	EvGCSweepEnd         // GC sweep done [timestamp, swept bytes, reclaimed bytes]
	EvGCMarkAssistActive // GC mark assist active [timestamp, goroutine ID]
	EvGCMarkAssistBegin  // GC mark assist start [timestamp, stack ID]
	EvGCMarkAssistEnd    // GC mark assist done [timestamp]
	EvHeapAlloc          // gcController.heapLive change [timestamp, heap alloc in bytes]
	EvHeapGoal           // gcController.heapGoal() change [timestamp, heap goal in bytes]

	// Annotations.
	EvGoLabel         // apply string label to current running goroutine [timestamp, label string ID]
	EvUserTaskBegin   // trace.NewTask [timestamp, internal task ID, internal parent task ID, name string ID, stack ID]
	EvUserTaskEnd     // end of a task [timestamp, internal task ID, stack ID]
	EvUserRegionBegin // trace.{Start,With}Region [timestamp, internal task ID, name string ID, stack ID]
	EvUserRegionEnd   // trace.{End,With}Region [timestamp, internal task ID, name string ID, stack ID]
	EvUserLog         // trace.Log [timestamp, internal task ID, key string ID, value string ID, stack]

	// Coroutines. Added in Go 1.23.
	EvGoSwitch        // goroutine switch (coroswitch) [timestamp, goroutine ID, goroutine seq]
	EvGoSwitchDestroy // goroutine switch and destroy [timestamp, goroutine ID, goroutine seq]
	EvGoCreateBlocked // goroutine creation (starts blocked) [timestamp, new goroutine ID, new stack ID, stack ID]

	// GoStatus with stack. Added in Go 1.23.
	EvGoStatusStack // goroutine status at the start of a generation, with a stack [timestamp, goroutine ID, M ID, status, stack ID]

	// Batch event for an experimental batch with a custom format. Added in Go 1.23.
	EvExperimentalBatch // start of extra data [experiment ID, generation, M ID, timestamp, batch length, batch data...]

	// Sync batch. Added in Go 1.25. Previously a lone EvFrequency event.
	EvSync          // start of a sync batch [...EvFrequency|EvClockSnapshot]
	EvClockSnapshot // snapshot of trace, mono and wall clocks [timestamp, mono, sec, nsec]

	// In-band end-of-generation signal. Added in Go 1.26.
	// Used in Go 1.25 only internally.
	EvEndOfGeneration

	NumEvents
)
    Event types in the trace, args are given in square brackets.

    Naming scheme:
      - Time range event pairs have suffixes "Begin" and "End".
      - "Start", "Stop", "Create", "Destroy", "Block", "Unblock" are suffixes
        reserved for scheduling resources.

    NOTE: If you add an event type, make sure you also update all tables in this
    file!

const (
	MaxEvent EventType = 127 + iota

	// Experimental heap span events. Added in Go 1.23.
	EvSpan      // heap span exists [timestamp, id, npages, type/class]
	EvSpanAlloc // heap span alloc [timestamp, id, npages, type/class]
	EvSpanFree  // heap span free [timestamp, id]

	// Experimental heap object events. Added in Go 1.23.
	EvHeapObject      // heap object exists [timestamp, id, type]
	EvHeapObjectAlloc // heap object alloc [timestamp, id, type]
	EvHeapObjectFree  // heap object free [timestamp, id]

	// Experimental goroutine stack events. Added in Go 1.23.
	EvGoroutineStack      // stack exists [timestamp, id, order]
	EvGoroutineStackAlloc // stack alloc [timestamp, id, order]
	EvGoroutineStackFree  // stack free [timestamp, id]

	MaxExperimentalEvent
)
    Experimental events.

func (ev EventType) Experimental() bool

type Experiment uint
    Experiment is an experiment ID that events may be associated with.

const (
	// AllocFree is the alloc-free events experiment.
	AllocFree Experiment = 1 + iota

	NumExperiments
)
    Experiments.

const NoExperiment Experiment = 0
    NoExperiment is the reserved ID 0 indicating no experiment.

type GoStatus uint8
    GoStatus is the status of a goroutine.

    They correspond directly to the various goroutine states.

const (
	GoBad GoStatus = iota
	GoRunnable
	GoRunning
	GoSyscall
	GoWaiting
)
func (s GoStatus) String() string

type ProcStatus uint8
    ProcStatus is the status of a P.

    They mostly correspond to the various P states.

const (
	ProcBad ProcStatus = iota
	ProcRunning
	ProcIdle
	ProcSyscall

	// ProcSyscallAbandoned is a special case of
	// ProcSyscall. It's used in the very specific case
	// where the first a P is mentioned in a generation is
	// part of a ProcSteal event. If that's the first time
	// it's mentioned, then there's no GoSyscallBegin to
	// connect the P stealing back to at that point. This
	// special state indicates this to the parser, so it
	// doesn't try to find a GoSyscallEndBlocked that
	// corresponds with the ProcSteal.
	ProcSyscallAbandoned
)
func (s ProcStatus) String() string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
