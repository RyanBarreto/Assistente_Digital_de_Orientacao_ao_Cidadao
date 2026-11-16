from base_conhecimento import BaseConhecimento
from assistente import Assistente

def main():
    caminho_json = "data/base_conhecimento.json"
    base = BaseConhecimento(caminho_json)
    base.carregar()

    assistente = Assistente("Citizen Assist AI", base)

    print("========================================")
    print(f"  Bem-vindo ao {assistente.nome}!  ")
    print("  Seu assistente de serviços públicos ")
    print("========================================")

    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("[1] Fazer uma pergunta")
        print("[2] Navegar por categorias")
        print("[3] Ver indicadores de atendimento")
        print("[4] Sair e exportar relatório (CSV)")

        opcao = input("Escolha uma opção (1-4): ").strip()

        if opcao == "1":
            print("\n--- BUSCA DE DÚVIDAS ---")
            assistente.perguntar()

        elif opcao == "2":
            assistente.navegar()

        elif opcao == "3":
            assistente.indicadores()

        elif opcao == "4":
            nota = ""
            while nota not in ["1", "2", "3", "4", "5"]:
                nota = input("De 1 a 5, qual você avalia a facilidade de uso deste assistente?: ").strip()
                if nota not in ["1", "2", "3", "4", "5"]:
                    print("Entrada inválida. Digite um número inteiro de 1 a 5.")

            if assistente.historico:
                assistente.historico[-1]["facilidade_uso"] = int(nota)
                assistente.salvar_historico_arquivo()

            assistente.exportar_csv()
            print("\nObrigado por utilizar o Citizen Assist AI. Até logo!")
            break

        else:
            print("Opção inválida! Escolha um número entre 1 e 4.")

if __name__ == "__main__":
    main()
