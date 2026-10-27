# package internal/runtime/startlinetest

- 원문: <https://pkg.go.dev/internal/runtime/startlinetest>
- 분류: Go 표준 라이브러리

## 한국어 요약

`startlinetest` 패키지는 `runtime_test.TestStartLineAsm`을 위한 헬퍼들을 포함합니다.

## 원문 요약

Package startlinetest contains helpers for runtime_test.TestStartLineAsm.

## API 상세 (go doc -all)

~~~text
package startlinetest // import "internal/runtime/startlinetest"

Package startlinetest contains helpers for runtime_test.TestStartLineAsm.

VARIABLES

var CallerStartLine func(bool) int
    Provided by runtime_test.


FUNCTIONS

func AsmFunc() int
    Defined in func_amd64.s, this is a trivial assembly function that calls
    runtime_test.callerStartLine.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
