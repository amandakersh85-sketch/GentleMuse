# The Gentle Muse Flywheel — loops and status

**Date:** 2026-08-20
**The wheel:** Social → signup → newsletter → value + affiliate revenue → guides → nurture → paid product → back to newsletter. Every arrow below is a loop; a broken arrow leaks people.

---

## Loop map

### 1. Social → newsletter signup — CLOSED (today)
- 9 launch posts scheduled on X / Facebook / LinkedIn (Aug 20, 22, 25).
- Launch graphic created for Instagram/Facebook.
- Signup link: https://consider-this.subscribepage.io
- **Amanda:** bio link + post the graphic + record TikTok Reel from Post 1 script.

### 2. Existing subscribers → newsletter — CLOSED (today)
- "Want in?" invite sent to all 9 existing subscribers. 100% delivered.
- Newsletter campaigns filter to the Consider This group, so growth = people who opt in.

### 3. Signup → warm welcome — BUILT, needs activation
- Automation "Consider This — Welcome (new subscribers)" (196338050950759852).
- Now includes a P.S. gifting the free Reset Guide (payhip.com/b/9FE2U), which closes
  newsletter → lead magnet.
- **Amanda: activate it** → https://dashboard.mailerlite.com/automations/196338050950759852

### 4. Lead magnet → newsletter — BUILT, needs activation (the big leak, now plugged)
- Previously: Reset Guide nurture (6 emails) ended in silence. Guide subscribers were
  never told the newsletter exists. This is why 8 of 9 subscribers weren't on it.
- New automation "Newsletter Cross-Invite — after lead magnet nurture" (196342476720571577):
  14 days after joining any lead magnet group (Gentle Muse Subscribers, AI Beginner's
  Guide, Press Play, Bottleneck Quiz), sends 1 invite to Consider This. Fires once per
  subscriber, only for future joins.
- **Amanda: activate it** → https://dashboard.mailerlite.com/automations/196342476720571577

### 5. Newsletter → revenue — ALREADY CLOSED (by Amanda)
- Issue #001 shipped today at 7:00 AM with Target affiliate links and disclosure. 8 more
  issues queued weekly through Oct 15.
- Reset nurture pitches the $17 7-Day Gentle Reset (payhip.com/b/vb2PB).

### 6. Newsletter → referral — ALREADY CLOSED (by Amanda)
- Issue footer: "Know someone who'd want this? Send them to consider-this.subscribepage.io"
- **Amanda: verify that landing page loads on your phone** (this sandbox can't reach it).
  If it works, it's a prettier canonical signup link than the preview URL for bios.

### 7. Measure → adjust — CLOSED (today)
- Automated check-in fires Fri Aug 22, noon CT: invite opens/clicks, subscriber growth,
  form conversions, issue #001 stats, automation activation status, next action.

---

## Known leaks, deliberately left (small)
- Embedded forms "Reset Guide Signup, GM" and "AI Beginner's Guide — signup" are empty,
  inactive shells (no content designed). The working Reset Guide entry is the site popup
  (active, 15 opens, 1 conversion). Design the embedded forms in the dashboard only if a
  page needs an inline form; otherwise ignore or delete them.
- The AI Beginner's Guide group has 0 subscribers; its delivery automation is ready but
  the guide has no live front door yet. Worth a social post + working form when Amanda
  wants to push it.
- Scheduled social posts use the long preview signup URL. Works fine; swap to
  consider-this.subscribepage.io in future posts once Amanda confirms it loads.

---

## The second newsletter: Just Another Tuesday (added 2026-08-21)

**What happened.** Amanda's Skool post in Women Build AI ("Just Another Tuesday . . . .
Or is it?") drew real feedback Aug 17-20 (8 likes, comments). On Aug 19, Christine
(chgaiotti@gmail.com) signed up for Just Another Tuesday via a subscribepage.io landing
page. But JAT had 0 campaigns and 0 automations in MailerLite: its 5 September issues
(v3, Amanda-corrected) were drafted in Drive on Aug 18 and stopped at Amanda's own
approval gate ("Nothing goes into MailerLite until Amanda reads and approves the copy").
Same morning, Consider This DID get fully loaded and scheduled, which is why it felt
handled.

**Closed on 2026-08-21:**
- Bridge note "You're early. That's the best seat." SENT to the JAT group (Christine +
  Amanda). Sets the premise, teases Issue 1, gracefully covers the mis-aimed guide
  invite she received.
- JAT welcome automation BUILT (196381310295475426), needs Amanda's activation.

**Loaded and scheduled (Amanda approved 2026-08-21):** all 5 v3 issues are in
MailerLite, status ready, sending to the Just Another Tuesday group at 7:00 each Tuesday:
- #001 He Couldn't Prove He Wrote It — Aug 25 (196381563274921031)
- #002 My Robots Took 2 Mondays Off — Sep 1 (196381581785433178)
- #003 The Wix Ceiling — Sep 8 (196381600378783573)
- #004 Still My Best Post Ever — Sep 15 (196381630673192538)
- #005 Be Bad On Purpose — Sep 22 (196381652112377183)
Copy is verbatim from the v3 Drive doc, internal notes stripped, sabrina.dev linked in
#003. One week earlier than the doc's September dates, which keeps the wrappers fresher.
Pre-send verification reminders armed: Sep 7 (Sabrina subscriber phrasing for #003,
wrapper glance for #004) and Sep 18 (Anthropic course count for #005). Each campaign
stays editable in the dashboard until its send morning.

**Still open:**
- The dual popup (195832725497709843) is inactive AND feeds the wrong group (Gentle
  Muse Subscribers, not the 2 newsletter groups). Fix group assignment in the dashboard
  before ever activating it.
- ~~Exact JAT subscribepage.io URL unknown.~~ RESOLVED 2026-08-27. It is
  **https://just-another-tuesday-gm.subscribepage.io** and it has been documented in
  Drive since 08/18 in `START_HERE_0818_gentle-muse-master-context`. This workspace
  called it unknown for 6 days because no session read that file.
- Amanda's own blockers doc also flags the Paycheck Planner pricing decision ($22
  standing discount vs $37 anchor) before the November campaign.

---

---

## Results check-in — 2026-08-25 (5 days after launch)

| Metric | Aug 20 | Aug 25 |
|---|---|---|
| Total subscribers | 9 | 10 |
| Consider This group | 1 | 2 |
| Just Another Tuesday group | 2 | 2 active + 1 unconfirmed |
| Signup form opens | 5 | 8 |
| Signup form conversions | 0 | 1 (12.5%) |

- **Invite campaign:** 9 delivered, 3 opens (33.3%), 1 click (11.1%) on the signup
  button, 33.3% click-to-open. That click converted on Aug 21 at 19:32, which is the
  Consider This group going 1 to 2. The invite is the only thing that has produced a
  newsletter signup so far.
- **All 6 launch posts published** (Post 1 Aug 20, Post 2 Aug 22, across X, Facebook,
  LinkedIn). Post 3 is scheduled for Aug 25 6:00 PM CDT. Form opens went 5 to 8 in that
  window, so social produced traffic but no conversion yet.
- **JAT #001 sent on time** Aug 25 at 7:00 AM, 2 delivered, 100% delivery. Too early for
  opens at the time of this check.
- **Consider This #001** (Aug 20) went to 1 person and has 0 opens. It sent before the
  invite grew the group, so it reached the smallest possible audience.
- **All 3 new automations are still switched off.** The Aug 21 signup got no welcome
  email, and the unconfirmed JAT subscriber is stuck at double opt-in with nothing
  chasing them. This is the live cost of the pending activation clicks.

**Highest-impact next action:** the 60 Day AI Journey series is at Day 58 and ends this
week. Those posts run daily to the exact audience Just Another Tuesday serves, and none
of them mention it. The finale is the natural handoff: the 60 days end, the Tuesdays
continue. Nothing else in the funnel reaches that many of the right people for free.

---

## Amanda's activation list
1. Activate Consider This welcome: https://dashboard.mailerlite.com/automations/196338050950759852
2. Activate cross-invite: https://dashboard.mailerlite.com/automations/196342476720571577
3. Activate JAT welcome: https://dashboard.mailerlite.com/automations/196381310295475426
4. Open consider-this.subscribepage.io on your phone and confirm it loads.
   (This is now the canonical link everywhere. The old preview.mailerlite.io share
   links were on Amanda's DO NOT USE list and have been purged from this kit.)
5. ~~Paste the JAT signup URL.~~ Done, it was already in Drive: just-another-tuesday-gm.subscribepage.io
