# package internal/runtime/syscall/windows

- 원문: <https://pkg.go.dev/internal/runtime/syscall/windows>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package windows // import "internal/runtime/syscall/windows"


CONSTANTS

const (
	CurrentProcess = ^uintptr(0) // -1 = current process
	CurrentThread  = ^uintptr(1) // -2 = current thread
)
    Pseudo handles.

const (
	PROT_NONE  = 0
	PROT_READ  = 1
	PROT_WRITE = 2
	PROT_EXEC  = 4
)
const (
	MAP_ANON    = 1
	MAP_PRIVATE = 2
)
const (
	SIGINT  = 0x2
	SIGTERM = 0xF
)
const (
	CTRL_C_EVENT        = 0x0
	CTRL_BREAK_EVENT    = 0x1
	CTRL_CLOSE_EVENT    = 0x2
	CTRL_LOGOFF_EVENT   = 0x5
	CTRL_SHUTDOWN_EVENT = 0x6
)
const (
	EXCEPTION_ACCESS_VIOLATION     = 0xc0000005
	EXCEPTION_IN_PAGE_ERROR        = 0xc0000006
	EXCEPTION_BREAKPOINT           = 0x80000003
	EXCEPTION_ILLEGAL_INSTRUCTION  = 0xc000001d
	EXCEPTION_FLT_DENORMAL_OPERAND = 0xc000008d
	EXCEPTION_FLT_DIVIDE_BY_ZERO   = 0xc000008e
	EXCEPTION_FLT_INEXACT_RESULT   = 0xc000008f
	EXCEPTION_FLT_OVERFLOW         = 0xc0000091
	EXCEPTION_FLT_UNDERFLOW        = 0xc0000093
	EXCEPTION_INT_DIVIDE_BY_ZERO   = 0xc0000094
	EXCEPTION_INT_OVERFLOW         = 0xc0000095
)
const (
	SEM_FAILCRITICALERRORS = 0x0001
	SEM_NOGPFAULTERRORBOX  = 0x0002
	SEM_NOOPENFILEERRORBOX = 0x8000
)
const (
	EXCEPTION_CONTINUE_EXECUTION  = -0x1
	EXCEPTION_CONTINUE_SEARCH     = 0x0
	EXCEPTION_CONTINUE_SEARCH_SEH = 0x1
)
const (
	SYNCHRONIZE        = 0x00100000
	TIMER_QUERY_STATE  = 0x0001
	TIMER_MODIFY_STATE = 0x0002
)
const (
	STATUS_SUCCESS   = 0x00000000
	STATUS_PENDING   = 0x00000103
	STATUS_CANCELLED = 0xC0000120
)
    https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-erref/596a1078-e883-4972-9bbc-49e60bebca55

const CONTEXT_CONTROL = 0x100001
const CREATE_WAITABLE_TIMER_HIGH_RESOLUTION = 0x00000002
const DUPLICATE_SAME_ACCESS = 0x2
const DWORD_MAX = 0xffffffff
const (
	ERROR_ACCESS_DENIED = 5
)
const FAIL_FAST_GENERATE_EXCEPTION_ADDRESS = 0x1
const INFINITE = 0xffffffff
const INVALID_HANDLE_VALUE = ^uintptr(0)
const THREAD_PRIORITY_HIGHEST = 0x2
const WAIT_TIMEOUT = 258
const WER_FAULT_REPORTING_NO_UI = 0x0020

FUNCTIONS

func AsmStdCallAddr() uintptr
    AsmStdCallAddr is the address of a function that accepts a pointer to
    StdCallInfo stored on the stack following the C calling convention,
    and calls the function using Windows' stdcall calling convention. Shouldn't
    be called directly from Go.

func StdCall(fn *StdCallInfo) uint32
    StdCall calls a function using Windows' stdcall convention. The calling
    thread's last-error code value is cleared before calling the function,
    and stored in the return value.


TYPES

type Context struct {
	P1Home       uint64
	P2Home       uint64
	P3Home       uint64
	P4Home       uint64
	P5Home       uint64
	P6Home       uint64
	ContextFlags uint32
	MxCsr        uint32
	SegCs        uint16
	SegDs        uint16
	SegEs        uint16
	SegFs        uint16
	SegGs        uint16
	SegSs        uint16
	EFlags       uint32
	DR0          uint64
	DR1          uint64
	DR2          uint64
	DR3          uint64
	DR6          uint64
	DR7          uint64
	Rax          uint64
	Rcx          uint64
	Rdx          uint64
	Rbx          uint64
	Rsp          uint64
	Rbp          uint64
	Rsi          uint64
	Rdi          uint64
	R8           uint64
	R9           uint64
	R10          uint64
	R11          uint64
	R12          uint64
	R13          uint64
	R14          uint64
	R15          uint64
	Rip          uint64

	VectorRegister       [26]M128
	VectorControl        uint64
	DebugControl         uint64
	LastBranchToRip      uint64
	LastBranchFromRip    uint64
	LastExceptionToRip   uint64
	LastExceptionFromRip uint64
	// Has unexported fields.
}

func (c *Context) LR() uintptr
    AMD64 does not have link register, so this returns 0.

func (c *Context) PC() uintptr

func (c *Context) PushCall(targetPC, resumePC uintptr)

func (c *Context) SP() uintptr

func (c *Context) SetFP(x uintptr)

func (c *Context) SetLR(x uintptr)

func (c *Context) SetPC(x uintptr)

func (c *Context) SetSP(x uintptr)

type DISPATCHER_CONTEXT struct {
	ControlPc        uint64
	ImageBase        uint64
	FunctionEntry    uintptr
	EstablisherFrame uint64
	TargetIp         uint64
	Context          *Context
	LanguageHandler  uintptr
	HandlerData      uintptr
}

func (c *DISPATCHER_CONTEXT) Ctx() *Context

type ExceptionPointers struct {
	Record  *ExceptionRecord
	Context *Context
}
    https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-exception_pointers

type ExceptionRecord struct {
	ExceptionCode        uint32
	ExceptionFlags       uint32
	ExceptionRecord      *ExceptionRecord
	ExceptionAddress     uintptr
	NumberParameters     uint32
	ExceptionInformation [15]uintptr
}
    https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-exception_record

type Handle uintptr

type M128 struct {
	Low  uint64
	High int64
}

type MemoryBasicInformation struct {
	BaseAddress       uintptr
	AllocationBase    uintptr
	AllocationProtect uint32
	PartitionId       uint16
	RegionSize        uintptr
	State             uint32
	Protect           uint32
	Type              uint32
}
    https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-memory_basic_information

type OSVERSIONINFOW struct {
	OSVersionInfoSize uint32
	MajorVersion      uint32
	MinorVersion      uint32
	BuildNumber       uint32
	PlatformID        uint32
	CSDVersion        [128]uint16
}
    https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/ns-wdm-_osversioninfow

type Overlapped struct {
	Internal     uintptr
	InternalHigh uintptr
	Offset       uint32
	OffsetHigh   uint32
	HEvent       Handle
}
    https://learn.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-overlapped

type StdCallInfo struct {
	Fn   uintptr
	N    uintptr // number of parameters
	Args uintptr // parameters
	R1   uintptr // return values
	R2   uintptr
}
    StdCallInfo is a structure used to pass parameters to the system call.

type SystemInfo struct {
	ProcessorArchitecture     uint16
	Reserved                  uint16
	PageSize                  uint32
	MinimumApplicationAddress *byte
	MaximumApplicationAddress *byte
	ActiveProcessorMask       uintptr
	NumberOfProcessors        uint32
	ProcessorType             uint32
	AllocationGranularity     uint32
	ProcessorLevel            uint16
	ProcessorRevision         uint16
}
    https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/ns-sysinfoapi-system_info
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
