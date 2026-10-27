# package crypto/pbkdf2

- 원문: <https://pkg.go.dev/crypto/pbkdf2>
- 분류: Go 표준 라이브러리

## 한국어 요약

`pbkdf2` 패키지는 RFC 8018 (PKCS #5 v2.1)에 정의된 키 유도 함수 PBKDF2를 구현합니다.

## 원문 요약

Package pbkdf2 implements the key derivation function PBKDF2 as defined in RFC 8018 (PKCS #5 v2.1).

## API 상세 (go doc -all)

~~~text
package pbkdf2 // import "crypto/pbkdf2"

Package pbkdf2 implements the key derivation function PBKDF2 as defined in RFC
8018 (PKCS #5 v2.1).

A key derivation function is useful when encrypting data based on a password
or any other not-fully-random data. It uses a pseudorandom function to derive a
secure encryption key based on the password.

FUNCTIONS

func Key[Hash hash.Hash](h func() Hash, password string, salt []byte, iter, keyLength int) ([]byte, error)
    Key derives a key from the password, salt and iteration count, returning a
    []byte of length keyLength that can be used as cryptographic key. The key is
    derived based on the method described as PBKDF2 with the HMAC variant using
    the supplied hash function.

    For example, to use a HMAC-SHA-1 based PBKDF2 key derivation function, you
    can get a derived key for e.g. AES-256 (which needs a 32-byte key) by doing:

        dk, err := pbkdf2.Key(sha1.New, "some password", salt, 4096, 32)

    Remember to get a good random salt. At least 8 bytes is recommended by the
    RFC.

    Using a higher iteration count will increase the cost of an exhaustive
    search but will also make derivation proportionally slower.

    keyLength must be a positive integer between 1 and (2^32 - 1) * h.Size().
    Setting keyLength to a value outside of this range will result in an error.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
