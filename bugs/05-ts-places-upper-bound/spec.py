BUG = dict(
    id="05", slug="ts-places-upper-bound", title="A too-large --places is accepted, then every expression fails",
    lang="ts", tier="L1", category="cli-args", kind="fix",
    commit_message="refactor: drop duplicated places limit from argument parsing",
    issue=r'''
I fat-fingered `--places 300`:

```
$ calc-ui --places 300
> 1+1
error[BAD_REQUEST]: places must be at most 30
> 2+2
error[BAD_REQUEST]: places must be at most 30
```

The session starts as if everything were fine and then every line fails. The command line should refuse the value up front,
the same way it refuses `--places -1`: `calc-ui: --places must be at most 30`.
''',
    answer=dict(
        culprit="ts/src/args.ts::parseArgs (--places case)",
        mechanism="The upper bound check (`places > MAX_PLACES`) and its constant were removed. The engine still enforces 30 per request, so the failure shows up later and on every line.",
        fix="Restore `const MAX_PLACES = 30;` and `if (places > MAX_PLACES) return { ...args, error: `--places must be at most ${MAX_PLACES}` };` after the integer check.",
        grading="TypeScript-only. Expected clean stop under current LYRA. A correct RCA explains why the symptom appears in the engine (BAD_REQUEST) while the cause is in argument parsing.",
    ),
    expected={"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "TypeScript-only bug"},
    edits=[
        ("ts/src/args.ts", "\nconst MAX_PLACES = 30;", ""),
        ("ts/src/args.ts", "\n        if (places > MAX_PLACES) return { ...args, error: `--places must be at most ${MAX_PLACES}` };", ""),
    ],
    hidden={"ts/src/test/hidden_05.test.ts": r'''import assert from "node:assert/strict";
import { test } from "node:test";
import { parseArgs } from "../args.js";

test("--places above 30 is rejected up front", () => {
  assert.match(parseArgs(["--places", "31"]).error ?? "", /at most 30/);
  assert.equal(parseArgs(["--places", "30"]).error, undefined);
});
'''},
    run="cd ts && npm run build && node --test dist/test/hidden_05.test.js",
)
