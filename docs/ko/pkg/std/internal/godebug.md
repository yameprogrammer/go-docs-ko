# package internal/godebug

- 원문: <https://pkg.go.dev/internal/godebug>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package godebug makes the settings in the $GODEBUG environment variable available to other packages.

## 원문 요약

Package godebug makes the settings in the $GODEBUG environment variable available to other packages.

## API 상세 (go doc -all)

~~~text
package godebug // import "internal/godebug"

Package godebug makes the settings in the $GODEBUG environment variable
available to other packages. These settings are often used for compatibility
tweaks, when we need to change a default behavior but want to let users opt back
in to the original. For example GODEBUG=http2server=0 disables HTTP/2 support in
the net/http server.

In typical usage, code should declare a Setting as a global and then call Value
each time the current setting value is needed:

    var http2server = godebug.New("http2server")

    func ServeConn(c net.Conn) {
    	if http2server.Value() == "0" {
    		disallow HTTP/2
    		...
    	}
    	...
    }

Each time a non-default setting causes a change in program behavior, code
must call Setting.IncNonDefault to increment a counter that can be reported
by runtime/metrics.Read. The call must only happen when the program executes a
non-default behavior, not just when the setting is set to a non-default value.
This is occasionally (but very rarely) infeasible, in which case the
internal/godebugs table entry must set Opaque: true, and the documentation in
doc/godebug.md should mention that metrics are unavailable.

Conventionally, the global variable representing a godebug is named for the
godebug itself, with no case changes:

    var gotypesalias = godebug.New("gotypesalias") // this
    var goTypesAlias = godebug.New("gotypesalias") // NOT THIS

The test in internal/godebugs that checks for use of IncNonDefault requires the
use of this convention.

Note that counters used with IncNonDefault must be added to various tables in
other packages. See the Setting.IncNonDefault documentation for details.

TYPES

type Setting struct {
	// Has unexported fields.
}
    A Setting is a single setting in the $GODEBUG environment variable.

func New(name string) *Setting
    New returns a new Setting for the $GODEBUG setting with the given name.

    GODEBUGs meant for use by end users must be listed in ../godebugs/table.go,
    which is used for generating and checking various documentation.
    If the name is not listed in that table, New will succeed but calling
    Value on the returned Setting will panic. To disable that panic for
    access to an undocumented setting, prefix the name with a #, as in
    godebug.New("#gofsystrace"). The # is a signal to New but not part of the
    key used in $GODEBUG.

    Note that almost all settings should arrange to call [IncNonDefault]
    precisely when program behavior is changing from the default due to the
    setting (not just when the setting is different, but when program behavior
    changes). See the internal/godebug package comment for more.

func (s *Setting) IncNonDefault()
    IncNonDefault increments the non-default behavior counter associated with
    the given setting. This counter is exposed in the runtime/metrics value
    /godebug/non-default-behavior/<name>:events.

    Note that Value must be called at least once before IncNonDefault.

func (s *Setting) Name() string
    Name returns the name of the setting.

func (s *Setting) String() string
    String returns a printable form for the setting: name=value.

func (s *Setting) Undocumented() bool
    Undocumented reports whether this is an undocumented setting.

func (s *Setting) Value() string
    Value returns the current value for the GODEBUG setting s.

    Value maintains an internal cache that is synchronized with changes to the
    $GODEBUG environment variable, making Value efficient to call as frequently
    as needed. Clients should therefore typically not attempt their own caching
    of Value's result.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
