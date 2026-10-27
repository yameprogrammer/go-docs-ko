# package internal/trace

- 원문: <https://pkg.go.dev/internal/trace>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package trace // import "internal/trace"


CONSTANTS

const (
	// NoTask indicates the lack of a task.
	NoTask = TaskID(^uint64(0))

	// BackgroundTask is the global task that events are attached to if there was
	// no other task in the context at the point the event was emitted.
	BackgroundTask = TaskID(0)
)
const NoGoroutine = GoID(-1)
    NoGoroutine indicates that the relevant events don't correspond to any
    goroutine in particular.

const NoProc = ProcID(-1)
    NoProc indicates that the relevant events don't correspond to any P in
    particular.

const NoThread = ThreadID(-1)
    NoThread indicates that the relevant events don't correspond to any thread
    in particular.


VARIABLES

var NoStack = Stack{}
    NoStack is a sentinel value that can be compared against any Stack value,
    indicating a lack of a stack trace.


FUNCTIONS

func IsSystemGoroutine(entryFn string) bool
func MutatorUtilizationV2(events []Event, flags UtilFlags) [][]MutatorUtil
    MutatorUtilizationV2 returns a set of mutator utilization functions for the
    given v2 trace, passed as an io.Reader. Each function will always end with 0
    utilization. The bounds of each function are implicit in the first and last
    event; outside of these bounds each function is undefined.

    If the UtilPerProc flag is not given, this always returns a single
    utilization function. Otherwise, it returns one function per P.

func RelatedGoroutinesV2(events []Event, goid GoID) map[GoID]struct{}
    RelatedGoroutinesV2 finds a set of goroutines related to goroutine goid for
    v2 traces. The association is based on whether they have synchronized with
    each other in the Go scheduler (one has unblocked another).


TYPES

type ClockSnapshot struct {
	// Trace is a snapshot of the trace clock.
	Trace Time

	// Wall is a snapshot of the system's wall clock.
	Wall time.Time

	// Mono is a snapshot of the system's monotonic clock.
	Mono uint64
}
    ClockSnapshot represents a near-simultaneous clock reading of several
    different system clocks. The snapshot can be used as a reference to convert
    timestamps to different clocks, which is helpful for correlating timestamps
    with data captured by other tools.

type Event struct {
	// Has unexported fields.
}
    Event represents a single event in the trace.

func MakeEvent[T EventDetails](c EventConfig[T]) (e Event, err error)
    MakeEvent creates a new trace event from the given configuration.

func (e Event) Experimental() ExperimentalEvent
    Experimental returns a view of the raw event for an experimental event.

    Panics if Kind != EventExperimental.

func (e Event) Goroutine() GoID
    Goroutine returns the ID of the goroutine that was executing when this event
    happened. It describes part of the execution context for this event.

    Note that for goroutine state transitions this always refers to the state
    before the transition. For example, if a goroutine is just starting
    to run on this thread and/or proc, then this will return NoGoroutine.
    In this case, the goroutine starting to run will be can be found at
    Event.StateTransition().Resource.

func (e Event) Kind() EventKind
    Kind returns the kind of event that this is.

func (e Event) Label() Label
    Label returns details about a Label event.

    Panics if Kind != EventLabel.

func (e Event) Log() Log
    Log returns details about a Log event.

    Panics if Kind != EventLog.

func (e Event) Metric() Metric
    Metric returns details about a Metric event.

    Panics if Kind != EventMetric.

func (e Event) Proc() ProcID
    Proc returns the ID of the proc this event event pertains to.

    Note that for proc state transitions this always refers to the state before
    the transition. For example, if a proc is just starting to run on this
    thread, then this will return NoProc.

func (e Event) Range() Range
    Range returns details about an EventRangeBegin, EventRangeActive,
    or EventRangeEnd event.

    Panics if Kind != EventRangeBegin, Kind != EventRangeActive, and Kind !=
    EventRangeEnd.

func (e Event) RangeAttributes() []RangeAttribute
    RangeAttributes returns attributes for a completed range.

    Panics if Kind != EventRangeEnd.

func (e Event) Region() Region
    Region returns details about a RegionBegin or RegionEnd event.

    Panics if Kind != EventRegionBegin and Kind != EventRegionEnd.

func (e Event) Stack() Stack
    Stack returns a handle to a stack associated with the event.

    This represents a stack trace at the current moment in time for the current
    execution context.

func (e Event) StateTransition() StateTransition
    StateTransition returns details about a StateTransition event.

    Panics if Kind != EventStateTransition.

func (e Event) String() string
    String returns the event as a human-readable string.

    The format of the string is intended for debugging and is subject to change.

func (e Event) Sync() Sync
    Sync returns details that are relevant for the following events, up to but
    excluding the next EventSync event.

func (e Event) Task() Task
    Task returns details about a TaskBegin or TaskEnd event.

    Panics if Kind != EventTaskBegin and Kind != EventTaskEnd.

func (e Event) Thread() ThreadID
    Thread returns the ID of the thread this event pertains to.

    Note that for thread state transitions this always refers to the state
    before the transition. For example, if a thread is just starting to run,
    then this will return NoThread.

    Note: tracking thread state is not currently supported, so this will always
    return a valid thread ID. However thread state transitions may be tracked in
    the future, and callers must be robust to this possibility.

func (e Event) Time() Time
    Time returns the timestamp of the event.

type EventConfig[T EventDetails] struct {
	// Time is the timestamp of the event.
	Time Time

	// Kind is the kind of the event.
	Kind EventKind

	// Goroutine is the goroutine ID of the event.
	Goroutine GoID

	// Proc is the proc ID of the event.
	Proc ProcID

	// Thread is the thread ID of the event.
	Thread ThreadID

	// Stack is the stack of the event.
	Stack Stack

	// Details is the kind specific details of the event.
	Details T
}
    EventConfig holds the data for constructing a trace event.

type EventDetails interface {
	Metric | Label | Range | StateTransition | Sync | Task | Region | Log | StackSample
}

type EventKind uint16
    EventKind indicates the kind of event this is.

    Use this information to obtain a more specific event that allows access to
    more detailed information.

const (
	EventBad EventKind = iota

	// EventKindSync is an event that indicates a global synchronization
	// point in the trace. At the point of a sync event, the
	// trace reader can be certain that all resources (e.g. threads,
	// goroutines) that have existed until that point have been enumerated.
	EventSync

	// EventMetric is an event that represents the value of a metric at
	// a particular point in time.
	EventMetric

	// EventLabel attaches a label to a resource.
	EventLabel

	// EventStackSample represents an execution sample, indicating what a
	// thread/proc/goroutine was doing at a particular point in time via
	// its backtrace.
	//
	// Note: Samples should be considered a close approximation of
	// what a thread/proc/goroutine was executing at a given point in time.
	// These events may slightly contradict the situation StateTransitions
	// describe, so they should only be treated as a best-effort annotation.
	EventStackSample

	// EventRangeBegin and EventRangeEnd are a pair of generic events representing
	// a special range of time. Ranges are named and scoped to some resource
	// (identified via ResourceKind). A range that has begun but has not ended
	// is considered active.
	//
	// EvRangeBegin and EvRangeEnd will share the same name, and an End will always
	// follow a Begin on the same instance of the resource. The associated
	// resource ID can be obtained from the Event. ResourceNone indicates the
	// range is globally scoped. That is, any goroutine/proc/thread can start or
	// stop, but only one such range may be active at any given time.
	//
	// EventRangeActive is like EventRangeBegin, but indicates that the range was
	// already active. In this case, the resource referenced may not be in the current
	// context.
	EventRangeBegin
	EventRangeActive
	EventRangeEnd

	// EvTaskBegin and EvTaskEnd are a pair of events representing a runtime/trace.Task.
	EventTaskBegin
	EventTaskEnd

	// EventRegionBegin and EventRegionEnd are a pair of events represent a runtime/trace.Region.
	EventRegionBegin
	EventRegionEnd

	// EventLog represents a runtime/trace.Log call.
	EventLog

	// EventStateTransition represents a state change for some resource.
	EventStateTransition

	// EventExperimental is an experimental event that is unvalidated and exposed in a raw form.
	// Users are expected to understand the format and perform their own validation. These events
	// may always be safely ignored.
	EventExperimental
)
func (e EventKind) String() string
    String returns a string form of the EventKind.

type ExperimentalBatch struct {
	// Thread is the ID of the thread that produced a packet of data.
	Thread ThreadID

	// Data is a packet of unparsed data all produced by one thread.
	Data []byte
}
    ExperimentalBatch represents a packet of unparsed data along with metadata
    about that packet.

type ExperimentalEvent struct {
	// Name is the name of the event.
	Name string

	// Experiment is the name of the experiment this event is a part of.
	Experiment string

	// Args lists the names of the event's arguments in order.
	Args []string

	// Has unexported fields.
}
    ExperimentalEvent presents a raw view of an experimental event's arguments
    and their names.

func (e ExperimentalEvent) ArgValue(i int) Value
    ArgValue returns a typed Value for the i'th argument in the experimental
    event.

type GoID int64
    GoID is the runtime-internal G structure's goid field. This is unique for
    each goroutine.

type GoState uint8
    GoState represents the state of a goroutine.

    New GoStates may be added in the future. Users of this type must be robust
    to that possibility.

const (
	GoUndetermined GoState = iota // No information is known about the goroutine.
	GoNotExist                    // Goroutine does not exist.
	GoRunnable                    // Goroutine is runnable but not running.
	GoRunning                     // Goroutine is running.
	GoWaiting                     // Goroutine is waiting on something to happen.
	GoSyscall                     // Goroutine is in a system call.
)
func (s GoState) Executing() bool
    Executing returns true if the state indicates that the goroutine is
    executing and bound to its thread.

func (s GoState) String() string
    String returns a human-readable representation of a GoState.

    The format of the returned string is for debugging purposes and is subject
    to change.

type GoroutineExecStats struct {
	// These stats are all non-overlapping.
	ExecTime          time.Duration
	SchedWaitTime     time.Duration
	BlockTimeByReason map[string]time.Duration
	SyscallTime       time.Duration
	SyscallBlockTime  time.Duration

	// TotalTime is the duration of the goroutine's presence in the trace.
	// Necessarily overlaps with other stats.
	TotalTime time.Duration

	// Total time the goroutine spent in certain ranges; may overlap
	// with other stats.
	RangeTime map[string]time.Duration
}
    GoroutineExecStats contains statistics about a goroutine's execution during
    a period of time.

func (s GoroutineExecStats) NonOverlappingStats() map[string]time.Duration

func (s GoroutineExecStats) UnknownTime() time.Duration
    UnknownTime returns whatever isn't accounted for in TotalTime.

type GoroutineSummary struct {
	ID           GoID
	Name         string // A non-unique human-friendly identifier for the goroutine.
	PC           uint64 // The first PC we saw for the entry function of the goroutine
	CreationTime Time   // Timestamp of the first appearance in the trace.
	StartTime    Time   // Timestamp of the first time it started running. 0 if the goroutine never ran.
	EndTime      Time   // Timestamp of when the goroutine exited. 0 if the goroutine never exited.

	// List of regions in the goroutine, sorted based on the start time.
	Regions []*UserRegionSummary

	// Statistics of execution time during the goroutine execution.
	GoroutineExecStats

	// Has unexported fields.
}
    GoroutineSummary contains statistics and execution details of a single
    goroutine. (For v2 traces.)

type Label struct {
	// Label is the label applied to some resource.
	Label string

	// Resource is the resource to which this label should be applied.
	Resource ResourceID
}
    Label provides details about a Label event.

type Log struct {
	// Task is the ID of the task this region is associated with.
	Task TaskID

	// Category is the category that was passed to runtime/trace.Log or runtime/trace.Logf.
	Category string

	// Message is the message that was passed to runtime/trace.Log or runtime/trace.Logf.
	Message string
}
    Log provides details about a Log event.

type MMUCurve struct {
	// Has unexported fields.
}
    An MMUCurve is the minimum mutator utilization curve across multiple window
    sizes.

func NewMMUCurve(utils [][]MutatorUtil) *MMUCurve
    NewMMUCurve returns an MMU curve for the given mutator utilization function.

func (c *MMUCurve) Examples(window time.Duration, n int) (worst []UtilWindow)
    Examples returns n specific examples of the lowest mutator utilization for
    the given window size. The returned windows will be disjoint (otherwise
    there would be a huge number of mostly-overlapping windows at the single
    lowest point). There are no guarantees on which set of disjoint windows this
    returns.

func (c *MMUCurve) MMU(window time.Duration) (mmu float64)
    MMU returns the minimum mutator utilization for the given time window.
    This is the minimum utilization for all windows of this duration across the
    execution. The returned value is in the range [0, 1].

func (c *MMUCurve) MUD(window time.Duration, quantiles []float64) []float64
    MUD returns mutator utilization distribution quantiles for the given window
    size.

    The mutator utilization distribution is the distribution of mean mutator
    utilization across all windows of the given window size in the trace.

    The minimum mutator utilization is the minimum (0th percentile) of this
    distribution. (However, if only the minimum is desired, it's more efficient
    to use the MMU method.)

type Metric struct {
	// Name is the name of the sampled metric.
	//
	// Names follow the same convention as metric names in the
	// runtime/metrics package, meaning they include the unit.
	// Names that match with the runtime/metrics package represent
	// the same quantity. Note that this corresponds to the
	// runtime/metrics package for the Go version this trace was
	// collected for.
	Name string

	// Value is the sampled value of the metric.
	//
	// The Value's Kind is tied to the name of the metric, and so is
	// guaranteed to be the same for metric samples for the same metric.
	Value Value
}
    Metric provides details about a Metric event.

type MutatorUtil struct {
	Time int64
	// Util is the mean mutator utilization starting at Time. This
	// is in the range [0, 1].
	Util float64
}
    MutatorUtil is a change in mutator utilization at a particular time. Mutator
    utilization functions are represented as a time-ordered []MutatorUtil.

type ProcID int64
    ProcID is the runtime-internal G structure's id field. This is unique for
    each P.

type ProcState uint8
    ProcState represents the state of a proc.

    New ProcStates may be added in the future. Users of this type must be robust
    to that possibility.

const (
	ProcUndetermined ProcState = iota // No information is known about the proc.
	ProcNotExist                      // Proc does not exist.
	ProcRunning                       // Proc is running.
	ProcIdle                          // Proc is idle.
)
func (s ProcState) Executing() bool
    Executing returns true if the state indicates that the proc is executing and
    bound to its thread.

func (s ProcState) String() string
    String returns a human-readable representation of a ProcState.

    The format of the returned string is for debugging purposes and is subject
    to change.

type Range struct {
	// Name is a human-readable name for the range.
	//
	// This name can be used to identify the end of the range for the resource
	// its scoped to, because only one of each type of range may be active on
	// a particular resource. The relevant resource should be obtained from the
	// Event that produced these details. The corresponding RangeEnd will have
	// an identical name.
	Name string

	// Scope is the resource that the range is scoped to.
	//
	// For example, a ResourceGoroutine scope means that the same goroutine
	// must have a start and end for the range, and that goroutine can only
	// have one range of a particular name active at any given time. The
	// ID that this range is scoped to may be obtained via Event.Goroutine.
	//
	// The ResourceNone scope means that the range is globally scoped. As a
	// result, any goroutine/proc/thread may start or end the range, and only
	// one such named range may be active globally at any given time.
	//
	// For RangeBegin and RangeEnd events, this will always reference some
	// resource ID in the current execution context. For RangeActive events,
	// this may reference a resource not in the current context. Prefer Scope
	// over the current execution context.
	Scope ResourceID
}
    Range provides details about a Range event.

type RangeAttribute struct {
	// Name is the human-readable name for the range.
	Name string

	// Value is the value of the attribute.
	Value Value
}
    RangeAttribute provides attributes about a completed Range.

type Reader struct {
	// Has unexported fields.
}
    Reader reads a byte stream, validates it, and produces trace events.

    Provided the trace is non-empty the Reader always produces a Sync event as
    the first event, and a Sync event as the last event. (There may also be any
    number of Sync events in the middle, too.)

func NewReader(r io.Reader) (*Reader, error)
    NewReader creates a new trace reader.

func (r *Reader) ReadEvent() (e Event, err error)
    ReadEvent reads a single event from the stream.

    If the stream has been exhausted, it returns an invalid event and io.EOF.

type Region struct {
	// Task is the ID of the task this region is associated with.
	Task TaskID

	// Type is the regionType that was passed to runtime/trace.StartRegion or runtime/trace.WithRegion.
	Type string
}
    Region provides details about a Region event.

type ResourceID struct {
	// Kind is the kind of resource this ID is for.
	Kind ResourceKind
	// Has unexported fields.
}
    ResourceID represents a generic resource ID.

func MakeResourceID[T interface{ GoID | ProcID | ThreadID }](id T) ResourceID
    MakeResourceID creates a general resource ID from a specific resource's ID.

func (r ResourceID) Goroutine() GoID
    Goroutine obtains a GoID from the resource ID.

    r.Kind must be ResourceGoroutine or this function will panic.

func (r ResourceID) Proc() ProcID
    Proc obtains a ProcID from the resource ID.

    r.Kind must be ResourceProc or this function will panic.

func (r ResourceID) String() string
    String returns a human-readable string representation of the ResourceID.

    This representation is subject to change and is intended primarily for
    debugging.

func (r ResourceID) Thread() ThreadID
    Thread obtains a ThreadID from the resource ID.

    r.Kind must be ResourceThread or this function will panic.

type ResourceKind uint8
    ResourceKind indicates a kind of resource that has a state machine.

    New ResourceKinds may be added in the future. Users of this type must be
    robust to that possibility.

const (
	ResourceNone      ResourceKind = iota // No resource.
	ResourceGoroutine                     // Goroutine.
	ResourceProc                          // Proc.
	ResourceThread                        // Thread.
)
func (r ResourceKind) String() string
    String returns a human-readable representation of a ResourceKind.

    The format of the returned string is for debugging purposes and is subject
    to change.

type Stack struct {
	// Has unexported fields.
}
    Stack represents a stack. It's really a handle to a stack and it's trivially
    comparable.

    If two Stacks are equal then their Frames are guaranteed to be identical.
    If they are not equal, however, their Frames may still be equal.

func MakeStack(frames []StackFrame) Stack
    MakeStack create a stack from a list of stack frames.

func (s Stack) Frames() iter.Seq[StackFrame]
    Frames is an iterator over the frames in a Stack.

func (s Stack) String() string
    String returns the stack as a human-readable string.

    The format of the string is intended for debugging and is subject to change.

type StackFrame struct {
	// PC is the program counter of the function call if this
	// is not a leaf frame. If it's a leaf frame, it's the point
	// at which the stack trace was taken.
	PC uint64

	// Func is the name of the function this frame maps to.
	Func string

	// File is the file which contains the source code of Func.
	File string

	// Line is the line number within File which maps to PC.
	Line uint64
}
    StackFrame represents a single frame of a stack.

type StackSample struct{}
    StackSample is used to construct StackSample events via MakeEvent. There are
    no details associated with it, use EventConfig.Stack instead.

type StateTransition struct {
	// Resource is the resource this state transition is for.
	Resource ResourceID

	// Reason is a human-readable reason for the state transition.
	Reason string

	// Stack is the stack trace of the resource making the state transition.
	//
	// This is distinct from the result (Event).Stack because it pertains to
	// the transitioning resource, not any of the ones executing the event
	// this StateTransition came from.
	//
	// An example of this difference is the NotExist -> Runnable transition for
	// goroutines, which indicates goroutine creation. In this particular case,
	// a Stack here would refer to the starting stack of the new goroutine, and
	// an (Event).Stack would refer to the stack trace of whoever created the
	// goroutine.
	Stack Stack

	// Has unexported fields.
}
    StateTransition provides details about a StateTransition event.

func MakeGoStateTransition(id GoID, from, to GoState) StateTransition
    MakeGoStateTransition creates a goroutine state transition.

func MakeProcStateTransition(id ProcID, from, to ProcState) StateTransition
    MakeProcStateTransition creates a proc state transition.

func (d StateTransition) Goroutine() (from, to GoState)
    Goroutine returns the state transition for a goroutine.

    Transitions to and from states that are Executing are special in that they
    change the future execution context. In other words, future events on the
    same thread will feature the same goroutine until it stops running.

    Panics if d.Resource.Kind is not ResourceGoroutine.

func (d StateTransition) Proc() (from, to ProcState)
    Proc returns the state transition for a proc.

    Transitions to and from states that are Executing are special in that they
    change the future execution context. In other words, future events on the
    same thread will feature the same goroutine until it stops running.

    Panics if d.Resource.Kind is not ResourceProc.

type Summarizer struct {
	// Has unexported fields.
}
    Summarizer constructs per-goroutine time statistics for v2 traces.

func NewSummarizer() *Summarizer
    NewSummarizer creates a new struct to build goroutine stats from a trace.

func (s *Summarizer) Event(ev *Event)
    Event feeds a single event into the stats summarizer.

func (s *Summarizer) Finalize() *Summary
    Finalize indicates to the summarizer that we're done processing the trace.
    It cleans up any remaining state and returns the full summary.

type Summary struct {
	Goroutines map[GoID]*GoroutineSummary
	Tasks      map[TaskID]*UserTaskSummary
}
    Summary is the analysis result produced by the summarizer.

type Sync struct {
	// N indicates that this is the Nth sync event in the trace.
	N int

	// ClockSnapshot represents a near-simultaneous clock reading of several
	// different system clocks. The snapshot can be used as a reference to
	// convert timestamps to different clocks, which is helpful for correlating
	// timestamps with data captured by other tools. The value is nil for traces
	// before go1.25.
	ClockSnapshot *ClockSnapshot

	// ExperimentalBatches contain all the unparsed batches of data for a given experiment.
	ExperimentalBatches map[string][]ExperimentalBatch
}
    Sync contains details potentially relevant to all the following events,
    up to but excluding the next EventSync event.

type Task struct {
	// ID is a unique identifier for the task.
	//
	// This can be used to associate the beginning of a task with its end.
	ID TaskID

	// ParentID is the ID of the parent task.
	Parent TaskID

	// Type is the taskType that was passed to runtime/trace.NewTask.
	//
	// May be "" if a task's TaskBegin event isn't present in the trace.
	Type string
}
    Task provides details about a Task event.

type TaskID uint64
    TaskID is the internal ID of a task used to disambiguate tasks (even if they
    are of the same type).

type ThreadID int64
    ThreadID is the runtime-internal M structure's ID. This is unique for each
    OS thread.

type Time int64
    Time is a timestamp in nanoseconds.

    It corresponds to the monotonic clock on the platform that the trace was
    taken, and so is possible to correlate with timestamps for other traces
    taken on the same machine using the same clock (i.e. no reboots in between).

    The actual absolute value of the timestamp is only meaningful in relation to
    other timestamps from the same clock.

    BUG: Timestamps coming from traces on Windows platforms are only comparable
    with timestamps from the same trace. Timestamps across traces cannot be
    compared, because the system clock is not used as of Go 1.22.

    BUG: Traces produced by Go versions 1.21 and earlier cannot be compared with
    timestamps from other traces taken on the same machine. This is because the
    system clock was not used at all to collect those timestamps.

func (t Time) Sub(t0 Time) time.Duration
    Sub subtracts t0 from t, returning the duration in nanoseconds.

type UserRegionSummary struct {
	TaskID TaskID
	Name   string

	// Region start event. Normally EventRegionBegin event or nil,
	// but can be a state transition event from NotExist or Undetermined
	// if the region is a synthetic region representing task inheritance
	// from the parent goroutine.
	Start *Event

	// Region end event. Normally EventRegionEnd event or nil,
	// but can be a state transition event to NotExist if the goroutine
	// terminated without explicitly ending the region.
	End *Event

	GoroutineExecStats
}
    UserRegionSummary represents a region and goroutine execution stats while
    the region was active. (For v2 traces.)

type UserTaskSummary struct {
	ID       TaskID
	Name     string
	Parent   *UserTaskSummary // nil if the parent is unknown.
	Children []*UserTaskSummary

	// Task begin event. An EventTaskBegin event or nil.
	Start *Event

	// End end event. Normally EventTaskEnd event or nil.
	End *Event

	// Logs is a list of EventLog events associated with the task.
	Logs []*Event

	// List of regions in the task, sorted based on the start time.
	Regions []*UserRegionSummary

	// Goroutines is the set of goroutines associated with this task.
	Goroutines map[GoID]*GoroutineSummary
}
    UserTaskSummary represents a task in the trace.

func (s *UserTaskSummary) Complete() bool
    Complete returns true if we have complete information about the task from
    the trace: both a start and an end.

func (s *UserTaskSummary) Descendents() []*UserTaskSummary
    Descendents returns a slice consisting of itself (always the first task
    returned), and the transitive closure of all of its children.

type UtilFlags int
    UtilFlags controls the behavior of MutatorUtilization.

const (
	// UtilSTW means utilization should account for STW events.
	// This includes non-GC STW events, which are typically user-requested.
	UtilSTW UtilFlags = 1 << iota
	// UtilBackground means utilization should account for
	// background mark workers.
	UtilBackground
	// UtilAssist means utilization should account for mark
	// assists.
	UtilAssist
	// UtilSweep means utilization should account for sweeping.
	UtilSweep

	// UtilPerProc means each P should be given a separate
	// utilization function. Otherwise, there is a single function
	// and each P is given a fraction of the utilization.
	UtilPerProc
)
type UtilWindow struct {
	Time int64
	// MutatorUtil is the mean mutator utilization in this window.
	MutatorUtil float64
}
    UtilWindow is a specific window at Time.

type Value struct {
	// Has unexported fields.
}
    Value is a dynamically-typed value obtained from a trace.

func StringValue(s string) Value
    StringValue creates a value of kind ValueString.

func Uint64Value(x uint64) Value
    Uint64Value creates a value of kind ValueUint64.

func (v Value) Kind() ValueKind
    Kind returns the ValueKind of the value.

    It represents the underlying structure of the value.

    New ValueKinds may be added in the future. Users of this type must be robust
    to that possibility.

func (v Value) String() string
    String returns the string value for a ValueString, and otherwise a string
    representation of the value for other kinds of values.

func (v Value) Uint64() uint64
    Uint64 returns the uint64 value for a ValueUint64.

    Panics if this Value's Kind is not ValueUint64.

type ValueKind uint8
    ValueKind is the type of a dynamically-typed value from a trace.

const (
	ValueBad ValueKind = iota
	ValueUint64
	ValueString
)
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
