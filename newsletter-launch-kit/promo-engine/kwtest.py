# Real audience comments, 7-day window, both IG accounts. Verbatim from blotato_list_comments.
Q, N = "QUALIFIED", "noise"
comments = [
 ("4172237","cesa",Q,"They get to pee wherever they want when they're old 😂 I tried to get mine to go outside but he wouldn't make it sometimes. It's an honor to clean it up after all those years together."),
 ("4103323","cesa",Q,"Omg, she's so happy! 🥹 My 18 year old Chiweenie can still walk,  but is losing her vision and bumping into things. I miss seeing her hopping around like your Cesla."),
 ("3690124","cesa",Q,"What's your secret?! She looks so healthy!!"),
 ("3667740","cesa",Q,"Wow 19!! I hope little doggie lives this long if it can still do walkies"),
 ("3832450","main",Q,"Nothing like it mine is 15 and its like that everyday I come home ❤️"),
 ("3791926","cesa","KEYWORD","Cesa please"),
 ("3863905","cesa",N,"😍😍😍😍😍😍😍😍😍😍"),
 ("3813284","cesa","SPAM","So beautiful ❤️ let's team up ❤️❤️❤️"),
 ("3715348","cesa",N,"She looks amazing!"),
 ("3650212","cesa",N,"Cutie pie xxx enjoy your walks lovely girl"),
 ("3624952","cesa",N,"Bless her xx"),
 ("4087312","main",N,"❤️"),
 ("3763687","main",N,"So happy😍😍😍"),
 ("3758983","main","SPAM","Você gostaria de conversar comigo agora? Venha para o chat privado."),
 ("3747133","main",N,"Work it girl ❤️"),
 ("3742357","main",N,"Beautiful"),
 ("3685258","main",N,"😍😍😍😍"),
 ("3683482","main",N,"How super sweet ❣️🥰💖🩷🐾"),
 ("3680369","main",N,"Precious"),
 ("3677465","main",N,"Awwwww...so sweet! 😍"),
 ("3659384","main",N,"Such a beautiful dog ❤️"),
 ("3636647","main",N,"😂😂😂😂❤️❤️❤️❤️❤️❤️❤️"),
 ("3629569","main",N,"So happy mom's home. 😍❤️❤️❤️ . I love you my friend thank you for sharing this 😍😍😍😍"),
 ("3627526","main",N,"19 wow!!!"),
 ("3605505","main",N,"😍😍😍😍😍😍😍😍"),
]
# Case-sensitive substring, exactly how Blotato matches. Casing variants included per the standing rule.
KW = ["your secret","Your secret","YOUR SECRET",
      "her secret","Her secret",
      "mine is","Mine is","mine was","Mine was",
      "get mine","got mine","Get mine",
      "year old","Year old","years old","Years old","yr old","yrs old",
      "still walk","Still walk","still walks",
      "walkies","Walkies",
      "how old","How old","HOW OLD",
      "my dog","My dog","my girl","My girl","my boy","My boy",
      "senior dog","Senior dog","senior pup"]

def fires(t): return [k for k in KW if k in t]

hit_q = miss_q = fp = 0
print(f"{'id':>8} {'acct':<5} {'truth':<9} {'fires':<6} matched")
print("-"*84)
for cid, acct, truth, txt in comments:
    m = fires(txt)
    f = "YES" if m else "no"
    if truth == Q:
        if m: hit_q += 1
        else: miss_q += 1
    elif truth in (N,"SPAM") and m:
        fp += 1
    print(f"{cid:>8} {acct:<5} {truth:<9} {f:<6} {', '.join(m) if m else ''}")
print("-"*84)
tot_q = sum(1 for c in comments if c[2]==Q)
noise = sum(1 for c in comments if c[2] in (N,"SPAM"))
print(f"qualified caught : {hit_q}/{tot_q}")
print(f"qualified missed : {miss_q}/{tot_q}")
print(f"false positives  : {fp}/{noise} noise+spam comments")
