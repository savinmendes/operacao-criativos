import json,requests,sys,concurrent.futures as cf
from dotenv import dotenv_values
k=dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
key=[v for kk,v in k.items() if 'ELEVEN' in kk.upper()][0]
P={
"A":"Instrumental modern Latin reggaeton / dembow beat at 95 BPM, sensual and elegant luxury-perfume vibe, lush warm synth pads, clean crisp dembow percussion, deep smooth 808 bass, subtle plucked synth motif, glossy high-end production like a trending TikTok background track in Chile. Starts immediately on the full beat with no slow intro, steady energy throughout, no vocals, no lyrics, no vocal chops, original melody.",
"B":"Instrumental Chilean guaracha / aleteo and Latin tech-house at 124 BPM, energetic festive Black Friday party vibe, punchy four-on-the-floor kick, tribal Latin percussion, congas and timbales, bright rolling bassline, short synth stabs and whistle-like lead, high energy club drop feel like a viral TikTok trend in Chile. Starts immediately at full energy with no slow intro, steady groove throughout, no vocals, no lyrics, no vocal chops, original melody.",
"C":"Instrumental light Latin pop / afrobeat at 105 BPM, feminine, joyful and sunny, bouncy afro percussion and shakers, soft marimba and bright guitar plucks, warm bass, airy pads, feel-good trending TikTok background track for a beauty product in Latin America. Starts immediately on the full groove with no slow intro, steady energy throughout, no vocals, no lyrics, no vocal chops, original melody.",
}
json.dump(P,open("prompts.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
def g(n):
    r=requests.post("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192",headers={"xi-api-key":key},
        json={"prompt":P[n],"music_length_ms":52000,"force_instrumental":True},timeout=600)
    if r.status_code!=200: return n,f"ERR {r.status_code} {r.text[:300]}"
    open(f"trilha_{n}.mp3","wb").write(r.content); return n,f"ok {len(r.content)} bytes"
with cf.ThreadPoolExecutor(3) as ex:
    for n,s in ex.map(g,sys.argv[1:] or sorted(P)): print(n,s)
