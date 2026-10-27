## 개요

이 문서는 보고된 이슈를 처리하는 Go 보안 팀의 프로세스와 그에 따라 기대할 수 있는 사항에 대해 설명합니다.

## 보안 버그 보고하기

Go 배포판의 모든 보안 버그는 이메일 [security@golang.org](mailto:security@golang.org)로 보고해야 합니다. 이 메일은 Go 보안 팀으로 전달됩니다.

이메일 제목을 "Vulnerability: {package name}: {one-line summary}" 형식으로 작성해 주시고, 메시지가 스팸으로 처리되는 것을 방지하기 위해 꼭 필요한 경우가 아니면 **첨부 파일을 보내지 마십시오.** 또한, **이메일 한 통당 하나의 보고서만** 보내 주시기 바랍니다.

원하신다면 보고서의 일부로 선호하시는 기여 표시(attribution)를 포함해 주세요.
CVE가 발행될 경우, 이 기여 표시가 CVE에 추가됩니다.

보고서는 간결하게 작성해 주시기 바랍니다. 발견하신 문제에 대한 설명, 해당 문제가 어떻게 악용될 수 있다고 생각하시는지에 대한 내용, 그리고 해당 문제를 증명할 수 있는 간단한 재현 테스트 케이스나 프로그램을 포함해 주세요.

자주 보고되는 문제 카테고리에 대한 [결정 사항 목록](/doc/security/decisions)이 있습니다.

귀하의 이메일은 7일 이내에 접수 확인될 예정입니다. 그때까지 답변을 받지 못하신 경우, [security@golang.org](mailto:security@golang.org)로 Go Security 팀에 다시 문의해 주시기 바랍니다. 이메일에 **vulnerability**라는 단어가 포함되어 있는지 확인해 주세요.

3일이 더 지났음에도 리포트에 대한 확인 답장을 받지 못하셨다면, 귀하의 이메일이 스팸으로 분류되었을 가능성이 있습니다. 이 경우, [여기에서 이슈를 제기해 주세요](https://g.co/vulnz). _"I want to report a technical security or an abuse risk related bug in a Google product (SQLi, XSS, etc.)"_를 선택하시고, 영향받는 제품으로 _"Go"_를 기재해 주시기 바랍니다.

귀하의 이슈는 저희의 최초 확인 후 90일 이내에 해결되거나 공개될 것입니다.

보안 문제를 보고하는 이메일은 수정 상태를 추적하고 발견자를 정확하게 식별하기 위해 무기한으로 보관됩니다.

### LLM 생성 보고서

적절한 검토(curation) 없이 LLM이 생성한 보고서를 전송하지 마십시오.

현대적인 LLM은 실제적이고 중요한 보안 버그를 찾는 데 매우 능숙합니다.
불행히도, LLM은 가상의 문제나 [보안 버그가 아닌](/doc/security/decisions#non-vuln) 실제 문제를 찾는 것에도 매우 능숙합니다. LLM의 출력은 종종 장황하며, 중요한 정보를 무관한 텍스트 속에 묻어버리거나, 과장되고 근거 없는 주장을 포함하곤 합니다.

LLM이 생성한 보고서의 가치는 큐레이션(curation)에 있습니다. 수십 가지의 잠재적 보안 문제를 보내면서 그 속에 숨겨진 단 하나의 유의미한 결과를 저희가 직접 찾게 하는 것은, 저희에게 큐레이션 작업을 요구하는 것이며 궁극적으로 Go를 안전하게 만들려는 저희의 목표를 방해하는 일입니다. 이러한 이유로, 저희는 실제 발견 비율이 상당한 수준인 제보자에게만 발견 공로를 인정합니다.

엄격하고 고정된 규칙은 없으나, 일반적인 가이드라인으로서 보고하신 내용의 대부분이 보안 이슈로 지정되지 않고, 유용한 큐레이션(curation)을 제공하고 있지 않다고 판단될 경우, 나머지 발견 사항에 대해서는 크레딧을 제공하지 않습니다. "대부분"에 대한 구체적인 기준이나 "큐레이션"이 무엇을 수반하는지에 대해 의도적으로 정의하지 않았습니다. 하지만 저희의 의도는 의미 있는 가치를 제공하는 선의의 보고자에게는 항상 크레딧을 제공하되, LLM의 출력물을 무분별하게 대량으로 전달하는 보고자에게는 제공하지 않는 것입니다.

## 트랙 (Tracks)

문제의 성격에 따라 Go 보안 팀은 해당 이슈를 PUBLIC, PRIVATE 또는 URGENT 트랙으로 분류합니다. 모든 보안 이슈에는 CVE 번호가 부여됩니다.

Go 보안 팀은 보안 문제에 대해 전통적인 세분화된 심각도 라벨(예: CRITICAL, HIGH, MEDIUM, LOW)을 부여하지 않습니다. 이는 심각도가 사용자가 영향을 받는 API나 기능을 어떻게 사용하고 있는지에 따라 크게 달라지기 때문입니다. 또한, Go 보안 문제에 대해 CVE를 발행할 때 CVSS 점수를 부여하지 않는데, 이는 동일한 이유로 해당 점수 산정 시스템이 Go에 적용 가능하다는 점에 근본적으로 동의하지 않기 때문입니다. MITRE나 NIST와 같은 제3자가 NVD를 통해 당사의 취약점에 CVSS 점수를 부여할 수 있으나, 당사는 이러한 점수가 해당 영향력을 정확하게 반영한다고 보증하지 않습니다.

예를 들어, `encoding/json` 파서의 리소스 고갈 문제로 인한 영향은 무엇을 파싱하느냐에 따라 달라집니다. 사용자가 로컬 파일 시스템에서 신뢰할 수 있는 JSON 파일을 파싱하는 경우, 영향은 낮을 가능성이 큽니다. 반면, 사용자가 HTTP 요청 본문에서 신뢰할 수 없는 임의의 JSON을 파싱하는 경우, 영향은 훨씬 더 클 수 있습니다.

그럼에도 불구하고, 다음과 같은 이슈 트랙은 보안 팀이 해당 이슈의 심각성과 영향 범위를 어떻게 판단하는지를 나타냅니다. 예를 들어, 많은 사용자에게 중간 정도에서 상당한 영향을 미치는 이슈는 이 정책에서 PRIVATE 트랙 이슈로 분류되며, 영향이 무시할 수 있거나 경미한 이슈, 또는 소수의 사용자에게만 영향을 미치는 이슈는 PUBLIC 트랙 이슈로 분류됩니다.

### 공개 (PUBLIC)

PUBLIC 트랙의 이슈들은 니치(niche)한 설정에 영향을 미치거나, 영향력이 매우 제한적이거나, 또는 이미 널리 알려진 것들입니다.

PUBLIC 트랙 이슈는 [`Proposal-Security`](https://github.com/golang/go/labels/Proposal-Security) 라벨이 지정되며, [Go 제안 검토 프로세스](https://go.googlesource.com/proposal/+/master/README.md#proposal-review)를 통해 논의되어 **공개적으로 수정(fixed in public)**된 후, 다음 예정된 [마이너 릴리스](/wiki/MinorReleases)(약 매월 발생)에 백포트됩니다. 릴리스 공지에는 이러한 이슈에 대한 세부 사항이 포함되지만, 사전 공지는 제공되지 않습니다.

과거 PUBLIC 이슈의 예시는 다음과 같습니다:

- [#44916](/issue/44916): archive/zip: Reader.Open 호출 시 패닉이 발생할 수 있음
- [#44913](/issue/44913): encoding/xml: 커스텀 TokenReader와 함께 xml.NewTokenDecoder를 사용할 때 무한 루프 발생
- [#43786](/issue/43786): crypto/elliptic: P-224 곡선에서 잘못된 연산 수행
- [#40928](/issue/40928): net/http/cgi,net/http/fcgi: Content-Type이 지정되지 않았을 때 교차 사이트 스크립팅(XSS) 취약점 발생
- [#40618](/issue/40618): encoding/binary: ReadUvarint 및 ReadVarint가 잘못된 입력으로부터 무제한의 바이트를 읽을 수 있음
- [#36834](/issue/36834): crypto/x509: Windows 10에서 인증서 검증 우회 가능

### 비공개(PRIVATE)

PRIVATE 트랙의 이슈는 약속된 보안 속성(committed security properties)을 위반하는 사항들입니다.

PRIVATE 트랙 이슈는 **다음 예정된 [minor releases](/wiki/MinorReleases)에서 수정**되며, 그때까지 비공개로 유지됩니다.

릴리스 3~7일 전에 golang-announce에 사전 공지가 전송됩니다. 이 공지에는 다가오는 릴리스에 하나 이상의 보안 수정 사항이 포함되어 있다는 점과, 해당 이슈가 표준 라이브러리, 툴체인 또는 둘 다에 영향을 미치는지 여부, 그리고 각 수정 사항에 예약된 CVE ID가 포함됩니다.

[주 버전 릴리스 후보](/s/release)에 존재하는 이슈의 경우, 다음 예정된 릴리스 후보에 수정 사항을 포함하는 동일한 프로세스를 따릅니다.

과거 PRIVATE 이슈의 몇 가지 예시는 다음과 같습니다:

- [#53416](/issue/53416): path/filepath: Glob에서 스택 소진(stack exhaustion) 발생
- [#53616](/issue/53616): go/parser: 모든 Parse* 함수에서 스택 소진(stack exhaustion) 발생
- [#54658](/issue/54658): net/http: GOAWAY 전송 후 서버 오류 처리
- [#56284](/issue/56284): syscall, os/exec: 환경 변수 내 정제되지 않은 NUL 문자 처리

### 긴급

URGENT 트랙 이슈는 Go 생태계의 무결성에 위협이 되거나, 실제로 활발하게 악용되어 심각한 피해를 초래하는 문제입니다. 한 가지 예로 [Go 1.27.3 및 Go 1.26.10 릴리스](https://groups.google.com/g/golang-announce/c/66pojueaQek)가 있습니다. 그 외에도 `net/http`에서의 원격 코드 실행(RCE)이나 `crypto/tls`에서의 실질적인 키 복구 등이 포함될 수 있습니다.

긴급한 track 문제는 비공개로 수정되며, 사전 공지 없이 **즉각적인 전용 보안 릴리스를 트리거**할 수 있습니다.

## 기존 이슈를 보안 관련으로 표시하기

[기존 이슈](/issue)가 보안과 관련이 있다고 생각하신다면, [security@golang.org](mailto:security@golang.org)로 이메일을 보내주시기 바랍니다. 이메일에는 이슈 ID와 해당 이슈를 왜 이 보안 정책에 따라 처리해야 하는지에 대한 짧은 설명을 포함해야 합니다.

## 공개 프로세스

Go 프로젝트는 다음과 같은 공개 프로세스를 사용합니다:

1. 보안 보고서가 접수되면 기본 처리 담당자(primary handler)가 지정됩니다. 이 담당자는 수정 및 릴리스 프로세스를 조정합니다.

2. 이슈가 확인되었으며 영향받는 소프트웨어 목록이 결정되었습니다.

3. 유사한 잠재적 문제가 있는지 확인하기 위해 코드를 감사(audit)합니다.

4. 제출자와의 협의를 통해 CVE 번호가 필요하다고 판단되면, 기본 담당자(primary handler)가 이를 발급받습니다.

5. 최근 두 개의 메이저 릴리스와 head/master 리비전에 대해 수정 사항이 준비됩니다. 수정 사항은 최근 두 개의 메이저 릴리스를 위해 준비되며 head/master에 병합됩니다.

6. 수정 사항이 적용되는 날짜에 [golang-announce](https://groups.google.com/group/golang-announce), [golang-dev](https://groups.google.com/group/golang-dev), 그리고 [golang-nuts](https://groups.google.com/group/golang-nuts)로 공지사항이 전송됩니다.

이 과정은 특히 다른 프로젝트의 유지 관리자와의 협력이 필요할 때 시간이 다소 소요될 수 있습니다. 버그를 가능한 한 신속하게 처리하기 위해 모든 노력을 기울이겠지만, 공개 과정이 일관되게 처리되도록 하기 위해 위에 설명된 프로세스를 따르는 것이 중요합니다.

CVE 번호가 할당되는 보안 문제의 경우, 해당 문제는 [CVEDetails 웹사이트의 "Golang" 제품](https://www.cvedetails.com/vulnerability-list/vendor_id-14185/Golang.html)과 [National Vulnerability Disclosure 사이트](https://web.nvd.nist.gov/view/vuln/search)에 공개적으로 목록화됩니다.

## 보안 업데이트 수신

보안 공지사항을 받는 가장 좋은 방법은 [golang-announce](https://groups.google.com/forum/#!forum/golang-announce) 메일링 리스트를 구독하는 것입니다. 보안 이슈와 관련된 모든 메시지에는 `[security]` 접두사가 붙습니다.

## 이 정책에 대한 의견

이 정책을 개선하기 위한 제안 사항이 있다면, [이슈를 생성](/issue/new)하여 논의해 주세요.
