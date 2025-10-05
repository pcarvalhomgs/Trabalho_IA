from IA_Blargura import busca_largura
from IA_Bprofundidade import busca_profundidade
from IA_Bgulosa import busca_gulosa
from IA_Aestrela import a_estrela
import numpy as np 

objetivo = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

def exibir_resultados(nome, niveis, ordem, analisados, fronteira, profundidade, caminho, caminho_estados):
    print(f"\n=== {nome} ===")
    print("Estados por nível da árvore:\n")
    for nivel, estados in niveis.items():
        print(f"Nível {nivel}: {len(estados)} estados")
        for e in estados:
            print(np.array(e), "\n")

    print(f"\nOrdem de Exploração {nome}:\n")
    for i, (estado, prof) in enumerate(ordem):
        print(f"Passo {i} (nível {prof}):\n{np.array(estado)}\n")

    print(f'Estados analisados: {analisados}\nEstados na fronteira: {len(fronteira)}\nProfundidade da solução: {profundidade}\n')
    print("Caminho da solução:", " -> ".join(caminho))
    print("\nCaminho de estados até a solução:\n")
    for i, (estado, prof) in enumerate(caminho_estados):
        print(f"Passo {i} (nível {prof}):\n{np.array(estado)}\n")

def exibir_resultados_heuristicas(nome, niveis, ordem, analisados, fronteira, profundidade, caminho, caminho_estados):
    print(f"\n=== {nome} ===")
    print("Estados por nível da árvore:\n")
    for nivel, estados in niveis.items():
        print(f"Nível {nivel}: {len(estados)} estados")
        for estado, h in estados:  # desempacota a tupla (estado, 'h ou f' dependendo do algoritmo)
            print(f"(f ou h)={h}")
            print(np.array(estado), "\n")

    print(f"\nOrdem de Exploração {nome}:\n")
    for i, (estado, prof, heur) in enumerate(ordem):
        print(f"Passo {i} | nível={prof} | (f ou h)={heur}")
        print(np.array(estado), "\n")

    print(f'Estados analisados: {analisados}\nEstados na fronteira: {len(fronteira)}\nProfundidade da solução: {profundidade}\n')
    print("Caminho da solução:", " -> ".join(caminho))
    print("\nCaminho de estados até a solução:\n")
    for i, (estado, prof) in enumerate(caminho_estados):
        print(f"Passo {i} (nível {prof}):\n{np.array(estado)}\n")

def conta_inversoes(estado): 
    lista = [num for linha in estado for num in linha if num != 0]
    inversoes = 0
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] > lista[j]:
                inversoes += 1
    return inversoes

def eh_solucionavel(estado): 
    inversoes = conta_inversoes(estado)
    return inversoes % 2 == 0

def le_estado_inicial():
    while True:
        print("Digite o estado inicial do quebra-cabeça 3x3 (use 0 para o espaço em branco):")
        estado = []
        for i in range(3):
            linha = input(f"Digite a linha {i+1} (3 números separados por espaço): ")
            estado.append([int(x) for x in linha.split()])
        if eh_solucionavel(estado):
            return estado
        else:
            print("Estado inicial é insolucionável.")

def escolher_algoritmo(estado_inicial):
    while True:
        print("\nEscolha um algoritmo para resolver o quebra-cabeça:")
        print("1. Busca em Largura")
        print("2. Busca em Profundidade")
        print("3. Busca Gulosa")
        print("4. Busca A*")
        print("5. Escolher outro estado inicial")
        print("0. Sair")

        opcao = input("Digite o número da opção desejada: ")
    #1##
        if opcao == "1":
            print("\nExecutando Busca em Largura...")
            niveis_BFS, ordem_exploracao, estados_analisados, fila, profundidade, caminho, caminho_estados = busca_largura(estado_inicial, objetivo)
            exibir_resultados('Busca em Largura', niveis_BFS, ordem_exploracao, estados_analisados, fila, profundidade, caminho, caminho_estados)
    #2##
        elif opcao == "2":
            print("\nExecutando Busca em Profundidade...")
            niveis_DFS, ordem_exploracao, estados_analisados, pilha, profundidade, caminho, caminho_estados = busca_profundidade(estado_inicial, objetivo)
            exibir_resultados('Busca em Profundidade', niveis_DFS, ordem_exploracao, estados_analisados, pilha, profundidade, caminho, caminho_estados)
            
    #3##
        elif opcao == "3":
            print("\nExecutando Busca Gulosa...")
            niveis_Gula, ordem_exploracao, estados_analisados, fila, profundidade, caminho, caminho_estados = busca_gulosa(estado_inicial, objetivo)
            exibir_resultados_heuristicas('Busca Gulosa', niveis_Gula, ordem_exploracao, estados_analisados, fila, profundidade, caminho, caminho_estados)
    #4##
        elif opcao == "4":
            print("\nExecutando Busca A*...")
            niveis_Star, ordem_exploracao, estados_analisados, fila, profundidade, caminho, caminho_estados = a_estrela(estado_inicial, objetivo)
            exibir_resultados_heuristicas('Busca A*...', niveis_Star, ordem_exploracao, estados_analisados, fila, profundidade, caminho, caminho_estados)
        
        elif opcao == "5":
            estado_inicial = le_estado_inicial()

        elif opcao == "0":
            print("Saindo...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

# Programa principal
estado_inicial = le_estado_inicial()
escolher_algoritmo(estado_inicial)
