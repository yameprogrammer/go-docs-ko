# package image/gif

- 원문: <https://pkg.go.dev/image/gif>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `gif`는 GIF 이미지 디코더 및 인코더를 구현합니다.

## 원문 요약

Package gif implements a GIF image decoder and encoder.

## API 상세 (go doc -all)

~~~text
package gif // import "image/gif"

Package gif implements a GIF image decoder and encoder.

The GIF specification is at https://www.w3.org/Graphics/GIF/spec-gif89a.txt.

When decoding untrusted input, read dimensions with DecodeConfig before calling
Decode or DecodeAll; see those functions and the "Security Considerations"
section in the image package documentation.

CONSTANTS

const (
	DisposalNone       = 0x01
	DisposalBackground = 0x02
	DisposalPrevious   = 0x03
)
    Disposal Methods.


FUNCTIONS

func Decode(r io.Reader) (image.Image, error)
    Decode reads a GIF image from r and returns the first embedded image as an
    image.Image.

    When decoding images from untrusted sources, it is safest to first call
    DecodeConfig and check the image size so that unexpectedly large memory
    allocations may be safely avoided.

func DecodeConfig(r io.Reader) (image.Config, error)
    DecodeConfig returns the global color model and dimensions of a GIF image
    without decoding the entire image.

    It reads the logical screen descriptor and global color table only; it does
    not allocate pixel buffers for frames. Use it to check width and height
    before calling Decode or DecodeAll.

func Encode(w io.Writer, m image.Image, o *Options) error
    Encode writes the Image m to w in GIF format.

func EncodeAll(w io.Writer, g *GIF) error
    EncodeAll writes the images in g to w in GIF format with the given loop
    count and delay between frames.


TYPES

type GIF struct {
	Image []*image.Paletted // The successive images.
	Delay []int             // The successive delay times, one per frame, in 100ths of a second.
	// LoopCount controls the number of times an animation will be
	// restarted during display.
	// A LoopCount of 0 means to loop forever.
	// A LoopCount of -1 means to show each frame only once.
	// Otherwise, the animation is looped LoopCount+1 times.
	LoopCount int
	// Disposal is the successive disposal methods, one per frame. For
	// backwards compatibility, a nil Disposal is valid to pass to EncodeAll,
	// and implies that each frame's disposal method is 0 (no disposal
	// specified).
	Disposal []byte
	// Config is the global color table (palette), width and height. A nil or
	// empty-color.Palette Config.ColorModel means that each frame has its own
	// color table and there is no global color table. Each frame's bounds must
	// be within the rectangle defined by the two points (0, 0) and
	// (Config.Width, Config.Height).
	//
	// For backwards compatibility, a zero-valued Config is valid to pass to
	// EncodeAll, and implies that the overall GIF's width and height equals
	// the first frame's bounds' Rectangle.Max point.
	Config image.Config
	// BackgroundIndex is the background index in the global color table, for
	// use with the DisposalBackground disposal method.
	BackgroundIndex byte
}
    GIF represents the possibly multiple images stored in a GIF file.

func DecodeAll(r io.Reader) (*GIF, error)
    DecodeAll reads a GIF image from r and returns the sequential frames and
    timing information.

    Like Decode, this allocates a paletted buffer per frame from width and
    height in the image descriptors. DecodeAll retains every decoded frame in
    memory. For untrusted input, call DecodeConfig first to verify the logical
    screen size and reject inputs that would require excessive memory.

type Options struct {
	// NumColors is the maximum number of colors used in the image.
	// It ranges from 1 to 256.
	NumColors int

	// Quantizer is used to produce a palette with size NumColors.
	// palette.Plan9 is used in place of a nil Quantizer.
	Quantizer draw.Quantizer

	// Drawer is used to convert the source image to the desired palette.
	// draw.FloydSteinberg is used in place of a nil Drawer.
	Drawer draw.Drawer
}
    Options are the encoding parameters.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
