# package crypto/internal/fips140/hkdf

- 원문: <https://pkg.go.dev/crypto/internal/fips140/hkdf>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package hkdf // import "crypto/internal/fips140/hkdf"


FUNCTIONS

func Expand[H hash.Hash](h func() H, pseudorandomKey []byte, info string, keyLen int) []byte
func Extract[H hash.Hash](h func() H, secret, salt []byte) []byte
func Key[H hash.Hash](h func() H, secret, salt []byte, info string, keyLen int) []byte
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
