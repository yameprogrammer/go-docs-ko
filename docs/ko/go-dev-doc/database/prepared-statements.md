<!--{
  "제목": "준비된 문(Prepared Statements) 사용하기"
}-->

반복적으로 사용할 수 있도록 준비된 문을 정의할 수 있습니다. 이를 통해 코드가 데이터베이스 작업을 수행할 때마다 문을 다시 생성하는 오버헤드를 줄여 코드가 약간 더 빠르게 실행되도록 할 수 있습니다.

**참고:** 준비된 문(prepared statements)의 파라미터 대체자는 사용하는 DBMS 및 드라이버에 따라 다릅니다. 예를 들어, [pq 드라이버](https://pkg.go.dev/github.com/lib/pq) (Postgres용)는 `?` 대신 `$1`과 같은 대체자를 사용해야 합니다.

### 준비된 쿼리란 무엇인가? {#what_prepared_statement}

```sql
-- 예시:
SELECT * FROM users WHERE id = $id AND email = $email;
```

Prepared statement은 SQL 쿼리를 미리 정의하고, 그 정의된 쿼리에 값을 대입하여 실행하는 방식입니다. 이를 통해 SQL Injection과 같은 보안 취약점을 방지할 수 있습니다.

준비된 문은 DBMS에 의해 파싱되고 저장되는 SQL이며, 일반적으로 대체자를 포함하지만 실제 매개변수 값을 포함하지 않습니다. 이후, 해당 문은 일련의 매개변수 값과 함께 실행될 수 있습니다.

### 준비된 문을 사용하는 방법 {#use_prepared_statement}

```sql
-- 예시: 데이터베이스에 'user'라는 이름과 'example@example.com' 이메일 주소를 가진 새 사용자를 추가합니다.
PREPARE AddUserStmt FROM 'INSERT INTO users (name, email) VALUES (?, ?)';
SET @name = 'user';
SET @email = 'example@example.com';
EXECUTE AddUserStmt;
DEALLOCATE PREPARE AddUserStmt;
```

## 주의사항

*   준비된 문은 여러 번 실행할 수 있습니다.
*   각 실행 시 다른 값으로 괄호 안에 있는 플레이스홀더를 바꿀 수 있습니다.
*   준비된 문은 SQL Injection 공격으로부터 보호하는 데 도움이 됩니다.

`sql.Stmt`를 사용하여 동일한 SQL 쿼리를 반복적으로 실행할 때, SQL 쿼리를 미리 준비하고 필요에 따라 실행할 수 있습니다.

다음 예시는 데이터베이스에서 특정 앨범을 선택하는 준비된 문을 생성합니다. [`DB.Prepare`](https://pkg.go.dev/database/sql#DB.Prepare)는 주어진 SQL 텍스트에 대한 준비된 문을 나타내는 [`sql.Stmt`](https://pkg.go.dev/database/sql#Stmt)를 반환합니다. SQL 문에 대한 매개 변수를 `Stmt.Exec`, `Stmt.QueryRow` 또는 `Stmt.Query`에 전달하여 문을 실행할 수 있습니다.

```markdown
// AlbumByID는 지정된 앨범을 가져옵니다.
func AlbumByID(id int) (Album, error) {
	// 쿼리문을 정의합니다. 일반적으로 이와 같은 함수에서 쿼리문을 정의하고 저장하여 재사용합니다.
	stmt, err := db.Prepare("SELECT * FROM album WHERE id = ?")
	if err != nil {
		log.Fatal(err)
	}
	defer stmt.Close()

	var album Album

	// 준비된 쿼리문을 실행하고, ? 플레이스 홀더에 id 값을 전달합니다.
	err := stmt.QueryRow(id).Scan(&album.ID, &album.Title, &album.Artist, &album.Price, &album.Quantity)
	if err != nil {
		if err == sql.ErrNoRows {
			// 결과가 없는 경우를 처리합니다.
		}
		return album, err
	}
	return album, nil
}
```

### 준비된 문(Prepared Statement) 동작 방식 {#behavior}

```
prepared statement
```

준비된 [`sql.Stmt`](https://pkg.go.dev/database/sql#Stmt)는 문을 실행하기 위한
일반적인 `Exec`, `QueryRow`, 및 `Query` 메서드를 제공합니다.
이 메서드를 사용하는 방법에 대한 자세한 내용은 [데이터 쿼리](/doc/database/querying) 및
[데이터를 반환하지 않는 SQL 문 실행](/doc/database/change-data)를 참조하십시오.

하지만, `sql.Stmt`는 이미 설정된 SQL 문을 나타내므로, `Exec`, `QueryRow` 및 `Query` 메서드는 SQL 텍스트를 제외하고, 플레이스홀더에 해당하는 SQL 매개변수 값만 사용합니다.

다양한 방식으로 새 `sql.Stmt`를 정의할 수 있으며, 이는 사용 방법에 따라 달라집니다.

*   `DB.Prepare` 및 `DB.PrepareContext`는 트랜잭션 외부에서 격리된 방식으로 실행할 수 있는 준비된 문을 생성합니다. 이는 `DB.Exec` 및 `DB.Query`와 유사합니다.
*   `Tx.Prepare`, `Tx.PrepareContext`, `Tx.Stmt`, 및 `Tx.StmtContext`는 특정 트랜잭션에서 사용할 준비된 문을 생성합니다. `Prepare` 및 `PrepareContext`는 SQL 텍스트를 사용하여 문을 정의합니다. `Stmt` 및 `StmtContext`는 `DB.Prepare` 또는 `DB.PrepareContext`의 결과를 사용합니다. 즉, 트랜잭션에 적합하지 않은 `sql.Stmt`를 현재 트랜잭션에 적합한 `sql.Stmt`로 변환합니다.
*   `Conn.PrepareContext`는 예약된 연결을 나타내는 `sql.Conn`에서 준비된 문을 생성합니다.

`stmt.Close`를 호출하여, 코드가 특정 문과 작업을 마치면 반드시 호출해야 합니다. 이렇게 하면 해당 문과 관련된 모든 데이터베이스 리소스 (예: 기본 연결)를 해제할 수 있습니다. 함수 내에서만 사용되는 변수(문)의 경우, `defer stmt.Close()`를 사용하는 것으로 충분합니다.

#### 준비된 문을 만드는 함수 {#prepared_statement_functions}

```markdown
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
                <code><a href="https://pkg.go.dev/database/sql#DB.Prepare">DB.Prepare</a><br />
                <code><a href="https://pkg.go.dev/database/sql#DB.PrepareContext">DB.PrepareContext</a></code>
            </td>
            <td class="DocTable-cell">실행을 위해 구문(statement)을 준비하거나, Tx.Stmt를 사용하여 트랜잭션 내에서 사용될 구문으로 변환합니다.</td>
        </tr>
        <tr class="DocTable-row">
            <td class="DocTable-cell">
                <code><a href="https://pkg.go.dev/database/sql#Tx.Prepare">Tx.Prepare</a><br />
                <code><a href="https://pkg.go.dev/database/sql#Tx.PrepareContext">Tx.PrepareContext</a><br />
                <code><a href="https://pkg.go.dev/database/sql#Tx.Stmt">Tx.Stmt</a><br />
                <code><a href="https://pkg.go.dev/database/sql#Tx.StmtContext">Tx.StmtContext</a></code>
            </td>
            <td class="DocTable-cell">특정 트랜잭션에서 사용할 구문을 준비합니다. 자세한 내용은 <a href="/doc/database/execute-transactions">트랜잭션 실행</a>을 참조하십시오.</td>
        </tr>
        <tr class="DocTable-row">
            <td class="DocTable-cell">
                <code><a href="https://pkg.go.dev/database/sql#Conn.PrepareContext">Conn.PrepareContext</a></code>
            </td>
            <td class="DocTable-cell">예약된 연결을 사용하기 위한 용도입니다. 자세한 내용은 <a href="/doc/database/manage-connections">연결 관리</a>를 참조하십시오.</td>
        </tr>
    </tbody>
</table>
```
