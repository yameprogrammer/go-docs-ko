# package crypto/internal/fips140/nistec/fiat

- 원문: <https://pkg.go.dev/crypto/internal/fips140/nistec/fiat>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package fiat // import "crypto/internal/fips140/nistec/fiat"


TYPES

type P224Element struct {
	// Has unexported fields.
}
    P224Element is an integer modulo 2^224 - 2^96 + 1.

    The zero value is a valid zero element.

func (e *P224Element) Add(t1, t2 *P224Element) *P224Element
    Add sets e = t1 + t2, and returns e.

func (e *P224Element) Bytes() []byte
    Bytes returns the 28-byte big-endian encoding of e.

func (e *P224Element) Equal(t *P224Element) int
    Equal returns 1 if e == t, and zero otherwise.

func (e *P224Element) Invert(x *P224Element) *P224Element
    Invert sets e = 1/x, and returns e.

    If x == 0, Invert returns e = 0.

func (e *P224Element) IsZero() int
    IsZero returns 1 if e == 0, and zero otherwise.

func (e *P224Element) Mul(t1, t2 *P224Element) *P224Element
    Mul sets e = t1 * t2, and returns e.

func (e *P224Element) One() *P224Element
    One sets e = 1, and returns e.

func (v *P224Element) Select(a, b *P224Element, cond int) *P224Element
    Select sets v to a if cond == 1, and to b if cond == 0.

func (e *P224Element) Set(t *P224Element) *P224Element
    Set sets e = t, and returns e.

func (e *P224Element) SetBytes(v []byte) (*P224Element, error)
    SetBytes sets e = v, where v is a big-endian 28-byte encoding, and returns
    e. If v is not 28 bytes or it encodes a value higher than 2^224 - 2^96 + 1,
    SetBytes returns nil and an error, and e is unchanged.

func (e *P224Element) Square(t *P224Element) *P224Element
    Square sets e = t * t, and returns e.

func (e *P224Element) Sub(t1, t2 *P224Element) *P224Element
    Sub sets e = t1 - t2, and returns e.

type P256Element struct {
	// Has unexported fields.
}
    P256Element is an integer modulo 2^256 - 2^224 + 2^192 + 2^96 - 1.

    The zero value is a valid zero element.

func (e *P256Element) Add(t1, t2 *P256Element) *P256Element
    Add sets e = t1 + t2, and returns e.

func (e *P256Element) Bytes() []byte
    Bytes returns the 32-byte big-endian encoding of e.

func (e *P256Element) Equal(t *P256Element) int
    Equal returns 1 if e == t, and zero otherwise.

func (e *P256Element) Invert(x *P256Element) *P256Element
    Invert sets e = 1/x, and returns e.

    If x == 0, Invert returns e = 0.

func (e *P256Element) IsZero() int
    IsZero returns 1 if e == 0, and zero otherwise.

func (e *P256Element) Mul(t1, t2 *P256Element) *P256Element
    Mul sets e = t1 * t2, and returns e.

func (e *P256Element) One() *P256Element
    One sets e = 1, and returns e.

func (v *P256Element) Select(a, b *P256Element, cond int) *P256Element
    Select sets v to a if cond == 1, and to b if cond == 0.

func (e *P256Element) Set(t *P256Element) *P256Element
    Set sets e = t, and returns e.

func (e *P256Element) SetBytes(v []byte) (*P256Element, error)
    SetBytes sets e = v, where v is a big-endian 32-byte encoding, and returns
    e. If v is not 32 bytes or it encodes a value higher than 2^256 - 2^224 +
    2^192 + 2^96 - 1, SetBytes returns nil and an error, and e is unchanged.

func (e *P256Element) Square(t *P256Element) *P256Element
    Square sets e = t * t, and returns e.

func (e *P256Element) Sub(t1, t2 *P256Element) *P256Element
    Sub sets e = t1 - t2, and returns e.

type P384Element struct {
	// Has unexported fields.
}
    P384Element is an integer modulo 2^384 - 2^128 - 2^96 + 2^32 - 1.

    The zero value is a valid zero element.

func (e *P384Element) Add(t1, t2 *P384Element) *P384Element
    Add sets e = t1 + t2, and returns e.

func (e *P384Element) Bytes() []byte
    Bytes returns the 48-byte big-endian encoding of e.

func (e *P384Element) Equal(t *P384Element) int
    Equal returns 1 if e == t, and zero otherwise.

func (e *P384Element) Invert(x *P384Element) *P384Element
    Invert sets e = 1/x, and returns e.

    If x == 0, Invert returns e = 0.

func (e *P384Element) IsZero() int
    IsZero returns 1 if e == 0, and zero otherwise.

func (e *P384Element) Mul(t1, t2 *P384Element) *P384Element
    Mul sets e = t1 * t2, and returns e.

func (e *P384Element) One() *P384Element
    One sets e = 1, and returns e.

func (v *P384Element) Select(a, b *P384Element, cond int) *P384Element
    Select sets v to a if cond == 1, and to b if cond == 0.

func (e *P384Element) Set(t *P384Element) *P384Element
    Set sets e = t, and returns e.

func (e *P384Element) SetBytes(v []byte) (*P384Element, error)
    SetBytes sets e = v, where v is a big-endian 48-byte encoding, and returns
    e. If v is not 48 bytes or it encodes a value higher than 2^384 - 2^128 -
    2^96 + 2^32 - 1, SetBytes returns nil and an error, and e is unchanged.

func (e *P384Element) Square(t *P384Element) *P384Element
    Square sets e = t * t, and returns e.

func (e *P384Element) Sub(t1, t2 *P384Element) *P384Element
    Sub sets e = t1 - t2, and returns e.

type P521Element struct {
	// Has unexported fields.
}
    P521Element is an integer modulo 2^521 - 1.

    The zero value is a valid zero element.

func (e *P521Element) Add(t1, t2 *P521Element) *P521Element
    Add sets e = t1 + t2, and returns e.

func (e *P521Element) Bytes() []byte
    Bytes returns the 66-byte big-endian encoding of e.

func (e *P521Element) Equal(t *P521Element) int
    Equal returns 1 if e == t, and zero otherwise.

func (e *P521Element) Invert(x *P521Element) *P521Element
    Invert sets e = 1/x, and returns e.

    If x == 0, Invert returns e = 0.

func (e *P521Element) IsZero() int
    IsZero returns 1 if e == 0, and zero otherwise.

func (e *P521Element) Mul(t1, t2 *P521Element) *P521Element
    Mul sets e = t1 * t2, and returns e.

func (e *P521Element) One() *P521Element
    One sets e = 1, and returns e.

func (v *P521Element) Select(a, b *P521Element, cond int) *P521Element
    Select sets v to a if cond == 1, and to b if cond == 0.

func (e *P521Element) Set(t *P521Element) *P521Element
    Set sets e = t, and returns e.

func (e *P521Element) SetBytes(v []byte) (*P521Element, error)
    SetBytes sets e = v, where v is a big-endian 66-byte encoding, and returns
    e. If v is not 66 bytes or it encodes a value higher than 2^521 - 1,
    SetBytes returns nil and an error, and e is unchanged.

func (e *P521Element) Square(t *P521Element) *P521Element
    Square sets e = t * t, and returns e.

func (e *P521Element) Sub(t1, t2 *P521Element) *P521Element
    Sub sets e = t1 - t2, and returns e.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
