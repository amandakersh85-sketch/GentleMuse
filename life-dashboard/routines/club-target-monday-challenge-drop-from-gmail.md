# Club Target: Monday challenge drop from Gmail

- id: trig_018yBeoQES7zGTiZJnztqJJp
- cron (UTC): 40 13 * * 1
- enabled: True
- bound session: session_01XtExtQnr44bCFsA7WAyvut
- connectors: none
- model: default

## Prompt

Pull Amanda's Club Target challenge drop out of Gmail. It lands every Monday around 13:00 UTC, 8 AM Central, from `target@duel.technology`.

WHAT CHANGED 14 SEP 2026. The egress policy loosened. **The tile image CDN `d3k81ch9hvuctc.cloudfront.net` now returns 200**, and so does `obs.duel.me`. That means you can read the challenge NAMES yourself, out of the email, with zero input from Amanda. This used to be impossible and the old version of this routine told you not to try. Try.

Only `club.target.com` is still unreadable, and not because of the network: it resolves fine and is a JavaScript app behind her login that serves an empty shell to any non-browser client. Do not re-test that one.

DO THIS.

1. `mcp__Gmail__search_threads` for `from:duel.technology newer_than:8d`. Take the newest message whose body contains "New Challenges".

2. Read it with `messageFormat: PLAIN_TEXT`. Extract every distinct `https://club.target.com/t/XXXX` link in order, de-duplicated. Normally 4 a week. Note the subject line, it names the seasonal theme.

3. NOW GET THE NAMES. Read the same thread with `messageFormat: FULL_CONTENT`. The result is too large to read inline and gets saved to a file: parse it with python3, do not Read it raw.
   - Pull `htmlBody`, regex every `cloudfront\.net/company/SmsXRV/images/([0-9a-f-]+)\.png`, keep first-seen order.
   - `curl` each to a file. Check dimensions with
     `python3 -c "import struct;d=open(F,'rb').read();print(struct.unpack('>II',d[16:24]))"`.
   - **The challenge tiles are the square-ish ones**, roughly 521x542 in a 3-challenge week and 521x530 in a 4-challenge week. Skip 223x73 buttons, 561x249 banners, 448x85 headers, and anything 1201 wide (that is the monthly creator spotlight).
   - Read the tile PNGs. Each carries the challenge name, a one-line brief, the eligible platforms and the tier gate.
   - **Tile order matches challenge-link order in the plaintext body.**

4. The tiles do NOT carry the hashtag or the closing date. Those only exist on the challenge card in the portal. **Never invent a hashtag.** A wrong hashtag credits 0 and the post still carries a paid partnership disclosure. So ask Amanda for the tag only, not the name, and tell her which challenge each link is so she knows what she is tapping.

5. Post to Amanda: the subject line as header, then one line per challenge with its NAME and its link. Ask her to tap each, screenshot the card, and paste. Say plainly that you only need the hashtag and the closing date now. Keep it short, she reads it on her phone before work.

6. Write names, briefs, links and the date into `content/club-target-theme-board.md` under a dated heading, hashtag marked `unknown`. When she sends screenshots, fill in the exact hashtag and closing date, then re-sort the whole board by closing date, soonest first.

7. Flag any brief that conflicts with how Amanda actually works, because a wrong reading wastes a store run. Two live examples:
   - **Game Day Lineup** (7 Sep, `t/0pdm`) reads "turn your tailgate must-haves into a packing checklist" and the tile shows an Igloo cooler, a handheld fan and Olipop. It is gear and drinks, NOT apparel. Amanda shot sportswear on 12 Sep, which is the wrong read.
   - **The Fall Outfit Edit** (14 Sep, `t/0pp9`) asks for a GRWM. Amanda is never on camera, so the standard reading does not fit her. A rack-to-cart or layering flat-lay is the substitute, and it is worth confirming with her.

8. Once the board has real hashtags and dates, build the batch run sheet in `content/club-target-game-plan.md`: every open challenge in closing-date order, one line each with the product to film and the exact caption tags, so one store run covers the most challenges.

KNOWN CADENCE. 4 new challenges most weeks, every Monday. Codes do not repeat week to week apart from a rotating evergreen slot: `txd` in August, `tt7` as of 14 Sep, explicitly monthly and repeatable. Challenges accumulate, which is why a batched store run every 2 to 3 weeks beats a weekly trip.

POINTS REALITY. No Club Target credit on Instagram below 500 followers, confirmed by Amanda 30 Aug. TikTok is 30 points and is the only placement that pays. A theme is worth 30, not 75. Do not put Instagram Stories on her task list.

THE PRICING RULE, CORRECTLY SCOPED. She cannot state prices for TikTok Shop items she links on TikTok. That is the whole rule. It is NOT a Target rule, Target's own Scope of Work says nothing about prices, and a price in a Club Target caption is fine. Do not flag one. See `content/canon/pricing-rule.md`.

ON-SCREEN DISCLOSURE. Target requires `#TargetPartner` on screen EARLY in any video, near the product, repeated in anything over roughly 15 seconds. An end-card-only disclosure does not count and is the likely reason her board reads 0%. See `content/canon/disclosure-rule.md`.

CONSTRAINTS. No em dashes, digits not spelled out numbers, contractions, no hype. Commit and push any file changes to branch `claude/club-target-game-plan-9xs2du`.
