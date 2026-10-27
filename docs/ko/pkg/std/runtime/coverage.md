# package runtime/coverage

- 원문: <https://pkg.go.dev/runtime/coverage>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 커버지는 런타임에 장시간 실행되거나 `os.Exit`를 통해 종료되지 않는 프로그램 (예: 서버 프로그램)의 커버리지 프로필 데이터를 작성하기 위한 API를 제공합니다.

## 원문 요약

Package coverage contains APIs for writing coverage profile data at runtime from long-running and/or server programs that do not terminate via os.Exit.

## API 상세 (go doc -all)

~~~text
package coverage // import "runtime/coverage"

Package coverage contains APIs for writing coverage profile data at runtime from
long-running and/or server programs that do not terminate via os.Exit.

FUNCTIONS

func ClearCounters() error
    ClearCounters clears/resets all coverage counter variables in the currently
    running program. It returns an error if the program in question was not
    built with the "-cover" flag. Clearing of coverage counters is also not
    supported for programs not using atomic counter mode (see more detailed
    comments below for the rationale here).

func WriteCounters(w io.Writer) error
    WriteCounters writes coverage counter-data content for the currently running
    program to the writer 'w'. An error will be returned if the operation can't
    be completed successfully (for example, if the currently running program was
    not built with "-cover", or if a write fails). The counter data written will
    be a snapshot taken at the point of the invocation.

func WriteCountersDir(dir string) error
    WriteCountersDir writes a coverage counter-data file for the currently
    running program to the directory specified in 'dir'. An error will be
    returned if the operation can't be completed successfully (for example,
    if the currently running program was not built with "-cover", or if the
    directory does not exist). The counter data written will be a snapshot taken
    at the point of the call.

func WriteMeta(w io.Writer) error
    WriteMeta writes the meta-data content (the payload that would normally
    be emitted to a meta-data file) for the currently running program to the
    writer 'w'. An error will be returned if the operation can't be completed
    successfully (for example, if the currently running program was not built
    with "-cover", or if a write fails).

func WriteMetaDir(dir string) error
    WriteMetaDir writes a coverage meta-data file for the currently running
    program to the directory specified in 'dir'. An error will be returned if
    the operation can't be completed successfully (for example, if the currently
    running program was not built with "-cover", or if the directory does not
    exist).
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
