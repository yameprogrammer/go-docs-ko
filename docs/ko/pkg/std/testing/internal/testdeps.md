# package testing/internal/testdeps

- 원문: <https://pkg.go.dev/testing/internal/testdeps>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `testdeps`는 테스트 실행에 필요한 의존성에 접근하는 기능을 제공합니다.

## 원문 요약

Package testdeps provides access to dependencies needed by test execution.

## API 상세 (go doc -all)

~~~text
package testdeps // import "testing/internal/testdeps"

Package testdeps provides access to dependencies needed by test execution.

This package is imported by the generated main package, which passes TestDeps
into testing.Main. This allows tests to use packages at run time without making
those packages direct dependencies of package testing. Direct dependencies of
package testing are harder to write tests for.

VARIABLES

var (
	CoverSnapshotFunc           func() float64
	CoverProcessTestDirFunc     func(dir string, cfile string, cm string, cpkg string, w io.Writer, selpkgs []string) error
	CoverMarkProfileEmittedFunc func(val bool)
)
    These variables below are set at runtime (via code in testmain) to point to
    the equivalent functions in package internal/coverage/cfile; doing things
    this way allows us to have tests import internal/coverage/cfile only when
    -cover is in effect (as opposed to importing for all tests).

var Cover bool
    Cover indicates whether coverage is enabled.

var CoverMode string
var CoverSelectedPackages []string
var Covered string
var ImportPath string
    ImportPath is the import path of the testing binary, set by the generated
    main function.

var ModulePath string

TYPES

type TestDeps struct{}
    TestDeps is an implementation of the testing.testDeps interface, suitable
    for passing to testing.MainStart.

func (TestDeps) CheckCorpus(vals []any, types []reflect.Type) error

func (TestDeps) CoordinateFuzzing(
	timeout time.Duration,
	limit int64,
	minimizeTimeout time.Duration,
	minimizeLimit int64,
	parallel int,
	seed []fuzz.CorpusEntry,
	types []reflect.Type,
	corpusDir,
	cacheDir string) (err error)

func (TestDeps) ImportPath() string

func (TestDeps) InitRuntimeCoverage() (mode string, tearDown func(string, string) (string, error), snapcov func() float64)

func (TestDeps) MatchString(pat, str string) (result bool, err error)

func (TestDeps) ModulePath() string

func (TestDeps) ReadCorpus(dir string, types []reflect.Type) ([]fuzz.CorpusEntry, error)

func (TestDeps) ResetCoverage()

func (TestDeps) RunFuzzWorker(fn func(fuzz.CorpusEntry) error) error

func (TestDeps) SetPanicOnExit0(v bool)
    SetPanicOnExit0 tells the os package whether to panic on os.Exit(0).

func (TestDeps) SnapshotCoverage()

func (TestDeps) StartCPUProfile(w io.Writer) error

func (TestDeps) StartTestLog(w io.Writer)

func (TestDeps) StopCPUProfile()

func (TestDeps) StopTestLog() error

func (TestDeps) WriteProfileTo(name string, w io.Writer, debug int) error
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
