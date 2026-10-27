[Go 취약점 관리로 돌아가기](/security/vuln)

## 개요

Go 취약점 데이터베이스 ([https://vuln.go.dev](https://vuln.go.dev))는
[Open Source Vulnerability (OSV) 스키마](https://ossf.github.io/osv-schema/)를 사용하여
Go 취약점 정보를 제공합니다.

또한, 데이터베이스에서 취약점을 검색할 수 있습니다. [pkg.go.dev/vuln](https://pkg.go.dev/vuln) 에서 확인하십시오.

**다음 내용을 참조하지 마세요.** x/vulndb Git 저장소의 YAML 파일은 내부 형식으로 관리되며, 사전 예고 없이 변경될 수 있습니다.

## 기여하기

저희는 모든 Go 패키지 관리자가 자신의 프로젝트에 대한 공개적인 취약점에 대한 정보를 [기여]( /s/vulndb-report-new)하고,
Go 패키지에 대한 기존의 취약점 정보를 [업데이트]( /s/vulndb-report-feedback)하도록 요청합니다.

저희는 보고 프로세스를 최대한 간편하게 만들기 위해 노력하고 있습니다.
따라서, 제안 사항이 있으시면 [저희에게 보내주세요](/s/vuln-feedback).

**Go** 표준 라이브러리 또는 하위 저장소에 대한 취약점을 보고할 때는 다음 양식을 사용하지 마십시오.
대신, Go 프로젝트에 대한 취약점에 대한 절차는 [go.dev/security/policy](/security/policy)를 참조하십시오.

## API

공식 Go 취약점 데이터베이스인 [https://vuln.go.dev](https://vuln.go.dev)는 아래에 지정된 엔드포인트에 대한 GET 요청을 처리할 수 있는 HTTP 서버입니다.

이 엔드포인트는 쿼리 매개변수를 사용하지 않고, 특정 헤더도 필요하지 않습니다.
따라서, 고정 파일 시스템(예: `file://` URL)에서 서비스를 제공하는 웹사이트도 이 API를 구현할 수 있습니다.

각 엔드포인트는 JSON 형식으로 인코딩된 응답을 반환하며, 압축되지 않은 형식(`.json`) 또는 gzipped 형식(`.json.gz`)으로 반환됩니다 (요청 시).

다음 엔드포인트가 있습니다:

- `/index/db.json[.gz]`

데이터베이스에 대한 메타데이터를 반환합니다:

```json
  {
    // 데이터베이스가 마지막으로 변경된 시점을 나타내는
    // RFC3339 형식의 UTC 시간(마지막에 "Z"로 끝나는)
    "modified": string
  }
```

참고: 수정 시간은 벽시계 시간과 비교해서는 안 됩니다.
예를 들어, 캐시 무효화 목적으로는, 데이터베이스 수정이 적용되는 데 시간이 걸릴 수 있으므로 사용해서는 안 됩니다.

`/index/db.json`에서 실시간 예제를 확인하세요.

- `/index/modules.json[.gz]`

데이터베이스 내 각 모듈에 대한 메타데이터를 포함하는 목록을 반환합니다:

```json
  [
    {
      // 모듈 경로.
      "path": "string",
      // 이 모듈에 영향을 미치는 취약점.
      "vulns": [
        {
          // 취약점 ID.
          "id": "string",
          // 취약점이 마지막으로 수정된 시점 (RFC3339 형식의 UTC 시간, "Z"로 끝나는).
          "modified": "string",
          // (선택 사항) 취약점에 대한 최신 패치를 포함하는 모듈 버전 (SemVer 2.0.0 형식).
          // 알려지지 않았거나 사용할 수 없는 경우 이 필드는 생략해야 합니다.
          "fixed": "string",
        }
      ]
    }
  ]
```

`/index/modules.json`에서 실시간 예제를 참조하십시오.

- `/index/vulns.json[.gz]`

데이터베이스 내 각 취약점에 대한 메타데이터를 포함하는 목록을 반환합니다:

```json
   [ {
       // 취약점 ID.
       "id": 문자열,
       // 취약점이 마지막으로 수정된 시간을 RFC3339 형식의 UTC
       // 시간(마지막에 "Z"로 끝나는)으로 나타냅니다.
       "modified": 문자열,
       // 동일한 취약점의 다른 데이터베이스에서 취약점 ID 목록입니다.
       "aliases": [ 문자열 ]
   } ]
  ```

`/index/vulns.json`에서 실시간 예제를 참조하십시오.

- `/ID/$id.json[.gz]`

반환되는 것은 `$id` ID를 가진 취약점에 대한 개별 보고서이며, OSV 형식 (아래의 [스키마](#schema)에서 설명)으로 제공됩니다.

자세한 예제를 보려면 [/ID/GO-2022-0191.json](https://vuln.go.dev/ID/GO-2022-0191.json) 참조하십시오.

### 대량 다운로드

전체 Go 취약점 데이터베이스를 다운로드하는 데 도움이 되도록, 인덱스 및 OSV 파일이 모두 포함된 zip 파일은 다음 위치에서 사용할 수 있습니다:
[vuln.go.dev/vulndb.zip](https://vuln.go.dev/vulndb.zip).

### `govulncheck`에서의 사용법

```
govulncheck --scan-type=security <패턴>
```

예시:

```
govulncheck --scan-type=security "example.com"
```

이 명령어는 `example.com` 도메인에서 보안 취약점을 검색합니다.

기본적으로, `govulncheck`은 [vuln.go.dev](https://vuln.go.dev)에서 제공하는 공식 Go 취약점 데이터베이스를 사용합니다.

이 명령은 `-db` 플래그를 사용하여 다른 취약점 데이터베이스에 연결하도록 구성할 수 있습니다. 이 플래그는 `http://`, `https://`, 또는 `file://` 프로토콜을 사용하는 취약점 데이터베이스 URL을 허용합니다.

`govulncheck`와 올바르게 작동하려면, 지정된 취약점 데이터베이스가 위에 설명된 API를 구현해야 합니다. `govulncheck` 명령은 http(s) 소스에서 읽을 때 압축된 ".json.gz" 엔드포인트를 사용하고, 파일 소스에서 읽을 때 ".json" 엔드포인트를 사용합니다.

### 기존 API

표준 데이터베이스에는 일부 추가 엔드포인트가 있으며, 이는 오래된 API의 일부입니다.
저희는 곧 이러한 엔드포인트에 대한 지원을 중단할 예정입니다. 만약 귀하가 오래된 API에 의존하고 있으며, 마이그레이션에 추가 시간이 필요하다면, [저희에게 알려주세요](/s/govulncheck-feedback).

## 스키마

보고서는 다음
[오픈 소스 취약점 (OSV) 스키마](https://ossf.github.io/osv-schema/)를 사용합니다.
Go 취약점 데이터베이스는 다음 필드에 다음과 같은 의미를 할당합니다:

### id

`id` 필드는 취약점 항목에 대한 고유 식별자입니다. 형식은 `GO-<YEAR>-<ENTRYID>`입니다.

### 영향을 받은

[영향을 받는](https://ossf.github.io/osv-schema/#affected-fields) 필드는
취약점을 포함하는 모듈 버전을 설명하는 객체가 포함된 JSON 배열입니다.

#### 영향을 받는 패키지

The
[affected[].package](https://ossf.github.io/osv-schema/#affectedpackage-field)
필드는 영향을 받는 _모듈_을 식별하는 JSON 객체입니다. 이 객체에는 두 개의 필수 필드가 있습니다:

- **생태계**: 이 값은 항상 "Go"입니다.
- **이름**: 이것은 Go 모듈 경로입니다.
  - 표준 라이브러리에 있는 가져올 수 있는 패키지는 _stdlib_라는 이름을 가집니다.
  - `go` 명령은 _toolchain_라는 이름을 가집니다.

#### affected[].ecosystem_specific

The
[affected[].ecosystem_specific](https://ossf.github.io/osv-schema/#affectedecosystem_specific-field)
필드는 Go의 취약점 탐지 도구에서 사용되는, 취약점에 대한 추가 정보를 포함하는 JSON 객체입니다.

현재, 생태계별로 특정하는 것은 항상 단일 필드가 있는 객체입니다.
`imports`

##### 영향을 받는 애플리케이션의 종속성

`affected[].ecosystem_specific.imports` 필드는 JSON 배열이며, 이 배열에는 취약점에 영향을 받는 패키지와 심볼이 포함되어 있습니다. 배열 내의 각 객체는 다음 두 필드를 갖습니다:

- **path:** 패키지 내의 취약점을 포함하는 임포트 경로 문자열
- **symbols:** 취약점이 포함된 심볼 (함수 또는 메서드)의 이름 문자열 배열
- **goos:** 심볼이 나타나는 실행 운영 체제가 알려진 경우, 문자열 배열
- **goarch:** 심볼이 나타나는 아키텍처가 알려진 경우, 문자열 배열

### 데이터베이스별

`database_specific` 필드는 Go 취약점 데이터베이스에 특정한 사용자 정의 필드를 포함합니다.

```
#### 데이터베이스별 URL
```

`database_specific.url` 필드는 Go 취약점 보고서의 완전한 URL을 나타내는 문자열입니다. 예: "https://pkg.go.dev/vuln/GO-2023-1621".

```
#### 데이터베이스별 리뷰 상태
```

`database_specific.review_status` 필드는 취약점 보고의 검토 상태를 나타내는 문자열입니다. 만약 필드가 존재하지 않으면 보고서를 `REVIEWED`로 간주합니다. 가능한 값은 다음과 같습니다:

- `UNREVIEWED`: 보고는 다른 소스 (예: CVE 또는 GHSA)를 기반으로 자동으로 생성되었습니다. 데이터가 제한적이며 Go 팀에 의해 확인되지 않았습니다.
- `REVIEWED`: 보고는 Go 팀에서 작성되었거나 외부 소스를 기반으로 생성되었습니다. Go 팀의 구성원이 보고를 검토하고, 필요한 경우 추가 데이터를 추가했습니다.

다른 필드에 대한 정보는 스키마에서 참조하십시오. [OSV 사양](https://ossf.github.io/osv-schema)을 참조하십시오.

## 버전 정보

우리 도구는 소스 권고 사항에 있는 모듈 및 버전 정보를 표준 [Go 모듈 버전 번호](/doc/modules/version-numbers)에 따라, 표준 Go 모듈 및 버전으로 자동 매핑하려고 시도합니다. `govulncheck`와 같은 도구는 이러한 표준 버전을 사용하여 Go 프로젝트가 종속성에 존재하는 취약점의 영향을 받는지 여부를 결정하도록 설계되었습니다.

일부 경우, 특히 Go 프로젝트가 자체 버전 관리 체계를 사용하는 경우,
표준 Go 버전으로의 매핑이 실패할 수 있습니다. 이러한 경우, Go
취약점 데이터베이스 보고서가 모든 Go 버전을 영향을 받는 것으로
보수적으로 나열할 수 있습니다. 이를 통해 `govulncheck`과 같은 도구가
알 수 없는 버전 범위로 인해 취약점을 보고하지 못하는 것을 방지합니다 (오탐 방지).
그러나 모든 버전을 영향을 받는 것으로 보수적으로 나열하면, 도구가 특정 모듈의
고정 버전에 취약성이 존재한다고 잘못 보고할 수 있습니다 (오탐).

만약 `govulncheck`이 취약점을 잘못 보고하거나 보고하지 않는다고 생각하면,
취약점 보고에 다음을 제안해주세요:
[편집 제안](https://github.com/golang/vulndb/issues/new?assignees=&labels=Needs+Triage%2CSuggested+Edit&template=suggest_edit.yaml&title=x%2Fvulndb%3A+GO-2024-2965+관련 제안&report=GO-XXXX-YYYY)
그러면 저희가 검토하겠습니다.

## 예제

Go 취약점 데이터베이스에 있는 모든 취약점은 위에서 설명된 OSV 스키마를 사용합니다.

아래 링크를 참조하여 다양한 Go 취약점의 예제를 확인하십시오:

- **Go 표준 라이브러리 취약점** (GO-2022-0191):
  [JSON](https://vuln.go.dev/ID/GO-2022-0191.json),
  [HTML](https://pkg.go.dev/vuln/GO-2022-0191)
- **Go 툴체인 취약점** (GO-2022-0189):
  [JSON](https://vuln.go.dev/ID/GO-2022-0189.json),
  [HTML](https://pkg.go.dev/vuln/GO-2022-0189)
- **Go 모듈 내 취약점** (GO-2020-0015):
  [JSON](https://vuln.go.dev/ID/GO-2020-0015.json),
  [HTML](https://pkg.go.dev/vuln/GO-2020-0015)

## 제외된 보고서

Go 취약점 데이터베이스의 보고서는 다양한
출처에서 수집되며, Go 보안 팀에서 관리합니다. 우리는 취약점 알림(예: CVE 또는 GHSA)을 발견하고 다양한 이유로 제외할 수 있습니다.
이 경우, `x/vulndb` 저장소에 최소한의 보고서가 생성됩니다.
[x/vulndb/data/excluded](https://github.com/golang/vulndb/tree/master/data/excluded)에 있습니다.

보고서는 다음과 같은 이유로 제외될 수 있습니다:

- `NOT_GO_CODE`: 이 취약점은 Go 패키지에 있지 않지만, 다른 출처에서 Go 생태계에 대한 보안 조언으로 표시되었습니다.
  이 취약점은 어떤
  Go 패키지도 영향을 미치지 않습니다. (예: C++ 라이브러리의 취약점)
- `NOT_IMPORTABLE`: 이 취약점은 `main` 패키지 또는 `internal/` 패키지에 발생하며, `main` 패키지만 가져올 수 있거나, 다른 모듈에서 가져올 수 없는 위치에 발생합니다.
- `EFFECTIVELY_PRIVATE`: 다른 모듈에서 가져올 수 있는 Go 패키지에 취약점이 발생하지만, 해당 패키지는 외부 사용을 위한 것이 아니며, 정의된 모듈 외부에서 가져오는 경우는 거의 없을 것입니다.
- `DEPENDENT_VULNERABILITY`: 이 취약점은 데이터베이스의 다른 취약점의 하위 집합입니다. 예를 들어, 패키지 A에 취약점이 있는 경우, 패키지 B가 패키지 A에 의존하고, 패키지 A와 B에 별도의 CVE ID가 있는 경우, 보고서를 A에 대한 보고서에 완전히 대체하여 B에 대한 보고서를 표시할 수 있습니다.
- `NOT_A_VULNERABILITY`: CVE ID 또는 GHSA가 할당되었지만, 관련된 알려진 취약점은 없습니다.
- `WITHDRAWN`: 해당 출처에서 취약점이 철회되었습니다.

현재 제외된 보고는 [vuln.go.dev](https://vuln.go.dev) API를 통해 제공되지 않습니다. 하지만, 특정 사용 사례가 있고 API를 통해 이 정보를 얻는 것이 도움이 된다면, [피드백을 보내주세요](/s/govulncheck-feedback).
