import numpy as np


def gran_m(tipo_optimizacion, c, A, signos, b):
    """
    Implementación del método de la Gran M.
    """
    num_vars = len(c)
    num_restricciones = len(A)

    # Contar variables adicionales (holgura, exceso, artificiales)
    num_holgura = sum(1 for signo in signos if signo == "<=")
    num_exceso = sum(1 for signo in signos if signo == ">=")
    num_artificiales = sum(1 for signo in signos if signo in [">=", "="])

    total_vars = num_vars + num_holgura + num_exceso + num_artificiales

    # Crear la tabla inicial
    tableau = np.zeros((num_restricciones + 1, total_vars + 1), dtype=object)  # Usamos dtype=object para manejar 'M'
    tableau[:num_restricciones, :num_vars] = A
    tableau[:num_restricciones, -1] = b

    # Agregar variables de holgura, exceso y artificiales
    variable_names = [f"X{i + 1}" for i in range(num_vars)]
    holgura_index = num_vars
    exceso_index = num_vars + num_holgura
    artificial_index = num_vars + num_holgura + num_exceso

    for i, signo in enumerate(signos):
        if signo == "<=":
            tableau[i, holgura_index] = 1
            variable_names.append(f"S{i + 1}")
            holgura_index += 1
        elif signo == ">=":
            tableau[i, exceso_index] = -1
            tableau[i, artificial_index] = 1
            variable_names.append(f"E{i + 1}")
            variable_names.append(f"A{i + 1}")
            exceso_index += 1
            artificial_index += 1
        elif signo == "=":
            tableau[i, artificial_index] = 1
            variable_names.append(f"A{i + 1}")
            artificial_index += 1

    # Función objetivo con penalización M
    M = "M"  # Representamos M como un símbolo
    objective = np.zeros(total_vars, dtype=object)
    objective[:num_vars] = -np.array(c) if tipo_optimizacion == "max" else np.array(c)
    for i, var in enumerate(variable_names):
        if var.startswith("A"):
            objective[i] = -M if tipo_optimizacion == "max" else M

    tableau[-1, :-1] = objective
    base_variables = [var for var in variable_names if var.startswith("S") or var.startswith("A")]
    base_variables.append("Z")

    iteraciones = []

    while True:
        # Guardar la tabla actual para las iteraciones
        tabla_con_nombres = {
            "base": base_variables.copy(),
            "columnas": variable_names + ["RHS"],
            "valores": [[val if val != "M" else "M" for val in fila] for fila in tableau.tolist()],
        }
        iteraciones.append(tabla_con_nombres)

        # Condición de optimalidad
        if all(val >= 0 if isinstance(val, (int, float)) else False for val in tableau[-1, :-1]):
            break

        # Elegir columna pivote (variable entrante)
        pivot_col = np.argmin([float("inf") if val == "M" else val for val in tableau[-1, :-1]])
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
        "iteraciones": iteraciones,
    }