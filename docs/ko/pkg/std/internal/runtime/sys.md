# package internal/runtime/sys

- 원문: <https://pkg.go.dev/internal/runtime/sys>
- 분류: Go 표준 라이브러리

## 한국어 요약

`sys` 패키지는 런타임에서 사용하는 시스템, 설정 및 아키텍처 전용 상수를 포함합니다.

## 원문 요약

package sys contains system- and configuration- and architecture-specific constants used by the runtime.

## API 상세 (go doc -all)

~~~text
package sys // import "internal/runtime/sys"

package sys contains system- and configuration- and architecture-specific
constants used by the runtime.

CONSTANTS

const DefaultPhysPageSize = goarch.DefaultPhysPageSize
    DefaultPhysPageSize is the default physical page size.

const Int64Align = goarch.PtrSize
    Int64Align is the required alignment for a 64-bit integer (4 on 32-bit
    systems, 8 on 64-bit).

const MinFrameSize = goarch.MinFrameSize
    MinFrameSize is the size of the system-reserved words at the bottom of
    a frame (just above the architectural stack pointer). It is zero on x86
    and PtrSize on most non-x86 (LR-based) systems. On PowerPC it is larger,
    to cover three more reserved words: the compiler word, the link editor word,
    and the TOC save word.

const PCQuantum = goarch.PCQuantum
    PCQuantum is the minimal unit for a program counter (1 on x86, 4 on most
    other systems). The various PC tables record PC deltas pre-divided by
    PCQuantum.

const StackAlign = goarch.StackAlign
    StackAlign is the required alignment of the SP register. The stack must be
    at least word aligned, but some architectures require more.

const StackGuardMultiplier = 1 + goos.IsAix + goos.IsOpenbsd + isRace
    AIX and OpenBSD require a larger stack for syscalls. The race build also
    needs more stack. See issue 54291. This arithmetic must match that in
    cmd/internal/objabi/stack.go:stackGuardMultiplier.


VARIABLES

var DITSupported = false

FUNCTIONS

func Bswap32(x uint32) uint32
    Bswap32 returns its input with byte order reversed 0x01020304 -> 0x04030201

func Bswap64(x uint64) uint64
    Bswap64 returns its input with byte order reversed 0x0102030405060708 ->
    0x0807060504030201

func DITEnabled() bool
func DisableDIT()
func EnableDIT() bool
func GetCallerPC() uintptr
func GetCallerSP() uintptr
func GetClosurePtr() uintptr
    GetClosurePtr returns the pointer to the current closure. GetClosurePtr
    can only be used in an assignment statement at the entry of a function.
    Moreover, go:nosplit directive must be specified at the declaration of
    caller function, so that the function prolog does not clobber the closure
    register. for example:

        //go:nosplit
        func f(arg1, arg2, arg3 int) {
        	dx := GetClosurePtr()
        }

    The compiler rewrites calls to this function into instructions that fetch
    the pointer from a well-known register (DX on x86 architecture, etc.)
    directly.

    WARNING: PGO-based devirtualization cannot detect that
    caller of GetClosurePtr requires closure context,
    and thus must maintain a list of these functions, which is in
    cmd/compile/internal/devirtualize/pgo.maybeDevirtualizeFunctionCall.

func LeadingZeros64(x uint64) int
    LeadingZeros64 returns the number of leading zero bits in x; the result is
    64 for x == 0.

func LeadingZeros8(x uint8) int
    LeadingZeros8 returns the number of leading zero bits in x; the result is 8
    for x == 0.

func Len64(x uint64) (n int)
    Len64 returns the minimum number of bits required to represent x; the result
    is 0 for x == 0.

    nosplit because this is used in src/runtime/histogram.go, which make run in
    sensitive contexts.

func Len8(x uint8) int
    Len8 returns the minimum number of bits required to represent x; the result
    is 0 for x == 0.

func OnesCount64(x uint64) int
    OnesCount64 returns the number of one bits ("population count") in x.

func Prefetch(addr uintptr)
    Prefetch prefetches data from memory addr to cache

    AMD64: Produce PREFETCHT0 instruction

    ARM64: Produce PRFM instruction with PLDL1KEEP option

func PrefetchStreamed(addr uintptr)
    PrefetchStreamed prefetches data from memory addr, with a hint that this
    data is being streamed. That is, it is likely to be accessed very soon,
    but only once. If possible, this will avoid polluting the cache.

    AMD64: Produce PREFETCHNTA instruction

    ARM64: Produce PRFM instruction with PLDL1STRM option

func TrailingZeros32(x uint32) int
    TrailingZeros32 returns the number of trailing zero bits in x; the result is
    32 for x == 0.

func TrailingZeros64(x uint64) int
    TrailingZeros64 returns the number of trailing zero bits in x; the result is
    64 for x == 0.

func TrailingZeros8(x uint8) int
    TrailingZeros8 returns the number of trailing zero bits in x; the result is
    8 for x == 0.


TYPES

type NotInHeap struct {
	// Has unexported fields.
}
    NotInHeap is a type must never be allocated from the GC'd heap or on the
    stack, and is called not-in-heap.

    Other types can embed NotInHeap to make it not-in-heap. Specifically,
    pointers to these types must always fail the `runtime.inheap` check.
    The type may be used for global variables, or for objects in unmanaged
    memory (e.g., allocated with `sysAlloc`, `persistentalloc`, `fixalloc`,
    or from a manually-managed span).

    Specifically:

    1. `new(T)`, `make([]T)`, `append([]T, ...)` and implicit heap allocation of
    T are disallowed. (Though implicit allocations are disallowed in the runtime
    anyway.)

    2. A pointer to a regular type (other than `unsafe.Pointer`) cannot be
    converted to a pointer to a not-in-heap type, even if they have the same
    underlying type.

    3. Any type that containing a not-in-heap type is itself considered as
    not-in-heap.

    - Structs and arrays are not-in-heap if their elements are not-in-heap.
    - Maps and channels contains no-in-heap types are disallowed.

    4. Write barriers on pointers to not-in-heap types can be omitted.

    The last point is the real benefit of NotInHeap. The runtime uses it for
    low-level internal structures to avoid memory barriers in the scheduler
    and the memory allocator where they are illegal or simply inefficient.
    This mechanism is reasonably safe and does not compromise the readability of
    the runtime.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
