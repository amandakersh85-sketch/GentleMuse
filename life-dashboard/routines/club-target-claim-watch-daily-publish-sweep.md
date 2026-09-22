# Club Target claim watch — daily publish sweep

- id: trig_01LikHf7zVVJZAxZMe5mLNsj
- cron (UTC): 0 16 * * *
- enabled: True
- bound session: session_01XtExtQnr44bCFsA7WAyvut
- connectors: none
- model: default

## Prompt

CLUB TARGET CLAIM WATCH. Amanda asked for this on 13 Sep 2026: "anytime Blotato posts a scheduled draft of Target, go and claim my points." Each challenge theme is worth 30 points and she has been losing them to posts that publish and then get forgotten.

You cannot claim on club.target.com. It is a JavaScript app behind a login and returns the same empty shell to any non-browser client. Never say you claimed or submitted anything. You detect the publish and hand her the row. She presses the button.

STEP 1. Call blotato_list_posts, since = 36 hours ago, until = now, status ["published","failed"], limit 250. If the result is too large to read inline it gets saved to a file: parse that with python3, do not read it raw. A Club Target row is any post whose text contains "#ClubTarget" or "club.target.com", case insensitive.

STEP 2. For each, pull state.postUrl, the platform, and the challenge theme hashtag.

**THE THEME HASHTAG REGEX. Get this right, a narrow one invents phantom point losses.**
Her theme tags do NOT all start with "Target". Confirmed live examples include `#GameDayWithTarget` and `#HalloweenDecorAtTarget`, which a `#Target\\w+` pattern misses entirely. On 15 Sep that bug reported 2 scheduled rows as having no theme tag when both were correctly tagged.

Use: `#(\\w*[Tt]arget\\w*|HeyDay\\w+)` and then drop `TargetPartner` and `ClubTarget` from the matches. Anything left is the theme tag.

STEP 3. Append new rows to content/club-target-claim-ledger.md on branch claude/club-target-game-plan-9xs2du. Never duplicate a row already there. Commit and push.

STEP 4. Report to Amanda, short. One line each:
  CLAIM: <theme> — <platform> — <url>
Then https://club.target.com

If nothing published, say "No Target posts published" in one line and stop. Do not pad it.

FLAG, these are point losses:
- state.type "failed". It never went live. Name it and the error.
- A row with #ClubTarget and #TargetPartner but genuinely no theme hashtag after applying the WIDE regex above. Name the post id. Known and already logged, do not re-report: `6776722` (IG, 5 Sep) truly has none; `6837551` (TikTok, 7 Sep) carries only `#targetfinds`.
- An empty forward queue. Check the next 21 days with ONE fresh pull. If there are zero Club Target rows scheduled, say so.
- ON-SCREEN DISCLOSURE, see below.

THE ON-SCREEN DISCLOSURE RULE. From Target's own Scope of Work.
On videos `#TargetPartner` must appear ON SCREEN, EARLY, near the product, and repeat in anything over roughly 15 seconds. End-card-only does NOT count. Her captions all pass the first-2-lines rule, but 2 of 3 videos sampled 13 Sep carried it only in the final frame and 1 had none. That is the likely reason her board reads 0%.
Videos built since 14 Sep DO pass: the denim TikTok `7042258` and the fall fits IG `4448610` both carry it from frame one. So the fix is in. Spot check new ones, do not re-check those two.
Full rule: content/canon/disclosure-rule.md.
To check: curl the mediaUrls entry, `pip install imageio-ffmpeg`, `FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")`, then `"$FF" -v error -ss 0.3 -i v.mp4 -frames:v 1 f.png -y` and read f.png. At most 3 videos per run, newest first. Skip if the run is otherwise clean.

HARD RULES
- **Do not assume whether she is on camera.** It varies: talking head through 12 Sep, silent b-roll on 14 Sep, on camera in a fitting room on 15 Sep. Cut and describe what the frames actually contain. See content/canon/filming-method.md. Never flag her own footage as a rule violation because of an older stated preference.
- Instagram earns no Club Target credit until she passes 500 followers. Note IG rows, mark "no credit yet."
- THE PRICING RULE, CORRECTLY SCOPED: she cannot state prices for TikTok Shop items she links on TikTok. That is the whole rule. It is not a Target rule, the Scope of Work says nothing about prices, and a price or a percent off in a Club Target caption is fine. Do not flag it. See content/canon/pricing-rule.md.
- POOLED SNAPSHOTS ARE NOT STATE. Saved list_posts files accumulate across runs. Any "what is scheduled right now" question needs ONE fresh pull. Pooling them produced 3 phantom rows and 36 phantom duplicates on 14 Sep.
- blotato_list_posts.postTime is unreliable and has been wrong by up to 9 days. For published rows trust state.postUrl existing.
- Voice: no em dashes, digits not spelled out, contractions, no hype.
- Read only. Do not schedule, edit, or delete any post. The ledger commit is the only write.
