#!/usr/bin/env bash
# AC0 messaging-hygiene gate (R-14 P0 patch table).
#
# Fails if any non-allowlisted file in the scan set asserts a CFPB circular
# numbered "2026-03" as authority. That circular does not exist: a dedicated
# primary-source search (research/findings/R-12-circular-2026-03-primary-verification.md)
# found no such document on CFPB.gov, in CFPB's Newsroom archive, or in the
# Federal Register. See research/findings/R-14-r12-r13-closeout-amendment-proposal.md
# for the close-out and the approved patch set.
#
# Historical citations of Circular 2022-03 / 2023-03 (withdrawn May 12, 2025)
# are NOT banned — only the exact phrase "Circular 2026-03" is, since there is
# no legitimate current or historical use of that phrase anywhere in this repo.
#
# Scan set: deep-research-v1.md, research/, templates/, src/, README.md.
# Golden tests take over enforcement in src/ post-P0; banlist remains the
# docs/templates/README gate for shipping copy hygiene.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

BANLIST_PATTERN='Circular 2026-03'
SCAN_PATHS=(deep-research-v1.md research README.md)
# Optional paths — added when present (repo-bootstrap+).
for optional in templates src; do
  [ -e "$optional" ] && SCAN_PATHS+=("$optional")
done

# Path-based allowlist: files that legitimately discuss/debunk the phrase —
# the primary-source verification ticket, its close-out amendment, and the
# dated session logs that recorded the (later-corrected) belief at the time.
is_allowlisted() {
  case "$1" in
    research/findings/R-12-*|research/findings/R-14-*|research/sessions/*) return 0 ;;
    *) return 1 ;;
  esac
}

# Lines that mention the phrase only to forbid, debunk, or mark unsupported are OK.
is_negated_context() {
  grep -qiE 'do[[:space:]-]*not|not assert|not operative|unsupported|unverified|❌|debunk|do-not-claim|messaging hygiene|no primary source' <<<"$1"
}

scan_file_for_violations() {
  local file=$1
  local lineno=0
  local line
  while IFS= read -r line || [ -n "$line" ]; do
    lineno=$((lineno + 1))
    [[ "$line" == *"$BANLIST_PATTERN"* ]] || continue
    is_negated_context "$line" && continue
    echo "$lineno:$line"
  done < "$file"
}

hits=0

for path in "${SCAN_PATHS[@]}"; do
  [ -e "$path" ] || continue
  if [ -f "$path" ]; then
    files=("$path")
  else
    mapfile -d '' files < <(find "$path" -type f \( -name '*.md' -o -name '*.py' -o -name '*.jinja2' -o -name '*.j2' \) -print0)
  fi
  for file in "${files[@]}"; do
    is_allowlisted "$file" && continue
    violations=$(scan_file_for_violations "$file" || true)
    if [ -n "$violations" ]; then
      echo "BANLIST VIOLATION: $file"
      echo "$violations" | sed 's/^/  /'
      hits=$((hits + 1))
    fi
  done
done

# RESEARCH_FOUNDATION_v2.md: scanned unless it carries the supersession
# banner (R-14 P2 — body stays frozen/unedited; the banner is what makes
# excluding it from the scan safe).
FOUNDATION_FILE="RESEARCH_FOUNDATION_v2.md"
if [ -f "$FOUNDATION_FILE" ]; then
  if grep -q "Supersession notice" "$FOUNDATION_FILE"; then
    echo "SKIP: $FOUNDATION_FILE (supersession banner present)"
  elif grep -qF "$BANLIST_PATTERN" "$FOUNDATION_FILE"; then
    echo "BANLIST VIOLATION: $FOUNDATION_FILE (no supersession banner found)"
    grep -nF "$BANLIST_PATTERN" "$FOUNDATION_FILE" | sed 's/^/  /'
    hits=$((hits + 1))
  fi
fi

if [ "$hits" -gt 0 ]; then
  echo
  echo "FAIL: $hits file(s) assert unverified \"Circular 2026-03\" authority."
  echo "See research/findings/R-12-circular-2026-03-primary-verification.md"
  exit 1
fi

echo "PASS: banlist clean (${SCAN_PATHS[*]}, $FOUNDATION_FILE)."
exit 0
