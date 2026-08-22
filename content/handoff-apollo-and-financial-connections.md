# Handoff — Apollo.io setup + financial project connections

Written 08/22/2026 by the cloud session for the local Claude / VS Code session.
Two separate jobs below. Job 2 needs Amanda present with password access.

## Account state (verified 08/22)

Apollo.io connected, free tier, nothing used yet:
- 180 lead credits, 160 direct dial credits, 5,000 AI credits
- 0 export credits (no bulk CSV export on this tier)
- Waterfall email and phone enrichment: NOT enabled
- Budget rule stands: 10 USD per month ceiling, stay on free tier

180 lead credits is the real constraint. Roughly 180 contact reveals total.
Do not burn them on broad searches. Search first (search is free), reveal only
the contacts that pass a human check.

## Job 1 — Apollo setup for Consider This sponsorship sales

Goal: a second income stream on the newsletter Amanda already owns, on top of
its affiliate links. Not for selling her consumer digital products, Apollo
cannot target individual consumers.

Steps:
1. Build the Context Center profile (apollo_context_center_create_profile).
   Product = Consider This, a weekly email about 1 overlooked thing in your
   home. Audience = US women running households, practical, budget-aware.
   Positioning for sponsors = high-trust, low-volume, honest recommendations.
2. Define the sponsor ICP: brand marketing, partnerships, and influencer
   marketing titles at cleaning, home goods, small appliance, and organization
   brands. Company size 50 to 5,000. US.
3. Run apollo_mixed_people_api_search against that ICP. Search costs nothing.
   Shortlist 20 to 30 by hand before revealing a single contact.
4. Reveal only the shortlist. Track spend, report the credit balance back to
   Amanda after every reveal.
5. Draft the outreach sequence but DO NOT SEND. Amanda approves all outreach.

Hard constraints on outreach:
- NEVER send from gentlemuse.co. Cold email from the newsletter's sending
  domain can wreck MailerLite deliverability to real subscribers. Buy or use a
  separate outreach domain.
- CAN-SPAM: real physical address (6701 Corporate Drive, Suite R, Johnston,
  Iowa 50131), working opt-out, honest subject line.
- Voice rules apply to outreach copy too: no em dashes, digits not spelled-out
  numbers, contractions, no hype.

Timing: sponsors buy November and December slots in early October. September
is for growing the subscriber count, because sponsors ask for list size.
Nothing to sell until there is a number worth quoting.

Secondary Apollo uses, same credit budget:
- Brand partnership contacts at Bissell, The Ordinary, FlavCity

ON HOLD per Amanda 08/22: Kersh Vending placement outreach. Do not start it.

## Job 1b — Laundromat acquisition research (owner financing)

Amanda is rebuilding credit toward business loan approval, targeting a local
laundromat purchase, ideally with creative or owner financing. Timeline is a
few months out. A game plan reportedly already exists, find it before adding
anything new.

Apollo's role here is LIMITED and it must be said plainly. Apollo is a
database of operating companies and their employees. It has no for-sale
filter, no owner-financing filter, and no listing data. Small owner-operated
laundromats often have no Apollo record at all because the database skews
toward companies with employees and a digital footprint.

Where Apollo genuinely helps: building an off-market owner contact list.
Search organizations by industry and Des Moines metro geography, then find
the owner or principal. Off-market direct approach is how a lot of seller
financing actually gets negotiated, because there is no broker pushing for
all cash at close. Expect thin coverage, verify every hit by hand.

Better primary sources for the actual deal hunt, none of which are Apollo:
BizBuySell (has a seller-financing filter), BizQuest, local business brokers,
county records, and simply driving the routes she already drives.

Free expert help, no budget impact: America's SBDC Iowa serves all 99
counties through 15 regional centers, no cost, and explicitly covers
financing, loan proposals, cash flow projections, and acquisition. Getting an
SBDC advisor involved before she talks to a bank is worth more than any tool
on this list. https://iowasbdc.org/

## Job 2 — Financial project connections (relay to Avery / Codex)

Amanda's message, relayed as given: the financial project connections still
need to be set up. She says Avery will know what this refers to. Do not guess
at the scope, confirm it with Amanda before touching anything financial.

Known and verifiable from the cloud session: 3 connectors are authorized but
NOT signed in, and a cloud session cannot run their OAuth flows:
- Stripe
- Meta Ads
- Canva

These have to be authorized interactively by Amanda, either in claude.ai
connector settings or through /mcp in a local interactive session.

Amanda expects this to require password lookups and probably password
resets. Plan for it. She wants to be walked to each sign-in point rather than
handed a list.

Rules that do not bend on financial work:
- Nothing financial is automated or filed without Amanda's approval
- HOLD documents are never touched, moved, renamed, or sent
- doc-triage-LOCAL-ONLY.csv never leaves the machine
- No new paid services, 10 USD per month ceiling

## Time estimates

Apollo setup (Job 1): 45 to 60 minutes, and most of it is decisions, not
passwords. Context Center 15 min, ICP and first search 20 min, shortlist and
reveals 15 min, draft sequence 10 min. Amanda needs to be present for the ICP
decisions and the shortlist, not for the mechanical parts.

Financial connections (Job 2): 90 minutes to 3 hours, realistically. The
variance is entirely password resets and 2FA. Each connector is 5 minutes if
the password works and 20 to 30 minutes if it needs a reset with email or SMS
verification. 3 connectors plus whatever Avery's financial project scope adds.
Do this in one sitting with the password manager open. It is a one time cost,
it does not recur.

Recommended order: Job 2 first while Amanda has the patience for passwords,
Job 1 second because it is the more interesting work and makes a better
finish.
