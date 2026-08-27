# COWORK HANDOFF: get the Cesa guide deliverable live

Amanda has ALREADY put `cesa-guide.subscribepage.io` in the TikTok bio for
@cesasgoldenyears. People may be clicking it right now. Treat this as live.

Work in this order. Stop and tell her after step 1 if it is already fine.

## STEP 1, MOST URGENT. Does the bio link even resolve?

Open https://cesa-guide.subscribepage.io in a browser.

- If it 404s, the bio link is dead right now. Build the page, step 2.
- If it loads, skip to step 3.

## STEP 2. Build the landing page. All copy is already written.

MailerLite > Sites > Landing pages > Create.

Every word to paste is in Google Doc **BUILD_0826_cesa-landing-page-paste-kit**,
id `1LgdWJ6qDEUkYu_P16WDJz46Jl1HYosqSVRwmo5dYSmU`, SECTION A. Do not rewrite it.

Settings that matter:
- Slug: `cesa-guide` so the URL matches the bio link she already posted.
- Point the signup at the EXISTING group **Cesa**, id `196024300390581479`.
  Do NOT create a new group. The delivery automation triggers off that exact id.
- **Turn DOUBLE OPT-IN OFF.** Cold TikTok traffic will not leave the app to
  confirm an email. This is where most signups die.
- Publish.

## STEP 2b. The hero photo. Amanda has picked it.

The photo is the one of Cesa on her back in the cream sherpa blanket, blue
paw print fleece on the left, tongue out, both front paws up, looking straight
at the camera. Amanda sent it in chat on 27 Aug and said "I love this one".
It is on her phone or in her camera roll, not yet in Drive.

Ask her to drop it in Drive, or pull it from her camera roll, then:

- **Landing page hero.** The original is portrait, roughly 3:4. Do NOT stretch
  it into a wide banner, that decapitates her. Crop to a **square, 1:1**,
  centered on her face and chest, so her ears stay inside the frame and the
  blanket fills the corners. Export around 1200x1200. Place it above the
  headline, not behind text, the photo is busy and text on top of it will not
  read.
- **PDF cover.** Keep it portrait, uncropped. Set the width to about 55% of
  the page and center it under the title. Do not full bleed it.
- Alt text: `Cesa, a 19 year old chihuahua, lying on her back in a blanket
  with her tongue out.`

Do not filter it, do not run it through an AI upscaler, do not "enhance" it.
She picked this frame because it is really her.

## STEP 3. Host the PDF and get a public link.

The finished PDF is in GitHub, repo `amandakersh85-sketch/GentleMuse`, branch
`claude/club-target-game-plan-9xs2du`, at
`content/guides/19-years-old-10-of-them-mine.pdf` (8 pages). Amanda also has it
downloaded from chat.

Upload it to Google Drive, then Share > **Anyone with the link** > Viewer, and
copy the link. Confirm it opens in a private window before trusting it.

## STEP 4. Point the delivery email at that link.

MailerLite automation **Cesa Guide Delivery: 19 Years Old, 10 of Them Mine**,
id `196289160620803395`. It is enabled and correctly wired already.

In email 1, "Her guide is here" (`196289524674856662`):
- Set the **Read her guide** button URL to the Drive link from step 3.
  Right now nobody can verify where it points, and the guide it promised did not
  exist until today.
- Fix the page count. The email says "13 pages of what actually keeps her
  comfortable". The real PDF is **8 pages**. Change 13 to 8.

## STEP 5. Test it end to end, with a real address.

Sign up through the landing page. Confirm email 1 arrives and the button opens
the PDF. Do not skip this. Nobody has ever completed this path.

## STEP 6. Tidy, only after the above works.

- Old embedded form `196289170922014393` is empty and off. Leave it dead.
- The Cesa DM automations in Blotato (ids 2952 and 2954, account 65540) use an
  email gate, not a link. Once the landing page is live, consider adding the URL
  as a button so people can self serve instead of typing an email into a DM.

## Context you need

- **What the guide is.** 8 pages, "19 Years Old, 10 of Them Mine", written today
  and approved by Amanda. Source is `content/guides/19-years-old-10-of-them-mine.md`
  in the repo. It never gives veterinary advice, by design. Do not add any.
- **Cesa's facts**, so nothing contradicts the guide: Princesa, chihuahua, 19.
  Amanda met her 2015, adoption finalized 2016 after her 3rd litter at age 9.
  Pyometra and spay 2022 at 15, cancer found and removed in that same surgery.
  Dentals 2020, 2021, 2024.
- **Voice rules.** No em dashes. Digits, not spelled out numbers. Contractions.
  Warm, grounded, plain. No hype. Instagram max 5 hashtags. Never state a price,
  there is an open TikTok Shop violation from 04 Aug 2026 over pricing.
- **Verified links only.** Consider This `https://consider-this.subscribepage.io`,
  AI Guide `https://ai-guide.subscribepage.io`, Press Play
  `https://press-play.subscribepage.io`, Reset Guide `https://payhip.com/b/9FE2U`.
  NEVER use `gentlemuse.co/reset-guide` or `preview.mailerlite.io`, both dead.
- **Do not** add this guide to Payhip. Amanda decided against it, it adds a
  second email step for someone who already gave their address.

## What is already done, do not redo

- The guide is written, corrected by Amanda, and rendered to PDF.
- The delivery automation is enabled and correctly triggered by the Cesa group.
- Email 1 and the 4 day follow up "Walk the house at her height" both exist.
- The newsletter signup form `195832725497709843` was rewired on 27 Aug from the
  wrong group to Consider This + Just Another Tuesday. It is still `active:false`
  and needs a manual toggle in the dashboard. Separate job from this one.

## Report back

Tell Amanda: whether the bio link resolved, the public PDF URL, that the button
now points at it, and the result of the step 5 test.
