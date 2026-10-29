# package vendor/golang.org/x/net/internal/http3

- 원문: <https://pkg.go.dev/vendor/golang.org/x/net/internal/http3>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package http3 implements the HTTP/3 protocol.

## 원문 요약

Package http3 implements the HTTP/3 protocol.

## API 상세 (go doc -all)

~~~text
package http3 // import "vendor/golang.org/x/net/internal/http3"

Package http3 implements the HTTP/3 protocol.

This package is a work in progress. It is not ready for production usage.
Its API is subject to change without notice.

FUNCTIONS

func RegisterServer(s *http.Server, opts ServerOpts)
    RegisterServer adds HTTP/3 support to a net/http Server.

    RegisterServer must be called before s begins serving, and only affects
    s.ListenAndServeTLS.

func RegisterTransport(tr *http.Transport, opts TransportOpts)
    RegisterTransport configures a net/http HTTP/1 Transport to use HTTP/3.


TYPES

type ServerOpts struct {
	// ListenQUIC determines how the server will open a QUIC endpoint.
	// By default, quic.Listen("udp", addr, config) is used.
	ListenQUIC func(addr string, config *quic.Config) (*quic.Endpoint, error)

	// QUICConfig is the QUIC configuration used by the server.
	// QUICConfig may be nil and should not be modified after calling
	// RegisterServer.
	// If QUICConfig.TLSConfig is nil, the TLSConfig of the net/http Server
	// given to RegisterServer will be used.
	QUICConfig *quic.Config
}

type TransportOpts struct {
	// ListenQUIC determines how the transport will open a QUIC endpoint.
	// By default, quic.Listen("udp", addr, config) is used.
	// ListenQUIC might be called multiple times.
	ListenQUIC func(addr string, config *quic.Config) (*quic.Endpoint, error)

	// QUICConfig is the QUIC configuration used by the transport.
	// QUICConfig may be nil and should not be modified after calling
	// RegisterTransport.
	// If QUICConfig.TLSConfig is nil, the TLSConfig of the net/http Transport
	// given to RegisterTransport will be used.
	QUICConfig *quic.Config
}
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
