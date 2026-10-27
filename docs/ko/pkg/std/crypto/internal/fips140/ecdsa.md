# package crypto/internal/fips140/ecdsa

- 원문: <https://pkg.go.dev/crypto/internal/fips140/ecdsa>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package ecdsa // import "crypto/internal/fips140/ecdsa"


FUNCTIONS

func Verify[P Point[P]](c *Curve[P], pub *PublicKey, hash []byte, sig *Signature) error
    Verify verifies the signature, sig, of hash (which should be the result of
    hashing a larger message) using the public key, pub. If the hash is longer
    than the bit-length of the private key's curve order, the hash will be
    truncated to that length.

    The inputs are not considered confidential, and may leak through timing side
    channels, or if an attacker has control of part of the inputs.

func TestingOnlyNewDRBG[H hash.Hash](hash func() H, entropy, nonce []byte, s []byte) *hmacDRBG
    TestingOnlyNewDRBG creates an SP 800-90A Rev. 1 HMAC_DRBG with a plain
    personalization string.

    This should only be used for ACVP testing. hmacDRBG is not intended to be
    used directly.


TYPES

type Curve[P Point[P]] struct {
	N *bigmod.Modulus
	// Has unexported fields.
}

func P224() *Curve[*nistec.P224Point]

func P256() *Curve[*nistec.P256Point]

func P384() *Curve[*nistec.P384Point]

func P521() *Curve[*nistec.P521Point]

type Point[P any] interface {
	*nistec.P224Point | *nistec.P256Point | *nistec.P384Point | *nistec.P521Point
	Bytes() []byte
	BytesX() ([]byte, error)
	SetBytes([]byte) (P, error)
	ScalarMult(P, []byte) (P, error)
	ScalarBaseMult([]byte) (P, error)
	Add(p1, p2 P) P
}
    Point is a generic constraint for the nistec Point types.

type PrivateKey struct {
	// Has unexported fields.
}

func GenerateKey[P Point[P]](c *Curve[P], rand io.Reader) (*PrivateKey, error)
    GenerateKey generates a new ECDSA private key pair for the specified curve.

func NewPrivateKey[P Point[P]](c *Curve[P], D, Q []byte) (*PrivateKey, error)
    NewPrivateKey creates a new ECDSA private key from the given D and Q byte
    slices. D must be the fixed-length big-endian encoding of the private
    scalar, and Q must be the compressed or uncompressed encoding of the public
    point.

func (priv *PrivateKey) Bytes() []byte

func (priv *PrivateKey) PublicKey() *PublicKey

type PublicKey struct {
	// Has unexported fields.
}

func NewPublicKey[P Point[P]](c *Curve[P], Q []byte) (*PublicKey, error)
    NewPublicKey creates a new ECDSA public key from the given Q byte slice.
    Q must be the compressed or uncompressed encoding of the public point.

func (pub *PublicKey) Bytes() []byte

type Signature struct {
	R, S []byte
}
    Signature is an ECDSA signature, where r and s are represented as big-endian
    byte slices of the same length as the curve order.

func Sign[P Point[P], H hash.Hash](c *Curve[P], h func() H, priv *PrivateKey, rand io.Reader, hash []byte) (*Signature, error)
    Sign signs a hash (which should be the result of hashing a larger message
    with the hash function H) using the private key, priv. If the hash is longer
    than the bit-length of the private key's curve order, the hash will be
    truncated to that length.

func SignDeterministic[P Point[P], H hash.Hash](c *Curve[P], h func() H, priv *PrivateKey, hash []byte) (*Signature, error)
    SignDeterministic signs a hash (which shall be the result of hashing a
    larger message with the hash function H) using the private key, priv.
    If the hash is longer than the bit-length of the private key's curve order,
    the hash will be truncated to that length. This applies Deterministic ECDSA
    as specified in FIPS 186-5 and RFC 6979.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
