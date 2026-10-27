이 페이지는 Go 개발자가 프로젝트의 보안을 향상시키는 데 필요한 리소스를 제공합니다.

(참고: [Go 개발자를 위한 보안 모범 사례](/security/best-practices).)

## 알려진 취약점 찾고 해결하기

Go의 취약점 탐지는 개발자가 자신의 프로젝트에 영향을 미칠 수 있는 알려진 취약점에 대해 배우는 데 도움이 되는, 소음이 적고 신뢰할 수 있는 도구를 제공하는 것을 목표로 합니다.
개요를 보려면, Go의 취약점 관리 아키텍처에 대한 [이 요약 및 FAQ 페이지](/security/vuln)를 참조하십시오. 실제 적용 방안을 살펴보기 위해, 아래 도구를 참조하십시오.

### govulncheck을 사용하여 코드의 취약점 검사

개발자는 `govulncheck` 도구를 사용하여 코드에 영향을 미치는 알려진 취약점이 있는지 확인하고, 실제로 호출되는 취약한 함수 및 메서드를 기반으로 다음 단계를 우선순위로 정할 수 있습니다.

- [govulncheck 문서를 보려면](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)
- [튜토리얼: govulncheck 시작하기](/doc/tutorial/govulncheck)

### 편집기에서 취약점 감지

VS Code Go 확장 프로그램은 제3자 종속성을 검사하고 관련 취약점을 표시합니다.

- [사용자 문서](/security/vuln/editor)
- [VS Code Go 다운로드](https://marketplace.visualstudio.com/items?itemName=golang.go)
- [튜토리얼: VS Code Go 시작하기](/doc/tutorial/govulncheck-ide)

### Go 모듈을 기반으로 빌드할 수 있는 모듈 찾기

[Pkg.go.dev](https://pkg.go.dev/)는 Go 패키지와 모듈을 검색, 평가하고 더 자세히 알아볼 수 있는 웹사이트입니다. pkg.go.dev에서 패키지를 검색하고 평가할 때, 해당 버전에 취약점이 있는 경우 [페이지 상단에 배너가 표시](https://pkg.go.dev/golang.org/x/text@v0.3.7/language)됩니다. 또한, 패키지의 각 버전에 영향을 미치는 취약점은 버전 기록 페이지에서 [볼 수 있습니다](https://pkg.go.dev/golang.org/x/text@v0.3.7/language?tab=versions).

### 취약점 데이터베이스 검색

Go 취약점 데이터베이스는 Go 패키지
유지 관리자뿐만 아니라 [MITRE](https://www.cve.org/) 및 [GitHub](https://github.com/)과 같은 외부 소스에서 직접 데이터를 수집합니다. 보고서는 Go Security 팀에서 관리합니다.

- [Go 취약점 데이터베이스 보고서 검색](https://pkg.go.dev/vuln/)
- [Go 취약점 데이터베이스 문서 보기](/security/vuln/database)
- [데이터베이스에 공개 취약점을 기여](/s/vulndb-report-new)

## Go 프로젝트의 보안 버그 보고하기

**보고하는 방법:**

*   **버그 트래커:** [버그 트래커 링크 삽입] (예: GitHub Issues, Bugzilla 등)
*   **문제 설명:**
    *   버그의 명확하고 간결한 설명
    *   재현 단계 (Reproducible steps)
    *   예상되는 영향 (Impact)
    *   가능한 해결 방안 (Suggested solutions) (선택 사항)
*   **첨부 파일:**
    *   로그 파일
    *   스크린샷
    *   코드 스니펫 (만약 관련 코드가 있다면)
    *   빌드 결과 (Makefile, build.sh 등)

**팁:**

*   가능하면 가장 자세하고 정확하게 정보를 제공하세요.
*   다른 사람이 문제를 쉽게 재현할 수 있도록 명확한 설명이 중요합니다.
*   여러 사람이 동시에 동일한 버그를 보고하는 것을 방지하기 위해, 버그 트래커를 사용하세요.
*   `go.mod` 파일과 같은 프로젝트 관련 정보를 함께 제공하면 문제 해결에 도움이 됩니다.

### [보안 정책](/security/policy)

보고 절차에 대한 자세한 내용은 보안 정책을 참조하십시오.
[Go 프로젝트의 취약점 보고 방법](/security/policy#reporting-a-security-bug).
이 페이지에서는 Go 보안 팀의 문제 추적 및 공개 프로세스에 대한 자세한 내용을 담고 있습니다. 과거 보안 패치에 대한 자세한 내용은 [릴리스 기록](/doc/devel/release)를 참조하십시오. [릴리스 정책](/doc/devel/release#policy)에 따라, 우리는 Go의 두 가장 최근 주요 릴리스에 보안 패치를 제공합니다.

- [흔히 보고되는 취약점에 대한 분류 결정](/doc/security/decisions)

## 예상치 못한 입력으로 테스트하기 (퍼징)

Go 네이티브 퍼징은 프로그램을 대상으로 지속적으로 입력을 조작하여 버그를 찾는 자동화된 테스트 유형을 제공합니다. Go 1.18부터 Go는 표준 도구 체인에서 퍼징을 지원합니다. 네이티브 Go 퍼징 테스트는 [OSS-Fuzz](https://google.github.io/oss-fuzz/getting-started/new-project-guide/go-lang/#native-go-fuzzing-support)에서 지원됩니다.

- [퍼징의 기본 사항 검토](/security/fuzz)
- [튜토리얼: 퍼징 시작하기](/doc/tutorial/fuzz)

## Go의 암호화 라이브러리를 사용하여 안전한 서비스를 구축하기

```go
package main

import (
	"crypto/rand"
	"fmt"
	"math/big"
)

func main() {
	// 난수 생성
	num, err := rand.Int(rand.Reader, big.NewInt(1000))
	if err != nil {
		fmt.Println("Error generating random number:", err)
		return
	}
	fmt.Println("Random number:", num.String())

	// 암호화 (예시: AES)
	// 실제 사용 시에는 적절한 암호화 알고리즘 및 키 관리를 사용해야 합니다.
	// 이 예시는 단순한 개념 설명일 뿐입니다.
}
```

## 주요 내용

*   Go의 강력한 암호화 라이브러리 사용
*   보안 서비스 구축을 위한 핵심 기능 소개
*   예시 코드 제공 (Go)
*   더 자세한 내용은 관련 Go 패키지를 참조하세요.

Go의 암호화 라이브러리는 개발자가 안전한 애플리케이션을 구축하는 데 도움을 주기 위해 설계되었습니다.
[crypto 패키지](https://pkg.go.dev/golang.org/x/crypto)에 대한 문서를 참조하십시오.
그리고 [golang.org/x/crypto/](https://pkg.go.dev/golang.org/x/crypto/).

## FIPS 140-3 인증 암호화

Go의 암호화 라이브러리는 규제된 환경에서 사용하기 위해 FIPS 140-3 규격에 따른 모드로 사용할 수 있습니다. 자세한 내용은 [FIPS 140-3 규격 준수](/doc/security/fips140) 문서를 참조하십시오.
