# package crypto/internal/fips140/subtle

- 원문: <https://pkg.go.dev/crypto/internal/fips140/subtle>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package subtle // import "crypto/internal/fips140/subtle"


FUNCTIONS

func ConstantTimeCompare(x, y []byte) int
    ConstantTimeCompare returns 1 if the two slices, x and y, have equal
    contents and 0 otherwise. The time taken is a function of the length of the
    slices and is independent of the contents. If the lengths of x and y do not
    match it returns 0 immediately.

func ConstantTimeCopy(v int, x, y []byte)
    ConstantTimeCopy copies the contents of y into x (a slice of equal length)
    if v == 1. If v == 0, x is left unchanged. Its behavior is undefined if v
    takes any other value.

func ConstantTimeLessOrEqBytes(x, y []byte) int
    ConstantTimeLessOrEqBytes returns 1 if x <= y and 0 otherwise.
    The comparison is lexicographical, or big-endian. The time taken is a
    function of the length of the slices and is independent of the contents.
    If the lengths of x and y do not match it returns 0 immediately.

func XORBytes(dst, x, y []byte) int
    XORBytes sets dst[i] = x[i] ^ y[i] for all i < n = min(len(x), len(y)),
    returning n, the number of bytes written to dst.

    If dst does not have length at least n, XORBytes panics without writing
    anything to dst.

    dst and x or y may overlap exactly or not at all, otherwise XORBytes may
    panic.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
