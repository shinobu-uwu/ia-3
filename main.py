# Alunos: Matheus Filipe dos Santos Reinert, Matheus Soares Cardoso, João Henrique Galeazzi

import math
import random
import numpy as np
import matplotlib.pyplot as plt


def criar_populacao():
    for i in range(0, len(populacao)):

        for j in range(0, len(populacao)):
            populacao[i][j] = j

        random.shuffle(populacao[i])


def calcular_distancia():
    global distancias

    # copia o array copiando a primeira coluna na última para voltar a origem
    tour = np.insert(populacao, 0, populacao[:, len(populacao) - 1], axis=1)

    d_cidade_tmp = np.zeros(shape=(NUMERO_CIDADES, NUMERO_CIDADES))

    # calcula distancia entre as cidades
    for i in range(NUMERO_CIDADES):
        for j in range(NUMERO_CIDADES):
            d_cidade_tmp[i, j] = np.sqrt((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2)

    for i in range(NUMERO_POPULACAO):
        distancias[i, 0] = 0
        for j in range(NUMERO_CIDADES):
            distancias[i, 0] += d_cidade_tmp[tour[i, j] - 1, tour[i, j + 1] - 1]


# ordena a população e as distâncias da menor para a maior
def ordenar():
    global distancias, populacao

    ordem = distancias[:, -1].argsort()
    distancias = distancias[ordem]
    populacao = populacao[ordem]


# seleciona os 5 pais usando a roleta com maior a chance para o melhor, os 10 primeiros continuam
def selecionar_pais():
    escolhidos = []

    while len(escolhidos) < math.ceil(NUMERO_POPULACAO / 4):
        p1 = random.choice(roleta)
        p2 = random.choice(roleta)

        # evitar que os dois tenham os mesmos pais
        if p1 != p2:
            escolhidos.append((p1, p2))

    return escolhidos


# crossover usando cycle
def crossover_cycle(pais_arr):
    nova_geracao = []

    # realiza crossover em cada par de pais
    for pais in pais_arr:
        # escolhe uma posição aleatória para fazer a primeira troca
        swap_pos = random.choice(range(NUMERO_CIDADES))

        # busca os cromossomos relacionados aos pais atuais e cria uma deep copy
        filho1 = np.copy(populacao[pais[0]])
        filho2 = np.copy(populacao[pais[1]])

        # troca os genes na posição escolhida
        filho1[swap_pos], filho2[swap_pos] = filho2[swap_pos], filho1[swap_pos]
        duplicatas = procurar_posicoes_duplicadas(filho1)

        # se houver genes duplicados, troca o gene na posição diferente da posição inicial
        while len(duplicatas) > 0:

            # não trocar a posição que acabou de trocar para não entrar em loop
            if duplicatas[0] != swap_pos:
                swap_pos = duplicatas[0]
            else:
                swap_pos = duplicatas[1]

            filho1[swap_pos], filho2[swap_pos] = filho2[swap_pos], filho1[swap_pos]

            duplicatas = procurar_posicoes_duplicadas(filho1)

        nova_geracao.append(filho1)
        nova_geracao.append(filho2)

    return nova_geracao


def procurar_posicoes_duplicadas(arr):
    unique, counts = np.unique(arr, return_counts=True)
    duplicates = unique[counts > 1]
    indexes = []

    for duplicate in duplicates:
        indexes.extend(np.where(np.array(arr) == duplicate)[0].tolist())

    return indexes


# escolhe dois genes de forma aleatória e os troca
def mutar(individuos):
    for individuo in individuos:
        posicoes = random.sample(range(0, NUMERO_CIDADES), 2)

        individuo[posicoes[0]], individuo[posicoes[1]] = individuo[posicoes[1]], individuo[posicoes[0]]


def organiza_nova_geracao(nova_geracao):
    global populacao

    # sobrescreve a segunda metade da população
    for i in range(len(nova_geracao)):
        populacao[i + math.ceil(NUMERO_POPULACAO / 2)] = nova_geracao[i]


def mostra_resultado():
    print('Tamanho da população:', NUMERO_POPULACAO)
    print('População inicial:', populacao_inicial, '\n')
    print('População final:', populacao, '\n')
    print('Número de cidades:', NUMERO_CIDADES, '\n')
    print('Melhor custo:', distancias[0], '\n')
    print('Melhor solução:', populacao[0], ' \n')

    caminho_horizontal = np.zeros([20, 1], dtype=np.float64)
    caminho_vertical = np.zeros([20, 1], dtype=np.float64)

    for i in range(NUMERO_CIDADES):
        caminho_horizontal[i] = (x[populacao[0][i]])
        caminho_vertical[i] = (y[populacao[0][i]])

    plt.plot(caminho_horizontal, caminho_vertical, '--', color='red')
    plt.plot(caminho_horizontal, caminho_vertical, 'o', color='blue')
    plt.title("Trabalho 3: Algoritmos Genéticos - Caixeiro Viajante")
    plt.show()


data = np.loadtxt('cidades.mat')

NUMERO_POPULACAO = 20
NUMERO_CIDADES = len(data[0])
NUMERO_ITERACOES = 10_000

# coordenadas
x = data[0]
y = data[1]

populacao = np.zeros(shape=(NUMERO_POPULACAO, NUMERO_CIDADES), dtype=int)
distancias = np.zeros(shape=(NUMERO_POPULACAO, 1))

roleta = [i for i in range(9, -1, -1) for _ in range(i + 1)]

criar_populacao()
populacao_inicial = populacao

for i in range(NUMERO_ITERACOES):
    calcular_distancia()
    ordenar()
    pais_escolhidos = selecionar_pais()
    nova_geracao = crossover_cycle(pais_escolhidos)
    mutar(nova_geracao)
    organiza_nova_geracao(nova_geracao)

calcular_distancia()
ordenar()
mostra_resultado()
