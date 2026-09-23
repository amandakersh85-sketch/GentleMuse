# Daily: DM email sync + keyword failure sweep

- id: trig_0123dXXH4Gn978bHSD6gehCZ
- cron (UTC): 0 13 * * *
- enabled: True
- bound session: session_01Lj4AttK199DuE1QnxDMi2g
- connectors: none
- model: default

## Prompt

Daily lead sync and keyword health check for The Gentle Muse. Blotato DM automations that use an emailGate capture addresses in the DM thread, and nothing pushes them to MailerLite, so the delivery automations never fire without this job.

Current as of 2026-09-01. ManyChat was disconnected on 2026-08-30 and is dead; Blotato holds every keyword outright. The 10 duplicate "DO NOT ACTIVATE" automations were deleted on 2026-08-30, so no duplicate of a live automation should exist. If you find one, deactivate it and say so: Instagram allows one private reply per comment, and two automations watching the same comment means one fails silently with error 20102.

STEP 1. Call blotato_list_automations. Build the list yourself: every automation with isActive true AND an emailGate. Do not trust this list, it changes. On 2026-09-10 it was exactly 3, all SEASONAL and all deliberate: 4009 (Amanda's IG 45886), 4010 (Amanda's FB 30840), 4011 (cesasgoldenyears IG 65540), all into group Consider This.

2771 TUESDAY (IG 45886) and 2772 TUESDAY (FB 30840) had their emailGate REMOVED on 2026-09-09 and must stay that way. The gate was burning the single private-reply slot per comment before the person ever got the link. If an emailGate reappears on 2771 or 2772, flag it loudly, do not sync around it.

CESA needs no syncing. 445, 432 and 2952 had their emailGate removed on 2026-08-28 and now send a button to https://cesa-guide.subscribepage.io, which captures the email itself and feeds the Cesa group directly. Only sync a CESA automation if it somehow has an emailGate again.

STEP 2. For each qualifying automation call blotato_list_automation_runs and blotato_list_automation_logs. Pull captured addresses out of the logs. Add each with mcp__MailerLite__add_subscriber, ALWAYS passing status "active" explicitly, never relying on the default. Joining the group IS the delivery. Skip anyone already active.
Group IDs: Cesa 196024300390581479, Consider This 195832544509298574, Just Another Tuesday 195832548837819660, AI Beginner's Guide 195970516536788891, Press Play 195515945901360732, Gentle Muse Subscribers 191820189953688990.

STEP 3. Check every live automation for failed runs, not just the emailGate ones. Report each failure with its error, the post, and the time.
- Error 20102, "already has a reply", means something claimed that comment's single DM slot first. With ManyChat gone the likely causes are a person private-replying from the Instagram app before the automation, or a duplicate automation. Public comment replies do NOT consume the slot and Amanda should keep making them.
- NO automation should have a followGate. 5 Instagram automations briefly had one on 2026-08-30 (445 CESA, 435 RESET, 1393 CONSIDER, 1019 PLAY, 1424 GUIDE) and Amanda had all 5 removed on 2026-08-31: with zero real keyword usage the gate could only add friction to the one thing that converts. If a followGate appears on any automation, flag it rather than removing it, and say which one.

STEP 4. Sweep the subscriber list. Call mcp__MailerLite__list_subscribers and filter the statuses YOURSELF in the returned data. The filter_status parameter is unreliable and has returned every subscriber regardless of the value passed.
(a) Anyone "unconfirmed", or active with sent 0: get their group, re-add with status "active" and that same group, and report the signup date and how long they were stuck.
(b) THE 12-SEND CHECK, standing decision by Amanda 2026-09-01.

FIRST, before applying any part of this check, remove Amanda's own addresses and test aliases from the set entirely: amandakersh85@gmail.com, amanda@gentlemuse.co, any +cesatest / +cesatest2 / +cesaloop / +lptest alias, and princesamaryelizabeth@gmail.com. These are NEVER eligible for the 12-send check no matter what their sent or opens_count say. Amanda does not open her own broadcasts, so her addresses will keep crossing this threshold forever. amanda@gentlemuse.co reached 12 sends and 0 opens on 2026-09-10 and is expected to keep climbing. Never surface it, never call it ready to remove.

THEN apply the check to whoever is left. Report by name any remaining subscriber whose sent count has reached 12 or more while opens_count is still exactly 0. Amanda's decision is that these get dropped, so surface them clearly and say the record is ready to remove and awaiting her go-ahead in the session. Do not delete on your own. This was set for Melissa (mmlaird8@gmail.com) and Nadia (nadezhda.isaenko.psy@gmail.com), both at 8 sends and 0 opens on 2026-09-01, but it applies to anyone who meets the condition. Both were suppressed on 2026-09-08 at 9 sends, status unsubscribed and not deleted, which is the correct method: suppression, never deletion, because Amanda imports contact lists and deleted records silently come back. Nobody with even 1 open qualifies, and nobody under 12 sends qualifies.
Caveat to state alongside it: an open is an image pixel, so Apple Mail Privacy Protection and image blocking can hide a real reader. At 12 sends with nothing registered that risk is small but it is not zero.

Who is real. As of 2026-09-09 there are 7 real subscribers on this account: Mary (marymichellebutler@yahoo.com), Melissa, Nadia, christine (chgaiotti@gmail.com), Laura (ljdanielson@gmail.com), Shaniya and artine. Everything else is Amanda's own addresses and tests: amandakersh85@gmail.com, amanda@gentlemuse.co, the +cesatest / +cesatest2 / +cesaloop / +lptest aliases, and princesamaryelizabeth@gmail.com which shares her IP. Never count those as audience and never quote an open rate without subtracting them first. At this size say the number of named humans, not a percentage.

Baseline expectation. Every real conversion so far has come through a landing page webform, never through a keyword. As of 2026-09-10 no real audience member has ever used a keyword, and the AI Beginner's Guide and Press Play groups have never had a subscriber. So an empty keyword result is the normal result right now, not evidence the job is broken. The first genuine keyword capture is real news and is worth saying loudly.

Report only if something was added, converted, or FAILED, if a followGate reappeared, if an emailGate came back on 2771 or 2772, or if someone who is NOT one of Amanda's own addresses hit the 12-send check. Failed runs are always worth reporting even when nothing was captured. Otherwise say nothing and stay quiet.
