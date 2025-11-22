from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import UsuarioViewSet, AlunoViewSet, TurmaViewSet, MensalidadeViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'alunos', AlunoViewSet, basename='aluno')
router.register(r'turmas', TurmaViewSet, basename='turma')
router.register(r'mensalidades', MensalidadeViewSet, basename='mensalidade')

urlpatterns = [
    path('', include(router.urls)),
]
