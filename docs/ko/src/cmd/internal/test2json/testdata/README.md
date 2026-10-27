# test2json 테스트 결과물(artifacts)

이 디렉토리는 [test2json_test.go](../test2json_test.go)의 `TestGolden`을 위한 테스트 결과물(artifacts)을 포함하고 있습니다. 각 `<test>.*` 파일 세트에 대하여:

- `<test>.src` 파일이 존재하는 경우, TestGolden은 이를 스크립트 테스트로 실행하고 출력이 `<test>.test`와 일치하는지 확인합니다. 이는 testing 패키지가 test2json에서 기대하는 출력을 생성하는지 검증합니다.
- TestGolden은 `<test>.test` 파일을 읽어 `Converter`로 처리하며, 그 결과가 `<test>.json`과 일치하는지 확인합니다. 이는 test2json이 기대하는 출력 이벤트를 생성하는지 검증합니다.
