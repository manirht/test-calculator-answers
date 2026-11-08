#!/usr/bin/env sh
# Prepare a scratch repository for one bug, ready to hand to LYRA.
#   tools/prepare.sh <bug-id> <dest-dir> [remote-url]
# The scratch repo is the base commit plus one plausible-looking commit that introduces the bug.
# Its history never mentions that the bug is planted, so LYRA's git archaeology works as it would
# on a real regression. The hidden tests and the answer are NOT copied there.
set -eu
root="$(cd "$(dirname "$0")/.." && pwd)"
id="${1:?usage: prepare.sh <bug-id> <dest-dir> [remote-url]}"
dest="${2:?usage: prepare.sh <bug-id> <dest-dir> [remote-url]}"
remote="${3:-}"
base_repo="${TEST_CALC_REPO:-$root/../test-calculator}"
bug_dir="$(ls -d "$root"/bugs/"$id"-* | head -n 1)"

[ -e "$dest" ] && { echo "$dest already exists" >&2; exit 1; }
git clone -q --no-hardlinks "$base_repo" "$dest"
cd "$dest"
git checkout -q base-v1
git checkout -q -B main
git remote remove origin
[ -n "$remote" ] && git remote add origin "$remote"

if [ -s "$bug_dir/inject.patch" ]; then
  git apply "$bug_dir/inject.patch"
  message="$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['commit_message'])" "$bug_dir/meta.json")"
  git add -A
  git commit -q -m "$message"
fi
cp "$bug_dir/issue.md" "$dest/../issue-$id.md" 2>/dev/null || cp "$bug_dir/issue.md" "$(dirname "$dest")/issue-$id.md"
echo "prepared $dest at $(git rev-parse --short HEAD)"
echo "issue text: $(dirname "$dest")/issue-$id.md"
echo "run LYRA:   lyra run --repo $dest --issue <number> --issue-file $(dirname "$dest")/issue-$id.md"
