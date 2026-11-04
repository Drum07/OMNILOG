# Documento de Visão — OMNILOG HUB

## 1. Objetivo
Construir uma plataforma integrada para gestão de pedidos, estoque, armazenagem, transporte, entregas e comércio eletrônico omnichannel.

## 2. Atores
- Cliente: consulta catálogo, realiza pedidos e acompanha entregas.
- Operador de Armazém: registra movimentações, separação e alocação de produtos.
- Gerente Logístico: acompanha indicadores, rotas, frota e entregas.
- Administrador: gerencia usuários, perfis, parâmetros e auditoria.

## 3. Requisitos funcionais iniciais
- RF001: autenticar usuários conforme seu perfil.
- RF002: manter cadastro de clientes e endereços.
- RF003: manter catálogo de produtos e categorias.
- RF004: consultar disponibilidade de estoque por armazém.
- RF005: criar e acompanhar pedidos.
- RF006: registrar pagamentos e seus estados.
- RF007: alocar produtos em posições de armazém.
- RF008: planejar rotas e associar entregas, veículos e motoristas.
- RF009: consultar rastreamento por código.
- RF010: registrar eventos relevantes em trilha de auditoria.
- RF011: gerar indicadores gerenciais.
- RF012: administrar usuários e papéis.

## 4. Requisitos não funcionais iniciais
- RNF001: API documentada via OpenAPI.
- RNF002: consultas comuns devem buscar resposta inferior a 2 segundos em ambiente de referência, com dados e carga definidos nos testes.
- RNF003: senhas devem ser armazenadas somente como hashes seguros.
- RNF004: dados pessoais devem ter finalidade, acesso restrito, retenção definida e proteção compatível com a LGPD.
- RNF005: operações críticas de estoque e pedido devem utilizar transações.
- RNF006: código versionado com Git e revisões por pull request.
- RNF007: testes automatizados para regras críticas.
- RNF008: backups devem ser testados por restauração, não apenas por geração.

## 5. Premissas e limites
O projeto é acadêmico e utiliza dados fictícios. Integrações reais de pagamento, transportadoras e mapas serão simuladas até que existam credenciais e ambientes autorizados.
