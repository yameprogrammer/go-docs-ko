# package crypto/tls/internal/fips140tls

- 원문: <https://pkg.go.dev/crypto/tls/internal/fips140tls>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package fips140tls controls whether crypto/tls requires FIPS-approved settings.

## 원문 요약

Package fips140tls controls whether crypto/tls requires FIPS-approved settings.

## API 상세 (go doc -all)

~~~text
package fips140tls // import "crypto/tls/internal/fips140tls"

Package fips140tls controls whether crypto/tls requires FIPS-approved settings.

FUNCTIONS

func Force()
    Force forces crypto/tls to restrict TLS configurations to FIPS-approved
    settings. By design, this call is impossible to undo (except in tests).

func Required() bool
    Required reports whether FIPS-approved settings are required.

    Required is true if FIPS 140-3 mode is enabled with GODEBUG=fips140=on, or
    if the crypto/tls/fipsonly package is imported by a Go+BoringCrypto build.

func TestingOnlyAbandon()
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
