# package internal/syscall/windows/registry

- 원문: <https://pkg.go.dev/internal/syscall/windows/registry>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package registry provides access to the Windows registry.

## 원문 요약

Package registry provides access to the Windows registry.

## API 상세 (go doc -all)

~~~text
package registry // import "internal/syscall/windows/registry"

Package registry provides access to the Windows registry.

Here is a simple example, opening a registry key and reading a string value from
it.

    k, err := registry.OpenKey(registry.LOCAL_MACHINE, `SOFTWARE\Microsoft\Windows NT\CurrentVersion`, registry.QUERY_VALUE)
    if err != nil {
    	log.Fatal(err)
    }
    defer k.Close()

    s, _, err := k.GetStringValue("SystemRoot")
    if err != nil {
    	log.Fatal(err)
    }
    fmt.Printf("Windows system root is %q\n", s)

NOTE: This package is a copy of golang.org/x/sys/windows/registry with
KeyInfo.ModTime removed to prevent dependency cycles.

CONSTANTS

const (
	// Registry key security and access rights.
	// See https://learn.microsoft.com/en-us/windows/win32/sysinfo/registry-key-security-and-access-rights
	// for details.
	ALL_ACCESS         = 0xf003f
	CREATE_LINK        = 0x00020
	CREATE_SUB_KEY     = 0x00004
	ENUMERATE_SUB_KEYS = 0x00008
	EXECUTE            = 0x20019
	NOTIFY             = 0x00010
	QUERY_VALUE        = 0x00001
	READ               = 0x20019
	SET_VALUE          = 0x00002
	WOW64_32KEY        = 0x00200
	WOW64_64KEY        = 0x00100
	WRITE              = 0x20006
)
const (
	// Windows defines some predefined root keys that are always open.
	// An application can use these keys as entry points to the registry.
	// Normally these keys are used in OpenKey to open new keys,
	// but they can also be used anywhere a Key is required.
	CLASSES_ROOT   = Key(syscall.HKEY_CLASSES_ROOT)
	CURRENT_USER   = Key(syscall.HKEY_CURRENT_USER)
	LOCAL_MACHINE  = Key(syscall.HKEY_LOCAL_MACHINE)
	USERS          = Key(syscall.HKEY_USERS)
	CURRENT_CONFIG = Key(syscall.HKEY_CURRENT_CONFIG)
)
const (
	// Registry value types.
	NONE                       = 0
	SZ                         = 1
	EXPAND_SZ                  = 2
	BINARY                     = 3
	DWORD                      = 4
	DWORD_BIG_ENDIAN           = 5
	LINK                       = 6
	MULTI_SZ                   = 7
	RESOURCE_LIST              = 8
	FULL_RESOURCE_DESCRIPTOR   = 9
	RESOURCE_REQUIREMENTS_LIST = 10
	QWORD                      = 11
)

VARIABLES

var (
	// ErrShortBuffer is returned when the buffer was too short for the operation.
	ErrShortBuffer = syscall.ERROR_MORE_DATA

	// ErrNotExist is returned when a registry key or value does not exist.
	ErrNotExist = syscall.ERROR_FILE_NOT_FOUND

	// ErrUnexpectedType is returned by Get*Value when the value's type was unexpected.
	ErrUnexpectedType = errors.New("unexpected key value type")
)

FUNCTIONS

func CreateKey(k Key, path string, access uint32) (newk Key, openedExisting bool, err error)
    CreateKey creates a key named path under open key k. CreateKey returns the
    new key and a boolean flag that reports whether the key already existed.
    The access parameter specifies the access rights for the key to be created.

func DeleteKey(k Key, path string) error
    DeleteKey deletes the subkey path of key k and its values.

func ExpandString(value string) (string, error)
    ExpandString expands environment-variable strings and replaces them with the
    values defined for the current user. Use ExpandString to expand EXPAND_SZ
    strings.

func OpenKey(k Key, path string, access uint32) (Key, error)
    OpenKey opens a new key with path name relative to key k. It accepts any
    open key, including CURRENT_USER and others, and returns the new key and an
    error. The access parameter specifies desired access rights to the key to be
    opened.


TYPES

type Key syscall.Handle
    Key is a handle to an open Windows registry key. Keys can be obtained
    by calling OpenKey; there are also some predefined root keys such as
    CURRENT_USER. Keys can be used directly in the Windows API.

func (k Key) Close() error
    Close closes open key k.

func (k Key) DeleteValue(name string) error
    DeleteValue removes a named value from the key k.

func (k Key) GetBinaryValue(name string) (val []byte, valtype uint32, err error)
    GetBinaryValue retrieves the binary value for the specified value name
    associated with an open key k. It also returns the value's type. If value
    does not exist, GetBinaryValue returns ErrNotExist. If value is not BINARY,
    it will return the correct value type and ErrUnexpectedType.

func (k Key) GetIntegerValue(name string) (val uint64, valtype uint32, err error)
    GetIntegerValue retrieves the integer value for the specified value name
    associated with an open key k. It also returns the value's type. If value
    does not exist, GetIntegerValue returns ErrNotExist. If value is not DWORD
    or QWORD, it will return the correct value type and ErrUnexpectedType.

func (k Key) GetMUIStringValue(name string) (string, error)
    GetMUIStringValue retrieves the localized string value for the specified
    value name associated with an open key k. If the value name doesn't exist
    or the localized string value can't be resolved, GetMUIStringValue returns
    ErrNotExist.

func (k Key) GetStringValue(name string) (val string, valtype uint32, err error)
    GetStringValue retrieves the string value for the specified value name
    associated with an open key k. It also returns the value's type. If value
    does not exist, GetStringValue returns ErrNotExist. If value is not SZ or
    EXPAND_SZ, it will return the correct value type and ErrUnexpectedType.

func (k Key) GetStringsValue(name string) (val []string, valtype uint32, err error)
    GetStringsValue retrieves the []string value for the specified value
    name associated with an open key k. It also returns the value's type.
    If value does not exist, GetStringsValue returns ErrNotExist. If value is
    not MULTI_SZ, it will return the correct value type and ErrUnexpectedType.

func (k Key) GetValue(name string, buf []byte) (n int, valtype uint32, err error)
    GetValue retrieves the type and data for the specified value associated with
    an open key k. It fills up buffer buf and returns the retrieved byte count
    n. If buf is too small to fit the stored value it returns ErrShortBuffer
    error along with the required buffer size n. If no buffer is provided,
    it returns true and actual buffer size n. If no buffer is provided,
    GetValue returns the value's type only. If the value does not exist,
    the error returned is ErrNotExist.

    GetValue is a low level function. If value's type is known, use the
    appropriate Get*Value function instead.

func (k Key) ReadSubKeyNames() ([]string, error)
    ReadSubKeyNames returns the names of subkeys of key k.

func (k Key) ReadValueNames() ([]string, error)
    ReadValueNames returns the value names of key k.

func (k Key) SetBinaryValue(name string, value []byte) error
    SetBinaryValue sets the data and type of a name value under key k to value
    and BINARY.

func (k Key) SetDWordValue(name string, value uint32) error
    SetDWordValue sets the data and type of a name value under key k to value
    and DWORD.

func (k Key) SetExpandStringValue(name, value string) error
    SetExpandStringValue sets the data and type of a name value under key k to
    value and EXPAND_SZ. The value must not contain a zero byte.

func (k Key) SetQWordValue(name string, value uint64) error
    SetQWordValue sets the data and type of a name value under key k to value
    and QWORD.

func (k Key) SetStringValue(name, value string) error
    SetStringValue sets the data and type of a name value under key k to value
    and SZ. The value must not contain a zero byte.

func (k Key) SetStringsValue(name string, value []string) error
    SetStringsValue sets the data and type of a name value under key k to value
    and MULTI_SZ. The value strings must not contain a zero byte.

func (k Key) Stat() (*KeyInfo, error)
    Stat retrieves information about the open key k.

type KeyInfo struct {
	SubKeyCount     uint32
	MaxSubKeyLen    uint32 // size of the key's subkey with the longest name, in Unicode characters, not including the terminating zero byte
	ValueCount      uint32
	MaxValueNameLen uint32 // size of the key's longest value name, in Unicode characters, not including the terminating zero byte
	MaxValueLen     uint32 // longest data component among the key's values, in bytes
	// Has unexported fields.
}
    A KeyInfo describes the statistics of a key. It is returned by Stat.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
