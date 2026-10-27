[Go 취약점 관리로 돌아가기](/security/vuln)

## 개요

Go 취약점 데이터베이스([https://vuln.go.dev](https://vuln.go.dev))는
[Open Source Vulnerability (OSV) 스키마](https://ossf.github.io/osv-schema/) 형식으로 Go 취약점 정보를 제공합니다.

또한 [pkg.go.dev/vuln](https://pkg.go.dev/vuln)에서 데이터베이스의 취약점을 찾아볼 수 있습니다.

**x/vulndb** Git 리포지토리의 내용에 의존**하지 마십시오**. 해당 리포지토리의 YAML 파일들은 예고 없이 변경될 수 있는 내부 포맷을 사용하여 관리됩니다.

## 기여하기

모든 Go 패키지 유지 관리자가 자신의 프로젝트에 있는 공개 취약점 정보를 [제공](/s/vulndb-report-new)하고, Go 패키지의 기존 취약점 정보를 [업데이트](/s/vulndb-report-feedback)해주시기를 부탁드립니다.

저희는 제보 과정의 마찰을 최소화하는 것을 목표로 하고 있습니다.
따라서 언제든지 [제안 사항을 보내주시기 바랍니다](/s/vuln-feedback).

Go 표준 라이브러리 또는 서브 리포지토리의 취약점을 보고하시려면 위 양식을 **사용하지 마십시오.**
대신, Go 프로젝트와 관련된 취약점은 [go.dev/security/policy](/security/policy)의 절차를 따라주시기 바랍니다.

## API

정식 Go 취약점 데이터베이스인 [https://vuln.go.dev](https://vuln.go.dev)는 아래에 지정된 엔드포인트에 대한 GET 요청에 응답할 수 있는 HTTP 서버입니다.

엔드포인트에는 쿼리 매개변수가 없으며, 필요한 특정 헤더도 없습니다.
이 덕분에 고정된 파일 시스템( `file://` URL 포함)에서 제공되는 사이트라도 이 API를 구현할 수 있습니다.

각 엔드포인트는 JSON으로 인코딩된 응답을 반환하며, 요청 방식에 따라 압축되지 않은 형태(`.json`으로 요청 시) 또는 gzip으로 압축된 형태(`.json.gz`로 요청 시)로 제공됩니다.

엔드포인트는 다음과 같습니다:

- `/index/db.json[.gz]`

데이터베이스에 대한 메타데이터를 반환합니다:

```json
  {
    // 데이터베이스가 수정된 것으로 간주되어야 하는 최신 시간입니다.
    // "Z"로 끝나는 RFC3339 형식의 UTC 타임스탬프여야 합니다.
    "modified": string
  }
  ```

수정 시간(modified time)을 벽시계 시간(wall clock time)과 비교해서는 *안 된다*는 점에 유의하십시오. 예를 들어, 데이터베이스 수정 사항이 실제로 반영되기까지 지연이 발생할 수 있으므로 캐시 무효화 등의 목적으로 이를 사용해서는 안 됩니다.

실시간 예시는 [/index/db.json](https://vuln.go.dev/index/db.json)에서 확인할 수 있습니다.

- `/index/modules.json[.gz]`

데이터베이스의 각 모듈에 대한 메타데이터를 포함하는 리스트를 반환합니다:

```json
  [ {
    // 모듈 경로.
    "path": string,
    // 이 모듈에 영향을 주는 취약점들.
    "vulns":
      [ {
        // 취약점 ID.
        "id": string,
        // 취약점이 마지막으로 수정된 것으로 간주되는 시간.
        // "Z"로 끝나는 RFC3339 형식의 UTC 타임스탬프로 표기합니다.
        "modified": string,
        // (선택 사항) 해당 취약점에 대한 최신 수정 사항이 포함된
        // 모듈 버전(SemVer 2.0.0 형식).
        // 알 수 없거나 제공되지 않는 경우 생략합니다.
        "fixed": string,
      } ]
  } ]
  ```

실시간 예제는 [/index/modules.json](https://vuln.go.dev/index/modules.json)을 참조하세요.

- `/index/vulns.json[.gz]`

데이터베이스에 있는 각 취약점에 대한 메타데이터를 포함하는 리스트를 반환합니다:

```json
   [ {
       // 취약점 ID.
       "id": string,
       // 취약점이 수정된 것으로 간주되는 최신 시간.
       // "Z"로 끝나는 RFC3339 형식의 UTC 타임스탬프입니다.
       "modified": string,
       // 다른 데이터베이스에 등록된 동일한 취약점 ID 목록입니다.
       "aliases": [ string ]
   } ]
  ```

실시간 예제는 [/index/vulns.json](https://vuln.go.dev/index/vulns.json)에서 확인하십시오.

- `/ID/$id.json[.gz]`

ID가 `$id`인 취약점에 대한 개별 보고서를 OSV 형식([Schema](#schema)에서 설명됨)으로 반환합니다.

실제 예시는 [/ID/GO-2022-0191.json](https://vuln.go.dev/ID/GO-2022-0191.json)을 참조하십시오.

### 대량 다운로드

전체 Go 취약점 데이터베이스를 더 쉽게 다운로드할 수 있도록, 모든 인덱스 및 OSV 파일이 포함된 zip 파일을 [vuln.go.dev/vulndb.zip](https://vuln.go.dev/vulndb.zip)에서 제공합니다.

### `govulncheck`에서의 사용법

기본적으로 `govulncheck`는 [vuln.go.dev](https://vuln.go.dev)에 있는 공식 Go 취약점 데이터베이스를 사용합니다.

`-db` 플래그를 사용하여 다른 취약점 데이터베이스에 접속하도록 명령어를 설정할 수 있으며, 이 플래그는 `http://`, `https://` 또는 `file://` 프로토콜을 사용하는 취약점 데이터베이스 URL을 허용합니다.

`govulncheck`가 올바르게 작동하려면, 지정된 취약점 데이터베이스가 위에 설명된 API를 구현해야 합니다. `govulncheck` 명령은 http(s) 소스에서 읽을 때는 압축된 ".json.gz" 엔드포인트를 사용하며, 파일 소스에서 읽을 때는 ".json" 엔드포인트를 사용합니다.

### 레거시 API

정식 데이터베이스에는 레거시 API의 일부인 몇 가지 추가 엔드포인트가 포함되어 있습니다.
저희는 곧 이러한 엔드포인트에 대한 지원을 중단할 계획입니다. 만약 레거시 API를 사용 중이며 마이그레이션을 위한 추가 시간이 필요하시다면, [저희에게 알려주시기 바랍니다](/s/govulncheck-feedback).

## 스키마

리포트는 [Open Source Vulnerability (OSV) 스키마](https://ossf.github.io/osv-schema/)를 사용합니다.
Go 취약점 데이터베이스는 각 필드에 다음과 같은 의미를 부여합니다.

### id

`id` 필드는 취약점 항목의 고유 식별자입니다. 이 필드는 `GO-<YEAR>-<ENTRYID>` 형식의 문자열입니다.

### 영향받는 범위

[affected](https://ossf.github.io/osv-schema/#affected-fields) 필드는 취약점이 포함된 모듈 버전을 설명하는 객체들을 포함하는 JSON 배열입니다.

#### affected[].package

[affected[].package](https://ossf.github.io/osv-schema/#affectedpackage-field)
필드는 영향을 받는 _모듈_을 식별하는 JSON 객체입니다. 이 객체에는 두 가지 필수 필드가 있습니다:

- **ecosystem**: 이 값은 항상 "Go"입니다.
- **name**: Go 모듈 경로입니다.
  - 표준 라이브러리에서 임포트 가능한 패키지는 이름이 _stdlib_가 됩니다.
  - go 명령어는 이름이 _toolchain_이 됩니다.

#### affected[].ecosystem_specific

[affected[].ecosystem_specific](https://ossf.github.io/osv-schema/#affectedecosystem_specific-field)
필드는 취약점에 대한 추가 정보를 담은 JSON 객체이며, Go의 취약점 탐지 도구에서 사용됩니다.

현재로서는 ecosystem specific은 항상 `imports`라는 단일 필드를 가진 객체가 됩니다.

##### affected[].ecosystem_specific.imports

`affected[].ecosystem_specific.imports` 필드는 취약점의 영향을 받는 패키지와 심볼을 포함하는 JSON 배열입니다. 배열의 각 객체는 다음 두 필드를 가집니다:

- **path:** 취약점이 포함된 패키지의 임포트 경로(import path)를 나타내는 문자열
- **symbols:** 취약점이 포함된 심볼(함수 또는 메서드)의 이름들을 담은 문자열 배열
- **goos**: 심볼이 나타나는 실행 운영체제를 알고 있는 경우, 해당 운영체제들의 문자열 배열
- **goarch**: 심볼이 나타나는 아키텍처를 알고 있는 경우, 해당 아키텍처들의 문자열 배열

### database_specific

`database_specific` 필드는 Go 취약점 데이터베이스에 특화된 사용자 정의 필드들을 포함합니다.

#### database_specific.url

`database_specific.url` 필드는 Go 취약점 보고서의 전체 경로 URL을 나타내는 문자열입니다. 예: "https://pkg.go.dev/vuln/GO-2023-1621".

#### database_specific.review_status

`database_specific.review_status` 필드는 취약점 보고서의 검토 상태를 나타내는 문자열입니다. 이 필드가 없는 경우, 해당 보고서는 `REVIEWED` 상태인 것으로 간주해야 합니다. 가능한 값은 다음과 같습니다:

- `UNREVIEWED`: 보고서가 CVE 또는 GHSA와 같은 다른 소스를 기반으로 자동 생성되었습니다. 데이터가 제한적일 수 있으며 Go 팀의 검증을 거치지 않았습니다.
- `REVIEWED`: 보고서가 Go 팀에서 시작되었거나 외부 소스를 기반으로 생성되었습니다. Go 팀원이 보고서를 검토하였으며, 적절한 경우 추가 데이터를 추가했습니다.

스키마의 다른 필드에 대한 정보는 [OSV spec](https://ossf.github.io/osv-schema)을 참조하세요.

## 버전 관련 참고 사항

우리의 툴링은 표준 [Go module version numbers](/doc/modules/version-numbers)에 따라 소스 권고안(advisories)의 모듈과 버전을 정준(canonical) Go 모듈 및 버전으로 자동 매핑하려고 시도합니다. `govulncheck`와 같은 도구들은 이러한 표준 버전에 의존하여 Go 프로젝트가 종속성의 취약점에 영향을 받는지 여부를 판단하도록 설계되었습니다.

Go 프로젝트가 자체적인 버전 관리 체계를 사용하는 경우와 같이, 표준 Go 버전으로의 매핑이 실패할 수 있는 사례가 있습니다. 이런 일이 발생하면 Go 취약점 데이터베이스 보고서는 보수적으로 모든 Go 버전을 영향 받는 것으로 나열할 수 있습니다. 이는 `govulncheck`와 같은 도구가 인식되지 않은 버전 범위로 인해 취약점 보고를 누락하는 상황(미검출, false negatives)을 방지하기 위함입니다. 하지만 모든 버전을 영향 받는 것으로 보수적으로 나열하면, 도구가 모듈의 수정된 버전을 취약점이 포함된 것으로 잘못 보고하는 상황(오탐, false positives)이 발생할 수 있습니다.

`govulncheck`가 취약점을 잘못 보고하고 있거나(또는 보고하지 못하고 있다고) 생각하신다면, 취약점 보고서에 [수정을 제안](https://github.com/golang/vulndb/issues/new?assignees=&labels=Needs+Triage%2CSuggested+Edit&template=suggest_edit.yaml&title=x%2Fvulndb%3A+suggestion+regarding+GO-2024-2965&report=GO-XXXX-YYYY)해 주세요. 검토 후 반영하겠습니다.

## 예제

Go 취약점 데이터베이스의 모든 취약점은 위에 설명된 OSV 스키마를 사용합니다.

다양한 Go 취약점 예시는 아래 링크를 참조하십시오:

- **Go 표준 라이브러리 취약점** (GO-2022-0191):
  [JSON](https://vuln.go.dev/ID/GO-2022-0191.json),
  [HTML](https://pkg.go.dev/vuln/GO-2022-0191)
- **Go 툴체인 취약점** (GO-2022-0189):
  [JSON](https://vuln.go.dev/ID/GO-2022-0189.json),
  [HTML](https://pkg.go.dev/vuln/GO-2022-0189)
- **Go 모듈 취약점** (GO-2020-0015):
  [JSON](https://vuln.go.dev/ID/GO-2020-0015.json),
  [HTML](https://pkg.go.dev/vuln/GO-2020-0015)

## 제외된 보고서

Go 취약점 데이터베이스의 보고서는 다양한 소스에서 수집되며 Go 보안 팀에 의해 큐레이션됩니다. 저희는 취약점 권고(예: CVE 또는 GHSA)를 발견하더라도 여러 가지 이유로 이를 제외하기로 결정할 수 있습니다. 이러한 경우, [x/vulndb/data/excluded](https://github.com/golang/vulndb/tree/master/data/excluded) 아래의 x/vulndb 저장소에 최소한의 보고서가 생성됩니다.

다음과 같은 이유로 보고서가 제외될 수 있습니다:

- `NOT_GO_CODE`: 취약점이 Go 패키지에 있는 것이 아니라, 다른 소스에 의해 Go 생태계의 보안 권고로 표시된 경우입니다. 이 취약점은 어떠한 Go 패키지에도 영향을 미칠 수 없습니다. (예: C++ 라이브러리의 취약점)
- `NOT_IMPORTABLE`: 취약점이 `main` 패키지, `main` 패키지에 의해서만 임포트되는 `internal/` 패키지, 또는 다른 모듈에서 절대 임포트할 수 없는 다른 위치에서 발생하는 경우입니다.
- `EFFECTIVELY_PRIVATE`: 취약점이 다른 모듈에서 임포트할 수 있는 Go 패키지에서 발생하지만, 해당 패키지가 외부 사용을 위해 의도되지 않았으며 정의된 모듈 외부에서 임포트될 가능성이 낮은 경우입니다.
- `DEPENDENT_VULNERABILITY`: 이 취약점은 데이터베이스에 있는 다른 취약점의 하위 집합입니다. 예를 들어, 패키지 A에 취약점이 있고 패키지 B가 패키지 A에 의존하며 패키지 A와 B에 대해 별도의 CVE ID가 있는 경우, B에 대한 보고서를 A의 보고서에 의해 완전히 대체되는 종속 취약점으로 표시할 수 있습니다.
- `NOT_A_VULNERABILITY`: CVE ID 또는 GHSA가 할당되었지만, 이와 관련된 알려진 취약점이 없는 경우입니다.
- `WITHDRAWN`: 취약점이 소스에 의해 철회된 경우입니다.

현재 제외된 보고서는 [vuln.go.dev](https://vuln.go.dev) API를 통해 제공되지 않습니다. 하지만 특정 사용 사례가 있거나 API를 통해 이 정보에 액세스하는 것이 도움이 될 경우, [저희에게 알려주시기 바랍니다](/s/govulncheck-feedback).
