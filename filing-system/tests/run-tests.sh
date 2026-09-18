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

# Run 9 taught the offer ladder that a number with nobody named as its source
# becomes next quarter's fact. The same hole was open here: a reviewer's guess
# at a competitor's price read exactly like a price the company publishes.
python3 - "$TMP" "$TBANK" <<'PY8B'
import csv, os, sys
tmp, bank = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(bank, newline="", encoding="utf-8-sig")))
cols = list(rows[0].keys())

def dump(name, rs):
    h = open(os.path.join(tmp, name), "w", newline="", encoding="utf-8")
    w = csv.DictWriter(h, fieldnames=cols); w.writeheader(); w.writerows(rs)

def find(rs, tid):
    return next(x for x in rs if x["TeardownID"] == tid)

# CT-015 carries a $499 price and a third-party $8,500
r = [dict(x) for x in rows]; find(r, "CT-015")["ClaimStatus"] = ""
dump("bank-noclaim.csv", r)

r = [dict(x) for x in rows]; find(r, "CT-015")["ClaimStatus"] = "probably true"
dump("bank-badclaim.csv", r)

# CT-005 carries no audience or money figure, so it may stay blank
r = [dict(x) for x in rows]; find(r, "CT-005")["ClaimStatus"] = ""
dump("bank-nofigure.csv", r)

# the column itself going missing is a schema failure, not a silent pass
r = [dict(x) for x in rows]
c2 = [c for c in cols if c != "ClaimStatus"]
h = open(os.path.join(tmp, "bank-noclaimcol.csv"), "w", newline="", encoding="utf-8")
w = csv.DictWriter(h, fieldnames=c2, extrasaction="ignore")
w.writeheader(); w.writerows(r)
PY8B

tb() { # name expected_exit bank [expected_code ...]
  local name="$1" want="$2" bank="$3"; shift 3
  local out; out="$(python3 "$TGATE" --bank "$bank" 2>&1)"; local got=$?
  local ok=1
  [ "$got" = "$want" ] || { ok=0; echo "  exit $got, wanted $want"; }
  for code in "$@"; do
    grep -q "$code" <<<"$out" || { ok=0; echo "  missing finding: $code"; }
  done
  if [ $ok = 1 ]; then echo "PASS  $name"; pass=$((pass+1))
  else echo "FAIL  $name"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi
}

tb "a figure with no named source is refused" 1 "$TMP/bank-noclaim.csv"    T10_NO_CLAIM_STATUS
tb "an unknown ClaimStatus is refused"        1 "$TMP/bank-badclaim.csv"   T11_BAD_CLAIM_STATUS
tb "a row with no figure may leave it blank"  0 "$TMP/bank-nofigure.csv"
tb "the column going missing is caught"       1 "$TMP/bank-noclaimcol.csv" T09_SCHEMA

# The research that drove the pivot is in the bank, graded rather than trusted.
out="$(python3 "$TGATE" --bank "$TBANK" 2>&1)"
if grep -q "14 of 22 rows are backed by an artifact somebody read" <<<"$out"; then
  echo "PASS  the bank separates what was read from what was listed"; pass=$((pass+1))
else echo "FAIL  the bank separates what was read from what was listed"
     echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

# Afnan is the row the whole pivot rests on, and her money claims are disputed.
row="$(grep '^CT-012' "$TBANK")"
if grep -q "disputed" <<<"$row" && grep -q "reported" <<<"$row"; then
  echo "PASS  the pivot's source row is graded disputed"; pass=$((pass+1))
else echo "FAIL  the pivot's source row is graded disputed"; fail=$((fail+1)); fi

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
      "1 slots over" "4 slots under" "1 posts beyond" "1 on channels"


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


# ---------------------------------------------------------------- Run 9
# The offer ladder, and the price a caption is never allowed to carry.

OFFER="$HERE/../scripts/gm_offer_check.py"
OLADDER="$HERE/../data/offer-ladder.csv"

ofr() { # name expected_exit mode arg [expected_code ...]
  local name="$1" want="$2" mode="$3" arg="$4"; shift 4
  local out; out="$(python3 "$OFFER" "$mode" "$arg" 2>&1)"; local got=$?
  local ok=1
  [ "$got" = "$want" ] || { ok=0; echo "  exit $got, wanted $want"; }
  for code in "$@"; do
    grep -q "$code" <<<"$out" || { ok=0; echo "  missing finding: $code"; }
  done
  if [ $ok = 1 ]; then echo "PASS  $name"; pass=$((pass+1))
  else echo "FAIL  $name"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi
}

echo
echo "== offer ladder =="

# The shipped ladder does not pass, and that is the point of shipping it. It
# named the 2 products nobody can find and the 2 rungs that led nowhere. The
# 2 rungs were fixed on 09/18, so L05 is gone from the shipped ladder and is
# exercised against a synthesised one below. What remains is the Method's
# missing parts, and a credit on the Plan that no buyer has been told about.
ofr "the shipped ladder names its own gaps" 1 --ladder "$OLADDER" \
    L04_UNVERIFIED_COMPONENT H02_CREDIT_UNPUBLISHED
ofr "a reprice is held for Amanda, not failed" 1 --ladder "$OLADDER" H01_REPRICE_PENDING

python3 - "$TMP" "$OLADDER" <<'PY9'
import csv, os, sys
tmp, src = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(src, newline="", encoding="utf-8-sig")))
cols = list(rows[0].keys())

def dump(name, rs):
    h = open(os.path.join(tmp, name), "w", newline="", encoding="utf-8")
    w = csv.DictWriter(h, fieldnames=cols); w.writeheader(); w.writerows(rs)

def find(rs, oid):
    return next(r for r in rs if r["OfferID"] == oid)

r = [dict(x) for x in rows]; find(r, "OF-002")["Evidence"] = ""
dump("ladder-noevidence.csv", r)

r = [dict(x) for x in rows]; find(r, "OF-002")["PriceStatus"] = "maybe"
dump("ladder-badfield.csv", r)

# two rungs answering to one comment
r = [dict(x) for x in rows]; find(r, "OF-002")["Keyword"] = "BOTTLENECK"
dump("ladder-collision.csv", r)

# the same number on two rungs, which is how one price came to mean two things
r = [dict(x) for x in rows]
x = find(r, "OF-002"); x["Price"] = "750"; x["Unit"] = "once"
dump("ladder-sameprice.csv", r)

# a rung crediting toward something that is not on the ladder
r = [dict(x) for x in rows]; find(r, "OF-002")["CreditsToward"] = "OF-999"
dump("ladder-badref.csv", r)

# live, with no keyword and no URL, so nobody can reach it
r = [dict(x) for x in rows]
x = find(r, "OF-002"); x["Keyword"] = ""; x["URL"] = ""
dump("ladder-nopath.csv", r)
PY9

ofr "a rung with no evidence is refused"    1 --ladder "$TMP/ladder-noevidence.csv" L01_NO_EVIDENCE
ofr "an unknown PriceStatus is refused"     1 --ladder "$TMP/ladder-badfield.csv"   L02_BAD_FIELD
ofr "two rungs on one keyword are refused"  1 --ladder "$TMP/ladder-collision.csv"  L03_KEYWORD_COLLISION
ofr "one price on two rungs is refused"     1 --ladder "$TMP/ladder-sameprice.csv"  L06_PRICE_COLLISION
ofr "a reference that resolves to nothing"  1 --ladder "$TMP/ladder-badref.csv"     L07_UNKNOWN_REF
ofr "a live rung with no way in is refused" 1 --ladder "$TMP/ladder-nopath.csv"     L08_NO_PATH

echo
echo "== the price a caption may not carry =="

# The launch pack shipped a caption naming an hourly rate and an application
# form naming a price that has never been published.
ofr "the launch pack prices are refused" 1 --queue "$HERE/offer.launchpack.json" \
    Q01_PRICE_IN_CAPTION Q02_UNAPPROVED_PRICE

python3 - "$TMP" <<'PY9'
import json, os, sys
tmp = sys.argv[1]
def w(name, rows): json.dump(rows, open(os.path.join(tmp, name), "w"))
w("price-clean.json", [
  {"id": "cap", "surface": "caption",
   "text": "Comment BOTTLENECK and I will send the free check."},
  {"id": "page", "surface": "page",
   "text": "The Decision Map is $47, and you send voice notes instead of booking a call."}])
w("price-onscreen.json", [
  {"id": "vo", "surface": "voiceover", "text": "It is 47 dollars and it is worth it."}])
w("price-unknown.json", [
  {"id": "pg", "surface": "page", "text": "The Intensive is $2,400."}])
w("price-surface.json", [
  {"id": "odd", "surface": "billboard", "text": "Anything."}])
PY9

ofr "a live price on a page passes"        0 --queue "$TMP/price-clean.json"
ofr "a price spoken aloud is refused"      1 --queue "$TMP/price-onscreen.json" Q01_PRICE_IN_CAPTION
ofr "a price on no rung is refused"        1 --queue "$TMP/price-unknown.json" Q03_UNKNOWN_PRICE
ofr "an undeclared surface is refused"     1 --queue "$TMP/price-surface.json" Q04_BAD_SURFACE

echo
echo "== the tables against the platform =="
ofr "drift from live is caught" 1 --sync "$HERE/offer.sync-drift.json" \
    S01_NOT_LIVE S03_ACCOUNT_DRIFT S04_PRICE_DRIFT S05_URL_DRIFT

out="$(python3 "$OFFER" --sync "$HERE/offer.sync-drift.json" --scope GUIDE 2>&1)"
if grep -q S03_ACCOUNT_DRIFT <<<"$out" && ! grep -q S05_URL_DRIFT <<<"$out"; then
  echo "PASS  --scope narrows the comparison"; pass=$((pass+1))
else echo "FAIL  --scope narrows the comparison"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

echo
echo "== a keyword that was never a keyword =="
cta "comment WAITLIST is refused"      1 "$HERE/cta.waitlist.json" P10_INVENTED_KEYWORD
cta "an unpublished keyword is refused" 1 "$HERE/cta.waitlist.json" P09_DRAFT_KEYWORD

# the whole reason P10 exists: every other check here reads the map, so a word
# that is in no map row was never looked at by anything.
out="$(python3 "$CTA" --queue "$HERE/cta.waitlist.json" 2>&1)"
if grep -q "WAITLIST is in no automation" <<<"$out"; then
  echo "PASS  the invented keyword is named, not just counted"; pass=$((pass+1))
else echo "FAIL  the invented keyword is named, not just counted"; fail=$((fail+1)); fi

# ---------------------------------------------------------------- Run 10
# The message as a table, and the lane as a field.

POSGATE="$HERE/../scripts/gm_position_check.py"

pos() { # name expected_exit mode [arg] -- greps
  local name="$1" want="$2"; shift 2
  local args=() greps=()
  while [ $# -gt 0 ] && [ "$1" != "--" ]; do args+=("$1"); shift; done
  [ "${1:-}" = "--" ] && shift
  greps=("$@")
  local out; out="$(python3 "$POSGATE" "${args[@]}" 2>&1)"; local got=$?
  local ok=1
  [ "$got" = "$want" ] || { ok=0; echo "  exit $got, wanted $want"; }
  for code in "${greps[@]}"; do
    grep -q "$code" <<<"$out" || { ok=0; echo "  missing finding: $code"; }
  done
  if [ $ok = 1 ]; then echo "PASS  $name"; pass=$((pass+1))
  else echo "FAIL  $name"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi
}

echo
echo "== the message =="
pos "the shipped positioning passes" 0 --position
pos "the shipped rotation passes"    0 --rotation

python3 - "$TMP" "$HERE/../data" <<'PY10'
import csv, os, sys
tmp, data = sys.argv[1], sys.argv[2]

def dump(name, rows, cols):
    h = open(os.path.join(tmp, name), "w", newline="", encoding="utf-8")
    w = csv.DictWriter(h, fieldnames=cols); w.writeheader(); w.writerows(rows)

pos = list(csv.DictReader(open(os.path.join(data, "brand-position.csv"),
                               newline="", encoding="utf-8-sig")))
pcols = list(pos[0].keys())

r = [dict(x) for x in pos]
next(x for x in r if x["PosID"] == "POS-004")["Source"] = ""
dump("pos-nosource.csv", r, pcols)

r = [dict(x) for x in pos]
next(x for x in r if x["PosID"] == "POS-004")["Field"] = "vibes"
dump("pos-badfield.csv", r, pcols)

# the guarantee going missing is how a promise quietly stops being one
r = [x for x in pos if x["PosID"] != "POS-004"]
dump("pos-noguarantee.csv", r, pcols)

rot = list(csv.DictReader(open(os.path.join(data, "rotation-magnet.csv"),
                               newline="", encoding="utf-8-sig")))
rcols = list(rot[0].keys())

# the old week gave 2 of 7 slots to the dog guide
r = [dict(x) for x in rot]
sat = next(x for x in r if x["Weekday"] == "Saturday")
sat["Keyword"] = "PRINCESS"; sat["Magnet"] = "19 Years Old, 10 of Them Mine"
dump("rot-cesa.csv", r, rcols)

r = [dict(x) for x in rot]
next(x for x in r if x["Weekday"] == "Monday")["Serves"] = ""
dump("rot-nomessage.csv", r, rcols)

r = [dict(x) for x in rot]
next(x for x in r if x["Weekday"] == "Monday")["Format"] = "F-FREESTYLE"
dump("rot-noformat.csv", r, rcols)

r = [dict(x) for x in rot]
next(x for x in r if x["Weekday"] == "Monday")["Keyword"] = "RETAINER"
dump("rot-draftkw.csv", r, rcols)
PY10

pos "a claim with no source is refused"  1 --position --position-file "$TMP/pos-nosource.csv" -- M02_NO_SOURCE
pos "an unknown field is refused"        1 --position --position-file "$TMP/pos-badfield.csv" -- M03_BAD_FIELD
pos "losing the guarantee is caught"     1 --position --position-file "$TMP/pos-noguarantee.csv" -- M05_MISSING_FIELD

echo
echo "== the lane =="
# The failure this run exists for: 2 of 7 slots pointed at a free dog guide
# while the 2 products that take money had no slot at all.
pos "a Cesa keyword in Amanda's week is refused" 1 --rotation \
    --rotation-file "$TMP/rot-cesa.csv" -- R01_LANE_LEAK
pos "a slot serving no message is refused"       1 --rotation \
    --rotation-file "$TMP/rot-nomessage.csv" -- R03_NO_MESSAGE
pos "a slot with no rails is refused"            1 --rotation \
    --rotation-file "$TMP/rot-noformat.csv" -- R02_UNKNOWN_FORMAT
pos "an unpublished keyword in the week is caught" 1 --rotation \
    --rotation-file "$TMP/rot-draftkw.csv" -- R04_DEAD_KEYWORD

python3 - "$TMP" <<'PY10B'
import json, os, sys
tmp = sys.argv[1]
json.dump([
 {"id": "leak-cesa", "accountId": "45886",
  "text": "She is 19 today. Comment PRINCESS and I will send the guide."},
 {"id": "leak-biz", "accountId": "65540",
  "text": "Comment BOTTLENECK and I will send the free check."},
 {"id": "ok-amanda", "accountId": "45886",
  "text": "Comment BOTTLENECK and I will send the free check."},
 {"id": "ok-cesa", "accountId": "65540",
  "text": "Comment PRINCESS and I will send the guide."},
], open(os.path.join(tmp, "lane.json"), "w"))
PY10B

pos "both directions of lane leak are caught" 1 --queue "$TMP/lane.json" -- Q01_LANE_LEAK

out="$(python3 "$POSGATE" --queue "$TMP/lane.json" 2>&1)"
if [ "$(grep -c Q01_LANE_LEAK <<<"$out")" = 2 ] \
   && ! grep -q "ok-amanda" <<<"$out" && ! grep -q "ok-cesa" <<<"$out"; then
  echo "PASS  a post in its own lane passes clean"; pass=$((pass+1))
else echo "FAIL  a post in its own lane passes clean"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

# Every weekday now names a live keyword and the 2 paid products finally have one.
wk="$(cut -d, -f4 "$HERE/../data/rotation-magnet.csv" | tail -n +2 | sort -u | tr '\n' ' ')"
if grep -q BUDGET <<<"$wk" && grep -q DECISION <<<"$wk" && ! grep -q CESA <<<"$wk"; then
  echo "PASS  the paid products are in the week and the dog guide is not"; pass=$((pass+1))
else echo "FAIL  the paid products are in the week and the dog guide is not ($wk)"; fail=$((fail+1)); fi

# ---------------------------------------------------------------- Run 11
# Brand deals are first class, the capitalised keyword is caught, and the week
# has to actually get filmed.

echo
echo "== every live keyword, not just the magnets =="

python3 - "$TMP" <<'PY11'
import json, os, sys
tmp = sys.argv[1]
def w(n, rows): json.dump(rows, open(os.path.join(tmp, n), "w"))

# 23 affiliate keywords and 13 PR screening phrases are live capture paths.
# Refusing them as invented would block every brand deal Amanda runs.
w("kw-affiliate.json", [
  {"id":"bloom","platform":"instagram","accountId":"45886","at":"2026-09-20T15:00:00Z",
   "text":"#ad This is the one I actually keep buying. Comment BLOOM and I will send the link."},
  {"id":"bracelet","platform":"facebook","accountId":"30840","at":"2026-09-20T19:00:00Z",
   "text":"Comment BRACELET and I will send you the link."}])

# The word comment starts most sentences, so it usually arrives capitalised.
w("kw-case.json", [
  {"id":"lower","platform":"instagram","accountId":"45886","at":"2026-09-20T15:00:00Z",
   "text":"If that is you, comment WAITLIST and I will add you."},
  {"id":"upper","platform":"instagram","accountId":"45886","at":"2026-09-20T17:00:00Z",
   "text":"Comment WAITLIST and I will add you."}])

base = [{"id":d,"accountId":"45886","delivery":"face",
         "text":"Comment %s and I will send it." % k}
        for d,k in (("mon","BOTTLENECK"),("tue","TUESDAY"),("wed","GUIDE"),
                    ("thu","BUDGET"),("fri","DECISION"),("sat","RESET"),("sun","TUESDAY"))]
filmed = [dict(r, delivery=("face" if r["id"] in ("mon","tue","wed","thu") else "text"))
          for r in base]
w("week-filmed.json", filmed)
w("week-filler.json", [dict(r, delivery=("face" if r["id"]=="mon" else "text")) for r in base])
w("week-silent.json", [{k:v for k,v in r.items() if k != "delivery"} for r in base])
PY11

cta "a live affiliate keyword passes"      0 "$TMP/kw-affiliate.json"
cta "a capitalised invented keyword fails" 1 "$TMP/kw-case.json" P10_INVENTED_KEYWORD

out="$(python3 "$CTA" --queue "$TMP/kw-case.json" 2>&1)"
if [ "$(grep -c P10_INVENTED_KEYWORD <<<"$out")" = 2 ]; then
  echo "PASS  both cases of comment are caught"; pass=$((pass+1))
else echo "FAIL  both cases of comment are caught"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

# Every keyword the platform answers should be in the table, with its kind.
kinds="$(python3 -c "
import csv,sys
print(' '.join(sorted({r['Kind'] for r in csv.DictReader(open(sys.argv[1],newline='',encoding='utf-8-sig'))})))
" "$HERE/../data/magnet-map.csv")"
if grep -q magnet <<<"$kinds" && grep -q offer <<<"$kinds" \
   && grep -q affiliate <<<"$kinds" && grep -q screening <<<"$kinds"; then
  echo "PASS  the map knows all 4 kinds of keyword"; pass=$((pass+1))
else echo "FAIL  the map knows all 4 kinds of keyword ($kinds)"; fail=$((fail+1)); fi

echo
echo "== the week has to get filmed =="
pos "a filmed week passes"              0 --week "$TMP/week-filmed.json"
pos "a week of filler is refused"       1 --week "$TMP/week-filler.json" -- W01_FACE_FLOOR
pos "undeclared delivery holds"         2 --week "$TMP/week-silent.json" -- H03_NO_DELIVERY

# the floor is a flag, and it has to actually move
out="$(python3 "$POSGATE" --week "$TMP/week-filmed.json" --face-floor 7 2>&1)"
if grep -q W01_FACE_FLOOR <<<"$out"; then
  echo "PASS  --face-floor raises the bar"; pass=$((pass+1))
else echo "FAIL  --face-floor raises the bar"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

# the money question: where the asks actually went
out="$(python3 "$POSGATE" --week "$TMP/week-filmed.json" 2>&1)"
if grep -q "the asks went to" <<<"$out" && grep -q "offer" <<<"$out"; then
  echo "PASS  the week reports where the asks went"; pass=$((pass+1))
else echo "FAIL  the week reports where the asks went"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

# every slot states what it prefers and what it falls back to
nface="$(python3 -c "
import csv,sys
rows=list(csv.DictReader(open(sys.argv[1],newline='',encoding='utf-8-sig')))
print(sum(1 for r in rows if r['Delivery']=='face' and r['Filler']))
" "$HERE/../data/rotation-magnet.csv")"
if [ "$nface" = 7 ]; then
  echo "PASS  every slot prefers face and names its filler"; pass=$((pass+1))
else echo "FAIL  every slot prefers face and names its filler"; fail=$((fail+1)); fi

# ------------------------------------------------- the 09/18 production change
# CLEANUP was published at $750 and the CESA automations were retired from
# Amanda's Instagram and Facebook, on her explicit approval. Cesa's own channel
# was left alone. These cases exist so none of that drifts back silently.

echo
echo "== the split, as shipped =="

python3 - "$TMP" <<'PY12'
import json, os, sys
tmp = sys.argv[1]
def w(n, rows): json.dump(rows, open(os.path.join(tmp, n), "w"))

w("shipped-cesa.json", [
  {"id":"cesa-on-gm","platform":"instagram","accountId":"45886","at":"2026-09-20T15:00:00Z",
   "text":"She turned 19 this week. Comment CESA and I will send the guide. https://cesa-guide.subscribepage.io"},
  {"id":"cesa-on-hers","platform":"instagram","accountId":"65540","at":"2026-09-20T23:00:00Z",
   "text":"She turned 19 this week. Comment CESA and I will send the guide. https://cesa-guide.subscribepage.io"}])

w("shipped-price.json", [
  {"id":"plan-page","surface":"page",
   "text":"The Chaos Cleanup Plan is $750, paid once."},
  {"id":"intensive-page","surface":"page",
   "text":"The Intensive is $3,000."}])
PY12

out="$(python3 "$CTA" --queue "$TMP/shipped-cesa.json" 2>&1)"
if grep -q "P01_DEAD_KEYWORD *cesa-on-gm" <<<"$out" \
   && ! grep -q "cesa-on-hers" <<<"$out"; then
  echo "PASS  CESA is dead on Amanda's channel and alive on Cesa's"; pass=$((pass+1))
else echo "FAIL  CESA is dead on Amanda's channel and alive on Cesa's"
     echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

# $750 shipped, so it may appear on a page. $3,000 has not, so it may not.
out="$(python3 "$OFFER" --queue "$TMP/shipped-price.json" 2>&1)"
if ! grep -q "plan-page" <<<"$out" && grep -q "Q02_UNAPPROVED_PRICE *intensive-page" <<<"$out"; then
  echo "PASS  a published price may ship and a proposed one may not"; pass=$((pass+1))
else echo "FAIL  a published price may ship and a proposed one may not"
     echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

# the ladder should agree that the Plan is live
liv="$(python3 -c "
import csv,sys
r=[x for x in csv.DictReader(open(sys.argv[1],newline='',encoding='utf-8-sig')) if x['OfferID']=='OF-004'][0]
print(r['PriceStatus'], r['Status'])
" "$HERE/../data/offer-ladder.csv")"
if [ "$liv" = "live live" ]; then
  echo "PASS  the ladder records the Plan as live"; pass=$((pass+1))
else echo "FAIL  the ladder records the Plan as live (got: $liv)"; fail=$((fail+1)); fi

# ------------------------------------------------------------ the bridge
# Every account on the strategy bench that converts credits the first purchase
# toward the next tier. Contrarian Thinking credits $2,000, Hello Seven credits
# $497. Amanda's $37 and $47 credited toward nothing until 09/18.

echo
echo "== the bridge =="

# the 2 entry products now lead somewhere, so L05 is silent on both
out="$(python3 "$OFFER" --ladder "$OLADDER" 2>&1)"
if ! grep -q "L05_NO_BRIDGE *OF-002" <<<"$out" && ! grep -q "L05_NO_BRIDGE *OF-003" <<<"$out"; then
  echo "PASS  the \$37 and \$47 lead somewhere"; pass=$((pass+1))
else echo "FAIL  the \$37 and \$47 lead somewhere"; echo "$out" | sed 's/^/      /'; fail=$((fail+1)); fi

# and the credit is one a buyer has actually been told about
crd="$(python3 -c "
import csv,sys
rows={r['OfferID']:r for r in csv.DictReader(open(sys.argv[1],newline='',encoding='utf-8-sig'))}
print(' '.join('%s:%s>%s' % (i, rows[i]['CreditStatus'], rows[i]['CreditsToward'])
               for i in ('OF-002','OF-003')))
" "$OLADDER")"
if [ "$crd" = "OF-002:live>OF-004 OF-003:live>OF-004" ]; then
  echo "PASS  both credits are published, not just recorded"; pass=$((pass+1))
else echo "FAIL  both credits are published, not just recorded (got: $crd)"; fail=$((fail+1)); fi

python3 - "$TMP" "$OLADDER" <<'PY13'
import csv, os, sys
tmp, src = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(src, newline="", encoding="utf-8-sig")))
cols = list(rows[0].keys())

def dump(name, rs):
    h = open(os.path.join(tmp, name), "w", newline="", encoding="utf-8")
    w = csv.DictWriter(h, fieldnames=cols); w.writeheader(); w.writerows(rs)

# a credit written into the table and told to nobody
r = [dict(x) for x in rows]
next(x for x in r if x["OfferID"] == "OF-002")["CreditStatus"] = "proposed"
dump("ladder-creditunseen.csv", r)

r = [dict(x) for x in rows]
next(x for x in r if x["OfferID"] == "OF-002")["CreditStatus"] = "maybe"
dump("ladder-badcredit.csv", r)

# and the failure this whole run existed to clear
r = [dict(x) for x in rows]
for x in r:
    if x["OfferID"] in ("OF-002", "OF-003"):
        x["CreditsToward"] = ""; x["CreditStatus"] = "none"
dump("ladder-nobridge.csv", r)
PY13

# exit 1, not 2: the shipped ladder also carries the Method's unverified parts,
# which are a failure. H02 itself is a hold and the code has to appear.
ofr "a credit nobody was told is named"  1 --ladder "$TMP/ladder-creditunseen.csv" H02_CREDIT_UNPUBLISHED
ofr "an unknown CreditStatus is refused" 1 --ladder "$TMP/ladder-badcredit.csv"   L02_BAD_FIELD
ofr "removing the bridge is caught"     1 --ladder "$TMP/ladder-nobridge.csv"     L05_NO_BRIDGE

echo
echo "$pass passed, $fail failed"
[ "$fail" = 0 ]
