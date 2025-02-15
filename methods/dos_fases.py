import numpy as np


def dos_fases(tipo_optimizacion, c, A, signos, b):
    """
    Implementación del método de las dos fases.
    """
    num_vars = len(c)
    num_restricciones = len(A)

    # Crear la tabla inicial
    tableau = np.zeros((num_restricciones + 1, num_vars + num_restricciones * 2 + 1))
    tableau[:num_restricciones, :num_vars] = A
    tableau[:num_restricciones, -1] = b

    # Agregar variables de holgura, exceso y artificiales
    variable_names = [f"X{i + 1}" for i in range(num_vars)]
    holgura_index = num_vars
    artificial_index = num_vars + num_restricciones

    for i, signo in enumerate(signos):
        if signo == "<=":
            tableau[i, holgura_index] = 1
            variable_names.append(f"S{i + 1}")
            holgura_index += 1
        elif signo == ">=":
            tableau[i, holgura_index] = -1
            tableau[i, artificial_index] = 1
            variable_names.append(f"E{i + 1}")
            variable_names.append(f"A{i + 1}")
            holgura_index += 1
            artificial_index += 1
        elif signo == "=":
            tableau[i, artificial_index] = 1
            variable_names.append(f"A{i + 1}")
            artificial_index += 1

    # Fase 1: Minimizar la suma de variables artificiales
    objective_fase1 = np.zeros(len(variable_names))
    for i, var in enumerate(variable_names):
        if var.startswith("A"):
            objective_fase1[i] = 1

    tableau[-1, :-1] = objective_fase1
    base_variables = [var for var in variable_names if var.startswith("S") or var.startswith("A")]
    base_variables.append("Z")

    iteraciones_fase1 = []

    while True:
        # Guardar la tabla actual para las iteraciones
        tabla_con_nombres = {
            "base": base_variables.copy(),
            "columnas": variable_names + ["RHS"],
            "valores": tableau.tolist(),
        }
        iteraciones_fase1.append(tabla_con_nombres)

        # Condición de optimalidad
        if all(val >= 0 for val in tableau[-1, :-1]):
            break

        # Elegir columna pivote (variable entrante)
        pivot_col = np.argmin(tableau[-1, :-1])
        variable_entrante = variable_names[pivot_col]

        # Elegir fila pivote (variable saliente)
        ratios = tableau[:-1, -1] / tableau[:-1, pivot_col]
        ratios[tableau[:-1, pivot_col] <= 0] = np.inf
        pivot_row = np.argmin(ratios)
        variable_saliente = base_variables[pivot_row]

        # Actualizar variables básicas
        base_variables[pivot_row] = variable_entrante

        # Pivoteo
        pivot_value = tableau[pivot_row, pivot_col]
        tableau[pivot_row, :] /= pivot_value
        for i in range(tableau.shape[0]):
            if i != pivot_row:
                tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]

    # Verificar si hay solución factible
    if tableau[-1, -1] > 0:
        return {"error": "No hay solución factible."}

    # Eliminar variables artificiales
    tableau = np.delete(tableau, [i for i, var in enumerate(variable_names) if var.startswith("A")], axis=1)
    variable_names = [var for var in variable_names if not var.startswith("A")]

    # Fase 2: Resolver el problema original
    tableau[-1, :-1] = -np.array(c) if tipo_optimizacion == "max" else np.array(c)
    iteraciones_fase2 = []

    while True:
        # Guardar la tabla actual para las iteraciones
        tabla_con_nombres = {
            "base": base_variables.copy(),
            "columnas": variable_names + ["RHS"],
            "valores": tableau.tolist(),
        }
        iteraciones_fase2.append(tabla_con_nombres)

        # Condición de optimalidad
        if all(val >= 0 for val in tableau[-1, :-1]):
            break

        # Elegir columna pivote (variable entrante)
        pivot_col = np.argmin(tableau[-1, :-1])
        variable_entrante = variable_names[pivot_col]

        # Elegir fila pivote (variable saliente)
        ratios = tableau[:-1, -1] / tableau[:-1, pivot_col]
        ratios[tableau[:-1, pivot_col] <= 0] = np.inf
        pivot_row = np.argmin(ratios)
        variable_saliente = base_variables[pivot_row]

        # Actualizar variables básicas
        base_variables[pivot_row] = variable_entrante

        # Pivoteo
        pivot_value = tableau[pivot_row, pivot_col]
        tableau[pivot_row, :] /= pivot_value
        for i in range(tableau.shape[0]):
            if i != pivot_row:
                tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]

    # Extraer solución óptima
    solucion = {}
    for i, var in enumerate(variable_names):
        col = tableau[:, i]
        if np.sum(col == 1) == 1 and np.sum(col == 0) == len(col) - 1:
            row = np.where(col == 1)[0][0]
            solucion[var] = tableau[row, -1]
        else:
            solucion[var] = 0  # Variables no básicas

    valor_optimo = tableau[-1, -1]
    return {
        "solucion": solucion,
        "valor_optimo": valor_optimo,
        "iteraciones_fase1": iteraciones_fase1,
        "iteraciones_fase2": iteraciones_fase2,
    }