# package vendor/golang.org/x/text/secure/bidirule

- 원문: <https://pkg.go.dev/vendor/golang.org/x/text/secure/bidirule>
- 분류: Go 표준 라이브러리

## 한국어 요약

`bidirule` 패키지는 RFC 5893에 정의된 Bidi Rule을 구현합니다.

## 원문 요약

Package bidirule implements the Bidi Rule defined by RFC 5893.

## API 상세 (go doc -all)

~~~text
package bidirule // import "vendor/golang.org/x/text/secure/bidirule"

Package bidirule implements the Bidi Rule defined by RFC 5893.

This package is under development. The API may change without notice and without
preserving backward compatibility.

VARIABLES

var ErrInvalid = errors.New("bidirule: failed Bidi Rule")
    ErrInvalid indicates a label is invalid according to the Bidi Rule.


FUNCTIONS

func Direction(b []byte) bidi.Direction
    Direction reports the direction of the given label as defined by RFC 5893.
    The Bidi Rule does not have to be applied to labels of the category
    LeftToRight.

func DirectionString(s string) bidi.Direction
    DirectionString reports the direction of the given label as defined by RFC
    5893. The Bidi Rule does not have to be applied to labels of the category
    LeftToRight.

func Valid(b []byte) bool
    Valid reports whether b conforms to the BiDi rule.

func ValidString(s string) bool
    ValidString reports whether s conforms to the BiDi rule.


TYPES

type Transformer struct {
	// Has unexported fields.
}
    Transformer implements transform.Transform.

func New() *Transformer
    New returns a Transformer that verifies that input adheres to the Bidi Rule.

func (t *Transformer) Reset()
    Reset implements transform.Transformer.

func (t *Transformer) Span(src []byte, atEOF bool) (n int, err error)
    Span returns the first n bytes of src that conform to the Bidi rule.

func (t *Transformer) Transform(dst, src []byte, atEOF bool) (nDst, nSrc int, err error)
    Transform implements transform.Transformer. This Transformer has state and
    needs to be reset between uses.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
