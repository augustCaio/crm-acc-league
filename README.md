# CRM da Liga ACC

Este é um projeto de CRM (Customer Relationship Management) desenvolvido em Django para gerenciar uma liga de corridas do jogo Assetto Corsa Competizione (ACC). A aplicação web permite a administração de pilotos, equipes, eventos de corrida e o processamento de resultados para gerar classificações da liga.

## V1.0 - MVP (Minimum Viable Product)

A versão 1.0 foca nas funcionalidades essenciais para colocar a liga em funcionamento.

### Funcionalidades Principais

- **Gestão de Pilotos:** Cadastro, edição e visualização de pilotos participantes.
- **Gestão de Equipes:** Criação e gerenciamento de equipes, com associação de pilotos.
- **Gestão de Eventos:** Agendamento de corridas e temporadas.
- **Upload de Resultados:** Funcionalidade para o administrador fazer o upload dos arquivos de resultado `.json` gerados pelo ACC.
- **Processamento de Resultados:** Leitura dos arquivos `.json` para extrair dados da corrida (posições, voltas, etc.).
- **Classificação da Liga:** Cálculo e exibição da tabela de classificação geral com base nos resultados processados.
- **Autenticação:** Sistema de login para a área administrativa do Django.

## 🛠️ Configuração do Projeto

Siga os passos abaixo para configurar o ambiente de desenvolvimento local.

### Pré-requisitos

- Python 3.8+
- Git

### Instalação

1.  **Clone o repositório:**

    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd crm-acc-league
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux / macOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute as migrações do banco de dados:**

    ```bash
    python manage.py migrate
    ```

5.  **Crie um superusuário para acessar o Admin:**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Inicie o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```
    Acesse a aplicação em `http://127.0.0.1:8000`. A área administrativa estará em `http://127.0.0.1:8000/admin`.

## 🗃️ Banco de Dados

Para a V1.0, o projeto está configurado para usar **SQLite**. Este é um banco de dados leve, baseado em arquivo (`db.sqlite3`), ideal para desenvolvimento e para as fases iniciais do projeto. O arquivo do banco de dados é ignorado pelo Git (via `.gitignore`) para evitar conflitos.

## 🚀 Hospedagem (Deployment)

O projeto está preparado para ser hospedado na plataforma PaaS **Render.com**.

- O `gunicorn` está incluído no `requirements.txt` como servidor de aplicação WSGI.
- As configurações de produção (como `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`) devem ser gerenciadas por variáveis de ambiente no painel do Render.
- O Render detectará o projeto como uma aplicação Python e utilizará o `requirements.txt` para instalar as dependências.
- O comando de inicialização no Render deve ser configurado como: `gunicorn core.wsgi`
