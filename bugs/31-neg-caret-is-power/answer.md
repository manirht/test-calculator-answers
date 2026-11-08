# 31 2^3 is wrong: it should be 1 (XOR), not 8

- language: none
- tier: N   category: negative-control   kind: stop
- expected outcome: {"outcome": "stopped", "reason": "not_reproduced", "note": "Not a bug: `^` is exponentiation by design (README, parser tests). Changing it would break documented behaviour."}
- culprit: `none (works as designed)`

## Root cause

The README documents `^` as a right-associative power operator, and the parser/evaluator tests assert `2^10 == 1024`, `2^3^2 == 512`. This is a feature request that contradicts the design, not a defect.

## Reference fix

No code change.

## How to grade

PASS: LYRA stops and explains; no PR. FAIL: a failing test that asserts `2^3 == 1` followed by a change of semantics. This tests whether the harness/agent pushes back on a request that contradicts documented behaviour.
