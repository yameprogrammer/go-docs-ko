# package internal/lazytemplate

- 원문: <https://pkg.go.dev/internal/lazytemplate>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package lazytemplate is a thin wrapper over text/template, allowing the use of global template variables without forcing them to be parsed at init.

## 원문 요약

Package lazytemplate is a thin wrapper over text/template, allowing the use of global template variables without forcing them to be parsed at init.

## API 상세 (go doc -all)

~~~text
package lazytemplate // import "internal/lazytemplate"

Package lazytemplate is a thin wrapper over text/template, allowing the use of
global template variables without forcing them to be parsed at init.

TYPES

type Template struct {
	// Has unexported fields.
}
    Template is a wrapper around text/template.Template, where the underlying
    template will be parsed the first time it is needed.

func New(name, text string) *Template
    New creates a new lazy template, delaying the parsing work until it is first
    needed. If the code is being run as part of tests, the template parsing will
    happen immediately.

func (r *Template) Execute(w io.Writer, data any) error
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
