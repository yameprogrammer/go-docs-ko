# package encoding/json/internal/jsonwire

- 원문: <https://pkg.go.dev/encoding/json/internal/jsonwire>
- 분류: Go 표준 라이브러리

## 한국어 요약

package jsonwire는 JSON 텍스트를 처리하기 위한 상태 비저장(stateless) 기능을 구현합니다.

## 원문 요약

Package jsonwire implements stateless functionality for handling JSON text.

## API 상세 (go doc -all)

~~~text
package jsonwire // import "encoding/json/internal/jsonwire"

Package jsonwire implements stateless functionality for handling JSON text.

VARIABLES

var ErrInvalidUTF8 = errors.New("invalid UTF-8")
    TODO(https://go.dev/issue/70547): Use utf8.ErrInvalid instead.


FUNCTIONS

func AppendFloat(dst []byte, src float64, bits int) []byte
    AppendFloat appends src to dst as a JSON number per RFC 7159, section 6.
    It formats numbers similar to the ES6 number-to-string conversion.
    See https://go.dev/issue/14135.

    The output is identical to ECMA-262, 6th edition, section 7.1.12.1 and with
    RFC 8785, section 3.2.2.3 for 64-bit floating-point numbers except for -0,
    which is formatted as -0 instead of just 0.

    For 32-bit floating-point numbers, the output is a 32-bit equivalent of the
    algorithm. Note that ECMA-262 specifies no algorithm for 32-bit numbers.

func AppendQuote(dst, src []byte, flags *jsonflags.Flags) ([]byte, error)
    AppendQuote appends src to dst as a JSON string per RFC 7159, section 7.

    It takes in flags and respects the following:
      - EscapeForHTML escapes '<', '>', and '&'.
      - EscapeForJS escapes '\u2028' and '\u2029'.
      - AllowInvalidUTF8 avoids reporting an error for invalid UTF-8.

    Regardless of whether AllowInvalidUTF8 is specified, invalid bytes are
    replaced with the Unicode replacement character ('\ufffd'). If no escape
    flags are set, then the shortest representable form is used, which is also
    the canonical form for strings (RFC 8785, section 3.2.2.2).

func AppendUnquote(dst, src []byte) (v []byte, err error)
    AppendUnquote appends the unescaped form of a JSON string in src to dst.
    Any invalid UTF-8 within the string will be replaced with utf8.RuneError,
    but the error will be specified as having encountered such an error.
    The input must be an entire JSON string with no surrounding whitespace.

func CompareUTF16(x, y []byte) int
    CompareUTF16 lexicographically compares x to y according to the UTF-16
    codepoints of the UTF-8 encoded input strings. This implements the ordering
    specified in RFC 8785, section 3.2.3.

func ConsumeFalse(b []byte) int
    ConsumeFalse consumes the next JSON false literal per RFC 7159, section 3.
    It returns 0 if it is invalid, in which case ConsumeLiteral should be used.

func ConsumeLiteral(b []byte, lit string) (n int, err error)
    ConsumeLiteral consumes the next JSON literal per RFC 7159, section 3.
    If the input appears truncated, it returns io.ErrUnexpectedEOF.

func ConsumeNull(b []byte) int
    ConsumeNull consumes the next JSON null literal per RFC 7159, section 3.
    It returns 0 if it is invalid, in which case ConsumeLiteral should be used.

func ConsumeNumber(b []byte) (n int, err error)
    ConsumeNumber consumes the next JSON number per RFC 7159, section 6. It
    reports the number of bytes consumed and whether an error was encountered.
    If the input appears truncated, it returns io.ErrUnexpectedEOF.

    Note that JSON numbers are not self-terminating. If the entire input is
    consumed, then the caller needs to consider whether there may be subsequent
    unread data that may still be part of this number.

func ConsumeSimpleNumber(b []byte) (n int)
    ConsumeSimpleNumber consumes the next JSON number per RFC 7159, section
    6 but is limited to the grammar for a non-negative integer. It returns 0
    if it is invalid or more complicated than a simple integer, in which case
    ConsumeNumber should be called.

func ConsumeSimpleString(b []byte) (n int)
    ConsumeSimpleString consumes the next JSON string per RFC 7159, section 7
    but is limited to the grammar for an ASCII string without escape sequences.
    It returns 0 if it is invalid or more complicated than a simple string,
    in which case ConsumeString should be called.

    It rejects '<', '>', and '&' for compatibility reasons since these were
    always escaped in the v1 implementation. Thus, if this function reports
    non-zero then we know that the string would be encoded the same way under
    both v1 or v2 escape semantics.

func ConsumeString(flags *ValueFlags, b []byte, validateUTF8 bool) (n int, err error)
    ConsumeString consumes the next JSON string per RFC 7159, section 7.
    If validateUTF8 is false, then this allows the presence of invalid UTF-8
    characters within the string itself. It reports the number of bytes consumed
    and whether an error was encountered. If the input appears truncated,
    it returns io.ErrUnexpectedEOF.

func ConsumeStringResumable(flags *ValueFlags, b []byte, resumeOffset int, validateUTF8 bool) (n int, err error)
    ConsumeStringResumable is identical to ConsumeString but supports resuming
    from a previous call that returned io.ErrUnexpectedEOF.

func ConsumeTrue(b []byte) int
    ConsumeTrue consumes the next JSON true literal per RFC 7159, section 3.
    It returns 0 if it is invalid, in which case ConsumeLiteral should be used.

func ConsumeWhitespace(b []byte) (n int)
    ConsumeWhitespace consumes leading JSON whitespace per RFC 7159, section 2.

func HasSuffixByte(b []byte, c byte) bool
    HasSuffixByte reports whether b ends with c.

func NeedEscape(src []byte) bool
    NeedEscape reports whether src needs escaping of any characters.
    It conservatively assumes EscapeForHTML and EscapeForJS. It reports true for
    inputs with invalid UTF-8.

func NewInvalidCharacterError[Bytes ~[]byte | ~string](prefix Bytes, where string) error
func NewInvalidEscapeSequenceError[Bytes ~[]byte | ~string](what Bytes) error
func ParseUint(b []byte) (v uint64, ok bool)
    ParseUint parses b as a decimal unsigned integer according to a strict
    subset of the JSON number grammar, returning the value if valid. It returns
    (0, false) if there is a syntax error and returns (math.MaxUint64, false) if
    there is an overflow.

func QuoteRune(b []byte) string
    QuoteRune quotes the first rune in the input.

func ReformatNumber(dst, src []byte, flags *jsonflags.Flags) ([]byte, int, error)
    ReformatNumber consumes a JSON number from src and appends it to dst,
    canonicalizing it if specified. It returns the appended output and the
    number of consumed input bytes.

func ReformatString(dst, src []byte, flags *jsonflags.Flags) ([]byte, int, error)
    ReformatString consumes a JSON string from src and appends it to dst,
    reformatting it if necessary according to the specified flags. It returns
    the appended output and the number of consumed input bytes.

func TrimSuffixByte(b []byte, c byte) []byte
    TrimSuffixByte removes c from the end of b if it is present.

func TrimSuffixString(b []byte) []byte
    TrimSuffixString trims a valid JSON string at the end of b. The behavior is
    undefined if there is not a valid JSON string present.

func TrimSuffixWhitespace(b []byte) []byte
    TrimSuffixWhitespace trims JSON whitespace from the end of b.

func TruncatePointer(s string, n int) string
    TruncatePointer optionally truncates the JSON pointer, enforcing that the
    length roughly does not exceed n.

func UnquoteMayCopy(b []byte, isVerbatim bool) []byte
    UnquoteMayCopy returns the unescaped form of b. If there are no escaped
    characters, the output is simply a subslice of the input with the
    surrounding quotes removed. Otherwise, a new buffer is allocated for the
    output. It assumes the input is valid.


TYPES

type ConsumeNumberState uint

func ConsumeNumberResumable(b []byte, resumeOffset int, state ConsumeNumberState) (n int, _ ConsumeNumberState, err error)
    ConsumeNumberResumable is identical to ConsumeNumber but supports resuming
    from a previous call that returned io.ErrUnexpectedEOF.

type InvalidTextError struct {
	Label string // e.g., "character" | "escape sequence" | "surrogate pair"
	What  string // raw invalid text
	Where string // e.g., "in string" | "at start of value"
}

func (e *InvalidTextError) Error() string

type ValueFlags uint

func (f ValueFlags) IsCanonical() bool

func (f ValueFlags) IsVerbatim() bool

func (f *ValueFlags) Join(f2 ValueFlags)
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
