# package crypto/md5

- 원문: <https://pkg.go.dev/crypto/md5>
- 분류: Go 표준 라이브러리

## 한국어 요약

`md5` 패키지는 RFC 1321에 정의된 MD5 해시 알고리즘을 구현합니다.

## 원문 요약

Package md5 implements the MD5 hash algorithm as defined in RFC 1321.

## API 상세 (go doc -all)

~~~text
package md5 // import "crypto/md5"

Package md5 implements the MD5 hash algorithm as defined in RFC 1321.

MD5 is cryptographically broken and should not be used for secure applications.

CONSTANTS

const BlockSize = 64
    The blocksize of MD5 in bytes.

const Size = 16
    The size of an MD5 checksum in bytes.


FUNCTIONS

func New() hash.Hash
    New returns a new hash.Hash computing the MD5 checksum. The Hash
    also implements encoding.BinaryMarshaler, encoding.BinaryAppender and
    encoding.BinaryUnmarshaler to marshal and unmarshal the internal state of
    the hash.

func Sum(data []byte) [Size]byte
    Sum returns the MD5 checksum of the data.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
