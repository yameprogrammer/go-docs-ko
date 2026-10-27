# package go/importer

- 원문: <https://pkg.go.dev/go/importer>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package importer는 export 데이터 importer에 대한 액세스를 제공합니다.

## 원문 요약

Package importer provides access to export data importers.

## API 상세 (go doc -all)

~~~text
package importer // import "go/importer"

Package importer provides access to export data importers.

These functions, which are mostly deprecated, date from before the introduction
of modules in release Go 1.11. They should no longer be relied on except for use
in test cases using small programs that depend only on the standard library.
For reliable module-aware loading of type information, use the packages.Load
function from golang.org/x/tools/go/packages.

FUNCTIONS

func Default() types.Importer
    Default returns an Importer for the compiler that built the running binary.
    If available, the result implements types.ImporterFrom.

    Default may be convenient for use in the simplest of cases, but most clients
    should instead use ForCompiler, which accepts a token.FileSet from the
    caller; without it, all position information derived from the Importer will
    be incorrect and misleading. See also the package documentation.

func For(compiler string, lookup Lookup) types.Importer
    For calls ForCompiler with a new FileSet.

    Deprecated: Use ForCompiler, which populates a FileSet with the positions of
    objects created by the importer.

func ForCompiler(fset *token.FileSet, compiler string, lookup Lookup) types.Importer
    ForCompiler returns an Importer for importing from installed packages for
    the compilers "gc" and "gccgo", or for importing directly from the source
    if the compiler argument is "source". In this latter case, importing may
    fail under circumstances where the exported API is not entirely defined in
    pure Go source code (if the package API depends on cgo-defined entities,
    the type checker won't have access to those).

    The lookup function is called each time the resulting importer needs to
    resolve an import path. In this mode the importer can only be invoked with
    canonical import paths (not relative or absolute ones); it is assumed that
    the translation to canonical import paths is being done by the client of the
    importer.

    A lookup function must be provided for correct module-aware
    operation. Providing a nil value for lookup is deprecated but, for
    backwards-compatibility, the importer will in this case attempt to resolve
    imports in the $GOPATH workspace.


TYPES

type Lookup func(path string) (io.ReadCloser, error)
    A Lookup function returns a reader to access package data for a given import
    path, or an error if no matching package is found.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
