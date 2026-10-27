# package crypto/internal/rand

- 원문: <https://pkg.go.dev/crypto/internal/rand>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package rand // import "crypto/internal/rand"


VARIABLES

var Reader io.Reader = reader{}
    Reader is an io.Reader that calls drbg.Read.

    It should be used internally instead of crypto/rand.Reader, because the
    latter can be set by applications outside of tests. These applications then
    risk breaking between Go releases, if the way the Reader is used changes.


FUNCTIONS

func CustomReader(r io.Reader) io.Reader
    CustomReader returns Reader or, only if the GODEBUG setting
    "cryptocustomrand=1" is set, the provided io.Reader.

    If returning a non-default Reader, it calls randutil.MaybeReadByte on it,
    unless it's the global testing Reader set with SetTestingReader.

func IsDefaultReader(r io.Reader) bool
    IsDefaultReader reports whether r is the default crypto/rand.Reader.

    If true, the Read method of r can be assumed to call drbg.Read.

func SetTestingReader(r io.Reader)
    SetTestingReader overrides all calls to drbg.Read. The Read method of r must
    never return an error or return short.

    SetTestingReader panics when building against Go Cryptographic Module
    v1.0.0.

    SetTestingReader is pulled by testing/cryptotest.SetGlobalRandom via
    go:linkname.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
