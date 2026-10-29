# package internal/saferio

- 원문: <https://pkg.go.dev/internal/saferio>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package saferio provides I/O functions that avoid allocating large amounts of memory unnecessarily.

## 원문 요약

Package saferio provides I/O functions that avoid allocating large amounts of memory unnecessarily.

## API 상세 (go doc -all)

~~~text
package saferio // import "internal/saferio"

Package saferio provides I/O functions that avoid allocating large amounts
of memory unnecessarily. This is intended for packages that read data from an
io.Reader where the size is part of the input data but the input may be corrupt,
or may be provided by an untrustworthy attacker.

FUNCTIONS

func ReadData(r io.Reader, n uint64) ([]byte, error)
    ReadData reads n bytes from the input stream, but avoids allocating all n
    bytes if n is large. This avoids crashing the program by allocating all n
    bytes in cases where n is incorrect.

    The error is io.EOF only if no bytes were read. If an io.EOF happens after
    reading some but not all the bytes, ReadData returns io.ErrUnexpectedEOF.

func ReadDataAt(r io.ReaderAt, n uint64, off int64) ([]byte, error)
    ReadDataAt reads n bytes from the input stream at off, but avoids allocating
    all n bytes if n is large. This avoids crashing the program by allocating
    all n bytes in cases where n is incorrect.

func SliceCap[E any](c uint64) int
    SliceCap is like SliceCapWithSize but using generics.

func SliceCapWithSize(size, c uint64) int
    SliceCapWithSize returns the capacity to use when allocating a slice. After
    the slice is allocated with the capacity, it should be built using append.
    This will avoid allocating too much memory if the capacity is large and
    incorrect.

    A negative result means that the value is always too big.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
