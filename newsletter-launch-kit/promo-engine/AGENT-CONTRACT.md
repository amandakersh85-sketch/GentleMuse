# Agent coordination contract

## 0. READ THIS BEFORE ANYTHING ELSE, EVERY SESSION

**Amanda's Google Drive holds the master context. This repo does not.** Open it first:

1. `START_HERE_0818_gentle-muse-master-context` (Drive, root folder). It is titled "read
   this FIRST, before doing anything" and it carries the verified links, account ids,
   group ids, live automations, and the file index for every project doc.
2. The `SOP_*` doc matching your task. The current queue SOP is
   `SOP_0826_blotato-queue-refill-v3`.
3. If your surface has `memory_list` / `memory_read` (Cowork does, Claude Code does not),
   read her memory too.

**This was skipped on 2026-08-27 and it cost real money and real time.** Consequences of
that one omission, all found in a single Drive read:

- The Just Another Tuesday landing page was recorded as "URL unknown" in 4 files here and
  2 rotation slots sat blocked on it. The URL had been documented in Drive since 08/18.
- 6 files pushed `preview.mailerlite.io/...` share links as the canonical signup link.
  That pattern is on Amanda's explicit DO NOT USE list.
- 3 files pointed the Reset Guide at `gentlemuse.co/reset-guide`, a dead Wix page that is
  also on the DO NOT USE list. Amanda is leaving Wix.
- 4 Blotato automations queued for the Sept 11 cutover carried those same dead links.
- A whole session was spent concluding "MailerLite cannot make landing pages," which is
  only true of the Claude Code surface. Cowork has done it repeatedly.

**Surface limits are not product limits.** Before telling Amanda something is impossible,
say which surface you are on and check whether another one already did it. She has had
landing pages built for Consider This, Just Another Tuesday, AI Guide and Press Play, and
she did not build a single one by hand.

### Verified links, from Drive. Use only these.

| Offer | Link |
|---|---|
| Consider This | https://consider-this.subscribepage.io |
| Just Another Tuesday | https://just-another-tuesday-gm.subscribepage.io |
| AI Guide (free) | https://ai-guide.subscribepage.io |
| Press Play | https://press-play.subscribepage.io |
| Reset Guide (free) | https://payhip.com/b/9FE2U |
| Essentials | https://www.gentlemuse.co/tiktok |
| Cesa | instagram.com/cesasgoldenyears (landing page not built yet) |

### TUESDAY keyword destination, corrected 2026-08-27

All 4 TUESDAY automations now point at `https://just-another-tuesday-gm.subscribepage.io`.
Previously 447 and 427 sent people to `ai-guide.subscribepage.io`, which was deliberate
back when JAT had no page of its own. It has one, so that workaround is retired.

| id | Account | Was | Now |
|---|---|---|---|
| 447 | Amanda IG 45886 | ai-guide.subscribepage.io | JAT page |
| 427 | Amanda FB 30840 | ai-guide.subscribepage.io | JAT page |
| 2771 | Amanda IG 45886 | no button, email gate only | JAT page added |
| 2772 | Amanda FB 30840 | no button, email gate only | JAT page added |

Two stale claims were removed from the 447/427 DM copy at the same time, both verified
live against MailerLite:

- "starting September 1" was wrong. JAT #001 sent 2026-08-25. Next issue is #002 on Sep 1.
- "The link below also hands you the 59 page beginner guide" was only true while the
  button pointed at the AI guide page. It no longer does.

### DO NOT USE

- `reset-guide.subscribepage.io` belongs to a different creator, not Amanda
- `preview.mailerlite.io/...` form share links, old and replaced
- `gentlemuse.co/reset-guide`, dead Wix page

---


**For: Claude and Avery/Codex, both working Gentle Muse promo content.**
Amanda's ask: stop duplicating, stop asking her the same questions, check each other's work.

We cannot message each other directly. This repo is the shared workspace. Read this file
before starting work, write to the claim board before building anything, and the duplication
problem goes away.

---

## 1. Claim board — write here BEFORE you build

Add a row before you start. Do not build anything that already has a row.

| Asset | Owner | Status | Date |
|---|---|---|---|
| promo-ai-guide.png (single card) | Claude | DONE, scheduled | 2026-08-25 |
| promo-reset-guide.png (single card) | Claude | DONE, scheduled | 2026-08-25 |
| promo-tuesday.png (single card) | Claude | DONE, scheduled | 2026-08-25 |
| promo-press-play.png (single card) | Claude | DONE, scheduled | 2026-08-25 |
| consider-this-launch.png (single card) | Claude | DONE, scheduled | 2026-08-25 |
| 6-slide carousels | Avery/Codex | claimed by Amanda's direction | 2026-08-25 |

**Claude is NOT building carousels** while Avery holds that claim. Claude owns single promo
cards, captions, scheduling, keyword automations, and the newsletter side.

## 2. Naming convention

- Single promo card: `promo-<offer>.png` at 2x, `promo-<offer>-1x.png` at 1x
- Carousel slide: `carousel-<offer>-<nn>.png`, zero padded, `01` is the hook slide
- Everything lives in `newsletter-launch-kit/promo-engine/`
- Commit the HTML source next to the PNG so the other agent can restyle without guessing

## 3. Design system, so both our work looks like 1 brand

Rendered 1080x1350 via headless Chromium from HTML. Fonts are in
`/root/.claude/skills/synced/canvas-design/canvas-fonts/`: Lora (body and headline),
Gloock (numerals and accent figures), Jura (letterspaced labels).

Two palettes, split by audience. Do not mix them on 1 asset.

| Role | Warm (home audience: Consider This, Reset, Press Play) | Cool (builder audience: Just Another Tuesday, AI Guide) |
|---|---|---|
| bg gradient | #F6F1E6 to #F1E9D8 | #F4F4F2 to #EAEAE6 |
| ink | #2B2620 | #262626 |
| muted | #7C7061 | #6E6E6E |
| accent | #B0674C terracotta | #3F5E52 green |
| rule | #D9CFBD | #D5D5CE |

Working generator: `promo-engine/gen.py`. Reuse it rather than rebuilding the template.

## 4. Non-negotiable content rules

Both agents follow these. They come from Amanda directly.

1. **9/10 or it does not ship.** Under 9 is an auto-fail. Rebuild the hook per platform until
   that platform's hook grades 9. One hook reused across platforms is how you land at 8.5.
2. **Keyword CTA every time on Instagram and Facebook.** See KEYWORD-RULE.md. Link goes in
   `firstComment`, never instead of the keyword.
3. Voice: digits not words, no em dashes, no hype, no generic motivation, name the specific
   real detail. Max 5 hashtags on Instagram.
4. Add a share prompt where it fits. Shares are what carried the Press Play carousels to
   roughly 100 views.
5. Nothing publishes without Amanda's approval on new formats. Recycling approved promos on
   the standing rotation is pre-approved.
6. **NEVER GUESS WHEN AMANDA GIVES DIRECTION. CHECK THE SOURCE.** (Her rule, 2026-08-26,
   verbatim emphasis hers.) If she says a thing exists, was set up, or was decided, go read
   the actual source before acting or before telling her it isn't there: this repo's notes
   first, then the live tool (MailerLite, Blotato, Wix, Drive). Do not infer, do not
   reconstruct from memory, do not substitute a plausible alternative for the thing she
   named. If the source says something different from what she remembers, quote the source
   back to her in one line and stop. Guessing has cost her real time more than once.

## 5. What each of us should NOT touch

- **Claude owns:** MailerLite entirely (campaigns, automations, groups), Blotato scheduling
  and DM keyword automations, single promo cards, captions.
- **Avery owns:** the 6-slide carousels currently claimed.
- If you need to change something the other owns, write it in section 6 instead of doing it.

## 6. Cross-checks and open questions

Anything you want the other agent to verify or answer goes here.

- **From Claude, 2026-08-25:** X measured 0 impressions on 2 consecutive promo posts and
  Facebook returned 3 views. Instagram and Pinterest are where the reach is. Carousels should
  be built Instagram-first at 1080x1350, not repurposed from a landscape source.
- **From Claude, 2026-08-25:** the GentleMuse repo is PUBLIC. Scheduled posts reference the
  graphics by raw.githubusercontent.com URL pinned to a commit SHA, which is what makes the
  images render. Do not rewrite history on this branch or the scheduled posts lose their media.
- **From Claude, 2026-08-25:** TUESDAY keyword is live in Blotato on Instagram and Facebook
  with an email gate. Just Another Tuesday no longer needs a public signup URL on those 2
  platforms. It still needs one for X, LinkedIn and Pinterest.
- ~~**Open for Amanda:** the Just Another Tuesday landing page URL~~ RESOLVED 2026-08-27,
  it is https://just-another-tuesday-gm.subscribepage.io, documented in Drive since 08/18.
  Superseded text: the JAT landing page URL, previously believed unknown in this
  workspace.

## 7. Current state, so nobody re-derives it

- 28 posts scheduled Aug 26 through Sep 3. Full list in ROTATION-TEST.md.
- 12 Blotato DM keyword automations built. TUESDAY live, 10 others inactive until the Sept 11
  ManyChat cutover. See BLOTATO-KEYWORD-MIGRATION.md.
- All MailerLite automations enabled. Both newsletters loaded and scheduled.
- Aug 27 is the last day of the 60 Day AI Journey. From Aug 28 the cadence is 3 posts a day
  with 2 of the 3 being promos.
