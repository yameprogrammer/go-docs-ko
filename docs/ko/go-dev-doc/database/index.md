<!--{
  "Title": "관계형 데이터베이스 액세스",
  "Breadcrumb": true
}-->

# 관계형 데이터베이스 액세스

관계형 데이터베이스(RDBMS)를 사용하면 데이터를 구조화된 테이블 형식으로 저장하고 관리할 수 있습니다. Go에서는 `database/sql` 표준 패키지를 통해 데이터베이스와 상호작용하는 일반적인 인터페이스를 제공합니다.

## 데이터베이스 드라이버

`database/sql` 패키지는 범용 인터페이스만 제공하며, 실제 데이터베이스와의 통신을 위해서는 특정 데이터베이스에 맞는 **드라이버(driver)**가 필요합니다.

인기 있는 Go 데이터베이스 드라이버는 다음과 같습니다:
- **PostgreSQL**: `github.com/lib/pq` 또는 `github.com/jackc/pgx`
- **MySQL**: `github.com/go-sql-driver/mysql`
- **SQLite**: `github.com/mattn/go-sqlite3`

## 연결 설정

데이터베이스에 연결하려면 드라이버를 임포트하고 `sql.Open` 함수를 사용해야 합니다.

```go
import (
    "database/sql"
    _ "github.com/lib/pq" // 드라이버를 사이드 이펙트로 임포트
)

func main() {
    connStr := "user=pqgotest dbname=pqgotest sslmode=disable"
    db, err := sql.Open("postgres", connStr)
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()
}
```

## 쿼리 실행

### 데이터 읽기 (SELECT)

단일 행을 가져오려면 `QueryRow`를, 여러 행을 가져오려면 `Query`를 사용합니다.

```go
var name string
var age int
err := db.QueryRow("SELECT name, age FROM users WHERE id = $1", 1).Scan(&name, &age)
```

### 데이터 수정 (INSERT, UPDATE, DELETE)

결과 집합을 반환하지 않는 작업에는 `Exec`를 사용합니다.

```go
res, err := db.Exec("UPDATE users SET age = $1 WHERE name = $2", 30, "John Doe")
if err != nil {
    log.Fatal(err)
}

count, _ := res.RowsAffected()
fmt.Printf("Updated %d rows\n", count)
```

## 트랜잭션 관리

데이터 일관성을 유지하기 위해 `db.Begin()`을 사용하여 트랜잭션을 시작할 수 있습니다.

| 메서드 | 설명 |
| :--- | :--- |
| `Begin()` | 새로운 트랜잭션을 시작합니다. |
| `Commit()` | 트랜잭션의 모든 변경 사항을 확정합니다. |
| `Rollback()` | 트랜잭션을 취소하고 이전 상태로 되돌립니다. |

## 보안 주의사항: SQL 인젝션 방지

절대로 사용자 입력을 문자열 포맷팅(예: `fmt.Sprintf`)을 통해 쿼리에 직접 넣지 마십시오. 대신 **매개변수화된 쿼리(Parameterized Queries)**를 사용하십시오.

**잘못된 방법 (위험):**
```go
// SQL 인젝션에 취약함
query := fmt.Sprintf("SELECT * FROM users WHERE name = '%s'", userInput)
```

**올바른 방법 (안전):**
```go
// 드라이버가 안전하게 이스케이프 처리를 수행함
db.Query("SELECT * FROM users WHERE name = $1", userInput)
```

Go를 사용하면 애플리케이션에 매우 다양한 데이터베이스와 데이터 액세스 방식을 통합할 수 있습니다. 이 섹션의 주제들은 관계형 데이터베이스에 액세스하기 위해 표준 라이브러리의 [`database/sql`](https://pkg.go.dev/database/sql) 패키지를 사용하는 방법을 설명합니다.

Go를 이용한 데이터 액세스 입문 튜토리얼은
[Tutorial: Accessing a relational database](/doc/tutorial/database-access)를 참조하시기 바랍니다.

Go는 관계형 데이터베이스에 대한 상위 수준의 액세스를 위한 ORM 라이브러리와 비관계형 NoSQL 데이터 저장소를 포함하여 다른 데이터 액세스 기술도 지원합니다.

*   **객체 관계 매핑(ORM) 라이브러리.** `database/sql` 패키지는 하위 수준의 데이터 액세스 로직을 위한 함수들을 포함하고 있지만, 더 높은 추상화 수준에서 데이터 저장소에 액세스하기 위해 Go를 사용할 수도 있습니다. Go에서 인기 있는 두 가지 객체 관계 매핑(ORM) 라이브러리에 대한 자세한 내용은 [GORM](https://gorm.io/index.html) ([패키지 참조](https://pkg.go.dev/gorm.io/gorm)) 및 [ent](https://entgo.io/) ([패키지 참조](https://pkg.go.dev/entgo.io/ent))를 참조하세요.
*   **NoSQL 데이터 저장소.** Go 커뮤니티는 [MongoDB](https://docs.mongodb.com/drivers/go/) 및 [Couchbase](https://docs.couchbase.com/go-sdk/current/hello-world/overview.html)를 포함하여 대부분의 NoSQL 데이터 저장소를 위한 드라이버를 개발해 왔습니다. 더 많은 정보는 [pkg.go.dev](https://pkg.go.dev/)에서 검색할 수 있습니다.

### 지원되는 데이터베이스 관리 시스템 {#supported_dbms}

Go는 MySQL, Oracle, Postgres, SQL Server, SQLite를 포함하여 가장 일반적인 모든 관계형 데이터베이스 관리 시스템을 지원합니다.

전체 드라이버 목록은 [SQLDrivers](/wiki/SQLDrivers) 페이지에서 확인하실 수 있습니다.

### 쿼리를 실행하거나 데이터베이스 변경을 수행하는 함수 {#functions}

`database/sql` 패키지에는 실행하려는 데이터베이스 작업의 종류에 따라 특별히 설계된 함수들이 포함되어 있습니다. 예를 들어, 쿼리를 실행하기 위해 `Query`나 `QueryRow`를 사용할 수 있지만, `QueryRow`는 단 하나의 행(row)만 예상하는 경우를 위해 설계되었으며, 단 하나의 행만 포함된 `sql.Rows`를 반환하는 오버헤드를 생략합니다. `INSERT`, `UPDATE` 또는 `DELETE`와 같은 SQL 문으로 데이터베이스 변경 사항을 적용하려면 `Exec` 함수를 사용할 수 있습니다.

더 자세한 내용은 다음을 참조하십시오.

*   [데이터를 반환하지 않는 SQL 문 실행하기](/doc/database/change-data)
*   [데이터 쿼리하기](/doc/database/querying)

### Transactions {#transactions}

`sql.Tx`를 통해 데이터베이스 작업을 트랜잭션으로 실행하는 코드를 작성할 수 있습니다. 트랜잭션 내에서는 여러 작업을 함께 수행할 수 있으며, 모든 변경 사항을 하나의 원자적 단계로 적용하기 위한 최종 commit 또는 변경 사항을 폐기하기 위한 rollback으로 마무리합니다.

트랜잭션에 대한 자세한 내용은 [트랜잭션 실행](/doc/database/execute-transactions)을 참조하세요.

### 쿼리 취소 {#query_cancellation}

클라이언트의 연결이 종료되거나 작업이 예상보다 오래 실행되는 경우와 같이, 데이터베이스 작업을 취소할 수 있는 기능이 필요할 때 `context.Context`를 사용할 수 있습니다.

모든 데이터베이스 작업에 대해 `Context`를 인자로 받는 `database/sql` 패키지 함수를 사용할 수 있습니다. `Context`를 사용하여 해당 작업의 타임아웃(timeout)이나 마감 기한(deadline)을 지정할 수 있습니다. 또한 `Context`를 통해 애플리케이션 전체에서 SQL 문을 실행하는 함수까지 취소 요청을 전파하여, 더 이상 필요하지 않은 리소스가 확실히 해제되도록 할 수 있습니다.

자세한 내용은 [진행 중인 작업 취소하기](/doc/database/cancel-operations)를 참조하십시오.

### 관리형 연결 풀 (Managed connection pool) {#connection_pool}

`sql.DB` 데이터베이스 핸들을 사용할 때는 코드의 필요에 따라 연결을 생성하고 폐기하는 내장 연결 풀(connection pool)을 통해 연결하게 됩니다. `sql.DB`를 통한 핸들은 Go에서 데이터베이스 액세스를 수행하는 가장 일반적인 방법입니다. 자세한 내용은 [데이터베이스 핸들 열기](/doc/database/open-handle)를 참조하세요.

`database/sql` 패키지는 커넥션 풀을 자동으로 관리합니다. 하지만 더 고급 설정이 필요한 경우, [커넥션 풀 속성 설정하기](/doc/database/manage-connections#connection_pool_properties)에서 설명하는 대로 커넥션 풀 속성을 설정할 수 있습니다.

단일 예약 연결(reserved connection)이 필요한 작업의 경우, `database/sql` 패키지는 [`sql.Conn`](https://pkg.go.dev/database/sql#Conn)을 제공합니다. `Conn`은 `sql.Tx`를 사용한 트랜잭션이 적절하지 않은 선택일 때 특히 유용합니다.

예를 들어, 코드가 다음과 같은 작업이 필요할 수 있습니다:

*   자체적인 트랜잭션 의미론(transaction semantics)을 포함하는 로직을 포함하여, DDL을 통해 스키마 변경을 수행합니다. `sql` 패키지의 트랜잭션 함수와 SQL 트랜잭션 문을 혼용하는 것은 [트랜잭션 실행](/doc/database/execute-transactions)에서 설명한 바와 같이 권장되지 않는 관행입니다.
*   임시 테이블을 생성하는 쿼리 잠금(locking) 작업을 수행합니다.

더 자세한 내용은 [전용 연결 사용하기](/doc/database/manage-connections#dedicated_connections)를 참조하세요.
