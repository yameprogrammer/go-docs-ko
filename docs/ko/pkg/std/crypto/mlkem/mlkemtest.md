# package crypto/mlkem/mlkemtest

- 원문: <https://pkg.go.dev/crypto/mlkem/mlkemtest>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `mlkemtest`는 ML-KEM 알고리즘에 대한 테스트 함수를 제공합니다.

## 원문 요약

Package mlkemtest provides testing functions for the ML-KEM algorithm.

## API 상세 (go doc -all)

~~~text
package mlkemtest // import "crypto/mlkem/mlkemtest"

Package mlkemtest provides testing functions for the ML-KEM algorithm.

FUNCTIONS

func Encapsulate1024(ek *mlkem.EncapsulationKey1024, random []byte) (sharedKey, ciphertext []byte, err error)
    Encapsulate1024 implements derandomized ML-KEM-1024 encapsulation
    (ML-KEM.Encaps_internal from FIPS 203) using the provided encapsulation key
    ek and 32 bytes of randomness.

    It must only be used for known-answer tests.

func Encapsulate768(ek *mlkem.EncapsulationKey768, random []byte) (sharedKey, ciphertext []byte, err error)
    Encapsulate768 implements derandomized ML-KEM-768 encapsulation
    (ML-KEM.Encaps_internal from FIPS 203) using the provided encapsulation key
    ek and 32 bytes of randomness.

    It must only be used for known-answer tests.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
