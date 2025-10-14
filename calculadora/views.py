from django.shortcuts import render
from .models import Analise

def pagina_inicial(request):
    analises_recentes = Analise.objects.order_by('-criado_em')[:5]

    contexto = {
        'analises': analises_recentes
    }
    return render(request, 'calculadora/pagina_inicial.html', contexto)

def pagina_encontrar_raiz(request):
    contexto = {}
    if request.method == 'POST':
        funcao = request.POST.get('funcao_texto')
        intervalo_a = float(request.POST.get('intervalo_a'))
        intervalo_b = float(request.POST.get('intervalo_b'))
        metodo = request.POST.get('metodo')

        #implementar logica do calculo aqui
        resultado_final = 1.52138
        Analise.objects.create(
            funcao_texto=funcao,
            intervalo_a=intervalo_a,
            intervalo_b=intervalo_b,
            metodo_utilizado=metodo,
            resultado=resultado_final
        )
        contexto['resultado'] = resultado_final
        contexto['metodo_utilizado'] = metodo.replace("_", " ").title()

    return render(request, 'calculadora/pagina_encontrar_raiz.html', contexto)