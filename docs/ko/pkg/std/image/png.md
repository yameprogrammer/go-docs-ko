# package image/png

- 원문: <https://pkg.go.dev/image/png>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package png implements a PNG image decoder and encoder.

## 원문 요약

Package png implements a PNG image decoder and encoder.

## API 상세 (go doc -all)

~~~text
package png // import "image/png"

Package png implements a PNG image decoder and encoder.

The PNG specification is at https://www.w3.org/TR/PNG/.

FUNCTIONS

func Decode(r io.Reader) (image.Image, error)
    Decode reads a PNG image from r and returns it as an image.Image. The type
    of Image returned depends on the PNG contents.

func DecodeConfig(r io.Reader) (image.Config, error)
    DecodeConfig returns the color model and dimensions of a PNG image without
    decoding the entire image.

func Encode(w io.Writer, m image.Image) error
    Encode writes the Image m to w in PNG format. Any Image may be encoded,
    but images that are not image.NRGBA might be encoded lossily.

    Note that the exact bytes written to w are not covered by the Go 1
    compatibility promise. Callers, including tests, should not depend on the
    exact written bytes.


TYPES

type CompressionLevel int
    CompressionLevel indicates the compression level.

const (
	DefaultCompression CompressionLevel = 0
	NoCompression      CompressionLevel = -1
	BestSpeed          CompressionLevel = -2
	BestCompression    CompressionLevel = -3
)
type Encoder struct {
	CompressionLevel CompressionLevel

	// BufferPool optionally specifies a buffer pool to get temporary
	// EncoderBuffers when encoding an image.
	BufferPool EncoderBufferPool
}
    Encoder configures encoding PNG images.

func (enc *Encoder) Encode(w io.Writer, m image.Image) error
    Encode writes the Image m to w in PNG format.

    Note that the exact bytes written to w are not covered by the Go 1
    compatibility promise. Callers, including tests, should not depend on the
    exact written bytes.

type EncoderBuffer encoder
    EncoderBuffer holds the buffers used for encoding PNG images.

type EncoderBufferPool interface {
	Get() *EncoderBuffer
	Put(*EncoderBuffer)
}
    EncoderBufferPool is an interface for getting and returning temporary
    instances of the EncoderBuffer struct. This can be used to reuse buffers
    when encoding multiple images.

type FormatError string
    A FormatError reports that the input is not a valid PNG.

func (e FormatError) Error() string

type UnsupportedError string
    An UnsupportedError reports that the input uses a valid but unimplemented
    PNG feature.

func (e UnsupportedError) Error() string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
