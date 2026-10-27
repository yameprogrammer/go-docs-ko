# package internal/coverage/decodecounter

- 원문: <https://pkg.go.dev/internal/coverage/decodecounter>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package decodecounter // import "internal/coverage/decodecounter"


TYPES

type CounterDataReader struct {
	// Has unexported fields.
}

func NewCounterDataReader(fn string, rs io.ReadSeeker) (*CounterDataReader, error)

func (cdr *CounterDataReader) BeginNextSegment() (bool, error)
    BeginNextSegment sets up the reader to read the next segment, returning TRUE
    if we do have another segment to read, or FALSE if we're done with all the
    segments (also an error if something went wrong).

func (cdr *CounterDataReader) Goarch() string
    Goarch returns the GOARCH setting in effect for the "-cover" binary that
    produced this counter data file. The GOARCH value may be empty in the case
    where the counter data file was produced from a merge in which more than one
    GOARCH value was present.

func (cdr *CounterDataReader) Goos() string
    Goos returns the GOOS setting in effect for the "-cover" binary that
    produced this counter data file. The GOOS value may be empty in the case
    where the counter data file was produced from a merge in which more than one
    GOOS value was present.

func (cdr *CounterDataReader) NextFunc(p *FuncPayload) (bool, error)
    NextFunc reads data for the next function in this current segment into "p",
    returning TRUE if the read was successful or FALSE if we've read all the
    functions already (also an error if something went wrong with the read or we
    hit a premature EOF).

func (cdr *CounterDataReader) NumFunctionsInSegment() uint32
    NumFunctionsInSegment returns the number of live functions in the currently
    selected segment.

func (cdr *CounterDataReader) NumSegments() uint32
    NumSegments returns the number of execution segments in the file.

func (cdr *CounterDataReader) OsArgs() []string
    OsArgs returns the program arguments (saved from os.Args during the run of
    the instrumented binary) read from the counter data file. Not all coverage
    data files will have os.Args values; for example, if a data file is produced
    by merging coverage data from two distinct runs, no os args will be
    available (an empty list is returned).

type FuncPayload struct {
	PkgIdx   uint32
	FuncIdx  uint32
	Counters []uint32
}
    FuncPayload encapsulates the counter data payload for a single function as
    read from a counter data file.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
