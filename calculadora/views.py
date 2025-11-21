from django.shortcuts import render, redirect
from django.http import HttpResponse
import sympy
import numpy as np
import re
from .metodos import (
    calcular_bissecao, calcular_falsa_posicao, calcular_newton,
    calcular_gauss, calcular_gauss_jordan, calcular_jacobi
)
from .models import Sessao
import json

def pagina_inicial(request):
    return render(request, 'calculadora/pagina_inicial.html')

def pagina_encontrar_raiz(request):
    contexto = {}

    if request.method == 'POST':
        funcao_texto = request.POST.get('funcao_texto')
        metodo = request.POST.get('metodo')
        nomes_metodos = {
            'bissecao': 'Método da Bisseção',
            'falsa_posicao': 'Método da Falsa Posição',
            'newton': 'Método de Newton-Raphson'
        }
        metodo_nome_exibicao = nomes_metodos.get(metodo, metodo.replace("_", " ").title())
        
        intervalo_a = request.POST.get('intervalo_a', '')
        intervalo_b = request.POST.get('intervalo_b', '')
        estimativa_inicial = request.POST.get('estimativa_inicial', '')

        try:
            funcao_formatada = funcao_texto.replace('^', '**')
            
            funcao_formatada = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', funcao_formatada)
            
            funcao_formatada = re.sub(r'([a-zA-Z])(\()', r'\1*\2', funcao_formatada)

            funcao_formatada = re.sub(r'(\))([a-zA-Z])', r'\1*\2', funcao_formatada)

            funcao_formatada = re.sub(r'(\))(\()', r'\1*\2', funcao_formatada)

            funcao_formatada = re.sub(r'(\d)(\()', r'\1*\2', funcao_formatada)

            x = sympy.symbols('x')
            funcao_simbolica = sympy.sympify(funcao_formatada)
            funcao_executavel = sympy.lambdify(x, funcao_simbolica, 'numpy')

            resultado_final = None
            iteracoes = []
            
            if metodo == 'bissecao':
                resultado_final, iteracoes = calcular_bissecao(
                    funcao_executavel, float(intervalo_a), float(intervalo_b)
                )
            elif metodo == 'falsa_posicao':
                resultado_final, iteracoes = calcular_falsa_posicao(
                    funcao_executavel, float(intervalo_a), float(intervalo_b)
                )
            elif metodo == 'newton':
                derivada_simbolica = sympy.diff(funcao_simbolica, x)
                derivada_executavel = sympy.lambdify(x, derivada_simbolica, 'numpy')
                resultado_final, iteracoes = calcular_newton(
                    funcao_executavel, 
                    derivada_executavel, 
                    float(estimativa_inicial)
                )
            
            if resultado_final is not None:
                contexto['resultado'] = round(resultado_final, 5)
                contexto['metodo_utilizado'] = metodo_nome_exibicao
                contexto['metodo_selecionado'] = metodo
                contexto['iteracoes'] = iteracoes

                relatorio = f"=== RELATÓRIO ===\nFERRAMENTA: Encontrar Raíz\nMÉTODO: {metodo_nome_exibicao}\nFUNÇÃO: {funcao_texto}\nRESULTADO: {round(resultado_final, 5)}\n"
                request.session['relatorio_download'] = relatorio
                request.session['dados_sessao_atual'] = {
                    'tipo': 'raiz',
                    'metodo': metodo,
                    'inputs': {
                        'funcao_texto': funcao_texto,
                        'intervalo_a': intervalo_a,
                        'intervalo_b': intervalo_b,
                        'estimativa_inicial': estimativa_inicial
                    },
                    'outputs': {
                        'resultado': round(resultado_final, 5),
                        'iteracoes': iteracoes
                    }
                }

            else:
                contexto['erro'] = f"Não foi possível encontrar uma raiz com o {metodo_nome_exibicao}."

        except Exception as e:
            contexto['erro'] = f"Erro ao processar a função. Verifique a sintaxe. (Erro: {e})"
    
    return render(request, 'calculadora/pagina_encontrar_raiz.html', contexto)

def pagina_sistemas_lineares(request):
    contexto = {}
    
    if request.method == 'POST':
        try:
            M_linhas = int(request.POST.get('matrix_rows'))
            N_colunas = int(request.POST.get('matrix_cols'))
            metodo = request.POST.get('metodo')
            metodo_nome_exibicao = metodo.replace("_", " ").title()

            if M_linhas != N_colunas:
                contexto['erro'] = f"Erro: O método {metodo_nome_exibicao} exige uma matriz quadrada."
                return render(request, 'calculadora/pagina_sistemas_lineares.html', contexto)

            matriz_A = []
            vetor_b = []
            
            inputs_matriz = {
                'matrix_rows': M_linhas,
                'matrix_cols': N_colunas,
                'metodo': metodo
            }

            for i in range(M_linhas):
                linha = []
                for j in range(N_colunas):
                    nome_campo_a = f'a_{i}_{j}'
                    valor = float(request.POST.get(nome_campo_a))
                    linha.append(valor)
                    inputs_matriz[nome_campo_a] = request.POST.get(nome_campo_a) # Salva para a sessão
                
                matriz_A.append(linha)
                
                nome_campo_b = f'b_{i}'
                valor_b = float(request.POST.get(nome_campo_b))
                vetor_b.append(valor_b)
                inputs_matriz[nome_campo_b] = request.POST.get(nome_campo_b) # Salva para a sessão

            solucao = None
            iteracoes = []

            if metodo == 'gauss':
                solucao, iteracoes = calcular_gauss(matriz_A, vetor_b)
            elif metodo == 'gauss_jordan':
                solucao, iteracoes = calcular_gauss_jordan(matriz_A, vetor_b)
            elif metodo == 'jacobi':
                solucao, iteracoes = calcular_jacobi(matriz_A, vetor_b)

            if solucao is not None:
                solucao_arredondada = [round(val, 5) for val in solucao]
                contexto['solucao'] = solucao_arredondada
                contexto['iteracoes'] = iteracoes
                contexto['metodo_utilizado'] = metodo_nome_exibicao

                relatorio = f"=== RELATÓRIO ===\nFERRAMENTA: Sistemas Lineares\nMÉTODO: {metodo_nome_exibicao}\nSOLUÇÃO: {solucao_arredondada}\n"
                request.session['relatorio_download'] = relatorio
                
                request.session['dados_sessao_atual'] = {
                    'tipo': 'sistema',
                    'metodo': metodo,
                    'inputs': inputs_matriz,
                    'outputs': {
                        'solucao': solucao_arredondada,
                        'iteracoes': iteracoes
                    }
                }

            else:
                contexto['erro'] = f"Não foi possível encontrar uma solução com {metodo_nome_exibicao}."

        except Exception as e:
            contexto['erro'] = f"Erro ao processar a matriz: {e}"

    return render(request, 'calculadora/pagina_sistemas_lineares.html', contexto)


def baixar_relatorio(request):
    conteudo_relatorio = request.session.get('relatorio_download', 'Nenhum cálculo realizado recentemente.')
    response = HttpResponse(conteudo_relatorio, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="relatorio_calculo.txt"'
    return response

def salvar_sessao(request):
    dados_para_salvar = request.session.get('dados_sessao_atual')
    
    if dados_para_salvar:
        Sessao.objects.create(
            tipo_ferramenta=dados_para_salvar['tipo'],
            metodo=dados_para_salvar['metodo'],
            dados_input=dados_para_salvar['inputs'],
            dados_output=dados_para_salvar['outputs']
        )
        return redirect('historico') 
    return redirect('pagina_inicial')

def pagina_historico(request):
    sessoes = Sessao.objects.order_by('-data_criacao')
    return render(request, 'calculadora/historico.html', {'sessoes': sessoes})

def carregar_sessao(request, sessao_id):
    try:
        sessao = Sessao.objects.get(id=sessao_id)
        
        contexto = {
            'inputs': sessao.dados_input,
            'resultado': sessao.dados_output.get('resultado'),
            'iteracoes': sessao.dados_output.get('iteracoes'),
            'solucao': sessao.dados_output.get('solucao'),
            'metodo_utilizado': sessao.metodo.replace("_", " ").title(),
            'metodo_selecionado': sessao.metodo
        }
        
        if sessao.tipo_ferramenta == 'raiz':
            return render(request, 'calculadora/pagina_encontrar_raiz.html', contexto)
        elif sessao.tipo_ferramenta == 'sistema':
            return render(request, 'calculadora/pagina_sistemas_lineares.html', contexto)

    except Sessao.DoesNotExist:
        return redirect('historico')