# package internal/msan

- 원문: <https://pkg.go.dev/internal/msan>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `msan`은 메모리 검사기를 위한 코드를 수동으로 분석하기 위한 유틸리티 함수를 포함합니다.

## 원문 요약

Package msan contains helper functions for manually instrumenting code for the memory sanitizer.

## API 상세 (go doc -all)

~~~text
package msan // import "internal/msan"

Package msan contains helper functions for manually instrumenting code for the
memory sanitizer. This package exports the private msan routines in runtime
unconditionally but without the "msan" build tag they are no-ops.

CONSTANTS

const Enabled = false

FUNCTIONS

func Free(addr unsafe.Pointer, sz uintptr)
func Malloc(addr unsafe.Pointer, sz uintptr)
func Move(dst, src unsafe.Pointer, sz uintptr)
func Read(addr unsafe.Pointer, sz uintptr)
func Write(addr unsafe.Pointer, sz uintptr)
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
