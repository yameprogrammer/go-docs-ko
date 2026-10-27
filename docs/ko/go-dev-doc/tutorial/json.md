<!--{
  "제목": "JSON 사용 튜토리얼",
  "메뉴 경로": true
}-->

JSON (JavaScript Object Notation)은 간단한 데이터 교환 형식입니다.
구문적으로는 JavaScript의 객체와 목록과 유사합니다.
네트워크 API 서비스와의 통신에 일반적으로 사용되지만, 다른 곳에서도 널리 사용됩니다.
그의 공식 홈페이지, [json.org](http://json.org),
는 표준에 대한 훌륭하고 간결한 정의를 제공합니다.

이 [encoding/json/v2 패키지](/pkg/encoding/json/v2)를 사용하면 Go 프로그램에서 JSON 데이터를 읽고 쓰는 것이 매우 쉽습니다.
이 패키지는 이전 버전인 [encoding/json](/pkg/encoding/json) 패키지보다 더 깔끔한 API와 더 나은 기본 설정을 제공합니다.

## 인코딩

JSON 데이터를 인코딩하려면 `Marshal` 함수를 사용합니다.

```
func Marshal(in any, opts ...Options) (out []바이트, err 오류)
```

주어진 Go 데이터 구조인 `Message`를 기준으로,

```
type Message 구조체 {
	Name 문자열
	Body 문자열
	Time time.Time
}
```

그리고 `Message`의 인스턴스

```
m := Message{"Alice", "Hello", time.Date(2011, 1, 25, 0, 0, 0, 0, time.UTC)}
```

우리는 `json.Marshal`를 사용하여 m의 JSON 인코딩된 버전을 직렬화할 수 있습니다:

b, err := json.Marshal(m)

만약 모든 것이 정상적으로 작동하면, `err`는 `nil`이 되고, `b`는 이 JSON 데이터를 포함하는 `[]byte`가 됩니다:

```
b == []byte(`{"Name":"Alice","Body":"Hello","Time":"2011-01-25T00:00:00Z"}`)
```

다음 데이터 구조만 유효한 JSON 형식으로 인코딩됩니다:

- 포인터는 그들이 가리키는 값으로 인코딩됩니다 (또는 포인터가 `nil`인 경우 `null`).

- JSON 객체는 키로만 문자열을 지원합니다.
    따라서 Go 맵을 JSON으로 인코딩하려면 JSON 문자열로 인코딩될 수 있는 키를 가져야 합니다.
    예를 들어 `map[string]T` (여기서 `T`는 `json` 패키지에 의해 지원되는 모든 Go 유형)입니다.

- 채널, 복잡한, 및 함수 타입은 인코딩할 수 없습니다.

- 순환 데이터 구조는 지원되지 않습니다.

- [`Marshal`](/pkg/encoding/json/v2#Marshal)는 전체 인코딩 의미론을 문서화합니다.

`json` 패키지는 구조체 유형의 내보낸 필드(대문자로 시작하는 필드)만 접근합니다.
따라서 JSON 출력에는 구조체의 내보낸 필드만 포함됩니다.

## 디코딩

JSON 데이터를 디코딩하려면 `Unmarshal` 함수를 사용합니다.

```
func Unmarshal(in []바이트, out any, opts ...옵션) (오류 오류)
```

우리는 먼저 디코딩된 데이터를 저장할 공간을 먼저 만들어야 합니다

```
var m Message
```

그리고 `json.Unmarshal`을 호출하여, JSON 데이터의 `[]byte`와 `m`의 포인터를 전달합니다.

```
err := json.Unmarshal(b, &m)
```

만약 `b`에 유효한 JSON이 포함되어 있고, 이 JSON이 `m`에 들어갈 수 있다면,
`err` 호출 후에는 `err` 값이 `nil`이 되고, `b`의 데이터가 `m`의 구조체에 저장됩니다.
이는 다음과 같은 할당처럼 동작합니다:

```
m = Message{
	Name: "Alice",
	Body: "Hello",
	Time: time.Date(2011, 1, 25, 0, 0, 0, 0, time.UTC),
}
```

`Unmarshal` 함수는 디코딩된 데이터를 저장할 필드를 어떻게 식별하는가?

주어진 JSON 키 `"Foo"`에 대해,
`Unmarshal` 함수는 다음과 같은 순서로 우선순위를 고려하여 대상 구조체의 필드를 탐색하여 찾습니다:

- 내보낸 필드에 `json:"Foo"` 태그가 지정되어 있습니다 (구조체 태그에 대한 자세한 내용은 [Go 사양](/ref/spec#Struct_types) 참조).

- 내보낸 필드 "Foo"

JSON 데이터의 구조가 Go 타입과 정확히 일치하지 않을 때 어떤 일이 발생하는가?

```
b := []byte(`{"Name":"Bob","Food":"Pickle"}`)
var m Message
err := json.Unmarshal(b, &m)
```

`Unmarshal`는 대상 유형에서 찾을 수 있는 필드만 디코딩합니다.
이 경우, `m`의 `Name` 필드만 채워지고, `Food` 필드는 무시됩니다.
이 동작은 특히 대규모 JSON 데이터에서 특정 필드만 선택하고자 할 때 유용합니다.
또한 대상 구조체에 정의되지 않은 (private) 필드는 `Unmarshal`에 의해 영향을 받지 않습니다.

하지만 JSON 데이터의 구조를 미리 알 수 없는 경우 어떻게 해야 할까요?

## `any` 타입으로 사용되는 일반 JSON

`any` 타입은 모든 Go 타입을 설명합니다.
`any`는 `interface{}` (빈 인터페이스)로 정의되며, 이는 메서드가 없는 인터페이스를 나타냅니다.
모든 Go 타입은 최소한 0개의 메서드를 구현하므로, 빈 인터페이스를 만족합니다.

`any`는 일반적인 컨테이너 타입으로 사용됩니다:

```
var a any
    a = "a string"
    a = 2011
    a = 2.777
```

타입 암시는 실제 구체적인 타입에 접근합니다:

```markdown
r := a.(float64)
fmt.Println("원의 넓이", math.Pi * r * r)
```

또는, 기본 유형이 알 수 없는 경우, 타입 스위치가 유형을 결정합니다:

```markdown
switch v := a.(type) {
  case int:
    fmt.Println("a의 2배는", v*2)
  case float64:
    fmt.Println("a의 역수는", 1/v)
  case string:
    h := len(v) / 2
    fmt.Println("a를 반으로 나누면", v[h:]+v[:h])
  default:
    // a는 위의 유형 중 하나가 아닙니다.
}
```

`json` 패키지는 `map[string]any` 및
`[]any` 값을 사용하여 임의의 JSON 객체와 배열을 저장합니다.
이 패키지는 유효한 모든 JSON 블록을 일반 `any` 값으로 자유롭게 언마샬링합니다. 기본 구체 Go 유형은 다음과 같습니다:

- `bool`을 사용하여 JSON 부울 값 표현

- `float64`를 JSON 숫자 형식으로 사용합니다,

- `string`을 JSON 문자열에 사용하고,

- `nil`을 JSON null 값으로 사용합니다.

## 임의의 데이터 디코딩

다음 JSON 데이터를 변수 `b`에 저장했다고 가정합니다:

```
b := []byte(`{"Name":"Wednesday","Age":6,"Parents":["Gomez","Morticia"]}`)
```

알려진 데이터 구조 없이, `Unmarshal` 함수를 사용하여 이를 `any` 값으로 디코딩할 수 있습니다:

```
var f any
err := json.Unmarshal(b, &f)
```

현재 `f` 내의 Go 값은 문자열을 키로 하고, 값은 `any` 유형으로 저장된 맵이 됩니다:

```
f = map[string]any{
	"이름": "Wednesday",
	"나이": 6,
	"부모": [
		"Gomez",
		"Morticia",
	],
}
```

이 데이터를 액세스하려면 `f`의 기본 `map[string]any`에 액세스하기 위해 타입 어설션을 사용할 수 있습니다:

```
m := f.(map[string]any)
```

다음으로, 우리는 `range` 문을 사용하여 맵을 반복하고, `type` 스위치를 사용하여 값들을 실제 유형으로 접근할 수 있습니다:

```
for k, v := range m {
	switch vv := v.(type) {
	case string:
		fmt.Println(k, "is string", vv)
	case float64:
		fmt.Println(k, "is float64", vv)
	case []any:
		fmt.Println(k, "is an array:")
		for i, u := range vv {
			fmt.Println(i, u)
		}
	default:
		fmt.Println(k, "is of a type I don't know how to handle")
	}
}
```

이 방법을 사용하면, 여전히 타입 안전의 이점을 누리면서, 알 수 없는 JSON 데이터를 처리할 수 있습니다.

## 참조 타입

다음 예제에서 가져온 데이터를 담을 수 있는 Go 타입을 정의해 보겠습니다:

```
구조 FamilyMember는 다음과 같은 필드를 가집니다.
	Name: 문자열
	Age: 정수
	Parents: 문자열 슬라이스

변수 m을 FamilyMember 타입으로 선언
err := json.Unmarshal(b, &m)
```

`FamilyMember` 값을 반환하는 데 성공합니다.
하지만 자세히 살펴보면 놀라운 일이 발생했습니다.
`var` 문을 사용하여 `FamilyMember` 구조체를 할당하고, 그 값을 `Unmarshal`에 전달했지만,
그 시점에 `Parents` 필드는 `nil` 슬라이스 값으로 남아 있었습니다.
`Parents` 필드를 채우기 위해, `Unmarshal`은 내부적으로 새로운 슬라이스를 할당했습니다.
이는 지원되는 참조 유형(포인터, 슬라이스, 맵)과의 작동 방식입니다.

다음 데이터 구조로 언마샬하는 것을 고려하십시오:

```markdown
```go
type Foo struct {
	Bar *Bar
}
```

만약 JSON 객체에 `Bar` 필드가 존재한다면,
`Unmarshal`은 새로운 `Bar`를 할당하고 초기화합니다.
그렇지 않으면, `Bar`는 `nil` 포인터로 남게 됩니다.

다음에서 유용한 패턴이 나타납니다: 몇 가지 구별되는 메시지 유형을 수신하는 애플리케이션이 있는 경우, 다음과 같은 "receiver" 구조를 정의할 수 있습니다:

```
type IncomingMessage struct {
	Cmd *Command
	Msg *Message
}
```

그리고 발신자는 `Cmd` 필드와/또는 `Msg` 필드를 상위 JSON 객체의 해당 필드에 채울 수 있습니다.
이는 발신자가 전달하고자 하는 메시지의 유형에 따라 달라집니다.
`Unmarshal` 함수는 JSON을 `IncomingMessage` 구조체로 디코딩할 때, JSON 데이터에 존재하는 데이터 구조만 할당합니다.
어떤 메시지를 처리해야 하는지 알기 위해, 개발자는 `Cmd` 또는 `Msg`가 `nil`인지 확인하기만 하면 됩니다.

## 스트리밍 방식으로 마샬 및 언마샬 수행

[`io.Reader`](/pkg/io#Reader) 및 [`io.Writer`](/pkg/io#Writer) 인터페이스는 Go에서 매우 흔하게 사용되며, HTTP 연결, WebSockets 또는 파일과 같은 리소스에 대한 스트리밍 액세스를 제공합니다.

`MarshalWrite` 및 `UnmarshalRead` 함수는 중간의 `[]byte`를 사용하는 대신, 이러한 스트림에 직접 마샬링 및 언마샬링을 가능하게 합니다.

```
func MarshalWrite(out io.Writer, in any, opts ...Options) (err error)
func UnmarshalRead(in io.Reader, out any, opts ...Options) (err error)
```

예를 들어, 우리는 직렬화된 출력을 표준 출력으로 직접 작성할 수 있습니다:

```
err := json.MarshalWrite(os.Stdout, m)
```

## 사용자 정의 Marshal 및 Unmarshal

때로는 기본 마샬 동작이 특정 유형에 적합하지 않을 수 있습니다.

예를 들어, 소프트웨어 버전을 설명하는 유형이 있다고 가정해 보겠습니다.

```
type Version struct {
	Major, Minor, Patch int64
}

v := Version{1, 2, 3}
b, err := json.Marshal(s)
```

이것은 `{"Major":1,"Minor":2,"Patch":3}` 형태로 표현되지만, 예상대로 구조 정의에 따라, "1.2.3"과 같은 버전 문자열이 JSON 소비자에게 더 적합한 표현일 가능성이 높습니다.

`[`MarshalerTo`](/pkg/encoding/json/v2#MarshalerTo) 인터페이스를 구현함으로써, 우리는 사용자 정의 JSON 표현을 제공할 수 있습니다.
`[`UnmarshalerFrom`](/pkg/encoding/json/v2#UnmarshalerFrom)는 사용자 정의 JSON 표현을 언마샬링하는 데 사용됩니다.

```
인터페이스 MarshalerTo {
	MarshalJSONTo(*jsontext.Encoder) 에러
}

인터페이스 UnmarshalerFrom {
	UnmarshalJSONFrom(*jsontext.Decoder) 에러
}
```

다음 방법을 사용하여 문자열 표현으로 변환하고 다시 변환할 수 있습니다.

```
func (v Version) MarshalJSONTo(enc *jsontext.Encoder) error {
	return json.MarshalEncode(enc, fmt.Sprintf("%d.%d.%d", v.Major, v.Minor, v.Patch))
}
```

사용자 정의 마샬링을 통해 `Version{1, 2, 3}` 값은 이제 `"1.2.3"`으로 마샬링됩니다.

```
func (v *Version) UnmarshalJSONFrom(dec *jsontext.Decoder) error {
	if k := dec.PeekKind(); k != jsontext.KindString {
		// 값은 문자열이어야 합니다.
		return &json.SemanticError{JSONKind: k}
	}

	var s string
	if err := json.UnmarshalDecode(dec, &s); err != nil {
		return err
	}

	_, err := fmt.Sscanf(s, "%d.%d.%d", &v.Major, &v.Minor, &v.Patch)
	return err
}
```

사용자 정의 언마샬링을 사용하면 `"1.2.3"`이 이제 `Version{1, 2, 3}`으로 언마샬됩니다.
이 간단한 예제는 정확한 `"major.minor.patch"` 버전 형식을 요구하지만, 더 복잡한 `UnmarshalJSONFrom`은 유연성을 추가할 수 있습니다. 예를 들어, minor 및 patch 버전이 선택 사항으로 만들 수 있습니다.

## 참고 자료

자세한 내용은 [encoding/json/v2](/pkg/encoding/json/v2) 및 [encoding/json/jsontext](/pkg/encoding/json/jsontext) 패키지 문서를 참조하십시오.
