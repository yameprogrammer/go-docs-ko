# package crypto/internal/fips140/mlkem

- 원문: <https://pkg.go.dev/crypto/internal/fips140/mlkem>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `mlkem`은 [NIST FIPS 203]에 명시된 양자-내성 키 캡슐화 방법인 ML-KEM (이전에는 Kyber로 알려짐)을 구현합니다.

## 원문 요약

Package mlkem implements the quantum-resistant key encapsulation method ML-KEM (formerly known as Kyber), as specified in [NIST FIPS 203].

## API 상세 (go doc -all)

~~~text
package mlkem // import "crypto/internal/fips140/mlkem"

Package mlkem implements the quantum-resistant key encapsulation method ML-KEM
(formerly known as Kyber), as specified in NIST FIPS 203.

[NIST FIPS 203]: https://doi.org/10.6028/NIST.FIPS.203

CONSTANTS

const (
	SharedKeySize = 32
	SeedSize      = 32 + 32
)
const (
	CiphertextSize768       = k*encodingSize10 + encodingSize4
	EncapsulationKeySize768 = k*encodingSize12 + 32
)
    ML-KEM-768 parameters.

const (
	CiphertextSize1024       = k1024*encodingSize11 + encodingSize5
	EncapsulationKeySize1024 = k1024*encodingSize12 + 32
)
    ML-KEM-1024 parameters.


FUNCTIONS

func TestingOnlyExpandedBytes1024(dk *DecapsulationKey1024) []byte
    TestingOnlyExpandedBytes1024 returns the decapsulation key as a byte slice
    using the full expanded NIST encoding.

    This should only be used for ACVP testing. For all other purposes prefer the
    Bytes method that returns the (much smaller) seed.

func TestingOnlyExpandedBytes768(dk *DecapsulationKey768) []byte
    TestingOnlyExpandedBytes768 returns the decapsulation key as a byte slice
    using the full expanded NIST encoding.

    This should only be used for ACVP testing. For all other purposes prefer the
    Bytes method that returns the (much smaller) seed.


TYPES

type DecapsulationKey1024 struct {
	// Has unexported fields.
}
    A DecapsulationKey1024 is the secret key used to decapsulate a shared key
    from a ciphertext. It includes various precomputed values.

func GenerateKey1024() (*DecapsulationKey1024, error)
    GenerateKey1024 generates a new decapsulation key, drawing random bytes from
    a DRBG. The decapsulation key must be kept secret.

func GenerateKeyInternal1024(d, z *[32]byte) *DecapsulationKey1024
    GenerateKeyInternal1024 is a derandomized version of GenerateKey1024,
    exclusively for use in tests.

func NewDecapsulationKey1024(seed []byte) (*DecapsulationKey1024, error)
    NewDecapsulationKey1024 parses a decapsulation key from a 64-byte seed in
    the "d || z" form. The seed must be uniformly random.

func TestingOnlyNewDecapsulationKey1024(b []byte) (*DecapsulationKey1024, error)
    TestingOnlyNewDecapsulationKey1024 parses a decapsulation key from its
    expanded NIST format.

    Bytes() must not be called on the returned key, as it will not produce the
    original seed.

    This function should only be used for ACVP testing. Prefer
    NewDecapsulationKey1024 for all other purposes.

func (dk *DecapsulationKey1024) Bytes() []byte
    Bytes returns the decapsulation key as a 64-byte seed in the "d || z" form.

    The decapsulation key must be kept secret.

func (dk *DecapsulationKey1024) Decapsulate(ciphertext []byte) (sharedKey []byte, err error)
    Decapsulate generates a shared key from a ciphertext and a decapsulation
    key. If the ciphertext is not valid, Decapsulate returns an error.

    The shared key must be kept secret.

func (dk *DecapsulationKey1024) EncapsulationKey() *EncapsulationKey1024
    EncapsulationKey returns the public encapsulation key necessary to produce
    ciphertexts.

type DecapsulationKey768 struct {
	// Has unexported fields.
}
    A DecapsulationKey768 is the secret key used to decapsulate a shared key
    from a ciphertext. It includes various precomputed values.

func GenerateKey768() (*DecapsulationKey768, error)
    GenerateKey768 generates a new decapsulation key, drawing random bytes from
    a DRBG. The decapsulation key must be kept secret.

func GenerateKeyInternal768(d, z *[32]byte) *DecapsulationKey768
    GenerateKeyInternal768 is a derandomized version of GenerateKey768,
    exclusively for use in tests.

func NewDecapsulationKey768(seed []byte) (*DecapsulationKey768, error)
    NewDecapsulationKey768 parses a decapsulation key from a 64-byte seed in the
    "d || z" form. The seed must be uniformly random.

func TestingOnlyNewDecapsulationKey768(b []byte) (*DecapsulationKey768, error)
    TestingOnlyNewDecapsulationKey768 parses a decapsulation key from its
    expanded NIST format.

    Bytes() must not be called on the returned key, as it will not produce the
    original seed.

    This function should only be used for ACVP testing. Prefer
    NewDecapsulationKey768 for all other purposes.

func (dk *DecapsulationKey768) Bytes() []byte
    Bytes returns the decapsulation key as a 64-byte seed in the "d || z" form.

    The decapsulation key must be kept secret.

func (dk *DecapsulationKey768) Decapsulate(ciphertext []byte) (sharedKey []byte, err error)
    Decapsulate generates a shared key from a ciphertext and a decapsulation
    key. If the ciphertext is not valid, Decapsulate returns an error.

    The shared key must be kept secret.

func (dk *DecapsulationKey768) EncapsulationKey() *EncapsulationKey768
    EncapsulationKey returns the public encapsulation key necessary to produce
    ciphertexts.

type EncapsulationKey1024 struct {
	// Has unexported fields.
}
    An EncapsulationKey1024 is the public key used to produce ciphertexts to be
    decapsulated by the corresponding DecapsulationKey1024.

func NewEncapsulationKey1024(encapsulationKey []byte) (*EncapsulationKey1024, error)
    NewEncapsulationKey1024 parses an encapsulation key from its encoded form.
    If the encapsulation key is not valid, NewEncapsulationKey1024 returns an
    error.

func (ek *EncapsulationKey1024) Bytes() []byte
    Bytes returns the encapsulation key as a byte slice.

func (ek *EncapsulationKey1024) Encapsulate() (sharedKey, ciphertext []byte)
    Encapsulate generates a shared key and an associated ciphertext from an
    encapsulation key, drawing random bytes from a DRBG.

    The shared key must be kept secret.

func (ek *EncapsulationKey1024) EncapsulateInternal(m *[32]byte) (sharedKey, ciphertext []byte)
    EncapsulateInternal is a derandomized version of Encapsulate, exclusively
    for use in tests.

type EncapsulationKey768 struct {
	// Has unexported fields.
}
    An EncapsulationKey768 is the public key used to produce ciphertexts to be
    decapsulated by the corresponding DecapsulationKey768.

func NewEncapsulationKey768(encapsulationKey []byte) (*EncapsulationKey768, error)
    NewEncapsulationKey768 parses an encapsulation key from its encoded form. If
    the encapsulation key is not valid, NewEncapsulationKey768 returns an error.

func (ek *EncapsulationKey768) Bytes() []byte
    Bytes returns the encapsulation key as a byte slice.

func (ek *EncapsulationKey768) Encapsulate() (sharedKey, ciphertext []byte)
    Encapsulate generates a shared key and an associated ciphertext from an
    encapsulation key, drawing random bytes from a DRBG.

    The shared key must be kept secret.

func (ek *EncapsulationKey768) EncapsulateInternal(m *[32]byte) (sharedKey, ciphertext []byte)
    EncapsulateInternal is a derandomized version of Encapsulate, exclusively
    for use in tests.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
