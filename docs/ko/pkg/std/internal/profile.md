# package internal/profile

- 원문: <https://pkg.go.dev/internal/profile>
- 분류: Go 표준 라이브러리

## 한국어 요약

패키지 프로필은 pprof 프로필을 방향성 그래프로 나타냅니다.

## 원문 요약

Package profile represents a pprof profile as a directed graph.

## API 상세 (go doc -all)

~~~text
package profile // import "internal/profile"

Package profile represents a pprof profile as a directed graph.

This package is a simplified fork of github.com/google/pprof/internal/graph.

Package profile provides a representation of
github.com/google/pprof/proto/profile.proto and methods to encode/decode/merge
profiles in this format.

VARIABLES

var ErrNoData = fmt.Errorf("empty input file")

FUNCTIONS

func CreateNodes(prof *Profile, o *Options) (Nodes, locationMap)
    CreateNodes creates graph nodes for all locations in a profile.
    It returns set of all nodes, plus a mapping of each location to the set of
    corresponding nodes (one per location.Line).


TYPES

type Demangler func(name []string) (map[string]string, error)
    Demangler maps symbol names to a human-readable form. This may include C++
    demangling and additional simplification. Names that are not demangled may
    be missing from the resulting map.

type Edge struct {
	Src, Dest *Node
	// The summary weight of the edge
	Weight, WeightDiv int64

	// residual edges connect nodes that were connected through a
	// separate node, which has been removed from the report.
	Residual bool
	// An inline edge represents a call that was inlined into the caller.
	Inline bool
}
    Edge contains any attributes to be represented about edges in a graph.

func (e *Edge) WeightValue() int64
    WeightValue returns the weight value for this edge, normalizing if a divisor
    is available.

type EdgeMap []*Edge
    EdgeMap is used to represent the incoming/outgoing edges from a node.

func (em *EdgeMap) Add(e *Edge)

func (em *EdgeMap) Delete(e *Edge)

func (em EdgeMap) FindTo(n *Node) *Edge

func (em EdgeMap) Sort() []*Edge
    Sort returns a slice of the edges in the map, in a consistent order.
    The sort order is first based on the edge weight (higher-to-lower) and then
    by the node names to avoid flakiness.

func (em EdgeMap) Sum() int64
    Sum returns the total weight for a set of nodes.

type Function struct {
	ID         uint64
	Name       string
	SystemName string
	Filename   string
	StartLine  int64

	// Has unexported fields.
}
    Function corresponds to Profile.Function

type Graph struct {
	Nodes Nodes
}
    Graph summarizes a performance profile into a format that is suitable for
    visualization.

func NewGraph(prof *Profile, o *Options) *Graph
    NewGraph computes a graph from a profile.

func (g *Graph) String() string
    String returns a text representation of a graph, for debugging purposes.

type Label struct {
	// Has unexported fields.
}
    Label corresponds to Profile.Label

type Line struct {
	Function *Function
	Line     int64

	// Has unexported fields.
}
    Line corresponds to Profile.Line

type Location struct {
	ID       uint64
	Mapping  *Mapping
	Address  uint64
	Line     []Line
	IsFolded bool

	// Has unexported fields.
}
    Location corresponds to Profile.Location

type Mapping struct {
	ID              uint64
	Start           uint64
	Limit           uint64
	Offset          uint64
	File            string
	BuildID         string
	HasFunctions    bool
	HasFilenames    bool
	HasLineNumbers  bool
	HasInlineFrames bool

	// Has unexported fields.
}
    Mapping corresponds to Profile.Mapping

type Node struct {
	// Info describes the source location associated to this node.
	Info NodeInfo

	// Function represents the function that this node belongs to. On
	// graphs with sub-function resolution (eg line number or
	// addresses), two nodes in a NodeMap that are part of the same
	// function have the same value of Node.Function. If the Node
	// represents the whole function, it points back to itself.
	Function *Node

	// Values associated to this node. Flat is exclusive to this node,
	// Cum includes all descendents.
	Flat, FlatDiv, Cum, CumDiv int64

	// In and out Contains the nodes immediately reaching or reached by
	// this node.
	In, Out EdgeMap
}
    Node is an entry on a profiling report. It represents a unique program
    location.

func (n *Node) AddToEdge(to *Node, v int64, residual, inline bool)
    AddToEdge increases the weight of an edge between two nodes. If there isn't
    such an edge one is created.

func (n *Node) AddToEdgeDiv(to *Node, dv, v int64, residual, inline bool)
    AddToEdgeDiv increases the weight of an edge between two nodes. If there
    isn't such an edge one is created.

func (n *Node) CumValue() int64
    CumValue returns the inclusive value for this node, computing the mean if a
    divisor is available.

func (n *Node) FlatValue() int64
    FlatValue returns the exclusive value for this node, computing the mean if a
    divisor is available.

type NodeInfo struct {
	Name              string
	Address           uint64
	StartLine, Lineno int
}
    NodeInfo contains the attributes for a node.

func (i *NodeInfo) NameComponents() []string
    NameComponents returns the components of the printable name to be used for a
    node.

func (i *NodeInfo) PrintableName() string
    PrintableName calls the Node's Formatter function with a single space
    separator.

type NodeMap map[NodeInfo]*Node
    NodeMap maps from a node info struct to a node. It is used to merge report
    entries with the same info.

func (nm NodeMap) FindOrInsertNode(info NodeInfo, kept NodeSet) *Node
    FindOrInsertNode takes the info for a node and either returns a matching
    node from the node map if one exists, or adds one to the map if one does
    not. If kept is non-nil, nodes are only added if they can be located on it.

type NodePtrSet map[*Node]bool
    NodePtrSet is a collection of nodes. Trimming a graph or tree requires
    a set of objects which uniquely identify the nodes to keep. In a graph,
    NodeInfo works as a unique identifier; however, in a tree multiple nodes may
    share identical NodeInfos. A *Node does uniquely identify a node so we can
    use that instead. Though a *Node also uniquely identifies a node in a graph,
    currently, during trimming, graphs are rebuilt from scratch using only the
    NodeSet, so there would not be the required context of the initial graph to
    allow for the use of *Node.

type NodeSet map[NodeInfo]bool
    NodeSet is a collection of node info structs.

type Nodes []*Node
    Nodes is an ordered collection of graph nodes.

func (ns Nodes) Sum() (flat int64, cum int64)
    Sum adds the flat and cum values of a set of nodes.

type Options struct {
	SampleValue       func(s []int64) int64 // Function to compute the value of a sample
	SampleMeanDivisor func(s []int64) int64 // Function to compute the divisor for mean graphs, or nil

	DropNegative bool // Drop nodes with overall negative values

	KeptNodes NodeSet // If non-nil, only use nodes in this set
}
    Options encodes the options for constructing a graph

type Profile struct {
	SampleType        []*ValueType
	DefaultSampleType string
	Sample            []*Sample
	Mapping           []*Mapping
	Location          []*Location
	Function          []*Function
	Comments          []string

	DropFrames string
	KeepFrames string

	TimeNanos     int64
	DurationNanos int64
	PeriodType    *ValueType
	Period        int64

	// Has unexported fields.
}
    Profile is an in-memory representation of profile.proto.

func Merge(srcs []*Profile) (*Profile, error)
    Merge merges all the profiles in profs into a single Profile. Returns a new
    profile independent of the input profiles. The merged profile is compacted
    to eliminate unused samples, locations, functions and mappings. Profiles
    must have identical profile sample and period types or the merge will fail.
    profile.Period of the resulting profile will be the maximum of all profiles,
    and profile.TimeNanos will be the earliest nonzero one.

func Parse(r io.Reader) (*Profile, error)
    Parse parses a profile and checks for its validity. The input must be an
    encoded pprof protobuf, which may optionally be gzip-compressed.

func (p *Profile) Aggregate(inlineFrame, function, filename, linenumber, address bool) error
    Aggregate merges the locations in the profile into equivalence classes
    preserving the request attributes. It also updates the samples to point to
    the merged locations.

func (p *Profile) CheckValid() error
    CheckValid tests whether the profile is valid. Checks include, but are not
    limited to:
      - len(Profile.Sample[n].value) == len(Profile.value_unit)
      - Sample.id has a corresponding Profile.Location

func (p *Profile) Compatible(pb *Profile) error
    Compatible determines if two profiles can be compared/merged. returns nil
    if the profiles are compatible; otherwise an error with details on the
    incompatibility.

func (p *Profile) Copy() *Profile
    Copy makes a fully independent copy of a profile.

func (p *Profile) Demangle(d Demangler) error
    Demangle attempts to demangle and optionally simplify any function names
    referenced in the profile. It works on a best-effort basis: it will silently
    preserve the original names in case of any errors.

func (p *Profile) Empty() bool
    Empty reports whether the profile contains no samples.

func (p *Profile) FilterSamplesByTag(focus, ignore TagMatch) (fm, im bool)
    FilterSamplesByTag removes all samples from the profile, except those that
    match focus and do not match the ignore regular expression.

func (p *Profile) HasFileLines() bool
    HasFileLines determines if all locations in this profile have symbolized
    file and line number information.

func (p *Profile) HasFunctions() bool
    HasFunctions determines if all locations in this profile have symbolized
    function information.

func (p *Profile) Merge(pb *Profile, r float64) error
    Merge adds profile p adjusted by ratio r into profile p. Profiles must be
    compatible (same Type and SampleType). TODO(rsilvera): consider normalizing
    the profiles based on the total samples collected.

func (p *Profile) Normalize(pb *Profile) error
    Normalize normalizes the source profile by multiplying each value in profile
    by the ratio of the sum of the base profile's values of that sample type to
    the sum of the source profile's value of that sample type.

func (p *Profile) Prune(dropRx, keepRx *regexp.Regexp)
    Prune removes all nodes beneath a node matching dropRx, and not matching
    keepRx. If the root node of a Sample matches, the sample will have an empty
    stack.

func (p *Profile) RemoveUninteresting() error
    RemoveUninteresting prunes and elides profiles using built-in tables of
    uninteresting function names.

func (p *Profile) Scale(ratio float64)
    Scale multiplies all sample values in a profile by a constant.

func (p *Profile) ScaleN(ratios []float64) error
    ScaleN multiplies each sample values in a sample by a different amount.

func (p *Profile) String() string
    Print dumps a text representation of a profile. Intended mainly for
    debugging purposes.

func (p *Profile) Write(w io.Writer) error
    Write writes the profile as a gzip-compressed marshaled protobuf.

type Sample struct {
	Location []*Location
	Value    []int64
	Label    map[string][]string
	NumLabel map[string][]int64
	NumUnit  map[string][]string

	// Has unexported fields.
}
    Sample corresponds to Profile.Sample

type TagMatch func(key, val string, nval int64) bool
    TagMatch selects tags for filtering

type ValueType struct {
	Type string // cpu, wall, inuse_space, etc
	Unit string // seconds, nanoseconds, bytes, etc

	// Has unexported fields.
}
    ValueType corresponds to Profile.ValueType
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
