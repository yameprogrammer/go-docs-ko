# package testing/cryptotest

- 원문: <https://pkg.go.dev/testing/cryptotest>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 cryptotest은 결정론적 무작위 소스 테스트를 제공합니다.

## 원문 요약

Package cryptotest provides deterministic random source testing.

## API 상세 (go doc -all)

~~~text
package cryptotest // import "testing/cryptotest"

Package cryptotest provides deterministic random source testing.

FUNCTIONS

func SetGlobalRandom(t *testing.T, seed uint64)
    SetGlobalRandom sets a global, deterministic cryptographic randomness source
    for the duration of test t. It affects crypto/rand, and all implicit sources
    of cryptographic randomness in the crypto/... packages.

    SetGlobalRandom may be called multiple times in the same test to reset the
    random stream or change the seed.

    Because SetGlobalRandom affects the whole process, it cannot be used in
    parallel tests or tests with parallel ancestors.

    Note that the way cryptographic algorithms use randomness is generally
    not specified and may change over time. Thus, if a test expects a specific
    output from a cryptographic function, it may fail in the future even if it
    uses SetGlobalRandom.

    SetGlobalRandom is not supported when building against the Go Cryptographic
    Module v1.0.0 (i.e. when crypto/fips140.Version returns "v1.0.0").
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
