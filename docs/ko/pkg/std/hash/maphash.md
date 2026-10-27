# package hash/maphash

- 원문: <https://pkg.go.dev/hash/maphash>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `maphash`는 바이트 시퀀스와 비교 가능한 값에 대한 해시 함수를 제공합니다.

## 원문 요약

Package maphash provides hash functions on byte sequences and comparable values.

## API 상세 (go doc -all)

~~~text
package maphash // import "hash/maphash"

Package maphash provides hash functions on byte sequences and comparable values.
It also defines Hasher, the interface between a hash function and a hash table.

These hash functions are intended to be used to implement hash tables, Bloom
filters, and other data structures that need to map arbitrary strings or byte
sequences to a uniform distribution on unsigned 64-bit integers.

Each different instance of a hash table or data structure should use its own
Seed.

The hash functions are not cryptographically secure. (See crypto/sha256 and
crypto/sha512 for cryptographic use.)

FUNCTIONS

func Bytes(seed Seed, b []byte) uint64
    Bytes returns the hash of b with the given seed.

    Bytes is equivalent to, but more convenient and efficient than:

        var h Hash
        h.SetSeed(seed)
        h.Write(b)
        return h.Sum64()

func Comparable[T comparable](seed Seed, v T) uint64
    Comparable returns the hash of comparable value v with the given seed
    such that Comparable(s, v1) == Comparable(s, v2) if v1 == v2. If v != v,
    then the resulting hash is randomly distributed.

func String(seed Seed, s string) uint64
    String returns the hash of s with the given seed.

    String is equivalent to, but more convenient and efficient than:

        var h Hash
        h.SetSeed(seed)
        h.WriteString(s)
        return h.Sum64()

func WriteComparable[T comparable](h *Hash, x T)
    WriteComparable adds x to the data hashed by h.


TYPES

type ComparableHasher[T comparable] struct {
	// Has unexported fields.
}
    ComparableHasher is an implementation of Hasher whose Equal(x, y) method is
    consistent with x == y.

    ComparableHasher is defined only for comparable types. The type system will
    not prevent you from instantiating a type such as ComparableHasher[any];
    nonetheless you must not pass non-comparable argument values to its Hash or
    Equal methods.

func (ComparableHasher[T]) Equal(x, y T) bool

func (ComparableHasher[T]) Hash(h *Hash, v T)

type Hash struct {
	// Has unexported fields.
}
    A Hash computes a seeded hash of a byte sequence.

    The zero Hash is a valid Hash ready to use. A zero Hash chooses a random
    seed for itself during the first call to a Reset, Write, Seed, Clone,
    or Sum64 method. For control over the seed, use SetSeed.

    The computed hash values depend only on the initial seed and the sequence
    of bytes provided to the Hash object, not on the way in which the bytes are
    provided. For example, the three sequences

        h.Write([]byte{'f','o','o'})
        h.WriteByte('f'); h.WriteByte('o'); h.WriteByte('o')
        h.WriteString("foo")

    all have the same effect.

    Hashes are intended to be collision-resistant, even for situations where an
    adversary controls the byte sequences being hashed.

    A Hash is not safe for concurrent use by multiple goroutines, but a Seed is.
    If multiple goroutines must compute the same seeded hash, each can declare
    its own Hash and call SetSeed with a common Seed.

func (h *Hash) BlockSize() int
    BlockSize returns h's block size.

func (h *Hash) Clone() (hash.Cloner, error)
    Clone implements hash.Cloner.

func (h *Hash) Reset()
    Reset discards all bytes added to h. (The seed remains the same.)

func (h *Hash) Seed() Seed
    Seed returns h's seed value.

func (h *Hash) SetSeed(seed Seed)
    SetSeed sets h to use seed, which must have been returned by MakeSeed or
    by another Hash.Seed method. Two Hash objects with the same seed behave
    identically. Two Hash objects with different seeds will very likely behave
    differently. Any bytes added to h before this call will be discarded.

func (h *Hash) Size() int
    Size returns h's hash value size, 8 bytes.

func (h *Hash) Sum(b []byte) []byte
    Sum appends the hash's current 64-bit value to b. It exists for implementing
    hash.Hash. For direct calls, it is more efficient to use Hash.Sum64.

func (h *Hash) Sum64() uint64
    Sum64 returns h's current 64-bit value, which depends on h's seed and
    the sequence of bytes added to h since the last call to Hash.Reset or
    Hash.SetSeed.

    All bits of the Sum64 result are close to uniformly and independently
    distributed, so it can be safely reduced by using bit masking, shifting,
    or modular arithmetic.

func (h *Hash) Write(b []byte) (int, error)
    Write adds b to the sequence of bytes hashed by h. It always writes all of b
    and never fails; the count and error result are for implementing io.Writer.

func (h *Hash) WriteByte(b byte) error
    WriteByte adds b to the sequence of bytes hashed by h. It never fails;
    the error result is for implementing io.ByteWriter.

func (h *Hash) WriteString(s string) (int, error)
    WriteString adds the bytes of s to the sequence of bytes hashed by h.
    It always writes all of s and never fails; the count and error result are
    for implementing io.StringWriter.

type Hasher[T any] interface {
	Hash(*Hash, T)
	Equal(x, y T) bool
}
    A Hasher defines the interface between a hash-based container and its
    elements. It provides a hash function and an equivalence relation over
    values of type T, enabling those values to be inserted in hash tables and
    similar data structures.

    Of course, comparable types can already be used as keys of Go's built-in
    map type, but a Hasher enables non-comparable types to be used as keys of a
    suitable hash table too. Hashers may be useful even for comparable types,
    to define an equivalence relation that differs from the usual one (==),
    such as a field-based comparison for a pointer-to-struct type, or a
    case-insensitive comparison for strings, as in this example:

        // CaseInsensitive is a Hasher[string] whose
        // equivalence relation ignores letter case.
        type CaseInsensitive struct{}

        func (CaseInsensitive) Hash(h *Hash, s string) {
        	h.WriteString(strings.ToLower(s))
        }

        func (CaseInsensitive) Equal(x, y string) bool {
        	// (We avoid strings.EqualFold as it is not
        	// consistent with ToLower for all values.)
        	return strings.ToLower(x) == strings.ToLower(y)
        }

    A Hasher also permits values to be used with other hash-based data
    structures such as a Bloom filter. The ComparableHasher type makes it
    convenient to enable comparable types to be used in such data structures
    under their usual (==) equivalence relation.

    # Hash invariants

    If two values are equal as defined by Equal(x, y), then they must have the
    same hash as defined by the effects of Hash(h, x) on h.

    Hashers must be logically stateless: the behavior of the Hash and Equal
    methods depends only on the arguments.

    # Writing a good function

    When defining a hash function and equivalence relation for a data type,
    it may help to first define a canonical encoding for values of that type as
    a sequence of elements, each being a number, string, boolean, or pointer.
    An encoding is canonical if two values that are logically equal have the
    same encoding, even if they are represented differently. For example,
    a canonical case-insensitive encoding of a string is strings.ToLower.

    Once you have defined the encoding, the Hasher's Hash method should encode a
    value into the Hash using a sequence of calls to Hash.Write for byte slices,
    Hash.WriteString for strings, Hash.WriteByte for bytes, and WriteComparable
    for elements of other types. The Hasher's Equal method should compute
    the encodings of two values, then compare their corresponding elements,
    returning false at the first mismatch.

    A Hash method may discard information so long as it remains consistent with
    the Equal method as defined above. For example, valid implementations of
    CaseInsensitive.Hash might inspect only the first letter of the string,
    or even use a constant value. However, the lossier the hash function,
    the more frequent the hash collisions and the slower the hash table.

    Some data types, such as sets, are inherently unordered: the set {a, b,
    c} is equal to the set {c, b, a}. In some cases it is possible to define
    a canonical encoding for a set by sorting the elements into some order.
    In other cases this may inefficient, since it may require allocating memory,
    or infeasible, as when there is no convenient order. Another way to hash
    an unordered set is to compute the hash for each element separately,
    then combine all the element hashes using a commutative (order-independent)
    operator such as + or ^.

    The Hash method below, for a hypothetical Set type, illustrates this
    approach:

        type Set[T comparable] struct{ ... }

        type setHasher[T comparable] struct{}

        func (setHasher[T]) Hash(hash *maphash.Hash, set *Set[T]) {
        	var accum uint64
        	for elem := range set.Elements() {
        		// Initialize a hasher for the element,
        		// using same seed as the outer hash.
        		var sub maphash.Hash
        		sub.SetSeed(hash.Seed())

        		// Hash the element.
        		maphash.WriteComparable(&sub, elem)

        		// Mix the element's hash into the set's hash.
        		accum ^= sub.Sum64()
        	}
        	maphash.WriteComparable(hash, accum)
        }

    In many languages, a data type's hash operation simply returns an integer
    value. However, that makes it possible for an adversary to systematically
    construct a large number of values that all have the same hash, degrading
    the asymptotic performance of hash tables in a denial-of-service attack
    known as "hash flooding". By contrast, computing hashes as a sequence of
    values emitted into a Hash with an unpredictable Seed that varies from one
    hash table to another mitigates this attack.

    In effect, the Seed chooses one of 2⁶⁴ different hash functions. The code
    example above calls SetSeed on the element's sub-Hasher so that it uses the
    same hash function as for the Set itself, and not a random one.

type Seed struct {
	// Has unexported fields.
}
    A Seed is a random value that selects the specific hash function computed
    by a Hash. If two Hashes use the same Seeds, they will compute the same hash
    values for any given input. If two Hashes use different Seeds, they are very
    likely to compute distinct hash values for any given input.

    A Seed must be initialized by calling MakeSeed. The zero seed is
    uninitialized and not valid for use with Hash's SetSeed method.

    Each Seed value is local to a single process and cannot be serialized or
    otherwise recreated in a different process.

func MakeSeed() Seed
    MakeSeed returns a new random seed.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
