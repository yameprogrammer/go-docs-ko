# package internal/dag

- 원문: <https://pkg.go.dev/internal/dag>
- 분류: Go 표준 라이브러리

## 한국어 요약

`dag` 패키지는 유향 비순환 그래프(directed acyclic graphs)를 표현하기 위한 언어를 구현합니다.

## 원문 요약

Package dag implements a language for expressing directed acyclic graphs.

## API 상세 (go doc -all)

~~~text
package dag // import "internal/dag"

Package dag implements a language for expressing directed acyclic graphs.

The general syntax of a rule is:

    a, b < c, d;

which means c and d come after a and b in the partial order (that is, there are
edges from c and d to a and b), but doesn't provide a relative order between a
vs b or c vs d.

The rules can chain together, as in:

    e < f, g < h;

which is equivalent to

    e < f, g;
    f, g < h;

Except for the special bottom element "NONE", each name must appear exactly once
on the right-hand side of any rule. That rule serves as the definition of the
allowed successor for that name. The definition must appear before any uses of
the name on the left-hand side of a rule. (That is, the rules themselves must be
ordered according to the partial order, for easier reading by people.)

Negative assertions double-check the partial order:

    i !< j

means that it must NOT be the case that i < j. Negative assertions may appear
anywhere in the rules, even before i and j have been defined.

Comments begin with #.

TYPES

type Graph struct {
	Nodes []string

	// Has unexported fields.
}

func Parse(dag string) (*Graph, error)
    Parse parses the DAG language and returns the transitive closure of the
    described graph. In the returned graph, there is an edge from "b" to "a" if
    b < a (or a > b) in the partial order.

func (g *Graph) AddEdge(from, to string)

func (g *Graph) DelEdge(from, to string)

func (g *Graph) Edges(from string) []string

func (g *Graph) HasEdge(from, to string) bool

func (g *Graph) Topo() []string
    Topo returns a topological sort of g. This function is deterministic.

func (g *Graph) TransitiveReduction()
    TransitiveReduction removes edges from g that are transitively reachable.
    g must be transitively closed.

func (g *Graph) Transpose()
    Transpose reverses all edges in g.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
