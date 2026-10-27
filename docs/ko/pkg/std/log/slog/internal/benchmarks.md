# package log/slog/internal/benchmarks

- 원문: <https://pkg.go.dev/log/slog/internal/benchmarks>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `benchmarks`는 `slog`에 대한 벤치마크를 포함합니다.

## 원문 요약

Package benchmarks contains benchmarks for slog.

## API 상세 (go doc -all)

~~~text
package benchmarks // import "log/slog/internal/benchmarks"

Package benchmarks contains benchmarks for slog.

These benchmarks are loosely based on github.com/uber-go/zap/benchmarks.
They have the following desirable properties:

  - They test a complete log event, from the user's call to its return.

  - The benchmarked code is run concurrently in multiple goroutines, to better
    simulate a real server (the most common environment for structured logs).

  - Some handlers are optimistic versions of real handlers, doing real-world
    tasks as fast as possible (and sometimes faster, in that an implementation
    may not be concurrency-safe). This gives us an upper bound on handler
    performance, so we can evaluate the (handler-independent) core activity of
    the package in an end-to-end context without concern that a slow handler
    implementation is skewing the results.

  - We also test the built-in handlers, for comparison.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
