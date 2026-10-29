# 통합 중간 표현(Unified Intermediate Representation, UIR) 변경하기

UIR 변경 사항을 도입할 때는 신중함이 필요합니다. UIR은 컴파일러 파이프라인의 많은 부분에서 사용되므로, 작은 변경 사항이라도 광범위한 영향(ripple effect)을 미칠 수 있습니다.

## 변경 프로세스

UIR을 변경할 때 권장되는 단계는 다음과 같습니다.

1.  **영향 분석**: 변경하려는 구조가 어디에서 사용되는지 찾습니다. `grep`이나 IDE의 참조 찾기 기능을 사용하여 관련 코드를 식별하십시오.
2.  **작은 단위로 분할**: 가능한 한 변경 사항을 작은, 논리적인 단계로 나누십시오. 한 번에 너무 많은 것을 바꾸면 디버깅이 매우 어려워집니다.
3.  **테스트 케이스 작성**: 변경 전후의 동작을 검증할 수 있는 테스트 케이스를 먼저 작성하십시오.
4.  **점진적 업데이트**:
    *   먼저 UIR 정의를 업데이트합니다.
    *   컴파일 오류가 발생하는 모든 위치를 수정합니다.
    *   각 단계마다 테스트를 실행하여 회귀(regression)가 없는지 확인합니다.

## 일반적인 주의 사항

### 성능 고려 사항
UIR 노드에 새로운 필드를 추가할 때 메모리 사용량을 고려하십시오. 수백만 개의 노드가 생성되는 경우, 필드 하나가 추가됨에 따라 메모리 사용량이 크게 증가할 수 있습니다. 가능하다면 `optional` 필드나 별도의 맵(map) 구조를 사용하십시오.

### 하위 호환성
만약 UIR이 디스크에 직렬화(serialize)되어 저장된다면, 기존에 저장된 파일과의 호환성을 어떻게 유지할지 결정해야 합니다. 버전 관리를 도입하거나 마이그레이션 스크립트를 작성해야 할 수도 있습니다.

## 체크리스트

- [ ] 모든 참조 위치를 업데이트했는가?
- [ ] 관련 최적화 패스(optimization passes)가 여전히 올바르게 작동하는가?
- [ ] 메모리 사용량에 급격한 증가가 없는가?
- [ ] 새로운 테스트 케이스가 추가되었는가?
- [ ] 문서(있는 경우)를 업데이트했는가?

내보내기 데이터에 대한 일반적인 정보는 [여기](../../README.md)를 참조하십시오.

UIR은 컴파일러 중간 표현(intermediate representation)의 직렬화된 형태로, 제네릭 및/또는 인라인 함수(inlined functions)의 본문을 한 컴파일 단위에서 다른 단위로 전파하는 데 사용됩니다.

Go 컴파일러는 `src/cmd/compile/internal/noder/writer.go`에 단일하고 표준적인 UIR writer 구현을 가지고 있습니다. UIR writer가 작성하는 바이트 스트림을 업데이트할 때, *모든* UIR reader를 검토하고 잠재적으로 업데이트해야 합니다. 변경 사항이 reader들과 하위 호환되지 않을 수 있기 때문입니다. 이 지침은 모든 UIR reader를 최신 상태로 유지하는 데 필요한 단계를 설명합니다.

## The Writer

컴파일러가 작성하는 UIR 버전은 `src/cmd/compile/internal/noder/unified.go`에 의해 제어됩니다. 아직 이 부분을 수정하지 마십시오. 대신 다음과 같이 하십시오:

1. `internal/pkgbits/version.go`에서 `MyChange`에 대한 버전 플래그 N+1을 추가합니다.
2. `src/cmd/compile/internal/noder/writer.go`의 UIR writer를 업데이트하여 N+1에서 추가된 모든 필드의 쓰기 작업을 보호(guard)합니다. 참고: 버전 N에 머물러 있는 reader들이 제출 시 깨지는 것을 방지하려면, 이 변경 사항을 *절대로* 인지해서는 안 됩니다.

## 독자 (The Readers)

컴파일러 자체 외에도 `go`, `x/tools` 및 외부에는 다른 리더(reader)들이 존재합니다. `x/tools`와 일반 대중을 위한 리더가 존재하는 이유는 `go list -export`가 이 형식의 export 데이터 파일을 생성하며, 우리가 애플리케이션이 이를 디코딩할 수 있는 기능을 지원하기 때문입니다.

> `go list -export`에 의해 인코딩되는 형식을 변경하여 컴파일러의 IR을 x/tools에서 분리하려는 향후 계획이 있음에 유의하십시오. 이렇게 되면 UIR은 컴파일러의 내부 상세 구현이 되어 언제든지 변경될 수 있게 됩니다. 현재로서는 여전히 이 지침들을 따라야 합니다.

외부 리더(reader)들은 자체적으로 업데이트할 것으로 가정합니다. `go` 및 `x/tools`에서 필요한 리더 업데이트 사항은 아래에 자세히 설명되어 있습니다.

### go

3. `src/cmd/compile/internal/noder/reader.go`에 있는 컴파일러 자체의 UIR reader를 업데이트하여 N+1에서 추가된 모든 필드의 읽기 동작을 보호(guard)하십시오.
4. `src/go/internal/gcimporter/ureader.go` 및 `src/cmd/compile/internal/importer/ureader.go`에 있는 reader들에 대해서도 이 변경 사항을 반복하십시오. 이 reader들은 타입 체크에 필요한 데이터만 읽는다는 점에 유의하십시오 (각각 `src/go/types` 및 `src/cmd/compile/internal/types2`에서 사용). 예를 들어, 이들은 export된 함수 본문(function bodies)을 읽지 않습니다. 따라서 UIR의 변경 사항(함수 본문의 인코딩 등)이 발생하더라도 이 reader들에는 변경이 필요 없을 수 있습니다.

### x/tools

5. `internal/pkgbits/version.go`에 `MyChange`를 위한 버전 플래그를 추가합니다. 참고:
   x/tools는 자체적인 pkgbits 구현체를 가지고 있으며, 이는 [go에 있는 것](#the-writer)과 정확히 일치하도록 설계되었습니다. 어느 한 쪽에서 변경 사항이 발생하면 반드시 다른 쪽에도 반영되어야 합니다.
6. `internal/gcimporter/ureader.go`에 있는 x/tools UIR 리더를 업데이트하여 N+1에서 추가된 모든 필드의 읽기 작업을 보호(guard)합니다. 이 커밋을 C라고 부릅니다.
7. go에서, C의 커밋 해시를 가져와 [벤더링 지침](https://go.dev/wiki/MinorReleases#cherry-pick-cls-for-vendored-golangorgx-packages)에 따라 `src/cmd/go.mod`가 x/tools@C를 사용하도록 업데이트합니다.

## 마무리하기

> 이 UIR 변경 사항이 테스트될 예정이라면, [다음 섹션](#testing)을 확인하고 언제 마무리하는 것이 적절할지 고려하십시오.

모든 reader를 검토한 후에만, `src/cmd/compile/internal/noder/unified.go`에 작성된 writer의 UIR 버전을 N+1로 올리십시오. reader들이 이미 버전 N+1을 처리하도록 업데이트되었으므로, 이 변경 사항은 호환됩니다.

## 테스트(Testing)

광범위한 테스트가 필요한 새로운 기능과 관련하여 변경 사항을 만드는 경우, *모든* 테스트가 완료될 때까지 UIR 버전을 올리는 것을 미루는 것이 가장 좋습니다. 테스트를 점진적으로 커밋하려면, 로컬에서만 증가시킨 UIR 버전으로 테스트를 개발하고 *skipped* 상태의 테스트를 커밋하십시오. 아직 원격 UIR 버전은 올리지 마십시오.

필요한 모든 테스트가 완료되면, 이전에 건너뛴 모든 테스트를 활성화하면서 원격 UIR 버전을 올리십시오. 이렇게 하면 테스트를 통해 불일치 사항이 발견됨에 따라 발생하는 UIR 버전의 잦은 변경(churn)을 최소화할 수 있습니다.
