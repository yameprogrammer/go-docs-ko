# package crypto/internal/fips140/bigmod

- 원문: <https://pkg.go.dev/crypto/internal/fips140/bigmod>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package bigmod // import "crypto/internal/fips140/bigmod"


TYPES

type Modulus struct {
	// Has unexported fields.
}
    Modulus is used for modular arithmetic, precomputing relevant constants.

    A Modulus can leak the exact number of bits needed to store its value and is
    stored without padding. Its actual value is still kept secret.

func NewModulus(b []byte) (*Modulus, error)
    NewModulus creates a new Modulus from a slice of big-endian bytes. The
    modulus must be greater than one.

    The number of significant bits and whether the modulus is even is leaked
    through timing side-channels.

func NewModulusProduct(a, b []byte) (*Modulus, error)
    NewModulusProduct creates a new Modulus from the product of two numbers
    represented as big-endian byte slices. The result must be greater than one.

func (m *Modulus) BitLen() int
    BitLen returns the size of m in bits.

func (m *Modulus) Nat() *Nat
    Nat returns m as a Nat.

func (m *Modulus) Size() int
    Size returns the size of m in bytes.

type Nat struct {
	// Has unexported fields.
}
    Nat represents an arbitrary natural number

    Each Nat has an announced length, which is the number of limbs it has
    stored. Operations on this number are allowed to leak this length, but will
    not leak any information about the values contained in those limbs.

func NewNat() *Nat
    NewNat returns a new nat with a size of zero, just like new(Nat), but with
    the preallocated capacity to hold a number of up to preallocTarget bits.
    NewNat inlines, so the allocation can live on the stack.

func (x *Nat) Add(y *Nat, m *Modulus) *Nat
    Add computes x = x + y mod m.

    The length of both operands must be the same as the modulus. Both operands
    must already be reduced modulo m.

func (x *Nat) BitLenVarTime() int
    BitLenVarTime returns the actual size of x in bits.

    The actual size of x (but nothing more) leaks through timing side-channels.
    Note that this is ordinarily secret, as opposed to the announced size of x.

func (x *Nat) Bits() []uint
    Bits returns x as a little-endian slice of uint. The length of the
    slice matches the announced length of x. The result and x share the same
    underlying array.

func (x *Nat) Bytes(m *Modulus) []byte
    Bytes returns x as a zero-extended big-endian byte slice. The size of the
    slice will match the size of m.

    x must have the same size as m and it must be less than or equal to m.

func (x *Nat) DivShortVarTime(y uint) uint
    DivShortVarTime calculates x = x / y and returns the remainder.

    It panics if y is zero.

func (x *Nat) Equal(y *Nat) choice
    Equal returns 1 if x == y, and 0 otherwise.

    Both operands must have the same announced length.

func (out *Nat) Exp(x *Nat, e []byte, m *Modulus) *Nat
    Exp calculates out = x^e mod m.

    The exponent e is represented in big-endian order. The output will be
    resized to the size of m and overwritten. x must already be reduced modulo
    m.

    m must be odd, or Exp will panic.

func (out *Nat) ExpShortVarTime(x *Nat, e uint, m *Modulus) *Nat
    ExpShortVarTime calculates out = x^e mod m.

    The output will be resized to the size of m and overwritten. x must already
    be reduced modulo m. This leaks the exponent through timing side-channels.

    m must be odd, or ExpShortVarTime will panic.

func (x *Nat) ExpandFor(m *Modulus) *Nat
    ExpandFor ensures x has the right size to work with operations modulo m.

    The announced size of x must be smaller than or equal to that of m.

func (x *Nat) GCDVarTime(a, b *Nat) (*Nat, error)
    GCDVarTime calculates x = GCD(a, b) where at least one of a or b is odd,
    and both are non-zero. If GCDVarTime returns an error, x is not modified.

    The output will be resized to the size of the larger of a and b.

func (x *Nat) InverseVarTime(a *Nat, m *Modulus) (*Nat, bool)
    InverseVarTime calculates x = a⁻¹ mod m and returns (x, true) if a is
    invertible. Otherwise, InverseVarTime returns (x, false) and x is not
    modified.

    a must be reduced modulo m, but doesn't need to have the same size.
    The output will be resized to the size of m and overwritten.

func (x *Nat) IsMinusOne(m *Modulus) choice
    IsMinusOne returns 1 if x == -1 mod m, and 0 otherwise.

    The length of x must be the same as the modulus. x must already be reduced
    modulo m.

func (x *Nat) IsOdd() choice
    IsOdd returns 1 if x is odd, and 0 otherwise.

func (x *Nat) IsOne() choice
    IsOne returns 1 if x == 1, and 0 otherwise.

func (x *Nat) IsZero() choice
    IsZero returns 1 if x == 0, and 0 otherwise.

func (out *Nat) Mod(x *Nat, m *Modulus) *Nat
    Mod calculates out = x mod m.

    This works regardless how large the value of x is.

    The output will be resized to the size of m and overwritten.

func (x *Nat) Mul(y *Nat, m *Modulus) *Nat
    Mul calculates x = x * y mod m.

    The length of both operands must be the same as the modulus. Both operands
    must already be reduced modulo m.

func (x *Nat) SetBits(y []uint) *Nat
    SetBits assigns x = y, where y is a slice of little-endian uint. x is
    resized to the length of y.

func (x *Nat) SetBytes(b []byte, m *Modulus) (*Nat, error)
    SetBytes assigns x = b, where b is a slice of big-endian bytes. SetBytes
    returns an error if b >= m.

    The output will be resized to the size of m and overwritten.

func (x *Nat) SetOverflowingBytes(b []byte, m *Modulus) (*Nat, error)
    SetOverflowingBytes assigns x = b, where b is a slice of big-endian bytes.
    SetOverflowingBytes returns an error if b has a longer bit length than m,
    but reduces overflowing values up to 2^⌈log2(m)⌉ - 1.

    The output will be resized to the size of m and overwritten.

func (x *Nat) SetUint(y uint) *Nat
    SetUint assigns x = y.

    The output will be resized to a single limb and overwritten.

func (x *Nat) ShiftRightByOne() *Nat
    ShiftRightByOne sets x = x >> 1.

    The announced length of x is unchanged.

func (x *Nat) ShiftRightVarTime(n uint) *Nat
    ShiftRightVarTime sets x = x >> n.

    The announced length of x is unchanged.

func (x *Nat) Sub(y *Nat, m *Modulus) *Nat
    Sub computes x = x - y mod m.

    The length of both operands must be the same as the modulus. Both operands
    must already be reduced modulo m.

func (x *Nat) SubOne(m *Modulus) *Nat
    SubOne computes x = x - 1 mod m.

    The length of x must be the same as the modulus.

func (x *Nat) TrailingZeroBitsVarTime() uint
    TrailingZeroBitsVarTime returns the number of trailing zero bits in x.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
