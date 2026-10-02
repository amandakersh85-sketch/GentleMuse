# Food review rotation state

Created 2 Oct 2026. Amanda: "I like for my food reviews to get cycled through,
so that way people are used to seeing me as a food critic and food reviewer...
I don't want people to just think I'm one note."

See `canon/positioning.md` for why this is a standing pillar, not filler.

## The roster audit, 2 Oct 2026

Her list of six: Scooter's Coffee, Sidecar Cafe, Amigos, Rico Tacos,
Scratch Cupcakery, Lucy's.

**Method.** Full pagination of her entire Blotato record, all platforms,
all statuses. The record floors at **7 May 2026** (the last page returned
119 items and no cursor). 1910 unique posts pooled across 7 May to 31 Oct.
This is a complete read of Blotato, not a sample.

| Review | In Blotato | Asset exists |
|---|---|---|
| Scooter's Coffee | IG + FB 25 Aug, FB 10 Sep | yes, 2 variants |
| Amigos | TikTok, IG, FB, YouTube all 24 Sep | yes, 4 variants |
| Sidecar Cafe | nothing, ever | **no** |
| Rico Tacos | nothing, ever | **no** |
| Scratch Cupcakery | nothing, ever | **no** |
| Lucy's | nothing, filmed 2 Oct | raw footage on her phone |

**Only 2 of the 6 exist as usable assets.** The other four cannot be
queued because there is no media to queue. Blotato media URLs only exist
where a post was made, so "never posted through Blotato" and "no asset"
are the same fact here.

**Caveat that must be stated when reporting this.** She posts natively
sometimes, and native posts never touch Blotato. Absence from Blotato is
not proof a review never ran. It IS proof there is no reusable file.

## What was queued 2 Oct

The queue was front-loaded: 11 to 18 posts/day through 8 Oct, then starving
at 1 to 3/day after 20 Oct. The rotation went into the thin half.

| Post | Platform | When | Schedule id |
|---|---|---|---|
| Scooter's | Instagram | 18 Oct 18:30 UTC | 5091972 |
| Scooter's | YouTube | 19 Oct 19:45 UTC | 5091973 |
| Amigos | Facebook | 29 Oct 17:10 UTC | 5091983 |
| Amigos | YouTube | 29 Oct 19:45 UTC | 5091985 |

Already in queue before this: Scooter's TikTok 18 Oct 15:00 (4716089),
Scooter's Facebook 19 Oct 17:10 (4716095).

That completes Scooter's as a four-channel wave on 18 to 19 Oct, and puts
Amigos back out on 29 Oct, which had been a completely empty day.

All captions rewritten rather than copied, so the re-runs are not
byte-identical to the originals.

## The audio finding, 2 Oct

Amanda, 2 Oct: "I'm really tired of having some weird music or store
background."

Measured the Amigos TikTok master. Per-half-second RMS over 29 windows:
min -27.9 dB, max -14.7 dB, **spread 13.3 dB with no silence gaps.**
That is a continuous music or ambient bed, not speech. Speech drops to
roughly -45 dB in the pauses between phrases.

**So the food review masters carry a bed she dislikes, and all meaning is
carried by on-screen text cards.** This matches the silent-b-roll mode in
`canon/filming-method.md`.

**Consequence, and it is a rule now.** Do not auto-queue these masters to
TikTok or Instagram, where sound-on matters and a disliked bed is a real
cost. Facebook and YouTube are more tolerant and were queued as-is.
For TikTok and Instagram, deliver a silent recut as a file so she can add
a Commercial Music Library song natively in-app. This is the same call that
was made and accepted for the Kuromi video on 2 Oct.

## The Amigos recut

Built 2 Oct from the TikTok master (`eefdabc3`). Verdict-first structure,
because the original opened on an abstract line over a sign and the verdict
sat at 25s.

- cold open 25.2 to 27.4, the storefront with "7.5 out of 10. I would go back."
- body 0 to 24.5, the original in order
- close 28.2 to 30.8, the mural storefront

29.3s, 1080x1920, 30fps, silent. Trims about 2s of duplicated outro.
Reordering was safe only because the audio is a non-semantic bed.

## What is blocked and why

**Sidecar Cafe, Rico Tacos, Scratch Cupcakery have no footage anywhere I
can reach.** These need to be refilmed, or she needs to confirm they only
ever ran natively and supply the files.

**Lucy's** (loose meat sandwich shop, Cedar Rapids, filmed 2 Oct) is raw on
her phone.

**The phone being plugged in does not help this session.** This runs in a
cloud container. It cannot see her phone or her laptop. The route that does
work without the laptop session: generate a Blotato presigned upload URL,
she uploads the raw footage from her end, that yields a public URL this
session can download, cut, add text cards to, re-upload and queue.
