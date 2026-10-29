# package crypto/des

- 원문: <https://pkg.go.dev/crypto/des>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package des implements the Data Encryption Standard (DES) and the Triple Data Encryption Algorithm (TDEA) as defined in U.S. Federal Information Processing Standards Publication 46-3.

## 원문 요약

Package des implements the Data Encryption Standard (DES) and the Triple Data Encryption Algorithm (TDEA) as defined in U.S. Federal Information Processing Standards Publication 46-3.

## API 상세 (go doc -all)

~~~text
package des // import "crypto/des"

Package des implements the Data Encryption Standard (DES) and the Triple Data
Encryption Algorithm (TDEA) as defined in U.S. Federal Information Processing
Standards Publication 46-3.

DES is cryptographically broken and should not be used for secure applications.

CONSTANTS

const BlockSize = 8
    The DES block size in bytes.


FUNCTIONS

func NewCipher(key []byte) (cipher.Block, error)
    NewCipher creates and returns a new cipher.Block.

func NewTripleDESCipher(key []byte) (cipher.Block, error)
    NewTripleDESCipher creates and returns a new cipher.Block.


TYPES

type KeySizeError int

func (k KeySizeError) Error() string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
