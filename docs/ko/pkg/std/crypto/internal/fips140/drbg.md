# package crypto/internal/fips140/drbg

- 원문: <https://pkg.go.dev/crypto/internal/fips140/drbg>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `drbg`는 FIPS 코드에서 사용할 수 있는 암호학적으로 안전한 랜덤 바이트를 제공합니다.

## 원문 요약

Package drbg provides cryptographically secure random bytes usable by FIPS code.

## API 상세 (go doc -all)

~~~text
package drbg // import "crypto/internal/fips140/drbg"

Package drbg provides cryptographically secure random bytes usable by FIPS code.
In FIPS mode it uses an SP 800-90A Rev. 1 Deterministic Random Bit Generator
(DRBG). Otherwise, it uses the operating system's random number generator.

CONSTANTS

const (
	SeedSize = keySize + aes.BlockSize
)

FUNCTIONS

func IsDefaultReader(r io.Reader) bool
    IsDefaultReader reports whether the r embeds the DefaultReader type.

func Read(b []byte)
    Read fills b with cryptographically secure random bytes. In FIPS mode,
    it uses an SP 800-90A Rev. 1 Deterministic Random Bit Generator (DRBG).
    Otherwise, it uses the operating system's random number generator.

func ReadWithReader(r io.Reader, b []byte) error
    ReadWithReader uses Reader to fill b with cryptographically secure random
    bytes. It is intended for use in APIs that expose a rand io.Reader.

func SetTestingReader(r io.Reader)
    SetTestingReader sets a global, deterministic cryptographic randomness
    source for testing purposes. Its Read method must never return an error,
    it must never return short, and it must be safe for concurrent use.

    This is only intended to be used by the testing/cryptotest package.


TYPES

type Counter struct {
	// Has unexported fields.
}
    Counter is an SP 800-90A Rev. 1 CTR_DRBG instantiated with AES-256.

    Per Table 3, it has a security strength of 256 bits, a seed size of 384
    bits, a counter length of 128 bits, a reseed interval of 2^48 requests,
    and a maximum request size of 2^19 bits (2^16 bytes, 64 KiB).

    We support a narrow range of parameters that fit the needs of our RNG:
    AES-256, no derivation function, no personalization string, no prediction
    resistance, and 384-bit additional input.

    WARNING: this type provides tightly scoped support for the DRBG
    functionality we need for FIPS 140-3 _only_. This type _should not_ be used
    outside of the FIPS 140-3 module for any other use.

    In particular, as documented, Counter does not support the derivation
    function, or personalization strings which are necessary for safely using
    this DRBG for generic purposes without leaking sensitive values.

func NewCounter(entropy *[SeedSize]byte) *Counter

func (c *Counter) Generate(out []byte, additionalInput *[SeedSize]byte) (reseedRequired bool)
    Generate produces at most maxRequestSize bytes of random data in out.

func (c *Counter) Reseed(entropy, additionalInput *[SeedSize]byte)

type DefaultReader struct{}
    DefaultReader is a sentinel type, embedded in the default
    crypto/rand.Reader, used to recognize it when passed to APIs that accept a
    rand io.Reader.

    Any io.Reader that embeds this type is assumed to call Read as its
    io.Reader.Read method.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
