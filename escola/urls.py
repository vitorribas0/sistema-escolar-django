from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('alunos/', views.aluno_lista, name='aluno_lista'),
    path('alunos/novo/', views.aluno_criar, name='aluno_criar'),
    path('alunos/<int:pk>/', views.aluno_detalhe, name='aluno_detalhe'),
    path('alunos/<int:pk>/editar/', views.aluno_editar, name='aluno_editar'),
    path('alunos/<int:pk>/historico/', views.historico_pagamentos, name='historico_pagamentos'),
    path('turmas/', views.turma_lista, name='turma_lista'),
    path('turmas/<int:pk>/', views.turma_detalhe, name='turma_detalhe'),
    path('mensalidades/', views.mensalidade_lista, name='mensalidade_lista'),
    path('mensalidades/gerar/', views.gerar_mensalidades, name='gerar_mensalidades'),
    path('mensalidades/<int:pk>/recibo/', views.recibo, name='recibo'),
]
