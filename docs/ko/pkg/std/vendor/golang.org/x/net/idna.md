# package vendor/golang.org/x/net/idna

- 원문: <https://pkg.go.dev/vendor/golang.org/x/net/idna>
- 분류: Go 표준 라이브러리

## 한국어 요약

package idna는 IDNA2003에서 IDNA2008로의 전환을 처리하기 위한 표준을 정의하는 UTS (Unicode Technical Standard) #46에 정의된 호환성 프로세싱을 사용하여 IDNA2008을 구현합니다.

## 원문 요약

Package idna implements IDNA2008 using the compatibility processing defined by UTS (Unicode Technical Standard) #46, which defines a standard to deal with the transition from IDNA2003.

## API 상세 (go doc -all)

~~~text
package idna // import "vendor/golang.org/x/net/idna"

Package idna implements IDNA2008 using the compatibility processing defined by
UTS (Unicode Technical Standard) #46, which defines a standard to deal with the
transition from IDNA2003.

IDNA2008 (Internationalized Domain Names for Applications),
is defined in RFC 5890, RFC 5891, RFC 5892, RFC 5893 and RFC 5894.
UTS #46 is defined in https://www.unicode.org/reports/tr46. See
https://unicode.org/cldr/utility/idna.jsp for a visualization of the differences
between these two standards.

CONSTANTS

const UnicodeVersion = "17.0.0"
    UnicodeVersion is the Unicode version from which the tables in this package
    are derived.


VARIABLES

var (
	// Punycode is a Profile that does raw punycode processing with a minimum
	// of validation.
	Punycode *Profile = punycode

	// Lookup is the recommended profile for looking up domain names, according
	// to Section 5 of RFC 5891. The exact configuration of this profile may
	// change over time.
	Lookup *Profile = lookup

	// Display is the recommended profile for displaying domain names.
	// The configuration of this profile may change over time.
	Display *Profile = display

	// Registration is the recommended profile for checking whether a given
	// IDN is valid for registration, according to Section 4 of RFC 5891.
	Registration *Profile = registration
)

FUNCTIONS

func ToASCII(s string) (string, error)
    ToASCII is a wrapper for Punycode.ToASCII.

func ToUnicode(s string) (string, error)
    ToUnicode is a wrapper for Punycode.ToUnicode.


TYPES

type Option func(*options)
    An Option configures a Profile at creation time.

func BidiRule() Option
    BidiRule enables the Bidi rule as defined in RFC 5893. Any application that
    relies on proper validation of labels should include this rule.

    This option corresponds to the CheckBidi flag in UTS #46.

func CheckHyphens(enable bool) Option
    CheckHyphens sets whether to check for correct use of hyphens ('-') in
    labels. Most web browsers do not have this option set, since labels such as
    "r3---sn-apo3qvuoxuxbt-j5pe" are in common use.

    This option corresponds to the CheckHyphens flag in UTS #46.

func CheckJoiners(enable bool) Option
    CheckJoiners sets whether to check the ContextJ rules as defined in Appendix
    A of RFC 5892, concerning the use of joiner runes.

    This option corresponds to the CheckJoiners flag in UTS #46.

func MapForLookup() Option
    MapForLookup sets validation and mapping options such that a given IDN is
    transformed for domain name lookup according to the requirements set out in
    Section 5 of RFC 5891. The mappings follow the recommendations of RFC 5894,
    RFC 5895 and UTS 46. It does not add the Bidi Rule. Use the BidiRule option
    to add this check.

    The mappings include normalization and mapping case, width and other
    compatibility mappings.

func RemoveLeadingDots(remove bool) Option
    RemoveLeadingDots removes leading label separators. Leading runes that map
    to dots, such as U+3002 IDEOGRAPHIC FULL STOP, are removed as well.

func StrictDomainName(use bool) Option
    StrictDomainName limits the set of permissible ASCII characters to
    those allowed in domain names as defined in RFC 1034 (A-Z, a-z,
    0-9 and the hyphen). This is set by default for MapForLookup and
    ValidateForRegistration, but is only useful if ValidateLabels is set.

    This option is useful, for instance, for browsers that allow
    characters outside this range, for example a '_' (U+005F LOW LINE).
    See http://www.rfc-editor.org/std/std3.txt for more details.

    This option corresponds to the UseSTD3ASCIIRules flag in UTS #46.

func Transitional(transitional bool) Option
    Transitional sets a Profile to use the Transitional mapping as defined in
    UTS #46. This will cause, for example, "ß" to be mapped to "ss". Using the
    transitional mapping provides a compromise between IDNA2003 and IDNA2008
    compatibility. It is used by some browsers when resolving domain names.
    This option is only meaningful if combined with MapForLookup.

func ValidateForRegistration() Option
    ValidateForRegistration sets validation options to verify that a given IDN
    is properly formatted for registration as defined by Section 4 of RFC 5891.

func ValidateLabels(enable bool) Option
    ValidateLabels sets whether to check the mandatory label validation criteria
    as defined in Section 5.4 of RFC 5891. This includes testing for correct use
    of hyphens ('-'), normalization, validity of runes, and the context rules.
    In particular, ValidateLabels also sets the CheckHyphens and CheckJoiners
    flags in UTS #46.

func VerifyDNSLength(verify bool) Option
    VerifyDNSLength sets whether a Profile should fail if any of the IDN parts
    are longer than allowed by the RFC.

    This option corresponds to the VerifyDnsLength flag in UTS #46.

type Profile struct {
	// Has unexported fields.
}
    A Profile defines the configuration of an IDNA mapper.

func New(o ...Option) *Profile
    New creates a new Profile.

    With no options, the returned Profile is the most permissive and equals the
    Punycode Profile. Options can be passed to further restrict the Profile.
    The MapForLookup and ValidateForRegistration options set a collection of
    options, for lookup and registration purposes respectively, which can be
    tailored by adding more fine-grained options, where later options override
    earlier options.

func (p *Profile) String() string
    String reports a string with a description of the profile for debugging
    purposes. The string format may change with different versions.

func (p *Profile) ToASCII(s string) (string, error)
    ToASCII converts a domain or domain label to its ASCII form. For example,
    ToASCII("bücher.example.com") is "xn--bcher-kva.example.com", and
    ToASCII("golang") is "golang". If an error is encountered it will return an
    error and a (partially) processed result.

func (p *Profile) ToUnicode(s string) (string, error)
    ToUnicode converts a domain or domain label to its Unicode form. For
    example, ToUnicode("xn--bcher-kva.example.com") is "bücher.example.com",
    and ToUnicode("golang") is "golang". If an error is encountered it will
    return an error and a (partially) processed result.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
