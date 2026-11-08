# 06 :history 0 says there is no history

- language: ts
- tier: L1   category: repl-commands   kind: fix
- expected outcome: {"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "TypeScript-only bug"}
- culprit: `ts/src/commands.ts::parseCommand (history case)`

## Root cause

The count check was loosened to `count < 0`, so 0 is accepted and `History.list(0)` returns an empty list, which the REPL reports as no history.

## Reference fix

Require `count < 1` to be an error.

## How to grade

TypeScript-only. Expected clean stop under current LYRA.

## Hidden test

Files: `ts/src/test/hidden_06.test.ts`

```sh
cd ts && npm run build && node --test dist/test/hidden_06.test.js
```
