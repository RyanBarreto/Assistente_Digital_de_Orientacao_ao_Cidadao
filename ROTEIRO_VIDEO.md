# Roteiro técnico — 7 minutos e 30 segundos

**00:00–00:30 | Abertura:** apresentar integrantes e RMs, público geral, dificuldade de localizar informações oficiais e objetivo do programa.

**00:30–01:15 | JSON:** abrir `data/base_conhecimento.json`; explicar um registro, chaves, valores, lista de palavras-chave, fonte e data; mostrar dicionários e explicar que a busca retorna tuplas `(pontos, orientacao)`.

**01:15–02:20 | Classes e composição:** abrir `orientacao.py`, `base_conhecimento.py` e `assistente.py`; explicar `__init__`, `self`, atributos, métodos, lista de orientações e a composição Assistente -> BaseConhecimento -> Orientacao.

**02:20–03:20 | Algoritmo:** abrir `normalizar()` e `pontuar()`; demonstrar `Como faço o cartão do SUS?`. A chave `cartao do sus` vale 3, `cartao sus` não é sequência contígua nesta frase, `cartao` no título vale 1, `sus` também aparece no título mas tem menos de quatro letras. Se a chave `cartao sus` não aparecer, a pontuação será 4 (MÉDIA). Calcular os pontos reais na execução e explicar a regra de 3 e 6 pontos.

**03:20–04:50 | Execução:** rodar `python main.py`; perguntar `Como faço o cartão do SUS?`, depois `Como consertar meu foguete?` (não encontrada), testar opção inválida `99`, texto com CPF fictício `123.456.789-00` (não deve ser registrado) e navegar por Saúde com 0 para voltar.

**04:50–05:40 | Mudança ao vivo:** antes da gravação, confirmar que `Como faço meu documento lilás?` não encontra resposta. Abrir JSON e acrescentar a palavra-chave `documento lilas` à orientação de identidade. Salvar, reiniciar o programa e repetir a pergunta; agora ela será encontrada. Explicar que a base é estática e a atualização depende de edição manual. *Este é um termo fictício apenas para demonstrar a pontuação, não um serviço oficial.*

**05:40–06:35 | Histórico e indicadores:** mostrar `data/historico.json`, `data/atendimentos.csv`, `data/facilidade.json` e opção 3; exibir os indicadores dos testes reais com pelo menos três pessoas e dez atendimentos.

**06:35–07:30 | Decisão técnica e limitação:** justificar o uso de regras locais e fontes em JSON, sem API e sem coleta de dados pessoais. Explicar que a busca pode falhar com sinônimos não cadastrados e que as informações precisam ser revisadas. Encerrar mostrando README e link do vídeo.

**Atenção:** todos os integrantes precisam falar. Se for trabalho individual, a pessoa apresenta todas as partes. Não utilizar voz sintética. A demonstração da alteração no JSON deve acontecer ao vivo e o termo fictício deve ser removido depois.
