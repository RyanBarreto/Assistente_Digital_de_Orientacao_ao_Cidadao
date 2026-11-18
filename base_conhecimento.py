import json
import os
from orientacao import Orientacao

ACENTOS = {
    "á": "a", "à": "a", "ã": "a", "â": "a",
    "é": "e", "ê": "e",
    "í": "i",
    "ó": "o", "õ": "o", "ô": "o",
    "ú": "u",
    "ç": "c"
}

def normalizar(texto):
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " " .join(texto.split()) + " "

class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        if not os.path.exists(self.caminho):
            print(f"Aviso: O arquivo {self.caminho} não foi encontrado. Iniciando com base vazia.")
            self.orientacoes = []
            return

        try:
            with open(self.caminho, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
                self.orientacoes = [
                    Orientacao(
                        id=item["id"],
                        categoria=item["categoria"],
                        titulo=item["titulo"],
                        palavras_chave=item["palavras_chave"],
                        resposta=item["resposta"],
                        documentos=item["documentos"],
                        onde=item["onde"],
                        fonte=item["fonte"],
                        verificado_em=item["verificado_em"]
                    )
                    for item in dados
                ]
        except (json.JSONDecodeError, Exception) as e:
            print(f"Aviso: Erro ao ler o arquivo JSON ({e}). A base estará vazia.")
            self.orientacoes = []

    def categorias(self):
        return sorted(list(set(o.categoria for o in self.orientacoes)))

    def por_categoria(self, categoria_desejada):
        return [o for o in self.orientacoes if o.categoria.lower() == categoria_desejada.lower()]

    def pontuar(self, pergunta):
        pergunta_norm = normalizar(pergunta)
        pontuacoes = []

        for orientacao in self.orientacoes:
            pontos = 0

            for pc in orientacao.palavras_chave:
                pc_norm = normalizar(pc)
                if pc_norm in pergunta_norm:
                    pontos += 3

            titulo_norm = normalizar(orientacao.titulo)
            palavras_pergunta = pergunta_norm.split()
            for palavra in palavras_pergunta:
                if len(palavra) >= 4 and palavra in titulo_norm:
                    pontos += 1

            if pontos > 0:
                pontuacoes.append((pontos, orientacao))

        pontuacoes.sort(key=lambda x: x[0], reverse=True)
        return pontuacoes

    def buscar(self, pergunta):
        return self.pontuar(pergunta)
