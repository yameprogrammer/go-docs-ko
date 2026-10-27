# package vendor/golang.org/x/text/transform

- 원문: <https://pkg.go.dev/vendor/golang.org/x/text/transform>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `transform`은 바이트를 처리하면서 변환을 수행하는 리더 및 라이터 래퍼를 제공합니다. 또한 다양한 변환 기능을 제공합니다.

## 원문 요약

Package transform provides reader and writer wrappers that transform the bytes passing through as well as various transformations.

## API 상세 (go doc -all)

~~~text
package transform // import "vendor/golang.org/x/text/transform"

Package transform provides reader and writer wrappers that transform the bytes
passing through as well as various transformations. Example transformations
provided by other packages include normalization and conversion between
character sets.

VARIABLES

var (
	// ErrShortDst means that the destination buffer was too short to
	// receive all of the transformed bytes.
	ErrShortDst = errors.New("transform: short destination buffer")

	// ErrShortSrc means that the source buffer has insufficient data to
	// complete the transformation.
	ErrShortSrc = errors.New("transform: short source buffer")

	// ErrEndOfSpan means that the input and output (the transformed input)
	// are not identical.
	ErrEndOfSpan = errors.New("transform: input and output are not identical")
)
var (
	// Discard is a Transformer for which all Transform calls succeed
	// by consuming all bytes and writing nothing.
	Discard Transformer = discard{}

	// Nop is a SpanningTransformer that copies src to dst.
	Nop SpanningTransformer = nop{}
)

FUNCTIONS

func Append(t Transformer, dst, src []byte) (result []byte, n int, err error)
    Append appends the result of converting src[:n] using t to dst, where n <=
    len(src), If err == nil, n will be len(src). It calls Reset on t.

func Bytes(t Transformer, b []byte) (result []byte, n int, err error)
    Bytes returns a new byte slice with the result of converting b[:n] using t,
    where n <= len(b). If err == nil, n will be len(b). It calls Reset on t.

func String(t Transformer, s string) (result string, n int, err error)
    String returns a string with the result of converting s[:n] using t,
    where n <= len(s). If err == nil, n will be len(s). It calls Reset on t.


TYPES

type NopResetter struct{}
    NopResetter can be embedded by implementations of Transformer to add a nop
    Reset method.

func (NopResetter) Reset()
    Reset implements the Reset method of the Transformer interface.

type Reader struct {
	// Has unexported fields.
}
    Reader wraps another io.Reader by transforming the bytes read.

func NewReader(r io.Reader, t Transformer) *Reader
    NewReader returns a new Reader that wraps r by transforming the bytes read
    via t. It calls Reset on t.

func (r *Reader) Read(p []byte) (int, error)
    Read implements the io.Reader interface.

type SpanningTransformer interface {
	Transformer

	// Span returns a position in src such that transforming src[:n] results in
	// identical output src[:n] for these bytes. It does not necessarily return
	// the largest such n. The atEOF argument tells whether src represents the
	// last bytes of the input.
	//
	// Callers should always account for the n bytes consumed before
	// considering the error err.
	//
	// A nil error means that all input bytes are known to be identical to the
	// output produced by the Transformer. A nil error can be returned
	// regardless of whether atEOF is true. If err is nil, then n must
	// equal len(src); the converse is not necessarily true.
	//
	// ErrEndOfSpan means that the Transformer output may differ from the
	// input after n bytes. Note that n may be len(src), meaning that the output
	// would contain additional bytes after otherwise identical output.
	// ErrShortSrc means that src had insufficient data to determine whether the
	// remaining bytes would change. Other than the error conditions listed
	// here, implementations are free to report other errors that arise.
	//
	// Calling Span can modify the Transformer state as a side effect. In
	// effect, it does the transformation just as calling Transform would, only
	// without copying to a destination buffer and only up to a point it can
	// determine the input and output bytes are the same. This is obviously more
	// limited than calling Transform, but can be more efficient in terms of
	// copying and allocating buffers. Calls to Span and Transform may be
	// interleaved.
	Span(src []byte, atEOF bool) (n int, err error)
}
    SpanningTransformer extends the Transformer interface with a Span method
    that determines how much of the input already conforms to the Transformer.

type Transformer interface {
	// Transform writes to dst the transformed bytes read from src, and
	// returns the number of dst bytes written and src bytes read. The
	// atEOF argument tells whether src represents the last bytes of the
	// input.
	//
	// Callers should always process the nDst bytes produced and account
	// for the nSrc bytes consumed before considering the error err.
	//
	// A nil error means that all of the transformed bytes (whether freshly
	// transformed from src or left over from previous Transform calls)
	// were written to dst. A nil error can be returned regardless of
	// whether atEOF is true. If err is nil then nSrc must equal len(src);
	// the converse is not necessarily true.
	//
	// ErrShortDst means that dst was too short to receive all of the
	// transformed bytes. ErrShortSrc means that src had insufficient data
	// to complete the transformation. If both conditions apply, then
	// either error may be returned. Other than the error conditions listed
	// here, implementations are free to report other errors that arise.
	Transform(dst, src []byte, atEOF bool) (nDst, nSrc int, err error)

	// Reset resets the state and allows a Transformer to be reused.
	Reset()
}
    Transformer transforms bytes.

func Chain(t ...Transformer) Transformer
    Chain returns a Transformer that applies t in sequence.

func RemoveFunc(f func(r rune) bool) Transformer
    Deprecated: Use runes.Remove instead.

type Writer struct {
	// Has unexported fields.
}
    Writer wraps another io.Writer by transforming the bytes read. The user
    needs to call Close to flush unwritten bytes that may be buffered.

func NewWriter(w io.Writer, t Transformer) *Writer
    NewWriter returns a new Writer that wraps w by transforming the bytes
    written via t. It calls Reset on t.

func (w *Writer) Close() error
    Close implements the io.Closer interface.

func (w *Writer) Write(data []byte) (n int, err error)
    Write implements the io.Writer interface. If there are not enough bytes
    available to complete a Transform, the bytes will be buffered for the next
    write. Call Close to convert the remaining bytes.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
