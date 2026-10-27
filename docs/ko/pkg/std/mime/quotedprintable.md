# package mime/quotedprintable

- 원문: <https://pkg.go.dev/mime/quotedprintable>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `quotedprintable`는 RFC 2045에서 정의된 쿼드 프린테이블 인코딩을 구현합니다.

## 원문 요약

Package quotedprintable implements quoted-printable encoding as specified by RFC 2045.

## API 상세 (go doc -all)

~~~text
package quotedprintable // import "mime/quotedprintable"

Package quotedprintable implements quoted-printable encoding as specified by RFC
2045.

TYPES

type Reader struct {
	// Has unexported fields.
}
    Reader is a quoted-printable decoder.

func NewReader(r io.Reader) *Reader
    NewReader returns a quoted-printable reader, decoding from r.

func (r *Reader) Read(p []byte) (n int, err error)
    Read reads and decodes quoted-printable data from the underlying reader.

type Writer struct {
	// Binary mode treats the writer's input as pure binary and processes end of
	// line bytes as binary data.
	Binary bool

	// Has unexported fields.
}
    A Writer is a quoted-printable writer that implements io.WriteCloser.

func NewWriter(w io.Writer) *Writer
    NewWriter returns a new Writer that writes to w.

func (w *Writer) Close() error
    Close closes the Writer, flushing any unwritten data to the underlying
    io.Writer, but does not close the underlying io.Writer.

func (w *Writer) Write(p []byte) (n int, err error)
    Write encodes p using quoted-printable encoding and writes it to the
    underlying io.Writer. It limits line length to 76 characters. The encoded
    bytes are not necessarily flushed until the Writer is closed.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
