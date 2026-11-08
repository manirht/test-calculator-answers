# 26 --no-history still writes the history file

- language: ts (also rust)
- tier: L2   category: cli   kind: fix
- expected outcome: {"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "TypeScript-only bug"}
- culprit: `ts/src/cli.ts::main`

## Root cause

The guard around `saveHistory` (`if (!args.noHistory)`) was removed, so history is written whenever an interactive session ends, regardless of `--no-history`.

## Reference fix

`if (!args.noHistory) saveHistory(historyFile, history);`

## How to grade

TypeScript-only. The hidden test runs the built CLI with a piped stdin and checks that the file does or does not appear.

## Hidden test

Files: `ts/src/test/hidden_26.test.ts`

```sh
cd ts && npm run build && node --test dist/test/hidden_26.test.js
```
