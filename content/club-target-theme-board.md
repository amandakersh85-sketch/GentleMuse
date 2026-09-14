# Club Target Theme Board

## How the board actually gets here

**Updated 14 Sep 2026.** The egress policy has loosened. `obs.duel.me` and the
tile image CDN `d3k81ch9hvuctc.cloudfront.net` now both return 200, so the old
"everything is 403" note below is out of date and the challenge names are readable
without her. Only `club.target.com` itself still fails, and not on the network: it
resolves fine and is simply a JavaScript app behind her login that serves an empty
shell to any non-browser client. Do not re-test that one.

**The route in is Gmail.** Club Target emails the week's challenges every Monday
around 8 AM Central from `target@duel.technology`. The email carries the direct
challenge links. It does NOT carry the challenge names, those are baked into tile
images on the blocked CDN.

So: Claude gets the links automatically, Amanda taps them and screenshots.
Screenshots are readable, so that closes the loop.

Routine `trig_018yBeoQES7zGTiZJnztqJJp` pulls this every Monday at 8:40 AM Central.

## Cadence, measured from 3 weeks of emails

| Email | Subject | New challenges |
| --- | --- | --- |
| 17 Aug | New Ideas Made for Your Feed | 4 |
| 24 Aug | New Week. New Creative Ideas | 4 |
| 31 Aug | Start Your Fall Content Refresh | 4 |

**4 new challenges a week.** Codes do not repeat week to week, except `txd` which
appears to be a long running evergreen one. Challenges accumulate rather than
replace, which is the whole argument for a batched store run every 2 to 3 weeks
instead of a weekly trip.

## HOW TO NAME A CHALLENGE WITHOUT ASKING HER. Works as of 14 Sep 2026.

**The tile image CDN is no longer blocked.** `d3k81ch9hvuctc.cloudfront.net`
returns 200. So do `obs.duel.me` and `indd.adobe.com`. Only `club.target.com`
itself is still unreadable, because it is a JavaScript app behind her login.

That means the challenge NAMES can be read straight out of the weekly email with
no input from Amanda at all:

1. `mcp__Gmail__get_thread` with `messageFormat: FULL_CONTENT`. The result is too
   large to read inline, so parse the saved file with python3.
2. Pull `htmlBody` and regex every
   `cloudfront.net/company/SmsXRV/images/<id>.png`, keeping first-seen order.
3. `curl` each one. The challenge tiles are the square-ish ones, roughly 521x542
   in a 3-challenge week and 521x530 in a 4-challenge week. Skip the 223x73
   buttons, the 561x249 banners and the 1201-wide creator spotlight.
4. Read the PNGs. Each tile carries the challenge name, a one-line brief, the
   eligible platforms and the tier gate.
5. Tile order matches challenge-link order in the plaintext body.

**The tiles do NOT carry the hashtag or the closing date.** Those still only come
from the challenge card in the portal. So this method gets the name and the brief
for free, and Amanda only needs to supply the tag.

## LIVE NOW, dropped 14 Sep 2026, "Switch Up Your Content This Season"

4 challenges. All Instagram plus TikTok, all Tier 3+.

| Link | Name | Brief | Hashtag |
| --- | --- | --- | --- |
| `t/0pp2` | **Meet Target Beauty Studio** | Explore Target's new beauty destination and share your faves in a haul or first-look review | unknown |
| `t/0pp9` | **The Fall Outfit Edit** | Share a GRWM with the layers, denim and wardrobe staples you'll style all season | unknown |
| `t/0q0x` | **Set the Halloween Vibe** | Create a decorate-with-me moment featuring seasonal touches transforming your space | unknown |
| `t/tt7` | **Share your budget finds** | Repeatable. "Anytime you spot something you love, you can come back to this challenge once a month" | unknown |

`tt7` is the evergreen slot, the same role `txd` played in August. It is explicitly
monthly and repeatable.

**The Fall Outfit Edit asks for a GRWM.** Amanda is not on camera, so the standard
read does not fit. Her denim rack footage and the dress and sweater she bought can
carry a layering flat-lay or rack-to-cart version instead. Worth confirming with her
before producing.

## Dropped 7 Sep 2026, "Fresh Ideas to Fuel Your Creativity". NAMES NOW KNOWN.

3 challenges. All Instagram plus TikTok, Tier 3+.

| Link | Name | Brief | Hashtag |
| --- | --- | --- | --- |
| `t/0pdf` | **On The Menu: Wellness Refresh** | A "what I eat in a day" with feel-good bites and sips | unknown |
| `t/0pdm` | **Game Day Lineup** | "Turn your tailgate must-haves into a packing checklist for kickoff and beyond" | unknown |
| `t/0pdq` | **Family Game Night Finds** | Share how you spend family time and turn it into a content moment | unknown |

### Game Day Lineup: the apparel reading was wrong

The tile settles it. The brief says **tailgate must-haves as a packing checklist**,
and the artwork is an Igloo cooler, a handheld fan and a pack of Olipop. It is gear
and drinks, not clothing.

Amanda shot **sportswear** on 12 Sep. That is the wrong read and would likely score
0. She already offered to go back for chips, dips and drinks. She should. Add a
cooler and a portable fan to the list if the store has them.

### Family Game Night Finds: her 12 Sep footage fits

She filmed the entire gaming wall and framed it as family game night. The tile shows
LEGO, a window cling kit and Jackpot Roll. Direct match, no reshoot needed.


## Dropped 31 Aug 2026, "Start Your Fall Content Refresh", "Start Your Fall Content Refresh"

Names and closing dates unknown, awaiting screenshots.

| Link | Name | Hashtag | Closes |
| --- | --- | --- | --- |
| https://club.target.com/t/0p19 | unknown | unknown | unknown |
| https://club.target.com/t/0p1f | unknown | unknown | unknown |
| https://club.target.com/t/0p1c | unknown | unknown | unknown |
| https://club.target.com/t/txd | unknown, recurring code | unknown | unknown |

The subject line says fall, so at least some of this batch is fall styling. That
matters: Amanda has a sweater outfit ready and only needs brown leggings.

## Dropped 24 Aug 2026, may still be open

| Link |
| --- |
| https://club.target.com/t/0n9n |
| https://club.target.com/t/0n97 |
| https://club.target.com/t/0nas |
| https://club.target.com/t/0n9f |

## Dropped 17 Aug 2026, may still be open

| Link |
| --- |
| https://club.target.com/t/0kvn |
| https://club.target.com/t/0kyp |
| https://club.target.com/t/0kyt |
| https://club.target.com/t/0kyz |

That is **12 challenges from the last 3 weeks**, minus whatever has closed. At 30
points each on TikTok, the open subset is worth up to 360 points in one store run.

## Expired unfilmed

Fresh Home Finds and Game Day Throwback, deadline 30 Aug 2026. 60 points. Amanda
was at work and could not make a store run. Exact hashtags were never confirmed.

## Banked, TikTok published

| Theme | Hashtag | Published |
| --- | --- | --- |
| Everyday Essentials | #TargetEverydayEssentials | 20 Aug |
| HeyDay Tech August | #HeyDayTechAugust | 20 Aug |
| Lunch Throwback | #TargetLunchThrowback | 21 Aug |
| Budget Finds | #TargetBudgetFinds | 21 Aug |
| Target Fave | #TargetFave | 21 Aug |
| Fall First Looks | #TargetFallFirstLooks | 21 Aug |
| College MVPs | #TargetCollegeMVPs | 21 Aug |
| Pet Faves | #TargetPetFaves | 21 Aug |
| Good and Gather Faves | #TargetGoodandGatherFaves | 21 Aug |

## Scheduled, footage exists

| Theme | Hashtag | TikTok |
| --- | --- | --- |
| Cat and Jack Summer | #TargetCatandJackSummer | 2 Sep, 10 AM Central |
| Little Finds, Adornia | #TargetLittleFinds | 3 Sep, 10 AM Central |
