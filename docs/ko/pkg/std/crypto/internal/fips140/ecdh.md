# package crypto/internal/fips140/ecdh

- 원문: <https://pkg.go.dev/crypto/internal/fips140/ecdh>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package ecdh // import "crypto/internal/fips140/ecdh"


FUNCTIONS

func ECDH[P Point[P]](c *Curve[P], k *PrivateKey, peer *PublicKey) ([]byte, error)

TYPES

type Curve[P Point[P]] struct {
	N []byte
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
}
    Point is a generic constraint for the nistec Point types.

type PrivateKey struct {
	// Has unexported fields.
}

func GenerateKey[P Point[P]](c *Curve[P], rand io.Reader) (*PrivateKey, error)
    GenerateKey generates a new ECDSA private key pair for the specified curve.

func NewPrivateKey[P Point[P]](c *Curve[P], key []byte) (*PrivateKey, error)

func (priv *PrivateKey) Bytes() []byte

func (priv *PrivateKey) PublicKey() *PublicKey

type PublicKey struct {
	// Has unexported fields.
}

func NewPublicKey[P Point[P]](c *Curve[P], key []byte) (*PublicKey, error)

func (pub *PublicKey) Bytes() []byte
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
