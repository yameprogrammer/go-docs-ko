# package internal/coverage/decodemeta

- 원문: <https://pkg.go.dev/internal/coverage/decodemeta>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package decodemeta // import "internal/coverage/decodemeta"


TYPES

type CoverageMetaDataDecoder struct {
	// Has unexported fields.
}

func NewCoverageMetaDataDecoder(b []byte, readonly bool) (*CoverageMetaDataDecoder, error)

func (d *CoverageMetaDataDecoder) ModulePath() string

func (d *CoverageMetaDataDecoder) NumFuncs() uint32

func (d *CoverageMetaDataDecoder) PackageName() string

func (d *CoverageMetaDataDecoder) PackagePath() string

func (d *CoverageMetaDataDecoder) ReadFunc(fidx uint32, f *coverage.FuncDesc) error
    ReadFunc reads the coverage meta-data for the function with index 'findex',
    filling it into the FuncDesc pointed to by 'f'.

type CoverageMetaFileReader struct {
	// Has unexported fields.
}
    CoverageMetaFileReader provides state and methods for reading a meta-data
    file from a code coverage run.

func NewCoverageMetaFileReader(f *os.File, fileView []byte) (*CoverageMetaFileReader, error)
    NewCoverageMetaFileReader returns a new helper object for reading the
    coverage meta-data output file 'f'. The param 'fileView' is a read-only
    slice containing the contents of 'f' obtained by mmap'ing the file
    read-only; 'fileView' may be nil, in which case the helper will read the
    contents of the file using regular file Read operations.

func (r *CoverageMetaFileReader) CounterGranularity() coverage.CounterGranularity
    CounterGranularity returns the counter granularity (single counter per
    function, or counter per block) selected when building for coverage for the
    program that produce this meta-data file.

func (r *CoverageMetaFileReader) CounterMode() coverage.CounterMode
    CounterMode returns the counter mode (set, count, atomic) used when building
    for coverage for the program that produce this meta-data file.

func (r *CoverageMetaFileReader) FileHash() [16]byte
    FileHash returns the hash computed for all of the package meta-data blobs.
    Coverage counter data files refer to this hash, and the hash will be encoded
    into the meta-data file name.

func (r *CoverageMetaFileReader) GetPackageDecoder(pkIdx uint32, payloadbuf []byte) (*CoverageMetaDataDecoder, []byte, error)
    GetPackageDecoder requests a decoder object for the package within the
    meta-data file whose index is 'pkIdx'. If the CoverageMetaFileReader was
    set up with a read-only file view, a pointer into that file view will be
    returned, otherwise the buffer 'payloadbuf' will be written to (or if it is
    not of sufficient size, a new buffer will be allocated). Return value is the
    decoder, a byte slice with the encoded meta-data, and an error.

func (r *CoverageMetaFileReader) GetPackagePayload(pkIdx uint32, payloadbuf []byte) ([]byte, error)
    GetPackagePayload returns the raw (encoded) meta-data payload for
    the package with index 'pkIdx'. As with GetPackageDecoder, if the
    CoverageMetaFileReader was set up with a read-only file view, a pointer
    into that file view will be returned, otherwise the buffer 'payloadbuf'
    will be written to (or if it is not of sufficient size, a new buffer will
    be allocated). Return value is the decoder, a byte slice with the encoded
    meta-data, and an error.

func (r *CoverageMetaFileReader) NumPackages() uint64
    NumPackages returns the number of packages for which this file contains
    meta-data.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
