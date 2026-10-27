# package internal/syscall/windows

- 원문: <https://pkg.go.dev/internal/syscall/windows>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package windows // import "internal/syscall/windows"


CONSTANTS

const (
	O_NOFOLLOW_ANY = 0x200000000 // disallow symlinks anywhere in the path
	O_WRITE_ATTRS  = 0x800000000 // FILE_WRITE_ATTRIBUTES, used by Chmod
)
    Openat flags not supported by syscall.Open.

    These are invented values, use values in the 33-63 bit range to avoid
    overlap with flags and attributes supported by syscall.Open.

    When adding a new flag here, add an unexported version to the set of
    invented O_ values in syscall/types_windows.go to avoid overlap.

const (
	SYMLINKAT_DIRECTORY = SymlinkatFlags(1 << iota)
	SYMLINKAT_RELATIVE
)
const (
	SO_TYPE                                = 0x1008
	SO_PROTOCOL_INFOW                      = 0x2005
	SIO_TCP_INITIAL_RTO                    = syscall.IOC_IN | syscall.IOC_VENDOR | 17
	TCP_INITIAL_RTO_UNSPECIFIED_RTT        = ^uint16(0)
	TCP_INITIAL_RTO_NO_SYN_RETRANSMISSIONS = ^uint8(1)
)
const (
	FSCTL_SET_REPARSE_POINT    = 0x000900A4
	IO_REPARSE_TAG_MOUNT_POINT = 0xA0000003
	IO_REPARSE_TAG_DEDUP       = 0x80000013
	IO_REPARSE_TAG_AF_UNIX     = 0x80000023

	SYMLINK_FLAG_RELATIVE = 1
)
    Reparse tag values are taken from
    https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-fscc/c8e77b37-3909-4fe6-a4ea-2b9d423b1ee4

const (
	SecurityAnonymous      = 0
	SecurityIdentification = 1
	SecurityImpersonation  = 2
	SecurityDelegation     = 3
)
const (
	TOKEN_ADJUST_PRIVILEGES = 0x0020
	SE_PRIVILEGE_ENABLED    = 0x00000002
)
const (
	LG_INCLUDE_INDIRECT  = 0x1
	MAX_PREFERRED_LENGTH = 0xFFFFFFFF
)
const (
	NERR_UserNotFound syscall.Errno = 2221
	NERR_UserExists   syscall.Errno = 2224
)
const (
	SID_REVISION = 1
	// https://learn.microsoft.com/en-us/windows/win32/services/localsystem-account
	SECURITY_LOCAL_SYSTEM_RID = 18
	// https://learn.microsoft.com/en-us/windows/win32/services/localservice-account
	SECURITY_LOCAL_SERVICE_RID = 19
	// https://learn.microsoft.com/en-us/windows/win32/services/networkservice-account
	SECURITY_NETWORK_SERVICE_RID = 20
)
const (
	ERROR_INVALID_PARAMETER syscall.Errno = 87

	FILE_SUPPORTS_OBJECT_IDS      = 0x00010000
	FILE_SUPPORTS_OPEN_BY_FILE_ID = 0x01000000

	// symlink support for CreateSymbolicLink() starting with Windows 10 (1703, v10.0.14972)
	SYMBOLIC_LINK_FLAG_ALLOW_UNPRIVILEGED_CREATE = 0x2

	// FileInformationClass values
	FileBasicInfo                  = 0    // FILE_BASIC_INFO
	FileStandardInfo               = 1    // FILE_STANDARD_INFO
	FileNameInfo                   = 2    // FILE_NAME_INFO
	FileDispositionInfo            = 4    // FILE_DISPOSITION_INFO
	FileStreamInfo                 = 7    // FILE_STREAM_INFO
	FileCompressionInfo            = 8    // FILE_COMPRESSION_INFO
	FileAttributeTagInfo           = 9    // FILE_ATTRIBUTE_TAG_INFO
	FileIdBothDirectoryInfo        = 0xa  // FILE_ID_BOTH_DIR_INFO
	FileIdBothDirectoryRestartInfo = 0xb  // FILE_ID_BOTH_DIR_INFO
	FileRemoteProtocolInfo         = 0xd  // FILE_REMOTE_PROTOCOL_INFO
	FileFullDirectoryInfo          = 0xe  // FILE_FULL_DIR_INFO
	FileFullDirectoryRestartInfo   = 0xf  // FILE_FULL_DIR_INFO
	FileStorageInfo                = 0x10 // FILE_STORAGE_INFO
	FileAlignmentInfo              = 0x11 // FILE_ALIGNMENT_INFO
	FileIdInfo                     = 0x12 // FILE_ID_INFO
	FileIdExtdDirectoryInfo        = 0x13 // FILE_ID_EXTD_DIR_INFO
	FileIdExtdDirectoryRestartInfo = 0x14 // FILE_ID_EXTD_DIR_INFO
)
const (
	ERROR_INVALID_HANDLE         syscall.Errno = 6
	ERROR_BAD_LENGTH             syscall.Errno = 24
	ERROR_SHARING_VIOLATION      syscall.Errno = 32
	ERROR_LOCK_VIOLATION         syscall.Errno = 33
	ERROR_NOT_SUPPORTED          syscall.Errno = 50
	ERROR_CALL_NOT_IMPLEMENTED   syscall.Errno = 120
	ERROR_INVALID_NAME           syscall.Errno = 123
	ERROR_NEGATIVE_SEEK          syscall.Errno = 131
	ERROR_LOCK_FAILED            syscall.Errno = 167
	ERROR_IO_INCOMPLETE          syscall.Errno = 996
	ERROR_NO_TOKEN               syscall.Errno = 1008
	ERROR_NO_UNICODE_TRANSLATION syscall.Errno = 1113
	ERROR_CANT_ACCESS_FILE       syscall.Errno = 1920
)
const (
	GAA_FLAG_INCLUDE_PREFIX   = 0x00000010
	GAA_FLAG_INCLUDE_GATEWAYS = 0x0080
)
const (
	IF_TYPE_OTHER              = 1
	IF_TYPE_ETHERNET_CSMACD    = 6
	IF_TYPE_ISO88025_TOKENRING = 9
	IF_TYPE_PPP                = 23
	IF_TYPE_SOFTWARE_LOOPBACK  = 24
	IF_TYPE_ATM                = 37
	IF_TYPE_IEEE80211          = 71
	IF_TYPE_TUNNEL             = 131
	IF_TYPE_IEEE1394           = 144
)
const (
	IfOperStatusUp             = 1
	IfOperStatusDown           = 2
	IfOperStatusTesting        = 3
	IfOperStatusUnknown        = 4
	IfOperStatusDormant        = 5
	IfOperStatusNotPresent     = 6
	IfOperStatusLowerLayerDown = 7
)
const (
	// flags for CreateToolhelp32Snapshot
	TH32CS_SNAPMODULE   = 0x08
	TH32CS_SNAPMODULE32 = 0x10
)
const (
	WSA_FLAG_OVERLAPPED        = 0x01
	WSA_FLAG_NO_HANDLE_INHERIT = 0x80

	WSAEINVAL       syscall.Errno = 10022
	WSAEMSGSIZE     syscall.Errno = 10040
	WSAEAFNOSUPPORT syscall.Errno = 10047

	MSG_PEEK   = 0x2
	MSG_TRUNC  = 0x0100
	MSG_CTRUNC = 0x0200
)
const (
	ComputerNameNetBIOS                   = 0
	ComputerNameDnsHostname               = 1
	ComputerNameDnsDomain                 = 2
	ComputerNameDnsFullyQualified         = 3
	ComputerNamePhysicalNetBIOS           = 4
	ComputerNamePhysicalDnsHostname       = 5
	ComputerNamePhysicalDnsDomain         = 6
	ComputerNamePhysicalDnsFullyQualified = 7
	ComputerNameMax                       = 8

	MOVEFILE_REPLACE_EXISTING      = 0x1
	MOVEFILE_COPY_ALLOWED          = 0x2
	MOVEFILE_DELAY_UNTIL_REBOOT    = 0x4
	MOVEFILE_WRITE_THROUGH         = 0x8
	MOVEFILE_CREATE_HARDLINK       = 0x10
	MOVEFILE_FAIL_IF_NOT_TRACKABLE = 0x20
)
const (
	LOCKFILE_FAIL_IMMEDIATELY = 0x00000001
	LOCKFILE_EXCLUSIVE_LOCK   = 0x00000002
)
const (
	STYPE_DISKTREE  = 0x00
	STYPE_TEMPORARY = 0x40000000
)
    Constants from lmshare.h

const (
	FILE_NAME_NORMALIZED = 0x0
	FILE_NAME_OPENED     = 0x8

	VOLUME_NAME_DOS  = 0x0
	VOLUME_NAME_GUID = 0x1
	VOLUME_NAME_NONE = 0x4
	VOLUME_NAME_NT   = 0x2
)
const (
	SERVICE_RUNNING      = 4
	SERVICE_QUERY_STATUS = 4
)
const (
	PIPE_ACCESS_INBOUND  = 0x00000001
	PIPE_ACCESS_OUTBOUND = 0x00000002
	PIPE_ACCESS_DUPLEX   = 0x00000003

	PIPE_TYPE_BYTE    = 0x00000000
	PIPE_TYPE_MESSAGE = 0x00000004

	PIPE_READMODE_BYTE    = 0x00000000
	PIPE_READMODE_MESSAGE = 0x00000002
)
const (
	TCP_KEEPIDLE  = 0x03
	TCP_KEEPCNT   = 0x10
	TCP_KEEPINTVL = 0x11

	SIO_UDP_NETRESET = syscall.IOC_IN | syscall.IOC_VENDOR | 15
)
    Socket related.

const (
	FILE_READ_DATA        = 0x00000001
	FILE_READ_ATTRIBUTES  = 0x00000080
	FILE_READ_EA          = 0x00000008
	FILE_WRITE_DATA       = 0x00000002
	FILE_WRITE_ATTRIBUTES = 0x00000100
	FILE_WRITE_EA         = 0x00000010
	FILE_APPEND_DATA      = 0x00000004
	FILE_EXECUTE          = 0x00000020

	FILE_GENERIC_READ    = STANDARD_RIGHTS_READ | FILE_READ_DATA | FILE_READ_ATTRIBUTES | FILE_READ_EA | SYNCHRONIZE
	FILE_GENERIC_WRITE   = STANDARD_RIGHTS_WRITE | FILE_WRITE_DATA | FILE_WRITE_ATTRIBUTES | FILE_WRITE_EA | FILE_APPEND_DATA | SYNCHRONIZE
	FILE_GENERIC_EXECUTE = STANDARD_RIGHTS_EXECUTE | FILE_READ_ATTRIBUTES | FILE_EXECUTE | SYNCHRONIZE

	FILE_LIST_DIRECTORY = 0x00000001
	FILE_TRAVERSE       = 0x00000020

	FILE_SHARE_READ                      = 0x00000001
	FILE_SHARE_WRITE                     = 0x00000002
	FILE_SHARE_DELETE                    = 0x00000004
	FILE_ATTRIBUTE_READONLY              = 0x00000001
	FILE_ATTRIBUTE_HIDDEN                = 0x00000002
	FILE_ATTRIBUTE_SYSTEM                = 0x00000004
	FILE_ATTRIBUTE_DIRECTORY             = 0x00000010
	FILE_ATTRIBUTE_ARCHIVE               = 0x00000020
	FILE_ATTRIBUTE_DEVICE                = 0x00000040
	FILE_ATTRIBUTE_NORMAL                = 0x00000080
	FILE_ATTRIBUTE_TEMPORARY             = 0x00000100
	FILE_ATTRIBUTE_SPARSE_FILE           = 0x00000200
	FILE_ATTRIBUTE_REPARSE_POINT         = 0x00000400
	FILE_ATTRIBUTE_COMPRESSED            = 0x00000800
	FILE_ATTRIBUTE_OFFLINE               = 0x00001000
	FILE_ATTRIBUTE_NOT_CONTENT_INDEXED   = 0x00002000
	FILE_ATTRIBUTE_ENCRYPTED             = 0x00004000
	FILE_ATTRIBUTE_INTEGRITY_STREAM      = 0x00008000
	FILE_ATTRIBUTE_VIRTUAL               = 0x00010000
	FILE_ATTRIBUTE_NO_SCRUB_DATA         = 0x00020000
	FILE_ATTRIBUTE_RECALL_ON_OPEN        = 0x00040000
	FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS = 0x00400000

	INVALID_FILE_ATTRIBUTES = 0xffffffff
)
const (
	DELETE                   = 0x00010000
	READ_CONTROL             = 0x00020000
	WRITE_DAC                = 0x00040000
	WRITE_OWNER              = 0x00080000
	SYNCHRONIZE              = 0x00100000
	STANDARD_RIGHTS_REQUIRED = 0x000F0000
	STANDARD_RIGHTS_READ     = READ_CONTROL
	STANDARD_RIGHTS_WRITE    = READ_CONTROL
	STANDARD_RIGHTS_EXECUTE  = READ_CONTROL
	STANDARD_RIGHTS_ALL      = 0x001F0000
	SPECIFIC_RIGHTS_ALL      = 0x0000FFFF
	ACCESS_SYSTEM_SECURITY   = 0x01000000
	MAXIMUM_ALLOWED          = 0x02000000
	GENERIC_READ             = 0x80000000
	GENERIC_WRITE            = 0x40000000
	GENERIC_EXECUTE          = 0x20000000
	GENERIC_ALL              = 0x10000000
)
    Constants for type ACCESS_MASK

const (
	OBJ_INHERIT                       = 0x00000002
	OBJ_PERMANENT                     = 0x00000010
	OBJ_EXCLUSIVE                     = 0x00000020
	OBJ_CASE_INSENSITIVE              = 0x00000040
	OBJ_OPENIF                        = 0x00000080
	OBJ_OPENLINK                      = 0x00000100
	OBJ_KERNEL_HANDLE                 = 0x00000200
	OBJ_FORCE_ACCESS_CHECK            = 0x00000400
	OBJ_IGNORE_IMPERSONATED_DEVICEMAP = 0x00000800
	OBJ_DONT_REPARSE                  = 0x00001000
	OBJ_VALID_ATTRIBUTES              = 0x00001FF2
)
    Values for the Attributes member of OBJECT_ATTRIBUTES.

const (
	O_FILE_FLAG_OPEN_NO_RECALL     = 0x00100000
	O_FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
	O_FILE_FLAG_SESSION_AWARE      = 0x00800000
	O_FILE_FLAG_POSIX_SEMANTICS    = 0x01000000
	O_FILE_FLAG_BACKUP_SEMANTICS   = 0x02000000
	O_FILE_FLAG_DELETE_ON_CLOSE    = 0x04000000
	O_FILE_FLAG_SEQUENTIAL_SCAN    = 0x08000000
	O_FILE_FLAG_RANDOM_ACCESS      = 0x10000000
	O_FILE_FLAG_NO_BUFFERING       = 0x20000000
	O_FILE_FLAG_OVERLAPPED         = 0x40000000
	O_FILE_FLAG_WRITE_THROUGH      = 0x80000000
)
    File flags for os.OpenFile. The O_ prefix is used to indicate that these
    flags are specific to the OpenFile function.

const (
	// CreateDisposition flags for NtCreateFile and NtCreateNamedPipeFile.
	FILE_SUPERSEDE           = 0x00000000
	FILE_OPEN                = 0x00000001
	FILE_CREATE              = 0x00000002
	FILE_OPEN_IF             = 0x00000003
	FILE_OVERWRITE           = 0x00000004
	FILE_OVERWRITE_IF        = 0x00000005
	FILE_MAXIMUM_DISPOSITION = 0x00000005

	// CreateOptions flags for NtCreateFile and NtCreateNamedPipeFile.
	FILE_DIRECTORY_FILE            = 0x00000001
	FILE_WRITE_THROUGH             = 0x00000002
	FILE_SEQUENTIAL_ONLY           = 0x00000004
	FILE_NO_INTERMEDIATE_BUFFERING = 0x00000008
	FILE_SYNCHRONOUS_IO_ALERT      = 0x00000010
	FILE_SYNCHRONOUS_IO_NONALERT   = 0x00000020
	FILE_NON_DIRECTORY_FILE        = 0x00000040
	FILE_CREATE_TREE_CONNECTION    = 0x00000080
	FILE_COMPLETE_IF_OPLOCKED      = 0x00000100
	FILE_NO_EA_KNOWLEDGE           = 0x00000200
	FILE_OPEN_REMOTE_INSTANCE      = 0x00000400
	FILE_RANDOM_ACCESS             = 0x00000800
	FILE_DELETE_ON_CLOSE           = 0x00001000
	FILE_OPEN_BY_FILE_ID           = 0x00002000
	FILE_OPEN_FOR_BACKUP_INTENT    = 0x00004000
	FILE_NO_COMPRESSION            = 0x00008000
	FILE_OPEN_REQUIRING_OPLOCK     = 0x00010000
	FILE_DISALLOW_EXCLUSIVE        = 0x00020000
	FILE_SESSION_AWARE             = 0x00040000
	FILE_RESERVE_OPFILTER          = 0x00100000
	FILE_OPEN_REPARSE_POINT        = 0x00200000
	FILE_OPEN_NO_RECALL            = 0x00400000
	FILE_OPEN_FOR_FREE_SPACE_QUERY = 0x00800000
)
const (
	FILE_DISPOSITION_DO_NOT_DELETE             = 0x00000000
	FILE_DISPOSITION_DELETE                    = 0x00000001
	FILE_DISPOSITION_POSIX_SEMANTICS           = 0x00000002
	FILE_DISPOSITION_FORCE_IMAGE_SECTION_CHECK = 0x00000004
	FILE_DISPOSITION_ON_CLOSE                  = 0x00000008
	FILE_DISPOSITION_IGNORE_READONLY_ATTRIBUTE = 0x00000010
)
    https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntddk/ns-ntddk-_file_disposition_information_ex

const (
	FILE_RENAME_REPLACE_IF_EXISTS = 0x00000001
	FILE_RENAME_POSIX_SEMANTICS   = 0x00000002
)
    Flags for FILE_RENAME_INFORMATION_EX.

const (
	TRUSTEE_IS_SID              = 0x0
	TRUSTEE_IS_NAME             = 0x1
	TRUSTEE_BAD_FORM            = 0x2
	TRUSTEE_IS_OBJECTS_AND_SID  = 0x3
	TRUSTEE_IS_OBJECTS_AND_NAME = 0x4
)
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa379638.aspx

const (
	NOT_USED_ACCESS   = 0x0
	GRANT_ACCESS      = 0x1
	SET_ACCESS        = 0x2
	DENY_ACCESS       = 0x3
	REVOKE_ACCESS     = 0x4
	SET_AUDIT_SUCCESS = 0x5
	SET_AUDIT_FAILURE = 0x6
)
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa374899.aspx

const (
	NO_INHERITANCE                     = 0x0
	SUB_OBJECTS_ONLY_INHERIT           = 0x1
	SUB_CONTAINERS_ONLY_INHERIT        = 0x2
	SUB_CONTAINERS_AND_OBJECTS_INHERIT = 0x3
	INHERIT_NO_PROPAGATE               = 0x4
	INHERIT_ONLY                       = 0x8
)
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa446627.aspx

const (
	SE_UNKNOWN_OBJECT_TYPE     = 0x0
	SE_FILE_OBJECT             = 0x1
	SE_SERVICE                 = 0x2
	SE_PRINTER                 = 0x3
	SE_REGISTRY_KEY            = 0x4
	SE_LMSHARE                 = 0x5
	SE_KERNEL_OBJECT           = 0x6
	SE_WINDOW_OBJECT           = 0x7
	SE_DS_OBJECT               = 0x8
	SE_DS_OBJECT_ALL           = 0x9
	SE_PROVIDER_DEFINED_OBJECT = 0xa
	SE_WMIGUID_OBJECT          = 0xb
	SE_REGISTRY_WOW64_32KEY    = 0xc
	SE_REGISTRY_WOW64_64KEY    = 0xd
)
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa379593.aspx

const (
	OWNER_SECURITY_INFORMATION               = 0x00000001
	GROUP_SECURITY_INFORMATION               = 0x00000002
	DACL_SECURITY_INFORMATION                = 0x00000004
	SACL_SECURITY_INFORMATION                = 0x00000008
	LABEL_SECURITY_INFORMATION               = 0x00000010
	UNPROTECTED_SACL_SECURITY_INFORMATION    = 0x10000000
	UNPROTECTED_DACL_SECURITY_INFORMATION    = 0x20000000
	PROTECTED_SACL_SECURITY_INFORMATION      = 0x40000000
	PROTECTED_DACL_SECURITY_INFORMATION      = 0x80000000
	ATTRIBUTE_SECURITY_INFORMATION           = 0x00000020
	SCOPE_SECURITY_INFORMATION               = 0x00000040
	PROCESS_TRUST_LABEL_SECURITY_INFORMATION = 0x00000080
	BACKUP_SECURITY_INFORMATION              = 0x00010000
)
    https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-dtyp/23e75ca3-98fd-4396-84e5-86cd9d40d343

const (
	PF_ARM_64BIT_LOADSTORE_ATOMIC              = 25
	PF_ARM_DIVIDE_INSTRUCTION_AVAILABLE        = 24
	PF_ARM_EXTERNAL_CACHE_AVAILABLE            = 26
	PF_ARM_FMAC_INSTRUCTIONS_AVAILABLE         = 27
	PF_ARM_VFP_32_REGISTERS_AVAILABLE          = 18
	PF_3DNOW_INSTRUCTIONS_AVAILABLE            = 7
	PF_CHANNELS_ENABLED                        = 16
	PF_COMPARE_EXCHANGE_DOUBLE                 = 2
	PF_COMPARE_EXCHANGE128                     = 14
	PF_COMPARE64_EXCHANGE128                   = 15
	PF_FASTFAIL_AVAILABLE                      = 23
	PF_FLOATING_POINT_EMULATED                 = 1
	PF_FLOATING_POINT_PRECISION_ERRATA         = 0
	PF_MMX_INSTRUCTIONS_AVAILABLE              = 3
	PF_NX_ENABLED                              = 12
	PF_PAE_ENABLED                             = 9
	PF_RDTSC_INSTRUCTION_AVAILABLE             = 8
	PF_RDWRFSGSBASE_AVAILABLE                  = 22
	PF_SECOND_LEVEL_ADDRESS_TRANSLATION        = 20
	PF_SSE3_INSTRUCTIONS_AVAILABLE             = 13
	PF_SSSE3_INSTRUCTIONS_AVAILABLE            = 36
	PF_SSE4_1_INSTRUCTIONS_AVAILABLE           = 37
	PF_SSE4_2_INSTRUCTIONS_AVAILABLE           = 38
	PF_AVX_INSTRUCTIONS_AVAILABLE              = 39
	PF_AVX2_INSTRUCTIONS_AVAILABLE             = 40
	PF_AVX512F_INSTRUCTIONS_AVAILABLE          = 41
	PF_VIRT_FIRMWARE_ENABLED                   = 21
	PF_XMMI_INSTRUCTIONS_AVAILABLE             = 6
	PF_XMMI64_INSTRUCTIONS_AVAILABLE           = 10
	PF_XSAVE_ENABLED                           = 17
	PF_ARM_V8_INSTRUCTIONS_AVAILABLE           = 29
	PF_ARM_V8_CRYPTO_INSTRUCTIONS_AVAILABLE    = 30
	PF_ARM_V8_CRC32_INSTRUCTIONS_AVAILABLE     = 31
	PF_ARM_V81_ATOMIC_INSTRUCTIONS_AVAILABLE   = 34
	PF_ARM_V82_DP_INSTRUCTIONS_AVAILABLE       = 43
	PF_ARM_V83_JSCVT_INSTRUCTIONS_AVAILABLE    = 44
	PF_ARM_V83_LRCPC_INSTRUCTIONS_AVAILABLE    = 45
	PF_ARM_SVE_INSTRUCTIONS_AVAILABLE          = 46
	PF_ARM_SVE2_INSTRUCTIONS_AVAILABLE         = 47
	PF_ARM_SVE2_1_INSTRUCTIONS_AVAILABLE       = 48
	PF_ARM_SVE_AES_INSTRUCTIONS_AVAILABLE      = 49
	PF_ARM_SVE_PMULL128_INSTRUCTIONS_AVAILABLE = 50
	PF_ARM_SVE_BITPERM_INSTRUCTIONS_AVAILABLE  = 51
	PF_ARM_SVE_BF16_INSTRUCTIONS_AVAILABLE     = 52
	PF_ARM_SVE_EBF16_INSTRUCTIONS_AVAILABLE    = 53
	PF_ARM_SVE_B16B16_INSTRUCTIONS_AVAILABLE   = 54
	PF_ARM_SVE_SHA3_INSTRUCTIONS_AVAILABLE     = 55
	PF_ARM_SVE_SM4_INSTRUCTIONS_AVAILABLE      = 56
	PF_ARM_SVE_I8MM_INSTRUCTIONS_AVAILABLE     = 57
	PF_ARM_SVE_F32MM_INSTRUCTIONS_AVAILABLE    = 58
	PF_ARM_SVE_F64MM_INSTRUCTIONS_AVAILABLE    = 59
	PF_BMI2_INSTRUCTIONS_AVAILABLE             = 60
	PF_MOVDIR64B_INSTRUCTION_AVAILABLE         = 61
	PF_ARM_LSE2_AVAILABLE                      = 62
	PF_ARM_SHA3_INSTRUCTIONS_AVAILABLE         = 64
	PF_ARM_SHA512_INSTRUCTIONS_AVAILABLE       = 65
	PF_ARM_V82_I8MM_INSTRUCTIONS_AVAILABLE     = 66
	PF_ARM_V82_FP16_INSTRUCTIONS_AVAILABLE     = 67
	PF_ARM_V86_BF16_INSTRUCTIONS_AVAILABLE     = 68
	PF_ARM_V86_EBF16_INSTRUCTIONS_AVAILABLE    = 69
	PF_ARM_SME_INSTRUCTIONS_AVAILABLE          = 70
	PF_ARM_SME2_INSTRUCTIONS_AVAILABLE         = 71
	PF_ARM_SME2_1_INSTRUCTIONS_AVAILABLE       = 72
	PF_ARM_SME2_2_INSTRUCTIONS_AVAILABLE       = 73
	PF_ARM_SME_AES_INSTRUCTIONS_AVAILABLE      = 74
	PF_ARM_SME_SBITPERM_INSTRUCTIONS_AVAILABLE = 75
	PF_ARM_SME_SF8MM4_INSTRUCTIONS_AVAILABLE   = 76
	PF_ARM_SME_SF8MM8_INSTRUCTIONS_AVAILABLE   = 77
	PF_ARM_SME_SF8DP2_INSTRUCTIONS_AVAILABLE   = 78
	PF_ARM_SME_SF8DP4_INSTRUCTIONS_AVAILABLE   = 79
	PF_ARM_SME_SF8FMA_INSTRUCTIONS_AVAILABLE   = 80
	PF_ARM_SME_F8F32_INSTRUCTIONS_AVAILABLE    = 81
	PF_ARM_SME_F8F16_INSTRUCTIONS_AVAILABLE    = 82
	PF_ARM_SME_F16F16_INSTRUCTIONS_AVAILABLE   = 83
	PF_ARM_SME_B16B16_INSTRUCTIONS_AVAILABLE   = 84
	PF_ARM_SME_F64F64_INSTRUCTIONS_AVAILABLE   = 85
	PF_ARM_SME_I16I64_INSTRUCTIONS_AVAILABLE   = 86
	PF_ARM_SME_LUTv2_INSTRUCTIONS_AVAILABLE    = 87
	PF_ARM_SME_FA64_INSTRUCTIONS_AVAILABLE     = 88
	PF_UMONITOR_INSTRUCTION_AVAILABLE          = 89
)
    The processor features to be tested for IsProcessorFeaturePresent, see
    https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-isprocessorfeaturepresent

const FileFlagsMask = 0xFFF00000
const (
	FileModeInformation = 16
)
const FileReplaceCompletionInformation = 61
const MAX_MODULE_NAME32 = 255
const MB_ERR_INVALID_CHARS = 8
const (
	O_DIRECTORY = 0x04000 // target must be a directory
)
    Openat flags supported by syscall.Open.

const SE_GROUP_INTEGRITY = 0x00000020
const SizeofModuleEntry32 = unsafe.Sizeof(ModuleEntry32{})
const (
	USER_PRIV_USER = 1
)
const VER_NT_WORKSTATION = 0x0000001
    https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-osversioninfoexa
    https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/ns-wdm-_osversioninfoexw

const ValidFileFlagsMask = O_FILE_FLAG_OPEN_REPARSE_POINT |
	O_FILE_FLAG_BACKUP_SEMANTICS |
	O_FILE_FLAG_OVERLAPPED |
	O_FILE_FLAG_OPEN_NO_RECALL |
	O_FILE_FLAG_SESSION_AWARE |
	O_FILE_FLAG_POSIX_SEMANTICS |
	O_FILE_FLAG_DELETE_ON_CLOSE |
	O_FILE_FLAG_SEQUENTIAL_SCAN |
	O_FILE_FLAG_NO_BUFFERING |
	O_FILE_FLAG_RANDOM_ACCESS |
	O_FILE_FLAG_WRITE_THROUGH

VARIABLES

var CanUseLongPaths bool
    CanUseLongPaths is true when the OS supports opting into proper long path
    handling without the need for fixups.

var SECURITY_NT_AUTHORITY = SID_IDENTIFIER_AUTHORITY{
	Value: [6]byte{0, 0, 0, 0, 0, 5},
}
var SupportTCPInitialRTONoSYNRetransmissions = sync.OnceValue(func() bool {
	major, _, build := Version()
	return major >= 10 && build >= 16299
})
    SupportTCPInitialRTONoSYNRetransmissions indicates whether the current
    Windows version supports the TCP_INITIAL_RTO_NO_SYN_RETRANSMISSIONS.
    The minimal requirement is Windows 10.0.16299.

var SupportUnixSocket = sync.OnceValue(func() bool {
	var size uint32

	_, _ = syscall.WSAEnumProtocols(nil, nil, &size)
	n := int32(size) / int32(unsafe.Sizeof(syscall.WSAProtocolInfo{}))

	buf := make([]syscall.WSAProtocolInfo, n)
	n, err := syscall.WSAEnumProtocols(nil, &buf[0], &size)
	if err != nil {
		return false
	}
	for i := int32(0); i < n; i++ {
		if buf[i].AddressFamily == syscall.AF_UNIX {
			return true
		}
	}
	return false
})
    SupportUnixSocket indicates whether the current Windows version supports
    Unix Domain Sockets. The minimal requirement is Windows 10.0.17063.

var SupportUnlimitedTransmitFile = sync.OnceValue(func() bool {
	info := getVersionInfo()
	return info.productType != VER_NT_WORKSTATION
})
    SupportUnlimitedTransmitFile indicates whether the current Windows version's
    TransmitFile function imposes any concurrent operation limits. Workstation
    and client versions of Windows limit the number of concurrent TransmitFile
    operations allowed on the system to a maximum of two. Please see:
    https://learn.microsoft.com/en-us/windows/win32/api/mswsock/nf-mswsock-transmitfile
    https://golang.org/issue/73746

var TestDeleteatFallback bool
    TestDeleteatFallback should only be used for testing purposes. When set,
    Deleteat uses the fallback path unconditionally.

var WSAID_WSARECVMSG = syscall.GUID{
	Data1: 0xf689d7c8,
	Data2: 0x6f1f,
	Data3: 0x436b,
	Data4: [8]byte{0x8a, 0x53, 0xe5, 0x4f, 0xe3, 0x51, 0xc3, 0x22},
}
var WSAID_WSASENDMSG = syscall.GUID{
	Data1: 0xa441e712,
	Data2: 0x754f,
	Data3: 0x43ca,
	Data4: [8]byte{0x84, 0xa7, 0x0d, 0xee, 0x44, 0xcf, 0x60, 0x6d},
}

FUNCTIONS

func AdjustTokenPrivileges(token syscall.Token, disableAllPrivileges bool, newstate *TOKEN_PRIVILEGES, buflen uint32, prevstate *TOKEN_PRIVILEGES, returnlen *uint32) error
func CreateEnvironmentBlock(block **uint16, token syscall.Token, inheritExisting bool) (err error)
func CreateEvent(eventAttrs *SecurityAttributes, manualReset uint32, initialState uint32, name *uint16) (handle syscall.Handle, err error)
func CreateIoCompletionPort(filehandle syscall.Handle, cphandle syscall.Handle, key uintptr, threadcnt uint32) (handle syscall.Handle, err error)
func CreateNamedPipe(name *uint16, flags uint32, pipeMode uint32, maxInstances uint32, outSize uint32, inSize uint32, defaultTimeout uint32, sa *syscall.SecurityAttributes) (handle syscall.Handle, err error)
func Deleteat(dirfd syscall.Handle, name string, options uint32) error
func DestroyEnvironmentBlock(block *uint16) (err error)
func DuplicateTokenEx(hExistingToken syscall.Token, dwDesiredAccess uint32, lpTokenAttributes *syscall.SecurityAttributes, impersonationLevel uint32, tokenType TokenType, phNewToken *syscall.Token) (err error)
func ErrorLoadingGetTempPath2() error
func FinalPath(h syscall.Handle, flags uint32) (string, error)
func GetACP() (acp uint32)
func GetAdaptersAddresses(family uint32, flags uint32, reserved unsafe.Pointer, adapterAddresses *IpAdapterAddresses, sizePointer *uint32) (errcode error)
func GetComputerNameEx(nameformat uint32, buf *uint16, n *uint32) (err error)
func GetConsoleCP() (ccp uint32)
func GetCurrentThread() (pseudoHandle syscall.Handle, err error)
func GetFileInformationByHandleEx(handle syscall.Handle, class uint32, info *byte, bufsize uint32) (err error)
func GetFileSizeEx(handle syscall.Handle, size *int64) (err error)
func GetFinalPathNameByHandle(file syscall.Handle, filePath *uint16, filePathSize uint32, flags uint32) (n uint32, err error)
func GetModuleFileName(module syscall.Handle, fn *uint16, len uint32) (n uint32, err error)
func GetModuleHandle(modulename *uint16) (handle syscall.Handle, err error)
func GetOverlappedResult(handle syscall.Handle, overlapped *syscall.Overlapped, done *uint32, wait bool) (err error)
func GetProcessMemoryInfo(handle syscall.Handle, memCounters *PROCESS_MEMORY_COUNTERS, cb uint32) (err error)
func GetProfilesDirectory(dir *uint16, dirLen *uint32) (err error)
func GetSidSubAuthority(sid *syscall.SID, subAuthorityIdx uint32) uint32
func GetSidSubAuthorityCount(sid *syscall.SID) uint8
func GetSystemDirectory() string
    GetSystemDirectory retrieves the path to current location of the system
    directory, which is typically, though not always, `C:\Windows\System32`.

func GetTempPath2(buflen uint32, buf *uint16) (n uint32, err error)
func GetTokenGroups(t syscall.Token) (*TOKEN_GROUPS, error)
func GetUserName(format uint32) (string, error)
    GetUserName retrieves the user name of the current thread in the specified
    format.

func GetVolumeInformationByHandle(file syscall.Handle, volumeNameBuffer *uint16, volumeNameSize uint32, volumeNameSerialNumber *uint32, maximumComponentLength *uint32, fileSystemFlags *uint32, fileSystemNameBuffer *uint16, fileSystemNameSize uint32) (err error)
func GetVolumeNameForVolumeMountPoint(volumeMountPoint *uint16, volumeName *uint16, bufferlength uint32) (err error)
func ImpersonateLoggedOnUser(token syscall.Token) (err error)
func ImpersonateSelf(impersonationlevel uint32) (err error)
func IsNonblock(fd syscall.Handle) (nonblocking bool, err error)
    IsNonblock returns whether the file descriptor fd is opened in non-blocking
    mode, that is, the windows.O_FILE_FLAG_OVERLAPPED flag was set when the file
    was opened.

func IsProcessorFeaturePresent(ProcessorFeature uint32) (ret bool)
func IsValidSid(sid *syscall.SID) (valid bool)
func Linkat(olddirfd syscall.Handle, oldpath string, newdirfd syscall.Handle, newpath string) error
func LockFileEx(file syscall.Handle, flags uint32, reserved uint32, bytesLow uint32, bytesHigh uint32, overlapped *syscall.Overlapped) (err error)
func LogonUser(username *uint16, domain *uint16, password *uint16, logonType uint32, logonProvider uint32, token *syscall.Token) (err error)
func LookupPrivilegeValue(systemname *uint16, name *uint16, luid *LUID) (err error)
func Mkdirat(dirfd syscall.Handle, name string, mode uint32) error
func Module32First(snapshot syscall.Handle, moduleEntry *ModuleEntry32) (err error)
func Module32Next(snapshot syscall.Handle, moduleEntry *ModuleEntry32) (err error)
func MoveFileEx(from *uint16, to *uint16, flags uint32) (err error)
func MultiByteToWideChar(codePage uint32, dwFlags uint32, str *byte, nstr int32, wchar *uint16, nwchar int32) (nwrite int32, err error)
func NetShareAdd(serverName *uint16, level uint32, buf *byte, parmErr *uint16) (neterr error)
func NetShareDel(serverName *uint16, netName *uint16, reserved uint32) (neterr error)
func NetUserAdd(serverName *uint16, level uint32, buf *byte, parmErr *uint32) (neterr error)
func NetUserDel(serverName *uint16, userName *uint16) (neterr error)
func NetUserGetLocalGroups(serverName *uint16, userName *uint16, level uint32, flags uint32, buf **byte, prefMaxLen uint32, entriesRead *uint32, totalEntries *uint32) (neterr error)
func NewNTUnicodeString(s string) (*NTUnicodeString, error)
    NewNTUnicodeString returns a new NTUnicodeString structure for use with
    native NT APIs that work over the NTUnicodeString type. Note that most
    Windows APIs do not use NTUnicodeString, and instead UTF16PtrFromString
    should be used for the more common *uint16 string type.

func NtCreateFile(handle *syscall.Handle, access uint32, oa *OBJECT_ATTRIBUTES, iosb *IO_STATUS_BLOCK, allocationSize *int64, attributes uint32, share uint32, disposition uint32, options uint32, eabuffer unsafe.Pointer, ealength uint32) (ntstatus error)
func NtOpenFile(handle *syscall.Handle, access uint32, oa *OBJECT_ATTRIBUTES, iosb *IO_STATUS_BLOCK, share uint32, options uint32) (ntstatus error)
func NtQueryInformationFile(handle syscall.Handle, iosb *IO_STATUS_BLOCK, inBuffer unsafe.Pointer, inBufferLen uint32, class uint32) (ntstatus error)
func NtSetInformationFile(handle syscall.Handle, iosb *IO_STATUS_BLOCK, inBuffer unsafe.Pointer, inBufferLen uint32, class uint32) (ntstatus error)
func OpenSCManager(machineName *uint16, databaseName *uint16, access uint32) (handle syscall.Handle, err error)
func OpenService(mgr syscall.Handle, serviceName *uint16, access uint32) (handle syscall.Handle, err error)
func OpenThreadToken(h syscall.Handle, access uint32, openasself bool, token *syscall.Token) (err error)
func Openat(dirfd syscall.Handle, name string, flag uint64, perm uint32) (_ syscall.Handle, e1 error)
func ProcessPrng(buf []byte) (err error)
func QueryPerformanceCounter() int64
    QueryPerformanceCounter retrieves the current value of performance counter.

func QueryPerformanceFrequency() int64
    QueryPerformanceFrequency retrieves the frequency of the performance
    counter. The returned value is represented as counts per second.

func QueryServiceStatus(hService syscall.Handle, lpServiceStatus *SERVICE_STATUS) (err error)
func ReOpenFile(filehandle syscall.Handle, desiredAccess uint32, shareMode uint32, flagAndAttributes uint32) (handle syscall.Handle, err error)
func Rename(oldpath, newpath string) error
func Renameat(olddirfd syscall.Handle, oldpath string, newdirfd syscall.Handle, newpath string) error
func RevertToSelf() (err error)
func RtlIsDosDeviceName_U(name *uint16) (ret uint32)
func RtlVirtualUnwind(handlerType uint32, baseAddress uintptr, pc uintptr, entry *RUNTIME_FUNCTION, ctxt unsafe.Pointer, data unsafe.Pointer, frame *uintptr, ctxptrs unsafe.Pointer) (ret uintptr)
func SetEntriesInAcl(countExplicitEntries uint32, explicitEntries *EXPLICIT_ACCESS, oldACL *ACL, newACL **ACL) (ret error)
func SetFileInformationByHandle(handle syscall.Handle, fileInformationClass uint32, buf unsafe.Pointer, bufsize uint32) (err error)
func SetNamedSecurityInfo(objectName string, objectType uint32, securityInformation uint32, owner *syscall.SID, group *syscall.SID, dacl *ACL, sacl *ACL) (ret error)
func SetTokenInformation(tokenHandle syscall.Token, tokenInformationClass uint32, tokenInformation unsafe.Pointer, tokenInformationLength uint32) (err error)
func SupportTCPKeepAliveCount() bool
    SupportTCPKeepAliveCount indicates whether TCP_KEEPCNT is supported.
    supports TCP_KEEPCNT. The minimal requirement is Windows 10.0.15063.

func SupportTCPKeepAliveIdle() bool
    SupportTCPKeepAliveIdle indicates whether TCP_KEEPIDLE is supported.
    The minimal requirement is Windows 10.0.16299.

func SupportTCPKeepAliveInterval() bool
    SupportTCPKeepAliveInterval indicates whether TCP_KEEPINTVL is supported.
    The minimal requirement is Windows 10.0.16299.

func Symlinkat(oldname string, newdirfd syscall.Handle, newname string, flags SymlinkatFlags) error
func UTF16PtrToString(p *uint16) string
    UTF16PtrToString is like UTF16ToString, but takes *uint16 as a parameter
    instead of []uint16.

func UnlockFileEx(file syscall.Handle, reserved uint32, bytesLow uint32, bytesHigh uint32, overlapped *syscall.Overlapped) (err error)
func Version() (major, minor, build uint32)
    Version retrieves the major, minor, and build version numbers of the current
    Windows OS from the RtlGetVersion API.

func VirtualQuery(address uintptr, buffer *MemoryBasicInformation, length uintptr) (err error)
func WSADuplicateSocket(s syscall.Handle, processID uint32, info *syscall.WSAProtocolInfo) (err error)
func WSAGetOverlappedResult(h syscall.Handle, o *syscall.Overlapped, bytes *uint32, wait bool, flags *uint32) (err error)
func WSARecvMsg(fd syscall.Handle, msg *WSAMsg, bytesReceived *uint32, overlapped *syscall.Overlapped, croutine *byte) error
func WSASendMsg(fd syscall.Handle, msg *WSAMsg, flags uint32, bytesSent *uint32, overlapped *syscall.Overlapped, croutine *byte) error
func WSASendtoInet4(s syscall.Handle, bufs *syscall.WSABuf, bufcnt uint32, sent *uint32, flags uint32, to *syscall.SockaddrInet4, overlapped *syscall.Overlapped, croutine *byte) (err error)
func WSASendtoInet6(s syscall.Handle, bufs *syscall.WSABuf, bufcnt uint32, sent *uint32, flags uint32, to *syscall.SockaddrInet6, overlapped *syscall.Overlapped, croutine *byte) (err error)
func WSASocket(af int32, typ int32, protocol int32, protinfo *syscall.WSAProtocolInfo, group uint32, flags uint32) (handle syscall.Handle, err error)

TYPES

type ACCESS_MASK uint32
    https://learn.microsoft.com/en-us/windows/win32/secauthz/access-mask

type ACL struct {
	AclRevision byte
	Sbz1        byte
	AclSize     uint16
	AceCount    uint16
	Sbz2        uint16
}
    https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/ns-wdm-_acl

type Context = windows.Context

type EXPLICIT_ACCESS struct {
	AccessPermissions uint32
	AccessMode        uint32
	Inheritance       uint32
	Trustee           TRUSTEE
}
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa446627.aspx

type FILE_ATTRIBUTE_TAG_INFO struct {
	FileAttributes uint32
	ReparseTag     uint32
}

type FILE_BASIC_INFO struct {
	CreationTime   int64
	LastAccessTime int64
	LastWriteTime  int64
	ChangedTime    int64
	FileAttributes uint32

	// Has unexported fields.
}

type FILE_COMPLETION_INFORMATION struct {
	Port syscall.Handle
	Key  uintptr
}
    https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/ns-ntifs-_file_completion_information

type FILE_DISPOSITION_INFO struct {
	DeleteFile byte
}
    https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_disposition_info

type FILE_DISPOSITION_INFORMATION struct {
	DeleteFile byte
}
    https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntddk/ns-ntddk-_file_disposition_information

type FILE_DISPOSITION_INFORMATION_EX struct {
	Flags uint32
}
    https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntddk/ns-ntddk-_file_disposition_information_ex

type FILE_FULL_DIR_INFO struct {
	NextEntryOffset uint32
	FileIndex       uint32
	CreationTime    syscall.Filetime
	LastAccessTime  syscall.Filetime
	LastWriteTime   syscall.Filetime
	ChangeTime      syscall.Filetime
	EndOfFile       uint64
	AllocationSize  uint64
	FileAttributes  uint32
	FileNameLength  uint32
	EaSize          uint32
	FileName        [1]uint16
}

type FILE_ID_BOTH_DIR_INFO struct {
	NextEntryOffset uint32
	FileIndex       uint32
	CreationTime    syscall.Filetime
	LastAccessTime  syscall.Filetime
	LastWriteTime   syscall.Filetime
	ChangeTime      syscall.Filetime
	EndOfFile       uint64
	AllocationSize  uint64
	FileAttributes  uint32
	FileNameLength  uint32
	EaSize          uint32
	ShortNameLength uint32
	ShortName       [12]uint16
	FileID          uint64
	FileName        [1]uint16
}

type FILE_LINK_INFORMATION struct {
	ReplaceIfExists byte
	RootDirectory   syscall.Handle
	FileNameLength  uint32
	FileName        [syscall.MAX_PATH]uint16
}
    https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/ns-ntifs-_file_link_information

type FILE_MODE_INFORMATION struct {
	Mode uint32
}
    https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/ns-ntifs-_file_mode_information

type FILE_RENAME_INFORMATION struct {
	ReplaceIfExists byte
	RootDirectory   syscall.Handle
	FileNameLength  uint32
	FileName        [syscall.MAX_PATH]uint16
}
    https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/ns-ntifs-_file_rename_information

type FILE_RENAME_INFORMATION_EX struct {
	Flags          uint32
	RootDirectory  syscall.Handle
	FileNameLength uint32
	FileName       [syscall.MAX_PATH]uint16
}
    https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/ns-ntifs-_file_rename_information

type IO_STATUS_BLOCK struct {
	Status      NTStatus
	Information uintptr
}
    https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/ns-wdm-_io_status_block

type IpAdapterAddresses struct {
	Length                 uint32
	IfIndex                uint32
	Next                   *IpAdapterAddresses
	AdapterName            *byte
	FirstUnicastAddress    *IpAdapterUnicastAddress
	FirstAnycastAddress    *IpAdapterAnycastAddress
	FirstMulticastAddress  *IpAdapterMulticastAddress
	FirstDnsServerAddress  *IpAdapterDnsServerAdapter
	DnsSuffix              *uint16
	Description            *uint16
	FriendlyName           *uint16
	PhysicalAddress        [syscall.MAX_ADAPTER_ADDRESS_LENGTH]byte
	PhysicalAddressLength  uint32
	Flags                  uint32
	Mtu                    uint32
	IfType                 uint32
	OperStatus             uint32
	Ipv6IfIndex            uint32
	ZoneIndices            [16]uint32
	FirstPrefix            *IpAdapterPrefix
	TransmitLinkSpeed      uint64
	ReceiveLinkSpeed       uint64
	FirstWinsServerAddress *IpAdapterWinsServerAddress
	FirstGatewayAddress    *IpAdapterGatewayAddress
}

type IpAdapterAnycastAddress struct {
	Length  uint32
	Flags   uint32
	Next    *IpAdapterAnycastAddress
	Address SocketAddress
}

type IpAdapterDnsServerAdapter struct {
	Length   uint32
	Reserved uint32
	Next     *IpAdapterDnsServerAdapter
	Address  SocketAddress
}

type IpAdapterGatewayAddress struct {
	Length   uint32
	Reserved uint32
	Next     *IpAdapterGatewayAddress
	Address  SocketAddress
}

type IpAdapterMulticastAddress struct {
	Length  uint32
	Flags   uint32
	Next    *IpAdapterMulticastAddress
	Address SocketAddress
}

type IpAdapterPrefix struct {
	Length       uint32
	Flags        uint32
	Next         *IpAdapterPrefix
	Address      SocketAddress
	PrefixLength uint32
}

type IpAdapterUnicastAddress struct {
	Length             uint32
	Flags              uint32
	Next               *IpAdapterUnicastAddress
	Address            SocketAddress
	PrefixOrigin       int32
	SuffixOrigin       int32
	DadState           int32
	ValidLifetime      uint32
	PreferredLifetime  uint32
	LeaseLifetime      uint32
	OnLinkPrefixLength uint8
}

type IpAdapterWinsServerAddress struct {
	Length   uint32
	Reserved uint32
	Next     *IpAdapterWinsServerAddress
	Address  SocketAddress
}

type LUID struct {
	LowPart  uint32
	HighPart int32
}

type LUID_AND_ATTRIBUTES struct {
	Luid       LUID
	Attributes uint32
}

type LocalGroupUserInfo0 struct {
	Name *uint16
}

type MemoryBasicInformation = windows.MemoryBasicInformation

type ModuleEntry32 struct {
	Size         uint32
	ModuleID     uint32
	ProcessID    uint32
	GlblcntUsage uint32
	ProccntUsage uint32
	ModBaseAddr  uintptr
	ModBaseSize  uint32
	ModuleHandle syscall.Handle
	Module       [MAX_MODULE_NAME32 + 1]uint16
	ExePath      [syscall.MAX_PATH]uint16
}

type MountPointReparseBuffer struct {
	// The integer that contains the offset, in bytes,
	// of the substitute name string in the PathBuffer array,
	// computed as an offset from byte 0 of PathBuffer. Note that
	// this offset must be divided by 2 to get the array index.
	SubstituteNameOffset uint16
	// The integer that contains the length, in bytes, of the
	// substitute name string. If this string is null-terminated,
	// SubstituteNameLength does not include the Unicode null character.
	SubstituteNameLength uint16
	// PrintNameOffset is similar to SubstituteNameOffset.
	PrintNameOffset uint16
	// PrintNameLength is similar to SubstituteNameLength.
	PrintNameLength uint16
	PathBuffer      [1]uint16
}

func (rb *MountPointReparseBuffer) Path() string
    Path returns path stored in rb.

type NTStatus uint32
    NTStatus corresponds with NTSTATUS, error values returned by ntdll.dll and
    other native functions.

const (
	STATUS_OBJECT_NAME_COLLISION     NTStatus = 0xC0000035
	STATUS_FILE_IS_A_DIRECTORY       NTStatus = 0xC00000BA
	STATUS_DIRECTORY_NOT_EMPTY       NTStatus = 0xC0000101
	STATUS_NOT_A_DIRECTORY           NTStatus = 0xC0000103
	STATUS_CANNOT_DELETE             NTStatus = 0xC0000121
	STATUS_REPARSE_POINT_ENCOUNTERED NTStatus = 0xC000050B
	STATUS_NOT_SUPPORTED             NTStatus = 0xC00000BB
	STATUS_INVALID_PARAMETER         NTStatus = 0xC000000D
	STATUS_INVALID_INFO_CLASS        NTStatus = 0xC0000003
	STATUS_ACCESS_DENIED             NTStatus = 0xC0000022
)
    x/sys/windows/mkerrors.bash can generate a complete list of NTStatus codes.

    At the moment, we only need a couple, so just put them here manually. If
    this list starts getting long, we should consider generating the full set.

func (s NTStatus) Errno() syscall.Errno

func (s NTStatus) Error() string

type NTUnicodeString struct {
	Length        uint16
	MaximumLength uint16
	Buffer        *uint16
}
    NTUnicodeString is a UTF-16 string for NT native APIs, corresponding to
    UNICODE_STRING.

type OBJECT_ATTRIBUTES struct {
	Length             uint32
	RootDirectory      syscall.Handle
	ObjectName         *NTUnicodeString
	Attributes         uint32
	SecurityDescriptor *SECURITY_DESCRIPTOR
	SecurityQoS        *SECURITY_QUALITY_OF_SERVICE
}
    https://learn.microsoft.com/en-us/windows/win32/api/ntdef/ns-ntdef-_object_attributes

type PROCESS_MEMORY_COUNTERS struct {
	CB                         uint32
	PageFaultCount             uint32
	PeakWorkingSetSize         uintptr
	WorkingSetSize             uintptr
	QuotaPeakPagedPoolUsage    uintptr
	QuotaPagedPoolUsage        uintptr
	QuotaPeakNonPagedPoolUsage uintptr
	QuotaNonPagedPoolUsage     uintptr
	PagefileUsage              uintptr
	PeakPagefileUsage          uintptr
}

type REPARSE_DATA_BUFFER struct {
	ReparseTag        uint32
	ReparseDataLength uint16
	Reserved          uint16
	DUMMYUNIONNAME    byte
}

type REPARSE_DATA_BUFFER_HEADER struct {
	ReparseTag uint32
	// The size, in bytes, of the reparse data that follows
	// the common portion of the REPARSE_DATA_BUFFER element.
	// This value is the length of the data starting at the
	// SubstituteNameOffset field.
	ReparseDataLength uint16
	Reserved          uint16
}
    REPARSE_DATA_BUFFER_HEADER is a common part of REPARSE_DATA_BUFFER
    structure.

type RUNTIME_FUNCTION struct {
	BeginAddress uint32
	EndAddress   uint32
	UnwindData   uint32
}

func RtlLookupFunctionEntry(pc uintptr, baseAddress *uintptr, table unsafe.Pointer) (ret *RUNTIME_FUNCTION)

type SECURITY_DESCRIPTOR struct {
	// Has unexported fields.
}
    https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/ns-ntifs-_security_descriptor

type SECURITY_DESCRIPTOR_CONTROL uint16
    https://learn.microsoft.com/en-us/windows-hardware/drivers/ifs/security-descriptor-control

type SECURITY_QUALITY_OF_SERVICE struct {
	Length              uint32
	ImpersonationLevel  uint32 // type SECURITY_IMPERSONATION_LEVEL
	ContextTrackingMode byte   // type SECURITY_CONTEXT_TRACKING_MODE
	EffectiveOnly       byte
}
    https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-security_quality_of_service

type SERVICE_STATUS struct {
	ServiceType             uint32
	CurrentState            uint32
	ControlsAccepted        uint32
	Win32ExitCode           uint32
	ServiceSpecificExitCode uint32
	CheckPoint              uint32
	WaitHint                uint32
}

type SHARE_INFO_2 struct {
	Netname     *uint16
	Type        uint32
	Remark      *uint16
	Permissions uint32
	MaxUses     uint32
	CurrentUses uint32
	Path        *uint16
	Passwd      *uint16
}

type SID_AND_ATTRIBUTES struct {
	Sid        *syscall.SID
	Attributes uint32
}

type SID_IDENTIFIER_AUTHORITY struct {
	Value [6]byte
}
    https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-sid_identifier_authority

func GetSidIdentifierAuthority(sid *syscall.SID) SID_IDENTIFIER_AUTHORITY

type SecurityAttributes struct {
	Length             uint16
	SecurityDescriptor uintptr
	InheritHandle      bool
}

type SocketAddress struct {
	Sockaddr       *syscall.RawSockaddrAny
	SockaddrLength int32
}

type SymbolicLinkReparseBuffer struct {
	// The integer that contains the offset, in bytes,
	// of the substitute name string in the PathBuffer array,
	// computed as an offset from byte 0 of PathBuffer. Note that
	// this offset must be divided by 2 to get the array index.
	SubstituteNameOffset uint16
	// The integer that contains the length, in bytes, of the
	// substitute name string. If this string is null-terminated,
	// SubstituteNameLength does not include the Unicode null character.
	SubstituteNameLength uint16
	// PrintNameOffset is similar to SubstituteNameOffset.
	PrintNameOffset uint16
	// PrintNameLength is similar to SubstituteNameLength.
	PrintNameLength uint16
	// Flags specifies whether the substitute name is a full path name or
	// a path name relative to the directory containing the symbolic link.
	Flags      uint32
	PathBuffer [1]uint16
}

func (rb *SymbolicLinkReparseBuffer) Path() string
    Path returns path stored in rb.

type SymlinkatFlags uint
    SymlinkatFlags configure Symlinkat.

    Symbolic links have two properties: They may be directory or file links,
    and they may be absolute or relative.

    The Windows API defines flags describing these properties
    (SYMBOLIC_LINK_FLAG_DIRECTORY and SYMLINK_FLAG_RELATIVE), but the flags
    are passed to different system calls and do not have distinct values,
    so we define our own enumeration that permits expressing both.

type TCP_INITIAL_RTO_PARAMETERS struct {
	Rtt                   uint16
	MaxSynRetransmissions uint8
}

type TOKEN_GROUPS struct {
	GroupCount uint32
	Groups     [1]SID_AND_ATTRIBUTES
}

func (g *TOKEN_GROUPS) AllGroups() []SID_AND_ATTRIBUTES

type TOKEN_MANDATORY_LABEL struct {
	Label SID_AND_ATTRIBUTES
}

func (tml *TOKEN_MANDATORY_LABEL) Size() uint32

type TOKEN_PRIVILEGES struct {
	PrivilegeCount uint32
	Privileges     [1]LUID_AND_ATTRIBUTES
}

type TRUSTEE struct {
	MultipleTrustee          *TRUSTEE
	MultipleTrusteeOperation uint32
	TrusteeForm              uint32
	TrusteeType              uint32
	Name                     uintptr
}
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa379636.aspx

type TokenType uint32

const (
	TokenPrimary       TokenType = 1
	TokenImpersonation TokenType = 2
)
type UserInfo1 struct {
	Name        *uint16
	Password    *uint16
	PasswordAge uint32
	Priv        uint32
	HomeDir     *uint16
	Comment     *uint16
	Flags       uint32
	ScriptPath  *uint16
}

type UserInfo4 struct {
	Name            *uint16
	Password        *uint16
	PasswordAge     uint32
	Priv            uint32
	HomeDir         *uint16
	Comment         *uint16
	Flags           uint32
	ScriptPath      *uint16
	AuthFlags       uint32
	FullName        *uint16
	UsrComment      *uint16
	Parms           *uint16
	Workstations    *uint16
	LastLogon       uint32
	LastLogoff      uint32
	AcctExpires     uint32
	MaxStorage      uint32
	UnitsPerWeek    uint32
	LogonHours      *byte
	BadPwCount      uint32
	NumLogons       uint32
	LogonServer     *uint16
	CountryCode     uint32
	CodePage        uint32
	UserSid         *syscall.SID
	PrimaryGroupID  uint32
	Profile         *uint16
	HomeDirDrive    *uint16
	PasswordExpired uint32
}

type WSAMsg struct {
	Name        *syscall.RawSockaddrAny
	Namelen     int32
	Buffers     *syscall.WSABuf
	BufferCount uint32
	Control     syscall.WSABuf
	Flags       uint32
}
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
