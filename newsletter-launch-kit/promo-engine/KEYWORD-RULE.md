# Standing rule: use the keyword every single time

**Set by Amanda, 2026-08-25.** On Instagram and Facebook, if a comment-to-DM keyword exists
for the offer, the post uses it. Not "link in bio." Not a bare URL. The keyword.

Reason it matters: a keyword captures the lead inside the platform, in a DM thread, where the
delivery is automatic and the person never has to leave the app. A bio link asks them to
leave, remember, and tap. The keyword converts, the bio link leaks.

## Live keywords

| Keyword | Offer | Confirmed on |
|---|---|---|
| CONSIDER | Consider This newsletter | Instagram, Facebook |
| GUIDE | AI Beginner's Guide | Instagram, Facebook |
| RESET | Reset Guide | Instagram, Facebook |
| PLAY | Press Play book list | Instagram, Facebook |
| CESA | Cesa guide | Instagram, Facebook |
| (none yet) | Just Another Tuesday | now TUESDAY, live in Blotato |

## Cesa's channel (@cesasgoldenyears)

| Keyword | Offer | Status |
|---|---|---|
| CESA | Cesa guide | live |
| CONSIDER | Consider This | live |

Every post on Cesa's channel should carry 1 of these 2. It previously carried none, so every
comment on that account was a lead that evaporated.

## How to write the CTA

- Instagram and Facebook: `Comment KEYWORD and I'll send it to you.`
- Put the raw link in `firstComment` instead of the caption. The keyword leads, the link is
  still there for anyone who prefers it, and the caption stays clean.
- TikTok cannot fire comment-to-DM. TikTok stays on `link in bio`.
- X, LinkedIn, Pinterest have no keyword mechanism. They carry the direct link.
- Add a share prompt wherever it fits naturally. Shares are what made the Press Play
  carousels reach roughly 100 views each.

## Closed item (was open until 08-25)

Just Another Tuesday now has TUESDAY, live in Blotato on both platforms: `2771` on Instagram,
`2772` on Facebook. It was never built in ManyChat and never needed to be. Every JAT post on
Instagram and Facebook should use it. The JAT signup URL is
https://just-another-tuesday-gm.subscribepage.io, verified in Drive 08/18, and both DMs carry
it on a "Get Tuesdays" button as well as gating for the email in thread.


---

## The one-DM-per-comment limit, and the 2026-08-28 failures

**Corrected 2026-08-29. An earlier note here said "do not reply to keyword comments."
That was wrong and it was not the cause.**

### How it actually works

Instagram does not send an auto reply. Nothing of Instagram's own races the automation.

The real constraint: **a comment can trigger exactly one DM.** That is Meta's private reply
rule. The first tool to claim that comment's DM slot wins. Anything else that tries after
gets error **20102, "The comment you are trying to reply to, already has a reply."** The
loser fails silently. Nothing shows on the post, and the lead is gone.

Replying publicly in the comment thread is a normal comment and is good for reach. Keep
doing it. The slot that matters is the DM slot, not the public thread.

### What happened on 2026-08-28

One contact commented CESA on 3 different posts. 3 different comments, so the "one per
comment" rule was not self inflicted by repeat attempts.

| Time UTC | Post | Blotato result |
|---|---|---|
| 16:33 | 6536249 | FAILED 20102 |
| 18:58 | 6533423 | FAILED 20102 |
| 19:32 | 6503252 | Sent |

Something claimed the DM slot on 2 of those comments before Blotato reached them. It was
not another Blotato automation: `445` is the only active CESA automation on account 45886,
verified against the live list.

### Prime suspect: ManyChat and Blotato are both holding the same keywords

ManyChat is live on the same Instagram account until the Sept 11 cutover, and it carries
the same keywords Blotato now carries. Two tools watching the same comment is a race, and
a race is exactly what intermittent 2-of-3 failure looks like.

**This cannot be verified from this workspace.** There is no ManyChat connector here. It is
a strong inference from the evidence, not a confirmed fact.

### The decisive test, 30 seconds

Have someone comment **CESA** on any post. Do not touch the comment. Then read the DM:

- **"15 pages" with a "Get the guide" button** to `cesa-guide.subscribepage.io` → Blotato won,
  the system is healthy.
- **Any other wording, or an older link** → ManyChat intercepted it. It is answering with
  stale copy that does not point at the new landing page.
- **No DM at all** → neither won. Pull the run log.

### The fix either way

**Do not let ManyChat and Blotato hold the same keyword on the same account.** Every keyword
already migrated to Blotato should be switched OFF in ManyChat now, not on Sept 11. While
both are live, every lead is a coin flip, and when ManyChat wins the person gets old copy
without the landing page.

Keywords to switch off in ManyChat: CESA, CONSIDER, TUESDAY, GUIDE, PLAY, RESET.


---

## CONFIRMED 2026-08-30: the race was the cause, and it is fixed

Amanda disconnected her accounts from ManyChat, then tested both automations by commenting
CESA across her two Instagram accounts. Both passed clean on the first try.

| Automation | Account | Before | After |
|---|---|---|---|
| `2952` | @cesasgoldenyears IG | never fired | **completed** 16:36:43 to 16:36:48 |
| `445` | @thegentlemuse2026 IG | 2 FAILED 20102, 1 sent | **completed** 16:48:31 to 16:48:36 |

`445` is the one that matters. It is the automation that failed twice on 08-28, and it
succeeded on the first attempt once ManyChat was gone. That moves the two-tool race from a
strong inference to a confirmed cause.

**Record: 3 failures out of 4 before the fix. 2 clean out of 2 after.**

Both DMs went out identical and correct: 15 pages, and a "Get the guide" button to
`https://cesa-guide.subscribepage.io`. Comment to DM sent in 5 seconds on both.

### The rule that comes out of this

**One tool per keyword per account. Never two.** Instagram gives a comment exactly one DM
slot. When two tools watch the same comment, one wins and the other fails silently with
20102, and the lead is gone with nothing visible on the post. This is the failure mode to
suspect first any time keyword conversion looks lower than the comment count.

The corollary for the Sept 11 cutover: the `[Sept 11 cutover]` drafts renamed **DO NOT
ACTIVATE** are all duplicates of a live automation. Activating one recreates exactly this
race, in Blotato against itself.

### How to test a keyword without waiting for real traffic

Amanda has 2 Instagram accounts, so each can test the other. Comment the keyword from
@cesasgoldenyears onto a @thegentlemuse2026 post to test `445`, and the reverse to test
`2952`. The commenter must not be the account that owns the post: an automation ignores its
own owner, which is also why this cannot be run from Blotato's API, whose comment tool posts
only as the post's own account.

---

## 2026-08-30: the wiring works. Nobody is using it.

ManyChat is disconnected, so every keyword automation was audited against its own run log.
A run is one execution. No run means the automation never fired, for anyone, ever.

| ID | Keyword | Where | Live since | Runs | Who |
|---|---|---|---|---|---|
| 445 | CESA | IG main | Aug 8 | 4 | Amanda's other account, testing |
| 435 | RESET | IG main | Aug 8 | 1 | Amanda, testing 08-30 |
| 1424 | GUIDE | IG main | Aug 16 | 1 | Amanda, testing 08-17 |
| 2952 | CESA | IG Cesa | Aug 26 | 1 | Amanda, testing 08-30 |
| 1393 | CONSIDER | IG main | Aug 16 | **0** | — |
| 1019 | PLAY | IG main | Aug 12 | **0** | — |
| 2771 | TUESDAY | IG main | Aug 25 | **0** | — |
| 2954 | CONSIDER | IG Cesa | Aug 26 | **0** | — |
| 432 | CESA | FB | Aug 8 | **0** | — |
| 1394 | CONSIDER | FB | Aug 16 | **0** | — |
| 1422 | GUIDE | FB | Aug 16 | **0** | — |
| 1020 | PLAY | FB | Aug 12 | **0** | — |
| 2772 | TUESDAY | FB | Aug 25 | **0** | — |
| 2778 | RESET | FB | Aug 25 | **0** | — |

**Not one real audience member has ever commented a keyword. Not once, on either account, on
either platform, in 22 days.** Every run in the system is Amanda testing.

Facebook is the starkest read: 6 live automations, zero runs between them, going back to
Aug 8.

This changes what the 08-28 failure meant. The race was real and fixing it was right, but it
cost 3 leads out of a lifetime total of 4, and all 4 were tests. The pipe was never the
bottleneck. Nothing is being poured in.

### The last 80 comments on the main IG account, sorted

Emoji, compliments on the dog, condolences about someone else's dog, conversation, spam.
Zero keyword attempts from anyone but Amanda. People are engaging warmly and never once
being moved to type the word. That is a CTA and reach problem, not a wiring problem, and it
is the thing worth attacking next.

### Keyword matching is case sensitive. Proven, not assumed.

On 08-29 at 15:26 a real follower commented "Keep playing I got somewhere you can strut too"
on post 6564622, account 45886. Automation `1019` watches that account for `PLAY` on any
post and was live. It did not fire. "playing" contains "play" in any case-insensitive
reading, so the match must be case sensitive.

Matching is also **substring, not whole word** — the schema says "fire when the comment
contains one of these keywords."

Those two facts together are a trap. The obvious fix for a case-sensitive matcher is to add
lowercase variants, and that is the wrong move here:

- add `play` and that same "Keep playing" comment DMs a stranger a book list
- add `cesa` and every "Princesa", "@cesasgoldenyears" and "Cesa is beautiful" fires
- add `consider` and "I'm considering it" fires
- add `guide` and "guidelines" fires

**So the single-casing automations were left alone.** `445`, `432`, `435`, `1393`, `1394`,
`1019`, `1020`, `1422`, `1424` still match uppercase only. Given that the real-world miss
rate is currently zero out of zero, closing a theoretical leak by opening a real misfire is
a bad trade.

Worth knowing, not yet worth acting on: `2771`, `2772`, `2778`, `2952` and `2954` already
carry all three casings. On Cesa's account that means an ordinary "Cesa is adorable" would
fire the guide DM. Arguably a feature on a dog account. Flagging it so it is a decision
rather than a surprise.

### The standing rule is unchanged and now unopposed

**One tool per keyword per account.** ManyChat is gone, so Blotato is the only thing holding
these keywords. The only way to break that rule now is to activate one of the 10
`DO NOT ACTIVATE` drafts, which would put Blotato in a race with itself. Do not.

---

## REVERSED 2026-08-31: the follow gates came off after 1 day

Amanda's call, and it is the right one. **Removed from all 5** (`445`, `435`, `1393`, `1019`,
`1424`) on 08-31. Her reasoning: they cost more than they earn.

The numbers back her. The gate can only ever act on someone who already wants something she
made, and the audit below shows that is nobody yet. So the upside was 0 followers and the
downside was friction on the single mechanism in the funnel that converts. When the first real
person finally comments a keyword, the last thing that should happen is being asked to do a
second thing before getting what they asked for.

Nothing was lost. The gates were live for roughly 22 hours and no automation fired in that
window, so no real person ever saw one.

**Standing rule: no followGate on any automation.** The daily sync job checks for one and
flags it rather than removing it, so a reappearance gets a decision instead of a silent fix.

The original write-up follows for the record.

## 2026-08-30 (SUPERSEDED): follow gate added to the 5 lead magnet keywords on @thegentlemuse2026

Amanda's goal is 500 Instagram followers, which is the threshold that unlocks her Club Target
affiliate account. `followGate` is now on every lead magnet keyword on her main account.

| Automation | Keyword | Gated |
|---|---|---|
| `445` | CESA | yes |
| `435` | RESET | yes |
| `1393` | CONSIDER | yes |
| `1019` | PLAY | yes |
| `1424` | GUIDE | yes |
| `2771` | TUESDAY | **no, deliberately** |

TUESDAY already runs an `emailGate`. Stacking a follow gate on top means follow, then hand
over an email, then finally get the thing. That is 2 hurdles in front of 1 offer and it will
lose people. One word from Amanda and it goes on, but it should be a choice, not a side
effect.

Gate copy, same shape across all 5, offer-specific in the middle line:

> One small thing first.
>
> Follow along, then tap below and [the thing] is yours. That's the only thing I ask for it.
>
> Amanda

Button: "I'm following".

**Facebook got nothing.** `followGate` is Instagram only and the API rejects it elsewhere.
Cesa's account (`2952`, `2954`) was also left alone: gating there grows @cesasgoldenyears,
and the 500 target is on @thegentlemuse2026.

### It does not bomb existing followers

This was Amanda's worry and it is the right worry. The gate holds the DM back **until the
contact follows**. Someone who already follows has already satisfied that condition, so they
skip the gate and get the guide immediately. The gate message only ever reaches someone who
is not following yet.

Read from the API contract, not tested live. To confirm in 1 comment: have an account that
already follows @thegentlemuse2026 comment CESA. If the guide arrives with no follow prompt,
confirmed.

### Honest expectation

**This will convert 0 people right now**, because 0 real people have ever commented a keyword.
See the audit above. The gate is correct and costs nothing, and it is not the thing that gets
her to 500. Reach is.

---

## Rejected: a "follow" keyword automation. Red teamed 2026-08-30 at Amanda's request.

The idea was to fire a follow request on comments containing words like "follow", so
follow-for-follow commenters get asked to follow. Amanda flagged the risk herself and asked
for it to be attacked rather than built. It should not be built. Four reasons, worst first.

**1. It would hit the exact people she wants to spare, almost every time.** Keyword matching
is substring based and case sensitive, proven above. The word "follow" in a comment is
overwhelmingly *past tense*: "Following you now", "I've been following for months",
"followed!", "Love your stuff, followed". Every one of those fires the trigger, and every one
of those is already a follower. The automation would ask loyal followers to follow, which
reads as though she is not paying attention. Her instinct was backwards from what the data
would actually produce, and it is worth saying so plainly: the word signals someone who
already did it.

**2. Follow-for-follow traffic is worth less than nothing.** F4F accounts follow, wait for the
follow back, then unfollow. They do not open newsletters and do not buy. Worse, they crater
engagement rate, which is what the algorithm uses to decide reach. Getting to 500 that way
makes every future post reach fewer real people, and Instagram periodically purges those
accounts anyway. The Club Target application is not helped by 500 followers that Instagram is
about to delete.

**3. It risks the entire keyword system.** Instagram's private reply exists to answer a
comment. DMing "please follow me" to someone who commented an emoji is not answering
anything, and it is the pattern the one-DM-per-comment limit was built to police. The
downside is not a warning, it is losing private reply permission, which would kill CESA,
GUIDE, RESET, PLAY, CONSIDER and TUESDAY in one stroke. Risking the whole funnel to chase
followers she does not want is a bad trade at any odds.

**4. It is off brand.** The voice is "I'd rather you finish 2 than bookmark 50." A DM that
says follow me back is the opposite of that, and it is the first impression for anyone who
gets it.

**What does the same job safely:** `followGate`, now live on 5 automations. It only asks
people who want something she made, only if they are not already following, and it asks as a
trade rather than a favor. It cannot be read as spam because it is a genuine reply to a
genuine request.

---

# THE FIRST REAL ONE, 2026-09-05

**Everything above that says "zero keyword attempts from anyone but Amanda" was true until
today. It is not true any more.** The statements at lines 180, 190, 214 and 242 describe the
period Aug 8 to Sept 4 and should be read as history, not current state.

## What happened

`2026-09-05T01:36:05Z` — 8:36 PM Central, Sept 4 — someone commented **"Cesa please"** on post
`6743958` on **@cesasgoldenyears**. Automation **2952** fired, run `150551`.

| Field | Value |
|---|---|
| Contact | `1774569036904343` |
| Comment | `"Cesa please"` |
| Automation | 2952, CESA, account 65540 |
| Run status | **`waiting`** |
| DM sent | Yes, `sent`, no error |
| Reply | **None, 11.5 hours later** |

## Why this is a real person and not another test

- **The contact id has never appeared in any run.** Every prior run in the entire system used
  `955627417560872` or `1048429878116670`, Amanda's own accounts.
- **The phrasing is natural.** Amanda's tests comment the bare keyword — the Aug 30 run's comment
  text is literally `"CESA"`. This one is `"Cesa please"`. Nobody types "please" to a test.
- **The timing is wrong for testing.** Amanda's test runs all sit in the 16:00-19:30 UTC band,
  mid-workday. This landed at 01:36 UTC, a Friday evening on the couch.

Also worth noting for the case-sensitivity rule above: **`"Cesa please"` matched because 2952
carries `Cesa` as well as `CESA` and `cesa`.** Had it only carried `CESA`, this comment would
have silently missed and the first real lead in the funnel's history would have gone nowhere.
Every keyword needs all three casings. 1019 PLAY, 1424 GUIDE, 1393/1394 CONSIDER, 445/432 CESA,
435 RESET and the whole product set still carry **only the all-caps form**.

## Two things went wrong at exactly the wrong moment

### 1. The emailGate regression cost this lead the fast path

`2952`'s emailGate was removed on 2026-08-28 precisely so that CESA comments would get the
**button to `cesa-guide.subscribepage.io`**, which captures the address on the page and feeds the
Cesa group instantly, with no daily job in the loop.

**The gate came back on 2026-09-03** (flagged in that day's sync). So this person was asked to
**reply with their email in a DM thread** instead of being handed the page. That path only
completes when this daily job runs and pushes the address to MailerLite.

Had the gate not been re-added, they would already have the guide.

### 2. MailerLite is unavailable, so the delivery leg is down

`mcp__MailerLite__add_subscriber` and `mcp__MailerLite__list_subscribers` are **not available
this session** — the server requires re-authorization and this session cannot run the OAuth
flow. Confirmed by search, not assumed.

So **step 4 of the daily job did not run today**, and if this person replies with their address,
**nothing can deliver it.** The first real capture in the funnel's history is sitting one reply
away from a leg that is currently broken.

## What has to happen

1. **Amanda re-authorizes MailerLite** (claude.ai connector settings). Nothing in the email half
   of the funnel works until she does.
2. **Take the gate off 2952 again**, back to the Aug 28 design: button to
   `cesa-guide.subscribepage.io`, no in-thread capture. The page does not depend on a daily job.
3. **Add the lowercase and title-case variants to every remaining keyword.** This lead only
   converted because 2952 happened to have them.
4. **Watch run `150551`.** If they reply, the address needs adding by hand until MailerLite is
   back. If they never reply, that is the argument for the button over the gate, in one datapoint.

---

# 2026-09-07: the casings were fixed, and the fix has a sharp edge

## What changed

Between **00:00:29 and 00:02:43 UTC today**, 20 live automations gained lowercase and title-case
keyword variants. That is the fix recommended on 09-05 after "Cesa please" only converted because
2952 happened to carry `Cesa`.

| Now carrying 3+ casings | ids |
|---|---|
| Instagram, acct 45886 | 2278 BLOOM, 2277 FALLFIT, 2276 CURLTALK, 1424 GUIDE, 1393 CONSIDER, 1019 PLAY, 445 CESA, 444 SCRUB, 443 BUTTER, 442 NATIVE, 441 SOOTHE, 440 LIPDRIP, 439 BROW, 436 SOAK, 435 RESET |
| Facebook, acct 30840 | 1422 GUIDE, 1394 CONSIDER, 1020 PLAY, 432 CESA, 428 SCRUB |

FALLFIT, CURLTALK and LIPDRIP got a fourth variant (`FallFit`, `CurlTalk`, `LipDrip`), which is
the right instinct for compound words.

## The problem this creates, and I should have flagged it when recommending the fix

**Blotato matches substrings.** That is documented higher up in this file and it is what makes a
lowercase variant dangerous: `brow` does not only match the word "brow", it matches **any**
lowercase text containing those four letters.

Checked against ordinary words, not assumed — **12 of the 19 lowercase variants match inside
common English words:**

| Keyword | Fires on ordinary words like | Risk on this account |
|---|---|---|
| `brow` | brown, browns, browning, eyebrow, browse, brownie | **HIGH.** Cesa's muzzle, blankets, furniture. "her brown fur" fires a brow gel ad. |
| `play` | playing, playful, played, display, displays | **HIGH.** A dog account. "watching her play" fires the audiobook list. |
| `native` | **alternative**, alternatives, natively | **HIGH.** Home tips constantly say "a cheaper alternative". |
| `bloom` | blooming, blooms, bloomed | **MEDIUM.** She posted about dandelions being open. |
| `butter` | butterfly, butterflies, buttercup, buttery | MEDIUM |
| `consider` | considering, considered, consideration | MEDIUM. "I'm considering one" fires a newsletter signup. |
| `soak` | soaking, soaked, soaks | LOW |
| `scrub` | scrubbing, scrubbed, scrubs | LOW |
| `guide` | guided, guidelines, guidebook, misguided | LOW |
| `soothe` | soothed, soother | LOW |
| `reset` | preset, presets, resetting | LOW |
| `seasonal` | seasonally | LOW |

**Two costs when a false positive fires:**

1. Someone making an ordinary comment gets DM'd an unrelated product link. That reads as spam on
   the account that is trying to earn 500 followers.
2. **It burns the one private reply per comment.** Instagram allows exactly one (error 20102). If a
   comment says "her brown fur is going white, send me the CESA guide", `brow` can claim the slot
   and **the real keyword fails silently.** The fix for missing leads would then start causing them.

**Title case does not solve it either.** `Brow` matches "Brown blankets…" at the start of a
sentence, `Play` matches "Playing with her…". Rarer than mid-sentence, but not safe.

## Recommended, proportionate fix, no caption changes required

Nothing in the queue needs rewriting for this — the CTAs all say the all-caps form.

- **Drop the bare lowercase variant on all 12 above.** Keep `ALLCAPS` + `Title`. That cuts the
  exposure to sentence-initial hits only.
- **For `brow`, `play` and `native`, go all-caps only.** Their host words (brown, playing,
  alternative) are too common to accept even sentence-initial risk.
- **Leave the compound keywords as they are.** `fallfit`, `curltalk`, `lipdrip`, `dishwasher`,
  `bottleneck`, `tuesday`, `cesa` are not substrings of ordinary words, so their lowercase forms
  are safe and are exactly the case that caught the first real lead.

## Not yet observed

**Zero false positives so far.** The change went live 13 hours ago and all 34 live automations
were swept today: no new runs anywhere. Comment volume is low enough that absence of evidence here
is weak evidence — this is a prediction from the matching rule, not an incident report.

## Two things the overnight pass did not touch

- **`454` GEL and `453` MASK are still all-caps only.** Both are `message-received` (DM keyword,
  not comment), which is why they were probably skipped. `GEL` is worth leaving alone regardless:
  lowercase `gel` would match "angel".
- **`2952`'s emailGate is still in place**, `updatedAt` unchanged at 2026-09-03T05:51:17Z. The pass
  edited keywords, not gates. So the first real lead is still on the slow path.

## Live state of the first real lead

Run `150551`, contact `1774569036904343`, comment "Cesa please". **Still `waiting`. No reply,
59.5 hours on.** Not expired.

MailerLite has now been unavailable for **3 days** (09-05, 09-06, 09-07), confirmed by search each
day. Step 4 of the daily sync has not run since 09-04.

---

# 2026-09-08: the first real lead expired. Outcome recorded.

Run `150551` on automation **2952** flipped from `waiting` to **`expired` at 2026-09-08T05:00:00Z**.

| | |
|---|---|
| Comment | `"Cesa please"`, 2026-09-05T01:36:05Z |
| Contact | `1774569036904343` — never seen before or since |
| DM sent | Yes, `sent`, no error |
| Replies received | **Zero.** Conversation `452629` holds exactly 1 message, outgoing. |
| Time from DM to expiry | **~75.4 hours** |
| Result | **Lead lost. No email captured. Guide never delivered.** |

**This is the whole funnel's first real keyword use, and it converted to nothing.**

## Why, mechanically

`2952` carried an `emailGate` when the comment landed. The gate replaces the button flow with
"reply with your email address and I'll send it." So the path was:

```
comment "Cesa please"  ->  DM asks for email in thread  ->  no reply  ->  expired
```

The path this automation was **deliberately built to use on 2026-08-28** was:

```
comment "Cesa please"  ->  DM with button  ->  cesa-guide.subscribepage.io  ->  page captures  ->  guide delivered
```

The gate came back on **2026-09-03T05:51:17Z**, two days before the comment. It is **still there
as of today**, `updatedAt` unchanged. Nothing in the 09-07 keyword-casing pass touched it.

## What this is and is not evidence for

**It is one datapoint, not a proven mechanism.** This person may simply not have wanted the guide
enough to type an address. Plenty of people comment and then lose interest.

**What it does establish, without needing a bigger sample:** the gate makes conversion depend on a
second deliberate action from the reader, inside Instagram DMs, plus a daily sync job, plus a live
MailerLite connection. The button path depends on one tap. **Three of those four dependencies were
either slower or entirely broken during this lead's window** — MailerLite has now been unavailable
since 09-05, so even a reply could not have been delivered.

The asymmetry is the argument, not the single loss.

## Standing recommendation, unchanged and now with a cost attached

1. **Remove the emailGate from 2952.** Restore the Aug 28 design. The landing page captures and
   delivers without a daily job in the loop.
2. Re-authorize MailerLite. Unavailable **4 days** now (09-05 through 09-08), confirmed by search
   each day. Step 4 of this job has not run since 09-04.
3. Strip the bare lowercase variants from the 12 keywords listed in the 09-07 section. Still
   present, still untouched.

## Sweep result today

All **34** live automations checked. **No new runs. No new failures.** The only failures on record
remain two `20102` errors on `445` from 2026-08-28. **No followGate anywhere.**

**No false positives from the lowercase keywords yet** — they have been live ~37 hours and comment
volume is low. Still a prediction, not an observation.

---

# 2026-09-08: THE LOWERCASE VARIANTS STAY. RECOMMENDATION WITHDRAWN.

## Do not strip them. Amanda's direct instruction, and she is right.

The 09-07 and 09-08 sections above recommend removing the bare lowercase keyword variants from
12 automations because Blotato matches substrings and `brow` sits inside "brown".

**That recommendation is withdrawn. Do not act on it.** If you are a future session reading this
file, the sections above are kept only as the record of a bad call. **Every keyword keeps every
casing.**

## Why the recommendation was wrong

Set the two risks side by side honestly:

| | Missed match | Substring false positive |
|---|---|---|
| Status | **Demonstrated** | **Predicted, never observed** |
| Evidence | The only real keyword lead in the funnel's history — "Cesa please", 2026-09-05 — matched **solely because 2952 carried `Cesa`**. All-caps only and it silently misses. | 12 keywords, live since 2026-09-07 00:00 UTC. Swept every automation daily since. **Zero false-positive runs.** |
| Cost when it happens | A real person asks for the thing, gets nothing, never knows, and neither do we | An unrelated DM, and one burned reply slot |

I argued from a word list. She argued from the one conversion the funnel has ever produced. **Her
evidence is real and mine was hypothetical**, and I weighted them the wrong way round.

## The standing rule, in her words

> **"We don't want it to be case specific. They're there for a reason. We don't want any missed
> connections. The goal is conversion. If somebody doesn't get the link when they comment the
> keyword in the wrong case, that's a leak."**

That is the priority order for this whole funnel: **a missed connection is a leak, and a leak
outranks tidiness.** Nobody types keywords in all caps. Expecting them to is the bug.

**Any new automation gets ALLCAPS + lowercase + Title case at minimum**, plus a camel variant for
compounds (`FallFit`, `CurlTalk`, `LipDrip`). `5215` DISHWASHER was built this way from the start.

The two remaining single-casing automations, `454` GEL and `453` MASK, are `message-received`
(DM keyword, not comment). **GEL is the one genuine exception**: lowercase `gel` matches "angel",
and that one is worth leaving alone.

## What monitoring stays

The daily sweep already checks every live automation's runs. If a false positive ever actually
fires, that is data and it gets reported with the comment text that triggered it. **Until one
does, there is nothing to report and nothing to change.**

## The gate came off 2952 today

Same instruction, same conversation. `blotato_update_automation` with `emailGate: null`.

Verified on a fresh `list_automations` read, not from the write response:

| Field | State after |
|---|---|
| `emailGate` | **absent** |
| `buttons` | `Get the guide` -> `https://cesa-guide.subscribepage.io` |
| `keywords` | `["CESA","cesa","Cesa"]` — **all three intact** |
| `isActive` | `true` |
| `publishedVersionId` | 6298 -> **8481**, so it is live |

CESA on Cesa's Instagram is back to the Aug 28 design: **comment -> DM with button -> landing page
captures the email and delivers the guide itself.** No in-thread reply required, no daily sync job
in the path, no MailerLite dependency. One tap.

That is the path the first real lead should have gotten. The next one will.

---

# WATCH RESULT 2026-09-08T16:18Z: no new CESA comment. Three other things surfaced.

Trigger `trig_01ErT42pMQ87cEbk1Y3NXppt`, first firing. Amanda's instruction was "watch for the
next cesa comment and confirm it delivers." **No CESA comment has landed since the gate came
off.** The honest result is silence. But the watch also had a standing requirement to report
gate reappearances even with no new run, and that requirement earned its keep.

## 1. The three watched automations, verified on a fresh paged read

Paged `blotato_list_automations` to an empty page. All three examined directly, not inferred.

| Automation | Account | `emailGate` | `followGate` | `keywords` | Active | New runs |
|---|---|---|---|---|---|---|
| `2952` CESA | 65540 Cesa IG | **absent** | absent | `CESA`/`cesa`/`Cesa` | yes | none |
| `445` CESA | 45886 IG main | **absent** | absent | `CESA`/`cesa`/`Cesa` | yes | none |
| `432` CESA | 30840 FB | **absent** | absent | `CESA`/`cesa`/`Cesa` | yes | none |

No gate has reappeared on any of the three. All three lowercase/mixed variants intact on all
three, per Amanda's standing rule. Runs unchanged: `2952` still shows `150551` expired and
`122274` completed; `445` still shows `122325`/`113285` completed and `113157`/`112624` failed
`20102` from Aug 28; `432` still has zero runs.

**The watcher itself is confirmed working end to end.** It fired into this session with MCP
tools intact, which also settles the open question about the connector warning: that warning
was about fresh-session triggers, not session-bound ones.

## 2. `1393` CONSIDER on IG main is carrying an emailGate. Its Facebook twin is not.

Found while paging, outside the three watched automations.

| Automation | Keyword | Account | `emailGate` |
|---|---|---|---|
| `1393` | CONSIDER | 45886 IG main | **present** |
| `1394` | CONSIDER | 30840 FB | absent |

Same offer, same keyword, two different delivery paths depending on which platform someone
comments on. The gate text asks the commenter to "Reply with your email address and I'll add
you" — the same mechanism that just cost the first real CESA lead.

The Aug 29 design record in `FLYWHEEL-STATUS.md` names the intended emailGate set as `2954`
CONSIDER on Cesa's IG, `2771` and `2772` TUESDAY. **`1393` is not in that set.** Whether the
gate is a regression like `2952`'s or was never removed in the first place, the read does not
say, and this file is not going to guess.

**Nothing has been lost through it.** `blotato_list_automation_runs` on `1393` returns
`{"runs":[]}` — zero runs since it was created Aug 16. It is a leak that has not leaked yet.

**Not changed.** The standing rule in this file is that a gate reappearance gets flagged for a
decision rather than a silent fix, and Amanda's instruction was scoped to `2952`. Flagged.

## 3. The lost lead, in full, and it is worse than "expired"

The conversation is on the record. One message, and the person never came back.

| When | What |
|---|---|
| 2026-09-05T01:36:05Z | Contact `1774569036904343` comments **"Cesa please"** on post `6743958` |
| 2026-09-05T01:36:06Z | `2952` fires. One outgoing DM, status `sent`, message `1419557` |
| since | **Nothing. Zero incoming messages. Conversation `452629` `updatedAt` == `createdAt`** |

What she was sent, verbatim:

> Yes. 15 pages, free, everything that actually keeps her comfortable at 19. Written from our
> living room, not a clinic. Reply with your email address and I'll send it.

She typed the word *please*. She asked politely for a free thing and was asked for her email
address instead of being handed the thing. She never replied, the run expired, and the guide
was never delivered.

This is the demonstrated case, and it is why the casing variants stay and why the gates come
off. Not a predicted failure. A named human who asked and got nothing.

**Recovery may still be possible but is not guaranteed.** Conversation `452629` exists and
`blotato_send_message` can target `recipientId` `1774569036904343` on account `65540`. Against
it: Instagram's messaging window for business accounts is 24 hours from the last user message,
and this is roughly 63 hours past it, so the send may simply be rejected. A rejection costs
nothing and is itself information. **Amanda's call — this is an unsolicited DM to a real
person, so it does not go out on my own initiative.**

## 4. Two warm people commented on Cesa's account and neither used the keyword

Both on account `65540`, both inside 48 hours, both exactly the audience the guide is written
for. Neither triggered anything, and neither was supposed to — the automations behaved
correctly. The leak is upstream of the automation.

| Comment | When | Post | Text |
|---|---|---|---|
| `4172237` | 09-08T10:29Z | `6600952` | "They get to pee wherever they want when they're old 😂 I tried to get mine to go outside but he wouldn't make it sometimes. It's an honor to clean it up after all those years together." |
| `4103323` | 09-07T19:30Z | `6519273` | "...I miss seeing her hopping around like your **Cesla**." |

`6600952`'s caption does say "Comment CESA and I'll send you what I wrote about her." She
answered the post instead of the instruction — which is what people do when a caption moves
them. The guide is about incontinence, traction and door distance; she described incontinence.

`4103323` typed **Cesla**. One letter off. Substring matching does not save it: `Cesa` is not
inside `Cesla`. No casing variant would have caught this either, so it is not an argument
against the current keyword set — it is an argument that the keyword is not the only door that
should exist. A public comment reply catches both of these, and public replies do not consume
the one-DM-per-comment slot.

**Drafts not written and nothing posted.** Replying to these is content, and content is
approval-first.
