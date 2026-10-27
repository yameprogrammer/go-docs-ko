# package time/tzdata

- 원문: <https://pkg.go.dev/time/tzdata>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package tzdata provides an embedded copy of the timezone database.

## 원문 요약

Package tzdata provides an embedded copy of the timezone database.

## API 상세 (go doc -all)

~~~text
package tzdata // import "time/tzdata"

Package tzdata provides an embedded copy of the timezone database. If this
package is imported anywhere in the program, then if the time package cannot
find tzdata files on the system, it will use this embedded information.

Importing this package will increase the size of a program by about 450 KB.

This package should normally be imported by a program's main package, not by a
library. Libraries normally shouldn't decide whether to include the timezone
database in a program.

This package will be automatically imported if you build with -tags timetzdata.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
