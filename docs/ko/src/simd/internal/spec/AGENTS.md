## spec에 오퍼레이션(operation)을 추가하는 방법

전반적인 안내 사항은 `doc.go`를 읽어보세요.

우리가 추가할 수 있는 모든 연산은 이미 `simd` 또는 `simd/archsimd` 패키지에 정의되어 있습니다. 이를 참조로 사용하십시오. 예를 들어 `GOEXPERIMENT=simd go doc simd ReduceSum` 또는 `GOEXPERIMENT=simd GOARCH=amd64 go doc archsimd MulAdd`를 사용하여 기존 문서를 확인하십시오. 각 연산에 대해 GOARCH amd64, arm64, wasm의 archsimd 문서를 확인하십시오.

함수 선언을 작성할 때, `spec`은 맥시멀리스트(maximalist) 방식임을 유의하십시오. 따라서 연산이 `simd`나 `archsimd`에 나타날 수 있는 타입 너머로 어떻게 일반화될 수 있을지 고려하시기 바랍니다. 예를 들어, `int`에만 적용되는 수치 연산은 종종 `int` 또는 `uint`로 일반화될 수 있습니다. 또한, `float`에 대한 수치 연산 역시 `int`나 `uint`로 일반화될 수 있는 경우가 많지만, 이 경우 복잡한 오버플로(overflow)나 반올림(rounding) 동작이 새로 도입되지 않도록 주의하십시오.

함수 구현의 경우, `simd/simd_emulated.go`와 `simd/archsimd/internal/simd_test`를 참고하십시오. `simd_emulated.go`는 완전히 구체적인 타입(concrete types)을 기반으로 동작하는 반면, spec은 제네릭 타입(generic types)을 기반으로 동작합니다. 일반적으로 float 타입 간 또는 int/uint 타입 간의 일반화는 쉽지만, float와 int/uint 모두를 위해 하나의 구현으로 일반화하는 것은 어려울 수 있습니다. 그런 경우에는 두 개의 구현으로 나누어도 무방합니다 (예를 들어, `AbsFloat`와 `AbsInt`를 참고하십시오).

작업 내용을 확인하기 위해 임시 테스트를 작성할 수 있지만, 그대로 유지하지는 마십시오. 모든 연산을 `spec`에서 테스트하지는 않는데, 이는 결과적으로 하드웨어를 통해 검증될 것이기 때문입니다.

사용자에게 모든 코너 케이스(corner-case) 동작과 이를 어떻게 해결했는지, 그리고 플랫폼 전반에 걸쳐 `simd`와 `archsimd` 사이에서 일관성이 있었는지에 대해 설명하십시오.
