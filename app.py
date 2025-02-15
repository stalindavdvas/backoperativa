from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS
from methods.simplex import simplex
from methods.gran_m import gran_m
from methods.dos_fases import dos_fases
from methods.dual import dual
from methods.esquina_noroeste import esquina_noroeste
from methods.costo_minimo import costo_minimo
from methods.vogel import vogel
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
################ EJECUCION DE PROGRAMA ######################################
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)