#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$HOME/.local/bin:$PATH"

echo "=== Checking GitHub Authentication ==="
gh auth status

echo "=== Publishing HM2 as hmweek2 ==="
cd "$DIR/hm2"
if ! gh repo view DavideLights/hmweek2 >/dev/null 2>&1; then
  gh repo create hmweek2 --public --source=. --remote=origin --push
else
  git remote set-url origin https://github.com/DavideLights/hmweek2.git 2>/dev/null || git remote add origin https://github.com/DavideLights/hmweek2.git
  git push -u origin main
fi
gh api -X POST repos/DavideLights/hmweek2/pages -f build_type=workflow 2>/dev/null || true

echo "=== Publishing HM3 as hm3 ==="
cd "$DIR/hm3"
if ! gh repo view DavideLights/hm3 >/dev/null 2>&1; then
  gh repo create hm3 --public --source=. --remote=origin --push
else
  git remote set-url origin https://github.com/DavideLights/hm3.git 2>/dev/null || git remote add origin https://github.com/DavideLights/hm3.git
  git push -u origin main
fi
gh api -X POST repos/DavideLights/hm3/pages -f build_type=workflow 2>/dev/null || true

echo "=== Publishing HM4 as hm4 ==="
cd "$DIR/hm4"
if ! gh repo view DavideLights/hm4 >/dev/null 2>&1; then
  gh repo create hm4 --public --source=. --remote=origin --push
else
  git remote set-url origin https://github.com/DavideLights/hm4.git 2>/dev/null || git remote add origin https://github.com/DavideLights/hm4.git
  git push -u origin main
fi
gh api -X POST repos/DavideLights/hm4/pages -f build_type=workflow 2>/dev/null || true

echo "=== Publishing HM5 as hm5 ==="
cd "$DIR/hm5"
if ! gh repo view DavideLights/hm5 >/dev/null 2>&1; then
  gh repo create hm5 --public --source=. --remote=origin --push
else
  git remote set-url origin https://github.com/DavideLights/hm5.git 2>/dev/null || git remote add origin https://github.com/DavideLights/hm5.git
  git push -u origin main
fi
gh api -X POST repos/DavideLights/hm5/pages -f build_type=workflow 2>/dev/null || true

echo "=== All homeworks published and GitHub Pages workflows triggered! ==="
