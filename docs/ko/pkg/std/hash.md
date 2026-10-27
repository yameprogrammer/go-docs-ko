# package hash

- 원문: <https://pkg.go.dev/hash>
- 분류: Go 표준 라이브러리

## 한국어 요약

`hash` 패키지는 해시 함수를 위한 인터페이스를 제공합니다.

## 원문 요약

Package hash provides interfaces for hash functions.

## API 상세 (go doc -all)

~~~text
package hash // import "hash"

Package hash provides interfaces for hash functions.

TYPES

type Cloner interface {
	Hash
	Clone() (Cloner, error)
}
    A Cloner is a hash function whose state can be cloned, returning a value
    with equivalent and independent state.

    All Hash implementations in the standard library implement this interface,
    unless GOFIPS140=v1.0.0 is set.

    If a hash can only determine at runtime if it can be cloned (e.g.
    if it wraps another hash), Clone may return an error wrapping
    errors.ErrUnsupported. Otherwise, Clone must always return a nil error.

type Hash interface {
	// Write (via the embedded io.Writer interface) adds more data to the running hash.
	// It never returns an error.
	io.Writer

	// Sum appends the current hash to b and returns the resulting slice.
	// It does not change the underlying hash state.
	Sum(b []byte) []byte

	// Reset resets the Hash to its initial state.
	Reset()

	// Size returns the number of bytes Sum will return.
	Size() int

	// BlockSize returns the hash's underlying block size.
	// The Write method must be able to accept any amount
	// of data, but it may operate more efficiently if all writes
	// are a multiple of the block size.
	BlockSize() int
}
    Hash is the common interface implemented by all hash functions.

    Hash implementations in the standard library (e.g. hash/crc32
    and crypto/sha256) implement the encoding.BinaryMarshaler,
    encoding.BinaryAppender, encoding.BinaryUnmarshaler and Cloner interfaces.
    Marshaling a hash implementation allows its internal state to be saved and
    used for additional processing later, without having to re-write the data
    previously written to the hash. The hash state may contain portions of the
    input in its original form, which users are expected to handle for any
    possible security implications.

    Compatibility: Any future changes to hash or crypto packages will endeavor
    to maintain compatibility with state encoded using previous versions.
    That is, any released versions of the packages should be able to decode
    data written with any previously released version, subject to issues such
    as security fixes. See the Go compatibility document for background:
    https://golang.org/doc/go1compat

type Hash32 interface {
	Hash
	Sum32() uint32
}
    Hash32 is the common interface implemented by all 32-bit hash functions.

type Hash64 interface {
	Hash
	Sum64() uint64
}
    Hash64 is the common interface implemented by all 64-bit hash functions.

type XOF interface {
	// Write absorbs more data into the XOF's state. It panics if called
	// after Read.
	io.Writer

	// Read reads more output from the XOF. It may return io.EOF if there
	// is a limit to the XOF output length.
	io.Reader

	// Reset resets the XOF to its initial state.
	Reset()

	// BlockSize returns the XOF's underlying block size.
	// The Write method must be able to accept any amount
	// of data, but it may operate more efficiently if all writes
	// are a multiple of the block size.
	BlockSize() int
}
    XOF (extendable output function) is a hash function with arbitrary or
    unlimited output length.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
