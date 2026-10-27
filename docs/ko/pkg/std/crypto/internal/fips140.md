# package crypto/internal/fips140

- 원문: <https://pkg.go.dev/crypto/internal/fips140>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package fips140 // import "crypto/internal/fips140"


VARIABLES

var Enabled bool

FUNCTIONS

func CAST(name string, f func() error)
    CAST runs the named Cryptographic Algorithm Self-Test (if operated in FIPS
    mode) and aborts the program (stopping the module input/output and entering
    the "error state") if the self-test fails.

    CASTs are mandatory self-checks that must be performed by FIPS 140-3 modules
    before the algorithm is used. See Implementation Guidance 10.3.A.

    The name must not contain commas, colons, hashes, or equal signs.

    If a package p calls CAST from its init function, an import of p should also
    be added to crypto/internal/fips140test. If a package p calls CAST on the
    first use of the algorithm, an invocation of that algorithm should be added
    to fipstest.TestConditionals.

func Name() string
func PCT(name string, f func() error)
    PCT runs the named Pairwise Consistency Test (if operated in FIPS mode) and
    aborts the program (stopping the module input/output and entering the "error
    state") if the test fails.

    PCTs are mandatory for every generated (but not imported) key pair,
    including ephemeral keys (which effectively doubles the cost of key
    establishment). See Implementation Guidance 10.3.A Additional Comment 1.

    The name must not contain commas, colons, hashes, or equal signs.

    If a package p calls PCT during key generation, an invocation of that
    function should be added to fipstest.TestConditionals.

func RecordApproved()
    RecordApproved is an internal function that records the use of an approved
    service. It does not override RecordNonApproved calls in the same span.

    It should be called by exposed functions that perform a whole cryptographic
    alrgorithm (e.g. by Sum, not by New, unless a cryptographic Instantiate
    algorithm is performed) and should be called after any checks that may cause
    the function to error out or panic.

func RecordNonApproved()
    RecordNonApproved is an internal function that records the use of a
    non-approved service. It overrides any RecordApproved calls in the same
    span.

func ResetServiceIndicator()
    ResetServiceIndicator clears the service indicator for the running
    goroutine.

func ServiceIndicator() bool
    ServiceIndicator returns true if and only if all services invoked by this
    goroutine since the last ResetServiceIndicator call are approved.

    If ResetServiceIndicator was not called before by this goroutine, its return
    value is undefined.

func Supported() error
    Supported returns an error if FIPS 140-3 mode can't be enabled.

func Version() string
    Version returns the formal version (such as "v1.0.0") if building against a
    frozen module with GOFIPS140. Otherwise, it returns "latest".
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
