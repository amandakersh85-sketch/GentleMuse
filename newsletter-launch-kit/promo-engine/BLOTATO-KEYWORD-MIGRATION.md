# Keyword automation: ManyChat to Blotato migration

**Deadline: 2026-09-11.** ManyChat subscription ends. Everything must be on Blotato by then.
All 12 DM automations are BUILT. Only activation timing separates them.

## Live now

| ID | Keyword | Platform | Offer |
|---|---|---|---|
| 2771 | TUESDAY | Instagram | Just Another Tuesday |
| 2772 | TUESDAY | Facebook | Just Another Tuesday |

TUESDAY is new, so there is no ManyChat flow to collide with. It went live immediately.

## Built, inactive, flip on Sept 10

| ID | Keyword | Platform | Offer |
|---|---|---|---|
| 2773 / 2774 | CONSIDER | IG / FB | Consider This |
| 2775 / 2776 | GUIDE | IG / FB | AI Beginner's Guide |
| 2777 / 2778 | RESET | IG / FB | Reset Guide |
| 2779 / 2780 | PLAY | IG / FB | Press Play book list |
| 2781 / 2782 | CESA | IG / FB | Cesa guide |

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
