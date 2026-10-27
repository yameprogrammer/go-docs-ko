# package internal/byteorder

- 원문: <https://pkg.go.dev/internal/byteorder>
- 분류: Go 표준 라이브러리

## 한국어 요약

`byteorder` 패키지는 바이트 슬라이스로부터 리틀 엔디안(little endian) 및 빅 엔디안(big endian) 정수 타입을 디코딩하고 인코딩하는 함수들을 제공합니다.

## 원문 요약

Package byteorder provides functions for decoding and encoding little and big endian integer types from/to byte slices.

## API 상세 (go doc -all)

~~~text
package byteorder // import "internal/byteorder"

Package byteorder provides functions for decoding and encoding little and big
endian integer types from/to byte slices.

FUNCTIONS

func BEAppendUint16(b []byte, v uint16) []byte
func BEAppendUint32(b []byte, v uint32) []byte
func BEAppendUint64(b []byte, v uint64) []byte
func BEPutUint16(b []byte, v uint16)
func BEPutUint32(b []byte, v uint32)
func BEPutUint64(b []byte, v uint64)
func BEUint16(b []byte) uint16
func BEUint32(b []byte) uint32
func BEUint64(b []byte) uint64
func LEAppendUint16(b []byte, v uint16) []byte
func LEAppendUint32(b []byte, v uint32) []byte
func LEAppendUint64(b []byte, v uint64) []byte
func LEPutUint16(b []byte, v uint16)
func LEPutUint32(b []byte, v uint32)
func LEPutUint64(b []byte, v uint64)
func LEUint16(b []byte) uint16
func LEUint32(b []byte) uint32
func LEUint64(b []byte) uint64
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
