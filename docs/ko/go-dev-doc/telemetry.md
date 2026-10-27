```markdown
<style>
.DocInfo {
  배경색: var(--color-background-info);
  패딩: 1.5rem 2rem 1.5rem 4rem;
  왼쪽 테두리: 0.875rem 고체 var(--color-border);
  위치: 상대적;
}
.DocInfo:before {
  콘텐츠: "ⓘ";
  위치: 절대적;
  상단: 1rem;
  왼쪽: 1rem;
  글꼴 크기: 2rem;
}
</style>
```

목차:

[배경](#background)\
 [개요](#overview)\
 [설정](#config)\
 [카운터](#counters)\
 [보고서 및 업로드](#reports)\
 [차트](#charts) \
 [제안](#proposals)\
 [IDE 프롬프트](#ide) \
 [자주 묻는 질문](#faq)

## 배경 {#background}

Go 텔러메트리는 Go 도구 체인 프로그램이 성능 및 사용에 대한 데이터를 수집하는 방법입니다. 여기서 "Go 도구 체인"은 Go 팀에서 유지 관리하는 개발 도구를 의미하며, 여기에는 `go` 명령과 `gopls` (Go 언어 서버) 또는 `govulncheck` (Go 보안 도구)와 같은 보조 도구가 포함됩니다. Go 텔러메트리는 Go 팀 및 선택된 의존체 (예: [Delve])에 의해 유지 관리되는 프로그램에서만 사용하도록 설계되었습니다.

기본적으로, 텔레메트리 데이터는 로컬 컴퓨터에만 저장되지만, 사용자는 [telemetry.go.dev]로 승인된 텔레메트리 데이터의 일부를 업로드하도록 선택할 수 있습니다.
업로드된 데이터는 Go 팀이 Go 언어와 도구를 개선하는 데 도움이 되며, 사용량 및 오류를 파악하는 데 활용됩니다.

단어 "Telemetry"는 오픈 소스 소프트웨어 분야에서 부정적인 의미를 갖게 되었으며, 이는 상당 부분 정당화될 수 있습니다. 하지만 사용자 경험을 측정하는 것은 현대적인 소프트웨어 엔지니어링의 중요한 요소이며, GitHub 이슈나 연례 설문조사와 같은 데이터 소스는 거친 정보이며, 지연된 지표로서, Go 팀이 답변해야 하는 질문에 충분하지 않습니다.

Go telemetry는 프로그램이 자체의 신뢰성, 성능 및 사용에 대한 유용한 데이터를 수집하는 데 도움이 되도록 설계되었으며, 동시에 사용자가 Go 프로젝트에서 기대하는 투명성과 개인 정보를 유지합니다. telemetry의 설계 과정 및 동기에 대해 자세히 알아보려면 [telemetry 블로그 게시물](https://research.swtch.com/telemetry)을 참조하십시오.

telemetry 및 개인 정보에 대해 자세히 알아보려면 [telemetry 개인 정보 보호 정책](https://telemetry.go.dev/privacy)을 참조하십시오.

이 페이지는 Go 기반의 전력 측정 시스템이 어떻게 작동하는지에 대해 자세히 설명합니다. 자주 묻는 질문에 대한 빠른 답변을 원하시면 [자주 묻는 질문](#faq)를 참조하세요.

```markdown
<div class="DocInfo">
Go 1.23 또는 이후 버전을 사용하여, Go 팀으로 <strong>텔레메트리 데이터 업로드 활성화</strong>하려면 다음 명령어를 실행합니다.
<pre>
go telemetry on
</pre>
로컬 수집을 포함하여 모든 텔레메트리 수집을 완전히 비활성화하려면 다음 명령어를 실행합니다.
<pre>
go telemetry off
</pre>
로컬 전용 텔레메트리 모드로 되돌리려면 다음 명령어를 실행합니다.
<pre>
go telemetry local
</pre>
Go 1.23 이전 버전에서는 다음 명령어를 사용하여
<code go="text"><a href="https://golang.org/x/telemetry/cmd/gotelemetry">golang.org/x/telemetry/cmd/gotelemetry</a></code>
</code go="text">
를 실행할 수 있습니다. 자세한 내용은 <a href="#config">Configuration</a>을 참조하십시오.
</div>
```

## 개요 {#overview}

Go telemetry는 세 가지 핵심 데이터 유형을 사용합니다:

- [_카운터_](#counters)는 이름이 지정된 이벤트의 가벼운 카운트이며, 툴체인 프로그램에서 측정됩니다. 수집이 활성화되어 있으면 (설정 모드가 **local** 또는 **on**인 경우), 카운터는 로컬 파일 시스템의 메모리 매핑된 파일에 기록됩니다.
- [_보고서_](#reports)는 주어진 주에 대한 카운터의 집계된 요약입니다. 업로드가 활성화되어 있으면 (설정 모드가 **on**인 경우), [승인된 카운터](#proposals)에 대한 보고서가 [telemetry.go.dev]로 업로드되며, 여기에서 공개적으로 접근할 수 있습니다.
- [_차트_](#charts)는 모든 사용자의 업로드된 보고서를 요약합니다. 차트는 [telemetry.go.dev]에서 볼 수 있습니다.

모든 로컬 Go 텔레메트리 데이터 및 구성은 다음 디렉토리에 저장됩니다.
<code>[os.UserConfigDir()](/pkg/os#UserConfigDir)/go/telemetry</code>
디렉토리입니다. 아래에서는 이 디렉토리를 `<gotelemetry>`라고 참조합니다.

아래 다이어그램은 이러한 데이터 흐름을 보여줍니다.

```markdown
<div class="image">
  <center>
    <img max-width="800px" src="/doc/telemetry/dataflow.png" />
  </center>
</div>
```

이 문서의 나머지 부분에서는 이 다이어그램의 구성 요소를 살펴보겠습니다. 하지만
먼저, 이 구성 요소를 제어하는 구성에 대해 자세히 알아보겠습니다.

## 설정 {#config}

Go 텔레메트리의 동작은 단 하나의 값인 `mode`에 의해 제어됩니다. `mode`에 사용할 수 있는 값은 `local` (기본값), `on`, 또는 `off`입니다:

- `mode`가 `local`일 때, 텔레메트리 데이터는 로컬 컴퓨터에서 수집 및 저장되지만, 원격 서버로 업로드되지 않습니다.
- `mode`가 `on`일 때, 데이터가 수집되고, [샘플링](#uploads)에 따라 업로드될 수 있습니다.
- `mode`가 `off`일 때, 데이터는 수집되거나 업로드되지 않습니다.

Go 1.23 또는 이후 버전에서는 다음 명령이 텔레메트리 모드와 상호 작용합니다:

- `go telemetry`: 현재 모드를 확인합니다.
- `go telemetry on`: 모드를 `on`으로 설정합니다.
- `go telemetry off`: 모드를 `off`으로 설정합니다.
- `go telemetry local`: 모드를 `local`로 설정합니다.

텔레메트리 구성에 대한 정보는 다음과 같은 읽기 전용 Go 환경 변수를 통해 확인할 수 있습니다:

- `go env GOTELEMETRY`는 텔레메트리 모드를 보고합니다.
- `go env GOTELEMETRYDIR`는 텔레메트리 구성 및 데이터를 저장하는 디렉토리를 보고합니다.

명령 [`gotelemetry`](/pkg/golang.org/x/telemetry/cmd/gotelemetry)는 또한 텔레메트리 모드를 구성하는 데 사용할 수 있으며, 로컬 텔레메트리 데이터를 검사하는 데도 사용할 수 있습니다. 다음 명령어를 사용하여 설치하십시오:

```
go install golang.org/x/telemetry/cmd/gotelemetry@최신
```

`gotelemetry` 명령줄 도구의 전체 사용 정보는 다음 [패키지 설명서]( /pkg/golang.org/x/telemetry/cmd/gotelemetry)를 참조하십시오.

## 카운터 란 무엇인가? {#counters}

위에서 언급했듯이, Go 텔레메트리는 _카운터_를 통해 측정됩니다. 카운터는 다음과 같은 두 가지 유형으로 제공됩니다: 기본 카운터 및 스택 카운터.

### 기본 카운터

기본적인 _카운터_는 이름을 통해 설명되는 증가 가능한 값입니다. 예를 들어, `gopls/client:vscode` 카운터는 VS Code에서 시작된 `gopls` 세션의 횟수를 기록합니다. 이 카운터와 함께 `gopls/client:neovim`, `gopls/client:eglot` 등을 사용하여 다양한 편집기 또는 언어 클라이언트에 대한 세션을 기록할 수 있습니다. 만약 일주일 동안 여러 편집기를 사용했다면, 다음과 같은 카운터 데이터를 기록할 수 있습니다:

gopls/클라이언트: vscode 8
    gopls/클라이언트: neovim 5
    gopls/클라이언트: eglot 2

때문에 카운터들이 이런 식으로 관련되어 있을 때, 콜론(:) 앞부분인 _차트 이름_ (이 경우에는 `gopls/client`)과 콜론(:) 뒤부분인 _버킷 이름_ (이 경우에는 `vscode`)을 참조하는 경우가 있습니다. `charts`를 다루면서 왜 이것이 중요한지 알게 될 것입니다.

기본 카운터는 히스토그램을 나타낼 수도 있습니다. 예를 들어, {{raw
`<code>gopls/completion/latency:&lt;50ms</code>`}} 카운터는 자동 완성 시간이 50ms 미만인 횟수를 기록합니다.

```
gopls/완성도 지연 시간: &lt;10ms
gopls/완성도 지연 시간: &lt;50ms
gopls/완성도 지연 시간: &lt;100ms
...
```

이 히스토그램 데이터 기록 패턴은 관례입니다: {{raw `<code>&lt;50ms</code>`}}라는 래더 이름 자체에 특별한 의미는 없습니다. 이러한 카운터는 성능을 측정하는 데 일반적으로 사용됩니다.

### 스택 카운터

`_스택 카운터_는, 카운트가 증가될 때 현재 Go 툴체인 프로그램의 호출 스택을 기록하는 카운터입니다. 예를 들어, `crash/crash` 스택 카운터는 툴체인 프로그램이 충돌할 때 호출 스택을 기록합니다:

crash/crash
    golang.org/x/tools/gopls/internal/golang.hoverBuiltin:+22
    golang.org/x/tools/gopls/internal/golang.Hover:+94
    golang.org/x/tools/gopls/internal/server.Hover:+42
    ...

스택 카운터는 일반적으로 프로그램의 일관성이 위반되는 이벤트를 측정합니다.
가장 흔한 예는 충돌이지만, 또 다른 예는 `gopls/bug` 스택 카운터로, 프로그래머가 미리 파악한 비정상적인 상황을 셉니다. 예를 들어 복구된 패닉이나 "발생할 수 없는" 오류 등이 있습니다. 스택 카운터는 Go 툴체인 프로그램 내의 함수 이름과 라인 번호만 포함합니다. 사용자의 입력에 대한 정보, 예를 들어 사용자의 소스 코드의 이름이나 내용은 포함하지 않습니다.

스택 카운터는 다른 방법으로는 발견하기 어려운 희귀하거나 까다로운 버그를 추적하는 데 도움이 될 수 있습니다. `gopls/bug` 카운터를 도입한 이후, 실제로 실행되는 "접근 불가능한" 코드의 수십 건을 찾아냈으며, 이러한 예외를 추적하는 과정에서 사용자가 알아보기 어렵거나 보고하기 어려운 많은 버그를 발견하고 수정할 수 있었습니다. 특히 프리릴리즈 테스트의 경우, 스택 카운터는 자동화 없이도 제품 개선을 보다 효율적으로 할 수 있도록 도와줍니다.

### 카운터 파일

모든 카운터 데이터는 `<gotelemetry>/local` 디렉토리에 저장되며, 다음 스키마에 따라 이름이 지정된 파일에 저장됩니다:

```
[프로그램 이름]@[프로그램 버전]-[Go 버전]-[GOOS]-[GOARCH]-[날짜].v1.count
```

- **프로그램 이름**은 프로그램의 패키지 경로의 기본 이름으로, [debug.BuildInfo]에서 보고된 값입니다.
- **프로그램 버전** 및 **go 버전** 또한 [debug.BuildInfo]에서 보고됩니다.
- **GOOS** 및 **GOARCH** 값은 [`runtime.GOOS`](/pkg/runtime#GOOS) 및 [`runtime.GOARCH`](/pkg/runtime#GOARCH)에서 보고됩니다.
- **날짜**는 카운터 파일이 생성된 날짜이며, `YYYY-MM-DD` 형식으로 표시됩니다.

이 파일들은 각 실행 중인 프로그래밍된 프로그램의 메모리에 매핑됩니다. 메모리에 매핑된 파일을 사용하는 것은 프로그램이 즉시 중단되거나 여러 개의 프로그래밍된 도구가 동시에 실행되는 경우에도 카운터가 안전하게 기록되도록 합니다.

## 보고서 작성 및 업로드 {#보고서}

이 섹션에서는 보고서 작성 및 업로드 방법에 대해 설명합니다.

약 1주에 한 번, 카운터 데이터가 `<date>.json`이라는 이름으로 `<gotelemetry>/local` 디렉터리에 보고서로 집계됩니다. 이러한 보고서는 이전 주의 모든 카운터를, 카운터 파일에 사용된 동일한 프로그램 식별자를 기준으로 그룹화하여 합산합니다 (프로그램 이름, 프로그램 버전, Go 버전, GOOS, GOARCH).

로컬 보고서를 차트 형태로 볼 수 있습니다.
`gotelemetry view` 명령을 사용합니다.
다음은 `gopls/completion/latency` 카운터의 예시 요약입니다:

```markdown
<div class="image">
  <center>
    <img max-width="800px" src="/doc/telemetry/gopls-latency.png" />
  </center>
</div>
```

### 업로드하기 {#uploads}

만약 텔레메트리 업로드가 활성화되어 있다면, 주간 보고 프로세스는 또한 [업로드 설정](https://telemetry.go.dev/config)에 포함된 카운터의 하위 집합을 포함하는 보고서를 생성합니다. 이러한 카운터는 다음 섹션에 설명된 공개 검토 프로세스를 통해 승인되어야 합니다. 성공적으로 업로드되면, 업로드된 보고서의 복사본이 `<gotelemetry>/upload` 디렉토리에 저장됩니다.

충분한 사용자가 텔레메트리 데이터를 업로드하도록 동의하면, 업로드 프로세스는 보고서의 일부를 무작위로 업로드하지 않도록 하여, 데이터 수집량을 줄이고 개인 정보 보호를 유지하면서 통계적 유의성을 유지합니다.

## 차트 {#charts}

뿐만 아니라 업로드 기능을 지원하는 [telemetry.go.dev] 웹사이트는 업로드된
데이터를 공개적으로 사용할 수 있도록 합니다. 매일 업로드된 보고서는 두 가지 형태로
처리되어 [telemetry.go.dev] 홈페이지에서 확인할 수 있습니다.

- _병합된_ 보고서에는 주어진 날짜에 수신된 모든 업로드의 카운터 값을 병합했습니다.
- _차트_는 [차트 구성]에 명시된 업로드된 데이터를 표시합니다. 이 구성은 제안 프로세스의 일부로 생성되었습니다. [카운터](#counters)에 대한 논의에서 알 수 있듯이, `foo:bar`와 같은 카운터 이름은 차트 이름 `foo`와 바구니 이름 `bar`로 분해됩니다. 각 차트는 동일한 차트 이름을 가진 카운터를 해당 바구니로 집계합니다.

차트는 `chartconfig` 패키지의 형식을 사용하여 정의됩니다. 예를 들어, `gopls/client` 차트의 차트 구성은 다음과 같습니다.

제목: 에디터 배포
    카운터: gopls/클라이언트:{vscode, vscodium, vscode-insiders, code-server, eglot, govim, neovim, coc.nvim, sublime text, 기타}
    설명: gopls 사용자를 위한 에디터 배포 측정.
    유형: 파티션
    문제: https://go.dev/issue/61038
    문제: https://go.dev/issue/62214 # vscode-insiders 추가
    프로그램: golang.org/x/tools/gopls
    버전: v0.13.0 # 임시로 설정 생성 시연을 위해 버전 되돌림.

이 구성은 생성될 차트, 집계할 카운터 집합, 그리고 해당 차트가 적용되는 프로그램 버전을 설명합니다. 또한, [제안 프로세스](#proposals)는 수락된 제안이 차트와 연결되어 있어야 합니다. 다음은 해당 구성에서 생성된 차트입니다:

```markdown
<div class="image">
  <center>
    <img src="/doc/telemetry/gopls-clients.png" />
  </center>
</div>
```

## 텔레메트리 제안 프로세스 {#proposals}

[telemetry.go.dev]에서 업로드 구성 또는 차트 세트에 대한 변경 사항은 `_telemetry proposal process_`를 통해 진행해야 합니다. 이는 텔레메트리 구성 변경에 대한 투명성을 보장하기 위한 것입니다.

특히, 이 프로세스에서 업로드 구성과 차트 구성 간에 실제로 차이가 없습니다. 업로드 구성은 telemetry.go.dev에서 표시하고자 하는 집계에 따라 정의되며, "우리가 보고 싶은 데이터만 수집해야 한다"는 원칙에 기반합니다.

제안 절차는 다음과 같습니다:

1. 제안자는 [config.txt] 파일을 [chartconfig] 패키지를 수정하여 원하는 새로운 카운터 집계를 포함하도록 변경합니다.
2. 제안자는 이 변경 사항을 병합하기 위한 [proposal]를 제출합니다.
3. 논의가 완료되면, Go 팀의 구성원이 제안을 승인하거나 거부합니다.
4. 자동화된 프로세스가 업로드 설정을 재생성하여 새로운 차트에 필요한 카운터를 업로드할 수 있도록 합니다. 이 프로세스는 관련 프로그램의 새로운 버전을 업로드 설정에 주기적으로 추가합니다.

새로운 차트는 민감한 사용자 정보를 포함할 수 없으며, 또한 유용하고 실현 가능해야 합니다. 유용하려면, 차트는 특정 목적을 달성하고 실행 가능한 결과를 가져야 합니다. 실현 가능하려면, 필요한 데이터를 안정적으로 수집할 수 있어야 하며, 결과로 얻은 측정값은 통계적으로 유의미해야 합니다. 실현 가능성을 입증하기 위해, 제안자는 대상 프로그램을 카운터로 장비하고 먼저 현장에서 수집하도록 요청할 수 있습니다.

전체 제안 목록은 GitHub의 [프로젝트](https://github.com/orgs/golang/projects/29) 페이지에서 확인할 수 있습니다.

## IDE를 통한 제안 {#ide}

Telemetry가 우리가 질문하고자 하는 종류의 질문에 답변할 수 있도록, 업로드를 선택하는 사용자의 수는 크게 필요하지 않습니다. 약 16,000명의 참가자가 원하는 수준의 상세 정보에 대한 통계적으로 유의미한 측정을 가능하게 합니다. 그러나 이러한 건강한 샘플을 구성하는 데는 여전히 비용이 발생합니다: 우리는 많은 수의 Go 개발자에게 이메일로 문의하여 참여를 요청해야 합니다.

또한, 만약 많은 사용자가 현재 _즉시_ 참여를 선택한다면 (예를 들어, Go 블로그 게시물을 읽은 후), 이러한 사용자는 주로 숙련된 Go 개발자로 구성될 수 있으며, 시간이 지남에 따라 초기 샘플은 더욱 편향될 것입니다.

또한, 사람들이 컴퓨터를 교체할 때, 그들은 다시 참여를 _적극적으로_ 선택해야 합니다. "Telemetry" 블로그 게시물 시리즈에서는, 이러한 현상을 "캠페인 비용"(https://research.swtch.com/telemetry-opt-in#campaign)이라고 합니다.

참가 사용자 샘플을 최신 상태로 유지하는 데 도움이 되도록, Go 언어 서버
[`gopls`]는 사용자가 Go 텔레메트리에 참여하도록 요청하는 프롬프트를 지원합니다.
VS Code에서 이것은 다음과 같이 표시됩니다:

<div class="image">
  <center>
    <img width="600px" src="/doc/telemetry/prompt.png" />
  </center>
</div>

만약 사용자가 "예"를 선택하면, 그들의 텔레메트리 [모드](#config)는 `on`으로 설정됩니다. 이는 `gotelemetry on`을 실행한 것과 동일합니다 ((`/pkg/golang.org/x/telemetry/cmd/gotelemetry`) ). 이렇게 하면, 참여는 최대한 간단하며, 우리는 지속적으로 Go 개발자들의 대규모 및 다양한 그룹을 확보할 수 있습니다.

## 자주 묻는 질문 {#faq}

**Q: Go 프로그래밍의 통계를 활성화 또는 비활성화하는 방법은 무엇입니까?**

A: `gotelemetry` 명령어를 사용합니다. `go install golang.org/x/telemetry/cmd/gotelemetry@latest`를 사용하여 설치할 수 있습니다. 로컬 수집을 포함하여 모든 것을 비활성화하려면 `gotelemetry off`를 실행합니다. 승인된 카운터를 [telemetry.go.dev]로 업로드하는 등 모든 기능을 활성화하려면 `gotelemetry on`을 실행합니다. 자세한 내용은 [Configuration](#config) 섹션을 참조하십시오.

**Q: 로컬 데이터는 어디에 저장됩니까?**

A: `<code>[os.UserConfigDir()](/pkg/os#UserConfigDir)/go/telemetry</code> 디렉토리 내에.

**Q: 데이터 업로드 빈도는 어떻게 되나요? (선택 시)**

A: 대략 일주일에 한 번.

**Q: 어떤 데이터가 업로드되나요? (선택 시)**

A: 목록에 나열된 카운터만 업로드할 수 있습니다.
[업로드 설정](https://telemetry.go.dev/config)에서 확인할 수 있습니다.
이 정보는 [차트 설정]에서 생성되며, 더 읽기 쉬울 수 있습니다.

**Q: 업로드 설정에 카운터는 어떻게 추가되나요?**

A: 공개 제안 프로세스를 통해: [제안](#proposals)

**Q: 업로드된 텔레메트리 데이터를 어디에서 확인할 수 있나요?**

A: 업로드된 데이터는 차트 또는 병합된 요약 형태로 [telemetry.go.dev]에서 확인 가능합니다.

**Q: Go 기반의 텔레메트리 시스템의 소스 코드는 어디에 있습니까?**

A: [golang.org/x/telemetry](https://golang.org/x/telemetry)에서.

[`gopls`]: /pkg/golang.org/x/tools/gopls
[`govulncheck`]: /pkg/golang.org/x/vuln/cmd/govulncheck
[Delve]: /pkg/github.com/go-delve/delve#section-readme
[debug.BuildInfo]: /pkg/runtime/debug#BuildInfo
[proposal]: /issue/new?assignees=&labels=Telemetry-Proposal&projects=golang%2F29&template=12-telemetry.yml&title=x%2Ftelemetry%2Fconfig%3A+proposal+title
[telemetry.go.dev]: https://telemetry.go.dev
[chartconfig]: /pkg/golang.org/x/telemetry/internal/chartconfig
[config.txt]: https://go.googlesource.com/telemetry/+/refs/heads/master/internal/chartconfig/config.txt
