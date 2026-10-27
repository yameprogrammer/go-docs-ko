# package encoding/json/jsontext

- 원문: <https://pkg.go.dev/encoding/json/jsontext>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package jsontext implements syntactic processing of JSON as specified in RFC 4627, RFC 7159, RFC 7493, RFC 8259, and RFC 8785.

## 원문 요약

Package jsontext implements syntactic processing of JSON as specified in RFC 4627, RFC 7159, RFC 7493, RFC 8259, and RFC 8785.

## API 상세 (go doc -all)

~~~text
package jsontext // import "encoding/json/jsontext"

Package jsontext implements syntactic processing of JSON as specified in
RFC 4627, RFC 7159, RFC 7493, RFC 8259, and RFC 8785. JSON is a simple data
interchange format that can represent primitive data types such as booleans,
strings, and numbers, in addition to structured data types such as objects and
arrays.

The Encoder and Decoder types are used to encode or decode a stream of JSON
tokens or values.

# Tokens and Values

A JSON token refers to the basic structural elements of JSON:

  - a JSON literal (i.e., null, true, or false)
  - a JSON string (e.g., "hello, world!")
  - a JSON number (e.g., 123.456)
  - a begin or end delimiter for a JSON object (i.e., '{' or '}')
  - a begin or end delimiter for a JSON array (i.e., '[' or ']')

A JSON token is represented by the Token type in Go. Technically, there are
two additional structural characters (i.e., ':' and ','), but there is no Token
representation for them since their presence can be inferred by the structure
of the JSON grammar itself. For example, there must always be an implicit colon
between the name and value of a JSON object member.

A JSON value refers to a complete unit of JSON data:

  - a JSON literal, string, or number
  - a JSON object (e.g., `{"name":"value"}`)
  - a JSON array (e.g., `[1,2,3]`)

A JSON value is represented by the Value type in Go and is a []byte containing
the raw textual representation of the value. There is some overlap between
tokens and values as both contain literals, strings, and numbers. However,
only a value can represent the entirety of a JSON object or array.

The Encoder and Decoder types contain methods to read or write the next Token
or Value in a sequence. They maintain a state machine to validate whether the
sequence of JSON tokens and/or values produces valid JSON. Options may be
passed to the NewEncoder or NewDecoder constructors to configure the behavior of
encoding and decoding.

# Terminology

The terms "encode" and "decode" are used for syntactic functionality that is
concerned with processing JSON based on its grammar, and the terms "marshal" and
"unmarshal" are used for semantic functionality that determines the meaning of
JSON values as Go values and vice versa. This package deals with JSON syntax,
while encoding/json/v2 deals with JSON semantics. The goal is to provide a clear
distinction between functionality that is purely concerned with encoding versus
that of marshaling. For example, one can directly encode a stream of JSON tokens
without needing to marshal a concrete Go value representing them. Similarly,
one can decode a stream of JSON tokens without needing to unmarshal them into a
concrete Go value.

This package uses JSON terminology when discussing JSON, which may differ from
related concepts in Go or elsewhere in computing literature.

  - a JSON "object" refers to an unordered collection of name/value members.
  - a JSON "array" refers to an ordered sequence of elements.
  - a JSON "value" refers to either a literal (i.e., null, false, or true),
    string, number, object, or array.

See RFC 8259 for more information.

# Specifications

Relevant specifications include RFC 4627, RFC 7159, RFC 7493, RFC 8259, and RFC
8785. Each RFC is generally a stricter subset of another RFC. In increasing
order of strictness:

  - RFC 4627 and RFC 7159 do not require (but recommend) the use of UTF-8 and
    also do not require (but recommend) that object names be unique.
  - RFC 8259 requires the use of UTF-8, but does not require (but recommends)
    that object names be unique.
  - RFC 7493 requires the use of UTF-8 and also requires that object names be
    unique.
  - RFC 8785 defines a canonical representation. It requires the use of UTF-8
    and also requires that object names be unique and in a specific ordering.
    It specifies exactly how strings and numbers must be formatted.

The primary difference between RFC 4627 and RFC 7159 is that the former
restricted top-level values to only JSON objects and arrays, while RFC 7159 and
subsequent RFCs permit top-level values to additionally be JSON nulls, booleans,
strings, or numbers.

By default, this package operates on RFC 7493, but can be configured to operate
according to the other RFC specifications. RFC 7493 is a stricter subset of
RFC 8259 and fully compliant with it. In particular, it makes specific choices
about behavior that RFC 8259 leaves as undefined in order to ensure greater
interoperability.

# Security Considerations

See the "Security Considerations" section in encoding/json/v2.

VARIABLES

var ErrDuplicateName = errors.New("duplicate object member name")
    ErrDuplicateName indicates that a JSON token could not be encoded or decoded
    because it results in a duplicate JSON object name. This error is directly
    wrapped within a SyntacticError when produced.

    The name of a duplicate JSON object member can be extracted as:

        err := ...
        serr, ok := errors.AsType[*jsontext.SyntacticError](err)
        if ok && serr.Err == jsontext.ErrDuplicateName {
        	ptr := serr.JSONPointer // JSON pointer to duplicate name
        	name := ptr.LastToken() // duplicate name itself
        	...
        }

    This error is only returned if AllowDuplicateNames is false.

var ErrNonStringName = errors.New("object member name must be a string")
    ErrNonStringName indicates that a JSON token could not be encoded or decoded
    because it is not a string, as required for JSON object names according to
    RFC 8259, section 4. This error is directly wrapped within a SyntacticError
    when produced.

var Internal exporter
    Internal is for internal use only. This is exempt from the Go compatibility
    agreement.


FUNCTIONS

func AppendFloat(dst []byte, src float64, bits int) []byte
    AppendFloat appends src to dst as a JSON number per RFC 8259, section 6.

    Except for -0, which is formatted as -0 instead of 0, the output is
    identical to ECMA-262, 10th edition, section 7.1.12.1 and (for 64-bit
    precision) identical to RFC 8785, section 3.2.2.3. The values NaN, +Inf, and
    -Inf will be represented as a JSON string with the values "NaN", "Infinity",
    and "-Infinity".

    Note that most JSON libraries and standards assume that JSON numbers are
    64-bit floating-point numbers. As such, prefer using 64 bits of precision
    unless the recipient can know from other context that the encoded number
    uses 32 bits of precision.

func AppendFormat[Bytes ~[]byte | ~string](dst []byte, src Bytes, opts ...Options) ([]byte, error)
    AppendFormat formats the JSON value in src and appends it to dst according
    to the specified options. See Value.Format for more details about the
    formatting behavior.

    The dst and src may overlap. If an error is reported, then the entirety of
    src is appended to dst.

func AppendQuote[Bytes ~[]byte | ~string](dst []byte, src Bytes) ([]byte, error)
    AppendQuote appends a double-quoted JSON string literal representing
    src to dst and returns the extended buffer. It uses the minimal string
    representation per RFC 8785, section 3.2.2.2. Invalid UTF-8 bytes are
    replaced with the Unicode replacement character and an error is returned at
    the end indicating the presence of invalid UTF-8. The dst must not overlap
    with the src.

func AppendUnquote[Bytes ~[]byte | ~string](dst []byte, src Bytes) ([]byte, error)
    AppendUnquote appends the decoded interpretation of src as a double-quoted
    JSON string literal to dst and returns the extended buffer. The input src
    must be a JSON string without any surrounding whitespace. Invalid UTF-8
    bytes are replaced with the Unicode replacement character and an error is
    returned at the end indicating the presence of invalid UTF-8. Any trailing
    bytes after the JSON string literal results in an error. The dst must not
    overlap with the src.


TYPES

type Decoder struct {
	// Has unexported fields.
}
    Decoder is a streaming decoder for raw JSON tokens and values. It is used
    to read a stream of top-level JSON values, each separated by optional
    whitespace characters.

    Decoder.ReadToken and Decoder.ReadValue calls may be interleaved. For
    example, the following JSON value:

        {"name":"value","array":[null,false,true,3.14159],"object":{"k":"v"}}

    can be parsed with the following calls (ignoring errors for brevity):

        d.ReadToken() // {
        d.ReadToken() // "name"
        d.ReadToken() // "value"
        d.ReadValue() // "array"
        d.ReadToken() // [
        d.ReadToken() // null
        d.ReadToken() // false
        d.ReadValue() // true
        d.ReadToken() // 3.14159
        d.ReadToken() // ]
        d.ReadValue() // "object"
        d.ReadValue() // {"k":"v"}
        d.ReadToken() // }

    The above is one of many possible sequences of calls and may not represent
    the most sensible method to call for any given token/value. For example,
    it is probably more common to call Decoder.ReadToken to obtain a string
    token for object names.

func NewDecoder(r io.Reader, opts ...Options) *Decoder
    NewDecoder constructs a new streaming decoder reading from r.

    If r is a bytes.Buffer, then the decoder parses directly from the buffer
    without first copying the contents to an intermediate buffer. Additional
    writes to the buffer must not occur while the decoder is in use.

func (d *Decoder) InputOffset() int64
    InputOffset returns the current input byte offset. It gives the location of
    the next byte immediately after the most recently returned token or value.
    The number of bytes actually read from the underlying io.Reader may be more
    than this offset due to internal buffering.

func (d *Decoder) Options() Options
    Options returns the options used to construct the decoder
    and may additionally contain semantic options passed to a
    encoding/json/v2.UnmarshalDecode call.

    If operating within a encoding/json/v2.UnmarshalerFrom.UnmarshalJSONFrom
    method call or a encoding/json/v2.UnmarshalFromFunc function call, then the
    returned options are only valid within the call.

func (d *Decoder) PeekKind() Kind
    PeekKind retrieves the next token kind, but does not advance the read
    offset.

    It returns KindInvalid if an error occurs. Any such error is cached until
    the next read call and it is the caller's responsibility to eventually
    follow up a PeekKind call with a read call.

func (d *Decoder) ReadToken() (Token, error)
    ReadToken reads the next Token, advancing the read offset. The returned
    token is only valid until the next Peek, Read, or Skip call. It returns
    io.EOF if there are no more tokens.

func (d *Decoder) ReadValue() (Value, error)
    ReadValue returns the next raw JSON value, advancing the read offset.
    The value is stripped of any leading or trailing whitespace and contains
    the exact bytes of the input, which may contain invalid UTF-8 if
    AllowInvalidUTF8 is specified.

    The returned value is only valid until the next Peek, Read, or Skip call
    and may not be mutated while the Decoder remains in use. If the decoder
    is currently at the end token for an object or array, then it reports a
    SyntacticError and the internal state remains unchanged. It returns io.EOF
    if there are no more values.

func (d *Decoder) Reset(r io.Reader, opts ...Options)
    Reset resets a decoder such that it is reading afresh from r and configured
    with the provided options. Reset must not be called on a Decoder passed
    to the encoding/json/v2.UnmarshalerFrom.UnmarshalJSONFrom method or the
    encoding/json/v2.UnmarshalFromFunc function.

func (d *Decoder) SkipValue() error
    SkipValue is semantically equivalent to calling Decoder.ReadValue and
    discarding the result, except that memory is not wasted trying to hold the
    entire result.

func (d *Decoder) StackDepth() int
    StackDepth returns the depth of the state machine for JSON data that has
    already been read. Each level on the stack represents a nested JSON object
    or array. It is incremented whenever a BeginObject or BeginArray token
    is encountered and decremented whenever an EndObject or EndArray token is
    encountered.

    StackDepth returns 0 when not inside any object or array. In particular,
    it returns 0 before any tokens have been read, after any top-level value
    has been read, and between values when decoding a stream of top-level values
    (e.g., NDJSON). StackDepth returns 1 inside a top-level object or array,
    2 inside a nested object or array, and so on.

    For example, consider decoding the following JSON:

        {"a": [1, 2], "b": {"c": 3}}

    While decoding, StackDepth would report the following:

      - At the start, StackDepth reports 0.
      - After decoding the outer '{', StackDepth reports 1.
      - After decoding the inner '[', StackDepth reports 2.
      - After decoding the inner ']', StackDepth reports 1.
      - After decoding the outer '}', StackDepth reports 0.

func (d *Decoder) StackIndex(i int) (Kind, int64)
    StackIndex returns information about the specified stack level. It must
    be a number between 0 and Decoder.StackDepth, inclusive. For each level,
    it reports the kind:

      - KindInvalid for a level of zero,
      - KindBeginObject for a level representing a JSON object, and
      - KindBeginArray for a level representing a JSON array.

    It also reports the length of that JSON object or array decoded so far.
    Each name and value in a JSON object is counted separately, so the effective
    number of members is half the length. A complete JSON object must have an
    even length.

func (d *Decoder) StackPointer() Pointer
    StackPointer returns a JSON Pointer (RFC 6901) to the most recently read
    value.

func (d *Decoder) UnreadBuffer() []byte
    UnreadBuffer returns the data remaining in the unread buffer, which may
    contain zero or more bytes. This is the data already consumed from the input
    io.Reader, but not yet read by a Decoder.ReadToken or Decoder.ReadValue
    call. It may contain bytes that do not form valid JSON, since it has not yet
    been validated according to the JSON grammar. The exact amount of buffered
    data is an implementation detail of the Decoder and may change over time.

    It is the caller's responsibility to concatenate this buffer with the
    remainder of the input Reader to obtain the full sequence of bytes after the
    last read JSON token or value.

    The returned buffer must not be mutated while Decoder continues to be used.
    The buffer contents are valid until the next Peek, Read, or Skip call.

type Encoder struct {
	// Has unexported fields.
}
    Encoder is a streaming encoder to raw JSON tokens and values. It is used
    to write a stream of top-level JSON values, each terminated with a newline
    character.

    Encoder.WriteToken and Encoder.WriteValue calls may be interleaved.
    For example, the following JSON value:

        {"name":"value","array":[null,false,true,3.14159],"object":{"k":"v"}}

    can be composed with the following calls (ignoring errors for brevity):

        e.WriteToken(BeginObject)        // {
        e.WriteToken(String("name"))     // "name"
        e.WriteToken(String("value"))    // "value"
        e.WriteValue(Value(`"array"`))   // "array"
        e.WriteToken(BeginArray)         // [
        e.WriteToken(Null)               // null
        e.WriteToken(False)              // false
        e.WriteValue(Value("true"))      // true
        e.WriteToken(Float(3.14159))     // 3.14159
        e.WriteToken(EndArray)           // ]
        e.WriteValue(Value(`"object"`))  // "object"
        e.WriteValue(Value(`{"k":"v"}`)) // {"k":"v"}
        e.WriteToken(EndObject)          // }

    The above is one of many possible sequences of calls and may not represent
    the most sensible method to call for any given token/value. For example,
    it is probably more common to call Encoder.WriteToken with a string for
    object names.

func NewEncoder(w io.Writer, opts ...Options) *Encoder
    NewEncoder constructs a new streaming encoder writing to w configured with
    the provided options. It flushes the internal buffer when the buffer is
    sufficiently full or when a top-level value has been written.

    If w is a bytes.Buffer, then the encoder appends directly into the buffer
    without copying the contents from an intermediate buffer.

func (e *Encoder) AvailableBuffer() []byte
    AvailableBuffer returns a zero-length buffer with a possible non-zero
    capacity. This buffer is intended to be used to populate a Value being
    passed to an immediately succeeding Encoder.WriteValue call.

    Example usage:

        b := e.AvailableBuffer()
        b = append(b, '"')
        b = appendString(b, v) // append the string formatting of v
        b = append(b, '"')
        ... := e.WriteValue(b)

    Note that WriteValue expects a valid JSON value. Constructing a value in a
    raw []byte requires more care than using constructor functions like String,
    which always return valid [Token]s or [Value]s.

func (e *Encoder) Options() Options
    Options returns the options used to construct the encoder
    and may additionally contain semantic options passed to a
    encoding/json/v2.MarshalEncode call.

    If operating within a encoding/json/v2.MarshalerTo.MarshalJSONTo method call
    or a encoding/json/v2.MarshalToFunc function call, then the returned options
    are only valid within the call.

func (e *Encoder) OutputOffset() int64
    OutputOffset returns the current output byte offset. It gives the location
    of the next byte immediately after the most recently written token or value.
    The number of bytes actually written to the underlying io.Writer may be less
    than this offset due to internal buffering.

func (e *Encoder) Reset(w io.Writer, opts ...Options)
    Reset resets an encoder such that it is writing afresh to w and configured
    with the provided options. Reset must not be called on an Encoder
    passed to the encoding/json/v2.MarshalerTo.MarshalJSONTo method or the
    encoding/json/v2.MarshalToFunc function.

func (e *Encoder) StackDepth() int
    StackDepth returns the depth of the state machine for written JSON data.
    Each level on the stack represents a nested JSON object or array. It is
    incremented whenever a BeginObject or BeginArray token is encountered and
    decremented whenever an EndObject or EndArray token is encountered.

    StackDepth returns 0 when not inside any object or array. In particular, it
    returns 0 before any tokens have been written, after any top-level value has
    been written, and between values when encoding a stream of top-level values
    (e.g., NDJSON). StackDepth returns 1 inside a top-level object or array,
    2 inside a nested object or array, and so on.

    For example, consider encoding the following JSON:

        {"a": [1, 2], "b": {"c": 3}}

    While encoding, StackDepth would report the following:

      - At the start, StackDepth reports 0.
      - After encoding the outer '{', StackDepth reports 1.
      - After encoding the inner '[', StackDepth reports 2.
      - After encoding the inner ']', StackDepth reports 1.
      - After encoding the outer '}', StackDepth reports 0.

func (e *Encoder) StackIndex(i int) (Kind, int64)
    StackIndex returns information about the specified stack level. It must
    be a number between 0 and Encoder.StackDepth, inclusive. For each level,
    it reports the kind:

      - KindInvalid for a level of zero,
      - KindBeginObject for a level representing a JSON object, and
      - KindBeginArray for a level representing a JSON array.

    It also reports the length of that JSON object or array encoded so far.
    Each name and value in a JSON object is counted separately, so the effective
    number of members is half the length. A complete JSON object must have an
    even length.

func (e *Encoder) StackPointer() Pointer
    StackPointer returns a JSON Pointer (RFC 6901) to the most recently written
    value.

func (e *Encoder) WriteToken(t Token) error
    WriteToken writes the next token and advances the internal write offset.

    The provided token kind must be consistent with the JSON grammar.
    For example, it is an error to provide a number when the encoder is
    expecting an object name (which is always a string), or to provide an end
    object delimiter when the encoder is finishing an array. If the provided
    token is invalid, then WriteToken reports a SyntacticError and the internal
    state remains unchanged. The offset reported in SyntacticError will be the
    Encoder.OutputOffset plus any delimiter or whitespace characters that would
    have preceded the provided token.

func (e *Encoder) WriteValue(v Value) error
    WriteValue writes the next raw value and advances the internal write
    offset. The Encoder does not simply copy the provided value verbatim,
    but parses it to ensure that it is syntactically valid and reformats it
    according to how the Encoder is configured to format whitespace and strings.
    If AllowInvalidUTF8 is specified, then any invalid UTF-8 is mangled as the
    Unicode replacement character, U+FFFD.

    The provided value kind must be consistent with the JSON grammar (see
    examples on Encoder.WriteToken). If the provided value is invalid,
    then WriteValue reports a SyntacticError and the internal state
    remains unchanged. The offset reported in SyntacticError will be the
    Encoder.OutputOffset plus the offset into v of any encountered syntax error.

type Kind byte
    A Kind represents the kind of a JSON token.

    A Kind is a single byte, which is conveniently the first byte of that kind's
    symbol in the grammar (except for numbers, which are always represented with
    '0').

const (
	KindInvalid     Kind = 0   // invalid kind
	KindNull        Kind = 'n' // null
	KindFalse       Kind = 'f' // false
	KindTrue        Kind = 't' // true
	KindString      Kind = '"' // string
	KindNumber      Kind = '0' // number
	KindBeginObject Kind = '{' // begin object
	KindEndObject   Kind = '}' // end object
	KindBeginArray  Kind = '[' // begin array
	KindEndArray    Kind = ']' // end array
)
func (k Kind) String() string
    String returns a string representation of k.

type Options = jsonopts.Options
    Options configures NewEncoder, Encoder.Reset, NewDecoder, and Decoder.Reset
    with specific features. Each function takes in a variadic list of options,
    where properties set in later options override the value of previously set
    properties.

    There is a single Options type, which is used with both encoding and
    decoding. Some options affect both operations, while others only affect one
    operation:

      - AllowDuplicateNames affects encoding and decoding
      - AllowInvalidUTF8 affects encoding and decoding
      - EscapeForHTML affects encoding only
      - EscapeForJS affects encoding only
      - PreserveRawStrings affects encoding only
      - CanonicalizeRawInts affects encoding only
      - CanonicalizeRawFloats affects encoding only
      - ReorderRawObjects affects encoding only
      - SpaceAfterColon affects encoding only
      - SpaceAfterComma affects encoding only
      - Multiline affects encoding only
      - WithIndent affects encoding only
      - WithIndentPrefix affects encoding only

    Options that do not affect a particular operation are ignored.

    The Options type is identical to encoding/json.Options and
    encoding/json/v2.Options. Options from the other packages may be passed to
    functionality in this package, but are ignored. Options from this package
    may be used with the other packages.

func AllowDuplicateNames(v bool) Options
    AllowDuplicateNames specifies that JSON objects may contain duplicate member
    names. Disabling the duplicate name check may provide performance benefits,
    but breaks compliance with RFC 7493, section 2.3. The input or output will
    still be compliant with RFC 8259, which leaves the handling of duplicate
    names as unspecified behavior.

    This affects either encoding or decoding.

func AllowInvalidUTF8(v bool) Options
    AllowInvalidUTF8 specifies that JSON strings may contain invalid UTF-8,
    which will be mangled as the Unicode replacement character, U+FFFD.
    This causes the encoder or decoder to break compliance with RFC 7493,
    section 2.1, and RFC 8259, section 8.1.

    This affects either encoding or decoding.

func CanonicalizeRawFloats(v bool) Options
    CanonicalizeRawFloats specifies that when encoding a raw JSON floating-point
    number (i.e., a number with a fraction or exponent) in a Token or Value,
    the number is canonicalized according to RFC 8785, section 3.2.2.3. As a
    special case, the number -0 is canonicalized as 0.

    JSON numbers are treated as IEEE 754 double precision numbers. It is safe
    to canonicalize a serialized single precision number and parse it back as
    a single precision number and expect the same value. If a number exceeds
    ±1.7976931348623157e+308, which is the maximum finite number, then it is
    saturated at that value and formatted as such.

    This only affects encoding and is ignored when decoding.

func CanonicalizeRawInts(v bool) Options
    CanonicalizeRawInts specifies that when encoding a raw JSON integer number
    (i.e., a number without a fraction and exponent) in a Token or Value,
    the number is canonicalized according to RFC 8785, section 3.2.2.3. As a
    special case, the number -0 is canonicalized as 0.

    JSON numbers are treated as IEEE 754 double precision numbers. Any numbers
    with precision beyond what is representable by that form will lose their
    precision when canonicalized. For example, integer values beyond ±2⁵³ will
    lose their precision. For example, 1234567890123456789 is formatted as
    1234567890123456800.

    This only affects encoding and is ignored when decoding.

func EscapeForHTML(v bool) Options
    EscapeForHTML specifies that '<', '>', and '&' characters within JSON
    strings should be escaped as a hexadecimal Unicode codepoint (e.g., \u003c)
    so that the output is safe to embed within HTML.

    This only affects encoding and is ignored when decoding.

func EscapeForJS(v bool) Options
    EscapeForJS specifies that U+2028 and U+2029 characters within JSON strings
    should be escaped as a hexadecimal Unicode codepoint (e.g., \u2028) so that
    the output is valid to embed within JavaScript. See RFC 8259, section 12.

    This only affects encoding and is ignored when decoding.

func Multiline(v bool) Options
    Multiline specifies that the JSON output should expand to multiple lines,
    where every JSON object member or JSON array element appears on a new,
    indented line according to the nesting depth.

    If SpaceAfterColon is not specified, then the default is true. If
    SpaceAfterComma is not specified, then the default is false. If WithIndent
    is not specified, then the default is "\t".

    If set to false, then the output is a single line, where the only whitespace
    emitted is determined by the current values of SpaceAfterColon and
    SpaceAfterComma.

    This only affects encoding and is ignored when decoding.

func PreserveRawStrings(v bool) Options
    PreserveRawStrings specifies that when encoding a raw JSON string in a
    Token or Value, pre-escaped sequences in a JSON string are preserved to the
    output. However, raw strings still respect EscapeForHTML and EscapeForJS
    such that the relevant characters are escaped. If AllowInvalidUTF8 is
    enabled, bytes of invalid UTF-8 are preserved to the output.

    This only affects encoding and is ignored when decoding.

func ReorderRawObjects(v bool) Options
    ReorderRawObjects specifies that when encoding a raw JSON object in a Value,
    the object members are reordered according to RFC 8785, section 3.2.3.

    This only affects encoding and is ignored when decoding.

func SpaceAfterColon(v bool) Options
    SpaceAfterColon specifies that the JSON output should emit a space character
    after each colon separator following a JSON object name. If false, then no
    space character appears after the colon separator.

    This only affects encoding and is ignored when decoding.

func SpaceAfterComma(v bool) Options
    SpaceAfterComma specifies that the JSON output should emit a space character
    after each comma separator following a JSON object value or array element.
    If false, then no space character appears after the comma separator.

    This only affects encoding and is ignored when decoding.

func WithIndent(indent string) Options
    WithIndent specifies that the encoder should emit multiline output where
    each element in a JSON object or array begins on a new, indented line
    beginning with the indent prefix (see WithIndentPrefix) followed by one or
    more copies of indent according to the nesting depth. The indent must be
    composed of only space and tab characters.

    If the intent is to emit indented output without a preference for the
    particular indent string, then use Multiline instead.

    This only affects encoding and is ignored when decoding. Use of this option
    implies Multiline being set to true.

func WithIndentPrefix(prefix string) Options
    WithIndentPrefix specifies that the encoder should emit multiline output
    where each element in a JSON object or array begins on a new, indented line
    beginning with the indent prefix followed by one or more copies of indent
    (see WithIndent) according to the nesting depth. The prefix must be composed
    of only space and tab characters.

    This only affects encoding and is ignored when decoding. Use of this option
    implies Multiline being set to true.

type Pointer string
    Pointer is a JSON Pointer (RFC 6901) that references a particular JSON value
    relative to the root of the top-level JSON value.

    A Pointer is a slash-separated list of tokens, where each token is either
    a JSON object name or an index to a JSON array element encoded as a base-10
    integer value. It is impossible to distinguish between an array index and
    an object name (that happens to be a base-10 encoded integer) without also
    knowing the structure of the top-level JSON value that the pointer refers
    to.

    There is exactly one representation of a pointer to a particular value,
    so comparability of Pointer values is equivalent to checking whether they
    both point to the same value.

func (p Pointer) AppendToken(tok string) Pointer
    AppendToken appends a token to the end of p and returns the full pointer.

func (p Pointer) Contains(pc Pointer) bool
    Contains reports whether the JSON value that p points to is equal to or
    contains the JSON value that pc points to.

func (p Pointer) IsValid() bool
    IsValid reports whether p is a valid JSON Pointer according to RFC 6901.
    Note that the concatenation of two valid pointers produces a valid pointer.

func (p Pointer) LastToken() string
    LastToken returns the last token in the pointer. The last token of an empty
    Pointer is the empty string.

func (p Pointer) Parent() Pointer
    Parent strips off the last token and returns the remaining pointer.
    The parent of an empty Pointer is the empty string.

func (p Pointer) Tokens() iter.Seq[string]
    Tokens returns an iterator over the reference tokens in the JSON pointer,
    from first to last.

type SyntacticError struct {

	// ByteOffset indicates that an error occurred at or after this byte offset.
	ByteOffset int64
	// JSONPointer indicates that an error occurred within this JSON value
	// as indicated using the JSON Pointer notation (see RFC 6901).
	JSONPointer Pointer

	// Err is the underlying error.
	Err error
	// Has unexported fields.
}
    SyntacticError is a description of an error that occurred when encoding or
    decoding JSON according to the grammar.

    The contents of this error as produced by this package may change over time.

func (e *SyntacticError) Error() string

func (e *SyntacticError) Unwrap() error

type Token struct {
	// Has unexported fields.
}
    Token represents a lexical JSON token, which may be one of the following:
      - a JSON literal (i.e., null, true, or false)
      - a JSON string (e.g., "hello, world!")
      - a JSON number (e.g., 123.456)
      - a begin or end delimiter for a JSON object (i.e., { or } )
      - a begin or end delimiter for a JSON array (i.e., [ or ] )

    A Token cannot represent entire array or object values, while a Value can.
    There is no Token to represent commas and colons since these structural
    tokens can be inferred from the surrounding context.

    A Token stores data in one of two forms:

      - As raw JSON text: backed by the internal buffer of the Decoder and only
        ever produced by Decoder.ReadToken. Such a token is only valid until
        the next call to any method on that Decoder (e.g., Decoder.PeekKind,
        Decoder.ReadToken, Decoder.ReadValue, or Decoder.SkipValue). Call
        Token.Clone to copy the raw text into an independent allocation that
        persists beyond subsequent Decoder calls.

      - As a typed Go value: a self-contained representation produced by the
        constructor functions (e.g., String, Int, Uint, Float). Such tokens are
        valid indefinitely and do not need to be cloned.

var (
	Null  Token = rawToken("null")
	False Token = rawToken("false")
	True  Token = rawToken("true")

	BeginObject Token = rawToken("{")
	EndObject   Token = rawToken("}")
	BeginArray  Token = rawToken("[")
	EndArray    Token = rawToken("]")
)
func Bool(b bool) Token
    Bool constructs a Token representing a JSON boolean.

func Float(n float64) Token
    Float constructs a Token representing a JSON number as a 64-bit
    floating-point number formatted according to ECMA-262, 10th edition,
    section 7.1.12.1 and RFC 8785, section 3.2.2.3. with the exception that -0
    is still formatted as -0. The values NaN, +Inf, and -Inf will be represented
    as a JSON string with the values "NaN", "Infinity", and "-Infinity".

func Float32(n float32) Token
    Float32 constructs a Token representing a JSON number as a 32-bit
    floating-point number formatted according to ECMA-262, 10th edition,
    section 7.1.12.1, with the exception that -0 is still formatted as -0.
    The values NaN, +Inf, and -Inf will be represented as a JSON string with the
    values "NaN", "Infinity", and "-Infinity".

    Note that most JSON libraries and standards assume that JSON numbers are
    64-bit floating-point numbers. Use of 32-bit precision should only be used
    if the corresponding decoder knows that this JSON number token is expected
    to only have 32-bit precision. For all other situations, prefer using the
    Float constructor instead.

func Int(n int64) Token
    Int constructs a Token representing a JSON number from an int64.

func String(s string) Token
    String constructs a Token representing a JSON string. The provided string
    should contain valid UTF-8, otherwise invalid characters may be mangled as
    the Unicode replacement character.

func Uint(n uint64) Token
    Uint constructs a Token representing a JSON number from a uint64.

func (t Token) Bool() bool
    Bool returns the value for a JSON boolean. It panics if the token kind is
    not a JSON boolean.

func (t Token) Clone() Token
    Clone returns a copy of the token with a value that is not backed by the
    Decoder buffer and therefore remains valid past subsequent Decoder calls.
    It has no effect on tokens produced by constructor functions, since those
    are already self-contained.

func (t Token) Float() (float64, error)
    Float returns the floating-point value for a JSON number parsed according to
    64 bits of precision.

    If the JSON number is outside the representable range of a float64,
    it returns +Inf or -Inf along with an error that matches strconv.ErrRange
    according to errors.Is.

    It returns a NaN, +Inf, or -Inf value for any JSON string with the values
    "NaN", "Infinity", or "-Infinity".

    It panics if the token kind is not a JSON number or a JSON string with the
    aforementioned values.

func (t Token) Float32() (float32, error)
    Float32 returns the floating-point value for a JSON number parsed according
    to 32 bits of precision.

    If the JSON number is outside the representable range of a float32,
    it returns +Inf or -Inf along with an error that matches strconv.ErrRange
    according to errors.Is.

    It returns a NaN, +Inf, or -Inf value for any JSON string with the values
    "NaN", "Infinity", or "-Infinity".

    It panics if the token kind is not a JSON number or a JSON string with the
    aforementioned values.

    Note that most JSON libraries and standards assume that JSON numbers are
    64-bit floating-point numbers. This method should only be used if the caller
    knows from other context that this token is a JSON number formatted only to
    32 bits of precision (such as being encoded using the Float32 constructor).
    For all other situations, prefer using the Token.Float accessor instead.

func (t Token) Int() (int64, error)
    Int returns the signed integer value for a JSON number.

    It reports an error that matches strconv.ErrSyntax according to errors.Is
    if the JSON number does not match the restricted grammar of just a signed
    integer. It reports an error that matches strconv.ErrRange according to
    errors.Is if the JSON number is a signed integer, but outside the range
    of an int64. Even if an error is reported, a reasonable value is still
    returned. The fractional component of any number is ignored (truncation
    toward zero). Any number beyond the representation of an int64 will be
    saturated to the closest representable value.

    It panics if the token kind is not a JSON number.

func (t Token) Kind() Kind
    Kind returns the token kind.

func (t Token) String() string
    String returns the unescaped string value for a JSON string. For other JSON
    kinds, this returns the raw JSON representation.

func (t Token) Uint() (uint64, error)
    Uint returns the unsigned integer value for a JSON number.

    It reports an error that matches strconv.ErrSyntax if the JSON number
    does not match the restricted grammar of just an unsigned integer.
    It reports an error that matches strconv.ErrRange if the JSON number is
    an unsigned integer, but outside the representable range of a uint64.
    Even if an error is reported, a reasonable value is still returned.
    The fractional component of any number is ignored (truncation toward zero).
    Any number beyond the representation of a uint64 will be saturated to the
    closest representable value.

    It panics if the token kind is not a JSON number.

type Value []byte
    Value represents a single raw JSON value, which may be one of the following:
      - a JSON literal (i.e., null, true, or false)
      - a JSON string (e.g., "hello, world!")
      - a JSON number (e.g., 123.456)
      - an entire JSON object (e.g., {"fizz":"buzz"} )
      - an entire JSON array (e.g., [1,2,3] )

    Value can represent entire array or object values, while Token cannot.
    Value may contain leading and/or trailing whitespace.

func (v *Value) Canonicalize(opts ...Options) error
    Canonicalize canonicalizes the raw JSON value according to the JSON
    Canonicalization Scheme (JCS) as defined by RFC 8785. Canonicalization
    produces a JSON value with the same meaning as the original, but is stable
    in the sense that calling Canonicalize on a canonicalized value does
    nothing.

    JSON strings are formatted to use their minimal representation, JSON
    numbers are formatted as double precision numbers according to some stable
    serialization algorithm. JSON object members are sorted in ascending order
    by name. All whitespace is removed.

    Canonicalize is equivalent to calling Value.Format with the following
    options:
      - CanonicalizeRawInts(true)
      - CanonicalizeRawFloats(true)
      - ReorderRawObjects(true)

    Any options specified by the caller are applied after the initial set and
    may deliberately override prior options.

    Note that JCS treats all JSON numbers as IEEE 754 double precision numbers.
    Any numbers with precision beyond what is representable by that form will
    lose their precision when canonicalized. For example, integer values beyond
    ±2⁵³ will lose their precision. To preserve the original representation of
    JSON integers, additionally set CanonicalizeRawInts to false:

        v.Canonicalize(jsontext.CanonicalizeRawInts(false))

func (v Value) Clone() Value
    Clone returns a copy of v.

func (v *Value) Compact(opts ...Options) error
    Compact removes all whitespace from the raw JSON value.

    It does not reformat JSON strings or numbers to use any other
    representation. To maximize the set of JSON values that can be formatted,
    it permits values with duplicate names and invalid UTF-8.

    Compact is equivalent to calling Value.Format with the following options:
      - AllowDuplicateNames(true)
      - AllowInvalidUTF8(true)
      - PreserveRawStrings(true)

    Any options specified by the caller are applied after the initial set and
    may deliberately override prior options.

func (v *Value) Format(opts ...Options) error
    Format formats the raw JSON value in place.

    By default (if no options are specified), it validates according to RFC 7493
    and produces the minimal JSON representation, where all whitespace is elided
    and JSON strings use the shortest encoding.

    Relevant options include:
      - AllowDuplicateNames
      - AllowInvalidUTF8
      - EscapeForHTML
      - EscapeForJS
      - PreserveRawStrings
      - CanonicalizeRawInts
      - CanonicalizeRawFloats
      - ReorderRawObjects
      - SpaceAfterColon
      - SpaceAfterComma
      - Multiline
      - WithIndent
      - WithIndentPrefix

    All other options are ignored.

    It is guaranteed to succeed if the value is valid according to the same
    options. If the value is already formatted, then the buffer is not mutated.

func (v *Value) Indent(opts ...Options) error
    Indent reformats the whitespace in the raw JSON value so that each element
    in a JSON object or array begins on an indented line according to the
    nesting.

    It does not reformat JSON strings or numbers to use any other
    representation. To maximize the set of JSON values that can be formatted,
    it permits values with duplicate names and invalid UTF-8.

    Indent is equivalent to calling Value.Format with the following options:
      - AllowDuplicateNames(true)
      - AllowInvalidUTF8(true)
      - PreserveRawStrings(true)
      - Multiline(true)

    Any options specified by the caller are applied after the initial set and
    may deliberately override prior options.

func (v Value) IsValid(opts ...Options) bool
    IsValid reports whether the raw JSON value is syntactically valid according
    to the specified options.

    By default (if no options are specified), it validates according to RFC
    7493. It verifies whether the input is properly encoded as UTF-8, that
    escape sequences within strings decode to valid Unicode codepoints, and that
    all names in each object are unique. It does not verify whether numbers are
    representable within the limits of any common numeric type (e.g., float64,
    int64, or uint64).

    Relevant options include:
      - AllowDuplicateNames
      - AllowInvalidUTF8

    All other options are ignored.

func (v Value) Kind() Kind
    Kind returns the starting token kind. For a valid value, this will never
    include KindEndObject or KindEndArray.

func (v Value) MarshalJSON() ([]byte, error)
    MarshalJSON returns v as the JSON encoding of v. It performs no validation.
    If v is nil, then this returns a JSON null.

func (v Value) String() string
    String returns the string formatting of v.

func (v *Value) UnmarshalJSON(b []byte) error
    UnmarshalJSON sets v as the JSON encoding of b. It stores a copy of the
    provided raw JSON input without any validation.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
