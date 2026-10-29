# package internal/chacha8rand

- 원문: <https://pkg.go.dev/internal/chacha8rand>
- 분류: Go 표준 라이브러리

## 한국어 요약

Package chacha8rand implements a pseudorandom generator based on ChaCha8.

## 원문 요약

Package chacha8rand implements a pseudorandom generator based on ChaCha8.

## API 상세 (go doc -all)

~~~text
package chacha8rand // import "internal/chacha8rand"

Package chacha8rand implements a pseudorandom generator based on ChaCha8.
It is used by both runtime and math/rand/v2 and must have minimal dependencies.

ChaCha8 is ChaCha with 8 rounds. See
https://cr.yp.to/chacha/chacha-20080128.pdf.

ChaCha8 operates on a 4x4 matrix of uint32 values, initially set to:

    const1 const2 const3 const4
    seed   seed   seed   seed
    seed   seed   seed   seed
    counter64     0      0

We use the same constants as ChaCha20 does, a random seed, and a counter.
Running ChaCha8 on this input produces a 4x4 matrix of pseudo-random values with
as much entropy as the seed.

Given SIMD registers that can hold N uint32s, it is possible to run N ChaCha8
block transformations in parallel by filling the first register with the N
copies of const1, the second with N copies of const2, and so on, and then
running the operations.

Each iteration of ChaCha8Rand operates over 32 bytes of input and produces 992
bytes of RNG output, plus 32 bytes of input for the next iteration.

The 32 bytes of input are used as a ChaCha8 key, with a zero nonce, to produce
1024 bytes of output (16 blocks, with counters 0 to 15). First, for each block,
the values 0x61707865, 0x3320646e, 0x79622d32, 0x6b206574 are subtracted from
the 32-bit little-endian words at position 0, 1, 2, and 3 respectively, and an
increasing counter starting at zero is subtracted from each word at position 12.
Then, this stream is permuted such that for each sequence of four blocks,
first we output the first four bytes of each block, then the next four bytes
of each block, and so on. Finally, the last 32 bytes of output are used as the
input of the next iteration, and the remaining 992 bytes are the RNG output.

See https://c2sp.org/chacha8rand for additional details.

Normal ChaCha20 implementations for encryption use this same parallelism
but then have to deinterlace the results so that it appears the blocks were
generated separately. For the purposes of generating random numbers, the
interlacing is fine. We are simply locked in to preserving the 4-way interlacing
in any future optimizations.

FUNCTIONS

func Marshal(s *State) []byte
    Marshal marshals the state into a byte slice. Marshal and Unmarshal are
    functions, not methods, so that they will not be linked into the runtime
    when it uses the State struct, since the runtime does not need these.

func Unmarshal(s *State, data []byte) error
    Unmarshal unmarshals the state from a byte slice.


TYPES

type State struct {
	// Has unexported fields.
}
    A State holds the state for a single random generator. It must be used
    from one goroutine at a time. If used by multiple goroutines at a time,
    the goroutines may see the same random values, but the code will not crash
    or cause out-of-bounds memory accesses.

func (s *State) Init(seed [32]byte)
    Init seeds the State with the given seed value.

func (s *State) Init64(seed [4]uint64)
    Init64 seeds the state with the given seed value.

func (s *State) Next() (uint64, bool)
    Next returns the next random value, along with a boolean indicating whether
    one was available. If one is not available, the caller should call Refill
    and then repeat the call to Next.

    Next is //go:nosplit to allow its use in the runtime with per-m data without
    holding the per-m lock.

func (s *State) Refill()
    Refill refills the state with more random values. After a call to Refill,
    an immediate call to Next will succeed (unless multiple goroutines are
    incorrectly sharing a state).

func (s *State) Reseed()
    Reseed reseeds the state with new random values. After a call to Reseed,
    any previously returned random values have been erased from the memory of
    the state and cannot be recovered.
~~~

> 이 페이지는 비공식 한국어 미러 문서입니다. API의 권위 있는 원문은 pkg.go.dev 및 golang/go에 있습니다.
