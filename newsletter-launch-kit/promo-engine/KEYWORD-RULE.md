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
