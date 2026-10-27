# package internal/unsafeheader

- 원문: <https://pkg.go.dev/internal/unsafeheader>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package unsafeheader contains header declarations for the Go runtime's slice and string implementations.

## 원문 요약

Package unsafeheader contains header declarations for the Go runtime's slice and string implementations.

## API 상세 (go doc -all)

~~~text
package unsafeheader // import "internal/unsafeheader"

Package unsafeheader contains header declarations for the Go runtime's slice and
string implementations.

This package allows packages that cannot import "reflect" to use types that are
tested to be equivalent to reflect.SliceHeader and reflect.StringHeader.

TYPES

type Slice struct {
	Data unsafe.Pointer
	Len  int
	Cap  int
}
    Slice is the runtime representation of a slice. It cannot be used safely or
    portably and its representation may change in a later release.

    Unlike reflect.SliceHeader, its Data field is sufficient to guarantee the
    data it references will not be garbage collected.

type String struct {
	Data unsafe.Pointer
	Len  int
}
    String is the runtime representation of a string. It cannot be used safely
    or portably and its representation may change in a later release.

    Unlike reflect.StringHeader, its Data field is sufficient to guarantee the
    data it references will not be garbage collected.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
