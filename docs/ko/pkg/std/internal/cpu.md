# package internal/cpu

- 원문: <https://pkg.go.dev/internal/cpu>
- 분류: Go 표준 라이브러리

## 한국어 요약

`cpu` 패키지는 Go 표준 라이브러리에서 사용하는 프로세서 기능 탐지 기능을 구현합니다.

## 원문 요약

Package cpu implements processor feature detection used by the Go standard library.

## API 상세 (go doc -all)

~~~text
package cpu // import "internal/cpu"

Package cpu implements processor feature detection used by the Go standard
library.

CONSTANTS

const CacheLinePadSize = 64

VARIABLES

var ARM struct {
	_            CacheLinePad
	HasVFPv4     bool
	HasIDIVA     bool
	HasV7Atomics bool
	_            CacheLinePad
}
    The booleans in ARM contain the correspondingly named cpu feature bit.
    The struct is padded to avoid false sharing.

var ARM64 struct {
	_          CacheLinePad
	HasAES     bool
	HasPMULL   bool
	HasSHA1    bool
	HasSHA2    bool
	HasSHA512  bool
	HasSHA3    bool
	HasCRC32   bool
	HasATOMICS bool
	HasCPUID   bool
	HasDIT     bool
	HasSB      bool
	IsNeoverse bool
	_          CacheLinePad
}
    The booleans in ARM64 contain the correspondingly named cpu feature bit.
    The struct is padded to avoid false sharing.

var CacheLineSize uintptr = CacheLinePadSize
    CacheLineSize is the CPU's assumed cache line size. There is currently no
    runtime detection of the real cache line size so we use the constant per
    GOARCH CacheLinePadSize as an approximation.

var Loong64 struct {
	_              CacheLinePad
	HasLSX         bool // support 128-bit vector extension
	HasLASX        bool // support 256-bit vector extension
	HasCRC32       bool // support CRC instruction
	HasLAMCAS      bool // support AMCAS[_DB].{B/H/W/D}
	HasLAM_BH      bool // support AM{SWAP/ADD}[_DB].{B/H} instruction
	HasLLACQ_SCREL bool // support LLACQ.{W/D}, SCREL.{W/D} instruction
	HasSCQ         bool // support SC.Q instruction
	HasDBAR_HINTS  bool // supports finer-grained DBAR hints
	_              CacheLinePad
}
    The booleans in Loong64 contain the correspondingly named cpu feature bit.
    The struct is padded to avoid false sharing.

var MIPS64X struct {
	_      CacheLinePad
	HasMSA bool // MIPS SIMD architecture
	_      CacheLinePad
}
var PPC64 struct {
	_         CacheLinePad
	HasDARN   bool // Hardware random number generator (requires kernel enablement)
	HasSCV    bool // Syscall vectored (requires kernel enablement)
	IsPOWER8  bool // ISA v2.07 (POWER8)
	IsPOWER9  bool // ISA v3.00 (POWER9)
	IsPOWER10 bool // ISA v3.1  (POWER10)
	_         CacheLinePad
}
    For ppc64(le), it is safe to check only for ISA level starting on ISA v3.00,
    since there are no optional categories. There are some exceptions that
    also require kernel support to work (darn, scv), so there are feature bits
    for those as well. The minimum processor requirement is POWER8 (ISA 2.07).
    The struct is padded to avoid false sharing.

var RISCV64 struct {
	_                 CacheLinePad
	HasFastMisaligned bool // Fast misaligned accesses
	HasV              bool // Vector extension compatible with RVV 1.0
	HasZbb            bool // Basic bit-manipulation extension
	HasZbc            bool // Carryless multiplication extension
	HasZvbb           bool // Vector Basic Bit-manipulation
	HasZvbc           bool // Vector Carryless Multiplication
	HasZvkg           bool // Vector GCM/GMAC
	HasZvkned         bool // NIST Suite: Vector AES Block Cipher
	HasZvknha         bool // NIST Suite: Vector SHA-2 Secure Hash
	HasZvknhb         bool // NIST Suite: Vector SHA-2 Secure Hash
	HasZvksed         bool // ShangMi Suite: SM4 Block Cipher
	HasZvksh          bool // ShangMi Suite: SM3 Secure Hash
	HasZvkt           bool // Vector Data-Independent Execution Latency
	_                 CacheLinePad
}
    RISCV64 contains the supported CPU features and performance characteristics
    for riscv64 platforms. The booleans in RISCV64, with the exception of
    HasFastMisaligned, indicate the presence of RISC-V extensions. The struct is
    padded to avoid false sharing.

var S390X struct {
	_         CacheLinePad
	HasZARCH  bool // z architecture mode is active [mandatory]
	HasSTFLE  bool // store facility list extended [mandatory]
	HasLDISP  bool // long (20-bit) displacements [mandatory]
	HasEIMM   bool // 32-bit immediates [mandatory]
	HasDFP    bool // decimal floating point
	HasETF3EH bool // ETF-3 enhanced
	HasMSA    bool // message security assist (CPACF)
	HasAES    bool // KM-AES{128,192,256} functions
	HasAESCBC bool // KMC-AES{128,192,256} functions
	HasAESCTR bool // KMCTR-AES{128,192,256} functions
	HasAESGCM bool // KMA-GCM-AES{128,192,256} functions
	HasGHASH  bool // KIMD-GHASH function
	HasSHA1   bool // K{I,L}MD-SHA-1 functions
	HasSHA256 bool // K{I,L}MD-SHA-256 functions
	HasSHA512 bool // K{I,L}MD-SHA-512 functions
	HasSHA3   bool // K{I,L}MD-SHA3-{224,256,384,512} and K{I,L}MD-SHAKE-{128,256} functions
	HasVX     bool // vector facility. Note: the runtime sets this when it processes auxv records.
	HasVXE    bool // vector-enhancements facility 1
	HasKDSA   bool // elliptic curve functions
	HasECDSA  bool // NIST curves
	HasEDDSA  bool // Edwards curves
	_         CacheLinePad
}
var X86 struct {
	_                   CacheLinePad
	HasAES              bool
	HasADX              bool
	HasAVX              bool
	HasAVXVNNI          bool
	HasAVX2             bool
	HasAVX512           bool // Virtual feature: F+CD+BW+DQ+VL
	HasAVX512F          bool
	HasAVX512CD         bool
	HasAVX512BW         bool
	HasAVX512DQ         bool
	HasAVX512VL         bool
	HasAVX512GFNI       bool
	HasAVX512VAES       bool
	HasAVX512VNNI       bool
	HasAVX512VBMI       bool
	HasAVX512VBMI2      bool
	HasAVX512BITALG     bool
	HasAVX512VPOPCNTDQ  bool
	HasAVX512VPCLMULQDQ bool
	HasBMI1             bool
	HasBMI2             bool
	HasERMS             bool
	HasFSRM             bool
	HasFMA              bool
	HasGFNI             bool
	HasOSXSAVE          bool
	HasPCLMULQDQ        bool
	HasPOPCNT           bool
	HasRDTSCP           bool
	HasSHA              bool
	HasSSE3             bool
	HasSSSE3            bool
	HasSSE41            bool
	HasSSE42            bool
	HasVAES             bool
	HasVPCLMULQDQ       bool
	_                   CacheLinePad
}
    The booleans in X86 contain the correspondingly named cpuid feature bit.
    HasAVX and HasAVX2 are only set if the OS does support XMM and YMM registers
    in addition to the cpuid feature bit being set. The struct is padded to
    avoid false sharing.


FUNCTIONS

func DataCacheSizes() []uintptr
    DataCacheSizes returns the size of each data cache from lowest level in the
    hierarchy to highest.

    Unlike other parts of this package's public API, it is not safe to reference
    early in runtime initialization because it allocates. It's intended for
    testing only.

func Initialize(env string)
    Initialize examines the processor and sets the relevant variables above.
    This is called by the runtime package early in program initialization,
    before normal init functions are run. env is set by runtime if the OS
    supports cpu feature options in GODEBUG.

func Name() string
    Name returns the CPU name given by the vendor. If the CPU name can not be
    determined an empty string is returned.


TYPES

type CacheLinePad struct {
	// Has unexported fields.
}
    CacheLinePad is used to pad structs to avoid false sharing.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
