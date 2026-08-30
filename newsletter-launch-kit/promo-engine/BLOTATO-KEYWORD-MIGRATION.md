# Keyword automation: ManyChat to Blotato migration

**Deadline: 2026-09-11.** ManyChat subscription ends. Everything must be on Blotato by then.
All 12 DM automations are BUILT. Only activation timing separates them.

## Live now

| ID | Keyword | Platform | Offer |
|---|---|---|---|
| 2771 | TUESDAY | Instagram (main) | Just Another Tuesday |
| 2772 | TUESDAY | Facebook | Just Another Tuesday |
| 2952 | CESA | Instagram (cesasgoldenyears) | Cesa guide |
| 2954 | CONSIDER | Instagram (cesasgoldenyears) | Consider This |

Cesa's channel had no keyword automation at all, so both went live immediately with no
ManyChat collision to worry about. CONSIDER belongs there because every Consider This issue
closes with an "And for Cesa" section, so the dog audience is being sent something that
genuinely includes them rather than a bolted-on newsletter pitch.

TUESDAY is new, so there is no ManyChat flow to collide with. It went live immediately.

## Built, inactive, flip on Sept 10

| ID | Keyword | Platform | Offer |
|---|---|---|---|
| 2773 / 2774 | CONSIDER | IG / FB | Consider This |
| 2775 / 2776 | GUIDE | IG / FB | AI Beginner's Guide |
| 2777 / 2778 | RESET | IG / FB | Reset Guide |
| 2779 / 2780 | PLAY | IG / FB | Press Play book list |
| 2953 / 2782 | CESA | IG (main) / FB | Cesa guide |

These stay off until the cutover because ManyChat still owns those keywords. Activating early
would DM every commenter twice. A reminder fires Sept 10 to flip all 10 and to prompt Amanda
to switch the matching ManyChat flows off.

## The email gate solves the missing landing page

TUESDAY, CONSIDER, PLAY and CESA use Blotato's email gate: the DM asks for the address, waits
for the reply, and saves it to the contact. That means Just Another Tuesday no longer needs a
public signup URL to collect subscribers on Instagram and Facebook. The DM is the form.

GUIDE and RESET use a link button instead, because both already have a working destination.

## The one gap, and how it is covered

Blotato captures the email in the DM thread but does not push it to MailerLite. Nothing
bridges those 2 systems automatically. A weekly job pulls captured addresses from the
automation runs and adds them to the right MailerLite group, then re-arms itself. First run
Sept 1.

If Amanda ever wants this instant instead of weekly, the automations accept a webhook that
fires with the captured email as JSON. That needs 1 public endpoint to exist.


## Cesa's channel: the unlock, and what is still missing

Amanda's read is right. cesasgoldenyears had an engaged audience converting to nothing at
all. It now has 2 live keywords, CESA and CONSIDER.

**The bigger opportunity, not yet built:** there is no lead magnet made for that audience.
CESA delivers a personal essay and CONSIDER delivers a home newsletter. Neither is the thing
a senior dog owner would trade an email for without hesitating. A short senior dog checklist,
the practical version of what Amanda already does for Cesa, would be. Floor traction, where
they sleep versus where you walk carrying something hot, water bowl height, the things that
change when a dog stops moving out of the way.

That is a real gap and it is Amanda's call whether to build it.

**Deliberately not added to Cesa's channel:** GUIDE and TUESDAY. Both serve the builder
audience and would read as spam on a dog account. PLAY and RESET are plausible later, but
adding 4 keywords to a channel with 2 working ones dilutes rather than converts.

---

## 2026-08-30: ManyChat is dead. The cutover happened today, not Sept 11.

**Amanda disconnected her Instagram and Facebook accounts from ManyChat on 2026-08-30.**
Her words: "ManyChat is now a dead end. We're not utilizing it anymore. We're going strictly
with Blotato."

Everything above that describes a *pending* Sept 11 cutover is history. There is no cutover
left to run. Blotato is the only tool holding these keywords, on both accounts, on both
platforms. The Sept 11 deadline is moot and the Sept 10 reminder has nothing to fire on.

### The 10 `DO NOT ACTIVATE` drafts are now pure liability

They were built as the Sept 11 replacements for automations that were still live in ManyChat.
Those originals never went anywhere, so every one of these 10 is a duplicate of a Blotato
automation that is already live and already working.

| Draft | Duplicate of | Keyword / platform |
|---|---|---|
| 2953 | 445 | CESA / IG |
| 2781 | 445 | CESA / IG |
| 2782 | 432 | CESA / FB |
| 2773 | 1393 | CONSIDER / IG |
| 2774 | 1394 | CONSIDER / FB |
| 2775 | 1424 | GUIDE / IG |
| 2776 | 1422 | GUIDE / FB |
| 2777 | 435 | RESET / IG |
| 2779 | 1019 | PLAY / IG |
| 2780 | 1020 | PLAY / FB |

All 10 are inactive. Activating any one of them recreates the exact race that cost 3 of 4
leads on 08-28, except this time Blotato would be racing itself. They serve no purpose now.
**Recommend deleting all 10.** Deletion is irreversible, so it waits on Amanda's word.

### Does Blotato have a message-to-new-follower trigger?

**No.** Asked and answered against the API, not from memory. `blotato_create_automation`
accepts exactly two trigger types:

```
type: "comment-received"  = fire on a comment
type: "message-received"  = fire on a DM
```

That enum is the whole list. There is no follow event, no new-follower event, nothing that
fires on anything but a comment or a DM. All 55 automations on the account use one of those 2.

`followGate` is the near miss and it is worth knowing what it actually does, because the name
invites the wrong assumption. It is a **gate on a DM that is already firing**, Instagram only:
someone comments the keyword, and instead of the guide they get "follow me first" plus a
button. Once they follow, the real DM goes out. It converts a commenter into a follower. It
does not notice a follower and message them.

Nothing to wire. Per Amanda: "If not, don't worry about it."
