# package internal/syscall/unix

- 원문: <https://pkg.go.dev/internal/syscall/unix>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package unix // import "internal/syscall/unix"


FUNCTIONS

func KernelVersion() (major int, minor int)
func KernelVersionGE(x, y int) bool
    KernelVersionGE checks if the running kernel version is greater than or
    equal to the provided version.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
