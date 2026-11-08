BUG = dict(
    id="06", slug="ts-history-zero-count", title=":history 0 says there is no history",
    lang="ts", tier="L1", category="repl-commands", kind="fix",
    commit_message="refactor: simplify :history argument parsing",
    issue=r'''
```
> 1+1
2
> :history 0
(no history)
```

I had just evaluated something, so "(no history)" is misleading. `:history -1` and `:history x` print the usage hint
(`usage: :history [count]`); I would expect `:history 0` to do the same since a count of zero makes no sense.
''',
    answer=dict(
        culprit="ts/src/commands.ts::parseCommand (history case)",
        mechanism="The count check was loosened to `count < 0`, so 0 is accepted and `History.list(0)` returns an empty list, which the REPL reports as no history.",
        fix="Require `count < 1` to be an error.",
        grading="TypeScript-only. Expected clean stop under current LYRA.",
    ),
    expected={"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "TypeScript-only bug"},
    edits=[("ts/src/commands.ts", "!Number.isInteger(count) || count < 1)", "!Number.isInteger(count) || count < 0)")],
    hidden={"ts/src/test/hidden_06.test.ts": r'''import assert from "node:assert/strict";
import { test } from "node:test";
import { parseCommand } from "../commands.js";

test(":history 0 is a usage error", () => {
  assert.equal(parseCommand(":history 0")?.kind, "error");
  assert.deepEqual(parseCommand(":history 1"), { kind: "history", count: 1 });
});
'''},
    run="cd ts && npm run build && node --test dist/test/hidden_06.test.js",
)
