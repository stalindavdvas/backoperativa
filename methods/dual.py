import numpy as np


def dual(c, A, b):
    """
    Implementación del método dual.
    """
    num_vars = len(c)
    num_restricciones = len(A)

    # Crear el problema dual
    dual_c = b
    dual_A = np.array(A).T  # Transponer la matriz de coeficientes
    dual_b = c

    # Resolver el problema dual usando el método simplex
    tableau = np.zeros((num_vars + 1, num_restricciones + num_vars + 1))
    tableau[:num_vars, :num_restricciones] = dual_A
    tableau[:num_vars, -1] = dual_b
    tableau[-1, :num_restricciones] = -np.array(dual_c)

    # Agregar variables de holgura
    variable_names = [f"Y{i + 1}" for i in range(num_restricciones)] + [f"S{i + 1}" for i in range(num_vars)] + ["RHS"]
    base_variables = [f"S{i + 1}" for i in range(num_vars)] + ["W"]

    for i in range(num_vars):
        tableau[i, num_restricciones + i] = 1

    iteraciones = []

    while True:
        # Guardar la tabla actual para las iteraciones
        tabla_con_nombres = {
            "base": base_variables.copy(),
            "columnas": variable_names,
            "valores": [[float(val) for val in fila] for fila in tableau.tolist()],  # Convertir a float
        }
        iteraciones.append(tabla_con_nombres)

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
    for i, var in enumerate(variable_names[:-1]):  # Excluimos RHS
        col = tableau[:, i]
        if np.sum(col == 1) == 1 and np.sum(col == 0) == len(col) - 1:
            row = np.where(col == 1)[0][0]
            solucion[var] = float(tableau[row, -1])  # Convertir a float
        else:
            solucion[var] = 0.0  # Variables no básicas

    valor_optimo = float(tableau[-1, -1])  # Convertir a float
    return {
        "dual_funcion_objetivo": [float(val) for val in dual_c],  # Convertir a float
        "dual_restricciones": [{"coeficientes": [float(val) for val in row], "valor": float(val)}
                               for row, val in zip(dual_A, dual_b)],  # Convertir a float
        "solucion": {var: float(val) for var, val in solucion.items()},  # Convertir a float
        "valor_optimo": valor_optimo,
        "iteraciones": iteraciones,
    }