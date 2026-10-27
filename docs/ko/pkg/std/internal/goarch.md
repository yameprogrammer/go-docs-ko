# package internal/goarch

- 원문: <https://pkg.go.dev/internal/goarch>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `goarch`는 `GOARCH`-특이한 상수들을 포함합니다.

## 원문 요약

package goarch contains GOARCH-specific constants.

## API 상세 (go doc -all)

~~~text
package goarch // import "internal/goarch"

package goarch contains GOARCH-specific constants.

CONSTANTS

const BigEndian = IsArmbe|IsArm64be|IsMips|IsMips64|IsPpc|IsPpc64|IsS390|IsS390x|IsSparc|IsSparc64 == 1
    BigEndian reports whether the architecture is big-endian.

const DefaultPhysPageSize = _DefaultPhysPageSize
    DefaultPhysPageSize is the default physical page size.

const GOARCH = `amd64`
const Int64Align = PtrSize
    Int64Align is the required alignment for a 64-bit integer (4 on 32-bit
    systems, 8 on 64-bit).

const Is386 = 0
const IsAmd64 = 1
const IsAmd64p32 = 0
const IsArm = 0
const IsArm64 = 0
const IsArm64be = 0
const IsArmbe = 0
const IsLoong64 = 0
const IsMips = 0
const IsMips64 = 0
const IsMips64le = 0
const IsMips64p32 = 0
const IsMips64p32le = 0
const IsMipsle = 0
const IsPpc = 0
const IsPpc64 = 0
const IsPpc64le = 0
const IsRiscv = 0
const IsRiscv64 = 0
const IsS390 = 0
const IsS390x = 0
const IsSparc = 0
const IsSparc64 = 0
const IsWasm = 0
const MinFrameSize = _MinFrameSize
    MinFrameSize is the size of the system-reserved words at the bottom of
    a frame (just above the architectural stack pointer). It is zero on x86
    and PtrSize on most non-x86 (LR-based) systems. On PowerPC it is larger,
    to cover three more reserved words: the compiler word, the link editor word,
    and the TOC save word.

const PCQuantum = _PCQuantum
    PCQuantum is the minimal unit for a program counter (1 on x86, 4 on most
    other systems). The various PC tables record PC deltas pre-divided by
    PCQuantum.

const PtrBits = PtrSize * 8
    PtrBits is bit width of a pointer.

const PtrSize = 4 << (^uintptr(0) >> 63)
    PtrSize is the size of a pointer in bytes - unsafe.Sizeof(uintptr(0)) but
    as an ideal constant. It is also the size of the machine's native word size
    (that is, 4 on 32-bit systems, 8 on 64-bit).

const StackAlign = _StackAlign
    StackAlign is the required alignment of the SP register. The stack must be
    at least word aligned, but some architectures require more.


TYPES

type ArchFamilyType int
    ArchFamilyType represents a family of one or more related architectures.
    For example, ppc64 and ppc64le are both members of the PPC64 family.

const (
	AMD64 ArchFamilyType = iota
	ARM
	ARM64
	I386
	LOONG64
	MIPS
	MIPS64
	PPC64
	RISCV64
	S390X
	WASM
)
const ArchFamily ArchFamilyType = _ArchFamily
    ArchFamily is the architecture family (AMD64, ARM, ...)
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
