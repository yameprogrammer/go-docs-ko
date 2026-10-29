# package internal/nettrace

- 원문: <https://pkg.go.dev/internal/nettrace>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package nettrace contains internal hooks for tracing activity in the net package.

## 원문 요약

Package nettrace contains internal hooks for tracing activity in the net package.

## API 상세 (go doc -all)

~~~text
package nettrace // import "internal/nettrace"

Package nettrace contains internal hooks for tracing activity in the net
package. This package is purely internal for use by the net/http/httptrace
package and has no stable API exposed to end users.

TYPES

type LookupIPAltResolverKey struct{}
    LookupIPAltResolverKey is a context.Context Value key used by tests to
    specify an alternate resolver func. It is not exposed to outsider users.
    (But see issue 12503) The value should be the same type as lookupIP:

        func lookupIP(ctx context.Context, host string) ([]IPAddr, error)

type Trace struct {
	// DNSStart is called with the hostname of a DNS lookup
	// before it begins.
	DNSStart func(name string)

	// DNSDone is called after a DNS lookup completes (or fails).
	// The coalesced parameter is whether singleflight de-duped
	// the call. The addrs are of type net.IPAddr but can't
	// actually be for circular dependency reasons.
	DNSDone func(netIPs []any, coalesced bool, err error)

	// ConnectStart is called before a Dial, excluding Dials made
	// during DNS lookups. In the case of DualStack (Happy Eyeballs)
	// dialing, this may be called multiple times, from multiple
	// goroutines.
	ConnectStart func(network, addr string)

	// ConnectDone is called after a Dial with the results, excluding
	// Dials made during DNS lookups. It may also be called multiple
	// times, like ConnectStart.
	ConnectDone func(network, addr string, err error)
}
    Trace contains a set of hooks for tracing events within the net package.
    Any specific hook may be nil.

type TraceKey struct{}
    TraceKey is a context.Context Value key. Its associated value should be a
    *Trace struct.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
