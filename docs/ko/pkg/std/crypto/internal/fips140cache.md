# package crypto/internal/fips140cache

- 원문: <https://pkg.go.dev/crypto/internal/fips140cache>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `fips140cache`는 값을 키와 연결하는 약한 맵을 제공합니다. 이 맵은 값의 수명을 키의 수명과 연결합니다.

## 원문 요약

Package fips140cache provides a weak map that associates the lifetime of values with the lifetime of keys.

## API 상세 (go doc -all)

~~~text
package fips140cache // import "crypto/internal/fips140cache"

Package fips140cache provides a weak map that associates the lifetime of values
with the lifetime of keys.

It can be used to associate a precomputed value (such as an internal/fips140
PrivateKey value, which in FIPS 140-3 mode may have required an expensive
pairwise consistency test) with a type that doesn't have private fields (such
as an ed25519.PrivateKey), or that can't be safely modified because it may be
concurrently copied (such as an ecdsa.PrivateKey).

TYPES

type Cache[K, V any] struct {
	// Has unexported fields.
}

func (c *Cache[K, V]) Get(k *K, new func() (*V, error), check func(*V) bool) (*V, error)
    Get returns the result of new, for an associated key k.

    If Get was called with k before and didn't return an error, Get may return
    the same value it returned from the previous call if check returns true on
    it. If check returns false, Get will call new again and return the result.

    The cache is evicted some time after k becomes unreachable.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
