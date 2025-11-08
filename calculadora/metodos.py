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