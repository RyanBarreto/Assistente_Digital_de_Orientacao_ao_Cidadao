# Citizen Assist AI — Assistente Digital de Orientação ao Cidadão

Projeto da Global Solution 2026.2 — Pensamento Computacional e Automação com Python.

## Equipe
- Integrante 1: Ryan Barreto Carlos Dias - RM: 574126
- Integrante 2: Fernando Henrique Lembo - RM: 570228


## Público e problema
**Público:** cidadãos em geral. **Problema:** informações sobre documentos, saúde, trabalho e direitos do consumidor estão dispersas em diferentes portais. O assistente orienta por texto livre ou categorias e apresenta fontes oficiais. Não substitui atendimento governamental.

## ODS relacionadas
- ODS 3 — Saúde e Bem-Estar (acesso a orientações sobre saúde).
- ODS 8 — Trabalho Decente e Crescimento Econômico (informações sobre trabalho).
- ODS 16 — Paz, Justiça e Instituições Eficazes (acesso à informação e serviços).


Menu: 1 perguntar, 2 categorias, 3 indicadores, 4 exportar CSV, 0 sair. Para testar, digite `Como faço o cartão do SUS?`.

## Arquitetura e orientação a objetos
- `orientacao.py`: classe `Orientacao`, armazena um registro JSON e implementa `exibir()`.
- `base_conhecimento.py`: classe `BaseConhecimento`, usa uma lista de objetos `Orientacao`; carrega JSON, lista categorias, pontua e busca.
- `assistente.py`: classe `Assistente`, contém um objeto `BaseConhecimento` e histórico de atendimentos; pergunta, navega, registra, calcula indicadores e exporta CSV.
- `main.py`: instancia as classes e mantém o menu.

**Composição:** `Assistente -> BaseConhecimento -> lista de Orientacao`. Os registros JSON são dicionários; os resultados de busca são tuplas `(pontos, orientacao)`.

## Busca inteligente por regras
`normalizar()` converte para minúsculas, remove acentos e pontuação. Cada palavra-chave completa encontrada na pergunta vale **+3 pontos**; cada palavra distinta da pergunta com pelo menos quatro caracteres presente no título vale **+1 ponto**. A busca devolve tuplas ordenadas por pontuação decrescente. **6+ pontos:** confiança ALTA; **3–5:** MÉDIA; **menos de 3:** não encontrada. Exibe até duas alternativas. Não usa IA generativa nem consulta a internet durante a execução.

## Segurança, transparência e limitações
Perguntas contendo `@` ou uma sequência com oito ou mais dígitos, inclusive separados por pontuação, são recusadas e não registradas. O programa não solicita dados pessoais. A proteção é heurística e não garante detecção de todo dado sensível; por isso, os testes devem usar apenas perguntas genéricas. Cada orientação exibe fonte, data e aviso de não oficialidade. A base é estática, a busca depende de palavras-chave e serviços podem variar conforme localidade. Não há geolocalização nem atualização automática.

## Base e fontes
12 orientações distribuídas em quatro categorias: Documentos, Saúde, Trabalho e Consumidor. Cada registro contém `id`, `categoria`, `titulo`, `palavras_chave`, `resposta`, `documentos`, `onde`, `fonte`, `verificado_em`.

Fontes de referência: [Receita Federal](https://www.gov.br/receitafederal/pt-br/assuntos/meu-cpf), [Carteira de Identidade Nacional](https://www.gov.br/gestao/pt-br/assuntos/identificacao-do-cidadao/carteira-de-identidade-nacional), [TSE](https://www.tse.jus.br/servicos-eleitorais), [Meu SUS Digital](https://meususdigital.saude.gov.br/), [Ministério da Saúde](https://www.gov.br/saude/pt-br), [Ministério do Trabalho e Emprego](https://www.gov.br/trabalho-e-emprego/pt-br), [Consumidor.gov.br](https://www.consumidor.gov.br/), [Código de Defesa do Consumidor](https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm).


## Histórico e indicadores
`data/historico.json` guarda data, origem, pergunta, ID, encontrou, ajudou, tentativas e tempo em segundos. `data/facilidade.json` guarda somente notas anônimas de 1 a 5. `data/atendimentos.csv` exporta o histórico. Indicadores: percentual encontrado, percentual que ajudou, tempo médio, tentativas médias, facilidade média e dúvidas sem solução. Não são coletados nomes dos participantes.

## Testes com usuários — preencher com dados reais
Realizar **no mínimo três participantes externos à equipe e dez atendimentos**. Não inserir nomes nem dados pessoais. Após os testes, preencher:

| Indicador | Resultado real |
|---|---|
| Participantes externos | [PREENCHER] |
| Atendimentos | [PREENCHER] |
| Resposta encontrada | [PREENCHER]% |
| Taxa de acerto (ajudou) | [PREENCHER]% |
| Tempo médio | [PREENCHER] s |
| Tentativas médias | [PREENCHER] |
| Facilidade média | [PREENCHER]/5 |
| Dúvidas sem solução | [PREENCHER] |

**Melhoria após teste:** [DESCREVER UMA MUDANÇA REAL FEITA A PARTIR DO FEEDBACK].

