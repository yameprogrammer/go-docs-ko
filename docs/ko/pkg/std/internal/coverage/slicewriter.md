# package internal/coverage/slicewriter

- 원문: <https://pkg.go.dev/internal/coverage/slicewriter>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package slicewriter // import "internal/coverage/slicewriter"


TYPES

type WriteSeeker struct {
	// Has unexported fields.
}
    WriteSeeker is a helper object that implements the io.WriteSeeker interface.
    Clients can create a WriteSeeker, make a series of Write calls to add data
    to it (and possibly Seek calls to update previously written portions),
    then finally invoke BytesWritten() to get a pointer to the constructed byte
    slice.

func (sws *WriteSeeker) BytesWritten() []byte
    BytesWritten returns the underlying byte slice for the WriteSeeker,
    containing the data written to it via Write/Seek calls.

func (sws *WriteSeeker) Read(p []byte) (n int, err error)

func (sws *WriteSeeker) Seek(offset int64, whence int) (int64, error)
    Seek repositions the read/write position of the WriteSeeker within its
    internally maintained slice. Note that it is not possible to expand the size
    of the slice using SEEK_SET; trying to seek outside the slice will result in
    an error.

func (sws *WriteSeeker) Write(p []byte) (n int, err error)
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
