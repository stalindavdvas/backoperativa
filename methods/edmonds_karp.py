from collections import deque, defaultdict  # Importar defaultdict

def bfs(grafo_residual, fuente, sumidero, padres):
    """
    Realiza una búsqueda en anchura (BFS) para encontrar un camino aumentante.
    """
    visitados = set()
    cola = deque([fuente])
    visitados.add(fuente)
    padres[fuente] = None

    while cola:
        nodo_actual = cola.popleft()

        for vecino, capacidad_residual in grafo_residual[nodo_actual].items():
            if vecino not in visitados and capacidad_residual > 0:
                cola.append(vecino)
                visitados.add(vecino)
                padres[vecino] = nodo_actual

                if vecino == sumidero:
                    return True

    return False


def edmonds_karp(grafo, fuente, sumidero):
    """
    Calcula el flujo máximo usando el algoritmo de Edmonds-Karp.
    """
    # Crear el grafo residual
    grafo_residual = defaultdict(lambda: defaultdict(int))  # Usar defaultdict
    for u in grafo:
        for v, capacidad in grafo[u].items():
            grafo_residual[u][v] = capacidad

    padres = {}
    flujo_maximo = 0
    aristas_utilizadas = []

    while bfs(grafo_residual, fuente, sumidero, padres):
        # Encontrar el flujo mínimo en el camino aumentante
        flujo_camino = float("inf")
        s = sumidero
        while s != fuente:
            flujo_camino = min(flujo_camino, grafo_residual[padres[s]][s])
            s = padres[s]

        # Actualizar el flujo máximo
        flujo_maximo += flujo_camino

        # Actualizar el grafo residual
        v = sumidero
        while v != fuente:
            u = padres[v]
            grafo_residual[u][v] -= flujo_camino
            grafo_residual[v][u] += flujo_camino

            # Registrar las aristas utilizadas
            aristas_utilizadas.append({
                "from": u,
                "to": v,
                "capacidad": grafo[u][v],
                "flujo": flujo_camino,
            })

            v = padres[v]

    return flujo_maximo, aristas_utilizadas