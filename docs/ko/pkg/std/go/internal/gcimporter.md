# package go/internal/gcimporter

- 원문: <https://pkg.go.dev/go/internal/gcimporter>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `gcimporter`는 `gc`에서 생성된 객체 파일에 대한 임포트를 구현합니다.

## 원문 요약

Package gcimporter implements Import for gc-generated object files.

## API 상세 (go doc -all)

~~~text
package gcimporter // import "go/internal/gcimporter"

Package gcimporter implements Import for gc-generated object files.

FUNCTIONS

func Import(fset *token.FileSet, packages map[string]*types.Package, path, srcDir string, lookup func(path string) (io.ReadCloser, error)) (pkg *types.Package, err error)
    Import imports a gc-generated package given its import path and srcDir,
    adds the corresponding package object to the packages map, and returns the
    object. The packages map must contain all packages already imported.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
