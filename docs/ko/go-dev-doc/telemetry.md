제공해주신 내용이 CSS 스타일 시트만 포함되어 있으며, 번역할 텍스트 콘텐츠가 없습니다. CSS 코드는 기술적인 식별자와 스타일 정의이므로 번역하지 않고 그대로 유지합니다.

```html
<style>
.DocInfo {
  background-color: var(--color-background-info);
  padding: 1.5rem 2rem 1.5rem 4rem;
  border-left: 0.875rem solid var(--color-border);
  position: relative;
}
.DocInfo:before {
  content: "ⓘ";
  position: absolute;
  top: 1rem;
  left: 1rem;
  font-size: 2rem;
}
</style>
```

목차:

[배경](#background)\
 [개요](#overview)\
 [설정](#config)\
 [카운터](#counters)\
 [보고 및 업로드](#reports)\
 [차트](#charts) \
 [텔레메트리 제안](#proposals)\
 [IDE 프롬프팅](#ide) \
 [자주 묻는 질문](#faq)

## 배경 {#background}

Go telemetry는 Go 툴체인 프로그램이 성능 및 사용량에 관한 데이터를 수집하기 위한 방법입니다. 여기서 "Go 툴체인"이란 `go` 명령어를 비롯하여 Go 언어 서버인 [`gopls`] 또는 Go 보안 도구인 [`govulncheck`]와 같은 보조 도구를 포함하여 Go 팀이 유지 관리하는 개발자 도구를 의미합니다. Go telemetry는 Go 팀이 유지 관리하는 프로그램과 [Delve]와 같이 선택된 종속성에서만 사용하도록 설계되었습니다.

기본적으로 텔레메트리 데이터는 로컬 컴퓨터에만 저장되지만, 사용자는 승인된 텔레메트리 데이터의 일부를 [telemetry.go.dev]로 업로드하는 것에 동의할 수 있습니다. 업로드된 데이터는 사용 방식과 오류 사례를 이해하는 데 도움을 주어, Go 팀이 Go 언어와 도구들을 개선하는 데 기여합니다.

"telemetry"라는 단어는 오픈 소스 소프트웨어 세계에서 부정적인 함의를 갖게 되었으며, 많은 경우 이는 당연한 결과였습니다. 하지만 사용자 경험을 측정하는 것은 현대 소프트웨어 공학의 중요한 요소이며, GitHub issue나 연례 설문조사와 같은 데이터 소스는 거칠고 뒤처지는 지표이기에 Go 팀이 답해야 하는 유형의 질문들에 대응하기에는 불충분합니다.

Go telemetry는 Go 프로젝트에 사용자가 기대하는 투명성과 개인정보 보호를 유지하면서, 툴체인의 프로그램들이 신뢰성, 성능 및 사용법에 관한 유용한 데이터를 수집할 수 있도록 설계되었습니다. telemetry의 설계 과정과 동기에 대해 더 자세히 알아보려면 [telemetry 블로그 포스트](https://research.swtch.com/telemetry)를 참조하십시오.

telemetry와 개인정보 보호에 대해 더 자세히 알아보려면 [telemetry 개인정보 보호정책](https://telemetry.go.dev/privacy)을 참조하십시오.

이 페이지는 Go 텔레메트리가 어떻게 작동하는지 상세히 설명합니다. 자주 묻는 질문에 대한 빠른 답변은 [FAQ](#faq)를 참조하십시오.

<div class="DocInfo">
Go 1.23 이상 버전에서 Go 팀으로 텔레메트리 데이터를 업로드하는 것에 <strong>동의(opt in)</strong>하려면 다음을 실행하세요:
<pre>
go telemetry on
</pre>
로컬 수집을 포함하여 텔레메트리를 완전히 비활성화하려면 다음을 실행하세요:
<pre>
go telemetry off
</pre>
로컬 전용 텔레메트리라는 기본 모드로 되돌리려면 다음을 실행하세요:
<pre>
go telemetry local
</pre>
Go 1.23 이전 버전에서는 <code>golang.org/x/telemetry/cmd/gotelemetry</code> 명령어로도 이를 수행할 수 있습니다. 자세한 내용은 <a
href="#config">Configuration</a>을 참조하세요.
</div>

## 개요 {#overview}

Go 텔레메트리는 세 가지 핵심 데이터 타입을 사용합니다:

- [_Counters_](#counters)는 툴체인 프로그램에 내장된 이름 지정 이벤트의 경량 카운트입니다. 수집이 활성화된 경우([mode](#config)가 **local** 또는 **on**), 카운터는 로컬 파일 시스템의 메모리 맵 파일(memory-mapped file)에 기록됩니다.
- [_Reports_](#reports)는 특정 주에 대한 카운터의 집계 요약입니다. 업로드가 활성화된 경우([mode](#config)가 **on**), [approved counters](#proposals)에 대한 리포트가 [telemetry.go.dev]로 업로드되며, 여기에서 공개적으로 접근할 수 있습니다.
- [_Charts_](#charts)는 모든 사용자에 대해 업로드된 리포트를 요약합니다. 차트는 [telemetry.go.dev]에서 확인할 수 있습니다.

모든 로컬 Go 텔레메트리 데이터와 설정은 다음 디렉토리에 저장됩니다:
`<code>[os.UserConfigDir()](/pkg/os#UserConfigDir)/go/telemetry</code>`
디렉토리. 아래에서는 이 디렉토리를 `<gotelemetry>`라고 부르겠습니다.

아래 다이어그램은 이러한 데이터 흐름을 보여줍니다.

<div class="image">
  <center>
    <img max-width="800px" src="/doc/telemetry/dataflow.png" />
  </center>
</div>

이 문서의 나머지 부분에서는 이 다이어그램의 구성 요소들에 대해 살펴보겠습니다. 하지만 그 전에, 이를 제어하는 설정에 대해 더 자세히 알아보겠습니다.

## 설정 {#config}

Go 텔레메트리의 동작은 단일 값인 telemetry _mode_에 의해 제어됩니다. `mode`에 설정 가능한 값은 `local`(기본값), `on`, 또는 `off`입니다.

- `mode`가 `local`일 때, 텔레메트리 데이터는 로컬 컴퓨터에 수집 및 저장되지만, 원격 서버로 업로드되지 않습니다.
- `mode`가 `on`일 때, 데이터가 수집되며 [sampling](#uploads) 설정에 따라 업로드될 수 있습니다.
- `mode`가 `off`일 때, 데이터는 수집되지도 업로드되지도 않습니다.

Go 1.23 버전 이후부터는 다음 명령어를 통해 텔레메트리(telemetry) 모드와 상호작용할 수 있습니다.

- `go telemetry`: 현재 모드를 확인합니다.
- `go telemetry on`: 모드를 `on`으로 설정합니다.
- `go telemetry off`: 모드를 `off`로 설정합니다.
- `go telemetry local`: 모드를 `local`로 설정합니다.

텔레메트리 설정에 관한 정보는 읽기 전용 Go 환경 변수를 통해서도 확인할 수 있습니다:

- `go env GOTELEMETRY`는 텔레메트리 모드를 보고합니다.
- `go env GOTELEMETRYDIR`은 텔레메트리 설정 및 데이터가 저장된 디렉토리를 보고합니다.

[`gotelemetry`](/pkg/golang.org/x/telemetry/cmd/gotelemetry) 명령어를 사용하여 텔레메트리 모드를 설정하거나 로컬 텔레메트리 데이터를 확인할 수 있습니다. 다음 명령어를 사용하여 설치하십시오.

```
go install golang.org/x/telemetry/cmd/gotelemetry@latest
```

`gotelemetry` 명령줄 도구의 전체 사용법에 대한 정보는 [패키지 문서](/pkg/golang.org/x/telemetry/cmd/gotelemetry)를 참조하세요.

## Counters {#counters}

앞서 언급했듯이, Go 텔레메트리는 _counters_를 통해 계측됩니다. Counter에는 두 가지 변형이 있습니다: 기본 카운터(basic counters)와 스택 카운터(stack counters)입니다.

### 기본 카운터

_기본 카운터(basic counter)_는 이름이 지정된 증가 가능한 값으로, 해당 이름은 카운트하는 이벤트를 설명합니다. 예를 들어, `gopls/client:vscode` 카운터는 VS Code에 의해 `gopls` 세션이 시작된 횟수를 기록합니다. 이 카운터와 함께 `gopls/client:neovim`, `gopls/client:eglot` 등을 두어 서로 다른 에디터나 언어 클라이언트와의 세션을 기록할 수 있습니다. 일주일 동안 여러 에디터를 사용했다면 다음과 같은 카운터 데이터를 기록하게 될 것입니다:

gopls/client:vscode 8
    gopls/client:neovim 5
    gopls/client:eglot  2

카운터들이 이러한 방식으로 연관되어 있을 때, 우리는 때때로 `:` 앞부분을 *차트 이름*(`gopls/client`), `:` 뒷부분을 *버킷 이름*(`vscode`)이라고 부릅니다. 이것이 왜 중요한지는 [차트](#charts)에 대해 논의할 때 살펴보겠습니다.

기본 카운터는 _히스토그램_을 표현하는 데에도 사용될 수 있습니다. 예를 들어, {{raw
`<code>gopls/completion/latency:&lt;50ms</code>`}} 카운터는 자동 완성이 50ms 미만으로 걸린 횟수를 기록합니다.

{{raw `
<pre>
gopls/completion/latency:&lt;10ms
gopls/completion/latency:&lt;50ms
gopls/completion/latency:&lt;100ms
...
</pre>
`}}

히스토그램 데이터를 기록하는 이 패턴은 관례입니다. `<code>&lt;50ms</code>` 버킷 이름에 특별한 의미가 있는 것은 아닙니다. 이러한 유형의 카운터는 일반적으로 성능 측정에 사용됩니다.

### 스택 카운터(Stack counters)

_스택 카운터(stack counter)_는 카운트가 증가할 때 Go 툴체인 프로그램의 현재 호출 스택(call stack)을 함께 기록하는 카운터입니다. 예를 들어, `crash/crash` 스택 카운터는 툴체인 프로그램이 충돌(crash)했을 때의 호출 스택을 기록합니다.

crash/crash
    golang.org/x/tools/gopls/internal/golang.hoverBuiltin:+22
    golang.org/x/tools/gopls/internal/golang.Hover:+94
    golang.org/x/tools/gopls/internal/server.Hover:+42
    ...

스택 카운터(Stack counters)는 일반적으로 프로그램 불변성(invariants)이 위반되는 이벤트를 측정합니다.
가장 흔한 예는 크래시(crash)이지만, 다른 예로는 `gopls/bug` 스택 카운터가 있습니다. 이는 복구된 패닉(recovered panic)이나 "발생할 수 없는" 에러와 같이 프로그래머가 사전에 식별한 특이 상황을 카운트합니다. 스택 카운터에는 Go 툴체인 프로그램 내 함수들의 이름과 라인 번호만 포함됩니다. 사용자 소스 코드의 이름이나 내용과 같은 사용자 입력에 관한 정보는 포함되지 않습니다.

스택 카운터(Stack counters)는 다른 수단으로는 보고되지 않는 드물거나 까다로운 버그를 추적하는 데 도움이 됩니다. `gopls/bug` 카운터를 도입한 이후, 실제로 실행된 [수십 건의](https://github.com/golang/go/issues?q=label%3Agopls%2Ftelemetry-wins) "도달 불가능한(unreachable)" 코드 사례를 발견했습니다. 이러한 예외 상황을 추적함으로써 사용자에게 명확히 드러나지 않았거나 보고하기 너무 어려웠던 많은 사용자 가시적 버그를 발견하고 수정할 수 있었습니다. 특히 프리릴리스 테스트 단계에서 스택 카운터는 자동화 없이는 불가능했을 방식으로 제품을 더 효율적으로 개선하는 데 도움을 줍니다.

### 카운터 파일 (Counter files)

모든 카운터 데이터는 `<gotelemetry>/local` 디렉토리에 작성되며, 파일 이름은 다음 스키마에 따라 지정됩니다:

```
[program name]@[program version]-[go version]-[GOOS]-[GOARCH]-[date].v1.count
```

- **프로그램 이름**은 [debug.BuildInfo]에서 보고하는 프로그램 패키지 경로의 basename입니다.
- **프로그램 버전**과 **go 버전** 또한 [debug.BuildInfo]에서 보고합니다.
- **GOOS** 및 **GOARCH** 값은 [`runtime.GOOS`](/pkg/runtime#GOOS)와 [`runtime.GOARCH`](/pkg/runtime#GOARCH)에서 보고합니다.
- **날짜**는 카운터 파일이 생성된 날짜이며, `YYYY-MM-DD` 형식입니다.

이 파일들은 계측된 프로그램의 각 실행 인스턴스에 메모리 맵핑(memory mapped)됩니다. 메모리 맵핑 파일을 사용하면 프로그램이 즉시 충돌하거나, 계측된 도구의 여러 복사본이 동시에 실행되더라도 카운터가 안전하게 기록됩니다.

## 리포팅 및 업로드 {#reports}

약 일주일에 한 번씩, 카운터 데이터가 `<gotelemetry>/local` 디렉토리의 `<date>.json`이라는 이름의 보고서로 집계됩니다. 이 보고서들은 카운터 파일에 사용된 것과 동일한 프로그램 식별자(프로그램 이름, 프로그램 버전, go 버전, GOOS 및 GOARCH)로 그룹화하여 지난 일주일 동안의 모든 카운트 합계를 계산합니다.

로컬 보고서는 [`gotelemetry view`](/pkg/golang.org/x/telemetry/cmd/gotelemetry) 명령어를 사용하여 차트로 볼 수 있습니다.
다음은 `gopls/completion/latency` 카운터의 요약 예시입니다:

<div class="image">
  <center>
    <img max-width="800px" src="/doc/telemetry/gopls-latency.png" />
  </center>
</div>

### 업로드하기 {#uploads}

텔레메트리 업로드가 활성화된 경우, 주간 보고 프로세스는 [upload config](https://telemetry.go.dev/config)에 포함된 카운터의 서브셋을 포함하는 보고서도 함께 생성합니다. 이러한 카운터는 다음 섹션에서 설명하는 공개 검토 프로세스를 통해 승인을 받아야 합니다. 성공적으로 업로드되면, 업로드된 보고서의 복사본이 `<gotelemetry>/upload` 디렉토리에 저장됩니다.

충분한 수의 사용자가 텔레메트리(telemetry) 데이터 업로드에 동의하면, 통계적 유의성을 유지하면서 수집량을 줄이고 개인정보 보호를 강화하기 위해 일부 보고서에 대해 업로드 프로세스가 무작위로 업로드를 건너뛰게 됩니다.

## 차트 {#charts}

[telemetry.go.dev] 웹사이트는 업로드를 받는 것 외에도, 업로드된 데이터를 공개적으로 제공합니다. 매일 업로드된 리포트가 두 가지 출력물로 처리되며, 이는 [telemetry.go.dev] 홈페이지에서 확인할 수 있습니다.

- _merged_는 해당 날짜에 수신된 모든 업로드로부터 병합된 카운터(counter)를 보고합니다.
- _charts_는 [chart config]에 지정된 대로 업로드된 데이터를 플롯합니다. 이 설정은 제안 프로세스의 일부로 생성되었습니다. [counters](#counters)에 대한 논의에서 기억하시듯, `foo:bar`와 같은 카운터 이름은 차트 이름 `foo`와 버킷 이름 `bar`로 분해됩니다. 각 차트는 동일한 차트 이름을 가진 카운터들을 해당 버킷으로 집계합니다.

차트는 [chartconfig] 패키지 형식으로 지정됩니다. 예를 들어, 다음은 `gopls/client` 차트의 차트 설정입니다.

title: 에디터 분포
    counter: gopls/client:{vscode,vscodium,vscode-insiders,code-server,eglot,govim,neovim,coc.nvim,sublimetext,other}
    description: gopls 사용자의 에디터 분포를 측정합니다.
    type: partition
    issue: https://go.dev/issue/61038
    issue: https://go.dev/issue/62214 # vscode-insiders 추가
    program: golang.org/x/tools/gopls
    version: v0.13.0 # 설정 생성을 시연하기 위해 일시적으로 이전 버전으로 되돌림.

이 설정은 생성될 차트를 설명하고, 집계할 카운터 세트를 나열하며, 차트가 적용되는 프로그램 버전을 지정합니다. 또한, [제안 프로세스](#proposals)에 따라 승인된 제안이 차트와 연결되어 있어야 합니다. 해당 설정으로 인해 생성된 차트는 다음과 같습니다:

<div class="image">
  <center>
    <img src="/doc/telemetry/gopls-clients.png" />
  </center>
</div>

## 텔레메트리 제안 프로세스 {#proposals}

[telemetry.go.dev]의 업로드 설정 또는 차트 세트의 변경 사항은 _telemetry 제안 프로세스(telemetry proposal process)_를 거쳐야 하며, 이는 텔레메트리 설정 변경에 대한 투명성을 보장하기 위함입니다.

특히, 이 과정에서는 업로드 설정(upload configuration)과 차트 설정(chart configuration) 사이에 실제적인 구분이 없습니다. 업로드 설정 자체는 telemetry.go.dev에 렌더링하고자 하는 집계(aggregation) 관점에서 표현됩니다. 이는 우리가 _보고 싶은_ 데이터만 수집해야 한다는 원칙에 기반합니다.

제안 프로세스는 다음과 같습니다:

1. 제안자는 `chartconfig` 패키지의 `config.txt`를 수정하여 원하는 새로운 카운터 집계(counter aggregations)를 포함하는 CL을 생성합니다.
2. 제안자는 이 CL을 병합하기 위한 [proposal]을 제출합니다.
3. 해당 이슈에 대한 논의가 완료되면, Go 팀의 구성원이 제안을 승인하거나 거절합니다.
4. 자동화된 프로세스가 업로드 설정을 다시 생성하여 새 차트에 필요한 카운터 업로드를 허용합니다. 이 프로세스는 관련 프로그램의 새 버전이 릴리스될 때마다 업로드 설정에 정기적으로 추가합니다.

승인받기 위해 새로운 차트는 민감한 사용자 정보를 포함해서는 안 되며, 추가적으로 유용성과 실현 가능성을 모두 갖춰야 합니다. 유용하기 위해서는 차트가 실행 가능한 결과와 함께 구체적인 목적을 제공해야 합니다. 실현 가능하기 위해서는 필요한 데이터를 안정적으로 수집할 수 있어야 하며, 결과 측정값이 통계적으로 유의미해야 합니다. 실현 가능성을 입증하기 위해, 제안자는 대상 프로그램에 counter를 삽입하여 먼저 로컬에서 데이터를 수집하도록 요청받을 수 있습니다.

이러한 제안서의 전체 세트는 GitHub의 [proposal project](https://github.com/orgs/golang/projects/29)에서 확인할 수 있습니다.

## IDE 프롬프팅 {#ide}

텔레메트리가 우리가 묻고자 하는 유형의 질문에 답하기 위해, 업로드를 선택(opt-in)하는 사용자 집단이 반드시 클 필요는 없습니다. 약 16,000명의 참여자만으로도 원하는 수준의 세분성에서 통계적으로 유의미한 측정이 가능할 것입니다. 하지만 이러한 유효한 샘플을 수집하는 데에는 여전히 비용이 따릅니다. 즉, 수많은 Go 개발자들에게 참여 의사를 물어봐야 한다는 점입니다.

게다가, 설령 많은 수의 사용자가 *지금* (아마도 Go 블로그 게시물을 읽은 후) 참여(opt in)하기로 선택하더라도, 해당 사용자들은 숙련된 Go 개발자 쪽으로 편향될 가능성이 있으며, 시간이 지남에 따라 그 초기 표본은 더욱 편향될 것입니다.
또한, 사용자가 컴퓨터를 교체할 때마다 다시 적극적으로 참여를 선택해야 합니다. 텔레메트리 블로그 게시물 시리즈에서는 이를 참여 모델의 ["캠페인 비용(campaign cost)"](https://research.swtch.com/telemetry-opt-in#campaign)이라고 부릅니다.

참여 사용자 샘플을 최신 상태로 유지하기 위해, Go 언어 서버 [`gopls`]는 사용자에게 Go 텔레메트리(telemetry) 참여 여부를 묻는 프롬프트를 지원합니다.
VS Code에서 어떻게 보이는지는 다음과 같습니다.

<div class="image">
  <center>
    <img width="600px" src="/doc/telemetry/prompt.png" />
  </center>
</div>

사용자가 "Yes"를 선택하면, [`gotelemetry on`](/pkg/golang.org/x/telemetry/cmd/gotelemetry) 명령어를 실행한 것과 동일하게 텔레메트리 [모드](#config)가 `on`으로 설정됩니다. 이러한 방식을 통해 사용자가 최대한 쉽게 참여할 수 있도록 하며, 우리는 지속적으로 광범위하고 계층화된 Go 개발자 샘플을 확보할 수 있습니다.

## 자주 묻는 질문 {#faq}

**Q: Go 텔레메트리(telemetry)를 어떻게 활성화하거나 비활성화하나요?**

A: `go install golang.org/x/telemetry/cmd/gotelemetry@latest`로 설치할 수 있는 `gotelemetry` 명령어를 사용하세요. 로컬 수집을 포함한 모든 기능을 비활성화하려면 `gotelemetry off`를 실행하세요. [telemetry.go.dev]로의 승인된 카운터 업로드를 포함한 모든 기능을 활성화하려면 `gotelemetry on`을 실행하세요. 자세한 내용은 [Configuration](#config) 섹션을 참조하세요.

**Q: 로컬 데이터는 어디에 저장되나요?**

A: `<code>[os.UserConfigDir()](/pkg/os#UserConfigDir)/go/telemetry</code>` 디렉토리에 있습니다.

**Q: 데이터 업로드에 동의할 경우, 데이터는 얼마나 자주 업로드되나요?**

A: 대략 일주일에 한 번 정도입니다.

**Q: 옵트인(opt in)을 선택하면 어떤 데이터가 업로드되나요?**

[upload config](https://telemetry.go.dev/config)에 나열된 카운터만 업로드할 수 있습니다. 
이는 더 읽기 쉬울 수 있는 [chart config]로부터 생성됩니다.

**Q: 카운터가 업로드 설정(upload config)에 어떻게 추가되나요?**

A: [공개 제안 프로세스](#proposals)를 통해 가능합니다.

**Q: 업로드된 텔레메트리 데이터를 어디에서 확인할 수 있나요?**

업로드된 데이터는 [telemetry.go.dev]에서 차트 또는 병합된 요약 형태로 확인할 수 있습니다.

**Q: Go 텔레메트리(telemetry)의 소스 코드는 어디에 있나요?**

A: [golang.org/x/telemetry](/pkg/golang.org/x/telemetry)에서 확인하세요.

[`gopls`]: /pkg/golang.org/x/tools/gopls
[`govulncheck`]: /pkg/golang.org/x/vuln/cmd/govulncheck
[Delve]: /pkg/github.com/go-delve/delve#section-readme
[debug.BuildInfo]: /pkg/runtime/debug#BuildInfo
[proposal]: /issue/new?assignees=&labels=Telemetry-Proposal&projects=golang%2F29&template=12-telemetry.yml&title=x%2Ftelemetry%2Fconfig%3A+proposal+title
[telemetry.go.dev]: https://telemetry.go.dev
[chartconfig]: /pkg/golang.org/x/telemetry/internal/chartconfig
[config.txt]: https://go.googlesource.com/telemetry/+/refs/heads/master/internal/chartconfig/config.txt
