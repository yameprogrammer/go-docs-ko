# package internal/buildcfg

- 원문: <https://pkg.go.dev/internal/buildcfg>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `buildcfg`는 현재 환경에서 설명된 빌드 설정을 액세스할 수 있게 해줍니다.

## 원문 요약

Package buildcfg provides access to the build configuration described by the current environment.

## API 상세 (go doc -all)

~~~text
package buildcfg // import "internal/buildcfg"

Package buildcfg provides access to the build configuration described by the
current environment. It is for use by build tools such as cmd/go or cmd/compile
and for setting up go/build's Default context.

Note that it does NOT provide access to the build configuration used to
build the currently-running binary. For that, use runtime.GOOS etc as well as
internal/goexperiment.

CONSTANTS

const DefaultCGO_ENABLED = ""
const DefaultGO386 = `sse2`
const DefaultGOAMD64 = `v1`
const DefaultGOARM = `7`
const DefaultGOARM64 = `v8.0`
const DefaultGOEXPERIMENT = defaultGOEXPERIMENT
    DefaultGOEXPERIMENT is the embedded default GOEXPERIMENT string. It is not
    guaranteed to be canonical.

const DefaultGOFIPS140 = `off`
const DefaultGOMIPS = `hardfloat`
const DefaultGOMIPS64 = `hardfloat`
const DefaultGOPPC64 = `power8`
const DefaultGORISCV64 = `rva20u64`

VARIABLES

var (
	GOROOT    = os.Getenv("GOROOT") // cached for efficiency
	GOARCH    = envOr("GOARCH", defaultGOARCH)
	GOOS      = envOr("GOOS", defaultGOOS)
	GO386     = envOr("GO386", DefaultGO386)
	GOAMD64   = goamd64()
	GOARM     = goarm()
	GOARM64   = goarm64()
	GOMIPS    = gomips()
	GOMIPS64  = gomips64()
	GOPPC64   = goppc64()
	GORISCV64 = goriscv64()
	GOWASM    = gowasm()
	ToolTags  = toolTags()
	GO_LDSO   = defaultGO_LDSO
	GOFIPS140 = gofips140()
	Version   = version
)
var Error error
    Error is one of the errors found (if any) in the build configuration.

var FramePointerEnabled = GOARCH == "amd64" || GOARCH == "arm64"
    FramePointerEnabled enables the use of platform conventions for saving frame
    pointers.

    This used to be an experiment, but now it's always enabled on platforms that
    support it.

    Note: must agree with runtime.framepointer_enabled.


FUNCTIONS

func Check()
    Check exits the program with a fatal error if Error is non-nil.

func GOGOARCH() (name, value string)
    GOGOARCH returns the name and value of the GO$GOARCH setting. For example,
    if GOARCH is "amd64" it might return "GOAMD64", "v2".

func Getgoextlinkenabled() string
func ParseGOEXPERIMENT(goos, goarch, goexp string) (*ExperimentFlags, error)
    ParseGOEXPERIMENT parses a (GOOS, GOARCH, GOEXPERIMENT) configuration tuple
    and returns the enabled and baseline experiment flag sets.

    TODO(mdempsky): Move to internal/goexperiment.

func ParseGoarm64(v string) (g Goarm64Features, e error)

TYPES

type ExperimentFlags struct {
	goexperiment.Flags
	// Has unexported fields.
}
    ExperimentFlags represents a set of GOEXPERIMENT flags relative to a
    baseline (platform-default) experiment configuration.

var Experiment ExperimentFlags = func() ExperimentFlags {
	flags, err := ParseGOEXPERIMENT(GOOS, GOARCH, envOr("GOEXPERIMENT", defaultGOEXPERIMENT))
	if err != nil {
		Error = err
		return ExperimentFlags{}
	}
	return *flags
}()
    Experiment contains the toolchain experiments enabled for the current build.

    (This is not necessarily the set of experiments the compiler itself was
    built with.)

    Experiment.baseline specifies the experiment flags that are enabled
    by default in the current toolchain. This is, in effect, the "control"
    configuration and any variation from this is an experiment.

func (exp *ExperimentFlags) All() []string
    All returns a list of all experiment settings. Disabled experiments appear
    in the list prefixed by "no".

func (exp *ExperimentFlags) Enabled() []string
    Enabled returns a list of enabled experiments, as lower-cased experiment
    names.

func (exp *ExperimentFlags) String() string
    String returns the canonical GOEXPERIMENT string to enable this experiment
    configuration. (Experiments in the same state as in the baseline are
    elided.)

type Goarm64Features struct {
	Version string
	// Large Systems Extension
	LSE bool
	// ARM v8.0 Cryptographic Extension. It includes the following features:
	// * FEAT_AES, which includes the AESD and AESE instructions.
	// * FEAT_PMULL, which includes the PMULL, PMULL2 instructions.
	// * FEAT_SHA1, which includes the SHA1* instructions.
	// * FEAT_SHA256, which includes the SHA256* instructions.
	Crypto bool
}

func (g Goarm64Features) String() string

func (g Goarm64Features) Supports(s string) bool
    Returns true if g supports giving ARM64 ISA Note that this function doesn't
    accept / test suffixes (like ",lse" or ",crypto")

type GoarmFeatures struct {
	Version   int
	SoftFloat bool
}

func (g GoarmFeatures) String() string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
