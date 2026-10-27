# package vendor/golang.org/x/text/unicode/norm

- 원문: <https://pkg.go.dev/vendor/golang.org/x/text/unicode/norm>
- 분류: Go 표준 라이브러리

## 한국어 요약

`norm` 패키지는 Unicode 문자열을 정규화하기 위한 타입과 함수들을 제공합니다.

## 원문 요약

Package norm contains types and functions for normalizing Unicode strings.

## API 상세 (go doc -all)

~~~text
package norm // import "vendor/golang.org/x/text/unicode/norm"

Package norm contains types and functions for normalizing Unicode strings.

CONSTANTS

const (
	// Version is the Unicode edition from which the tables are derived.
	Version = "17.0.0"

	// MaxTransformChunkSize indicates the maximum number of bytes that Transform
	// may need to write atomically for any Form. Making a destination buffer at
	// least this size ensures that Transform can always make progress and that
	// the user does not need to grow the buffer on an ErrShortDst.
	MaxTransformChunkSize = 35 + maxNonStarters*4
)
const GraphemeJoiner = "\u034F"
    GraphemeJoiner is inserted after maxNonStarters non-starter runes.

const MaxSegmentSize = maxByteBufferSize
    MaxSegmentSize is the maximum size of a byte buffer needed to consider any
    sequence of starter and non-starter runes for the purpose of normalization.


TYPES

type Form int
    A Form denotes a canonical representation of Unicode code points. The
    Unicode-defined normalization and equivalence forms are:

        NFC   Unicode Normalization Form C
        NFD   Unicode Normalization Form D
        NFKC  Unicode Normalization Form KC
        NFKD  Unicode Normalization Form KD

    For a Form f, this documentation uses the notation f(x) to mean the bytes or
    string x converted to the given form. A position n in x is called a boundary
    if conversion to the form can proceed independently on both sides:

        f(x) == append(f(x[0:n]), f(x[n:])...)

    References: https://unicode.org/reports/tr15/ and
    https://unicode.org/notes/tn5/.

const (
	NFC Form = iota
	NFD
	NFKC
	NFKD
)
func (f Form) Append(out []byte, src ...byte) []byte
    Append returns f(append(out, b...)). The buffer out must be nil, empty,
    or equal to f(out).

func (f Form) AppendString(out []byte, src string) []byte
    AppendString returns f(append(out, []byte(s))). The buffer out must be nil,
    empty, or equal to f(out).

func (f Form) Bytes(b []byte) []byte
    Bytes returns f(b). May return b if f(b) = b.

func (f Form) FirstBoundary(b []byte) int
    FirstBoundary returns the position i of the first boundary in b or -1 if b
    contains no boundary.

func (f Form) FirstBoundaryInString(s string) int
    FirstBoundaryInString returns the position i of the first boundary in s or
    -1 if s contains no boundary.

func (f Form) IsNormal(b []byte) bool
    IsNormal returns true if b == f(b).

func (f Form) IsNormalString(s string) bool
    IsNormalString returns true if s == f(s).

func (f Form) LastBoundary(b []byte) int
    LastBoundary returns the position i of the last boundary in b or -1 if b
    contains no boundary.

func (f Form) NextBoundary(b []byte, atEOF bool) int
    NextBoundary reports the index of the boundary between the first and next
    segment in b or -1 if atEOF is false and there are not enough bytes to
    determine this boundary.

func (f Form) NextBoundaryInString(s string, atEOF bool) int
    NextBoundaryInString reports the index of the boundary between the first and
    next segment in b or -1 if atEOF is false and there are not enough bytes to
    determine this boundary.

func (f Form) Properties(s []byte) Properties
    Properties returns properties for the first rune in s.

func (f Form) PropertiesString(s string) Properties
    PropertiesString returns properties for the first rune in s.

func (f Form) QuickSpan(b []byte) int
    QuickSpan returns a boundary n such that b[0:n] == f(b[0:n]). It is not
    guaranteed to return the largest such n.

func (f Form) QuickSpanString(s string) int
    QuickSpanString returns a boundary n such that s[0:n] == f(s[0:n]). It is
    not guaranteed to return the largest such n.

func (f Form) Reader(r io.Reader) io.Reader
    Reader returns a new reader that implements Read by reading data from r and
    returning f(data).

func (Form) Reset()
    Reset implements the Reset method of the transform.Transformer interface.

func (f Form) Span(b []byte, atEOF bool) (n int, err error)
    Span implements transform.SpanningTransformer. It returns a boundary n such
    that b[0:n] == f(b[0:n]). It is not guaranteed to return the largest such n.

func (f Form) SpanString(s string, atEOF bool) (n int, err error)
    SpanString returns a boundary n such that s[0:n] == f(s[0:n]). It is not
    guaranteed to return the largest such n.

func (f Form) String(s string) string
    String returns f(s).

func (f Form) Transform(dst, src []byte, atEOF bool) (nDst, nSrc int, err error)
    Transform implements the Transform method of the transform.Transformer
    interface. It may need to write segments of up to MaxSegmentSize at once.
    Users should either catch ErrShortDst and allow dst to grow or have dst be
    at least of size MaxTransformChunkSize to be guaranteed of progress.

func (f Form) Writer(w io.Writer) io.WriteCloser
    Writer returns a new writer that implements Write(b) by writing f(b) to w.
    The returned writer may use an internal buffer to maintain state across
    Write calls. Calling its Close method writes any buffered data to w.

type Iter struct {
	// Has unexported fields.
}
    An Iter iterates over a string or byte slice, while normalizing it to a
    given Form.

func (i *Iter) Done() bool
    Done returns true if there is no more input to process.

func (i *Iter) Init(f Form, src []byte)
    Init initializes i to iterate over src after normalizing it to Form f.

func (i *Iter) InitString(f Form, src string)
    InitString initializes i to iterate over src after normalizing it to Form f.

func (i *Iter) Next() []byte
    Next returns f(i.input[i.Pos():n]), where n is a boundary of i.input.
    For any input a and b for which f(a) == f(b), subsequent calls to Next
    will return the same segments. Modifying runes are grouped together with
    the preceding starter, if such a starter exists. Although not guaranteed,
    n will typically be the smallest possible n.

func (i *Iter) Pos() int
    Pos returns the byte position at which the next call to Next will commence
    processing.

func (i *Iter) Seek(offset int64, whence int) (int64, error)
    Seek sets the segment to be returned by the next call to Next to start at
    position p. It is the responsibility of the caller to set p to the start of
    a segment.

type Properties struct {
	// Has unexported fields.
}
    Properties provides access to normalization properties of a rune.

func (p Properties) BoundaryAfter() bool
    BoundaryAfter returns true if runes cannot combine with or otherwise
    interact with this or previous runes.

func (p Properties) BoundaryBefore() bool
    BoundaryBefore returns true if this rune starts a new segment and cannot
    combine with any rune on the left.

func (p Properties) CCC() uint8
    CCC returns the canonical combining class of the underlying rune.

func (p Properties) Decomposition() []byte
    Decomposition returns the decomposition for the underlying rune or nil if
    there is none.

func (p Properties) LeadCCC() uint8
    LeadCCC returns the CCC of the first rune in the decomposition. If there is
    no decomposition, LeadCCC equals CCC.

func (p Properties) Size() int
    Size returns the length of UTF-8 encoding of the rune.

func (p Properties) TrailCCC() uint8
    TrailCCC returns the CCC of the last rune in the decomposition. If there is
    no decomposition, TrailCCC equals CCC.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
