# package internal/trace/internal/testgen

- 원문: <https://pkg.go.dev/internal/trace/internal/testgen>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package testgen // import "internal/trace/internal/testgen"


VARIABLES

var (
	NoString = ""
	NoStack  = []trace.StackFrame{}
)

FUNCTIONS

func Main(ver version.Version, f func(*Trace))

TYPES

type Batch struct {
	// Has unexported fields.
}
    Batch represents an event batch.

func (b *Batch) Event(name string, args ...any)
    Event emits an event into a batch. name must correspond to one of the names
    in Specs() result for the version that was passed to this trace. Callers
    must omit the timestamp delta.

func (b *Batch) RawEvent(typ tracev2.EventType, data []byte, args ...uint64)
    RawEvent emits an event into a batch. name must correspond to one of the
    names in Specs() result for the version that was passed to this trace.

type Generation struct {
	// Has unexported fields.
}
    Generation represents a single generation in the trace.

func (g *Generation) Batch(thread trace.ThreadID, time Time) *Batch
    Batch starts a new event batch in the trace data.

    This is convenience function for generating correct batches.

func (g *Generation) Stack(stk []trace.StackFrame) uint64
    Stack registers a stack with the trace.

    This is a convenience function for easily adding correct stacks to traces.

func (g *Generation) String(s string) uint64
    String registers a string with the trace.

    This is a convenience function for easily adding correct strings to traces.

func (g *Generation) Sync(freq uint64, time Time, mono uint64, wall time.Time)
    Sync configures the sync batch for the generation. For go1.25 and later,
    the time value is the timestamp of the EvClockSnapshot event. For earlier
    version, the time value is the timestamp of the batch containing a lone
    EvFrequency event.

type Seq uint64
    Seq represents a sequence counter.

type Time uint64
    Time represents a low-level trace timestamp (which does not necessarily
    correspond to nanoseconds, like trace.Time does).

type Trace struct {
	// Has unexported fields.
}
    Trace represents an execution trace for testing.

    It does a little bit of work to ensure that the produced trace is valid,
    just for convenience. It mainly tracks batches and batch sizes (so they're
    trivially correct), tracks strings and stacks, and makes sure emitted string
    and stack batches are valid. That last part can be controlled by a few
    options.

    Otherwise, it performs no validation on the trace at all.

func NewTrace(ver version.Version) *Trace
    NewTrace creates a new trace.

func (t *Trace) DisableTimestamps()
    DisableTimestamps makes the timestamps for all events generated after this
    call zero. Raw events are exempted from this because the caller has to pass
    their own timestamp into those events anyway.

func (t *Trace) ExpectFailure(pattern string)
    ExpectFailure writes down that the trace should be broken. The caller must
    provide a pattern matching the expected error produced by the parser.

func (t *Trace) ExpectSuccess()
    ExpectSuccess writes down that the trace should successfully parse.

func (t *Trace) Generate() []byte
    Generate creates a test file for the trace.

func (t *Trace) Generation(gen uint64) *Generation
    Generation creates a new trace generation.

    This provides more structure than Event to allow for more easily creating
    complex traces that are mostly or completely correct.

func (t *Trace) RawEvent(typ tracev2.EventType, data []byte, args ...uint64)
    RawEvent emits an event into the trace. name must correspond to one of the
    names in Specs() result for the version that was passed to this trace.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
