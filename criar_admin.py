import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_escolar.settings')
django.setup()

from escola.models import Usuario

# Criar superusuário admin
if not Usuario.objects.filter(username='admin').exists():
    Usuario.objects.create_superuser(
        username='admin',
        email='admin@escola.com',
        password='admin123',
        first_name='Administrador',
        last_name='Sistema',
        tipo='admin'
    )
    print('✅ Superusuário criado com sucesso!')
    print('Username: admin')
    print('Password: admin123')
else:
    print('⚠️ Usuário admin já existe!')
