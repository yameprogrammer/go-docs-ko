# package internal/synctest

- 원문: <https://pkg.go.dev/internal/synctest>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `synctest`는 동시성 코드 테스트를 위한 지원을 제공합니다.

## 원문 요약

Package synctest provides support for testing concurrent code.

## API 상세 (go doc -all)

~~~text
package synctest // import "internal/synctest"

Package synctest provides support for testing concurrent code.

See the testing/synctest package for function documentation.

CONSTANTS

const (
	Unbubbled     = Association(iota) // not associated with any bubble
	CurrentBubble                     // associated with the current bubble
	OtherBubble                       // associated with a different bubble
)

FUNCTIONS

func Disassociate[T any](p *T)
    Disassociate disassociates p from any bubble.

func IsAssociated[T any](p *T) bool
    IsAssociated reports whether p is associated with the current bubble.

func IsInBubble() bool
    IsInBubble reports whether the current goroutine is in a bubble.

func Run(f func())
func Wait()

TYPES

type Association int
    Association is the state of a pointer's bubble association.

func Associate[T any](p *T) Association
    Associate attempts to associate p with the current bubble. It returns the
    new association status of p.

type Bubble struct {
	// Has unexported fields.
}
    A Bubble is a synctest bubble.

    Not a public API. Used by syscall/js to propagate bubble membership through
    syscalls.

func Acquire() *Bubble
    Acquire returns a reference to the current goroutine's bubble. The bubble
    will not become idle until Release is called.

func (b *Bubble) Release()
    Release releases the reference to the bubble, allowing it to become idle
    again.

func (b *Bubble) Run(f func())
    Run executes f in the bubble. The current goroutine must not be part of a
    bubble.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
