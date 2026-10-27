이 페이지는 Go 개발자가 프로젝트의 보안을 강화하는 데 도움이 되는 리소스를 제공합니다.

(참고: [Go 개발자를 위한 보안 모범 사례](/security/best-practices).)

## 알려진 취약점 찾기 및 수정하기

Go의 취약점 탐지는 개발자가 자신의 프로젝트에 영향을 줄 수 있는 알려진 취약점에 대해 학습할 수 있도록, 노이즈가 적고 신뢰할 수 있는 도구를 제공하는 것을 목표로 합니다. 개요를 확인하시려면 Go의 취약점 관리 아키텍처에 관한 [요약 및 FAQ 페이지](/security/vuln)부터 시작하세요. 실제 적용 방법은 아래의 도구들을 살펴보시기 바랍니다.

### govulncheck를 사용하여 코드의 취약점 스캔하기

개발자는 `govulncheck` 도구를 사용하여 알려진 취약점이 코드에 영향을 미치는지 확인하고, 실제로 호출되는 취약한 함수와 메서드를 기반으로 다음 단계의 우선순위를 정할 수 있습니다.

- [govulncheck 문서 보기](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)
- [튜토리얼: govulncheck 시작하기](/doc/tutorial/govulncheck)

### 에디터에서 취약점 탐지하기

VS Code Go 확장은 서드파티 의존성을 확인하고 관련 취약점을 표시합니다.

- [사용자 문서](/security/vuln/editor)
- [VS Code Go 다운로드](https://marketplace.visualstudio.com/items?itemName=golang.go)
- [튜토리얼: VS Code Go 시작하기](/doc/tutorial/govulncheck-ide)

### 기반으로 구축할 Go 모듈 찾기

[Pkg.go.dev](https://pkg.go.dev/)는 Go 패키지와 모듈을 발견하고, 평가하며, 더 자세히 배울 수 있는 웹사이트입니다. pkg.go.dev에서 패키지를 발견하고 평가할 때, 해당 버전에 취약점이 있다면 [페이지 상단에 배너가 표시됩니다](https://pkg.go.dev/golang.org/x/text@v0.3.7/language). 또한, 버전 기록 페이지에서 [패키지의 각 버전에 영향을 미치는 취약점](https://pkg.go.dev/golang.org/x/text@v0.3.7/language?tab=versions)을 확인할 수 있습니다.

### 취약점 데이터베이스 찾아보기

Go 취약점 데이터베이스는 Go 패키지 유지관리자와 [MITRE](https://www.cve.org/), [GitHub](https://github.com/)와 같은 외부 소스로부터 직접 데이터를 수집합니다. 보고서는 Go 보안 팀(Go Security team)에 의해 관리됩니다.

- [Go 취약점 데이터베이스에서 리포트 찾아보기](https://pkg.go.dev/vuln/)
- [Go 취약점 데이터베이스 문서 보기](/security/vuln/database)
- [데이터베이스에 공개 취약점 기여하기](/s/vulndb-report-new)

## Go 프로젝트의 보안 버그 보고하기

### [보안 정책](/security/policy)

[Go 프로젝트의 취약점 보고 방법](/security/policy#reporting-a-security-bug)에 대한 지침은 보안 정책(Security Policy)을 참조하십시오. 해당 페이지에는 Go 보안 팀의 이슈 추적 및 공개 프로세스에 대한 상세 내용이 포함되어 있습니다. 과거의 보안 수정 사항에 대한 자세한 내용은 [릴리스 기록](/doc/devel/release)을 확인하십시오. [릴리스 정책](/doc/devel/release#policy)에 따라, 당사는 Go의 최신 두 가지 메이저 릴리스에 대해 보안 수정을 제공합니다.

- [자주 보고되는 취약점에 대한 분류 결정](/doc/security/decisions)

## 퍼징(fuzzing)으로 예상치 못한 입력 테스트하기

Go 네이티브 퍼징(native fuzzing)은 프로그램의 입력을 지속적으로 조작하여 버그를 찾는 일종의 자동화된 테스트를 제공합니다. Go는 Go 1.18부터 표준 툴체인에서 퍼징을 지원합니다. 네이티브 Go 퍼즈 테스트는 [OSS-Fuzz에서 지원됩니다](https://google.github.io/oss-fuzz/getting-started/new-project-guide/go-lang/#native-go-fuzzing-support).

- [퍼징(fuzzing)의 기초 검토](/security/fuzz)
- [튜토리얼: 퍼징 시작하기](/doc/tutorial/fuzz)

## Go의 암호화 라이브러리로 서비스 보안 강화하기

Go의 cryptography 라이브러리는 개발자가 보안 애플리케이션을 구축하는 것을 돕는 것을 목표로 합니다.
[crypto 패키지](https://pkg.go.dev/golang.org/x/crypto) 및 [golang.org/x/crypto/](https://pkg.go.dev/golang.org/x/crypto)에 대한 문서를 확인하세요.

## FIPS 140-3 준수 암호화

Go의 cryptography 라이브러리는 규제 환경에서 사용할 수 있도록 FIPS 140-3 준수 모드로 사용할 수 있습니다. 자세한 내용은 [FIPS 140-3 Compliance](/doc/security/fips140) 문서를 참조하십시오.
