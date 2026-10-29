# package crypto/internal/fips140/check/checktest

- 원문: <https://pkg.go.dev/crypto/internal/fips140/check/checktest>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package checktest defines some code and data for use in the crypto/internal/fips140/check test.

## 원문 요약

Package checktest defines some code and data for use in the crypto/internal/fips140/check test.

## API 상세 (go doc -all)

~~~text
package checktest // import "crypto/internal/fips140/check/checktest"

Package checktest defines some code and data for use in the
crypto/internal/fips140/check test.

VARIABLES

var BSS *int
var DATA = struct {
	P *int
	X int
}{&NOPTRDATA, 3}
    DATA needs to have both a pointer and an int so that _some_ of it gets
    initialized at link time, so it is treated as DATA and not BSS. The pointer
    is deferred to init time.

var NOPTRBSS int
var NOPTRDATA int = 1
var RODATA int32 // set to 2 in asm.s
    The linkname here disables asan registration of this global, because asan
    gets mad about rodata globals.


FUNCTIONS

func PtrStaticData() *uint32
func PtrStaticText() unsafe.Pointer
func TEXT()
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
