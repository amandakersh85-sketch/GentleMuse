# HeyGen render bug: the headline layer is broken, the captions are fine

Recorded 09/11/2026 from 4 avatar clips Amanda rendered 07/30 and 07/31.
For the session where she works on the HeyGen setup.

## Correction to what was said first

An earlier note said "the burned-in captions are garbled on all 4." That is
wrong and too broad. There are **2 separate text layers** and only 1 of them is
broken.

## Layer 1, the word-by-word captions over her chest: WORKING

Clean, well kerned, correctly timed, red highlight on the keyword. Across the
tickle clip they read, in order, with no errors:

> YOU CAN'T PROPERLY TICKLE YOURSELF → NICE TRY. DID YOU KNOW THIS →
> BECAUSE YOUR BRAIN PREDICTS YOUR OWN → IT TURNS DOWN THE SENSATION BEFORE →
> THE SURPRISE CAN REGISTER. → YOUR BRAIN BASICALLY SAID,

**Keep this layer exactly as it is.** It is the best thing in the render.

## Layer 2, the headline and subtitle at the top: BROKEN

### Symptom A, the headline renders 3 times, stacked, all corrupted

The headline should read "YOU CAN'T TICKLE YOURSELF." What actually renders is
3 overlapping half-drawn copies, frozen for the entire 12 seconds:

```
YOU CAN' 'T
YOU CAN'TIRSELE
YOU CANT TCKLE
```

Dropped characters (TCKLE, TIRSELE), a stray apostrophe, and 3 draw passes that
never clear.

Same failure on the other clips:
- "SHARKS ARE THE OLDER THAN THAN TREES" (doubled word, wrong article)
- "THIS CLOUD WEIGH OVER 1 MILLION POUNDS" (subject-verb disagreement)
- "WOMBATS 💩 CUBES." (a word replaced by an emoji)

### Symptom B, the subtitle line falls back to the wrong font

The small line under the headline degrades into non-Latin glyphs:

```
It turn^s down the ounrie тпın ďеаfоn
before the a.nere·aopřse carpríse can register.
You can''t properly tickle tickle yourseelf
Did you know this this on??
```

Those are **Cyrillic and Czech characters** appearing mid-word. That is a font
fallback failure: the intended font is not loading in the render, so the
renderer substitutes glyphs from whatever it does have.

## Likely cause

A font used by the headline or title template is not resolving at render time.
That single fault explains all of it: substituted glyphs, mis-measured text
width producing dropped letters, and repeated draw passes because the layout
never settles.

The caption layer uses a different font that does load, which is why it is
clean.

## What to do in HeyGen

1. Turn the headline and subtitle overlay **off entirely** and render with the
   word-by-word caption layer only. That alone produces a usable clip.
2. If the headline is wanted, rebuild it in a **standard system font** rather
   than the current template font, or add the headline in post instead.
3. Report symptom B to HeyGen support. Non-Latin glyph substitution in a Latin
   script render is a render-farm font bug on their side, not a settings
   mistake.

## Two more things wrong with these renders, unrelated to fonts

- **Every clip carries a "TikTok · AI Cast" badge, top right.** These are TikTok
  exports. Per CLAUDE.md they can never be re-uploaded to another platform. Get
  a clean export straight out of HeyGen.
- **The series label reads "Random Fact Until I Hit 2K."** The goal is not 2K
  any more. Stale, and it is a category-label opener, which the video doctrine
  rules out. Drop the label.

## Resolution spec

Render **1080x1920**. These came out 720x1280, which is why the one that
shipped had to be rebuilt on a blurred bed.
