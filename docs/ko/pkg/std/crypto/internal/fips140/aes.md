# package crypto/internal/fips140/aes

- 원문: <https://pkg.go.dev/crypto/internal/fips140/aes>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package aes // import "crypto/internal/fips140/aes"


CONSTANTS

const BlockSize = 16
    BlockSize is the AES block size in bytes.


FUNCTIONS

func EncryptBlockInternal(c *Block, dst, src []byte)
    EncryptBlockInternal applies the AES encryption function to one block.

    It is an internal function meant only for the gcm package.

func EncryptionKeySchedule(c *Block) []uint32
    EncryptionKeySchedule is used from the GCM implementation to access the
    precomputed AES key schedule, to pass to the assembly implementation.

func RoundToBlock(c *CTR)
    RoundToBlock is used by CTR_DRBG, which discards the rightmost unused bits
    at each request. It rounds the offset up to the next block boundary.


TYPES

type Block struct {
	// Has unexported fields.
}
    A Block is an instance of AES using a particular key. It is safe for
    concurrent use.

func New(key []byte) (*Block, error)
    New creates and returns a new [cipher.Block] implementation. The key
    argument should be the AES key, either 16, 24, or 32 bytes to select
    AES-128, AES-192, or AES-256.

func (c *Block) BlockSize() int

func (c *Block) Decrypt(dst, src []byte)

func (c *Block) Encrypt(dst, src []byte)

type CBCDecrypter struct {
	// Has unexported fields.
}

func NewCBCDecrypter(b *Block, iv [BlockSize]byte) *CBCDecrypter
    NewCBCDecrypter returns a [cipher.BlockMode] which decrypts in cipher block
    chaining mode, using the given Block.

func (c *CBCDecrypter) BlockSize() int

func (c *CBCDecrypter) CryptBlocks(dst, src []byte)

func (x *CBCDecrypter) SetIV(iv []byte)

type CBCEncrypter struct {
	// Has unexported fields.
}

func NewCBCEncrypter(b *Block, iv [BlockSize]byte) *CBCEncrypter
    NewCBCEncrypter returns a [cipher.BlockMode] which encrypts in cipher block
    chaining mode, using the given Block.

func (c *CBCEncrypter) BlockSize() int

func (c *CBCEncrypter) CryptBlocks(dst, src []byte)

func (x *CBCEncrypter) SetIV(iv []byte)

type CTR struct {
	// Has unexported fields.
}

func NewCTR(b *Block, iv []byte) *CTR

func (c *CTR) XORKeyStream(dst, src []byte)

func (c *CTR) XORKeyStreamAt(dst, src []byte, offset uint64)
    XORKeyStreamAt behaves like XORKeyStream but keeps no state, and instead
    seeks into the keystream by the given bytes offset from the start (ignoring
    any XORKetStream calls). This allows for random access into the keystream,
    up to 16 EiB from the start.

type KeySizeError int

func (k KeySizeError) Error() string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
