notgo.base64는 Go가 아닌 바이너리에서 debug/buildinfo 오류를 테스트하는 데 사용되는 base64 인코딩된 C hello world 바이너리입니다.

보안 스캐너가 이를 감지하여 차단하는 것을 방지하기 위해 바이너리는 base64로 인코딩되어 있습니다.

linux-amd64 환경에서 다음 명령어로 `notgo.base64`를 생성하세요:

$ cc -o notgo main.c
$ base64 notgo > notgo.base64
$ rm notgo

현재 바이너리는 "gcc version 14.2.0 (Debian 14.2.0-3+build4)"로 빌드되었습니다.

TODO(prattmic): 이상적으로는 모든 실행 파일 형식을 더 잘 지원하기 위해 이를 즉석에서(on the fly) 빌드하는 것이 좋겠지만, 그렇게 하려면 각 플랫폼의 C 컴파일러를 호출하는 복잡한 세부 사항들을 인코딩해야 합니다.
