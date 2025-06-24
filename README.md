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
