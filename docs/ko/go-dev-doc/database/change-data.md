<!--{
  "Title": "데이터를 반환하지 않는 SQL 문 실행하기"
}-->

데이터를 반환하지 않는 데이터베이스 작업을 수행할 때는 `database/sql` 패키지의 `Exec` 또는 `ExecContext` 메서드를 사용하세요. 이런 방식으로 실행하는 SQL 문에는 `INSERT`, `DELETE`, `UPDATE` 등이 포함됩니다.

쿼리가 행(rows)을 반환할 가능성이 있는 경우에는 대신 `Query` 또는 `QueryContext` 메서드를 사용하세요. 자세한 내용은 [데이터베이스 쿼리하기](/doc/database/querying)를 참조하세요.

`ExecContext` 메서드는 `Exec` 메서드와 동일하게 작동하지만, [진행 중인 작업 취소하기](/doc/database/cancel-operations)에 설명된 것과 같이 추가적인 `context.Context` 인자를 갖습니다.

다음 예제의 코드는 [`DB.Exec`](https://pkg.go.dev/database/sql#DB.Exec)를 사용하여 `album` 테이블에 새로운 레코드 앨범을 추가하는 문장을 실행합니다.

```go
func AddAlbum(alb Album) (int64, error) {
	result, err := db.Exec("INSERT INTO album (title, artist) VALUES (?, ?)", alb.Title, alb.Artist)
	if err != nil {
		return 0, fmt.Errorf("AddAlbum: %v", err)
	}

	// 클라이언트를 위해 생성된 새 앨범의 ID를 가져옵니다.
	id, err := result.LastInsertId()
	if err != nil {
		return 0, fmt.Errorf("AddAlbum: %v", err)
	}
	// 새 앨범의 ID를 반환합니다.
	return id, nil
}
```

`DB.Exec`은 [`sql.Result`](https://pkg.go.dev/database/sql#Result)와 error 값을 반환합니다. error가 `nil`인 경우, `Result`를 사용하여 마지막으로 삽입된 항목의 ID를 가져오거나(예제와 같이) 작업에 의해 영향을 받은 행의 수를 조회할 수 있습니다.

**참고:** 준비된 문장(prepared statements)의 파라미터 플레이스홀더는 사용하는 DBMS와 드라이버에 따라 다릅니다. 예를 들어, Postgres용 [pq driver](https://pkg.go.dev/github.com/lib/pq)는 `?` 대신 `$1`과 같은 플레이스홀더를 사용해야 합니다.

코드가 동일한 SQL 문을 반복적으로 실행하는 경우, `sql.Stmt`를 사용하여 해당 SQL 문으로부터 재사용 가능한 준비된 문장(prepared statement)을 생성하는 것을 고려하십시오. 자세한 내용은 [Using prepared statements](/doc/database/prepared-statements)를 참조하십시오.

**주의:** SQL 문을 구성할 때 `fmt.Sprintf`와 같은 문자열 포맷팅 함수를 사용하지 마십시오! SQL 인젝션 위험이 발생할 수 있습니다.
자세한 내용은 [SQL 인젝션 위험 방지](/doc/database/sql-injection)를 참조하십시오.

#### 행을 반환하지 않는 SQL 문을 실행하기 위한 함수 {#no_rows_functions}

<table id="no-rows-functions-list" class="DocTable">
  <thead>
    <tr class="DocTable-head">
      <th class="DocTable-cell" width="20%">함수</th>
      <th class="DocTable-cell">설명</th>
    </tr>
  </thead>
  <tbody>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#DB.Exec">DB.Exec</a></code><br/>
        <code><a href="https://pkg.go.dev/database/sql#DB.ExecContext">DB.ExecContext</a></code>
      </td>
      <td class="DocTable-cell">단일 SQL 문을 독립적으로 실행합니다.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Tx.Exec">Tx.Exec</a></code><br/>
        <code><a href="https://pkg.go.dev/database/sql#Tx.ExecContext">Tx.ExecContext</a></code>
      </td>
      <td class="DocTable-cell">더 큰 트랜잭션 내에서 SQL 문을 실행합니다. 자세한 내용은
          <a href="/doc/database/execute-transactions">트랜잭션 실행(Executing transactions)</a>을 참조하십시오.
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Stmt.Exec">Stmt.Exec</a></code><br/>
        <code><a href="https://pkg.go.dev/database/sql#Stmt.ExecContext">Stmt.ExecContext</a></code>
      </td>
      <td class="DocTable-cell">이미 준비된(prepared) SQL 문을 실행합니다. 자세한 내용은
          <a href="/doc/database/prepared-statements">준비된 문장 사용(Using prepared statements)</a>을 참조하십시오.
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Conn.ExecContext">Conn.ExecContext</a></code>
      </td>
      <td class="DocTable-cell">예약된 연결(reserved connections)과 함께 사용합니다. 자세한 내용은
          <a href="/doc/database/manage-connections">연결 관리(Managing connections)</a>를 참조하십시오.
      </td>
    </tr>
  </tbody>
</table>
