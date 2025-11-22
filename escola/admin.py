from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Aluno, Turma, Mensalidade


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Admin para model Usuario"""
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo',)}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'tipo', 'is_staff']
    list_filter = ['tipo', 'is_staff', 'is_superuser']
    search_fields = ['username', 'first_name', 'last_name', 'email']


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    """Admin para model Aluno"""
    list_display = ['nome', 'documento', 'telefone', 'ativo', 'data_cadastro']
    list_filter = ['ativo', 'data_cadastro']
    search_fields = ['nome', 'documento', 'nome_pai', 'nome_mae']
    readonly_fields = ['data_cadastro']
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'documento', 'data_nascimento', 'foto')
        }),
        ('Informações Familiares', {
            'fields': ('nome_pai', 'nome_mae')
        }),
        ('Contato', {
            'fields': ('telefone', 'email', 'endereco')
        }),
        ('Mensalidade', {
            'fields': ('valor_mensalidade',),
            'description': 'Valor fixo mensal que este aluno paga'
        }),
        ('Status', {
            'fields': ('ativo', 'data_cadastro')
        }),
    )


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    """Admin para model Turma"""
    list_display = ['nome', 'ano_letivo', 'periodo', 'professor_responsavel', 'ativa']
    list_filter = ['ano_letivo', 'periodo', 'ativa']
    search_fields = ['nome']
    filter_horizontal = ['alunos']
    readonly_fields = ['data_criacao']
    fieldsets = (
        ('Informações da Turma', {
            'fields': ('nome', 'ano_letivo', 'periodo', 'professor_responsavel')
        }),
        ('Alunos', {
            'fields': ('alunos',)
        }),
        ('Status', {
            'fields': ('ativa', 'data_criacao')
        }),
    )


@admin.register(Mensalidade)
class MensalidadeAdmin(admin.ModelAdmin):
    """Admin para model Mensalidade"""
    list_display = ['aluno', 'valor', 'vencimento', 'status', 'data_pagamento']
    list_filter = ['status', 'vencimento']
    search_fields = ['aluno__nome']
    readonly_fields = ['data_cadastro']
    date_hierarchy = 'vencimento'
    fieldsets = (
        ('Informações da Mensalidade', {
            'fields': ('aluno', 'valor', 'vencimento', 'status')
        }),
        ('Pagamento', {
            'fields': ('data_pagamento', 'observacoes')
        }),
        ('Controle', {
            'fields': ('data_cadastro',)
        }),
    )
