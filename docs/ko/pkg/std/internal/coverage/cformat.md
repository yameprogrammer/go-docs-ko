# package internal/coverage/cformat

- 원문: <https://pkg.go.dev/internal/coverage/cformat>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package cformat // import "internal/coverage/cformat"


TYPES

type Formatter struct {
	// Has unexported fields.
}

func NewFormatter(cm coverage.CounterMode) *Formatter

func (fm *Formatter) AddUnit(file string, fname string, isfnlit bool, unit coverage.CoverableUnit, count uint32)
    AddUnit passes info on a single coverable unit (file, funcname, literal
    flag, range of lines, and counter value) to the formatter. Counter values
    will be accumulated where appropriate.

func (fm *Formatter) EmitFuncs(w io.Writer) error
    EmitFuncs writes out a function-level summary to the writer 'w'. A note on
    handling function literals: although we collect coverage data for unnamed
    literals, it probably does not make sense to include them in the function
    summary since there isn't any good way to name them (this is also consistent
    with the legacy cmd/cover implementation). We do want to include their
    counts in the overall summary however.

func (fm *Formatter) EmitPercent(w io.Writer, pkgs []string, inpkgs string, noteEmpty bool, aggregate bool) error
    EmitPercent writes out a "percentage covered" string to the writer 'w',
    selecting the set of packages in 'pkgs' and suffixing the printed string
    with 'inpkgs'.

func (fm *Formatter) EmitTextual(pkgs []string, w io.Writer) error
    EmitTextual writes the accumulated coverage data for 'pkgs' in the
    legacy cmd/cover text format to the writer 'w'; if pkgs is empty,
    text output is emitted for all packages recorded. We sort the data items
    by importpath, source file, and line number before emitting (this sorting
    is not explicitly mandated by the format, but seems like a good idea for
    repeatable/deterministic dumps).

func (fm *Formatter) SetPackage(importpath string)
    SetPackage tells the formatter that we're about to visit the coverage data
    for the package with the specified import path. Note that it's OK to call
    SetPackage more than once with the same import path; counter data values
    will be accumulated.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
