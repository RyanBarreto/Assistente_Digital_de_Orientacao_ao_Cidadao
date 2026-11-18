import csv
import json
import os
import re
import time
from datetime import datetime


class Assistente:
    CAMPOS = ['data', 'origem', 'pergunta', 'id_orientacao', 'encontrou', 'ajudou', 'tentativas', 'tempo']

    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.historico = []
        self.notas = []
        self.carregar_historico()

    def carregar_historico(self):
        try:
            with open('data/historico.json', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
            self.historico = dados if isinstance(dados, list) else []
        except (OSError, json.JSONDecodeError):
            self.historico = []
        try:
            with open('data/facilidade.json', encoding='utf-8') as arquivo:
                notas = json.load(arquivo)
            self.notas = [n for n in notas if isinstance(n, int) and 1 <= n <= 5] if isinstance(notas, list) else []
        except (OSError, json.JSONDecodeError):
            self.notas = []

    def salvar_historico_arquivo(self):
        os.makedirs('data', exist_ok=True)
        try:
            with open('data/historico.json', 'w', encoding='utf-8') as arquivo:
                json.dump(self.historico, arquivo, ensure_ascii=False, indent=2)
        except OSError as erro:
            print(f'Erro ao salvar histórico: {erro}')

    def validar_dado_pessoal(self, texto):
        # Recusa @ e sequências com 8+ dígitos, mesmo com separadores (CPF/telefone).
        if '@' in texto:
            return True
        return any(len(re.sub(r'\D', '', trecho)) >= 8 for trecho in re.findall(r'\d[\d\s().-]*\d|\d+', texto))

    def registrar(self, origem, pergunta, orientacao, encontrou, ajudou, tentativas, inicio):
        # Perguntas com dados pessoais nunca chegam ao registro.
        if self.validar_dado_pessoal(pergunta):
            return
        registro = {
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'origem': origem,
            'pergunta': pergunta,
            'id_orientacao': orientacao.id if orientacao else None,
            'encontrou': encontrou,
            'ajudou': ajudou,
            'tentativas': tentativas,
            'tempo': round(time.time() - inicio, 1),
        }
        self.historico.append(registro)
        self.salvar_historico_arquivo()

    def _ajudou(self):
        while True:
            resposta = input('Essa orientação respondeu sua dúvida? (s/n): ').strip().lower()
            if resposta in ('s', 'n'):
                return resposta == 's'
            print('Entrada inválida. Digite s ou n.')

    def perguntar(self):
        inicio = time.time()
        tentativas = 0
        while True:
            pergunta = input('Digite sua dúvida (0 para voltar): ').strip()
            if pergunta == '0':
                return
            if not pergunta:
                print('Digite uma pergunta ou 0 para voltar.')
                continue
            if self.validar_dado_pessoal(pergunta):
                print('Atenção: não digite CPF, telefone ou e-mail. Reescreva.')
                continue
            tentativas += 1
            resultados = self.base.buscar(pergunta)
            if resultados:
                pontos, melhor = resultados[0]
                print(f'Confiança da resposta: {"ALTA" if pontos >= 6 else "MÉDIA"} ({pontos} pontos)')
                melhor.exibir()
                if len(resultados) > 1:
                    print('Alternativas:')
                    for pontos_alt, alternativa in resultados[1:3]:
                        print(f' - {alternativa.titulo} ({pontos_alt} pontos)')
                ajudou = self._ajudou()
                self.registrar('pergunta', pergunta, melhor, True, ajudou, tentativas, inicio)
                return
            print('Não encontrei orientação. Tente outras palavras ou navegue pelas categorias.')
            while True:
                opcao = input('Tentar outra pergunta? (s/n): ').strip().lower()
                if opcao in ('s', 'n'):
                    break
                print('Digite s ou n.')
            if opcao == 'n':
                self.registrar('pergunta', pergunta, None, False, False, tentativas, inicio)
                return

    def navegar(self):
        while True:
            categorias = self.base.categorias()
            if not categorias:
                print('Nenhuma categoria disponível.')
                return
            print('\n--- Categorias ---')
            for i, categoria in enumerate(categorias, 1):
                print(f'[{i}] {categoria}')
            print('[0] Voltar')
            escolha = input('Escolha uma categoria: ').strip()
            if escolha == '0':
                return
            if not escolha.isdigit() or not 1 <= int(escolha) <= len(categorias):
                print('Opção inválida.')
                continue
            self._listar_por_categoria(categorias[int(escolha) - 1])

    def _listar_por_categoria(self, categoria):
        inicio = time.time()
        itens = self.base.por_categoria(categoria)
        while True:
            print(f'\n--- {categoria} ---')
            for i, orientacao in enumerate(itens, 1):
                print(f'[{i}] {orientacao.titulo}')
            print('[0] Voltar')
            escolha = input('Escolha uma orientação: ').strip()
            if escolha == '0':
                return
            if not escolha.isdigit() or not 1 <= int(escolha) <= len(itens):
                print('Opção inválida.')
                continue
            orientacao = itens[int(escolha) - 1]
            orientacao.exibir()
            ajudou = self._ajudou()
            self.registrar('categoria', f'Navegação na categoria {categoria}', orientacao, True, ajudou, 1, inicio)
            inicio = time.time()

    def avaliar_facilidade(self):
        while True:
            nota = input('Facilidade de uso (1 a 5; 0 para não avaliar): ').strip()
            if nota == '0':
                return
            if nota in ('1', '2', '3', '4', '5'):
                self.notas.append(int(nota))
                try:
                    with open('data/facilidade.json', 'w', encoding='utf-8') as arquivo:
                        json.dump(self.notas, arquivo, indent=2)
                except OSError as erro:
                    print(f'Erro ao salvar nota: {erro}')
                return
            print('Digite um número de 1 a 5, ou 0.')

    def indicadores(self):
        total = len(self.historico)
        if not total:
            print('Nenhum atendimento registrado.')
            return
        encontrados = sum(bool(h.get('encontrou')) for h in self.historico)
        ajudaram = sum(bool(h.get('ajudou')) for h in self.historico)
        tempo = sum(float(h.get('tempo') or 0) for h in self.historico) / total
        tentativas = sum(int(h.get('tentativas') or 0) for h in self.historico) / total
        facilidade = f'{sum(self.notas) / len(self.notas):.1f}/5' if self.notas else 'sem avaliações'
        print('\n=== INDICADORES ===')
        print(f'Total de atendimentos: {total}')
        print(f'Resposta encontrada: {encontrados / total * 100:.1f}%')
        print(f'Taxa de acerto (ajudou): {ajudaram / total * 100:.1f}%')
        print(f'Tempo médio: {tempo:.1f} segundos')
        print(f'Tentativas por atendimento: {tentativas:.1f}')
        print(f'Facilidade de uso: {facilidade}')
        print('Dúvidas sem solução:')
        pendentes = [h.get('pergunta', '(não informada)') for h in self.historico if not h.get('encontrou') or not h.get('ajudou')]
        for pergunta in pendentes:
            print(f' - {pergunta}')
        if not pendentes:
            print(' - Nenhuma')

    def exportar_csv(self):
        os.makedirs('data', exist_ok=True)
        try:
            with open('data/atendimentos.csv', 'w', newline='', encoding='utf-8-sig') as arquivo:
                writer = csv.DictWriter(arquivo, fieldnames=self.CAMPOS, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(self.historico)
            print('CSV exportado para data/atendimentos.csv')
        except OSError as erro:
            print(f'Erro ao exportar CSV: {erro}')
