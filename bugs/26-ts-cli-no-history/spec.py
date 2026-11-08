BUG = dict(
    id="26", slug="ts-cli-no-history", title="--no-history still writes the history file",
    lang="ts", also=["rust"], tier="L2", category="cli", kind="fix", suites=["rust", "ts"],
    commit_message="refactor: always flush history when the session ends",
    issue=r'''
I use `calc-ui --no-history` when I'm calculating things I'd rather not keep (salaries, mostly):

```
$ echo "85000 / 12
:quit" | calc-ui --no-history
7083.3333333333
$ cat .calc_history.json
[
  {
    "expr": "85000 / 12",
    ...
```

The flag clearly prevents history from being *read* at start (my old entries don't come back) but the new entries are still
saved at the end of the session. The help text says "do not read or write history".
''',
    answer=dict(
        culprit="ts/src/cli.ts::main",
        mechanism="The guard around `saveHistory` (`if (!args.noHistory)`) was removed, so history is written whenever an interactive session ends, regardless of `--no-history`.",
        fix="`if (!args.noHistory) saveHistory(historyFile, history);`",
        grading="TypeScript-only. The hidden test runs the built CLI with a piped stdin and checks that the file does or does not appear.",
    ),
    expected={"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "TypeScript-only bug"},
    edits=[("ts/src/cli.ts", "    if (!args.noHistory) saveHistory(historyFile, history);", "    saveHistory(historyFile, history);")],
    hidden={"ts/src/test/hidden_26.test.ts": r'''import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const binary = process.env.CALC_BIN ?? join(here, "..", "..", "..", "target", "debug", "calc");
const cli = join(here, "..", "cli.js");

function session(flags: string[]): string {
  const dir = mkdtempSync(join(tmpdir(), "calc-hidden-26-"));
  const file = join(dir, "history.json");
  const result = spawnSync(process.execPath, [cli, "--bin", binary, "--history-file", file, ...flags], {
    input: "85000 / 12\n:quit\n",
    encoding: "utf8",
  });
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /7083\.3333333333/);
  return file;
}

test("--no-history neither reads nor writes the history file", () => {
  assert.ok(existsSync(binary), `build the engine first: ${binary}`);
  assert.equal(existsSync(session(["--no-history"])), false);
  assert.equal(existsSync(session([])), true);
});
'''},
    run="cd ts && npm run build && node --test dist/test/hidden_26.test.js",
)
