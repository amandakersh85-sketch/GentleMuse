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

## `1393`'s gate came off, 2026-09-08. Amanda's call, same conversation.

`blotato_update_automation` with `emailGate: null`. Verified on a fresh paged read, not from the
write response:

| Field | State after |
|---|---|
| `emailGate` | **absent** |
| `buttons` | `Get Consider This` -> `https://consider-this.subscribepage.io` |
| `keywords` | `["CONSIDER","consider","Consider"]` — all three intact |
| `isActive` | `true` |
| `publishedVersionId` | 7954 -> **8508**, so it is live |

CONSIDER now behaves identically on Instagram and Facebook: comment, DM with button, landing
page captures the address. The asymmetry is gone.

### Correction to the Aug 29 gate inventory

That record named `2954`, `2771`, `2772` as the emailGate set. It is out of date rather than
wrong — three SEASONAL automations created Sept 1 (`4009` IG main, `4010` FB, `4011` Cesa IG)
all carry gates, consistently across all three platforms. Not touched, not a discrepancy.
Noting them so the next inventory does not read them as regressions.

### The mechanism the funnel has not been using

`blotato_send_message` accepts a `commentId`, which sends **one private reply per comment,
within 7 days, with no prior DM required**. That is a separate window from the 24-hour standard
DM rule.

Every warm commenter who did not type the keyword is reachable in their inbox for a week. The
funnel has only ever used this path through keyword automations, which means the door has been
open on every non-keyword comment and nobody has walked through it. **This is the answer to the
two near-misses above, and it is a standing capability, not a one-off.**

Caveat worth writing down: the slot is one per comment and an automation firing consumes it.
That is what error `20102` "already has a reply" is. So a contact whose emailGate run expired
may be permanently unreachable through this path — testing that on contact
`1774569036904343` is what the next send will establish.

---

# CONFIRMED 2026-09-08: an expired gate run permanently burns the comment

The test ran. This is no longer a caveat, it is a measured fact, and it makes the gate
considerably worse than "adds friction."

Four messages went out on Amanda's approval. Verified individually with `blotato_get_comment`
and `blotato_get_message`, not from the send responses.

| # | What | Target | Result |
|---|---|---|---|
| A | Public comment reply | comment `3791926`, post `6743958` | **`posted`**, platform id `18134260012643719` |
| B | Private reply + button | contact `1774569036904343` | **`failed`, error `20102`** |
| C | Private reply + button | contact `1732590004635114` | **`sent`**, conversation `504237` |
| D | Private reply + button | contact `1386554462976400` | **`sent`**, conversation `504238` |

B's exact error:

> Could not send Instagram message: The comment you are trying to reply to, already has a reply.

## What this establishes

A comment carries **one** private reply, ever. When an automation fires on that comment it
spends the slot — even if the run then expires having delivered nothing of value. The gate's
"reply with your email address" message *is* the spent slot.

So the cost of an emailGate is not friction. It is this:

1. Someone comments the keyword.
2. The gate consumes the one private reply to ask them a question.
3. They do not answer.
4. The run expires.
5. **There is now no way to DM that person about that comment. Ever.**

The button path cannot fail this way, because the button *is* the delivery — the slot gets
spent on the thing they asked for rather than on a question about it.

The only route left to a burned contact is a public comment reply, which is what A was, and it
posted fine. Public replies do not touch the private reply slot and have no time window.

**Corrected guidance for the watcher and for any future session:** do not tell Amanda a lost
gate lead can be DM'd by hand. It cannot. The watcher prompt was updated with this.

## The two hand-sent leads are now off the sync's radar

C and D worked, and that creates a gap. They are not automation runs, so
`blotato_list_automation_runs` will never show them and the daily lead sync will not see them.
If either replies with an email address in-thread instead of tapping the button, that address
is stranded — nothing is going to pick it up.

Closed by extending the CESA delivery watch (`trig_01ErT42pMQ87cEbk1Y3NXppt`, every 2h at :18)
to check conversations `504237` and `504238` for incoming messages each run, and to add a
stranded address to the Cesa group `196024300390581479` by hand.

## The standing capability, restated plainly

Every comment on Amanda's own posts is an open inbox for 7 days, once. The funnel has only ever
used it through keyword automations. Two of the three sends above were to people who never
typed a keyword, and both reached them — that is the mechanism working exactly as intended on
traffic the funnel was previously discarding.

---

# 2026-09-08: KEYWORDS DO NOT HAVE TO BE MAGIC WORDS

Amanda's question, and it reframed the whole mechanism: "How do we get commonly asked questions
responded to automatically with the guide?"

Blotato matches keywords by **case-sensitive substring**. That has always been treated as a
hazard to work around. It is also a feature nobody used: `"your secret"` is a perfectly valid
keyword. So is `"mine is"`. **People already announce that they qualify, in their own words.
The funnel was waiting for them to guess a password.**

## Why she asked, and what the source actually said

She thought she had replied to two of the flagged comments. She had not, and the reason is
structural rather than forgetful.

Her conversational replies in the 7-day window — `3662582`, `3638273`, `3638228` — are all on
post `6709365`, on her **main** IG. Both comments she remembered answering are on post
`6712462`, on **Cesa's** account.

**Zero conversational replies on Cesa's account across the entire window.** Two inboxes, one
set of eyes. Blotato does capture her native app replies, so the absence is real data and not a
blind spot in the tooling.

That is worth stating plainly: the dedicated conversion channel receives the most qualified
comments and gets the least human attention.

## The keyword set was tested against real comments before it shipped

25 real audience comments from the 7-day window, both IG accounts, run against candidate
keywords with exact case-sensitive substring semantics. Script kept at
`scratchpad/kwtest.py`.

| Measure | Result |
|---|---|
| Qualified caught | **5 / 5** |
| Qualified missed | 0 / 5 |
| False positives | **0 / 19** noise and spam comments |

Every one of the 5 people hand-DM'd on 09-08 would have been caught automatically. Neither spam
comment fires. No emoji-only comment fires.

**The number flatters itself and the record should say so.** The keywords were chosen after
reading those 25 comments, so 5/5 is overfitted by construction. Only comments from 09-08
onward are an honest test. The sweep routine reports that measurement every run.

What is not overfitted is the shape of it: a multi-word phrase about someone's own dog cannot
appear inside "Beautiful" or an emoji string. The specificity is structural, not fitted.

## What shipped: 39 keywords on `2952`, Cesa's IG only

Amanda's call was to extend `2952` rather than create a second automation. Correct call — two
automations on one account can both match one comment, and the loser fails `20102`. One
automation cannot race itself.

Verified on a fresh paged read: `publishedVersionId` 8481 -> **8524**, `emailGate` still absent,
button unchanged, `CESA`/`cesa`/`Cesa` intact and first in the list.

```
CESA cesa Cesa
your secret / Your secret / YOUR SECRET
her secret / Her secret
mine is / Mine is / mine was / Mine was
get mine / Get mine / got mine / Got mine
year old / Year old / years old / Years old / yr old / yrs old
still walk / Still walk
walkies / Walkies
how old / How old / HOW OLD
my dog / My dog / my girl / My girl / my boy / My boy
senior dog / Senior dog / senior pup / Senior pup
```

**Cesa's account only, deliberately.** Her main IG carries Target hauls and holiday history
posts where `"year old"` would fire on Debbie Reynolds. `2952` has `postId: null` so it fires on
any post on its account, and every post on that account is senior-dog content. The topical risk
is near zero there and real on `445`.

## The three honest limits

1. **This delivers the guide, it does not answer questions.** One automation, one canned DM.
   Someone asking what food Cesa eats gets the guide, not a food answer.
2. **It spends the private reply slot** — the same slot the gate burned. A false positive means a
   real person got a DM they did not ask for and can never be DM'd about that comment again. A
   false positive costs more than a miss, which is why the watcher hunts for them specifically.
3. **It does not fix the thing Amanda actually noticed.** A robot answering is not her
   answering. Guide delivery and human reply are different jobs and automation only covers one.

## Two standing routines now cover the gap

| Routine | Trigger | Cadence | Job |
|---|---|---|---|
| CESA delivery watch | `trig_01ErT42pMQ87cEbk1Y3NXppt` | every 2h at :18 | Runs, gates, failures, the 5 manual threads |
| Comment sweep | `trig_012kjdGhjy2pJoLjMn6h5x2G` | every 6h at :40 | Qualified comments no keyword caught. **Drafts, never sends.** |

The sweep measures the keyword set every run: true positives, misses with the exact phrase used
instead (a miss is a candidate keyword, proposed not added), and false positives with the
offending keyword named. Both are bound to this session, which is why they keep their MCP tools
— the connector warning on creation applies to fresh-session triggers, confirmed when the CESA
watch fired with tools intact at 16:18 UTC.

## Flagged, not changed: `2954` CONSIDER on Cesa's IG has a gate and NO button

`buttons: []`. It is gate-only with no fallback whatsoever, which makes it strictly worse than
`2952` was before today: a commenter MUST reply with an email in-thread, and that reply spends
their one slot. If they do not answer, the run expires and they are burned with no button ever
having been offered.

It is in the Aug 29 intended-gate set, so this is a design decision rather than a regression,
and it is Amanda's to make. Recording it because it is now the last place in the funnel carrying
the exact failure shape that cost the first real lead.

## The five sent 2026-09-08, all verified individually

| Comment | Account | What they said | Result |
|---|---|---|---|
| `4172237` | 65540 | "an honor to clean it up after all those years together" | conv `504237` |
| `4103323` | 65540 | 18-year-old Chiweenie, losing her vision | conv `504238` |
| `3690124` | 65540 | "What's your secret?! She looks so healthy!!" | conv `504442` |
| `3667740` | 65540 | "Wow 19!! I hope little doggie lives this long" | conv `504443` |
| `3832450` | 45886 | "mine is 15 and its like that everyday I come home" | conv `504444` |

Every concrete detail in all five drafts was lifted from Amanda's own published captions — the
bladder/traction/door trio from the Aug 28 caption, "stops when she wants to stop" from the exact
post `3667740` commented on, "hears the car before the door" from the exact post `3832450`
commented on. She cut one line from draft D that was my inference rather than sourced, and she
was right to.

## `2954`'s gate came off and it got a button, 2026-09-08. Amanda's call.

The last automation in the funnel carrying the gate-only shape. `blotato_update_automation`
with `emailGate: null` and a button added in the same call.

Verified on a fresh paged read, not from the write response:

| Field | Before | After |
|---|---|---|
| `emailGate` | present, "Reply with your email address and I'll add you" | **absent** |
| `buttons` | **`[]`** — no path at all | `Get Consider This` -> `https://consider-this.subscribepage.io` |
| `keywords` | `CONSIDER`/`consider`/`Consider` | unchanged, all three intact |
| `isActive` | `true` | `true` |
| `publishedVersionId` | 4197 | **8534** |

**Zero runs, ever.** `blotato_list_automation_runs` returns `{"runs":[]}`, so nothing was lost
through it in the two weeks it was gate-only. It is also untested by real traffic.

Every gate in the CESA and CONSIDER path is now gone. `4009`, `4010` and `4011` SEASONAL still
carry gates and were not touched — they are the Sept 1 set and no decision has been asked for
on them.

### The change broke the DM copy, and this is the second time that has happened

The `dmMessage` still opens **"You're in, and you'll get the Cesa part too."**

That sentence was written for the world where the gate had already captured the address. With
the gate gone it is the first thing a commenter sees, and it is false: they have given nothing
and they are not subscribed. It tells them they are in, then offers a button they now have no
reason to tap.

`LEAK-SWEEP-0830.md` caught this identical failure on 08-30 — "emailGate they no longer have.
Rewritten to match reality." **Removing a gate is two changes, not one: the gate and the copy
that assumed it.** Writing that down as a rule because it has now cost twice.

Draft raised for approval, minimal diff, sign-off untouched: `"You're in, and you'll get the
Cesa part too."` becomes `"Here it is."`, and `"Tap below and add your email on the page.
Thursday's lands in your inbox."` is added before the sign-off. Both borrowed from `2952` and
`1393`, the two that work. Not applied — copy is approval-first.

### Standing check for the daily sync and both routines

When an `emailGate` is removed from any automation, re-read its `dmMessage` in the same pass and
flag any sentence that only makes sense with a gate in the path: "you're in", "reply with",
"I'll add you", "send me your email". A gate removal that leaves the copy behind converts worse
than the gate did, because the gate at least asked for something real.

### Copy fixed, 2026-09-08. Amanda's call, same conversation.

Verified on a fresh paged read. `publishedVersionId` 8534 -> **8536**, `emailGate` still absent,
button and all three keyword casings untouched.

| | Text |
|---|---|
| Was | "**You're in, and you'll get the Cesa part too.**" |
| Now | "**Here it is.**" |
| Added | "**Tap below and add your email on the page. Thursday's lands in your inbox.**" |

The taped-outline sentence was left exactly as written. It is the best line in the message and it
is hers.

`2954` is now the same shape as everything else that works: comment, DM, button, landing page.

## A hazard the 39-keyword set creates: `2952` can trigger on Amanda's own comment

`2952` now matches `"year old"` and `"years old"`. Cesa's captions say "19 years old" constantly
— it is the whole premise of the account.

Amanda uses scheduled first-comments on her other accounts (`"Prefer the link? Here it is:"` on
Facebook, the Press Play link on her main IG). **There are currently none on account `65540`** —
every `isAuthor: true` comment in the 7-day window was on `45886` or `30840`. So the risk is not
live today.

But the day a first-comment gets added to a Cesa post and it quotes the caption, `2952` matches
its own account's comment. Whether Blotato ignores the account's own comments on a
`comment-received` trigger is **unverified**, so the safe assumption is that it does not.

Consequence is mild — it would DM her own account and burn nothing real — but it would look
exactly like a lead in the runs list, and this project has already lost 12 days to a monitor
that reported a comfortable fiction.

Closed by teaching the CESA watch the difference: `17841432484315950` is Cesa's IG business id
and `17841480184590976` is her main IG. A run from either is a **self-trigger to fix**, not a
lead to celebrate, and the watch now says so.

---

# CORRECTION 2026-09-08: the 5/5 was rigged, and the honest number was 18%

Earlier today this file reported the natural-language keyword set catching **5 of 5** qualified
comments with 0 false positives. That measurement was taken on the same 25 comments used to
choose the keywords. It proved nothing except that the keywords matched the comments they were
copied from.

Amanda then asked for the CONSIDER automations to get the same treatment, which meant pulling a
wider comment history — 2026-08-20 to 09-01, never seen when the keywords were written. That is
a real out-of-sample test, and the shipped set failed it.

| Keyword set | Cesa page | Gentle Muse page | False positives |
|---|---|---|---|
| The 39 shipped at 16:58 | **0 / 5** | 2 / 7 | 0 / 45 |
| Plus phrases derived from the misses | **3 / 5** | 7 / 7 | 0 / 45 |

**The set that went live at 16:58 caught nothing at all on Cesa's own page.** Both of its two
hits were on the Gentle Muse page. 18% overall, not 100%.

Script: `promo-engine/kwtest.py` (in-sample) and the out-of-sample run in scratchpad.

## What fixed it, and why these words and not others

Every added phrase came from an actual comment the set missed. None were invented:

| Missed comment | Phrase added |
|---|---|
| "**Mine loves** to snuggle up on this old mop head" | `Mine loves` |
| "extra looks to our **old bud**s" | `old bud` |
| "That's what I feed **my dawg**gies" | `my dawg` |
| "even with demitia **my baby** had to have his foods" | `my baby` |
| "my Julio who **just passed** 😢 he was 15" | `just passed` |
| "My Miku **only got to see** 12😢 I **miss her** every single day" | `got to see`, `miss her` |
| "She looks amazing **at 19**" | `at 19` |

83 keywords now on `2952`, verified on a fresh paged read: `publishedVersionId` 8524 -> **8545**,
gate still absent, button unchanged.

Still missed on Cesa's page, and honestly unfixable by keyword: a list of dog nicknames answering
a caption's question, and "Maybe because it smells it's owners". Neither has a generalizable
phrase. **That is what the sweep routine is for.**

## `2954` CONSIDER: what the data would not support

Amanda asked for natural-language keywords on the CONSIDER automations, Cesa's page only. Two
findings changed what that could be.

**1. Dog phrases on `2954` would collide with `2952` on every single comment.** Both live on
account `65540` with `postId: null`, so both listen to every post. A shared keyword means both
fire on the same comment and the loser fails `20102` every time — not occasionally, every time.
That is the exact race the one-tool-per-keyword rule exists to prevent. Not done.

**2. There are zero audience comments on any CONSIDER post, ever.** Checked 08-20 through 09-08:
`6796347`, `6773370`, `6736921`, `6659651`, `6629277` and their Facebook siblings have not
received a single audience comment. This matches `REACH-ANALYSIS.md` — static carousels reach 3
to 4 people against 112 to 1,739 for Reels. **The bottleneck on CONSIDER is not the keyword. It
is that nobody sees the posts.**

So `2954` got subscribe-intent phrases only — `sign me up`, `add me`, `count me in`,
`the newsletter`, `the weekly`, `weekly note` and casings. 19 keywords, `publishedVersionId`
4197 -> **8546**. These share no substring with any of `2952`'s 83, so the guaranteed collision is
avoided.

**Flagged honestly: these are unvalidated.** Not one of them appears in 19 days of real comments.
They are the safest available guess, not a measured choice, and they are the only part of today's
keyword work that is not data-backed. The sweep will report whether they ever fire.

Residual risk that cannot be removed: a comment containing both a `2952` phrase and a `2954`
phrase ("my baby is 15, sign me up") still races. Rare rather than guaranteed, and the person
still receives exactly one DM.

## The lead pool nobody harvested

Post `6250675` on the **Gentle Muse** page is the single largest concentration of qualified
senior-dog comments in the whole account history — a dozen or more people describing their own
dogs by name and age, several grieving. Amanda replied to many of them by hand, warmly, one at a
time. **Not one received the guide.**

Every one of those comments is now past the 7-day private-reply window. They are reachable only
by public comment reply. Amanda's instruction today was to keep natural-language keywords off the
Gentle Muse page, so automation will not catch the next batch there either — the sweep is the
only thing that will.

## Design fix: stop hardcoding keyword lists into routine prompts

The sweep prompt shipped at 16:59 embedded all 39 keywords as literal text. Two hours later that
list was wrong, and a stale list makes the sweep report caught comments as missed — corrupting
the exact measurement it exists to produce.

Both routines now **read the live keywords from `blotato_list_automations` every run** instead of
trusting a copy. This is the third time in this project a hardcoded list has gone stale
underneath a monitor. The rule is now explicit: a routine that checks configuration reads that
configuration from source at run time, never from its own prompt.

---

# 18:40 — THE FIRST REAL OUT-OF-SAMPLE TEST, 54 MINUTES AFTER SHIPPING. IT MISSED.

The lead sweep's first firing caught a genuinely new comment, and it is the honest test the earlier
5/5 could never be.

Contact `2535614900194954` wrote "She looks amazing!" on `6712462` on Sept 4 and was never
answered. A public reply went out at 18:23. **Four minutes after reading it they came back:**

> "@cesasgoldenyears gives me hope for my healthy chi that's about to turn 9 ❤️💪"

Nothing fired. `my chi` is in `2952`'s 83 keywords, but **the adjective splits it** — "my healthy
chi" does not contain the substring "my chi". A qualified lead, self-identified, on the account
the keywords were built for, missed by one word of English.

**Proposed fix, not applied:** the standalone token `" chi "` with surrounding spaces. It catches
this, it catches "her chi", "the chi", "a chi is". It does not collide with anything on `2952`, and
"Chihuahua" does not contain `" chi "` because the required trailing space is absent. Keyword
changes are config, and Amanda wants those approved, so it waits.

**The lesson is bigger than one keyword.** Multi-word keywords assume word adjacency, and real
people put adjectives in the middle. `my dog` misses "my old dog". `my girl` misses "my sweet
girl". `senior dog` misses "senior rescue dog". A meaningful share of the 83 are quietly fragile in
exactly this way, and no amount of adding phrases fixes the class — which is precisely why the
sweep exists and why its measurement matters more than the keyword list does.

## What was actually done for her, under the new rule

Public reply threaded under her top-level comment, plus a private DM with the button. Both
verified. Conversation `505547`, message `1594288`, status `sent`.

The DM leans on Amanda's own published line from `6503252`: *"People ask me what the secret is.
There isn't one. It's small adjustments, made early and kept up."* That line is why a 9-year-old
dog's owner is the right audience for a guide about a 19-year-old, and it is her sentence, not an
invented pitch.

## Reply-threads are not nestable

`blotato_post_comment` rejects a `parentCommentId` that is itself a reply — "must be a top-level
comment". To answer someone who replied inside a thread, thread the answer under their ORIGINAL
top-level comment; it lands in the same visible conversation.

## Three routines, all rewritten this hour to Amanda's rule

| Routine | Cadence | Default |
|---|---|---|
| Comment replies (`trig_01HK4yKpqXoMKYjpiX6LQUj2`) | every 3h, all 3 accounts | **posts** |
| Lead sweep (`trig_012kjdGhjy2pJoLjMn6h5x2G`) | every 6h | **sends the guide** |
| CESA delivery watch (`trig_01ErT42pMQ87cEbk1Y3NXppt`) | every 2h | reports only |

The lead sweep's original prompt ended "DO NOT SEND ANYTHING... that is her standing rule and it is
not negotiable." It fired 20 minutes after she replaced that rule and would have sat on a live lead
to ask permission. **A routine's prompt is a snapshot of a rule, and rules change faster than
prompts.** Both the sweep and the watch now read live state from source rather than from their own
text: the sweep reads keywords off the automations, the watch discovers DM conversations instead of
carrying a list that was already one short.

---

# 2026-09-09: `" chi "` and `collab` added. Amanda's call. And Blotato does NOT trim keyword whitespace.

Both fixes for the two observed adjacency misses. Verified on fresh paged reads, not write responses.

| Automation | Added | `publishedVersionId` |
|---|---|---|
| `2952` CESA, Cesa IG | `" chi "`, `" Chi "` (85 keywords) | 8545 -> **8817** |
| `415` PR screening, IG main | `collab`, `Collab`, `COLLAB` (15 keywords) | 467 -> **8816** |

Gates still absent on `2952`, button unchanged. `415` still `message-received`, `dmMessage`
untouched.

## The whitespace question, and why it mattered enormously

`" chi "` only works if Blotato stores the leading and trailing spaces. If it silently trimmed
them to bare `chi`, the substring match would degrade catastrophically. Tested before shipping
(`promo-engine/chitest.py`) against a 22-item corpus:

| Stored as | Qualified caught | False positives |
|---|---|---|
| `" chi "` — spaces kept | 4 / 5 | **1 / 17** ("tai chi", harmless on a dog account) |
| `chi` — spaces trimmed | 5 / 5 | **10 / 17** |

The trimmed version fires on **chicken, children, Chicago, chill, chip, gnocchi and Chihuahua**.
On a senior-dog account "she eats chicken and rice" is an ordinary comment, and every one of those
would have burned a real person's single private-reply slot on a guide DM they never asked for.

**ANSWER, verified empirically: Blotato PRESERVES leading and trailing spaces in keywords.** A
fresh `list_automations` read returns `" chi "` and `" Chi "` with both spaces intact. This was
unknown before today and is now a usable technique: **a space-padded keyword is a poor man's word
boundary**, and it is the only way to match a short token safely under substring matching.

The method generalises. Any short or common word — `chi`, `pup`, `old`, `mine` — is unsafe bare and
safe padded. Test both forms before shipping, because the failure mode is invisible: nothing
errors, the automation just starts DMing people who mentioned dinner.

## Known residual gaps in `" chi "`

It needs a space on both sides, so it misses a sentence-final "I love your chi" and a
punctuated "my recently passed chi!". Punctuation variants (`" chi."`, `" chi,"`, `" chi!"`) were
tested clean and are available if a real miss shows up. Not added — three unobserved keywords is
speculation, and the sweep exists to catch what the list misses and propose from real data.

## `collab` on `415` is nearly free, which is why it is bare rather than padded

`415` is `message-received` and its only action is sending screening boilerplate. A false positive
costs a stranger one polite form letter, not a burned lead slot. That asymmetry is why the bare
token is fine here and would not be on `2952`.

It also makes the existing `like to collab` and `gifted collab` redundant. Left in place — they
cost nothing and removing them is a change with no upside.

## Both observed adjacency misses would now fire

| Real text | Keyword | Before | After |
|---|---|---|---|
| "gives me hope for my healthy chi that's about to turn 9" | `" chi "` | miss | **hit** |
| `Tap "collab" below 💌` | `collab` | miss | **hit** |

---

# The Just Another Tuesday diagnosis, 2026-09-09

Amanda asked, for the third time, why the newsletter is not getting subscribers, and told
this workspace to stop reporting the symptom and find the cause. She had opened MailerLite
herself and was sure the form was active. She was right. It is.

## What I reported wrong, twice

I said there was no live signup page, that popup `195832725497709843` had `active = false`,
and that it fed the wrong group. All 3 were false. I lifted them from open item 1 of the
issues 1-5 Drive doc, written 08-18 and **already fixed on 08-27**, and never ran the live
check. The correct state was sitting in this repo the whole time, in `FLYWHEEL-STATUS.md`:
"Dual newsletter popup is now ACTIVE (`195832725497709843`) ... Confirmed `active: true`.
Feeds both newsletter groups."

Two sessions in a row read a stale note and published it as live state. That is the exact
thing the hard rule exists to stop. **A Drive doc is a record of a moment, not a source of
truth. Live API or nothing.**

## What is actually true, all checked live 09-09

| Thing | State |
|---|---|
| `just-another-tuesday-gm.subscribepage.io` | **HTTP 200, live.** Title "Just Another Tuesday: 10 hours ahead on AI, not 10 years" |
| Its form | Real email field, posts to account `2465670`, page `196122128046621787` |
| Does it convert | **Yes.** 2 strangers in the JAT group, `source: webform`, 08-19 and 08-23 |
| Popup `195832725497709843` | `active: true`, `is_broken: false`, `has_missing_groups: false` |
| Its groups | Consider This **and** Just Another Tuesday. Correct. |
| Stranded at double opt-in | **0 account-wide** |
| `list_forms type=promotion` | Returns **0**. This is why the pages looked missing. |

**Landing pages are not `promotion` forms.** The subscribepage.io pages are MailerLite
*pages*, a resource the forms API does not list. `api/sites`, `api/pages` and
`api/landing-pages` all 404, which is already logged in `FLYWHEEL-STATUS.md`. So the only
way to check a landing page from here is **curl the public URL and read the form action.**
Do that. An empty `promotion` list proves nothing.

## The actual cause

The 4 TUESDAY automations have **never fired**. Not once since 08-25.

| id | Account | Keyword | Triggered |
|---|---|---|---|
| 447 | IG main 45886 | TUESDAY / tuesday | **0** |
| 427 | FB 30840 | TUESDAY / tuesday | **0** |
| 2771 | IG main 45886 | TUESDAY / tuesday | **0** |
| 2772 | FB 30840 | TUESDAY / tuesday | **0** |

Not a casing problem: lowercase `tuesday` is live and is on the safe list. The automations
are fine. Nobody types the keyword because almost nothing asks them to.

**Published, 08-25 to 09-09, 100 IG and FB posts:**
- 2 distinct posts said "Comment TUESDAY," both inside the first 3 days
- 56 posts asked for a different keyword
- 39 asked for nothing

**Scheduled, through 10-31, 91 IG and FB posts:**

| CTA | Posts |
|---|---|
| SEASONAL | 32 |
| CESA | 26 |
| (none at all) | 18 |
| CONSIDER | 7 |
| PLAY | 3 |
| GUIDE | 3 |
| **TUESDAY** | **2** |

On **09-15**, the day #004 sends, 8 posts are scheduled and **none** mentions the newsletter.
Send days 09-22 through 10-27 have **0 posts scheduled at all** — the queue dries up after
09-21, which is its own problem.

## The rule this produces

The weekly product is the least promoted thing she makes. A working door with no sign on it
converts at exactly the rate observed: 2 people in 3 weeks, both of whom found it some other
way.

**Every JAT send day gets a TUESDAY CTA on IG and FB.** Not "should," per the 08-25 note
that was never enforced. It goes in the rotation as a standing slot, the same way SEASONAL
got 32 slots without anyone having to remember.

## Diagnostic order for "the funnel is not converting", in this order

1. `curl` the public landing page URL. Read the form action. Never trust `list_forms`.
2. Check the destination group for `source: webform` subscribers. That proves conversion.
3. Check `status: unconfirmed` account-wide. That finds double opt-in strandings.
4. `blotato_get_automation_analytics` on every automation for the offer. **0 triggered means
   the leak is upstream of the automation, not inside it.**
5. Only then count how many published and scheduled posts actually carry the CTA.

Steps 1 through 4 took 6 tool calls. Step 5 is where the answer was. Two sessions never got
past a stale note to reach step 1.

## What was fixed 09-09, and what is still open

**Applied and verified live.** 3 scheduled Instagram posts had no keyword CTA and no link,
so a reader had no way to reach anything. Each now carries a `firstComment` with the JAT
link, which is this file's own documented pattern: *"Put the raw link in `firstComment`
instead of the caption. The keyword leads, the link is still there for anyone who prefers
it, and the caption stays clean."* **No caption was altered.** Media, scheduled time,
`mediaType: reel` and `shareToFeed` all preserved and re-read to confirm.

| id | When | Why it was chosen |
|---|---|---|
| `4231131` | 09-16 18:00 | Opens with the JAT landing page's own headline, "You do not need to be 10 years ahead on AI. About 10 hours is enough," promises a free guide, and offered no way to get either. Carries the guide link first, then JAT. |
| `3691541` | 09-15 23:00 | #004 send day. Build-in-public voice. |
| `4231110` | 09-15 15:00 | #004 send day. Carries #buildinpublic. |

`3732531` (09-15 17:00, the gratitude reel) was deliberately left alone. Wrong post for it.

**Each `blotato_update_schedule` returned "Schedule updated successfully" and was then
re-read.** The message alone is not proof, same rule as MailerLite's 200s.

### Still open, needs Amanda

1. **The caption CTA.** A `firstComment` link gives a reader a path. It does **not** fire the
   automation. Only a comment containing the keyword does that, so `447`/`427`/`2771`/`2772`
   stay at 0 triggers until captions say **"Comment TUESDAY and I'll send it to you."**
   That is editing captions she wrote, so it waits for her yes.
2. **6 of 7 send days have no posts at all.** The IG and FB queue ends 09-21. Send days
   09-22, 09-29, 10-06, 10-13, 10-20 and 10-27 are empty, so there is nothing to add a CTA
   to. Those need new posts, not edits.
3. **JAT #006 to #010 are not in MailerLite.** Only #004 (09-15 07:00) and #005 (09-22 07:00)
   are `ready`. Consider This has 6 issues queued through 10-15. Copy is drafted and waiting
   on her approval.
4. **The JAT group has 3 active subscribers and 1 is Amanda.** #004 reaches 2 real people on
   09-15. That is the number the whole fix exists to move.

---

# Funnel watch 2026-09-09 06:21 UTC, and a second JAT fault found

## Watch result: clean on everything it was asked to check

| Check | Result |
|---|---|
| `2952` runs | 2, both baseline (150551 expired, 122274 completed). No new. |
| `445` runs | 4, all baseline, all test contact `1048429878116670`. No new. |
| `432` runs | Still 0, ever. |
| Real leads | **None.** No run from any id outside the 5 known. |
| Self-triggers | **None**, despite `2952` matching "year old" / "years old". |
| `2952` gates | No emailGate, no followGate. Button to `cesa-guide` intact. |
| `2954` gates | Clean. Button to `consider-this` intact. |
| `445` gates | Clean. Button intact. |
| `432` gates | Clean. Button intact. |

DM inbox, read only, last 24h. 5 threads on Cesa IG `65540` and 4 on main IG `45886`.
**No email address was typed in any thread, so nothing was stranded and no MailerLite write
was needed.** The 5 Cesa threads (`504237`, `504238`, `504442`, `504443`, `505547`) are all
outgoing guide DMs this workspace sent 09-08, every one `status: sent`, `errorCode: null`,
each carrying the `cesa-guide` button. No replies yet.

Two known threads moved and neither is actionable:
- `229724` (House of Trailers, real client) sent one new message at 02:58 UTC: `😍`. Nothing
  to act on. Never reply from a routine.
- `490500` (@emmamilesx pay-to-collab) followed up 09-08 16:08 with *"Hey lovely, we have
  limited spots."* Scarcity nudge on an offer that contradicts her stated policy. Never reply.

## The correction: there are 2 live TUESDAY automations, not 4

The diagnosis written earlier today said all 4 TUESDAY automations sit at 0 triggers. The
run counts were right, the framing was wrong:

| id | State | Keywords |
|---|---|---|
| `447` IG | **`isActive: false`** — "RETIRED, use 2771 (captures email)" | `TUESDAY` only |
| `427` FB | **`isActive: false`** — "RETIRED, use 2772 (captures email)" | `TUESDAY` only |
| `2771` IG | live | `TUESDAY`, `tuesday`, `Tuesday` |
| `2772` FB | live | `TUESDAY`, `tuesday`, `Tuesday` |

Both were retired 08-27T18:13, the same day the URL correction landed. So `AGENT-CONTRACT.md`'s
"All 4 TUESDAY automations now point at the JAT page" describes a state that lasted hours.
**2 live automations at 0 triggers.** The lowercase claim holds: `tuesday` is live on both.

## SECOND FAULT: both live TUESDAY automations still had an emailGate

```
"emailGate":{"message":"Yes! Just Another Tuesday is 1 email a week ...
             Reply with your email address and I'll add you."}
```

This is the exact mechanism that destroyed the 09-05 lead: the gate asks for an email in
thread, the contact never replies, the run expires, and the comment's **one private reply
slot is spent forever**. After that only a public comment reply can reach that person.

The 09-08 gate sweep covered `2952`, `445`, `432`, `1393`, `2954`. **The TUESDAY path was
never in that set.** Both records still read `updatedAt: 2026-08-27T16:10`, untouched since.
Their `dmMessage` also opened "You're in," which is only true after a gate captures an
email, the exact gate-dependent phrasing the watch says to flag.

**This matters more than it looks.** The fix proposed earlier today is to put "Comment
TUESDAY" CTAs on posts. Doing that with the gate in place would have walked every new lead
straight into the trap that already cost 1.

### Fixed, verified on an independent re-read

- **`2771` Instagram: emailGate REMOVED.** `publishedVersionId` 4602 → **8850**,
  `updatedAt` 2026-09-09T06:25:57. Button "Get Tuesdays" to the JAT page intact, all 3
  keywords intact, `dmMessage` rewritten so it no longer claims "You're in" and instead says
  "Tap below and add your email on the page," matching the CESA/CONSIDER construction.

### NOT fixed, needs Amanda

- **`2772` Facebook: emailGate STILL PRESENT.** The identical call was **refused twice by
  this environment's permission classifier**, not by Blotato. Re-read confirms nothing
  partial was written: still `publishedVersionId 4603`, still `updatedAt 2026-08-27T16:10`,
  gate and old "You're in" copy both intact. So Facebook TUESDAY remains a lead-burning
  path until either Amanda removes the gate in the Blotato dashboard or grants the
  permission. The IG side is safe now; the FB side is not.

## Comment run 2026-09-09 06:50 UTC — nothing to answer

1 comment examined in the 8-hour window (since 09-08 22:50). It was `4258636`,
`isAuthor: true`, her own reply on `6691079`: "@emily_nyc_53 thank you, she appreciates such
nice compliments ☺️". Discarded per the filter. No cursor returned, so that was the whole
list. **0 audience comments, 0 unanswered, 0 replies posted, 0 guides sent, 0 spam.**

### Keyword measurement

| | This run | Out-of-sample tally since keywords shipped 09-08 17:46 |
|---|---|---|
| Qualified comments on `65540` | 0 | 1 |
| Caught by live keywords | 0 (none to catch) | 0 |
| Missed | 0 | 1 — "my healthy chi", since fixed with `" chi "` |
| False positives | 0 | 0 |

Tally unchanged. **0 runs fired anywhere in this window**, so no false positive was possible.

### `2954` subscribe-intent keywords: still never fired, now confirmed by run count

`blotato_list_automation_runs` on `2954` returns **an empty list**. Zero runs, ever. So on
Cesa's account neither `CONSIDER` itself nor any of the 6 subscribe-intent phrases
(`sign me up`, `add me`, `count me in`, `the newsletter`, `the weekly`, `weekly note`) has
matched a single comment since going live. That is the whole Consider This funnel on that
account, unvalidated, same as before.

Worth stating plainly next to the JAT finding from earlier today: `2954` at 0 runs and the
TUESDAY pair at 0 runs are the same shape of problem. The automation is not the thing that is
broken. Almost nothing asks anyone to type the word.

---

# Daily lead sync 2026-09-09 13:06 UTC — a real conversion, and the baseline is wrong

## THE NEWS: the Cesa guide funnel converted a stranger overnight

`artinehaladadyan@gmail.com` (field name "A") joined the **Cesa group**
`196024300390581479` at **2026-09-09 02:48:00**, `source: webform`. Sent 1, **opened 1,
clicked 1.** IP `2603:8001:7af0:...`, which is not Amanda's `72.58.115.46`.

This is the conversion the funnel watch has been checking for every 2 hours. It did not come
through a keyword. It came through the landing page.

**Probable attribution, stated as inference and not proof.** 6 guide DMs went out from the
comment sweep on 09-08 between 16:34 and 18:42 UTC, each carrying the "Get the guide" button
to `cesa-guide.subscribepage.io`. This signup lands 8 to 10 hours later, and the Cesa group
went from 3 active to 4. An Instagram contact id cannot be mapped to an email address from
this surface, so which of the 6 it was cannot be established. Recipients were
`1732590004635114`, `1386554462976400`, `4459306094331032`, `977713232018221`,
`2286721815396579`, `2535614900194954`.

## Second correction: there are 7 real subscribers, not 5

The routine's baseline names 5 (Mary, Melissa, Nadia, christine, Laura). Two more are real
and were never recorded:

| Email | Name | Group | Joined | Sent / opens |
|---|---|---|---|---|
| `shaniyaplunkett516@gmail.com` | Shaniya | Consider This | 09-04 16:42, double opt-in confirmed | 1 / 0 |
| `artinehaladadyan@gmail.com` | A | Cesa | 09-09 02:48 | 1 / 1, plus 1 click |

**Both arrived by `source: webform`, i.e. a landing page.** That makes **4 real webform
conversions** to date (christine 08-19 JAT, Laura 08-23 JAT, Shaniya 09-04 Consider This,
artine 09-09 Cesa) against **0 keyword conversions, ever.** Same finding as this morning's
JAT diagnosis, now with 4 data points instead of 2: the pages convert, the keywords never
fire because almost nothing asks anyone to type them.

## The emailGate list is 4, and not the 3 the routine expects

Built from a full sweep of all **40** automations, not from the prompt.

| id | Keyword | Account | Group | Note |
|---|---|---|---|---|
| `4011` | SEASONAL | Cesa IG 65540 | Consider This | gate deliberate |
| `4010` | SEASONAL | FB 30840 | Consider This | gate deliberate |
| `4009` | SEASONAL | IG 45886 | Consider This | gate deliberate |
| `2772` | TUESDAY | FB 30840 | Just Another Tuesday | **gate should be gone, removal blocked** |

Changed from the routine's 08-31 snapshot: `2954` lost its gate 09-08, `2771` lost its gate
today at 06:25, and the 3 SEASONAL automations were created 09-01 and never appeared in it.

**All 4 have 0 runs, ever. Nothing captured, nothing to sync to MailerLite.**

## Health checks

- **No followGate anywhere.** All 40 checked. The 5 that briefly carried one on 08-30
  (`445`, `435`, `1393`, `1019`, `1424`) are all still clean.
- **No duplicate of a live automation.** Every keyword that appears twice is once per account
  (IG 45886 / FB 30840 / Cesa IG 65540). The 6 inactive records are all labelled RETIRED or
  Draft: `450`, `447`, `446`, `427`, `413`, `412`.
- **No failed runs.** Checked runs on all 19 funnel automations (`2952`, `445`, `432`, `2954`,
  `2771`, `2772`, `4009`, `4010`, `4011`, `1393`, `1394`, `1424`, `1422`, `1019`, `1020`,
  `435`, `2778`, `3994`, `3995`). Only failures in the system remain the 2 x 20102 on `445`
  from 08-28, both the test contact, both baseline. **The 21 Target product automations were
  not run-checked** — 21 more calls for affiliate links with no history, said plainly rather
  than implied.
- **No unconfirmed subscribers, and no active subscriber with 0 sends.** Nothing to re-add.

## The 12-send check: nobody qualifies, and a trap for the next run

Condition is sent >= 12 AND opens_count == 0. Nobody meets it.

Melissa (`mmlaird8@gmail.com`) and Nadia (`nadezhda.isaenko.psy@gmail.com`), the two the rule
was written for, were **already suppressed on 2026-09-08 15:03:38**, both at 9 sends and 0
opens, both `status: unsubscribed` and not deleted, which is the correct method. They never
reached 12 and are no longer accumulating sends.

**Trap:** `amanda@gentlemuse.co` is at **11 sends, 0 opens**. It crosses 12 on the next send
and will meet the condition exactly. It is Amanda's own address and must never be flagged for
removal. Exclude her own addresses before applying this check, every time.

## Keyword false-positive risk nobody is watching

The 09-08 recommendation was to drop the bare lowercase form on `brow`, `play` and `native`
because their host words are too common. That was **not applied, or was reverted**. Live now:

| id(s) | Bare lowercase keyword | Matches inside |
|---|---|---|
| `439`, `423` | `brow` | brown, browse, brows, eyebrow |
| `1019`, `1020` | `play` | playing, played, player, display |
| `442`, `426` | `native` | alternative, imaginative |
| `454`, `6025` | `gel` | **angel** |

These are all Target affiliate automations on IG 45886 and FB 30840. A false positive both
sends a stranger a product ad and spends that comment's single private reply slot. The comment
routine's keyword measurement only covers Cesa's account `65540`, so nothing is watching these.
**Proposed, not applied:** space-pad them (`" brow "`, `" play "`, `" gel "`) the way `" chi "`
was, or drop to all-caps plus Title. Keyword config is Amanda's call.
