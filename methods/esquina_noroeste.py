def esquina_noroeste(data):
    """
    Implementación del método de la esquina noroeste.
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
    i, j = 0, 0
    oferta_actual = ofertas[:]
    demanda_actual = demandas[:]

    while i < len(origenes) and j < len(destinos):
        cantidad = min(oferta_actual[i], demanda_actual[j])
        asignaciones.append({
            "origen": origenes[i],
            "destino": destinos[j],
            "cantidad": cantidad,
        })

        oferta_actual[i] -= cantidad
        demanda_actual[j] -= cantidad

        if oferta_actual[i] == 0:
            i += 1
        if demanda_actual[j] == 0:
            j += 1

    # Calcular el costo total
    costo_total = sum(
        asignacion["cantidad"] * matriz_costos[origenes.index(asignacion["origen"])][destinos.index(asignacion["destino"])]
        for asignacion in asignaciones
    )

    return {
        "asignaciones": asignaciones,
        "costo_total": costo_total,
    }