[Go 취약점 관리로 돌아가기](/security/vuln)

## 개요

Go CNA는 Go 생태계의 공개 취약점에 대해 [CVE ID](https://www.cve.org/ResourcesSupport/Glossary?activeTerm=glossaryCVEID)를 부여하고 [CVE Record](https://www.cve.org/ResourcesSupport/Glossary?activeTerm=glossaryRecord)를 게시하는 [CVE Numbering Authority](https://www.cve.org/ProgramOrganization/CNAs)입니다. 이는 Google CNA의 하위 CNA(sub-CNA)입니다.

## 범위

Go CNA는 Go 프로젝트(Go [표준 라이브러리](/pkg) 및 [서브 리포지토리](https://pkg.go.dev/golang.org/x))의 취약점과, 다른 CNA에서 이미 다루지 않는 가져오기 가능한(importable) Go 모듈의 공개 취약점을 다룹니다.

이 범위는 임포트할 수 없는(예: `main` 패키지의 모든 항목) Go로 작성된 애플리케이션 또는 패키지의 취약점을 명시적으로 제외하기 위한 것입니다. 제외된 보고서에 대한 자세한 내용은 [go.dev/security/vuln/database#excluded-reports](/security/vuln/database#excluded-reports)를 참조하십시오.

Go 프로젝트의 잠재적인 새로운 취약점을 보고하려면 [go.dev/security/policy](/security/policy)를 참조하십시오.

## 공개 취약점에 대한 CVE ID 요청하기

**중요**: 아래에 링크된 양식은 이슈 트래커에 공개 이슈를 생성하므로, Go의 공개되지 않은 취약점을 보고하는 데 *사용해서는 안 됩니다* (공개되지 않은 이슈 보고 방법은 [보안 정책](/security/policy)을 참조하십시오).

Go 생태계 내의 기존 공개(PUBLIC) 취약점에 대해 CVE ID를 요청하시려면,
[이 양식을 통해 요청을 제출하십시오](/s/vulndb-report-new).

취약점이 이미 공개적으로 알려졌거나, 귀하가 유지 관리하는 패키지에 존재하며 이를 공개적으로 알릴 준비가 된 경우 해당 취약점은 공개된 것으로 간주됩니다.
