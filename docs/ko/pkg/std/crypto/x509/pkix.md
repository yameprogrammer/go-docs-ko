# package crypto/x509/pkix

- 원문: <https://pkg.go.dev/crypto/x509/pkix>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package pkix contains shared, low level structures used for ASN.1 parsing and serialization of X.509 certificates, CRL and OCSP.

## 원문 요약

Package pkix contains shared, low level structures used for ASN.1 parsing and serialization of X.509 certificates, CRL and OCSP.

## API 상세 (go doc -all)

~~~text
package pkix // import "crypto/x509/pkix"

Package pkix contains shared, low level structures used for ASN.1 parsing and
serialization of X.509 certificates, CRL and OCSP.

TYPES

type AlgorithmIdentifier struct {
	Algorithm  asn1.ObjectIdentifier
	Parameters asn1.RawValue `asn1:"optional"`
}
    AlgorithmIdentifier represents the ASN.1 structure of the same name. See RFC
    5280, section 4.1.1.2.

type AttributeTypeAndValue struct {
	Type  asn1.ObjectIdentifier
	Value any
}
    AttributeTypeAndValue mirrors the ASN.1 structure of the same name in RFC
    5280, Section 4.1.2.4.

    When parsed as part of a pkix.Name structure in a crypto/x509 type,
    the Value will be

      - a string if the ASN.1 type is PrintableString, IA5String, NumericString,
        BMPString, T61String, or UTF8String;
      - an int64 if the ASN.1 type is INTEGER;
      - an asn1.BitString if the ASN.1 type is BIT STRING;
      - a []byte if the ASN.1 type is OCTET STRING;
      - an asn1.ObjectIdentifier if the ASN.1 type is OBJECT IDENTIFIER;
      - a time.Time if the ASN.1 type is UTCTIME or GENERALIZEDTIME;
      - a bool if the ASN.1 type is BOOLEAN;
      - nil if the ASN.1 type is NULL;
      - an asn1.RawValue otherwise.

type AttributeTypeAndValueSET struct {
	Type  asn1.ObjectIdentifier
	Value [][]AttributeTypeAndValue `asn1:"set"`
}
    AttributeTypeAndValueSET represents a set of ASN.1 sequences of
    AttributeTypeAndValue sequences from RFC 2986 (PKCS #10).

type CertificateList struct {
	TBSCertList        TBSCertificateList
	SignatureAlgorithm AlgorithmIdentifier
	SignatureValue     asn1.BitString
}
    CertificateList represents the ASN.1 structure of the same name.
    See RFC 5280, section 5.1. Use Certificate.CheckCRLSignature to verify the
    signature.

    Deprecated: x509.RevocationList should be used instead.

func (certList *CertificateList) HasExpired(now time.Time) bool
    HasExpired reports whether certList should have been updated by now.

type Extension struct {
	Id       asn1.ObjectIdentifier
	Critical bool `asn1:"optional"`
	Value    []byte
}
    Extension represents the ASN.1 structure of the same name. See RFC 5280,
    section 4.2.

type Name struct {
	Country, Organization, OrganizationalUnit []string
	Locality, Province                        []string
	StreetAddress, PostalCode                 []string
	SerialNumber, CommonName                  string

	// Names contains all parsed attributes. When parsing distinguished names,
	// this can be used to extract non-standard attributes that are not parsed
	// by this package. When marshaling to RDNSequences, the Names field is
	// ignored, see ExtraNames.
	Names []AttributeTypeAndValue

	// ExtraNames contains attributes to be copied, raw, into any marshaled
	// distinguished names. Values override any attributes with the same OID.
	// The ExtraNames field is not populated when parsing, see Names.
	ExtraNames []AttributeTypeAndValue
}
    Name represents an X.509 distinguished name. This only includes the common
    elements of a DN. Note that Name is only an approximation of the X.509
    structure. If an accurate representation is needed, asn1.Unmarshal the raw
    subject or issuer as an RDNSequence.

func (n *Name) FillFromRDNSequence(rdns *RDNSequence)
    FillFromRDNSequence populates n from the provided RDNSequence. Multi-entry
    RDNs are flattened, all entries are added to the relevant n fields, and the
    grouping is not preserved.

func (n Name) String() string
    String returns the string form of n, roughly following the RFC 2253
    Distinguished Names syntax.

func (n Name) ToRDNSequence() (ret RDNSequence)
    ToRDNSequence converts n into a single RDNSequence. The following attributes
    are encoded as multi-value RDNs:

      - Country
      - Organization
      - OrganizationalUnit
      - Locality
      - Province
      - StreetAddress
      - PostalCode

    Each ExtraNames entry is encoded as an individual RDN.

type RDNSequence []RelativeDistinguishedNameSET

func (r RDNSequence) String() string
    String returns a string representation of the sequence r, roughly following
    the RFC 2253 Distinguished Names syntax.

type RelativeDistinguishedNameSET []AttributeTypeAndValue

type RevokedCertificate struct {
	SerialNumber   *big.Int
	RevocationTime time.Time
	Extensions     []Extension `asn1:"optional"`
}
    RevokedCertificate represents the ASN.1 structure of the same name. See RFC
    5280, section 5.1.

type TBSCertificateList struct {
	Raw                 asn1.RawContent
	Version             int `asn1:"optional,default:0"`
	Signature           AlgorithmIdentifier
	Issuer              RDNSequence
	ThisUpdate          time.Time
	NextUpdate          time.Time            `asn1:"optional"`
	RevokedCertificates []RevokedCertificate `asn1:"optional"`
	Extensions          []Extension          `asn1:"tag:0,optional,explicit"`
}
    TBSCertificateList represents the ASN.1 structure of the same name. See RFC
    5280, section 5.1.

    Deprecated: x509.RevocationList should be used instead.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
