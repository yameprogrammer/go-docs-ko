# package crypto/internal/fips140/aes/gcm

- 원문: <https://pkg.go.dev/crypto/internal/fips140/aes/gcm>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package gcm // import "crypto/internal/fips140/aes/gcm"


FUNCTIONS

func GHASH(key *[16]byte, inputs ...[]byte) []byte
    GHASH is exposed to allow crypto/cipher to implement non-AES GCM modes.
    It is not allowed as a stand-alone operation in FIPS mode because it is not
    ACVP tested.

func SealWithRandomNonce(g *GCM, nonce, out, plaintext, additionalData []byte)
    SealWithRandomNonce encrypts plaintext to out, and writes a random
    nonce to nonce. nonce must be 12 bytes, and out must be 16 bytes longer
    than plaintext. out and plaintext may overlap exactly or not at all.
    additionalData and out must not overlap.

    This complies with FIPS 140-3 IG C.H Scenario 2.

    Note that this is NOT a [cipher.AEAD].Seal method.


TYPES

type CMAC struct {
	// Has unexported fields.
}
    CMAC implements the CMAC mode from NIST SP 800-38B.

    It is optimized for use in Counter KDF (SP 800-108r1) and XAES-256-GCM
    (https://c2sp.org/XAES-256-GCM), rather than for exposing it to applications
    as a stand-alone MAC.

func NewCMAC(b *aes.Block) *CMAC

func (c *CMAC) MAC(m []byte) [aes.BlockSize]byte

type CounterKDF struct {
	// Has unexported fields.
}
    CounterKDF implements a KDF in Counter Mode instantiated with CMAC-AES,
    according to NIST SP 800-108 Revision 1 Update 1, Section 4.1.

    It produces a 256-bit output, and accepts a 8-bit Label and a 96-bit
    Context. It uses a counter of 16 bits placed before the fixed data. The
    fixed data is the sequence Label || 0x00 || Context. The L field is omitted,
    since the output key length is fixed.

    It's optimized for use in XAES-256-GCM (https://c2sp.org/XAES-256-GCM),
    rather than for exposing it to applications as a stand-alone KDF.

func NewCounterKDF(b *aes.Block) *CounterKDF
    NewCounterKDF creates a new CounterKDF with the given key.

func (kdf *CounterKDF) DeriveKey(label byte, context [12]byte) [32]byte
    DeriveKey derives a key from the given label and context.

type GCM struct {
	// Has unexported fields.
}
    GCM represents a Galois Counter Mode with a specific key.

func New(cipher *aes.Block, nonceSize, tagSize int) (*GCM, error)

func (g *GCM) NonceSize() int

func (g *GCM) Open(dst, nonce, ciphertext, data []byte) ([]byte, error)

func (g *GCM) Overhead() int

func (g *GCM) Seal(dst, nonce, plaintext, data []byte) []byte

type GCMWithCounterNonce struct {
	// Has unexported fields.
}

func NewGCMForSSH(cipher *aes.Block) (*GCMWithCounterNonce, error)
    NewGCMForSSH returns a new AEAD that works like GCM, but enforces the
    construction of nonces as specified in RFC 5647.

    This complies with FIPS 140-3 IG C.H Scenario 1.d.

func NewGCMForTLS12(cipher *aes.Block) (*GCMWithCounterNonce, error)
    NewGCMForTLS12 returns a new AEAD that works like GCM, but enforces the
    construction of nonces as specified in RFC 5288, Section 3 and RFC 9325,
    Section 7.2.1.

    This complies with FIPS 140-3 IG C.H Scenario 1.a.

func NewGCMWithCounterNonce(cipher *aes.Block) (*GCMWithCounterNonce, error)
    NewGCMWithCounterNonce returns a new AEAD that works like GCM, but enforces
    the construction of deterministic nonces. The nonce must be 96 bits,
    the first 32 bits must be an encoding of the module name, and the last
    64 bits must be a counter. The starting value of the counter is set on
    the first call to Seal, and each subsequent call must increment it as a
    big-endian uint64. If the counter reaches the starting value minus one,
    Seal will panic.

    This complies with FIPS 140-3 IG C.H Scenario 3.

func (g *GCMWithCounterNonce) NonceSize() int

func (g *GCMWithCounterNonce) Open(dst, nonce, ciphertext, data []byte) ([]byte, error)

func (g *GCMWithCounterNonce) Overhead() int

func (g *GCMWithCounterNonce) Seal(dst, nonce, plaintext, data []byte) []byte
    Seal implements the [cipher.AEAD] interface, checking that the nonce prefix
    is stable and that the counter is strictly increasing.

    It is not safe for concurrent use.

type GCMWithXORCounterNonce struct {
	// Has unexported fields.
}

func NewGCMForHPKE(cipher *aes.Block) (*GCMWithXORCounterNonce, error)
    NewGCMForHPKE returns a new AEAD that works like GCM, but enforces the
    construction of nonces as specified in RFC 9180, Section 5.2.

    This complies with FIPS 140-3 IG C.H Scenario 5.

func NewGCMForQUIC(cipher *aes.Block, iv []byte) (*GCMWithXORCounterNonce, error)
    NewGCMForQUIC returns a new AEAD that works like GCM, but enforces the
    construction of nonces as specified in RFC 9001, Section 5.3.

    Unlike in TLS 1.3, the QUIC nonce counter does not always start at zero,
    as the packet number does not reset on key updates, so the XOR mask must
    be provided explicitly instead of being learned on the first Seal call.
    Note that the nonce passed to Seal must already be XOR'd with the IV,
    the IV is provided here only to allow Seal to enforce that the counter is
    strictly increasing.

    This complies with FIPS 140-3 IG C.H Scenario 5.

func NewGCMForTLS13(cipher *aes.Block) (*GCMWithXORCounterNonce, error)
    NewGCMForTLS13 returns a new AEAD that works like GCM, but enforces the
    construction of nonces as specified in RFC 8446, Section 5.3.

    This complies with FIPS 140-3 IG C.H Scenario 1.a.

func NewGCMWithXORCounterNonce(cipher *aes.Block) (*GCMWithXORCounterNonce, error)
    NewGCMWithXORCounterNonce returns a new AEAD that works like GCM,
    but enforces the construction of deterministic nonces. The nonce must be 96
    bits, the first 32 bits must be an encoding of the module name, and the last
    64 bits must be a counter XOR'd with a fixed value. The module name and XOR
    mask can be set with [GCMWithCounterNonce.SetNoncePrefixAndMask], or they
    are set on the first call to Seal, assuming the counter starts at zero.
    Each subsequent call must increment the counter as a big-endian uint64.
    If the counter reaches 2⁶⁴ minus one, Seal will panic.

    This complies with FIPS 140-3 IG C.H Scenario 3.

func (g *GCMWithXORCounterNonce) NonceSize() int

func (g *GCMWithXORCounterNonce) Open(dst, nonce, ciphertext, data []byte) ([]byte, error)

func (g *GCMWithXORCounterNonce) Overhead() int

func (g *GCMWithXORCounterNonce) Seal(dst, nonce, plaintext, data []byte) []byte
    Seal implements the [cipher.AEAD] interface, checking that the nonce prefix
    is stable and that the counter is strictly increasing.

    It is not safe for concurrent use.

func (g *GCMWithXORCounterNonce) SetNoncePrefixAndMask(nonce []byte) error
    SetNoncePrefixAndMask sets the fixed prefix and XOR mask for the nonces used
    in Seal. It must be called before the first call to Seal.

    The first 32 bits of nonce are used as the fixed prefix, and the last 64
    bits are used as the XOR mask.

    Note that Seal expects the nonce to be already XOR'd with the mask. The mask
    is provided here only to allow Seal to enforce that the counter is strictly
    increasing.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
