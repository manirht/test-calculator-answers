BUG = dict(
    id="12", slug="ts-cli-exit-code", title="calc-ui exits with status 0 when the expression fails",
    lang="ts", also=["rust"], tier="L2", category="cli", kind="fix", suites=["rust", "ts"],
    commit_message="refactor: simplify one-shot exit handling in the CLI",
    issue=r'''
In a script I rely on the exit status:

```
$ calc-ui "1/0"
error[DIV_BY_ZERO]: division by zero
$ echo $?
0
```

The error goes to stderr, which is right, but the status is `0`, so `calc-ui "1/0" || handle_error` never fires. The plain
`calc eval "1/0"` binary exits with `1` in the same situation. I expect `calc-ui` to do the same.
''',
    answer=dict(
        culprit="ts/src/cli.ts::main (one-shot branch)",
        mechanism="The one-shot branch computes `output.error ? 1 : 0` but the return was changed to a constant `0`.",
        fix="`return output.error ? 1 : 0;`.",
        grading="TypeScript-only; the hidden test runs the built CLI against the real engine binary. Expected clean stop under current LYRA.",
    ),
    expected={"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "TypeScript-only bug"},
    edits=[("ts/src/cli.ts", "      return output.error ? 1 : 0;", "      return 0;")],
    hidden={"ts/src/test/hidden_12.test.ts": r'''import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const binary = process.env.CALC_BIN ?? join(here, "..", "..", "..", "target", "debug", "calc");

test("a failing expression gives a non-zero exit status", () => {
  assert.ok(existsSync(binary), `build the engine first: ${binary}`);
  const cli = join(here, "..", "cli.js");
  const failed = spawnSync(process.execPath, [cli, "--bin", binary, "1/0"], { encoding: "utf8" });
  assert.equal(failed.status, 1);
  assert.match(failed.stderr, /DIV_BY_ZERO/);
  const fine = spawnSync(process.execPath, [cli, "--bin", binary, "1+1"], { encoding: "utf8" });
  assert.equal(fine.status, 0);
  assert.equal(fine.stdout.trim(), "2");
});
'''},
    run="cd ts && npm run build && node --test dist/test/hidden_12.test.js",
)
