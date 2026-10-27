# package crypto/fips140

- 원문: <https://pkg.go.dev/crypto/fips140>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `fips140`는 FIPS 140-3 Go 암호화 모듈 및 FIPS 140-3 모드에 대한 정보를 제공합니다.

## 원문 요약

Package fips140 provides information about the FIPS 140-3 Go Cryptographic Module and FIPS 140-3 mode.

## API 상세 (go doc -all)

~~~text
package fips140 // import "crypto/fips140"

Package fips140 provides information about the FIPS 140-3 Go Cryptographic
Module and FIPS 140-3 mode.

For more details, see the FIPS 140-3 documentation.

[FIPS 140-3 documentation]: https://go.dev/doc/security/fips140

FUNCTIONS

func Enabled() bool
    Enabled reports whether the cryptography libraries are operating in FIPS
    140-3 mode.

    It can be controlled at runtime using the GODEBUG setting "fips140".
    If set to "on", FIPS 140-3 mode is enabled. If set to "only", non-approved
    cryptography functions will additionally return errors or panic.

    This can't be changed after the program has started.

func Enforced() bool
    Enforced indicates if strict FIPS 140-3 enforcement is enabled. Strict
    enforcement is enabled when a program is run with GODEBUG=fips140=only and
    enforcement has not been disabled by a call to WithoutEnforcement.

func Version() string
    Version returns the FIPS 140-3 Go Cryptographic Module version (such as
    "v1.0.0"), as referenced in the Security Policy for the module, if building
    against a frozen module with GOFIPS140. Otherwise, it returns "latest".
    If an alias is in use (such as "inprogress") the actual resolved version is
    returned.

    The returned version may not uniquely identify the frozen module which
    was used to build the program, if there are multiple copies of the
    frozen module at the same version. The uniquely identifying version
    suffix can be found by checking the value of the GOFIPS140 setting in
    runtime/debug.BuildInfo.Settings.

func WithoutEnforcement(f func())
    WithoutEnforcement disables strict FIPS 140-3 enforcement while
    executing f. Calling WithoutEnforcement without strict enforcement
    enabled (GODEBUG=fips140=only is not set or already inside of a call to
    WithoutEnforcement) is a no-op.

    WithoutEnforcement is inherited by any goroutines spawned while executing f.

    As this disables enforcement, it should be applied carefully to tightly
    scoped functions.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
