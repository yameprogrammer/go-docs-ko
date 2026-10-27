<!--{
  "제목": "관계형 데이터베이스에 접근",
  "브레드크럼": true
}-->

Go를 사용하면 다양한 데이터베이스 및 데이터 액세스 방법을 애플리케이션에 통합할 수 있습니다. 이 섹션의 주제에서는 표준 라이브러리의 [`database/sql`](https://pkg.go.dev/database/sql) 패키지를 사용하여 관계형 데이터베이스에 액세스하는 방법을 설명합니다.

데이터 접근에 대한 Go를 사용한 입문 튜토리얼을 참조하십시오.
[튜토리얼: 관계형 데이터베이스 접근: [/doc/tutorial/database-access]

Go는 관계형 데이터베이스에 대한 고수준 액세스를 위한 ORM 라이브러리뿐만 아니라 다른 데이터 액세스 기술도 지원합니다. 또한, 비관계형 NoSQL 데이터 스토어도 지원합니다.

*   **객체-관계 매핑 (ORM) 라이브러리.** `database/sql` 패키지는 저수준 데이터 접근 로직에 대한 함수를 포함하지만, Go를 사용하여 더 높은 추상 수준에서 데이터 저장소를 액세스할 수도 있습니다. Go를 위한 두 인기 있는 객체-관계 매핑 (ORM) 라이브러리에 대해 자세히 알아보려면 [GORM](https://gorm.io/index.html) ([패키지 참조](https://pkg.go.dev/gorm.io/gorm)) 및 [ent](https://entgo.io/) ([패키지 참조](https://pkg.go.dev/entgo.io/ent))를 참조하십시오.
*   **NoSQL 데이터 저장소.** Go 커뮤니티는 MongoDB ([https://docs.mongodb.com/drivers/go/](https://docs.mongodb.com/drivers/go/)) 및 Couchbase ([https://docs.couchbase.com/go-sdk/current/hello-world/overview.html](https://docs.couchbase.com/go-sdk/current/hello-world/overview.html))를 포함한 대부분의 NoSQL 데이터 저장소에 대한 드라이버를 개발했습니다. [pkg.go.dev](https://pkg.go.dev/)에서 더 많은 정보를 찾을 수 있습니다.

### 지원되는 데이터베이스 관리 시스템 {#supported_dbms}

Go는 MySQL, Oracle, Postgres, SQL Server, SQLite 등 대부분의 일반적인 관계형 데이터베이스 관리 시스템을 지원합니다.

전체 드라이버 목록은 다음 페이지에서 확인할 수 있습니다:
[SQLDrivers](/wiki/SQLDrivers)

### 쿼리 실행 또는 데이터베이스 변경을 위한 함수 {#functions}

`database/sql` 패키지는 특정 유형의 데이터베이스 작업을 실행하는 데 필요한 함수를 포함합니다. 예를 들어, `Query` 또는 `QueryRow`를 사용하여 쿼리를 실행할 수 있지만, `QueryRow`는 단일 행만 예상되는 경우에 사용하도록 설계되었습니다. 즉, 단일 행만 포함하는 `sql.Rows`를 반환하는 오버헤드를 생략할 수 있습니다. `Exec` 함수를 사용하여 `INSERT`, `UPDATE`, 또는 `DELETE`와 같은 SQL 문을 사용하여 데이터베이스 변경을 수행할 수 있습니다.

자세한 내용은 다음을 참조하십시오:

*   [데이터를 반환하지 않는 SQL 문 실행](/doc/database/change-data)
*   [데이터 쿼리](/doc/database/querying)

### 거래 {#transactions}

`sql.Tx`를 사용하면 트랜잭션 내에서 데이터베이스 작업을 실행하는 코드를 작성할 수 있습니다. 트랜잭션 내에서 여러 작업을 함께 수행하고, 최종적으로 커밋하여 모든 변경 사항을 단일 원자적 단계로 적용하거나, 롤백하여 변경 사항을 취소할 수 있습니다.

자세한 내용은 [트랜잭션 실행](/doc/database/execute-transactions)를 참조하세요.

### 쿼리 취소 {#query_cancellation}

`context.Context`를 사용하면 데이터베이스 작업을 취소할 수 있습니다. 예를 들어, 클라이언트의 연결이 닫히거나 작업이 원하는 시간보다 오래 실행되는 경우에 유용합니다.

어떤 데이터베이스 작업에 대해서도, `Context`를 인자로 받는 `database/sql` 패키지의 함수를 사용할 수 있습니다. `Context`를 사용하여 작업에 대한 타임아웃 또는 데드라인을 지정할 수 있습니다. 또한 `Context`를 사용하여 SQL 문을 실행하는 함수에 취소 요청을 애플리케이션 전체에 전달하여, 더 이상 필요하지 않은 리소스를 해제할 수 있도록 할 수 있습니다.

자세한 내용은 [진행 중인 작업 취소](/doc/database/cancel-operations)를 참조하십시오.

### 관리형 연결 풀 {#connection_pool}

`sql.DB` 데이터베이스 핸들을 사용할 때, 사용 코드가 필요에 따라 연결을 생성하고 해제하는 내장 연결 풀에 연결합니다. `sql.DB`를 통해 얻은 핸들은 Go에서 데이터베이스 액세스를 하는 가장 일반적인 방법입니다. 자세한 내용은 "[데이터베이스 핸들 열기](/doc/database/open-handle)"를 참조하십시오.

패키지 `database/sql`는 연결 풀 관리를 대신 처리합니다. 하지만 더 복잡한 요구 사항의 경우, "[연결 풀 속성 설정](/doc/database/manage-connections#connection_pool_properties)"에 설명된 대로 연결 풀 속성을 설정할 수 있습니다.

다음과 같이 단일 예약을 필요로 하는 작업의 경우,
`database/sql` 패키지는 [`sql.Conn`](https://pkg.go.dev/database/sql#Conn)를 제공합니다.
`Conn`는 특히 `sql.Tx`를 사용한 트랜잭션이 적합하지 않을 때 유용합니다.

예를 들어, 귀하의 코드는 다음과 같은 작업을 수행해야 할 수 있습니다:

*   DDL을 통해 스키마 변경을 수행하고, 자체적인 트랜잭션 의미를 포함하는 로직을 포함합니다. `sql` 패키지의 트랜잭션 함수를 SQL 트랜잭션 문과 혼합하는 것은 [트랜잭션 실행](/doc/database/execute-transactions)에서 설명된 좋지 않은 방법입니다.
*   임시 테이블을 생성하는 쿼리 잠금 작업을 수행합니다.

자세한 내용은 [전용 연결 사용 방법](/doc/database/manage-connections#dedicated_connections)을 참조하세요.
