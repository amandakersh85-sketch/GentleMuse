# Full leak sweep, 2026-08-30

Every surface checked end to end: 151 scheduled posts, 15 MailerLite automations, 16
campaigns, 12 groups, 11 forms, 13 subscribers, 14 DM automations.

## Fixed in this sweep

### Dead and wrong links in the queue

| Post | Fires | Copy is about | Was pointing at | Now |
|---|---|---|---|---|
| `3797034` FB | Aug 31 | Consider This | **preview.mailerlite.io**, DO NOT USE list | consider-this |
| `3939624` LI | Sep 22 | Consider This | ai-guide | consider-this |
| `3939651` LI | Sep 24 | Consider This | ai-guide | consider-this |
| `3939608` FB | Sep 22 | Consider This | payhip Reset | consider-this |
| `3939603` X | Sep 21 | Press Play | payhip Reset | press-play |
| `3939602` FB | Sep 21 | Press Play | payhip Reset | PLAY keyword + press-play |
| `3939640` X | Sep 23 | AI guide | payhip Reset | ai-guide |
| `3939641` YT | Sep 23 | Press Play | payhip Reset | press-play |
| `3939593` IG | Sep 21 | AI guide | **nothing at all** | GUIDE keyword |

The Reset payhip link had become a catch-all footer. On unrelated posts that reads as a
deliberate default and was left. On posts whose copy is about a different offer it sends the
reader somewhere they did not ask to go, and those are fixed.

`3797034` was the urgent one. Firing Aug 31 with a `preview.mailerlite.io` link. **The August
sweep missed it because that sweep read post text and this link lived in `firstComment`.**
Any future link audit reads `text`, `firstComment` and `target.link`.

### Keyword CTAs on platforms that cannot fire them

`3939624` and `3939651` both said "Comment CONSIDER" on **LinkedIn**, which has no comment to
DM mechanism at all. Per KEYWORD-RULE those channels carry the direct link. Both rewritten.

### Same-minute self-cannibalization

Reels, TikToks and Shorts were publishing to one account in the same minute. On Aug 23 two
Instagram Reels went out 2 seconds apart and got 1,818 and 162 views. Fixed across Instagram,
TikTok, YouTube and Facebook. **Zero posts now fall within 30 minutes of another on the same
account.**

### Captions

6 Instagram captions cut from 616-699 characters to 290-390, one ask each. Detail and grades
in promo-engine/REACH-ANALYSIS.md.

## Checked and clean

- **All 15 MailerLite automations enabled.** Reset, 5 Bottleneck branches, Press Play, AI
  Guide, Cesa delivery, Cesa nurture, Cesa to Consider This, both newsletter welcomes, the
  JAT AI guide bonus, and the cross-invite.
- **All 11 scheduled campaigns correctly targeted.** JAT #002 on Sep 1 checks out:
  `is_eligible_for_sending: true`, `needs_repair: false`, no warnings, audience "In any group:
  Just Another Tuesday." The Sep 1 social post claiming "today's issue went out this morning"
  is accurate.
- **No stranded subscribers.** Nobody unconfirmed, nobody with `sent: 0`. Laura, who was
  stuck 4 days, is active and receiving.
- **Cesa delivery proven end to end.** `+cesatest` shows 1 sent, 1 open, 1 click.
- **No DO NOT USE link anywhere in the queue** after the fixes above.

## The real leak: Just Another Tuesday was never offered to the existing list

Consider This got a launch invite on Aug 20. It went to 9 people across every existing group,
pulled 3 opens and 1 click, and converted Mary.

**Just Another Tuesday never got one.** Its 3 subscribers are Amanda's own address plus 2
people who found it themselves. The 7 people on Gentle Muse Subscribers have never once been
told the second newsletter exists.

The cross-invite automation does not cover them. It triggers on joining a group, and all 7
joined before it was built on Aug 20.

**Prepared, not sent:** campaign `197253464357602578`, "DRAFT — Just Another Tuesday Launch
Invite (existing subscribers)." Targeted at Gentle Muse Subscribers, `recipients_count: 7`,
eligible to send, no schedule. It mirrors the Consider This invite that worked, uses the
winning short shape, leads with the automations story, and says plainly that this is the only
time she will ask.

**SENT 2026-08-31 15:03 UTC** on Amanda's word. 7 recipients, the full Gentle Muse
Subscribers group.

### It would have gone out broken

The pre-send check caught it. `create_campaign` stored the HTML **escaped**, so the body was
sitting in MailerLite as literal `&lt;div style="font-family..."&gt;` text. It would have
arrived as visible markup instead of a formatted email, to the entire list, as the first
thing most of them had heard from Amanda in weeks.

**Rule: after creating or updating a campaign, re-read the stored `content` before sending.**
A 200 response means the write landed, not that the write is correct. Same lesson as the
MailerLite PUT endpoints that return success while ignoring fields.

The fix needed `update_campaign` with raw markup, and that endpoint requires `name` even when
only `content` is changing; without it the call fails with "The name field is required."

Timing worked out. The invite landed Monday, JAT #002 goes out Tuesday 07:00, so anyone who
signs up gets a real issue within 24 hours instead of waiting a week.

## Honest state of the list

**CORRECTED 2026-09-01 by Amanda.** The table below originally counted 7 in Gentle Muse
Subscribers. That was wrong, and every percentage computed off it this session was inflated.

There are **5 real subscribers on the whole account**: Mary, Melissa, Nadia, christine and
Laura. Everything else is Amanda's own addresses or junk:

| Record | What it is |
|---|---|
| `amandakersh85@gmail.com` | Amanda |
| `amanda@gentlemuse.co` | Amanda |
| `+cesatest`, `+cesatest2`, `+cesaloop`, `+lptest` | Amanda's tests |
| `princesamaryelizabeth@gmail.com` (field name "Cesa") | Amanda's own signup. Same IP, 72.58.115.46, as her main address and her +lptest |
| `kendricklamar662@gmail.com` ("Sirkendrick") | junk from the July import, no IP, never opened |

| Group | Records | **Real people** |
|---|---|---|
| Gentle Muse Subscribers | 7 | **3** (Mary, Melissa, Nadia) |
| Just Another Tuesday | 3 | **2** (christine, Laura) |
| Consider This | 2 | **1** (Mary) |
| Cesa | 3 | **0**, all Amanda's tests |
| AI Beginner's Guide | 0 | **0** |
| Press Play | 0 | **0** |

### Only 3 of the 5 are alive

Lifetime opens per real subscriber:

| Subscriber | Sent | Opens | Reading? |
|---|---|---|---|
| Mary | 3 | 1, plus 1 click | yes |
| christine | 5 | 1 | yes |
| Laura | 2 | 1 | yes |
| Melissa | 8 | **0** | never once |
| Nadia | 8 | **0** | never once |

**Melissa and Nadia have never opened an email, across 8 sends each.** So the working
audience is 3 people. Consider This reaches 1 of them. Just Another Tuesday reaches 2.

Any open rate quoted against a group's record count is meaningless at this size. Count named
humans instead.

Consider This #001 reached 1 person. #002 reached 2. JAT #001 reached 2.

The AI Guide and Press Play groups have never had a single subscriber, despite live keywords
on 2 platforms and live landing pages for both. That matches the keyword audit exactly: no
real person has ever used a keyword. These are not broken pipes. Nothing has been poured in.

## Flagged, needs a decision

- **4 TikTok posts on @thegentlemuse2026 say "Full list is in my bio"** for the Press Play
  list. Per the per-account bio rule her bio holds her website, not that list. Either the bio
  changes or those 4 captions do.
- **The AI Beginner's Guide embedded form** (`195976901405181520`) is `active: false` with
  `has_content: false` and `double_optin: true`. It is an empty stub that has never been
  opened, and the live front door is the landing page, so it leaks nothing today. Worth
  deleting so it cannot be wired up by mistake later.


---

## Daily sync job rewritten, 2026-08-31

`trig_0123dXXH4Gn978bHSD6gehCZ`, now "Daily: DM email sync + keyword failure sweep."

It fired on 08-31 and did the right thing, but its prompt was a week stale: it described
ManyChat as a live collision risk and told the reader to check the CESA automations for an
emailGate they no longer have. Rewritten to match reality, and 3 things were added that the
old version would have got wrong:

- **followGate runs.** 5 Instagram automations gained one on 08-30. A run parked in "waiting"
  means the person has not followed yet and is normal. A run that reaches **"expired"** is a
  lost lead and now gets reported, because a string of those means the gate is costing more
  conversions than it earns and should come off.
- **`filter_status` on `list_subscribers` is unreliable.** Passing "unconfirmed" returned all
  13 subscribers regardless. The job now filters the returned data itself. It also looks for
  active subscribers with `sent: 0`, which is how Laura was found.
- **A baseline, so silence reads correctly.** No real audience member has ever used a keyword,
  so an empty result is the expected result right now rather than evidence the job broke. The
  first genuine capture is called out loudly.

### Today's run

Zero captures, zero failures, nobody stranded. All 3 emailGate automations (`2771`, `2772`,
`2954`) have never fired. 12 active subscribers, 1 unsubscribed, and that one is Amanda's own
`+cesaloop` test she cancelled herself 3 minutes after making it. `445` still shows only the
2 error 20102 failures from 08-28 and the 2 clean runs since.


---

## Correction 2026-09-01: the JAT invite reached 3 people, and 1 of them was a real reader

Reported yesterday as "7 recipients, 0 opens, and the subject line is the likely cause."
The delivery numbers were right. The conclusion was wrong.

The 7 recipients were Mary, Melissa, Nadia, Amanda's own address, her `+lptest`, the
`princesamaryelizabeth` signup and the `kendricklamar662` junk record. Of those, **3 are real
people, and only Mary has ever opened anything.** Melissa and Nadia are at 0 opens across 8
sends each.

christine and Laura, the other 2 live readers, never got the invite. Correctly: they were
already in the Just Another Tuesday group.

**So the invite had exactly 1 plausible taker and she did not open it that day. That is a
sample of 1.** The subject-line theory is withdrawn. Nothing can be concluded about copy from
one person not opening one email, and saying otherwise was reading a story into noise.

What does hold: 7 of 7 delivered, 0 bounces, 0 spam complaints, 0 unsubscribes. Sender
reputation intact.

The comparison drawn to the Consider This launch invite (9 sent, 3 opens, "33%") does not
survive either. That campaign also went mostly to Amanda's own addresses, and hers open at
75% and 62.5% while Melissa and Nadia sit at 0%. Those 3 opens were plausibly Amanda's own
inboxes. **It was never a 33% benchmark against real readers and should not be used as one.**

### The rule this produces

Before quoting any rate, subtract Amanda's own addresses and the junk records, then say the
number of named humans. At this size a percentage is a way of not saying "1 person."
