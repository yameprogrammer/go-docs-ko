# package log/internal

- 원문: <https://pkg.go.dev/log/internal>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `internal`은 `log` 및 `log/slog` 모두에서 사용되는 정의를 포함합니다.

## 원문 요약

Package internal contains definitions used by both log and log/slog.

## API 상세 (go doc -all)

~~~text
package internal // import "log/internal"

Package internal contains definitions used by both log and log/slog.

VARIABLES

var DefaultOutput func(pc uintptr, data []byte) error
    DefaultOutput holds a function which calls the default log.Logger's output
    function. It allows slog.defaultHandler to call into an unexported function
    of the log package.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
