# package vendor/golang.org/x/net/http2/hpack

- 원문: <https://pkg.go.dev/vendor/golang.org/x/net/http2/hpack>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 hpack은 HPACK을 구현합니다. HPACK은 HTTP/2의 맥락에서 HTTP 헤더 필드를 효율적으로 표현하기 위한 압축 형식입니다.

## 원문 요약

Package hpack implements HPACK, a compression format for efficiently representing HTTP header fields in the context of HTTP/2.

## API 상세 (go doc -all)

~~~text
package hpack // import "vendor/golang.org/x/net/http2/hpack"

Package hpack implements HPACK, a compression format for efficiently
representing HTTP header fields in the context of HTTP/2.

See http://tools.ietf.org/html/draft-ietf-httpbis-header-compression-09

VARIABLES

var ErrInvalidHuffman = errors.New("hpack: invalid Huffman-encoded data")
    ErrInvalidHuffman is returned for errors found decoding Huffman-encoded
    strings.

var ErrStringLength = errors.New("hpack: string too long")
    ErrStringLength is returned by Decoder.Write when the max string length (as
    configured by Decoder.SetMaxStringLength) would be violated.


FUNCTIONS

func AppendHuffmanString(dst []byte, s string) []byte
    AppendHuffmanString appends s, as encoded in Huffman codes, to dst and
    returns the extended buffer.

func HuffmanDecode(w io.Writer, v []byte) (int, error)
    HuffmanDecode decodes the string in v and writes the expanded result to w,
    returning the number of bytes written to w and the Write call's return
    value. At most one Write call is made.

func HuffmanDecodeToString(v []byte) (string, error)
    HuffmanDecodeToString decodes the string in v.

func HuffmanEncodeLength(s string) uint64
    HuffmanEncodeLength returns the number of bytes required to encode s in
    Huffman codes. The result is round up to byte boundary.


TYPES

type Decoder struct {
	// Has unexported fields.
}
    A Decoder is the decoding context for incremental processing of header
    blocks.

func NewDecoder(maxDynamicTableSize uint32, emitFunc func(f HeaderField)) *Decoder
    NewDecoder returns a new decoder with the provided maximum dynamic table
    size. The emitFunc will be called for each valid field parsed, in the same
    goroutine as calls to Write, before Write returns.

func (d *Decoder) Close() error
    Close declares that the decoding is complete and resets the Decoder to be
    reused again for a new header block. If there is any remaining data in the
    decoder's buffer, Close returns an error.

func (d *Decoder) DecodeFull(p []byte) ([]HeaderField, error)
    DecodeFull decodes an entire block.

    TODO: remove this method and make it incremental later? This is easier for
    debugging now.

func (d *Decoder) EmitEnabled() bool
    EmitEnabled reports whether calls to the emitFunc provided to NewDecoder are
    currently enabled. The default is true.

func (d *Decoder) SetAllowedMaxDynamicTableSize(v uint32)
    SetAllowedMaxDynamicTableSize sets the upper bound that the encoded stream
    (via dynamic table size updates) may set the maximum size to.

func (d *Decoder) SetEmitEnabled(v bool)
    SetEmitEnabled controls whether the emitFunc provided to NewDecoder should
    be called. The default is true.

    This facility exists to let servers enforce MAX_HEADER_LIST_SIZE while
    still decoding and keeping in-sync with decoder state, but without doing
    unnecessary decompression or generating unnecessary garbage for header
    fields past the limit.

func (d *Decoder) SetEmitFunc(emitFunc func(f HeaderField))
    SetEmitFunc changes the callback used when new header fields are decoded.
    It must be non-nil. It does not affect EmitEnabled.

func (d *Decoder) SetMaxDynamicTableSize(v uint32)

func (d *Decoder) SetMaxStringLength(n int)
    SetMaxStringLength sets the maximum size of a HeaderField name or value
    string. If a string exceeds this length (even after any decompression),
    Write will return ErrStringLength. A value of 0 means unlimited and is the
    default from NewDecoder.

func (d *Decoder) Write(p []byte) (n int, err error)

type DecodingError struct {
	Err error
}
    A DecodingError is something the spec defines as a decoding error.

func (de DecodingError) Error() string

type Encoder struct {
	// Has unexported fields.
}

func NewEncoder(w io.Writer) *Encoder
    NewEncoder returns a new Encoder which performs HPACK encoding. An encoded
    data is written to w.

func (e *Encoder) MaxDynamicTableSize() (v uint32)
    MaxDynamicTableSize returns the current dynamic header table size.

func (e *Encoder) SetMaxDynamicTableSize(v uint32)
    SetMaxDynamicTableSize changes the dynamic header table size to v. The
    actual size is bounded by the value passed to SetMaxDynamicTableSizeLimit.

func (e *Encoder) SetMaxDynamicTableSizeLimit(v uint32)
    SetMaxDynamicTableSizeLimit changes the maximum value that can be
    specified in SetMaxDynamicTableSize to v. By default, it is set to 4096,
    which is the same size of the default dynamic header table size described
    in HPACK specification. If the current maximum dynamic header table size is
    strictly greater than v, "Header Table Size Update" will be done in the next
    WriteField call and the maximum dynamic header table size is truncated to v.

func (e *Encoder) WriteField(f HeaderField) error
    WriteField encodes f into a single Write to e's underlying Writer. This
    function may also produce bytes for "Header Table Size Update" if necessary.
    If produced, it is done before encoding f.

type HeaderField struct {
	Name, Value string

	// Sensitive means that this header field should never be
	// indexed.
	Sensitive bool
}
    A HeaderField is a name-value pair. Both the name and value are treated as
    opaque sequences of octets.

func (hf HeaderField) IsPseudo() bool
    IsPseudo reports whether the header field is an http2 pseudo header.
    That is, it reports whether it starts with a colon. It is not otherwise
    guaranteed to be a valid pseudo header field, though.

func (hf HeaderField) Size() uint32
    Size returns the size of an entry per RFC 7541 section 4.1.

func (hf HeaderField) String() string

type InvalidIndexError int
    An InvalidIndexError is returned when an encoder references a table entry
    before the static table or after the end of the dynamic table.

func (e InvalidIndexError) Error() string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
