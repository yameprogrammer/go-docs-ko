구글 내부에서는 FIPS 140 관련 작업의 일환으로, 다양한 암호화 프리미티브에 BoringCrypto([BoringSSL](https://boringssl.googlesource.com/boringssl/)의 핵심)를 사용하는 Go 포크(fork) 버전을 개발해 왔습니다.

일부 외부 Go 사용자분들도 이 코드에 관심이 있다는 소식을 접하였기에, `GOEXPERIMENT=boringcrypto` 설정 뒤에 이 코드를 메인 Go 저장소에 공개하였습니다.

Google 외부에서 `GOEXPERIMENT=boringcrypto`를 사용하는 것은 _지원되지 않습니다_.
이 모드는 [Go 1 호환성 규칙](https://go.dev/doc/go1compat)의 일부가 아니며, 언제든지 호환되지 않는 방식으로 변경되거나 다른 문제가 발생할 수 있습니다.

명확히 말씀드리자면, 당사는 이 코드가 FIPS 140 표준에 적합한지 여부에 대해 어떠한 진술이나 표현도 하지 않습니다. 관심 있는 사용자는 이 코드가 자신의 목적에 유용한지 직접 평가해야 합니다.

Please provide the Markdown content you would like me to translate. I am ready to translate your technical text from English to Korean while preserving all structures and code.

이 디렉토리는 BoringCrypto 구현의 핵심뿐만 아니라, 모듈 자체를 위한 빌드 스크립트인 `syso/*.syso`를 포함하고 있습니다.

syso/goboringcrypto_linux_amd64.syso는 다음으로 빌드되었습니다:

GOARCH=amd64 ./build.sh

syso/goboringcrypto_linux_arm64.syso는 다음으로 빌드되었습니다:

GOARCH=arm64 ./build.sh

둘 다 Docker를 사용하여 실행됩니다.

arm64 빌드를 x86 시스템에서 실행하려면 다음이 필요합니다.

`apt-get install qemu-user-static qemu-binfmt-support`

x86 커널이 QEMU를 통해 arm64 바이너리를 실행할 수 있도록 허용합니다.

amd64 빌드를 Apple Silicon macOS에서 실행하려면 Rosetta 2가 필요합니다.

빌드에 대한 자세한 내용은 `build.sh`를 참조하세요.
