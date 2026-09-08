# GENTLE MUSE — CAROUSEL BUILD AND SCHEDULING HANDOFF
**Paste everything below as your first message in the Carousel Build project.**

---

Read `CLAUDE.md` at the repo root first. The posting board is in there and it
does not get re-litigated. Branch: `claude/holiday-caption-strategy-m5abq8`.

You own two things: **the lead magnet carousels**, and **the schedule**. A
second local session handles the D: drive footage — see
`HANDOFF_0908_local-footage-and-volume.md`. Do not duplicate its work.

## THE BOARD. THIS IS THE WHOLE CADENCE.

| Channel | Per day | What goes there | Call to action |
|---|---|---|---|
| Instagram | 3 to 5 | everything | comment keyword to DM |
| Facebook | 3 to 5 | everything, same cadence as IG, they move as a pair | comment keyword to DM |
| TikTok | 3 to 5 | everything | **link in bio, never the keyword** |
| YouTube | 3 to 5 | everything. Shorts for reels, **long form for food reviews** | link in description |
| LinkedIn | **1** | **business only.** Just Another Tuesday, or the free AI guide | link |
| X | **0** | dropped 09/08. Not serving. | none |

3 to 5 is **per account**, not per platform: the 2 Instagram accounts are 2
audiences. 2 hours minimum between posts on one account, never measured
across accounts. Nothing between 02:00 and 13:00 UTC.

This lives in `filing-system/data/channel-rules.csv` and
`gm_cadence_check.py` enforces it. A 2nd LinkedIn post in a day is caught. A
post to X is caught. **Change the CSV, never the gate, and never a note
instead of either.**

## VARIETY IS THE POINT OF THE VOLUME

A day is not 5 of the same lane. The lanes:

1. **Holiday fact** — the Halloween run, then Thanksgiving
2. **Cesa** — the 19 year old chihuahua, weekends are hers
3. **Club Target** — `#TargetPartner` first, never state a price
4. **Food review** — YouTube long form, plus short cuts for IG, FB, TikTok
5. **Lead magnet carousel** — yours, below. **One of the 3 to 5 every day.**
6. **Amanda on camera** — she films, or HeyGen carries it
7. **Trivia** — fact verified, source verified, cited, true

When you fill a day, fill it across lanes. Never 5 Halloween facts.

## YOUR FIRST JOB: A CAROUSEL IN THE DAILY ROTATION

The carousel factory already exists and works:
- `reel-factory/carousel.html` — the slide composition, same palette and
  faces as the reels
- `reel-factory/carousel-shots.mjs` — the Playwright shooter, does 4:5
  carousel slides and 9:16 talls
- 5 sets already shot: turnip, snick, casper, coffinbell, lugnano

The magnets and which weekday carries which are in
`filing-system/data/rotation-magnet.csv`:

```
Monday     reflective   TUESDAY   Just Another Tuesday
Tuesday    plain        CONSIDER  Consider This
Wednesday  plain        GUIDE     Beginner's Guide to AI Tools
Thursday   tender       RESET     Gentle Self-Reset Checklist
Friday     warm         CONSIDER  Consider This
Sat / Sun  quiet        CESA      19 Years Old, 10 of Them Mine
```

Build one carousel per weekday magnet, put it in the daily rotation, and let
the keyword do the work on Instagram and Facebook. On TikTok the same
carousel runs with a bio link instead of the keyword.

**Just Another Tuesday goes to YouTube and LinkedIn.** That is the LinkedIn
business post on the days it runs; the free AI guide covers the rest.

### The carousels are evergreen. Treat them that way.

A free lead magnet carousel does not expire. The offer does not change and
it is not seasonal, so it can run again on any platform, any time. There is
already enough variation to keep going until the volume target is met or
the data says stop. New sets lead because they are the best quality; drop
an older one in now and then to keep the mix fresh.

**Reuse before you generate.** The budget does not stretch to regenerating
what already exists and works. Spend credits only where the piece genuinely
has to be new.

All 6 sets are shot and **all 6 are now hosted**: turnip, snick, casper,
coffinbell, lugnano, trailer. 48 slides and talls, every URL verified byte
for byte, all in `blitz-media-map.csv`. Nothing here costs a credit to use
again.

### Pinterest, which is cold and should not be

1 pin a day, recycled off the same evergreen carousel slides. The point is
keeping the account warm, not conversion: Amanda's words are "we run dry on
it constantly." Rotate unless the data shows it is not worth it.

Pinterest is the one place a repeat is fine. A pin is a bookmark and
repinning is how the platform works, so the no re-wear rule does not apply
there. It still applies everywhere else.

The pin's destination is a **link field on the pin**, not caption text, so
no keyword automation applies and the caption does not carry the call to
action.

**48 pins are staged** in `staging-library.csv`, which at 1 a day is 7
weeks of Pinterest with no new work and no credits. They could not be
scheduled yet only because the queue is at 200, so they load on the next
drain.

The 9:16 talls are the better pin shape and should lead; the 4:5 slides
carry the same content and work as the carousel on Instagram.

## YOUR SECOND JOB: THE 99 POST PULL, ALREADY APPROVED

105 posts sit between 19 Sep and 31 Oct at 2.4 a day, holding half the
200 slot queue. 99 are not locked to their date. Pulling them frees 99 slots
so the near 12 days can run full.

Amanda has approved this. Do it in this exact order and no other:

1. Write all 99 into `staging-library.csv` as STAGED rows with caption,
   hosted media URL, account and intended slot.
2. Read every row back. **A row missing its media URL is not a row.**
3. Only then remove the schedules, and only for rows that read back complete.
4. Refill across lanes, per above. Never 5 of one thing.

93 of the 105 are Halloween facts, which is exactly why step 4 matters. If
you reload them denser you have made the variety problem worse, not better.

The 6 that stay: Samhain on 31 Oct (x2), trick or treat on 30 Sep and 4 Oct.

## THE CAP

Blotato starter holds **200 scheduled posts**. That is not a monthly
allowance, it is how many can wait in line. 200 / 16 a day is **12.5 days**,
so the queue holds a rolling 12 day window and the reservoir holds the rest.
A post held for 31 Oct owns a slot for 53 days, and that is what starved the
near days.

**Never propose a plan upgrade.** She has ruled twice. Extra credits bought
separately are fine. 2,974 credits as of 09/08.

## BEFORE YOU SCHEDULE ANYTHING

```
python3 filing-system/scripts/gm_cadence_check.py <day.csv>
```
Columns: `id, postTimeUTC, platform, accountId, label`. Build the proposed
day **with the new post in it**, run the gate, then schedule. Not after.
This rule exists because it was broken the day after it was written.

Check three things per post: the FACT is not already scheduled elsewhere,
the MEDIA is not already worn by a scheduled post, and the day passes the
gate with it added.

## SLOTS

```
Instagram 45886   15:00  18:00  20:00  23:00  01:30    UTC
TikTok    41488   15:00  17:00  20:00  23:00
Facebook  30840   14:00  17:00  19:30  22:00
YouTube   36129   14:30  17:20  20:20  23:20
LinkedIn  20723   13:30                                 (1 a day)
```
Two do not move: Instagram 15:00 is the 10:00 Central peak and moving it
costs 25 percent. Nothing lands at 19:00 Central because that is 00:00Z the
next day, an off by one that already cost 4 Cesa posts a day.

## ACCOUNTS

```
instagram 45886 thegentlemuse2026   instagram 65540 cesasgoldenyears
tiktok    41488 thegentlemuse2026   tiktok    55761 cesasgoldenyears
facebook  30840 pageId 1086399221215093
youtube   36129    linkedin 20723    pinterest 6328
```

## RULES THAT DO NOT BEND

1. Propose only by default. Nothing moves without an explicit execute flag.
2. Nothing deletes. Execute moves to `_QUARANTINE`.
3. HOLD is never automated. The OF lane stays excluded and hand filed.
4. Approval is the gate.
5. No substitution. Missing input means say so and stop.

Voice: calm, specific, emotionally precise. No hype, no em dashes, no
spelled out numbers. `post-grader`, do not ship below 8 out of 10.

Tests before and after you touch anything: `bash filing-system/tests/run-tests.sh`
Expect **96 passed, 0 failed**.
