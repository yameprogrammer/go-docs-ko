# package unique

- 원문: <https://pkg.go.dev/unique>
- 분류: Go 표준 라이브러리

## 한국어 요약

이 고유 패키지는 비교 가능한 값을 "표준화"(내장)하는 기능을 제공합니다.

## 원문 요약

The unique package provides facilities for canonicalizing ("interning") comparable values.

## API 상세 (go doc -all)

~~~text
package unique // import "unique"

The unique package provides facilities for canonicalizing ("interning")
comparable values.

TYPES

type Handle[T comparable] struct {
	// Has unexported fields.
}
    Handle is a globally unique identity for some value of type T.

    Two handles compare equal exactly if the two values used to create the
    handles would have also compared equal. The comparison of two handles is
    trivial and typically much more efficient than comparing the values used to
    create them.

func Make[T comparable](value T) Handle[T]
    Make returns a globally unique handle for a value of type T. Handles are
    equal if and only if the values used to produce them are equal. Make is safe
    for concurrent use by multiple goroutines.

func (h Handle[T]) Value() T
    Value returns a shallow copy of the T value that produced the Handle.
    Value is safe for concurrent use by multiple goroutines.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
