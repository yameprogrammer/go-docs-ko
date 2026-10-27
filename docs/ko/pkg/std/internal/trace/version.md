# package internal/trace/version

- 원문: <https://pkg.go.dev/internal/trace/version>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package version // import "internal/trace/version"


FUNCTIONS

func WriteHeader(w io.Writer, v Version) (int, error)
    WriteHeader writes a header for a trace version v to w.


TYPES

type Version uint32
    Version represents the version of a trace file.

const (
	Go111   Version = 11 // v1
	Go119   Version = 19 // v1
	Go121   Version = 21 // v1
	Go122   Version = 22 // v2
	Go123   Version = 23 // v2
	Go125   Version = 25 // v2
	Go126   Version = 26 // v2
	Current         = Go126
)
func ReadHeader(r io.Reader) (Version, error)
    ReadHeader reads the version of the trace out of the trace file's header,
    whose prefix must be present in v.

func (v Version) EventName(typ tracev2.EventType) string
    EventName returns a string name of a wire format event for a particular
    trace version.

func (v Version) Specs() []tracev2.EventSpec
    Specs returns the set of event.Specs for this version.

func (v Version) Valid() bool
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
