# Beds

## eerie-calm-bed.wav

The bed under every reel in the 2026 spooky season. 63 seconds, 44.1k
stereo PCM.

Generated through HeyGen on 09/04/2026, id `3488ed42a9204b65abd0d84518efbb20`,
described by the catalogue as "eerie-calm ambient, ominous minimalist
drones". It was picked from 3 candidates and it is the one Amanda approved
with "beds in, let it run".

It lives here because it had been living nowhere. The only copies were a
cloud container's scratch directory and a HeyGen S3 link that expires 7
days after it was signed, around 09/11. Losing it does not cost a file, it
costs the season its sound: every reel already shipped carries this exact
track, and a re-resolved "eerie calm ambient" would be a different piece of
music under the ones that come next.

## How it goes under a reel

Voiceover ducks the bed, rather than the bed being mixed quiet and left
there. Each reel takes a different 27 seconds of the track so 5 in a row do
not open identically.

    [vo]amix=inputs=N:normalize=0,apad=whole_dur=DUR,asplit=2[vo1][vo2];
    [bed]atrim=OFF:OFF+DUR,asetpts=PTS-STARTPTS,
         afade=t=in:d=1.2,afade=t=out:st=DUR-1.8:d=1.8,volume=0.32[bedraw];
    [bedraw][vo1]sidechaincompress=threshold=0.02:ratio=10:attack=60:release=500[bed];
    [vo2][bed]amix=inputs=2:normalize=0[out]

Then mux with `-c:v copy -c:a aac -b:a 160k -shortest`. Never re-encode the
video to add audio.

## It is code now, not this file

Until 10/04 the recipe below lived here and nowhere else. Nothing ran it. The
muxing was done by hand, which means it was done once with 1 offset for the
whole Halloween run and then not at all: 6 posts were queued with no audio
track and all 20 published nights carry the identical 18 seconds. Amanda, 10/04:
"it's going out with no sound again."

`bed.mjs` does it now and `build.mjs` calls it on every render. A payload names
a family, `beds.csv` maps the family to a file, and the reel is **refused** if
either is missing. There are 5 ways to end up without music and all 5 stop the
render:

- the payload names no bed
- the family is not in `beds.csv`
- the family has no file yet, and the refusal says what to go and get
- the file is not in `beds/`
- the bed is shorter than the reel

And after the mux it measures the result. If the output has no audible audio it
deletes it and refuses, because a real AAC track carrying silence is exactly
what shipped before and it passes every other check.

The slice is taken from the reel's own slug, so each reel gets a different one
and the same slug always gets the same one. That is what this file asked for all
along.

The level is measured, not assumed. `volume=0.32` below is the figure for a bed
sitting under a voiceover. These have no voiceover, and using it put the first
batch 8 dB under the rest of the run. `bed.mjs` measures the slice and gains it
to a mean of -17.4 dB with a ceiling of -1.5, which is where the 20 shipped
nights sit.

`bed.test.mjs` checks all of it against the real bed file. It needs ffmpeg and
node, no chromium, so it runs without the render path. The suite skips it when
`FFMPEG` is unset and says so rather than passing quietly.
