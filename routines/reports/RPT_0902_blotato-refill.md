# Blotato queue top-up, 09/02/2026

First local run. The routine is installed and it works.

## Read this first: the push didn't land

The commit is saved on your machine (0b7d95e) but it did NOT reach GitHub.
Git asked for credentials and there aren't any stored on this computer:

```
remote: Invalid username or token. Password authentication is not supported
fatal: Authentication failed for 'https://github.com/amandakersh85-sketch/GentleMuse.git/'
```

This is not the same emergency it was in the cloud. The daily job runs here now
and reads the local file, so tomorrow's run is already protected and won't
double-load. What's stale is GitHub, not your machine.

The fix takes about 30 seconds and only you can do it. Git Credential Manager
is already installed, it just has nothing saved. Open a normal terminal and run
this once. A browser window will open, sign in to GitHub, and it'll remember
from then on:

```bash
cd "D:\Claude Projects\GentleMuse"; git push origin claude/club-target-game-plan-9xs2du
```

After that every future run pushes on its own.

## What loaded

Queue was at 182 with 18 free. It's now at 200, which is the Starter cap, so
it's full. 18 rows loaded, last one reached was GW0104. Nothing failed. No row
hit an error of any kind, and the 200 cap was reached exactly, not overshot.

Everything I loaded is confirmed sitting in the live queue. I checked with
list_posts rather than post status, because post status lies about this.

The queue now runs continuously through 15 October 2026 at 10:00 AM Central.
After that there's a hole until a single Christmas post on 1 December at
10:00 AM Central. That hole closes on its own as posts publish and the daily
job refills behind them. There are still 61 unloaded rows in Wave 1 and 200 in
Wave 2, of which 192 load on their own and 8 are HOLD rows waiting on you, so
Wave 3 is nowhere near needed yet. That's 253 rows of supply ready to go.

Two of the 3 empty days are now filled. 26 and 27 September have content.
12 September is still empty and there's no row that wants that date.

## Rows I moved

11 of the 18 couldn't sit where they were written because the slot was already
taken. Each moved to the next free slot for its platform. All times Central.

| Row | Platform | Written | Moved to |
|---|---|---|---|
| GW0001 | Instagram | 21 Sep 10:00 AM | 22 Sep 10:00 AM |
| GW0004 | Facebook | 21 Sep 12:10 PM | 26 Sep 12:10 PM |
| GW0005 | X | 21 Sep 8:30 AM | 24 Sep 8:30 AM |
| GW0007 | Instagram | 22 Sep 10:00 AM | 24 Sep 10:00 AM |
| GW0010 | Facebook | 22 Sep 12:10 PM | 27 Sep 12:10 PM |
| GW0012 | LinkedIn | 22 Sep 8:30 AM | 23 Sep 8:30 AM |
| GW0017 | X | 23 Sep 8:30 AM | 26 Sep 8:30 AM |
| GW0023 | X | 24 Sep 8:30 AM | 27 Sep 8:30 AM |
| GW0033 | Facebook | 26 Sep 12:10 PM | 28 Sep 12:10 PM |
| GW0097 | Instagram | 9 Oct 10:00 AM | 13 Oct 10:00 AM |
| GW0103 | Instagram | 10 Oct 10:00 AM | 14 Oct 10:00 AM |

The other 7 kept their written time.

## The thing that almost went wrong

`wave1-loaded.log` was empty. Just the 2 header lines, no rows. But 117 of the
196 Wave 1 rows were already scheduled and live in Blotato.

If the job had run against that empty log it would have re-loaded all 117 as
duplicate posts, the same caption going out twice on the same account.

The 31 August cloud run is what caused it. It loaded rows, then couldn't push
its own log because the proxy blocked the repo, so the record never got
written. It left a backup note in Drive saying 56 rows were affected. The real
number is 117. I checked every row against the live queue on platform plus
exact post text, not on the note, and 117 of them are already out there.

Those 117 are now in the log, marked reconciled so you can tell them apart from
a normal load. That file is the only thing standing between you and duplicate
posts, so it should never be blanked.

Worth knowing: matching on text alone would have been wrong. The library was
built by recombining captions you'd already published, so the same words
legitimately appear on a different platform on purpose. Only a match on the
same platform is a real duplicate. GW0005 looked like a duplicate at first
glance and isn't. It's the 5 books post pointing at the Reset Guide, and the
older one points at Press Play. Different post, so I loaded it.

## The validator was broken on this machine

`validate-wave.py` crashed before it could run a single check. It opened the
library files using whatever text encoding Windows defaults to, which here is
cp1252, and your libraries are UTF-8. It died on the first character it
couldn't read. This never showed up in the cloud because Linux defaults to
UTF-8.

Fixed. It now reads UTF-8 explicitly. Both libraries pass all 17 checks.

That matters more than it sounds like. The routine is built to stop and load
nothing if validation fails, so unfixed, the 6 AM job would have failed
silently every single morning and you'd never have known why.

## Two things the queue did on its own

While I was working, Blotato moved 9 posts by itself. There were 6 slots where
2 or 3 Instagram posts sat on the exact same minute, plus 1 doubled LinkedIn
slot. Blotato broke them apart on its own before I touched anything, which is
good, and 3 September had 3 Instagram posts stacked on one minute so that was
worth fixing.

The catch is where it put them. 2 of them landed at 12:00 noon Central, which
is the slot SOP v3 specifically retired because Instagram buries it. Those are
LinkedIn on 3 September and Instagram on 5 September. Not urgent, but the
platform is undoing your slot rules when it reshuffles, so it's worth knowing
it does this.

Separately, 2 X posts that were scheduled for 21 and 22 September left the
queue while I was working. I didn't remove them and they aren't in the failed
list. Your Cesa daily pipeline was running at the same time and added 2
Instagram posts of its own, so something else is writing to this queue
concurrently. The 2 that went were "5 books" pointing at Press Play, and "The
older I get, the more I understand why people stop going out". If you didn't
delete those on purpose, that's worth a look.

## About the 7 AM start

I set it to 6:00 AM Central, not 7:00. Your own rule is nothing recurring
inside 7 AM to 1 PM because that's when you're actually on the machine, and
6 AM is the documented default. It still lands well before your 1:30 shift, so
the reason for a morning run holds either way. Your Cesa wake task already
wakes the computer at 5:50, so 6:00 catches a machine that's already up.

Say the word if you want it at 7 anyway.

## What's installed

Task name is **GM Blotato Daily Refill**. Daily at 6:00 AM Central, verified
Ready, next run 3 September 6:00 AM. It wakes the machine if it's asleep and
runs as soon as it can if the computer was off at 6.

```
routines/RUN_blotato-refill.md      the instructions the job follows
routines/run-blotato-refill.ps1     what the scheduler actually runs
routines/run-blotato-refill.sh      same thing for bash, kept for portability
routines/logs/                      one log per day
routines/reports/                   this report and the ones after it
```

One more thing about the repo. It's a public repo on GitHub, so your full
content library, captions and all, is readable by anyone who finds it. That may
be exactly what you want for building in public. Just flagging it, since the
libraries carry every caption before it goes out.

## No HOLD rows are due

Wave 1 has no HOLD rows at all. All 8 of them are in Wave 2, which covers
30 October to 8 December, so the Halloween and Black Friday beats are in there.
The earliest is HOLD-GW2001 and none of them land before 31 October. Nothing
needs your review in the next 14 days, but those 8 are newly written sales copy
rather than something you've already published, so they wait on you. You
release one by dropping the HOLD- prefix yourself.
