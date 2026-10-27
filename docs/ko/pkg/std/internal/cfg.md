# package internal/cfg

- 원문: <https://pkg.go.dev/internal/cfg>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `cfg`는 `go` 명령어와 `internal/testenv`에서 공유되는 설정을 포함합니다.

## 원문 요약

Package cfg holds configuration shared by the Go command and internal/testenv.

## API 상세 (go doc -all)

~~~text
package cfg // import "internal/cfg"

Package cfg holds configuration shared by the Go command and internal/testenv.
Definitions that don't need to be exposed outside of cmd/go should be in
cmd/go/internal/cfg instead of this package.

CONSTANTS

const KnownEnv = `
	AR
	CC
	CGO_CFLAGS
	CGO_CFLAGS_ALLOW
	CGO_CFLAGS_DISALLOW
	CGO_CPPFLAGS
	CGO_CPPFLAGS_ALLOW
	CGO_CPPFLAGS_DISALLOW
	CGO_CXXFLAGS
	CGO_CXXFLAGS_ALLOW
	CGO_CXXFLAGS_DISALLOW
	CGO_ENABLED
	CGO_FFLAGS
	CGO_FFLAGS_ALLOW
	CGO_FFLAGS_DISALLOW
	CGO_LDFLAGS
	CGO_LDFLAGS_ALLOW
	CGO_LDFLAGS_DISALLOW
	CXX
	FC
	GCCGO
	GO111MODULE
	GO386
	GOAMD64
	GOARCH
	GOARM
	GOARM64
	GOAUTH
	GOBIN
	GOCACHE
	GOCACHEPROG
	GOENV
	GOEXE
	GOEXPERIMENT
	GOFIPS140
	GOFLAGS
	GOGCCFLAGS
	GOHOSTARCH
	GOHOSTOS
	GOINSECURE
	GOMIPS
	GOMIPS64
	GOMODCACHE
	GONOPROXY
	GONOSUMDB
	GOOS
	GOPATH
	GOPPC64
	GOPRIVATE
	GOPROXY
	GORISCV64
	GOROOT
	GOSUMDB
	GOTMPDIR
	GOTOOLCHAIN
	GOTOOLDIR
	GOVCS
	GOWASM
	GOWORK
	GO_EXTLINK_ENABLED
	PKG_CONFIG
`
    KnownEnv is a list of environment variables that affect the operation of the
    Go command.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
