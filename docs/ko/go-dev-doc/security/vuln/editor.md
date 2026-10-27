[Go 보안으로 돌아가기](/security)

편집기는 [Go 언어 서버](https://pkg.go.dev/golang.org/x/tools/cmd/gopls)와 함께 통합될 수 있으며, 예를 들어 [VS Code에 Go 확장](https://marketplace.visualstudio.com/items?itemName=golang.go)을 사용하는 경우, 사용자의 종속성에 있는 취약점을 감지할 수 있습니다.

의존성에서 취약점을 감지하는 데는 두 가지 모드가 있습니다. 두 가지 모두 [Go 취약점 데이터베이스](https://vuln.go.dev)를 기반으로 하며 서로 보완적인 역할을 합니다.

* 가져온 패키지 기반 분석: 이 모드에서는 편집기가 워크스페이스에서 가져온 패키지의 집합을 스캔하여 취약점을 보고하고, `go.mod` 파일에서 진단 결과로 표시합니다. 이 방식은 빠르지만, 코드에서 취약한 심볼을 포함하는 패키지를 가져오지만, 취약한 함수가 접근 불가능한 경우 오탐을 발생시킬 수 있습니다. 이 모드는 [`"vulncheck": "Imports"`](https://github.com/golang/tools/blob/master/gopls/doc/settings.md#vulncheck-enum) gopls 설정을 통해 활성화할 수 있습니다.
* `Govulncheck` 분석: 이 분석은 `gopls`에 내장된 [`govulncheck`](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck) 명령줄 도구를 기반으로 합니다. 이는 코드에서 실제로 취약한 함수를 호출하는지 확인하는 안정적이고 낮은 노이즈 방식으로 작동합니다. 왜냐하면 이 분석은 계산 비용이 많이 들기 때문에, 가져온 패키지 기반 분석에서 생성된 진단 결과와 관련된 "Run govulncheck to verify" 코드 액션을 사용하여 수동으로 트리거하거나, `go.mod` 파일에서 [`"codelenses.run_govulncheck"`](https://github.com/golang/tools/blob/master/gopls/doc/settings.md#run-govulncheck) 코드 렌스를 사용하여 트리거해야 합니다.

```markdown
<div style="text-align: center;">
<img src="vscode.gif" alt="Vulncheck">
```

```markdown
<div style="text-align: center;">
<img src="vscode.gif" alt="Vulncheck">
```

<em>Go: Vulncheck 기능 켜기/끄기</em> <a
href="https://user-images.githubusercontent.com/4999471/206977512-a821107d-9ffb-4456-9b27-6a6a4f900ba6.mp4">(vulncheck.mp4)</a>
</div>

이 기능은 `gopls` v0.11.0 또는 그 이상 버전에 사용 가능합니다. 피드백을 [go.dev/s/vsc-vulncheck-feedback](/s/vsc-vulncheck-feedback)에서 공유해 주세요.

## 편집기별 지침

### VS Code

[Go 확장 프로그램](https://marketplace.visualstudio.com/items?itemName=golang.go)은 gopls와의 통합을 제공합니다. 다음 설정이 취약점 스캔 기능을 활성화하는 데 필요합니다:

```
"go.diagnostic.vulncheck": "자동으로 가져오기 활성화", // 기본적으로 가져오기 기반 분석을 활성화합니다.
"gopls": {
  "ui.codelenses": {
    "run_govulncheck": true  // go.mod 파일에서 "govulncheck 실행" 코드 렌스를 사용합니다.
  }
}
```

명령 ["Go Toggle Vulncheck"](https://github.com/golang/vscode-go/wiki/Commands#go-toggle-vulncheck)을 사용하여 현재 워크스페이스에 대한 imports 기반 분석을 켜고 끌 수 있습니다.

### Vim/NeoVim

[coc.nvim](https://www.vim.org/scripts/script.php?script_id=5779)을 사용하는 경우, 다음 설정은 가져오기 기반 분석을 활성화합니다.

```json
{
    "codeLens.enable": true,
    "languageserver": {
        "go": {
            "command": "gopls",
            ...
            "initializationOptions": {
                "vulncheck": "Imports",
            }
        }
    }
}
```

## 참고 사항 및 주의 사항

- 이 확장 기능은 개인 패키지를 스캔하거나 개인 모듈에 대한 정보를 전송하지 않습니다. 모든 분석은 Go 취약점 데이터베이스에서 알려진 취약 모듈 목록을 가져온 다음 로컬에서 교차점을 계산하여 수행됩니다.
- `import` 기반 분석은 워크스페이스 모듈의 패키지 목록을 사용하며, `go.mod` 파일에서 보이는 것과 다를 수 있습니다(특히 `go.work` 또는 모듈 `replace`/`exclude`가 사용되는 경우).
- `govulncheck` 분석 결과는 코드를 수정하거나 Go 취약점 데이터베이스가 업데이트됨에 따라 오래될 수 있습니다. 분석 결과를 수동으로 무효화하려면 `go.mod` 파일 상단에 표시된 `"Reset go.mod diagnostics"` 코드를 사용하십시오. 그렇지 않으면 결과는 1시간 후에 자동으로 무효화됩니다.
- 현재 이 기능은 표준 라이브러리 또는 도구 체인에 대한 취약점을 보고하지 않습니다. 저희는 취약점 결과를 표시할 위치와 사용자가 문제를 해결하는 데 도움이 되는 방법을 조사하고 있습니다.
