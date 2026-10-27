# package compress/bzip2

- 원문: <https://pkg.go.dev/compress/bzip2>
- 분류: Go 표준 라이브러리

## 한국어 요약

`bzip2` 패키지는 bzip2 압축 해제를 구현합니다.

## 원문 요약

Package bzip2 implements bzip2 decompression.

## API 상세 (go doc -all)

~~~text
package bzip2 // import "compress/bzip2"

Package bzip2 implements bzip2 decompression.

FUNCTIONS

func NewReader(r io.Reader) io.Reader
    NewReader returns an io.Reader which decompresses bzip2 data from r.
    If r does not also implement io.ByteReader, the decompressor may read more
    data than necessary from r.


TYPES

type StructuralError string
    A StructuralError is returned when the bzip2 data is found to be
    syntactically invalid.

func (s StructuralError) Error() string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
