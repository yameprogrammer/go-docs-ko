# package internal/runtime/exithook

- 원문: <https://pkg.go.dev/internal/runtime/exithook>
- 분류: Go 표준 라이브러리

## 한국어 요약

`exithook` 패키지는 종료 시 정리(cleanup) 작업을 위한 제한적인 지원을 제공합니다.

## 원문 요약

Package exithook provides limited support for on-exit cleanup.

## API 상세 (go doc -all)

~~~text
package exithook // import "internal/runtime/exithook"

Package exithook provides limited support for on-exit cleanup.

CAREFUL! The expectation is that Add should only be called from a safe
context (e.g. not an error/panic path or signal handler, preemption enabled,
allocation allowed, write barriers allowed, etc), and that the exit function F
will be invoked under similar circumstances. That is to say, we are expecting
that F uses normal / high-level Go code as opposed to one of the more restricted
dialects used for the trickier parts of the runtime.

VARIABLES

var (

	// runtime sets these for us
	Gosched func()
	Goid    func() uint64
	Throw   func(string)
)

FUNCTIONS

func Add(h Hook)
    Add adds a new exit hook.

func Run(code int)
    Run runs the exit hooks.

    If an exit hook panics, Run will throw with the panic on the stack. If an
    exit hook invokes exit in the same goroutine, the goroutine will throw.
    If an exit hook invokes exit in another goroutine, that exit will block.


TYPES

type Hook struct {
	F            func() // func to run
	RunOnFailure bool   // whether to run on non-zero exit code
}
    A Hook is a function to be run at program termination (when someone invokes
    os.Exit, or when main.main returns). Hooks are run in reverse order of
    registration: the first hook added is the last one run.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
