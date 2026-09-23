"""Build 1 week of the 33 Nights countdown: reel payloads and captions.

  python3 build_week.py 1 --plates DIR      writes week1-reels.json and week1-posts.json

Reads ../approval/plan.json (the approved order) and beats.json (on-screen text).
Reposted nights (Goosebumps, turnips, Samhain) carry no render; their existing
media is filled in by hand in week<N>-posts.json.
"""
import json, os, sys, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
TIMES = [(0.0, 3.2), (3.2, 7.6), (7.6, 12.4), (12.4, 15.4), (15.4, 17.8)]
TAGS = {'folklore': '#history', 'words': '#etymology', 'science': '#science', 'nature': '#nature', 'nostalgia': '#nostalgia'}
NOTE = 'https://consider-this.subscribepage.io'
SAFE_IMG = {}


def captions(n):
    body = f"{n['hook']}\n\n{n['fact']}\n\n{n['backbone']}\n\nNight {n['night']} of 33."
    return {
        'instagram': body + "\n\nComment SEASONAL and I'll send you the weekly note.",
        'tiktok': body + f"\n\nFollow for the real one, every night until Halloween. The note is in my bio.\n\n#LearnOnTikTok #halloween {TAGS[n['lane']]}",
        'facebook': body + f"\n\nComment SEASONAL and I'll send you the weekly note.\n\n{NOTE}",
        'youtube': body + f"\n\nSubscribe for the real one, every night until Halloween. The weekly note:\n{NOTE}\n\n#gentlemuse #halloween #shorts",
        'title': n['hook'].rstrip('.'),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('week', type=int)
    a = ap.parse_args()
    plan = json.load(open(os.path.join(HERE, '..', 'approval', 'plan.json')))
    beats = json.load(open(os.path.join(HERE, 'beats.json')))
    nights = plan[(a.week - 1) * 7: a.week * 7]
    reels, posts = [], []
    for n in nights:
        entry = dict(night=n['night'], date=n['date'], slug=n['slug'], fb_yt=bool(n['fb_yt']), reused=n['reused'])
        if not n['reused']:
            b = beats[n['slug']]
            img = f"plates/{n['plate']}" if n['plate'] else f"plates/new-{n['slug']}.jpg"
            reels.append({
                'id': f"N{n['night']:02d}", 'slug': f"n{n['night']:02d}-{n['slug']}", 'seed': 100 + n['night'],
                'duration': 18.0, 'label': f"Gentle Muse · Night {n['night']} of 33",
                'source': f"Source: {b['src']}",
                'contract': 'Every holiday carries a fact somebody softened. I post the real one before the day arrives.',
                'delivery': 'text', 'keyword': 'SEASONAL',
                'beats': [{'in': t[0], 'out': t[1], 'html': (f"<span class='em'>{h}</span>" if i == 3 else h), 'cta': None}
                          for i, (t, h) in enumerate(zip(TIMES, b['beats']))],
                'clip': {'file': img, 'push': 0.07, 'clip_id': os.path.basename(img)[:-4], 'match_reason': n.get('plate_desc') or n.get('new_image')},
            })
            entry.update(captions(n), render=f"GM-n{n['night']:02d}-{n['slug']}.mp4")
        posts.append(entry)
    json.dump(reels, open(os.path.join(HERE, f'week{a.week}-reels.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump(posts, open(os.path.join(HERE, f'week{a.week}-posts.json'), 'w'), indent=1, ensure_ascii=False)
    print(len(reels), 'reels,', len(posts), 'nights')


if __name__ == '__main__':
    main()
