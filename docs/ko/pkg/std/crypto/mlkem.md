# package crypto/mlkem

- 원문: <https://pkg.go.dev/crypto/mlkem>
- 분류: Go 표준 라이브러리

## 한국어 요약

`mlkem` 패키지는 [NIST FIPS 203]에 정의된 양자 내성 키 캡슐화 메커니즘인 ML-KEM(이전 명칭 Kyber)을 구현합니다.

## 원문 요약

Package mlkem implements the quantum-resistant key encapsulation method ML-KEM (formerly known as Kyber), as specified in [NIST FIPS 203].

## API 상세 (go doc -all)

~~~text
package mlkem // import "crypto/mlkem"

Package mlkem implements the quantum-resistant key encapsulation method ML-KEM
(formerly known as Kyber), as specified in NIST FIPS 203.

Most applications should use the ML-KEM-768 parameter set, as implemented by
DecapsulationKey768 and EncapsulationKey768.

[NIST FIPS 203]: https://doi.org/10.6028/NIST.FIPS.203

CONSTANTS

const (
	// SharedKeySize is the size of a shared key produced by ML-KEM.
	SharedKeySize = 32

	// SeedSize is the size of a seed used to generate a decapsulation key.
	SeedSize = 64

	// CiphertextSize768 is the size of a ciphertext produced by ML-KEM-768.
	CiphertextSize768 = 1088

	// EncapsulationKeySize768 is the size of an ML-KEM-768 encapsulation key.
	EncapsulationKeySize768 = 1184

	// CiphertextSize1024 is the size of a ciphertext produced by ML-KEM-1024.
	CiphertextSize1024 = 1568

	// EncapsulationKeySize1024 is the size of an ML-KEM-1024 encapsulation key.
	EncapsulationKeySize1024 = 1568
)

TYPES

type DecapsulationKey1024 struct {
	// Has unexported fields.
}
    DecapsulationKey1024 is the secret key used to decapsulate a shared key from
    a ciphertext. It includes various precomputed values.

func GenerateKey1024() (*DecapsulationKey1024, error)
    GenerateKey1024 generates a new decapsulation key, drawing random bytes from
    a secure source. The decapsulation key must be kept secret.

func NewDecapsulationKey1024(seed []byte) (*DecapsulationKey1024, error)
    NewDecapsulationKey1024 expands a decapsulation key from a 64-byte seed in
    the "d || z" form. The seed must be uniformly random.

func (dk *DecapsulationKey1024) Bytes() []byte
    Bytes returns the decapsulation key as a 64-byte seed in the "d || z" form.

    The decapsulation key must be kept secret.

func (dk *DecapsulationKey1024) Decapsulate(ciphertext []byte) (sharedKey []byte, err error)
    Decapsulate generates a shared key from a ciphertext and a decapsulation
    key. If the ciphertext is not the correct length, Decapsulate returns an
    error. A ciphertext that is the correct length but otherwise invalid will
    not return an error; instead, it will produce a shared key that does not
    match the sender's, according to FIPS 203.

    The shared key must be kept secret.

func (dk *DecapsulationKey1024) EncapsulationKey() *EncapsulationKey1024
    EncapsulationKey returns the public encapsulation key necessary to produce
    ciphertexts.

func (dk *DecapsulationKey1024) Encapsulator() crypto.Encapsulator
    Encapsulator returns the encapsulation key, like
    DecapsulationKey1024.EncapsulationKey.

    It implements crypto.Decapsulator.

type DecapsulationKey768 struct {
	// Has unexported fields.
}
    DecapsulationKey768 is the secret key used to decapsulate a shared key from
    a ciphertext. It includes various precomputed values.

func GenerateKey768() (*DecapsulationKey768, error)
    GenerateKey768 generates a new decapsulation key, drawing random bytes from
    a secure source. The decapsulation key must be kept secret.

func NewDecapsulationKey768(seed []byte) (*DecapsulationKey768, error)
    NewDecapsulationKey768 expands a decapsulation key from a 64-byte seed in
    the "d || z" form. The seed must be uniformly random.

func (dk *DecapsulationKey768) Bytes() []byte
    Bytes returns the decapsulation key as a 64-byte seed in the "d || z" form.

    The decapsulation key must be kept secret.

func (dk *DecapsulationKey768) Decapsulate(ciphertext []byte) (sharedKey []byte, err error)
    Decapsulate generates a shared key from a ciphertext and a decapsulation
    key. If the ciphertext is not the correct length, Decapsulate returns an
    error. A ciphertext that is the correct length but otherwise invalid will
    not return an error; instead, it will produce a shared key that does not
    match the sender's, according to FIPS 203.

    The shared key must be kept secret.

func (dk *DecapsulationKey768) EncapsulationKey() *EncapsulationKey768
    EncapsulationKey returns the public encapsulation key necessary to produce
    ciphertexts.

func (dk *DecapsulationKey768) Encapsulator() crypto.Encapsulator
    Encapsulator returns the encapsulation key, like
    DecapsulationKey768.EncapsulationKey.

    It implements crypto.Decapsulator.

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
    encapsulation key, drawing random bytes from a secure source.

    The shared key must be kept secret.

    For testing, derandomized encapsulation is provided by the
    crypto/mlkem/mlkemtest package.

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
    encapsulation key, drawing random bytes from a secure source.

    The shared key must be kept secret.

    For testing, derandomized encapsulation is provided by the
    crypto/mlkem/mlkemtest package.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
