## 개요

이 문서는 Go 툴체인 및 표준 라이브러리에 대한 일반적인 위협 모델을 정의합니다. 패키지 문서에 정의된 위협 모델이 없는 경우, 이 문서에 설명된 모델이 표준 라이브러리의 모든 패키지에 적용되는 것으로 간주해야 합니다.

### 위협 모델 (Threat Model)

#### 빌드 안전성 (Build Safety)

Go 코드를 빌드하는 것은 안전한 것으로 간주되며, 예기치 않은 실행과 같은 부작용이 없어야 합니다.

#### 런타임 실행

일반적으로 당사는 악성 코드의 실행을 관련 보안 문제로 간주하지 않습니다. Go에 익숙한 사용자는 자신이 무엇을 실행하고 있는지 이해하고 있다고 가정합니다.

#### 메모리 안전성 (Memory Safety)

`unsafe` 패키지를 사용하지 않는 한, 메모리 안전성은 런타임에 의해 보장되는 것으로 간주됩니다.

#### 신뢰 경계 (Trust Boundaries)

임의의 사용자 제공 입력을 수락할 것으로 합리적으로 예상되는 API는 패닉(panic) 및 임의의 리소스 소비에 대해 하드닝(hardening) 처리가 되어 있는 것으로 간주합니다.

API에 쓰레기 값(garbage)을 전달하여 예상치 못한 결과가 발생하는 것은 보안 문제로 간주되지 않습니다.

#### 환경 제어

로컬 시스템은 안전하다고 가정합니다. OS가 이미 침해된 상태에 의존하는 공격은 관련이 없는 것으로 간주합니다. 예를 들어, 공격자가 파일 시스템, `PATH`와 같은 환경 변수를 제어하거나 메모리 접근 및 제어권을 갖는 것은 본 모델의 범위에 포함되지 않습니다.

### 자체 모델을 보유한 패키지들

* [encoding/json](/pkg/encoding/json/#hdr-Security_Considerations)
* [encoding/json/v2](/pkg/encoding/json/v2/#hdr-Security_Considerations)
* [encoding/json/jsontext](/pkg/encoding/json/jsontext/#hdr-Security_Considerations)
* [encoding/gob](/pkg/encoding/gob/#hdr-Security)
* [html/template](/pkg/html/template/#hdr-Security_Model)
* [image](/pkg/image/#hdr-Security_Considerations)
* [debug/pe](/pkg/debug/pe/#hdr-Security)
* [debug/macho](/pkg/debug/macho/#hdr-Security)
* [debug/dwarf](/pkg/debug/dwarf/#hdr-Security)
* [debug/plan9obj](/pkg/debug/plan9obj/#hdr-Security)
* [debug/elf](/pkg/debug/elf/#hdr-Security)
