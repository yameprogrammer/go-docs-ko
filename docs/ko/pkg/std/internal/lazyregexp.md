# package internal/lazyregexp

- 원문: <https://pkg.go.dev/internal/lazyregexp>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package lazyregexp is a thin wrapper over regexp, allowing the use of global regexp variables without forcing them to be compiled at init.

## 원문 요약

Package lazyregexp is a thin wrapper over regexp, allowing the use of global regexp variables without forcing them to be compiled at init.

## API 상세 (go doc -all)

~~~text
package lazyregexp // import "internal/lazyregexp"

Package lazyregexp is a thin wrapper over regexp, allowing the use of global
regexp variables without forcing them to be compiled at init.

TYPES

type Regexp struct {
	// Has unexported fields.
}
    Regexp is a wrapper around regexp.Regexp, where the underlying regexp will
    be compiled the first time it is needed.

func New(str string) *Regexp
    New creates a new lazy regexp, delaying the compiling work until it is first
    needed. If the code is being run as part of tests, the regexp compiling will
    happen immediately.

func (r *Regexp) FindAllString(s string, n int) []string

func (r *Regexp) FindString(s string) string

func (r *Regexp) FindStringSubmatch(s string) []string

func (r *Regexp) FindStringSubmatchIndex(s string) []int

func (r *Regexp) FindSubmatch(s []byte) [][]byte

func (r *Regexp) MatchString(s string) bool

func (r *Regexp) ReplaceAll(src, repl []byte) []byte

func (r *Regexp) ReplaceAllString(src, repl string) string

func (r *Regexp) SubexpNames() []string
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
