# 알고리즘 임계값 보정 (Calibration of Algorithm Thresholds)

이 문서는 [calibrate_test.go](calibrate_test.go)에 구현된 `math/big` 내 알고리즘 임계값(thresholds)의 캘리브레이션 접근 방식에 대해 설명합니다.

곱셈 및 나눗셈과 같은 기본 연산은 다양한 구현 방법이 존재합니다.
점근적으로 더 효율적인 대부분의 알고리즘은 오버헤드가 있어 입력값이 작을 때는 오히려 더 느리게 실행됩니다. 연산을 수행해야 할 때, `math/big`은 어떤 알고리즘을 사용할지 결정해야 합니다.

예를 들어, 입력 값이 작을 때는 "초등학교 곱셈 알고리즘(grade school algorithm)"을 사용한 곱셈이 가장 빠릅니다.
여러 자리의 $x, y$와 결과값이 저장될 $z$가 주어졌을 때, $z$를 비우고 각 자리수 $y[i]$에 대해 $z[i:] += x * y[i]$를 수행합니다.
벡터에 (자리수와 벡터의 곱을 더하는) 마지막 연산은(곱셈 및 덧셈 과정에서의 올림 처리 포함), 최적화된 어셈블리 루프로 구현할 수 있습니다.
전체 속도는 $x$와 $y$의 자리수 $N$에 대해 $O(N^2)$이지만(두 자리수가 같다고 가정), 최적화된 내부 루프는 입력 값이 작을 때 좋은 성능을 보입니다.

[Karatsuba 알고리즘](https://en.wikipedia.org/wiki/Karatsuba_algorithm)은
두 개의 N자리 숫자를 반으로 나누어 세 개의 N/2자리 곱셈을 계산한 뒤, 몇 번의 덧셈과 뺄셈을 통해 최종 곱셈 결과를 재구성하여 곱하는 방식입니다. 이 알고리즘은 O(N\*\*log₂ 3) = O(N\*\*1.58) 시간에 실행됩니다.
입력값이 작을 때는 초등학교 방식의 루프가 더 빠르게 작동하지만, 결국 Karatsuba의 더 짧은 점근적 실행 시간이 승리하게 됩니다.

곱셈 구현체는 어떤 방식을 사용할지 결정해야 합니다.
어느 지점 N부터 Karatsuba 알고리즘이 더 빨라지면, 그보다 더 큰 모든 N에 대해서도 계속 더 빠를 것이라는 가정하에,
입력 길이 N이 `karatsubaThreshold` 이상일 때 Karatsuba 알고리즘을 사용하는 규칙을 적용합니다.

Calibration은 `karatsubaThreshold`를 얼마로 설정해야 하는지 결정하는 과정입니다.
그렇게 어렵지 않을 것처럼 들리지만, 실제로는 다음과 같은 이유로 어렵습니다:
- 이론적 분석은 도움이 되지 않습니다: 정답은 실제 기계와 두 구현체에 포함된 실제 상수 요인(constant factors)에 따라 달라집니다.
- 우리는 모든 시스템에 대해 단일한 `karatsubaThreshold`를 선택하고 있습니다. 하지만 시스템마다 두 알고리즘의 연산에 대한 상대적인 실행 속도가 다릅니다.
(이론적으로는 아키텍처마다 다른 임계값을 선택할 수 있겠지만, 동일한 아키텍처 내에서도 상당한 편차가 있을 수 있습니다.)
- 점근적으로 더 우수한 알고리즘이 더 빨라지기 시작하여 계속 더 빠른 상태를 유지하는 단일한 $N$이 존재한다는 가정은 일반적으로 사실이 아닙니다.
- Karatsuba와 같은 재귀 알고리즘은 입력 크기가 큰 서로 다른 경우에 대해 서로 다른 최적의 임계값을 가질 수 있습니다.
- 임계값들이 서로 간섭할 수 있습니다. 예를 들어, `karatsubaThreshold`를 변경하면 곱셈 속도가 빨라지거나 느려지며, 이는 다시 최적의 `divRecursiveThreshold`에 영향을 줍니다(나눗셈에서 곱셈을 사용하기 때문입니다).

우리가 할 수 있는 최선은 다양한 입력값과 임계값에 걸쳐 전체 곱셈 알고리즘의 성능을 측정하고, 이러한 모든 고려 사항들을 합리적으로 균형 있게 조절하는 임계값을 찾는 것입니다. 이때 임계값은 의존성 순서(예: 나눗셈 전의 곱셈)에 따라 설정합니다.

`calibrate_test.go`의 코드는 다양한 입력 크기와 임계값(threshold)에 대해 이러한 측정을 수행하고, 타이밍 결과를 CSV 파일로 출력합니다.
`calibrate_graph.go`의 코드는 해당 CSV를 읽어 데이터를 플롯한 SVG 파일을 생성합니다.
예를 들어:

```bash
go test -run=Calibrate/KaratsubaMul -timeout=1h -calibrate >kmul.csv
	go run calibrate_graph.go kmul.csv >kmul.svg
```

특정 입력은 임계값(threshold)의 아주 적은 수의 전환에만 민감하게 반응합니다.
예를 들어, 크기가 320인 입력은 크기가 160인 입력으로 재귀 호출되고,
이는 다시 크기가 80인 입력으로,
이는 다시 크기가 40인 입력으로 재귀 호출되며,
이런 식으로 Karatsuba 임계값 아래로 떨어질 때까지 계속됩니다.
다음은 크기가 320인 입력에 대한 타이밍 결과이며, 가장 빠른 타이밍을 1.0으로 정규화한 값입니다.

![Apple M3 Pro에서의 KaratsubaThreshold, N=320 전용](https://swtch.com/math/big/_calibrate/KaratsubaMul/cal.mac320.svg)

이 입력의 경우, 21부터 40까지의 모든 임계값이 최적으로 그리고 동일하게 작동합니다. 즉, 모두 "N=40에서는 재귀 호출을 수행하지만 N=20에서는 수행하지 않음"을 의미합니다.
크기가 N=320인 단일 입력만으로는 이 20개의 임계값 중 어느 것이 최적인지 결정할 수 없습니다.

다른 입력값들은 다른 결정 지점들을 실행합니다. 예를 들어, N=240일 때의 타이밍은 다음과 같습니다:

![Apple M3 Pro에서의 KaratsubaThreshold, N=240 전용](https://swtch.com/math/big/_calibrate/KaratsubaMul/cal.mac240.svg)

이 경우, 31에서 60 사이의 모든 임계값은 최적으로 동일하게 작동하며, N=60에서는 재귀적으로 수행되지만 N=30에서는 그렇지 않습니다.

이 두 가지를 하나의 그래프로 결합하고 두 선의 기하 평균을 파란색으로 표시하면, 최적의 범위가 조금 더 명확해집니다:

![Apple M3 Pro에서의 KaratsubaThreshold](https://swtch.com/math/big/_calibrate/KaratsubaMul/cal.mac240+320.svg)

실제 보정(calibration) 과정에서는 N=200부터 N=400까지 8씩 증가시키며 가능한 모든 입력을 실행하며, 26개의 모든 선을 연한 회색으로 플로팅합니다 (y축 스케일이 변경되어 1.0 근처로 확대되었음에 유의하십시오).

![Apple M3 Pro에서의 KaratsubaThreshold](https://swtch.com/math/big/_calibrate/KaratsubaMul/cal.mac.svg)

이제 최적값이 명확해졌습니다. 이러한 알고리즘 구현을 적용했을 때, 이 칩에서의 최적 임계값(threshold)은 40입니다.

안타깝게도 다른 칩들은 다릅니다. 여기 Intel Xeon 서버 칩이 있습니다:

![Intel Xeon Gold 6253CL에서의 KaratsubaThreshold](https://swtch.com/math/big/_calibrate/KaratsubaMul/cal.c2s16.svg)

이 칩에서 가장 적절한 임계값(threshold)은 60에 더 가깝습니다. 다행히 40 또한 나쁜 선택은 아닙니다. 평균적으로 약 2% 정도만 더 느리기 때문입니다.

이 문서의 나머지 부분에서는 다양한 머신에서 `math/big` 임계값에 대해 측정된 타이밍을 제시하고 최종 임계값의 타당성을 설명합니다. 타이밍 측정에는 다음 머신들이 사용되었습니다:

- `gotip-linux-amd64_c3h88-perf_vs_release` gomote: Intel Xeon Platinum 8481C CPU (Emerald Rapids)를 사용하는 Google Cloud c3-high-88 머신.
- `gotip-linux-amd64_c2s16-perf_vs_release` gomote: Intel Xeon Gold 6253CL CPU (Cascade Lake)를 사용하는 Google Cloud c2-standard-16 머신.
- AMD Ryzen 9 7950X CPU로 구축한 홈 서버.
- `gotip-linux-arm64_c4as16-perf_vs_release` gomote: Google의 Axiom Arm CPU를 사용하는 Google Cloud c4a-standard-16 머신.
- Apple M3 Pro CPU가 탑재된 Apple MacBook Pro.

일반적으로, 동일한 조건일 경우 최신 c3h88 x86 perf gomote를 우선순위로 두고, 그다음으로 c4as16 arm64 perf gomote, 그리고 나머지들을 순차적으로 선택하여 처리합니다.

## Karatsuba 곱셈 (Karatsuba Multiplication)

Karatsuba 곱셈 임계값(threshold)에 대한 전체 결과입니다.

![Intel Xeon Platinum 8481C에서의 KaratsubaThreshold](https://swtch.com/math/big/_calibrate/KaratsubaMul/cal.c3h88.svg)
![Intel Xeon Gold 6253CL에서의 KaratsubaThreshold](https://swtch.com/math/big/_calibrate/KaratsubaMul/cal.c2s16.svg)
![AMD Ryzen 9 7950X에서의 KaratsubaThreshold](https://swtch.com/math/big/_calibrate/KaratsubaMul/cal.s7.svg)
![Axiom Arm에서의 KaratsubaThreshold](https://swtch.com/math/big/_calibrate/KaratsubaMul/cal.c4as16.svg)
![Apple M3 Pro에서의 KaratsubaThreshold](https://swtch.com/math/big/_calibrate/KaratsubaMul/cal.mac.svg)

대부분의 시스템은 40 근처에서 최적의 임계값을 가지므로, `karatsubaThreshold = 40`으로 선택했습니다.

## 기본 제곱 구하기

숫자를 제곱할 때 (`z.Mul(x, x)`), `math/big`은 `basicSqrThreshold`까지는 초등학교 방식의 곱셈(grade school multiplication)을 사용하며, 그 이후에는 커스텀 알고리즘으로 전환합니다. 이 알고리즘은 여전히 이차 시간 복잡도(quadratic)를 갖지만, 두 인자가 동일하기 때문에 워드 단위 곱셈 횟수를 절반으로 줄일 수 있습니다.

해당 알고리즘의 내부 루프는 초등학교 방식의 곱셈만큼 타이트하지 않기 때문에 입력값이 작을 때는 더 느립니다. 어느 정도로 작을 때 그럴까요?

타이밍은 다음과 같습니다:

![BasicSqrThreshold on an Intel Xeon Platinum 8481C](https://swtch.com/math/big/_calibrate/BasicSqr/cal.c3h88.svg)
![BasicSqrThreshold on an Intel Xeon Gold 6253CL](https://swtch.com/math/big/_calibrate/BasicSqr/cal.c2s16.svg)
![BasicSqrThreshold on an AMD Ryzen 9 7950X](https://swtch.com/math/big/_calibrate/BasicSqr/cal.s7.svg)
![BasicSqrThreshold on an Axiom Arm](https://swtch.com/math/big/_calibrate/BasicSqr/cal.c4as16.svg)
![BasicSqrThreshold on an Apple M3 Pro](https://swtch.com/math/big/_calibrate/BasicSqr/cal.mac.svg)

이 입력값들은 매우 작기 때문에, 캘리브레이션 시 개별 연산 대신 100개씩 배치로 처리합니다.
단일 시스템 내에서도 최적의 임계값(threshold) 하나만 존재하지는 않는데, 이는 일부 크기에서는 초등학교 방식의 알고리즘(grade school algorithm)이 다른 크기보다 더 빠르게 실행되는 것으로 보이기 때문입니다.
예를 들어 AMD CPU의 경우,
N=14일 때는 기본 제곱 연산이 기본 곱셈 연산보다 4% 더 빠르며 이는 임계값을 넘어섰음을 시사하지만,
N=16일 때는 기본 곱셈 연산이 기본 제곱 연산보다 9% 더 빠릅니다.
이는 아마도 최적화된 어셈블리가 더 큰 덩어리(chunk)를 사용할 수 있기 때문일 것입니다.

Axiom Arm 타이밍이 왜 이렇게 믿기 힘들 정도로 노이즈가 심한지 불분명합니다.

우리는 `basicSqrThreshold = 12`로 선택했습니다.

## Karatsuba 제곱 (Karatsuba Squaring)

기본적인 제곱 임계값을 넘어 어느 시점부터는 커스텀 Karatsuba 알고리즘이 적용될 수 있습니다.
이 알고리즘은 3개의 절반 크기 곱셈 대신 3개의 절반 크기 제곱 연산을 사용합니다.
타이밍은 다음과 같습니다:

![Intel Xeon Platinum 8481C에서의 KaratsubaSqrThreshold](https://swtch.com/math/big/_calibrate/KaratsubaSqr/cal.c3h88.svg)
![Intel Xeon Gold 6253CL에서의 KaratsubaSqrThreshold](https://swtch.com/math/big/_calibrate/KaratsubaSqr/cal.c2s16.svg)
![AMD Ryzen 9 7950X에서의 KaratsubaSqrThreshold](https://swtch.com/math/big/_calibrate/KaratsubaSqr/cal.s7.svg)
![Axiom Arm에서의 KaratsubaSqrThreshold](https://swtch.com/math/big/_calibrate/KaratsubaSqr/cal.c4as16.svg)
![Apple M3 Pro에서의 KaratsubaSqrThreshold](https://swtch.com/math/big/_calibrate/KaratsubaSqr/cal.mac.svg)

대부분의 칩은 60-70 정도의 낮은 임계값을 선호했지만, 구형 Intel Xeon과 AMD는 100-120 정도의 임계값을 선호합니다.

우리는 모든 칩에서 최적값의 2% 이내인 `karatsubaSqrThreshold = 80`을 선택했습니다.

## 재귀적 나눗셈 (Recursive Division)

나눗셈은 큰 입력값에 대해 재귀적인 분할 정복(divide-and-conquer) 알고리즘을 사용하며, 최종적으로는 더 전통적인 초등 수학 방식의 전체 입력 시도-오류(trial-and-error) 나눗셈 방식으로 전환됩니다.
다음은 두 방식 사이의 임계값(threshold)에 대한 타이밍입니다:

![Intel Xeon Platinum 8481C에서의 DivRecursiveThreshold](https://swtch.com/math/big/_calibrate/DivRecursive/cal.c3h88.svg)
![Intel Xeon Gold 6253CL에서의 DivRecursiveThreshold](https://swtch.com/math/big/_calibrate/DivRecursive/cal.c2s16.svg)
![AMD Ryzen 9 7950X에서의 DivRecursiveThreshold](https://swtch.com/math/big/_calibrate/DivRecursive/cal.s7.svg)
![Axiom Arm에서의 DivRecursiveThreshold](https://swtch.com/math/big/_calibrate/DivRecursive/cal.c4as16.svg)
![Apple M3 Pro에서의 DivRecursiveThreshold](https://swtch.com/math/big/_calibrate/DivRecursive/cal.mac.svg)

우리는 `divRecursiveThreshold = 40`으로 선택했습니다.
