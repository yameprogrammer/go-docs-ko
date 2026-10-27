# package crypto/internal/randutil

- 원문: <https://pkg.go.dev/crypto/internal/randutil>
- 분류: Go 표준 라이브러리

## 한국어 요약

`randutil` 패키지는 다양한 crypto 패키지를 위한 내부 무작위성 유틸리티를 포함하고 있습니다.

## 원문 요약

Package randutil contains internal randomness utilities for various crypto packages.

## API 상세 (go doc -all)

~~~text
package randutil // import "crypto/internal/randutil"

Package randutil contains internal randomness utilities for various crypto
packages.

FUNCTIONS

func MaybeReadByte(r io.Reader)
    MaybeReadByte reads a single byte from r with 50% probability. This is
    used to ensure that callers do not depend on non-guaranteed behaviour, e.g.
    assuming that rsa.GenerateKey is deterministic w.r.t. a given random stream.

    This does not affect tests that pass a stream of fixed bytes as the random
    source (e.g. a zeroReader).
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
