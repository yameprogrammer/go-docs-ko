이 디렉터리는 코멘트 파서(comment parser)를 위한 테스트 파일(*.txt)들을 포함하고 있습니다.

파일은 [txtar 형식](https://pkg.go.dev/golang.org/x/tools/txtar)으로 되어 있습니다.
다음 예시를 살펴보십시오:

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
“input”이라는 이름의 파일이 가장 먼저 와야 하며, [comment.Parser](https://pkg.go.dev/go/doc/comment/#Parser)에 전달될 입력 내용을 포함합니다.

나머지 파일들은 [comment.Printer](https://pkg.go.dev/go/doc/comment/#Printer)에 의해 생성된 지정된 형식의 예상 출력값을 포함하고 있습니다:
Printer.Comment의 경우 “gofmt”(gofmt에서 사용하는 Go 주석 형식),
Printer.HTML의 경우 “html”, Printer.Markdown의 경우 “markdown”, 그리고 Printer.Text의 경우 “text”입니다.
또한 raw 데이터 구조의 텍스트 덤프를 위해 형식을 “dump”로 설정할 수도 있습니다.

`-- input --` 라인 앞에 텍스트가 있는 경우, 이는 `comment.Printer`를 초기화하기 위해 언마샬링(unmarshal)될 JSON입니다. 예를 들어, 이 테스트 케이스는 `Printer`의 `TextWidth` 필드를 20으로 설정합니다:

{"TextWidth": 20}
	-- input --
	Package gob manages streams of gobs - binary values exchanged between an
	Encoder (transmitter) and a Decoder (receiver).
	-- text --
	Package gob은
	Encoder(송신자)와
	Decoder(수신자)
	사이에서 교환되는
	이진 값인 gob의
	스트림을 관리합니다.
