# package crypto/internal/fips140/rsa

- 원문: <https://pkg.go.dev/crypto/internal/fips140/rsa>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package rsa // import "crypto/internal/fips140/rsa"


VARIABLES

var ErrDecryption = errors.New("crypto/rsa: decryption error")
var ErrMessageTooLong = errors.New("crypto/rsa: message too long for RSA key size")
var ErrVerification = errors.New("crypto/rsa: verification error")

FUNCTIONS

func DecryptOAEP(hash, mgfHash hash.Hash, priv *PrivateKey, ciphertext []byte, label []byte) ([]byte, error)
    DecryptOAEP decrypts ciphertext using RSAES-OAEP.

func DecryptWithCheck(priv *PrivateKey, ciphertext []byte) ([]byte, error)
    DecryptWithCheck performs the RSA private key operation and checks the
    result to defend against errors in the CRT computation.

func DecryptWithoutCheck(priv *PrivateKey, ciphertext []byte) ([]byte, error)
    DecryptWithoutCheck performs the RSA private key operation.

func Encrypt(pub *PublicKey, plaintext []byte) ([]byte, error)
    Encrypt performs the RSA public key operation.

func EncryptOAEP(hash, mgfHash hash.Hash, random io.Reader, pub *PublicKey, msg []byte, label []byte) ([]byte, error)
    EncryptOAEP encrypts the given message with RSAES-OAEP.

func PSSMaxSaltLength(pub *PublicKey, hash hash.Hash) (int, error)
    PSSMaxSaltLength returns the maximum salt length for a given public key and
    hash function.

func SignPKCS1v15(priv *PrivateKey, hash string, hashed []byte) ([]byte, error)
    SignPKCS1v15 calculates an RSASSA-PKCS1-v1.5 signature.

    hash is the name of the hash function as returned by crypto.Hash.String or
    the empty string to indicate that the message is signed directly.

func SignPSS(rand io.Reader, priv *PrivateKey, hash hash.Hash, hashed []byte, saltLength int) ([]byte, error)
    SignPSS calculates the signature of hashed using RSASSA-PSS.

func TestingOnlyLargeExponentDecryptOAEP(hash, mgfHash hash.Hash, priv *TestingOnlyLargeExponentPrivateKey, ciphertext []byte, label []byte) ([]byte, error)
    TestingOnlyLargeExponentDecryptOAEP decrypts ciphertext using RSAES-OAEP
    with a private key that has a large public exponent. It is only meant for
    ACVP testing.

func TestingOnlyLargeExponentEncryptOAEP(hash, mgfHash hash.Hash, random io.Reader, pub *TestingOnlyLargeExponentPublicKey, msg []byte, label []byte) ([]byte, error)
    TestingOnlyLargeExponentEncryptOAEP encrypts the given message with
    RSAES-OAEP using a public key with a large exponent. It is only meant for
    ACVP testing.

func TestingOnlyLargeExponentVerifyPKCS1v15(pub *TestingOnlyLargeExponentPublicKey, hash string, hashed []byte, sig []byte) error
func TestingOnlyLargeExponentVerifyPSS(pub *TestingOnlyLargeExponentPublicKey, hash hash.Hash, digest []byte, sig []byte) error
func VerifyPKCS1v15(pub *PublicKey, hash string, hashed []byte, sig []byte) error
    VerifyPKCS1v15 verifies an RSASSA-PKCS1-v1.5 signature.

    hash is the name of the hash function as returned by crypto.Hash.String or
    the empty string to indicate that the message is signed directly.

func VerifyPSS(pub *PublicKey, hash hash.Hash, digest []byte, sig []byte) error
    VerifyPSS verifies sig with RSASSA-PSS automatically detecting the salt
    length.

func VerifyPSSWithSaltLength(pub *PublicKey, hash hash.Hash, digest []byte, sig []byte, saltLength int) error
    VerifyPSSWithSaltLength verifies sig with RSASSA-PSS and an expected salt
    length.


TYPES

type PrivateKey struct {
	// Has unexported fields.
}

func GenerateKey(rand io.Reader, bits int) (*PrivateKey, error)
    GenerateKey generates a new RSA key pair of the given bit size. bits must be
    at least 32.

    It follows the process described at c2sp.org/det-keygen, which is compliant
    with FIPS 186-5, Appendix A.1, IFC Key Pair Generation and FIPS 186-5,
    Appendix A.1.3, Generation of Random Primes that are Probably Prime.
    The prime candidates are drawn from rand, which in production will be
    the global DRBG, while in tests can be an HMAC_DRBG as specified in
    c2sp.org/det-keygen, to allow using its tests vectors.

func NewPrivateKey(N []byte, e int, d, P, Q []byte) (*PrivateKey, error)
    NewPrivateKey creates a new RSA private key from the given parameters.

    All values are in big-endian byte slice format, and may have leading zeros
    or be shorter if leading zeroes were trimmed.

func NewPrivateKeyWithPrecomputation(N []byte, e int, d, P, Q, dP, dQ, qInv []byte) (*PrivateKey, error)
    NewPrivateKeyWithPrecomputation creates a new RSA private key from the given
    parameters, which include precomputed CRT values.

func NewPrivateKeyWithoutCRT(N []byte, e int, d []byte) (*PrivateKey, error)
    NewPrivateKeyWithoutCRT creates a new RSA private key from the given
    parameters.

    This is meant for deprecated multi-prime keys, and is not FIPS 140
    compliant.

func (priv *PrivateKey) Export() (N []byte, e int, d, P, Q, dP, dQ, qInv []byte)
    Export returns the key parameters in big-endian byte slice format.

    P, Q, dP, dQ, and qInv may be nil if the key was created with
    NewPrivateKeyWithoutCRT.

func (priv *PrivateKey) PublicKey() *PublicKey

type PublicKey struct {
	N *bigmod.Modulus
	E int
}

func (pub *PublicKey) Size() int
    Size returns the modulus size in bytes. Raw signatures and ciphertexts for
    or by this public key will have the same size.

type TestingOnlyLargeExponentPrivateKey struct {
	// Has unexported fields.
}
    TestingOnlyLargeExponentPrivateKey is a variant of PrivateKey that supports
    large public exponents. It is only meant for supporting the full ACVP test
    suite. This type must not be used in production code.

func TestingOnlyNewLargeExponentPrivateKeyWithPrecomputation(N []byte, e []byte, d, P, Q, dP, dQ, qInv []byte) (*TestingOnlyLargeExponentPrivateKey, error)
    TestingOnlyNewLargeExponentPrivateKeyWithPrecomputation creates a new
    RSA private key with a large public exponent from the given parameters.
    It is only meant for ACVP testing.

func (priv *TestingOnlyLargeExponentPrivateKey) Size() int

type TestingOnlyLargeExponentPublicKey struct {
	N *bigmod.Modulus
	// E is the public exponent, represented as a big-endian byte slice.
	E []byte
}
    TestingOnlyLargeExponentPublicKey is a variant of PublicKey that supports
    large public exponents. It is only meant for supporting the full ACVP test
    suite, which unfortunately forces us to choose between a fixed exponent and
    the full (2¹⁶, 2²⁵⁶) range. This type must not be used in production code,
    nor for e values < 2³¹, which instead must use PublicKey.

func (pub *TestingOnlyLargeExponentPublicKey) Size() int
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
