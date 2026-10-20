# -*- coding: utf-8 -*-
"""Abre posts públicos do Facebook num Chrome invisível e captura a URL do vídeo em HD
(browser_native_hd_url / playable_url_quality_hd / hd_src) no HTML e nas respostas de rede.
Uso: python fb_post_hd.py lista.txt saida.json   (lista: "PASTA url" por linha)"""
import json, re, sys, time
from playwright.sync_api import sync_playwright

PADROES = [r'"browser_native_hd_url":"(https:[^"]+)"', r'"playable_url_quality_hd":"(https:[^"]+)"',
           r'"hd_src(?:_no_ratelimit)?":"(https:[^"]+)"']
PADROES_SD = [r'"browser_native_sd_url":"(https:[^"]+)"', r'"playable_url":"(https:[^"]+)"', r'"sd_src(?:_no_ratelimit)?":"(https:[^"]+)"']

def limpar(u):
    return u.encode().decode('unicode_escape').replace('\\/', '/') if '\\' in u else u

def extrair(texto, achado):
    for pad in PADROES:
        for u in re.findall(pad, texto):
            u = limpar(u)
            if u not in achado['hd']:
                achado['hd'].append(u)
    for pad in PADROES_SD:
        for u in re.findall(pad, texto):
            u = limpar(u)
            if u not in achado['sd']:
                achado['sd'].append(u)

linhas = [l.split(None, 1) for l in open(sys.argv[1], encoding='utf-8') if l.strip()]
saida = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for pasta, url in linhas:
        url = url.strip()
        achado = {'pasta': pasta, 'hd': [], 'sd': [], 'mp4_rede': []}
        pg = b.new_page(locale="es-ES", viewport={"width": 1280, "height": 1000})
        def on_resp(r, achado=achado):
            try:
                if 'video' in r.url and '.mp4' in r.url and r.url.split('&bytestart')[0] not in achado['mp4_rede']:
                    achado['mp4_rede'].append(r.url.split('&bytestart')[0])
                if 'graphql' in r.url or 'facebook.com' in r.url:
                    extrair(r.text(), achado)
            except Exception:
                pass
        pg.on("response", on_resp)
        try:
            pg.goto(url, wait_until="domcontentloaded", timeout=90000)
            time.sleep(6)
            extrair(pg.content(), achado)
            for _ in range(4):
                pg.mouse.wheel(0, 1500); time.sleep(1.5)
            extrair(pg.content(), achado)
        except Exception as e:
            achado['erro'] = str(e)[:120]
        pg.close()
        saida[url] = achado
        print(pasta, url.rsplit('/', 2)[-2], 'HD:', len(achado['hd']), 'SD:', len(achado['sd']), 'rede:', len(achado['mp4_rede']))
    b.close()
json.dump(saida, open(sys.argv[2], 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
