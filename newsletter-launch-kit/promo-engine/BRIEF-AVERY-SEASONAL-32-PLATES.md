# Brief to Avery: 32 seasonal plates

**From:** Claude, on Amanda's instruction, 2026-09-10
**Deliverable:** 32 still images, 1 per night, 2026-09-19 through 2026-10-30
**Captions:** already written and graded. `newsletter-launch-kit/DRAFT_0910_seasonal-33-nights-v1.txt`
**Approval:** Amanda approves the set before anything is scheduled. Do not schedule. Do not post.

---

## 0. Read this part before generating anything

Amanda's whole reason for routing this to you is cost. Her Blotato balance is 2,974 credits and
the existing seasonal run burned **146 separate renders on 117 posts**, because every cross-post
got its own file. That is the mistake this brief exists to not repeat.

**1 image per fact. Not 1 per post.** The same file goes to Instagram, TikTok, Facebook and
YouTube. Only Pinterest gets a second crop, and only because the shape genuinely differs.

So: **32 primary images. 32 Pinterest crops. 64 files total, and not 1 more.**

---

## 1. The visual system, fixed for all 32

These 32 run on consecutive nights against a queue that already has 8 nights of her avatar on
video. The still plates cannot look like 32 unrelated stock images or the run reads as broken.
They are a **series**. Treat them as numbered plates from a single almanac.

### Style
Hand-inked engraving, in the manner of a 19th century natural history or almanac plate.
Visible line work and cross-hatching. Flat printing, no photographic depth of field, no 3D
render, no glossy digital lighting, no lens flare, no bokeh.

### Palette, exact, every plate
| Role | Hex | Use |
|---|---|---|
| Ground | `#F2EBDD` | aged bone paper, the full background |
| Ink | `#1B1830` | deep aubergine-black, all line work |
| Ember | `#C2552B` | burnt amber, ONE element per plate, never more |
| Moss | `#4F7A5C` | muted green, secondary, optional |

4 colors. No others. No gradients except the paper's own subtle age mottling. If a plate needs a
5th color it is the wrong composition, fix the composition.

### Composition, every plate
- **1 subject, centered**, occupying roughly the middle 60% of the frame.
- A **thin single ruled border** inset 6% from every edge, in Ink, 2px at 1080 wide.
- Generous empty paper between the subject and the border. Do not fill the frame.
- Bottom-left, inside the border: a small plate number in Roman numerals, Ink, tiny.
  Plate I through Plate XXXII.
- **NO OTHER TEXT ANYWHERE IN THE IMAGE.** No titles, no captions, no labels, no dates, no
  signage lettering, no book spines with readable words. Image models mangle text and the
  caption already carries every word. If the subject would naturally have writing on it, draw it
  as illegible marks.

### Sizes
- **Primary: 1080 x 1350 (4:5).** This is the file that goes to IG, TikTok, FB, YouTube.
- **Pinterest: 1080 x 1920 (9:16).** Same artwork, recomposed, not stretched or letterboxed.
  Regenerate at the new ratio rather than cropping.

### File naming, exact
`seasonal-plate-NN-slug-4x5.png` and `seasonal-plate-NN-slug-9x16.png`
NN is zero-padded 01 to 32. Slug is the one given in the table below. No other naming.

---

## 2. How to run it: one at a time, checked, then the next

Do not batch all 32 and hand back a folder. The failure mode with a 32-image series is drift:
plate 1 and plate 32 stop looking related and nobody notices until they are all done.

**Generate plate 01. Stop. Check it against section 3. Fix it until it passes.**
**That approved plate 01 is now the reference for the whole series.**

Then, for plates 02 through 32, one at a time:
1. Generate at 4:5.
2. Run the section 3 checklist against it, **side by side with plate 01**, not alone.
3. If it fails any line, regenerate that plate. Do not proceed with a failing plate.
4. When it passes, generate the 9:16.
5. Move to the next.

After every 8th plate, lay 01 through that plate out together and look at them as a row. Drift
shows up in a row and hides in a single image. If the row has broken, say so and stop rather
than finishing 32 plates that do not match.

---

## 3. Checklist. A plate ships only if every line is yes.

1. Background is `#F2EBDD` bone paper, edge to edge.
2. Exactly 4 colors present, and they are the 4 above.
3. Ember `#C2552B` appears on exactly 1 element.
4. Thin ruled border present, inset, unbroken, Ink.
5. Roman numeral plate number, bottom-left, inside the border, small.
6. **Zero readable words anywhere in the image.**
7. Line-work engraving style, not photographic, not 3D, not painterly.
8. 1 clear subject, centered, with real empty paper around it.
9. Placed next to plate 01, it reads as the same hand and the same book.
10. Nothing gruesome. Bones, graves and masks are fine as period illustration. No gore, no blood,
    no corpses, no distressed human faces. This runs on Amanda's brand, and several plates cover
    real deaths of real named people.

---

## 4. The 32 plates

Prompt each one as: *the style block from section 1*, then the subject line below.

| # | Slug | Subject to draw |
|---|---|---|
| 01 | `soul-cakes` | A stack of small round spiced cakes on a pewter plate, a heavy wooden door standing ajar behind it. Ember on the cakes. |
| 02 | `apple-bobbing` | A wooden tub of water with apples floating, 1 apple lifted slightly, faint scratch marks on its skin. Ember on the lifted apple. |
| 03 | `beggars-night` | A porch lamp lit above a doorstep, a small folded paper slip on the step, empty street beyond. Ember in the lamp. |
| 04 | `crowd-control` | A tipped garden gate and an overturned wooden crate on a 1930s residential street, nobody present. Ember on the gate. |
| 05 | `danse-macabre` | A procession in profile: a crowned figure, a robed figure, a farmer and a child, walking in a line with skeletal figures between them. Ember on the crown. |
| 06 | `plague-mask` | A beaked plague doctor mask resting face-up on a table, dried lavender and a small glass vial beside it. Ember on the lavender. |
| 07 | `mercy-brown` | A winter graveyard at night, bare trees, a single lantern set on the ground beside an upright shovel. Ember in the lantern flame. |
| 08 | `saved-by-the-bell` | Two bells side by side on a plain surface: a boxing ring bell and a small graveside handbell on a cord. Ember on the boxing bell. |
| 09 | `stoker-library` | A library reading desk with an open book, a folded map, and a brass lamp. No readable text on the pages. Ember in the lamp. |
| 10 | `nosferatu` | A film reel lying flat with a length of film unspooling, and a wax seal stamped on a folded document beneath it. Ember on the wax seal. |
| 11 | `lugosi-cape` | Two capes hanging on a coat hook, one visibly heavier and lined, one thin and light. Ember on the lining of the heavy one. |
| 12 | `no-name` | An empty engraved nameplate on a plain wooden frame, the plate blank and unmarked. Ember on the frame corner. |
| 13 | `pentagram-1941` | A manual typewriter on a desk with a sheet of paper in the carriage, a 5 pointed star drawn on the page. Ember on the star. |
| 14 | `bats-see` | A single bat in flight, wings extended, thin concentric arcs radiating from its head. Ember on the arcs. |
| 15 | `black-cat` | A black cat sitting calmly behind the bars of a shelter kennel, facing out. Ember on a small tag hanging on the kennel door. |
| 16 | `ouija-patent` | A planchette resting on a flat board, drawn as a patent office technical illustration with fine measurement lines. No letters or numbers on the board. Ember on the planchette. |
| 17 | `chicken-feed` | A metal feed scoop tipped on its side with kernels spilling from it, the kernels tri-banded like candy corn. Ember on the spilled kernels. |
| 18 | `harvest-latte` | A plain paper cup with no branding, beside a cinnamon stick, a nutmeg and a star anise. Ember on the spices. |
| 19 | `dead-retail` | The exterior of a large empty big-box store at dusk, sign board blank, parking lot vacant. Ember in one lit window. |
| 20 | `poe-clothes` | A straw hat and an ill-fitting coat left on a set of stone steps on an empty street. Ember on the hatband. |
| 21 | `hessian` | A cavalry helmet resting on the ground beside a single cannonball, tall grass around them. Ember on the helmet plume. |
| 22 | `monster-mash` | A 45 rpm vinyl record on a turntable with the tonearm lifted away from it. Blank label, no text. Ember on the tonearm. |
| 23 | `public-domain` | A film canister open on a table, the lid set aside, a printed slip in the lid deliberately blank. Ember on the canister rim. |
| 24 | `chocolate-syrup` | A shower drain seen from directly above, a dark liquid spiralling into it, tile around it. Ember nowhere near the drain, on a single tile instead. |
| 25 | `real-skeletons` | An empty backyard swimming pool at night, rain falling, a ladder at one end. Ember on the ladder rail. |
| 26 | `ambulances` | A cinema marquee at night with a plain blank board, an ambulance parked at the kerb below it. Ember on the ambulance lamp. |
| 27 | `over-wine` | A table with 2 empty wine bottles, 2 glasses, and a stack of loose legal papers. No readable writing. Ember on the wine glasses. |
| 28 | `listed-dead` | A wooden utility pole with several weathered paper notices stapled to it, all of them blank. Ember on one notice's corner. |
| 29 | `three-hundred-k` | A film clapperboard lying closed on bare ground, slate blank. Ember on the clapper stripe. |
| 30 | `two-dollar-mask` | A plain featureless white face mask on a shop counter, a small blank price tag tied to it with string. Ember on the string. |
| 31 | `no-full-moon` | A lunar phase chart drawn as a row of moons across the plate, 1 of them ringed. Ember on the ring. |
| 32 | `dia-de-muertos` | A small home altar with marigolds, 2 lit candles and a framed photograph turned away from the viewer. Ember on the marigolds. |

---

## 5. Hand back

- The 64 files, named per section 1.
- The row-check images from after plates 8, 16, 24, 32.
- A 1 line note on any plate you had to regenerate more than twice, and why.

**Then stop.** Amanda reviews the set. Claude wires them to the captions and schedules only after
she says go. Nothing goes into Blotato from your side.

---

## Handoff protocol — how to answer this

Same as `CONFERENCE-BRIEF-AVERY.md`. **Write your answers directly into this file and commit
them.** There is no live channel between us; this repo is the channel.

Amanda approved this brief on 2026-09-10. It is not a proposal, it is a work order. But if any
part of it is wrong, unbuildable, or you can see a better way, say so here BEFORE generating,
under a heading `## Avery's response`. Amanda decides, not me.

Specifically, answer these:
1. Can you hit this spec with the tools you have? If not, which requirement breaks first?
2. Roughly how long, and does anything here cost Amanda money? She is watching spend closely.
3. Anything in the checklist you think is wrong or will produce a worse result.

If it is all fine, write `## Avery's response` / `Accepted, starting.` and begin.

**Do not upload anything to Blotato. Do not schedule. Do not post.** Hand the files back, Amanda
approves, Claude wires them to the captions.
