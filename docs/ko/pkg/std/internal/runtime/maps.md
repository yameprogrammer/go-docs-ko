# package internal/runtime/maps

- 원문: <https://pkg.go.dev/internal/runtime/maps>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `maps`는 Go의 기본 `map` 유형을 구현합니다.

## 원문 요약

Package maps implements Go's builtin map type.

## API 상세 (go doc -all)

~~~text
package maps // import "internal/runtime/maps"

Package maps implements Go's builtin map type.

CONSTANTS

const Use64BitHash = goarch.PtrSize == 8 && goarch.IsWasm == 0
    Use 64-bit hash on 64-bit systems, except on Wasm, where we use 32-bit hash
    (see runtime/hash32.go).


VARIABLES

var UseAeshash bool
    runtime variable to check if the processor we're running on actually
    supports the instructions used by the AES-based hash implementation.


FUNCTIONS

func AlgInit()
func MemHash(p unsafe.Pointer, h, s uintptr) uintptr
func MemHash32(k uint32, h uintptr) uintptr
func MemHash64(k uint64, h uintptr) uintptr
func StrHash(s string, h uintptr) uintptr

TYPES

type Iter struct {
	// Has unexported fields.
}

func (it *Iter) Elem() unsafe.Pointer
    Elem returns a pointer to the current element. nil indicates end of
    iteration.

    Must not be called prior to Next.

func (it *Iter) Init(typ *abi.MapType, m *Map)
    Init initializes Iter for iteration.

func (it *Iter) Initialized() bool

func (it *Iter) Key() unsafe.Pointer
    Key returns a pointer to the current key. nil indicates end of iteration.

    Must not be called prior to Next.

func (it *Iter) Map() *Map
    Map returns the map this iterator is iterating over.

func (it *Iter) Next()
    Next proceeds to the next element in iteration, which can be accessed via
    the Key and Elem methods.

    The table can be mutated during iteration, though there is no guarantee that
    the mutations will be visible to the iteration.

    Init must be called prior to Next.

type Map struct {
	// Has unexported fields.
}
    Note: changes here must be reflected in
    cmd/compile/internal/reflectdata/map.go:MapType.

func NewEmptyMap() *Map

func NewMap(mt *abi.MapType, hint uintptr, m *Map, maxAlloc uintptr) *Map
    If m is non-nil, it should be used rather than allocating.

    maxAlloc should be runtime.maxAlloc.

    TODO(prattmic): Put maxAlloc somewhere accessible.

func (m *Map) Clear(typ *abi.MapType)
    Clear deletes all entries from the map resulting in an empty map.

func (m *Map) Clone(typ *abi.MapType) *Map

func (m *Map) Delete(typ *abi.MapType, key unsafe.Pointer)

func (m *Map) Get(typ *abi.MapType, key unsafe.Pointer) (unsafe.Pointer, bool)
    Get performs a lookup of the key that key points to. It returns a pointer to
    the element, or false if the key doesn't exist.

func (m *Map) Put(typ *abi.MapType, key, elem unsafe.Pointer)

func (m *Map) PutSlot(typ *abi.MapType, key unsafe.Pointer) unsafe.Pointer
    PutSlot returns a pointer to the element slot where an inserted element
    should be written.

    PutSlot never returns nil.

func (m *Map) Used() uint64
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
