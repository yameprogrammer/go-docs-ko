# package crypto/internal/fips140/check

- 원문: <https://pkg.go.dev/crypto/internal/fips140/check>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `check`는 FIPS 140 규정에 따른 로드 타임 코드+데이터 검증을 구현합니다.

## 원문 요약

Package check implements the FIPS 140 load-time code+data verification.

## API 상세 (go doc -all)

~~~text
package check // import "crypto/internal/fips140/check"

Package check implements the FIPS 140 load-time code+data verification.
Every FIPS package providing cryptographic functionality except hmac and sha256
must import crypto/internal/fips140/check, so that the verification happens
before initialization of package global variables. The hmac and sha256 packages
are used by this package, so they cannot import it. Instead, those packages
must be careful not to change global variables during init. (If necessary,
we could have check call a PostCheck function in those packages after the check
has completed.)

VARIABLES

var Linkinfo struct {
	Magic [16]byte
	Sum   [32]byte
	Self  uintptr
	Sects [4]struct {
		// Note: These must be unsafe.Pointer, not uintptr,
		// or else checkptr panics about turning uintptrs
		// into pointers into the data segment during
		// go test -race.
		Start unsafe.Pointer
		End   unsafe.Pointer
	}
}
    Linkinfo holds the go:fipsinfo symbol prepared by the linker. See
    cmd/link/internal/ld/fips.go for details.

var Verified bool
    Verified is set when verification succeeded. It can be expected to always be
    true when fips140.Enabled is true, or init would have panicked.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
