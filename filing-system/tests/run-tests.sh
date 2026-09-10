#!/usr/bin/env bash
# Regression suite for Run 6 (caption to clip binding) and Run 7 (holiday captions).
# Run from the repo root:  bash filing-system/tests/run-tests.sh
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
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

hcheck() { # name expected_exit post_file [expected_code ...]   HARGS adds gate flags
  local name="$1" want="$2" post="$3"; shift 3
  local out; out="$(python3 "$HGATE" --post "$post" --bank "$BANK" --calendar "$CAL" $HARGS 2>&1)"; local got=$?
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

python3 - "$TMP" <<'PY7'
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

python3 - "$TMP" "$BANK" <<'PY7'
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

out="$(python3 "$HGATE" --post "$HERE/holiday.clean.json" --bank "$TMP/bank-nosource.csv" --calendar "$CAL" 2>&1)"
got=$?
if [ "$got" = 1 ] && grep -q E02_UNUSABLE_FACT <<<"$out"; then
  echo "PASS  sourceless fact cannot ship"; pass=$((pass+1))
else echo "FAIL  sourceless fact cannot ship"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

echo
echo "== holiday bank =="
expect_exit "audit passes the shipped bank" 0 python3 "$BANK_TOOL" --audit --bank "$BANK" --calendar "$CAL"
expect_exit "audit blocks a sourceless row" 1 python3 "$BANK_TOOL" --audit --bank "$TMP/bank-nosource.csv" --calendar "$CAL"

out="$(python3 "$BANK_TOOL" --audit --bank "$BANK" --calendar "$CAL" 2>&1)"
missing=0
for want in "thanksgiving       2026-11-26" "black-friday       2026-11-27" \
            "easter             2026-04-05" "memorial-day       2026-05-25" \
            "mothers-day        2026-05-10" "labor-day          2026-09-07"; do
  grep -q "$want" <<<"$out" || { missing=1; echo "  missing date: $want"; }
done
if [ $missing = 0 ]; then echo "PASS  floating dates resolve for 2026"; pass=$((pass+1))
else echo "FAIL  floating dates resolve for 2026"; fail=$((fail+1)); fi

out="$(python3 "$BANK_TOOL" --plan --from 2026-10-01 --to 2026-10-31 --per-holiday 5 \
      --bank "$BANK" --calendar "$CAL" --out "$TMP/plan.csv" 2>&1)"; got=$?
if [ "$got" = 0 ] && grep -q "5 posts planned" <<<"$out" && [ "$(wc -l < "$TMP/plan.csv")" = 6 ]; then
  echo "PASS  plan binds every post to a sourced fact"; pass=$((pass+1))
else echo "FAIL  plan binds every post to a sourced fact"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

head -1 "$BANK" > "$TMP/bank-empty.csv"
expect_exit "plan holds on an empty bank" 2 python3 "$BANK_TOOL" --plan --from 2026-10-01 \
      --to 2026-10-31 --bank "$TMP/bank-empty.csv" --calendar "$CAL"


python3 - "$TMP" "$BANK" <<'PY7'
import csv, os, sys
tmp, bank = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(bank, encoding="utf-8-sig")))
for row in rows:
    if row["FactID"] == "HAL-003":
        row["Delivery"] = "interpretive dance"
h = open(os.path.join(tmp, "bank-baddelivery.csv"), "w", newline="", encoding="utf-8")
w = csv.DictWriter(h, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
PY7

expect_exit "audit rejects a bad Delivery" 1 python3 "$BANK_TOOL" --audit \
      --bank "$TMP/bank-baddelivery.csv" --calendar "$CAL"

out="$(python3 "$BANK_TOOL" --plan --from 2026-10-01 --to 2026-10-31 --per-holiday 8 \
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

expect_exit "shipped teardown bank passes" 0 python3 "$TGATE" --bank "$TBANK"

python3 - "$TMP" "$TBANK" <<'PY8'
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

expect_exit "listicle mention cannot be a finding" 1 python3 "$TGATE" --bank "$TMP/bank-listicle.csv"
expect_exit "verified row needs evidence"         1 python3 "$TGATE" --bank "$TMP/bank-noevidence.csv"
expect_exit "verified row needs a real handle"    1 python3 "$TGATE" --bank "$TMP/bank-placeholder.csv"
expect_exit "engagement rate must reconcile"      1 python3 "$TGATE" --bank "$TMP/bank-engrate.csv"
expect_exit "verified row must name the promise"  1 python3 "$TGATE" --bank "$TMP/bank-nocontract.csv"
expect_exit "a bank of leads only holds"          2 python3 "$TGATE" --bank "$TMP/bank-allleads.csv"

echo
echo "== the contract on a reel =="
python3 - "$TMP" <<'PY9'
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

expect_exit "a CTA with no contract is refused"   1 python3 "$TGATE" --render "$TMP/reel-nocontract.json"
expect_exit "follow for more is not a contract"   1 python3 "$TGATE" --render "$TMP/reel-generic.json"
expect_exit "a two word contract is refused"      1 python3 "$TGATE" --render "$TMP/reel-thin.json"
expect_exit "a real contract passes"              0 python3 "$TGATE" --render "$TMP/reel-good.json"
expect_exit "an unconfirmed claim holds"          2 python3 "$TGATE" --render "$TMP/reel-held.json"

python3 - "$TMP" <<'PY11'
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

expect_exit "a request label is refused"          1 python3 "$TGATE" --render "$TMP/cta-ask-label.json"
expect_exit "a request line is refused"           1 python3 "$TGATE" --render "$TMP/cta-ask-line.json"
expect_exit "a delivery close passes"             0 python3 "$TGATE" --render "$TMP/cta-deliver.json"

python3 - "$TMP" <<'PY12'
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

expect_exit "silence about capture is refused"    1 python3 "$TGATE" --render "$TMP/kw-silent.json"
expect_exit "an empty gap note is refused"        1 python3 "$TGATE" --render "$TMP/kw-thin.json"
expect_exit "a named keyword passes"              0 python3 "$TGATE" --render "$TMP/kw-named.json"
expect_exit "a declared gap passes with a note"   0 python3 "$TGATE" --render "$TMP/kw-declared.json"
expect_exit "shipped reels declare a contract"    0 python3 "$TGATE" --render "$HERE/../../reel-factory/"

echo
echo "== the factory payloads reach the Run 6 gate =="
expect_exit "factory payloads bind and pass" 0 python3 "$GATE" \
      --render "$HERE/../../reel-factory/" --library "$HERE/../data/clip-library-drive.csv"

python3 - "$TMP" <<'PY10'
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

python3 - "$TMP" <<'PY13'
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
  local out; out="$(python3 "$CTA" --queue "$q" 2>&1)"; local got=$?
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

# 2026-08-21: 4 paid and promotional posts inside 3 minutes took 2, 0, 0 and 0
# likes. The spacing rule was already written down and nothing read it at ship.
cta "the Aug 21 paid stack is refused"  1 "$HERE/cta.paid.json" P08_PAID_STACKED
cta "paid posts spaced out pass"        0 "$HERE/cta.paid-clean.json"
cta "paid with no run time holds"       2 "$HERE/cta.paid-notime.json" H02_PAID_NO_TIME

# the stack is 3 posts, so 2 consecutive pairs are too close, not 1.
out="$(python3 "$CTA" --queue "$HERE/cta.paid.json" 2>&1)"
if [ "$(grep -c P08_PAID_STACKED <<<"$out")" = 2 ]; then
  echo "PASS  every close pair is reported, not just the first"; pass=$((pass+1))
else echo "FAIL  every close pair is reported, not just the first"; fail=$((fail+1)); fi

# a shorter window is a different question, and the flag has to actually change it.
out="$(python3 "$CTA" --queue "$HERE/cta.paid-clean.json" --paid-window 600 2>&1)"
if grep -q P08_PAID_STACKED <<<"$out"; then
  echo "PASS  --paid-window widens the rule"; pass=$((pass+1))
else echo "FAIL  --paid-window widens the rule"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

# 2026-09-09: a business pitch landed under a Cesa video and the audience
# turned on it. Amanda's rule: the business products and Cesa never mix.
cta "a business link on the cesa account is refused" 1 "$HERE/cta.cesa-zone.json" P09_CESA_ZONE
cta "a business keyword on the cesa account is refused even unwired" 1 "$HERE/cta.cesa-zone.json" \
    P01_DEAD_KEYWORD P09_CESA_ZONE
cta "cesa content with cesa links passes"            0 "$HERE/cta.cesa-ok.json"
cta "cesa content with a business link elsewhere holds" 2 "$HERE/cta.crossover.json" H03_CESA_CROSSOVER


PLAN="$HERE/../scripts/gm_queue_plan.py"

qplan() { # name expected_exit queue_file [grep ...]
  local name="$1" want="$2" q="$3"; shift 3
  local out; out="$(python3 "$PLAN" --queue "$q" --start 2026-09-02 --days 1 2>&1)"; local got=$?
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
out="$(python3 "$ANCH" --year 2026 2>&1)"
anch_ok=1
while read -r id want; do
  [ -z "$id" ] && continue
  got="$(grep -E "^$id " <<<"$out" | awk '{print $2}')"
  if [ "$got" != "$want" ]; then anch_ok=0; echo "  $id resolved $got, wanted $want"; fi
done < "$HERE/anchors.expected.txt"
if [ $anch_ok = 1 ]; then echo "PASS  every rule form resolves to the right date"; pass=$((pass+1))
else echo "FAIL  every rule form resolves to the right date"; fail=$((fail+1)); fi

# an offset rule must land 1 day after the holiday it hangs off
tg="$(python3 "$ANCH" --year 2026 | grep -E "^thanksgiving " | awk '{print $2}')"
bf="$(python3 "$ANCH" --year 2026 | grep -E "^black-friday " | awk '{print $2}')"
if [ "$(date -d "$tg +1 day" +%F 2>/dev/null)" = "$bf" ]; then
  echo "PASS  an offset rule hangs off its base"; pass=$((pass+1))
else echo "FAIL  an offset rule hangs off its base ($tg -> $bf)"; fail=$((fail+1)); fi

echo
echo "== daily routine =="
if python3 "$DAILY" --queue "$HERE/cta.clean.json" --today 2026-09-02 >/dev/null 2>&1; [ $? -le 1 ]; then
  echo "PASS  the daily pass runs end to end"; pass=$((pass+1))
else echo "FAIL  the daily pass runs end to end"; fail=$((fail+1)); fi

if python3 "$DAILY" --queue "$HERE/does-not-exist.json" --today 2026-09-02 >/dev/null 2>&1; [ $? = 2 ]; then
  echo "PASS  an unreadable queue exits 2 instead of guessing"; pass=$((pass+1))
else echo "FAIL  an unreadable queue exits 2 instead of guessing"; fail=$((fail+1)); fi



RELAY="$HERE/../scripts/gm_symphony.py"
STUB="$HERE/symphony-stub.py"
PORT=8973

echo
echo "== symphony relay =="

python3 "$STUB" "$PORT" >/dev/null 2>&1 &
STUB_PID=$!
trap 'kill $STUB_PID 2>/dev/null; rm -rf "$TMP"' EXIT
for _ in $(seq 1 30); do
  python3 -c "import socket,sys;s=socket.socket();sys.exit(s.connect_ex(('127.0.0.1',$PORT)))" && break
  sleep 0.2
done

relay() { # name expected_exit env_token args... ; greps come after a --
  local name="$1" want="$2" tok="$3"; shift 3
  local args=() greps=()
  while [ $# -gt 0 ] && [ "$1" != "--" ]; do args+=("$1"); shift; done
  [ "${1:-}" = "--" ] && shift
  greps=("$@")
  local out
  out="$(SYMPHONY_BASE="http://127.0.0.1:$PORT" SYMPHONY_TOKEN="$tok" \
         python3 "$RELAY" --wait 6 --interval 1 "${args[@]}" 2>&1)"
  local got=$?
  local ok=1
  [ "$got" = "$want" ] || { ok=0; echo "  exit $got, wanted $want"; }
  for pat in "${greps[@]}"; do
    grep -qi -e "$pat" <<<"$out" || { ok=0; echo "  missing: $pat"; }
  done
  if [ $ok = 1 ]; then echo "PASS  $name"; pass=$((pass+1))
  else echo "FAIL  $name"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi
}

# rule 1, propose only. A bare run must not reach the network at all.
relay "nothing is sent without --send"        0 "tok-abc" \
      --message "book the call" -- "PROPOSED" "Nothing was sent"

# rule 5, no substitution. No token means stop, not send unsigned.
relay "no token stops instead of sending"     2 "" \
      --message "book the call" --send -- "SYMPHONY_TOKEN is not set" "Nothing was sent"

relay "an answer comes back clean"            0 "tok-abc" \
      --message "book the call" --send -- "Booked" "Tuesday at 10"

# the failure this tool exists for: success on the wire, no work done.
relay "the credit wall is not read as work"   1 "tok-abc" \
      --message "WALL book the call" --send -- "THIS IS NOT AN ANSWER" \
      "credit limit" "Do not record it as done"

relay "a deferred answer is collected"        0 "tok-abc" \
      --message "SLOW book the call" --send -- "Three follow ups"

relay "silence times out, does not hang"      2 "tok-abc" \
      --message "NEVER book the call" --send -- "did not answer" "--resume"

relay "a rejected token says how to fix it"   2 "tok-abc" \
      --message "AUTH book the call" --send -- "HTTP 401" "Reissue it"

relay "resume collects an open conversation"  0 "tok-abc" \
      --resume c-slow -- "Three follow ups"

relay "an empty message is refused"           2 "tok-abc" \
      --message "   " --send -- "no message"

# a reply that describes instead of reporting is the wall in a politer register.
relay "a capability blurb is caught"          1 "tok-abc" \
      --message "PROSE what is on my calendar" --send --expect-data -- \
      "THIS IS NOT AN ANSWER" "describes what it can do" "0 particulars"

# the false positive that would make the check untrustworthy. Prose is the
# right answer to a question that wanted prose, so without the flag it passes.
relay "the same blurb passes without the flag" 0 "tok-abc" \
      --message "PROSE what should I post Tuesday" --send -- "stay on top"

relay "an honest refusal is still no data"     1 "tok-abc" \
      --message "NOACC what is on my calendar" --send --expect-data -- \
      "THIS IS NOT AN ANSWER" "unproven rather than delivered"

# real particulars that happen to close with an offer of help must pass.
relay "an answer that offers help still passes" 0 "tok-abc" \
      --message "MIXED what is on my calendar" --send --expect-data -- "CESA drop"

relay "a clean answer passes with the flag on" 0 "tok-abc" \
      --message "book the call" --send --expect-data -- "Booked"

# Symphony's real refusal register, captured 09/09. The original hedge list
# matched none of it.
relay "the observed refusal voice is caught" 1 "tok-abc" \
      --message "VOICE what are my recent posts" --send --expect-data -- \
      "THIS IS NOT AN ANSWER" "unproven rather than delivered"

# the wall is the more specific finding, so it wins when both fire.
relay "the wall outranks the blurb"           1 "tok-abc" \
      --message "WPROSE what is on my calendar" --send --expect-data -- \
      "credit limit"

# the token must never reach the terminal, on any path.
leak=0
for m in "book the call" "AUTH book the call" "WALL book the call"; do
  out="$(SYMPHONY_BASE="http://127.0.0.1:$PORT" SYMPHONY_TOKEN="s3cr3t-tok" \
         python3 "$RELAY" --message "$m" --send --wait 4 --interval 1 2>&1)"
  grep -q "s3cr3t-tok" <<<"$out" && { leak=1; echo "  leaked on: $m"; }
done
if [ $leak = 0 ]; then echo "PASS  the token never reaches the terminal"; pass=$((pass+1))
else echo "FAIL  the token never reaches the terminal"; fail=$((fail+1)); fi

kill $STUB_PID 2>/dev/null
trap 'rm -rf "$TMP"' EXIT


echo
echo "$pass passed, $fail failed"
[ "$fail" = 0 ]
