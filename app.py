from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS
from methods.simplex import simplex
from methods.gran_m import gran_m
from methods.dos_fases import dos_fases
from methods.dual import dual
from methods.esquina_noroeste import esquina_noroeste
from methods.costo_minimo import costo_minimo
from methods.vogel import vogel
from methods.dijkstra import dijkstra
from utils.graph_utils import validate_graph_data
from collections import defaultdict
from methods.edmonds_karp import edmonds_karp
from methods.kruskal import kruskal
app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

###################### SIMPLEX ###########################################
@app.route('/simplex', methods=['POST'])
def resolver_simplex():
    try:
        data = request.json
        funcion_objetivo = data['funcion_objetivo']
        restricciones_coeficientes = data['restricciones_coeficientes']
        restricciones_valores = data['restricciones_valores']

        # Validar datos
        if not funcion_objetivo or not restricciones_coeficientes or not restricciones_valores:
            return jsonify({"error": "Datos incompletos"}), 400

        # Resolver el problema
        resultado = simplex(funcion_objetivo, restricciones_coeficientes, restricciones_valores)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


################### METODO GRAN M ###################################
@app.route('/gran-m', methods=['POST'])
def resolver_gran_m():
    try:
        data = request.json
        tipo_optimizacion = data['tipo_optimizacion']
        funcion_objetivo = data['funcion_objetivo']
        restricciones_coeficientes = data['restricciones_coeficientes']
        restricciones_signos = data['restricciones_signos']
        restricciones_valores = data['restricciones_valores']

        # Validar datos
        if not funcion_objetivo or not restricciones_coeficientes or not restricciones_signos or not restricciones_valores:
            return jsonify({"error": "Datos incompletos"}), 400

        # Resolver el problema
        resultado = gran_m(tipo_optimizacion, funcion_objetivo, restricciones_coeficientes, restricciones_signos,
                           restricciones_valores)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

######################### METODD DOS FASES ##################################
@app.route('/dos-fases', methods=['POST'])
def resolver_dos_fases():
    try:
        data = request.json
        tipo_optimizacion = data['tipo_optimizacion']
        funcion_objetivo = data['funcion_objetivo']
        restricciones_coeficientes = data['restricciones_coeficientes']
        restricciones_signos = data['restricciones_signos']
        restricciones_valores = data['restricciones_valores']

        # Validar datos
        if not funcion_objetivo or not restricciones_coeficientes or not restricciones_signos or not restricciones_valores:
            return jsonify({"error": "Datos incompletos"}), 400

        # Resolver el problema
        resultado = dos_fases(tipo_optimizacion, funcion_objetivo, restricciones_coeficientes, restricciones_signos,
                              restricciones_valores)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

######################## METODO DUAL #########################################
@app.route('/dual', methods=['POST'])
def resolver_dual():
    try:
        data = request.json
        funcion_objetivo = data['funcion_objetivo']
        restricciones_coeficientes = data['restricciones_coeficientes']
        restricciones_valores = data['restricciones_valores']

        # Validar datos
        if not funcion_objetivo or not restricciones_coeficientes or not restricciones_valores:
            return jsonify({"error": "Datos incompletos"}), 400

        # Resolver el problema dual
        resultado = dual(funcion_objetivo, restricciones_coeficientes, restricciones_valores)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
################## Metodos de Transporte: Esquina Noroeste######################
@app.route('/esquina-noroeste', methods=['POST'])
def resolver_esquina_noroeste():
    try:
        data = request.json
        origenes = data['origenes']
        destinos = data['destinos']
        matriz_costos = data['matriz_costos']
        ofertas = data['ofertas']
        demandas = data['demandas']

        # Validar datos
        if not origenes or not destinos or not matriz_costos or not ofertas or not demandas:
            return jsonify({"error": "Datos incompletos"}), 400

        # Resolver el problema
        resultado = esquina_noroeste({
            "origenes": origenes,
            "destinos": destinos,
            "matriz_costos": matriz_costos,
            "ofertas": ofertas,
            "demandas": demandas,
        })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
################## Metodos de Transporte: Costo Minimo######################
@app.route('/costo-minimo', methods=['POST'])
def resolver_costo_minimo():
    try:
        data = request.json
        origenes = data['origenes']
        destinos = data['destinos']
        matriz_costos = data['matriz_costos']
        ofertas = data['ofertas']
        demandas = data['demandas']

        # Validar datos
        if not origenes or not destinos or not matriz_costos or not ofertas or not demandas:
            return jsonify({"error": "Datos incompletos"}), 400

        # Resolver el problema
        resultado = costo_minimo({
            "origenes": origenes,
            "destinos": destinos,
            "matriz_costos": matriz_costos,
            "ofertas": ofertas,
            "demandas": demandas,
        })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
################## Metodos de Transporte: Vogel######################
@app.route('/vogel', methods=['POST'])
def resolver_vogel():
    try:
        data = request.json
        print("Datos recibidos:", data)

        origenes = data['origenes']
        destinos = data['destinos']
        matriz_costos = data['matriz_costos']
        ofertas = data['ofertas']
        demandas = data['demandas']

        # Validar datos
        if not origenes or not destinos or not matriz_costos or not ofertas or not demandas:
            return jsonify({"error": "Datos incompletos"}), 400

        # Resolver el problema
        resultado = vogel({
            "origenes": origenes,
            "destinos": destinos,
            "matriz_costos": matriz_costos,
            "ofertas": ofertas,
            "demandas": demandas,
        })

        print("Respuesta enviada al frontend:", resultado)  # Imprimir la respuesta completa
        return jsonify(resultado)
    except Exception as e:
        print("Error en el backend:", str(e))  # Imprimir el error detallado
        return jsonify({"error": str(e)}), 500


################### REDES: CAMINO MAS CORTO CON DIJKSTRA##############################
@app.route("/camino-mas-corto", methods=["POST"])
def calcular_camino_mas_corto():
    try:
        data = request.json

        # Extraer datos
        nodos = data.get("nodos")
        aristas = data.get("aristas")
        inicio = data.get("inicio")
        fin = data.get("fin")

        # Validar datos
        validate_graph_data(nodos, aristas, inicio, fin)

        # Calcular el camino más corto
        resultado = dijkstra(nodos, aristas, inicio, fin)
        return jsonify(resultado)
    except ValueError as ve:
        # Capturar errores de validación
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        # Capturar otros errores
        print("Error interno:", str(e))  # Imprimir el error en los logs del servidor
        return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500

########################### REDES FLUJO MAXIMO ##################################
@app.route("/flujo-maximo", methods=["POST"])
def calcular_flujo_maximo():
    try:
        data = request.json

        # Extraer datos
        nodos = data.get("nodos")
        aristas = data.get("aristas")
        fuente = data.get("fuente")
        sumidero = data.get("sumidero")

        # Validar datos
        if not nodos or not isinstance(nodos, list) or len(nodos) == 0:
            return jsonify({"error": "La lista de nodos está vacía o no es válida."}), 400
        if not aristas or not isinstance(aristas, list) or len(aristas) == 0:
            return jsonify({"error": "La lista de aristas está vacía o no es válida."}), 400
        if not fuente or not sumidero or fuente not in nodos or sumidero not in nodos:
            return jsonify({"error": "Los nodos fuente y sumidero son inválidos o no existen en la red."}), 400

        # Construir el grafo
        grafo = {}
        for arista in aristas:
            u, v, capacidad = arista["from"], arista["to"], arista["capacidad"]
            if u not in grafo:
                grafo[u] = {}
            grafo[u][v] = capacidad

        # Calcular el flujo máximo
        flujo_maximo, aristas_utilizadas = edmonds_karp(grafo, fuente, sumidero)

        return jsonify({
            "flujo_maximo": flujo_maximo,
            "aristas_utilizadas": aristas_utilizadas,
        })
    except Exception as e:
        print("Error interno:", str(e))  # Imprimir el error en los logs del servidor
        return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500
######################## REDES ARBOL EXPANSION MINIMA ################################
@app.route("/mst", methods=["POST"])
def calcular_mst():
    try:
        data = request.json

        # Extraer datos
        nodos = data.get("nodos")
        aristas = data.get("aristas")

        # Validar datos
        if not nodos or not isinstance(nodos, list) or len(nodos) == 0:
            return jsonify({"error": "La lista de nodos está vacía o no es válida."}), 400
        if not aristas or not isinstance(aristas, list) or len(aristas) == 0:
            return jsonify({"error": "La lista de aristas está vacía o no es válida."}), 400

        # Calcular el MST
        costo_total, aristas_mst = kruskal(nodos, aristas)

        return jsonify({
            "costo_total": costo_total,
            "aristas_mst": aristas_mst,
        })
    except Exception as e:
        print("Error interno:", str(e))  # Imprimir el error en los logs del servidor
        return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500
################ EJECUCION DE PROGRAMA ######################################
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)