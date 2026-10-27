Go 1.27에 도입된 [encoding/json/v2](/pkg/encoding/json/v2) 패키지는 원래의 [encoding/json](/pkg/encoding/json) 패키지의 주요 개선 사항입니다.

이 가이드는 v1에서 v2 패키지로 마이그레이션해야 하는 이유와 안전하게 수행하는 방법에 대해 설명합니다.

# 이전을 해야 하는 이유는 무엇인가?

먼저, 이것은 필수는 아닙니다!
`encoding/json` 패키지는 절대 사라지지 않습니다.
이는 Go 1 호환성 약속의 대상이 되므로, `encoding/json`을 사용하는 패키지는 계속해서 작동할 것입니다.

또한, `encoding/json` 및 `encoding/json/v2`는 서로 호환됩니다.
예를 들어, 유형이 [`encoding/json/v2.MarshalerTo`](/pkg/encoding/json/v2#MarshalerTo)를 사용하여 사용자 정의 매싱 동작을 구현하는 경우, `encoding/json.Marshal`](/pkg/encoding/json#Marshal)를 통해 이 유형을 매싱하는 호출자는 여전히 사용자 정의 매셔를 사용합니다.
마찬가지로 Go 1.27에서 함께 도입된 새로운 `json` 구조체 태그와 `encoding/json/v2`도 `encoding/json`에서 지원됩니다.

물론, 이 기능을 사용하지 않아도 괜찮지만, 다음과 같은 몇 가지 좋은 이유가 있습니다:

먼저, 새로운 API는 사용하기가 더 쉽습니다.
예를 들어, [`io.Writer`](/pkg/io#Writer)로 쉽게 직렬화할 수 있으며, `encoding/json/v2.MarshalWrite`를 사용하므로, `encoding/json.Encoder`가 필요하지 않습니다.
`encoding/json/v2.Marshalers`를 사용하면 특정 유형의 직렬화 동작을 재정의할 수 있으며, 해당 유형을 제어하지 않더라도 가능합니다.
`encoding/json/v2.MatchCaseInsenstiveNames`를 사용하면 JSON 객체 멤버 이름과 Go 구조체 필드의 대소문자 구분을 제어할 수 있습니다.

이러한 개선 사항은 유용하지만, 마이그레이션의 가장 큰 이유는 v2 패키지가 v1보다 더 엄격하고 상호 운용성이 높은 기본 설정을 선택하기 때문입니다. [`encoding/json` 설명서](/pkg/encoding/json#hdr-Migrating_to_v2)에는 모든 차이점이 포함되어 있으며, 주요 내용은 다음과 같습니다:

* v1 버전에서는 문자열 내의 유효하지 않은 UTF-8 바이트가 Unicode 대체 문자로 무시되도록 처리됩니다. 반면 v2 버전에서는 유효하지 않은 UTF-8의 존재는 오류를 발생시킵니다.
* v1 버전에서는 중복된 이름을 가진 JSON 객체가 허용됩니다. 반면 v2 버전에서는 중복된 이름을 가진 JSON 객체는 오류를 발생시킵니다.
* v1 버전에서는 Go 구조체 유형 중 일부 구조적 오류(예: 잘못된 필드 태그)가 있는 경우, 런타임에 오류가 보고되지 않습니다. 반면 v2 버전에서는 JSON 직렬화와 관련하여 유효하지 않은 Go 유형에 대해 런타임 오류를 보고합니다.
* v1 버전에서는 Go 슬라이스 또는 Go 맵이 `nil`일 때 JSON null로 직렬화됩니다. 반면 v2 버전에서는 Go 슬라이스 또는 Go 맵이 `nil`일 때 각각 빈 JSON 배열 또는 JSON 객체로 직렬화됩니다.

이 변경 사항은 `encoding/json/v2`를 더 광범위한 JSON 생태계와 호환되도록, 더 예측 가능하고, 오류 발생 가능성을 줄이도록 설계되었습니다.
그러나 이 변경 사항은 이전 버전과 호환되지 않습니다. 일부 애플리케이션은 v1의 동작에 의존할 수 있습니다.
따라서 v2로의 마이그레이션에는 호환성을 보장하기 위한 신중한 테스트가 필요합니다.

# API와 동작 변경 비교

단순한 직렬화 및 역직렬화를 위해, Go API는 언어 수준에서 대부분 호환되므로, API 마이그레이션은 매우 간단합니다.
예를 들어, `b, err := json.Marshal(v)`는 `import "encoding/json"`을 `import "encoding/json/v2"`로 변경하는 것만으로도 계속 컴파일됩니다.

v1에서 v2로 마이그레이트하는 가장 어려운 부분은 API 차이 때문이 아니라, 직렬화 및 역직렬화 동작의 변경입니다.

다음 프로그램을 고려해 보세요:

```markdown
패키지 main

import (
	"encoding/json"
	"fmt"
)

형식 Pet {
	Name      string
	Nicknames []string
}

함수 main() {
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

`run`를 실행하면 다음과 같은 결과가 출력됩니다:

```json
[{"Name":"Oliver","Nicknames":["Ollie","Olliepop"]},{"Name":"Remi","Nicknames":null}]
```

만약 이 프로그램을 `encoding/json/v2`로 단순히 마이그레이션하면, import 문만 변경해도 프로그램은 여전히 컴파일됩니다.
[실행](/play/p/E-SprmrVHZF)하면 다음 출력을 생성합니다:

```json
[{"Name":"Oliver","Nicknames":["Ollie","Olliepop"]},{"Name":"Remi","Nicknames":[]}]
```

참고: "별명" 필드의 Remi 값은 `null`에서 `[]`로 변경되었습니다.
만약 이것이 새로운 프로그램이라면, 빈 배열을 사용하는 것은 좋은 개선일 수 있지만, 기존 애플리케이션의 후속 소비자들은 이 출력의 존재 여부에 의존하고 있을 수 있으므로, 이 변경은 그들을 손상시킬 수 있습니다.

# 옵션

[`Options`](/pkg/encoding/json/v2#Options)에서 v2의 동작 방식과 v1의 동작 방식이 다른 모든 경우를 처리합니다. 이를 통해 v2 API를 사용하여 v1 동작 방식을 지정할 수 있습니다.

v2 API를 사용하면서 모든 v1 동작 방식을 지정하려면 [`DefaultOptionsV1`](/pkg/encoding/json#DefaultOptionsV1)를 사용하십시오:

```
패키지 main

import (
	jsonv1 "encoding/json"
	"encoding/json/v2"
	"fmt"
)

구조 Pet {
	이름      string
	별명     []string
}

함수 main() {
	반장 := []Pet{
		{이름: "Oliver", 별명: []string{"Ollie", "Olliepop"}},
		{이름: "Remi"},
	}
	b, err := json.Marshal(반장, jsonv1.DefaultOptionsV1())
	if err != nil {
		panic(err)
	}
	fmt.Println(string(b))
}
```

`[run](/play/p/8wg09vDeNN6)`을 실행하면, 이 역시 `null`을 출력합니다:

```json
[{"Name":"Oliver","Nicknames":["Ollie","Olliepop"]},{"Name":"Remi","Nicknames":null}]
```

[DefaultOptionsV1](/pkg/encoding/json#DefaultOptionsV1) 문서는 v1 호환성을 위한 사용되는 모든 옵션을 나열합니다.

후에 정의된 옵션은 이전 옵션을 덮어쓰므로, 이 목록을 사용하여 v2 동작을 하나씩 활성화할 수 있습니다.

# 마이그레이션

애플리케이션의 유형과 위험 허용 수준에 따라 v2 마이그레이션을 수행하는 데 여러 가지 다른 방법이 있습니다:

* 높은 위험 감수 수준: [all-at-once](#all-at-once)
* 낮은 위험 감수 수준 또는 문제 해결: [option-by-option](#option-by-option)
* 프로덕션 서버 애플리케이션: [jsonsplit](#jsonsplit)

## 한 번에 수행 {#all-at-once}

만약 애플리케이션이 간단하거나 높은 위험 허용 수준을 가지고 있다면 (이동으로 인해 문제가 발생해도 큰 결과가 없으므로), 복잡한 마이그레이션 프로세스가 필요하지 않을 수 있습니다.

단순히 호출 위치를 `encoding/json/v2`를 사용하도록 업데이트하고, 테스트가 통과하는지 확인하고, 커밋합니다.

만약 호환성 문제가 발생하면, 차이점의 원인은 변경 내용이나 오류 메시지에서 명확하게 드러날 수 있습니다. 이 경우, 적절한 호환성 옵션을 설정할 수 있습니다. [적절한 호환성 옵션](/pkg/encoding/json#DefaultOptionsV1).

문제의 원인이 명확하지 않은 경우, 아래의 방법을 사용하여 문제를 해결하는 데 도움을 받을 수 있습니다.

이 방법은 또한 단위를 테스트를 통해 식별된 명확한 문제(예: 문제)를 빠르게 찾아 수정하는 방법이 될 수 있으며, 이를 통해 나머지 문제를 해결하는 보다 정교한 접근 방식을 사용하기 전에 이 문제를 해결할 수 있습니다.

## 옵션별로 설정하기 {#option-by-option}

만약 애플리케이션이 복잡하거나 위험 감수 수준이 낮다면, 더 신중하고 점진적인 접근 방식을 취해야 할 수 있습니다.

위에서 언급했듯이, `Marshal` 또는 `Unmarshal` 함수를 `DefaultOptionsV1`로 호출하면, 해당 호출은 `encoding/json`과 동일하게 동작합니다.
첫 번째 단계로, `DefaultOptionsV1`를 사용하여 모든 `encoding/json/v2` 호출을 마이그레이션합니다.
이것은 간단하고 안전한 변경 사항입니다. 실제로, `encoding/json`은 `Marshal` 및 `Unmarshal`을 다음과 같이 구현합니다: [`encoding/json`](https://cs.opensource.google/go/go/+/refs/tags/go1.27rc2:src/encoding/json/v2_encode.go:184-186)!

추가로 전달된 옵션은 이전 옵션을 덮어쓰기 때문에, 개별 [v1 호환 옵션]을 비활성화할 수 있습니다. ([/pkg/encoding/json#DefaultOptionsV1](/)
예를 들어, `json.Marshal(v, jsonv1.DefaultOptionsV1(), json.FormatNilSliceAsNull(false))`는 `nil` 슬라이스를 빈 배열로 형식화하는 것 외에는 v1과 동일하게 작동합니다.

이것은 한 번에 모든 동작을 변경하는 대신, 더 느린 마이그레이션을 수행하는 방법을 제공합니다.
각 옵션을 개별적으로 활성화하여 변경되는 내용을 명확하게 확인할 수도 있고, 유사한 옵션을 그룹화할 수도 있습니다.
대안으로, 이러한 옵션을 디버깅할 때, 특정 오류 동작 변경을 정확하게 찾아내는 방법을 제공할 수 있습니다. 이는 아래의 `jsonsplit`에서 볼 것인 옵션 감지와 유사합니다.

## jsonsplit

[`github.com/go-json-experiment/jsonsplit`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit)는 JSON 래퍼 패키지로, 프로덕션 환경에서 v1과 v2 간의 차이점을 보고하여 마이그레이션을 돕습니다.

`jsonsplit`는 기본적으로 `encoding/json`과 동일하게 동작하는 `Marshal` 및 `Unmarshal` 래퍼 함수를 제공합니다. 그러나 런타임에 v1, v2, 또는 둘 다를 사용할 수 있도록 구성할 수 있습니다.

`CallBothButReturnV1` 모드로 설정하면 `jsonsplit.Marshal`은 입력값을 두 번에 걸쳐 직렬화합니다: 한 번은 v1 및 v2로.
차이점을 보고하지만, 여전히 호출자에게 v1 값을 반환합니다.
이를 통해 프로덕션 서비스는 동작을 변경하지 않고 차이점을 보고할 수 있습니다.
선택 사항인 [`AutoDetectOptions`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#Codec)를 사용하면 `jsonsplit`은 어떤 특정 옵션이 차이점을 유발하는지 자동으로 식별합니다.

참고: 이 기능은 비용이 발생합니다.
v1 및 v2 모두 사용하여 차이점을 감지하는 마셜링은 마셜링 비용을 약 두 배로 증가시키며, `AutoDetectOptions`는 관련 옵션을 좁히기 위해 더욱 많은 마셜링을 수행합니다.
이 비용을 완화하기 위해, `jsonsplit`는 [`SetMarshalCallRatio`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#Codec.SetMarshalCallRatio)를 사용하여 호출의 임의 하위 집합만 확인하도록 허용합니다.

여기서, 원래 예제에 `jsonsplit`을 적용했습니다:

```
package main

import (
	"fmt"

	"github.com/go-json-experiment/jsonsplit"
)

func init() {
	// v1 및 v2를 모두 호출하여 차이를 감지할 수 있지만,
	// v1 출력을 계속 사용합니다.
	jsonsplit.GlobalCodec.SetMarshalCallMode(jsonsplit.CallBothButReturnV1)

	// 차이가 감지되면 어떤 옵션이 차이를 유발하는지 자동으로 감지하도록 지정합니다.
	jsonsplit.GlobalCodec.AutoDetectOptions = true

	// v1과 v2 사이의 차이가 감지될 때마다 로그를 기록합니다.
	jsonsplit.GlobalCodec.ReportDifference = func(d jsonsplit.Difference) {
		fmt.Printf("jsonv1-to-jsonv2 차이 감지: %v\n", d)
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

`[run](/play/p/wagp5v8V1w-)`를 실행하면 차이를 보고하며, 특히 `FormatNilSliceAsNull`이 이러한 차이에 책임이 있다는 것을 보여줍니다:

```
발견된 jsonv1-to-jsonv2 차이: {"Caller":"main.main+5","Func":"Marshal","GoType":"[]main.Pet","JSONValueV1":[{"Name":"Oliver","Nicknames":["Ollie","Olliepop"]},{"Name":"Remi","Nicknames":null}],"JSONValueV2":[{"Name":"Oliver","Nicknames":["Ollie","Olliepop"]},{"Name":"Remi","Nicknames":[]}],"Options":["jsonv2.FormatNilSliceAsNull"]}
[{"Name":"Oliver","Nicknames":["Ollie","Olliepop"]},{"Name":"Remi","Nicknames":null}]
```

다음과 같은 절차를 사용하여 프로덕션 서비스를 원활하게 마이그레이션할 수 있습니다:

1. `jsonsplit`로 호출 위치를 변경하고, [`CallBothButReturnV1`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#CallMode), [`AutoDetectOptions`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#CallMode) (선택 사항) 및 원하는 모니터링 방식을 `ReportDifference`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#CallMode) (예: 로깅 또는 게시된 메트릭)에 연결합니다.

2. 보고된 차이점을 확인하기 위해 프로덕션 환경을 모니터링합니다.

3. 차이를 인코딩합니다.

`jsonsplit`에서 차이점을 보고하는 경우, 옵션 또는 타입을 조정하여 동일한 출력을 보장해야 합니다.

예를 들어, 위의 예시에서 `json.FormatNilSliceAsNull(true)` 옵션을 전달합니다.
다른 경우에는 v2가 해결하기 쉬운 문제를 보고할 수 있습니다.
예를 들어, "string" JSON 구조 필드 태그를 유효하지 않은 유형(예: 구조체)에 적용하는 것은 v1에서는 무시되지만, v2에서는 오류를 보고합니다.
`[ReportErrorsWithLegacySemantics](pkg/encoding/json#ReportErrorsWithLegacySemantics)`를 사용하면 오류를 억제할 수 있지만, "string" 태그를 제거하는 것이 더 합리적입니다.
어차피 아무것도 하지 않습니다.

참고: 출력의 차이가 반드시 후속 동작에 문제를 일으키는 것은 아니지만, 문제가 발생할 가능성이 있음을 의미합니다.

현재 설정을 조정하여 대부분의 마이그레이션을 중단 없이 완료할 수 있도록 하지만, v2로 전환한 후에는 이러한 위치를 다시 확인하여 새로운 동작으로 마이그레이션할 수 있는지 확인해야 합니다.

4. v2 버전으로 전환

한 번 프로덕션 환경에서 새로운 차이점을 보고하는 것이 중단되면, [`OnlyCallV2`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#CallMode) 또는 [`CallBothButReturnV2`](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#CallMode)를 설정하여 차이점을 계속 확인하도록 변경할 수 있습니다.

5. 정리

스위치를 v2로 안전하게 배포한 후, 마이그레이션을 정리합니다. `jsonsplit`를 `encoding/json/v2` 자체로 변경합니다.

이 시점에서 (3)에서 일부 v1 동작을 유지하는 경우를 평가하여, 이를 v2 동작으로 변경해도 안전한지 확인할 수 있습니다.

자세한 내용은 [`jsonsplit` 문서를 참조](https://pkg.go.dev/github.com/go-json-experiment/jsonsplit#hdr-Example_usage_and_migration)하세요.
