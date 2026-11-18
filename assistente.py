import time
import json
import os
import csv
from base_conhecimento import BaseConhecimento


class Assistente:
    def __init__(self, nome, base: BaseConhecimento):
        self.nome = nome
        self.base = base
        self.historico = []
        self.carregar_historico()

    def carregar_historico(self):
        caminho_hist = "data/historico.json"
        if os.path.exists(caminho_hist):
            try:
                with open(caminho_hist, 'r', encoding='utf-8') as f:
                    self.historico = json.load(f)
            except:
                self.historico = []

    def salvar_historico_arquivo(self):
        os.makedirs("data", exist_ok=True)
        caminho_hist = "data/historico.json"
        try:
            with open(caminho_hist, 'w', encoding='utf-8') as f:
                json.dump(self.historico, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")

    def validar_dado_pessoal(self, texto):
        if "@" in texto:
            return True

        digitos_consecutivos = 0
        for char in texto:
            if char.isdigit():
                digitos_consecutivos += 1
                if digitos_consecutivos >= 8:
                    return True
            else:
                digitos_consecutivos = 0
        return False

    def perguntar(self):
        inicio = time.time()
        pergunta = input("Digite sua dúvida (0 para voltar): ").strip()

        if pergunta == "0":
            return

        if self.validar_dado_pessoal(pergunta):
            print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
            return

        resultados = self.base.buscar(pergunta)

        encontrou = False
        id_orientacao = None

        if not resultados:
            print("Não encontrei nenhuma orientação correspondente.")
            print("Sugestão: tente usar outras palavras-chave ou navegue pelas categorias.")
        else:
            melhor_pontos, melhor_ori = resultados[0]

            if melhor_pontos >= 6:
                confianca = "ALTA"
            elif melhor_pontos >= 3:
                confianca = "MÉDIA"
            else:
                confianca = "BAIXA"

            print(f"Confiança da resposta: {confianca} ({melhor_pontos} pontos)")
            melhor_ori.exibir()

            encontrou = True
            id_orientacao = melhor_ori.id

            if len(resultados) > 1:
                print("\nOutras alternativas que podem ajudar:")
                for i in range(1, min(3, len(resultados))):
                    pts, alt = resultados[i]
                    print(f"- [ID {alt.id}] {alt.titulo} ({pts} pontos)")

        ajudou_resp = ""
        while ajudou_resp not in ["s", "n"]:
            ajudou_resp = input("Essa orientação respondeu sua dúvida? (s/n): ").lower().strip()
            if ajudou_resp not in ["s", "n"]:
                print("Entrada inválida. Digite apenas 's' para sim ou 'n' para não.")

        ajudou = True if ajudou_resp == "s" else False
        tempo_gasto = round(time.time() - inicio, 1)

        registro = {
            "data": time.strftime("%Y-%m-%d %H:%M:%S"),
            "origem": "pergunta",
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": 1,
            "tempo": tempo_gasto
        }
        self.historico.append(registro)
        self.salvar_historico_arquivo()

    def navegar(self):
        categorias = self.base.categorias()
        if not categorias:
            print("Nenhuma categoria cadastrada.")
            return

        while True:
            print("\n--- Categorias Disponíveis ---")
            for idx, cat in enumerate(categorias, 1):
                print(f"[{idx}] {cat}")
            print("[0] Voltar")

            escolha = input("Escolha uma categoria (número): ").strip()
            if escolha == "0":
                return

            if escolha.isdigit():
                num = int(escolha)
                if 1 <= num <= len(categorias):
                    cat_escolhida = categorias[num - 1]
                    self._listar_por_categoria(cat_escolhida)
                    return
            print("Entrada inválida. Digite um número da lista.")

    def _listar_por_categoria(self, categoria):
        itens = self.base.por_categoria(categoria)
        while True:
            print(f"\n--- Categoria: {categoria} ---")
            for item in itens:
                print(f"[{item.id}] {item.titulo}")
            print("[0] Voltar")

            escolha = input("Escolha o ID da orientação desejada: ").strip()
            if escolha == "0":
                return

            if escolha.isdigit():
                id_escolhido = int(escolha)
                ori_selecionada = next((o for o in itens if o.id == id_escolhido), None)
                if ori_selecionada:
                    inicio = time.time()
                    ori_selecionada.exibir()
                    tempo_gasto = round(time.time() - inicio, 1)

                    ajudou_resp = ""
                    while ajudou_resp not in ["s", "n"]:
                        ajudou_resp = input("Essa orientação respondeu sua dúvida? (s/n): ").lower().strip()
                        if ajudou_resp not in ["s", "n"]:
                            print("Entrada inválida. Digite 's' ou 'n'.")

                    registro = {
                        "data": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "origem": "categoria",
                        "pergunta": f"Navegação na categoria {categoria}",
                        "id_orientacao": ori_selecionada.id,
                        "encontrou": True,
                        "ajudou": (ajudou_resp == "s"),
                        "tentativas": 1,
                        "tempo": tempo_gasto
                    }
                    self.historico.append(registro)
                    self.salvar_historico_arquivo()
                    return
                else:
                    print("ID não encontrado nesta categoria.")
            else:
                print("Entrada inválida.")

    def indicadores(self):
        total = len(self.historico)
        if total == 0:
            print("\nNenhum atendimento realizado ainda.")
            return

        encontrados = sum(1 for h in self.historico if h["encontrou"])
        ajudaram = sum(1 for h in self.historico if h["ajudou"])
        tempo_total = sum(h["tempo"] for h in self.historico)

        taxa_encontro = (encontrados / total) * 100
        taxa_ajuda = (ajudaram / total) * 100
        tempo_medio = tempo_total / total

        print("\n================ INDICADORES ================")
        print(f"Total de atendimentos: {total}")
        print(f"Resposta encontrada: {taxa_encontro:.1f}%")
        print(f"Taxa de acerto (ajudou): {taxa_ajuda:.1f}%")
        print(f"Tempo médio por atendimento: {tempo_medio:.1f} segundos")

        sem_solucao = [h["pergunta"] for h in self.historico if not h["ajudou"] or not h["encontrou"]]
        if sem_solucao:
            print("\nDúvidas sem solução registrada:")
            for d in sem_solucao:
                print(f"- {d}")
        print("=============================================")

    def exportar_csv(self):
        os.makedirs("data", exist_ok=True)
        caminho_csv = "data/atendimentos.csv"
        try:
            with open(caminho_csv, 'w', newline='', encoding='utf-8') as f:
                if self.historico:
                    chaves = self.historico[0].keys()
                    writer = csv.DictWriter(f, fieldnames=chaves)
                    writer.writeheader()
                    writer.writerows(self.historico)
                    print(f"Histórico exportado com sucesso para {caminho_csv}!")
                else:
                    print("Histórico vazio, nada para exportar.")
        except Exception as e:
            print(f"Erro ao exportar CSV: {e}")
