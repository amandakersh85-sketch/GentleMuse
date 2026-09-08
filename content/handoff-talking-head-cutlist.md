# Handoff — talking-head cut list spec (for the laptop session)

Written 09/08/2026 by the cloud session. Amanda confirmed the laptop session
owns this: it can reach her camera roll and local archive, this session cannot.

## The job

Pull Amanda's face-to-camera clips out of the local footage archive and cut
them into drafts for her approval. She is not re-recording yet, so this works
with what already exists.

## Why this matters, from the data

Amanda's face-to-camera posts hold attention better than almost anything on
the account. Her 2 highest watch times are both her talking:
- "The glow up is not always a new body" 11.0 seconds
- "I let the AI post before I checked it" 10.6 seconds

But those posts only got 132 and 156 views on Instagram. People who find them
stay to the end. That is a distribution problem, not a content problem, and
the lever is the opening frame.

Her single best face-to-camera post is the "women over 40, inappropriate
sound" humor reel: 1,818 views, 8.2 seconds watch, 17 comments. Humor in that
vein is the only Amanda format that competes with Cesa on Instagram. Weight
the cut list toward it.

Facebook is different: her face does much better there without help. My 2
personalities did 941, the car reel 420. Same clip, very different ceilings.
Cut for Instagram, and Facebook takes care of itself.

## Cut rules, non negotiable

1. **No fade from black.** First frame is the thumbnail and the hook. Scan
   the first 3 seconds of every raw clip and start the cut on the strongest
   visual hook frame: motion already happening, her face mid expression, a
   product in hand, or text already on screen.
2. **No category labels in frame 1.** No "Day 57 of 60" as an opener, no
   title cards. The interesting part goes first.
3. Something must change size or position within the first 2 seconds.
4. Captions are an overlay, keep them off her face.
5. Voice rules apply to every caption: no em dashes, digits not spelled out
   numbers, contractions, no hype, Instagram max 5 hashtags.
6. If a video names or shows a specific product, the caption carries that
   product's own link. Club Target format:
   https://club.target.com/s/amanda.20/_/sku/{SKU}

## Process

1. Run GM-Video-Triage.ps1 PROPOSE-ONLY against the footage archive. Never
   pass -Execute without Amanda's explicit approval on that run's list.
2. Report first: how many real face-to-camera clips of Amanda exist locally,
   and the vertical vs horizontal split. That number decides everything else.
3. Classify each clip: face-to-camera talking, Cesa footage, b-roll, other.
4. For every face-to-camera clip, note the timestamp of its strongest visual
   hook frame.
5. Produce a cut list weighted toward humor and self deprecating moments
   first, honest confession second, reflective third.
6. Present the inventory and proposed cuts to Amanda. Nothing renders final
   or schedules without her approval.

## Coordination

- The daily talking-head "yapper" video is this session's job.
- Trivia (HeyGen avatar) and Cesa organic are handled elsewhere.
- Target is 3 to 4 posts per platform per day across Instagram, TikTok,
  Facebook, and YouTube Shorts.
- Full campaign context: content/1k-campaign-plan.md on this branch.
