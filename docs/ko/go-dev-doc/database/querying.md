<!--{
  "제목": "데이터 쿼리"
}-->

SQL 문을 실행하여 데이터를 반환할 때, `database/sql` 패키지에 제공된 `Query` 메서드 중 하나를 사용합니다. 각 메서드는 `Row` 또는 `Rows`를 반환하며, 이 데이터는 `Scan` 메서드를 사용하여 변수에 복사할 수 있습니다. 예를 들어, `SELECT` 문을 실행하는 데 이러한 메서드를 사용합니다.

명령을 실행할 때, 데이터가 반환되지 않는 경우 `Exec` 또는 `ExecContext` 메서드를 사용하는 것이 좋습니다. 자세한 내용은 [데이터가 반환되지 않는 명령 실행하기](/doc/database/change-data)를 참조하십시오.

`database/sql` 패키지는 쿼리를 실행하고 결과를 얻는 두 가지 방법을 제공합니다.

*   **단일 행 쿼리** – `QueryRow`는 데이터베이스에서 최대 하나의 `Row`만 반환합니다. 자세한 내용은 [단일 행 쿼리](#single_row)를 참조하세요.
*   **여러 행 쿼리** – `Query`는 일치하는 모든 행을 `Rows` 구조체로 반환하며, 이를 통해 코드가 반복문을 사용할 수 있습니다. 자세한 내용은 [여러 행 쿼리](#multiple_rows)를 참조하세요.

만약 코드가 동일한 SQL 문을 반복적으로 실행해야 한다면,
준비된 문(prepared statement)을 사용하는 것을 고려해 보세요. 자세한 내용은
[준비된 문 사용하기](/doc/database/prepared-statements)를 참조하십시오.

**주의:** `fmt.Sprintf`와 같은 문자열 포맷 함수를 사용하여 SQL 문을 구성하지 마세요! 이렇게 하면 SQL 삽입 위험이 발생할 수 있습니다. 자세한 내용은 [SQL 삽입 위험 방지](/doc/database/sql-injection)를 참조하세요.

### 단일 행 쿼리 {#single_row}

`QueryRow`는 단일 데이터베이스 행을 가져옵니다. 예를 들어, 고유 ID를 사용하여 데이터를 조회할 때 유용합니다. 쿼리가 여러 행을 반환하면 `Scan` 메서드는 첫 번째 행만 유지하고 나머지는 모두 버립니다.

`QueryRowContext`는 `QueryRow`와 유사하지만 `context.Context` 인수를 사용합니다.
자세한 내용은 [진행 중인 작업 취소](/doc/database/cancel-operations)를 참조하십시오.

다음 예제는 구매를 지원하기에 충분한 재고가 있는지 확인하기 위한 쿼리를 사용합니다. SQL 문은 충분한 재고가 있으면 `true`를, 그렇지 않으면 `false`를 반환합니다. [`Row.Scan`](https://pkg.go.dev/database/sql#Row.Scan)는 포인터를 통해 boolean 반환 값을 `enough` 변수에 복사합니다.

```
func canPurchase(id int, quantity int) (bool, error) {
	var enough bool
	// 'album' 테이블에서 특정 ID와 수량에 해당하는 데이터를 쿼리합니다.
	if err := db.QueryRow("SELECT (quantity >= ?) FROM album WHERE id = ?",
		quantity, id).Scan(&enough); err != nil {
		if err == sql.ErrNoRows {
			return false, fmt.Errorf("canPurchase %d: 알 수 없는 앨범", id)
		}
		return false, fmt.Errorf("canPurchase %d: %v", id, err)
	}
	return enough, nil
}
```

**참고:** 준비된 문(prepared statements)의 매개변수 대체자는 사용하는 DBMS 및 드라이버에 따라 다릅니다. 예를 들어, Postgres에 사용되는 [pq 드라이버](https://pkg.go.dev/github.com/lib/pq)는 `?` 대신 `$1`과 같은 대체자를 필요로 합니다.

#### 오류 처리 {#단_행_오류}

`QueryRow` 자체는 오류를 반환하지 않습니다. 대신, `Scan`은 결합된 검색 및 스캔에서 발생하는 모든 오류를 보고합니다. 쿼리가 행을 찾지 못할 때 `[`sql.ErrNoRows`](https://pkg.go.dev/database/sql#ErrNoRows)를 반환합니다.

#### 단일 행을 반환하는 함수 {#단일_행_함수}

```markdown
<table id="single-row-functions-list" class="DocTable">
  <thead>
    <tr class="DocTable-head">
      <th class="DocTable-cell" width="20%">함수</th>
      <th class="DocTable-cell">설명</th>
    </tr>
  </thead>
  <tbody>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#DB.QueryRow">DB.QueryRow</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#DB.QueryRowContext">DB.QueryRowContext</a></code>
      </td>
      <td class="DocTable-cell">격리된 단일 행 쿼리를 실행합니다.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Tx.QueryRow">Tx.QueryRow</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#Tx.QueryRowContext">Tx.QueryRowContext</a></code>
      </td>
      <td class="DocTable-cell">더 큰 트랜잭션 내에서 단일 행 쿼리를 실행합니다. 자세한 내용은 다음을 참조하십시오:
        <a href="/doc/database/execute-transactions">트랜잭션 실행</a>.
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Stmt.QueryRow">Stmt.QueryRow</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#Stmt.QueryRowContext">Stmt.QueryRowContext</a></code>
      </td>
      <td class="DocTable-cell">이미 준비된 문을 사용하여 단일 행 쿼리를 실행합니다. 자세한 내용은 다음을 참조하십시오:
        <a href="/doc/database/prepared-statements">준비된 문 사용</a>.
      </td>
    </tr>
    <tr class="DocTable-row">
        <td class="DocTable-cell">
  <code><a href="https://pkg.go.dev/database/sql#Conn.QueryRowContext">Conn.QueryRowContext</a></code>
      </td>
      <td class="DocTable-cell">예약된 연결을 사용하기 위한 것입니다. 자세한 내용은 다음을 참조하십시오:
        <a href="/doc/database/manage-connections">연결 관리</a>.
      </td>
    </tr>
  </tbody>
</table>

### 여러 행 쿼리하기 {#multiple_rows}

`Query` 또는 `QueryContext`를 사용하여 여러 행을 쿼리할 수 있으며, 이는 쿼리 결과에 해당하는 `Rows`를 반환합니다. 반환된 행을 반복하기 위해 `[Rows.Next](https://pkg.go.dev/database/sql#Rows.Next)`를 사용합니다. 각 반복에서 `Scan`을 호출하여 열 값을 변수에 복사합니다.

`QueryContext`는 `Query`와 유사하게 작동하지만 `context.Context` 인수를 사용합니다.
자세한 내용은 [진행 중인 작업 취소](/doc/database/cancel-operations)를 참조하십시오.

다음 예제는 지정된 아티스트의 앨범을 검색하는 쿼리를 실행합니다. 앨범은 `sql.Rows` 형식으로 반환됩니다. 이 코드는 `[`Rows.Scan`](https://pkg.go.dev/database/sql#Rows.Scan)를 사용하여 열 값을 포인터로 표현된 변수에 복사합니다.

```
func albumsByArtist(artist string) ([]Album, error) {
	rows, err := db.Query("SELECT * FROM album WHERE artist = ?", artist)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	// Album 정보를 담을 슬라이스.
	var albums []Album

	// 각 행을 순회하며, Scan 함수를 사용하여 컬럼 데이터를 구조체 필드에 할당.
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

참고: [`rows.Close`](https://pkg.go.dev/database/sql#Rows.Close)를 사용하여 `rows`를 닫는 것을 잊지 마십시오.
이것은 함수가 어떤 방식으로든 반환되더라도 `rows`가 사용하는 모든 리소스를 해제합니다. `rows`를 반복하여 닫는 것도 가능하지만, `defer`를 사용하면 `rows`가 항상 닫히도록 할 수 있습니다.

**참고:** 준비된 문(prepared statement)의 파라미터 자리표는 사용 중인 DBMS 및 드라이버에 따라 다릅니다. 예를 들어, Postgres용 [pq 드라이버](https://pkg.go.dev/github.com/lib/pq)는 `$1`과 같은 자리표를 사용해야 하지만, `?`를 사용하지 않습니다.

#### 오류 처리 {#multiple_rows_오류}

쿼리 결과에 대한 반복 후 `sql.Rows`에서 오류를 확인하십시오.
쿼리가 실패한 경우, 코드가 이를 어떻게 확인하는지 보여줍니다.

#### 여러 행을 반환하는 함수 {#multiple_rows_functions}

```markdown
<table id="multiple-row-functions-list" class="DocTable">
  <thead>
    <tr class="DocTable-head">
      <th class="DocTable-cell" width="20%">기능</th>
      <th class="DocTable-cell">설명</th>
    </tr>
  </thead>
  <tbody>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#DB.Query">DB.Query</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#DB.QueryContext">DB.QueryContext</a></code>
      </td>
      <td class="DocTable-cell">격리된 쿼리를 실행합니다.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Tx.Query">Tx.Query</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#Tx.QueryContext">Tx.QueryContext</a></code>
      </td>
      <td class="DocTable-cell">더 큰 트랜잭션 내에서 쿼리를 실행합니다. 자세한 내용은 "트랜잭션 실행"을 참조하십시오.
        <a href="/doc/database/execute-transactions">Executing transactions</a>.
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Stmt.Query">Stmt.Query</a></code><br />
        <code><a href="https://pkg.go.dev/database/sql#Stmt.QueryContext">Stmt.QueryContext</a></code>
      </td>
      <td class="DocTable-cell">이미 준비된 상태를 사용하여 쿼리를 실행합니다. 자세한 내용은 "준비된 상태 사용"을 참조하십시오.
        <a href="/doc/database/prepared-statements">Using prepared
          statements</a>.
    </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Conn.QueryContext">Conn.QueryContext</a></code>
      </td>
      <td class="DocTable-cell">예약된 연결을 사용하는 데 사용합니다. 자세한 내용은 "연결 관리"를 참조하십시오.
        <a href="/doc/database/manage-connections">Managing connections</a>.
      </td>
    </tr>
  </tbody>
</table>

### NULL 값 처리하는 열 {#nullable_columns}

`database/sql` 패키지는 `Scan` 함수에 인수로 사용할 수 있는 여러 특별한 유형을 제공합니다. 이러한 유형은 열의 값이 null일 수 있는 경우에 사용할 수 있습니다. 각 유형에는 `Valid` 필드가 포함되어 있으며, 이는 값이 null이 아닌지 여부를 보고하고, 값이 null인 경우 해당 값을 저장하는 필드를 포함합니다.

다음 예제에서 코드는 고객 이름을 쿼리합니다. 만약 이름 값이 null이면, 코드는 애플리케이션에서 사용할 다른 값을 대체합니다.

```
var s sql.NullString
err := db.QueryRow("SELECT name FROM customer WHERE id = ?", id).Scan(&s)
if err != nil {
	log.Fatal(err)
}

// 고객 이름 찾기, 이름이 없는 경우 플레이스홀더 사용.
name := "Valued Customer"
if s.Valid {
	name = s.String
}
```

자세한 내용은 `sql` 패키지의 참조 문서를 참조하세요:

*   [`NullBool`](https://pkg.go.dev/database/sql#NullBool)
*   [`NullFloat64`](https://pkg.go.dev/database/sql#NullFloat64)
*   [`NullInt32`](https://pkg.go.dev/database/sql#NullInt32)
*   [`NullInt64`](https://pkg.go.dev/database/sql#NullInt64)
*   [`NullString`](https://pkg.go.dev/database/sql#NullString)
*   [`NullTime`](https://pkg.go.dev/database/sql#NullTime)

### 열에서 데이터 가져오기 {#column_data}

쿼리에서 반환된 행을 반복할 때, `Scan` 함수를 사용하여 행의 열 값을 Go 변수에 복사합니다. 이는 [`Rows.Scan`](https://pkg.go.dev/database/sql#Rows.Scan) 참조에 설명된 대로입니다.

다음과 같은 모든 드라이버에서 지원되는 기본 데이터 변환이 있습니다. 예를 들어, SQL의 `INT`를 Go의 `int`로 변환하는 것입니다. 일부 드라이버는 이러한 변환 세트를 확장합니다. 자세한 내용은 각 드라이버의 문서를 참조하십시오.

물론, `Scan`은 열의 데이터 유형을 유사한 Go 유형으로 변환합니다. 예를 들어, `Scan`은 SQL의 `CHAR`, `VARCHAR` 및 `TEXT`를 Go의 `string`으로 변환합니다. 그러나 `Scan`은 열 값에 적합한 다른 Go 유형으로도 변환할 수 있습니다. 예를 들어, 열이 항상 숫자를 포함하는 `VARCHAR`인 경우, `int`와 같은 숫자 Go 유형을 지정하여 값을 받을 수 있으며, `Scan`은 `strconv.Atoi`를 사용하여 변환합니다.

자세한 내용은 `Scan` 함수의 변환에 대해 [`Rows.Scan`](https://pkg.go.dev/database/sql#Rows.Scan) 참조를 참조하세요.

### 여러 결과 집합 처리 {#multiple_result_sets}

데이터베이스 작업이 여러 결과 집합을 반환할 때, 다음을 사용하여
그 결과를 가져올 수 있습니다:
[`Rows.NextResultSet`](https://pkg.go.dev/database/sql#Rows.NextResultSet).
이는 특히, 여러 테이블에 대해 개별적으로 쿼리를 실행하고, 각 쿼리의 결과 집합을 반환하는 경우에 유용할 수 있습니다.

`Rows.NextResultSet`는 다음 결과 세트를 준비하여 `Rows.Next` 호출을 통해 해당 세트의 첫 번째 행을 가져옵니다. 다음 결과 세트가 존재하는지 여부를 나타내는 부울 값을 반환합니다.

다음 예제에서 코드는 `DB.Query`를 사용하여 두 개의 SQL 문을 실행합니다.
첫 번째 결과 세트는 프로시저의 첫 번째 쿼리에서 생성되며, `album` 테이블의 모든 행을 검색합니다. 다음 결과 세트는 두 번째 쿼리에서 생성되며, `song` 테이블의 행을 검색합니다.

```
rows, err := db.Query("SELECT * from album; SELECT * from song;")
if err != nil {
	log.Fatal(err)
}
defer rows.Close()

// 첫 번째 결과 집합을 반복합니다.
for rows.Next() {
	// 결과 집합을 처리합니다.
}

// 다음 결과 집합으로 이동합니다.
rows.NextResultSet()

// 두 번째 결과 집합을 반복합니다.
for rows.Next() {
	// 두 번째 집합을 처리합니다.
}

// 두 결과 집합 중 어느 것에든 오류가 있는지 확인합니다.
if err := rows.Err(); err != nil {
	log.Fatal(err)
}
```
