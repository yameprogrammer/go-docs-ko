[Go 보안으로 돌아가기](/security)

[Go 언어 서버](https://pkg.go.dev/golang.org/x/tools/cmd/gopls)와 통합된 에디터(예: [Go 확장 기능이 설치된 VS Code](https://marketplace.visualstudio.com/items?itemName=golang.go))는 종속성에서 취약점을 감지할 수 있습니다.

종속성에서 취약점을 탐지하는 두 가지 모드가 있습니다. 두 모드 모두 [Go vulnerability database](https://vuln.go.dev)를 기반으로 하며 서로를 보완합니다.

* 임포트 기반 분석(Imports-based analysis): 이 모드에서 에디터는 워크스페이스에 임포트된 패키지 집합을 스캔하여 취약점을 보고하며, 그 결과를 `go.mod` 파일의 진단(diagnostics)으로 표시합니다. 이 방식은 빠르지만, 코드에서 취약한 심볼을 포함하는 패키지를 임포트했더라도 실제 취약한 함수에 도달할 수 없는 경우 오탐(false positives)을 보고할 수 있습니다. 이 모드는 gopls 설정의 [`"vulncheck": "Imports"`](https://github.com/golang/tools/blob/master/gopls/doc/settings.md#vulncheck-enum)를 통해 활성화할 수 있습니다.
* `Govulncheck` 분석: 이 방식은 `gopls`에 내장된 [`govulncheck`](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck) 명령줄 도구를 기반으로 합니다. 이를 통해 코드가 실제로 취약한 함수를 호출하는지 확인하는 저노이즈의 신뢰할 수 있는 방법을 제공합니다. 이 분석은 계산 비용이 많이 들 수 있으므로, 임포트 기반 분석의 진단 보고서와 연결된 "Run govulncheck to verify" 코드 액션을 사용하거나, `go.mod` 파일에서 [`"codelenses.run_govulncheck"`](https://github.com/golang/tools/blob/master/gopls/doc/settings.md#run-govulncheck) 코드 렌즈를 사용하여 수동으로 실행해야 합니다.

<div style="text-align: center;"><img src="vscode.gif" alt="Vulncheck"></div>

<em>Go: Toggle Vulncheck</em> <a
href="https://user-images.githubusercontent.com/4999471/206977512-a821107d-9ffb-4456-9b27-6a6a4f900ba6.mp4">(vulncheck.mp4)</a>
</div>

이 기능들은 `gopls` v0.11.0 또는 그 이후 버전에서 사용할 수 있습니다. 의견이 있으시면 [go.dev/s/vsc-vulncheck-feedback](/s/vsc-vulncheck-feedback)에 공유해 주세요.

## 에디터별 지침

### VS Code

[Go 확장 기능](https://marketplace.visualstudio.com/items?itemName=golang.go)은 gopls와의 통합을 제공합니다. 취약점 스캔 기능을 활성화하려면 다음 설정이 필요합니다:

```
"go.diagnostic.vulncheck": "Imports", // 기본적으로 import 기반 분석을 활성화합니다.
"gopls": {
  "ui.codelenses": {
    "run_govulncheck": true  // go.mod 파일에 "Run govulncheck" 코드 렌즈를 표시합니다.
  }
}
```

["Go Toggle Vulncheck"](https://github.com/golang/vscode-go/wiki/Commands#go-toggle-vulncheck) 명령을 사용하여 현재 작업 영역에 대해 임포트 기반 분석(imports-based analysis)을 켜거나 끌 수 있습니다.

### Vim/NeoVim

[coc.nvim](https://www.vim.org/scripts/script.php?script_id=5779)을 사용할 때, 다음 설정을 통해 import 기반 분석을 활성화할 수 있습니다.

```
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

## 참고 및 주의 사항

- 이 확장은 프라이빗 패키지를 스캔하지 않으며 프라이빗 모듈에 대한 어떠한 정보도 전송하지 않습니다. 모든 분석은 Go 취약점 데이터베이스에서 알려진 취약한 모듈 목록을 가져온 뒤, 로컬에서 교집합을 계산하는 방식으로 수행됩니다.
- 임포트 기반 분석은 워크스페이스 모듈의 패키지 목록을 사용합니다. 만약 `go.work`나 모듈 `replace`/`exclude`가 사용된 경우, `go.mod` 파일에서 보이는 내용과 다를 수 있습니다.
- 코드를 수정하거나 Go 취약점 데이터베이스가 업데이트되면 govulncheck 분석 결과가 오래된 정보가 될 수 있습니다. 분석 결과를 수동으로 무효화하려면 `go.mod` 파일 상단에 표시되는 `"Reset go.mod diagnostics"` 코드렌즈(codelens)를 사용하십시오. 그렇지 않으면 결과는 한 시간 후에 자동으로 무효화됩니다.
- 이 기능들은 현재 표준 라이브러리나 툴체인의 취약점은 보고하지 않습니다. 분석 결과를 어디에 표시하고 사용자가 문제를 어떻게 해결하도록 도울지에 대한 UX를 계속 조사 중입니다.
