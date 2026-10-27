<!--{
  "Title": "데이터베이스 핸들 열기",
  "Breadcrumb": true
}-->

[`database/sql`](https://pkg.go.dev/database/sql) 패키지는 연결 관리의 필요성을 줄여 데이터베이스 액세스를 간소화합니다. 많은 데이터 액세스 API와 달리, `database/sql`에서는 명시적으로 연결을 열고 작업을 수행한 뒤 연결을 닫지 않습니다. 대신, 코드가 연결 풀을 나타내는 데이터베이스 핸들을 열고, 이 핸들을 통해 데이터 액세스 작업을 수행하며, 조회된 행(rows)이나 준비된 문장(prepared statement)이 보유한 리소스와 같이 리소스를 해제해야 할 때에만 `Close` 메서드를 호출합니다.

다시 말해, [`sql.DB`](https://pkg.go.dev/database/sql#DB)로 표현되는 데이터베이스 핸들이 연결을 관리하며, 코드 대신 연결을 열고 닫는 역할을 합니다. 코드가 이 핸들을 사용하여 데이터베이스 작업을 수행하면, 해당 작업들은 데이터베이스에 동시 접근(concurrent access)하게 됩니다. 자세한 내용은 [Managing connections](/doc/database/manage-connections)을 참조하세요.

**참고:** 데이터베이스 연결을 예약할 수도 있습니다. 자세한 내용은 [전용 연결 사용하기](/doc/database/manage-connections#dedicated_connections)를 참조하세요.

`database/sql` 패키지에서 제공하는 API 외에도, Go 커뮤니티는 가장 일반적인(그리고 많은 드문) 모든 데이터베이스 관리 시스템(DBMS)을 위한 드라이버를 개발해 왔습니다.

데이터베이스 핸들을 열 때, 다음과 같은 상위 수준의 단계를 따릅니다:

1. 드라이버를 찾습니다.

드라이버는 Go 코드와 데이터베이스 사이에서 요청과 응답을 변환합니다. 자세한 내용은 [데이터베이스 드라이버 찾기 및 가져오기](#database_driver)를 참조하세요.

2. 데이터베이스 핸들을 엽니다.

드라이버를 임포트한 후, 특정 데이터베이스에 대한 핸들을 열 수 있습니다. 자세한 내용은 [데이터베이스 핸들 열기](#opening_handle)를 참조하세요.

3. 연결을 확인합니다.

데이터베이스 핸들을 열면, 코드를 통해 연결 가능 여부를 확인할 수 있습니다. 자세한 내용은 [연결 확인](#confirm_connection)을 참조하십시오.

일반적으로 코드에서 데이터베이스 연결을 명시적으로 열거나 닫지 않습니다. 이 작업은 데이터베이스 핸들이 처리합니다. 하지만 쿼리 결과가 포함된 `sql.Rows`와 같이 작업 과정에서 획득한 리소스는 코드를 통해 해제해야 합니다. 자세한 내용은 [리소스 해제](#free_resources)를 참조하십시오.

### 데이터베이스 드라이버 찾기 및 가져오기 {#database_driver}

사용 중인 DBMS를 지원하는 데이터베이스 드라이버가 필요합니다. 사용 중인 데이터베이스에 맞는 드라이버를 찾으려면 [SQLDrivers](/wiki/SQLDrivers)를 참조하세요.

드라이버를 코드에서 사용할 수 있게 하려면, 다른 Go 패키지를 가져오는 것과 동일하게 import 하면 됩니다. 다음은 예시입니다:

```
import "github.com/go-sql-driver/mysql"
```

`sql` 패키지에 의해 암시적으로 사용되는 경우처럼 드라이버 패키지에서 함수를 직접 호출하지 않는 경우에는, 임포트 경로 앞에 언더스코어(`_`)를 붙이는 blank import를 사용해야 합니다:

```go
import _ "github.com/go-sql-driver/mysql"
```

**참고:** 권장 사항으로, 데이터베이스 작업을 위해 데이터베이스 드라이버 자체의 API를 사용하는 것을 지양하십시오. 대신 `database/sql` 패키지의 함수들을 사용하십시오. 이렇게 하면 코드가 DBMS와 느슨하게 결합되어, 필요한 경우 다른 DBMS로 더 쉽게 전환할 수 있습니다.

### 데이터베이스 핸들 열기 {#opening_handle}

`sql.DB` 데이터베이스 핸들은 개별적으로 또는 트랜잭션 내에서 데이터베이스에 읽고 쓸 수 있는 기능을 제공합니다.

`sql.Open`(연결 문자열을 받음) 또는 `sql.OpenDB`(`driver.Connector`를 받음)를 호출하여 데이터베이스 핸들을 얻을 수 있습니다. 두 함수 모두 [`sql.DB`](https://pkg.go.dev/database/sql#DB)에 대한 포인터를 반환합니다.

**참고:** 데이터베이스 인증 정보가 Go 소스 코드에 포함되지 않도록 주의하십시오.
자세한 내용은 [데이터베이스 인증 정보 저장하기](#store_credentials)를 참조하십시오.

#### 연결 문자열로 열기 {#open_connection_string}

연결 문자열을 사용하여 연결하려는 경우 [`sql.Open` 함수](https://pkg.go.dev/database/sql#Open)를 사용하십시오. 문자열의 형식은 사용하는 드라이버에 따라 다릅니다.

MySQL의 예시는 다음과 같습니다:

```go
db, err = sql.Open("mysql", "username:password@tcp(127.0.0.1:3306)/jazzrecords")
if err != nil {
	log.Fatal(err)
}
```

하지만 연결 속성을 더 구조적인 방식으로 캡처하는 것이 코드의 가독성을 높여준다는 점을 알게 되실 것입니다. 세부 사항은 드라이버마다 다를 수 있습니다.

예를 들어, 이전 예제를 다음과 같이 변경할 수 있습니다. 이 방식은 MySQL 드라이버의 [`Config`](https://pkg.go.dev/github.com/go-sql-driver/mysql#Config)를 사용하여 속성을 지정하고, [`FormatDSN 메서드`](https://pkg.go.dev/github.com/go-sql-driver/mysql#Config.FormatDSN)를 사용하여 연결 문자열을 생성합니다.

```go
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

#### 커넥터로 열기 {#open_connector}

연결 문자열(connection string)에서는 사용할 수 없는 드라이버 전용 연결 기능을 활용하려는 경우 [`sql.OpenDB function`](https://pkg.go.dev/database/sql#OpenDB)을 사용하십시오. 각 드라이버는 고유한 연결 속성 세트를 지원하며, 대개 DBMS에 특화된 연결 요청을 사용자 정의하는 방법을 제공합니다.

앞선 `sql.Open` 예제를 `sql.OpenDB`를 사용하도록 수정하면, 다음과 같은 코드로 핸들을 생성할 수 있습니다.

```go
// 연결 속성을 지정합니다.
cfg := mysql.NewConfig()
cfg.User = username
cfg.Passwd = password
cfg.Net = "tcp"
cfg.Addr = "127.0.0.1:3306"
cfg.DBName = "jazzrecords"

// 드라이버 전용 커넥터를 가져옵니다.
connector, err := mysql.NewConnector(&cfg)
if err != nil {
	log.Fatal(err)
}

// 데이터베이스 핸들을 가져옵니다.
db = sql.OpenDB(connector)
```

#### 에러 처리 {#handle_errors}

코드는 `sql.Open`과 같이 핸들을 생성하려는 시도에서 발생하는 에러를 확인해야 합니다. 이는 연결 에러(connection error)가 아닙니다. 대신, `sql.Open`이 핸들을 초기화할 수 없는 경우 에러가 발생합니다. 예를 들어, 지정한 DSN을 파싱할 수 없는 경우에 이런 일이 발생할 수 있습니다.

### 연결 확인 {#confirm_connection}

데이터베이스 핸들을 열 때, `sql` 패키지는 즉시 새로운 데이터베이스 연결을 생성하지 않을 수 있습니다. 대신, 코드에서 연결이 필요할 때 연결을 생성할 수 있습니다. 데이터베이스를 즉시 사용하지 않지만 연결이 성공적으로 수립될 수 있는지 확인하고 싶다면, [`Ping`](https://pkg.go.dev/database/sql#DB.Ping) 또는 [`PingContext`](https://pkg.go.dev/database/sql#DB.PingContext)를 호출하십시오.

다음 예제의 코드는 데이터베이스에 ping을 보내 연결을 확인합니다.

```go
db, err = sql.Open("mysql", connString)

// 연결 성공 여부를 확인합니다.
if err := db.Ping(); err != nil {
	log.Fatal(err)
}
```

### 데이터베이스 자격 증명 저장하기 {#store_credentials}

데이터베이스 자격 증명을 Go 소스 코드에 저장하지 마세요. 이는 데이터베이스의 내용이 타인에게 노출될 위험이 있습니다. 대신, 코드 외부의 위치에 저장하되 코드에서 접근할 수 있는 방법을 찾으십시오. 예를 들어, 자격 증명을 저장하고 코드가 DBMS 인증을 위해 자격 증명을 검색하는 데 사용할 수 있는 API를 제공하는 시크릿 키퍼(secret keeper) 앱을 고려해 보십시오.

인기 있는 접근 방식 중 하나는 프로그램이 시작되기 전에(아마도 시크릿 매니저에서 로드하여) 환경 변수에 시크릿을 저장하고, Go 프로그램에서 [`os.Getenv`](https://pkg.go.dev/os#Getenv)를 사용하여 이를 읽는 것입니다.

```go
username := os.Getenv("DB_USER")
password := os.Getenv("DB_PASS")
```

이 방식은 로컬 테스트를 위해 환경 변수를 직접 설정할 수 있게 해줍니다.

### 리소스 해제 {#free_resources}

`database/sql` 패키지를 사용할 때 연결(connection)을 명시적으로 관리하거나 닫지는 않지만, 더 이상 필요하지 않은 리소스는 코드를 통해 해제해야 합니다. 여기에는 쿼리 결과 데이터를 나타내는 `sql.Rows`나 준비된 문장(prepared statement)을 나타내는 `sql.Stmt`가 보유한 리소스가 포함될 수 있습니다.

일반적으로 `Close` 함수 호출을 `defer`하여 리소스가 닫히도록 함으로써, 리소스를 감싸고 있는 함수가 종료되기 전에 해당 리소스들이 해제되도록 합니다.

다음 예제의 코드는 [`sql.Rows`](https://pkg.go.dev/database/sql#Rows)가 보유한 리소스를 해제하기 위해 `Close`를 defer 합니다.

```go
rows, err := db.Query("SELECT * FROM album WHERE artist = ?", artist)
if err != nil {
	log.Fatal(err)
}
defer rows.Close()

// 반환된 행들을 루프하며 처리합니다.
```
