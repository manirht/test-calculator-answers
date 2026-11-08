# 12 calc-ui exits with status 0 when the expression fails

- language: ts (also rust)
- tier: L2   category: cli   kind: fix
- expected outcome: {"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "TypeScript-only bug"}
- culprit: `ts/src/cli.ts::main (one-shot branch)`

## Root cause

The one-shot branch computes `output.error ? 1 : 0` but the return was changed to a constant `0`.

## Reference fix

`return output.error ? 1 : 0;`.

## How to grade

TypeScript-only; the hidden test runs the built CLI against the real engine binary. Expected clean stop under current LYRA.

## Hidden test

Files: `ts/src/test/hidden_12.test.ts`

```sh
cd ts && npm run build && node --test dist/test/hidden_12.test.js
```
