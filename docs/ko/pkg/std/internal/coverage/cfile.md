# package internal/coverage/cfile

- 원문: <https://pkg.go.dev/internal/coverage/cfile>
- 분류: Go 표준 라이브러리

## 한국어 요약

`cfile` 패키지는 커버리지 파일 관리를 구현합니다.

## 원문 요약

Package cfile implements management of coverage files.

## API 상세 (go doc -all)

~~~text
package cfile // import "internal/coverage/cfile"

Package cfile implements management of coverage files. It provides functionality
exported in runtime/coverage as well as additional functionality used directly
by package testing through testing/internal/testdeps.

FUNCTIONS

func ClearCounters() error
    ClearCounters implements runtime/coverage.ClearCounters.

func InitHook(istest bool)
    InitHook is invoked from the main package "init" routine in programs built
    with "-cover". This function is intended to be called only by the compiler
    (via runtime/coverage.initHook).

    If 'istest' is false, it indicates we're building a regular program ("go
    build -cover ..."), in which case we immediately try to write out the
    meta-data file, and register emitCounterData as an exit hook.

    If 'istest' is true (indicating that the program in question is a Go test
    binary), then we tentatively queue up both emitMetaData and emitCounterData
    as exit hooks. In the normal case (e.g. regular "go test -cover" run) the
    testmain.go boilerplate will run at the end of the test, write out the
    coverage percentage, and then invoke MarkProfileEmitted to indicate that
    no more work needs to be done. If however that call is never made, this
    is a sign that the test binary is being used as a replacement binary for
    the tool being tested, hence we do want to run exit hooks when the program
    terminates.

func MarkProfileEmitted(val bool)
    MarkProfileEmitted signals the coverage machinery that coverage data
    output files have already been written out, and there is no need to take
    any additional action at exit time. This function is called from the
    coverage-related boilerplate code in _testmain.go emitted for go unit tests.

func ProcessCoverTestDir(dir string, cfile string, cm string, cpkg string, w io.Writer, selpkgs []string) error
    ProcessCoverTestDir is called from testmain code when "go test -cover" is
    in effect. It is not intended to be used other than internally by the Go
    command's generated code.

func Snapshot() float64
    Snapshot returns a snapshot of coverage percentage at a moment of time
    within a running test, so as to support the testing.Coverage() function.
    This version doesn't examine coverage meta-data, so the result it returns
    will be less accurate (more "slop") due to the fact that we don't look at
    the meta data to see how many statements are associated with each counter.

func WriteCounters(w io.Writer) error
    WriteCounters implements runtime/coverage.WriteCounters.

func WriteCountersDir(dir string) error
    WriteCountersDir implements runtime/coverage.WriteCountersDir.

func WriteMeta(w io.Writer) error
    WriteMeta implements runtime/coverage.WriteMeta.

func WriteMetaDir(dir string) error
    WriteMetaDir implements runtime/coverage.WriteMetaDir.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
