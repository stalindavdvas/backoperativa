def validate_graph_data(nodos, aristas, inicio, fin):
    """
    Valida que los datos del grafo sean completos y consistentes.
    """
    errors = []

    # Validar nodos
    if not nodos or not isinstance(nodos, list) or len(nodos) == 0:
        errors.append("La lista de nodos está vacía o no es válida.")

    # Validar aristas
    if not aristas or not isinstance(aristas, list) or len(aristas) == 0:
        errors.append("La lista de aristas está vacía o no es válida.")
    else:
        for i, arista in enumerate(aristas):
            if (
                "from" not in arista
                or "to" not in arista
                or "peso" not in arista
                or arista["from"] not in nodos
                or arista["to"] not in nodos
                or not isinstance(arista["peso"], (int, float))
            ):
                errors.append(f"Arista {i + 1} es inválida: {arista}")

    # Validar inicio y fin
    if not inicio or not fin or inicio not in nodos or fin not in nodos:
        errors.append("Los nodos de inicio o destino son inválidos o no existen en la red.")

    if errors:
        raise ValueError("\n".join(errors))

    return True