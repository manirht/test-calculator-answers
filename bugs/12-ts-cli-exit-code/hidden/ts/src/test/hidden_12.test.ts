import assert from "node:assert/strict";
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
