# Blotato queue top-up, 09/02/2026 (second run of the day)

Nothing loaded this run. The queue is full.

This is the second top-up on 09/02. The first run's report is in
`RPT_0902_blotato-refill.md` and it's the one with the action item in it.

## What the queue looks like

There were 200 posts scheduled when I checked, and 0 free slots. That's the
Blotato Starter cap exactly. The rule is to load nothing when there are fewer
than 10 free slots, so I didn't create a single post.

This isn't a problem, it's this run catching up with the first one. The routine
file's baseline says 182 scheduled and 18 free. The ledger shows 18 rows loaded
earlier today on top of the 117 that got reconciled. 182 plus 18 is 200. The
first run filled the queue right up to the cap, and everything lines up.

I confirmed the 200 is a real total and not just a page limit on the response.
The single wide query returned 200 with no cursor, which on its own could have
meant a cap. Splitting the same range into disjoint windows gives 143 in
September, 56 in October and 1 in December, which is 200, and the ID sets match
exactly. So it's a true count.

## Runway

Content runs continuously through 15 October 2026 at 10:00 AM Central. After
that there's a 46 day gap with nothing in it, then a single Christmas post on
1 December 2026 at 10:00 AM Central.

One empty day inside the run: 12 September. The baseline had 26 and 27 September
empty too, and the 18 rows the first run loaded filled both of those.

## Loaded

0 rows. No last row ID reached, because nothing was attempted.

No row times were moved, since no rows were loaded. No failures to report, and
nothing hit the 200 cap mid-load. I stopped before loading, not during.

## HOLD rows

None due in the next 14 days. Wave 1 has no HOLD rows at all. Wave 2 has 8, and
the earliest is HOLD-GW2001 on 31 October 2026. The rest run from 17 November
through 1 December. Nothing needs your eyes yet.

## Library supply

Plenty left. 61 rows unloaded in Wave 1, 192 in Wave 2, so 253 across the two.
Wave 3 isn't needed anywhere close to yet.

Both libraries passed all 17 validation checks, so the encoding fix from the
first run is holding. Wave 1 is 196 rows, Wave 2 is 200, and every ID is unique.
The 8 HOLD rows in Wave 2 carry their own numbering alongside the plain rows,
so HOLD-GW2001 and GW2001 are 2 different rows. That's fine, just worth knowing
if you ever grep by ID.

## Preflight

All account IDs matched the live API exactly, including Pinterest 6328 and both
of Cesa's own accounts, TikTok 55761 and Instagram 65540. No differences to
report. Blotato MCP was reachable the whole run. The git pull came back already
up to date.

## Commit and push

Nothing to append to the ledger, since nothing loaded. `content/wave1-loaded.log`
is untouched and still holds all 135 entries, 117 reconciled and 18 loaded.

## One thing to know about these reports

Both runs today wrote to the same filename, because the naming is 1 report per
date. The first run's report landed on disk after I'd already committed mine to
the same path, so mine would have quietly replaced it. I kept both instead. The
first run's is at the original name and this one has run2 on the end.

If the daily job ever runs twice in a day again, the same collision is waiting.
Worth adding a time to the filename at some point so a second run can't erase
the first one's report.

## What actually matters here

The cap is the constraint now, not the content. You've got 253 rows ready to go
and nowhere to put them until posts publish and free up slots. Slots open as
September's posts go out, roughly a handful a day, so tomorrow's 6 AM run should
have room again.

The thing worth watching is 15 October. That's where the queue stops being
continuous. There's 46 days of nothing after it, and closing that gap needs free
slots more than it needs new writing.
