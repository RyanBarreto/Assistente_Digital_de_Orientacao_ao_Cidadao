# Citizen Assist AI — Assistente Digital de Orientação ao Cidadão

Projeto da Global Solution 2026.2 — Pensamento Computacional e Automação com Python.

## Equipe
- Integrante 1: Ryan Barreto Carlos Dias - RM: 574126
- Integrante 2: Fernando Henrique Lembo - RM: 570228


## Público e problema
**Público:** cidadãos em geral. **Problema:** informações sobre documentos, saúde, trabalho e direitos do consumidor estão dispersas em diferentes portais. O assistente orienta por texto livre ou categorias e apresenta fontes oficiais. Não substitui atendimento governamental.


## Estrutura e orientação a objetos
- orientacao.py — Representa um registro da base, guarda seus atributos e apresenta a orientação com exibir().
- base_conhecimento.py — Carrega o JSON, cria os objetos Orientacao, lista categorias e executa a busca por pontuação.
- assistente.py — Recebe perguntas, permite navegação, registra atendimentos, calcula indicadores e exporta CSV.
- main.py: inicializa as classes e executa o menu principal.
  
A arquitetura usa composição: Assistente → BaseConhecimento → lista de Orientacao. Cada orientação vem de um dicionário JSON e a busca devolve tuplas (pontos, orientacao) ordenadas pela pontuação.

## Base de conhecimento
A base data/base_conhecimento.json contém 12 orientações distribuídas por quatro categorias: Documentos, Saúde, Trabalho e Consumidor. Cada registro possui os campos id, categoria, titulo, palavras_chave, resposta, documentos, onde, fonte e verificado_em.

As respostas são locais e só podem ser alteradas mediante edição da base JSON. Antes de apresentar uma orientação como atualizada, é necessário conferir o procedimento e a data de verificação no respectivo órgão oficial.

## Busca inteligente por regras
A função normalizar() transforma o texto em minúsculas e remove acentos e pontuação. Para cada orientação:
- Palavra-chave completa presente na pergunta: +3 pontos.
- Palavra distinta da pergunta, com pelo menos quatro caracteres, presente no título: +1 ponto.
O método buscar() devolve resultados ordenados por pontuação. A melhor resposta recebe confiança ALTA (6 pontos ou mais), MÉDIA (3 a 5 pontos) ou é considerada não encontrada (menos de 3 pontos). O assistente pode mostrar até duas orientações alternativas.

Exemplo: a pergunta Como faço o cartão do SUS? é normalizada e comparada com as palavras-chave e títulos das orientações. As correspondências somam pontos e determinam a confiança exibida.

## Atendimento, segurança e limitações
O assistente trata opções inválidas sem encerrar inesperadamente o programa. Perguntas com @ ou sequências de oito ou mais dígitos, inclusive separadas por pontuação, são recusadas e não são registradas. O programa não solicita nome, CPF, telefone ou e-mail.

A verificação de dados pessoais é heurística, não sendo uma garantia completa contra a inclusão de informações sensíveis. Por isso, recomenda-se utilizar perguntas genéricas. Toda resposta apresenta a fonte, a data de verificação cadastrada e o aviso de que o assistente não é um canal oficial.

Limitações: a base é estática, depende das palavras-chave cadastradas, não consulta sites em tempo real, não identifica automaticamente a localização do usuário e pode não cobrir procedimentos específicos de cada município ou estado.

## Histórico, indicadores e exportação
O arquivo data/historico.json armazena a data, a origem do atendimento (pergunta ou categoria), a pergunta, o ID da orientação, se houve resposta, se ajudou, o número de tentativas e o tempo em segundos. O arquivo data/facilidade.json guarda avaliações anônimas de facilidade, de 1 a 5.

Na opção 3 — Indicadores, o programa apresenta o total de atendimentos, o percentual de respostas encontradas, a taxa de respostas consideradas úteis, o tempo médio, as tentativas médias, a facilidade média e as dúvidas sem solução. Na opção 4 — Exportar CSV, os atendimentos são gravados em data/atendimentos.csv usando csv.DictWriter.

## Fontes oficiais de referência
- Receita Federal — Meu CPF
- Governo Federal — Carteira de Identidade Nacional
- Tribunal Superior Eleitoral — Serviços eleitorais
- Meu SUS Digital
- Ministério da Saúde
- Ministério do Trabalho e Emprego
- Consumidor.gov.br
- Código de Defesa do Consumidor — Lei nº 8.078/1990
