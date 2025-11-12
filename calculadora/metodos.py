import numpy as np

def calcular_bissecao(funcao, a, b, tolerancia=1e-5, max_iter=100):

    iteracoes = []

    if funcao(a) * funcao(b) >= 0:
        print("Erro: A função não muda de sinal no intervalo [a, b].")
        return None, iteracoes

    p = a
    for i in range(max_iter):
        p = (a + b) / 2
        f_p = funcao(p)
        iteracoes.append({'n': i + 1, 'a': a, 'b': b, 'p': p, 'f_p': f_p})
        if f_p == 0 or (b - a) / 2 < tolerancia:
            return p, iteracoes
        if funcao(a) * f_p < 0:
            b = p
        else:
            a = p

    print("Aviso: O método excedeu o número máximo de iterações.")
    return p, iteracoes

def calcular_falsa_posicao(funcao, a, b, tolerancia=1e-5, max_iter=100):
    iteracoes = []
    f_a = funcao(a)
    f_b = funcao(b)

    if f_a * f_b >= 0:
        print("Erro: A função não muda de sinal no intervalo [a, b].")
        return None, iteracoes

    p = a
    for i in range(max_iter):
        p = (a * f_b - b * f_a) / (f_b - f_a)
        f_p = funcao(p)

        iteracoes.append({'n': i + 1, 'a': a, 'b': b, 'p': p, 'f_p': f_p})

        if abs(f_p) < tolerancia:
            return p, iteracoes
        if f_a * f_p < 0:
            b = p
            f_b = f_p
        else:
            a = p
            f_a = f_p
    
    print("Aviso: O método excedeu o número máximo de iterações.")
    return p, iteracoes

def calcular_newton(funcao, derivada, estimativa_inicial, tolerancia=1e-5, max_iter=100):
    iteracoes = []
    xi = estimativa_inicial

    for i in range(max_iter):
        f_xi = funcao(xi)
        df_xi = derivada(xi)
        iteracoes.append({'n': i + 1, 'xi': xi, 'f_xi': f_xi, 'df_xi': df_xi})

        if abs(df_xi) < 1e-10:
            print("Erro: Derivada muito próxima de zero.")
            return None, iteracoes
        x_novo = xi - (f_xi / df_xi)
        if abs(x_novo - xi) < tolerancia:
            return x_novo, iteracoes
        xi = x_novo

    print("Aviso: O método excedeu o número máximo de iterações.")
    return xi, iteracoes

def calcular_gauss(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    n = len(b)
    iteracoes = []
    Aug = np.c_[A, b]
    iteracoes.append({'passo': 'Matriz Aumentada Inicial', 'matriz': Aug.tolist()})

    for k in range(n - 1):
        max_index = np.argmax(np.abs(Aug[k:, k])) + k
        
        if max_index != k:
            Aug[[k, max_index]] = Aug[[max_index, k]]
            iteracoes.append({'passo': f'Pivotação: Linha {k+1} <-> Linha {max_index+1}', 'matriz': Aug.tolist()})

        if Aug[k, k] == 0:
            print("Erro: Matriz singular, pivô zero encontrado.")
            return None, iteracoes

        for i in range(k + 1, n):
            fator = Aug[i, k] / Aug[k, k]
            Aug[i, k:] = Aug[i, k:] - fator * Aug[k, k:]
        
        iteracoes.append({'passo': f'Eliminação na coluna {k+1}', 'matriz': Aug.tolist()})

    if Aug[n - 1, n - 1] == 0:
        print("Erro: Matriz singular após eliminação.")
        return None, iteracoes

    x = np.zeros(n, dtype=float)
    for i in range(n - 1, -1, -1):
        soma = np.dot(Aug[i, i+1:n], x[i+1:n])
        x[i] = (Aug[i, n] - soma) / Aug[i, i]
    return x.tolist(), iteracoes

def calcular_gauss_jordan(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    n = len(b)
    iteracoes = []

    Aug = np.c_[A, b]
    iteracoes.append({'passo': 'Matriz Aumentada Inicial', 'matriz': Aug.tolist()})

    for k in range(n):
        max_index = np.argmax(np.abs(Aug[k:, k])) + k
        if max_index != k:
            Aug[[k, max_index]] = Aug[[max_index, k]]
            iteracoes.append({'passo': f'Pivotação: Linha {k+1} <-> Linha {max_index+1}', 'matriz': Aug.tolist()})

        pivo = Aug[k, k]
        if pivo == 0:
            print("Erro: Matriz singular.")
            return None, iteracoes

        Aug[k, :] = Aug[k, :] / pivo
        iteracoes.append({'passo': f'Normalização da Linha {k+1} (L{k+1} / {pivo:.4f})', 'matriz': Aug.tolist()})

        for i in range(n):
            if i != k:
                fator = Aug[i, k]
                Aug[i, :] = Aug[i, :] - fator * Aug[k, :]
        
        iteracoes.append({'passo': f'Eliminação na coluna {k+1}', 'matriz': Aug.tolist()})

    solucao = Aug[:, n]

    return solucao.tolist(), iteracoes