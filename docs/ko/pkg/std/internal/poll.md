# package internal/poll

- 원문: <https://pkg.go.dev/internal/poll>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package poll supports non-blocking I/O on file descriptors with polling.

## 원문 요약

Package poll supports non-blocking I/O on file descriptors with polling.

## API 상세 (go doc -all)

~~~text
package poll // import "internal/poll"

Package poll supports non-blocking I/O on file descriptors with polling.
This supports I/O operations that block only a goroutine, not a thread. This
is used by the net and os packages. It uses a poller built into the runtime,
with support from the runtime scheduler.

VARIABLES

var AcceptFunc func(syscall.Handle, syscall.Handle, *byte, uint32, uint32, uint32, *uint32, *syscall.Overlapped) error = syscall.AcceptEx
    AcceptFunc is used to hook the accept call.

var CloseFunc func(syscall.Handle) error = syscall.Closesocket
    CloseFunc is used to hook the close call.

var ConnectExFunc func(syscall.Handle, syscall.Sockaddr, *byte, uint32, *uint32, *syscall.Overlapped) error = syscall.ConnectEx
    ConnectExFunc is used to hook the ConnectEx call.

var ErrDeadlineExceeded error = &DeadlineExceededError{}
    ErrDeadlineExceeded is returned for an expired deadline. This is exported by
    the os package as os.ErrDeadlineExceeded.

var ErrFileClosing = errors.New("use of closed file")
    ErrFileClosing is returned when a file descriptor is used after it has been
    closed.

var ErrNetClosing = errNetClosing{}
    ErrNetClosing is returned when a network descriptor is used after it has
    been closed.

var ErrNoDeadline = errors.New("file type does not support deadline")
    ErrNoDeadline is returned when a request is made to set a deadline on a file
    type that does not use the poller.

var ErrNotPollable = errors.New("not pollable")
    ErrNotPollable is returned when the file or socket is not suitable for event
    notification.

var InitWSA = sync.OnceFunc(func() {
	var d syscall.WSAData
	e := syscall.WSAStartup(uint32(0x202), &d)
	if e != nil {
		initErr = e
	}
})
    InitWSA initiates the use of the Winsock DLL by the current process.
    It is called from the net package at init time to avoid loading ws2_32.dll
    when net is not used.

var ReadConsole = syscall.ReadConsole // changed for testing
var TestHookDidSendFile = func(dstFD *FD, src uintptr, written int64, err error, handled bool) {}
var TestHookDidWritev = func(wrote int) {}
    TestHookDidWritev is a hook for testing writev.


FUNCTIONS

func DupCloseOnExec(fd int) (int, string, error)
func IsPollDescriptor(fd uintptr) bool
    IsPollDescriptor reports whether fd is the descriptor being used by the
    poller. This is only used for testing.

    IsPollDescriptor should be an internal detail, but widely used packages
    access it using linkname. Notable members of the hall of shame include:
      - github.com/opencontainers/runc

    Do not remove or change the type signature. See go.dev/issue/67401.

func SendFile(fd *FD, src uintptr, size int64) (written int64, err error, handled bool)
    SendFile wraps the TransmitFile call.


TYPES

type DeadlineExceededError struct{}
    DeadlineExceededError is returned for an expired deadline.

func (e *DeadlineExceededError) Error() string
    Implement the net.Error interface. The string is "i/o timeout" because that
    is what was returned by earlier Go versions. Changing it may break programs
    that match on error strings.

func (e *DeadlineExceededError) Temporary() bool

func (e *DeadlineExceededError) Timeout() bool

type FD struct {

	// System file descriptor. Immutable until Close.
	Sysfd syscall.Handle

	// Whether this is a streaming descriptor, as opposed to a
	// packet-based descriptor like a UDP socket.
	IsStream bool

	// Whether a zero byte read indicates EOF. This is false for a
	// message based socket connection.
	ZeroReadIsEOF bool

	// Has unexported fields.
}
    FD is a file descriptor. The net and os packages embed this type in a larger
    type representing a network connection or OS file.

func (fd *FD) Accept(sysSocket func() (syscall.Handle, error)) (syscall.Handle, []syscall.RawSockaddrAny, uint32, string, error)
    Accept handles accepting a socket. The sysSocket parameter is used to
    allocate the net socket.

func (fd *FD) Close() error
    Close closes the FD. The underlying file descriptor is closed by the destroy
    method when there are no remaining references.

func (fd *FD) ConnectEx(ra syscall.Sockaddr) error
    Call ConnectEx. This doesn't need any locking, since it is only called when
    the descriptor is first created. This is here rather than in the net package
    so that it can use fd.wop.

func (fd *FD) DisassociateIOCP() error
    DisassociateIOCP disassociates the file handle from the IOCP. The
    disassociate operation will not succeed if there is any in-progress I/O
    operation on the file handle.

func (fd *FD) Fchdir() error
    Fchdir wraps syscall.Fchdir.

func (fd *FD) Fchmod(mode uint32) error
    Fchmod updates syscall.ByHandleFileInformation.Fileattributes when needed.

func (fd *FD) Fchown(uid, gid int) error
    Fchown wraps syscall.Fchown.

func (fd *FD) Fsync() error
    Fsync wraps syscall.Fsync.

func (fd *FD) Ftruncate(size int64) error
    Ftruncate wraps syscall.Ftruncate.

func (fd *FD) GetFileInformationByHandle(data *syscall.ByHandleFileInformation) error
    GetFileInformationByHandle wraps GetFileInformationByHandle.

func (fd *FD) GetFileType() (uint32, error)
    GetFileType wraps syscall.GetFileType.

func (fd *FD) GetsockoptInt(level, name int) (int, error)
    GetsockoptInt wraps the getsockopt network call with an int argument.

func (fd *FD) Init(net string, pollable bool) error
    Init initializes the FD. The Sysfd field should already be set. This can
    be called multiple times on a single FD. The net argument is a network
    name from the net package (e.g., "tcp"), or "file" or "console" or "dir".
    Set pollable to true if fd should be managed by runtime netpoll. Pollable
    must be set to true for overlapped fds.

func (fd *FD) Pread(buf []byte, off int64) (int, error)
    Pread emulates the Unix pread system call.

func (fd *FD) Pwrite(buf []byte, off int64) (int, error)
    Pwrite emulates the Unix pwrite system call.

func (fd *FD) RawControl(f func(uintptr)) error
    RawControl invokes the user-defined function f for a non-IO operation.

func (fd *FD) RawRead(f func(uintptr) bool) error
    RawRead invokes the user-defined function f for a read operation.

func (fd *FD) RawWrite(f func(uintptr) bool) error
    RawWrite invokes the user-defined function f for a write operation.

func (fd *FD) Read(buf []byte) (int, error)
    Read implements io.Reader.

func (fd *FD) ReadFrom(buf []byte) (int, syscall.Sockaddr, error)
    ReadFrom wraps the recvfrom network call.

func (fd *FD) ReadFromInet4(buf []byte, sa4 *syscall.SockaddrInet4) (int, error)
    ReadFromInet4 wraps the recvfrom network call for IPv4.

func (fd *FD) ReadFromInet6(buf []byte, sa6 *syscall.SockaddrInet6) (int, error)
    ReadFromInet6 wraps the recvfrom network call for IPv6.

func (fd *FD) ReadMsg(p []byte, oob []byte, flags int) (int, int, int, syscall.Sockaddr, error)
    ReadMsg wraps the WSARecvMsg network call.

func (fd *FD) ReadMsgInet4(p []byte, oob []byte, flags int, sa4 *syscall.SockaddrInet4) (int, int, int, error)
    ReadMsgInet4 is ReadMsg, but specialized to return a syscall.SockaddrInet4.

func (fd *FD) ReadMsgInet6(p []byte, oob []byte, flags int, sa6 *syscall.SockaddrInet6) (int, int, int, error)
    ReadMsgInet6 is ReadMsg, but specialized to return a syscall.SockaddrInet6.

func (fd *FD) Seek(offset int64, whence int) (int64, error)
    Seek wraps syscall.Seek.

func (fd *FD) SetDeadline(t time.Time) error
    SetDeadline sets the read and write deadlines associated with fd.

func (fd *FD) SetReadDeadline(t time.Time) error
    SetReadDeadline sets the read deadline associated with fd.

func (fd *FD) SetWriteDeadline(t time.Time) error
    SetWriteDeadline sets the write deadline associated with fd.

func (fd *FD) SetsockoptIPMreq(level, name int, mreq *syscall.IPMreq) error
    SetsockoptIPMreq wraps the setsockopt network call with an IPMreq argument.

func (fd *FD) SetsockoptIPv6Mreq(level, name int, mreq *syscall.IPv6Mreq) error
    SetsockoptIPv6Mreq wraps the setsockopt network call with an IPv6Mreq
    argument.

func (fd *FD) SetsockoptInet4Addr(level, name int, arg [4]byte) error
    SetsockoptInet4Addr wraps the setsockopt network call with an IPv4 address.

func (fd *FD) SetsockoptInt(level, name, arg int) error
    SetsockoptInt wraps the setsockopt network call with an int argument.

func (fd *FD) SetsockoptLinger(level, name int, l *syscall.Linger) error
    SetsockoptLinger wraps the setsockopt network call with a Linger argument.

func (fd *FD) Shutdown(how int) error
    Shutdown wraps syscall.Shutdown.

func (fd *FD) WSAIoctl(iocc uint32, inbuf *byte, cbif uint32, outbuf *byte, cbob uint32, cbbr *uint32, overlapped *syscall.Overlapped, completionRoutine uintptr) error
    WSAIoctl wraps the WSAIoctl network call.

func (fd *FD) Write(buf []byte) (int, error)
    Write implements io.Writer.

func (fd *FD) WriteMsg(p []byte, oob []byte, sa syscall.Sockaddr) (int, int, error)
    WriteMsg wraps the WSASendMsg network call.

func (fd *FD) WriteMsgInet4(p []byte, oob []byte, sa *syscall.SockaddrInet4) (int, int, error)
    WriteMsgInet4 is WriteMsg specialized for syscall.SockaddrInet4.

func (fd *FD) WriteMsgInet6(p []byte, oob []byte, sa *syscall.SockaddrInet6) (int, int, error)
    WriteMsgInet6 is WriteMsg specialized for syscall.SockaddrInet6.

func (fd *FD) WriteTo(buf []byte, sa syscall.Sockaddr) (int, error)
    WriteTo wraps the sendto network call.

func (fd *FD) WriteToInet4(buf []byte, sa4 *syscall.SockaddrInet4) (int, error)
    WriteToInet4 is WriteTo, specialized for syscall.SockaddrInet4.

func (fd *FD) WriteToInet6(buf []byte, sa6 *syscall.SockaddrInet6) (int, error)
    WriteToInet6 is WriteTo, specialized for syscall.SockaddrInet6.

func (fd *FD) Writev(buf *[][]byte) (int64, error)
    Writev emulates the Unix writev system call.

type String string
    String is an internal string definition for methods/functions that is not
    intended for use outside the standard libraries.

    Other packages in std that import internal/poll and have some exported APIs
    (now we've got some in net.rawConn) which are only used internally and are
    not intended to be used outside the standard libraries, Therefore, we make
    those APIs use internal types like poll.FD or poll.String in their function
    signatures to disable the usability of these APIs from external codebase.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
