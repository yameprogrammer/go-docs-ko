# package vendor/golang.org/x/crypto/chacha20poly1305

- 원문: <https://pkg.go.dev/vendor/golang.org/x/crypto/chacha20poly1305>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `chacha20poly1305`는 RFC 8439 및 draft-irtf-cfrg-xchacha-01에 명시된 ChaCha20-Poly1305 AEAD 및 그 확장된 nonce 변형 XChaCha20-Poly1305를 구현합니다.

## 원문 요약

Package chacha20poly1305 implements the ChaCha20-Poly1305 AEAD and its extended nonce variant XChaCha20-Poly1305, as specified in RFC 8439 and draft-irtf-cfrg-xchacha-01.

## API 상세 (go doc -all)

~~~text
package chacha20poly1305 // import "vendor/golang.org/x/crypto/chacha20poly1305"

Package chacha20poly1305 implements the ChaCha20-Poly1305 AEAD and its
extended nonce variant XChaCha20-Poly1305, as specified in RFC 8439 and
draft-irtf-cfrg-xchacha-01.

CONSTANTS

const (
	// KeySize is the size of the key used by this AEAD, in bytes.
	KeySize = 32

	// NonceSize is the size of the nonce used with the standard variant of this
	// AEAD, in bytes.
	//
	// Note that this is too short to be safely generated at random if the same
	// key is reused more than 2³² times.
	NonceSize = 12

	// NonceSizeX is the size of the nonce used with the XChaCha20-Poly1305
	// variant of this AEAD, in bytes.
	NonceSizeX = 24

	// Overhead is the size of the Poly1305 authentication tag, and the
	// difference between a ciphertext length and its plaintext.
	Overhead = 16
)

FUNCTIONS

func New(key []byte) (cipher.AEAD, error)
    New returns a ChaCha20-Poly1305 AEAD that uses the given 256-bit key.

func NewX(key []byte) (cipher.AEAD, error)
    NewX returns a XChaCha20-Poly1305 AEAD that uses the given 256-bit key.

    XChaCha20-Poly1305 is a ChaCha20-Poly1305 variant that takes a longer nonce,
    suitable to be generated randomly without risk of collisions. It should be
    preferred when nonce uniqueness cannot be trivially ensured, or whenever
    nonces are randomly generated.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
