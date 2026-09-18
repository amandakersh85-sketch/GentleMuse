# /cleanup, the page that has to exist

Drafted 09/18/2026 during an away session. **This is copy, not a publish.**
Nothing was changed on gentlemuse.co. Publishing to the live site was not
unlocked for this session, and this page is Amanda's to put up.

## Why this is the highest-value page in the business right now

The CLEANUP automation went live this morning and was paused this afternoon.
Its button reads `See the $750 plan` and points at `gentlemuse.co/cleanup`,
which answers 404. Every person who commented CLEANUP got a real message, a
real price and a dead link.

The message also says, in its own words: **"The page has everything, terms
included."** So the page is not a nice-to-have that would help conversion. It is
a promise already made to every buyer who has seen the DM. Nothing about the
offer needs deciding. The DM decided it. This page has to carry it.

Everything below comes from the live automation 7213 and 7214 text, from the
BUDGET and DECISION credit lines already published, and from nowhere else.
Where a term is genuinely unknown, it is listed at the bottom as a question
rather than guessed at.

---

## The copy

### Hero

**The Chaos Cleanup Plan**

You've got 5 things you know are broken and no free afternoon to work out which
one to fix first. I'll tell you. In order, with who should do each one and what
it should cost.

`[ Buy the plan, $750 ]`

*Paid once. Up to 2 a month, so it may be next month.*

---

### The line that saves us both a call

I don't do the fixes.

This is the audit and the order of operations. You get a map of what's wrong,
ranked, with a person and a number next to each item. What you do with it is
yours: hand it to your own people, hand it to freelancers, or hand it back to me
and we'll talk about me running it.

If what you actually want is somebody to do the work, say so now and we'll skip
to that conversation instead.

---

### Who this is for

You're making money. The business works. What's stopped scaling is you, because
every decision still routes through your head and your head is fully booked.

This is not a competence problem and I'm not going to treat it like one. You
built all of this. You just haven't had a clear Thursday since 2024.

### Who this isn't for

Somebody who wants to be taught how to do it themselves. There are cheaper and
better ways to learn this than paying me. This is for the woman who'd rather
buy the answer back than go and get it.

---

### What you get

**1. The audit.** I go through your offers, your pages, your emails, your
automations and your tools, and I write down what's actually happening. Up to 10
tools and 3 offers.

Everything is view-only. **I never ask for passwords.** Not once, not for
anything. If a tool can't be shown to me read-only, we work from screenshots.

**2. One live call.** We go through what I found. You tell me what I got wrong,
because you know things about your own business that no audit surfaces.

**3. Your 30 day roadmap, in writing.** Up to 5 fixes, in the order they should
happen, with who should do each one and roughly what it costs. Not a list of
everything wrong. The 5 that are holding the rest up, sequenced.

---

### How the order works

1. You buy the plan.
2. I send you the access checklist. Read-only links, no passwords.
3. I audit.
4. We get on the call.
5. Your roadmap lands in writing.

---

### If you've already bought from me

If you bought **Done Reacting to Money**, that $37 comes off this.

If you bought **The Decision Map**, that $47 comes off this.

Email me before you buy and I'll send you the adjusted link.

---

### The terms, in plain words

- **$750, paid once.** Not a retainer. Not a subscription.
- **Up to 2 of these a month.** The audit is the slow part and I'd rather do 2
  properly than 4 badly.
- **Refunds happen only when I can't deliver.** If I take your money and don't
  produce the audit, the call and the roadmap, you get all of it back. Changing
  your mind after the work is done isn't a refund, and I'd rather say that here
  than in an email later.
- **I don't do the fixes.** Said twice on purpose.
- **View-only access, always.** I never hold a password of yours.

---

### Still deciding

Email me at amanda@gentlemuse.co and ask. I'd rather answer 3 questions than
take $750 from somebody this isn't right for.

If you'd rather see how I think before you spend anything, comment BOTTLENECK on
any of my posts and I'll send you the free check that finds which of the 5
things is holding the other 4 up.

---

## What Amanda has to supply before this can go up

These are genuinely unknown here. None of them is guessed at above, and each one
leaves a visible gap in the page.

1. **The buy button's destination.** The DM's button pointed at this page, so
   this page needs the actual checkout. Payhip, a Wix Stores product, or a
   Stripe link. The other 2 paid rungs are Payhip and the Fixed-Fee Project
   Deposit is Wix Stores, so either is already set up.
2. **The turnaround.** "Your roadmap lands in writing" needs a number of days
   after the call. The DM says 30 day roadmap, which is the roadmap's span, not
   the delivery time. Those get confused constantly and the page should say both.
3. **How the call gets booked.** A scheduling link, or she emails times.
4. **How long the call is.** The DM says 1 live call and no duration.
5. **Whether the 2 credits stack.** Somebody who bought both products has been
   told, in 2 separate live DMs, that each one comes off the Plan. Neither DM
   says only one applies. So as published, both do, and $84 comes off. The page
   above is written that way because that is what the promise says. If she wants
   only the larger to apply, the DMs have to change first, not the page.

## What was checked

- The copy above is reconciled line by line against the live dmMessage on
  automations 7213 and 7214, read from Blotato today. Every term the DM states
  appears here. No term appears here that the DM does not state.
- The credit lines are reconciled against the published BUDGET and DECISION
  messages, automations 448 and 451.
- Voice pass: no em dashes, no spelled-out numbers, contractions throughout,
  and nothing implying the reader is not capable.
- Prices appear only on a page surface, which `gm_offer_check.py` permits.
  There is no price in any caption, on-screen card or voiceover anywhere in
  today's work.
- `post-grader` is not installed in this environment, so this carries no grade.
  The 8 out of 10 floor still applies before it goes up.

## What happens the moment it's live

1. Amanda publishes the page.
2. `python3 filing-system/scripts/gm_offer_check.py --urls` to confirm it
   answers 200 rather than 404. That check is what caught this.
3. Reactivate automations 7213 and 7214.
4. Set OF-004 back to `live` in `offer-ladder.csv` and CLEANUP back to `live`
   in `magnet-map.csv`, then run the suite.
5. Monday's face script can switch its keyword from BOTTLENECK to CLEANUP.
