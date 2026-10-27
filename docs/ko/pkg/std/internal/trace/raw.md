# package internal/trace/raw

- 원문: <https://pkg.go.dev/internal/trace/raw>
- 분류: Go 표준 라이브러리

## 한국어 요약

`raw` 패키지는 Go 실행 트레이스(execution traces)를 해석하고 출력하기 위한 인터페이스를 제공합니다.

## 원문 요약

Package raw provides an interface to interpret and emit Go execution traces.

## API 상세 (go doc -all)

~~~text
package raw // import "internal/trace/raw"

Package raw provides an interface to interpret and emit Go execution traces.
It can interpret and emit execution traces in its wire format as well as a
bespoke but simple text format.

The readers and writers in this package perform no validation on or ordering
of the input, and so are generally unsuitable for analysis. However,
they're very useful for testing and debugging the tracer in the runtime and more
sophisticated trace parsers.

# Text format specification

The trace text format produced and consumed by this package is a line-oriented
format.

The first line in each text trace is the header line.

    Trace Go1.XX

Following that is a series of event lines. Each event begins with an event name,
followed by zero or more named unsigned integer arguments. Names are separated
from their integer values by an '=' sign. Names can consist of any UTF-8
character except '='.

For example:

    EventName arg1=23 arg2=55 arg3=53

Any amount of whitespace is allowed to separate each token. Whitespace is
identified via unicode.IsSpace.

Some events have additional data on following lines. There are two such special
cases.

The first special case consists of events with trailing byte-oriented data.
The trailer begins on the following line from the event. That line consists of a
single argument 'data' and a Go-quoted string representing the byte data within.
Note: an explicit argument for the length is elided, because it's just the
length of the unquoted string.

For example:

    String id=5
    	data="hello world\x00"

These events are identified in their spec by the HasData flag.

The second special case consists of stack events. These events are identified
by the IsStack flag. These events also have a trailing unsigned integer argument
describing the number of stack frame descriptors that follow. Each stack frame
descriptor is on its own line following the event, consisting of four signed
integer arguments: the PC, an integer describing the function name, an integer
describing the file name, and the line number in that file that function was at
at the time the stack trace was taken.

For example:

    Stack id=5 n=2
    	pc=1241251 func=3 file=6 line=124
    	pc=7534345 func=6 file=3 line=64

TYPES

type Event struct {
	Version version.Version
	Ev      tracev2.EventType
	Args    []uint64
	Data    []byte
}
    Event is a simple representation of a trace event.

    Note that this typically includes much more than just timestamped events,
    and it also represents parts of the trace format's framing. (But not
    interpreted.)

func (e *Event) EncodedSize() int
    EncodedSize returns the canonical encoded size of an event.

func (e *Event) String() string
    String returns the canonical string representation of the event.

    This format is the same format that is parsed by the TextReader and emitted
    by the TextWriter.

type Reader struct {
	// Has unexported fields.
}
    Reader parses trace bytes with only very basic validation into an event
    stream.

func NewReader(r io.Reader) (*Reader, error)
    NewReader creates a new reader for the trace wire format.

func (r *Reader) ReadEvent() (Event, error)
    ReadEvent reads and returns the next trace event in the byte stream.

func (r *Reader) Version() version.Version
    Version returns the version of the trace that we're reading.

type TextReader struct {
	// Has unexported fields.
}
    TextReader parses a text format trace with only very basic validation into
    an event stream.

func NewTextReader(r io.Reader) (*TextReader, error)
    NewTextReader creates a new reader for the trace text format.

func (r *TextReader) ReadEvent() (Event, error)
    ReadEvent reads and returns the next trace event in the text stream.

func (r *TextReader) Version() version.Version
    Version returns the version of the trace that we're reading.

type TextWriter struct {
	// Has unexported fields.
}
    TextWriter emits the text format of a trace.

func NewTextWriter(w io.Writer, v version.Version) (*TextWriter, error)
    NewTextWriter creates a new write for the trace text format.

func (w *TextWriter) WriteEvent(e Event) error
    WriteEvent writes a single event to the stream.

type Writer struct {
	// Has unexported fields.
}
    Writer emits the wire format of a trace.

    It may not produce a byte-for-byte compatible trace from what is produced by
    the runtime, because it may be missing extra padding in the LEB128 encoding
    that the runtime adds but isn't necessary when you know the data up-front.

func NewWriter(w io.Writer, v version.Version) (*Writer, error)
    NewWriter creates a new byte format writer.

func (w *Writer) WriteEvent(e Event) error
    WriteEvent writes a single event to the trace wire format stream.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
