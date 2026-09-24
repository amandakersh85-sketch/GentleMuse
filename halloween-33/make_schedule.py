"""Build schedule.json: every post of the 33 Nights countdown, ready to load.

  python3 make_schedule.py      reads weeks/week*-posts.json, weeks/media.json and
                                backup/queue-2026-09-23-full.json, writes schedule.json

Each entry is 1 post: when, where, what, and which old Halloween posts on that
date it replaces. load.py does the loading, 7 days ahead at a time.
"""
import json, os, glob, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://database.blotato.io/storage/v1/object/public/public_media/5472a21c-0213-4305-8693-b19295e4d67e/'
ACCT = {'instagram': '45886', 'tiktok': '41488', 'facebook': '30840', 'youtube': '36129'}
FB_PAGE = '1086399221215093'
NOTE = 'https://consider-this.subscribepage.io'
KEEP = {'4459039', '4459043', '4137937', '4137938'}  # Samhain 5 nights out, Samhain itself
TIME = {'instagram': '23:00', 'tiktok': '23:00', 'facebook': '23:30', 'youtube': '23:30'}

# Reposted nights: existing media, existing words, plus the night count.
REPOSTS = {
    'REUSE-goosebumps': {
        'media': {'instagram': 'fadd5a7e-e360-4395-864c-6232d82c12e1.mp4', 'tiktok': 'cda9a85f-0e23-4478-b6b4-b8a72a5108f6.mp4',
                  'facebook': '4c1f1094-ebdc-4595-999b-f33044610061.mp4', 'youtube': '35288a2f-8449-4793-b450-082b68dd1cbc.mp4'},
        'hook': 'Goosebumps was dismissed by every serious critic who looked at it.',
        'body': 'Books in 1992, television by 1995, and R.L. Stine writing at roughly one a month. Fast, cheap, and for children.',
        'close': 'It taught a whole generation that a chapter ending on a hook is worth staying up for.', 'tag': '#nostalgia'},
    'REUSE-turnips': {
        'media': {p: 'afe4cff5-2d64-40f2-a4a8-6a30a74b6a48.mp4' for p in ACCT},
        'hook': 'Jack o lanterns were turnips.',
        'body': 'Ireland and Scotland carved them out of turnips and beets for centuries. Irish immigrants switched to pumpkins in America because they were bigger and easier to hollow out.',
        'close': 'The ritual mattered. The turnip did not.', 'tag': '#history'},
    'REUSE-samhain': {
        'media': {p: 'cceb6cc6-6a2b-491b-9a40-2c10a0b27a1f.mp4' for p in ACCT},
        'hook': 'Halloween was never about fear.',
        'body': 'It grew out of Samhain, the Gaelic festival marking the end of harvest and the start of winter, when the boundary between this world and the next was believed to thin.',
        'close': 'It was about the year turning, and needing a ritual for the dark half of it.', 'tag': '#samhain'},
}


def text_for(p, hook, body, close, night, tag, title=None):
    t = f"{hook}\n\n{body}\n\n{close}\n\nNight {night} of 33."
    if p == 'instagram':
        return t + "\n\nComment SEASONAL and I'll send you the weekly note."
    if p == 'tiktok':
        return t + f"\n\nFollow for the real one, every night until Halloween. The note is in my bio.\n\n#LearnOnTikTok #halloween {tag}"
    if p == 'facebook':
        return t + f"\n\nComment SEASONAL and I'll send you the weekly note.\n\n{NOTE}"
    return t + f"\n\nSubscribe for the real one, every night until Halloween. The weekly note:\n{NOTE}\n\n#gentlemuse #halloween #shorts"


def central_date(iso):
    t = dt.datetime.fromisoformat(iso.replace('Z', '+00:00')) - dt.timedelta(hours=5)
    return t.date().isoformat()


def main():
    media = json.load(open(os.path.join(HERE, 'weeks', 'media.json'))) if os.path.exists(os.path.join(HERE, 'weeks', 'media.json')) else {}
    queue = json.load(open(os.path.join(HERE, 'backup', 'queue-2026-09-23-full.json')))
    old = {}
    for x in queue:
        c = x['draft']['content']
        if x['id'] in KEEP or x['scheduledAt'] < '2026-09-29':
            continue
        if 'SEASONAL' in c['text'] or '#halloween' in c['text']:
            old.setdefault(central_date(x['scheduledAt']), []).append(x['id'])
    out = []
    for f in sorted(glob.glob(os.path.join(HERE, 'weeks', 'week*-posts.json'))):
        for n in json.load(open(f)):
            plats = ['instagram', 'tiktok'] + (['facebook', 'youtube'] if n['fb_yt'] else [])
            for p in plats:
                if n['slug'] == 'REUSE-samhain' and p in ('instagram', 'tiktok'):
                    continue  # already queued; load.py retimes it
                if n['reused']:
                    r = REPOSTS[n['slug']]
                    text = text_for(p, r['hook'], r['body'], r['close'], n['night'], r['tag'])
                    url = BASE + r['media'][p]
                    title = r['hook'].rstrip('.')
                else:
                    text = n['youtube' if p == 'youtube' else p]
                    url = media.get(n['render'])
                    title = n['title']
                e = dict(key=f"n{n['night']:02d}-{p}", night=n['night'], platform=p, accountId=ACCT[p],
                         scheduledTime=f"{n['date']}T{TIME[p]}:00Z", text=text, mediaUrl=url,
                         replaces=old.get(n['date'], []) if p == 'instagram' else [])
                if p == 'facebook':
                    e.update(pageId=FB_PAGE, mediaType='reel')
                if p == 'instagram':
                    e.update(mediaType='reel', shareToFeed=True)
                if p in ('youtube', 'tiktok'):
                    e['title'] = title[:95]
                out.append(e)
    extras = [
        dict(key='trailer-' + p, night=0, platform=p, accountId=ACCT[p], scheduledTime=f"2026-09-28T{'23:00' if p in ('instagram','tiktok') else '23:30'}:00Z",
             text=("The season sells you fear.\n\nThe real stories are stranger. 1 true thing about this season, every night from tomorrow to Halloween.\n\n33 nights. It starts tomorrow."
                   + {'instagram': "\n\nComment SEASONAL and I'll send you the weekly note.",
                      'tiktok': "\n\nFollow along, every night until Halloween. The note is in my bio.\n\n#LearnOnTikTok #halloween #history",
                      'facebook': f"\n\nComment SEASONAL and I'll send you the weekly note.\n\n{NOTE}",
                      'youtube': f"\n\nSubscribe for the real one, every night until Halloween. The weekly note:\n{NOTE}\n\n#gentlemuse #halloween #shorts"}[p]),
             mediaUrl=BASE + '6e2a688c-ff90-43f1-a8e4-a1a94efc3397.mp4', replaces=[],
             **({'pageId': FB_PAGE, 'mediaType': 'reel'} if p == 'facebook' else {}),
             **({'mediaType': 'reel', 'shareToFeed': True} if p == 'instagram' else {}),
             **({'title': '33 nights. It starts tomorrow'} if p in ('youtube', 'tiktok') else {}))
        for p in ACCT]
    retimes = [dict(key='retime-samhain-ig', id='4137937', scheduledTime='2026-10-31T23:00:00Z'),
               dict(key='retime-samhain-tt', id='4137938', scheduledTime='2026-10-31T23:00:00Z'),
               dict(key='retime-5-nights-ig', id='4459039', scheduledTime='2026-10-27T00:30:00Z'),
               dict(key='retime-5-nights-tt', id='4459043', scheduledTime='2026-10-27T00:30:00Z')]
    json.dump({'posts': extras + out, 'retimes': retimes}, open(os.path.join(HERE, 'schedule.json'), 'w'), indent=1, ensure_ascii=False)
    missing = [e['key'] for e in out if not e['mediaUrl']]
    print(len(extras + out), 'posts,', sum(len(v) for v in old.values()), 'old posts to replace on', len(old), 'dates;',
          len(missing), 'still need media')


if __name__ == '__main__':
    main()
