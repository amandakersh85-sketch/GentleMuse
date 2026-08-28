#!/usr/bin/env bash
# Regression suite for the caption-to-clip binding gate.
# Run from the repo root:  bash filing-system/tests/run-tests.sh
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
GATE="$HERE/../scripts/gm_bind_check.py"
LIB_TOOL="$HERE/../scripts/gm_clip_library.py"
LIB="$HERE/clip-library.sample.csv"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
pass=0; fail=0

check() { # name expected_exit render_file [expected_code ...]
  local name="$1" want="$2" render="$3"; shift 3
  local out; out="$(python3 "$GATE" --render "$render" --library "$LIB" 2>&1)"; local got=$?
  local ok=1
  [ "$got" = "$want" ] || { ok=0; echo "  exit $got, wanted $want"; }
  for code in "$@"; do
    grep -q "$code" <<<"$out" || { ok=0; echo "  missing finding: $code"; }
  done
  if [ $ok = 1 ]; then echo "PASS  $name"; pass=$((pass+1))
  else echo "FAIL  $name"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi
}

echo "== gate =="
check "clean reel passes"            0 "$HERE/render.clean.json"
check "reported bug is caught"       1 "$HERE/render.broken.json" E04_OVERRUN E07_TOPIC_MISMATCH E11_BETTER_CLIP_EXISTS
check "missing footage holds"        2 "$HERE/render.hold.json"   H01_NEEDS_FOOTAGE
check "edge cases all fire"          1 "$HERE/render.edge.json" \
      E02_UNDESCRIBED E06_ORIENTATION E08_NO_MATCH_REASON E09_REUSE_CONFLICT E01_UNKNOWN_CLIP

python3 - "$TMP" <<'PY'
import json, sys, os
tmp = sys.argv[1]
bad_sum = {"title":"Sum Reel","format":"9:16","duration":12,"clips":[
  {"clip_id":"coffee-morning-pour-01","start":0,"duration":4,"text":"Coffee poured slow",
   "match_reason":"clip is the oat milk pour into coffee"}]}
json.dump(bad_sum, open(os.path.join(tmp,"sum.json"),"w"))
override = {"title":"Override Reel","format":"9:16","duration":4,"clips":[
  {"clip_id":"coffee-morning-pour-01","start":0,"duration":4,"text":"Discipline is a quiet thing",
   "match_reason":"the unhurried pour is the visual metaphor for restraint","override":True}]}
json.dump(override, open(os.path.join(tmp,"override.json"),"w"))
PY
check "duration arithmetic checked"  1 "$TMP/sum.json"      E05_SUM_MISMATCH
check "explicit override allowed"    0 "$TMP/override.json" N01_OVERRIDE

echo
echo "== library builder =="
cat > "$TMP/video-triage.csv" <<'CSV'
Asset Name,Type,Lane,Category / Use,Lives On,Folder / Location,Direct Link,Status,Needs Filing?,Verdict,Why,DurationSec,Resolution,Orientation,SizeMB,Modified,Thumb,FullPath,SHA256
VID_001.mp4,Video,GM,Raw footage,Local,D:\Footage\driving,,Raw,YES,KEEP,vertical,11.4,1080x1920,Vertical,22.1,2026-07-14,0001_a.jpg,D:\Footage\driving\VID_001.mp4,AAA1
VID_002.mp4,Video,GM,Raw footage,Local,D:\Footage\bed,,Raw,YES,KEEP,vertical,3.0,1080x1920,Vertical,6.4,2026-07-15,0002_b.jpg,D:\Footage\bed\VID_002.mp4,BBB2
VID_003.mp4,Video,GM,Raw footage,Local,D:\Footage\bed,,Raw,No,CUT,duplicate,3.0,1080x1920,Vertical,6.4,2026-07-15,,D:\Footage\bed\VID_003.mp4,BBB2
CSV
out="$(python3 "$LIB_TOOL" --from-triage "$TMP/video-triage.csv" --out "$TMP/lib.csv" 2>&1)"
if grep -q "(2 clips)" <<<"$out" && grep -q "described   : 0 of 2" <<<"$out"; then
  echo "PASS  builds skeleton from KEEP rows only"; pass=$((pass+1))
else echo "FAIL  builds skeleton from KEEP rows only"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

python3 "$LIB_TOOL" --audit "$TMP/lib.csv" >/dev/null 2>&1
[ $? = 1 ] && { echo "PASS  audit blocks an undescribed library"; pass=$((pass+1)); } \
           || { echo "FAIL  audit blocks an undescribed library"; fail=$((fail+1)); }

python3 - "$TMP/lib.csv" <<'PY'
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")))
for r in rows:
    r["Shot"] = "Amanda in the passenger seat with her feet on the dash" if "driving" in r["ClipID"] \
                else "Close shot of tangled sheets and a pillow at a strange angle"
    r["Described"] = "yes"
w = csv.DictWriter(open(sys.argv[1], "w", newline="", encoding="utf-8"), fieldnames=rows[0].keys())
w.writeheader(); w.writerows(rows)
PY
python3 "$LIB_TOOL" --audit "$TMP/lib.csv" >/dev/null 2>&1
[ $? = 0 ] && { echo "PASS  audit passes a described library"; pass=$((pass+1)); } \
           || { echo "FAIL  audit passes a described library"; fail=$((fail+1)); }

out="$(python3 "$LIB_TOOL" --from-triage "$TMP/video-triage.csv" --out "$TMP/lib.csv" --merge 2>&1)"
if grep -q "carried forward: 2" <<<"$out"; then
  echo "PASS  re-triage keeps descriptions"; pass=$((pass+1))
else echo "FAIL  re-triage keeps descriptions"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

echo
echo "$pass passed, $fail failed"
[ "$fail" = 0 ]
