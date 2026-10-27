<!--{
  "Title": "트랜잭션 실행하기"
}-->

트랜잭션을 나타내는 [`sql.Tx,`](https://pkg.go.dev/database/sql#Tx)를 사용하여 데이터베이스 트랜잭션을 실행할 수 있습니다.
트랜잭션 전용 시맨틱을 나타내는 `Commit` 및 `Rollback` 메서드 외에도, `sql.Tx`는 일반적인 데이터베이스 작업을 수행하는 데 사용하는 모든 메서드를 가지고 있습니다. `sql.Tx`를 얻으려면 `DB.Begin` 또는 `DB.BeginTx`를 호출하십시오.

[데이터베이스 트랜잭션](https://en.wikipedia.org/wiki/Database_transaction)은
더 큰 목표의 일부로서 여러 작업을 그룹화합니다. 모든 작업이 성공하거나, 아니면 모두 실패해야 하며, 어느 경우든 데이터의 무결성이 유지되어야 합니다.
일반적으로 트랜잭션 워크플로우에는 다음이 포함됩니다:

1. 트랜잭션 시작.
2. 일련의 데이터베이스 작업 수행.
3. 오류가 발생하지 않은 경우, 트랜잭션을 커밋하여 데이터베이스 변경 사항을 반영.
4. 오류가 발생한 경우, 트랜잭션을 롤백하여 데이터베이스를 변경 전 상태로 유지.

`sql` 패키지는 트랜잭션을 시작하고 종료하는 메서드뿐만 아니라, 그 사이의 데이터베이스 작업을 수행하는 메서드들을 제공합니다. 이러한 메서드들은 위 워크플로우의 4단계에 대응합니다.

*   트랜잭션을 시작합니다.

[`DB.Begin`](https://pkg.go.dev/database/sql#DB.Begin) 또는
    [`DB.BeginTx`](https://pkg.go.dev/database/sql#DB.BeginTx)는 새로운
    데이터베이스 트랜잭션을 시작하며, 이를 나타내는 `sql.Tx`를 반환합니다.
*   데이터베이스 작업을 수행합니다.

`sql.Tx`를 사용하면 단일 연결을 사용하는 일련의 작업으로 데이터베이스를 쿼리하거나 업데이트할 수 있습니다. 이를 지원하기 위해 `Tx`는 다음과 같은 메서드들을 제공합니다:

*   `INSERT`, `UPDATE`, `DELETE`와 같은 SQL 문을 통해 데이터베이스 변경 사항을 적용하기 위한 [`Exec`](https://pkg.go.dev/database/sql#Tx.Exec) 및 [`ExecContext`](https://pkg.go.dev/database/sql#Tx.ExecContext)가 있습니다.

더 자세한 내용은 [데이터를 반환하지 않는 SQL 문 실행하기](/doc/database/change-data)를 참조하십시오.

*   행(rows)을 반환하는 작업에는 [`Query`](https://pkg.go.dev/database/sql#Tx.Query),
        [`QueryContext`](https://pkg.go.dev/database/sql#Tx.QueryContext),
        [`QueryRow`](https://pkg.go.dev/database/sql#Tx.QueryRow), 및
        [`QueryRowContext`](https://pkg.go.dev/database/sql#Tx.QueryRowContext)를 사용합니다.

더 자세한 내용은 [데이터 쿼리하기](/doc/database/querying)를 참조하세요.

*   준비된 문장(prepared statements)을 미리 정의하기 위한 [`Prepare`](https://pkg.go.dev/database/sql#Tx.Prepare), [`PrepareContext`](https://pkg.go.dev/database/sql#Tx.PrepareContext), [`Stmt`](https://pkg.go.dev/database/sql#Tx.Stmt), 및 [`StmtContext`](https://pkg.go.dev/database/sql#Tx.StmtContext).

자세한 내용은 [Using prepared statements](/doc/database/prepared-statements)를 참조하세요.

*   다음 중 _하나_를 사용하여 트랜잭션을 종료하십시오:
    *   [`Tx.Commit`](https://pkg.go.dev/database/sql#Tx.Commit)을 사용하여 트랜잭션을 커밋합니다.

`Commit`이 성공하면(`nil` 에러를 반환하면), 모든 쿼리 결과는 유효한 것으로 확정되며 실행된 모든 업데이트는 단일 원자적 변경 사항으로 데이터베이스에 적용됩니다. `Commit`이 실패하면, `Tx`에서 수행한 `Query` 및 `Exec`의 모든 결과는 유효하지 않은 것으로 간주하여 폐기해야 합니다.
    *   [`Tx.Rollback`](https://pkg.go.dev/database/sql#Tx.Rollback)을 사용하여 트랜잭션을 롤백하십시오.

`Tx.Rollback`이 실패하더라도, 트랜잭션은 더 이상 유효하지 않으며 데이터베이스에 커밋되지도 않습니다.

### 권장 모범 사례 {#best_practices}

트랜잭션에서 때때로 요구되는 복잡한 시맨틱과 연결 관리를 더 효율적으로 처리하려면 아래의 권장 사항을 따르십시오.

*   트랜잭션을 관리하려면 이 섹션에서 설명하는 API를 사용하십시오. `BEGIN` 및 `COMMIT`과 같은 트랜잭션 관련 SQL 문을 직접 사용하지 *마십시오*. 그렇게 하면 특히 동시성 프로그램에서 데이터베이스가 예측 불가능한 상태가 될 수 있습니다.
*   트랜잭션을 사용할 때, 트랜잭션에 포함되지 않은 `sql.DB` 메서드를 직접 호출하지 않도록 주의하십시오. 해당 메서드들은 트랜잭션 외부에서 실행되어 코드에 일관성 없는 데이터베이스 상태를 보여주거나 심지어 데드락(deadlock)을 유발할 수 있습니다.

### 예제 {#example}

다음 예제의 코드는 트랜잭션을 사용하여 앨범에 대한 새로운 고객 주문을 생성합니다. 이 과정에서 코드는 다음과 같은 작업을 수행합니다:

1. 트랜잭션을 시작합니다.
2. 트랜잭션의 rollback을 defer합니다. 트랜잭션이 성공하면 함수가 종료되기 전에 commit되며, 이 경우 defer된 rollback 호출은 아무런 동작도 하지 않습니다(no-op). 트랜잭션이 실패하면 commit되지 않으며, 함수가 종료될 때 rollback이 호출됩니다.
3. 고객이 주문하려는 앨범의 재고가 충분한지 확인합니다.
4. 재고가 충분하다면, 주문한 앨범 수만큼 재고 수량을 줄여 업데이트합니다.
5. 새로운 주문을 생성하고, 클라이언트를 위해 생성된 주문 ID를 가져옵니다.
6. 트랜잭션을 commit하고 ID를 반환합니다.

이 예제는 `context.Context` 인자를 받는 `Tx` 메서드들을 사용합니다. 이를 통해 데이터베이스 작업을 포함한 함수의 실행 시간이 너무 길어지거나 클라이언트 연결이 끊긴 경우, 실행 중인 작업을 취소할 수 있습니다. 자세한 내용은 [진행 중인 작업 취소하기](/doc/database/cancel-operations)를 참조하십시오.

```go
// CreateOrder는 앨범에 대한 주문을 생성하고 새로운 주문 ID를 반환합니다.
func CreateOrder(ctx context.Context, albumID, quantity, custID int) (orderID int64, err error) {

	// 실패 결과를 준비하기 위한 헬퍼 함수를 생성합니다.
	fail := func(err error) (int64, error) {
		return 0, fmt.Errorf("CreateOrder: %v", err)
	}

	// 트랜잭션 요청을 위한 Tx를 가져옵니다.
	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return fail(err)
	}
	// 실패할 경우를 대비해 롤백을 예약(defer)합니다.
	defer tx.Rollback()

	// 앨범 재고가 주문량에 충분한지 확인합니다.
	var enough bool
	if err = tx.QueryRowContext(ctx, "SELECT (quantity >= ?) from album where id = ?",
		quantity, albumID).Scan(&enough); err != nil {
		if err == sql.ErrNoRows {
			return fail(fmt.Errorf("no such album"))
		}
		return fail(err)
	}
	if !enough {
		return fail(fmt.Errorf("not enough inventory"))
	}

	// 주문 수량만큼 앨범 재고를 차감하도록 업데이트합니다.
	_, err = tx.ExecContext(ctx, "UPDATE album SET quantity = quantity - ? WHERE id = ?",
		quantity, albumID)
	if err != nil {
		return fail(err)
	}

	// album_order 테이블에 새로운 행을 생성합니다.
	result, err := tx.ExecContext(ctx, "INSERT INTO album_order (album_id, cust_id, quantity, date) VALUES (?, ?, ?, ?)",
		albumID, custID, quantity, time.Now())
	if err != nil {
		return fail(err)
	}
	// 방금 생성된 주문 항목의 ID를 가져옵니다.
	orderID, err = result.LastInsertId()
	if err != nil {
		return fail(err)
	}

	// 트랜잭션을 커밋합니다.
	if err = tx.Commit(); err != nil {
		return fail(err)
	}

	// 주문 ID를 반환합니다.
	return orderID, nil
}
```
