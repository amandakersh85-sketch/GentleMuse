# Halloween 33 Nights

1 true fact every night, Sep 29 to Oct 31, plus the trailer on Sep 28.
Approved plan: https://claude.ai/artifact/FwBepNEF5t6sovQi3z16t9

## How it runs

- `approval/plan.json` is the approved order: which fact on which night, and its background.
- `weeks/beats.json` is the on-screen text. `weeks/build_week.py N` turns a week into
  reel payloads and captions (`weekN-reels.json`, `weekN-posts.json`).
- Reels render in the reel factory (holiday branch) with the music bed, then upload to
  Blotato. `weeks/media.json` maps each render to its Blotato URL.
- `make_schedule.py` builds `schedule.json`: every post, its time, and the old Halloween
  repeats it replaces. Rebuild it after media.json changes.
- `load.py` loads 7 days ahead. The GitHub job `Halloween 33 Nights` runs it daily at
  7 AM Central, so the countdown fits the 200-post queue as room opens. It removes the
  old repeat on a date only when that night's new post goes in. Every removed post is in
  `backup/queue-2026-09-23-full.json`.
- Times: Instagram and TikTok 6:00 PM Central nightly, Facebook and YouTube 6:30 PM on
  odd nights. Samhain moves to 6:00 PM Oct 31. "Samhain is 5 nights out" moves to
  7:30 PM Oct 26.
- To stop it: set the repository variable `HALLOWEEN_33_OFF` to `true`.

Tests: `python3 halloween-33/tests/test_load.py`
