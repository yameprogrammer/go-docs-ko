<!--{
  "제목": "가이드: govulncheck을 사용하여 취약한 종속성을 찾고 수정하기",
  "목차 숨기기": true,
  "빵 크럼": true
}-->

Govulncheck는 저소음 도구로, Go 프로젝트의 취약한 의존성을 찾고 해결하는 데 도움을 줍니다. 이는 프로젝트의 의존성을 스캔하여 알려진 취약점을 찾고, 그런 다음 해당 취약점에 대한 직접적이거나 간접적인 호출을 코드에서 식별합니다.

이 튜토리얼에서는 `govulncheck`을 사용하여 간단한 프로그램을 스캔하는 방법을 배우게 됩니다. 또한, 취약점을 우선순위로 지정하고 평가하는 방법을 배우므로, 가장 중요한 취약점을 먼저 수정하는 데 집중할 수 있습니다.

자세한 내용은 다음 [govulncheck 문서](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)를 참조하십시오.
또한, Go를 위한 취약점 관리 관련 이 [블로그 게시물](/blog/vuln)도 참고하십시오.
또한, 여러분의 의견을 [알려주시면 감사하겠습니다](/s/govulncheck-feedback).

## 필수 조건

- **Go.** 이 튜토리얼을 따라하려면 Go의 최신 버전을 사용하는 것을 권장합니다.
  설치 지침은 [Installing Go](/doc/install)를 참조하세요.
- **코드 편집기.** 사용 중인 어떤 편집기든 괜찮습니다.
- **명령 터미널.** Go는 Linux 및 Mac에서 어떤 터미널에서도, 그리고 Windows의 PowerShell 또는 cmd에서도 잘 작동합니다.

이 튜토리얼에서는 다음 단계를 안내합니다:

1. 취약점이 있는 의존성을 포함하는 샘플 Go 모듈을 생성합니다.
2. `govulncheck` 설치 및 실행
3. 취약점 평가
4. 취약한 의존성 업그레이드

## 취약점이 있는 의존성을 포함하는 샘플 Go 모듈 만들기

**1단계.** 먼저, `vuln-tutorial`이라는 새 폴더를 만들고 Go 모듈을 초기화합니다.
(Go 모듈에 익숙하지 않으신 경우, [go.dev/doc/tutorial/create-module](go.dev/doc/tutorial/create-module)를 참조하십시오.)

홈 디렉토리에서 다음 명령을 실행합니다:

```
$ mkdir vuln-tutorial
$ cd vuln-tutorial
$ go mod init vuln.tutorial
```

**2단계.** `vuln-tutorial` 폴더 내에 `main.go`라는 파일을 생성하고, 다음 코드를 복사합니다:

```
패키지 main

import (
        "fmt"
        "os"

        "golang.org/x/text/language"
)

함수 main() {
        for _, arg := range os.Args[1:] {
                tag, err := language.Parse(arg)
                if err != nil {
                        fmt.Printf("%s: 오류: %v\n", arg, err)
                } else if tag == language.Und {
                        fmt.Printf("%s: 정의되지 않음\n", arg)
                } else {
                        fmt.Printf("%s: 태그 %s\n", arg, tag)
                }
        }
}
```

이 샘플 프로그램은 명령줄 인수로 언어 태그 목록을 받아 각 태그에 대해 성공적으로 파싱되었는지, 태그가 정의되지 않았는지, 또는 태그 파싱 중 오류가 발생했는지 여부를 나타내는 메시지를 출력합니다.

**3단계.** `go mod tidy`를 실행합니다. 이 명령은 이전 단계에서 `main.go`에 추가한 코드에 필요한 모든 종속성을 `go.mod` 파일에 채웁니다.

`vuln-tutorial` 폴더에서 다음 명령을 실행합니다:

```
go mod tidy
```

```markdown
## 개요

이 문서는 Go 언어에서 `net/http` 패키지를 사용하여 HTTP 요청을 보내는 방법에 대한 가이드입니다.

## HTTP 요청 보내기

`net/http` 패키지를 사용하여 HTTP 요청을 보내려면 다음 단계를 따르세요.

1.  **패키지 가져오기:**

    ```go
    package main

    import (
    	"fmt"
    	"net/http"
    )
    ```

2.  **요청 생성:**

    `http.Request` 구조체를 사용하여 HTTP 요청을 생성합니다.

    ```go
    req, err := http.NewRequest("GET", "https://example.com", nil)
    if err != nil {
    	fmt.Println("요청 생성 오류:", err)
    	return
    }
    ```

3.  **요청 설정:**

    필요에 따라 요청 헤더를 설정할 수 있습니다.

    ```go
    req.Header.Set("User-Agent", "Mozilla/5.0")
    ```

4.  **요청 보내기:**

    `http.Client.Do()` 메서드를 사용하여 요청을 보냅니다.

    ```go
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
    	fmt.Println("요청 보내기 오류:", err)
    	return
    }
    defer resp.Body.Close()
    ```

5.  **응답 처리:**

    응답 상태 코드를 확인하고, 응답 본문을 처리합니다.

    ```go
    fmt.Println("상태 코드:", resp.StatusCode)
    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
    	fmt.Println("응답 읽기 오류:", err)
    	return
    }
    fmt.Println("응답 내용:", string(body))
    ```

## 예제 코드

다음은 간단한 예제 코드입니다.

```go
package main

import (
	"fmt"
	"net/http"
)

func main() {
	req, err := http.NewRequest("GET", "https://example.com", nil)
	if err != nil {
		fmt.Println("요청 생성 오류:", err)
		return
	}

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Println("요청 보내기 오류:", err)
		return
	}

	defer resp.Body.Close()

	fmt.Println("상태 코드:", resp.StatusCode)
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("응답 읽기 오류:", err)
		return
	}
	fmt.Println("응답 내용:", string(body))
}
```

## 추가 정보

*   [net/http 패키지](https://pkg.go.dev/net/http)
*   [go.dev](https://go.dev/)
```

```markdown
go: golang.org/x/text 패키지의 모듈을 찾았습니다: golang.org/x/text/language
go: golang.org/x/text v0.9.0을 다운로드합니다.
go: golang.org/x/text/language를 golang.org/x/text v0.9.0에서 찾았습니다.
```

**4단계.** `go.mod` 파일을 열어 다음 내용과 일치하는지 확인하십시오:

```
모듈 vuln.tutorial

go 1.20

require golang.org/x/text v0.9.0
```

**5단계.** `golang.org/x/text`의 버전을 v0.3.5로 다운그레이드합니다. 이 버전에는 알려진 취약점이 포함되어 있습니다. 다음 명령을 실행합니다:

```
$ go get golang.org/x/text@v0.3.5
```

```markdown
# 소개

이 문서는 Go 패키지, 식별자, URL, 명령 및 코드 스니펫에 대한 설명을 제공합니다.

## 테이블

| 항목 | 설명 |
|---|---|
| Go 패키지 | Go 패키지 설명 |
| 식별자 | 식별자 설명 |
| URL | URL 설명 |
| 명령 | 명령 설명 |
| 코드 스니펫 | 코드 스니펫 설명 |

## 목록

* Go 패키지를 사용하는 방법
* Go 패키지를 설치하는 방법
* Go 패키지를 사용하는 예제

## 코드

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, world!")
}
```

## 링크

* [Go 공식 웹사이트](https://golang.org/)
* [Go 패키지 설명](https://pkg.go.dev/)
* [Go 명령 설명](https://github.com/golang/tools/tree/master/cmd/go)
```

```
go: downgrading golang.org/x/text from v0.9.0 => v0.3.5
```

`go.mod` 파일은 다음과 같이 읽어야 합니다:

```
모듈 vuln.tutorial

go 1.20

require golang.org/x/text v0.3.5
```

자, 이제 govulncheck를 실제로 사용해 보겠습니다.

## 설치 및 govulncheck 실행 방법

**1. 설치**

govulncheck를 설치하려면 다음 명령을 사용합니다.

```bash
go install github.com/github/govulncheck/cmd/govulncheck
```

**2. 실행**

govulncheck를 실행하려면 다음 명령을 사용합니다.

```bash
govulncheck --version
```

이 명령은 govulncheck 버전 정보를 표시합니다.

**3. 사용 예시**

```bash
govulncheck -all
```

이 명령은 프로젝트의 모든 Go 모듈을 스캔합니다.

**4. 추가 정보**

*   govulncheck에 대한 자세한 내용은 [공식 문서](https://github.com/github/govulncheck)를 참조하십시오.
*   도움말 메시지를 보려면 `govulncheck --help`를 실행하십시오.

**6단계.** `go install` 명령어를 사용하여 govulncheck를 설치합니다:

```
$ go install golang.org/x/vuln/cmd/govulncheck@최신
```

**7단계.** 분석하려는 폴더에서 (이 경우 `vuln-tutorial`) 다음 명령을 실행합니다:

```
$ govulncheck ./...
```

```markdown
# 소개

이 문서는 Go 언어의 기본적인 사용법을 안내합니다.

## 설치

Go를 설치하려면 다음 단계를 따르세요.

1.  [Go 공식 웹사이트](https://go.dev/dl/)에서 Go를 다운로드합니다.
2.  다운로드한 파일을 실행하여 Go를 설치합니다.
3.  터미널에서 `go version` 명령을 실행하여 Go가 제대로 설치되었는지 확인합니다.

## Hello, World!

다음은 Go로 작성된 "Hello, World!" 프로그램입니다.

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

이 프로그램을 컴파일하고 실행하려면 다음 명령을 사용하세요.

```bash
go run hello.go
```

## 변수

Go에서 변수는 다음과 같이 선언합니다.

```go
var x int
x = 10
```

## 함수

Go에서 함수는 다음과 같이 정의합니다.

```go
func add(a int, b int) int {
    return a + b
}
```

## 구조체

Go에서 구조체는 다음과 같이 정의합니다.

```go
type Person struct {
    Name string
    Age  int
}
```

## 테이블

다음은 Go에서 테이블을 사용하는 예입니다.

```go
package main

import "fmt"

func main() {
    table := map[string]int{
        "apple":  1,
        "banana": 2,
        "orange": 3,
    }

    fmt.Println(table["apple"])
    fmt.Println(table["banana"])
    fmt.Println(table["orange"])
}
```

## 리스트

다음은 Go에서 리스트를 사용하는 예입니다.

```go
package main

import "fmt"

func main() {
    list := []int{1, 2, 3}

    fmt.Println(list[0])
    fmt.Println(list[1])
    fmt.Println(list[2])
}
```

## 인라인 코드

다음은 인라인 코드를 사용하는 예입니다.

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, " + "World!")
}
```

## 코드 펜스

다음은 코드 펜스를 사용하는 예입니다.

```go
package main

import "fmt"

func main() {
    fmt.Println(
        "Hello, " +
        "World!",
    )
}
```
```

`govulncheck`는 실험적인 도구입니다. 피드백은 https://go.dev/s/govulncheck-feedback 에서 공유해주세요.

`go1.20.3` 및 `govulncheck@v0.0.0`를 사용하여
`https://vuln.go.dev` (2023-04-18 21:32:26 +0000 UTC에 마지막 수정) 에서 제공되는 취약점 데이터를 활용합니다.

코드와 1개의 의존 모듈에 걸쳐 46개의 패키지를 스캔하여 알려진 취약점을 찾고 있습니다...
코드에는 1개의 모듈에서 1개의 취약점이 발견되었습니다.

취약점 #1: GO-2021-0113
잘못된 인덱스 계산으로 인해 잘못 형식화된
언어 태그가 범위를 벗어난 읽기를 통해 `Parse`를 패닉 상태로 만들 수 있습니다.
`Parse`를 사용하여 신뢰할 수 없는 사용자 입력을 처리하는 경우, 이를
서비스 거부 공격의 벡터로 사용할 수 있습니다.

자세한 정보: https://pkg.go.dev/vuln/GO-2021-0113

모듈: golang.org/x/text
존재하는 위치: golang.org/x/text@v0.3.5
수정된 버전: golang.org/x/text@v0.3.7

코드 내 호출 스택:
  main.go:12:29: vuln.tutorial.main이 golang.org/x/text/language.Parse를 호출

=== 정보 ===

수입하는 패키지에 1개의 취약점이 발견되었지만, 해당 취약점 사용으로 이어지는 호출 스택은 없습니다.
따라서 조치를 취할 필요가 없을 수 있습니다. 자세한 내용은 https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck 를 참조하세요.

취약점 #1: GO-2022-1059
공격자는 `ParseAcceptLanguage`가 상당한 시간이 소요되도록 Accept-Language 헤더를 조작하여
서비스 거부를 유발할 수 있습니다.
자세한 정보: https://pkg.go.dev/vuln/GO-2022-1059
존재하는 위치: golang.org/x/text@v0.3.5
수정된 버전: golang.org/x/text@v0.3.8

### 출력 해석

*참고: Go의 최신 버전을 사용하지 않는 경우, 표준 라이브러리에서 추가적인 취약점을 발견할 수 있습니다.

우리 코드에는 다음과 같은 취약점이 있습니다:
[GO-2021-0113](https://pkg.go.dev/vuln/GO-2021-0113),
이는 `golang.org/x/text/language`의 `Parse` 함수를 취약한 버전(v0.3.5)에서 직접 호출하기 때문입니다.

또 다른 취약점, [GO-2022-1059](https://pkg.go.dev/vuln/GO-2022-1059)이 `golang.org/x/text` 모듈의 v0.3.5 버전에서 존재합니다. 그러나, 이는 "정보"로 보고되는 이유는, 우리의 코드가 해당 취약한 함수를 직접 또는 간접적으로 호출하지 않기 때문입니다.

이제 취약점을 평가하고 적절한 조치를 결정해 보겠습니다.

### 취약점 평가

a. 취약점 평가

먼저, 취약점의 설명을 읽고, 실제로 귀하의 코드와 사용 사례에 적용되는지 확인하십시오. 필요한 경우 "자세한 내용" 링크를 참조하십시오.

설명에 따르면, GO-2021-0113 취약점은 `Parse`를 사용하여 신뢰할 수 없는 사용자 입력을 처리할 때 패닉을 발생시킬 수 있습니다. 저희 프로그램이 신뢰할 수 없는 입력을 견딜 수 있도록 설계되었고, 서비스 거부 공격에 대한 우려가 있으므로, 이 취약점이 적용될 가능성이 높다고 가정합니다.

GO-2022-1059는 아마도 저희 코드에 영향을 미치지 않을 것입니다. 왜냐하면 저희 코드가 해당 보고서에 언급된 취약한 함수를 호출하지 않기 때문입니다.

b. 실행할 작업을 결정합니다.

GO-2021-0113을 완화하기 위한 몇 가지 옵션이 있습니다:
- **옵션 1: 고정 버전으로 업그레이드.** 패치가 제공되는 경우, 모듈의 고정 버전을 업그레이드하여 취약한 종속성을 제거할 수 있습니다.
- **옵션 2: 취약한 심볼(들) 사용 중단.** 코드를 수정하여 취약한 함수의 모든 호출을 제거할 수 있습니다.
  대체 방법을 찾아야 하거나 직접 구현해야 합니다.

이 경우, 해결책이 있으며, `Parse` 함수는 우리 프로그램에서 핵심적인 역할을 합니다. "해결된 버그"가 포함된 버전인 v0.3.7으로 의존성을 업그레이드합시다.

우리는 정보 취약점 GO-2022-1059를 수정하는 것을 우선순위에서 낮추기로 결정했습니다.
하지만 이 취약점은 GO-2021-0113과 같은 모듈에 있으며, 이 취약점에 대한 수정된 버전이 v0.3.8이므로, 이를 v0.3.8으로 업그레이드하여 두 개를 동시에 제거할 수 있습니다.

## 취약한 의존성 업그레이드

다행히 취약한 의존성을 업그레이드하는 것은 매우 간단합니다.

**8단계.** `golang.org/x/text`를 v0.3.8 버전으로 업그레이드합니다:

```
$ go get golang.org/x/text@v0.3.8
```

## 소개

이 문서는 Go 언어의 기본적인 구조와 특징을 설명합니다.

### Go 언어의 특징

*   **경량화된 프로세스:** Go는 Go루틴이라는 경량화된 프로세스 모델을 사용합니다.
*   **동시성:** Go는 채널을 사용하여 동시성을 쉽게 구현할 수 있습니다.
*   **정적 타입:** Go는 정적 타입 언어입니다.
*   **컴파일 언어:** Go는 컴파일 언어입니다.

### Go 언어의 예제 코드

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

### Go 언어의 테이블

| 항목 | 설명 |
|---|---|
| Go | Go 언어 |
| Go루틴 | 경량화된 프로세스 |
| 채널 | 동시성 구현을 위한 통신 채널 |

### Go 언어의 링크

*   [Go 공식 웹사이트](https://go.dev/)
*   [Go 튜토리얼](https://go.dev/tour/welcome/1)

### Go 언어의 목록

*   Go 언어
*   Go루틴
*   채널
*   정적 타입
*   컴파일 언어

```
go: 업그레이드됨: golang.org/x/text v0.3.5 => v0.3.8
```

(참고: 우리는 `latest` 또는 v0.3.8 이후의 다른 버전으로 업그레이드할 수도 있었습니다).

**9단계.** 이제 govulncheck를 다시 실행합니다:

```
$ govulncheck ./...
```

## 제목

안녕하세요!

이것은 예시 Markdown 콘텐츠입니다.

### 섹션 1

*   항목 1
*   항목 2
*   항목 3

#### 서브 섹션 1

*   서브 항목 1
*   서브 항목 2

**글꼴 강조**

`코드 예시`

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, world!")
}
```

| 헤더 1 | 헤더 2 |
|---|---|
| 셀 1 | 셀 2 |
| 셀 3 | 셀 4 |

[링크](https://www.example.com)

*   항목 목록 1
*   항목 목록 2
*   항목 목록 3

## 제목 2

**중요:**

*   항목 A
*   항목 B
*   항목 C

```python
def hello_world():
    print("Hello, world!")
```

`govulncheck`는 실험적인 도구입니다. 피드백을 https://go.dev/s/govulncheck-feedback 에서 공유해주세요.

`go1.20.3`와 `govulncheck@v0.0.0`를 사용하여
취약점 데이터를 https://vuln.go.dev (2023-04-06 19:19:26 +0000 UTC에 마지막으로 수정됨)에서 가져왔습니다.

코드와 46개의 패키스 (1개의 종속 모듈)에 대해 알려진 취약점을 스캔 중입니다...
취약점은 발견되지 않았습니다.

마지막으로, govulncheck는 취약점이 발견되지 않았음을 확인합니다.

정기적으로 `govulncheck` 명령어를 사용하여 의존성을 검사하면, 취약점을 식별, 우선순위 지정, 해결하여 코드베이스를 보호할 수 있습니다.
