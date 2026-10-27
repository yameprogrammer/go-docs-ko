# package internal/sync

- 원문: <https://pkg.go.dev/internal/sync>
- 분류: Go 표준 라이브러리

## 한국어 요약

`sync` 패키지는 상호 배제 락(mutual exclusion locks)과 같은 기본적인 동기화 기본 제공 객체들을 내부 패키지(`sync`에 의존하는 패키지 포함)에 제공합니다.

## 원문 요약

Package sync provides basic synchronization primitives such as mutual exclusion locks to internal packages (including ones that depend on sync).

## API 상세 (go doc -all)

~~~text
package sync // import "internal/sync"

Package sync provides basic synchronization primitives such as mutual exclusion
locks to internal packages (including ones that depend on sync).

Tests are defined in package sync.

TYPES

type HashTrieMap[K comparable, V any] struct {
	// Has unexported fields.
}
    HashTrieMap is an implementation of a concurrent hash-trie.
    The implementation is designed around frequent loads, but offers decent
    performance for stores and deletes as well, especially if the map is larger.
    Its primary use-case is the unique package, but can be used elsewhere as
    well.

    The zero HashTrieMap is empty and ready to use. It must not be copied after
    first use.

func (ht *HashTrieMap[K, V]) All() func(yield func(K, V) bool)
    All returns an iterator over each key and value present in the map.

    The iterator does not necessarily correspond to any consistent snapshot
    of the HashTrieMap's contents: no key will be visited more than once,
    but if the value for any key is stored or deleted concurrently (including
    by yield), the iterator may reflect any mapping for that key from any point
    during iteration. The iterator does not block other methods on the receiver;
    even yield itself may call any method on the HashTrieMap.

func (ht *HashTrieMap[K, V]) Clear()
    Clear deletes all the entries, resulting in an empty HashTrieMap.

func (ht *HashTrieMap[K, V]) CompareAndDelete(key K, old V) (deleted bool)
    CompareAndDelete deletes the entry for key if its value is equal to old. The
    value type must be comparable, otherwise this CompareAndDelete will panic.

    If there is no current value for key in the map, CompareAndDelete returns
    false (even if the old value is the nil interface value).

func (ht *HashTrieMap[K, V]) CompareAndSwap(key K, old, new V) (swapped bool)
    CompareAndSwap swaps the old and new values for key if the value stored
    in the map is equal to old. The value type must be of a comparable type,
    otherwise CompareAndSwap will panic.

func (ht *HashTrieMap[K, V]) Delete(key K)
    Delete deletes the value for a key.

func (ht *HashTrieMap[K, V]) Load(key K) (value V, ok bool)
    Load returns the value stored in the map for a key, or nil if no value is
    present. The ok result indicates whether value was found in the map.

func (ht *HashTrieMap[K, V]) LoadAndDelete(key K) (value V, loaded bool)
    LoadAndDelete deletes the value for a key, returning the previous value if
    any. The loaded result reports whether the key was present.

func (ht *HashTrieMap[K, V]) LoadOrStore(key K, value V) (result V, loaded bool)
    LoadOrStore returns the existing value for the key if present. Otherwise,
    it stores and returns the given value. The loaded result is true if the
    value was loaded, false if stored.

func (ht *HashTrieMap[K, V]) Range(yield func(K, V) bool)
    Range calls f sequentially for each key and value present in the map.
    If f returns false, range stops the iteration.

    This exists for compatibility with sync.Map; All should be preferred.
    It provides the same guarantees as sync.Map, and All.

func (ht *HashTrieMap[K, V]) Store(key K, new V)
    Store sets the value for a key.

func (ht *HashTrieMap[K, V]) Swap(key K, new V) (previous V, loaded bool)
    Swap swaps the value for a key and returns the previous value if any.
    The loaded result reports whether the key was present.

type Mutex struct {
	// Has unexported fields.
}
    A Mutex is a mutual exclusion lock.

    See package sync.Mutex documentation.

func (m *Mutex) Lock()
    Lock locks m.

    See package sync.Mutex documentation.

func (m *Mutex) TryLock() bool
    TryLock tries to lock m and reports whether it succeeded.

    See package sync.Mutex documentation.

func (m *Mutex) Unlock()
    Unlock unlocks m.

    See package sync.Mutex documentation.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
