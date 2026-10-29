## 도구 {#tools}

### Go 명령 {#go-command}

### Cgo {#cgo}

### Vet {#vet}

새로운 [`scannererr`](https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/scannererr) 분석기는 [bufio.Scanner.Scan] 루프 이후에 스캐너 오류를 처리하지 않는 경우를 확인하며, 이는 스캐닝 또는 I/O 오류가 보고되지 않는 원인이 될 수 있습니다. <!-- /issue/17747/ -->

[`sqlrowserr`](https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/sqlrowserr) 분석기는 [sql.Rows.Next]를 사용하는 루프에 대해 유사한 검사를 수행하여, 반복 중 발생한 오류가 단순히 결과가 적은 것과 올바르게 구분되도록 합니다.
