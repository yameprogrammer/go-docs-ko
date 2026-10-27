# package crypto/internal/fips140/nistec

- 원문: <https://pkg.go.dev/crypto/internal/fips140/nistec>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 nistec는 NIST SP 800-186에서 정의된 타원 곡선을 구현합니다.

## 원문 요약

Package nistec implements the elliptic curves from NIST SP 800-186.

## API 상세 (go doc -all)

~~~text
package nistec // import "crypto/internal/fips140/nistec"

Package nistec implements the elliptic curves from NIST SP 800-186.

This package uses fiat-crypto or specialized assembly and Go code for its
backend field arithmetic (not math/big) and exposes constant-time, heap
allocation-free, byte slice-based safe APIs. Group operations use modern and
safe complete addition formulas where possible. The point at infinity is handled
and encoded according to SEC 1, Version 2.0, and invalid curve points can't be
represented.

FUNCTIONS

func P256OrdInverse(k *[4]uint64)
    P256OrdInverse sets k to the inverse of k modulo ord(G). k is encoded as
    four uint64 limbs in little-endian order, and must be reduced. If k is zero,
    the result is zero.


TYPES

type P224Point struct {
	// Has unexported fields.
}
    P224Point is a P224 point. The zero value is NOT valid.

func NewP224Point() *P224Point
    NewP224Point returns a new P224Point representing the point at infinity
    point.

func (q *P224Point) Add(p1, p2 *P224Point) *P224Point
    Add sets q = p1 + p2, and returns q. The points may overlap.

func (p *P224Point) Bytes() []byte
    Bytes returns the uncompressed or infinity encoding of p, as specified in
    SEC 1, Version 2.0, Section 2.3.3. Note that the encoding of the point at
    infinity is shorter than all other encodings.

func (p *P224Point) BytesCompressed() []byte
    BytesCompressed returns the compressed or infinity encoding of p,
    as specified in SEC 1, Version 2.0, Section 2.3.3. Note that the encoding of
    the point at infinity is shorter than all other encodings.

func (p *P224Point) BytesX() ([]byte, error)
    BytesX returns the encoding of the x-coordinate of p, as specified in SEC 1,
    Version 2.0, Section 2.3.5, or an error if p is the point at infinity.

func (q *P224Point) Double(p *P224Point) *P224Point
    Double sets q = p + p, and returns q. The points may overlap.

func (p *P224Point) ScalarBaseMult(scalar []byte) (*P224Point, error)
    ScalarBaseMult sets p = scalar * B, where B is the canonical generator,
    and returns p.

func (p *P224Point) ScalarMult(q *P224Point, scalar []byte) (*P224Point, error)
    ScalarMult sets p = scalar * q, and returns p.

func (q *P224Point) Select(p1, p2 *P224Point, cond int) *P224Point
    Select sets q to p1 if cond == 1, and to p2 if cond == 0.

func (p *P224Point) Set(q *P224Point) *P224Point
    Set sets p = q and returns p.

func (p *P224Point) SetBytes(b []byte) (*P224Point, error)
    SetBytes sets p to the compressed, uncompressed, or infinity value encoded
    in b, as specified in SEC 1, Version 2.0, Section 2.3.4. If the point is not
    on the curve, it returns nil and an error, and the receiver is unchanged.
    Otherwise, it returns p.

func (p *P224Point) SetGenerator() *P224Point
    SetGenerator sets p to the canonical generator and returns p.

type P256Point struct {
	// Has unexported fields.
}
    P256Point is a P-256 point. The zero value should not be assumed to be valid
    (although it is in this implementation).

func NewP256Point() *P256Point
    NewP256Point returns a new P256Point representing the point at infinity.

func (q *P256Point) Add(r1, r2 *P256Point) *P256Point
    Add sets q = p1 + p2, and returns q. The points may overlap.

func (p *P256Point) Bytes() []byte
    Bytes returns the uncompressed or infinity encoding of p, as specified in
    SEC 1, Version 2.0, Section 2.3.3. Note that the encoding of the point at
    infinity is shorter than all other encodings.

func (p *P256Point) BytesCompressed() []byte
    BytesCompressed returns the compressed or infinity encoding of p,
    as specified in SEC 1, Version 2.0, Section 2.3.3. Note that the encoding of
    the point at infinity is shorter than all other encodings.

func (p *P256Point) BytesX() ([]byte, error)
    BytesX returns the encoding of the x-coordinate of p, as specified in SEC 1,
    Version 2.0, Section 2.3.5, or an error if p is the point at infinity.

func (q *P256Point) Double(p *P256Point) *P256Point
    Double sets q = p + p, and returns q. The points may overlap.

func (r *P256Point) ScalarBaseMult(scalar []byte) (*P256Point, error)
    ScalarBaseMult sets r = scalar * generator, where scalar is a 32-byte big
    endian value, and returns r. If scalar is not 32 bytes long, ScalarBaseMult
    returns an error and the receiver is unchanged.

func (r *P256Point) ScalarMult(q *P256Point, scalar []byte) (*P256Point, error)
    ScalarMult sets r = scalar * q, where scalar is a 32-byte big endian value,
    and returns r. If scalar is not 32 bytes long, ScalarBaseMult returns an
    error and the receiver is unchanged.

func (q *P256Point) Select(p1, p2 *P256Point, cond int) *P256Point
    Select sets q to p1 if cond == 1, and to p2 if cond == 0.

func (p *P256Point) Set(q *P256Point) *P256Point
    Set sets p = q and returns p.

func (p *P256Point) SetBytes(b []byte) (*P256Point, error)
    SetBytes sets p to the compressed, uncompressed, or infinity value encoded
    in b, as specified in SEC 1, Version 2.0, Section 2.3.4. If the point is not
    on the curve, it returns nil and an error, and the receiver is unchanged.
    Otherwise, it returns p.

func (p *P256Point) SetGenerator() *P256Point
    SetGenerator sets p to the canonical generator and returns p.

type P384Point struct {
	// Has unexported fields.
}
    P384Point is a P384 point. The zero value is NOT valid.

func NewP384Point() *P384Point
    NewP384Point returns a new P384Point representing the point at infinity
    point.

func (q *P384Point) Add(p1, p2 *P384Point) *P384Point
    Add sets q = p1 + p2, and returns q. The points may overlap.

func (p *P384Point) Bytes() []byte
    Bytes returns the uncompressed or infinity encoding of p, as specified in
    SEC 1, Version 2.0, Section 2.3.3. Note that the encoding of the point at
    infinity is shorter than all other encodings.

func (p *P384Point) BytesCompressed() []byte
    BytesCompressed returns the compressed or infinity encoding of p,
    as specified in SEC 1, Version 2.0, Section 2.3.3. Note that the encoding of
    the point at infinity is shorter than all other encodings.

func (p *P384Point) BytesX() ([]byte, error)
    BytesX returns the encoding of the x-coordinate of p, as specified in SEC 1,
    Version 2.0, Section 2.3.5, or an error if p is the point at infinity.

func (q *P384Point) Double(p *P384Point) *P384Point
    Double sets q = p + p, and returns q. The points may overlap.

func (p *P384Point) ScalarBaseMult(scalar []byte) (*P384Point, error)
    ScalarBaseMult sets p = scalar * B, where B is the canonical generator,
    and returns p.

func (p *P384Point) ScalarMult(q *P384Point, scalar []byte) (*P384Point, error)
    ScalarMult sets p = scalar * q, and returns p.

func (q *P384Point) Select(p1, p2 *P384Point, cond int) *P384Point
    Select sets q to p1 if cond == 1, and to p2 if cond == 0.

func (p *P384Point) Set(q *P384Point) *P384Point
    Set sets p = q and returns p.

func (p *P384Point) SetBytes(b []byte) (*P384Point, error)
    SetBytes sets p to the compressed, uncompressed, or infinity value encoded
    in b, as specified in SEC 1, Version 2.0, Section 2.3.4. If the point is not
    on the curve, it returns nil and an error, and the receiver is unchanged.
    Otherwise, it returns p.

func (p *P384Point) SetGenerator() *P384Point
    SetGenerator sets p to the canonical generator and returns p.

type P521Point struct {
	// Has unexported fields.
}
    P521Point is a P521 point. The zero value is NOT valid.

func NewP521Point() *P521Point
    NewP521Point returns a new P521Point representing the point at infinity
    point.

func (q *P521Point) Add(p1, p2 *P521Point) *P521Point
    Add sets q = p1 + p2, and returns q. The points may overlap.

func (p *P521Point) Bytes() []byte
    Bytes returns the uncompressed or infinity encoding of p, as specified in
    SEC 1, Version 2.0, Section 2.3.3. Note that the encoding of the point at
    infinity is shorter than all other encodings.

func (p *P521Point) BytesCompressed() []byte
    BytesCompressed returns the compressed or infinity encoding of p,
    as specified in SEC 1, Version 2.0, Section 2.3.3. Note that the encoding of
    the point at infinity is shorter than all other encodings.

func (p *P521Point) BytesX() ([]byte, error)
    BytesX returns the encoding of the x-coordinate of p, as specified in SEC 1,
    Version 2.0, Section 2.3.5, or an error if p is the point at infinity.

func (q *P521Point) Double(p *P521Point) *P521Point
    Double sets q = p + p, and returns q. The points may overlap.

func (p *P521Point) ScalarBaseMult(scalar []byte) (*P521Point, error)
    ScalarBaseMult sets p = scalar * B, where B is the canonical generator,
    and returns p.

func (p *P521Point) ScalarMult(q *P521Point, scalar []byte) (*P521Point, error)
    ScalarMult sets p = scalar * q, and returns p.

func (q *P521Point) Select(p1, p2 *P521Point, cond int) *P521Point
    Select sets q to p1 if cond == 1, and to p2 if cond == 0.

func (p *P521Point) Set(q *P521Point) *P521Point
    Set sets p = q and returns p.

func (p *P521Point) SetBytes(b []byte) (*P521Point, error)
    SetBytes sets p to the compressed, uncompressed, or infinity value encoded
    in b, as specified in SEC 1, Version 2.0, Section 2.3.4. If the point is not
    on the curve, it returns nil and an error, and the receiver is unchanged.
    Otherwise, it returns p.

func (p *P521Point) SetGenerator() *P521Point
    SetGenerator sets p to the canonical generator and returns p.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
