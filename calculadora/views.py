from django.shortcuts import render
import sympy
from .metodos import calcular_bissecao

def pagina_inicial(request):
    return render(request, 'calculadora/pagina_inicial.html')

def pagina_encontrar_raiz(request):
    contexto = {}
    if request.method == 'POST':
        funcao_texto = request.POST.get('funcao_texto')
        intervalo_a = float(request.POST.get('intervalo_a'))
        intervalo_b = float(request.POST.get('intervalo_b'))
        metodo = request.POST.get('metodo')
        try:
            x = sympy.symbols('x')
            funcao_simbolica = sympy.sympify(funcao_texto)
            funcao_executavel = sympy.lambdify(x, funcao_simbolica, 'numpy')
            resultado_final = None
            iteracoes = []
            metodo_nome_exibicao = metodo.replace("_", " ").title()
            if metodo == 'bissecao':
                resultado_final, iteracoes = calcular_bissecao(
                    funcao_executavel, 
                    intervalo_a, 
                    intervalo_b
                )
            if resultado_final is not None:
                contexto['resultado'] = round(resultado_final, 5)
                contexto['metodo_utilizado'] = metodo_nome_exibicao
                contexto['iteracoes'] = iteracoes
            else:
                contexto['erro'] = f"Não foi possível encontrar uma raiz no intervalo [{intervalo_a}, {intervalo_b}] com o {metodo_nome_exibicao}."

        except Exception as e:
            contexto['erro'] = f"Erro ao processar a função: {e}"
    return render(request, 'calculadora/pagina_encontrar_raiz.html', contexto)