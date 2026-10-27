<!--{
  "Template": true,
  "Title": "튜토리얼: 퍼징 시작하기",
  "HideTOC": true,
  "Breadcrumb": true
}-->

이 튜토리얼에서는 Go의 퍼징(fuzzing) 기초를 소개합니다. 퍼징을 사용하면 무작위 데이터를 테스트에 입력하여 취약점을 찾거나 크래시를 유발하는 입력을 탐색합니다. 퍼징을 통해 찾을 수 있는 취약점의 예로는 SQL 인젝션, 버퍼 오버플로우, 서비스 거부(DoS) 및 크로스 사이트 스크립팅(XSS) 공격 등이 있습니다.

이 튜토리얼에서는 간단한 함수에 대한 퍼즈 테스트(fuzz test)를 작성하고, `go` 명령어를 실행하며, 코드의 문제를 디버깅하고 수정하는 방법을 알아봅니다.

이 튜토리얼 전반에 걸쳐 사용되는 용어에 대한 도움말은 [Go Fuzzing glossary](/security/fuzz/#glossary)를 참조하세요.

다음 섹션들을 통해 학습을 진행하시게 됩니다:

1. [코드를 위한 폴더를 생성합니다.](#create_folder)
2. [테스트할 코드를 추가합니다.](#code_to_test)
3. [단위 테스트를 추가합니다.](#unit_test)
4. [퍼즈 테스트를 추가합니다.](#fuzz_test)
5. [두 개의 버그를 수정합니다.](#fix_invalid_string_error)
6. [추가 리소스를 살펴봅니다.](#conclusion)

**참고:** 다른 튜토리얼은 [Tutorials](/doc/tutorial/index.html)를 참조하십시오.

**참고:** Go 퍼징(fuzzing)은 현재 [Go Fuzzing 문서](/security/fuzz/#requirements)에 나열된 일부 기본 타입들만 지원하며, 향후 더 많은 기본 타입에 대한 지원이 추가될 예정입니다.

## 사전 요구 사항

- **Go.** 이 튜토리얼을 따라오시려면 최신 버전의 Go를 사용하시는 것을 권장합니다.
  설치 안내는 [Installing Go](/doc/install)를 참조하십시오.
- **코드 편집 도구.** 사용 가능한 모든 텍스트 편집기를 사용할 수 있습니다.
- **커맨드 터미널.** Go는 Linux 및 Mac의 모든 터미널, 그리고 Windows의 PowerShell 또는 cmd에서 잘 작동합니다.
- **퍼징(fuzzing)을 지원하는 환경.** 커버리지 계측(coverage instrumentation)을 이용한 Go 퍼징은 현재 AMD64 및 ARM64 아키텍처에서만 사용할 수 있습니다.

## 코드 폴더 생성하기 {#create_folder}

시작하려면, 작성할 코드를 위한 폴더를 생성하세요.

1. 명령 프롬프트를 열고 홈 디렉터리로 이동하십시오.

Linux 또는 Mac에서:

```
   $ cd
   ```

Windows에서:

```
   C:\> cd %HOMEPATH%
   ```

나머지 튜토리얼에서는 프롬프트로 `$`가 표시됩니다. 사용하시는 명령어들은 Windows에서도 작동합니다.

2. 명령 프롬프트에서 코드를 저장할 `fuzz`라는 이름의 디렉토리를 생성합니다.

```
   $ mkdir fuzz
   $ cd fuzz
   ```

3. 코드를 보관할 모듈을 생성합니다.

`go mod init` 명령어를 실행하고, 새 코드의 모듈 경로를 지정하세요.

```
   $ go mod init example/fuzz
   go: creating new go.mod: module example/fuzz
   ```

**참고:** 프로덕션 코드에서는 자신의 필요에 더 적합하고 구체적인 모듈 경로를 지정해야 합니다. 자세한 내용은 [의존성 관리](/doc/modules/managing-dependencies)를 참조하세요.

다음으로, 나중에 퍼징(fuzz)할 문자열 반전(reverse)을 위한 간단한 코드를 추가하겠습니다.

## 테스트 코드 추가 {#code_to_test}

이 단계에서는 문자열을 뒤집는 함수를 추가하게 됩니다.

### 코드 작성하기

1. 텍스트 에디터를 사용하여 `fuzz` 디렉토리에 `main.go`라는 파일을 생성하세요.
2. `main.go` 파일의 최상단에 다음 패키지 선언문을 붙여넣으세요.

```
    package main
    ```

단독 실행 프로그램(라이브러리와 반대되는 개념)은 항상 `main` 패키지에 속합니다.

3. 패키지 선언 아래에 다음 함수 선언을 붙여넣으세요.

```
    func Reverse(s string) string {
        b := []byte(s)
        for i, j := 0, len(b)-1; i {{raw "<"}} len(b)/2; i, j = i+1, j-1 {
            b[i], b[j] = b[j], b[i]
        }
        return string(b)
    }
    ```

이 함수는 `string`을 입력받아 한 번에 한 `byte`씩 루프를 돌며, 마지막에 역순으로 정렬된 문자열을 반환합니다.

_참고:_ 이 코드는 golang.org/x/example 내의 `stringutil.Reverse` 함수를 기반으로 합니다.

4.  `main.go` 파일의 상단, 패키지 선언 아래에 다음 `main` 함수를 붙여넣으세요. 이 함수는 문자열을 초기화하고, 이를 뒤집어 출력하며, 이 과정을 반복합니다.

```
    func main() {
        input := "The quick brown fox jumped over the lazy dog"
        rev := Reverse(input)
        doubleRev := Reverse(rev)
        fmt.Printf("original: %q\n", input)
        fmt.Printf("reversed: %q\n", rev)
        fmt.Printf("reversed again: %q\n", doubleRev)
    }
    ```

이 함수는 몇 번의 `Reverse` 작업을 수행한 후, 그 결과를 커맨드 라인에 출력합니다. 이는 코드가 실제로 어떻게 작동하는지 확인하고, 잠재적으로 디버깅하는 데 도움이 될 수 있습니다.

5. `main` 함수는 `fmt` 패키지를 사용하므로, 이를 import 해야 합니다.

코드의 첫 몇 줄은 다음과 같아야 합니다:

```
    package main
```

import "fmt"
    ```

### 코드 실행하기

`main.go` 파일이 포함된 디렉토리의 명령줄에서 코드를 실행하세요.

```
$ go run .
original: "The quick brown fox jumped over the lazy dog"
reversed: "god yzal eht revo depmuj xof nworb kciuq ehT"
reversed again: "The quick brown fox jumped over the lazy dog"
```

원래의 문자열과 이를 한 번 뒤집은 결과, 그리고 다시 한 번 뒤집어 원래와 동일해진 결과를 확인할 수 있습니다.

이제 코드가 실행되므로, 테스트를 진행할 차례입니다.

## 단위 테스트 추가 {#unit_test}

이 단계에서는 `Reverse` 함수에 대한 기본적인 단위 테스트를 작성하게 됩니다.

### 코드 작성하기

1. 텍스트 편집기를 사용하여 `fuzz` 디렉토리에 `reverse_test.go`라는 파일을 생성하세요.
2. 다음 코드를 `reverse_test.go`에 붙여넣으세요.

```
   package main
```

```go
import (
       "testing"
   )
```

```go
func TestReverse(t *testing.T) {
       testcases := []struct {
           in, want string
       }{
           {"Hello, world", "dlrow ,olleH"},
           {" ", " "},
           {"!12345", "54321!"},
       }
       for _, tc := range testcases {
           rev := Reverse(tc.in)
           if rev != tc.want {
                   t.Errorf("Reverse: %q, want %q", rev, tc.want)
           }
       }
   }
   ```

이 간단한 테스트는 나열된 입력 문자열들이 올바르게 반전되는지 확인합니다.

### 코드 실행하기

`go test`를 사용하여 유닛 테스트를 실행하세요.

```
$ go test
PASS
ok      example/fuzz  0.013s
```

다음으로, 단위 테스트를 퍼즈 테스트(fuzz test)로 변경하겠습니다.

## 퍼즈 테스트 추가하기 {#fuzz_test}

단위 테스트에는 한계가 있는데, 즉 개발자가 각 입력을 테스트에 직접 추가해야 한다는 점입니다. 퍼징(fuzzing)의 장점 중 하나는 코드에 필요한 입력을 자동으로 생성하며, 개발자가 생각한 테스트 케이스가 도달하지 못한 엣지 케이스(edge cases)를 식별할 수 있다는 것입니다.

이 섹션에서는 단위 테스트를 퍼즈 테스트(fuzz test)로 변환하여, 더 적은 노력으로 더 많은 입력을 생성하는 방법을 알아봅니다!

단위 테스트, 벤치마크 및 퍼즈 테스트를 동일한 `*_test.go` 파일에 유지할 수 있다는 점에 유의하세요. 하지만 이 예제에서는 단위 테스트를 퍼즈 테스트로 변환해 보겠습니다.

### 코드 작성하기

텍스트 에디터에서 `reverse_test.go`에 있는 단위 테스트를 다음 퍼즈 테스트(fuzz test)로 교체하세요.

```go
func FuzzReverse(f *testing.F) {
    testcases := []string{"Hello, world", " ", "!12345"}
    for _, tc := range testcases {
        f.Add(tc)  // 시드 코퍼스(seed corpus)를 제공하기 위해 f.Add를 사용합니다.
    }
    f.Fuzz(func(t *testing.T, orig string) {
        rev := Reverse(orig)
        doubleRev := Reverse(rev)
        if orig != doubleRev {
            t.Errorf("Before: %q, after: %q", orig, doubleRev)
        }
        if utf8.ValidString(orig) && !utf8.ValidString(rev) {
            t.Errorf("Reverse produced invalid UTF-8 string %q", rev)
        }
    })
}
```

퍼징(Fuzzing)에도 몇 가지 한계가 있습니다. 단위 테스트에서는 `Reverse` 함수의 예상 출력값을 예측하고, 실제 출력값이 해당 예상치와 일치하는지 확인할 수 있습니다.

예를 들어, `Reverse("Hello, world")` 테스트 케이스에서 단위 테스트는 반환 값으로 `"dlrow ,olleH"`를 지정합니다.

퍼징(fuzzing)을 할 때는 입력값을 제어할 수 없기 때문에, 예상되는 출력값을 예측할 수 없습니다.

하지만 퍼즈 테스트(fuzz test)에서 확인할 수 있는 `Reverse` 함수의 몇 가지 속성들이 있습니다. 이 퍼즈 테스트에서 확인하는 두 가지 속성은 다음과 같습니다:

1. 문자열을 두 번 뒤집으면 원래 값이 유지됩니다.
2. 뒤집힌 문자열은 유효한 UTF-8 상태를 유지합니다.

단위 테스트와 퍼즈 테스트(fuzz test)의 구문 차이점에 유의하세요:

- 함수는 `TestXxx` 대신 `FuzzXxx`로 시작하며, `*testing.T` 대신 `*testing.F`를 인자로 받습니다.
- `t.Run` 실행이 예상되는 위치에 대신 `f.Fuzz`가 사용됩니다. `f.Fuzz`는 파라미터로 `*testing.T`와 퍼징할 타입들을 받는 퍼즈 타겟(fuzz target) 함수를 인자로 받습니다. 단위 테스트의 입력값들은 `f.Add`를 사용하여 시드 코퍼스(seed corpus) 입력으로 제공됩니다.

새로운 패키지인 `unicode/utf8`가 임포트되었는지 확인하십시오.

```go
package main

import (
    "testing"
    "unicode/utf8"
)
```

단위 테스트를 퍼즈 테스트(fuzz test)로 변환했으므로, 이제 테스트를 다시 실행할 차례입니다.

### 코드 실행하기

1. 시드 입력값이 통과하는지 확인하기 위해 퍼징 없이 퍼즈 테스트를 실행하세요.

```
   $ go test
   PASS
   ok      example/fuzz  0.013s
   ```

해당 파일에 다른 테스트들이 있고 퍼즈 테스트(fuzz test)만 실행하고 싶다면 `go test -run=FuzzReverse`를 실행할 수도 있습니다.

2. `FuzzReverse`를 퍼징(fuzzing)으로 실행하여, 무작위로 생성된 문자열 입력으로 인해 실패가 발생하는지 확인합니다. 이는 `go test`에 새로운 플래그인 `-fuzz`를 `Fuzz` 매개변수로 설정하여 실행합니다. 아래 명령어를 복사하세요.

```
    $ go test -fuzz=Fuzz
    ```

또 다른 유용한 플래그는 퍼징에 소요되는 시간을 제한하는 `-fuzztime`입니다.
    예를 들어, 아래 테스트에서 `-fuzztime 10s`를 지정하면,
    이전에 실패가 발생하지 않는 한 테스트는 기본적으로
    10초가 경과한 후 종료됩니다. 다른 테스트 플래그를 확인하려면 cmd/go
    문서의 [이 섹션](https://pkg.go.dev/cmd/go#hdr-Testing_flags)을 참조하십시오.

이제 방금 복사한 명령어를 실행하세요.

```
   $ go test -fuzz=Fuzz
   fuzz: elapsed: 0s, gathering baseline coverage: 0/3 completed
   fuzz: elapsed: 0s, gathering baseline coverage: 3/3 completed, now fuzzing with 8 workers
   fuzz: minimizing 38-byte failing input file...
   --- FAIL: FuzzReverse (0.01s)
       --- FAIL: FuzzReverse (0.00s)
           reverse_test.go:20: Reverse produced invalid UTF-8 string "\x9c\xdd"
```

실패한 입력값이 testdata/fuzz/FuzzReverse/af69258a12129d6cbba438df5d5f25ba0ec050461c116f777e77ea7c9a0d217a 에 기록되었습니다.
       재실행 방법:
       go test -run=FuzzReverse/af69258a12129d6cbba438df5d5f25ba0ec050461c116f777e77ea7c9a0d217a
   FAIL
   exit status 1
   FAIL    example/fuzz  0.030s
   ```

퍼징 도중 실패가 발생했으며, 문제를 일으킨 입력값은 시드 코퍼스(seed corpus) 파일에 기록됩니다. 이 파일은 `-fuzz` 플래그 없이 `go test`를 호출하더라도 다음 실행 시에 함께 실행됩니다. 실패를 유발한 입력값을 확인하려면 `testdata/fuzz/FuzzReverse` 디렉토리에 기록된 코퍼스 파일을 텍스트 에디터로 여십시오. 사용자의 시드 코퍼스 파일에는 다른 문자열이 포함되어 있을 수 있지만, 형식은 동일합니다.

```
   go test fuzz v1
   string("泃")
   ```

코퍼스 파일의 첫 번째 줄은 인코딩 버전을 나타냅니다. 그 다음의 각 줄은 코퍼스 엔트리를 구성하는 각 타입의 값을 나타냅니다. 퍼즈 타겟(fuzz target)은 단 하나의 입력만 받으므로, 버전 뒤에는 하나의 값만 존재합니다.

3. `-fuzz` 플래그 없이 `go test`를 다시 실행하십시오. 그러면 새로 실패한 시드 코퍼스(seed corpus) 항목이 사용됩니다.

```
   $ go test
   --- FAIL: FuzzReverse (0.00s)
       --- FAIL: FuzzReverse/af69258a12129d6cbba438df5d5f25ba0ec050461c116f777e77ea7c9a0d217a (0.00s)
           reverse_test.go:20: Reverse produced invalid string
   FAIL
   exit status 1
   FAIL    example/fuzz  0.016s
   ```

테스트가 실패했으므로, 이제 디버깅을 할 시간입니다.

## invalid string 에러 해결하기 {#fix_invalid_string_error}

이 섹션에서는 실패 원인을 디버깅하고 버그를 수정합니다.

다음 단계로 넘어가기 전에, 시간을 갖고 충분히 생각하며 스스로 이 문제를 해결해 보시기 바랍니다.

### 오류 진단

이 오류를 디버깅하는 몇 가지 방법이 있습니다. 텍스트 에디터로 VS Code를 사용하고 계신다면, [디버거를 설정](https://github.com/golang/vscode-go/blob/master/docs/debugging.md)하여 조사할 수 있습니다.

이 튜토리얼에서는 유용한 디버깅 정보를 터미널에 기록하는 방법을 알아보겠습니다.

먼저, [`utf8.ValidString`](https://pkg.go.dev/unicode/utf8)의 문서를 살펴보십시오.

```
ValidString은 s가 완전히 유효한 UTF-8 인코딩된 룬(runes)으로 구성되어 있는지 여부를 보고합니다.
```

현재의 `Reverse` 함수는 문자열을 바이트 단위로 뒤집으며, 바로 이 점이 문제입니다. 원래 문자열의 UTF-8 인코딩된 룬(rune)들을 보존하려면, 대신 문자열을 룬 단위로 뒤집어야 합니다.

입력값(이 경우 한자 `泃`)이 왜 `Reverse` 함수로 반전시켰을 때 유효하지 않은 문자열을 생성하는지 확인하려면, 반전된 문자열의 rune 개수를 조사해 보면 됩니다.

#### 코드 작성하기

텍스트 에디터에서 `FuzzReverse` 내의 fuzz target을 다음 내용으로 교체하세요.

```
f.Fuzz(func(t *testing.T, orig string) {
    rev := Reverse(orig)
    doubleRev := Reverse(rev)
    t.Logf("Number of runes: orig=%d, rev=%d, doubleRev=%d", utf8.RuneCountInString(orig), utf8.RuneCountInString(rev), utf8.RuneCountInString(doubleRev))
    if orig != doubleRev {
        t.Errorf("Before: %q, after: %q", orig, doubleRev)
    }
    if utf8.ValidString(orig) && !utf8.ValidString(rev) {
        t.Errorf("Reverse produced invalid UTF-8 string %q", rev)
    }
})
```

이 `t.Logf` 라인은 에러가 발생하거나 `-v` 옵션으로 테스트를 실행할 때 커맨드 라인에 출력되며, 이는 해당 문제를 디버깅하는 데 도움이 될 수 있습니다.

#### 코드 실행하기

`go test`를 사용하여 테스트를 실행하세요.

```
$ go test
--- FAIL: FuzzReverse (0.00s)
    --- FAIL: FuzzReverse/28f36ef487f23e6c7a81ebdaa9feffe2f2b02b4cddaa6252e87f69863046a5e0 (0.00s)
        reverse_test.go:16: Number of runes: orig=1, rev=3, doubleRev=1
        reverse_test.go:21: Reverse produced invalid UTF-8 string "\x83\xb3\xe6"
FAIL
exit status 1
FAIL    example/fuzz    0.598s
```

전체 시드 코퍼스(seed corpus)는 모든 문자가 단일 바이트인 문자열을 사용했습니다.
하지만 泃와 같은 문자는 여러 바이트가 필요할 수 있습니다. 따라서,
문자열을 바이트 단위로 뒤집으면 멀티바이트 문자가 손상됩니다.

**참고:** Go가 문자열을 어떻게 처리하는지 궁금하시다면, 더 깊은 이해를 위해 블로그 포스트 [Strings, bytes, runes and characters in Go](/blog/strings)를 읽어보세요.

버그에 대해 더 잘 이해했으므로, `Reverse` 함수의 오류를 수정하십시오.

### 에러 수정하기

`Reverse` 함수를 수정하기 위해, 바이트(bytes) 대신 룬(runes) 단위로 문자열을 순회해 보겠습니다.

#### 코드 작성하기

텍스트 에디터에서 기존의 `Reverse()` 함수를 다음 내용으로 교체하세요.

```
func Reverse(s string) string {
    r := []rune(s)
    for i, j := 0, len(r)-1; i {{raw "<"}} len(r)/2; i, j = i+1, j-1 {
        r[i], r[j] = r[j], r[i]
    }
    return string(r)
}
```

핵심적인 차이점은 `Reverse`가 이제 문자열의 각 `byte`가 아니라 각 `rune`을 순회한다는 점입니다. 이는 단순한 예제일 뿐이며, [결합 문자(combining characters)](https://en.wikipedia.org/wiki/Combining_character)를 올바르게 처리하지 않는다는 점에 유의하세요.

#### 코드 실행하기

1. `go test`를 사용하여 테스트를 실행하십시오.

```
   $ go test
   PASS
   ok      example/fuzz  0.016s
   ```

이제 테스트가 통과되었습니다!

2. `go test -fuzz`로 다시 퍼징(fuzzing)하여 새로운 버그가 있는지 확인합니다.

```
   $ go test -fuzz=Fuzz
   fuzz: elapsed: 0s, gathering baseline coverage: 0/37 completed
   fuzz: minimizing 506-byte failing input file...
   fuzz: elapsed: 0s, gathering baseline coverage: 5/37 completed
   --- FAIL: FuzzReverse (0.02s)
       --- FAIL: FuzzReverse (0.00s)
           reverse_test.go:33: Before: "\x91", after: "�"
```

실패한 입력값이 testdata/fuzz/FuzzReverse/1ffc28f7538e29d79fce69fef20ce5ea72648529a9ca10bea392bcff28cd015c 에 기록되었습니다.
       재실행 방법:
       go test -run=FuzzReverse/1ffc28f7538e29d79fce69fef20ce5ea72648529a9ca10bea392bcff28cd015c
   FAIL
   exit status 1
   FAIL    example/fuzz  0.032s
   ```

두 번 뒤집은 후의 문자열이 원래의 문자열과 다르다는 것을 알 수 있습니다. 이번에는 입력값 자체가 유효하지 않은 유니코드입니다. 문자열로 퍼징(fuzzing)을 하고 있는데 어떻게 이런 일이 가능할까요?

다시 디버깅해 봅시다.

## 이중 리버스 오류 수정 {#fix_double_reverse_error}

이 섹션에서는 double reverse 실패 사례를 디버깅하고 버그를 수정합니다.

다음 단계로 넘어가기 전에, 시간을 갖고 충분히 생각하며 스스로 문제를 해결해 보시기 바랍니다.

### 오류 진단

이전과 마찬가지로, 이 실패를 디버깅하는 방법은 여러 가지가 있습니다. 이 경우에는
[debugger](https://github.com/golang/vscode-go/blob/master/docs/debugging.md)를
사용하는 것이 좋은 접근 방식이 될 것입니다.

이 튜토리얼에서는 `Reverse` 함수에 유용한 디버깅 정보를 기록하는 방법을 알아보겠습니다.

역전된 문자열을 자세히 살펴보고 오류를 찾아보세요. Go에서 [문자열은 읽기 전용 바이트 슬라이스](/blog/strings)이며, 유효하지 않은 UTF-8 바이트를 포함할 수 있습니다. 원본 문자열은 `'\x91'`이라는 하나의 바이트를 가진 바이트 슬라이스입니다. 입력 문자열이 `[]rune`으로 설정되면, Go는 바이트 슬라이스를 UTF-8로 인코딩하고 해당 바이트를 UTF-8 문자 �로 대체합니다. 이 대체된 UTF-8 문자를 입력 바이트 슬라이스와 비교하면, 두 값은 분명히 서로 다릅니다.

#### 코드 작성하기

1. 텍스트 에디터에서 `Reverse` 함수를 다음과 같이 변경하세요.

```
   func Reverse(s string) string {
       fmt.Printf("input: %q\n", s)
       r := []rune(s)
       fmt.Printf("runes: %q\n", r)
       for i, j := 0, len(r)-1; i {{raw "<"}} len(r)/2; i, j = i+1, j-1 {
           r[i], r[j] = r[j], r[i]
       }
       return string(r)
   }
   ```

이 내용은 문자열을 rune 슬라이스로 변환할 때 무엇이 잘못되고 있는지 이해하는 데 도움이 될 것입니다.

#### 코드 실행하기

이번에는 로그를 확인하기 위해 실패한 테스트만 실행하려고 합니다. 이를 위해 `go test -run`을 사용하겠습니다.

`FuzzXxx/testdata` 내의 특정 코퍼스 항목을 실행하려면 `-run` 플래그에 `{FuzzTestName}/{filename}`을 제공하면 됩니다. 이는 디버깅 시 유용할 수 있습니다.
이 경우, `-run` 플래그를 실패한 테스트의 정확한 해시 값과 동일하게 설정하십시오.
터미널에 표시된 고유 해시를 복사하여 붙여넣으십시오.
해당 값은 아래에 표시된 값과 다를 것입니다.

```
$ go test -run=FuzzReverse/28f36ef487f23e6c7a81ebdaa9feffe2f2b02b4cddaa6252e87f69863046a5e0
input: "\x91"
runes: ['�']
input: "�"
runes: ['�']
--- FAIL: FuzzReverse (0.00s)
    --- FAIL: FuzzReverse/28f36ef487f23e6c7a81ebdaa9feffe2f2b02b4cddaa6252e87f69863046a5e0 (0.00s)
        reverse_test.go:16: Number of runes: orig=1, rev=1, doubleRev=1
        reverse_test.go:18: Before: "\x91", after: "�"
FAIL
exit status 1
FAIL    example/fuzz    0.145s
```

입력이 유효하지 않은 유니코드라는 점을 알았으니, `Reverse` 함수의 오류를 수정해 보겠습니다.

### 에러 수정하기

이 문제를 해결하기 위해, `Reverse`의 입력값이 유효한 UTF-8이 아닌 경우 에러를 반환하도록 하겠습니다.

#### 코드 작성하기

1. 텍스트 에디터에서 기존의 `Reverse` 함수를 다음 내용으로 교체하세요.

```
   func Reverse(s string) (string, error) {
       if !utf8.ValidString(s) {
           return s, errors.New("input is not valid UTF-8")
       }
       r := []rune(s)
       for i, j := 0, len(r)-1; i {{raw "<"}} len(r)/2; i, j = i+1, j-1 {
           r[i], r[j] = r[j], r[i]
       }
       return string(r), nil
   }
   ```

이 변경 사항은 입력 문자열에 유효하지 않은 UTF-8 문자가 포함되어 있을 경우 에러를 반환합니다.

1. 이제 Reverse 함수가 error를 반환하므로, `main` 함수를 수정하여 추가된 error 값을 무시하도록 하세요. 기존의 `main` 함수를 다음과 같이 교체하십시오.

```
   func main() {
       input := "The quick brown fox jumped over the lazy dog"
       rev, revErr := Reverse(input)
       doubleRev, doubleRevErr := Reverse(rev)
       fmt.Printf("original: %q\n", input)
       fmt.Printf("reversed: %q, err: %v\n", rev, revErr)
       fmt.Printf("reversed again: %q, err: %v\n", doubleRev, doubleRevErr)
   }
   ```

입력 문자열이 유효한 UTF-8이므로, `Reverse`에 대한 이 호출들은 nil 에러를 반환해야 합니다.

1. `errors` 및 `unicode/utf8` 패키지를 임포트해야 합니다.
   `main.go`의 임포트 문은 다음과 같아야 합니다.

```
   import (
       "errors"
       "fmt"
       "unicode/utf8"
   )
   ```

1. `reverse_test.go` 파일을 수정하여 에러를 확인하고, 에러가 발생하면 반환(returning)을 통해 테스트를 건너뛰도록 하십시오.

```go
   func FuzzReverse(f *testing.F) {
       testcases := []string {"Hello, world", " ", "!12345"}
       for _, tc := range testcases {
           f.Add(tc)  // f.Add를 사용하여 시드 코퍼스(seed corpus)를 제공합니다.
       }
       f.Fuzz(func(t *testing.T, orig string) {
           rev, err1 := Reverse(orig)
           if err1 != nil {
               return
           }
           doubleRev, err2 := Reverse(rev)
           if err2 != nil {
                return
           }
           if orig != doubleRev {
               t.Errorf("Before: %q, after: %q", orig, doubleRev)
           }
           if utf8.ValidString(orig) && !utf8.ValidString(rev) {
               t.Errorf("Reverse produced invalid UTF-8 string %q", rev)
           }
       })
   }
   ```

단순히 반환하는 대신, `t.Skip()`을 호출하여 해당 퍼즈(fuzz) 입력의 실행을 중단할 수도 있습니다.

#### 코드 실행하기

1. `go test`를 사용하여 테스트를 실행하세요.

```
   $ go test
   PASS
   ok      example/fuzz  0.019s
   ```

2. `go test -fuzz=Fuzz`로 퍼징을 수행한 다음, 몇 초가 지나면 `ctrl-C`를 눌러 퍼징을 중단하세요. 퍼즈 테스트는 `-fuzztime` 플래그를 전달하지 않는 한 실패하는 입력을 찾을 때까지 계속 실행됩니다. 기본적으로 실패가 발생하지 않으면 무한히 실행되며, `ctrl-C`로 프로세스를 중단할 수 있습니다.

```
   $ go test -fuzz=Fuzz
   fuzz: elapsed: 0s, gathering baseline coverage: 0/38 completed
   fuzz: elapsed: 0s, gathering baseline coverage: 38/38 completed, now fuzzing with 4 workers
   fuzz: elapsed: 3s, execs: 86342 (28778/sec), new interesting: 2 (total: 35)
   fuzz: elapsed: 6s, execs: 193490 (35714/sec), new interesting: 4 (total: 37)
   fuzz: elapsed: 9s, execs: 304390 (36961/sec), new interesting: 4 (total: 37)
   ...
   fuzz: elapsed: 3m45s, execs: 7246222 (32357/sec), new interesting: 8 (total: 41)
   ^Cfuzz: elapsed: 3m48s, execs: 7335316 (31648/sec), new interesting: 8 (total: 41)
   PASS
   ok      example/fuzz  228.000s
   ```

3. `go test -fuzz=Fuzz -fuzztime 30s` 명령어로 퍼징을 수행합니다. 이 명령은 실패 사례가 발견되지 않을 경우 30초 동안 퍼징을 진행한 후 종료됩니다.

```
   $ go test -fuzz=Fuzz -fuzztime 30s
   fuzz: elapsed: 0s, gathering baseline coverage: 0/5 completed
   fuzz: elapsed: 0s, gathering baseline coverage: 5/5 completed, now fuzzing with 4 workers
   fuzz: elapsed: 3s, execs: 80290 (26763/sec), new interesting: 12 (total: 12)
   fuzz: elapsed: 6s, execs: 210803 (43501/sec), new interesting: 14 (total: 14)
   fuzz: elapsed: 9s, execs: 292882 (27360/sec), new interesting: 14 (total: 14)
   fuzz: elapsed: 12s, execs: 371872 (26329/sec), new interesting: 14 (total: 14)
   fuzz: elapsed: 15s, execs: 517169 (48433/sec), new interesting: 15 (total: 15)
   fuzz: elapsed: 18s, execs: 663276 (48699/sec), new interesting: 15 (total: 15)
   fuzz: elapsed: 21s, execs: 771698 (36143/sec), new interesting: 15 (total: 15)
   fuzz: elapsed: 24s, execs: 924768 (50990/sec), new interesting: 16 (total: 16)
   fuzz: elapsed: 27s, execs: 1082025 (52427/sec), new interesting: 17 (total: 17)
   fuzz: elapsed: 30s, execs: 1172817 (30281/sec), new interesting: 17 (total: 17)
   fuzz: elapsed: 31s, execs: 1172817 (0/sec), new interesting: 17 (total: 17)
   PASS
   ok      example/fuzz  31.025s
   ```

퍼징(Fuzzing) 통과!

`-fuzz` 플래그 외에도 `go test`에 여러 새로운 플래그가 추가되었으며, 이는 [문서](/security/fuzz/#custom-settings)에서 확인할 수 있습니다.

퍼징 출력에 사용되는 용어에 대한 자세한 내용은 [Go Fuzzing](/security/fuzz/#command-line-output)을 참조하세요. 예를 들어, "new interesting"은 기존 퍼즈 테스트 코퍼스의 코드 커버리지를 확장하는 입력을 의미합니다. "new interesting" 입력의 수는 퍼징이 시작될 때 급격히 증가하고, 새로운 코드 경로가 발견됨에 따라 여러 번 급증한 후, 시간이 지남에 따라 점차 감소할 것으로 예상할 수 있습니다.

## 결론 {#conclusion}

잘하셨습니다! 방금 Go의 퍼징(fuzzing)에 입문하셨습니다.

다음 단계는 코드에서 퍼징(fuzz)하고 싶은 함수를 선택하여 시도해 보는 것입니다! 만약 퍼징을 통해 코드의 버그를 발견했다면, [trophy case](/wiki/Fuzzing-trophy-case)에 추가하는 것을 고려해 보세요.

문제가 발생하거나 기능 제안 아이디어가 있다면, [이슈를 등록해 주세요](/issue/new/?&labels=fuzz).

기능에 대한 논의 및 일반적인 피드백을 위해 Gophers Slack의 [#fuzzing 채널](https://gophers.slack.com/archives/CH5KV1AKE)에도 참여하실 수 있습니다.

더 자세한 내용은 [go.dev/security/fuzz](/security/fuzz/#requirements)의 문서를 확인하세요.

## 완성된 코드

--- main.go ---

```go
package main

import (
    "errors"
    "fmt"
    "unicode/utf8"
)

func main() {
    input := "The quick brown fox jumped over the lazy dog"
    rev, revErr := Reverse(input)
    doubleRev, doubleRevErr := Reverse(rev)
    fmt.Printf("original: %q\n", input)
    fmt.Printf("reversed: %q, err: %v\n", rev, revErr)
    fmt.Printf("reversed again: %q, err: %v\n", doubleRev, doubleRevErr)
}

func Reverse(s string) (string, error) {
    if !utf8.ValidString(s) {
        return s, errors.New("input is not valid UTF-8")
    }
    r := []rune(s)
    for i, j := 0, len(r)-1; i < len(r)/2; i, j = i+1, j-1 {
        r[i], r[j] = r[j], r[i]
    }
    return string(r), nil
}
```

--- reverse_test.go ---

```go
package main

import (
    "testing"
    "unicode/utf8"
)

func FuzzReverse(f *testing.F) {
    testcases := []string{"Hello, world", " ", "!12345"}
    for _, tc := range testcases {
        f.Add(tc) // 시드 코퍼스(seed corpus)를 제공하기 위해 f.Add 사용
    }
    f.Fuzz(func(t *testing.T, orig string) {
        rev, err1 := Reverse(orig)
        if err1 != nil {
            return
        }
        doubleRev, err2 := Reverse(rev)
        if err2 != nil {
            return
        }
        if orig != doubleRev {
            t.Errorf("Before: %q, after: %q", orig, doubleRev)
        }
        if utf8.ValidString(orig) && !utf8.ValidString(rev) {
            t.Errorf("Reverse produced invalid UTF-8 string %q", rev)
        }
    })
}
```

[맨 위로](#top)
