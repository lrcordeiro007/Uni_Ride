## UniRide - Seu App de Caronas Universitárias
Este projeto é uma plataforma para estudantes universitários organizarem caronas, conectando motoristas e passageiros de forma eficiente e segura. A aplicação foi arquitetada como uma base sólida para o desenvolvimento de um serviço de caronas que requer alta performance e um sistema de gerenciamento de banco de dados relacional confiável.

O foco principal do projeto é a simplicidade e a manutenibilidade. Ele implementa as operações essenciais de um `CRUD` (Create, Read, Update, Delete) em um modelo de dados simples, permitindo a gestão de recursos de forma intuitiva e segura, como o cadastro de perfis de motoristas e passageiros.

## ✨ Recursos
API RESTful Completa: Operações CRUD para gestão de dados.

Performance Excepcional: Aproveita as vantagens de assincronicidade do FastAPI, resultando em respostas rápidas e baixo consumo de recursos.

Integração com `MySQL`: Utiliza o `SQLAlchemy` para uma comunicação ORM (Object-Relational Mapping) com o banco de dados, simplificando a manipulação de dados.

Padrão de Código: Código limpo, modular e seguindo as melhores práticas de desenvolvimento Python.

Documentação Automática: O FastAPI gera automaticamente a documentação interativa da API (Swagger UI e ReDoc), facilitando o teste e a compreensão dos endpoints.

Front-end Simples: Uma demonstração de como a API pode ser consumida por um front-end, utilizando HTML, CSS e JavaScript.

## 🛠️ Tecnologias Utilizadas
Python 3.10+

- FastAPI

- MySQL

- SQLAlchemy

- Pydantic

- Uvicorn

- HTML, CSS, JavaScript

## ⚙️ Como Rodar o Projeto
Você tem duas opções para iniciar o projeto, usando um ambiente virtual ou com Docker.

Opção 1: Usando Ambiente Virtual e Uvicorn (Recomendado)
Ambiente Virtual: Crie um ambiente virtual para gerenciar as dependências do projeto.
```bash
python -m venv venv
```
Ative-o:
Windows:
```bash
venv\Scripts\activate
```
macOS/Linux:
```bash
 source venv/bin/activate
```
Instalação das Dependências: Instale as bibliotecas Python necessárias.
```bash
pip install -r requirements.txt
```
Configuração do Banco de Dados: Certifique-se de que o MySQL esteja rodando na sua máquina. Crie um banco de dados e configure as credenciais de acesso no seu projeto. A URL de conexão do SQLAlchemy terá um formato parecido com este:

mysql+mysqlconnector://<seu_usuario>:<sua_senha>@localhost/<nome_do_seu_banco>

Execução do Servidor: Com o ambiente ativado, rode a API com o Uvicorn.
```bash
uvicorn main:app --reload
```
O flag --reload é útil para o desenvolvimento, pois o servidor reinicia automaticamente a cada alteração no código
