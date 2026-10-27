# package internal/runtime/cgroup

- 원문: <https://pkg.go.dev/internal/runtime/cgroup>
- 분류: Go 표준 라이브러리

## 한국어 요약

_요약이 비어 있습니다._

## 원문 요약

_Synopsis is empty._

## API 상세 (go doc -all)

~~~text
package cgroup // import "internal/runtime/cgroup"


CONSTANTS

const (
	// Required amount of scratch space for CPULimit.
	//
	// TODO(prattmic): This is shockingly large (~70KiB) due to the (very
	// unlikely) combination of extremely long paths consisting mostly
	// escaped characters. The scratch buffer ends up in .bss in package
	// runtime, so it doesn't contribute to binary size and generally won't
	// be faulted in, but it would still be nice to shrink this. A more
	// complex parser that did not need to keep entire lines in memory
	// could get away with much less. Alternatively, we could do a one-off
	// mmap allocation for this buffer, which is only mapped larger if we
	// actually need the extra space.
	ScratchSize = PathSize + ParseSize

	// Required space to store a path of the cgroup in the filesystem.
	PathSize = _PATH_MAX

	// Required space to parse /proc/self/mountinfo and /proc/self/cgroup.
	// See findCPUMount and findCPURelativePath.
	ParseSize = 4 * escapedPathMax
)

VARIABLES

var (
	ErrNoCgroup error = stringError("not in a cgroup")
)

TYPES

type Version int
    Version indicates the cgroup version.

const (
	VersionUnknown Version = iota
	V1
	V2
)
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
