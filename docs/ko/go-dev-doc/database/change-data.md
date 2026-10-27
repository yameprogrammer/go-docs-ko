<!--{
  "제목": "데이터를 반환하지 않는 SQL 문 실행"
}-->

데이터를 반환하지 않는 데이터베이스 작업을 수행할 때는 `database/sql` 패키지의 `Exec` 또는 `ExecContext` 메서드를 사용하십시오. 이러한 방식으로 실행할 SQL 문은 `INSERT`, `DELETE` 및 `UPDATE` 등이 포함됩니다.

쿼리가 행을 반환할 수 있는 경우, `Query` 또는 `QueryContext` 메서드를 사용하세요. 자세한 내용은 [데이터베이스 쿼리](/doc/database/querying)를 참조하세요.

`ExecContext` 메서드는 `Exec` 메서드와 유사하게 작동하지만, [실행 중인 작업 취소](/doc/database/cancel-operations)에서 설명된 대로 추가적인 `context.Context` 인수를 사용합니다.

다음 예제에서 사용된 코드는
[`DB.Exec`](https://pkg.go.dev/database/sql#DB.Exec)를 사용하여 `album` 테이블에 새 레코드 앨범을 추가하는 문을 실행합니다.

```
func AddAlbum(alb Album) (int64, error) {
	result, err := db.Exec("INSERT INTO album (title, artist) VALUES (?, ?)", alb.Title, alb.Artist)
	if err != nil {
		return 0, fmt.Errorf("AddAlbum: %v", err)
	}

	// 클라이언트에 새 앨범의 생성된 ID를 가져옵니다.
	id, err := result.LastInsertId()
	if err != nil {
		return 0, fmt.Errorf("AddAlbum: %v", err)
	}
	// 새 앨범의 ID를 반환합니다.
	return id, nil
}
```

`DB.Exec`는 값을 반환합니다: `[sql.Result](https://pkg.go.dev/database/sql#Result)`
와 오류. 오류가 `nil`인 경우, `Result`를 사용하여 마지막 삽입된 항목의 ID를 얻거나, 작업에 의해 영향을 받은 행 수를 검색할 수 있습니다 (예제와 같이).

**참고:** 준비된 문(prepared statement)의 파라미터 자리표는 사용하는 DBMS 및 드라이버에 따라 다릅니다. 예를 들어, Postgres에 사용되는 [pq 드라이버](https://pkg.go.dev/github.com/lib/pq)는 `?` 대신 `$1`과 같은 자리표를 필요로 합니다.

만약 코드가 동일한 SQL 문을 반복적으로 실행해야 한다면, 재사용 가능한 준비된 문을 만들기 위해 `sql.Stmt`를 사용하는 것을 고려해 보세요. 자세한 내용은 [준비된 문 사용](/doc/database/prepared-statements)를 참조하세요.

**주의:** `fmt.Sprintf`와 같은 문자열 포맷팅 함수를 사용하여 SQL 문을 구성하지 마세요! SQL 삽입 위험을 초래할 수 있습니다.
자세한 내용은 [SQL 삽입 위험 방지](/doc/database/sql-injection)를 참조하세요.

#### 행을 반환하지 않는 SQL 문 실행 함수 {#no_rows_functions}

```markdown
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
      <td class="DocTable-cell">격리된 상태에서 단일 SQL 문을 실행합니다.</td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Tx.Exec">Tx.Exec</a></code><br/>
        <code><a href="https://pkg.go.dev/database/sql#Tx.ExecContext">Tx.ExecContext</a></code>
      </td>
      <td class="DocTable-cell">더 큰 트랜잭션 내에서 SQL 문을 실행합니다. 자세한 내용은 다음을 참조하세요:
          <a href="/doc/database/execute-transactions">트랜잭션 실행</a>.
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Stmt.Exec">Stmt.Exec</a></code><br/>
        <code><a href="https://pkg.go.dev/database/sql#Stmt.ExecContext">Stmt.ExecContext</a></code>
      </td>
      <td class="DocTable-cell">이미 준비된 SQL 문을 실행합니다. 자세한 내용은 다음을 참조하세요:
          <a href="/doc/database/prepared-statements">준비된 문 사용</a>.
      </td>
    </tr>
    <tr class="DocTable-row">
      <td class="DocTable-cell">
        <code><a href="https://pkg.go.dev/database/sql#Conn.ExecContext">Conn.ExecContext</a></code>
      </td>
      <td class="DocTable-cell">예약된 연결에 사용합니다. 자세한 내용은 다음을 참조하세요:
          <a href="/doc/database/manage-connections">연결 관리</a>.
      </td>
    </tr>
  </tbody>
</table
