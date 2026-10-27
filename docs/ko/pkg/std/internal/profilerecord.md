# package internal/profilerecord

- 원문: <https://pkg.go.dev/internal/profilerecord>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package profilerecord holds internal types used to represent profiling records with deep stack traces.

## 원문 요약

Package profilerecord holds internal types used to represent profiling records with deep stack traces.

## API 상세 (go doc -all)

~~~text
package profilerecord // import "internal/profilerecord"

Package profilerecord holds internal types used to represent profiling records
with deep stack traces.

TODO: Consider moving this to internal/runtime, see golang.org/issue/65355.

TYPES

type BlockProfileRecord struct {
	Count  int64
	Cycles int64
	Stack  []uintptr
}

type MemProfileRecord struct {
	ObjectSize                int64
	AllocObjects, FreeObjects int64
	Stack                     []uintptr
}

func (r *MemProfileRecord) InUseBytes() int64

func (r *MemProfileRecord) InUseObjects() int64

type StackRecord struct {
	Stack []uintptr
}
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
