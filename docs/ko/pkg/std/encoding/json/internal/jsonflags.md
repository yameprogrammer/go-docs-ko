# package encoding/json/internal/jsonflags

- 원문: <https://pkg.go.dev/encoding/json/internal/jsonflags>
- 분류: Go 표준 라이브러리

## 한국어 요약

jsonflags는 모든 선택적 부울 플래그를 구현합니다.

## 원문 요약

jsonflags implements all the optional boolean flags.

## API 상세 (go doc -all)

~~~text
package jsonflags // import "encoding/json/internal/jsonflags"

jsonflags implements all the optional boolean flags. These flags are shared
across both "json", "jsontext", and "jsonopts".

CONSTANTS

const (
	// AllFlags is the set of all flags.
	AllFlags = AllCoderFlags | AllArshalV2Flags | AllArshalV1Flags

	// AllCoderFlags is the set of all encoder/decoder flags.
	AllCoderFlags = (maxCoderFlag - 1) - initFlag

	// AllArshalV2Flags is the set of all v2 marshal/unmarshal flags.
	AllArshalV2Flags = (maxArshalV2Flag - 1) - (maxCoderFlag - 1)

	// AllArshalV1Flags is the set of all v1 marshal/unmarshal flags.
	AllArshalV1Flags = (maxArshalV1Flag - 1) - (maxArshalV2Flag - 1)

	// NonBooleanFlags is the set of non-boolean flags,
	// where the value is some other concrete Go type.
	// The value of the flag is stored within jsonopts.Struct.
	NonBooleanFlags = 0 |
		Indent |
		IndentPrefix |
		ByteLimit |
		DepthLimit |
		Marshalers |
		Unmarshalers |
		FormatTag

	// DefaultV1Flags is the set of boolean flags that default to true under
	// v1 semantics. None of the non-boolean flags differ between v1 and v2.
	DefaultV1Flags = 0 |
		AllowDuplicateNames |
		AllowInvalidUTF8 |
		EscapeForHTML |
		EscapeForJS |
		PreserveRawStrings |
		Deterministic |
		FormatNilMapAsNull |
		FormatNilSliceAsNull |
		MatchCaseInsensitiveNames |
		CallMethodsWithLegacySemantics |
		FormatByteArrayAsArray |
		FormatBytesWithLegacySemantics |
		FormatDurationAsNano |
		MatchCaseSensitiveDelimiter |
		MergeWithLegacySemantics |
		OmitEmptyWithLegacySemantics |
		ParseBytesWithLooseRFC4648 |
		ParseTimeWithLooseRFC3339 |
		ReportErrorsWithLegacySemantics |
		StringifyWithLegacySemantics |
		UnmarshalArrayFromAnyLength

	// AnyWhitespace reports whether the encoded output might have any whitespace.
	AnyWhitespace = Multiline | SpaceAfterColon | SpaceAfterComma

	// WhitespaceFlags is the set of flags related to whitespace formatting.
	// In contrast to AnyWhitespace, this includes Indent and IndentPrefix
	// as those settings take no effect if Multiline is false.
	WhitespaceFlags = AnyWhitespace | Indent | IndentPrefix

	// AnyEscape is the set of flags related to escaping in a JSON string.
	AnyEscape = EscapeForHTML | EscapeForJS

	// CanonicalizeNumbers is the set of flags related to raw number canonicalization.
	CanonicalizeNumbers = CanonicalizeRawInts | CanonicalizeRawFloats

	// TagFlags is the set of flags related to the presence of struct field tags.
	// Tags have non-recursive effects, where the tag only applies to
	// the top-level of the field value itself.
	// Whenever descending into a JSON object or array, these flags are cleared.
	TagFlags = StringTag | FormatTag
)

TYPES

type Bools uint64
    Bools represents zero or more boolean flags, all set to true or false.
    The least-significant bit is the boolean value of all flags in the set.
    The remaining bits identify which particular flags.

    In common usage, this is OR'd with 0 or 1. For example:
      - (AllowInvalidUTF8 | 0) means "AllowInvalidUTF8 is false"
      - (Multiline | Indent | 1) means "Multiline and Indent are true"

const (
	AllowDuplicateNames   Bools // encode or decode
	AllowInvalidUTF8            // encode or decode
	WithinArshalCall            // encode or decode; for internal use by json.Marshal and json.Unmarshal
	OmitTopLevelNewline         // encode only; for internal use by json.Marshal and json.MarshalWrite
	PreserveRawStrings          // encode only
	CanonicalizeRawInts         // encode only
	CanonicalizeRawFloats       // encode only
	ReorderRawObjects           // encode only
	EscapeForHTML               // encode only
	EscapeForJS                 // encode only
	Multiline                   // encode only
	SpaceAfterColon             // encode only
	SpaceAfterComma             // encode only
	Indent                      // encode only; non-boolean flag
	IndentPrefix                // encode only; non-boolean flag
	ByteLimit                   // encode or decode; non-boolean flag
	DepthLimit                  // encode or decode; non-boolean flag

)
    Encoder and decoder flags.

const (
	StringifyNumbers          Bools // marshal or unmarshal
	Deterministic                   // marshal only
	FormatNilMapAsNull              // marshal only
	FormatNilSliceAsNull            // marshal only
	OmitZeroStructFields            // marshal only
	MatchCaseInsensitiveNames       // marshal or unmarshal
	RejectUnknownMembers            // unmarshal only
	Marshalers                      // marshal only; non-boolean flag
	Unmarshalers                    // unmarshal only; non-boolean flag
	StringTag                       // marshal or unmarshal
	FormatTag                       // marshal or unmarshal; non-boolean flag
	FormatTagSupported              // marshal or unmarshal

)
    Marshal and Unmarshal flags (for v2).

const (
	CallMethodsWithLegacySemantics  Bools // marshal or unmarshal
	FormatByteArrayAsArray                // marshal or unmarshal
	FormatBytesWithLegacySemantics        // marshal or unmarshal
	FormatDurationAsNano                  // marshal or unmarshal
	MatchCaseSensitiveDelimiter           // marshal or unmarshal
	MergeWithLegacySemantics              // unmarshal
	OmitEmptyWithLegacySemantics          // marshal
	ParseBytesWithLooseRFC4648            // unmarshal
	ParseTimeWithLooseRFC3339             // unmarshal
	ReportErrorsWithLegacySemantics       // marshal or unmarshal
	StringifyWithLegacySemantics          // marshal or unmarshal
	UnmarshalAnyWithRawNumber             // unmarshal; for internal use by jsonv1.Decoder.UseNumber
	UnmarshalArrayFromAnyLength           // unmarshal

)
    Marshal and Unmarshal flags (for v1).

func (Bools) JSONOptions(internal.NotForPublicUse)

type Flags struct{ Presence, Values uint64 }
    Flags is a set of boolean flags. If the presence bit is zero, then the value
    bit must also be zero. The least-significant bit of both fields is always
    zero.

    Unlike Bools, which can represent a set of bools that are all true or false,
    Flags represents a set of bools, each individually may be true or false.

func (fs *Flags) Clear(f Bools)
    Clear clears both the presence and value for the provided bool or bools.
    The value bit of f (i.e., the LSB) is ignored.

func (fs Flags) Get(f Bools) bool
    Get reports whether the bool (or any of the bools) is true. This is
    generally only used with a singular bool. The value bit of f (i.e., the LSB)
    is ignored.

func (fs Flags) Has(f Bools) bool
    Has reports whether the bool (or any of the bools) is set. The value bit of
    f (i.e., the LSB) is ignored.

func (dst *Flags) Join(src Flags)
    Join joins two sets of flags such that the latter takes precedence.

func (fs *Flags) Set(f Bools)
    Set sets both the presence and value for the provided bool (or set of
    bools).
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
