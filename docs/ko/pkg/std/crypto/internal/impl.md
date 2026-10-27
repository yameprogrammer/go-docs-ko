# package crypto/internal/impl

- 원문: <https://pkg.go.dev/crypto/internal/impl>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `impl`은 암호화 기본 구성 요소의 대안 구현을 등록하는 레지스트리입니다. 이를 통해 테스트 시 선택할 수 있습니다.

## 원문 요약

Package impl is a registry of alternative implementations of cryptographic primitives, to allow selecting them for testing.

## API 상세 (go doc -all)

~~~text
package impl // import "crypto/internal/impl"

Package impl is a registry of alternative implementations of cryptographic
primitives, to allow selecting them for testing.

FUNCTIONS

func List(pkg string) []string
    List returns the names of all alternative implementations registered for the
    given package, whether available or not. The implicit base implementation is
    not included.

func Packages() []string
    Packages returns the list of all packages for which alternative
    implementations are registered.

func Register(pkg, name string, available *bool)
    Register records an alternative implementation of a cryptographic primitive.
    The implementation might be available or not based on CPU support.
    If available is false, the implementation is unavailable and can't be tested
    on this machine. If available is true, it can be set to false to disable the
    implementation. If all alternative implementations but one are disabled,
    the remaining one must be used (i.e. disabling one implementation must
    not implicitly disable any other). Each package has an implicit base
    implementation that is selected when all alternatives are unavailable
    or disabled. pkg must be the package name, not path (e.g. "aes" not
    "crypto/aes").

func Reset(pkg string)
func Select(pkg, name string) bool
    Select disables all implementations for the given package except the one
    with the given name. If name is empty, the base implementation is selected.
    It returns whether the selected implementation is available.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
