# package internal/runtime/math

- 원문: <https://pkg.go.dev/internal/runtime/math>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package math // import "internal/runtime/math"


CONSTANTS

const (
	MaxUint16  = ^uint16(0)
	MaxUint32  = ^uint32(0)
	MaxUint64  = ^uint64(0)
	MaxUintptr = ^uintptr(0)

	MaxInt64 = int64(MaxUint64 >> 1)
)

FUNCTIONS

func Add64(x, y, carry uint64) (sum, carryOut uint64)
    Add64 returns the sum with carry of x, y and carry: sum = x + y + carry.
    The carry input must be 0 or 1; otherwise the behavior is undefined.
    The carryOut output is guaranteed to be 0 or 1.

    This function's execution time does not depend on the inputs. On supported
    platforms this is an intrinsic lowered by the compiler.

func MulUintptr(a, b uintptr) (uintptr, bool)
    MulUintptr returns a * b and whether the multiplication overflowed.
    On supported platforms this is an intrinsic lowered by the compiler.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
