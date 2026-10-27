# package encoding/ascii85

- 원문: <https://pkg.go.dev/encoding/ascii85>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 ascii85는 btoa 도구와 Adobe의 PostScript 및 PDF 문서 형식에서 사용되는 ascii85 데이터 인코딩을 구현합니다.

## 원문 요약

Package ascii85 implements the ascii85 data encoding as used in the btoa tool and Adobe's PostScript and PDF document formats.

## API 상세 (go doc -all)

~~~text
package ascii85 // import "encoding/ascii85"

Package ascii85 implements the ascii85 data encoding as used in the btoa tool
and Adobe's PostScript and PDF document formats.

FUNCTIONS

func Decode(dst, src []byte, flush bool) (ndst, nsrc int, err error)
    Decode decodes src into dst, returning both the number of bytes written to
    dst and the number consumed from src. If src contains invalid ascii85 data,
    Decode will return the number of bytes successfully written and a
    CorruptInputError. Decode ignores space and control characters in src.
    Often, ascii85-encoded data is wrapped in <~ and ~> symbols. Decode expects
    these to have been stripped by the caller.

    If flush is true, Decode assumes that src represents the end of the input
    stream and processes it completely rather than wait for the completion of
    another 32-bit block.

    NewDecoder wraps an io.Reader interface around Decode.

func Encode(dst, src []byte) int
    Encode encodes src into at most MaxEncodedLen(len(src)) bytes of dst,
    returning the actual number of bytes written.

    The encoding handles 4-byte chunks, using a special encoding for the last
    fragment, so Encode is not appropriate for use on individual blocks of a
    large data stream. Use NewEncoder instead.

    Often, ascii85-encoded data is wrapped in <~ and ~> symbols. Encode does not
    add these.

func MaxEncodedLen(n int) int
    MaxEncodedLen returns the maximum length of an encoding of n source bytes.

func NewDecoder(r io.Reader) io.Reader
    NewDecoder constructs a new ascii85 stream decoder.

func NewEncoder(w io.Writer) io.WriteCloser
    NewEncoder returns a new ascii85 stream encoder. Data written to the
    returned writer will be encoded and then written to w. Ascii85 encodings
    operate in 32-bit blocks; when finished writing, the caller must Close the
    returned encoder to flush any trailing partial block.


TYPES

type CorruptInputError int64

func (e CorruptInputError) Error() string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
