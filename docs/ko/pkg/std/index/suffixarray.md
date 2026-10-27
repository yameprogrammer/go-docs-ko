# package index/suffixarray

- 원문: <https://pkg.go.dev/index/suffixarray>
- 분류: Go 표준 라이브러리

## 한국어 요약

`suffixarray` 패키지는 인메모리 접미사 배열(suffix array)을 사용하여 로그 시간 내에 부분 문자열 검색을 구현합니다.

## 원문 요약

Package suffixarray implements substring search in logarithmic time using an in-memory suffix array.

## API 상세 (go doc -all)

~~~text
package suffixarray // import "index/suffixarray"

Package suffixarray implements substring search in logarithmic time using an
in-memory suffix array.

Example use:

    // create index for some data
    index := suffixarray.New(data)

    // lookup byte slice s
    offsets1 := index.Lookup(s, -1) // the list of all indices where s occurs in data
    offsets2 := index.Lookup(s, 3)  // the list of at most 3 indices where s occurs in data

TYPES

type Index struct {
	// Has unexported fields.
}
    Index implements a suffix array for fast substring search.

func New(data []byte) *Index
    New creates a new Index for data. Index creation time is O(N) for N =
    len(data).

func (x *Index) Bytes() []byte
    Bytes returns the data over which the index was created. It must not be
    modified.

func (x *Index) FindAllIndex(r *regexp.Regexp, n int) (result [][]int)
    FindAllIndex returns a sorted list of non-overlapping matches of the regular
    expression r, where a match is a pair of indices specifying the matched
    slice of x.Bytes(). If n < 0, all matches are returned in successive order.
    Otherwise, at most n matches are returned and they may not be successive.
    The result is nil if there are no matches, or if n == 0.

func (x *Index) Lookup(s []byte, n int) (result []int)
    Lookup returns an unsorted list of at most n indices where the byte string
    s occurs in the indexed data. If n < 0, all occurrences are returned.
    The result is nil if s is empty, s is not found, or n == 0. Lookup time is
    O(log(N)*len(s) + len(result)) where N is the size of the indexed data.

func (x *Index) Read(r io.Reader) error
    Read reads the index from r into x; x must not be nil.

func (x *Index) Write(w io.Writer) error
    Write writes the index x to w.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
