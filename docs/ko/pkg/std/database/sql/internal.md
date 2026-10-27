# package database/sql/internal

- 원문: <https://pkg.go.dev/database/sql/internal>
- 분류: Go 표준 라이브러리

## 한국어 요약

`internal` 패키지는 `database/sql`과 `database/sql/driver` 간에 공유되는 내부 심볼들을 포함합니다.

## 원문 요약

Package internal contains internal symbols shared between database/sql and database/sql/driver.

## API 상세 (go doc -all)

~~~text
package internal // import "database/sql/internal"

Package internal contains internal symbols shared between database/sql and
database/sql/driver.

FUNCTIONS

func ScanContextValue(c ScanContext) any

TYPES

type ScanContext struct {
	// Has unexported fields.
}
    ScanContext is database/sql/driver.ScanContext. We define it here so
    driver.ScanContext can be opaque to users but visible to database/sql.

func NewScanContext(v any) ScanContext
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
