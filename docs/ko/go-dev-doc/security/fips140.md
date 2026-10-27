Go 1.24부터, Go 바이너리는 FIPS 140-3 규정을 준수하도록 지원하는 모드로 원시적으로 작동할 수 있습니다. 또한, Go Cryptographic Module을 구성하는 암호화 패키지의 래핑 버전을 대상으로 빌드할 수 있습니다.

## FIPS 140-3

## 개요

FIPS 140-3 (Federal Information Processing Standards 140-3)은 미국 국립표준기술협회(NIST)에서 개발한 정보보호 기준으로, 암호화 모듈의 보안 요구 사항을 정의합니다. 이 표준은 암호화 모듈이 특정 보안 수준을 충족해야 함을 명시하며, 이를 통해 정부 기관 및 민간 부문에서 사용되는 암호화 모듈의 신뢰성을 확보합니다.

## 주요 내용

*   **보안 수준:** FIPS 140-3은 암호화 모듈의 보안 수준을 3가지로 분류합니다.

    *   **Level 1:** 기본적인 보안 요구 사항을 충족합니다.
    *   **Level 2:** Level 1에 더하여, 모듈에 직접 접근하여 암호 키를 추출하는 것을 방지합니다.
    *   **Level 3:** Level 2에 더하여, 모듈에 대한 물리적 접근을 방지합니다.

*   **테스트:** 암호화 모듈은 NIST에서 정의한 엄격한 테스트를 통과해야 합니다. 이 테스트는 암호화 알고리즘의 강도, 키 관리, 물리적 보안 등을 평가합니다.

*   **보고서:** 테스트 결과를 NIST에 보고해야 하며, 보고서에는 모듈의 보안 수준 및 테스트 결과에 대한 상세 정보가 포함됩니다.

## 적용 분야

FIPS 140-3은 다음과 같은 분야에 적용됩니다.

*   정부 기관
*   금융 기관
*   헬스케어 기관
*   군사 기관

## 관련 링크

*   [NIST FIPS 140-3](https://csrc.nist.gov/fips/140-3)

NIST FIPS 140-3은 암호화
애플리케이션에 대한 미국 정부의 규제 체계로, 여기에는 승인된
알고리즘 집을 사용해야 하는 것 외에도,
[CMVP](https://csrc.nist.gov/projects/cryptographic-module-validation-program)에서 검증된 암호화 모듈을 대상 운영 환경에서 테스트하도록 요구합니다.

이 페이지에 설명된 메커니즘은 Go 애플리케이션의 규정 준수를 용이하게 합니다.

FIPS 140-3 준수가 필요하지 않은 애플리케이션은 이를 무시하고, FIPS 140-3 모드를 활성화할 필요가 없습니다.

**참고:** FIPS 140-3 호환 및 검증된 암호화 모듈을 사용하는 것만으로는—독립적으로—모든 관련 규제 요구 사항을 충족하지 못할 수 있습니다. Go 팀은 제공된 FIPS 140-3 모드의 사용이 특정 규제 요구 사항을 충족하는지 여부에 대한 어떠한 보장이나 지원도 제공할 수 없습니다. 이 모듈의 사용이 귀하의 특정 요구 사항을 충족하는지 신중하게 판단해야 합니다.

## Go 암호화 모듈

```go
package crypto

import (
	"crypto/rand"
	"encoding/base64"
	"fmt"
)

// GenerateRandomString generates a random string of a specified length.
func GenerateRandomString(length int) (string, error) {
	b := make([]byte, length)
	_, err := rand.Read(b)
	if err != nil {
		return "", fmt.Errorf("failed to generate random string: %w", err)
	}
	return string(b), nil
}

// Base64Encode encodes a string using Base64.
func Base64Encode(s string) (string, error) {
	return base64.StdEncoding.EncodeToString([]byte(s)), nil
}

// Base64Decode decodes a Base64 encoded string.
func Base64Decode(s string) (string, error) {
	return base64.StdEncoding.DecodeString(s), nil
}
```

## Usage Examples

```go
package main

import (
	"fmt"
	"your_package/crypto" // Replace with your actual package path
)

func main() {
	// Generate a random string
	randomString, err := crypto.GenerateRandomString(16)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	fmt.Println("Random string:", randomString)

	// Encode a string using Base64
	encodedString, err := crypto.Base64Encode("This is a test string.")
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	fmt.Println("Base64 encoded:", encodedString)

	// Decode a Base64 encoded string
	decodedString, err := crypto.Base64Decode(encodedString)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	fmt.Println("Base64 decoded:", decodedString)
}
```

Go 암호화 모듈은 `crypto/internal/fips140/...` 아래에 있는 표준 라이브러리 Go 패키지의 집합으로, FIPS 140-3에 승인된 알고리즘을 구현합니다.

공개 API 패키지인 `crypto/ecdsa` 및 `crypto/rand`은 Go 암호화 모듈을 사용하여 FIPS 140-3 알고리즘을 구현합니다.

## FIPS 140-3 모드

FIPS 140-3 모드로 작동할 때:

- Go 암호화 모듈은 `init` 시간에 자동으로 무결성 자체 검사를 수행하여, 빌드 시간에 계산된 모듈의 객체 파일의 체크섬을 메모리에 로드된 심볼과 비교합니다.

- 모든 알고리즘은 관련 FIPS 140-3 구현 지침에 따라 알려진 답을 가진 자체 테스트를 수행합니다. 이는 `init` 시점 또는 첫 사용 시점에 수행됩니다.

- 생성된 암호화 키에 대한 쌍별 일관성 테스트가 수행됩니다.
   참고: 특정 키 유형의 경우 최대 2배의 성능 저하가 발생할 수 있으며, 이는 특히 일시적인 키에 특히 관련이 있습니다.

- [`crypto/rand.Reader`](/pkg/crypto/rand/#Reader)는 NIST SP 800-90A DRBG를 기반으로 구현되었습니다. FIPS 140-3 모드로 실행되지 않는 프로그램과 동일한 수준의 보안을 보장하기 위해, `Read` 시마다 플랫폼의 CSPRNG에서 생성된 난수 바이트를 가져와 출력에 추가 데이터를 혼합합니다.

- [`crypto/tls`](/pkg/crypto/tls/) 패키지는 FIPS 140-3에서 승인되지 않은 모든 프로토콜 버전, 암호화 모음, 서명 알고리즘 또는 키 교환 메커니즘을 무시하고 협상하지 않습니다. (이는 기존의 `crypto/tls/fipsonly` Go+BoringCrypto 메커니즘과 동일합니다.)

- [`crypto/rsa.SignPSS`](/pkg/crypto/rsa/#SignPSS)를 사용하여
   [`PSSSaltLengthAuto`](/pkg/crypto/rsa/#PSSSaltLengthAuto)를 지정하면,
   솔트의 길이를 해시의 길이에 제한합니다.

FIPS 140-3 모드는 OpenBSD, Wasm, AIX, 및 32비트 Windows에서는 지원되지 않습니다.

## `crypto/fips140` 패키지

## 개요

이 패키지는 미국 FIPS 140-2 표준을 준수하는 암호화 기능을 제공합니다. FIPS 140-2는 연방 정부 기관에서 사용할 수 있는 암호화 모듈에 대한 요구 사항을 정의합니다.

## 사용법

이 패키지를 사용하려면 먼저 `crypto` 패키지를 가져와야 합니다.

```go
import (
    "crypto/fips140"
)
```

다음은 `fips140` 패키지를 사용하여 암호화 및 복호화를 수행하는 예제 코드입니다.

```go
package main

import (
    "crypto/fips140"
    "fmt"
    "log"
)

func main() {
    // FIPS 140-2 준수 모듈을 초기화합니다.
    // (여기서 실제 FIPS 140-2 준수 모듈 설정이 필요)
    // 예: fips140.New(..., ...)
    // 실제 설정은 FIPS 140-2 준수 모듈에 따라 다릅니다.

    // 예제: Dummy 모듈
    fips, err := fips140.New()
    if err != nil {
        log.Fatal(err)
    }

    // 암호화할 데이터
    plaintext := []byte("This is a secret message.")

    // 암호화 수행
    ciphertext, err := fips.Encrypt(plaintext)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("Ciphertext: %x\n", ciphertext)

    // 복호화 수행
    decryptedText, err := fips.Decrypt(ciphertext)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("Decrypted text: %s\n", decryptedText)
}
```

## 주의사항

*   이 패키지는 FIPS 140-2 표준을 준수하는 실제 FIPS 140-2 준수 모듈을 사용해야 합니다.
*   FIPS 140-2 준수 모듈은 반드시 인증을 받아야 합니다.
*   이 패키지는 예제 코드만 제공하며, 실제 사용 시에는 FIPS 140-2 표준을 준수하는 모듈을 사용해야 합니다.

## 관련 링크

*   [FIPS 140-2](https://csrc.nist.gov/standards/fips/140-2)

[`crypto/fips140.Enabled`](/pkg/crypto/fips140/#Enabled) 함수는 FIPS 140-3 모드가 활성화되어 있는지 여부를 보고합니다.

[`crypto/fips140.Version`](/pkg/crypto/fips140/#Version) 함수는 현재 사용 중인 Go 암호화 모듈의 버전을 반환합니다.

## `GOFIPS140` 환경 변수

이 환경 변수는 특정 지역 또는 국가를 식별하는 데 사용됩니다.

`GOFIPS140` 환경 변수는 `go build`, `go install`,
및 `go test` 명령과 함께 사용되어 실행 파일에 링크될 Go 암호화 모듈의 버전을 선택하고, 기본적으로 FIPS 140-3 모드를 활성화할 수 있습니다.

- `off`는 기본값이며, 표준 라이브러리 트리에 있는 `crypto/internal/fips140/...` 패키지를 사용합니다.

- `latest`는 `off`와 유사하지만, 기본적으로 FIPS 140-3 모드를 활성화합니다.

- `v1.0.0` 또는 `v1.26.0`는 특정 Go 암호화 모듈 버전을 선택합니다. 기본적으로 FIPS 140-3 모드를 활성화합니다.

- `inprocess` 및 `certified`는 각각 [CMVP Modules In Process List][]에 도달한 최신 버전 및 [CMVP validation certificate]를 획득한 최신 버전을 지정하는 것과 동일합니다.

[CMVP 모듈 진행 중 목록]: https://csrc.nist.gov/Projects/cryptographic-module-validation-program/modules-in-process/modules-in-process-list
[CMVP 유효성 검증 인증서]: https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules/search?SearchMode=Basic&ModuleName=Go+Cryptographic+Module&CertificateStatus=Active&ValidationYear=0

## `fips140` GODEBUG 옵션

이 옵션은 FIPS 140 준수를 시뮬레이션하는 데 사용됩니다.

실행 시 `fips140` 옵션 [GODEBUG](/doc/godebug) 은 Go
암호화 모듈이 FIPS 140-3 모드로 작동하는지 제어합니다. 프로그램이 시작된 후에는 변경할 수 없습니다.

기본적으로 `off`로 설정되지만, 빌드 시간에 `GOFIPS140`가 설정되면 `on`으로 설정됩니다.

`on`으로 설정하면 FIPS 140-3 모드가 활성화됩니다. 이는 `GOFIPS140`가 빌드 시간에 설정되지 않았더라도 가능합니다.

만약 `only`로 설정하면, FIPS 140-3 표준을 준수하지 않는 암호화 알고리즘은 오류를 반환하거나 예외를 발생시킵니다. 참고로, 이는 테스트, 평가 및 디버깅을 위한 "최대한의 노력" 모드입니다. *이는 프로덕션 환경에서 사용하도록 설계되지 않았으며*, 보안 정책에 의해 요구되지 않으며, 의도적으로 충돌과 잠재적으로 처리되지 않은 오류를 발생시킬 수 있으며, 오탐 또는 미탐이 발생할 수 있습니다.

대부분의 프로그램은 이 옵션을 직접 설정하는 대신 빌드 시간에 `GOFIPS140`를 사용하는 것이 좋습니다.

## 모듈 버전, 유효성 검사 및 호환성

Google는 현재 [Geomys](https://geomys.org/)와의 계약 관계를 통해 최소 연간 CMVP 검증을 수행합니다.
검증 시, Go 암호화 모듈을 멈추고 새로운 모듈 버전을 생성하여 제출합니다.

이 검증은 광범위한 운영 환경 세트에 대해 테스트되며, 많은 인기 있는 운영 체제 및 하드웨어 플랫폼 조합을 지원합니다.

이전 버전의 Go 암호화 모듈은 더 최신 버전이 CMVP 유효성 검사 인증서를 획득할 때까지 계속 지원되고 사용할 수 있습니다. 더 최신 버전이 CMVP 유효성 검사 인증서를 획득하면 이전 버전은 제거됩니다.

일부 표준 라이브러리 기능이 사용 불가능할 수 있으며, 이전 버전의 Go에서 래핑된 Go 암호화 모듈을 사용하는 경우 오류를 반환할 수 있습니다.

### Go 암호화 모듈 v1.26.0

Go 암호화 모듈 v1.26.0은 2026년 초에 Go 1.26에서 더 이상 업데이트되지 않았습니다.

이 기능은 Go 1.26 이상 버전에서 사용 가능합니다.

2026-04-28 기준으로, CMVP 모듈 프로세스 목록에서 검토 중입니다.
[CAVP 인증서 A8028](https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/details?validation=40638)에 의해 적용됩니다.

#### v1.0.0 대비 변경 사항

- ML-DSA 구현 완료.

- `testing/cryptotest.SetGlobalRandom` 기능이 지원됩니다.

- `crypto/hpke` 및 향후 노출될 API에서 사용하기 위한 새로운 AES-GCM 준수 API를 도입했습니다.

- Go 암호화 모듈은 이제 CPU jitter 엔트로피 소스를 사용하며,
  [ESV 인증서 #E318](https://csrc.nist.gov/projects/cryptographic-module-validation-program/entropy-validations/certificate/318) 및
  [CAVP 인증서 A7715](https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/details?product=20498)를 사용합니다.
  (플랫폼 CSPRNG는 모든 무작위 바이트에 대한 추가적인 데이터 소스로 계속 사용됩니다.)

- 다양한 안전 및 성능 개선 사항.

### Go 암호화 모듈 v1.0.0

```
패키지 이름: cryptography
```

Go 암호화 모듈 v1.0.0은 2024년 초에 Go 1.24에서 사용 불가능 상태로 변경되었습니다.

이것은 Go 1.24 이상 버전에서 사용할 수 있습니다.

이것은 [CMVP 인증서 #5247](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/5247) 및 [CAVP 인증서 A6650](https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/details?product=19371)에 의해 인증되었습니다.

## Go+BoringCrypto

이전, 지원되지 않는 방식으로 BoringCrypto 모듈을 특정 FIPS 140-3 승인 알고리즘에 사용하는 메커니즘은 현재 여전히 사용 가능하지만, 향후 릴리스에서 이 페이지에 설명된 메커니즘으로 대체될 예정입니다.

Go+BoringCrypto는 기본 FIPS 140-3 모드와 호환되지 않습니다.
