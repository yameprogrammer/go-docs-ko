[Go 보안으로 돌아가기](/security)

이 페이지는 Go 개발자에게 프로젝트의 보안을 우선시하는 데 도움이 되는 모범 사례를 제공합니다. 퍼징을 통한 자동화된 테스트부터 경매 조건의 쉬운 확인까지, 이러한 팁은 코드를 더 안전하고 안정적으로 만드는 데 도움이 될 수 있습니다.

## 소스 코드 및 바이너리를 스캔하여 취약점 감지

정기적으로 코드를 스캔하고 바이너리에서 취약점을 확인하면 잠재적인 보안 위험을 조기에 식별하는 데 도움이 됩니다.
[govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)를 사용하여 코드를 스캔하고, 어떤 취약점이 실제로 영향을 미치는지 분석할 수 있습니다.
[govulncheck](https://pkg.go.dev)를 기반으로 하는 취약점 데이터베이스를 활용하십시오.
[govulncheck 튜토리얼](/doc/tutorial/govulncheck)을 시작하여 사용법을 익히세요.

`Govulncheck`는 CI/CD 워크플로우에 통합할 수도 있습니다.
Go 팀은
[GitHub Marketplace에서 govulncheck용 GitHub Action](https://github.com/marketplace/actions/golang-govulncheck-action)을 제공합니다.
`Govulncheck`는 또한 개발자가 취약점 스캔을 다른 CI/CD 시스템과 통합하는 데 도움이 되는 `-json` 플래그를 지원합니다.

다음과 같이, 코드 편집기에서 직접 취약점을 검색할 수도 있습니다.
[Visual Studio Code용 Go 확장 기능](/security/vuln/editor)을 사용하세요.
[이 튜토리얼](/doc/tutorial/govulncheck-ide)을 시작하여 자세히 알아보세요.

## Go 버전 및 종속성을 최신 상태로 유지하세요

```
go version
```

최신 [Go 버전]을 유지하면 다음을 제공합니다:
* 최신 언어 기능,
* 성능 개선,
* 알려진 보안 취약점에 대한 패치.
업데이트된 Go 버전은 또한 새 버전의 종속성과 호환되도록 보장하여 잠재적인 통합 문제를 방지하는 데 도움이 됩니다.
Go 릴리스 간의 변경 사항을 확인하려면 [Go 릴리스 기록](/doc/devel/release)을 참조하십시오.
Go 팀은 릴리스 주기 동안 보안 버그를 해결하기 위해 점진적인 릴리스를 배포합니다.
최신 보안 패치를 보장하려면 항상 최신 Go 마이너 버전을 업데이트하십시오.

최신 버전으로 유지 관리하는 것은 또한 소프트웨어 보안, 성능 및 Go 생태계의 최신 표준 준수를 위해 제3자 종속성에 매우 중요합니다.
그러나, 철저한 검토 없이 최신 버전으로 업데이트하는 것은 위험할 수 있습니다[예:](https://research.swtch.com/npm-colors),
새로운 버그, 호환되지 않는 변경 사항 또는 심지어 악성 코드를 유발할 수 있습니다.
따라서, 최신 보안 패치 및 개선 사항을 위해 종속성을 업데이트하는 것이 중요하지만,
각 업데이트는 신중하게 검토하고 테스트해야 합니다.

## 퍼징을 사용하여 취약점을 발견하기 위한 테스트

[퍼징](/security/fuzz)은 자동화된 테스트 방법으로,
코드 내의 다양한 경우를 탐색하기 위해 무작위 입력을 조작하고, 커버리지 지침을 사용하여
SQL 삽입, 버퍼 오버플로우, 서비스 거부 및 크로스 사이트 스크립팅 공격과 같은 잠재적인 취약점을 찾고 보고합니다.
퍼징은 프로그래머가 놓치거나 테스트하기에 너무 가능성이 낮다고 생각하는 경계 사례에 도달할 수 있습니다.
[이 튜토리얼]( /doc/tutorial/fuzz)을 시작하세요.

## Go의 Race Detector을 사용하여 경쟁 조건 검사하기

Go의 Race Detector는 프로그램에서 발생할 수 있는 경쟁 조건(race condition)을 자동으로 탐지하는 데 도움이 되는 도구입니다. 경쟁 조건은 여러 goroutine이 공유 자원에 동시에 접근할 때 발생하며, 예측 불가능한 결과를 초래할 수 있습니다.

Race Detector를 사용하면 다음과 같은 이점을 얻을 수 있습니다.

*   **자동 탐지:** Race Detector는 프로그램 실행 중에 공유 자원에 대한 동시 접근을 감지하고 잠재적인 경쟁 조건을 식별합니다.
*   **명확한 문제 진단:** Race Detector는 문제가 발생하는 특정 코드 영역을 정확하게 지적하여 디버깅을 용이하게 합니다.
*   **프로그램 안정성 향상:** Race Detector를 통해 경쟁 조건을 사전에 방지함으로써 프로그램의 안정성과 예측 가능성을 높일 수 있습니다.

**Race Detector 사용 방법**

Race Detector를 사용하려면 다음과 같은 단계를 따르세요.

1.  **Race Detector 설치:**

    ```bash
    go install golang.org/x/tools/cmd/go vet
    ```

2.  **프로그램 빌드 및 실행:**

    ```bash
    go build -race your_program.go
    ./your_program
    ```

    `-race` 플래그는 Race Detector를 활성화합니다.

3.  **Race Detector 결과 확인:**

    프로그램 실행 중에 Race Detector는 잠재적인 경쟁 조건을 감지하고 오류 메시지를 출력합니다. 이러한 메시지는 문제가 발생하는 코드 영역과 관련 goroutine을 식별하는 데 도움이 됩니다.

**예제**

다음은 Race Detector가 탐지할 수 있는 간단한 경쟁 조건의 예입니다.

```go
package main

import (
	"fmt"
	"sync"
)

var counter int
var wg sync.WaitGroup

func increment() {
	for i := 0; i < 1000; i++ {
		// 경쟁 조건 발생 가능
		counter++
		fmt.Print(counter, " ")
	}
	wg.Done()
}

func main() {
	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go increment()
	}
	wg.Wait()
}
```

이 예제에서 `counter` 변수는 여러 goroutine에서 동시에 증가되므로 경쟁 조건이 발생할 수 있습니다. Race Detector는 이러한 상황을 감지하고 오류 메시지를 출력합니다.

**결론**

Go의 Race Detector는 프로그램에서 경쟁 조건을 자동으로 탐지하고 해결하는 데 매우 유용한 도구입니다. Race Detector를 사용하면 프로그램의 안정성을 높이고 예측 불가능한 오류를 방지할 수 있습니다.

경쟁 조건은 두 개 이상의 [goroutine](/tour/concurrency/1)이
동시에 동일한 리소스를 접근할 때 발생하며,
그 중 최소 하나는 쓰기 작업입니다.
이는 소프트웨어에서 예측 불가능하고, 진단하기 어려운 문제로 이어질 수 있습니다.
Go 코드에서 잠재적인 경쟁 조건을 식별하려면 내장된
[race detector](/doc/articles/race_detector)를 사용하세요.
이는 동시 프로그램의 안전성과 신뢰성을 보장하는 데 도움이 됩니다.
race detector는 런타임에 발생하는 경쟁을 찾지만, 실행되지 않는 코드 경로의 경쟁은 찾을 수 없습니다.

레이스 감지기를 사용하려면 테스트를 실행하거나 애플리케이션을 빌드할 때 `-race` 플래그를 추가합니다.
예: `go test -race`
이렇게 하면 레이스 감지기가 활성화된 상태로 코드를 컴파일하고, 실행 중에 감지된 모든 경쟁 상황을 보고합니다.
레이스 감지기가 프로그램에서 데이터 경쟁을 발견하면, 다음과 같은 내용을 포함하는 보고서를 [인쇄합니다](/doc/articles/race_detector#report-format):
- 충돌하는 접근에 대한 스택 트레이스
- 관련된 고루틴이 생성된 스택

## Vet 명령어를 사용하여 의심스러운 구성 요소 검사

`go vet` 명령은 Go의 [vet 명령](https://pkg.go.dev/cmd/vet)은 소스 코드를 분석하도록 설계되었습니다.
이는 구문 오류가 아닐 수 있지만, 런타임 중에 문제가 발생할 수 있는 잠재적인 문제를 식별합니다.
예를 들어, 도달할 수 없는 코드, 사용되지 않는 변수 및 goroutine 관련 일반적인 오류가 포함됩니다.
개발 프로세스의 초기에 이러한 문제를 감지함으로써, `go vet`은 코드 품질을 유지하고, 디버깅 시간을 줄이며, 전반적인 소프트웨어 신뢰성을 향상시킵니다.
특정 프로젝트에 대해 `go vet`을 실행하려면 다음 명령을 실행합니다:

```
go vet ./...
```

## golang-announce 뉴스레터를 구독하여 보안 릴리스 알림 받기

Go에서 보안 패치를 포함하는 릴리스는 [golang-announce@googlegroups.com](https://groups.google.com/group/golang-announce) 이메일 목록에 사전에 공지됩니다.
Go 자체에 대한 보안 패치가 출시될 때 알리고 싶다면, 구독하십시오.
