CAND = [" chi ", " Chi ", " CHI ", " chi.", " Chi.", " chi,", " chi!", " chi?"]
# If Blotato TRIMS keyword whitespace, " chi " degrades to "chi". Test that too.
TRIMMED = ["chi", "Chi", "CHI"]

TARGET = "@cesasgoldenyears gives me hope for my healthy chi that's about to turn 9 ❤️💪"

# Real qualified + noise corpus, plus words that would break a trimmed keyword.
CORPUS = [
 ("QUAL", "@cesasgoldenyears gives me hope for my healthy chi that's about to turn 9 ❤️💪"),
 ("QUAL", "Reminds me of my recently passed chi! Every morning I'd get scared when I went to Check on him 😢"),
 ("QUAL", "my old chi is 16"),
 ("QUAL", "I love your chi"),
 ("QUAL", "she's a beautiful chi."),
 ("noise", "😍😍😍😍😍😍😍😍😍😍"),
 ("noise", "She looks amazing!"),
 ("noise", "Cutie pie xxx enjoy your walks lovely girl"),
 ("noise", "Bless her xx"),
 ("noise", "Such a beautiful dog ❤️"),
 ("noise", "So happy mom's home. 😍❤️❤️❤️"),
 ("noise", "19 wow!!!"),
 ("noise", "Chihuahuas never forget meals! even with demitia my baby had to have his foods😍"),
 ("noise", "my Chihuahua is the sweetest"),
 ("noise", "She eats chicken and rice"),
 ("noise", "my chicken recipe is better"),
 ("noise", "my children love her"),
 ("noise", "I'm in Chicago this week"),
 ("noise", "she looks so chill"),
 ("noise", "gnocchi night here"),
 ("noise", "that chip on her shoulder 😂"),
 ("noise", "we do tai chi in the mornings"),
]
def hits(t, kw): return [k for k in kw if k in t]

for label, kws in (("PROPOSED (spaces preserved)", CAND), ("IF BLOTATO TRIMS to bare 'chi'", TRIMMED)):
    tp = fp = 0; fps = []
    print(f"\n=== {label} ===")
    for truth, txt in CORPUS:
        m = hits(txt, kws)
        if truth == "QUAL" and m: tp += 1
        if truth == "noise" and m: fp += 1; fps.append((m, txt))
    q = sum(1 for c in CORPUS if c[0]=="QUAL"); n = sum(1 for c in CORPUS if c[0]=="noise")
    print(f"  qualified caught: {tp}/{q}")
    print(f"  FALSE POSITIVES : {fp}/{n}")
    for m, t in fps: print(f"     !! {m} <- {t}")
    print(f"  target comment  : {'HIT' if hits(TARGET, kws) else 'MISS'}")
