# package crypto/mldsa

- 원문: <https://pkg.go.dev/crypto/mldsa>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `mldsa`는 [FIPS 204]에 명시된 포스트 양자 ML-DSA 서명 스킴을 구현합니다.

## 원문 요약

Package mldsa implements the post-quantum ML-DSA signature scheme specified in [FIPS 204].

## API 상세 (go doc -all)

~~~text
package mldsa // import "crypto/mldsa"

Package mldsa implements the post-quantum ML-DSA signature scheme specified in
FIPS 204.

This package is unavailable if using the FIPS 140-3 Go Cryptographic Module
v1.0.0, in which case GenerateKey, NewPrivateKey, NewPublicKey, and Verify will
return an error. It is available if using v1.26.0 or later.

[FIPS 204]: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf
[FIPS 140-3 Go Cryptographic Module]: https://go.dev/doc/security/fips140

CONSTANTS

const (
	PrivateKeySize = 32

	MLDSA44PublicKeySize = 1312
	MLDSA65PublicKeySize = 1952
	MLDSA87PublicKeySize = 2592

	MLDSA44SignatureSize = 2420
	MLDSA65SignatureSize = 3309
	MLDSA87SignatureSize = 4627
)

FUNCTIONS

func Verify(pk *PublicKey, message []byte, signature []byte, opts *Options) error
    Verify reports whether signature is a valid signature of message by pk.
    If opts is nil, it's equivalent to the zero value of Options.


TYPES

type Options struct {
	// Context can be used to distinguish signatures created for different
	// purposes. It must be at most 255 bytes long, and it is empty by default.
	//
	// The same context must be used when signing and verifying a signature.
	Context string
}
    Options contains additional options for signing and verifying ML-DSA
    signatures.

func (opts *Options) HashFunc() crypto.Hash
    HashFunc returns zero, to implement the crypto.SignerOpts interface.

type Parameters struct {
	// Has unexported fields.
}
    Parameters represents one of the fixed parameter sets defined in FIPS 204.

    Most applications should use MLDSA44.

    Multiple invocations of MLDSA44, MLDSA65, or MLDSA87 will return the
    same respective value, which can be used for equality checks and switch
    statements. The returned value is safe for concurrent use.

func MLDSA44() Parameters
    MLDSA44 returns the ML-DSA-44 parameter set defined in FIPS 204.

func MLDSA65() Parameters
    MLDSA65 returns the ML-DSA-65 parameter set defined in FIPS 204.

func MLDSA87() Parameters
    MLDSA87 returns the ML-DSA-87 parameter set defined in FIPS 204.

func (params Parameters) PublicKeySize() int
    PublicKeySize returns the size of public keys for this parameter set,
    in bytes.

func (params Parameters) SignatureSize() int
    SignatureSize returns the size of signatures for this parameter set,
    in bytes.

func (params Parameters) String() string
    String returns the name of the parameter set, e.g. "ML-DSA-44".

type PrivateKey struct {
	// Has unexported fields.
}
    PrivateKey is an in-memory ML-DSA private key. It implements crypto.Signer
    and the informal extended crypto.PrivateKey interface.

    A PrivateKey is safe for concurrent use.

func GenerateKey(params Parameters) (*PrivateKey, error)
    GenerateKey generates a new random ML-DSA private key.

func NewPrivateKey(params Parameters, seed []byte) (*PrivateKey, error)
    NewPrivateKey decodes an ML-DSA private key from the given seed.

    The seed must be exactly PrivateKeySize bytes long.

func (sk *PrivateKey) Bytes() []byte
    Bytes returns the private key seed.

func (sk *PrivateKey) Equal(x crypto.PrivateKey) bool
    Equal reports whether sk and x are the same key (i.e. they are derived from
    the same seed).

    If x is not a *PrivateKey, Equal returns false.

func (sk *PrivateKey) Public() crypto.PublicKey
    Public returns the corresponding PublicKey for this private key.

    It implements the crypto.Signer interface.

func (sk *PrivateKey) PublicKey() *PublicKey
    PublicKey returns the corresponding PublicKey for this private key.

func (sk *PrivateKey) Sign(_ io.Reader, message []byte, opts crypto.SignerOpts) (signature []byte, err error)
    Sign returns a signature of the given message using this private key.

    If opts is nil or opts.HashFunc returns zero, the message is signed
    directly. If opts.HashFunc returns crypto.MLDSAMu, the provided message
    must be a pre-hashed μ message representative. opts can be of type *Options
    if a context string is desired along with a directly-signed message.
    The io.Reader argument is ignored.

[pre-hashed μ message representative]: https://www.rfc-editor.org/rfc/rfc9881.html#externalmu

func (sk *PrivateKey) SignDeterministic(message []byte, opts crypto.SignerOpts) (signature []byte, err error)
    SignDeterministic works like PrivateKey.Sign, but the signature is
    deterministic.

type PublicKey struct {
	// Has unexported fields.
}
    PublicKey is an ML-DSA public key. It implements the informal extended
    crypto.PublicKey interface.

    A PublicKey is safe for concurrent use.

func NewPublicKey(params Parameters, encoding []byte) (*PublicKey, error)
    NewPublicKey creates a new ML-DSA public key from the given encoding.

func (pk *PublicKey) Bytes() []byte
    Bytes returns the public key encoding.

func (pk *PublicKey) Equal(x crypto.PublicKey) bool
    Equal reports whether pk and x are the same key (i.e. they have the same
    encoding).

    If x is not a *PublicKey, Equal returns false.

func (pk *PublicKey) Parameters() Parameters
    Parameters returns the parameters associated with this public key.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
