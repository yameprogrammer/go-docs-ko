# package crypto/internal/fips140/sha3

- 원문: <https://pkg.go.dev/crypto/internal/fips140/sha3>
- 분류: Go 표준 라이브러리

## 한국어 요약

`sha3` 패키지는 [FIPS 202]에서 정의한 SHA-3 고정 출력 길이 해시 함수와 SHAKE 가변 출력 길이 함수, 그리고 [SP 800-185]에서 정의한 cSHAKE 확장 출력 길이 함수를 구현합니다.

## 원문 요약

Package sha3 implements the SHA-3 fixed-output-length hash functions and the SHAKE variable-output-length functions defined by [FIPS 202], as well as the cSHAKE extendable-output-length functions defined by [SP 800-185].

## API 상세 (go doc -all)

~~~text
package sha3 // import "crypto/internal/fips140/sha3"

Package sha3 implements the SHA-3 fixed-output-length hash functions and the
SHAKE variable-output-length functions defined by FIPS 202, as well as the
cSHAKE extendable-output-length functions defined by SP 800-185.

[FIPS 202]: https://doi.org/10.6028/NIST.FIPS.202
[SP 800-185]: https://doi.org/10.6028/NIST.SP.800-185

TYPES

type Digest struct {
	// Has unexported fields.
}

func New224() *Digest
    New224 returns a new Digest computing the SHA3-224 hash.

func New256() *Digest
    New256 returns a new Digest computing the SHA3-256 hash.

func New384() *Digest
    New384 returns a new Digest computing the SHA3-384 hash.

func New512() *Digest
    New512 returns a new Digest computing the SHA3-512 hash.

func NewLegacyKeccak256() *Digest
    NewLegacyKeccak256 returns a new Digest computing the legacy, non-standard
    Keccak-256 hash.

func NewLegacyKeccak512() *Digest
    NewLegacyKeccak512 returns a new Digest computing the legacy, non-standard
    Keccak-512 hash.

func (d *Digest) AppendBinary(b []byte) ([]byte, error)

func (d *Digest) BlockSize() int
    BlockSize returns the rate of sponge underlying this hash function.

func (d *Digest) Clone() *Digest

func (d *Digest) MarshalBinary() ([]byte, error)

func (d *Digest) Reset()
    Reset resets the Digest to its initial state.

func (d *Digest) Size() int
    Size returns the output size of the hash function in bytes.

func (d *Digest) Sum(b []byte) []byte
    Sum appends the current hash to b and returns the resulting slice. It does
    not change the underlying hash state.

func (d *Digest) UnmarshalBinary(b []byte) error

func (d *Digest) Write(p []byte) (n int, err error)
    Write absorbs more data into the hash's state.

type SHAKE struct {
	// Has unexported fields.
}

func NewCShake128(N, S []byte) *SHAKE
    NewCShake128 creates a new cSHAKE128 XOF.

    N is used to define functions based on cSHAKE, it can be empty when
    plain cSHAKE is desired. S is a customization byte string used for domain
    separation. When N and S are both empty, this is equivalent to NewShake128.

func NewCShake256(N, S []byte) *SHAKE
    NewCShake256 creates a new cSHAKE256 XOF.

    N is used to define functions based on cSHAKE, it can be empty when
    plain cSHAKE is desired. S is a customization byte string used for domain
    separation. When N and S are both empty, this is equivalent to NewShake256.

func NewShake128() *SHAKE
    NewShake128 creates a new SHAKE128 XOF.

func NewShake256() *SHAKE
    NewShake256 creates a new SHAKE256 XOF.

func (s *SHAKE) AppendBinary(b []byte) ([]byte, error)

func (s *SHAKE) BlockSize() int

func (s *SHAKE) Clone() *SHAKE
    Clone returns a copy of the SHAKE context in its current state.

func (s *SHAKE) MarshalBinary() ([]byte, error)

func (s *SHAKE) Read(out []byte) (n int, err error)

func (s *SHAKE) Reset()
    Reset resets the hash to initial state.

func (s *SHAKE) Size() int

func (s *SHAKE) Sum(in []byte) []byte
    Sum appends a portion of output to b and returns the resulting slice.
    The output length is selected to provide full-strength generic security:
    32 bytes for SHAKE128 and 64 bytes for SHAKE256. It does not change the
    underlying state. It panics if any output has already been read.

func (s *SHAKE) UnmarshalBinary(b []byte) error

func (s *SHAKE) Write(p []byte) (n int, err error)
    Write absorbs more data into the hash's state. It panics if any output has
    already been read.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
