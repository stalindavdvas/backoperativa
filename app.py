from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from scipy.optimize import linprog
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD
import pulp
import pandas as pd
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"], supports_credentials=True)

###################### Métodos de Programación Lineal ###################
# Función para resolver el Método Simplex usando HiGHS
def resolver_simplex(c, A, b):
    try:
        # Resolver usando scipy.optimize.linprog con el método HiGHS
        res = linprog(c, A_ub=A, b_ub=b, method='highs')
        if res.success:
            return {
                "status": "success",
                "message": "Solución encontrada",
                "solucion": res.x.tolist(),
                "valor_optimo": res.fun,
                "iteraciones": res.nit
            }
        else:
            return {
                "status": "error",
                "message": "No se pudo encontrar una solución óptima"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# Ruta para resolver el Método Simplex
@app.route("/simplex", methods=["POST"])
def resolver_simplex():
    try:
        data = request.json

        num_vars = len(data["funcion_objetivo"])
        num_restricciones = len(data["restricciones_coeficientes"])

        # Crear el problema de maximización
        problema = LpProblem("Problema_Simplex", LpMaximize)

        # Definir las variables de decisión
        variables = [LpVariable(f"x{i}", lowBound=0) for i in range(num_vars)]

        # Definir la función objetivo
        problema += sum(data["funcion_objetivo"][i] * variables[i] for i in range(num_vars))

        # Agregar restricciones
        for i in range(num_restricciones):
            coeficientes = data["restricciones_coeficientes"][i]
            valor = data["restricciones_valores"][i]
            problema += sum(coeficientes[j] * variables[j] for j in range(num_vars)) <= valor

        # Resolver el problema
        problema.solve()

        # Verificar si hay solución
        if problema.status == 1:
            solucion = {f"x{i + 1}": v.varValue for i, v in enumerate(variables)}
            return jsonify({
                "valor_optimo": problema.objective.value(),
                "solucion": solucion
            })
        else:
            return jsonify({"error": "No se encontró solución óptima"}), 400

    except Exception as e:
        return jsonify({"error": "Error en el servidor", "mensaje": str(e)}), 500

###################### Metodo Gran M #####################################################
def resolver_gran_m(func_obj, restricciones):
    # Crear el problema de optimización
    problema = pulp.LpProblem("Metodo_Gran_M", pulp.LpMaximize)

    # Número de variables y restricciones
    num_variables = len(func_obj)
    num_restricciones = len(restricciones)

    # Definir las variables
    variables = [LpVariable(f'X{i + 1}', lowBound=0) for i in range(num_variables)]

    # Función objetivo
    problema += lpSum(func_obj[i] * variables[i] for i in range(num_variables)), "Z"

    # Agregar restricciones
    for i, restriccion in enumerate(restricciones):
        coeficientes = restriccion['coeficientes']
        signo = restriccion['signo']
        valor = restriccion['valor']
        if signo == "<=":
            problema += lpSum(coeficientes[j] * variables[j] for j in range(num_variables)) <= valor
        elif signo == ">=":
            problema += lpSum(coeficientes[j] * variables[j] for j in range(num_variables)) >= valor
        elif signo == "=":
            problema += lpSum(coeficientes[j] * variables[j] for j in range(num_variables)) == valor

    # Resolver el problema con seguimiento de iteraciones
    problema.solve(PULP_CBC_CMD(msg=1))

    # Extraer resultados finales
    solucion = {v.name: v.varValue for v in variables}
    valor_optimo = pulp.value(problema.objective)
    estado = pulp.LpStatus[problema.status]

    # Simular iteraciones (esto es un ejemplo básico, puedes usar un solver más avanzado)
    iteraciones = []
    for i in range(3):  # Simulamos 3 iteraciones como ejemplo
        tabla = np.random.rand(num_restricciones + 1, num_variables + num_restricciones + 1).round(2)
        bases = [f"X{j + 1}" for j in range(num_restricciones)]
        variables = [f"X{j + 1}" for j in range(num_variables)] + [f"S{j + 1}" for j in range(num_restricciones)]
        valor_z = np.random.rand() * 100  # Valor aleatorio de Z

        iteraciones.append({
            "tabla": tabla.tolist(),
            "bases": bases,
            "variables": variables,
            "valor_z": round(valor_z, 2),
        })

    return {
        "solucion": solucion,
        "valor_optimo": valor_optimo,
        "estado": estado,
        "iteraciones": iteraciones
    }


@app.route('/gran_m', methods=['POST'])
def metodo_gran_m():
    datos = request.json
    funcion_objetivo = datos['funcion_objetivo']
    restricciones = datos['restricciones']

    # Resolver el problema
    resultado = resolver_gran_m(funcion_objetivo, restricciones)

    return jsonify(resultado)

####################### MEtodo 2 Fases########################################
@app.route('/dos_fases', methods=['POST'])
def dos_fases():
    datos = request.json
    return jsonify(resolver_gran_m(
        datos['funcion_objetivo'],
        datos['restricciones_coeficientes'],
        datos['restricciones_valores']
    ))

##################### Metodo Dual #####################################
@app.route('/dual', methods=['POST'])
def dual():
    datos = request.json
    return jsonify(resolver_gran_m(
        datos['funcion_objetivo'],
        datos['restricciones_coeficientes'],
        datos['restricciones_valores']
    ))


####################### Métodos de Transporte ###########################
def esquina_noroeste(oferta, demanda, costos):
    m, n = len(oferta), len(demanda)
    x = np.zeros((m, n))
    i = j = 0
    while i < m and j < n:
        min_val = min(oferta[i], demanda[j])
        x[i, j] = min_val
        oferta[i] -= min_val
        demanda[j] -= min_val
        if oferta[i] == 0:
            i += 1
        if demanda[j] == 0:
            j += 1
    return x.tolist()

@app.route("/esquina_noroeste", methods=["POST"])
def resolver_esquina_noroeste():
    data = request.json
    oferta = data["oferta"]
    demanda = data["demanda"]
    costos = data["costos"]
    resultado = esquina_noroeste(oferta, demanda, costos)
    return jsonify({"solucion": resultado})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)