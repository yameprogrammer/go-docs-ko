# package internal/coverage/encodecounter

- 원문: <https://pkg.go.dev/internal/coverage/encodecounter>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package encodecounter // import "internal/coverage/encodecounter"


TYPES

type CounterVisitor interface {
	VisitFuncs(f CounterVisitorFn) error
}
    CounterVisitor describes a helper object used during counter file writing;
    when writing counter data files, clients pass a CounterVisitor to the
    write/emit routines, then the expectation is that the VisitFuncs method
    will then invoke the callback "f" with data for each function to emit to the
    file.

type CounterVisitorFn func(pkid uint32, funcid uint32, counters []uint32) error
    CounterVisitorFn describes a callback function invoked when writing coverage
    counter data.

type CoverageDataWriter struct {
	// Has unexported fields.
}

func NewCoverageDataWriter(w io.Writer, flav coverage.CounterFlavor) *CoverageDataWriter

func (cfw *CoverageDataWriter) AppendSegment(args map[string]string, visitor CounterVisitor) error
    AppendSegment appends a new segment to a counter data, with a new args
    section followed by a payload of counter data clauses.

func (cfw *CoverageDataWriter) Write(metaFileHash [16]byte, args map[string]string, visitor CounterVisitor) error
    Write writes the contents of the count-data file to the writer previously
    supplied to NewCoverageDataWriter. Returns an error if something went wrong
    somewhere with the write.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
