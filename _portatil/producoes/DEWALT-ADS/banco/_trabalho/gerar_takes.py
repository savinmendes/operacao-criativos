# -*- coding: utf-8 -*-
"""Lista dos takes -> takes.json (entrada do cortar_takes.py e base do indice.json)."""
import json
L21 = "upscale 2x Real-ESRGAN + LaMa: legenda PT branca e logo Tork"
L41 = "upscale 2x Real-ESRGAN + LaMa: legenda PT amarela"
L37 = "upscale 2x Real-ESRGAN + LaMa: titulos PT"
L37N = "upscale 2x Real-ESRGAN (trecho sem texto)"
L38 = "upscale 2x Real-ESRGAN + recorte 576x1130 -> 9:16 (sem texto)"
L30 = "upscale 2x Real-ESRGAN (sem texto)"
L40 = "upscale 2x Real-ESRGAN + LaMa: setas animadas vermelha/amarela"
F = {"21": "limpo/21.mp4", "41": "limpo/41.mp4", "37": "limpo/37.mp4", "38": "up/38.mp4", "30": "up/30.mp4", "40": "limpo/40s.mp4"}
OFF = {"40": 24.0}
# (acao, ad, ini, fim, limpeza, obs[, velocidade])
R = [
 ("caixa", "41", 0.2, 2.3, L41, "Frente da caixa do kit (texto da caixa em ES/PT: 'juego de taladro percutor / atornillador')"),
 ("caixa", "41", 4.0, 5.8, L41, "Caixa em close: DEWALT + '20V brushless' + DCD7781D2"),
 ("caixa", "21", 1.0, 2.35, L21, "Caixa amarela 20V brushless no deposito, camera passando"),
 ("caixa", "21", 3.95, 5.25, L21, "Caixa (lado com selo UN3481 e 20V brushless)"),
 ("maleta", "41", 5.95, 7.15, L41, "Maleta DEWALT fechada -> abre rapido (fim ja mostra o kit dentro)"),
 ("maleta", "21", 6.6, 8.7, L21, "Maleta DEWALT fechada em pe, mao entra no fim"),
 ("maleta", "40", 0.6, 1.9, L40, "Tampa da maleta DEWALT (obra, piso de cimento), mao abrindo"),
 ("kit_completo", "41", 7.4, 9.6, L41, "Maleta aberta: taladro + bateria + carregador"),
 ("kit_completo", "41", 10.1, 12.0, L41, "Taladro com bateria encaixado na maleta (close)"),
 ("kit_completo", "41", 12.1, 13.4, L41, "Carregador + 2a bateria na maleta"),
 ("kit_completo", "41", 33.6, 37.3, L41, "Kit no balcao: taladro em pe + 2 baterias + carregador (melhor plano de kit)"),
 ("kit_completo", "21", 9.3, 10.85, L21, "Abrindo a maleta: taladro + bateria dentro"),
 ("kit_completo", "21", 11.6, 13.8, L21, "Maleta + carregador + bateria na bancada"),
 ("kit_completo", "21", 54.8, 56.9, L21, "Maleta + carregador -> taladro em pe com bateria (fechamento)"),
 ("kit_completo", "40", 3.6, 6.0, L40, "Maleta aberta na obra: taladro + 2 baterias + carregador (sujeira leve de uso)"),
 ("kit_completo", "40", 6.2, 8.2, L40, "Close do taladro com bateria 2Ah na maleta (obra)"),
 ("bateria", "41", 14.0, 16.8, L41, "Bateria 20V MAX na mao de luva"),
 ("bateria", "21", 13.8, 16.6, L21, "2 baterias 20V 2Ah na bancada (pan)"),
 ("bateria", "21", 28.0, 31.8, L21, "Maos com bateria e taladro (mostra a bateria 2Ah)"),
 ("bateria", "38", 11.9, 15.0, L38, "Bateria 20V 2Ah na mao, indicador de carga verde aceso"),
 ("mandril", "21", 18.0, 20.6, L21, "Taladro deitado na bancada, mandril em destaque"),
 ("mandril", "21", 22.2, 26.1, L21, "Taladro deitado, mandril + anel 13/15 + logo brushless"),
 ("anel", "41", 21.2, 25.1, L41, "Taladro na mao: anel de torque numerado (legenda '15 posicoes' removida)"),
 ("anel", "41", 25.5, 27.0, L41, "Close do anel/seletor com luva"),
 ("anel", "41", 27.3, 30.0, L41, "Close do anel girando (luva)"),
 ("anel", "41", 30.0, 32.8, L41, "Anel girado ate 11-13-15 (posicao de percussao)"),
 ("anel", "21", 33.0, 34.9, L21, "Vista de cima: anel 13-15 e mandril"),
 ("anel", "21", 37.6, 40.9, L21, "Mao girando o anel: 11-13-15 / 5-7-9 / 1-3 (inclui modo martelo)"),
 ("seletor_velocidade", "21", 41.2, 45.0, L21, "Seletor de 2 velocidades no topo (1/2)"),
 ("motor", "21", 35.0, 36.9, L21, "Traseira 'BRUSHLESS MOTOR' na mao (texto 'a DCD7781D2' removido)"),
 ("motor", "38", 10.3, 11.7, L38, "Traseira 'BRUSHLESS MOTOR' girando na mao"),
 ("lateral_brushless", "38", 0.1, 1.9, L38, "Close lateral 'DEWALT 20V MAX BRUSHLESS'"),
 ("gatilho", "38", 2.0, 3.7, L38, "Taladro na mao, dedo no gatilho (expositor da loja)"),
 ("led", "38", 3.7, 7.0, L38, "Gatilho apertado: mandril girando + LED aceso"),
 ("led", "41", 17.2, 21.0, L41, "Taladro na mao de luva, LED acende (legenda removida)"),
 ("led", "21", 50.5, 52.8, L21, "LED aceso iluminando a mao"),
 ("furando_concreto", "30", 0.3, 3.8, L30, "1a pessoa furando parede branca (alvenaria/reboco) com broca longa - corpo DCD778x/7781 (anel 13-15)"),
 ("furando_concreto", "30", 6.0, 9.8, L30, "Mesmo plano do anterior (parede), trecho final - nao usar os 2 no mesmo video"),
]
R37 = [
 ("furando_madeira", "37", 0.95, 1.93, L37N, "Broca entrando na madeira com cavaco (camera lenta 0,8x)", 0.8),
 ("taladro", "37", 4.45, 6.7, L37, "Taladro em pe com bateria (titulo 'parafusadeira furadeira de impacto' removido)"),
 ("taladro", "37", 6.75, 8.2, L37, "Taladro de perfil na bancada (titulo/codigo removidos)"),
 ("maleta", "37", 15.05, 16.85, L37N, "Maleta DEWALT fechada, estudio"),
 ("bateria", "37", 16.95, 18.5, L37N, "Mao encaixando o taladro na bateria/carregador, estudio"),
 ("gatilho", "37", 21.0, 25.0, L37N, "Maos pegando o taladro da bancada, estudio"),
 ("motor", "37", 27.2, 29.3, L37N, "Traseira 'BRUSHLESS MOTOR' na mao, estudio"),
 ("seletor_velocidade", "37", 29.5, 31.9, L37, "Seletor de 2 velocidades (titulo '2 velocidades' removido)"),
 ("taladro", "37", 49.7, 51.7, L37N, "Taladro com bateria na mao sobre a bancada, estudio"),
 ("led", "37", 61.0, 63.5, L37N, "LED aceso, taladro na mao, estudio"),
 ("parafusando_madeira", "37", 64.0, 67.1, L37N, "Tela dividida: taladro em cima + parafuso entrando na madeira embaixo"),
 ("furando_madeira", "37", 67.25, 69.5, L37N, "Tela dividida: taladro em cima + broca/mandril na madeira embaixo"),
 ("parafusando_madeira", "37", 69.9, 71.4, L37N, "Tela dividida: taladro com LED em cima + parafuso na madeira embaixo"),
]
import sys
if "37" in sys.argv: R += R37
cont = {}; out = []
for r in R:
    acao, ad, a, b, limp, obs = r[:6]; vel = r[6] if len(r) > 6 else 1.0
    cont[acao] = cont.get(acao, 0) + 1
    off = OFF.get(ad, 0.0)
    out.append({"arquivo": f"{acao}_{cont[acao]:02d}.mp4", "acao": acao, "ad_origem": ad, "fonte": F[ad], "ini": a, "fim": b,
                "tempo_original": f"{a + off:.2f}-{b + off:.2f}s", "velocidade": vel, "limpeza": limp, "observacoes": obs})
json.dump(out, open("takes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "takes")
