# package net/rpc/jsonrpc

- 원문: <https://pkg.go.dev/net/rpc/jsonrpc>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package jsonrpc implements a JSON-RPC 1.0 ClientCodec and ServerCodec for the rpc package.

## 원문 요약

Package jsonrpc implements a JSON-RPC 1.0 ClientCodec and ServerCodec for the rpc package.

## API 상세 (go doc -all)

~~~text
package jsonrpc // import "net/rpc/jsonrpc"

Package jsonrpc implements a JSON-RPC 1.0 ClientCodec and ServerCodec for the
rpc package. For JSON-RPC 2.0 support, see https://godoc.org/?q=json-rpc+2.0

FUNCTIONS

func Dial(network, address string) (*rpc.Client, error)
    Dial connects to a JSON-RPC server at the specified network address.

func NewClient(conn io.ReadWriteCloser) *rpc.Client
    NewClient returns a new rpc.Client to handle requests to the set of services
    at the other end of the connection.

func NewClientCodec(conn io.ReadWriteCloser) rpc.ClientCodec
    NewClientCodec returns a new rpc.ClientCodec using JSON-RPC on conn.

func NewServerCodec(conn io.ReadWriteCloser) rpc.ServerCodec
    NewServerCodec returns a new rpc.ServerCodec using JSON-RPC on conn.

func ServeConn(conn io.ReadWriteCloser)
    ServeConn runs the JSON-RPC server on a single connection. ServeConn blocks,
    serving the connection until the client hangs up. The caller typically
    invokes ServeConn in a go statement.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
