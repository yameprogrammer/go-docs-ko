# package crypto/internal/fips140/tls12

- 원문: <https://pkg.go.dev/crypto/internal/fips140/tls12>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package tls12 // import "crypto/internal/fips140/tls12"


FUNCTIONS

func MasterSecret[H hash.Hash](hash func() H, preMasterSecret, transcript []byte) []byte
    MasterSecret implements the TLS 1.2 extended master secret derivation,
    as defined in RFC 7627 and allowed by SP 800-135, Revision 1, Section 4.2.2.

func PRF[H hash.Hash](hash func() H, secret []byte, label string, seed []byte, keyLen int) []byte
    PRF implements the TLS 1.2 pseudo-random function, as defined in RFC 5246,
    Section 5 and allowed by SP 800-135, Revision 1, Section 4.2.2.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
