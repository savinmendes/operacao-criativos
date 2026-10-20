import os,requests
from dotenv import dotenv_values
k=dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
key=[v for kk,v in k.items() if 'ELEVEN' in kk.upper()][0]
r=requests.get("https://api.elevenlabs.io/v1/user/subscription",headers={"xi-api-key":key}).json()
print({x:r.get(x) for x in ["tier","character_count","character_limit","next_character_count_reset_unix","status"]})
