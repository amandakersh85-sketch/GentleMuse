# Club Target audit (Sun/Wed) — TikTok coverage + theme windows

- id: trig_01CHbGjy41Va6Pw7LVCSGC83
- cron (UTC): 0 0 * * 1,4
- enabled: True
- bound session: session_01XtExtQnr44bCFsA7WAyvut
- connectors: none
- model: default

## Prompt

Run the Club Target audit for Amanda (The Gentle Muse), handle `amanda.20`.

CLOCK DISCIPLINE. Blotato and Metricool return UTC. Amanda is Central: UTC-5 during CDT, UTC-6 from 1 Nov 2026. Convert before judging any time as good or bad. A past audit wrongly called 22:50 UTC a bad slot; it is 5:50 PM Central and it is fine.

POINTS REALITY, confirmed by Amanda 30 Aug 2026. No Club Target credit on Instagram until she crosses 500 followers.
- TikTok is 30 points and is the ONLY placement that pays.
- Instagram Reel and Story are worth 0. A theme is worth 30, not 75.
- Do not put Instagram Stories on her task list. Do not chase unmatched Reels.
- Keep distributing to Instagram anyway, it feeds the follower gate. It is just not points.
Re-check if she crosses 500.

=== POOLED SNAPSHOTS ARE NOT STATE. READ BEFORE REPORTING ANYTHING. ===

Added 14 Sep 2026 after two phantoms in one run.

`blotato_list_posts` results are often too large to read inline and get saved to files. Those files accumulate across runs. **Pooling them tells you what was true at various past moments, not what is true now.**

On 14 Sep, pooling 15 snapshot files taken over 3 weeks produced:
- 3 "scheduled" Club Target rows missing a tag. `blotato_get_schedule` returned NOT FOUND for all of them. They no longer exist.
- 36 "duplicate groups". Against a single fresh pull there were ZERO. They were the same posts seen in different snapshots.

**Rule: any check that asks "what is scheduled right now" runs against ONE fresh pull.** Pooling is only valid for questions about the published past, such as which themes have ever had a TikTok row.

=== THE PRICING RULE, CORRECTLY SCOPED. READ THIS BEFORE FLAGGING A PRICE. ===

Corrected by Amanda 13 Sep 2026. See `content/canon/pricing-rule.md`.

**The rule: she cannot state prices for TikTok Shop items she links on TikTok.**
That is the whole rule. It comes from a TikTok Shop violation on 4 Aug 2026, enforced by TikTok Shop against TikTok Shop listings.

**It is NOT a Target rule.** Club Target has no pricing penalty and never issued one. Target's own Scope of Work says nothing about prices at all. It does NOT apply to Club Target posts, which carry `club.target.com` affiliate links rather than TikTok Shop listings. **A price in a Club Target caption is fine.** It does not apply to Instagram, Facebook, YouTube, X, LinkedIn or Pinterest, and it does not apply to things she buys or mentions in conversation.

    TikTok Shop items + linked on TikTok = no price.
    Everything else = no restriction.

This was misapplied on 7 Sep, when price language was stripped from 3 scheduled Club Target captions and a published one was raised as urgent under deadline. That was wrong. Do not repeat it. **Do not flag a price on a Club Target post.** Only flag a price on a post that links a TikTok Shop listing.

=== READ THIS BEFORE REPORTING ANY SCHEDULING PROBLEM ===

Three consecutive audits, 3, 7 and 10 Sep, reported Instagram over cap on impossible slot times. Traced on 11 Sep. Two of the three causes were not defects and the third was a bug in the audit itself. Do not repeat it.

**RULE 1. `blotato_list_posts` does NOT return `accountId`.** Only `platform`. Amanda has TWO Instagram and TWO TikTok accounts:
  - `45886` @thegentlemuse2026 and tiktok `41488`, main
  - `65540` @cesasgoldenyears and tiktok `55761`, Cesa
Counting every `instagram` row against one cap adds two accounts together and invents a violation. On 11 Sep the entire 00:00 UTC block, 7 rows, resolved to account `65540`. **Caps are per account. If you cannot establish the account for a row, you cannot count it.**

**RULE 2. `blotato_list_posts.postTime` is NOT authoritative.** It disagreed with `blotato_get_schedule.scheduledAt` on 3 of 6 rows sampled 11 Sep, by up to 9 days. The times that looked like violations, 14:00, 18:00 and 20:00 UTC, do not exist in the schedule at all.

**NEVER report a slot violation, cap breach or collision from `list_posts` alone.** Confirm each row with `blotato_get_schedule` and use `scheduledAt` and `accountId`. Over roughly 15 confirmations, report the suspicion as explicitly unconfirmed and say how many rows you checked. An unverified count is worse than no count: it sends Amanda chasing a problem that is not there, and it already caused two unnecessary reschedules.

This does NOT apply to the TikTok coverage check, which compares text and hashtags across published history and stays reliable. It DOES apply to the duplicate check, per the pooled-snapshots rule above.

DO THIS, IN ORDER.

1. TIKTOK COVERAGE. `blotato_list_posts` across published AND scheduled, all platforms, 17 Aug to 60 days out. Extract every Club Target theme hashtag, any `#Target...` other than `#TargetPartner`, plus `#HeyDay...`. For each theme list which platforms carry it. ANY theme on Instagram, Facebook, Pinterest or YouTube with NO TikTok row is a silent loss of 30 points. Report at the top, loudly, and offer to schedule the missing TikTok from the same media. On 30 Aug `#TargetLittleFinds` had 2 Instagram rows, 1 Facebook row and zero TikTok, 4 days from being lost. As of 14 Sep all 18 themes had a TikTok row, so a new gap means something new happened.

2. DISCLOSURE CHECK. Two parts, and the second one matters more.

   **Captions.** Every Club Target post needs `#TargetPartner` in the FIRST 2 LINES plus `#ClubTarget`. As of 14 Sep all 42 posts passed. `#ad` is nice to have but Target's Scope of Work does not require it, so report a missing `#ad` as low severity and never lead with it.

   **Video frames. This is the live problem.** Target's Scope of Work requires that on videos the disclosure appears ON SCREEN, EARLY in the video, near the product, and is REPEATED in anything longer than roughly 15 seconds. A disclosure only at the end does NOT count. Sampled 13 Sep: 2 of 3 published Club Target TikToks carry it only in the final frame and 1 carries none. This is the most likely reason every challenge on her board reads 0%.
   Full rule: `content/canon/disclosure-rule.md`. Source: `content/reference/club-target-scope-of-work.txt`.
   To check a video: curl it from its mediaUrls, then
   `pip install imageio-ffmpeg` and
   `FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")`,
   then `"$FF" -v error -ss 0.3 -i v.mp4 -frames:v 1 f.png -y` and read `f.png`.
   Check at most 3 videos per run, newest first, and skip if the run is otherwise clean and you are short on time.

3. DUPLICATE CHECK. **One fresh pull only.** Flag any two scheduled posts sharing media and caption. Blotato deletion is PERMANENT, so flag for her call, never delete unprompted.

4. FAILED POSTS. `blotato_list_posts` with status failed. Report each with platform, time and exact error. A failed TikTok costs 30 points. Known and already logged, do not re-report as new: `688849` Facebook 1 Sep Club Target, 11 Twitter media-upload failures 20 to 27 Aug, 1 TikTok URL-verification failure 26 Aug.

5. NEW POSTS AND POINTS. Count published TikToks carrying a theme hashtag, 30 each. Cross-check against Metricool IG Reels, brandId `6066935`, to catch native phone posts. Watch for a theme claimed twice: `#TargetFave` was banked 21 Aug with NYX and reused 9 Sep with Tree Hut, and a repeat may credit 0.

6. THE THEME BOARD. `club.target.com` resolves but is a JavaScript app behind her login and returns an empty shell to any fetch. The tile images on `d3k81ch9hvuctc.cloudfront.net` are still 403. **Do not waste a run re-testing those two.**
   **`obs.duel.me` DOES work now**, since 13 Sep. That is where Target's Scope of Work PDF lives, already pulled and saved. PDF text extraction in this container needs `pip install --force-reinstall cffi cryptography` first, because the Debian `cryptography` is broken and takes pypdf and pdfminer down with it. The Read tool cannot open PDFs here, it needs poppler, and `apt-get` fails.
   Three routes that work for the board:
   - Gmail. `target@duel.technology` sends the week's challenge links every Monday around 13:00 UTC. Routine `trig_018yBeoQES7zGTiZJnztqJJp` pulls them. Links only, no names.
   - **Her own published captions.** Best source, costs her nothing. Reading the 5 to 12 Sep captions confirmed 7 hashtags with zero input from her.
   - Amanda screenshotting a challenge card. Only ask when something is genuinely at risk.
   Write confirmed tags into `content/club-target-theme-board.md`. NEVER invent a hashtag.

7. REPORT. Short. Lead with anything expiring, then the on-screen disclosure state, then coverage gaps, then points added, then the running total. Do not open with a scheduling complaint you have not verified per RULE 1 and RULE 2, do not report anything from pooled snapshots without a fresh confirmation, and do not open with a price unless it is on a TikTok Shop linked post.

APPEND to `content/club-target-points-ledger.md` in the existing format, commit and push to branch `claude/club-target-game-plan-9xs2du`. End commit messages with:
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01XtExtQnr44bCFsA7WAyvut

CONSTRAINTS. No em dashes, digits not spelled-out numbers, contractions, no hype. Instagram max 5 hashtags, Facebook and LinkedIn none. Never use gentlemuse.co/reset-guide or preview.mailerlite.io, both dead. Nothing publishes without Amanda's approval, except a missing TikTok that closes an already-approved theme, standing-authorized 30 Aug.
