# package math/cmplx

- 원문: <https://pkg.go.dev/math/cmplx>
- 분류: Go 표준 라이브러리

## 한국어 요약

`cmplx` 패키지는 복소수를 위한 기본적인 상수와 수학 함수를 제공합니다.

## 원문 요약

Package cmplx provides basic constants and mathematical functions for complex numbers.

## API 상세 (go doc -all)

~~~text
package cmplx // import "math/cmplx"

Package cmplx provides basic constants and mathematical functions for complex
numbers. Special case handling conforms to the C99 standard Annex G IEC
60559-compatible complex arithmetic.

FUNCTIONS

func Abs(x complex128) float64
    Abs returns the absolute value (also called the modulus) of x.

func Acos(x complex128) complex128
    Acos returns the inverse cosine of x.

func Acosh(x complex128) complex128
    Acosh returns the inverse hyperbolic cosine of x.

func Asin(x complex128) complex128
    Asin returns the inverse sine of x.

func Asinh(x complex128) complex128
    Asinh returns the inverse hyperbolic sine of x.

func Atan(x complex128) complex128
    Atan returns the inverse tangent of x.

func Atanh(x complex128) complex128
    Atanh returns the inverse hyperbolic tangent of x.

func Conj(x complex128) complex128
    Conj returns the complex conjugate of x.

func Cos(x complex128) complex128
    Cos returns the cosine of x.

func Cosh(x complex128) complex128
    Cosh returns the hyperbolic cosine of x.

func Cot(x complex128) complex128
    Cot returns the cotangent of x.

func Exp(x complex128) complex128
    Exp returns e**x, the base-e exponential of x.

func Inf() complex128
    Inf returns a complex infinity, complex(+Inf, +Inf).

func IsInf(x complex128) bool
    IsInf reports whether either real(x) or imag(x) is an infinity.

func IsNaN(x complex128) bool
    IsNaN reports whether either real(x) or imag(x) is NaN and neither is an
    infinity.

func Log(x complex128) complex128
    Log returns the natural logarithm of x.

func Log10(x complex128) complex128
    Log10 returns the decimal logarithm of x.

func NaN() complex128
    NaN returns a complex “not-a-number” value.

func Phase(x complex128) float64
    Phase returns the phase (also called the argument) of x. The returned value
    is in the range [-Pi, Pi].

func Polar(x complex128) (r, θ float64)
    Polar returns the absolute value r and phase θ of x, such that x = r *
    e**θi. The phase is in the range [-Pi, Pi].

func Pow(x, y complex128) complex128
    Pow returns x**y, the base-x exponential of y. For generalized compatibility
    with math.Pow:

        Pow(0, ±0) returns 1+0i
        Pow(0, c) for real(c)<0 returns Inf+0i if imag(c) is zero, otherwise Inf+Inf i.

func Rect(r, θ float64) complex128
    Rect returns the complex number x with polar coordinates r, θ.

func Sin(x complex128) complex128
    Sin returns the sine of x.

func Sinh(x complex128) complex128
    Sinh returns the hyperbolic sine of x.

func Sqrt(x complex128) complex128
    Sqrt returns the square root of x. The result r is chosen so that real(r) ≥
    0 and imag(r) has the same sign as imag(x).

func Tan(x complex128) complex128
    Tan returns the tangent of x.

func Tanh(x complex128) complex128
    Tanh returns the hyperbolic tangent of x.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
