BUG = dict(
    id="04", slug="ts-places-zero", title="calc-ui --places 0 is rejected",
    lang="ts", tier="L1", category="cli-args", kind="fix",
    commit_message="refactor: validate --places in parseArgs",
    issue=r'''
I want whole numbers only, so I run:

```
$ calc-ui --places 0 "10/4"
calc-ui: --places needs a non-negative integer
```

Zero is a non-negative integer, and `:places 0` inside the REPL works fine. `--places 1` through `--places 30` are accepted.
Expected output for the command above is `3` (half-up).
''',
    answer=dict(
        culprit="ts/src/args.ts::parseArgs (--places case)",
        mechanism="The validation uses `places <= 0`, so the legal value 0 is reported as an error. The message says non-negative.",
        fix="Change the comparison back to `places < 0`.",
        grading="TypeScript bug. Current LYRA cannot reproduce it with `cargo test`; the expected result is a clean stop (not reproduced / unsupported), not a fabricated Rust test. If a run supports TS profiles, the fix is the one-character change above.",
    ),
    expected={"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "TypeScript-only bug"},
    edits=[("ts/src/args.ts", "!Number.isInteger(places) || places < 0) {", "!Number.isInteger(places) || places <= 0) {")],
    hidden={"ts/src/test/hidden_04.test.ts": r'''import assert from "node:assert/strict";
import { test } from "node:test";
import { parseArgs } from "../args.js";

test("--places 0 is accepted", () => {
  const args = parseArgs(["--places", "0", "10/4"]);
  assert.equal(args.error, undefined);
  assert.equal(args.places, 0);
  assert.equal(args.expr, "10/4");
});
'''},
    run="cd ts && npm run build && node --test dist/test/hidden_04.test.js",
)
