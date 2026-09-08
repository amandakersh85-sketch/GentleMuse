#!/usr/bin/env bash
# Regression suite for Run 6 (caption to clip binding) and Run 7 (holiday captions).
# Run from the repo root:  bash filing-system/tests/run-tests.sh
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
. "$HERE/../scripts/gm_py.sh"   # sets $PY. See that file: the name python3 is a Store stub on Windows.
GATE="$HERE/../scripts/gm_bind_check.py"
LIB_TOOL="$HERE/../scripts/gm_clip_library.py"
LIB="$HERE/clip-library.sample.csv"
HGATE="$HERE/../scripts/gm_holiday_check.py"
BANK_TOOL="$HERE/../scripts/gm_holiday_bank.py"
BANK="$HERE/../data/holiday-fact-bank.csv"
CAL="$HERE/../data/holiday-calendar.csv"
HARGS=""
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
pass=0; fail=0

check() { # name expected_exit render_file [expected_code ...]
  local name="$1" want="$2" render="$3"; shift 3
  local out; out="$("$PY" "$GATE" --render "$render" --library "$LIB" 2>&1)"; local got=$?
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

"$PY" - "$TMP" <<'PY'
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
out="$("$PY" "$LIB_TOOL" --from-triage "$TMP/video-triage.csv" --out "$TMP/lib.csv" 2>&1)"
if grep -q "(2 clips)" <<<"$out" && grep -q "described   : 0 of 2" <<<"$out"; then
  echo "PASS  builds skeleton from KEEP rows only"; pass=$((pass+1))
else echo "FAIL  builds skeleton from KEEP rows only"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

"$PY" "$LIB_TOOL" --audit "$TMP/lib.csv" >/dev/null 2>&1
[ $? = 1 ] && { echo "PASS  audit blocks an undescribed library"; pass=$((pass+1)); } \
           || { echo "FAIL  audit blocks an undescribed library"; fail=$((fail+1)); }

"$PY" - "$TMP/lib.csv" <<'PY'
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")))
for r in rows:
    r["Shot"] = "Amanda in the passenger seat with her feet on the dash" if "driving" in r["ClipID"] \
                else "Close shot of tangled sheets and a pillow at a strange angle"
    r["Described"] = "yes"
w = csv.DictWriter(open(sys.argv[1], "w", newline="", encoding="utf-8"), fieldnames=rows[0].keys())
w.writeheader(); w.writerows(rows)
PY
"$PY" "$LIB_TOOL" --audit "$TMP/lib.csv" >/dev/null 2>&1
[ $? = 0 ] && { echo "PASS  audit passes a described library"; pass=$((pass+1)); } \
           || { echo "FAIL  audit passes a described library"; fail=$((fail+1)); }

out="$("$PY" "$LIB_TOOL" --from-triage "$TMP/video-triage.csv" --out "$TMP/lib.csv" --merge 2>&1)"
if grep -q "carried forward: 2" <<<"$out"; then
  echo "PASS  re-triage keeps descriptions"; pass=$((pass+1))
else echo "FAIL  re-triage keeps descriptions"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

hcheck() { # name expected_exit post_file [expected_code ...]   HARGS adds gate flags
  local name="$1" want="$2" post="$3"; shift 3
  local out; out="$("$PY" "$HGATE" --post "$post" --bank "$BANK" --calendar "$CAL" $HARGS 2>&1)"; local got=$?
  local ok=1
  [ "$got" = "$want" ] || { ok=0; echo "  exit $got, wanted $want"; }
  for code in "$@"; do
    grep -q "$code" <<<"$out" || { ok=0; echo "  missing finding: $code"; }
  done
  if [ $ok = 1 ]; then echo "PASS  $name"; pass=$((pass+1))
  else echo "FAIL  $name"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi
  HARGS=""
}

expect_exit() { # name expected_exit command...
  local name="$1" want="$2"; shift 2
  local out; out="$("$@" 2>&1)"; local got=$?
  if [ "$got" = "$want" ]; then echo "PASS  $name"; pass=$((pass+1))
  else echo "FAIL  $name (exit $got, wanted $want)"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi
}

echo
echo "== holiday gate =="
hcheck "clean holiday batch passes"   0 "$HERE/holiday.clean.json"
hcheck "invented fact is caught"      1 "$HERE/holiday.broken.json" E01_UNKNOWN_FACT
hcheck "unsourced year is caught"     1 "$HERE/holiday.broken.json" E07_UNSOURCED_YEAR
hcheck "voice violations are caught"  1 "$HERE/holiday.broken.json" E11_SPELLED_NUMBER E13_HYPE
hcheck "missing fact holds"           2 "$HERE/holiday.hold.json"   H01_NEEDS_FACT
hcheck "edge cases all fire"          1 "$HERE/holiday.edge.json" \
      E04_WRONG_HOLIDAY E05_OUT_OF_SEASON E08_FACT_NOT_TOLD E12_HASHTAG_COUNT \
      E14_PLATFORM E15_REUSE

"$PY" - "$TMP" <<'PY7'
import json, os, sys
tmp = sys.argv[1]
def w(name, data): json.dump(data, open(os.path.join(tmp, name), "w"))

w("h-decade.json", [{"title":"Decade paraphrase","holiday_id":"halloween","post_date":"2026-10-16",
  "platform":"instagram","fact_id":"HAL-003","hook":"Nobody was burned at Salem.",
  "caption":"Of the 20 people executed in the 1690s, 19 were hanged and Giles Corey was pressed to death under stones. The lurid detail everyone repeats is the one that is wrong.",
  "hashtags":["#gentlemuse"]}])
w("h-override.json", [{"title":"Sourced elsewhere","holiday_id":"halloween","post_date":"2026-10-16",
  "platform":"instagram","fact_id":"HAL-003","override":True,
  "override_reason":"the 1711 restitution act is sourced separately from the Massachusetts Archives",
  "hook":"Nobody was burned at Salem.",
  "caption":"Of the 20 people executed in 1692, 19 were hanged and Giles Corey was pressed to death. The colony passed restitution in 1711, which almost nobody mentions.",
  "hashtags":["#gentlemuse"]}])
w("h-noturn.json", [{"title":"Trivia account","holiday_id":"halloween","post_date":"2026-10-16",
  "platform":"instagram","fact_id":"HAL-003",
  "caption":"Nobody was burned at the Salem witch trials of 1692. Of the 20 people executed, 19 were hanged and Giles Corey was pressed to death under stones.",
  "hashtags":["#gentlemuse"]}])
w("h-era.json", [{"title":"Wrong childhood","holiday_id":"halloween","post_date":"2026-10-28",
  "platform":"instagram","fact_id":"HAL-013","hook":"Halloweentown premiered in 1998.",
  "caption":"Debbie Reynolds was 66 when she played Aggie Cromwell. The character everyone remembers as the fearless one was a woman in her 60s, which is the whole point of the film.",
  "hashtags":["#gentlemuse"]}])
w("h-dash.json", [{"title":"Dash","holiday_id":"halloween","post_date":"2026-10-09","platform":"instagram",
  "fact_id":"HAL-002","hook":"Jack-o'-lanterns were turnips first — and that matters.",
  "caption":"Ireland and Scotland carved turnips and beets. The ritual survived because people let the tool change.",
  "hashtags":["#gentlemuse"]}])
PY7

hcheck "decade paraphrase accepted"   0 "$TMP/h-decade.json"
hcheck "explicit override allowed"    0 "$TMP/h-override.json" N01_OVERRIDE
hcheck "trivia with no turn fails"    1 "$TMP/h-noturn.json"   E09_NO_TURN
hcheck "em dash caught"               1 "$TMP/h-dash.json"     E10_EM_DASH
HARGS="--era 1989-1994"
hcheck "era break caught"             1 "$TMP/h-era.json"      E06_ERA_BREAK

"$PY" - "$TMP" "$BANK" <<'PY7'
import csv, os, sys
tmp, bank = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(bank, encoding="utf-8-sig")))
for row in rows:
    if row["FactID"] == "HAL-002":
        row["Source"] = ""
handle = open(os.path.join(tmp, "bank-nosource.csv"), "w", newline="", encoding="utf-8")
writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
writer.writeheader(); writer.writerows(rows)
PY7

out="$("$PY" "$HGATE" --post "$HERE/holiday.clean.json" --bank "$TMP/bank-nosource.csv" --calendar "$CAL" 2>&1)"
got=$?
if [ "$got" = 1 ] && grep -q E02_UNUSABLE_FACT <<<"$out"; then
  echo "PASS  sourceless fact cannot ship"; pass=$((pass+1))
else echo "FAIL  sourceless fact cannot ship"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

echo
echo "== holiday bank =="
expect_exit "audit passes the shipped bank" 0 "$PY" "$BANK_TOOL" --audit --bank "$BANK" --calendar "$CAL"
expect_exit "audit blocks a sourceless row" 1 "$PY" "$BANK_TOOL" --audit --bank "$TMP/bank-nosource.csv" --calendar "$CAL"

out="$("$PY" "$BANK_TOOL" --audit --bank "$BANK" --calendar "$CAL" 2>&1)"
missing=0
for want in "thanksgiving       2026-11-26" "black-friday       2026-11-27" \
            "easter             2026-04-05" "memorial-day       2026-05-25" \
            "mothers-day        2026-05-10" "labor-day          2026-09-07"; do
  grep -q "$want" <<<"$out" || { missing=1; echo "  missing date: $want"; }
done
if [ $missing = 0 ]; then echo "PASS  floating dates resolve for 2026"; pass=$((pass+1))
else echo "FAIL  floating dates resolve for 2026"; fail=$((fail+1)); fi

out="$("$PY" "$BANK_TOOL" --plan --from 2026-10-01 --to 2026-10-31 --per-holiday 5 \
      --bank "$BANK" --calendar "$CAL" --out "$TMP/plan.csv" 2>&1)"; got=$?
if [ "$got" = 0 ] && grep -q "5 posts planned" <<<"$out" && [ "$(wc -l < "$TMP/plan.csv")" = 6 ]; then
  echo "PASS  plan binds every post to a sourced fact"; pass=$((pass+1))
else echo "FAIL  plan binds every post to a sourced fact"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

head -1 "$BANK" > "$TMP/bank-empty.csv"
expect_exit "plan holds on an empty bank" 2 "$PY" "$BANK_TOOL" --plan --from 2026-10-01 \
      --to 2026-10-31 --bank "$TMP/bank-empty.csv" --calendar "$CAL"


"$PY" - "$TMP" "$BANK" <<'PY7'
import csv, os, sys
tmp, bank = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(bank, encoding="utf-8-sig")))
for row in rows:
    if row["FactID"] == "HAL-003":
        row["Delivery"] = "interpretive dance"
h = open(os.path.join(tmp, "bank-baddelivery.csv"), "w", newline="", encoding="utf-8")
w = csv.DictWriter(h, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
PY7

expect_exit "audit rejects a bad Delivery" 1 "$PY" "$BANK_TOOL" --audit \
      --bank "$TMP/bank-baddelivery.csv" --calendar "$CAL"

out="$("$PY" "$BANK_TOOL" --plan --from 2026-10-01 --to 2026-10-31 --per-holiday 8 \
      --bank "$BANK" --calendar "$CAL" 2>&1)"
if grep -q "What this plan needs filmed" <<<"$out" \
   && grep -q "can be finished with no footage at all" <<<"$out"; then
  echo "PASS  plan doubles as a shot list"; pass=$((pass+1))
else echo "FAIL  plan doubles as a shot list"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

# ---------------------------------------------------------------- Run 8
# Competitor teardowns, and the contract a reel has to declare before it is
# allowed to ask the viewer for anything.

echo
echo "== teardown bank =="
TGATE="$HERE/../scripts/gm_teardown_check.py"
TBANK="$HERE/../data/competitor-teardowns.csv"

expect_exit "shipped teardown bank passes" 0 "$PY" "$TGATE" --bank "$TBANK"

"$PY" - "$TMP" "$TBANK" <<'PY8'
import csv, os, sys
tmp, bank = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(bank, newline="", encoding="utf-8-sig")))
cols = list(rows[0].keys())

def dump(name, rs):
    h = open(os.path.join(tmp, name), "w", newline="", encoding="utf-8")
    w = csv.DictWriter(h, fieldnames=cols); w.writeheader(); w.writerows(rs)

# a listicle mention promoted to a finding
r = [dict(x) for x in rows]
for x in r:
    if x["Confidence"] == "listed":
        x["Verified"] = "yes"
dump("bank-listicle.csv", r)

# verified, but nobody wrote down where it came from
r = [dict(x) for x in rows]
r[0]["Evidence"] = ""
dump("bank-noevidence.csv", r)

# verified with a handle nobody confirmed
r = [dict(x) for x in rows]
r[0]["Handle"] = "unconfirmed"
dump("bank-placeholder.csv", r)

# the arithmetic does not hold
r = [dict(x) for x in rows]
r[0]["EngRate"] = "0.900"
dump("bank-engrate.csv", r)

# verified, but the promise was never named
r = [dict(x) for x in rows]
r[0]["Contract"] = ""
dump("bank-nocontract.csv", r)

# nothing in the bank has been read by anyone
r = [dict(x) for x in rows]
for x in r:
    x["Verified"] = "no"
dump("bank-allleads.csv", r)
PY8

expect_exit "listicle mention cannot be a finding" 1 "$PY" "$TGATE" --bank "$TMP/bank-listicle.csv"
expect_exit "verified row needs evidence"         1 "$PY" "$TGATE" --bank "$TMP/bank-noevidence.csv"
expect_exit "verified row needs a real handle"    1 "$PY" "$TGATE" --bank "$TMP/bank-placeholder.csv"
expect_exit "engagement rate must reconcile"      1 "$PY" "$TGATE" --bank "$TMP/bank-engrate.csv"
expect_exit "verified row must name the promise"  1 "$PY" "$TGATE" --bank "$TMP/bank-nocontract.csv"
expect_exit "a bank of leads only holds"          2 "$PY" "$TGATE" --bank "$TMP/bank-allleads.csv"

echo
echo "== the contract on a reel =="
"$PY" - "$TMP" <<'PY9'
import json, os, sys
tmp = sys.argv[1]
base = {"id": "T-1", "duration": 12.0, "delivery": "text", "keyword": "CESA",
        "beats": [{"in": 0, "out": 6, "html": "A line."},
                  {"in": 6, "out": 12, "cta": "The real one",
                   "html": "Somebody you know needs this one."}]}

def dump(name, doc):
    json.dump(doc, open(os.path.join(tmp, name), "w"))

dump("reel-nocontract.json", dict(base))
dump("reel-generic.json", dict(base, contract="Follow for more spooky facts."))
dump("reel-thin.json", dict(base, contract="History stuff."))
dump("reel-good.json", dict(base, contract=("Every holiday carries a fact somebody "
                                            "softened. I post the real one before "
                                            "the day arrives.")))
dump("reel-held.json", dict(base, contract=("Cesa is old and I am keeping the record "
                                            "while she is still here."),
                            holds=["Her age is unconfirmed."]))
PY9

expect_exit "a CTA with no contract is refused"   1 "$PY" "$TGATE" --render "$TMP/reel-nocontract.json"
expect_exit "follow for more is not a contract"   1 "$PY" "$TGATE" --render "$TMP/reel-generic.json"
expect_exit "a two word contract is refused"      1 "$PY" "$TGATE" --render "$TMP/reel-thin.json"
expect_exit "a real contract passes"              0 "$PY" "$TGATE" --render "$TMP/reel-good.json"
expect_exit "an unconfirmed claim holds"          2 "$PY" "$TGATE" --render "$TMP/reel-held.json"

"$PY" - "$TMP" <<'PY11'
import json, os, sys
tmp = sys.argv[1]
C = ("Every holiday carries a fact somebody softened. I post the real one "
     "before the day arrives.")
def dump(name, cta, html):
    json.dump({"id": "T-" + name, "duration": 12.0, "delivery": "text", "contract": C,
               "keyword": "CESA",
               "beats": [{"in": 0, "out": 6, "html": "Nobody was burned at Salem."},
                         {"in": 6, "out": 12, "cta": cta, "html": html}]},
              open(os.path.join(tmp, name + ".json"), "w"))
dump("cta-ask-label", "Share it", "Somebody you know still says burned. You can fix that now.")
dump("cta-ask-line",  "The real one", "Send this to whoever still says they were burned.")
dump("cta-deliver",   "The real one", "Somebody you know still says burned. You can fix that now.")
PY11

expect_exit "a request label is refused"          1 "$PY" "$TGATE" --render "$TMP/cta-ask-label.json"
expect_exit "a request line is refused"           1 "$PY" "$TGATE" --render "$TMP/cta-ask-line.json"
expect_exit "a delivery close passes"             0 "$PY" "$TGATE" --render "$TMP/cta-deliver.json"

"$PY" - "$TMP" <<'PY12'
import json, os, sys
tmp = sys.argv[1]
C = ("Every holiday carries a fact somebody softened. I post the real one "
     "before the day arrives.")
def dump(name, **extra):
    doc = {"id": "T-" + name, "duration": 12.0, "delivery": "text", "contract": C,
           "beats": [{"in": 0, "out": 6, "html": "Nobody was burned at Salem."},
                     {"in": 6, "out": 12, "cta": "The real one",
                      "html": "Somebody you know still says burned."}]}
    doc.update(extra)
    json.dump(doc, open(os.path.join(tmp, name + ".json"), "w"))
dump("kw-silent")
dump("kw-thin", keyword=None, keyword_gap="none")
dump("kw-named", keyword="CESA")
dump("kw-declared", keyword=None,
     keyword_gap="No live keyword matches this lane. The share close stands until one exists.")
PY12

expect_exit "silence about capture is refused"    1 "$PY" "$TGATE" --render "$TMP/kw-silent.json"
expect_exit "an empty gap note is refused"        1 "$PY" "$TGATE" --render "$TMP/kw-thin.json"
expect_exit "a named keyword passes"              0 "$PY" "$TGATE" --render "$TMP/kw-named.json"
expect_exit "a declared gap passes with a note"   0 "$PY" "$TGATE" --render "$TMP/kw-declared.json"
expect_exit "shipped reels declare a contract"    0 "$PY" "$TGATE" --render "$HERE/../../reel-factory/"

echo
echo "== the factory payloads reach the Run 6 gate =="
expect_exit "factory payloads bind and pass" 0 "$PY" "$GATE" \
      --render "$HERE/../../reel-factory/" --library "$HERE/../data/clip-library-drive.csv"

"$PY" - "$TMP" <<'PY10'
import json, os, sys
tmp = sys.argv[1]
# a plate bound with no reason given, and no metaphor declared
json.dump({"id": "T-2", "duration": 8.0,
           "clip": {"file": "clips/coffee-morning-pour-01.webm"},
           "beats": [{"in": 0, "out": 8, "html": "Hocus Pocus was a flop."}]},
          open(os.path.join(tmp, "factory-bare.json"), "w"))
# a typography cut that never says it is one
json.dump({"id": "T-3", "duration": 8.0,
           "beats": [{"in": 0, "out": 8, "html": "Nobody was burned at Salem."}]},
          open(os.path.join(tmp, "factory-silent.json"), "w"))
PY10

check "factory plate needs a stated reason" 1 "$TMP/factory-bare.json" E08_NO_MATCH_REASON E07_TOPIC_MISMATCH

"$PY" - "$TMP" <<'PY13'
import json, os, sys
tmp = sys.argv[1]
# home-landscape-window-01 is the horizontal clip in the sample library
base = {"id": "T-4", "duration": 8.0, "format": "9:16",
        "beats": [{"in": 0, "out": 8, "html": "A window in a quiet home."}]}
def dump(name, **clip):
    doc = dict(base)
    doc["clip"] = dict({"file": "clips/home-landscape-window-01.webm",
                        "match_reason": "The line is about a window and the clip is a window.",
                        }, **clip)
    json.dump(doc, open(os.path.join(tmp, name + ".json"), "w"))
dump("horiz-bare")
dump("horiz-thin", framed="cropped")
dump("horiz-framed", framed="Cover fitted to 1920 tall and shifted 120px right so the window clears the caption block.")
PY13

check "a horizontal plate is refused"      1 "$TMP/horiz-bare.json"  E06_ORIENTATION
check "a vague framing note is refused"    1 "$TMP/horiz-thin.json"  E06_ORIENTATION
check "a declared framing passes"          0 "$TMP/horiz-framed.json"
check "a typography cut must say so"        1 "$TMP/factory-silent.json" E00_NO_CLIPS

CTA="$HERE/../scripts/gm_cta_check.py"

cta() { # name expected_exit queue_file [expected_code ...]
  local name="$1" want="$2" q="$3"; shift 3
  local out; out="$("$PY" "$CTA" --queue "$q" 2>&1)"; local got=$?
  local ok=1
  [ "$got" = "$want" ] || { ok=0; echo "  exit $got, wanted $want"; }
  for code in "$@"; do
    grep -q "$code" <<<"$out" || { ok=0; echo "  missing finding: $code"; }
  done
  if [ $ok = 1 ]; then echo "PASS  $name"; pass=$((pass+1))
  else echo "FAIL  $name"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi
}

echo
echo "== cta gate =="
cta "a working call to action passes"   0 "$HERE/cta.clean.json"
cta "broken calls to action are caught" 1 "$HERE/cta.broken.json" \
    P01_DEAD_KEYWORD P02_WRONG_LINK P03_LINK_WITHOUT_MENTION P06_DUPLICATE_LINK P07_PROMISE_MISMATCH
cta "edge cases all fire"               1 "$HERE/cta.edge.json" \
    P00_UNKNOWN_ACCOUNT P01_DEAD_KEYWORD P04_NO_ACTION P05_NO_LINK
cta "a tiktok follow is a real return" 0 "$HERE/cta.tiktok.json"
cta "a reach only post holds"           2 "$HERE/cta.hold.json"   H01_NO_CAPTURE_PATH

REPOST="$HERE/../scripts/gm_repost_media_check.py"

repost() { # name expected_exit queue_file [expected_code ...]
  local name="$1" want="$2" q="$3"; shift 3
  local out; out="$("$PY" "$REPOST" --queue "$q" --published "$HERE/repost-published.json" \
                    --campaigns "$HERE/repost-campaigns.csv" 2>&1)"; local got=$?
  local ok=1
  [ "$got" = "$want" ] || { ok=0; echo "  exit $got, wanted $want"; }
  for pat in "$@"; do
    grep -q "$pat" <<<"$out" || { ok=0; echo "  missing: $pat"; }
  done
  if [ $ok = 1 ]; then echo "PASS  $name"; pass=$((pass+1))
  else echo "FAIL  $name"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi
}

echo
echo "== repost media check =="
repost "fresh media on a repeat and a campaign carousel both pass" 0 "$HERE/repost.clean.json"
repost "a repeat wearing its worn media and a scheduled twin are caught" 1 "$HERE/repost.broken.json" \
    R01_WORN_MEDIA_REPOST R02_TWIN_IN_SCHEDULE


PLAN="$HERE/../scripts/gm_queue_plan.py"

qplan() { # name expected_exit queue_file [grep ...]
  local name="$1" want="$2" q="$3"; shift 3
  local out; out="$("$PY" "$PLAN" --queue "$q" --start 2026-09-02 --days 1 2>&1)"; local got=$?
  local ok=1
  [ "$got" = "$want" ] || { ok=0; echo "  exit $got, wanted $want"; }
  for pat in "$@"; do
    grep -q "$pat" <<<"$out" || { ok=0; echo "  missing: $pat"; }
  done
  if [ $ok = 1 ]; then echo "PASS  $name"; pass=$((pass+1))
  else echo "FAIL  $name"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi
}

echo
echo "== queue plan =="
qplan "a day that matches the model passes" 0 "$HERE/queue.model.json" \
      "0 slots over, 0 slots under, 0 posts beyond"
qplan "drift in every direction is caught"  1 "$HERE/queue.drift.json" \
      "1 slots over" "2 slots under" "1 posts beyond" "1 on channels"


ANCH="$HERE/../scripts/gm_anchors.py"
DAILY="$HERE/../scripts/gm_queue_daily.py"

echo
echo "== holiday anchors =="
out="$("$PY" "$ANCH" --year 2026 2>&1)"
anch_ok=1
while read -r id want; do
  [ -z "$id" ] && continue
  got="$(grep -E "^$id " <<<"$out" | awk '{print $2}')"
  if [ "$got" != "$want" ]; then anch_ok=0; echo "  $id resolved $got, wanted $want"; fi
done < "$HERE/anchors.expected.txt"
if [ $anch_ok = 1 ]; then echo "PASS  every rule form resolves to the right date"; pass=$((pass+1))
else echo "FAIL  every rule form resolves to the right date"; fail=$((fail+1)); fi

# an offset rule must land 1 day after the holiday it hangs off
tg="$("$PY" "$ANCH" --year 2026 | grep -E "^thanksgiving " | awk '{print $2}')"
bf="$("$PY" "$ANCH" --year 2026 | grep -E "^black-friday " | awk '{print $2}')"
if [ "$(date -d "$tg +1 day" +%F 2>/dev/null)" = "$bf" ]; then
  echo "PASS  an offset rule hangs off its base"; pass=$((pass+1))
else echo "FAIL  an offset rule hangs off its base ($tg -> $bf)"; fail=$((fail+1)); fi

echo
echo "== daily routine =="
if "$PY" "$DAILY" --queue "$HERE/cta.clean.json" --today 2026-09-02 >/dev/null 2>&1; [ $? -le 1 ]; then
  echo "PASS  the daily pass runs end to end"; pass=$((pass+1))
else echo "FAIL  the daily pass runs end to end"; fail=$((fail+1)); fi

if "$PY" "$DAILY" --queue "$HERE/does-not-exist.json" --today 2026-09-02 >/dev/null 2>&1; [ $? = 2 ]; then
  echo "PASS  an unreadable queue exits 2 instead of guessing"; pass=$((pass+1))
else echo "FAIL  an unreadable queue exits 2 instead of guessing"; fail=$((fail+1)); fi


echo
echo "== cadence gate, 3 to 5 a day =="
CAD="$HERE/../scripts/gm_cadence_check.py"

if "$PY" "$CAD" "$HERE/cadence.clean.csv" >/dev/null 2>&1; then
  echo "PASS  4 posts spaced 2 hours apart passes clean"; pass=$((pass+1))
else echo "FAIL  4 posts spaced 2 hours apart passes clean"; fail=$((fail+1)); fi

if "$PY" "$CAD" "$HERE/cadence.overloaded.csv" 2>/dev/null | grep -q C01_DAY_OVER; then
  echo "PASS  a 6th post in a day is refused"; pass=$((pass+1))
else echo "FAIL  a 6th post in a day is refused"; fail=$((fail+1)); fi

if "$PY" "$CAD" "$HERE/cadence.overloaded.csv" 2>/dev/null | grep -q C01_DAY_STARVED; then
  echo "PASS  a day under 3 posts is flagged as starved"; pass=$((pass+1))
else echo "FAIL  a day under 3 posts is flagged as starved"; fail=$((fail+1)); fi

if "$PY" "$CAD" "$HERE/cadence.overloaded.csv" 2>/dev/null | grep -q C06_DEAD_HOUR; then
  echo "PASS  a post in the dead hours is caught"; pass=$((pass+1))
else echo "FAIL  a post in the dead hours is caught"; fail=$((fail+1)); fi

if "$PY" "$CAD" "$HERE/cadence.clean.csv" 2>/dev/null | grep -q C06_DEAD_HOUR; then
  echo "FAIL  19:00 Central is prime time, not a dead hour"; fail=$((fail+1))
else echo "PASS  19:00 Central is prime time, not a dead hour"; pass=$((pass+1)); fi

if "$PY" "$CAD" "$HERE/cadence.collision.csv" 2>/dev/null | grep -q C02_SLOT_COLLISION; then
  echo "PASS  2 posts in the same minute are caught"; pass=$((pass+1))
else echo "FAIL  2 posts in the same minute are caught"; fail=$((fail+1)); fi

if "$PY" "$CAD" "$HERE/cadence.tooclose.csv" 2>/dev/null | grep -q C05_TOO_CLOSE; then
  echo "PASS  2 posts inside 2 hours are caught"; pass=$((pass+1))
else echo "FAIL  2 posts inside 2 hours are caught"; fail=$((fail+1)); fi

if "$PY" "$CAD" "$HERE/cadence.countdown.csv" --target 2026-10-31 2>/dev/null | grep -q "D2"; then
  echo "PASS  a countdown that drifted off its date is caught"; pass=$((pass+1))
else echo "FAIL  a countdown that drifted off its date is caught"; fail=$((fail+1)); fi

if "$PY" "$CAD" "$HERE/cadence.board.csv" 2>/dev/null | grep -q "cadence clean"; then
  echo "PASS  4 platforms at 4 a day is a full board, not an overload"; pass=$((pass+1))
else echo "FAIL  4 platforms at 4 a day is a full board, not an overload"
     "$PY" "$CAD" "$HERE/cadence.board.csv" 2>&1 | sed 's/^/      /'; fail=$((fail+1)); fi

if "$PY" "$CAD" "$HERE/cadence.board.csv" 2>/dev/null | grep -q "C02_SLOT_COLLISION"; then
  echo "FAIL  2 platforms at the same minute is not a collision"; fail=$((fail+1))
else echo "PASS  2 platforms at the same minute is not a collision"; pass=$((pass+1)); fi

if "$PY" "$CAD" "$HERE/cadence.twoaccounts.csv" 2>/dev/null | grep -q "cadence clean"; then
  echo "PASS  2 accounts on 1 platform are counted apart"; pass=$((pass+1))
else echo "FAIL  2 accounts on 1 platform are counted apart"
     "$PY" "$CAD" "$HERE/cadence.twoaccounts.csv" 2>&1 | sed 's/^/      /'; fail=$((fail+1)); fi

if "$PY" "$CAD" "$HERE/cadence.board.csv" 2>/dev/null | grep -q "instagram .*4.0 a day"; then
  echo "PASS  the summary reports each platform, not one total"; pass=$((pass+1))
else echo "FAIL  the summary reports each platform, not one total"; fail=$((fail+1)); fi

echo
echo "== channel rules (added 09/08) =="
# 3 to 5 is not the rule everywhere. LinkedIn is 1 a day and always
# business. X was dropped. The rule lives in data/channel-rules.csv so it
# can be read and changed without touching the gate.
if "$PY" "$CAD" "$HERE/cadence.channels.csv" 2>/dev/null | grep -q "cadence clean"; then
  echo "PASS  LinkedIn at 1 a day is clean, not starved"; pass=$((pass+1))
else echo "FAIL  LinkedIn at 1 a day is clean, not starved"
     "$PY" "$CAD" "$HERE/cadence.channels.csv" 2>&1 | sed 's/^/      /'; fail=$((fail+1)); fi

if "$PY" "$CAD" "$HERE/cadence.channels-broken.csv" 2>/dev/null | grep -q "C01_DAY_OVER.*linkedin"; then
  echo "PASS  a 2nd LinkedIn post in a day is caught"; pass=$((pass+1))
else echo "FAIL  a 2nd LinkedIn post in a day is caught"; fail=$((fail+1)); fi

if "$PY" "$CAD" "$HERE/cadence.channels-broken.csv" 2>/dev/null | grep -q "C07_RETIRED_CHANNEL"; then
  echo "PASS  scheduling to a dropped channel is caught"; pass=$((pass+1))
else echo "FAIL  scheduling to a dropped channel is caught"; fail=$((fail+1)); fi

if grep -q "^twitter,.*,0,0," "$HERE/../data/channel-rules.csv"; then
  echo "PASS  X is recorded as dropped, in data not prose"; pass=$((pass+1))
else echo "FAIL  X is recorded as dropped, in data not prose"; fail=$((fail+1)); fi

echo
echo "== media reachability (Run 6, added 09/08) =="
# A clip row can be complete and still be unusable: the footage is on a
# machine the renderer has never seen. Describing a shot is not having it.
MR="$HERE/media-reach.library.csv"
MRROOT="$HERE/media-reach-root"
expect_exit "a local plate that is on disk passes" 0 \
  env GM_MEDIA_ROOT="$MRROOT" "$PY" "$GATE" --render "$HERE/media-reach.present.json"  --library "$MR" --quiet
expect_exit "a local plate that is not on disk is refused" 1 \
  env GM_MEDIA_ROOT="$MRROOT" "$PY" "$GATE" --render "$HERE/media-reach.missing.json"  --library "$MR" --quiet
expect_exit "footage that only exists on the phone is refused" 1 \
  env GM_MEDIA_ROOT="$MRROOT" "$PY" "$GATE" --render "$HERE/media-reach.offline.json"  --library "$MR" --quiet
expect_exit "a clip with no MediaState passes with a note" 0 \
  env GM_MEDIA_ROOT="$MRROOT" "$PY" "$GATE" --render "$HERE/media-reach.unstated.json" --library "$MR" --quiet

if env GM_MEDIA_ROOT="$MRROOT" "$PY" "$GATE" --render "$HERE/media-reach.offline.json" \
     --library "$MR" 2>&1 | grep -q E11_MEDIA_UNREACHABLE; then
  echo "PASS  unreachable footage is named by rule, not just refused"; pass=$((pass+1))
else echo "FAIL  unreachable footage is named by rule, not just refused"; fail=$((fail+1)); fi

if env GM_MEDIA_ROOT="$MRROOT" "$PY" "$GATE" --render "$HERE/media-reach.offline.json" \
     --library "$MR" 2>&1 | grep -q "D:.Phone Backup"; then
  echo "PASS  the refusal says where the footage actually is"; pass=$((pass+1))
else echo "FAIL  the refusal says where the footage actually is"; fail=$((fail+1)); fi

echo
echo "== a composition that ignores the plate (Run 6, added 09/08) =="
# reel.html draws embers and no footage. A payload that binds a clip must
# not render there: it succeeds, and the missing footage looks deliberate.
RF="$HERE/../../reel-factory"
if grep -q "__consumes_plate = false" "$RF/reel.html"; then
  echo "PASS  the typography cut declares it draws no footage"; pass=$((pass+1))
else echo "FAIL  the typography cut declares it draws no footage"; fail=$((fail+1)); fi

if grep -q "__consumes_plate = true" "$RF/reel-footage.html"; then
  echo "PASS  the footage cut declares it draws footage"; pass=$((pass+1))
else echo "FAIL  the footage cut declares it draws footage"; fail=$((fail+1)); fi

if grep -q "declaresClip && !state.consumesPlate" "$RF/build.mjs"; then
  echo "PASS  the build refuses a bound clip on a plateless composition"; pass=$((pass+1))
else echo "FAIL  the build refuses a bound clip on a plateless composition"; fail=$((fail+1)); fi

echo
echo "== a beat that wrapped past its own line breaks (Run 6, added 09/08) =="
# 11 of 26 beats shipped with an orphaned word on its own line. The words
# were right, the card was not, and only looking at it caught that.
if grep -q "__overflow" "$RF/reel-footage.html"; then
  echo "PASS  the composition counts drawn lines against asked lines"; pass=$((pass+1))
else echo "FAIL  the composition counts drawn lines against asked lines"; fail=$((fail+1)); fi

if grep -q "wrapped past their own line breaks" "$RF/build.mjs"; then
  echo "PASS  the build refuses a beat that wrapped"; pass=$((pass+1))
else echo "FAIL  the build refuses a beat that wrapped"; fail=$((fail+1)); fi

if grep -q "shorten the line, or move the break" -i "$RF/build.mjs"; then
  echo "PASS  the refusal says what to do about it"; pass=$((pass+1))
else echo "FAIL  the refusal says what to do about it"; fail=$((fail+1)); fi

echo
echo "== portability, so the suite is not red on one machine (added 09/08) =="

# 1. The interpreter. gm_py.sh has already run by the time we get here.
if [ -n "${PY:-}" ] && "$PY" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)' >/dev/null 2>&1; then
  echo "PASS  gm_py.sh resolved something that runs Python 3"; pass=$((pass+1))
else
  echo "FAIL  gm_py.sh resolved something that runs Python 3"
  echo "      PY=${PY:-<unset>}"; fail=$((fail+1))
fi

# 2. The trap that cost 09/08. On Windows the name python3 IS on PATH: it is a
# Microsoft Store alias stub that prints an install message and exits non-zero.
# So `command -v python3` succeeds and every call then fails. Only running a
# candidate can tell a real interpreter from a stub. Prove the resolver still
# does, by putting a stub named python3 in front of it.
STUB="$TMP/stubbin"; mkdir -p "$STUB"
REAL="$("$PY" -c 'import sys; print(sys.executable)')"
printf '#!/usr/bin/env bash\necho "Python was not found; run without arguments to install from the Microsoft Store" >&2\nexit 9009\n' > "$STUB/python3"
printf '#!/usr/bin/env bash\nexec "%s" "$@"\n' "$REAL" > "$STUB/python"
chmod +x "$STUB/python3" "$STUB/python"
picked="$(PATH="$STUB:$PATH" PY="" bash -c '. "$1" >/dev/null 2>&1 && printf "%s" "$PY"' _ "$HERE/../scripts/gm_py.sh" 2>/dev/null)"
if [ -n "$picked" ] && PATH="$STUB:$PATH" "$picked" -c 'raise SystemExit(0)' >/dev/null 2>&1; then
  echo "PASS  a stub named python3 is stepped over, not trusted"; pass=$((pass+1))
else
  echo "FAIL  a stub named python3 is stepped over, not trusted"
  echo "      resolver picked: ${picked:-<nothing>}"; fail=$((fail+1))
fi

# 3. The other half of 09/08. A fixture checked out CRLF makes a gate compare a
# value against the same value plus a carriage return, and the mismatch prints
# as two identical strings because a CR only moves the cursor. .gitattributes
# pins the tree to LF; this is what says so out loud if that ever slips.
#
# This runs in Python rather than grep on purpose. Cygwin and Git Bash grep read
# in text mode and strip the CR before matching, so `grep $'\r'` finds nothing on
# the one platform where the problem actually happens.
crlf="$("$PY" - "$HERE/.." <<'PYCRLF'
import os, sys
root = sys.argv[1]
exts = (".csv", ".txt", ".json", ".sh", ".py", ".md")
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in ("__pycache__", "node_modules", ".git")]
    for name in filenames:
        if not name.endswith(exts):
            continue
        path = os.path.join(dirpath, name)
        try:
            with open(path, "rb") as fh:
                if b"\r" in fh.read():
                    print(os.path.relpath(path, root).replace(os.sep, "/"))
        except OSError:
            pass
PYCRLF
)"
if [ -z "$crlf" ]; then
  echo "PASS  no gate input is checked out with CRLF"; pass=$((pass+1))
else
  echo "FAIL  no gate input is checked out with CRLF"
  echo "$crlf" | sed 's|^|      filing-system/|'
  echo "      .gitattributes pins these to LF. Refresh the tree with:"
  echo "        git rm --cached -r -q . && git reset --hard"
  fail=$((fail+1))
fi

echo
echo "$pass passed, $fail failed"
[ "$fail" = 0 ]
