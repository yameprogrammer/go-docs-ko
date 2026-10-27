# package internal/trace/traceviewer/format

- 원문: <https://pkg.go.dev/internal/trace/traceviewer/format>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 `traceviewer`는 Chrome 트레이스 뷰어에서 사용되는 JSON 데이터 구조의 정의를 제공합니다.

## 원문 요약

Package traceviewer provides definitions of the JSON data structures used by the Chrome trace viewer.

## API 상세 (go doc -all)

~~~text
package format // import "internal/trace/traceviewer/format"

Package traceviewer provides definitions of the JSON data structures used by the
Chrome trace viewer.

The official description of the format is in this file:
https://docs.google.com/document/d/1CvAClvFfyA5R-PhYUmn5OOQtYMH4h6I0nSsKchNAySU/preview

Note: This can't be part of the parent traceviewer package as that would throw.
go_bootstrap cannot depend on the cgo version of package net in ./make.bash.

CONSTANTS

const (
	ProcsSection = 0 // where Goroutines or per-P timelines are presented.
	StatsSection = 1 // where counters are presented.
	TasksSection = 2 // where Task hierarchy & timeline is presented.
)

TYPES

type BlockedArg struct {
	Blocked string `json:"blocked"`
}

type Data struct {
	Events   []*Event         `json:"traceEvents"`
	Frames   map[string]Frame `json:"stackFrames"`
	TimeUnit string           `json:"displayTimeUnit"`
}

type Event struct {
	Name      string  `json:"name,omitempty"`
	Phase     string  `json:"ph"`
	Scope     string  `json:"s,omitempty"`
	Time      float64 `json:"ts"`
	Dur       float64 `json:"dur,omitempty"`
	PID       uint64  `json:"pid"`
	TID       uint64  `json:"tid"`
	ID        uint64  `json:"id,omitempty"`
	BindPoint string  `json:"bp,omitempty"`
	Stack     int     `json:"sf,omitempty"`
	EndStack  int     `json:"esf,omitempty"`
	Arg       any     `json:"args,omitempty"`
	Cname     string  `json:"cname,omitempty"`
	Category  string  `json:"cat,omitempty"`
}

type Frame struct {
	Name   string `json:"name"`
	Parent int    `json:"parent,omitempty"`
}

type GoroutineCountersArg struct {
	Running   uint64
	Runnable  uint64
	GCWaiting uint64
}

type HeapCountersArg struct {
	Allocated uint64
	NextGC    uint64
}

type NameArg struct {
	Name string `json:"name"`
}

type SchedCtxArg struct {
	ThreadID uint64 `json:"thread,omitempty"`
	ProcID   uint64 `json:"proc,omitempty"`
}

type SortIndexArg struct {
	Index int `json:"sort_index"`
}

type ThreadCountersArg struct {
	Running   int64
	InSyscall int64
}
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
