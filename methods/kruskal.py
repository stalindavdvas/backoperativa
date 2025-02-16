class UnionFind:
    """
    Estructura de datos Union-Find para manejar conjuntos disjuntos.
    """
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])  # Path compression
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u == root_v:
            return False

        # Union by rank
        if self.rank[root_u] > self.rank[root_v]:
            self.parent[root_v] = root_u
        elif self.rank[root_u] < self.rank[root_v]:
            self.parent[root_u] = root_v
        else:
            self.parent[root_v] = root_u
            self.rank[root_u] += 1

        return True


def kruskal(nodos, aristas):
    """
    Calcula el Árbol de Expansión Mínima usando el algoritmo de Kruskal.
    """
    # Mapear nodos a índices numéricos
    nodo_a_indice = {nodo: i for i, nodo in enumerate(nodos)}

    # Ordenar las aristas por peso
    aristas_ordenadas = sorted(aristas, key=lambda arista: arista["peso"])

    # Inicializar Union-Find
    uf = UnionFind(len(nodos))

    costo_total = 0
    aristas_mst = []

    for arista in aristas_ordenadas:
        u = nodo_a_indice[arista["from"]]
        v = nodo_a_indice[arista["to"]]
        peso = arista["peso"]

        if uf.union(u, v):
            costo_total += peso
            aristas_mst.append({
                "from": arista["from"],
                "to": arista["to"],
                "peso": peso,
            })

    return costo_total, aristas_mst