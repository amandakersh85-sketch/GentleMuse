import subprocess, pathlib
F="/root/.claude/skills/synced/canvas-design/canvas-fonts"
TPL = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:'Lora';src:url('file://{F}/Lora-Regular.ttf');font-weight:400}}
@font-face{{font-family:'Lora';src:url('file://{F}/Lora-Bold.ttf');font-weight:700}}
@font-face{{font-family:'Lora';src:url('file://{F}/Lora-Italic.ttf');font-style:italic}}
@font-face{{font-family:'Gloock';src:url('file://{F}/Gloock-Regular.ttf')}}
@font-face{{font-family:'Jura';src:url('file://{F}/Jura-Light.ttf');font-weight:300}}
@font-face{{font-family:'Jura';src:url('file://{F}/Jura-Medium.ttf');font-weight:500}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{background:{bg2}}}
html,body{{width:1080px;height:1350px}}
body{{background:linear-gradient(178deg,{bg1} 0%,{bg2} 100%);color:{ink};font-family:'Lora',serif;-webkit-font-smoothing:antialiased;overflow:hidden}}
.page{{position:absolute;inset:34px;border:1px solid {line};padding:60px 70px 56px;display:flex;flex-direction:column}}
.mast{{display:flex;justify-content:space-between;align-items:baseline}}
.brand{{font-family:'Jura';font-weight:500;letter-spacing:.42em;font-size:20px;text-transform:uppercase}}
.idx{{font-family:'Jura';font-weight:300;letter-spacing:.28em;font-size:15px;color:{muted};text-transform:uppercase}}
.kick{{font-family:'Jura';font-weight:300;letter-spacing:.30em;font-size:15px;color:{muted};text-transform:uppercase;margin-top:12px}}
.rule{{height:2px;background:{accent};width:56px;margin-top:24px}}
.head{{font-family:'Lora';font-weight:700;font-size:{hs}px;line-height:1.16;margin-top:30px}}
.head em{{font-style:italic;font-weight:400}}
.head .n{{font-family:'Gloock';color:{accent};font-size:{hs2}px}}
.list{{margin-top:20px;flex:1;display:flex;flex-direction:column;justify-content:center}}
.item{{display:flex;gap:26px;padding:20px 0;border-top:1px solid {line}}}
.item:last-child{{border-bottom:1px solid {line}}}
.num{{font-family:'Gloock';color:{accent};font-size:38px;line-height:1;width:44px;flex:none;padding-top:2px}}
.txt{{font-size:28px;line-height:1.34}}
.foot{{display:flex;justify-content:space-between;align-items:center;margin-top:30px}}
.cta{{font-family:'Jura';font-weight:500;letter-spacing:.22em;font-size:17px;color:{accent};text-transform:uppercase}}
.sig{{font-style:italic;font-size:26px}}
</style></head><body><div class="page">
<div class="mast"><div class="brand">{brand}</div><div class="idx">{idx}</div></div>
<div class="kick">{kick}</div><div class="rule"></div>
<div class="head">{head}</div>
<div class="list">{items}</div>
<div class="foot"><div class="cta">{cta}</div><div class="sig">The Gentle Muse</div></div>
</div></body></html>"""

WARM = dict(bg1="#F6F1E6", bg2="#F1E9D8", ink="#2B2620", muted="#7C7061", accent="#B0674C", line="#D9CFBD")
COOL = dict(bg1="#F4F4F2", bg2="#EAEAE6", ink="#262626", muted="#6E6E6E", accent="#3F5E52", line="#D5D5CE")

def items(rows):
    return "".join('<div class="item"><div class="num">%d</div><div class="txt">%s</div></div>' % (i+1, t) for i, t in enumerate(rows))

SPECS = [
 dict(name="promo-ai-guide", pal=COOL, brand="THE AI GUIDE", idx="59 PAGES", kick="Free &middot; no account needed",
   head='<span class="n">10</span> hours ahead is enough.', hs=54, hs2=60,
   items=items(["You don&rsquo;t need to know the vocabulary first.",
                "You don&rsquo;t need a team, or a budget.",
                "You need 10 hours and a record of what broke.",
                "That&rsquo;s the whole guide. 59 pages of it."]),
   cta="Free &middot; Link in bio"),
 dict(name="promo-reset-guide", pal=WARM, brand="THE RESET GUIDE", idx="FREE", kick="For the weeks that got heavy",
   head='I had <span class="n">13</span> tabs open and <em>no idea where to start.</em>', hs=50, hs2=56,
   items=items(["A notebook full of half-finished plans.",
                "Files named things I could no longer decode.",
                "Not disorganized. Carrying too much at once.",
                "Pick 1 line from the checklist. Do that one."]),
   cta="Free &middot; Link in bio"),
 dict(name="promo-tuesday", pal=COOL, brand="JUST ANOTHER TUESDAY", idx="WEEKLY", kick="1 lesson &middot; every Tuesday",
   head='<span class="n">6</span> automations I trusted had <em>quietly stopped.</em>', hs=50, hs2=56,
   items=items(["Every one of them still said enabled.",
                "12 days of my logging broke unnoticed.",
                "My own notes caught it. I didn&rsquo;t.",
                "1 thing I learned the hard way, weekly."]),
   cta="Free &middot; Link in bio"),
]

out=[]
for s in SPECS:
    html = TPL.format(F=F, brand=s["brand"], idx=s["idx"], kick=s["kick"], head=s["head"],
                      hs=s["hs"], hs2=s["hs2"], items=s["items"], cta=s["cta"], **s["pal"])
    hp = f'/home/user/GentleMuse/newsletter-launch-kit/promo-engine/{s["name"]}.html'
    pp = f'/home/user/GentleMuse/newsletter-launch-kit/promo-engine/{s["name"]}.png'
    open(hp,'w').write(html)
    subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome","--headless=new","--no-sandbox",
      "--disable-gpu","--hide-scrollbars","--allow-file-access-from-files","--force-device-scale-factor=2",
      "--window-size=1080,1350",f"--screenshot={pp}",f"file://{hp}"],capture_output=True)
    out.append(pp)
for o in out: print(o)
