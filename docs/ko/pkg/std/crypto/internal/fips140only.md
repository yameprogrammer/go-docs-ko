# package crypto/internal/fips140only

- 원문: <https://pkg.go.dev/crypto/internal/fips140only>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package fips140only // import "crypto/internal/fips140only"


FUNCTIONS

func ApprovedHash(h hash.Hash) bool
func ApprovedRandomReader(r io.Reader) bool
func Enforced() bool
    Enforced reports whether FIPS 140-only mode is enabled and enforced,
    in which non-approved cryptography returns an error or panics.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
