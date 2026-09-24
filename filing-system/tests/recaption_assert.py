#!/usr/bin/env python3
"""
A caption reused on another channel arrives carrying the old channel's ask.

gm_fill_plan copies a caption from whichever channel last ran the fact. The
body travels, because the fact is true everywhere. The ask does not, because
it is a property of where the post lands: Instagram and Facebook have a
listener for the keyword, TikTok and YouTube have none, and a keyword nobody
answers is worse than no ask at all.

On 09/11 the plan proposed 2 YouTube fills carrying "Comment SEASONAL",
straight after 20 posts with that exact defect had been fixed by hand. The
generator would have put it back every night.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "scripts"))
import gm_fill_plan as F

fails = []


def want(cond, msg):
    if not cond:
        fails.append(msg)


cta = F.load_cta_lines()
src = ("Jack o lanterns were turnips.\n\n"
       "Ireland and Scotland carved them for centuries.\n\n"
       "The ritual mattered. The turnip did not.\n\n"
       "Comment SEASONAL and I'll send you the weekly note.\n\n"
       "https://consider-this.subscribepage.io")

yt = F.recaption(src, "youtube", "36129", cta)
tt = F.recaption(src, "tiktok", "41488", cta)
fb = F.recaption(src, "facebook", "30840", cta)
ig = F.recaption(src, "instagram", "45886", cta)

want("Comment SEASONAL" not in yt, "youtube kept a keyword it cannot answer")
want("Subscribe for the real one" in yt, "youtube did not get its own ask")
want("#gentlemuse" in yt, "youtube did not get its own hashtags")
want("The weekly note:\nhttps://" in yt,
     "the link did not follow the colon on the next line")

want("Comment SEASONAL" not in tt, "tiktok kept a keyword it cannot answer")
want("in my bio" in tt, "tiktok did not get the bio ask")
want("http" not in tt, "tiktok got a URL, which is not tappable there")

want("Comment SEASONAL" in fb, "facebook lost the keyword it does answer")
want("https://consider-this.subscribepage.io" in fb,
     "facebook lost the link, which is clickable there")

want("Comment SEASONAL" in ig, "instagram lost the keyword it does answer")
want("http" not in ig,
     "instagram got a URL, which is not clickable there")

# The body is the part that travels.
for name, out in (("youtube", yt), ("tiktok", tt), ("facebook", fb)):
    want("The ritual mattered." in out,
         "%s lost the body during the rewrite" % name)
    want("Jack o lanterns were turnips." in out,
         "%s lost the opening line" % name)

# No substitution. A channel with no recorded ask does not get one invented,
# and it does not get another channel's either.
want(F.recaption(src, "twitter", "21430", cta) is None,
     "a channel with no recorded ask got one invented for it")

if fails:
    for f in fails:
        print("  " + f)
    sys.exit(1)
print("  recaption: 4 channels re-asked, 1 unknown channel refused")
sys.exit(0)
