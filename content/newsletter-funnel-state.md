# Newsletter funnel state, 27 Aug 2026

What the holiday campaign depends on, what was fixed, and the one thing only
Amanda can do. Written because SPEC_0818 flagged "the signup form is switched off
AND wired to the wrong group" as a revenue blocker for the November sale, and
that turned out to be half right and worse than described.

## The form in question

`Gentle Muse Newsletters — Consider This + Just Another Tuesday`
Form id `195832725497709843`, type **popup**, slug `UGuJgo`
Dashboard: https://dashboard.mailerlite.com/forms/195832725497709843/overview

Not to be confused with `Consider This — Social Launch Signup` (`195835257531925894`),
which is a different, **embedded** form. That one is active, correctly wired to the
Consider This group, and has taken registrations. The spec's complaint was never
about it. Anyone re-checking this should look at the popup.

## What was actually wrong

The popup was wired to a single group: **Gentle Muse Subscribers**
(`191820189953688990`).

That group is the trigger for automation `191820204159796265`, *Reset Guide
Welcome + Nurture Sequence*, which is enabled and runs **6 emails** opening
"Hey Reset Bestie" and pitching the 7-Day Gentle Reset.

So a visitor who signed up for two newsletters would have:

1. been added to neither newsletter group,
2. received a 6-email sequence about a different product,
3. never appeared on the list the Black Friday sale is sent to.

Switching the form on without fixing the wiring first would have been worse than
leaving it off.

## Fixed on 27 Aug

Groups rewired via the API and verified by reading the record back:

| Before | After |
| --- | --- |
| Gentle Muse Subscribers (191820189953688990) | Consider This (195832544509298574) |
| | Just Another Tuesday (195832548837819660) |

`has_missing_groups: false`, `is_broken: false`. The legacy group is detached, so
the Reset Guide sequence can no longer fire from this form.

## STILL TO DO, and only Amanda can do it

**The form is still `active: false`.** The MailerLite API accepts `active` in a
PUT and returns 200, but silently ignores it. It is a dashboard-only toggle.

1. Open https://dashboard.mailerlite.com/forms/195832725497709843/overview
2. Switch the form on.
3. Confirm the groups still read Consider This and Just Another Tuesday.

Until that toggle is on, the popup collects nothing, and the only route into the
Just Another Tuesday list is the TUESDAY comment keyword feeding the daily DM
sync. That works, but it is one channel carrying a sale.

## Two judgement calls left alone on purpose

**Two welcome emails.** With both groups attached, one signup now triggers both
`Consider This — Welcome` and `Just Another Tuesday — Welcome`. Each is a single
step, so it is 2 emails at once, not a flood. It is honest, they did sign up for
both, but it reads better as one combined welcome. Worth tidying, not urgent, and
not something to change quietly before a campaign.

**Double opt-in is on.** It costs conversions on a small list and protects
deliverability. The sibling embedded form sits at 8 opens and 1 conversion, and
double opt-in is a plausible part of that. This is a real tradeoff and Amanda's
call, so it was left as found.

## List sizes as of 27 Aug 2026

| Group | Active |
| --- | --- |
| Consider This | 2 |
| Just Another Tuesday | 2 (plus 1 unconfirmed) |
| Gentle Muse Subscribers | 7 |

The November sale goes to Just Another Tuesday. At 2 confirmed subscribers, the
form toggle is the difference between a campaign and an email to 2 people.
