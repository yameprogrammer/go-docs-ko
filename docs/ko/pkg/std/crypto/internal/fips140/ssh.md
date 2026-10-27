# package crypto/internal/fips140/ssh

- 원문: <https://pkg.go.dev/crypto/internal/fips140/ssh>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 ssh는 RFC 4253, 7.2 섹션 및 SP 800-135 Revision 1에 명시된 대로 SSH KDF를 구현합니다.

## 원문 요약

Package ssh implements the SSH KDF as specified in RFC 4253, Section 7.2 and allowed by SP 800-135 Revision 1.

## API 상세 (go doc -all)

~~~text
package ssh // import "crypto/internal/fips140/ssh"

Package ssh implements the SSH KDF as specified in RFC 4253, Section 7.2 and
allowed by SP 800-135 Revision 1.

FUNCTIONS

func Keys[Hash hash.Hash](hash func() Hash, d Direction,
	K, H, sessionID []byte,
	ivKeyLen, keyLen, macKeyLen int,
) (ivKey, key, macKey []byte)

TYPES

type Direction struct {
	// Has unexported fields.
}

var ServerKeys, ClientKeys Direction
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
