# Plano de Testes — OMNILOG HUB

## Objetivo
Verificar regras de domínio, API, persistência, interface, segurança básica e recuperação. Executar em banco de homologação com dados fictícios; nunca usar dados pessoais reais.

## Casos de teste
| ID | Tipo | Pré-condição | Passos | Resultado esperado |
|---|---|---|---|---|
| CT01 | Caixa branca | Java compilado | Criar Van e calcular frete | Retorno numérico coerente e sem exceção |
| CT02 | Caixa branca | Java compilado | Informar carga acima da capacidade | `IllegalArgumentException` |
| CT03 | Caixa branca | Java compilado | Empilhar ações A/B e voltar | B retornado primeiro (LIFO) |
| CT04 | Caixa branca | Java compilado | Enfileirar P1/P2 e despachar | P1 retornado primeiro (FIFO) |
| CT05 | Caixa preta | API Node ativa | GET /api/health | HTTP 200 e status ok |
| CT06 | Caixa preta | Sessão encerrada | GET /api/customers | HTTP 401 |
| CT07 | Caixa preta | Sessão válida | Criar cliente com e-mail inválido | HTTP 400 |
| CT08 | Caixa preta | Sessão válida e e-mail novo | Criar cliente | HTTP 201 e ID gerado |
| CT09 | Segurança | API em homologação | Enviar texto SQL como valor de busca | Valor tratado como dado; sem alteração SQL |
| CT10 | Segurança | Frontend em homologação | Inserir texto HTML em campos de cadastro | Texto não deve executar script ao renderizar |
| CT11 | Integração | MySQL disponível | Criar cliente e consultar lista | Registro persistido e retornado |
| CT12 | Recuperação | Backup válido | Restaurar em schema de teste e consultar | Dados recuperados e consistentes |

## Registro de defeitos
Use a planilha `registro-defeitos.csv`. Para cada falha: ID, data, versão, ambiente, passos para reproduzir, resultado atual, resultado esperado, severidade, responsável, status e evidência. Não registrar credenciais ou dados pessoais.

## Critério de saída
Todos os casos executados; defeitos críticos corrigidos; testes repetidos após correção; anexar logs e capturas. Casos ainda não executados devem ficar como “Não executado”, nunca como aprovados.
