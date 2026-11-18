class Orientacao:
    def __init__(self, dados):
        for campo in ('id', 'categoria', 'titulo', 'palavras_chave', 'resposta', 'documentos', 'onde', 'fonte', 'verificado_em'):
            setattr(self, campo, dados[campo])

    def exibir(self):
        print(f'\n>> {self.titulo} [{self.categoria}]')
        print(self.resposta)
        print('Documentos necessários:')
        for documento in self.documentos:
            print(f' - {documento}')
        print(f'Onde: {self.onde}')
        print(f'Fonte: {self.fonte} (verificado em {self.verificado_em})')
        print('Aviso: este assistente NÃO é um canal oficial. Confira as informações na fonte.')
