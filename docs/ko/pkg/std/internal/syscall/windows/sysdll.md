# package internal/syscall/windows/sysdll

- 원문: <https://pkg.go.dev/internal/syscall/windows/sysdll>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package sysdll is an internal leaf package that records and reports which Windows DLL names are used by Go itself.

## 원문 요약

Package sysdll is an internal leaf package that records and reports which Windows DLL names are used by Go itself.

## API 상세 (go doc -all)

~~~text
package sysdll // import "internal/syscall/windows/sysdll"

Package sysdll is an internal leaf package that records and reports which
Windows DLL names are used by Go itself. These DLLs are then only loaded from
the System32 directory. See Issue 14959.

VARIABLES

var IsSystemDLL = map[string]bool{}
    IsSystemDLL reports whether the named dll key (a base name, like "foo.dll")
    is a system DLL which should only be loaded from the Windows SYSTEM32
    directory.

    Filenames are case sensitive, but that doesn't matter because the case
    registered with Add is also the same case used with LoadDLL later.

    It has no associated mutex and should only be mutated serially (currently:
    during init), and not concurrent with DLL loading.


FUNCTIONS

func Add(dll string) string
    Add notes that dll is a system32 DLL which should only be loaded from the
    Windows SYSTEM32 directory. It returns its argument back, for ease of use in
    generated code.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
