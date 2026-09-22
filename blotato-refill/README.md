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
    content/wave2-staging-library.txt   starts only when wave 1 is fully logged
    content/wave1-loaded.log            1 line per row: ID loaded|present DATE
    content/wave2-loaded.log
    scripts/validate-wave.py            the library check
    content/refill-reports/             1 short report per run

## The rules, and why each exists

1. **Library check first.** `validate-wave.py` must pass on both waves. Any
   failure loads nothing. A failing library is a bug to fix.
2. **Room.** The queue holds 200. Through 31 Oct, 40 slots stay free for the
   Halloween countdown. Under 10 slots of room means load nothing.
3. **Never load `HOLD-` rows.** Amanda reads those first and releases one by
   removing the prefix. Any due within 14 days is named in the report.
4. **Duplicates.** A row is already done if the same platform already has the
   same media file or the same first 120 characters of text, in the queue or
   published in the last 30 days. It is skipped and marked `present` in the log.
   Never decided on platform plus time. (31 Aug and 3 Sep duplicates.)
5. **Slots, UTC, holding Central time constant:**

       before 1 Nov  instagram 15:00 23:00 · tiktok 15:00 · facebook 17:10 22:00
                     youtube 17:20 · x and linkedin 13:30
       from 1 Nov    instagram 16:00 23:00 · tiktok 16:00 · facebook 18:10 23:00
                     youtube 18:20 · x and linkedin 14:30

6. **Daily caps per account:** instagram 2 on weekdays and 1 at weekends,
   facebook 2, everything else 1. Counted across the whole day after loading.
7. **Halloween evening series sits outside the caps.** From 28 Sep to 31 Oct,
   main-account posts at 23:00 on Instagram and TikTok and 23:30 on Facebook and
   YouTube do not count toward the caps, but they still hold their timestamp.
   Business runs in the morning, Halloween in the evening.
8. **Moving.** A row whose day is at cap or whose timestamp is taken moves to the
   next day with room, at that platform's own slot. No invented times. Rows
   whose date has passed start from today.
9. **X is capped at 280 characters.** Longer rows are not loaded and are named.
10. **Text goes out exactly as written.** A standalone ` / ` is a line break.
    Hashtags, `#TargetPartner` and `#ad` stay.
11. **Pricing (Amanda, 13 Sep).** No price on TikTok Shop items linked on TikTok.
    Nothing else is restricted. Club Target captions may carry prices.
12. **The log is the record.** Every loaded or present row is appended and pushed
    to the library branch in the same run. A failed push is reported first,
    because the next run would load those rows twice.

## Accounts

facebook 30840 (page 1086399221215093) · instagram 45886 · tiktok 41488 ·
youtube 36129 · x 21430 · linkedin 20723. Cesa's own accounts (instagram 65540,
tiktok 55761) are never loaded from these libraries.

## How it runs

The routine `Blotato refill (Sonnet, every 2 days)` runs every 2 days at 6:00 AM
Central in a fresh session with only the Blotato connector. It lists the queue,
runs `refill.py plan`, creates exactly the posts in the plan, runs
`refill.py log`, and pushes the log. The session makes no placement decisions.

`refill.py apply --execute` does the same through Blotato's REST API with
`BLOTATO_API_KEY` set, with no Claude session at all. It is ready for a
scheduled GitHub workflow once Amanda approves adding one.
