# Cesa's channel: posting standard

**@cesasgoldenyears is a conversion channel now, not a scrapbook.** Amanda's call, 2026-08-26.
Every post on that account carries a keyword CTA. No exceptions.

## The live keywords on that channel. RE-READ FROM SOURCE 2026-09-11.

**This section said "the 2 live keywords." There are 3, and the gate status was wrong.**
Corrected against `blotato_list_automations` on 2026-09-11.

| Keyword | Delivers | Blotato ID | Email gate? |
|---|---|---|---|
| CESA | The Cesa guide, 19 Years Old, 10 of Them Mine | 2952 | **No** |
| CONSIDER | Consider This newsletter | 2954 | **No, not any more** |
| SEASONAL | Consider This newsletter | 4011 | **Yes** |

All 3 are LIVE. 2 corrections to what this file used to say:

1. **SEASONAL (`4011`) has been live on this channel since 2026-09-01** and this file never
   recorded it. It is the seasonal campaign's automation, running on Cesa's account.
2. **`2954` CONSIDER no longer gates.** This file said it "still gates and still needs the
   daily sync in its path." There is no `emailGate` on `2954` as of 2026-09-11. It sends a
   button to `consider-this.subscribepage.io`, the same shape as CESA. `4011` SEASONAL is now
   the only automation on this channel that gates, so it is the only one that needs the daily
   sync in its path.

**`2952` CESA no longer uses an email gate** either — Amanda removed it 2026-09-08 after the
gate cost the first real lead, so CESA sends a button straight to
`cesa-guide.subscribepage.io` and the landing page captures the address.

### CESA also catches grief, deliberately

`2952` carries these keywords live: "just passed", "recently passed", "passed away",
"he passed", "she passed", "lost my", "miss her", "miss him", "got to see", "only got".

This matters for the holidays. People miss their dogs in November and December and they will
say so in her comments, and the guide reaches them automatically. **So the grief on this
channel arrives from the audience and gets met with something useful, while Cesa's own
captions stay exactly as unbothered as she is.** That division is correct and needs no change.
It is also why the holiday lane does not need a single sad post in it.

## The CTA rule for this channel

- Every post ends with `Comment CESA and I'll send you what I wrote about her.` or
  `Comment CONSIDER and I'll add you.`
- Alternate them. Roughly 2 CESA posts to 1 CONSIDER post, because CESA is the offer that
  matches why people followed her in the first place.
- Never post to this channel with no CTA. That was the old pattern and it converted nothing.
- Keep the tone hers: the specific real detail, not sentiment. The 3 feet of floor, the taped
  outline, the 17 nicknames. Not "cherish every moment."

## VOICE. CORRECTED BY AMANDA 2026-09-11. THIS IS THE BIGGEST FIX ON THIS CHANNEL.

**Write from inside Cesa's head, not from across the room.**

Her words: *"we're giving it in third person, we're not giving it in point of view from Cesa
... go into the mind of the dog and think what the dog would be thinking as I'm filming her
... POV, you peed on mom's office floor, but we can get away with it because you're a cute
face. That's what I think is wrong with the content on Cesa's channel. She's growing
organically but she could do way better."*

She is right, and the proof is already in the queue. The 1 post on that channel written in
Cesa's POV is the strongest thing on it:

> **POV, you peed in Mom's office.**
> But you're 19, adorable, and fully aware that 1 sad little face gets the whole case
> dismissed. I cleaned it up and apologized to her. To HER.
> Follow along, she's never lost a case. *(post `3836004`)*

Everything else reads like a caption **about** a dog: *"She is 19 and bath day is not a
fight." "Her seat. Her blanket. Her sunbeam." "She has opinions about how I pet her."*
Those are Amanda narrating. They are warm and they are not wrong, and they are also why the
channel is growing slowly instead of fast.

### The rule

| Do | Do not |
|---|---|
| Cesa's POV. What is she thinking while this is filmed | Amanda describing Cesa from outside |
| "You" and "we", her running commentary on her own life | "She" as the subject of every sentence |
| Total unearned confidence. She knows she is getting away with it | Sentiment, wistfulness, "cherish every moment" |
| Dry, deadpan, a little smug. She is 19 and she runs this house | Cute-voice baby talk, misspellings, excessive emoji |

**She is not a sad old dog and she is not a prop.** She is an extremely old, extremely small
animal who has correctly concluded that the rules do not apply to her. That is the comedy and
that is the warmth, and it is the same joke every time: she is right.

**The grief stays offstage.** Amanda's own ache about a 19 year old dog belongs on Amanda's
channels, in Amanda's voice. Cesa's channel is Cesa's, and Cesa is not worried about anything.
Any post that reads as pre-grieving her is in the wrong voice on the wrong account.

## Caption shape that works here

1. **The POV hook.** 1 line, from her side. "POV, you peed in Mom's office."
2. The specific real detail, still in her voice. Her age, her spot, the thing she got away with.
3. The turn. What it says about her, delivered deadpan, never instructing the reader.
4. The keyword CTA.
5. 4 hashtags. `#seniordog #dogmom #chihuahua #cesasgoldenyears`

**Cross-posts to Amanda's own channels may stay in Amanda's voice.** This POV rule governs
`@cesasgoldenyears`. On Amanda's accounts, Cesa is someone Amanda is telling you about, which
is a different and also correct job.

## The gap this standard was written to fix

On 2026-08-26 the channel had 2 live keyword automations and **zero scheduled posts**. Live
capture with nothing driving it captures nothing, which is exactly what the first daily lead
sync found: 0 triggers across every active automation.

Cross-posting Cesa material to the main accounts is fine and already happens, but the
dedicated channel is where the audience self-selected. It needs its own queue.

## Standing job

The daily lead sync (routine trig_0123dXXH4Gn978bHSD6gehCZ, 13:00 UTC) pulls captured
addresses from the DM threads into the matching MailerLite group. Joining the group is what
fires the delivery automation, so the group assignment IS the delivery.


---

## THE HOLIDAY LANE, 2026-09-11

`DRAFT_0911_cesa-holiday-lane.txt`. 21 posts, Nov 1 to Jan 1, nothing scheduled.

**21, not 62.** Her channel already runs daily at 00:10 UTC and does not need replacing. The
lane is the nights the season actually reaches her; every other night keeps running normal
Cesa content. 62 would have meant inventing 62 scenes in her house, and nothing about her, the
house or Amanda's life gets fabricated. So every caption uses only details already in her own
published posts, and everything I do not know sits in a SHOT line as a direction rather than
being asserted as fact in a caption.

**The build enforces the voice.** It refuses to write the file on: a hook that is not a POV
hook, a sentence starting with "She" (the outside voice Amanda diagnosed), sentiment or grief
language from a blocklist, a post with no SHOT note, em dashes, hashtags outside 4 to 5, or a
CESA to CONSIDER ratio off the 2 to 1 standard. It currently lands at exactly 14 to 7.

**The cruise, Nov 5 to 11.** Not a gap; the queue posts without her. 2 posts fall in that
window and both are written to assert nothing about who is in the house or where Amanda is,
because that is the one thing that cannot be known in advance. The build fails a cruise-window
caption that says "mom" or "my" or claims anyone's presence.

**TikTok gets a different CTA.** @cesasgoldenyears on TikTok has no comment-to-DM, so
"Comment CESA" is a dead instruction there. The file carries the bio-link replacement for both
keyword types.

**Open for Amanda:** whether SEASONAL joins the keyword rotation on this channel during the
campaign. It would work and it is already live here, but this standard says CESA is the native
ask at roughly 2 to 1, so changing the mix is her call and the lane does not assume it.

**Deliberately not used:** the xoloitzcuintli, the dog that carries souls across the river in
Aztec belief. It is a genuinely great fact and it is in the main campaign on Nov 4 instead.
On a 19 year old dog's own channel it reads as pre-grieving her, which is the one thing this
standard forbids.
