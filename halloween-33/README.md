# Halloween 33 Nights

1 true fact every night, Sep 29 to Oct 31, plus the trailer on Sep 28.
Approved plan: https://claude.ai/artifact/FwBepNEF5t6sovQi3z16t9

## How it runs

- `approval/plan.json` is the approved order: which fact on which night, and its background.
- `weeks/beats.json` is the on-screen text. `weeks/build_week.py N` turns a week into
  reel payloads and captions (`weekN-reels.json`, `weekN-posts.json`).
- Reels render in the reel factory (holiday branch) with the music bed, then upload to
  Blotato. `weeks/media.json` maps each render to its Blotato URL.
- `make_schedule.py` builds `schedule.json`: every post, its time, and the old Halloween
  repeats it replaces. Rebuild it after media.json changes.
- `load.py` loads 7 days ahead. The GitHub job `Halloween 33 Nights` runs it daily at
  7 AM Central, so the countdown fits the 200-post queue as room opens. It removes the
  old repeat on a date only when that night's new post goes in. Every removed post is in
  `backup/queue-2026-09-23-full.json`.
- Times: Instagram and TikTok 6:00 PM Central nightly, Facebook and YouTube 6:30 PM
  nightly. Samhain moves to 6:00 PM Oct 31. "Samhain is 5 nights out" moves to
  7:30 PM Oct 26.
- Facebook and YouTube ran odd nights only until 09/28. The trailer on both says
  "every night from tomorrow to Halloween. 33 nights", so Amanda added the 16 even
  nights that day: the same videos and the captions already written for them. 134
  posts in all. `approval/plan.json` books them too, so rebuilding the weeks keeps them.
- To stop it: set the repository variable `HALLOWEEN_33_OFF` to `true`.

Tests: `python3 halloween-33/tests/test_load.py`

## The facts were checked on 10/04

Amanda asked for the Thanksgiving facts to be checked and 4 of the 26 were
wrong. `gm_fact_check.py` then reported this plan as 28 nights with no
verification record at all, so the same pass was run over the 28 still to come.
Every row now carries `verified`, `checked` and sources with URLs.

This plan held up far better than the Thanksgiving draft did. It already cited
real sources with links rather than the prose gestures the Thanksgiving rows
had, and 20 of the 25 facts needed nothing but a verdict. What came back:

| night | was | is |
|---|---|---|
| 10 | candy corn "was invented by George Renninger" | credited to him on oral history. History.com and National Geographic both say nobody knows for certain. The 1880s date and the Chicken Feed name are solid |
| 19 | sugar was "among the first" groceries rationed | it was the **first** food rationed. Sales stopped 04/27/1942, resumed 05/05 at half a pound a person a week |
| 30 | the Owens house was in "San Juan County Park" and the source is a page about Whidbey Island | the house was on San Juan Island, the town is Coupeville on Whidbey. The land carries Native American heritage so no digging was allowed, which is **why** it was a shell |
| 32 | Odilo "died in 1048" | sources give 1048 and 1 January 1049. The year is not the fact, so it is out |
| 24 | "the reflex stayed because it quietly does a second job" | the study found shared wiring, not a reason the reflex persisted. That inference was being put in its mouth |

5 rows got better from being read rather than corrected: the werewolf survives
in only 3 passages of Old English, all by the same man; the Guila Naquitz squash
predates maize and beans by more than 4,000 years, not merely "earlier"; only 14
of Burns's works carry his own footnotes and Halloween has more than any of
them; the 1978 crew cut paper leaves, painted them, and collected them after
each scene to use again; and Samuel Johnson's 1755 dictionary guessed bonfire
came from the French *bon*.

### Night 33 is the 1 that is not settled, and it is the finale

"Samhain: the night the year turns" leans on Samhain as the Celtic new year.
That reading was proposed by Rhys and Frazer in the late 1800s and **is
disputed**. What is attested is the dark half of the year: Cormac's Glossary of
about AD 900 gives November 1 as the first day of winter, and a monastic rule
from the 500s says the same. The `fact` field now carries that version and the
row is marked `verified: partly` with the dispute written into it.

The hook itself is fair read as the turn between the 2 halves, so it stays. What
could not be checked from here is the body text of the existing reel, which is
already scheduled for 10/31 on Instagram and TikTok. **Somebody has to watch
that reel before it runs.** If it says new year, it is on the losing side of a
real argument on the biggest night of the run.

Night 17 is marked `n/a`. "The series that ran the book fair" is a
characterization, not a claim with a truth value.

The 5 nights that published before 10/04 are marked `n/a, published before this
pass and not re-read`. Refusing a night that already went out fixes nothing, so
the gate is scoped to today forward and those rows say plainly that they were
not part of this.
