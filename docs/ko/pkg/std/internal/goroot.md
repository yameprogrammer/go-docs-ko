# package internal/goroot

- 원문: <https://pkg.go.dev/internal/goroot>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package goroot // import "internal/goroot"


FUNCTIONS

func IsStandardPackage(readDir func(string) ([]os.DirEntry, error), goroot, compiler, path string) bool
    IsStandardPackage reports whether path is a standard package, given goroot
    and compiler. readDir accepts OS filesystem paths.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
