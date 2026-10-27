# package crypto/aes

- 원문: <https://pkg.go.dev/crypto/aes>
- 분류: Go 표준 라이브러리

## 한국어 요약

`aes` 패키지는 미국 연방 정보 처리 표준(U.S. Federal Information Processing Standards) 출판물 197에 정의된 AES 암호화(이전의 Rijndael)를 구현합니다.

## 원문 요약

Package aes implements AES encryption (formerly Rijndael), as defined in U.S. Federal Information Processing Standards Publication 197.

## API 상세 (go doc -all)

~~~text
package aes // import "crypto/aes"

Package aes implements AES encryption (formerly Rijndael), as defined in U.S.
Federal Information Processing Standards Publication 197.

The AES operations in this package are not implemented using constant-time
algorithms. An exception is when running on systems with enabled hardware
support for AES that makes these operations constant-time. Examples
include amd64 systems using AES-NI extensions and s390x systems using
Message-Security-Assist extensions. On such systems, when the result of
NewCipher is passed to cipher.NewGCM, the GHASH operation used by GCM is also
constant-time.

CONSTANTS

const BlockSize = 16
    The AES block size in bytes.


FUNCTIONS

func NewCipher(key []byte) (cipher.Block, error)
    NewCipher creates and returns a new cipher.Block. The key argument must
    be the AES key, either 16, 24, or 32 bytes to select AES-128, AES-192,
    or AES-256.


TYPES

type KeySizeError int

func (k KeySizeError) Error() string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
