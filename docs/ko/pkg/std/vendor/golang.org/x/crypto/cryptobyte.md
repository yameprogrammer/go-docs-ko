# package vendor/golang.org/x/crypto/cryptobyte

- 원문: <https://pkg.go.dev/vendor/golang.org/x/crypto/cryptobyte>
- 분류: Go 표준 라이브러리

## 한국어 요약

`cryptobyte` 패키지는 ASN.1 DER를 포함하여, 길이 접두사가 붙은 바이너리 메시지를 파싱하고 구성하는 데 도움이 되는 타입들을 제공합니다.

## 원문 요약

Package cryptobyte contains types that help with parsing and constructing length-prefixed, binary messages, including ASN.1 DER.

## API 상세 (go doc -all)

~~~text
package cryptobyte // import "vendor/golang.org/x/crypto/cryptobyte"

Package cryptobyte contains types that help with parsing and constructing
length-prefixed, binary messages, including ASN.1 DER. (The asn1 subpackage
contains useful ASN.1 constants.)

The String type is for parsing. It wraps a []byte slice and provides helper
functions for consuming structures, value by value.

The Builder type is for constructing messages. It providers helper functions for
appending values and also for appending length-prefixed submessages – without
having to worry about calculating the length prefix ahead of time.

See the documentation and examples for the Builder and String types to get
started.

TYPES

type BuildError struct {
	Err error
}
    BuildError wraps an error. If a BuilderContinuation panics with this value,
    the panic will be recovered and the inner error will be returned from
    Builder.Bytes.

type Builder struct {
	// Has unexported fields.
}
    A Builder builds byte strings from fixed-length and length-prefixed values.
    Builders either allocate space as needed, or are ‘fixed’, which means that
    they write into a given buffer and produce an error if it's exhausted.

    The zero value is a usable Builder that allocates space as needed.

    Simple values are marshaled and appended to a Builder using methods
    on the Builder. Length-prefixed values are marshaled by providing a
    BuilderContinuation, which is a function that writes the inner contents of
    the value to a given Builder. See the documentation for BuilderContinuation
    for details.

func NewBuilder(buffer []byte) *Builder
    NewBuilder creates a Builder that appends its output to the given buffer.
    Like append(), the slice will be reallocated if its capacity is exceeded.
    Use Bytes to get the final buffer.

func NewFixedBuilder(buffer []byte) *Builder
    NewFixedBuilder creates a Builder that appends its output into the given
    buffer. This builder does not reallocate the output buffer. Writes that
    would exceed the buffer's capacity are treated as an error.

func (b *Builder) AddASN1(tag asn1.Tag, f BuilderContinuation)
    AddASN1 appends an ASN.1 object. The object is prefixed with the given tag.
    Tags greater than 30 are not supported and result in an error (i.e.
    low-tag-number form only). The child builder passed to the
    BuilderContinuation can be used to build the content of the ASN.1 object.

func (b *Builder) AddASN1BigInt(n *big.Int)
    AddASN1BigInt appends a DER-encoded ASN.1 INTEGER.

func (b *Builder) AddASN1BitString(data []byte)
    AddASN1BitString appends a DER-encoded ASN.1 BIT STRING. This does not
    support BIT STRINGs that are not a whole number of bytes.

func (b *Builder) AddASN1Boolean(v bool)

func (b *Builder) AddASN1Enum(v int64)
    AddASN1Enum appends a DER-encoded ASN.1 ENUMERATION.

func (b *Builder) AddASN1GeneralizedTime(t time.Time)
    AddASN1GeneralizedTime appends a DER-encoded ASN.1 GENERALIZEDTIME.

func (b *Builder) AddASN1Int64(v int64)
    AddASN1Int64 appends a DER-encoded ASN.1 INTEGER.

func (b *Builder) AddASN1Int64WithTag(v int64, tag asn1.Tag)
    AddASN1Int64WithTag appends a DER-encoded ASN.1 INTEGER with the given tag.

func (b *Builder) AddASN1NULL()

func (b *Builder) AddASN1ObjectIdentifier(oid encoding_asn1.ObjectIdentifier)

func (b *Builder) AddASN1OctetString(bytes []byte)
    AddASN1OctetString appends a DER-encoded ASN.1 OCTET STRING.

func (b *Builder) AddASN1UTCTime(t time.Time)
    AddASN1UTCTime appends a DER-encoded ASN.1 UTCTime.

func (b *Builder) AddASN1Uint64(v uint64)
    AddASN1Uint64 appends a DER-encoded ASN.1 INTEGER.

func (b *Builder) AddBytes(v []byte)
    AddBytes appends a sequence of bytes to the byte string.

func (b *Builder) AddUint16(v uint16)
    AddUint16 appends a big-endian, 16-bit value to the byte string.

func (b *Builder) AddUint16LengthPrefixed(f BuilderContinuation)
    AddUint16LengthPrefixed adds a big-endian, 16-bit length-prefixed byte
    sequence.

func (b *Builder) AddUint24(v uint32)
    AddUint24 appends a big-endian, 24-bit value to the byte string. The highest
    byte of the 32-bit input value is silently truncated.

func (b *Builder) AddUint24LengthPrefixed(f BuilderContinuation)
    AddUint24LengthPrefixed adds a big-endian, 24-bit length-prefixed byte
    sequence.

func (b *Builder) AddUint32(v uint32)
    AddUint32 appends a big-endian, 32-bit value to the byte string.

func (b *Builder) AddUint32LengthPrefixed(f BuilderContinuation)
    AddUint32LengthPrefixed adds a big-endian, 32-bit length-prefixed byte
    sequence.

func (b *Builder) AddUint48(v uint64)
    AddUint48 appends a big-endian, 48-bit value to the byte string.

func (b *Builder) AddUint64(v uint64)
    AddUint64 appends a big-endian, 64-bit value to the byte string.

func (b *Builder) AddUint8(v uint8)
    AddUint8 appends an 8-bit value to the byte string.

func (b *Builder) AddUint8LengthPrefixed(f BuilderContinuation)
    AddUint8LengthPrefixed adds a 8-bit length-prefixed byte sequence.

func (b *Builder) AddValue(v MarshalingValue)
    AddValue calls Marshal on v, passing a pointer to the builder to append to.
    If Marshal returns an error, it is set on the Builder so that subsequent
    appends don't have an effect.

func (b *Builder) Bytes() ([]byte, error)
    Bytes returns the bytes written by the builder or an error if one has
    occurred during building.

func (b *Builder) BytesOrPanic() []byte
    BytesOrPanic returns the bytes written by the builder or panics if an error
    has occurred during building.

func (b *Builder) MarshalASN1(v interface{})
    MarshalASN1 calls encoding_asn1.Marshal on its input and appends the result
    if successful or records an error if one occurred.

func (b *Builder) SetError(err error)
    SetError sets the value to be returned as the error from Bytes. Writes
    performed after calling SetError are ignored.

func (b *Builder) Unwrite(n int)
    Unwrite rolls back non-negative n bytes written directly to the Builder.
    An attempt by a child builder passed to a continuation to unwrite bytes from
    its parent will panic.

type BuilderContinuation func(child *Builder)
    BuilderContinuation is a continuation-passing interface for building
    length-prefixed byte sequences. Builder methods for length-prefixed
    sequences (AddUint8LengthPrefixed etc) will invoke the BuilderContinuation
    supplied to them. The child builder passed to the continuation can be used
    to build the content of the length-prefixed sequence. For example:

        parent := cryptobyte.NewBuilder()
        parent.AddUint8LengthPrefixed(func (child *Builder) {
          child.AddUint8(42)
          child.AddUint8LengthPrefixed(func (grandchild *Builder) {
            grandchild.AddUint8(5)
          })
        })

    It is an error to write more bytes to the child than allowed by the reserved
    length prefix. After the continuation returns, the child must be considered
    invalid, i.e. users must not store any copies or references of the child
    that outlive the continuation.

    If the continuation panics with a value of type BuildError then the
    inner error will be returned as the error from Bytes. If the child panics
    otherwise then Bytes will repanic with the same value.

type MarshalingValue interface {
	// Marshal is called by Builder.AddValue. It receives a pointer to a builder
	// to marshal itself into. It may return an error that occurred during
	// marshaling, such as unset or invalid values.
	Marshal(b *Builder) error
}
    A MarshalingValue marshals itself into a Builder.

type String []byte
    String represents a string of bytes. It provides methods for parsing
    fixed-length and length-prefixed values from it.

func (s *String) CopyBytes(out []byte) bool
    CopyBytes copies len(out) bytes into out and advances over them. It reports
    whether the copy operation was successful

func (s String) Empty() bool
    Empty reports whether the string does not contain any bytes.

func (s String) PeekASN1Tag(tag asn1.Tag) bool
    PeekASN1Tag reports whether the next ASN.1 value on the string starts with
    the given tag.

func (s *String) ReadASN1(out *String, tag asn1.Tag) bool
    ReadASN1 reads the contents of a DER-encoded ASN.1 element (not including
    tag and length bytes) into out, and advances. The element must match the
    given tag. It reports whether the read was successful.

    Tags greater than 30 are not supported (i.e. low-tag-number format only).

func (s *String) ReadASN1BitString(out *encoding_asn1.BitString) bool
    ReadASN1BitString decodes an ASN.1 BIT STRING into out and advances.
    It reports whether the read was successful.

func (s *String) ReadASN1BitStringAsBytes(out *[]byte) bool
    ReadASN1BitStringAsBytes decodes an ASN.1 BIT STRING into out and advances.
    It is an error if the BIT STRING is not a whole number of bytes. It reports
    whether the read was successful.

func (s *String) ReadASN1Boolean(out *bool) bool
    ReadASN1Boolean decodes an ASN.1 BOOLEAN and converts it to a boolean
    representation into out and advances. It reports whether the read was
    successful.

func (s *String) ReadASN1Bytes(out *[]byte, tag asn1.Tag) bool
    ReadASN1Bytes reads the contents of a DER-encoded ASN.1 element (not
    including tag and length bytes) into out, and advances. The element must
    match the given tag. It reports whether the read was successful.

func (s *String) ReadASN1Element(out *String, tag asn1.Tag) bool
    ReadASN1Element reads the contents of a DER-encoded ASN.1 element (including
    tag and length bytes) into out, and advances. The element must match the
    given tag. It reports whether the read was successful.

    Tags greater than 30 are not supported (i.e. low-tag-number format only).

func (s *String) ReadASN1Enum(out *int) bool
    ReadASN1Enum decodes an ASN.1 ENUMERATION into out and advances. It reports
    whether the read was successful.

func (s *String) ReadASN1GeneralizedTime(out *time.Time) bool
    ReadASN1GeneralizedTime decodes an ASN.1 GENERALIZEDTIME into out and
    advances. It reports whether the read was successful.

func (s *String) ReadASN1Int64WithTag(out *int64, tag asn1.Tag) bool
    ReadASN1Int64WithTag decodes an ASN.1 INTEGER with the given tag into out
    and advances. It reports whether the read was successful and resulted in a
    value that can be represented in an int64.

func (s *String) ReadASN1Integer(out interface{}) bool
    ReadASN1Integer decodes an ASN.1 INTEGER into out and advances. If out
    does not point to an integer, to a big.Int, or to a []byte it panics. Only
    positive and zero values can be decoded into []byte, and they are returned
    as big-endian binary values that share memory with s. Positive values will
    have no leading zeroes, and zero will be returned as a single zero byte.
    ReadASN1Integer reports whether the read was successful.

func (s *String) ReadASN1ObjectIdentifier(out *encoding_asn1.ObjectIdentifier) bool
    ReadASN1ObjectIdentifier decodes an ASN.1 OBJECT IDENTIFIER into out and
    advances. It reports whether the read was successful.

func (s *String) ReadASN1UTCTime(out *time.Time) bool
    ReadASN1UTCTime decodes an ASN.1 UTCTime into out and advances. It reports
    whether the read was successful.

func (s *String) ReadAnyASN1(out *String, outTag *asn1.Tag) bool
    ReadAnyASN1 reads the contents of a DER-encoded ASN.1 element (not including
    tag and length bytes) into out, sets outTag to its tag, and advances.
    It reports whether the read was successful.

    Tags greater than 30 are not supported (i.e. low-tag-number format only).

func (s *String) ReadAnyASN1Element(out *String, outTag *asn1.Tag) bool
    ReadAnyASN1Element reads the contents of a DER-encoded ASN.1 element
    (including tag and length bytes) into out, sets outTag to is tag, and
    advances. It reports whether the read was successful.

    Tags greater than 30 are not supported (i.e. low-tag-number format only).

func (s *String) ReadBytes(out *[]byte, n int) bool
    ReadBytes reads n bytes into out and advances over them. It reports whether
    the read was successful.

func (s *String) ReadOptionalASN1(out *String, outPresent *bool, tag asn1.Tag) bool
    ReadOptionalASN1 attempts to read the contents of a DER-encoded ASN.1
    element (not including tag and length bytes) tagged with the given tag into
    out. It stores whether an element with the tag was found in outPresent,
    unless outPresent is nil. It reports whether the read was successful.

func (s *String) ReadOptionalASN1Boolean(out *bool, tag asn1.Tag, defaultValue bool) bool
    ReadOptionalASN1Boolean attempts to read an optional ASN.1 BOOLEAN
    explicitly tagged with tag into out and advances. If no element with a
    matching tag is present, it sets "out" to defaultValue instead. It reports
    whether the read was successful.

func (s *String) ReadOptionalASN1Integer(out interface{}, tag asn1.Tag, defaultValue interface{}) bool
    ReadOptionalASN1Integer attempts to read an optional ASN.1 INTEGER
    explicitly tagged with tag into out and advances. If no element with a
    matching tag is present, it writes defaultValue into out instead. Otherwise,
    it behaves like ReadASN1Integer.

func (s *String) ReadOptionalASN1OctetString(out *[]byte, outPresent *bool, tag asn1.Tag) bool
    ReadOptionalASN1OctetString attempts to read an optional ASN.1 OCTET STRING
    explicitly tagged with tag into out and advances. If no element with a
    matching tag is present, it sets "out" to nil instead. It reports whether
    the read was successful.

func (s *String) ReadUint16(out *uint16) bool
    ReadUint16 decodes a big-endian, 16-bit value into out and advances over it.
    It reports whether the read was successful.

func (s *String) ReadUint16LengthPrefixed(out *String) bool
    ReadUint16LengthPrefixed reads the content of a big-endian, 16-bit
    length-prefixed value into out and advances over it. It reports whether the
    read was successful.

func (s *String) ReadUint24(out *uint32) bool
    ReadUint24 decodes a big-endian, 24-bit value into out and advances over it.
    It reports whether the read was successful.

func (s *String) ReadUint24LengthPrefixed(out *String) bool
    ReadUint24LengthPrefixed reads the content of a big-endian, 24-bit
    length-prefixed value into out and advances over it. It reports whether the
    read was successful.

func (s *String) ReadUint32(out *uint32) bool
    ReadUint32 decodes a big-endian, 32-bit value into out and advances over it.
    It reports whether the read was successful.

func (s *String) ReadUint48(out *uint64) bool
    ReadUint48 decodes a big-endian, 48-bit value into out and advances over it.
    It reports whether the read was successful.

func (s *String) ReadUint64(out *uint64) bool
    ReadUint64 decodes a big-endian, 64-bit value into out and advances over it.
    It reports whether the read was successful.

func (s *String) ReadUint8(out *uint8) bool
    ReadUint8 decodes an 8-bit value into out and advances over it. It reports
    whether the read was successful.

func (s *String) ReadUint8LengthPrefixed(out *String) bool
    ReadUint8LengthPrefixed reads the content of an 8-bit length-prefixed value
    into out and advances over it. It reports whether the read was successful.

func (s *String) Skip(n int) bool
    Skip advances the String by n byte and reports whether it was successful.

func (s *String) SkipASN1(tag asn1.Tag) bool
    SkipASN1 reads and discards an ASN.1 element with the given tag. It reports
    whether the operation was successful.

func (s *String) SkipOptionalASN1(tag asn1.Tag) bool
    SkipOptionalASN1 advances s over an ASN.1 element with the given tag,
    or else leaves s unchanged. It reports whether the operation was successful.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
