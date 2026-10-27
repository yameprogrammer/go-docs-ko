<!--{
  "Title": "튜토리얼: JSON 작업하기",
  "Breadcrumb": true
}-->

JSON (JavaScript Object Notation)은 단순한 데이터 교환 포맷입니다.
구문적으로는 JavaScript의 객체 및 리스트와 유사합니다.
일반적으로 네트워크 API 서비스와의 통신에 사용되지만, 그 외의 많은 곳에서도 사용됩니다.
홈페이지인 [json.org](http://json.org)에서 이 표준에 대한 매우 명확하고 간결한 정의를 제공합니다.

[encoding/json/v2 패키지](/pkg/encoding/json/v2)를 사용하면 Go 프로그램에서 JSON 데이터를 읽고 쓰는 것이 매우 간편합니다.
이 패키지는 기존의 [encoding/json](/pkg/encoding/json) 패키지보다 더 깔끔한 API와 더 나은 기본 설정을 제공합니다.

## 인코딩

JSON 데이터를 인코딩하려면 [`Marshal`](/pkg/encoding/json/v2#Marshal) 함수를 사용합니다.

```
func Marshal(in any, opts ...Options) (out []byte, err error)
```

Go 데이터 구조체인 `Message`가 주어졌을 때,

```
type Message struct {
	Name string
	Body string
	Time time.Time
}
```

그리고 `Message` 인스턴스 하나

```
m := Message{"Alice", "Hello", time.Date(2011, 1, 25, 0, 0, 0, 0, time.UTC)}
```

`json.Marshal`을 사용하여 `m`의 JSON 인코딩 버전을 마샬링할 수 있습니다:

```
b, err := json.Marshal(m)
```

모든 것이 정상이라면, `err`은 `nil`이 되고 `b`는 다음 JSON 데이터를 포함하는 `[]byte`가 됩니다.

```
b == []byte(`{"Name":"Alice","Body":"Hello","Time":"2011-01-25T00:00:00Z"}`)
```

유효한 JSON으로 표현될 수 있는 데이터 구조만 인코딩됩니다:

- 포인터는 가리키는 값으로 인코딩됩니다 (포인터가 `nil`인 경우 `null`로 인코딩됩니다).

- JSON 객체는 키로 문자열만 지원합니다.
    따라서 Go 맵을 인코딩하려면, `map[string]T`(`T`는 json 패키지에서 지원하는 모든 Go 타입)와 같이 JSON 문자열로 인코딩 가능한 키를 가져야 합니다.

- 채널(Channel), 복소수(complex), 함수(function) 타입은 인코딩할 수 없습니다.

- 순환 데이터 구조(Cyclic data structures)는 지원되지 않습니다.

- [`Marshal`](/pkg/encoding/json/v2#Marshal)에 전체 인코딩 시맨틱스에 대한 문서가 설명되어 있습니다.

`json` 패키지는 구조체 타입의 내보내기 된(exported) 필드(대문자로 시작하는 필드)에만 접근합니다.
따라서 구조체의 내보내기 된 필드만이 JSON 출력에 포함됩니다.

## 디코딩(Decoding)

JSON 데이터를 디코딩하려면 [`Unmarshal`](/pkg/encoding/json/v2#Unmarshal) 함수를 사용합니다.

```
func Unmarshal(in []byte, out any, opts ...Options) (err error)
```

먼저 디코딩된 데이터가 저장될 공간을 생성해야 합니다.

```
var m Message
```

그리고 `json.Unmarshal`을 호출하며, JSON 데이터가 담긴 `[]byte`와 `m`에 대한 포인터를 전달합니다.

```
err := json.Unmarshal(b, &m)
```

`b`에 `m`에 적합한 유효한 JSON이 포함되어 있다면,
호출 후 `err`은 `nil`이 되며 `b`의 데이터가
다음과 같은 할당문처럼
구조체 `m`에 저장됩니다:

```
m = Message{
	Name: "Alice",
	Body: "Hello",
	Time: time.Date(2011, 1, 25, 0, 0, 0, 0, time.UTC),
}
```

`Unmarshal`은 디코딩된 데이터를 저장할 필드를 어떻게 식별하나요?
특정 JSON 키 `"Foo"`에 대해,
`Unmarshal`은 대상 구조체의 필드를 다음 순서(우선순위 순)로 탐색하여 찾습니다:

- `json:"Foo"` 태그가 지정된 내보내기 가능한(exported) 필드([Go spec](/ref/spec#Struct_types)에서 구조체 태그에 대한 자세한 내용을 확인하세요), 또는

- `Foo`라는 이름의 공개(exported) 필드.

JSON 데이터의 구조가 Go 타입과 정확히 일치하지 않을 때 어떤 일이 발생하나요?

```
b := []byte(`{"Name":"Bob","Food":"Pickle"}`)
var m Message
err := json.Unmarshal(b, &m)
```

`Unmarshal`은 대상 타입에서 찾을 수 있는 필드만 디코딩합니다.
이 경우, `m`의 `Name` 필드만 값이 채워지며,
`Food` 필드는 무시됩니다.
이러한 동작은 거대한 JSON 블롭에서 몇 개의 특정 필드만 선택해서 가져오고 싶을 때 특히 유용합니다.
또한 이는 대상 구조체의 모든 비공개(unexported) 필드가 `Unmarshal`의 영향을 받지 않음을 의미합니다.

하지만 JSON 데이터의 구조를 미리 알지 못하는 경우에는 어떻게 해야 할까요?

## `any`를 사용한 제네릭 JSON

`any` 타입은 모든 Go 타입을 설명합니다.
`any`는 메서드가 하나도 없는 인터페이스인 `interface{}` (빈 인터페이스)로 정의됩니다.
모든 Go 타입은 최소 0개의 메서드를 구현하므로 빈 인터페이스를 만족합니다.

`any`는 일반적인 컨테이너 타입으로 사용됩니다:

```go
var a any
	a = "a string"
	a = 2011
	a = 2.777
```

타입 단언(type assertion)은 기저의 구체적인 타입(concrete type)에 접근합니다:

```go
r := a.(float64)
	fmt.Println("the circle's area", math.Pi*r*r)
```

또는, 기본 타입(underlying type)을 알 수 없는 경우, 타입 스위치(type switch)를 통해 타입을 결정합니다:

```go
switch v := a.(type) {
	case int:
	    fmt.Println("twice a is", v*2)
	case float64:
	    fmt.Println("the reciprocal of a is", 1/v)
	case string:
	    h := len(v) / 2
	    fmt.Println("a swapped by halves is", v[h:]+v[:h])
	default:
	    // a는 위의 타입 중 하나가 아닙니다
	}
```

`json` 패키지는 임의의 JSON 객체와 배열을 저장하기 위해 `map[string]any` 및 `[]any` 값을 사용합니다. 유효한 JSON 블롭(blob)이라면 어떤 것이든 `any` 값으로 기꺼이 언마셜(unmarshal)합니다. 기본 구체 Go 타입은 다음과 같습니다.

- JSON 불리언(boolean)을 위한 `bool`,

- JSON 숫자를 위한 `float64`,

- JSON 문자열을 위한 `string`, 그리고

- JSON null의 경우 `nil`을 사용합니다.

## 임의의 데이터 디코딩하기

변수 `b`에 저장된 다음 JSON 데이터를 살펴보겠습니다.

```
b := []byte(`{"Name":"Wednesday","Age":6,"Parents":["Gomez","Morticia"]}`)
```

데이터의 구조를 모르는 상태에서도 `Unmarshal`을 사용하여 `any` 값으로 디코딩할 수 있습니다:

```go
var f any
err := json.Unmarshal(b, &f)
```

이 시점에서 `f`에 담긴 Go 값은 키가 문자열이고 값 자체가 `any` 값으로 저장된 맵이 됩니다.

```
f = map[string]any{
	"Name": "Wednesday",
	"Age":  6,
	"Parents": []any{
		"Gomez",
		"Morticia",
	},
}
```

이 데이터에 접근하기 위해 타입 단언(type assertion)을 사용하여 `f`의 기본 `map[string]any`에 접근할 수 있습니다:

```
m := f.(map[string]any)
```

그 다음 `range` 문을 사용하여 맵을 반복하고, 타입 스위치(type switch)를 사용하여 맵의 값들에 구체적인 타입으로 접근할 수 있습니다.

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

이러한 방식으로 타입 안정성의 이점을 누리면서 동시에 알 수 없는 JSON 데이터와 함께 작업할 수 있습니다.

## 참조 타입 (Reference Types)

이전 예제의 데이터를 포함하는 Go 타입을 정의해 보겠습니다:

```go
type FamilyMember struct {
	Name    string
	Age     int
	Parents []string
}

var m FamilyMember
err := json.Unmarshal(b, &m)
```

해당 데이터를 `FamilyMember` 값으로 언마샬링(Unmarshaling)하는 것은 예상대로 작동하지만, 자세히 살펴보면 주목할 만한 일이 일어났음을 알 수 있습니다.
`var` 문을 통해 `FamilyMember` 구조체를 할당했고, 그 값의 포인터를 `Unmarshal`에 전달했지만, 그 당시 `Parents` 필드는 `nil` 슬라이스 값이었습니다.
`Parents` 필드를 채우기 위해 `Unmarshal`은 내부적으로 새로운 슬라이스를 할당했습니다.
이는 `Unmarshal`이 지원하는 참조 타입(포인터, 슬라이스, 맵)을 처리하는 전형적인 방식입니다.

다음 데이터 구조로 언마샬링(unmarshaling)하는 경우를 생각해 보겠습니다.

```
type Foo struct {
	Bar *Bar
}
```

JSON 객체에 `Bar` 필드가 있다면,
`Unmarshal`은 새로운 `Bar`를 할당하고 값을 채웁니다.
그렇지 않다면, `Bar`는 `nil` 포인터 상태로 남게 됩니다.

이로부터 유용한 패턴이 하나 도출됩니다. 몇 가지 서로 다른 메시지 유형을 수신하는 애플리케이션이 있는 경우, 다음과 같이 "receiver" 구조체를 정의할 수 있습니다.

```go
type IncomingMessage struct {
	Cmd *Command
	Msg *Message
}
```

그리고 송신 측은 전달하려는 메시지 유형에 따라 최상위 JSON 객체의 `Cmd` 필드 및/또는 `Msg` 필드를 채울 수 있습니다.
`Unmarshal`은 JSON을 `IncomingMessage` 구조체로 디코딩할 때 JSON 데이터에 존재하는 데이터 구조만 할당합니다.
어떤 메시지를 처리해야 하는지 알기 위해, 프로그래머는 단순히 `Cmd` 또는 `Msg`가 `nil`이 아닌지 확인하면 됩니다.

## 스트리밍 Marshal 및 Unmarshal

[`io.Reader`](/pkg/io#Reader) 및 [`io.Writer`](/pkg/io#Writer) 인터페이스는 Go에서 어디서나 사용되며, HTTP 연결, WebSocket 또는 파일과 같은 리소스에 대한 스트리밍 액세스를 제공합니다.
`MarshalWrite` 및 `UnmarshalRead` 함수를 사용하면 전체 메시지를 담는 중간 `[]byte` 없이 이러한 스트림으로 직접 마샬링(marshaling) 및 언마샬링(unmarshaling)을 수행할 수 있습니다.

```
func MarshalWrite(out io.Writer, in any, opts ...Options) (err error)
func UnmarshalRead(in io.Reader, out any, opts ...Options) (err error)
```

예를 들어, marshal 출력 결과를 표준 출력(standard out)으로 직접 작성할 수 있습니다:

```
err := json.MarshalWrite(os.Stdout, m)
```

## 사용자 정의 Marshal 및 Unmarshal

때로는 기본 마샬링(marshal) 동작이 사용자의 타입에 적합하지 않을 수 있습니다.

예를 들어, 소프트웨어 버전을 설명하는 타입이 있다고 가정해 보겠습니다.

```go
type Version struct {
	Major, Minor, Patch int64
}

v := Version{1, 2, 3}
b, err := json.Marshal(s)
```

이는 구조체 정의에 따라 예상대로 `{"Major":1,"Minor":2,"Patch":3}`로 마샬링되지만, JSON 소비자를 위해서는 "1.2.3"과 같은 버전 문자열이 더 나은 표현 방식일 가능성이 높습니다.

[`MarshalerTo`](/pkg/encoding/json/v2#MarshalerTo) 인터페이스를 구현함으로써, 사용자 정의 JSON 표현을 제공할 수 있습니다.
[`UnmarshalerFrom`](/pkg/encoding/json/v2#UnmarshalerFrom)은 사용자 정의 JSON 표현의 언마샬링(unmarshaling)을 제공합니다.

```
type MarshalerTo interface {
	MarshalJSONTo(*jsontext.Encoder) error
}

type UnmarshalerFrom interface {
	UnmarshalJSONFrom(*jsontext.Decoder) error
}
```

문자열 표현으로 변환하거나 문자열 표현으로부터 변환하기 위해 이러한 메서드들을 구현할 수 있습니다.

```go
func (v Version) MarshalJSONTo(enc *jsontext.Encoder) error {
	return json.MarshalEncode(enc, fmt.Sprintf("%d.%d.%d", v.Major, v.Minor, v.Patch))
}
```

커스텀 마샬링을 통해, 이제 `Version{1, 2, 3}` 값은 `"1.2.3"`으로 마샬링됩니다.

```go
func (v *Version) UnmarshalJSONFrom(dec *jsontext.Decoder) error {
	if k := dec.PeekKind(); k != jsontext.KindString {
		// 값은 반드시 문자열이어야 합니다.
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

커스텀 언마셜링(unmarshaling)을 통해, 이제 `"1.2.3"`은 `Version{1, 2, 3}`으로 언마셜링됩니다.
이 간단한 예제는 정확한 `"major.minor.patch"` 버전 형식을 요구하지만, 더 복잡한 `UnmarshalJSONFrom`을 구현하면 minor 및 patch 버전을 선택 사항으로 만드는 등 유연성을 추가할 수 있습니다.

## 참고 문헌

더 자세한 정보는 [encoding/json/v2](/pkg/encoding/json/v2) 및 [encoding/json/jsontext](/pkg/encoding/json/jsontext) 패키지 문서를 참조하세요.
