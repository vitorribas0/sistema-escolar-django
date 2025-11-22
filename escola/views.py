from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.contrib import messages
from .models import Aluno, Turma, Mensalidade


@login_required
def home(request):
    """View para página inicial com dashboard"""
    total_alunos = Aluno.objects.filter(ativo=True).count()
    total_turmas = Turma.objects.filter(ativa=True).count()
    mensalidades_pendentes = Mensalidade.objects.filter(status='pendente').count()
    mensalidades_pagas = Mensalidade.objects.filter(status='pago').count()
    mensalidades_atrasadas = Mensalidade.objects.filter(status='atrasado').order_by('vencimento')[:5]
    turmas_ativas = Turma.objects.filter(ativa=True).prefetch_related('alunos')[:5]
    
    context = {
        'total_alunos': total_alunos,
        'total_turmas': total_turmas,
        'mensalidades_pendentes': mensalidades_pendentes,
        'mensalidades_pagas': mensalidades_pagas,
        'mensalidades_atrasadas': mensalidades_atrasadas,
        'turmas_ativas': turmas_ativas,
    }
    return render(request, 'home.html', context)


@login_required
def aluno_lista(request):
    """View para listagem de alunos"""
    alunos = Aluno.objects.all().order_by('nome')
    
    # Filtro de busca
    query = request.GET.get('q')
    if query:
        alunos = alunos.filter(
            Q(nome__icontains=query) |
            Q(documento__icontains=query) |
            Q(nome_pai__icontains=query) |
            Q(nome_mae__icontains=query)
        )
    
    context = {
        'alunos': alunos,
    }
    return render(request, 'aluno_lista.html', context)


@login_required
def aluno_detalhe(request, pk):
    """View para detalhes de um aluno"""
    aluno = get_object_or_404(Aluno, pk=pk)
    context = {
        'aluno': aluno,
    }
    return render(request, 'aluno_detalhe.html', context)


@login_required
def aluno_criar(request):
    """View para criar novo aluno"""
    if request.method == 'POST':
        try:
            aluno = Aluno()
            aluno.nome = request.POST.get('nome')
            aluno.documento = request.POST.get('documento')
            aluno.data_nascimento = request.POST.get('data_nascimento') or None
            aluno.nome_pai = request.POST.get('nome_pai', '')
            aluno.nome_mae = request.POST.get('nome_mae', '')
            aluno.endereco = request.POST.get('endereco', '')
            aluno.telefone = request.POST.get('telefone', '')
            aluno.email = request.POST.get('email', '')
            aluno.valor_mensalidade = request.POST.get('valor_mensalidade', 450.00)
            aluno.ativo = request.POST.get('ativo') == 'on'
            
            if request.FILES.get('foto'):
                aluno.foto = request.FILES['foto']
            
            aluno.save()
            messages.success(request, f'Aluno {aluno.nome} cadastrado com sucesso!')
            return redirect('aluno_detalhe', pk=aluno.id)
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar aluno: {str(e)}')
    
    return render(request, 'aluno_form.html', {'titulo': 'Novo Aluno', 'aluno': None})


@login_required
def aluno_editar(request, pk):
    """View para editar aluno"""
    aluno = get_object_or_404(Aluno, pk=pk)
    
    if request.method == 'POST':
        try:
            aluno.nome = request.POST.get('nome')
            aluno.documento = request.POST.get('documento')
            aluno.data_nascimento = request.POST.get('data_nascimento') or None
            aluno.nome_pai = request.POST.get('nome_pai', '')
            aluno.nome_mae = request.POST.get('nome_mae', '')
            aluno.endereco = request.POST.get('endereco', '')
            aluno.telefone = request.POST.get('telefone', '')
            aluno.email = request.POST.get('email', '')
            aluno.valor_mensalidade = request.POST.get('valor_mensalidade', 450.00)
            aluno.ativo = request.POST.get('ativo') == 'on'
            
            if request.FILES.get('foto'):
                aluno.foto = request.FILES['foto']
            
            aluno.save()
            messages.success(request, f'Aluno {aluno.nome} atualizado com sucesso!')
            return redirect('aluno_detalhe', pk=aluno.id)
        except Exception as e:
            messages.error(request, f'Erro ao atualizar aluno: {str(e)}')
    
    return render(request, 'aluno_form.html', {'titulo': 'Editar Aluno', 'aluno': aluno})


@login_required
def turma_lista(request):
    """View para listagem de turmas"""
    turmas = Turma.objects.all().prefetch_related('alunos', 'professor_responsavel').order_by('-ano_letivo', 'nome')
    
    context = {
        'turmas': turmas,
    }
    return render(request, 'turma_lista.html', context)


@login_required
def turma_detalhe(request, pk):
    """View para detalhes de uma turma"""
    turma = get_object_or_404(Turma.objects.prefetch_related('alunos'), pk=pk)
    context = {
        'turma': turma,
    }
    return render(request, 'turma_detalhe.html', context)


@login_required
def mensalidade_lista(request):
    """View para listagem de mensalidades"""
    from django.contrib import messages
    from django.shortcuts import redirect
    from django.utils import timezone
    
    # Ação rápida para mudar status
    if request.method == 'POST' and 'mensalidade_id' in request.POST:
        mensalidade_id = request.POST.get('mensalidade_id')
        novo_status = request.POST.get('status')
        mensalidade = get_object_or_404(Mensalidade, pk=mensalidade_id)
        
        mensalidade.status = novo_status
        if novo_status == 'pago':
            mensalidade.data_pagamento = timezone.now().date()
        else:
            mensalidade.data_pagamento = None
        mensalidade.save()
        
        messages.success(request, f'Status atualizado para {mensalidade.get_status_display()}!')
        return redirect('mensalidade_lista')
    
    mensalidades = Mensalidade.objects.all().select_related('aluno').order_by('-vencimento')
    
    # Filtro de busca por nome
    query = request.GET.get('q')
    if query:
        mensalidades = mensalidades.filter(aluno__nome__icontains=query)
    
    # Filtro por status da mensalidade
    status = request.GET.get('status')
    if status:
        mensalidades = mensalidades.filter(status=status)
    
    # Filtro por período (mês/ano inicial e final)
    mes_inicial = request.GET.get('mes_inicial')
    ano_inicial = request.GET.get('ano_inicial')
    mes_final = request.GET.get('mes_final')
    ano_final = request.GET.get('ano_final')
    
    if mes_inicial and ano_inicial:
        from datetime import date
        data_inicial = date(int(ano_inicial), int(mes_inicial), 1)
        mensalidades = mensalidades.filter(vencimento__gte=data_inicial)
    
    if mes_final and ano_final:
        from datetime import date
        import calendar
        ultimo_dia = calendar.monthrange(int(ano_final), int(mes_final))[1]
        data_final = date(int(ano_final), int(mes_final), ultimo_dia)
        mensalidades = mensalidades.filter(vencimento__lte=data_final)
    
    # Filtro por status do aluno (ativo/inativo)
    aluno_ativo = request.GET.get('aluno_ativo')
    if aluno_ativo:
        if aluno_ativo == '1':
            mensalidades = mensalidades.filter(aluno__ativo=True)
        elif aluno_ativo == '0':
            mensalidades = mensalidades.filter(aluno__ativo=False)
    
    # Cálculo dos totais
    total_pago = mensalidades.filter(status='pago').aggregate(total=Sum('valor'))['total'] or 0
    total_pendente = mensalidades.filter(status='pendente').aggregate(total=Sum('valor'))['total'] or 0
    total_atrasado = mensalidades.filter(status='atrasado').aggregate(total=Sum('valor'))['total'] or 0
    total_geral = total_pago + total_pendente + total_atrasado
    
    # Anos disponíveis para o filtro
    anos_disponiveis = Mensalidade.objects.dates('vencimento', 'year', order='DESC')
    
    context = {
        'mensalidades': mensalidades,
        'total_pago': total_pago,
        'total_pendente': total_pendente,
        'total_atrasado': total_atrasado,
        'total_geral': total_geral,
        'anos_disponiveis': anos_disponiveis,
    }
    return render(request, 'mensalidade_lista.html', context)


@login_required
def recibo(request, pk):
    """View para emissão de recibo de mensalidade"""
    from django.utils import timezone
    mensalidade = get_object_or_404(Mensalidade, pk=pk)
    context = {
        'mensalidade': mensalidade,
        'hoje': timezone.now(),
        'forma_pagamento': request.GET.get('forma', 'Dinheiro'),
    }
    return render(request, 'recibo.html', context)


@login_required
def historico_pagamentos(request, pk):
    """View para histórico de pagamentos de um aluno"""
    from django.utils import timezone
    from django.db.models import Count, Avg
    
    aluno = get_object_or_404(Aluno, pk=pk)
    mensalidades = aluno.mensalidades.all().order_by('-vencimento')
    
    # Estatísticas
    total_pagas = mensalidades.filter(status='pago').count()
    total_pendentes = mensalidades.filter(status='pendente').count()
    total_atrasadas = mensalidades.filter(status='atrasado').count()
    total_mensalidades = mensalidades.count()
    
    valor_pago = sum(m.valor for m in mensalidades.filter(status='pago'))
    valor_pendente = sum(m.valor for m in mensalidades.filter(status='pendente'))
    valor_atrasado = sum(m.valor for m in mensalidades.filter(status='atrasado'))
    valor_total = valor_pago + valor_pendente + valor_atrasado
    
    # Percentual de pagamento
    percentual_pagamento = (total_pagas / total_mensalidades * 100) if total_mensalidades > 0 else 0
    
    # Ticket médio
    ticket_medio = mensalidades.aggregate(media=Avg('valor'))['media'] or 0
    
    # Meses consecutivos em dia (simplificado)
    meses_consecutivos = 0
    for mens in mensalidades.filter(status='pago').order_by('-vencimento'):
        meses_consecutivos += 1
    
    context = {
        'aluno': aluno,
        'mensalidades': mensalidades,
        'total_pagas': total_pagas,
        'total_pendentes': total_pendentes,
        'total_atrasadas': total_atrasadas,
        'total_mensalidades': total_mensalidades,
        'valor_pago': valor_pago,
        'valor_pendente': valor_pendente,
        'valor_atrasado': valor_atrasado,
        'valor_total': valor_total,
        'percentual_pagamento': percentual_pagamento,
        'ticket_medio': ticket_medio,
        'meses_consecutivos': meses_consecutivos,
        'hoje': timezone.now(),
    }
    return render(request, 'historico_pagamentos.html', context)


@login_required
def gerar_mensalidades(request):
    """View para gerar mensalidades automáticas"""
    from django.contrib import messages
    from django.utils import timezone
    from datetime import date
    from decimal import Decimal
    
    hoje = date.today()
    
    if request.method == 'POST':
        mes = int(request.POST.get('mes'))
        ano = int(request.POST.get('ano'))
        
        # Data de vencimento: dia 10 do mês
        vencimento = date(ano, mes, 10)
        
        alunos_ativos = Aluno.objects.filter(ativo=True)
        criadas = 0
        ja_existentes = 0
        
        for aluno in alunos_ativos:
            # Verifica se já existe mensalidade para este mês
            existe = Mensalidade.objects.filter(
                aluno=aluno,
                vencimento__year=ano,
                vencimento__month=mes
            ).exists()
            
            if not existe:
                # Determina o status baseado na data
                if vencimento < hoje:
                    status = 'atrasado'
                else:
                    status = 'pendente'
                
                # Usa o valor individual do aluno
                valor_aluno = aluno.valor_mensalidade
                
                Mensalidade.objects.create(
                    aluno=aluno,
                    valor=valor_aluno,
                    vencimento=vencimento,
                    status=status,
                    observacoes=f'Mensalidade gerada automaticamente - {mes:02d}/{ano}'
                )
                criadas += 1
            else:
                ja_existentes += 1
        
        if criadas > 0:
            messages.success(request, f'✅ {criadas} mensalidade(s) gerada(s) com sucesso para {mes:02d}/{ano}!')
        if ja_existentes > 0:
            messages.info(request, f'⚠️ {ja_existentes} aluno(s) já possuíam mensalidade para este período.')
        if criadas == 0 and ja_existentes == 0:
            messages.warning(request, 'Nenhum aluno ativo encontrado.')
    
    context = {
        'total_alunos': Aluno.objects.filter(ativo=True).count(),
        'mes_atual': hoje.month,
        'ano_atual': hoje.year,
        'ultima_geracao': Mensalidade.objects.filter(
            observacoes__contains='gerada automaticamente'
        ).order_by('-data_cadastro').first(),
        'total_ultima_geracao': Mensalidade.objects.filter(
            observacoes__contains='gerada automaticamente',
            data_cadastro__date=hoje
        ).count(),
    }
    return render(request, 'gerar_mensalidades.html', context)
