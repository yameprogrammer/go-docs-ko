Go 1.27에서 도입된 [encoding/json/v2](/pkg/encoding/json/v2) 패키지는 기존 [encoding/json](/pkg/encoding/json) 패키지를 대폭 수정하여 만든 버전입니다.
이 가이드는 왜 v1에서 v2 패키지로 마이그레이션해야 하는지와 이를 안전하게 수행하는 방법에 대해 설명합니다.

# 왜 마이그레이션해야 하는가?

가장 먼저 말씀드릴 점은, 반드시 하실 필요는 없다는 것입니다!
`encoding/json` 패키지는 사라지지 않습니다.
이 패키지는 Go 1 호환성 약속(compatibility promise)의 적용을 받으므로, `encoding/json`을 사용하는 패키지들은 앞으로도 계속해서 정상적으로 작동할 것입니다.

또한, `encoding/json`과 `encoding/json/v2`는 서로 호환됩니다.
예를 들어, 어떤 타입이 [`encoding/json/v2.MarshalerTo`](/pkg/encoding/json/v2#MarshalerTo)를 통해 커스텀 마샬링 동작을 구현한 경우, [`encoding/json.Marshal`](/pkg/encoding/json#Marshal)을 통해 이 타입을 마샬링하는 호출자도 여전히 해당 커스텀 마샬러를 거치게 됩니다.
마찬가지로, `encoding/json/v2`와 함께 Go 1.27에서 도입된 새로운 `json` 구조체 태그 또한 `encoding/json`에서 지원됩니다.

마이그레이션이 필수 사항은 아니지만, 그렇게 해야 할 몇 가지 타당한 이유가 있습니다:

우선, 새로운 API는 사용하기 더 쉽습니다.
예를 들어, [`encoding/json.Encoder`](/pkg/encoding/json#Encoder)가 필요했던 이전과 달리, [`encoding/json/v2.MarshalWrite`](/pkg/encoding/json/v2#MarshalWrite)를 사용하여 [`io.Writer`](/pkg/io#Writer)로 쉽게 마샬링(marshal)할 수 있습니다.
[`encoding/json/v2.Marshalers`](/pkg/encoding/json/v2#Marshalers)를 사용하면 직접 제어할 수 없는 타입이라 하더라도 특정 타입의 마샬링 동작을 오버라이드할 수 있습니다.
[`encoding/json/v2.MatchCaseInsenstiveNames`](/pkg/encoding/json/v2#MatchCaseInsenstiveNames)를 통해 JSON 객체의 멤버 이름과 Go 구조체 필드를 매칭할 때의 대소문자 구분 여부를 제어할 수 있습니다.

이러한 개선 사항들도 좋지만, 마이그레이션을 해야 하는 가장 큰 이유는 v2 패키지가 v1보다 더 엄격하고 상호 운용성이 높은 기본값을 선택했다는 점입니다. [`encoding/json` 문서](/pkg/encoding/json#hdr-Migrating_to_v2)에 전체 차이점이 설명되어 있으며, 주요 내용은 다음과 같습니다.

* v1에서는 문자열 내의 잘못된 UTF-8 바이트가 유니코드 대체 문자로 조용히 대체됩니다. 반면, v2에서는 잘못된 UTF-8이 존재할 경우 에러가 발생합니다.
* v1에서는 중복된 이름이 있는 JSON 객체가 허용됩니다. 반면, v2에서는 중복된 이름이 있는 JSON 객체가 있을 경우 에러가 발생합니다.
* v1에서는 nil Go 슬라이스나 Go 맵이 JSON null로 마샬링됩니다. 반면, v2에서는 nil Go 슬라이스나 Go 맵을 각각 빈 JSON 배열이나 JSON 객체로 마샬링합니다.
* v1에서는 구조적 에러(예: 잘못된 필드 태그)가 있는 Go 구조체 타입에 대해 런타임에 에러를 보고하지 않습니다. 반면, v2에서는 JSON 직렬화와 관련하여 유효하지 않은 Go 타입에 대해 런타임 에러를 보고합니다.

이러한 변경 사항들은 `encoding/json/v2`가 더 넓은 JSON 생태계와 더 잘 상호 운용되고, 예측 가능하며, 오류가 적도록 설계되었습니다.
하지만 이는 하위 호환성을 유지하지 않습니다. 일부 애플리케이션은 v1의 동작 방식에 의존하고 있을 수 있습니다.
따라서 v2로 마이그레이션할 때는 호환성을 보장하기 위해 세심한 테스트가 수반되어야 합니다.

# API vs 동작 변경 사항 (behavior changes)

단순한 마샬링(marshaling) 및 언마샬링(unmarshaling)의 경우, Go API는 언어 수준에서 대부분 호환되므로 API 마이그레이션이 매우 간단합니다.
예를 들어, `import "encoding/json"`을 `import "encoding/json/v2"`로 변경하는 것만으로도 `b, err := json.Marshal(v)` 코드는 그대로 컴파일됩니다.

v1에서 v2로 마이그레이션할 때 어려운 점은 API의 차이가 아니라, 마샬링(marshaling) 및 언마샬링(unmarshaling) 시의 동작 변경 사항입니다.
다음 프로그램을 살펴보십시오:

```go
package main

import (
	"encoding/json"
	"fmt"
)

type Pet struct {
	Name      string
	Nicknames []string
}

func main() {
	pets := []Pet{
		{Name: "Oliver", Nicknames: []string{"Ollie", "Olliepop"}},
		{Name: "Remi"},
	}
	b, err := json.Marshal(pets)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(b))
}
```

[실행](/play/p/Us887UVmEwm) 시, 다음과 같이 출력됩니다:

```
[{"Name":"Oliver","Nicknames":["Ollie","Olliepop"]},{"Name":"Remi","Nicknames":null}]
```

임포트를 변경하여 이 프로그램을 `encoding/json/v2`로 간단히 마이그레이션하더라도, 프로그램은 여전히 컴파일됩니다.
[실행](/play/p/E-SprmrVHZF)하면 다음과 같이 출력됩니다:

```
[{"Name":"Oliver","Nicknames":["Ollie","Olliepop"]},{"Name":"Remi","Nicknames":[]}]
```

Remi의 "Nicknames" 필드가 `null`에서 `[]`로 변경된 점에 유의하십시오.
만약 이것이 새로운 프로그램이었다면 빈 배열을 사용하는 것이 좋은 개선이었겠지만, 기존 애플리케이션의 경우 이 출력값을 사용하는 다운스트림 소비자들이 `null` 값의 존재에 의존하고 있을 수 있으므로, 이러한 변경 사항은 시스템 장애를 일으킬 수 있습니다.

# 옵션

v2 동작이 v1과 다른 모든 부분은 [`Options`](/pkg/encoding/json/v2#Options)에서 다루고 있으며, 이를 통해 v2 API를 사용하면서 v1 동작을 지정할 수 있습니다.
v2 API를 사용하되 모든 v1 동작을 지정하려면 [`DefaultOptionsV1`](/pkg/encoding/json#DefaultOptionsV1)을 사용하십시오:

```go
package main

import (
	jsonv1 "encoding/json"
	"encoding/json/v2"
	"fmt"
)

type Pet struct {
	Name      string
	Nicknames []string
}

func main() {
	pets := []Pet{
		{Name: "Oliver", Nicknames: []string{"Ollie", "Olliepop"}},
		{Name: "Remi"},
	}
	b, err := json.Marshal(pets, jsonv1.DefaultOptionsV1())
	if err != nil {
		panic(err)
	}
	fmt.Println(string(b))
}
```

[실행](/play/p/8wg09vDeNN6)하면, 이번에도 다시 `null`이 출력됩니다:

```
[{"Name":"Oliver","Nicknames":["Ollie","Olliepop"]},{"Name":"Remi","Nicknames":null}]
```

[DefaultOptionsV1](/pkg/encoding/json#DefaultOptionsV1) 문서는 v1 호환성을 위해 사용되는 옵션의 전체 세트를 나열합니다.
나중에 정의된 옵션이 이전 옵션을 덮어쓰므로, 이 목록을 사용하여 v2 동작을 하나씩 활성화할 수 있습니다.

# 마이그레이션

애플리케이션의 유형과 리스크 허용 범위에 따라 v2 마이그레이션에 접근하는 여러 가지 방법이 있습니다.

* 높은 위험 감수 성향: [all-at-once](#all-at-once)
* 낮은 위험 감수 성향 또는 문제 해결 중: [option-by-option](#option-by-option)
* 프로덕션 서버 애플리케이션: [jsonsplit](#jsonsplit)

## All-at-once {#all-at-once}

애플리케이션이 단순하거나 리스크 허용 범위가 높은 경우(마이그레이션으로 인해 문제가 발생해도 영향이 적은 경우), 정교한 마이그레이션 프로세스가 필요하지 않을 수 있습니다.
단순히 호출 사이트(callsites)에서 `encoding/json/v2`를 사용하도록 업데이트하고, 테스트가 통과하는지 확인한 후 커밋하십시오.

호환성 문제가 발생하는 경우, 변경 사항이나 에러 메시지를 통해 차이점이 명확하게 드러날 수 있으며, 이 경우 [적절한 호환성 옵션](/pkg/encoding/json#DefaultOptionsV1)을 설정할 수 있습니다.
문제의 원인이 명확하지 않은 경우, 문제 해결을 돕기 위해 아래 방법 중 하나를 사용할 수 있습니다.

이는 나머지 문제를 추적하기 위한 더 세밀한 접근 방식으로 넘어가기 전에, 명백한 문제(단위 테스트에 의해 식별된 문제 등)를 빠르게 찾아 수정하는 방법이 될 수도 있습니다.

## 옵션별 설명 {#option-by-option}

애플리케이션이 복잡하거나 위험 허용 범위가 낮다면, 더 느리고 신중한 접근 방식이 필요할 수 있습니다.

앞서 언급했듯이, [DefaultOptionsV1](/pkg/encoding/json#DefaultOptionsV1)을 사용하여 `Marshal` 또는 `Unmarshal`을 호출하면 `encoding/json`과 동일하게 동작합니다.
첫 번째 단계로, `DefaultOptionsV1`을 사용하여 `encoding/json/v2`로의 모든 호출을 마이그레이션하십시오.
이는 단순하고 안전한 변경입니다. 실제로 이것이 바로 [`encoding/json`이 `Marshal` 및 `Unmarshal`를 구현하는 방식](https://cs.opensource.google/go/go/+/refs/tags/go1.27rc2:src/encoding/json/v2_encode.go;l=184-186)입니다!

추가로 전달된 옵션은 이전 옵션을 덮어쓰므로, 개별 [v1 호환성 옵션](/pkg/encoding/json#DefaultOptionsV1)을 비활성화할 수 있습니다.
예를 들어, `json.Marshal(v, jsonv1.DefaultOptionsV1(), json.FormatNilSliceAsNull(false))`는 `nil` 슬라이스가 빈 배열로 포맷팅되는 점을 제외하고는 v1과 동일하게 동작합니다.

이는 모든 동작을 한꺼번에 변경하는 대신, 더 완만한 마이그레이션을 수행할 수 있는 경로를 제공합니다.
무엇이 변경되고 있는지 확실히 확인하기 위해 한 번에 하나의 옵션만 활성화하거나, 유사한 옵션들을 그룹화하여 활성화할 수 있습니다.
또는 트러블슈팅 시, 아래 `jsonsplit`에서 살펴볼 옵션 감지 방식과 유사하게, 정확히 어떤 동작 변경으로 인해 문제가 발생했는지 이분법(bisect) 방식으로 찾아낼 수 있는 방법을 제공합니다.

## jsonsplit {#jsonsplit}

[`github.com/go-json-experiment/jsonsplit`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit)은 운영 환경에서 v1과 v2 사이의 차이점을 보고함으로써 마이그레이션을 돕는 JSON 래퍼 패키지입니다.

`jsonsplit`은 기본적으로 `encoding/json`과 동일하게 동작하는 `Marshal` 및 `Unmarshal` 래퍼 함수를 제공하며, 런타임에 v1, v2 또는 두 버전 모두를 사용하도록 설정할 수 있습니다.

([`CallBothButReturnV1`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#CallMode))를 사용하도록 설정하면, `jsonsplit.Marshal`은 입력을 v1과 v2로 각각 한 번씩, 총 두 번 마샬링합니다.
차이점이 발견되면 이를 보고하지만, 호출자에게는 여전히 v1 값을 반환합니다.
이를 통해 운영 서비스는 동작을 변경하지 않고도 차이점을 보고할 수 있습니다.
선택 사항인 [`AutoDetectOptions`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#Codec)를 사용하면, `jsonsplit`은 어떤 특정 옵션이 차이를 유발하는지 자동으로 판별합니다.

이 기능에는 비용이 따른다는 점에 유의하십시오.
차이점을 감지하기 위해 v1과 v2 모두를 사용하여 마샬링(marshaling)하면 마샬링 비용이 거의 두 배로 증가하며, `AutoDetectOptions`는 관련 옵션을 좁히기 위해 훨씬 더 많은 마샬링을 수행합니다.
이러한 비용을 완화하기 위해, `jsonsplit`은 [`SetMarshalCallRatio`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#Codec.SetMarshalCallRatio)를 통해 호출의 무작위 서브셋만 확인하도록 허용합니다.

여기에서는 원래 예제에 `jsonsplit`을 적용해 보았습니다:

```go
package main

import (
	"fmt"

	"github.com/go-json-experiment/jsonsplit"
)

func init() {
	// 차이점을 감지할 수 있도록 v1과 v2를 모두 호출하지만,
	// v1 출력물을 계속 사용합니다.
	jsonsplit.GlobalCodec.SetMarshalCallMode(jsonsplit.CallBothButReturnV1)

	// 차이점이 감지되었을 때, 어떤 옵션이 차이를 유발하는지
	// 자동으로 감지하도록 지정합니다.
	jsonsplit.GlobalCodec.AutoDetectOptions = true

	// v1과 v2 사이의 차이점이 감지될 때마다 로그를 남깁니다.
	jsonsplit.GlobalCodec.ReportDifference = func(d jsonsplit.Difference) {
		fmt.Printf("detected jsonv1-to-jsonv2 difference: %v\n", d)
	}
}

type Pet struct {
	Name      string
	Nicknames []string
}

func main() {
	pets := []Pet{
		{Name: "Oliver", Nicknames: []string{"Ollie", "Olliepop"}},
		{Name: "Remi"},
	}
	b, err := jsonsplit.Marshal(pets)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(b))
}
```

[실행](/play/p/wagp5v8V1w-)하면, 차이점이 보고되며 심지어 `FormatNilSliceAsNull`이 그 차이의 원인임이 나타납니다:

```
detected jsonv1-to-jsonv2 difference: {"Caller":"main.main+5","Func":"Marshal","GoType":"[]main.Pet","JSONValueV1":[{"Name":"Oliver","Nicknames":["Ollie","Olliepop"]},{"Name":"Remi","Nicknames":null}],"JSONValueV2":[{"Name":"Oliver","Nicknames":["Ollie","Olliepop"]},{"Name":"Remi","Nicknames":[]}],"Options":["jsonv2.FormatNilSliceAsNull"]}
[{"Name":"Oliver","Nicknames":["Ollie","Olliepop"]},{"Name":"Remi","Nicknames":null}]
```

다음과 같은 절차를 통해 운영 서비스를 원활하게 마이그레이션할 수 있습니다:

1. 호출 사이트를 `jsonsplit`으로 전환하고, [`CallBothButReturnV1`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#CallMode), [`AutoDetectOptions`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#CallMode) (선택 사항)를 설정하십시오. 또한 [`ReportDifference`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#CallMode)에 선호하는 모니터링 방식(로그 기록 또는 게시된 메트릭 등)을 연결하십시오.

2. 보고된 차이점이 있는지 프로덕션 환경을 모니터링하십시오.

3. 차이점 인코딩(Encode differences).

`jsonsplit`이 차이점을 보고하는 경우, 출력이 동일하도록 옵션이나 타입을 조정하십시오.

예를 들어, 위의 예시에서는 `json.FormatNilSliceAsNull(true)` 옵션을 전달하십시오.
다른 경우에 v2는 수정하기 간단한 문제를 보고할 수 있습니다.
예를 들어, 잘못된 타입(구조체 등)에 "string" JSON 구조체 필드 태그를 적용하는 것은 v1에서는 무시되었지만, v2에서는 에러를 보고합니다.
[`ReportErrorsWithLegacySemantics`](/pkg/encoding/json#ReportErrorsWithLegacySemantics)를 사용하면 해당 에러를 억제할 수 있지만, "string" 태그를 제거하는 것이 더 합리적입니다.
어차피 아무런 역할도 하지 않기 때문입니다.

출력 결과의 차이가 반드시 다운스트림 동작의 파손을 의미하는 것은 아니며, 파손될 가능성이 있음을 의미한다는 점에 유의하십시오.
현재 옵션을 조정하는 이유는 미세한 출력 변화를 평가하기 위해 멈추지 않고 마이그레이션의绝대다수를 완료하기 위함입니다. 하지만 v2로 전환한 후에는 해당 위치들을 다시 검토하여 새로운 동작으로 마이그레이션할 수 있는지 판단해야 합니다.

4. v2로 전환하십시오.

운영 환경에서 더 이상 새로운 차이점이 보고되지 않으면, [`OnlyCallV2`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#CallMode)를 설정하여 v2 동작으로 마이그레이션하거나, 차이점을 계속 확인하기 위해 [`CallBothButReturnV2`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#CallMode)를 설정할 수 있습니다.

5. 정리.

v2로의 전환이 안전하게 배포되면, `jsonsplit`에서 `encoding/json/v2` 자체로 전환하여 마이그레이션을 정리하십시오.
이 시점에서, v1 동작을 유지했던 (3)의 사례들을 평가하여 v2 동작으로 전환해도 안전한지 결정할 수 있습니다.

`jsonsplit` 마이그레이션에 대한 자세한 내용은 [`jsonsplit` 문서](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#hdr-Example_usage_and_migration)를 참조하세요.
