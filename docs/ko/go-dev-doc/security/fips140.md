Go 1.24부터 Go 바이너리는 FIPS 140-3 준수를 용이하게 하는 모드로 네이티브하게 동작할 수 있습니다. 또한, 툴체인은 Go Cryptographic Module을 구성하는 cryptography 패키지들의 동결된(frozen) 버전을 대상으로 빌드할 수 있습니다.

## FIPS 140-3

NIST FIPS 140-3는 암호화 애플리케이션을 위한 미국 정부의 컴플라이언스 체계로, 무엇보다 승인된 알고리즘 세트의 사용과 대상 운영 환경에서 테스트되어 [CMVP](https://csrc.nist.gov/projects/cryptographic-module-validation-program) 검증을 받은 암호화 모듈의 사용을 요구합니다.

이 페이지에서 설명하는 메커니즘은 Go 애플리케이션의 컴플라이언스 준수를 용이하게 합니다.

FIPS 140-3 준수가 필요하지 않은 애플리케이션은 이를 안전하게 무시할 수 있으며, FIPS 140-3 모드를 활성화하지 않아야 합니다.

**참고:** 단순히 FIPS 140-3를 준수하고 검증된 암호화 모듈을 사용하는 것만으로는 관련 규제 요구 사항을 모두 충족하지 못할 수 있습니다. Go 팀은 제공된 FIPS 140-3 모드 사용이 개별 사용자의 특정 규제 요구 사항을 충족하는지 여부에 대해 어떠한 보장이나 지원도 제공할 수 없습니다. 본 모듈의 사용이 귀하의 특정 요구 사항을 충족하는지 결정할 때 주의를 기울여야 합니다.

## Go 암호화 모듈 (The Go Cryptographic Module)

Go 암호화 모듈(Cryptographic Module)은 FIPS 140-3 승인 알고리즘을 구현하는 `crypto/internal/fips140/...` 하위의 Go 표준 라이브러리 패키지 모음입니다.

`crypto/ecdsa` 및 `crypto/rand`와 같은 공용 API 패키지는 Go Cryptographic Module을 투명하게 사용하여 FIPS 140-3 알고리즘을 구현합니다.

## FIPS 140-3 모드

FIPS 140-3 모드로 작동할 때:

- Go Cryptographic Module은 `init` 시점에 자동으로 무결성 자가 점검을 수행하며, 빌드 시점에 계산된 모듈 객체 파일의 체크섬을 메모리에 로드된 심볼과 비교합니다.

- 모든 알고리즘은 관련 FIPS 140-3 구현 가이드라인(Implementation Guidance)에 따라 `init` 시점 또는 최초 사용 시에 기지 응답 자체 테스트(known-answer self-tests)를 수행합니다.

- 생성된 암호화 키에 대해 쌍별 일관성 테스트(Pairwise consistency tests)가 수행됩니다.
   이로 인해 특정 키 유형의 경우 최대 2배까지 속도가 느려질 수 있으며, 이는 특히 임시 키(ephemeral keys)에서 두드러집니다.

- [`crypto/rand.Reader`](/pkg/crypto/rand/#Reader)는 NIST SP 800-90A DRBG를 기반으로 구현되었습니다. FIPS 140-3 모드에서 실행되지 않는 프로그램과 동일한 수준의 보안을 보장하기 위해, 매 `Read`마다 플랫폼의 CSPRNG로부터 랜덤 바이트를 추가로 가져와 이를 신뢰할 수 없는 추가 데이터(uncredited additional data)로 출력값에 혼합합니다.

- [`crypto/tls`](/pkg/crypto/tls/) 패키지는 FIPS 140-3 승인을 받지 않은 프로토콜 버전, 사이퍼 스위트(cipher suite), 서명 알고리즘 또는 키 교환 메커니즘을 무시하며 협상하지 않습니다. (이는 기존의 선택적 적용 방식인 `crypto/tls/fipsonly` Go+BoringCrypto 메커니즘과 동일합니다.)

- [`crypto/rsa.SignPSS`](/pkg/crypto/rsa/#SignPSS)에서 [`PSSSaltLengthAuto`](/pkg/crypto/rsa/#PSSSaltLengthAuto)를 사용하면 솔트(salt)의 길이가 해시의 길이로 제한됩니다.

FIPS 140-3 모드는 OpenBSD, Wasm, AIX 및 32비트 Windows에서 지원되지 않습니다.

## `crypto/fips140` 패키지

[`crypto/fips140.Enabled`](/pkg/crypto/fips140/#Enabled) 함수는 FIPS 140-3 모드가 활성화되어 있는지 여부를 보고합니다.

[`crypto/fips140.Version`](/pkg/crypto/fips140/#Version) 함수는 사용 중인 Go Cryptographic Module의 버전을 반환합니다.

## `GOFIPS140` 환경 변수

`GOFIPS140` 환경 변수는 `go build`, `go install`, `go test`와 함께 사용하여 실행 프로그램에 링크될 Go Cryptographic Module의 버전을 선택하고, 기본적으로 FIPS 140-3 모드를 활성화하는 데 사용할 수 있습니다.

- `off`가 기본값이며, 사용 중인 표준 라이브러리 트리의 `crypto/internal/fips140/...` 패키지를 사용합니다.

- `latest`는 `off`와 유사하지만, 기본적으로 FIPS 140-3 모드를 활성화합니다.

- `v1.0.0` 또는 `v1.26.0`은 각각 특정 Go Cryptographic Module 버전을 선택합니다. 이 버전들은 기본적으로 FIPS 140-3 모드를 활성화합니다.

- `inprocess`와 `certified`는 각각 [CMVP Modules In Process List][]에 도달한 최신 버전과 [CMVP validation certificate][]를 획득한 최신 버전을 지정하는 것과 동일합니다.

[CMVP Modules In Process List]: https://csrc.nist.gov/Projects/cryptographic-module-validation-program/modules-in-process/modules-in-process-list
[CMVP validation certificate]: https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules/search?SearchMode=Basic&ModuleName=Go+Cryptographic+Module&CertificateStatus=Active&ValidationYear=0

## `fips140` GODEBUG 옵션

런타임 `fips140` [GODEBUG](/doc/godebug) 옵션은 Go 암호화 모듈이 FIPS 140-3 모드로 동작할지 여부를 제어합니다. 이 옵션은 프로그램이 시작된 후에는 변경할 수 없습니다.

빌드 시점에 `GOFIPS140`이 설정되지 않은 한, 기본값은 `off`입니다.

`on`으로 설정하면 FIPS 140-3 모드가 활성화됩니다. 이는 빌드 시에 `GOFIPS140`이 설정되지 않았더라도 가능합니다.

`only`로 설정하면 FIPS 140-3를 준수하지 않는 암호화 알고리즘은 에러를 반환하거나 패닉(panic)을 일으킵니다. 이 모드는 테스트, 평가 및 디버깅을 위한 최선 노력(best effort) 모드임을 유의하십시오. *운영 환경에서 사용하도록 설계되지 않았으며*, 보안 정책(Security Policy)에서 요구하는 사항이 아닙니다. 또한 설계상 의도적으로 크래시 및 처리되지 않은 에러를 발생시킬 수 있으며, 오탐(false positives)이나 미탐(false negatives)이 발생할 수 있습니다.

대부분의 프로그램은 이 옵션을 직접 설정해서는 안 되며, 대신 빌드 시에 `GOFIPS140`을 사용해야 합니다.

## 모듈 버전, 검증 및 호환성

Google은 현재 Go 암호화 모듈(Go Cryptographic Module)의 CMVP 검증을 최소 매년 수행하기 위해 [Geomys](https://geomys.org/)와 계약 관계를 맺고 있습니다. 검증 시점에 Go 암호화 모듈을 동결하고, 제출을 위한 새로운 모듈 버전을 생성할 예정입니다.

이러한 검증은 다양한 인기 운영 체제와 하드웨어 플랫폼 조합을 지원하는 포괄적인 운영 환경 세트에서 테스트됩니다.

이전 버전의 Go 암호화 모듈은 더 최신 버전이 CMVP 검증 인증서를 획득하기 전까지 계속 지원되며 제공됩니다. 더 최신 버전이 CMVP 검증 인증서를 획득하면, 이전 버전들은 제거됩니다.

이전 버전의 Go에서 동결(frozen)된 Go Cryptographic Module을 사용하는 경우, 일부 표준 라이브러리 기능이 제공되지 않거나 에러를 반환할 수 있습니다.

### Go Cryptographic Module v1.26.0

Go Cryptographic Module v1.26.0는 2026년 초 Go 1.26에서 동결되었습니다.

Go 1.26+ 버전에서 사용할 수 있습니다.

2026-04-28 기준, 이 모듈은 CMVP Modules In Process List에서 Pending Review 상태입니다.
이 모듈은 [CAVP Certificate A8028](https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/details?validation=40638)에 의해 커버됩니다.

#### v1.0.0에서의 변경 사항

- ML-DSA를 구현했습니다.

- [testing/cryptotest.SetGlobalRandom](/pkg/testing/cryptotest#SetGlobalRandom)이 이제 지원됩니다.

- `crypto/hpke` 및 향후 공개될 API에서 사용할 새로운 AES-GCM 준수(compliance) API를 도입했습니다.

- Go 암호화 모듈은 이제 [ESV Certificate #E318](https://csrc.nist.gov/projects/cryptographic-module-validation-program/entropy-validations/certificate/318) 및 [CAVP Certificate A7715](https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/details?product=20498)를 통해 검증된 CPU jitter 엔트로피 소스를 사용합니다.
  (플랫폼 CSPRNG는 여전히 모든 랜덤 바이트에 대해 인증되지 않은 추가 데이터 소스로 사용됩니다.)

- 다양한 안전 및 성능 개선 사항.

### Go 암호화 모듈 v1.0.0

Go Cryptographic Module v1.0.0은 2024년 초 Go 1.24부터 동결되었습니다.

Go 1.24+ 버전에서 사용할 수 있습니다.

이는 [CMVP Certificate #5247](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/5247) 및 [CAVP Certificate A6650](https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/details?product=19371)에 의해 인증되었습니다.

## Go+BoringCrypto

특정 FIPS 140-3 승인 알고리즘에 대해 BoringCrypto 모듈을 사용하던 이전의 지원되지 않는 메커니즘은 현재 여전히 사용할 수 있지만, 향후 릴리스에서 제거되고 이 페이지에 설명된 메커니즘으로 대체될 예정입니다.

Go+BoringCrypto는 네이티브 FIPS 140-3 모드와 호환되지 않습니다.
