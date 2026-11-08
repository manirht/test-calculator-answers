# 28 calc-ui --mode is ignored

- language: ts (also rust)
- tier: L2   category: cli   kind: fix
- expected outcome: {"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "TypeScript-only bug"}
- culprit: `ts/src/cli.ts::main`

## Root cause

The line that copies `args.mode` into the REPL settings (`if (args.mode !== undefined) settings.mode = args.mode;`) was removed. `--places` is still applied, so the flag looks half-working.

## Reference fix

Restore `if (args.mode !== undefined) settings.mode = args.mode;` next to the places line.

## How to grade

TypeScript-only; hidden test runs the built CLI. Expected clean stop under current LYRA.

## Hidden test

Files: `ts/src/test/hidden_28.test.ts`

```sh
cd ts && npm run build && node --test dist/test/hidden_28.test.js
```
