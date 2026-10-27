# package crypto/internal/fips140/hmac

- 원문: <https://pkg.go.dev/crypto/internal/fips140/hmac>
- 분류: Go 표준 라이브러리

## 한국어 요약

package hmac은 [FIPS 198-1]에 따른 HMAC을 구현합니다.

## 원문 요약

Package hmac implements HMAC according to [FIPS 198-1].

## API 상세 (go doc -all)

~~~text
package hmac // import "crypto/internal/fips140/hmac"

Package hmac implements HMAC according to FIPS 198-1.

[FIPS 198-1]: https://doi.org/10.6028/NIST.FIPS.198-1

FUNCTIONS

func MarkAsUsedInKDF(h *HMAC)
    MarkAsUsedInKDF records that this HMAC instance is used as part of a KDF.


TYPES

type HMAC struct {
	// Has unexported fields.
}

func New[H hash.Hash](h func() H, key []byte) *HMAC
    New returns a new HMAC hash using the given hash.Hash type and key.

func (h *HMAC) BlockSize() int

func (h *HMAC) Clone() (hash.Cloner, error)
    Clone implements hash.Cloner if the underlying hash does. Otherwise,
    it returns an error wrapping errors.ErrUnsupported.

func (h *HMAC) Reset()

func (h *HMAC) Size() int

func (h *HMAC) Sum(in []byte) []byte

func (h *HMAC) Write(p []byte) (n int, err error)
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
