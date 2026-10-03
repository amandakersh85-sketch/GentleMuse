# Target footage inventory, 12 Sep 2026

## Where the footage actually is

**Not on any machine I can reach.** This session runs in a fresh cloud container.
Scanned the whole filesystem: 1 media file total, and it is not hers. `/home/user`
holds only the git repo. Her Downloads, phone exports and local drives do not exist
in this environment and never will.

**Google Drive: no video files.** Searched `mimeType contains 'video/'` modified
since 1 Aug. Zero results.

**The real library is Blotato.** Every asset she has ever posted or queued lives on
the Blotato CDN and is referenced by the posts. That is a complete, dated,
caption-labelled inventory and it is fully readable.

Harvested from 1,620 post rows across 7 queue pulls:

| | count |
| --- | --- |
| Unique media assets | 659 |
| Video | 337 |
| Image and graphic | 322 |
| **Carrying a Club Target tag** | **26** |

## The 26 Target assets, chronological

| First used | Asset | What it shows |
| --- | --- | --- |
| 20 Aug | `0d080199` | FlavCity protein variety pack |
| 20 Aug | `571b6622` | **heyday phone cases** |
| 21 Aug | `095a9b3b`, `3e2a525c` | Good and Gather cookbook |
| 21 Aug | `19d97015` | Cat and Jack kids |
| 21 Aug | `1b40ca1a`, `ffb909be` | Sweaters, skirts, cardigan |
| 21 Aug | `2469fb31`, `afb5fddf` | Freshpet, pet aisle |
| 21 Aug | `6623546a`, `83d89173` | Native, Raw Sugar, dorm |
| 21 Aug | `95acfd10` | Cinnamon Toast Crunch |
| 21 Aug | `a484faa6` | NYX fat oil |
| 31 Aug | `600306c6` | Cat and Jack summer |
| 3 Sep | `232050d5` | Adornia necklace |
| 5 Sep | `aac8732a` | Fall aisles, Starbucks wall |
| 5 Sep | `f2c482e8` | Molly's Suds, cleaning aisle |
| 6 Sep | `6463cc6c` | **All in Motion sherpa zip** |
| 7 Sep | `99a1586f` | Tillamook freezer door |
| 8 Sep | `9c6802ec` | **Good and Gather salad kits** |
| 9 Sep | `ce491416` | **Tree Hut pink hibiscus scrub** |
| 10 Sep | `2c27e52c`, `fd75c909` | **Glass pumpkins, Threshold candle** |
| 10 Sep | `4cac0223` | **Fall racks** |
| 11 Sep | `7ece215a` | NYX |
| 12 Sep | `503b0ef8` | **Wellness reset** |

## Coverage against the 10 board themes

| Theme | Assets | Verdict |
| --- | --- | --- |
| Quick & Easy Meals | 3 | **covered**, `9c6802ec` is current |
| Fall Style Collage | 6 | **covered**, `4cac0223` shot 10 Sep |
| Fresh Activewear | 1 | **covered**, `6463cc6c` shot 6 Sep |
| Fall Home Refresh | 3 | **covered**, `fd75c909` shot 10 Sep |
| Everyday Target Favorites | 4 | **covered**, `ce491416` shot 9 Sep |
| Your Everyday Wellness Reset | 4 | **covered**, `503b0ef8` shot 12 Sep |
| Make It Yours with Heyday | 1 | **August only**, `571b6622`. Needs new. |
| Find Your Denim | **0** | Nothing. Needs new. |
| New Ways to Play | 0 usable | Only a NYX post matched on the word "play". Needs new. |
| Game Day Line Up | **0** | Nothing. Needs new. |

## Broken things found

**`2277` IG FALLFIT.** Confirmed exactly as Amanda described. The automation is
literally named "NEEDS SKU, cardigan 94430282 is dead" and its button points at
`club.target.com/a/amanda.20`, the bare storefront. Anyone who comments FALLFIT
lands on a storefront, not the cardigan.

**`453` FB MASK, not previously known.** Same failure. Named "medicube Turmeric
Mask, NEEDS SKU", button points at the bare storefront. Broken since 8 Aug.

Both need a SKU captured in store. Nothing else can fix them.

## Blotato Instagram Story support: CONFIRMED

`blotato_create_post` accepts `mediaType: "story"` for Instagram and Facebook.
Assumption A is resolved in the good direction. Stories can be queued like any
other post. No manual folder, no tap-through list needed.

Caveat: `firstComment` is not supported on stories, so a Story cannot carry a
keyword in a comment. The keyword has to be on-screen or in a link sticker.
