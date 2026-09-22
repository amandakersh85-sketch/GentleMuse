# Funnel watch — deliveries, gates, and the DM inbox

- id: trig_01ErT42pMQ87cEbk1Y3NXppt
- cron (UTC): 18 */2 * * *
- enabled: False
- bound session: session_01Lj4AttK199DuE1QnxDMi2g
- connectors: none
- model: default

## Prompt

FUNNEL WATCH. Confirm the funnel delivers. Watch the DM inbox but DO NOT reply in it. Stay silent unless something below fires.

STEP 1. RUNS. blotato_list_automation_runs on 2952 (CESA, Cesa IG, 65540), 445 (CESA, main IG, 45886), 432 (CESA, Facebook, 30840).

Baseline as of 2026-09-08 15:15 UTC — ignore:
- 2952: run 150551 (expired, contact 1774569036904343), 122274 (completed, 955627417560872)
- 445: 122325, 113285 completed; 113157, 112624 failed 20102; all contact 1048429878116670
- 432: none, ever

NOT A LEAD: test contacts 1048429878116670, 955627417560872. NOT A LEAD, A FAULT: her own ids 17841432484315950 (Cesa IG), 17841480184590976 (main IG), 1086399221215093 (FB page). 2952 matches "year old"/"years old" and her captions say "19 years old" constantly, so a first-comment on that account could self-trigger. Whether Blotato ignores an account's own comments is UNVERIFIED. A run from one of her ids is a self-trigger to fix — name the keyword and which of her comments it caught.

A REAL ONE is any new run whose contactId is none of those five.

STEP 2. IF A REAL ONE APPEARS: blotato_list_automation_logs with the flowRunId, quote the comment and post id. DM status "sent", errorCode null. Failed 20102 means the comment's one private-reply slot was already spent and it CANNOT be retried by DM — only a public comment reply reaches that person; never tell Amanda to DM a 20102 lead by hand, it is impossible (confirmed by test 2026-09-08, contact 1774569036904343). Confirm the button to https://cesa-guide.subscribepage.io. Run "completed" is good; "waiting" means a gate is back in the path, flag it hard. THE ACTUAL CONVERSION: mcp__MailerLite__list_subscribers, new record in Cesa group 196024300390581479 after the comment. If MailerLite is unavailable SAY SO — a check that cannot run is not a check that passed.

STEP 3. GATES. Confirm 2952, 445 and 432 carry NO emailGate and NO followGate. All gates in the CESA/CONSIDER path were removed 2026-09-08 (2952, 445, 432, 1393, 2954). SEASONAL (4009, 4010, 4011) keep theirs deliberately — not yours to change. A gate HAS reappeared spontaneously before, on 2952 between Aug 28 and Sept 3, so actually check rather than reasoning that nothing could have changed it.

Cheap single-record reads — a cursor is base64 of "<createdAt>_<id>":
- 445: encode "2026-08-08T19:57:27.092Z_446", limit 1
- 432: encode "2026-08-08T19:48:25.060Z_434", limit 1
- 2952 + 2954: cursor MjAyNi0wOC0yN1QxODoxNTowMi4wMDBaXzI5NTQ=, limit 2

If a gate reappeared, ALSO re-read that automation's dmMessage and flag any sentence that only makes sense with a gate in the path — "you're in", "reply with", "I'll add you", "send me your email".

STEP 4. THE DM INBOX — READ ONLY. DO NOT SEND DMs FROM THIS ROUTINE.

**CRITICAL FINDING, 2026-09-09 04:18. You CANNOT tell whether a DM has been answered.** Blotato records DMs it sent itself and DMs received, but NOT the replies Amanda sends from the Instagram app. Proof: conversations 229724 and 219329 contain ONLY incoming messages, yet both correspondents quote her replies back at her ("I like the way you think", "You're right about Cesa", "You're not chasing shiny objects"). She is answering; the record just does not show it.

An earlier version of this prompt told you to reply to any DM that looked unanswered. That was wrong and is now revoked. Acting on it risks replying into a conversation she is actively conducting, in a register that is hers and not yours, and possibly contradicting something she already said and you cannot see.

**Her DM inbox is not a queue. It is her correspondence.** Some of it is personal. Some is live business negotiation. Read it, report it, do not answer it.

blotato_list_conversations for 65540 and 45886, platform instagram. Take every conversation whose createdAt OR updatedAt falls in the last 24 hours — NOT just createdAt. For each, blotato_list_messages. Then:

**An email address typed in-thread** → that address is STRANDED; nothing syncs a hand-sent thread. Add it to the Cesa group 196024300390581479 yourself, say you did. This is the ONLY DM action you take without asking.

**Everything else** → REPORT IT TO HER, quote it, name the account, and take no action. That includes warm fans, senior-dog owners, solicitations, and business talk. If someone qualifies for the guide, hand her the exact send parameters (accountId, platform, recipientId, commentId if there is one) and note the 24-hour DM window, but do not send it.

**Known threads, context so you do not misread them:**
- `229724`, contact 1725097938924220 — sells food trailers, proposing a commission arrangement with her in Iowa, warm personal register ("Yes honey"). House of Trailers is one of her real website clients, so treat this as a genuine business relationship, NOT a scam. Never reply. Report new messages only.
- `490500`, contact 965890496530269 (@emmamilesx / ratherpeach.com) — pay-to-collab: place an order with a discount code, then get "onboarded". Contradicts her stated policy, "I do not pay shipping, processing, membership, starter kit, or ambassador fees." Never reply.
- `219329`, contact 1701463360911952 — MLM recruiter, "freedom-based online business", high-ticket affiliate Roadmap, bumping since Aug 20. She has replied herself. Never reply.

**Abuse, sexual content, legal threats, accusations about Cesa's care** → never reply, quote it so she can block.

Her PR screening automation 415 is missing the collab pitches: its keywords are phrases like "like to collab", so 'Tap "collab" below' does not match. Same substring-adjacency failure as "my chi" not matching "my healthy chi". Proposed fix is the standalone token "collab" — PROPOSE, do not add. Keyword changes are config Amanda approves.

ALSO REPORT, even with nothing else: a new FAILED run; a gate reappearing; a run from one of her own ids; any new DM.

PUBLIC COMMENT replies are a different matter and are handled by trig_01HK4yKpqXoMKYjpiX6LQUj2, which posts them without asking. That routine is correct and unaffected: a comment is public, its reply history is fully visible, and there is no hidden side to the conversation.

Otherwise say nothing. Silence is the expected result most of the time.
