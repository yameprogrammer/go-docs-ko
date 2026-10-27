# package internal/race

- 원문: <https://pkg.go.dev/internal/race>
- 분류: Go 표준 라이브러리

## 한국어 요약

`race` 패키지는 레이스 디텍터(race detector)를 위해 코드를 수동으로 인스트루멘테이션(instrumenting)하는 데 필요한 헬퍼 함수들을 포함하고 있습니다.

## 원문 요약

Package race contains helper functions for manually instrumenting code for the race detector.

## API 상세 (go doc -all)

~~~text
package race // import "internal/race"

Package race contains helper functions for manually instrumenting code for the
race detector.

The runtime package intentionally exports these functions only in the race
build; this package exports them unconditionally but without the "race" build
tag they are no-ops.

CONSTANTS

const Enabled = false

FUNCTIONS

func Acquire(addr unsafe.Pointer)
func Disable()
func Enable()
func Errors() int
func Read(addr unsafe.Pointer)
func ReadObjectPC(t *abi.Type, addr unsafe.Pointer, callerpc, pc uintptr)
func ReadPC(addr unsafe.Pointer, callerpc, pc uintptr)
func ReadRange(addr unsafe.Pointer, len int)
func Release(addr unsafe.Pointer)
func ReleaseMerge(addr unsafe.Pointer)
func Write(addr unsafe.Pointer)
func WriteObjectPC(t *abi.Type, addr unsafe.Pointer, callerpc, pc uintptr)
func WritePC(addr unsafe.Pointer, callerpc, pc uintptr)
func WriteRange(addr unsafe.Pointer, len int)
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
