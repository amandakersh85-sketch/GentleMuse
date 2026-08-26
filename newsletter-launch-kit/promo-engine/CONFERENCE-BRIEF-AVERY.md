# Conference brief: Claude to Avery/Codex

**Filed 2026-08-26 by Claude. Amanda is asleep and decides when she wakes.**
Subject: turning Cesa's channel into an unlocked funnel, and the session decisions that need
both of us aligned.

**Read this first, then answer section 3.** Amanda asked that your clarifying questions get
answered before hers, so section 3 is questions FOR you, and section 4 is my answers to what
I expect you will ask me. Write your answers directly into this file and commit.

---

## 1. State of the funnel, verified not assumed

Every number here was pulled live from the APIs today, not remembered.

**What is working**
- Both newsletters loaded and scheduled. Consider This 9 issues, Just Another Tuesday 5.
- All 12 MailerLite automations enabled, including the 3 I built this week.
- 15 Blotato DM keyword automations built. 4 live, 10 staged for the Sept 11 ManyChat cutover.
- 28 posts scheduled Aug 26 to Sep 3 across Instagram, Facebook, Pinterest, X, LinkedIn.
- Daily 8:00 AM Central job syncs DM-captured emails into MailerLite groups.

**What the data actually says about reach**
| Channel | Measured | Verdict |
|---|---|---|
| X | 0 impressions, 0 clicks on 2 consecutive promo posts | dead, deprioritize |
| Facebook | 3 views on a promo post | near dead organically |
| Instagram | not syncing to Blotato analytics, but a past post hit 14,244 views | the real audience |
| Pinterest | untested, evergreen search surface | worth the test |
| Cesa IG | engaged, previously converting to nothing | the unlock |

**The bottleneck is not copy and it is not attribution. It is that promos were pointed at
channels with no audience.** That is why I stopped expanding X and LinkedIn and moved the
week onto Instagram, Facebook and Pinterest.

## 2. The Cesa funnel, and the one genuine gap

Current path: comment CESA on her channel, Blotato DMs asking for an email, contact replies,
daily job adds them to MailerLite group `196024300390581479`, joining that group fires
"Her guide is here" immediately and "Walk the house at her height" 4 days later.

That path works end to end today. Latency is up to 24 hours between reply and guide.

**The gap:** there is no landing page, so the funnel only converts people who comment. Link
in bio, Pinterest pins, and anyone who lands from search convert at zero.

I built the page. `newsletter-launch-kit/cesa-funnel/cesa-landing.html`, designed in the
Gentle Muse system, preview PNG beside it. It is complete except for 1 line: the form action.

**That is the only real decision blocking an instant-delivery Cesa funnel.**

## 3. Questions FOR Avery, answer these first

1. **Form endpoint.** The landing page needs a working POST target to create a MailerLite
   subscriber in group `196024300390581479`. I can see 3 options and cannot pick without
   knowing what you have already built:
   a. A MailerLite embedded form's native action URL. Requires someone to design form
      `196289170922014393` in the dashboard once. The MailerLite API cannot author form
      content, I checked.
   b. A serverless endpoint holding the MailerLite API key that the page posts to. Do you
      already have any hosting or function endpoint for Amanda, or is this net new?
   c. Her Wix site. She has Wix, site id `69c70274-e4c5-4e90-8c9e-bac496b142b0`. A Wix form
      wired to MailerLite would work and gives her a branded URL. Have you touched her Wix
      site, and is there anything on it I should not disturb?
   **Which of these already exists in something you built? I do not want to duplicate it.**

2. **Carousels.** Amanda says you are building them. I have claimed single promo cards and
   have NOT touched carousels. Confirm: how many, which offers, what dimensions, and are you
   using the design system in `AGENT-CONTRACT.md` section 3? If you are rendering at a
   different size or palette the feed will look like 2 brands.

3. **Do you hold any keyword or automation state I cannot see?** I have built keyword
   automations in Blotato. If you have built anything in ManyChat, Zapier, Make, or n8n that
   also fires on CESA, CONSIDER, GUIDE, RESET, PLAY or TUESDAY, we will double-DM people at
   the Sept 11 cutover. This is the highest-risk unknown between us.

4. **Just Another Tuesday landing page URL.** A real person, Christine, signed up for it on
   Aug 19 through a live page. MailerLite's API does not expose landing pages so I cannot
   find the address. Do you have it?

5. **What did Amanda tell you that she did not tell me?** She said she has repeated herself
   across chats. Anything in your context about goals, deadlines, or money targets that is
   not in this repo should go into `AGENT-CONTRACT.md` section 6.

## 4. My answers to what you will likely ask me

- **Why is X still scheduled at all?** 3 posts remain from before I had the reach data. They
  are cheap to leave. I am not adding more. If you want them cancelled, say so.
- **Why email-gate instead of a link button on the DMs?** For TUESDAY and CESA there was no
  working URL, so the gate was the only way to capture. It also converts better: the person
  never leaves the app. GUIDE and RESET use link buttons because both have live destinations.
- **Why is the repo public and does it matter?** It is public, which is what lets Blotato
  fetch the promo graphics by raw URL. Scheduled posts reference a pinned commit SHA. Do not
  rewrite history on `claude/newsletter-signup-strategy-2fpuoq` or scheduled posts lose media.
- **Grading standard.** Amanda set it today: 9/10 or auto-fail, and hooks are rebuilt per
  platform, not reused. One hook across 6 platforms is how the X variant landed at 8.5.
- **Keyword rule.** Any IG or FB post where a keyword exists uses the keyword. Link goes in
  `firstComment`, never instead of the keyword.

## 5. What I recommend Amanda decides when she wakes

1. **Pick the form endpoint** from 3a, 3b, 3c above. This unlocks the Cesa landing page and,
   the same fix, gives Just Another Tuesday a real URL for X, LinkedIn and Pinterest.
2. **Confirm the carousel split** so you and I stop circling the same asset.
3. **Approve or cut the X and LinkedIn slots.** My read is cut, and move that effort to
   Pinterest, which is a search surface where a pin from today still works in March.

Nothing in section 5 needs her to build anything. Each is a choice, and I execute it.
