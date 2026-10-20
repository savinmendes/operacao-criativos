# -*- coding: utf-8 -*-
"""Fila de links em disco.

A ideia é que dê para ir jogando link durante a semana e rodar tudo de uma vez.
Por isso a fila mora num JSON simples, legível e editável à mão: se algo der
errado no meio de um lote de 200 vídeos, dá para abrir o arquivo e ver onde
parou, em vez de depender de um banco opaco.
"""
import io
import json
import os
import tempfile
from datetime import datetime

from .texto import extrair_id

STATUS = ("pendente", "feito", "erro", "sem-legenda")


class Fila(object):
    def __init__(self, caminho):
        self.caminho = caminho
        self.itens = self._carregar()

    def _carregar(self):
        if not os.path.exists(self.caminho):
            return []
        try:
            with io.open(self.caminho, encoding="utf-8") as f:
                dados = json.load(f)
        except (ValueError, OSError):
            # Fila corrompida não pode derrubar a ferramenta: o usuário perderia
            # o controle do que já foi feito. Começa vazia e o arquivo antigo
            # continua lá para inspeção.
            return []
        itens = dados.get("itens") if isinstance(dados, dict) else dados
        return itens if isinstance(itens, list) else []

    def salvar(self):
        pasta = os.path.dirname(os.path.abspath(self.caminho))
        if pasta:
            os.makedirs(pasta, exist_ok=True)
        # Grava em arquivo temporário e troca: se o processo morrer no meio de um
        # lote longo, a fila não fica pela metade.
        fd, tmp = tempfile.mkstemp(dir=pasta or ".", suffix=".tmp")
        os.close(fd)
        with io.open(tmp, "w", encoding="utf-8") as f:
            f.write(json.dumps({"itens": self.itens}, ensure_ascii=False, indent=1))
        os.replace(tmp, self.caminho)

    def buscar(self, video_id):
        for it in self.itens:
            if it.get("video_id") == video_id:
                return it
        return None

    def adicionar(self, url, titulo=None, canal=None):
        """Devolve 1 se entrou, 0 se já existia ou se a URL não é de vídeo."""
        vid = extrair_id(url)
        if not vid or self.buscar(vid):
            return 0
        self.itens.append({
            "video_id": vid,
            "url": "https://www.youtube.com/watch?v=" + vid,
            "titulo": titulo,
            "canal": canal,
            "status": "pendente",
            "motor": None,
            "arquivo": None,
            "erro": None,
            "adicionado_em": datetime.now().isoformat(timespec="seconds"),
            "processado_em": None,
        })
        return 1

    def marcar(self, video_id, status, arquivo=None, motor=None, erro=None,
               titulo=None, canal=None, duracao=None):
        it = self.buscar(video_id)
        if not it:
            return False
        it["status"] = status
        it["processado_em"] = datetime.now().isoformat(timespec="seconds")
        for chave, valor in (("arquivo", arquivo), ("motor", motor), ("erro", erro),
                             ("titulo", titulo), ("canal", canal), ("duracao", duracao)):
            if valor is not None:
                it[chave] = valor
        return True

    def pendentes(self, incluir_erros=False):
        alvo = {"pendente"}
        if incluir_erros:
            alvo |= {"erro", "sem-legenda"}
        return [it for it in self.itens if it.get("status") in alvo]

    def remover_concluidos(self):
        antes = len(self.itens)
        self.itens = [it for it in self.itens if it.get("status") != "feito"]
        return antes - len(self.itens)

    def resumo(self):
        c = {}
        for it in self.itens:
            c[it.get("status", "?")] = c.get(it.get("status", "?"), 0) + 1
        return c
