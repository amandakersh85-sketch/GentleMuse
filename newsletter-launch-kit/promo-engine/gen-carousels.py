import subprocess, os
F="/root/.claude/skills/synced/canvas-design/canvas-fonts"
OUT="/home/user/GentleMuse/newsletter-launch-kit/promo-engine/carousels"
os.makedirs(OUT, exist_ok=True)
W=dict(bg1="#F6F1E6",bg2="#F1E9D8",ink="#2B2620",muted="#7C7061",accent="#B0674C",line="#D9CFBD")

BASE="""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
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
<div class="foot"><div class="pg">{pg}</div><div class="sig">The Gentle Muse</div></div>
</div></body></html>"""

def hook(t): return f'<div class="hook">{t}</div>'
def step(n,t): return f'<div class="step">{n}</div><div class="body">{t}</div>'
def cta(t,s): return f'<div class="cta">{t}</div><div class="sub">{s}</div>'

SETS=[
 ("sponge","THE SPONGE",[
  hook('Microwaving your sponge <em>isn&rsquo;t sanitizing it.</em>'),
  step(1,'It kills some bacteria. The ones that survive are the tough ones.'),
  step(2,'You&rsquo;re left with a smaller, hardier population. Not a clean sponge.'),
  step(3,'Researchers who sampled used sponges found the regularly cleaned ones were no less contaminated.'),
  step(4,'Replace it weekly. Or switch to a brush that dries out between uses.'),
  cta('Comment <span>CONSIDER</span>','1 overlooked thing in your home, every week. Free.')]),
 ("duct","THE DRYER","""""".join and [
  hook('Your lint screen is clean. <em>The duct behind it isn&rsquo;t.</em>'),
  step(1,'The screen catches most lint. Most is not all.'),
  step(2,'What slips past builds up in the duct, where you can&rsquo;t see it.'),
  step(3,'Restricted airflow means longer dry times, and lint is flammable.'),
  step(4,'Check it once a year. Longer dry times are the first warning.'),
  cta('Comment <span>CONSIDER</span>','1 overlooked thing in your home, every week. Free.')]),
 ("filter","THE FURNACE FILTER",[
  hook('The highest-rated filter <em>might be the wrong one.</em>'),
  step(1,'A higher rating catches finer particles. It also restricts airflow.'),
  step(2,'Most home systems are built for a specific range, not the maximum.'),
  step(3,'Too restrictive and the blower strains. That shortens the system&rsquo;s life.'),
  step(4,'Check the manual for the range yours was designed for. Then buy that.'),
  cta('Comment <span>CONSIDER</span>','1 overlooked thing in your home, every week. Free.')]),
 ("gasket","THE WASHER",[
  hook('The part of your washer <em>that never gets clean.</em>'),
  step(1,'Front loaders have a rubber gasket that holds water after every cycle.'),
  step(2,'Dark, damp, sealed shut. That is where the smell actually comes from.'),
  step(3,'Peel it back and look. That fold is the part nobody wipes.'),
  step(4,'Dry it after the last load. Leave the door open between washes.'),
  cta('Comment <span>CONSIDER</span>','1 overlooked thing in your home, every week. Free.')]),
 ("towels","THE TOWELS",[
  hook('Your towels aren&rsquo;t old. <em>They&rsquo;re coated.</em>'),
  step(1,'Fabric softener leaves a film behind. That film is what feels soft.'),
  step(2,'It also repels water, which is the opposite of a towel&rsquo;s job.'),
  step(3,'It builds up over months, so it feels like the towel simply wore out.'),
  step(4,'Wash them hot with vinegar, no softener. They come back.'),
  cta('Comment <span>CONSIDER</span>','1 overlooked thing in your home, every week. Free.')]),
 ("pillow","THE PILLOW",[
  hook('Your pillow <em>has an expiration date.</em>'),
  step(1,'It absorbs oil, sweat and skin every night for years.'),
  step(2,'The fill compresses, so it stops holding your neck where it should be.'),
  step(3,'Fold it in half. If it stays folded instead of springing back, it is done.'),
  step(4,'Most last 1 to 2 years. A protector buys time, not forever.'),
  cta('Comment <span>CONSIDER</span>','1 overlooked thing in your home, every week. Free.')]),
]
CHROME="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
made=[]
for name,tag,slides in SETS:
    for i,mid in enumerate(slides,1):
        pg=f"{i} / {len(slides)}"
        html=BASE.format(F=F,tag=tag,mid=mid,pg=pg,**W)
        hp=f"{OUT}/carousel-{name}-{i:02d}.html"; pp=f"{OUT}/carousel-{name}-{i:02d}.png"
        open(hp,'w').write(html)
        subprocess.run([CHROME,"--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars",
          "--allow-file-access-from-files","--force-device-scale-factor=1","--window-size=1080,1350",
          f"--screenshot={pp}",f"file://{hp}"],capture_output=True)
        made.append(pp)
print(f"rendered {len(made)} slides")
