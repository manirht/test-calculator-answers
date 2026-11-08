#!/usr/bin/env python3
"""Check every bug against the base tag.

For each bug, in a scratch checkout of the base tag:
  1. inject.patch applies cleanly                      (the bug is plantable)
  2. the visible test suites still pass                (the bug is silent: LYRA is not handed a red test)
  3. the hidden test fails, and fails by assertion     (the bug is real and the test is not just broken)
  4. fix.patch applies and the hidden test passes      (the reference fix is right)
  5. the visible suites pass again after the fix

Usage: tools/verify.py [bug-id ...]     (default: all)
"""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_REPO = Path(os.environ.get("TEST_CALC_REPO", ROOT.parent / "test-calculator"))
BASE_TAG = os.environ.get("TEST_CALC_BASE_TAG", "base-v1")
WORK = Path(os.environ.get("VERIFY_DIR", "/tmp/calc-verify"))
TREE = WORK / "tree"
ENV = {
    **os.environ,
    "CARGO_TARGET_DIR": str(WORK / "target"),
    "CARGO_TERM_COLOR": "never",
    "CALC_BIN": str(WORK / "target" / "debug" / "calc"),
}
if Path("/opt/homebrew/opt/rustup/bin").exists():
    ENV["PATH"] = "/opt/homebrew/opt/rustup/bin:" + ENV["PATH"]
GIT = ["git", "-c", "user.name=verify", "-c", "user.email=verify@example.invalid", "-c", "commit.gpgsign=false"]

VISIBLE = {
    "rust": "cargo fmt --all -- --check && cargo test --workspace",
    "python": "cd python && python3 -m unittest discover tests",
    "ts": "cd ts && npm test",
}
# A hidden test that fails for one of these reasons is broken, not a proof of the bug.
BROKEN = ("error[E", "could not compile", "SyntaxError", "ImportError", "ModuleNotFoundError", "error TS", "Cannot find module")


def sh(cmd, timeout=600):
    try:
        p = subprocess.run(cmd, shell=True, cwd=TREE, env=ENV, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired as e:
        return 124, (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else str(e.stdout or "")


def git(*args, check=True):
    return subprocess.run(GIT + list(args), cwd=TREE, check=check, capture_output=True, text=True)


def base_sha():
    return subprocess.run(["git", "-C", str(BASE_REPO), "rev-parse", BASE_TAG], check=True, capture_output=True, text=True).stdout.strip()


def setup_tree():
    stamp = WORK / "base.sha"
    if TREE.exists() and (not stamp.exists() or stamp.read_text().strip() != base_sha()):
        shutil.rmtree(TREE)  # the base tag moved: start from a fresh export
    if not (TREE / ".git").exists():
        WORK.mkdir(parents=True, exist_ok=True)
        stamp.write_text(base_sha())
        TREE.mkdir(parents=True, exist_ok=True)
        archive = subprocess.run(["git", "-C", str(BASE_REPO), "archive", BASE_TAG], check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", str(TREE)], input=archive, check=True)
        git("init", "-q")
        git("add", "-A")
        git("commit", "-q", "-m", "base")
        print("installing TypeScript dependencies once ...")
        code, out = sh("cd ts && npm ci --silent")
        if code:
            raise SystemExit(out)


def reset_tree():
    git("reset", "--hard", "-q", "HEAD")
    git("clean", "-fdq")


def run_visible(suites):
    for suite in suites:
        if suite == "ts":
            # Compiled hidden tests from an earlier step must not leak into the visible run.
            shutil.rmtree(TREE / "ts" / "dist", ignore_errors=True)
        code, out = sh(VISIBLE[suite])
        if code:
            return False, f"visible {suite} suite failed:\n{out[-1500:]}"
    return True, ""


def verify(bug_dir):
    meta = json.loads((bug_dir / "meta.json").read_text())
    if meta["kind"] != "fix":
        return True, "no code check (stop-expected)" if not (bug_dir / "inject.patch").read_text() else _verify_stop(bug_dir, meta)
    reset_tree()
    patch = bug_dir / "inject.patch"
    p = subprocess.run(["git", "apply", str(patch)], cwd=TREE, capture_output=True, text=True)
    if p.returncode:
        return False, f"inject.patch does not apply: {p.stderr}"
    ok, why = run_visible(meta["suites"])
    if not ok:
        return False, "bug is not silent. " + why

    hidden_root = bug_dir / "hidden"
    for rel in meta["hidden_files"]:
        dest = TREE / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(hidden_root / rel, dest)
    code, out = sh(meta["hidden_run"])
    if code == 0:
        return False, "hidden test PASSES with the bug present"
    if any(marker in out for marker in BROKEN):
        return False, "hidden test is broken, not failing by assertion:\n" + out[-1500:]
    for rel in meta["hidden_files"]:
        (TREE / rel).unlink()

    p = subprocess.run(["git", "apply", str(bug_dir / "fix.patch")], cwd=TREE, capture_output=True, text=True)
    if p.returncode:
        return False, f"fix.patch does not apply: {p.stderr}"
    for rel in meta["hidden_files"]:
        shutil.copyfile(hidden_root / rel, TREE / rel)
    code, out = sh(meta["hidden_run"])
    if code:
        return False, "hidden test still FAILS after the reference fix:\n" + out[-1500:]
    for rel in meta["hidden_files"]:
        (TREE / rel).unlink()
    ok, why = run_visible(meta["suites"])
    if not ok:
        return False, "after the fix. " + why
    return True, ""


def _verify_stop(bug_dir, meta):
    reset_tree()
    p = subprocess.run(["git", "apply", str(bug_dir / "inject.patch")], cwd=TREE, capture_output=True, text=True)
    if p.returncode:
        return False, f"inject.patch does not apply: {p.stderr}"
    ok, why = run_visible(meta["suites"] or ["rust", "python", "ts"])
    return ok, why or "stop-expected; patch applies and the visible suites stay green"


def main():
    wanted = set(sys.argv[1:])
    setup_tree()
    results = []
    for bug_dir in sorted((ROOT / "bugs").glob("*-*")):
        if not (bug_dir / "meta.json").exists():
            continue
        bug_id = bug_dir.name.split("-")[0]
        if wanted and bug_id not in wanted:
            continue
        start = time.time()
        ok, why = verify(bug_dir)
        results.append((bug_dir.name, ok, why))
        print(f"{'ok  ' if ok else 'FAIL'} {bug_dir.name} ({time.time() - start:.0f}s)")
        if not ok:
            print("     " + why.replace("\n", "\n     "))
    failed = [r for r in results if not r[1]]
    print(f"\n{len(results) - len(failed)}/{len(results)} bugs verified")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
