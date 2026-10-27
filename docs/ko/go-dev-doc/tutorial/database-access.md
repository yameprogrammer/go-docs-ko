<!--{
  "제목": "튜토리얼: 관계형 데이터베이스 접근",
  "내비게이션": true
}-->

이 튜토리얼에서는 Go와 표준 라이브러리의 `database/sql` 패키지를 사용하여 관계형 데이터베이스에 접근하는 기본 사항을 소개합니다.

이 튜토리얼을 최대한 활용하려면 Go와 그 도구에 대한 기본적인 이해가 필요합니다. Go에 처음 접하신다면, [튜토리얼: Go 시작하기](/doc/tutorial/getting-started)를 참고하여 빠르게 시작할 수 있습니다.

[`database/sql`](https://pkg.go.dev/database/sql) 패키지는 데이터베이스에 연결하고, 트랜잭션을 실행하고, 진행 중인 작업을 취소하는 등의 기능을 위한 타입과 함수를 포함합니다. 패키지를 사용하는 방법에 대한 자세한 내용은 [데이터베이스 액세스](/doc/database/index)를 참조하십시오.

이 튜토리얼에서는 데이터베이스를 생성하고, 그런 다음 데이터베이스에 액세스하는 코드를 작성하는 방법을 배울 수 있습니다. 예시 프로젝트는 빈티지 재즈 레코드에 대한 데이터 저장소입니다.

이 튜토리얼에서는 다음 섹션을 따라 진행합니다:

1. 코드용 폴더를 만듭니다.
2. 데이터베이스를 설정합니다.
3. 데이터베이스 드라이버를 가져옵니다.
4. 데이터베이스 핸들을 얻고 연결합니다.
5. 여러 행에 대한 쿼리를 실행합니다.
6. 단일 행에 대한 쿼리를 실행합니다.
7. 데이터를 추가합니다.

**참고:** 다른 튜토리얼은 [튜토리얼](/doc/tutorial/index.html)에서 확인하십시오.

## 필수 구성 요소 {#prerequisites}

*   **MySQL 관계형 데이터베이스 관리 시스템(DBMS) 설치.**
    참조: [MySQL 설치 가이드](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/)
*   **Go 설치.** 설치 방법에 대한 내용은 [Installing Go](/doc/install)를 참조하십시오.
*   **코드 편집 도구.** 사용하시는 텍스트 편집기 모두 사용할 수 있습니다.
*   **명령줄 터미널.** Go는 Linux 및 Mac의 모든 터미널, PowerShell 또는 Windows의 cmd에서 잘 작동합니다.

## 코드를 위한 폴더 만들기 {#create_folder}

```
mkdir my_code
```

시작하려면, 작성할 코드를 위한 폴더를 만드세요.

1. 명령 프롬프트를 열고 홈 디렉토리로 이동합니다.

리눅스 또는 맥에서:

```
    $ cd
```

On Windows:

```
    C:\> cd %HOMEPATH%
```

이 튜토리얼의 나머지 부분에서는 프롬프트로 "$"를 사용하겠습니다.
    저희가 사용하는 명령은 Windows에서도 작동합니다.

2. 명령 프롬프트에서, 코드용 디렉토리를 생성합니다. 디렉토리 이름은 `data-access` 입니다.

```
    $ mkdir data-access
    $ cd data-access
    ```

3. 이 튜토리얼에서 추가할 의존성을 관리할 수 있는 모듈을 만듭니다.

`go mod init` 명령을 실행하고, 새 코드의 모듈 경로를 지정합니다.

```
    $ go mod init example/data-access
    go: 생성 중인 새 go.mod: 모듈 example/data-access
    ```

이 명령은 추가하는 종속성을 추적하기 위한 `go.mod` 파일을 생성합니다. 자세한 내용은 다음 문서를 참조하십시오:
    [종속성 관리](/doc/modules/managing-dependencies).

**참고:** 실제 개발에서는 특정 요구 사항에 더 적합한 모듈 경로를 지정해야 합니다. 자세한 내용은 [의존성 관리](/doc/modules/managing-dependencies#naming_module)를 참조하세요.

다음으로, 데이터베이스를 생성합니다.

## 데이터베이스 설정 {#set_up_database}

이 단계에서는 작업할 데이터베이스를 생성합니다. CLI를 사용하여 DBMS 자체에서 데이터베이스와 테이블을 만들고, 데이터를 추가할 수 있습니다.

빈티지 재즈 레코드에 대한 데이터를 포함하는 데이터베이스를 생성할 것입니다.

이 코드는 [MySQL CLI](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)를 사용하지만, 대부분의 DBMS는 유사한 기능을 갖춘 자체 CLI를 가지고 있습니다.

1. 새 명령 프롬프트를 엽니다.
2. 명령줄에서 DBMS에 로그인합니다 (다음 예시를 MySQL에 적용).

```
    $ mysql -u root -p
    비밀번호를 입력하세요:
```

```

3. `mysql` 명령 프롬프트에서 데이터베이스를 생성합니다.

```
    mysql> create database recordings;
```

4. 새로 만든 데이터베이스로 변경하여 테이블을 추가할 수 있습니다.

```
    mysql> use recordings;
    데이터베이스 변경됨
```

5. 텍스트 편집기에서, 데이터 접근 폴더에 `create-tables.sql`이라는 파일을 생성하여 테이블을 추가하는 SQL 스크립트를 저장합니다.
6. 파일에 다음 SQL 코드를 붙여넣은 다음 파일을 저장합니다.

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

```markdown
```sql
INSERT INTO album
      (title, artist, price)
    VALUES
      ('Blue Train', 'John Coltrane', 56.99),
      ('Giant Steps', 'John Coltrane', 63.99),
      ('Jeru', 'Gerry Mulligan', 17.99),
      ('Sarah Vaughan', 'Sarah Vaughan', 34.98);
```

이 SQL 코드에서, 다음과 같은 작업을 수행합니다:

*   `album` 테이블을 삭제 (제거) 합니다. 이 명령을 먼저 실행하면 나중에 스크립트를 다시 실행할 때 테이블을 처음부터 다시 시작하는 것이 더 쉬워집니다.

*   `album` 테이블을 다음과 같은 네 개의 컬럼으로 생성합니다: `title`, `artist`, `price`.
        각 행의 `id` 값은 DBMS에 의해 자동으로 생성됩니다.

*   4개의 행을 추가하고 값 설정.

7. `mysql` 명령 프롬프트에서, 새로 만든 스크립트를 실행합니다.

다음 형식으로 `source` 명령어를 사용하십시오:

```
    mysql> source /path/to/create-tables.sql
```

8. DBMS 명령 프롬프트에서 `SELECT` 문을 사용하여 테이블이 데이터와 함께 성공적으로 생성되었는지 확인합니다.

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

다음으로, 연결을 설정하여 쿼리할 수 있도록 Go 코드를 작성합니다.

## 데이터베이스 드라이버 찾고 임포트하기 {#import_driver}

데이터베이스 드라이버를 찾고 임포트하는 방법은 다음과 같습니다.

1.  **드라이버 찾기:**
    *   사용하려는 데이터베이스 시스템에 맞는 드라이버를 찾아야 합니다. 예를 들어, MySQL 데이터베이스를 사용하려면 `mysql` 드라이버가 필요합니다.
    *   드라이버는 종종 데이터베이스 시스템의 공식 웹사이트나 패키지 관리자에서 제공됩니다.

2.  **드라이버 설치:**
    *   드라이버를 다운로드한 후, 프로젝트에 설치해야 합니다.
    *   설치 방법은 사용 중인 운영체제 및 패키지 관리자에 따라 다릅니다. 예를 들어, Python 환경에서 `pip install mysql-connector-python`와 같이 설치할 수 있습니다.

3.  **드라이버 임포트:**
    *   드라이버를 설치한 후, 프로젝트 코드에서 해당 드라이버를 임포트하여 사용할 수 있습니다.
    *   예를 들어, Python 코드에서 `import mysql.connector`와 같이 임포트할 수 있습니다.

다음은 간단한 예제 코드입니다.

```python
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="yourdatabase"
)

print(mydb)
```

위 코드는 `mysql.connector` 드라이버를 사용하여 MySQL 데이터베이스에 연결하는 방법을 보여줍니다. `host`, `user`, `password`, `database`를 실제 값으로 바꿔야 합니다.

이제 데이터가 포함된 데이터베이스를 가지고 있으므로, Go 코드를 시작하세요.

데이터베이스 드라이버를 찾아서 가져오세요. 이 드라이버는 `database/sql` 패키지의 함수를 통해 보내는 요청을, 데이터베이스가 이해할 수 있는 형식으로 변환합니다.

1. 브라우저에서 [SQLDrivers](/wiki/SQLDrivers) 위키 페이지를 방문하여 사용할 수 있는 드라이버를 식별합니다.

페이지에 있는 목록을 사용하여 사용할 드라이버를 식별합니다. 이 튜토리얼에서 MySQL에 액세스하려면 다음 드라이버를 사용합니다.
    [Go-MySQL-Driver](https://github.com/go-sql-driver/mysql/).

2. 드라이버의 패키지 이름을 확인하세요 -- 여기는 `github.com/go-sql-driver/mysql` 입니다.

3. 텍스트 편집기를 사용하여 Go 코드를 작성할 파일과,
    이전에 생성한 data-access 디렉터리에 main.go라는 이름으로 저장합니다.

4. `main.go` 파일에 다음 코드를 붙여서 `driver` 패키지를 가져옵니다.

```
    패키지 main
```

```
import "github.com/go-sql-driver/mysql"
```

이 코드에서, 다음을 수행합니다:

*   `main` 패키지에 코드를 추가하여 독립적으로 실행할 수 있습니다.

*   `github.com/go-sql-driver/mysql` 드라이버를 가져옵니다.

드라이버가 임포트되면, 이제 데이터베이스에 접근하기 위한 코드를 작성하기 시작합니다.

## 데이터베이스 핸들 획득 및 연결 {#get_handle}

이제 데이터베이스 핸들을 사용하여 데이터베이스에 액세스하는 Go 코드를 작성합니다.

`sql.DB` 구조체의 포인터를 사용하면, 특정 데이터베이스에 대한 액세스를 나타냅니다.

```markdown
#### 코드를 작성하세요
```

1. `main.go` 파일에, 새로 추가한 `import` 코드 아래에 다음 Go 코드를 붙여넣습니다.
    데이터베이스 핸들을 생성하는 Go 코드.

```
    var db *sql.DB
```

```markdown
```go
package main

import (
	"os"
)

func main() {
	// 연결 속성을 캡처합니다.
	cfg := mysql.NewConfig()
	cfg.User = os.Getenv("DBUSER")
	cfg.Passwd = os.Getenv("DBPASS")
	cfg.Net = "tcp"
	cfg.Addr = "127.0.0.1:3306"
	cfg.DBName = "recordings"
}
```

// 데이터베이스 핸들을 가져옵니다.
    	var err error
    	db, err = sql.Open("mysql", cfg.FormatDSN())
    	if err != nil {
    		log.Fatal(err)
    	}

```
    	pingErr := db.Ping()
    	if pingErr != nil {
    		log.Fatal(pingErr)
    	}
    	fmt.Println("Connected!")
```

이 코드에서, 당신은:

*   `db` 변수를 `[*sql.DB](https://pkg.go.dev/database/sql#DB)` 유형으로 선언합니다.
        이것은 데이터베이스 핸들입니다.

`db`를 전역 변수로 만드는 것은 이 예제를 단순화합니다.
        실제 환경에서는 전역 변수를 피하는 것이 좋습니다. 예를 들어, 필요한 함수에 변수를 전달하거나, 구조체 내에 래핑하는 방식으로 사용할 수 있습니다.

*   `Config` (https://pkg.go.dev/github.com/go-sql-driver/mysql#Config)를 사용하세요.
    -- 그리고 `FormatDSN` (https://pkg.go.dev/github.com/go-sql-driver/mysql#Config.FormatDSN) 메서드를 사용하여 연결 속성을 수집하고, 이를 연결 문자열용 DSN으로 형식화합니다.

`Config` 구조체는 연결 문자열보다 더 읽기 쉬운 코드를 만드는 데 도움이 됩니다.

*   `sql.Open` 함수를 호출하여 `db` 변수를 초기화하고, `FormatDSN` 함수의 반환 값을 전달합니다.

*   `sql.Open`에서 오류를 확인합니다. 예를 들어, 데이터베이스 연결 특정 정보가 올바르게 구성되지 않은 경우에 실패할 수 있습니다.

코드를 단순화하기 위해, `log.Fatal`을 호출하여 실행을 종료하고 오류를 콘솔에 출력합니다. 실제 코드에서는 오류를 더 깔끔하게 처리하는 것이 좋습니다.

*   `[`DB.Ping`](https://pkg.go.dev/database/sql#DB.Ping)를 호출하여
        데이터베이스에 연결하는 데 문제가 없는지 확인합니다. 실행 시간에,
        `sql.Open`이 즉시 연결하지 않을 수 있으며, 이는 드라이버에 따라 다릅니다.
        여기서는 `Ping`을 사용하여 `database/sql` 패키지가 필요한 경우 연결할 수 있는지 확인합니다.

*   `Ping`에서 오류를 확인하여, 연결이 실패한 경우를 처리합니다.

*   `Ping` 연결이 성공하면 메시지를 출력합니다.

2. main.go 파일의 상단, 패키지 선언 바로 아래에,
    새로 작성한 코드를 지원하기 위해 필요한 패키지를 임포트합니다.

이제 파일의 상단은 다음과 같아야 합니다:

```
    패키지 main
```

```
import (
    	"database/sql"
    	"fmt"
    	"log"
    	"os"
)
```

```
github.com/go-sql-driver/mysql"
)
```

3. `main.go` 저장.

#### 코드를 실행합니다

1. MySQL 드라이버 모듈을 종속성으로 추적을 시작합니다.

`go get`를 사용하여 `github.com/go-sql-driver/mysql` 모듈을 현재 모듈의 종속성으로 추가합니다. 현재 디렉토리의 코드를 위한 종속성을 지정하려면 점(.)을 사용합니다.

```
    $ go get .
    go: 추가됨: filippo.io/edwards25519 v1.1.0
    go: 추가됨: github.com/go-sql-driver/mysql v1.8.1
```

Go는 이 종속성을 다운로드했습니다. 이는 이전 단계에서 `import` 선언에 추가했기 때문입니다. 종속성 추적에 대한 자세한 내용은 [종속성 추가](/doc/modules/managing-dependencies#adding_dependency)를 참조하십시오.

2. 명령 프롬프트에서 `DBUSER` 및 `DBPASS` 환경 변수를 설정하여 Go 프로그램에서 사용합니다.

리눅스 또는 맥에서:

```
    $ export DBUSER=사용자이름
    $ export DBPASS=비밀번호
    ```

온 Windows에서:

```
    C:\Users\you\data-access> set DBUSER=사용자이름
    C:\Users\you\data-access> set DBPASS=비밀번호
```

3. 명령줄에서 `main.go` 파일이 있는 디렉토리에서 다음 명령을 실행하여 코드를 실행합니다.
    `go run` 명령 뒤에 점(.)을 추가하여 "현재 디렉토리에 있는 패키지를 실행"한다는 의미를 나타냅니다.

```
    go run .
    연결되었습니다!
    ```

연결할 수 있습니다! 다음으로, 데이터를 쿼리합니다.

## 여러 행에 대한 쿼리 {#multiple_rows}

이 섹션에서는 Go를 사용하여 여러 행을 반환하도록 설계된 SQL 쿼리를 실행합니다.

SQL 문이 여러 행을 반환할 수 있는 경우, `database/sql` 패키지의 `Query` 메서드를 사용하고, 반환되는 행을 반복합니다. (나중에 단일 행을 쿼리하는 방법을 [Query for a single row](#single_row) 섹션에서 배울 수 있습니다.)
#### 코드를 작성하세요

1. `main.go` 파일에서 `func main` 바로 위쪽에 다음 `Album` 구조체 정의를 붙여넣습니다. 이 구조체는 쿼리에서 반환된 행 데이터를 저장하는 데 사용됩니다.

```
    type Album struct {
    	ID     int64
    	Title  string
    	Artist string
    	Price  float32
    }
```

2. `func main` 아래에 다음 `albumsByArtist` 함수를 붙여서
    데이터베이스를 쿼리합니다.

```
    // albumsByArtist는 지정된 아티스트 이름과 일치하는 앨범을 쿼리합니다.
    func albumsByArtist(name string) ([]Album, error) {
    	// 반환된 행에서 데이터를 저장할 앨범 슬라이스.
    	var albums []Album
```

```
	rows, err := db.Query("SELECT * FROM album WHERE artist = ?", name)
    	if err != nil {
    		return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
    	}
    	defer rows.Close()
    	// rows를 반복 처리, Scan을 사용하여 컬럼 데이터를 구조체 필드에 할당합니다.
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

이 코드에서, 다음을 수행합니다:

*   `Album` 유형으로 정의한 `albums` 슬라이스를 선언합니다. 이 슬라이스는 반환된 행의 데이터를 저장합니다. 구조체 필드 이름과 유형은 데이터베이스 열 이름과 유형과 일치합니다.

*   `DB.Query`를 사용하여
        지정된 아티스트 이름과 일치하는 앨범을 쿼리하는 `SELECT` 문을 실행합니다.

`Query` 함수의 첫 번째 매개변수는 SQL 문입니다. 매개변수 뒤에는 0개 이상의 모든 유형의 매개변수를 전달할 수 있습니다. 이를 통해 SQL 문의 매개변수 값에 대한 값을 지정할 수 있습니다. SQL 문과 매개변수 값을 연결하는 대신 (예: `fmt.Sprintf`) 분리함으로써, `database/sql` 패키지가 SQL 텍스트와 별도로 값을 전달할 수 있게 되어 SQL 삽입 위험을 제거합니다.

*   `rows`를 닫는 것을 `defer`하여, 함수가 종료될 때 해당 자원이 해제되도록 합니다.

*   반환된 행을 순회하면서,
        [`Rows.Scan`](https://pkg.go.dev/database/sql#Rows.Scan)를 사용하여
        각 행의 열 값을 `Album` 구조체의 필드에 할당합니다.

`Scan`은 Go 값의 포인터 목록을 받습니다. 여기서, 열 값은 `alb` 변수에 생성된 필드 포인터를 통해 쓰여집니다. `&` 연산자를 사용하여 생성된 `alb` 변수의 필드 포인터를 전달합니다.
`Scan`은 포인터를 통해 구조체 필드를 업데이트합니다.

*   루프 안에서, 구조체의 필드에 열 값을 스캔하는 동안 발생하는 오류를 확인합니다.

*   루프 안에서 새로운 `alb`를 `albums` 슬라이스에 추가합니다.

*   루프가 완료된 후, 전체 쿼리의 오류를 확인합니다. `rows.Err`를 사용합니다. 쿼리 자체에 오류가 있는 경우, 오류를 확인하는 것이 결과가 불완전함을 알 수 있는 유일한 방법입니다.

3. `main` 함수를 업데이트하여 `albumsByArtist` 함수를 호출합니다.

`func main`의 끝에 다음 코드를 추가하십시오.

```
    albums, err := albumsByArtist("John Coltrane")
    if err != nil {
    	log.Fatal(err)
    }
    fmt.Printf("앨범 목록: %v\n", albums)
```

새로운 코드에서는 다음을 수행합니다:

*   `albumsByArtist` 함수를 호출하고, 반환 값을 새로운 `albums` 변수에 할당합니다.

*   결과를 출력합니다.

#### 코드를 실행하세요

명령줄에서 main.go 파일이 있는 디렉토리에서 코드를 실행합니다.

```
$ go run .
연결되었습니다!
앨범 발견: [{1 Blue Train John Coltrane 56.99} {2 Giant Steps John Coltrane 63.99}]
```

다음으로, 단일 행을 쿼리합니다.

## 단일 행 쿼리 {#single_row}

이 섹션에서는 Go를 사용하여 데이터베이스에서 단일 행을 쿼리하는 방법을 보여드리겠습니다.

SQL 문이 최대 1개의 행만 반환할 것으로 예상되는 경우, `QueryRow`를 사용하는 것이 `Query` 루프를 사용하는 것보다 간단합니다.

```markdown
#### 코드를 작성하세요

1. `albumsByArtist` 아래에 다음 `albumByID` 함수를 붙여넣습니다.

```
    // albumByID은 지정된 ID를 가진 앨범을 쿼리합니다.
    func albumByID(id int64) (Album, error) {
    	// 반환된 행에서 데이터를 저장할 앨범 변수.
    	var alb Album
```

```
row := db.QueryRow("SELECT * FROM album WHERE id = ?", id)
    	if err := row.Scan(&alb.ID, &alb.Title, &alb.Artist, &alb.Price); err != nil {
    		if err == sql.ErrNoRows {
    			return alb, fmt.Errorf("albumsById %d: 해당 앨범이 없습니다", id)
    		}
    		return alb, fmt.Errorf("albumsById %d: %v", id, err)
    	}
    	return alb, nil
    }
```

이 코드에서, 다음과 같은 작업을 수행합니다:

*   `[`DB.QueryRow`](https://pkg.go.dev/database/sql#DB.QueryRow)를 사용하여 지정된 ID를 가진 앨범을 쿼리하는 `SELECT` 문을 실행합니다.

이것은 `sql.Row`를 반환합니다. 호출하는 코드(즉, `your code!`)를 단순화하기 위해 `QueryRow`는 오류를 반환하지 않습니다. 대신, `Rows.Scan`에서 발생하는 모든 오류(예: `sql.ErrNoRows`)를 나중에 반환하도록 처리합니다.

*   `Row.Scan` 함수를 사용하여 컬럼 값을 구조체 필드에 복사합니다.

*   `Scan`에서 오류가 있는지 확인합니다.

특수한 오류 `sql.ErrNoRows`는 쿼리가 행을 반환하지 않았음을 나타냅니다. 일반적으로 이 오류는 더 구체적인 텍스트로 대체하는 것이 좋습니다. 예를 들어, "앨범을 찾을 수 없습니다"와 같이.

2. `main` 함수를 `albumByID`를 호출하도록 업데이트합니다.

`func main`의 끝에 다음 코드를 추가합니다.

```
    // ID 2를 직접 입력하여 쿼리를 테스트합니다.
    alb, err := albumByID(2)
    if err != nil {
    	log.Fatal(err)
    }
    fmt.Printf("앨범 찾음: %v\n", alb)
```

새로운 코드에서는 다음과 같이 변경되었습니다:

*   `albumByID` 함수를 추가한 것을 호출합니다.

*   반환된 앨범 ID를 출력합니다.

#### 코드를 실행하세요

명령줄에서 `main.go` 파일이 있는 디렉토리에서 코드를 실행합니다.

```
$ go run .
연결되었습니다!
앨범 발견: [{1 Blue Train John Coltrane 56.99} {2 Giant Steps John Coltrane 63.99}]
앨범 발견: {2 Giant Steps John Coltrane 63.99}
```

다음으로, 데이터베이스에 앨범을 추가합니다.

## 데이터 추가 {#add_data}

이 섹션에서는 Go를 사용하여 SQL `INSERT` 문을 실행하여 데이터베이스에 새 행을 추가합니다.

다음과 같이 `Query` 및 `QueryRow`를 사용하여 데이터를 반환하는 SQL 문을 사용하는 방법을 보셨습니다. 데이터가 반환되지 않는 SQL 문을 실행하려면 `Exec`를 사용합니다.

```markdown
#### 코드를 작성하세요

1. `albumByID` 아래에 다음 `addAlbum` 함수를 붙여넣어 새로운
    앨범을 데이터베이스에 삽입하고, `main.go`를 저장합니다.

```
    // addAlbum은 지정된 앨범을 데이터베이스에 추가하고, 새로운 항목의 앨범 ID를 반환합니다.
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

이 코드에서는 다음을 수행합니다:

*   `DB.Exec`를 사용하여
        `INSERT` 문을 실행합니다.

`Query`와 `Exec` 모두 SQL 문과 함께 SQL 문에 대한 매개변수 값을 취합니다.

*   `INSERT` 시도 중 오류를 확인합니다.

*   삽입된 데이터베이스 행의 ID를 가져오기 위해
        [`Result.LastInsertId`](https://pkg.go.dev/database/sql#Result.LastInsertId)를 사용합니다.

*   ID를 가져오는 시도 중 오류가 있는지 확인합니다.

2. `main` 함수를 수정하여 새로운 `addAlbum` 함수를 호출하도록 합니다.

`func main`의 끝에 다음 코드를 추가하세요.

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

새로운 코드에서는, 이제 다음을 수행합니다:

*   `addAlbum` 함수를 호출하여 새로운 앨범을 생성하고, 생성된 앨범의 ID를 `albID` 변수에 할당합니다.

#### 코드를 실행

명령줄에서 `main.go` 파일이 있는 디렉토리에서 코드를 실행합니다.

```
$ go run .
연결되었습니다!
앨범 발견: [{1 Blue Train John Coltrane 56.99} {2 Giant Steps John Coltrane 63.99}]
앨범 발견: {2 Giant Steps John Coltrane 63.99}
추가된 앨범의 ID: 5
```

## 결론 {#conclusion}

축하합니다! 이제 Go를 사용하여 관계형 데이터베이스와 간단한 작업을 수행할 수 있습니다.

제안된 다음 주제:

*   자세한 정보가 포함된 데이터 액세스 가이드도 참고해 보세요.

*   Go를 처음 접하시는 경우, 다음과 같은 유용한 실무 지침을 참고하시면 도움이 될 것입니다:
    [Effective Go](/doc/effective_go) 및 [How to write Go code](/doc/code)

*   [Go Tour](/tour/)는 Go의 기본 개념에 대한 훌륭한 단계별 소개입니다.

## 완성된 코드 {#completed_code}

이 섹션에는 이 튜토리얼을 사용하여 구축한 애플리케이션의 코드가 포함되어 있습니다.

```
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

	// 쿼리를 테스트하기 위해 ID 2를 하드 코딩합니다.
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
	// 데이터를 저장할 앨범 슬라이스
	var albums []Album

	rows, err := db.Query("SELECT * FROM album WHERE artist = ?", name)
	if err != nil {
		return nil, fmt.Errorf("albumsByArtist %q: %v", name, err)
	}
	defer rows.Close()
	// 행을 반복하고, Scan을 사용하여 열 데이터를 구조체 필드에 할당합니다.
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
	// 반환된 행을 저장할 앨범
	var alb Album
```

```markdown
```go
row := db.QueryRow("SELECT * FROM album WHERE id = ?", id)
	if err := row.Scan(&alb.ID, &alb.Title, &alb.Artist, &alb.Price); err != nil {
		if err == sql.ErrNoRows {
			return alb, fmt.Errorf("albumsById %d: 해당 알बम이 없습니다", id)
		}
		return alb, fmt.Errorf("albumsById %d: %v", id, err)
	}
	return alb, nil
}

// addAlbum은 지정된 알बम을 데이터베이스에 추가하고,
// 새로운 엔트리의 알बम ID를 반환합니다.
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
