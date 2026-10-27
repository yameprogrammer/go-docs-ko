# package log/slog/internal/buffer

- 원문: <https://pkg.go.dev/log/slog/internal/buffer>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package buffer provides a pool-allocated byte buffer.

## 원문 요약

Package buffer provides a pool-allocated byte buffer.

## API 상세 (go doc -all)

~~~text
package buffer // import "log/slog/internal/buffer"

Package buffer provides a pool-allocated byte buffer.

TYPES

type Buffer []byte
    Buffer is a byte buffer.

    This implementation is adapted from the unexported type buffer in
    go/src/fmt/print.go.

func New() *Buffer

func (b *Buffer) Free()

func (b *Buffer) Len() int

func (b *Buffer) Reset()

func (b *Buffer) SetLen(n int)

func (b *Buffer) String() string

func (b *Buffer) Write(p []byte) (int, error)

func (b *Buffer) WriteByte(c byte) error

func (b *Buffer) WriteString(s string) (int, error)
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
