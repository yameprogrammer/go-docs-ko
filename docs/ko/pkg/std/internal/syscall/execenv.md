# package internal/syscall/execenv

- 원문: <https://pkg.go.dev/internal/syscall/execenv>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package execenv // import "internal/syscall/execenv"


FUNCTIONS

func Default(sys *syscall.SysProcAttr) ([]string, error)
    Default will return the default environment variables based on the process
    attributes provided.

    Defaults to syscall.Environ() on all platforms other than Windows.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
