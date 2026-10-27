<!--{
  "Title": "모듈 게시하기"
}-->

다른 개발자들이 모듈을 사용할 수 있게 하려면, Go 도구들이 인식할 수 있도록 모듈을 publish 해야 합니다. 모듈을 publish 하고 나면, 해당 패키지를 가져오는 개발자들은 `go get`과 같은 명령어를 실행하여 모듈에 대한 의존성을 해결할 수 있게 됩니다.

> **참고:** 모듈을 게시한 후에는 태그가 지정된 버전을 변경하지 마세요. 해당 모듈을 사용하는 개발자의 경우, Go 도구는 다운로드한 모듈을 처음 다운로드한 복사본과 대조하여 인증합니다. 두 버전이 다를 경우, Go 도구는 보안 오류를 반환합니다. 이전에 게시한 버전의 코드를 변경하는 대신, 새 버전을 게시하세요.

**함께 보기**

* 모듈 개발에 대한 개요는 [Developing and publishing modules](developing)를 참조하세요.
* 게시 과정을 포함한 상위 수준의 모듈 개발 워크플로우는 [Module release and versioning workflow](release-workflow)를 참조하세요.

## 게시 단계

다음 단계에 따라 모듈을 게시하십시오.

1. 명령 프롬프트를 열고 로컬 저장소에 있는 모듈의 루트 디렉터리로 이동하십시오.

1.  `go mod tidy`를 실행하세요. 이 명령어는 모듈에 누적된 종속성 중 더 이상 필요하지 않은 항목을 제거합니다.

```
    $ go mod tidy
    ```

1. `go test ./...`를 마지막으로 한 번 더 실행하여 모든 것이 제대로 작동하는지 확인하십시오.

이 명령은 Go 테스트 프레임워크를 사용하여 작성한 단위 테스트를 실행합니다.

```
    $ go test ./...
    ok      example.com/mymodule       0.015s
    ```

1. `git tag` 명령어를 사용하여 프로젝트에 새로운 버전 번호 태그를 지정합니다.

버전 번호의 경우, 이번 릴리스의 변경 사항 성격을 사용자에게 알릴 수 있는 번호를 사용하십시오. 자세한 내용은 [Module version numbering](version-numbers)을 참조하십시오.

```
    $ git commit -m "mymodule: changes for v0.1.0"
    $ git tag v0.1.0
    ```

1. 새 태그를 origin 저장소로 push합니다.

```
    $ git push origin v0.1.0
    ```

1.  [`go list` 명령](/cmd/go/#hdr-List_packages_or_modules)을 실행하여 Go가 게시하려는 모듈에 대한 정보로 모듈 인덱스를 업데이트하도록 유도함으로써 모듈을 사용할 수 있게 만드십시오.

명령어 앞에 `GOPROXY` 환경 변수를 Go 프록시로 설정하는 문구를 추가하십시오. 이렇게 하면 요청이 프록시에 도달하게 됩니다.

```
    $ GOPROXY=proxy.golang.org go list -m example.com/mymodule@v0.1.0
    ```

작성하신 모듈에 관심이 있는 개발자들은 다른 모듈과 마찬가지로 해당 모듈에서 패키지를 import하고 [`go get` 명령어]()를 실행합니다. 최신 버전을 위해 [`go get` 명령어]()를 실행하거나, 다음 예제와 같이 특정 버전을 지정할 수 있습니다.

```
$ go get example.com/mymodule@v0.1.0
```
