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

## Open item

Just Another Tuesday has no keyword yet. TUESDAY is the obvious candidate. Once Amanda sets it
up in ManyChat, every JAT post on Instagram and Facebook should use it, and that also removes
the dependency on the JAT signup URL for those 2 platforms. (That URL is no longer
unknown: https://just-another-tuesday-gm.subscribepage.io, verified in Drive 08/18.)


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
