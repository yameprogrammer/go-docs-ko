# package net/internal/socktest

- 원문: <https://pkg.go.dev/net/internal/socktest>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package socktest provides utilities for socket testing.

## 원문 요약

Package socktest provides utilities for socket testing.

## API 상세 (go doc -all)

~~~text
package socktest // import "net/internal/socktest"

Package socktest provides utilities for socket testing.

TYPES

type AfterFilter func(*Status) error
    An AfterFilter represents a socket system call filter after an execution of
    a system call.

    It will only be executed after a system call for a socket that has an entry
    in internal table. If the filter returns a non-nil error, the system call
    function returns the non-nil error.

type Cookie uint64
    A Cookie represents a 3-tuple of a socket; address family, socket type and
    protocol number.

func (c Cookie) Family() int
    Family returns an address family.

func (c Cookie) Protocol() int
    Protocol returns a protocol number.

func (c Cookie) Type() int
    Type returns a socket type.

type Filter func(*Status) (AfterFilter, error)
    A Filter represents a socket system call filter.

    It will only be executed before a system call for a socket that has an entry
    in internal table. If the filter returns a non-nil error, the execution
    of system call will be canceled and the system call function returns the
    non-nil error. It can return a non-nil AfterFilter for filtering after the
    execution of the system call.

type FilterType int
    A FilterType represents a filter type.

const (
	FilterSocket        FilterType = iota // for Socket
	FilterConnect                         // for Connect or ConnectEx
	FilterListen                          // for Listen
	FilterAccept                          // for Accept, Accept4 or AcceptEx
	FilterGetsockoptInt                   // for GetsockoptInt
	FilterClose                           // for Close or Closesocket
)
type Sockets map[syscall.Handle]Status
    Sockets maps a socket descriptor to the status of socket.

type Stat struct {
	Family   int // address family
	Type     int // socket type
	Protocol int // protocol number

	Opened    uint64 // number of sockets opened
	Connected uint64 // number of sockets connected
	Listened  uint64 // number of sockets listened
	Accepted  uint64 // number of sockets accepted
	Closed    uint64 // number of sockets closed

	OpenFailed    uint64 // number of sockets open failed
	ConnectFailed uint64 // number of sockets connect failed
	ListenFailed  uint64 // number of sockets listen failed
	AcceptFailed  uint64 // number of sockets accept failed
	CloseFailed   uint64 // number of sockets close failed
}
    A Stat represents a per-cookie socket statistics.

func (st Stat) String() string

type Status struct {
	Cookie    Cookie
	Err       error // error status of socket system call
	SocketErr error // error status of socket by SO_ERROR
}
    A Status represents the status of a socket.

func (so Status) String() string

type Switch struct {
	// Has unexported fields.
}
    A Switch represents a callpath point switch for socket system calls.

func (sw *Switch) AcceptEx(ls syscall.Handle, as syscall.Handle, b *byte, rxdatalen uint32, laddrlen uint32, raddrlen uint32, rcvd *uint32, overlapped *syscall.Overlapped) error
    AcceptEx wraps syscall.AcceptEx.

func (sw *Switch) Closesocket(s syscall.Handle) (err error)
    Closesocket wraps syscall.Closesocket.

func (sw *Switch) Connect(s syscall.Handle, sa syscall.Sockaddr) (err error)
    Connect wraps syscall.Connect.

func (sw *Switch) ConnectEx(s syscall.Handle, sa syscall.Sockaddr, b *byte, n uint32, nwr *uint32, o *syscall.Overlapped) (err error)
    ConnectEx wraps syscall.ConnectEx.

func (sw *Switch) Listen(s syscall.Handle, backlog int) (err error)
    Listen wraps syscall.Listen.

func (sw *Switch) Set(t FilterType, f Filter)
    Set deploys the socket system call filter f for the filter type t.

func (sw *Switch) Sockets() Sockets
    Sockets returns mappings of socket descriptor to socket status.

func (sw *Switch) Stats() []Stat
    Stats returns a list of per-cookie socket statistics.

func (sw *Switch) WSASocket(family, sotype, proto int32, protinfo *syscall.WSAProtocolInfo, group uint32, flags uint32) (s syscall.Handle, err error)
    WSASocket wraps syscall.WSASocket.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
