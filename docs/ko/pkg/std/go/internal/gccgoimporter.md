# package go/internal/gccgoimporter

- 원문: <https://pkg.go.dev/go/internal/gccgoimporter>
- 분류: Go 표준 라이브러리

## 한국어 요약

`gccgoimporter` 패키지는 gccgo로 생성된 객체 파일에 대한 `Import`를 구현합니다.

## 원문 요약

Package gccgoimporter implements Import for gccgo-generated object files.

## API 상세 (go doc -all)

~~~text
package gccgoimporter // import "go/internal/gccgoimporter"

Package gccgoimporter implements Import for gccgo-generated object files.

TYPES

type GccgoInstallation struct {
	// Version of gcc (e.g. 4.8.0).
	GccVersion string

	// Target triple (e.g. x86_64-unknown-linux-gnu).
	TargetTriple string

	// Built-in library paths used by this installation.
	LibPaths []string
}
    Information about a specific installation of gccgo.

func (inst *GccgoInstallation) GetImporter(incpaths []string, initmap map[*types.Package]InitData) Importer
    Return an importer that searches incpaths followed by the gcc installation's
    built-in search paths and the current directory.

func (inst *GccgoInstallation) InitFromDriver(gccgoPath string, args ...string) (err error)
    Ask the driver at the given path for information for this GccgoInstallation.
    The given arguments are passed directly to the call of the driver.

func (inst *GccgoInstallation) SearchPaths() (paths []string)
    Return the list of export search paths for this GccgoInstallation.

type Importer func(imports map[string]*types.Package, path, srcDir string, lookup func(string) (io.ReadCloser, error)) (*types.Package, error)
    An Importer resolves import paths to Packages. The imports map records
    packages already known, indexed by package path. An importer must determine
    the canonical package path and check imports to see if it is already present
    in the map. If so, the Importer can return the map entry. Otherwise, the
    importer must load the package data for the given path into a new *Package,
    record it in imports map, and return the package.

func GetImporter(searchpaths []string, initmap map[*types.Package]InitData) Importer

type InitData struct {
	// Initialization priority of this package relative to other packages.
	// This is based on the maximum depth of the package's dependency graph;
	// it is guaranteed to be greater than that of its dependencies.
	Priority int

	// The list of packages which this package depends on to be initialized,
	// including itself if needed. This is the subset of the transitive closure of
	// the package's dependencies that need initialization.
	Inits []PackageInit
}
    The gccgo-specific init data for a package.

type PackageInit struct {
	Name     string // short package name
	InitFunc string // name of init function
	Priority int    // priority of init function, see InitData.Priority
}
    A PackageInit describes an imported package that needs initialization.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
