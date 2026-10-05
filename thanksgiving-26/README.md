# Thanksgiving, 26 nights

11/01 to 11/26, which is Thanksgiving Day itself. 1 fact a night on all 4 main
accounts: Instagram 45886 and TikTok 41488 at 23:00 UTC, Facebook 30840 and
YouTube 36129 at 23:30. Same shape as `halloween-33/` so C13, C14, C15 and C16
read it with no change to any script.

Drafted 10/04. Not announced, so `campaign-targets.csv` has it at `Live=no` and
nothing is scheduled against it.

## What is settled

26 nights, 26 different facts. No reuse. Amanda, 10/04: a new fact every single
night. 11/01 is Dia de los Muertos, which she chose as the handover out of
Halloween, and the run then moves through harvest, the 1621 meal, how the
holiday was actually made, the parade, the food and the day itself.

26 different images, 1 per fact. The same render goes to all 4 accounts. No
per-platform variants and no rotation. Amanda, 10/04: "a stylized version per
day, per fact."

The image is the room the fact happened in. That is the style the Halloween run
set and these follow it: a short specific scene, 1 light source, no people, no
faces, objects doing the work. Halloween was candle and fog. This is lamplight
and wet leaves.

## The sound is picked per fact, which Halloween never did

Halloween shipped 1 track under all 33 nights. Every published night is the
identical 18 seconds, measured 10/04. That was never the design and
`reel-factory/beds/README.md` had said so all along.

Here the sound matches the era of the fact, so it is doing work instead of
sitting there. The `bed` column is the family and `bed_desc` says what it is:

| bed | what it is | used on |
|---|---|---|
| `traditional-solo` | a single guitar, no ensemble | Dia de los Muertos |
| `period-bare` | 1 plucked string, sparse | anything pre 1700, and the 1663 Bible on night 23 |
| `period-piano` | sparse piano, 1860s parlour | the Lincoln nights |
| `period-scratch` | scratchy period recording | 1880s and 1920s |
| `period-brass` | period brass band | 1876 football, the 1924 parade |
| `period-radio` | 1930s radio orchestra, slight hiss | Franksgiving |
| `period-light` | light orchestral | 1955 and 1989 |
| `modern-jazz` | warm jazz piano trio, newly played | the 1973 television night |
| `modern-warm` | warm modern instrumental | the science and nature nights |

`modern-jazz` is newly played, never the original score of anything. A carol
or a tune can be out of copyright while every recording of it is still owned,
and that distinction is the whole reason this column exists rather than a note
saying "find something Christmassy".

## The facts were checked on 10/04, and 4 of them were wrong

Amanda, 10/04: "rewrite 13, 22 and 23 and don't forget to fact check the other
ones." All 26 were read against sources that day. Every row now carries
`verified`, `checked` and a `sources` line that points at something, and
`gm_fact_check.py` refuses a night that does not.

4 rows were wrong, and all 4 said `confidence: high`:

| night | said | is |
|---|---|---|
| 8 | Sarah Hale campaigned 17 years | 36, from 1827. 17 is the letter campaign alone, from 1846 |
| 20 | the name Pilgrims dates to the 1840s | Daniel Webster said it at the 1820 bicentennial |
| 24 | writing down 3 things beats thinking them | the study used 5 items and never compared writing against thinking |
| 26 | a fact | a closing thought, now marked `editorial` |

Confidence is a session's opinion of its own memory, which is the thing that
was already wrong. The 2 rules that came out of this: a fact is not checked
until something says what it was checked against, and a row that is not a
factual claim says so in its own confidence column rather than borrowing the
word high.

3 nights were rewritten because they read flat, which is what Amanda asked for:

- **13** was "wild turkeys fly, and fast". Now they sleep in trees, and the
  bird we eat was bred too heavy to get up there.
- **22** was "trees drop their leaves to avoid dying of thirst". Now leaves do
  not fall, they get pushed, and the tree builds the breaking point in spring.
- **23** was the turkey's snood changing colour. Replaced. It is now Wôpanâak,
  the language spoken at that 1621 harvest, which had no speakers after about
  1833 and is being taught in Wampanoag households again.

2 rows pass by declaration rather than by being confirmed, and the gate lists
both on every run so they cannot quietly multiply:

- **14**, the wishbone, is `partly`. The Etruscan link and alectryomancy are
  well attested for the 8th to 3rd century BCE. The detail about drying the bone
  and stroking it for wishes comes from popular retellings and not from primary
  scholarship, so the caption says roughly 2500 years old and stops.
- **26** is `n/a`. It is a closing thought and not a claim.

## Before this ships

1. **26 images to generate**, 1 per night, from the `plate_desc` lines. Blotato
   `create_visual` at 50 credits each. 2,644 credits in the account on 10/04,
   which covers Thanksgiving and leaves Christmas about 1,000 short.
2. **9 bed files to source**, by family rather than 26 separate hunts. Only
   `eerie-calm` has a file. `reel-factory/bed.mjs` **refuses** a render whose
   family has no file, so every Thanksgiving night fails to build until these
   exist. That is the intended behaviour and it is also the blocker.
3. **Wôpanâak carries diacritics**, and nothing in the render path has been run
   against a non-ASCII caption. Check night 23 renders before it queues. Do not
   fix it by stripping the accents off the name of a language this fact is about
   being reclaimed.
4. **Live=no, and somebody has to flip it.** `gm_cadence_check.load_target`
   returns the first row with `Live=yes`, so exactly 1 wave can be live at a
   time. Halloween stops on 10/31 and this starts on 11/01, so they never
   overlap, but the handover is a manual edit on 1 day and nothing reminds
   anyone to make it.
5. **The Halloween plan was checked on 10/04 too.** It had no `verified` or
   `checked` column at all when the gate first ran. All 28 nights still to come
   have been read against sources now: 5 needed correcting and night 33, the
   finale, rests on a disputed claim. `halloween-33/README.md` has the detail.
