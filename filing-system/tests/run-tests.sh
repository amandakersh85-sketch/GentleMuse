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

REPOST="$HERE/../scripts/gm_repost_media_check.py"

repost() { # name expected_exit queue_file [expected_code ...]
  local name="$1" want="$2" q="$3"; shift 3
  local out; out="$(python3 "$REPOST" --queue "$q" --published "$HERE/repost-published.json" \
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


echo
echo "== cadence gate, 3 to 5 a day =="
CAD="$HERE/../scripts/gm_cadence_check.py"

if python3 "$CAD" "$HERE/cadence.clean.csv" >/dev/null 2>&1; then
  echo "PASS  4 posts spaced 2 hours apart passes clean"; pass=$((pass+1))
else echo "FAIL  4 posts spaced 2 hours apart passes clean"; fail=$((fail+1)); fi

if python3 "$CAD" "$HERE/cadence.overloaded.csv" 2>/dev/null | grep -q C01_DAY_OVER; then
  echo "PASS  a 6th post in a day is refused"; pass=$((pass+1))
else echo "FAIL  a 6th post in a day is refused"; fail=$((fail+1)); fi

if python3 "$CAD" "$HERE/cadence.overloaded.csv" 2>/dev/null | grep -q C01_DAY_STARVED; then
  echo "PASS  a day under 3 posts is flagged as starved"; pass=$((pass+1))
else echo "FAIL  a day under 3 posts is flagged as starved"; fail=$((fail+1)); fi

if python3 "$CAD" "$HERE/cadence.overloaded.csv" 2>/dev/null | grep -q C06_DEAD_HOUR; then
  echo "PASS  a post in the dead hours is caught"; pass=$((pass+1))
else echo "FAIL  a post in the dead hours is caught"; fail=$((fail+1)); fi

if python3 "$CAD" "$HERE/cadence.clean.csv" 2>/dev/null | grep -q C06_DEAD_HOUR; then
  echo "FAIL  19:00 Central is prime time, not a dead hour"; fail=$((fail+1))
else echo "PASS  19:00 Central is prime time, not a dead hour"; pass=$((pass+1)); fi

if python3 "$CAD" "$HERE/cadence.collision.csv" 2>/dev/null | grep -q C02_SLOT_COLLISION; then
  echo "PASS  2 posts in the same minute are caught"; pass=$((pass+1))
else echo "FAIL  2 posts in the same minute are caught"; fail=$((fail+1)); fi

if python3 "$CAD" "$HERE/cadence.tooclose.csv" 2>/dev/null | grep -q C05_TOO_CLOSE; then
  echo "PASS  2 posts inside 2 hours are caught"; pass=$((pass+1))
else echo "FAIL  2 posts inside 2 hours are caught"; fail=$((fail+1)); fi

if python3 "$CAD" "$HERE/cadence.countdown.csv" --target 2026-10-31 2>/dev/null | grep -q "D2"; then
  echo "PASS  a countdown that drifted off its date is caught"; pass=$((pass+1))
else echo "FAIL  a countdown that drifted off its date is caught"; fail=$((fail+1)); fi

if python3 "$CAD" "$HERE/cadence.board.csv" 2>/dev/null | grep -q "cadence clean"; then
  echo "PASS  4 platforms at 4 a day is a full board, not an overload"; pass=$((pass+1))
else echo "FAIL  4 platforms at 4 a day is a full board, not an overload"
     python3 "$CAD" "$HERE/cadence.board.csv" 2>&1 | sed 's/^/      /'; fail=$((fail+1)); fi

if python3 "$CAD" "$HERE/cadence.board.csv" 2>/dev/null | grep -q "C02_SLOT_COLLISION"; then
  echo "FAIL  2 platforms at the same minute is not a collision"; fail=$((fail+1))
else echo "PASS  2 platforms at the same minute is not a collision"; pass=$((pass+1)); fi

if python3 "$CAD" "$HERE/cadence.twoaccounts.csv" 2>/dev/null | grep -q "cadence clean"; then
  echo "PASS  2 accounts on 1 platform are counted apart"; pass=$((pass+1))
else echo "FAIL  2 accounts on 1 platform are counted apart"
     python3 "$CAD" "$HERE/cadence.twoaccounts.csv" 2>&1 | sed 's/^/      /'; fail=$((fail+1)); fi

if python3 "$CAD" "$HERE/cadence.board.csv" 2>/dev/null | grep -q "instagram .*4.0 a day"; then
  echo "PASS  the summary reports each platform, not one total"; pass=$((pass+1))
else echo "FAIL  the summary reports each platform, not one total"; fail=$((fail+1)); fi

echo
echo "== channel rules (added 09/08) =="
# 3 to 5 is not the rule everywhere. LinkedIn is 1 a day and always
# business. X was dropped. The rule lives in data/channel-rules.csv so it
# can be read and changed without touching the gate.
if python3 "$CAD" "$HERE/cadence.channels.csv" 2>/dev/null | grep -q "cadence clean"; then
  echo "PASS  LinkedIn at 1 a day is clean, not starved"; pass=$((pass+1))
else echo "FAIL  LinkedIn at 1 a day is clean, not starved"
     python3 "$CAD" "$HERE/cadence.channels.csv" 2>&1 | sed 's/^/      /'; fail=$((fail+1)); fi

if python3 "$CAD" "$HERE/cadence.channels-broken.csv" 2>/dev/null | grep -q "C01_DAY_OVER.*linkedin"; then
  echo "PASS  a 2nd LinkedIn post in a day is caught"; pass=$((pass+1))
else echo "FAIL  a 2nd LinkedIn post in a day is caught"; fail=$((fail+1)); fi

if python3 "$CAD" "$HERE/cadence.channels-broken.csv" 2>/dev/null | grep -q "C07_RETIRED_CHANNEL"; then
  echo "PASS  scheduling to a dropped channel is caught"; pass=$((pass+1))
else echo "FAIL  scheduling to a dropped channel is caught"; fail=$((fail+1)); fi

if grep -q "^twitter,.*,0,0," "$HERE/../data/channel-rules.csv"; then
  echo "PASS  X is recorded as dropped, in data not prose"; pass=$((pass+1))
else echo "FAIL  X is recorded as dropped, in data not prose"; fail=$((fail+1)); fi

echo
echo "== a channel with nothing on it (added 09/08) =="
# Every rule above groups the rows it was given, so a channel with no rows
# makes no group and gets no finding. Pinterest sat at 0 posts for 11 days
# and the board reported clean, while Amanda could see the empty channel
# with her own eyes. Absence has to be checked against the roster, not the
# file.
if python3 "$CAD" "$HERE/cadence.silent.csv" 2>/dev/null | grep -q "C11_CHANNEL_SILENT.*pinterest"; then
  echo "PASS  a channel scheduled to post and holding nothing is caught"; pass=$((pass+1))
else echo "FAIL  a channel scheduled to post and holding nothing is caught"
     python3 "$CAD" "$HERE/cadence.silent.csv" 2>&1 | sed 's/^/      /'; fail=$((fail+1)); fi

if python3 "$CAD" "$HERE/cadence.silent.csv" 2>/dev/null | grep -q "C11_CHANNEL_SILENT.*linkedin"; then
  echo "PASS  a 1 a day channel missing a single day is caught"; pass=$((pass+1))
else echo "FAIL  a 1 a day channel missing a single day is caught"; fail=$((fail+1)); fi

# A channel that is posting its full cadence is not silent.
if python3 "$CAD" "$HERE/cadence.silent.csv" 2>/dev/null | grep -q "C11_CHANNEL_SILENT.*youtube"; then
  echo "FAIL  a channel posting every day is not called silent"; fail=$((fail+1))
else echo "PASS  a channel posting every day is not called silent"; pass=$((pass+1)); fi

# 1 post held for Halloween must not make every channel look silent for the
# 6 weeks in between. The window ends at the first real gap.
if python3 "$CAD" "$HERE/cadence.tail.csv" 2>/dev/null | grep -q "of the 1 days"; then
  echo "PASS  a lone post far out does not stretch the window"; pass=$((pass+1))
else echo "FAIL  a lone post far out does not stretch the window"
     python3 "$CAD" "$HERE/cadence.tail.csv" 2>&1 | grep C11 | sed 's/^/      /'; fail=$((fail+1)); fi

# X is set to 0 a day. Silence there is the point, not a finding.
if python3 "$CAD" "$HERE/cadence.silent.csv" 2>/dev/null | grep -q "C11_CHANNEL_SILENT.*twitter"; then
  echo "FAIL  a retired channel is not called silent"; fail=$((fail+1))
else echo "PASS  a retired channel is not called silent"; pass=$((pass+1)); fi

echo
echo "== filling an empty day without repeating too soon (added 09/10) =="
# The board holds about 17 distinct video facts, so filling an empty day is
# almost always a re-air. Amanda, 09/10: "re-air is fine after 4+ days".
# The picker is only as good as the history it checks, and a history that
# cannot be read produces a confident wrong answer rather than an error.
FP="$HERE/../scripts/gm_fill_plan.py"

if python3 "$FP" --day 2026-09-20 --history "$HERE/fill.history.json" \
     --queue "$HERE/../data/queue-2026-09-10-backfill.json" >/dev/null 2>&1; then
  echo "PASS  an empty day is filled from a readable history"; pass=$((pass+1))
else echo "FAIL  an empty day is filled from a readable history"
     python3 "$FP" --day 2026-09-20 --history "$HERE/fill.history.json" \
       --queue "$HERE/../data/queue-2026-09-10-backfill.json" 2>&1 | sed 's/^/      /'; fail=$((fail+1)); fi

# The 09/10 near miss: a dump that had lost its caption text made every fact
# read as never aired, and the plan put a fact on YouTube 1 day after it runs.
if python3 "$FP" --day 2026-09-20 --history "$HERE/fill.history-blind.json" \
     --queue "$HERE/../data/queue-2026-09-10-backfill.json" 2>&1 | grep -q "carry no text"; then
  echo "PASS  a history with no captions is refused, not guessed at"; pass=$((pass+1))
else echo "FAIL  a history with no captions is refused, not guessed at"; fail=$((fail+1)); fi

# The same failure 1 step along: a history that stops before the day being
# filled cannot see what was scheduled in between.
if python3 "$FP" --day 2026-09-25 --history "$HERE/fill.history.json" \
     --queue "$HERE/../data/queue-2026-09-10-backfill.json" 2>&1 | grep -q "history stops at"; then
  echo "PASS  a history that stops short of the day is refused"; pass=$((pass+1))
else echo "FAIL  a history that stops short of the day is refused"; fail=$((fail+1)); fi

echo
echo "== where the board runs dry (added 09/09) =="
# The cap is a fixed number of slots, so a post held for Halloween owns its
# slot for 7 weeks. That filled the queue on 09/08 while the next 11 days
# starved, and the nightly backfill tried it again on 09/09: every row left
# in the backlog was dated Oct 12 or later while the board was about to go
# dark on Sep 19. Scheduling oldest first is what does it, because the
# oldest waiting row is the furthest from useful.
if python3 "$CAD" "$HERE/cadence.runway.csv" 2>/dev/null | grep -q "51 empty day"; then
  echo "PASS  the hole between the board and its tail is measured"; pass=$((pass+1))
else echo "FAIL  the hole between the board and its tail is measured"
     python3 "$CAD" "$HERE/cadence.runway.csv" 2>&1 | grep C12 | sed 's/^/      /'; fail=$((fail+1)); fi

if python3 "$CAD" "$HERE/cadence.runway.csv" 2>/dev/null | grep -q "1 slot(s) are held past the hole"; then
  echo "PASS  slots held on the far side of the hole are counted"; pass=$((pass+1))
else echo "FAIL  slots held on the far side of the hole are counted"; fail=$((fail+1)); fi

# Running dry is information, not a defect. A board with no tail must not
# fail the gate for simply having an end.
if python3 "$CAD" "$HERE/cadence.runway-notail.csv" 2>/dev/null | grep -q "runway ends 2026-09-09"; then
  echo "PASS  a board with no tail reports its runway without failing"; pass=$((pass+1))
else echo "FAIL  a board with no tail reports its runway without failing"; fail=$((fail+1)); fi

if python3 "$CAD" "$HERE/cadence.runway-notail.csv" 2>/dev/null | grep -q "C12_RUNWAY_END"; then
  echo "FAIL  running dry with nothing held past it is not a finding"; fail=$((fail+1))
else echo "PASS  running dry with nothing held past it is not a finding"; pass=$((pass+1)); fi

echo
echo "== fact repeats (added 09/08, after the queue ran 1 fact 6 times) =="
# The board counted posts and called itself healthy while YouTube carried
# the same Disney reel on 6 of 11 days and TikTok ran 1 fact twice in a day.
# Nothing recorded what a post was about, so nothing could see it. The fix
# is the fact column and these 3 rules, not a reminder to vary the queue.
if python3 "$CAD" "$HERE/cadence.facts.csv" 2>/dev/null | grep -q "cadence clean"; then
  echo "PASS  a board with spaced facts is clean"; pass=$((pass+1))
else echo "FAIL  a board with spaced facts is clean"
     python3 "$CAD" "$HERE/cadence.facts.csv" 2>&1 | sed 's/^/      /'; fail=$((fail+1)); fi

if python3 "$CAD" "$HERE/cadence.facts-broken.csv" 2>/dev/null | grep -q "C08_FACT_TWICE"; then
  echo "PASS  the same fact twice on 1 channel in 1 day is caught"; pass=$((pass+1))
else echo "FAIL  the same fact twice on 1 channel in 1 day is caught"; fail=$((fail+1)); fi

# Amanda, 09/10: "re-air is fine after 4+ days". Spacing is the rule and the
# count is not capped, so a 3rd airing 5 days out is correct, not a finding.
if python3 "$CAD" "$HERE/cadence.thrice.csv" 2>/dev/null | grep -qE "^C09"; then
  echo "FAIL  a 3rd airing spaced 5 days is allowed"; fail=$((fail+1))
else echo "PASS  a 3rd airing spaced 5 days is allowed"; pass=$((pass+1)); fi

if python3 "$CAD" "$HERE/cadence.facts-broken.csv" 2>/dev/null | grep -q "Minimum is 4 days"; then
  echo "PASS  2 airings closer than 4 days is caught"; pass=$((pass+1))
else echo "FAIL  2 airings closer than 4 days is caught"
     python3 "$CAD" "$HERE/cadence.facts-broken.csv" 2>&1 | grep C09 | sed 's/^/      /'; fail=$((fail+1)); fi

# A check that quietly skips the rows it cannot read is worse than no check.
if python3 "$CAD" "$HERE/cadence.facts-broken.csv" 2>/dev/null | grep -q "C10_FACT_UNLABELLED"; then
  echo "PASS  a row with no fact fails rather than passing unchecked"; pass=$((pass+1))
else echo "FAIL  a row with no fact fails rather than passing unchecked"; fail=$((fail+1)); fi

# Pinterest is the 1 channel where repeating is the mechanism. A pin is a
# bookmark, so repinning the same image is how the platform works, and the
# gate flagging it was enforcing a rule the house policy already exempts.
if python3 "$CAD" "$HERE/cadence.exempt.csv" 2>/dev/null | grep -qE "^C0[89]"; then
  echo "FAIL  a repeat-exempt channel is not flagged for repeating"; fail=$((fail+1))
else echo "PASS  a repeat-exempt channel is not flagged for repeating"; pass=$((pass+1)); fi

# And the exemption is per channel, not a hole in the rule.
if python3 "$CAD" "$HERE/cadence.notexempt.csv" 2>/dev/null | grep -q "C08_FACT_TWICE"; then
  echo "PASS  a channel that is not exempt still fails on a same day repeat"; pass=$((pass+1))
else echo "FAIL  a channel that is not exempt still fails on a same day repeat"; fail=$((fail+1)); fi

# Read as CSV, not with grep: the Why column is a long quoted string that
# spans physical lines, so a line-oriented match never sees the record.
if python3 "$HERE/trivia_assert.py" pinterest-exempt; then
  echo "PASS  the exemption lives in the CSV, not in the gate"; pass=$((pass+1))
else echo "FAIL  the exemption lives in the CSV, not in the gate"; fail=$((fail+1)); fi

# Boards written before the column existed must not start failing for it.
if python3 "$CAD" "$HERE/cadence.board.csv" 2>/dev/null | grep -q "cadence clean"; then
  echo "PASS  a board with no fact column is still checked as before"; pass=$((pass+1))
else echo "FAIL  a board with no fact column is still checked as before"; fail=$((fail+1)); fi

echo
echo "== filling the fact column from a queue dump (added 09/08) =="
# The queue carries a caption, not a fact. This is the step in between, and
# it is where the 09/08 miss actually happened: matched on the whole caption,
# a correct pair scored 0.21 and Hocus Pocus came out as 2 facts.
SNAP="$HERE/../scripts/gm_board_snapshot.py"
OUT="$(mktemp)"
python3 "$SNAP" "$HERE/board.queue.json" "$OUT" --register "$HERE/board.register.csv" >/dev/null 2>&1

# The CTA, the link and the hashtags are the same on every post in a lane.
# Only the opening says what the post is about.
if [ "$(grep -c ',nbc,' "$OUT")" = "2" ]; then
  echo "PASS  a fact buried under a long CTA is still found"; pass=$((pass+1))
else echo "FAIL  a fact buried under a long CTA is still found"
     cat "$OUT" | sed 's/^/      /'; fail=$((fail+1)); fi

# 2 plates of 1 fact are 1 fact. The plate is the reel; the fact is what
# the person scrolling sees twice.
if [ "$(awk -F, '$6=="nbc"' "$OUT" | wc -l)" = "2" ] && grep -q "^q2,.*,nbc," "$OUT"; then
  echo "PASS  2 plates of 1 fact collapse to 1 fact"; pass=$((pass+1))
else echo "FAIL  2 plates of 1 fact collapse to 1 fact"; fail=$((fail+1)); fi

# A guess that looks like an answer is worse than a blank.
if grep -q "^q4,[^,]*,,youtube,36129,," "$OUT"; then
  echo "PASS  a row the register does not cover gets no fact, not a guess"; pass=$((pass+1))
else echo "FAIL  a row the register does not cover gets no fact, not a guess"
     grep "^q4," "$OUT" | sed 's/^/      /'; fail=$((fail+1)); fi

# The guess is still written down, in a column the gate does not read, so
# whoever fills the register has somewhere to start.
if grep -q "^q4,.*she-picked-the-blanket-with-the-gold" "$OUT"; then
  echo "PASS  the guess is kept beside it for whoever fills the register"; pass=$((pass+1))
else echo "FAIL  the guess is kept beside it for whoever fills the register"; fail=$((fail+1)); fi

# End to end: the snapshot feeds the gate, and the gate says the board is
# not fully checked rather than passing it.
if python3 "$CAD" "$OUT" 2>/dev/null | grep -q "C10_FACT_UNLABELLED"; then
  echo "PASS  the gate reads the snapshot and reports the unchecked rows"; pass=$((pass+1))
else echo "FAIL  the gate reads the snapshot and reports the unchecked rows"; fail=$((fail+1)); fi

# The roster travels in the file, not in somebody remembering a flag. A
# snapshot that does not carry it cannot be checked for a silent channel,
# and the 1 time that mattered was the 1 time it would have been forgotten.
if head -1 "$OUT" | grep -q "roster"; then
  echo "PASS  the snapshot carries the roster so silence can be checked"; pass=$((pass+1))
else echo "FAIL  the snapshot carries the roster so silence can be checked"; fail=$((fail+1)); fi

if awk -F, 'NR==2' "$OUT" | grep -q "pinterest"; then
  echo "PASS  the roster names every channel that owes a post"; pass=$((pass+1))
else echo "FAIL  the roster names every channel that owes a post"
     awk -F, 'NR==2' "$OUT" | sed 's/^/      /'; fail=$((fail+1)); fi
rm -f "$OUT"

echo
echo "== trivia fact bank and caption gate (Run 8, added 09/09) =="
# The trivia lane is the one where a language model can do the most damage:
# a confident invented number, in her voice, to an audience that follows her
# partly because she gets this right. 2 failures the holiday lane does not
# have: a fact sourced to the newsletter it was found in, and a moving fact
# repeated after it stopped being true.
TB="$HERE/../scripts/gm_trivia_bank.py"
TC="$HERE/../scripts/gm_trivia_check.py"

if python3 "$TB" --bank "$HERE/trivia.bank.csv" --audit 2>/dev/null | grep -q "is a newsletter"; then
  echo "PASS  a fact sourced to the newsletter it came from is held"; pass=$((pass+1))
else echo "FAIL  a fact sourced to the newsletter it came from is held"; fail=$((fail+1)); fi

if python3 "$TB" --bank "$HERE/trivia.bank.csv" --audit 2>/dev/null | grep -q "past the 90 day window"; then
  echo "PASS  a moving fact checked too long ago is held"; pass=$((pass+1))
else echo "FAIL  a moving fact checked too long ago is held"; fail=$((fail+1)); fi

python3 "$TC" --post "$HERE/trivia.clean.json" --bank "$HERE/trivia.bank.csv" >/dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "PASS  a caption traced to a checked fact passes"; pass=$((pass+1))
else echo "FAIL  a caption traced to a checked fact passes"
     python3 "$TC" --post "$HERE/trivia.clean.json" --bank "$HERE/trivia.bank.csv" 2>&1 | sed 's/^/      /'; fail=$((fail+1)); fi

# The rule that does the most work. Extra numbers are the whole risk.
python3 "$TC" --post "$HERE/trivia.invented.json" --bank "$HERE/trivia.bank.csv" >/dev/null 2>&1
if [ $? -eq 1 ] && python3 "$TC" --post "$HERE/trivia.invented.json" --bank "$HERE/trivia.bank.csv" 2>/dev/null | grep -q "T03_NUMBER_NOT_IN_BANK"; then
  echo "PASS  a number the bank does not carry is refused"; pass=$((pass+1))
else echo "FAIL  a number the bank does not carry is refused"; fail=$((fail+1)); fi

python3 "$TC" --post "$HERE/trivia.noturn.json" --bank "$HERE/trivia.bank.csv" >/dev/null 2>&1
if [ $? -eq 1 ]; then
  echo "PASS  a caption that reports the fact and never turns it is refused"; pass=$((pass+1))
else echo "FAIL  a caption that reports the fact and never turns it is refused"; fail=$((fail+1)); fi

python3 "$TC" --post "$HERE/trivia.secondary.json" --bank "$HERE/trivia.bank.csv" >/dev/null 2>&1
if [ $? -eq 1 ]; then
  echo "PASS  a post built on a newsletter sourced fact is refused"; pass=$((pass+1))
else echo "FAIL  a post built on a newsletter sourced fact is refused"; fail=$((fail+1)); fi

# No fact is HOLD, not FAIL, and never the nearest fact that fits.
python3 "$TC" --post "$HERE/trivia.nofact.json" --bank "$HERE/trivia.bank.csv" >/dev/null 2>&1
if [ $? -eq 2 ]; then
  echo "PASS  a post naming no fact holds rather than guessing one"; pass=$((pass+1))
else echo "FAIL  a post naming no fact holds rather than guessing one"; fail=$((fail+1)); fi

# Approving a reading list is only half a rule. Without this check a session
# could mine any newsletter in the inbox and bank it, and FoundIn would
# quietly say so while every other rule passed.
if python3 "$TB" --bank "$HERE/trivia.bank.csv" --sources "$HERE/trivia.sources.csv" --audit 2>/dev/null \
   | grep -q 'FoundIn "amn@mail.beehiiv.com" is not an approved source'; then
  echo "PASS  a fact mined from a parked newsletter is held"; pass=$((pass+1))
else echo "FAIL  a fact mined from a parked newsletter is held"; fail=$((fail+1)); fi

# And the rule is "not approved", not "has a FoundIn at all".
if python3 "$HERE/trivia_assert.py" approved-passes; then
  echo "PASS  a fact found in an approved newsletter still passes"; pass=$((pass+1))
else echo "FAIL  a fact found in an approved newsletter still passes"; fail=$((fail+1)); fi

# Amanda's real list, so a bad edit to it shows up here rather than in a post.
if python3 "$HERE/trivia_assert.py" live-list; then
  echo "PASS  the live list is her 09/09 answer, tier 1 and 3, tier 2 parked"; pass=$((pass+1))
else echo "FAIL  the live list is her 09/09 answer, tier 1 and 3, tier 2 parked"; fail=$((fail+1)); fi

# The live bank ships unverified on purpose. Nothing was marked checked that
# was not actually opened and read.
if python3 "$TB" --audit 2>/dev/null | grep -q "0 usable"; then
  echo "PASS  the shipped bank holds every row until somebody verifies it"; pass=$((pass+1))
else echo "FAIL  the shipped bank holds every row until somebody verifies it"; fail=$((fail+1)); fi

echo
echo "== media reachability (Run 6, added 09/08) =="
# A clip row can be complete and still be unusable: the footage is on a
# machine the renderer has never seen. Describing a shot is not having it.
MR="$HERE/media-reach.library.csv"
MRROOT="$HERE/media-reach-root"
expect_exit "a local plate that is on disk passes" 0 \
  env GM_MEDIA_ROOT="$MRROOT" python3 "$GATE" --render "$HERE/media-reach.present.json"  --library "$MR" --quiet
expect_exit "a local plate that is not on disk is refused" 1 \
  env GM_MEDIA_ROOT="$MRROOT" python3 "$GATE" --render "$HERE/media-reach.missing.json"  --library "$MR" --quiet
expect_exit "footage that only exists on the phone is refused" 1 \
  env GM_MEDIA_ROOT="$MRROOT" python3 "$GATE" --render "$HERE/media-reach.offline.json"  --library "$MR" --quiet
expect_exit "a clip with no MediaState passes with a note" 0 \
  env GM_MEDIA_ROOT="$MRROOT" python3 "$GATE" --render "$HERE/media-reach.unstated.json" --library "$MR" --quiet

if env GM_MEDIA_ROOT="$MRROOT" python3 "$GATE" --render "$HERE/media-reach.offline.json" \
     --library "$MR" 2>&1 | grep -q E11_MEDIA_UNREACHABLE; then
  echo "PASS  unreachable footage is named by rule, not just refused"; pass=$((pass+1))
else echo "FAIL  unreachable footage is named by rule, not just refused"; fail=$((fail+1)); fi

if env GM_MEDIA_ROOT="$MRROOT" python3 "$GATE" --render "$HERE/media-reach.offline.json" \
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
echo "== a keyword the account cannot answer (Run 9, added 09/11) =="
# 09/11: keyword-audit.csv listed 13 automations. Blotato had 57. Reading the
# repo said BROW was not a keyword. It had been live on 2 accounts since 08/08.
KG="$HERE/../scripts/gm_keyword_check.py"
KR="$HERE/keyword.registry.csv"

if python3 "$KG" --posts "$HERE/keyword.clean.json" --registry "$KR" >/dev/null 2>&1; then
  echo "PASS  a live keyword on the right account passes"; pass=$((pass+1))
else echo "FAIL  a live keyword on the right account passes"; fail=$((fail+1)); fi

if python3 "$KG" --posts "$HERE/keyword.dead.json" --registry "$KR" 2>&1 | grep -q K01_KEYWORD_DEAD; then
  echo "PASS  a keyword with no automation on that account is refused"; pass=$((pass+1))
else echo "FAIL  a keyword with no automation on that account is refused"; fail=$((fail+1)); fi

if python3 "$KG" --posts "$HERE/keyword.dead.json" --registry "$KR" 2>&1 | grep -q "live on instagram 45886"; then
  echo "PASS  the refusal says which account does answer it"; pass=$((pass+1))
else echo "FAIL  the refusal says which account does answer it"; fail=$((fail+1)); fi

if python3 "$KG" --posts "$HERE/keyword.tiktok.json" --registry "$KR" 2>&1 | grep -q K02_KEYWORD_NO_LISTENER; then
  echo "PASS  a keyword CTA on TikTok is refused"; pass=$((pass+1))
else echo "FAIL  a keyword CTA on TikTok is refused"; fail=$((fail+1)); fi

if python3 "$KG" --posts "$HERE/keyword.broken.json" --registry "$KR" 2>&1 | grep -q K03_KEYWORD_BROKEN; then
  echo "PASS  a live keyword whose link is dead is refused"; pass=$((pass+1))
else echo "FAIL  a live keyword whose link is dead is refused"; fail=$((fail+1)); fi

if python3 "$KG" --posts "$HERE/keyword.nodisclosure.json" --registry "$KR" 2>&1 | grep -q K04_NO_DISCLOSURE; then
  echo "PASS  an affiliate keyword with no disclosure in the caption is refused"; pass=$((pass+1))
else echo "FAIL  an affiliate keyword with no disclosure in the caption is refused"; fail=$((fail+1)); fi

if python3 "$KG" --posts "$HERE/keyword.price.json" --registry "$KR" 2>&1 | grep -q K05_PRICE_ON_AFFILIATE; then
  echo "PASS  a price on affiliate content is refused"; pass=$((pass+1))
else echo "FAIL  a price on affiliate content is refused"; fail=$((fail+1)); fi

# The question that started this. The registry has to answer it off the repo,
# with no network, or the next session reads the stale file and says no.
if python3 "$KG" --keyword BROW --platform instagram --account 45886 \
     --registry "$HERE/../data/keyword-registry.csv" 2>&1 | grep -q "automation 439"; then
  echo "PASS  the registry answers is BROW live on IG without a network call"; pass=$((pass+1))
else echo "FAIL  the registry answers is BROW live on IG without a network call"; fail=$((fail+1)); fi

if python3 "$KG" --keyword BROW --platform tiktok \
     --registry "$HERE/../data/keyword-registry.csv" >/dev/null 2>&1; then
  echo "FAIL  the registry claims BROW works on TikTok"; fail=$((fail+1))
else echo "PASS  the registry does not claim BROW works on TikTok"; pass=$((pass+1)); fi

if python3 "$HERE/keyword_assert.py"; then
  echo "PASS  every live Target keyword in Blotato has a registry row"; pass=$((pass+1))
else echo "FAIL  every live Target keyword in Blotato has a registry row"; fail=$((fail+1)); fi

echo
echo "$pass passed, $fail failed"
[ "$fail" = 0 ]
