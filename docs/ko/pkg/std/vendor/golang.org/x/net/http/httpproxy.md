# package vendor/golang.org/x/net/http/httpproxy

- 원문: <https://pkg.go.dev/vendor/golang.org/x/net/http/httpproxy>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package httpproxy provides support for HTTP proxy determination based on environment variables, as provided by net/http.ProxyFromEnvironment function.

## 원문 요약

Package httpproxy provides support for HTTP proxy determination based on environment variables, as provided by net/http.ProxyFromEnvironment function.

## API 상세 (go doc -all)

~~~text
package httpproxy // import "vendor/golang.org/x/net/http/httpproxy"

Package httpproxy provides support for HTTP proxy determination based on
environment variables, as provided by net/http.ProxyFromEnvironment function.

The API is not subject to the Go 1 compatibility promise and may change at any
time.

TYPES

type Config struct {
	// HTTPProxy represents the value of the HTTP_PROXY or
	// http_proxy environment variable. It will be used as the proxy
	// URL for HTTP requests unless overridden by NoProxy.
	HTTPProxy string

	// HTTPSProxy represents the HTTPS_PROXY or https_proxy
	// environment variable. It will be used as the proxy URL for
	// HTTPS requests unless overridden by NoProxy.
	HTTPSProxy string

	// NoProxy represents the NO_PROXY or no_proxy environment
	// variable. It specifies a string that contains comma-separated values
	// specifying hosts that should be excluded from proxying. Each value is
	// represented by an IP address prefix (1.2.3.4), an IP address prefix in
	// CIDR notation (1.2.3.4/8), a domain name, or a special DNS label (*).
	// An IP address prefix and domain name can also include a literal port
	// number (1.2.3.4:80).
	// A domain name matches that name and all subdomains. A domain name with
	// a leading "." matches subdomains only. For example "foo.com" matches
	// "foo.com" and "bar.foo.com"; ".y.com" matches "x.y.com" but not "y.com".
	// A single asterisk (*) indicates that no proxying should be done.
	// A best effort is made to parse the string and errors are
	// ignored.
	NoProxy string

	// CGI holds whether the current process is running
	// as a CGI handler (FromEnvironment infers this from the
	// presence of a REQUEST_METHOD environment variable).
	// When this is set, ProxyForURL will return an error
	// when HTTPProxy applies, because a client could be
	// setting HTTP_PROXY maliciously. See https://go.dev/s/cgihttpproxy.
	CGI bool
}
    Config holds configuration for HTTP proxy settings. See FromEnvironment for
    details.

func FromEnvironment() *Config
    FromEnvironment returns a Config instance populated from the environment
    variables HTTP_PROXY, HTTPS_PROXY and NO_PROXY (or the lowercase versions
    thereof).

    The environment values may be either a complete URL or a "host[:port]",
    in which case the "http" scheme is assumed. An error is returned if the
    value is a different form.

func (cfg *Config) ProxyFunc() func(reqURL *url.URL) (*url.URL, error)
    ProxyFunc returns a function that determines the proxy URL to use for a
    given request URL. Changing the contents of cfg will not affect proxy
    functions created earlier.

    A nil URL and nil error are returned if no proxy is defined in the
    environment, or a proxy should not be used for the given request, as defined
    by NO_PROXY.

    As a special case, if reqURL.Host is "localhost" or a loopback address (with
    or without a port number), then a nil URL and nil error will be returned.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
