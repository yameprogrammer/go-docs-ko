# package crypto/internal/sysrand

- 원문: <https://pkg.go.dev/crypto/internal/sysrand>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package rand provides cryptographically secure random bytes from the operating system.

## 원문 요약

Package rand provides cryptographically secure random bytes from the operating system.

## API 상세 (go doc -all)

~~~text
package sysrand // import "crypto/internal/sysrand"

Package rand provides cryptographically secure random bytes from the operating
system.

FUNCTIONS

func Read(b []byte)
    Read fills b with cryptographically secure random bytes from the operating
    system. It always fills b entirely and crashes the program irrecoverably if
    an error is encountered. The operating system APIs are documented to never
    return an error on all but legacy Linux systems.

    Note that Read is not affected by testing/cryptotest.SetGlobalRand, and it
    should not be used directly by algorithm implementations.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
