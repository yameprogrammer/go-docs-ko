# package vendor/golang.org/x/crypto/cryptobyte/asn1

- 원문: <https://pkg.go.dev/vendor/golang.org/x/crypto/cryptobyte/asn1>
- 분류: Go 표준 라이브러리

## 한국어 요약

`asn1` 패키지는 `cryptobyte` 패키지를 사용하여 ASN.1 메시지를 파싱하고 구축하는 데 필요한 지원 타입을 제공합니다.

## 원문 요약

Package asn1 contains supporting types for parsing and building ASN.1 messages with the cryptobyte package.

## API 상세 (go doc -all)

~~~text
package asn1 // import "vendor/golang.org/x/crypto/cryptobyte/asn1"

Package asn1 contains supporting types for parsing and building ASN.1 messages
with the cryptobyte package.

CONSTANTS

const (
	BOOLEAN           = Tag(1)
	INTEGER           = Tag(2)
	BIT_STRING        = Tag(3)
	OCTET_STRING      = Tag(4)
	NULL              = Tag(5)
	OBJECT_IDENTIFIER = Tag(6)
	ENUM              = Tag(10)
	UTF8String        = Tag(12)
	SEQUENCE          = Tag(16 | classConstructed)
	SET               = Tag(17 | classConstructed)
	PrintableString   = Tag(19)
	T61String         = Tag(20)
	IA5String         = Tag(22)
	UTCTime           = Tag(23)
	GeneralizedTime   = Tag(24)
	GeneralString     = Tag(27)
)
    The following is a list of standard tag and class combinations.


TYPES

type Tag uint8
    Tag represents an ASN.1 identifier octet, consisting of a tag number
    (indicating a type) and class (such as context-specific or constructed).

    Methods in the cryptobyte package only support the low-tag-number form,
    i.e. a single identifier octet with bits 7-8 encoding the class and bits 1-6
    encoding the tag number.

func (t Tag) Constructed() Tag
    Constructed returns t with the constructed class bit set.

func (t Tag) ContextSpecific() Tag
    ContextSpecific returns t with the context-specific class bit set.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
