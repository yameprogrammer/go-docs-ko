<!--{
  "Title": "튜토리얼: 관계형 데이터베이스 액세스",
  "Breadcrumb": true
}-->

이 튜토리얼에서는 Go와 표준 라이브러리의 `database/sql` 패키지를 사용하여 관계형 데이터베이스에 액세스하는 기본 방법을 소개합니다.

Go와 그 도구들에 대해 기본적인 지식이 있다면 이 튜토리얼을 최대한 활용하실 수 있습니다. Go를 처음 접하신다면, [Tutorial: Get started with Go](/doc/tutorial/getting-started)에서 빠른 입문 가이드를 확인하시기 바랍니다.

사용하시게 될 [`database/sql`](https://pkg.go.dev/database/sql) 패키지에는 데이터베이스 연결, 트랜잭션 실행, 진행 중인 작업 취소 등을 위한 타입과 함수들이 포함되어 있습니다. 패키지 사용에 대한 자세한 내용은 [Accessing databases](/doc/database/index)를 참조하세요.

이 튜토리얼에서는 데이터베이스를 생성한 다음, 해당 데이터베이스에 액세스하는 코드를 작성합니다. 예제 프로젝트는 빈티지 재즈 레코드 데이터 저장소가 될 것입니다.

이 튜토리얼에서는 다음 섹션들을 차례대로 학습하게 됩니다:

1. 코드를 위한 폴더를 생성합니다.
2. 데이터베이스를 설정합니다.
3. 데이터베이스 드라이버를 임포트합니다.
4. 데이터베이스 핸들을 가져와 연결합니다.
5. 여러 행을 쿼리합니다.
6. 단일 행을 쿼리합니다.
7. 데이터를 추가합니다.

**참고:** 다른 튜토리얼은 [Tutorials](/doc/tutorial/index.html)를 참조하세요.

## 사전 요구 사항 {#prerequisites}

*   **[MySQL](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/) 관계형 데이터베이스 관리 시스템(DBMS) 설치.**
*   **Go 설치.** 설치 방법은 [Installing Go](/doc/install)를 참조하십시오.
*   **코드 편집 도구.** 사용 가능한 모든 텍스트 편집기를 사용할 수 있습니다.
*   **명령어 터미널.** Go는 Linux 및 Mac의 모든 터미널, 그리고 Windows의 PowerShell 또는 cmd에서 원활하게 작동합니다.

## 코드를 위한 폴더 생성 {#create_folder}

시작하려면, 작성할 코드를 위한 폴더를 생성하세요.

1. 명령 프롬프트를 열고 홈 디렉터리로 이동하십시오.

Linux 또는 Mac에서:

```
    $ cd
    ```

Windows에서:

```
    C:\> cd %HOMEPATH%
    ```

이 튜토리얼의 나머지 부분에서는 프롬프트로 `$`를 표시하겠습니다. 우리가 사용하는 명령어들은 Windows에서도 작동합니다.

2. 명령 프롬프트에서 코드를 저장할 `data-access`라는 이름의 디렉터리를 생성합니다.

```
    $ mkdir data-access
    $ cd data-access
    ```

3. 이번 튜토리얼 동안 추가할 의존성들을 관리할 수 있는 모듈을 생성하세요.

`go mod init` 명령어를 실행하고, 새 코드의 모듈 경로를 입력하세요.

```
    $ go mod init example/data-access
    go: creating new go.mod: module example/data-access
    ```

이 명령은 추가한 의존성들이 추적을 위해 나열될 `go.mod` 파일을 생성합니다. 자세한 내용은 [의존성 관리](/doc/modules/managing-dependencies)를 참조하십시오.

**참고:** 실제 개발 시에는 본인의 필요에 맞는 더 구체적인 모듈 경로를 지정해야 합니다. 자세한 내용은 [의존성 관리](/doc/modules/managing-dependencies#naming_module)를 참조하세요.

다음으로, 데이터베이스를 생성합니다.

## 데이터베이스 설정 {#set_up_database}

이 단계에서는 작업에 사용할 데이터베이스를 생성합니다. DBMS 자체의 CLI를 사용하여 데이터베이스와 테이블을 생성하고 데이터를 추가합니다.

바이닐(LP)로 된 빈티지 재즈 녹음 데이터를 포함하는 데이터베이스를 생성하게 됩니다.

여기 사용된 코드는 [MySQL CLI](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)를 사용하지만, 대부분의 DBMS는 유사한 기능을 가진 자체 CLI를 제공합니다.

1. 새 명령 프롬프트를 엽니다.
2. 명령줄에서 다음 MySQL 예시와 같이 DBMS에 로그인합니다.

```
    $ mysql -u root -p
    Enter password:
```

mysql>
    ```

3. `mysql` 명령 프롬프트에서 데이터베이스를 생성합니다.

```
    mysql> create database recordings;
    ```

4. 테이블을 추가할 수 있도록 방금 생성한 데이터베이스로 변경하십시오.

```
    mysql> use recordings;
    Database changed
    ```

5. 텍스트 에디터의 `data-access` 폴더에 테이블 추가를 위한 SQL 스크립트를 저장할 `create-tables.sql` 파일을 생성하세요.
6. 파일에 다음 SQL 코드를 붙여넣고 파일을 저장하세요.

```
    DROP TABLE IF EXISTS album;
    CREATE TABLE album (
      id         INT AUTO_INCREMENT NOT NULL,
      title      VARCHAR(128) NOT NULL,
      artist     VARCHAR(255) NOT NULL,
      price      DECIMAL(5,2) NOT NULL,
      PRIMARY KEY (`id`)
    );
```

```sql
INSERT INTO album
      (title, artist, price)
    VALUES
      ('Blue Train', 'John Coltrane', 56.99),
      ('Giant Steps', 'John Coltrane', 63.99),
      ('Jeru', 'Gerry Mulligan', 17.99),
      ('Sarah Vaughan', 'Sarah Vaughan', 34.98);
```

이 SQL 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   `album`이라는 이름의 테이블을 삭제(drop)합니다. 이 명령을 먼저 실행하면, 나중에 테이블을 처음부터 다시 시작하고 싶을 때 스크립트를 더 쉽게 재실행할 수 있습니다.

*   `title`, `artist`, `price` 네 개의 컬럼을 가진 `album` 테이블을 생성합니다.
        각 행의 `id` 값은 DBMS에 의해 자동으로 생성됩니다.

*   값이 포함된 행 4개를 추가합니다.

7. `mysql` 명령 프롬프트에서 방금 생성한 스크립트를 실행하세요.

다음과 같은 형식으로 `source` 명령어를 사용하게 됩니다:

```
    mysql> source /path/to/create-tables.sql
    ```

8. DBMS 명령 프롬프트에서 `SELECT` 문을 사용하여 데이터가 포함된 테이블이 성공적으로 생성되었는지 확인하십시오.

```
    mysql> select * from album;
    +----+---------------+----------------+-------+
    | id | title         | artist         | price |
    +----+---------------+----------------+-------+
    |  1 | Blue Train    | John Coltrane  | 56.99 |
    |  2 | Giant Steps   | John Coltrane  | 63.99 |
    |  3 | Jeru          | Gerry Mulligan | 17.99 |
    |  4 | Sarah Vaughan | Sarah Vaughan  | 34.98 |
    +----+---------------+----------------+-------+
    4 rows in set (0.00 sec)
    ```

다음으로, 쿼리를 실행할 수 있도록 연결하는 Go 코드를 작성하겠습니다.

## 데이터베이스 드라이버 찾기 및 임포트하기 {#import_driver}

데이터가 포함된 데이터베이스가 준비되었으니, 이제 Go 코드를 작성해 보겠습니다.

`database/sql` 패키지의 함수를 통해 보내는 요청을 데이터베이스가 이해할 수 있는 요청으로 변환해 줄 데이터베이스 드라이버를 찾아 임포트(import)하세요.

1. 브라우저에서 [SQLDrivers](/wiki/SQLDrivers) 위키 페이지를 방문하여 사용할 수 있는 드라이버를 확인하세요.

페이지의 목록을 사용하여 사용할 드라이버를 식별하세요. 이 튜토리얼에서 MySQL에 접속하기 위해 [Go-MySQL-Driver](https://github.com/go-sql-driver/mysql/)를 사용합니다.

2. 드라이버의 패키지 이름을 확인하세요 -- 여기서는 `github.com/go-sql-driver/mysql`입니다.

3. 텍스트 에디터를 사용하여 Go 코드를 작성할 파일을 생성하고, 이전에 생성한 `data-access` 디렉토리에 `main.go`라는 이름으로 저장하십시오.

4. `main.go` 파일에 다음 코드를 붙여넣어 드라이버 패키지를 임포트하세요.

```
    package main
```

```go
import "github.com/go-sql-driver/mysql"
    ```

이 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   코드를 `main` 패키지에 추가하여 독립적으로 실행할 수 있도록 하세요.

*   MySQL 드라이버 `github.com/go-sql-driver/mysql`를 임포트합니다.

드라이버를 임포트했으므로, 이제 데이터베이스에 액세스하기 위한 코드를 작성하기 시작합니다.

## 데이터베이스 핸들 가져오기 및 연결 {#get_handle}

이제 데이터베이스 핸들을 통해 데이터베이스 액세스를 제공하는 Go 코드를 작성해 보겠습니다.

특정 데이터베이스에 대한 액세스를 나타내는 `sql.DB` 구조체에 대한 포인터를 사용하게 됩니다.

#### 코드 작성하기

1. `main.go` 파일의 방금 추가한 `import` 코드 아래에, 데이터베이스 핸들을 생성하기 위해 다음 Go 코드를 붙여넣으세요.

```go
    var db *sql.DB
```

```go
func main() {
    	// 연결 속성을 캡처합니다.
    	cfg := mysql.NewConfig()
    	cfg.User = os.Getenv("DBUSER")
    	cfg.Passwd = os.Getenv("DBPASS")
    	cfg.Net = "tcp"
    	cfg.Addr = "127.0.0.1:3306"
    	cfg.DBName = "recordings"
```

// 데이터베이스 핸들을 가져옵니다.
    	var err error
    	db, err = sql.Open("mysql", cfg.FormatDSN())
    	if err != nil {
    		log.Fatal(err)
    	}

```go
pingErr := db.Ping()
    	if pingErr != nil {
    		log.Fatal(pingErr)
    	}
    	fmt.Println("Connected!")
    }
    ```

이 코드에서 당신은 다음을 수행합니다:

*   [`*sql.DB`](https://pkg.go.dev/database/sql#DB) 타입의 `db` 변수를 선언합니다.
        이것이 데이터베이스 핸들이 됩니다.

`db`를 전역 변수로 설정하면 이 예제가 간단해집니다. 실제 운영 환경에서는 변수가 필요한 함수에 해당 변수를 전달하거나 구조체로 래핑하는 등의 방법을 통해 전역 변수 사용을 피해야 합니다.

*   MySQL 드라이버의 [`Config`](https://pkg.go.dev/github.com/go-sql-driver/mysql#Config)와
    -- 그리고 해당 타입의 [`FormatDSN`](https://pkg.go.dev/github.com/go-sql-driver/mysql#Config.FormatDSN)을 사용하여
    -– 연결 속성을 수집하고 이를 연결 문자열을 위한 DSN으로 포맷팅합니다.

`Config` 구조체를 사용하면 연결 문자열(connection string)을 사용하는 것보다 코드를 더 읽기 쉽게 만들 수 있습니다.

*   `FormatDSN`의 반환 값을 전달하여 `db` 변수를 초기화하기 위해 [`sql.Open`](https://pkg.go.dev/database/sql#Open)을 호출합니다.

*   `sql.Open`에서 발생한 에러가 있는지 확인하세요. 예를 들어, 데이터베이스 연결 세부 정보가 올바르게 구성되지 않은 경우 실패할 수 있습니다.

코드를 단순화하기 위해, `log.Fatal`을 호출하여 실행을 종료하고 콘솔에 에러를 출력하고 있습니다. 실제 운영 코드에서는 더 정중한(graceful) 방식으로 에러를 처리해야 합니다.

*   [`DB.Ping`](https://pkg.go.dev/database/sql#DB.Ping)을 호출하여 데이터베이스 연결이 정상적으로 작동하는지 확인하세요. 런타임 시 `sql.Open`은 드라이버에 따라 즉시 연결되지 않을 수 있습니다. 여기서 `Ping`을 사용하는 이유는 `database/sql` 패키지가 필요할 때 연결할 수 있는지 확인하기 위해서입니다.

*   연결에 실패했을 경우를 대비해 `Ping`에서 발생한 에러가 있는지 확인하십시오.

*   `Ping` 연결에 성공하면 메시지를 출력합니다.

2. `main.go` 파일의 상단, package 선언 바로 아래에 방금 작성한 코드를 지원하는 데 필요한 패키지들을 import 하세요.

이제 파일의 상단은 다음과 같아야 합니다:

```
    package main
```

```go
import (
    	"database/sql"
    	"fmt"
    	"log"
    	"os"
```

"github.com/go-sql-driver/mysql"
    )
    ```

3. `main.go`를 저장하세요.

#### 코드 실행하기

1. MySQL 드라이버 모듈을 종속성으로 추적하기 시작합니다.

[`go get`](/cmd/go/#hdr-Add_dependencies_to_current_module_and_install_them)를 사용하여 `github.com/go-sql-driver/mysql` 모듈을 사용자 모듈의 의존성으로 추가하세요. 현재 디렉토리에 있는 코드에 대한 의존성을 가져오려면 점(`.`) 인수를 사용하세요.

```
    $ go get .
    go: added filippo.io/edwards25519 v1.1.0
    go: added github.com/go-sql-driver/mysql v1.8.1
    ```

Go는 이전 단계에서 `import` 선언에 이 패키지를 추가했기 때문에 해당 의존성을 다운로드했습니다. 의존성 추적에 대한 자세한 내용은 [의존성 추가하기](/doc/modules/managing-dependencies#adding_dependency)를 참조하세요.

2. 명령 프롬프트에서 Go 프로그램이 사용할 수 있도록 `DBUSER` 및 `DBPASS` 환경 변수를 설정하십시오.

Linux 또는 Mac에서:

```
    $ export DBUSER=username
    $ export DBPASS=password
    ```

Windows에서:

```
    C:\Users\you\data-access> set DBUSER=username
    C:\Users\you\data-access> set DBPASS=password
    ```

3. `main.go` 파일이 포함된 디렉토리의 명령줄에서, "현재 디렉토리의 패키지를 실행하라"는 의미의 점(`.`) 인자를 사용하여 `go run`을 입력해 코드를 실행하세요.

```
    $ go run .
    Connected!
    ```

연결되었습니다! 다음으로, 데이터를 쿼리하겠습니다.

## 여러 행 쿼리하기 {#multiple_rows}

이 섹션에서는 Go를 사용하여 여러 행을 반환하도록 설계된 SQL 쿼리를 실행해 보겠습니다.

여러 행을 반환할 수 있는 SQL 문장의 경우, `database/sql` 패키지의 `Query` 메서드를 사용한 다음 반환된 행들을 루프(loop)로 처리합니다. (단일 행을 쿼리하는 방법은 이후 [단일 행 쿼리](#single_row) 섹션에서 배우게 됩니다.)

#### 코드 작성하기

1. `main.go` 파일의 `func main` 바로 위에 다음 `Album` 구조체 정의를 붙여넣으세요. 이 구조체는 쿼리에서 반환된 행 데이터를 저장하는 데 사용됩니다.

```
    type Album struct {
    	ID     int64
    	Title  string
    	Artist string
    	Price  float32
    }
    ```

2. `func main` 아래에 데이터베이스를 쿼리하기 위한 다음 `albumsByArtist` 함수를 붙여넣으세요.

```go
    // albumsByArtist는 지정된 아티스트 이름을 가진 앨범을 쿼리합니다.
    func albumsByArtist(name string) ([]Album, error) {
    	// 반환된 행의 데이터를 저장할 albums 슬라이스입니다.
    	var albums []Album
```

```go
rows, err := db.Query("SELECT * FROM album WHERE artist = ?", name)
    	if err != nil {
    		return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
    	}
    	defer rows.Close()
    	// rows를 순회하며, Scan을 사용하여 컬럼 데이터를 구조체 필드에 할당합니다.
    	for rows.Next() {
    		var alb Album
    		if err := rows.Scan(&alb.ID, &alb.Title, &alb.Artist, &alb.Price); err != nil {
    			return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
    		}
    		albums = append(albums, alb)
    	}
    	if err := rows.Err(); err != nil {
    		return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
    	}
    	return albums, nil
    }
    ```

이 코드에서 귀하는 다음과 같은 작업을 수행합니다:

*   정의한 `Album` 타입의 `albums` 슬라이스를 선언합니다. 여기에는 반환된 행(row)의 데이터가 저장됩니다. 구조체 필드 이름과 타입은 데이터베이스 컬럼 이름 및 타입과 일치해야 합니다.

*   [`DB.Query`](https://pkg.go.dev/database/sql#DB.Query)를 사용하여 `SELECT` 문을 실행하고, 지정된 artist name을 가진 앨범들을 조회하세요.

`Query`의 첫 번째 파라미터는 SQL 문입니다. 해당 파라미터 이후에 모든 타입의 파라미터를 0개 이상 전달할 수 있습니다. 이를 통해 SQL 문 내의 파라미터 값을 지정할 수 있습니다. SQL 문과 파라미터 값을 분리함으로써 (예를 들어 `fmt.Sprintf`를 사용하여 결합하는 대신), `database/sql` 패키지가 SQL 텍스트와 값을 분리하여 전송하게 하여 SQL 인젝션 위험을 제거할 수 있습니다.

*   함수가 종료될 때 `rows`가 보유한 모든 리소스가 해제되도록 `rows` 닫기를 `defer` 하십시오.

*   반환된 행들을 루프(loop)하며, [`Rows.Scan`](https://pkg.go.dev/database/sql#Rows.Scan)을 사용하여 각 행의 컬럼 값을 `Album` 구조체 필드에 할당합니다.

`Scan`은 컬럼 값이 기록될 Go 값들의 포인터 리스트를 인자로 받습니다. 여기서는 `&` 연산자를 사용하여 생성한 `alb` 변수 필드들의 포인터를 전달합니다. `Scan`은 이 포인터들을 통해 구조체 필드를 업데이트합니다.

*   루프 내부에서, 컬럼 값들을 구조체 필드로 스캔하는 과정에서 발생하는 에러를 확인하십시오.

*   루프 내부에서, 새로운 `alb`를 `albums` 슬라이스에 append 하세요.

*   루프가 끝난 후, `rows.Err`를 사용하여 전체 쿼리에서 발생한 에러가 있는지 확인하십시오. 쿼리 자체가 실패한 경우, 여기서 에러를 확인하는 것이 결과가 불완전하다는 것을 알 수 있는 유일한 방법입니다.

3. `main` 함수를 업데이트하여 `albumsByArtist`를 호출하세요.

`func main` 끝에 다음 코드를 추가하세요.

```
    albums, err := albumsByArtist("John Coltrane")
    if err != nil {
    	log.Fatal(err)
    }
    fmt.Printf("Albums found: %v\n", albums)
    ```

새 코드에서는 다음과 같이 처리합니다:

*   추가한 `albumsByArtist` 함수를 호출하고, 그 반환 값을 새로운 `albums` 변수에 할당하세요.

*   결과를 출력합니다.

#### 코드 실행하기

`main.go` 파일이 포함된 디렉토리의 명령줄에서 코드를 실행하세요.

```
$ go run .
Connected!
Albums found: [{1 Blue Train John Coltrane 56.99} {2 Giant Steps John Coltrane 63.99}]
```

다음으로, 단일 행을 쿼리하겠습니다.

## 단일 행 쿼리 {#single_row}

이 섹션에서는 Go를 사용하여 데이터베이스에서 단일 행을 쿼리하는 방법을 알아봅니다.

최대 단일 행만 반환할 것이라고 확신하는 SQL 문장의 경우, `Query` 루프를 사용하는 것보다 더 간단한 `QueryRow`를 사용할 수 있습니다.

#### 코드 작성하기

1. `albumsByArtist` 아래에 다음 `albumByID` 함수를 붙여넣으세요.

```go
    // albumByID는 지정된 ID의 앨범을 쿼리합니다.
    func albumByID(id int64) (Album, error) {
    	// 반환된 행의 데이터를 저장할 앨범 변수입니다.
    	var alb Album
```

```go
row := db.QueryRow("SELECT * FROM album WHERE id = ?", id)
    	if err := row.Scan(&alb.ID, &alb.Title, &alb.Artist, &alb.Price); err != nil {
    		if err == sql.ErrNoRows {
    			return alb, fmt.Errorf("albumsById %d: no such album", id)
    		}
    		return alb, fmt.Errorf("albumsById %d: %v", id, err)
    	}
    	return alb, nil
    }
    ```

이 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   지정된 ID로 앨범을 조회하는 `SELECT` 문을 실행하기 위해 [`DB.QueryRow`](https://pkg.go.dev/database/sql#DB.QueryRow)를 사용하세요.

`sql.Row`를 반환합니다. 호출하는 코드(사용자의 코드!)를 단순화하기 위해, `QueryRow`는 에러를 반환하지 않습니다. 대신, 쿼리 에러(예: `sql.ErrNoRows`)를 나중에 `Rows.Scan`에서 반환하도록 처리합니다.

*   [`Row.Scan`](https://pkg.go.dev/database/sql#Row.Scan)을 사용하여 컬럼 값을 구조체 필드로 복사하세요.

*   `Scan`에서 발생한 에러가 있는지 확인하십시오.

특수 에러인 `sql.ErrNoRows`는 쿼리 결과로 반환된 행이 없음을 나타냅니다. 일반적으로 이 에러는 여기에서 "no such album"과 같이 더 구체적인 텍스트로 대체하는 것이 좋습니다.

2. `main`이 `albumByID`를 호출하도록 업데이트합니다.

`func main` 끝에 다음 코드를 추가하세요.

```
    // 쿼리를 테스트하기 위해 여기에 ID 2를 하드코딩합니다.
    alb, err := albumByID(2)
    if err != nil {
    	log.Fatal(err)
    }
    fmt.Printf("Album found: %v\n", alb)
    ```

새로운 코드에서는 이제 다음과 같이 수행합니다:

*   추가한 `albumByID` 함수를 호출하세요.

*   반환된 album ID를 출력합니다.

#### 코드 실행하기

`main.go`가 포함된 디렉토리의 커맨드 라인에서 코드를 실행하십시오.

```
$ go run .
Connected!
Albums found: [{1 Blue Train John Coltrane 56.99} {2 Giant Steps John Coltrane 63.99}]
Album found: {2 Giant Steps John Coltrane 63.99}
```

다음으로, 데이터베이스에 앨범을 추가하겠습니다.

## 데이터 추가 {#add_data}

이 섹션에서는 Go를 사용하여 SQL `INSERT` 문을 실행하고 데이터베이스에 새 행을 추가하는 방법을 알아봅니다.

데이터를 반환하는 SQL 문과 함께 `Query` 및 `QueryRow`를 사용하는 방법을 살펴보았습니다. 데이터를 반환하지 _않는_ SQL 문을 실행하려면 `Exec`를 사용합니다.

#### 코드 작성하기

1. `albumByID` 아래에, 데이터베이스에 새로운 앨범을 삽입하는 다음 `addAlbum` 함수를 붙여넣은 후 main.go를 저장하세요.

```
    // addAlbum은 지정된 앨범을 데이터베이스에 추가하고,
    // 새 항목의 앨범 ID를 반환합니다.
    func addAlbum(alb Album) (int64, error) {
    	result, err := db.Exec("INSERT INTO album (title, artist, price) VALUES (?, ?, ?)", alb.Title, alb.Artist, alb.Price)
    	if err != nil {
    		return 0, fmt.Errorf("addAlbum: %v", err)
    	}
    	id, err := result.LastInsertId()
    	if err != nil {
    		return 0, fmt.Errorf("addAlbum: %v", err)
    	}
    	return id, nil
    }
    ```

이 코드에서 귀하는 다음을 수행합니다:

*   `INSERT` 문을 실행하려면 [`DB.Exec`](https://pkg.go.dev/database/sql#DB.Exec)를 사용하세요.

`Query`와 마찬가지로, `Exec`는 SQL 문과 그 뒤에 이어지는 SQL 문의 매개변수 값들을 인자로 받습니다.

*   `INSERT` 시도 중 발생한 에러가 있는지 확인하십시오.

*   [`Result.LastInsertId`](https://pkg.go.dev/database/sql#Result.LastInsertId)를 사용하여 삽입된 데이터베이스 행의 ID를 가져옵니다.

*   ID를 가져오려는 시도에서 오류가 발생했는지 확인합니다.

2. `main`이 새로운 `addAlbum` 함수를 호출하도록 업데이트합니다.

`func main` 끝에 다음 코드를 추가하세요.

```
    albID, err := addAlbum(Album{
    	Title:  "The Modern Sound of Betty Carter",
    	Artist: "Betty Carter",
    	Price:  49.99,
    })
    if err != nil {
    	log.Fatal(err)
    }
    fmt.Printf("ID of added album: %v\n", albID)
    ```

새 코드에서는 이제 다음과 같이 수행합니다:

*   `addAlbum`을 호출하여 새 앨범을 추가하고, 추가되는 앨범의 ID를 `albID` 변수에 할당하세요.

#### 코드 실행

`main.go` 파일이 포함된 디렉토리의 명령줄에서 코드를 실행하세요.

```
$ go run .
Connected!
Albums found: [{1 Blue Train John Coltrane 56.99} {2 Giant Steps John Coltrane 63.99}]
Album found: {2 Giant Steps John Coltrane 63.99}
ID of added album: 5
```

## 결론 {#conclusion}

축하합니다! 방금 Go를 사용하여 관계형 데이터베이스에서 간단한 작업을 수행하셨습니다.

추천 다음 주제:

*   여기서 간략하게 다룬 주제들에 대해 더 자세한 정보를 제공하는 데이터 액세스 가이드를 살펴보십시오.

*   Go가 처음이시라면, [Effective Go](/doc/effective_go)와 [How to write Go code](/doc/code)에 설명된 유용한 모범 사례들을 확인해 보세요.

*   [Go Tour](/tour/)는 Go의 기본 개념을 단계별로 배울 수 있는 훌륭한 입문서입니다.

## 완성된 코드 {#completed_code}

이 섹션에는 이 튜토리얼을 통해 구축하는 애플리케이션의 코드가 포함되어 있습니다.

```go
package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"

	"github.com/go-sql-driver/mysql"
)

var db *sql.DB

type Album struct {
	ID     int64
	Title  string
	Artist string
	Price  float32
}

func main() {
	// 연결 속성을 캡처합니다.
	cfg := mysql.NewConfig()
	cfg.User = os.Getenv("DBUSER")
	cfg.Passwd = os.Getenv("DBPASS")
	cfg.Net = "tcp"
	cfg.Addr = "127.0.0.1:3306"
	cfg.DBName = "recordings"

	// 데이터베이스 핸들을 가져옵니다.
	var err error
	db, err = sql.Open("mysql", cfg.FormatDSN())
	if err != nil {
		log.Fatal(err)
	}

	pingErr := db.Ping()
	if pingErr != nil {
		log.Fatal(pingErr)
	}
	fmt.Println("Connected!")

	albums, err := albumsByArtist("John Coltrane")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Albums found: %v\n", albums)

	// 쿼리를 테스트하기 위해 ID 2를 하드코딩합니다.
	alb, err := albumByID(2)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Album found: %v\n", alb)

	albID, err := addAlbum(Album{
		Title:  "The Modern Sound of Betty Carter",
		Artist: "Betty Carter",
		Price:  49.99,
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("ID of added album: %v\n", albID)
}

// albumsByArtist는 지정된 아티스트 이름을 가진 앨범을 쿼리합니다.
func albumsByArtist(name string) ([]Album, error) {
	// 반환된 행의 데이터를 저장할 albums 슬라이스입니다.
	var albums []Album

	rows, err := db.Query("SELECT * FROM album WHERE artist = ?", name)
	if err != nil {
		return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
	}
	defer rows.Close()
	// 행을 반복하며, Scan을 사용하여 컬럼 데이터를 구조체 필드에 할당합니다.
	for rows.Next() {
		var alb Album
		if err := rows.Scan(&alb.ID, &alb.Title, &alb.Artist, &alb.Price); err != nil {
			return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
		}
		albums = append(albums, alb)
	}
	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
	}
	return albums, nil
}

// albumByID는 지정된 ID를 가진 앨범을 쿼리합니다.
func albumByID(id int64) (Album, error) {
	// 반환된 행의 데이터를 저장할 album입니다.
	var alb Album
```

```go
row := db.QueryRow("SELECT * FROM album WHERE id = ?", id)
	if err := row.Scan(&alb.ID, &alb.Title, &alb.Artist, &alb.Price); err != nil {
		if err == sql.ErrNoRows {
			return alb, fmt.Errorf("albumsById %d: no such album", id)
		}
		return alb, fmt.Errorf("albumsById %d: %v", id, err)
	}
	return alb, nil
}

// addAlbum은 지정된 앨범을 데이터베이스에 추가하고,
// 새 항목의 앨범 ID를 반환합니다.
func addAlbum(alb Album) (int64, error) {
	result, err := db.Exec("INSERT INTO album (title, artist, price) VALUES (?, ?, ?)", alb.Title, alb.Artist, alb.Price)
	if err != nil {
		return 0, fmt.Errorf("addAlbum: %v", err)
	}
	id, err := result.LastInsertId()
	if err != nil {
		return 0, fmt.Errorf("addAlbum: %v", err)
	}
	return id, nil
}
```
