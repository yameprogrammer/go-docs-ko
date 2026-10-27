# package math/big/internal/asmgen

- 원문: <https://pkg.go.dev/math/big/internal/asmgen>
- 분류: Go 표준 라이브러리

## 한국어 요약

Asmgen은 수학/빅 어셈블리 코드를 생성합니다.

## 원문 요약

Asmgen generates math/big assembly.

## API 상세 (go doc -all)

~~~text
package asmgen // import "math/big/internal/asmgen"

Asmgen generates math/big assembly.

Usage:

    cd go/src/math/big
    go test ./internal/asmgen -generate

Or:

    go generate math/big

VARIABLES

var Arch386 = &Arch{
	Name:      "386",
	WordBits:  32,
	WordBytes: 4,

	regs: []string{
		"BX", "SI", "DI", "BP",
		"CX", "DX", "AX",
	},
	op3:              x86Op3,
	hint:             x86Hint,
	memOK:            true,
	subCarryIsBorrow: true,
	maxColumns:       1,

	memIndex: _386MemIndex,

	mov:      "MOVL",
	adds:     "ADDL",
	adcs:     "ADCL",
	subs:     "SUBL",
	sbcs:     "SBBL",
	lsh:      "SHLL",
	lshd:     "SHLL",
	rsh:      "SHRL",
	rshd:     "SHRL",
	and:      "ANDL",
	or:       "ORL",
	xor:      "XORL",
	neg:      "NEGL",
	lea:      "LEAL",
	mulWideF: x86MulWide,

	addWords: "LEAL (%[2]s)(%[1]s*4), %[3]s",

	jmpZero:       "TESTL %[1]s, %[1]s; JZ %[2]s",
	jmpNonZero:    "TESTL %[1]s, %[1]s; JNZ %[2]s",
	loopBottom:    "SUBL $1, %[1]s; JNZ %[2]s",
	loopBottomNeg: "ADDL $1, %[1]s; JNZ %[2]s",
}
var ArchAMD64 = &Arch{
	Name:      "amd64",
	WordBits:  64,
	WordBytes: 8,

	regs: []string{
		"BX", "SI", "DI",
		"R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15",
		"AX", "DX", "CX",
	},
	op3:              x86Op3,
	hint:             x86Hint,
	memOK:            true,
	subCarryIsBorrow: true,

	options: map[Option]func(*Asm, string){
		OptionAltCarry: amd64JmpADX,
	},

	mov:      "MOVQ",
	adds:     "ADDQ",
	adcs:     "ADCQ",
	subs:     "SUBQ",
	sbcs:     "SBBQ",
	lsh:      "SHLQ",
	lshd:     "SHLQ",
	rsh:      "SHRQ",
	rshd:     "SHRQ",
	and:      "ANDQ",
	or:       "ORQ",
	xor:      "XORQ",
	neg:      "NEGQ",
	lea:      "LEAQ",
	addF:     amd64Add,
	mulWideF: x86MulWide,

	addWords: "LEAQ (%[2]s)(%[1]s*8), %[3]s",

	jmpZero:       "TESTQ %[1]s, %[1]s; JZ %[2]s",
	jmpNonZero:    "TESTQ %[1]s, %[1]s; JNZ %[2]s",
	loopBottom:    "SUBQ $1, %[1]s; JNZ %[2]s",
	loopBottomNeg: "ADDQ $1, %[1]s; JNZ %[2]s",
}
var ArchARM = &Arch{
	Name:          "arm",
	WordBits:      32,
	WordBytes:     4,
	CarrySafeLoop: true,

	regs: []string{

		"R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R11", "R12",
	},
	regShift: true,

	mov:  "MOVW",
	add:  "ADD",
	adds: "ADD.S",
	adc:  "ADC",
	adcs: "ADC.S",
	sub:  "SUB",
	subs: "SUB.S",
	sbc:  "SBC",
	sbcs: "SBC.S",
	rsb:  "RSB",
	and:  "AND",
	or:   "ORR",
	xor:  "EOR",

	mulWideF: armMulWide,

	addWords: "ADD %s<<2, %s, %s",

	jmpZero:    "TEQ $0, %s; BEQ %s",
	jmpNonZero: "TEQ $0, %s; BNE %s",

	loadIncN:  armLoadIncN,
	loadDecN:  armLoadDecN,
	storeIncN: armStoreIncN,
	storeDecN: armStoreDecN,
}
var ArchARM64 = &Arch{
	Name:          "arm64",
	WordBits:      64,
	WordBytes:     8,
	CarrySafeLoop: true,

	regs: []string{

		"R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9",
		"R10", "R11", "R12", "R13", "R14", "R15", "R16", "R17", "R19",
		"R20", "R21", "R22", "R23", "R24", "R25", "R26",
	},
	reg0: "ZR",

	mov:   "MOVD",
	add:   "ADD",
	adds:  "ADDS",
	adc:   "ADC",
	adcs:  "ADCS",
	sub:   "SUB",
	subs:  "SUBS",
	sbc:   "SBC",
	sbcs:  "SBCS",
	mul:   "MUL",
	mulhi: "UMULH",
	lsh:   "LSL",
	rsh:   "LSR",
	and:   "AND",
	or:    "ORR",
	xor:   "EOR",

	addWords: "ADD %[1]s<<3, %[2]s, %[3]s",

	jmpZero:    "CBZ %s, %s",
	jmpNonZero: "CBNZ %s, %s",

	loadIncN:  arm64LoadIncN,
	loadDecN:  arm64LoadDecN,
	storeIncN: arm64StoreIncN,
	storeDecN: arm64StoreDecN,
}
var ArchLoong64 = &Arch{
	Name:          "loong64",
	WordBits:      64,
	WordBytes:     8,
	CarrySafeLoop: true,

	regs: []string{

		"R4", "R5", "R6", "R7", "R8", "R9",
		"R10", "R11", "R12", "R13", "R14", "R15", "R16", "R17", "R18", "R19",
		"R20", "R21", "R23", "R24", "R25", "R26", "R27",
		"R31",
	},
	reg0:        "R0",
	regCarry:    "R28",
	regAltCarry: "R29",
	regTmp:      "R30",

	mov:   "MOVV",
	add:   "ADDVU",
	sub:   "SUBVU",
	sltu:  "SGTU",
	mul:   "MULV",
	mulhi: "MULHVU",
	lsh:   "SLLV",
	rsh:   "SRLV",
	and:   "AND",
	or:    "OR",
	xor:   "XOR",

	addWords: "ALSLV $3, %[1]s, %[2]s, %[3]s",

	jmpZero:    "BEQ %s, %s",
	jmpNonZero: "BNE %s, %s",
}
var ArchMIPS = &Arch{
	Name:          "mipsx",
	Build:         "mips || mipsle",
	WordBits:      32,
	WordBytes:     4,
	CarrySafeLoop: true,

	regs: []string{

		"R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9",
		"R10", "R11", "R12", "R13", "R14", "R15", "R16", "R17", "R18", "R19",
		"R20", "R21", "R22", "R24", "R25",
	},
	reg0:        "R0",
	regTmp:      "R23",
	regCarry:    "R24",
	regAltCarry: "R25",

	mov:      "MOVW",
	add:      "ADDU",
	sltu:     "SGTU",
	sub:      "SUBU",
	mulWideF: mipsMulWide,
	lsh:      "SLL",
	rsh:      "SRL",
	and:      "AND",
	or:       "OR",
	xor:      "XOR",

	jmpZero:    "BEQ %s, %s",
	jmpNonZero: "BNE %s, %s",
}
var ArchMIPS64x = &Arch{
	Name:          "mips64x",
	Build:         "mips64 || mips64le",
	WordBits:      64,
	WordBytes:     8,
	CarrySafeLoop: true,

	regs: []string{

		"R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9",
		"R10", "R11", "R12", "R13", "R14", "R15", "R16", "R17", "R18", "R19",
		"R20", "R21", "R22", "R24", "R25",
	},
	reg0:        "R0",
	regTmp:      "R23",
	regCarry:    "R24",
	regAltCarry: "R25",

	mov:      "MOVV",
	add:      "ADDVU",
	sltu:     "SGTU",
	sub:      "SUBVU",
	mulWideF: mips64MulWide,
	lsh:      "SLLV",
	rsh:      "SRLV",
	and:      "AND",
	or:       "OR",
	xor:      "XOR",

	jmpZero:    "BEQ %s, %s",
	jmpNonZero: "BNE %s, %s",
}
var ArchPPC64x = &Arch{
	Name:          "ppc64x",
	Build:         "ppc64 || ppc64le",
	WordBits:      64,
	WordBytes:     8,
	CarrySafeLoop: true,

	regs: []string{

		"R3", "R4", "R5", "R6", "R7", "R8", "R9",
		"R10", "R11", "R12", "R14", "R15", "R16", "R17", "R18", "R19",
		"R20", "R21", "R22", "R23", "R24", "R25", "R26", "R27", "R28", "R29",
	},
	reg0:   "R0",
	regTmp: "R31",

	mov:   "MOVD",
	add:   "ADD",
	adds:  "ADDC",
	adcs:  "ADDE",
	sub:   "SUB",
	subs:  "SUBC",
	sbcs:  "SUBE",
	mul:   "MULLD",
	mulhi: "MULHDU",
	lsh:   "SLD",
	rsh:   "SRD",
	and:   "ANDCC",
	or:    "OR",
	xor:   "XOR",

	jmpZero:    "CMP %[1]s, $0; BEQ %[2]s",
	jmpNonZero: "CMP %s, $0; BNE %s",

	loopTop:    "CMP %[1]s, $0; BEQ %[2]s; MOVD %[1]s, CTR",
	loopBottom: "BDNZ %[2]s",
}
var ArchRISCV64 = &Arch{
	Name:          "riscv64",
	WordBits:      64,
	WordBytes:     8,
	CarrySafeLoop: true,

	regs: []string{

		"X5", "X6", "X7", "X8", "X9",
		"X10", "X11", "X12", "X13", "X14", "X15", "X16", "X17", "X18", "X19",
		"X20", "X21", "X22", "X23", "X24", "X25", "X26",
		"X30",
	},

	reg0:        "X0",
	regCarry:    "X28",
	regAltCarry: "X29",
	regTmp:      "X31",

	mov:   "MOV",
	add:   "ADD",
	sub:   "SUB",
	mul:   "MUL",
	mulhi: "MULHU",
	lsh:   "SLL",
	rsh:   "SRL",
	and:   "AND",
	or:    "OR",
	xor:   "XOR",
	sltu:  "SLTU",

	jmpZero:    "BEQZ %s, %s",
	jmpNonZero: "BNEZ %s, %s",
}
var ArchS390X = &Arch{
	Name:          "s390x",
	WordBits:      64,
	WordBytes:     8,
	CarrySafeLoop: true,

	regs: []string{

		"R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9",
		"R10", "R11", "R12",
	},
	reg0:       "R0",
	regTmp:     "R10",
	setup:      s390xSetup,
	maxColumns: 2,
	op3:        s390xOp3,
	hint:       s390xHint,

	mov:      "MOVD",
	adds:     "ADDC",
	adcs:     "ADDE",
	subs:     "SUBC",
	sbcs:     "SUBE",
	mulWideF: s390MulWide,
	lsh:      "SLD",
	rsh:      "SRD",
	and:      "AND",
	or:       "OR",
	xor:      "XOR",
	neg:      "NEG",
	lea:      "LAY",

	jmpZero:    "CMPBEQ %s, $0, %s",
	jmpNonZero: "CMPBNE %s, $0, %s",
}

TYPES

type Arch struct {
	Name          string // name of architecture
	Build         string // build tag
	WordBits      int    // length of word in bits (32 or 64)
	WordBytes     int    // length of word in bytes (4 or 8)
	CarrySafeLoop bool   // whether loops preserve carry flag across iterations

	// Has unexported fields.
}
    An Arch defines how to generate assembly for a specific architecture.

func (a *Arch) HasShiftWide() bool
    HasShiftWide reports whether the Arch has working LshWide/RshWide
    instructions. If not, calling them will panic.

type Asm struct {
	Arch *Arch // architecture

	// Has unexported fields.
}
    An Asm is an assembly file being written.

func NewAsm(arch *Arch) *Asm
    NewAsm returns a new Asm preparing assembly for the given architecture to be
    written to file.

func (a *Asm) Add(src1, src2, dst Reg, carry Carry)
    Add emits dst = src1+src2, with the specified carry behavior.

func (a *Asm) AddWords(src1 Reg, src2, dst RegPtr)
    AddWords emits dst = src1*WordBytes + src2. It does not set or use the carry
    flag.

func (a *Asm) AltCarry() Reg
    AltCarry returns the secondary carry register, or else the zero Reg.

func (a *Asm) And(src1, src2, dst Reg)
    And emits dst = src1 & src2 It may modify the carry flag.

func (a *Asm) Carry() Reg
    Carry returns the carry register, or else the zero Reg.

func (a *Asm) ClearCarry(which Carry)
    ClearCarry clears the carry flag. The ‘which’ parameter must be AddCarry
    or SubCarry to specify how the flag will be used. (On some systems, the sub
    carry's actual processor bit is inverted from its usual value.)

func (a *Asm) Comment(format string, args ...any)
    Comment emits a line comment to the assembly output.

func (a *Asm) ConvertCarry(which Carry, dst Reg)
    ConvertCarry converts the carry flag in dst from the internal format to a 0
    or 1. The carry flag is left in an undefined state.

func (a *Asm) EOL(format string, args ...any)
    EOL appends an end-of-line comment to the previous line.

func (a *Asm) Enabled(option Option) bool
    Enabled reports whether the optional CPU feature is considered to be enabled
    at this point in the assembly output.

func (a *Asm) Fatalf(format string, args ...any)
    Fatalf reports a fatal error by panicking. Panicking is appropriate because
    there is a bug in the generator, and panicking will show the exact source
    lines leading to that bug.

func (a *Asm) Free(r Reg)
    Free frees a previously allocated register. If r is not a register (if it's
    an immediate or a memory reference), Free is a no-op.

func (a *Asm) FreeAll()
    FreeAll frees all known registers.

func (a *Asm) Func(decl string) *Func
    Func starts a new function in the assembly output.

func (a *Asm) HasRegShift() bool
    HasRegShift reports whether the architecture can use shift expressions as
    operands.

func (a *Asm) Imm(x int) Reg
    Imm returns a Reg representing an immediate (constant) value.

func (a *Asm) IsZero(r Reg) bool
    IsZero reports whether r is a zero immediate or the zero register.

func (a *Asm) Jmp(label string)
    Jmp jumps to the label.

func (a *Asm) JmpEnable(option Option, label string) bool
    JmpEnable emits a test for the optional CPU feature that jumps to label
    if the feature is present. If JmpEnable returns false, the feature is not
    available on this architecture and no code was emitted.

func (a *Asm) JmpNonZero(src Reg, label string)
    JmpNonZero jumps to the label if src is non-zero. It may modify the carry
    flag unless a.Arch,CarrySafeLoop is true.

func (a *Asm) JmpZero(src Reg, label string)
    JmpZero jumps to the label if src is zero. It may modify the carry flag
    unless a.Arch.CarrySafeLoop is true.

func (a *Asm) Label(name string)
    Label emits a label with the given name.

func (a *Asm) Lsh(shift, src, dst Reg)
    Lsh emits dst = src << shift. It may modify the carry flag.

func (a *Asm) LshReg(shift, src Reg) Reg
    LshReg returns a shift-expression operand src<<shift. If a.HasRegShift() ==
    false, LshReg panics.

func (a *Asm) LshWide(shift, adj, src, dst Reg)
    LshWide emits dst = src << shift with low bits shifted from adj. It may
    modify the carry flag.

func (a *Asm) Mov(src, dst Reg)
    Mov emits dst = src.

func (a *Asm) MulWide(src1, src2, dstlo, dsthi Reg)
    MulWide emits dstlo = src1 * src2 and dsthi = (src1 * src2) >> WordBits. The
    carry flag is left in an undefined state. If dstlo or dsthi is the zero Reg,
    then those outputs are discarded.

func (a *Asm) Neg(src, dst Reg)
    Neg emits dst = -src. It may modify the carry flag.

func (a *Asm) Or(src1, src2, dst Reg)
    Or emits dst = src1 | src2 It may modify the carry flag.

func (a *Asm) Printf(format string, args ...any)
    Printf emits to the assembly output.

func (a *Asm) Reg() Reg
    Reg allocates a new register.

func (a *Asm) RegHint(hint Hint) Reg
    RegHint allocates a new register, with a hint as to its purpose.

func (a *Asm) RegsUsed() RegsUsed
    RegsUsed returns a snapshot of which registers are currently allocated,
    which can be passed to a future call to Asm.SetRegsUsed.

func (a *Asm) RestoreCarry(src Reg)
    RestoreCarry restores the carry flag from src. src is left in an undefined
    state.

func (a *Asm) Ret()
    Ret returns.

func (a *Asm) Rsh(shift, src, dst Reg)
    Rsh emits dst = src >> shift. It may modify the carry flag.

func (a *Asm) RshReg(shift, src Reg) Reg
    RshReg returns a shift-expression operand src>>shift. If a.HasRegShift() ==
    false, RshReg panics.

func (a *Asm) RshWide(shift, adj, src, dst Reg)
    RshWide emits dst = src >> shift with high bits shifted from adj. It may
    modify the carry flag.

func (a *Asm) SLTU(src1, src2, dst Reg)
    SLTU emits dst = src2 < src1 (0 or 1), using an unsigned comparison.

func (a *Asm) SaveCarry(dst Reg)
    SaveCarry saves the carry flag into dst. The meaning of the bits in dst is
    architecture-dependent. The carry flag is left in an undefined state.

func (a *Asm) SaveConvertCarry(which Carry, dst Reg)
    SaveConvertCarry saves and converts the carry flag into dst: 0 unset, 1 set.
    The carry flag is left in an undefined state.

func (a *Asm) SetOption(option Option, on bool)
    SetOption changes whether the optional CPU feature should be considered to
    be enabled.

func (a *Asm) SetRegsUsed(used RegsUsed)
    SetRegsUsed sets which registers are currently allocated. The argument
    should have been returned from a previous call to Asm.RegsUsed.

func (a *Asm) Sub(src1, src2, dst Reg, carry Carry)
    Sub emits dst = src2-src1, with the specified carry behavior.

func (a *Asm) Unfree(r Reg)
    Unfree reallocates a previously freed register r. If r is not a register
    (if it's an immediate or a memory reference), Unfree is a no-op. If r is not
    free for allocation, Unfree panics. A Free paired with Unfree can release
    a register for use temporarily but then reclaim it, such as at the end of a
    loop body when it must be restored.

func (a *Asm) Xor(src1, src2, dst Reg)
    Xor emits dst = src1 ^ src2 It may modify the carry flag.

func (a *Asm) ZR() Reg
    ZR returns the zero register (the specific register guaranteed to hold the
    integer 0), or else the zero Reg (Reg{}, which has r.Valid() == false).

type Carry uint
    A Carry is a flag field explaining how an instruction sets and uses the
    carry flags. Different operations expect different sets of bits. Add and
    Sub expect: UseCarry or 0, SetCarry, KeepCarry, or SmashCarry; and AltCarry
    or 0. ClearCarry, SaveCarry, and ConvertCarry expect: AddCarry or SubCarry;
    and AltCarry or 0.

const (
	SetCarry   Carry = 1 << iota // sets carry
	UseCarry                     // uses carry
	KeepCarry                    // must preserve carry
	SmashCarry                   // can modify carry or not, whatever is easiest

	AltCarry // use the secondary carry flag
	AddCarry // use add carry flag semantics (for ClearCarry, ConvertCarry)
	SubCarry // use sub carry flag semantics (for ClearCarry, ConvertCarry)
)
type Func struct {
	Name string
	Asm  *Asm

	// Has unexported fields.
}
    A Func represents a single assembly function.

func (f *Func) Arg(name string) Reg
    Arg allocates a new register, copies the named argument (or result) into it,
    and returns that register.

func (f *Func) ArgHint(name string, hint Hint) Reg
    ArgHint is like Arg but uses a register allocation hint.

func (f *Func) ArgPtr(name string) RegPtr
    ArgPtr is like Arg but returns a RegPtr.

func (f *Func) Pipe() *Pipe
    Pipe creates and returns a new pipe for use in the function f.

func (f *Func) StoreArg(src Reg, name string)
    StoreArg stores src into the named argument (or result).

type Hint uint
    A Hint is a hint about what a register will be used for, so that an
    appropriate one can be selected.

const (
	HintNone       Hint = iota
	HintShiftCount      // shift count (CX on x86)
	HintMulSrc          // mul source operand (AX on x86)
	HintMulHi           // wide mul high output (DX on x86)
	HintMemOK           // a memory reference is okay
	HintCarry           // carry flag
	HintAltCarry        // secondary carry flag
)
type Option int
    An Option denotes an optional CPU feature that can be tested at runtime.

const (

	// OptionAltCarry checks whether there is an add instruction
	// that uses a secondary carry flag, so that two different sums
	// can be accumulated in parallel with independent carry flags.
	// Some architectures (MIPS, Loong64, RISC-V) provide this
	// functionality natively, indicated by asm.Carry().Valid() being true.
	OptionAltCarry Option
)
type Pipe struct {
	// Has unexported fields.
}
    A Pipe manages the input and output data pipelines for a function's memory
    operations.

    The input is one or more equal-length slices of words, so collectively it
    can be viewed as a matrix, in which each slice is a row and each column is
    a set of corresponding words from the different slices. The output can be
    viewed the same way, although it is often just one row.

func (p *Pipe) AtUnrollEnd(end func())
    AtUnrollEnd sets a function to call at the end of an unrolled sequence.
    See Pipe.Loop for details.

func (p *Pipe) AtUnrollStart(start func())
    AtUnrollStart sets a function to call at the start of an unrolled sequence.
    See Pipe.Loop for details.

func (p *Pipe) Done()
    Done frees all the registers allocated by the pipe.

func (p *Pipe) DropInput(name string)
    DropInput deletes the named input from the pipe, usually because it has been
    exhausted. (This is not used yet but will be used in a future generator.)

func (p *Pipe) LoadN(n int) [][]Reg
    LoadN returns the next n columns of input words as a slice of rows.
    Regs for inputs that have been marked using p.SetMemOK will be direct memory
    references. Regs for other inputs will be newly allocated registers and must
    be freed.

func (p *Pipe) LoadPtrs(n Reg)
    LoadPtrs loads the slice pointer arguments into registers, assuming that the
    slice length n has already been loaded into the register n.

    Start will call LoadPtrs if it has not been called already. LoadPtrs only
    needs to be called explicitly when code needs to use LoadN before Start,
    like when the shift.go generators read an initial word before the loop.

func (p *Pipe) Loop(block func(in, out [][]Reg))
    Loop emits code for the loop, calling block repeatedly to emit code
    that handles a block of N input columns (for arbitrary N = len(in[0])
    chosen by p). block must call p.StoreN(out) to write N output columns.
    The out slice is a pre-allocated matrix of uninitialized Reg values.
    block is expected to set each entry to the Reg that should be written before
    calling p.StoreN(out).

    For example, if the loop is to be unrolled 4x in blocks of 2 columns each,
    the sequence of calls to emit the unrolled loop body is:

        start()  // set by pAtUnrollStart
        ... reads for 2 columns ...
        block()
        ... writes for 2 columns ...
        ... reads for 2 columns ...
        block()
        ... writes for 2 columns ...
        end()  // set by p.AtUnrollEnd

    Any registers allocated during block are freed automatically when block
    returns.

func (p *Pipe) Restart(n Reg, factors ...int)
    Restart prepares to loop over an additional n columns, beyond a previous
    loop run by p.Start/p.Loop.

func (p *Pipe) SetBackward()
    SetBackward sets the pipe to process the input and output columns in reverse
    order. This is needed for left shifts, which might otherwise overwrite data
    they will read later.

func (p *Pipe) SetHint(name string, hint Hint)
    SetHint records that the inputs from the named vector should be allocated
    with the given register hint.

    If the hint indicates a single register on the target architecture, then
    SetHint calls SetMaxColumns(1), since the hinted register can only be used
    for one value at a time.

func (p *Pipe) SetLabel(label string)
    SetLabel sets the label prefix for the loops emitted by the pipe. The
    default prefix is "loop".

func (p *Pipe) SetMaxColumns(m int)
    SetMaxColumns sets the maximum number of columns processed in a single loop
    body call.

func (p *Pipe) SetUseIndexCounter()
    SetUseIndexCounter sets the pipe to use an index counter if possible,
    meaning the loop counter is also used as an index for accessing the slice
    data. This clever trick is slower on modern processors, but it is still
    necessary on 386. On non-386 systems, SetUseIndexCounter is a no-op.

func (p *Pipe) Start(n Reg, factors ...int)
    Start prepares to loop over n columns. The factors give a sequence of
    unrolling factors to use, which must be either strictly increasing or
    strictly decreasing and must include 1. For example, 4, 1 means to process
    4 elements at a time and then 1 at a time for the final 0-3; specifying 1,4
    instead handles 0-3 elements first and then 4 at a time. Similarly, 32, 4,
    1 means to process 32 at a time, then 4 at a time, then 1 at a time.

    One benefit of using 1, 4 instead of 4, 1 is that the body processing 4 at a
    time needs more registers, and if it is the final body, the register holding
    the fragment count (0-3) has been freed and is available for use.

    Start may modify the carry flag.

    Start must be followed by a call to Loop1 or LoopN, but it is permitted to
    emit other instructions first, for example to set an initial carry flag.

func (p *Pipe) StoreN(regs [][]Reg)
    StoreN writes regs (a slice of rows) to the next n columns of output,
    where n = len(regs[0]).

type Reg struct {
	// Has unexported fields.
}
    A Reg is an allocated register or other assembly operand. (For example,
    a constant might have name "$123" and a memory reference might have name
    "0(R8)".)

func (r Reg) IsImm() bool
    IsImm reports whether r is an immediate value.

func (r Reg) IsMem() bool
    IsMem reports whether r is a memory value.

func (r Reg) String() string
    String returns the assembly syntax for r.

func (r Reg) Valid() bool
    Valid reports whether is valid, meaning r is not the zero value of Reg (a
    register with no name).

type RegPtr struct {
	// Has unexported fields.
}
    A RegPtr is like a Reg but expected to hold a pointer. The separate Go type
    helps keeps pointers and scalars separate and avoid mistakes; it is okay to
    convert to Reg as needed to use specific routines.

func (r RegPtr) String() string
    String returns the assembly syntax for r.

func (r RegPtr) Valid() bool
    Valid reports whether is valid, meaning r is not the zero value of RegPtr (a
    register with no name).

type RegsUsed struct {
	// Has unexported fields.
}
    A RegsUsed is a snapshot of which registers are allocated.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
