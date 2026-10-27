<!--{
  "제목": "데이터베이스 핸들 열기",
  "브레드크럼": true
}-->

[`database/sql`](https://pkg.go.dev/database/sql) 패키지는 데이터베이스 액세스를 단순화하여 연결 관리에 대한 필요성을 줄입니다. 많은 데이터 액세스 API와 달리, `database/sql`을 사용하면 명시적으로 연결을 열거나, 작업을 수행하고, 연결을 닫는 과정이 필요하지 않습니다. 대신, 코드는 연결 풀을 나타내는 데이터베이스 핸들을 열고, 해당 핸들을 사용하여 데이터 액세스 작업을 수행하며, 필요한 경우에만 `Close` 메서드를 호출하여 리소스를 해제합니다. 예를 들어, 검색된 행이나 준비된 문에 의해 유지되는 리소스를 해제합니다.

즉, 이는 `sql.DB` (https://pkg.go.dev/database/sql#DB)로 표현되는 데이터베이스 핸들로서, 연결 관리를 처리하고, 코드가 대신 열고 닫습니다. 코드가 해당 핸들을 사용하여 데이터베이스 작업을 수행하면, 이러한 작업은 데이터베이스에 동시 접근을 제공합니다. 자세한 내용은 [연결 관리](/doc/database/manage-connections)를 참조하십시오.

**참고:** 또한, 데이터베이스 연결을 예약할 수도 있습니다. 자세한 내용은 [전용 연결 사용]( /doc/database/manage-connections#dedicated_connections)을 참조하십시오.

`database/sql` 패키지에 사용 가능한 API 외에도, Go 커뮤니티는 가장 일반적인 (그리고 많은 특수한) 데이터베이스 관리 시스템 (DBMS)에 대한 드라이버를 개발했습니다.

데이터베이스 핸들을 열 때, 다음의 고수준 단계를 따릅니다:

1. 운전자 찾기.

운영자는 Go 코드와 데이터베이스 간의 요청 및 응답을 번역합니다. 자세한 내용은 [데이터베이스 드라이버 찾기 및 가져오기](#database_driver)를 참조하세요.

2. 데이터베이스 핸들을 엽니다.

드라이버를 가져온 후, 특정 데이터베이스에 대한 핸들을 열 수 있습니다. 자세한 내용은 [데이터베이스 핸들 열기](#opening_handle)를 참조하세요.

3. 연결 확인

데이터베이스 핸들을 열면, 코드는 연결이 사용 가능한지 확인할 수 있습니다. 자세한 내용은 [연결 확인](#confirm_connection)를 참조하세요.

프로그램은 일반적으로 명시적으로 데이터베이스 연결을 열거나 닫지 않습니다. 이는 데이터베이스 핸들이 담당합니다. 그러나 프로그램은 쿼리 결과가 포함된 `sql.Rows`와 같은 얻은 리소스를 해제해야 합니다. 자세한 내용은 [리소스 해제](#free_resources)를 참조하세요.

### 데이터베이스 드라이버 찾기 및 가져오기 {#database_driver}

```go
// 예시: Go 패키지에서 데이터베이스 드라이버 가져오기
import (
	"database/sql"
	_ "github.com/lib/pq" // PostgreSQL 드라이버
)
```

```
// 설명:
// 위 예시는 Go 패키지에서 데이터베이스 드라이버를 가져오는 방법을 보여줍니다.
// "github.com/lib/pq"는 PostgreSQL 드라이버의 예시 URL입니다.
// 실제 사용 시에는 사용하는 데이터베이스에 맞는 드라이버 URL을 사용해야 합니다.
```

필요한 것은 사용 중인 DBMS를 지원하는 데이터베이스 드라이버입니다. 사용 중인 데이터베이스에 대한 드라이버를 찾으려면 [SQLDrivers](/wiki/SQLDrivers)를 참조하십시오.

드라이버를 코드로 사용하려면, 다른 Go 패키지와 마찬가지로 가져옵니다. 다음은 예시입니다:

```
import "github.com/go-sql-driver/mysql"
```

참고: 드라이버 패키지에서 직접 함수를 호출하지 않는 경우 (예: `sql` 패키지에 암시적으로 사용되는 경우)
- 즉, 가져오기 경로 앞에 밑줄을 추가하여 빈 가져오기를 사용하는 것이 필요합니다:

```
import "github.com/go-sql-driver/mysql"
```

**참고:** 최선의 방법으로, 데이터베이스 드라이버의 자체 API를 데이터베이스 작업에 사용하는 것을 피하십시오. 대신 `database/sql` 패키지에 있는 함수를 사용하십시오. 이렇게 하면 코드가 DBMS와 느슨하게 결합되도록 하여, 필요한 경우 다른 DBMS로 쉽게 전환할 수 있습니다.

### 데이터베이스 핸들 열기 {#opening_handle}

```go
package main

import (
	"database/sql"
	"fmt"
	_ "github.com/lib/pq" // PostgreSQL 드라이버
)

func main() {
	db, err := sql.Open("postgres", "user=postgres dbname=mydatabase sslmode=disable")
	if err != nil {
		fmt.Println("Error opening database:", err)
		return
	}
	defer db.Close()

	// 데이터베이스 연결 확인
	err = db.Ping()
	if err != nil {
		fmt.Println("Error pinging database:", err)
		return
	}

	fmt.Println("Successfully connected to the database!")

	// 예: 테이블 생성
	_, err = db.Exec("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")
	if err != nil {
		fmt.Println("Error creating table:", err)
		return
	}

	fmt.Println("Table 'users' created successfully (if it didn't exist already).")
}
```

## 데이터베이스 연결 방법

다음은 Go에서 데이터베이스에 연결하는 방법의 예입니다. 이 예에서는 PostgreSQL를 사용하지만, 다른 데이터베이스 시스템에 대해서도 유사한 방식으로 연결할 수 있습니다.

**1. 데이터베이스 드라이버 가져오기:**

먼저 필요한 데이터베이스 드라이버를 가져와야 합니다. 예를 들어 PostgreSQL의 경우 `github.com/lib/pq`를 사용합니다.

```go
import (
	"database/sql"
	"fmt"
	_ "github.com/lib/pq" // PostgreSQL 드라이버
)
```

**2. `sql.Open()` 함수 사용:**

`sql.Open()` 함수는 새 데이터베이스 연결을 설정합니다.  첫 번째 인자는 데이터베이스 드라이버 이름(예: `"postgres"`), 두 번째 인자는 데이터베이스 연결 문자열입니다.

```go
db, err := sql.Open("postgres", "user=postgres dbname=mydatabase sslmode=disable")
```

**3. 연결 문자열 구성:**

데이터베이스 연결 문자열은 데이터베이스 서버, 사용자 이름, 비밀번호, 데이터베이스 이름, SSL 모드 등 필요한 연결 정보를 포함합니다.  예를 들어 위의 예에서 사용된 연결 문자열은 다음과 같습니다.

```
user=postgres dbname=mydatabase sslmode=disable
```

**4. 연결 확인 (Ping):**

`db.Ping()` 함수는 데이터베이스에 성공적으로 연결되었는지 확인합니다.  이 함수는 데이터베이스 서버에 쿼리를 보내고 응답을 확인하여 연결을 테스트합니다.

```go
err = db.Ping()
if err != nil {
	fmt.Println("Error pinging database:", err)
	return
}
```

**5. 데이터베이스 작업 수행:**

데이터베이스에 연결되면 이제 데이터를 쿼리, 삽입, 업데이트 또는 삭제하는 등의 작업을 수행할 수 있습니다.  Go의 `database/sql` 패키지는 이러한 작업을 수행하기 위한 다양한 함수를 제공합니다.  예를 들어 `db.Exec()`, `db.Query()` 및 `db.Close()` 함수를 사용할 수 있습니다.

**6. 연결 닫기:**

데이터베이스 작업을 완료한 후에는 반드시 `defer db.Close()`를 사용하여 데이터베이스 연결을 닫아야 합니다.  이렇게 하면 리소스를 효율적으로 관리하고 잠재적인 문제를 방지할 수 있습니다.

```go
defer db.Close()
```

`sql.DB` 데이터베이스 핸들은 데이터베이스에서 읽고 쓰는 기능을 제공하며, 개별적으로 또는 트랜잭션 내에서 사용할 수 있습니다.

다음 중 하나를 호출하여 데이터베이스 핸들을 얻을 수 있습니다: `sql.Open` (연결 문자열을 사용) 또는 `sql.OpenDB` (`driver.Connector`를 사용). 둘 다 [`sql.DB`](https://pkg.go.dev/database/sql#DB)의 포인터에 대한 참조를 반환합니다.

**참고:** 데이터베이스 자격 증명을 Go 소스에 포함하지 않도록 주의하십시오.
자세한 내용은 [데이터베이스 자격 증명 저장](#store_credentials)를 참조하십시오.

#### 연결 문자열로 시작하기 {#open_connection_string}

`[`sql.Open`](https://pkg.go.dev/database/sql#Open) 함수를 사용하여 연결을 설정할 때, 연결 문자열을 사용합니다. 문자열의 형식은 사용 중인 드라이버에 따라 달라집니다.

다음은 MySQL 예시입니다:

```
db, err = sql.Open("mysql", "username:password@tcp(127.0.0.1:3306)/jazzrecords")
if err != nil {
	log.Fatal(err)
}
```

하지만, 연결 속성을 더 구조화된 방식으로 캡처하면 더 읽기 쉬운 코드를 얻을 수 있을 것입니다. 구체적인 내용은 드라이버에 따라 다릅니다.

예를 들어, 다음과 같이 변경할 수 있습니다.
이 예제에서는 [`Config`](https://pkg.go.dev/github.com/go-sql-driver/mysql#Config)를 사용하여 속성을 지정하고,
[`FormatDSN 메서드`](https://pkg.go.dev/github.com/go-sql-driver/mysql#Config.FormatDSN)를 사용하여 연결 문자열을 구성합니다.

```
// 연결 속성을 지정합니다.
cfg := mysql.NewConfig()
cfg.User = username
cfg.Passwd = password
cfg.Net = "tcp"
cfg.Addr = "127.0.0.1:3306"
cfg.DBName = "jazzrecords"

// 데이터베이스 핸들을 가져옵니다.
db, err = sql.Open("mysql", cfg.FormatDSN())
if err != nil {
	log.Fatal(err)
}
```

#### 커넥터로 시작하기 {#open_connector}

`[sql.OpenDB 함수](https://pkg.go.dev/database/sql#OpenDB)`를 사용하는 경우, 연결 문자열에 제공되지 않는 드라이버별 연결 기능의 이점을 활용할 수 있습니다. 각 드라이버는 자체 연결 속성을 지원하며, 이는 종종 DBMS에 특정한 연결 요청을 사용자 정의하는 방법을 제공합니다.

이전의 `sql.Open` 예제를 `sql.OpenDB`를 사용하여 사용하도록 변경하면, 다음과 같은 코드를 사용하여 핸들을 만들 수 있습니다:

```
// 연결 속성을 지정합니다.
cfg := mysql.NewConfig()
cfg.User = username
cfg.Passwd = password
cfg.Net = "tcp"
cfg.Addr = "127.0.0.1:3306"
cfg.DBName = "jazzrecords"

// 드라이버별 연결자를 가져옵니다.
connector, err := mysql.NewConnector(&cfg)
if err != nil {
	log.Fatal(err)
}

// 데이터베이스 핸들을 가져옵니다.
db = sql.OpenDB(connector)
```

#### 오류 처리 {#handle_errors}

코드에서 `sql.Open`과 같은 방식으로 핸들을 생성하는 데 문제가 발생했는지 확인하십시오. 이는 연결 오류가 아닙니다. 대신, `sql.Open`이 핸들을 초기화할 수 없는 경우 오류를 받게 됩니다. 예를 들어, 지정한 DSN을 파싱할 수 없는 경우에 발생할 수 있습니다.

### 연결 확인 {#confirm_connection}

데이터베이스 핸들을 열 때, `sql` 패키지는 즉시 새로운
데이터베이스 연결을 생성하지 않을 수 있습니다. 대신, 코드가 필요할 때 연결을 생성할 수 있습니다.
데이터베이스를 즉시 사용하지 않으면서 연결이 설정될 수 있는지 확인하려면
`[`Ping`](https://pkg.go.dev/database/sql#DB.Ping) 또는
`[PingContext`](https://pkg.go.dev/database/sql#DB.PingContext)를 호출하십시오.

다음 예제에서 코드는 데이터베이스에 연결이 확인되었는지 확인하기 위해 핑을 수행합니다.

```
db, err = sql.Open("mysql", connString)

// 연결 성공 여부를 확인합니다.
if err := db.Ping(); err != nil {
	log.Fatal(err)
}
```

### 데이터베이스 자격 증명 저장 {#store_credentials}

데이터베이스 자격 증명을 Go 소스에 저장하는 것을 피하십시오. 이렇게 하면 다른 사람이 데이터베이스의 내용을 노출할 수 있습니다. 대신, 자격 증명을 코드 외부의 위치에 저장하는 방법을 찾으십시오. 예를 들어, 자격 증명을 저장하고 코드에서 사용할 수 있는 API를 제공하는 "비밀 관리 애플리케이션"을 고려해 볼 수 있습니다. 이 API를 사용하여 DBMS와 인증하는 데 필요한 자격 증명을 검색할 수 있습니다.

일반적인 접근 방식 중 하나는 프로그램을 시작하기 전에 비밀 정보를 환경 변수에 저장하는 것입니다. 예를 들어, 비밀 관리자에서 로드하여 Go 프로그램이 [`os.Getenv`](https://pkg.go.dev/os#Getenv)를 사용하여 읽을 수 있습니다:

```
username = os.Getenv("DB_USER")
password = os.Getenv("DB_PASS")
```

이 접근 방식은 또한 로컬 테스트를 위해 환경 변수를 직접 설정할 수 있도록 해줍니다.

### 사용하지 않는 자원 해제 {#free_resources}

`database/sql` 패키지를 사용하여 연결을 명시적으로 관리하거나 닫지 않더라도, 코드는 더 이상 필요하지 않은 리소스를 해제해야 합니다. 여기에는 쿼리 결과로 반환된 데이터를 나타내는 `sql.Rows` 또는 준비된 문을 나타내는 `sql.Stmt`에 의해 보유된 리소스가 포함될 수 있습니다.

일반적으로, `Close` 함수에 대한 호출을 `defer`를 사용하여 예약함으로써 리소스를 닫습니다. 이렇게 하면 예약된 함수가 종료되기 전에 리소스가 해제됩니다.

다음 예제에서 `Close`를 호출하여 `sql.Rows`가 보유한 리소스를 해제합니다.
[`https://pkg.go.dev/database/sql#Rows`](https://pkg.go.dev/database/sql#Rows)

```markdown
```
행, 오류 := db.Query("SELECT * FROM album WHERE artist = ?", artist)
if err != nil {
	log.Fatal(err)
}
defer rows.Close()

// 반환된 행을 순회합니다.
```
