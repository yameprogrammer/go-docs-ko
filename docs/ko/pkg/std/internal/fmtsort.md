# package internal/fmtsort

- 원문: <https://pkg.go.dev/internal/fmtsort>
- 분류: Go 표준 라이브러리

## 한국어 요약

`fmtsort` 패키지는 `fmt` 및 `text/template` 패키지를 대신하여 맵(map)에 대한 일반적인 안정적 정렬 메커니즘을 제공합니다.

## 원문 요약

Package fmtsort provides a general stable ordering mechanism for maps, on behalf of the fmt and text/template packages.

## API 상세 (go doc -all)

~~~text
package fmtsort // import "internal/fmtsort"

Package fmtsort provides a general stable ordering mechanism for maps, on behalf
of the fmt and text/template packages. It is not guaranteed to be efficient and
works only for types that are valid map keys.

TYPES

type KeyValue struct {
	Key, Value reflect.Value
}
    KeyValue holds a single key and value pair found in a map.

type SortedMap []KeyValue
    SortedMap is a slice of KeyValue pairs that simplifies sorting and iterating
    over map entries.

    Each KeyValue pair contains a map key and its corresponding value.

func Sort(mapValue reflect.Value) SortedMap
    Sort accepts a map and returns a SortedMap that has the same keys and values
    but in a stable sorted order according to the keys, modulo issues raised by
    unorderable key values such as NaNs.

    The ordering rules are more general than with Go's < operator:

      - when applicable, nil compares low
      - ints, floats, and strings order by <
      - NaN compares less than non-NaN floats
      - bool compares false before true
      - complex compares real, then imag
      - pointers compare by machine address
      - channel values compare by machine address
      - structs compare each field in turn
      - arrays compare each element in turn. Otherwise identical arrays compare
        by length.
      - interface values compare first by reflect.Type describing the concrete
        type and then by concrete value as described in the previous rules.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
