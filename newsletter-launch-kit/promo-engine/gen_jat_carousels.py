"""Just Another Tuesday carousel sets.

Built 2026-09-24 to Amanda's instruction: JAT carousels have to be as good as the
Consider This ones, and single-image newsletter promos are retired.

Structure is copied slide for slide from carousels/carousel-pillow-*.html so the two
newsletters read as one system: slide 1 hook, slides 2 to 5 numbered beats, slide 6 CTA.
The only deliberate difference is the palette. Consider This runs WARM, Just Another
Tuesday runs COOL, which is the same split the retired single-page promos already used.

Every beat below traces to approved copy in DRAFT_0909_just-another-tuesday-issues-6-10-v1
or to the promo-tuesday page it replaces. Nothing invented.
"""
import subprocess, pathlib

F = "/mnt/skills/examples/canvas-design/canvas-fonts"
OUT = pathlib.Path("/home/user/GentleMuse/newsletter-launch-kit/promo-engine/carousels")

COOL = dict(bg1="#F4F4F2", bg2="#EAEAE6", ink="#262626", muted="#6E6E6E",
            accent="#3F5E52", line="#D5D5CE")

TPL = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:'Lora';src:url('file://{F}/Lora-Regular.ttf');font-weight:400}}
@font-face{{font-family:'Lora';src:url('file://{F}/Lora-Bold.ttf');font-weight:700}}
@font-face{{font-family:'Lora';src:url('file://{F}/Lora-Italic.ttf');font-style:italic}}
@font-face{{font-family:'Gloock';src:url('file://{F}/Gloock-Regular.ttf')}}
@font-face{{font-family:'Jura';src:url('file://{F}/Jura-Light.ttf');font-weight:300}}
@font-face{{font-family:'Jura';src:url('file://{F}/Jura-Medium.ttf');font-weight:500}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{background:{bg2}}}html,body{{width:1080px;height:1350px}}
body{{background:linear-gradient(178deg,{bg1} 0%,{bg2} 100%);color:{ink};font-family:'Lora',serif;-webkit-font-smoothing:antialiased;overflow:hidden}}
.p{{position:absolute;inset:34px;border:1px solid {line};padding:70px 74px;display:flex;flex-direction:column}}
.tag{{font-family:'Jura';font-weight:500;letter-spacing:.36em;font-size:17px;text-transform:uppercase;color:{muted}}}
.acc{{height:2px;background:{accent};width:56px;margin-top:22px}}
.mid{{flex:1;display:flex;flex-direction:column;justify-content:center}}
.hook{{font-weight:700;font-size:72px;line-height:1.14}}
.hook em{{font-style:italic;font-weight:400}}
.body{{font-size:46px;line-height:1.38}}
.body b{{font-weight:700}}
.step{{font-family:'Gloock';color:{accent};font-size:70px;line-height:1;margin-bottom:26px}}
.foot{{display:flex;justify-content:space-between;align-items:center;font-size:15px}}
.sig{{font-style:italic;font-size:24px}}
.pg{{font-family:'Jura';font-weight:300;letter-spacing:.24em;color:{muted};font-size:15px}}
.cta{{font-weight:700;font-size:60px;line-height:1.2}}
.cta span{{color:{accent}}}
.sub{{font-size:30px;line-height:1.4;color:{muted};margin-top:28px}}
</style></head><body><div class="p">
<div class="tag">{tag}</div><div class="acc"></div>
<div class="mid">{mid}</div>
<div class="foot"><div class="pg">{n} / 6</div><div class="sig">The Gentle Muse</div></div>
</div></body></html>"""

CTA_MID = ('<div class="cta">Comment <span>TUESDAY</span></div>'
           '<div class="sub">1 thing I learned the hard way, every Tuesday. Free.</div>')

SETS = [
    dict(slug="jat-enabled", tag="THE AUTOMATIONS",
         hook="6 automations had stopped. <em>All 6 still said enabled.</em>",
         beats=[
             "Every one of them still read enabled in the dashboard.",
             "12 days of my own logging broke and nothing flagged it.",
             "The tool reports what is written in it, not what is running.",
             "Now I open the thing and read it instead of glancing at it.",
         ]),
    dict(slug="jat-number", tag="THE NUMBER",
         hook="I found my number 1 problem. <em>Then ignored it 3 weeks.</em>",
         beats=[
             "The number was zero website clicks, across 4 straight weeks.",
             "I flagged it on day 5. Again on day 18. Again on day 20.",
             "I was not idle. I built 3 spreadsheets and 20 demos instead.",
             "Producing had a finish line. Testing only had a verdict.",
         ]),
    dict(slug="jat-doors", tag="THE 4 DOORS",
         hook="I had 4 front doors. <em>They were all the same door.</em>",
         beats=[
             "4 free offers, 4 keywords, 4 audiences. So the dashboard said.",
             "On day 27 I read it properly. All 4 shared a single rule.",
             "That rule ran on 1 platform, so 3 audiences hit nothing.",
             "It was not lying to me. It was showing what I put in it.",
         ]),
    dict(slug="jat-obedient", tag="THE TAGS",
         hook="The algorithm was not broken. <em>It was obedient.</em>",
         beats=[
             "I opened a freelance lane in June. The leads were bad for weeks.",
             "Wrong work, wrong rates. So I blamed the matching.",
             "Day 25 I read my own profile. Every tag said customer service.",
             "It matched me perfectly to the document I wrote about myself.",
         ]),
    dict(slug="jat-923", tag="THE $9.23",
         hook="I chased down $9.23. <em>It found the real problem.</em>",
         beats=[
             "Monthly audit, and my rule is that no unknown stays unknown.",
             "The $9.23 was interest. I could have rounded it and moved on.",
             "Going line by line is what showed me the month ran a deficit.",
             "A monthly total is the exact shape that hides a timing problem.",
         ]),
    dict(slug="jat-permission", tag="THE STOP",
         hook="My first robot <em>asked permission before it moved.</em>",
         beats=[
             "Day 8. Thousands of files in no order, so I built a sorter.",
             "It hashed every file, caught the duplicates, planned each move.",
             "Then it did nothing at all, because I built it propose only.",
             "It showed me 150 files and waited. The stop is the design.",
         ]),
]

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
made = []
for s in SETS:
    mids = [f'<div class="hook">{s["hook"]}</div>']
    mids += [f'<div class="step">{i+1}</div><div class="body">{b}</div>'
             for i, b in enumerate(s["beats"])]
    mids.append(CTA_MID)
    for i, mid in enumerate(mids, start=1):
        html = TPL.format(F=F, tag=s["tag"], mid=mid, n=i, **COOL)
        hp = OUT / f'carousel-{s["slug"]}-{i:02d}.html'
        pp = OUT / f'carousel-{s["slug"]}-{i:02d}.png'
        hp.write_text(html)
        subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
                        "--hide-scrollbars", "--allow-file-access-from-files",
                        "--window-size=1080,1350", f"--screenshot={pp}", f"file://{hp}"],
                       capture_output=True)
        made.append(str(pp))

for m in made:
    print(m)
