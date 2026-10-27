<!--{
  "제목": "튜토리얼: VS Code Go를 사용하여 취약한 의존성을 찾고 수정하기",
  "브레드크럼": true
}-->

[Go 보안으로 돌아가기](/security)

Visual Studio Code의 Go 확장 기능을 사용하여, 편집기 내에서 직접 코드를 스캔하여 취약점을 탐지할 수 있습니다.

참고: 아래 이미지에 포함된 취약점 수정에 대한 설명은 [govulncheck 튜토리얼](/doc/tutorial/govulncheck)에서 확인하십시오.

## 필수 조건:

- **Go.** 이 튜토리얼을 따라가기 위해 Go의 최신 버전을 사용하는 것이 좋습니다. 설치 지침은 [Installing Go](/doc/install)를 참조하세요.
- **VS Code**, 최신 버전으로 업데이트되었습니다. [여기에서 다운로드](https://code.visualstudio.com/). 또한 Vim을 사용할 수도 있습니다 (자세한 내용은 [여기](/security/vuln/editor#editor-specific-instructions) 참조). 그러나 이 튜토리얼은 VS Code Go에 초점을 맞추고 있습니다.
- **VS Code Go 확장**, [여기에서 다운로드](https://marketplace.visualstudio.com/items?itemName=golang.go).
- **편집기별 설정 변경.** 아래 결과를 재현하기 전에, [이러한 사양에 따라](/security/vuln/editor#editor-specific-instructions) IDE 설정을 변경해야 합니다.

## VS Code Go를 사용하여 취약점 스캔하는 방법

이 문서에서는 VS Code의 Go 확장을 사용하여 Go 프로젝트에서 취약점을 스캔하는 방법을 설명합니다.

### 1. 필요한 도구 설치

*   **Go:** Go 언어가 설치되어 있어야 합니다.
*   **Go 도구:** `go`, `gopls` 등이 설치되어 있어야 합니다.
*   **(선택 사항) Go 이미지 분석 도구:** Go 이미지 분석 도구를 설치할 수 있습니다. 예를 들어, `go-analyzer`, `staticcheck` 등이 있습니다.

### 2. VS Code 설정

*   **Go 확장을 설치:** VS Code Marketplace에서 "Go" 확장을 설치합니다.
*   **Go 도구 구성:** VS Code 설정에서 Go 도구가 올바르게 구성되었는지 확인합니다. (예: Go 언어 버전, 도구 경로 등)
*   **(선택 사항) Go 이미지 분석 도구 통합:** Go 이미지 분석 도구를 VS Code에 통합합니다. (설치 및 설정 방법은 각 도구의 문서를 참조)

### 3. 코드 스캔

1.  **프로젝트 열기:** VS Code에서 Go 프로젝트를 엽니다.
2.  **터미널 열기:** VS Code 터미널을 엽니다.
3.  **스캔 명령 실행:** 터미널에서 적절한 스캔 명령을 실행합니다. 예를 들어, Go 이미지 분석 도구를 사용하는 경우 다음과 같이 실행합니다.

    ```bash
    go-analyzer ./
    ```

    또는 `staticcheck`를 사용하는 경우:

    ```bash
    staticcheck ./
    ```

4.  **결과 확인:** 스캔 결과가 터미널에 표시됩니다. 결과를 검토하여 취약점을 확인합니다.

### 4. 결과 분석 및 수정

*   **결과 검토:** 스캔 결과에서 발견된 취약점을 주의 깊게 검토합니다.
*   **취약점 수정:** 발견된 취약점을 수정합니다.
*   **재 스캔:** 수정 후, 다시 스캔하여 취약점이 해결되었는지 확인합니다.

### 5. 추가 정보

*   각 Go 이미지 분석 도구의 공식 문서를 참조하여 자세한 사용법 및 설정을 확인하십시오.
*   VS Code Go 확장의 설정 및 사용법에 대한 추가 정보를 얻으려면 공식 문서를 참조하십시오.
*   Go 언어의 보안 모범 사례를 준수하십시오.

**1단계.** "Go: Vulncheck 활성화" 실행

`[Toggle Vulncheck](https://github.com/golang/vscode-go/wiki/Commands#go-toggle-vulncheck)` 명령은 모듈에 나열된 모든 종속성에 대한 취약성 분석을 표시합니다. 이 명령을 사용하려면, IDE (Linux/Windows에서 Ctrl+Shift+P 또는 Mac OS에서 Cmd+Shift+P)에서 [명령 팔레트](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette)를 열고 "Go: Toggle Vulncheck"를 실행합니다. `go.mod` 파일에서는 코드에서 직접 또는 간접적으로 사용되는 취약한 종속성에 대한 진단 정보를 확인할 수 있습니다.

```markdown
<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="editor_tutorial_1.png" alt="Run Toggle Vulncheck">
  </center>
</div>
```

참고: 이 튜토리얼을 자신의 편집기에서 재현하려면 아래 코드를 `main.go` 파일에 복사하십시오.

```
// 이 프로그램은 명령줄 인수로 언어 태그를 받아 파싱합니다.

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
			fmt.Printf("%s: 오류: %v\n", arg, err)
		} else if tag == language.Und {
			fmt.Printf("%s: 정의되지 않음\n", arg)
		} else {
			fmt.Printf("%s: 태그 %s\n", arg, tag)
		}
	}
}
```

다음 Markdown 콘텐츠를 한국어로 번역합니다. Markdown 구조, 제목, 표, 링크, 목록, 인라인 코드, 코드 펜을 유지합니다. Go 패키지 이름, 식별자, URL, 명령, 코드 스니펫은 번역하지 않습니다.

```
모듈 module1

go 1.18

require golang.org/x/text v0.3.5
```

이제 `go mod tidy`를 실행하여 `go.sum` 파일이 업데이트되었는지 확인합니다.

**2단계.** 코드 액션을 통해 govulncheck 실행.

`govulncheck`를 코드 액션으로 실행하면, 실제로 코드에서 호출되는 종속성에 집중할 수 있습니다. VS Code의 코드 액션은 밝은 전구 아이콘으로 표시됩니다. 관련 종속성에 마우스를 올리면 취약점에 대한 정보를 볼 수 있습니다. 그런 다음 "Quick Fix"을 선택하여 옵션 목록을 표시합니다. 이 목록에서 "govulncheck을 실행하여 확인"을 선택하면, 관련 `govulncheck` 출력이 터미널에 표시됩니다.

```markdown
<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="editor_tutorial_2.png" alt="govulncheck 코드 액션">
  </center>
</div>
```

```markdown
<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="editor_tutorial_3.png" alt="VS Code Go govulncheck 출력">
  </center>
</div>
```

**3단계**. `go.mod` 파일에 나열된 종속성에 마우스를 가져갑니다.

관련 `govulncheck` 출력은 또한 `go.mod` 파일에서 해당 종속성을 마우스를 올리면 확인할 수 있습니다. 종속성 정보의 빠른 확인을 위해, 이 옵션은 코드 액션을 사용하는 것보다 훨씬 효율적입니다.

```markdown
<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="editor_tutorial_4.png" alt="의존성에 대한 취약점 정보를 확인하려면 마우스를 올려주세요"></img>
  </center>
</div>
```

**4단계.** 의존성의 "수정된 버전"으로 업그레이드합니다.

코드 액션은 또한 의존성의 취약점이 수정된 버전으로 빠르게 업그레이드하는 데에도 사용할 수 있습니다. 이를 위해 코드 액션 드롭다운 메뉴에서 "업그레이드" 옵션을 선택하십시오.

```markdown
<div class="image">
  <center>
    <img style="width: 100%" width="2110" height="952" src="editor_tutorial_5.png" alt="코드 액션 메뉴를 사용하여 최신 버전으로 업그레이드">
  </center>
</div>
```

## 추가 자료

- 자세한 내용은 [이 페이지](/security/vuln/editor)를 참조하세요. 특히, [참고 사항 및 주의 사항](/security/vuln/editor#notes-and-caveats) 섹션에서는 위 예시보다 더 복잡할 수 있는 특별한 경우에 대한 정보를 다룹니다.
- [Go 취약점 데이터베이스](https://pkg.go.dev/vuln/)에는 Go 패키지 관리자가 직접 Go 보안 팀에 보고하는 것 외에도 다양한 기존 소스의 정보가 포함되어 있습니다.
- [Go 취약점 관리](/security/vuln/) 페이지는 Go의 취약점 탐지, 보고 및 관리를 위한 고수준 아키텍처에 대한 개요를 제공합니다.
