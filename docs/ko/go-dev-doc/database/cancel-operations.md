<!--{
  "제목": "진행 중인 작업 취소"
}-->

다음 Go 패키지를 사용하여 진행 중인 작업을 관리할 수 있습니다.
[`context.Context`](https://pkg.go.dev/context#Context). `Context`는 전체 작업을 나타내는 작업을 취소했음을 보고하고 더 이상 필요하지 않을 때 알려주는 표준 Go 데이터 값입니다. 애플리케이션 내의 함수 호출 및 서비스 간에 `context.Context`를 전달하여, 해당 프로세스가 더 이상 필요하지 않을 때 조기에 중단하고 오류를 반환할 수 있습니다. `Context`에 대한 자세한 내용은 [Go Concurrency Patterns: Context](/blog/context)를 참조하세요.

예를 들어, 다음과 같은 작업을 수행하고 싶을 수 있습니다:

*   긴 시간이 걸리는 작업을 중단합니다 (특히, 데이터베이스 작업 등).
*   클라이언트가 연결을 닫는 등 다른 곳에서 전파되는 취소 요청을 처리합니다.

많은 Go 개발자를 위한 API는 `Context` 인수를 받는 메서드를 포함하고 있으며, 이를 통해 애플리케이션 전체에서 `Context`를 더 쉽게 사용할 수 있습니다.

### 타임아웃 후 데이터베이스 작업 취소 {#timeout_cancel}

```go
func CancelDatabaseOperations(timeout time.Duration) {
  // 예: 데이터베이스 연결 닫기
  db.Close()
}
```

| 작업 | 상태 |
|---|---|
| 데이터베이스 연결 | 닫힘 |
| 데이터베이스 쿼리 | 취소됨 |

`Context`를 사용하여 작업을 취소할 시간 또는 마감일을 설정할 수 있습니다. 시간 또는 마감일을 가진 `Context`를 얻으려면 `context.WithTimeout` 또는 `context.WithDeadline` 함수를 호출하십시오.

다음 타임아웃 예제에서 코드는 `Context`를 생성하고 이를 `sql.DB`의 [`QueryContext`](https://pkg.go.dev/database/sql#DB.QueryContext) 메서드에 전달합니다.

```markdown
```go
func QueryWithTimeout(ctx context.Context) {
	// 타임아웃이 있는 컨텍스트를 생성합니다.
	queryCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	// 타임아웃 컨텍스트를 사용하여 쿼리를 실행합니다.
	rows, err := db.QueryContext(queryCtx, "SELECT * FROM album")
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	// 반환된 행을 처리합니다.
}
```

`queryCtx`가 `ctx`에서 파생되는 경우 (예: 이 예시에서), 외부 컨텍스트가 취소되면, 파생된 컨텍스트도 자동으로 취소됩니다. 예를 들어, HTTP 서버에서 `http.Request.Context` 메서드는 요청과 관련된 컨텍스트를 반환합니다. 이 컨텍스트는 HTTP 클라이언트가 연결을 끊거나 HTTP 요청을 취소할 경우 취소됩니다 (HTTP/2에서 가능). `QueryWithTimeout`에 HTTP 요청의 컨텍스트를 전달하면, 데이터베이스 쿼리가 다음 중 하나로 인해 조기에 중단됩니다:
* 전체 HTTP 요청이 취소된 경우
* 쿼리가 5초 이상 소요된 경우

**참고:** 새 `Context`를 만들 때 시간 초 또는 데드라인이 설정된 경우 반환되는 `cancel` 함수 호출을 항상 미루세요. 이렇게 하면 새 `Context`가 보유한 리소스를 해제할 수 있습니다. 또한 `queryCtx`를 취소하지만, 함수가 반환될 때까지 `queryCtx`를 사용하는 다른 것은 없어야 합니다.
