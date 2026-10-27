# package net/http/cookiejar

- 원문: <https://pkg.go.dev/net/http/cookiejar>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `cookiejar`는 [RFC 6265]에 부합하는, 메모리에 저장되는 [http.CookieJar]를 구현합니다.

## 원문 요약

Package cookiejar implements an in-memory [RFC 6265]-compliant [http.CookieJar].

## API 상세 (go doc -all)

~~~text
package cookiejar // import "net/http/cookiejar"

Package cookiejar implements an in-memory RFC 6265-compliant http.CookieJar.

[RFC 6265]: https://www.rfc-editor.org/info/rfc6265

TYPES

type Jar struct {
	// Has unexported fields.
}
    Jar implements the net/http.CookieJar interface.

func New(o *Options) (*Jar, error)
    New returns a new cookie jar. A nil *Options is equivalent to a zero
    Options.

func (j *Jar) Cookies(u *url.URL) (cookies []*http.Cookie)
    Cookies implements the Cookies method of the http.CookieJar interface.

    It returns an empty slice if the URL's scheme is not HTTP or HTTPS.

func (j *Jar) SetCookies(u *url.URL, cookies []*http.Cookie)
    SetCookies implements the SetCookies method of the http.CookieJar interface.

    It does nothing if the URL's scheme is not HTTP or HTTPS.

type Options struct {
	// PublicSuffixList is the public suffix list that determines whether
	// an HTTP server can set a cookie for a domain.
	//
	// A nil value is valid and may be useful for testing but it is not
	// secure: it means that the HTTP server for foo.co.uk can set a cookie
	// for bar.co.uk.
	PublicSuffixList PublicSuffixList
}
    Options are the options for creating a new Jar.

type PublicSuffixList interface {
	// PublicSuffix returns the public suffix of domain.
	//
	// TODO: specify which of the caller and callee is responsible for IP
	// addresses, for leading and trailing dots, for case sensitivity, and
	// for IDN/Punycode.
	PublicSuffix(domain string) string

	// String returns a description of the source of this public suffix
	// list. The description will typically contain something like a time
	// stamp or version number.
	String() string
}
    PublicSuffixList provides the public suffix of a domain. For example:
      - the public suffix of "example.com" is "com",
      - the public suffix of "foo1.foo2.foo3.co.uk" is "co.uk", and
      - the public suffix of "bar.pvt.k12.ma.us" is "pvt.k12.ma.us".

    Implementations of PublicSuffixList must be safe for concurrent use by
    multiple goroutines.

    An implementation that always returns "" is valid and may be useful for
    testing but it is not secure: it means that the HTTP server for foo.com can
    set a cookie for bar.com.

    A public suffix list implementation is in the package
    golang.org/x/net/publicsuffix.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
