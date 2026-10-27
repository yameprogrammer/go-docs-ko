# package structs

- 원문: <https://pkg.go.dev/structs>
- 분류: Go 표준 라이브러리

## 한국어 요약

`structs` 패키지는 구조체의 속성을 수정하기 위해 구조체 필드로 사용할 수 있는 마커 타입들을 정의합니다.

## 원문 요약

Package structs defines marker types that can be used as struct fields to modify the properties of a struct.

## API 상세 (go doc -all)

~~~text
package structs // import "structs"

Package structs defines marker types that can be used as struct fields to modify
the properties of a struct.

By convention, a marker type should be used as the type of a field named "_",
placed at the beginning of a struct type definition.

TYPES

type HostLayout struct {
	// Has unexported fields.
}
    HostLayout marks a struct as using host memory layout. A struct with a
    field of type HostLayout will be laid out in memory according to host
    expectations, generally following the host's C ABI.

    HostLayout does not affect layout within any other struct-typed fields of
    the containing struct, nor does it affect layout of structs containing the
    struct marked as host layout.

    By convention, HostLayout should be used as the type of a field named "_",
    placed at the beginning of the struct type definition.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
