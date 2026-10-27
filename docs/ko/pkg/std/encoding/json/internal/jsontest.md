# package encoding/json/internal/jsontest

- 원문: <https://pkg.go.dev/encoding/json/internal/jsontest>
- 분류: Go 표준 라이브러리

## 한국어 요약

`jsontest` 패키지는 JSON 테스트를 지원하는 기능을 포함하고 있습니다.

## 원문 요약

Package jsontest contains functionality to assist in testing JSON.

## API 상세 (go doc -all)

~~~text
package jsontest // import "encoding/json/internal/jsontest"

Package jsontest contains functionality to assist in testing JSON.

VARIABLES

var Data = func() (entries []Entry) {
	fis := mustGet(fs.ReadDir(testdataFS, "_embed"))
	slices.SortFunc(fis, func(x, y fs.DirEntry) int { return strings.Compare(x.Name(), y.Name()) })
	for _, fi := range fis {
		var entry Entry

		words := strings.Split(strings.TrimSuffix(fi.Name(), ".json.zst"), "_")
		for i := range words {
			words[i] = strings.Title(words[i])
		}
		entry.Name = strings.Join(words, "")

		entry.Data = sync.OnceValue(func() []byte {
			filePath := path.Join("_embed", fi.Name())
			b := mustGet(fs.ReadFile(testdataFS, filePath))
			zr := zstd.NewReader(bytes.NewReader(b))
			return mustGet(io.ReadAll(zr))
		})

		switch entry.Name {
		case "CanadaGeometry":
			entry.New = func() any { return new(canadaRoot) }
		case "CitmCatalog":
			entry.New = func() any { return new(citmRoot) }
		case "GolangSource":
			entry.New = func() any { return new(golangRoot) }
		case "StringEscaped":
			entry.New = func() any { return new(stringRoot) }
		case "StringUnicode":
			entry.New = func() any { return new(stringRoot) }
		case "SyntheaFhir":
			entry.New = func() any { return new(syntheaRoot) }
		case "TwitterStatus":
			entry.New = func() any { return new(twitterRoot) }
		}

		entries = append(entries, entry)
	}
	return entries
}()
    Data is a list of JSON testdata.


TYPES

type CaseName struct {
	Name  string
	Where CasePos
}
    CaseName is a case name annotated with a file and line.

func Name(s string) (c CaseName)
    Name annotates a case name with the file and line of the caller.

type CasePos struct {
	// Has unexported fields.
}
    CasePos represents a file and line number.

func (pos CasePos) String() string

type Entry struct {
	Name string
	Data func() []byte
	New  func() any // nil if there is no concrete type for this
}
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
