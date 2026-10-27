# package crypto/internal/fips140/mldsa

- 원문: <https://pkg.go.dev/crypto/internal/fips140/mldsa>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package mldsa // import "crypto/internal/fips140/mldsa"


CONSTANTS

const (
	R  = 4294967296 // 2³²
	RR = 2365951    // R² mod q, aka R in the Montgomery domain

)
const (
	PrivateKeySize = 32

	PublicKeySize44 = 32 + 4*n*10/8
	PublicKeySize65 = 32 + 6*n*10/8
	PublicKeySize87 = 32 + 8*n*10/8

	SignatureSize44 = 128/4 + 4*n*(17+1)/8 + 80 + 4
	SignatureSize65 = 192/4 + 5*n*(19+1)/8 + 55 + 6
	SignatureSize87 = 256/4 + 7*n*(19+1)/8 + 75 + 8
)

FUNCTIONS

func Sign(priv *PrivateKey, msg []byte, context string) ([]byte, error)
func SignDeterministic(priv *PrivateKey, msg []byte, context string) ([]byte, error)
func SignExternalMu(priv *PrivateKey, μ []byte) ([]byte, error)
func SignExternalMuDeterministic(priv *PrivateKey, μ []byte) ([]byte, error)
func TestingOnlyPrivateKeySemiExpandedBytes(priv *PrivateKey) []byte
func TestingOnlySignExternalMuWithRandom(priv *PrivateKey, μ []byte, random []byte) ([]byte, error)
func TestingOnlySignWithRandom(priv *PrivateKey, msg []byte, context string, random []byte) ([]byte, error)
func Verify(pub *PublicKey, msg, sig []byte, context string) error
func VerifyExternalMu(pub *PublicKey, μ []byte, sig []byte) error

TYPES

type PrivateKey struct {
	// Has unexported fields.
}

func GenerateKey44() *PrivateKey

func GenerateKey65() *PrivateKey

func GenerateKey87() *PrivateKey

func NewPrivateKey44(seed []byte) (*PrivateKey, error)

func NewPrivateKey65(seed []byte) (*PrivateKey, error)

func NewPrivateKey87(seed []byte) (*PrivateKey, error)

func TestingOnlyNewPrivateKeyFromSemiExpanded(sk []byte) (*PrivateKey, error)
    TestingOnlyNewPrivateKeyFromSemiExpanded creates a PrivateKey from a
    semi-expanded private key encoding, for testing purposes. It rejects
    inconsistent keys.

    PrivateKey.Bytes must NOT be called on the resulting key, as it will produce
    a random value.

func (priv *PrivateKey) Bytes() []byte

func (priv *PrivateKey) Equal(x *PrivateKey) bool

func (priv *PrivateKey) PublicKey() *PublicKey

type PublicKey struct {
	// Has unexported fields.
}

func NewPublicKey44(pk []byte) (*PublicKey, error)

func NewPublicKey65(pk []byte) (*PublicKey, error)

func NewPublicKey87(pk []byte) (*PublicKey, error)

func (pub *PublicKey) Bytes() []byte

func (pub *PublicKey) Equal(x *PublicKey) bool

func (pub *PublicKey) Parameters() string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
