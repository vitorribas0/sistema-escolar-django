# Sistema Escolar Django

Sistema completo de gestão escolar desenvolvido em Django com interface web responsiva e API REST.

## Funcionalidades

### Gestão de Alunos
- Cadastro completo com foto e dados familiares
- Busca por nome, documento, nome dos pais
- Histórico de turmas e mensalidades
- Status ativo/inativo

### Gestão de Turmas
- Organização por ano letivo e período (matutino/vespertino/noturno)
- Atribuição de professor responsável
- Gestão de alunos matriculados
- Controle de turmas ativas/inativas

### Gestão de Mensalidades
- Registro de mensalidades com controle de vencimento
- Status: Pendente, Pago, Atrasado
- Filtros por aluno e status
- Resumo financeiro completo

### API REST
- Endpoints completos para todas as entidades
- Autenticação via sessão ou básica
- Filtros, busca e ordenação
- Paginação automática
- Documentação interativa em `/api/`

### Painel Administrativo
- Interface Django Admin customizada
- Controle de usuários (Admin/Professor)
- Gerenciamento completo de dados

## Tecnologias

- Python 3.x
- Django 5.2.8
- Django REST Framework
- SQLite
- Bootstrap 5
- Bootstrap Icons

## Instalação

1. Clone o repositório e entre na pasta do projeto

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
```

3. Instale as dependências:
```bash
pip install django djangorestframework django-filter Pillow
```

4. Execute as migrações:
```bash
python manage.py migrate
```

5. Crie um superusuário:
```bash
python manage.py createsuperuser
```

6. Execute o servidor:
```bash
python manage.py runserver
```

7. Acesse o sistema em `http://localhost:8000`

## Estrutura do Projeto

```
sistema_escolar/
├── escola/                      # App principal
│   ├── templates/              # Templates HTML
│   │   ├── base.html          # Template base
│   │   ├── home.html          # Dashboard
│   │   ├── aluno_lista.html   # Lista de alunos
│   │   ├── aluno_detalhe.html # Detalhes do aluno
│   │   ├── turma_lista.html   # Lista de turmas
│   │   ├── turma_detalhe.html # Detalhes da turma
│   │   ├── mensalidade_lista.html # Lista de mensalidades
│   │   └── registration/
│   │       └── login.html     # Página de login
│   ├── models.py              # Modelos de dados
│   ├── views.py               # Views do sistema
│   ├── admin.py               # Configuração do admin
│   ├── serializers.py         # Serializers da API
│   ├── api_views.py           # ViewSets da API
│   ├── urls.py                # URLs do sistema
│   └── api_urls.py            # URLs da API
├── sistema_escolar/            # Configurações do projeto
│   ├── settings.py            # Configurações
│   ├── urls.py                # URLs principais
│   └── wsgi.py                # WSGI
├── media/                      # Arquivos de upload
├── staticfiles/                # Arquivos estáticos
├── db.sqlite3                  # Banco de dados
├── manage.py                   # Script de gerenciamento
└── requirements.txt            # Dependências

```

## Modelos de Dados

### Usuario (AbstractUser)
- Tipos: Administrador ou Professor
- Autenticação customizada
- Permissões por tipo

### Aluno
- Dados pessoais completos
- Foto (upload)
- Informações dos pais
- Contato e endereço

### Turma
- Ano letivo e período
- Professor responsável
- Alunos matriculados (ManyToMany)
- Status ativo/inativo

### Mensalidade
- Vinculada a um aluno
- Valor e datas (vencimento/pagamento)
- Status automático
- Observações

## API REST

### Endpoints Disponíveis

- **Usuários**: `/api/usuarios/`
- **Alunos**: `/api/alunos/`
- **Turmas**: `/api/turmas/`
- **Mensalidades**: `/api/mensalidades/`

### Ações Personalizadas

**Alunos**
- `GET /api/alunos/{id}/turmas/` - Turmas do aluno
- `GET /api/alunos/{id}/mensalidades/` - Mensalidades do aluno

**Turmas**
- `POST /api/turmas/{id}/adicionar_aluno/` - Adicionar aluno
- `POST /api/turmas/{id}/remover_aluno/` - Remover aluno

**Mensalidades**
- `POST /api/mensalidades/{id}/marcar_como_paga/` - Marcar como paga

### Autenticação

A API usa autenticação por sessão (para uso web) e autenticação básica (para clientes externos).

### Filtros e Busca

Todos os endpoints suportam:
- Busca por texto
- Filtros por campos específicos
- Ordenação
- Paginação (20 itens por página)

## Interface Web

### Dashboard (`/`)
- Estatísticas gerais
- Mensalidades atrasadas
- Turmas ativas
- Acesso rápido

### Alunos (`/alunos/`)
- Listagem com busca
- Visualização de detalhes
- Links para edição no admin

### Turmas (`/turmas/`)
- Cards com informações
- Detalhes com lista de alunos
- Edição no admin

### Mensalidades (`/mensalidades/`)
- Tabela com filtros
- Resumo financeiro
- Status coloridos

### Admin (`/admin/`)
- CRUD completo
- Filtros avançados
- Upload de imagens
- Gerenciamento de usuários

## Credenciais Padrão

Após criar o superusuário, acesse:
- URL: `http://localhost:8000`
- Login: (usuário criado no passo 5)
- Senha: (senha criada no passo 5)

## Personalização

### Adicionar Novos Campos
1. Edite `models.py`
2. Crie migrações: `python manage.py makemigrations`
3. Aplique: `python manage.py migrate`
4. Atualize admin, serializers e templates

### Customizar Interface
- Templates estão em `escola/templates/`
- Usa Bootstrap 5 via CDN
- Ícones Bootstrap Icons

### Configurar Produção
1. Altere `DEBUG = False` em settings.py
2. Configure `ALLOWED_HOSTS`
3. Use banco de dados robusto (PostgreSQL)
4. Configure servidor web (nginx + gunicorn)
5. Colete arquivos estáticos: `python manage.py collectstatic`

## Licença

Projeto educacional - livre para uso e modificação.
