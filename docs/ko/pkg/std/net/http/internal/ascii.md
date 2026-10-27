# package net/http/internal/ascii

- 원문: <https://pkg.go.dev/net/http/internal/ascii>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package ascii // import "net/http/internal/ascii"


FUNCTIONS

func EqualFold(s, t string) bool
    EqualFold is strings.EqualFold, ASCII only. It reports whether s and t are
    equal, ASCII-case-insensitively.

func Is(s string) bool
    Is returns whether s is ASCII.

func IsPrint(s string) bool
    IsPrint returns whether s is ASCII and printable according to
    https://tools.ietf.org/html/rfc20#section-4.2.

func ToLower(s string) (lower string, ok bool)
    ToLower returns the lowercase version of s if s is ASCII and printable.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
