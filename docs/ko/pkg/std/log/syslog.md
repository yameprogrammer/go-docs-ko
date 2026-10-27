# package log/syslog

- 원문: <https://pkg.go.dev/log/syslog>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package syslog provides a simple interface to the system log service.

## 원문 요약

Package syslog provides a simple interface to the system log service.

## API 상세 (go doc -all)

~~~text
package syslog // import "log/syslog"

Package syslog provides a simple interface to the system log service. It can
send messages to the syslog daemon using UNIX domain sockets, UDP or TCP.

Only one call to Dial is necessary. On write failures, the syslog client will
attempt to reconnect to the server and write again.

The syslog package is frozen and is not accepting new features. Some external
packages provide more functionality. See:

    https://godoc.org/?q=syslog

BUG: This package is not implemented on Windows. As the
syslog package is frozen, Windows users are encouraged to
use a package outside of the standard library. For background,
see https://golang.org/issue/1108.

BUG: This package is not implemented on Plan 9.

BUG: As of Darwin's macOS 12.X (Monterey), Apple's syslog daemon no
longer listens on a UNIX domain socket and instead now uses their proprietary
Apple Unified Logging (AUL) system, hence this package will no longer work.
Please see https://developer.apple.com/documentation/os/logging.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
