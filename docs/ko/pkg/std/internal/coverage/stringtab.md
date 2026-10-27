# package internal/coverage/stringtab

- 원문: <https://pkg.go.dev/internal/coverage/stringtab>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package stringtab // import "internal/coverage/stringtab"


TYPES

type Reader struct {
	// Has unexported fields.
}
    Reader is a helper for reading a string table previously serialized by a
    Writer.Write call.

func NewReader(r *slicereader.Reader) *Reader
    NewReader creates a stringtab.Reader to read the contents of a string table
    from 'r'.

func (str *Reader) Entries() int
    Entries returns the number of decoded entries in a string table.

func (str *Reader) Get(idx uint32) string
    Get returns string 'idx' within the string table.

func (str *Reader) Read()
    Read reads/decodes a string table using the reader provided.

type Writer struct {
	// Has unexported fields.
}
    Writer implements a string table writing utility.

func (stw *Writer) Freeze()
    Freeze sends a signal to the writer that no more additions are allowed,
    only lookups of existing strings (if a lookup triggers addition, a panic
    will result). Useful as a mechanism for "finalizing" a string table prior to
    writing it out.

func (stw *Writer) InitWriter()
    InitWriter initializes a stringtab.Writer.

func (stw *Writer) Lookup(s string) uint32
    Lookup looks up string 's' in the writer's table, adding a new entry if need
    be, and returning an index into the table.

func (stw *Writer) Nentries() uint32
    Nentries returns the number of strings interned so far.

func (stw *Writer) Size() uint32
    Size computes the memory in bytes needed for the serialized version of a
    stringtab.Writer.

func (stw *Writer) Write(w io.Writer) error
    Write writes the string table in serialized form to the specified io.Writer.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
