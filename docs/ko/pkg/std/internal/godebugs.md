# package internal/godebugs

- 원문: <https://pkg.go.dev/internal/godebugs>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package godebugs provides a table of known GODEBUG settings, for use by a variety of other packages, including internal/godebug, runtime, runtime/metrics, and cmd/go/internal/load.

## 원문 요약

Package godebugs provides a table of known GODEBUG settings, for use by a variety of other packages, including internal/godebug, runtime, runtime/metrics, and cmd/go/internal/load.

## API 상세 (go doc -all)

~~~text
package godebugs // import "internal/godebugs"

Package godebugs provides a table of known GODEBUG settings, for use by a
variety of other packages, including internal/godebug, runtime, runtime/metrics,
and cmd/go/internal/load.

VARIABLES

var All = []Info{
	{Name: "allowmultiplevcs", Package: "cmd/go"},
	{Name: "containermaxprocs", Package: "runtime", Changed: 25, Old: "0"},
	{Name: "cryptocustomrand", Package: "crypto", Changed: 26, Old: "1"},
	{Name: "dataindependenttiming", Package: "crypto/subtle", Opaque: true},
	{Name: "decoratemappings", Package: "runtime", Opaque: true, Changed: 25, Old: "0"},
	{Name: "embedfollowsymlinks", Package: "cmd/go"},
	{Name: "execerrdot", Package: "os/exec"},
	{Name: "fips140", Package: "crypto/fips140", Opaque: true, Immutable: true},
	{Name: "fips140ems", Package: "crypto/tls"},
	{Name: "gocachehash", Package: "cmd/go"},
	{Name: "gocachetest", Package: "cmd/go"},
	{Name: "gocacheverify", Package: "cmd/go"},
	{Name: "gotestjsonbuildtext", Package: "cmd/go", Changed: 24, Old: "1"},
	{Name: "htmlmetacontenturlescape", Package: "html/template"},
	{Name: "http2client", Package: "net/http"},
	{Name: "http2debug", Package: "net/http", Opaque: true},
	{Name: "http2server", Package: "net/http"},
	{Name: "httpcookiemaxnum", Package: "net/http", Changed: 24, Old: "0"},
	{Name: "httplaxcontentlength", Package: "net/http", Changed: 22, Old: "1"},
	{Name: "httpmuxgo121", Package: "net/http", Changed: 22, Old: "1"},
	{Name: "httpservecontentkeepheaders", Package: "net/http", Changed: 23, Old: "1"},
	{Name: "httpservecontentmaxranges", Package: "net/http", Changed: 26, Old: "1"},
	{Name: "installgoroot", Package: "go/build"},
	{Name: "jstmpllitinterp", Package: "html/template", Opaque: true},

	{Name: "multipartmaxheaders", Package: "mime/multipart"},
	{Name: "multipartmaxparts", Package: "mime/multipart"},
	{Name: "multipathtcp", Package: "net", Changed: 24, Old: "0"},
	{Name: "netdns", Package: "net", Opaque: true},
	{Name: "netedns0", Package: "net", Changed: 19, Old: "0"},
	{Name: "panicnil", Package: "runtime", Changed: 21, Old: "1"},
	{Name: "randautoseed", Package: "math/rand"},
	{Name: "randseednop", Package: "math/rand", Changed: 24, Old: "0"},
	{Name: "rsa1024min", Package: "crypto/rsa", Changed: 24, Old: "0"},
	{Name: "tarinsecurepath", Package: "archive/tar"},
	{Name: "tlsmaxrsasize", Package: "crypto/tls"},
	{Name: "tlsmlkem", Package: "crypto/tls", Changed: 24, Old: "0", Opaque: true},
	{Name: "tlssecpmlkem", Package: "crypto/tls", Changed: 26, Old: "0", Opaque: true},
	{Name: "tlssha1", Package: "crypto/tls", Changed: 25, Old: "1"},

	{Name: "tracebacklabels", Package: "runtime", Changed: 27, Old: "0", Opaque: true},
	{Name: "updatemaxprocs", Package: "runtime", Changed: 25, Old: "0"},
	{Name: "urlmaxqueryparams", Package: "net/url", Changed: 24, Old: "0"},
	{Name: "urlstrictcolons", Package: "net/url", Changed: 26, Old: "0"},
	{Name: "winreadlinkvolume", Package: "os", Changed: 23, Old: "0"},
	{Name: "winsymlink", Package: "os", Changed: 23, Old: "0"},
	{Name: "x509negativeserial", Package: "crypto/x509", Changed: 23, Old: "1"},
	{Name: "x509rsacrt", Package: "crypto/x509", Changed: 24, Old: "0"},
	{Name: "x509sha256skid", Package: "crypto/x509", Changed: 25, Old: "0"},
	{Name: "x509sslcertoverrideplatform", Package: "crypto/x509", Changed: 27, Old: "0"},
	{Name: "x509usefallbackroots", Package: "crypto/x509"},
	{Name: "x509usepolicies", Package: "crypto/x509", Changed: 24, Old: "0"},
	{Name: "zipinsecurepath", Package: "archive/zip"},
}
    All is the table of known settings, sorted by Name.

    Note: After adding entries to this table, run 'go generate runtime/metrics'
    to update the runtime/metrics doc comment. (Otherwise the runtime/metrics
    test will fail.)

    Note: After adding entries to this table, update the list in doc/godebug.md
    as well. (Otherwise the test in this package will fail.)

var Removed = []RemovedInfo{
	{Name: "x509sha1", Removed: 24, Old: one},
	{Name: "tlskyber", Removed: 24, Old: zero},
	{Name: "gotypesalias", Removed: 27, Old: zero},
	{Name: "tlsunsafeekm", Removed: 27, Old: one},
	{Name: "tlsrsakex", Removed: 27, Old: one},
	{Name: "tls3des", Removed: 27, Old: one},
	{Name: "tls10server", Removed: 27, Old: one},
	{Name: "x509keypairleaf", Removed: 27, Old: zero},
	{Name: "asynctimerchan", Removed: 27, Old: func(s string) bool { return s == "1" || s == "2" }},
}
    Removed contains all GODEBUGs that we have removed.

    Every removed GODEBUG must have a corresponding section in doc/godebug.md,
    since cmd/go links to that document when a removed GODEBUG is used.


TYPES

type Info struct {
	Name      string // name of the setting ("panicnil")
	Package   string // package that uses the setting ("runtime")
	Changed   int    // minor version when default changed, if any; 21 means Go 1.21
	Old       string // value that restores behavior prior to Changed
	Opaque    bool   // setting does not export information to runtime/metrics using [internal/godebug.Setting.IncNonDefault]
	Immutable bool   // setting cannot be changed after program start
}
    An Info describes a single known GODEBUG setting.

func Lookup(name string) *Info
    Lookup returns the Info with the given name.

type RemovedInfo struct {
	Name    string            // name of the removed GODEBUG setting.
	Removed int               // minor version of Go, when the removal happened
	Old     func(string) bool // reports whether the GODEBUG value (argument) is an old (invalid) value
}
    A RemovedInfo describes a GODEBUG setting that has been removed.

    Per the policy for removing GODEBUG settings (go.dev/issue/76163), using any
    non-"old" value for the removed setting is permissible. Using an old value,
    indicating a non-final default value for that setting, leads to a build or
    vet error. To support multiple "old" values (see asynctimerchan), the Old
    field is a predicate.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
