# package internal/stringslite

- 원문: <https://pkg.go.dev/internal/stringslite>
- 분류: Go 표준 라이브러리

## 한국어 요약

`stringslite` 패키지는 "os"에서 임포트할 수 있는 패키지만을 사용하여 `strings` 패키지의 서브셋(subset)을 구현합니다.

## 원문 요약

Package stringslite implements a subset of strings, only using packages that may be imported by "os".

## API 상세 (go doc -all)

~~~text
package stringslite // import "internal/stringslite"

Package stringslite implements a subset of strings, only using packages that may
be imported by "os".

Tests for these functions are in the strings package.

FUNCTIONS

func Clone(s string) string
func Cut(s, sep string) (before, after string, found bool)
func CutPrefix(s, prefix string) (after string, found bool)
func CutSuffix(s, suffix string) (before string, found bool)
func HasPrefix(s, prefix string) bool
func HasSuffix(s, suffix string) bool
func Index(s, substr string) int
func IndexByte(s string, c byte) int
func TrimPrefix(s, prefix string) string
func TrimSuffix(s, suffix string) string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
