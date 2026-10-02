"""AI Guide carousel sets.

Built 2026-09-24 to Amanda's instruction to hit LinkedIn hard with Just Another Tuesday
and the AI Guide. The AI Guide had no carousel, only the retired single-page
`promo-ai-guide.png`, so it could not be posted under the carousels-only rule.

Structure and type system copied from carousels/carousel-pillow-*.html, same as the JAT
sets. Palette is COOL, which is what the retired AI Guide single-pager already used.

Every beat traces to approved copy in ../launch-content.md (the AI Guide LinkedIn and
Instagram captions) or ../DRAFT_0909_jat-send-day-promo-posts.txt. Nothing invented.

The CTA slide carries no keyword, on purpose. LinkedIn has no comment-to-DM automation, so
the caption carries the link there and the keyword CTA is added in the caption on the
platforms that do have one.
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

CTA_MID = ('<div class="cta"><span>59</span> pages. Free.</div>'
           '<div class="sub">No account. No upsell. No 40 step framework.</div>')

SETS = [
    dict(slug="guide-needed", tag="THE GUIDE",
         hook="I wrote the AI guide <em>I needed 60 days ago.</em>",
         beats=[
             "Everything I found assumed I already knew the vocabulary.",
             "Or it was a 40 step framework built for someone with a team.",
             "I had a shift to work, 1 income, and no idea what an automation was.",
             "So I wrote down what worked, in order, in plain language.",
         ]),
    dict(slug="guide-hours", tag="10 HOURS",
         hook="You do not need to be <em>10 years ahead on AI.</em>",
         beats=[
             "About 10 hours is enough to be genuinely useful with it.",
             "Not 10 hours of theory. 10 hours of trying it on your own work.",
             "You do not need a team, a budget, or the vocabulary first.",
             "You need 10 hours and a record of what broke.",
         ]),
    dict(slug="guide-behind", tag="THE VOCABULARY",
         hook="Most AI advice starts <em>3 steps past you.</em>",
         beats=[
             "It assumes you already know the words before it explains anything.",
             "So the first thing you learn is that you are behind.",
             "You are not behind. The explanation got skipped.",
             "This one starts at the beginning and stays in plain language.",
         ]),
    dict(slug="guide-explorer", tag="THE WORD",
         hook="I stopped calling myself <em>an AI expert.</em>",
         beats=[
             "The word fit like someone else's coat, so I put it down.",
             "Explorer fits. I am writing it down while I am still learning it.",
             "Come find out with me beats I already know.",
             "That is who this guide is written by, and who it is written for.",
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
