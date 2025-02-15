import numpy as np
def simplex(c, A, b):
    """
    Implementación básica del método simplex con nombres de variables.
    """
    num_vars = len(c)
    num_restricciones = len(A)

    # Crear la tabla inicial
    tableau = np.zeros((num_restricciones + 1, num_vars + num_restricciones + 1))
    tableau[:num_restricciones, :num_vars] = A
    tableau[:num_restricciones, -1] = b
    tableau[-1, :num_vars] = -np.array(c)

    # Agregar variables de holgura
    for i in range(num_restricciones):
        tableau[i, num_vars + i] = 1

    # Nombres de las variables
    variable_names = [f"X{i + 1}" for i in range(num_vars)] + [f"S{i + 1}" for i in range(num_restricciones)] + ["RHS"]
    base_variables = [f"S{i + 1}" for i in range(num_restricciones)] + ["Z"]

    iteraciones = []

    while True:
        # Guardar la tabla actual para las iteraciones
        tabla_con_nombres = {
            "base": base_variables.copy(),
            "columnas": variable_names,
            "valores": tableau.tolist(),
        }
        iteraciones.append(tabla_con_nombres)

        # Condición de optimalidad
        if all(tableau[-1, :-1] >= 0):
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
    for i, var in enumerate(variable_names[:-1]):  # Excluimos RHS
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
        "iteraciones": iteraciones,
    }