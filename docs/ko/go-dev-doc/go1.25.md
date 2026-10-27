Please provide the Markdown content you would like me to translate. You have provided the CSS style, but not the text to be translated. I am ready to start once you provide the source content.

## Go 1.25 소개 {#introduction}

최신 Go 릴리스인 버전 1.25는 [Go 1.24](/doc/go1.24) 이후 6개월 뒤인 [2025년 8월](/doc/devel/release#go1.25.0)에 출시됩니다.
변경 사항의 대부분은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언제나 그렇듯이, 이번 릴리스는 호환성에 대한 Go 1 약속을 유지합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 기대합니다.

## 언어 변경 사항 {#language}

<!-- go.dev/issue/70128 -->

Go 1.25에서는 Go 프로그램에 영향을 주는 언어 변경 사항이 없습니다.
하지만 [언어 사양](/ref/spec)에서 핵심 타입(core types)이라는 개념이 제거되었으며, 대신 전용 설명 문구로 대체되었습니다.
자세한 내용은 관련 [블로그 포스트](/blog/coretypes)를 참조하십시오.

## 도구 {#tools}

### Go 명령어 {#go-command}

`go build`의 `-asan` 옵션은 이제 프로그램 종료 시 기본적으로 누수 탐지(leak detection)를 수행합니다.
C에서 할당된 메모리가 해제되지 않았고, C 또는 Go에서 할당된 다른 메모리에 의해 참조되지 않는 경우 에러를 보고합니다.
이러한 새로운 에러 보고는 프로그램을 실행할 때 환경 변수에 `ASAN_OPTIONS=detect_leaks=0`을 설정하여 비활성화할 수 있습니다.

<!-- go.dev/issue/71867 -->
Go 배포판에 포함되는 사전 빌드된 도구 바이너리 수가 줄어듭니다. 컴파일러 및 링커와 같은 핵심 툴체인 바이너리는 계속 포함되지만, 빌드 또는 테스트 작업에서 호출되지 않는 도구들은 필요에 따라 `go tool`에 의해 빌드되고 실행됩니다.

<!-- go.dev/issue/42965 -->
새로운 `go.mod` `ignore` [지시어](/ref/mod#go-mod-file-ignore)를 사용하여 `go` 명령어가 무시해야 할 디렉토리를 지정할 수 있습니다. 이 디렉토리와 그 하위 디렉토리에 있는 파일들은 `all` 또는 `./...`와 같은 패키지 패턴을 매칭할 때 `go` 명령어에 의해 무시되지만, 모듈 zip 파일에는 여전히 포함됩니다.

<!-- go.dev/issue/68106 -->
새로운 `go doc` `-http` 옵션은 요청된 객체의 문서를 보여주는 문서 서버를 시작하고, 브라우저 창에서 해당 문서를 엽니다.

<!-- go.dev/issue/69712 -->

새로운 `go version -m -json` 옵션은 지정된 Go 바이너리 파일에 내장된 `runtime/debug.BuildInfo` 구조체의 JSON 인코딩을 출력합니다.

<!-- go.dev/issue/34055 -->
이제 `go` 명령어는 `<meta name="go-import" content="root-path vcs repo-url subdir">` 구문을 사용하여 `root-path`가 버전 관리 시스템 `vcs`를 사용하는 `repo-url`의 `subdir`에 해당함을 나타낼 때, [모듈 경로를 확인](/ref/mod#vcs-find)하는 과정에서 저장소의 하위 디렉터리를 모듈 루트 경로로 사용하는 것을 지원합니다.

<!-- go.dev/issue/71294 -->

새로운 `work` 패키지 패턴은 작업(이전의 main) 모듈 내의 모든 패키지와 일치합니다. 이는 모듈 모드에서의 단일 작업 모듈 또는 워크스페이스 모드에서의 워크스페이스 모듈 집합을 의미합니다.

<!-- go.dev/issue/65847 -->

`go` 명령어가 `go.mod` 또는 `go.work` 파일의 `go` 라인을 업데이트할 때, 더 이상 해당 명령어의 현재 버전을 지정하는 toolchain 라인을 [추가하지 않습니다](/ref/mod#go-mod-file-toolchain).

### Vet {#vet}

`go vet` 명령어에 새로운 분석기(analyzers)들이 추가되었습니다:

<!-- go.dev/issue/18022 -->

- [waitgroup](https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/waitgroup),
  [`sync.WaitGroup.Add`](/pkg/sync#WaitGroup.Add) 호출 위치가 잘못된 경우를 보고합니다.

<!-- go.dev/issue/28308 -->

- [hostport](https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/hostport),
  `net.Dial`(/pkg/net#Dial)을 위한 주소를 생성할 때 `fmt.Sprintf("%s:%d", host, port)`를 사용하는 경우를 보고합니다. 이러한 방식은 IPv6에서 작동하지 않으므로, 대신 [`net.JoinHostPort`](/pkg/net#JoinHostPort)를 사용할 것을 권장합니다.

## 런타임 {#runtime}

### 컨테이너 인식 `GOMAXPROCS`

<!-- go.dev/issue/73193 -->

`GOMAXPROCS`의 기본 동작이 변경되었습니다. 이전 버전의 Go에서는 `GOMAXPROCS`가 시작 시 사용 가능한 논리 CPU 수([`runtime.NumCPU`](/pkg/runtime#NumCPU))를 기본값으로 사용했습니다. Go 1.25에서는 두 가지 변경 사항이 도입되었습니다:

1. Linux에서 런타임은 프로세스가 포함된 cgroup의 CPU 대역폭 제한(있는 경우)을 고려합니다. CPU 대역폭 제한이 사용 가능한 논리 CPU 수보다 낮으면, `GOMAXPROCS`는 기본적으로 더 낮은 제한값을 갖게 됩니다. Kubernetes와 같은 컨테이너 런타임 시스템에서 cgroup CPU 대역폭 제한은 일반적으로 "CPU limit" 옵션에 해당합니다. Go 런타임은 "CPU requests" 옵션을 고려하지 않습니다.

2. 모든 OS에서, 사용 가능한 논리 CPU의 수 또는 cgroup CPU 대역폭 제한이 변경되면 런타임이 주기적으로 `GOMAXPROCS`를 업데이트합니다.

이 두 가지 동작은 `GOMAXPROCS` 환경 변수나 [`runtime.GOMAXPROCS`](/pkg/runtime#GOMAXPROCS) 호출을 통해 `GOMAXPROCS`가 수동으로 설정된 경우 자동으로 비활성화됩니다. 또한 [GODEBUG 설정](/doc/godebug)인 `containermaxprocs=0` 및 `updatemaxprocs=0`을 통해 각각 명시적으로 비활성화할 수도 있습니다.

업데이트된 cgroup 제한 사항을 읽는 기능을 지원하기 위해, 런타임은 프로세스 수명 주기 동안 cgroup 파일에 대한 캐시된 파일 서술자(file descriptors)를 유지합니다.

### 새로운 실험적 가비지 컬렉터

<!-- go.dev/issue/73581 -->

새로운 가비지 컬렉터를 실험적 기능으로 사용할 수 있습니다. 이 가비지 컬렉터의 설계는 향상된 로컬리티(locality)와 CPU 확장성을 통해 작은 객체의 마킹 및 스캐닝 성능을 개선합니다. 벤치마크 결과는 다양하지만, 가비지 컬렉터를 많이 사용하는 실제 프로그램에서 가비지 컬렉션 오버헤드가 약 10—40% 정도 감소할 것으로 기대합니다.

새로운 가비지 컬렉터는 빌드 시 `GOEXPERIMENT=greenteagc`를 설정하여 활성화할 수 있습니다. 저희는 이 설계가 계속해서 진화하고 개선될 것으로 기대하고 있습니다. 이를 위해 Go 개발자분들이 직접 사용해 보시고 경험을 공유해 주시기를 권장합니다. 설계에 대한 자세한 내용과 피드백 공유 방법은 [GitHub 이슈](/issue/73581)를 참조하십시오.

### Trace flight recorder

<!-- go.dev/issue/63185 -->

[런타임 실행 추적(Runtime execution traces)](/pkg/runtime/trace)은 애플리케이션의 저수준 동작을 이해하고 디버깅하는 강력하지만 비용이 많이 드는 방법을 오랫동안 제공해 왔습니다. 불행히도, 추적 데이터의 크기가 크고 실행 추적을 지속적으로 기록하는 비용이 많이 들기 때문에, 일반적으로 드물게 발생하는 이벤트를 디버깅하는 데에는 실용적이지 않았습니다.

새로운 [`runtime/trace.FlightRecorder`](/pkg/runtime/trace#FlightRecorder) API는 인메모리 링 버퍼에 트레이스를 지속적으로 기록함으로써 런타임 실행 트레이스를 캡처하는 가벼운 방법을 제공합니다. 중요한 이벤트가 발생했을 때, 프로그램은 [`FlightRecorder.WriteTo`](/pkg/runtime/trace#FlightRecorder.WriteTo)를 호출하여 최근 몇 초간의 트레이스 스냅샷을 파일로 저장할 수 있습니다. 이러한 방식은 애플리케이션이 중요한 트레이스만 캡처할 수 있게 하여 훨씬 작은 크기의 트레이스를 생성합니다.

[`FlightRecorder`](/pkg/runtime/trace#FlightRecorder)가 캡처하는 시간의 길이와 데이터 양은 [`FlightRecorderConfig`](/pkg/runtime/trace#FlightRecorderConfig) 내에서 설정할 수 있습니다.

### 처리되지 않은 패닉 출력 변경

<!-- go.dev/issue/71517 -->

처리되지 않은 패닉(unhandled panic)으로 인해 프로그램이 종료될 때, 복구(recovered) 후 다시 패닉(repanicked)된 경우 출력되는 메시지에서 더 이상 패닉 값의 텍스트가 반복되지 않습니다.

이전에 `panic("PANIC")`으로 패닉이 발생하고, 이를 복구(recover)한 뒤 다시 원래 값으로 패닉을 발생시킨 프로그램은 다음과 같이 출력했습니다:

panic: PANIC [recovered]
      panic: PANIC

이 프로그램은 이제 다음과 같이 출력합니다:

panic: PANIC [recovered, repanicked]

### Linux의 VMA 이름 (VMA names on Linux)

<!-- go.dev/issue/71546 -->

익명 가상 메모리 영역(VMA) 이름에 대한 커널 지원(`CONFIG_ANON_VMA_NAME`)이 제공되는 Linux 시스템에서, Go 런타임은 익명 메모리 매핑에 해당 용도에 대한 컨텍스트를 주석으로 추가합니다. 예를 들어, 힙 메모리의 경우 `[anon: Go: heap]`와 같이 표시됩니다. 이 기능은 [GODEBUG 설정](/doc/godebug) `decoratemappings=0`을 통해 비활성화할 수 있습니다.

## 컴파일러 {#compiler}

### `nil` 포인터 버그

<!-- https://go.dev/issue/72860, CL 657715 -->

이번 릴리스에서는 Go 1.21에서 도입되어 nil 포인터 체크를 잘못 지연시킬 수 있었던 [컴파일러 버그](/issue/72860)를 수정했습니다. 이전에는 (잘못하게) 성공적으로 실행되었던 다음과 같은 프로그램들이 이제는 (정확하게) nil-pointer 예외와 함께 패닉(panic)이 발생하게 됩니다.

```go
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

이 프로그램은 `os.Open`의 결과를 에러 체크 전에 사용하기 때문에 잘못되었습니다. 만약 `err`가 non-nil이라면 `f` 결과가 nil일 수 있으며, 이 경우 `f.Name()`은 패닉(panic)이 발생해야 합니다. 하지만 Go 버전 1.21부터 1.24까지의 컴파일러는 nil 체크를 에러 체크 *이후*로 잘못 지연시켰으며, 이로 인해 Go 스펙을 위반하고 프로그램이 성공적으로 실행되는 결과가 발생했습니다. Go 1.25에서는 더 이상 성공적으로 실행되지 않습니다. 이 변경 사항이 코드에 영향을 미친다면, 해결 방법은 non-nil 에러 체크를 코드의 더 앞부분, 가급적이면 에러를 생성하는 문장 직후에 배치하는 것입니다.

### DWARF5 지원

<!-- https://go.dev/issue/26379 -->

Go 1.25의 컴파일러와 링커는 이제 [DWARF version 5](https://dwarfstd.org/dwarf5std.html)를 사용하여 디버그 정보를 생성합니다. 최신 DWARF 버전은 Go 바이너리의 디버깅 정보에 필요한 공간을 줄여주며, 특히 대규모 Go 바이너리의 경우 링킹 시간을 단축시킵니다.

빌드 시 환경 변수 `GOEXPERIMENT=nodwarf5`를 설정하여 DWARF 5 생성을 비활성화할 수 있습니다 (이 폴백 옵션은 향후 Go 릴리스에서 제거될 수 있습니다).

### 더 빠른 슬라이스(Faster slices)

<!-- CLs 653856, 657937, 663795, 664299 -->

이제 컴파일러가 더 많은 상황에서 슬라이스의 backing store를 스택에 할당할 수 있게 되었으며, 이는 성능을 향상시킵니다. 이 변경 사항은 잘못된 [`unsafe.Pointer](/pkg/unsafe#Pointer) 사용의 영향을 증폭시킬 가능성이 있으며, 이에 대한 예로 [issue 73199](/issue/73199)를 참조하십시오. 이러한 문제들을 추적하기 위해, `-compile=variablemake` 플래그를 사용하여 문제를 일으키는 할당 지점을 찾는 [bisect tool](https://pkg.go.dev/golang.org/x/tools/cmd/bisect)을 사용할 수 있습니다. 또한 `-gcflags=all=-d=variablemakehash=n`을 사용하여 이러한 모든 새로운 스택 할당을 끌 수 있습니다.

## 링커 (Linker) {#linker}

<!-- CL 660996 -->

이제 링커가 함수 엔트리의 정렬을 지정하는 `-funcalign=N` 커맨드 라인 옵션을 지원합니다.
기본값은 플랫폼에 따라 다르며, 이번 릴리스에서 변경되지 않았습니다.

## 표준 라이브러리 {#library}

### 새로운 testing/synctest 패키지

<!-- go.dev/issue/67434, go.dev/issue/73567 -->
새로운 [`testing/synctest`](/pkg/testing/synctest) 패키지는 동시성 코드 테스트를 위한 지원을 제공합니다.

[`Test`](/pkg/testing/synctest#Test) 함수는 격리된 "버블(bubble)" 내에서 테스트 함수를 실행합니다. 버블 내부에서 시간은 가상화됩니다: [`time`](/pkg/time) 패키지 함수들은 가짜 시계(fake clock)를 기반으로 동작하며, 버블 내의 모든 고루틴(goroutine)이 차단(blocked)된 경우 시계는 즉각적으로 앞으로 이동합니다.

[`Wait`](/pkg/testing/synctest#Wait) 함수는 현재 버블(bubble) 내의 모든 고루틴이 블록(block)될 때까지 기다립니다.

이 패키지는 처음 Go 1.24에서 `GOEXPERIMENT=synctest` 하에 약간 다른 API로 제공되었습니다. 이제 이 실험적 기능은 일반 제공(general availability) 단계로 전환되었습니다. `GOEXPERIMENT=synctest`가 설정되어 있다면 이전 API를 여전히 사용할 수 있지만, Go 1.26에서 제거될 예정입니다.

### 새로운 실험적 encoding/json/v2 패키지 {#json_v2}

Go 1.25에는 새로운 실험적 JSON 구현이 포함되어 있으며, 빌드 시 환경 변수 `GOEXPERIMENT=jsonv2`를 설정하여 활성화할 수 있습니다.

활성화하면 다음 두 가지 새로운 패키지를 사용할 수 있습니다:
- [`encoding/json/v2`](/pkg/encoding/json/v2) 패키지는 `encoding/json` 패키지의 주요 개정 버전입니다.
- [`encoding/json/jsontext`](/pkg/encoding/json/jsontext) 패키지는 JSON 구문의 더 낮은 수준의 처리를 제공합니다.

또한, "jsonv2" `GOEXPERIMENT`가 활성화된 경우:
- [`encoding/json`](/pkg/encoding/json) 패키지가
  새로운 JSON 구현을 사용합니다.
  마샬링(Marshaling) 및 언마샬링(unmarshaling) 동작은 영향을 받지 않지만,
  패키지 함수에서 반환하는 에러 메시지 텍스트가 변경될 수 있습니다.
- [`encoding/json`](/pkg/encoding/json) 패키지에
  마샬러(marshaler)와 언마샬러(unmarshaler)를 구성하는 데 사용할 수 있는
  다수의 새로운 옵션이 포함됩니다.

새로운 구현은 많은 시나리오에서 기존 구현보다 상당히 더 나은 성능을 보여줍니다. 일반적으로 인코딩 성능은 두 구현이 비슷하며, 디코딩은 새로운 구현에서 상당히 더 빠릅니다. 더 자세한 분석은 [github.com/go-json-experiment/jsonbench](https://github.com/go-json-experiment/jsonbench) 저장소를 참조하십시오.

더 자세한 내용은 [제안 이슈](/issue/71497)를 참조하십시오.

[`encoding/json`](/pkg/encoding/json) 사용자는 `GOEXPERIMENT=jsonv2`를 활성화하여 프로그램을 테스트함으로써 새로운 구현과의 호환성 문제를 감지하시길 권장합니다.

우리는 [`encoding/json/v2`](/pkg/encoding/json/v2)의 설계가 계속해서 발전할 것으로 예상합니다. 개발자분들이 새로운 API를 사용해 보시고 [제안 이슈](/issue/71497)를 통해 피드백을 제공해 주시기를 권장합니다.

### 라이브러리의 소규모 변경 사항 {#minor_library_changes}

#### [`archive/tar`](/pkg/archive/tar/)

[`Writer.AddFS`](/pkg/archive/tar#Writer.AddFS) 구현이 이제 [`io/fs.ReadLinkFS`](/pkg/io/fs#ReadLinkFS)를 구현하는 파일 시스템에 대해 심볼릭 링크(symbolic links)를 지원합니다.

#### [`encoding/asn1`](/pkg/encoding/asn1/)

[`Unmarshal`](/pkg/encoding/asn1#Unmarshal) 및 [`UnmarshalWithParams`](/pkg/encoding/asn1#UnmarshalWithParams)가 이제 ASN.1 타입인 T61String 및 BMPString을 더 일관되게 파싱합니다. 이로 인해 이전에 허용되었던 일부 잘못된 형식의 인코딩이 이제 거부될 수 있습니다.

#### [`crypto`](/pkg/crypto/)

[`MessageSigner`](/pkg/crypto#MessageSigner)는 서명할 메시지를 직접 해시하려는 서명자가 구현할 수 있는 새로운 서명 인터페이스입니다. 또한 [`SignMessage`](/pkg/crypto#SignMessage)라는 새로운 함수가 도입되었는데, 이 함수는 [`Signer`](/pkg/crypto#Signer) 인터페이스를 [`MessageSigner`](/pkg/crypto#MessageSigner)로 업그레이드하려고 시도하며, 성공하면 [`MessageSigner.SignMessage`](/pkg/crypto#MessageSigner.SignMessage) 메서드를 사용하고, 그렇지 않으면 [`Signer.Sign`](/pkg/crypto#Signer.Sign)을 사용합니다. 이는 코드에서 [`Signer`](/pkg/crypto#Signer)와 [`MessageSigner`](/pkg/crypto#MessageSigner)를 모두 지원하고자 할 때 사용할 수 있습니다.

프로그램이 시작된 후 `fips140` [GODEBUG 설정](/doc/godebug)을 변경하는 것은 이제 아무런 동작을 하지 않습니다(no-op).
이전에는 허용되지 않는 것으로 문서화되어 있었으며, 변경 시 panic이 발생할 수 있었습니다.

AVX2 명령어를 사용할 수 없는 amd64 환경에서 SHA-1, SHA-256, SHA-512의 속도가 이제 더 느려졌습니다.
2015년 이후에 생산된 모든 서버 프로세서(및 대부분의 기타 프로세서)는 AVX2를 지원합니다.

#### [`crypto/ecdsa`](/pkg/crypto/ecdsa/)

새로운 [`ParseRawPrivateKey`](/pkg/crypto/ecdsa#ParseRawPrivateKey),
[`ParseUncompressedPublicKey`](/pkg/crypto/ecdsa#ParseUncompressedPublicKey),
[`PrivateKey.Bytes`](/pkg/crypto/ecdsa#PrivateKey.Bytes), 그리고
[`PublicKey.Bytes`](/pkg/crypto/ecdsa#PublicKey.Bytes) 함수와 메서드는
저수준 인코딩을 구현하며, 이를 통해 [`crypto/elliptic`](/pkg/crypto/elliptic) 또는
[`math/big`](/pkg/math/big)의 함수와 메서드를 사용할 필요가 없어졌습니다.

FIPS 140-3 모드가 활성화되었을 때, 서명 속도가 이제 4배 더 빨라져 non-FIPS 모드의 성능과 동일해졌습니다.

#### [`crypto/ed25519`](/pkg/crypto/ed25519/)

FIPS 140-3 모드가 활성화되었을 때, 서명 속도가 4배 빨라져 non-FIPS 모드의 성능과 동일해졌습니다.

#### [`crypto/elliptic`](/pkg/crypto/elliptic/)

일부 [`Curve`](/pkg/crypto/elliptic#Curve) 구현체에 있던 숨겨져 있고 문서화되지 않은 `Inverse` 및 `CombinedMult` 메서드가 제거되었습니다.

#### [`crypto/rsa`](/pkg/crypto/rsa/)

[`PublicKey`](/pkg/crypto/rsa#PublicKey)는 더 이상 모듈러스(modulus) 값이 비밀로 취급된다고 주장하지 않습니다. [`VerifyPKCS1v15`](/pkg/crypto/rsa#VerifyPKCS1v15) 및 [`VerifyPSS`](/pkg/crypto/rsa#VerifyPSS)는 이미 모든 입력값이 공개되어 있으며 유출될 수 있다는 점을 경고했으며, 다른 공개 값들로부터 모듈러스를 복구할 수 있는 수학적 공격 방법들이 존재합니다.

키 생성 속도가 이제 3배 더 빨라졌습니다.

#### [`crypto/sha1`](/pkg/crypto/sha1/)

SHA-NI 명령어를 사용할 수 있는 amd64 환경에서 해싱 속도가 이제 두 배 더 빨라졌습니다.

#### [`crypto/sha3`](/pkg/crypto/sha3/)

새로운 [`SHA3.Clone`](/pkg/crypto/sha3#SHA3.Clone) 메서드는 [`hash.Cloner`](/pkg/hash#Cloner)를 구현합니다.

Apple M 프로세서에서 해싱 속도가 이제 두 배 더 빨라졌습니다.

#### [`crypto/tls`](/pkg/crypto/tls/)

새로운 [`ConnectionState.CurveID`](/pkg/crypto/tls#ConnectionState.CurveID) 필드는 연결을 설정하는 데 사용된 키 교환 메커니즘을 노출합니다.

새로운 [`Config.GetEncryptedClientHelloKeys`](/pkg/crypto/tls#Config.GetEncryptedClientHelloKeys)
콜백을 사용하여, 클라이언트가 Encrypted Client Hello 확장을 보낼 때 서버가 사용할 [`EncryptedClientHelloKey`](/pkg/crypto/tls#EncryptedClientHelloKey)들을 설정할 수 있습니다.

[RFC 9155](https://www.rfc-editor.org/rfc/rfc9155.html)에 따라, 이제 TLS 1.2 핸드쉐이크에서 SHA-1 서명 알고리즘이 허용되지 않습니다.
[GODEBUG 설정](/doc/godebug) `tlssha1=1`을 통해 다시 활성화할 수 있습니다.

[FIPS 140-3 모드](/doc/security/fips140)가 활성화되면, 이제 TLS 1.2에서 Extended Master Secret이 필수적으로 요구되며, Ed25519 및 X25519MLKEM768 사용이 허용됩니다.

이제 TLS 서버는 클라이언트가 가장 선호하는 프로토콜 버전이 아니더라도, 지원되는 가장 높은 프로토콜 버전을 우선적으로 사용합니다.

<!-- CL 687855 -->
이제 TLS 클라이언트와 서버 모두 사양을 더 엄격하게 준수하며, 사양을 벗어난 동작을 더 엄격하게 거부합니다. 규격에 맞는 피어와의 연결은 영향을 받지 않습니다.

#### [`crypto/x509`](/pkg/crypto/x509/)

[`CreateCertificate`](/pkg/crypto/x509#CreateCertificate),
[`CreateCertificateRequest`](/pkg/crypto/x509#CreateCertificateRequest), 및
[`CreateRevocationList`](/pkg/crypto/x509#CreateRevocationList) 함수가 이제
[`crypto.Signer`](/pkg/crypto#Signer)뿐만 아니라
[`crypto.MessageSigner`](/pkg/crypto#MessageSigner) 서명 인터페이스도 허용합니다. 이를 통해 해당 함수들은 호출자가 아닌 서명 작업의 일부로 해싱이 수행되는 "원샷(one-shot)" 서명 인터페이스를 구현하는 서명자를 사용할 수 있습니다.

[`CreateCertificate`](/pkg/crypto/x509#CreateCertificate)는 이제 `SubjectKeyId`가 누락된 경우 이를 채우기 위해 절단된(truncated) SHA-256을 사용합니다.
[GODEBUG 설정](/doc/godebug) `x509sha256skid=0`을 사용하면 SHA-1로 되돌립니다.

[`ParseCertificate`](/pkg/crypto/x509#ParseCertificate)가 이제 음수 `pathLenConstraint`를 포함하는 BasicConstraints 확장이 포함된 인증서를 거부합니다.

[`ParseCertificate`](/pkg/crypto/x509#ParseCertificate)가 이제 ASN.1 T61String 및 BMPString 타입으로 인코딩된 문자열을 더 일관되게 처리합니다. 이로 인해 이전에는 허용되었던 일부 잘못된 형식의 인코딩이 이제 거부될 수 있습니다.

#### [`debug/elf`](/pkg/debug/elf/)

[`debug/elf`](/pkg/debug/elf) 패키지에 RISC-V ELF 파싱을 위한 두 개의 새로운 상수가 추가되었습니다:
- [`PT_RISCV_ATTRIBUTES`](/pkg/debug/elf#PT_RISCV_ATTRIBUTES)
- [`SHT_RISCV_ATTRIBUTES`](/pkg/debug/elf#SHT_RISCV_ATTRIBUTES)

#### [`go/ast`](/pkg/go/ast/)

[`FilterPackage`](/pkg/ast#FilterPackage), [`PackageExports`](/pkg/ast#PackageExports), [`MergePackageFiles`](/pkg/ast#MergePackageFiles) 함수와 [`MergeMode`](/pkg/go/ast#MergeMode) 타입 및 해당 상수들은 모두 deprecated 되었습니다. 이는 오래전에 deprecated 된 [`Object`](/pkg/ast#Object) 및 [`Package`](/pkg/ast#Package) 메커니즘에서만 사용되기 때문입니다.

새로운 [`PreorderStack`](/pkg/go/ast#PreorderStack) 함수는 [`Inspect`](/pkg/go/ast#Inspect)와 마찬가지로 구문 트리(syntax tree)를 순회하며 하위 트리로의 진입 제어 기능을 제공하지만, 편의상 각 지점에서의 상위 노드 스택(stack of enclosing nodes)도 함께 제공합니다.

#### [`go/parser`](/pkg/go/parser/)

[`ParseDir`](/pkg/go/parser#ParseDir) 함수는 더 이상 권장되지 않습니다(deprecated).

#### [`go/token`](/pkg/go/token/)

새로운 [`FileSet.AddExistingFiles`](/pkg/go/token#FileSet.AddExistingFiles) 메서드를 통해 기존의 [`File`](/pkg/go/token#File)들을 [`FileSet`](/pkg/go/token#FileSet)에 추가하거나, 임의의 [`File`](/pkg/go/token#File) 집합에 대한 [`FileSet`](/pkg/go/token#FileSet)을 구성할 수 있으며, 이를 통해 수명이 긴 애플리케이션에서 단일 전역 [`FileSet`](/pkg/go/token#FileSet)과 관련하여 발생하던 문제들을 완화할 수 있습니다.

#### [`go/types`](/pkg/go/types/)

[`Var`](/pkg/go/types#Var)에 변수를 패키지 수준(package-level), 리시버(receiver), 매개변수(parameter), 결과(result), 지역 변수(local variable), 또는 구조체 필드(struct field) 중 하나로 분류하는 [`Var.Kind`](/pkg/go/types#Var.Kind) 메서드가 추가되었습니다.

새로운 [`LookupSelection`](/pkg/go/types#LookupSelection) 함수는 기존의 [`LookupFieldOrMethod`](/pkg/go/types#LookupFieldOrMethod) 함수와 마찬가지로 주어진 이름과 리시버 타입의 필드 또는 메서드를 조회하지만, 그 결과를 [`Selection`](/pkg/go/types#Selection) 형태로 반환합니다.

#### [`hash`](/pkg/hash/)

새로운 [`XOF`](/pkg/hash#XOF) 인터페이스는 [SHAKE](/pkg/crypto/sha3#SHAKE)와 같이 출력 길이가 임의이거나 무제한인 해시 함수인 "확장 가능 출력 함수(extendable output functions)"에 의해 구현될 수 있습니다.

새로운 [`Cloner`](/pkg/hash#Cloner) 인터페이스를 구현하는 Hash는 자신의 상태 복사본을 반환할 수 있습니다.
이제 모든 표준 라이브러리 [`Hash`](/pkg/hash#Hash) 구현체는 [`Cloner`](/pkg/hash#Cloner)를 구현합니다.

#### [`hash/maphash`](/pkg/hash/maphash/)

새로운 [`Hash.Clone`](/pkg/hash/maphash#Hash.Clone) 메서드는 [`hash.Cloner`](/pkg/hash#Cloner)를 구현합니다.

#### [`io/fs`](/pkg/io/fs/)

새로운 [`ReadLinkFS`](/pkg/io/fs#ReadLinkFS) 인터페이스는 파일 시스템에서 심볼릭 링크(symbolic links)를 읽을 수 있는 기능을 제공합니다.

#### [`log/slog`](/pkg/log/slog/)

[`GroupAttrs`](/pkg/log/slog#GroupAttrs)는 [`Attr`](/pkg/log/slog#Attr) 값들의 슬라이스로부터 그룹 [`Attr`](/pkg/log/slog#Attr)를 생성합니다.

[`Record`](/pkg/log/slog#Record)에 이제 [`Source`](/pkg/log/slog#Record.Source) 메서드가 추가되어, 소스 위치를 반환하거나 사용할 수 없는 경우 nil을 반환합니다.

#### [`mime/multipart`](/pkg/mime/multipart/)

새로운 헬퍼 함수인 [`FileContentDisposition`](/pkg/mime/multipart#FileContentDisposition)은 multipart Content-Disposition 헤더 필드를 생성합니다.

#### [`net`](/pkg/net/)

[`LookupMX`](/pkg/net#LookupMX) 및 [`Resolver.LookupMX`](/pkg/net#Resolver.LookupMX)가 이제 유효한 도메인 이름뿐만 아니라 유효한 IP 주소처럼 보이는 DNS 이름도 반환합니다.
이전에는 네임 서버가 DNS 이름으로 IP 주소를 반환하면, RFC 요구 사항에 따라 [`LookupMX`](/pkg/net#LookupMX)가 이를 폐기했습니다.
하지만 실제 네임 서버에서는 때때로 IP 주소를 반환하는 경우가 있습니다.

Windows에서 [`ListenMulticastUDP`](/pkg/net#ListenMulticastUDP)가 이제 IPv6 주소를 지원합니다.

Windows에서 이제 [`os.File`](/pkg/os#File)과 네트워크 연결 간의 변환이 가능해졌습니다. 구체적으로, [`FileConn`](/pkg/net#FileConn), [`FilePacketConn`](/pkg/net#FilePacketConn), [`FileListener`](/pkg/net#FileListener) 함수가 구현되었으며, 열려 있는 파일에 해당하는 네트워크 연결 또는 리스너를 반환합니다. 마찬가지로 [`TCPConn`](/pkg/net#TCPConn.File), [`UDPConn`](/pkg/net#UDPConn.File), [`UnixConn`](/pkg/net#UnixConn.File), [`IPConn`](/pkg/net#IPConn.File), [`TCPListener`](/pkg/net#TCPListener.File), [`UnixListener`](/pkg/net#UnixListener.File)의 `File` 메서드가 구현되어, 네트워크 연결의 기본 [`os.File`](/pkg/os#File)을 반환합니다.

#### [`net/http`](/pkg/net/http/)

새로운 [`CrossOriginProtection`](/pkg/net/http#CrossOriginProtection)은 안전하지 않은 교차 출처(cross-origin) 브라우저 요청을 거부함으로써 [교차 사이트 요청 위조 (CSRF)](https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/CSRF)에 대한 보호 기능을 구현합니다.
이 기능은 [최신 브라우저의 Fetch 메타데이터](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-Fetch-Site)를 사용하며, 토큰이나 쿠키가 필요하지 않고, 출처(origin) 기반 및 패턴 기반의 우회(bypass)를 지원합니다.

#### [`os`](/pkg/os/)

Windows에서 [`NewFile`](/pkg/os#NewFile)은 이제 비동기 I/O를 위해 열린 핸들(즉, [`syscall.CreateFile`](/pkg/syscall#CreateFile) 호출 시 [`syscall.FILE_FLAG_OVERLAPPED`](/pkg/syscall#FILE_FLAG_OVERLAPPED)가 지정된 경우)을 지원합니다. 이러한 핸들은 Go 런타임의 I/O 완료 포트(I/O completion port)와 연결되며, 결과적으로 생성된 [`File`](/pkg/os#File)에 다음과 같은 이점을 제공합니다.

- I/O 메서드([`File.Read`](/pkg/os#File.Read), [`File.Write`](/pkg/os#File.Write), [`File.ReadAt`](/pkg/os#File.ReadAt), [`File.WriteAt`](/pkg/os#File.WriteAt))는 OS 스레드를 차단(block)하지 않습니다.
- Deadline 메서드([`File.SetDeadline`](/pkg/os#File.SetDeadline), [`File.SetReadDeadline`](/pkg/os#File.SetReadDeadline), [`File.SetWriteDeadline`](/pkg/os#File.SetWriteDeadline))가 지원됩니다.

이 개선 사항은 특히 Windows에서 이름 있는 파이프(named pipes)를 통해 통신하는 애플리케이션에 유용합니다.

핸들은 한 번에 하나의 완료 포트(completion port)와만 연결될 수 있다는 점에 유의하십시오.
[`NewFile`](/pkg/os#NewFile)에 제공된 핸들이 이미 완료 포트와 연결되어 있는 경우, 반환되는 [`File`](/pkg/os#File)은 동기 I/O 모드로 다운그레이드됩니다.
이 경우, I/O 메서드는 OS 스레드를 블록하며, deadline 메서드는 아무런 영향을 주지 않습니다.

[`DirFS`](/pkg/os#DirFS) 및 [`Root.FS`](/pkg/os#Root.FS)가 반환하는 파일 시스템은 새로운 [`io/fs.ReadLinkFS`](/pkg/io/fs#ReadLinkFS) 인터페이스를 구현합니다.
[`CopyFS`](/pkg/os#CopyFS)는 [`io/fs.ReadLinkFS`](/pkg/io/fs#ReadLinkFS)를 구현하는 파일 시스템을 복사할 때 심볼릭 링크를 지원합니다.

[`Root`](/pkg/os#Root) 타입은 다음과 같은 추가 메서드들을 지원합니다:

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

<!-- go.dev/issue/73126는 67002의 일부로 문서화되었습니다 -->

#### [`reflect`](/pkg/reflect/)

새로운 [`TypeAssert`](/pkg/reflect#TypeAssert) 함수를 사용하면 [`Value`](/pkg/reflect#Value)를 지정된 타입의 Go 값으로 직접 변환할 수 있습니다. 이는 [`Value.Interface`](/pkg/reflect#Value.Interface)의 결과에 타입 단언(type assertion)을 사용하는 것과 비슷하지만, 불필요한 메모리 할당을 피할 수 있다는 장점이 있습니다.

#### [`regexp/syntax`](/pkg/regexp/syntax/)

`\p{name}` 및 `\P{name}` 문자 클래스 구문에서 이제 Any, ASCII, Assigned, Cn, LC라는 이름뿐만 아니라 `\pL`에 대한 `\p{Letter}`와 같은 Unicode 카테고리 별칭을 사용할 수 있습니다. [Unicode TR18](https://unicode.org/reports/tr18/)에 따라, 이제 대소문자를 구분하지 않고 공백, 언더바(_), 하이픈(-)을 무시하는 이름 조회를 사용합니다.

#### [`runtime`](/pkg/runtime/)

[`AddCleanup`](/pkg/runtime#AddCleanup)에 의해 예약된 정리(Cleanup) 함수들이 이제 동시적(concurrently)이고 병렬적(in parallel)으로 실행되어, [`unique`](/pkg/unique) 패키지와 같이 사용량이 많은 경우에도 정리 기능을 더 효율적으로 사용할 수 있게 되었습니다. 다만, 개별 정리 함수가 실행 시간이 길거나 차단(block)될 가능성이 있는 경우, 정리 큐를 차단하지 않도록 여전히 새로운 goroutine으로 작업을 위임해야 한다는 점에 유의하십시오.

새로운 `GODEBUG=checkfinalizers=1` 설정은 [GC 가이드](/doc/gc-guide#Finalizers_cleanups_and_weak_pointers)에 설명된 것과 같이 파이널라이저(finalizers) 및 정리(cleanups)와 관련된 일반적인 문제를 찾는 데 도움이 됩니다. 이 모드에서 런타임은 각 가비지 컬렉션 사이클마다 진단을 수행하며, 실행 시간이 긴 파이널라이저 또는 정리 작업으로 인한 문제를 식별할 수 있도록 파이널라이저 및 정리 큐의 길이를 stderr로 정기적으로 보고합니다. 자세한 내용은 [GODEBUG 문서](https://pkg.go.dev/runtime#hdr-Environment_Variables)를 참조하십시오.

새로운 [`SetDefaultGOMAXPROCS`](/pkg/runtime#SetDefaultGOMAXPROCS) 함수는 `GOMAXPROCS` 환경 변수가 설정되지 않은 것처럼 `GOMAXPROCS`를 런타임 기본값으로 설정합니다. 이는 `GOMAXPROCS` 환경 변수나 이전의 [`GOMAXPROCS`](/pkg/runtime#GOMAXPROCS) 호출로 인해 비활성화된 경우, [새로운 `GOMAXPROCS` 기본값](#container-aware-gomaxprocs)을 활성화하는 데 유용합니다.

#### [`runtime/pprof`](/pkg/runtime/pprof/)

런타임 내부 락(runtime-internal locks)의 경합에 대한 뮤텍스 프로필(mutex profile)이 이제 지연을 유발한 임계 구역(critical section)의 끝 지점을 정확하게 가리킵니다. 이는 `sync.Mutex` 값의 경합에 대한 프로필 동작과 일치합니다. 프로필의 이 부분에 대해 Go 1.22부터 1.24까지의 특이한 동작을 선택적으로 사용할 수 있게 했던 `GODEBUG` 설정인 `runtimecontentionstacks`는 이제 제거되었습니다.

#### [`sync`](/pkg/sync/)

새로운 [`WaitGroup.Go`](/pkg/sync#WaitGroup.Go) 메서드는 고루틴을 생성하고 개수를 세는 일반적인 패턴을 더 편리하게 만들어 줍니다.

#### [`testing`](/pkg/testing/)

새로운 메서드 [`T.Attr`](/pkg/testing#T.Attr), [`B.Attr`](/pkg/testing#B.Attr), 그리고 [`F.Attr`](/pkg/testing#F.Attr)는 테스트 로그에 속성(attribute)을 출력합니다. 속성은 테스트와 연관된 임의의 키(key)와 값(value)입니다.

예를 들어, `TestF`라는 이름의 테스트에서
`t.Attr("key", "value")`는 다음과 같이 출력합니다:

```
=== ATTR  TestF key value
```

`-json` 플래그를 사용하면, 속성(attributes)이 새로운 "attr" 액션으로 표시됩니다.

<!-- go.dev/issue/59928 -->

[`T`](/pkg/testing#T), [`B`](/pkg/testing#B) 및 [`F`](/pkg/testing#F)의 새로운 [`Output`](/pkg/testing#T.Output) 메서드는 [`TB.Log`](/pkg/testing#TB.Log)와 동일한 테스트 출력 스트림에 기록하는 [`io.Writer`](/pkg/io#Writer)를 제공합니다.
`TB.Log`와 마찬가지로 출력 결과에 들여쓰기가 적용되지만, 파일 이름과 라인 번호는 포함되지 않습니다.

<!-- https://go.dev/issue/70464, CL 630137 -->
이제 병렬 테스트가 실행 중인 경우 [`AllocsPerRun`](/pkg/testing#AllocsPerRun) 함수가 패닉(panic)을 발생시킵니다.
다른 테스트가 실행 중일 때 [`AllocsPerRun`](/pkg/testing#AllocsPerRun)의 결과는 본질적으로 불안정(flaky)합니다.
새로 도입된 패닉 동작은 이러한 버그를 찾는 데 도움이 됩니다.

#### [`testing/fstest`](/pkg/testing/fstest/)

[`MapFS`](/pkg/testing/fstest#MapFS)는 새로운 [`io/fs.ReadLinkFS`](/pkg/io/fs#ReadLinkFS) 인터페이스를 구현합니다.
[`TestFS`](/pkg/testing/fstest#TestFS)는 [`io/fs.ReadLinkFS`](/pkg/io/fs#ReadLinkFS) 인터페이스가 구현된 경우 해당 기능을 검증합니다.
[`TestFS`](/pkg/testing/fstest#TestFS)는 무제한 재귀를 방지하기 위해 더 이상 심볼릭 링크를 따라가지 않습니다.

#### [`unicode`](/pkg/unicode/)

새로운 [`CategoryAliases`](/pkg/unicode#CategoryAliases) 맵은 “L”에 대한 “Letter”와 같은 카테고리 별칭 이름에 대한 접근을 제공합니다.

새로운 카테고리인 [`Cn`](/pkg/unicode#Cn)과 [`LC`](/pkg/unicode#LC)는 각각 할당되지 않은 코드 포인트(unassigned codepoints)와 대소문자 구분이 있는 문자(cased letters)를 정의합니다.
이들은 항상 Unicode에서 정의되어 있었으나, 이전 버전의 Go에서 실수로 누락되었습니다.
이제 [`C`](/pkg/unicode#C) 카테고리에 [`Cn`](/pkg/unicode#Cn)이 포함되어, 모든 할당되지 않은 코드 포인트가 추가되었습니다.

#### [`unique`](/pkg/unique/)

[`unique`](/pkg/unique) 패키지가 이제 인턴(interned)된 값들을 더 적극적이고 효율적이며 병렬적으로 회수합니다. 그 결과, [`Make`](/pkg/unique#Make)를 사용하는 애플리케이션에서 실제로 고유한 값들이 많이 인턴될 때 메모리가 급격히 증가하는 현상이 발생할 가능성이 줄어들었습니다.

[`Handle`](/pkg/unique#Handle)를 포함하여 [`Make`](/pkg/unique#Make)에 전달된 값들은 이전에는 [`Handle`](/pkg/unique#Handle) 값 체인의 깊이에 비례하여 이를 수집하는 데 여러 번의 가비지 컬렉션 사이클이 필요했습니다. 이제 사용되지 않는 값들은 단 한 번의 사이클에서 즉시 수집됩니다.

## 포트 {#ports}

### Darwin

<!-- go.dev/issue/69839 -->
Go 1.24 릴리스 노트에서 [공지](/doc/go1.24#darwin)한 바와 같이, Go 1.25는 macOS 12 Monterey 또는 그 이후 버전을 요구합니다.
이전 버전에 대한 지원은 중단되었습니다.

### Windows

<!-- go.dev/issue/71671 -->
Go 1.25은 [결함이 있는](/doc/go1.24#windows) 32비트 windows/arm 포트(`GOOS=windows` `GOARCH=arm`)를 포함하는 마지막 릴리스입니다. 해당 포트는 Go 1.26에서 제거될 예정입니다.

### AMD64

<!-- go.dev/issue/71204 -->
`GOAMD64=v3` 이상의 모드에서, 컴파일러는 부동 소수점 연산을 더 빠르고 정확하게 만들기 위해 융합 곱셈-덧셈(fused multiply-add) 명령어를 사용합니다. 이로 인해 프로그램이 생성하는 정확한 부동 소수점 값이 변경될 수 있습니다.

융합(fusing)을 방지하려면 `float64(a*b)+c`와 같이 명시적인 `float64` 캐스팅을 사용하세요.

### Loong64

<!-- CLs 533717, 533716, 543316, 604176 -->
이제 linux/loong64 포트에서 레이스 디텍터(race detector)를 지원하며, [`runtime.SetCgoTraceback`](/pkg/runtime#SetCgoTraceback)을 사용하여 C 코드로부터 트레이스백(traceback) 정보를 수집하고, 내부 링크 모드(internal link mode)로 cgo 프로그램을 링크하는 기능이 지원됩니다.

### RISC-V

<!-- CL 420114 -->
이제 linux/riscv64 포트에서 `plugin` 빌드 모드를 지원합니다.

<!-- https://go.dev/issue/61476, CL 633417 -->
`GORISCV64` 환경 변수에서 이제 새로운 값인 `rva23u64`를 사용할 수 있으며, 이는 RVA23U64 사용자 모드 애플리케이션 프로필을 선택합니다.

<!--
2025-05-23에 생성 및 검토된 relnote todo의 출력 결과와 버그/CL의 요약 정보입니다. -->

<!-- Go 1.25 릴리스 노트에 언급될 필요는 없으나 relnote todo에 의해 수집된 항목들
오래된 제안서들 업데이트 중
accepted proposal https://go.dev/issue/30999 (from https://go.dev/cl/671795)
accepted proposal https://go.dev/issue/36532 (from https://go.dev/cl/647555)
accepted proposal https://go.dev/issue/48429 (from https://go.dev/cl/648577)
accepted proposal https://go.dev/issue/51572 (from https://go.dev/cl/651996)
accepted proposal https://go.dev/issue/51430 (from https://go.dev/cl/644997, https://go.dev/cl/646355)
accepted proposal https://go.dev/issue/60905 (from https://go.dev/cl/645795)
accepted proposal https://go.dev/issue/61716 (from https://go.dev/cl/644475)
accepted proposal https://go.dev/issue/64876 (from https://go.dev/cl/649435)
accepted proposal https://go.dev/issue/70123 (from https://go.dev/cl/657116)
accepted proposal https://go.dev/issue/61901 (from https://go.dev/cl/647875)
accepted proposal https://go.dev/issue/64207 (from https://go.dev/cl/647015, https://go.dev/cl/652235)
accepted proposal https://go.dev/issue/70200 (from https://go.dev/cl/674916) -->

subrepos의 경우:
승인된 제안 https://go.dev/issue/53757 (출처: https://go.dev/cl/644575)
승인된 제안 https://go.dev/issue/54743 (출처: https://go.dev/cl/532415)
승인된 제안 https://go.dev/issue/57792 (출처: https://go.dev/cl/649716, https://go.dev/cl/651737)
승인된 제안 https://go.dev/issue/58523 (출처: https://go.dev/cl/538235)
승인된 제안 https://go.dev/issue/61537 (출처: https://go.dev/cl/531935)
승인된 제안 https://go.dev/issue/61940 (출처: https://go.dev/cl/650235)
승인된 제안 https://go.dev/issue/67839 (출처: https://go.dev/cl/646535)
승인된 제안 https://go.dev/issue/68780 (출처: https://go.dev/cl/659835)
승인된 제안 https://go.dev/issue/69095 (출처: https://go.dev/cl/649320, https://go.dev/cl/649321, https://go.dev/cl/649337, https://go.dev/cl/649376, https://go.dev/cl/649377, https://go.dev/cl/649378, https://go.dev/cl/649379, https://go.dev/cl/649380, https://go.dev/cl/649397, https://go.dev/cl/649398, https://go.dev/cl/649419, https://go.dev/cl/649497, https://go.dev/cl/649498, https://go.dev/cl/649618, https://go.dev/cl/649675, https://go.dev/cl/649676, https://go.dev/cl/649677, https://go.dev/cl/649695, https://go.dev/cl/649696, https://go.dev/cl/649697, https://go.dev/cl/649698, https://go.dev/cl/649715, https://go.dev/cl/649717, https://go.dev/cl/649718, https://go.dev/cl/649755, https://go.dev/cl/649775, https://go.dev/cl/649795, https://go.dev/cl/649815, https://go.dev/cl/649835, https://go.dev/cl/651336, https://go.dev/cl/651736, https://go.dev/cl/651737, https://go.dev/cl/658018)
승인된 제안 https://go.dev/issue/70859 (출처: https://go.dev/cl/666056, https://go.dev/cl/670835, https://go.dev/cl/672015, https://go.dev/cl/672016, https://go.dev/cl/672017)
승인된 제안 https://go.dev/issue/32816 (출처: https://go.dev/cl/645155, https://go.dev/cl/645455, https://go.dev/cl/645955, https://go.dev/cl/646255, https://go.dev/cl/646455, https://go.dev/cl/646495, https://go.dev/cl/646655, https://go.dev/cl/646875, https://go.dev/cl/647298, https://go.dev/cl/647299, https://go.dev/cl/647736, https://go.dev/cl/648581, https://go.dev/cl/648715, https://go.dev/cl/648976, https://go.dev/cl/648995, https://go.dev/cl/649055, https://go.dev/cl/649056, https://go.dev/cl/649057, https://go.dev/cl/649456, https://go.dev/cl/649476, https://go.dev/cl/650755, https://go.dev/cl/651615, https://go.dev/cl/651617, https://go.dev/cl/651655, https://go.dev/cl/653436)
-->
[cross-site request forgery (csrf)]: https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/CSRF
[sec-fetch-site]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-Fetch-Site
