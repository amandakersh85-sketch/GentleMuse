# Christmas, 29 nights

The evenings of 11/27 to 12/25, which is Christmas Day itself. 1 fact a night on
all 4 main accounts: Instagram 45886 and TikTok 41488 at 6:00 PM Central,
Facebook 30840 and YouTube 36129 at 6:30 PM. Same shape as `halloween-33/` and
`thanksgiving-26/` so C13, C14, C15 and C16 read it with no change to any script.

Drafted 10/04. Not announced, so `campaign-targets.csv` has it at `Live=no` and
nothing is scheduled against it. December captions are due for approval by
11/14.

## The facts were checked before they were written, not after

This is the only one of the 3 waves done in that order. The Thanksgiving plan
was written from memory and then checked, and 4 of its 26 rows were wrong. Here
every one of the 29 was read against a source first, so every row ships
`verified: yes` with 1 or 2 citations carrying URLs.

5 of these are facts whose popular version is wrong, which is why they are in:

- the candy cane's Christian symbolism was invented in a **1996 children's
  book**. Cards before 1900 show the canes plain white
- **Coca-Cola did not put Santa in red.** Nast had him in red by 1881, and a red
  Santa with a Coke ran in 1930, a year before the paintings everyone credits
- there is **no mention of Christmas anywhere in Jingle Bells**
- *It's a Wonderful Life* became a classic because nobody filed a renewal in
  1974 and stations could run it free for 19 years
- the **earliest sunset is about 12/07**, a fortnight before the solstice

2 rows name their own uncertainty inside the sources cell rather than claiming
more than was found. Night 10, the Jingle Bells row, rests on the lyrics rather
than on the Thanksgiving performance story, because Medford and Savannah dispute
where and when it was written. Night 18 claims the AD 336 record and the
Chronograph of 354 and stops, because why 12/25 was chosen is still argued over
and both the Annunciation calculation and the Saturnalia theory are proposals.

## 29 images, 1 per fact

Same rule as Thanksgiving. Amanda, 10/04: "a stylized version per day, per
fact." The same render goes to all 4 accounts, no per-platform variants and no
rotation.

The image is the room the fact happened in: a short specific scene, 1 light
source, no people, no faces, objects doing the work. Halloween was candle and
fog, Thanksgiving is lamplight and wet leaves, this is snow light and firelight.
29 distinct `plate_desc` lines, checked for duplicates in the build.

## The sound is a different carol every night

Amanda, 10/04: "a combination of a rotation of all three options. But show
versions, because we want different feelings per different days. The feeling
needs to coincide with the fact. If it's a history fact... related to something
in that time era, we could use the orchestral, scratchy sounding dated, because
that would complement it." And: "preferably one different song per day for the
run."

Both halves of that are in the data. The `treatment` column is the 3 kinds and
the `bed` column is this night's own song:

| treatment | what it is | nights |
|---|---|---|
| `carol-scratch` | a dated scratchy orchestral recording | 9 |
| `carol-solo` | 1 instrument, sparse and close | 12 |
| `carol-full` | a fuller newly played arrangement, warm | 8 |

She named `carol-scratch` herself and it goes on the nights that sit in a
recorded era: the 1908 advent calendar, Rudolph in 1939, the 1843 card, 1870,
the 1848 engraving, White Christmas. `carol-solo` takes the old and the quiet
ones, the 300s, the solstice, the truce. `carol-full` takes the film nights, the
science nights and the finale.

**The naming of the 3 is mine, not hers.** She said "all three options" about
options offered in conversation that were never written into this repo, which is
the thing CLAUDE.md says not to let happen. What is hers is quoted above: 3
kinds in rotation, matched to the feeling, the dated orchestral one for period
facts, a different song each night. If the 3 she had in mind were different
kinds, the column names change and nothing else does.

### 29 songs, and the recording is the part that bites

All 29 tunes are public domain as compositions: Silent Night, Greensleeves, the
Coventry Carol, Divinum Mysterium, and so on down the list in
`reel-factory/beds/beds.csv`.

**A tune being out of copyright does not make a recording of it free.** Every
recording is owned by whoever made it. This is the single most likely way this
wave gets muted or claimed on 4 accounts at once, and it is why the beds here
are 29 separate rows rather than 3: each one has to be newly played or provably
public domain in its own right.

`White Christmas` is on night 27 as the fact. It is **not** the bed. Berlin's
song is still in copyright. The bed that night is Away in a Manger.

## The clocks, which are the reason the dates look wrong

Central goes to standard time on 11/01, so every night of this wave and every
night of Thanksgiving runs at UTC-6. 6:00 PM Central is **00:00 UTC the next
morning.**

Each row therefore carries 2 dates:

- `date` is the **UTC day the post lands**, which is what every gate and loader
  in this repo already reads
- `evening` is the **Central day the audience sees it**, which is what `left`
  counts and what the wave means by a night

In September and October those were the same day, which is why nothing had to
say so until now. The first Christmas night is the evening of 11/27 and the UTC
date on its row is 11/28.

This was found while drafting this wave and the Thanksgiving plan had the same
error: it was written with `23:00Z`, which is 5:00 PM Central once the clocks go
back, an hour early on all 26 nights. Both plans are corrected.
`halloween-33/make_schedule.py` still subtracts a hardcoded 5 hours, which was
right for every Halloween night and is wrong for every night of these 2 waves.
The Christmas loader does not exist yet, so it can be written correctly instead
of being corrected later.

## Before this ships

1. **29 songs to source**, 1 per night, newly played or provably public domain.
   `reel-factory/bed.mjs` **refuses** a render whose bed has no file, so every
   night of this wave fails to build until its own song exists. That is the
   intended behaviour and it is also the biggest single blocker in the repo
   right now: 29 here plus 9 for Thanksgiving is 38 files.
2. **29 images to generate** from the `plate_desc` lines. Blotato
   `create_visual` is 50 credits each, so 1,450 for this wave and 1,300 for
   Thanksgiving. The balance on 10/04 was 2,644. At 1 attempt each that is 106
   credits short; at the rate Halloween actually ran, 1.35 plates a fact, it is
   about 3,700 credits needed and roughly 1,000 short. Nothing has been bought.
   The free fallback is the typography-only composition that 9 Halloween nights
   used.
3. **No loader.** Halloween ships from a GitHub job that reads its own plan.
   Thanksgiving and Christmas have no equivalent. Whoever writes it works in
   Central and converts, per the section above.
4. **`left` counts Central evenings and no gate knows that.** Nothing states a
   number of nights left in any caption here, so C04 has nothing to check. If a
   trailer is posted that names a number, C04 needs to read `evening` and not
   `date`, or it will be off by 1.
5. **Live=no, and only 1 wave can be live at a time.**
   `gm_cadence_check.load_target` returns the first row with `Live=yes`. The
   handover from Thanksgiving is the evening of 11/27 and it is a manual edit on
   1 day with nothing to remind anyone, which is now the 3rd wave with that same
   note on it.
