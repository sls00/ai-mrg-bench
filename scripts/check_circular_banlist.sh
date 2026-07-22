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
# Scan set at AC0 time: deep-research-v1.md, research/ (the only shipping doc
# paths that exist pre-bootstrap). The repo-bootstrap PR extends SCAN_PATHS to
# templates/, src/, README.md once those paths exist (golden tests take over
# enforcement there).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

BANLIST_PATTERN='Circular 2026-03'
SCAN_PATHS=(deep-research-v1.md research)

# Path-based allowlist: files that legitimately discuss/debunk the phrase —
# the primary-source verification ticket, its close-out amendment, and the
# dated session logs that recorded the (later-corrected) belief at the time.
is_allowlisted() {
  case "$1" in
    research/findings/R-12-*|research/findings/R-14-*|research/sessions/*) return 0 ;;
    *) return 1 ;;
  esac
}

hits=0

for path in "${SCAN_PATHS[@]}"; do
  [ -e "$path" ] || continue
  while IFS= read -r -d '' file; do
    is_allowlisted "$file" && continue
    if grep -qF "$BANLIST_PATTERN" "$file"; then
      echo "BANLIST VIOLATION: $file"
      grep -nF "$BANLIST_PATTERN" "$file" | sed 's/^/  /'
      hits=$((hits + 1))
    fi
  done < <(find "$path" -type f -name '*.md' -print0)
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
