# package internal/zstd

- 원문: <https://pkg.go.dev/internal/zstd>
- 분류: Go 표준 라이브러리

## 한국어 요약

`zstd` 패키지는 RFC 8878에 설명된 zstd 스트림을 위한 압축 해제 도구(decompressor)를 제공합니다.

## 원문 요약

Package zstd provides a decompressor for zstd streams, described in RFC 8878.

## API 상세 (go doc -all)

~~~text
package zstd // import "internal/zstd"

Package zstd provides a decompressor for zstd streams, described in RFC 8878.
It does not support dictionaries.

TYPES

type Reader struct {
	// Has unexported fields.
}
    Reader implements io.Reader to read a zstd compressed stream.

func NewReader(input io.Reader) *Reader
    NewReader creates a new Reader that decompresses data from the given reader.

func (r *Reader) Read(p []byte) (int, error)
    Read implements io.Reader.

func (r *Reader) ReadByte() (byte, error)
    ReadByte implements io.ByteReader.

func (r *Reader) Reset(input io.Reader)
    Reset discards the current state and starts reading a new stream from r.
    This permits reusing a Reader rather than allocating a new one.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
