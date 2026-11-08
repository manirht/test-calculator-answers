#!/usr/bin/env python3
"""Expand every bugs/*/spec.py into the files a grader and a run need.

For each bug it writes, next to the spec:
  meta.json     machine-readable facts (language, tier, expected outcome, hidden-test command, ...)
  issue.md      the issue text exactly as a user would file it (title on the first line)
  answer.md     culprit, mechanism, reference fix and grading notes
  inject.patch  applies to the base tag; plants the bug
  fix.patch     the reverse; the reference fix
  hidden/       tests that are never shown to the agent; they fail before the fix and pass after
and finally INDEX.md. Run it again after editing a spec; output is deterministic.
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_REPO = Path(os.environ.get("TEST_CALC_REPO", ROOT.parent / "test-calculator"))
BASE_TAG = os.environ.get("TEST_CALC_BASE_TAG", "base-v1")
GIT = ["git", "-c", "user.name=builder", "-c", "user.email=builder@example.invalid", "-c", "commit.gpgsign=false"]


def run(cmd, cwd=None, **kw):
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True, **kw).stdout


def load_spec(path):
    module_spec = importlib.util.spec_from_file_location("spec", path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module.BUG


def export_base(dest):
    archive = subprocess.run(["git", "-C", str(BASE_REPO), "archive", BASE_TAG], check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(dest)], input=archive, check=True)


def apply_edits(tree, edits):
    for edit in edits:
        kind = edit[0]
        if kind == "add":
            _, rel, content = edit
            target = tree / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        elif kind == "delete":
            (tree / edit[1]).unlink()
        else:
            rel, old, new = edit
            target = tree / rel
            text = target.read_text()
            if text.count(old) != 1:
                raise SystemExit(f"{rel}: expected exactly one match for:\n{old}\n(found {text.count(old)})")
            target.write_text(text.replace(old, new))


def make_patches(edits):
    with tempfile.TemporaryDirectory() as tmp:
        tree = Path(tmp)
        export_base(tree)
        run(GIT + ["init", "-q"], cwd=tree)
        run(GIT + ["add", "-A"], cwd=tree)
        run(GIT + ["commit", "-q", "-m", "base"], cwd=tree)
        apply_edits(tree, edits)
        run(GIT + ["add", "-A"], cwd=tree)
        inject = run(GIT + ["diff", "--cached", "--no-color"], cwd=tree)
        fix = run(GIT + ["diff", "--cached", "--no-color", "-R"], cwd=tree)
    return inject, fix


def write_bug(bug_dir, spec):
    inject, fix = make_patches(spec.get("edits", []))
    (bug_dir / "inject.patch").write_text(inject)
    (bug_dir / "fix.patch").write_text(fix)

    hidden_dir = bug_dir / "hidden"
    if hidden_dir.exists():
        for old in sorted(hidden_dir.rglob("*"), reverse=True):
            old.unlink() if old.is_file() else old.rmdir()
    for rel, content in spec.get("hidden", {}).items():
        target = hidden_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)

    meta = {
        "id": spec["id"],
        "slug": spec["slug"],
        "title": spec["title"],
        "lang": spec["lang"],
        "also_touches": spec.get("also", []),
        "tier": spec["tier"],
        "category": spec["category"],
        "kind": spec["kind"],
        "expected": spec.get("expected", {"outcome": "fix"}),
        "culprit": spec["answer"].get("culprit", ""),
        "commit_message": spec.get("commit_message", "refactor: tidy up"),
        "suites": spec.get("suites", [spec["lang"]] if spec["lang"] != "none" else []),
        "hidden_files": sorted(spec.get("hidden", {})),
        "hidden_run": spec.get("run", ""),
    }
    (bug_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    (bug_dir / "issue.md").write_text(f"# {spec['title']}\n\n{spec['issue'].strip()}\n")

    answer = spec["answer"]
    lines = [f"# {spec['id']} {spec['title']}", ""]
    lines.append(f"- language: {spec['lang']}" + (f" (also {', '.join(spec['also'])})" if spec.get("also") else ""))
    lines.append(f"- tier: {spec['tier']}   category: {spec['category']}   kind: {spec['kind']}")
    lines.append(f"- expected outcome: {json.dumps(meta['expected'])}")
    lines.append(f"- culprit: `{answer.get('culprit', '-')}`")
    lines.append("")
    for heading, key in (("Root cause", "mechanism"), ("Reference fix", "fix"), ("How to grade", "grading"), ("Notes", "notes")):
        if answer.get(key):
            lines += [f"## {heading}", "", answer[key].strip(), ""]
    if spec.get("run"):
        lines += ["## Hidden test", "", f"Files: {', '.join(f'`{p}`' for p in sorted(spec.get('hidden', {})))}", "", "```sh", spec["run"], "```", ""]
    (bug_dir / "answer.md").write_text("\n".join(lines))
    return meta


def main():
    only = set(sys.argv[1:])
    metas = []
    for spec_path in sorted((ROOT / "bugs").glob("*/spec.py")):
        bug_dir = spec_path.parent
        if only and bug_dir.name.split("-")[0] not in only:
            metas.append(json.loads((bug_dir / "meta.json").read_text()))
            continue
        spec = load_spec(spec_path)
        assert bug_dir.name == f"{spec['id']}-{spec['slug']}", f"{bug_dir.name} does not match its spec id/slug"
        metas.append(write_bug(bug_dir, spec))
        print(f"built {bug_dir.name}")

    rows = ["| id | lang | tier | category | kind | title |", "|---|---|---|---|---|---|"]
    for m in metas:
        lang = m["lang"] + (f" (+{', '.join(m['also_touches'])})" if m["also_touches"] else "")
        rows.append(f"| {m['id']} | {lang} | {m['tier']} | {m['category']} | {m['kind']} | {m['title']} |")
    counts = {}
    for m in metas:
        counts[m["lang"]] = counts.get(m["lang"], 0) + 1
    summary = ", ".join(f"{k}: {v}" for k, v in sorted(counts.items()))
    (ROOT / "INDEX.md").write_text(f"# Bug index\n\n{len(metas)} bugs ({summary})\n\n" + "\n".join(rows) + "\n")


if __name__ == "__main__":
    main()
