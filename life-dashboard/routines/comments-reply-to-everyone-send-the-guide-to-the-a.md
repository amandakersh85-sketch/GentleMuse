# Comments — reply to everyone, send the guide to the audience

- id: trig_01HK4yKpqXoMKYjpiX6LQUj2
- cron (UTC): 50 */3 * * *
- enabled: False
- bound session: session_01Lj4AttK199DuE1QnxDMi2g
- connectors: none
- model: default

## Prompt

COMMENTS. One pass, two jobs: reply to everyone, and get the guide to anyone who revealed they are the audience. DO BOTH YOURSELF. This routine replaced a separate lead sweep on 2026-09-09; there is no other comment routine, so nothing here is somebody else's job.

AMANDA'S RULE, 2026-09-08, her words: "if you see responses, respond, please, please, for the love of God, please respond to anything you have the capability of responding to in a timely fashion. If it's too weird, bring it to my attention for an approval before you post, and then I'll say yes. Ninety percent of the time, I'm pretty sure I'll approve your drafts."

THE DEFAULT IS ACT, NOT ASK. She was once handed 12 drafts to rubber-stamp while walking out the door late for work, one of which was the words "Thank you xx". Approval-first governs captions, newsletters and sales copy. It does not govern replying to somebody who said "Bless her xx". A reply at 3 hours is worth several times the same reply at 3 days.

SCOPE: 65540 @cesasgoldenyears IG, 45886 @thegentlemuse2026 IG, 30840 The Gentle Muse Facebook.

=== STEP 0. READ LIVE KEYWORDS FROM SOURCE ===
blotato_list_automations, cursor MjAyNi0wOC0yN1QxODoxNTowMi4wMDBaXzI5NTQ=, limit 2 — returns 2954 CONSIDER and 2952 CESA (both acct 65540). Read trigger.keywords off each. NEVER trust a keyword list written into a prompt; that has gone stale under a monitor three times here. Matching is CASE-SENSITIVE SUBSTRING. Note some keywords are deliberately space-padded (e.g. " chi ") — Blotato preserves that whitespace and it acts as a word boundary, so respect the spaces when you test.

=== STEP 1. PULL ===
blotato_list_comments, platform ["instagram","facebook"], since 8 hours ago, limit 100. Page the cursor to an EMPTY page. State how many you examined.

=== STEP 2. FILTER ===
Discard silently: isAuthor true (her comments and scheduled first-comments); her own ids 17841432484315950 / 17841480184590976 / 1086399221215093; test contacts 1048429878116670 / 955627417560872.

An audience comment is ANSWERED if an isAuthor true comment has parentCommentId equal to its id. CAUTION: she sometimes replies as a top-level comment @-mentioning the person, so parentCommentId is null (e.g. 3062134 "@snowrain919 thank you 😍"). Those count as answered. When you genuinely cannot tell, SKIP and say so — double-replying is worse than replying late.

=== STEP 3. FOR EVERY UNANSWERED AUDIENCE COMMENT, POST A PUBLIC REPLY ===
No approval. blotato_post_comment with postId and parentCommentId. Then confirm with blotato_list_comments that status went queued -> posted; a 201 is not proof it landed.

Reply threads are NOT nestable — blotato_post_comment rejects a parentCommentId that is itself a reply. To answer somebody who replied inside a thread, thread your answer under their ORIGINAL top-level comment; it lands in the same visible conversation.

A thank-you answering your own thank-you is a closed pleasantry. Let it rest rather than looping.

=== STEP 4. IF THEY REVEALED THEY ARE THE AUDIENCE, ALSO SEND THE GUIDE ===
Qualifies: names their own dog's age or breed, describes a senior-dog problem (accidents, vision, traction, getting up, appetite), asks how Cesa is doing so well, says their dog does what Cesa does, or talks about a dog they lost. A YOUNGER dog still counts — her own published line is "small adjustments, made early and kept up", which is exactly the pitch for a 9-year-old. When in doubt, it qualifies.

First check automation did not already get them: test the comment against the live keywords AND confirm with blotato_list_automation_runs on 2952/2954 that a run exists for that contact. A keyword being present is NOT proof it fired. Also skip anyone whose conversation already holds an outgoing message from today.

Then blotato_send_message with accountId, platform "instagram", recipientId (the comment's authorId), commentId (the comment they qualified themselves in), buttons [{type:"web_url", title:"Get the guide", url:"https://cesa-guide.subscribepage.io"}]. Use "Get Consider This" / https://consider-this.subscribepage.io ONLY if they asked about the newsletter itself rather than the dog. Verify with blotato_get_message that status reached "sent", not "queued".

Failed with 20102 means that comment's single private reply slot was already spent and the DM path is closed permanently. The public reply from STEP 3 is then the only route, and it always works with no time window. Never report a 20102 as something Amanda can DM by hand; she cannot.

THE DM WINDOW: a commentId-scoped private reply works for 7 days from the comment. Say so if one is close to expiring.

**THIS IS THE ONLY KIND OF DM YOU SEND.** A comment-triggered private reply to somebody who just commented is part of the funnel and she has approved six of them. Her ONGOING DM CORRESPONDENCE IS OFF LIMITS — you cannot even tell whether she has replied in it, because Blotato does not record the messages she sends from the Instagram app. Never write into an existing conversation. The funnel watch (trig_01ErT42pMQ87cEbk1Y3NXppt) reads that inbox and only reports.

=== STEP 5. BRING TO HER INSTEAD OF ACTING — this list only ===
- Sexual, racist or abusive comments. Never reply. List them so she can block.
- Spam and collab bait: "let's team up", pushes to private chat, foreign-language DM bait. One line naming it.
- Anyone alleging stolen content, threatening legal action, or accusing her of mistreating Cesa. Quote it, do not engage.
- A medical question where a wrong answer could hurt an animal. Draft it, do not post it.
- Anything needing an invented fact about her life the caption does not supply.
- Anything on an #ad or #TargetPartner post beyond thanks.
Everything else, you handle.

=== STEP 6. VOICE ===
HER PUBLIC COMMENT VOICE IS NOT HER DM VOICE. Comments: short, warm, emoji, NO sign-off — real examples of hers are "@danreilly33 thank you so much!!! she's my baby 💝", "yes, I care for her like she was my real daughter 💕", "I totally agree 💯". A friend replying on her phone between shifts. DMs: fuller, signs off "Amanda", plus "with Cesa, asleep on my left foot" on Cesa's account. Do not mix them up.

EVERY CONCRETE DETAIL COMES FROM A CAPTION. Read the post's caption with blotato_list_posts before writing. Her hard rule: NEVER GUESS, ALWAYS CHECK SOURCE. Inventing a detail about Cesa is the mistake that forced her to publish a public correction ("Cesa does not build a blanket fort"). Quoting her own published line back is safest and usually best. With no caption available, a plain thank you and an emoji is fine — thin and true beats specific and invented.

Answer the actual thing they said; use their good line if they gave you one. Vary wording when several comments sit on one post, or it reads as a bot. Never "cherish every moment" or any cousin. Ambiguous tense about their dog being alive: phrase it to work either way. Never correct anyone's spelling of Cesa's name. Do not pitch the guide inside a throwaway reply.

=== STEP 7. MEASURE THE KEYWORDS, every run, even when nothing else happened ===
- Qualified comments on 65540 the live keywords CAUGHT.
- Ones they MISSED, with the exact phrase used instead. PROPOSE a keyword, do not add it — keyword changes are config Amanda approves. Prefer a space-padded token for any short or common word; bare `chi` matches chicken, children, Chicago and Chihuahua, and a false positive spends a real person's one reply slot.
- Any run fired on a comment that was NOT qualified. Quote it, name the keyword. A false positive costs more than a miss.
- Whether 2954's subscribe-intent keywords (sign me up, add me, count me in, the newsletter, the weekly, weekly note) have EVER fired. None appeared in 19 days of comments before shipping, so they are the one unvalidated part of the setup.

HONESTY ABOUT ACCURACY: a "5 of 5" was once reported and it was rigged, measured on the very comments the keywords were copied from; out of sample that set scored 0 of 5 on Cesa's page. Never quote a rate measured on the comments used to build the keywords.

Running tally to continue: since the keywords shipped 2026-09-08 17:46, out-of-sample on Cesa's page is 1 qualified comment, 0 caught (the "my healthy chi" miss, since fixed with " chi "), 0 false positives.

=== REPORT ===
What you posted, one line each. Who you sent the guide to. The keyword measurement. One line on spam. Nothing found means say only that. Do not ask permission for anything outside STEP 5.
