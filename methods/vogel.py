def calcular_penalizaciones(matriz_costos):
    """
    Calcula las penalizaciones para cada fila y columna.
    """
    num_filas = len(matriz_costos)
    num_columnas = len(matriz_costos[0])

    penalizaciones_fila = []
    for fila in matriz_costos:
        # Filtrar valores finitos (ignorar infinitos)
        valores_validos = [costo for costo in fila if costo != float("inf")]
        if len(valores_validos) >= 2:
            sorted_fila = sorted(valores_validos)
            penalizacion = sorted_fila[1] - sorted_fila[0]
        elif len(valores_validos) == 1:
            penalizacion = valores_validos[0]
        else:
            penalizacion = 0  # Si no hay valores válidos, la penalización es 0
        penalizaciones_fila.append(penalizacion)

    penalizaciones_columna = []
    for j in range(num_columnas):
        # Filtrar valores finitos (ignorar infinitos)
        columna = [matriz_costos[i][j] for i in range(num_filas) if matriz_costos[i][j] != float("inf")]
        if len(columna) >= 2:
            sorted_columna = sorted(columna)
            penalizacion = sorted_columna[1] - sorted_columna[0]
        elif len(columna) == 1:
            penalizacion = columna[0]
        else:
            penalizacion = 0  # Si no hay valores válidos, la penalización es 0
        penalizaciones_columna.append(penalizacion)

    return penalizaciones_fila, penalizaciones_columna


def vogel(data):
    """
    Implementación del método de Vogel.
    """
    origenes = data["origenes"]
    destinos = data["destinos"]
    matriz_costos_original = data["matriz_costos"]  # Guardar la matriz original
    ofertas = data["ofertas"]
    demandas = data["demandas"]

    # Verificar si el problema está balanceado
    total_oferta = sum(ofertas)
    total_demanda = sum(demandas)

    if total_oferta > total_demanda:
        # Agregar un destino ficticio
        destinos.append("Ficticio")
        demandas.append(total_oferta - total_demanda)
        for fila in matriz_costos_original:
            fila.append(0)  # Costo cero para el destino ficticio
    elif total_demanda > total_oferta:
        # Agregar un origen ficticio
        origenes.append("Ficticio")
        ofertas.append(total_demanda - total_oferta)
        matriz_costos_original.append([0] * len(destinos))  # Costo cero para el origen ficticio

    # Copiar la matriz de costos para modificarla durante el algoritmo
    matriz_costos = [fila[:] for fila in matriz_costos_original]

    # Inicializar variables
    asignaciones = []
    oferta_actual = ofertas[:]
    demanda_actual = demandas[:]
    iteraciones = []

    while True:
        # Guardar la tabla actual para las iteraciones
        tabla_actual = {
            "matriz_costos": [fila[:] for fila in matriz_costos],
            "ofertas": oferta_actual[:],
            "demandas": demanda_actual[:],
        }

        # Calcular penalizaciones
        penalizaciones_fila, penalizaciones_columna = calcular_penalizaciones(matriz_costos)
        tabla_actual["penalizaciones_fila"] = penalizaciones_fila
        tabla_actual["penalizaciones_columna"] = penalizaciones_columna
        iteraciones.append(tabla_actual)

        # Encontrar la fila o columna con la mayor penalización
        max_penalizacion = -1
        seleccion = None  # (tipo, índice, costo_mínimo, fila/col)
        for i, penalizacion in enumerate(penalizaciones_fila):
            if oferta_actual[i] > 0 and penalizacion > max_penalizacion:
                # Filtrar valores finitos (ignorar infinitos)
                min_costo = min((costo, j) for j, costo in enumerate(matriz_costos[i]) if
                                demanda_actual[j] > 0 and costo != float("inf"))
                max_penalizacion = penalizacion
                seleccion = ("fila", i, min_costo[0], min_costo[1])

        for j, penalizacion in enumerate(penalizaciones_columna):
            if demanda_actual[j] > 0 and penalizacion > max_penalizacion:
                # Filtrar valores finitos (ignorar infinitos)
                min_costo = min((matriz_costos[i][j], i) for i in range(len(origenes)) if
                                oferta_actual[i] > 0 and matriz_costos[i][j] != float("inf"))
                max_penalizacion = penalizacion
                seleccion = ("columna", j, min_costo[0], min_costo[1])

        if not seleccion:
            break  # No hay más celdas válidas

        tipo, indice, costo_minimo, otro_indice = seleccion

        if tipo == "fila":
            i, j = indice, otro_indice
        else:
            j, i = indice, otro_indice

        # Asignar la cantidad mínima posible
        cantidad = min(oferta_actual[i], demanda_actual[j])
        asignaciones.append({
            "origen": origenes[i],
            "destino": destinos[j],
            "cantidad": cantidad,
        })

        oferta_actual[i] -= cantidad
        demanda_actual[j] -= cantidad

        # Si la oferta o la demanda se agotan, ya no se consideran
        if oferta_actual[i] == 0:
            for k in range(len(destinos)):
                matriz_costos[i][k] = 0  # Reemplazar infinito por 0
        if demanda_actual[j] == 0:
            for k in range(len(origenes)):
                matriz_costos[k][j] = 0  # Reemplazar infinito por 0

        # Si todas las ofertas y demandas están satisfechas, terminar
        if all(o == 0 for o in oferta_actual) and all(d == 0 for d in demanda_actual):
            break

    # Calcular el costo total usando la matriz de costos original
    costo_total = sum(
        asignacion["cantidad"] * matriz_costos_original[origenes.index(asignacion["origen"])][
            destinos.index(asignacion["destino"])]
        for asignacion in asignaciones
    )

    # Reemplazar valores infinitos por 0 en las iteraciones
    for iteracion in iteraciones:
        iteracion["matriz_costos"] = [
            [0 if costo == float("inf") else costo for costo in fila]
            for fila in iteracion["matriz_costos"]
        ]
        iteracion["penalizaciones_fila"] = [
            0 if penalizacion == float("inf") else penalizacion
            for penalizacion in iteracion["penalizaciones_fila"]
        ]
        iteracion["penalizaciones_columna"] = [
            0 if penalizacion == float("inf") else penalizacion
            for penalizacion in iteracion["penalizaciones_columna"]
        ]

    return {
        "asignaciones": asignaciones,
        "costo_total": float(costo_total),  # Asegurarse de que sea un número flotante
        "iteraciones": iteraciones,
    }