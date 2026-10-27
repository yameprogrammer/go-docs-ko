# package crypto/internal/fips140deps/cpu

- 원문: <https://pkg.go.dev/crypto/internal/fips140deps/cpu>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package cpu // import "crypto/internal/fips140deps/cpu"


CONSTANTS

const (
	BigEndian = goarch.BigEndian
	AMD64     = goarch.IsAmd64 == 1
	ARM64     = goarch.IsArm64 == 1
	PPC64     = goarch.IsPpc64 == 1
	PPC64le   = goarch.IsPpc64le == 1
)

VARIABLES

var (
	ARM64HasAES    = cpu.ARM64.HasAES
	ARM64HasPMULL  = cpu.ARM64.HasPMULL
	ARM64HasSHA2   = cpu.ARM64.HasSHA2
	ARM64HasSHA512 = cpu.ARM64.HasSHA512
	ARM64HasSHA3   = cpu.ARM64.HasSHA3

	LOONG64HasLSX  = cpu.Loong64.HasLSX
	LOONG64HasLASX = cpu.Loong64.HasLASX

	RISCV64HasV = cpu.RISCV64.HasV

	S390XHasAES    = cpu.S390X.HasAES
	S390XHasAESCBC = cpu.S390X.HasAESCBC
	S390XHasAESCTR = cpu.S390X.HasAESCTR
	S390XHasAESGCM = cpu.S390X.HasAESGCM
	S390XHasECDSA  = cpu.S390X.HasECDSA
	S390XHasGHASH  = cpu.S390X.HasGHASH
	S390XHasSHA256 = cpu.S390X.HasSHA256
	S390XHasSHA3   = cpu.S390X.HasSHA3
	S390XHasSHA512 = cpu.S390X.HasSHA512

	X86HasAES       = cpu.X86.HasAES
	X86HasADX       = cpu.X86.HasADX
	X86HasAVX       = cpu.X86.HasAVX
	X86HasAVX2      = cpu.X86.HasAVX2
	X86HasBMI2      = cpu.X86.HasBMI2
	X86HasPCLMULQDQ = cpu.X86.HasPCLMULQDQ
	X86HasSHA       = cpu.X86.HasSHA
	X86HasSSE41     = cpu.X86.HasSSE41
	X86HasSSSE3     = cpu.X86.HasSSSE3
)
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
