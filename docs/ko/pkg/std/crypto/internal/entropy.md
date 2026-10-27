# package crypto/internal/entropy

- 원문: <https://pkg.go.dev/crypto/internal/entropy>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package entropy provides the passive entropy source for the FIPS 140-3 module.

## 원문 요약

Package entropy provides the passive entropy source for the FIPS 140-3 module.

## API 상세 (go doc -all)

~~~text
package entropy // import "crypto/internal/entropy"

Package entropy provides the passive entropy source for the FIPS 140-3 module.
It is only used in FIPS mode by crypto/internal/fips140/drbg.Read from the FIPS
140-3 Go Cryptographic Module v1.0.0.

Later versions of the module use the CPU jitter-based entropy source in the
crypto/internal/entropy/v1.0.0 sub-package.

This complied with IG 9.3.A, Additional Comment 12, which until January 1,
2026 allows new modules to meet an earlier version of Resolution 2(b):
"A software module that contains an approved DRBG that receives a LOAD command
(or its logical equivalent) with entropy obtained from [...] inside the physical
perimeter of the operational environment of the module [...]."

Distributions that have their own SP 800-90B entropy source should replace this
package with their own implementation.

[earlier version]: https://csrc.nist.gov/CSRC/media/Projects/cryptographic-module-validation-program/documents/IG%209.3.A%20Resolution%202b%5BMarch%2026%202024%5D.pdf

FUNCTIONS

func Depleted(LOAD func(*[48]byte))
    Depleted notifies the entropy source that the entropy in the module is
    "depleted" and provides the callback for the LOAD command.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
