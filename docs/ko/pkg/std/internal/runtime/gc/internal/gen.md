# package internal/runtime/gc/internal/gen

- 원문: <https://pkg.go.dev/internal/runtime/gc/internal/gen>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package gen // import "internal/runtime/gc/internal/gen"


FUNCTIONS

func Arg[W wrap[T], T Word](fn *Func) T
func Deref[W wrap[T], T Value](ptr Ptr[W]) T
func Return(results ...Value)

TYPES

type Array[T Value] struct {
	// Has unexported fields.
}

func ConstArray[T Value](vals []T, name string) (y Array[T])

func (o Array) String() string

type File struct {
	// Has unexported fields.
}

func NewFile(w io.Writer) *File

func (f *File) AddConst(name string, data any)

func (f *File) AddFunc(fn *Func)

func (f *File) Compile()

type Func struct {
	// Has unexported fields.
}

func NewFunc(name string) *Func

type Mask64 struct {
	// Has unexported fields.
}

func ConstMask64(c uint64) (y Mask64)

func (x Mask64) Or(y Mask64) (z Mask64)

func (x Mask64) ShiftLeft(c uint8) (z Mask64)

func (x Mask64) ShiftRight(c uint8) (z Mask64)

func (o Mask64) String() string

func (x Mask64) ToUint64() (z Uint64)

type Mask8 struct {
	// Has unexported fields.
}

func ConstMask8(c uint8) (y Mask8)

func (x Mask8) Or(y Mask8) (z Mask8)

func (x Mask8) ShiftLeft(c uint8) (z Mask8)

func (o Mask8) String() string

func (x Mask8) ToUint8() (z Uint64)

type Ptr[T Value] struct {
	// Has unexported fields.
}

func (x Ptr[T]) AddConst(off int) (y Ptr[T])

func (o Ptr) String() string

type Uint64 struct {
	// Has unexported fields.
}

func ConstUint64(c uint64, name string) (y Uint64)

func (o Uint64) String() string

type Uint64x8 struct {
	// Has unexported fields.
}

func BroadcastUint64x8Zeroed(src Uint64, mask Mask8) (z Uint64x8)

func ConstUint64x8(c [8]uint64, name string) (y Uint64x8)

func (x Uint64x8) BroadcastMasked(src Uint64, mask Mask8) (z Uint64x8)

func (x Uint64x8) GF2P8Affine(y Uint8x64) (z Uint8x64)

func (x Uint64x8) Or(y Uint64x8) (z Uint64x8)

func (x Uint64x8) ShuffleBits(y Uint8x64) (z Mask64)

func (x Uint64x8) ShuffleBitsMasked(y Uint8x64, mask Mask64) (z Mask64)

func (o Uint64x8) String() string

func (x Uint64x8) Sub(y Uint64x8) (z Uint64x8)

func (x Uint64x8) ToUint8x64() (z Uint8x64)

type Uint8x64 struct {
	// Has unexported fields.
}

func ConstUint8x64(c [64]uint8, name string) (y Uint8x64)

func (x Uint8x64) Shuffle(shuf Uint8x64) (y Uint8x64)

func (x Uint8x64) Shuffle2(y Uint8x64, shuf Uint8x64) (z Uint8x64)

func (x Uint8x64) Shuffle2Masked(y Uint8x64, shuf Uint8x64, mask Mask64) (z Uint8x64)

func (x Uint8x64) Shuffle2Zeroed(y Uint8x64, shuf Uint8x64, mask Mask64) (z Uint8x64)

func (x Uint8x64) ShuffleMasked(shuf Uint8x64, mask Mask64) (y Uint8x64)

func (x Uint8x64) ShuffleZeroed(shuf Uint8x64, mask Mask64) (y Uint8x64)

func (o Uint8x64) String() string

func (x Uint8x64) ToUint64x8() (z Uint64x8)

type Value interface {
	// Has unexported methods.
}

type Word interface {
	Value
	// Has unexported methods.
}
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
