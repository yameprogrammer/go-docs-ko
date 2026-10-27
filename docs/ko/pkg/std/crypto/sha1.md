# package crypto/sha1

- 원문: <https://pkg.go.dev/crypto/sha1>
- 분류: Go 표준 라이브러리

## 한국어 요약

`sha1` 패키지는 RFC 3174에 정의된 SHA-1 해시 알고리즘을 구현합니다.

## 원문 요약

Package sha1 implements the SHA-1 hash algorithm as defined in RFC 3174.

## API 상세 (go doc -all)

~~~text
package sha1 // import "crypto/sha1"

Package sha1 implements the SHA-1 hash algorithm as defined in RFC 3174.

SHA-1 is cryptographically broken and should not be used for secure
applications.

CONSTANTS

const BlockSize = 64
    The blocksize of SHA-1 in bytes.

const Size = 20
    The size of a SHA-1 checksum in bytes.


FUNCTIONS

func New() hash.Hash
    New returns a new hash.Hash computing the SHA1 checksum. The Hash
    also implements encoding.BinaryMarshaler, encoding.BinaryAppender and
    encoding.BinaryUnmarshaler to marshal and unmarshal the internal state of
    the hash.

func Sum(data []byte) [Size]byte
    Sum returns the SHA-1 checksum of the data.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
