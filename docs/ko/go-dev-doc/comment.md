목차:

[패키지](#package)\
 [명령어](#cmd)\
 [타입](#type)\
 [함수](#func)\
 [상수](#const)\
 [변수](#var)\
 [구문](#syntax)\
 [일반적인 실수와 함정](#mistakes)

“Doc comments”(문서 주석)는 최상위 package, const, func, type 및 var 선언 바로 앞에 빈 줄 없이 나타나는 주석을 말합니다.
모든 export된(대문자로 시작하는) 이름에는 문서 주석이 있어야 합니다.

[go/doc](/pkg/go/doc) 및 [go/doc/comment](/pkg/go/doc/comment) 패키지는 Go 소스 코드에서 문서를 추출하는 기능을 제공하며, 다양한 도구들이 이 기능을 활용합니다.
[`go` `doc`](/cmd/go#hdr-Show_documentation_for_package_or_symbol) 명령어는 주어진 패키지나 심볼의 문서 주석을 찾아 출력합니다.
(심볼은 최상위 const, func, type, 또는 var를 의미합니다.)
웹 서버 [pkg.go.dev](https://pkg.go.dev/)는 공개 Go 패키지의 문서를 보여줍니다 (라이선스가 해당 사용을 허용하는 경우).
해당 사이트를 제공하는 프로그램은 [golang.org/x/pkgsite/cmd/pkgsite](https://pkg.go.dev/golang.org/x/pkgsite/cmd/pkgsite)이며, 이는 로컬에서 실행하여 프라이빗 모듈의 문서를 확인하거나 인터넷 연결 없이 문서를 볼 때 사용할 수 있습니다.
언어 서버 [gopls](https://pkg.go.dev/golang.org/x/tools/gopls)는 IDE에서 Go 소스 파일을 편집할 때 문서를 제공합니다.

이 페이지의 나머지 부분에서는 Go doc 주석을 작성하는 방법을 설명합니다.

## 패키지 {#package}

모든 패키지는 해당 패키지를 소개하는 패키지 주석을 가져야 합니다.
이 주석은 패키지 전체와 관련된 정보를 제공하며, 일반적으로 패키지에 대한 기대치를 설정합니다.
특히 규모가 큰 패키지의 경우, 패키지 주석에서 API의 가장 중요한 부분들에 대한 간략한 개요를 제공하고 필요에 따라 다른 문서 주석으로 링크를 연결하는 것이 도움이 될 수 있습니다.

패키지가 간단하다면, 패키지 주석은 간결하게 작성할 수 있습니다.
예를 들어:

// Package path는 슬래시(/)로 구분된 경로를 조작하기 위한 유틸리티 루틴을 구현합니다.
	//
	// path 패키지는 URL 경로와 같이 전방 슬래시로 구분된 경로에만 사용해야 합니다.
	// 이 패키지는 드라이브 문자나 백슬래시(\)가 포함된 Windows 경로를 다루지 않습니다.
	// 운영 체제 경로를 조작하려면 [path/filepath] 패키지를 사용하십시오.
	package path

`[path/filepath]`의 대괄호는 [문서 링크](#links)를 생성합니다.

이 예제에서 볼 수 있듯이, Go 문서 주석은 완전한 문장을 사용합니다.
패키지 주석의 경우, [첫 번째 문장](/pkg/go/doc/#Package.Synopsis)은 “Package <name>”으로 시작해야 함을 의미합니다.

여러 파일로 구성된 패키지의 경우, 패키지 주석은 단 하나의 소스 파일에만 있어야 합니다.
만약 여러 파일에 패키지 주석이 있다면, 이들은 모두 연결되어 전체 패키지를 위한 하나의 커다란 주석을 형성하게 됩니다.

## Commands {#cmd}

커맨드(command)를 위한 패키지 주석도 비슷하지만, 패키지 내의 Go 심볼보다는 프로그램의 동작을 설명합니다.
첫 번째 문장은 관례적으로 프로그램의 이름으로 시작하며, 문장의 시작이므로 첫 글자는 대문자로 씁니다.
예를 들어, [gofmt](/cmd/gofmt)의 패키지 주석을 축약한 버전은 다음과 같습니다.

/*
	Gofmt는 Go 프로그램을 포맷팅합니다.
	들여쓰기에는 탭(tabs)을 사용하고, 정렬에는 공백(blanks)을 사용합니다.
	정렬은 에디터가 고정폭 글꼴(fixed-width font)을 사용한다고 가정합니다.

명시적인 경로가 없으면 표준 입력을 처리합니다. 파일이 지정되면 해당 파일에 대해 작동하고, 디렉터리가 지정되면 해당 디렉터리 내의 모든 .go 파일에 대해 재귀적으로 작동합니다. (마침표로 시작하는 파일은 무시됩니다.) 기본적으로 gofmt는 재포맷된 소스 코드를 표준 출력으로 출력합니다.

사용법:

gofmt [flags] [path ...]

플래그는 다음과 같습니다:

-d
			재포맷된 소스 코드를 표준 출력으로 출력하지 않습니다.
			파일의 포맷이 gofmt와 다를 경우, 차이점(diffs)을 표준 출력으로 출력합니다.
		-w
			재포맷된 소스 코드를 표준 출력으로 출력하지 않습니다.
			파일의 포맷이 gofmt와 다를 경우, gofmt 버전으로 덮어씁니다. 덮어쓰는 동안 오류가 발생하면 자동 백업본을 통해 원래 파일을 복구합니다.

`gofmt`가 표준 입력으로부터 읽을 때, 전체 Go 프로그램 또는 프로그램 조각(fragment)을 모두 허용합니다. 프로그램 조각은 구문적으로 유효한 선언 목록, 문장 목록 또는 표현식이어야 합니다. 이러한 조각을 포맷팅할 때 `gofmt`는 앞부분의 들여쓰기와 앞뒤 공백을 유지하므로, Go 프로그램의 개별 섹션들을 `gofmt`로 파이핑하여 포맷팅할 수 있습니다.
	*/
	package main

주석의 시작 부분은 [semantic linefeeds](https://rhodesmill.org/brandon/2012/one-sentence-per-line/)를 사용하여 작성되었습니다.
이 방식은 각 새 문장이나 긴 구절을 별도의 줄에 배치하여,
코드와 주석이 진화함에 따라 diff를 더 쉽게 읽을 수 있게 합니다.
이후의 단락들은 우연히 이 관례를 따르지 않았으며
수동으로 줄 바꿈이 되었습니다.
귀하의 코드 베이스에 가장 적합한 방식을 사용하시면 됩니다.
어떤 방식이든, `go` `doc`와 `pkgsite`는 문서 주석 텍스트를 출력할 때 자동으로 줄 바꿈을 다시 처리합니다.
예를 들어:

$ go doc gofmt
	Gofmt는 Go 프로그램을 포맷팅합니다. 들여쓰기에는 탭을 사용하고, 정렬에는 공백을 사용합니다. 정렬은 에디터가 고정 폭 글꼴(fixed-width font)을 사용하고 있다고 가정합니다.

명시적인 경로가 없으면 표준 입력을 처리합니다. 파일이 지정되면 해당 파일에 대해 동작하며, 디렉터리가 지정되면 해당 디렉터리 내의 모든 .go 파일에 대해 재귀적으로 동작합니다. (마침표로 시작하는 파일은 무시됩니다.) 기본적으로 `gofmt`는 재형식화된 소스 코드를 표준 출력으로 출력합니다.

사용법:

gofmt [flags] [path ...]

플래그는 다음과 같습니다:

-d
			재정렬된 소스 코드를 표준 출력으로 출력하지 않습니다.
			파일의 포맷이 gofmt와 다를 경우, 표준 출력으로 diff를 출력합니다.
	...

들여쓰기가 된 줄은 사전 서식 지정 텍스트(preformatted text)로 처리됩니다:
이 줄들은 줄 바꿈이 다시 적용되지 않으며,
HTML 및 Markdown 표현 시 코드 글꼴로 출력됩니다.
(자세한 내용은 아래의 [Syntax](#syntax) 섹션에서 확인할 수 있습니다.)

## 타입 {#type}

타입의 문서 주석(doc comment)은 해당 타입의 각 인스턴스가 무엇을 나타내는지 또는 무엇을 제공하는지 설명해야 합니다.
API가 단순하다면, 문서 주석은 매우 짧을 수 있습니다.
예를 들어:

package zip

// Reader는 ZIP 아카이브로부터 콘텐츠를 제공합니다.
	type Reader struct {
		...
	}

기본적으로 프로그래머는 어떤 타입이 한 번에 단 하나의 goroutine에서만 사용되는 것이 안전하다고 생각해야 합니다.
만약 타입이 더 강력한 보장(guarantees)을 제공한다면, 문서 주석에 이를 명시해야 합니다.
예를 들어:

package regexp

// Regexp는 컴파일된 정규 표현식의 표현체입니다.
	// Regexp는 Longest와 같은 설정 메서드를 제외하고,
	// 여러 goroutine에서 동시에 사용해도 안전합니다.
	type Regexp struct {
		...
	}

Go 타입은 제로 값(zero value)이 유용한 의미를 갖도록 설계하는 것을 목표로 해야 합니다.
그 의미가 명확하지 않다면, 문서로 기록해야 합니다. 예를 들어:

package bytes

// Buffer는 Read 및 Write 메서드를 가진 가변 크기의 바이트 버퍼입니다.
	// Buffer의 제로 값(zero value)은 즉시 사용 가능한 빈 버퍼입니다.
	type Buffer struct {
		...
	}

내보내기(exported)된 필드가 있는 구조체의 경우, 문서 주석(doc comment)이나 필드별 주석을 통해 각 내보내기된 필드의 의미를 설명해야 합니다.
예를 들어, 다음 타입의 문서 주석은 필드들에 대해 설명하고 있습니다:

```go
	package io
```

```go
	// LimitedReader는 R에서 읽어오지만, 반환되는 데이터의 양을 
	// N 바이트로 제한합니다. Read를 호출할 때마다 
	// N은 남은 양을 반영하여 업데이트됩니다.
	// N <= 0일 때 Read는 EOF를 반환합니다.
	type LimitedReader struct {
		R   Reader // 하위 reader
		N   int64  // 남은 최대 바이트 수
	}
```

반면, 이 타입의 문서 주석(doc comment)은 설명을 각 필드별 주석에 맡깁니다:

```go
	package comment
```

```go
	// Printer는 문서 주석(doc comment) 프린터입니다.
	// 구조체의 필드들은 출력 메서드를 호출하기 전에 채워 넣을 수 있으며,
	// 이를 통해 출력 프로세스의 세부 사항을 사용자 정의할 수 있습니다.
	type Printer struct {
		// HeadingLevel은 HTML 및 Markdown 제목에 사용되는
		// 중첩 레벨입니다.
		// HeadingLevel이 0이면 기본값으로 레벨 3이 설정되어,
		// <h3> 및 ###이 사용됩니다.
		HeadingLevel int
		...
	}
```

패키지(위) 및 함수(아래)와 마찬가지로, 타입에 대한 문서 주석은 선언된 심볼의 이름으로 시작하는 완전한 문장으로 작성합니다.
명시적인 주체를 지정하면 문구가 더 명확해지며, 웹 페이지나 커맨드 라인에서 텍스트를 검색하기가 더 쉬워집니다.
예를 들어:

$ go doc -all regexp | grep pairs
	pairs within the input string: result[2*n:2*n+2] identifies the indexes
	    FindReaderSubmatchIndex returns a slice holding the index pairs identifying
	    FindStringSubmatchIndex returns a slice holding the index pairs identifying
	    FindSubmatchIndex returns a slice holding the index pairs identifying the
	$

## Funcs {#func}

함수의 문서 주석(doc comment)은 함수가 무엇을 반환하는지, 또는 부수 효과(side effects)를 위해 호출되는 함수의 경우 무엇을 수행하는지를 설명해야 합니다.
이름이 지정된 매개변수와 결과값은 백틱(`)과 같은 특별한 구문 없이 주석에서 직접 참조할 수 있습니다.
(이 관례의 결과로, 일반적인 단어로 오해받을 수 있는 `a`와 같은 이름은 보통 피하게 됩니다.)
예를 들어:

package strconv

// Quote는 s를 나타내는 큰따옴표로 둘러싸인 Go 문자열 리터럴을 반환합니다.
	// 반환된 문자열은 IsPrint에 의해 정의된 제어 문자와 출력 불가능한 문자에 대해
	// Go 이스케이프 시퀀스(\t, \n, \xFF, \u0100)를 사용합니다.
	func Quote(s string) string {
		...
	}

번역할 내용을 제공해 주세요. 영문 Markdown 콘텐츠를 주시면 지침에 따라 정밀하게 한국어로 번역해 드리겠습니다.

package os

// Exit는 주어진 상태 코드로 현재 프로그램을 종료합니다.
	// 관례적으로 코드 0은 성공을, 0이 아닌 값은 에러를 나타냅니다.
	// 프로그램은 즉시 종료되며, deferred 함수들은 실행되지 않습니다.
	//
	// 이식성을 위해 상태 코드는 [0, 125] 범위 내에 있어야 합니다.
	func Exit(code int) {
		...
	}

문서 주석(Doc comments)에서는 일반적으로 boolean을 반환하는 함수를 설명할 때 “reports whether”라는 문구를 사용합니다.
“or not”이라는 문구는 불필요합니다.
예를 들어:

package strings

// HasPrefix는 문자열 s가 prefix로 시작하는지 여부를 보고합니다.
	func HasPrefix(s, prefix string) bool

문서 주석(doc comment)에서 여러 결과 값을 설명해야 하는 경우, 함수 본문에서 해당 이름들을 사용하지 않더라도 결과 값에 이름을 지정하면 문서 주석을 더 이해하기 쉽게 만들 수 있습니다.
예를 들어:

`package io`

```go
	// Copy는 src에서 EOF에 도달하거나 오류가 발생할 때까지 dst로 복사합니다.
	// 작성된 총 바이트 수와 복사 중 발생한 첫 번째 오류(있는 경우)를 반환합니다.
	//
	// Copy가 성공하면 err == EOF가 아닌 err == nil을 반환합니다.
	// Copy는 EOF가 발생할 때까지 src에서 읽도록 정의되어 있으므로,
	// Read에서 발생한 EOF를 보고해야 할 오류로 처리하지 않습니다.
	func Copy(dst Writer, src Reader) (n int64, err error) {
		...
	}
```

반대로, 문서 주석(doc comment)에서 결과에 이름을 붙일 필요가 없는 경우, 프레젠테이션이 복잡해지는 것을 방지하기 위해 위 `Quote` 예제와 같이 코드에서도 보통 생략합니다.

이 규칙들은 일반 함수와 메서드 모두에 적용됩니다.
메서드의 경우, 동일한 리시버 이름을 사용하면 타입의 모든 메서드를 나열할 때 불필요한 변동을 피할 수 있습니다.

$ go doc bytes.Buffer
	package bytes // import "bytes"

```go
type Buffer struct {
		// Has unexported fields.
	}
```
`Buffer`는 `Read` 및 `Write` 메서드를 가진 가변 크기의 바이트 버퍼입니다.
`Buffer`의 제로 값(zero value)은 즉시 사용할 수 있는 빈 버퍼입니다.

```go
func NewBuffer(buf []byte) *Buffer
	func NewBufferString(s string) *Buffer
	func (b *Buffer) Bytes() []byte
	func (b *Buffer) Cap() int
	func (b *Buffer) Grow(n int)
	func (b *Buffer) Len() int
	func (b *Buffer) Next(n int) []byte
	func (b *Buffer) Read(p []byte) (n int, err error)
	func (b *Buffer) ReadByte() (byte, error)
	...
```

이 예제는 타입 `T` 또는 포인터 `*T`를 반환하는 최상위 함수(아마도 추가적인 error 결과와 함께)가 `T`의 생성자라는 가정하에, 타입 `T` 및 해당 메서드들과 함께 표시됨을 보여줍니다.

기본적으로 프로그래머는 최상위 함수(top-level function)가 여러 goroutine에서 호출해도 안전하다고 가정할 수 있으며, 이 사실을 명시적으로 기술할 필요는 없습니다.

반면, 이전 섹션에서 언급했듯이,
메서드 호출을 포함하여 어떤 방식으로든
타입의 인스턴스를 사용하는 것은
일반적으로 한 번에 하나의 고루틴으로 제한된다고 가정합니다.
동시 사용(concurrent use)이 안전한 메서드가
타입의 문서 주석(doc comment)에 명시되어 있지 않다면,
해당 메서드별 주석에 명시해야 합니다.
예를 들어:

package sql

```go
	// Close는 연결을 연결 풀(connection pool)로 반환합니다.
	// Close 이후의 모든 작업은 ErrConnDone을 반환하며 종료됩니다.
	// Close는 다른 작업들과 동시에 호출해도 안전하며, 다른 모든 작업이 완료될 때까지 차단(block)됩니다.
	// 사용 중인 context를 먼저 취소한 다음 Close를 직접 호출하는 것이 유용할 수 있습니다.
	func (c *Conn) Close() error {
		...
	}
```

함수와 메서드의 문서 주석은 해당 연산이 무엇을 반환하거나 수행하는지, 즉 호출자가 알아야 할 세부 사항에 집중해야 한다는 점에 유의하십시오.
특히 특수한 경우(special cases)를 문서화하는 것이 매우 중요할 수 있습니다.
예를 들어:

{{raw `
	package math`}}

```go
// Sqrt는 x의 제곱근을 반환합니다.
//
// 특수 사례는 다음과 같습니다:
//
//	Sqrt(+Inf) = +Inf
//	Sqrt(±0) = ±0
//	Sqrt(x < 0) = NaN
//	Sqrt(NaN) = NaN
	func Sqrt(x float64) float64 {
		...
	}
```

문서 주석(Doc comments)은 현재 구현에 사용된 알고리즘과 같은 내부 세부 사항을 설명해서는 안 됩니다. 이러한 내용은 함수 본문 내부의 주석으로 남겨두는 것이 가장 좋습니다. 다만, 해당 세부 사항이 호출자에게 특히 중요한 경우에는 점근적 시간 또는 공간 복잡도(asymptotic time or space bounds)를 제공하는 것이 적절할 수 있습니다. 예를 들어:

package sort

// Sort는 Less 메서드에 의해 결정된 오름차순으로 데이터를 정렬합니다.
	// n을 결정하기 위해 data.Len을 한 번 호출하며, data.Less와 data.Swap을
	// O(n*log(n))번 호출합니다. 이 정렬은 안정성(stable)을 보장하지 않습니다.
	func Sort(data Interface) {
		...
	}

이 문서 주석은 어떤 정렬 알고리즘이 사용되는지 언급하지 않으므로, 향후 다른 알고리즘을 사용하도록 구현을 변경하기가 더 쉽습니다.

## Consts {#const}

Go의 선언 구문은 선언들을 그룹화하는 것을 허용하며, 이 경우 하나의 문서 주석(doc comment)으로 연관된 상수 그룹을 소개하고 개별 상수는 줄 끝의 짧은 주석으로만 설명할 수 있습니다. 예를 들어:

package scanner // import "text/scanner"

// Scan의 결과는 다음 토큰 중 하나이거나 유니코드 문자입니다.
	const (
		EOF = -(iota + 1)
		Ident
		Int
		Float
		Char
		...
	)

때로는 그룹에 문서 주석(doc comment)이 전혀 필요하지 않을 수도 있습니다. 예를 들어:

package unicode // import "unicode"

```go
const (
		MaxRune         = '\U0010FFFF' // 유효한 최대 유니코드 코드 포인트.
		ReplacementChar = '\uFFFD'     // 유효하지 않은 코드 포인트를 나타냄.
		MaxASCII        = '\u007F'     // 최대 ASCII 값.
		MaxLatin1       = '\u00FF'     // 최대 Latin-1 값.
	)
```

반면에, 그룹화되지 않은 상수는 일반적으로 완전한 문장으로 시작하는 전체 문서 주석(doc comment)이 필요합니다. 예를 들면 다음과 같습니다:

package unicode

// Version은 테이블이 파생된 Unicode 에디션입니다.
	const Version = "13.0.0"

타입이 지정된 상수는 해당 타입의 선언 옆에 표시되며, 그 결과 상수의 그룹 문서 주석 대신 타입의 문서 주석을 사용하는 경우가 많습니다.
예를 들어:

package syntax

// Op은 단일 정규 표현식 연산자입니다.
	type Op uint8

```go
const (
		OpNoMatch        Op = 1 + iota // 어떤 문자열과도 일치하지 않음
		OpEmptyMatch                   // 빈 문자열과 일치
		OpLiteral                      // Runes 시퀀스와 일치
		OpCharClass                    // 범위 쌍 목록으로 해석된 Runes와 일치
		OpAnyCharNotNL                 // 줄바꿈 문자를 제외한 모든 문자와 일치
		...
	)
```

(HTML 표현 방식은 [pkg.go.dev/regexp/syntax#Op](https://pkg.go.dev/regexp/syntax#Op)를 참조하십시오.)

## Vars {#var}

변수의 명명 규칙은 상수의 명명 규칙과 동일합니다.
예를 들어, 다음과 같이 그룹화된 변수 세트가 있습니다:

package fs

// 일반적인 파일 시스템 에러입니다.
	// 파일 시스템에서 반환된 에러는 errors.Is를 사용하여
	// 다음 에러들과 비교하여 테스트할 수 있습니다.
	var (
		ErrInvalid    = errInvalid()    // "invalid argument"
		ErrPermission = errPermission() // "permission denied"
		ErrExist      = errExist()      // "file already exists"
		ErrNotExist   = errNotExist()   // "file does not exist"
		ErrClosed     = errClosed()     // "file already closed"
	)

그리고 단일 변수:

package unicode

// Scripts는 Unicode 스크립트 테이블의 집합입니다.
	var Scripts = map[string]*RangeTable{
		"Adlam":                  Adlam,
		"Ahom":                   Ahom,
		"Anatolian_Hieroglyphs":  Anatolian_Hieroglyphs,
		"Arabic":                 Arabic,
		"Armenian":               Armenian,
		...
	}

## 구문 {#syntax}

Go doc 주석은 단락, 헤딩, 링크, 리스트, 그리고 미리 서식이 지정된 코드 블록을 지원하는 단순한 구문으로 작성됩니다.
소스 파일에서 주석을 가볍고 읽기 쉽게 유지하기 위해, 글꼴 변경이나 raw HTML과 같은 복잡한 기능은 지원하지 않습니다.
Markdown 애호가들은 이 구문을 Markdown의 단순화된 서브셋으로 볼 수 있습니다.

표준 포맷터인 [gofmt](/cmd/gofmt)는 이러한 각 기능에 대해 표준 포맷팅을 사용하도록 문서 주석(doc comments)의 형식을 다시 지정합니다. Gofmt는 소스 코드 내의 주석 작성 방식에 대해 가독성과 사용자 제어를 지향하지만, 일반 소스 코드에서 `1+2 * 3`을 `1 + 2*3`으로 다시 포맷팅하는 것과 유사하게, 특정 주석의 의미론적 의미를 더 명확하게 하기 위해 표현 방식을 조정합니다.

Gofmt는 doc comment의 앞뒤 빈 줄을 제거합니다.
doc comment의 모든 줄이 동일한 공백 및 탭 시퀀스로 시작하는 경우, gofmt는 해당 접두사를 제거합니다.

### 단락 {#paragraphs}

단락은 들여쓰기가 되지 않은 비어 있지 않은 행들의 구간입니다.
우리는 이미 단락의 많은 예시를 살펴보았습니다.

두 개의 연속된 백틱(\` U+0060)은
유니코드 왼쪽 따옴표(“ U+201C)로 해석되며,
두 개의 연속된 작은따옴표(\' U+0027)는
유니코드 오른쪽 따옴표(” U+201D)로 해석됩니다.

Gofmt는 문단 텍스트의 줄 바꿈을 보존하며, 텍스트를 다시 줄 바꿈(rewrap)하지 않습니다.
이를 통해 앞서 살펴본 것과 같이 [semantic linefeeds](https://rhodesmill.org/brandon/2012/one-sentence-per-line/)를 사용할 수 있습니다.
Gofmt는 문단 사이에 중복된 빈 줄이 있을 경우 이를 하나의 빈 줄로 대체합니다.
또한 Gofmt는 연속된 백틱(`)이나 작은따옴표(')를 해당 Unicode 해석으로 다시 형식화합니다.

#### 참고 사항 {#notes}

노트는 `MARKER(uid): body` 형태의 특별한 주석입니다.
MARKER는 노트의 유형을 식별하는 2글자 이상의 대문자 `[A-Z]`로 구성되어야 하며,
uid는 최소 1글자 이상으로, 일반적으로 더 많은 정보를 제공할 수 있는 사람의 사용자 이름입니다.
uid 뒤에 오는 `:`는 선택 사항입니다.

Notes는 pkg.go.dev의 별도 섹션에 수집 및 렌더링됩니다.

예를 들어:

// TODO(user1): 표준 라이브러리 context를 사용하도록 리팩토링
	// BUG(user2): 정리되지 않음
	var ctx context.Context

#### Deprecations {#deprecations}

`Deprecated: `로 시작하는 단락은 사용 중단(deprecation) 공지로 처리됩니다.
일부 도구는 사용 중단된 식별자가 사용될 때 경고를 표시합니다.
[pkg.go.dev](https://pkg.go.dev)에서는 기본적으로 해당 문서들을 숨깁니다.

사용 중단(Deprecation) 공지는 해당 중단에 대한 정보와, 적용 가능한 경우 이를 대체하여 사용할 권장 사항이 뒤따릅니다.
해당 단락이 문서 주석의 마지막 단락일 필요는 없습니다.

예를 들어:

// Package rc4는 RC4 스트림 암호를 구현합니다.
	//
	// Deprecated: RC4는 암호학적으로 취약하며, 레거시 시스템과의 호환성을 
	// 제외하고는 사용해서는 안 됩니다.
	//
	// 이 패키지는 동결되었으며 새로운 기능은 추가되지 않습니다.
	package rc4

// Reset은 키 데이터를 0으로 초기화하여 Cipher를 사용할 수 없게 만듭니다.
	//
	// Deprecated: Reset은 키가 프로세스의 메모리에서 완전히 제거되는 것을 보장할 수 없습니다.
	func (c *Cipher) Reset()

### 헤딩 (Headings) {#headings}

제목은 숫자 기호(U+0023)로 시작하여 공백 하나와 제목 텍스트가 이어지는 줄입니다.
제목으로 인식되려면, 해당 줄에 들여쓰기가 없어야 하며 빈 줄을 통해 인접한 단락 텍스트와 구분되어야 합니다.

예를 들어:

// Package strconv는 기본 데이터 타입의 문자열 표현으로의 변환 및 그 반대의 변환을 구현합니다.
	//
	// # 숫자 변환 (Numeric Conversions)
	//
	// 가장 일반적인 숫자 변환은 [Atoi] (문자열에서 정수로)와 [Itoa] (정수에서 문자열로)입니다.
	...
	package strconv

반면에:

// #이것은 헤딩이 아닙니다. 공백이 없기 때문입니다.
	//
	// # 이것은 헤딩이 아닙니다,
	// # 여러 줄로 나뉘어 있기 때문입니다.
	//
	// # 이것은 헤딩이 아닙니다,
	// 마찬가지로 여러 줄로 나뉘어 있기 때문입니다.
	//
	// 다음 단락은 추가 텍스트가 없으므로 헤딩이 아닙니다:
	//
	// #
	//
	// 빈 줄이 없는 텍스트 구간의 중간에 있는
	// # 이것 또한 헤딩이 아닙니다.
	//
	//     # 이것은 들여쓰기가 되어 있으므로 헤딩이 아닙니다.

# 문법은 Go 1.19에서 추가되었습니다.
Go 1.19 이전에는 특정 조건(가장 눈에 띄는 점은 문장 끝에 구두점이 없어야 한다는 것)을 충족하는 단일 행 단락을 통해 헤딩을 암시적으로 식별했습니다.

Gofmt는 이전 버전의 Go에서 [암시적 헤딩(implicit headings)](https://github.com/golang/proposal/blob/master/design/51082-godocfmt.md#headings)으로 처리되었던 라인들을 `#` 헤딩을 사용하도록 다시 포맷팅합니다.
만약 이러한 재포맷팅이 적절하지 않은 경우—즉, 해당 라인이 헤딩으로 의도된 것이 아닌 경우—이를 문단으로 만드는 가장 쉬운 방법은 마침표나 콜론과 같은 종결 문장 부호를 도입하거나, 해당 라인을 두 줄로 나누는 것입니다.

### 링크 {#links}

들여쓰기가 되지 않은 비어 있지 않은 줄들의 연속이 모든 줄이 “[Text]: URL” 형태일 때 링크 타겟을 정의합니다.
동일한 문서 주석 내의 다른 텍스트에서
“[Text]”는 해당 텍스트를 사용하여 URL로 연결되는 링크를 나타내며, HTML로는
\<a href="URL">Text\</a>가 됩니다.
예를 들어:

// Package json은 [RFC 7159]에 정의된 JSON의 인코딩 및 디코딩을 구현합니다.
	// JSON과 Go 값 사이의 매핑은 Marshal 및 Unmarshal 함수의 문서에 설명되어 있습니다.
	//
	// 이 패키지에 대한 소개는 “[JSON and Go]” 문서를 참조하십시오.
	//
	// [RFC 7159]: https://tools.ietf.org/html/rfc7159
	// [JSON and Go]: https://golang.org/doc/articles/json_and_go.html
	package json

URL을 별도의 섹션에 유지함으로써,
이 형식은 실제 텍스트의 흐름을 최소한으로 방해합니다.
또한 이는 선택 사항인 제목 텍스트를 제외하고,
Markdown의 [shortcut reference link format](https://spec.commonmark.org/0.30/#shortcut-reference-link)과 대략적으로 일치합니다.

해당하는 URL 선언이 없는 경우,
(다음 섹션에서 설명하는 doc 링크를 제외하고)
“[Text]”는 하이퍼링크가 아니며, 표시될 때 대괄호가 그대로 유지됩니다.
각 doc 코멘트는 독립적으로 처리됩니다.
하나의 코멘트 내에 정의된 링크 대상은 다른 코멘트에 영향을 주지 않습니다.

링크 대상 정의 블록이 일반 문단과 섞여 있을 수 있지만, `gofmt`는 모든 링크 대상 정의를 문서 주석의 끝으로 이동시킵니다.

이는 최대 두 개의 블록으로 나뉩니다. 첫 번째 블록에는 주석 내에서 참조된 모든 링크 대상이 포함되며, 그 다음 블록에는 주석에서 참조되지 _않은_ 모든 대상이 포함됩니다. 이렇게 블록을 분리하면 사용되지 않는 대상을 쉽게 발견하여 수정(링크나 정의에 오타가 있는 경우)하거나 삭제(정의가 더 이상 필요 없는 경우)할 수 있습니다.

URL로 인식되는 일반 텍스트는 HTML 렌더링 시 자동으로 링크로 연결됩니다.

### 문서 링크 {#doclinks}

문서 링크(Doc links)는 현재 패키지의 내보내기(exported) 식별자를 참조하기 위한 “[Name1]” 또는 “[Name1.Name2]” 형태의 링크이거나, 다른 패키지의 식별자를 참조하기 위한 “[pkg]”, “[pkg.Name1]” 또는 “[pkg.Name1.Name2]” 형태의 링크입니다.

예를 들어:

package bytes

```go
	// ReadFrom은 EOF가 발생할 때까지 r에서 데이터를 읽어 버퍼에 추가하며,
	// 필요에 따라 버퍼의 크기를 늘립니다. 반환 값 n은 읽은 바이트 수입니다.
	// 읽기 중에 [io.EOF]를 제외한 오류가 발생하면 해당 오류도 함께 반환됩니다.
	// 버퍼가 너무 커지면 ReadFrom은 [ErrTooLarge]와 함께 패닉(panic)을 발생시킵니다.
	func (b *Buffer) ReadFrom(r io.Reader) (n int64, err error) {
		...
	}
```

심볼 링크의 대괄호 텍스트에는 선택적으로 앞에 별표(`*`)를 포함할 수 있어, `[*bytes.Buffer]`와 같은 포인터 타입을 쉽게 참조할 수 있습니다.

다른 패키지를 참조할 때, “pkg”는 전체 import 경로이거나 기존 import의 가정된 패키지 이름(assumed package name)일 수 있습니다. 가정된 패키지 이름은 이름을 변경하여 import한 경우의 식별자이거나, [goimports에 의해 가정된 이름](https://pkg.go.dev/golang.org/x/tools/internal/imports#ImportPathToAssumedName)입니다. (goimports는 이러한 가정이 올바르지 않을 때 이름을 변경하여 삽입하므로, 이 규칙은 기본적으로 거의 모든 Go 코드에 적용됩니다.)

예를 들어, 현재 패키지가 `encoding/json`을 import하고 있다면, `encoding/json`의 `Decoder` 문서로 링크를 걸기 위해 `[encoding/json.Decoder]` 대신 `[json.Decoder]`라고 쓸 수 있습니다.

만약 패키지 내의 서로 다른 소스 파일들이 동일한 이름을 사용하여 서로 다른 패키지를 import하고 있다면, 이러한 약칭은 모호하므로 사용할 수 없습니다.

“pkg”는 도메인 이름(점(.)이 포함된 경로 요소)으로 시작하거나 표준 라이브러리의 패키지([os], [encoding/json] 등) 중 하나인 경우에만 전체 임포트 경로로 간주됩니다.
예를 들어, `[os.File]`과 `[example.com/sys.File]`은 문서 링크이지만(후자는 깨진 링크가 됩니다), `[os/sys.File]`은 표준 라이브러리에 os/sys 패키지가 없으므로 링크가 아닙니다.

map, generics, array 타입과 관련된 문제를 방지하기 위해, doc link의 앞뒤에는 반드시 문장 부호, 공백, 탭, 또는 줄의 시작이나 끝이 있어야 합니다. 예를 들어, “map[ast.Expr]TypeAndValue”라는 텍스트는 doc link를 포함하고 있지 않습니다.

### 리스트 {#lists}

리스트는 들여쓰기된 줄이나 빈 줄의 범위로,
(다음 섹션에서 설명하는 대로, 그렇지 않았다면 코드 블록이 되었을 내용입니다)
그중 첫 번째 들여쓰기된 줄이 불렛 리스트 마커(bullet list marker) 또는 번호 매기기 리스트 마커(numbered list marker)로 시작하는 것을 말합니다.

글머리 기호 목록 마커는 별표, 플러스, 대시 또는 유니코드 글머리 기호
(*, +, -, •; U+002A, U+002B, U+002D, U+2022)
뒤에 공백이나 탭, 그리고 텍스트가 이어지는 형태입니다.
글머리 기호 목록에서 글머리 기호 목록 마커로 시작하는 각 줄은 새로운 목록 항목을 시작합니다.

예를 들어:

package url

// PublicSuffixList는 도메인의 퍼블릭 접미사(public suffix)를 제공합니다. 예를 들어:
	//   - "example.com"의 퍼블릭 접미사는 "com"입니다.
	//   - "foo1.foo2.foo3.co.uk"의 퍼블릭 접미사는 "co.uk"입니다.
	//   - "bar.pvt.k12.ma.us"의 퍼블릭 접미사는 "pvt.k12.ma.us"입니다.
	//
	// PublicSuffixList의 구현체는 여러 goroutine에서 동시에 사용해도 안전해야 합니다.
	//
	// 항상 ""를 반환하는 구현체도 유효하며 테스트 시 유용할 수 있지만, 보안상 안전하지 않습니다.
	// 이는 foo.com의 HTTP 서버가 bar.com에 대한 쿠키를 설정할 수 있음을 의미하기 때문입니다.
	//
	// 퍼블릭 접미사 리스트 구현체는 golang.org/x/net/publicsuffix 패키지에 포함되어 있습니다.
	type PublicSuffixList interface {
		...
	}

번호 매기기 목록 마커는 길이에 상관없는 십진수 뒤에 마침표 또는 오른쪽 괄호가 오고, 그 뒤에 공백이나 탭, 그리고 텍스트가 이어지는 형태입니다.
번호 매기기 목록에서 번호 목록 마커로 시작하는 각 줄은 새로운 목록 항목을 시작합니다.
항목 번호는 그대로 유지되며, 절대 다시 번호를 매기지 않습니다.

예를 들어:

package path

// Clean은 순수하게 어휘적 처리(lexical processing)를 통해 path와 동일한 최단 경로 이름을 반환합니다.
// 이 함수는 더 이상 처리할 수 없을 때까지 다음 규칙들을 반복적으로 적용합니다:
//
//  1. 여러 개의 슬래시를 단일 슬래시로 대체합니다.
//  2. 각 . 경로 이름 요소(현재 디렉터리)를 제거합니다.
//  3. 각 내부 .. 경로 이름 요소(부모 디렉터리)와 그 앞에 오는 non-.. 요소를 함께 제거합니다.
//  4. 루트 경로로 시작하는 .. 요소를 제거합니다:
//     즉, 경로 시작 부분의 "/.."를 "/"로 대체합니다.
//
// 반환된 경로는 루트 "/"인 경우에만 슬래시로 끝납니다.
//
// 이 처리 결과가 빈 문자열인 경우, Clean은 문자열 "."를 반환합니다.
//
// 참고: Rob Pike, “[Lexical File Names in Plan 9].”
//
// [Lexical File Names in Plan 9]: https://9p.io/sys/doc/lexnames.html
	func Clean(path string) string {
		...
	}

목록 항목에는 코드 블록이나 중첩된 목록 없이 단락만 포함됩니다.
이렇게 하면 공백 계산의 미묘한 차이나 일관성 없는 들여쓰기에서 탭이 몇 개의 공백으로 계산되는지에 대한 문제를 피할 수 있습니다.

Gofmt는 글머리 기호 목록을 다음과 같이 다시 형식화합니다.
글머리 기호 마커로 대시(`-`)를 사용하고,
대시 앞에 두 칸의 들여쓰기를 적용하며,
이어지는 줄에는 네 칸의 들여쓰기를 적용합니다.

Gofmt는 번호 매기기 목록(numbered lists)을 숫자 앞에 공백 한 칸, 숫자 뒤에 마침표, 그리고 이어지는 줄에는 4칸의 들여쓰기를 사용하도록 다시 서식을 지정합니다.

Gofmt는 리스트와 그 앞의 단락 사이의 빈 줄을 유지하지만, 반드시 필요로 하지는 않습니다.
리스트와 그 뒤에 오는 단락 또는 헤더 사이에는 빈 줄을 삽입합니다.

### 코드 블록 {#code}

코드 블록은 글머리 기호 목록 표시자나 번호 매기기 목록 표시자로 시작하지 않는, 들여쓰기가 되었거나 빈 줄로 이루어진 구간입니다.
이는 미리 서식 지정된 텍스트(HTML의 `<pre>` 블록)로 렌더링됩니다.

코드 블록에는 종종 Go 코드가 포함됩니다. 예를 들어:

```go
	package sort
```

// Search는 이진 탐색을 사용합니다...
	//
	// 좀 더 기발한 예시로, 이 프로그램은 당신의 숫자를 맞춥니다:
	//
	//	func GuessingGame() {
	//		var s string
	//		fmt.Printf("0에서 100 사이의 정수를 선택하세요.\n")
	//		answer := sort.Search(100, func(i int) bool {
	//			fmt.Printf("선택한 숫자가 %d보다 작거나 같습니까? ", i)
	//			fmt.Scanf("%s", &s)
	//			return s != "" && s[0] == 'y'
	//		})
	//		fmt.Printf("당신의 숫자는 %d입니다.\n", answer)
	//	}
	func Search(n int, f func(int) bool) int {
		...
	}
`}}

물론, 코드 블록에는 코드 외에도 미리 서식이 지정된 텍스트가 포함되는 경우가 많습니다. 예를 들면 다음과 같습니다:

```go
	package path
```

// Match는 name이 쉘 패턴과 일치하는지 여부를 보고합니다.
	// 패턴 구문은 다음과 같습니다:
	//
	//	pattern:
	//		{ term }
	//	term:
	//		'*'         '/'가 아닌 임의의 문자 시퀀스와 일치
	//		'?'         '/'가 아닌 임의의 단일 문자와 일치
	//		'[' [ '^' ] { character-range } ']'
	//		            문자 클래스 (비어 있지 않아야 함)
	//		c           문자 c와 일치 (c != '*', '?', '\\', '[')
	//		'\\' c      문자 c와 일치
	//
	//	character-range:
	//		c           문자 c와 일치 (c != '\\', '-', ']')
	//		'\\' c      문자 c와 일치
	//		lo '-' hi   lo <= c <= hi인 문자 c와 일치
	//
	// Match는 pattern이 name의 부분 문자열이 아닌 전체와 일치해야 합니다.
	// 반환될 수 있는 유일한 오류는 pattern이 잘못 형성되었을 때의 [ErrBadPattern]입니다.
	func Match(pattern, name string) (matched bool, err error) {
		...
	}
`}}

Gofmt는 코드 블록의 모든 줄을 하나의 탭으로 들여쓰며, 공백이 아닌 줄들이 공통으로 가지고 있는 다른 모든 들여쓰기를 대체합니다.
또한 Gofmt는 각 코드 블록의 앞과 뒤에 빈 줄을 삽입하여, 코드 블록을 주변 단락 텍스트와 명확하게 구분합니다.

### 지시어 (Directives) {#directives}

`//go:generate`와 같은 지시어 주석(directive comments)은 문서 주석(doc comment)의 일부로 간주되지 않으며, 렌더링된 문서에서 제외됩니다.
Gofmt는 지시어 주석을 문서 주석의 끝으로 이동시키며, 그 앞에 빈 줄을 추가합니다.
예를 들어:

package regexp

```go
// Op은 단일 정규 표현식 연산자입니다.
//
//go:generate stringer -type Op -trimprefix Op
type Op uint8
```

지시어 주석(directive comment)은 정규 표현식 `//(line |extern |export |[a-z0-9]+:[a-z0-9])`로 시작하는 줄을 의미합니다.

도구는 `//toolname:directive arguments` 형식을 사용하여 자체 지시어 주석을 정의할 수 있습니다.
도구 지시어는 정규 표현식 `//([a-z0-9]+):([a-z0-9]\PZ*)($|\pZ+)(.*)`와 일치하며, 여기서 첫 번째 그룹은 도구 이름이고 두 번째 그룹은 지시어 이름입니다.
선택적 인자는 하나 이상의 유니코드 공백 문자로 지시어 이름과 구분됩니다.
각 도구는 자체적인 인자 구문을 정의할 수 있지만, 일반적인 관례는 공백으로 구분된 인자들의 시퀀스이며, 여기서 인자는 일반 단어(bare word), 큰따옴표로 묶인 Go 문자열, 또는 백틱으로 묶인 Go 문자열일 수 있습니다.
도구 이름 `go`는 Go 툴체인에서 사용하도록 예약되어 있습니다.

[`go/ast.ParseDirective`](/pkg/go/ast#ParseDirective) 함수와 관련 타입들은 도구 지시어(tool directive) 구문을 파싱합니다.

## 일반적인 실수와 함정 {#mistakes}

문서 주석(doc comment)에서 들여쓰기가 되었거나 빈 줄로 이루어진 모든 구간을 코드 블록으로 렌더링하는 규칙은 Go의 아주 초기 시절부터 시작되었습니다.
안타깝게도 gofmt에서 문서 주석에 대한 지원이 부족하여, 코드 블록을 만들 의도 없이 들여쓰기를 사용한 기존 주석들이 많이 생성되었습니다.

예를 들어, 들여쓰기가 되지 않은 이 리스트는 godoc에 의해 항상 세 줄의 단락과 그 뒤를 잇는 한 줄의 코드 블록으로 해석되었습니다:

`package http`

// cancelTimerBody는 rc를 래핑하여 다음 두 가지 기능을 제공하는 io.ReadCloser입니다:
	// 1) Read 에러 발생 시 또는 close 시, stop 함수가 호출됩니다.
	// 2) Read 실패 시, reqDidTimeout이 true라면 에러를 래핑하고
	//    타임아웃이 발생한 net.Error로 표시합니다.
	type cancelTimerBody struct {
		...
	}

이것은 항상 `go` `doc`에서 다음과 같이 렌더링되었습니다:

`cancelTimerBody`는 `rc`를 래핑하며 다음과 같은 두 가지 기능을 가진 `io.ReadCloser`입니다:
	1) `Read` 에러가 발생하거나 닫힐 때, `stop` 함수가 호출됩니다. 2) `Read` 실패 시,
	`reqDidTimeout`이 true이면 에러가 래핑되어

타임아웃이 발생한 `net.Error`로 표시됩니다.

마찬가지로, 이 주석의 명령은 한 줄의 단락과 그 뒤를 잇는 한 줄의 코드 블록으로 구성됩니다:

package smtp

// localhostCert는 src/crypto/tls에서 생성된 PEM 인코딩된 TLS 인증서입니다:
	//
	// go run generate_cert.go --rsa-bits 1024 --host 127.0.0.1,::1,example.com \
	//     --ca --start-date "Jan 1 00:00:00 1970" --duration=1000000h
	var localhostCert = []byte(`...`)

이 내용은 `go` `doc`에서 다음과 같이 렌더링됩니다:

localhostCert는 `src/crypto/tls`에서 생성된 PEM 인코딩된 TLS 인증서입니다:

go run generate_cert.go --rsa-bits 1024 --host 127.0.0.1,::1,example.com \

--ca --start-date "Jan 1 00:00:00 1970" --duration=1000000h

그리고 이 주석은 두 줄의 단락(두 번째 줄은 “{”)이며,
그 뒤로 여섯 줄의 들여쓰기 된 코드 블록과 한 줄의 단락(“}”)이 이어집니다.

// 네트워크상에서 JSON은 다음과 같은 형태가 됩니다:
	// {
	//	"kind":"MyAPIObject",
	//	"apiVersion":"v1",
	//	"myPlugin": {
	//		"kind":"PluginA",
	//		"aOption":"foo",
	//	},
	// }

그리고 이것은 `go` `doc`에서 다음과 같이 렌더링됩니다:

네트워크 상에서 JSON은 다음과 같은 형태가 됩니다: {

"kind":"MyAPIObject",
	    "apiVersion":"v1",
	    "myPlugin": {
	    	"kind":"PluginA",
	    	"aOption":"foo",
	    },

제공해주신 원문 내용이 없습니다. 번역할 Markdown 콘텐츠를 입력해 주세요. 기술적인 맥락을 유지하며 정확하게 한국어로 번역해 드리겠습니다.

또 다른 흔한 실수는 들여쓰기가 되지 않은 Go 함수 정의나, 마찬가지로 “{”와 “}”로 묶인 블록 문장이었습니다.

Go 1.19의 `gofmt`에 도입된 문서 주석(doc comment) 재형성 기능은 코드 블록 주변에 빈 줄을 추가함으로써 다음과 같은 실수들을 더 쉽게 발견할 수 있게 해줍니다.

2022년의 분석에 따르면, 공개 Go 모듈 내 문서 주석 중 Go 1.19 초안의 `gofmt`에 의해 서식이 변경된 것은 단 3%에 불과했습니다.
이러한 주석들만으로 한정했을 때, `gofmt`의 서식 변경 중 약 87%는 사람이 주석을 읽으며 추론하는 구조를 그대로 유지했습니다.
약 6%는 들여쓰기가 되지 않은 목록, 들여쓰기가 되지 않은 다중 행 셸 명령어, 그리고 들여쓰기가 되지 않은 중괄호 구분 코드 블록과 같은 사례들로 인해 제대로 처리되지 않았습니다.

이 분석에 따르면, Go 1.19 `gofmt`는 들여쓰기가 되지 않은 줄을 인접한 들여쓰기 목록이나 코드 블록으로 병합하기 위해 몇 가지 휴리스틱을 적용합니다.
이러한 조정과 함께, Go 1.19 `gofmt`는 위의 예제들을 다음과 같이 재포맷합니다:

// cancelTimerBody는 rc를 래핑하여 다음 두 가지 기능을 제공하는 io.ReadCloser입니다:
	//  1. Read 에러 발생 시 또는 close 시 stop 함수가 호출됩니다.
	//  2. Read 실패 시 reqDidTimeout이 true라면, 에러를 래핑하여
	//     타임아웃이 발생한 net.Error로 표시합니다.

// localhostCert는 src/crypto/tls에서 생성된 PEM 인코딩된 TLS 인증서입니다:
	//
	//	go run generate_cert.go --rsa-bits 1024 --host 127.0.0.1,::1,example.com \
	//	    --ca --start-date "Jan 1 00:00:00 1970" --duration=1000000h

// 네트워크 전송 시, JSON은 다음과 같은 형태가 됩니다:
	//
	//	{
	//		"kind":"MyAPIObject",
	//		"apiVersion":"v1",
	//		"myPlugin": {
	//			"kind":"PluginA",
	//			"aOption":"foo",
	//		},
	//	}

이러한 서식 변경은 의미를 더 명확하게 할 뿐만 아니라, 이전 버전의 Go에서도 문서 주석(doc comments)이 올바르게 렌더링되도록 합니다.
만약 휴리스틱이 잘못된 결정을 내린 경우, 빈 줄을 삽입하여 단락 텍스트와 비단락 텍스트를 명확하게 분리함으로써 이를 오버라이드할 수 있습니다.

이러한 휴리스틱을 적용하더라도, 렌더링을 수정하기 위해 기존의 다른 주석들을 수동으로 조정해야 할 것입니다.
가장 흔한 실수는 들여쓰기가 되지 않은 텍스트 줄이 줄바꿈되었을 때 이를 들여쓰는 것입니다.
예를 들어:

// TODO 이 설계를 다시 검토하십시오. 해당 노드들을 한 번만 순회하는 것이 합리적일 수 있습니다.

// 문서에 따르면:
	// "이미지 파일 내 섹션의 raw 데이터를 정렬하는 데 사용되는 정렬 계수(바이트 단위)입니다.
	// 값은 512에서 64K 사이의 2의 거듭제곱이어야 합니다."

이 두 경우 모두 마지막 줄이 들여쓰기 되어 있어 코드 블록으로 처리되었습니다.
해결 방법은 해당 줄의 들여쓰기를 제거하는 것입니다.

또 다른 흔한 실수는 리스트나 코드 블록에서 줄 바꿈된 들여쓰기 라인을 다시 들여쓰지 않는 것입니다.
예를 들어:

// 이 에러 모델의 사용 사례는 다음과 같습니다:
	//
	//   - 부분적 에러(Partial errors). 서비스가 클라이언트에 부분적 에러를 반환해야 하는 경우,
	//     일반 응답 내에 `Status`를 포함시켜 부분적 에러를 나타낼 수 있습니다.
	//
	//   - 워크플로우 에러(Workflow errors). 일반적인 워크플로우는 여러 단계로 구성됩니다. 각 단계는
	//     에러 보고를 위한 `Status` 메시지를 가질 수 있습니다.

해결 방법은 줄 바꿈된 행들을 들여쓰기하는 것입니다.

Go doc 주석은 중첩 리스트(nested lists)를 지원하지 않으므로, gofmt가 이를 다시 포맷팅합니다.

// 여기에 리스트가 있습니다:
	//
	//  - 항목 1.
	//    * 하위 항목 1.
	//    * 하위 항목 2.
	//  - 항목 2.
	//  - 항목 3.

번역할 내용을 제공해 주세요. 내용을 보내주시면 요청하신 지침에 따라 기술적으로 정확하게 한국어로 번역해 드리겠습니다.

// 여기 리스트가 있습니다:
	//
	//  - 항목 1.
	//  - 하위 항목 1.
	//  - 하위 항목 2.
	//  - 항목 2.
	//  - 항목 3.

텍스트를 다시 작성하여 중첩 목록을 피하는 것이 일반적으로 문서 품질을 개선하며 가장 좋은 해결책입니다.
또 다른 잠재적인 해결 방법은 목록 마커를 혼용하는 것입니다. 불렛 마커는 번호 매기기 목록에서 목록 항목을 생성하지 않으며, 그 반대의 경우도 마찬가지이기 때문입니다.
예를 들어:

// 다음은 목록입니다:
	//
	//  1. 항목 1.
	//
	//     - 하위 항목 1.
	//
	//     - 하위 항목 2.
	//
	//  2. 항목 2.
	//
	//  3. 항목 3.
