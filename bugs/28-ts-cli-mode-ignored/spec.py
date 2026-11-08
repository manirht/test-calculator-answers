BUG = dict(
    id="28", slug="ts-cli-mode-ignored", title="calc-ui --mode is ignored",
    lang="ts", also=["rust"], tier="L2", category="cli", kind="fix", suites=["rust", "ts"],
    commit_message="refactor: apply CLI settings in one place",
    issue=r'''
```
$ calc eval 2/3 --places 2 --mode truncate
0.66
$ calc-ui --places 2 --mode truncate 2/3
0.67
```

The engine's own CLI honours `--mode`. `calc-ui` accepts the flag (a typo in it is reported) and `--places` works, but the result is
still rounded half-up. Typing `:mode truncate` inside an interactive session works, so the REPL itself is fine.
''',
    answer=dict(
        culprit="ts/src/cli.ts::main",
        mechanism="The line that copies `args.mode` into the REPL settings (`if (args.mode !== undefined) settings.mode = args.mode;`) was removed. `--places` is still applied, so the flag looks half-working.",
        fix="Restore `if (args.mode !== undefined) settings.mode = args.mode;` next to the places line.",
        grading="TypeScript-only; hidden test runs the built CLI. Expected clean stop under current LYRA.",
    ),
    expected={"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "TypeScript-only bug"},
    edits=[("ts/src/cli.ts", "  if (args.mode !== undefined) settings.mode = args.mode;\n", "")],
    hidden={"ts/src/test/hidden_28.test.ts": r'''import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const binary = process.env.CALC_BIN ?? join(here, "..", "..", "..", "target", "debug", "calc");
const cli = join(here, "..", "cli.js");

test("--mode reaches the engine", () => {
  assert.ok(existsSync(binary), `build the engine first: ${binary}`);
  const run = (...flags: string[]) =>
    spawnSync(process.execPath, [cli, "--bin", binary, "--places", "2", ...flags, "2/3"], { encoding: "utf8" }).stdout.trim();
  assert.equal(run("--mode", "truncate"), "0.66");
  assert.equal(run("--mode", "half-up"), "0.67");
  assert.equal(run(), "0.67");
});
'''},
    run="cd ts && npm run build && node --test dist/test/hidden_28.test.js",
)
