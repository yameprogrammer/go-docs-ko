[Go 보안으로 돌아가기](/security)

## 개요

Go는 개발자가 공격자에 의해 악용될 위험이 있는 오류나 취약점을 탐지, 평가 및 해결할 수 있도록 돕습니다. 백그라운드에서 Go 팀은 취약점 보고서를 큐레이션하는 파이프라인을 운영하며, 이 보고서들은 Go vulnerability database에 저장됩니다. 다양한 라이브러리와 도구가 이러한 보고서를 읽고 분석하여 특정 사용자 프로젝트가 어떤 영향을 받을 수 있는지 파악할 수 있습니다. 이 기능은 [Go package discovery site](https://pkg.go.dev)와 새로운 CLI 도구인 `govulncheck`에 통합되어 있습니다.

이 프로젝트는 현재 작업 중이며 활발하게 개발되고 있습니다.
더 나은 개선을 위해 여러분의 [피드백](#feedback)을 환영합니다!

**참고**: Go 프로젝트의 취약점을 보고하시려면 [Go Security Policy](/security/policy)를 참조하시기 바랍니다.

## 아키텍처

<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="architecture.png" alt="Go Vulnerability Management Architecture"></img>
  </center>
</div>

Go의 취약점 관리는 다음과 같은 상위 수준의 요소들로 구성됩니다:

1. **데이터 파이프라인**은 [National Vulnerability Database (NVD)](https://nvd.nist.gov/), [GitHub Advisory Database](https://github.com/advisories), 그리고 [Go 패키지 유지 관리자로부터 직접](/s/vulndb-report-new) 전달되는 내용을 포함하여 다양한 소스로부터 취약점 정보를 수집합니다.
2. **취약점 데이터베이스**는 데이터 파이프라인의 정보를 사용하여 보고서로 채워집니다. 데이터베이스의 모든 보고서는 Go 보안 팀에 의해 검토 및 큐레이션됩니다. 보고서는 [Open Source Vulnerability (OSV) 형식](https://ossf.github.io/osv-schema/)으로 작성되며 [API](/security/vuln/database#api)를 통해 접근할 수 있습니다.
3. [pkg.go.dev](https://pkg.go.dev) 및 govulncheck와의 **통합**을 통해 개발자가 자신의 프로젝트에서 취약점을 찾을 수 있도록 합니다. [govulncheck 명령어](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)는 코드베이스를 분석하여, 코드 내의 어떤 함수가 취약한 함수를 전이적으로 호출하고 있는지에 따라 실제로 영향을 주는 취약점만을 표시합니다. Govulncheck는 프로젝트에서 알려진 취약점을 찾을 수 있는 노이즈가 적고 신뢰할 수 있는 방법을 제공합니다.

## 리소스

### Go 취약점 데이터베이스 (Go Vulnerability Database)

[Go 취약점 데이터베이스](https://vuln.go.dev)는 Go 패키지 메인테이너가 Go 보안 팀에 직접 보고한 내용 외에도 많은 기존 소스의 정보를 포함하고 있습니다.
데이터베이스의 각 항목은 취약점 설명, 패키지 및 심볼 정보, 버전 세부 사항이 정확한지 확인하기 위해 검토됩니다.

Go 취약점 데이터베이스에 대한 자세한 내용은 [go.dev/security/vuln/database](/security/vuln/database)를 참조하시고, 브라우저에서 데이터베이스의 취약점을 확인하시려면 [pkg.go.dev/vuln](https://pkg.go.dev/vuln)을 방문하십시오.

패키지 유지 관리자분들께서 자신의 프로젝트에 있는 공개 취약점 정보를 [제공](#feedback)하고, 마찰을 줄일 수 있는 방법에 대한 [제안 사항을 보내주시길](/s/vuln-feedback) 권장합니다.

### Go를 위한 취약점 탐지

Go의 취약점 탐지는 Go 사용자가 자신의 프로젝트에 영향을 미칠 수 있는 알려진 취약점에 대해 알 수 있도록 노이즈가 적고 신뢰할 수 있는 방법을 제공하는 것을 목표로 합니다.
취약점 점검은 새로운 커맨드 라인 툴인 [govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck), [Go 패키지 검색 사이트](https://pkg.go.dev), Go 확장 프로그램을 사용하는 VS Code와 같은 [주요 에디터](/security/vuln/editor)를 포함하여 Go의 도구 및 서비스에 통합되어 있습니다.

govulncheck를 사용하시려면 프로젝트에서 다음 명령어를 실행하십시오:

```
$ go install golang.org/x/vuln/cmd/govulncheck@latest
$ govulncheck ./...
```

에디터에서 취약점 탐지를 활성화하려면 [editor integration](/security/vuln/editor) 페이지의 안내를 참조하세요.

### Go CNA

Go 보안 팀은 [CVE Numbering Authority](https://www.cve.org/ProgramOrganization/CNAs)입니다.
자세한 내용은 [go.dev/security/vuln/cna](/security/vuln/cna)를 참조하십시오.

## 피드백

다음과 같은 방법으로 기여하여 저희가 개선해 나갈 수 있도록 도와주시면 감사하겠습니다:

- 유지 관리 중인 Go 패키지의 공개 취약점에 대해 새로운 정보를 [제공](/s/vulndb-report-new)하거나 기존 정보를 [업데이트](/s/vulndb-report-feedback)하세요.
- [이 설문조사](/s/govulncheck-feedback)에 참여하여 govulncheck 사용 경험을 공유해 주세요.
- 문제점 및 기능 요청에 대한 [피드백을 보내주세요](/s/vuln-feedback).

## FAQ

**Go 프로젝트의 보안 취약점을 어떻게 보고하나요?**

Go 프로젝트의 모든 보안 버그는 [security@golang.org](mailto:security@golang.org)로 이메일을 보내 보고해 주세요.
프로세스에 대한 자세한 내용은 [Go의 보안 정책](/security/policy)을 읽어보시기 바랍니다.

**Go 취약점 데이터베이스에 공개 취약점을 추가하려면 어떻게 해야 하나요?**

Go 취약점 데이터베이스에 공개 취약점 추가를 요청하려면,
[이 양식을 작성해 주세요](/s/vulndb-report-new).

취약점이 이미 공개적으로 알려졌거나, 귀하가 유지 관리하는 패키지에 존재하여 (귀하가 공개할 준비가 된) 경우, 해당 취약점은 공개된 것으로 간주됩니다. 이 양식은 Go 팀이 유지 관리하지 않는(Go 표준 라이브러리, Go 툴체인 및 golang.org 모듈 이외의 모든 것) 가져오기 가능한 Go 패키지의 공개 취약점만을 대상으로 합니다.

이 양식은 새로운 CVE ID를 요청하는 데에도 사용할 수 있습니다.
Go CVE Numbering Authority에 대한 [더 자세한 내용은 여기](/security/vuln/cna)에서 확인하십시오.

**취약점 수정을 제안하려면 어떻게 해야 하나요?**

Go 취약점 데이터베이스(vulnerability database)의 기존 보고서에 대한 수정을 제안하시려면,
[여기에서 양식을 작성해 주세요](/s/vulndb-report-feedback).

**govulncheck에 대한 이슈를 보고하거나 피드백을 주는 방법은 무엇인가요?**

이슈나 피드백은 [Go 이슈 트래커](/s/vuln-feedback)를 통해 제출해 주세요.

**다른 데이터베이스에서 이 취약점을 발견했습니다. 왜 Go 취약점 데이터베이스에는 없나요?**

보고서는 여러 가지 이유로 Go 취약점 데이터베이스에서 제외될 수 있습니다. 여기에는 관련 취약점이 Go 패키지에 존재하지 않거나, 취약점이 임포트 가능한 패키지가 아닌 설치 가능한 커맨드에 있는 경우, 또는 이미 데이터베이스에 존재하는 다른 취약점에 의해 해당 취약점이 포괄되는 경우 등이 포함됩니다.

Go 보안 팀의 [보고서 제외 사유에 대해 여기에서](/security/vuln/database#excluded-reports) 더 자세히 알아볼 수 있습니다.

만약 보고서가 vuln.go.dev에서 잘못 제외되었다고 생각하신다면, [저희에게 알려주시기 바랍니다](/s/vulndb-report-feedback).

**Go 취약점 데이터베이스(vulnerability database)에서 심각도 레이블(severity labels)을 사용하지 않는 이유는 무엇인가요?**

대부분의 취약점 보고 형식은 "LOW", "MEDIUM", "CRITICAL"과 같은 심각도 레이블을 사용하여 서로 다른 취약점의 영향을 나타내고, 개발자가 보안 문제의 우선순위를 정하는 데 도움을 줍니다.
하지만 Go는 몇 가지 이유로 이러한 레이블의 사용을 지양합니다.

취약점의 영향이 보편적인 경우는 드뭅니다. 이는 심각도 지표가 종종 기만적일 수 있음을 의미합니다. 예를 들어, 파서(parser)의 충돌은 사용자 제공 입력을 파싱하는 데 사용되어 DoS 공격에 이용될 수 있다면 심각한 수준의 이슈가 될 수 있지만, 파서가 로컬 설정 파일을 파싱하는 데 사용된다면 심각도를 "낮음(low)"이라고 부르는 것조차 과장일 수 있습니다.

심각도를 지정하는 것은 필연적으로 주관적일 수밖에 없습니다.
이는 공격 벡터, 복잡성, 악용 가능성과 같은 취약점의 관련 측면을 세분화하는 공식을 제시하는 [CVE 프로그램](https://www.cve.org/About/Overview)의 경우에도 마찬가지입니다.
하지만 이 모든 요소는 주관적인 평가를 필요로 합니다.

우리는 취약점에 대한 상세한 설명이 심각도 지표보다 더 유용하다고 믿습니다.
좋은 설명은 문제가 무엇인지,
어떻게 트리거될 수 있는지, 그리고 소비자가 자신의 소프트웨어에 미치는 영향을 판단할 때
무엇을 고려해야 하는지를 상세히 분석해 줄 수 있습니다.

이 주제에 대해 의견을 공유하고 싶으시다면 언제든지 [이슈를 제기](/s/vuln-feedback)해 주세요.
