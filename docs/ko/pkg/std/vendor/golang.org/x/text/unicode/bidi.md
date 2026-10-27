# package vendor/golang.org/x/text/unicode/bidi

- 원문: <https://pkg.go.dev/vendor/golang.org/x/text/unicode/bidi>
- 분류: Go 표준 라이브러리

## 한국어 요약

`bidi` 패키지는 양방향 텍스트 지원을 위한 기능을 제공합니다.

## 원문 요약

Package bidi contains functionality for bidirectional text support.

## API 상세 (go doc -all)

~~~text
package bidi // import "vendor/golang.org/x/text/unicode/bidi"

Package bidi contains functionality for bidirectional text support.

See https://www.unicode.org/reports/tr9.

NOTE: UNDER CONSTRUCTION. This API may change in backwards incompatible ways and
without notice.

CONSTANTS

const UnicodeVersion = "17.0.0"
    UnicodeVersion is the Unicode version from which the tables in this package
    are derived.


FUNCTIONS

func AppendReverse(out, in []byte) []byte
    AppendReverse reverses the order of characters of in, appends them to out,
    and returns the result. Modifiers will still follow the runes they modify.
    Brackets are replaced with their counterparts.

func ReverseString(s string) string
    ReverseString reverses the order of characters in s and returns a new
    string. Modifiers will still follow the runes they modify. Brackets are
    replaced with their counterparts.


TYPES

type Class uint
    Class is the Unicode BiDi class. Each rune has a single class.

const (
	L       Class = iota // LeftToRight
	R                    // RightToLeft
	EN                   // EuropeanNumber
	ES                   // EuropeanSeparator
	ET                   // EuropeanTerminator
	AN                   // ArabicNumber
	CS                   // CommonSeparator
	B                    // ParagraphSeparator
	S                    // SegmentSeparator
	WS                   // WhiteSpace
	ON                   // OtherNeutral
	BN                   // BoundaryNeutral
	NSM                  // NonspacingMark
	AL                   // ArabicLetter
	Control              // Control LRO - PDI

	LRO // LeftToRightOverride
	RLO // RightToLeftOverride
	LRE // LeftToRightEmbedding
	RLE // RightToLeftEmbedding
	PDF // PopDirectionalFormat
	LRI // LeftToRightIsolate
	RLI // RightToLeftIsolate
	FSI // FirstStrongIsolate
	PDI // PopDirectionalIsolate

)
type Direction int
    A Direction indicates the overall flow of text.

const (
	// LeftToRight indicates the text contains no right-to-left characters and
	// that either there are some left-to-right characters or the option
	// DefaultDirection(LeftToRight) was passed.
	LeftToRight Direction = iota

	// RightToLeft indicates the text contains no left-to-right characters and
	// that either there are some right-to-left characters or the option
	// DefaultDirection(RightToLeft) was passed.
	RightToLeft

	// Mixed indicates text contains both left-to-right and right-to-left
	// characters.
	Mixed

	// Neutral means that text contains no left-to-right and right-to-left
	// characters and that no default direction has been set.
	Neutral
)
type Option func(*options)
    An Option is an option for Bidi processing.

func DefaultDirection(d Direction) Option
    DefaultDirection sets the default direction for a Paragraph. The direction
    is overridden if the text contains directional characters.

type Ordering struct {
	// Has unexported fields.
}
    An Ordering holds the computed visual order of runs of a Paragraph. Calling
    SetBytes or SetString on the originating Paragraph invalidates an Ordering.
    The methods of an Ordering should only be called by one goroutine at a time.

func (o *Ordering) Direction() Direction
    Direction reports the directionality of the runs.

    The direction may be LeftToRight, RightToLeft, Mixed, or Neutral.

func (o *Ordering) NumRuns() int
    NumRuns returns the number of runs.

func (o *Ordering) Run(i int) Run
    Run returns the ith run within the ordering.

type Paragraph struct {
	// Has unexported fields.
}
    A Paragraph holds a single Paragraph for Bidi processing.

func (p *Paragraph) Direction() Direction
    Direction returns the direction of the text of this paragraph.

    The direction may be LeftToRight, RightToLeft, Mixed, or Neutral.

func (p *Paragraph) IsLeftToRight() bool
    IsLeftToRight reports whether the principle direction of rendering for this
    paragraphs is left-to-right. If this returns false, the principle direction
    of rendering is right-to-left.

func (p *Paragraph) Line(start, end int) (Ordering, error)
    Line computes the visual ordering of runs for a single line starting and
    ending at the given positions in the original text.

func (p *Paragraph) Order() (Ordering, error)
    Order computes the visual ordering of all the runs in a Paragraph.

func (p *Paragraph) RunAt(pos int) Run
    RunAt reports the Run at the given position of the input text.

    This method can be used for computing line breaks on paragraphs.

func (p *Paragraph) SetBytes(b []byte, opts ...Option) (n int, err error)
    SetBytes configures p for the given paragraph text. It replaces text
    previously set by SetBytes or SetString. If b contains a paragraph separator
    it will only process the first paragraph and report the number of bytes
    consumed from b including this separator. Error may be non-nil if options
    are given.

func (p *Paragraph) SetString(s string, opts ...Option) (n int, err error)
    SetString configures s for the given paragraph text. It replaces text
    previously set by SetBytes or SetString. If s contains a paragraph separator
    it will only process the first paragraph and report the number of bytes
    consumed from s including this separator. Error may be non-nil if options
    are given.

type Properties struct {
	// Has unexported fields.
}
    Properties provides access to BiDi properties of runes.

func Lookup(s []byte) (p Properties, sz int)
    Lookup returns properties for the first rune in s and the width in bytes of
    its encoding. The size will be 0 if s does not hold enough bytes to complete
    the encoding.

func LookupRune(r rune) (p Properties, size int)
    LookupRune returns properties for r.

func LookupString(s string) (p Properties, sz int)
    LookupString returns properties for the first rune in s and the width in
    bytes of its encoding. The size will be 0 if s does not hold enough bytes to
    complete the encoding.

func (p Properties) Class() Class
    Class returns the Bidi class for p.

func (p Properties) IsBracket() bool
    IsBracket reports whether the rune is a bracket.

func (p Properties) IsOpeningBracket() bool
    IsOpeningBracket reports whether the rune is an opening bracket. IsBracket
    must return true.

type Run struct {
	// Has unexported fields.
}
    A Run is a continuous sequence of characters of a single direction.

func (r *Run) Bytes() []byte
    Bytes returns the text of the run in its original order.

func (r *Run) Direction() Direction
    Direction reports the direction of the run.

func (r *Run) Pos() (start, end int)
    Pos returns the position of the Run within the text passed to SetBytes or
    SetString of the originating Paragraph value.

func (r *Run) String() string
    String returns the text of the run in its original order.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
