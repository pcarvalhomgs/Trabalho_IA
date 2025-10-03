from collections import defaultdict

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

def busca_profundidade(estado_inicial, objetivo):
    pilha = [(estado_inicial, 0, [], [(estado_inicial, 0)])] # estado_inicial, profundidade, caminho_gerado, caminho_estados
    visitado = set()
    estados_analisados = 0
    ordem_exploracao = [] # guarda a ordem de busca da DFS

    niveis = defaultdict(list)  # Armazena os estados por nível
    niveis[0].append(estado_inicial)

    while pilha:
        estado_atual, profundidade, caminho, caminho_estados = pilha.pop()
        estados_analisados += 1
        ordem_exploracao.append((estado_atual, profundidade))

        if verifica(estado_atual, objetivo):
            return niveis, ordem_exploracao, estados_analisados, pilha, profundidade, caminho, caminho_estados
        
        visitado.add(tuple(map(tuple, estado_atual)))
        for possibilidade, movimento in descobre_possibilidades(estado_atual):
            if tuple(map(tuple, possibilidade)) not in visitado:
                pilha.append((possibilidade, profundidade + 1, caminho + [movimento], caminho_estados + [(possibilidade, profundidade + 1)]))
                niveis[profundidade + 1].append(possibilidade)

    return None # Não encontrou solução
