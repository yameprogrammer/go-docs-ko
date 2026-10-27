# package internal/runtime/gc

- 원문: <https://pkg.go.dev/internal/runtime/gc>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package gc // import "internal/runtime/gc"


CONSTANTS

const (
	// PageWords is the number of pointer-words per page.
	PageWords = PageSize / goarch.PtrSize

	// A malloc header is functionally a single type pointer, but
	// we need to use 8 here to ensure 8-byte alignment of allocations
	// on 32-bit platforms. It's wasteful, but a lot of code relies on
	// 8-byte alignment for 8-byte atomics.
	MallocHeaderSize = 8

	// The minimum object size that has a malloc header, exclusive.
	//
	// The size of this value controls overheads from the malloc header.
	// The minimum size is bound by writeHeapBitsSmall, which assumes that the
	// pointer bitmap for objects of a size smaller than this doesn't cross
	// more than one pointer-word boundary. This sets an upper-bound on this
	// value at the number of bits in a uintptr, multiplied by the pointer
	// size in bytes.
	//
	// We choose a value here that has a natural cutover point in terms of memory
	// overheads. This value just happens to be the maximum possible value this
	// can be.
	//
	// A span with heap bits in it will have 128 bytes of heap bits on 64-bit
	// platforms, and 256 bytes of heap bits on 32-bit platforms. The first size
	// class where malloc headers match this overhead for 64-bit platforms is
	// 512 bytes (8 KiB / 512 bytes * 8 bytes-per-header = 128 bytes of overhead).
	// On 32-bit platforms, this same point is the 256 byte size class
	// (8 KiB / 256 bytes * 8 bytes-per-header = 256 bytes of overhead).
	//
	// Guaranteed to be exactly at a size class boundary. The reason this value is
	// an exclusive minimum is subtle. Suppose we're allocating a 504-byte object
	// and its rounded up to 512 bytes for the size class. If minSizeForMallocHeader
	// is 512 and an inclusive minimum, then a comparison against minSizeForMallocHeader
	// by the two values would produce different results. In other words, the comparison
	// would not be invariant to size-class rounding. Eschewing this property means a
	// more complex check or possibly storing additional state to determine whether a
	// span has malloc headers.
	MinSizeForMallocHeader = goarch.PtrSize * goarch.PtrBits

	// PageSize is the increment in which spans are managed.
	PageSize = 1 << PageShift
)
const (
	MinHeapAlign       = 8
	MaxSmallSize       = 32768
	SmallSizeDiv       = 8
	SmallSizeMax       = 1024
	LargeSizeDiv       = 128
	NumSizeClasses     = 68
	PageShift          = 13
	MaxObjsPerSpan     = 1024
	MaxSizeClassNPages = 10
	TinySize           = 16
	TinySizeClass      = 2
)

VARIABLES

var SizeClassToDivMagic = [NumSizeClasses]uint32{0, ^uint32(0)/8 + 1, ^uint32(0)/16 + 1, ^uint32(0)/24 + 1, ^uint32(0)/32 + 1, ^uint32(0)/48 + 1, ^uint32(0)/64 + 1, ^uint32(0)/80 + 1, ^uint32(0)/96 + 1, ^uint32(0)/112 + 1, ^uint32(0)/128 + 1, ^uint32(0)/144 + 1, ^uint32(0)/160 + 1, ^uint32(0)/176 + 1, ^uint32(0)/192 + 1, ^uint32(0)/208 + 1, ^uint32(0)/224 + 1, ^uint32(0)/240 + 1, ^uint32(0)/256 + 1, ^uint32(0)/288 + 1, ^uint32(0)/320 + 1, ^uint32(0)/352 + 1, ^uint32(0)/384 + 1, ^uint32(0)/416 + 1, ^uint32(0)/448 + 1, ^uint32(0)/480 + 1, ^uint32(0)/512 + 1, ^uint32(0)/576 + 1, ^uint32(0)/640 + 1, ^uint32(0)/704 + 1, ^uint32(0)/768 + 1, ^uint32(0)/896 + 1, ^uint32(0)/1024 + 1, ^uint32(0)/1152 + 1, ^uint32(0)/1280 + 1, ^uint32(0)/1408 + 1, ^uint32(0)/1536 + 1, ^uint32(0)/1792 + 1, ^uint32(0)/2048 + 1, ^uint32(0)/2304 + 1, ^uint32(0)/2688 + 1, ^uint32(0)/3072 + 1, ^uint32(0)/3200 + 1, ^uint32(0)/3456 + 1, ^uint32(0)/4096 + 1, ^uint32(0)/4864 + 1, ^uint32(0)/5376 + 1, ^uint32(0)/6144 + 1, ^uint32(0)/6528 + 1, ^uint32(0)/6784 + 1, ^uint32(0)/6912 + 1, ^uint32(0)/8192 + 1, ^uint32(0)/9472 + 1, ^uint32(0)/9728 + 1, ^uint32(0)/10240 + 1, ^uint32(0)/10880 + 1, ^uint32(0)/12288 + 1, ^uint32(0)/13568 + 1, ^uint32(0)/14336 + 1, ^uint32(0)/16384 + 1, ^uint32(0)/18432 + 1, ^uint32(0)/19072 + 1, ^uint32(0)/20480 + 1, ^uint32(0)/21760 + 1, ^uint32(0)/24576 + 1, ^uint32(0)/27264 + 1, ^uint32(0)/28672 + 1, ^uint32(0)/32768 + 1}
var SizeClassToNPages = [NumSizeClasses]uint8{0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 3, 2, 3, 1, 3, 2, 3, 4, 5, 6, 1, 7, 6, 5, 4, 3, 5, 7, 2, 9, 7, 5, 8, 3, 10, 7, 4}
var SizeClassToSize = [NumSizeClasses]uint16{0, 8, 16, 24, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 256, 288, 320, 352, 384, 416, 448, 480, 512, 576, 640, 704, 768, 896, 1024, 1152, 1280, 1408, 1536, 1792, 2048, 2304, 2688, 3072, 3200, 3456, 4096, 4864, 5376, 6144, 6528, 6784, 6912, 8192, 9472, 9728, 10240, 10880, 12288, 13568, 14336, 16384, 18432, 19072, 20480, 21760, 24576, 27264, 28672, 32768}
var SizeToSizeClass128 = [(MaxSmallSize-SmallSizeMax)/LargeSizeDiv + 1]uint8{32, 33, 34, 35, 36, 37, 37, 38, 38, 39, 39, 40, 40, 40, 41, 41, 41, 42, 43, 43, 44, 44, 44, 44, 44, 45, 45, 45, 45, 45, 45, 46, 46, 46, 46, 47, 47, 47, 47, 47, 47, 48, 48, 48, 49, 49, 50, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 53, 53, 54, 54, 54, 54, 55, 55, 55, 55, 55, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 58, 58, 58, 58, 58, 58, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 61, 61, 61, 61, 61, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 66, 66, 66, 66, 66, 66, 66, 66, 66, 66, 66, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67}
var SizeToSizeClass8 = [SmallSizeMax/SmallSizeDiv + 1]uint8{0, 1, 2, 3, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 19, 19, 20, 20, 20, 20, 21, 21, 21, 21, 22, 22, 22, 22, 23, 23, 23, 23, 24, 24, 24, 24, 25, 25, 25, 25, 26, 26, 26, 26, 27, 27, 27, 27, 27, 27, 27, 27, 28, 28, 28, 28, 28, 28, 28, 28, 29, 29, 29, 29, 29, 29, 29, 29, 30, 30, 30, 30, 30, 30, 30, 30, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32}

TYPES

type ObjMask [MaxObjsPerSpan / (goarch.PtrSize * 8)]uintptr
    ObjMask is a bitmap where each bit corresponds to an object in a span.

    It is sized to accommodate all size classes.

type PtrMask [PageSize / goarch.PtrSize / (goarch.PtrSize * 8)]uintptr
    PtrMask is a bitmap where each bit represents a pointer-word in a single
    runtime page.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
