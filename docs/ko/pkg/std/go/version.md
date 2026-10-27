# package go/version

- 원문: <https://pkg.go.dev/go/version>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package version은 [Go toolchain name syntax] 형식의 [Go versions](예: "go1.20", "go1.21.0", "go1.22rc2", "go1.23.4-custom"와 같은 문자열)에 대한 작업을 제공합니다.

## 원문 요약

Package version provides operations on [Go versions] in [Go toolchain name syntax]: strings like "go1.20", "go1.21.0", "go1.22rc2", and "go1.23.4-custom".

## API 상세 (go doc -all)

~~~text
package version // import "go/version"

Package version provides operations on Go versions in Go toolchain name syntax:
strings like "go1.20", "go1.21.0", "go1.22rc2", and "go1.23.4-custom".

[Go versions]: https://go.dev/doc/toolchain#version
[Go toolchain name syntax]: https://go.dev/doc/toolchain#name

FUNCTIONS

func Compare(x, y string) int
    Compare returns -1, 0, or +1 depending on whether x < y, x == y, or x > y,
    interpreted as Go versions. The versions x and y must begin with a "go"
    prefix: "go1.21" not "1.21". Invalid versions, including the empty string,
    compare less than valid versions and equal to each other. The language
    version "go1.21" compares less than the release candidate and eventual
    releases "go1.21rc1" and "go1.21.0".

func IsValid(x string) bool
    IsValid reports whether the version x is valid.

func Lang(x string) string
    Lang returns the Go language version for version x. If x is not a valid
    version, Lang returns the empty string. For example:

        Lang("go1.21rc2") = "go1.21"
        Lang("go1.21.2") = "go1.21"
        Lang("go1.21") = "go1.21"
        Lang("go1") = "go1"
        Lang("bad") = ""
        Lang("1.21") = ""
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
