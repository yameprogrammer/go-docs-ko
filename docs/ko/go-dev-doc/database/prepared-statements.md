<!--{
  "Title": "Prepared statement 사용하기"
}-->

반복해서 사용할 수 있도록 준비된 문장(prepared statement)을 정의할 수 있습니다. 이렇게 하면 코드가 데이터베이스 작업을 수행할 때마다 문장을 다시 생성하는 오버헤드를 피할 수 있어 코드 실행 속도를 다소 높일 수 있습니다.

**참고:** 준비된 문장(prepared statements)의 파라미터 플레이스홀더는 사용하는 DBMS와 드라이버에 따라 다릅니다. 예를 들어, Postgres용 [pq driver](https://pkg.go.dev/github.com/lib/pq)는 `?` 대신 `$1`과 같은 플레이스홀더를 사용해야 합니다.

### Prepared statement란 무엇인가요? {#what_prepared_statement}

준비된 문장(Prepared statement)은 DBMS에 의해 파싱되고 저장되는 SQL로, 일반적으로 실제 매개변수 값 대신 플레이스홀더(placeholder)를 포함하고 있습니다. 이후, 이 문장은 일련의 매개변수 값과 함께 실행될 수 있습니다.

### prepared statements 사용 방법 {#use_prepared_statement}

동일한 SQL을 반복적으로 실행해야 하는 경우, `sql.Stmt`를 사용하여 SQL 문을 미리 준비(prepare)한 다음 필요할 때마다 실행할 수 있습니다.

다음 예제는 데이터베이스에서 특정 앨범을 선택하는 prepared statement를 생성합니다. [`DB.Prepare`](https://pkg.go.dev/database/sql#DB.Prepare)는 주어진 SQL 텍스트에 대한 prepared statement를 나타내는 [`sql.Stmt`](https://pkg.go.dev/database/sql#Stmt)를 반환합니다. `Stmt.Exec`, `Stmt.QueryRow` 또는 `Stmt.Query`에 SQL 문을 위한 파라미터를 전달하여 해당 문을 실행할 수 있습니다.

```go
// AlbumByID는 지정된 앨범을 검색합니다.
func AlbumByID(id int) (Album, error) {
	// 준비된 문장(prepared statement)을 정의합니다. 일반적으로 문장은
	// 다른 곳에서 정의하고 이와 같은 함수에서 사용할 수 있도록 저장합니다.
	stmt, err := db.Prepare("SELECT * FROM album WHERE id = ?")
	if err != nil {
		log.Fatal(err)
	}
	defer stmt.Close()

	var album Album

	// 준비된 문장을 실행하며, 플레이스홀더인 ?에 해당하는 
	// id 값을 전달합니다.
	err := stmt.QueryRow(id).Scan(&album.ID, &album.Title, &album.Artist, &album.Price, &album.Quantity)
	if err != nil {
		if err == sql.ErrNoRows {
			// 행이 반환되지 않은 경우를 처리합니다.
		}
		return album, err
	}
	return album, nil
}
```

### Prepared statement 동작 방식 {#behavior}

준비된 [`sql.Stmt`](https://pkg.go.dev/database/sql#Stmt)는 문장을 호출하기 위한 일반적인 `Exec`, `QueryRow`, `Query` 메서드를 제공합니다. 이 메서드들의 사용법에 대한 자세한 내용은 [데이터 쿼리하기](/doc/database/querying) 및 [데이터를 반환하지 않는 SQL 문 실행하기](/doc/database/change-data)를 참조하십시오.

하지만 `sql.Stmt`는 이미 미리 설정된 SQL 문을 나타내므로, `Exec`, `QueryRow`, `Query` 메서드는 SQL 텍스트를 생략하고 플레이스홀더에 해당하는 SQL 파라미터 값만 인자로 받습니다.

`sql.Stmt`를 정의하는 방법은 사용 용도에 따라 여러 가지가 있습니다.

*   `DB.Prepare`와 `DB.PrepareContext`는 `DB.Exec` 및 `DB.Query`와 마찬가지로 트랜잭션 외부에서 독립적으로 실행될 수 있는 준비된 문장(prepared statement)을 생성합니다.
*   `Tx.Prepare`, `Tx.PrepareContext`, `Tx.Stmt`, 그리고 `Tx.StmtContext`는 특정 트랜잭션 내에서 사용할 준비된 문장을 생성합니다. `Prepare`와 `PrepareContext`는 SQL 텍스트를 사용하여 문장을 정의합니다. `Stmt`와 `StmtContext`는 `DB.Prepare` 또는 `DB.PrepareContext`의 결과물을 사용합니다. 즉, 트랜잭션용이 아닌 `sql.Stmt`를 해당 트랜잭션 전용 `sql.Stmt`로 변환합니다.
*   `Conn.PrepareContext`는 예약된 연결을 나타내는 `sql.Conn`으로부터 준비된 문장을 생성합니다.

코드가 statement 사용을 마쳤을 때 `stmt.Close`가 호출되었는지 확인하십시오. 이렇게 하면 해당 statement와 연결된 모든 데이터베이스 리소스(기본 연결 등)가 해제됩니다. 함수의 지역 변수로만 사용되는 statement의 경우, `defer stmt.Close()`를 사용하는 것으로 충분합니다.

#### 준비된 문장(prepared statement) 생성을 위한 함수 {#prepared_statement_functions}

<table id="prepared-statement-functions-list" class="DocTable">
    <thead>
        <tr class="DocTable-head">
            <th class="DocTable-cell" width="20%">함수</th>
            <th class="DocTable-cell">설명</th>
        </tr>
    </thead>
    <tbody>
        <tr class="DocTable-row">
            <td class="DocTable-cell">
                <code><a href="https://pkg.go.dev/database/sql#DB.Prepare">DB.Prepare</a></code><br />
                <code><a href="https://pkg.go.dev/database/sql#DB.PrepareContext">DB.PrepareContext</a></code>
            </td>
            <td class="DocTable-cell">독립적으로 실행하거나, <code>Tx.Stmt</code>를 사용하여 트랜잭션 내의 준비된 문장(prepared statement)으로 변환될 문장을 준비합니다.</td>
        </tr>
        <tr class="DocTable-row">
            <td class="DocTable-cell">
                <code><a href="https://pkg.go.dev/database/sql#Tx.Prepare">Tx.Prepare</a></code><br />
                <code><a href="https://pkg.go.dev/database/sql#Tx.PrepareContext">Tx.PrepareContext</a></code><br />
                <code><a href="https://pkg.go.dev/database/sql#Tx.Stmt">Tx.Stmt</a></code><br />
                <code><a href="https://pkg.go.dev/database/sql#Tx.StmtContext">Tx.StmtContext</a></code>
            </td>
            <td class="DocTable-cell">특정 트랜잭션에서 사용할 문장을 준비합니다. 자세한 내용은 <a href="/doc/database/execute-transactions">트랜잭션 실행(Executing transactions)</a>을 참조하십시오.
            </td>
        </tr>
        <tr class="DocTable-row">
            <td class="DocTable-cell">
                <code><a href="https://pkg.go.dev/database/sql#Conn.PrepareContext">Conn.PrepareContext</a></code>
            </td>
            <td class="DocTable-cell">예약된 연결(reserved connections)과 함께 사용합니다. 자세한 내용은 <a href="/doc/database/manage-connections">연결 관리(Managing connections)</a>를 참조하십시오.
            </td>
        </tr>
    </tbody>
</table>
