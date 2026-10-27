# package crypto/internal/constanttime

- 원문: <https://pkg.go.dev/crypto/internal/constanttime>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package constanttime // import "crypto/internal/constanttime"


FUNCTIONS

func ByteEq(x, y uint8) int
    ByteEq returns 1 if x == y and 0 otherwise.

func Eq(x, y int32) int
    Eq returns 1 if x == y and 0 otherwise.

func LessOrEq(x, y int) int
    LessOrEq returns 1 if x <= y and 0 otherwise. Its behavior is undefined if x
    or y are negative or > 2**31 - 1.

func Select(v, x, y int) int
    Select returns x if v == 1 and y if v == 0. Its behavior is undefined if v
    takes any other value.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
