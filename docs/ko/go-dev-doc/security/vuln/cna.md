[Go 취약점 관리로 돌아가기](/security/vuln)

## 개요

Go CNA는
[CVE 번호 지정 기관](https://www.cve.org/ProgramOrganization/CNAs)이며,
[CVE ID](https://www.cve.org/ResourcesSupport/Glossary?activeTerm=glossaryCVEID)를 발행하고
[CVE 레코드](https://www.cve.org/ResourcesSupport/Glossary?activeTerm=glossaryRecord)를 게시하여 Go 생태계의 공개 취약점에 대한 정보를 제공합니다. 이는 Google CNA의 하위 기관입니다.

## 범위

Go CNA는 Go 프로젝트(Go
[표준 라이브러리](/pkg) 및
[서브 리포지토리](https://pkg.go.dev/golang.org/x))에서 발견되는 취약점뿐만 아니라, 다른 CNA에서 이미 다루지 않은, 가져올 수 있는 Go 모듈의 공용 취약점에 대해 다룹니다.

이 범위는 Go로 작성된 애플리케이션이나 패키지에서 가져올 수 없는 취약점 (예: `main` 패키지 내의 모든 것)을 명시적으로 제외하는 데 사용됩니다. 제외된 보고에 대한 자세한 내용은 [go.dev/security/vuln/database#excluded-reports](/security/vuln/database#excluded-reports)를 참조하세요.

잠재적인 새로운 취약점을 Go 프로젝트에 보고하려면 다음을 참조하세요:
[go.dev/security/policy](https://go.dev/security/policy)

## 공공 취약점에 대한 CVE ID 요청

**중요**: 아래에 연결된 양식은 이슈 추적 시스템에 공개 이슈를 생성하므로,
*반드시* Go의 미공지된 취약점을 보고하기 위한 용도로 사용해서는 안 됩니다 (미공지된 이슈 보고 방법에 대한 자세한 내용은 [보안 정책](/security/policy)을 참조).

기존의 공개적인 Go 생태계의 취약점에 대해 CVE ID를 요청하려면,
[이 양식을 통해 요청 제출](/s/vulndb-report-new)

취약점은 다음과 같은 경우에 공개 취약점이라고 간주됩니다.

*   이미 공개적으로 알려졌거나
*   당신이 관리하는 패키지에 존재하며, 공개적으로 알려질 준비가 완료된 경우
