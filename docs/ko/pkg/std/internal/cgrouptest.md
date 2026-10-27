# package internal/cgrouptest

- 원문: <https://pkg.go.dev/internal/cgrouptest>
- 분류: Go 표준 라이브러리

## 한국어 요약

`cgrouptest` 패키지는 cgroup 내부에서 테스트를 실행하기 위한 최선의 노력(best-effort) 헬퍼들을 제공합니다.

## 원문 요약

Package cgrouptest provides best-effort helpers for running tests inside a cgroup.

## API 상세 (go doc -all)

~~~text
package cgrouptest // import "internal/cgrouptest"

Package cgrouptest provides best-effort helpers for running tests inside a
cgroup.

FUNCTIONS

func InCgroupV2(t *testing.T, fn func(*CgroupV2))
    InCgroupV2 creates a new v2 cgroup, migrates the current process into it,
    and then calls fn. When fn returns, the current process is migrated back to
    the original cgroup and the new cgroup is destroyed.

    If a new cgroup cannot be created, the test is skipped.

    This must not be used in parallel tests, as it affects the entire process.


TYPES

type CgroupV2 struct {
	// Has unexported fields.
}

func (c *CgroupV2) CPUMaxPath() string
    Path to cpu.max.

func (c *CgroupV2) Path() string

func (c *CgroupV2) SetCPUMax(quota, period int64) error
    Set cpu.max. Pass -1 for quota to disable the limit.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
