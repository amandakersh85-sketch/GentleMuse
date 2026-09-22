# Life dashboard

Amanda's day on 1 page: https://claude.ai/artifact/Qj7XdVzjE4kbTBs3kVtGLy

- `life-dashboard.html` is the page. Calendar and Gmail are read live when it opens.
- The routines section reads 1 database document, `status/current`.
- `Life dashboard refresh` rewrites that document at 6:15 AM and 4:15 PM Central.
- `routines/` holds the instructions each routine runs. The routine records are
  the live copy. These files are what you read and diff.

## Where each routine reports

Routines used to report into 3 old conversations holding 474k to 659k tokens.
Every run reread all of it, and that is what ran out the weekly limit on Sep 21.
On Sep 22 they moved into small runner conversations. The old routines are
switched off and renamed `Replaced: ...`. Nothing was deleted.

| Runner | Session | Routines |
|---|---|---|
| Club Target | session_017FKVm4cJdbqbk7GCXU9wHd | claim watch (daily 11 AM), Monday challenge drop (Mon 8:40 AM), audit (Sun and Wed 7 PM) |
| Newsletter and funnel | session_01RFNX367xcxF1C9xLp6kki5 | DM email sync (daily 8 AM), breakout watcher (Tue and Fri 9 AM), Monday check (Mon 10 AM), Consider This warning (Thu Sep 24, 9 AM) |
| 1K campaign | session_01RzZjPAf4c5aT3DeUCWAUi3 | nightly scrub (9:30 PM) |
| Life dashboard | session_01S9HU9gs7eVbKsKC2uGE78w | dashboard refresh (6:15 AM and 4:15 PM), Sonnet |

The Monday check folds 4 routines into 1: scoreboard, grant deadlines,
MailerLite health and Meta Pixel. It skips any part whose old routine is still
switched on, so nothing posts twice while Amanda switches those 3 off by hand.

The refresh flags any runner over 300k tokens. When that happens, start a fresh
runner and move its routines, the same way.

Still running on their own, unchanged: Blotato queue top-up, morning email
digest, freelance lead triage, Payhip link audit.
