# package internal/runtime/atomic

- 원문: <https://pkg.go.dev/internal/runtime/atomic>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package atomic provides atomic operations, independent of sync/atomic, to the runtime.

## 원문 요약

Package atomic provides atomic operations, independent of sync/atomic, to the runtime.

## API 상세 (go doc -all)

~~~text
package atomic // import "internal/runtime/atomic"

Package atomic provides atomic operations, independent of sync/atomic, to the
runtime.

On most platforms, the compiler is aware of the functions defined in this
package, and they're replaced with platform-specific intrinsics. On other
platforms, generic implementations are made available.

Unless otherwise noted, operations defined in this package are sequentially
consistent across threads with respect to the values they manipulate.
More specifically, operations that happen in a specific order on one thread,
will always be observed to happen in exactly that order by another thread.

FUNCTIONS

func And(ptr *uint32, val uint32)
func And32(ptr *uint32, val uint32) uint32
func And64(ptr *uint64, val uint64) uint64
func And8(ptr *uint8, val uint8)
func Anduintptr(ptr *uintptr, val uintptr) uintptr
func Cas(ptr *uint32, old, new uint32) bool
func Cas64(ptr *uint64, old, new uint64) bool
func CasRel(ptr *uint32, old, new uint32) bool
func Casint32(ptr *int32, old, new int32) bool
func Casint64(ptr *int64, old, new int64) bool
func Casp1(ptr *unsafe.Pointer, old, new unsafe.Pointer) bool
    NO go:noescape annotation; see atomic_pointer.go.

func Casuintptr(ptr *uintptr, old, new uintptr) bool
func Load(ptr *uint32) uint32
func Load64(ptr *uint64) uint64
func Load8(ptr *uint8) uint8
func LoadAcq(ptr *uint32) uint32
func LoadAcq64(ptr *uint64) uint64
func LoadAcquintptr(ptr *uintptr) uintptr
func Loadint32(ptr *int32) int32
func Loadint64(ptr *int64) int64
func Loadp(ptr unsafe.Pointer) unsafe.Pointer
func Loaduint(ptr *uint) uint
func Loaduintptr(ptr *uintptr) uintptr
func Or(ptr *uint32, val uint32)
func Or32(ptr *uint32, val uint32) uint32
func Or64(ptr *uint64, val uint64) uint64
func Or8(ptr *uint8, val uint8)
func Oruintptr(ptr *uintptr, val uintptr) uintptr
func Store(ptr *uint32, val uint32)
func Store64(ptr *uint64, val uint64)
func Store8(ptr *uint8, val uint8)
func StoreRel(ptr *uint32, val uint32)
func StoreRel64(ptr *uint64, val uint64)
func StoreReluintptr(ptr *uintptr, val uintptr)
func Storeint32(ptr *int32, new int32)
func Storeint64(ptr *int64, new int64)
func StorepNoWB(ptr unsafe.Pointer, val unsafe.Pointer)
    StorepNoWB performs *ptr = val atomically and without a write barrier.

    NO go:noescape annotation; see atomic_pointer.go.

func Storeuintptr(ptr *uintptr, new uintptr)
func Xadd(ptr *uint32, delta int32) uint32
func Xadd64(ptr *uint64, delta int64) uint64
func Xaddint32(ptr *int32, delta int32) int32
func Xaddint64(ptr *int64, delta int64) int64
func Xadduintptr(ptr *uintptr, delta uintptr) uintptr
func Xchg(ptr *uint32, new uint32) uint32
func Xchg64(ptr *uint64, new uint64) uint64
func Xchg8(ptr *uint8, new uint8) uint8
func Xchgint32(ptr *int32, new int32) int32
func Xchgint64(ptr *int64, new int64) int64
func Xchguintptr(ptr *uintptr, new uintptr) uintptr

TYPES

type Bool struct {
	// Has unexported fields.
}
    Bool is an atomically accessed bool value.

    A Bool must not be copied.

func (b *Bool) Load() bool
    Load accesses and returns the value atomically.

func (b *Bool) Store(value bool)
    Store updates the value atomically.

type Float64 struct {
	// Has unexported fields.
}
    Float64 is an atomically accessed float64 value.

    8-byte aligned on all platforms, unlike a regular float64.

    A Float64 must not be copied.

func (f *Float64) Load() float64
    Load accesses and returns the value atomically.

func (f *Float64) Store(value float64)
    Store updates the value atomically.

type Int32 struct {
	// Has unexported fields.
}
    Int32 is an atomically accessed int32 value.

    An Int32 must not be copied.

func (i *Int32) Add(delta int32) int32
    Add adds delta to i atomically, returning the new updated value.

    This operation wraps around in the usual two's-complement way.

func (i *Int32) CompareAndSwap(old, new int32) bool
    CompareAndSwap atomically compares i's value with old, and if they're equal,
    swaps i's value with new. It reports whether the swap ran.

func (i *Int32) Load() int32
    Load accesses and returns the value atomically.

func (i *Int32) Store(value int32)
    Store updates the value atomically.

func (i *Int32) Swap(new int32) int32
    Swap replaces i's value with new, returning i's value before the
    replacement.

type Int64 struct {
	// Has unexported fields.
}
    Int64 is an atomically accessed int64 value.

    8-byte aligned on all platforms, unlike a regular int64.

    An Int64 must not be copied.

func (i *Int64) Add(delta int64) int64
    Add adds delta to i atomically, returning the new updated value.

    This operation wraps around in the usual two's-complement way.

func (i *Int64) CompareAndSwap(old, new int64) bool
    CompareAndSwap atomically compares i's value with old, and if they're equal,
    swaps i's value with new. It reports whether the swap ran.

func (i *Int64) Load() int64
    Load accesses and returns the value atomically.

func (i *Int64) Store(value int64)
    Store updates the value atomically.

func (i *Int64) Swap(new int64) int64
    Swap replaces i's value with new, returning i's value before the
    replacement.

type Pointer[T any] struct {
	// Has unexported fields.
}
    Pointer is an atomic pointer of type *T.

func (p *Pointer[T]) CompareAndSwap(old, new *T) bool
    CompareAndSwap atomically (with respect to other methods) compares u's value
    with old, and if they're equal, swaps u's value with new. It reports whether
    the swap ran.

func (p *Pointer[T]) CompareAndSwapNoWB(old, new *T) bool
    CompareAndSwapNoWB atomically (with respect to other methods) compares u's
    value with old, and if they're equal, swaps u's value with new. It reports
    whether the swap ran.

    WARNING: As the name implies this operation does *not* perform a write
    barrier on value, and so this operation may hide pointers from the GC.
    Use with care and sparingly. It is safe to use with values not found in the
    Go heap. Prefer CompareAndSwap instead.

func (p *Pointer[T]) Load() *T
    Load accesses and returns the value atomically.

func (p *Pointer[T]) Store(value *T)
    Store updates the value atomically.

func (p *Pointer[T]) StoreNoWB(value *T)
    StoreNoWB updates the value atomically.

    WARNING: As the name implies this operation does *not* perform a write
    barrier on value, and so this operation may hide pointers from the GC.
    Use with care and sparingly. It is safe to use with values not found in the
    Go heap. Prefer Store instead.

type Uint32 struct {
	// Has unexported fields.
}
    Uint32 is an atomically accessed uint32 value.

    A Uint32 must not be copied.

func (u *Uint32) Add(delta int32) uint32
    Add adds delta to u atomically, returning the new updated value.

    This operation wraps around in the usual two's-complement way.

func (u *Uint32) And(value uint32)
    And takes value and performs a bit-wise "and" operation with the value of u,
    storing the result into u.

    The full process is performed atomically.

func (u *Uint32) CompareAndSwap(old, new uint32) bool
    CompareAndSwap atomically compares u's value with old, and if they're equal,
    swaps u's value with new. It reports whether the swap ran.

func (u *Uint32) CompareAndSwapRelease(old, new uint32) bool
    CompareAndSwapRelease is a partially unsynchronized version of Cas that
    relaxes ordering constraints. Other threads may observe operations that
    occur after this operation to precede it, but no operation that precedes
    it on this thread can be observed to occur after it. It reports whether the
    swap ran.

    WARNING: Use sparingly and with great care.

func (u *Uint32) Load() uint32
    Load accesses and returns the value atomically.

func (u *Uint32) LoadAcquire() uint32
    LoadAcquire is a partially unsynchronized version of Load that relaxes
    ordering constraints. Other threads may observe operations that precede this
    operation to occur after it, but no operation that occurs after it on this
    thread can be observed to occur before it.

    WARNING: Use sparingly and with great care.

func (u *Uint32) Or(value uint32)
    Or takes value and performs a bit-wise "or" operation with the value of u,
    storing the result into u.

    The full process is performed atomically.

func (u *Uint32) Store(value uint32)
    Store updates the value atomically.

func (u *Uint32) StoreRelease(value uint32)
    StoreRelease is a partially unsynchronized version of Store that relaxes
    ordering constraints. Other threads may observe operations that occur after
    this operation to precede it, but no operation that precedes it on this
    thread can be observed to occur after it.

    WARNING: Use sparingly and with great care.

func (u *Uint32) Swap(value uint32) uint32
    Swap replaces u's value with new, returning u's value before the
    replacement.

type Uint64 struct {
	// Has unexported fields.
}
    Uint64 is an atomically accessed uint64 value.

    8-byte aligned on all platforms, unlike a regular uint64.

    A Uint64 must not be copied.

func (u *Uint64) Add(delta int64) uint64
    Add adds delta to u atomically, returning the new updated value.

    This operation wraps around in the usual two's-complement way.

func (u *Uint64) CompareAndSwap(old, new uint64) bool
    CompareAndSwap atomically compares u's value with old, and if they're equal,
    swaps u's value with new. It reports whether the swap ran.

func (u *Uint64) Load() uint64
    Load accesses and returns the value atomically.

func (u *Uint64) LoadAcquire() uint64
    LoadAcquire is a partially unsynchronized version of Load that relaxes
    ordering constraints. Other threads may observe operations that precede this
    operation to occur after it, but no operation that occurs after it on this
    thread can be observed to occur before it.

    WARNING: Use sparingly and with great care.

func (u *Uint64) Store(value uint64)
    Store updates the value atomically.

func (u *Uint64) StoreRelease(value uint64)
    StoreRelease is a partially unsynchronized version of Store that relaxes
    ordering constraints. Other threads may observe operations that occur after
    this operation to precede it, but no operation that precedes it on this
    thread can be observed to occur after it.

    WARNING: Use sparingly and with great care.

func (u *Uint64) Swap(value uint64) uint64
    Swap replaces u's value with new, returning u's value before the
    replacement.

type Uint8 struct {
	// Has unexported fields.
}
    Uint8 is an atomically accessed uint8 value.

    A Uint8 must not be copied.

func (u *Uint8) And(value uint8)
    And takes value and performs a bit-wise "and" operation with the value of u,
    storing the result into u.

    The full process is performed atomically.

func (u *Uint8) Load() uint8
    Load accesses and returns the value atomically.

func (u *Uint8) Or(value uint8)
    Or takes value and performs a bit-wise "or" operation with the value of u,
    storing the result into u.

    The full process is performed atomically.

func (u *Uint8) Store(value uint8)
    Store updates the value atomically.

type Uintptr struct {
	// Has unexported fields.
}
    Uintptr is an atomically accessed uintptr value.

    A Uintptr must not be copied.

func (u *Uintptr) Add(delta uintptr) uintptr
    Add adds delta to u atomically, returning the new updated value.

    This operation wraps around in the usual two's-complement way.

func (u *Uintptr) CompareAndSwap(old, new uintptr) bool
    CompareAndSwap atomically compares u's value with old, and if they're equal,
    swaps u's value with new. It reports whether the swap ran.

func (u *Uintptr) Load() uintptr
    Load accesses and returns the value atomically.

func (u *Uintptr) LoadAcquire() uintptr
    LoadAcquire is a partially unsynchronized version of Load that relaxes
    ordering constraints. Other threads may observe operations that precede this
    operation to occur after it, but no operation that occurs after it on this
    thread can be observed to occur before it.

    WARNING: Use sparingly and with great care.

func (u *Uintptr) Store(value uintptr)
    Store updates the value atomically.

func (u *Uintptr) StoreRelease(value uintptr)
    StoreRelease is a partially unsynchronized version of Store that relaxes
    ordering constraints. Other threads may observe operations that occur after
    this operation to precede it, but no operation that precedes it on this
    thread can be observed to occur after it.

    WARNING: Use sparingly and with great care.

func (u *Uintptr) Swap(value uintptr) uintptr
    Swap replaces u's value with new, returning u's value before the
    replacement.

type UnsafePointer struct {
	// Has unexported fields.
}
    UnsafePointer is an atomically accessed unsafe.Pointer value.

    Note that because of the atomicity guarantees, stores to values of this type
    never trigger a write barrier, and the relevant methods are suffixed with
    "NoWB" to indicate that explicitly. As a result, this type should be used
    carefully, and sparingly, mostly with values that do not live in the Go heap
    anyway.

    An UnsafePointer must not be copied.

func (u *UnsafePointer) CompareAndSwap(old, new unsafe.Pointer) bool
    CompareAndSwap atomically compares u's value with old, and if they're equal,
    swaps u's value with new. It reports whether the swap ran.

func (u *UnsafePointer) CompareAndSwapNoWB(old, new unsafe.Pointer) bool
    CompareAndSwapNoWB atomically (with respect to other methods) compares u's
    value with old, and if they're equal, swaps u's value with new. It reports
    whether the swap ran.

    WARNING: As the name implies this operation does *not* perform a write
    barrier on value, and so this operation may hide pointers from the GC.
    Use with care and sparingly. It is safe to use with values not found in the
    Go heap. Prefer CompareAndSwap instead.

func (u *UnsafePointer) Load() unsafe.Pointer
    Load accesses and returns the value atomically.

func (u *UnsafePointer) Store(value unsafe.Pointer)
    Store updates the value atomically.

func (u *UnsafePointer) StoreNoWB(value unsafe.Pointer)
    StoreNoWB updates the value atomically.

    WARNING: As the name implies this operation does *not* perform a write
    barrier on value, and so this operation may hide pointers from the GC.
    Use with care and sparingly. It is safe to use with values not found in the
    Go heap. Prefer Store instead.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
