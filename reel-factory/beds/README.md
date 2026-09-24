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
