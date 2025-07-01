# MVP-backend-api-python

# ⚙️ Instalação do Projeto

Este projeto utiliza um ambiente virtual e dependências definidas no arquivo `requirements.txt`. Siga as instruções abaixo para configurar o ambiente automaticamente de acordo com o seu sistema operacional.

---

## 🪟 Windows

1. Abra o terminal e navegue até a pasta do projeto.
2. Execute o script:
   ```bash
   .\setup.bat

## 🐧 Linux

1. Abra o terminal e navegue até a pasta do projeto
2. Execute o script para dar permissão:
   ```bash
   chmod +x setup.sh
3. Execute o script:
   ```bash
   ./setup.sh

---

## ✏️ Variáveis no arquivo .env

para de fato conectar a aplicação, é necessário que crie duas variáveis no arquivo .env, a SECRET_KEY possui a chave de criptografia para senhas e a MONGO_URI possui o endereço de conexão com o Mongo DB Atlas:
1. SECRET_KEY
2. MONGO_URI

## ✅ Após a instalação, no terminal, digite o seguinte comando para rodar a API:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## 📖 Documentação da API

A Api utiliza o Swagger para a documentação e testes.
endereço da documentação: 
   ```bash
   http://127.0.0.1:8000/api-docs
   ```

# 📘 Especificação de Requisitos da API

## Requisitos Funcionais

|Funcionalidade | Descrição |
|----------------|-----------|
| Cadastro e Login de Administradores | Permitir que administradores se registrem, façam login seguro e gerenciem suas sessões de acesso. |
| Gerenciamento de Informações | O sistema deve permitir que Administradores possam criar, atualizar e remover dados sobre atividades e eventos. |
| Consulta Pública de Dados | O sistema deve permitir que Visitantes acessam informações atualizadas, sem necessidade de autenticação. |

---

## Requisitos Não Funcionais

| Categoria | Descrição |
|-----------|-----------|
| Desempenho | A API deve responder às requisições em até 2 segundos mesmo com alta demanda simultânea. |
| Segurança | Rotas protegidas com autenticação JWT e criptografia dos dados sensíveis. |
| Documentação | Todos os endpoints documentados com Swagger (OpenAPI), facilitando testes e integração. |
| Confiabilidade | Uptime acima de 99,5% e mensagens claras em caso de falhas ou indisponibilidade de serviço. |

---

