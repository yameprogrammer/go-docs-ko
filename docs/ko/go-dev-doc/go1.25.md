```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.25 소개 {#introduction}

### 새 기능 및 개선 사항

*   **Go 1.25의 주요 특징**
    *   새로운 기능
    *   성능 개선
    *   보안 강화
*   **Go 1.25에서 변경된 사항**
    *   버그 수정
    *   API 변경
    *   기타 개선 사항

### Go 1.25 다운로드

*   [Go 1.25 다운로드](https://example.com/go1.25)
*   [Go 1.25 설치 가이드](https://example.com/go1.25-install)

가장 최신 Go 릴리스인 버전 1.25는 [2025년 8월](/doc/devel/release#go1.25.0)에 출시되며, Go 1.24 이후 6개월 후입니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
항상처럼, 이 릴리스는 Go 1의 호환성 약속을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

<!-- go.dev/issue/70128 -->

Go 1.25에서는 Go 프로그램에 영향을 미치는 언어 변경 사항은 없습니다.
그러나 [언어 사양](/ref/spec)에서는 핵심 유형의 개념을 제거하고 대신 상세한 설명을 사용하도록 변경되었습니다.
자세한 내용은 다음 [블로그 게시물](/blog/coretypes)를 참조하십시오.

## 도구 {#tools}

### Go 명령어 {#go-command}

`go build` 명령어의 `-asan` 옵션은 이제 프로그램 종료 시 누수 감지를 기본 설정으로 사용합니다.
이 옵션은 C에서 할당된 메모리가 해제되지 않고, C 또는 Go에서 할당된 다른 메모리에 의해 참조되지 않으면 오류를 보고합니다.
이 새로운 오류 보고는 `ASAN_OPTIONS=detect_leaks=0`을 환경 변수에 설정하여 비활성화할 수 있습니다.

<!-- go.dev/issue/71867 -->
Go 배포판에는 사전 빌드된 도구 바이너리가 줄어듭니다. 컴파일러 및 링커와 같은 핵심 도구 체인 바이너리는 여전히 포함되지만, 빌드 또는 테스트 작업에 의해 호출되지 않는 도구는 필요에 따라 `go tool`을 사용하여 빌드 및 실행됩니다.

<!-- go.dev/issue/42965 -->
새로운 `go.mod` `ignore` 지시문 [설명](https://go.dev/ref/mod#go-mod-file-ignore)을 사용하여, `go` 명령이 무시해야 할 디렉토리를 지정할 수 있습니다. 이러한 디렉토리 및 하위 디렉토리에 있는 파일은 `go` 명령에서 `all` 또는 `./...`과 같은 패키지 패턴과 일치할 때 무시되지만, 여전히 모듈 ZIP 파일에 포함됩니다.

<!-- go.dev/issue/68106 -->
새로운 `go doc` `-http` 옵션은 요청된 객체의 문서를 보여주는 문서 서버를 시작하고, 브라우저 창에서 문서를 엽니다.

<!-- go.dev/issue/69712 -->

새로운 `go version -m -json` 옵션은 주어진 Go 바이너리 파일에 내장된 `runtime/debug.BuildInfo` 구조체의 JSON 인코딩을 출력합니다.

<!-- go.dev/issue/34055 -->
`go` 명령은 이제 저장소의 하위 디렉토리를 모듈의 루트 경로로 사용할 수 있습니다. `<meta name="go-import" content="root-path vcs repo-url subdir">` 구문을 사용하여 모듈 경로를 `<vcs-find>` 시에 지정할 때, `root-path`가 버전 관리 시스템 `vcs`의 `repo-url`의 `subdir`와 일치함을 나타낼 수 있습니다.

<!-- go.dev/issue/71294 -->

새로운 `work` 패키지 패턴은 `work` (이전에는 `main`이라고 불렸던) 모듈 내의 모든 패키지를 일치시킵니다.
이것은 모드 모드에서 단일 `work` 모듈이거나, 워크스페이스 모드에서 워크스페이스 모듈의 집합일 수 있습니다.

<!-- go.dev/issue/65847 -->

`go` 명령이 `go.mod` 또는 `go.work` 파일의 `go` 줄을 업데이트하면,
[더 이상](/ref/mod#go-mod-file-toolchain) 도구 줄을 추가하지 않고,
명령의 현재 버전을 지정하는 줄을 추가하지 않습니다.

### 수의사 {#vet}

`go vet` 명령어는 다음과 같은 새로운 분석 기능을 포함합니다:

<!-- go.dev/issue/18022 -->

- [waitgroup](https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/waitgroup),
  `sync.WaitGroup.Add` 호출이 잘못된 경우를 보고합니다;

<!-- go.dev/issue/28308 -->

- [hostport](https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/hostport),
  이것은 `fmt.Sprintf("%s:%d", host, port)`를 사용하여 주소(`net.Dial`](/pkg/net#Dial)를 구성하는 사용법을 보고하며, 이는 IPv6와 호환되지 않습니다. 대신, `net.JoinHostPort`](/pkg/net#JoinHostPort)를 사용하는 것을 권장합니다.

## 런타임 {#runtime}

### 컨테이너를 고려한 `GOMAXPROCS`

<!-- go.dev/issue/73193 -->

`GOMAXPROCS`의 기본 동작이 변경되었습니다. 이전 Go 버전에서는 `GOMAXPROCS`는 시작 시 사용 가능한 논리적 CPU의 수를 기본값으로 사용했습니다 ([`runtime.NumCPU`](/pkg/runtime#NumCPU)). Go 1.25에서는 두 가지 변경 사항이 도입되었습니다:

1. 리눅스에서, 런타임은 프로세스가 포함된 cgroup의 CPU 대역폭 제한을 고려합니다. 만약 CPU 대역폭 제한이 사용 가능한 논리 CPU 수보다 낮다면, `GOMAXPROCS`는 기본적으로 낮은 제한값으로 설정됩니다. 컨테이너 런타임 시스템(예: Kubernetes)에서 cgroup CPU 대역폭 제한은 일반적으로 "CPU 제한" 옵션과 일치합니다. Go 런타임은 "CPU 요청" 옵션을 고려하지 않습니다.

2. 모든 운영체제에서 런타임은 사용 가능한 논리적 CPU 개수 또는 cgroup CPU 대역폭 제한이 변경되면 주기적으로 `GOMAXPROCS`를 업데이트합니다.

이 두 가지 동작은 `GOMAXPROCS` 환경 변수를 수동으로 설정하거나 `runtime.GOMAXPROCS` 호출을 통해 설정되었을 때 자동으로 비활성화됩니다. 또한, `GODEBUG` 설정인 `containermaxprocs=0` 및 `updatemaxprocs=0`을 사용하여 명시적으로 비활성화할 수도 있습니다.

업데이트된 cgroup 한도를 읽기 위해, 런타임은 프로세스 수명 동안 cgroup 파일의 파일 디스크립터를 캐시에 유지합니다.

### 새로운 실험적인 가비지 컬렉터

<!-- go.dev/issue/73581 -->

새로운 가비지 컬렉터가 실험용으로 제공됩니다. 이 가비지 컬렉터의 설계는 더 나은 지역성과 CPU 확장성을 통해, 작은 객체의 마킹 및 스캔 성능을 향상시킵니다. 벤치마크 결과는 다양하지만, 실제 프로그램에서 가비지 컬렉터를 많이 사용하는 경우, 10~40%의 가비지 컬렉션 오버헤드 감소를 기대할 수 있습니다.

새로운 가비지 컬렉터는 빌드 시간에 `GOEXPERIMENT=greenteagc`를 설정하여 활성화할 수 있습니다. 저희는 이 설계가 계속 발전하고 개선될 것으로 예상합니다. 이에 Go 개발자 여러분께서는 이 기능을 사용해 보시고 경험을 공유해 주시기를 권장합니다. 설계에 대한 자세한 내용과 피드백 공유 방법을 참조하려면 [GitHub 이슈](https://github.com/issue/73581)를 참조하십시오.

### 비행기 블랙박스 추적

<!-- go.dev/issue/63185 -->

[실시간 실행 추적](/pkg/runtime/trace)은 오랫동안 애플리케이션의 저수준 동작을 이해하고 디버깅하는 강력하고 효과적인 방법을 제공해 왔지만, 비용이 많이 듭니다. 불행하게도, 추적의 크기와 지속적으로 실행 추적을 기록하는 비용 때문에, 이러한 추적은 드문 이벤트의 디버깅에는 일반적으로 실용적이지 않았습니다.

새로운 [`runtime/trace.FlightRecorder`](/pkg/runtime/trace#FlightRecorder) API는 지속적으로 트레이스를 메모리 내 링 버퍼에 기록하는 방식으로 런타임 실행 트레이스를 캡처하는 가벼운 방법을 제공합니다. 중요한 이벤트가 발생하면 프로그램은 [`FlightRecorder.WriteTo`](/pkg/runtime/trace#FlightRecorder.WriteTo)를 호출하여 트레이스의 마지막 몇 초를 파일에 저장할 수 있습니다. 이 방법은 애플리케이션이 실제로 중요한 트레이스만 캡처할 수 있도록 하여 훨씬 작은 트레이스를 생성합니다.

[`FlightRecorder`](/pkg/runtime/trace#FlightRecorder)가 캡처하는 시간 및 데이터 양은
[`FlightRecorderConfig`](/pkg/runtime/trace#FlightRecorderConfig) 내에서 구성할 수 있습니다.

### 처리되지 않은 패닉 출력 변경

<!-- go.dev/issue/71517 -->

프로그램이 처리되지 않은 패닉으로 종료될 때 출력되는 메시지
(패닉이 복구되었지만 다시 패닉이 발생한 경우)에는 더 이상
패닉 값의 텍스트가 반복되지 않습니다.

이전에, 프로그램이 `panic("PANIC")`를 발생시키고, 발생한 panic을 복구한 다음 원래 값을 사용하여 다시 panic을 발생시키면 다음과 같은 내용을 출력했습니다:

panic: PANIC [복구됨]
      panic: PANIC

이 프로그램은 이제 다음을 출력합니다:

panic: PANIC [복구, 재발생]

### Linux에서 VMA (가상 주소 영역) 이름

```
# VMA 이름 관련 정보
# 예시:
# /proc/meminfo 파일에서 VMA 정보 확인
# cat /proc/meminfo | grep VMA
```

## VMA의 종류

*   **Physical Memory:** 실제 물리 메모리 영역
*   **DMA 영역:** DMA (Direct Memory Access)를 통해 접근 가능한 영역
*   **Swap 영역:** 스왑 영역

## VMA 이름 확인 방법

1.  `cat /proc/meminfo` 명령어를 사용하여 VMA 정보를 확인합니다.
2.  `grep` 명령어를 사용하여 특정 VMA 이름을 검색합니다.

## 예시

```bash
cat /proc/meminfo | grep VMA
```

## 추가 정보

*   VMA는 프로세스 및 시스템 메모리 관리에 중요한 역할을 합니다.
*   VMA 정보를 통해 메모리 사용량을 분석하고 문제를 해결할 수 있습니다.

<!-- go.dev/issue/71546 -->

Linux 시스템에서 익명 가상 메모리 영역 (VMA) 이름에 대한 커널 지원이 있는 경우 (`CONFIG_ANON_VMA_NAME`), Go 런타임은 익명 메모리 매핑에 목적에 대한 컨텍스트 정보를 추가합니다. 예를 들어, 힙 메모리의 경우 `[anon: Go: heap]`입니다. 이 기능을 비활성화하려면 [GODEBUG 설정](/doc/godebug)에서 `decoratemappings=0`를 사용하십시오.

## 컴파일러

### `nil` 포인터 버그

<!-- https://go.dev/issue/72860, CL 657715 -->

이 릴리스는 Go 1.21에 도입된 [컴파일러 버그](/issue/72860)를 수정합니다. 이 버그는 nil 포인터 검사를 잘못하게 지연시킬 수 있습니다. 다음과 같은 프로그램(이전에는 성공적으로, 하지만(잘못하게) 실행되었지만) 이제(올바르게) nil-포인터 예외로 인해 패닉됩니다:

```
package main

import "os"

func main() {
	f, err := os.Open("nonExistentFile")
	name := f.Name()
	if err != nil {
		return
	}
	println(name)
}
```

이 프로그램은 `os.Open`의 결과를 확인하기 전에 결과를 사용하기 때문에 잘못되었습니다. 만약 `err`가 nil이 아니면, `f`의 결과가 nil일 수 있으며, 이 경우 `f.Name()`을 호출하면 오류가 발생해야 합니다. 하지만 Go 1.21 ~ 1.24 버전에서는 컴파일러가 오류 확인 후에 nil 체크를 지연시켜, Go 사양 위반으로 프로그램이 성공적으로 실행됩니다. Go 1.25에서는 더 이상 성공적으로 실행되지 않습니다. 만약 이러한 변경 사항이 코드를 영향을 미치고 있다면, 해결책은 `err`가 nil이 아닌지 확인하는 부분을 코드의 앞부분, 특히 오류를 발생시키는 문 바로 뒤에 배치하는 것입니다.

### DWARF5 지원

<!-- https://go.dev/issue/26379 -->

Go 1.25의 컴파일러와 링커는 이제 [DWARF 버전 5](https://dwarfstd.org/dwarf5std.html)를 사용하여 디버깅 정보를 생성합니다.
새로운 DWARF 버전은 Go 바이너리에 필요한 디버깅 정보의 공간을 줄이고, 특히 큰 Go 바이너리의 경우 링킹 시간을 단축합니다.
DWARF 5 생성 기능을 비활성화하려면 빌드 시간에 환경 변수 `GOEXPERIMENT=nodwarf5`를 설정할 수 있습니다 (이 백업 기능은 향후 Go 릴리스에서 제거될 수 있습니다).

### 더 빠른 슬라이스

<!-- CL 653856, 657937, 663795, 664299 -->

컴파일러는 이제 슬라이스의 백잉 스토어를 스택에 더 많은 경우에 할당할 수 있으며, 이는 성능을 향상시킵니다. 이 변경 사항은 잘못된 [unsafe.Pointer](/pkg/unsafe#Pointer) 사용의 영향을 증폭시킬 수 있습니다. 예를 들어 [issue 73199](/issue/73199)를 참조하십시오. 이러한 문제를 해결하려면 [bisect tool](https://pkg.go.dev/golang.org/x/tools/cmd/bisect)을 사용하여 `-compile=variablemake` 플래그를 사용하여 문제를 일으키는 할당을 찾을 수 있습니다. 또한 이러한 모든 새로운 스택 할당을 `-gcflags=all=-d=variablemakehash=n`을 사용하여 비활성화할 수도 있습니다.

## 링커 {#linker}

<!-- CL 660996 -->

이제 링커는 `-funcalign=N` 명령줄 옵션을 지원하며, 이는 함수 엔트리의 정렬을 지정합니다.
기본값은 플랫폼에 따라 다르며, 이번 릴리스에서는 변경되지 않았습니다.

## 표준 라이브러리 {#library}

### 새로운 testing/synctest 패키지

<!-- go.dev/issue/67434, go.dev/issue/73567 -->
새로운 `testing/synctest` 패키지는 동시성 코드 테스트를 위한 지원을 제공합니다.

[`Test`](/pkg/testing/synctest#Test) 함수는 격리된 "방" 내에서 테스트 함수를 실행합니다. 이 방 안에서는 시간이 가상으로 작동합니다: [`time`](/pkg/time) 패키지의 함수는 가짜 시계에서 작동하며, 방 내의 모든 고루틴이 차단되면 시계가 즉시 진행됩니다.

[`Wait`](/pkg/testing/synctest#Wait) 함수는 현재 루프 내의 모든 고루틴이 차단될 때까지 대기합니다.

이 패키지는 Go 1.24에서 `GOEXPERIMENT=synctest`로 처음 제공되었으며, 약간 다른 API를 사용했습니다. 이 실험 기능은 이제 일반적으로 사용 가능합니다. 이전 API는 `GOEXPERIMENT=synctest`로 설정된 경우 여전히 존재하지만, Go 1.26에서 제거될 예정입니다.

### 새로운 실험적인 encoding/json/v2 패키지 {#json_v2}

Go 1.25에는 새로운 실험적인 JSON 구현이 포함되어 있으며, 빌드 시간에 환경 변수 `GOEXPERIMENT=jsonv2`를 설정하여 활성화할 수 있습니다.

사용 시, 다음 두 개의 새로운 패키지가 사용 가능합니다:
- [`encoding/json/v2`](/pkg/encoding/json/v2) 패키지는 `encoding/json` 패키지의 주요 버전입니다.
- [`encoding/json/jsontext`](/pkg/encoding/json/jsontext) 패키지는 JSON 구문에 대한 더 낮은 수준의 처리를 제공합니다.

또한, "jsonv2" GOEXPERIMENT이 활성화되면:
- [`encoding/json`](/pkg/encoding/json) 패키지는 새로운 JSON 구현을 사용합니다.
  - 직렬화 및 역직렬화 동작은 변경되지 않지만, 패키지 함수의 반환하는 오류의 텍스트가 변경될 수 있습니다.
- [`encoding/json`](/pkg/encoding/json) 패키지에는 직렬화 및 역직렬화 설정을 위한 여러 새로운 옵션이 포함되어 있습니다.

새로운 구현은 많은 시나리오에서 기존 구현보다 훨씬 뛰어난 성능을 보입니다. 일반적으로, 인코딩 성능은 두 구현 간에 거의 동일하며, 새로운 구현에서는 디코딩 속도가 훨씬 빠릅니다. 더 자세한 분석은 [github.com/go-json-experiment/jsonbench](https://github.com/go-json-experiment/jsonbench) 저장소에서 확인할 수 있습니다.

자세한 내용은 [제안 이슈](/issue/71497)를 참조하십시오.

저희는 `encoding/json`을 사용하는 사용자들이 `GOEXPERIMENT=jsonv2`를 활성화하여 프로그램을 테스트하도록 권장합니다. 이를 통해 새로운 구현과의 호환성 문제를 감지하는 데 도움이 됩니다.

저희는 [`encoding/json/v2`](/pkg/encoding/json/v2)의 디자인이 계속 발전할 것으로 예상합니다. 개발자 여러분께서는 새로운 API를 사용해 보고 [제안 이슈](/issue/71497)에 피드백을 제공해 주시기를 권장합니다.

### 라이브러리의 미세 조정 {#미세_조정}

#### [`archive/tar`](/pkg/archive/tar/)

[`Writer.AddFS`](/pkg/archive/tar#Writer.AddFS) 구현은 이제 `io/fs.ReadLinkFS`](/pkg/io/fs#ReadLinkFS)를 구현하는 파일 시스템에 대한 심볼릭 링크를 지원합니다.

```
#### [`encoding/asn1`](/pkg/encoding/asn1/)
```

[`Unmarshal`](/pkg/encoding/asn1#Unmarshal) 및 [`UnmarshalWithParams`](/pkg/encoding/asn1#UnmarshalWithParams)
이제 ASN.1 유형인 T61String 및 BMPString을 보다 일관성 있게 파싱합니다. 이로 인해 이전에는 허용되었던 잘못된 인코딩이 이제 거부될 수 있습니다.

#### [`crypto`](/pkg/crypto/)

[`MessageSigner`](/pkg/crypto#MessageSigner)는 메시지를 서명하기 전에 직접 해시를 생성하고자 하는 서명자에게 구현될 수 있는 새로운 서명 인터페이스입니다.
또한, [`SignMessage`](/pkg/crypto#SignMessage)라는 새로운 함수가 도입되었으며, 이는 [`Signer`](/pkg/crypto#Signer) 인터페이스를 [`MessageSigner`](/pkg/crypto#MessageSigner)로 업그레이드하려고 시도합니다. 성공적으로 수행되면 [`MessageSigner.SignMessage`](/pkg/crypto#MessageSigner.SignMessage) 메서드를 사용하고, 그렇지 않으면 [`Signer.Sign`](/pkg/crypto#Signer.Sign) 메서드를 사용합니다. 이를 통해 코드가 [`Signer`](/pkg/crypto#Signer) 및 [`MessageSigner`](/pkg/crypto#MessageSigner)를 모두 지원할 수 있습니다.

`fips140` [GODEBUG 설정](/doc/godebug)이 프로그램이 시작된 후 변경하는 것은 더 이상 효과가 없습니다.
이전에는 이 설정을 변경하는 것이 허용되지 않았으며, 변경하면 프로그램이 예기치 않게 종료될 수 있다고 설명되어 있었습니다.

SHA-1, SHA-256 및 SHA-512은 AVX2 명령어가 사용되지 않는 amd64 환경에서는 더 느려집니다.
2015년 이후에 출시된 모든 서버 프로세서(및 대부분의 다른 프로세서)는 AVX2를 지원합니다.

#### [`crypto/ecdsa`](/pkg/crypto/ecdsa/)

새로운 [`ParseRawPrivateKey`](/pkg/crypto/ecdsa#ParseRawPrivateKey),
[`ParseUncompressedPublicKey`](/pkg/crypto/ecdsa#ParseUncompressedPublicKey),
[`PrivateKey.Bytes`](/pkg/crypto/ecdsa#PrivateKey.Bytes), 및
[`PublicKey.Bytes`](/pkg/crypto/ecdsa#PublicKey.Bytes) 함수 및 메서드는
낮은 수준의 인코딩을 구현하며, [`crypto/elliptic`](/pkg/crypto/elliptic) 또는 [`math/big`](/pkg/math/big)
함수 및 메서드를 사용하는 필요성을 대체합니다.

FIPS 140-3 모드가 활성화되면 서명 속도가 4배 더 빨라져, 비-FIPS 모드와 동일한 성능을 제공합니다.

#### [`crypto/ed25519`](/pkg/crypto/ed25519/)

FIPS 140-3 모드가 활성화되면, 서명 속도가 4배 빨라져, 비-FIPS 모드와 동일한 성능을 제공합니다.

#### [`crypto/elliptic`](/pkg/crypto/elliptic/)

일부 [`Curve`](/pkg/crypto/elliptic#Curve) 구현에서 숨겨져 있거나 문서화되지 않은 `Inverse` 및 `CombinedMult` 메서드가 제거되었습니다.

#### [`crypto/rsa`](/pkg/crypto/rsa/)

[`PublicKey`](/pkg/crypto/rsa#PublicKey)는 더 이상 모듈 값은 비밀로 취급된다는 주장을 하지 않습니다. [`VerifyPKCS1v15`](/pkg/crypto/rsa#VerifyPKCS1v15) 및 [`VerifyPSS`](/pkg/crypto/rsa#VerifyPSS)는 이미 모든 입력이 공개되어 유출될 수 있으며, 다른 공개 값으로부터 모듈을 복구할 수 있는 수학적 공격이 존재한다는 경고를 이미 표시하고 있었습니다.

키 생성 속도가 현재 3배 더 빨라졌습니다.

#### [`crypto/sha1`](/pkg/crypto/sha1/)

해싱은 SHA-NI 지침이 사용 가능한 경우 amd64에서 2배 더 빠릅니다.

#### [`crypto/sha3`](/pkg/crypto/sha3/)

새로운 [`SHA3.Clone`](/pkg/crypto/sha3#SHA3.Clone) 메서드는 [`hash.Cloner`](/pkg/hash#Cloner)를 구현합니다.

해싱은 Apple M 프로세서에서 2배 더 빠르게 수행됩니다.

#### [`crypto/tls`](/pkg/crypto/tls/)

새로운 [`ConnectionState.CurveID`](/pkg/crypto/tls#ConnectionState.CurveID)
필드는 연결을 설정하는 데 사용되는 키 교환 메커니즘을 노출합니다.

새로운 [`Config.GetEncryptedClientHelloKeys`](/pkg/crypto/tls#Config.GetEncryptedClientHelloKeys)
콜백은 서버가 암호화된 클라이언트 헬로 확장(Encrypted Client Hello extension)을 수신할 때 사용할 [`EncryptedClientHelloKey`](/pkg/crypto/tls#EncryptedClientHelloKey)를 설정하는 데 사용될 수 있습니다.

SHA-1 서명 알고리즘은 TLS 1.2 핸shakes에서 더 이상 허용되지 않습니다 (RFC 9155 참조: [https://www.rfc-editor.org/rfc/rfc9155.html]).
`tlssha1=1`의 [GODEBUG 설정](/doc/godebug)을 사용하여 다시 활성화할 수 있습니다.

[FIPS 140-3 모드](/doc/security/fips140)가 활성화되면, TLS 1.2에서는 Extended Master Secret이 필요하며, Ed25519 및 X25519MLKEM768이 허용됩니다.

TLS 서버는 이제 가장 지원되는 프로토콜 버전을 선호하며, 이는 클라이언트가 선호하는 버전이 아닐 수도 있습니다.

<!-- CL 687855 -->
TLS 클라이언트와 서버 모두 이제 사양을 더 엄격하게 준수하고, 비호환 동작을 거부합니다. 호환되는 피어와의 연결에는 영향을 미치지 않아야 합니다.

#### [`crypto/x509`](/pkg/crypto/x509/)

[`CreateCertificate`](/pkg/crypto/x509#CreateCertificate),
[`CreateCertificateRequest`](/pkg/crypto/x509#CreateCertificateRequest) 및
[`CreateRevocationList`](/pkg/crypto/x509#CreateRevocationList)는 이제 `crypto.MessageSigner` 서명 인터페이스뿐만 아니라
`crypto.Signer`도 받을 수 있습니다. 이를 통해 이러한 함수는 "한 번 실행" 서명 인터페이스를 구현하는 서명자를 사용할 수 있으며, 호출자가 아닌 서명 자체에서 해싱을 수행합니다.

[`CreateCertificate`](/pkg/crypto/x509#CreateCertificate)는 `SubjectKeyId`가 누락된 경우에 SHA-256의 절단된 버전을 사용하여 채웁니다.
[GODEBUG 설정](/doc/godebug)인 `x509sha256skid=0`는 SHA-1로 되돌립니다.

[`ParseCertificate`](/pkg/crypto/x509#ParseCertificate)는 이제 `BasicConstraints` 확장 내에 음성 `pathLenConstraint`가 포함된 인증서를 거부합니다.

[`ParseCertificate`](/pkg/crypto/x509#ParseCertificate)는 이제 ASN.1 T61String 및 BMPString 유형으로 인코딩된 문자열을 보다 일관성 있게 처리합니다. 이로 인해 이전에는 허용되었던 잘못된 인코딩이 이제 거부될 수 있습니다.

#### [`debug/elf`](/pkg/debug/elf/)

[`debug/elf`](/pkg/debug/elf) 패키지는 다음과 같은 두 가지 새로운 상수를 추가합니다:
- [`PT_RISCV_ATTRIBUTES`](/pkg/debug/elf#PT_RISCV_ATTRIBUTES)
- [`SHT_RISCV_ATTRIBUTES`](/pkg/debug/elf#SHT_RISCV_ATTRIBUTES)
  RISC-V ELF 파싱용.

```
#### [`go/ast`](패키지/go/ast/)
```

`[FilterPackage](pkg/ast#FilterPackage)`, `[PackageExports](pkg/ast#PackageExports)`, 및 `[MergePackageFiles](pkg/ast#MergePackageFiles)` 함수, 그리고 `[MergeMode](pkg/go/ast#MergeMode)` 타입 및 그 상수들은 모두 더 이상 사용되지 않습니다. 이는 매우 오래된 `[Object](pkg/ast#Object)` 및 `[Package](pkg/ast#Package)` 메커니즘에서만 사용하기 위한 것입니다.

새로운 [`PreorderStack`](/pkg/go/ast#PreorderStack) 함수는 [`Inspect`](/pkg/go/ast#Inspect)와 마찬가지로 구문 트리를 순회하고 서브 트리의 탐색을 제어하지만, 편의를 위해 각 지점에서 감싸고 있는 노드의 스택도 제공합니다.

#### [`go/parser`](/pkg/go/parser/)

[`ParseDir`](/pkg/go/parser#ParseDir) 함수는 더 이상 사용되지 않습니다.

#### [`go/token`](/pkg/go/token/)

새로운 [`FileSet.AddExistingFiles`](/pkg/go/token#FileSet.AddExistingFiles) 메서드는 기존
[`File`](/pkg/go/token#File)를 [`FileSet`](/pkg/go/token#FileSet)에 추가하거나, 특정
[`File`](/pkg/go/token#File)들의 집합에 대해 [`FileSet`](/pkg/go/token#FileSet)를 생성할 수 있도록 하여, 장기간 실행되는 애플리케이션에서 단일 전역
[`FileSet`](/pkg/go/token#FileSet)와 관련된 문제를 해결합니다.

#### [`go/types`](/pkg/go/types/)

[`Var`](/pkg/go/types#Var)에 이제 `Var.Kind` 메서드가 추가되어 변수를 다음과 같이 분류할 수 있습니다: 패키지 수준, 수신자, 매개변수, 결과, 지역 변수 또는 구조체 필드.

새로운 [`LookupSelection`](/pkg/go/types#LookupSelection) 함수는 주어진 이름과 수신자 유형에 해당하는 필드 또는 메서드를 찾고, 기존의 [`LookupFieldOrMethod`](/pkg/go/types#LookupFieldOrMethod) 함수와 유사하게 작동하지만, 결과를 [`Selection`](/pkg/go/types#Selection) 형식으로 반환합니다.

#### [`hash`](/pkg/hash/)

새로운 [`XOF`](/pkg/hash#XOF) 인터페이스는 "확장 가능한 출력 함수"를 통해 구현될 수 있으며, 이는 임의의 또는 무제한의 출력 길이를 갖는 해시 함수와 같습니다. 예를 들어 [SHAKE](/pkg/crypto/sha3#SHAKE)가 있습니다.

새로운 [`Cloner`](/pkg/hash#Cloner) 인터페이스를 구현하는 해시 객체는 자신의 상태의 복사본을 반환할 수 있습니다.
표준 라이브러리의 모든 [`Hash`](/pkg/hash#Hash) 구현이 이제 [`Cloner`](/pkg/hash#Cloner) 인터페이스를 구현합니다.

#### [`hash/maphash`](/pkg/hash/maphash/)

새로운 `[Hash.Clone](pkg/hash/maphash#Hash.Clone)` 메서드는 `[hash.Cloner](pkg/hash#Cloner)`를 구현합니다.

#### [`io/fs`](/pkg/io/fs/)

새로운 [`ReadLinkFS`](/pkg/io/fs#ReadLinkFS) 인터페이스는 파일 시스템 내의 심볼릭 링크를 읽을 수 있는 기능을 제공합니다.

#### [`log/slog`](/pkg/log/slog/)

[`GroupAttrs`](/pkg/log/slog#GroupAttrs)는 [`Attr`](/pkg/log/slog#Attr) 값의 슬라이스를 사용하여 그룹 [`Attr`](/pkg/log/slog#Attr)를 생성합니다.

[`Record`](/pkg/log/slog#Record)에 이제 `Source` 메서드가 추가되었으며, 해당 소스 위치를 반환하거나, 사용할 수 없는 경우 `nil`을 반환합니다.

```
#### [`mime/multipart`](/pkg/mime/multipart/)
```

새로운 헬퍼 함수 [`FileContentDisposition`](/pkg/mime/multipart#FileContentDisposition)는 multipart
Content-Disposition 헤더 필드를 생성합니다.

#### [`net`](/pkg/net/)

[`LookupMX`](/pkg/net#LookupMX) 및 [`Resolver.LookupMX`](/pkg/net#Resolver.LookupMX)는 이제 유효한 IP 주소와 함께 유효한 도메인 이름을 반환합니다.
이전에는 이름 서버가 IP 주소를 DNS 이름으로 반환하면, `LookupMX`는 RFC 요구 사항에 따라 이를 버렸습니다.
그러나 실제로는 이름 서버가 때때로 IP 주소를 반환합니다.

Windows에서, [`ListenMulticastUDP`](/pkg/net#ListenMulticastUDP)가 이제 IPv6 주소를 지원합니다.

On Windows, 이제 [`os.File`](/pkg/os#File) 와 네트워크 연결 간의 변환이 가능합니다. 구체적으로, `[FileConn](https://pkg/net#FileConn)`, `[FilePacketConn](https://pkg/net#FilePacketConn)`, 그리고 `[FileListener](https://pkg/net#FileListener)` 함수가 구현되었으며, 이는 열린 파일에 해당하는 네트워크 연결 또는 리스너를 반환합니다.

마찬가지로, `[TCPConn](https://pkg/net#TCPConn.File)`, `[UDPConn](https://pkg/net#UDPConn.File)`, `[UnixConn](https://pkg/net#UnixConn.File)`, `[IPConn](https://pkg/net#IPConn.File)`, `[TCPListener](https://pkg/net#TCPListener.File)`, 그리고 `[UnixListener](https://pkg/net#UnixListener.File)`의 `File` 메서드가 구현되었으며, 이는 네트워크 연결의 기본 `[os.File](https://pkg/os#File)`을 반환합니다.

#### [`net/http`](/pkg/net/http/)

새로운 [`CrossOriginProtection`](/pkg/net/http#CrossOriginProtection)는 [Cross-Site
Request Forgery (CSRF)](https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/CSRF)에 대한 보호를 구현하여, 안전하지 않은 크로스-오리진 브라우저 요청을 거부합니다.
[최신 브라우저 Fetch 메타데이터](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-Fetch-Site)를 사용하며, 토큰이나 쿠키가 필요하지 않으며, 원본 기반 및 패턴 기반 우회 기능을 지원합니다.

#### [`os`](/pkg/os/)

Windows에서, [`NewFile`](/pkg/os#NewFile)는 이제 비동기 I/O에 사용되는 핸들을 지원합니다 (즉,
[`syscall.FILE_FLAG_OVERLAPPED`](/pkg/syscall#FILE_FLAG_OVERLAPPED)가 [`syscall.CreateFile`](/pkg/syscall#CreateFile) 호출에 지정됩니다).
이 핸들은 Go 런타임의 I/O 완료 포트와 연결되며, 그 결과인 [`File`](/pkg/os#File)에 다음과 같은 이점을 제공합니다:

- I/O 메서드 (`File.Read`, `/pkg/os#File.Read`, `File.Write`, `/pkg/os#File.Write`, `File.ReadAt`, `/pkg/os#File.ReadAt`, `File.WriteAt`, `/pkg/os#File.WriteAt`)는 OS 스레드를 차단하지 않습니다.
- 데드라인 메서드 (`File.SetDeadline`, `/pkg/os#File.SetDeadline`, `File.SetReadDeadline`, `/pkg/os#File.SetReadDeadline`, `File.SetWriteDeadline`, `/pkg/os#File.SetWriteDeadline`)는 지원됩니다.

이 기능은 특히 Windows에서 이름 지정된 파이프를 통해 통신하는 애플리케이션에 특히 유용합니다.

참고: 핸들은 한 번에 하나의 완료 포트와만 연결될 수 있습니다.
`NewFile`에 제공된 핸드가 이미 완료 포트와 연결되어 있는 경우, 반환되는 `File`은 동기 I/O 모드로 다운그레이드됩니다.
이 경우, I/O 메서드는 OS 스레드를 차단하고, 타임아웃 메서드는 아무런 효과가 없습니다.

`DirFS` 및 `Root.FS`가 반환하는 파일 시스템은 새로운 `io/fs.ReadLinkFS` 인터페이스를 구현합니다.
`CopyFS`는 `io/fs.ReadLinkFS` 인터페이스를 구현하는 파일 시스템을 복사할 때 심볼릭 링크를 지원합니다.

[`Root`](/pkg/os#Root) 타입은 다음 추가 메서드를 지원합니다:

* [`Root.Chmod`](/pkg/os#Root.Chmod)
  * [`Root.Chown`](/pkg/os#Root.Chown)
  * [`Root.Chtimes`](/pkg/os#Root.Chtimes)
  * [`Root.Lchown`](/pkg/os#Root.Lchown)
  * [`Root.Link`](/pkg/os#Root.Link)
  * [`Root.MkdirAll`](/pkg/os#Root.MkdirAll)
  * [`Root.ReadFile`](/pkg/os#Root.ReadFile)
  * [`Root.Readlink`](/pkg/os#Root.Readlink)
  * [`Root.RemoveAll`](/pkg/os#Root.RemoveAll)
  * [`Root.Rename`](/pkg/os#Root.Rename)
  * [`Root.Symlink`](/pkg/os#Root.Symlink)
  * [`Root.WriteFile`](/pkg/os#Root.WriteFile)

<!-- go.dev/issue/73126는 67002의 일부로 문서화됨 -->

#### [`reflect`](/pkg/reflect/)

새로운 [`TypeAssert`](/pkg/reflect#TypeAssert) 함수는 주어진 유형의 [`Value`](/pkg/reflect#Value)를 직접 Go 값으로 변환할 수 있습니다. 이는 [`Value.Interface`](/pkg/reflect#Value.Interface)의 결과에 대한 유형 확인과 유사하지만, 불필요한 메모리 할당을 방지합니다.

#### [`regexp/syntax`](/pkg/regexp/syntax/)

`\p{name}` 및 `\P{name}` 특수 문자 클래스 구문은 이제 다음과 같은 이름을 허용합니다.
Any, ASCII, Assigned, Cn, 및 LC, 뿐만 아니라 `\p{Letter}`를 `\pL`로 사용하는와 같이 유니코드 범주 별칭도 지원합니다.
[Unicode TR18](https://unicode.org/reports/tr18/)에 따라, 대소문자를 구분하지 않고, 공백, 밑줄, 하이픈을 무시하며 이름 검색을 수행합니다.

#### [`runtime`](/pkg/runtime/)

`[`AddCleanup`](/pkg/runtime#AddCleanup)에 의해 예약된 정리 함수는 이제 동시에
병렬로 실행되므로, 특히 `[unique]( /pkg/unique)` 패키지와 같이
많은 사용 사례에 적합한 정리 작업을 더 효율적으로 수행할 수 있습니다.
단, 개별 정리 작업이 실행하거나, 오랜 시간 동안 대기해야 하는 경우,
정리 큐를 차단하지 않도록 새 고루틴으로 작업을 전달해야 합니다.

새로운 `GODEBUG=checkfinalizers=1` 설정은 finalizer 및 정리 작업과 관련된 일반적인 문제를 찾도록 도와줍니다. 예를 들어, GC 가이드 [`/doc/gc-guide#Finalizers_cleanups_and_weak_pointers`](https://pkg.go.dev/runtime#hdr-Environment_Variables)에 설명된 내용과 유사한 문제들을 찾을 수 있습니다.

이 모드에서는 런타임이 각 가비지 컬렉션 주기마다 진단을 실행하고, 또한 finalizer 및 정리 큐의 길이를 정기적으로 stderr로 보고하여, 장시간 실행되는 finalizer 및/또는 정리 작업과 관련된 문제를 식별하는 데 도움이 됩니다.

자세한 내용은 [GODEBUG 문서](https://pkg.go.dev/runtime#hdr-Environment_Variables)를 참조하십시오.

새로운 [`SetDefaultGOMAXPROCS`](/pkg/runtime#SetDefaultGOMAXPROCS) 함수는 `GOMAXPROCS`를 런타임 기본값으로 설정합니다. 즉, `GOMAXPROCS` 환경 변수가 설정되지 않은 것처럼 동작합니다. 이는 [새로운 `GOMAXPROCS` 기본값](https://container-aware-gomaxprocs)을 활성화하는 데 유용하며, 이 기본값이 `GOMAXPROCS` 환경 변이나 이전 [`GOMAXPROCS`](/pkg/runtime#GOMAXPROCS) 호출에 의해 비활성화된 경우에 사용됩니다.

#### [`runtime/pprof`](/pkg/runtime/pprof/)

실시간 내부 잠금에 대한 뮤텍스 프로파일이 이제 올바르게 작동하여 지연을 유발한 비상 영역의 끝을 가리킵니다. 이는 `sync.Mutex` 값에 대한 비상 상황에 대한 프로파일의 동작과 일치합니다. `GODEBUG`에 설정된 `runtimecontentionstacks` 설정, 이 설정은 Go 1.22부터 1.24까지의 이 프로파일의 비정상적인 동작을 활성화할 수 있었지만, 이제 제거되었습니다.

#### [`sync`](/pkg/sync/)

새로운 [`WaitGroup.Go`](/pkg/sync#WaitGroup.Go) 메서드는 goroutine을 생성하고 카운트하는 일반적인 패턴을 더 쉽게 사용할 수 있도록 합니다.

#### [`testing`](/pkg/testing/)

새로운 메서드 [`T.Attr`](/pkg/testing#T.Attr), [`B.Attr`](/pkg/testing#B.Attr), 및 [`F.Attr`](/pkg/testing#F.Attr)는 테스트 로그에 속성을 출력합니다. 속성은 테스트와 관련된 임의의 키와 값을 나타냅니다.

예를 들어, `TestF`라는 이름의 테스트에서,
`t.Attr("key", "value")`는 다음과 같이 출력됩니다:

```
=== ATTR 테스트 키 값
```

`-json` 플래그를 사용하면 속성이 "attr"라는 새 액션으로 나타납니다.

<!-- go.dev/issue/59928 -->

새로운 `[`Output`](/pkg/testing#T.Output) 메서드인 [`T`](/pkg/testing#T), [`B`](/pkg/testing#B) 및 [`F`](/pkg/testing#F)는 `[`TB.Log`](/pkg/testing#TB.Log)와 동일한 테스트 출력 스트림에 쓰는 `io.Writer`를 제공합니다.
`TB.Log`와 마찬가지로, 출력은 들여쓰기가 되어 있지만 파일 및 줄 번호는 포함하지 않습니다.

<!-- https://go.dev/issue/70464, CL 630137 -->
`AllocsPerRun` 함수가 이제 병렬 테스트가 실행될 때 패닉을 발생시킵니다.
`AllocsPerRun` 함수의 결과는 다른 테스트가 실행될 때 본질적으로 불안정합니다.
새로운 패닉 동작은 이러한 버그를 감지하는 데 도움이 됩니다.

#### [`testing/fstest`](/pkg/testing/fstest/)

[`MapFS`](/pkg/testing/fstest#MapFS)는 새로운 [`io/fs.ReadLinkFS`](/pkg/io/fs#ReadLinkFS) 인터페이스를 구현합니다.
[`TestFS`](/pkg/testing/fstest#TestFS)는 [`io/fs.ReadLinkFS`](/pkg/io/fs#ReadLinkFS) 인터페이스가 구현된 경우 해당 인터페이스의 기능을 검증합니다.
[`TestFS`](/pkg/testing/fstest#TestFS)는 무한 재귀를 방지하기 위해 심볼릭 링크를 더 이상 따라가지 않습니다.

#### [`unicode`](/pkg/unicode/)

새로운 `CategoryAliases` 맵은 카테고리 별칭 이름에 접근할 수 있도록 제공합니다 (예: "Letter"는 "L"에 해당).

새로운 카테고리 [`Cn`](/pkg/unicode#Cn) 및 [`LC`](/pkg/unicode#LC)는 각각 할당되지 않은 코드포인트와 대문자를 정의합니다.
이들은 항상 유니코드에 정의되어 있었지만, 이전 Go 버전에서는 실수로 누락되었습니다.
[`C`](/pkg/unicode#C) 카테고리에 이제 [`Cn`](/pkg/unicode#Cn)가 포함되어 있으며, 이는 모든 할당되지 않은 코드포인트를 포함함을 의미합니다.

#### [`unique`](/pkg/unique/)

[`unique`](/pkg/unique) 패키지는 이제 더 적극적이고, 효율적이며, 병렬 방식으로 인터내팅된 값을 회수합니다. 그 결과, `Make`를 사용하는 애플리케이션은 많은 실제 고유 값이 인터내팅될 때 메모리 부족 문제를 겪을 가능성이 줄어들었습니다.

`Make`에 전달되는 값 (특히 [`Handle`](/pkg/unique#Handle) 포함)이 이전에는 여러
가비지 컬렉션 사이클을 거쳐 수집되었으며, 이는 [`Handle`](/pkg/unique#Handle) 값의 체인의 깊이에 비례했습니다. 이제, 사용되지 않게 되면, 즉시 단일 사이클에서 수집됩니다.

## 포트

### 다윈

<!-- go.dev/issue/69839 -->
[공지](https://go.dev/doc/go1.24#darwin)된 바와 같이, Go 1.25는 macOS 12 Monterey 또는 이후 버전을 요구합니다.
이전 버전 지원은 중단되었습니다.

### Windows

<!-- go.dev/issue/71671 -->
Go 1.25는 [비활성화된](/doc/go1.24#windows) 32비트 윈도우/ARM 포트(`GOOS=windows` `GOARCH=arm`)를 포함하는 마지막 릴리스입니다. Go 1.26에서 제거됩니다.

### AMD64

<!-- go.dev/issue/71204 -->
`GOAMD64=v3` 모드 또는 그 이상의 모드에서는 컴파일러가 이제 fused multiply-add 명령어를 사용하여 부동 소수점 연산을 더 빠르고 정확하게 수행합니다. 이로 인해 프로그램이 생성하는 정확한 부동 소수점 값에 변경이 생길 수 있습니다.

충분한 정밀도를 확보하기 위해 명시적인 `float64` 형 변환을 사용하세요. 예를 들어, `float64(a*b)+c`와 같이 사용합니다.

### Loong64

<!-- CLs 533717, 533716, 543316, 604176 -->
Linux/loong64 포트는 이제 race detector를 지원하며, C 코드에서 traceback 정보를 수집합니다.
`runtime.SetCgoTraceback`을 사용하여, Cgo 프로그램을 내부 링크 모드로 연결합니다.

### RISC-V

<!-- CL 420114 -->
리눅스/리스이64 포트는 이제 `plugin` 빌드 모드를 지원합니다.

<!-- https://go.dev/issue/61476, CL 633417 -->
`GORISCV64` 환경 변수는 이제 새로운 값을 `rva23u64`를 지원하며, 이는 RVA23U64 사용자 모드 애플리케이션 프로필을 선택합니다.

<!--
relnote todo에서 생성 및 검토된 결과, 그리고 bug/CL:에서 추출한 요약 정보: -->

<!-- 1.25 릴리스 노트에 언급할 필요 없는 항목이지만, relnote todo에 의해 캡처됨
* 기존 제안 업데이트
* 승인된 제안: https://go.dev/issue/30999 (https://go.dev/cl/671795)
* 승인된 제안: https://go.dev/issue/36532 (https://go.dev/cl/647555)
* 승인된 제안: https://go.dev/issue/48429 (https://go.dev/cl/648577)
* 승인된 제안: https://go.dev/issue/51572 (https://go.dev/cl/651996)
* 승인된 제안: https://go.dev/issue/51430 (https://go.dev/cl/644997, https://go.dev/cl/646355)
* 승인된 제안: https://go.dev/issue/60905 (https://go.dev/cl/645795)
* 승인된 제안: https://go.dev/issue/61716 (https://go.dev/cl/644475)
* 승인된 제안: https://go.dev/issue/64876 (https://go.dev/cl/649435)
* 승인된 제안: https://go.dev/issue/70123 (https://go.dev/cl/657116)
* 승인된 제안: https://go.dev/issue/61901 (https://go.dev/cl/647875)
* 승인된 제안: https://go.dev/issue/64207 (https://go.dev/cl/647015, https://go.dev/cl/652235)
* 승인된 제안: https://go.dev/issue/70200 (https://go.dev/cl/674916)

For subrepos:
승인된 제안 https://go.dev/issue/53757 (https://go.dev/cl/644575)
승인된 제안 https://go.dev/issue/54743 (https://go.dev/cl/532415)
승인된 제안 https://go.dev/issue/57792 (https://go.dev/cl/649716, https://go.dev/cl/651737)
승인된 제안 https://go.dev/issue/58523 (https://go.dev/cl/538235)
승인된 제안 https://go.dev/issue/61537 (https://go.dev/cl/531935)
승인된 제안 https://go.dev/issue/61940 (https://go.dev/cl/650235)
승인된 제안 https://go.dev/issue/67839 (https://go.dev/cl/646535)
승인된 제안 https://go.dev/issue/68780 (https://go.dev/cl/659835)
승인된 제안 https://go.dev/issue/69095 (https://go.dev/cl/649320, https://go.dev/cl/649321, https://go.dev/cl/649337, https://go.dev/cl/649376, https://go.dev/cl/649377, https://go.dev/cl/649378, https://go.dev/cl/649379, https://go.dev/cl/649380, https://go.dev/cl/649397, https://go.dev/cl/649398, https://go.dev/cl/649419, https://go.dev/cl/649497, https://go.dev/cl/649498, https://go.dev/cl/649618, https://go.dev/cl/649675, https://go.dev/cl/649676, https://go.dev/cl/649677, https://go.dev/cl/649695, https://go.dev/cl/649696, https://go.dev/cl/649697, https://go.dev/cl/649698, https://go.dev/cl/649715, https://go.dev/cl/649717, https://go.dev/cl/649718, https://go.dev/cl/649755, https://go.dev/cl/649775, https://go.dev/cl/649795, https://go.dev/cl/649815, https://go.dev/cl/649835, https://go.dev/cl/651336, https://go.dev/cl/651736, https://go.dev/cl/651737, https://go.dev/cl/658018)
승인된 제안 https://go.dev/issue/70859 (https://go.dev/cl/666056, https://go.dev/cl/670835, https://go.dev/cl/672015, https://go.dev/cl/672016, https://go.dev/cl/672017)
승인된 제안 https://go.dev/issue/32816 (https://go.dev/cl/645155, https://go.dev/cl/645455, https://go.dev/cl/645955, https://go.dev/cl/646255, https://go.dev/cl/646455, https://go.dev/cl/646495, https://go.dev/cl/646655, https://go.dev/cl/646875, https://go.dev/cl/647298, https://go.dev/cl/647299, https://go.dev/cl/647736, https://go.dev/cl/648581, https://go.dev/cl/648715, https://go.dev/cl/648976, https://go.dev/cl/648995, https://go.dev/cl/649055, https://go.dev/cl/649056, https://go.dev/cl/649057, https://go.dev/cl/649456, https://go.dev/cl/649476, https://go.dev/cl/650755, https://go.dev/cl/651615, https://go.dev/cl/651617, https://go.dev/cl/651655, https://go.dev/cl/653436)
[cross-site request forgery (csrf)]: https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/CSRF
[sec-fetch-site]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-Fetch-Site
