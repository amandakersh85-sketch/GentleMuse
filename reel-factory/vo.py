import json, os, re, subprocess, sys
D = sys.argv[1]; TTS = sys.argv[2]
reels = json.load(open(os.path.join(D, "reels.json")))
strip = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()
plan = []
for r in reels:
    outdir = os.path.join(D, "vo", r["id"]); os.makedirs(outdir, exist_ok=True)
    for i, b in enumerate(r["beats"]):
        text = strip(b["html"])
        wav = os.path.join(outdir, "b%d.wav" % i)
        if not os.path.exists(wav):
            subprocess.run([TTS, "tts", text, "-v", "af_heart", "-s", "0.92", "-o", wav],
                           check=True, capture_output=True)
        import wave
        with wave.open(wav) as w: dur = w.getnframes() / w.getframerate()
        room = b["out"] - b["in"]
        plan.append((r["id"], i, round(dur,2), round(room,2), "OK" if dur <= room - 0.15 else "TIGHT", text[:44]))
print("%-9s %3s %6s %6s %-5s %s" % ("reel","#","speech","room","fit","line"))
for p in plan: print("%-9s %3d %6.2f %6.2f %-5s %s" % p)
tight = [p for p in plan if p[4] == "TIGHT"]
print("\n%d of %d beats are tight" % (len(tight), len(plan)))
