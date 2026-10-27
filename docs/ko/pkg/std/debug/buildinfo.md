# package debug/buildinfo

- 원문: <https://pkg.go.dev/debug/buildinfo>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `buildinfo`는 Go 바이너리 내부에 포함된 정보를 사용하여, 해당 바이너리가 어떻게 빌드되었는지에 대한 정보를 제공합니다.

## 원문 요약

Package buildinfo provides access to information embedded in a Go binary about how it was built.

## API 상세 (go doc -all)

~~~text
package buildinfo // import "debug/buildinfo"

Package buildinfo provides access to information embedded in a Go binary about
how it was built. This includes the Go toolchain version, and the set of modules
used (for binaries built in module mode).

Build information is available for the currently running binary in
runtime/debug.ReadBuildInfo.

TYPES

type BuildInfo = debug.BuildInfo
    Type alias for build info. We cannot move the types here, since
    runtime/debug would need to import this package, which would make it a much
    larger dependency.

func Read(r io.ReaderAt) (*BuildInfo, error)
    Read returns build information embedded in a Go binary file accessed through
    the given ReaderAt. Most information is only available for binaries built
    with module support.

func ReadFile(name string) (info *BuildInfo, err error)
    ReadFile returns build information embedded in a Go binary file at the given
    path. Most information is only available for binaries built with module
    support.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
