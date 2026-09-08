# HANDOFF — old camera roll to finished posts

Paste everything below the line into Claude Code on the laptop as the first
message. Written 09/08/2026 by the cloud session, which cannot reach the phone,
OneDrive, or the local drive.

---

You are finishing something Amanda Kersh (The Gentle Muse) has been asking for
since June and has not gotten. She has months of footage of herself talking to
camera sitting unedited in her camera roll. It is taking up space on her
devices and none of it has ever shipped. Your job is to turn it into posted
content. Not a plan. Not an inventory. Finished files with captions, ready to
upload.

Read `CLAUDE.md` in the GentleMuse repo first. Every rule in it applies.

## The one thing that matters

**Do not stop to report and wait.** Previous sessions have run a triage, handed
her a table of numbers, and stopped. That is the exact failure. Go all the way
to finished pieces in a folder, then show her those.

She has said, in her own words, "I don't care if it's not great. It doesn't
have to be great. That's the entire point." Believe her. Bad lighting,
bedhead, no makeup, rambling, a false start, a dog barking, all of it ships.
Perfect is the reason none of this has been posted for 3 months.

**Target for the first run: 10 finished pieces.** If you get 10, that is
2 to 3 days of posting across 4 platforms.

## Step 1, find the footage

Look in all of these on Windows:
- `%USERPROFILE%\OneDrive\Pictures\Camera Roll`
- `%USERPROFILE%\Pictures\Camera Roll`
- `%USERPROFILE%\Videos`
- `%USERPROFILE%\Downloads`
- `%USERPROFILE%\OneDrive\Pictures\Saved Pictures`
- Any Google Takeout export folder
- The folder holding `asset_scanner.py`, plus anything the Master Asset Index
  lists under footage

Go back to **June 2026 and earlier**. Do not limit to recent files.

`GM-Video-Triage.ps1` (Run 3 of the 28 run system) exists for the inventory
half of this and has never been run. Use it if it helps, propose-only, but it
is not the deliverable and do not stop when it finishes.

## Step 2, filter to talking-to-camera

The signature you are looking for:
- Portrait or vertical orientation, or square
- Duration 15 seconds or longer
- **Has an audio track with speech in it** (this is the strongest filter, most
  b-roll and pet clips are silent or ambient)
- Shot on a phone, so filenames like `VID_2026...`, `2026-04-08-...`, or a
  plain timestamp

Use ffprobe for orientation, duration, and audio stream presence. Then confirm
speech by transcribing, next step.

**Excluded, never touch:** anything in the private or OF lane, anything the
doc triage flagged HOLD, and `doc-triage-LOCAL-ONLY.csv`. Do not move,
rename, delete, or upload any original. Copy what you use to a working folder
and leave the originals where they are.

## Step 3, transcribe everything that passed

`hyperframes transcribe` handles this locally, or Whisper directly. You need
the words before you can pick a cut, and the transcript is also the source for
the on-screen text and the caption. Save each transcript next to its clip.

## Step 4, pick the cut, do not use the whole file

For each clip, read the transcript and find the strongest continuous 20 to 45
seconds. Rules:

- **Start at the strongest sentence, not at file start.** Almost every phone
  video opens with 3 seconds of her getting settled. Cut that off. The first
  frame is the thumbnail and the hook.
- **No fade from black. Ever.** Open on her mid-sentence, mid-expression, or
  already moving.
- If a clip has 2 good separate thoughts in it, cut 2 pieces from it.
- If a clip has nothing usable, skip it and move on. Do not force one.
- Trailing off at the end is fine, cut on the last real word.

Cut with ffmpeg. Keep the original audio, do not re-encode more than once.

## Step 5, build the piece

Use the skills, they exist for exactly this:
- **`/talking-head-recut`** for the designed on-screen text: the hook card on
  frame 1, and 2 or 3 text beats through the clip that name what she is
  actually saying. Not decoration, not subtitles. Intelligent text about the
  point she is making.
- **`/embedded-captions`** for the word by word captions underneath.

On-screen text rules:
- Frame 1 carries the hook, in her own words pulled from the transcript, large,
  upper third. It has to make a stranger stop.
- Text sits in the upper or lower third, off her face.
- Something moves or changes by second 2.
- No category labels. No "storytime." No "random fact of the day."

If a clip's audio is unusable but the video is good, it becomes a
text-on-screen piece instead: her on camera, the point told in designed text,
Meta trending audio underneath. Still ships.

## Step 6, caption and CTA per platform

Write a caption per platform for every piece. Run all of them through
**`/post-grader`, minimum 9 out of 10**, before anything is called finished.

- **Instagram:** 3 to 5 lines, max 5 hashtags, CTA is follow or comment a
  keyword. Reels.
- **TikTok:** shorter and blunter, hook restated in the first line, CTA is
  follow or comment.
- **Facebook:** longest and warmest, no hashtags at all, CTA points to the
  Consider This newsletter when the topic fits.
- **YouTube Shorts:** title line plus 2 sentences, CTA is subscribe.

Hard rule from CLAUDE.md, check it on every single piece: **if she names or
shows a specific product, that product's own link goes in the caption.** Not
the storefront, not link in bio. If a product is named and you cannot find the
link, flag that piece and keep going.

Voice rules: no em dashes, digits not spelled out, contractions, no hype,
never a price on affiliate content.

## Step 7, export and hand off

One folder, `/GM-Ready-To-Post/`, and inside it per piece:
- `NN_slug.mp4`, the finished vertical render, 1080x1920
- `NN_slug.md`, the 4 platform captions and the grader score

Export clean from the render. **Never download a published video from one
platform and re-upload it to another.** Instagram demotes competitor
watermarks and AI badges. Confirmed case: a trivia reel carrying a TikTok AI
Cast badge got 37 views on Instagram while the clean version ran 230 to 577 on
Facebook.

Then show Amanda the folder and the caption list. **That is the first time you
stop.** She approves finished pieces, not plans, and she does not pick clips
for you.

## Also grab these 6 from Google Drive

The cloud session found 6 raw camera files in Drive that have never been
reviewed. Pull them into the same pipeline:

| File | Drive ID | Size |
|---|---|---|
| VID_20260703_134404522.mp4 | 1YHCQk9On9c53HFLXcoQ961EfT3sYuEQ7 | 34 MB |
| 2026-04-08-101630981.mp4 | 1TGWMzRWXD4QiPGwq49-u0Dmi6-e9osnN | 7.9 MB |
| 2026-07-09-010916706.mp4 | 1HdNOf2MIZQrS6Z56kYjeBdCHCRC0o2Uq | 13.9 MB |
| VID_20260409_115349002.mp4 | 13UfvEhgp2t_K5kGsuBSKPUBakR2NNxGo | 12.2 MB |
| lv_7447243289301880069_20260509132226.mp4 | 1LpKqJQQSsbWyxGjtMqHGcAWaMAVaMN9T | 12.9 MB |
| CesaVideo 91320 | 139j9y_xn7YY1kn1AIwjp0daRWSQk9gBx | 250 MB |

The `lv_` file is probably a saved TikTok, so it is blueprint reference, not
her footage. The 2020 Cesa file is a Cesa's Golden Years asset, not a talking
head, but it is 250 MB of a much younger Cesa and worth a look.

Everything else in that Drive is the June HeyGen avatar library. **Those do
not ship.** Their scripts are reusable, the avatar videos are not.

## Do not

- Do not stop after the inventory
- Do not ask her which clips to use, pick them
- Do not discard a clip for lighting, appearance, or rambling
- Do not open a fade from black
- Do not delete, move, or rename an original file
- Do not touch the private lane or any HOLD file
- Do not schedule or publish anything, she approves first
- Do not rebuild the existing system, read it before you touch it
