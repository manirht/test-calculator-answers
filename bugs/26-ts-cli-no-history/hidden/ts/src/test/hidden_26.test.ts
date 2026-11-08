import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const binary = process.env.CALC_BIN ?? join(here, "..", "..", "..", "target", "debug", "calc");
const cli = join(here, "..", "cli.js");

function session(flags: string[]): string {
  const dir = mkdtempSync(join(tmpdir(), "calc-hidden-26-"));
  const file = join(dir, "history.json");
  const result = spawnSync(process.execPath, [cli, "--bin", binary, "--history-file", file, ...flags], {
    input: "85000 / 12\n:quit\n",
    encoding: "utf8",
  });
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /7083\.3333333333/);
  return file;
}

test("--no-history neither reads nor writes the history file", () => {
  assert.ok(existsSync(binary), `build the engine first: ${binary}`);
  assert.equal(existsSync(session(["--no-history"])), false);
  assert.equal(existsSync(session([])), true);
});
