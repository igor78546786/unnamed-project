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