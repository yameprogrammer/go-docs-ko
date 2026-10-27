<!--{
  "제목": "트랜잭션 실행"
}-->

다음과 같은 [`sql.Tx`](https://pkg.go.dev/database/sql#Tx)를 사용하여 데이터베이스 트랜잭션을 실행할 수 있습니다. 이는 트랜잭션을 나타냅니다.
`Commit` 및 `Rollback` 메서드와 같이 트랜잭션에 특정한 의미를 나타내는 것 외에도, `sql.Tx`는 일반적인 데이터베이스 작업을 수행하는 데 사용되는 모든 메서드를 포함합니다. `sql.Tx`를 얻으려면 `DB.Begin` 또는 `DB.BeginTx`를 호출합니다.

데이터베이스 트랜잭션은 여러 연산을 하나의 큰 목표를 달성하기 위해 그룹화합니다. 모든 연산이 성공해야 하거나, 그렇지 않으면 어떤 것도 수행할 수 없으며, 이 경우에도 데이터의 무결성이 유지됩니다.
일반적으로 트랜잭션 워크플로우에는 다음이 포함됩니다:

1. 트랜잭션 시작.
2. 데이터베이스 작업 집합 실행.
3. 오류가 발생하지 않으면, 데이터베이스 변경 사항을 반영하여 트랜잭션을 커밋.
4. 오류가 발생하면, 데이터베이스를 변경하지 않고 트랜잭션을 롤백.

`sql` 패키지는 트랜잭션 시작 및 종료 방법을 제공하며, 그 중간에 수행되는 데이터베이스 작업을 수행하는 방법도 제공합니다. 이러한 방법들은 위 워크플로우의 네 단계에 해당합니다.

*   트랜잭션을 시작합니다.

[`DB.Begin`](https://pkg.go.dev/database/sql#DB.Begin) 또는
    [`DB.BeginTx`](https://pkg.go.dev/database/sql#DB.BeginTx)은 새로운
    데이터베이스 트랜잭션을 시작하고, 이를 나타내는 `sql.Tx`를 반환합니다.
*   데이터베이스 작업을 수행합니다.

`sql.Tx`를 사용하면 단일 연결을 사용하여 여러 연산을 수행하여 데이터베이스를 쿼리하거나 업데이트할 수 있습니다. 이를 지원하기 위해 `Tx`는 다음 메서드를 내보냅니다:

*   [`Exec`](https://pkg.go.dev/database/sql#Tx.Exec) 및
        [`ExecContext`](https://pkg.go.dev/database/sql#Tx.ExecContext)를 사용하여 `INSERT`, `UPDATE`, `DELETE`와 같은 SQL 문을 통해 데이터베이스 변경을 수행합니다.

자세한 내용은 [데이터를 반환하지 않는 SQL 문 실행 방법](/doc/database/change-data)을 참조하세요.

*   [`Query`](https://pkg.go.dev/database/sql#Tx.Query),
        [`QueryContext`](https://pkg.go.dev/database/sql#Tx.QueryContext),
        [`QueryRow`](https://pkg.go.dev/database/sql#Tx.QueryRow), 및
        [`QueryRowContext`](https://pkg.go.dev/database/sql#Tx.QueryRowContext)
        는 결과로 행을 반환하는 작업에 사용됩니다.

자세한 내용은 [데이터 쿼리 참조](/doc/database/querying)

*   [`Prepare`](https://pkg.go.dev/database/sql#Tx.Prepare),
    [`PrepareContext`](https://pkg.go.dev/database/sql#Tx.PrepareContext),
    [`Stmt`](https://pkg.go.dev/database/sql#Tx.Stmt), 및
    [`StmtContext`](https://pkg.go.dev/database/sql#Tx.StmtContext)는
    사전 정의된 쿼리를 사용하기 위한 기능입니다.

자세한 내용은 [준비된 문을 사용하기](https://example.com/doc/database/prepared-statements)를 참조하세요.

*   다음 중 하나로 트랜잭션을 완료합니다:
    *   `Tx.Commit`을 사용하여 트랜잭션을 커밋합니다: [`https://pkg.go.dev/database/sql#Tx.Commit`](https://pkg.go.dev/database/sql#Tx.Commit).

만약 `Commit`이 성공하면 (오류가 반환되지 않으면), 모든 쿼리 결과는 유효한 것으로 확인되고, 실행된 모든 업데이트는 단일 원자적 변경으로 데이터베이스에 적용됩니다. 만약 `Commit`이 실패하면, `Tx`에 있는 `Query` 및 `Exec`의 모든 결과는 유효하지 않은 것으로 폐기되어야 합니다.
    *   [`Tx.Rollback`](https://pkg.go.dev/database/sql#Tx.Rollback)를 사용하여 트랜잭션을 롤백합니다.

`Tx.Rollback`이 실패하더라도, 트랜잭션은 더 이상 유효하지 않으며, 데이터베이스에 커밋되지 않습니다.

### 최적의 실무 지침 {#best_practices}

복잡한 의미와 트랜잭션이 필요로 하는 연결 관리를 보다 효과적으로 이해하기 위해, 다음 우수 사례를 따르세요.

*   이 섹션에 설명된 API를 사용하여 트랜잭션을 관리하십시오. `BEGIN` 및 `COMMIT`과 같은 트랜잭션 관련 SQL 문을 직접 사용하는 것은 피하십시오. 이렇게 하면 특히 동시 프로그램에서 데이터베이스 상태가 예측 불가능해질 수 있습니다.
*   트랜잭션을 사용할 때는 또한, 직접 `sql.DB`의 트랜잭션 관련 메서드를 호출하지 않도록 주의하십시오. 이러한 호출은 트랜잭션 외부에서 실행되므로, 코드에 데이터베이스 상태에 대한 일관성 없는 뷰를 제공하거나 심지어 데드락을 발생시킬 수 있습니다.

### 예제 {#example}

다음 예제에서 사용된 코드는 새 앨범 주문을 생성하기 위해 트랜잭션을 사용합니다. 이 과정에서 코드는 다음과 같이 수행합니다:

1. 트랜잭션을 시작합니다.
2. 트랜잭션의 롤백을 지연합니다. 트랜잭션이 성공하면 함수가 종료되기 전에 커밋되며, 지연된 롤백 호출은 아무 작업도 수행하지 않습니다. 트랜잭션이 실패하면 커밋되지 않으므로, 함수가 종료될 때 롤백이 호출됩니다.
3. 고객이 주문하는 앨범에 충분한 재고가 있는지 확인합니다.
4. 충분하다면, 주문한 앨범 수를 기준으로 재고 수를 업데이트합니다.
5. 새로운 주문을 생성하고 클라이언트에게 생성된 주문 ID를 반환합니다.
6. 트랜잭션을 커밋하고 ID를 반환합니다.

이 예제는 `Tx` 메서드를 사용하며, 이는 `context.Context` 인수를 취합니다. 이를 통해 함수의 실행 (데이터베이스 작업 포함)이 너무 오래 실행되거나 클라이언트 연결이 닫힐 경우 중단될 수 있습니다. 자세한 내용은 [중단 중인 작업 취소](/doc/database/cancel-operations)를 참조하세요.

```
// CreateOrder는 앨범에 대한 주문을 생성하고 새로운 주문 ID를 반환합니다.
func CreateOrder(ctx context.Context, albumID, quantity, custID int) (orderID int64, err error) {

	// 실패 결과 준비를 위한 헬퍼 함수를 만듭니다.
	fail := func(err error) (int64, error) {
		return 0, fmt.Errorf("CreateOrder: %v", err)
	}

	// 트랜잭션 요청을 위한 Tx를 가져옵니다.
	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return fail(err)
	}
	// 오류가 발생하면 롤백을 미루도록 합니다.
	defer tx.Rollback()

	// 주문에 필요한 앨범 재고가 있는지 확인합니다.
	var enough bool
	if err = tx.QueryRowContext(ctx, "SELECT (quantity >= ?) from album where id = ?",
		quantity, albumID).Scan(&enough); err != nil {
		if err == sql.ErrNoRows {
			return fail(fmt.Errorf("앨범을 찾을 수 없음"))
		}
		return fail(err)
	}
	if !enough {
		return fail(fmt.Errorf("재고가 부족함"))
	}

	// 주문에서 수량을 뺀 앨범 재고를 업데이트합니다.
	_, err = tx.ExecContext(ctx, "UPDATE album SET quantity = quantity - ? WHERE id = ?",
		quantity, albumID)
	if err != nil {
		return fail(err)
	}

	// album_order 테이블에 새 행을 만듭니다.
	result, err := tx.ExecContext(ctx, "INSERT INTO album_order (album_id, cust_id, quantity, date) VALUES (?, ?, ?, ?)",
		albumID, custID, quantity, time.Now())
	if err != nil {
		return fail(err)
	}
	// 새로 생성된 주문 항목의 ID를 가져옵니다.
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
