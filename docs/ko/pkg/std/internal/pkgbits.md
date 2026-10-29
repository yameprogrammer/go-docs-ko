# package internal/pkgbits

- 원문: <https://pkg.go.dev/internal/pkgbits>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package pkgbits implements low-level coding abstractions for Unified IR's (UIR) binary export data format.

## 원문 요약

Package pkgbits implements low-level coding abstractions for Unified IR's (UIR) binary export data format.

## API 상세 (go doc -all)

~~~text
package pkgbits // import "internal/pkgbits"

Package pkgbits implements low-level coding abstractions for Unified IR's (UIR)
binary export data format.

At a low-level, the exported objects of a package are encoded as a byte
array. This array contains byte representations of primitive, potentially
variable-length values, such as integers, booleans, strings, and constants.

Additionally, the array may contain values which denote indices in the byte
array itself. These are termed "relocations" and allow for references.

The details of mapping high-level Go constructs to primitives are left to other
packages.

TYPES

type AbsElemIdx = uint32
    An AbsElemIdx, or absolute element index, is an index into the elements that
    is not relative to some other index.

type Code interface {
	// Marker returns the SyncMarker for the Code's dynamic type.
	Marker() SyncMarker

	// Value returns the Code's ordinal value.
	Value() int
}
    A Code is an enum value that can be encoded into bitstreams.

    Code types are preferable for enum types, because they allow Decoder to
    detect desyncs.

type CodeObj int
    A CodeObj distinguishes among go/types.Object encodings.

const (
	ObjAlias CodeObj = iota
	ObjConst
	ObjType
	ObjFunc
	ObjVar
	ObjStub
)
func (c CodeObj) Marker() SyncMarker

func (c CodeObj) Value() int

type CodeType int
    A CodeType distinguishes among go/types.Type encodings.

const (
	TypeBasic CodeType = iota
	TypeNamed
	TypePointer
	TypeSlice
	TypeArray
	TypeChan
	TypeMap
	TypeSignature
	TypeStruct
	TypeInterface
	TypeUnion
	TypeTypeParam
)
func (c CodeType) Marker() SyncMarker

func (c CodeType) Value() int

type CodeVal int
    A CodeVal distinguishes among go/constant.Value encodings.

const (
	ValBool CodeVal = iota
	ValString
	ValInt64
	ValBigInt
	ValBigRat
	ValBigFloat
)
func (c CodeVal) Marker() SyncMarker

func (c CodeVal) Value() int

type Decoder struct {
	Relocs []RefTableEntry
	Data   strings.Reader

	Idx RelElemIdx
	// Has unexported fields.
}
    A Decoder provides methods for decoding an individual element's bitstream
    data.

func (r *Decoder) Bool() bool
    Bool decodes and returns a bool value from the element bitstream.

func (r *Decoder) Code(mark SyncMarker) int
    Code decodes a Code value from the element bitstream and returns its
    ordinal value. It's the caller's responsibility to convert the result to an
    appropriate Code type.

    TODO(mdempsky): Ideally this method would have signature "Code[T Code] T"
    instead, but we don't allow generic methods and the compiler can't depend on
    generics yet anyway.

func (r *Decoder) Int() int
    Int decodes and returns an int value from the element bitstream.

func (r *Decoder) Int64() int64
    Int64 decodes and returns an int64 value from the element bitstream.

func (r *Decoder) Len() int
    Len decodes and returns a non-negative int value from the element bitstream.

func (r *Decoder) Reloc(k SectionKind) RelElemIdx
    Reloc decodes a relocation of expected section k from the element bitstream
    and returns an index to the referenced element.

func (r *Decoder) String() string
    String decodes and returns a string value from the element bitstream.

func (r *Decoder) Strings() []string
    Strings decodes and returns a variable-length slice of strings from the
    element bitstream.

func (r *Decoder) Sync(mWant SyncMarker)
    Sync decodes a sync marker from the element bitstream and asserts that it
    matches the expected marker.

    If EnableSync is false, then Sync is a no-op.

func (r *Decoder) Uint() uint
    Uint decodes and returns a uint value from the element bitstream.

func (r *Decoder) Uint64() uint64
    Uint64 decodes and returns a uint64 value from the element bitstream.

func (r *Decoder) Value() constant.Value
    Value decodes and returns a constant.Value from the element bitstream.

func (w *Decoder) Version() Version
    Version reports the version of the bitstream.

type Encoder struct {
	Relocs   []RefTableEntry
	RelocMap map[RefTableEntry]uint32
	Data     bytes.Buffer // accumulated element bitstream data

	Idx RelElemIdx // index within relocation section
	// Has unexported fields.
}
    An Encoder provides methods for encoding an individual element's bitstream
    data.

func (w *Encoder) Bool(b bool) bool
    Bool encodes and writes a bool value into the element bitstream, and then
    returns the bool value.

    For simple, 2-alternative encodings, the idiomatic way to call Bool is
    something like:

        if w.Bool(x != 0) {
        	// alternative #1
        } else {
        	// alternative #2
        }

    For multi-alternative encodings, use Code instead.

func (w *Encoder) Code(c Code)
    Code encodes and writes a Code value into the element bitstream.

func (w *Encoder) Flush() RelElemIdx
    Flush finalizes the element's bitstream and returns its RelElemIdx.

func (w *Encoder) Int(x int)
    Int encodes and writes an int value into the element bitstream.

func (w *Encoder) Int64(x int64)
    Int64 encodes and writes an int64 value into the element bitstream.

func (w *Encoder) Len(x int)
    Len encodes and writes a non-negative int value into the element bitstream.

func (w *Encoder) Reloc(k SectionKind, idx RelElemIdx)
    Reloc encodes and writes a relocation for the given (section, index) pair
    into the element bitstream.

    Note: Only the index is formally written into the element bitstream,
    so bitstream decoders must know from context which section an encoded
    relocation refers to.

func (w *Encoder) String(s string)
    String encodes and writes a string value into the element bitstream.

    Internally, strings are deduplicated by adding them to the strings section
    (if not already present), and then writing a relocation into the element
    bitstream.

func (w *Encoder) StringRef(idx RelElemIdx)
    StringRef writes a reference to the given index, which must be a previously
    encoded string value.

func (w *Encoder) Strings(ss []string)
    Strings encodes and writes a variable-length slice of strings into the
    element bitstream.

func (w *Encoder) Sync(m SyncMarker)

func (w *Encoder) Uint(x uint)
    Uint encodes and writes a uint value into the element bitstream.

func (w *Encoder) Uint64(x uint64)
    Uint64 encodes and writes a uint64 value into the element bitstream.

func (w *Encoder) Value(val constant.Value)
    Value encodes and writes a constant.Value into the element bitstream.

func (w *Encoder) Version() Version
    Version reports the version of the bitstream.

type Field int
    Field denotes a unit of data in the serialized unified IR bitstream.
    It is conceptually a like field in a structure.

    We only really need Fields when the data may or may not be present in a
    stream based on the Version of the bitstream.

    Unlike much of pkgbits, Fields are not serialized and can change values as
    needed.

const (
	// Flags in a uint32 in the header of a bitstream
	// that is used to indicate whether optional features are enabled.
	Flags Field = iota

	// Deprecated: HasInit was a bool indicating whether a package
	// has any init functions.
	HasInit

	// Deprecated: DerivedFuncInstance was a bool indicating
	// whether an object was a function instance.
	DerivedFuncInstance

	// ObjAlias has a list of TypeParamNames.
	AliasTypeParamNames

	// Deprecated: DerivedInfoNeeded was a bool indicating
	// whether a type was a derived type.
	DerivedInfoNeeded

	// Composite literals use a more compact format for element lists.
	CompactCompLiterals

	// Generic methods may appear as standalone function objects.
	GenericMethods

	// Method index is encoded to preserve relative order of
	// nongeneric and generic methods.
	PreserveMethodOrder
)
type Index int32
    An Index represents a bitstream element index *within* (i.e., relative to) a
    particular section.

type PkgDecoder struct {
	// Has unexported fields.
}
    A PkgDecoder provides methods for decoding a package's Unified IR export
    data.

func NewPkgDecoder(pkgPath, input string) PkgDecoder
    NewPkgDecoder returns a PkgDecoder initialized to read the Unified IR export
    data from input. pkgPath is the package path for the compilation unit that
    produced the export data.

func (pr *PkgDecoder) AbsIdx(k SectionKind, idx RelElemIdx) int
    AbsIdx returns the absolute index for the given (section, index) pair.

func (pr *PkgDecoder) DataIdx(k SectionKind, idx RelElemIdx) string
    DataIdx returns the raw element bitstream for the given (section, index)
    pair.

func (pr *PkgDecoder) Fingerprint() [8]byte
    Fingerprint returns the package fingerprint.

func (pr *PkgDecoder) NewDecoder(k SectionKind, idx RelElemIdx, marker SyncMarker) Decoder
    NewDecoder returns a Decoder for the given (section, index) pair, and
    decodes the given SyncMarker from the element bitstream.

func (pr *PkgDecoder) NewDecoderRaw(k SectionKind, idx RelElemIdx) Decoder
    NewDecoderRaw returns a Decoder for the given (section, index) pair.

    Most callers should use NewDecoder instead.

func (pr *PkgDecoder) NumElems(k SectionKind) int
    NumElems returns the number of elements in section k.

func (pr *PkgDecoder) PeekObj(idx RelElemIdx) (string, string, CodeObj)
    PeekObj returns the package path, object name, and CodeObj for the specified
    object index.

func (pr *PkgDecoder) PeekPkgPath(idx RelElemIdx) string
    PeekPkgPath returns the package path for the specified package index.

func (pr *PkgDecoder) PkgPath() string
    PkgPath returns the package path for the package

    TODO(mdempsky): Remove; unneeded since CL 391014.

func (pr *PkgDecoder) RetireDecoder(d *Decoder)

func (pr *PkgDecoder) StringIdx(idx RelElemIdx) string
    StringIdx returns the string value for the given string index.

func (pr *PkgDecoder) SyncMarkers() bool
    SyncMarkers reports whether pr uses sync markers.

func (pr *PkgDecoder) TempDecoder(k SectionKind, idx RelElemIdx, marker SyncMarker) Decoder
    TempDecoder returns a Decoder for the given (section, index) pair,
    and decodes the given SyncMarker from the element bitstream. If possible
    the Decoder should be RetireDecoder'd when it is no longer needed, this will
    avoid heap allocations.

func (pr *PkgDecoder) TempDecoderRaw(k SectionKind, idx RelElemIdx) Decoder

func (pr *PkgDecoder) TotalElems() int
    TotalElems returns the total number of elements across all sections.

type PkgEncoder struct {
	// Has unexported fields.
}
    A PkgEncoder provides methods for encoding a package's Unified IR export
    data.

func NewPkgEncoder(version Version, syncFrames int) PkgEncoder
    NewPkgEncoder returns an initialized PkgEncoder.

    syncFrames is the number of caller frames that should be serialized at
    Sync points. Serializing additional frames results in larger export data
    files, but can help diagnosing desync errors in higher-level Unified IR
    reader/writer code. If syncFrames is negative, then sync markers are omitted
    entirely.

func (pw *PkgEncoder) DumpTo(out0 io.Writer) (fingerprint [8]byte)
    DumpTo writes the package's encoded data to out0 and returns the package
    fingerprint.

func (pw *PkgEncoder) NewEncoder(k SectionKind, marker SyncMarker) *Encoder
    NewEncoder returns an Encoder for a new element within the given section,
    and encodes the given SyncMarker as the start of the element bitstream.

func (pw *PkgEncoder) NewEncoderRaw(k SectionKind) *Encoder
    NewEncoderRaw returns an Encoder for a new element within the given section.

    Most callers should use NewEncoder instead.

func (pw *PkgEncoder) StringIdx(s string) RelElemIdx
    StringIdx adds a string value to the strings section, if not already
    present, and returns its index.

func (pw *PkgEncoder) SyncMarkers() bool
    SyncMarkers reports whether pw uses sync markers.

type RefTableEntry struct {
	Kind SectionKind
	Idx  RelElemIdx
}
    A RefTableEntry is an entry in an element's reference table. All elements
    are preceded by a reference table which provides locations for referenced
    elements.

type RelElemIdx = Index
    TODO(markfreeman): Make this its own type. A RelElemIdx, or relative element
    index, is an index into the elements relative to some other index, such as
    the start of a section.

const (
	PublicRootIdx  RelElemIdx = 0
	PrivateRootIdx RelElemIdx = 1
)
    Reserved indices within the SectionMeta section.

type SectionKind int32 // TODO(markfreeman): Replace with uint8.
    A SectionKind indicates a section, as well as the ordering of sections
    within unified export data. Any object given a dedicated section can be
    referred to via a section / index pair (and thus dereferenced) in other
    sections.

const (
	SectionString SectionKind = iota
	SectionMeta
	SectionPosBase
	SectionPkg
	SectionName
	SectionType
	SectionObj
	SectionObjExt
	SectionObjDict
	SectionBody
)
type SyncMarker int
    SyncMarker is an enum type that represents markers that may be written to
    export data to ensure the reader and writer stay synchronized.

const (

	// Low-level coding markers.
	SyncEOF SyncMarker
	SyncBool
	SyncInt64
	SyncUint64
	SyncString
	SyncValue
	SyncVal
	SyncRelocs
	SyncReloc
	SyncUseReloc

	// Higher-level object and type markers.
	SyncPublic
	SyncPos
	SyncPosBase
	SyncObject
	SyncObject1
	SyncPkg
	SyncPkgDef
	SyncMethod
	SyncType
	SyncTypeIdx
	SyncTypeParamNames
	SyncSignature
	SyncParams
	SyncParam
	SyncCodeObj
	SyncSym
	SyncLocalIdent
	SyncSelector

	// Private markers (only known to cmd/compile).
	SyncPrivate

	SyncFuncExt
	SyncVarExt
	SyncTypeExt
	SyncPragma

	SyncExprList
	SyncExprs
	SyncExpr
	SyncExprType
	SyncAssign
	SyncOp
	SyncFuncLit
	SyncCompLit

	SyncDecl
	SyncFuncBody
	SyncOpenScope
	SyncCloseScope
	SyncCloseAnotherScope
	SyncDeclNames
	SyncDeclName

	SyncStmts
	SyncBlockStmt
	SyncIfStmt
	SyncForStmt
	SyncSwitchStmt
	SyncRangeStmt
	SyncCaseClause
	SyncCommClause
	SyncSelectStmt
	SyncDecls
	SyncLabeledStmt
	SyncUseObjLocal
	SyncAddLocal
	SyncLinkname
	SyncStmt1
	SyncStmtsEnd
	SyncLabel
	SyncOptLabel

	SyncMultiExpr
	SyncRType
	SyncConvRTTI
)
func (i SyncMarker) String() string

type Version uint32
    Version indicates a version of a unified IR bitstream. Each Version
    indicates the addition, removal, or change of new data in the bitstream.

    These are serialized to disk and the interpretation remains fixed.

const (
	// V0: initial prototype.
	//
	// All data that is not assigned a Field is in version V0
	// and has not been deprecated.
	V0 Version = iota

	// V1: adds the Flags uint32 word
	V1

	// V2: removes unused legacy fields and supports type parameters for aliases.
	// - remove the legacy "has init" bool from the public root
	// - remove obj's "derived func instance" bool
	// - add a TypeParamNames field to ObjAlias
	// - remove derived info "needed" bool
	V2

	// V3: introduces a more compact format for composite literal element lists
	// - negative lengths indicate that (some) elements may have keys
	// - positive lengths indicate that no element has a key
	// - a negative struct field index indicates an embedded field
	V3

	// V4: encodes generic methods as standalone function objects
	V4

	// V5: encodes the index of methods to preserve relative order
	// of nongeneric and generic methods (go.dev/issue/81188).
	V5
)
func (v Version) Has(f Field) bool
    Has reports whether field f is present in a bitstream at version v.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
