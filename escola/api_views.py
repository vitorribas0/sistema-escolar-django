from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Usuario, Aluno, Turma, Mensalidade
from .serializers import (
    UsuarioSerializer, AlunoSerializer, TurmaSerializer,
    TurmaSimpleSerializer, MensalidadeSerializer, MensalidadeSimpleSerializer
)


class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualização de usuários.
    Somente leitura - gerenciamento via admin.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    filterset_fields = ['tipo', 'is_staff', 'is_active']


class AlunoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo de alunos.
    """
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nome', 'documento', 'nome_pai', 'nome_mae']
    filterset_fields = ['ativo']
    ordering_fields = ['nome', 'data_cadastro']
    ordering = ['nome']

    @action(detail=True, methods=['get'])
    def turmas(self, request, pk=None):
        """Retorna as turmas de um aluno específico"""
        aluno = self.get_object()
        turmas = aluno.turmas.all()
        serializer = TurmaSimpleSerializer(turmas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def mensalidades(self, request, pk=None):
        """Retorna as mensalidades de um aluno específico"""
        aluno = self.get_object()
        mensalidades = aluno.mensalidades.all()
        serializer = MensalidadeSimpleSerializer(mensalidades, many=True)
        return Response(serializer.data)


class TurmaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo de turmas.
    """
    queryset = Turma.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nome']
    filterset_fields = ['ano_letivo', 'periodo', 'ativa']
    ordering_fields = ['nome', 'ano_letivo', 'data_criacao']
    ordering = ['-ano_letivo', 'nome']

    def get_serializer_class(self):
        """Usa serializer simplificado para list, completo para retrieve"""
        if self.action == 'list':
            return TurmaSimpleSerializer
        return TurmaSerializer

    @action(detail=True, methods=['post'])
    def adicionar_aluno(self, request, pk=None):
        """Adiciona um aluno à turma"""
        turma = self.get_object()
        aluno_id = request.data.get('aluno_id')
        
        try:
            aluno = Aluno.objects.get(pk=aluno_id)
            turma.alunos.add(aluno)
            return Response({'status': 'Aluno adicionado à turma'})
        except Aluno.DoesNotExist:
            return Response({'error': 'Aluno não encontrado'}, status=404)

    @action(detail=True, methods=['post'])
    def remover_aluno(self, request, pk=None):
        """Remove um aluno da turma"""
        turma = self.get_object()
        aluno_id = request.data.get('aluno_id')
        
        try:
            aluno = Aluno.objects.get(pk=aluno_id)
            turma.alunos.remove(aluno)
            return Response({'status': 'Aluno removido da turma'})
        except Aluno.DoesNotExist:
            return Response({'error': 'Aluno não encontrado'}, status=404)


class MensalidadeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo de mensalidades.
    """
    queryset = Mensalidade.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['aluno__nome']
    filterset_fields = ['status', 'vencimento']
    ordering_fields = ['vencimento', 'valor', 'data_cadastro']
    ordering = ['-vencimento']

    def get_serializer_class(self):
        """Usa serializer simplificado para list, completo para outros"""
        if self.action == 'list':
            return MensalidadeSimpleSerializer
        return MensalidadeSerializer

    @action(detail=True, methods=['post'])
    def marcar_como_paga(self, request, pk=None):
        """Marca uma mensalidade como paga"""
        mensalidade = self.get_object()
        from django.utils import timezone
        mensalidade.status = 'pago'
        mensalidade.data_pagamento = timezone.now().date()
        mensalidade.save()
        serializer = self.get_serializer(mensalidade)
        return Response(serializer.data)
