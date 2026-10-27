# package encoding/pem

- 원문: <https://pkg.go.dev/encoding/pem>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 pem는 PEM 데이터 인코딩을 구현하며, 이는 프라이버시 강화 이메일에서 유래되었습니다.

## 원문 요약

Package pem implements the PEM data encoding, which originated in Privacy Enhanced Mail.

## API 상세 (go doc -all)

~~~text
package pem // import "encoding/pem"

Package pem implements the PEM data encoding, which originated in Privacy
Enhanced Mail. The most common use of PEM encoding today is in TLS keys and
certificates. See RFC 1421.

FUNCTIONS

func Encode(out io.Writer, b *Block) error
    Encode writes the PEM encoding of b to out.

func EncodeToMemory(b *Block) []byte
    EncodeToMemory returns the PEM encoding of b.

    If b has invalid headers and cannot be encoded, EncodeToMemory returns nil.
    If it is important to report details about this error case, use Encode
    instead.


TYPES

type Block struct {
	Type    string            // The type, taken from the preamble (i.e. "RSA PRIVATE KEY").
	Headers map[string]string // Optional headers.
	Bytes   []byte            // The decoded bytes of the contents. Typically a DER encoded ASN.1 structure.
}
    A Block represents a PEM encoded structure.

    The encoded form is:

        -----BEGIN Type-----
        Headers
        base64-encoded Bytes
        -----END Type-----

    where Block.Headers is a possibly empty sequence of Key: Value lines.

func Decode(data []byte) (p *Block, rest []byte)
    Decode will find the next PEM formatted block (certificate, private key etc)
    in the input. It returns that block and the remainder of the input. If no
    PEM data is found, p is nil and the whole of the input is returned in rest.
    Blocks must start at the beginning of a line and end at the end of a line.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
