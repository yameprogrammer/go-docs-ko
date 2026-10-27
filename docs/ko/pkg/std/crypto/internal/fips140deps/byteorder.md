# package crypto/internal/fips140deps/byteorder

- 원문: <https://pkg.go.dev/crypto/internal/fips140deps/byteorder>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package byteorder // import "crypto/internal/fips140deps/byteorder"


FUNCTIONS

func BEAppendUint16(b []byte, v uint16) []byte
func BEAppendUint32(b []byte, v uint32) []byte
func BEAppendUint64(b []byte, v uint64) []byte
func BEPutUint16(b []byte, v uint16)
func BEPutUint32(b []byte, v uint32)
func BEPutUint64(b []byte, v uint64)
func BEUint32(b []byte) uint32
func BEUint64(b []byte) uint64
func LEPutUint16(b []byte, v uint16)
func LEPutUint64(b []byte, v uint64)
func LEUint16(b []byte) uint16
func LEUint64(b []byte) uint64
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
