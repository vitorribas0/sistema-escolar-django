from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from decimal import Decimal
from escola.models import Aluno, Mensalidade


class Command(BaseCommand):
    help = 'Gera mensalidades automáticas para todos os alunos ativos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mes',
            type=int,
            help='Mês para gerar mensalidades (1-12)',
        )
        parser.add_argument(
            '--ano',
            type=int,
            help='Ano para gerar mensalidades',
        )
        parser.add_argument(
            '--valor',
            type=float,
            default=450.00,
            help='Valor padrão da mensalidade',
        )

    def handle(self, *args, **options):
        hoje = date.today()
        mes = options['mes'] or hoje.month
        ano = options['ano'] or hoje.year
        valor_padrao = Decimal(str(options['valor']))

        # Data de vencimento: dia 10 do mês
        vencimento = date(ano, mes, 10)

        alunos_ativos = Aluno.objects.filter(ativo=True)
        total_alunos = alunos_ativos.count()

        if total_alunos == 0:
            self.stdout.write(self.style.WARNING('Nenhum aluno ativo encontrado.'))
            return

        criadas = 0
        ja_existentes = 0

        self.stdout.write(f'\n🎓 Gerando mensalidades para {mes}/{ano}...\n')

        for aluno in alunos_ativos:
            # Verifica se já existe mensalidade para este mês
            existe = Mensalidade.objects.filter(
                aluno=aluno,
                vencimento__year=ano,
                vencimento__month=mes
            ).exists()

            if existe:
                ja_existentes += 1
                self.stdout.write(f'   ⚠️  {aluno.nome} - Já possui mensalidade')
            else:
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
                    observacoes=f'Mensalidade gerada automaticamente - {mes}/{ano}'
                )
                criadas += 1
                self.stdout.write(self.style.SUCCESS(f'   ✅ {aluno.nome} - R$ {valor_aluno} - Mensalidade criada'))

        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'\n✅ Processo concluído!'))
        self.stdout.write(f'\n📊 Resumo:')
        self.stdout.write(f'   • Total de alunos ativos: {total_alunos}')
        self.stdout.write(f'   • Mensalidades criadas: {criadas}')
        self.stdout.write(f'   • Já existentes: {ja_existentes}')
        self.stdout.write(f'   • Valor unitário: R$ {valor_padrao}')
        self.stdout.write(f'   • Valor total gerado: R$ {valor_padrao * criadas}')
        self.stdout.write('\n' + '='*60 + '\n')
