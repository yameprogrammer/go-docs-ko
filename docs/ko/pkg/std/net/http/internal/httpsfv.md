# package net/http/internal/httpsfv

- 원문: <https://pkg.go.dev/net/http/internal/httpsfv>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package httpsfv // import "net/http/internal/httpsfv"


FUNCTIONS

func ParseBareInnerList(s string, f func(bareItem, param string)) (ok bool)
    ParseBareInnerList parses a bare inner list from a given HTTP Structured
    Field Values.

    We define a bare inner list as an inner list
    (https://www.rfc-editor.org/rfc/rfc9651.html#name-parsing-an-inner-list),
    without the top-most parameter of the inner list. For example, given the
    inner list `(a;b c;d);e`, the bare inner list would be `(a;b c;d)`.

    Given an HTTP SFV string that represents a bare inner list, it will call
    the given function using each of the bare item and parameter within the bare
    inner list. This allows the caller to extract information out of the bare
    inner list.

    This function will return once it encounters the end of the bare inner list,
    or something that is not a bare inner list. If it cannot consume the entire
    given string, the ok value returned will be false.

func ParseBoolean(s string) (parsed bool, ok bool)
    ParseBoolean parses a boolean from a given HTTP Structured Field Values.

    The entire HTTP SFV string must consist of a valid boolean. It returns the
    parsed boolean and an ok boolean value, indicating success or not.

    https://www.rfc-editor.org/rfc/rfc9651.html#name-parsing-a-boolean.

func ParseByteSequence(s string) (parsed []byte, ok bool)
    ParseByteSequence parses a byte sequence from a given HTTP Structured Field
    Values.

    The entire HTTP SFV string must consist of a valid byte sequence. It returns
    the parsed byte sequence and an ok boolean value, indicating success or not.

    https://www.rfc-editor.org/rfc/rfc9651.html#name-parsing-a-byte-sequence.

func ParseDate(s string) (parsed time.Time, ok bool)
    ParseDate parses a date from a given HTTP Structured Field Values.

    The entire HTTP SFV string must consist of a valid date. It returns the
    parsed date and an ok boolean value, indicating success or not.

    https://www.rfc-editor.org/rfc/rfc9651.html#name-parsing-a-date.

func ParseDecimal(s string) (parsed float64, ok bool)
    ParseDecimal parses a decimal from a given HTTP Structured Field Values.

    The entire HTTP SFV string must consist of a valid decimal. It returns the
    parsed decimal and an ok boolean value, indicating success or not.

    https://www.rfc-editor.org/rfc/rfc9651.html#name-parsing-an-integer-or-decim.

func ParseDictionary(s string, f func(key, val, param string)) (ok bool)
    ParseDictionary parses a dictionary from a given HTTP Structured Field
    Values.

    Given an HTTP SFV string that represents a dictionary, it will call the
    given function using each of the keys, values, and parameters contained in
    the dictionary. This allows the caller to extract information out of the
    dictionary.

    This function will return once it encounters the end of the string,
    or something that is not a dictionary. If it cannot consume the entire given
    string, the ok value returned will be false.

    https://www.rfc-editor.org/rfc/rfc9651.html#name-parsing-a-dictionary.

func ParseDisplayString(s string) (parsed string, ok bool)
    ParseDisplayString parses a display string from a given HTTP Structured
    Field Values.

    The entire HTTP SFV string must consist of a valid display string.
    It returns the parsed display string and an ok boolean value, indicating
    success or not.

    https://www.rfc-editor.org/rfc/rfc9651.html#name-parsing-a-display-string.

func ParseInteger(s string) (parsed int64, ok bool)
    ParseInteger parses an integer from a given HTTP Structured Field Values.

    The entire HTTP SFV string must consist of a valid integer. It returns the
    parsed integer and an ok boolean value, indicating success or not.

    https://www.rfc-editor.org/rfc/rfc9651.html#name-parsing-an-integer-or-decim.

func ParseItem(s string, f func(bareItem, param string)) (ok bool)
    ParseItem parses an item from a given HTTP Structured Field Values.

    Given an HTTP SFV string that represents an item, it will call the given
    function once, with the bare item and the parameter of the item. This allows
    the caller to extract information out of the item.

    This function will return once it encounters the end of the string, or
    something that is not an item. If it cannot consume the entire given string,
    the ok value returned will be false.

    https://www.rfc-editor.org/rfc/rfc9651.html#name-parsing-an-item.

func ParseList(s string, f func(member, param string)) (ok bool)
    ParseList parses a list from a given HTTP Structured Field Values.

    Given an HTTP SFV string that represents a list, it will call the given
    function using each of the members and parameters contained in the list.
    This allows the caller to extract information out of the list.

    This function will return once it encounters the end of the string, or
    something that is not a list. If it cannot consume the entire given string,
    the ok value returned will be false.

    https://www.rfc-editor.org/rfc/rfc9651.html#name-parsing-a-list.

func ParseParameter(s string, f func(key, val string)) (ok bool)
    ParseParameter parses a parameter from a given HTTP Structured Field Values.

    Given an HTTP SFV string that represents a parameter, it will call the given
    function using each of the keys and values contained in the parameter.
    This allows the caller to extract information out of the parameter.

    This function will return once it encounters the end of the string,
    or something that is not a parameter. If it cannot consume the entire given
    string, the ok value returned will be false.

    https://www.rfc-editor.org/rfc/rfc9651.html#parse-param.

func ParseString(s string) (parsed string, ok bool)
    ParseString parses a Go string from a given HTTP Structured Field Values.

    The entire HTTP SFV string must consist of a valid string. It returns the
    parsed string and an ok boolean value, indicating success or not.

    https://www.rfc-editor.org/rfc/rfc9651.html#name-parsing-a-string.

func ParseToken(s string) (parsed string, ok bool)
    ParseToken parses a token from a given HTTP Structured Field Values.

    The entire HTTP SFV string must consist of a valid token. It returns the
    parsed token and an ok boolean value, indicating success or not.

    https://www.rfc-editor.org/rfc/rfc9651.html#name-parsing-a-token
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
