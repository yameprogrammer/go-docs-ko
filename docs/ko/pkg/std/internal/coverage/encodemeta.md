# package internal/coverage/encodemeta

- 원문: <https://pkg.go.dev/internal/coverage/encodemeta>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package encodemeta // import "internal/coverage/encodemeta"


FUNCTIONS

func HashFuncDesc(f *coverage.FuncDesc) [16]byte
    HashFuncDesc computes an md5 sum of a coverage.FuncDesc and returns a digest
    for it.


TYPES

type CoverageMetaDataBuilder struct {
	// Has unexported fields.
}

func NewCoverageMetaDataBuilder(pkgpath string, pkgname string, modulepath string) (*CoverageMetaDataBuilder, error)

func (b *CoverageMetaDataBuilder) AddFunc(f coverage.FuncDesc) uint
    AddFunc registers a new function with the meta data builder.

func (b *CoverageMetaDataBuilder) Emit(w io.WriteSeeker) ([16]byte, error)
    Emit writes the meta-data accumulated so far in this builder to 'w'. Returns
    a hash of the meta-data payload and an error.

type CoverageMetaFileWriter struct {
	// Has unexported fields.
}

func NewCoverageMetaFileWriter(mfname string, w io.Writer) *CoverageMetaFileWriter

func (m *CoverageMetaFileWriter) Write(finalHash [16]byte, blobs [][]byte, mode coverage.CounterMode, granularity coverage.CounterGranularity) error
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
