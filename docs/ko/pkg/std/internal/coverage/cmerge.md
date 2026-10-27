# package internal/coverage/cmerge

- 원문: <https://pkg.go.dev/internal/coverage/cmerge>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package cmerge // import "internal/coverage/cmerge"


FUNCTIONS

func SaturatingAdd(dst, src uint32) (uint32, bool)
    SaturatingAdd does a saturating addition of 'dst' and 'src', returning added
    value or math.MaxUint32 plus an overflow flag.


TYPES

type Merger struct {
	// Has unexported fields.
}
    Merger provides state and methods to help manage the process of merging
    together coverage counter data for a given function, for tools that need to
    implicitly merge counter as they read multiple coverage counter data files.

func (cm *Merger) Granularity() coverage.CounterGranularity

func (m *Merger) MergeCounters(dst, src []uint32) (error, bool)
    MergeCounters takes the counter values in 'src' and merges them into 'dst'
    according to the correct counter mode.

func (cm *Merger) Mode() coverage.CounterMode

func (cm *Merger) ResetModeAndGranularity()

func (m *Merger) SaturatingAdd(dst, src uint32) uint32
    SaturatingAdd does a saturating addition of 'dst' and 'src', returning added
    value or math.MaxUint32 if there is an overflow. Overflows are recorded in
    case the client needs to track them.

func (cm *Merger) SetModeAndGranularity(mdf string, cmode coverage.CounterMode, cgran coverage.CounterGranularity) error
    SetModeAndGranularity records the counter mode and granularity for the
    current merge. In the specific case of merging across coverage data files
    from different binaries, where we're combining data from more than one
    meta-data file, we need to check for and resolve mode/granularity clashes.

func (cm *Merger) SetModeMergePolicy(policy ModeMergePolicy)

type ModeMergePolicy uint8

const (
	ModeMergeStrict ModeMergePolicy = iota
	ModeMergeRelaxed
)
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
