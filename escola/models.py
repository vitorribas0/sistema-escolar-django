from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


class Usuario(AbstractUser):
    """Model customizado de usuário para admin e professores"""
    TIPO_CHOICES = [
        ('admin', 'Administrador'),
        ('professor', 'Professor'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='professor')
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_tipo_display()})"


class Aluno(models.Model):
    """Model para cadastro de alunos"""
    nome = models.CharField(max_length=200, verbose_name='Nome Completo')
    nome_pai = models.CharField(max_length=200, verbose_name='Nome do Pai', blank=True)
    nome_mae = models.CharField(max_length=200, verbose_name='Nome da Mãe', blank=True)
    documento = models.CharField(max_length=20, unique=True, verbose_name='RG/CPF')
    foto = models.ImageField(
        upload_to='alunos/fotos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        verbose_name='Foto do Aluno'
    )
    data_nascimento = models.DateField(verbose_name='Data de Nascimento', null=True, blank=True)
    endereco = models.TextField(verbose_name='Endereço', blank=True)
    telefone = models.CharField(max_length=20, verbose_name='Telefone', blank=True)
    email = models.EmailField(verbose_name='E-mail', blank=True)
    valor_mensalidade = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Valor da Mensalidade',
        default=450.00,
        help_text='Valor fixo mensal da mensalidade deste aluno'
    )
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Turma(models.Model):
    """Model para turmas escolares"""
    nome = models.CharField(max_length=100, verbose_name='Nome da Turma')
    ano_letivo = models.IntegerField(verbose_name='Ano Letivo')
    periodo = models.CharField(
        max_length=20,
        choices=[
            ('matutino', 'Matutino'),
            ('vespertino', 'Vespertino'),
            ('noturno', 'Noturno'),
        ],
        default='matutino',
        verbose_name='Período'
    )
    alunos = models.ManyToManyField(Aluno, related_name='turmas', verbose_name='Alunos')
    professor_responsavel = models.ForeignKey(
        'Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='turmas_responsavel',
        limit_choices_to={'tipo': 'professor'},
        verbose_name='Professor Responsável'
    )
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    ativa = models.BooleanField(default=True, verbose_name='Ativa')
    
    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        ordering = ['-ano_letivo', 'nome']
    
    def __str__(self):
        return f"{self.nome} - {self.ano_letivo}"


class Mensalidade(models.Model):
    """Model para mensalidades dos alunos"""
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='mensalidades', verbose_name='Aluno')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    vencimento = models.DateField(verbose_name='Data de Vencimento')
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('atrasado', 'Atrasado'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente', verbose_name='Status')
    data_pagamento = models.DateField(null=True, blank=True, verbose_name='Data de Pagamento')
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    
    class Meta:
        verbose_name = 'Mensalidade'
        verbose_name_plural = 'Mensalidades'
        ordering = ['-vencimento']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.vencimento.strftime('%m/%Y')} - R$ {self.valor}"
