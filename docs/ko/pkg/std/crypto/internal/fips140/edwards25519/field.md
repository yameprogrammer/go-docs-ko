# package crypto/internal/fips140/edwards25519/field

- 원문: <https://pkg.go.dev/crypto/internal/fips140/edwards25519/field>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package field implements fast arithmetic modulo 2^255-19.

## 원문 요약

Package field implements fast arithmetic modulo 2^255-19.

## API 상세 (go doc -all)

~~~text
package field // import "crypto/internal/fips140/edwards25519/field"

Package field implements fast arithmetic modulo 2^255-19.

TYPES

type Element struct {
	// Has unexported fields.
}
    Element represents an element of the field GF(2^255-19). Note that this is
    not a cryptographically secure group, and should only be used to interact
    with edwards25519.Point coordinates.

    This type works similarly to math/big.Int, and all arguments and receivers
    are allowed to alias.

    The zero value is a valid zero element.

func (v *Element) Absolute(u *Element) *Element
    Absolute sets v to |u|, and returns v.

func (v *Element) Add(a, b *Element) *Element
    Add sets v = a + b, and returns v.

func (v *Element) Bytes() []byte
    Bytes returns the canonical 32-byte little-endian encoding of v.

func (v *Element) Equal(u *Element) int
    Equal returns 1 if v and u are equal, and 0 otherwise.

func (v *Element) Invert(z *Element) *Element
    Invert sets v = 1/z mod p, and returns v.

    If z == 0, Invert returns v = 0.

func (v *Element) IsNegative() int
    IsNegative returns 1 if v is negative, and 0 otherwise.

func (v *Element) Mult32(x *Element, y uint32) *Element
    Mult32 sets v = x * y, and returns v.

func (v *Element) Multiply(x, y *Element) *Element
    Multiply sets v = x * y, and returns v.

func (v *Element) Negate(a *Element) *Element
    Negate sets v = -a, and returns v.

func (v *Element) One() *Element
    One sets v = 1, and returns v.

func (v *Element) Pow22523(x *Element) *Element
    Pow22523 set v = x^((p-5)/8), and returns v. (p-5)/8 is 2^252-3.

func (v *Element) Select(a, b *Element, cond int) *Element
    Select sets v to a if cond == 1, and to b if cond == 0.

func (v *Element) Set(a *Element) *Element
    Set sets v = a, and returns v.

func (v *Element) SetBytes(x []byte) (*Element, error)
    SetBytes sets v to x, where x is a 32-byte little-endian encoding. If x is
    not of the right length, SetBytes returns nil and an error, and the receiver
    is unchanged.

    Consistent with RFC 7748, the most significant bit (the high bit of the last
    byte) is ignored, and non-canonical values (2^255-19 through 2^255-1) are
    accepted. Note that this is laxer than specified by RFC 8032, but consistent
    with most Ed25519 implementations.

func (r *Element) SqrtRatio(u, v *Element) (R *Element, wasSquare int)
    SqrtRatio sets r to the non-negative square root of the ratio of u and v.

    If u/v is square, SqrtRatio returns r and 1. If u/v is not square, SqrtRatio
    sets r according to Section 4.3 of draft-irtf-cfrg-ristretto255-decaf448-00,
    and returns r and 0.

func (v *Element) Square(x *Element) *Element
    Square sets v = x * x, and returns v.

func (v *Element) SquareN(x *Element, n int) *Element
    SquareN sets v = x^(2^n), and returns v. n must be positive.

func (v *Element) Subtract(a, b *Element) *Element
    Subtract sets v = a - b, and returns v.

func (v *Element) Swap(u *Element, cond int)
    Swap swaps v and u if cond == 1 or leaves them unchanged if cond == 0,
    and returns v.

func (v *Element) Zero() *Element
    Zero sets v = 0, and returns v.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
