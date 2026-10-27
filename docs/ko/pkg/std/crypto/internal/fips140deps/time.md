# package crypto/internal/fips140deps/time

- 원문: <https://pkg.go.dev/crypto/internal/fips140deps/time>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package time // import "crypto/internal/fips140deps/time"


FUNCTIONS

func HighPrecisionNow() int64
    HighPrecisionNow returns a high-resolution timestamp suitable for measuring
    small time differences. It uses Windows' QueryPerformanceCounter.

    Its unit, epoch, and resolution are unspecified, and may change, but can be
    assumed to be sufficiently precise to measure time differences on the order
    of tens to hundreds of nanoseconds.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
