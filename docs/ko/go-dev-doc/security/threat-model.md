---
제목: Go 위협 모델
레이아웃: 기사
내비게이션: true

## 개요

이 문서는 Go 도구 체인 및 표준 라이브러리에 대한 일반적인 위협 모델을 정의합니다. 패키지 문서가 위협 모델을 정의하지 않는 경우, 이 문서에 설명된 모델은 표준 라이브러리의 모든 패키지에 적용된다고 가정합니다.

### 위협 모델

#### 안전 빌드

Go 코드 빌드 과정은 안전하다고 가정하며, 예기치 않은 실행과 같은 부작용이 없어야 합니다.

#### 런타임 실행

일반적으로 악성 코드 실행을 보안 문제로 간주하지 않습니다. Go에 익숙한 사용자는 자신이 실행하는 코드가 무엇인지 이해한다고 가정합니다.

#### 메모리 안전성

다음과 같이 가정합니다. `unsafe` 패키지를 사용하지 않는 경우, 런타임 환경이 메모리 안전성을 보장합니다.

#### 신뢰 영역

API는 사용자가 제공하는 임의의 입력을 수락할 것으로 예상되므로, 다음과 같은 사항에 대해 보호되어 있다고 가정합니다:

*   예상치 못한 오류(panics) 방지
*   자원 소비 제한

API에 불필요한 데이터를 전달하여 예상치 못한 결과를 얻는 것은 보안 문제로 간주되지 않습니다.

#### 환경 제어

다음과 같이 가정합니다. 로컬 시스템이 안전하다고 가정합니다. 이미 운영체제가 손상된 경우에 의존하는 공격은 관련이 없습니다. 예를 들어, 파일 시스템, 환경 변수(예: PATH), 메모리 접근 또는 제어를 통한 공격은 우리의 모델에 포함되지 않습니다.

### 자체 모델을 가진 패키지

* [encoding/json](/pkg/encoding/json/#hdr-보안_고려사항)
* [encoding/json/v2](/pkg/encoding/json/v2/#hdr-보안_고려사항)
* [encoding/json/jsontext](/pkg/encoding/json/jsontext/#hdr-보안_고려사항)
* [encoding/gob](/pkg/encoding/gob/#hdr-보안)
* [html/template](/pkg/html/template/#hdr-보안_모델)
* [image](/pkg/image/#hdr-보안_고려사항)
* [debug/pe](/pkg/debug/pe/#hdr-보안)
* [debug/macho](/pkg/debug/macho/#hdr-보안)
* [debug/dwarf](/pkg/debug/dwarf/#hdr-보안)
* [debug/plan9obj](/pkg/debug/plan9obj/#hdr-보안)
* [debug/elf](/pkg/debug/elf/#hdr-보안)
