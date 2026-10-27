# package internal/platform

- 원문: <https://pkg.go.dev/internal/platform>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package platform // import "internal/platform"


VARIABLES

var List = []OSArch{
	{"aix", "ppc64"},
	{"android", "386"},
	{"android", "amd64"},
	{"android", "arm"},
	{"android", "arm64"},
	{"darwin", "amd64"},
	{"darwin", "arm64"},
	{"dragonfly", "amd64"},
	{"freebsd", "386"},
	{"freebsd", "amd64"},
	{"freebsd", "arm"},
	{"freebsd", "arm64"},
	{"freebsd", "riscv64"},
	{"illumos", "amd64"},
	{"ios", "amd64"},
	{"ios", "arm64"},
	{"js", "wasm"},
	{"linux", "386"},
	{"linux", "amd64"},
	{"linux", "arm"},
	{"linux", "arm64"},
	{"linux", "loong64"},
	{"linux", "mips"},
	{"linux", "mips64"},
	{"linux", "mips64le"},
	{"linux", "mipsle"},
	{"linux", "ppc64"},
	{"linux", "ppc64le"},
	{"linux", "riscv64"},
	{"linux", "s390x"},
	{"linux", "sparc64"},
	{"netbsd", "386"},
	{"netbsd", "amd64"},
	{"netbsd", "arm"},
	{"netbsd", "arm64"},
	{"openbsd", "386"},
	{"openbsd", "amd64"},
	{"openbsd", "arm"},
	{"openbsd", "arm64"},
	{"openbsd", "ppc64"},
	{"openbsd", "riscv64"},
	{"plan9", "386"},
	{"plan9", "amd64"},
	{"plan9", "arm"},
	{"solaris", "amd64"},
	{"wasip1", "wasm"},
	{"windows", "386"},
	{"windows", "amd64"},
	{"windows", "arm64"},
}
    List is the list of all valid GOOS/GOARCH combinations, including
    known-broken ports.


FUNCTIONS

func ASanSupported(goos, goarch string) bool
    ASanSupported reports whether goos/goarch supports the address sanitizer
    option.

func Broken(goos, goarch string) bool
    Broken reports whether goos/goarch is considered a broken port. (See
    https://go.dev/wiki/PortingPolicy#broken-ports.)

func BuildModeSupported(compiler, buildmode, goos, goarch string) bool
    BuildModeSupported reports whether goos/goarch supports the given build
    mode using the given compiler. There is a copy of this function in
    cmd/dist/test.go.

func CgoSupported(goos, goarch string) bool
    CgoSupported reports whether goos/goarch supports cgo.

func DefaultPIE(goos, goarch string, isRace bool) bool
    DefaultPIE reports whether goos/goarch produces a PIE binary when using
    the "default" buildmode. On Windows this is affected by -race, so force the
    caller to pass that in to centralize that choice.

func ExecutableHasDWARF(goos, goarch string) bool
    ExecutableHasDWARF reports whether the linked executable includes DWARF
    symbols on goos/goarch.

func FirstClass(goos, goarch string) bool
    FirstClass reports whether goos/goarch is considered a “first class” port.
    (See https://go.dev/wiki/PortingPolicy#first-class-ports.)

func FuzzInstrumented(goos, goarch string) bool
    FuzzInstrumented reports whether fuzzing on goos/goarch uses coverage
    instrumentation. (FuzzInstrumented implies FuzzSupported.)

func FuzzSupported(goos, goarch string) bool
    FuzzSupported reports whether goos/goarch supports fuzzing ('go test
    -fuzz=.').

func InternalLinkPIESupported(goos, goarch string) bool
func MSanSupported(goos, goarch string) bool
    MSanSupported reports whether goos/goarch supports the memory sanitizer
    option.

func MustLinkExternal(goos, goarch string, withCgo bool) bool
    MustLinkExternal reports whether goos/goarch requires external linking with
    or without cgo dependencies.

func RaceDetectorSupported(goos, goarch string) bool
    RaceDetectorSupported reports whether goos/goarch supports the race
    detector. There is a copy of this function in cmd/dist/test.go. Race
    detector only supports 48-bit VMA on arm64. But it will always return true
    for arm64, because we don't have VMA size information during the compile
    time.


TYPES

type OSArch struct {
	GOOS, GOARCH string
}
    An OSArch is a pair of GOOS and GOARCH values indicating a platform.

func (p OSArch) String() string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
