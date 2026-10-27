# package internal/abi

- 원문: <https://pkg.go.dev/internal/abi>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package abi // import "internal/abi"


CONSTANTS

const (

	// RAX, RBX, RCX, RDI, RSI, R8, R9, R10, R11.
	IntArgRegs = 9

	// X0 -> X14.
	FloatArgRegs = 15

	// We use SSE2 registers which support 64-bit float operations.
	EffectiveFloatRegSize = 8
)
const (
	BoundsMaxReg   = 15
	BoundsMaxConst = 31
)
const (
	// Number of bits in the group.slot count.
	MapGroupSlotsBits = 3

	// Number of slots in a group.
	MapGroupSlots = 1 << MapGroupSlotsBits // 8

	// Maximum key or elem size to keep inline (instead of mallocing per element).
	// Must fit in a uint8.
	MapMaxKeyBytes  = 128
	MapMaxElemBytes = 128

	// Value of control word with all empty slots.
	MapCtrlEmpty = bitsetLSB * uint64(ctrlEmpty)
)
    Map constants common to several packages
    runtime/runtime-gdb.py:MapTypePrinter contains its own copy

const (
	MapNeedKeyUpdate = 1 << iota
	MapHashMightPanic
	MapIndirectKey
	MapIndirectElem
)
    Flag values

const (
	RF_DONE          = RF_State(iota) // body of loop has exited in a non-panic way
	RF_READY                          // body of loop has not exited yet, is not running  -- this is not a panic index
	RF_PANIC                          // body of loop is either currently running, or has panicked
	RF_EXHAUSTED                      // iterator function return, i.e., sequence is "exhausted"
	RF_MISSING_PANIC = 4              // body of loop panicked but iterator function defer-recovered it away
)
    These constants are shared between the compiler, which uses them for state
    functions and panic indicators, and the runtime, which turns them into more
    meaningful strings For best code generation, RF_DONE and RF_READY should be
    0 and 1.

const (
	// StackNosplitBase is the base maximum number of bytes that a chain of
	// NOSPLIT functions can use.
	//
	// This value must be multiplied by the stack guard multiplier, so do not
	// use it directly. See runtime/stack.go:stackNosplit and
	// cmd/internal/objabi/stack.go:StackNosplit.
	StackNosplitBase = 800

	// After a stack split check the SP is allowed to be StackSmall bytes below
	// the stack guard.
	//
	// Functions that need frames <= StackSmall can perform the stack check
	// using a single comparison directly between the stack guard and the SP
	// because we ensure that StackSmall bytes of stack space are available
	// beyond the stack guard.
	StackSmall = 128

	// Functions that need frames <= StackBig can assume that neither
	// SP-framesize nor stackGuard-StackSmall will underflow, and thus use a
	// more efficient check. In order to ensure this, StackBig must be <= the
	// size of the unmapped space at zero.
	StackBig = 4096
)
const (
	PCDATA_UnsafePoint   = 0
	PCDATA_StackMapIndex = 1
	PCDATA_InlTreeIndex  = 2
	PCDATA_ArgLiveIndex  = 3
	PCDATA_PanicBounds   = 4

	FUNCDATA_ArgsPointerMaps    = 0
	FUNCDATA_LocalsPointerMaps  = 1
	FUNCDATA_StackObjects       = 2
	FUNCDATA_InlTree            = 3
	FUNCDATA_OpenCodedDeferInfo = 4
	FUNCDATA_ArgInfo            = 5
	FUNCDATA_ArgLiveInfo        = 6
	FUNCDATA_WrapInfo           = 7
)
    IDs for PCDATA and FUNCDATA tables in Go binaries.

    These must agree with ../../../runtime/funcdata.h.

const (
	UnsafePointSafe   = -1 // Safe for async preemption
	UnsafePointUnsafe = -2 // Unsafe for async preemption

	// UnsafePointRestart1(2) apply on a sequence of instructions, within
	// which if an async preemption happens, we should back off the PC
	// to the start of the sequence when resuming.
	// We need two so we can distinguish the start/end of the sequence
	// in case that two sequences are next to each other.
	UnsafePointRestart1 = -3
	UnsafePointRestart2 = -4

	// Like UnsafePointRestart1, but back to function entry if async preempted.
	UnsafePointRestartAtEntry = -5
)
    Special values for the PCDATA_UnsafePoint table.

const (
	// TFlagUncommon means that there is a data with a type, UncommonType,
	// just beyond the shared-per-type common data.  That is, the data
	// for struct types will store their UncommonType at one offset, the
	// data for interface types will store their UncommonType at a different
	// offset.  UncommonType is always accessed via a pointer that is computed
	// using trust-us-we-are-the-implementors pointer arithmetic.
	//
	// For example, if t.Kind() == Struct and t.tflag&TFlagUncommon != 0,
	// then t has UncommonType data and it can be accessed as:
	//
	//	type structTypeUncommon struct {
	//		structType
	//		u UncommonType
	//	}
	//	u := &(*structTypeUncommon)(unsafe.Pointer(t)).u
	TFlagUncommon TFlag = 1 << 0

	// TFlagExtraStar means the name in the str field has an
	// extraneous '*' prefix. This is because for most types T in
	// a program, the type *T also exists and reusing the str data
	// saves binary size.
	TFlagExtraStar TFlag = 1 << 1

	// TFlagNamed means the type has a name.
	TFlagNamed TFlag = 1 << 2

	// TFlagRegularMemory means that equal and hash functions can treat
	// this type as a single region of t.size bytes.
	TFlagRegularMemory TFlag = 1 << 3

	// TFlagGCMaskOnDemand means that the GC pointer bitmask will be
	// computed on demand at runtime instead of being precomputed at
	// compile time. If this flag is set, the GCData field effectively
	// has type **byte instead of *byte. The runtime will store a
	// pointer to the GC pointer bitmask in *GCData.
	TFlagGCMaskOnDemand TFlag = 1 << 4

	// TFlagDirectIface means that a value of this type is stored directly
	// in the data field of an interface, instead of indirectly.
	// This flag is just a cached computation of Size_ == PtrBytes == goarch.PtrSize.
	TFlagDirectIface TFlag = 1 << 5

	// Leaving this breadcrumb behind for dlv. It should not be used, and no
	// Kind should be big enough to set this bit.
	KindDirectIface Kind = 1 << 5
)
const (
	TraceArgsLimit    = 10 // print no more than 10 args/components
	TraceArgsMaxDepth = 5  // no more than 5 layers of nesting

	// maxLen is a (conservative) upper bound of the byte stream length. For
	// each arg/component, it has no more than 2 bytes of data (size, offset),
	// and no more than one {, }, ... at each level (it cannot have both the
	// data and ... unless it is the last one, just be conservative). Plus 1
	// for _endSeq.
	TraceArgsMaxLen = (TraceArgsMaxDepth*3+2)*TraceArgsLimit + 1
)
const (
	TraceArgsEndSeq         = 0xff
	TraceArgsStartAgg       = 0xfe
	TraceArgsEndAgg         = 0xfd
	TraceArgsDotdotdot      = 0xfc
	TraceArgsOffsetTooLarge = 0xfb
	TraceArgsSpecial        = 0xf0 // above this are operators, below this are ordinary offsets
)
    Populate the data. The data is a stream of bytes, which contains the offsets
    and sizes of the non-aggregate arguments or non-aggregate fields/elements of
    aggregate-typed arguments, along with special "operators". Specifically,
      - for each non-aggregate arg/field/element, its offset from FP (1 byte)
        and size (1 byte)
      - special operators:
      - 0xff - end of sequence
      - 0xfe - print { (at the start of an aggregate-typed argument)
      - 0xfd - print } (at the end of an aggregate-typed argument)
      - 0xfc - print ... (more args/fields/elements)
      - 0xfb - print _ (offset too large)

const ArgsSizeUnknown = -0x80000000
    ArgsSizeUnknown is set in Func.argsize to mark all functions whose argument
    size is unknown (C vararg functions, and assembly code without an explicit
    specification). This value is generated by the compiler, assembler,
    or linker.

const FuncTabBucketSize = 256 * MINFUNC // size of bucket in the pc->func lookup table
const MINFUNC = 16 // minimum size for a function
const MaxPtrmaskBytes = 16
    MaxPtrmaskBytes is the maximum length of a GC ptrmask bitmap,
    which holds 1-bit entries describing where pointers are in a given type.
    Above this length, the runtime computes the GC ptrmask bitmap as needed.
    The information is used by the runtime to initialize the heap bitmap.

    There is a bit of overhead to computing the GC ptrmask bitmap the first
    time. On the other hand building GC ptrmask bitmaps for all types at compile
    time takes space in the binary for large types that have a lot of pointers,
    such as large array types. Using 16 means that types that keep their
    pointers in the first 512 (on 32-bit) or 1024 (on 64-bit) bytes are computed
    at compile time, and types with more pointers are computed at run time.
    This tradeoff sounds reasonable, and 16 was the cutoff back when we used GC
    programs, but this has not been benchmarked.

const ZeroValSize = 1024
    ZeroValSize is the size in bytes of runtime.zeroVal.


FUNCTIONS

func BoundsDecode(v int) (code BoundsErrorCode, signed, xIsReg, yIsReg bool, xVal, yVal int)
func BoundsEncode(code BoundsErrorCode, signed, xIsReg, yIsReg bool, xVal, yVal int) int
    Encode bounds failure information into an integer for PCDATA_PanicBounds.
    Register numbers must be in 0-15. Constants must be in 0-31.

func CommonSize(ptrSize int) int
    CommonSize returns sizeof(Type) for a compilation target with a given
    ptrSize

func Escape[T any](x T) T
    Escape forces any pointers in x to escape to the heap.

func EscapeNonString[T any](v T)
    EscapeNonString forces v to be on the heap, if v contains a non-string
    pointer.

    This is used in hash/maphash.Comparable. We cannot hash pointers to local
    variables on stack, as their addresses might change on stack growth.
    Strings are okay as the hash depends on only the content, not the pointer.

    This is essentially

        if hasNonStringPointers(T) { Escape(v) }

    Implemented as a compiler intrinsic.

func EscapeToResultNonString[T any](v T) T
    EscapeToResultNonString models a data flow edge from v to the result,
    if v contains a non-string pointer. If v contains only string pointers,
    it returns a copy of v, but is not modeled as a data flow edge from the
    escape analysis's perspective.

    This is used in unique.clone, to model the data flow edge on the value with
    strings excluded, because strings are cloned (by content).

    TODO: probably we should define this as a intrinsic and EscapeNonString
    could just be "heap = EscapeToResultNonString(v)". This way we can model an
    edge to the result but not necessarily heap.

func FuncPCABI0(f any) uintptr
    FuncPCABI0 returns the entry PC of the function f, which must be a direct
    reference of a function defined as ABI0. Otherwise it is a compile-time
    error.

    Implemented as a compile intrinsic.

func FuncPCABIInternal(f any) uintptr
    FuncPCABIInternal returns the entry PC of the function f. If f is a direct
    reference of a function, it must be defined as ABIInternal. Otherwise it is
    a compile-time error. If f is not a direct reference of a defined function,
    it assumes that f is a func value. Otherwise the behavior is undefined.

    Implemented as a compile intrinsic.

func ITabTypeOff(ptrSize int) int
    ITabTypeOff returns the offset of ITab.Type for a compilation target with a
    given ptrSize

func NoEscape(p unsafe.Pointer) unsafe.Pointer
    NoEscape hides the pointer p from escape analysis, preventing it from
    escaping to the heap. It compiles down to nothing.

    WARNING: This is very subtle to use correctly. The caller must ensure that
    it's truly safe for p to not escape to the heap by maintaining runtime
    pointer invariants (for example, that globals and the heap may not generally
    point into a stack).

func RTypeSize(kind Kind, ptrSize int) int
    RTypeSize returns sizeof(kindType) for a compilation target with a given
    ptrSize.

func StructFieldSize(ptrSize int) int
    StructFieldSize returns sizeof(StructField) for a compilation target with a
    given ptrSize

func TFlagOff(ptrSize int) int
    TFlagOff returns the offset of Type.TFlag for a compilation target with a
    given ptrSize

func UncommonSize() uint64
    UncommonSize returns sizeof(UncommonType). This currently does not depend on
    ptrSize. This exported function is in an internal package, so it may change
    to depend on ptrSize in the future.

func UseInterfaceSwitchCache(arch goarch.ArchFamilyType) bool

TYPES

type ArrayType struct {
	Type
	Elem  *Type // array element type
	Slice *Type // slice type
	Len   uintptr
}
    ArrayType represents a fixed array type.

type BoundsErrorCode uint8
    This type and constants are for encoding different kinds of bounds check
    failures.

const (
	BoundsIndex      BoundsErrorCode = iota // s[x], 0 <= x < len(s) failed
	BoundsSliceAlen                         // s[?:x], 0 <= x <= len(s) failed
	BoundsSliceAcap                         // s[?:x], 0 <= x <= cap(s) failed
	BoundsSliceB                            // s[x:y], 0 <= x <= y failed (but boundsSliceA didn't happen)
	BoundsSlice3Alen                        // s[?:?:x], 0 <= x <= len(s) failed
	BoundsSlice3Acap                        // s[?:?:x], 0 <= x <= cap(s) failed
	BoundsSlice3B                           // s[?:x:y], 0 <= x <= y failed (but boundsSlice3A didn't happen)
	BoundsSlice3C                           // s[x:y:?], 0 <= x <= y failed (but boundsSlice3A/B didn't happen)
	BoundsConvert                           // (*[x]T)(s), 0 <= x <= len(s) failed

)
type ChanDir int

const (
	RecvDir    ChanDir = 1 << iota         // <-chan
	SendDir                                // chan<-
	BothDir            = RecvDir | SendDir // chan
	InvalidDir ChanDir = 0
)
type ChanType struct {
	Type
	Elem *Type
	Dir  ChanDir
}
    ChanType represents a channel type

type CommonInterface struct {
	Data unsafe.Pointer
	// Has unexported fields.
}
    CommonInterface describes the layout of both EmptyInterface and
    NonEmptyInterface.

type EmptyInterface struct {
	Type *Type
	Data unsafe.Pointer
}
    EmptyInterface describes the layout of a "interface{}" or a "any." These are
    represented differently than non-empty interface, as the first word always
    points to an abi.Type.

type FuncFlag uint8
    A FuncFlag records bits about a function, passed to the runtime.

const (
	// FuncFlagTopFrame indicates a function that appears at the top of its stack.
	// The traceback routine stop at such a function and consider that a
	// successful, complete traversal of the stack.
	// Examples of TopFrame functions include goexit, which appears
	// at the top of a user goroutine stack, and mstart, which appears
	// at the top of a system goroutine stack.
	FuncFlagTopFrame FuncFlag = 1 << iota

	// FuncFlagSPWrite indicates a function that writes an arbitrary value to SP
	// (any write other than adding or subtracting a constant amount).
	// The traceback routines cannot encode such changes into the
	// pcsp tables, so the function traceback cannot safely unwind past
	// SPWrite functions. Stopping at an SPWrite function is considered
	// to be an incomplete unwinding of the stack. In certain contexts
	// (in particular garbage collector stack scans) that is a fatal error.
	FuncFlagSPWrite

	// FuncFlagAsm indicates that a function was implemented in assembly.
	FuncFlagAsm
)
type FuncID uint8
    A FuncID identifies particular functions that need to be treated specially
    by the runtime. Note that in some situations involving plugins, there may be
    multiple copies of a particular special runtime function.

const (
	FuncIDNormal FuncID = iota // not a special function
	FuncID_abort
	FuncID_asmcgocall
	FuncID_asyncPreempt
	FuncID_cgocallback
	FuncID_corostart
	FuncID_debugCallV2
	FuncID_gcBgMarkWorker
	FuncID_goexit
	FuncID_gogo
	FuncID_gopanic
	FuncID_handleAsyncEvent
	FuncID_mcall
	FuncID_morestack
	FuncID_mstart
	FuncID_panicwrap
	FuncID_rt0_go
	FuncID_runtime_main
	FuncID_runFinalizers
	FuncID_runCleanups
	FuncID_sigpanic
	FuncID_systemstack
	FuncID_systemstack_switch
	FuncIDWrapper // any autogenerated code (hash/eq algorithms, method wrappers, etc.)
)
type FuncType struct {
	Type
	InCount  uint16
	OutCount uint16 // top bit is set if last input parameter is ...
}
    FuncType represents a function type.

    A *Type for each in and out parameter is stored in an array that directly
    follows the funcType (and possibly its uncommonType). So a function type
    with one method, one input, and one output is:

        struct {
        	funcType
        	uncommonType
        	[2]*rtype    // [0] is in, [1] is out
        }

func (t *FuncType) In(i int) *Type

func (t *FuncType) InSlice() []*Type

func (t *FuncType) IsVariadic() bool

func (t *FuncType) NumIn() int

func (t *FuncType) NumOut() int

func (t *FuncType) Out(i int) *Type

func (t *FuncType) OutSlice() []*Type

type ITab struct {
	Inter *InterfaceType
	Type  *Type
	Hash  uint32     // copy of Type.Hash. Used for type switches.
	Fun   [1]uintptr // variable sized. fun[0]==0 means Type does not implement Inter.
}
    The first word of every non-empty interface type contains an *ITab.
    It records the underlying concrete type (Type), the interface type it is
    implementing (Inter), and some ancillary information.

    allocated in non-garbage-collected memory

func (it *ITab) Size() int
    Size returns the size of the itab in memory.

type Imethod struct {
	Name NameOff // name of method
	Typ  TypeOff // .(*FuncType) underneath
}
    Imethod represents a method on an interface type

type IntArgRegBitmap [(IntArgRegs + 7) / 8]uint8
    IntArgRegBitmap is a bitmap large enough to hold one bit per integer
    argument/return register.

func (b *IntArgRegBitmap) Get(i int) bool
    Get returns whether the i'th bit of the bitmap is set.

    nosplit because it's called in extremely sensitive contexts, like on the
    reflectcall return path.

func (b *IntArgRegBitmap) Set(i int)
    Set sets the i'th bit of the bitmap to 1.

type InterfaceSwitch struct {
	Cache  *InterfaceSwitchCache
	NCases int

	// Array of NCases elements.
	// Each case must be a non-empty interface type.
	Cases [1]*InterfaceType
}

type InterfaceSwitchCache struct {
	Mask    uintptr                      // mask for index. Must be a power of 2 minus 1
	Entries [1]InterfaceSwitchCacheEntry // Mask+1 entries total
}

type InterfaceSwitchCacheEntry struct {
	// type of source value (a *Type)
	Typ uintptr
	// case # to dispatch to
	Case int
	// itab to use for resulting case variable (a *runtime.itab)
	Itab uintptr
}

type InterfaceType struct {
	Type
	PkgPath Name      // import path
	Methods []Imethod // sorted by hash
}

func (t *InterfaceType) NumMethod() int
    NumMethod returns the number of interface methods in the type's method set.

type Kind uint8
    A Kind represents the specific kind of type that a Type represents. The zero
    Kind is not a valid kind.

const (
	Invalid Kind = iota
	Bool
	Int
	Int8
	Int16
	Int32
	Int64
	Uint
	Uint8
	Uint16
	Uint32
	Uint64
	Uintptr
	Float32
	Float64
	Complex64
	Complex128
	Array
	Chan
	Func
	Interface
	Map
	Pointer
	Slice
	String
	Struct
	UnsafePointer
)
func (k Kind) String() string
    String returns the name of k.

type MapType struct {
	Type
	Key   *Type
	Elem  *Type
	Group *Type // internal type representing a slot group
	// function for hashing keys (ptr to key, seed) -> hash
	Hasher    func(unsafe.Pointer, uintptr) uintptr
	GroupSize uintptr // == Group.Size_
	// These fields describe how to access keys and elems within a group.
	// The formulas key(i) = KeysOff + i*KeyStride and
	// elem(i) = ElemsOff + i*ElemStride work for both group layouts:
	//
	// With GOEXPERIMENT=mapsplitgroup (split arrays KKKKVVVV):
	//   KeysOff    = offset of keys array in group
	//   KeyStride  = size of a single key
	//   ElemsOff   = offset of elems array in group
	//   ElemStride = size of a single elem
	//
	// Without (interleaved slots KVKVKVKV):
	//   KeysOff    = offset of slots array in group
	//   KeyStride  = size of a key/elem slot (stride between keys)
	//   ElemsOff   = offset of first elem (slots offset + elem offset within slot)
	//   ElemStride = size of a key/elem slot (stride between elems)
	KeysOff    uintptr
	KeyStride  uintptr
	ElemsOff   uintptr
	ElemStride uintptr
	ElemOff    uintptr // GOEXPERIMENT=nomapsplitgroup only
	Flags      uint32
}

func (mt *MapType) HashMightPanic() bool

func (mt *MapType) IndirectElem() bool

func (mt *MapType) IndirectKey() bool

func (mt *MapType) NeedKeyUpdate() bool

type Method struct {
	Name NameOff // name of method
	Mtyp TypeOff // method type (without receiver)
	Ifn  TextOff // fn used in interface call (one-word receiver)
	Tfn  TextOff // fn used for normal method call
}
    Method on non-interface type

type Name struct {
	Bytes *byte
}

func NewName(n, tag string, exported, embedded bool) Name

func (n Name) Data(off int) *byte
    Data does pointer arithmetic on n's Bytes, and that arithmetic is
    asserted to be safe because the runtime made the call (other packages use
    DataChecked)

func (n Name) DataChecked(off int, whySafe string) *byte
    DataChecked does pointer arithmetic on n's Bytes, and that arithmetic
    is asserted to be safe for the reason in whySafe (which can appear in a
    backtrace, etc.)

func (n Name) HasTag() bool
    HasTag returns true iff there is tag data following this name

func (n Name) IsBlank() bool
    IsBlank indicates whether n is "_".

func (n Name) IsEmbedded() bool
    IsEmbedded returns true iff n is embedded (an anonymous field).

func (n Name) IsExported() bool
    IsExported returns "is n exported?"

func (n Name) Name() string
    Name returns the name of n, or empty if it does not actually have a name.

func (n Name) ReadVarint(off int) (int, int)
    ReadVarint parses a varint as encoded by encoding/binary. It returns the
    number of encoded bytes and the encoded value.

func (n Name) Tag() string
    Tag returns the tag string for n, or empty if there is none.

type NameOff int32
    NameOff is the offset to a name from moduledata.types. See resolveNameOff in
    runtime.

type NonEmptyInterface struct {
	ITab *ITab
	Data unsafe.Pointer
}
    NonEmptyInterface describes the layout of an interface that contains any
    methods.

type PCLnTabMagic uint32
    PCLnTabMagic is the version at the start of the PC/line table.
    This is the start of the .pclntab section, and is also runtime.pcHeader.
    The magic numbers are chosen such that reading the value with a different
    endianness does not result in the same value. That lets us the magic number
    to determine the endianness.

const (
	// Initial PCLnTabMagic value used in Go 1.2 through Go 1.15.
	Go12PCLnTabMagic PCLnTabMagic = 0xfffffffb
	// PCLnTabMagic value used in Go 1.16 through Go 1.17.
	// Several fields added to header (CL 241598).
	Go116PCLnTabMagic PCLnTabMagic = 0xfffffffa
	// PCLnTabMagic value used in Go 1.18 through Go 1.19.
	// Entry PC of func data changed from address to offset (CL 351463).
	Go118PCLnTabMagic PCLnTabMagic = 0xfffffff0
	// PCLnTabMagic value used in Go 1.20 and later.
	// A ":" was added to generated symbol names (#37762).
	Go120PCLnTabMagic PCLnTabMagic = 0xfffffff1

	// CurrentPCLnTabMagic is the value emitted by the current toolchain.
	// This is written by the linker to the pcHeader and read by the
	// runtime and debug/gosym (and external tools like Delve).
	//
	// Change this value when updating the pclntab version.
	// Changing this exported value is OK because is an
	// internal package.
	CurrentPCLnTabMagic = Go120PCLnTabMagic
)
type PtrType struct {
	Type
	Elem *Type // pointer element (pointed at) type
}

type RF_State int

type RegArgs struct {
	// Values in these slots should be precisely the bit-by-bit
	// representation of how they would appear in a register.
	//
	// This means that on big endian arches, integer values should
	// be in the top bits of the slot. Floats are usually just
	// directly represented, but some architectures treat narrow
	// width floating point values specially (e.g. they're promoted
	// first, or they need to be NaN-boxed).
	Ints   [IntArgRegs]uintptr  // untyped integer registers
	Floats [FloatArgRegs]uint64 // untyped float registers

	// Ptrs is a space that duplicates Ints but with pointer type,
	// used to make pointers passed or returned  in registers
	// visible to the GC by making the type unsafe.Pointer.
	Ptrs [IntArgRegs]unsafe.Pointer

	// ReturnIsPtr is a bitmap that indicates which registers
	// contain or will contain pointers on the return path from
	// a reflectcall. The i'th bit indicates whether the i'th
	// register contains or will contain a valid Go pointer.
	ReturnIsPtr IntArgRegBitmap
}
    RegArgs is a struct that has space for each argument and return value
    register on the current architecture.

    Assembly code knows the layout of the first two fields of RegArgs.

    RegArgs also contains additional space to hold pointers when it may not be
    safe to keep them only in the integer register space otherwise.

func (r *RegArgs) Dump()

func (r *RegArgs) IntRegArgAddr(reg int, argSize uintptr) unsafe.Pointer
    IntRegArgAddr returns a pointer inside of r.Ints[reg] that is appropriately
    offset for an argument of size argSize.

    argSize must be non-zero, fit in a register, and a power-of-two.

    This method is a helper for dealing with the endianness of different CPU
    architectures, since sub-word-sized arguments in big endian architectures
    need to be "aligned" to the upper edge of the register to be interpreted by
    the CPU correctly.

type SliceType struct {
	Type
	Elem *Type // slice element type
}

type StructField struct {
	Name   Name    // name is always non-empty
	Typ    *Type   // type of field
	Offset uintptr // byte offset of field
}

func (f *StructField) Embedded() bool

type StructType struct {
	Type
	PkgPath Name
	Fields  []StructField
}

type TFlag uint8
    TFlag is used by a Type to signal what extra type information is available
    in the memory directly following the Type value.

type TextOff int32
    TextOff is an offset from the top of a text section. See (rtype).textOff in
    runtime.

type Type struct {
	Size_       uintptr
	PtrBytes    uintptr // number of (prefix) bytes in the type that can contain pointers
	Hash        uint32  // hash of type; avoids computation in hash tables
	TFlag       TFlag   // extra type information flags
	Align_      uint8   // alignment of variable with this type
	FieldAlign_ uint8   // alignment of struct field with this type
	Kind_       Kind    // what kind of type this is (string, int, ...)
	// function for comparing objects of this type
	// (ptr to object A, ptr to object B) -> ==?
	Equal func(unsafe.Pointer, unsafe.Pointer) bool
	// GCData stores the GC type data for the garbage collector.
	// Normally, GCData points to a bitmask that describes the
	// ptr/nonptr fields of the type. The bitmask will have at
	// least PtrBytes/ptrSize bits.
	// If the TFlagGCMaskOnDemand bit is set, GCData is instead a
	// **byte and the pointer to the bitmask is one dereference away.
	// The runtime will build the bitmask if needed.
	// (See runtime/type.go:getGCMask.)
	// Note: multiple types may have the same value of GCData,
	// including when TFlagGCMaskOnDemand is set. The types will, of course,
	// have the same pointer layout (but not necessarily the same size).
	GCData    *byte
	Str       NameOff // string form
	PtrToThis TypeOff // type for pointer to this type, may be zero
}
    Type is the runtime representation of a Go type.

    Be careful about accessing this type at build time, as the version of this
    type in the compiler/linker may not have the same layout as the version in
    the target binary, due to pointer width differences and any experiments.
    Use cmd/compile/internal/rttype or the functions in compiletype.go to access
    this type instead. (TODO: this admonition applies to every type in this
    package. Put it in some shared location?)

func TypeFor[T any]() *Type
    TypeFor returns the abi.Type for a type parameter.

func TypeOf(a any) *Type
    TypeOf returns the abi.Type of some value.

func (t *Type) Align() int
    Align returns the alignment of data with type t.

func (t *Type) ArrayType() *ArrayType
    ArrayType returns t cast to a *ArrayType, or nil if its tag does not match.

func (t *Type) ChanDir() ChanDir
    ChanDir returns the direction of t if t is a channel type, otherwise
    InvalidDir (0).

func (t *Type) ChanType() *ChanType
    ChanType returns t cast to a *ChanType, or nil if its tag does not match.

func (t *Type) Common() *Type

func (t *Type) DescriptorSize() int
    DescriptorSize returns the contiguous size taken in memory by the type
    descriptor. This is the size of the Type struct, plus other fields used
    by some type kinds, plus the UncommonType struct if present, plus other
    optional information. This is just the size of the bytes that appear
    contiguously in memory. It does not include the size of things like type
    strings and field names that appear elsewhere.

    This code must match the data structures build by
    cmd/compile/internal/reflectdata/reflect.go:writeType.

func (t *Type) Elem() *Type
    Elem returns the element type for t if t is an array, channel, map, pointer,
    or slice, otherwise nil.

func (t *Type) ExportedMethods() []Method

func (t *Type) FieldAlign() int

func (t *Type) FuncType() *FuncType
    FuncType returns t cast to a *FuncType, or nil if its tag does not match.

func (t *Type) GcSlice(begin, end uintptr) []byte

func (t *Type) HasName() bool

func (t *Type) InterfaceType() *InterfaceType
    InterfaceType returns t cast to a *InterfaceType, or nil if its tag does not
    match.

func (t *Type) IsDirectIface() bool
    IsDirectIface reports whether t is stored directly in an interface value.

func (t *Type) Key() *Type

func (t *Type) Kind() Kind

func (t *Type) Len() int
    Len returns the length of t if t is an array type, otherwise 0

func (t *Type) MapType() *MapType
    MapType returns t cast to a *MapType, or nil if its tag does not match.

func (t *Type) NumMethod() int

func (t *Type) PointerType() *PtrType
    PointerType returns t cast to a *PtrType, or nil if its tag does not match.

func (t *Type) Pointers() bool
    Pointers reports whether t contains pointers.

func (t *Type) Size() uintptr
    Size returns the size of data with type t.

func (t *Type) SliceType() *SliceType
    SliceType returns t cast to a *SliceType, or nil if its tag does not match.

func (t *Type) StructType() *StructType
    StructType returns t cast to a *StructType, or nil if its tag does not
    match.

func (t *Type) Uncommon() *UncommonType
    Uncommon returns a pointer to T's "uncommon" data if there is any, otherwise
    nil

type TypeAssert struct {
	Cache   *TypeAssertCache
	Inter   *InterfaceType
	CanFail bool
}

type TypeAssertCache struct {
	Mask    uintptr
	Entries [1]TypeAssertCacheEntry
}

type TypeAssertCacheEntry struct {
	// type of source value (a *runtime._type)
	Typ uintptr
	// itab to use for result (a *runtime.itab)
	// nil if CanFail is set and conversion would fail.
	Itab uintptr
}

type TypeOff int32
    TypeOff is the offset to a type from moduledata.types. See resolveTypeOff in
    runtime.

type UncommonType struct {
	PkgPath NameOff // import path; empty for built-in types like int, string
	Mcount  uint16  // number of methods
	Xcount  uint16  // number of exported methods
	Moff    uint32  // offset from this uncommontype to [mcount]Method
	// Has unexported fields.
}
    UncommonType is present only for defined types or types with methods
    (if T is a defined type, the uncommonTypes for T and *T have methods).
    Using a pointer to this struct reduces the overall size required to describe
    a non-defined type with no methods.

func (t *UncommonType) ExportedMethods() []Method

func (t *UncommonType) Methods() []Method
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
