# package vendor/golang.org/x/net/nettest

- 원문: <https://pkg.go.dev/vendor/golang.org/x/net/nettest>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `nettest`는 네트워크 테스트를 위한 유틸리티를 제공합니다.

## 원문 요약

Package nettest provides utilities for network testing.

## API 상세 (go doc -all)

~~~text
package nettest // import "vendor/golang.org/x/net/nettest"

Package nettest provides utilities for network testing.

FUNCTIONS

func LocalPath() (string, error)
    LocalPath returns a local path that can be used for Unix-domain protocol
    testing.

func LoopbackInterface() (*net.Interface, error)
    LoopbackInterface returns an available logical network interface for
    loopback test.

func MulticastSource(network string, ifi *net.Interface) (net.IP, error)
    MulticastSource returns a unicast IP address on ifi when ifi is an IP
    multicast-capable network interface.

    The provided network must be "ip", "ip4" or "ip6".

func NewLocalListener(network string) (net.Listener, error)
    NewLocalListener returns a listener which listens to a loopback IP address
    or local file system path.

    The provided network must be "tcp", "tcp4", "tcp6", "unix" or "unixpacket".

func NewLocalPacketListener(network string) (net.PacketConn, error)
    NewLocalPacketListener returns a packet listener which listens to a loopback
    IP address or local file system path.

    The provided network must be "udp", "udp4", "udp6" or "unixgram".

func RoutedInterface(network string, flags net.Flags) (*net.Interface, error)
    RoutedInterface returns a network interface that can route IP traffic and
    satisfies flags.

    The provided network must be "ip", "ip4" or "ip6".

func SupportsIPv4() bool
    SupportsIPv4 reports whether the platform supports IPv4 networking
    functionality.

func SupportsIPv6() bool
    SupportsIPv6 reports whether the platform supports IPv6 networking
    functionality.

func SupportsRawSocket() bool
    SupportsRawSocket reports whether the current session is available to use
    raw sockets.

func TestConn(t *testing.T, mp MakePipe)
    TestConn tests that a net.Conn implementation properly satisfies the
    interface. The tests should not produce any false positives, but may
    experience false negatives. Thus, some issues may only be detected when the
    test is run multiple times. For maximal effectiveness, run the tests under
    the race detector.

func TestableAddress(network, address string) bool
    TestableAddress reports whether address of network is testable on the
    current platform configuration.

func TestableNetwork(network string) bool
    TestableNetwork reports whether network is testable on the current platform
    configuration.

    See func Dial of the standard library for the supported networks.


TYPES

type MakePipe func() (c1, c2 net.Conn, stop func(), err error)
    MakePipe creates a connection between two endpoints and returns the pair as
    c1 and c2, such that anything written to c1 is read by c2 and vice-versa.
    The stop function closes all resources, including c1, c2, and the underlying
    net.Listener (if there is one), and should not be nil.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
