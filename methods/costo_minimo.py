def costo_minimo(data):
    """
    Implementación del método del costo mínimo.
    """
    origenes = data["origenes"]
    destinos = data["destinos"]
    matriz_costos = data["matriz_costos"]
    ofertas = data["ofertas"]
    demandas = data["demandas"]

    # Verificar si el problema está balanceado
    total_oferta = sum(ofertas)
    total_demanda = sum(demandas)

    if total_oferta > total_demanda:
        # Agregar un destino ficticio
        destinos.append("Ficticio")
        demandas.append(total_oferta - total_demanda)
        for fila in matriz_costos:
            fila.append(0)  # Costo cero para el destino ficticio
    elif total_demanda > total_oferta:
        # Agregar un origen ficticio
        origenes.append("Ficticio")
        ofertas.append(total_demanda - total_oferta)
        matriz_costos.append([0] * len(destinos))  # Costo cero para el origen ficticio

    # Inicializar variables
    asignaciones = []
    oferta_actual = ofertas[:]
    demanda_actual = demandas[:]

    while True:
        # Encontrar la celda con el costo mínimo
        min_cost = float("inf")
        min_i, min_j = -1, -1

        for i in range(len(origenes)):
            for j in range(len(destinos)):
                if oferta_actual[i] > 0 and demanda_actual[j] > 0 and matriz_costos[i][j] < min_cost:
                    min_cost = matriz_costos[i][j]
                    min_i, min_j = i, j

        if min_i == -1 or min_j == -1:
            break  # No hay más celdas válidas

        # Asignar la cantidad mínima posible
        cantidad = min(oferta_actual[min_i], demanda_actual[min_j])
        asignaciones.append({
            "origen": origenes[min_i],
            "destino": destinos[min_j],
            "cantidad": cantidad,
        })

        oferta_actual[min_i] -= cantidad
        demanda_actual[min_j] -= cantidad

        # Si la oferta o la demanda se agotan, ya no se consideran
        if oferta_actual[min_i] == 0:
            oferta_actual[min_i] = 0
        if demanda_actual[min_j] == 0:
            demanda_actual[min_j] = 0

    # Calcular el costo total
    costo_total = sum(
        asignacion["cantidad"] * matriz_costos[origenes.index(asignacion["origen"])][destinos.index(asignacion["destino"])]
        for asignacion in asignaciones
    )

    return {
        "asignaciones": asignaciones,
        "costo_total": costo_total,
    }