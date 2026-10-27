<!--{
  "Title": "SQL 인젝션 위험 방지하기"
}-->

`sql` 패키지 함수 인자로 SQL 파라미터 값을 제공함으로써 SQL 인젝션 위험을 방지할 수 있습니다. `sql` 패키지의 많은 함수들이 SQL 문을 위한 파라미터와 해당 문의 파라미터에 사용될 값들을 위한 파라미터를 제공합니다 (다른 함수들은 prepared statement를 위한 파라미터와 파라미터들을 제공합니다).

다음 예제의 코드는 `id` 파라미터의 자리 표시자로 `?` 기호를 사용하며, 이 파라미터는 함수 인자로 제공됩니다.

```go
// 파라미터를 사용하여 SQL 문을 실행하는 올바른 형식입니다.
rows, err := db.Query("SELECT * FROM user WHERE id = ?", id)
```

데이터베이스 작업을 수행하는 `sql` 패키지 함수들은 사용자가 제공한 인수를 통해 prepared statement를 생성합니다. 런타임에 `sql` 패키지는 SQL 문을 prepared statement로 변환하고, 이를 별도의 파라미터와 함께 전송합니다.

**참고:** 파라미터 플레이스홀더는 사용하는 DBMS 및 드라이버에 따라 다릅니다. 예를 들어, Postgres용 [pq driver](https://pkg.go.dev/github.com/lib/pq)는 `?` 대신 `$1`과 같은 형태의 플레이스홀더를 사용합니다.

매개변수가 포함된 SQL 문을 문자열로 구성하기 위해 `fmt` 패키지의 함수를 사용하고 싶은 유혹이 생길 수 있습니다. 예를 들어 다음과 같이 말이죠:

```
// 보안 위험!
rows, err := db.Query(fmt.Sprintf("SELECT * FROM user WHERE id = %s", id))
```

이것은 안전하지 않습니다! 이렇게 하면 Go는 전체 SQL 문을 DBMS로 보내기 전에 `%s` 형식 지정자를 매개변수 값으로 대체하여 전체 SQL 문을 조립합니다. 이는 코드 호출자가 `id` 인자로 예상치 못한 SQL 조각을 보낼 수 있기 때문에 [SQL injection](https://en.wikipedia.org/wiki/SQL_injection) 위험을 초래합니다. 해당 조각은 애플리케이션에 위험한 방식으로 SQL 문을 예측 불가능하게 완성할 수 있습니다.

예를 들어, 특정 `%s` 값을 전달하면 다음과 같은 결과가 되어 데이터베이스의 모든 사용자 레코드가 반환될 수 있습니다:

```
SELECT * FROM user WHERE id = 1 OR 1=1;
```
