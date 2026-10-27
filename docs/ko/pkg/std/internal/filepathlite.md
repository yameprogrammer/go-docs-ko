# package internal/filepathlite

- 원문: <https://pkg.go.dev/internal/filepathlite>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package filepathlite implements a subset of path/filepath, only using packages which may be imported by "os".

## 원문 요약

Package filepathlite implements a subset of path/filepath, only using packages which may be imported by "os".

## API 상세 (go doc -all)

~~~text
package filepathlite // import "internal/filepathlite"

Package filepathlite implements a subset of path/filepath, only using packages
which may be imported by "os".

Tests for these functions are in path/filepath.

CONSTANTS

const (
	Separator     = '\\' // OS-specific path separator
	ListSeparator = ';'  // OS-specific path list separator
)

FUNCTIONS

func Base(path string) string
    Base is filepath.Base.

func Clean(path string) string
    Clean is filepath.Clean.

func Dir(path string) string
    Dir is filepath.Dir.

func Ext(path string) string
    Ext is filepath.Ext.

func FromSlash(path string) string
    FromSlash is filepath.FromSlash.

func IsAbs(path string) (b bool)
    IsAbs reports whether the path is absolute.

func IsLocal(path string) bool
    IsLocal is filepath.IsLocal.

func IsPathSeparator(c uint8) bool
func Localize(path string) (string, error)
    Localize is filepath.Localize.

func Split(path string) (dir, file string)
    Split is filepath.Split.

func ToSlash(path string) string
    ToSlash is filepath.ToSlash.

func VolumeName(path string) string
    VolumeName is filepath.VolumeName.

func VolumeNameLen(path string) int
    VolumeNameLen returns the length of the leading volume name on Windows.
    It returns 0 elsewhere.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
