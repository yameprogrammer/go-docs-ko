# package syscall

- 원문: <https://pkg.go.dev/syscall>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `syscall`은 저수준 운영체제 기본 기능을 사용할 수 있는 인터페이스를 제공합니다.

## 원문 요약

Package syscall contains an interface to the low-level operating system primitives.

## API 상세 (go doc -all)

~~~text
package syscall // import "syscall"

Package syscall contains an interface to the low-level operating system
primitives. The details vary depending on the underlying system, and by default,
godoc will display the syscall documentation for the current system. If you
want godoc to display syscall documentation for another system, set $GOOS and
$GOARCH to the desired system. For example, if you want to view documentation
for freebsd/arm on linux/amd64, set $GOOS to freebsd and $GOARCH to arm.
The primary use of syscall is inside other packages that provide a more portable
interface to the system, such as "os", "time" and "net". Use those packages
rather than this one if you can. For details of the functions and data types
in this package consult the manuals for the appropriate operating system.
These calls return err == nil to indicate success; otherwise err is an operating
system error describing the failure. On most systems, that error has type Errno.

NOTE: Most of the functions, types, and constants defined in this package are
also available in the golang.org/x/sys package. That package has more system
call support than this one, and most new code should prefer that package where
possible. See https://golang.org/s/go1.4-syscall for more information.

CONSTANTS

const (
	STANDARD_RIGHTS_REQUIRED = 0xf0000
	STANDARD_RIGHTS_READ     = 0x20000
	STANDARD_RIGHTS_WRITE    = 0x20000
	STANDARD_RIGHTS_EXECUTE  = 0x20000
	STANDARD_RIGHTS_ALL      = 0x1F0000
)
const (
	NameUnknown          = 0
	NameFullyQualifiedDN = 1
	NameSamCompatible    = 2
	NameDisplay          = 3
	NameUniqueId         = 6
	NameCanonical        = 7
	NameUserPrincipal    = 8
	NameCanonicalEx      = 9
	NameServicePrincipal = 10
	NameDnsDomain        = 12
)
const (
	// do not reorder
	NetSetupUnknownStatus = iota
	NetSetupUnjoined
	NetSetupWorkgroupName
	NetSetupDomainName
)
const (
	// do not reorder
	SidTypeUser = 1 + iota
	SidTypeGroup
	SidTypeDomain
	SidTypeAlias
	SidTypeWellKnownGroup
	SidTypeDeletedAccount
	SidTypeInvalid
	SidTypeUnknown
	SidTypeComputer
	SidTypeLabel
)
const (
	// do not reorder
	TOKEN_ASSIGN_PRIMARY = 1 << iota
	TOKEN_DUPLICATE
	TOKEN_IMPERSONATE
	TOKEN_QUERY
	TOKEN_QUERY_SOURCE
	TOKEN_ADJUST_PRIVILEGES
	TOKEN_ADJUST_GROUPS
	TOKEN_ADJUST_DEFAULT
	TOKEN_ADJUST_SESSIONID

	TOKEN_ALL_ACCESS = STANDARD_RIGHTS_REQUIRED |
		TOKEN_ASSIGN_PRIMARY |
		TOKEN_DUPLICATE |
		TOKEN_IMPERSONATE |
		TOKEN_QUERY |
		TOKEN_QUERY_SOURCE |
		TOKEN_ADJUST_PRIVILEGES |
		TOKEN_ADJUST_GROUPS |
		TOKEN_ADJUST_DEFAULT |
		TOKEN_ADJUST_SESSIONID
	TOKEN_READ  = STANDARD_RIGHTS_READ | TOKEN_QUERY
	TOKEN_WRITE = STANDARD_RIGHTS_WRITE |
		TOKEN_ADJUST_PRIVILEGES |
		TOKEN_ADJUST_GROUPS |
		TOKEN_ADJUST_DEFAULT
	TOKEN_EXECUTE = STANDARD_RIGHTS_EXECUTE
)
const (
	// do not reorder
	TokenUser = 1 + iota
	TokenGroups
	TokenPrivileges
	TokenOwner
	TokenPrimaryGroup
	TokenDefaultDacl
	TokenSource
	TokenType
	TokenImpersonationLevel
	TokenStatistics
	TokenRestrictedSids
	TokenSessionId
	TokenGroupsAndPrivileges
	TokenSessionReference
	TokenSandBoxInert
	TokenAuditPolicy
	TokenOrigin
	TokenElevationType
	TokenLinkedToken
	TokenElevation
	TokenHasRestrictions
	TokenAccessInformation
	TokenVirtualizationAllowed
	TokenVirtualizationEnabled
	TokenIntegrityLevel
	TokenUIAccess
	TokenMandatoryPolicy
	TokenLogonSid
	MaxTokenInfoClass
)
const (
	// Invented values to support what package os expects.
	O_RDONLY   = 0x00000
	O_WRONLY   = 0x00001
	O_RDWR     = 0x00002
	O_CREAT    = 0x00040
	O_EXCL     = 0x00080
	O_NOCTTY   = 0x00100
	O_TRUNC    = 0x00200
	O_NONBLOCK = 0x00800
	O_APPEND   = 0x00400
	O_SYNC     = 0x01000
	O_ASYNC    = 0x02000

	O_CLOEXEC = 0x80000
)
const (
	// More invented values for signals
	SIGHUP  = Signal(0x1)
	SIGINT  = Signal(0x2)
	SIGQUIT = Signal(0x3)
	SIGILL  = Signal(0x4)
	SIGTRAP = Signal(0x5)
	SIGABRT = Signal(0x6)
	SIGBUS  = Signal(0x7)
	SIGFPE  = Signal(0x8)
	SIGKILL = Signal(0x9)
	SIGSEGV = Signal(0xb)
	SIGPIPE = Signal(0xd)
	SIGALRM = Signal(0xe)
	SIGTERM = Signal(0xf)
)
const (
	GENERIC_READ    = 0x80000000
	GENERIC_WRITE   = 0x40000000
	GENERIC_EXECUTE = 0x20000000
	GENERIC_ALL     = 0x10000000

	FILE_LIST_DIRECTORY = 0x00000001
	FILE_APPEND_DATA    = 0x00000004

	FILE_WRITE_ATTRIBUTES = 0x00000100

	FILE_SHARE_READ              = 0x00000001
	FILE_SHARE_WRITE             = 0x00000002
	FILE_SHARE_DELETE            = 0x00000004
	FILE_ATTRIBUTE_READONLY      = 0x00000001
	FILE_ATTRIBUTE_HIDDEN        = 0x00000002
	FILE_ATTRIBUTE_SYSTEM        = 0x00000004
	FILE_ATTRIBUTE_DIRECTORY     = 0x00000010
	FILE_ATTRIBUTE_ARCHIVE       = 0x00000020
	FILE_ATTRIBUTE_NORMAL        = 0x00000080
	FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400

	INVALID_FILE_ATTRIBUTES = 0xffffffff

	CREATE_NEW        = 1
	CREATE_ALWAYS     = 2
	OPEN_EXISTING     = 3
	OPEN_ALWAYS       = 4
	TRUNCATE_EXISTING = 5

	FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000

	FILE_FLAG_BACKUP_SEMANTICS = 0x02000000

	FILE_FLAG_OVERLAPPED = 0x40000000

	HANDLE_FLAG_INHERIT    = 0x00000001
	STARTF_USESTDHANDLES   = 0x00000100
	STARTF_USESHOWWINDOW   = 0x00000001
	DUPLICATE_CLOSE_SOURCE = 0x00000001
	DUPLICATE_SAME_ACCESS  = 0x00000002

	STD_INPUT_HANDLE  = -10
	STD_OUTPUT_HANDLE = -11
	STD_ERROR_HANDLE  = -12

	FILE_BEGIN   = 0
	FILE_CURRENT = 1
	FILE_END     = 2

	LANG_ENGLISH       = 0x09
	SUBLANG_ENGLISH_US = 0x01

	FORMAT_MESSAGE_ALLOCATE_BUFFER = 256
	FORMAT_MESSAGE_IGNORE_INSERTS  = 512
	FORMAT_MESSAGE_FROM_STRING     = 1024
	FORMAT_MESSAGE_FROM_HMODULE    = 2048
	FORMAT_MESSAGE_FROM_SYSTEM     = 4096
	FORMAT_MESSAGE_ARGUMENT_ARRAY  = 8192
	FORMAT_MESSAGE_MAX_WIDTH_MASK  = 255

	MAX_PATH      = 260
	MAX_LONG_PATH = 32768

	MAX_COMPUTERNAME_LENGTH = 15

	TIME_ZONE_ID_UNKNOWN  = 0
	TIME_ZONE_ID_STANDARD = 1

	TIME_ZONE_ID_DAYLIGHT = 2
	IGNORE                = 0
	INFINITE              = 0xffffffff

	WAIT_TIMEOUT   = 258
	WAIT_ABANDONED = 0x00000080
	WAIT_OBJECT_0  = 0x00000000
	WAIT_FAILED    = 0xFFFFFFFF

	CREATE_NEW_PROCESS_GROUP   = 0x00000200
	CREATE_UNICODE_ENVIRONMENT = 0x00000400

	PROCESS_TERMINATE         = 1
	PROCESS_QUERY_INFORMATION = 0x00000400
	SYNCHRONIZE               = 0x00100000

	PAGE_READONLY          = 0x02
	PAGE_READWRITE         = 0x04
	PAGE_WRITECOPY         = 0x08
	PAGE_EXECUTE_READ      = 0x20
	PAGE_EXECUTE_READWRITE = 0x40
	PAGE_EXECUTE_WRITECOPY = 0x80

	FILE_MAP_COPY    = 0x01
	FILE_MAP_WRITE   = 0x02
	FILE_MAP_READ    = 0x04
	FILE_MAP_EXECUTE = 0x20

	CTRL_C_EVENT        = 0
	CTRL_BREAK_EVENT    = 1
	CTRL_CLOSE_EVENT    = 2
	CTRL_LOGOFF_EVENT   = 5
	CTRL_SHUTDOWN_EVENT = 6
)
const (
	// flags for CreateToolhelp32Snapshot
	TH32CS_SNAPHEAPLIST = 0x01
	TH32CS_SNAPPROCESS  = 0x02
	TH32CS_SNAPTHREAD   = 0x04
	TH32CS_SNAPMODULE   = 0x08
	TH32CS_SNAPMODULE32 = 0x10
	TH32CS_SNAPALL      = TH32CS_SNAPHEAPLIST | TH32CS_SNAPMODULE | TH32CS_SNAPPROCESS | TH32CS_SNAPTHREAD
	TH32CS_INHERIT      = 0x80000000
)
const (
	// do not reorder
	FILE_NOTIFY_CHANGE_FILE_NAME = 1 << iota
	FILE_NOTIFY_CHANGE_DIR_NAME
	FILE_NOTIFY_CHANGE_ATTRIBUTES
	FILE_NOTIFY_CHANGE_SIZE
	FILE_NOTIFY_CHANGE_LAST_WRITE
	FILE_NOTIFY_CHANGE_LAST_ACCESS
	FILE_NOTIFY_CHANGE_CREATION
)
const (
	// do not reorder
	FILE_ACTION_ADDED = iota + 1
	FILE_ACTION_REMOVED
	FILE_ACTION_MODIFIED
	FILE_ACTION_RENAMED_OLD_NAME
	FILE_ACTION_RENAMED_NEW_NAME
)
const (
	// wincrypt.h
	PROV_RSA_FULL                    = 1
	PROV_RSA_SIG                     = 2
	PROV_DSS                         = 3
	PROV_FORTEZZA                    = 4
	PROV_MS_EXCHANGE                 = 5
	PROV_SSL                         = 6
	PROV_RSA_SCHANNEL                = 12
	PROV_DSS_DH                      = 13
	PROV_EC_ECDSA_SIG                = 14
	PROV_EC_ECNRA_SIG                = 15
	PROV_EC_ECDSA_FULL               = 16
	PROV_EC_ECNRA_FULL               = 17
	PROV_DH_SCHANNEL                 = 18
	PROV_SPYRUS_LYNKS                = 20
	PROV_RNG                         = 21
	PROV_INTEL_SEC                   = 22
	PROV_REPLACE_OWF                 = 23
	PROV_RSA_AES                     = 24
	CRYPT_VERIFYCONTEXT              = 0xF0000000
	CRYPT_NEWKEYSET                  = 0x00000008
	CRYPT_DELETEKEYSET               = 0x00000010
	CRYPT_MACHINE_KEYSET             = 0x00000020
	CRYPT_SILENT                     = 0x00000040
	CRYPT_DEFAULT_CONTAINER_OPTIONAL = 0x00000080

	USAGE_MATCH_TYPE_AND = 0
	USAGE_MATCH_TYPE_OR  = 1

	X509_ASN_ENCODING   = 0x00000001
	PKCS_7_ASN_ENCODING = 0x00010000

	CERT_STORE_PROV_MEMORY = 2

	CERT_STORE_ADD_ALWAYS = 4

	CERT_STORE_DEFER_CLOSE_UNTIL_LAST_FREE_FLAG = 0x00000004

	CERT_TRUST_NO_ERROR                          = 0x00000000
	CERT_TRUST_IS_NOT_TIME_VALID                 = 0x00000001
	CERT_TRUST_IS_REVOKED                        = 0x00000004
	CERT_TRUST_IS_NOT_SIGNATURE_VALID            = 0x00000008
	CERT_TRUST_IS_NOT_VALID_FOR_USAGE            = 0x00000010
	CERT_TRUST_IS_UNTRUSTED_ROOT                 = 0x00000020
	CERT_TRUST_REVOCATION_STATUS_UNKNOWN         = 0x00000040
	CERT_TRUST_IS_CYCLIC                         = 0x00000080
	CERT_TRUST_INVALID_EXTENSION                 = 0x00000100
	CERT_TRUST_INVALID_POLICY_CONSTRAINTS        = 0x00000200
	CERT_TRUST_INVALID_BASIC_CONSTRAINTS         = 0x00000400
	CERT_TRUST_INVALID_NAME_CONSTRAINTS          = 0x00000800
	CERT_TRUST_HAS_NOT_SUPPORTED_NAME_CONSTRAINT = 0x00001000
	CERT_TRUST_HAS_NOT_DEFINED_NAME_CONSTRAINT   = 0x00002000
	CERT_TRUST_HAS_NOT_PERMITTED_NAME_CONSTRAINT = 0x00004000
	CERT_TRUST_HAS_EXCLUDED_NAME_CONSTRAINT      = 0x00008000
	CERT_TRUST_IS_OFFLINE_REVOCATION             = 0x01000000
	CERT_TRUST_NO_ISSUANCE_CHAIN_POLICY          = 0x02000000
	CERT_TRUST_IS_EXPLICIT_DISTRUST              = 0x04000000
	CERT_TRUST_HAS_NOT_SUPPORTED_CRITICAL_EXT    = 0x08000000

	CERT_CHAIN_POLICY_BASE              = 1
	CERT_CHAIN_POLICY_AUTHENTICODE      = 2
	CERT_CHAIN_POLICY_AUTHENTICODE_TS   = 3
	CERT_CHAIN_POLICY_SSL               = 4
	CERT_CHAIN_POLICY_BASIC_CONSTRAINTS = 5
	CERT_CHAIN_POLICY_NT_AUTH           = 6
	CERT_CHAIN_POLICY_MICROSOFT_ROOT    = 7
	CERT_CHAIN_POLICY_EV                = 8

	CERT_E_EXPIRED       = 0x800B0101
	CERT_E_ROLE          = 0x800B0103
	CERT_E_PURPOSE       = 0x800B0106
	CERT_E_UNTRUSTEDROOT = 0x800B0109
	CERT_E_CN_NO_MATCH   = 0x800B010F

	AUTHTYPE_CLIENT = 1
	AUTHTYPE_SERVER = 2
)
const (
	GetFileExInfoStandard = 0
	GetFileExMaxInfoLevel = 1
)
const (
	// winuser.h
	SW_HIDE            = 0
	SW_NORMAL          = 1
	SW_SHOWNORMAL      = 1
	SW_SHOWMINIMIZED   = 2
	SW_SHOWMAXIMIZED   = 3
	SW_MAXIMIZE        = 3
	SW_SHOWNOACTIVATE  = 4
	SW_SHOW            = 5
	SW_MINIMIZE        = 6
	SW_SHOWMINNOACTIVE = 7
	SW_SHOWNA          = 8
	SW_RESTORE         = 9
	SW_SHOWDEFAULT     = 10
	SW_FORCEMINIMIZE   = 11
)
    ShowWindow constants

const (
	AF_UNSPEC  = 0
	AF_UNIX    = 1
	AF_INET    = 2
	AF_INET6   = 23
	AF_NETBIOS = 17

	SOCK_STREAM    = 1
	SOCK_DGRAM     = 2
	SOCK_RAW       = 3
	SOCK_SEQPACKET = 5

	IPPROTO_IP   = 0
	IPPROTO_IPV6 = 0x29
	IPPROTO_TCP  = 6
	IPPROTO_UDP  = 17

	SOL_SOCKET                = 0xffff
	SO_REUSEADDR              = 4
	SO_KEEPALIVE              = 8
	SO_DONTROUTE              = 16
	SO_BROADCAST              = 32
	SO_LINGER                 = 128
	SO_RCVBUF                 = 0x1002
	SO_SNDBUF                 = 0x1001
	SO_UPDATE_ACCEPT_CONTEXT  = 0x700b
	SO_UPDATE_CONNECT_CONTEXT = 0x7010

	IOC_OUT                            = 0x40000000
	IOC_IN                             = 0x80000000
	IOC_VENDOR                         = 0x18000000
	IOC_INOUT                          = IOC_IN | IOC_OUT
	IOC_WS2                            = 0x08000000
	SIO_GET_EXTENSION_FUNCTION_POINTER = IOC_INOUT | IOC_WS2 | 6
	SIO_KEEPALIVE_VALS                 = IOC_IN | IOC_VENDOR | 4
	SIO_UDP_CONNRESET                  = IOC_IN | IOC_VENDOR | 12

	IP_TOS             = 0x3
	IP_TTL             = 0x4
	IP_MULTICAST_IF    = 0x9
	IP_MULTICAST_TTL   = 0xa
	IP_MULTICAST_LOOP  = 0xb
	IP_ADD_MEMBERSHIP  = 0xc
	IP_DROP_MEMBERSHIP = 0xd

	IPV6_V6ONLY         = 0x1b
	IPV6_UNICAST_HOPS   = 0x4
	IPV6_MULTICAST_IF   = 0x9
	IPV6_MULTICAST_HOPS = 0xa
	IPV6_MULTICAST_LOOP = 0xb
	IPV6_JOIN_GROUP     = 0xc
	IPV6_LEAVE_GROUP    = 0xd

	SOMAXCONN = 0x7fffffff

	TCP_NODELAY = 1

	SHUT_RD   = 0
	SHUT_WR   = 1
	SHUT_RDWR = 2

	WSADESCRIPTION_LEN = 256
	WSASYS_STATUS_LEN  = 128
)
const (
	S_IFMT   = 0x1f000
	S_IFIFO  = 0x1000
	S_IFCHR  = 0x2000
	S_IFDIR  = 0x4000
	S_IFBLK  = 0x6000
	S_IFREG  = 0x8000
	S_IFLNK  = 0xa000
	S_IFSOCK = 0xc000
	S_ISUID  = 0x800
	S_ISGID  = 0x400
	S_ISVTX  = 0x200
	S_IRUSR  = 0x100
	S_IWRITE = 0x80
	S_IWUSR  = 0x80
	S_IXUSR  = 0x40
)
    Invented values to support what package os expects.

const (
	FILE_TYPE_CHAR    = 0x0002
	FILE_TYPE_DISK    = 0x0001
	FILE_TYPE_PIPE    = 0x0003
	FILE_TYPE_REMOTE  = 0x8000
	FILE_TYPE_UNKNOWN = 0x0000
)
const (
	DNS_TYPE_A       = 0x0001
	DNS_TYPE_NS      = 0x0002
	DNS_TYPE_MD      = 0x0003
	DNS_TYPE_MF      = 0x0004
	DNS_TYPE_CNAME   = 0x0005
	DNS_TYPE_SOA     = 0x0006
	DNS_TYPE_MB      = 0x0007
	DNS_TYPE_MG      = 0x0008
	DNS_TYPE_MR      = 0x0009
	DNS_TYPE_NULL    = 0x000a
	DNS_TYPE_WKS     = 0x000b
	DNS_TYPE_PTR     = 0x000c
	DNS_TYPE_HINFO   = 0x000d
	DNS_TYPE_MINFO   = 0x000e
	DNS_TYPE_MX      = 0x000f
	DNS_TYPE_TEXT    = 0x0010
	DNS_TYPE_RP      = 0x0011
	DNS_TYPE_AFSDB   = 0x0012
	DNS_TYPE_X25     = 0x0013
	DNS_TYPE_ISDN    = 0x0014
	DNS_TYPE_RT      = 0x0015
	DNS_TYPE_NSAP    = 0x0016
	DNS_TYPE_NSAPPTR = 0x0017
	DNS_TYPE_SIG     = 0x0018
	DNS_TYPE_KEY     = 0x0019
	DNS_TYPE_PX      = 0x001a
	DNS_TYPE_GPOS    = 0x001b
	DNS_TYPE_AAAA    = 0x001c
	DNS_TYPE_LOC     = 0x001d
	DNS_TYPE_NXT     = 0x001e
	DNS_TYPE_EID     = 0x001f
	DNS_TYPE_NIMLOC  = 0x0020
	DNS_TYPE_SRV     = 0x0021
	DNS_TYPE_ATMA    = 0x0022
	DNS_TYPE_NAPTR   = 0x0023
	DNS_TYPE_KX      = 0x0024
	DNS_TYPE_CERT    = 0x0025
	DNS_TYPE_A6      = 0x0026
	DNS_TYPE_DNAME   = 0x0027
	DNS_TYPE_SINK    = 0x0028
	DNS_TYPE_OPT     = 0x0029
	DNS_TYPE_DS      = 0x002B
	DNS_TYPE_RRSIG   = 0x002E
	DNS_TYPE_NSEC    = 0x002F
	DNS_TYPE_DNSKEY  = 0x0030
	DNS_TYPE_DHCID   = 0x0031
	DNS_TYPE_UINFO   = 0x0064
	DNS_TYPE_UID     = 0x0065
	DNS_TYPE_GID     = 0x0066
	DNS_TYPE_UNSPEC  = 0x0067
	DNS_TYPE_ADDRS   = 0x00f8
	DNS_TYPE_TKEY    = 0x00f9
	DNS_TYPE_TSIG    = 0x00fa
	DNS_TYPE_IXFR    = 0x00fb
	DNS_TYPE_AXFR    = 0x00fc
	DNS_TYPE_MAILB   = 0x00fd
	DNS_TYPE_MAILA   = 0x00fe
	DNS_TYPE_ALL     = 0x00ff
	DNS_TYPE_ANY     = 0x00ff
	DNS_TYPE_WINS    = 0xff01
	DNS_TYPE_WINSR   = 0xff02
	DNS_TYPE_NBSTAT  = 0xff01
)
const (
	// flags inside DNSRecord.Dw
	DnsSectionQuestion   = 0x0000
	DnsSectionAnswer     = 0x0001
	DnsSectionAuthority  = 0x0002
	DnsSectionAdditional = 0x0003
)
const (
	TF_DISCONNECT         = 1
	TF_REUSE_SOCKET       = 2
	TF_WRITE_BEHIND       = 4
	TF_USE_DEFAULT_WORKER = 0
	TF_USE_SYSTEM_THREAD  = 16
	TF_USE_KERNEL_APC     = 32
)
const (
	IFF_UP           = 1
	IFF_BROADCAST    = 2
	IFF_LOOPBACK     = 4
	IFF_POINTTOPOINT = 8
	IFF_MULTICAST    = 16
)
const (
	// do not reorder
	HKEY_CLASSES_ROOT = 0x80000000 + iota
	HKEY_CURRENT_USER
	HKEY_LOCAL_MACHINE
	HKEY_USERS
	HKEY_PERFORMANCE_DATA
	HKEY_CURRENT_CONFIG
	HKEY_DYN_DATA

	KEY_QUERY_VALUE        = 1
	KEY_SET_VALUE          = 2
	KEY_CREATE_SUB_KEY     = 4
	KEY_ENUMERATE_SUB_KEYS = 8
	KEY_NOTIFY             = 16
	KEY_CREATE_LINK        = 32
	KEY_WRITE              = 0x20006
	KEY_EXECUTE            = 0x20019
	KEY_READ               = 0x20019
	KEY_WOW64_64KEY        = 0x0100
	KEY_WOW64_32KEY        = 0x0200
	KEY_ALL_ACCESS         = 0xf003f
)
const (
	// do not reorder
	REG_NONE = iota
	REG_SZ
	REG_EXPAND_SZ
	REG_BINARY
	REG_DWORD_LITTLE_ENDIAN
	REG_DWORD_BIG_ENDIAN
	REG_LINK
	REG_MULTI_SZ
	REG_RESOURCE_LIST
	REG_FULL_RESOURCE_DESCRIPTOR
	REG_RESOURCE_REQUIREMENTS_LIST
	REG_QWORD_LITTLE_ENDIAN
	REG_DWORD = REG_DWORD_LITTLE_ENDIAN
	REG_QWORD = REG_QWORD_LITTLE_ENDIAN
)
const (
	AI_PASSIVE     = 1
	AI_CANONNAME   = 2
	AI_NUMERICHOST = 4
)
const (
	FILE_SKIP_COMPLETION_PORT_ON_SUCCESS = 1
	FILE_SKIP_SET_EVENT_ON_HANDLE        = 2
)
const (
	WSAPROTOCOL_LEN    = 255
	MAX_PROTOCOL_CHAIN = 7
	BASE_PROTOCOL      = 1
	LAYERED_PROTOCOL   = 0

	XP1_CONNECTIONLESS           = 0x00000001
	XP1_GUARANTEED_DELIVERY      = 0x00000002
	XP1_GUARANTEED_ORDER         = 0x00000004
	XP1_MESSAGE_ORIENTED         = 0x00000008
	XP1_PSEUDO_STREAM            = 0x00000010
	XP1_GRACEFUL_CLOSE           = 0x00000020
	XP1_EXPEDITED_DATA           = 0x00000040
	XP1_CONNECT_DATA             = 0x00000080
	XP1_DISCONNECT_DATA          = 0x00000100
	XP1_SUPPORT_BROADCAST        = 0x00000200
	XP1_SUPPORT_MULTIPOINT       = 0x00000400
	XP1_MULTIPOINT_CONTROL_PLANE = 0x00000800
	XP1_MULTIPOINT_DATA_PLANE    = 0x00001000
	XP1_QOS_SUPPORTED            = 0x00002000
	XP1_UNI_SEND                 = 0x00008000
	XP1_UNI_RECV                 = 0x00010000
	XP1_IFS_HANDLES              = 0x00020000
	XP1_PARTIAL_MESSAGE          = 0x00040000
	XP1_SAN_SUPPORT_SDP          = 0x00080000

	PFL_MULTIPLE_PROTO_ENTRIES  = 0x00000001
	PFL_RECOMMENDED_PROTO_ENTRY = 0x00000002
	PFL_HIDDEN                  = 0x00000004
	PFL_MATCHES_PROTOCOL_ZERO   = 0x00000008
	PFL_NETWORKDIRECT_PROVIDER  = 0x00000010
)
const (
	FSCTL_GET_REPARSE_POINT          = 0x900A8
	MAXIMUM_REPARSE_DATA_BUFFER_SIZE = 16 * 1024

	IO_REPARSE_TAG_SYMLINK       = 0xA000000C
	SYMBOLIC_LINK_FLAG_DIRECTORY = 0x1
)
const APPLICATION_ERROR = 1 << 29
    Windows reserves errors >= 1<<29 for application use.

const (
	DNS_INFO_NO_RECORDS = 0x251D
)
const ImplementsGetwd = true
const InvalidHandle = ^Handle(0)
const MAXLEN_IFDESCR = 256
const MAXLEN_PHYSADDR = 8
const MAX_ADAPTER_ADDRESS_LENGTH = 8
const MAX_ADAPTER_DESCRIPTION_LENGTH = 128
const MAX_ADAPTER_NAME_LENGTH = 256
const MAX_INTERFACE_NAME_LEN = 256
const SIO_GET_INTERFACE_LIST = 0x4004747F
const UNIX_PATH_MAX = 108 // defined in afunix.h

VARIABLES

var (
	Stdin  = getStdHandle(STD_INPUT_HANDLE)
	Stdout = getStdHandle(STD_OUTPUT_HANDLE)
	Stderr = getStdHandle(STD_ERROR_HANDLE)
)
var (
	OID_PKIX_KP_SERVER_AUTH = []byte("1.3.6.1.5.5.7.3.1\x00")
	OID_SERVER_GATED_CRYPTO = []byte("1.3.6.1.4.1.311.10.3.3\x00")
	OID_SGC_NETSCAPE        = []byte("2.16.840.1.113730.4.1\x00")
)
var ForkLock sync.RWMutex
    ForkLock is not used on Windows.

var SocketDisableIPv6 bool
    For testing: clients can set this flag to force creation of IPv6 sockets to
    return EAFNOSUPPORT.

var WSAID_CONNECTEX = GUID{
	0x25a207b9,
	0xddf3,
	0x4660,
	[8]byte{0x8e, 0xe9, 0x76, 0xe5, 0x8c, 0x74, 0x06, 0x3e},
}

FUNCTIONS

func Accept(fd Handle) (nfd Handle, sa Sockaddr, err error)
func AcceptEx(ls Handle, as Handle, buf *byte, rxdatalen uint32, laddrlen uint32, raddrlen uint32, recvd *uint32, overlapped *Overlapped) (err error)
func Bind(fd Handle, sa Sockaddr) (err error)
func BytePtrFromString(s string) (*byte, error)
    BytePtrFromString returns a pointer to a NUL-terminated array of bytes
    containing the text of s. If s contains a NUL byte at any location,
    it returns (nil, EINVAL).

func ByteSliceFromString(s string) ([]byte, error)
    ByteSliceFromString returns a NUL-terminated slice of bytes containing
    the text of s. If s contains a NUL byte at any location, it returns (nil,
    EINVAL).

func CancelIo(s Handle) (err error)
func CancelIoEx(s Handle, o *Overlapped) (err error)
func CertAddCertificateContextToStore(store Handle, certContext *CertContext, addDisposition uint32, storeContext **CertContext) (err error)
func CertCloseStore(store Handle, flags uint32) (err error)
func CertCreateCertificateContext(certEncodingType uint32, certEncoded *byte, encodedLen uint32) (context *CertContext, err error)
func CertEnumCertificatesInStore(store Handle, prevContext *CertContext) (context *CertContext, err error)
func CertFreeCertificateChain(ctx *CertChainContext)
func CertFreeCertificateContext(ctx *CertContext) (err error)
func CertGetCertificateChain(engine Handle, leaf *CertContext, time *Filetime, additionalStore Handle, para *CertChainPara, flags uint32, reserved uintptr, chainCtx **CertChainContext) (err error)
func CertOpenStore(storeProvider uintptr, msgAndCertEncodingType uint32, cryptProv uintptr, flags uint32, para uintptr) (handle Handle, err error)
func CertOpenSystemStore(hprov Handle, name *uint16) (store Handle, err error)
func CertVerifyCertificateChainPolicy(policyOID uintptr, chain *CertChainContext, para *CertChainPolicyPara, status *CertChainPolicyStatus) (err error)
func Chdir(path string) (err error)
func Chmod(path string, mode uint32) (err error)
func Chown(path string, uid int, gid int) (err error)
func Clearenv()
func Close(fd Handle) (err error)
func CloseHandle(handle Handle) (err error)
func CloseOnExec(fd Handle)
func Closesocket(s Handle) (err error)
func CommandLineToArgv(cmd *uint16, argc *int32) (argv *[8192]*[8192]uint16, err error)
func ComputerName() (name string, err error)
func Connect(fd Handle, sa Sockaddr) (err error)
func ConnectEx(fd Handle, sa Sockaddr, sendBuf *byte, sendDataLen uint32, bytesSent *uint32, overlapped *Overlapped) error
func ConvertSidToStringSid(sid *SID, stringSid **uint16) (err error)
func ConvertStringSidToSid(stringSid *uint16, sid **SID) (err error)
func CopySid(destSidLen uint32, destSid *SID, srcSid *SID) (err error)
func CreateDirectory(path *uint16, sa *SecurityAttributes) (err error)
func CreateFile(name *uint16, access uint32, mode uint32, sa *SecurityAttributes, createmode uint32, attrs uint32, templatefile int32) (handle Handle, err error)
func CreateFileMapping(fhandle Handle, sa *SecurityAttributes, prot uint32, maxSizeHigh uint32, maxSizeLow uint32, name *uint16) (handle Handle, err error)
func CreateHardLink(filename *uint16, existingfilename *uint16, reserved uintptr) (err error)
func CreateIoCompletionPort(filehandle Handle, cphandle Handle, key uint32, threadcnt uint32) (Handle, error)
    Deprecated: CreateIoCompletionPort has the wrong function signature.
    Use x/sys/windows.CreateIoCompletionPort.

func CreatePipe(readhandle *Handle, writehandle *Handle, sa *SecurityAttributes, size uint32) (err error)
func CreateProcess(appName *uint16, commandLine *uint16, procSecurity *SecurityAttributes, threadSecurity *SecurityAttributes, inheritHandles bool, creationFlags uint32, env *uint16, currentDir *uint16, startupInfo *StartupInfo, outProcInfo *ProcessInformation) (err error)
func CreateProcessAsUser(token Token, appName *uint16, commandLine *uint16, procSecurity *SecurityAttributes, threadSecurity *SecurityAttributes, inheritHandles bool, creationFlags uint32, env *uint16, currentDir *uint16, startupInfo *StartupInfo, outProcInfo *ProcessInformation) (err error)
func CreateSymbolicLink(symlinkfilename *uint16, targetfilename *uint16, flags uint32) (err error)
func CreateToolhelp32Snapshot(flags uint32, processId uint32) (handle Handle, err error)
func CryptAcquireContext(provhandle *Handle, container *uint16, provider *uint16, provtype uint32, flags uint32) (err error)
func CryptGenRandom(provhandle Handle, buflen uint32, buf *byte) (err error)
func CryptReleaseContext(provhandle Handle, flags uint32) (err error)
func DeleteFile(path *uint16) (err error)
func DeviceIoControl(handle Handle, ioControlCode uint32, inBuffer *byte, inBufferSize uint32, outBuffer *byte, outBufferSize uint32, bytesReturned *uint32, overlapped *Overlapped) (err error)
func DnsNameCompare(name1 *uint16, name2 *uint16) (same bool)
func DnsQuery(name string, qtype uint16, options uint32, extra *byte, qrs **DNSRecord, pr *byte) (status error)
func DnsRecordListFree(rl *DNSRecord, freetype uint32)
func DuplicateHandle(hSourceProcessHandle Handle, hSourceHandle Handle, hTargetProcessHandle Handle, lpTargetHandle *Handle, dwDesiredAccess uint32, bInheritHandle bool, dwOptions uint32) (err error)
func Environ() []string
func EscapeArg(s string) string
    EscapeArg rewrites command line argument s as prescribed in
    https://msdn.microsoft.com/en-us/library/ms880421. This function returns ""
    (2 double quotes) if s is empty. Alternatively, these transformations are
    done:
      - every back slash (\) is doubled, but only if immediately followed by
        double quote (");
      - every double quote (") is escaped by back slash (\);
      - finally, s is wrapped with double quotes (arg -> "arg"), but only if
        there is space or tab inside s.

func Exec(argv0 string, argv []string, envv []string) (err error)
func Exit(code int)
func ExitProcess(exitcode uint32)
func Fchdir(fd Handle) (err error)
func Fchmod(fd Handle, mode uint32) (err error)
func Fchown(fd Handle, uid int, gid int) (err error)
func FindClose(handle Handle) (err error)
func FindFirstFile(name *uint16, data *Win32finddata) (handle Handle, err error)
func FindNextFile(handle Handle, data *Win32finddata) (err error)
func FlushFileBuffers(handle Handle) (err error)
func FlushViewOfFile(addr uintptr, length uintptr) (err error)
func FormatMessage(flags uint32, msgsrc uint32, msgid uint32, langid uint32, buf []uint16, args *byte) (n uint32, err error)
    FormatMessage is deprecated (msgsrc should be uintptr, not uint32, but can
    not be changed due to the Go 1 compatibility guarantee).

    Deprecated: Use FormatMessage from golang.org/x/sys/windows instead.

func FreeAddrInfoW(addrinfo *AddrinfoW)
func FreeEnvironmentStrings(envs *uint16) (err error)
func FreeLibrary(handle Handle) (err error)
func Fsync(fd Handle) (err error)
func Ftruncate(fd Handle, length int64) (err error)
func FullPath(name string) (path string, err error)
    FullPath retrieves the full path of the specified file.

func GetAcceptExSockaddrs(buf *byte, rxdatalen uint32, laddrlen uint32, raddrlen uint32, lrsa **RawSockaddrAny, lrsalen *int32, rrsa **RawSockaddrAny, rrsalen *int32)
func GetAdaptersInfo(ai *IpAdapterInfo, ol *uint32) (errcode error)
func GetAddrInfoW(nodename *uint16, servicename *uint16, hints *AddrinfoW, result **AddrinfoW) (sockerr error)
func GetCommandLine() (cmd *uint16)
func GetComputerName(buf *uint16, n *uint32) (err error)
func GetConsoleMode(console Handle, mode *uint32) (err error)
func GetCurrentDirectory(buflen uint32, buf *uint16) (n uint32, err error)
func GetCurrentProcess() (pseudoHandle Handle, err error)
func GetEnvironmentStrings() (envs *uint16, err error)
func GetEnvironmentVariable(name *uint16, buffer *uint16, size uint32) (n uint32, err error)
func GetExitCodeProcess(handle Handle, exitcode *uint32) (err error)
func GetFileAttributes(name *uint16) (attrs uint32, err error)
func GetFileAttributesEx(name *uint16, level uint32, info *byte) (err error)
func GetFileInformationByHandle(handle Handle, data *ByHandleFileInformation) (err error)
func GetFileType(filehandle Handle) (n uint32, err error)
func GetFullPathName(path *uint16, buflen uint32, buf *uint16, fname **uint16) (n uint32, err error)
func GetHostByName(name string) (h *Hostent, err error)
func GetIfEntry(pIfRow *MibIfRow) (errcode error)
func GetLastError() (lasterr error)
func GetLengthSid(sid *SID) (len uint32)
func GetLongPathName(path *uint16, buf *uint16, buflen uint32) (n uint32, err error)
func GetProcAddress(module Handle, procname string) (proc uintptr, err error)
func GetProcessTimes(handle Handle, creationTime *Filetime, exitTime *Filetime, kernelTime *Filetime, userTime *Filetime) (err error)
func GetProtoByName(name string) (p *Protoent, err error)
func GetQueuedCompletionStatus(cphandle Handle, qty *uint32, key *uint32, overlapped **Overlapped, timeout uint32) error
    Deprecated: GetQueuedCompletionStatus has the wrong function signature.
    Use x/sys/windows.GetQueuedCompletionStatus.

func GetServByName(name string, proto string) (s *Servent, err error)
func GetShortPathName(longpath *uint16, shortpath *uint16, buflen uint32) (n uint32, err error)
func GetStartupInfo(startupInfo *StartupInfo) error
func GetStdHandle(stdhandle int) (handle Handle, err error)
func GetSystemTimeAsFileTime(time *Filetime)
func GetTempPath(buflen uint32, buf *uint16) (n uint32, err error)
func GetTimeZoneInformation(tzi *Timezoneinformation) (rc uint32, err error)
func GetTokenInformation(t Token, infoClass uint32, info *byte, infoLen uint32, returnedLen *uint32) (err error)
func GetUserNameEx(nameFormat uint32, nameBuffre *uint16, nSize *uint32) (err error)
func GetUserProfileDirectory(t Token, dir *uint16, dirLen *uint32) (err error)
func GetVersion() (ver uint32, err error)
func Getegid() (egid int)
func Getenv(key string) (value string, found bool)
func Geteuid() (euid int)
func Getgid() (gid int)
func Getgroups() (gids []int, err error)
func Getpagesize() int
func Getpeername(fd Handle) (sa Sockaddr, err error)
func Getpid() (pid int)
func Getppid() (ppid int)
func Getsockname(fd Handle) (sa Sockaddr, err error)
func Getsockopt(s Handle, level int32, optname int32, optval *byte, optlen *int32) (err error)
func GetsockoptInt(fd Handle, level, opt int) (int, error)
func Gettimeofday(tv *Timeval) (err error)
func Getuid() (uid int)
func Getwd() (wd string, err error)
func Lchown(path string, uid int, gid int) (err error)
func Link(oldpath, newpath string) (err error)
    TODO(brainman): fix all needed for os

func Listen(s Handle, n int) (err error)
func LoadCancelIoEx() error
func LoadConnectEx() error
func LoadCreateSymbolicLink() error
func LoadDLL(name string) (*DLL, error)
    LoadDLL loads the named DLL file into memory.

    If name is not an absolute path and is not a known system DLL used by Go,
    Windows will search for the named DLL in many locations, causing potential
    DLL preloading attacks.

    Use LazyDLL in golang.org/x/sys/windows for a secure way to load system
    DLLs.

func LoadGetAddrInfo() error
func LoadLibrary(libname string) (handle Handle, err error)
func LoadSetFileCompletionNotificationModes() error
func LocalFree(hmem Handle) (handle Handle, err error)
func LookupAccountName(systemName *uint16, accountName *uint16, sid *SID, sidLen *uint32, refdDomainName *uint16, refdDomainNameLen *uint32, use *uint32) (err error)
func LookupAccountSid(systemName *uint16, sid *SID, name *uint16, nameLen *uint32, refdDomainName *uint16, refdDomainNameLen *uint32, use *uint32) (err error)
func LookupSID(system, account string) (sid *SID, domain string, accType uint32, err error)
    LookupSID retrieves a security identifier sid for the account and the name
    of the domain on which the account was found. System specify target computer
    to search.

func MapViewOfFile(handle Handle, access uint32, offsetHigh uint32, offsetLow uint32, length uintptr) (addr uintptr, err error)
func Mkdir(path string, mode uint32) (err error)
func MoveFile(from *uint16, to *uint16) (err error)
func NetApiBufferFree(buf *byte) (neterr error)
func NetGetJoinInformation(server *uint16, name **uint16, bufType *uint32) (neterr error)
func NetUserGetInfo(serverName *uint16, userName *uint16, level uint32, buf **byte) (neterr error)
func NewCallback(fn any) uintptr
    NewCallback converts a Go function to a function pointer conforming to the
    stdcall calling convention. This is useful when interoperating with Windows
    code requiring callbacks. The argument is expected to be a function with
    one uintptr-sized result. The function must not have arguments with size
    larger than the size of uintptr. Only a limited number of callbacks may be
    created in a single Go process, and any memory allocated for these callbacks
    is never released. Between NewCallback and NewCallbackCDecl, at least 1024
    callbacks can always be created.

func NewCallbackCDecl(fn any) uintptr
    NewCallbackCDecl converts a Go function to a function pointer conforming
    to the cdecl calling convention. This is useful when interoperating with
    Windows code requiring callbacks. The argument is expected to be a function
    with one uintptr-sized result. The function must not have arguments with
    size larger than the size of uintptr. Only a limited number of callbacks
    may be created in a single Go process, and any memory allocated for these
    callbacks is never released. Between NewCallback and NewCallbackCDecl,
    at least 1024 callbacks can always be created.

func Ntohs(netshort uint16) (u uint16)
func Open(name string, flag int, perm uint32) (fd Handle, err error)
func OpenCurrentProcessToken() (Token, error)
    OpenCurrentProcessToken opens the access token associated with current
    process.

func OpenProcess(da uint32, inheritHandle bool, pid uint32) (handle Handle, err error)
func OpenProcessToken(h Handle, access uint32, token *Token) (err error)
func Pipe(p []Handle) (err error)
func PostQueuedCompletionStatus(cphandle Handle, qty uint32, key uint32, overlapped *Overlapped) error
    Deprecated: PostQueuedCompletionStatus has the wrong function signature.
    Use x/sys/windows.PostQueuedCompletionStatus.

func Process32First(snapshot Handle, procEntry *ProcessEntry32) (err error)
func Process32Next(snapshot Handle, procEntry *ProcessEntry32) (err error)
func Read(fd Handle, p []byte) (n int, err error)
func ReadConsole(console Handle, buf *uint16, toread uint32, read *uint32, inputControl *byte) (err error)
func ReadDirectoryChanges(handle Handle, buf *byte, buflen uint32, watchSubTree bool, mask uint32, retlen *uint32, overlapped *Overlapped, completionRoutine uintptr) (err error)
func ReadFile(fd Handle, p []byte, done *uint32, overlapped *Overlapped) error
func Readlink(path string, buf []byte) (n int, err error)
    Readlink returns the destination of the named symbolic link.

func Recvfrom(fd Handle, p []byte, flags int) (n int, from Sockaddr, err error)
func RegCloseKey(key Handle) (regerrno error)
func RegEnumKeyEx(key Handle, index uint32, name *uint16, nameLen *uint32, reserved *uint32, class *uint16, classLen *uint32, lastWriteTime *Filetime) (regerrno error)
    RegEnumKeyEx enumerates the subkeys of an open registry key. Each call
    retrieves information about one subkey. name is a buffer that should
    be large enough to hold the name of the subkey plus a null terminating
    character. nameLen is its length. On return, nameLen will contain the actual
    length of the subkey.

    Should name not be large enough to hold the subkey, this function will
    return ERROR_MORE_DATA, and must be called again with an appropriately sized
    buffer.

    reserved must be nil. class and classLen behave like name and nameLen but
    for the class of the subkey, except that they are optional. lastWriteTime,
    if not nil, will be populated with the time the subkey was last written.

    The caller must enumerate all subkeys in order. That is RegEnumKeyEx
    must be called with index starting at 0, incrementing the index until the
    function returns ERROR_NO_MORE_ITEMS, or with the index of the last subkey
    (obtainable from RegQueryInfoKey), decrementing until index 0 is enumerated.

    Successive calls to this API must happen on the same OS thread, so call
    runtime.LockOSThread before calling this function.

func RegOpenKeyEx(key Handle, subkey *uint16, options uint32, desiredAccess uint32, result *Handle) (regerrno error)
func RegQueryInfoKey(key Handle, class *uint16, classLen *uint32, reserved *uint32, subkeysLen *uint32, maxSubkeyLen *uint32, maxClassLen *uint32, valuesLen *uint32, maxValueNameLen *uint32, maxValueLen *uint32, saLen *uint32, lastWriteTime *Filetime) (regerrno error)
func RegQueryValueEx(key Handle, name *uint16, reserved *uint32, valtype *uint32, buf *byte, buflen *uint32) (regerrno error)
func RemoveDirectory(path *uint16) (err error)
func Rename(oldpath, newpath string) (err error)
func Rmdir(path string) (err error)
func Seek(fd Handle, offset int64, whence int) (newoffset int64, err error)
func Sendto(fd Handle, p []byte, flags int, to Sockaddr) (err error)
func SetCurrentDirectory(path *uint16) (err error)
func SetEndOfFile(handle Handle) (err error)
func SetEnvironmentVariable(name *uint16, value *uint16) (err error)
func SetFileAttributes(name *uint16, attrs uint32) (err error)
func SetFileCompletionNotificationModes(handle Handle, flags uint8) (err error)
func SetFilePointer(handle Handle, lowoffset int32, highoffsetptr *int32, whence uint32) (newlowoffset uint32, err error)
func SetFileTime(handle Handle, ctime *Filetime, atime *Filetime, wtime *Filetime) (err error)
func SetHandleInformation(handle Handle, mask uint32, flags uint32) (err error)
func SetNonblock(fd Handle, nonblocking bool) (err error)
func Setenv(key, value string) error
func Setsockopt(s Handle, level int32, optname int32, optval *byte, optlen int32) (err error)
func SetsockoptIPMreq(fd Handle, level, opt int, mreq *IPMreq) (err error)
func SetsockoptIPv6Mreq(fd Handle, level, opt int, mreq *IPv6Mreq) (err error)
func SetsockoptInet4Addr(fd Handle, level, opt int, value [4]byte) (err error)
func SetsockoptInt(fd Handle, level, opt int, value int) (err error)
func SetsockoptLinger(fd Handle, level, opt int, l *Linger) (err error)
func SetsockoptTimeval(fd Handle, level, opt int, tv *Timeval) (err error)
func Shutdown(fd Handle, how int) (err error)
func Socket(domain, typ, proto int) (fd Handle, err error)
func StartProcess(argv0 string, argv []string, attr *ProcAttr) (pid int, handle uintptr, err error)
func StringBytePtr(s string) *byte
    StringBytePtr returns a pointer to a NUL-terminated array of bytes. If s
    contains a NUL byte this function panics instead of returning an error.

    Deprecated: Use BytePtrFromString instead.

func StringByteSlice(s string) []byte
    StringByteSlice converts a string to a NUL-terminated []byte, If s contains
    a NUL byte this function panics instead of returning an error.

    Deprecated: Use ByteSliceFromString instead.

func StringToSid(s string) (*SID, error)
    StringToSid converts a string-format security identifier sid into a valid,
    functional sid.

func StringToUTF16(s string) []uint16
    StringToUTF16 returns the UTF-16 encoding of the UTF-8 string s, with a
    terminating NUL added. If s contains a NUL byte this function panics instead
    of returning an error.

    Deprecated: Use UTF16FromString instead.

func StringToUTF16Ptr(s string) *uint16
    StringToUTF16Ptr returns pointer to the UTF-16 encoding of the UTF-8 string
    s, with a terminating NUL added. If s contains a NUL byte this function
    panics instead of returning an error.

    Deprecated: Use UTF16PtrFromString instead.

func Symlink(path, link string) (err error)
func Syscall(trap, nargs, a1, a2, a3 uintptr) (r1, r2 uintptr, err Errno)
    Deprecated: Use SyscallN instead.

func Syscall12(trap, nargs, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12 uintptr) (r1, r2 uintptr, err Errno)
    Deprecated: Use SyscallN instead.

func Syscall15(trap, nargs, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15 uintptr) (r1, r2 uintptr, err Errno)
    Deprecated: Use SyscallN instead.

func Syscall18(trap, nargs, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18 uintptr) (r1, r2 uintptr, err Errno)
    Deprecated: Use SyscallN instead.

func Syscall6(trap, nargs, a1, a2, a3, a4, a5, a6 uintptr) (r1, r2 uintptr, err Errno)
    Deprecated: Use SyscallN instead.

func Syscall9(trap, nargs, a1, a2, a3, a4, a5, a6, a7, a8, a9 uintptr) (r1, r2 uintptr, err Errno)
    Deprecated: Use SyscallN instead.

func SyscallN(p uintptr, args ...uintptr) (r1, r2 uintptr, err Errno)
    SyscallN executes procedure p with arguments args.

    See Proc.Call for more information.

func TerminateProcess(handle Handle, exitcode uint32) (err error)
func TimespecToNsec(ts Timespec) int64
func TranslateAccountName(username string, from, to uint32, initSize int) (string, error)
    TranslateAccountName converts a directory service object name from one
    format to another.

func TranslateName(accName *uint16, accNameFormat uint32, desiredNameFormat uint32, translatedName *uint16, nSize *uint32) (err error)
func TransmitFile(s Handle, handle Handle, bytesToWrite uint32, bytsPerSend uint32, overlapped *Overlapped, transmitFileBuf *TransmitFileBuffers, flags uint32) (err error)
func UTF16FromString(s string) ([]uint16, error)
    UTF16FromString returns the UTF-16 encoding of the UTF-8 string s,
    with a terminating NUL added. If s contains a NUL byte at any location,
    it returns (nil, EINVAL). Unpaired surrogates are encoded using WTF-8.

func UTF16PtrFromString(s string) (*uint16, error)
    UTF16PtrFromString returns pointer to the UTF-16 encoding of the UTF-8
    string s, with a terminating NUL added. If s contains a NUL byte at any
    location, it returns (nil, EINVAL). Unpaired surrogates are encoded using
    WTF-8.

func UTF16ToString(s []uint16) string
    UTF16ToString returns the UTF-8 encoding of the UTF-16 sequence s, with a
    terminating NUL removed. Unpaired surrogates are decoded using WTF-8 instead
    of UTF-8 encoding.

func Unlink(path string) (err error)
func UnmapViewOfFile(addr uintptr) (err error)
func Unsetenv(key string) error
func Utimes(path string, tv []Timeval) (err error)
func UtimesNano(path string, ts []Timespec) (err error)
func VirtualLock(addr uintptr, length uintptr) (err error)
func VirtualUnlock(addr uintptr, length uintptr) (err error)
func WSACleanup() (err error)
func WSAEnumProtocols(protocols *int32, protocolBuffer *WSAProtocolInfo, bufferLength *uint32) (n int32, err error)
func WSAIoctl(s Handle, iocc uint32, inbuf *byte, cbif uint32, outbuf *byte, cbob uint32, cbbr *uint32, overlapped *Overlapped, completionRoutine uintptr) (err error)
func WSARecv(s Handle, bufs *WSABuf, bufcnt uint32, recvd *uint32, flags *uint32, overlapped *Overlapped, croutine *byte) (err error)
func WSARecvFrom(s Handle, bufs *WSABuf, bufcnt uint32, recvd *uint32, flags *uint32, from *RawSockaddrAny, fromlen *int32, overlapped *Overlapped, croutine *byte) (err error)
func WSASend(s Handle, bufs *WSABuf, bufcnt uint32, sent *uint32, flags uint32, overlapped *Overlapped, croutine *byte) (err error)
func WSASendTo(s Handle, bufs *WSABuf, bufcnt uint32, sent *uint32, flags uint32, to *RawSockaddrAny, tolen int32, overlapped *Overlapped, croutine *byte) (err error)
func WSASendto(s Handle, bufs *WSABuf, bufcnt uint32, sent *uint32, flags uint32, to Sockaddr, overlapped *Overlapped, croutine *byte) (err error)
func WSAStartup(verreq uint32, data *WSAData) (sockerr error)
func WaitForSingleObject(handle Handle, waitMilliseconds uint32) (event uint32, err error)
func Write(fd Handle, p []byte) (n int, err error)
func WriteConsole(console Handle, buf *uint16, towrite uint32, written *uint32, reserved *byte) (err error)
func WriteFile(fd Handle, p []byte, done *uint32, overlapped *Overlapped) error

TYPES

type AddrinfoW struct {
	Flags     int32
	Family    int32
	Socktype  int32
	Protocol  int32
	Addrlen   uintptr
	Canonname *uint16
	Addr      Pointer
	Next      *AddrinfoW
}

type ByHandleFileInformation struct {
	FileAttributes     uint32
	CreationTime       Filetime
	LastAccessTime     Filetime
	LastWriteTime      Filetime
	VolumeSerialNumber uint32
	FileSizeHigh       uint32
	FileSizeLow        uint32
	NumberOfLinks      uint32
	FileIndexHigh      uint32
	FileIndexLow       uint32
}

type CertChainContext struct {
	Size                       uint32
	TrustStatus                CertTrustStatus
	ChainCount                 uint32
	Chains                     **CertSimpleChain
	LowerQualityChainCount     uint32
	LowerQualityChains         **CertChainContext
	HasRevocationFreshnessTime uint32
	RevocationFreshnessTime    uint32
}

type CertChainElement struct {
	Size              uint32
	CertContext       *CertContext
	TrustStatus       CertTrustStatus
	RevocationInfo    *CertRevocationInfo
	IssuanceUsage     *CertEnhKeyUsage
	ApplicationUsage  *CertEnhKeyUsage
	ExtendedErrorInfo *uint16
}

type CertChainPara struct {
	Size                         uint32
	RequestedUsage               CertUsageMatch
	RequstedIssuancePolicy       CertUsageMatch
	URLRetrievalTimeout          uint32
	CheckRevocationFreshnessTime uint32
	RevocationFreshnessTime      uint32
	CacheResync                  *Filetime
}

type CertChainPolicyPara struct {
	Size            uint32
	Flags           uint32
	ExtraPolicyPara Pointer
}

type CertChainPolicyStatus struct {
	Size              uint32
	Error             uint32
	ChainIndex        uint32
	ElementIndex      uint32
	ExtraPolicyStatus Pointer
}

type CertContext struct {
	EncodingType uint32
	EncodedCert  *byte
	Length       uint32
	CertInfo     *CertInfo
	Store        Handle
}

type CertEnhKeyUsage struct {
	Length           uint32
	UsageIdentifiers **byte
}

type CertInfo struct {
}

type CertRevocationCrlInfo struct {
}

type CertRevocationInfo struct {
	Size             uint32
	RevocationResult uint32
	RevocationOid    *byte
	OidSpecificInfo  Pointer
	HasFreshnessTime uint32
	FreshnessTime    uint32
	CrlInfo          *CertRevocationCrlInfo
}

type CertSimpleChain struct {
	Size                       uint32
	TrustStatus                CertTrustStatus
	NumElements                uint32
	Elements                   **CertChainElement
	TrustListInfo              *CertTrustListInfo
	HasRevocationFreshnessTime uint32
	RevocationFreshnessTime    uint32
}

type CertTrustListInfo struct {
}

type CertTrustStatus struct {
	ErrorStatus uint32
	InfoStatus  uint32
}

type CertUsageMatch struct {
	Type  uint32
	Usage CertEnhKeyUsage
}

type Conn interface {
	// SyscallConn returns a raw network connection.
	SyscallConn() (RawConn, error)
}
    Conn is implemented by some types in the net and os packages to provide
    access to the underlying file descriptor or handle.

type DLL struct {
	Name   string
	Handle Handle
}
    A DLL implements access to a single DLL.

func MustLoadDLL(name string) *DLL
    MustLoadDLL is like LoadDLL but panics if load operation fails.

func (d *DLL) FindProc(name string) (proc *Proc, err error)
    FindProc searches DLL d for procedure named name and returns *Proc if found.
    It returns an error if search fails.

func (d *DLL) MustFindProc(name string) *Proc
    MustFindProc is like DLL.FindProc but panics if search fails.

func (d *DLL) Release() (err error)
    Release unloads DLL d from memory.

type DLLError struct {
	Err     error
	ObjName string
	Msg     string
}
    DLLError describes reasons for DLL load failures.

func (e *DLLError) Error() string

func (e *DLLError) Unwrap() error

type DNSMXData struct {
	NameExchange *uint16
	Preference   uint16
	Pad          uint16
}

type DNSPTRData struct {
	Host *uint16
}

type DNSRecord struct {
	Next     *DNSRecord
	Name     *uint16
	Type     uint16
	Length   uint16
	Dw       uint32
	Ttl      uint32
	Reserved uint32
	Data     [40]byte
}

type DNSSRVData struct {
	Target   *uint16
	Priority uint16
	Weight   uint16
	Port     uint16
	Pad      uint16
}

type DNSTXTData struct {
	StringCount uint16
	StringArray [1]*uint16
}

type Errno uintptr
    Errno is the Windows error number.

    Errno values can be tested against error values using errors.Is. For
    example:

        _, _, err := syscall.Syscall(...)
        if errors.Is(err, fs.ErrNotExist) ...

const (
	// Windows errors.
	ERROR_FILE_NOT_FOUND      Errno = 2
	ERROR_PATH_NOT_FOUND      Errno = 3
	ERROR_ACCESS_DENIED       Errno = 5
	ERROR_NO_MORE_FILES       Errno = 18
	ERROR_HANDLE_EOF          Errno = 38
	ERROR_NETNAME_DELETED     Errno = 64
	ERROR_FILE_EXISTS         Errno = 80
	ERROR_BROKEN_PIPE         Errno = 109
	ERROR_BUFFER_OVERFLOW     Errno = 111
	ERROR_INSUFFICIENT_BUFFER Errno = 122
	ERROR_MOD_NOT_FOUND       Errno = 126
	ERROR_PROC_NOT_FOUND      Errno = 127
	ERROR_DIR_NOT_EMPTY       Errno = 145
	ERROR_ALREADY_EXISTS      Errno = 183
	ERROR_ENVVAR_NOT_FOUND    Errno = 203
	ERROR_MORE_DATA           Errno = 234
	ERROR_OPERATION_ABORTED   Errno = 995
	ERROR_IO_PENDING          Errno = 997
	ERROR_NOT_FOUND           Errno = 1168
	ERROR_PRIVILEGE_NOT_HELD  Errno = 1314
	WSAEACCES                 Errno = 10013
	WSAENOPROTOOPT            Errno = 10042
	WSAECONNABORTED           Errno = 10053
	WSAECONNRESET             Errno = 10054
)
const (
	ENOENT  Errno = ERROR_FILE_NOT_FOUND
	ENOTDIR Errno = ERROR_PATH_NOT_FOUND
)
    Go names for Windows errors.

const (
	E2BIG Errno = APPLICATION_ERROR + iota
	EACCES
	EADDRINUSE
	EADDRNOTAVAIL
	EADV
	EAFNOSUPPORT
	EAGAIN
	EALREADY
	EBADE
	EBADF
	EBADFD
	EBADMSG
	EBADR
	EBADRQC
	EBADSLT
	EBFONT
	EBUSY
	ECANCELED
	ECHILD
	ECHRNG
	ECOMM
	ECONNABORTED
	ECONNREFUSED
	ECONNRESET
	EDEADLK
	EDEADLOCK
	EDESTADDRREQ
	EDOM
	EDOTDOT
	EDQUOT
	EEXIST
	EFAULT
	EFBIG
	EHOSTDOWN
	EHOSTUNREACH
	EIDRM
	EILSEQ
	EINPROGRESS
	EINTR
	EINVAL
	EIO
	EISCONN
	EISDIR
	EISNAM
	EKEYEXPIRED
	EKEYREJECTED
	EKEYREVOKED
	EL2HLT
	EL2NSYNC
	EL3HLT
	EL3RST
	ELIBACC
	ELIBBAD
	ELIBEXEC
	ELIBMAX
	ELIBSCN
	ELNRNG
	ELOOP
	EMEDIUMTYPE
	EMFILE
	EMLINK
	EMSGSIZE
	EMULTIHOP
	ENAMETOOLONG
	ENAVAIL
	ENETDOWN
	ENETRESET
	ENETUNREACH
	ENFILE
	ENOANO
	ENOBUFS
	ENOCSI
	ENODATA
	ENODEV
	ENOEXEC
	ENOKEY
	ENOLCK
	ENOLINK
	ENOMEDIUM
	ENOMEM
	ENOMSG
	ENONET
	ENOPKG
	ENOPROTOOPT
	ENOSPC
	ENOSR
	ENOSTR
	ENOSYS
	ENOTBLK
	ENOTCONN
	ENOTEMPTY
	ENOTNAM
	ENOTRECOVERABLE
	ENOTSOCK
	ENOTSUP
	ENOTTY
	ENOTUNIQ
	ENXIO
	EOPNOTSUPP
	EOVERFLOW
	EOWNERDEAD
	EPERM
	EPFNOSUPPORT
	EPIPE
	EPROTO
	EPROTONOSUPPORT
	EPROTOTYPE
	ERANGE
	EREMCHG
	EREMOTE
	EREMOTEIO
	ERESTART
	EROFS
	ESHUTDOWN
	ESOCKTNOSUPPORT
	ESPIPE
	ESRCH
	ESRMNT
	ESTALE
	ESTRPIPE
	ETIME
	ETIMEDOUT
	ETOOMANYREFS
	ETXTBSY
	EUCLEAN
	EUNATCH
	EUSERS
	EWOULDBLOCK
	EXDEV
	EXFULL
	EWINDOWS
)
    Invented values to support what package os and others expects.

func (e Errno) Error() string

func (e Errno) Is(target error) bool

func (e Errno) Temporary() bool

func (e Errno) Timeout() bool

type FileNotifyInformation struct {
	NextEntryOffset uint32
	Action          uint32
	FileNameLength  uint32
	FileName        uint16
}

type Filetime struct {
	LowDateTime  uint32
	HighDateTime uint32
}

func NsecToFiletime(nsec int64) (ft Filetime)

func (ft *Filetime) Nanoseconds() int64
    Nanoseconds returns Filetime ft in nanoseconds since Epoch (00:00:00 UTC,
    January 1, 1970).

type GUID struct {
	Data1 uint32
	Data2 uint16
	Data3 uint16
	Data4 [8]byte
}

type Handle uintptr

type Hostent struct {
	Name     *byte
	Aliases  **byte
	AddrType uint16
	Length   uint16
	AddrList **byte
}

type IPMreq struct {
	Multiaddr [4]byte /* in_addr */
	Interface [4]byte /* in_addr */
}

type IPv6Mreq struct {
	Multiaddr [16]byte /* in6_addr */
	Interface uint32
}

type InterfaceInfo struct {
	Flags            uint32
	Address          SockaddrGen
	BroadcastAddress SockaddrGen
	Netmask          SockaddrGen
}

type IpAdapterInfo struct {
	Next                *IpAdapterInfo
	ComboIndex          uint32
	AdapterName         [MAX_ADAPTER_NAME_LENGTH + 4]byte
	Description         [MAX_ADAPTER_DESCRIPTION_LENGTH + 4]byte
	AddressLength       uint32
	Address             [MAX_ADAPTER_ADDRESS_LENGTH]byte
	Index               uint32
	Type                uint32
	DhcpEnabled         uint32
	CurrentIpAddress    *IpAddrString
	IpAddressList       IpAddrString
	GatewayList         IpAddrString
	DhcpServer          IpAddrString
	HaveWins            bool
	PrimaryWinsServer   IpAddrString
	SecondaryWinsServer IpAddrString
	LeaseObtained       int64
	LeaseExpires        int64
}

type IpAddrString struct {
	Next      *IpAddrString
	IpAddress IpAddressString
	IpMask    IpMaskString
	Context   uint32
}

type IpAddressString struct {
	String [16]byte
}

type IpMaskString IpAddressString

type LazyDLL struct {
	Name string
	// Has unexported fields.
}
    A LazyDLL implements access to a single DLL. It will delay the load of
    the DLL until the first call to its LazyDLL.Handle method or to one of its
    LazyProc's Addr method.

    LazyDLL is subject to the same DLL preloading attacks as documented on
    LoadDLL.

    Use LazyDLL in golang.org/x/sys/windows for a secure way to load system
    DLLs.

func NewLazyDLL(name string) *LazyDLL
    NewLazyDLL creates new LazyDLL associated with DLL file.

func (d *LazyDLL) Handle() uintptr
    Handle returns d's module handle.

func (d *LazyDLL) Load() error
    Load loads DLL file d.Name into memory. It returns an error if fails.
    Load will not try to load DLL, if it is already loaded into memory.

func (d *LazyDLL) NewProc(name string) *LazyProc
    NewProc returns a LazyProc for accessing the named procedure in the DLL d.

type LazyProc struct {
	Name string

	// Has unexported fields.
}
    A LazyProc implements access to a procedure inside a LazyDLL. It delays the
    lookup until the LazyProc.Addr, LazyProc.Call, or LazyProc.Find method is
    called.

func (p *LazyProc) Addr() uintptr
    Addr returns the address of the procedure represented by p. The return value
    can be passed to Syscall to run the procedure.

func (p *LazyProc) Call(a ...uintptr) (r1, r2 uintptr, lastErr error)
    Call executes procedure p with arguments a. See the documentation of
    Proc.Call for more information.

func (p *LazyProc) Find() error
    Find searches DLL for procedure named p.Name. It returns an error if search
    fails. Find will not search procedure, if it is already found and loaded
    into memory.

type Linger struct {
	Onoff  int32
	Linger int32
}

type MibIfRow struct {
	Name            [MAX_INTERFACE_NAME_LEN]uint16
	Index           uint32
	Type            uint32
	Mtu             uint32
	Speed           uint32
	PhysAddrLen     uint32
	PhysAddr        [MAXLEN_PHYSADDR]byte
	AdminStatus     uint32
	OperStatus      uint32
	LastChange      uint32
	InOctets        uint32
	InUcastPkts     uint32
	InNUcastPkts    uint32
	InDiscards      uint32
	InErrors        uint32
	InUnknownProtos uint32
	OutOctets       uint32
	OutUcastPkts    uint32
	OutNUcastPkts   uint32
	OutDiscards     uint32
	OutErrors       uint32
	OutQLen         uint32
	DescrLen        uint32
	Descr           [MAXLEN_IFDESCR]byte
}

type Overlapped struct {
	Internal     uintptr
	InternalHigh uintptr
	Offset       uint32
	OffsetHigh   uint32
	HEvent       Handle
}

type Pointer *struct{}
    Pointer represents a pointer to an arbitrary Windows type.

    Pointer-typed fields may point to one of many different types. It's up to
    the caller to provide a pointer to the appropriate type, cast to Pointer.
    The caller must obey the unsafe.Pointer rules while doing so.

type Proc struct {
	Dll  *DLL
	Name string
	// Has unexported fields.
}
    A Proc implements access to a procedure inside a DLL.

func (p *Proc) Addr() uintptr
    Addr returns the address of the procedure represented by p. The return value
    can be passed to Syscall to run the procedure.

func (p *Proc) Call(a ...uintptr) (uintptr, uintptr, error)
    Call executes procedure p with arguments a.

    The returned error is always non-nil, constructed from the result of
    GetLastError. Callers must inspect the primary return value to decide
    whether an error occurred (according to the semantics of the specific
    function being called) before consulting the error. The error always has
    type Errno.

    On amd64, Call can pass and return floating-point values. To pass an
    argument x with C type "float", use uintptr(math.Float32bits(x)).
    To pass an argument with C type "double", use uintptr(math.Float64bits(x)).
    Floating-point return values are returned in r2. The return value for C
    type "float" is math.Float32frombits(uint32(r2)). For C type "double",
    it is math.Float64frombits(uint64(r2)).

type ProcAttr struct {
	Dir   string
	Env   []string
	Files []uintptr
	Sys   *SysProcAttr
}

type ProcessEntry32 struct {
	Size            uint32
	Usage           uint32
	ProcessID       uint32
	DefaultHeapID   uintptr
	ModuleID        uint32
	Threads         uint32
	ParentProcessID uint32
	PriClassBase    int32
	Flags           uint32
	ExeFile         [MAX_PATH]uint16
}

type ProcessInformation struct {
	Process   Handle
	Thread    Handle
	ProcessId uint32
	ThreadId  uint32
}

type Protoent struct {
	Name    *byte
	Aliases **byte
	Proto   uint16
}

type RawConn interface {
	// Control invokes f on the underlying connection's file
	// descriptor or handle.
	// The file descriptor fd is guaranteed to remain valid while
	// f executes but not after f returns.
	Control(f func(fd uintptr)) error

	// Read invokes f on the underlying connection's file
	// descriptor or handle; f is expected to try to read from the
	// file descriptor.
	// If f returns true, Read returns. Otherwise Read blocks
	// waiting for the connection to be ready for reading and
	// tries again repeatedly.
	// The file descriptor is guaranteed to remain valid while f
	// executes but not after f returns.
	Read(f func(fd uintptr) (done bool)) error

	// Write is like Read but for writing.
	Write(f func(fd uintptr) (done bool)) error
}
    A RawConn is a raw network connection.

type RawSockaddr struct {
	Family uint16
	Data   [14]int8
}

type RawSockaddrAny struct {
	Addr RawSockaddr
	Pad  [100]int8
}

func (rsa *RawSockaddrAny) Sockaddr() (Sockaddr, error)

type RawSockaddrInet4 struct {
	Family uint16
	Port   uint16
	Addr   [4]byte /* in_addr */
	Zero   [8]uint8
}

type RawSockaddrInet6 struct {
	Family   uint16
	Port     uint16
	Flowinfo uint32
	Addr     [16]byte /* in6_addr */
	Scope_id uint32
}

type RawSockaddrUnix struct {
	Family uint16
	Path   [UNIX_PATH_MAX]int8
}

type Rusage struct {
	CreationTime Filetime
	ExitTime     Filetime
	KernelTime   Filetime
	UserTime     Filetime
}
    Invented structures to support what package os expects.

type SID struct{}
    The security identifier (SID) structure is a variable-length structure used
    to uniquely identify users or groups.

func (sid *SID) Copy() (*SID, error)
    Copy creates a duplicate of security identifier sid.

func (sid *SID) Len() int
    Len returns the length, in bytes, of a valid security identifier sid.

func (sid *SID) LookupAccount(system string) (account, domain string, accType uint32, err error)
    LookupAccount retrieves the name of the account for this sid and the name of
    the first domain on which this sid is found. System specify target computer
    to search for.

func (sid *SID) String() (string, error)
    String converts sid to a string format suitable for display, storage,
    or transmission.

type SIDAndAttributes struct {
	Sid        *SID
	Attributes uint32
}

type SSLExtraCertChainPolicyPara struct {
	Size       uint32
	AuthType   uint32
	Checks     uint32
	ServerName *uint16
}

type SecurityAttributes struct {
	Length             uint32
	SecurityDescriptor uintptr
	InheritHandle      uint32
}

type Servent struct {
	Name    *byte
	Aliases **byte
	Proto   *byte
	Port    uint16
}

type Signal int

func (s Signal) Signal()

func (s Signal) String() string

type Sockaddr interface {
	// Has unexported methods.
}

type SockaddrGen [24]byte

type SockaddrInet4 struct {
	Port int
	Addr [4]byte
	// Has unexported fields.
}

type SockaddrInet6 struct {
	Port   int
	ZoneId uint32
	Addr   [16]byte
	// Has unexported fields.
}

type SockaddrUnix struct {
	Name string
	// Has unexported fields.
}

type StartupInfo struct {
	Cb uint32

	Desktop       *uint16
	Title         *uint16
	X             uint32
	Y             uint32
	XSize         uint32
	YSize         uint32
	XCountChars   uint32
	YCountChars   uint32
	FillAttribute uint32
	Flags         uint32
	ShowWindow    uint16

	StdInput  Handle
	StdOutput Handle
	StdErr    Handle
	// Has unexported fields.
}

type SysProcAttr struct {
	HideWindow                 bool
	CmdLine                    string // used if non-empty, else the windows command line is built by escaping the arguments passed to StartProcess
	CreationFlags              uint32
	Token                      Token               // if set, runs new process in the security context represented by the token
	ProcessAttributes          *SecurityAttributes // if set, applies these security attributes as the descriptor for the new process
	ThreadAttributes           *SecurityAttributes // if set, applies these security attributes as the descriptor for the main thread of the new process
	NoInheritHandles           bool                // if set, no handles are inherited by the new process, not even the standard handles, contained in ProcAttr.Files, nor the ones contained in AdditionalInheritedHandles
	AdditionalInheritedHandles []Handle            // a list of additional handles, already marked as inheritable, that will be inherited by the new process
	ParentProcess              Handle              // if non-zero, the new process regards the process given by this handle as its parent process, and AdditionalInheritedHandles, if set, should exist in this parent process
}

type Systemtime struct {
	Year         uint16
	Month        uint16
	DayOfWeek    uint16
	Day          uint16
	Hour         uint16
	Minute       uint16
	Second       uint16
	Milliseconds uint16
}

type TCPKeepalive struct {
	OnOff    uint32
	Time     uint32
	Interval uint32
}

type Timespec struct {
	Sec  int64
	Nsec int64
}
    Timespec is an invented structure on Windows, but here for consistency with
    the syscall package for other operating systems.

func NsecToTimespec(nsec int64) (ts Timespec)

func (ts *Timespec) Nano() int64
    Nano returns the time stored in ts as nanoseconds.

func (ts *Timespec) Unix() (sec int64, nsec int64)
    Unix returns the time stored in ts as seconds plus nanoseconds.

type Timeval struct {
	Sec  int32
	Usec int32
}
    Invented values to support what package os expects.

func NsecToTimeval(nsec int64) (tv Timeval)

func (tv *Timeval) Nano() int64
    Nano returns the time stored in tv as nanoseconds.

func (tv *Timeval) Nanoseconds() int64

func (tv *Timeval) Unix() (sec int64, nsec int64)
    Unix returns the time stored in tv as seconds plus nanoseconds.

type Timezoneinformation struct {
	Bias         int32
	StandardName [32]uint16
	StandardDate Systemtime
	StandardBias int32
	DaylightName [32]uint16
	DaylightDate Systemtime
	DaylightBias int32
}

type Token Handle
    An access token contains the security information for a logon session.
    The system creates an access token when a user logs on, and every process
    executed on behalf of the user has a copy of the token. The token identifies
    the user, the user's groups, and the user's privileges. The system uses the
    token to control access to securable objects and to control the ability of
    the user to perform various system-related operations on the local computer.

func (t Token) Close() error
    Close releases access to access token.

func (t Token) GetTokenPrimaryGroup() (*Tokenprimarygroup, error)
    GetTokenPrimaryGroup retrieves access token t primary group information.
    A pointer to a SID structure representing a group that will become the
    primary group of any objects created by a process using this access token.

func (t Token) GetTokenUser() (*Tokenuser, error)
    GetTokenUser retrieves access token t user account information.

func (t Token) GetUserProfileDirectory() (string, error)
    GetUserProfileDirectory retrieves path to the root directory of the access
    token t user's profile.

type Tokenprimarygroup struct {
	PrimaryGroup *SID
}

type Tokenuser struct {
	User SIDAndAttributes
}

type TransmitFileBuffers struct {
	Head       uintptr
	HeadLength uint32
	Tail       uintptr
	TailLength uint32
}

type UserInfo10 struct {
	Name       *uint16
	Comment    *uint16
	UsrComment *uint16
	FullName   *uint16
}

type WSABuf struct {
	Len uint32
	Buf *byte
}

type WSAData struct {
	Version      uint16
	HighVersion  uint16
	MaxSockets   uint16
	MaxUdpDg     uint16
	VendorInfo   *byte
	Description  [WSADESCRIPTION_LEN + 1]byte
	SystemStatus [WSASYS_STATUS_LEN + 1]byte
}

type WSAProtocolChain struct {
	ChainLen     int32
	ChainEntries [MAX_PROTOCOL_CHAIN]uint32
}

type WSAProtocolInfo struct {
	ServiceFlags1     uint32
	ServiceFlags2     uint32
	ServiceFlags3     uint32
	ServiceFlags4     uint32
	ProviderFlags     uint32
	ProviderId        GUID
	CatalogEntryId    uint32
	ProtocolChain     WSAProtocolChain
	Version           int32
	AddressFamily     int32
	MaxSockAddr       int32
	MinSockAddr       int32
	SocketType        int32
	Protocol          int32
	ProtocolMaxOffset int32
	NetworkByteOrder  int32
	SecurityScheme    int32
	MessageSize       uint32
	ProviderReserved  uint32
	ProtocolName      [WSAPROTOCOL_LEN + 1]uint16
}

type WaitStatus struct {
	ExitCode uint32
}

func (w WaitStatus) Continued() bool

func (w WaitStatus) CoreDump() bool

func (w WaitStatus) ExitStatus() int

func (w WaitStatus) Exited() bool

func (w WaitStatus) Signal() Signal

func (w WaitStatus) Signaled() bool

func (w WaitStatus) StopSignal() Signal

func (w WaitStatus) Stopped() bool

func (w WaitStatus) TrapCause() int

type Win32FileAttributeData struct {
	FileAttributes uint32
	CreationTime   Filetime
	LastAccessTime Filetime
	LastWriteTime  Filetime
	FileSizeHigh   uint32
	FileSizeLow    uint32
}

type Win32finddata struct {
	FileAttributes    uint32
	CreationTime      Filetime
	LastAccessTime    Filetime
	LastWriteTime     Filetime
	FileSizeHigh      uint32
	FileSizeLow       uint32
	Reserved0         uint32
	Reserved1         uint32
	FileName          [MAX_PATH - 1]uint16
	AlternateFileName [13]uint16
}


BUG: The definition of Linger is not appropriate for direct use
with Setsockopt and Getsockopt.
Use SetsockoptLinger instead.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
