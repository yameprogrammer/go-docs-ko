# package internal/txtar

- 원문: <https://pkg.go.dev/internal/txtar>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `txtar`는 간단한 텍스트 기반 파일 아카이브 형식을 구현합니다.

## 원문 요약

Package txtar implements a trivial text-based file archive format.

## API 상세 (go doc -all)

~~~text
package txtar // import "internal/txtar"

Package txtar implements a trivial text-based file archive format.

The goals for the format are:

  - be trivial enough to create and edit by hand.
  - be able to store trees of text files describing go command test cases.
  - diff nicely in git history and code reviews.

Non-goals include being a completely general archive format, storing binary
data, storing file modes, storing special files like symbolic links, and so on.

# Txtar format

A txtar archive is zero or more comment lines and then a sequence of file
entries. Each file entry begins with a file marker line of the form "-- FILENAME
--" and is followed by zero or more file content lines making up the file data.
The comment or file content ends at the next file marker line. The file marker
line must begin with the three-byte sequence "-- " and end with the three-byte
sequence " --", but the enclosed file name can be surrounding by additional
white space, all of which is stripped.

If the txtar file is missing a trailing newline on the final line, parsers
should consider a final newline to be present anyway.

There are no possible syntax errors in a txtar archive.

FUNCTIONS

func Format(a *Archive) []byte
    Format returns the serialized form of an Archive. It is assumed that the
    Archive data structure is well-formed: a.Comment and all a.File[i].Data
    contain no file marker lines, and all a.File[i].Name is non-empty.


TYPES

type Archive struct {
	Comment []byte
	Files   []File
}
    An Archive is a collection of files.

func Parse(data []byte) *Archive
    Parse parses the serialized form of an Archive. The returned Archive holds
    slices of data.

func ParseFile(file string) (*Archive, error)
    ParseFile parses the named file as an archive.

type File struct {
	Name string // name of file ("foo/bar.txt")
	Data []byte // text content of file
}
    A File is a single file in an archive.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
