# package testing/slogtest

- 원문: <https://pkg.go.dev/testing/slogtest>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `slogtest`는 `log/slog.Handler` 구현의 테스트를 지원합니다.

## 원문 요약

Package slogtest implements support for testing implementations of log/slog.Handler.

## API 상세 (go doc -all)

~~~text
package slogtest // import "testing/slogtest"

Package slogtest implements support for testing implementations of
log/slog.Handler.

FUNCTIONS

func Run(t *testing.T, newHandler func(*testing.T) slog.Handler, result func(*testing.T) map[string]any)
    Run exercises a slog.Handler on the same test cases as TestHandler, but runs
    each case in a subtest. For each test case, it first calls newHandler to get
    an instance of the handler under test, then runs the test case, then calls
    result to get the result. If the test case fails, it calls t.Error.

func TestHandler(h slog.Handler, results func() []map[string]any) error
    TestHandler tests a slog.Handler. If TestHandler finds any misbehaviors,
    it returns an error for each, combined into a single error with errors.Join.

    TestHandler installs the given Handler in a slog.Logger and makes several
    calls to the Logger's output methods. The Handler should be enabled for
    levels Info and above.

    The results function is invoked after all such calls. It should return
    a slice of map[string]any, one for each call to a Logger output method.
    The keys and values of the map should correspond to the keys and values of
    the Handler's output. Each group in the output should be represented as its
    own nested map[string]any. The standard keys slog.TimeKey, slog.LevelKey and
    slog.MessageKey should be used.

    If the Handler outputs JSON, then calling encoding/json.Unmarshal with a
    `map[string]any` will create the right data structure.

    If a Handler intentionally drops an attribute that is checked by a test,
    then the results function should check for its absence and add it to the map
    it returns.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
