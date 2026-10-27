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

FUNCTIONS

func FindCPU(out []byte, scratch []byte) (int, Version, error)
    FindCPU finds the path to the CPU cgroup that this process is a member of
    and places it in out. scratch is a scratch buffer for internal use.

    out must have length PathSize. scratch must have length ParseSize.

    Returns the number of bytes written to out and the cgroup version (1 or 2).

    Returns ErrNoCgroup if the process is not in a CPU cgroup.

func FindCPUCgroup(out []byte, scratch []byte) (int, Version, error)
    FindCPUCgroup finds the path to the CPU cgroup that this process is a member
    of and places it in out. scratch is a scratch buffer for internal use.

    out must have length PathSize. scratch must have length ParseSize.

    Returns the number of bytes written to out and the cgroup version (1 or 2).

    Returns ErrNoCgroup if the process is not in a CPU cgroup.

func FindCPUMountPoint(out, cgroup []byte, version Version, scratch []byte) (int, error)
    FindCPUMountPoint finds the mount point containing the specified cgroup and
    version with cpu controller, and compose the full path to the cgroup in out.
    scratch is a scratch buffer for internal use.

    out must have length PathSize, may overlap with cgroup. scratch must have
    length ParseSize.

    Returns the number of bytes written to out.

    Returns ErrNoCgroup if no matching mount point is found.

func OpenCPU(scratch []byte) (CPU, error)
    OpenCPU returns a CPU for the CPU cgroup containing the current process,
    or ErrNoCgroup if the process is not in a CPU cgroup.

    scratch must have length ScratchSize.

func ReadCPULimit(c CPU) (float64, bool, error)
    Returns average CPU throughput limit from the cgroup, or ok false if there
    is no limit.


TYPES

type CPU struct {
	// Has unexported fields.
}
    CPU owns the FDs required to read the CPU limit from a cgroup.

func (c CPU) Close()

type Version int
    Version indicates the cgroup version.

const (
	VersionUnknown Version = iota
	V1
	V2
)
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
