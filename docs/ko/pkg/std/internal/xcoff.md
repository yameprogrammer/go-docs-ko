# package internal/xcoff

- 원문: <https://pkg.go.dev/internal/xcoff>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package xcoff implements access to XCOFF (Extended Common Object File Format) files.

## 원문 요약

Package xcoff implements access to XCOFF (Extended Common Object File Format) files.

## API 상세 (go doc -all)

~~~text
package xcoff // import "internal/xcoff"

Package xcoff implements access to XCOFF (Extended Common Object File Format)
files.

CONSTANTS

const (
	SAIAMAG   = 0x8
	AIAFMAG   = "`\n"
	AIAMAG    = "<aiaff>\n"
	AIAMAGBIG = "<bigaf>\n"

	// Sizeof
	FL_HSZ_BIG = 0x80
	AR_HSZ_BIG = 0x70
)
const (
	FILHSZ_32 = 20
	FILHSZ_64 = 24
)
const (
	U802TOCMAGIC = 0737 // AIX 32-bit XCOFF
	U64_TOCMAGIC = 0767 // AIX 64-bit XCOFF
)
const (
	F_RELFLG    = 0x0001
	F_EXEC      = 0x0002
	F_LNNO      = 0x0004
	F_FDPR_PROF = 0x0010
	F_FDPR_OPTI = 0x0020
	F_DSA       = 0x0040
	F_VARPG     = 0x0100
	F_DYNLOAD   = 0x1000
	F_SHROBJ    = 0x2000
	F_LOADONLY  = 0x4000
)
    Flags that describe the type of the object file.

const (
	STYP_DWARF  = 0x0010
	STYP_TEXT   = 0x0020
	STYP_DATA   = 0x0040
	STYP_BSS    = 0x0080
	STYP_EXCEPT = 0x0100
	STYP_INFO   = 0x0200
	STYP_TDATA  = 0x0400
	STYP_TBSS   = 0x0800
	STYP_LOADER = 0x1000
	STYP_DEBUG  = 0x2000
	STYP_TYPCHK = 0x4000
	STYP_OVRFLO = 0x8000
)
    Flags defining the section type.

const (
	SSUBTYP_DWINFO  = 0x10000 // DWARF info section
	SSUBTYP_DWLINE  = 0x20000 // DWARF line-number section
	SSUBTYP_DWPBNMS = 0x30000 // DWARF public names section
	SSUBTYP_DWPBTYP = 0x40000 // DWARF public types section
	SSUBTYP_DWARNGE = 0x50000 // DWARF aranges section
	SSUBTYP_DWABREV = 0x60000 // DWARF abbreviation section
	SSUBTYP_DWSTR   = 0x70000 // DWARF strings section
	SSUBTYP_DWRNGES = 0x80000 // DWARF ranges section
	SSUBTYP_DWLOC   = 0x90000 // DWARF location lists section
	SSUBTYP_DWFRAME = 0xA0000 // DWARF frames section
	SSUBTYP_DWMAC   = 0xB0000 // DWARF macros section
)
const (
	// Nscnum
	N_DEBUG = -2
	N_ABS   = -1
	N_UNDEF = 0

	//Ntype
	SYM_V_INTERNAL  = 0x1000
	SYM_V_HIDDEN    = 0x2000
	SYM_V_PROTECTED = 0x3000
	SYM_V_EXPORTED  = 0x4000
	SYM_TYPE_FUNC   = 0x0020 // is function
)
const (
	C_NULL    = 0   // Symbol table entry marked for deletion
	C_EXT     = 2   // External symbol
	C_STAT    = 3   // Static symbol
	C_BLOCK   = 100 // Beginning or end of inner block
	C_FCN     = 101 // Beginning or end of function
	C_FILE    = 103 // Source file name and compiler information
	C_HIDEXT  = 107 // Unnamed external symbol
	C_BINCL   = 108 // Beginning of include file
	C_EINCL   = 109 // End of include file
	C_WEAKEXT = 111 // Weak external symbol
	C_DWARF   = 112 // DWARF symbol
	C_GSYM    = 128 // Global variable
	C_LSYM    = 129 // Automatic variable allocated on stack
	C_PSYM    = 130 // Argument to subroutine allocated on stack
	C_RSYM    = 131 // Register variable
	C_RPSYM   = 132 // Argument to function or procedure stored in register
	C_STSYM   = 133 // Statically allocated symbol
	C_BCOMM   = 135 // Beginning of common block
	C_ECOML   = 136 // Local member of common block
	C_ECOMM   = 137 // End of common block
	C_DECL    = 140 // Declaration of object
	C_ENTRY   = 141 // Alternate entry
	C_FUN     = 142 // Function or procedure
	C_BSTAT   = 143 // Beginning of static block
	C_ESTAT   = 144 // End of static block
	C_GTLS    = 145 // Global thread-local variable
	C_STTLS   = 146 // Static thread-local variable
)
    Storage Class.

const (
	XTY_ER = 0 // External reference
	XTY_SD = 1 // Section definition
	XTY_LD = 2 // Label definition
	XTY_CM = 3 // Common csect definition
)
    Symbol type field.

const (
	XFT_FN = 0   // Source File Name
	XFT_CT = 1   // Compile Time Stamp
	XFT_CV = 2   // Compiler Version Number
	XFT_CD = 128 // Compiler Defined Information
)
    Defines for File auxiliary definitions: x_ftype field of x_file

const (
	XMC_PR     = 0  // Program code
	XMC_RO     = 1  // Read-only constant
	XMC_DB     = 2  // Debug dictionary table
	XMC_TC     = 3  // TOC entry
	XMC_UA     = 4  // Unclassified
	XMC_RW     = 5  // Read/Write data
	XMC_GL     = 6  // Global linkage
	XMC_XO     = 7  // Extended operation
	XMC_SV     = 8  // 32-bit supervisor call descriptor
	XMC_BS     = 9  // BSS class
	XMC_DS     = 10 // Function descriptor
	XMC_UC     = 11 // Unnamed FORTRAN common
	XMC_TC0    = 15 // TOC anchor
	XMC_TD     = 16 // Scalar data entry in the TOC
	XMC_SV64   = 17 // 64-bit supervisor call descriptor
	XMC_SV3264 = 18 // Supervisor call descriptor for both 32-bit and 64-bit
	XMC_TL     = 20 // Read/Write thread-local data
	XMC_UL     = 21 // Read/Write thread-local data (.tbss)
	XMC_TE     = 22 // TOC entry
)
    Storage-mapping class.

const (
	LDHDRSZ_32 = 32
	LDHDRSZ_64 = 56
)
const (
	R_POS = 0x00 // A(sym) Positive Relocation
	R_NEG = 0x01 // -A(sym) Negative Relocation
	R_REL = 0x02 // A(sym-*) Relative to self
	R_TOC = 0x03 // A(sym-TOC) Relative to TOC
	R_TRL = 0x12 // A(sym-TOC) TOC Relative indirect load.

	R_TRLA = 0x13 // A(sym-TOC) TOC Rel load address. modifiable inst
	R_GL   = 0x05 // A(external TOC of sym) Global Linkage
	R_TCL  = 0x06 // A(local TOC of sym) Local object TOC address
	R_RL   = 0x0C // A(sym) Pos indirect load. modifiable instruction
	R_RLA  = 0x0D // A(sym) Pos Load Address. modifiable instruction
	R_REF  = 0x0F // AL0(sym) Non relocating ref. No garbage collect
	R_BA   = 0x08 // A(sym) Branch absolute. Cannot modify instruction
	R_RBA  = 0x18 // A(sym) Branch absolute. modifiable instruction
	R_BR   = 0x0A // A(sym-*) Branch rel to self. non modifiable
	R_RBR  = 0x1A // A(sym-*) Branch rel to self. modifiable instr

	R_TLS    = 0x20 // General-dynamic reference to TLS symbol
	R_TLS_IE = 0x21 // Initial-exec reference to TLS symbol
	R_TLS_LD = 0x22 // Local-dynamic reference to TLS symbol
	R_TLS_LE = 0x23 // Local-exec reference to TLS symbol
	R_TLSM   = 0x24 // Module reference to TLS symbol
	R_TLSML  = 0x25 // Module reference to local (own) module

	R_TOCU = 0x30 // Relative to TOC - high order bits
	R_TOCL = 0x31 // Relative to TOC - low order bits
)
const SYMESZ = 18

TYPES

type Archive struct {
	ArchiveHeader
	Members []*Member

	// Has unexported fields.
}
    Archive represents an open AIX big archive.

func NewArchive(r io.ReaderAt) (*Archive, error)
    NewArchive creates a new Archive for accessing an AIX big archive in an
    underlying reader.

func OpenArchive(name string) (*Archive, error)
    OpenArchive opens the named archive using os.Open and prepares it for use as
    an AIX big archive.

func (a *Archive) Close() error
    Close closes the Archive. If the Archive was created using NewArchive
    directly instead of OpenArchive, Close has no effect.

func (arch *Archive) GetFile(name string) (*File, error)
    GetFile returns the XCOFF file defined by member name. FIXME: This doesn't
    work if an archive has two members with the same name which can occur if an
    archive has both 32-bits and 64-bits files.

type ArchiveHeader struct {
	// Has unexported fields.
}
    ArchiveHeader holds information about a big archive file header

type AuxCSect32 struct {
	Xscnlen   uint32 // Length or symbol table index
	Xparmhash uint32 // Offset of parameter type-check string
	Xsnhash   uint16 // .typchk section number
	Xsmtyp    uint8  // Symbol alignment and type
	Xsmclas   uint8  // Storage-mapping class
	Xstab     uint32 // Reserved
	Xsnstab   uint16 // Reserved
}
    csect Auxiliary Entry.

type AuxCSect64 struct {
	Xscnlenlo uint32 // Lower 4 bytes of length or symbol table index
	Xparmhash uint32 // Offset of parameter type-check string
	Xsnhash   uint16 // .typchk section number
	Xsmtyp    uint8  // Symbol alignment and type
	Xsmclas   uint8  // Storage-mapping class
	Xscnlenhi uint32 // Upper 4 bytes of length or symbol table index
	Xpad      uint8  // Unused
	Xauxtype  uint8  // Type of auxiliary entry
}

type AuxFcn32 struct {
	Xexptr   uint32 // File offset to exception table entry
	Xfsize   uint32 // Size of function in bytes
	Xlnnoptr uint32 // File pointer to line number
	Xendndx  uint32 // Symbol table index of next entry
	Xpad     uint16 // Unused
}
    Function Auxiliary Entry

type AuxFcn64 struct {
	Xlnnoptr uint64 // File pointer to line number
	Xfsize   uint32 // Size of function in bytes
	Xendndx  uint32 // Symbol table index of next entry
	Xpad     uint8  // Unused
	Xauxtype uint8  // Type of auxiliary entry
}

type AuxFile64 struct {
	Xfname   [8]byte // Name or offset inside string table
	Xftype   uint8   // Source file string type
	Xauxtype uint8   // Type of auxiliary entry
}
    File Auxiliary Entry

type AuxSect64 struct {
	Xscnlen uint64 // section length
	Xnreloc uint64 // Num RLDs

	Xauxtype uint8 // Type of auxiliary entry
	// Has unexported fields.
}

type AuxiliaryCSect struct {
	Length              int64
	StorageMappingClass int
	SymbolType          int
}
    AuxiliaryCSect holds information about an XCOFF symbol in an AUX_CSECT
    entry.

type AuxiliaryFcn struct {
	Size int64
}
    AuxiliaryFcn holds information about an XCOFF symbol in an AUX_FCN entry.

type File struct {
	FileHeader
	Sections     []*Section
	Symbols      []*Symbol
	StringTable  []byte
	LibraryPaths []string

	// Has unexported fields.
}
    A File represents an open XCOFF file.

func NewFile(r io.ReaderAt) (*File, error)
    NewFile creates a new File for accessing an XCOFF binary in an underlying
    reader.

func Open(name string) (*File, error)
    Open opens the named file using os.Open and prepares it for use as an XCOFF
    binary.

func (f *File) CSect(name string) []byte
    CSect reads and returns the contents of a csect.

func (f *File) Close() error
    Close closes the File. If the File was created using NewFile directly
    instead of Open, Close has no effect.

func (f *File) DWARF() (*dwarf.Data, error)

func (f *File) ImportedLibraries() ([]string, error)
    ImportedLibraries returns the names of all libraries referred to by the
    binary f that are expected to be linked with the binary at dynamic link
    time.

func (f *File) ImportedSymbols() ([]ImportedSymbol, error)
    ImportedSymbols returns the names of all symbols referred to by the binary
    f that are expected to be satisfied by other libraries at dynamic load time.
    It does not return weak symbols.

func (f *File) Section(name string) *Section
    Section returns the first section with the given name, or nil if no such
    section exists. Xcoff have section's name limited to 8 bytes. Some sections
    like .gosymtab can be trunked but this method will still find them.

func (f *File) SectionByType(typ uint32) *Section
    SectionByType returns the first section in f with the given type, or nil if
    there is no such section.

type FileHeader struct {
	TargetMachine uint16
}
    FileHeader holds information about an XCOFF file header.

type FileHeader32 struct {
	Fmagic   uint16 // Target machine
	Fnscns   uint16 // Number of sections
	Ftimedat uint32 // Time and date of file creation
	Fsymptr  uint32 // Byte offset to symbol table start
	Fnsyms   uint32 // Number of entries in symbol table
	Fopthdr  uint16 // Number of bytes in optional header
	Fflags   uint16 // Flags
}
    File Header.

type FileHeader64 struct {
	Fmagic   uint16 // Target machine
	Fnscns   uint16 // Number of sections
	Ftimedat uint32 // Time and date of file creation
	Fsymptr  uint64 // Byte offset to symbol table start
	Fopthdr  uint16 // Number of bytes in optional header
	Fflags   uint16 // Flags
	Fnsyms   uint32 // Number of entries in symbol table
}

type ImportedSymbol struct {
	Name    string
	Library string
}
    ImportedSymbol holds information about an imported XCOFF symbol.

type LoaderHeader32 struct {
	Lversion uint32 // Loader section version number
	Lnsyms   uint32 // Number of symbol table entries
	Lnreloc  uint32 // Number of relocation table entries
	Listlen  uint32 // Length of import file ID string table
	Lnimpid  uint32 // Number of import file IDs
	Limpoff  uint32 // Offset to start of import file IDs
	Lstlen   uint32 // Length of string table
	Lstoff   uint32 // Offset to start of string table
}
    Loader Header.

type LoaderHeader64 struct {
	Lversion uint32 // Loader section version number
	Lnsyms   uint32 // Number of symbol table entries
	Lnreloc  uint32 // Number of relocation table entries
	Listlen  uint32 // Length of import file ID string table
	Lnimpid  uint32 // Number of import file IDs
	Lstlen   uint32 // Length of string table
	Limpoff  uint64 // Offset to start of import file IDs
	Lstoff   uint64 // Offset to start of string table
	Lsymoff  uint64 // Offset to start of symbol table
	Lrldoff  uint64 // Offset to start of relocation entries
}

type LoaderSymbol32 struct {
	Lname   [8]byte // Symbol name or byte offset into string table
	Lvalue  uint32  // Address field
	Lscnum  uint16  // Section number containing symbol
	Lsmtype uint8   // Symbol type, export, import flags
	Lsmclas uint8   // Symbol storage class
	Lifile  uint32  // Import file ID; ordinal of import file IDs
	Lparm   uint32  // Parameter type-check field
}
    Loader Symbol.

type LoaderSymbol64 struct {
	Lvalue  uint64 // Address field
	Loffset uint32 // Byte offset into string table of symbol name
	Lscnum  uint16 // Section number containing symbol
	Lsmtype uint8  // Symbol type, export, import flags
	Lsmclas uint8  // Symbol storage class
	Lifile  uint32 // Import file ID; ordinal of import file IDs
	Lparm   uint32 // Parameter type-check field
}

type Member struct {
	MemberHeader
	// Has unexported fields.
}
    Member represents a member of an AIX big archive.

type MemberHeader struct {
	Name string
	Size uint64
}
    MemberHeader holds information about a big archive member

type Reloc struct {
	VirtualAddress   uint64
	Symbol           *Symbol
	Signed           bool
	InstructionFixed bool
	Length           uint8
	Type             uint8
}

type Reloc32 struct {
	Rvaddr  uint32 // (virtual) address of reference
	Rsymndx uint32 // Index into symbol table
	Rsize   uint8  // Sign and reloc bit len
	Rtype   uint8  // Toc relocation type
}

type Reloc64 struct {
	Rvaddr  uint64 // (virtual) address of reference
	Rsymndx uint32 // Index into symbol table
	Rsize   uint8  // Sign and reloc bit len
	Rtype   uint8  // Toc relocation type
}

type Section struct {
	SectionHeader
	Relocs []Reloc
	io.ReaderAt
	// Has unexported fields.
}

func (s *Section) Data() ([]byte, error)
    Data reads and returns the contents of the XCOFF section s.

type SectionHeader struct {
	Name           string
	VirtualAddress uint64
	Size           uint64
	Type           uint32
	Relptr         uint64
	Nreloc         uint32
}
    SectionHeader holds information about an XCOFF section header.

type SectionHeader32 struct {
	Sname    [8]byte // Section name
	Spaddr   uint32  // Physical address
	Svaddr   uint32  // Virtual address
	Ssize    uint32  // Section size
	Sscnptr  uint32  // Offset in file to raw data for section
	Srelptr  uint32  // Offset in file to relocation entries for section
	Slnnoptr uint32  // Offset in file to line number entries for section
	Snreloc  uint16  // Number of relocation entries
	Snlnno   uint16  // Number of line number entries
	Sflags   uint32  // Flags to define the section type
}
    Section Header.

type SectionHeader64 struct {
	Sname    [8]byte // Section name
	Spaddr   uint64  // Physical address
	Svaddr   uint64  // Virtual address
	Ssize    uint64  // Section size
	Sscnptr  uint64  // Offset in file to raw data for section
	Srelptr  uint64  // Offset in file to relocation entries for section
	Slnnoptr uint64  // Offset in file to line number entries for section
	Snreloc  uint32  // Number of relocation entries
	Snlnno   uint32  // Number of line number entries
	Sflags   uint32  // Flags to define the section type
	Spad     uint32  // Needs to be 72 bytes long
}

type SymEnt32 struct {
	Nname   [8]byte // Symbol name
	Nvalue  uint32  // Symbol value
	Nscnum  uint16  // Section number of symbol
	Ntype   uint16  // Basic and derived type specification
	Nsclass uint8   // Storage class of symbol
	Nnumaux uint8   // Number of auxiliary entries
}
    Symbol Table Entry.

type SymEnt64 struct {
	Nvalue  uint64 // Symbol value
	Noffset uint32 // Offset of the name in string table or .debug section
	Nscnum  uint16 // Section number of symbol
	Ntype   uint16 // Basic and derived type specification
	Nsclass uint8  // Storage class of symbol
	Nnumaux uint8  // Number of auxiliary entries
}

type Symbol struct {
	Name          string
	Value         uint64
	SectionNumber int
	StorageClass  int
	AuxFcn        AuxiliaryFcn
	AuxCSect      AuxiliaryCSect
}
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
