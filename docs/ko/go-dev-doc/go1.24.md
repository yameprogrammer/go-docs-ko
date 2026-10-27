```markdown
<style>
  main ul li { margin: 0.5em 0; }
</style>
```

## Go 1.24 소개 {#introduction}

가장 최신 Go 릴리스, 버전 1.24는 [2025년 2월](/doc/devel/release#go1.24.0)에 출시되며, [Go 1.23](/doc/go1.23) 이후 6개월 후입니다.
대부분의 변경 사항은 도구 체인, 런타임 및 라이브러리의 구현에 있습니다.
물론, 이번 릴리스도 Go 1의 [호환성 약속](/doc/go1compat)을 유지합니다.
대부분의 Go 프로그램이 기존과 동일하게 컴파일 및 실행될 것으로 예상합니다.

## 언어 변경 사항 {#language}

```
// Example Go code
package main

import "fmt"

func main() {
  fmt.Println("Hello, world!")
}
```

| Feature | Description |
|---|---|
| Language | English |
| Locale | en_US |
| Date Format | YYYY-MM-DD |

*   List item 1
*   List item 2
*   List item 3

<!-- go.dev/issue/46477 -->
Go 1.24에서 이제 완전히 [일반 타입 별칭](/issue/46477)을 지원합니다:
타입 별칭은 정의된 타입과 마찬가지로 매개변수화될 수 있습니다.
자세한 내용은 [언어 사양](/ref/spec#Alias_declarations)을 참조하십시오.
현재 이 기능을 비활성화하려면 `GOEXPERIMENT=noaliastypeparams`를 설정할 수 있습니다.
하지만 `aliastypeparams` 설정은 Go 1.25에서 제거됩니다.

## 도구 {#tools}

### Go 명령어 {#go-command}

<!-- go.dev/issue/48429 -->

Go 모듈은 이제 `tool` 지시어를 사용하여 실행 파일 종속성을 추적할 수 있습니다. 이는 이전 방식인 "tools.go"라는 이름으로 파일을 만들고 도구를 템플릿으로 추가하는 것을 제거합니다. `go tool` 명령은 이제 Go 배포판에 포함된 도구 외에도 이러한 도구를 실행할 수 있습니다. 자세한 내용은 [문서](/doc/modules/managing-dependencies#tools)를 참조하십시오.

새로운 `-tool` 플래그는 `go get` 명령에 도구 지침을 현재 모듈에 추가하고, 이름이 지정된 패키지에 대한 요구 지침을 추가합니다.

새로운 [`tool` 메타 패턴](/cmd/go#hdr-Package_lists_and_patterns)은 현재 모듈 내의 모든 도구를 참조합니다. 이를 사용하여 `go get tool` 명령으로 모두 업그레이드하거나, `go install tool` 명령으로 GOBIN 디렉터리에 설치할 수 있습니다.

<!-- go.dev/issue/69290 -->

`go run`로 생성된 실행 파일과 `go tool`의 새로운 동작이 이제 Go 빌드 캐시에 저장됩니다. 이를 통해 반복 실행이 빨라지지만, 캐시 크기가 커집니다. 자세한 내용은 [#69290](/issue/69290)를 참조하십시오.

<!-- go.dev/issue/62067 -->

`go build` 및 `go install` 명령은 이제 표준 출력으로 빌드 출력 및 실패를 구조화된 JSON 형식으로 보고하는 `-json` 플래그를 지원합니다.
보고 형식에 대한 자세한 내용은 `go help buildjson`을 참조하십시오.

또한, `go test -json`은 이제 빌드 출력 및 실패를 JSON 형식으로 보고하며, 테스트 결과 JSON과 함께 제공됩니다.
새로운 `Action` 유형으로 구분되지만, 테스트 통합 시스템에서 문제가 발생하면 `GODEBUG` 설정을 사용하여 텍스트 기반 빌드 출력을 다시 사용할 수 있습니다: `gotestjsonbuildtext=1`.

<!-- go.dev/issue/26232 -->

새로운 `GOAUTH` 환경 변수는 개인 모듈 가져오기의 인증을 위한 유연한 방법을 제공합니다. 자세한 내용은 `go help goauth`를 참조하십시오.

<!-- go.dev/issue/50603 -->

`go build` 명령은 컴파일된 바이너리에 [메인 모듈의 버전](/pkg/runtime/debug#BuildInfo.Main)을 버전 관리 시스템 태그 및/또는 커밋에 따라 설정합니다.
커밋되지 않은 변경 사항이 있는 경우 `+dirty` 접미사가 추가됩니다.
버전 관리 시스템 정보를 바이너리에서 제외하려면 `-buildvcs=false` 플래그를 사용하십시오.

<!-- go.dev/issue/63939 -->

새로운 [GODEBUG 설정](/doc/godebug)인 `toolchaintrace=1` ([/doc/toolchain#select](https://example.com/toolchain#select))을 사용하여 `go` 명령어의 툴체인 선택 프로세스를 추적할 수 있습니다.

### Cgo {#cgo}

<!-- go.dev/issue/56378, CL 579955 -->
Cgo는 C 함수에 대한 새로운 주석을 지원하여 런타임 성능을 향상합니다.
`#cgo noescape cFunctionName`는 컴파일러에게 C 함수 `cFunctionname`으로 전달되는 메모리가 더 이상 범위를 벗어나지 않는다는 것을 알려줍니다.
`#cgo nocallback cFunctionName`는 컴파일러에게 C 함수 `cFunctionName`이 Go 함수에 대한 콜백을 호출하지 않는다는 것을 알려줍니다.
자세한 내용은 [cgo 문서를 참조하십시오](/pkg/cmd/cgo#hdr-Optimizing_calls_of_C_code).

<!-- go.dev/issue/67699 -->
Cgo는 현재 여러 개의 호환되지 않는 선언이 있는 C 함수에 대한 호출을 컴파일하는 것을 거부합니다. 예를 들어, `f`가 `void f(int)` 및 `void f(double)`로 선언된 경우, cgo는 `f(0)`에 대한 잘못된 호출 시퀀스를 생성하는 대신 오류를 보고합니다. 이번 릴리스의 새로운 기능은 호환되지 않는 선언이 서로 다른 파일에 나타날 때 이 오류 조건을 더 잘 감지합니다. 자세한 내용은 [#67699](/issue/67699)를 참조하십시오.

### Objdump

```bash
objdump -d <executable_file>
```

<!-- go.dev/issue/15255, go.dev/issue/36738 -->
`objdump` 도구가 이제 64비트
LoongArch (`GOARCH=loong64`), RISC-V (`GOARCH=riscv64`), 및 S390X (`GOARCH=s390x`) 아키텍처에 대한 디스어셈블을 지원합니다.

### 수의사

<!-- go.dev/issue/44251 -->
새로운 `tests` 분석기는 테스트, 퍼저, 벤치마크 및 테스트 패키지에 있는 예제에 대한 일반적인 오류를 보고합니다. 여기에는 잘못된 이름, 잘못된 서명 또는 존재하지 않는 식별자를 문서화하는 예제가 포함됩니다. 이러한 오류 중 일부는 테스트 실행을 방지할 수 있습니다.
이 분석기는 `go test`가 실행하는 분석기의 일부입니다.

<!-- go.dev/issue/60529 -->
기존의 `printf` 분석기는 `fmt.Printf(s)` 형태의 호출에 대해 진단 메시지를 보고합니다. 여기서 `s`는 상수 형식 문자열이 아니고, 다른 인수가 없는 경우입니다. 이러한 호출은 거의 항상 오류이며, `s`의 값이 `%` 문자를 포함할 수 있습니다. `fmt.Print`를 사용하는 것이 좋습니다. 자세한 내용은 [#60529](/issue/60529)를 참조하십시오. 이 검사는 기존 코드에서 결과를 생성하는 경향이 있습니다. 따라서 Go 1.24 이상 버전의 언어(go.mod 파일의 `go` 지시어나 `//go:build` 주석으로 지정된 대로)로 업데이트할 때 지속적인 통합 실패를 방지하기 위해 적용됩니다.

<!-- go.dev/issue/64127 -->
기존의 `buildtag` 분석기는 `//go:build` 지시문에 유효하지 않은 Go [메이저 버전 빌드 제약 조건](https://pkg.go.dev/cmd/go#hdr-Build_constraints)이 있는 경우 오류를 보고합니다. 예를 들어, `//go:build go1.23.1`은 특정 릴리스를 참조합니다. 대신 `//go:build go1.23`을 사용하십시오.
자세한 내용은 [#64127](https://pkg.go.dev/issue/64127)를 참조하십시오.

<!-- go.dev/issue/66387 -->
기존의 `copylock` 분석기는 3개의 절을 가진 "for" 루프 내에서 선언된 변수가 `sync.Locker`를 포함하는 경우(예: `sync.Mutex`)에 진단을 보고합니다. (예: `for i := iter(); done(i); i = next(i) { ... }`). [Go 1.22](/doc/go1.22#language)는 이러한 루프의 동작을 변경하여 각 반복마다 새 변수를 생성하고 이전 반복의 값을 복사하도록 했습니다. 이 복사 작업은 잠금에 안전하지 않습니다. 자세한 내용은 [#66387](/issue/66387)를 참조하십시오.

### GOCACHEPROG

<!-- go.dev/issue/64876 -->
`cmd/go` 내부 바이너리와 테스트 캐싱 메커니즘은 이제 자식 프로세스가 `cmd/go` 도구와 `GOCACHEPROG` 환경 변수로 지정된 자식 프로세스 간에 JSON 프로토콜을 구현하여 구현할 수 있습니다.
이 기능은 이전에 `GOEXPERIMENT` 뒤에 숨겨져 있었습니다.
프로토콜 세부 정보는 [문서](https://example.com/cmd/go/internal/cacheprog)를 참조하십시오.

## 실행 시점 {#runtime}

<!-- go.dev/issue/54766 -->
<!-- go.dev/cl/614795 -->
<!-- go.dev/issue/68578 -->

다양한 대표적인 벤치마크에서 평균적으로 런타임 성능 개선을 통해 CPU 오버헤드를 2~3% 감소시켰습니다.
결과는 애플리케이션에 따라 다를 수 있습니다.
이러한 개선 사항에는 [Swiss Tables](https://abseil.io/about/design/swisstables)를 기반으로 하는 새로운 기본 `map` 구현, 작은 객체의 더 효율적인 메모리 할당, 그리고 새로운 런타임 내부 뮤텍스 구현이 포함됩니다.

새로운 기본 `map` 구현 및 새로운 런타임 내부 뮤텍스는 각각 빌드 시간에 `GOEXPERIMENT=noswissmap` 및 `GOEXPERIMENT=nospinbitmutex`를 설정하여 비활성화할 수 있습니다.

## 컴파일러

<!-- go.dev/issue/60725, go.dev/issue/57926 -->
컴파일러는 이미 cgo로 생성된 수신자 유형으로 새 메서드를 정의하는 것을 금지했지만, 별칭 유형을 통해 이를 우회할 수 있었습니다.
Go 1.24에서는 수신자가 cgo로 생성된 유형을 직접적으로 또는 간접적으로 (별칭 유형을 통해) 나타내는 경우 항상 오류를 보고합니다.

## 링크 편집기 {#linker}

<!-- go.dev/issue/68678, go.dev/issue/68652, CL 618598, CL 618601 -->
링커는 이제 ELF 플랫폼에서는 GNU 빌드 ID (ELF `NT_GNU_BUILD_ID` 노트)와 macOS에서는 UUID (Mach-O `LC_UUID` 로드 명령)를 기본적으로 생성합니다.
빌드 ID 또는 UUID는 Go 빌드 ID에서 파생됩니다.
`-B none` 링커 플래그로 비활성화하거나, 사용자가 지정한 16진수 값으로 `-B 0xNNNN` 링커 플래그를 사용하여 덮어쓸 수 있습니다.

## 부트스트랩 {#bootstrap}

<!-- go.dev/issue/64751 -->
앞서 [Go 1.22 릴리스 노트](/doc/go1.22#bootstrap)에서 언급했듯이, Go 1.24는 이제 1.22.6 또는 그 이후 버전을 필요로 합니다.
또한, Go 1.26은 1.24의 특정 버전을 필요로 할 것으로 예상됩니다.

## 표준 라이브러리 {#library}

### 디렉토리 기반 파일 시스템 접근

<!-- go.dev/issue/67002 -->
새로운 [`os.Root`](/pkg/os#Root) 타입은 특정 디렉토리 내에서 파일 시스템 작업을 수행하는 기능을 제공합니다.

[`os.OpenRoot`](/pkg/os#OpenRoot) 함수는 디렉토리를 열고 `os.Root` 객체를 반환합니다.
`os.Root` 객체에 있는 메서드는 디렉토리 내에서 작동하며, 디렉토리 외부의 위치를 참조하는 경로, 특히 디렉토리 내의 심볼릭 링크를 따라가는 경로를 허용하지 않습니다.
`os.Root`에 있는 메서드는 `os` 패키지에 있는 대부분의 파일 시스템 작업을 반영하며, 예를 들어 [`os.Root.Open`](/pkg/os#Root.Open),
[`os.Root.Create`](/pkg/os#Root.Create),
[`os.Root.Mkdir`](/pkg/os#Root.Mkdir),
및 [`os.Root.Stat`](/pkg/os#Root.Stat) 등이 있습니다.

### 새로운 벤치마크 함수

벤치마크는 더 빠르고 오류 발생 가능성이 적은 [`testing.B.Loop`](/pkg/testing#B.Loop) 방법을 사용하여 `for b.Loop() { ... }`와 같은 반복 작업을 수행할 수 있습니다. 이는 일반적으로 `b.N`을 사용하는 반복 구조 대신에 사용됩니다. 이렇게 하면 다음과 같은 두 가지 주요 이점을 얻을 수 있습니다.
 - 벤치마크 함수는 `-count` 횟수만큼 정확히 실행되므로, 비싼 설정 및 정리 작업이 한 번만 실행됩니다.
 - 함수 호출의 매개변수와 결과가 유지되므로, 컴파일러가 루프 본문을 완전히 최적화하지 못합니다.

### 개선된 최종 정리 기능

<!-- go.dev/issue/67535 -->
새로운 `runtime.AddCleanup` 함수는 [`runtime.SetFinalizer`](/pkg/runtime#SetFinalizer)보다 더 유연하고, 효율적이며, 오류 발생 가능성이 적은 최종화 메커니즘입니다.
`AddCleanup`은 객체가 더 이상 사용되지 않을 때 실행되는 정리 함수를 객체에 연결합니다.
그러나 `SetFinalizer`와 달리,
단일 객체에 여러 개의 정리 함수가 연결될 수 있습니다.
정리 함수는 내부 포인터에 연결될 수도 있습니다.
객체가 순환 구조를 형성하는 경우, 정리 함수는 일반적으로 메모리 누수를 발생시키지 않습니다.
또한, 정리 함수는 객체 또는 객체에 가리키는 객체의 해제 지연을 발생시키지 않습니다.
새로운 코드는 `SetFinalizer` 대신 `AddCleanup`을 사용하는 것을 선호해야 합니다.

### 새로운 약한 패키지 {#weak}

새로운 [`weak`](/pkg/weak/) 패키지는 약 참조를 제공합니다.

약 참조는 메모리 효율적인 구조를 생성할 수 있도록 제공되는 기본적인 기능입니다. 예를 들어, 값과 관련된 약 맵, `unique` 패키지에 포함되지 않은 모든 항목에 대한 명명 맵, 그리고 다양한 종류의 캐시를 만들 수 있습니다.

이러한 사용 사례를 지원하기 위해, 이번 릴리스는 `runtime.AddCleanup` 및 `maphash.Comparable`을 제공합니다.

### 새로운 crypto/mlkem 패키지 {#crypto-mlkem}

<!-- go.dev/issue/70122 -->

새로운 [`crypto/mlkem`](/pkg/crypto/mlkem/) 패키지는
ML-KEM-768 및 ML-KEM-1024를 구현합니다.

ML-KEM은 이전에는 Kyber로 알려졌던 포스트 양자 키 교환 메커니즘으로, [FIPS 203](https://doi.org/10.6028/NIST.FIPS.203)에서 정의되어 있습니다.

### 새로운 crypto/hkdf, crypto/pbkdf2, crypto/sha3 패키지 {#crypto-packages}

<!-- go.dev/issue/61477, go.dev/issue/69488, go.dev/issue/69982, go.dev/issue/65269, CL 629176 -->

새로운 [`crypto/hkdf`](/pkg/crypto/hkdf/) 패키지는
[RFC 5869](https://www.rfc-editor.org/rfc/rfc5869.html)에 정의된 대로,
HMAC 기반의 Extract-and-Expand 키 파생 함수 HKDF를 구현합니다.

새로운 [`crypto/pbkdf2`](/pkg/crypto/pbkdf2/) 패키지는
[RFC 8018](https://www.rfc-editor.org/rfc/rfc8018.html)에 정의된
비밀 기반 키 파생 함수 PBKDF2를 구현합니다.

새로운 [`crypto/sha3`](/pkg/crypto/sha3/) 패키지는 SHA-3 해시 함수 및 SHAKE 및 cSHAKE 확장 출력 함수를 구현합니다.
이것들은 [FIPS 202](http://doi.org/10.6028/NIST.FIPS.202)에서 정의된 대로입니다.

이 세 가지 패키지는 기존 `golang.org/x/crypto/...` 패키지에 기반합니다.

### FIPS 140-3 준수 {#fips140}

이 릴리스에는 FIPS 140-3
규정을 준수하기 위한 [새로운 메커니즘 세트]가 포함되어 있습니다.](/doc/security/fips140)

Go 암호화 모듈은 FIPS 140-3 승인된 알고리즘을 구현하는 데 사용되는 내부 표준 라이브러리 패키지의 집합입니다. 애플리케이션은 Go 암호화 모듈을 사용하여 승인된 알고리즘을 사용하기 위해 변경할 필요가 없습니다.

새로운 `GOFIPS140` 환경 변수를 사용하여 빌드에서 사용할 Go
암호화 모듈 버전을 선택할 수 있습니다. 새로운 `fips140` [GODEBUG
설정](/doc/godebug)을 사용하여 런타임에 FIPS 140-3 모드를 활성화할 수 있습니다.

Go 1.24에는 Go 암호화 모듈 버전 v1.0.0이 포함되어 있으며, 현재 CMVP 인증을 받은 실험실에서 테스트되고 있습니다.

### 새로운 실험적 테스트/synctest 패키지 {#testing-synctest}

새로운 실험적인 [`testing/synctest`](/pkg/testing/synctest/) 패키지는 동시 코드 테스트를 위한 지원을 제공합니다.
- `[`synctest.Run`](/pkg/testing/synctest/#Run)` 함수는 격리된 "버블" 내에서 고루틴 그룹을 시작합니다.
  버블 내에서 `[`time`](/pkg/time)` 패키지 함수는 가짜 시계를 사용하여 작동합니다.
- `[`synctest.Wait`](/pkg/testing/synctest#Wait)` 함수는 현재 버블 내의 모든 고루틴이 차단될 때까지 기다립니다.

자세한 내용은 패키지 문서를 참조하십시오.

`synctest` 패키지는 실험적인 기능이며, 빌드 시간에 `GOEXPERIMENT=synctest`를 설정하여 활성화해야 합니다.
패키지 API는 향후 릴리스에서 변경될 수 있습니다.
자세한 내용 및 피드백을 제공하려면 [issue #67434](/issue/67434)를 참조하십시오.

### 라이브러리의 세부 변경 사항 {#minor_library_changes}

#### [`archive`](/pkg/archive/)

`(*Writer).AddFS` 구현은 `archive/zip` 및 `archive/tar` 모두에서 빈 디렉토리에 대한 디렉토리 헤더를 작성합니다.

#### [`bytes`](/pkg/bytes/)

[`bytes`](/pkg/bytes) 패키지는 여러 개의 반복자를 사용하는 함수를 추가합니다:
- [`Lines`](/pkg/bytes#Lines)는 바이트 슬라이스의 개행 문자로 구분된 줄에 대한 반복자를 반환합니다.
- [`SplitSeq`](/pkg/bytes#SplitSeq)는 구분자를 기준으로 바이트 슬라이스의 모든 하위 슬라이스에 대한 반복자를 반환합니다.
- [`SplitAfterSeq`](/pkg/bytes#SplitAfterSeq)는 구분자의 각 인스턴스 다음에 바이트 슬라이스의 하위 슬라이스에 대한 반복자를 반환합니다.
- [`FieldsSeq`](/pkg/bytes#FieldsSeq)는 [`unicode.IsSpace`](/pkg/unicode#IsSpace)에 의해 정의된 공백 문자의 연속으로 바이트 슬라이스를 분할한 하위 슬라이스에 대한 반복자를 반환합니다.
- [`FieldsFuncSeq`](/pkg/bytes#FieldsFuncSeq)는 특정 조건을 만족하는 유니코드 코드 포인트의 연속으로 바이트 슬라이스를 분할한 하위 슬라이스에 대한 반복자를 반환합니다.

#### [`crypto/aes`](/pkg/crypto/aes/)

`[`NewCipher`](/pkg/crypto/aes#NewCipher) 함수가 반환하는 값은 더 이상
`NewCTR`, `NewGCM`, `NewCBCEncrypter`, 그리고 `NewCBCDecrypter`
메서드를 구현하지 않습니다. 이러한 메서드는 문서화되지 않았으며 모든 아키텍처에서 사용 가능하지 않았습니다.
대신, `[`Block`](/pkg/crypto/cipher#Block) 값을 적절한
`[crypto/cipher](https://pkg.go.dev/crypto/cipher)` 함수에 직접 전달해야 합니다.
현재, `crypto/cipher`는 `Block` 값에 이러한 메서드를 여전히 확인합니다.
표준 라이브러리에서 더 이상 사용되지 않더라도 말입니다.

#### [`crypto/cipher`](/pkg/crypto/cipher/)

새로운 [`NewGCMWithRandomNonce`](/pkg/crypto/cipher#NewGCMWithRandomNonce)
함수는 `AEAD`를 반환하며, `Seal` 작업 중에 무작위 nonce를 생성하고 이를 암호화된 텍스트 앞에 추가하여 AES-GCM을 구현합니다.

[`Stream`](/pkg/crypto/cipher#Stream) 구현이 [`NewCTR`](/pkg/crypto/cipher#NewCTR)를 사용하여 [`crypto/aes`](/pkg/crypto/aes/)와 함께 사용될 때, amd64 및 arm64에서 여러 배 더 빠릅니다.

[`NewOFB`](/pkg/crypto/cipher#NewOFB),
[`NewCFBEncrypter`](/pkg/crypto/cipher#NewCFBEncrypter), 및
[`NewCFBDecrypter`](/pkg/crypto/cipher#NewCFBDecrypter)는 더 이상 사용되지 않습니다.
OFB 및 CFB 모드는 인증되지 않으므로, 일반적으로 공격자가 평문 데이터를 조작하고 복구할 수 있습니다. 애플리케이션은 [`AEAD`](/pkg/crypto/cipher#AEAD) 모드를 사용하는 것이 권장됩니다. 인증되지 않은 [`Stream`](/pkg/crypto/cipher#Stream) 모드가 필요한 경우, [`NewCTR`](/pkg/crypto/cipher#NewCTR)를 사용하십시오.

#### [`crypto/ecdsa`](/pkg/crypto/ecdsa/)

<!-- go.dev/issue/64802 -->
[`PrivateKey.Sign`](/pkg/crypto/ecdsa#PrivateKey.Sign)는 이제 무작위 소스가 `nil`일 경우, [RFC 6979](https://www.rfc-editor.org/rfc/rfc6979.html)에 따라 결정적인 서명을 생성합니다.

#### [`crypto/md5`](/pkg/crypto/md5/)

[`md5.New`](/pkg/md5#New)에서 반환되는 값은 이제 `encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 인터페이스도 구현합니다.

#### [`crypto/rand`](/pkg/crypto/rand/)

<!-- go.dev/issue/66821 -->
`Read` 함수는 이제 실패할 가능성이 없습니다.
항상 `nil`을 `error` 결과로 반환합니다.
만약 `Read`가 `Reader`에서 읽을 때 오류를 만나면, 프로그램은 복구할 수 없이 종료됩니다.
참고로, 기본 `Reader`가 사용하는 플랫폼 API는 항상 성공한다는 설명이 되어 있으므로, 이 변경 사항은 `Reader` 변수를 재정의하는 프로그램에만 영향을 미쳐야 합니다. 예외는 리눅스 커널 버전 3.17 이전 버전에서, 기본 `Reader`가 여전히 `/dev/urandom`을 열고 실패할 수 있다는 것입니다.

<!-- go.dev/issue/69577 -->
Linux 6.11 이상에서는 `Reader`가 이제 vDSO를 통해 `getrandom` 시스템 호출을 사용합니다.
특히 작은 읽기 작업의 경우, 몇 배 더 빠릅니다.

<!-- CL 608395 -->
OpenBSD에서, `Reader`는 이제 `arc4random_buf(3)`를 사용합니다.

<!-- go.dev/issue/67057 -->
새로운 `Text` 함수는 암호학적으로 안전한 임의의 텍스트 문자열을 생성하는 데 사용할 수 있습니다.

#### [`crypto/rsa`](/pkg/crypto/rsa/)

[`GenerateKey`](/pkg/crypto/rsa#GenerateKey)는 이제 1024비트보다 작은 키를 요청할 경우 오류를 반환합니다.
모든 Sign, Verify, Encrypt, Decrypt 메서드는 1024비트보다 작은 키를 사용할 때 오류를 반환합니다. 이러한 키는 안전하지 않으며 사용해서는 안 됩니다.
[GODEBUG 설정](/doc/godebug) `rsa1024min=0`은 이전 동작을 복원하지만, 필요한 경우에만, 예를 들어 테스트 파일에 `//go:debug rsa1024min=0` 줄을 추가하여 수행할 것을 권장합니다.
새로운 `GenerateKey` [예제](/pkg/crypto/rsa#example-GenerateKey-TestKey)는 사용하기 쉬운 표준 2048비트 테스트 키를 제공합니다.

이제 `PrivateKey.Precompute`를 호출하는 것이 더 안전하고 효율적입니다.
[`PrivateKey.Precompute`](/pkg/crypto/rsa#PrivateKey.Precompute)를 호출하기 전에
`PrivateKey.Validate`를 호출하는 것이 좋습니다.
`Precompute`는 부분적으로 채워진 `PrecomputedValues` (예: JSON에서 키를 언마샬링할 때)가 있는 경우 더 빠릅니다.

이 패키지는 이제 `Validate`를 호출하지 않아도 더 많은 유효하지 않은 키를 거부하며,
[`GenerateKey`](/pkg/crypto/rsa#GenerateKey)가 손상된 무작위 소스에 대해 새로운 오류를 반환할 수 있습니다.
[`Primes`](/pkg/crypto/rsa#PrivateKey.Primes) 및
[`Precomputed`](/pkg/crypto/rsa#PrivateKey.Precomputed) 필드는 `PrivateKey`의 필드이며,
일부 값이 누락된 경우에도 사용 및 검증됩니다.
또한 RSA 키의 `crypto/x509` 파싱 및 직렬화에 대한 변경 사항에 대한 내용이 [아래](#cryptox509pkgcryptox509)에서 설명되어 있습니다.

<!-- go.dev/issue/43923 -->
[`SignPKCS1v15`](/pkg/crypto/rsa#SignPKCS1v15) 및
[`VerifyPKCS1v15`](/pkg/crypto/rsa#VerifyPKCS1v15)는 이제
SHA-512/224, SHA-512/256, 및 SHA-3를 지원합니다.

<!-- CL 639936 -->
[`GenerateKey`](/pkg/crypto/rsa#GenerateKey)는 이제 프라이빗 지수 생성을 위해 약간 다른 방법을 사용합니다(카말의 토테인 대신 유클리드의 토테인). 프라이머 팩터만 사용하여 외부에서 키를 재생하는 드문 경우에서는 다른 결과가 생성되지만 호환되는 결과를 생성할 수 있습니다.

<!-- CL 626957 -->
공개 키 및 개인 키 연산이 WASM에서 이제 두 배 더 빠릅니다.

#### [`crypto/sha1`](/pkg/crypto/sha1/)

`[sha1.New`](/pkg/sha1#New)에서 반환되는 값은 이제 `[encoding.BinaryAppender](https://golang.org/pkg/encoding#BinaryAppender)` 인터페이스도 구현합니다.

#### [`crypto/sha256`](/pkg/crypto/sha256/)

`[sha256.New`](/pkg/sha256#New) 및 `[sha256.New224`](/pkg/sha256#New224)에서 반환되는 값은 이제 `[encoding.BinaryAppender](https://golang.org/pkg/encoding#BinaryAppender)` 인터페이스를 구현합니다.

#### [`crypto/sha512`](/pkg/crypto/sha512/)

`sha512.New`,
`sha512.New384`,
`sha512.New512_224` 및
`sha512.New512_256` 함수에서 반환되는 값은 이제
`encoding.BinaryAppender` 인터페이스를 구현합니다.

#### [`crypto/subtle`](/pkg/crypto/subtle/)

새로운 [`WithDataIndependentTiming`](/pkg/crypto/subtle#WithDataIndependentTiming)
함수는 사용자가 특정 아키텍처에 특화된 기능을 활성화하여, 특정 명령어의 데이터 값 타이밍이 불변하도록 보장합니다.
이를 통해, 항상 일정하게 실행되도록 설계된 코드가 CPU 수준의 기능에 의해 변동 시간으로 실행되지 않도록 할 수 있습니다.
현재, `WithDataIndependentTiming`은 arm64에서 `PSTATE.DIT` 비트를 사용하며, 다른 모든 아키텍처에서는 아무런 효과가 없습니다. [GODEBUG 설정](/doc/godebug)
`dataindependenttiming=1`을 설정하면, Go 프로그램 전체에 DIT 모드가 활성화됩니다.

<!-- CL 622276 -->
`XORBytes` 함수의 출력은 반드시 입력과 완전히 일치하거나 전혀 겹치지 않아야 합니다. 이전에는 동작이 정의되지 않았지만, 이제 `XORBytes`는 panic을 발생시킵니다.

#### [`crypto/tls`](/pkg/crypto/tls/)

TLS 서버는 이제 암호화된 클라이언트 헬로 (ECH)를 지원합니다. 이 기능을 활성화하려면 [`Config.EncryptedClientHelloKeys`](/pkg/crypto/tls#Config.EncryptedClientHelloKeys) 필드를 채워야 합니다.

새로운 포스트-양자 [`X25519MLKEM768`](/pkg/crypto/tls#X25519MLKEM768) 키 교환 메커니즘이 이제 지원되며, `[Config.CurvePreferences](/pkg/crypto/tls#Config.CurvePreferences)`가 `nil`일 때 기본적으로 활성화됩니다.
[GODEBUG 설정](/doc/godebug) `tlsmlkem=0`는 기본 설정을 재설정합니다.
이는 큰 레코드를 제대로 처리하지 못하는 결함 있는 TLS 서버를 처리할 때 유용할 수 있으며, 이는 핸드셰이크 중에 시간 초과를 유발합니다 (참조: [TLS 포스트-양자 TL;DR 실패](https://tldr.fail/)).

`X25519Kyber768Draft00` 키 교환에 대한 지원이 제거되었습니다.

<!-- go.dev/issue/69393, CL 630775 -->
키 교환 순서는 이제 `crypto/tls` 패키지에 의해 완전히 처리됩니다.
`Config.CurvePreferences`의 순서는 더 이상 무시되지 않으며, 해당 필드가 채워질 때 어떤 키 교환을 활성화할지 결정하는 데만 사용됩니다.

<!-- go.dev/issue/32936 -->
새로운 [`ClientHelloInfo.Extensions`](/pkg/crypto/tls#ClientHelloInfo.Extensions)
필드는 클라이언트 헬로 메시지에 수신된 확장 기능의 ID 목록을 제공합니다.
이는 TLS 클라이언트를 식별하는 데 유용할 수 있습니다.

<!-- go.dev/issue/72111, Go 1.27 릴리즈 이후에 문서화됨 -->

`tlskyber`의 `GODEBUG` 설정 (Go 1.23에 추가됨: [Go 1.23](/doc/godebug#go-123))
이 설정이 제거되었습니다.

#### [`crypto/x509`](/pkg/crypto/x509/)

<!-- go.dev/issue/41682 -->
`x509sha1` [GODEBUG 설정](/doc/godebug)이 제거되었습니다.
[`Certificate.Verify`](/pkg/crypto/x509#Certificate.Verify)는 이제 SHA-1 기반의 서명을 지원하지 않습니다.

[`OID`](/pkg/crypto/x509#OID)는 이제
[`encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 및
[`encoding.TextAppender`](/pkg/encoding#TextAppender) 인터페이스를 구현합니다.

기본 인증서 정책 필드는 다음과 같이 변경되었습니다.
[`Certificate.PolicyIdentifiers`](/pkg/crypto/x509#Certificate.PolicyIdentifiers)
에서 [`Certificate.Policies`](/pkg/crypto/x509#Certificate.Policies)로.
인증서를 파싱할 때, 두 필드 모두 채워지지만, 인증서 정책은 이제 `Certificate.Policies` 필드에서 가져오게 됩니다. `Certificate.PolicyIdentifiers` 필드 대신. 이 변경 사항은 [GODEBUG 설정](/doc/godebug)에서 `x509usepolicies=0`으로 되돌릴 수 있습니다.

<!-- go.dev/issue/67675 -->
`CreateCertificate`(/pkg/crypto/x509#CreateCertificate) 이제 RFC 5280에 부합하는 방법을 사용하여 시리얼 번호를 생성합니다. 템플릿에 `Certificate.SerialNumber`(/pkg/crypto/x509#Certificate.SerialNumber) 필드가 `nil`인 경우, 오류가 발생하는 대신 시리얼 번호를 생성합니다.

[`Certificate.Verify`](/pkg/crypto/x509#Certificate.Verify)가 이제 RFC 5280 및 RFC 9618에 정의된 정책 검증을 지원합니다. 새로운
[`VerifyOptions.CertificatePolicies`](/pkg/crypto/x509#VerifyOptions.CertificatePolicies] 필드를 유효한 정책 [`OID`](/pkg/crypto/x509#OID] 집합으로 설정할 수 있습니다.
[`Certificate.Verify`](/pkg/crypto/x509#Certificate.Verify]에서 유효한 정책 그래프를 가진 인증서 체인만 반환됩니다.

[`MarshalPKCS8PrivateKey`](/pkg/crypto/x509#MarshalPKCS8PrivateKey)는 이제 유효하지 않은 RSA 키를 직렬화하는 대신 오류를 반환합니다.
([`MarshalPKCS1PrivateKey`](/pkg/crypto/x509#MarshalPKCS1PrivateKey)는 오류를 반환하지 않으며, 유효하지 않은 키를 제공할 때의 동작은 정의되지 않았습니다.)

[`ParsePKCS1PrivateKey`](/pkg/crypto/x509#ParsePKCS1PrivateKey) 및
[`ParsePKCS8PrivateKey`](/pkg/crypto/x509#ParsePKCS8PrivateKey]은 이제 인코딩된 CRT 값을 사용하고 유효성을 검사하므로, 이전에 허용되었던 유효하지 않은 RSA 키를 거부할 수 있습니다. CRT 값을 다시 계산하도록 되돌리려면 [GODEBUG 설정](/doc/godebug] `x509rsacrt=0`를 사용하십시오.

#### [`debug/elf`](/pkg/debug/elf/)

<!-- go.dev/issue/63952 -->

[`debug/elf`](/pkg/debug/elf) 패키지는 동적 ELF (Executable and Linkable Format) 파일에서 심볼 버전을 처리하는 기능을 추가합니다.
새로운 `File.DynamicVersions` 메서드(`/pkg/debug/elf#File.DynamicVersions`)는 ELF 파일에 정의된 동적 버전을 목록으로 반환합니다.
새로운 `File.DynamicVersionNeeds` 메서드(`/pkg/debug/elf#File.DynamicVersionNeeds`)는 이 ELF 파일에서 요구되는 동적 버전을 반환합니다.
이러한 동적 버전들은 다른 ELF 객체에서 정의되어 있습니다.
마지막으로, 새로운 `Symbol.HasVersion` 및 `Symbol.VersionIndex` 필드는 심볼의 버전을 나타냅니다.

#### [`encoding`](/pkg/encoding/)

두 개의 새로운 인터페이스, [`TextAppender`](/pkg/encoding#TextAppender) 및 [`BinaryAppender`](/pkg/encoding#BinaryAppender)가 도입되었습니다. 이러한 인터페이스는 객체의 텍스트 또는 이진 표현을 바이트 슬라이스에 추가하는 기능을 제공합니다. 이 인터페이스는 [`TextMarshaler`](/pkg/encoding#TextMarshaler) 및 [`BinaryMarshaler`](/pkg/encoding#BinaryMarshaler)와 동일한 기능을 제공하지만, 매번 새로운 슬라이스를 할당하는 대신 데이터를 기존 슬라이스에 직접 추가합니다.

이 인터페이스는 이미 `TextMarshaler` 및/또는 `BinaryMarshaler`를 구현한 표준 라이브러리 유형에 의해 구현됩니다.

#### [`encoding/json`](/pkg/encoding/json/)

<!-- go.dev/issue/45669 -->
마샬링 시, 구조체 필드에 새 `omitzero` 옵션을 사용하여 구조체 필드 태그를 지정하면, 값이 0인 경우 해당 필드가 생략됩니다. 필드 유형에 `IsZero() bool` 메서드가 있는 경우, 이를 사용하여 값이 0인지 여부를 판단합니다. 그렇지 않으면, 해당 유형의 [제로 값](/ref/spec#The_zero_value)인 경우 0으로 간주합니다.
`omitzero` 필드 태그는 0 값을 생략하려는 경우, `omitempty`보다 명확하고 오류 발생 가능성이 적습니다.
특히, `omitempty`와 달리, `omitzero`는 `time.Time` 값 ([`time.Time`](/pkg/time#Time))을 0 값으로 생략합니다. 이는 흔한 문제의 원인이 됩니다.

만약 `omitempty`와 `omitzero`가 모두 지정되면, 값이 비어 있거나 0이거나 (둘 중 하나) 둘 다인 경우 해당 필드는 삭제됩니다.

[`UnmarshalTypeError.Field`](/pkg/encoding/json#UnmarshalTypeError.Field)는 더 자세한 오류 메시지를 제공하기 위해 내장된 구조체를 포함합니다.

#### [`go/types`](/pkg/go/types/)

`go/types` 데이터 구조 중, `Len() int` 및 `At(int) T`와 같이 쌍의 메서드를 사용하여 시퀀스를 노출하는 모든 데이터 구조는 이제 반복자를 반환하는 메서드도 제공합니다. 이를 통해 다음과 같은 코드를 단순화할 수 있습니다:

```
params := fn.Type.(*types.Signature).Params()
for i := 0; i < params.Len(); i++ {
   use(params.At(i))
}
```

다음 Markdown 콘텐츠를 한국어로 번역합니다. Markdown 구조, 제목, 표, 링크, 목록, 인라인 코드 및 코드 펜을 유지합니다. Go 패키지 이름, 식별자, URL, 명령 또는 코드 스니펫은 번역하지 않습니다. 번역된 Markdown만 반환합니다.

```
for param in fn.Signature().Params().Variables():
   use(param)
```

다음은 메서드 목록입니다:
[`Interface.EmbeddedTypes`](/pkg/go/types#Interface.EmbeddedTypes),
[`Interface.ExplicitMethods`](/pkg/go/types#Interface.ExplicitMethods),
[`Interface.Methods`](/pkg/go/types#Interface.Methods),
[`MethodSet.Methods`](/pkg/go/types#MethodSet.Methods),
[`Named.Methods`](/pkg/go/types#Named.Methods),
[`Scope.Children`](/pkg/go/types#Scope.Children),
[`Struct.Fields`](/pkg/go/types#Struct.Fields),
[`Tuple.Variables`](/pkg/go/types#Tuple.Variables),
[`TypeList.Types`](/pkg/go/types#TypeList.Types),
[`TypeParamList.TypeParams`](/pkg/go/types#TypeParamList.TypeParams),
[`Union.Terms`](/pkg/go/types#Union.Terms).

#### [`hash/adler32`](/pkg/hash/adler32/)

`[`New`](/pkg/hash/adler32#New)에서 반환되는 값은 이제 `encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 인터페이스도 구현합니다.

#### [`hash/crc32`](/pkg/hash/crc32/)

반환되는 값인 [`New`](/pkg/hash/crc32#New) 및 [`NewIEEE`](/pkg/hash/crc32#NewIEEE)는 이제 [`encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 인터페이스를 구현합니다.

#### [`hash/crc64`](/pkg/hash/crc64/)

`[`New`](/pkg/hash/crc64#New)에서 반환되는 값은 이제 `encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 인터페이스도 구현합니다.

#### [`hash/fnv`](/pkg/hash/fnv/)

다음 함수들 (`New32`, `/pkg/hash/fnv#New32`, `New32a`, `/pkg/hash/fnv#New32a`, `New64`, `/pkg/hash/fnv#New64`, `New64a`, `/pkg/hash/fnv#New64a`, `New128`, `/pkg/hash/fnv#New128`, `New128a`, `/pkg/hash/fnv#New128a`)이 이제 `encoding.BinaryAppender` 인터페이스를 구현합니다.

#### [`hash/maphash`](/pkg/hash/maphash/)

새로운 [`Comparable`](/pkg/hash/maphash#Comparable) 및
[`WriteComparable`](/pkg/hash/maphash#WriteComparable) 함수는 모든 비교 가능한 값의 해시를 계산할 수 있습니다.
이를 통해 Go map 키로 사용할 수 있는 모든 것을 해시할 수 있습니다.

#### [`log/slog`](/pkg/log/slog/)

새로운 [`DiscardHandler`](/pkg/log/slog#DiscardHandler)는 항상 비활성화되고 출력을 항상 버리는 핸들러입니다.

[`Level`](/pkg/log/slog#Level) 및 [`LevelVar`](/pkg/log/slog#LevelVar)은 이제 `encoding.TextAppender` 인터페이스를 구현합니다.

#### [`math/big`](/pkg/math/big/)

[`Float`](/pkg/math/big#Float), [`Int`](/pkg/math/big#Int) 및 [`Rat`](/pkg/math/big#Rat)는 이제 `encoding.TextAppender` 인터페이스를 구현합니다.

#### [`math/rand`](/pkg/math/rand/)

`Seed` 함수 ([`Seed`](/pkg/math/rand#Seed))의 호출은 더 이상 영향을 미치지 않습니다.
원래 동작을 복원하려면 [GODEBUG 설정](/doc/godebug)에서 `randseednop=0`을 설정합니다.
자세한 내용은 [제안 #67273](/issue/67273)를 참조하십시오.

#### [`math/rand/v2`](/pkg/math/rand/v2/)

[`ChaCha8`](/pkg/math/rand/v2#ChaCha8) 및 [`PCG`](/pkg/math/rand/v2#PCG)는 이제 [`encoding.BinaryAppender`](/pkg/encoding#BinaryAppender) 인터페이스를 구현합니다.

#### [`net`](/pkg/net/)

[`ListenConfig`](/pkg/net#ListenConfig)는 이제 지원되는 시스템에서는 기본적으로 MPTCP를 사용합니다 (현재 Linux에서만 지원).

[`IP`](/pkg/net#IP)는 이제 [`encoding.TextAppender`](/pkg/encoding#TextAppender) 인터페이스를 구현합니다.

#### [`net/http`](/pkg/net/http/)

[`Transport`](/pkg/net/http#Transport)가 요청에 대한 1xx 유형의 정보 응답 수신에 대해 한도를 변경했습니다.
이전에는 5개의 1xx 응답을 수신한 후 요청을 중단하고 오류를 반환했습니다.
이제 모든 1xx 응답의 총 크기가 [`Transport.MaxResponseHeaderBytes`](/pkg/net/http#Transport.MaxResponseHeaderBytes) 구성 설정보다 크면 오류를 반환합니다.

또한, 요청에 `net/http/httptrace.ClientTrace.Got1xxResponse` 트레이스 훅이 포함되어 있는 경우, 1xx 응답의 총 개수에 대한 제한이 더 이상 없습니다.
`Got1xxResponse` 훅은 요청을 중단하기 위해 오류를 반환할 수 있습니다.

[`Transport`](/pkg/net/http#Transport) 및 [`Server`](/pkg/net/http#Server)는 이제 `HTTP2` 필드를 제공하여 HTTP/2 프로토콜 설정을 구성할 수 있습니다.

새로운 `Server.Protocols` 및 `Transport.Protocols` 필드는 서버 또는 클라이언트가 사용하는 HTTP 프로토콜을 간단하게 구성하는 방법을 제공합니다.

서버와 클라이언트는 암호화되지 않은 HTTP/2 연결을 지원하도록 구성될 수 있습니다.

`[Server.Protocols](https://pkg/net/http#Server.Protocols)`에 `UnencryptedHTTP2`가 포함되어 있으면, 서버는 암호화되지 않은 포트에서 HTTP/2 연결을 수락합니다. 서버는 동일한 포트에서 HTTP/1 및 암호화되지 않은 HTTP/2를 모두 수락할 수 있습니다.

`[Transport.Protocols`](/pkg/net/http#Transport.Protocols)가 UnencryptedHTTP2를 포함하고 HTTP1을 포함하지 않는 경우, 트랜스포트는 `http://` URL에 대해 암호화되지 않은 HTTP/2를 사용합니다.

트랜스포트가 HTTP/1과 암호화되지 않은 HTTP/2를 모두 사용하도록 구성된 경우, HTTP/1을 사용합니다.

"암호화되지 않은 HTTP/2 지원은 'HTTP/2 with Prior Knowledge'를 사용합니다. (RFC 9113, 3.3절)."
폐기된 "Upgrade: h2c" 헤더는 지원되지 않습니다.

#### [`net/netip`](/pkg/net/netip/)

[`Addr`](/pkg/net/netip#Addr), [`AddrPort`](/pkg/net/netip#AddrPort) 및 [`Prefix`](/pkg/net/netip#Prefix)는 이제 `encoding.BinaryAppender` 및
`encoding.TextAppender` 인터페이스를 구현합니다.

#### [`net/url`](/pkg/net/url/)

[`URL`](/pkg/net/url#URL)는 이제 `encoding.BinaryAppender` 인터페이스도 구현합니다.

#### [`os/user`](/pkg/os/user/)

On Windows, [`Current`](/pkg/os/user#Current)는 이제 Windows Nano Server에서도 사용할 수 있습니다.
구현이 업데이트되어 `NetApi32` 라이브러리의 함수를 사용하는 것을 피하도록 변경되었습니다. 이 라이브러리는 Nano Server에서 사용 가능하지 않습니다.

On Windows, [`Current`](/pkg/os/user#Current), [`Lookup`](/pkg/os/user#Lookup) 및 [`LookupId`](/pkg/os/user#LookupId)는 이제 다음 기본 서비스 사용자 계정을 지원합니다.
- `NT AUTHORITY\SYSTEM`
- `NT AUTHORITY\LOCAL SERVICE`
- `NT AUTHORITY\NETWORK SERVICE`

On Windows, [`Current`](/pkg/os/user#Current)의 성능이 현재 사용자가 느린 도메인에 가입된 경우에 현저히 향상되었습니다. 이는 많은 기업 사용자에게 흔한 경우입니다. 새로운 구현의 성능은 이제 십수 밀리초 수준이며, 이전 구현은 몇 초, 심지어 몇 분이 걸릴 수 있었습니다.

On Windows, [`Current`](/pkg/os/user#Current) now returns 사용자 계정 정보를 반환할 때, 현재 스레드가 다른 사용자를 모방하고 있을 경우, 현재 사용자 정보를 반환합니다. 이전에 오류를 반환했습니다.

#### [`regexp`](/pkg/regexp/)

[`Regexp`](/pkg/regexp#Regexp)는 이제 [`encoding.TextAppender`](/pkg/encoding#TextAppender) 인터페이스를 구현합니다.

#### [`runtime`](/pkg/runtime/)

[`GOROOT`](/pkg/runtime#GOROOT) 함수는 이제 사용되지 않습니다.
새로운 코드에서는 "go" 바이너리를 찾기 위해 시스템 경로를 사용하는 것이 좋습니다.
`go env GOROOT`를 사용하여 GOROOT를 찾으십시오.

#### [`strings`](/pkg/strings/)

[`strings`](/pkg/strings) 패키지는 여러 개의 반복자와 함께 작동하는 함수를 추가합니다:
- [`Lines`](/pkg/strings#Lines)는 문자열 내의 개행 문자로 구분된 줄에 대한 반복자를 반환합니다.
- [`SplitSeq`](/pkg/strings#SplitSeq)는 구분자를 기준으로 문자열을 분할하여 모든 하위 문자열에 대한 반복자를 반환합니다.
- [`SplitAfterSeq`](/pkg/strings#SplitAfterSeq)는 구분자의 각 인스턴스 후에 문자열을 분할하여 하위 문자열에 대한 반복자를 반환합니다.
- [`FieldsSeq`](/pkg/strings#FieldsSeq)는 [`unicode.IsSpace`](/pkg/unicode#IsSpace)에 의해 정의된 공백 문자의 연속으로 문자열을 분할하여 하위 문자열에 대한 반복자를 반환합니다.
- [`FieldsFuncSeq`](/pkg/strings#FieldsFuncSeq)는 특정 조건(predicate)을 만족하는 유니코드 코드 포인트 연속으로 문자열을 분할하여 하위 문자열에 대한 반복자를 반환합니다.

#### [`sync`](/pkg/sync/)

`[sync.Map](pkg/sync#Map)`의 구현이 변경되어 성능이 향상되었으며, 특히 맵 수정에 대해 그렇습니다.
예를 들어, 키 집합의 수정은 더 큰 맵에서 상당한 경쟁을 겪을 가능성이 줄어들었고, 맵에서 낮은 경쟁 부하를 달성하는 데 더 이상 초기화 시간이 필요하지 않습니다.

만약 문제가 발생하면, 빌드 시간에 `GOEXPERIMENT=nosynchashtriemap`을 설정하여 이전 구현으로 되돌릴 수 있습니다. 자세한 내용은 [이슈를 제출해주세요](/issue/new).

#### [`testing`](/pkg/testing/)

새로운 [`T.Context`](/pkg/testing#T.Context) 및 [`B.Context`](/pkg/testing#B.Context) 메서드는 테스트가 완료되고 테스트 정리 함수가 실행되기 전에 취소된 컨텍스트를 반환합니다.

<!-- testing.B.Loop가 6-stdlib/6-testing-bloop.md에 언급됨. -->

새로운 `[T.Chdir](pkg/testing#T.Chdir)` 및 `[B.Chdir](pkg/testing#B.Chdir)` 메서드는 테스트 또는 벤치마크의 실행 기간 동안 작업 디렉토리를 변경하는 데 사용할 수 있습니다.

#### [`text/template`](/pkg/text/template/)

템플릿이 이제 `range-over-func` 및 `range-over-int`를 지원합니다.

#### [`time`](/pkg/time/)

[`Time`](/pkg/time#Time)은 이제 `encoding.BinaryAppender` 및 `encoding.TextAppender` 인터페이스를 구현합니다.

## 포트

### 리눅스 {#linux}

<!-- go.dev/issue/67001 -->
[공지](go1.23#linux)된 바와 같이, Go 1.24는 Linux 커널 버전 3.2 이상을 요구합니다.

### Darwin
```
# Darwin
```

<!-- go.dev/issue/69839 -->
Go 1.24은 macOS 11 Big Sur에서 실행되는 마지막 버전입니다.
Go 1.25는 macOS 12 Monterey 또는 그 이상을 요구합니다.

### WebAssembly {#wasm}

웹 어셈블리

<!-- go.dev/issue/65199, CL 603055 -->
`go:wasmexport` 컴파일러 지시어를 통해 Go 프로그램이 WebAssembly 호스트로 함수를 내보낼 수 있습니다.

WebAssembly 시스템 인터페이스 미리보기 1 (`GOOS=wasip1 GOARCH=wasm`)에서 Go 1.24는 다음을 지원합니다:
`reactor/library`로 Go 프로그램을 빌드하는 것,
`-buildmode=c-shared` 빌드 플래그를 지정하여.
[https://github.com/WebAssembly/WASI/blob/63a46f61052a21bfab75a76558485cf097c0dbba/legacy/application-abi.md#current-unstable-abi](https://github.com/WebAssembly/WASI/blob/63a46f61052a21bfab75a76558485cf097c0dbba/legacy/application-abi.md#current-unstable-abi)

<!-- go.dev/issue/66984, CL 626615 -->
이제 `go:wasmimport` 함수에 대한 인자 또는 결과 유형으로 더 많은 유형이 허용됩니다.
특히, `bool`, `string`, `uintptr`, 그리고 특정 유형의 포인터가 허용됩니다 (자세한 내용은 [문서](pkg/cmd/compile#hdr-WebAssembly_Directives) 참조).
또한 32비트 및 64비트 정수 및 부동 소수점 유형, `unsafe.Pointer`도 이미 허용됩니다.
이러한 유형은 `go:wasmexport` 함수에 대한 인자 또는 결과 유형으로도 허용됩니다.

<!-- go.dev/issue/68024 -->
웹 어셈블리 지원 파일이 `lib/wasm`에서 `misc/wasm`으로 이동되었습니다.

<!-- CL 621635, CL 621636 -->
초기 메모리 크기가 크게 줄어듭니다. 특히, 작은 WebAssembly 애플리케이션의 경우에 더욱 그렇습니다.

### Windows
```
{#windows}
```

<!-- go.dev/issue/70705 -->
32비트 Windows/ARM 포트(`GOOS=windows GOARCH=arm`)가 "비정상"으로 표시되었습니다.
자세한 내용은 [issue #70705](/issue/70705)를 참조하세요.

<!-- 1.24 릴리스 노트에 언급할 필요가 없는 항목이지만, relnote todo에 의해 캡처됨.

수락된 제안: https://go.dev/issue/25309 (https://go.dev/cl/594018, https://go.dev/cl/595120, https://go.dev/cl/595564, https://go.dev/cl/601778) - 새로운 x/crypto 패키지; 언급할 필요가 없어 보임
수락된 제안: https://go.dev/issue/43744 (https://go.dev/cl/357530) - 표준 라이브러리에 변경 없음
수락된 제안: https://go.dev/issue/60905 (https://go.dev/cl/610195) - CL 610195가 되돌림
수락된 제안: https://go.dev/issue/61395 (https://go.dev/cl/594738, https://go.dev/cl/594976) - amd64에서 sync/atomic AND/OR 연산을 기본으로 추가, 하지만 API는 Go 1.23에 이미 추가됨; CL 594976은 수정 사항; 아마도 Go 1.24 릴리스 노트에 필요하지 않음 (성능 변경만)
수락된 제안: https://go.dev/issue/51269 (https://go.dev/cl/627035) - Go 1.24 릴리스 노트에 언급할 가치가 있거나, 또는 제외해도 괜찮음; https://go.dev/issue/51269#issuecomment-2501802763에서 언급됨; Ian은 제외해도 괜찮다고 확인
수락된 제안: https://go.dev/issue/66540 (https://go.dev/cl/603958) - Go 언어 사양 명확화; Go 1.24 릴리스 노트에 언급할 필요가 없을 수 있음; https://go.dev/issue/66540#issuecomment-2502051684에서 언급됨; Robert은 실제로 언급할 필요가 없다고 확인
수락된 제안: https://go.dev/issue/34208 (https://go.dev/cl/586241) - CL 586241은 Go 1.23 기능에 대한 수정 사항이며, Go 1.24 릴리스 노트에 추가적인 사항은 필요 없어 보임
수락된 제안: https://go.dev/issue/43993 (https://go.dev/cl/626116) - CL 626116는 vet 변경을 준비하지만, vet 변경 자체는 Go 1.24에 구현되지 않았으므로, Go 1.24 릴리스 노트에 언급할 필요 없음
수락된 제안: https://go.dev/issue/44505 (https://go.dev/cl/609955) - CL 609955는 x/tools 내부 정리 작업이며, Go 1.24 릴리스 노트에 언급할 필요 없음
수락된 제안: https://go.dev/issue/61476 (https://go.dev/cl/608255) - CL 608255는 Go 1.23에 추가된 GORISCV64를 기반으로 함; Go 1.24 릴리스 노트에 언급할 필요 없음
수락된 제안: https://go.dev/issue/66315 (https://go.dev/cl/577996) - x/tools/go/analysis에 Pass.Module 필드를 추가하는 것은 Go 1.24 릴리스 노트에 언급할 필요가 없어 보임
수락된 제안: https://go.dev/issue/57786 (https://go.dev/cl/472717) - CL 472717은 x/net/http2에 있으며 Go 1.21 제안을 참조; Go 1.24 릴리스 노트에 추가적인 사항은 필요 없어 보임
수락된 제안: https://go.dev/issue/54265 (https://go.dev/cl/609915, https://go.dev/cl/610675) - Go 1.22 제안을 참조하는 CL; 추가적인 사항은 Go 1.24 릴리스 노트에 필요 없음
수락된 제안: https://go.dev/issue/53021 (https://go.dev/cl/622276) - CL 622276은 문서 개선; Go 1.20 제안인 53021은 추가적인 사항이 필요 없음
수락된 제안: https://go.dev/issue/51430 (https://go.dev/cl/613375) - CL 613375는 x/tools 내부 문서 주석; Go 1.20/1.21 제안인 51430에 대한 추가적인 사항은 필요 없음
수락된 제안: https://go.dev/issue/38445 (https://go.dev/cl/626495) - CL 626495는 x/tools/go/package에 대한 제안 38445를 구현; 추가적인 사항은 Go 1.24 릴리스 노트에 필요 없음
수락된 제안: https://go.dev/issue/56986 (https://go.dev/cl/618115) - CL 618115는 문서 추가; 추가적인 사항은 Go 1.24 릴리스 노트에 언급할 필요 없음
수락된 제안: https://go.dev/issue/60061 (https://go.dev/cl/612038) - CL 612038은 x/tools/go/ast에서 deprecate를 하고 Go 1.22 제안을 참조; 추가적인 사항은 Go 1.24 릴리스 노트에 필요 없음
수락된 제안: https://go.dev/issue/61324 (https://go.dev/cl/411907) - CL 411907은 x/tools CL로 새로운 패키지에 대한 제안을 구현; 추가적인 사항은 Go 1.24 릴리스 노트에 필요 없음
수락된 제안: https://go.dev/issue/61777 (https://go.dev/cl/601496) - CL 601496은 x/net/http2.Server에 WriteByteTimeout 필드를 추가; 추가적인 사항은 Go 1.24 릴리스 노트에 필요 없음
수락된 제안: https://go.dev/issue/61940 (https://go.dev/cl/600997) - CL 600997은 x/build에서 obsolete 코드를 삭제하고 수락된 제안을 참조; 추가적인 사항은 Go 1.24 릴리스 노트에 필요 없음
수락된 제안: https://go.dev/issue/62113 (https://go.dev/cl/594195) - CL 594195는 x/net/html에 iterator 관련 추가 기능; 추가적인 사항은 Go 1.24 릴리스 노트에 필요 없음
수락된 제안: https://go.dev/issue/62484 (https://go.dev/cl/600775) - CL 600775는 CopyFS symlink 동작을 문서화하고 Go 1.23 제안을 참조; 추가적인 사항은 Go 1.24 릴리스 노트에 필요 없음
수락된 제안: https://go.dev/issue/64207 (https://go.dev/cl/605875) - x/website CL로 Go 1.23 제안을 따름; 추가적인 사항은 Go 1.24 릴리스 노트에 필요 없음
수락된 제안: https://go.dev/issue/65236 (https://go.dev/cl/596135) - CL 596135는 Go 1.23 제안 65236에 대한 테스트 추가; 추가적인 사항은 Go 1.24 릴리스 노트에 필요 없음
수락된 제안: https://go.dev/issue/67795 (https://go.dev/cl/616218) - x/tools/go/ast/inspector에 iterator 지원; 추가적인 사항은 Go 1.24 릴리스 노트에 필요 없음
수락된 제안: https://go.dev/issue/67812 (https://go.dev/cl/601497) - x/net/http2.Server에 configurable server pings 추가; 추가적인 사항은 Go 1.24 릴리스 노트에 필요 없음
수락된 제안: https://go.dev/issue/68232 (https://go.dev/cl/595676) - x/sys/unix 추가; 추가적인 사항은 Go 1.24 릴리스 노트에 필요 없음
수락된 제안: https://go.dev/issue/68898 (https://go.dev/cl/607495, https://go.dev/cl/620036, https://go.dev/cl/620135, https://go.dev/cl/623638) - x/tools/go/gcexportdata에 2개의 릴리스 및 tip 지원 정책을 문서화하는 제안; x/tools이므로 Go 1.24 릴리스 노트에 추가할 필요 없음
수락된 제안: https://go.dev/issue/69095 (https://go.dev/cl/593683, https://go.dev/cl/608955, https://go.dev/cl/610716) - Go 1.22 제안을 참조하는 CL; 추가적인 사항은 Go 1.24 릴리스 노트에 필요 없음
수락된 제안: https://go.dev/issue/68384 (https://go.dev/cl/611875) - Go Telemetry의 범위를 Delve를 포함하도록 확장하는 것은 Go 1.24와 직접 관련이 없으며 Go 1.24 릴리스 노트에 언급할 필요가 없음
수락된 제안: https://go.dev/issue/69291 (https://go.dev/cl/610939) - CL 610939는 x/tools에서 코드를 리팩터링하고 Go 1.24에서 구현될 예정인 #69291 제안을 참조; Go 1.24 릴리스 노트에 추가할 필요 없음
수락된 제안: https://go.dev/issue/69360 (https://go.dev/cl/614158, https://go.dev/cl/614159, https://go.dev/cl/614635, https://go.dev/cl/614675) - 69360 제안은 x/tools에서 gorename을 태그하고 삭제하는 것으로, Go 1.24 릴리스 노트에 추가할 필요 없음
수락된 제안: https://go.dev/issue/61417 (https://go.dev/cl/605955) - x/oauth2에 새로운 필드; Go 1.24 릴리스 노트에 추가할 필요 없음
수락된 제안: https://go.dev/issue/29266 (https://go.dev/cl/632897) - go.dev/doc/contribute에 대한 문서만 포함하는 제안; 추가적인 사항은 Go 1.24 릴리스 노트에 필요 없음
