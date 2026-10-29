# package image/jpeg

- 원문: <https://pkg.go.dev/image/jpeg>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package jpeg implements a JPEG image decoder and encoder.

## 원문 요약

Package jpeg implements a JPEG image decoder and encoder.

## API 상세 (go doc -all)

~~~text
package jpeg // import "image/jpeg"

Package jpeg implements a JPEG image decoder and encoder.

JPEG is defined in ITU-T T.81: https://www.w3.org/Graphics/JPEG/itu-t81.pdf.

CONSTANTS

const DefaultQuality = 75
    DefaultQuality is the default quality encoding parameter.


FUNCTIONS

func Decode(r io.Reader) (image.Image, error)
    Decode reads a JPEG image from r and returns it as an image.Image.

func DecodeConfig(r io.Reader) (image.Config, error)
    DecodeConfig returns the color model and dimensions of a JPEG image without
    decoding the entire image.

func Encode(w io.Writer, m image.Image, o *Options) error
    Encode writes the Image m to w in JPEG 4:2:0 baseline format with the given
    options. Default parameters are used if a nil *Options is passed.


TYPES

type FormatError string
    A FormatError reports that the input is not a valid JPEG.

func (e FormatError) Error() string

type Options struct {
	Quality int
}
    Options are the encoding parameters. Quality ranges from 1 to 100 inclusive,
    higher is better.

type Reader interface {
	io.ByteReader
	io.Reader
}
    Deprecated: Reader is not used by the image/jpeg package and should not be
    used by others. It is kept for compatibility.

type UnsupportedError string
    An UnsupportedError reports that the input uses a valid but unimplemented
    JPEG feature.

func (e UnsupportedError) Error() string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
