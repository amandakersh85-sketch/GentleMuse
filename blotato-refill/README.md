# Blotato refill

The daily top-up of Amanda's Blotato queue, as rules in a script instead of
judgment in a conversation. This file is the SOP. It replaces
`SOP_0826_blotato-queue-refill-v3` in Drive, which predates the 13 Sep pricing
correction and the evening Halloween series.

- `refill.py` decides what loads and where. It sends nothing without `--execute`.
- `tests/test_refill.py` checks every rule below. `python3 blotato-refill/tests/test_refill.py`

## Where things live

The libraries and load logs stay on branch `claude/club-target-game-plan-9xs2du`:

    content/wave1-staging-library.txt   rows to load
    content/wave2-staging-library.txt   loads after wave 1
    content/wave1-loaded.log            1 line per row: ID loaded|present DATE
    content/wave2-loaded.log
    scripts/validate-wave.py            the library check
    content/refill-reports/             1 short report per run

## The rules, and why each exists

1. **Library check first.** `validate-wave.py` must pass on both waves. Any
   failure loads nothing. A failing library is a bug to fix.
2. **Room.** The queue holds 200. 10 slots always stay free for the loaders that
   post on a promise: the nightly seasonal run and the daily trivia. Under 10
   slots of room means load nothing. From 09/23 to 09/28 this held 40 for
   Halloween and every run loaded 0, while the days ahead thinned out.
3. **Never load `HOLD-` rows.** Amanda reads those first. Any due within 14 days
   is named in the report. A released HOLD row is scheduled by hand at its own
   date and time, never through this script: the library check refuses holiday
   wording without `HOLD-`, and HOLD-GW2001 to HOLD-GW2008 share their numbers
   with the ordinary rows GW2001 to GW2008.
4. **Duplicates.** A row is already done if the same platform already has the
   same media file or the same first 120 characters of text, in the queue or
   published in the last 30 days. It is skipped and marked `present` in the log.
   Never decided on platform plus time. (31 Aug and 3 Sep duplicates.) 2
   text-only rows, media `-`, are not copies of each other.
5. **Nearest day first, 7 days at most.** A row goes to the nearest day, from
   today, with room. Nothing loads more than 7 days out: the queue holds about
   10 days at full volume, and Amanda, 09/28: "we don't put it all in the queue,
   obviously". Row dates are advisory. A row with no room waits for the next
   run.
6. **Slots, in Central time,** so the clock time holds across the 1 Nov change:
   2:00 PM on Instagram, TikTok, Facebook and YouTube, 8:30 AM on LinkedIn. 2 PM
   is the day's evergreen slot. 10 AM is trivia, noon is Amanda, 4 PM is Club
   Target and 6 PM is the seasonal post. Noon Central was retired on 24 Aug
   after a pileup.
7. **3 a day per account.** Everything on the account that Central day counts,
   the 6 PM seasonal post included, because the board's 3 to 5 counts everything.
   LinkedIn is 1.
8. **2 hours apart.** A post stays 2 hours clear of every other post on its
   account, the same spacing as `gm_cadence_check.py` C05. The 6 PM seasonal post
   (6:30 PM on Facebook and YouTube) is held clear from 28 Sep to 1 Jan even
   before its own loader has put it in.
9. **A named day is that day.** A row that names a day of the week goes out on
   that day only. "Just Another Tuesday" is the newsletter, and TUESDAY in
   capitals is its keyword, so neither counts.
10. **Keyword check.** Every row goes through `gm_keyword_check.py` against
    `keyword-registry.csv` before it loads. A row asking for a keyword its
    account cannot answer is refused and named in every report until the row is
    fixed. On 09/28, 7 wave rows asked for CESA on the main accounts, retired
    there on 09/18, and 3 LinkedIn rows asked for CONSIDER, which LinkedIn has no
    automation to answer.
11. **X is 0 a day** since 09/08. Its rows are skipped and counted, never
    loaded, and they no longer hold wave 2 back.
12. **Wave 1 goes before wave 2.** A row that cannot load never blocks the rows
    behind it.
13. **Text goes out exactly as written.** A standalone ` / ` is a line break.
    Hashtags, `#TargetPartner` and `#ad` stay.
14. **Pricing (Amanda, 13 Sep).** No price on TikTok Shop items linked on TikTok.
    Nothing else is restricted. Club Target captions may carry prices.
15. **The log is the record.** Every loaded or present row is appended and pushed
    to the library branch in the same run. A failed push is reported first,
    because the next run would load those rows twice.

## Accounts

facebook 30840 (page 1086399221215093) · instagram 45886 · tiktok 41488 ·
youtube 36129 · linkedin 20723. X 21430 is not loaded. Cesa's own accounts
(instagram 65540, tiktok 55761) are never loaded from these libraries.

## How it runs

The GitHub job `Blotato refill` (`.github/workflows/blotato-refill.yml`) runs
every 2 days at 6:30 AM Central daylight time. It checks out the library branch,
runs the tests, runs `refill.py apply --execute`, and pushes the load log and the
report to `content/refill-reports/` on the library branch. It shares the
`blotato-queue` group with the other loaders, so they never race for the 200.
The Sonnet routine that did this before is off.

To see what a run would do without sending anything:

    python3 blotato-refill/refill.py plan --lib <library checkout> --queue-file queue.json --report r.md
