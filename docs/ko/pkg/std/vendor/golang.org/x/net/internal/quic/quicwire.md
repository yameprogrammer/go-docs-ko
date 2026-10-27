# package vendor/golang.org/x/net/internal/quic/quicwire

- 원문: <https://pkg.go.dev/vendor/golang.org/x/net/internal/quic/quicwire>
- 분류: Go 표준 라이브러리

## 한국어 요약

`quicwire` 패키지는 QUIC/HTTP3 와이어 인코딩 타입, 특히 가변 길이 정수(variable-length integers)를 인코딩하고 디코딩합니다.

## 원문 요약

Package quicwire encodes and decode QUIC/HTTP3 wire encoding types, particularly variable-length integers.

## API 상세 (go doc -all)

~~~text
package quicwire // import "vendor/golang.org/x/net/internal/quic/quicwire"

Package quicwire encodes and decode QUIC/HTTP3 wire encoding types, particularly
variable-length integers.

CONSTANTS

const (
	MaxVarintSize = 8 // encoded size in bytes
	MaxVarint     = (1 << 62) - 1
)

FUNCTIONS

func AppendUint8Bytes(b, v []byte) []byte
    AppendUint8Bytes appends a sequence of bytes prefixed by an 8-bit length.

func AppendVarint(b []byte, v uint64) []byte
    AppendVarint appends a variable-length integer to b.

    https://www.rfc-editor.org/rfc/rfc9000.html#section-16

func AppendVarintBytes(b, v []byte) []byte
    AppendVarintBytes appends a sequence of bytes prefixed by a variable-length
    integer length.

func ConsumeUint32(b []byte) (uint32, int)
    ConsumeUint32 parses a 32-bit fixed-length, big-endian integer, reporting
    its length. It returns a negative length upon an error.

func ConsumeUint64(b []byte) (uint64, int)
    ConsumeUint64 parses a 64-bit fixed-length, big-endian integer, reporting
    its length. It returns a negative length upon an error.

func ConsumeUint8Bytes(b []byte) ([]byte, int)
    ConsumeUint8Bytes parses a sequence of bytes prefixed with an 8-bit length,
    reporting the total number of bytes consumed. It returns a negative length
    upon an error.

func ConsumeVarint(b []byte) (v uint64, n int)
    ConsumeVarint parses a variable-length integer, reporting its length.
    It returns a negative length upon an error.

    https://www.rfc-editor.org/rfc/rfc9000.html#section-16

func ConsumeVarintBytes(b []byte) ([]byte, int)
    ConsumeVarintBytes parses a sequence of bytes preceded by a variable-length
    integer length, reporting the total number of bytes consumed. It returns a
    negative length upon an error.

func ConsumeVarintInt64(b []byte) (v int64, n int)
    ConsumeVarintInt64 parses a variable-length integer as an int64.

func SizeVarint(v uint64) int
    SizeVarint returns the size of the variable-length integer encoding of f.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
