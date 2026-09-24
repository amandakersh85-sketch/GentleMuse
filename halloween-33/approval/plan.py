"""Build plan.json: the 33-night Halloween countdown, Sep 29 to Oct 31.
Run: python3 plan.py  (writes plan.json next to this file)"""
import json, datetime, pathlib, re
HERE = pathlib.Path(__file__).parent
facts = {}
for f in ['batch-folklore', 'batch-words-science-nature', 'batch-nostalgia']:
    for x in json.load(open(HERE.parent / 'facts' / f'{f}.json')):
        facts[x['slug']] = x

P = {  # plate key -> (thumbnail file, what it shows)
 'bedroom': ('mare-nightma-804338b6.jpg', 'bedroom by candlelight'),
 'porch': ('trackA-porch.jpg', 'lit porch, candy bowl'),
 'doorway': ('trickortreat-326e2898.jpg', 'open doorway, lantern'),
 'library': ('goosebumps-ea746655.jpg', 'paperback rack, green lamp'),
 'moon': ('nightmare-be-659ed73b.jpg', 'full moon, bare tree'),
 'radio': ('trackA-radio.jpg', 'old radio, armchair'),
 'staircase': ('casper-c4d2ca45.jpg', 'grand staircase, empty house'),
 'theater': ('nightmare-be-c515317f.jpg', 'empty theater'),
 'field': ('trackA-salem.jpg', 'field at dusk'),
 'press': ('trackA-press.jpg', 'print shop, 1 candle'),
 'nightstand': ('mare-nightma-997ba4ff.jpg', 'candle on a nightstand'),
 'rocking': ('mare-nightma-d0141171.jpg', 'rocking chair, empty room'),
 'livingroom': ('snick-7c6dbfec.jpg', 'living room, old TV'),
 'desk': ('trackA-shelley.jpg', 'candle, open book, window'),
 'fourposter': ('mare-nightma-9df21ca1.jpg', 'four-poster bed'),
 'campfire': ('afraidark-d2e115f7.jpg', 'campfire in the woods'),
 'moordoor': ('countdown-door-clean.jpg', 'stone doorway, raven'),
 'cemetery': ('nightmare-be-ab9dee9d.jpg', 'cemetery gate in fog'),
 'goosebumps': ('goosebumps-df7810a2.jpg', 'existing reel'),
 'turnip': ('turnip-2fc8b92d.jpg', 'existing reel'),
 'samhain': ('samhain-48be37e1.jpg', 'existing reel'),
}
REUSED = {
 'REUSE-goosebumps': dict(lane='nostalgia', hook='Goosebumps, the series that ran the book fair.',
     note='Your best Halloween post: over 2,000 views on TikTok. Reposted once, mid-run.'),
 'REUSE-turnips': dict(lane='folklore', hook='The first jack-o-lanterns were turnips.',
     note='Top Facebook Halloween reel: 470 and 246 views. Reposted once.'),
 'REUSE-samhain': dict(lane='folklore', hook='Samhain: the night the year turns.',
     note='Already scheduled for Oct 31 on Instagram and TikTok. Stays as the finale.'),
}
ORDER = [  # (slug, plate or None for a new image)
 ('halloween-saints-eve', 'bedroom'), ('great-pumpkin-candy-mail', 'porch'),
 ('leaves-hidden-yellow', None), ('guising-scotland-ireland', 'doorway'),
 ('ghostbusters-library', 'library'), ('werewolf-man-wolf', 'moon'),
 ('apple-bobbing-courtship', None), ('monster-mash-banned-bbc', 'radio'),
 ('fear-sweet-spot', 'staircase'), ('candy-corn-1880s', None),
 ('myers-mask-captain-kirk', 'theater'), ('owl-silent-feathers', 'field'),
 ('mischief-night-1790', 'press'), ('scary-stories-most-challenged', 'nightstand'),
 ('haunt-to-visit-often', 'rocking'), ('anoka-1920', None),
 ('REUSE-goosebumps', 'goosebumps'), ('pumpkin-ancient-fruit', None),
 ('wwii-sugar-rationing', 'radio'), ('thriller-film-registry', 'livingroom'),
 ('pareidolia-male-faces', None), ('burns-halloween-poem', 'desk'),
 ('halloween-shot-in-spring', None), ('goosebumps-fur-reflex', 'fourposter'),
 ('blair-witch-missing-flyers', None), ('REUSE-turnips', 'turnip'),
 ('bonfire-bone-fire', 'campfire'), ('treehouse-raven', 'moordoor'),
 ('soul-cakes-souling', 'porch'), ('practical-magic-hollow-house', 'staircase'),
 ('dia-de-muertos-roots', None), ('all-souls-odilo', 'cemetery'),
 ('REUSE-samhain', 'samhain'),
]
assert len(ORDER) == 33
new = [s for s, _ in ORDER if not s.startswith('REUSE')]
assert len(new) == 30 and set(new) == set(facts), 'every new fact used exactly once'

def sources(s):
    out = []
    for part in s.split(' ; '):
        m = re.match(r'(.*?):\s*(https?://\S+)', part.strip())
        out.append({'name': m.group(1), 'url': m.group(2)} if m else {'name': part, 'url': None})
    return out

nights, start = [], datetime.date(2026, 9, 29)
for i, (slug, plate) in enumerate(ORDER):
    n, d = i + 1, start + datetime.timedelta(days=i)
    row = dict(night=n, date=d.isoformat(), slug=slug, left=33 - n,
               ig_tt='23:00Z', fb_yt='23:30Z' if n % 2 == 1 else None)
    if slug.startswith('REUSE'):
        row.update(REUSED[slug], reused=True)
    else:
        f = facts[slug]
        row.update(lane=f['lane'], hook=f['hook'], fact=f['fact'], backbone=f['backbone'],
                   quote=f['quote'], confidence=f['confidence'], sources=sources(f['source']),
                   reused=False)
    if plate:
        row['plate'], row['plate_desc'] = P[plate]
    else:
        row['plate'], row['new_image'] = None, facts[slug]['visual']
    nights.append(row)

# no plate twice within 5 nights
last = {}
for r in nights:
    if r['plate']:
        assert r['night'] - last.get(r['plate'], -99) > 5, r
        last[r['plate']] = r['night']
json.dump(nights, open(HERE / 'plan.json', 'w'), indent=1)
print(len(nights), 'nights;', sum(1 for r in nights if r['plate'] is None), 'new images;',
      sum(1 for r in nights if r['fb_yt']), 'FB/YT nights')
