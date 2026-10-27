# package net/http/internal

- 원문: <https://pkg.go.dev/net/http/internal>
- 분류: Go 표준 라이브러리

## 한국어 요약

`internal` 패키지는 `net/http` 및 `net/http/httputil`에서 공유하는 HTTP 내부 구현 내용을 포함합니다.

## 원문 요약

Package internal contains HTTP internals shared by net/http and net/http/httputil.

## API 상세 (go doc -all)

~~~text
package internal // import "net/http/internal"

Package internal contains HTTP internals shared by net/http and
net/http/httputil.

CONSTANTS

const SniffLen = 512
    The algorithm uses at most SniffLen bytes to make its decision.


VARIABLES

var (
	ErrAbortHandler    = errors.New("net/http: abort Handler")
	ErrBodyNotAllowed  = errors.New("http: request method or response status code does not allow body")
	ErrRequestCanceled = errors.New("net/http: request canceled")
	ErrSkipAltProtocol = errors.New("net/http: skip alternate protocol")
)
var ErrLineTooLong = errors.New("header line too long")

FUNCTIONS

func DetectContentType(data []byte) string
    DetectContentType implements the algorithm described at
    https://mimesniff.spec.whatwg.org/ to determine the Content-Type of
    the given data. It considers at most the first 512 bytes of data.
    DetectContentType always returns a valid MIME type: if it cannot determine a
    more specific one, it returns "application/octet-stream".

func NewChunkedReader(r io.Reader) io.Reader
    NewChunkedReader returns a new chunkedReader that translates the data read
    from r out of HTTP "chunked" format before returning it. The chunkedReader
    returns io.EOF when the final 0-length chunk is read.

    NewChunkedReader is not needed by normal applications. The http package
    automatically decodes chunking when reading response bodies.

func NewChunkedWriter(w io.Writer) io.WriteCloser
    NewChunkedWriter returns a new chunkedWriter that translates writes into
    HTTP "chunked" format before writing them to w. Closing the returned
    chunkedWriter sends the final 0-length chunk that marks the end of the
    stream but does not send the final CRLF that appears after trailers;
    trailers and the last CRLF must be written separately.

    NewChunkedWriter is not needed by normal applications. The http package
    adds chunking automatically if handlers don't set a Content-Length header.
    Using newChunkedWriter inside a handler would result in double chunking or
    chunking with a Content-Length length, both of which are wrong.


TYPES

type FlushAfterChunkWriter struct {
	*bufio.Writer
}
    FlushAfterChunkWriter signals from the caller of NewChunkedWriter that each
    chunk should be followed by a flush. It is used by the net/http.Transport
    code to keep the buffering behavior for headers and trailers, but flush out
    chunks aggressively in the middle for request bodies which may be generated
    slowly. See Issue 6574.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
