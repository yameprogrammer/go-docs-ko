# package crypto/internal/fips140deps

- 원문: <https://pkg.go.dev/crypto/internal/fips140deps>
- 분류: Go 표준 라이브러리

## 한국어 요약

`fipsdeps` 패키지는 FIPS 모듈에 노출되는 내부 API를 위한 래퍼(wrapper) 패키지들을 포함하고 있습니다.

## 원문 요약

Package fipsdeps contains wrapper packages for internal APIs that are exposed to the FIPS module.

## API 상세 (go doc -all)

~~~text
package fipsdeps // import "crypto/internal/fips140deps"

Package fipsdeps contains wrapper packages for internal APIs that are exposed
to the FIPS module. Since modules are frozen upon validation and supported for
a number of future versions, APIs exposed by crypto/internal/fips140deps/...
must not be changed until the modules that use them are no longer supported.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
