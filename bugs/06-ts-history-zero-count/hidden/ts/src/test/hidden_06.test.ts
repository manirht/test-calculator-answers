import assert from "node:assert/strict";
import { test } from "node:test";
import { parseCommand } from "../commands.js";

test(":history 0 is a usage error", () => {
  assert.equal(parseCommand(":history 0")?.kind, "error");
  assert.deepEqual(parseCommand(":history 1"), { kind: "history", count: 1 });
});
