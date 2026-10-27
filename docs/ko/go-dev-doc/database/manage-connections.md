<!--{
  "Title": "연결 관리하기"
}-->

대부분의 프로그램에서는 `sql.DB` 연결 풀(connection pool)의 기본값을 조정할 필요가 없습니다. 하지만 일부 고급 프로그램에서는 연결 풀 매개변수를 튜닝하거나 연결을 명시적으로 제어해야 할 수도 있습니다. 이 주제에서는 그 방법을 설명합니다.

[`sql.DB`](https://pkg.go.dev/database/sql#DB) 데이터베이스 핸들은 여러 고루틴(goroutine)이 동시에 사용해도 안전합니다(즉, 다른 언어에서 말하는 "스레드 세이프(thread-safe)"한 핸들입니다). 일부 다른 데이터베이스 액세스 라이브러리는 한 번에 하나의 작업만 수행할 수 있는 연결(connection)을 기반으로 합니다. 이러한 차이를 메우기 위해, 각 `sql.DB`는 기본 데이터베이스에 대한 활성 연결 풀을 관리하며, Go 프로그램의 병렬 처리를 위해 필요한 경우 새로운 연결을 생성합니다.

커넥션 풀(connection pool)은 대부분의 데이터 액세스 요구 사항에 적합합니다. `sql.DB`의 `Query` 또는 `Exec` 메서드를 호출하면, `sql.DB` 구현체는 풀에서 사용 가능한 커넥션을 가져오거나 필요 시 새로 생성합니다. 패키지는 커넥션이 더 이상 필요하지 않을 때 이를 다시 풀로 반환합니다. 이를 통해 데이터베이스 액세스에 대해 높은 수준의 병렬성을 지원합니다.

### 연결 풀 속성 설정 {#connection_pool_properties}

`sql` 패키지가 커넥션 풀을 관리하는 방식을 안내하는 속성들을 설정할 수 있습니다. 이러한 속성들이 미치는 영향에 대한 통계를 확인하려면 [`DB.Stats`](https://pkg.go.dev/database/sql#DB.Stats)를 사용하십시오.

#### 최대 열린 연결 수 설정 {#max_open_connections}

[`DB.SetMaxOpenConns`](https://pkg.go.dev/database/sql#DB.SetMaxOpenConns)는 열려 있는 연결 수에 제한을 둡니다. 이 제한을 초과하면, 새로운 데이터베이스 작업은 기존 작업이 완료될 때까지 대기하며, 그 시점에 `sql.DB`가 새로운 연결을 생성합니다. 기본적으로 `sql.DB`는 연결이 필요할 때 모든 기존 연결이 사용 중이라면 언제든 새로운 연결을 생성합니다.

제한(limit)을 설정하면 데이터베이스 사용 방식이 락(lock)이나 세마포어(semaphore)를 획득하는 것과 비슷해지며, 그 결과 애플리케이션이 새로운 데이터베이스 연결을 기다리다가 데드락(deadlock) 상태에 빠질 수 있다는 점을 유의하십시오.

#### 유휴 연결의 최대 수 설정 {#max_idle_connections}

[`DB.SetMaxIdleConns`](https://pkg.go.dev/database/sql#DB.SetMaxIdleConns)는 `sql.DB`가 유지하는 유휴 연결(idle connections)의 최대 개수 제한을 변경합니다.

특정 데이터베이스 연결에서 SQL 작업이 완료되었을 때, 일반적으로 연결이 즉시 종료되지는 않습니다. 애플리케이션이 곧 다시 연결이 필요할 수 있으며, 열려 있는 연결을 유지하면 다음 작업을 위해 데이터베이스에 다시 연결해야 하는 상황을 피할 수 있기 때문입니다. 기본적으로 `sql.DB`는 어느 시점에서나 두 개의 유휴(idle) 연결을 유지합니다. 병렬성이 높은 프로그램의 경우, 이 제한 수치를 높이면 빈번한 재연결을 방지할 수 있습니다.

#### 연결이 유휴 상태로 유지될 수 있는 최대 시간 설정 {#max_idle_time}

[`DB.SetConnMaxIdleTime`](https://pkg.go.dev/database/sql#DB.SetConnMaxIdleTime)은
연결이 닫히기 전까지 유휴 상태로 유지될 수 있는 최대 시간을 설정합니다.
이를 통해 `sql.DB`는 지정된 기간보다 오래 유휴 상태인 연결을 닫습니다.

기본적으로 유휴 연결(idle connection)이 연결 풀에 추가되면, 다시 필요할 때까지 그곳에 유지됩니다. 병렬 활동이 급증하는 동안 허용되는 유휴 연결 수를 늘리기 위해 `DB.SetMaxIdleConns`를 사용할 때, `DB.SetConnMaxIdleTime`을 함께 사용하면 시스템이 한산해졌을 때 해당 연결들을 나중에 해제하도록 설정할 수 있습니다.

#### 연결의 최대 수명 설정 {#max_connection_lifetime}

[`DB.SetConnMaxLifetime`](https://pkg.go.dev/database/sql#DB.SetConnMaxLifetime)을 사용하면 연결이 닫히기 전까지 열려 있을 수 있는 최대 시간을 설정할 수 있습니다.

기본적으로 연결(connection)은 위에서 설명한 제한 사항에 따라 임의의 시간 동안 사용 및 재사용될 수 있습니다. 로드 밸런싱된 데이터베이스 서버를 사용하는 시스템과 같은 일부 환경에서는, 애플리케이션이 재연결 없이 특정 연결을 너무 오랫동안 사용하지 않도록 보장하는 것이 도움이 될 수 있습니다.

### 전용 연결 사용하기 {#dedicated_connections}

`database/sql` 패키지는 특정 연결에서 실행되는 일련의 작업에 데이터베이스가 암시적인 의미를 부여할 수 있는 경우에 사용할 수 있는 함수들을 포함하고 있습니다.

가장 일반적인 예시는 트랜잭션입니다. 트랜잭션은 보통 `BEGIN` 명령어로 시작하여 `COMMIT` 또는 `ROLLBACK` 명령어로 끝나며, 해당 명령어들 사이에서 연결(connection)을 통해 발행된 모든 명령어를 전체 트랜잭션에 포함합니다. 이 사용 사례의 경우, `sql` 패키지의 트랜잭션 지원 기능을 사용하십시오. [트랜잭션 실행](/doc/database/execute-transactions)을 참조하십시오.

일련의 개별 작업들이 모두 동일한 연결에서 실행되어야 하는 다른 유즈케이스의 경우, `sql` 패키지는 전용 연결(dedicated connections)을 제공합니다. [`DB.Conn`](https://pkg.go.dev/database/sql#DB.Conn)을 통해 전용 연결인 [`sql.Conn`](https://pkg.go.dev/database/sql#Conn)을 얻을 수 있습니다. `sql.Conn`은 `BeginTx`, `ExecContext`, `PingContext`, `PrepareContext`, `QueryContext`, `QueryRowContext` 메서드를 가지고 있으며, 이는 DB의 동일한 메서드와 유사하게 동작하지만 오직 해당 전용 연결만을 사용합니다. 전용 연결 사용을 마쳤다면, 반드시 `Conn.Close`를 사용하여 연결을 해제해야 합니다.
