<!--
참고: 이 문서 및 이 디렉토리의 다른 문서들에서는
`hello` `world`와 같이 고정폭 구문을 비고정폭 공백으로 설정하는 것이 관례입니다.
이러한 구문에서 내부 태그를 제거하는 CL을 보내지 마십시오.
-->

제공해주신 내용이 스타일 시트뿐이라 번역할 텍스트가 없지만, 요청하신 지침에 따라 기술 번역을 수행할 준비가 되어 있습니다. 번역할 Markdown 콘텐츠를 제공해 주세요.

## Go 1.11 소개 {#introduction}

최신 Go 릴리스인 버전 1.11이 [Go 1.10](go1.10) 출시 6개월 만에 공개되었습니다.
변경 사항의 대부분은 툴체인, 런타임 및 라이브러리의 구현에 집중되어 있습니다.
언제나 그렇듯, 이번 릴리스에서도 Go 1의 [호환성 약속](/doc/go1compat.html)을 유지합니다.
거의 모든 Go 프로그램이 이전과 동일하게 컴파일되고 실행될 것으로 기대합니다.

## 언어 변경 사항 {#language}

언어 사양에는 변경 사항이 없습니다.

## 포트 {#ports}

<!-- CL 94255, CL 115038, etc -->
[Go 1.10 릴리스 노트](go1.10#ports)에서 발표한 바와 같이, Go 1.11부터는 OpenBSD 6.2 이상, macOS 10.10 Yosemite 이상, 또는 Windows 7 이상이 필요합니다. 이전 버전의 운영 체제에 대한 지원은 제거되었습니다.

<!-- CL 121657 -->
Go 1.11은 출시 예정인 OpenBSD 6.4 버전을 지원합니다. OpenBSD 커널의 변경 사항으로 인해, 이전 버전의 Go는 OpenBSD 6.4에서 작동하지 않습니다.

i386 하드웨어에서 NetBSD를 사용할 때 [알려진 문제](/issue/25206)들이 있습니다.

<!-- CL 107935 -->
이제 `linux/ppc64le`에서 race detector를 지원하며, `netbsd/amd64`에서도 제한적으로 지원합니다. NetBSD의 race detector 지원에는 [알려진 문제](/issue/26403)가 있습니다.

<!-- CL 109255 -->
이제 `linux/arm64`에서 메모리 새니타이저(`-msan`)를 지원합니다.

<!-- CL 93875 -->
이제 `freebsd/amd64`에서 빌드 모드 `c-shared` 및 `c-archive`가 지원됩니다.

<!-- CL 108475 -->
64비트 MIPS 시스템에서는 새로운 환경 변수 설정인
`GOMIPS64=hardfloat`(기본값)와
`GOMIPS64=softfloat`를 통해 부동 소수점 계산에
하드웨어 명령어를 사용할지 또는 소프트웨어 에뮬레이션을 사용할지 선택합니다.
32비트 시스템의 경우, [Go 1.10에서 추가된](go1.10#mips) 바와 같이 환경 변수는 여전히 `GOMIPS`입니다.

<!-- CL 107475 -->
소프트 플로트(soft-float) ARM 시스템(`GOARM=5`)에서 Go가 이제 더 효율적인 소프트웨어 부동 소수점 인터페이스를 사용합니다. 이는 Go 코드에는 투명하게 적용되지만, GOARM으로 보호되지 않은 부동 소수점 명령어를 사용하는 ARM 어셈블리는 작동하지 않으며 [새 인터페이스](/cl/107475)로 포팅되어야 합니다.

<!-- CL 94076 -->
ARMv7의 Go 1.11은 더 이상 `KUSER_HELPERS`로 설정된 Linux 커널을 요구하지 않습니다. 이 설정은 기본 커널 구성에서는 활성화되어 있지만, 경량화된(stripped-down) 구성에서는 때때로 비활성화되기도 합니다.

### WebAssembly {#wasm}

Go 1.11에서는 [WebAssembly](https://webassembly.org)(`js/wasm`)로의 실험적인 포트가 추가되었습니다.

현재 Go 프로그램은 고루틴 스케줄링, 가비지 컬렉션, 맵 등을 위한 Go 런타임이 포함된 하나의 WebAssembly 모듈로 컴파일됩니다.

그 결과, 결과물의 크기는 최소 약 2MB(압축 시 500KB) 정도입니다. Go 프로그램은 새로운 실험적 패키지인 [`syscall/js`](/pkg/syscall/js/)를 사용하여 JavaScript를 호출할 수 있습니다.

바이너리 크기와 다른 언어와의 상호 운용성은 아직 우선순위가 아니었으나, 향후 릴리스에서 다뤄질 수 있습니다.

새로운 `GOOS` 값 "`js`"와 `GOARCH` 값 "`wasm`"이 추가됨에 따라, `*_js.go` 또는 `*_wasm.go`라는 이름의 Go 파일은 해당 GOOS/GOARCH 값이 사용될 때를 제외하고는 이제 [Go 도구에서 무시됩니다](/pkg/go/build/#hdr-Build_Constraints).
해당 패턴과 일치하는 기존 파일 이름이 있는 경우, 파일 이름을 변경해야 합니다.

더 자세한 정보는 [WebAssembly 위키 페이지](/wiki/WebAssembly)에서 확인하실 수 있습니다.

### RISC-V GOARCH 예약 값 {#riscv}

<!-- CL 106256 -->
메인 Go 컴파일러는 아직 RISC-V 아키텍처를 지원하지 않지만 <!-- is gonna change everything -->
RISC-V를 지원하는 Gccgo에서 사용하는 `GOARCH` 값인
"`riscv`"와 "`riscv64`"를 예약해 두었습니다. 이는 이제
`*_riscv.go`라는 이름의 Go 파일들이 해당 GOOS/GOARCH 값이
사용될 때를 제외하고는 [Go 도구에 의해](/pkg/go/build/#hdr-Build_Constraints)
무시됨을 의미합니다.

## 도구 {#tools}

### 모듈, 패키지 버전 관리 및 의존성 관리 {#modules}

Go 1.11은 GOPATH의 대안이자 버전 관리 및 패키지 배포 지원 기능이 통합된 [“모듈(modules)”이라는 새로운 개념](/cmd/go/#hdr-Modules__module_versions__and_more)에 대한 예비 지원을 추가합니다.
모듈을 사용하면 개발자는 더 이상 GOPATH 내부에서만 작업할 필요가 없으며, 버전 의존성 정보가 명시적이면서도 가볍게 유지되고, 빌드의 신뢰성과 재현성이 높아집니다.

모듈 지원은 실험적인 것으로 간주됩니다.
Go 1.11 사용자들의 피드백에 따라 세부 사항이 변경될 가능성이 높으며, 추가적인 도구들을 계획하고 있습니다.
모듈 지원의 세부 사항은 변경될 수 있지만, Go 1.11을 사용하여 모듈로 전환한 프로젝트는 Go 1.12 및 이후 버전에서도 계속 작동합니다.
모듈 사용 중 버그를 발견하시면, 저희가 수정할 수 있도록 [이슈를 제출](/issue/new)해 주세요. 자세한 내용은 [`go` 명령 문서](/cmd/go#hdr-Modules__module_versions__and_more)를 참조하십시오.

### 임포트 경로 제한 {#importpath}

Go 모듈 지원으로 인해 명령줄 작업에서 `@` 기호에 특별한 의미가 부여됨에 따라, 이제 `go` 명령어는 `@` 기호를 포함하는 임포트 경로(import paths)의 사용을 허용하지 않습니다.
이러한 임포트 경로는 `go get`에서도 허용된 적이 없으므로, 이 제한은 다른 수단으로 커스텀 GOPATH 트리를 구축하는 사용자에게만 영향을 미칠 수 있습니다.

### 패키지 로딩 {#gopackages}

새로운 패키지 [`golang.org/x/tools/go/packages`](https://godoc.org/golang.org/x/tools/go/packages)는 Go 소스 코드 패키지를 찾고 로드하기 위한 간단한 API를 제공합니다. 아직 표준 라이브러리의 일부는 아니지만, 많은 작업에서 모듈을 완전히 지원하지 못하는 [`go/build`](/pkg/go/build) 패키지를 효과적으로 대체합니다. 이 패키지는 Go 패키지에 대한 정보를 얻기 위해 [`go list`](/cmd/go/#hdr-List_packages)와 같은 외부 쿼리 명령을 실행하므로, [Bazel](https://bazel.build) 및 [Buck](https://buckbuild.com)과 같은 대체 빌드 시스템에서도 동일하게 잘 작동하는 분석 도구를 구축할 수 있게 해줍니다.

### 빌드 캐시 요구 사항 {#gocache}

Go 1.11은 Go 1.10에서 도입된 [빌드 캐시](/cmd/go/#hdr-Build_and_test_caching)를 비활성화하기 위해 환경 변수 `GOCACHE=off`를 설정하는 기능을 지원하는 마지막 릴리스가 됩니다.

Go 1.12부터는 `$GOPATH/pkg`를 제거하기 위한 단계의 일환으로 빌드 캐시가 필수적으로 요구됩니다. 위에 설명된 모듈 및 패키지 로딩 지원은 이미 빌드 캐시가 활성화되어 있을 것을 전제로 합니다.

문제를 피하기 위해 빌드 캐시를 비활성화하셨다면, [이슈를 제출](/issue/new)하여 저희에게 알려주시기 바랍니다.

### 컴파일러 툴체인 {#compiler}

<!-- CL 109918 -->
이제 `panic`을 호출하는 함수를 포함하여 더 많은 함수가 기본적으로 인라이닝(inlining) 대상이 됩니다.

<!-- CL 97375 -->
이제 컴파일러 툴체인이 [line directives](/cmd/compile/#hdr-Compiler_Directives)에서 열(column) 정보를 지원합니다.

<!-- CL 106797 -->
새로운 패키지 export 데이터 형식이 도입되었습니다.
이는 대규모 Go 프로젝트의 빌드 시간을 단축시키는 것 외에는 최종 사용자에게 영향을 주지 않아야 합니다.
만약 문제가 발생할 경우, 바이너리를 빌드할 때 `go` 툴에 `-gcflags=all=-iexport=false`를 전달하여 다시 끌 수 있습니다.

<!-- CL 100459 -->
이제 컴파일러는 다음과 같은 예제의 `x`와 같이 타입 스위치 가드(type switch guard)에서 선언되었지만 사용되지 않은 변수를 거부합니다.

```go
func f(v interface{}) {
		switch x := v.(type) {
		}
	}
```

이 내용은 이미 `gccgo`와 [go/types](/pkg/go/types/) 모두에서 거절되었습니다.

### Assembler {#assembler}

<!-- CL 113315 -->
`amd64`용 어셈블러가 이제 AVX512 명령어를 지원합니다.

### 디버깅 {#debugging}

<!-- CL 100738, CL 93664 -->
이제 컴파일러는 변수 위치 정보, 라인 번호 및 중단점(breakpoint) 위치를 포함하여 최적화된 바이너리에 대해 훨씬 더 정확한 디버그 정보를 생성합니다.
이를 통해 `-N` `-l` 없이 컴파일된 바이너리도 디버깅할 수 있게 되었습니다.
디버그 정보의 품질에는 여전히 제한 사항이 있으며, 그 중 일부는 근본적인 문제이고 일부는 향후 릴리스를 통해 계속 개선될 예정입니다.

<!-- CL 118276 -->
컴파일러가 생성하는 디버그 정보가 더 확장되고 정확해짐에 따라, 이제 DWARF 섹션이 기본적으로 압축됩니다.
이는 대부분의 ELF 도구(Linux 및 \*BSD의 디버거 등)에서 투명하게 처리되며 모든 플랫폼의 Delve 디버거에서 지원되지만, macOS 및 Windows의 네이티브 도구에서는 지원이 제한적입니다.
DWARF 압축을 비활성화하려면, 바이너리를 빌드할 때 `go` 도구에 `-ldflags=-compressdwarf=false`를 전달하십시오.

<!-- CL 109699 -->
Go 1.11에서는 디버거 내에서 Go 함수를 호출할 수 있는 실험적 지원이 추가되었습니다.
이는 예를 들어, 중단점(breakpoint)에서 일시 중지되었을 때 `String` 메서드를 호출하는 등의 작업에 유용합니다.
현재 이 기능은 Delve(버전 1.1.0 이상)에서만 지원됩니다.

### 테스트 {#test}

Go 1.10부터 `go` `test` 명령은 테스트를 실행하기 전 문제를 식별하기 위해 테스트 대상 패키지에 대해 `go` `vet`을 실행합니다. `vet`은 실행 전 [go/types](/pkg/go/types/)를 통해 코드의 타입 체크를 수행하므로, 타입 체크를 통과하지 못하는 테스트는 이제 실패하게 됩니다. 특히, 클로저 내부에 사용되지 않는 변수가 포함된 테스트의 경우, Go 컴파일러가 이를 잘못 수용했기 때문에 Go 1.10에서는 컴파일되었으나([Issue #3059](/issues/3059)), 이제는 `go/types`가 이 경우를 "unused variable" 오류로 올바르게 보고하므로 실패하게 됩니다.

<!-- CL 102696 -->
`go`&nbsp;`test`의 `-memprofile` 플래그는 이제 기본적으로 "allocs" 프로파일을 사용하며, 이는 테스트가 시작된 이후 할당된 총 바이트 수(가비지 컬렉션된 바이트 포함)를 기록합니다.

### Vet {#vet}

<!-- CL 108555 -->
이제 [`go`&nbsp;`vet`](/cmd/vet/)
명령어는 분석 중인 패키지의 타입 체크(typecheck)에 실패할 경우 치명적 오류(fatal error)를 보고합니다. 이전에는 타입 체크 오류가 발생하면 단순히 경고가 출력되고 `vet`이 상태 코드 1로 종료되었습니다.

<!-- CL 108559 -->
또한, [`go`&nbsp;`vet`](/cmd/vet)이 `printf` 래퍼(wrapper)의 형식을 검사할 때 더욱 견고해졌습니다.
이제 Vet은 다음 예제와 같은 실수를 감지합니다:

```go
func wrapper(s string, args ...interface{}) {
		fmt.Printf(s, args...)
	}
```

```go
func main() {
		wrapper("%s", 42)
	}
```

### Trace {#trace}

<!-- CL 63274 -->
새로운 `runtime/trace` 패키지의 [사용자 주석 API](/pkg/runtime/trace/#hdr-User_annotation)를 통해 사용자는 실행 트레이스에 애플리케이션 수준의 정보를 기록하고 관련 goroutine 그룹을 생성할 수 있습니다.
`go`&nbsp;`tool`&nbsp;`trace` 명령은 이러한 정보를 트레이스 뷰와 새로운 사용자 태스크/리전 분석 페이지에서 시각화하여 보여줍니다.

### Cgo {#cgo}

Go 1.10부터 cgo는 일부 C 포인터 타입을 Go 타입인 `uintptr`로 변환해 왔습니다. 이러한 타입에는 Darwin의 CoreFoundation 프레임워크에 있는 `CFTypeRef` 계층과 Java JNI 인터페이스의 `jobject` 계층이 포함됩니다. Go 1.11에서는 이러한 타입을 감지하는 코드에 여러 개선 사항이 적용되었습니다. 해당 타입을 사용하는 코드는 일부 업데이트가 필요할 수 있습니다. 자세한 내용은 [Go 1.10 릴리스 노트](go1.10.html#cgo)를 참조하십시오. <!-- CL 126275, CL 127156, CL 122217, CL 122575, CL 123177 -->

### Go 커맨드 {#go_command}

<!-- CL 126656 -->
이제 `GOFLAGS` 환경 변수를 사용하여 `go` 명령의 기본 플래그를 설정할 수 있습니다.
이는 특정 상황에서 유용합니다.
사양이 낮은 시스템에서는 DWARF로 인해 링킹 속도가 현저히 느려질 수 있으며, 사용자는 기본값으로 `-ldflags=-w`를 설정하고 싶을 수 있습니다.
모듈의 경우, 일부 사용자나 CI 시스템은 항상 벤더링(vendoring)을 원하므로 기본값으로 `-mod=vendor`를 설정해야 합니다.
자세한 내용은 [`go` 명령 문서](/cmd/go/#hdr-Environment_variables)를 참조하십시오.

### Godoc {#godoc}

Go 1.11은 `godoc`의 커맨드라인 인터페이스를 지원하는 마지막 릴리스가 됩니다.
향후 릴리스에서 `godoc`은 웹 서버로만 제공됩니다. 커맨드라인 도움말 출력이 필요한 사용자는 대신 `go` `doc`을 사용해야 합니다.

<!-- CL 85396, CL 124495 -->
이제 `godoc` 웹 서버에서 새로운 API 기능이 어떤 Go 버전에서 도입되었는지 표시합니다. 타입, 함수 및 메서드의 최초 도입 Go 버전이 우측 정렬되어 표시됩니다. 예를 들어, 우측에 "1.11"이 표시된 [`UserCacheDir`](/pkg/os/#UserCacheDir)를 확인하십시오. 구조체 필드의 경우, 해당 필드가 구조체 자체가 도입된 버전과 다른 Go 버전에서 추가되었다면 인라인 주석이 추가됩니다.
구조체 필드 예시는 [`ClientTrace.Got1xxResponse`](/pkg/net/http/httptrace/#ClientTrace.Got1xxResponse)를 확인하십시오.

### Gofmt {#gofmt}

Go 소스 코드의 기본 포맷팅과 관련된 사소한 세부 사항 하나가 변경되었습니다.
인라인 주석이 포함된 표현식 목록을 포맷팅할 때, 주석들은 휴리스틱에 따라 정렬되었습니다.
하지만 일부 경우에 정렬이 너무 쉽게 나뉘거나, 너무 많은 공백이 도입되는 문제가 있었습니다.
사람이 작성한 코드에 대해 더 잘 작동하도록 휴리스틱이 변경되었습니다.

`gofmt`에 대한 이러한 종류의 사소한 업데이트는 때때로 발생할 수 있음을 유의하십시오.
일반적으로 Go 소스 코드의 일관된 포맷팅이 필요한 시스템은 특정 버전의 `gofmt` 바이너리를 사용해야 합니다.
자세한 내용은 [go/format](/pkg/go/format/) 패키지 문서를 참조하십시오.

### 실행 {#run}

<!-- CL 109341 -->
이제 [`go`&nbsp;`run`](/cmd/go/)
명령어에서 단일 임포트 경로(import path), 디렉토리 이름 또는 단일 패키지와 일치하는 패턴을 사용할 수 있습니다.
이를 통해 `go`&nbsp;`run`&nbsp;`pkg` 또는 `go`&nbsp;`run`&nbsp;`dir`, 그리고 가장 중요하게는 `go`&nbsp;`run`&nbsp;`.`와 같은 사용이 가능합니다.

## 런타임 {#runtime}

<!-- CL 85887 -->
이제 런타임에서 희소 힙 레이아웃(sparse heap layout)을 사용하므로 Go 힙 크기에 더 이상 제한이 없습니다 (이전 제한은 512GiB였습니다). 이는 또한 Go/C 혼합 바이너리 또는 `-race` 옵션으로 컴파일된 바이너리에서 드물게 발생하던 "주소 공간 충돌(address space conflict)" 오류를 해결합니다.

<!-- CL 108679, CL 106156 -->
macOS 및 iOS에서 런타임이 커널을 직접 호출하는 대신 `libSystem.dylib`를 사용합니다. 이를 통해 Go 바이너리가 향후 버전의 macOS 및 iOS와 더 높은 호환성을 갖게 될 것입니다.
`syscall`([/pkg/syscall]) 패키지는 여전히 직접 시스템 호출을 수행하며, 이에 대한 수정은 향후 릴리스에서 계획되어 있습니다.

## 성능 {#performance}

언제나 그렇듯, 변경 사항이 매우 일반적이고 다양하여 성능에 대해 정확한 진술을 하기는 어렵습니다. 하지만 더 개선된 코드 생성과 핵심 라이브러리의 최적화 덕분에 대부분의 프로그램이 조금 더 빠르게 실행될 것입니다.

<!-- CL 74851 -->
`math/big` 패키지에 여러 성능 변경 사항이 있었으며, `GOARCH=arm64`와 관련된 트리 전반의 많은 변경 사항이 있었습니다.

### 컴파일러 툴체인 {#performance-compiler}

<!-- CL 110055 -->
이제 컴파일러는 다음과 같은 형태의 맵 초기화(map clearing) 작업을 최적화합니다:

```go
for k := range m {
		delete(m, k)
	}
```

<!-- CL 109517 -->
이제 컴파일러가 `append(s,`&nbsp;`make([]T,`&nbsp;`n)...)` 형태의 슬라이스 확장을 최적화합니다.

<!-- CL 100277, CL 105635, CL 109776 -->
이제 컴파일러가 훨씬 더 공격적으로 경계 검사(bounds-check) 및 분기 제거(branch elimination)를 수행합니다. 특히, 이제는 이행적 관계(transitive relations)를 인식하므로, `i<j`이고 `j<len(s)`라면 이러한 사실을 이용하여 `s[i]`에 대한 경계 검사를 제거할 수 있습니다. 또한 `s[i-10]`과 같은 간단한 산술 연산을 이해하며, 루프 내에서 더 많은 귀납적 사례를 인식할 수 있습니다. 더불어, 컴파일러는 이제 경계 정보를 사용하여 시프트 연산을 더욱 공격적으로 최적화합니다.

## 표준 라이브러리 {#library}

표준 라이브러리의 모든 변경 사항은 사소합니다.

### 라이브러리의 소규모 변경 사항 {#minor_library_changes}

언제나 그렇듯이, Go 1의 [호환성 약속](/doc/go1compat)을 염두에 둔 라이브러리의 다양한 소규모 변경 및 업데이트가 있었습니다.

<!-- CL 115095: https://golang.org/cl/115095: yes (`go test pkg` now always builds pkg even if there are no test files): cmd/go: output coverage report even if there are no test files -->
<!-- CL 110395: https://golang.org/cl/110395: cmd/go, cmd/compile: use Windows response files to avoid arg length limits -->
<!-- CL 112436: https://golang.org/cl/112436: cmd/pprof: add readline support similar to upstream -->

#### [crypto](/pkg/crypto/)

<!-- CL 64451 -->
[`ecdsa.Sign`](/pkg/crypto/ecdsa/#Sign),
[`rsa.EncryptPKCS1v15`](/pkg/crypto/rsa/#EncryptPKCS1v15) 및
[`rsa.GenerateKey`](/pkg/crypto/rsa/#GenerateKey)를 포함한 일부 암호화 작업에서, 이제 테스트가 내부 동작에 의존하지 않도록 무작위로 추가 바이트의 랜덤 값을 읽습니다.

<!-- crypto -->

#### [crypto/cipher](/pkg/crypto/cipher/)

<!-- CL 48510, CL 116435 -->
새로운 함수 [`NewGCMWithTagSize`](/pkg/crypto/cipher/#NewGCMWithTagSize)는 기존 암호 시스템과의 호환성을 위해 표준이 아닌 태그 길이를 사용하는 Galois Counter Mode를 구현합니다.

<!-- crypto/cipher -->

#### [crypto/rsa](/pkg/crypto/rsa/)

<!-- CL 103876 -->
[`PublicKey`](/pkg/crypto/rsa/#PublicKey)에 이제 모듈러스 크기를 바이트 단위로 반환하는 [`Size`](/pkg/crypto/rsa/#PublicKey.Size) 메서드가 구현되었습니다.

<!-- crypto/rsa -->

#### [crypto/tls](/pkg/crypto/tls/)

<!-- CL 85115 -->
[`ConnectionState`](/pkg/crypto/tls/#ConnectionState)의 새로운 [`ExportKeyingMaterial`](/pkg/crypto/tls/#ConnectionState.ExportKeyingMaterial) 메서드는 RFC 5705에 따라 연결에 바인딩된 키 생성 재료(keying material)를 내보낼 수 있게 합니다.

<!-- crypto/tls -->

#### [crypto/x509](/pkg/crypto/x509/)

<!-- CL 123355, CL 123695 -->
Subject Alternative Names(SAN)가 없을 때 `CommonName` 필드를 호스트 이름으로 처리하던 더 이상 사용되지 않는 레거시 동작은, 이제 CN이 유효한 호스트 이름이 아닐 경우 비활성화됩니다.
`GODEBUG` 환경 변수에 실험적 값인 `x509ignoreCN=1`을 추가하면 `CommonName`을 완전히 무시할 수 있습니다.
CN이 무시되면, SAN이 없는 인증서는 `NameConstraintsWithoutSANs`를 반환하는 대신 이름 제약(name constraints)이 있는 체인 하에서 검증됩니다.

<!-- CL 113475 -->
확장 키 용도(Extended key usage) 제한은 이제 항상 확인되는 대신, [`VerifyOptions`](/pkg/crypto/x509/#VerifyOptions)의 `KeyUsages` 필드에 명시된 경우에만 다시 확인됩니다. 이는 Go 1.9 및 이전 버전의 동작과 일치합니다.

<!-- CL 102699 -->
[`SystemCertPool`](/pkg/crypto/x509/#SystemCertPool)에서 반환하는 값은 이제 캐시되며, 호출 사이에 발생한 시스템 변경 사항이 반영되지 않을 수 있습니다.

<!-- crypto/x509 -->

#### [debug/elf](/pkg/debug/elf/)

<!-- CL 112115 -->
더 많은 [`ELFOSABI`](/pkg/debug/elf/#ELFOSABI_NONE)
및 [`EM`](/pkg/debug/elf/#EM_NONE)
상수가 추가되었습니다.

<!-- debug/elf -->

#### [encoding/asn1](/pkg/encoding/asn1/)

<!-- CL 110561 -->
`Marshal` 및 [`Unmarshal`](/pkg/encoding/asn1/#Unmarshal)에서 이제 필드에 대한 "private" 클래스 어노테이션을 지원합니다.

<!-- encoding/asn1 -->

#### [encoding/base32](/pkg/encoding/base32/)

<!-- CL 112516 -->
이제 디코더가 불완전한 청크(chunk)에 대해 일관되게 `io.ErrUnexpectedEOF`를 반환합니다. 이전에는 일부 경우에 `io.EOF`를 반환했습니다.

<!-- encoding/base32 -->

#### [encoding/csv](/pkg/encoding/csv/)

<!-- CL 99696 -->
이제 `Reader`는 [`Comma`](/pkg/encoding/csv/#Reader.Comma) 필드를 큰따옴표(double-quote) 문자로 설정하려는 시도를 거부합니다. 큰따옴표 문자는 CSV에서 이미 특별한 의미를 갖기 때문입니다.

<!-- encoding/csv -->

<!-- CL 100235이 되돌려졌습니다 -->

#### [html/template](/pkg/html/template/)

<!-- CL 121815 -->
타입이 지정된 인터페이스(typed interface) 값이 암시적 이스케이퍼(implicit escaper) 함수로 전달될 때의 동작이 변경되었습니다. 이전에는 이러한 값이 `<nil>`의 (이스케이프된 형태)로 기록되었습니다. 이제 이러한 값들은 타입이 지정되지 않은 `nil` 값이 (과거부터 지금까지) 무시되었던 것과 마찬가지로 무시됩니다.

<!-- html/template -->

#### [image/gif](/pkg/image/gif/)

<!-- CL 93076 -->
이제 반복되지 않는 애니메이션 GIF가 지원됩니다. 이는 [`LoopCount`](/pkg/image/gif/#GIF.LoopCount) 값이 -1인 것으로 표시됩니다.

<!-- image/gif -->

#### [io/ioutil](/pkg/io/ioutil/)

<!-- CL 105675 -->
[`TempFile`](/pkg/io/ioutil/#TempFile)
함수는 이제 파일 이름에서 무작위 문자가 배치될 위치를 지정하는 기능을 지원합니다. `prefix` 인자에 "`*`"가 포함되어 있으면, 무작위 문자열이 "`*`"를 대체합니다. 예를 들어, `prefix` 인자가 "`myname.*.bat`"인 경우 "`myname.123456.bat`"와 같은 무작위 파일 이름이 생성됩니다. "`*`"가 포함되지 않은 경우에는 기존 동작이 유지되어 무작위 숫자가 끝에 추가됩니다.

<!-- io/ioutil -->

#### [math/big](/pkg/math/big/)

<!-- CL 108996 -->
[`ModInverse`](/pkg/math/big/#Int.ModInverse)는 이제 g와 n이 서로소(relatively prime)가 아닐 때 nil을 반환합니다. 이전에는 결과가 정의되지 않았습니다.

<!-- math/big -->

#### [mime/multipart](/pkg/mime/multipart/)

<!-- CL 121055 -->
파일 이름이 누락되었거나 비어 있는 form-data의 처리 방식이 Go 1.9의 동작으로 복구되었습니다. form-data 파트의 [`Form`](/pkg/mime/multipart/#Form)에서 해당 값은 `File` 필드가 아닌 `Value` 필드에서 사용할 수 있습니다. Go 1.10부터 1.10.3 릴리스까지는 파일 이름이 누락되었거나 비어 있고 "Content-Type" 필드가 비어 있지 않은 form-data 파트가 `File` 필드에 저장되었습니다. 이 변경 사항은 1.10 버전의 실수였으며, 다시 1.9 버전의 동작으로 되돌려졌습니다.

제공해주신 내용이 없거나 빈 파일(`<!-- mime/multipart -->`)인 것으로 보입니다. 번역할 영어 텍스트를 제공해 주시면, 요청하신 기술 번역 지침에 따라 정성껏 번역해 드리겠습니다.

#### [mime/quotedprintable](/pkg/mime/quotedprintable/)

<!-- CL 121095 -->
실제 환경에서 발견되는 잘못된 입력값을 지원하기 위해, 이제 이 패키지는 non-ASCII 바이트를 허용하지만 해당 인코딩을 검증하지는 않습니다.

제공해주신 입력 내용에 번역할 텍스트가 포함되어 있지 않습니다. 번역이 필요한 Markdown 콘텐츠를 제공해 주시면, 요청하신 지침에 따라 정교하게 한국어로 번역해 드리겠습니다.

#### [net](/pkg/net/)

<!-- CL 72810 -->
새로운 [`ListenConfig`](/pkg/net/#ListenConfig) 타입과 새로운
[`Dialer.Control`](/pkg/net/#Dialer.Control) 필드를 통해 각각 연결을 수락(accept)하거나 생성(create)하기 전에 소켓 옵션을 설정할 수 있습니다.

<!-- CL 76391 -->
[`syscall.RawConn`](/pkg/syscall/#RawConn)의 `Read` 및 `Write` 메서드가 이제 Windows에서 올바르게 작동합니다.

<!-- CL 107715 -->
이제 `net` 패키지는 [`io.Copy`](/pkg/io/#Copy)에 의해 호출되는 [`TCPConn.ReadFrom`](/pkg/net/#TCPConn.ReadFrom)에서 TCP 연결 간에 데이터를 복사할 때, Linux의 경우 [`splice` 시스템 콜](https://man7.org/linux/man-pages/man2/splice.2.html)을 자동으로 사용합니다. 그 결과, TCP 프록싱이 더 빠르고 효율적으로 이루어집니다.

<!-- CL 108297 -->
[`TCPConn.File`](/pkg/net/#TCPConn.File),
[`UDPConn.File`](/pkg/net/#UDPConn.File),
[`UnixConn.File`](/pkg/net/#UnixCOnn.File),
및 [`IPConn.File`](/pkg/net/#IPConn.File)
메서드가 더 이상 반환된 `*os.File`을
블로킹(blocking) 모드로 설정하지 않습니다.

<!-- net -->

#### [net/http](/pkg/net/http/)

<!-- CL 71272 -->
[`Transport`](/pkg/net/http/#Transport) 타입에 호스트당 최대 연결 수를 제한할 수 있는 새로운 [`MaxConnsPerHost`](/pkg/net/http/#Transport.MaxConnsPerHost) 옵션이 추가되었습니다.

<!-- CL 79919 -->
[`Cookie`](/pkg/net/http/#Cookie) 타입에 최근 대부분의 브라우저에서 지원하는 새로운 쿠키 속성을 나타내기 위한 [`SameSite`](/pkg/net/http/#Cookie.SameSite) 필드(마찬가지로 [`SameSite`](/pkg/net/http/#SameSite)라는 이름의 새로운 타입)가 추가되었습니다.
`net/http`의 `Transport`는 `SameSite` 속성을 직접 사용하지 않지만, 패키지 차원에서 브라우저가 사용할 수 있도록 해당 속성의 파싱 및 직렬화를 지원합니다.

<!-- CL 81778 -->
[`Shutdown`](/pkg/net/http/#Server.Shutdown) 또는 [`Close`](/pkg/net/http/#Server.Close)를 호출한 후에는 [`Server`](/pkg/net/http/#Server)를 재사용할 수 없습니다. 이는 과거에도 공식적으로 지원된 적이 없었으며, 종종 예상치 못한 동작을 보였습니다. 이제 셧다운 또는 종료 후 서버의 `Serve` 메서드에 대한 모든 향후 호출은 에러를 반환합니다.

<!-- CL 89275는 Go 1.11 이전에 되돌려졌습니다(reverted) -->

<!-- CL 93296 -->
이제 HTTP 상태 코드 421에 대해 `StatusMisdirectedRequest` 상수가 정의되었습니다.

<!-- CL 123875 -->
HTTP 서버는 이제 파이프라인된 HTTP/1.1 요청을 수신할 때 컨텍스트를 취소하거나 [`CloseNotifier`](/pkg/net/http/#CloseNotifier) 채널로 전송하지 않습니다. 브라우저는 HTTP 파이프라이닝을 사용하지 않지만, 일부 클라이언트(예: Debian의 `apt`)는 그렇게 설정되어 있을 수 있습니다.

<!-- CL 115255 -->
[`DefaultTransport`](/pkg/net/http/#DefaultTransport)에서 사용하는 [`ProxyFromEnvironment`](/pkg/net/http/#ProxyFromEnvironment)가 이제 `NO_PROXY` 환경 변수에서 CIDR 표기법과 포트 지정을 지원합니다.

<!-- net/http -->

#### [net/http/httputil](/pkg/net/http/httputil/)

<!-- CL 77410 -->
[`ReverseProxy`](/pkg/net/http/httputil/#ReverseProxy)에 오류 처리 방식을 변경할 수 있도록 하는 새로운 [`ErrorHandler`](/pkg/net/http/httputil/#ReverseProxy.ErrorHandler) 옵션이 추가되었습니다.

<!-- CL 115135 -->
이제 `ReverseProxy`는 gRPC 프로토콜의 요구 사항에 따라 "`TE:`&nbsp;`trailers`" 요청 헤더를 백엔드로 전달합니다.

<!-- net/http/httputil -->

#### [os](/pkg/os/)

<!-- CL 78835 -->
새로운 [`UserCacheDir`](/pkg/os/#UserCacheDir) 함수는
사용자별 캐시 데이터에 사용할 기본 루트 디렉토리를 반환합니다.

<!-- CL 94856 -->
새로운 [`ModeIrregular`](/pkg/os/#ModeIrregular)은
파일이 일반 파일이 아니지만 그 외에 알려진 정보가 없거나,
Go에 정의된 모드 비트가 있는 소켓, 디바이스, 이름 있는 파이프(named pipe), 심볼릭 링크 또는 기타 파일 유형이 아님을 나타내는 [`FileMode`](/pkg/os/#FileMode) 비트입니다.

<!-- CL 99337 -->
이제 개발자 모드가 활성화된 Windows 10 머신에서 비특권 사용자에 대해서도 [`Symlink`](/pkg/os/#Symlink)가 작동합니다.

<!-- CL 100077 -->
비차단(non-blocking) 디스크립터가 [`NewFile`](/pkg/os#NewFile)에 전달되면, 결과로 생성되는 `*File`은 비차단 모드로 유지됩니다. 이는 해당 `*File`에 대한 I/O가 별도의 스레드가 아닌 런타임 폴러(runtime poller)를 사용하며, [`SetDeadline`](/pkg/os/#File.SetDeadline) 메서드들이 정상적으로 작동함을 의미합니다.

<!-- os -->

#### [os/signal](/pkg/os/signal/)

<!-- CL 108376 -->
새로운 [`Ignored`](/pkg/os/signal/#Ignored) 함수는 시그널이 현재 무시되고 있는지 여부를 보고합니다.

<!-- os/signal -->

#### [os/user](/pkg/os/user/)

<!-- CL 92456 -->
이제 `os/user` 패키지를 환경 변수 `CGO_ENABLED=0` 사용 여부와 관계없이, 빌드 태그 "`osusergo`"를 사용하여 순수 Go(pure Go) 모드로 빌드할 수 있습니다. 이전에는 프로그램 전체에서 `cgo` 지원을 비활성화해야만 해당 패키지의 순수 Go 구현체를 사용할 수 있었습니다.

<!-- os/user -->

<!-- CL 101715이 되돌려졌습니다 -->

#### [runtime](/pkg/runtime/)

<!-- CL 70993 -->
`<code>GODEBUG=tracebackancestors=_N_</code>` 환경 변수를 설정하면 이제 traceback에 goroutine이 생성된 시점의 스택이 추가로 포함됩니다. 여기서 `_N_`은 보고할 조상 goroutine의 수를 제한합니다.

<!-- runtime -->

#### [runtime/pprof](/pkg/runtime/pprof/)

<!-- CL 102696 -->
이번 릴리스에서는 프로그램 시작 이후 할당된 총 바이트 수(가비지 컬렉션된 바이트 포함)를 프로파일링하는 새로운 "allocs" 프로파일 유형이 추가되었습니다. 이는 `-alloc_space` 모드로 확인하는 기존 "heap" 프로파일과 동일합니다.
이제 `go test -memprofile=...`는 "heap" 프로파일 대신 "allocs" 프로파일을 보고합니다.

<!-- runtime/pprof -->

#### [sync](/pkg/sync/)

<!-- CL 87095 -->
이제 mutex 프로파일에 [`RWMutex`](/pkg/sync/#RWMutex)의 reader/writer 경합(contention) 정보가 포함됩니다.
Writer/writer 경합은 이미 mutex 프로파일에 포함되어 있었습니다.

<!-- sync -->

#### [syscall](/pkg/syscall/)

<!-- CL 106275 -->
Windows에서 Go의 가비지 컬렉터와 관련된 문제를 방지하기 위해 여러 필드가 `uintptr`에서 새로운 [`Pointer`](/pkg/syscall/?GOOS=windows&GOARCH=amd64#Pointer) 타입으로 변경되었습니다. 동일한 변경 사항이 [`golang.org/x/sys/windows`](https://godoc.org/golang.org/x/sys/windows) 패키지에도 적용되었습니다. 영향을 받는 코드가 있는 경우, 사용자는 먼저 `syscall` 패키지에서 `golang.org/x/sys/windows` 패키지로 마이그레이션한 다음, [`unsafe.Pointer` 변환 규칙](/pkg/unsafe/#Pointer)을 준수하며 `Pointer`를 사용하도록 변경해야 합니다.

<!-- CL 118658 -->
Linux에서 [`Faccessat`](/pkg/syscall/?GOOS=linux&GOARCH=amd64#Faccessat)의 `flags` 매개변수가 이제 glibc와 동일하게 구현되었습니다. 이전 Go 릴리스에서는 flags 매개변수가 무시되었습니다.

<!-- CL 118658 -->
Linux에서 [`Fchmodat`](/pkg/syscall/?GOOS=linux&GOARCH=amd64#Fchmodat)의 `flags` 파라미터에 대한 검증이 추가되었습니다. Linux의 `fchmodat`은 `flags` 파라미터를 지원하지 않으므로, 이제 glibc의 동작을 모방하여 해당 값이 0이 아니면 에러를 반환합니다.

<!-- syscall -->

#### [text/scanner](/pkg/text/scanner/)

<!-- CL 112037 -->
[`Scanner.Scan`](/pkg/text/scanner/#Scanner.Scan) 메서드는 이제 raw string 리터럴에 대해 [`String`](/pkg/text/scanner/#String) 대신 [`RawString`](/pkg/text/scanner/#RawString) 토큰을 반환합니다.

<!-- text/scanner -->

#### [text/template](/pkg/text/template/)

<!-- CL 84480 -->
이제 `=` 토큰을 통해 할당 방식으로 템플릿 변수를 수정하는 것이 허용됩니다:

{{ $v := "init" }}
	  {{ if true }}
	    {{ $v = "changed" }}
	  {{ end }}
	  v: {{ $v }} {{/* "changed" */}}

<!-- CL 95215 -->
이전 버전에서는 템플릿 함수로 전달된 타입이 지정되지 않은 `nil` 값은 무시되었습니다. 이제는 일반 인자로 전달됩니다.

<!-- text/template -->

#### [time](/pkg/time/)

<!-- CL 98157 -->
이제 부호와 오프셋으로 표시된 시간대(timezone)의 파싱이 지원됩니다. 이전 버전에서는 숫자 형태의 시간대 이름(예: `+03`)은 유효하지 않은 것으로 간주되었으며, 시간대 이름을 기대하는 상황에서 세 글자로 된 약어(예: `MST`)만 허용되었습니다.

<!-- time -->
