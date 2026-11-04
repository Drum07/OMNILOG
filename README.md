# OMNILOG HUB
### Sistema de Gestão Logística

**Interface acessível em preto e branco | Português do Brasil**

O **OMNILOG HUB** é um sistema de gestão logística desenvolvido do zero, com o objetivo de integrar e organizar operações de clientes, produtos, estoque, pedidos, armazéns e entregas em uma única plataforma.

O projeto possui interface responsiva, alto contraste e recursos de acessibilidade, além de integração com banco de dados MySQL por meio de uma API desenvolvida em Python e FastAPI.

## Funcionalidades

- Painel de indicadores.
- Cadastro e gerenciamento de clientes.
- Gerenciamento de categorias.
- Cadastro e gerenciamento de produtos.
- Controle de armazéns.
- Gerenciamento de estoque.
- Registro e acompanhamento de pedidos.
- Cadastro e acompanhamento de entregas.
- Pesquisa e filtragem de registros.
- Criação, edição e exclusão de dados.

## Tecnologias utilizadas

- Python 3.12+
- FastAPI
- SQLAlchemy
- MySQL 8+
- HTML5
- CSS3
- JavaScript
- Pytest

## Acessibilidade

A interface foi desenvolvida com foco em acessibilidade e facilidade de utilização, incluindo:

- Design em preto e branco com alto contraste.
- Navegação por teclado.
- Indicadores de foco visíveis.
- Link para pular diretamente ao conteúdo.
- Rótulos acessíveis nos formulários.
- Mensagens com suporte a tecnologias assistivas.
- Preferência por movimento reduzido.
- Layout responsivo.

## Requisitos para instalação

- Windows 10 ou superior.
- Python 3.12 ou superior.
- MySQL 8 ou superior.
- Visual Studio Code (recomendado).

## Instalação

### 1. Preparar o projeto

Descompacte o projeto e abra a pasta raiz no terminal do VS Code.

### 2. Criar o ambiente virtual

```powershell
py -m venv .venv
```

### 3. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```powershell
py -m pip install -r .\backend\requirements.txt
```

### 5. Configurar o banco de dados

Copie o arquivo `.env.example` para `.env` e configure localmente a conexão com o MySQL.

Não compartilhe o arquivo `.env` nem publique suas credenciais.

### 6. Iniciar o servidor

Na pasta raiz do projeto, execute:

```powershell
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

### 7. Acessar o sistema

- API: http://127.0.0.1:8000/
- Documentação da API: http://127.0.0.1:8000/docs

## Banco de dados

O sistema utiliza MySQL 8 e possui tabelas relacionadas a clientes, produtos, categorias, estoque, pedidos, entregas, pagamentos, usuários, motoristas, veículos, rotas e armazéns.

As operações respeitam as restrições de integridade referencial e as chaves estrangeiras definidas no banco de dados.

**Importante:** faça backup antes de realizar alterações no esquema ou nos dados.

## Segurança

- Credenciais mantidas em arquivo de configuração local.
- Consultas parametrizadas quando aplicável.
- Restrições de integridade no banco de dados.
- Recomenda-se utilizar uma conta MySQL com permissões limitadas.
- A implementação de autenticação e autorização deve ser concluída antes de disponibilizar o sistema publicamente.

## Documentação complementar

Os materiais técnicos e acadêmicos estão organizados nas seguintes pastas:

- `docs/pt-BR/`: documentação em português.
- `docs/en-US/`: documentação técnica em inglês.
- `docs/diagrams/`: diagramas do sistema.
- `docs/qa/`: plano de testes e registro de defeitos.
- `uc4-java/`: módulo de orientação a objetos em Java.
- `uc8-desktop/`: protótipo de aplicação desktop.
- `uc13-node/`: módulo de API com Node.js e Express.

Consulte `docs/pt-BR/04-matriz-de-atendimento.md` para verificar o andamento dos requisitos acadêmicos.

---

## Autor

**Desenvolvimento:** Jean Paul da Silva

**Projeto:** OMNILOG HUB — Sistema de Gestão Logística

**Área:** Tecnologia da Informação e Desenvolvimento de Sistemas