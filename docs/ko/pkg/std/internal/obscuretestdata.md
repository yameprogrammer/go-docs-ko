# package internal/obscuretestdata

- 원문: <https://pkg.go.dev/internal/obscuretestdata>
- 분류: Go 표준 라이브러리

## 한국어 요약

`obscuretestdata` 패키지는 주로 golang.org/issue/34986로 인해 반드시 익명화(obscure)되어야 하는 테스트 데이터(testdata)를 테스트에서 더 쉽게 다루기 위해 사용되는 기능을 제공합니다.

## 원문 요약

Package obscuretestdata contains functionality used by tests to more easily work with testdata that must be obscured primarily due to golang.org/issue/34986.

## API 상세 (go doc -all)

~~~text
package obscuretestdata // import "internal/obscuretestdata"

Package obscuretestdata contains functionality used by tests to more easily work
with testdata that must be obscured primarily due to golang.org/issue/34986.

FUNCTIONS

func DecodeToTempFile(name string) (path string, err error)
    DecodeToTempFile decodes the named file to a temporary location.
    If successful, it returns the path of the decoded file. The caller is
    responsible for ensuring that the temporary file is removed.

func ReadFile(name string) ([]byte, error)
    ReadFile reads the named file and returns its decoded contents.

func Rot13(data []byte) []byte
    Rot13 returns the rot13 encoding or decoding of its input.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
