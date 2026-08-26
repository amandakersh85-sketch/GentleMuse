# Cesa's TikTok bio link — what's done, and the one step only Amanda can do

**Goal (Amanda's, 2026-08-26):** @cesasgoldenyears on TikTok gets its **own** Cesa landing
page as its link in bio. Not gentlemuse.co/tiktok. Not Amanda's link tree. Cesa's own page.

---

## The blocker, stated once

**MailerLite's API does not expose landing pages.** This is not new and it is not a guess.
It is already written in this repo in 3 places from earlier in the build:

- `promo-engine/day-60-handoff.md` line 11
- `promo-engine/CONFERENCE-BRIEF-AVERY.md` lines 78-79
- `promo-engine/ROTATION-TEST.md` line 116

Re-verified 2026-08-26 against the live tool, not from memory:

| Tool | What it actually accepts | Verdict |
|---|---|---|
| `create_form` | name, type, groups. Nothing else. | Creates an empty shell |
| `update_form` | **name only** | Cannot add content, cannot activate |
| `get_more_tools` (asked for landing pages explicitly) | "we have shown you the full tool list" | No such tool exists |

That is why `consider-this.subscribepage.io`, `ai-guide.subscribepage.io` and
`press-play.subscribepage.io` all exist and a Cesa one does not: **Amanda built those 3 by
hand in the MailerLite dashboard.** Cesa's has to be built the same way. It is the only
piece of this funnel that cannot be done from code.

---

## Everything downstream is already wired and waiting

Nothing else is blocking. The moment the page exists it works end to end:

| Piece | ID | State |
|---|---|---|
| Cesa group | 196024300390581479 | Live |
| Cesa Guide Delivery automation | 196289160620803395 | **ENABLED**, 3 steps, fires on joining the group |
| Cesa form (empty shell) | 196289170922014393 | Already points at the Cesa group |
| Guide PDF, publicly hosted | see below | Live, no auth |
| CESA keyword, Amanda IG | Blotato 445 | ACTIVE, email gate + guide button |
| CESA keyword, Amanda FB | Blotato 432 | ACTIVE, email gate + guide button |
| CESA keyword, Cesa IG | Blotato 2952 | ACTIVE |

So a person who signs up on the new page lands in the Cesa group, and the delivery
automation sends the guide with no further wiring.

---

## The 3 minute dashboard job

Fastest route is to duplicate a page that already works rather than start blank.

1. MailerLite → **Sites → Landing pages**
2. Duplicate **consider-this** (its layout is already proven)
3. Rename it `cesa`, so the address becomes `cesa.subscribepage.io`
4. **Set the group to `Cesa`** (196024300390581479). This is the step that makes the
   delivery automation fire. If the group is wrong, signups go nowhere.
5. Paste the copy below
6. Publish

### Copy, ready to paste

> **Eyebrow:** A free guide, for the ones who slowed down
>
> **Headline:** 19 Years Old, 10 of Them Mine
>
> **Subhead:** What living with a very old dog taught me about the room she lives in.
>
> **Body:**
> She picked her spot in the kitchen years ago and she does not intend to renegotiate it.
>
> She's slow to get up these days. She doesn't move out of the way like she used to. For a
> while I kept asking her to be quicker, without ever saying it out loud, and then one
> afternoon I moved what sits on the counter and realized I had also moved where I stand
> while I wait. Which put me directly over her.
>
> So now I tape out her spot at the same time I tape the appliance footprint. Where she
> lies and the path I walk carrying something hot should not be the same 3 feet.
>
> That's the whole guide. Not training. Not a routine. Just the small adjustments you make
> to a room once the dog in it has earned the right to be slow.
>
> **What's inside:**
> 1. Measure her spot before you rearrange, not after.
> 2. The 3 feet that should never be both her bed and your path.
> 3. Traction, and why the pretty floor is the hard one.
> 4. Walk the house at her height. You will find things you cannot unsee.
> 5. What to stop asking her to do, and design around instead.
>
> **Button:** Send it to me
>
> **Fine print:** 1 email with the guide, then 1 follow-up 4 days later. That's it.
> Leave any time, no hard feelings.

The same copy is already laid out and styled in `cesa-landing.html` in this folder if the
builder lets you import or if the layout is easier to copy visually.

---

## Then, in order

1. Paste `https://cesa.subscribepage.io` into the **@cesasgoldenyears** TikTok bio.
   That account, not the Gentle Muse one.
2. Tell Claude the URL. 3 scheduled TikTok captions get "Her guide is in my bio" added
   back: schedule ids **3835340**, **3835351**, **3835358**.
3. Add it to `promo-engine/ROTATION-TEST.md` as the Cesa destination.

---

## Interim, so tonight is not a dead end

The guide PDF is already publicly hosted and needs no signup:

```
https://database.blotato.io/storage/v1/object/public/public_media/5472a21c-0213-4305-8693-b19295e4d67e/2b25c0b1-87ce-4bec-8e2a-5ddd121b2774.pdf
```

That can sit in Cesa's TikTok bio right now. It hands people the guide immediately.
**It captures no email**, so it grows trust and not the list. It is a stopgap for the days
between now and the real page, not the answer.

---

## Why the captions currently say no such thing

As of 2026-08-26 the 3 Cesa TikTok captions end on "Follow along for more of her." and
nothing else. The bio-link line was removed on purpose, because per Amanda's own rule a
"link in bio" CTA is only valid when the bio points at a converting page, and hers did not
yet. That also matches the post that actually performed: the Aug 26 TikTok that worked
closed on exactly "Follow along for more of her." and nothing more.
