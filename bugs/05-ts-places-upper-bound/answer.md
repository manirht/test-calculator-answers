# 05 A too-large --places is accepted, then every expression fails

- language: ts
- tier: L1   category: cli-args   kind: fix
- expected outcome: {"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "TypeScript-only bug"}
- culprit: `ts/src/args.ts::parseArgs (--places case)`

## Root cause

The upper bound check (`places > MAX_PLACES`) and its constant were removed. The engine still enforces 30 per request, so the failure shows up later and on every line.

## Reference fix

Restore `const MAX_PLACES = 30;` and `if (places > MAX_PLACES) return { ...args, error: `--places must be at most ${MAX_PLACES}` };` after the integer check.

## How to grade

TypeScript-only. Expected clean stop under current LYRA. A correct RCA explains why the symptom appears in the engine (BAD_REQUEST) while the cause is in argument parsing.

## Hidden test

Files: `ts/src/test/hidden_05.test.ts`

```sh
cd ts && npm run build && node --test dist/test/hidden_05.test.js
```
