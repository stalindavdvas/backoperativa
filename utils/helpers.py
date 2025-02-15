def validar_datos(datos):
    """
    Valida que los datos de entrada sean correctos.
    Parámetros:
    - datos: Diccionario con la función objetivo y las restricciones.
    Retorna:
    - True si los datos son válidos, False en caso contrario.
    """
    if "funcion_objetivo" not in datos or "restricciones" not in datos:
        return False

    # Validar que la función objetivo sea una lista no vacía
    if not isinstance(datos["funcion_objetivo"], list) or len(datos["funcion_objetivo"]) == 0:
        return False

    # Validar que las restricciones sean una lista no vacía
    if not isinstance(datos["restricciones"], list) or len(datos["restricciones"]) == 0:
        return False

    # Validar cada restricción
    for restriccion in datos["restricciones"]:
        if "coeficientes" not in restriccion or "signo" not in restriccion or "valor" not in restriccion:
            return False
        if not isinstance(restriccion["coeficientes"], list) or len(restriccion["coeficientes"]) == 0:
            return False
        if restriccion["signo"] not in ["<=", ">=", "="]:
            return False
        if not isinstance(restriccion["valor"], (int, float)):
            return False

    return True


def extraer_variables_artificiales(solucion, num_variables, num_restricciones):
    """
    Extrae las variables artificiales de la solución.
    Parámetros:
    - solucion: Diccionario con la solución devuelta por el método simplex.
    - num_variables: Número de variables originales.
    - num_restricciones: Número de restricciones.
    Retorna:
    - Diccionario con las variables artificiales.
    """
    variables_artificiales = {}
    for i in range(num_restricciones):
        nombre_variable = f"x{num_variables + i + 1}"  # Variables artificiales comienzan después de las originales
        valor = solucion.get(nombre_variable, 0)
        variables_artificiales[nombre_variable] = valor
    return variables_artificiales


def verificar_solucion_factible(solucion, num_variables, num_restricciones, tolerancia=1e-8):
    """
    Verifica si hay una solución factible basada en las variables artificiales.
    Parámetros:
    - solucion: Diccionario con la solución devuelta por el método simplex.
    - num_variables: Número de variables originales.
    - num_restricciones: Número de restricciones.
    - tolerancia: Tolerancia para considerar valores cercanos a cero.
    Retorna:
    - True si hay solución factible, False en caso contrario.
    """
    variables_artificiales = extraer_variables_artificiales(solucion, num_variables, num_restricciones)
    return all(valor <= tolerancia for valor in variables_artificiales.values())