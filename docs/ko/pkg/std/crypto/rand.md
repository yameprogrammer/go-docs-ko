# package crypto/rand

- 원문: <https://pkg.go.dev/crypto/rand>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `rand`은 암호학적으로 안전한 난수 생성기를 구현합니다.

## 원문 요약

Package rand implements a cryptographically secure random number generator.

## API 상세 (go doc -all)

~~~text
package rand // import "crypto/rand"

Package rand implements a cryptographically secure random number generator.

VARIABLES

var Reader io.Reader = rand.Reader
    Reader is a global, shared instance of a cryptographically secure random
    number generator. It is safe for concurrent use.

      - On Linux, FreeBSD, Dragonfly, and Solaris, Reader uses getrandom(2).
      - On legacy Linux (< 3.17), Reader opens /dev/urandom on first use.
      - On macOS, iOS, and OpenBSD Reader, uses arc4random_buf(3).
      - On NetBSD, Reader uses the kern.arandom sysctl.
      - On Windows, Reader uses the ProcessPrng API.
      - On js/wasm, Reader uses the Web Crypto API.
      - On wasip1/wasm, Reader uses random_get.

    In FIPS 140-3 mode, the output passes through an SP 800-90A Rev.
    1 Deterministric Random Bit Generator (DRBG).


FUNCTIONS

func Int(rand io.Reader, max *big.Int) (n *big.Int, err error)
    Int returns a uniform random value in [0, max). It panics if max <= 0,
    and returns an error if rand.Read returns one.

func Prime(r io.Reader, bits int) (*big.Int, error)
    Prime returns a number of the given bit length that is prime with high
    probability. Prime will return error for any error returned by rand.Read or
    if bits < 2.

    Since Go 1.26, a secure source of random bytes is always used,
    and the Reader is ignored unless GODEBUG=cryptocustomrand=1 is set.
    This setting will be removed in a future Go release. Instead, use
    testing/cryptotest.SetGlobalRandom.

func Read(b []byte) (n int, err error)
    Read fills b with cryptographically secure random bytes. It never returns an
    error, and always fills b entirely.

    Read calls io.ReadFull on Reader and crashes the program irrecoverably if
    an error is returned. The default Reader uses operating system APIs that are
    documented to never return an error on all but legacy Linux systems.

func Text() string
    Text returns a cryptographically random string using the standard RFC
    4648 base32 alphabet for use when a secret string, token, password, or
    other text is needed. The result contains at least 128 bits of randomness,
    enough to prevent brute force guessing attacks and to make the likelihood
    of collisions vanishingly small. A future version may return longer texts as
    needed to maintain those properties.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
