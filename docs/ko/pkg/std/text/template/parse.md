# package text/template/parse

- 원문: <https://pkg.go.dev/text/template/parse>
- 분류: Go 표준 라이브러리

## 한국어 요약

`parse` 패키지는 `text/template` 및 `html/template`에 정의된 템플릿의 파스 트리(parse tree)를 생성합니다.

## 원문 요약

Package parse builds parse trees for templates as defined by text/template and html/template.

## API 상세 (go doc -all)

~~~text
package parse // import "text/template/parse"

Package parse builds parse trees for templates as defined by text/template and
html/template. Clients should use those packages to construct templates rather
than this one, which provides shared internal data structures not intended for
general use.

FUNCTIONS

func IsEmptyTree(n Node) bool
    IsEmptyTree reports whether this tree (node) is empty of everything but
    space or comments.

func Parse(name, text, leftDelim, rightDelim string, funcs ...map[string]any) (map[string]*Tree, error)
    Parse returns a map from template name to Tree, created by parsing the
    templates described in the argument string. The top-level template will be
    given the specified name. If an error is encountered, parsing stops and an
    empty map is returned with the error.


TYPES

type ActionNode struct {
	NodeType
	Pos

	Line int       // The line number in the input. Deprecated: Kept for compatibility.
	Pipe *PipeNode // The pipeline in the action.
	// Has unexported fields.
}
    ActionNode holds an action (something bounded by delimiters). Control
    actions have their own nodes; ActionNode represents simple ones such as
    field evaluations and parenthesized pipelines.

func (a *ActionNode) Copy() Node

func (a *ActionNode) String() string

type BoolNode struct {
	NodeType
	Pos

	True bool // The value of the boolean constant.
	// Has unexported fields.
}
    BoolNode holds a boolean constant.

func (b *BoolNode) Copy() Node

func (b *BoolNode) String() string

type BranchNode struct {
	NodeType
	Pos

	Line     int       // The line number in the input. Deprecated: Kept for compatibility.
	Pipe     *PipeNode // The pipeline to be evaluated.
	List     *ListNode // What to execute if the value is non-empty.
	ElseList *ListNode // What to execute if the value is empty (nil if absent).
	// Has unexported fields.
}
    BranchNode is the common representation of if, range, and with.

func (b *BranchNode) Copy() Node

func (b *BranchNode) String() string

type BreakNode struct {
	NodeType
	Pos
	Line int
	// Has unexported fields.
}
    BreakNode represents a {{break}} action.

func (b *BreakNode) Copy() Node

func (b *BreakNode) String() string

type ChainNode struct {
	NodeType
	Pos

	Node  Node
	Field []string // The identifiers in lexical order.
	// Has unexported fields.
}
    ChainNode holds a term followed by a chain of field accesses (identifier
    starting with '.'). The names may be chained ('.x.y'). The periods are
    dropped from each ident.

func (c *ChainNode) Add(field string)
    Add adds the named field (which should start with a period) to the end of
    the chain.

func (c *ChainNode) Copy() Node

func (c *ChainNode) String() string

type CommandNode struct {
	NodeType
	Pos

	Args []Node // Arguments in lexical order: Identifier, field, or constant.
	// Has unexported fields.
}
    CommandNode holds a command (a pipeline inside an evaluating action).

func (c *CommandNode) Copy() Node

func (c *CommandNode) String() string

type CommentNode struct {
	NodeType
	Pos

	Text string // Comment text.
	// Has unexported fields.
}
    CommentNode holds a comment.

func (c *CommentNode) Copy() Node

func (c *CommentNode) String() string

type ContinueNode struct {
	NodeType
	Pos
	Line int
	// Has unexported fields.
}
    ContinueNode represents a {{continue}} action.

func (c *ContinueNode) Copy() Node

func (c *ContinueNode) String() string

type DotNode struct {
	NodeType
	Pos
	// Has unexported fields.
}
    DotNode holds the special identifier '.'.

func (d *DotNode) Copy() Node

func (d *DotNode) String() string

func (d *DotNode) Type() NodeType

type FieldNode struct {
	NodeType
	Pos

	Ident []string // The identifiers in lexical order.
	// Has unexported fields.
}
    FieldNode holds a field (identifier starting with '.'). The names may be
    chained ('.x.y'). The period is dropped from each ident.

func (f *FieldNode) Copy() Node

func (f *FieldNode) String() string

type IdentifierNode struct {
	NodeType
	Pos

	Ident string // The identifier's name.
	// Has unexported fields.
}
    IdentifierNode holds an identifier.

func NewIdentifier(ident string) *IdentifierNode
    NewIdentifier returns a new IdentifierNode with the given identifier name.

func (i *IdentifierNode) Copy() Node

func (i *IdentifierNode) SetPos(pos Pos) *IdentifierNode
    SetPos sets the position. NewIdentifier is a public method so we can't
    modify its signature. Chained for convenience. TODO: fix one day?

func (i *IdentifierNode) SetTree(t *Tree) *IdentifierNode
    SetTree sets the parent tree for the node. NewIdentifier is a public method
    so we can't modify its signature. Chained for convenience. TODO: fix one
    day?

func (i *IdentifierNode) String() string

type IfNode struct {
	BranchNode
}
    IfNode represents an {{if}} action and its commands.

func (i *IfNode) Copy() Node

type ListNode struct {
	NodeType
	Pos

	Nodes []Node // The element nodes in lexical order.
	// Has unexported fields.
}
    ListNode holds a sequence of nodes.

func (l *ListNode) Copy() Node

func (l *ListNode) CopyList() *ListNode

func (l *ListNode) String() string

type Mode uint
    A Mode value is a set of flags (or 0). Modes control parser behavior.

const (
	ParseComments Mode = 1 << iota // parse comments and add them to AST
	SkipFuncCheck                  // do not check that functions are defined
)
type NilNode struct {
	NodeType
	Pos
	// Has unexported fields.
}
    NilNode holds the special identifier 'nil' representing an untyped nil
    constant.

func (n *NilNode) Copy() Node

func (n *NilNode) String() string

func (n *NilNode) Type() NodeType

type Node interface {
	Type() NodeType
	String() string
	// Copy does a deep copy of the Node and all its components.
	// To avoid type assertions, some XxxNodes also have specialized
	// CopyXxx methods that return *XxxNode.
	Copy() Node
	Position() Pos // byte position of start of node in full original input string

	// Has unexported methods.
}
    A Node is an element in the parse tree. The interface is trivial.
    The interface contains an unexported method so that only types local to this
    package can satisfy it.

type NodeType int
    NodeType identifies the type of a parse tree node.

const (
	NodeText    NodeType = iota // Plain text.
	NodeAction                  // A non-control action such as a field evaluation.
	NodeBool                    // A boolean constant.
	NodeChain                   // A sequence of field accesses.
	NodeCommand                 // An element of a pipeline.
	NodeDot                     // The cursor, dot.

	NodeField      // A field or method name.
	NodeIdentifier // An identifier; always a function name.
	NodeIf         // An if action.
	NodeList       // A list of Nodes.
	NodeNil        // An untyped nil constant.
	NodeNumber     // A numerical constant.
	NodePipe       // A pipeline of commands.
	NodeRange      // A range action.
	NodeString     // A string constant.
	NodeTemplate   // A template invocation action.
	NodeVariable   // A $ variable.
	NodeWith       // A with action.
	NodeComment    // A comment.
	NodeBreak      // A break action.
	NodeContinue   // A continue action.
)
func (t NodeType) Type() NodeType
    Type returns itself and provides an easy default implementation for
    embedding in a Node. Embedded in all non-trivial Nodes.

type NumberNode struct {
	NodeType
	Pos

	IsInt      bool       // Number has an integral value.
	IsUint     bool       // Number has an unsigned integral value.
	IsFloat    bool       // Number has a floating-point value.
	IsComplex  bool       // Number is complex.
	Int64      int64      // The signed integer value.
	Uint64     uint64     // The unsigned integer value.
	Float64    float64    // The floating-point value.
	Complex128 complex128 // The complex value.
	Text       string     // The original textual representation from the input.
	// Has unexported fields.
}
    NumberNode holds a number: signed or unsigned integer, float, or complex.
    The value is parsed and stored under all the types that can represent the
    value. This simulates in a small amount of code the behavior of Go's ideal
    constants.

func (n *NumberNode) Copy() Node

func (n *NumberNode) String() string

type PipeNode struct {
	NodeType
	Pos

	Line     int             // The line number in the input. Deprecated: Kept for compatibility.
	IsAssign bool            // The variables are being assigned, not declared.
	Decl     []*VariableNode // Variables in lexical order.
	Cmds     []*CommandNode  // The commands in lexical order.
	// Has unexported fields.
}
    PipeNode holds a pipeline with optional declaration

func (p *PipeNode) Copy() Node

func (p *PipeNode) CopyPipe() *PipeNode

func (p *PipeNode) String() string

type Pos int
    Pos represents a byte position in the original input text from which this
    template was parsed.

func (p Pos) Position() Pos

type RangeNode struct {
	BranchNode
}
    RangeNode represents a {{range}} action and its commands.

func (r *RangeNode) Copy() Node

type StringNode struct {
	NodeType
	Pos

	Quoted string // The original text of the string, with quotes.
	Text   string // The string, after quote processing.
	// Has unexported fields.
}
    StringNode holds a string constant. The value has been "unquoted".

func (s *StringNode) Copy() Node

func (s *StringNode) String() string

type TemplateNode struct {
	NodeType
	Pos

	Line int       // The line number in the input. Deprecated: Kept for compatibility.
	Name string    // The name of the template (unquoted).
	Pipe *PipeNode // The command to evaluate as dot for the template.
	// Has unexported fields.
}
    TemplateNode represents a {{template}} action.

func (t *TemplateNode) Copy() Node

func (t *TemplateNode) String() string

type TextNode struct {
	NodeType
	Pos

	Text []byte // The text; may span newlines.
	// Has unexported fields.
}
    TextNode holds plain text.

func (t *TextNode) Copy() Node

func (t *TextNode) String() string

type Tree struct {
	Name      string    // name of the template represented by the tree.
	ParseName string    // name of the top-level template during parsing, for error messages.
	Root      *ListNode // top-level root of the tree.
	Mode      Mode      // parsing mode.

	// Has unexported fields.
}
    Tree is the representation of a single parsed template.

func New(name string, funcs ...map[string]any) *Tree
    New allocates a new parse tree with the given name.

func (t *Tree) Copy() *Tree
    Copy returns a copy of the Tree. Any parsing state is discarded.

func (t *Tree) ErrorContext(n Node) (location, context string)
    ErrorContext returns a textual representation of the location of the node
    in the input text. The receiver is only used when the node does not have a
    pointer to the tree inside, which can occur in old code.

func (t *Tree) Parse(text, leftDelim, rightDelim string, treeSet map[string]*Tree, funcs ...map[string]any) (tree *Tree, err error)
    Parse parses the template definition string to construct a representation
    of the template for execution. If either action delimiter string is empty,
    the default ("{{" or "}}") is used. Embedded template definitions are added
    to the treeSet map.

type VariableNode struct {
	NodeType
	Pos

	Ident []string // Variable name and fields in lexical order.
	// Has unexported fields.
}
    VariableNode holds a list of variable names, possibly with chained field
    accesses. The dollar sign is part of the (first) name.

func (v *VariableNode) Copy() Node

func (v *VariableNode) String() string

type WithNode struct {
	BranchNode
}
    WithNode represents a {{with}} action and its commands.

func (w *WithNode) Copy() Node
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
