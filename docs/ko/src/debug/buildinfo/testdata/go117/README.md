go117.base64는 1.18 이전 버전의 buildinfo 인코딩에 대한 `debug/buildinfo`를 테스트하는 데 사용되는 base64 인코딩된 Go 1.17 hello world 바이너리입니다.

해당 바이너리는 Go 1.17이 본질적으로 안전하지 않다고 판단하는 보안 스캐너로부터 숨기기 위해 base64로 인코딩되었습니다.

다음 명령어로 `go117.base64`를 생성하십시오:

$ GOTOOLCHAIN=go1.17 GOOS=linux GOARCH=amd64 go build -trimpath
$ base64 go117 > go117.base64
$ rm go117

TODO(prattmic): 이상적으로는 모든 실행 파일 형식을 더 잘 지원하기 위해 이를 즉석에서 빌드하는 것이 좋겠지만, 그렇게 하려면 오래된 Go 툴체인을 다운로드하기 위한 네트워크 연결이 필요합니다.
