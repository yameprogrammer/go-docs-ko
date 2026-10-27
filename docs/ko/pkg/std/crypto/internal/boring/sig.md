# package crypto/internal/boring/sig

- 원문: <https://pkg.go.dev/crypto/internal/boring/sig>
- 분류: Go 표준 라이브러리

## 한국어 요약

`sig` 패키지는 호출 시 최종 바이너리에 특정 코드 시퀀스가 링크되도록 하는 "코드 서명(code signatures)"을 보유합니다.

## 원문 요약

Package sig holds “code signatures” that can be called and will result in certain code sequences being linked into the final binary.

## API 상세 (go doc -all)

~~~text
package sig // import "crypto/internal/boring/sig"

Package sig holds “code signatures” that can be called and will result in
certain code sequences being linked into the final binary. The functions
themselves are no-ops.

FUNCTIONS

func BoringCrypto()
    BoringCrypto indicates that the BoringCrypto module is present.

func FIPSOnly()
    FIPSOnly indicates that package crypto/tls/fipsonly is present.

func StandardCrypto()
    StandardCrypto indicates that standard Go crypto is present.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
