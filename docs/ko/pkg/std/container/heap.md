# package container/heap

- 원문: <https://pkg.go.dev/container/heap>
- 분류: Go 표준 라이브러리

## 한국어 요약

`heap` 패키지는 `heap.Interface`를 구현하는 모든 타입에 대해 힙 연산을 제공합니다.

## 원문 요약

Package heap provides heap operations for any type that implements heap.Interface.

## API 상세 (go doc -all)

~~~text
package heap // import "container/heap"

Package heap provides heap operations for any type that implements
heap.Interface. A heap is a tree with the property that each node is the
minimum-valued node in its subtree.

The minimum element in the tree is the root, at index 0.

A heap is a common way to implement a priority queue. To build a priority queue,
implement the Heap interface with the (negative) priority as the ordering for
the Less method, so Push adds items while Pop removes the highest-priority
item from the queue. The Examples include such an implementation; the file
example_pq_test.go has the complete source.

FUNCTIONS

func Fix(h Interface, i int)
    Fix re-establishes the heap ordering after the element at index i has
    changed its value. Changing the value of the element at index i and then
    calling Fix is equivalent to, but less expensive than, calling Remove(h,
    i) followed by a Push of the new value. The complexity is O(log n) where n =
    h.Len().

func Init(h Interface)
    Init establishes the heap invariants required by the other routines in
    this package. Init is idempotent with respect to the heap invariants and
    may be called whenever the heap invariants may have been invalidated.
    The complexity is O(n) where n = h.Len().

func Pop(h Interface) any
    Pop removes and returns the minimum element (according to Less) from the
    heap. The complexity is O(log n) where n = h.Len(). Pop is equivalent to
    Remove(h, 0).

func Push(h Interface, x any)
    Push pushes the element x onto the heap. The complexity is O(log n) where n
    = h.Len().

func Remove(h Interface, i int) any
    Remove removes and returns the element at index i from the heap. The
    complexity is O(log n) where n = h.Len().


TYPES

type Interface interface {
	sort.Interface
	Push(x any) // add x as element Len()
	Pop() any   // remove and return element Len() - 1.
}
    The Interface type describes the requirements for a type using the routines
    in this package. Any type that implements it may be used as a min-heap with
    the following invariants (established after Init has been called or if the
    data is empty or sorted):

        !h.Less(j, i) for 0 <= i < h.Len() and 2*i+1 <= j <= 2*i+2 and j < h.Len()

    Note that Push and Pop in this interface are for package heap's
    implementation to call. To add and remove things from the heap, use
    heap.Push and heap.Pop.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
