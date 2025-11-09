from django.shortcuts import render
import sympy
from .metodos import calcular_bissecao, calcular_falsa_posicao, calcular_newton, calcular_gauss

def pagina_inicial(request):
    return render(request, 'calculadora/pagina_inicial.html')

def pagina_encontrar_raiz(request):
    contexto = {}

    if request.method == 'POST':
        funcao_texto = request.POST.get('funcao_texto')
        metodo = request.POST.get('metodo')
        metodo_nome_exibicao = metodo.replace("_", " ").title()

        try:
            x = sympy.symbols('x')
            funcao_simbolica = sympy.sympify(funcao_texto)
            funcao_executavel = sympy.lambdify(x, funcao_simbolica, 'numpy')

            resultado_final = None
            iteracoes = []
            if metodo == 'bissecao':
                intervalo_a = float(request.POST.get('intervalo_a'))
                intervalo_b = float(request.POST.get('intervalo_b'))
                
                resultado_final, iteracoes = calcular_bissecao(
                    funcao_executavel, intervalo_a, intervalo_b
                )
            
            elif metodo == 'falsa_posicao':
                intervalo_a = float(request.POST.get('intervalo_a'))
                intervalo_b = float(request.POST.get('intervalo_b'))

                resultado_final, iteracoes = calcular_falsa_posicao(
                    funcao_executavel, intervalo_a, intervalo_b
                )

            elif metodo == 'newton':
                estimativa_inicial = float(request.POST.get('estimativa_inicial'))
                derivada_simbolica = sympy.diff(funcao_simbolica, x)
                derivada_executavel = sympy.lambdify(x, derivada_simbolica, 'numpy')
                resultado_final, iteracoes = calcular_newton(
                    funcao_executavel, 
                    derivada_executavel, 
                    estimativa_inicial
                )
            if resultado_final is not None:
                contexto['resultado'] = round(resultado_final, 5)
                contexto['metodo_utilizado'] = metodo_nome_exibicao
                contexto['iteracoes'] = iteracoes
            else:
                contexto['erro'] = f"Não foi possível encontrar uma raiz com o {metodo_nome_exibicao}. Verifique o intervalo ou a estimativa inicial."

        except Exception as e:
            contexto['erro'] = f"Erro ao processar a função: {e}. (Lembre-se de usar '**' para potência)"
    return render(request, 'calculadora/pagina_encontrar_raiz.html', contexto)

def pagina_sistemas_lineares(request):
    contexto = {}
    
    if request.method == 'POST':
        try:
            M_linhas = int(request.POST.get('matrix_rows'))
            N_colunas = int(request.POST.get('matrix_cols'))
            metodo = request.POST.get('metodo')

            if M_linhas != N_colunas:
                contexto['erro'] = f"Erro: O método de Eliminação Gaussiana implementado assume um sistema quadrado (Nº de equações = Nº de variáveis). Você inseriu {M_linhas}x{N_colunas}."
                return render(request, 'calculadora/pagina_sistemas_lineares.html', contexto)

            matriz_A = []
            vetor_b = []

            for i in range(M_linhas):
                linha = []
                for j in range(N_colunas):
                    nome_campo_a = f'a_{i}_{j}'
                    valor = float(request.POST.get(nome_campo_a))
                    linha.append(valor)
                
                matriz_A.append(linha)
                nome_campo_b = f'b_{i}'
                valor_b = float(request.POST.get(nome_campo_b))
                vetor_b.append(valor_b)

            if metodo == 'gauss':
                solucao, iteracoes = calcular_gauss(matriz_A, vetor_b)

                if solucao is not None:
                    contexto['solucao'] = [round(val, 5) for val in solucao]
                    contexto['iteracoes'] = iteracoes
                else:
                    contexto['erro'] = "A matriz é singular. O sistema não possui solução única ou tem infinitas soluções."

        except Exception as e:
            contexto['erro'] = f"Erro ao processar a matriz: {e}"

    return render(request, 'calculadora/pagina_sistemas_lineares.html', contexto)