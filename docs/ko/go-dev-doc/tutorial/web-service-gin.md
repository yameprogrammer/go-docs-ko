<!--{
  "Title": "튜토리얼: Go와 Gin을 이용한 RESTful API 개발",
  "Breadcrumb": true
}-->

이 튜토리얼에서는 Go와 [Gin Web Framework](https://gin-gonic.com/en/docs/) (Gin)를 사용하여 RESTful 웹 서비스 API를 작성하는 기본 방법을 소개합니다.

Go와 그 툴링에 대해 기본적인 익숙함이 있다면 이 튜토리얼을 가장 효과적으로 활용하실 수 있습니다. Go를 처음 접하신다면, [Tutorial: Get started with Go](/doc/tutorial/getting-started)를 통해 빠르게 입문해 보세요.

Gin은 웹 서비스 구축을 포함하여 웹 애플리케이션 빌드와 관련된 많은 코딩 작업을 단순화합니다. 이 튜토리얼에서는 Gin을 사용하여 요청을 라우팅하고, 요청 세부 정보를 검색하며, 응답을 위한 JSON 마샬링을 수행하는 방법을 알아봅니다.

이 튜토리얼에서는 두 개의 엔드포인트를 가진 RESTful API 서버를 구축하게 됩니다. 예제 프로젝트는 빈티지 재즈 레코드 데이터 저장소입니다.

튜토리얼은 다음 섹션들로 구성되어 있습니다:

1. API 엔드포인트를 설계합니다.
2. 코드를 위한 폴더를 생성합니다.
3. 데이터를 생성합니다.
4. 모든 아이템을 반환하는 핸들러를 작성합니다.
5. 새로운 아이템을 추가하는 핸들러를 작성합니다.
6. 특정 아이템을 반환하는 핸들러를 작성합니다.

**참고:** 다른 튜토리얼은 [Tutorials](/doc/tutorial/index.html)를 참조하세요.

Google Cloud Shell에서 완료할 수 있는 대화형 튜토리얼로 시도하시려면, 아래 버튼을 클릭하세요.

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.png)](https://ide.cloud.google.com/?cloudshell_workspace=~&walkthrough_tutorial_url=https://raw.githubusercontent.com/golang/tour/master/tutorial/web-service-gin.md)

## 사전 요구 사항

*   **Go.** 이 튜토리얼을 따라하기 위해 최신 버전의 Go 사용을 권장합니다.
    설치 방법은 [Installing Go](/doc/install)를 참조하세요.
*   **코드 편집 도구.** 사용 중인 어떤 텍스트 편집기라도 괜찮습니다.
*   **명령어 터미널.** Go는 Linux 및 Mac의 모든 터미널, 그리고 Windows의 PowerShell 또는 cmd에서 잘 작동합니다.
*   **curl 도구.** Linux 및 Mac에는 이미 설치되어 있을 것입니다. Windows의 경우, Windows 10 Insider 빌드 17063 및 이후 버전에는 포함되어 있습니다. 이전 Windows 버전의 경우 별도로 설치해야 할 수도 있습니다. 자세한 내용은 [Tar and Curl Come to Windows](https://docs.microsoft.com/en-us/virtualization/community/team-blog/2017/20171219-tar-and-curl-come-to-windows)를 참조하세요.

## API 엔드포인트 설계 {#design_endpoints}

빈티지 바이닐 레코드를 판매하는 상점에 액세스할 수 있는 API를 구축하게 됩니다. 따라서 클라이언트가 사용자를 위해 앨범을 조회하고 추가할 수 있는 엔드포인트를 제공해야 합니다.

API를 개발할 때, 일반적으로 엔드포인트를 설계하는 것부터 시작합니다. 엔드포인트를 이해하기 쉽게 설계하면 API 사용자들이 더 효율적으로 사용할 수 있습니다.

이 튜토리얼에서 생성하게 될 엔드포인트들은 다음과 같습니다.

/albums
*   `GET` – 모든 앨범 목록을 JSON으로 반환하여 가져옵니다.
*   `POST` – JSON으로 전송된 요청 데이터를 통해 새 앨범을 추가합니다.

/albums/:id
*   `GET` – ID를 통해 앨범을 조회하며, 앨범 데이터를 JSON으로 반환합니다.

다음으로, 코드를 저장할 폴더를 생성하겠습니다.

## 코드 폴더 생성하기 {#create_folder}

먼저, 작성할 코드를 위한 프로젝트를 생성하세요.

1. 명령 프롬프트를 열고 홈 디렉토리로 이동하십시오.

Linux 또는 Mac에서:

```
    $ cd
    ```

Windows에서:

```
    C:\> cd %HOMEPATH%
    ```

2. 명령 프롬프트를 사용하여 코드를 저장할 `web-service-gin`이라는 디렉토리를 생성하세요.

```
    $ mkdir web-service-gin
    $ cd web-service-gin
    ```

3. 의존성을 관리할 수 있는 모듈을 생성하세요.

`go mod init` 명령어를 실행하고, 코드가 위치하게 될 모듈의 경로를 지정하십시오.

```
    $ go mod init example/web-service-gin
    go: creating new go.mod: module example/web-service-gin
    ```

이 명령은 추가하는 의존성들이 추적을 위해 나열되는 go.mod 파일을 생성합니다. 모듈 경로를 사용한 모듈 명명법에 대한 자세한 내용은 [Managing dependencies](/doc/modules/managing-dependencies#naming_module)를 참조하세요.

다음으로, 데이터를 처리하기 위한 데이터 구조를 설계하게 됩니다.

## 데이터 생성 {#create_data}

튜토리얼을 단순하게 유지하기 위해, 데이터는 메모리에 저장합니다. 실제 일반적인 API는 데이터베이스와 상호작용합니다.

데이터를 메모리에 저장하면 서버를 중지할 때마다 앨범 세트가 손실되며, 서버를 시작할 때 다시 생성된다는 점에 유의하세요.

#### 코드 작성하기

1. 텍스트 에디터를 사용하여 `web-service` 디렉토리에 `main.go`라는 파일을 생성하세요. 이 파일에 Go 코드를 작성하게 됩니다.
2. `main.go` 파일의 최상단에 다음 패키지 선언을 붙여넣으세요.

```
    package main
    ```

독립 실행형 프로그램(라이브러리와 반대되는 개념)은 항상 `main` 패키지에 포함됩니다.

3. 패키지 선언 아래에 다음과 같은 `album` struct 선언을 붙여넣으세요. 이를 사용하여 앨범 데이터를 메모리에 저장하게 됩니다.

``json:"artist"``와 같은 구조체 태그(Struct tags)는 구조체의 내용이 JSON으로 직렬화될 때 필드 이름이 어떻게 되어야 하는지를 지정합니다. 태그가 없으면 JSON은 구조체의 대문자로 시작하는 필드 이름을 그대로 사용하게 되는데, 이는 JSON에서 흔히 사용하는 스타일이 아닙니다.

```
    // album은 레코드 앨범에 관한 데이터를 나타냅니다.
    type album struct {
    	ID     string  `json:"id"`
    	Title  string  `json:"title"`
    	Artist string  `json:"artist"`
    	Price  float64 `json:"price"`
    }
    ```

4. 방금 추가한 struct 선언 아래에, 시작할 때 사용할 데이터가 포함된 다음 `album` struct 슬라이스를 붙여넣으세요.

```
    // 레코드 앨범 데이터를 시딩하기 위한 albums 슬라이스입니다.
    var albums = []album{
    	{ID: "1", Title: "Blue Train", Artist: "John Coltrane", Price: 56.99},
    	{ID: "2", Title: "Jeru", Artist: "Gerry Mulligan", Price: 17.99},
    	{ID: "3", Title: "Sarah Vaughan and Clifford Brown", Artist: "Sarah Vaughan", Price: 39.99},
    }
    ```

다음으로, 첫 번째 엔드포인트를 구현하기 위한 코드를 작성하겠습니다.

## 모든 항목을 반환하는 핸들러 작성하기 {#all_items}

클라이언트가 `GET /albums`로 요청을 보낼 때, 모든 앨범 정보를 JSON으로 반환하고자 합니다.

이를 위해 다음과 같이 작성합니다:

*   응답을 준비하는 로직
*   요청 경로를 로직에 매핑하는 코드

이는 런타임 시 실행되는 순서와는 반대라는 점에 유의하십시오. 하지만 먼저 의존성을 추가한 다음, 해당 의존성에 의존하는 코드를 추가하는 방식입니다.

#### 코드 작성하기

1. 이전 섹션에서 추가한 struct 코드 아래에 다음 코드를 붙여넣어 앨범 목록을 가져오십시오.

이 `getAlbums` 함수는 `album` 구조체 슬라이스로부터 JSON을 생성하여, 해당 JSON을 응답에 씁니다.

```
    // getAlbums는 모든 앨범 목록을 JSON으로 응답합니다.
    func getAlbums(c *gin.Context) {
    	c.IndentedJSON(http.StatusOK, albums)
    }
    ```

이 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   [`gin.Context`](https://pkg.go.dev/github.com/gin-gonic/gin#Context) 파라미터를 받는 `getAlbums` 함수를 작성하세요. 이 함수의 이름은 자유롭게 정할 수 있습니다. Gin과 Go 모두 특정한 함수 이름 형식을 요구하지 않습니다.

`gin.Context`는 Gin에서 가장 중요한 부분입니다. 요청 세부 정보를 전달하고, JSON을 검증 및 직렬화하며, 그 외 다양한 기능을 수행합니다. (이름은 비슷하지만, Go의 내장 [`context`](/pkg/context/) 패키지와는 다릅니다.)

*   [`Context.IndentedJSON`](https://pkg.go.dev/github.com/gin-gonic/gin#Context.IndentedJSON)을 호출하여
        struct를 JSON으로 직렬화하고 응답에 추가합니다.

함수의 첫 번째 인자는 클라이언트로 보내고자 하는 HTTP 상태 코드입니다. 여기서는 `200 OK`를 나타내기 위해 `net/http` 패키지의 [`StatusOK`](https://pkg.go.dev/net/http#StatusOK) 상수를 전달하고 있습니다.

더 간결한 JSON을 전송하려면 `Context.IndentedJSON`을 [`Context.JSON`](https://pkg.go.dev/github.com/gin-gonic/gin#Context.JSON) 호출로 대체할 수 있습니다. 실제로 디버깅 시에는 들여쓰기 형태가 훨씬 다루기 쉬우며, 크기 차이는 보통 미미합니다.

2. `main.go` 파일 상단, `albums` 슬라이스 선언 바로 아래에 다음 코드를 붙여넣어 핸들러 함수를 엔드포인트 경로에 할당하세요.

이 설정은 `getAlbums`가 `/albums` 엔드포인트 경로로 들어오는 요청을 처리하는 연관 관계를 설정합니다.

```go
    func main() {
    	router := gin.Default()
    	router.GET("/albums", getAlbums)
```

```go
router.Run("localhost:8080")
    }
    ```

이 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   [`Default`](https://pkg.go.dev/github.com/gin-gonic/gin#Default)를 사용하여 Gin 라우터를 초기화합니다.
    *   [`GET`](https://pkg.go.dev/github.com/gin-gonic/gin#RouterGroup.GET) 함수를 사용하여 `GET` HTTP 메서드와 `/albums` 경로를 핸들러 함수에 연결합니다.

`getAlbums` 함수의 _이름_을 전달하고 있다는 점에 유의하세요. 이는 `getAlbums()`(괄호에 주의)를 통해 함수의 _결과_를 전달하는 것과는 다릅니다.

*   [`Run`](https://pkg.go.dev/github.com/gin-gonic/gin#Engine.Run) 함수를 사용하여 라우터를 `http.Server`에 연결하고 서버를 시작하십시오.

3. `main.go` 파일의 상단, package 선언 바로 아래에 방금 작성한 코드를 지원하는 데 필요한 패키지들을 import 하세요.

코드의 첫 부분은 다음과 같아야 합니다:

```markdown
    package main
```

제공해주신 내용이 코드 조각(`import` 문)뿐이라 번역할 텍스트가 없지만, 요청하신 기술 번역 가이드라인에 따라 해당 부분을 유지하여 전달해 드립니다.

```go
import (
    	"net/http"
```

"github.com/gin-gonic/gin"
    )
    ```

4. main.go를 저장하세요.

#### 코드 실행하기

1. Gin 모듈을 종속성으로 추적하기 시작합니다.

커맨드 라인에서 [`go get`](/cmd/go/#hdr-Add_dependencies_to_current_module_and_install_them)을 사용하여 github.com/gin-gonic/gin 모듈을 현재 모듈의 의존성으로 추가하세요.
점(`.`) 인수를 사용하여 "현재 디렉터리에 있는 코드의 의존성을 가져오기"를 의미하도록 하세요.

```
    $ go get .
    go get: added github.com/gin-gonic/gin v1.7.2
    ```

Go는 이전 단계에서 추가한 `import` 선언을 충족하기 위해 이 의존성을 해결하고 다운로드했습니다.

2. `main.go` 파일이 포함된 디렉토리의 명령줄에서 코드를 실행하세요.
    "현재 디렉토리의 코드를 실행하라"는 의미로 점(`.`) 인자를 사용하세요.

```
    $ go run .
    ```

코드가 실행되면, 요청을 보낼 수 있는 HTTP 서버가 구동됩니다.

3. 새로운 명령줄 창에서 `curl`을 사용하여 실행 중인 웹 서비스에 요청을 보내십시오.

```
    $ curl http://localhost:8080/albums
    ```

해당 명령어는 서비스에 시딩(seed)한 데이터를 표시해야 합니다.

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

API를 시작하셨습니다! 다음 섹션에서는 아이템을 추가하기 위한 `POST` 요청을 처리하는 코드가 포함된 또 다른 엔드포인트를 생성하게 됩니다.

## 새로운 항목을 추가하는 핸들러 작성하기 {#add_item}

클라이언트가 `/albums` 경로로 `POST` 요청을 보낼 때, 요청 본문에 기술된 앨범을 기존 앨범 데이터에 추가하고자 합니다.

이를 위해 다음과 같이 작성합니다:

*   새 앨범을 기존 리스트에 추가하는 로직.
*   `POST` 요청을 해당 로직으로 라우팅하는 간단한 코드.

#### 코드 작성하기

1. 앨범 목록에 앨범 데이터를 추가하는 코드를 추가합니다.

`import` 문 이후 적절한 위치에 다음 코드를 붙여넣으세요. (파일의 끝부분이 적당하지만, Go는 함수 선언 순서를 강제하지 않습니다.)

```go
    // postAlbums는 요청 본문에서 받은 JSON으로부터 앨범을 추가합니다.
    func postAlbums(c *gin.Context) {
    	var newAlbum album
```

// BindJSON을 호출하여 수신된 JSON을
    	// newAlbum에 바인딩합니다.
    	if err := c.BindJSON(&newAlbum); err != nil {
    		return
    	}

// 새 앨범을 슬라이스에 추가합니다.
    	albums = append(albums, newAlbum)
    	c.IndentedJSON(http.StatusCreated, newAlbum)
    }
    ```

이 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   [`Context.BindJSON`](https://pkg.go.dev/github.com/gin-gonic/gin#Context.BindJSON)을 사용하여 요청 본문을 `newAlbum`에 바인딩하세요.
    *   JSON에서 초기화된 `album` 구조체를 `albums` 슬라이스에 추가하세요.
    *   응답에 `201` 상태 코드와 함께 추가한 앨범을 나타내는 JSON을 추가하세요.

2. `main` 함수를 다음과 같이 `router.POST` 함수를 포함하도록 변경하세요.

```go
    func main() {
    	router := gin.Default()
    	router.GET("/albums", getAlbums)
    	router.POST("/albums", postAlbums)
```

router.Run("localhost:8080")
    }
    ```

이 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   `/albums` 경로의 `POST` 메서드를 `postAlbums` 함수와 연결합니다.

Gin을 사용하면 핸들러를 HTTP 메서드와 경로의 조합에 연결할 수 있습니다. 이러한 방식으로, 클라이언트가 사용하는 메서드에 따라 단일 경로로 전송된 요청을 별도로 라우팅할 수 있습니다.

#### 코드 실행하기

1. 이전 섹션에서 서버가 여전히 실행 중이라면, 서버를 중지하세요.
2. `main.go` 파일이 포함된 디렉토리의 명령줄에서 코드를 실행하세요.

```
    $ go run .
    ```

3. 다른 명령줄 창에서 `curl`을 사용하여 실행 중인 웹 서비스에 요청을 보내십시오.

```
    $ curl http://localhost:8080/albums \
        --include \
        --header "Content-Type: application/json" \
        --request "POST" \
        --data '{"id": "4","title": "The Modern Sound of Betty Carter","artist": "Betty Carter","price": 49.99}'
    ```

명령어는 추가된 앨범의 헤더와 JSON을 표시해야 합니다.

```
    HTTP/1.1 201 Created
    Content-Type: application/json; charset=utf-8
    Date: Wed, 02 Jun 2021 00:34:12 GMT
    Content-Length: 116
```

```json
{
        "id": "4",
        "title": "The Modern Sound of Betty Carter",
        "artist": "Betty Carter",
        "price": 49.99
    }
    ```

4. 이전 섹션에서와 같이 `curl`을 사용하여 앨범 전체 목록을 조회하고, 새 앨범이 추가되었는지 확인하십시오.

```
    $ curl http://localhost:8080/albums \
        --header "Content-Type: application/json" \
        --request "GET"
    ```

해당 명령어는 앨범 목록을 표시해야 합니다.

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

## 특정 항목을 반환하는 핸들러 작성하기 {#specific_item}

클라이언트가 `GET /albums/[id]` 요청을 보낼 때, `id` 경로 파라미터와 일치하는 ID를 가진 앨범을 반환하고자 합니다.

이를 위해 다음 단계를 수행합니다:

*   요청된 앨범을 가져오는 로직을 추가합니다.
*   경로를 해당 로직에 매핑합니다.

#### 코드 작성하기

1. 이전 섹션에서 추가한 `postAlbums` 함수 아래에, 특정 앨범을 조회하기 위한 다음 코드를 붙여넣으세요.

이 `getAlbumByID` 함수는 요청 경로(request path)에서 ID를 추출한 다음, 그에 맞는 앨범을 찾습니다.

```go
    // getAlbumByID는 클라이언트가 보낸 id 파라미터와 ID 값이 일치하는 앨범을 찾아
    // 해당 앨범을 응답으로 반환합니다.
    func getAlbumByID(c *gin.Context) {
    	id := c.Param("id")
```

```go
    	// 앨범 리스트를 반복하며 ID 값이 매개변수와 일치하는 앨범을 찾습니다.
    	for _, a := range albums {
    		if a.ID == id {
    			c.IndentedJSON(http.StatusOK, a)
    			return
    		}
    	}
    	c.IndentedJSON(http.StatusNotFound, gin.H{"message": "album not found"})
    }
    ```

이 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   URL에서 `id` 경로 파라미터를 가져오려면 [`Context.Param`](https://pkg.go.dev/github.com/gin-gonic/gin#Context.Param)을 사용하세요. 이 핸들러를 경로에 매핑할 때, 경로에 파라미터를 위한 플레이스홀더를 포함하게 됩니다.
    *   슬라이스 내의 `album` 구조체들을 루프 돌며, `ID` 필드 값이 `id` 파라미터 값과 일치하는 항목을 찾으세요. 일치하는 항목을 찾으면, 해당 `album` 구조체를 JSON으로 직렬화하여 `200 OK` HTTP 코드와 함께 응답으로 반환합니다.

앞서 언급했듯이, 실제 서비스에서는 이러한 조회를 수행하기 위해 데이터베이스 쿼리를 사용할 가능성이 높습니다.

*   앨범을 찾을 수 없는 경우 [`http.StatusNotFound`](https://pkg.go.dev/net/http#StatusNotFound)와 함께 HTTP `404` 에러를 반환합니다.

2. 마지막으로, 다음 예제와 같이 경로가 `/albums/:id`인 `router.GET` 호출을 새로 추가하여 `main` 함수를 수정하세요.

```go
    func main() {
    	router := gin.Default()
    	router.GET("/albums", getAlbums)
    	router.GET("/albums/:id", getAlbumByID)
    	router.POST("/albums", postAlbums)
```

router.Run("localhost:8080")
    }
    ```

이 코드에서 당신은 다음과 같은 작업을 수행합니다:

*   `/albums/:id` 경로를 `getAlbumByID` 함수와 연결합니다.
        Gin에서 경로 항목 앞에 붙는 콜론(`:`)은 해당 항목이 경로 매개변수(path parameter)임을 의미합니다.

#### 코드 실행하기

1. 이전 섹션에서 서버가 여전히 실행 중이라면, 서버를 중지하세요.
2. `main.go` 파일이 포함된 디렉토리의 명령줄에서 코드를 실행하여 서버를 시작하세요.

```
    $ go run .
    ```

3. 다른 명령줄 창에서 `curl`을 사용하여 실행 중인 웹 서비스에 요청을 보내십시오.

```
    $ curl http://localhost:8080/albums/2
    ```

해당 명령어는 사용자가 입력한 ID에 해당하는 앨범의 JSON을 표시해야 합니다. 만약 앨범을 찾지 못한 경우, 에러 메시지가 포함된 JSON을 받게 됩니다.

```
    {
            "id": "2",
            "title": "Jeru",
            "artist": "Gerry Mulligan",
            "price": 17.99
    }
    ```

## 결론 {#conclusion}

축하합니다! 방금 Go와 Gin을 사용하여 간단한 RESTful 웹 서비스를 작성하셨습니다.

추천 다음 주제:

*   Go가 처음이시라면 [Effective Go](/doc/effective_go)와 [How to write Go code](/doc/code)에서 유용한 모범 사례를 확인하실 수 있습니다.
*   [Go Tour](/tour/)는 Go의 기초를 단계별로 배울 수 있는 훌륭한 입문 가이드입니다.
*   Gin에 대한 더 자세한 내용은 [Gin Web Framework 패키지 문서](https://pkg.go.dev/github.com/gin-gonic/gin) 또는 [Gin Web Framework 문서](https://gin-gonic.com/en/docs/)를 참조하세요.

## 완성된 코드 {#completed_code}

이 섹션에는 이 튜토리얼을 통해 구축하는 애플리케이션의 코드가 포함되어 있습니다.

```go
package main

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

// albums 슬라이스는 초기 레코드 앨범 데이터를 심기(seed) 위해 사용됩니다.
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

// getAlbums는 모든 앨범의 목록을 JSON으로 응답합니다.
func getAlbums(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, albums)
}

// postAlbums는 요청 본문에서 받은 JSON을 통해 앨범을 추가합니다.
func postAlbums(c *gin.Context) {
	var newAlbum album

	// BindJSON을 호출하여 수신된 JSON을
	// newAlbum에 바인딩합니다.
	if err := c.BindJSON(&newAlbum); err != nil {
		return
	}

	// 새 앨범을 슬라이스에 추가합니다.
	albums = append(albums, newAlbum)
	c.IndentedJSON(http.StatusCreated, newAlbum)
}

// getAlbumByID는 클라이언트가 보낸 id 파라미터와 일치하는 ID 값을 가진
// 앨범을 찾아 해당 앨범을 응답으로 반환합니다.
func getAlbumByID(c *gin.Context) {
	id := c.Param("id")

	// 앨범 목록을 순회하며 ID 값이
	// 파라미터와 일치하는 앨범을 찾습니다.
	for _, a := range albums {
		if a.ID == id {
			c.IndentedJSON(http.StatusOK, a)
			return
		}
	}
	c.IndentedJSON(http.StatusNotFound, gin.H{"message": "album not found"})
}
```
