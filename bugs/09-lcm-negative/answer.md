# 09 lcm() returns a negative number when an argument is negative

- language: rust
- tier: L2   category: builtins   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-eval/src/builtins.rs::call ("lcm" arm)`

## Root cause

`lcm` computes `(a / g) * b` and the sign of the product follows the inputs. The `.abs()` on the result was dropped.

## Reference fix

Map the product through `v.abs()`: `.map(|v| Rational::from_int(v.abs()))`.

## How to grade

Fix must make all three sign combinations positive. A fix that only takes `abs` of the arguments is equivalent and acceptable.

## Hidden test

Files: `crates/calc-eval/tests/hidden_09.rs`

```sh
cargo test -p calc-eval --test hidden_09
```
