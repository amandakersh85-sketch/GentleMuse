# Queue supplier contract, 09/02/2026

For the Holiday caption strategy and voice session, which now owns the Blotato
queue. Written by the Club Target / wave-library side.

Amanda's decision, 09/02: **this side supplies and gates, your side decides.**
The wave libraries, the load ledger and `validate-wave.py` stay here as the
content source and the safety check. What enters the live queue, and when, is
yours alone. One writer to the queue.

The `GM Blotato Daily Refill` scheduled task is **Disabled** as of 09/02 so it
cannot compete with you for slots. Do not re-enable it without saying so.

---

## 1. Read this before you load anything from the wave libraries

`content/wave1-loaded.log` on THIS branch (`claude/club-target-game-plan-9xs2du`)
has 135 entries. The copy on your branch is the old one with 2 header lines and
no rows.

117 of those entries are rows that are **already live in Blotato**. They were
loaded by the 31 August cloud run, which then failed to push its own ledger, so
the record was lost. If you load from the wave libraries while reading an empty
ledger, you will re-post all 117: the same caption, twice, on the same account.

Until the branches are reconciled, either work from the ledger on this branch or
do not load from the wave libraries at all.

The reconciliation was done on **platform + exact post text**, not on text alone.
That matters. The libraries were built by recombining captions Amanda had already
published, so identical wording on a *different* platform is intentional
cross-posting, not a duplicate. Only a same-platform match is a real duplicate.

There is no `wave2-loaded.log` yet. One has been created here with the same
header. Wave 2 loading must append to it or the same problem repeats.

## 2. The validator is a hard gate, not advice

`python scripts/validate-wave.py content/wave2-staging-library.txt`

Use `python`, not `python3` — `python3` is a Microsoft Store stub on this machine
and fails. The script was fixed on 09/02 to read UTF-8; before that it crashed on
Windows before running a single check.

Four rules it enforces that will bite seasonal copy specifically:

- **Seasonal copy must carry the `HOLD-` prefix.** Any row matching black friday,
  cyber monday, small business saturday, thanksgiving, halloween, on sale, sale
  closes, last call and *not* prefixed `HOLD-` fails the run. A failing library is
  meant to stop a load entirely, so one unprefixed row silently halts everything.
- **No price may appear.** No `$` followed by a digit, anywhere.
- **No discount percentage.** No "20% off". Both of these trace to the open
  TikTok Shop violation from 08/04/2026 over misleading pricing. Not cosmetic.
- **Every Club Target theme needs a TikTok row.** Points only accrue on TikTok
  while Amanda is under 500 Instagram followers. A theme placed on Instagram or
  Facebook with no TikTok twin silently loses all 30 points for that theme.

That last rule is keyed to a number Amanda is actively trying to cross. **The day
she passes 500 IG followers, revisit it** or it will misroute points.

## 3. The 8 HOLD rows are the commercial floor

Amanda's decision: keep these as guaranteed coverage of the commercial beats, and
write the relatable seasonal layer around them. They need a dedupe pass against
whatever you write.

All 8 live in `content/wave2-staging-library.txt`. All times UTC.

| ID | When (UTC) | Beat |
|---|---|---|
| HOLD-GW2001 | 31 Oct 15:00 | Halloween, Cesa in no costume |
| HOLD-GW2002 | 17 Nov 16:00 | Teaser, "I have been sitting on something since July" |
| HOLD-GW2003 | 24 Nov 16:00 | The AI + worksheet money walkthrough |
| HOLD-GW2004 | 26 Nov 16:00 | Thanksgiving, no pitch |
| HOLD-GW2005 | 27 Nov 16:00 | Black Friday, Paycheck Planner sale opens |
| HOLD-GW2006 | 28 Nov 16:00 | Small Business Saturday |
| HOLD-GW2007 | 30 Nov 16:00 | Cyber Monday, last call |
| HOLD-GW2008 | 1 Dec 16:00 | Sale over, thank you |

Amanda releases one by dropping the `HOLD-` prefix herself. Nothing auto-loads
them. Do not drop the prefix on her behalf.

### Two gaps in that arc worth filling

**Every one of the 8 is Instagram.** No TikTok, no Facebook, no X, no LinkedIn.
For a campaign that is supposed to serve a follower goal and an email goal, the
whole commercial arc currently exists on one surface. That is the clearest place
for your seasonal layer to add reach rather than duplicate.

**It is a sales arc with no cross-platform top of funnel.** GW2005 through GW2007
sell; nothing in the 8 drives new reach into them beforehand except GW2001 and
GW2002.

### Two live dependencies that will break it

1. **The Payhip sale price.** GW2005, GW2006 and GW2007 all promise a live sale
   running 27 to 30 November. Disabling a Payhip sale wipes the stored sale price,
   so when it is re-enabled the price must be retyped or the planner sells at $5.
   Whoever turns that sale on needs to check the price on the listing, not just
   the toggle.
2. **A newsletter issue must ship 24 November.** GW2002 promises "it goes out on
   the 24th" and GW2003, dated 24 November, opens with "the full walkthrough went
   out this morning". If that issue does not exist, GW2003 is a false claim in
   Amanda's voice. Confirm the issue is written before releasing either row.

## 3b. What the zone model does to these libraries

Added 09/02 after reading the zone contract (SPRINT 0-7, MODEL 8-14, ANCHOR 15+
date-locked holiday only, PAID within its day).

**Wave 1's dates now conflict with it.** Wave 1 rows are written for 21 Sep to
29 Oct, which is 19 to 57 days out, so every one of them lands in ANCHOR. They
are evergreen rows, not holiday anchors, so under the zone contract none of them
may load at its written time.

The clean reading: **the wave libraries stop being a dated schedule and become a
draft bank.** Rows get pulled forward into MODEL as it comes due, and each row's
stored `scheduledTime` is advisory, kept only for slot shape (which platform,
which hour) and ignored as a date. The ledger and the validator still apply
unchanged, because both are keyed to row IDs and text, not to dates.

That resolves cleanly against Wave 2's HOLD rows, which *are* date-locked
holiday anchors and belong in ANCHOR exactly as written.

**Open question: who fills MODEL.** The zone contract says the MODEL zone is fed
"from the draft bank" and moved by "the daily refill", but that refill is the
task Amanda disabled on 09/02 so it would stop competing for slots. Right now no
job holds that. `gm_queue_daily.py` reports the MODEL shortfall; something still
has to fill it. Either re-enable the daily task scoped to MODEL only, or take the
job into the queue-planning side. It should not be left to whoever notices.

## 4. Slots, and the DST change

The libraries and the Blotato API are UTC. Amanda reads Central. Label which one
you mean every time.

```
before 1 Nov (UTC-5)   instagram 15:00 and 23:00, tiktok 15:00,
                       facebook 17:10, youtube 17:20, x and linkedin 13:30
from 1 Nov (UTC-6)     instagram 16:00 and 23:00, tiktok 16:00,
                       facebook 18:10, youtube 18:20, x and linkedin 14:30
```

The whole HOLD arc except GW2001 falls after the change, which is why those rows
read 16:00 rather than 15:00. Same local hour, different UTC.

Other rules: one post per platform per timestamp; Instagram at most 2 a weekday
and 1 at the weekend; nothing on Instagram between 02:00 and 13:00 UTC; noon
Central is retired as a slot; and when a slot is contested, Cesa wins.

**Blotato reflows on its own.** It breaks same-minute collisions without being
asked, but it scatters posts into times that are not SOP slots, including noon
Central. Observed 09/02: 9 posts moved inside 25 minutes, 2 of them to noon
Central. Re-measure the queue immediately before acting on it; a snapshot minutes
old can already be wrong.

## 5. Links

Verified, use only these:

```
Consider This  https://consider-this.subscribepage.io
AI Guide       https://ai-guide.subscribepage.io
Press Play     https://press-play.subscribepage.io
Reset Guide    https://payhip.com/b/9FE2U
Essentials     https://www.gentlemuse.co/tiktok
Cesa           instagram.com/cesasgoldenyears
```

Dead, do not use: `reset-guide.subscribepage.io` is a different creator,
`preview.mailerlite.io/...` was replaced 08/18/2026, `gentlemuse.co/reset-guide`
503s and Wix is being left.

Your CTA gate is already correct that a TikTok caption URL is not tappable. The
same constraint has a second half worth carrying: Blotato DM automations run on
Instagram and Facebook only, so a TikTok "comment CESA" CTA never fires either.
On TikTok, route to bio.

## 6. State as of 09/02, 11:20 Central

- Queue held 200 at the cap after this side's load; October has since been cleared
  into your backlog and held 5 posts when last measured, all 5 from that load.
- Supply remaining: 61 unloaded in Wave 1, 192 loadable in Wave 2 plus the 8 HOLD.
- 5 commits on this branch are **unpushed**. GitHub has no credential on this
  machine. Amanda runs `git push` once from an interactive terminal, signs in
  through the browser prompt, and it is fixed permanently. Until then this branch
  exists only on her disk, which is why the ledger has not reached you.
