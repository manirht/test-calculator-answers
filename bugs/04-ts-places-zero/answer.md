# 04 calc-ui --places 0 is rejected

- language: ts
- tier: L1   category: cli-args   kind: fix
- expected outcome: {"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "TypeScript-only bug"}
- culprit: `ts/src/args.ts::parseArgs (--places case)`

## Root cause

The validation uses `places <= 0`, so the legal value 0 is reported as an error. The message says non-negative.

## Reference fix

Change the comparison back to `places < 0`.

## How to grade

TypeScript bug. Current LYRA cannot reproduce it with `cargo test`; the expected result is a clean stop (not reproduced / unsupported), not a fabricated Rust test. If a run supports TS profiles, the fix is the one-character change above.

## Hidden test

Files: `ts/src/test/hidden_04.test.ts`

```sh
cd ts && npm run build && node --test dist/test/hidden_04.test.js
```
