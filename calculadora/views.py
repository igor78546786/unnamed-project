from django.shortcuts import render

def pagina_inicial(request):
    return render(request, 'calculadora/pagina_inicial.html', contexto)

def pagina_encontrar_raiz(request):
    contexto = {}
    if request.method == 'POST':
        funcao = request.POST.get('funcao_texto')
        intervalo_a = float(request.POST.get('intervalo_a'))
        intervalo_b = float(request.POST.get('intervalo_b'))
        metodo = request.POST.get('metodo')



        resultado_final = 1.52138 # placeholder


        contexto['resultado'] = resultado_final
        contexto['metodo_utilizado'] = metodo.replace("_", " ").title()

    return render(request, 'calculadora/pagina_encontrar_raiz.html')