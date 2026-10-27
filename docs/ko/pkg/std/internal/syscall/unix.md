# package internal/syscall/unix

- 원문: <https://pkg.go.dev/internal/syscall/unix>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package unix // import "internal/syscall/unix"


CONSTANTS

const (
	AT_EACCESS          = 0x200
	AT_FDCWD            = -0x64
	AT_REMOVEDIR        = 0x200
	AT_SYMLINK_NOFOLLOW = 0x100

	UTIME_OMIT = 0x3ffffffe

	O_PATH = 0x200000
)
const (
	R_OK = 0x4
	W_OK = 0x2
	X_OK = 0x1

	// NoFollowErrno is the error returned from open/openat called with
	// O_NOFOLLOW flag, when the trailing component (basename) of the path
	// is a symbolic link.
	NoFollowErrno = noFollowErrno
)
const (
	P_PID   = 1
	P_PIDFD = 3
)

FUNCTIONS

func CopyFileRange(rfd int, roff *int64, wfd int, woff *int64, len int, flags int) (n int, err error)
func Eaccess(path string, mode uint32) error
func Fchmodat(dirfd int, path string, mode uint32, flags int) error
func Fchownat(dirfd int, path string, uid, gid int, flags int) error
func Fcntl(fd int, cmd int, arg int) (int, error)
func Fstatat(dirfd int, path string, stat *syscall.Stat_t, flags int) error
func GetRandom(p []byte, flags GetRandomFlag) (n int, err error)
    GetRandom calls the getrandom system call.

func HasNonblockFlag(flag int) bool
func IsNonblock(fd int) (nonblocking bool, err error)
func KernelVersion() (major, minor int)
    KernelVersion returns major and minor kernel version numbers parsed from the
    syscall.Uname's Release field, or (0, 0) if the version can't be obtained or
    parsed.

func KernelVersionGE(x, y int) bool
    KernelVersionGE checks if the running kernel version is greater than or
    equal to the provided version.

func Linkat(olddirfd int, oldpath string, newdirfd int, newpath string, flag int) error
func Mkdirat(dirfd int, path string, mode uint32) error
func Openat(dirfd int, path string, flags int, perm uint32) (int, error)
func PidFDOpen(pid, flags int) (uintptr, error)
func PidFDSendSignal(pidfd uintptr, s syscall.Signal) error
func Readlinkat(dirfd int, path string, buf []byte) (int, error)
func RecvfromInet4(fd int, p []byte, flags int, from *syscall.SockaddrInet4) (int, error)
func RecvfromInet6(fd int, p []byte, flags int, from *syscall.SockaddrInet6) (n int, err error)
func RecvmsgInet4(fd int, p, oob []byte, flags int, from *syscall.SockaddrInet4) (n, oobn int, recvflags int, err error)
func RecvmsgInet6(fd int, p, oob []byte, flags int, from *syscall.SockaddrInet6) (n, oobn int, recvflags int, err error)
func Renameat(olddirfd int, oldpath string, newdirfd int, newpath string) error
func SendmsgNInet4(fd int, p, oob []byte, to *syscall.SockaddrInet4, flags int) (n int, err error)
func SendmsgNInet6(fd int, p, oob []byte, to *syscall.SockaddrInet6, flags int) (n int, err error)
func SendtoInet4(fd int, p []byte, flags int, to *syscall.SockaddrInet4) (err error)
func SendtoInet6(fd int, p []byte, flags int, to *syscall.SockaddrInet6) (err error)
func Symlinkat(oldpath string, newdirfd int, newpath string) error
func Tcsetpgrp(fd int, pgid int32) (err error)
func Unlinkat(dirfd int, path string, flags int) error
func Utimensat(dirfd int, path string, times *[2]syscall.Timespec, flag int) error
func Waitid(idType int, id int, info *SiginfoChild, options int, rusage *syscall.Rusage) error

TYPES

type GetRandomFlag uintptr
    GetRandomFlag is a flag supported by the getrandom system call.

const (
	// GRND_NONBLOCK means return EAGAIN rather than blocking.
	GRND_NONBLOCK GetRandomFlag = 0x0001

	// GRND_RANDOM means use the /dev/random pool instead of /dev/urandom.
	GRND_RANDOM GetRandomFlag = 0x0002
)
type SiginfoChild struct {
	Signo int32

	Pid    int32
	Uid    uint32
	Status int32

	// Has unexported fields.
}
    SiginfoChild is a struct filled in by Linux waitid syscall. In C, siginfo_t
    contains a union with multiple members; this struct corresponds to one used
    when Signo is SIGCHLD.

    NOTE fields are exported to be used by TestSiginfoChildLayout.

func (s *SiginfoChild) WaitStatus() (ws syscall.WaitStatus)
    WaitStatus converts SiginfoChild, as filled in by the waitid syscall,
    to syscall.WaitStatus.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
