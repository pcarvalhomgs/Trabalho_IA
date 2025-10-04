from IA_Blargura import busca_largura
from IA_Bprofundidade import busca_profundidade
from IA_Bgulosa import busca_gulosa
from IA_Aestrela import a_estrela
import numpy as np 

objetivo = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

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
    print("Digite o estado inicial do quebra-cabeça 3x3 (use 0 para o espaço em branco):")
    estado = []
    for i in range(3):
        linha = input(f"Digite a linha {i+1} (3 números separados por espaço): ")
        estado.append([int(x) for x in linha.split()])
    return estado

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
            if eh_solucionavel(estado_inicial):
                niveis_BFS, ordem_exploracao, estados_analisados, fila, profundidade, caminho, caminho_estados = busca_largura(estado_inicial, objetivo)

                print("Estados por nível da árvore:\n")
                for nivel, estados in niveis_BFS.items():
                    print(f"Nível {nivel}: {len(estados)} estados")
                    for e in estados:
                        print(np.array(e), "\n")

                print("\nOrdem de Exploração BFS:\n")
                for i, (estado, prof) in enumerate(ordem_exploracao):
                    print(f"Passo {i} (nível {prof}):\n{np.array(estado)}\n")

                print(f'Estados analisados: {estados_analisados}\nEstados na fronteira: {len(fila)}\nProfundidade da solução: {profundidade}\n')
                print("Caminho da solução:", " -> ".join(caminho))
                print("\nCaminho de estados até a solução:\n")
                for i, (estado, prof) in enumerate(caminho_estados):
                    print(f"Passo {i} (nível {prof}):\n{np.array(estado)}\n")
            else:
                print("Estado inicial é insolucionável.")
    #2##
        elif opcao == "2":
            print("\nExecutando Busca em Profundidade...")
            if eh_solucionavel(estado_inicial):
                niveis_DFS, ordem_exploracao, estados_analisados, pilha, profundidade, caminho, caminho_estados = busca_profundidade(estado_inicial, objetivo)

                print("Estados por nível da árvore:\n")
                for nivel, estados in niveis_DFS.items():
                    print(f"Nível {nivel}: {len(estados)} estados")
                    for e in estados:
                        print(np.array(e), "\n")
                
                print("\nOrdem de Exploração DFS:\n")
                for i, (estado, prof) in enumerate(ordem_exploracao):
                    print(f"Passo {i} (nível {prof}):\n{np.array(estado)}\n")

                print(f'Estados analisados: {estados_analisados}\nEstados na fronteira: {len(pilha)}\nProfundidade da solução: {profundidade}\n')
                print("Caminho da solução:", " -> ".join(caminho))
                print("\nCaminho de estados até a solução:\n")
                for i, (estado, prof) in enumerate(caminho_estados):
                    print(f"Passo {i} (nível {prof}):\n{np.array(estado)}\n")

            else:
                print("Estado inicial é insolucionável.")
    #3##
        elif opcao == "3":
            print("\nExecutando Busca Gulosa...")
            if eh_solucionavel(estado_inicial):
                niveis_Gula, ordem_exploracao, estados_analisados, fila, profundidade, caminho, caminho_estados = busca_gulosa(estado_inicial, objetivo)
                
                print("Estados por nível da árvore:\n")
                for nivel, estados in niveis_Gula.items():
                    print(f"Nível {nivel}: {len(estados)} estados")
                    for estado, h in estados:  # desempacota a tupla (estado, heuristica)
                        print(f"Heurística: {h}")
                        print(np.array(estado), "\n")

                print("\nOrdem de Exploração Busca Gulosa:\n")
                for i, (estado, prof, heur) in enumerate(ordem_exploracao):
                    print(f"Passo {i} (nível {prof}) (heurística: {heur}):\n{np.array(estado)}\n")

                print(f'Estados analisados: {estados_analisados}\nEstados na fronteira: {len(fila)}\nProfundidade da solução: {profundidade}\n')
                print("Caminho da solução:", " -> ".join(caminho))
                print("\nCaminho de estados até a solução:\n")
                for i, (estado, prof) in enumerate(caminho_estados):
                    print(f"Passo {i} (nível {prof}):\n{np.array(estado)}\n")
            else:
                print("Estado inicial é insolucionável.")
    #4##
        elif opcao == "4":
            print("\nExecutando Busca A*...")
            if eh_solucionavel(estado_inicial):
                niveis_Star, ordem_exploracao, estados_analisados, fila, profundidade, caminho, caminho_estados = a_estrela(estado_inicial, objetivo)
                
                print("Estados por nível da árvore:\n")
                for nivel, estados in niveis_Star.items():
                    print(f"Nível {nivel}: {len(estados)} estados")
                    for estado, h in estados:  # desempacota a tupla (estado, heuristica)
                        print(f"Heurística: {h}")
                        print(np.array(estado), "\n")

                print("\nOrdem de Exploração A*...:\n")
                for i, (estado, prof, f) in enumerate(ordem_exploracao):
                    print(f"Passo {i} (nível {prof}) (f=(g+h): {f}):\n{np.array(estado)}\n")

                print(f'Estados analisados: {estados_analisados}\nEstados na fronteira: {len(fila)}\nProfundidade da solução: {profundidade}\n')
                print("Caminho da solução:", " -> ".join(caminho))
                print("\nCaminho de estados até a solução:\n")
                for i, (estado, prof) in enumerate(caminho_estados):
                    print(f"Passo {i} (nível {prof}):\n{np.array(estado)}\n")
            else:
                print("Estado inicial é insolucionável.")

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
