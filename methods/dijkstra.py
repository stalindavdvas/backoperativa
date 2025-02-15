import heapq

def dijkstra(nodos, aristas, inicio, fin):
    """
    Calcula el camino más corto usando el algoritmo de Dijkstra.
    """
    # Construir el grafo
    grafo = {nodo: {} for nodo in nodos}
    for arista in aristas:
        grafo[arista["from"]][arista["to"]] = arista["peso"]
        grafo[arista["to"]][arista["from"]] = arista["peso"]  # Grafo no dirigido

    # Inicializar distancias y predecesores
    distancias = {nodo: float("inf") for nodo in nodos}
    distancias[inicio] = 0
    predecesores = {nodo: None for nodo in nodos}

    # Cola de prioridad
    cola = [(0, inicio)]

    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)

        # Si ya visitamos este nodo con una distancia menor, ignorarlo
        if distancia_actual > distancias[nodo_actual]:
            continue

        # Explorar vecinos
        for vecino, peso in grafo[nodo_actual].items():
            nueva_distancia = distancia_actual + peso
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                predecesores[vecino] = nodo_actual
                heapq.heappush(cola, (nueva_distancia, vecino))

    # Reconstruir el camino
    camino = []
    nodo_actual = fin
    while nodo_actual:
        camino.append(nodo_actual)
        nodo_actual = predecesores[nodo_actual]
    camino.reverse()

    return {"camino": camino, "costo_total": distancias[fin]}