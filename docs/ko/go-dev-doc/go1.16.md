<!--
참고: 이 문서 및 이 디렉토리에 있는 다른 문서에서, 고정 폭 문구와 고정 폭이 아닌 공백을 함께 사용하는 규칙을 따릅니다. 예를 들어, `hello` `world`와 같이 사용합니다.
이러한 문구에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.16 소개 {#introduction}

가장 최신 Go 릴리스인 버전 1.16은 Go 1.15 ([Go 1.15](/doc/go1.15)) 이후 6개월 만에 출시됩니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
물론, 이 릴리스는 Go 1의 호환성 ([Go 1 호환성](/doc/go1compat.html))을 유지합니다.
대부분의 Go 프로그램이 이전과 동일하게 컴파일 및 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

```
// Go code example
package main
```

```markdown
## 변경 사항 없음

```

## 포트 {#ports}

### Darwin 및 iOS {#darwin}

<!-- golang.org/issue/38485, golang.org/issue/41385, CL 266373, 더 많은 CL -->
Go 1.16은 macOS (또는 Apple Silicon)에서 64비트 ARM 아키텍처를 지원하는 기능을 추가합니다. 이를 위해 `GOOS=darwin`, `GOARCH=arm64`를 사용합니다.
`darwin/amd64` 포트와 마찬가지로, `darwin/arm64` 포트는 cgo, 내부 및 외부 링킹, `c-archive`, `c-shared`, `pie` 빌드 모드 및 래스 검출기를 지원합니다.

<!-- CL 254740 -->
이전의 iOS 포트인 `darwin/arm64`은 `ios/arm64`로 이름이 변경되었습니다. `GOOS=ios`는 `darwin` 빌드 태그를 의미하며, `GOOS=android`와 마찬가지로 `linux` 빌드 태그를 나타냅니다. 이 변경 사항은 `gomobile`를 사용하여 iOS 앱을 빌드하는 모든 사용자에게는 투명하게 적용되어야 합니다.

`GOOS=ios`를 사용하면 파일 이름
예를 들어 `x_ios.go`는 이제
`GOOS=ios`에 대해서만 빌드됩니다. 자세한 내용은
[`go`
`help` `buildconstraint`](/cmd/go/#hdr-Build_constraints)를 참조하십시오.
이러한 형식의 파일 이름을 사용하는 기존 패키지는 파일 이름을 변경해야 합니다.

<!-- golang.org/issue/42100, CL 263798 -->
Go 1.16에서 `ios/amd64` 포트를 추가하여, AMD64 기반의 macOS에서 실행되는 iOS
시뮬레이터를 대상으로 합니다. 이전에 `darwin/amd64`를 사용하여
`ios` 빌드 태그를 설정하여 비공식적으로 지원되었습니다.
[`misc/ios/README`](/misc/ios/README)에서 iOS 및 iOS 시뮬레이터용 프로그램을 빌드하는 방법에 대한 자세한 내용을 참조하십시오.

<!-- golang.org/issue/23011 -->
Go 1.16은 macOS 10.12 Sierra에서 실행되는 마지막 버전입니다.
Go 1.17은 macOS 10.13 High Sierra 또는 이후 버전이 필요합니다.

### NetBSD {#netbsd}

<!-- golang.org/issue/30824 -->
Go는 이제 NetBSD (netbsd/arm64 포트)에서 64비트 ARM 아키텍처를 지원합니다.

### OpenBSD {#openbsd}

<!-- golang.org/issue/40995 -->
Go는 이제 OpenBSD ( `openbsd/mips64` 포트)에서 MIPS64 아키텍처를 지원합니다. 이 포트는 아직 cgo를 지원하지 않습니다.

<!-- golang.org/issue/36435, 많은 CL -->
OpenBSD의 64비트 x86 및 64비트 ARM 아키텍처 ( `openbsd/amd64` 및 `openbsd/arm64` 포트)에서, 시스템
호출은 이제 `libc`를 통해 이루어지며, `SYSCALL`/`SVC` 명령어 직접 사용이 아닙니다. 이는 OpenBSD의 미래 버전과의 호환성을 보장합니다. 특히, OpenBSD 6.9 이후 버전에서는, 정적이지 않은 Go 바이너리에서 시스템 호출이 `libc`를 통해 이루어져야 합니다.

### 386 {#386}

<!-- golang.org/issue/40255, golang.org/issue/41848, CL 258957, 및 CL 260017 -->
Go 1.15 릴리스 노트에 [공지된](go1.15#386) 바와 같이,
Go 1.16은 x87 모드 컴파일(`GO386=387`) 지원을 중단합니다.
이제 SSE2가 아닌 프로세서에서 soft float 모드(`GO386=softfloat`)를 사용하여 지원이 가능합니다.
SSE2가 아닌 프로세서에서 실행 중인 사용자는 `GO386=387`을 `GO386=softfloat`으로 대체해야 합니다.

### RISC-V {#riscv}

<!-- golang.org/issue/36641, CL 267317 -->
`linux/riscv64` 포트가 이제 cgo 및
`-buildmode=pie`를 지원합니다. 이 릴리스에는 RISC-V에 대한 성능 최적화 및 코드 생성 개선 사항도 포함되어 있습니다.

## 도구 {#tools}

### Go 명령어 {#go-command}

#### 모듈 {#modules}

<!-- golang.org/issue/41330 -->
모듈 인식 모드는 현재 작업 디렉터리 또는 상위 디렉터리에 `go.mod` 파일이 존재하더라도 기본적으로 활성화됩니다. 좀 더 정확하게 말하면, `GO111MODULE` 환경 변수는 기본적으로 `on`으로 설정됩니다. 이전 동작으로 되돌리려면 `GO111MODULE`을 `auto`로 설정하십시오.

<!-- golang.org/issue/40728 -->
`go build` 및 `go test`와 같은 빌드 명령은 기본적으로 `go.mod` 및 `go.sum` 파일을 수정하지 않습니다. 대신, 모듈 요구 사항 또는 체크섬을 추가하거나 업데이트해야 하는 경우 오류를 보고합니다 (`-mod=readonly` 플래그가 사용된 것처럼). `go mod tidy` 또는 `go get` 명령을 사용하여 모듈 요구 사항 및 체크섬을 조정할 수 있습니다.

<!-- golang.org/issue/40276 -->
`go install` 명령어가 이제 버전 접미사(예: `go install example.com/cmd@v1.0.0`)를 포함하는 인수를 허용합니다. 이를 통해 `go install`은 현재 디렉토리 또는 상위 디렉토리에 있는 `go.mod` 파일을 무시하고, 모듈을 인식하는 방식으로 패키지를 빌드하고 설치합니다. 이는 메인 모듈의 종속성에 영향을 주지 않고 실행 파일을 설치하는 데 유용합니다.

<!-- golang.org/issue/40276 -->
`go install`, 단 버전 접미사가 있는 경우 또는 없는 경우, 모듈 모드로 패키지를 빌드하고 설치하는 데 권장되는 방법입니다. `go get`은 `-d` 플래그와 함께 사용하여 현재 모듈의 종속성을 빌드하지 않고 조정하는 데 사용해야 하며, `go get`을 사용하여 패키지를 빌드하고 설치하는 것은 더 이상 권장되지 않습니다. 향후 릴리스에서는 `-d` 플래그가 항상 활성화됩니다.

<!-- golang.org/issue/24031 -->
`retract` 지시어를 `go.mod` 파일에 사용하여 특정 버전의 모듈이 다른 모듈에서 사용되지 않도록 지정할 수 있습니다. 모듈 작성자는 심각한 문제가 발견되거나 버전이 실수로 게시된 경우, 해당 버전을 철회할 수 있습니다.

<!-- golang.org/issue/26603 -->
`go` `mod` `vendor`
및 `go` `mod` `tidy` 서브 명령어는 이제 `-e` 플래그를 받아들여, 누락된 패키지를 해결하는 데 오류가 발생하더라도 계속 진행되도록 지시합니다.

<!-- golang.org/issue/36465 -->
`go` 명령은 이제 메인 모듈에서 `exclude` 지침으로 지정된 모듈 버전 요구 사항을 무시합니다. 이전에는 `go` 명령이 제외된 버전을 다음 버전으로 사용했지만, 해당 버전은 시간이 지남에 따라 변경될 수 있었고, 그 결과 재현 불가능한 빌드가 발생했습니다.

<!-- golang.org/issue/43052, golang.org/issue/43985 -->
모듈 모드에서는 `go` 명령이 이제 비-ASCII 문자 또는 선행 점(.) 문자를 포함하는 가져오기 경로를 허용하지 않습니다. 이러한 문자를 포함하는 모듈 경로는 이미 금지되어 있었습니다 (자세한 내용은 [모듈 경로 및 버전](/ref/mod#go-mod-file-ident) 참조). 따라서 이 변경 사항은 모듈 하위 디렉토리 내의 경로에만 영향을 미칩니다.

#### 파일 임베딩 {#embed}

```
// 예시:
const myFileContent = `
# This is a header in the file
This is some content in the file.
`;

// 사용 예시:
console.log(myFileContent);
```

`go` 명령은 이제 최종 실행 파일에 정적 파일과 파일 트리를 포함할 수 있습니다. 이를 위해 새로운 `//go:embed` 지시어를 사용합니다.
자세한 내용은 새로운 [`embed`](/pkg/embed/) 패키지의 문서를 참조하십시오.

#### `go` 테스트 {#go-test}

<!-- golang.org/issue/29062 -->
`go test`를 사용할 때, 테스트 함수 내에서 `os.Exit(0)`를 호출하는 테스트는 이제 실패로 간주됩니다.
이 기능은 테스트가 `os.Exit(0)`를 호출하는 코드를 호출하고, 그 결과로 모든 후속 테스트를 중단하는 경우를 감지하는 데 도움이 됩니다.
만약 `TestMain` 함수가 `os.Exit(0)`를 호출하면, 여전히 성공적인 테스트로 간주됩니다.

<!-- golang.org/issue/39484 -->
`go` `test`는 `-c`
또는 `-i` 플래그를 알려지지 않은 플래그와 함께 사용할 때 오류를 보고합니다. 일반적으로,
알려지지 않은 플래그는 테스트에 전달되지만, `-c` 또는 `-i`를 사용할 때는 테스트가 실행되지 않습니다.

#### `go get` {#go-get}

<!-- golang.org/issue/37519 -->
`go get` 명령어의 `-insecure` 플래그는
더 이상 사용되지 않으며, 향후 버전에서 제거됩니다. 이 플래그는 HTTP와 같은 불안정한 스킴을 사용하여 저장소에서 가져오고 사용자 정의 도메인을 해결할 수 있게 하며, 체크섬 데이터베이스를 사용하여 모듈 서명 검증을 우회할 수도 있습니다. 불안정한 스킴을 사용하려면 `GOINSECURE` 환경 변수를 사용하십시오. 모듈 서명 검증을 우회하려면 `GOPRIVATE` 또는 `GONOSUMDB`를 사용하십시오. 자세한 내용은 `go help environment`를 참조하십시오.

<!-- golang.org/cl/263267 -->
`go get example.com/mod@patch` 이제
`example.com/mod`의 특정 버전을 메인 모듈에서 이미 요구하도록 합니다.
(하지만, `go get -u=patch`는 새롭게 추가된 의존성도 계속 패치합니다.)

#### `GOVCS` 환경 변수 {#govcs}

<!-- golang.org/issue/266420 -->
`GOVCS`는 `go` 명령어가 소스 코드를 다운로드하는 데 사용할 수 있는 버전 관리 도구를 제한하는 새로운 환경 변수입니다. 이는 일반적으로 신뢰할 수 있는, 인증된 환경에서 사용되는 도구와 관련된 보안 문제를 완화합니다. 기본적으로 `git` 및 `hg`는 모든 저장소에서 코드를 다운로드하는 데 사용될 수 있습니다. `svn`, `bzr`, 및 `fossil`은 `GOPRIVATE` 환경 변수에 정의된 패턴과 일치하는 모듈 경로 또는 패키지 경로를 가진 저장소에서만 코드를 다운로드하는 데 사용될 수 있습니다. 자세한 내용은 [`go`
`help` `vcs`](/cmd/go/#hdr-Controlling_version_control_with_GOVCS)를 참조하십시오.

#### `all` 패턴 {#all-패턴}

```go
package main

import "fmt"

func main() {
	// 모든 요소를 반복
	for _, element := range []int{1, 2, 3, 4, 5} {
		fmt.Println(element)
	}

	// 조건에 맞는 요소만 필터링
	filtered := []int{}
	for _, element := range []int{1, 2, 3, 4, 5} {
		if element%2 == 0 {
			filtered = append(filtered, element)
		}
	}
	fmt.Println(filtered)
}
```

<!-- golang.org/cl/240623 -->
메인 모듈의 `go.mod` 파일이 `go`를 `1.16` 또는 그 이상의 버전으로 선언하는 경우, `all` 패키지 패턴은 이제 메인 모듈에 포함된 패키지 또는 테스트에 의해 트랜지티브로 가져온 패키지만 일치합니다. (메인 모듈에 의해 가져온 패키지의 `_tests` 테스트가 포함된 패키지는 더 이상 포함되지 않습니다.) 이는 Go 1.11 이후 `go` `mod` `vendor`에 의해 유지되는 패키지의 동일한 집합입니다.

#### `-toolexec` 빌드 플래그 {#toolexec}

<!-- golang.org/cl/263357 -->
`-toolexec` 빌드 플래그를 사용하여 컴파일 또는 어셈블과 같은 툴체인 프로그램을 호출할 때, `TOOLEXEC_IMPORTPATH` 환경 변수는 현재 빌드되는 패키지의 가져오기 경로로 설정됩니다.

#### `-i` 빌드 플래그 {#i-플래그}

<!-- golang.org/issue/41696 -->
`go build`, `go install` 및 `go test` 명령에 사용되는 `-i` 플래그는 이제 사용되지 않습니다.
`-i` 플래그는 명령줄에 지정된 패키지에 가져온 패키지에 대한 패키지를 설치하도록 `go` 명령에 지시합니다.
Go 1.10부터 빌드 캐시가 도입된 이후, `-i` 플래그는 더 이상 빌드 시간에 상당한 영향을 미치지 않으며, 설치 디렉토리에 쓰기 권한이 없을 때 오류를 발생시킵니다.

#### `list` 명령어 {#list-buildid}

```
list buildid
```

<!-- golang.org/cl/263542 -->
`-export` 플래그가 지정되면, `BuildID`
필드가 컴파일된 패키지의 빌드 ID로 설정됩니다. 이는 `go` `tool` `buildid`를 실행하는 것과 동일하며,
`go` `list` `-exported` `-f` `{{.Export}}`를 사용하는 것과 같습니다. 하지만, 추가 단계를 거치지 않습니다.

#### `-overlay` 플래그 {#overlay-플래그}

<!-- golang.org/issue/39958 -->
`-overlay` 플래그는 파일 경로 대체에 대한 집합이 포함된 JSON 구성 파일을 지정합니다. `-overlay` 플래그는 모든 빌드 명령 및 `go` `mod` 하위 명령과 함께 사용할 수 있습니다.
이는 주로 gopls와 같은 편집 도구가 저장되지 않은 소스 파일의 변경 사항의 영향을 이해하는 데 사용하도록 설계되었습니다. 구성 파일은 실제 파일 경로를 대체 파일 경로에 매핑하며, `go` 명령 및 빌드는 대체 파일 경로에 지정된 내용을 사용하여 실제 파일 경로가 존재하는 것처럼 실행되거나, 대체 파일 경로가 비어 있으면 존재하지 않는 것으로 간주됩니다.

### Cgo {#cgo}

<!-- CL 252378 -->
[cgo](/cmd/cgo) 도는 도구가 C 구조체의 비트 필드를 Go 구조체 필드로 변환하는 것을 더 이상 시도하지 않습니다.
비트 필드가 Go에서 표현될 수 있더라도, C 구조체의 비트 필드가 메모리에 나타나는 순서는 구현에 따라 다릅니다. 따라서, cgo 도구는 때때로 의도치 않게 잘못된 결과를 생성했습니다.

### 수의사 {#vet}

#### 유효하지 않은 testing.T 사용에 대한 새로운 경고 {#vet-testing-T}

<!-- CL 235677 -->
동작 검사 도구가 이제 `testing.T`
메서드의 `Fatal` 호출이 테스트 중에 생성된 goroutine 내에서 유효하지 않은 경우에 대해 경고합니다.
또한, `testing.T` 테스트 또는 `testing.B` 벤치마크에서 `Fatalf`, `FailNow`, 및 `Skip{,f,Now}` 메서드의 호출에 대해서도 경고합니다.

다음 메서드 호출은 생성된 고루틴의 실행을 중단시키고, `Test*` 또는 `Benchmark*` 함수를 중단시키지는 않습니다. 따라서 이러한 메서드는 고루틴이 테스트 또는 벤치마크 함수를 실행하는 경우에 호출되어야 합니다. 예를 들어:

```markdown
```go
func TestFoo(t *testing.T) {
	    go func() {
	        if condition() {
	            t.Fatal("oops") // 이렇게 하면 내부 함수가 아닌 TestFoo가 종료됩니다.
	        }
	        ...
	    }()
	}
```

`t.Fatal` (또는 유사한 메서드)를 생성된
고루틴에서 호출하는 코드는 테스트 실패를 알리는 데 `t.Error`를 사용하고, `return` 문과 같은 대체 방법을 사용하여 고루틴을 조기에 종료하도록 변경해야 합니다. 이전 예시는 다음과 같이 변경할 수 있습니다:

```markdown
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

#### 프레임 포인터에 대한 새 경고 {#vet-frame-pointer}

<!-- CL 248686, CL 276372 -->
이제 펫 툴은 amd64 어셈블리가 프레임 포인터(BP 레지스터)를 저장하고 복원하지 않고 무시하는 것을 경고합니다. 이는 호출 규칙에 위배됩니다. BP 레지스터를 저장하지 않는 코드는 다음 중 하나로 수정해야 합니다.
* BP를 사용하지 않도록 수정
* BP를 저장하고 복원하도록 수정
BP를 안전하게 저장하는 방법은 프레임 크기를 0이 아닌 값으로 설정하는 것입니다. 이렇게 하면 생성된 prologue와 epilogue가 BP 레지스터를 자동으로 저장합니다.
예시 수정 사항은 [CL 248260](/cl/248260)를 참조하십시오.

#### 새로운 경고: asn1.Unmarshal {#vet-asn1-unmarshal}

<!-- CL 243397 -->
이제 동물 관리 도구가 `asn1.Unmarshal`에 잘못된 방식으로, 즉, 포인터가 아닌 값이나 `nil` 값을 전달하는 경우 경고합니다.
이는 기존의 `encoding/json.Unmarshal` 및 `encoding/xml.Unmarshal`에 대한 검사와 유사합니다.

## 런타임 {#runtime}

새로운 [`runtime/metrics`](/pkg/runtime/metrics/) 패키지는 Go 런타임에서 구현 정의된 메트릭을 읽기 위한 안정적인 인터페이스를 제공합니다.
이는 기존 함수인
[`runtime.ReadMemStats`](/pkg/runtime/#ReadMemStats) 및
[`debug.GCStats`](/pkg/runtime/debug/#GCStats)를 대체하며, 훨씬 더 일반적이고 효율적입니다.
자세한 내용은 패키지 문서를 참조하십시오.

<!-- CL 254659 -->
`GODEBUG` 환경 변수를 `inittrace=1`로 설정하면, 런타임이 각 패키지의 `init` 실행 시간을 요약하고 메모리 할당 정보를 표준 오류 스트림에 단일 줄로 출력합니다. 이 트레이스를 사용하여 Go 시작 성능의 병목 현상이나 오류를 찾을 수 있습니다.
[`GODEBUG`
문서](/pkg/runtime/#hdr-Environment_Variables)에서 형식을 설명합니다.

<!-- CL 267100 -->
Linux에서, 런타임은 이제 운영 체제에 메모를 즉시(MADV_DONTNEED 사용) 할당하도록 설정되어,
운영 체제가 메모 부족 상태일 때(MADV_FREE 사용)처럼 지연시키는 대신입니다.
이는 Go 프로세스가 사용하는 실제 메모의 양을 보다 정확하게 반영하는 프로세스 수준의 메모 통계(예: RSS)를 의미합니다.
현재 `GODEBUG=madvdontneed=1`을 사용하여 메모 모니터링 동작을 개선하는 시스템에서는
이 환경 변수를 설정할 필요가 없습니다.

<!-- CL 220419, CL 271987 -->
Go 1.16은 race detector와 [Go 메모리 모델](/ref/mem) 간의 불일치를 수정합니다. race detector는 이제 메모리 모델의 채널 동기화 규칙을 보다 정확하게 따릅니다. 결과적으로, detector는 이전에 감지하지 못했던 race를 이제 감지할 수 있습니다.

## 컴파일러

<!-- CL 256459, CL 264837, CL 266203, CL 256460 -->
컴파일러는 이제 레이블이 지정되지 않은 `for` 루프, 메서드 값, 및 타입 스위치와 함께 함수를 인라인할 수 있습니다. 인라인 기능은 또한 인라인이 가능한 더 많은 간접 호출을 감지할 수 있습니다.

## 링커 {#linker}

<!-- CL 248197 -->
이 릴리스에는 Go 링커에 대한 추가 개선 사항이 포함되어 있으며, 링커의 리소스 사용량(시간 및 메모리 모두)을 줄이고 코드의 견고성/유지보수성을 향상시킵니다. 이러한 변경 사항은 Go 링커를 현대화하는 두 릴리스 프로젝트의 두 번째 부분입니다. 자세한 내용은 [더 나은 링커](/s/better-linker)를 참조하십시오.

링크러의 변경 사항 (1.16)은 1.15의 개선 사항을 모든 지원되는 아키텍처/OS 조합에 적용합니다 (1.15의 성능 개선은 주로 `ELF`-기반 OS 및 `amd64` 아키텍처에 집중되었습니다). 대표적인 대규모 Go 프로그램의 경우, 링크는 1.15보다 20-25% 더 빠르고, `linux/amd64`에서 평균적으로 5-15% 더 적은 메모리를 사용합니다. 다른 아키텍처 및 OS에서는 더 큰 개선이 이루어집니다. 또한, 더 적극적인 심볼 정리로 인해 대부분의 바이너리가 더 작아집니다.

<!-- CL 255259 -->
Windows에서, `go build -buildmode=c-shared` 명령은 기본적으로 Windows용 ASLR DLL을 생성합니다. ASLR 기능을 `--ldflags=-aslr=false` 옵션을 사용하여 비활성화할 수 있습니다.

## 표준 라이브러리 {#library}

### 내장 파일 {#library-embed}

새로운 [`embed`](/pkg/embed/) 패키지는 컴파일 시 프로그램에 포함된 파일을 접근하는 기능을 제공합니다.
이는 새로운 [`//go:embed` 지시어](#embed)를 사용합니다.

### 파일 시스템 {#fs}

새로운 [`io/fs`](/pkg/io/fs/) 패키지는
[`fs.FS`](/pkg/io/fs/#FS) 인터페이스를 정의하며, 이는 읽기 전용 파일 트리의 추상화입니다.
표준 라이브러리 패키지는 이 인터페이스를 적절하게 활용하도록 수정되었습니다.

생성자 측 인터페이스에서,
새로운 [`embed.FS`](/pkg/embed/#FS) 타입은 `fs.FS` 인터페이스를 구현하며,
`zip.Reader`](/pkg/archive/zip/#Reader)도 `fs.FS` 인터페이스를 구현합니다.
새로운 [`os.DirFS`](/pkg/os/#DirFS) 함수는 운영 체제 파일의 트리를 기반으로 `fs.FS` 인터페이스의 구현을 제공합니다.

소비자 측면에서,
새로운 [`http.FS`](/pkg/net/http/#FS)
함수는 `fs.FS`를
[`http.FileSystem`](/pkg/net/http/#FileSystem)로 변환합니다.
또한, [`html/template`](/pkg/html/template/) 및 [`text/template`](/pkg/text/template/) 패키지의 [`ParseFS`](/pkg/html/template/#ParseFS) 함수 및 메서드는 `fs.FS`에서 템플릿을 읽습니다.

`fs.FS`를 구현하는 코드를 테스트하는 경우,
새로운 [`testing/fstest`](/pkg/testing/fstest/)
패키지는 [`TestFS`](/pkg/testing/fstest/#TestFS)
함수를 제공합니다. 이 함수는 일반적인 오류를 감지하고 보고합니다.
또한, `fs.FS` 구현을 사용하는 코드를 테스트하는 데 유용한 간단한 인메모리 파일 시스템 구현인
[`MapFS`](/pkg/testing/fstest/#MapFS)를 제공합니다.

### `io/ioutil` 패키지의 폐기

[`io/ioutil`](/pkg/io/ioutil/) 패키지는
잘 정의되지 않고 이해하기 어려운 기능들의 모음으로
결론되었습니다. 패키지가 제공하는 모든 기능이 다른 패키지로 이동되었습니다.
`io/ioutil` 패키지는 계속 작동하지만, 새로운 코드는
[`io`](/pkg/io/) 및 [`os`](/pkg/os/) 패키지에 있는 새로운 정의를 사용하는 것을 권장합니다.
다음은 `io/ioutil`에서 내보낸 이름의 새로운 위치 목록입니다:

- [`Discard`](/pkg/io/ioutil/#Discard)
    => [`io.Discard`](/pkg/io/#Discard)
  - [`NopCloser`](/pkg/io/ioutil/#NopCloser)
    => [`io.NopCloser`](/pkg/io/#NopCloser)
  - [`ReadAll`](/pkg/io/ioutil/#ReadAll)
    => [`io.ReadAll`](/pkg/io/#ReadAll)
  - [`ReadDir`](/pkg/io/ioutil/#ReadDir)
    => [`os.ReadDir`](/pkg/os/#ReadDir)
    (참고:
    [`os.DirEntry`](/pkg/os/#DirEntry)
    슬라이스를 반환하며,
    [`fs.FileInfo`](/pkg/io/fs/#FileInfo)
    슬라이스를 반환하지 않습니다)
  - [`ReadFile`](/pkg/io/ioutil/#ReadFile)
    => [`os.ReadFile`](/pkg/os/#ReadFile)
  - [`TempDir`](/pkg/io/ioutil/#TempDir)
    => [`os.MkdirTemp`](/pkg/os/#MkdirTemp)
  - [`TempFile`](/pkg/io/ioutil/#TempFile)
    => [`os.CreateTemp`](/pkg/os/#CreateTemp)
  - [`WriteFile`](/pkg/io/ioutil/#WriteFile)
    => [`os.WriteFile`](/pkg/os/#WriteFile)

### 라이브러리의 미세 조정 {#minor_library_changes}

물론, 라이브러리에는 항상 다양한 미세한 변경 사항과 업데이트가 있으며, 이는 Go 1의 [호환성](https://doc/go1compat)을 염두에 두고 이루어졌습니다.

#### [archive/zip](/pkg/archive/zip/)

<!-- CL 243937 -->
새로운 `Reader.Open` 메서드는 `fs.FS` 인터페이스를 구현합니다.

#### [crypto/dsa](/pkg/crypto/dsa/)

<!-- CL 257939 -->
`crypto/dsa` 패키지는 이제 더 이상 사용되지 않습니다.
자세한 내용은 [이슈 #40337](/issue/40337)를 참조하세요.

<!-- crypto/dsa -->

#### [crypto/hmac](/pkg/crypto/hmac/)

<!-- CL 261960 -->
[`New`](/pkg/crypto/hmac/#New)는 이제 해시 생성 함수에 대한 별도의 호출이 새 값을 반환하지 못할 경우에 패닉(panic)을 발생시킵니다.
이전에는 동작이 정의되지 않았고, 때로는 유효하지 않은 결과가 생성되었습니다.

<!-- crypto/hmac -->

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 256897 -->
닫히거나 닫힌 TLS 연결에 대한 I/O 작업이 이제 `net.ErrClosed` 오류를 사용하여 감지할 수 있습니다. (`net.ErrClosed` ([/pkg/net/#ErrClosed](https://example.com/pkg/net/#ErrClosed)) 참조). 일반적인 사용 예는 `errors.Is(err, net.ErrClosed)`입니다.

<!-- CL 266037 -->
기본적인 쓰기 마감 시간이 `Conn.Close`에서 설정되어
"close notify" 알림을 보내기 전에 설정됩니다. 이는 무한정 멈추는 것을 방지하기 위함입니다.

<!-- CL 239748 -->
클라이언트는 이제 서버가 클라이언트에서 광고한 목록에 없는
[
ALPN 프로토콜](/pkg/crypto/tls/#ConnectionState.NegotiatedProtocol)을 선택하는 경우 handshake 오류를 반환합니다.

<!-- CL 262857 -->
서버는 이제 AES 하드웨어 지원이 없으면, 클라이언트 또는 서버 중 어느 쪽이든 AES 암호화 모음(예: ChaCha20Poly1305)을 지원하지 않는 경우, AES-GCM 암호화 모음 대신 다른 사용 가능한 AEAD 암호화 모음을 선호합니다. 단, 다음 두 가지 설정이 모두 활성화된 경우에만 해당합니다.
```
[Config.PreferServerCipherSuites](pkg/crypto/tls/#Config.PreferServerCipherSuites)
```
및
```
[Config.CipherSuites](pkg/crypto/tls/#Config.CipherSuites)
```
클라이언트는 AES-GCM 암호화 모음을 선호하지 않는 경우 AES 하드웨어 지원이 없다고 가정합니다.

<!-- CL 246637 -->
[`Config.Clone`](/pkg/crypto/tls/#Config.Clone) 메서드가 이제
수신 객체가 nil인 경우 panic() 대신 nil을 반환합니다.

<!-- crypto/tls -->

#### [crypto/x509](/pkg/crypto/x509/)

`GODEBUG=x509ignoreCN=0` 플래그는 Go 1.17에서 제거됩니다.
이는 X.509 인증서의 `CommonName` 필드를 호스트 이름으로 처리하는 기존 동작을 활성화합니다.

<!-- CL 235078 -->
[`ParseCertificate`](/pkg/crypto/x509/#ParseCertificate) 및
[`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate)
함수는 이제 `DNSNames`, `EmailAddresses`, `URIs` 필드에 대한 문자 인코딩 제한을 적용합니다. 이러한 필드에는 ASCII 범위 내의 문자만 포함할 수 있습니다.

<!-- CL 259697 -->
[`CreateCertificate`](/pkg/crypto/x509/#CreateCertificate)
이제 생성된 인증서의 서명을 생성자의
공개 키를 사용하여 확인합니다. 서명이 유효하지 않으면, 잘못된 인증서 대신 오류가 반환됩니다.

<!-- CL 257939 -->
DSA 서명 검증이 더 이상 지원되지 않습니다. 참고로 DSA 서명 생성은 이전부터 지원되지 않았습니다.
자세한 내용은 [문제 #40337](/issue/40337)를 참조하십시오.

<!-- CL 257257 -->
Windows에서, [`Certificate.Verify`](/pkg/crypto/x509/#Certificate.Verify)
는 이제 플랫폼 인증 팩트 확인기로 구성된 모든 인증서 체인을 반환합니다. 이전에는 최고 순위의 체인만 반환했습니다.

<!-- CL 262343 -->
새로운 `SystemRootsError.Unwrap`
메서드는 `Err` 필드에 액세스할 수 있도록 `errors` 패키지의 함수를 사용합니다. (참조: `/pkg/crypto/x509/#SystemRootsError.Unwrap`)

<!-- CL 230025 -->
유닉스 시스템에서 `crypto/x509` 패키지는 시스템 인증서 풀의 복사본을 저장하는 데 더 효율적입니다.
작은 수의 루트 인증서만 사용하는 프로그램은 약 50MB 정도의 메모리를 덜 사용합니다.

<!-- crypto/x509 -->

#### [debug/elf](/pkg/debug/elf/)

<!-- CL 255138 -->
더 많은 [`DT`](/pkg/debug/elf/#DT_NULL) 및 [`PT`](/pkg/debug/elf/#PT_NULL) 상수가 추가되었습니다.

<!-- 디버깅/ELF -->

#### [encoding/asn1](/pkg/encoding/asn1)

<!-- CL 255881 -->
[`Unmarshal`](/pkg/encoding/asn1/#Unmarshal) 및
[`UnmarshalWithParams`](/pkg/encoding/asn1/#UnmarshalWithParams)
함수는 이제 인수가 포인터가 아니거나 `nil`인 경우 예외를 발생시키는 대신 오류를 반환합니다. 이 변경 사항은 [`encoding/json`](/pkg/encoding/json)과 같은 다른 인코딩 패키지의 동작과 일치합니다.

#### [encoding/json](/pkg/encoding/json/)

<!-- CL 234818 -->
`json` 구조체 필드 태그가 `Marshal` ( /pkg/encoding/json/#Marshal),
`Unmarshal` ( /pkg/encoding/json/#Unmarshal),
및 관련 기능에서 인식되도록 변경되었습니다. 이제 Go 구조체 필드의 JSON 객체 이름에 세미콜론 문자를 포함할 수 있습니다.

<!-- encoding/json -->

#### [encoding/xml](/pkg/encoding/xml/)

<!-- CL 264024 -->
인코더는 항상 `xml`로 시작하는 네임스페이스 접두사를 사용하는 것을 피하도록 주의해 왔습니다. 이러한 접두사는 XML
사양에서 예약되어 있습니다.
이제 사양을 더 엄격하게 준수하기 위해, 이 확인은 대소문자를 구분하지 않게 되었습니다. 따라서 `XML`, `XmL`와 같은 접두사도 피하게 됩니다.

<!-- encoding/xml -->

#### [flag](/pkg/flag/)

<!-- CL 240014 -->
새로운 `Func` 함수
는 함수를 호출하여 플래그를 구현하는 기능을 등록할 수 있도록 합니다.
이는 `Value` 인터페이스를 구현하는 것보다 가벼운 대안입니다.

<!-- 플래그 -->

#### [go/build](/pkg/go/build/)

<!-- CL 243941, CL 283636 -->
`[`Package`](/pkg/go/build/#Package)
구조체는 패키지에 있는 `//go:embed` 지침에 대한 정보를 보고하는 새로운 필드를 가집니다:
[`EmbedPatterns`](/pkg/go/build/#Package.EmbedPatterns),
[`EmbedPatternPos`](/pkg/go/build/#Package.EmbedPatternPos),
[`TestEmbedPatterns`](/pkg/go/build/#Package.TestEmbedPatterns),
[`TestEmbedPatternPos`](/pkg/go/build/#Package.TestEmbedPatternPos),
[`XTestEmbedPatterns`](/pkg/go/build/#Package.XTestEmbedPatterns),
[`XTestEmbedPatternPos`](/pkg/go/build/#Package.XTestEmbedPatternPos).

<!-- CL 240551 -->
`Package` 필드
`IgnoredGoFiles`
이제 "\_" 또는 "."으로 시작하는 파일은 포함하지 않으며, 이러한 파일은 항상 무시됩니다.
`IgnoredGoFiles`는 빌드 제약 조건으로 인해 무시되는 파일에 사용됩니다.

<!-- CL 240551 -->
새로운 `[`Package`](/pkg/go/build/#Package)
필드 `[`IgnoredOtherFiles`](/pkg/go/build/#Package.IgnoredOtherFiles)는 빌드 제약 조건으로 인해 무시되는 비-Go 파일 목록을 포함합니다.

<!-- go/build -->

#### [go/build/constraint]

<!-- CL 240604 -->
새로운
[`go/build/constraint`](/pkg/go/build/constraint/)
패키지는 빌드 제약 조건 라인을 파싱합니다. 여기에는 원래
`// +build` 구문과 Go 1.17에서 도입될
`//go:build` 구문 모두 포함됩니다.
이 패키지는 Go 1.16으로 빌드된 도구가 Go 1.17 소스 코드를 처리할 수 있도록 하기 위해 존재합니다.
빌드 제약 구문 및 `//go:build` 구문으로의 계획된 전환에 대한 자세한 내용은 다음 링크를 참조하십시오:
[https://golang.org/design/draft-gobuild](https://golang.org/design/draft-gobuild)
참고: `//go:build` 라인은 Go 1.16에서는 **지원되지 않으며** 아직 Go 프로그램에 도입해서는 안 됩니다.

<!-- go/build/제약 -->

#### [html/template](pkg/html/template/)

<!-- CL 243938 -->
새로운 [`template.ParseFS`](/pkg/html/template/#ParseFS)
함수와 [`template.Template.ParseFS`](/pkg/html/template/#Template.ParseFS)
메서드는 [`template.ParseGlob`](/pkg/html/template/#ParseGlob)
와 [`template.Template.ParseGlob`](/pkg/html/template/#Template.ParseGlob)와 유사하지만, 템플릿을 [`fs.FS`](/pkg/io/fs/#FS)에서 읽습니다.

<!-- html/템플릿 -->

#### [io](/pkg/io/)

<!-- CL 261577 -->
이 패키지는 이제 `ReadSeekCloser` 인터페이스를 정의합니다.
[`ReadSeekCloser`](/pkg/io/#ReadSeekCloser)

<!-- CL 263141 -->
현재 패키지는 다음 함수들을 정의하며, 이는 `io/ioutil` 패키지의 동일한 이름으로 사용되던 것들을 대체합니다.
[`Discard`](/pkg/io/#Discard),
[`NopCloser`](/pkg/io/#NopCloser), 및
[`ReadAll`](/pkg/io/#ReadAll).

<!-- 입출력 -->

#### [log](/pkg/log/)

<!-- CL 264460 -->
새로운 `Default` 함수는 기본 `Logger`에 접근하는 기능을 제공합니다.

<!-- 로그 -->

#### [log/syslog](/pkg/log/syslog/)

<!-- CL 264297 -->
[`Writer`](/pkg/log/syslog/#Writer)
이제 사용자 지정 Unix 도메인 소켓에 로깅할 때,
호스트 이름(제거) 및 더 짧은 타임스탬프를 사용하여
기본 로그 소켓에 이미 사용되는 형식과 일치하는
로컬 메시지 형식을 사용합니다.

<!-- log/syslog -->

#### [mime/multipart](/pkg/mime/multipart/)

<!-- CL 247477 -->
`Reader`의
[`ReadForm`](/pkg/mime/multipart/#Reader.ReadForm)
메서드가 최대 `int64` 값을 한계로 전달할 때, 폼 데이터를 더 이상 거부하지 않습니다.

<!-- mime/multipart -->

#### [net](/pkg/net/)

<!-- CL 250357 -->
I/O가 닫힌 네트워크 연결 또는 I/O가 완료되기 전에 닫힌 네트워크 연결에서 발생하는 경우를 이제 `[`ErrClosed`](/pkg/net/#ErrClosed) 오류를 사용하여 감지할 수 있습니다. 일반적인 사용 방법은 `errors.Is(err, net.ErrClosed)`입니다.
이전 버전에서는 `Error` 메서드가 반환하는 문자열과 `"use of closed network connection"`를 일치시켜 이 경우를 신뢰성 있게 감지하는 유일한 방법이었습니다.

<!-- CL 255898 -->
이전 Go 릴리스에서는 Linux 시스템에서 `/proc/sys/net/core/somaxconn`을 통해 설정되는 기본 TCP 리스너의 백로그 크기 최대값이 `65535`로 제한되어 있었습니다.
Linux 커널 버전 4.1 이상에서는 최대값이 `4294967295`로 변경되었습니다.

<!-- CL 238629 -->
Linux에서 호스트 이름 조회는 `/etc/nsswitch.conf`이 없는 경우 `/etc/hosts`를 확인하기 전에 DNS를 사용하지 않습니다. 이는 musl 기반 시스템에서 흔히 발생하며, Go 프로그램이 해당 시스템에서 C 프로그램과 동일한 동작을 갖도록 합니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- CL 233637 -->
[`net/http`](/pkg/net/http/) 패키지에서, [`StripPrefix`](/pkg/net/http/#StripPrefix) 함수의 동작이 변경되어, 요청 URL의 `RawPath` 필드뿐만 아니라 `Path` 필드에서도 접두사를 제거하도록 변경되었습니다.
이전 버전에서는 `Path` 필드만 잘렸기 때문에, 요청 URL에 이스케이프된 문자가 포함되어 있는 경우, `Path`와 `RawPath` 필드가 일치하지 않도록 URL이 수정되었습니다.
Go 1.16에서는 `StripPrefix`가 두 필드를 모두 잘립니다.
요청 URL의 접두사 부분에 이스케이프된 문자가 있는 경우, 이전 동작 대신 404 오류를 반환합니다.

<!-- CL 252497 -->
`net/http` 패키지는 이제 `"Range": "bytes=--N"` 형식의 HTTP 범위 요청을 거부합니다. 여기서 `"--N"`은 음수 길이 접미사입니다(예: `"Range": "bytes=--2"`)입니다. 이제 `416 "Range Not Satisfiable"` 응답을 반환합니다.

<!-- CL 256498, golang.org/issue/36990 -->
[`SameSiteDefaultMode`](/pkg/net/http/#SameSiteDefaultMode)로 설정된 쿠키는
현재 사양에 따라 동작하며, 값을 지정하지 않고 SameSite 키를 생성하는 대신,
특성을 설정하지 않습니다.

<!-- CL 250039 -->
`[Client](pkg/net/http/#Client)`는 이제 빈 본체를 가진 `PATCH` 요청에서 명시적인 `Content-Length:` 헤더를 `0`으로 설정하여, 기존의 `POST` 및 `PUT` 요청의 동작과 일치하도록 변경되었습니다.

<!-- CL 249440 -->
`[`ProxyFromEnvironment`](/pkg/net/http/#ProxyFromEnvironment)
함수는 `https://` URL에 대해 `HTTPS_PROXY` 환경 변수가 설정되지 않은 경우, `HTTP_PROXY` 환경 변수의 값을 더 이상 반환하지 않습니다.

<!-- 259917 -->
`Transport`
형에 새로운 필드인
`GetProxyConnectHeader`가 추가되었습니다.
(`/pkg/net/http/#Transport.GetProxyConnectHeader`)
이 필드는 `CONNECT` 요청 중에 프록시에 전송할 헤더를 반환하는 함수로 설정할 수 있습니다.
실제로 `GetProxyConnectHeader`는 기존 필드인
`ProxyConnectHeader`의 동적 버전입니다.
만약 `GetProxyConnectHeader`가 `nil`이 아니면, `ProxyConnectHeader`는 무시됩니다.

<!-- CL 243939 -->
새로운 [`http.FS`](/pkg/net/http/#FS)
함수는 [`fs.FS`](/pkg/io/fs/#FS)
를 [`http.FileSystem`](/pkg/net/http/#FileSystem)
로 변환합니다.

<!-- net/http -->

#### [net/http/httputil](/pkg/net/http/httputil/)

<!-- CL 260637 -->
[`ReverseProxy`](/pkg/net/http/httputil/#ReverseProxy)
이제 알려지지 않은 바디 길이를 가진 스트리밍 응답을 프록시할 때 버퍼링된 데이터를 더 적극적으로 플러시합니다.

<!-- net/http/httputil -->

#### [net/smtp](/pkg/net/smtp/)

<!-- CL 247257 -->
`Client`의
[`Mail`](/pkg/net/smtp/#Client.Mail)
메서드는 이제 `SMTPUTF8` 지시어를 지원하는 서버에 보내어, 주소가 UTF-8로 인코딩되었음을 나타냅니다.

```markdown
<!-- net/smtp -->
```

#### [os](/pkg/os/)

<!-- CL 242998 -->
`Process.Signal` ([`Process.Signal`](/pkg/os/#Process.Signal) 이제
`ErrProcessDone` ([`ErrProcessDone`](/pkg/os/#ErrProcessDone))를 반환하는 대신,
프로세스가 이미 종료되었을 때
숨겨진 `errFinished`를 반환하는 대신.

<!-- CL 261540 -->
이 패키지는 [`DirEntry`](/pkg/os/#DirEntry) 타입을 정의하고, 이는 [`fs.DirEntry`](/pkg/io/fs/#DirEntry)의 별칭입니다.
새로운 [`ReadDir`](/pkg/os/#ReadDir) 함수와 새로운
[`File.ReadDir`](/pkg/os/#File.ReadDir) 메서드는 디렉토리의 내용을 `DirEntry` 슬라이스로 읽는 데 사용될 수 있습니다.
[`File.Readdir`](/pkg/os/#File.Readdir) 메서드 (참고: `dir`에 대문자 `d`를 사용)는 여전히 존재하며, `FileInfo` 슬라이스를 반환하지만, 대부분의 프로그램에서는 `File.ReadDir`으로 전환하는 것이 더 효율적입니다.

<!-- CL 263141 -->
이 패키지는 다음과 같은 함수를 정의하며, 이를 `io/ioutil` 패키지에 정의된 함수 대신 사용합니다.
[`CreateTemp`](/pkg/os/#CreateTemp),
[`MkdirTemp`](/pkg/os/#MkdirTemp),
[`ReadFile`](/pkg/os/#ReadFile),
[`WriteFile`](/pkg/os/#WriteFile)

<!-- CL 243906 -->
`FileInfo`, `FileMode` 및 `PathError` 유형은 이제 `io/fs` 패키지의 동일한 이름을 가진 유형에 대한 별칭입니다.
`os` 패키지의 함수 시그니처는 `io/fs` 패키지의 이름으로 업데이트되었습니다.
이 변경은 기존 코드에 영향을 미치지 않아야 합니다.

<!-- CL 243911 -->
새로운 `[DirFS](pkg/os/#DirFS)` 함수는
`[fs.FS](pkg/io/fs/#FS)` 인터페이스를 구현하며,
운영 체제 파일로 구성된 트리 기반으로 동작합니다.

<!-- os -->

#### [os/signal](/pkg/os/signal/)

<!-- CL 219640 -->
새로운
[`NotifyContext`](/pkg/os/signal/#NotifyContext)
함수는 특정 신호가 도착하면 컨텍스트가 취소되도록 컨텍스트를 만드는 것을 허용합니다.

<!-- os/신호 -->

#### [경로](/pkg/path/)

<!-- CL 264397, golang.org/issues/28614 -->
`Match` 함수는 이제 패턴의 일치하지 않는 부분이 구문 오류를 가질 경우 오류를 반환합니다. 이전 버전에서는 함수가 일치에 실패하면 조기에 반환되었기 때문에 패턴에 있는 이후의 구문 오류는 보고되지 않았습니다.

<!-- 경로 -->

#### [path/filepath](/pkg/path/filepath/)

<!-- CL 267887 -->
새로운 함수
[`WalkDir`](/pkg/path/filepath/#WalkDir)
은
[`Walk`](/pkg/path/filepath/#Walk)
과 유사하지만, 일반적으로 더 효율적입니다.
`WalkDir`에 전달되는 함수는
[`fs.DirEntry`](/pkg/io/fs/#DirEntry)
을 받지만,
[`fs.FileInfo`](/pkg/io/fs/#FileInfo)
를 받지 않습니다.
(만약 `Walk` 함수가
[`os.FileInfo`](/pkg/os/#FileInfo)
를 받는 것으로 기억하는 경우,
`os.FileInfo`는 이제 `fs.FileInfo`의 별칭입니다.)

<!-- CL 264397, golang.org/issues/28614 -->
`Match` 및 `Glob` 함수는 패턴의 일치하지 않는 부분이 구문 오류를 가질 경우 이제 오류를 반환합니다. 이전에는 함수가 실패한 매치에서 조기에 종료되었기 때문에 패턴의 나중에 발생하는 구문 오류는 보고되지 않았습니다.

<!-- path/경로 -->

#### [reflect](/pkg/reflect/)

<!-- CL 192331 -->
`Zero` 함수가 최적화되어 할당을 피하도록 변경되었습니다. 반환된 `Value`를 다른 `Value`와 비교하는 코드는 이전 Go 버전에서 얻은 결과와 다를 수 있습니다. 특히 `==` 또는 `DeepEqual`을 사용하는 경우, `reflect.Value`에 대한 설명서([`reflect.Value`](/pkg/reflect#Value))에서 두 개의 `Value`를 올바르게 비교하는 방법을 설명합니다.

<!-- 반사 -->

#### [runtime/debug](/pkg/runtime/debug/)

<!-- CL 249677 -->
`runtime.Error` 값은 `SetPanicOnFault`가 활성화될 때 사용되는 경우 이제 `Addr` 메서드를 가질 수 있습니다. 해당 메서드가 존재하면, 오류를 발생시킨 메모리 주소를 반환합니다.

<!-- 실행/디버깅 -->

#### [strconv](/pkg/strconv/)

<!-- CL 260858 -->
[`ParseFloat`](/pkg/strconv/#ParseFloat)가 이제
[Eisel-Lemire
알고리즘](https://nigeltao.github.io/blog/2020/eisel-lemire.html)을 사용하며, 성능을 최대 2배 향상시킵니다. 이를 통해 [`encoding/json`](/pkg/encoding/json/)과 같은 텍스트 형식의 디코딩 속도를 향상시킬 수도 있습니다.

<!-- strconv -->

#### [syscall](/pkg/syscall/)

<!-- CL 263271 -->
[`NewCallback`](/pkg/syscall/?GOOS=windows#NewCallback)
과
[`NewCallbackCDecl`](/pkg/syscall/?GOOS=windows#NewCallbackCDecl)
이제 여러 개의
`uintptr`-크기의 서브 인자를 순차적으로 전달하는 콜백 함수를 올바르게 지원합니다. 이를 위해서는 이러한 함수를 사용하는 방식에서 작은 인자 사이의 수동 패딩을 제거해야 할 수 있습니다.

<!-- CL 261917 -->
`SysProcAttr` (`/pkg/syscall/?GOOS=windows#SysProcAttr`) 에서 Windows에서는 새로운 `NoInheritHandles` 필드가 새 프로세스를 생성할 때 핸들 상속을 비활성화합니다.

<!-- CL 269761, golang.org/issue/42584 -->
[`DLLError`](/pkg/syscall/?GOOS=windows#DLLError) (Windows에서) 이제 자체 오류를 해체하기 위한 `Unwrap` 메서드를 갖습니다.

<!-- CL 210639 -->
리눅스에서,
[`Setgid`](/pkg/syscall/#Setgid),
[`Setuid`](/pkg/syscall/#Setuid),
그리고 관련된 호출이 이제 구현되었습니다.
이전에, 이들은 `syscall.EOPNOTSUPP` 오류를 반환했습니다.

<!-- CL 210639 -->
Linux에서, 새로운 함수
[`AllThreadsSyscall`](/pkg/syscall/#AllThreadsSyscall)
와 [`AllThreadsSyscall6`](/pkg/syscall/#AllThreadsSyscall6)를 사용하여 프로세 내의 모든 Go 스레드에서 시스템 호출을 수행할 수 있습니다.
이 함수는 cgo를 사용하지 않는 프로그램에서만 사용할 수 있습니다.
만약 프로그램이 cgo를 사용한다면, 항상
[`syscall.ENOTSUP`](/pkg/syscall/#ENOTSUP)를 반환합니다.

<!-- syscall -->

#### [testing/iotest](/pkg/testing/iotest/)

<!-- CL 199501 -->
새로운
[`ErrReader`](/pkg/testing/iotest/#ErrReader)
함수는 항상 오류를 반환하는
[`io.Reader`](/pkg/io/#Reader)를 반환합니다.

<!-- CL 243909 -->
새로운
[`TestReader`](/pkg/testing/iotest/#TestReader)
함수는
[`io.Reader`](/pkg/io/#Reader)
이 올바르게 작동하는지 테스트합니다.

<!-- testing/iotest -->

#### [text/template](pkg/text/template/)

<!-- CL 254257, golang.org/issue/29770 -->
새 줄 문자가 이제 액션 구분자 내부에 허용됩니다.
이를 통해 액션이 여러 줄에 걸쳐 표현할 수 있습니다.

<!-- CL 243938 -->
새로운 `[template.ParseFS](pkg/text/template#/ParseFS)`
함수와 `[template.Template.ParseFS](pkg/text/template#/Template.ParseFS)`
메서드는 `[template.ParseGlob](pkg/text/template#/ParseGlob)`
과 `[template.Template.ParseGlob](pkg/text/template#/Template.ParseGlob)`과 유사하지만, 템플릿을 `[fs.FS](pkg/io/fs#/FS)`에서 읽습니다.

<!-- 텍스트/템플릿 -->

#### [text/template/parse](/pkg/text/template/parse/)

<!-- CL 229398, golang.org/issue/34652 -->
새로운 [`CommentNode`](/pkg/text/template/parse/#CommentNode)가 파싱 트리에 추가되었습니다. `parse.Tree`의 `Mode` 필드를 통해 이를 사용할 수 있습니다.

<!-- text/template/parse -->

#### [time/tzdata](/pkg/time/tzdata/)

<!-- CL 261877 -->
얇은 시간대 데이터 형식은 `$GOROOT/lib/time/zoneinfo.zip`에 있는 시간대 데이터베이스와 이 패키지에 포함된 복사본에 사용됩니다. 이를 통해 시간대 데이터베이스의 크기가 약 350KB 줄어듭니다.

<!-- time/tzdata -->

#### [unicode](/pkg/unicode/)

<!-- CL 248765 -->
[`unicode`](/pkg/unicode/) 패키지와 시스템 전체에 걸쳐 있는 관련
지원 기능이 Unicode 12.0.0에서 Unicode 13.0.0으로 업그레이드되었습니다.
이 업데이트는 5,930개의 새로운 문자, 4개의 새로운 스크립트 및 55개의 새로운 이모지를 포함합니다.
Unicode 13.0.0은 U+30000부터 U+3FFFF까지의 3번째 플레인을 제3의 이데오그래픽 플레인으로 지정합니다.

<!-- unicode -->
