# package image/internal/imageutil

- 원문: <https://pkg.go.dev/image/internal/imageutil>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package imageutil contains code shared by image-related packages.

## 원문 요약

Package imageutil contains code shared by image-related packages.

## API 상세 (go doc -all)

~~~text
package imageutil // import "image/internal/imageutil"

Package imageutil contains code shared by image-related packages.

FUNCTIONS

func DrawYCbCr(dst *image.RGBA, r image.Rectangle, src *image.YCbCr, sp image.Point) (ok bool)
    DrawYCbCr draws the YCbCr source image on the RGBA destination image
    with r.Min in dst aligned with sp in src. It reports whether the draw was
    successful. If it returns false, no dst pixels were changed.

    This function assumes that r is entirely within dst's bounds and the
    translation of r from dst coordinate space to src coordinate space is
    entirely within src's bounds.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
