# package image/draw

- 원문: <https://pkg.go.dev/image/draw>
- 분류: Go 표준 라이브러리

## 한국어 요약

`draw` 패키지는 이미지 합성 함수를 제공합니다.

## 원문 요약

Package draw provides image composition functions.

## API 상세 (go doc -all)

~~~text
package draw // import "image/draw"

Package draw provides image composition functions.

See "The Go image/draw package" for an introduction to this package:
https://golang.org/doc/articles/image_draw.html

FUNCTIONS

func Draw(dst Image, r image.Rectangle, src image.Image, sp image.Point, op Op)
    Draw calls DrawMask with a nil mask.

func DrawMask(dst Image, r image.Rectangle, src image.Image, sp image.Point, mask image.Image, mp image.Point, op Op)
    DrawMask aligns r.Min in dst with sp in src and mp in mask and then replaces
    the rectangle r in dst with the result of a Porter-Duff composition.
    A nil mask is treated as opaque.


TYPES

type Drawer interface {
	// Draw aligns r.Min in dst with sp in src and then replaces the
	// rectangle r in dst with the result of drawing src on dst.
	Draw(dst Image, r image.Rectangle, src image.Image, sp image.Point)
}
    Drawer contains the Draw method.

var FloydSteinberg Drawer = floydSteinberg{}
    FloydSteinberg is a Drawer that is the Src Op with Floyd-Steinberg error
    diffusion.

type Image interface {
	image.Image
	Set(x, y int, c color.Color)
}
    Image is an image.Image with a Set method to change a single pixel.

type Op int
    Op is a Porter-Duff compositing operator.

const (
	// Over specifies ``(src in mask) over dst''.
	Over Op = iota
	// Src specifies ``src in mask''.
	Src
)
func (op Op) Draw(dst Image, r image.Rectangle, src image.Image, sp image.Point)
    Draw implements the Drawer interface by calling the Draw function with this
    Op.

type Quantizer interface {
	// Quantize appends up to cap(p) - len(p) colors to p and returns the
	// updated palette suitable for converting m to a paletted image.
	Quantize(p color.Palette, m image.Image) color.Palette
}
    Quantizer produces a palette for an image.

type RGBA64Image interface {
	image.RGBA64Image
	Set(x, y int, c color.Color)
	SetRGBA64(x, y int, c color.RGBA64)
}
    RGBA64Image extends both the Image and image.RGBA64Image interfaces with
    a SetRGBA64 method to change a single pixel. SetRGBA64 is equivalent to
    calling Set, but it can avoid allocations from converting concrete color
    types to the color.Color interface type.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
