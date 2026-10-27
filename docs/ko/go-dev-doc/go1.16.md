<!--
참고: 이 문서와 이 디렉토리의 다른 문서들에서는
`hello` `world`와 같이 고정폭 구절을 비고정폭 공백으로 설정하는
관례를 따릅니다.
이러한 구절에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

<style>
  main ul li { margin: 0.5em 0; }
</style>

## Go 1.16 소개 {#introduction}

최신 Go 릴리스인 버전 1.16가 [Go 1.15](/doc/go1.15) 출시 6개월 만에 공개되었습니다.
변경 사항의 대부분은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언제나 그렇듯, 이번 릴리스에서도 Go 1 [호환성 약속](/doc/go1compat.html)을 유지합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 기대합니다.

## 언어 변경 사항 {#language}

제공해주신 내용이 없어 번역할 텍스트가 없습니다. 번역이 필요한 영문 Markdown 내용을 제공해 주시면, 요청하신 지침에 따라 정교하게 한국어로 번역해 드리겠습니다.

## 포트 {#ports}

### Darwin 및 iOS {#darwin}

<!-- golang.org/issue/38485, golang.org/issue/41385, CL 266373, more CLs -->
Go 1.16은 `GOOS=darwin`, `GOARCH=arm64`를 통해 macOS(Apple Silicon으로도 알려짐)의 64비트 ARM 아키텍처 지원을 추가합니다.
`darwin/amd64` 포트와 마찬가지로, `darwin/arm64` 포트는 cgo, 내부 및 외부 링킹, `c-archive`, `c-shared`, `pie` 빌드 모드 및 race detector를 지원합니다.

<!-- CL 254740 -->
이전에 `darwin/arm64`였던 iOS 포트가 `ios/arm64`로 이름이 변경되었습니다. `GOOS=android`가 `linux` 빌드 태그를 암시하는 것과 마찬가지로, `GOOS=ios`는 `darwin` 빌드 태그를 암시합니다. 이 변경 사항은 gomobile을 사용하여 iOS 앱을 빌드하는 모든 사용자에게 투명하게 적용될 것입니다.

`GOOS=ios`가 도입됨에 따라 `x_ios.go`와 같은 파일 이름은 이제 `GOOS=ios`일 때만 빌드됩니다. 자세한 내용은 [`go` `help` `buildconstraint`](/cmd/go/#hdr-Build_constraints)를 참조하십시오. 이러한 형태의 파일 이름을 사용하는 기존 패키지들은 파일 이름을 변경해야 합니다.

<!-- golang.org/issue/42100, CL 263798 -->
Go 1.16에서는 AMD64 기반 macOS에서 실행되는 iOS 시뮬레이터를 대상으로 하는 `ios/amd64` 포트가 추가되었습니다. 이전에는 `ios` 빌드 태그를 설정한 `darwin/amd64`를 통해 비공식적으로 지원되었습니다. iOS 및 iOS 시뮬레이터용 프로그램 빌드 방법에 대한 자세한 내용은 [`misc/ios/README`](/misc/ios/README)를 참조하십시오.

<!-- golang.org/issue/23011 -->
Go 1.16은 macOS 10.12 Sierra에서 실행되는 마지막 릴리스입니다.
Go 1.17부터는 macOS 10.13 High Sierra 또는 그 이후 버전이 필요합니다.

### NetBSD {#netbsd}

<!-- golang.org/issue/30824 -->
Go는 이제 NetBSD의 64비트 ARM 아키텍처(`netbsd/arm64` 포트)를 지원합니다.

### OpenBSD {#openbsd}

<!-- golang.org/issue/40995 -->
이제 Go가 OpenBSD의 MIPS64 아키텍처(`openbsd/mips64` 포트)를 지원합니다. 이 포트는 아직 cgo를 지원하지 않습니다.

<!-- golang.org/issue/36435, many CLs -->
OpenBSD의 64비트 x86 및 64비트 ARM 아키텍처(`openbsd/amd64` 및 `openbsd/arm64` 포트)에서, 이제 시스템 호출은 `SYSCALL`/`SVC` 명령어를 직접 사용하는 대신 `libc`를 통해 이루어집니다. 이는 향후 OpenBSD 버전과의 전방 호환성을 보장하기 위함입니다. 특히, OpenBSD 6.9 버전부터는 정적 링크되지 않은 Go 바이너리의 경우 반드시 `libc`를 통해 시스템 호출을 수행해야 합니다.

### 386 {#386}

<!-- golang.org/issue/40255, golang.org/issue/41848, CL 258957, and CL 260017 -->
Go 1.15 릴리스 노트에서 [공지](go1.15#386)한 바와 같이,
Go 1.16부터는 x87 모드 컴파일(`GO386=387`) 지원이 중단됩니다.
SSE2를 지원하지 않는 프로세서에 대한 지원은 이제 소프트 플로트(soft float)
모드(`GO386=softfloat`)를 통해 제공됩니다.
SSE2 미지원 프로세서를 사용하는 사용자는 `GO386=387`을
`GO386=softfloat`로 변경해야 합니다.

### RISC-V {#riscv}

<!-- golang.org/issue/36641, CL 267317 -->
`linux/riscv64` 포트가 이제 cgo와 `-buildmode=pie`를 지원합니다. 이번 릴리스에는 RISC-V를 위한 성능 최적화 및 코드 생성 개선 사항이 포함되어 있습니다.

## 도구 {#tools}

### Go 커맨드 {#go-command}

#### 모듈 {#modules}

<!-- golang.org/issue/41330 -->
현재 작업 디렉터리나 상위 디렉터리에 `go.mod` 파일이 있는지 여부와 관계없이, 모듈 인식(Module-aware) 모드가 기본적으로 활성화됩니다. 더 정확하게는, `GO111MODULE` 환경 변수의 기본값이 이제 `on`으로 설정됩니다. 이전 동작으로 전환하려면 `GO111MODULE`을 `auto`로 설정하십시오.

<!-- golang.org/issue/40728 -->
`go build` 및 `go test`와 같은 빌드 명령은 더 이상 기본적으로 `go.mod`와 `go.sum`을 수정하지 않습니다. 대신, 모듈 요구 사항이나 체크섬을 추가 또는 업데이트해야 하는 경우 에러를 보고합니다 (`-mod=readonly` 플래그를 사용한 것과 동일). 모듈 요구 사항 및 합계는 `go mod tidy` 또는 `go get`으로 조정할 수 있습니다.

<!-- golang.org/issue/40276 -->
이제 `go` `install`은 버전 접미사가 포함된 인수를 허용합니다 (예: `go` `install` `example.com/cmd@v1.0.0`). 이 경우 `go` `install`은 모듈 인식(module-aware) 모드로 패키지를 빌드하고 설치하며, 현재 디렉토리나 상위 디렉토리에 `go.mod` 파일이 있더라도 이를 무시합니다. 이는 메인 모듈의 의존성에 영향을 주지 않고 실행 파일을 설치할 때 유용합니다.

<!-- golang.org/issue/40276 -->
(위에서 설명한 대로) 버전 접미사 유무와 상관없이 `go` `install`을 사용하는 것이 이제 모듈 모드에서 패키지를 빌드하고 설치하는 권장 방법입니다. `go` `get`은 패키지를 빌드하지 않고 현재 모듈의 의존성을 조정하기 위해 `-d` 플래그와 함께 사용해야 하며, 패키지를 빌드하고 설치하기 위해 `go` `get`을 사용하는 것은 더 이상 권장되지 않습니다(deprecated). 향후 릴리스에서는 `-d` 플래그가 항상 활성화될 예정입니다.

<!-- golang.org/issue/24031 -->
이제 `go.mod` 파일에서 `retract` 지시문을 사용하여, 게시된 모듈의 특정 버전이 다른 모듈에 의해 사용되지 않아야 함을 나타낼 수 있습니다. 모듈 작성자는 심각한 문제가 발견되었거나 버전이 의도치 않게 게시된 경우 해당 버전을 철회(retract)할 수 있습니다.

<!-- golang.org/issue/26603 -->
이제 `go` `mod` `vendor` 및 `go` `mod` `tidy` 하위 명령에서 `-e` 플래그를 사용할 수 있습니다. 이 플래그는 누락된 패키지를 해결하는 과정에서 오류가 발생하더라도 계속 진행하도록 지시합니다.

<!-- golang.org/issue/36465 -->
이제 `go` 명령어는 메인 모듈의 `exclude` 지시문에 의해 제외된 모듈 버전의 요구 사항을 무시합니다. 이전에는 `go` 명령어가 제외된 버전보다 더 높은 다음 버전을 사용했으나, 해당 버전이 시간이 지남에 따라 변경될 수 있어 빌드 재현성(non-reproducible builds) 문제가 발생할 수 있었습니다.

<!-- golang.org/issue/43052, golang.org/issue/43985 -->
모듈 모드에서 `go` 명령어는 이제 비-ASCII 문자나 점(`.`)으로 시작하는 경로 요소가 포함된 임포트 경로를 허용하지 않습니다. 이러한 문자가 포함된 모듈 경로는 이미 금지되어 있었으므로([모듈 경로 및 버전](/ref/mod#go-mod-file-ident) 참조), 이번 변경 사항은 모듈 하위 디렉토리 내의 경로에만 영향을 미칩니다.

#### 파일 임베딩 {#embed}

이제 `go` 명령은 새로운 `//go:embed` 지시어를 사용하여 정적 파일과 파일 트리를 최종 실행 파일의 일부로 포함하는 기능을 지원합니다. 자세한 내용은 새로운 [`embed`](/pkg/embed/) 패키지 문서를 참조하십시오.

#### `go` `test` {#go-test}

<!-- golang.org/issue/29062 -->
`go` `test`를 사용할 때, 테스트 함수 실행 중에 `os.Exit(0)`을 호출하는 테스트는 이제 실패한 것으로 간주됩니다.
이는 테스트가 `os.Exit(0)`을 호출하는 코드를 실행하여 이후의 모든 테스트가 중단되는 경우를 찾아내는 데 도움이 됩니다.
만약 `TestMain` 함수가 `os.Exit(0)`을 호출하는 경우에는 여전히 통과한 테스트로 간주됩니다.

<!-- golang.org/issue/39484 -->
`go` `test` 명령에서 `-c` 또는 `-i` 플래그를 알 수 없는 플래그와 함께 사용할 때 에러가 보고됩니다. 일반적으로 알 수 없는 플래그는 테스트로 전달되지만, `-c` 또는 `-i`가 사용되면 테스트가 실행되지 않습니다.

#### `go` `get` {#go-get}

<!-- golang.org/issue/37519 -->
`go` `get` `-insecure` 플래그는 더 이상 사용되지 않으며(deprecated) 향후 버전에서 제거될 예정입니다. 이 플래그는 HTTP와 같은 보안되지 않은 스킴(scheme)을 사용하여 리포지토리에서 가져오거나 커스텀 도메인을 해석하는 것을 허용하며, 체크섬 데이터베이스를 통한 모듈 합계(sum) 검증을 우회합니다. 보안되지 않은 스킴의 사용을 허용하려면 대신 `GOINSECURE` 환경 변수를 사용하십시오. 모듈 합계 검증을 우회하려면 `GOPRIVATE` 또는 `GONOSUMDB`를 사용하십시오.
자세한 내용은 `go` `help` `environment`를 참조하십시오.

<!-- golang.org/cl/263267 -->
이제 `go` `get` `example.com/mod@patch`를 사용하려면 메인 모듈에서 `example.com/mod`의 특정 버전이 이미 요구(required)되고 있어야 합니다.
(단, `go` `get` `-u=patch`는 새로 추가된 의존성에 대해서도 계속해서 패치를 적용합니다.)

#### `GOVCS` 환경 변수 {#govcs}

<!-- golang.org/issue/266420 -->
`GOVCS`는 `go` 명령어가 소스 코드를 다운로드하는 데 사용할 수 있는 버전 관리 도구를 제한하는 새로운 환경 변수입니다. 이는 일반적으로 신뢰할 수 있고 인증된 환경에서 사용되는 도구들과 관련된 보안 문제를 완화합니다. 기본적으로 `git`과 `hg`는 모든 저장소에서 코드를 다운로드하는 데 사용할 수 있습니다. `svn`, `bzr`, `fossil`은 `GOPRIVATE` 환경 변수의 패턴과 일치하는 모듈 경로 또는 패키지 경로를 가진 저장소에서만 코드를 다운로드하는 데 사용할 수 있습니다. 자세한 내용은 [`go` `help` `vcs`](/cmd/go/#hdr-Controlling_version_control_with_GOVCS)를 참조하십시오.

#### `all` 패턴 {#all-pattern}

<!-- golang.org/cl/240623 -->
메인 모듈의 `go.mod` 파일이 `go` `1.16` 이상을 선언하는 경우, `all` 패키지 패턴은 이제 메인 모듈에서 발견된 패키지 또는 테스트에 의해 전이적으로(transitively) 임포트된 패키지만과 일치합니다. (메인 모듈에서 임포트한 패키지의 _테스트에서_ 임포트한 패키지는 더 이상 포함되지 않습니다.) 이는 Go 1.11 이후 `go` `mod` `vendor`가 유지해 온 패키지 집합과 동일합니다.

#### `-toolexec` 빌드 플래그 {#toolexec}

<!-- golang.org/cl/263357 -->
`compile` 또는 `asm`과 같은 툴체인 프로그램을 호출할 때 특정 프로그램을 사용하도록 `-toolexec` 빌드 플래그가 지정되면, 이제 환경 변수 `TOOLEXEC_IMPORTPATH`에 빌드 중인 패키지의 import 경로가 설정됩니다.

#### `-i` 빌드 플래그 {#i-flag}

<!-- golang.org/issue/41696 -->
`go` `build`, `go` `install`, 및 `go` `test`에서 사용되던 `-i` 플래그가 이제 deprecated 되었습니다. `-i` 플래그는 `go` 명령어로 하여금 커맨드 라인에 명시된 패키지들이 임포트하는 패키지들을 설치하도록 지시합니다. Go 1.10에서 빌드 캐시가 도입된 이후, `-i` 플래그는 더 이상 빌드 시간에 유의미한 영향을 주지 않으며, 설치 디렉토리에 쓰기 권한이 없는 경우 오류를 발생시킵니다.

#### `list` 명령 {#list-buildid}

<!-- golang.org/cl/263542 -->
`-export` 플래그가 지정되면, 이제 `BuildID` 필드에 컴파일된 패키지의 빌드 ID가 설정됩니다. 이는 `go` `list` `-exported` `-f` `{{.Export}}` 결과에 대해 `go` `tool` `buildid`를 실행하는 것과 동일하지만, 추가 단계가 필요하지 않습니다.

#### `-overlay` 플래그 {#overlay-flag}

<!-- golang.org/issue/39958 -->
`-overlay` 플래그는 파일 경로 교체 세트를 포함하는 JSON 설정 파일을 지정합니다. `-overlay` 플래그는 모든 빌드 명령 및 `go` `mod` 하위 명령과 함께 사용할 수 있습니다.
이 플래그는 주로 gopls와 같은 에디터 도구가 저장되지 않은 소스 파일 변경 사항의 영향을 파악하기 위해 사용하도록 설계되었습니다. 설정 파일은 실제 파일 경로를 교체 파일 경로에 매핑하며, `go` 명령 및 해당 빌드는 실제 파일 경로가 교체 파일 경로에 지정된 내용으로 존재하는 것처럼, 또는 교체 파일 경로가 비어 있는 경우 실제 파일 경로가 존재하지 않는 것처럼 실행됩니다.

### Cgo {#cgo}

<!-- CL 252378 -->
[cgo](/cmd/cgo) 도구는 C 구조체 비트 필드(bitfields)의 크기가 Go에서 표현 가능하더라도, 이를 더 이상 Go 구조체 필드로 변환하려 시도하지 않습니다. C 비트 필드가 메모리에 배치되는 순서는 구현 방식에 따라 다르기 때문에, 일부 경우에 cgo 도구가 명시적인 오류 없이 잘못된 결과를 생성했습니다.

### Vet {#vet}

#### 고루틴 내의 잘못된 testing.T 사용에 대한 새로운 경고 {#vet-testing-T}

<!-- CL 235677 -->
이제 vet 도구는 테스트 중에 생성된 고루틴(goroutine) 내부에서 `testing.T` 메서드인 `Fatal`을 잘못 호출하는 경우 경고를 표시합니다.
이는 `testing.T` 테스트 또는 `testing.B` 벤치마크에서 `Fatalf`, `FailNow`, 그리고 `Skip{,f,Now}` 메서드를 호출하는 경우에도 마찬가지로 경고를 표시합니다.

이 메서드들을 호출하면 `Test*` 또는 `Benchmark*` 함수가 아니라 생성된 goroutine의 실행이 중단됩니다. 따라서 이 메서드들은 테스트나 벤치마크 함수를 실행 중인 goroutine에서 [호출되어야 합니다](/pkg/testing/#T.FailNow). 예를 들어:

```go
func TestFoo(t *testing.T) {
	    go func() {
	        if condition() {
	            t.Fatal("oops") // 이는 TestFoo 대신 내부 함수를 종료시킵니다.
	        }
	        ...
	    }()
	}
```

생성된 goroutine에서 `t.Fatal`(또는 이와 유사한 메서드)을 호출하는 코드는 `t.Error`를 사용하여 테스트 실패를 알리고, `return` 문과 같은 대체 방법을 사용하여 goroutine을 조기에 종료하도록 재작성해야 합니다. 이전 예제는 다음과 같이 재작성할 수 있습니다.

```go
func TestFoo(t *testing.T) {
	    go func() {
	        if condition() {
	            t.Error("oops")
	            return
	        }
	        ...
	    }()
	}
```

#### 프레임 포인터에 대한 새로운 경고 {#vet-frame-pointer}

<!-- CL 248686, CL 276372 -->
이제 vet 도구는 호출 규약(calling convention)과 달리 BP 레지스터(프레임 포인터)를 저장하고 복원하지 않은 채 덮어쓰는 amd64 어셈블리에 대해 경고를 표시합니다. BP 레지스터를 보존하지 않는 코드는 BP를 전혀 사용하지 않도록 수정하거나, 저장 및 복원을 통해 BP를 보존하도록 수정해야 합니다. BP를 보존하는 쉬운 방법은 프레임 크기를 0이 아닌 값으로 설정하는 것이며, 이렇게 하면 생성된 prologue와 epilogue가 자동으로 BP 레지스터를 보존해 줍니다.
수정 예시는 [CL 248260](/cl/248260)을 참조하십시오.

#### asn1.Unmarshal에 대한 새로운 경고 {#vet-asn1-unmarshal}

<!-- CL 243397 -->
이제 vet 도구는 [`asn1.Unmarshal`](/pkg/encoding/asn1/#Unmarshal)에 포인터가 아니거나 nil인 인수를 잘못 전달했을 때 경고를 표시합니다.
이는 [`encoding/json.Unmarshal`](/pkg/encoding/json/#Unmarshal) 및 [`encoding/xml.Unmarshal`](/pkg/encoding/xml/#Unmarshal)에 대한 기존 검사와 유사합니다.

## Runtime {#runtime}

새로운 [`runtime/metrics`](/pkg/runtime/metrics/) 패키지는 Go 런타임에서 구현 정의 메트릭(implementation-defined metrics)을 읽기 위한 안정적인 인터페이스를 제공합니다. 이 패키지는 [`runtime.ReadMemStats`](/pkg/runtime/#ReadMemStats) 및 [`debug.GCStats`](/pkg/runtime/debug/#GCStats)와 같은 기존 함수들을 대체하며, 훨씬 더 일반적이고 효율적입니다. 자세한 내용은 패키지 문서를 참조하십시오.

<!-- CL 254659 -->
`GODEBUG` 환경 변수를 `inittrace=1`로 설정하면 이제 런타임이 각 패키지의 `init`에 대해 표준 에러로 한 줄의 내용을 출력하며, 실행 시간과 메모리 할당량을 요약하여 보여줍니다. 이 트레이스는 Go 시작 성능의 병목 지점이나 성능 저하(regression)를 찾는 데 사용할 수 있습니다.
[`GODEBUG`
문서](/pkg/runtime/#hdr-Environment_Variables)에서 해당 형식을 확인할 수 있습니다.

<!-- CL 267100 -->
Linux에서 런타임은 이제 운영체제가 메모리 압박을 받을 때 지연해서 메모리를 해제하는 방식(`MADV_FREE` 사용) 대신, 즉시 운영체제로 메모리를 해제하는 방식(`MADV_DONTNEED` 사용)을 기본값으로 사용합니다. 이는 RSS와 같은 프로세스 수준의 메모리 통계가 Go 프로세스에서 사용 중인 물리 메모리 양을 더 정확하게 반영하게 됨을 의미합니다. 메모리 모니터링 동작을 개선하기 위해 현재 `GODEBUG=madvdontneed=1`을 사용 중인 시스템은 더 이상 이 환경 변수를 설정할 필요가 없습니다.

<!-- CL 220419, CL 271987 -->
Go 1.16은 레이스 디텍터(race detector)와 [Go 메모리 모델](/ref/mem) 간의 불일치를 수정했습니다. 이제 레이스 디텍터는 메모리 모델의 채널 동기화 규칙을 더 정확하게 따릅니다. 그 결과, 이전에는 감지하지 못했던 레이스를 이제 보고할 수 있습니다.

## 컴파일러 {#compiler}

<!-- CL 256459, CL 264837, CL 266203, CL 256460 -->
이제 컴파일러가 레이블이 없는 `for` 루프, 메서드 값(method values), 그리고 타입 스위치(type switches)가 포함된 함수를 인라인화할 수 있습니다. 또한 인라이너가 인라인화가 가능한 더 많은 간접 호출(indirect calls)을 감지할 수 있게 되었습니다.

## Linker {#linker}

<!-- CL 248197 -->
이번 릴리스에는 Go 링커에 대한 추가 개선 사항이 포함되어 있으며, 이를 통해 링커 리소스 사용량(시간 및 메모리 모두)을 줄이고 코드의 견고성과 유지보수성을 향상시켰습니다. 이러한 변경 사항은 [Go 링커 현대화](/s/better-linker)를 위한 2단계 릴리스 프로젝트의 후반부에 해당합니다.

1.16의 링커 변경 사항은 1.15의 개선 사항을 지원되는 모든 아키텍처/OS 조합으로 확장합니다 (1.15의 성능 개선은 주로 `ELF` 기반 OS와 `amd64` 아키텍처에 집중되었습니다). 대표적인 대규모 Go 프로그램 세트의 경우, `linux/amd64`에서 링킹 속도가 1.15보다 20-25% 빨라지고 평균 메모리 사용량은 5-15% 감소하며, 다른 아키텍처와 OS에서는 더 큰 개선 효과가 있습니다. 또한 더 공격적인 심볼 프루닝(symbol pruning) 덕분에 대부분의 바이너리 크기가 줄어들었습니다.

<!-- CL 255259 -->
Windows에서 `go build -buildmode=c-shared`는 이제 기본적으로 Windows ASLR DLL을 생성합니다. ASLR은 `--ldflags=-aslr=false`를 통해 비활성화할 수 있습니다.

## 표준 라이브러리 {#library}

### 내장 파일 {#library-embed}

새로운 [`embed`](/pkg/embed/) 패키지는
새로운 [`//go:embed` 지시어](#embed)를 사용하여
컴파일 중에 프로그램에 내장된 파일에 대한 액세스를 제공합니다.

### 파일 시스템 {#fs}

새로운 [`io/fs`](/pkg/io/fs/) 패키지는 읽기 전용 파일 트리로의 추상화인 [`fs.FS`](/pkg/io/fs/#FS) 인터페이스를 정의합니다. 표준 라이브러리 패키지들은 적절한 경우 이 인터페이스를 활용하도록 조정되었습니다.

인터페이스의 생산자 측면에서,
새로운 [`embed.FS`](/pkg/embed/#FS) 타입은
[`zip.Reader`](/pkg/archive/zip/#Reader)와 마찬가지로
`fs.FS`를 구현합니다.
새로운 [`os.DirFS`](/pkg/os/#DirFS) 함수는
운영 체제 파일 트리를 기반으로 하는
`fs.FS` 구현체를 제공합니다.

사용자 측면에서는,
새로운 [`http.FS`](/pkg/net/http/#FS)
함수가 `fs.FS`를
[`http.FileSystem`](/pkg/net/http/#FileSystem)으로 변환합니다.
또한, [`html/template`](/pkg/html/template/)
및 [`text/template`](/pkg/text/template/)
패키지의 [`ParseFS`](/pkg/html/template/#ParseFS)
함수와 메서드들은 `fs.FS`에서 템플릿을 읽어옵니다.

`fs.FS`를 구현하는 코드를 테스트하기 위해, 새로운 [`testing/fstest`](/pkg/testing/fstest/) 패키지는 일반적인 실수들을 확인하고 보고하는 [`TestFS`](/pkg/testing/fstest/#TestFS) 함수를 제공합니다. 또한 `fs.FS` 구현체를 받아들이는 코드를 테스트할 때 유용한 간단한 인메모리 파일 시스템 구현체인 [`MapFS`](/pkg/testing/fstest/#MapFS)도 제공합니다.

### io/ioutil의 Deprecation {#ioutil}

[`io/ioutil`](/pkg/io/ioutil/) 패키지는 정의가 불분명하고 이해하기 어려운 기능들의 집합이었음이 드러났습니다. 해당 패키지에서 제공하던 모든 기능은 다른 패키지로 이동되었습니다. `io/ioutil` 패키지는 그대로 유지되며 이전과 동일하게 작동하겠지만, 새로운 코드에서는 [`io`](/pkg/io/) 및 [`os`](/pkg/os/) 패키지에 정의된 새로운 정의들을 사용할 것을 권장합니다.

다음은 `io/ioutil`에서 내보낸(exported) 이름들의 새로운 위치 목록입니다:

- [`Discard`](/pkg/io/ioutil/#Discard)
    => [`io.Discard`](/pkg/io/#Discard)
  - [`NopCloser`](/pkg/io/ioutil/#NopCloser)
    => [`io.NopCloser`](/pkg/io/#NopCloser)
  - [`ReadAll`](/pkg/io/ioutil/#ReadAll)
    => [`io.ReadAll`](/pkg/io/#ReadAll)
  - [`ReadDir`](/pkg/io/ioutil/#ReadDir)
    => [`os.ReadDir`](/pkg/os/#ReadDir)
    (참고: [`fs.FileInfo`](/pkg/io/fs/#FileInfo) 슬라이스 대신 
    [`os.DirEntry`](/pkg/os/#DirEntry) 슬라이스를 반환합니다)
  - [`ReadFile`](/pkg/io/ioutil/#ReadFile)
    => [`os.ReadFile`](/pkg/os/#ReadFile)
  - [`TempDir`](/pkg/io/ioutil/#TempDir)
    => [`os.MkdirTemp`](/pkg/os/#MkdirTemp)
  - [`TempFile`](/pkg/io/ioutil/#TempFile)
    => [`os.CreateTemp`](/pkg/os/#CreateTemp)
  - [`WriteFile`](/pkg/io/ioutil/#WriteFile)
    => [`os.WriteFile`](/pkg/os/#WriteFile)

### 라이브러리의 소규모 변경 사항 {#minor_library_changes}

언제나 그렇듯, Go 1 [호환성 약속](/doc/go1compat)을 염두에 두고 라이브러리에 다양한 소규모 변경 및 업데이트가 이루어졌습니다.

#### [archive/zip](/pkg/archive/zip/)

<!-- CL 243937 -->
새로운 [`Reader.Open`](/pkg/archive/zip/#Reader.Open)
메서드는 [`fs.FS`](/pkg/io/fs/#FS)
인터페이스를 구현합니다.

#### [crypto/dsa](/pkg/crypto/dsa/)

<!-- CL 257939 -->
[`crypto/dsa`](/pkg/crypto/dsa/) 패키지는 이제 더 이상 사용되지 않습니다(deprecated).
[issue #40337](/issue/40337)을 참조하십시오.

<!-- crypto/dsa -->

#### [crypto/hmac](/pkg/crypto/hmac/)

<!-- CL 261960 -->
[`New`](/pkg/crypto/hmac/#New)는 이제 해시 생성 함수를 별도로 호출했을 때 새로운 값이 반환되지 않으면 panic을 발생시킵니다. 이전에는 동작이 정의되지 않았으며, 때때로 유효하지 않은 출력값이 생성되었습니다.

<!-- crypto/hmac -->

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 256897 -->
이제 새로운 [`net.ErrClosed`](/pkg/net/#ErrClosed) 에러를 사용하여 닫히고 있거나 이미 닫힌 TLS 연결에서의 I/O 작업을 감지할 수 있습니다. 일반적인 사용 예시는 `errors.Is(err, net.ErrClosed)`입니다.

<!-- CL 266037 -->
무한 대기 상태가 되는 것을 방지하기 위해, [`Conn.Close`](/pkg/crypto/tls/#Conn.Close)에서 "close notify" 알림을 보내기 전에 기본 쓰기 마감 시간(write deadline)이 설정됩니다.

<!-- CL 239748 -->
이제 서버가 [클라이언트가 광고한 목록](/pkg/crypto/tls/#Config.NextProtos)에 없는 [ALPN 프로토콜](/pkg/crypto/tls/#ConnectionState.NegotiatedProtocol)을 선택하면 클라이언트가 핸드셰이크 오류를 반환합니다.

<!-- CL 262857 -->
이제 클라이언트나 서버 중 어느 한 쪽이라도 AES 하드웨어 가속을 지원하지 않는 경우, [
`Config.PreferServerCipherSuites`](/pkg/crypto/tls/#Config.PreferServerCipherSuites)
와 [`Config.CipherSuites`](/pkg/crypto/tls/#Config.CipherSuites)
가 모두 설정되어 있지 않다면 서버는 AES-GCM 사이퍼 스위트보다 다른 사용 가능한 AEAD 사이퍼 스위트(예: ChaCha20Poly1305)를 우선적으로 선택합니다. 클라이언트가 AES-GCM 사이퍼 스위트에 대한 선호도를 나타내지 않으면 AES 하드웨어 가속을 지원하지 않는 것으로 간주합니다.

<!-- CL 246637 -->
[`Config.Clone`](/pkg/crypto/tls/#Config.Clone)은 이제 리시버가 nil인 경우 패닉(panic)을 발생시키는 대신 nil을 반환합니다.

<!-- crypto/tls -->

#### [crypto/x509](/pkg/crypto/x509/)

`GODEBUG=x509ignoreCN=0` 플래그는 Go 1.17에서 제거될 예정입니다.
이 플래그는 Subject Alternative Names가 없을 때 X.509 인증서의 `CommonName` 필드를 호스트 이름으로 처리하는 레거시 동작을 활성화합니다.

<!-- CL 235078 -->
[`ParseCertificate`](/pkg/crypto/x509/#ParseCertificate) 및
[`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate)가
이제 `DNSNames`, `EmailAddresses`, `URIs` 필드에 대해 문자열 인코딩 제한을 강제합니다. 이 필드들은
ASCII 범위 내의 문자로 구성된 문자열만 포함할 수 있습니다.

<!-- CL 259697 -->
[`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate)는
이제 서명자의 공개 키를 사용하여 생성된 인증서의 서명을 검증합니다.
서명이 유효하지 않은 경우, 잘못된 형식의 인증서를 반환하는 대신
에러를 반환합니다.

<!-- CL 257939 -->
DSA 서명 검증이 더 이상 지원되지 않습니다. DSA 서명 생성은 원래 지원되지 않았음을 유의하시기 바랍니다.
[issue #40337](/issue/40337)을 참조하십시오.

<!-- CL 257257 -->
Windows에서 [`Certificate.Verify`](/pkg/crypto/x509/#Certificate.Verify)는 이제 가장 순위가 높은 체인 하나만 반환하는 대신, 플랫폼 인증서 검증기에 의해 구축된 모든 인증서 체인을 반환합니다.

<!-- CL 262343 -->
새로운 [`SystemRootsError.Unwrap`](/pkg/crypto/x509/#SystemRootsError.Unwrap)
메서드를 통해 [`errors`](/pkg/errors) 패키지 함수들로 [`Err`](/pkg/crypto/x509/#SystemRootsError.Err)
필드에 접근할 수 있습니다.

<!-- CL 230025 -->
Unix 시스템에서 `crypto/x509` 패키지가 시스템 인증서 풀(system cert pool)의 복사본을 저장하는 방식이 더 효율적으로 개선되었습니다.
소수의 루트 인증서만 사용하는 프로그램의 경우, 메모리 사용량이 약 0.5MB 감소합니다.

<!-- crypto/x509 -->

#### [debug/elf](/pkg/debug/elf/)

<!-- CL 255138 -->
더 많은 [`DT`](/pkg/debug/elf/#DT_NULL)
및 [`PT`](/pkg/debug/elf/#PT_NULL)
상수들이 추가되었습니다.

<!-- debug/elf -->

#### [encoding/asn1](/pkg/encoding/asn1)

<!-- CL 255881 -->
[`Unmarshal`](/pkg/encoding/asn1/#Unmarshal) 및
[`UnmarshalWithParams`](/pkg/encoding/asn1/#UnmarshalWithParams)는
이제 인자가 포인터가 아니거나 nil인 경우 패닉을 발생시키는 대신 에러를 반환합니다. 이 변경 사항은 [`encoding/json`](/pkg/encoding/json)과 같은 다른 인코딩 패키지의 동작과 일치합니다.

#### [encoding/json](/pkg/encoding/json/)

<!-- CL 234818 -->
[`Marshal`](/pkg/encoding/json/#Marshal),
[`Unmarshal`](/pkg/encoding/json/#Unmarshal) 및 관련 기능에서 인식하는 `json` 구조체 필드 태그가 이제 Go 구조체 필드에 대한 JSON 객체 이름 내에 세미콜론(`;`) 문자를 사용하는 것을 허용합니다.

<!-- encoding/json -->

#### [encoding/xml](/pkg/encoding/xml/)

<!-- CL 264024 -->
인코더는 항상 XML 명세에서 예약된 `xml`로 시작하는 네임스페이스 접두사 사용을 피하도록 처리해 왔습니다.
이제 명세를 더욱 엄격히 따라, 해당 확인 과정을 대소문자 구분 없이 수행함으로써 `XML`, `XmL` 등으로 시작하는 접두사 또한 사용되지 않도록 합니다.

<!-- encoding/xml -->

#### [flag](/pkg/flag/)

<!-- CL 240014 -->
새로운 [`Func`](/pkg/flag/#Func) 함수는
[`Value`](/pkg/flag/#Value) 인터페이스를 구현하는 것보다
더 가벼운 대안으로, 함수 호출을 통해 구현된 플래그를
등록할 수 있게 해줍니다.

제공해주신 내용이 비어 있거나 주석(`<!-- flag -->`)만 포함되어 있습니다. 번역할 구체적인 기술 콘텐츠를 제공해 주시면, 요청하신 지침에 따라 정성껏 한국어로 번역해 드리겠습니다.

#### [go/build](/pkg/go/build/)

<!-- CL 243941, CL 283636 -->
[`Package`](/pkg/go/build/#Package) 구조체에 패키지 내의 `//go:embed` 지시문에 대한 정보를 보고하는 새로운 필드들이 추가되었습니다:
[`EmbedPatterns`](/pkg/go/build/#Package.EmbedPatterns),
[`EmbedPatternPos`](/pkg/go/build/#Package.EmbedPatternPos),
[`TestEmbedPatterns`](/pkg/go/build/#Package.TestEmbedPatterns),
[`TestEmbedPatternPos`](/pkg/go/build/#Package.TestEmbedPatternPos),
[`XTestEmbedPatterns`](/pkg/go/build/#Package.XTestEmbedPatterns),
[`XTestEmbedPatternPos`](/pkg/go/build/#Package.XTestEmbedPatternPos).

<!-- CL 240551 -->
[`Package`](/pkg/go/build/#Package) 필드의
[`IgnoredGoFiles`](/pkg/go/build/#Package.IgnoredGoFiles)는
더 이상 "_" 또는 "."으로 시작하는 파일을 포함하지 않습니다.
해당 파일들은 항상 무시되기 때문입니다.
`IgnoredGoFiles`는 빌드 제약 조건(build constraints)으로 인해
무시된 파일들을 위한 것입니다.

<!-- CL 240551 -->
새로운 [`Package`](/pkg/go/build/#Package)
필드인 [`IgnoredOtherFiles`](/pkg/go/build/#Package.IgnoredOtherFiles)
에는 빌드 제약 조건(build constraints)으로 인해 무시된 non-Go 파일 목록이 포함됩니다.

<!-- go/build -->

#### [go/build/constraint](/pkg/go/build/constraint/)

<!-- CL 240604 -->
새로운 [`go/build/constraint`](/pkg/go/build/constraint/) 패키지는 기존의 `// +build` 구문과 Go 1.17에서 도입될 `//go:build` 구문 모두를 포함하여 빌드 제약 조건 라인을 파싱합니다. 이 패키지는 Go 1.16으로 빌드된 도구들이 Go 1.17 소스 코드를 처리할 수 있도록 하기 위해 존재합니다. 빌드 제약 조건 구문과 `//go:build` 구문으로의 전환 계획에 대한 자세한 내용은 [https://golang.org/design/draft-gobuild](/design/draft-gobuild)를 참조하십시오. `//go:build` 라인은 Go 1.16에서 지원**되지** 않으며, 아직 Go 프로그램에 도입해서는 안 된다는 점에 유의하십시오.

<!-- go/build/constraint -->

#### [html/template](/pkg/html/template/)

<!-- CL 243938 -->
새로운 [`template.ParseFS`](/pkg/html/template/#ParseFS)
함수와 [`template.Template.ParseFS`](/pkg/html/template/#Template.ParseFS)
메서드는 [`template.ParseGlob`](/pkg/html/template/#ParseGlob)
및 [`template.Template.ParseGlob`](/pkg/html/template/#Template.ParseGlob)와
유사하지만, [`fs.FS`](/pkg/io/fs/#FS)에서 템플릿을 읽어옵니다.

<!-- html/template -->

#### [io](/pkg/io/)

<!-- CL 261577 -->
이제 패키지에 [`ReadSeekCloser`](/pkg/io/#ReadSeekCloser) 인터페이스가 정의되었습니다.

<!-- CL 263141 -->
이제 이 패키지는 [`io/ioutil`](/pkg/io/ioutil/) 패키지의 동일한 이름 대신 사용할 수 있도록
[`Discard`](/pkg/io/#Discard),
[`NopCloser`](/pkg/io/#NopCloser), 및
[`ReadAll`](/pkg/io/#ReadAll)을 정의합니다.

<!-- io -->

#### [log](/pkg/log/)

<!-- CL 264460 -->
새로운 [`Default`](/pkg/log/#Default) 함수는
기본 [`Logger`](/pkg/log/#Logger)에 대한 접근을 제공합니다.

제시해주신 내용이 비어 있거나 주석(`<!-- log -->`)만 포함되어 있습니다. 번역할 영문 텍스트를 제공해 주시면, 요청하신 대로 Markdown 구조와 기술적 식별자를 유지하여 정확하게 한국어로 번역해 드리겠습니다.

#### [log/syslog](/pkg/log/syslog/)

<!-- CL 264297 -->
[`Writer`](/pkg/log/syslog/#Writer)는 이제 사용자 정의 Unix 도메인 소켓으로 로깅할 때
로컬 메시지 형식(호스트 이름을 생략하고 더 짧은 타임스탬프를 사용)을 사용하며,
이는 기본 로그 소켓에 이미 사용되고 있는 형식과 일치합니다.

<!-- log/syslog -->

#### [mime/multipart](/pkg/mime/multipart/)

<!-- CL 247477 -->
[`Reader`](/pkg/mime/multipart/#Reader)의
[`ReadForm`](/pkg/mime/multipart/#Reader.ReadForm)
메서드는 이제 제한 값으로 최대 `int64` 값이 전달되어도 폼 데이터를 거부하지 않습니다.

제공해주신 콘텐츠가 비어 있거나 `<!-- mime/multipart -->` 주석만 포함되어 있습니다. 번역할 실제 텍스트 내용을 제공해 주시면, 요청하신 기술 번역 원칙에 따라 Markdown 구조와 코드를 유지하며 정확하게 한국어로 번역해 드리겠습니다.

#### [net](/pkg/net/)

<!-- CL 250357 -->
닫힌 네트워크 연결에서의 I/O, 또는 I/O가 완료되기 전에 닫힌 네트워크 연결에서의 I/O 케이스를 이제 새로운 [`ErrClosed`](/pkg/net/#ErrClosed) 에러를 통해 감지할 수 있습니다. 전형적인 사용 방식은 `errors.Is(err, net.ErrClosed)`입니다.
이전 릴리스에서는 이 케이스를 안정적으로 감지하는 유일한 방법이 `Error` 메서드가 반환하는 문자열이 `"use of closed network connection"`과 일치하는지 확인하는 것이었습니다.

<!-- CL 255898 -->
이전 Go 릴리스에서는 `/proc/sys/net/core/somaxconn`에 의해 설정되는 Linux 시스템의 기본 TCP 리스너 백로그(backlog) 크기가 최대 `65535`로 제한되었습니다.
Linux 커널 버전 4.1 이상부터는 이 최대값이 `4294967295`로 변경되었습니다.

<!-- CL 238629 -->
Linux에서 `/etc/nsswitch.conf` 파일이 없는 경우, 호스트 이름 조회 시 `/etc/hosts`를 확인하기 전에 더 이상 DNS를 사용하지 않습니다. 이는 musl 기반 시스템에서 흔히 나타나는 현상이며, 이를 통해 Go 프로그램이 해당 시스템의 C 프로그램 동작 방식과 일치하게 됩니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- CL 233637 -->
[`net/http`](/pkg/net/http/) 패키지에서 [`StripPrefix`](/pkg/net/http/#StripPrefix)의 동작이 변경되어, 요청 URL의 `Path` 필드뿐만 아니라 `RawPath` 필드에서도 접두사(prefix)를 제거합니다.
이전 릴리스에서는 `Path` 필드만 트리밍되었으므로, 요청 URL에 이스케이프된 문자가 포함되어 있는 경우 URL의 `Path`와 `RawPath` 필드가 일치하지 않게 수정되었습니다.
Go 1.16부터 `StripPrefix`는 두 필드를 모두 트리밍합니다.
요청 URL의 접두사 부분에 이스케이프된 문자가 포함되어 있는 경우, 이전에는 일치하지 않는 `Path`/`RawPath` 쌍으로 기본 핸들러를 호출했으나, 이제는 404 응답을 반환합니다.

<!-- CL 252497 -->
이제 [`net/http`](/pkg/net/http/) 패키지는 `"-N"`이 음수 접미사 길이인 `"Range": "bytes=--N"` 형태의 HTTP 범위 요청(예: `"Range": "bytes=--2"`)을 거부합니다. 이제 이러한 요청에 대해 `416 "Range Not Satisfiable"` 응답을 반환합니다.

<!-- CL 256498, golang.org/issue/36990 -->
[`SameSiteDefaultMode`](/pkg/net/http/#SameSiteDefaultMode)로 설정된 쿠키가 이제 값 없는 SameSite 키를 생성하는 대신, 현재 사양에 따라 동작합니다(속성이 설정되지 않음).

<!-- CL 250039 -->
이제 [`Client`](/pkg/net/http/#Client)는 본문이 비어 있는 `PATCH` 요청 시 `Content-Length:` `0` 헤더를 명시적으로 전송하며, 이는 `POST` 및 `PUT`의 기존 동작과 일치합니다.

<!-- CL 249440 -->
[`ProxyFromEnvironment`](/pkg/net/http/#ProxyFromEnvironment)
함수는 이제 `HTTPS_PROXY` 환경 변수가 설정되지 않은 경우, `https://` URL에 대해 `HTTP_PROXY` 환경 변수의 설정을 반환하지 않습니다.

[`Transport`](/pkg/net/http/#Transport) 타입에 새로운 필드인 [`GetProxyConnectHeader`](/pkg/net/http/#Transport.GetProxyConnectHeader)가 추가되었습니다. 이 필드에는 `CONNECT` 요청 중에 프록시로 보낼 헤더를 반환하는 함수를 설정할 수 있습니다.

실질적으로 `GetProxyConnectHeader`는 기존 필드인 [`ProxyConnectHeader`](/pkg/net/http/#Transport.ProxyConnectHeader)의 동적 버전입니다. 만약 `GetProxyConnectHeader`가 `nil`이 아니면, `ProxyConnectHeader`는 무시됩니다.

<!-- CL 243939 -->
새로운 [`http.FS`](/pkg/net/http/#FS)
함수는 [`fs.FS`](/pkg/io/fs/#FS)를
[`http.FileSystem`](/pkg/net/http/#FileSystem)으로 변환합니다.

<!-- net/http -->

#### [net/http/httputil](/pkg/net/http/httputil/)

<!-- CL 260637 -->
[`ReverseProxy`](/pkg/net/http/httputil/#ReverseProxy)는 이제 본문 길이를 알 수 없는 스트리밍 응답을 프록시할 때 버퍼링된 데이터를 더 적극적으로 flush합니다.

<!-- net/http/httputil -->

#### [net/smtp](/pkg/net/smtp/)

<!-- CL 247257 -->
[`Client`](/pkg/net/smtp/#Client)의
[`Mail`](/pkg/net/smtp/#Client.Mail)
메서드는 이제 이를 지원하는 서버에 `SMTPUTF8` 지시어를 보내어, 주소가 UTF-8로 인코딩되었음을 알립니다.

<!-- net/smtp -->

#### [os](/pkg/os/)

<!-- CL 242998 -->
[`Process.Signal`](/pkg/os/#Process.Signal)은 이제 프로세스가 이미 종료된 경우, 공개되지 않은 `errFinished` 대신 [`ErrProcessDone`](/pkg/os/#ErrProcessDone)을 반환합니다.

<!-- CL 261540 -->
이 패키지는 [`fs.DirEntry`](/pkg/io/fs/#DirEntry)의 별칭(alias)으로 새로운 타입 [`DirEntry`](/pkg/os/#DirEntry)를 정의합니다.
새로운 [`ReadDir`](/pkg/os/#ReadDir) 함수와 [`File.ReadDir`](/pkg/os/#File.ReadDir) 메서드를 사용하여 디렉토리 내용을 [`DirEntry`](/pkg/os/#DirEntry) 슬라이스로 읽어올 수 있습니다.
[`File.Readdir`](/pkg/os/#File.Readdir) 메서드(`dir`의 `d`가 소문자인 점에 유의하세요)는 여전히 존재하며 [`FileInfo`](/pkg/os/#FileInfo) 슬라이스를 반환하지만, 대부분의 프로그램에서는 [`File.ReadDir`](/pkg/os/#File.ReadDir)로 전환하는 것이 더 효율적입니다.

<!-- CL 263141 -->
이제 이 패키지는 [`io/ioutil`](/pkg/io/ioutil/) 패키지에 정의된 함수들을 대신하여 사용할 수 있도록 [`CreateTemp`](/pkg/os/#CreateTemp), [`MkdirTemp`](/pkg/os/#MkdirTemp), [`ReadFile`](/pkg/os/#ReadFile), 그리고 [`WriteFile`](/pkg/os/#WriteFile)을 정의합니다.

<!-- CL 243906 -->
[`FileInfo`](/pkg/os/#FileInfo),
[`FileMode`](/pkg/os/#FileMode), 그리고
[`PathError`](/pkg/os/#PathError) 타입이
이제 [`io/fs`](/pkg/io/fs/) 패키지에 있는 동일한 이름의 타입들에 대한 별칭(alias)이 되었습니다.
[`os`](/pkg/os/) 패키지의 함수 시그니처들은 [`io/fs`](/pkg/io/fs/) 패키지의 이름을 참조하도록 업데이트되었습니다.
이는 기존 코드에 영향을 주지 않아야 합니다.

<!-- CL 243911 -->
새로운 [`DirFS`](/pkg/os/#DirFS) 함수는
운영 체제 파일 트리를 기반으로 하는
[`fs.FS`](/pkg/io/fs/#FS)의 구현체를 제공합니다.

<!-- os -->

#### [os/signal](/pkg/os/signal/)

<!-- CL 219640 -->
새로운 [`NotifyContext`](/pkg/os/signal/#NotifyContext) 함수를 사용하면 특정 시그널이 도착했을 때 취소되는 컨텍스트를 생성할 수 있습니다.

<!-- os/signal -->

#### [path](/pkg/path/)

<!-- CL 264397, golang.org/issues/28614 -->
이제 [`Match`](/pkg/path/#Match) 함수는 패턴의 일치하지 않는 부분에 구문 오류(syntax error)가 있는 경우 에러를 반환합니다. 이전에는 일치하지 않을 때 함수가 조기에 반환되었으며, 이로 인해 패턴 뒷부분에 있는 구문 오류를 보고하지 않았습니다.

<!-- path -->

#### [path/filepath](/pkg/path/filepath/)

<!-- CL 267887 -->
새로운 함수인 [`WalkDir`](/pkg/path/filepath/#WalkDir)는 [`Walk`](/pkg/path/filepath/#Walk)와 유사하지만, 일반적으로 더 효율적입니다. `WalkDir`에 전달되는 함수는 [`fs.FileInfo`](/pkg/io/fs/#FileInfo) 대신 [`fs.DirEntry`](/pkg/io/fs/#DirEntry)를 받습니다. (`Walk` 함수가 [`os.FileInfo`](/pkg/os/#FileInfo)를 받았던 것을 기억하시는 분들을 위해 설명하자면, `os.FileInfo`는 이제 `fs.FileInfo`의 별칭입니다.)

<!-- CL 264397, golang.org/issues/28614 -->
[`Match`](/pkg/path/filepath#Match) 및
[`Glob`](/pkg/path/filepath#Glob) 함수는 이제 패턴의 일치하지 않는 부분에 구문 오류가 있는 경우 에러를 반환합니다. 이전에는 일치 항목을 찾지 못하면 함수가 조기에 반환되었으며, 따라서 패턴의 뒷부분에 있는 구문 오류를 보고하지 않았습니다.

<!-- path/filepath -->

#### [reflect](/pkg/reflect/)

<!-- CL 192331 -->
`Zero` 함수가 할당(allocation)을 피하도록 최적화되었습니다. 반환된 `Value`를 `==` 또는 `DeepEqual`을 사용하여 다른 `Value`와 잘못 비교하는 코드는 이전 Go 버전에서 얻은 결과와 다른 결과를 얻을 수 있습니다. [`reflect.Value`](/pkg/reflect#Value)의 문서에서 두 `Value`를 올바르게 비교하는 방법을 설명합니다.

<!-- reflect -->

#### [runtime/debug](/pkg/runtime/debug/)

<!-- CL 249677 -->
`SetPanicOnFault`가 활성화되었을 때 사용되는 [`runtime.Error`](/pkg/runtime#Error) 값에 이제 `Addr` 메서드가 포함될 수 있습니다. 해당 메서드가 존재하는 경우, 결함(fault)을 유발한 메모리 주소를 반환합니다.

<!-- runtime/debug -->

#### [strconv](/pkg/strconv/)

<!-- CL 260858 -->
[`ParseFloat`](/pkg/strconv/#ParseFloat)가 이제 [Eisel-Lemire 알고리즘](https://nigeltao.github.io/blog/2020/eisel-lemire.html)을 사용하여 성능이 최대 2배 향상되었습니다. 이를 통해 [`encoding/json`](/pkg/encoding/json/)과 같은 텍스트 형식의 디코딩 속도 또한 향상될 수 있습니다.

<!-- strconv -->

#### [syscall](/pkg/syscall/)

<!-- CL 263271 -->
[`NewCallback`](/pkg/syscall/?GOOS=windows#NewCallback)
및
[`NewCallbackCDecl`](/pkg/syscall/?GOOS=windows#NewCallbackCDecl)
이 이제 `uintptr` 크기보다 작은 인자가 연속으로 여러 개 있는 콜백 함수를 올바르게 지원합니다. 이에 따라 작은 인자들 사이에 수동으로 추가했던 패딩(padding)을 제거하기 위해 해당 함수들의 사용 방식을 변경해야 할 수도 있습니다.

<!-- CL 261917 -->
Windows의 [`SysProcAttr`](/pkg/syscall/?GOOS=windows#SysProcAttr)에 새로운 `NoInheritHandles` 필드가 추가되었습니다. 이 필드는 새 프로세스를 생성할 때 핸들 상속을 비활성화합니다.

<!-- CL 269761, golang.org/issue/42584 -->
Windows의 [`DLLError`](/pkg/syscall/?GOOS=windows#DLLError)에 기본 에러(underlying error)를 언래핑(unwrapping)하기 위한 `Unwrap` 메서드가 추가되었습니다.

<!-- CL 210639 -->
Linux에서
[`Setgid`](/pkg/syscall/#Setgid),
[`Setuid`](/pkg/syscall/#Setuid)
및 관련 호출들이 이제 구현되었습니다.
이전에는 `syscall.EOPNOTSUPP` 에러를 반환했습니다.

<!-- CL 210639 -->
Linux에서 새로운 함수인
[`AllThreadsSyscall`](/pkg/syscall/#AllThreadsSyscall)
및 [`AllThreadsSyscall6`](/pkg/syscall/#AllThreadsSyscall6)
를 사용하여 프로세스 내의 모든 Go 스레드에서 시스템 콜을 호출할 수 있습니다.
이 함수들은 cgo를 사용하지 않는 프로그램에서만 사용할 수 있습니다.
프로그램이 cgo를 사용하는 경우, 이 함수들은 항상
[`syscall.ENOTSUP`](/pkg/syscall/#ENOTSUP)
을 반환합니다.

<!-- syscall -->

#### [testing/iotest](/pkg/testing/iotest/)

<!-- CL 199501 -->
새로운
[`ErrReader`](/pkg/testing/iotest/#ErrReader)
함수는 항상 에러를 반환하는
[`io.Reader`](/pkg/io/#Reader)를 반환합니다.

<!-- CL 243909 -->
새로운 [`TestReader`](/pkg/testing/iotest/#TestReader) 함수는 [`io.Reader`](/pkg/io/#Reader)가 올바르게 동작하는지 테스트합니다.

<!-- testing/iotest -->

#### [text/template](/pkg/text/template/)

<!-- CL 254257, golang.org/issue/29770 -->
이제 액션 구분자(action delimiters) 내에 개행 문자가 허용되어, 액션을 여러 줄에 걸쳐 작성할 수 있습니다.

<!-- CL 243938 -->
새로운 [`template.ParseFS`](/pkg/text/template/#ParseFS)
함수와 [`template.Template.ParseFS`](/pkg/text/template/#Template.ParseFS)
메서드는 [`template.ParseGlob`](/pkg/text/template/#ParseGlob)
및 [`template.Template.ParseGlob`](/pkg/text/template/#Template.ParseGlob)과
유사하지만, [`fs.FS`](/pkg/io/fs/#FS)에서 템플릿을 읽어옵니다.

<!-- text/template -->

#### [text/template/parse](/pkg/text/template/parse/)

<!-- CL 229398, golang.org/issue/34652 -->
파스 트리(parse tree)에 새로운 [`CommentNode`](/pkg/text/template/parse/#CommentNode)가 추가되었습니다. `parse.Tree`의 [`Mode`](/pkg/text/template/parse/#Mode) 필드를 통해 이에 접근할 수 있습니다.

<!-- text/template/parse -->

#### [time/tzdata](/pkg/time/tzdata/)

<!-- CL 261877 -->
이제 `$GOROOT/lib/time/zoneinfo.zip`의 타임존 데이터베이스와 이 패키지에 내장된 복사본에 슬림 타임존 데이터 포맷(slim timezone data format)이 사용됩니다. 이를 통해 타임존 데이터베이스의 크기가 약 350 KB 감소했습니다.

<!-- time/tzdata -->

#### [unicode](/pkg/unicode/)

<!-- CL 248765 -->
[`unicode`](/pkg/unicode/) 패키지와 시스템 전반의 관련 지원 사항이 Unicode 12.0.0에서 [Unicode 13.0.0](https://www.unicode.org/versions/Unicode13.0.0/)으로 업그레이드되었습니다. 이번 업데이트를 통해 4개의 새로운 스크립트를 포함한 5,930개의 새로운 문자와 55개의 새로운 이모지가 추가되었습니다. 또한 Unicode 13.0.0은 평면 3(U+30000-U+3FFFF)을 제3 표의문자 평면(tertiary ideographic plane)으로 지정합니다.

제공해주신 입력값에 번역할 텍스트가 포함되어 있지 않습니다. 번역이 필요한 Markdown 내용을 제공해 주시면, 기술적인 맥락을 유지하며 정확하게 한국어로 번역해 드리겠습니다.
