# 🚀 Deploy no PythonAnywhere (100% GRATUITO)

## 📋 Pré-requisitos
- Conta no GitHub (já tem ✅)
- Código já está no GitHub (já está ✅)

## 🎯 Passo a Passo Completo

### 1️⃣ Criar Conta no PythonAnywhere

1. Acesse: https://www.pythonanywhere.com/
2. Clique em **"Pricing & signup"**
3. Escolha **"Create a Beginner account"** (FREE - $0/month)
4. Preencha:
   - Username (ex: `vitorribas`)
   - Email
   - Password
5. Confirme o email

---

### 2️⃣ Configurar o Projeto

Após login, você verá o Dashboard. Siga:

#### A) Abrir Console Bash
1. Clique na aba **"Consoles"**
2. Clique em **"Bash"** (ou "$ Bash")

#### B) Clonar o Repositório
No console Bash, digite:

```bash
git clone https://github.com/vitorribas0/sistema-escolar-django.git
cd sistema-escolar-django
```

#### C) Criar Ambiente Virtual
```bash
mkvirtualenv --python=/usr/bin/python3.10 escola_env
```

Ou se não funcionar:
```bash
python3.10 -m venv venv
source venv/bin/activate
```

#### D) Instalar Dependências
```bash
pip install -r requirements.txt
```

#### E) Configurar Banco de Dados
```bash
python manage.py migrate
python criar_admin.py
```

#### F) Coletar Arquivos Estáticos
```bash
python manage.py collectstatic --noinput
```

---

### 3️⃣ Configurar Web App

#### A) Criar Web App
1. Volte ao Dashboard
2. Clique na aba **"Web"**
3. Clique em **"Add a new web app"**
4. Clique **"Next"**
5. Escolha **"Manual configuration"** (NÃO escolha Django!)
6. Escolha **Python 3.10**
7. Clique **"Next"**

#### B) Configurar Código
Na página Web, procure a seção **"Code"**:

1. **Source code:**
   ```
   /home/SEU_USERNAME/sistema-escolar-django
   ```
   (Substitua `SEU_USERNAME` pelo seu username do PythonAnywhere)

2. **Working directory:**
   ```
   /home/SEU_USERNAME/sistema-escolar-django
   ```

#### C) Configurar Virtual Environment
Na seção **"Virtualenv"**, clique em **"Enter path to a virtualenv"**:

Se usou `mkvirtualenv`:
```
/home/SEU_USERNAME/.virtualenvs/escola_env
```

Se usou `python -m venv`:
```
/home/SEU_USERNAME/sistema-escolar-django/venv
```

#### D) Editar WSGI Configuration File
1. Na seção **"Code"**, clique no link do arquivo WSGI (algo como `/var/www/SEU_USERNAME_pythonanywhere_com_wsgi.py`)
2. **DELETE TODO O CONTEÚDO** do arquivo
3. Cole este código:

```python
import os
import sys

# Adicionar o diretório do projeto ao path
path = '/home/SEU_USERNAME/sistema-escolar-django'
if path not in sys.path:
    sys.path.insert(0, path)

# Configurar variável de ambiente do Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'sistema_escolar.settings'

# Importar aplicação Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**⚠️ IMPORTANTE:** Substitua `SEU_USERNAME` pelo seu username!

4. Clique em **"Save"**

---

### 4️⃣ Configurar Arquivos Estáticos

Na página Web, procure a seção **"Static files"**:

Adicione duas entradas:

**1. Static files:**
- URL: `/static/`
- Directory: `/home/SEU_USERNAME/sistema-escolar-django/staticfiles`

**2. Media files:**
- URL: `/media/`
- Directory: `/home/SEU_USERNAME/sistema-escolar-django/media`

---

### 5️⃣ Criar Arquivo .env (Opcional)

Se quiser usar variáveis de ambiente:

```bash
cd /home/SEU_USERNAME/sistema-escolar-django
nano .env
```

Cole:
```
SECRET_KEY=l9$p%t)rhpr02_z!#-w30x&j#!d^xb#rs_rky6yc3(wy=z$-$i
DEBUG=False
ALLOWED_HOSTS=.pythonanywhere.com
```

Salve: `Ctrl+X`, `Y`, `Enter`

---

### 6️⃣ Ativar o Site

1. Volte para a aba **"Web"**
2. Role até o topo
3. Clique no botão verde **"Reload SEU_USERNAME.pythonanywhere.com"**
4. Aguarde alguns segundos

---

### 7️⃣ Acessar o Sistema

Seu site estará disponível em:
```
https://SEU_USERNAME.pythonanywhere.com
```

**Login:**
- Usuário: `admin`
- Senha: `admin123`

---

## 🔧 Comandos Úteis

### Atualizar o código do GitHub:
```bash
cd ~/sistema-escolar-django
git pull origin main
python manage.py collectstatic --noinput
# Depois clique em "Reload" na aba Web
```

### Ver logs de erro:
Na aba **"Web"**, clique em **"Log files"**:
- Error log
- Server log

### Popular com dados de exemplo:
```bash
cd ~/sistema-escolar-django
source ~/.virtualenvs/escola_env/bin/activate
python popular_dados.py
```

---

## 📱 Para Compartilhar no LinkedIn

Seu sistema estará online em:
```
https://SEU_USERNAME.pythonanywhere.com
```

**Exemplo de post:**

🎓 **Sistema de Gestão Escolar - Django**

Desenvolvi um sistema completo de gestão escolar utilizando Django, com funcionalidades como:

✅ Cadastro de alunos, turmas e mensalidades
✅ Controle financeiro com emissão de recibos
✅ Dashboard com estatísticas e gráficos
✅ API REST completa
✅ Interface moderna e responsiva

🔗 Acesse: https://SEU_USERNAME.pythonanywhere.com
💻 Código: https://github.com/vitorribas0/sistema-escolar-django

#Django #Python #WebDevelopment #FullStack #Portfolio

---

## ❓ Problemas Comuns

### Site mostra erro 500
- Verifique os logs na aba Web > Log files
- Certifique-se que o WSGI está configurado corretamente
- Verifique se o virtualenv está correto

### Static files não carregam
- Rode `python manage.py collectstatic --noinput` no console
- Verifique os caminhos na seção Static files
- Clique em Reload

### Não consigo fazer login
- Execute `python criar_admin.py` no console Bash
- Usuário: admin / Senha: admin123

---

## 🎉 Pronto!

Seu sistema está no ar, 100% gratuito e permanente no PythonAnywhere!

**URL do seu sistema:** https://SEU_USERNAME.pythonanywhere.com

**Repositório GitHub:** https://github.com/vitorribas0/sistema-escolar-django
