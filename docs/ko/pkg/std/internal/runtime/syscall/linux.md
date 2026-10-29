# package internal/runtime/syscall/linux

- 원문: <https://pkg.go.dev/internal/runtime/syscall/linux>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package linux provides the syscall primitives required for the runtime.

## 원문 요약

Package linux provides the syscall primitives required for the runtime.

## API 상세 (go doc -all)

~~~text
package linux // import "internal/runtime/syscall/linux"

Package linux provides the syscall primitives required for the runtime.

CONSTANTS

const (
	AT_FDCWD = -0x64

	ENOENT = 0x2

	EPOLLIN       = 0x1
	EPOLLOUT      = 0x4
	EPOLLERR      = 0x8
	EPOLLHUP      = 0x10
	EPOLLRDHUP    = 0x2000
	EPOLLET       = 0x80000000
	EPOLL_CLOEXEC = 0x80000
	EPOLL_CTL_ADD = 0x1
	EPOLL_CTL_DEL = 0x2
	EPOLL_CTL_MOD = 0x3
	EFD_CLOEXEC   = 0x80000

	O_RDONLY  = 0x0
	O_CLOEXEC = 0x80000

	PR_SET_VMA           = 0x53564d41
	PR_SET_VMA_ANON_NAME = 0
)
const (
	SYS_CLOSE         = 3
	SYS_MPROTECT      = 10
	SYS_FCNTL         = 72
	SYS_PRCTL         = 157
	SYS_EPOLL_CTL     = 233
	SYS_EPOLL_PWAIT   = 281
	SYS_EPOLL_CREATE1 = 291
	SYS_EPOLL_PWAIT2  = 441
	SYS_EVENTFD2      = 290
	SYS_OPENAT        = 257
	SYS_PREAD64       = 17
	SYS_READ          = 0
	SYS_UNAME         = 63

	EFD_NONBLOCK = 0x800

	O_LARGEFILE = 0x0
)

FUNCTIONS

func Close(fd int) (errno uintptr)
func EpollCreate1(flags int32) (fd int32, errno uintptr)
func EpollCtl(epfd, op, fd int32, event *EpollEvent) (errno uintptr)
func EpollWait(epfd int32, events []EpollEvent, maxev, waitms int32) (n int32, errno uintptr)
func Eventfd(initval, flags int32) (fd int32, errno uintptr)
func Open(path *byte, mode int, perm uint32) (fd int, errno uintptr)
func Pread(fd int, p []byte, offset int64) (n int, errno uintptr)
func Read(fd int, p []byte) (n int, errno uintptr)
func Syscall6(num, a1, a2, a3, a4, a5, a6 uintptr) (r1, r2, errno uintptr)
    Syscall6 calls system call number 'num' with arguments a1-6.

func Uname(buf *Utsname) (errno uintptr)

TYPES

type EpollEvent struct {
	Events uint32
	Data   [8]byte // unaligned uintptr
}

type Utsname struct {
	Sysname    [65]byte
	Nodename   [65]byte
	Release    [65]byte
	Version    [65]byte
	Machine    [65]byte
	Domainname [65]byte
}
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
