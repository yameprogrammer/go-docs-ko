# package internal/nettest

- 원문: <https://pkg.go.dev/internal/nettest>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package nettest // import "internal/nettest"


FUNCTIONS

func NewConnPair() (*Conn, *Conn)
    NewConnPair returns a pair of connected Conns.


TYPES

type Conn struct {
	// Has unexported fields.
}
    Conn is an in-memory test implementation of net.Conn.

func (c *Conn) CanRead() bool
    CanRead reports whether Read can proceed without blocking.

func (c *Conn) Close() error
    Close closes the connection.

func (c *Conn) CloseRead() error
    CloseRead shuts down the reading side of the connection.

func (c *Conn) CloseWrite() error
    CloseWrite shuts down the writing side of the connection.

func (c *Conn) IsClosed() bool
    IsClosed reports whether the connection has been closed. A connection is
    closed if [CloseRead] and [CloseWrite] are both called, or if [Close] is
    called.

    To identify when the other side of the Conn has been closed, use
    Conn.Peer().IsClosed().

func (c *Conn) LocalAddr() net.Addr
    LocalAddr returns the (fake) local network address.

func (c *Conn) Peer() *Conn
    Peer returns the other end of the connection.

func (c *Conn) Read(b []byte) (n int, err error)
    Read reads data from the connection.

func (c *Conn) RemoteAddr() net.Addr
    LocalAddr returns the (fake) remote network address.

func (c *Conn) SetCloseError(err error)
    SetCloseError sets the error returned by Close. Close still closes the
    connection. A nil error restores the usual behavior.

func (c *Conn) SetDeadline(t time.Time) error
    SetDeadline sets the read and write deadlines for the connection.

func (c *Conn) SetLocalAddr(addr net.Addr)
    SetLocalAddr sets the local address.

    To set the remote address, set the local address of Conn's peer.

func (c *Conn) SetReadBufferSize(size int)
    SetReadBufferSize sets the connection's read buffer. Writes to the other end
    of the connection will block so long as the buffer is full. Setting the size
    to 0 blocks all writes until the size is increased.

func (c *Conn) SetReadDeadline(t time.Time) error
    SetReadDeadline sets the read deadline for the connection.

func (c *Conn) SetReadError(err error)
    SetReadError causes any currently blocked and future Read calls to return
    a net.OpError wrapping err. It does not affect the other half of the
    connection. Reads will return any buffered data before returning the error,
    including data written after the error is set and io.EOF after the other end
    is closed. A nil error restores the usual behavior.

func (c *Conn) SetWriteDeadline(t time.Time) error
    SetWriteDeadline sets the write deadline for the connection.

func (c *Conn) SetWriteError(err error)
    SetWriteError causes any currently blocked and future Write calls to
    return a net.OpError wrapping err. It does not affect the other half of the
    connection. Writes will not write data to the connection buffer while an
    error is set. A nil error restores the usual behavior.

func (c *Conn) Write(b []byte) (n int, err error)
    Write writes data to the connection.

type Listener struct {
	// Has unexported fields.
}
    Listener is an in-memory test implementation of net.Listener.

func NewListener() *Listener
    NewListener returns a new Listener.

func (li *Listener) Accept() (net.Conn, error)
    Accept waits for and returns the next connection to the listener.

    The connections returned by Accept are always [*Conn]s.

func (li *Listener) Addr() net.Addr
    Addr returns the listener's network address.

    The address is always a *net.TCPAddr.

func (li *Listener) Close() error
    Close closes the listener. Any blocked Accept operations will be unblocked
    and return errors.

func (li *Listener) NewConn() *Conn
    NewConn returns a new connection to the listener.

    Accept will return the other side of the conn.

func (li *Listener) NewConnConfig(f func(*Conn)) *Conn
    NewConnConfig returns a new connection to the listener.

    The function f is called with the new client connection. After f returns,
    Accept will return the other side of the connection.

    For example, to create a connection from a specific IP address:

        conn := li.NewConnConfig(func(conn *nettest.Conn) {
        	conn.SetLocalAddr(net.TCPAddrFromAddrPort(netip.MustParseAddrPort("10.0.0.1:1234")))
        })

func (li *Listener) SetAcceptError(err error)
    SetAcceptError causes any currently blocked and future Accept calls to
    return a net.OpError wrapping err. Accept will return any available
    connections before returning the error, including connections created after
    the error is set. A nil error restores the usual behavior.

func (li *Listener) SetAddr(addr net.Addr)
    SetAddr sets the listener's network address.

func (li *Listener) SetCloseError(err error)
    SetCloseError sets the error returned by Close. Close still closes the
    listener. A nil error restores the usual behavior.

type PacketConn struct {
	// Has unexported fields.
}

func (p *PacketConn) CanRead() bool
    CanRead reports whether [ReadFrom] can return at least one byte or an error.
    If [ReadFrom] would block, CanRead returns false.

func (p *PacketConn) Close() error
    Close closes the connection.

func (p *PacketConn) IsClosed() bool
    IsClosed reports whether the connection has been closed.

func (p *PacketConn) LocalAddr() net.Addr
    LocalAddr returns the (fake) local network address.

func (p *PacketConn) ReadFrom(b []byte) (n int, addr net.Addr, err error)
    ReadFrom reads a packet from the connection, copying the payload into b.

func (c *PacketConn) SetCloseError(err error)
    SetCloseError sets the error returned by Close. Close still closes the
    connection. A nil error restores the usual behavior.

func (p *PacketConn) SetDeadline(t time.Time) error
    SetReadDeadline sets the read deadline for the connection. PacketConns have
    no write deadline.

func (p *PacketConn) SetReadDeadline(t time.Time) error
    SetReadDeadline sets the read deadline for the connection.

func (c *PacketConn) SetReadError(err error)
    SetReadError causes any currently blocked and future ReadFrom calls to
    return a net.OpError wrapping err. It does not affect the other half of the
    connection. Reads will return any buffered data before returning the error,
    including data written after the error is set. A nil error restores the
    usual behavior.

func (p *PacketConn) SetWriteDeadline(t time.Time) error
    SetWriteDeadline has no effect. Writes to PacketConns never block.

func (c *PacketConn) SetWriteError(err error)
    SetWriteError causes any currently blocked and future WriteTo calls to
    return a net.OpError wrapping err. It does not affect the other half of the
    connection. Writes will not write data while an error is set. A nil error
    restores the usual behavior.

func (p *PacketConn) WriteTo(b []byte, addr net.Addr) (n int, err error)
    WriteTo writes a packet with payload b to addr. addr must be a *net.UDPAddr.

    WriteTo appends the packet to the recipient's receive buffer. If no
    recipient is listening on addr or if the recipient's receive buffer is full,
    the packet is silently discarded.

type PacketNet struct {
	// Has unexported fields.
}
    A PacketNet is a group of communicating [PacketConn]s.

func NewPacketNet() *PacketNet
    NewPacketNet returns a new PacketNet.

func (n *PacketNet) NewConn(a net.Addr) (*PacketConn, error)
    NewConn returns a new PacketConn listening on the given address. It returns
    an error if there is an existing listener on this address.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
