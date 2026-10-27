# package crypto/internal/fips140hash

- 원문: <https://pkg.go.dev/crypto/internal/fips140hash>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package fips140hash // import "crypto/internal/fips140hash"


FUNCTIONS

func Unwrap(h hash.Hash) hash.Hash
    Unwrap returns h, or a crypto/internal/fips140 inner implementation of h.

    The return value can be type asserted to one
    of crypto/internal/fips140/sha256.Digest,
    crypto/internal/fips140/sha512.Digest, or
    crypto/internal/fips140/sha3.Digest if it is a FIPS 140-3 approved hash.

func UnwrapNew[Hash hash.Hash](newHash func() Hash) func() hash.Hash
    UnwrapNew returns a function that calls newHash and applies Unwrap to the
    return value.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
