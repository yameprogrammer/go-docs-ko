# package vendor/golang.org/x/net/dns/dnsmessage

- 원문: <https://pkg.go.dev/vendor/golang.org/x/net/dns/dnsmessage>
- 분류: Go 표준 라이브러리

## 한국어 요약

`dnsmessage` 패키지는 대부분 RFC 1035를 준수하는 DNS 메시지 패킹(packing) 및 언패킹(unpacking) 구현을 제공합니다.

## 원문 요약

Package dnsmessage provides a mostly RFC 1035 compliant implementation of DNS message packing and unpacking.

## API 상세 (go doc -all)

~~~text
package dnsmessage // import "vendor/golang.org/x/net/dns/dnsmessage"

Package dnsmessage provides a mostly RFC 1035 compliant implementation of DNS
message packing and unpacking.

The package also supports messages with Extension Mechanisms for DNS (EDNS(0))
as defined in RFC 6891.

This implementation is designed to minimize heap allocations and avoid
unnecessary packing and unpacking as much as possible.

VARIABLES

var (
	// ErrNotStarted indicates that the prerequisite information isn't
	// available yet because the previous records haven't been appropriately
	// parsed, skipped or finished.
	ErrNotStarted = errors.New("parsing/packing of this type isn't available yet")

	// ErrSectionDone indicated that all records in the section have been
	// parsed or finished.
	ErrSectionDone = errors.New("parsing/packing of this section has completed")
)

TYPES

type AAAAResource struct {
	AAAA [16]byte
}
    An AAAAResource is an AAAA Resource record.

func (r *AAAAResource) GoString() string
    GoString implements fmt.GoStringer.GoString.

type AResource struct {
	A [4]byte
}
    An AResource is an A Resource record.

func (r *AResource) GoString() string
    GoString implements fmt.GoStringer.GoString.

type Builder struct {
	// Has unexported fields.
}
    A Builder allows incrementally packing a DNS message.

    Example usage:

        buf := make([]byte, 2, 514)
        b := NewBuilder(buf, Header{...})
        b.EnableCompression()
        // Optionally start a section and add things to that section.
        // Repeat adding sections as necessary.
        buf, err := b.Finish()
        // If err is nil, buf[2:] will contain the built bytes.

func NewBuilder(buf []byte, h Header) Builder
    NewBuilder creates a new builder with compression disabled.

    Note: Most users will want to immediately enable compression with the
    EnableCompression method. See that method's comment for why you may or may
    not want to enable compression.

    The DNS message is appended to the provided initial buffer buf (which may be
    nil) as it is built. The final message is returned by the (*Builder).Finish
    method, which includes buf[:len(buf)] and may return the same underlying
    array if there was sufficient capacity in the slice.

func (b *Builder) AAAAResource(h ResourceHeader, r AAAAResource) error
    AAAAResource adds a single AAAAResource.

func (b *Builder) AResource(h ResourceHeader, r AResource) error
    AResource adds a single AResource.

func (b *Builder) CNAMEResource(h ResourceHeader, r CNAMEResource) error
    CNAMEResource adds a single CNAMEResource.

func (b *Builder) EnableCompression()
    EnableCompression enables compression in the Builder.

    Leaving compression disabled avoids compression related allocations,
    but can result in larger message sizes. Be careful with this mode as it can
    cause messages to exceed the UDP size limit.

    According to RFC 1035, section 4.1.4, the use of compression is optional,
    but all implementations must accept both compressed and uncompressed DNS
    messages.

    Compression should be enabled before any sections are added for best
    results.

func (b *Builder) Finish() ([]byte, error)
    Finish ends message building and generates a binary message.

func (b *Builder) HTTPSResource(h ResourceHeader, r HTTPSResource) error
    HTTPSResource adds a single HTTPSResource.

func (b *Builder) MXResource(h ResourceHeader, r MXResource) error
    MXResource adds a single MXResource.

func (b *Builder) NSResource(h ResourceHeader, r NSResource) error
    NSResource adds a single NSResource.

func (b *Builder) OPTResource(h ResourceHeader, r OPTResource) error
    OPTResource adds a single OPTResource.

func (b *Builder) PTRResource(h ResourceHeader, r PTRResource) error
    PTRResource adds a single PTRResource.

func (b *Builder) Question(q Question) error
    Question adds a single Question.

func (b *Builder) SOAResource(h ResourceHeader, r SOAResource) error
    SOAResource adds a single SOAResource.

func (b *Builder) SRVResource(h ResourceHeader, r SRVResource) error
    SRVResource adds a single SRVResource.

func (b *Builder) SVCBResource(h ResourceHeader, r SVCBResource) error
    SVCBResource adds a single SVCBResource.

func (b *Builder) StartAdditionals() error
    StartAdditionals prepares the builder for packing Additionals.

func (b *Builder) StartAnswers() error
    StartAnswers prepares the builder for packing Answers.

func (b *Builder) StartAuthorities() error
    StartAuthorities prepares the builder for packing Authorities.

func (b *Builder) StartQuestions() error
    StartQuestions prepares the builder for packing Questions.

func (b *Builder) TXTResource(h ResourceHeader, r TXTResource) error
    TXTResource adds a single TXTResource.

func (b *Builder) UnknownResource(h ResourceHeader, r UnknownResource) error
    UnknownResource adds a single UnknownResource.

type CNAMEResource struct {
	CNAME Name
}
    A CNAMEResource is a CNAME Resource record.

func (r *CNAMEResource) GoString() string
    GoString implements fmt.GoStringer.GoString.

type Class uint16
    A Class is a type of network.

const (
	// ResourceHeader.Class and Question.Class
	ClassINET   Class = 1
	ClassCSNET  Class = 2
	ClassCHAOS  Class = 3
	ClassHESIOD Class = 4

	// Question.Class
	ClassANY Class = 255
)
func (c Class) GoString() string
    GoString implements fmt.GoStringer.GoString.

func (c Class) String() string
    String implements fmt.Stringer.String.

type HTTPSResource struct {
	// Alias for SVCB resource record.
	SVCBResource
}
    An HTTPSResource is an HTTPS Resource record. It has the same format as the
    SVCB record.

func (r *HTTPSResource) GoString() string
    GoString implements fmt.GoStringer.GoString.

type Header struct {
	ID                 uint16
	Response           bool
	OpCode             OpCode
	Authoritative      bool
	Truncated          bool
	RecursionDesired   bool
	RecursionAvailable bool
	AuthenticData      bool
	CheckingDisabled   bool
	RCode              RCode
}
    Header is a representation of a DNS message header.

func (m *Header) GoString() string
    GoString implements fmt.GoStringer.GoString.

type MXResource struct {
	Pref uint16
	MX   Name
}
    An MXResource is an MX Resource record.

func (r *MXResource) GoString() string
    GoString implements fmt.GoStringer.GoString.

type Message struct {
	Header
	Questions   []Question
	Answers     []Resource
	Authorities []Resource
	Additionals []Resource
}
    Message is a representation of a DNS message.

func (m *Message) AppendPack(b []byte) ([]byte, error)
    AppendPack is like Pack but appends the full Message to b and returns the
    extended buffer.

func (m *Message) GoString() string
    GoString implements fmt.GoStringer.GoString.

func (m *Message) Pack() ([]byte, error)
    Pack packs a full Message.

func (m *Message) Unpack(msg []byte) error
    Unpack parses a full Message.

type NSResource struct {
	NS Name
}
    An NSResource is an NS Resource record.

func (r *NSResource) GoString() string
    GoString implements fmt.GoStringer.GoString.

type Name struct {
	Data   [255]byte
	Length uint8
}
    A Name is a non-encoded and non-escaped domain name. It is used instead of
    strings to avoid allocations.

func MustNewName(name string) Name
    MustNewName creates a new Name from a string and panics on error.

func NewName(name string) (Name, error)
    NewName creates a new Name from a string.

func (n *Name) GoString() string
    GoString implements fmt.GoStringer.GoString.

func (n Name) String() string
    String implements fmt.Stringer.String.

    Note: characters inside the labels are not escaped in any way.

type OPTResource struct {
	Options []Option
}
    An OPTResource is an OPT pseudo Resource record.

    The pseudo resource record is part of the extension mechanisms for DNS as
    defined in RFC 6891.

func (r *OPTResource) GoString() string
    GoString implements fmt.GoStringer.GoString.

type OpCode uint16
    An OpCode is a DNS operation code.

func (o OpCode) GoString() string
    GoString implements fmt.GoStringer.GoString.

type Option struct {
	Code uint16 // option code
	Data []byte
}
    An Option represents a DNS message option within OPTResource.

    The message option is part of the extension mechanisms for DNS as defined in
    RFC 6891.

func (o *Option) GoString() string
    GoString implements fmt.GoStringer.GoString.

type PTRResource struct {
	PTR Name
}
    A PTRResource is a PTR Resource record.

func (r *PTRResource) GoString() string
    GoString implements fmt.GoStringer.GoString.

type Parser struct {
	// Has unexported fields.
}
    A Parser allows incrementally parsing a DNS message.

    When parsing is started, the Header is parsed. Next, each Question can be
    either parsed or skipped. Alternatively, all Questions can be skipped at
    once. When all Questions have been parsed, attempting to parse Questions
    will return the ErrSectionDone error. After all Questions have been either
    parsed or skipped, all Answers, Authorities and Additionals can be either
    parsed or skipped in the same way, and each type of Resource must be fully
    parsed or skipped before proceeding to the next type of Resource.

    Parser is safe to copy to preserve the parsing state.

    Note that there is no requirement to fully skip or parse the message.

func (p *Parser) AAAAResource() (AAAAResource, error)
    AAAAResource parses a single AAAAResource.

    One of the XXXHeader methods must have been called before calling this
    method.

func (p *Parser) AResource() (AResource, error)
    AResource parses a single AResource.

    One of the XXXHeader methods must have been called before calling this
    method.

func (p *Parser) Additional() (Resource, error)
    Additional parses a single Additional Resource.

func (p *Parser) AdditionalHeader() (ResourceHeader, error)
    AdditionalHeader parses a single Additional ResourceHeader.

func (p *Parser) AllAdditionals() ([]Resource, error)
    AllAdditionals parses all Additional Resources.

func (p *Parser) AllAnswers() ([]Resource, error)
    AllAnswers parses all Answer Resources.

func (p *Parser) AllAuthorities() ([]Resource, error)
    AllAuthorities parses all Authority Resources.

func (p *Parser) AllQuestions() ([]Question, error)
    AllQuestions parses all Questions.

func (p *Parser) Answer() (Resource, error)
    Answer parses a single Answer Resource.

func (p *Parser) AnswerHeader() (ResourceHeader, error)
    AnswerHeader parses a single Answer ResourceHeader.

func (p *Parser) Authority() (Resource, error)
    Authority parses a single Authority Resource.

func (p *Parser) AuthorityHeader() (ResourceHeader, error)
    AuthorityHeader parses a single Authority ResourceHeader.

func (p *Parser) CNAMEResource() (CNAMEResource, error)
    CNAMEResource parses a single CNAMEResource.

    One of the XXXHeader methods must have been called before calling this
    method.

func (p *Parser) HTTPSResource() (HTTPSResource, error)
    HTTPSResource parses a single HTTPSResource.

    One of the XXXHeader methods must have been called before calling this
    method.

func (p *Parser) MXResource() (MXResource, error)
    MXResource parses a single MXResource.

    One of the XXXHeader methods must have been called before calling this
    method.

func (p *Parser) NSResource() (NSResource, error)
    NSResource parses a single NSResource.

    One of the XXXHeader methods must have been called before calling this
    method.

func (p *Parser) OPTResource() (OPTResource, error)
    OPTResource parses a single OPTResource.

    One of the XXXHeader methods must have been called before calling this
    method.

func (p *Parser) PTRResource() (PTRResource, error)
    PTRResource parses a single PTRResource.

    One of the XXXHeader methods must have been called before calling this
    method.

func (p *Parser) Question() (Question, error)
    Question parses a single Question.

func (p *Parser) SOAResource() (SOAResource, error)
    SOAResource parses a single SOAResource.

    One of the XXXHeader methods must have been called before calling this
    method.

func (p *Parser) SRVResource() (SRVResource, error)
    SRVResource parses a single SRVResource.

    One of the XXXHeader methods must have been called before calling this
    method.

func (p *Parser) SVCBResource() (SVCBResource, error)
    SVCBResource parses a single SVCBResource.

    One of the XXXHeader methods must have been called before calling this
    method.

func (p *Parser) SkipAdditional() error
    SkipAdditional skips a single Additional Resource.

    It does not perform a complete validation of the resource header, which
    means it may return a nil error when the [AdditionalHeader] would actually
    return an error.

func (p *Parser) SkipAllAdditionals() error
    SkipAllAdditionals skips all Additional Resources.

func (p *Parser) SkipAllAnswers() error
    SkipAllAnswers skips all Answer Resources.

func (p *Parser) SkipAllAuthorities() error
    SkipAllAuthorities skips all Authority Resources.

func (p *Parser) SkipAllQuestions() error
    SkipAllQuestions skips all Questions.

func (p *Parser) SkipAnswer() error
    SkipAnswer skips a single Answer Resource.

    It does not perform a complete validation of the resource header,
    which means it may return a nil error when the [AnswerHeader] would actually
    return an error.

func (p *Parser) SkipAuthority() error
    SkipAuthority skips a single Authority Resource.

    It does not perform a complete validation of the resource header, which
    means it may return a nil error when the [AuthorityHeader] would actually
    return an error.

func (p *Parser) SkipQuestion() error
    SkipQuestion skips a single Question.

func (p *Parser) Start(msg []byte) (Header, error)
    Start parses the header and enables the parsing of Questions.

func (p *Parser) TXTResource() (TXTResource, error)
    TXTResource parses a single TXTResource.

    One of the XXXHeader methods must have been called before calling this
    method.

func (p *Parser) UnknownResource() (UnknownResource, error)
    UnknownResource parses a single UnknownResource.

    One of the XXXHeader methods must have been called before calling this
    method.

type Question struct {
	Name  Name
	Type  Type
	Class Class
}
    A Question is a DNS query.

func (q *Question) GoString() string
    GoString implements fmt.GoStringer.GoString.

type RCode uint16
    An RCode is a DNS response status code.

const (
	RCodeSuccess        RCode = 0 // NoError
	RCodeFormatError    RCode = 1 // FormErr
	RCodeServerFailure  RCode = 2 // ServFail
	RCodeNameError      RCode = 3 // NXDomain
	RCodeNotImplemented RCode = 4 // NotImp
	RCodeRefused        RCode = 5 // Refused
)
    Header.RCode values.

func (r RCode) GoString() string
    GoString implements fmt.GoStringer.GoString.

func (r RCode) String() string
    String implements fmt.Stringer.String.

type Resource struct {
	Header ResourceHeader
	Body   ResourceBody
}
    A Resource is a DNS resource record.

func (r *Resource) GoString() string

type ResourceBody interface {

	// GoString implements fmt.GoStringer.GoString.
	GoString() string
	// Has unexported methods.
}
    A ResourceBody is a DNS resource record minus the header.

type ResourceHeader struct {
	// Name is the domain name for which this resource record pertains.
	Name Name

	// Type is the type of DNS resource record.
	//
	// This field will be set automatically during packing.
	Type Type

	// Class is the class of network to which this DNS resource record
	// pertains.
	Class Class

	// TTL is the length of time (measured in seconds) which this resource
	// record is valid for (time to live). All Resources in a set should
	// have the same TTL (RFC 2181 Section 5.2).
	TTL uint32

	// Length is the length of data in the resource record after the header.
	//
	// This field will be set automatically during packing.
	Length uint16
}
    A ResourceHeader is the header of a DNS resource record. There are many
    types of DNS resource records, but they all share the same header.

func (h *ResourceHeader) DNSSECAllowed() bool
    DNSSECAllowed reports whether the DNSSEC OK bit is set.

func (h *ResourceHeader) ExtendedRCode(rcode RCode) RCode
    ExtendedRCode returns an extended RCode.

    The provided rcode must be the RCode in DNS message header.

func (h *ResourceHeader) GoString() string
    GoString implements fmt.GoStringer.GoString.

func (h *ResourceHeader) SetEDNS0(udpPayloadLen int, extRCode RCode, dnssecOK bool) error
    SetEDNS0 configures h for EDNS(0).

    The provided extRCode must be an extended RCode.

type SOAResource struct {
	NS      Name
	MBox    Name
	Serial  uint32
	Refresh uint32
	Retry   uint32
	Expire  uint32

	// MinTTL the is the default TTL of Resources records which did not
	// contain a TTL value and the TTL of negative responses. (RFC 2308
	// Section 4)
	MinTTL uint32
}
    An SOAResource is an SOA Resource record.

func (r *SOAResource) GoString() string
    GoString implements fmt.GoStringer.GoString.

type SRVResource struct {
	Priority uint16
	Weight   uint16
	Port     uint16
	Target   Name // Not compressed as per RFC 2782.
}
    An SRVResource is an SRV Resource record.

func (r *SRVResource) GoString() string
    GoString implements fmt.GoStringer.GoString.

type SVCBResource struct {
	Priority uint16
	Target   Name
	Params   []SVCParam // Must be in strict increasing order by Key.
}
    An SVCBResource is an SVCB Resource record.

func (r *SVCBResource) DeleteParam(key SVCParamKey) bool
    DeleteParam deletes a parameter by key. It returns true if the parameter was
    present.

func (r *SVCBResource) GetParam(key SVCParamKey) (value []byte, ok bool)
    GetParam returns a parameter value by key.

func (r *SVCBResource) GoString() string
    GoString implements fmt.GoStringer.GoString.

func (r *SVCBResource) SetParam(key SVCParamKey, value []byte)
    SetParam sets a parameter value by key. The Params list is kept sorted by
    key.

type SVCParam struct {
	Key   SVCParamKey
	Value []byte
}
    A SVCParam is a service parameter.

func (p SVCParam) GoString() string
    GoString implements fmt.GoStringer.GoString.

type SVCParamKey uint16
    A SVCParamKey is a key for a service parameter.

const (
	SVCParamMandatory          SVCParamKey = 0
	SVCParamALPN               SVCParamKey = 1
	SVCParamNoDefaultALPN      SVCParamKey = 2
	SVCParamPort               SVCParamKey = 3
	SVCParamIPv4Hint           SVCParamKey = 4
	SVCParamECH                SVCParamKey = 5
	SVCParamIPv6Hint           SVCParamKey = 6
	SVCParamDOHPath            SVCParamKey = 7
	SVCParamOHTTP              SVCParamKey = 8
	SVCParamTLSSupportedGroups SVCParamKey = 9
)
    Values defined at
    https://www.iana.org/assignments/dns-svcb/dns-svcb.xhtml#dns-svcparamkeys.

func (k SVCParamKey) GoString() string
    GoString implements fmt.GoStringer.GoString.

func (k SVCParamKey) String() string
    String implements fmt.Stringer.String.

type TXTResource struct {
	TXT []string
}
    A TXTResource is a TXT Resource record.

func (r *TXTResource) GoString() string
    GoString implements fmt.GoStringer.GoString.

type Type uint16
    A Type is the type of a DNS Resource Record, as defined in the IANA
    registry.

[IANA registry]: https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml#dns-parameters-4

const (
	// ResourceHeader.Type and Question.Type
	TypeA     Type = 1
	TypeNS    Type = 2
	TypeCNAME Type = 5
	TypeSOA   Type = 6
	TypePTR   Type = 12
	TypeMX    Type = 15
	TypeTXT   Type = 16
	TypeAAAA  Type = 28
	TypeSRV   Type = 33
	TypeOPT   Type = 41
	TypeSVCB  Type = 64
	TypeHTTPS Type = 65

	// Question.Type
	TypeWKS   Type = 11
	TypeHINFO Type = 13
	TypeMINFO Type = 14
	TypeAXFR  Type = 252
	TypeALL   Type = 255
)
func (t Type) GoString() string
    GoString implements fmt.GoStringer.GoString.

func (t Type) String() string
    String implements fmt.Stringer.String.

type UnknownResource struct {
	Type Type
	Data []byte
}
    An UnknownResource is a catch-all container for unknown record types.

func (r *UnknownResource) GoString() string
    GoString implements fmt.GoStringer.GoString.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
