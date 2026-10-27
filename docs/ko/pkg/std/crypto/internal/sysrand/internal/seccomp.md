# package crypto/internal/sysrand/internal/seccomp

- 원문: <https://pkg.go.dev/crypto/internal/sysrand/internal/seccomp>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package seccomp // import "crypto/internal/sysrand/internal/seccomp"


FUNCTIONS

func DisableGetrandom() error
    DisableGetrandom makes future calls to getrandom(2) fail with ENOSYS.
    It applies only to the current thread and to any programs executed from it.
    Callers should use runtime.LockOSThread in a dedicated goroutine.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
