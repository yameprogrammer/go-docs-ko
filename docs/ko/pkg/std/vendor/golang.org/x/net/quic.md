# package vendor/golang.org/x/net/quic

- 원문: <https://pkg.go.dev/vendor/golang.org/x/net/quic>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `quic`는 QUIC 프로토콜을 구현합니다.

## 원문 요약

Package quic implements the QUIC protocol.

## API 상세 (go doc -all)

~~~text
package quic // import "vendor/golang.org/x/net/quic"

Package quic implements the QUIC protocol.

This package is a work in progress. It is not ready for production usage.
Its API is subject to change without notice.

This package is low-level. Most users will use it indirectly through an HTTP/3
implementation.

# Usage

An Endpoint sends and receives traffic on a network address. Create an Endpoint
to either accept inbound QUIC connections or create outbound ones.

A Conn is a QUIC connection.

A Stream is a QUIC stream, an ordered, reliable byte stream.

# Cancellation

All blocking operations may be canceled using a context.Context. When performing
an operation with a canceled context, the operation will succeed if doing so
does not require blocking. For example, reading from a stream will return data
when buffered data is available, even if the stream context is canceled.

# Limitations

This package is a work in progress. Known limitations include:

  - Performance is untuned.
  - 0-RTT is not supported.
  - Address migration is not supported.
  - Server preferred addresses are not supported.
  - The latency spin bit is not supported.
  - Stream send/receive windows are configurable, but are fixed and do not adapt
    to available throughput.
  - Path MTU discovery is not implemented.

# Security Policy

This package is a work in progress, and not yet covered by the Go security
policy.

CONSTANTS

const (
	// QLogLevelFrame includes per-frame information.
	// When this level is enabled, packet_sent and packet_received events will
	// contain information on individual frames sent/received.
	QLogLevelFrame = slog.Level(-6)

	// QLogLevelPacket events occur at most once per packet sent or received.
	//
	// For example: packet_sent, packet_received.
	QLogLevelPacket = slog.Level(-4)

	// QLogLevelConn events occur multiple times over a connection's lifetime,
	// but less often than the frequency of individual packets.
	//
	// For example: connection_state_updated.
	QLogLevelConn = slog.Level(-2)

	// QLogLevelEndpoint events occur at most once per connection.
	//
	// For example: connection_started, connection_closed.
	QLogLevelEndpoint = slog.Level(0)
)
    Log levels for qlog events.


FUNCTIONS

func Listen(network, address string, listenConfig *Config) (*Endpoint, error)
    Listen listens on a local network address.

    The config is used to for connections accepted by the endpoint. If the
    config is nil, the endpoint will not accept connections.

func NewEndpoint(conn net.PacketConn, config *Config) (*Endpoint, error)
    NewEndpoint creates an endpoint using a net.PacketConn as the underlying
    transport.

    If the PacketConn is not a *net.UDPConn, the endpoint may be slower and lack
    access to some features of the network.


TYPES

type ApplicationError struct {
	Code   uint64
	Reason string
}
    An ApplicationError is an application protocol error code (RFC 9000, Section
    20.2). Application protocol errors may be sent when terminating a stream or
    connection.

func (e *ApplicationError) Error() string

func (e *ApplicationError) Is(err error) bool
    Is reports a match if err is an *ApplicationError with a matching Code.

type Config struct {
	// TLSConfig is the endpoint's TLS configuration.
	// It must be non-nil and include at least one certificate or else set GetCertificate.
	TLSConfig *tls.Config

	// MaxBidiRemoteStreams limits the number of simultaneous bidirectional streams
	// a peer may open.
	// If zero, the default value of 100 is used.
	// If negative, the limit is zero.
	MaxBidiRemoteStreams int64

	// MaxUniRemoteStreams limits the number of simultaneous unidirectional streams
	// a peer may open.
	// If zero, the default value of 100 is used.
	// If negative, the limit is zero.
	MaxUniRemoteStreams int64

	// MaxStreamReadBufferSize is the maximum amount of data sent by the peer that a
	// stream will buffer for reading.
	// If zero, the default value of 1MiB is used.
	// If negative, the limit is zero.
	MaxStreamReadBufferSize int64

	// MaxStreamWriteBufferSize is the maximum amount of data a stream will buffer for
	// sending to the peer.
	// If zero, the default value of 1MiB is used.
	// If negative, the limit is zero.
	MaxStreamWriteBufferSize int64

	// MaxConnReadBufferSize is the maximum amount of data sent by the peer that a
	// connection will buffer for reading, across all streams.
	// If zero, the default value of 1MiB is used.
	// If negative, the limit is zero.
	MaxConnReadBufferSize int64

	// RequireAddressValidation may be set to true to enable address validation
	// of client connections prior to starting the handshake.
	//
	// Enabling this setting reduces the amount of work packets with spoofed
	// source address information can cause a server to perform,
	// at the cost of increased handshake latency.
	RequireAddressValidation bool

	// StatelessResetKey is used to provide stateless reset of connections.
	// A restart may leave an endpoint without access to the state of
	// existing connections. Stateless reset permits an endpoint to respond
	// to a packet for a connection it does not recognize.
	//
	// This field should be filled with random bytes.
	// The contents should remain stable across restarts,
	// to permit an endpoint to send a reset for
	// connections created before a restart.
	//
	// The contents of the StatelessResetKey should not be exposed.
	// An attacker can use knowledge of this field's value to
	// reset existing connections.
	//
	// If this field is left as zero, stateless reset is disabled.
	StatelessResetKey [32]byte

	// HandshakeTimeout is the maximum time in which a connection handshake must complete.
	// If zero, the default of 10 seconds is used.
	// If negative, there is no handshake timeout.
	HandshakeTimeout time.Duration

	// MaxIdleTimeout is the maximum time after which an idle connection will be closed.
	// If zero, the default of 30 seconds is used.
	// If negative, idle connections are never closed.
	//
	// The idle timeout for a connection is the minimum of the maximum idle timeouts
	// of the endpoints.
	MaxIdleTimeout time.Duration

	// KeepAlivePeriod is the time after which a packet will be sent to keep
	// an idle connection alive.
	// If zero, keep alive packets are not sent.
	// If greater than zero, the keep alive period is the smaller of KeepAlivePeriod and
	// half the connection idle timeout.
	KeepAlivePeriod time.Duration

	// QLogLogger receives qlog events.
	//
	// Events currently correspond to the definitions in draft-ietf-qlog-quic-events-03.
	// This is not the latest version of the draft, but is the latest version supported
	// by common event log viewers as of the time this paragraph was written.
	//
	// The qlog package contains a slog.Handler which serializes qlog events
	// to a standard JSON representation.
	QLogLogger *slog.Logger
}
    A Config structure configures a QUIC endpoint. A Config must not be modified
    after it has been passed to a QUIC function. A Config may be reused;
    the quic package will also not modify it.

func (c *Config) Clone() *Config
    Clone returns a shallow clone of c, or nil if c is nil. It is safe to clone
    a Config that is being used concurrently by a QUIC endpoint.

type Conn struct {
	// Has unexported fields.
}
    A Conn is a QUIC connection.

    Multiple goroutines may invoke methods on a Conn simultaneously.

func (c *Conn) Abort(err error)
    Abort closes the connection and returns immediately.

    If err is nil, Abort sends a transport error of NO_ERROR to the peer. If
    err is an ApplicationError, Abort sends its error code and text. Otherwise,
    Abort sends a transport error of APPLICATION_ERROR with the error's text.

func (c *Conn) AcceptStream(ctx context.Context) (*Stream, error)
    AcceptStream waits for and returns the next stream created by the peer.

func (c *Conn) Close() error
    Close closes the connection.

    Close is equivalent to:

        conn.Abort(nil)
        err := conn.Wait(context.Background())

func (c *Conn) ConnectionState() tls.ConnectionState
    ConnectionState returns basic TLS details about the connection.

func (c *Conn) LocalAddr() netip.AddrPort
    LocalAddr returns the local network address, if known.

func (c *Conn) NewSendOnlyStream(ctx context.Context) (*Stream, error)
    NewSendOnlyStream creates a unidirectional, send-only stream.

    If the peer's maximum stream limit for the connection has been reached,
    NewSendOnlyStream blocks until the limit is increased or the context
    expires.

func (c *Conn) NewStream(ctx context.Context) (*Stream, error)
    NewStream creates a stream.

    If the peer's maximum stream limit for the connection has been reached,
    NewStream blocks until the limit is increased or the context expires.

func (c *Conn) RemoteAddr() netip.AddrPort
    RemoteAddr returns the remote network address, if known.

func (c *Conn) String() string

func (c *Conn) Wait(ctx context.Context) error
    Wait waits for the peer to close the connection.

    If the connection is closed locally and the peer does not close its end of
    the connection, Wait will return with a non-nil error after the drain period
    expires.

    If the peer closes the connection with a NO_ERROR transport error, Wait
    returns nil. If the peer closes the connection with an application error,
    Wait returns an ApplicationError containing the peer's error code and
    reason. If the peer closes the connection with any other status, Wait
    returns a non-nil error.

type Endpoint struct {
	// Has unexported fields.
}
    An Endpoint handles QUIC traffic on a network address. It can accept inbound
    connections or create outbound ones.

    Multiple goroutines may invoke methods on an Endpoint simultaneously.

func (e *Endpoint) Accept(ctx context.Context) (*Conn, error)
    Accept waits for and returns the next connection.

func (e *Endpoint) Close(ctx context.Context) error
    Close closes the Endpoint. Any blocked operations on the Endpoint or
    associated Conns and Stream will be unblocked and return errors.

    Close aborts every open connection. Data in stream read and write buffers is
    discarded. It waits for the peers of any open connection to acknowledge the
    connection has been closed.

func (e *Endpoint) Dial(ctx context.Context, network, address string, config *Config) (*Conn, error)
    Dial creates and returns a connection to a network address. The config
    cannot be nil.

func (e *Endpoint) LocalAddr() netip.AddrPort
    LocalAddr returns the local network address.

type Stream struct {
	// Has unexported fields.
}
    A Stream is an ordered byte stream.

    Streams may be bidirectional, read-only, or write-only. Methods
    inappropriate for a stream's direction (for example, [Write] to a read-only
    stream) return errors.

    It is not safe to perform concurrent reads from or writes to a stream.
    It is safe, however, to read and write at the same time.

    Reads and writes are buffered. It is generally not necessary to wrap a
    stream in a bufio.ReadWriter or otherwise apply additional buffering.

    To cancel reads or writes, use the [SetReadContext] and [SetWriteContext]
    methods.

func (s *Stream) Close() error
    Close closes the stream. Any blocked stream operations will be unblocked and
    return errors.

    Close flushes any data in the stream write buffer and waits for the peer
    to acknowledge receipt of the data. If the stream has been reset, it waits
    for the peer to acknowledge the reset. If the context expires before the
    peer receives the stream's data, Close discards the buffer and returns the
    context error.

func (s *Stream) CloseRead()
    CloseRead aborts reads on the stream. Any blocked reads will be unblocked
    and return errors.

    CloseRead notifies the peer that the stream has been closed for reading.
    It does not wait for the peer to acknowledge the closure. Use Close to wait
    for the peer's acknowledgement.

func (s *Stream) CloseWrite()
    CloseWrite aborts writes on the stream. Any blocked writes will be unblocked
    and return errors.

    CloseWrite sends any data in the stream write buffer to the peer. It does
    not wait for the peer to acknowledge receipt of the data. Use Close to wait
    for the peer's acknowledgement.

func (s *Stream) Flush() error
    Flush flushes data written to the stream. It does not wait for the peer
    to acknowledge receipt of the data. Use Close to wait for the peer's
    acknowledgement.

func (s *Stream) ID() int64
    ID returns the QUIC stream ID of s.

    As specified in RFC 9000, the two least significant bits of a stream ID
    indicate the initiator and directionality of the stream. The upper bits are
    the stream number.

func (s *Stream) IsReadOnly() bool
    IsReadOnly reports whether the stream is read-only (a unidirectional stream
    created by the peer).

func (s *Stream) IsWriteOnly() bool
    IsWriteOnly reports whether the stream is write-only (a unidirectional
    stream created locally).

func (s *Stream) Read(b []byte) (n int, err error)
    Read reads data from the stream.

    Read returns as soon as at least one byte of data is available.

    If the peer closes the stream cleanly, Read returns io.EOF after returning
    all data sent by the peer. If the peer aborts reads on the stream, Read
    returns an error wrapping StreamResetCode.

    It is not safe to call Read concurrently.

func (s *Stream) ReadByte() (byte, error)
    ReadByte reads and returns a single byte from the stream.

    It is not safe to call ReadByte concurrently.

func (s *Stream) Reset(code uint64)
    Reset aborts writes on the stream and notifies the peer that the stream was
    terminated abruptly. Any blocked writes will be unblocked and return errors.

    Reset sends the application protocol error code, which must be less than
    2^62, to the peer. It does not wait for the peer to acknowledge receipt of
    the error. Use Close to wait for the peer's acknowledgement.

    Reset does not affect reads. Use CloseRead to abort reads on the stream.

func (s *Stream) SetReadContext(ctx context.Context)
    SetReadContext sets the context used for reads from the stream.

    It is not safe to call SetReadContext concurrently.

func (s *Stream) SetWriteContext(ctx context.Context)
    SetWriteContext sets the context used for writes to the stream. The write
    context is also used by Close when waiting for writes to be received by the
    peer.

    It is not safe to call SetWriteContext concurrently.

func (s *Stream) Write(b []byte) (n int, err error)
    Write writes data to the stream.

    Write writes data to the stream write buffer. Buffered data is only sent
    when the buffer is sufficiently full. Call the Flush method to ensure
    buffered data is sent.

func (s *Stream) WriteByte(c byte) error
    WriteByte writes a single byte to the stream.

type StreamErrorCode uint64
    A StreamErrorCode is an application protocol error code (RFC 9000, Section
    20.2) indicating why a stream is being closed.

func (e StreamErrorCode) Error() string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
