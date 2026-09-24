# Payhip link audit — 1st of month

- id: trig_019iiL9uHPvePKfYbYXmYf5J
- cron (UTC): 0 14 1 * *
- enabled: True
- bound session: fresh each run
- connectors: Slack, Wix
- model: default

## Prompt

Monthly Payhip link audit for The Gentle Muse (gentlemuse.co). Amanda has had product buttons on her Wix site silently break/point to dead links before (typo'd Payhip slugs vh2PB and 9GU8s are known-dead — never suggest these). This runs autonomously — Amanda is not present.

THE GOSPEL — the only correct live URLs, verified by Amanda directly in Payhip:
- Reset Guide (free): https://payhip.com/b/9FE2U
- Paycheck Planner: https://payhip.com/b/96U8s
- 7-Day Gentle Reset: https://payhip.com/b/vb2PB
- AI Tools Guide: https://payhip.com/b/PX8xh
(A 5th product, "Clarity Brain Dump," may exist by now — if you find a live Payhip link for it, use it as the gospel value for that product; otherwise skip it.)

STEPS:
1. Use the Wix connector to find every button/link on the live site that should point to one of the products above (services page, homepage, offer sections).
2. Compare each against the gospel list. Flag: dead/typo'd URLs, references to retired offers ("Content Clarity Mini"/"Clarity Package"), empty or placeholder ("#") links.
3. If everything's clean, post one line to Slack channel C0B6B4LHDPT saying so — done, no further action.
4. If you find broken/wrong links: Amanda has pre-approved you fixing these directly via the Wix API — she does NOT want a review-and-wait cycle for something this low-risk and clearly-correctable. Fix each wrong link to match the gospel URL directly, confirm the change went through, and post to Slack exactly what you changed (page, old value, new value) so she has a clear record. This is the ONE standing exception to "ask before changing the live site" — it only covers swapping a broken/wrong product link for its known-correct gospel URL. Do NOT touch page copy, layout, images, or anything else on the site under this task, and do NOT proceed with a fix if you're not fully certain which gospel URL is correct for that spot — flag genuine ambiguity in the Slack report instead of guessing.
5. If the Wix connector errors or you can't access a page, say exactly that in the Slack report rather than guessing.

End with <run-summary>clean or fixed count + Slack permalink</run-summary>.
