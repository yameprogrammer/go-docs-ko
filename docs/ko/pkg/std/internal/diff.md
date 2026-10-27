# package internal/diff

- 원문: <https://pkg.go.dev/internal/diff>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package diff // import "internal/diff"


FUNCTIONS

func Diff(oldName string, old []byte, newName string, new []byte) []byte
    Diff returns an anchored diff of the two texts old and new in the “unified
    diff” format. If old and new are identical, Diff returns a nil slice (no
    output).

    Unix diff implementations typically look for a diff with the smallest
    number of lines inserted and removed, which can in the worst case take
    time quadratic in the number of lines in the texts. As a result, many
    implementations either can be made to run for a long time or cut off the
    search after a predetermined amount of work.

    In contrast, this implementation looks for a diff with the smallest number
    of “unique” lines inserted and removed, where unique means a line that
    appears just once in both old and new. We call this an “anchored diff”
    because the unique lines anchor the chosen matching regions. An anchored
    diff is usually clearer than a standard diff, because the algorithm does
    not try to reuse unrelated blank lines or closing braces. The algorithm also
    guarantees to run in O(n log n) time instead of the standard O(n²) time.

    Some systems call this approach a “patience diff,” named for the
    “patience sorting” algorithm, itself named for a solitaire card game.
    We avoid that name for two reasons. First, the name has been used for
    a few different variants of the algorithm, so it is imprecise. Second,
    the name is frequently interpreted as meaning that you have to wait longer
    (to be patient) for the diff, meaning that it is a slower algorithm, when in
    fact the algorithm is faster than the standard one.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
