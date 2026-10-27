<!--{
  "템플릿": true,
  "제목": "가이드를 통한 fuzzing 시작",
  "목차 숨기기": true,
  "브레드크럼": true
}-->

이 튜토리얼은 Go에서 퍼징의 기본 사항을 소개합니다. 퍼징은 무작위 데이터를 테스트에 적용하여 취약점이나 오류를 유발하는 입력을 찾는 시도입니다. 퍼징을 통해 찾을 수 있는 취약점의 예로는 SQL 삽입, 버퍼 오버플로우, 서비스 거부 및 교차 사이트 스크립팅 공격 등이 있습니다.

이 튜토리얼에서는 간단한 함수의 퍼즈 테스트를 작성하고, `go` 명령을 실행하고, 코드 내의 문제점을 디버깅하고 수정하는 방법을 안내합니다.

이 튜토리얼의 용어에 대한 도움을 받으려면 [Go 퍼징
용어집](/security/fuzz/#glossary)을 참조하세요.

다음 섹션들을 따라 진행하게 됩니다:

1. [코드용 폴더를 생성합니다.](#create_folder)
2. [테스트 코드를 추가합니다.](#code_to_test)
3. [단위 테스트를 추가합니다.](#unit_test)
4. [퍼즈 테스트를 추가합니다.](#fuzz_test)
5. [두 가지 버그를 수정합니다.](#fix_invalid_string_error)
6. [추가 자료를 탐색합니다.](#conclusion)

**참고:** 다른 튜토리얼은 [Tutorials](/doc/tutorial/index.html) 에서 확인하십시오.

**참고:** 현재 Go fuzzing은 [Go Fuzzing 문서](https://go.dev/security/fuzz/#requirements)에 나열된 일부 기본 유형만 지원하며, 앞으로 더 많은 기본 유형에 대한 지원이 추가될 예정입니다.

## 필수 조건

- **Go.** 이 튜토리얼을 따라하기 위해 최신 버전의 Go를 사용하는 것이 좋습니다.
  설치 지침은 [Installing Go](/doc/install)를 참조하십시오.
- **코드 편집 도구.** 원하는 텍스트 편집기를 사용해도 됩니다.
- **명령 터미널.** Go는 Linux 및 Mac의 모든 터미널, PowerShell 또는 Windows의 cmd에서 잘 작동합니다.
- **퍼징을 지원하는 환경.** Go 퍼징(커버리지 인스트루멘테이션을 사용)은 현재 AMD64 및 ARM64 아키텍처에서만 지원됩니다.

## 코드용 폴더 생성 {#create_folder}

먼저, 코드를 작성할 폴더를 만듭니다.

1. 명령 프롬프트를 열고 홈 디렉토리로 이동합니다.

리눅스 또는 맥에서:

```
   $ cd
```

온 Windows:

```
   C:\> cd %HOMEPATH%
```

이 튜토리얼의 나머지 부분에서는 `$`를 프롬프트로 사용하겠습니다.
   사용하는 명령어는 Windows에서도 작동합니다.

2. 명령 프롬프트에서 코드를 위한 디렉토리를 만들고 이름을 `fuzz`으로 지정합니다.

```
   $ mkdir fuzz
   $ cd fuzz
```

3. 코드를 담을 모듈을 만듭니다.

`go mod init` 명령을 실행하고, 새 코드의 모듈 경로를 지정합니다.

```
   $ go mod init example/fuzz
   go: 생성 중: 새 go.mod 파일: module example/fuzz
   ```

**참고:** 실제 사용 시에는 특정 요구 사항에 맞는 더 구체적인 모듈 경로를 지정해야 합니다. 자세한 내용은 [의존성 관리](/doc/modules/managing-dependencies)를 참조하십시오.

다음으로, 문자열을 뒤집는 간단한 코드를 추가하겠습니다. 이를 나중에 퍼징(fuzzing)에 사용하겠습니다.

## 테스트 코드를 추가합니다 {#code_to_test}

이 단계에서는 문자열을 뒤집는 함수를 추가합니다.

### 코드를 작성하세요

1.  텍스트 편집기를 사용하여 fuzz 디렉토리에 "main.go"라는 파일을 만듭니다.
2.  main.go 파일의 맨 위에 다음 패키지 선언을 복사하여 붙여넣습니다.

```
    package main
```

독립 실행형 프로그램 (라이브러리가 아닌 경우)은 항상 `main` 패키지에 있습니다.

3. 패키지 선언 아래에 다음 함수 선언을 붙여넣으세요.

```
    func Reverse(s string) string {
        b := []byte(s)
        for i, j := 0, len(b)-1; i < j; i, j = i+1, j-1 {
            b[i], b[j] = b[j], b[i]
        }
        return string(b)
    }
```

이 함수는 `string`을 받아, 바이트 단위로 순회하고, 마지막에 뒤집힌 문자열을 반환합니다.

_참고:_ 이 코드는 `stringutil.Reverse` 함수를 golang.org/x/example에서 기반으로 사용합니다.

4. `main.go` 파일의 맨 위에, 패키지 선언 아래에 다음 `main` 함수를 붙여넣습니다. 이 함수는 문자열을 초기화하고, 반전시키고, 결과를 출력하고, 이 과정을 반복합니다.

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

이 함수는 몇 가지 `Reverse` 연산을 실행한 다음, 결과를 명령줄에 출력합니다. 이는 코드가 실제로 작동하는 것을 보는 데 도움이 될 수 있으며, 잠재적으로 디버깅에도 유용합니다.

5. `main` 함수는 `fmt` 패키지를 사용하므로, 이를 가져와야 합니다.

```go
package main

import "fmt"

func main() {
  fmt.Println("Hello, world!")
}
```

```
    패키지 main
```

```
import "fmt"
```

### 코드를 실행합니다

명령줄에서 main.go 파일이 있는 디렉토리에서 코드를 실행합니다.

```
$ go run .
원래: "The quick brown fox jumped over the lazy dog"
반전: "god yzal eht revo depmuj xof nworb kciuq ehT"
다시 반전: "The quick brown fox jumped over the lazy dog"
```

원래 문자열, 이를 뒤집은 결과, 그리고 다시 뒤집은 결과(이는 원래 문자열과 동일)를 확인할 수 있습니다.

이제 코드가 실행되고 있으므로, 테스트할 때입니다.

## 유닛 테스트 추가하기 {#unit_test}

이 단계에서는 `Reverse` 함수에 대한 기본적인 유닛 테스트를 작성합니다.

### 코드를 작성하세요

1. 텍스트 편집기를 사용하여 `reverse_test.go`라는 파일을 `fuzz` 디렉토리에 만듭니다.
2. 다음 코드를 `reverse_test.go` 파일에 붙여넣습니다.

```
   package main
```

```
import (
    "testing"
)
```

```markdown
```go
import (
	"testing"
)

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

이 간단한 테스트는 나열된 입력 문자열이 올바르게 반전되었는지 확인합니다.

### 코드를 실행하세요

단위 테스트를 `go test` 명령어로 실행합니다.

```
$ go test
PASS
ok      example/fuzz  0.013s
```

다음으로, 유닛 테스트를 퍼즈 테스트로 변경합니다.

## 래터럴 테스트 추가하기 {#fuzz_test}

단위 테스트는 한계가 있습니다. 즉, 각 입력은 개발자가 테스트에 추가해야 합니다. 퍼징의 장점은 코드를 위한 입력을 생성한다는 것입니다. 또한, 개발자가 직접 만든 테스트 케이스에서 다루지 못했던 예외적인 경우를 식별할 수 있습니다.

이 섹션에서는 유닛 테스트를 퍼즈 테스트로 변환하여 더 많은 입력을 더 적은 노력으로 생성할 수 있도록 합니다!

참고: 유닛 테스트, 벤치마크, 퍼즈 테스트를 동일한
*_test.go 파일에 유지할 수 있지만, 이 예제에서는 유닛 테스트를 퍼즈 테스트로 변환합니다.

### 코드를 작성하세요

```markdown
저 편집기에서 `reverse_test.go` 파일의 유닛 테스트를 다음 내용으로 대체하십시오.

```go
// fuzz test
func Fuzz() {
	// Your fuzzing logic here
	// Example:
	// for w := []; w < 10; w++ {
	// 	f.FuzzInt("w", w)
	// }
}
```

```
func FuzzReverse(f *testing.F) {
    testcases := []string{"Hello, world", " ", "!12345"}
    for _, tc := range testcases {
        f.Add(tc)  // f.Add를 사용하여 시드 코퍼스 제공
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

퍼징에는 몇 가지 제한 사항도 있습니다. 단위 테스트에서, `Reverse` 함수의 예상 출력을 예측하고, 실제 출력이 이러한 기대치를 충족하는지 확인할 수 있습니다.

예를 들어, `Reverse("Hello, world")` 테스트 케이스에서 유닛 테스트는 반환 값을 `"dlrow ,olleH"`로 지정합니다.

퍼징을 수행할 때, 입력에 대한 제어가 없기 때문에 예상되는 출력을 예측할 수 없습니다.

그러나, `Reverse` 함수의 몇 가지 속성을 퍼즈 테스트를 통해 확인할 수 있습니다. 이 퍼즈 테스트에서 검사되는 두 가지 속성은 다음과 같습니다:

1. 문자열을 두 번 뒤집는 것은 원래 값을 유지합니다.
2. 뒤집힌 문자열은 유효한 UTF-8 문자열로 상태를 유지합니다.

다음은 유닛 테스트와 퍼즈 테스트 간의 구문 차이점을 참고하십시오:

- 이 함수는 `TestXxx` 대신 `FuzzXxx`로 시작하며, `*testing.T` 대신 `*testing.F`를 사용합니다.
- `t.Run` 실행을 예상하는 위치 대신 `f.Fuzz`이 사용되며, 이 함수는 `*testing.T`를 매개변수로 사용하고, fuzzed할 타입을 입력으로 받습니다. 유닛 테스트에서 제공하는 입력은 `f.Add`를 사용하여 시드 코퍼스 입력으로 제공됩니다.

`unicode/utf8` 패키지를 가져오십시오.

```
패키지 main

import (
    "testing"
    "unicode/utf8"
)
```

단위 테스트를 퍼즈 테스트로 변경했으므로, 이제 테스트를 다시 실행하는 것이 좋습니다.

### 코드를 실행하세요

1.  퍼징 테스트를 실행하여, 시드 입력이 정상적으로 통과하는지 확인합니다.

```
   $ go 테스트
   성공
   ok      example/fuzz  0.013s
   ```

또한, 해당 파일에 다른 테스트가 있는 경우 `go test -run=FuzzReverse`를 실행하여 래버스 테스트만 실행할 수 있습니다.

2. `FuzzReverse`를 사용하여 퍼징을 실행하고, 임의로 생성된 문자열 입력을 통해 오류가 발생하는지 확인합니다. 이는 `go test` 명령을 사용하여, 새로운 플래그 `-fuzz`을 `Fuzz` 매개변수로 설정하여 실행합니다. 아래 명령어를 복사하십시오.

```
    $ go 테스트 -fuzz=Fuzz
    ```

또 다른 유용한 플래그는 `-fuzztime`으로, 퓨징 시간을 제한합니다.
예를 들어, 아래 테스트에서 `-fuzztime 10s`를 지정하면,
초기 오류가 발생하지 않는 한, 테스트는 기본적으로 10초가 경과된 후 종료됩니다. `cmd/go` 문서의 [이 섹션](https://pkg.go.dev/cmd/go#hdr-Testing_flags)을 참조하여 다른 테스트 플래그를 확인하십시오.

이제, 바로 복사한 명령을 실행하세요.

```
   $ go test -fuzz=Fuzz
   fuzz: 소요 시간: 0초, 기본 커버리지 수집: 0/3 완료
   fuzz: 소요 시간: 0초, 기본 커버리지 수집: 3/3 완료, 이제 8개의 작업자를 사용하여 덤핑 시작
   fuzz: 38바이트의 실패한 입력 파일 최소화 중...
   --- FAIL: FuzzReverse (0.01초)
       --- FAIL: FuzzReverse (0.00초)
           reverse_test.go:20: Reverse에서 유효하지 않은 UTF-8 문자열 "\x9c\xdd" 생성
```

실패한 입력이 testdata/fuzz/FuzzReverse/af69258a12129d6cbba438df5d5f25ba0ec050461c116f777e77ea7c9a0d217a에 기록되었습니다.
재실행하려면:
go test -run=FuzzReverse/af69258a12129d6cbba438df5d5f25ba0ec050461c116f777e77ea7c9a0d217a
실패
종료 상태 1
실패 example/fuzz 0.030s
```

오류가 핑거 테스트 중에 발생했으며, 문제를 일으킨 입력은
   다음 `go test` 실행 시에 자동으로 실행되는 시드 코퍼스 파일에 기록됩니다.
   `-fuzz` 플래그 없이도 이를 수행합니다.
   실패를 일으킨 입력을 확인하려면, 텍스트 편집기를 사용하여 testdata/fuzz/FuzzReverse
   디렉토리에 작성된 코퍼스 파일을 엽니다.
   당신의 시드 코퍼스 파일에는 다른 문자열이 포함될 수 있지만, 형식이 동일합니다.

```
   go 테스트 fuzz v1
   string("泃")
   ```

첫 번째 줄은 코퍼스 파일의 인코딩 버전을 나타냅니다.
   이후의 각 줄은 코퍼스 항목을 구성하는 각 유형의 값을 나타냅니다.
   왜냐하면 fuzz 타겟은 1개의 입력만 받기 때문에, 버전 다음에 1개의 값만 존재하기 때문입니다.

3. `go test` 명령어를 다시 실행하여 `-fuzz` 플래그를 제거합니다; 새로운 실패하는 시드 코퍼스 항목이 사용됩니다:

```
   $ go test
   --- 실패: FuzzReverse (0.00s)
       --- 실패: FuzzReverse/af69258a12129d6cbba438df5d5f25ba0ec050461c116f777e77ea7c9a0d217a (0.00s)
           reverse_test.go:20: Reverse가 유효하지 않은 문자열을 생성했습니다
   실패
   종료 상태 1
   실패    example/fuzz  0.016s
   ```

테스트가 실패했으므로, 디버깅할 때가 왔습니다.

## 유효하지 않은 문자열 오류 수정 {#fix_invalid_string_error}

이 섹션에서는 문제의 원인을 파악하고 버그를 수정합니다.

문제를 해결하기 위해 스스로 시간을 들여 생각하고 시도해 보세요.

### 오류 진단

이 오류를 디버깅하는 몇 가지 다른 방법이 있습니다. VS
Code를 텍스트 편집기로 사용하고 있다면, [디버거를 설정](https://github.com/golang/vscode-go/blob/master/docs/debugging.md)하여 조사할 수 있습니다.

이 튜토리얼에서는 유용한 디버깅 정보를 터미널에 기록하는 방법을 안내합니다.

먼저, 다음 문서를 참조하십시오:
[`utf8.ValidString`](https://pkg.go.dev/unicode/utf8).

`ValidString`은 `s`가 유효한 UTF-8 인코딩된 문자로만 구성되어 있는지 여부를 보고합니다.

현재 `Reverse` 함수는 문자열을 바이트 단위로 반전시키므로, 이 부분이 문제입니다. 원본 문자열의 UTF-8 인코딩된 문자를 보존하려면, 문자열을 문자 단위로 반전시켜야 합니다.

입력 (이 경우 중국어 문자 `泃`)이 `Reverse`가 역순으로 뒤집을 때 유효하지 않은 문자열을 생성하는 이유를 분석하려면, 역순 문자열의 문자 수를 확인하십시오.

```markdown
#### 코드를 작성하세요

본 텍스트 편집기에서 `FuzzReverse` 내의 퓨즈 타겟을 다음으로 변경하십시오.

f.Fuzz(func(t *testing.T, orig string) {
    rev := Reverse(orig)
    doubleRev := Reverse(rev)
    t.Logf("문자 수: orig=%d, rev=%d, doubleRev=%d", utf8.RuneCountInString(orig), utf8.RuneCountInString(rev), utf8.RuneCountInString(doubleRev))
    if orig != doubleRev {
        t.Errorf("이전: %q, 이후: %q", orig, doubleRev)
    }
    if utf8.ValidString(orig) && !utf8.ValidString(rev) {
        t.Errorf("Reverse는 유효하지 않은 UTF-8 문자열 %q를 생성했습니다", rev)
    }
})
```

이 `t.Logf` 줄은 오류가 발생하거나, 테스트를 `-v` 옵션으로 실행하면 명령줄에 출력됩니다. 이는 특정 문제를 디버깅하는 데 도움이 될 수 있습니다.

#### 코드를 실행합니다

테스트를 실행합니다.

```
$ go test
--- 실패: FuzzReverse (0.00초)
    --- 실패: FuzzReverse/28f36ef487f23e6c7a81ebdaa9feffe2f2b02b4cddaa6252e87f69863046a5e0 (0.00초)
        reverse_test.go:16: 문자 수: orig=1, rev=3, doubleRev=1
        reverse_test.go:21: 역순으로 변환된 UTF-8 문자열 "\x83\xb3\xe6"가 유효하지 않음
실패
종료 상태 1
실패    example/fuzz    0.598s
```

전체 시드 코퍼스에 사용된 문자열은 모든 문자가 단일 바이트를 사용했습니다.
그러나, 泃과 같은 문자는 여러 바이트를 필요로 합니다. 따라서, 문자열을 바이트 단위로 뒤집으면 다중 바이트 문자를 유효하지하게 만들 수 있습니다.

**참고:** Go에서 문자열을 다루는 방법에 대해 더 자세히 알고 싶다면, 다음 블로그 게시물을 참조하세요:
[Go에서 문자열, 바이트, 런, 문자](/blog/strings)

버그에 대한 더 나은 이해를 바탕으로, `Reverse` 함수에 있는 오류를 수정합니다.

### 오류 수정

`Reverse` 함수를 수정하려면, 바이트 단위가 아닌 문자를 기준으로 문자열을 순회하도록 합니다.

```markdown
#### 코드를 작성하세요
```

본 텍스트 편집기에서 기존의 `Reverse()` 함수를 다음과 같이 대체합니다.

```
func Reverse(s string) string {
    r := []rune(s)
    for i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
        r[i], r[j] = r[j], r[i]
    }
    return string(r)
}
```

핵심적인 차이점은 `Reverse`가 이제 문자열의 각 `rune`를 순회하는 것입니다. 이전에는 각 `byte`를 순회했습니다. 참고로, 이것은 단지 예시일 뿐이며, [병합 문자](https://en.wikipedia.org/wiki/Combining_character)를 올바르게 처리하지 않습니다.

#### 코드를 실행합니다

1. `go test` 명령어를 사용하여 테스트를 실행합니다.

```
   $ go 테스트
   PASS
   ok      example/fuzz  0.016s
   ```

테스트가 이제 성공적으로 통과되었습니다!

2. `go test -fuzz`를 사용하여 다시 퍼징하고, 새로운 버그가 있는지 확인합니다.

$ go test -fuzz=Fuzz
   fuzz: 소요 시간: 0초, 기본 커버리지 수집: 0/37 완료
   fuzz: 실패하는 506바이트 입력 파일 최소화 중...
   fuzz: 소요 시간: 0초, 기본 커버리지 수집: 5/37 완료
   --- 실패: FuzzReverse (0.02초)
       --- 실패: FuzzReverse (0.00초)
           reverse_test.go:33: 이전: "\x91", 이후: "�"

실패한 입력이 testdata/fuzz/FuzzReverse/1ffc28f7538e29d79fce69fef20ce5ea72648529a9ca10bea392bcff28cd015c에 기록됨
       다시 실행하려면:
       go test -run=FuzzReverse/1ffc28f7538e29d79fce69fef20ce5ea72648529a9ca10bea392bcff28cd015c
   실패
   종료 상태 1
   실패    example/fuzz 0.032s
   ```

우리는 문자열이 원래 문자열과 다르게 반전된 것을 확인할 수 있습니다. 이번에는 입력 문자열 자체가 유효하지 않은 유니코드입니다. 만약 문자열을 사용하여 퍼징을 수행한다면, 이것은 어떻게 가능한가?

다시 디버깅해 봅시다.

## 중복 반전 오류 수정 {#fix_double_reverse_error}

이 섹션에서는 "더블 리버스" 오류를 디버깅하고 버그를 수정하는 방법을 안내합니다.

시간을 내어 문제를 직접 해결해 보는 것을 권장합니다.

### 오류 진단

과거와 마찬가지로, 이 오류를 디버그하는 방법은 여러 가지가 있습니다. 이 경우에는
[디버거](https://github.com/golang/vscode-go/blob/master/docs/debugging.md)를 사용하는 것이 좋은 방법입니다.

이 튜토리얼에서는 `Reverse` 함수 내에서 유용한 디버깅 정보를 기록하는 방법을 설명합니다.

반전된 문자열을 주의 깊게 살펴보면 오류를 찾을 수 있습니다. Go에서 [문자열은 읽기 전용 바이트 슬라이스](https://blog/strings)이며, 유효하지 않은 UTF-8 바이트를 포함할 수 있습니다. 원래 문자열은 바이트 슬라이스 하나를 가지고 있으며, `'\x91'`입니다. 입력 문자열을 `[]rune`로 설정하면 Go는 바이트 슬라이스를 UTF-8로 인코딩하고, 바이트를 UTF-8 문자로 대체합니다. 대체된 UTF-8 문자를 입력 바이트 슬라이스와 비교하면, 명확하게 같지 않습니다.

```markdown
#### 코드를 작성하세요

1. 텍스트 편집기에서 `Reverse` 함수를 다음 내용으로 대체합니다.

```
   func Reverse(s string) string {
       fmt.Printf("입력: %q\n", s)
       r := []rune(s)
       fmt.Printf("문자 슬라이스: %q\n", r)
       for i, j := 0, len(r)-1; i < len(r)/2; i, j = i+1, j-1 {
           r[i], r[j] = r[j], r[i]
       }
       return string(r)
   }
```

이렇게 하면 문자열을 런(rune) 슬라이스로 변환할 때 어떤 문제가 발생하는지 이해하는 데 도움이 됩니다.

#### 코드를 실행합니다

이번에는 단순히 실패한 테스트만 실행하여 로그를 검사하기 위해 `go test -run` 명령어를 사용하겠습니다.

특정 코퍼스 항목을 FuzzXxx/testdata 내에서 실행하려면, `-run`에 `{FuzzTestName}/{filename}`을 제공할 수 있습니다. 이는 디버깅에 유용합니다.
이 경우, `-run` 플래그를 실패한 테스트의 정확한 해시 값으로 설정합니다.
터미널에서 고유한 해시 값을 복사하여 붙여넣으세요; 이는 아래의 것과 다릅니다.

$ go test -run=FuzzReverse/28f36ef487f23e6c7a81ebdaa9feffe2f2b02b4cddaa6252e87f69863046a5e0
입력: "\x91"
문자: ['�']
입력: "�"
문자: ['�']
--- 실패: FuzzReverse (0.00s)
    --- 실패: FuzzReverse/28f36ef487f23e6c7a81ebdaa9feffe2f2b02b4cddaa6252e87f69863046a5e0 (0.00s)
        reverse_test.go:16: 문자 개수: orig=1, rev=1, doubleRev=1
        reverse_test.go:18: 이전: "\x91", 이후: "�"
실패
종료 상태 1
실패    example/fuzz    0.145s
```

입력이 유효한 유니코드가 아니라는 것을 인지하고, `Reverse` 함수의 오류를 수정해 보겠습니다.

### 오류 수정

이 문제를 해결하려면, 입력이 유효한 UTF-8 형식이 아닌 경우 오류를 반환하도록 하겠습니다.

```markdown
#### 코드를 작성하세요

1. 텍스트 편집기에서 기존의 `Reverse` 함수를 다음 내용으로 교체합니다.

```
   함수 Reverse(s string) (string, error) {
       if !utf8.ValidString(s) {
           return s, errors.New("입력은 유효한 UTF-8 문자열이 아닙니다")
       }
       r := []rune(s)
       for i, j := 0, len(r)-1; i < len(r)/2; i, j = i+1, j-1 {
           r[i], r[j] = r[j], r[i]
       }
       return string(r), nil
   }
```

이 변경 사항은 입력 문자열에 유효하지 않은 UTF-8 문자가 포함된 경우 오류를 반환합니다.

1. `Reverse` 함수가 이제 오류를 반환하므로, `main` 함수를 수정하여 불필요한 오류 값을 버립니다. 기존 `main` 함수를 다음과 같이 대체합니다.

```
   func main() {
       input := "The quick brown fox jumped over the lazy dog"
       rev, revErr := Reverse(input)
       doubleRev, doubleRevErr := Reverse(rev)
       fmt.Printf("원래 문자열: %q\n", input)
       fmt.Printf("뒤집은 문자열: %q, 오류: %v\n", rev, revErr)
       fmt.Printf("다시 뒤집은 문자열: %q, 오류: %v\n", doubleRev, doubleRevErr)
   }
```

이 `Reverse` 호출은 유효한 UTF-8 문자열이므로 오류를 반환하지 않아야 합니다.

1. `errors` 및 `unicode/utf8` 패키지를 가져와야 합니다.
   `main.go` 파일의 import 문은 다음과 같아야 합니다.

```
   import (
       "errors"
       "fmt"
       "unicode/utf8"
   )
```

1. `reverse_test.go` 파일을 수정하여 오류를 검사하고, 오류가 발생하면 테스트를 건너뛰도록 합니다.

```
   func FuzzReverse(f *testing.F) {
       testcases := []string {"Hello, world", " ", "!12345"}
       for _, tc := range testcases {
           f.Add(tc)  // f.Add를 사용하여 시드 코퍼스 제공
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

대신, `t.Skip()`를 호출하여 해당 퓨즈 입력을 중지할 수 있습니다.

#### 코드를 실행합니다

1. `go test` 명령어를 사용하여 테스트 실행

```
   $ go 테스트
   성공
   ok      example/fuzz  0.019s
   ```

2.  `go test -fuzz=Fuzz`를 사용하여 퍼징을 실행하고, 몇 초가 지난 후에는 `ctrl-C`를 눌러 퍼징을 중지합니다. 퍼징 테스트는 실패하는 입력을 찾을 때까지 계속 실행됩니다(단, `-fuzztime` 플래그를 지정하지 않는 경우). 오류가 발생하지 않으면 기본적으로 무한정 실행되며, `ctrl-C`를 사용하여 프로세스를 중단할 수 있습니다.

$ go test -fuzz=Fuzz
   fuzz: 소요 시간: 0초, 기본 커버리지 수집: 0/38 완료
   fuzz: 소요 시간: 0초, 기본 커버리지 수집: 38/38 완료, 이제 4개의 작업자를 사용하여 퍼징
   fuzz: 소요 시간: 3초, 실행 횟수: 86342 (28778/초), 새로운 흥미로운 항목: 2 (총: 35)
   fuzz: 소요 시간: 6초, 실행 횟수: 193490 (35714/초), 새로운 흥미로운 항목: 4 (총: 37)
   fuzz: 소요 시간: 9초, 실행 횟수: 304390 (36961/초), 새로운 흥미로운 항목: 4 (총: 37)
   ...
   fuzz: 소요 시간: 3분 45초, 실행 횟수: 7246222 (32357/초), 새로운 흥미로운 항목: 8 (총: 41)
   ^Cfuzz: 소요 시간: 3분 48초, 실행 횟수: 7335316 (31648/초), 새로운 흥미로운 항목: 8 (총: 41)
   PASS
   ok      example/fuzz  228.000s
   ```

3. `go test -fuzz=Fuzz -fuzztime 30s`를 사용하여 30초 동안 묘사 테스트를 수행합니다. 오류가 발견되지 않으면 종료합니다.

```
   $ go test -fuzz=Fuzz -fuzztime 30s
   fuzz: 소요 시간: 0초, 기본 커버리지 수집: 0/5 완료
   fuzz: 소요 시간: 0초, 기본 커버리지 수집: 5/5 완료, 이제 4개의 워커로 퍼징 시작
   fuzz: 소요 시간: 3초, 실행 횟수: 80290 (26763/초), 새로운 흥미로운 항목: 12 (총: 12)
   fuzz: 소요 시간: 6초, 실행 횟수: 210803 (43501/초), 새로운 흥미로운 항목: 14 (총: 14)
   fuzz: 소요 시간: 9초, 실행 횟수: 292882 (27360/초), 새로운 흥미로운 항목: 14 (총: 14)
   fuzz: 소요 시간: 12초, 실행 횟수: 371872 (26329/초), 새로운 흥미로운 항목: 14 (총: 14)
   fuzz: 소요 시간: 15초, 실행 횟수: 517169 (48433/초), 새로운 흥미로운 항목: 15 (총: 15)
   fuzz: 소요 시간: 18초, 실행 횟수: 663276 (48699/초), 새로운 흥미로운 항목: 15 (총: 15)
   fuzz: 소요 시간: 21초, 실행 횟수: 771698 (36143/초), 새로운 흥미로운 항목: 15 (총: 15)
   fuzz: 소요 시간: 24초, 실행 횟수: 924768 (50990/초), 새로운 흥미로운 항목: 16 (총: 16)
   fuzz: 소요 시간: 27초, 실행 횟수: 1082025 (52427/초), 새로운 흥미로운 항목: 17 (총: 17)
   fuzz: 소요 시간: 30초, 실행 횟수: 1172817 (30281/초), 새로운 흥미로운 항목: 17 (총: 17)
   fuzz: 소요 시간: 31초, 실행 횟수: 1172817 (0/초), 새로운 흥미로운 항목: 17 (총: 17)
   PASS
   ok      example/fuzz  31.025초
   ```

테스팅 성공!

또한 `-fuzz` 플래그 외에도 `go test`에 여러 새로운 플래그가 추가되었으며, 자세한 내용은 [문서](https://example.com/security/fuzz/#custom-settings)에서 확인할 수 있습니다.

자세한 내용은 [Go 퍼징](/security/fuzz/#command-line-output)을 참조하세요.
   퍼징 결과에서 사용되는 용어에 대한 추가 정보를 제공합니다. 예를 들어, "new interesting"는 기존 퍼징 테스트 코버리지 범위를 확장하는 입력에 해당합니다. "new interesting" 입력의 수는 퍼징이 시작될 때 급격하게 증가하여, 새로운 코드 경로가 발견될 때마다 몇 번의 급등을 보이다가 시간이 지남에 따라 감소할 것으로 예상됩니다.

## 결론 {#conclusion}

훌륭합니다! 이제 Go에서 퍼징(fuzzing)을 시작하게 되었습니다.

다음 단계는 코드를 분석하기 위해 원하는 함수를 선택하고 실행하는 것입니다! 만약 fuzzing이 코드의 버그를 찾으면, 이를 [트로피 케이스](/wiki/Fuzzing-trophy-case)에 추가하는 것을 고려해 보세요.

만약 문제가 발생하거나 새로운 기능을 제안하고 싶다면, [문제 제기](/issue/new/?&labels=fuzz)를 이용해주세요.

기능에 대한 토론 및 일반적인 피드백을 제공하려면, [#fuzzing 채널](https://gophers.slack.com/archives/CH5KV1AKE)에서 Gophers Slack에 참여할 수 있습니다.

자세한 내용은 [go.dev/security/fuzz](/security/fuzz/#requirements) 에서 확인하십시오.

## 완성된 코드

--- main.go ---

```markdown
패키지 main

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
    for i, j := 0, len(r)-1; i {{raw "<"}} len(r)/2; i, j = i+1, j-1 {
        r[i], r[j] = r[j], r[i]
    }
    return string(r), nil
}
```

```
--- reverse_test.go ---
```

```go
package main

import "testing"

func TestReverse(t *testing.T) {
	// Test cases
	testCases := []struct {
		name     string
		input    string
		expected string
	}{
		{"Empty string", "", ""},
		{"Single character", "a", "a"},
		{"Simple string", "hello", "olleh"},
		{"Palindrome", "madam", "madam"},
		{"Long string", "This is a longer string", "gnirts regnol a si sihT"},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			result := Reverse(tc.input)
			if result != tc.expected {
				t.Errorf("For input '%s', expected '%s', but got '%s'", tc.input, tc.expected, result)
			}
		})
	}
}
```

```
package main

import (
    "testing"
    "unicode/utf8"
)

func FuzzReverse(f *testing.F) {
    testcases := []string{"Hello, world", " ", "!12345"}
    for _, tc := range testcases {
        f.Add(tc) // f.Add를 사용하여 시드 코퍼스 제공
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
            t.Errorf("이전: %q, 이후: %q", orig, doubleRev)
        }
        if utf8.ValidString(orig) && !utf8.ValidString(rev) {
            t.Errorf("Reverse 함수에서 유효하지 않은 UTF-8 문자열 %q 생성", rev)
        }
    })
}
```

[맨 위로 이동](#top)
