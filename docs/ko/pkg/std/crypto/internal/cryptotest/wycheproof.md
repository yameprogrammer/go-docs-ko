# package crypto/internal/cryptotest/wycheproof

- 원문: <https://pkg.go.dev/crypto/internal/cryptotest/wycheproof>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `wycheproof`는 Wycheproof 테스트 벡터 스키마 및 JSON 벡터 데이터를 기반으로 테스트를 작성하는 데 필요한 유틸리티를 제공합니다.

## 원문 요약

Package wycheproof provides helper utilities for writing tests that rely on Wycheproof test vector schemas and JSON vector data.

## API 상세 (go doc -all)

~~~text
package wycheproof // import "crypto/internal/cryptotest/wycheproof"

Package wycheproof provides helper utilities for writing tests that
rely on Wycheproof test vector schemas and JSON vector data. See
https://github.com/C2SP/wycheproof for more information.

FUNCTIONS

func LoadVectorFile(t *testing.T, filename string, value any)
    LoadVectorFile unmarshals Wycheproof JSON test vector file by name.

    Typically, the value argument will be a pointer to a Wycheproof schema type
    representing the in-memory structure of the JSON data.

    Panics if there is an error reading the Wycheproof JSON vector data file,
    or if it can't be unmarshalled into the provided value.

func MustDecodeHex(h string) []byte
    MustDecodeHex is a helper that decodes the provided string or panics.

    Many Wycheproof vector values are hex encoded strings and in a test context
    we don't intend to handle decoding errors gracefully.

func MustPanic(t *testing.T, name string, fn func())
    MustPanic calls fn and fails the test if fn does not panic.

    This is useful for testing that invalid inputs (like incorrect nonce sizes
    for AEAD ciphers) properly trigger panics rather than silently accepting the
    bad input.

func ParseHash(h string) crypto.Hash
    ParseHash maps from a Wycheproof hash name to a crypto.Hash implementation
    It panics if the provided hash name is unknown.

func ShouldPass(t *testing.T, result Result, flags []string, flagsShouldPass map[string]bool) bool
    ShouldPass returns true if a test should pass informed by expected result
    and flags.

    flagsShouldPass is a map used to determine if an "acceptable" result test
    case should pass based on test's flags. Every possible flag value that's
    associated with an "acceptable" result should be explicitly specified,
    otherwise ShouldPass will panic.

func TestName(file string, tv any) string
    TestName returns a t.Run subtest name for a Wycheproof test vector.


TYPES

type AeadTestGroup struct {
	// the IV size in bits
	IvSize int `json:"ivSize"`

	// the keySize in bits
	KeySize int `json:"keySize"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// the expected size of the tag in bits
	TagSize int `json:"tagSize"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []AeadTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type AeadTestGroupType `json:"type"`
}

func (j *AeadTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type AeadTestGroupType string

const AeadTestGroupTypeAeadTest AeadTestGroupType = "AeadTest"
func (j *AeadTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type AeadTestSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema AeadTestSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []AeadTestGroup `json:"testGroups"`
}

func (j *AeadTestSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type AeadTestSchemaV1JsonSchema string

const AeadTestSchemaV1JsonSchemaAeadTestSchemaV1Json AeadTestSchemaV1JsonSchema = "aead_test_schema_v1.json"
func (j *AeadTestSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type AeadTestVector struct {
	// additional authenticated data
	Aad string `json:"aad"`

	// A brief description of the test case
	Comment string `json:"comment"`

	// the ciphertext (without iv and tag)
	Ct string `json:"ct"`

	// A list of flags
	Flags []string `json:"flags"`

	// the nonce
	Iv string `json:"iv"`

	// the key
	Key string `json:"key"`

	// the plaintext
	Msg string `json:"msg"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// the authentication tag
	Tag string `json:"tag"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *AeadTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type AsnSignatureTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// The message to sign
	Msg string `json:"msg"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// An ASN encoded signature for msg
	Sig string `json:"sig"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *AsnSignatureTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type BlsAggregateVerifySchemaJson struct {
	// The primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// Additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// The number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema BlsAggregateVerifySchemaJsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []BlsAggregateVerifyTestGroup `json:"testGroups"`
}

func (j *BlsAggregateVerifySchemaJson) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type BlsAggregateVerifySchemaJsonSchema string

const BlsAggregateVerifySchemaJsonSchemaBlsAggregateVerifySchemaJson BlsAggregateVerifySchemaJsonSchema = "bls_aggregate_verify_schema.json"
func (j *BlsAggregateVerifySchemaJsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type BlsAggregateVerifyTestGroup struct {
	// The BLS ciphersuite identifier
	Ciphersuite string `json:"ciphersuite"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []BlsAggregateVerifyTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type BlsAggregateVerifyTestGroupType `json:"type"`
}

func (j *BlsAggregateVerifyTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type BlsAggregateVerifyTestGroupType string

const BlsAggregateVerifyTestGroupTypeBlsAggregateVerify BlsAggregateVerifyTestGroupType = "BlsAggregateVerify"
func (j *BlsAggregateVerifyTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type BlsAggregateVerifyTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// The messages that were signed
	Messages []string `json:"messages"`

	// The compressed public keys
	Pubkeys []string `json:"pubkeys"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// The aggregated BLS signature in compressed form
	Sig string `json:"sig"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *BlsAggregateVerifyTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type BlsHashToG2SchemaJson struct {
	// The primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// Additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// The number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema BlsHashToG2SchemaJsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []BlsHashToG2TestGroup `json:"testGroups"`
}

func (j *BlsHashToG2SchemaJson) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type BlsHashToG2SchemaJsonSchema string

const BlsHashToG2SchemaJsonSchemaBlsHashToG2SchemaJson BlsHashToG2SchemaJsonSchema = "bls_hash_to_g2_schema.json"
func (j *BlsHashToG2SchemaJsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type BlsHashToG2TestGroup struct {
	// The domain separation tag used for hash_to_curve
	Dst string `json:"dst"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []BlsHashToG2TestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type BlsHashToG2TestGroupType `json:"type"`
}

func (j *BlsHashToG2TestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type BlsHashToG2TestGroupType string

const BlsHashToG2TestGroupTypeBlsHashToG2 BlsHashToG2TestGroupType = "BlsHashToG2"
func (j *BlsHashToG2TestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type BlsHashToG2TestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// The expected hash-to-curve output point in compressed form
	Expected string `json:"expected"`

	// A list of flags
	Flags []string `json:"flags"`

	// The input message
	Msg string `json:"msg"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *BlsHashToG2TestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type BlsPublicKey struct {
	// The group the public key belongs to
	Group BlsPublicKeyGroup `json:"group"`

	// The size of the public key in bytes
	KeySize int `json:"keySize"`

	// The compressed public key
	Pk string `json:"pk"`
}

func (j *BlsPublicKey) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type BlsPublicKeyGroup string

const BlsPublicKeyGroupG1 BlsPublicKeyGroup = "G1"
const BlsPublicKeyGroupG2 BlsPublicKeyGroup = "G2"
func (j *BlsPublicKeyGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type BlsSigVerifySchemaJson struct {
	// The primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// Additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// The number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema BlsSigVerifySchemaJsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []BlsSigVerifyTestGroup `json:"testGroups"`
}

func (j *BlsSigVerifySchemaJson) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type BlsSigVerifySchemaJsonSchema string

const BlsSigVerifySchemaJsonSchemaBlsSigVerifySchemaJson BlsSigVerifySchemaJsonSchema = "bls_sig_verify_schema.json"
func (j *BlsSigVerifySchemaJsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type BlsSigVerifyTestGroup struct {
	// The BLS ciphersuite identifier, e.g.
	// BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_NUL_
	Ciphersuite string `json:"ciphersuite"`

	// PublicKey corresponds to the JSON schema field "publicKey".
	PublicKey BlsPublicKey `json:"publicKey"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []SignatureTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type BlsSigVerifyTestGroupType `json:"type"`
}

func (j *BlsSigVerifyTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type BlsSigVerifyTestGroupType string

const BlsSigVerifyTestGroupTypeBlsSigVerify BlsSigVerifyTestGroupType = "BlsSigVerify"
func (j *BlsSigVerifyTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type DaeadTestGroup struct {
	// the keySize in bits
	KeySize int `json:"keySize"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []DaeadTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type DaeadTestGroupType `json:"type"`
}

func (j *DaeadTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type DaeadTestGroupType string

const DaeadTestGroupTypeDaeadTest DaeadTestGroupType = "DaeadTest"
func (j *DaeadTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type DaeadTestSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema DaeadTestSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []DaeadTestGroup `json:"testGroups"`
}

func (j *DaeadTestSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type DaeadTestSchemaV1JsonSchema string

const DaeadTestSchemaV1JsonSchemaDaeadTestSchemaV1Json DaeadTestSchemaV1JsonSchema = "daead_test_schema_v1.json"
func (j *DaeadTestSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type DaeadTestVector struct {
	// additional authenticated data
	Aad string `json:"aad"`

	// A brief description of the test case
	Comment string `json:"comment"`

	// the ciphertext including tag
	Ct string `json:"ct"`

	// A list of flags
	Flags []string `json:"flags,omitempty,omitzero"`

	// the key
	Key string `json:"key"`

	// the plaintext
	Msg string `json:"msg"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *DaeadTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type DsaP1363TestGroup struct {
	// unencoded EC public key
	PublicKey DsaPublicKey `json:"publicKey"`

	// DER encoded public key
	PublicKeyDer string `json:"publicKeyDer"`

	// Pem encoded public key
	PublicKeyPem string `json:"publicKeyPem"`

	// the hash function used for DSA
	Sha string `json:"sha"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []SignatureTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type DsaP1363TestGroupType `json:"type"`
}

func (j *DsaP1363TestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type DsaP1363TestGroupType string

const DsaP1363TestGroupTypeDsaP1363Verify DsaP1363TestGroupType = "DsaP1363Verify"
func (j *DsaP1363TestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type DsaP1363VerifySchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema DsaP1363VerifySchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []DsaP1363TestGroup `json:"testGroups"`
}

func (j *DsaP1363VerifySchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type DsaP1363VerifySchemaV1JsonSchema string

const DsaP1363VerifySchemaV1JsonSchemaDsaP1363VerifySchemaV1Json DsaP1363VerifySchemaV1JsonSchema = "dsa_p1363_verify_schema_v1.json"
func (j *DsaP1363VerifySchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type DsaPublicKey struct {
	// the generator of the multiplicative subgroup
	G string `json:"g"`

	// the key size in bits
	KeySize int `json:"keySize"`

	// the modulus p
	P string `json:"p"`

	// the order of the generator g
	Q string `json:"q"`

	// the key type
	Type DsaPublicKeyType `json:"type"`

	// the public key value
	Y string `json:"y"`
}

func (j *DsaPublicKey) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type DsaPublicKeyType string

const DsaPublicKeyTypeDsaPublicKey DsaPublicKeyType = "DsaPublicKey"
func (j *DsaPublicKeyType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type DsaTestGroup struct {
	// unenocded DSA public key
	PublicKey DsaPublicKey `json:"publicKey"`

	// DER encoded public key
	PublicKeyDer string `json:"publicKeyDer"`

	// Pem encoded public key
	PublicKeyPem string `json:"publicKeyPem"`

	// the hash function used for DSA
	Sha string `json:"sha"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []AsnSignatureTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type DsaTestGroupType `json:"type"`
}

func (j *DsaTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type DsaTestGroupType string

const DsaTestGroupTypeDsaVerify DsaTestGroupType = "DsaVerify"
func (j *DsaTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type DsaVerifySchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema DsaVerifySchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []DsaTestGroup `json:"testGroups"`
}

func (j *DsaVerifySchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type DsaVerifySchemaV1JsonSchema string

const DsaVerifySchemaV1JsonSchemaDsaVerifySchemaV1Json DsaVerifySchemaV1JsonSchema = "dsa_verify_schema_v1.json"
func (j *DsaVerifySchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcCurveTest struct {
	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []EcCurveTestTestsElem `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type EcCurveTestType `json:"type"`
}
    A test for checking elliptic curve domain parameters.

func (j *EcCurveTest) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcCurveTestSchemaJson struct {
	// Algorithm corresponds to the JSON schema field "algorithm".
	Algorithm EcCurveTestSchemaJsonAlgorithm `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema EcCurveTestSchemaJsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []EcCurveTest `json:"testGroups"`
}

func (j *EcCurveTestSchemaJson) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcCurveTestSchemaJsonAlgorithm string

const EcCurveTestSchemaJsonAlgorithmEcCurveTest EcCurveTestSchemaJsonAlgorithm = "EcCurveTest"
func (j *EcCurveTestSchemaJsonAlgorithm) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcCurveTestSchemaJsonSchema string

const EcCurveTestSchemaJsonSchemaEcCurveTestSchemaJson EcCurveTestSchemaJsonSchema = "ec_curve_test_schema.json"
func (j *EcCurveTestSchemaJsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcCurveTestTestsElem struct {
	// Coefficient a of the curve's Weierstrass equation
	A string `json:"a"`

	// Coefficient b of the curve's Weierstrass equation
	B string `json:"b"`

	// A brief description of the test case
	Comment *string `json:"comment,omitempty,omitzero"`

	// A list of flags
	Flags []string `json:"flags,omitempty,omitzero"`

	// x coordinate of the curve's generator
	Gx string `json:"gx"`

	// y coordinate of the curve's generator
	Gy string `json:"gy"`

	// Cofactor of the curve
	H int `json:"h"`

	// Order of the curve
	N string `json:"n"`

	// Name identifying the elliptic curve
	Name *string `json:"name,omitempty,omitzero"`

	// Object identifier of the ellptic curve
	Oid string `json:"oid"`

	// Prime identifying the field of definition
	P string `json:"p"`

	// Standard containing the domain parameters
	Ref *string `json:"ref,omitempty,omitzero"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *EcCurveTestTestsElem) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcCurveTestType string

const EcCurveTestTypeEcCurveTest EcCurveTestType = "EcCurveTest"
func (j *EcCurveTestType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcPublicKey struct {
	// the EC group used by this public key
	Curve string `json:"curve"`

	// the key size in bits
	KeySize int `json:"keySize"`

	// the key type
	Type EcPublicKeyType `json:"type"`

	// encoded public key point
	Uncompressed string `json:"uncompressed"`

	// the x-coordinate of the public key point
	Wx string `json:"wx"`

	// the y-coordinate of the public key point
	Wy string `json:"wy"`
}

func (j *EcPublicKey) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcPublicKeyType string

const EcPublicKeyTypeEcPublicKey EcPublicKeyType = "EcPublicKey"
func (j *EcPublicKeyType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhEcpointTestGroup struct {
	// the name of the curve
	Curve string `json:"curve"`

	// the encoding of the public key
	Encoding string `json:"encoding"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []EcdhEcpointTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type EcdhEcpointTestGroupType `json:"type"`
}

func (j *EcdhEcpointTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhEcpointTestGroupType string

const EcdhEcpointTestGroupTypeEcdhEcpointTest EcdhEcpointTestGroupType = "EcdhEcpointTest"
func (j *EcdhEcpointTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhEcpointTestSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema EcdhEcpointTestSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []EcdhEcpointTestGroup `json:"testGroups"`
}

func (j *EcdhEcpointTestSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhEcpointTestSchemaV1JsonSchema string

const EcdhEcpointTestSchemaV1JsonSchemaEcdhEcpointTestSchemaV1Json EcdhEcpointTestSchemaV1JsonSchema = "ecdh_ecpoint_test_schema_v1.json"
func (j *EcdhEcpointTestSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhEcpointTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// The private exponent
	Private string `json:"private"`

	// ASN encoded public point
	Public string `json:"public"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// The shared secret key
	Shared string `json:"shared"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *EcdhEcpointTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhPemTestGroup struct {
	// the name of the curve
	Curve string `json:"curve"`

	// the encoding of the public key
	Encoding string `json:"encoding"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []EcdhPemTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type EcdhPemTestGroupType `json:"type"`
}

func (j *EcdhPemTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhPemTestGroupType string

const EcdhPemTestGroupTypeEcdhPemTest EcdhPemTestGroupType = "EcdhPemTest"
func (j *EcdhPemTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhPemTestSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema EcdhPemTestSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []EcdhPemTestGroup `json:"testGroups"`
}

func (j *EcdhPemTestSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhPemTestSchemaV1JsonSchema string

const EcdhPemTestSchemaV1JsonSchemaEcdhPemTestSchemaV1Json EcdhPemTestSchemaV1JsonSchema = "ecdh_pem_test_schema_v1.json"
func (j *EcdhPemTestSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhPemTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// Pem encoded private key
	Private string `json:"private"`

	// Pem encoded public key
	Public string `json:"public"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// The shared secret key
	Shared string `json:"shared"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *EcdhPemTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhTestGroup struct {
	// the name of the curve
	Curve string `json:"curve"`

	// the encoding of the public key
	Encoding string `json:"encoding"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []EcdhTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type EcdhTestGroupType `json:"type"`
}

func (j *EcdhTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhTestGroupType string

const EcdhTestGroupTypeEcdhTest EcdhTestGroupType = "EcdhTest"
func (j *EcdhTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhTestSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema EcdhTestSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []EcdhTestGroup `json:"testGroups"`
}

func (j *EcdhTestSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhTestSchemaV1JsonSchema string

const EcdhTestSchemaV1JsonSchemaEcdhTestSchemaV1Json EcdhTestSchemaV1JsonSchema = "ecdh_test_schema_v1.json"
func (j *EcdhTestSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// the private key
	Private string `json:"private"`

	// Encoded public key
	Public string `json:"public"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// The shared secret key
	Shared string `json:"shared"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *EcdhTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhWebcryptoTestGroup struct {
	// the name of the curve
	Curve string `json:"curve"`

	// the encoding of the public key
	Encoding string `json:"encoding"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []EcdhWebcryptoTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type EcdhWebcryptoTestGroupType `json:"type"`
}

func (j *EcdhWebcryptoTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhWebcryptoTestGroupType string

const EcdhWebcryptoTestGroupTypeEcdhWebcryptoTest EcdhWebcryptoTestGroupType = "EcdhWebcryptoTest"
func (j *EcdhWebcryptoTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhWebcryptoTestSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema EcdhWebcryptoTestSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []EcdhWebcryptoTestGroup `json:"testGroups"`
}

func (j *EcdhWebcryptoTestSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhWebcryptoTestSchemaV1JsonSchema string

const EcdhWebcryptoTestSchemaV1JsonSchemaEcdhWebcryptoTestSchemaV1Json EcdhWebcryptoTestSchemaV1JsonSchema = "ecdh_webcrypto_test_schema_v1.json"
func (j *EcdhWebcryptoTestSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhWebcryptoTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// Private key in webcrypto format
	Private EcdhWebcryptoTestVectorPrivate `json:"private"`

	// Public key in webcrypto format
	Public EcdhWebcryptoTestVectorPublic `json:"public"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// The shared secret key
	Shared string `json:"shared"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *EcdhWebcryptoTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdhWebcryptoTestVectorPrivate map[string]interface{}
    Private key in webcrypto format

type EcdhWebcryptoTestVectorPublic map[string]interface{}
    Public key in webcrypto format

type EcdsaP1363TestGroup struct {
	// unencoded EC public key
	PublicKey EcPublicKey `json:"publicKey"`

	// DER encoded public key
	PublicKeyDer string `json:"publicKeyDer"`

	// PublicKeyJwk corresponds to the JSON schema field "publicKeyJwk".
	PublicKeyJwk *JsonWebKey `json:"publicKeyJwk,omitempty,omitzero"`

	// Pem encoded public key
	PublicKeyPem string `json:"publicKeyPem"`

	// the hash function used for ECDSA
	Sha string `json:"sha"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []SignatureTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type EcdsaP1363TestGroupType `json:"type"`
}

func (j *EcdsaP1363TestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdsaP1363TestGroupType string

const EcdsaP1363TestGroupTypeEcdsaP1363Verify EcdsaP1363TestGroupType = "EcdsaP1363Verify"
func (j *EcdsaP1363TestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdsaP1363VerifySchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema EcdsaP1363VerifySchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []EcdsaP1363TestGroup `json:"testGroups"`
}

func (j *EcdsaP1363VerifySchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdsaP1363VerifySchemaV1JsonSchema string

const EcdsaP1363VerifySchemaV1JsonSchemaEcdsaP1363VerifySchemaV1Json EcdsaP1363VerifySchemaV1JsonSchema = "ecdsa_p1363_verify_schema_v1.json"
func (j *EcdsaP1363VerifySchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdsaTestGroup struct {
	// unencoded EC public key
	PublicKey EcPublicKey `json:"publicKey"`

	// DER encoded public key
	PublicKeyDer string `json:"publicKeyDer"`

	// Pem encoded public key
	PublicKeyPem string `json:"publicKeyPem"`

	// the hash function used for ECDSA
	Sha string `json:"sha"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []AsnSignatureTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type EcdsaTestGroupType `json:"type"`
}

func (j *EcdsaTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdsaTestGroupType string

const EcdsaTestGroupTypeEcdsaVerify EcdsaTestGroupType = "EcdsaVerify"
func (j *EcdsaTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdsaVerifySchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema EcdsaVerifySchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []EcdsaTestGroup `json:"testGroups"`
}

func (j *EcdsaVerifySchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EcdsaVerifySchemaV1JsonSchema string

const EcdsaVerifySchemaV1JsonSchemaEcdsaVerifySchemaV1Json EcdsaVerifySchemaV1JsonSchema = "ecdsa_verify_schema_v1.json"
func (j *EcdsaVerifySchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EddsaTestGroup struct {
	// PublicKey corresponds to the JSON schema field "publicKey".
	PublicKey PublicKey `json:"publicKey"`

	// Asn encoded public key
	PublicKeyDer string `json:"publicKeyDer"`

	// the public key in webcrypto format
	PublicKeyJwk *JsonWebKey `json:"publicKeyJwk,omitempty,omitzero"`

	// PEM encoded public key
	PublicKeyPem string `json:"publicKeyPem"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []SignatureTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type EddsaTestGroupType `json:"type"`
}

func (j *EddsaTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EddsaTestGroupType string

const EddsaTestGroupTypeEddsaVerify EddsaTestGroupType = "EddsaVerify"
func (j *EddsaTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EddsaVerifySchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema EddsaVerifySchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []EddsaTestGroup `json:"testGroups"`
}

func (j *EddsaVerifySchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type EddsaVerifySchemaV1JsonSchema string

const EddsaVerifySchemaV1JsonSchemaEddsaVerifySchemaV1Json EddsaVerifySchemaV1JsonSchema = "eddsa_verify_schema_v1.json"
func (j *EddsaVerifySchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type HkdfTestGroup struct {
	// the size of the ikm in bits
	KeySize int `json:"keySize"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []HkdfTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type HkdfTestGroupType `json:"type"`
}

func (j *HkdfTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type HkdfTestGroupType string

const HkdfTestGroupTypeHkdfTest HkdfTestGroupType = "HkdfTest"
func (j *HkdfTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type HkdfTestSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema HkdfTestSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []HkdfTestGroup `json:"testGroups"`
}

func (j *HkdfTestSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type HkdfTestSchemaV1JsonSchema string

const HkdfTestSchemaV1JsonSchemaHkdfTestSchemaV1Json HkdfTestSchemaV1JsonSchema = "hkdf_test_schema_v1.json"
func (j *HkdfTestSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type HkdfTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// the key (input key material)
	Ikm string `json:"ikm"`

	// additional information used in the key derivation
	Info string `json:"info"`

	// the generated bytes (output key material)
	Okm string `json:"okm"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// the salt for the key derivation
	Salt string `json:"salt"`

	// the size of the output in bytes
	Size int `json:"size"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *HkdfTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type IndCpaTestGroup struct {
	// the IV size in bits
	IvSize int `json:"ivSize"`

	// the keySize in bits
	KeySize int `json:"keySize"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []IndCpaTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type IndCpaTestGroupType `json:"type"`
}

func (j *IndCpaTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type IndCpaTestGroupType string

const IndCpaTestGroupTypeIndCpaTest IndCpaTestGroupType = "IndCpaTest"
func (j *IndCpaTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type IndCpaTestSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema IndCpaTestSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []IndCpaTestGroup `json:"testGroups"`
}

func (j *IndCpaTestSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type IndCpaTestSchemaV1JsonSchema string

const IndCpaTestSchemaV1JsonSchemaIndCpaTestSchemaV1Json IndCpaTestSchemaV1JsonSchema = "ind_cpa_test_schema_v1.json"
func (j *IndCpaTestSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type IndCpaTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// the raw ciphertext (without IV)
	Ct string `json:"ct"`

	// A list of flags
	Flags []string `json:"flags"`

	// the initialization vector
	Iv string `json:"iv"`

	// the key
	Key string `json:"key"`

	// the plaintext
	Msg string `json:"msg"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *IndCpaTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebCryptoSchemaV1Json struct {
	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema JsonWebCryptoSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []JsonWebCryptoTestGroup `json:"testGroups"`
}

func (j *JsonWebCryptoSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebCryptoSchemaV1JsonSchema string

const JsonWebCryptoSchemaV1JsonSchemaJsonWebCryptoSchemaV1Json JsonWebCryptoSchemaV1JsonSchema = "json_web_crypto_schema_v1.json"
func (j *JsonWebCryptoSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebCryptoTestGroup struct {
	// a description of what these tests have in common
	Comment *string `json:"comment,omitempty,omitzero"`

	// the private or secret key in webcrypto format
	Private JsonWebKeyOrKeyset `json:"private,omitempty,omitzero"`

	// [optional] the public key in webcrypto format
	Public JsonWebKeyOrKeyset `json:"public,omitempty,omitzero"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []JsonWebCryptoTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type *JsonWebCryptoTestGroupType `json:"type,omitempty,omitzero"`
}

func (j *JsonWebCryptoTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebCryptoTestGroupType string

const JsonWebCryptoTestGroupTypeJsonWebCrypto JsonWebCryptoTestGroupType = "JsonWebCrypto"
func (j *JsonWebCryptoTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebCryptoTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// The JSON Web Encryption
	Jwe interface{} `json:"jwe,omitempty,omitzero"`

	// The JSON Web Signature
	Jws interface{} `json:"jws,omitempty,omitzero"`

	// [optional] Plaintext
	Pt *string `json:"pt,omitempty,omitzero"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *JsonWebCryptoTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebEncryptionSchemaV1Json struct {
	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema JsonWebEncryptionSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []JsonWebEncryptionTestGroup `json:"testGroups"`
}

func (j *JsonWebEncryptionSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebEncryptionSchemaV1JsonSchema string

const JsonWebEncryptionSchemaV1JsonSchemaJsonWebEncryptionSchemaV1Json JsonWebEncryptionSchemaV1JsonSchema = "json_web_encryption_schema_v1.json"
func (j *JsonWebEncryptionSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebEncryptionTestGroup struct {
	// a description of what these tests have in common
	Comment *string `json:"comment,omitempty,omitzero"`

	// the private key
	Private *JsonWebKey `json:"private,omitempty,omitzero"`

	// the [optional] public key
	Public *JsonWebKey `json:"public,omitempty,omitzero"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []JsonWebEncryptionTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type *JsonWebEncryptionTestGroupType `json:"type,omitempty,omitzero"`
}

func (j *JsonWebEncryptionTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebEncryptionTestGroupType string

const JsonWebEncryptionTestGroupTypeJsonWebEncryption JsonWebEncryptionTestGroupType = "JsonWebEncryption"
func (j *JsonWebEncryptionTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebEncryptionTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// the content encryption algorithm
	Enc string `json:"enc"`

	// A list of flags
	Flags []string `json:"flags"`

	// The JSON Web Encryption in compact form
	Jwe string `json:"jwe"`

	// [optional] Plaintext
	Pt *string `json:"pt,omitempty,omitzero"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *JsonWebEncryptionTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebKey struct {
	// the encryption/signing algorithm to use
	Alg *string `json:"alg,omitempty,omitzero"`

	// which defined curve to use
	Crv *JsonWebKeyCrv `json:"crv,omitempty,omitzero"`

	// the private key value of an EC key or private exponent for RSA
	D *string `json:"d,omitempty,omitzero"`

	// the first factor Chinese Remainder Theorem exponent of an RSA key
	Dp *string `json:"dp,omitempty,omitzero"`

	// the second factor Chinese Remainder Theorem exponent of an RSA key
	Dq *string `json:"dq,omitempty,omitzero"`

	// the public exponent of an RSA key
	E *string `json:"e,omitempty,omitzero"`

	// the secret key value of an oct key
	K *string `json:"k,omitempty,omitzero"`

	// an alternative to use
	KeyOps []string `json:"key_ops,omitempty,omitzero"`

	// the ID of the key entry
	Kid *string `json:"kid,omitempty,omitzero"`

	// the family of algorithms the key belongs to
	Kty *JsonWebKeyKty `json:"kty,omitempty,omitzero"`

	// the public modulus of an RSA key
	N *string `json:"n,omitempty,omitzero"`

	// the first prime factgor of an RSA key
	P *string `json:"p,omitempty,omitzero"`

	// the second prime factor of an RSA key
	Q *string `json:"q,omitempty,omitzero"`

	// the first factor Chinese Remainder Theorem coefficient of an RSA key
	Qi *string `json:"qi,omitempty,omitzero"`

	// what type of crypto operation to perform
	Use *JsonWebKeyUse `json:"use,omitempty,omitzero"`

	// the x-coordinate of an EC key point
	X *string `json:"x,omitempty,omitzero"`

	// the y-coordinate of an EC key point
	Y *string `json:"y,omitempty,omitzero"`
}
    see https://tools.ietf.org/html/rfc7517#section-4 and
    https://tools.ietf.org/html/rfc7518#section-6

type JsonWebKeyCrv string

const JsonWebKeyCrvEd25519 JsonWebKeyCrv = "Ed25519"
const JsonWebKeyCrvEd448 JsonWebKeyCrv = "Ed448"
const JsonWebKeyCrvP256 JsonWebKeyCrv = "P-256"
const JsonWebKeyCrvP256K JsonWebKeyCrv = "P-256K"
const JsonWebKeyCrvP384 JsonWebKeyCrv = "P-384"
const JsonWebKeyCrvP521 JsonWebKeyCrv = "P-521"
const JsonWebKeyCrvSecp256K1 JsonWebKeyCrv = "secp256k1"
const JsonWebKeyCrvX25519 JsonWebKeyCrv = "X25519"
const JsonWebKeyCrvX448 JsonWebKeyCrv = "X448"
func (j *JsonWebKeyCrv) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebKeyKty string

const JsonWebKeyKtyBlank JsonWebKeyKty = ""
const JsonWebKeyKtyEC JsonWebKeyKty = "EC"
const JsonWebKeyKtyOKP JsonWebKeyKty = "OKP"
const JsonWebKeyKtyOct JsonWebKeyKty = "oct"
const JsonWebKeyKtyRSA JsonWebKeyKty = "RSA"
func (j *JsonWebKeyKty) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebKeyOrKeyset interface{}

type JsonWebKeySchemaV1Json struct {
	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema JsonWebKeySchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []JsonWebKeyTestGroup `json:"testGroups"`
}

func (j *JsonWebKeySchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebKeySchemaV1JsonSchema string

const JsonWebKeySchemaV1JsonSchemaJsonWebKeySchemaV1Json JsonWebKeySchemaV1JsonSchema = "json_web_key_schema_v1.json"
func (j *JsonWebKeySchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebKeyTestGroup struct {
	// a description of what these tests have in common
	Comment *string `json:"comment,omitempty,omitzero"`

	// the private or secret keyset in webcrypto format
	Private *JsonWebKeyset `json:"private,omitempty,omitzero"`

	// the public keyset in webcrypto format
	Public *JsonWebKeyset `json:"public,omitempty,omitzero"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []JsonWebKeyTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type *JsonWebKeyTestGroupType `json:"type,omitempty,omitzero"`
}

func (j *JsonWebKeyTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebKeyTestGroupType string

const JsonWebKeyTestGroupTypeJsonWebKey JsonWebKeyTestGroupType = "JsonWebKey"
func (j *JsonWebKeyTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebKeyTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// The JSON Web Signature in compact form
	Jws string `json:"jws"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *JsonWebKeyTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebKeyUse string

const JsonWebKeyUseEnc JsonWebKeyUse = "enc"
const JsonWebKeyUseSig JsonWebKeyUse = "sig"
func (j *JsonWebKeyUse) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebKeyset struct {
	// Keys corresponds to the JSON schema field "keys".
	Keys []JsonWebKey `json:"keys,omitempty,omitzero"`
}
    see https://tools.ietf.org/html/rfc7517#section-5

type JsonWebSignatureSchemaV1Json struct {
	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema JsonWebSignatureSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []JsonWebSignatureTestGroup `json:"testGroups"`
}

func (j *JsonWebSignatureSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebSignatureSchemaV1JsonSchema string

const JsonWebSignatureSchemaV1JsonSchemaJsonWebSignatureSchemaV1Json JsonWebSignatureSchemaV1JsonSchema = "json_web_signature_schema_v1.json"
func (j *JsonWebSignatureSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebSignatureTestGroup struct {
	// a description of what these tests have in common
	Comment *string `json:"comment,omitempty,omitzero"`

	// the private or secret key in webcrypto format
	Private *JsonWebKey `json:"private,omitempty,omitzero"`

	// [optional] the public key in webcrypto format
	Public *JsonWebKey `json:"public,omitempty,omitzero"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []JsonWebSignatureTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type *JsonWebSignatureTestGroupType `json:"type,omitempty,omitzero"`
}

func (j *JsonWebSignatureTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebSignatureTestGroupType string

const JsonWebSignatureTestGroupTypeJsonWebSignature JsonWebSignatureTestGroupType = "JsonWebSignature"
func (j *JsonWebSignatureTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type JsonWebSignatureTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// The JSON Web Signature in compact form
	Jws string `json:"jws"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *JsonWebSignatureTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type KeywrapTestGroup struct {
	// the keySize in bits
	KeySize int `json:"keySize"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []KeywrapTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type KeywrapTestGroupType `json:"type"`
}

func (j *KeywrapTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type KeywrapTestGroupType string

const KeywrapTestGroupTypeKeywrapTest KeywrapTestGroupType = "KeywrapTest"
func (j *KeywrapTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type KeywrapTestSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema KeywrapTestSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []KeywrapTestGroup `json:"testGroups"`
}

func (j *KeywrapTestSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type KeywrapTestSchemaV1JsonSchema string

const KeywrapTestSchemaV1JsonSchemaKeywrapTestSchemaV1Json KeywrapTestSchemaV1JsonSchema = "keywrap_test_schema_v1.json"
func (j *KeywrapTestSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type KeywrapTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// the wrapped key
	Ct string `json:"ct"`

	// A list of flags
	Flags []string `json:"flags"`

	// the wrapping key
	Key string `json:"key"`

	// the key bytes to wrap
	Msg string `json:"msg"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *KeywrapTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MLKEMDecapsTestGroup struct {
	// ParameterSet corresponds to the JSON schema field "parameterSet".
	ParameterSet MLKEMDecapsTestGroupParameterSet `json:"parameterSet"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []MLKEMDecapsTestGroupTestsElem `json:"tests"`

	// Test type for decapsulation validation
	Type MLKEMDecapsTestGroupType `json:"type"`
}
    A test for ML-KEM decapsulation validation

func (j *MLKEMDecapsTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MLKEMDecapsTestGroupParameterSet string

const MLKEMDecapsTestGroupParameterSetMLKEM1024 MLKEMDecapsTestGroupParameterSet = "ML-KEM-1024"
const MLKEMDecapsTestGroupParameterSetMLKEM512 MLKEMDecapsTestGroupParameterSet = "ML-KEM-512"
const MLKEMDecapsTestGroupParameterSetMLKEM768 MLKEMDecapsTestGroupParameterSet = "ML-KEM-768"
func (j *MLKEMDecapsTestGroupParameterSet) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MLKEMDecapsTestGroupTestsElem struct {
	// If present, the shared key the implementation MUST return on a successful
	// Decapsulate call.
	K *string `json:"K,omitempty,omitzero"`

	// An input ciphertext
	C string `json:"c"`

	// A brief description of the test case
	Comment *string `json:"comment,omitempty,omitzero"`

	// The full decapsulation key
	Dk string `json:"dk"`

	// The encapsulation key bytes of dk.
	Ek string `json:"ek"`

	// A list of flags
	Flags []string `json:"flags"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *MLKEMDecapsTestGroupTestsElem) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MLKEMDecapsTestGroupType string

const MLKEMDecapsTestGroupTypeMLKEMDecapsValidationTest MLKEMDecapsTestGroupType = "MLKEMDecapsValidationTest"
func (j *MLKEMDecapsTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MLKEMEncapsTestGroup struct {
	// ParameterSet corresponds to the JSON schema field "parameterSet".
	ParameterSet MLKEMEncapsTestGroupParameterSet `json:"parameterSet"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []MLKEMEncapsTestGroupTestsElem `json:"tests"`

	// A legacy field, test files contain only one type per file
	Type *MLKEMEncapsTestGroupType `json:"type,omitempty,omitzero"`
}
    A test for Encaps

func (j *MLKEMEncapsTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MLKEMEncapsTestGroupParameterSet string

const MLKEMEncapsTestGroupParameterSetMLKEM1024 MLKEMEncapsTestGroupParameterSet = "ML-KEM-1024"
const MLKEMEncapsTestGroupParameterSetMLKEM512 MLKEMEncapsTestGroupParameterSet = "ML-KEM-512"
const MLKEMEncapsTestGroupParameterSetMLKEM768 MLKEMEncapsTestGroupParameterSet = "ML-KEM-768"
func (j *MLKEMEncapsTestGroupParameterSet) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MLKEMEncapsTestGroupTestsElem struct {
	// The output shared secret
	K string `json:"K"`

	// The output ciphertext
	C string `json:"c"`

	// A brief description of the test case
	Comment *string `json:"comment,omitempty,omitzero"`

	// The encapsulation key
	Ek string `json:"ek"`

	// A list of flags
	Flags []string `json:"flags"`

	// The ML-KEM.Encaps_internal m input, a 32-byte value
	M string `json:"m"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *MLKEMEncapsTestGroupTestsElem) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MLKEMEncapsTestGroupType string

const MLKEMEncapsTestGroupTypeMLKEMEncapsTest MLKEMEncapsTestGroupType = "MLKEMEncapsTest"
func (j *MLKEMEncapsTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MLKEMKeyGenTestGroup struct {
	// ParameterSet corresponds to the JSON schema field "parameterSet".
	ParameterSet MLKEMKeyGenTestGroupParameterSet `json:"parameterSet"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []MLKEMKeyGenTestGroupTestsElem `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type MLKEMKeyGenTestGroupType `json:"type"`
}
    A test for KeyGen using seed format

func (j *MLKEMKeyGenTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MLKEMKeyGenTestGroupParameterSet string

const MLKEMKeyGenTestGroupParameterSetMLKEM1024 MLKEMKeyGenTestGroupParameterSet = "ML-KEM-1024"
const MLKEMKeyGenTestGroupParameterSetMLKEM512 MLKEMKeyGenTestGroupParameterSet = "ML-KEM-512"
const MLKEMKeyGenTestGroupParameterSetMLKEM768 MLKEMKeyGenTestGroupParameterSet = "ML-KEM-768"
func (j *MLKEMKeyGenTestGroupParameterSet) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MLKEMKeyGenTestGroupTestsElem struct {
	// A brief description of the test case
	Comment *string `json:"comment,omitempty,omitzero"`

	// The expected expanded decapsulation key
	Dk string `json:"dk"`

	// The expected encapsulation key
	Ek string `json:"ek"`

	// A list of flags
	Flags []string `json:"flags,omitempty,omitzero"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// The d || z seed for key generation
	Seed string `json:"seed"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *MLKEMKeyGenTestGroupTestsElem) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MLKEMKeyGenTestGroupType string

const MLKEMKeyGenTestGroupTypeMLKEMKeyGen MLKEMKeyGenTestGroupType = "MLKEMKeyGen"
func (j *MLKEMKeyGenTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MLKEMTestGroup struct {
	// ParameterSet corresponds to the JSON schema field "parameterSet".
	ParameterSet MLKEMTestGroupParameterSet `json:"parameterSet"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []MLKEMTestGroupTestsElem `json:"tests"`

	// A legacy field, test files contain only one type per file
	Type MLKEMTestGroupType `json:"type"`
}
    A test for KeyGen and/or Decaps

func (j *MLKEMTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MLKEMTestGroupParameterSet string

const MLKEMTestGroupParameterSetMLKEM1024 MLKEMTestGroupParameterSet = "ML-KEM-1024"
const MLKEMTestGroupParameterSetMLKEM512 MLKEMTestGroupParameterSet = "ML-KEM-512"
const MLKEMTestGroupParameterSetMLKEM768 MLKEMTestGroupParameterSet = "ML-KEM-768"
func (j *MLKEMTestGroupParameterSet) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MLKEMTestGroupTestsElem struct {
	// The output shared secret
	K string `json:"K"`

	// An input ciphertext
	C string `json:"c"`

	// A brief description of the test case
	Comment *string `json:"comment,omitempty,omitzero"`

	// The encapsulation key derived from the seed
	Ek *string `json:"ek,omitempty,omitzero"`

	// A list of flags
	Flags []string `json:"flags"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// The d || z seed
	Seed string `json:"seed"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *MLKEMTestGroupTestsElem) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MLKEMTestGroupType string

const MLKEMTestGroupTypeMLKEMTest MLKEMTestGroupType = "MLKEMTest"
func (j *MLKEMTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MacTestGroup struct {
	// the keySize in bits
	KeySize int `json:"keySize"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// the expected size of the tag in bits
	TagSize int `json:"tagSize"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []MacTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type MacTestGroupType `json:"type"`
}

func (j *MacTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MacTestGroupType string

const MacTestGroupTypeMacTest MacTestGroupType = "MacTest"
func (j *MacTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MacTestSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema MacTestSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []MacTestGroup `json:"testGroups"`
}

func (j *MacTestSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MacTestSchemaV1JsonSchema string

const MacTestSchemaV1JsonSchemaMacTestSchemaV1Json MacTestSchemaV1JsonSchema = "mac_test_schema_v1.json"
func (j *MacTestSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MacTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// the key
	Key string `json:"key"`

	// the plaintext
	Msg string `json:"msg"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// the authentication tag
	Tag string `json:"tag"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *MacTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MacWithIvTestGroup struct {
	// the IV size in bits
	IvSize int `json:"ivSize"`

	// the key size in bits
	KeySize int `json:"keySize"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// the expected size of the tag in bits
	TagSize int `json:"tagSize"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []MacWithIvTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type MacWithIvTestGroupType `json:"type"`
}

func (j *MacWithIvTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MacWithIvTestGroupType string

const MacWithIvTestGroupTypeMacWithIvTest MacWithIvTestGroupType = "MacWithIvTest"
func (j *MacWithIvTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MacWithIvTestSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema MacWithIvTestSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []MacWithIvTestGroup `json:"testGroups"`
}

func (j *MacWithIvTestSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MacWithIvTestSchemaV1JsonSchema string

const MacWithIvTestSchemaV1JsonSchemaMacWithIvTestSchemaV1Json MacWithIvTestSchemaV1JsonSchema = "mac_with_iv_test_schema_v1.json"
func (j *MacWithIvTestSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MacWithIvTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// the initialisation vector
	Iv string `json:"iv"`

	// the key
	Key string `json:"key"`

	// the plaintext
	Msg string `json:"msg"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// the authentication tag
	Tag string `json:"tag"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *MacWithIvTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlDsaSignNoSeedTestGroup struct {
	// Encoded ML-DSA private key
	PrivateKey string `json:"privateKey"`

	// Encoded ML-DSA public key derived from the private key, or null if the private
	// key is invalid
	PublicKey interface{} `json:"publicKey"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []MlDsaSignTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type MlDsaSignNoSeedTestGroupType `json:"type"`
}

func (j *MlDsaSignNoSeedTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlDsaSignNoSeedTestGroupType string

const MlDsaSignNoSeedTestGroupTypeMlDsaSign MlDsaSignNoSeedTestGroupType = "MlDsaSign"
func (j *MlDsaSignNoSeedTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlDsaSignTestGroup struct {
	// Private key as a DER-encoded PrivateKeyInfo, using the seed form
	PrivateKeyPkcs8 *string `json:"privateKeyPkcs8,omitempty,omitzero"`

	// 32-byte seed that generated the private key
	PrivateSeed string `json:"privateSeed"`

	// Encoded ML-DSA public key derived from the private seed, or null if the private
	// seed is invalid
	PublicKey interface{} `json:"publicKey"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []MlDsaSignTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type MlDsaSignTestGroupType `json:"type"`
}

func (j *MlDsaSignTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlDsaSignTestGroupType string

const MlDsaSignTestGroupTypeMlDsaSign MlDsaSignTestGroupType = "MlDsaSign"
func (j *MlDsaSignTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlDsaSignTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// [optional] The additional context string (if omitted, the context input is
	// empty)
	Ctx *string `json:"ctx,omitempty,omitzero"`

	// A list of flags
	Flags []string `json:"flags"`

	// [optional] The message to sign (if omitted, mu is provided to use with
	// Sign_internal)
	Msg *string `json:"msg,omitempty,omitzero"`

	// [optional] The 64-byte μ value (omitted in case of expected failure)
	Mu *string `json:"mu,omitempty,omitzero"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// [optional] The 32-byte random value (if omitted, implicitly all zeroes for
	// deterministic signing)
	Rnd *string `json:"rnd,omitempty,omitzero"`

	// The encoded signature (empty in case of expected failure)
	Sig string `json:"sig"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *MlDsaSignTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlDsaVerifyTestGroup struct {
	// Encoded ML-DSA public key
	PublicKey string `json:"publicKey"`

	// Public key as a DER-encoded SubjectPublicKeyInfo
	PublicKeyDer string `json:"publicKeyDer"`

	// Source corresponds to the JSON schema field "source".
	Source *Source `json:"source,omitempty,omitzero"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []MlDsaVerifyTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type MlDsaVerifyTestGroupType `json:"type"`
}

func (j *MlDsaVerifyTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlDsaVerifyTestGroupType string

const MlDsaVerifyTestGroupTypeMlDsaVerify MlDsaVerifyTestGroupType = "MlDsaVerify"
func (j *MlDsaVerifyTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlDsaVerifyTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// [optional] The additional context string (empty if not provided)
	Ctx *string `json:"ctx,omitempty,omitzero"`

	// A list of flags
	Flags []string `json:"flags"`

	// The message to verify
	Msg string `json:"msg"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// The encoded signature
	Sig string `json:"sig"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *MlDsaVerifyTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MldsaSignNoseedSchemaJson struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema MldsaSignNoseedSchemaJsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []MlDsaSignNoSeedTestGroup `json:"testGroups"`
}

func (j *MldsaSignNoseedSchemaJson) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MldsaSignNoseedSchemaJsonSchema string

const MldsaSignNoseedSchemaJsonSchemaMldsaSignNoseedSchemaJson MldsaSignNoseedSchemaJsonSchema = "mldsa_sign_noseed_schema.json"
func (j *MldsaSignNoseedSchemaJsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MldsaSignSeedSchemaJson struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema MldsaSignSeedSchemaJsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []MlDsaSignTestGroup `json:"testGroups"`
}

func (j *MldsaSignSeedSchemaJson) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MldsaSignSeedSchemaJsonSchema string

const MldsaSignSeedSchemaJsonSchemaMldsaSignSeedSchemaJson MldsaSignSeedSchemaJsonSchema = "mldsa_sign_seed_schema.json"
func (j *MldsaSignSeedSchemaJsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MldsaVerifySchemaJson struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema MldsaVerifySchemaJsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []MlDsaVerifyTestGroup `json:"testGroups"`
}

func (j *MldsaVerifySchemaJson) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MldsaVerifySchemaJsonSchema string

const MldsaVerifySchemaJsonSchemaMldsaVerifySchemaJson MldsaVerifySchemaJsonSchema = "mldsa_verify_schema.json"
func (j *MldsaVerifySchemaJsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlkemEncapsTestSchemaJson struct {
	// Algorithm corresponds to the JSON schema field "algorithm".
	Algorithm MlkemEncapsTestSchemaJsonAlgorithm `json:"algorithm"`

	// additional documentation
	Header []string `json:"header,omitempty,omitzero"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes,omitempty,omitzero"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema MlkemEncapsTestSchemaJsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []MLKEMEncapsTestGroup `json:"testGroups"`
}

func (j *MlkemEncapsTestSchemaJson) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlkemEncapsTestSchemaJsonAlgorithm string

const MlkemEncapsTestSchemaJsonAlgorithmMLKEM MlkemEncapsTestSchemaJsonAlgorithm = "ML-KEM"
func (j *MlkemEncapsTestSchemaJsonAlgorithm) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlkemEncapsTestSchemaJsonSchema string

const MlkemEncapsTestSchemaJsonSchemaMlkemEncapsTestSchemaJson MlkemEncapsTestSchemaJsonSchema = "mlkem_encaps_test_schema.json"
func (j *MlkemEncapsTestSchemaJsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlkemKeygenSeedTestSchemaJson struct {
	// Algorithm corresponds to the JSON schema field "algorithm".
	Algorithm MlkemKeygenSeedTestSchemaJsonAlgorithm `json:"algorithm"`

	// additional documentation
	Header []string `json:"header,omitempty,omitzero"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes,omitempty,omitzero"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema MlkemKeygenSeedTestSchemaJsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []MLKEMKeyGenTestGroup `json:"testGroups"`
}

func (j *MlkemKeygenSeedTestSchemaJson) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlkemKeygenSeedTestSchemaJsonAlgorithm string

const MlkemKeygenSeedTestSchemaJsonAlgorithmMLKEM MlkemKeygenSeedTestSchemaJsonAlgorithm = "ML-KEM"
func (j *MlkemKeygenSeedTestSchemaJsonAlgorithm) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlkemKeygenSeedTestSchemaJsonSchema string

const MlkemKeygenSeedTestSchemaJsonSchemaMlkemKeygenSeedTestSchemaJson MlkemKeygenSeedTestSchemaJsonSchema = "mlkem_keygen_seed_test_schema.json"
func (j *MlkemKeygenSeedTestSchemaJsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlkemSemiExpandedDecapsTestSchemaJson struct {
	// Algorithm corresponds to the JSON schema field "algorithm".
	Algorithm MlkemSemiExpandedDecapsTestSchemaJsonAlgorithm `json:"algorithm"`

	// additional documentation
	Header []string `json:"header,omitempty,omitzero"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes,omitempty,omitzero"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema MlkemSemiExpandedDecapsTestSchemaJsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []MLKEMDecapsTestGroup `json:"testGroups"`
}

func (j *MlkemSemiExpandedDecapsTestSchemaJson) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlkemSemiExpandedDecapsTestSchemaJsonAlgorithm string

const MlkemSemiExpandedDecapsTestSchemaJsonAlgorithmMLKEM MlkemSemiExpandedDecapsTestSchemaJsonAlgorithm = "ML-KEM"
func (j *MlkemSemiExpandedDecapsTestSchemaJsonAlgorithm) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlkemSemiExpandedDecapsTestSchemaJsonSchema string

const MlkemSemiExpandedDecapsTestSchemaJsonSchemaMlkemSemiExpandedDecapsTestSchemaJson MlkemSemiExpandedDecapsTestSchemaJsonSchema = "mlkem_semi_expanded_decaps_test_schema.json"
func (j *MlkemSemiExpandedDecapsTestSchemaJsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlkemTestSchemaJson struct {
	// Algorithm corresponds to the JSON schema field "algorithm".
	Algorithm MlkemTestSchemaJsonAlgorithm `json:"algorithm"`

	// additional documentation
	Header []string `json:"header,omitempty,omitzero"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes,omitempty,omitzero"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema MlkemTestSchemaJsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []MLKEMTestGroup `json:"testGroups"`
}

func (j *MlkemTestSchemaJson) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlkemTestSchemaJsonAlgorithm string

const MlkemTestSchemaJsonAlgorithmMLKEM MlkemTestSchemaJsonAlgorithm = "ML-KEM"
func (j *MlkemTestSchemaJsonAlgorithm) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type MlkemTestSchemaJsonSchema string

const MlkemTestSchemaJsonSchemaMlkemTestSchemaJson MlkemTestSchemaJsonSchema = "mlkem_test_schema.json"
func (j *MlkemTestSchemaJsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type NoteEntry struct {
	// The type of the bug tested for
	BugType string `json:"bugType"`

	// A list of potentially related CVEs
	Cves []string `json:"cves,omitempty,omitzero"`

	// A description of the flag
	Description *string `json:"description,omitempty,omitzero"`

	// The expected effect of failing the test vector
	Effect *string `json:"effect,omitempty,omitzero"`

	// A list of potentially related references
	Links []string `json:"links,omitempty,omitzero"`
}

func (j *NoteEntry) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type Notes map[string]NoteEntry

type PbkdfTestGroup struct {
	// Source corresponds to the JSON schema field "source".
	Source *Source `json:"source,omitempty,omitzero"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []PbkdfTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type PbkdfTestGroupType `json:"type"`
}

func (j *PbkdfTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type PbkdfTestGroupType string

const PbkdfTestGroupTypePbkdfTest PbkdfTestGroupType = "PbkdfTest"
func (j *PbkdfTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type PbkdfTestSchemaJson struct {
	// Algorithm corresponds to the JSON schema field "algorithm".
	Algorithm PbkdfTestSchemaJsonAlgorithm `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// Additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// The number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema PbkdfTestSchemaJsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []PbkdfTestGroup `json:"testGroups"`
}

func (j *PbkdfTestSchemaJson) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type PbkdfTestSchemaJsonAlgorithm string

const PbkdfTestSchemaJsonAlgorithmPBKDF2HMACSHA1 PbkdfTestSchemaJsonAlgorithm = "PBKDF2-HMACSHA1"
const PbkdfTestSchemaJsonAlgorithmPBKDF2HMACSHA224 PbkdfTestSchemaJsonAlgorithm = "PBKDF2-HMACSHA224"
const PbkdfTestSchemaJsonAlgorithmPBKDF2HMACSHA256 PbkdfTestSchemaJsonAlgorithm = "PBKDF2-HMACSHA256"
const PbkdfTestSchemaJsonAlgorithmPBKDF2HMACSHA384 PbkdfTestSchemaJsonAlgorithm = "PBKDF2-HMACSHA384"
const PbkdfTestSchemaJsonAlgorithmPBKDF2HMACSHA512 PbkdfTestSchemaJsonAlgorithm = "PBKDF2-HMACSHA512"
func (j *PbkdfTestSchemaJsonAlgorithm) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type PbkdfTestSchemaJsonSchema string

const PbkdfTestSchemaJsonSchemaPbkdfTestSchemaJson PbkdfTestSchemaJsonSchema = "pbkdf_test_schema.json"
func (j *PbkdfTestSchemaJsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type PbkdfTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// The derived key
	Dk string `json:"dk"`

	// The length of the derived key in bytes
	DkLen int `json:"dkLen"`

	// A list of flags
	Flags []string `json:"flags"`

	// The number of iterations for the key derivation
	IterationCount int `json:"iterationCount"`

	// The password as a hex-encoded byte string
	Password string `json:"password"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// The salt for the key derivation
	Salt string `json:"salt"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *PbkdfTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type PrimalityTestGroup struct {
	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []PrimalityTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type PrimalityTestGroupType `json:"type"`
}

func (j *PrimalityTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type PrimalityTestGroupType string

const PrimalityTestGroupTypePrimalityTest PrimalityTestGroupType = "PrimalityTest"
func (j *PrimalityTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type PrimalityTestSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema PrimalityTestSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []PrimalityTestGroup `json:"testGroups"`
}

func (j *PrimalityTestSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type PrimalityTestSchemaV1JsonSchema string

const PrimalityTestSchemaV1JsonSchemaPrimalityTestSchemaV1Json PrimalityTestSchemaV1JsonSchema = "primality_test_schema_v1.json"
func (j *PrimalityTestSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type PrimalityTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// Identifier of the test case
	TcId int `json:"tcId"`

	// the integer to test
	Value string `json:"value"`
}

func (j *PrimalityTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type PrivateKey struct {
	// Coefficient corresponds to the JSON schema field "coefficient".
	Coefficient *string `json:"coefficient,omitempty,omitzero"`

	// Exponent1 corresponds to the JSON schema field "exponent1".
	Exponent1 *string `json:"exponent1,omitempty,omitzero"`

	// Exponent2 corresponds to the JSON schema field "exponent2".
	Exponent2 *string `json:"exponent2,omitempty,omitzero"`

	// Modulus corresponds to the JSON schema field "modulus".
	Modulus string `json:"modulus"`

	// OtherPrimeInfos corresponds to the JSON schema field "otherPrimeInfos".
	OtherPrimeInfos [][]string `json:"otherPrimeInfos,omitempty,omitzero"`

	// Prime1 corresponds to the JSON schema field "prime1".
	Prime1 *string `json:"prime1,omitempty,omitzero"`

	// Prime2 corresponds to the JSON schema field "prime2".
	Prime2 *string `json:"prime2,omitempty,omitzero"`

	// PrivateExponent corresponds to the JSON schema field "privateExponent".
	PrivateExponent string `json:"privateExponent"`

	// PublicExponent corresponds to the JSON schema field "publicExponent".
	PublicExponent string `json:"publicExponent"`
}

func (j *PrivateKey) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type PublicKey struct {
	// the name of the curve
	Curve string `json:"curve"`

	// the size of the key in bits
	KeySize int `json:"keySize"`

	// the public key
	Pk string `json:"pk"`

	// Type corresponds to the JSON schema field "type".
	Type PublicKeyType `json:"type"`
}

func (j *PublicKey) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type PublicKeyType string

const PublicKeyTypeECDSAPublicKey PublicKeyType = "ECDSAPublicKey"
const PublicKeyTypeEDDSAPublicKey PublicKeyType = "EDDSAPublicKey"
func (j *PublicKeyType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type Recipient struct {
	// EncryptedKey corresponds to the JSON schema field "encrypted_key".
	EncryptedKey *string `json:"encrypted_key,omitempty,omitzero"`

	// header information that is not integrity protected
	Header RecipientHeader `json:"header,omitempty,omitzero"`
}
    Recipient specific information Section 7.2.1 of RFC 7516

type RecipientHeader map[string]interface{}
    header information that is not integrity protected

type Result string

const ResultAcceptable Result = "acceptable"
const ResultInvalid Result = "invalid"
const ResultValid Result = "valid"
func (j *Result) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsaesOaepDecryptSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema RsaesOaepDecryptSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []RsaesOaepTestGroup `json:"testGroups"`
}

func (j *RsaesOaepDecryptSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsaesOaepDecryptSchemaV1JsonSchema string

const RsaesOaepDecryptSchemaV1JsonSchemaRsaesOaepDecryptSchemaV1Json RsaesOaepDecryptSchemaV1JsonSchema = "rsaes_oaep_decrypt_schema_v1.json"
func (j *RsaesOaepDecryptSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsaesOaepTestGroup struct {
	// the keySize in bits
	KeySize int `json:"keySize"`

	// the message generating function (e.g. MGF1)
	Mgf string `json:"mgf"`

	// The hash function used for the message generating function.
	MgfSha string `json:"mgfSha"`

	// PrivateKey corresponds to the JSON schema field "privateKey".
	PrivateKey PrivateKey `json:"privateKey"`

	// PrivateKeyJwk corresponds to the JSON schema field "privateKeyJwk".
	PrivateKeyJwk *JsonWebKey `json:"privateKeyJwk,omitempty,omitzero"`

	// Pem encoded private key
	PrivateKeyPem string `json:"privateKeyPem"`

	// Pkcs 8 encoded private key.
	PrivateKeyPkcs8 string `json:"privateKeyPkcs8"`

	// The hash function for hashing the label.
	Sha string `json:"sha"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []RsaesOaepTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type RsaesOaepTestGroupType `json:"type"`
}

func (j *RsaesOaepTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsaesOaepTestGroupType string

const RsaesOaepTestGroupTypeRsaesOaepDecrypt RsaesOaepTestGroupType = "RsaesOaepDecrypt"
func (j *RsaesOaepTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsaesOaepTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// An encryption of msg
	Ct string `json:"ct"`

	// A list of flags
	Flags []string `json:"flags"`

	// The label used for the encryption
	Label string `json:"label"`

	// The encrypted message
	Msg string `json:"msg"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *RsaesOaepTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsaesPkcs1DecryptSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema RsaesPkcs1DecryptSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []RsaesPkcs1TestGroup `json:"testGroups"`
}

func (j *RsaesPkcs1DecryptSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsaesPkcs1DecryptSchemaV1JsonSchema string

const RsaesPkcs1DecryptSchemaV1JsonSchemaRsaesPkcs1DecryptSchemaV1Json RsaesPkcs1DecryptSchemaV1JsonSchema = "rsaes_pkcs1_decrypt_schema_v1.json"
func (j *RsaesPkcs1DecryptSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsaesPkcs1TestGroup struct {
	// The size of the key in bits
	KeySize int `json:"keySize"`

	// PrivateKey corresponds to the JSON schema field "privateKey".
	PrivateKey PrivateKey `json:"privateKey"`

	// JWK encoded private key
	PrivateKeyJwk *JsonWebKey `json:"privateKeyJwk,omitempty,omitzero"`

	// Pem encoded private key
	PrivateKeyPem string `json:"privateKeyPem"`

	// Pkcs 8 encoded private key.
	PrivateKeyPkcs8 string `json:"privateKeyPkcs8"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []RsaesPkcs1TestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type RsaesPkcs1TestGroupType `json:"type"`
}

func (j *RsaesPkcs1TestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsaesPkcs1TestGroupType string

const RsaesPkcs1TestGroupTypeRsaesPkcs1Decrypt RsaesPkcs1TestGroupType = "RsaesPkcs1Decrypt"
func (j *RsaesPkcs1TestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsaesPkcs1TestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// An encryption of msg
	Ct string `json:"ct"`

	// A list of flags
	Flags []string `json:"flags"`

	// The encrypted message
	Msg string `json:"msg"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *RsaesPkcs1TestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsassaPkcs1GenTestGroup struct {
	// DER encoding of the sequence [n, e]
	KeyAsn string `json:"keyAsn"`

	// DER encoding of the public key
	KeyDer string `json:"keyDer"`

	// [Optional] Private key in JWK format
	KeyJwk *JsonWebKey `json:"keyJwk,omitempty,omitzero"`

	// Pem encoded public key
	KeyPem string `json:"keyPem"`

	// the size of the modulus in bits
	KeySize int `json:"keySize"`

	// PrivateKey corresponds to the JSON schema field "privateKey".
	PrivateKey PrivateKey `json:"privateKey"`

	// [Optional] Private key in JWK format
	PrivateKeyJwk *JsonWebKey `json:"privateKeyJwk,omitempty,omitzero"`

	// Pem encoded private key
	PrivateKeyPem string `json:"privateKeyPem"`

	// DER encoding of the PKCS8 private key
	PrivateKeyPkcs8 string `json:"privateKeyPkcs8"`

	// the hash function used for the message
	Sha string `json:"sha"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []SignatureTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type RsassaPkcs1GenTestGroupType `json:"type"`
}

func (j *RsassaPkcs1GenTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsassaPkcs1GenTestGroupType string

const RsassaPkcs1GenTestGroupTypeRsassaPkcs1Generate RsassaPkcs1GenTestGroupType = "RsassaPkcs1Generate"
func (j *RsassaPkcs1GenTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsassaPkcs1GenerateSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema RsassaPkcs1GenerateSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []RsassaPkcs1GenTestGroup `json:"testGroups"`
}

func (j *RsassaPkcs1GenerateSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsassaPkcs1GenerateSchemaV1JsonSchema string

const RsassaPkcs1GenerateSchemaV1JsonSchemaRsassaPkcs1GenerateSchemaV1Json RsassaPkcs1GenerateSchemaV1JsonSchema = "rsassa_pkcs1_generate_schema_v1.json"
func (j *RsassaPkcs1GenerateSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsassaPkcs1TestGroup struct {
	// KeyJwk corresponds to the JSON schema field "keyJwk".
	KeyJwk *JsonWebKey `json:"keyJwk,omitempty,omitzero"`

	// the size of the modulus in bits
	KeySize int `json:"keySize"`

	// PublicKey corresponds to the JSON schema field "publicKey".
	PublicKey RsassaPkcs1TestGroupPublicKey `json:"publicKey"`

	// ASN encoding of the sequence [n, e]
	PublicKeyAsn string `json:"publicKeyAsn"`

	// ASN encoding of the public key
	PublicKeyDer string `json:"publicKeyDer"`

	// Pem encoded public key
	PublicKeyPem string `json:"publicKeyPem"`

	// the hash function used for the message
	Sha string `json:"sha"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []SignatureTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type RsassaPkcs1TestGroupType `json:"type"`
}

func (j *RsassaPkcs1TestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsassaPkcs1TestGroupPublicKey struct {
	// The modulus of the key
	Modulus string `json:"modulus"`

	// The public exponent
	PublicExponent string `json:"publicExponent"`
}

func (j *RsassaPkcs1TestGroupPublicKey) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsassaPkcs1TestGroupType string

const RsassaPkcs1TestGroupTypeRsassaPkcs1Verify RsassaPkcs1TestGroupType = "RsassaPkcs1Verify"
func (j *RsassaPkcs1TestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsassaPkcs1VerifySchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema RsassaPkcs1VerifySchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []RsassaPkcs1TestGroup `json:"testGroups"`
}

func (j *RsassaPkcs1VerifySchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsassaPkcs1VerifySchemaV1JsonSchema string

const RsassaPkcs1VerifySchemaV1JsonSchemaRsassaPkcs1VerifySchemaV1Json RsassaPkcs1VerifySchemaV1JsonSchema = "rsassa_pkcs1_verify_schema_v1.json"
func (j *RsassaPkcs1VerifySchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsassaPssTestGroup struct {
	// the size of the modulus in bits
	KeySize int `json:"keySize"`

	// the message generating function (e.g. MGF1)
	Mgf string `json:"mgf"`

	// The hash function used for the message generating function.
	MgfSha string `json:"mgfSha"`

	// PublicKey corresponds to the JSON schema field "publicKey".
	PublicKey RsassaPssTestGroupPublicKey `json:"publicKey"`

	// ASN encoding of the sequence [n, e]
	PublicKeyAsn string `json:"publicKeyAsn"`

	// ASN encoding of the public key
	PublicKeyDer string `json:"publicKeyDer"`

	// PublicKeyJwk corresponds to the JSON schema field "publicKeyJwk".
	PublicKeyJwk *JsonWebKey `json:"publicKeyJwk,omitempty,omitzero"`

	// Pem encoded public key
	PublicKeyPem string `json:"publicKeyPem"`

	// The salt length
	SLen int `json:"sLen"`

	// The hash function for hashing the message.
	Sha string `json:"sha"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []RsassaPssTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type RsassaPssTestGroupType `json:"type"`
}

func (j *RsassaPssTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsassaPssTestGroupPublicKey struct {
	// The modulus of the key
	Modulus string `json:"modulus"`

	// The public exponent
	PublicExponent string `json:"publicExponent"`
}

func (j *RsassaPssTestGroupPublicKey) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsassaPssTestGroupType string

const RsassaPssTestGroupTypeRsassaPssVerify RsassaPssTestGroupType = "RsassaPssVerify"
func (j *RsassaPssTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsassaPssTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// The message to sign
	Msg string `json:"msg"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// a signature for msg
	Sig string `json:"sig"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *RsassaPssTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsassaPssVerifySchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema RsassaPssVerifySchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []RsassaPssTestGroup `json:"testGroups"`
}

func (j *RsassaPssVerifySchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type RsassaPssVerifySchemaV1JsonSchema string

const RsassaPssVerifySchemaV1JsonSchemaRsassaPssVerifySchemaV1Json RsassaPssVerifySchemaV1JsonSchema = "rsassa_pss_verify_schema_v1.json"
func (j *RsassaPssVerifySchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type SignatureTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// The message to sign
	Msg string `json:"msg"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// A signature for msg
	Sig string `json:"sig"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *SignatureTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type Source struct {
	// Name corresponds to the JSON schema field "name".
	Name string `json:"name"`

	// Version corresponds to the JSON schema field "version".
	Version string `json:"version"`
}

func (j *Source) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhAsnCompSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema XdhAsnCompSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []XdhAsnTestGroup `json:"testGroups"`
}

func (j *XdhAsnCompSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhAsnCompSchemaV1JsonSchema string

const XdhAsnCompSchemaV1JsonSchemaXdhAsnCompSchemaV1Json XdhAsnCompSchemaV1JsonSchema = "xdh_asn_comp_schema_v1.json"
func (j *XdhAsnCompSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhAsnTestGroup struct {
	// the name of the curve
	Curve string `json:"curve"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []XdhAsnTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type XdhAsnTestGroupType `json:"type"`
}

func (j *XdhAsnTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhAsnTestGroupType string

const XdhAsnTestGroupTypeXdhAsnComp XdhAsnTestGroupType = "XdhAsnComp"
func (j *XdhAsnTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhAsnTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// PKCS #8 encoded private key
	Private string `json:"private"`

	// X.509 encoded the public key
	Public string `json:"public"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// the shared secret
	Shared string `json:"shared"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *XdhAsnTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhCompSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema XdhCompSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []XdhTestGroup `json:"testGroups"`
}

func (j *XdhCompSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhCompSchemaV1JsonSchema string

const XdhCompSchemaV1JsonSchemaXdhCompSchemaV1Json XdhCompSchemaV1JsonSchema = "xdh_comp_schema_v1.json"
func (j *XdhCompSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhJwkCompSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema XdhJwkCompSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []XdhJwkTestGroup `json:"testGroups"`
}

func (j *XdhJwkCompSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhJwkCompSchemaV1JsonSchema string

const XdhJwkCompSchemaV1JsonSchemaXdhJwkCompSchemaV1Json XdhJwkCompSchemaV1JsonSchema = "xdh_jwk_comp_schema_v1.json"
func (j *XdhJwkCompSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhJwkTestGroup struct {
	// the name of the curve
	Curve string `json:"curve"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []XdhJwkTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type XdhJwkTestGroupType `json:"type"`
}

func (j *XdhJwkTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhJwkTestGroupType string

const XdhJwkTestGroupTypeXdhJwkComp XdhJwkTestGroupType = "XdhJwkComp"
func (j *XdhJwkTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhJwkTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// the private key in jwk format
	Private JsonWebKey `json:"private"`

	// the public key in jwk format
	Public JsonWebKey `json:"public"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// the shared secret
	Shared string `json:"shared"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *XdhJwkTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhPemCompSchemaV1Json struct {
	// the primitive tested in the test file
	Algorithm string `json:"algorithm"`

	// DEPRECATED: prefer "source" property in test group
	GeneratorVersion *string `json:"generatorVersion,omitempty,omitzero"`

	// additional documentation
	Header []string `json:"header"`

	// Notes corresponds to the JSON schema field "notes".
	Notes Notes `json:"notes"`

	// the number of test vectors in this test
	NumberOfTests int `json:"numberOfTests"`

	// Schema corresponds to the JSON schema field "schema".
	Schema XdhPemCompSchemaV1JsonSchema `json:"schema"`

	// TestGroups corresponds to the JSON schema field "testGroups".
	TestGroups []XdhPemTestGroup `json:"testGroups"`
}

func (j *XdhPemCompSchemaV1Json) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhPemCompSchemaV1JsonSchema string

const XdhPemCompSchemaV1JsonSchemaXdhPemCompSchemaV1Json XdhPemCompSchemaV1JsonSchema = "xdh_pem_comp_schema_v1.json"
func (j *XdhPemCompSchemaV1JsonSchema) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhPemTestGroup struct {
	// the name of the curve
	Curve string `json:"curve"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []XdhPemTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type XdhPemTestGroupType `json:"type"`
}

func (j *XdhPemTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhPemTestGroupType string

const XdhPemTestGroupTypeXdhPemComp XdhPemTestGroupType = "XdhPemComp"
func (j *XdhPemTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhPemTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// a raw private key
	Private string `json:"private"`

	// PEM encoded public key
	Public string `json:"public"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// the shared secret
	Shared string `json:"shared"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *XdhPemTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhTestGroup struct {
	// the name of the curve
	Curve string `json:"curve"`

	// Source corresponds to the JSON schema field "source".
	Source Source `json:"source"`

	// Tests corresponds to the JSON schema field "tests".
	Tests []XdhTestVector `json:"tests"`

	// Type corresponds to the JSON schema field "type".
	Type XdhTestGroupType `json:"type"`
}

func (j *XdhTestGroup) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhTestGroupType string

const XdhTestGroupTypeXdhComp XdhTestGroupType = "XdhComp"
func (j *XdhTestGroupType) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.

type XdhTestVector struct {
	// A brief description of the test case
	Comment string `json:"comment"`

	// A list of flags
	Flags []string `json:"flags"`

	// the raw bytes of private key
	Private string `json:"private"`

	// the raw bytes of the public key
	Public string `json:"public"`

	// Result corresponds to the JSON schema field "result".
	Result Result `json:"result"`

	// the shared secret
	Shared string `json:"shared"`

	// Identifier of the test case
	TcId int `json:"tcId"`
}

func (j *XdhTestVector) UnmarshalJSON(value []byte) error
    UnmarshalJSON implements json.Unmarshaler.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
