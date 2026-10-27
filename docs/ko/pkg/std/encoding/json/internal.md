# package encoding/json/internal

- 원문: <https://pkg.go.dev/encoding/json/internal>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package internal // import "encoding/json/internal"


VARIABLES

var (
	ErrCycle           = errors.New("encountered a cycle")
	ErrNonNilReference = errors.New("value must be passed as a non-nil pointer reference")
	ErrNilInterface    = errors.New("cannot derive concrete type for nil interface with finite type set")
)
    Sentinel error values internally shared between jsonv1 and jsonv2.

var (
	// TransformMarshalError converts a v2 error into a v1 error.
	// It is called only at the top-level of a Marshal function.
	TransformMarshalError func(any, error) error
	// NewMarshalerError constructs a jsonv1.MarshalerError.
	// It is called after a user-defined Marshal method/function fails.
	NewMarshalerError func(any, error, string) error
	// TransformUnmarshalError converts a v2 error into a v1 error.
	// It is called only at the top-level of an Unmarshal function.
	TransformUnmarshalError func(any, error) error

	// NewRawNumber returns new(jsonv1.Number).
	NewRawNumber func() any
	// RawNumberOf returns jsonv1.Number(b).
	RawNumberOf func(b []byte) any
)

TYPES

type NotForPublicUse struct{}
    NotForPublicUse is a marker type that an API is for internal use only. It
    does not perfectly prevent usage of that API, but helps to restrict usage.
    Anything with this marker is not covered by the Go compatibility agreement.

var AllowInternalUse NotForPublicUse
    AllowInternalUse is passed from "json" to "jsontext" to authenticate that
    the caller can have access to internal functionality.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
