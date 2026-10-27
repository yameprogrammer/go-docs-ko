이 디렉터리는 코멘트 파서(comment parser)를 위한 테스트 파일(*.txt)들을 포함하고 있습니다.

파일들은 [txtar 형식](https://pkg.go.dev/golang.org/x/tools/txtar)으로 되어 있습니다.
다음 예시를 참고하십시오:

-- input --
	Hello.
	-- gofmt --
	Hello.
	-- html --
	<p>Hello.
	-- markdown --
	Hello.
	-- text --
	Hello.

각 `-- name --` 라인은 주어진 이름의 새로운 파일을 도입합니다.
“input”이라는 이름의 파일이 가장 먼저 와야 하며, [comment.Parser](https://pkg.go.dev/go/doc/comment/#Parser)의 입력을 포함합니다.

나머지 파일들은 [comment.Printer](https://pkg.go.dev/go/doc/comment/#Printer)에 의해 생성된 지정된 형식의 예상 출력값을 포함하고 있습니다:
Printer.Comment의 경우 “gofmt”(gofmt에서 사용하는 Go 주석 형식),
Printer.HTML의 경우 “html”, Printer.Markdown의 경우 “markdown”, 그리고 Printer.Text의 경우 “text”입니다.
또한 raw 데이터 구조의 텍스트 덤프를 위한 “dump” 형식도 사용할 수 있습니다.

`-- input --` 라인 이전의 텍스트가 존재하는 경우, 이는 `comment.Printer`를 초기화하기 위해 언마샬링(unmarshal)될 JSON입니다. 예를 들어, 이 테스트 케이스는 `Printer`의 `TextWidth` 필드를 20으로 설정합니다:

{"TextWidth": 20}
	-- input --
	Package gob은 Encoder(송신자)와 Decoder(수신자) 간에 교환되는 바이너리 값인 gob의 스트림을 관리합니다.
	-- text --
	Package gob은
	gob - Encoder(송신자)와
	Decoder(수신자) 간에
	교환되는 바이너리
	값의 스트림을
	관리합니다.
