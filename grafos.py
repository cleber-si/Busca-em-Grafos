import queue
import random
random.seed(37)

class Node:
    id = -1
    pai = None
    peso = 0
    custo = 0
    caminho = []

    def __init__(self, id):
        self.id = id
        self.caminho = []

class Grafo:
    matriz = []
    n = 0
    direcionado = False

    def __init__(self, n, direcionado):
        self.n = n
        self.direcionado = direcionado

        for i in range(n):
            self.matriz.append([0]*n)

    def addAresta(self, s, t, p):
        if (not self.direcionado):
            self.matriz[t][s] = p
        self.matriz[s][t] = p

    def traca_caminho(self, exploracao):
        caminho = []

        cont = 1
        vals = []

        for i in range(len(exploracao)):
            try:
                if exploracao[i+1][0] != exploracao[i][0]:
                    vals.append(exploracao[i])
                    if cont > 1:
                        for item in vals:
                            if item[1] == exploracao[i+1][0]:
                                caminho.append(item[1])
                                vals = []
                                cont = 1
                    else:
                        caminho.append(exploracao[i][1])
                        vals = []
                        cont = 1
                else:
                    cont += 1
                    vals.append(exploracao[i])
                    continue
            except:
                caminho.append(exploracao[i][1])
            vals = []

        return caminho

    def heuristica(self, t):
        h = [
            [0  , 188, 87 , 144, 105],
            [118, 0  , 77 , 150, 161],
            [87 , 77 , 0  , 79 , 85 ],
            [144, 150, 79 , 0  , 63 ],
            [105, 161, 85 , 63 , 0  ]
        ]

        return h[t]

    # Busca de custo uniforme
    def bcu(self, s, t):
        q = []

        node = Node(s)
        node.pai = Node(-1)

        q.append(node)

        exploracao = []

        # Faz uma cópia segura da matriz original
        matriz2 = self.matriz.copy()

        while not (len(q) == 0):
            # Seleciona o nó com o menor custo
            custos = [item.custo for item in q]
            menor_custo = min(item for item in custos)
            aux = q.pop(custos.index(menor_custo))

            exploracao.append([aux.pai.id, aux.id])

            # Teste de Objetivo
            if (aux.id == t):
                aux.caminho = self.traca_caminho(exploracao)
                return aux, exploracao
            
            # Expansão BCU
            lista = matriz2[aux.id].copy()
            if aux.pai.id > -1:
                lista[aux.pai.id] = 0
                # Calibra o custo dos nós seguintes
                for i in range(len(lista)): 
                    if lista[i] != 0:
                        lista[i] += aux.custo

            minimo = []
            indice = []

            for i in range(len(lista)):
                try:
                    minimo.append(min(item for item in lista if item != 0))
                except:
                    break
                
                indice.append(lista.index(minimo[i]))

                lista[indice[i]] = 0

            nos = list(zip(minimo, indice))

            for i in nos:
                if i[1] != aux.pai.id:
                    node = Node(i[1])
                    node.custo = i[0]
                    node.pai = aux
                    node.caminho.append(node.id)
                    q.append(node)


    # Busca Gulosa pela Melhor Escolha
    def bgme(self, s, t):
        q = []

        node = Node(s)
        node.pai = Node(-1)

        q.append(node)

        # Faz uma cópia segura da matriz original
        matriz3 = self.matriz.copy()

        #distancias = gera_distancia_reta(matriz, t)
        distancias = self.heuristica(t)
        caminho = []

        while not (len(q) == 0):
            aux = q.pop()
            
            caminho.append(aux.id)

            # Teste de Objetivo
            if (aux.id == t):
                aux.caminho = caminho
                return aux

            # Expansão BGME
            lista = matriz3[aux.id]

            # Informações dos nós adjacentes
            infos = [] # Col 0: índices - Col 1: valores - Col 2: distâncias

            for i in range(len(lista)):
                if lista[i] != 0:
                    infos.append([i, lista[i], distancias[i]])

            # Acha o nó adjacente com a menor distância em linha reta do objetivo
            dists = []
            for i in range(len(infos)):
                dists.append(infos[i][2])
            menor_distancia = min(dists)

            no = infos[dists.index(menor_distancia)]

            node = Node(no[0])
            node.pai = aux
            q.append(node)
    
    # Busca A*
    def aStar(self,s,t):
        q = []

        node = Node(s)
        node.pai = Node(-1)

        q.append(node)

        #distancias = gera_distancia_reta(matriz, t)
        distancias = self.heuristica(t)
        caminho = []

        while not (len(q) == 0):
            aux = q.pop()
            
            caminho.append(aux.id)

            # Teste de Objetivo
            if (aux.id == t):
                aux.caminho = caminho
                return aux

            # Expansão BGME
            lista = self.matriz[aux.id]

            # Informações dos nós adjacentes
            infos = [] # Col 0: índices - Col 1: valores - Col 2: distâncias

            for i in range(len(lista)):
                if lista[i] != 0:
                    infos.append([i, lista[i], distancias[i]+lista[i]])

            # Acha o nó adjacente com a menor distância em linha reta do objetivo
            dists = []
            for i in range(len(infos)):
                dists.append(infos[i][2])
            menor_distancia = min(dists)

            no = infos[dists.index(menor_distancia)]

            node = Node(no[0])
            node.pai = aux
            q.append(node)


    def printMatriz(self):
        print('\n')
        print('#'*10)
        for i in range(self.n):
            for j in range(self.n):
                print(self.matriz[i][j], end=' ')
            print()
        print('#'*10)
        print()
