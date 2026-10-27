[Go 보안으로 돌아가기](/security)

이 페이지는 Go 개발자가 프로젝트의 보안을 우선시하기 위한 모범 사례를 제공합니다. 퍼징(fuzzing)을 통한 테스트 자동화부터 레이스 컨디션(race conditions)의 간편한 확인까지, 이러한 팁들은 코드베이스를 더욱 안전하고 신뢰할 수 있게 만드는 데 도움이 됩니다.

## 소스 코드 및 바이너리 취약점 스캔

코드와 바이너리를 정기적으로 스캔하여 취약점을 찾는 것은 잠재적인 보안 리스크를 조기에 식별하는 데 도움이 됩니다.

[Go vulnerability database](https://pkg.go.dev)를 기반으로 하는 [govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)를 사용하여 코드의 취약점을 스캔하고, 어떤 취약점이 실제로 영향을 미치는지 분석할 수 있습니다.

[govulncheck 튜토리얼](/doc/tutorial/govulncheck)을 통해 시작해 보세요.

Govulncheck는 CI/CD 흐름에도 통합될 수 있습니다.
Go 팀은 GitHub Marketplace에서
[govulncheck를 위한 GitHub Action](https://github.com/marketplace/actions/golang-govulncheck-action)을
제공합니다.
또한 Govulncheck는 개발자가 취약점 스캔을 다른 CI/CD 시스템과 통합하는 것을 돕기 위해 `-json` 플래그를 지원합니다.

[Visual Studio Code용 Go 확장 기능](/security/vuln/editor)을 사용하여 코드 에디터에서 직접 취약점을 스캔할 수도 있습니다.
[이 튜토리얼](/doc/tutorial/govulncheck-ide)을 통해 시작해 보세요.

## Go 버전과 의존성을 최신 상태로 유지하세요

[Go 버전을 최신 상태로 유지](/doc/install)하면
최신 언어 기능, 성능 향상 및 알려진 보안 취약점에 대한 패치를 이용할 수 있습니다.
업데이트된 Go 버전은 최신 버전의 종속성과의 호환성을 보장하여,
잠재적인 통합 문제를 피하는 데 도움이 됩니다.
릴리스 간에 Go에 어떤 변경 사항이 있었는지 확인하려면 [Go 릴리스 기록](/doc/devel/release)을 검토하십시오.
Go 팀은 보안 버그를 해결하기 위해 릴리스 주기 전반에 걸쳐 포인트 릴리스(point releases)를 발행합니다.
최신 보안 수정 사항이 적용되었는지 확인하려면 반드시 최신 마이너(minor) Go 버전으로 업데이트하십시오.

최신 상태의 서드파티 의존성을 유지하는 것은 소프트웨어 보안, 성능, 그리고 Go 생태계의 최신 표준 준수를 위해 매우 중요합니다. 하지만 철저한 검토 없이 최신 버전으로 업데이트하는 것은 [위험할 수도 있으며](https://research.swtch.com/npm-colors), 잠재적으로 새로운 버그, 호환되지 않는 변경 사항, 또는 심지어 악성 코드를 유입시킬 수 있습니다. 따라서 최신 보안 패치와 개선 사항을 위해 의존성을 업데이트하는 것이 필수적이지만, 각 업데이트는 신중하게 검토하고 테스트해야 합니다.

## 퍼징(fuzzing) 테스트를 통한 엣지 케이스 익스플로잇 발견

[퍼징(Fuzzing)](/security/fuzz)은 커버리지 가이드(coverage guidance)를 사용하여 무작위 입력을 조작하고 코드를 탐색함으로써 SQL 인젝션, 버퍼 오버플로, 서비스 거부(DoS) 및 교차 사이트 스크립팅(XSS) 공격과 같은 잠재적인 취약점을 찾아 보고하는 자동화된 테스트 방식입니다. 퍼징은 프로그래머가 놓치거나 테스트하기에는 너무 희박한 확률이라고 판단한 엣지 케이스(edge cases)를 찾는 데 효과적입니다.
[이 튜토리얼](/doc/tutorial/fuzz)을 통해 시작해 보세요.

## Go의 race detector로 레이스 컨디션 확인하기

경쟁 상태(Race conditions)는 두 개 이상의 [goroutines](/tour/concurrency/1)가
동일한 리소스에 동시에 접근하고,
그중 최소 하나가 쓰기 작업일 때 발생합니다.
이는 소프트웨어에서 예측 불가능하고 진단하기 어려운 문제로 이어질 수 있습니다.
내장된 [race detector](/doc/articles/race_detector)를 사용하여 Go 코드에서 잠재적인 경쟁 상태를 식별하십시오.
이를 통해 동시성 프로그램의 안전성과 신뢰성을 확보할 수 있습니다.
다만, race detector는 런타임에 발생하는 경쟁 상태를 찾으므로,
실행되지 않은 코드 경로에 있는 경쟁 상태는 찾지 못합니다.

레이스 디텍터(race detector)를 사용하려면 테스트를 실행하거나 애플리케이션을 빌드할 때 `-race` 플래그를 추가하세요. 예를 들어, `go test -race`와 같이 사용합니다.
이렇게 하면 레이스 디텍터가 활성화된 상태로 코드가 컴파일되며, 런타임에 감지된 모든 레이스 컨디션(race conditions)을 보고합니다.
레이스 디텍터가 프로그램에서 데이터 레이스를 발견하면, 충돌이 발생한 액세스에 대한 스택 트레이스와 관련 고루틴(goroutines)이 생성된 지점의 스택이 포함된 [보고서를 출력](/doc/articles/race_detector#report-format)합니다.

## Vet를 사용하여 의심스러운 구문 검사하기

Go의 [vet 명령](https://pkg.go.dev/cmd/vet)은 소스 코드를 분석하여 반드시 구문 오류(syntax error)는 아니지만 런타임 중에 문제가 될 수 있는 잠재적인 이슈를 표시하도록 설계되었습니다.
여기에는 도달할 수 없는 코드(unreachable code), 사용되지 않는 변수, 그리고 고루틴(goroutine)과 관련된 흔한 실수와 같은 의심스러운 구조들이 포함됩니다.
개발 프로세스 초기 단계에서 이러한 이슈들을 포착함으로써, `go vet`은 코드 품질을 유지하고 디버깅 시간을 단축하며 소프트웨어의 전반적인 신뢰성을 높이는 데 도움을 줍니다.
특정 프로젝트에 대해 `go vet`을 실행하려면 다음을 실행하세요:

```
go vet ./...
```

## 보안 릴리스 알림을 위해 golang-announce 구독하기

보안 수정 사항이 포함된 Go 릴리스는 저용량 메일링 리스트 [golang-announce@googlegroups.com](https://groups.google.com/group/golang-announce)를 통해 사전 공지됩니다. Go 자체에 대한 보안 수정 사항이 언제 배포되는지 알고 싶으시다면 구독하시기 바랍니다.
