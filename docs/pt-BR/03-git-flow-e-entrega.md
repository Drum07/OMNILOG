# UC10 — Git Flow e entrega

## Branches
- `main`: versão estável de produção.
- `develop`: integração contínua da equipe.
- `feature/<nome>`: uma funcionalidade por branch, criada a partir de `develop`.
- `release/<versao>`: estabilização, documentação e correções finais.
- `hotfix/<correcao>`: correção urgente derivada de `main`.

## Commits semânticos
Usar `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `build:` e `chore:`. Exemplo: `feat: add customer search pagination`.

## Fluxo
1. Atualizar `develop`.
2. Criar `feature/...`.
3. Implementar e testar localmente.
4. Abrir Pull Request para `develop`, com descrição, evidências e checklist.
5. Solicitar revisão de outro integrante; corrigir comentários.
6. Integrar somente após CI verde.
7. Criar `release/...`, validar e integrar em `main` e `develop`.

## Evidências que dependem da equipe
Histórico real de commits, branches remotas, Pull Requests, revisões cruzadas e participantes devem ser gerados no GitHub/GitLab pela equipe. Não podem ser simulados por documentação local.

## CI
O workflow `.github/workflows/ci.yml` executa validações automáticas. Para entrega, anexar link do repositório e capturas dos PRs/reviews.
