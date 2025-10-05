from collections import defaultdict
import heapq as prioridade

# movimentos possíveis
movimentos = {
    (-1, 0): "Cima",
    (1, 0): "Baixo",
    (0, -1): "Esquerda",
    (0, 1): "Direita"
}

def encontra_zero(estado):
    for i in range(len(estado)):
        for j in range(len(estado[i])):
            if estado[i][j] == 0:
                return (i, j)
    return None

def verifica(estado_atual, objetivo):
    return estado_atual == objetivo

def descobre_possibilidades(estado):
    zero_i, zero_j = encontra_zero(estado)
    possibilidades = []
    for (di, dj), nome in movimentos.items():
        novo_i, novo_j = zero_i + di, zero_j + dj
        if 0 <= novo_i < 3 and 0 <= novo_j < 3: # se esta dentro do tabuleiro
            novo_estado = [linha[:] for linha in estado]  # Cria uma cópia do estado
            novo_estado[zero_i][zero_j], novo_estado[novo_i][novo_j] = (novo_estado[novo_i][novo_j], novo_estado[zero_i][zero_j]) 
            possibilidades.append((novo_estado, nome))
    
    return possibilidades

def distancia_manhattan(estado):
    distancia = 0
    for i in range(3):
        for j in range(3):
            if estado[i][j] != 0:  # Não conta o zero
                objetivo_x = (estado[i][j] - 1) // 3
                objetivo_y = (estado[i][j] - 1) % 3
                distancia += abs(i - objetivo_x) + abs(j - objetivo_y)
    return distancia

def a_estrela(estado_inicial, objetivo):
    fila_prioridade = []
    # (f(g+h), g(profundidade_custo do caminho), estado, caminho_gerado, caminho_estados)
    prioridade.heappush(fila_prioridade, (0, 0, estado_inicial, [], [(estado_inicial, 0)])) 
    visitados = set()
    visitados.add(tuple(map(tuple, estado_inicial)))
    estados_analisados = 0
    ordem_exploracao = [] # guarda a ordem de busca da BuscaGulosa

    niveis = defaultdict(list)  # Armazena os estados por nível
    niveis[0].append((estado_inicial, 0))

    while fila_prioridade:
        f, g, estado_atual, caminho, caminho_estados = prioridade.heappop(fila_prioridade) 
        estados_analisados += 1
        ordem_exploracao.append((estado_atual, g, f))

        if verifica(estado_atual, objetivo):
            return niveis, ordem_exploracao, estados_analisados, fila_prioridade, g, caminho, caminho_estados

        for possibilidade, movimento in descobre_possibilidades(estado_atual):
            if tuple(map(tuple, possibilidade)) not in visitados:
                visitados.add(tuple(map(tuple, possibilidade)))

                g_novo = g + 1
                h_novo = distancia_manhattan(possibilidade)
                f_novo = g_novo + h_novo
                prioridade.heappush(fila_prioridade, (f_novo, g_novo, possibilidade, caminho + [movimento], caminho_estados + [(possibilidade, g_novo)]))
                niveis[g_novo].append((possibilidade, f_novo)) # guarda estado e (f=g+h)

    return None
