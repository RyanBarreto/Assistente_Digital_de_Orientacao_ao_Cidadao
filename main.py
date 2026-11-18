from pathlib import Path
from base_conhecimento import BaseConhecimento
from assistente import Assistente


def main():
    # Permite executar o programa a partir de qualquer diretório.
    import os
    os.chdir(Path(__file__).resolve().parent)
    base = BaseConhecimento('data/base_conhecimento.json')
    base.carregar()
    assistente = Assistente('Citizen Assist AI', base)
    while True:
        print('\n=== CITIZEN ASSIST AI ===')
        print('[1] Fazer uma pergunta')
        print('[2] Navegar por categorias')
        print('[3] Ver indicadores')
        print('[4] Exportar atendimentos CSV')
        print('[0] Sair')
        opcao = input('Escolha uma opção: ').strip()
        if opcao == '1':
            assistente.perguntar()
        elif opcao == '2':
            assistente.navegar()
        elif opcao == '3':
            assistente.indicadores()
        elif opcao == '4':
            assistente.exportar_csv()
        elif opcao == '0':
            assistente.avaliar_facilidade()
            assistente.exportar_csv()
            print('Obrigado por utilizar o Citizen Assist AI!')
            break
        else:
            print('Opção inválida. Tente novamente.')


if __name__ == '__main__':
    main()
