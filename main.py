from grafos import Grafo

if __name__ == '__main__':

    g = Grafo(5, False)

    # g.printMatriz()

    g.addAresta(0, 1, 50)
    g.addAresta(0, 3, 40)
    g.addAresta(0, 4, 40)
    g.addAresta(1, 2, 10)
    g.addAresta(2, 3, 10)
    g.addAresta(3, 4, 20)

    g.printMatriz()

    # obj, exploracao = g.bcu(0,4)
    obj1, exploracao = g.bcu(0,2)
    obj2 = g.bgme(0,2)
    obj3 = g.aStar(0,2)
    print("obj1.caminho:", obj1.caminho)
    print("obj1.custo:", obj1.custo)
    print("obj2.caminho:", obj2.caminho)
    print("obj3.caminho:", obj3.caminho)
