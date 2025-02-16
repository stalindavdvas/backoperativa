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
    tableau = np.zeros((num_restricciones + 1, total_vars + 1), dtype=float)
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
            tableau[i, exceso_index] = -1  # Variable de exceso
            tableau[i, artificial_index] = 1  # Variable artificial
            variable_names.append(f"E{i + 1}")  # Variable de exceso
            variable_names.append(f"A{i + 1}")  # Variable artificial
            exceso_index += 1
            artificial_index += 1
        elif signo == "=":
            tableau[i, artificial_index] = 1  # Variable artificial
            variable_names.append(f"A{i + 1}")  # Variable artificial
            artificial_index += 1
    # Función objetivo con penalización M
    M = 1e6  # Usamos un valor numérico grande para M
    objective = np.zeros(total_vars, dtype=float)
    objective[:num_vars] = c if tipo_optimizacion == "min" else -np.array(c)
    for i, var in enumerate(variable_names):
        if var.startswith("A"):  # Penalizar variables artificiales
            objective[i] = M if tipo_optimizacion == "min" else -M
    tableau[-1, :-1] = objective
    base_variables = [var for var in variable_names if var.startswith("S") or var.startswith("A")]
    base_variables.append("Z")
    iteraciones = []
    while True:
        # Guardar la tabla actual para las iteraciones
        tabla_con_nombres = {
            "base": base_variables.copy(),
            "columnas": variable_names + ["RHS"],
            "valores": tableau.tolist(),
        }
        iteraciones.append(tabla_con_nombres)
        # Condición de optimalidad
        if all(val >= 0 for val in tableau[-1, :-1] if isinstance(val, (int, float))):
            break
        # Elegir columna pivote (variable entrante)
        pivot_col = np.argmin([val if isinstance(val, (int, float)) else np.inf for val in tableau[-1, :-1]])
        variable_entrante = variable_names[pivot_col]
        # Elegir fila pivote (variable saliente)
        ratios = []
        for i in range(num_restricciones):
            if tableau[i, pivot_col] > 0:  # Solo dividir si el valor en la columna pivote es positivo
                ratios.append(tableau[i, -1] / tableau[i, pivot_col])
            else:
                ratios.append(np.inf)  # Asignar infinito si no es válido
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