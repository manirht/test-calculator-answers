import assert from "node:assert/strict";
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
