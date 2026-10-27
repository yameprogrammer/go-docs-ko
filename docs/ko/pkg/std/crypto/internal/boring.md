# package crypto/internal/boring

- 원문: <https://pkg.go.dev/crypto/internal/boring>
- 분류: Go 표준 라이브러리

## 한국어 요약

`boring` 패키지는 BoringCrypto 구현 함수들에 대한 액세스를 제공합니다.

## 원문 요약

Package boring provides access to BoringCrypto implementation functions.

## API 상세 (go doc -all)

~~~text
package boring // import "crypto/internal/boring"

Package boring provides access to BoringCrypto implementation functions.
Check the constant Enabled to find out whether BoringCrypto is available.
If BoringCrypto is not available, the functions in this package all panic.

CONSTANTS

const Enabled = available
    Enabled reports whether BoringCrypto is available. When enabled is false,
    all functions in this package panic.

    BoringCrypto is only available on linux/amd64 and linux/arm64 systems.

const RandReader = randReader(0)

FUNCTIONS

func DecryptRSANoPadding(priv *PrivateKeyRSA, ciphertext []byte) ([]byte, error)
func DecryptRSAOAEP(h, mgfHash hash.Hash, priv *PrivateKeyRSA, ciphertext, label []byte) ([]byte, error)
func DecryptRSAPKCS1(priv *PrivateKeyRSA, ciphertext []byte) ([]byte, error)
func ECDH(*PrivateKeyECDH, *PublicKeyECDH) ([]byte, error)
func EncryptRSANoPadding(pub *PublicKeyRSA, msg []byte) ([]byte, error)
func EncryptRSAOAEP(h, mgfHash hash.Hash, pub *PublicKeyRSA, msg, label []byte) ([]byte, error)
func EncryptRSAPKCS1(pub *PublicKeyRSA, msg []byte) ([]byte, error)
func NewAESCipher(key []byte) (cipher.Block, error)
func NewGCMTLS(cipher.Block) (cipher.AEAD, error)
func NewGCMTLS13(cipher.Block) (cipher.AEAD, error)
func NewHMAC(h func() hash.Hash, key []byte) hash.Hash
func NewSHA1() hash.Hash
func NewSHA224() hash.Hash
func NewSHA256() hash.Hash
func NewSHA384() hash.Hash
func NewSHA512() hash.Hash
func SHA1([]byte) [20]byte
func SHA224([]byte) [28]byte
func SHA256([]byte) [32]byte
func SHA384([]byte) [48]byte
func SHA512([]byte) [64]byte
func SignMarshalECDSA(priv *PrivateKeyECDSA, hash []byte) ([]byte, error)
func SignRSAPKCS1v15(priv *PrivateKeyRSA, h crypto.Hash, hashed []byte) ([]byte, error)
func SignRSAPSS(priv *PrivateKeyRSA, h crypto.Hash, hashed []byte, saltLen int) ([]byte, error)
func Unreachable()
    Unreachable marks code that should be unreachable when BoringCrypto is in
    use. It is a no-op without BoringCrypto.

func UnreachableExceptTests()
    UnreachableExceptTests marks code that should be unreachable when
    BoringCrypto is in use. It is a no-op without BoringCrypto.

func VerifyECDSA(pub *PublicKeyECDSA, hash []byte, sig []byte) bool
func VerifyRSAPKCS1v15(pub *PublicKeyRSA, h crypto.Hash, hashed, sig []byte) error
func VerifyRSAPSS(pub *PublicKeyRSA, h crypto.Hash, hashed, sig []byte, saltLen int) error

TYPES

type BigInt []uint
    A BigInt is the raw words from a BigInt. This definition allows us to
    avoid importing math/big. Conversion between BigInt and *big.Int is in
    crypto/internal/boring/bbig.

func GenerateKeyECDSA(curve string) (X, Y, D BigInt, err error)

func GenerateKeyRSA(bits int) (N, E, D, P, Q, Dp, Dq, Qinv BigInt, err error)

type PrivateKeyECDH struct{}

func GenerateKeyECDH(string) (*PrivateKeyECDH, []byte, error)

func NewPrivateKeyECDH(string, []byte) (*PrivateKeyECDH, error)

func (*PrivateKeyECDH) PublicKey() (*PublicKeyECDH, error)

type PrivateKeyECDSA struct {
	// Has unexported fields.
}

func NewPrivateKeyECDSA(curve string, X, Y, D BigInt) (*PrivateKeyECDSA, error)

type PrivateKeyRSA struct {
	// Has unexported fields.
}

func NewPrivateKeyRSA(N, E, D, P, Q, Dp, Dq, Qinv BigInt) (*PrivateKeyRSA, error)

type PublicKeyECDH struct{}

func NewPublicKeyECDH(string, []byte) (*PublicKeyECDH, error)

func (*PublicKeyECDH) Bytes() []byte

type PublicKeyECDSA struct {
	// Has unexported fields.
}

func NewPublicKeyECDSA(curve string, X, Y BigInt) (*PublicKeyECDSA, error)

type PublicKeyRSA struct {
	// Has unexported fields.
}

func NewPublicKeyRSA(N, E BigInt) (*PublicKeyRSA, error)
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
