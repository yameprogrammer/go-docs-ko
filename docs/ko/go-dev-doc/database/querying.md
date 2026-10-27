<!--{
  "Title": "데이터 쿼리하기"
}-->

데이터를 반환하는 SQL 문을 실행할 때는 `database/sql` 패키지에서 제공하는 `Query` 메서드 중 하나를 사용하십시오. 이 메서드들은 각각 `Row` 또는 `Rows`를 반환하며, `Scan` 메서드를 사용하여 해당 데이터를 변수로 복사할 수 있습니다. 예를 들어, `SELECT` 문을 실행할 때 이러한 메서드들을 사용합니다.

데이터를 반환하지 않는 문장을 실행할 때는 대신 `Exec` 또는 `ExecContext` 메서드를 사용할 수 있습니다. 자세한 내용은 [데이터를 반환하지 않는 문장 실행하기](/doc/database/change-data)를 참조하세요.

`database/sql` 패키지는 결과값을 얻기 위해 쿼리를 실행하는 두 가지 방법을 제공합니다.

*   **단일 행 쿼리** – `QueryRow`는 데이터베이스에서 최대 하나의 `Row`를 반환합니다. 자세한 내용은 [단일 행 쿼리](#single_row)를 참조하세요.
*   **다중 행 쿼리** – `Query`는 일치하는 모든 행을 코드로 반복 처리할 수 있는 `Rows` 구조체로 반환합니다. 자세한 내용은 [다중 행 쿼리](#multiple_rows)를 참조하세요.

동일한 SQL 문을 반복적으로 실행하는 경우, prepared statement 사용을 고려하십시오. 자세한 내용은 [Using prepared statements](/doc/database/prepared-statements)를 참조하십시오.

**주의:** SQL 문을 작성할 때 `fmt.Sprintf`와 같은 문자열 포맷팅 함수를 사용하지 마세요! SQL 인젝션 위험이 발생할 수 있습니다. 자세한 내용은 [SQL 인젝션 위험 방지](/doc/database/sql-injection)를 참조하세요.

### 단일 행 쿼리하기 {#single_row}

`QueryRow`는 고유 ID로 데이터를 조회할 때와 같이 최대 하나의 데이터베이스 행을 가져옵니다. 쿼리에 의해 여러 행이 반환되는 경우, `Scan` 메서드는 첫 번째 행을 제외한 나머지를 모두 버립니다.

`QueryRowContext`는 `QueryRow`와 유사하게 작동하지만 `context.Context` 인자를 추가로 받습니다.
더 자세한 내용은 [진행 중인 작업 취소하기](/doc/database/cancel-operations)를 참조하세요.

다음 예제는 구매를 처리하기에 충분한 재고가 있는지 확인하기 위해 쿼리를 사용하는 방법을 보여줍니다. SQL 문은 재고가 충분하면 `true`를, 그렇지 않으면 `false`를 반환합니다. [`Row.Scan`](https://pkg.go.dev/database/sql#Row.Scan)은 포인터를 통해 불리언(boolean) 반환 값을 `enough` 변수에 복사합니다.

```go
func canPurchase(id int, quantity int) (bool, error) {
	var enough bool
	// 단일 행을 기반으로 값을 쿼리합니다.
	if err := db.QueryRow("SELECT (quantity >= ?) from album where id = ?",
		quantity, id).Scan(&enough); err != nil {
		if err == sql.ErrNoRows {
			return false, fmt.Errorf("canPurchase %d: unknown album", id)
		}
		return false, fmt.Errorf("canPurchase %d: %v", id, err)
	}
	return enough, nil
}
```

**참고:** Prepared statement의 파라미터 플레이스홀더는 사용하는 DBMS 및 드라이버에 따라 다릅니다. 예를 들어, Postgres용 [pq driver](https://pkg.go.dev/github.com/lib/pq)는 `?` 대신 `$1`과 같은 플레이스홀더를 사용해야 합니다.

#### 오류 처리 {#single_row_errors}

`QueryRow` 자체는 에러를 반환하지 않습니다. 대신, `Scan`이 조회와 스캔 과정에서 발생한 모든 에러를 보고합니다. 쿼리 결과로 반환된 행이 없을 경우 [`sql.ErrNoRows`](https://pkg.go.dev/database/sql#ErrNoRows)를 반환합니다.

#### 단일 행을 반환하는 함수 {#single_row_functions}

<table id="single-row-functions-list" class="DocTable">
  <thead>
    <tr class="DocTable-head">
      <th class="DocTable-cell" width="20%">Function</th>
      <th class="DocTable-cell">설명</th>
    </tr>
  </thead>
  <tbody>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#DB.QueryRow">DB.QueryRow</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#DB.QueryRowContext">DB.QueryRowContext</a></code>
      </td>
      <td class="DocTable-cell">단일 행 쿼리를 독립적으로 실행합니다.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Tx.QueryRow">Tx.QueryRow</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#Tx.QueryRowContext">Tx.QueryRowContext</a></code>
      </td>
      <td class="DocTable-cell">더 큰 트랜잭션 내부에서 단일 행 쿼리를 실행합니다. 자세한 내용은
        <a href="/doc/database/execute-transactions">트랜잭션 실행(Executing transactions)</a>을 참조하세요.
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Stmt.QueryRow">Stmt.QueryRow</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#Stmt.QueryRowContext">Stmt.QueryRowContext</a></code>
      </td>
      <td class="DocTable-cell">이미 준비된 문(prepared statement)을 사용하여 단일 행 쿼리를 실행합니다. 자세한 내용은
        <a href="/doc/database/prepared-statements">준비된 문 사용(Using prepared statements)</a>을 참조하세요.
      </td>
    </tr>
    <tr class="DocTable-row">
        <td class="DocTable-cell">
  <code><a href="https://pkg.go.dev/database/sql#Conn.QueryRowContext">Conn.QueryRowContext</a></code>
      </td>
      <td class="DocTable-cell">예약된 연결(reserved connections)과 함께 사용합니다. 자세한 내용은
        <a href="/doc/database/manage-connections">연결 관리(Managing connections)</a>를 참조하세요.
      </td>
    </tr>
  </tbody>
</table>

### 여러 행 쿼리하기 {#multiple_rows}

`Query` 또는 `QueryContext`를 사용하여 여러 행을 조회할 수 있으며, 이 메서드들은 쿼리 결과를 나타내는 `Rows`를 반환합니다. 작성한 코드는 [`Rows.Next`](https://pkg.go.dev/database/sql#Rows.Next)를 사용하여 반환된 행들을 반복 처리합니다. 각 반복 단계에서 `Scan`을 호출하여 컬럼 값을 변수로 복사합니다.

`QueryContext`는 `Query`와 유사하게 작동하지만 `context.Context` 인자를 추가로 받습니다. 자세한 내용은 [진행 중인 작업 취소하기](/doc/database/cancel-operations)를 참조하세요.

다음 예제는 지정된 아티스트의 앨범을 반환하는 쿼리를 실행합니다. 앨범 정보는 `sql.Rows` 형태로 반환됩니다. 이 코드는 [`Rows.Scan`](https://pkg.go.dev/database/sql#Rows.Scan)을 사용하여 컬럼 값을 포인터로 표현된 변수에 복사합니다.

```go
func albumsByArtist(artist string) ([]Album, error) {
	rows, err := db.Query("SELECT * FROM album WHERE artist = ?", artist)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	// 반환된 행(rows)의 데이터를 저장할 album 슬라이스입니다.
	var albums []Album

	// 행을 순회하며 Scan을 사용하여 컬럼 데이터를 구조체 필드에 할당합니다.
	for rows.Next() {
		var alb Album
		if err := rows.Scan(&alb.ID, &alb.Title, &alb.Artist,
			&alb.Price, &alb.Quantity); err != nil {
			return albums, err
		}
		albums = append(albums, alb)
	}
	if err = rows.Err(); err != nil {
		return albums, err
	}
	return albums, nil
}
```

[`rows.Close`](https://pkg.go.dev/database/sql#Rows.Close)에 대한 `defer` 호출에 유의하세요.
이는 함수가 어떻게 반환되든 `rows`가 보유한 모든 리소스를 해제합니다. `rows`를 끝까지 루프 도는 것도 암시적으로 이를 닫아주지만, 어떤 상황에서도 `rows`가 닫히도록 `defer`를 사용하는 것이 더 좋습니다.

**참고:** 준비된 문장(prepared statements)의 파라미터 플레이스홀더는 사용하는 DBMS와 드라이버에 따라 다릅니다. 예를 들어, Postgres용 [pq driver](https://pkg.go.dev/github.com/lib/pq)는 `?` 대신 `$1`과 같은 플레이스홀더가 필요합니다.

#### 에러 처리 {#multiple_rows_errors}

쿼리 결과에 대해 루프를 돌린 후, `sql.Rows`에서 에러가 발생했는지 반드시 확인하십시오.
쿼리가 실패했을 경우, 코드는 이 방법을 통해 이를 감지합니다.

#### 여러 행을 반환하는 함수 {#multiple_rows_functions}

<table id="multiple-row-functions-list" class="DocTable">
  <thead>
    <tr class="DocTable-head">
      <th class="DocTable-cell" width="20%">함수</th>
      <th class="DocTable-cell">설명</th>
    </tr>
  </thead>
  <tbody>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#DB.Query">DB.Query</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#DB.QueryContext">DB.QueryContext</a></code>
      </td>
      <td class="DocTable-cell">쿼리를 독립적으로 실행합니다.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Tx.Query">Tx.Query</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#Tx.QueryContext">Tx.QueryContext</a></code>
      </td>
      <td class="DocTable-cell">더 큰 트랜잭션 내부에서 쿼리를 실행합니다. 자세한 내용은
        <a href="/doc/database/execute-transactions">트랜잭션 실행</a>을 참조하십시오.
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Stmt.Query">Stmt.Query</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#Stmt.QueryContext">Stmt.QueryContext</a></code>
      </td>
      <td class="DocTable-cell">이미 준비된 문장(prepared statement)을 사용하여 쿼리를 실행합니다. 자세한 내용은
        <a href="/doc/database/prepared-statements">준비된 문장 사용</a>을 참조하십시오.
    </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Conn.QueryContext">Conn.QueryContext</a></code>
      </td>
      <td class="DocTable-cell">예약된 연결과 함께 사용합니다. 자세한 내용은
        <a href="/doc/database/manage-connections">연결 관리</a>를 참조하십시오.
      </td>
    </tr>
  </tbody>
</table>

### Nullable 컬럼 값 처리하기 {#nullable_columns}

`database/sql` 패키지는 컬럼의 값이 null일 수 있을 때 `Scan` 함수의 인자로 사용할 수 있는 몇 가지 특수 타입을 제공합니다. 각 타입은 값이 null이 아닌지를 보고하는 `Valid` 필드와, null이 아닐 경우 해당 값을 보유하는 필드를 포함합니다.

다음 예제의 코드는 고객 이름을 쿼리합니다. 이름 값이 null인 경우, 코드는 애플리케이션에서 사용할 다른 값으로 대체합니다.

```go
var s sql.NullString
err := db.QueryRow("SELECT name FROM customer WHERE id = ?", id).Scan(&s)
if err != nil {
	log.Fatal(err)
}

// 고객 이름을 찾습니다. 이름이 없으면 자리 표시자(placeholder)를 사용합니다.
name := "Valued Customer"
if s.Valid {
	name = s.String
}
```

각 타입에 대한 자세한 내용은 `sql` 패키지 레퍼런스를 참조하세요:

*    [`NullBool`](https://pkg.go.dev/database/sql#NullBool)
*    [`NullFloat64`](https://pkg.go.dev/database/sql#NullFloat64)
*    [`NullInt32`](https://pkg.go.dev/database/sql#NullInt32)
*    [`NullInt64`](https://pkg.go.dev/database/sql#NullInt64)
*    [`NullString`](https://pkg.go.dev/database/sql#NullString)
*    [`NullTime`](https://pkg.go.dev/database/sql#NullTime)

### 컬럼에서 데이터 가져오기 {#column_data}

쿼리에 의해 반환된 행(rows)을 루프 돌 때, [`Rows.Scan`](https://pkg.go.dev/database/sql#Rows.Scan) 레퍼런스에 설명된 대로 `Scan`을 사용하여 행의 컬럼 값들을 Go 값으로 복사합니다.

모든 드라이버가 지원하는 기본 데이터 변환 세트가 있으며, 예를 들어 SQL `INT`를 Go `int`로 변환하는 것이 이에 해당합니다. 일부 드라이버는 이 변환 세트를 확장하여 제공하므로, 자세한 내용은 각 개별 드라이버의 문서를 참조하십시오.

예상하시겠지만, `Scan`은 컬럼 타입에서 이와 유사한 Go 타입으로 변환을 수행합니다. 예를 들어, `Scan`은 SQL의 `CHAR`, `VARCHAR`, `TEXT` 타입을 Go의 `string`으로 변환합니다. 하지만 `Scan`은 컬럼 값에 적합한 다른 Go 타입으로의 변환도 수행합니다. 예를 들어, 컬럼이 항상 숫자를 포함하는 `VARCHAR`인 경우, 값을 받기 위해 `int`와 같은 숫자형 Go 타입을 지정할 수 있으며, 이 경우 `Scan`이 내부적으로 `strconv.Atoi`를 사용하여 변환을 수행합니다.

`Scan` 함수에 의해 수행되는 변환에 대한 자세한 내용은 [`Rows.Scan`](https://pkg.go.dev/database/sql#Rows.Scan) 참조 문서를 확인하세요.

### 여러 결과 세트 처리하기 {#multiple_result_sets}

데이터베이스 작업이 여러 개의 결과 집합(result set)을 반환할 수 있는 경우, [`Rows.NextResultSet`](https://pkg.go.dev/database/sql#Rows.NextResultSet)을 사용하여 이를 가져올 수 있습니다. 이는 예를 들어, 여러 테이블을 각각 쿼리하여 각 테이블에 대한 결과 집합을 반환하는 SQL을 보낼 때 유용할 수 있습니다.

`Rows.NextResultSet`는 다음 결과 집합(result set)을 준비하여 `Rows.Next` 호출 시 해당 결과 집합의 첫 번째 행을 가져올 수 있도록 합니다. 이 메서드는 다음 결과 집합이 존재하는지 여부를 나타내는 불리언(boolean) 값을 반환합니다.

다음 예제의 코드는 `DB.Query`를 사용하여 두 개의 SQL 문을 실행합니다.
첫 번째 결과 집합은 프로시저의 첫 번째 쿼리에서 생성되며, `album` 테이블의 모든 행을 가져옵니다. 다음 결과 집합은 두 번째 쿼리에서 생성되며, `song` 테이블의 행들을 가져옵니다.

```go
rows, err := db.Query("SELECT * from album; SELECT * from song;")
if err != nil {
	log.Fatal(err)
}
defer rows.Close()

// 첫 번째 결과 세트를 순회합니다.
for rows.Next() {
	// 결과 세트를 처리합니다.
}

// 다음 결과 세트로 이동합니다.
rows.NextResultSet()

// 두 번째 결과 세트를 순회합니다.
for rows.Next() {
	// 두 번째 세트를 처리합니다.
}

// 두 결과 세트 중 오류가 있는지 확인합니다.
if err := rows.Err(); err != nil {
	log.Fatal(err)
}
```
