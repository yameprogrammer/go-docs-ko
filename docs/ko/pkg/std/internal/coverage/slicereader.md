# package internal/coverage/slicereader

- 원문: <https://pkg.go.dev/internal/coverage/slicereader>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package slicereader // import "internal/coverage/slicereader"


TYPES

type Reader struct {
	// Has unexported fields.
}

func NewReader(b []byte, readonly bool) *Reader

func (r *Reader) Offset() int64

func (r *Reader) Read(b []byte) (int, error)

func (r *Reader) ReadString(len int64) string

func (r *Reader) ReadULEB128() (value uint64)

func (r *Reader) ReadUint32() uint32

func (r *Reader) ReadUint64() uint64

func (r *Reader) ReadUint8() uint8

func (r *Reader) Seek(offset int64, whence int) (ret int64, err error)
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
