# package crypto/hmac

- 원문: <https://pkg.go.dev/crypto/hmac>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `hmac`은 U.S. 연방 정보 처리 표준 Publication 198에서 정의된 키드 해시 메시지 인증 코드 (HMAC)를 구현합니다.

## 원문 요약

Package hmac implements the Keyed-Hash Message Authentication Code (HMAC) as defined in U.S. Federal Information Processing Standards Publication 198.

## API 상세 (go doc -all)

~~~text
package hmac // import "crypto/hmac"

Package hmac implements the Keyed-Hash Message Authentication Code (HMAC) as
defined in U.S. Federal Information Processing Standards Publication 198.
An HMAC is a cryptographic hash that uses a key to sign a message. The receiver
verifies the hash by recomputing it using the same key.

Receivers should be careful to use Equal to compare MACs in order to avoid
timing side-channels:

    // ValidMAC reports whether messageMAC is a valid HMAC tag for message.
    func ValidMAC(message, messageMAC, key []byte) bool {
    	mac := hmac.New(sha256.New, key)
    	mac.Write(message)
    	expectedMAC := mac.Sum(nil)
    	return hmac.Equal(messageMAC, expectedMAC)
    }

FUNCTIONS

func Equal(mac1, mac2 []byte) bool
    Equal compares two MACs for equality without leaking timing information.

func New(h func() hash.Hash, key []byte) hash.Hash
    New returns a new HMAC hash using the given hash.Hash type and key.
    New functions like crypto/sha256.New can be used as h. h must return a new
    Hash every time it is called. Note that unlike other hash implementations
    in the standard library, the returned Hash does not implement
    encoding.BinaryMarshaler or encoding.BinaryUnmarshaler.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
