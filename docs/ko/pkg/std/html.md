# package html

- 원문: <https://pkg.go.dev/html>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package html provides functions for escaping and unescaping HTML text.

## 원문 요약

Package html provides functions for escaping and unescaping HTML text.

## API 상세 (go doc -all)

~~~text
package html // import "html"

Package html provides functions for escaping and unescaping HTML text.

FUNCTIONS

func EscapeString(s string) string
    EscapeString escapes special characters like "<" to become "&lt;".
    It escapes only five such characters: <, >, &, ' and ".
    UnescapeString(EscapeString(s)) == s always holds, but the converse isn't
    always true.

func UnescapeString(s string) string
    UnescapeString unescapes entities like "&lt;" to become "<".
    It unescapes a larger range of entities than EscapeString escapes.
    For example, "&aacute;" unescapes to "á", as does "&#225;" and "&#xE1;".
    UnescapeString(EscapeString(s)) == s always holds, but the converse isn't
    always true.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
