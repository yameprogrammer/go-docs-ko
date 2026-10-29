# package net/http/internal/http2

- 원문: <https://pkg.go.dev/net/http/internal/http2>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package http2 implements the HTTP/2 protocol.

## 원문 요약

Package http2 implements the HTTP/2 protocol.

## API 상세 (go doc -all)

~~~text
package http2 // import "net/http/internal/http2"

Package http2 implements the HTTP/2 protocol.

This package is low-level and intended to be used directly by very few people.
Most users will use it indirectly through the automatic use by the net/http
package (from Go 1.6 and later). For use in earlier Go versions see
ConfigureServer. (Transport support requires Go 1.6 or later)

See https://http2.github.io/ for more information on HTTP/2.

CONSTANTS

const (
	// ClientPreface is the string that must be sent by new
	// connections from clients.
	ClientPreface = "PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"

	// NextProtoTLS is the NPN/ALPN protocol negotiated during
	// HTTP/2's TLS setup.
	NextProtoTLS = "h2"
)
const DefaultMaxHeaderBytes = 1 << 20 // keep this in sync with net/http
const TimeFormat = "Mon, 02 Jan 2006 15:04:05 GMT" // keep in sync with net/http
const TrailerPrefix = "Trailer:"
    TrailerPrefix is a magic prefix for ResponseWriter.Header map keys that, if
    present, signals that the map entry is actually for the response trailers,
    and not the response headers. The prefix is stripped after the ServeHTTP
    call finishes and the values are sent in the trailers.

    This mechanism is intended only for trailers that are not known prior to the
    headers being written. If the set of trailers is fixed or known before the
    header is written, the normal Go trailers mechanism is preferred:

        https://golang.org/pkg/net/http/#ResponseWriter
        https://golang.org/pkg/net/http/#example_ResponseWriter_trailers


VARIABLES

var (
	NoBody              io.ReadCloser
	LocalAddrContextKey any
)
    Variables defined in net/http and initialized by an init func in that
    package.

    NoBody and LocalAddrContextKey have concrete types in net/http,
    and therefore can't be moved into a common package without introducing a
    dependency cycle.

var (
	ErrAbortHandler    = internal.ErrAbortHandler
	ErrBodyNotAllowed  = internal.ErrBodyNotAllowed
	ErrNotSupported    = errors.ErrUnsupported
	ErrSkipAltProtocol = internal.ErrSkipAltProtocol
)
var (
	VerboseLogs bool
)
var (
	NewConnContextKey         = new("NewConnContextKey")
	ConnectionStateContextKey = new("ConnectionStateContextKey")
)
var (
	ErrRecursivePush    = errors.New("http2: recursive push not allowed")
	ErrPushLimitReached = errors.New("http2: push would exceed peer's SETTINGS_MAX_CONCURRENT_STREAMS")
)
    Push errors.

var DebugGoroutines = os.Getenv("DEBUG_HTTP2_GOROUTINES") == "1"
var ErrFrameTooLarge = errors.New("http2: frame too large")
    ErrFrameTooLarge is returned from Framer.ReadFrame when the peer sends a
    frame that is larger than declared with SetMaxReadFrameSize.

var ErrNoCachedConn error = noCachedConnError{}

FUNCTIONS

func ReadFrameHeader(r io.Reader) (FrameHeader, error)
    ReadFrameHeader reads 9 bytes from r and returns a FrameHeader. Most users
    should use Framer.ReadFrame instead.


TYPES

type ClientConn struct {
	// Has unexported fields.
}
    ClientConn is the state of a single HTTP/2 client connection to an HTTP/2
    server.

func (cc *ClientConn) CanTakeNewRequest() bool
    CanTakeNewRequest reports whether the connection can take a new request,
    meaning it has not been closed or received or sent a GOAWAY.

    If the caller is going to immediately make a new request on this connection,
    use ReserveNewRequest instead.

func (cc *ClientConn) Close() error
    Close closes the client connection immediately.

    In-flight requests are interrupted. For a graceful shutdown, use Shutdown
    instead.

func (cc *ClientConn) Ping(ctx context.Context) error
    Ping sends a PING frame to the server and waits for the ack.

func (cc *ClientConn) ReserveNewRequest() bool
    ReserveNewRequest is like CanTakeNewRequest but also reserves a concurrent
    stream in cc. The reservation is decremented on the next call to RoundTrip.

func (cc *ClientConn) RoundTrip(req *ClientRequest) (*ClientResponse, error)

func (cc *ClientConn) SetDoNotReuse()
    SetDoNotReuse marks cc as not reusable for future HTTP requests.

func (cc *ClientConn) Shutdown(ctx context.Context) error
    Shutdown gracefully closes the client connection, waiting for running
    streams to complete.

func (cc *ClientConn) State() ClientConnState
    State returns a snapshot of cc's state.

type ClientConnState struct {
	// Closed is whether the connection is closed.
	Closed bool

	// Closing is whether the connection is in the process of
	// closing. It may be closing due to shutdown, being a
	// single-use connection, being marked as DoNotReuse, or
	// having received a GOAWAY frame.
	Closing bool

	// StreamsActive is how many streams are active.
	StreamsActive int

	// StreamsReserved is how many streams have been reserved via
	// ClientConn.ReserveNewRequest.
	StreamsReserved int

	// StreamsPending is how many requests have been sent in excess
	// of the peer's advertised MaxConcurrentStreams setting and
	// are waiting for other streams to complete.
	StreamsPending int

	// MaxConcurrentStreams is how many concurrent streams the
	// peer advertised as acceptable. Zero means no SETTINGS
	// frame has been received yet.
	MaxConcurrentStreams uint32

	// LastIdle, if non-zero, is when the connection last
	// transitioned to idle state.
	LastIdle time.Time
}
    ClientConnState describes the state of a ClientConn.

type ClientRequest struct {
	Context       context.Context
	Method        string
	URL           *url.URL
	Header        Header
	Trailer       Header
	Body          io.ReadCloser
	Host          string
	GetBody       func() (io.ReadCloser, error)
	ContentLength int64
	Cancel        <-chan struct{}
	Close         bool
	ResTrailer    *Header

	// Has unexported fields.
}
    A ClientRequest is a Request used by the HTTP/2 client (Transport).

func (req *ClientRequest) Clone() *ClientRequest
    Clone makes a shallow copy of ClientRequest.

    Clone is only used in shouldRetryRequest. We can drop it if we ever get rid
    of or rework that function.

type ClientResponse struct {
	Status        string // e.g. "200"
	StatusCode    int    // e.g. 200
	ContentLength int64
	Uncompressed  bool
	Header        Header
	Trailer       Header
	Body          io.ReadCloser
	TLS           *tls.ConnectionState
}
    A ClientResponse is a Request used by the HTTP/2 client (Transport).

type Config struct {
	MaxConcurrentStreams          int
	StrictMaxConcurrentRequests   bool
	MaxDecoderHeaderTableSize     int
	MaxEncoderHeaderTableSize     int
	MaxReadFrameSize              int
	MaxReceiveBufferPerConnection int
	MaxReceiveBufferPerStream     int
	SendPingTimeout               time.Duration
	PingTimeout                   time.Duration
	WriteByteTimeout              time.Duration
	PermitProhibitedCipherSuites  bool
	CountError                    func(errType string)
}
    Config must be kept in sync with net/http.HTTP2Config.

type ConnState int
    ConnState is identical to net/http.ConnState.

const (
	ConnStateNew ConnState = iota
	ConnStateActive
	ConnStateIdle
	ConnStateHijacked
	ConnStateClosed
)
type ConnectionError ErrCode
    ConnectionError is an error that results in the termination of the entire
    connection.

func (e ConnectionError) Error() string

type ContinuationFrame struct {
	FrameHeader
	// Has unexported fields.
}
    A ContinuationFrame is used to continue a sequence of header block
    fragments. See https://httpwg.org/specs/rfc7540.html#rfc.section.6.10

func (f *ContinuationFrame) HeaderBlockFragment() []byte

func (f *ContinuationFrame) HeadersEnded() bool

type DataFrame struct {
	FrameHeader
	// Has unexported fields.
}
    A DataFrame conveys arbitrary, variable-length
    sequences of octets associated with a stream. See
    https://httpwg.org/specs/rfc7540.html#rfc.section.6.1

func (f *DataFrame) Data() []byte
    Data returns the frame's data octets, not including any padding size byte
    or padding suffix bytes. The caller must not retain the returned memory past
    the next call to ReadFrame.

func (f *DataFrame) StreamEnded() bool

type ErrCode uint32
    An ErrCode is an unsigned 32-bit error code as defined in the HTTP/2 spec.

const (
	ErrCodeNo                 ErrCode = 0x0
	ErrCodeProtocol           ErrCode = 0x1
	ErrCodeInternal           ErrCode = 0x2
	ErrCodeFlowControl        ErrCode = 0x3
	ErrCodeSettingsTimeout    ErrCode = 0x4
	ErrCodeStreamClosed       ErrCode = 0x5
	ErrCodeFrameSize          ErrCode = 0x6
	ErrCodeRefusedStream      ErrCode = 0x7
	ErrCodeCancel             ErrCode = 0x8
	ErrCodeCompression        ErrCode = 0x9
	ErrCodeConnect            ErrCode = 0xa
	ErrCodeEnhanceYourCalm    ErrCode = 0xb
	ErrCodeInadequateSecurity ErrCode = 0xc
	ErrCodeHTTP11Required     ErrCode = 0xd
)
func (e ErrCode) String() string

type Flags uint8
    Flags is a bitmask of HTTP/2 flags. The meaning of flags varies depending on
    the frame type.

const (
	// Data Frame
	FlagDataEndStream Flags = 0x1
	FlagDataPadded    Flags = 0x8

	// Headers Frame
	FlagHeadersEndStream  Flags = 0x1
	FlagHeadersEndHeaders Flags = 0x4
	FlagHeadersPadded     Flags = 0x8
	FlagHeadersPriority   Flags = 0x20

	// Settings Frame
	FlagSettingsAck Flags = 0x1

	// Ping Frame
	FlagPingAck Flags = 0x1

	// Continuation Frame
	FlagContinuationEndHeaders Flags = 0x4

	FlagPushPromiseEndHeaders Flags = 0x4
	FlagPushPromisePadded     Flags = 0x8
)
    Frame-specific FrameHeader flag bits.

func (f Flags) Has(v Flags) bool
    Has reports whether f contains all (0 or more) flags in v.

type Frame interface {
	Header() FrameHeader

	// Has unexported methods.
}
    A Frame is the base interface implemented by all frame types. Callers
    will generally type-assert the specific frame type: *HeadersFrame,
    *SettingsFrame, *WindowUpdateFrame, etc.

    Frames are only valid until the next call to Framer.ReadFrame.

type FrameHeader struct {

	// Type is the 1 byte frame type. There are ten standard frame
	// types, but extension frame types may be written by WriteRawFrame
	// and will be returned by ReadFrame (as UnknownFrame).
	Type FrameType

	// Flags are the 1 byte of 8 potential bit flags per frame.
	// They are specific to the frame type.
	Flags Flags

	// Length is the length of the frame, not including the 9 byte header.
	// The maximum size is one byte less than 16MB (uint24), but only
	// frames up to 16KB are allowed without peer agreement.
	Length uint32

	// StreamID is which stream this frame is for. Certain frames
	// are not stream-specific, in which case this field is 0.
	StreamID uint32
	// Has unexported fields.
}
    A FrameHeader is the 9 byte header of all HTTP/2 frames.

    See https://httpwg.org/specs/rfc7540.html#FrameHeader

func (h FrameHeader) Header() FrameHeader
    Header returns h. It exists so FrameHeaders can be embedded in other
    specific frame types and implement the Frame interface.

func (h FrameHeader) String() string

type FrameType uint8
    A FrameType is a registered frame type as defined in
    https://httpwg.org/specs/rfc7540.html#rfc.section.11.2 and other future
    RFCs.

const (
	FrameData           FrameType = 0x0
	FrameHeaders        FrameType = 0x1
	FramePriority       FrameType = 0x2
	FrameRSTStream      FrameType = 0x3
	FrameSettings       FrameType = 0x4
	FramePushPromise    FrameType = 0x5
	FramePing           FrameType = 0x6
	FrameGoAway         FrameType = 0x7
	FrameWindowUpdate   FrameType = 0x8
	FrameContinuation   FrameType = 0x9
	FramePriorityUpdate FrameType = 0x10
)
func (t FrameType) String() string

type FrameWriteRequest struct {
	// Has unexported fields.
}
    FrameWriteRequest is a request to write a frame.

func (wr FrameWriteRequest) Consume(n int32) (FrameWriteRequest, FrameWriteRequest, int)
    Consume consumes min(n, available) bytes from this frame, where available is
    the number of flow control bytes available on the stream. Consume returns 0,
    1, or 2 frames, where the integer return value gives the number of frames
    returned.

    If flow control prevents consuming any bytes, this returns (_, _, 0).
    If the entire frame was consumed, this returns (wr, _, 1). Otherwise, this
    returns (consumed, rest, 2), where 'consumed' contains the consumed bytes
    and 'rest' contains the remaining bytes. The consumed bytes are deducted
    from the underlying stream's flow control budget.

func (wr FrameWriteRequest) DataSize() int
    DataSize returns the number of flow control bytes that must be consumed to
    write this entire frame. This is 0 for non-DATA frames.

func (wr FrameWriteRequest) StreamID() uint32
    StreamID returns the id of the stream this frame will be written to.
    0 is used for non-stream frames such as PING and SETTINGS.

func (wr FrameWriteRequest) String() string
    String is for debugging only.

type Framer struct {

	// AllowIllegalWrites permits the Framer's Write methods to
	// write frames that do not conform to the HTTP/2 spec. This
	// permits using the Framer to test other HTTP/2
	// implementations' conformance to the spec.
	// If false, the Write methods will prefer to return an error
	// rather than comply.
	AllowIllegalWrites bool

	// AllowIllegalReads permits the Framer's ReadFrame method
	// to return non-compliant frames or frame orders.
	// This is for testing and permits using the Framer to test
	// other HTTP/2 implementations' conformance to the spec.
	// It is not compatible with ReadMetaHeaders.
	AllowIllegalReads bool

	// ReadMetaHeaders if non-nil causes ReadFrame to merge
	// HEADERS and CONTINUATION frames together and return
	// MetaHeadersFrame instead.
	ReadMetaHeaders *hpack.Decoder

	// MaxHeaderListSize is the http2 MAX_HEADER_LIST_SIZE.
	// It's used only if ReadMetaHeaders is set; 0 means a sane default
	// (currently 16MB)
	// If the limit is hit, MetaHeadersFrame.Truncated is set true.
	MaxHeaderListSize uint32

	// MaxHeaderValueCount is the maximum permitted number of
	// header values.
	// It's used only if ReadMetaHeaders is set; 0 means no limit.
	// If the limit is hit, MetaHeadersFrame.Truncated is set true.
	MaxHeaderValueCount int

	// Has unexported fields.
}
    A Framer reads and writes Frames.

func NewFramer(w io.Writer, r io.Reader) *Framer
    NewFramer returns a Framer that writes frames to w and reads them from r.

func (fr *Framer) ErrorDetail() error
    ErrorDetail returns a more detailed error of the last error returned by
    Framer.ReadFrame. For instance, if ReadFrame returns a StreamError with code
    PROTOCOL_ERROR, ErrorDetail will say exactly what was invalid. ErrorDetail
    is not guaranteed to return a non-nil value and like the rest of the http2
    package, its return value is not protected by an API compatibility promise.
    ErrorDetail is reset after the next call to ReadFrame.

func (fr *Framer) ReadFrame() (Frame, error)
    ReadFrame reads a single frame. The returned Frame is only valid until the
    next call to ReadFrame or ReadFrameBodyForHeader.

    If the frame is larger than previously set with SetMaxReadFrameSize,
    the returned error is ErrFrameTooLarge. Other errors may be of type
    ConnectionError, StreamError, or anything else from the underlying reader.

    If ReadFrame returns an error and a non-nil Frame, the Frame's StreamID
    indicates the stream responsible for the error.

func (fr *Framer) ReadFrameForHeader(fh FrameHeader) (Frame, error)
    ReadFrameForHeader reads the payload for the frame with the given
    FrameHeader.

    It behaves identically to ReadFrame, other than not checking the maximum
    frame size.

func (fr *Framer) ReadFrameHeader() (FrameHeader, error)
    ReadFrameHeader reads the header of the next frame. It reads the 9-byte
    fixed frame header, and does not read any portion of the frame payload.
    The caller is responsible for consuming the payload, either with
    ReadFrameForHeader or directly from the Framer's io.Reader.

    If the frame is larger than previously set with SetMaxReadFrameSize,
    it returns the frame header and ErrFrameTooLarge.

    If the returned FrameHeader.StreamID is non-zero, it indicates the stream
    responsible for the error.

func (fr *Framer) SetMaxReadFrameSize(v uint32)
    SetMaxReadFrameSize sets the maximum size of a frame that will be read by a
    subsequent call to ReadFrame. It is the caller's responsibility to advertise
    this limit with a SETTINGS frame.

func (fr *Framer) SetReuseFrames()
    SetReuseFrames allows the Framer to reuse Frames. If called on a Framer,
    Frames returned by calls to ReadFrame are only valid until the next call to
    ReadFrame.

func (f *Framer) WriteContinuation(streamID uint32, endHeaders bool, headerBlockFragment []byte) error
    WriteContinuation writes a CONTINUATION frame.

    It will perform exactly one Write to the underlying Writer. It is the
    caller's responsibility to not call other Write methods concurrently.

func (f *Framer) WriteData(streamID uint32, endStream bool, data []byte) error
    WriteData writes a DATA frame.

    It will perform exactly one Write to the underlying Writer. It is the
    caller's responsibility not to violate the maximum frame size and to not
    call other Write methods concurrently.

func (f *Framer) WriteDataPadded(streamID uint32, endStream bool, data, pad []byte) error
    WriteDataPadded writes a DATA frame with optional padding.

    If pad is nil, the padding bit is not sent. The length of pad must
    not exceed 255 bytes. The bytes of pad must all be zero, unless
    f.AllowIllegalWrites is set.

    It will perform exactly one Write to the underlying Writer. It is the
    caller's responsibility not to violate the maximum frame size and to not
    call other Write methods concurrently.

func (f *Framer) WriteGoAway(maxStreamID uint32, code ErrCode, debugData []byte) error

func (f *Framer) WriteHeaders(p HeadersFrameParam) error
    WriteHeaders writes a single HEADERS frame.

    This is a low-level header writing method. Encoding headers and splitting
    them into any necessary CONTINUATION frames is handled elsewhere.

    It will perform exactly one Write to the underlying Writer. It is the
    caller's responsibility to not call other Write methods concurrently.

func (f *Framer) WritePing(ack bool, data [8]byte) error

func (f *Framer) WritePriority(streamID uint32, p PriorityParam) error
    WritePriority writes a PRIORITY frame.

    It will perform exactly one Write to the underlying Writer. It is the
    caller's responsibility to not call other Write methods concurrently.

func (f *Framer) WritePriorityUpdate(streamID uint32, priority string) error
    WritePriorityUpdate writes a PRIORITY_UPDATE frame.

    It will perform exactly one Write to the underlying Writer. It is the
    caller's responsibility to not call other Write methods concurrently.

func (f *Framer) WritePushPromise(p PushPromiseParam) error
    WritePushPromise writes a single PushPromise Frame.

    As with Header Frames, This is the low level call for writing individual
    frames. Continuation frames are handled elsewhere.

    It will perform exactly one Write to the underlying Writer. It is the
    caller's responsibility to not call other Write methods concurrently.

func (f *Framer) WriteRSTStream(streamID uint32, code ErrCode) error
    WriteRSTStream writes a RST_STREAM frame.

    It will perform exactly one Write to the underlying Writer. It is the
    caller's responsibility to not call other Write methods concurrently.

func (f *Framer) WriteRawFrame(t FrameType, flags Flags, streamID uint32, payload []byte) error
    WriteRawFrame writes a raw frame. This can be used to write extension frames
    unknown to this package.

func (f *Framer) WriteSettings(settings ...Setting) error
    WriteSettings writes a SETTINGS frame with zero or more settings specified
    and the ACK bit not set.

    It will perform exactly one Write to the underlying Writer. It is the
    caller's responsibility to not call other Write methods concurrently.

func (f *Framer) WriteSettingsAck() error
    WriteSettingsAck writes an empty SETTINGS frame with the ACK bit set.

    It will perform exactly one Write to the underlying Writer. It is the
    caller's responsibility to not call other Write methods concurrently.

func (f *Framer) WriteWindowUpdate(streamID, incr uint32) error
    WriteWindowUpdate writes a WINDOW_UPDATE frame. The increment value must be
    between 1 and 2,147,483,647, inclusive. If the Stream ID is zero, the window
    update applies to the connection as a whole.

type GoAwayError struct {
	LastStreamID uint32
	ErrCode      ErrCode
	DebugData    string
}
    GoAwayError is returned by the Transport when the server closes the TCP
    connection after sending a GOAWAY frame.

func (e GoAwayError) Error() string

type GoAwayFrame struct {
	FrameHeader
	LastStreamID uint32
	ErrCode      ErrCode
	// Has unexported fields.
}
    A GoAwayFrame informs the remote peer to stop creating streams on this
    connection. See https://httpwg.org/specs/rfc7540.html#rfc.section.6.8

func (f *GoAwayFrame) DebugData() []byte
    DebugData returns any debug data in the GOAWAY frame. Its contents are not
    defined. The caller must not retain the returned memory past the next call
    to ReadFrame.

type Handler interface {
	ServeHTTP(*ResponseWriter, *ServerRequest)
}

type Header = textproto.MIMEHeader

type HeadersFrame struct {
	FrameHeader

	// Priority is set if FlagHeadersPriority is set in the FrameHeader.
	Priority PriorityParam

	// Has unexported fields.
}
    A HeadersFrame is used to open a stream and additionally carries a header
    block fragment.

func (f *HeadersFrame) HasPriority() bool

func (f *HeadersFrame) HeaderBlockFragment() []byte

func (f *HeadersFrame) HeadersEnded() bool

func (f *HeadersFrame) StreamEnded() bool

type HeadersFrameParam struct {
	// StreamID is the required Stream ID to initiate.
	StreamID uint32
	// BlockFragment is part (or all) of a Header Block.
	BlockFragment []byte

	// EndStream indicates that the header block is the last that
	// the endpoint will send for the identified stream. Setting
	// this flag causes the stream to enter one of "half closed"
	// states.
	EndStream bool

	// EndHeaders indicates that this frame contains an entire
	// header block and is not followed by any
	// CONTINUATION frames.
	EndHeaders bool

	// PadLength is the optional number of bytes of zeros to add
	// to this frame.
	PadLength uint8

	// Priority, if non-zero, includes stream priority information
	// in the HEADER frame.
	Priority PriorityParam
}
    HeadersFrameParam are the parameters for writing a HEADERS frame.

type MetaHeadersFrame struct {
	*HeadersFrame

	// Fields are the fields contained in the HEADERS and
	// CONTINUATION frames. The underlying slice is owned by the
	// Framer and must not be retained after the next call to
	// ReadFrame.
	//
	// Fields are guaranteed to be in the correct http2 order and
	// not have unknown pseudo header fields or invalid header
	// field names or values. Required pseudo header fields may be
	// missing, however. Use the MetaHeadersFrame.Pseudo accessor
	// method access pseudo headers.
	Fields []hpack.HeaderField

	// Truncated is whether the max header list size limit was hit
	// and Fields is incomplete. The hpack decoder state is still
	// valid, however.
	Truncated bool
}
    A MetaHeadersFrame is the representation of one HEADERS frame and zero or
    more contiguous CONTINUATION frames and the decoding of their HPACK-encoded
    contents.

    This type of frame does not appear on the wire and is only returned by the
    Framer when Framer.ReadMetaHeaders is set.

func (mh *MetaHeadersFrame) PseudoFields() []hpack.HeaderField
    PseudoFields returns the pseudo header fields of mh. The caller does not own
    the returned slice.

func (mh *MetaHeadersFrame) PseudoValue(pseudo string) string
    PseudoValue returns the given pseudo header field's value. The provided
    pseudo field should not contain the leading colon.

func (mh *MetaHeadersFrame) RegularFields() []hpack.HeaderField
    RegularFields returns the regular (non-pseudo) header fields of mh.
    The caller does not own the returned slice.

type NetHTTPClientConn struct {
	// Has unexported fields.
}
    netHTTPClientConn wraps ClientConn and implements the interface net/http
    expects from the RoundTripper returned by NewClientConn.

func (cc NetHTTPClientConn) Available() int

func (cc NetHTTPClientConn) Close() error

func (cc NetHTTPClientConn) Err() error

func (cc NetHTTPClientConn) InFlight() int

func (cc NetHTTPClientConn) Ping(ctx context.Context) error

func (cc NetHTTPClientConn) Release()

func (cc NetHTTPClientConn) Reserve() error

func (cc NetHTTPClientConn) RoundTrip(req *ClientRequest) (*ClientResponse, error)

type OpenStreamOptions struct {
	// PusherID is zero if the stream was initiated by the client. Otherwise,
	// PusherID names the stream that pushed the newly opened stream.
	PusherID uint32

	// Has unexported fields.
}
    OpenStreamOptions specifies extra options for WriteScheduler.OpenStream.

type PingFrame struct {
	FrameHeader
	Data [8]byte
}
    A PingFrame is a mechanism for measuring a minimal round trip time from
    the sender, as well as determining whether an idle connection is still
    functional. See https://httpwg.org/specs/rfc7540.html#rfc.section.6.7

func (f *PingFrame) IsAck() bool

type PriorityFrame struct {
	FrameHeader
	PriorityParam
}
    A PriorityFrame specifies the sender-advised priority of a stream.
    See https://httpwg.org/specs/rfc7540.html#rfc.section.6.3

type PriorityParam struct {
	// StreamDep is a 31-bit stream identifier for the
	// stream that this stream depends on. Zero means no
	// dependency.
	StreamDep uint32

	// Exclusive is whether the dependency is exclusive.
	Exclusive bool

	// Weight is the stream's zero-indexed weight. It should be
	// set together with StreamDep, or neither should be set. Per
	// the spec, "Add one to the value to obtain a weight between
	// 1 and 256."
	Weight uint8

	// Has unexported fields.
}
    PriorityParam are the stream prioritization parameters.

func (p PriorityParam) IsZero() bool

type PriorityUpdateFrame struct {
	FrameHeader
	Priority            string
	PrioritizedStreamID uint32
}
    PriorityUpdateFrame is a PRIORITY_UPDATE frame as described in
    https://www.rfc-editor.org/rfc/rfc9218.html#name-the-priority_update-frame.

type PushOptions struct {
	Method string
	Header Header
}

type PushPromiseFrame struct {
	FrameHeader
	PromiseID uint32
	// Has unexported fields.
}
    A PushPromiseFrame is used to initiate a server stream. See
    https://httpwg.org/specs/rfc7540.html#rfc.section.6.6

func (f *PushPromiseFrame) HeaderBlockFragment() []byte

func (f *PushPromiseFrame) HeadersEnded() bool

type PushPromiseParam struct {
	// StreamID is the required Stream ID to initiate.
	StreamID uint32

	// PromiseID is the required Stream ID which this
	// Push Promises
	PromiseID uint32

	// BlockFragment is part (or all) of a Header Block.
	BlockFragment []byte

	// EndHeaders indicates that this frame contains an entire
	// header block and is not followed by any
	// CONTINUATION frames.
	EndHeaders bool

	// PadLength is the optional number of bytes of zeros to add
	// to this frame.
	PadLength uint8
}
    PushPromiseParam are the parameters for writing a PUSH_PROMISE frame.

type RSTStreamFrame struct {
	FrameHeader
	ErrCode ErrCode
}
    A RSTStreamFrame allows for abnormal termination of a stream. See
    https://httpwg.org/specs/rfc7540.html#rfc.section.6.4

type ResponseWriter = responseWriter

type RoundTripOpt struct {
	// OnlyCachedConn controls whether RoundTripOpt may
	// create a new TCP connection. If set true and
	// no cached connection is available, RoundTripOpt
	// will return ErrNoCachedConn.
	OnlyCachedConn bool
}
    RoundTripOpt are options for the Transport.RoundTripOpt method.

type ServeConnOpts struct {
	// Context is the base context to use.
	// If nil, context.Background is used.
	Context context.Context

	// BaseConfig optionally sets the base configuration
	// for values. If nil, defaults are used.
	BaseConfig ServerConfig

	// Handler specifies which handler to use for processing
	// requests. If nil, BaseConfig.Handler is used. If BaseConfig
	// or BaseConfig.Handler is nil, http.DefaultServeMux is used.
	Handler Handler

	// Settings is the decoded contents of the HTTP2-Settings header
	// in an h2c upgrade request.
	Settings []byte

	UpgradeRequest *ServerRequest

	// SawClientPreface is set if the HTTP/2 connection preface
	// has already been read from the connection.
	SawClientPreface bool
}
    ServeConnOpts are options for the Server.ServeConn method.

type Server struct {
	// Has unexported fields.
}
    Server is an HTTP/2 server.

func (s *Server) Configure(conf ServerConfig, tcfg *tls.Config) error

func (s *Server) GracefulShutdown()

func (s *Server) ServeConn(c net.Conn, opts *ServeConnOpts)
    ServeConn serves HTTP/2 requests on the provided connection and blocks until
    the connection is no longer readable.

    ServeConn starts speaking HTTP/2 assuming that c has not had any reads or
    writes. It writes its initial settings frame and expects to be able to read
    the preface and settings frame from the client. If c has a ConnectionState
    method like a *tls.Conn, the ConnectionState is used to verify the TLS
    ciphersuite and to set the Request.TLS field in Handlers.

    ServeConn does not support h2c by itself. Any h2c support must be
    implemented in terms of providing a suitably-behaving net.Conn.

    The opts parameter is optional. If nil, default values are used.

type ServerConfig interface {
	MaxHeaderBytes() int
	MaxHeaderValueCount() int
	ConnState(net.Conn, ConnState)
	DoKeepAlives() bool
	WriteTimeout() time.Duration
	SendPingTimeout() time.Duration
	ErrorLog() *log.Logger
	ReadTimeout() time.Duration
	HTTP2Config() Config
	DisableClientPriority() bool
	IdleTimeout() time.Duration
}
    ServerConfig is configuration from an http.Server.

type ServerRequest struct {
	Context       context.Context
	Proto         string // e.g. "HTTP/1.0"
	ProtoMajor    int    // e.g. 1
	ProtoMinor    int    // e.g. 0
	Method        string
	URL           *url.URL
	Header        Header
	Trailer       Header
	Body          io.ReadCloser
	Host          string
	ContentLength int64
	RemoteAddr    string
	RequestURI    string
	TLS           *tls.ConnectionState
	MultipartForm *multipart.Form
}
    A ServerRequest is a Request used by the HTTP/2 server.

type Setting struct {
	// ID is which setting is being set.
	// See https://httpwg.org/specs/rfc7540.html#SettingFormat
	ID SettingID

	// Val is the value.
	Val uint32
}
    Setting is a setting parameter: which setting it is, and its value.

func (s Setting) String() string

func (s Setting) Valid() error
    Valid reports whether the setting is valid.

type SettingID uint16
    A SettingID is an HTTP/2 setting as defined in
    https://httpwg.org/specs/rfc7540.html#iana-settings

const (
	SettingHeaderTableSize       SettingID = 0x1
	SettingEnablePush            SettingID = 0x2
	SettingMaxConcurrentStreams  SettingID = 0x3
	SettingInitialWindowSize     SettingID = 0x4
	SettingMaxFrameSize          SettingID = 0x5
	SettingMaxHeaderListSize     SettingID = 0x6
	SettingEnableConnectProtocol SettingID = 0x8
	SettingNoRFC7540Priorities   SettingID = 0x9
)
func (s SettingID) String() string

type SettingsFrame struct {
	FrameHeader
	// Has unexported fields.
}
    A SettingsFrame conveys configuration parameters that affect how endpoints
    communicate, such as preferences and constraints on peer behavior.

    See https://httpwg.org/specs/rfc7540.html#SETTINGS

func (f *SettingsFrame) ForeachSetting(fn func(Setting) error) error
    ForeachSetting runs fn for each setting. It stops and returns the first
    error.

func (f *SettingsFrame) HasDuplicates() bool
    HasDuplicates reports whether f contains any duplicate setting IDs.

func (f *SettingsFrame) IsAck() bool

func (f *SettingsFrame) NumSettings() int

func (f *SettingsFrame) Setting(i int) Setting
    Setting returns the setting from the frame at the given 0-based index.
    The index must be >= 0 and less than f.NumSettings().

func (f *SettingsFrame) Value(id SettingID) (v uint32, ok bool)

type StreamError struct {
	StreamID uint32
	Code     ErrCode
	Cause    error // optional additional detail
}
    StreamError is an error that only affects one stream within an HTTP/2
    connection.

func (e StreamError) As(target any) bool
    This As function permits converting a StreamError into a
    x/net/http2.StreamError.

func (e StreamError) Error() string

type Transport struct {
	// Has unexported fields.
}
    Transport is an HTTP/2 Transport.

    A Transport internally caches connections to servers. It is safe for
    concurrent use by multiple goroutines.

func NewTransport(t1 TransportConfig) *Transport

func (t *Transport) AddConn(scheme, authority string, c net.Conn) error

func (t *Transport) CloseIdleConnections()
    CloseIdleConnections closes any connections which were previously connected
    from previous requests but are now sitting idle. It does not interrupt any
    connections currently in use.

func (t *Transport) IdleConnStrsForTesting() []string

func (t *Transport) NewClientConn(c net.Conn, internalStateHook func()) (NetHTTPClientConn, error)

func (t *Transport) RoundTrip(req *ClientRequest) (*ClientResponse, error)

func (t *Transport) RoundTripOpt(req *ClientRequest, opt RoundTripOpt) (*ClientResponse, error)
    RoundTripOpt is like RoundTrip, but takes options.

type TransportConfig interface {
	MaxHeaderListSize() int64
	MaxResponseHeaderBytes() int64
	DisableCompression() bool
	DisableKeepAlives() bool
	ExpectContinueTimeout() time.Duration
	ResponseHeaderTimeout() time.Duration
	IdleConnTimeout() time.Duration
	HTTP2Config() Config
}
    TransportConfig is configuration from an http.Transport.

type UnknownFrame struct {
	FrameHeader
	// Has unexported fields.
}
    An UnknownFrame is the frame type returned when the frame type is unknown or
    no specific frame type parser exists.

func (f *UnknownFrame) Payload() []byte
    Payload returns the frame's payload (after the header). It is not valid
    to call this method after a subsequent call to Framer.ReadFrame, nor is it
    valid to retain the returned slice. The memory is owned by the Framer and is
    invalidated when the next frame is read.

type WindowUpdateFrame struct {
	FrameHeader
	Increment uint32 // never read with high bit set
}
    A WindowUpdateFrame is used to implement flow control. See
    https://httpwg.org/specs/rfc7540.html#rfc.section.6.9

type WriteScheduler interface {
	// OpenStream opens a new stream in the write scheduler.
	// It is illegal to call this with streamID=0 or with a streamID that is
	// already open -- the call may panic.
	OpenStream(streamID uint32, options OpenStreamOptions)

	// CloseStream closes a stream in the write scheduler. Any frames queued on
	// this stream should be discarded. It is illegal to call this on a stream
	// that is not open -- the call may panic.
	CloseStream(streamID uint32)

	// AdjustStream adjusts the priority of the given stream. This may be called
	// on a stream that has not yet been opened or has been closed. Note that
	// RFC 7540 allows PRIORITY frames to be sent on streams in any state. See:
	// https://tools.ietf.org/html/rfc7540#section-5.1
	AdjustStream(streamID uint32, priority PriorityParam)

	// Push queues a frame in the scheduler. In most cases, this will not be
	// called with wr.StreamID()!=0 unless that stream is currently open. The one
	// exception is RST_STREAM frames, which may be sent on idle or closed streams.
	Push(wr FrameWriteRequest)

	// Pop dequeues the next frame to write. Returns false if no frames can
	// be written. Frames with a given wr.StreamID() are Pop'd in the same
	// order they are Push'd, except RST_STREAM frames. No frames should be
	// discarded except by CloseStream.
	Pop() (wr FrameWriteRequest, ok bool)
}
    WriteScheduler is the interface implemented by HTTP/2 write schedulers.
    Methods are never called concurrently.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
