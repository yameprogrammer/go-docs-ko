# package vendor/golang.org/x/crypto/internal/alias

- 원문: <https://pkg.go.dev/vendor/golang.org/x/crypto/internal/alias>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package alias implements memory aliasing tests.

## 원문 요약

Package alias implements memory aliasing tests.

## API 상세 (go doc -all)

~~~text
package alias // import "vendor/golang.org/x/crypto/internal/alias"

Package alias implements memory aliasing tests.

FUNCTIONS

func AnyOverlap(x, y []byte) bool
    AnyOverlap reports whether x and y share memory at any (not necessarily
    corresponding) index. The memory beyond the slice length is ignored.

func InexactOverlap(x, y []byte) bool
    InexactOverlap reports whether x and y share memory at any non-corresponding
    index. The memory beyond the slice length is ignored. Note that x and y can
    have different lengths and still not have any inexact overlap.

    InexactOverlap can be used to implement the requirements of the
    crypto/cipher AEAD, Block, BlockMode and Stream interfaces.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
