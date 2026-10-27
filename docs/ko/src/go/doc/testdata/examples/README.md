이 파일들은 `example_test.go:TestExamples`에 의해 처리됩니다.

`.golden` 파일은 해당 `.go` 파일의 `doc.Examples`에 의해 생성되어야 하는 각 예제에 대해 두 개의 섹션을 가진 `txtar` 파일입니다.

`EXAMPLE_NAME.Output`라는 이름의 한 섹션은 예제의 출력을 포함하며, 이는 `Example.Output` 필드의 값입니다.

다른 하나인 `EXAMPLE_NAME.Play`에는 예제의 실행 가능한 버전으로 포맷팅된 코드, 즉 `Example.Play` 필드의 값이 포함되어 있습니다.

섹션이 누락된 경우, 해당 섹션은 비어 있는 것으로 처리됩니다.
