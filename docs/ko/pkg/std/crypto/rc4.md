# package crypto/rc4

- 원문: <https://pkg.go.dev/crypto/rc4>
- 분류: Go 표준 라이브러리

## 한국어 요약

`rc4` 패키지는 Bruce Schneier의 Applied Cryptography에 정의된 RC4 암호화를 구현합니다.

## 원문 요약

Package rc4 implements RC4 encryption, as defined in Bruce Schneier's Applied Cryptography.

## API 상세 (go doc -all)

~~~text
package rc4 // import "crypto/rc4"

Package rc4 implements RC4 encryption, as defined in Bruce Schneier's Applied
Cryptography.

RC4 is cryptographically broken and should not be used for secure applications.

TYPES

type Cipher struct {
	// Has unexported fields.
}
    A Cipher is an instance of RC4 using a particular key.

func NewCipher(key []byte) (*Cipher, error)
    NewCipher creates and returns a new Cipher. The key argument should be the
    RC4 key, at least 1 byte and at most 256 bytes.

func (c *Cipher) Reset()
    Reset zeros the key data and makes the Cipher unusable.

    Deprecated: Reset can't guarantee that the key will be entirely removed from
    the process's memory.

func (c *Cipher) XORKeyStream(dst, src []byte)
    XORKeyStream sets dst to the result of XORing src with the key stream.
    Dst and src must overlap entirely or not at all.

type KeySizeError int

func (k KeySizeError) Error() string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
