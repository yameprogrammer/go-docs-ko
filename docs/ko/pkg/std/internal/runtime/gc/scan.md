# package internal/runtime/gc/scan

- 원문: <https://pkg.go.dev/internal/runtime/gc/scan>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package scan // import "internal/runtime/gc/scan"


FUNCTIONS

func CanAVX512() bool
func ExpandAVX512(sizeClass int, packed *gc.ObjMask, unpacked *gc.PtrMask)
    ExpandAVX512 expands each bit in packed into f consecutive bits in unpacked,
    where f is the word size of objects in sizeClass.

    This is a testing entrypoint to the expanders used by scanSpanPacked*.

func ExpandReference(sizeClass int, packed *gc.ObjMask, unpacked *gc.PtrMask)
    ExpandReference is a reference implementation of an expander function that
    translates object mark bits into a bitmap of one bit per word of marked
    object, assuming the object is of the provided size class.

func FilterNil(bufp *uintptr, n int32) int32
    FilterNil packs non-nil (non-zero) values in bufp together at the beginning
    of bufp, returning the length of the packed buffer. It treats bufp as an
    array of size n.

func FilterNilAVX512(bufp *uintptr, n int32) int32
    FilterNilAVX512 is the simd version of FilterNil, it is implemented in
    assembly.

func HasFastScanSpanPacked() bool
func ScanSpanPacked(mem unsafe.Pointer, bufp *uintptr, objMarks *gc.ObjMask, sizeClass uintptr, ptrMask *gc.PtrMask) (count int32)
func ScanSpanPackedAVX512(mem unsafe.Pointer, bufp *uintptr, objMarks *gc.ObjMask, sizeClass uintptr, ptrMask *gc.PtrMask) (count int32)
func ScanSpanPackedGo(mem unsafe.Pointer, bufp *uintptr, objMarks *gc.ObjMask, sizeClass uintptr, ptrMask *gc.PtrMask) (count int32)
    ScanSpanPackedGo is an optimized pure Go implementation of ScanSpanPacked.

func ScanSpanPackedReference(mem unsafe.Pointer, bufp *uintptr, objMarks *gc.ObjMask, sizeClass uintptr, ptrMask *gc.PtrMask) (count int32)
    ScanSpanPackedReference is the reference implementation of ScanScanPacked.
    It prioritizes clarity over performance.

    Concretely, ScanScanPacked functions read pointers from mem, assumed to be
    gc.PageSize-aligned and gc.PageSize in size, and writes them to bufp, which
    is large enough to guarantee that even if pointer-word of mem is a pointer,
    it will fit. Therefore bufp, is always at least gc.PageSize in size.

    ScanSpanPacked is supposed to identify pointers by first
    filtering words by objMarks, where each bit of the mask represents
    gc.SizeClassToSize[sizeClass] bytes of memory, and then filtering again by
    the bits in ptrMask.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
