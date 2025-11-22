import os
import django
from datetime import date, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_escolar.settings')
django.setup()

from escola.models import Usuario, Aluno, Turma, Mensalidade

print('🎓 Populando o Sistema Escolar com dados de exemplo...\n')

# Criar professores
professor1, created = Usuario.objects.get_or_create(
    username='prof.maria',
    defaults={
        'email': 'maria@escola.com',
        'first_name': 'Maria',
        'last_name': 'Silva',
        'tipo': 'professor',
        'is_staff': True
    }
)
if created:
    professor1.set_password('senha123')
    professor1.save()
    print('✅ Professora Maria Silva criada')

professor2, created = Usuario.objects.get_or_create(
    username='prof.joao',
    defaults={
        'email': 'joao@escola.com',
        'first_name': 'João',
        'last_name': 'Santos',
        'tipo': 'professor',
        'is_staff': True
    }
)
if created:
    professor2.set_password('senha123')
    professor2.save()
    print('✅ Professor João Santos criado')

# Criar alunos
alunos_data = [
    {'nome': 'Ana Carolina Souza', 'nome_pai': 'Carlos Souza', 'nome_mae': 'Julia Souza', 'documento': '123.456.789-01', 'telefone': '(11) 98765-4321', 'email': 'ana@email.com'},
    {'nome': 'Bruno Henrique Lima', 'nome_pai': 'Henrique Lima', 'nome_mae': 'Patricia Lima', 'documento': '234.567.890-12', 'telefone': '(11) 98765-4322', 'email': 'bruno@email.com'},
    {'nome': 'Carla Beatriz Costa', 'nome_pai': 'Roberto Costa', 'nome_mae': 'Fernanda Costa', 'documento': '345.678.901-23', 'telefone': '(11) 98765-4323', 'email': 'carla@email.com'},
    {'nome': 'Daniel Rodrigues Alves', 'nome_pai': 'Pedro Alves', 'nome_mae': 'Mariana Alves', 'documento': '456.789.012-34', 'telefone': '(11) 98765-4324', 'email': 'daniel@email.com'},
    {'nome': 'Eduarda Ferreira Santos', 'nome_pai': 'José Santos', 'nome_mae': 'Amanda Santos', 'documento': '567.890.123-45', 'telefone': '(11) 98765-4325', 'email': 'eduarda@email.com'},
    {'nome': 'Felipe Gabriel Oliveira', 'nome_pai': 'Gabriel Oliveira', 'nome_mae': 'Luciana Oliveira', 'documento': '678.901.234-56', 'telefone': '(11) 98765-4326', 'email': 'felipe@email.com'},
    {'nome': 'Giovanna Martins Silva', 'nome_pai': 'Marcelo Silva', 'nome_mae': 'Renata Silva', 'documento': '789.012.345-67', 'telefone': '(11) 98765-4327', 'email': 'giovanna@email.com'},
    {'nome': 'Henrique Costa Pereira', 'nome_pai': 'Ricardo Pereira', 'nome_mae': 'Cristina Pereira', 'documento': '890.123.456-78', 'telefone': '(11) 98765-4328', 'email': 'henrique@email.com'},
]

alunos_criados = []
for aluno_data in alunos_data:
    aluno, created = Aluno.objects.get_or_create(
        documento=aluno_data['documento'],
        defaults={
            'nome': aluno_data['nome'],
            'nome_pai': aluno_data['nome_pai'],
            'nome_mae': aluno_data['nome_mae'],
            'telefone': aluno_data['telefone'],
            'email': aluno_data['email'],
            'data_nascimento': date(2010, 1, 1),
            'endereco': 'Rua Exemplo, 123 - São Paulo/SP',
            'ativo': True
        }
    )
    if created:
        print(f'✅ Aluno {aluno.nome} criado')
    alunos_criados.append(aluno)

# Criar turmas
turma1, created = Turma.objects.get_or_create(
    nome='5º Ano A',
    ano_letivo=2025,
    defaults={
        'periodo': 'matutino',
        'professor_responsavel': professor1,
        'ativa': True
    }
)
if created:
    turma1.alunos.set(alunos_criados[:4])
    print(f'✅ Turma {turma1.nome} criada com {turma1.alunos.count()} alunos')

turma2, created = Turma.objects.get_or_create(
    nome='6º Ano B',
    ano_letivo=2025,
    defaults={
        'periodo': 'vespertino',
        'professor_responsavel': professor2,
        'ativa': True
    }
)
if created:
    turma2.alunos.set(alunos_criados[4:])
    print(f'✅ Turma {turma2.nome} criada com {turma2.alunos.count()} alunos')

# Criar mensalidades
print('\n💰 Criando mensalidades...')
hoje = date.today()
for i, aluno in enumerate(alunos_criados):
    # Mensalidade paga (mês passado)
    venc_passado = date(hoje.year, hoje.month - 1 if hoje.month > 1 else 12, 10)
    mens1, created = Mensalidade.objects.get_or_create(
        aluno=aluno,
        vencimento=venc_passado,
        defaults={
            'valor': Decimal('450.00'),
            'status': 'pago',
            'data_pagamento': venc_passado,
            'observacoes': 'Pagamento em dia'
        }
    )
    
    # Mensalidade do mês atual
    venc_atual = date(hoje.year, hoje.month, 10)
    status_atual = 'pago' if i < 4 else 'pendente'
    mens2, created = Mensalidade.objects.get_or_create(
        aluno=aluno,
        vencimento=venc_atual,
        defaults={
            'valor': Decimal('450.00'),
            'status': status_atual,
            'data_pagamento': venc_atual if status_atual == 'pago' else None,
            'observacoes': 'Mensalidade atual'
        }
    )
    
    # Algumas mensalidades atrasadas
    if i >= 6:
        venc_atrasado = date(hoje.year, hoje.month - 2 if hoje.month > 2 else 12, 10)
        mens3, created = Mensalidade.objects.get_or_create(
            aluno=aluno,
            vencimento=venc_atrasado,
            defaults={
                'valor': Decimal('450.00'),
                'status': 'atrasado',
                'observacoes': 'Aguardando pagamento'
            }
        )

print('\n✅ Sistema populado com sucesso!')
print(f'\n📊 Resumo:')
print(f'   👥 Alunos: {Aluno.objects.count()}')
print(f'   👨‍🏫 Professores: {Usuario.objects.filter(tipo="professor").count()}')
print(f'   📚 Turmas: {Turma.objects.count()}')
print(f'   💰 Mensalidades: {Mensalidade.objects.count()}')
print(f'\n🔐 Login de teste:')
print(f'   Admin: admin / admin123')
print(f'   Professor: prof.maria / senha123')
print(f'\n🌐 Acesse: http://127.0.0.1:8000')
