# package crypto/internal/cryptotest

- 원문: <https://pkg.go.dev/crypto/internal/cryptotest>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package cryptotest // import "crypto/internal/cryptotest"


FUNCTIONS

func BoundarySlices(t *testing.T, size int) (start, end []byte)
    BoundarySlices allocates a pair of slices of the given size one at the
    start of a page, another at the end. Any access beyond or before the slice
    boundaries should cause a fault.

func FetchModule(t *testing.T, module, version string) string
    FetchModule fetches the module at the given version and returns the
    directory containing its source tree. It skips the test if fetching modules
    is not possible in this environment.

func MustMinimumFIPS140ModuleVersion(tb testing.TB, min string)
    MustMinimumFIPS140ModuleVersion skips the test if compiled against a lower
    minor version of the FIPS 140-3 module than min (such as "v1.26.0").

func MustSupportFIPS140(tb testing.TB)
func NoExtraMethods(t *testing.T, ms any, allowed ...string)
    NoExtraMethods checks that the concrete type of *ms has no exported methods
    beyond the methods of the interface type of *ms, and any others specified in
    the allowed list.

    These methods are accessible through interface upgrades, so they end up part
    of the API even if undocumented per Hyrum's Law.

    ms must be a pointer to a non-nil interface.

func RerunWithFIPS140Enabled(t *testing.T)
func RerunWithFIPS140Enforced(t *testing.T)
func SkipTestAllocations(t *testing.T)
    SkipTestAllocations skips the test if there are any factors that interfere
    with allocation optimizations.

func TestAEAD(t *testing.T, mAEAD MakeAEAD)
    TestAEAD performs a set of tests on cipher.AEAD implementations, checking
    the documented requirements of NonceSize, Overhead, Seal and Open.

func TestAllImplementations(t *testing.T, pkg string, f func(t *testing.T))
    TestAllImplementations runs the provided test function with each available
    implementation of the package registered with crypto/internal/impl. If there
    are no alternative implementations for pkg, f is invoked directly once.

func TestBlock(t *testing.T, keySize int, mb MakeBlock)
    TestBlock performs a set of tests on cipher.Block implementations, checking
    the documented requirements of BlockSize, Encrypt, and Decrypt.

func TestBlockMode(t *testing.T, block cipher.Block, makeEncrypter, makeDecrypter MakeBlockMode)
    TestBlockMode performs a set of tests on cipher.BlockMode implementations,
    checking the documented requirements of CryptBlocks.

func TestHash(t *testing.T, mh MakeHash)
    TestHash performs a set of tests on hash.Hash implementations, checking the
    documented requirements of Write, Sum, Reset, Size, and BlockSize.

func TestStream(t *testing.T, ms MakeStream)
    TestStream performs a set of tests on cipher.Stream implementations,
    checking the documented requirements of XORKeyStream.

func TestStreamFromBlock(t *testing.T, block cipher.Block, blockMode func(b cipher.Block, iv []byte) cipher.Stream)
    TestStreamFromBlock creates a Stream from a cipher.Block used in a
    cipher.BlockMode. It addresses Issue 68377 by checking for a panic when the
    BlockMode uses an IV with incorrect length. For a valid IV, it also runs all
    TestStream tests on the resulting stream.


TYPES

type MakeAEAD func() (cipher.AEAD, error)
    MakeAEAD returns a cipher.AEAD instance.

    Multiple calls to MakeAEAD must return equivalent instances, so for example
    the key must be fixed.

type MakeBlock func(key []byte) (cipher.Block, error)

type MakeBlockMode func(b cipher.Block, iv []byte) cipher.BlockMode
    MakeBlockMode returns a cipher.BlockMode instance. It expects len(iv) ==
    b.BlockSize().

type MakeHash func() hash.Hash

type MakeStream func() cipher.Stream
    MakeStream returns a cipher.Stream instance.

    Multiple calls to MakeStream must return equivalent instances, so for
    example the key and/or IV must be fixed.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
