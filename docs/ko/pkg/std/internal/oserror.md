# package internal/oserror

- 원문: <https://pkg.go.dev/internal/oserror>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `oserror`는 `os` 패키지에서 사용되는 오류 값들을 정의합니다.

## 원문 요약

Package oserror defines errors values used in the os package.

## API 상세 (go doc -all)

~~~text
package oserror // import "internal/oserror"

Package oserror defines errors values used in the os package.

These types are defined here to permit the syscall package to reference them.

VARIABLES

var (
	ErrInvalid    = errors.New("invalid argument")
	ErrPermission = errors.New("permission denied")
	ErrExist      = errors.New("file already exists")
	ErrNotExist   = errors.New("file does not exist")
	ErrClosed     = errors.New("file already closed")
)
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
