# package crypto/internal/boring/bcache

- 원문: <https://pkg.go.dev/crypto/internal/boring/bcache>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package bcache implements a GC-friendly cache (see [Cache]) for BoringCrypto.

## 원문 요약

Package bcache implements a GC-friendly cache (see [Cache]) for BoringCrypto.

## API 상세 (go doc -all)

~~~text
package bcache // import "crypto/internal/boring/bcache"

Package bcache implements a GC-friendly cache (see Cache) for BoringCrypto.

TYPES

type Cache[K, V any] struct {
	// Has unexported fields.
}
    A Cache is a GC-friendly concurrent map from unsafe.Pointer to
    unsafe.Pointer. It is meant to be used for maintaining shadow BoringCrypto
    state associated with certain allocated structs, in particular public and
    private RSA and ECDSA keys.

    The cache is GC-friendly in the sense that the keys do not indefinitely
    prevent the garbage collector from collecting them. Instead, at the start
    of each GC, the cache is cleared entirely. That is, the cache is lossy,
    and the loss happens at the start of each GC. This means that clients need
    to be able to cope with cache entries disappearing, but it also means that
    clients don't need to worry about cache entries keeping the keys from being
    collected.

func (c *Cache[K, V]) Clear()
    Clear clears the cache. The runtime does this automatically at each garbage
    collection; this method is exposed only for testing.

func (c *Cache[K, V]) Get(k *K) *V
    Get returns the cached value associated with v, which is either the value
    v corresponding to the most recent call to Put(k, v) or nil if that cache
    entry has been dropped.

func (c *Cache[K, V]) Put(k *K, v *V)
    Put sets the cached value associated with k to v.

func (c *Cache[K, V]) Register()
    Register registers the cache with the runtime, so that c.ptable can be
    cleared at the start of each GC. Register must be called during package
    initialization.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
