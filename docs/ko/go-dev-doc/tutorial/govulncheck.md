<!--{
  "Title": "튜토리얼: govulncheck로 취약한 종속성 찾기 및 수정하기",
  "HideTOC": true,
  "Breadcrumb": true
}-->

# 튜토리얼: govulncheck로 취약한 종속성 찾기 및 수정하기

이 튜토리얼에서는 `govulncheck` 도구를 사용하여 Go 프로그램의 취약한 종속성을 식별하고 수정하는 방법을 알아봅니다.

## govulncheck란 무엇인가요?

`govulncheck`는 Go의 공식 취약점 분석 도구입니다. 이 도구는 Go 취약점 데이터베이스를 사용하여 프로그램이 사용하는 종속성 중 알려진 취약점이 있는 항목이 있는지 확인합니다.

`govulncheck`는 단순히 종속성 목록을 확인하는 것이 아니라, 실제 프로그램의 코드가 취약한 함수를 호출하는지 분석하는 **정적 분석**을 수행합니다. 따라서 실제로 실행 경로에 포함되지 않은 취약점은 무시하여 오탐(false positive)을 줄여줍니다.

## 시작하기

### govulncheck 설치

먼저 `govulncheck`를 설치해야 합니다. 다음 명령어를 실행하세요.

```bash
go install golang.org/x/vuln/cmd/govulncheck@latest
```

### 분석할 프로젝트 준비

테스트를 위해 의도적으로 취약한 버전의 패키지를 사용하는 샘플 프로젝트를 생성하거나 기존 프로젝트로 이동합니다.

```bash
mkdir vuln-demo
cd vuln-demo
go mod init vuln-demo
```

예를 들어, 취약점이 알려진 오래된 버전의 패키지를 추가해 보겠습니다.

```bash
go get golang.org/x/crypto@v0.0.0-20220315165801-2b6d9f71d76c
```

그 다음, 간단한 `main.go` 파일을 작성하여 해당 패키지를 사용합니다.

```go
package main

import (
	"fmt"
	"golang.org/x/crypto/ssh"
)

func main() {
	fmt.Println("SSH vulnerability check")
	_ = ssh.NewPublicKey() // 취약한 함수 호출 예시
}
```

## 취약점 스캔하기

이제 `govulncheck`를 실행하여 프로젝트를 분석합니다.

```bash
govulncheck ./...
```

### 결과 해석하기

`govulncheck`가 취약점을 발견하면 다음과 같은 정보를 출력합니다.

1.  **취약점 ID**: (예: GO-2022-XXXX)
2.  **설명**: 취약점의 내용과 영향.
3.  **수정 버전**: 취약점이 해결된 최소 버전.
4.  **호출 스택(Call Stack)**: 내 코드의 어느 부분에서 취약한 함수가 호출되었는지 보여주는 경로.

만약 취약점이 발견되지 않았다면 `No vulnerabilities found`라는 메시지가 표시됩니다.

## 취약점 수정하기

취약점을 수정하는 가장 일반적인 방법은 해당 패키지를 최신 버전으로 업데이트하는 것입니다.

### 패키지 업데이트

`go get` 명령어를 사용하여 패키지를 최신 버전으로 업데이트합니다.

```bash
go get -u golang.org/x/crypto
```

또는 특정 수정 버전 이상으로 업데이트합니다.

```bash
go get golang.org/x/crypto@v0.17.0
```

그 후, 다시 `go mod tidy`를 실행하여 종속성을 정리합니다.

```bash
go mod tidy
```

## 결과 확인

수정 사항을 적용한 후 다시 `govulncheck`를 실행하여 취약점이 해결되었는지 확인합니다.

```bash
govulncheck ./...
```

이제 `No vulnerabilities found` 메시지가 출력되어야 합니다.

## 요약

1.  `go install golang.org/x/vuln/cmd/govulncheck@latest`로 도구를 설치합니다.
2.  `govulncheck ./...`를 실행하여 취약점을 분석합니다.
3.  출력된 호출 스택을 통해 내 코드가 실제로 취약점에 노출되었는지 확인합니다.
4.  `go get -u`를 통해 취약한 패키지를 업데이트하여 문제를 해결합니다.

Govulncheck는 Go 프로젝트에서 취약한 의존성을 찾아 수정하는 것을 돕는 저소음(low-noise) 도구입니다. 이 도구는 프로젝트의 의존성에서 알려진 취약점을 스캔한 다음, 코드 내에서 해당 취약점으로 이어지는 직접 또는 간접 호출이 있는지 식별함으로써 이를 수행합니다.

이 튜토리얼에서는 `govulncheck`를 사용하여 간단한 프로그램의 취약점을 스캔하는 방법을 배웁니다. 또한, 취약점의 우선순위를 정하고 평가하는 방법을 배워 가장 중요한 문제부터 해결하는 데 집중하는 방법을 익히게 됩니다.

govulncheck에 대해 더 자세히 알아보려면 [govulncheck 문서](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)와 Go의 취약점 관리에 관한 이 [블로그 포스트](/blog/vuln)를 참조하세요.
또한 여러분의 [피드백을 기다리고 있습니다](/s/govulncheck-feedback).

## 사전 요구 사항

- **Go.** 이 튜토리얼을 따라 하기 위해 최신 버전의 Go를 사용하는 것을 권장합니다.
  설치 방법은 [Installing Go](/doc/install)를 참조하세요.
- **코드 에디터.** 사용 중인 어떤 에디터든 상관없습니다.
- **명령어 터미널.** Go는 Linux 및 Mac의 모든 터미널과 Windows의 PowerShell 또는 cmd에서 잘 작동합니다.

이 튜토리얼에서는 다음 단계들을 진행합니다:

1. 취약한 종속성이 있는 샘플 Go 모듈 생성
2. govulncheck 설치 및 실행
3. 취약점 평가
4. 취약한 종속성 업그레이드

## 취약한 종속성이 포함된 샘플 Go 모듈 생성하기

**Step 1.** 시작하려면 `vuln-tutorial`이라는 새 폴더를 생성하고 Go 모듈을 초기화하세요.
(Go 모듈이 처음이시라면, [go.dev/doc/tutorial/create-module](/doc/tutorial/create-module)을 확인해 보세요.)

예를 들어, 홈 디렉토리에서 다음을 실행하세요:

```
$ mkdir vuln-tutorial
$ cd vuln-tutorial
$ go mod init vuln.tutorial
```

**단계 2.** `vuln-tutorial` 폴더 안에 `main.go`라는 파일을 생성하고, 다음 코드를 복사하여 붙여넣으세요:

```go
package main

import (
        "fmt"
        "os"

        "golang.org/x/text/language"
)

func main() {
        for _, arg := range os.Args[1:] {
                tag, err := language.Parse(arg)
                if err != nil {
                        fmt.Printf("%s: error: %v\n", arg, err)
                } else if tag == language.Und {
                        fmt.Printf("%s: undefined\n", arg)
                } else {
                        fmt.Printf("%s: tag %s\n", arg, tag)
                }
        }
}
```

이 샘플 프로그램은 언어 태그 목록을 명령줄 인수로 받아, 각 태그가 성공적으로 파싱되었는지, 정의되지 않았는지, 또는 파싱 중 오류가 발생했는지를 나타내는 메시지를 출력합니다.

**3단계.** `go mod tidy`를 실행합니다. 이 명령은 이전 단계에서 `main.go`에 추가한 코드에 필요한 모든 의존성으로 `go.mod` 파일을 채웁니다.

`vuln-tutorial` 폴더에서 다음을 실행하세요:

```
$ go mod tidy
```

다음 출력이 표시되어야 합니다:

```
go: finding module for package golang.org/x/text/language
go: downloading golang.org/x/text v0.9.0
go: found golang.org/x/text/language in golang.org/x/text v0.9.0
```

**4단계.** `go.mod` 파일을 열어 다음과 같이 되어 있는지 확인하세요:

```
module vuln.tutorial

go 1.20

require golang.org/x/text v0.9.0
```

**5단계.** 알려진 취약점이 포함된 `golang.org/x/text` v0.3.5 버전으로 다운그레이드합니다. 다음을 실행하세요:

```
$ go get golang.org/x/text@v0.3.5
```

다음과 같은 출력이 표시되어야 합니다:

```
go: downgraded golang.org/x/text v0.9.0 => v0.3.5
```

`go.mod` 파일의 내용은 이제 다음과 같아야 합니다:

```
module vuln.tutorial

go 1.20

require golang.org/x/text v0.3.5
```

이제 `govulncheck`가 실제로 어떻게 작동하는지 살펴보겠습니다.

## govulncheck 설치 및 실행

**6단계.** `go install` 명령어로 govulncheck를 설치합니다:

```
$ go install golang.org/x/vuln/cmd/govulncheck@latest
```

**단계 7.** 분석하려는 폴더(`vuln-tutorial`)에서 다음을 실행하십시오:

```
$ govulncheck ./...
```

다음과 같은 출력이 표시되어야 합니다:

```
govulncheck는 실험적인 도구입니다. 피드백은 https://go.dev/s/govulncheck-feedback 로 보내주세요.

go1.20.3 및 govulncheck@v0.0.0을 사용 중이며,
https://vuln.go.dev (최종 수정일 2023-04-18 21:32:26 +0000 UTC)의 취약점 데이터를 사용합니다.

코드와 1개의 의존성 모듈에 걸친 46개 패키지에서 알려진 취약점을 스캔하는 중...
작성하신 코드가 1개 모듈의 1개 취약점에 영향을 받습니다.

취약점 #1: GO-2021-0113
  부적절한 인덱스 계산으로 인해, 잘못된 형식의
  언어 태그가 범위 외 읽기(out of bounds read)를 통해 Parse의 패닉을 유발할 수 있습니다.
  신뢰할 수 없는 사용자 입력을 처리하는 데 Parse를 사용하는 경우, 이는
  서비스 거부(DoS) 공격의 벡터로 이용될 수 있습니다.

  더 자세한 정보: https://pkg.go.dev/vuln/GO-2021-0113

  모듈: golang.org/x/text
    발견된 버전: golang.org/x/text@v0.3.5
    수정된 버전: golang.org/x/text@v0.3.7

    코드 내 호출 스택:
      main.go:12:29: vuln.tutorial.main 이(가) golang.org/x/text/language.Parse 를 호출합니다.

=== 정보 (Informational) ===

가져온 패키지에서 1개의 취약점이 발견되었으나, 해당 취약점 사용으로 이어지는
호출 스택이 없습니다. 아무런 조치를 취하지 않아도 될 수 있습니다. 자세한 내용은 https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck 를 참조하십시오.

취약점 #1: GO-2022-1059
  공격자가 ParseAcceptLanguage가 파싱하는 데 상당한 시간이 걸리는
  Accept-Language 헤더를 정교하게 제작하여 서비스 거부(DoS)를 유발할 수 있습니다.
  더 자세한 정보: https://pkg.go.dev/vuln/GO-2022-1059
  발견된 버전: golang.org/x/text@v0.3.5
  수정된 버전: golang.org/x/text@v0.3.8
```

### 출력 결과 해석하기

<font size="2">  *참고: 최신 버전의 Go를 사용하지 않는 경우, 표준 라이브러리에서 추가적인 취약점이 발견될 수 있습니다. </font>

저희 코드는 `golang.org/x/text/language` 패키지의 취약한 버전(v0.3.5)에 있는 `Parse` 함수를 직접 호출하고 있기 때문에, [GO-2021-0113](https://pkg.go.dev/vuln/GO-2021-0113) 취약점의 영향을 받습니다.

또 다른 취약점인 [GO-2022-1059](https://pkg.go.dev/vuln/GO-2022-1059)가 `golang.org/x/text` 모듈의 v0.3.5 버전에서 발견되었습니다. 하지만 저희 코드가 해당 취약점이 있는 함수를 (직접적으로든 간접적으로든) 전혀 호출하지 않기 때문에 "Informational"로 보고되었습니다.

이제 취약점을 평가하고 취해야 할 조치를 결정해 보겠습니다.

### 취약점 평가

a. 취약점을 평가합니다.

먼저, 취약점 설명을 읽고 해당 내용이 실제로 사용자의 코드와 유즈케이스에 적용되는지 판단하십시오. 추가 정보가 필요한 경우 "More info" 링크를 방문하십시오.

설명에 따르면, `Parse`가 신뢰할 수 없는 사용자 입력을 처리하는 데 사용될 때 취약점 GO-2021-0113으로 인해 패닉(panic)이 발생할 수 있습니다. 우리 프로그램이 신뢰할 수 없는 입력에도 견뎌내야 하며, 서비스 거부(denial of service) 공격이 우려된다고 가정한다면, 이 취약점은 적용될 가능성이 높습니다.

GO-2022-1059는 해당 보고서에 언급된 취약한 함수들을 우리 코드에서 호출하지 않기 때문에, 우리 코드에 영향을 미칠 가능성이 낮습니다.

b. 행동을 결정합니다.

GO-2021-0113를 완화하기 위해 다음과 같은 몇 가지 옵션이 있습니다:
- **옵션 1: 수정된 버전으로 업그레이드.** 수정 버전이 제공되는 경우, 모듈을 수정된 버전으로 업그레이드하여 취약한 종속성을 제거할 수 있습니다.
- **옵션 2: 취약한 심볼 사용 중단.** 코드 내에서 취약한 함수에 대한 모든 호출을 제거하는 방법을 선택할 수 있습니다. 이 경우 대체 방법을 찾거나 직접 구현해야 합니다.

이 경우 수정 방법이 존재하며, `Parse` 함수는 우리 프로그램에 필수적입니다. 의존성을 수정 버전인 v0.3.7로 업그레이드해 보겠습니다.

우리는 정보성 취약점인 GO-2022-1059의 수정 우선순위를 낮추기로 결정했습니다. 하지만 이 취약점은 GO-2021-0113과 동일한 모듈에 있으며, 수정 버전이 v0.3.8이므로, v0.3.8로 업그레이드함으로써 두 취약점을 동시에 쉽게 제거할 수 있습니다.

## 취약한 종속성 업그레이드

다행히도, 취약한 종속성을 업그레이드하는 방법은 매우 간단합니다.

**8단계.** `golang.org/x/text`를 v0.3.8로 업그레이드합니다:

```
$ go get golang.org/x/text@v0.3.8
```

다음과 같은 출력이 나타나야 합니다:

```
go: upgraded golang.org/x/text v0.3.5 => v0.3.8
```

(참고로 `latest` 또는 v0.3.8 이후의 다른 버전으로 업그레이드하는 것을 선택할 수도 있었습니다).

**9단계.** 이제 `govulncheck`를 다시 실행하세요:

```
$ govulncheck ./...
```

이제 다음과 같은 출력을 보게 됩니다:

```
govulncheck는 실험적인 도구입니다. 피드백은 https://go.dev/s/govulncheck-feedback 에서 공유해 주세요.

https://vuln.go.dev (최종 수정일 2023-04-06 19:19:26 +0000 UTC)의 취약점 데이터를 사용하여 go1.20.3 및 govulncheck@v0.0.0을 사용 중입니다.

1개의 의존 모듈에 걸쳐 코드와 46개의 패키지에서 알려진 취약점을 스캔하는 중...
취약점이 발견되지 않았습니다.
```

마지막으로, `govulncheck`를 통해 발견된 취약점이 없음을 확인합니다.

`govulncheck` 명령어로 종속성을 정기적으로 스캔함으로써, 취약점을 식별하고 우선순위를 정하며 해결하여 코드베이스를 안전하게 보호할 수 있습니다.
