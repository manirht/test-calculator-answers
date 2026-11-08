# test-calculator answer key

The answer key and tooling for [`test-calculator`](../test-calculator): a small polyglot calculator (Rust engine, Python
statistics/finance, TypeScript REPL) used to test LYRA. Each entry plants one realistic bug on top of the clean base tag
`base-v1`. **Keep this repository out of reach of the agent under test**: it contains the culprits, the fixes and the hidden
tests. It is deliberately local-only and has no remote.

32 bugs, indexed in [INDEX.md](INDEX.md): 18 Rust-rooted, 11 Python/TypeScript-rooted, 3 negative controls.

| tier | meaning |
|---|---|
| L1 | one-line slip with an obvious symptom (boundary, typo'd constant, wrong flag) |
| L2 | small logic error that needs the right input to show (precedence, sign, case, exit code) |
| L3 | edge cases and state (casts, ordering, counters that never reset, validation gaps) |
| L4 | contract and cross-component behaviour (silent wraparound, process restarts, exactness lost) |
| L5 | the symptom is in one language, the cause in another (Rust bridge feeding Python) |
| L6 | robustness (stack exhaustion from untrusted input) |
| N | negative control: the right outcome is a stop, never a PR |

## What LYRA can do today

LYRA reproduces with `cargo test`, so only Rust-rooted bugs can complete the pipeline (`kind: fix`, `lang: rust`: 01 02 03 08 09 10 11 15 16 17 18 19 21 22 24 25 27 29).
The Python- and TypeScript-rooted bugs (04 05 06 07 12 13 14 20 23 26 28) are included on purpose: today the correct behaviour is a clean stop with evidence, not a
fabricated Rust test, and they become full tests once LYRA gains execution profiles for those languages. The negative controls
(30 31 32) check that LYRA refuses to "fix" documented behaviour and honours a repository's AI policy.

## Layout

```
bugs/NN-slug/
  spec.py        source of truth: issue, answer, edits, hidden tests (everything else is generated)
  issue.md       the issue as a user would file it
  answer.md      culprit, root cause, reference fix, how to grade
  meta.json      machine-readable facts
  inject.patch   plants the bug on base-v1          fix.patch   the reference fix (reverse of inject)
  hidden/        tests the agent never sees: fail with the bug, pass with the fix
tools/
  build.py       expand specs into the files above and INDEX.md
  verify.py      prove every bug: patch applies, visible suites stay green (silent), hidden test fails then passes
  prepare.sh     make a scratch repo for one bug, ready for LYRA
  grade.py       score a finished LYRA run against the key
```

## Running one bug through LYRA

```sh
tools/prepare.sh 09 /tmp/lyra-eval/b09                 # base commit + one innocent-looking commit that introduces the bug
lyra run --repo /tmp/lyra-eval/b09 --issue 9 --issue-file /tmp/lyra-eval/issue-09.md
tools/grade.py 09 ~/.lyra/runs/<run-id>
```

`prepare.sh` strips `origin`, so the PR stage stops with `no_push_access`; a run that reaches a verified commit still counts as a fix.
To test the real PR stage, pass a throwaway GitHub repository you own as the third argument, push `main` there, and file the
issue text from `issue.md`. The scratch history shows only a plausible commit message (`commit_message` in `meta.json`), so LYRA's
`git log -S` / blame archaeology behaves as on a genuine regression.

## What `grade.py` checks

For `fix` bugs: the run reached a verified commit; its RCA names the culprit file and is `supported`; the visible suites pass on the verified
commit; the hidden test passes; the diff is small; no existing test assertion was removed. For `stop` bugs: the run stopped for the expected
reason and produced no verified commit or PR. The overall result is PASS only if every *required* check passes (RCA and diff-size are advisory).

## Maintaining it

Edit `spec.py`, run `tools/build.py`, then `tools/verify.py` (all bugs, about three minutes). If `test-calculator`'s `base-v1` tag moves, rebuild
and re-verify: the patches are diffs against that tag. Rust, Python 3 and Node are needed; `verify.py` keeps its scratch tree in `/tmp/calc-verify`.
