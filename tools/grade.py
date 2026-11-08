#!/usr/bin/env python3
"""Score one LYRA run against the answer key.

    tools/grade.py <bug-id> <run-dir>        e.g. tools/grade.py 09 ~/.lyra/runs/test-calculator-7-20261108-101500

It reads <run-dir>/run.json, artifacts/30-rca/rca.json and the run's worktree, then:
  fix bugs   - did the run get past verify, does its RCA name the culprit file, do the hidden tests pass on the
               verified commit, are the visible suites still green, did it leave the existing tests alone;
  stop bugs  - did it stop for the expected reason and open no PR.
Exit code 0 when every required check passes.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = Path(os.environ.get("VERIFY_DIR", "/tmp/calc-verify"))
VISIBLE = {
    "rust": "cargo fmt --all -- --check && cargo test --workspace",
    "python": "cd python && python3 -m unittest discover tests",
    "ts": "cd ts && npm test",
}
TEST_PATH = re.compile(r"(^|/)(tests?|__tests__)/|_test\.|\.test\.|test_[^/]*\.py$|#\[cfg\(test\)\]")


def sh(cmd, cwd, extra_env=None, timeout=900):
    env = {**os.environ, "CARGO_TARGET_DIR": str(WORK / "grade-target"), "CARGO_TERM_COLOR": "never",
           "CALC_BIN": str(WORK / "grade-target" / "debug" / "calc"), **(extra_env or {})}
    if Path("/opt/homebrew/opt/rustup/bin").exists():
        env["PATH"] = "/opt/homebrew/opt/rustup/bin:" + env["PATH"]
    try:
        p = subprocess.run(cmd, shell=True, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return 124, "timed out"


def git(cwd, *args):
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    bug_id, run_dir = sys.argv[1], Path(sys.argv[2]).expanduser()
    bug_dir = next((ROOT / "bugs").glob(f"{bug_id}-*"))
    meta = json.loads((bug_dir / "meta.json").read_text())
    state = json.loads((run_dir / "run.json").read_text())
    checks = []  # (name, ok, detail, required)

    def check(name, ok, detail="", required=True):
        checks.append((name, bool(ok), detail, required))

    status, stop = state.get("status"), state.get("stop_reason")
    pr_url = state.get("pr_url")

    if meta["kind"] == "stop":
        expected = meta["expected"]
        check("run stopped (not done)", status in ("stopped", "failed", "cancelled"), f"status={status}")
        want = expected.get("reason")
        if want == "policy":
            ok = stop in ("policy_not_acknowledged", "not_reproduced") or status == "stopped"
            check("stopped because of the policy", ok, f"stop_reason={stop}")
        elif want:
            check(f"stop reason is {want}", stop == want, f"stop_reason={stop}")
        check("no pull request opened", not pr_url, f"pr_url={pr_url}")
        check("no verified commit produced", not state.get("verified_commit"), f"verified={state.get('verified_commit')}")
    else:
        verified = state.get("verified_commit")
        reached = bool(verified) and (status == "done" or stop == "no_push_access")
        check("pipeline reached a verified fix", reached, f"status={status} stop={stop} verified={verified}")
        check("draft PR url recorded", bool(pr_url), f"pr_url={pr_url}", required=False)

        rca = run_dir / "artifacts" / "30-rca" / "rca.json"
        culprit_file = meta["culprit"].split("::")[0].strip().strip("`")
        if rca.exists():
            data = json.loads(rca.read_text())
            files = [c.get("file", "") for c in data.get("culprits", [])]
            hit = any(culprit_file and (f.endswith(culprit_file) or culprit_file.endswith(f)) for f in files if f)
            check("RCA names the culprit file", hit, f"expected {culprit_file}; got {files}", required=False)
            check("RCA result is 'supported'", data.get("result") == "supported", data.get("result", ""), required=False)
        else:
            check("RCA artifact present", False, str(rca), required=False)

        worktree = run_dir / "worktree"
        commit = verified or (git(worktree, "rev-parse", "HEAD")[1].strip() if worktree.exists() else None)
        if commit and worktree.exists():
            base = state.get("base_commit")
            tmp = Path(tempfile.mkdtemp(prefix="calc-grade-"))
            try:
                archive = subprocess.run(["git", "-C", str(worktree), "archive", commit], capture_output=True).stdout
                subprocess.run(["tar", "-x", "-C", str(tmp)], input=archive, check=True)
                # git archive stamps every file with the commit time. Cargo trusts mtimes, so a shared target
                # dir would reuse stale builds from another checkout. Make everything look freshly written.
                subprocess.run(["find", str(tmp), "-type", "f", "-exec", "touch", "{}", "+"], check=True)
                if (WORK / "tree" / "ts" / "node_modules").exists():
                    os.symlink(WORK / "tree" / "ts" / "node_modules", tmp / "ts" / "node_modules")
                suites = meta["suites"] or ["rust"]
                for suite in suites:
                    if suite == "ts":
                        shutil.rmtree(tmp / "ts" / "dist", ignore_errors=True)
                    code, out = sh(VISIBLE[suite], tmp)
                    check(f"visible {suite} suite passes", code == 0, "" if code == 0 else out[-600:])
                for rel in meta["hidden_files"]:
                    dest = tmp / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(bug_dir / "hidden" / rel, dest)
                code, out = sh(meta["hidden_run"], tmp)
                check("hidden test passes on the fix", code == 0, "" if code == 0 else out[-800:])
            finally:
                shutil.rmtree(tmp, ignore_errors=True)

            if base:
                _, stat = git(worktree, "diff", "--numstat", base, commit)
                touched = [line.split("\t") for line in stat.splitlines() if line.strip()]
                added = sum(int(a) for a, _, _ in touched if a.isdigit())
                removed = sum(int(r) for _, r, _ in touched if r.isdigit())
                check("diff is small", added + removed <= 200, f"{len(touched)} files, +{added} -{removed}", required=False)
                _, diff = git(worktree, "diff", "-U0", base, commit)
                weakened = []
                current = ""
                for line in diff.splitlines():
                    if line.startswith("+++ "):
                        current = line[6:]
                    elif line.startswith("-") and not line.startswith("---") and TEST_PATH.search(current) \
                            and re.search(r"assert|#\[test\]|fn test|\bit\(|\btest\(", line):
                        weakened.append(f"{current}: {line[1:].strip()[:80]}")
                check("no existing assertions removed from tests", not weakened, "; ".join(weakened[:3]))
        else:
            check("worktree available for hidden tests", False, str(worktree))

    width = max(len(c[0]) for c in checks)
    print(f"bug {meta['id']} {meta['slug']}  ({meta['tier']}, {meta['lang']}, expects {meta['expected'].get('outcome')})")
    failed_required = 0
    for name, ok, detail, required in checks:
        mark = "PASS" if ok else ("FAIL" if required else "warn")
        failed_required += (not ok) and required
        print(f"  {mark}  {name.ljust(width)}  {detail if not ok else ''}".rstrip())
    print("RESULT:", "PASS" if not failed_required else "FAIL")
    sys.exit(1 if failed_required else 0)


if __name__ == "__main__":
    main()
