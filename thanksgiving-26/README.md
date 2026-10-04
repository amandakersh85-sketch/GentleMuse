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
| `period-bare` | 1 plucked string, sparse | anything pre 1700 |
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

## Before this ships

1. **The sources are listed, not checked.** Every row carries `verified: no` and
   a `sources` line naming what to go and read. 16 are marked high confidence
   and 10 medium. The medium ones are where the popular version of the story and
   the documented one may not match: the cranberry bounce board, the parade
   balloon release, the wishbone, the 1876 football fixture, the turkey pardon,
   the Pilgrim naming, the snood, and the gratitude trials. Those get read
   before they get rendered.
2. **26 images to generate**, 1 per night, from the `plate_desc` lines.
3. **26 beds to source**, by family, not 26 separate hunts.
4. **The bed step still does not exist in any script.** It is prose in
   `beds/README.md` and nothing runs it. The Halloween nights were muxed by
   hand. If that is still true on 11/01 this wave ships silent too.
5. **Live=no, and somebody has to flip it.** `gm_cadence_check.load_target`
   returns the first row with `Live=yes`, so exactly 1 wave can be live at a
   time. Halloween stops on 10/31 and this starts on 11/01, so they never
   overlap, but the handover is a manual edit on 1 day and nothing reminds
   anyone to make it.
