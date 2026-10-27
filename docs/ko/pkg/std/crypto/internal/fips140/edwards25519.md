# package crypto/internal/fips140/edwards25519

- 원문: <https://pkg.go.dev/crypto/internal/fips140/edwards25519>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 edwards25519는 Twisted Edwards 곡선의 그룹 로직을 구현합니다.

## 원문 요약

Package edwards25519 implements group logic for the twisted Edwards curve

## API 상세 (go doc -all)

~~~text
package edwards25519 // import "crypto/internal/fips140/edwards25519"

Package edwards25519 implements group logic for the twisted Edwards curve

    -x^2 + y^2 = 1 + -(121665/121666)*x^2*y^2

This is better known as the Edwards curve equivalent to Curve25519, and is the
curve used by the Ed25519 signature scheme.

Most users don't need this package, and should instead use crypto/ed25519
for signatures, golang.org/x/crypto/curve25519 for Diffie-Hellman, or
github.com/gtank/ristretto255 for prime order group logic.

However, developers who do need to interact with low-level edwards25519
operations can use filippo.io/edwards25519, an extended version of this package
repackaged as an importable module.

(Note that filippo.io/edwards25519 and github.com/gtank/ristretto255 are
not maintained by the Go team and are not covered by the Go 1 Compatibility
Promise.)

TYPES

type Point struct {
	// Has unexported fields.
}
    Point represents a point on the edwards25519 curve.

    This type works similarly to math/big.Int, and all arguments and receivers
    are allowed to alias.

    The zero value is NOT valid, and it may be used only as a receiver.

func NewGeneratorPoint() *Point
    NewGeneratorPoint returns a new Point set to the canonical generator.

func NewIdentityPoint() *Point
    NewIdentityPoint returns a new Point set to the identity.

func (v *Point) Add(p, q *Point) *Point
    Add sets v = p + q, and returns v.

func (v *Point) Bytes() []byte
    Bytes returns the canonical 32-byte encoding of v, according to RFC 8032,
    Section 5.1.2.

func (v *Point) Equal(u *Point) int
    Equal returns 1 if v is equivalent to u, and 0 otherwise.

func (v *Point) Negate(p *Point) *Point
    Negate sets v = -p, and returns v.

func (v *Point) ScalarBaseMult(x *Scalar) *Point
    ScalarBaseMult sets v = x * B, where B is the canonical generator, and
    returns v.

    The scalar multiplication is done in constant time.

func (v *Point) ScalarMult(x *Scalar, q *Point) *Point
    ScalarMult sets v = x * q, and returns v.

    The scalar multiplication is done in constant time.

func (v *Point) Set(u *Point) *Point
    Set sets v = u, and returns v.

func (v *Point) SetBytes(x []byte) (*Point, error)
    SetBytes sets v = x, where x is a 32-byte encoding of v. If x does not
    represent a valid point on the curve, SetBytes returns nil and an error and
    the receiver is unchanged. Otherwise, SetBytes returns v.

    Note that SetBytes accepts all non-canonical encodings of valid points.
    That is, it follows decoding rules that match most implementations in the
    ecosystem rather than RFC 8032.

func (v *Point) Subtract(p, q *Point) *Point
    Subtract sets v = p - q, and returns v.

func (v *Point) VarTimeDoubleScalarBaseMult(a *Scalar, A *Point, b *Scalar) *Point
    VarTimeDoubleScalarBaseMult sets v = a * A + b * B, where B is the canonical
    generator, and returns v.

    Execution time depends on the inputs.

type Scalar struct {
	// Has unexported fields.
}
    A Scalar is an integer modulo

        l = 2^252 + 27742317777372353535851937790883648493

    which is the prime order of the edwards25519 group.

    This type works similarly to math/big.Int, and all arguments and receivers
    are allowed to alias.

    The zero value is a valid zero element.

func NewScalar() *Scalar
    NewScalar returns a new zero Scalar.

func (s *Scalar) Add(x, y *Scalar) *Scalar
    Add sets s = x + y mod l, and returns s.

func (s *Scalar) Bytes() []byte
    Bytes returns the canonical 32-byte little-endian encoding of s.

func (s *Scalar) Equal(t *Scalar) int
    Equal returns 1 if s and t are equal, and 0 otherwise.

func (s *Scalar) Multiply(x, y *Scalar) *Scalar
    Multiply sets s = x * y mod l, and returns s.

func (s *Scalar) MultiplyAdd(x, y, z *Scalar) *Scalar
    MultiplyAdd sets s = x * y + z mod l, and returns s. It is equivalent to
    using Multiply and then Add.

func (s *Scalar) Negate(x *Scalar) *Scalar
    Negate sets s = -x mod l, and returns s.

func (s *Scalar) Set(x *Scalar) *Scalar
    Set sets s = x, and returns s.

func (s *Scalar) SetBytesWithClamping(x []byte) (*Scalar, error)
    SetBytesWithClamping applies the buffer pruning described in RFC 8032,
    Section 5.1.5 (also known as clamping) and sets s to the result. The input
    must be 32 bytes, and it is not modified. If x is not of the right length,
    SetBytesWithClamping returns nil and an error, and the receiver is
    unchanged.

    Note that since Scalar values are always reduced modulo the prime
    order of the curve, the resulting value will not preserve any of the
    cofactor-clearing properties that clamping is meant to provide. It will
    however work as expected as long as it is applied to points on the prime
    order subgroup, like in Ed25519. In fact, it is lost to history why RFC
    8032 adopted the irrelevant RFC 7748 clamping, but it is now required for
    compatibility.

func (s *Scalar) SetCanonicalBytes(x []byte) (*Scalar, error)
    SetCanonicalBytes sets s = x, where x is a 32-byte little-endian encoding of
    s, and returns s. If x is not a canonical encoding of s, SetCanonicalBytes
    returns nil and an error, and the receiver is unchanged.

func (s *Scalar) SetUniformBytes(x []byte) (*Scalar, error)
    SetUniformBytes sets s = x mod l, where x is a 64-byte little-endian
    integer. If x is not of the right length, SetUniformBytes returns nil and an
    error, and the receiver is unchanged.

    SetUniformBytes can be used to set s to a uniformly distributed value given
    64 uniformly distributed random bytes.

func (s *Scalar) Subtract(x, y *Scalar) *Scalar
    Subtract sets s = x - y mod l, and returns s.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
