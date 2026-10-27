# package internal/testenv

- 원문: <https://pkg.go.dev/internal/testenv>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `testenv`는 Go 팀에서 실행되는 다양한 테스트 환경에서 어떤 기능이 사용 가능한지에 대한 정보를 제공합니다.

## 원문 요약

Package testenv provides information about what functionality is available in different testing environments run by the Go team.

## API 상세 (go doc -all)

~~~text
package testenv // import "internal/testenv"

Package testenv provides information about what functionality is available in
different testing environments run by the Go team.

It is an internal package because these details are specific to the Go team's
test setup (on build.golang.org) and not fundamental to tests in general.

VARIABLES

var Sigquit = os.Kill
    Sigquit is the signal to send to kill a hanging subprocess. On Unix we send
    SIGQUIT, but on non-Unix we only have os.Kill.


FUNCTIONS

func Builder() string
    Builder reports the name of the builder running this test. For example,
    "gotip-linux-amd64_avx512-test_only" or "go1.24-windows-arm64" on LUCI,
    or "linux-amd64" on our old infrastructure. Prefer using runtime.GOOS,
    runtime.GOARCH, race.Enabled, reading the OS version, checking CPU feature
    flags with internal/cpu, etc. over parsing builder names when possible. When
    matching builder names, prefer a fuzzy match instead of a strict comparison.
    If the test is not running on the build infrastructure, Builder returns the
    empty string.

func CPUIsSlow() bool
    CPUIsSlow reports whether the CPU running the test is suspected to be slow.

func CPUProfilingBroken() bool
    CPUProfilingBroken returns true if CPU profiling has known issues on this
    platform.

func CanInternalLink(withCgo bool) bool
    CanInternalLink reports whether the current system can link programs with
    internal linking.

func CleanCmdEnv(cmd *exec.Cmd) *exec.Cmd
    CleanCmdEnv will fill cmd.Env with the environment, excluding certain
    variables that could modify the behavior of the Go tools such as GODEBUG and
    GOTRACEBACK.

    If the caller wants to set cmd.Dir, set it before calling this function,
    so PWD will be set correctly in the environment.

func Command(t testing.TB, name string, args ...string) *exec.Cmd
    Command is like exec.Command, but applies the same changes as
    testenv.CommandContext (with a default Context).

func CommandContext(t testing.TB, ctx context.Context, name string, args ...string) *exec.Cmd
    CommandContext is like exec.CommandContext, but:
      - skips t if the platform does not support os/exec,
      - sends SIGQUIT (if supported by the platform) instead of SIGKILL in its
        Cancel function
      - if the test has a deadline, adds a Context timeout and WaitDelay for an
        arbitrary grace period before the test's deadline expires,
      - fails the test if the command does not complete before the test's
        deadline, and
      - sets a Cleanup function that verifies that the test did not leak a
        subprocess.

func Executable(t testing.TB) string
    Executable is a wrapper around MustHaveExec and os.Executable. It returns
    the path name for the executable that started the current process, or skips
    the test if the current system can't start new processes, or fails the test
    if the path can not be obtained.

func GOROOT(t testing.TB) string
    GOROOT reports the path to the directory containing the root of the Go
    project source tree. This is normally equivalent to runtime.GOROOT,
    but works even if the test binary was built with -trimpath and cannot exec
    'go env GOROOT'.

    If GOROOT cannot be found, GOROOT skips t if t is non-nil, or panics
    otherwise.

func GoTool() (string, error)
    GoTool reports the path to the Go tool.

func GoToolPath(t testing.TB) string
    GoToolPath reports the path to the Go tool. It is a convenience wrapper
    around GoTool. If the tool is unavailable GoToolPath calls t.Skip. If the
    tool should be available and isn't, GoToolPath calls t.Fatal.

func HasCGO() bool
    HasCGO reports whether the current system can use cgo.

func HasExternalNetwork() bool
    HasExternalNetwork reports whether the current system can use external
    (non-localhost) networks.

func HasGoBuild() bool
    HasGoBuild reports whether the current system can build programs with “go
    build” and then run them with os.StartProcess or exec.Command.

func HasGoRun() bool
    HasGoRun reports whether the current system can run programs with “go run”.

func HasLink() bool
    HasLink reports whether the current system can use os.Link.

func HasParallelism() bool
    HasParallelism reports whether the current system can execute multiple
    threads in parallel. There is a copy of this function in cmd/dist/test.go.

func HasSymlink() bool
    HasSymlink reports whether the current system can use os.Symlink.

func MustHaveBuildMode(t testing.TB, buildmode string)
    MustHaveBuildMode reports whether the current system can build programs
    in the given build mode. If not, MustHaveBuildMode calls t.Skip with an
    explanation.

func MustHaveCGO(t testing.TB)
    MustHaveCGO calls t.Skip if cgo is not available.

func MustHaveExec(t testing.TB)
    MustHaveExec checks that the current system can start new processes using
    os.StartProcess or (more commonly) exec.Command. If not, MustHaveExec calls
    t.Skip with an explanation.

    On some platforms MustHaveExec checks for exec support by re-executing
    the current executable, which must be a binary built by 'go test'.
    We intentionally do not provide a HasExec function because of the risk of
    inappropriate recursion in TestMain functions.

    To check for exec support outside of a test, just try to exec the command.
    If exec is not supported, testenv.SyscallIsNotSupported will return true for
    the resulting error.

func MustHaveExecPath(t testing.TB, path string)
    MustHaveExecPath checks that the current system can start the named
    executable using os.StartProcess or (more commonly) exec.Command. If not,
    MustHaveExecPath calls t.Skip with an explanation.

func MustHaveExternalNetwork(t testing.TB)
    MustHaveExternalNetwork checks that the current system can use external
    (non-localhost) networks. If not, MustHaveExternalNetwork calls t.Skip with
    an explanation.

func MustHaveGoBuild(t testing.TB)
    MustHaveGoBuild checks that the current system can build programs with
    “go build” and then run them with os.StartProcess or exec.Command. If not,
    MustHaveGoBuild calls t.Skip with an explanation.

func MustHaveGoRun(t testing.TB)
    MustHaveGoRun checks that the current system can run programs with “go run”.
    If not, MustHaveGoRun calls t.Skip with an explanation.

func MustHaveLink(t testing.TB)
    MustHaveLink reports whether the current system can use os.Link. If not,
    MustHaveLink calls t.Skip with an explanation.

func MustHaveParallelism(t testing.TB)
    MustHaveParallelism checks that the current system can execute multiple
    threads in parallel. If not, MustHaveParallelism calls t.Skip with an
    explanation.

func MustHaveSource(t testing.TB)
    MustHaveSource checks that the entire source tree is available under GOROOT.
    If not, it calls t.Skip with an explanation.

    This is needed when reading files from GOROOT that are not in ./testdata.

func MustHaveSymlink(t testing.TB)
    MustHaveSymlink reports whether the current system can use os.Symlink.
    If not, MustHaveSymlink calls t.Skip with an explanation.

func MustInternalLink(t testing.TB, with SpecialBuildTypes)
    MustInternalLink checks that the current system can link programs with
    internal linking. If not, MustInternalLink calls t.Skip with an explanation.

func MustInternalLinkPIE(t testing.TB)
    MustInternalLinkPIE checks whether the current system can link PIE binary
    using internal linking. If not, MustInternalLinkPIE calls t.Skip with an
    explanation.

func OptimizationOff() bool
    OptimizationOff reports whether optimization is disabled.

func ParallelOn64Bit(t *testing.T)
    ParallelOn64Bit calls t.Parallel() unless there is a case that cannot
    be parallel. This function should be used when it is necessary to avoid
    t.Parallel on 32-bit machines, typically because the test uses lots of
    memory.

func SetGODEBUG(t testing.TB, v string)
    SetGODEBUG appends v to the GODEBUG environment variable for the duration of
    the test.

func SkipFlaky(t testing.TB, issue int)
func SkipFlakyNet(t testing.TB)
func SkipIfOptimizationOff(t testing.TB)
    SkipIfOptimizationOff skips t if optimization is disabled.

func SkipIfShortAndSlow(t testing.TB)
    SkipIfShortAndSlow skips t if -short is set and the CPU running the test is
    suspected to be slow.

    (This is useful for CPU-intensive tests that otherwise complete quickly.)

func SyscallIsNotSupported(err error) bool
    SyscallIsNotSupported reports whether err may indicate that a system call is
    not supported by the current platform or execution environment.

func WriteImportcfg(t testing.TB, dstPath string, packageFiles map[string]string, pkgs ...string)
    WriteImportcfg writes an importcfg file used by the compiler or linker to
    dstPath containing entries for the file mappings in packageFiles, as well as
    for the packages transitively imported by the package(s) in pkgs.

    pkgs may include any package pattern that is valid to pass to 'go list',
    so it may also be a list of Go source files all in the same directory.


TYPES

type SpecialBuildTypes struct {
	Cgo  bool
	Asan bool
	Msan bool
	Race bool
}
    SpecialBuildTypes are interesting build types that may affect linking.

var NoSpecialBuildTypes SpecialBuildTypes
    NoSpecialBuildTypes indicates a standard, no cgo go build.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
