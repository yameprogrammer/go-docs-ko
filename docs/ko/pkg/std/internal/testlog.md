# package internal/testlog

- 원문: <https://pkg.go.dev/internal/testlog>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `testlog`는 테스트와 `os` 패키지 사이의 백채널 통신 경로를 제공하여, `cmd/go`가 테스트가 어떤 환경 변수 및 파일을 참조하는지 확인할 수 있도록 합니다.

## 원문 요약

Package testlog provides a back-channel communication path between tests and package os, so that cmd/go can see which environment variables and files a test consults.

## API 상세 (go doc -all)

~~~text
package testlog // import "internal/testlog"

Package testlog provides a back-channel communication path between tests and
package os, so that cmd/go can see which environment variables and files a test
consults.

FUNCTIONS

func Getenv(name string)
    Getenv calls Logger().Getenv, if a logger has been set.

func Open(name string)
    Open calls Logger().Open, if a logger has been set.

func PanicOnExit0() bool
    PanicOnExit0 reports whether to panic on a call to os.Exit(0). This is in
    the testlog package because, like other definitions in package testlog,
    it is a hook between the testing package and the os package. This is used to
    ensure that an early call to os.Exit(0) does not cause a test to pass.

func SetLogger(impl Interface)
    SetLogger sets the test logger implementation for the current process.
    It must be called only once, at process startup.

func SetPanicOnExit0(v bool)
    SetPanicOnExit0 sets panicOnExit0 to v.

    SetPanicOnExit0 should be an internal detail, but alternate implementations
    of go test in other build systems may need to access it using linkname.

    Do not remove or change the type signature. See go.dev/issue/67401.

func Stat(name string)
    Stat calls Logger().Stat, if a logger has been set.


TYPES

type Interface interface {
	Getenv(key string)
	Stat(file string)
	Open(file string)
	Chdir(dir string)
}
    Interface is the interface required of test loggers. The os package will
    invoke the interface's methods to indicate that it is inspecting the given
    environment variables or files. Multiple goroutines may call these methods
    simultaneously.

func Logger() Interface
    Logger returns the current test logger implementation. It returns nil if
    there is no logger.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
