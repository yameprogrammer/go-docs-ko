<!--{
  "제목": "튜토리얼: Go 및 Gin을 사용하여 RESTful API 개발",
  "브레드크럼": true
}-->

이 튜토리얼에서는 Go를 사용하여 RESTful 웹 서비스 API를 작성하는 기본 사항과 [Gin Web Framework](https://gin-gonic.com/en/docs/) (Gin)을 소개합니다.

이 튜토리얼을 최대한 활용하려면 Go 및 관련 도구에 대한 기본적인 이해가 필요합니다. Go에 처음 접하신다면, [튜토리얼: Go 시작하기](/doc/tutorial/getting-started)를 참조하여 빠르게 소개를 받아보세요.

Gin은 웹 애플리케이션을 구축하는 데 필요한 많은 코딩 작업을 단순화합니다. 여기에는 웹 서비스 구축도 포함됩니다. 이 튜토리얼에서는 Gin을 사용하여 요청을 라우팅하고, 요청 세부 정보를 가져오고, 응답에 대한 JSON을 직렬화하는 방법을 배웁니다.

이 튜토리얼에서는 두 개의 엔드포인트를 갖는 RESTful API 서버를 구축하는 방법을 배울 것입니다. 예제 프로젝트는 빈티지 재즈 레코드에 대한 데이터 저장소입니다.

이 튜토리얼에는 다음 섹션이 포함되어 있습니다:

1. API 엔드포인트 설계
2. 코드용 폴더 생성
3. 데이터 생성
4. 모든 항목을 반환하는 핸들러 작성
5. 새로운 항목을 추가하는 핸들러 작성
6. 특정 항목을 반환하는 핸들러 작성

**참고:** 다른 튜토리얼은 [튜토리얼](/doc/tutorial/index.html)에서 확인하세요.

이 튜토리얼을 Google Cloud Shell에서 직접 체험해 보려면,
아래 버튼을 클릭하세요.

[![Cloud Shell로 열기](https://gstatic.com/cloudssh/images/open-btn.png)](https://ide.cloud.google.com/?cloudshell_workspace=~&walkthrough_tutorial_url=https://raw.githubusercontent.com/golang/tour/master/tutorial/web-service-gin.md)

## 필수 조건

*   **Go.** 이 튜토리얼을 따라하려면 Go의 최신 버전을 사용하는 것을 권장합니다.
    설치 지침은 [Installing Go](/doc/install)를 참조하세요.
*   **코드 편집 도구.** 사용 중인 모든 텍스트 편집기가 잘 작동합니다.
*   **명령줄 터미널.** Go는 Linux 및 Mac에서 어떤 터미널에서도 잘 작동하며, Windows의 PowerShell 또는 cmd에서도 작동합니다.
*   **curl 도구.** Linux 및 Mac에서는 이미 설치되어 있을 것입니다. Windows에서는 Windows 10 Insider build 17063 이상에서 사용 가능합니다. 이전 버전의 Windows에서는 설치해야 할 수 있습니다. 자세한 내용은 [Tar and Curl Come to Windows](https://docs.microsoft.com/en-us/virtualization/community/team-blog/2017/20171219-tar-and-curl-come-to-windows)를 참조하세요.

## 디자인 API 엔드포인트 {#design_endpoints}

다음과 같은 API를 구축해야 합니다. 이 API는 빈티지 레코드(바이닐)를 판매하는 상점에 대한 액세스를 제공합니다. 따라서 클라이언트는 이를 통해 앨범을 가져오고 추가할 수 있는 엔드포인트를 제공해야 합니다.

API를 개발할 때, 일반적으로 엔드포인트를 먼저 설계합니다. API의 사용자가 엔드포인트를 더 쉽게 이해할 수 있도록 설계하는 것이 중요합니다.

다음은 이 튜토리얼에서 생성할 엔드포인트 목록입니다.

/albums
*   `GET` – 모든 앨범 목록을 JSON 형식으로 반환합니다.
*   `POST` – JSON 형식으로 전송된 요청 데이터에서 새 앨범을 추가합니다.

/albums/:id
*   `GET` – ID를 사용하여 앨범을 가져오고, 앨범 데이터를 JSON 형식으로 반환합니다.

다음으로, 코드를 위한 폴더를 만듭니다.

## 코드를 위한 폴더 생성 {#create_folder}

```
mkdir my_code
```

먼저, 코드를 작성할 프로젝트를 만듭니다.

1. 명령 프롬프트를 열고 홈 디렉토리로 이동합니다.

리눅스 또는 맥에서:

```
    $ cd
```

온 Windows:

```
    C:\> cd %HOMEPATH%
```

2. 명령 프롬프트를 사용하여 코드용 디렉토리를 만들고 이름을 `web-service-gin`으로 지정합니다.

```
    $ mkdir web-service-gin
    $ cd web-service-gin
    ```

3. 의존성을 관리할 수 있는 모듈을 만드세요.

`go mod init` 명령을 실행하고, 코드가 위치할 모듈의 경로를 지정합니다.

```
    $ go mod init example/web-service-gin
    go: 생성 중: 새 go.mod 파일: module example/web-service-gin
    ```

이 명령어는 `go.mod` 파일을 생성하며, 여기에 추가하는 의존성은 추적을 위해 나열됩니다. 모듈 경로를 사용하여 모듈을 명명하는 방법에 대한 자세한 내용은 [의존성 관리](/doc/modules/managing-dependencies#naming_module)를 참조하십시오.

다음으로, 데이터를 처리하기 위한 데이터 구조를 설계합니다.

## 데이터 생성 {#create_data}

튜토리얼을 간단하게 유지하기 위해, 데이터를 메모리에 저장합니다. 보다 일반적인 API는 데이터베이스와 상호 작용합니다.

참고: 메모리에 데이터를 저장하는 것은 서버를 중지할 때마다 앨범 세트가 손실되고 다시 시작할 때마다 다시 생성된다는 의미입니다.

```markdown
#### 코드를 작성하세요

1. 텍스트 편집기를 사용하여 `web-service` 디렉터리에 `main.go`라는 파일을 만듭니다. 이 파일에 Go 코드를 작성합니다.
2. `main.go` 파일의 맨 위에 다음 패키지 선언을 붙여넣습니다.

```
    패키지 main
```

독립 실행형 프로그램 (라이브러리가 아닌 경우)은 항상 `main` 패키지에 있습니다.

3. 패키지 선언 아래에 다음 `album` 구조체 선언을 붙여넣으세요. 이를 사용하여 메모리에 앨범 데이터를 저장할 수 있습니다.

구조체 태그 (예: ``json:"artist"``)는 구조체의 내용을 JSON으로 직렬화할 때 특정 필드의 이름을 지정합니다. 이러한 태그가 없으면 JSON은 구조체의 대문자로 된 필드 이름을 사용합니다 – JSON에서 흔하지 않은 스타일입니다.

```
    // album은 레코드 앨범에 대한 데이터를 나타냅니다.
    type album struct {
    	ID     string  `json:"id"`
    	Title  string  `json:"title"`
    	Artist string  `json:"artist"`
    	Price  float64 `json:"price"`
    }
```

4. 위에서 정의한 구조체 아래에, 사용할 데이터를 포함하는 다음과 같은 `album` 구조체의 슬라이스를 붙여넣으세요.

```
    // albums 슬라이스를 사용하여 레코드 앨범 데이터를 초기화합니다.
    var albums = []album{
    	{ID: "1", Title: "Blue Train", Artist: "John Coltrane", Price: 56.99},
    	{ID: "2", Title: "Jeru", Artist: "Gerry Mulligan", Price: 17.99},
    	{ID: "3", Title: "Sarah Vaughan and Clifford Brown", Artist: "Sarah Vaughan", Price: 39.99},
    }
```

다음으로, 여러분은 첫 번째 엔드포인트를 구현하기 위한 코드를 작성합니다.

## 모든 항목을 반환하는 핸들러 작성 {#all_items}

클라이언트가 `GET /albums` 요청을 할 때, 모든 앨범을 JSON 형식으로 반환하도록 합니다.

이를 수행하려면 다음을 작성하십시오:

*   응답을 준비하는 로직
*   요청 경로를 해당 로직에 매핑하는 코드

참고: 이는 실행 시간에 반대되는 방식이지만, 먼저 의존성을 추가하고, 그 다음 의존성을 사용하는 코드를 추가합니다.

```markdown
#### 코드를 작성하세요

1. 이전 섹션에서 추가한 구조 코드 아래에 다음 코드를 붙여넣어 앨범 목록을 가져옵니다.

이 `getAlbums` 함수는 `album` 구조체의 슬라이스를 JSON으로 변환하여, 이 JSON을 응답에 작성합니다.

```
    // getAlbums는 모든 앨범 목록을 JSON 형식으로 응답합니다.
    func getAlbums(c *gin.Context) {
    	c.IndentedJSON(http.StatusOK, albums)
    }
```

이 코드에서, 다음을 수행합니다:

*   `getAlbums` 함수를 작성하여 다음을 받습니다.
    [`gin.Context`](https://pkg.go.dev/github.com/gin-gonic/gin#Context) 매개변수.  참고: 이 함수에 다른 이름을 사용할 수 있었습니다. Gin 또는 Go는 특정 함수 이름 형식에 대해 요구하지 않습니다.

`gin.Context`는 Gin에서 가장 중요한 부분입니다. 요청 세부 정보를 담고, JSON을 검증하고 직렬화하며, 기타 기능을 수행합니다. (비록 이름이 유사하지만, 이는 Go의 내장 [`context`](/pkg/context/) 패키지와 다릅니다.)

*   `Context.IndentedJSON`를 호출하여 구조체를 JSON으로 직렬화하고 응답에 추가합니다. (참조: [https://pkg.go.dev/github.com/gin-gonic/gin#Context.IndentedJSON](https://pkg.go.dev/github.com/gin-gonic/gin#Context.IndentedJSON))

이 함수의 첫 번째 인수는 클라이언트로 보낼 HTTP 상태 코드를 지정합니다. 여기서는 `net/http` 패키지에서 `StatusOK` 상수를 전달하여 "200 OK"를 나타냅니다.

참고: `Context.IndentedJSON`를 `Context.JSON` 함수 호출로 대체할 수 있습니다.
        [`Context.JSON`](https://pkg.go.dev/github.com/gin-gonic/gin#Context.JSON)
        를 사용하여 더 간결한 JSON을 전송할 수 있습니다. 실제로는 디버깅할 때 들여쓰기 형식이 훨씬 편리하며, 크기 차이는 일반적으로 작습니다.

2. main.go의 맨 위에, `albums` 슬라이스 선언 바로 아래에 다음 코드를 붙여넣어 핸들러 함수를 엔드포인트 경로에 할당합니다.

이것은 `getAlbums`가 `/albums` 엔드포인트 경로에 대한 요청을 처리하는 연관을 설정합니다.

```
    func main() {
    	router := gin.Default()
    	router.GET("/albums", getAlbums)
    }
```

```
router.Run("localhost:8080")
}
```

이 코드에서, 다음을 수행합니다:

*   `Default`를 사용하여 Gin 라우터를 초기화합니다.
    *   `GET` HTTP 메서드와 `/albums` 경로를 핸들러 함수와 연결하기 위해 [`GET`](https://pkg.go.dev/github.com/gin-gonic/gin#RouterGroup.GET) 함수를 사용합니다.

참고: 여기서는 `getAlbums` 함수의 _이름_만 전달하고 있습니다. 이는
        함수의 _결과_를 전달하는 것과 다릅니다. 이는 `getAlbums()` (괄호 포함)를 전달하는 방식으로 수행됩니다.

*   `Run` 함수를 사용하여 라우터를 `http.Server`에 연결하고 서버를 시작합니다. (참조: https://pkg.go.dev/github.com/gin-gonic/gin#Engine.Run)

3. `main.go` 파일의 상단, 패키지 선언 바로 아래에, 새로 작성한 코드를 지원하는 데 필요한 패키지를 가져옵니다.

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, world!")
}
```

```
    package main
```

```
import (
    	"net/http"
)
```

"github.com/gin-gonic/gin"
)
```

4. main.go 저장.

#### 코드를 실행

1. Gin 모듈을 의존성으로 추적을 시작합니다.

명령줄에서, [`go get`](/cmd/go/#hdr-Add_dependencies_to_current_module_and_install_them)를 사용하여 `github.com/gin-gonic/gin` 모듈을 현재 모듈의 종속성으로 추가합니다.
    점(.) 인수를 사용하여 "현재 디렉토리에 있는 코드의 종속성을 가져옵니다"라는 의미를 갖습니다.

```
    go get .
    go get: github.com/gin-gonic/gin 버전 1.7.2 추가됨
    ```

Go에서 이 종속성을 해결하고 다운로드하여 이전 단계에서 추가한 `import` 선언을 충족했습니다.

2. 명령줄에서 `main.go` 파일이 있는 디렉토리에서 코드를 실행합니다.
    "."을 인수로 사용하여 "현재 디렉토리에서 코드를 실행"한다는 의미를 나타냅니다.

```
    go run .
```

코드가 실행되면, 요청을 보낼 수 있는 실행 중인 HTTP 서버가 있습니다.

3. 새로운 명령줄 창에서 `curl`을 사용하여 실행 중인 웹 서비스에 대한 요청을 만듭니다.

```
    $ curl http://localhost:8080/albums
    ```

이 명령은 서비스에 삽입한 데이터를 표시해야 합니다.

```
    [
            {
                    "id": "1",
                    "title": "Blue Train",
                    "artist": "John Coltrane",
                    "price": 56.99
            },
            {
                    "id": "2",
                    "title": "Jeru",
                    "artist": "Gerry Mulligan",
                    "price": 17.99
            },
            {
                    "id": "3",
                    "title": "Sarah Vaughan and Clifford Brown",
                    "artist": "Sarah Vaughan",
                    "price": 39.99
            }
    ]
    ```

API를 시작하셨습니다! 다음 섹션에서는 `POST` 요청을 처리하는 코드를 사용하여 새 엔드포인트를 만듭니다.

## 새 항목을 추가하는 핸들러 작성 {#add_item}

클라이언트가 `/albums`에 `POST` 요청을 할 때, 요청 본문에 설명된 앨범을 기존 앨범 데이터에 추가하고 싶습니다.

이를 수행하려면 다음을 작성하십시오:

*   기존 목록에 새 앨범을 추가하는 로직
*   `POST` 요청을 해당 로직으로 라우팅하는 데 필요한 코드

```markdown
#### 코드를 작성하세요

1. 앨범 데이터를 앨범 목록에 추가하는 코드를 추가합니다.

어떤 `import` 문 뒤에, 다음 코드를 붙여넣으십시오. (파일의 끝이 좋은 장소이지만, Go는 함수를 선언하는 순서를 강제하지 않습니다.)

```
    // postAlbums는 요청 본문에 수신된 JSON을 사용하여 새 앨범을 추가합니다.
    func postAlbums(c *gin.Context) {
    	var newAlbum album
```

// `BindJSON` 함수를 사용하여 수신된 JSON을 `newAlbum`에 바인딩합니다.
    	// err := c.BindJSON(&newAlbum); err != nil {
    	// }

// 새 앨범을 슬라이스에 추가합니다.
    	albums = albums + [newAlbum]
    	c.IndentedJSON(http.StatusCreated, newAlbum)
    }
```

이 코드에서는 다음을 수행합니다:

*   `[`Context.BindJSON`](https://pkg.go.dev/github.com/gin-gonic/gin#Context.BindJSON)`을 사용하여 요청 본문을 `newAlbum`에 바인딩합니다.
    *   JSON에서 초기화된 `album` 구조체를 `albums` 슬라이스에 추가합니다.
    *   응답에 `201` 상태 코드를 포함하여, 추가된 앨범을 나타내는 JSON을 함께 전달합니다.

2. `main` 함수를 수정하여 `router.POST` 함수를 포함하도록 합니다. 아래와 같이:

```
    func main() {
    	router := gin.Default()
    	router.GET("/albums", getAlbums)
    	router.POST("/albums", postAlbums)
    }
```

```
router.Run("localhost:8080")
}
```

이 코드에서, 다음을 수행합니다:

*   `/albums` 경로에 있는 `POST` 메서드를 `postAlbums` 함수와 연결합니다.

Gin을 사용하면 핸들러를 HTTP 메서드와 경로의 조합과 연결할 수 있습니다. 이를 통해 클라이언트가 사용하는 메서드에 따라 단일 경로로 전송된 요청을 개별적으로 라우팅할 수 있습니다.

#### 코드를 실행하세요

1. 만약 서버가 이전 섹션에서 실행 중이라면, 종료합니다.
2. `main.go` 파일이 있는 디렉토리의 명령줄에서 코드를 실행합니다.

```
    $ go run .
```

3. 다른 명령줄 창에서 `curl`을 사용하여 실행 중인 웹 서비스에 요청을 보냅니다.

```
    $ curl http://localhost:8080/albums \
        --include \
        --header "Content-Type: application/json" \
        --request "POST" \
        --data '{"id": "4","title": "The Modern Sound of Betty Carter","artist": "Betty Carter","price": 49.99}'
```

이 명령은 추가된 앨범의 헤더와 JSON을 표시해야 합니다.

```
    HTTP/1.1 201 Created
    Content-Type: application/json; charset=utf-8
    Date: Wed, 02 Jun 2021 00:34:12 GMT
    Content-Length: 116
```

```json
{
        "id": "4",
        "title": "현대적인 비티 카터의 사운드",
        "artist": "비티 카터",
        "price": 49.99
    }
```

4. 이전 섹션과 마찬가지로, `curl`을 사용하여 전체 앨범 목록을 가져옵니다. 이를 사용하여 새 앨범이 추가되었는지 확인할 수 있습니다.

```
    $ curl http://localhost:8080/albums \
        --header "Content-Type: application/json" \
        --request "GET"
```

이 명령은 앨범 목록을 표시해야 합니다.

```
    [
            {
                    "id": "1",
                    "title": "Blue Train",
                    "artist": "John Coltrane",
                    "price": 56.99
            },
            {
                    "id": "2",
                    "title": "Jeru",
                    "artist": "Gerry Mulligan",
                    "price": 17.99
            },
            {
                    "id": "3",
                    "title": "Sarah Vaughan and Clifford Brown",
                    "artist": "Sarah Vaughan",
                    "price": 39.99
            },
            {
                    "id": "4",
                    "title": "The Modern Sound of Betty Carter",
                    "artist": "Betty Carter",
                    "price": 49.99
            }
    ]
```

다음 섹션에서는 특정 항목에 대한 `GET` 요청을 처리하는 코드를 추가합니다.

## 특정 항목을 반환하는 핸들러 작성 {#specific_item}

```go
// Example Go code
package main

import (
	"fmt"
	"net/http"
)

func myHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Hello, world!")
}

func main() {
	http.HandleFunc("/hello", myHandler)
	fmt.Println("Server listening on port 8080")
	http.ListenAndServe(":8080", nil)
}
```

클라이언트가 `GET /albums/[id]` 요청을 할 때, `id` 경로 매개변수와 일치하는 ID를 가진 앨범을 반환하도록 합니다.

이를 수행하려면, 다음 단계를 따르세요:

*   요청된 앨범을 가져오는 로직 추가
*   로직을 경로에 매핑

```markdown
#### 코드를 작성하세요

1. 이전 섹션에서 추가한 `postAlbums` 함수 아래에, 다음 코드를 붙여넣어 특정 앨범을 가져옵니다.

이 `getAlbumByID` 함수는 요청 경로에서 ID를 추출하고,
    매칭되는 앨범을 찾습니다.

```
    // getAlbumByID은 클라이언트에서 전송된 id 값과 일치하는 album을 찾은 다음, 해당 album을 응답으로 반환합니다.
    func getAlbumByID(c *gin.Context) {
    	id := c.Param("id")
    }
```

```
// 앨범 목록을 반복하면서,
    	// ID 값이 매개변수와 일치하는 앨범을 찾습니다.
    	for _, a := range albums {
    		if a.ID == id {
    			c.IndentedJSON(http.StatusOK, a)
    			return
    		}
    	}
    	c.IndentedJSON(http.StatusNotFound, gin.H{"message": "앨범을 찾을 수 없습니다"})
    }
```

이 코드에서, 다음을 수행합니다:

*   `Context.Param`를 사용하여 URL에서 `id` 경로 매개변수를 검색합니다. 이 핸들러를 경로에 매핑할 때, 경로에 매개변수를 위한 자리 표시자를 포함합니다.
    *   슬라이스에 있는 `album` 구조체에 대해 반복하고, `ID` 필드 값이 `id` 매개변수 값과 일치하는 구조체를 찾습니다. 일치하는 항목이 있으면, 해당 `album` 구조체를 JSON으로 직렬화하고 `200 OK` HTTP 코드를 사용하여 응답으로 반환합니다.

위에서 언급했듯이, 실제 서비스는 이 작업을 수행하기 위해 데이터베이스 쿼리를 사용할 가능성이 높습니다.

*   앨범이 존재하지 않으면 [`http.StatusNotFound`](https://pkg.go.dev/net/http#StatusNotFound) HTTP `404` 오류를 반환합니다.

2. 마지막으로, `main` 함수를 수정하여 `router.GET` 호출을 추가하고, 경로를 `/albums/:id`로 변경하도록 합니다. 다음 예제에서 확인할 수 있습니다.

```
    func main() {
    	router := gin.Default()
    	router.GET("/albums", getAlbums)
    	router.GET("/albums/:id", getAlbumByID)
    	router.POST("/albums", postAlbums)
    }
```

```
router.Run("localhost:8080")
    }
```

이 코드에서, 다음을 수행합니다:

*   `/albums/:id` 경로를 `getAlbumByID` 함수와 연결합니다.
        Gin에서, 경로 내의 콜론은 해당 항목이 경로 매개변수임을 나타냅니다.

#### 코드를 실행하기

1. 만약 서버가 이전 섹션에서 실행 중이라면, 중지합니다.
2. main.go 파일이 있는 디렉토리의 명령줄에서 서버를 시작하는 코드를 실행합니다.

```
    go run .
```

3. 다른 명령줄 창에서 `curl`을 사용하여 실행 중인 웹 서비스에 대한 요청을 보냅니다.

```
    $ curl http://localhost:8080/albums/2
```

이 명령어는 사용한 앨범의 JSON을 표시합니다.
    앨범이 없으면 오류 메시지와 함께 JSON이 반환됩니다.

```json
{
        "id": "2",
        "title": "Jeru",
        "artist": "Gerry Mulligan",
        "price": 17.99
}
```

## 결론 {#conclusion}

축하합니다! 이제 Go와 Gin을 사용하여 간단한 RESTful 웹 서비스를 작성했습니다.

제안된 다음 주제:

*   Go에 처음 오시는 경우, 유용한 실무 지침은 다음에서 찾을 수 있습니다.
    [Effective Go](https://pkg.go.dev/std) 및
    [How to write Go code](https://pkg.go.dev/std).
*   [Go Tour](https://go.dev/tour/)는 Go 기본 개념에 대한 훌륭한 단계별 소개입니다.
*   Gin에 대해 자세히 알아보려면 다음 문서를 참조하십시오.
    [Gin Web Framework package documentation](https://pkg.go.dev/github.com/gin-gonic/gin)
    또는 [Gin Web Framework docs](https://gin-gonic.com/en/docs/).

## 완성된 코드 {#completed_code}

이 섹션에는 이 튜토리얼을 사용하여 구축하는 애플리케이션에 대한 코드가 포함되어 있습니다.

```markdown
패키지 main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// album은 레코드 앨범에 대한 데이터를 나타냅니다.
type album struct {
	ID     string  `json:"id"`
	Title  string  `json:"title"`
	Artist string  `json:"artist"`
	Price  float64 `json:"price"`
}

// albums는 레코드 앨범 데이터를 초기화하는 슬라이스입니다.
var albums = []album{
	{ID: "1", Title: "Blue Train", Artist: "John Coltrane", Price: 56.99},
	{ID: "2", Title: "Jeru", Artist: "Gerry Mulligan", Price: 17.99},
	{ID: "3", Title: "Sarah Vaughan and Clifford Brown", Artist: "Sarah Vaughan", Price: 39.99},
}

func main() {
	router := gin.Default()
	router.GET("/albums", getAlbums)
	router.GET("/albums/:id", getAlbumByID)
	router.POST("/albums", postAlbums)

	router.Run("localhost:8080")
}

// getAlbums은 모든 앨범 목록을 JSON 형식으로 응답합니다.
func getAlbums(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, albums)
}

// postAlbums는 요청 본문에 수신된 JSON에서 앨범을 추가합니다.
func postAlbums(c *gin.Context) {
	var newAlbum album

	// BindJSON을 호출하여 수신된 JSON을
	// newAlbum에 바인딩합니다.
	if err := c.BindJSON(&newAlbum); err != nil {
		return
	}

	// 새로운 앨범을 슬라이스에 추가합니다.
	albums = append(albums, newAlbum)
	c.IndentedJSON(http.StatusCreated, newAlbum)
}

// getAlbumByID는 클라이언트로부터 전송된 id 매개변수에 해당하는 ID 값을 가진 앨범을 찾은 다음, 해당 앨범을 응답으로 반환합니다.
func getAlbumByID(c *gin.Context) {
	id := c.Param("id")

	// albums 목록을 반복하며, ID 값이 매개변수와 일치하는
	// 앨범을 찾습니다.
	for _, a := range albums {
		if a.ID == id {
			c.IndentedJSON(http.StatusOK, a)
			return
		}
	}
	c.IndentedJSON(http.StatusNotFound, gin.H{"message": "album not found"})
}
```
