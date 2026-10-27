# package internal/sysinfo

- 원문: <https://pkg.go.dev/internal/sysinfo>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package sysinfo implements high level hardware information gathering that can be used for debugging or information purposes.

## 원문 요약

Package sysinfo implements high level hardware information gathering that can be used for debugging or information purposes.

## API 상세 (go doc -all)

~~~text
package sysinfo // import "internal/sysinfo"

Package sysinfo implements high level hardware information gathering that can be
used for debugging or information purposes.

VARIABLES

var CPUName = sync.OnceValue(func() string {
	if name := cpu.Name(); name != "" {
		return name
	}

	if name := osCPUInfoName(); name != "" {
		return name
	}

	return ""
})
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
