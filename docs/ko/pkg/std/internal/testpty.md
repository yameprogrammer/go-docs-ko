# package internal/testpty

- 원문: <https://pkg.go.dev/internal/testpty>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `testpty`는 CGO를 통해 C 함수를 호출하여 구현된 간단한 퓨전터미널 패키지로, 유닉스 시스템용입니다.

## 원문 요약

Package testpty is a simple pseudo-terminal package for Unix systems, implemented by calling C functions via cgo.

## API 상세 (go doc -all)

~~~text
package testpty // import "internal/testpty"

Package testpty is a simple pseudo-terminal package for Unix systems,
implemented by calling C functions via cgo.

VARIABLES

var ErrNotSupported = errors.New("testpty.Open not implemented on this platform")

FUNCTIONS

func Open() (pty *os.File, processTTY string, err error)
    Open returns a control pty and the name of the linked process tty.

    If Open is not implemented on this platform, it returns ErrNotSupported.


TYPES

type PtyError struct {
	FuncName    string
	ErrorString string
	Errno       error
}

func (e *PtyError) Error() string

func (e *PtyError) Unwrap() error
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
