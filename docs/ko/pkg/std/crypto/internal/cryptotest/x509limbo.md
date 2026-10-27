# package crypto/internal/cryptotest/x509limbo

- 원문: <https://pkg.go.dev/crypto/internal/cryptotest/x509limbo>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package x509limbo // import "crypto/internal/cryptotest/x509limbo"


CONSTANTS

const X509LimboModule = "github.com/C2SP/x509-limbo"
    X509LimboModule is the module path of the upstream x509-limbo project.

const X509LimboVersion = "v0.0.0-20260522003327-feb7caccc1af"
    X509LimboVersion is the X509LimboModule version that schema.go was generated
    against.


TYPES

type ExpectedResult string

const ExpectedResultFAILURE ExpectedResult = "FAILURE"
const ExpectedResultSUCCESS ExpectedResult = "SUCCESS"
func (j *ExpectedResult) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type Feature string

const FeatureDenialOfService Feature = "denial-of-service"
const FeatureHasCertPolicies Feature = "has-cert-policies"
const FeatureHasCrl Feature = "has-crl"
const FeatureHasPolicyConstraints Feature = "has-policy-constraints"
const FeatureMaxChainDepth Feature = "max-chain-depth"
const FeatureNameConstraintDn Feature = "name-constraint-dn"
const FeatureNoCertPolicies Feature = "no-cert-policies"
const FeaturePedanticPublicSuffixWildcard Feature = "pedantic-public-suffix-wildcard"
const FeaturePedanticRfc5280 Feature = "pedantic-rfc5280"
const FeaturePedanticSerialNumber Feature = "pedantic-serial-number"
const FeaturePedanticWebpkiEku Feature = "pedantic-webpki-eku"
const FeaturePedanticWebpkiSubscriberKey Feature = "pedantic-webpki-subscriber-key"
const FeatureRfc5280IncompatibleWithWebpki Feature = "rfc5280-incompatible-with-webpki"
func (j *Feature) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type Importance string

const ImportanceCritical Importance = "critical"
const ImportanceHigh Importance = "high"
const ImportanceLow Importance = "low"
const ImportanceMedium Importance = "medium"
const ImportanceUndetermined Importance = "undetermined"
func (j *Importance) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type KeyUsage string

const KeyUsageCRLSign KeyUsage = "cRLSign"
const KeyUsageContentCommitment KeyUsage = "contentCommitment"
const KeyUsageDataEncipherment KeyUsage = "dataEncipherment"
const KeyUsageDecipherOnly KeyUsage = "decipherOnly"
const KeyUsageDigitalSignature KeyUsage = "digitalSignature"
const KeyUsageEncipherOnly KeyUsage = "encipherOnly"
const KeyUsageKeyAgreement KeyUsage = "keyAgreement"
const KeyUsageKeyCertSign KeyUsage = "keyCertSign"
const KeyUsageKeyEncipherment KeyUsage = "keyEncipherment"
func (j *KeyUsage) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type KnownEKUs string

const KnownEKUsAnyExtendedKeyUsage KnownEKUs = "anyExtendedKeyUsage"
const KnownEKUsClientAuth KnownEKUs = "clientAuth"
const KnownEKUsCodeSigning KnownEKUs = "codeSigning"
const KnownEKUsEmailProtection KnownEKUs = "emailProtection"
const KnownEKUsOCSPSigning KnownEKUs = "OCSPSigning"
const KnownEKUsServerAuth KnownEKUs = "serverAuth"
const KnownEKUsTimeStamping KnownEKUs = "timeStamping"
func (j *KnownEKUs) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type Limbo struct {
	// One or more testcases in this testsuite
	Testcases []Testcase `json:"testcases"`

	// The limbo schema version; this must currently always be 1
	Version int `json:"version"`
}
    The top-level testcase container.

func (j *Limbo) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type PeerKind string

const PeerKindDNS PeerKind = "DNS"
const PeerKindIP PeerKind = "IP"
const PeerKindRFC822 PeerKind = "RFC822"
func (j *PeerKind) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type PeerName struct {
	// The kind of peer name
	Kind PeerKind `json:"kind"`

	// The peer's name
	Value string `json:"value"`
}
    Represents a peer (i.e., end entity) certificate's name (Subject or SAN).

func (j *PeerName) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type SignatureAlgorithm string

const SignatureAlgorithmDSAWITHSHA1 SignatureAlgorithm = "DSA_WITH_SHA1"
const SignatureAlgorithmDSAWITHSHA224 SignatureAlgorithm = "DSA_WITH_SHA224"
const SignatureAlgorithmDSAWITHSHA256 SignatureAlgorithm = "DSA_WITH_SHA256"
const SignatureAlgorithmDSAWITHSHA384 SignatureAlgorithm = "DSA_WITH_SHA384"
const SignatureAlgorithmDSAWITHSHA512 SignatureAlgorithm = "DSA_WITH_SHA512"
const SignatureAlgorithmECDSAWITHSHA1 SignatureAlgorithm = "ECDSA_WITH_SHA1"
const SignatureAlgorithmECDSAWITHSHA224 SignatureAlgorithm = "ECDSA_WITH_SHA224"
const SignatureAlgorithmECDSAWITHSHA256 SignatureAlgorithm = "ECDSA_WITH_SHA256"
const SignatureAlgorithmECDSAWITHSHA3224 SignatureAlgorithm = "ECDSA_WITH_SHA3_224"
const SignatureAlgorithmECDSAWITHSHA3256 SignatureAlgorithm = "ECDSA_WITH_SHA3_256"
const SignatureAlgorithmECDSAWITHSHA3384 SignatureAlgorithm = "ECDSA_WITH_SHA3_384"
const SignatureAlgorithmECDSAWITHSHA3512 SignatureAlgorithm = "ECDSA_WITH_SHA3_512"
const SignatureAlgorithmECDSAWITHSHA384 SignatureAlgorithm = "ECDSA_WITH_SHA384"
const SignatureAlgorithmECDSAWITHSHA512 SignatureAlgorithm = "ECDSA_WITH_SHA512"
const SignatureAlgorithmED25519 SignatureAlgorithm = "ED25519"
const SignatureAlgorithmED448 SignatureAlgorithm = "ED448"
const SignatureAlgorithmGOSTR34102012WITH34112012256 SignatureAlgorithm = "GOSTR3410_2012_WITH_3411_2012_256"
const SignatureAlgorithmGOSTR34102012WITH34112012512 SignatureAlgorithm = "GOSTR3410_2012_WITH_3411_2012_512"
const SignatureAlgorithmGOSTR341194WITH34102001 SignatureAlgorithm = "GOSTR3411_94_WITH_3410_2001"
const SignatureAlgorithmRSASSAPSS SignatureAlgorithm = "RSASSA_PSS"
const SignatureAlgorithmRSAWITHMD5 SignatureAlgorithm = "RSA_WITH_MD5"
const SignatureAlgorithmRSAWITHSHA1 SignatureAlgorithm = "RSA_WITH_SHA1"
const SignatureAlgorithmRSAWITHSHA224 SignatureAlgorithm = "RSA_WITH_SHA224"
const SignatureAlgorithmRSAWITHSHA256 SignatureAlgorithm = "RSA_WITH_SHA256"
const SignatureAlgorithmRSAWITHSHA3224 SignatureAlgorithm = "RSA_WITH_SHA3_224"
const SignatureAlgorithmRSAWITHSHA3256 SignatureAlgorithm = "RSA_WITH_SHA3_256"
const SignatureAlgorithmRSAWITHSHA3384 SignatureAlgorithm = "RSA_WITH_SHA3_384"
const SignatureAlgorithmRSAWITHSHA3512 SignatureAlgorithm = "RSA_WITH_SHA3_512"
const SignatureAlgorithmRSAWITHSHA384 SignatureAlgorithm = "RSA_WITH_SHA384"
const SignatureAlgorithmRSAWITHSHA512 SignatureAlgorithm = "RSA_WITH_SHA512"
func (j *SignatureAlgorithm) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type Testcase struct {
	// A list of testcase IDs that this testcase is mutually incompatible with
	ConflictsWith []string `json:"conflicts_with,omitempty,omitzero"`

	// A list of PEM-encoded Certificate Revocation Lists (CRLs)
	Crls []string `json:"crls,omitempty,omitzero"`

	// A short, Markdown-formatted description
	Description string `json:"description"`

	// For server (i.e. client-side) validation: the expected peer name, if any
	ExpectedPeerName *TestcaseExpectedPeerName `json:"expected_peer_name,omitempty,omitzero"`

	// For client (i.e. server-side) validation: the expected peer names
	ExpectedPeerNames []PeerName `json:"expected_peer_names"`

	// The expected validation result
	ExpectedResult ExpectedResult `json:"expected_result"`

	// A constraining list of extended key usages, either in well-known form or as
	// OIDs
	ExtendedKeyUsage []KnownEKUs `json:"extended_key_usage"`

	// Zero or more human-readable tags that describe OPTIONAL functionality described
	// by this testcase. Implementers should use this to specify testcases for
	// non-mandatory X.509 behavior (like certificate policy validation) or for
	// 'pedantic' cases. Consumers that don't understand a given feature should skip
	// tests that are marked with it.
	Features []Feature `json:"features,omitempty,omitzero"`

	// A short, unique identifier for this testcase
	Id string `json:"id"`

	// The testcase's importance
	Importance Importance `json:"importance,omitempty,omitzero"`

	// A constraining list of key usages
	KeyUsage []KeyUsage `json:"key_usage"`

	// The maximum chain-building depth
	MaxChainDepth interface{} `json:"max_chain_depth,omitempty,omitzero"`

	// The PEM-encoded peer (EE) certificate
	PeerCertificate string `json:"peer_certificate"`

	// The PEM-encoded private key for the peer certificate, if present
	PeerCertificateKey interface{} `json:"peer_certificate_key,omitempty,omitzero"`

	// A list of acceptable signature algorithms to constrain against
	SignatureAlgorithms []SignatureAlgorithm `json:"signature_algorithms"`

	// A list of PEM-encoded CA certificates to consider trusted
	TrustedCerts []string `json:"trusted_certs"`

	// A list of PEM-encoded untrusted intermediates to use during path building
	UntrustedIntermediates []string `json:"untrusted_intermediates"`

	// The kind of validation to perform
	ValidationKind ValidationKind `json:"validation_kind"`

	// The time at which to perform the validation
	ValidationTime interface{} `json:"validation_time,omitempty,omitzero"`
}
    Represents an individual Limbo testcase.

func (j *Testcase) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type TestcaseExpectedPeerName struct {
	// The kind of peer name
	Kind PeerKind `json:"kind"`

	// The peer's name
	Value string `json:"value"`
}
    For server (i.e. client-side) validation: the expected peer name, if any

func (j *TestcaseExpectedPeerName) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type TestcaseExpectedPeerName_0 = PeerName

type TestcaseMaxChainDepth_0 *int

type TestcasePeerCertificateKey_0 *string

type TestcaseValidationTime_0 *time.Time

type ValidationKind string

const ValidationKindCLIENT ValidationKind = "CLIENT"
const ValidationKindSERVER ValidationKind = "SERVER"
func (j *ValidationKind) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
