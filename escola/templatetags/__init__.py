from django import template

register = template.Library()

@register.filter
def extenso(valor):
    """Converte um valor numérico para extenso (simplificado)"""
    try:
        valor = float(valor)
        inteiro = int(valor)
        centavos = int((valor - inteiro) * 100)
        
        # Unidades
        unidades = ['', 'um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove']
        # Dezenas
        dezenas = ['', '', 'vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa']
        # Números especiais de 10 a 19
        especiais = ['dez', 'onze', 'doze', 'treze', 'quatorze', 'quinze', 'dezesseis', 'dezessete', 'dezoito', 'dezenove']
        # Centenas
        centenas = ['', 'cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos', 'setecentos', 'oitocentos', 'novecentos']
        
        def numero_por_extenso(n):
            if n == 0:
                return 'zero'
            if n == 100:
                return 'cem'
            
            resultado = []
            
            # Centenas
            c = n // 100
            if c > 0:
                resultado.append(centenas[c])
            
            # Dezenas e unidades
            resto = n % 100
            if resto >= 10 and resto < 20:
                resultado.append(especiais[resto - 10])
            else:
                d = resto // 10
                u = resto % 10
                if d > 0:
                    resultado.append(dezenas[d])
                if u > 0:
                    if d > 0:
                        resultado.append('e')
                    resultado.append(unidades[u])
            
            return ' '.join(resultado)
        
        # Milhares
        if inteiro >= 1000:
            milhares = inteiro // 1000
            if milhares == 1:
                resultado_reais = 'mil'
            else:
                resultado_reais = numero_por_extenso(milhares) + ' mil'
            
            resto = inteiro % 1000
            if resto > 0:
                if resto < 100:
                    resultado_reais += ' e ' + numero_por_extenso(resto)
                else:
                    resultado_reais += ' ' + numero_por_extenso(resto)
        else:
            resultado_reais = numero_por_extenso(inteiro)
        
        # Adiciona "reais"
        if inteiro == 1:
            resultado_reais += ' real'
        else:
            resultado_reais += ' reais'
        
        # Centavos
        if centavos > 0:
            resultado_centavos = numero_por_extenso(centavos)
            if centavos == 1:
                resultado_centavos += ' centavo'
            else:
                resultado_centavos += ' centavos'
            
            return resultado_reais + ' e ' + resultado_centavos
        
        return resultado_reais
        
    except (ValueError, TypeError):
        return str(valor)
