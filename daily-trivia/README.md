# Daily trivia

1 AI, automation or creator economy fact a day, as a HeyGen video of Amanda in
her own voice, on Instagram, Facebook, TikTok and YouTube. Nothing posts until
she merges the pull request it opens. This file is the SOP for the job.
`filing-system/sops/SOP_0909_trivia-pipeline.txt` is the lane it serves.

Free to run: it is 2 GitHub jobs, like the Blotato refill and the Halloween
loader. HeyGen charges its API credits for each video, the same as any HeyGen
render. Chosen 09/28/2026 over n8n, which has no free plan.

## A day, start to finish

1. 7:30 AM Central, the GitHub job `Daily trivia` runs `make.py`.
2. It picks the next fact (`filing-system/scripts/gm_trivia_pick.py`): usable in
   `trivia-fact-bank.csv` on the day, `talking-head`, and never approved or
   declined before.
3. The script is the Fact, then the Backbone, word for word. The 4 captions are
   those 2 lines plus each platform's own ask from `trivia-cta.csv`. No model
   writes anything, so no number can appear that the bank does not hold.
4. Every caption goes through the trivia gate (`gm_trivia_check.py`) and the
   keyword gate (`gm_keyword_check.py`). Any failure stops the day before a
   render is paid for.
5. HeyGen makes the video: 1 of her 2 podcast looks, rotated by day, her voice
   at 0.92, vertical 9:16. The HeyGen CLI does it, the same tool her own
   sessions use.
6. The video is copied to Blotato's storage, because a HeyGen link expires and
   approval can take days.
7. The job opens a pull request labelled `daily-trivia`, with the video link
   and all 4 captions. GitHub emails her.
8. **Merge** approves it. The merge runs `Daily trivia, schedule approved`,
   which puts the 4 posts into the next open daytime slots. **Close** skips it.

## The rules, and why each exists

1. **Nothing posts without the merge.** House rule 4. The job opens a pull
   request and stops.
2. **1 day at a time.** While a trivia pull request is open, the next morning
   makes nothing new. Unreviewed videos would cost HeyGen credit and pile up.
3. **A fact is made once.** A package in `approved/` is the record of an
   approved day. A closed pull request means skip, and that fact is not made
   again. Reuse before generating.
4. **No free topics, no written words.** The lane's rule since 09/09: ai,
   automation or creator, and only rows a person has checked. The design first
   proposed on 09/28 had a model write about a free topic. That is the one
   input this lane refuses.
5. **Every post has a time.** Blotato publishes a post at once if it has none,
   so the scheduler never sends one without a time.
6. **Slots.** 9:30 AM, 12:00 PM, 2:30 PM or 4:00 PM Central: the first that is
   at least an hour away and 2 hours clear of every other post on that
   account, the same spacing as the cadence gate. Today first, then up to 7
   days out. Daytime keeps it clear of the 6 PM Halloween posts.
7. **Room for Halloween.** 10 of the 200 queue slots stay free for the
   countdown's next load. If the queue is fuller than that, nothing from the
   day is scheduled and the run says so. Re-run the job from the Actions tab
   once posts have published and room has opened.
8. **Nothing twice.** A post whose video is already queued, or was published in
   the last 14 days, on that platform is skipped. Re-running is always safe.
9. **All 4 or none.** A day goes in whole, so the platforms stay together.
10. **TikTok labels it as AI.** The video is a HeyGen avatar, so every TikTok
    post carries TikTok's AI-generated label.

## Setting it up, once

1. **The HeyGen key.** Copy the API key from
   https://app.heygen.com/settings?nav=API and add it as a secret named
   `HEYGEN_API_KEY`:
   https://github.com/amandakersh85-sketch/GentleMuse/settings/secrets/actions/new
   The job starts the next morning. Until then it says "Not set up yet" and
   makes nothing. An API key spends HeyGen API credits, which are separate from
   the plan's own credits.
2. **Let the job open pull requests.** At
   https://github.com/amandakersh85-sketch/GentleMuse/settings/actions tick
   "Allow GitHub Actions to create and approve pull requests" under Workflow
   permissions, then Save. If this is off, the first video is still made and
   kept, and running the job again after ticking it opens the pull request
   without making a new one.
3. `BLOTATO_API_KEY` is already a secret. The refill and the Halloween loader
   use it.

To stop it: add the repository variable `DAILY_TRIVIA_OFF` with the value
`true`. To make a particular fact today: run `Daily trivia` from the Actions
tab and type its id.

## Accounts

instagram 45886 · facebook 30840 (page 1086399221215093) · tiktok 41488 ·
youtube 36129. Cesa's accounts never carry this lane.

## Files

    make.py                 the morning job: pick, gate, render, host, package
    schedule.py             the merge job: the approved day into Blotato
    approved/               1 package per approved day, the record
    tests/                  the whole day against a fake HeyGen and a fake Blotato
    ../filing-system/scripts/gm_trivia_pick.py   which fact, and the words
    ../filing-system/data/trivia-cta.csv         each platform's ask

Tests: `python3 daily-trivia/tests/test_daily_trivia.py`. They also run inside
`bash filing-system/tests/run-tests.sh`.
