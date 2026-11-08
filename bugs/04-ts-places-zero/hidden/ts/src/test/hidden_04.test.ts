import assert from "node:assert/strict";
import { test } from "node:test";
import { parseArgs } from "../args.js";

test("--places 0 is accepted", () => {
  const args = parseArgs(["--places", "0", "10/4"]);
  assert.equal(args.error, undefined);
  assert.equal(args.places, 0);
  assert.equal(args.expr, "10/4");
});
