import assert from "node:assert/strict";
import { test } from "node:test";
import { parseArgs } from "../args.js";

test("--places above 30 is rejected up front", () => {
  assert.match(parseArgs(["--places", "31"]).error ?? "", /at most 30/);
  assert.equal(parseArgs(["--places", "30"]).error, undefined);
});
