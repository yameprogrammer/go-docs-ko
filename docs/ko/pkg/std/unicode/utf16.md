# package unicode/utf16

- 원문: <https://pkg.go.dev/unicode/utf16>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package utf16 implements encoding and decoding of UTF-16 sequences.

## 원문 요약

Package utf16 implements encoding and decoding of UTF-16 sequences.

## API 상세 (go doc -all)

~~~text
package utf16 // import "unicode/utf16"

Package utf16 implements encoding and decoding of UTF-16 sequences.

FUNCTIONS

func AppendRune(a []uint16, r rune) []uint16
    AppendRune appends the UTF-16 encoding of the Unicode code point r to the
    end of p and returns the extended buffer. If the rune is not a valid Unicode
    code point, it appends the encoding of U+FFFD.

func Decode(s []uint16) []rune
    Decode returns the Unicode code point sequence represented by the UTF-16
    encoding s.

func DecodeRune(r1, r2 rune) rune
    DecodeRune returns the UTF-16 decoding of a surrogate pair. If the pair
    is not a valid UTF-16 surrogate pair, DecodeRune returns the Unicode
    replacement code point U+FFFD.

func Encode(s []rune) []uint16
    Encode returns the UTF-16 encoding of the Unicode code point sequence s.

func EncodeRune(r rune) (r1, r2 rune)
    EncodeRune returns the UTF-16 surrogate pair r1, r2 for the given rune.
    If the rune is not a valid Unicode code point or does not need encoding,
    EncodeRune returns U+FFFD, U+FFFD.

func IsSurrogate(r rune) bool
    IsSurrogate reports whether the specified Unicode code point can appear in a
    surrogate pair.

func RuneLen(r rune) int
    RuneLen returns the number of 16-bit words in the UTF-16 encoding of the
    rune. It returns -1 if the rune is not a valid value to encode in UTF-16.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
