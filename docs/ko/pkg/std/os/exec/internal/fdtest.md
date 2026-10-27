# package os/exec/internal/fdtest

- 원문: <https://pkg.go.dev/os/exec/internal/fdtest>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package fdtest는 exec 전후로 파일 디스크립터를 다루기 위한 테스트 헬퍼를 제공합니다.

## 원문 요약

Package fdtest provides test helpers for working with file descriptors across exec.

## API 상세 (go doc -all)

~~~text
package fdtest // import "os/exec/internal/fdtest"

Package fdtest provides test helpers for working with file descriptors across
exec.

FUNCTIONS

func Exists(fd uintptr) bool
    Exists returns true if fd is a valid file descriptor.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
