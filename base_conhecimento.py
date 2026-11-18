import json
import re
import unicodedata
from orientacao import Orientacao


def normalizar(texto):
    texto = unicodedata.normalize('NFD', texto.lower())
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return ' ' + ' '.join(re.findall(r'[a-z0-9]+', texto)) + ' '


class BaseConhecimento:
    CAMPOS = {'id', 'categoria', 'titulo', 'palavras_chave', 'resposta', 'documentos', 'onde', 'fonte', 'verificado_em'}

    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        try:
            with open(self.caminho, encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados, list):
                raise ValueError('A base deve ser uma lista.')
            validas = []
            for item in dados:
                if not isinstance(item, dict) or not self.CAMPOS.issubset(item):
                    continue
                if not isinstance(item['palavras_chave'], list) or len(item['palavras_chave']) < 3:
                    continue
                if not isinstance(item['documentos'], list):
                    continue
                validas.append(Orientacao(item))
            self.orientacoes = validas
            print(f'Base carregada: {len(validas)} orientações.')
        except (OSError, json.JSONDecodeError, ValueError) as erro:
            self.orientacoes = []
            print(f'Aviso: não foi possível carregar a base: {erro}')

    def categorias(self):
        return sorted({o.categoria for o in self.orientacoes})

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        pergunta_norm = normalizar(pergunta)
        titulo_norm = normalizar(orientacao.titulo)
        pontos = sum(3 for chave in orientacao.palavras_chave if normalizar(chave).strip() and normalizar(chave) in pergunta_norm)
        palavras = set(pergunta_norm.split())
        pontos += sum(1 for palavra in palavras if len(palavra) >= 4 and f' {palavra} ' in titulo_norm)
        return pontos

    def buscar(self, pergunta):
        resultados = [(self.pontuar(pergunta, o), o) for o in self.orientacoes]
        return sorted((r for r in resultados if r[0] >= 3), key=lambda r: (-r[0], r[1].id))
