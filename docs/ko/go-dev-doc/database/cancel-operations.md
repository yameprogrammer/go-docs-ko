<!--{
  "Title": "진행 중인 작업 취소하기"
}-->

Go의 [`context.Context`](https://pkg.go.dev/context#Context)를 사용하여 진행 중인 작업을 관리할 수 있습니다. `Context`는 자신이 나타내는 전체 작업이 취소되어 더 이상 필요하지 않은지 여부를 보고할 수 있는 표준 Go 데이터 값입니다. 애플리케이션 내의 함수 호출 및 서비스 간에 `context.Context`를 전달함으로써, 처리가 더 이상 필요하지 않을 때 작업을 조기에 중단하고 에러를 반환하게 할 수 있습니다. `Context`에 대한 자세한 내용은 [Go Concurrency Patterns: Context](/blog/context)를 참조하세요.

예를 들어, 다음과 같은 작업을 수행하고 싶을 수 있습니다:

*   너무 오래 걸리는 데이터베이스 작업을 포함하여, 실행 시간이 긴 작업을 종료합니다.
*   클라이언트가 연결을 닫는 경우와 같이, 다른 곳에서 발생한 취소 요청을 전파합니다.

Go 개발자를 위한 많은 API에는 `Context` 인자를 받는 메서드들이 포함되어 있어, 애플리케이션 전반에서 `Context`를 더 쉽게 사용할 수 있습니다.

### 타임아웃 후 데이터베이스 작업 취소하기 {#timeout_cancel}

`Context`를 사용하여 작업이 취소될 제한 시간(timeout) 또는 마감 기한(deadline)을 설정할 수 있습니다. 제한 시간이나 마감 기한이 설정된 `Context`를 파생시키려면 [`context.WithTimeout`](https://pkg.go.dev/context#WithTimeout) 또는 [`context.WithDeadline`](https://pkg.go.dev/context#WithDeadline)을 호출하십시오.

다음 타임아웃 예제의 코드는 `Context`를 생성하여 `sql.DB`의 [`QueryContext`](https://pkg.go.dev/database/sql#DB.QueryContext) 메서드로 전달합니다.

```go
func QueryWithTimeout(ctx context.Context) {
	// 타임아웃이 설정된 Context를 생성합니다.
	queryCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	// 쿼리와 함께 타임아웃 Context를 전달합니다.
	rows, err := db.QueryContext(queryCtx, "SELECT * FROM album")
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	// 반환된 행(rows)을 처리합니다.
}
```

이 예제에서 `queryCtx`가 `ctx`로부터 파생된 것처럼, 하나의 컨텍스트가 외부 컨텍스트로부터 파생된 경우, 외부 컨텍스트가 취소되면 파생된 컨텍스트 또한 자동으로 취소됩니다. 예를 들어, HTTP 서버에서 `http.Request.Context` 메서드는 요청과 연결된 컨텍스트를 반환합니다. 해당 컨텍스트는 HTTP 클라이언트가 연결을 끊거나 HTTP 요청을 취소하면(HTTP/2에서 가능) 취소됩니다. 위의 `QueryWithTimeout`에 HTTP 요청의 컨텍스트를 전달하면, 전체 HTTP 요청이 취소되었거나 쿼리가 5초 이상 걸린 경우 *둘 중 어느 쪽이든* 데이터베이스 쿼리가 조기에 중단됩니다.

**참고:** 타임아웃이나 데드라인을 설정하여 새로운 `Context`를 생성할 때 반환되는 `cancel` 함수 호출은 항상 `defer` 처리하십시오. 이렇게 하면 포함된 함수가 종료될 때 새로운 `Context`가 점유하고 있던 리소스가 해제됩니다. 또한 이는 `queryCtx`를 취소하지만, 함수가 반환될 시점에는 더 이상 `queryCtx`를 사용하는 곳이 없어야 합니다.
