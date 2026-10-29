# JobTrack

Sistema web para gerenciamento e acompanhamento de candidaturas a vagas de emprego.

Trabalho acadêmico da disciplina **Programação para Internet** — UENP, Campus Luiz Meneghel.

## Integrantes

- **Gabriel Rocha de Oliveira**
- **Ruan Tirabassi**

## Funcionalidades

- Autenticação simples (cadastro, login, logout) — cada usuário vê apenas suas candidaturas.
- **Dashboard** com indicadores, gráficos (distribuição por status e volume por mês) e candidaturas recentes.
- **Minhas candidaturas** — listagem com busca por empresa/cargo e filtros por status e modalidade, atualização ao vivo via HTMX.
- **Nova candidatura / Editar / Excluir** — CRUD completo com validação.
- Visualização detalhada de cada candidatura.
- Interface moderna, responsiva, pensada para desktop.

### Status de acompanhamento
Candidatado · Em análise · Entrevista · Aprovado · Reprovado · Desistência

### Modalidades
Remoto · Híbrido · Presencial

## Tecnologias

| Camada     | Tecnologia                          |
|------------|-------------------------------------|
| Backend    | Python 3.11+ · Django 5             |
| Banco      | SQLite (arquivo `db.sqlite3`)       |
| ORM        | Django ORM                          |
| Templates  | Django Templates                    |
| CSS        | Tailwind CSS (via CDN)              |
| JS         | HTMX (via CDN) · Chart.js (via CDN) |
| Fontes     | Inter (Google Fonts)                |

> Nenhum build/npm/webpack. Só Python e um `pip install`.

## Como executar

### Pré-requisitos
- Python 3.11 ou superior
- `pip` (vem com Python)

### Passo a passo

**Windows (PowerShell):**

```powershell
# 1. criar e ativar ambiente virtual
python -m venv .venv
.venv\Scripts\activate

# 2. instalar dependências
pip install -r requirements.txt

# 3. criar o banco de dados (SQLite, gerado automaticamente)
python manage.py makemigrations
python manage.py migrate

# 4. (opcional) criar um superusuário para acessar o /admin
python manage.py createsuperuser

# 5. subir o servidor
python manage.py runserver
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # opcional
python manage.py runserver
```

Acesse: **http://127.0.0.1:8000**

Se é o primeiro acesso, clique em **Cadastre-se** para criar sua conta.

## Estrutura

```
trab-aex/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3                        (gerado após migrate)
├── jobtrack/                         (configuração do projeto)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── candidaturas/                     (app principal)
    ├── models.py                     (modelo Candidatura)
    ├── forms.py                      (CandidaturaForm, SignupForm)
    ├── views.py                      (dashboard, lista, nova, editar, excluir, detalhe, signup)
    ├── urls.py
    ├── admin.py
    ├── migrations/
    └── templates/
        ├── base.html                 (layout global + Tailwind + HTMX)
        ├── registration/
        │   ├── login.html
        │   └── signup.html
        └── candidaturas/
            ├── dashboard.html
            ├── lista.html
            ├── _tabela.html          (parcial renderizada pelo HTMX)
            ├── form.html
            ├── detalhe.html
            └── confirmar_exclusao.html
```

## Rotas

| URL                                    | View       | Descrição                     |
|----------------------------------------|------------|-------------------------------|
| `/`                                    | dashboard  | Painel com gráficos e KPIs    |
| `/candidaturas/`                       | lista      | Listagem com busca e filtros  |
| `/candidaturas/nova/`                  | nova       | Formulário de criação         |
| `/candidaturas/<id>/`                  | detalhe    | Visualização completa         |
| `/candidaturas/<id>/editar/`           | editar     | Formulário de edição          |
| `/candidaturas/<id>/excluir/`          | excluir    | Confirmação + exclusão        |
| `/entrar/`                             | login      | Tela de login                 |
| `/sair/`                               | logout     | Sair da conta                 |
| `/cadastrar/`                          | signup     | Criar conta                   |
| `/admin/`                              | admin      | Admin do Django (opcional)    |

## Modelo de dados

### Candidatura

| Campo              | Tipo              | Obs.                                    |
|--------------------|-------------------|-----------------------------------------|
| usuario            | FK → User         | Dono da candidatura                     |
| empresa            | CharField(120)    | Obrigatório                             |
| cargo              | CharField(120)    | Obrigatório                             |
| salario            | Decimal(10,2)     | Opcional                                |
| modalidade         | choices           | Remoto / Híbrido / Presencial           |
| link               | URL               | Opcional                                |
| data_candidatura   | Date              | Obrigatório                             |
| status             | choices           | Candidatado / Em análise / Entrevista / Aprovado / Reprovado / Desistência |
| observacoes        | Text              | Opcional                                |
| criado_em          | DateTime          | Automático                              |
| atualizado_em      | DateTime          | Automático                              |

## Observações

- O banco SQLite é um único arquivo (`db.sqlite3`) gerado no primeiro `migrate` — não requer servidor, usuário ou senha.
- As dependências de front-end (Tailwind, HTMX, Chart.js, Inter) são carregadas via CDN público; é necessário estar com internet ao abrir a aplicação.
- Em produção, troque `SECRET_KEY` em `jobtrack/settings.py` e defina `DEBUG = False`.
