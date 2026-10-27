# package internal/gate

- 원문: <https://pkg.go.dev/internal/gate>
- 분류: Go 표준 라이브러리

## 한국어 요약

`gate` 패키지는 대안적인 조건 변수(condition variable)를 제공합니다.

## 원문 요약

Package gate contains an alternative condition variable.

## API 상세 (go doc -all)

~~~text
package gate // import "internal/gate"

Package gate contains an alternative condition variable.

TYPES

type Gate struct {
	// Has unexported fields.
}
    A Gate is a monitor (mutex + condition variable) with one bit of state.

    The condition may be either set or unset. Lock operations may be
    unconditional, or wait for the condition to be set. Unlock operations record
    the new state of the condition.

func New(set bool) Gate
    New returns a new, unlocked gate.

func (g *Gate) Lock() (set bool)
    Lock acquires the gate unconditionally. It reports whether the condition is
    set.

func (g *Gate) LockIfSet() (acquired bool)
    LockIfSet acquires the gate if and only if the condition is set.

func (g *Gate) Unlock(set bool)
    Unlock sets the condition and releases the gate.

func (g *Gate) WaitAndLock(ctx context.Context) error
    WaitAndLock waits until the condition is set before acquiring the gate.
    If the context expires, WaitAndLock returns an error and does not acquire
    the gate.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
