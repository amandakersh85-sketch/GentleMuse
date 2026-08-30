# Archive: the 10 duplicate DM automations, deleted 2026-08-30

Amanda approved deletion on 2026-08-30, conditional on them being true duplicates.
They were verified first, then archived here, then deleted. This file is the record.

## Why they existed

They were built on Aug 25-26 as the Sept 11 replacements for keyword flows still held by
ManyChat. ManyChat was disconnected on Aug 30 instead, eleven days early, so the originals
they were meant to replace never needed replacing. Every one of them shadowed a Blotato
automation that was already live and already working.

## The verification, before deleting anything

Each draft was matched against the live automation list on account, platform, keyword,
trigger type and post scope. All 10 matched a live counterpart on every axis. All 10 were
`isActive: false`. All 10 used `comment-received` with `postId: null`, exactly like their
live twin.

| Draft | Live twin | Account | Platform | Keyword | Twin still live? |
|---|---|---|---|---|---|
| 2953 | 445 | 45886 | Instagram | CESA | yes |
| 2781 | 445 | 45886 | Instagram | CESA | yes |
| 2782 | 432 | 30840 | Facebook | CESA | yes |
| 2773 | 1393 | 45886 | Instagram | CONSIDER | yes |
| 2774 | 1394 | 30840 | Facebook | CONSIDER | yes |
| 2775 | 1424 | 45886 | Instagram | GUIDE | yes |
| 2776 | 1422 | 30840 | Facebook | GUIDE | yes |
| 2777 | 435 | 45886 | Instagram | RESET | yes |
| 2779 | 1019 | 45886 | Instagram | PLAY | yes |
| 2780 | 1020 | 30840 | Facebook | PLAY | yes |

**Nothing was deleted that the live twin did not already do better.** Seven of the ten had
no link button at all and captured the email in the DM thread instead. That path does not
feed MailerLite; it needs a manual weekly bridge. Every live twin sends to a landing page
that writes straight into MailerLite. The drafts were the weaker half of the pair.

## Did they interfere?

Not while switched off. The hazard was future: a Sept 10 reminder existed that would have
told a session to activate all 10. With ManyChat already gone, that would have put Blotato
in a race against itself on every keyword, and Instagram gives a comment exactly one DM
slot. The loser fails silently with error 20102. That race already cost 3 of 4 leads on
Aug 28. The reminder was rewritten on Aug 30 to verify rather than activate, and now the
drafts are gone, so the trap cannot spring at all.

---

# Full copy, preserved

Kept because some of this copy is good and may be worth reusing in the live automations.

## 2953 — CESA / Instagram / email gate
**Gate:** Yes! This is the one about Cesa: 19 years old, 10 of them mine. Reply with your email address and I'll send it to you.
**DM:**
> Thank you for asking about her.
>
> Her guide is on its way to your inbox. It's called 19 Years Old, 10 of Them Mine. Worth checking your promotions tab if it isn't in the main one.
>
> She's 19. She picked her spot in the kitchen years ago and she does not intend to renegotiate it. She's slow to get up these days and she doesn't move out of the way like she used to, so I design around that now instead of asking her to be quicker.
>
> If your dog has a spot, measure it before you rearrange the room, not after. I learned that one the hard way.
>
> Amanda, The Gentle Muse

## 2781 — CESA / Instagram / email gate
**Gate:** same as 2953
**DM:**
> Sent.
>
> She's 19 and she has picked her spot in the kitchen and she does not intend to renegotiate it. She's slow to get up these days and she doesn't move out of the way like she used to, so I design around that instead of asking her to be quicker.
>
> If your dog has a spot, measure it before you rearrange the room, not after.
>
> Amanda, The Gentle Muse

## 2782 — CESA / Facebook / email gate
Identical body to 2953.

## 2773 — CONSIDER / Instagram / email gate + button "Sign up here" → consider-this.subscribepage.io
**Gate:** Yes! Consider This is 1 short email a week: 1 overlooked thing in your home, what's actually going on with it, and whether it's worth 2 minutes. Reply with your email address and I'll add you.
**DM:**
> You're in. Recent issues covered the washer gasket that never gets clean, why microwaving a sponge doesn't sanitize it, and the furnace filter that's rated highest but wrong for most houses.
>
> No 40-step routines. No pressure to buy anything.
>
> Hit reply and tell me the 1 spot in your home that's been bugging you. It helps me pick what to write about.
>
> Amanda, The Gentle Muse

**Worth stealing:** the 3 concrete examples in line 1, and the reply prompt at the end. The
live `1393` is vaguer and asks for nothing back.

## 2774 — CONSIDER / Facebook
Identical to 2773.

## 2775 — GUIDE / Instagram / button "Get the AI guide" → ai-guide.subscribepage.io
**DM:**
> Here it is. 59 pages, plain language, free, and no account needed to read it.
>
> I wrote it because I couldn't find it. Everything out there assumed I already knew the vocabulary, or it was a 40-step framework built for someone with a team. I had a shift to work and 1 income.
>
> You do not need to be 10 years ahead on AI. About 10 hours is enough.
>
> Amanda, The Gentle Muse

**Worth stealing:** "I had a shift to work and 1 income" is the strongest line in any of the
10. The live `1424` says "AI intimidated me at first too," which is softer and less specific.

## 2776 — GUIDE / Facebook
Identical to 2775.

## 2777 — RESET / Instagram / button "Get the checklist" → payhip.com/b/9FE2U
**DM:**
> Here's the Gentle Self-Reset Checklist. Free.
>
> The only instruction I'll give you: don't do all of it. Pick 1 line, the one that feels smallest right now, and do that. The rest will still be there tomorrow.
>
> I made it when I had 13 browser tabs open and files on my phone I could no longer decode. Not disorganized. Just carrying too much at once.
>
> Amanda, The Gentle Muse

**Note:** this is the same copy as live `2778` on Facebook. The Instagram twin `435` uses
older copy. Worth aligning.

## 2779 — PLAY / Instagram / email gate, no button
**Gate:** Yes! The list is 10 books you can listen to for free. 5 free forever, no account and no card. The other 5 are free library borrows. Reply with your email address and I'll send it over.
**DM:**
> Sent. 10 books you can listen to for free while you fold laundry.
>
> A library card is not a subscription. Nothing to cancel, no trial clock, you are never charged. You can apply online in about 5 minutes with proof of address.
>
> When a book has a waitlist on one app, check the other. They stock differently. That's how half my list stays free.
>
> I'd rather you finish 2 than bookmark 50.
>
> Amanda, The Gentle Muse

**Worth stealing:** the "library card is not a subscription" paragraph answers the real
objection. The live `1019` does not address it.

## 2780 — PLAY / Facebook
Identical to 2779.
