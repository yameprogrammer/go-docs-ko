<!--{
  "Title": "튜토리얼: VS Code Go로 취약한 종속성 찾기 및 수정하기",
  "Breadcrumb": true
}-->

[Go 보안으로 돌아가기](/security)

Visual Studio Code용 Go 확장을 사용하면 에디터에서 직접 코드의 취약점을 스캔할 수 있습니다.

참고: 아래 이미지에 포함된 취약점 수정 사항에 대한 설명은 [govulncheck 튜토리얼](/doc/tutorial/govulncheck)을 참조하십시오.

## 사전 요구 사항:

- **Go.** 이 튜토리얼을 따라 하기 위해 최신 버전의 Go를 사용하는 것을 권장합니다. 설치 안내는 [Installing Go](/doc/install)를 참조하세요.
- **VS Code**, 최신 버전으로 업데이트되어 있어야 합니다. [여기에서 다운로드](https://code.visualstudio.com/)하세요. Vim을 사용할 수도 있지만(자세한 내용은 [여기](/security/vuln/editor#editor-specific-instructions) 참조), 이 튜토리얼은 VS Code Go에 중점을 둡니다.
- **VS Code Go extension**, [여기에서 다운로드](https://marketplace.visualstudio.com/items?itemName=golang.go)할 수 있습니다.
- **에디터 전용 설정 변경.** 아래의 결과를 재현하려면 [이 사양](/security/vuln/editor#editor-specific-instructions)에 따라 IDE 설정을 수정해야 합니다.

## VS Code Go를 사용하여 취약점을 스캔하는 방법

**1단계.** "Go: Toggle Vulncheck"를 실행하세요.

[Toggle Vulncheck](https://github.com/golang/vscode-go/wiki/Commands#go-toggle-vulncheck) 명령은 모듈에 나열된 모든 종속성에 대한 취약점 분석 결과를 표시합니다. 이 명령을 사용하려면 IDE에서 [명령 팔레트](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette)(Linux/Windows의 경우 Ctrl+Shift+P, Mac OS의 경우 Cmd+Shift+P)를 열고 “Go: Toggle Vulncheck”를 실행하십시오. 그러면 `go.mod` 파일에서 코드에 직접 또는 간접적으로 사용된 취약한 종속성에 대한 진단 내용을 확인할 수 있습니다.

<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="editor_tutorial_1.png" alt="Run Toggle Vulncheck"></img>
  </center>
</div>

참고: 본 튜토리얼을 본인의 에디터에서 재현하려면, 아래 코드를 `main.go` 파일에 복사하세요.

```go
// 이 프로그램은 커맨드라인 인자로 언어 태그를 받아
// 이를 파싱합니다.

package main

import (
  "fmt"
  "os"

  "golang.org/x/text/language"
)

func main() {
  for _, arg := range os.Args[1:] {
    tag, err := language.Parse(arg)
    if err != nil {
      fmt.Printf("%s: error: %v\n", arg, err)
    } else if tag == language.Und {
      fmt.Printf("%s: undefined\n", arg)
    } else {
      fmt.Printf("%s: tag %s\n", arg, tag)
    }
  }
}
```

그 다음, 프로그램의 해당 `go.mod` 파일이 다음과 같이 되어 있는지 확인하십시오.

```
module module1

go 1.18

require golang.org/x/text v0.3.5
```

이제 `go mod tidy`를 실행하여 `go.sum` 파일이 업데이트되었는지 확인하세요.

**2단계.** 코드 액션을 통해 govulncheck를 실행합니다.

코드 액션을 사용하여 `govulncheck`를 실행하면 코드에서 실제로 호출되는 종속성에 집중할 수 있습니다. VS Code의 코드 액션은 전구 아이콘으로 표시됩니다. 관련 종속성 위에 마우스를 올리면 취약점 정보가 표시되며, 이때 “Quick Fix”를 선택하면 옵션 메뉴가 나타납니다. 이 중에서 “run govulncheck to verify”를 선택하십시오. 그러면 터미널에 관련 `govulncheck` 출력 결과가 표시됩니다.

<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="editor_tutorial_2.png" alt="govulncheck code action"></img>
  </center>
</div>

<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="editor_tutorial_3.png" alt="VS Code Go govulncheck output"></img>
  </center>
</div>

**단계 3**. `go.mod` 파일에 나열된 의존성 위에 마우스를 올리십시오.

특정 의존성에 대한 관련 govulncheck 출력 내용은 `go.mod` 파일에서 해당 의존성 위에 마우스를 올리면 확인할 수 있습니다. 의존성 정보를 빠르게 확인하려는 경우, 이 방법이 코드 액션(code action)을 사용하는 것보다 훨씬 효율적입니다.

<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="editor_tutorial_4.png" alt="Hover over dependency for vulnerability information"></img>
  </center>
</div>

**4단계.** 종속성의 "fixed in" 버전으로 업그레이드하세요.

코드 액션은 취약점이 수정된 버전으로 종속성을 빠르게 업그레이드하는 데에도 사용할 수 있습니다. 코드 액션 드롭다운 메뉴에서 “Upgrade” 옵션을 선택하여 이를 수행하세요.

<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="editor_tutorial_5.png" alt="Upgrade to Latest via code action menu"></img>
  </center>
</div>

## 추가 리소스

- IDE에서의 취약점 스캔에 대한 자세한 내용은 [이 페이지](/security/vuln/editor)를 참조하십시오. 특히 [Notes and Caveats 섹션](/security/vuln/editor#notes-and-caveats)에서는 위 예제보다 취약점 스캔이 더 복잡할 수 있는 특수한 경우들에 대해 다룹니다.
- [Go Vulnerability Database](https://pkg.go.dev/vuln/)는 Go 패키지 유지 관리자가 Go 보안 팀에 직접 보고한 내용 외에도 많은 기존 소스의 정보를 포함하고 있습니다.
- [Go Vulnerability Management](/security/vuln/) 페이지는 취약점을 탐지, 보고 및 관리하기 위한 Go의 아키텍처에 대한 하이레벨 뷰를 제공합니다.
