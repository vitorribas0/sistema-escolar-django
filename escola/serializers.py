from rest_framework import serializers
from .models import Usuario, Aluno, Turma, Mensalidade


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para model Usuario"""
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'tipo', 'is_staff', 'is_active']
        read_only_fields = ['id']


class AlunoSerializer(serializers.ModelSerializer):
    """Serializer para model Aluno"""
    turmas = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Aluno
        fields = [
            'id', 'nome', 'nome_pai', 'nome_mae', 'documento', 'foto',
            'data_nascimento', 'endereco', 'telefone', 'email',
            'data_cadastro', 'ativo', 'turmas'
        ]
        read_only_fields = ['id', 'data_cadastro']


class TurmaSerializer(serializers.ModelSerializer):
    """Serializer para model Turma"""
    alunos = AlunoSerializer(many=True, read_only=True)
    professor_responsavel = UsuarioSerializer(read_only=True)
    total_alunos = serializers.SerializerMethodField()
    
    class Meta:
        model = Turma
        fields = [
            'id', 'nome', 'ano_letivo', 'periodo', 'alunos',
            'professor_responsavel', 'data_criacao', 'ativa', 'total_alunos'
        ]
        read_only_fields = ['id', 'data_criacao']
    
    def get_total_alunos(self, obj):
        return obj.alunos.count()


class TurmaSimpleSerializer(serializers.ModelSerializer):
    """Serializer simplificado para Turma (sem alunos)"""
    professor_responsavel_nome = serializers.CharField(source='professor_responsavel.get_full_name', read_only=True)
    total_alunos = serializers.SerializerMethodField()
    
    class Meta:
        model = Turma
        fields = [
            'id', 'nome', 'ano_letivo', 'periodo',
            'professor_responsavel_nome', 'data_criacao', 'ativa', 'total_alunos'
        ]
        read_only_fields = ['id', 'data_criacao']
    
    def get_total_alunos(self, obj):
        return obj.alunos.count()


class MensalidadeSerializer(serializers.ModelSerializer):
    """Serializer para model Mensalidade"""
    aluno = AlunoSerializer(read_only=True)
    aluno_id = serializers.PrimaryKeyRelatedField(
        queryset=Aluno.objects.all(),
        source='aluno',
        write_only=True
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Mensalidade
        fields = [
            'id', 'aluno', 'aluno_id', 'valor', 'vencimento', 'status',
            'status_display', 'data_pagamento', 'observacoes', 'data_cadastro'
        ]
        read_only_fields = ['id', 'data_cadastro']


class MensalidadeSimpleSerializer(serializers.ModelSerializer):
    """Serializer simplificado para Mensalidade"""
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Mensalidade
        fields = [
            'id', 'aluno_nome', 'valor', 'vencimento', 'status',
            'status_display', 'data_pagamento', 'data_cadastro'
        ]
        read_only_fields = ['id', 'data_cadastro']
