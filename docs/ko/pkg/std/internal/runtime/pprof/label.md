# package internal/runtime/pprof/label

- 원문: <https://pkg.go.dev/internal/runtime/pprof/label>
- 분류: Go 표준 라이브러리

## 한국어 요약

`label` 패키지는 `runtime`과 `runtime/pprof` 패키지 모두에서 사용되는 공통 선언을 제공합니다.

## 원문 요약

Package label provides common declarations used by both the runtime and runtime/pprof packages.

## API 상세 (go doc -all)

~~~text
package label // import "internal/runtime/pprof/label"

Package label provides common declarations used by both the runtime
and runtime/pprof packages. The Set type is used for goroutine labels,
and is duplicated as runtime/pprof.LabelSet. The type is duplicated due to
go.dev/issue/65437 preventing the use of a type-alias in an existing public
interface.

TYPES

type Label struct {
	Key   string
	Value string
}
    Label is a key/value pair of strings.

type Set struct {
	List []Label
}
    Set is a set of labels.

func NewSet(list []Label) Set
    NewSet constructs a LabelSet that wraps the provided labels.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
