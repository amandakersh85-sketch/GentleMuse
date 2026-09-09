# Comment keywords — live Blotato wiring

Last verified against the live Blotato automations 09/09/2026, after the
"funnel wide open" pass. **52 active automations, 26 keywords.** Was 34 active
before this pass.

Accounts: 45886 = @thegentlemuse2026 IG. 30840 = Gentle Muse FB page.
65540 = @cesasgoldenyears IG.

## Lead magnets and newsletters

| Keyword | Delivers | Link | Live on |
|---|---|---|---|
| SEASONAL | Consider This weekly note, seasonal series | consider-this.subscribepage.io | IG, FB, Cesa IG |
| CONSIDER | Consider This weekly note | consider-this.subscribepage.io | IG, FB, Cesa IG |
| CESA | Cesa guide, 15 pages | cesa-guide.subscribepage.io | IG, FB, Cesa IG |
| RESET | Gentle Reset Guide, free | payhip.com/b/9FE2U | IG, FB |
| TUESDAY | Just Another Tuesday | just-another-tuesday-gm.subscribepage.io | IG, FB |
| PLAY | Press Play, 10 audiobooks | press-play.subscribepage.io | IG, FB |
| GUIDE | AI Tools Guide, 59 pages | ai-guide.subscribepage.io | IG, FB |
| BOTTLENECK | Business Bottleneck Check | gentlemuse.co/business-bottleneck-check | IG, FB |
| BUDGET | Paycheck Planner, paid | payhip.com/b/96U8s | IG |
| SESSION | Decision Session, paid | payhip.com/b/upvAa | IG |

## Club Target products, all SKUs verified live against target.com 09/09

| Keyword | Product | SKU | Live on |
|---|---|---|---|
| DISHWASHER | Molly's Suds dishwasher pods, citrus 45ct | 94851578 | IG, FB |
| BLOOM | Bloom Sparkling Energy, cherry lime 12oz | 91946019 | IG, FB |
| CURLTALK | Not Your Mother's Curl Talk cream, 6oz | 76550582 | IG, FB |
| SCRUB | Tree Hut Moroccan Rose Shea Sugar Scrub 18oz | 51693591 | IG, FB |
| BUTTER | Tree Hut Moroccan Rose Whipped Body Butter 8.4oz | 83245016 | IG, FB |
| HIBISCUS | Tree Hut Pink Hibiscus Shea Sugar Scrub 18oz | 89094549 | IG, FB |
| NATIVE | Native Sensitive Deodorant, Cotton & Lily 2.65oz | 76612085 | IG, FB |
| SOOTHE | Raw Sugar Green Tea Aloe Body Wash 20oz | 94837564 | IG, FB |
| LIPDRIP | NYX Fat Oil Lip Drip, Missed Call | 87824456 | IG, FB |
| BROW | NYX Thick It Stick It Brow Gel Mascara, Brunette | 83347380 | IG, FB |
| SOAK | Dr Teal's Calm & Serenity Rose Epsom Soak 3lb | 76858934 | IG, FB |
| GEL | medicube TXA Niacinamide Capsule Cream 55g | 1010763977 | IG, FB |
| NECKLACE | Adornia 14k Black Clover Station Necklace | 1005653750 | IG, FB |
| BRACELET | Adornia 14k Mother of Pearl Clover Bracelet | 1004621500 | IG, FB |
| MASK | medicube Turmeric Jelly Gel Mask | **NEEDS SKU** | FB |
| FALLFIT | Universal Thread Open Stitch Cozy Cardigan | **NEEDS SKU** | IG |

Plus **PR Collaboration Screening** on IG, auto-replying to collab, gifted
product, pr package, brand ambassador and similar DMs.

## What changed in the 09/09 pass

**Switched on, 12:** HIBISCUS on IG and FB, BRACELET on IG and FB, NECKLACE on
IG and FB, SOAK on FB, BROW on FB, SOOTHE on FB, NATIVE on FB, BUDGET on IG,
SESSION on IG.

**Created from scratch on Facebook, 6:** BUTTER, LIPDRIP, BLOOM, CURLTALK,
DISHWASHER, GEL. None of these existed on FB before.

**Fixed:**
- Every newly enabled keyword had only the uppercase form. Added lowercase and
  title case to all of them, matching how the working ones are set up.
- GEL and MASK were `message-received`, so they only fired on DMs. Both are now
  `comment-received`.
- FALLFIT pointed at SKU 94430282, which 404s. Repointed to the storefront so it
  stops sending people to a dead page, and renamed to flag it.

## 2 SKUs still needed

1. **FALLFIT** — Universal Thread Open Stitch Cozy Cardigan. Old SKU 94430282
   is dead. On the storefront link until replaced.
2. **MASK** — medicube Kojic Acid Turmeric Jelly Gel Mask. Never had a product
   SKU, only the storefront. Not findable from the cloud session.

Both are on and delivering to the storefront, which still earns, but neither is
a product link and both break the hard link rule until fixed.

## Correctly left off, 6

All duplicates or superseded. Turning any of them on would create a conflict.

- **447 TUESDAY IG** and **427 TUESDAY FB** — superseded by 2771 and 2772,
  which capture email. The old ones do not.
- **412 FB RESET** and **413 FB RESET DM** — superseded by 2778. 413 also points
  at the old gentlemuse.co/reset-guide URL.
- **446 IG AI** — sells the retired 17 USD AI guide, superseded by the free
  GUIDE. Its keyword is the bare string "AI", which would fire on any comment
  containing those 2 letters.
- **450 IG PROMO** — a promo rejection auto-reply whose keywords include
  "send me" and "promo". The PR Collaboration Screening (415) already handles
  this, and turning it on risks firing at people making ordinary comments.
