# package internal/reflectlite

- 원문: <https://pkg.go.dev/internal/reflectlite>
- 분류: Go 표준 라이브러리

## 한국어 요약

`reflectlite` 패키지는 `runtime`, `unsafe`, 그리고 `internal/abi` 외의 다른 패키지를 사용하지 않는 `reflect` 패키지의 경량화 버전을 구현합니다.

## 원문 요약

Package reflectlite implements lightweight version of reflect, not using any package except for "runtime", "unsafe", and "internal/abi"

## API 상세 (go doc -all)

~~~text
package reflectlite // import "internal/reflectlite"

Package reflectlite implements lightweight version of reflect, not using any
package except for "runtime", "unsafe", and "internal/abi"

CONSTANTS

const (
	// Import-and-export these constants as necessary
	Interface = abi.Interface
	Slice     = abi.Slice
	String    = abi.String
	Struct    = abi.Struct
)
const Ptr = abi.Pointer

FUNCTIONS

func Swapper(slice any) func(i, j int)
    Swapper returns a function that swaps the elements in the provided slice.

    Swapper panics if the provided interface is not a slice.


TYPES

type Kind = abi.Kind
    A Kind represents the specific kind of type that a Type represents. The zero
    Kind is not a valid kind.

type Type interface {

	// Name returns the type's name within its package for a defined type.
	// For other (non-defined) types it returns the empty string.
	Name() string

	// PkgPath returns a defined type's package path, that is, the import path
	// that uniquely identifies the package, such as "encoding/base64".
	// If the type was predeclared (string, error) or not defined (*T, struct{},
	// []int, or A where A is an alias for a non-defined type), the package path
	// will be the empty string.
	PkgPath() string

	// Size returns the number of bytes needed to store
	// a value of the given type; it is analogous to unsafe.Sizeof.
	Size() uintptr

	// Kind returns the specific kind of this type.
	Kind() Kind

	// Implements reports whether the type implements the interface type u.
	Implements(u Type) bool

	// AssignableTo reports whether a value of the type is assignable to type u.
	AssignableTo(u Type) bool

	// Comparable reports whether values of this type are comparable.
	Comparable() bool

	// String returns a string representation of the type.
	// The string representation may use shortened package names
	// (e.g., base64 instead of "encoding/base64") and is not
	// guaranteed to be unique among types. To test for type identity,
	// compare the Types directly.
	String() string

	// Elem returns a type's element type.
	// It panics if the type's Kind is not Ptr.
	Elem() Type

	// Has unexported methods.
}
    Type is the representation of a Go type.

    Not all methods apply to all kinds of types. Restrictions, if any,
    are noted in the documentation for each method. Use the Kind method to find
    out the kind of type before calling kind-specific methods. Calling a method
    inappropriate to the kind of type causes a run-time panic.

    Type values are comparable, such as with the == operator, so they can be
    used as map keys. Two Type values are equal if they represent identical
    types.

func TypeOf(i any) Type
    TypeOf returns the reflection Type that represents the dynamic type of i.
    If i is a nil interface value, TypeOf returns nil.

type Value struct {
	// Has unexported fields.
}
    Value is the reflection interface to a Go value.

    Not all methods apply to all kinds of values. Restrictions, if any,
    are noted in the documentation for each method. Use the Kind method to find
    out the kind of value before calling kind-specific methods. Calling a method
    inappropriate to the kind of type causes a run time panic.

    The zero Value represents no value. Its IsValid method returns false, its
    Kind method returns Invalid, its String method returns "<invalid Value>",
    and all other methods panic. Most functions and methods never return
    an invalid value. If one does, its documentation states the conditions
    explicitly.

    A Value can be used concurrently by multiple goroutines provided that the
    underlying Go value can be used concurrently for the equivalent direct
    operations.

    To compare two Values, compare the results of the Interface method. Using ==
    on two Values does not compare the underlying values they represent.

func ValueOf(i any) Value
    ValueOf returns a new Value initialized to the concrete value stored in the
    interface i. ValueOf(nil) returns the zero Value.

func (v Value) CanSet() bool
    CanSet reports whether the value of v can be changed. A Value can be changed
    only if it is addressable and was not obtained by the use of unexported
    struct fields. If CanSet returns false, calling Set or any type-specific
    setter (e.g., SetBool, SetInt) will panic.

func (v Value) Elem() Value
    Elem returns the value that the interface v contains or that the pointer v
    points to. It panics if v's Kind is not Interface or Pointer. It returns the
    zero Value if v is nil.

func (v Value) IsNil() bool
    IsNil reports whether its argument v is nil. The argument must be a chan,
    func, interface, map, pointer, or slice value; if it is not, IsNil panics.
    Note that IsNil is not always equivalent to a regular comparison with nil in
    Go. For example, if v was created by calling ValueOf with an uninitialized
    interface variable i, i==nil will be true but v.IsNil will panic as v will
    be the zero Value.

func (v Value) IsValid() bool
    IsValid reports whether v represents a value. It returns false if v is the
    zero Value. If IsValid returns false, all other methods except String panic.
    Most functions and methods never return an invalid Value. If one does,
    its documentation states the conditions explicitly.

func (v Value) Kind() Kind
    Kind returns v's Kind. If v is the zero Value (IsValid returns false),
    Kind returns Invalid.

func (v Value) Len() int
    Len returns v's length. It panics if v's Kind is not Array, Chan, Map,
    Slice, or String.

func (v Value) Set(x Value)
    Set assigns x to the value v. It panics if CanSet returns false. As in Go,
    x's value must be assignable to v's type.

func (v Value) Type() Type
    Type returns v's type.

type ValueError struct {
	Method string
	Kind   Kind
}
    A ValueError occurs when a Value method is invoked on a Value that does not
    support it. Such cases are documented in the description of each method.

func (e *ValueError) Error() string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
