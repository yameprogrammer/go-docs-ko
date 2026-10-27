# package uuid

- 원문: <https://pkg.go.dev/uuid>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 uuid는 UUID 생성 및 조작을 위한 기능을 제공합니다.

## 원문 요약

Package uuid provides support for generating and manipulating UUIDs.

## API 상세 (go doc -all)

~~~text
package uuid // import "uuid"

Package uuid provides support for generating and manipulating UUIDs.

See RFC 9562 for details.

Random components of new UUIDs are generated with a cryptographically secure
random number generator.

UUIDs may be generated using various algorithms. The New function returns a new
UUID generated using an algorithm suitable for most purposes.

[RFC 9562]: https://www.rfc-editor.org/rfc/rfc9562.html

TYPES

type UUID [16]byte
    A UUID is a Universally Unique Identifier as specified in RFC 9562.

    UUIDs are comparable, such as with the == operator.

func Max() UUID
    Max returns the Max UUID ffffffff-ffff-ffff-ffff-ffffffffffff.

    The Max UUID is defined in Section 5.10 of RFC 9562.

[Section 5.10 of RFC 9562]: https://www.rfc-editor.org/rfc/rfc9562#section-5.10

func MustParse(s string) UUID
    MustParse returns the UUID represented by s.

    It panics if s is not a valid string representation of a UUID as defined by
    Parse.

func New() UUID
    New returns a new UUID.

    Programs which do not have a need for a specific UUID generation algorithm
    should use New. At this time, New is equivalent to NewV4.

func NewV4() UUID
    NewV4 returns a new version 4 UUID.

    Version 4 UUIDs contain 122 bits of random data.

func NewV7() UUID
    NewV7 returns a new version 7 UUID.

    Version 7 UUIDs contain a timestamp in the most significant 48 bits,
    and at least 62 bits of random data.

    NewV7 always returns UUIDs which sort in increasing order, except when the
    system clock moves backwards.

func Nil() UUID
    Nil returns the Nil UUID 00000000-0000-0000-0000-000000000000.

    The Nil UUID is defined in Section 5.9 of RFC 9562. Note that this is not
    the same as the Go value nil.

[Section 5.9 of RFC 9562]: https://www.rfc-editor.org/rfc/rfc9562#section-5.9

func Parse(s string) (UUID, error)
    Parse returns the UUID represented by s.

    It accepts strings in the following forms:

        f81d4fae-7dec-11d0-a765-00a0c91e6bf6
        {f81d4fae-7dec-11d0-a765-00a0c91e6bf6}
        urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6
        f81d4fae7dec11d0a76500a0c91e6bf6

    Alphabetic characters in the hexadecimal digits may be any case.

func (u UUID) AppendText(b []byte) ([]byte, error)
    AppendText implements the encoding.TextAppender interface. The encoding is
    the same as returned by UUID.String

func (u UUID) Compare(v UUID) int
    Compare compares the UUID u with v. If u is before v, it returns -1.
    If u is after v, it returns +1. If they are the same, it returns 0.

    Compare uses the big-endian byte order defined in Section 6.11 of RFC 9562
    for sorting.

[Section 6.11 of RFC 9562]: https://www.rfc-editor.org/rfc/rfc9562#section-6.11

func (u UUID) MarshalText() ([]byte, error)
    MarshalText implements the encoding.TextMarshaler interface. The encoding is
    the same as returned by UUID.String

func (u UUID) String() string
    String returns the string representation of u.

    It uses the lowercase hex-and-dash representation defined in RFC 9562.

func (u *UUID) UnmarshalText(b []byte) error
    UnmarshalText implements the encoding.TextUnmarshaler interface. The UUID is
    expected in a form accepted by Parse.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
