# 통합 중간 표현(Unified Intermediate Representation, UIR) 변경하기

내보내기 데이터에 대한 일반적인 정보는 [여기](../../README.md)를 참조하십시오.

UIR은 컴파일러 중간 표현(intermediate representation)의 직렬화된 형태로, 제네릭 및/또는 인라인 함수 본문을 한 컴파일 단위에서 다른 단위로 전파하는 데 사용됩니다.

Go 컴파일러는 `src/cmd/compile/internal/noder/writer.go`에 단일하고 표준적인 UIR writer 구현체를 가지고 있습니다. UIR writer가 작성하는 바이트 스트림을 업데이트할 때, *모든* UIR reader를 검토하고 잠재적으로 업데이트해야 합니다. 변경 사항이 reader들과 하위 호환되지 않을 수 있기 때문입니다. 이 지침은 모든 UIR reader를 최신 상태로 유지하기 위해 필요한 단계들을 설명합니다.

## The Writer

컴파일러가 작성하는 UIR 버전은 `src/cmd/compile/internal/noder/unified.go`에서 제어됩니다. 아직 이 부분을 수정하지 마십시오. 대신 다음과 같이 진행하십시오:

1. `internal/pkgbits/version.go`에서 `MyChange`에 대한 버전 플래그 N+1을 추가합니다.
2. `src/cmd/compile/internal/noder/writer.go`의 UIR writer를 업데이트하여 N+1에서 추가된 모든 필드의 쓰기 작업을 보호(guard)합니다. 참고: 버전 N을 사용하는 reader는 제출 시 reader가 손상되는 것을 방지하기 위해 이 변경 사항을 *반드시* 인지하지 못해야(oblivious) 합니다.

## 독자 (The Readers)

컴파일러 자체 외에도 go, x/tools 및 외부에서 이를 읽는 다른 리더들이 있습니다. x/tools와 일반 대중을 위한 리더들이 존재하는 이유는 `go list -export`가 이 형식의 export 데이터 파일을 생성하며, 저희가 애플리케이션에서 이를 디코딩할 수 있는 기능을 지원하기 때문입니다.

> `go list -export`에 의해 인코딩되는 형식을 변경하여 컴파일러의 IR을 x/tools에서 분리하려는 향후 계획이 있음에 유의하십시오. 이렇게 되면 UIR은 컴파일러의 내부 상세 구현(private detail)이 되어 언제든지 변경될 수 있게 됩니다. 현재로서는 여전히 이 지침들을 따라야 합니다.

외부 리더(reader)들은 자체적으로 업데이트될 것으로 가정합니다. `go` 및 `x/tools`에서 필요한 리더 업데이트 사항은 아래에 자세히 설명되어 있습니다.

### go

3. `src/cmd/compile/internal/noder/reader.go`에 있는 컴파일러 자체의 UIR reader를 업데이트하여, N+1에서 추가된 모든 필드의 읽기 작업을 보호(guard)하십시오.
4. `src/go/internal/gcimporter/ureader.go`와 `src/cmd/compile/internal/importer/ureader.go`에 있는 reader들에 대해서도 이 변경 사항을 반복하십시오. 이 reader들은 타입 체크에 필요한 데이터만 읽는다는 점에 유의하십시오 (각각 `src/go/types`와 `src/cmd/compile/internal/types2`에서 사용됨). 예를 들어, 이들은 내보내기(exported)된 함수 본문을 읽지 않습니다. 따라서 UIR의 변경 사항(함수 본문의 인코딩 등)이 이러한 reader들의 변경을 필요로 하지 않을 수도 있습니다.

### x/tools

5. `internal/pkgbits/version.go`에 `MyChange`를 위한 버전 플래그를 추가합니다. 참고:
   x/tools는 자체적인 pkgbits 구현을 가지고 있으며, 이는 [go에 있는 것](#the-writer)과 정확히 동일한 복사본이어야 합니다. 어느 한쪽에 변경 사항이 생기면 반드시 다른 쪽에도 반영되어야 합니다.
6. `internal/gcimporter/ureader.go`에 있는 x/tools UIR reader를 업데이트하여 N+1에서 추가된 필드의 읽기 작업을 보호(guard)하도록 합니다. 이 커밋을 C라고 부릅니다.
7. go에서, C의 커밋 해시를 가져와 [벤더링 지침](https://go.dev/wiki/MinorReleases#cherry-pick-cls-for-vendored-golangorgx-packages)에 따라 `src/cmd/go.mod`가 x/tools@C를 사용하도록 업데이트합니다.

## 마무리하기

> 만약 이 UIR 변경 사항이 테스트될 예정이라면, [다음 섹션](#testing)을 확인하고
> 언제 마무리하는 것이 적절할지 고려하십시오.

*모든* reader를 검토한 후에만, `src/cmd/compile/internal/noder/unified.go`에 작성된 writer의 UIR 버전을 N+1로 올리십시오. reader들이 이미 버전 N+1을 처리하도록 업데이트되었으므로, 이 변경 사항은 호환됩니다.

## 테스트

광범위한 테스트가 필요한 새로운 기능과 관련된 변경 사항을 적용하는 경우, *모든* 테스트가 완료될 때까지 UIR 버전을 올리는 것을 미루는 것이 가장 좋습니다. 테스트를 점진적으로 커밋하려면, 로컬에서만 증가시킨 UIR 버전으로 테스트를 개발하고 *skipped* 테스트 상태로 커밋하십시오. 원격 UIR 버전은 아직 올리지 마십시오.

필요한 모든 테스트가 완료되면, 이전에 건너뛰었던 모든 테스트를 활성화하면서 원격 UIR 버전을 올리십시오. 이렇게 하면 테스트를 통해 불일치 사항이 발견됨에 따라 UIR 버전의 변경 횟수(churn)를 최소화할 수 있습니다.
