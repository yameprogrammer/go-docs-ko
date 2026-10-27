# package internal/asan

- 원문: <https://pkg.go.dev/internal/asan>
- 분류: Go 표준 라이브러리

## 한국어 요약

`asan` 패키지는 address sanitizer를 위해 코드를 수동으로 계측(instrumenting)하는 데 필요한 헬퍼 함수들을 포함하고 있습니다.

## 원문 요약

Package asan contains helper functions for manually instrumenting code for the address sanitizer.

## API 상세 (go doc -all)

~~~text
package asan // import "internal/asan"

Package asan contains helper functions for manually instrumenting code for the
address sanitizer. The runtime package intentionally exports these functions
only in the asan build; this package exports them unconditionally but without
the "asan" build tag they are no-ops.

CONSTANTS

const Enabled = false

FUNCTIONS

func Read(addr unsafe.Pointer, len uintptr)
func Write(addr unsafe.Pointer, len uintptr)
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
